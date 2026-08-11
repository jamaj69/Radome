#!/usr/bin/env python3
"""Compara inclinacoes Anatel com a geometria vertical TOPODATA por caminho."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import os
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from build_candidate_graph import EARTH_RADIUS_M
from build_canonical_smp import deterministic_gzip_csv, sha256_file
from evaluate_anatel_radio_link_topodata import Topodata

THRESHOLDS = (0.5, 1.0, 2.0, 5.0)
FIELDS = (
    "candidate_id", "path_id", "link_family", "service_fistel", "rf_act_number",
    "source_coordinate", "destination_coordinate", "frequency_mhz", "distance_km",
    "source_terrain_m", "destination_terrain_m", "source_height_m",
    "destination_height_m", "source_top_m", "destination_top_m",
    "registered_source_elevation_deg", "registered_destination_elevation_deg",
    "derived_source_elevation_k1_deg", "derived_destination_elevation_k1_deg",
    "maximum_two_end_error_k1_deg", "derived_source_elevation_k4_3_deg",
    "derived_destination_elevation_k4_3_deg", "maximum_two_end_error_k4_3_deg",
    "vertical_status_k1", "vertical_status_k4_3", "pairing_status",
    "vertical_semantics",
)


def elevation_angle(distance_m: float, source_altitude_m: float, destination_altitude_m: float, k: float) -> float:
    radius = EARTH_RADIUS_M * k
    central_angle = distance_m / radius
    vertical = (radius + destination_altitude_m) * math.cos(central_angle) - (radius + source_altitude_m)
    horizontal = (radius + destination_altitude_m) * math.sin(central_angle)
    return math.degrees(math.atan2(vertical, horizontal))


def angular_error(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def status(error: float | None, threshold: float = 1.0) -> str:
    if error is None:
        return "vertical_geometry_missing"
    return "vertical_consistent_1deg" if error <= threshold else "vertical_inconsistent_1deg"


def validate(paths: Path, keys: Path, emissions: Path, terrain_root: Path, terrain_index: Path, output: Path, report: Path) -> dict:
    path_rows = []
    with gzip.open(paths, "rt", encoding="utf-8", newline="") as stream:
        path_rows = list(csv.DictReader(stream))
    selected_keys = {(row["link_family"], row["service_fistel"], row["rf_act_number"]) for row in path_rows}
    source_keys = {}
    with gzip.open(keys, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            key = row["link_family"], row["service_fistel"], row["rf_act_number"]
            if key in selected_keys:
                source_keys[row["source_row_number"]] = key
    grouped = defaultdict(list)
    with gzip.open(emissions, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            key = source_keys.get(row["source_row_number"])
            if key:
                grouped[key].append(row)

    sampler = Topodata(terrain_root, terrain_index)
    results = []
    sensitivity1 = Counter()
    sensitivity43 = Counter()
    candidate_pass1 = {threshold: set() for threshold in THRESHOLDS}
    candidate_pass43 = {threshold: set() for threshold in THRESHOLDS}
    try:
        for row in path_rows:
            key = row["link_family"], row["service_fistel"], row["rf_act_number"]
            source = tuple(map(float, row["source_coordinate"].split(",")))
            destination = tuple(map(float, row["destination_coordinate"].split(",")))
            frequency = row["frequency_mhz"]
            source_angles = {
                item["elevation_angle_deg"] for item in grouped[key]
                if (float(item["latitude"]), float(item["longitude"])) == source
                and item["direction"] == "Transmissão" and item["frequency_mhz"] == frequency
                and item["elevation_angle_deg"]
            }
            destination_angles = {
                item["elevation_angle_deg"] for item in grouped[key]
                if (float(item["latitude"]), float(item["longitude"])) == destination
                and item["direction"] == "Recepção" and item["frequency_mhz"] == frequency
                and item["elevation_angle_deg"]
            }
            source_terrain = sampler(*source)
            destination_terrain = sampler(*destination)
            complete = len(source_angles) == len(destination_angles) == 1 and source_terrain is not None and destination_terrain is not None
            if complete:
                registered_source = float(next(iter(source_angles)))
                registered_destination = float(next(iter(destination_angles)))
                source_top = source_terrain + float(row["source_height_m"])
                destination_top = destination_terrain + float(row["destination_height_m"])
                distance_m = float(row["distance_km"]) * 1000.0
                derived_source1 = elevation_angle(distance_m, source_top, destination_top, 1.0)
                derived_destination1 = elevation_angle(distance_m, destination_top, source_top, 1.0)
                derived_source43 = elevation_angle(distance_m, source_top, destination_top, 4 / 3)
                derived_destination43 = elevation_angle(distance_m, destination_top, source_top, 4 / 3)
                error1 = max(angular_error(registered_source, derived_source1), angular_error(registered_destination, derived_destination1))
                error43 = max(angular_error(registered_source, derived_source43), angular_error(registered_destination, derived_destination43))
                for threshold in THRESHOLDS:
                    label1 = "consistent" if error1 <= threshold else "inconsistent"
                    label43 = "consistent" if error43 <= threshold else "inconsistent"
                    sensitivity1[(threshold, label1)] += 1
                    sensitivity43[(threshold, label43)] += 1
                    if label1 == "consistent":
                        candidate_pass1[threshold].add(row["candidate_id"])
                    if label43 == "consistent":
                        candidate_pass43[threshold].add(row["candidate_id"])
            else:
                registered_source = float(next(iter(source_angles))) if len(source_angles) == 1 else None
                registered_destination = float(next(iter(destination_angles))) if len(destination_angles) == 1 else None
                source_top = destination_top = derived_source1 = derived_destination1 = None
                derived_source43 = derived_destination43 = error1 = error43 = None
            results.append({
                "candidate_id": row["candidate_id"], "path_id": row["path_id"], "link_family": row["link_family"],
                "service_fistel": row["service_fistel"], "rf_act_number": row["rf_act_number"],
                "source_coordinate": row["source_coordinate"], "destination_coordinate": row["destination_coordinate"],
                "frequency_mhz": frequency, "distance_km": row["distance_km"],
                "source_terrain_m": "" if source_terrain is None else source_terrain,
                "destination_terrain_m": "" if destination_terrain is None else destination_terrain,
                "source_height_m": row["source_height_m"], "destination_height_m": row["destination_height_m"],
                "source_top_m": "" if source_top is None else source_top,
                "destination_top_m": "" if destination_top is None else destination_top,
                "registered_source_elevation_deg": "" if registered_source is None else registered_source,
                "registered_destination_elevation_deg": "" if registered_destination is None else registered_destination,
                "derived_source_elevation_k1_deg": "" if derived_source1 is None else derived_source1,
                "derived_destination_elevation_k1_deg": "" if derived_destination1 is None else derived_destination1,
                "maximum_two_end_error_k1_deg": "" if error1 is None else error1,
                "derived_source_elevation_k4_3_deg": "" if derived_source43 is None else derived_source43,
                "derived_destination_elevation_k4_3_deg": "" if derived_destination43 is None else derived_destination43,
                "maximum_two_end_error_k4_3_deg": "" if error43 is None else error43,
                "vertical_status_k1": status(error1), "vertical_status_k4_3": status(error43),
                "pairing_status": "not_performed",
                "vertical_semantics": "registered antenna tilt compared with spherical effective-Earth endpoint geometry; cadastral values not physically verified",
            })
    finally:
        sampler.close()

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="link-vertical-", dir=output.parent) as directory:
        staged = Path(directory) / output.name
        with deterministic_gzip_csv(staged, FIELDS) as writer:
            writer.writerows(results)
        os.replace(staged, output)

    def sensitivity(counter: Counter, candidates: dict) -> list[dict]:
        return [{
            "threshold_deg": threshold, "consistent_paths": counter[(threshold, "consistent")],
            "inconsistent_paths": counter[(threshold, "inconsistent")],
            "candidates_with_consistent_path": len(candidates[threshold]),
        } for threshold in THRESHOLDS]

    result = {
        "schema_version": 1, "paths_file": str(paths), "paths_sha256": sha256_file(paths),
        "keys_file": str(keys), "keys_sha256": sha256_file(keys), "emissions_file": str(emissions),
        "emissions_sha256": sha256_file(emissions), "terrain_index": str(terrain_index),
        "terrain_index_sha256": sha256_file(terrain_index), "path_count": len(results),
        "complete_vertical_geometry_count": sum(row["vertical_status_k1"] != "vertical_geometry_missing" for row in results),
        "missing_vertical_geometry_count": sum(row["vertical_status_k1"] == "vertical_geometry_missing" for row in results),
        "sensitivity_k1": sensitivity(sensitivity1, candidate_pass1),
        "sensitivity_k4_3": sensitivity(sensitivity43, candidate_pass43),
        "provisional_threshold_deg": 1.0,
        "vertical_model": "spherical effective Earth endpoint elevation from TOPODATA ground plus cadastral antenna height",
        "pairing_status": "not_performed", "output": str(output),
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
    parser.add_argument("--paths", type=Path, required=True)
    parser.add_argument("--keys", type=Path, required=True)
    parser.add_argument("--emissions", type=Path, required=True)
    parser.add_argument("--terrain-root", type=Path, required=True)
    parser.add_argument("--terrain-index", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(validate(args.paths, args.keys, args.emissions, args.terrain_root, args.terrain_index, args.output, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
