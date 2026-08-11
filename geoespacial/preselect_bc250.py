#!/usr/bin/env python3
"""Create a traceable continental preselection from IBGE BC250 point layers.

This is a screening tool. Nearby cities are a logistics proxy, not a terrain
viewshed, and BC250 quoted points are too sparse to replace a DEM.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

EARTH_RADIUS_KM = 6371.0088


@dataclass(frozen=True)
class Point:
    name: str
    longitude: float
    latitude: float
    elevation_m: float | None = None


def distance_km(a: Point, b: Point) -> float:
    lat1, lat2 = math.radians(a.latitude), math.radians(b.latitude)
    dlat = lat2 - lat1
    dlon = math.radians(b.longitude - a.longitude)
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(h))


def azimuth_sector(origin: Point, target: Point, sectors: int = 8) -> int:
    lat1, lat2 = math.radians(origin.latitude), math.radians(target.latitude)
    dlon = math.radians(target.longitude - origin.longitude)
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    bearing = (math.degrees(math.atan2(y, x)) + 360.0) % 360.0
    return min(int(bearing / (360.0 / sectors)), sectors - 1)


def normalize(values: list[float]) -> list[float]:
    low, high = min(values), max(values)
    if high == low:
        return [0.0 for _ in values]
    return [(value - low) / (high - low) for value in values]


def open_layer(dataset: object, name: str) -> object:
    layer = dataset.GetLayerByName(name)
    if layer is None:
        raise ValueError(f"missing BC250 layer: {name}")
    return layer


def read_points(dataset: object) -> tuple[list[Point], list[Point], list[Point]]:
    quoted = []
    for feature in open_layer(dataset, "rel_ponto_cotado_altimetrico_p"):
        geometry = feature.GetGeometryRef()
        quoted.append(Point(f"BC250-{feature.GetFID()}", geometry.GetX(), geometry.GetY(), feature["cota"]))
    peaks = []
    for feature in open_layer(dataset, "rel_pico_p"):
        geometry = feature.GetGeometryRef()
        peaks.append(Point(feature["nome"] or f"Pico-{feature.GetFID()}", geometry.GetX(), geometry.GetY()))
    cities = []
    for layer_name in ("lml_cidade_p", "lml_capital_p"):
        for feature in open_layer(dataset, layer_name):
            geometry = feature.GetGeometryRef()
            # Oceanic localities are outside the active continental scope.
            if geometry.GetX() <= -34.0:
                cities.append(Point(feature["nome"] or f"Cidade-{feature.GetFID()}", geometry.GetX(), geometry.GetY()))
    return quoted, peaks, cities


def deduplicate(candidates: list[Point], spacing_km: float) -> list[Point]:
    selected: list[Point] = []
    for point in sorted(candidates, key=lambda item: item.elevation_m or 0.0, reverse=True):
        if all(distance_km(point, other) >= spacing_km for other in selected):
            selected.append(point)
    return selected


def analyse(candidates: list[Point], peaks: list[Point], cities: list[Point], radius_km: float) -> list[dict[str, object]]:
    rows = []
    for candidate in candidates:
        nearby = [(distance_km(candidate, city), city) for city in cities]
        nearby.sort(key=lambda pair: pair[0])
        inside = [(distance, city) for distance, city in nearby if distance <= radius_km]
        sectors = {azimuth_sector(candidate, city) for _, city in inside}
        nearest_peak = min(peaks, key=lambda peak: distance_km(candidate, peak)) if peaks else None
        rows.append({
            "candidate_id": candidate.name,
            "longitude": candidate.longitude,
            "latitude": candidate.latitude,
            "elevation_m": candidate.elevation_m,
            "nearest_named_peak": nearest_peak.name if nearest_peak and distance_km(candidate, nearest_peak) <= 5 else "",
            "nearest_city": nearby[0][1].name if nearby else "",
            "nearest_city_km": nearby[0][0] if nearby else None,
            "cities_within_radius": len(inside),
            "occupied_azimuth_sectors": len(sectors),
            "logistics_radius_km": radius_km,
        })
    elevations = normalize([float(row["elevation_m"]) for row in rows])
    city_scores = normalize([math.log1p(int(row["cities_within_radius"])) for row in rows])
    sector_scores = [int(row["occupied_azimuth_sectors"]) / 8.0 for row in rows]
    for row, elevation, city_score, sector_score in zip(rows, elevations, city_scores, sector_scores, strict=True):
        row["screening_score"] = 0.60 * elevation + 0.25 * city_score + 0.15 * sector_score
    return sorted(rows, key=lambda row: float(row["screening_score"]), reverse=True)


def write_results(rows: list[dict[str, object]], csv_path: Path, geojson_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    features = [{
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [row["longitude"], row["latitude"]]},
        "properties": {key: value for key, value in row.items() if key not in {"longitude", "latitude"}},
    } for row in rows]
    geojson_path.write_text(json.dumps({
        "type": "FeatureCollection",
        "name": "bc250_continental_preselection",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4674"}},
        "features": features,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    from osgeo import ogr

    parser = argparse.ArgumentParser()
    parser.add_argument("bc250", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("reports/preselection_bc250"))
    parser.add_argument("--city-radius-km", type=float, default=250.0)
    parser.add_argument("--candidate-spacing-km", type=float, default=10.0)
    args = parser.parse_args()
    dataset = ogr.Open(str(args.bc250), 0)
    if dataset is None:
        raise SystemExit(f"cannot open {args.bc250}")
    quoted, peaks, cities = read_points(dataset)
    candidates = deduplicate(quoted, args.candidate_spacing_km)
    rows = analyse(candidates, peaks, cities, args.city_radius_km)
    write_results(rows, args.output_dir / "candidates.csv", args.output_dir / "candidates.geojson")
    print(json.dumps({
        "quoted_points": len(quoted), "deduplicated_candidates": len(candidates),
        "named_peaks": len(peaks), "continental_city_records": len(cities),
        "output_dir": str(args.output_dir),
    }, indent=2))


if __name__ == "__main__":
    main()
