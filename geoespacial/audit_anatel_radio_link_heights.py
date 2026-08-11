#!/usr/bin/env python3
"""Audita alturas cadastrais por caminho reciproco sem formar enlaces."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from build_canonical_smp import deterministic_gzip_csv, sha256_file

PATH_FIELDS = (
    "candidate_id", "link_family", "service_fistel", "rf_act_number", "path_id",
    "source_coordinate", "destination_coordinate", "frequency_mhz",
    "source_height_values_m", "destination_height_values_m", "source_height_m",
    "destination_height_m", "source_antenna_product_codes",
    "destination_antenna_product_codes", "source_record_count",
    "destination_record_count", "height_audit_status", "pairing_status",
)
CANDIDATE_FIELDS = (
    "candidate_id", "link_family", "service_fistel", "rf_act_number",
    "reciprocal_path_observations", "unambiguous_height_paths",
    "ambiguous_height_paths", "missing_height_paths", "height_audit_status",
    "terrain_status_k1", "terrain_status_k4_3", "pairing_status",
)


def coordinate(row: dict) -> tuple[float, float]:
    return float(row["latitude"]), float(row["longitude"])


def value_set(rows: list[dict], field: str) -> list[str]:
    return sorted({row[field] for row in rows if row.get(field)}, key=lambda value: float(value) if field == "antenna_height_m" else value)


def classify_heights(source_values: list[str], destination_values: list[str]) -> str:
    if not source_values or not destination_values:
        return "missing_height"
    if len(source_values) == 1 and len(destination_values) == 1:
        return "unambiguous_cadastral_height"
    return "ambiguous_cadastral_height"


def audit(geometry: Path, keys: Path, emissions: Path, terrain: Path, paths_output: Path, candidates_output: Path, report: Path) -> dict:
    selected = {}
    with gzip.open(geometry, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["geometry_status"] == "azimuth_consistent_15deg":
                key = row["link_family"], row["service_fistel"], row["rf_act_number"]
                selected[key] = row

    key_rows = {}
    with gzip.open(keys, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            key = row["link_family"], row["service_fistel"], row["rf_act_number"]
            if key in selected:
                key_rows[row["source_row_number"]] = (key, row)

    grouped = defaultdict(lambda: defaultdict(list))
    with gzip.open(emissions, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            match = key_rows.get(row["source_row_number"])
            if match:
                key, key_row = match
                enriched = dict(row)
                enriched["antenna_product_code"] = key_row["antenna_product_code"]
                grouped[key][coordinate(row)].append(enriched)

    terrain_by_candidate = {}
    with gzip.open(terrain, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            terrain_by_candidate[row["candidate_id"]] = row

    path_rows, candidate_rows = [], []
    path_counts, candidate_counts = Counter(), Counter()
    for key in sorted(selected):
        geometry_row = selected[key]
        endpoints = grouped[key]
        a = tuple(map(float, geometry_row["coordinate_a"].split(",")))
        b = tuple(map(float, geometry_row["coordinate_b"].split(",")))
        candidate_paths = []
        for source, destination in ((a, b), (b, a)):
            source_frequencies = {row["frequency_mhz"] for row in endpoints[source] if row["direction"] == "Transmissão" and row["frequency_mhz"]}
            destination_frequencies = {row["frequency_mhz"] for row in endpoints[destination] if row["direction"] == "Recepção" and row["frequency_mhz"]}
            for frequency in sorted(source_frequencies & destination_frequencies, key=float):
                source_rows = [row for row in endpoints[source] if row["direction"] == "Transmissão" and row["frequency_mhz"] == frequency]
                destination_rows = [row for row in endpoints[destination] if row["direction"] == "Recepção" and row["frequency_mhz"] == frequency]
                source_heights = value_set(source_rows, "antenna_height_m")
                destination_heights = value_set(destination_rows, "antenna_height_m")
                status = classify_heights(source_heights, destination_heights)
                path_counts[status] += 1
                path_id = f"{geometry_row['candidate_id']}:p{len(candidate_paths) + 1:03d}"
                candidate_paths.append(status)
                path_rows.append({
                    "candidate_id": geometry_row["candidate_id"], "link_family": key[0],
                    "service_fistel": key[1], "rf_act_number": key[2], "path_id": path_id,
                    "source_coordinate": f"{source[0]},{source[1]}",
                    "destination_coordinate": f"{destination[0]},{destination[1]}",
                    "frequency_mhz": frequency, "source_height_values_m": "|".join(source_heights),
                    "destination_height_values_m": "|".join(destination_heights),
                    "source_height_m": source_heights[0] if len(source_heights) == 1 else "",
                    "destination_height_m": destination_heights[0] if len(destination_heights) == 1 else "",
                    "source_antenna_product_codes": "|".join(value_set(source_rows, "antenna_product_code")),
                    "destination_antenna_product_codes": "|".join(value_set(destination_rows, "antenna_product_code")),
                    "source_record_count": len(source_rows), "destination_record_count": len(destination_rows),
                    "height_audit_status": status, "pairing_status": "not_performed",
                })
        counts = Counter(candidate_paths)
        if counts["unambiguous_cadastral_height"]:
            candidate_status = "usable_cadastral_path_present"
        elif counts["ambiguous_cadastral_height"]:
            candidate_status = "ambiguous_height_only"
        else:
            candidate_status = "missing_height_only"
        candidate_counts[candidate_status] += 1
        terrain_row = terrain_by_candidate[geometry_row["candidate_id"]]
        candidate_rows.append({
            "candidate_id": geometry_row["candidate_id"], "link_family": key[0],
            "service_fistel": key[1], "rf_act_number": key[2],
            "reciprocal_path_observations": len(candidate_paths),
            "unambiguous_height_paths": counts["unambiguous_cadastral_height"],
            "ambiguous_height_paths": counts["ambiguous_cadastral_height"],
            "missing_height_paths": counts["missing_height"], "height_audit_status": candidate_status,
            "terrain_status_k1": terrain_row["terrain_status_k1"],
            "terrain_status_k4_3": terrain_row["terrain_status_k4_3"], "pairing_status": "not_performed",
        })

    paths_output.parent.mkdir(parents=True, exist_ok=True)
    candidates_output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="link-heights-", dir=paths_output.parent) as directory:
        staged_paths = Path(directory) / paths_output.name
        staged_candidates = Path(directory) / candidates_output.name
        with deterministic_gzip_csv(staged_paths, PATH_FIELDS) as writer:
            writer.writerows(path_rows)
        with deterministic_gzip_csv(staged_candidates, CANDIDATE_FIELDS) as writer:
            writer.writerows(candidate_rows)
        os.replace(staged_paths, paths_output)
        os.replace(staged_candidates, candidates_output)

    result = {
        "schema_version": 1, "geometry_file": str(geometry), "geometry_sha256": sha256_file(geometry),
        "keys_file": str(keys), "keys_sha256": sha256_file(keys), "emissions_file": str(emissions),
        "emissions_sha256": sha256_file(emissions), "terrain_file": str(terrain), "terrain_sha256": sha256_file(terrain),
        "candidate_count": len(candidate_rows), "reciprocal_path_observation_count": len(path_rows),
        "path_height_status": dict(sorted(path_counts.items())), "candidate_height_status": dict(sorted(candidate_counts.items())),
        "height_semantics": "Anatel cadastral antenna height; one unique value per directed reciprocal-frequency endpoint is internally unambiguous but not physically verified",
        "pairing_status": "not_performed", "paths_output": str(paths_output), "candidates_output": str(candidates_output),
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(prefix=f".{report.name}.", dir=report.parent, delete=False) as stream:
        stream.write(payload)
        temporary = Path(stream.name)
    os.replace(temporary, report)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--geometry", type=Path, required=True)
    parser.add_argument("--keys", type=Path, required=True)
    parser.add_argument("--emissions", type=Path, required=True)
    parser.add_argument("--terrain", type=Path, required=True)
    parser.add_argument("--paths-output", type=Path, required=True)
    parser.add_argument("--candidates-output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.geometry, args.keys, args.emissions, args.terrain, args.paths_output, args.candidates_output, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
