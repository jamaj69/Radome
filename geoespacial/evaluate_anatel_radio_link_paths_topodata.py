#!/usr/bin/env python3
"""Calcula TOPODATA, curvatura e Fresnel por caminho cadastral nao ambiguo."""

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
from evaluate_anatel_radio_link_terrain import classify, profile
from evaluate_anatel_radio_link_topodata import Topodata

PATH_FIELDS = (
    "candidate_id", "path_id", "link_family", "service_fistel", "rf_act_number",
    "source_coordinate", "destination_coordinate", "frequency_mhz",
    "source_height_m", "destination_height_m", "distance_km", "terrain_samples",
    "missing_samples", "minimum_los_clearance_k1_m",
    "minimum_fresnel60_clearance_k1_m", "minimum_los_clearance_k4_3_m",
    "minimum_fresnel60_clearance_k4_3_m", "terrain_status_k1",
    "terrain_status_k4_3", "height_audit_status", "pairing_status",
    "terrain_source", "height_semantics",
)
CANDIDATE_FIELDS = (
    "candidate_id", "link_family", "service_fistel", "rf_act_number",
    "evaluated_path_count", "fresnel60_clear_paths_k1", "los_only_paths_k1",
    "obstructed_paths_k1", "terrain_missing_paths_k1", "candidate_status_k1",
    "fresnel60_clear_paths_k4_3", "los_only_paths_k4_3",
    "obstructed_paths_k4_3", "terrain_missing_paths_k4_3",
    "candidate_status_k4_3", "pairing_status",
)


def candidate_status(counts: Counter) -> str:
    if counts["fresnel60_clear"]:
        return "at_least_one_fresnel60_clear_path"
    if counts["los_clear_fresnel_obstructed"]:
        return "at_least_one_los_only_path"
    if counts["terrain_or_curvature_obstructed"]:
        return "all_evaluable_paths_obstructed"
    return "terrain_missing_for_all_paths"


def evaluate(geometry: Path, audited_paths: Path, terrain_root: Path, terrain_index: Path, paths_output: Path, candidates_output: Path, report: Path) -> dict:
    geometry_by_candidate = {}
    with gzip.open(geometry, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            geometry_by_candidate[row["candidate_id"]] = row
    with gzip.open(audited_paths, "rt", encoding="utf-8", newline="") as stream:
        audited_rows = list(csv.DictReader(stream))
    usable = [row for row in audited_rows if row["height_audit_status"] == "unambiguous_cadastral_height"]

    sampler = Topodata(terrain_root, terrain_index)
    path_rows = []
    grouped = defaultdict(list)
    try:
        for row in usable:
            source = tuple(map(float, row["source_coordinate"].split(",")))
            destination = tuple(map(float, row["destination_coordinate"].split(",")))
            distance = float(geometry_by_candidate[row["candidate_id"]]["distance_km"])
            k1 = profile(source, destination, distance, float(row["source_height_m"]), float(row["destination_height_m"]), float(row["frequency_mhz"]), sampler, k=1)
            k43 = profile(source, destination, distance, float(row["source_height_m"]), float(row["destination_height_m"]), float(row["frequency_mhz"]), sampler, k=4 / 3)
            result = {
                "candidate_id": row["candidate_id"], "path_id": row["path_id"],
                "link_family": row["link_family"], "service_fistel": row["service_fistel"],
                "rf_act_number": row["rf_act_number"], "source_coordinate": row["source_coordinate"],
                "destination_coordinate": row["destination_coordinate"], "frequency_mhz": row["frequency_mhz"],
                "source_height_m": row["source_height_m"], "destination_height_m": row["destination_height_m"],
                "distance_km": distance, "terrain_samples": k1["samples"],
                "missing_samples": max(k1["missing"], k43["missing"]),
                "minimum_los_clearance_k1_m": "" if k1["los"] is None else k1["los"],
                "minimum_fresnel60_clearance_k1_m": "" if k1["fresnel"] is None else k1["fresnel"],
                "minimum_los_clearance_k4_3_m": "" if k43["los"] is None else k43["los"],
                "minimum_fresnel60_clearance_k4_3_m": "" if k43["fresnel"] is None else k43["fresnel"],
                "terrain_status_k1": classify(k1), "terrain_status_k4_3": classify(k43),
                "height_audit_status": row["height_audit_status"], "pairing_status": "not_performed",
                "terrain_source": "TOPODATA/INPE numeric altitude GeoTIFF",
                "height_semantics": "one internally unambiguous Anatel cadastral height per directed frequency endpoint; not physically verified",
            }
            path_rows.append(result)
            grouped[row["candidate_id"]].append(result)
    finally:
        sampler.close()

    candidate_rows = []
    candidate_counts1, candidate_counts43 = Counter(), Counter()
    for candidate_id in sorted(grouped):
        rows = grouped[candidate_id]
        counts1 = Counter(row["terrain_status_k1"] for row in rows)
        counts43 = Counter(row["terrain_status_k4_3"] for row in rows)
        status1, status43 = candidate_status(counts1), candidate_status(counts43)
        candidate_counts1[status1] += 1
        candidate_counts43[status43] += 1
        first = rows[0]
        candidate_rows.append({
            "candidate_id": candidate_id, "link_family": first["link_family"],
            "service_fistel": first["service_fistel"], "rf_act_number": first["rf_act_number"],
            "evaluated_path_count": len(rows), "fresnel60_clear_paths_k1": counts1["fresnel60_clear"],
            "los_only_paths_k1": counts1["los_clear_fresnel_obstructed"],
            "obstructed_paths_k1": counts1["terrain_or_curvature_obstructed"],
            "terrain_missing_paths_k1": counts1["terrain_missing"], "candidate_status_k1": status1,
            "fresnel60_clear_paths_k4_3": counts43["fresnel60_clear"],
            "los_only_paths_k4_3": counts43["los_clear_fresnel_obstructed"],
            "obstructed_paths_k4_3": counts43["terrain_or_curvature_obstructed"],
            "terrain_missing_paths_k4_3": counts43["terrain_missing"], "candidate_status_k4_3": status43,
            "pairing_status": "not_performed",
        })

    paths_output.parent.mkdir(parents=True, exist_ok=True)
    candidates_output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="link-path-terrain-", dir=paths_output.parent) as directory:
        staged_paths = Path(directory) / paths_output.name
        staged_candidates = Path(directory) / candidates_output.name
        with deterministic_gzip_csv(staged_paths, PATH_FIELDS) as writer:
            writer.writerows(path_rows)
        with deterministic_gzip_csv(staged_candidates, CANDIDATE_FIELDS) as writer:
            writer.writerows(candidate_rows)
        os.replace(staged_paths, paths_output)
        os.replace(staged_candidates, candidates_output)

    path_counts1 = Counter(row["terrain_status_k1"] for row in path_rows)
    path_counts43 = Counter(row["terrain_status_k4_3"] for row in path_rows)
    result = {
        "schema_version": 1, "geometry_file": str(geometry), "geometry_sha256": sha256_file(geometry),
        "audited_paths_file": str(audited_paths), "audited_paths_sha256": sha256_file(audited_paths),
        "terrain_index": str(terrain_index), "terrain_index_sha256": sha256_file(terrain_index),
        "evaluated_path_count": len(path_rows), "evaluated_candidate_count": len(candidate_rows),
        "excluded_ambiguous_or_missing_path_count": len(audited_rows) - len(path_rows),
        "path_status_k1": dict(sorted(path_counts1.items())), "path_status_k4_3": dict(sorted(path_counts43.items())),
        "candidate_status_k1": dict(sorted(candidate_counts1.items())), "candidate_status_k4_3": dict(sorted(candidate_counts43.items())),
        "sample_spacing_km": 1.0, "curvature_models": [1.0, 4 / 3], "fresnel_clearance_fraction": 0.6,
        "height_semantics": "internally unambiguous cadastral values, not physical verification",
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
    parser.add_argument("--audited-paths", type=Path, required=True)
    parser.add_argument("--terrain-root", type=Path, required=True)
    parser.add_argument("--terrain-index", type=Path, required=True)
    parser.add_argument("--paths-output", type=Path, required=True)
    parser.add_argument("--candidates-output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(evaluate(args.geometry, args.audited_paths, args.terrain_root, args.terrain_index, args.paths_output, args.candidates_output, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
