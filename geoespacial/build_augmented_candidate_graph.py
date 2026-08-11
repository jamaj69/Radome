#!/usr/bin/env /home/python/pyenv/bin/python
"""Incorpora candidatos TOPODATA ao grafo continental sem promover visada."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import tempfile
from pathlib import Path

import networkx as nx

from build_candidate_graph import horizon_km
from build_canonical_smp import sha256_file
from enrich_candidate_geospatial_context import deterministic_gzip_csv, distance_km


SEMANTICS = (
    "effective-earth curvature upper bound using endpoint elevations; intermediate "
    "terrain, viewshed, Fresnel clearance, RF coverage and operational feasibility pending"
)


def candidate_attributes(row: dict, radome_height_m: float, target_altitude_m: float, earth_factor: float) -> dict:
    elevation = float(row["elevation_m"])
    radius = horizon_km(elevation + radome_height_m, earth_factor) + horizon_km(target_altitude_m, earth_factor)
    return {
        "node_type": "candidate_radome_gap", "kind": "candidate_radome_gap",
        "name": str(row["candidate_id"]), "longitude": float(row["longitude"]),
        "latitude": float(row["latitude"]), "terrain_elevation_m": elevation,
        "terrain_source": "TOPODATA/INPE", "radome_height_agl_m": radome_height_m,
        "target_altitude_m": target_altitude_m, "coverage_radius_km": round(radius, 3),
        "radius_status": "geometric_upper_bound_topographic_occlusion_pending",
        "terrain_screening_status": str(row["multiscale_status"]),
        "terrain_score": float(row["terrain_score"]), "uf": str(row["uf"]),
        "represented_cell_count": int(row["represented_cell_count"]),
        "represented_cell_ids": str(row["represented_cell_ids"]),
        "source_seed_id": str(row["seed_id"]), "operational_site": False,
        "candidate_semantics": SEMANTICS,
    }


def build(input_graph: Path, gap_candidates: Path, output_dir: Path, report: Path,
          radome_height_m: float = 15.0, target_altitude_m: float = 3000.0,
          earth_factor: float = 4.0 / 3.0) -> dict:
    graph = nx.read_graphml(input_graph, force_multigraph=True)
    original_candidates = [(str(i), a) for i, a in graph.nodes(data=True) if a.get("node_type") in {"capital", "airport"}]
    with gzip.open(gap_candidates, "rt", encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    for row in rows:
        identifier = str(row["candidate_id"])
        if identifier in graph:
            raise ValueError(f"identificador duplicado: {identifier}")
        graph.add_node(identifier, **candidate_attributes(row, radome_height_m, target_altitude_m, earth_factor))

    all_candidates = original_candidates + [(str(row["candidate_id"]), graph.nodes[str(row["candidate_id"])]) for row in rows]
    added_pairs = 0
    for index, (left_id, left) in enumerate(all_candidates):
        if left.get("node_type") != "candidate_radome_gap":
            start = len(original_candidates)
        else:
            start = index + 1
        left_horizon = horizon_km(float(left["terrain_elevation_m"]) + radome_height_m, earth_factor)
        for right_id, right in all_candidates[start:]:
            if left_id == right_id:
                continue
            separation = distance_km(float(left["latitude"]), float(left["longitude"]), float(right["latitude"]), float(right["longitude"]))
            right_horizon = horizon_km(float(right["terrain_elevation_m"]) + radome_height_m, earth_factor)
            if separation <= left_horizon + right_horizon:
                for origin, destination in ((left_id, right_id), (right_id, left_id)):
                    graph.add_edge(origin, destination, key=f"gap_curvature:{origin}:{destination}",
                                   relation="candidate_visibility_upper_bound", distance_km=round(separation, 3),
                                   status="curvature_only_terrain_pending", operational_edge=False,
                                   source_layer="topodata_gap_candidates", association_method=SEMANTICS)
                added_pairs += 1

    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "graph.graphml"
    with tempfile.NamedTemporaryFile(dir=output_dir, suffix=".graphml", delete=False) as stream:
        temporary = Path(stream.name)
    nx.write_graphml(graph, temporary, encoding="utf-8", prettyprint=False, infer_numeric_types=True)
    os.replace(temporary, output)
    table = output_dir / "gap_candidate_nodes.csv.gz"
    public = [{"candidate_id": str(row["candidate_id"]), **candidate_attributes(row, radome_height_m, target_altitude_m, earth_factor)} for row in rows]
    deterministic_gzip_csv(table, public, list(public[0]))
    result = {"schema_version": 1, "input_graph": str(input_graph), "input_graph_sha256": sha256_file(input_graph),
              "gap_candidates": str(gap_candidates), "gap_candidates_sha256": sha256_file(gap_candidates),
              "original_candidate_count": len(original_candidates), "gap_candidate_count": len(rows),
              "total_candidate_count": len(all_candidates), "added_curvature_pair_count": added_pairs,
              "added_directed_edge_count": added_pairs * 2, "total_graph_node_count": graph.number_of_nodes(),
              "total_graph_edge_count": graph.number_of_edges(), "operational_edge_count": sum(bool(a.get("operational_edge")) for *_, a in graph.edges(data=True)),
              "parameters": {"radome_height_agl_m": radome_height_m, "target_altitude_m": target_altitude_m, "effective_earth_radius_factor": earth_factor},
              "output_graph": str(output), "output_graph_sha256": sha256_file(output),
              "candidate_table": str(table), "candidate_table_sha256": sha256_file(table), "semantics": SEMANTICS}
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-graph", type=Path, required=True)
    parser.add_argument("--gap-candidates", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--radome-height-m", type=float, default=15.0)
    parser.add_argument("--target-altitude-m", type=float, default=3000.0)
    parser.add_argument("--earth-factor", type=float, default=4.0 / 3.0)
    args = parser.parse_args()
    print(json.dumps(build(args.input_graph, args.gap_candidates, args.output_dir, args.report,
                           args.radome_height_m, args.target_altitude_m, args.earth_factor), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
