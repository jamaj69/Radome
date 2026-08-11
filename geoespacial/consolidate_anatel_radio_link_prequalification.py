#!/usr/bin/env python3
"""Consolida os gates cadastrais por caminho sem criar arestas de enlace."""

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
from validate_anatel_radio_link_geometry import angular_error, bearing

FIELDS = (
    "candidate_id", "path_id", "link_family", "service_fistel", "rf_act_number",
    "source_coordinate", "destination_coordinate", "frequency_mhz",
    "height_audit_status", "registered_source_azimuth_deg",
    "registered_destination_azimuth_deg", "expected_source_bearing_deg",
    "expected_destination_bearing_deg", "maximum_two_end_azimuth_error_deg",
    "horizontal_status_15deg", "terrain_status_k1", "vertical_status_k1",
    "prequalification_status_k1", "blockers_k1", "terrain_status_k4_3",
    "vertical_status_k4_3", "prequalification_status_k4_3", "blockers_k4_3",
    "pairing_status", "evidence_semantics",
)
CANDIDATE_FIELDS = (
    "candidate_id", "link_family", "service_fistel", "rf_act_number",
    "path_observation_count", "prequalified_paths_k1", "candidate_status_k1",
    "prequalified_paths_k4_3", "candidate_status_k4_3", "pairing_status",
)


def qualification(height_status: str, horizontal_status: str, terrain_status: str | None, vertical_status: str | None) -> tuple[str, list[str]]:
    blockers = []
    if height_status != "unambiguous_cadastral_height":
        blockers.append(height_status)
    if horizontal_status != "horizontal_consistent_15deg":
        blockers.append(horizontal_status)
    if terrain_status != "fresnel60_clear":
        blockers.append(terrain_status or "terrain_not_evaluated")
    if vertical_status != "vertical_consistent_1deg":
        blockers.append(vertical_status or "vertical_not_evaluated")
    return ("cadastral_prequalified" if not blockers else "blocked", blockers)


def consolidate(audited_paths: Path, terrain_paths: Path, vertical_paths: Path, keys: Path, emissions: Path, output: Path, candidates_output: Path, report: Path) -> dict:
    with gzip.open(audited_paths, "rt", encoding="utf-8", newline="") as stream:
        audited = list(csv.DictReader(stream))
    with gzip.open(terrain_paths, "rt", encoding="utf-8", newline="") as stream:
        terrain = {row["path_id"]: row for row in csv.DictReader(stream)}
    with gzip.open(vertical_paths, "rt", encoding="utf-8", newline="") as stream:
        vertical = {row["path_id"]: row for row in csv.DictReader(stream)}

    selected_keys = {(row["link_family"], row["service_fistel"], row["rf_act_number"]) for row in audited}
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

    results = []
    horizontal_counts, prequalified1, prequalified43 = Counter(), Counter(), Counter()
    grouped_results = defaultdict(list)
    for row in audited:
        key = row["link_family"], row["service_fistel"], row["rf_act_number"]
        source = tuple(map(float, row["source_coordinate"].split(",")))
        destination = tuple(map(float, row["destination_coordinate"].split(",")))
        frequency = row["frequency_mhz"]
        source_azimuths = {
            item["azimuth_deg"] for item in grouped[key]
            if (float(item["latitude"]), float(item["longitude"])) == source
            and item["direction"] == "Transmissão" and item["frequency_mhz"] == frequency
            and item["azimuth_deg"]
        }
        destination_azimuths = {
            item["azimuth_deg"] for item in grouped[key]
            if (float(item["latitude"]), float(item["longitude"])) == destination
            and item["direction"] == "Recepção" and item["frequency_mhz"] == frequency
            and item["azimuth_deg"]
        }
        expected_source = bearing(source, destination)
        expected_destination = bearing(destination, source)
        if not source_azimuths or not destination_azimuths:
            horizontal_status, azimuth_error = "horizontal_azimuth_missing", None
        elif len(source_azimuths) != 1 or len(destination_azimuths) != 1:
            horizontal_status, azimuth_error = "horizontal_azimuth_ambiguous", None
        else:
            azimuth_error = max(
                angular_error(float(next(iter(source_azimuths))), expected_source),
                angular_error(float(next(iter(destination_azimuths))), expected_destination),
            )
            horizontal_status = "horizontal_consistent_15deg" if azimuth_error <= 15.0 else "horizontal_inconsistent_15deg"
        horizontal_counts[horizontal_status] += 1
        terrain_row = terrain.get(row["path_id"])
        vertical_row = vertical.get(row["path_id"])
        terrain1 = None if terrain_row is None else terrain_row["terrain_status_k1"]
        terrain43 = None if terrain_row is None else terrain_row["terrain_status_k4_3"]
        vertical1 = None if vertical_row is None else vertical_row["vertical_status_k1"]
        vertical43 = None if vertical_row is None else vertical_row["vertical_status_k4_3"]
        status1, blockers1 = qualification(row["height_audit_status"], horizontal_status, terrain1, vertical1)
        status43, blockers43 = qualification(row["height_audit_status"], horizontal_status, terrain43, vertical43)
        prequalified1[status1] += 1
        prequalified43[status43] += 1
        result = {
            "candidate_id": row["candidate_id"], "path_id": row["path_id"], "link_family": row["link_family"],
            "service_fistel": row["service_fistel"], "rf_act_number": row["rf_act_number"],
            "source_coordinate": row["source_coordinate"], "destination_coordinate": row["destination_coordinate"],
            "frequency_mhz": frequency, "height_audit_status": row["height_audit_status"],
            "registered_source_azimuth_deg": "|".join(sorted(source_azimuths, key=float)),
            "registered_destination_azimuth_deg": "|".join(sorted(destination_azimuths, key=float)),
            "expected_source_bearing_deg": expected_source, "expected_destination_bearing_deg": expected_destination,
            "maximum_two_end_azimuth_error_deg": "" if azimuth_error is None else azimuth_error,
            "horizontal_status_15deg": horizontal_status, "terrain_status_k1": terrain1 or "not_evaluated",
            "vertical_status_k1": vertical1 or "not_evaluated", "prequalification_status_k1": status1,
            "blockers_k1": "|".join(blockers1), "terrain_status_k4_3": terrain43 or "not_evaluated",
            "vertical_status_k4_3": vertical43 or "not_evaluated", "prequalification_status_k4_3": status43,
            "blockers_k4_3": "|".join(blockers43), "pairing_status": "not_performed",
            "evidence_semantics": "cadastral prequalification only; requires physical endpoint and installation verification",
        }
        results.append(result)
        grouped_results[row["candidate_id"]].append(result)

    candidate_rows = []
    candidate_counts1, candidate_counts43 = Counter(), Counter()
    for candidate_id in sorted(grouped_results):
        rows = grouped_results[candidate_id]
        count1 = sum(row["prequalification_status_k1"] == "cadastral_prequalified" for row in rows)
        count43 = sum(row["prequalification_status_k4_3"] == "cadastral_prequalified" for row in rows)
        status1 = "has_cadastral_prequalified_path" if count1 else "no_cadastral_prequalified_path"
        status43 = "has_cadastral_prequalified_path" if count43 else "no_cadastral_prequalified_path"
        candidate_counts1[status1] += 1
        candidate_counts43[status43] += 1
        first = rows[0]
        candidate_rows.append({
            "candidate_id": candidate_id, "link_family": first["link_family"], "service_fistel": first["service_fistel"],
            "rf_act_number": first["rf_act_number"], "path_observation_count": len(rows),
            "prequalified_paths_k1": count1, "candidate_status_k1": status1,
            "prequalified_paths_k4_3": count43, "candidate_status_k4_3": status43,
            "pairing_status": "not_performed",
        })

    output.parent.mkdir(parents=True, exist_ok=True)
    candidates_output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="link-prequalification-", dir=output.parent) as directory:
        staged_paths = Path(directory) / output.name
        staged_candidates = Path(directory) / candidates_output.name
        with deterministic_gzip_csv(staged_paths, FIELDS) as writer:
            writer.writerows(results)
        with deterministic_gzip_csv(staged_candidates, CANDIDATE_FIELDS) as writer:
            writer.writerows(candidate_rows)
        os.replace(staged_paths, output)
        os.replace(staged_candidates, candidates_output)

    result = {
        "schema_version": 1, "audited_paths_file": str(audited_paths), "audited_paths_sha256": sha256_file(audited_paths),
        "terrain_paths_file": str(terrain_paths), "terrain_paths_sha256": sha256_file(terrain_paths),
        "vertical_paths_file": str(vertical_paths), "vertical_paths_sha256": sha256_file(vertical_paths),
        "path_observation_count": len(results), "candidate_count": len(candidate_rows),
        "horizontal_status_15deg": dict(sorted(horizontal_counts.items())),
        "path_prequalification_k1": dict(sorted(prequalified1.items())),
        "path_prequalification_k4_3": dict(sorted(prequalified43.items())),
        "candidate_prequalification_k1": dict(sorted(candidate_counts1.items())),
        "candidate_prequalification_k4_3": dict(sorted(candidate_counts43.items())),
        "thresholds": {"horizontal_azimuth_deg": 15.0, "vertical_elevation_deg": 1.0, "fresnel_fraction": 0.6},
        "evidence_semantics": "cadastral prequalification; no physical verification and no operational edge",
        "pairing_status": "not_performed", "paths_output": str(output), "candidates_output": str(candidates_output),
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
    parser.add_argument("--audited-paths", type=Path, required=True)
    parser.add_argument("--terrain-paths", type=Path, required=True)
    parser.add_argument("--vertical-paths", type=Path, required=True)
    parser.add_argument("--keys", type=Path, required=True)
    parser.add_argument("--emissions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--candidates-output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(consolidate(args.audited_paths, args.terrain_paths, args.vertical_paths, args.keys, args.emissions, args.output, args.candidates_output, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
