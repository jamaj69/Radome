#!/usr/bin/env python3
"""Gera GraphML das hipoteses cadastrais pre-qualificadas, sem enlaces operacionais."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import tempfile
from pathlib import Path

import networkx as nx

from build_canonical_smp import sha256_file


def node_id(coordinate: str) -> str:
    canonical = ",".join(f"{float(value):.6f}" for value in coordinate.split(","))
    return "anatel_endpoint:" + hashlib.sha256(canonical.encode()).hexdigest()[:20]


def build_graph(prequalification_rows: list[dict], terrain_by_path: dict[str, dict], vertical_by_path: dict[str, dict]) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph(
        graph_type="cadastral_radio_link_hypotheses",
        evidence_semantics="not physically verified; not operational",
        pairing_status="not_performed",
    )
    for row in sorted(prequalification_rows, key=lambda item: item["path_id"]):
        pass_k1 = row["prequalification_status_k1"] == "cadastral_prequalified"
        pass_k43 = row["prequalification_status_k4_3"] == "cadastral_prequalified"
        if not pass_k1 and not pass_k43:
            continue
        source_id = node_id(row["source_coordinate"])
        destination_id = node_id(row["destination_coordinate"])
        source_latitude, source_longitude = map(float, row["source_coordinate"].split(","))
        destination_latitude, destination_longitude = map(float, row["destination_coordinate"].split(","))
        for identifier, latitude, longitude in (
            (source_id, source_latitude, source_longitude),
            (destination_id, destination_latitude, destination_longitude),
        ):
            graph.add_node(
                identifier, node_type="anatel_cadastral_endpoint", latitude=latitude,
                longitude=longitude, physical_verification=False, pairing_status="not_performed",
            )
        terrain = terrain_by_path[row["path_id"]]
        vertical = vertical_by_path[row["path_id"]]
        graph.add_edge(
            source_id, destination_id, key=row["path_id"], path_id=row["path_id"],
            candidate_id=row["candidate_id"], link_family=row["link_family"],
            service_fistel=row["service_fistel"], rf_act_number=row["rf_act_number"],
            frequency_mhz=float(row["frequency_mhz"]), distance_km=float(terrain["distance_km"]),
            source_height_m=float(terrain["source_height_m"]),
            destination_height_m=float(terrain["destination_height_m"]),
            minimum_fresnel60_clearance_k1_m=float(terrain["minimum_fresnel60_clearance_k1_m"]),
            minimum_fresnel60_clearance_k4_3_m=float(terrain["minimum_fresnel60_clearance_k4_3_m"]),
            maximum_two_end_azimuth_error_deg=float(row["maximum_two_end_azimuth_error_deg"]),
            maximum_two_end_elevation_error_k1_deg=float(vertical["maximum_two_end_error_k1_deg"]),
            maximum_two_end_elevation_error_k4_3_deg=float(vertical["maximum_two_end_error_k4_3_deg"]),
            prequalified_k1=pass_k1, prequalified_k4_3=pass_k43,
            edge_type="cadastral_prequalified_hypothesis", operational_edge=False,
            physical_verification=False, pairing_status="not_performed",
        )
    return graph


def component_summary(graph: nx.MultiDiGraph, attribute: str) -> dict:
    selected = [(source, destination) for source, destination, data in graph.edges(data=True) if data[attribute]]
    simple = nx.Graph()
    simple.add_edges_from(selected)
    sizes = sorted((len(component) for component in nx.connected_components(simple)), reverse=True)
    return {
        "node_count": simple.number_of_nodes(), "edge_hypothesis_count": len(selected),
        "component_count": len(sizes), "largest_component_node_count": sizes[0] if sizes else 0,
        "isolated_node_count": sum(size == 1 for size in sizes),
    }


def build(prequalification: Path, terrain: Path, vertical: Path, output: Path, report: Path) -> dict:
    with gzip.open(prequalification, "rt", encoding="utf-8", newline="") as stream:
        prequalification_rows = list(csv.DictReader(stream))
    with gzip.open(terrain, "rt", encoding="utf-8", newline="") as stream:
        terrain_by_path = {row["path_id"]: row for row in csv.DictReader(stream)}
    with gzip.open(vertical, "rt", encoding="utf-8", newline="") as stream:
        vertical_by_path = {row["path_id"]: row for row in csv.DictReader(stream)}
    graph = build_graph(prequalification_rows, terrain_by_path, vertical_by_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, prefix=f".{output.name}.", suffix=".graphml", delete=False) as stream:
        temporary = Path(stream.name)
    try:
        nx.write_graphml(graph, temporary, encoding="utf-8", prettyprint=True, infer_numeric_types=True)
        os.replace(temporary, output)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise

    result = {
        "schema_version": 1, "prequalification_file": str(prequalification),
        "prequalification_sha256": sha256_file(prequalification), "terrain_file": str(terrain),
        "terrain_sha256": sha256_file(terrain), "vertical_file": str(vertical),
        "vertical_sha256": sha256_file(vertical), "graphml_file": str(output),
        "graphml_sha256": sha256_file(output), "graph_type": "directed multigraph of cadastral hypotheses",
        "node_count": graph.number_of_nodes(), "edge_hypothesis_count": graph.number_of_edges(),
        "candidate_count": len({data["candidate_id"] for _, _, data in graph.edges(data=True)}),
        "frequency_count": len({data["frequency_mhz"] for _, _, data in graph.edges(data=True)}),
        "k1": component_summary(graph, "prequalified_k1"),
        "k4_3": component_summary(graph, "prequalified_k4_3"),
        "physical_verification": False, "operational_edge_count": 0, "pairing_status": "not_performed",
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
    parser.add_argument("--prequalification", type=Path, required=True)
    parser.add_argument("--terrain", type=Path, required=True)
    parser.add_argument("--vertical", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.prequalification, args.terrain, args.vertical, args.output, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
