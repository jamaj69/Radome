#!/usr/bin/env /home/python/pyenv/bin/python
"""Prioriza arestas da malha para perfilamento TOPODATA sem confirmar visada."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
from collections import defaultdict
from pathlib import Path

import networkx as nx

from build_canonical_smp import sha256_file
from enrich_candidate_geospatial_context import deterministic_gzip_csv, distance_km


SEMANTICS = "priority queue for terrain profiling; not line of sight, RF illumination, coverage, or an operational edge"


def face_edges(vertex_ids: str) -> list[tuple[str, str]]:
    vertices = vertex_ids.split("|")
    if len(vertices) != 3 or len(set(vertices)) != 3:
        raise ValueError(f"face must contain three unique vertices: {vertex_ids}")
    return sorted(tuple(sorted((vertices[left], vertices[right]))) for left, right in ((0, 1), (1, 2), (0, 2)))


def build(graph_path: Path, faces_path: Path, output: Path, report: Path) -> dict:
    graph = nx.read_graphml(graph_path, force_multigraph=True)
    with gzip.open(faces_path, "rt", encoding="utf-8", newline="") as source:
        faces = list(csv.DictReader(source))
    incidence: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for face in faces:
        for edge in face_edges(face["vertex_ids"]):
            incidence[edge].append(face)
    available = {
        tuple(sorted((str(origin), str(destination))))
        for origin, destination, attributes in graph.edges(data=True)
        if attributes.get("relation") == "candidate_visibility_upper_bound"
    }
    rows = []
    for (left, right), incident in sorted(incidence.items()):
        left_node, right_node = graph.nodes[left], graph.nodes[right]
        separation = distance_km(float(left_node["latitude"]), float(left_node["longitude"]),
                                 float(right_node["latitude"]), float(right_node["longitude"]))
        totals = {field: sum(int(face[field]) for face in incident) for field in
                  ("smp_site_count", "broadcast_site_count", "radio_link_endpoint_count")}
        diversity = sum(value > 0 for value in totals.values())
        rows.append({
            "edge_id": f"mesh-edge:{left}|{right}", "left_id": left, "right_id": right,
            "distance_km": round(separation, 6), "curvature_upper_bound_available": (left, right) in available,
            "incident_face_count": len(incident),
            "incident_k3_face_count": sum(face["face_status"] == "triangle_k3_curvature_pending" for face in incident),
            "incident_two_edge_face_count": sum(face["face_status"] == "triangle_two_edge_curvature_pending" for face in incident),
            "best_minimum_angle_deg": round(max(float(face["minimum_angle_deg"]) for face in incident), 6),
            "illuminator_class_count": diversity, **totals, "priority_semantics": SEMANTICS,
        })
    rows.sort(key=lambda row: (-int(row["curvature_upper_bound_available"]), -row["incident_k3_face_count"],
                               -row["illuminator_class_count"], -row["best_minimum_angle_deg"],
                               row["distance_km"], row["edge_id"]))
    for rank, row in enumerate(rows, 1):
        row["profile_priority_rank"] = rank
    fields = ["profile_priority_rank", *[key for key in rows[0] if key != "profile_priority_rank"]]
    output.parent.mkdir(parents=True, exist_ok=True)
    deterministic_gzip_csv(output, rows, fields)
    result = {"schema_version": 1, "graph": str(graph_path), "graph_sha256": sha256_file(graph_path),
              "faces": str(faces_path), "faces_sha256": sha256_file(faces_path),
              "face_count": len(faces), "unique_edge_count": len(rows),
              "curvature_upper_bound_edge_count": sum(row["curvature_upper_bound_available"] for row in rows),
              "edges_incident_to_k3_count": sum(row["incident_k3_face_count"] > 0 for row in rows),
              "edges_with_three_illuminator_classes_count": sum(row["illuminator_class_count"] == 3 for row in rows),
              "output": str(output), "output_sha256": sha256_file(output), "semantics": SEMANTICS}
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--faces", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.graph, args.faces, args.output, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
