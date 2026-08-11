#!/usr/bin/env /home/python/pyenv/bin/python
"""Reclassifica faces da malha por linha de visada TOPODATA."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
from collections import Counter
from pathlib import Path

from build_canonical_smp import sha256_file
from enrich_candidate_geospatial_context import deterministic_gzip_csv
from prioritize_augmented_mesh_edges import face_edges


SEMANTICS = "triangle edge counts from TOPODATA terrain LOS only; no Fresnel, RF illumination, coverage, or operational claim"


def face_status(los_count: int) -> str:
    if los_count == 3:
        return "triangle_k3_terrain_los"
    if los_count == 2:
        return "triangle_two_edge_terrain_los"
    return "triangle_sparse_terrain_los"


def build(faces_path: Path, mesh_geojson: Path, profiles_path: Path, output_dir: Path, report: Path) -> dict:
    with gzip.open(faces_path, "rt", encoding="utf-8", newline="") as source:
        faces = list(csv.DictReader(source))
    with gzip.open(profiles_path, "rt", encoding="utf-8", newline="") as source:
        profiles = {row["edge_id"]: row for row in csv.DictReader(source)}
    rows, counts1, counts43 = [], Counter(), Counter()
    for face in faces:
        edge_ids = [f"mesh-edge:{left}|{right}" for left, right in face_edges(face["vertex_ids"])]
        edge_profiles = [profiles.get(identifier) for identifier in edge_ids]
        additions = {}
        for suffix, field, counter in (("k1", "terrain_status_k1", counts1), ("k4_3", "terrain_status_k4_3", counts43)):
            values = [None if profile is None else profile[field] for profile in edge_profiles]
            los = sum(value == "los_clear" for value in values)
            missing = sum(value == "terrain_missing" for value in values)
            obstructed = sum(value == "terrain_or_curvature_obstructed" for value in values)
            unprofiled = sum(value is None for value in values)
            classification = face_status(los); counter[classification] += 1
            additions.update({f"los_edge_count_{suffix}": los, f"obstructed_edge_count_{suffix}": obstructed,
                              f"missing_edge_count_{suffix}": missing, f"unprofiled_edge_count_{suffix}": unprofiled,
                              f"terrain_face_status_{suffix}": classification})
        rows.append({**face, **additions, "terrain_face_semantics": SEMANTICS})
    output_dir.mkdir(parents=True, exist_ok=True)
    table = output_dir / "triangular_faces_topodata.csv.gz"
    deterministic_gzip_csv(table, rows, list(rows[0]))
    source_geojson = json.loads(mesh_geojson.read_text(encoding="utf-8"))
    by_id = {row["face_id"]: row for row in rows}
    for feature in source_geojson["features"]:
        row = by_id[feature["properties"]["face_id"]]
        feature["properties"].update({key: value for key, value in row.items()
                                      if key.startswith(("los_edge_", "obstructed_edge_", "missing_edge_", "unprofiled_edge_", "terrain_face_"))})
    source_geojson["name"] = "augmented_triangular_mesh_topodata_los"
    geojson = output_dir / "triangular_mesh_topodata.geojson"
    geojson.write_text(json.dumps(source_geojson, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    result = {"schema_version": 1, "faces": str(faces_path), "faces_sha256": sha256_file(faces_path),
              "profiles": str(profiles_path), "profiles_sha256": sha256_file(profiles_path),
              "face_count": len(rows), "profiled_edge_count": len(profiles),
              "face_status_k1": dict(sorted(counts1.items())), "face_status_k4_3": dict(sorted(counts43.items())),
              "faces_with_missing_terrain_k1": sum(int(row["missing_edge_count_k1"]) > 0 for row in rows),
              "faces_with_missing_terrain_k4_3": sum(int(row["missing_edge_count_k4_3"]) > 0 for row in rows),
              "outputs": {"table": {"path": str(table), "sha256": sha256_file(table)},
                          "geojson": {"path": str(geojson), "sha256": sha256_file(geojson)}}, "semantics": SEMANTICS}
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--faces", type=Path, required=True); parser.add_argument("--mesh-geojson", type=Path, required=True)
    parser.add_argument("--profiles", type=Path, required=True); parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True); args = parser.parse_args()
    print(json.dumps(build(args.faces, args.mesh_geojson, args.profiles, args.output_dir, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
