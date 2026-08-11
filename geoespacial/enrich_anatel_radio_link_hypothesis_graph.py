#!/usr/bin/env python3
"""Enriquece pontas hipoteticas com estacao, entidade e municipio canonicizados."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import tempfile
from collections import defaultdict
from pathlib import Path

import networkx as nx

from build_anatel_radio_link_hypothesis_graph import node_id
from build_canonical_smp import sha256_file


def apply_context(graph: nx.MultiDiGraph, context: dict[str, dict[str, set[str]]], municipality_graph: nx.Graph) -> dict:
    conflicts = 0
    missing_municipalities = set()
    referenced_municipalities = set()
    membership_edges = 0
    for endpoint_id in sorted(node for node, data in graph.nodes(data=True) if data.get("node_type") == "anatel_cadastral_endpoint"):
        values = context.get(endpoint_id, defaultdict(set))
        ibge_codes = sorted(values.get("ibge_codes", set()))
        stations = sorted(values.get("station_numbers", set()))
        entities = sorted(values.get("entities", set()))
        if len(ibge_codes) > 1:
            conflicts += 1
        graph.nodes[endpoint_id].update(
            ibge_codes="|".join(ibge_codes), municipality_count=len(ibge_codes),
            municipality_conflict=len(ibge_codes) > 1, station_numbers="|".join(stations),
            station_count=len(stations), entities="|".join(entities), entity_count=len(entities),
            context_semantics="sets from source rows supporting prequalified path hypotheses",
        )
        for code in ibge_codes:
            municipality_id = f"municipio:{code}"
            if municipality_id not in municipality_graph:
                missing_municipalities.add(code)
                continue
            referenced_municipalities.add(municipality_id)
            if municipality_id not in graph:
                attributes = dict(municipality_graph.nodes[municipality_id])
                attributes["node_type"] = "municipio"
                graph.add_node(municipality_id, **attributes)
            graph.add_edge(
                endpoint_id, municipality_id, key=f"located_in:{endpoint_id}:{code}",
                relation="located_in_cadastral", edge_type="administrative_context",
                operational_edge=False, physical_verification=False, pairing_status="not_performed",
            )
            membership_edges += 1
    return {
        "endpoint_municipality_conflict_count": conflicts,
        "referenced_municipality_count": len(referenced_municipalities),
        "municipality_membership_edge_count": membership_edges,
        "missing_municipality_codes": sorted(missing_municipalities),
    }


def enrich(graphml: Path, prequalification: Path, keys: Path, emissions: Path, municipality_graphml: Path, output: Path, report: Path) -> dict:
    graph = nx.read_graphml(graphml, force_multigraph=True)
    with gzip.open(prequalification, "rt", encoding="utf-8", newline="") as stream:
        paths = [
            row for row in csv.DictReader(stream)
            if row["prequalification_status_k1"] == "cadastral_prequalified"
            or row["prequalification_status_k4_3"] == "cadastral_prequalified"
        ]
    selected_groups = {(row["link_family"], row["service_fistel"], row["rf_act_number"]) for row in paths}
    source_groups = {}
    with gzip.open(keys, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            group = row["link_family"], row["service_fistel"], row["rf_act_number"]
            if group in selected_groups:
                source_groups[row["source_row_number"]] = group

    wanted = defaultdict(list)
    for row in paths:
        group = row["link_family"], row["service_fistel"], row["rf_act_number"]
        wanted[group].append((
            tuple(map(float, row["source_coordinate"].split(","))), "Transmissão", row["frequency_mhz"],
            node_id(row["source_coordinate"]),
        ))
        wanted[group].append((
            tuple(map(float, row["destination_coordinate"].split(","))), "Recepção", row["frequency_mhz"],
            node_id(row["destination_coordinate"]),
        ))
    wanted_lookup = defaultdict(set)
    for group, observations in wanted.items():
        for coordinate, direction, frequency, endpoint_id in observations:
            wanted_lookup[(group, coordinate, direction, frequency)].add(endpoint_id)

    context = defaultdict(lambda: defaultdict(set))
    with gzip.open(emissions, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            group = source_groups.get(row["source_row_number"])
            if group is None:
                continue
            lookup = (group, (float(row["latitude"]), float(row["longitude"])), row["direction"], row["frequency_mhz"])
            for endpoint_id in wanted_lookup.get(lookup, ()):
                if row["ibge_code"]:
                    context[endpoint_id]["ibge_codes"].add(row["ibge_code"])
                if row["station_number"]:
                    context[endpoint_id]["station_numbers"].add(row["station_number"])
                if row["entity"]:
                    context[endpoint_id]["entities"].add(row["entity"])

    municipality_graph = nx.read_graphml(municipality_graphml)
    enrichment = apply_context(graph, context, municipality_graph)
    endpoint_nodes = [node for node, data in graph.nodes(data=True) if data.get("node_type") == "anatel_cadastral_endpoint"]
    endpoints_without_context = sum(graph.nodes[node].get("station_count", 0) == 0 for node in endpoint_nodes)
    hypothesis_edges = sum(data.get("edge_type") == "cadastral_prequalified_hypothesis" for _, _, data in graph.edges(data=True))
    operational_edges = sum(bool(data.get("operational_edge")) for _, _, data in graph.edges(data=True))

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
        "schema_version": 1, "source_graphml": str(graphml), "source_graphml_sha256": sha256_file(graphml),
        "prequalification_file": str(prequalification), "prequalification_sha256": sha256_file(prequalification),
        "municipality_graphml": str(municipality_graphml), "municipality_graphml_sha256": sha256_file(municipality_graphml),
        "output_graphml": str(output), "output_graphml_sha256": sha256_file(output),
        "endpoint_node_count": len(endpoint_nodes), "endpoints_without_context_count": endpoints_without_context,
        **enrichment, "total_node_count": graph.number_of_nodes(), "total_edge_count": graph.number_of_edges(),
        "radio_link_hypothesis_edge_count": hypothesis_edges, "operational_edge_count": operational_edges,
        "physical_verification": False, "pairing_status": "not_performed",
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
    parser.add_argument("--graphml", type=Path, required=True)
    parser.add_argument("--prequalification", type=Path, required=True)
    parser.add_argument("--keys", type=Path, required=True)
    parser.add_argument("--emissions", type=Path, required=True)
    parser.add_argument("--municipality-graphml", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(enrich(args.graphml, args.prequalification, args.keys, args.emissions, args.municipality_graphml, args.output, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
