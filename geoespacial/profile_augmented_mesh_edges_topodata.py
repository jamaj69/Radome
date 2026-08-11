#!/usr/bin/env /home/python/pyenv/bin/python
"""Perfila arestas priorizadas da malha com TOPODATA e curvatura terrestre."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
from collections import Counter
from pathlib import Path

import networkx as nx

from build_candidate_graph import EARTH_RADIUS_M
from build_canonical_smp import sha256_file
from enrich_candidate_geospatial_context import deterministic_gzip_csv
from evaluate_anatel_radio_link_terrain import interpolate
from evaluate_anatel_radio_link_topodata import Topodata


SEMANTICS = "terrain line-of-sight profile only; no Fresnel frequency, RF illumination, coverage, or operational edge"


def los_profile(a: tuple[float, float], b: tuple[float, float], distance_km: float,
                height_a_m: float, height_b_m: float, sampler, spacing_km: float, k: float) -> dict:
    count = max(3, math.ceil(distance_km / spacing_km) + 1)
    terrain = [sampler(*interpolate(a, b, index / (count - 1))) for index in range(count)]
    missing = sum(value is None for value in terrain)
    if missing:
        return {"samples": count, "missing": missing, "clearance": None}
    top_a, top_b = terrain[0] + height_a_m, terrain[-1] + height_b_m
    distance_m = distance_km * 1000.0
    clearances = []
    for index, elevation in enumerate(terrain[1:-1], 1):
        fraction = index / (count - 1)
        first = fraction * distance_m
        second = distance_m - first
        straight_line = top_a + (top_b - top_a) * fraction
        bulge = first * second / (2 * EARTH_RADIUS_M * k)
        clearances.append(straight_line - elevation - bulge)
    return {"samples": count, "missing": 0, "clearance": min(clearances)}


def status(profile: dict) -> str:
    if profile["missing"]:
        return "terrain_missing"
    return "los_clear" if profile["clearance"] >= 0 else "terrain_or_curvature_obstructed"


def build(graph_path: Path, edges_path: Path, terrain_root: Path, terrain_index: Path,
          output: Path, report: Path, height_m: float = 15.0, spacing_km: float = 1.0,
          start_rank: int = 1, limit: int | None = None) -> dict:
    graph = nx.read_graphml(graph_path, force_multigraph=True)
    with gzip.open(edges_path, "rt", encoding="utf-8", newline="") as source:
        eligible = [row for row in csv.DictReader(source)
                    if row["curvature_upper_bound_available"].lower() == "true"
                    and int(row["profile_priority_rank"]) >= start_rank]
    if limit is not None:
        eligible = eligible[:limit]
    sampler = Topodata(terrain_root, terrain_index, cache_size=8)
    rows, counts1, counts43 = [], Counter(), Counter()
    try:
        for edge in eligible:
            left, right = graph.nodes[edge["left_id"]], graph.nodes[edge["right_id"]]
            a = (float(left["latitude"]), float(left["longitude"])); b = (float(right["latitude"]), float(right["longitude"]))
            distance = float(edge["distance_km"])
            profile1 = los_profile(a, b, distance, height_m, height_m, sampler, spacing_km, 1.0)
            profile43 = los_profile(a, b, distance, height_m, height_m, sampler, spacing_km, 4.0 / 3.0)
            status1, status43 = status(profile1), status(profile43); counts1[status1] += 1; counts43[status43] += 1
            rows.append({"profile_priority_rank": int(edge["profile_priority_rank"]), "edge_id": edge["edge_id"],
                         "left_id": edge["left_id"], "right_id": edge["right_id"], "distance_km": distance,
                         "endpoint_height_agl_m": height_m, "terrain_samples": profile1["samples"],
                         "missing_samples": max(profile1["missing"], profile43["missing"]),
                         "minimum_los_clearance_k1_m": "" if profile1["clearance"] is None else round(profile1["clearance"], 6),
                         "minimum_los_clearance_k4_3_m": "" if profile43["clearance"] is None else round(profile43["clearance"], 6),
                         "terrain_status_k1": status1, "terrain_status_k4_3": status43,
                         "terrain_source": "TOPODATA/INPE numeric altitude GeoTIFF", "profile_semantics": SEMANTICS})
    finally:
        sampler.close()
    fields = list(rows[0]) if rows else []
    deterministic_gzip_csv(output, rows, fields)
    result = {"schema_version": 1, "graph": str(graph_path), "graph_sha256": sha256_file(graph_path),
              "edges": str(edges_path), "edges_sha256": sha256_file(edges_path),
              "terrain_index": str(terrain_index), "terrain_index_sha256": sha256_file(terrain_index),
              "start_rank": start_rank, "limit": limit, "profiled_edge_count": len(rows),
              "endpoint_height_agl_m": height_m, "sample_spacing_km": spacing_km,
              "status_k1": dict(sorted(counts1.items())), "status_k4_3": dict(sorted(counts43.items())),
              "output": str(output), "output_sha256": sha256_file(output), "semantics": SEMANTICS}
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True); parser.add_argument("--edges", type=Path, required=True)
    parser.add_argument("--terrain-root", type=Path, required=True); parser.add_argument("--terrain-index", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True); parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--height-m", type=float, default=15.0); parser.add_argument("--spacing-km", type=float, default=1.0)
    parser.add_argument("--start-rank", type=int, default=1); parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    print(json.dumps(build(args.graph, args.edges, args.terrain_root, args.terrain_index, args.output, args.report,
                           args.height_m, args.spacing_km, args.start_rank, args.limit), ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
