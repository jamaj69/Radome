#!/usr/bin/env python3
"""Compõe municípios, emissores, candidatos e hipóteses RF num multigrafo dirigido."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from collections import Counter
from pathlib import Path

import networkx as nx

from build_canonical_smp import sha256_file


def node_type(attributes: dict) -> str:
    return str(attributes.get("node_type") or attributes.get("kind") or "unknown")


def add_node(graph: nx.MultiDiGraph, identifier: str, attributes: dict, layer: str, conflicts: list[dict]) -> None:
    incoming = dict(attributes)
    incoming["node_type"] = node_type(incoming)
    incoming["source_layers"] = layer
    if identifier not in graph:
        graph.add_node(identifier, **incoming)
        return
    current = graph.nodes[identifier]
    layers = set(str(current.get("source_layers", "")).split("|")) | {layer}
    current["source_layers"] = "|".join(sorted(value for value in layers if value))
    for key, value in incoming.items():
        if key in {"source_layers", "node_type"}:
            continue
        if key not in current or current[key] in {"", None}:
            current[key] = value
        elif value not in {"", None} and str(current[key]) != str(value):
            conflicts.append({"node_id": identifier, "attribute": key, "kept": str(current[key]), "incoming": str(value), "layer": layer})


def add_membership_layer(target: nx.MultiDiGraph, source: nx.Graph, layer: str, conflicts: list[dict]) -> None:
    for identifier, attributes in sorted(source.nodes(data=True)):
        add_node(target, identifier, attributes, layer, conflicts)
    for index, (left, right, attributes) in enumerate(sorted(source.edges(data=True), key=lambda item: (str(item[0]), str(item[1])))):
        left_type = node_type(source.nodes[left])
        right_type = node_type(source.nodes[right])
        if left_type == "municipio" and right_type != "municipio":
            origin, destination = right, left
        elif right_type == "municipio" and left_type != "municipio":
            origin, destination = left, right
        else:
            origin, destination = sorted((left, right))
        data = dict(attributes)
        data.update(source_layer=layer, directed_semantics=True, operational_edge=False)
        target.add_edge(origin, destination, key=f"{layer}:{index:08d}", **data)


def add_candidate_layer(target: nx.MultiDiGraph, source: nx.Graph, conflicts: list[dict]) -> int:
    layer = "site_candidates"
    for identifier, attributes in sorted(source.nodes(data=True)):
        add_node(target, identifier, attributes, layer, conflicts)
    logical_edges = 0
    for index, (left, right, attributes) in enumerate(sorted(source.edges(data=True), key=lambda item: (str(item[0]), str(item[1])))):
        logical_edges += 1
        data = dict(attributes)
        data.update(
            relation="candidate_visibility_upper_bound", source_layer=layer,
            directed_semantics=False, bidirectional_semantics=True,
            operational_edge=False, terrain_confirmation=False,
        )
        target.add_edge(left, right, key=f"{layer}:{index:08d}:forward", **data)
        target.add_edge(right, left, key=f"{layer}:{index:08d}:reverse", **data)
    return logical_edges


def add_hypothesis_layer(target: nx.MultiDiGraph, source: nx.MultiDiGraph, conflicts: list[dict]) -> None:
    layer = "radio_link_hypotheses"
    for identifier, attributes in sorted(source.nodes(data=True)):
        add_node(target, identifier, attributes, layer, conflicts)
    edges = sorted(source.edges(keys=True, data=True), key=lambda item: (str(item[0]), str(item[1]), str(item[2])))
    for index, (origin, destination, _, attributes) in enumerate(edges):
        data = dict(attributes)
        data["source_layer"] = layer
        data.setdefault("directed_semantics", True)
        data.setdefault("operational_edge", False)
        target.add_edge(origin, destination, key=f"{layer}:{index:08d}", **data)


def build(municipal: Path, broadcast: Path, candidates: Path, hypotheses: Path, output: Path, report: Path) -> dict:
    municipal_graph = nx.read_graphml(municipal, force_multigraph=True)
    broadcast_graph = nx.read_graphml(broadcast, force_multigraph=True)
    candidate_graph = nx.read_graphml(candidates, force_multigraph=True)
    hypothesis_graph = nx.read_graphml(hypotheses, force_multigraph=True)
    unified = nx.MultiDiGraph(
        graph_type="unified_geospatial_evidence_graph", scope="continental_brazil",
        operational_edge_count=0, evidence_semantics="mixed official cadastral layers and explicitly provisional hypotheses",
    )
    conflicts: list[dict] = []
    add_membership_layer(unified, municipal_graph, "smp_municipal", conflicts)
    add_membership_layer(unified, broadcast_graph, "broadcast_municipal", conflicts)
    candidate_logical_edges = add_candidate_layer(unified, candidate_graph, conflicts)
    add_hypothesis_layer(unified, hypothesis_graph, conflicts)

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, prefix=f".{output.name}.", suffix=".graphml", delete=False) as stream:
        temporary = Path(stream.name)
    try:
        nx.write_graphml(unified, temporary, encoding="utf-8", prettyprint=False, infer_numeric_types=True)
        os.replace(temporary, output)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise

    types = Counter(node_type(data) for _, data in unified.nodes(data=True))
    relations = Counter(str(data.get("relation") or data.get("edge_type") or "unknown") for _, _, data in unified.edges(data=True))
    operational_edges = sum(bool(data.get("operational_edge")) for _, _, data in unified.edges(data=True))
    result = {
        "schema_version": 1,
        "inputs": [
            {"layer": "smp_municipal", "file": str(municipal), "sha256": sha256_file(municipal)},
            {"layer": "broadcast_municipal", "file": str(broadcast), "sha256": sha256_file(broadcast)},
            {"layer": "site_candidates", "file": str(candidates), "sha256": sha256_file(candidates)},
            {"layer": "radio_link_hypotheses", "file": str(hypotheses), "sha256": sha256_file(hypotheses)},
        ],
        "output": str(output), "output_sha256": sha256_file(output),
        "node_count": unified.number_of_nodes(), "edge_record_count": unified.number_of_edges(),
        "node_type_counts": dict(sorted(types.items())), "edge_relation_counts": dict(sorted(relations.items())),
        "candidate_visibility_logical_edge_count": candidate_logical_edges,
        "candidate_visibility_stored_arc_count": candidate_logical_edges * 2,
        "node_attribute_conflict_count": len(conflicts), "node_attribute_conflicts": conflicts,
        "operational_edge_count": operational_edges,
        "safety_semantics": "candidate visibility is duplicated into two arcs but remains terrain-unconfirmed; RF hypotheses remain unverified; no operational edges",
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(dir=report.parent, prefix=f".{report.name}.", delete=False) as stream:
        stream.write(payload)
        temporary_report = Path(stream.name)
    os.replace(temporary_report, report)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--municipal", type=Path, required=True)
    parser.add_argument("--broadcast", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--hypotheses", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.municipal, args.broadcast, args.candidates, args.hypotheses, args.output, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
