#!/usr/bin/env /home/python/pyenv/bin/python
"""Compara cobertura K3, componentes LOS e falhas de vértice da malha."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
from collections import defaultdict
from pathlib import Path

import networkx as nx

from build_canonical_smp import sha256_file
from enrich_candidate_geospatial_context import deterministic_gzip_csv


SEMANTICS = "terrain-LOS mesh topology and assigned-cell sensitivity; no Fresnel, RF coverage, illumination, or operational availability"


def edge_key(left_id: str, right_id: str) -> tuple[str, str]:
    return tuple(sorted((left_id, right_id)))


def face_vertices(face: dict) -> list[str]:
    vertices = face["vertex_ids"].split("|")
    if len(vertices) != 3 or len(set(vertices)) != 3 or any(not vertex for vertex in vertices):
        raise ValueError(f"face {face.get('face_id', '<unknown>')} must contain three distinct vertex IDs")
    return vertices


def component_metrics(graph: nx.Graph) -> dict:
    components = sorted((len(component) for component in nx.connected_components(graph)), reverse=True)
    return {"node_count": graph.number_of_nodes(), "edge_count": graph.number_of_edges(),
            "component_count": len(components), "largest_component_node_count": components[0] if components else 0,
            "isolated_node_count": sum(size == 1 for size in components),
            "articulation_vertex_count": sum(1 for _ in nx.articulation_points(graph))}


def build(faces_path: Path, profiles_path: Path, disk_report: Path, output: Path, report: Path) -> dict:
    with gzip.open(faces_path, "rt", encoding="utf-8", newline="") as source:
        faces = list(csv.DictReader(source))
    with gzip.open(profiles_path, "rt", encoding="utf-8", newline="") as source:
        profiles = list(csv.DictReader(source))
    disk = json.loads(disk_report.read_text(encoding="utf-8"))
    if not faces:
        raise ValueError("faces input is empty")
    total_cells = int(disk["cell_count"])
    if total_cells <= 0:
        raise ValueError("disk report must contain a positive cell_count")
    vertices_by_face = [face_vertices(face) for face in faces]
    vertices = sorted({vertex for face_vertices_row in vertices_by_face for vertex in face_vertices_row})
    if int(disk["candidate_count"]) != len(vertices):
        raise ValueError("disk report candidate_count does not match the mesh vertex count")
    mesh_edges = {edge_key(vertices[0], vertices[1]) for vertices in vertices_by_face}
    mesh_edges.update(edge_key(vertices[1], vertices[2]) for vertices in vertices_by_face)
    mesh_edges.update(edge_key(vertices[2], vertices[0]) for vertices in vertices_by_face)
    graphs = {"k1": nx.Graph(), "k4_3": nx.Graph()}
    for graph in graphs.values(): graph.add_nodes_from(vertices)
    for profile in profiles:
        edge = edge_key(profile["left_id"], profile["right_id"])
        if edge[0] not in vertices or edge[1] not in vertices or edge not in mesh_edges:
            raise ValueError(f"profile {profile.get('edge_id', '<unknown>')} is not an edge of the input mesh")
        for suffix, field in (("k1", "terrain_status_k1"), ("k4_3", "terrain_status_k4_3")):
            if profile[field] == "los_clear": graphs[suffix].add_edge(profile["left_id"], profile["right_id"])
    articulation = {suffix: set(nx.articulation_points(graph)) for suffix, graph in graphs.items()}
    incident = {suffix: defaultdict(lambda: {"faces": 0, "cells": 0, "area": 0.0}) for suffix in graphs}
    k3_totals = {}
    for suffix in graphs:
        selected = [face for face in faces if face[f"terrain_face_status_{suffix}"] == "triangle_k3_terrain_los"]
        k3_totals[suffix] = {"face_count": len(selected),
                             "assigned_grid_cell_count": sum(int(face["continental_grid_cell_count"]) for face in selected),
                             "assigned_grid_area_km2": sum(float(face["continental_grid_area_km2"]) for face in selected)}
        if k3_totals[suffix]["assigned_grid_cell_count"] > total_cells:
            raise ValueError(f"{suffix} K3 assigned grid cells exceed the disk-report grid")
        for face in selected:
            for vertex in face["vertex_ids"].split("|"):
                values = incident[suffix][vertex]; values["faces"] += 1
                values["cells"] += int(face["continental_grid_cell_count"]); values["area"] += float(face["continental_grid_area_km2"])
    rows = []
    for vertex in vertices:
        row = {"vertex_id": vertex}
        for suffix in graphs:
            values = incident[suffix][vertex]
            row.update({f"los_degree_{suffix}": graphs[suffix].degree(vertex), f"articulation_{suffix}": vertex in articulation[suffix],
                        f"incident_k3_face_count_{suffix}": values["faces"],
                        f"k3_cells_lost_if_vertex_fails_{suffix}": values["cells"],
                        f"k3_area_km2_lost_if_vertex_fails_{suffix}": round(values["area"], 6)})
        row["sensitivity_semantics"] = SEMANTICS; rows.append(row)
    rows.sort(key=lambda row: (-row["k3_cells_lost_if_vertex_fails_k1"], -row["los_degree_k1"], row["vertex_id"]))
    deterministic_gzip_csv(output, rows, list(rows[0]))
    result = {"schema_version": 1, "faces": str(faces_path), "faces_sha256": sha256_file(faces_path),
              "profiles": str(profiles_path), "profiles_sha256": sha256_file(profiles_path),
              "disk_report": str(disk_report), "disk_report_sha256": sha256_file(disk_report),
              "disk_geometric_covered_cell_count": int(disk["covered_cell_count"]), "continental_grid_cell_count": total_cells,
              "models": {suffix: {**component_metrics(graphs[suffix]), **k3_totals[suffix],
                                    "assigned_grid_cell_fraction": k3_totals[suffix]["assigned_grid_cell_count"] / total_cells}
                         for suffix in graphs},
              "vertex_sensitivity_output": str(output), "vertex_sensitivity_sha256": sha256_file(output), "semantics": SEMANTICS}
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--faces", type=Path, required=True); parser.add_argument("--profiles", type=Path, required=True)
    parser.add_argument("--disk-report", type=Path, required=True); parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True); args = parser.parse_args()
    print(json.dumps(build(args.faces, args.profiles, args.disk_report, args.output, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
