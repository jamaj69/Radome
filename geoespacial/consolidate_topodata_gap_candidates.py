#!/usr/bin/env /home/python/pyenv/bin/python
"""Triagem multiescala e consolidação espacial das sementes TOPODATA."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import os
import tempfile
from collections import Counter
from pathlib import Path

from build_canonical_smp import deterministic_gzip_csv, sha256_file
from enrich_candidate_geospatial_context import distance_km
from evaluate_anatel_radio_link_topodata import Topodata


EARTH_RADIUS_KM = 6371.0088
RADII_KM = (5.0, 10.0, 25.0)
SEMANTICS = (
    "ring clearance is seed elevation minus maximum TOPODATA sample on a geodesic ring; "
    "it is a multi-scale summit/ridge screening proxy, not topographic prominence, viewshed, "
    "line of sight, RF coverage, or site approval"
)


def destination(latitude: float, longitude: float, distance: float, bearing_degrees: float) -> tuple[float, float]:
    angular = distance / EARTH_RADIUS_KM
    latitude_1 = math.radians(latitude)
    longitude_1 = math.radians(longitude)
    bearing = math.radians(bearing_degrees)
    latitude_2 = math.asin(
        math.sin(latitude_1) * math.cos(angular)
        + math.cos(latitude_1) * math.sin(angular) * math.cos(bearing)
    )
    longitude_2 = longitude_1 + math.atan2(
        math.sin(bearing) * math.sin(angular) * math.cos(latitude_1),
        math.cos(angular) - math.sin(latitude_1) * math.sin(latitude_2),
    )
    return math.degrees(latitude_2), ((math.degrees(longitude_2) + 540) % 360) - 180


def ring_clearance(
    terrain: Topodata,
    latitude: float,
    longitude: float,
    elevation: float,
    radius_km: float,
    azimuth_count: int,
) -> tuple[float | None, int]:
    values = []
    for index in range(azimuth_count):
        point = destination(latitude, longitude, radius_km, index * 360.0 / azimuth_count)
        value = terrain(*point)
        if value is not None:
            values.append(value)
    return (None if not values else elevation - max(values), len(values))


def normalize(rows: list[dict], key: str) -> dict[str, float]:
    values = [float(row[key]) for row in rows]
    low, high = min(values), max(values)
    return {row["seed_id"]: (0.0 if high == low else (float(row[key]) - low) / (high - low)) for row in rows}


def consolidate(rows: list[dict], minimum_distance_km: float) -> tuple[list[dict], dict[str, str]]:
    ordered = sorted(rows, key=lambda row: (-float(row["terrain_score"]), row["seed_id"]))
    selected: list[dict] = []
    assignment: dict[str, str] = {}
    for row in ordered:
        neighbours = [
            candidate for candidate in selected
            if distance_km(float(row["latitude"]), float(row["longitude"]), float(candidate["latitude"]), float(candidate["longitude"]))
            < minimum_distance_km
        ]
        if neighbours:
            winner = min(neighbours, key=lambda candidate: (
                distance_km(float(row["latitude"]), float(row["longitude"]), float(candidate["latitude"]), float(candidate["longitude"])),
                candidate["seed_id"],
            ))
            assignment[row["seed_id"]] = winner["seed_id"]
        else:
            selected.append(row)
            assignment[row["seed_id"]] = row["seed_id"]
    return sorted(selected, key=lambda row: row["seed_id"]), assignment


def screen(
    seeds_path: Path,
    terrain_root: Path,
    terrain_index: Path,
    output_dir: Path,
    report_path: Path,
    minimum_distance_km: float = 10.0,
    azimuth_count: int = 36,
) -> dict:
    if minimum_distance_km <= 0 or azimuth_count < 8:
        raise ValueError("distância mínima deve ser positiva e azimuth_count >= 8")
    with gzip.open(seeds_path, "rt", encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    terrain = Topodata(terrain_root, terrain_index)
    try:
        for row in rows:
            clearances = {}
            for radius in RADII_KM:
                clearance, count = ring_clearance(
                    terrain, float(row["latitude"]), float(row["longitude"]), float(row["elevation_m"]), radius, azimuth_count,
                )
                suffix = str(int(radius))
                clearance = clearance if count == azimuth_count else None
                clearances[suffix] = clearance
                row[f"ring_{suffix}km_sample_count"] = count
                row[f"ring_{suffix}km_clearance_m"] = "" if clearance is None else round(clearance, 3)
            available = [value for value in clearances.values() if value is not None]
            positives = sum(value > 0 for value in available)
            row["multiscale_status"] = (
                "terrain_ring_incomplete" if len(available) < len(RADII_KM)
                else "summit_like_all_scales" if positives == len(RADII_KM)
                else "ridge_or_summit_partial" if positives > 0
                else "connected_or_higher_nearby"
            )
            row["positive_ring_scale_count"] = positives
    finally:
        terrain.close()

    elevation_score = normalize(rows, "elevation_m")
    relief_score = normalize(rows, "relative_relief_m")
    for row in rows:
        positive_clearance = sum(max(0.0, float(row[f"ring_{int(radius)}km_clearance_m"] or 0.0)) for radius in RADII_KM)
        row["positive_clearance_sum_m"] = round(positive_clearance, 3)
    clearance_score = normalize(rows, "positive_clearance_sum_m")
    for row in rows:
        row["terrain_score"] = round(
            0.50 * elevation_score[row["seed_id"]]
            + 0.30 * relief_score[row["seed_id"]]
            + 0.20 * clearance_score[row["seed_id"]], 9,
        )

    selected, assignment = consolidate(rows, minimum_distance_km)
    represented: dict[str, list[str]] = {row["seed_id"]: [] for row in selected}
    for row in rows:
        represented[assignment[row["seed_id"]]].append(row["cell_id"])
    output_rows = []
    for row in selected:
        output_rows.append({
            **row,
            "candidate_id": row["seed_id"].replace("gap-seed:", "gap-candidate:"),
            "represented_cell_count": len(represented[row["seed_id"]]),
            "represented_cell_ids": "|".join(sorted(represented[row["seed_id"]])),
            "minimum_distance_km": minimum_distance_km,
            "semantics": SEMANTICS,
        })

    output_dir.mkdir(parents=True, exist_ok=True)
    table = output_dir / "gap_candidates.csv.gz"
    with deterministic_gzip_csv(table, tuple(output_rows[0])) as writer:
        writer.writerows(output_rows)
    geojson = output_dir / "gap_candidates.geojson"
    geojson.write_text(json.dumps({
        "type": "FeatureCollection", "name": "topodata_gap_candidates_multiscale_screening",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": [{
            "type": "Feature", "geometry": {"type": "Point", "coordinates": [float(row["longitude"]), float(row["latitude"])]},
            "properties": {key: value for key, value in row.items() if key not in {"longitude", "latitude", "semantics", "represented_cell_ids"}},
        } for row in output_rows],
    }, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    report = {
        "schema_version": 1, "seeds_file": str(seeds_path), "seeds_sha256": sha256_file(seeds_path),
        "terrain_index": str(terrain_index), "terrain_index_sha256": sha256_file(terrain_index),
        "input_seed_count": len(rows), "candidate_count": len(output_rows),
        "represented_cell_count": len({cell for cells in represented.values() for cell in cells}),
        "minimum_distance_km": minimum_distance_km, "ring_radii_km": list(RADII_KM),
        "ring_azimuth_count": azimuth_count,
        "complete_ring_counts": {
            str(int(radius)): sum(int(row[f"ring_{int(radius)}km_sample_count"]) == azimuth_count for row in rows)
            for radius in RADII_KM
        },
        "multiscale_status_counts": dict(sorted(Counter(row["multiscale_status"] for row in rows).items())),
        "candidate_count_by_uf": dict(sorted(Counter(row["uf"] for row in output_rows).items())),
        "outputs": {"table": {"path": str(table), "sha256": sha256_file(table)}, "geojson": {"path": str(geojson), "sha256": sha256_file(geojson)}},
        "semantics": SEMANTICS,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(prefix=f".{report_path.name}.", dir=report_path.parent, delete=False) as target:
        target.write(payload)
        temporary = Path(target.name)
    os.replace(temporary, report_path)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=Path, required=True)
    parser.add_argument("--terrain-root", type=Path, required=True)
    parser.add_argument("--terrain-index", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--minimum-distance-km", type=float, default=10.0)
    parser.add_argument("--azimuth-count", type=int, default=36)
    args = parser.parse_args()
    print(json.dumps(screen(args.seeds, args.terrain_root, args.terrain_index, args.output_dir, args.report, args.minimum_distance_km, args.azimuth_count), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
