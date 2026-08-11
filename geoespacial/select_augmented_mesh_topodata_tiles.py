#!/usr/bin/env /home/python/pyenv/bin/python
"""Seleciona folhas TOPODATA atravessadas por arestas priorizadas da malha."""

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

import networkx as nx

from build_canonical_smp import sha256_file
from evaluate_anatel_radio_link_terrain import interpolate
from select_topodata_route_tiles import tile_name


def edge_tile_names(left: tuple[float, float], right: tuple[float, float], distance_km: float,
                    spacing_km: float = 1.0) -> list[str]:
    if spacing_km <= 0:
        raise ValueError("spacing_km deve ser positivo")
    count = max(2, math.ceil(distance_km / spacing_km) + 1)
    return [tile_name(*interpolate(left, right, index / (count - 1))) for index in range(count)]


def select(graph_path: Path, edges_path: Path, manifest_path: Path, existing_dir: Path,
           output: Path, spacing_km: float = 1.0) -> dict:
    graph = nx.read_graphml(graph_path, force_multigraph=True)
    inventory = json.loads(manifest_path.read_text(encoding="utf-8"))
    available = {item["name"]: item for item in inventory["archives"]}
    required_counts: Counter[str] = Counter()
    affected_edges: defaultdict[str, set[str]] = defaultdict(set)
    selected_edge_count = excluded_edge_count = sample_count = 0
    with gzip.open(edges_path, "rt", encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            if row["curvature_upper_bound_available"].lower() != "true":
                excluded_edge_count += 1
                continue
            selected_edge_count += 1
            left, right = graph.nodes[row["left_id"]], graph.nodes[row["right_id"]]
            names = edge_tile_names((float(left["latitude"]), float(left["longitude"])),
                                    (float(right["latitude"]), float(right["longitude"])),
                                    float(row["distance_km"]), spacing_km)
            sample_count += len(names)
            for name in names:
                required_counts[name] += 1
                affected_edges[name].add(row["edge_id"])
    required = set(required_counts)
    missing = sorted(required - available.keys())
    selected_names = sorted(required & available.keys())
    existing = {path.name for path in existing_dir.glob("*.zip") if path.is_file()}
    new_names = sorted(set(selected_names) - existing)
    archives = [available[name] for name in selected_names]
    result = {
        "schema_version": 1, "graph": str(graph_path), "graph_sha256": sha256_file(graph_path),
        "edges": str(edges_path), "edges_sha256": sha256_file(edges_path),
        "manifest": str(manifest_path), "manifest_sha256": sha256_file(manifest_path),
        "sample_spacing_km": spacing_km, "selected_edge_count": selected_edge_count,
        "excluded_without_curvature_upper_bound_count": excluded_edge_count,
        "route_sample_count": sample_count, "selected_archive_count": len(archives),
        "selected_listed_size_bytes": sum(item["listed_size_bytes"] for item in archives),
        "already_local_archive_count": len(set(selected_names) & existing),
        "new_archive_count": len(new_names),
        "new_listed_size_bytes": sum(available[name]["listed_size_bytes"] for name in new_names),
        "new_archive_names": new_names, "missing_archive_names": missing,
        "missing_archive_details": [{"name": name, "route_sample_count": required_counts[name],
                                      "affected_edge_count": len(affected_edges[name])} for name in missing],
        "archives": archives,
        "selection_semantics": "great-circle samples at <=1 km along curvature-upper-bound mesh edges; terrain profile input only, not visibility or RF evidence",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(prefix=f".{output.name}.", dir=output.parent, delete=False) as target:
        target.write(payload); temporary = Path(target.name)
    os.replace(temporary, output)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--edges", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--existing-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--spacing-km", type=float, default=1.0)
    args = parser.parse_args()
    print(json.dumps(select(args.graph, args.edges, args.manifest, args.existing_dir, args.output, args.spacing_km), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
