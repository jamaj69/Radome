#!/usr/bin/env /usr/bin/python3
"""Ordena candidatos por critérios explícitos sem alegar cobertura operacional."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import os
import statistics
import tempfile
from pathlib import Path

import networkx as nx

from build_canonical_smp import sha256_file
from enrich_candidate_geospatial_context import coordinates, deterministic_gzip_csv, distance_km
from preselect_bc250 import Point, azimuth_sector


SCENARIOS = {
    "balanced": {
        "elevation": 0.40, "city_count": 0.15, "city_sectors": 0.10,
        "smp": 0.08, "broadcast": 0.08, "radio_link": 0.08, "connectivity": 0.11,
    },
    "altitude_priority": {
        "elevation": 0.60, "city_count": 0.10, "city_sectors": 0.08,
        "smp": 0.04, "broadcast": 0.04, "radio_link": 0.04, "connectivity": 0.10,
    },
    "logistics_rf_priority": {
        "elevation": 0.25, "city_count": 0.20, "city_sectors": 0.15,
        "smp": 0.10, "broadcast": 0.10, "radio_link": 0.10, "connectivity": 0.10,
    },
}
SEMANTICS = (
    "preliminary multicriteria screening; curvature-only radii and proximity counts; "
    "no terrain visibility, RF illumination, feasibility, or operational performance"
)


def normalize(values: list[float]) -> list[float]:
    low, high = min(values), max(values)
    if high == low:
        return [0.0] * len(values)
    return [(value - low) / (high - low) for value in values]


def city_points(gpkg: Path) -> list[Point]:
    from osgeo import ogr

    source = ogr.Open(str(gpkg))
    if source is None:
        raise ValueError(f"não foi possível abrir {gpkg}")
    layer = source.GetLayerByName("lml_cidade_p")
    if layer is None:
        raise ValueError("camada lml_cidade_p ausente na BC250")
    points = []
    for feature in layer:
        geometry = feature.GetGeometryRef()
        if geometry is not None and geometry.GetX() <= -34.0:
            points.append(Point(str(feature.GetField("nome") or feature.GetFID()), geometry.GetX(), geometry.GetY()))
    return points


def ranks(rows: list[dict], score_field: str) -> None:
    ordered = sorted(rows, key=lambda row: (-float(row[score_field]), str(row["node_id"])))
    for position, row in enumerate(ordered, 1):
        row[score_field.replace("score", "rank")] = position


def build(graphml: Path, bc250: Path, output_dir: Path, report: Path) -> dict:
    graph = nx.read_graphml(graphml, force_multigraph=True)
    cities = city_points(bc250)
    rows = []
    for identifier, attributes in sorted(graph.nodes(data=True)):
        if attributes.get("node_type") not in {"capital", "airport"}:
            continue
        latitude, longitude = coordinates(attributes)
        radius = float(attributes["coverage_radius_km"])
        origin = Point(str(attributes.get("name", identifier)), longitude, latitude)
        inside = [city for city in cities if distance_km(latitude, longitude, city.latitude, city.longitude) <= radius]
        sectors = len({azimuth_sector(origin, city) for city in inside})
        neighbours = {
            destination for _, destination, data in graph.out_edges(identifier, data=True)
            if data.get("relation") == "candidate_visibility_upper_bound"
        }
        rows.append({
            "node_id": identifier, "kind": attributes["node_type"], "name": attributes.get("name", ""),
            "longitude": longitude, "latitude": latitude,
            "canonical_municipality_code": attributes.get("canonical_municipality_code", ""),
            "terrain_elevation_m": float(attributes["terrain_elevation_m"]),
            "coverage_radius_km": radius, "nearby_city_count": len(inside),
            "occupied_city_azimuth_sectors": sectors, "candidate_geometric_degree": len(neighbours),
            "nearby_smp_site_count": int(attributes["nearby_smp_site_count"]),
            "nearby_broadcast_site_count": int(attributes["nearby_broadcast_site_count"]),
            "nearby_radio_link_endpoint_count": int(attributes["nearby_radio_link_endpoint_count"]),
        })

    components = {
        "elevation": [row["terrain_elevation_m"] for row in rows],
        "city_count": [math.log1p(row["nearby_city_count"]) for row in rows],
        "city_sectors": [row["occupied_city_azimuth_sectors"] / 8.0 for row in rows],
        "smp": [math.log1p(row["nearby_smp_site_count"]) for row in rows],
        "broadcast": [math.log1p(row["nearby_broadcast_site_count"]) for row in rows],
        "radio_link": [math.log1p(row["nearby_radio_link_endpoint_count"]) for row in rows],
        "connectivity": [math.log1p(row["candidate_geometric_degree"]) for row in rows],
    }
    normalized = {name: normalize([float(value) for value in values]) for name, values in components.items()}
    for index, row in enumerate(rows):
        for component in SCENARIOS["balanced"]:
            row[f"normalized_{component}"] = round(normalized[component][index], 9)
        for scenario, weights in SCENARIOS.items():
            row[f"score_{scenario}"] = round(sum(weights[key] * normalized[key][index] for key in weights), 9)
    for scenario in SCENARIOS:
        ranks(rows, f"score_{scenario}")
    for row in rows:
        scenario_ranks = [int(row[f"rank_{scenario}"]) for scenario in SCENARIOS]
        row["mean_scenario_rank"] = round(statistics.mean(scenario_ranks), 6)
        row["best_scenario_rank"] = min(scenario_ranks)
        row["worst_scenario_rank"] = max(scenario_ranks)
        row["rank_range"] = max(scenario_ranks) - min(scenario_ranks)
        row["top10_scenario_count"] = sum(rank <= 10 for rank in scenario_ranks)
        row["screening_semantics"] = SEMANTICS
    rows.sort(key=lambda row: (float(row["mean_scenario_rank"]), int(row["rank_range"]), str(row["node_id"])))
    for position, row in enumerate(rows, 1):
        row["robust_rank"] = position
        graph.nodes[row["node_id"]].update(row)

    output_dir.mkdir(parents=True, exist_ok=True)
    table = output_dir / "candidate_ranking.csv.gz"
    deterministic_gzip_csv(table, rows, list(rows[0]))
    geojson = output_dir / "candidate_ranking.geojson"
    geojson.write_text(json.dumps({
        "type": "FeatureCollection", "name": "candidate_preliminary_ranking",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4674"}},
        "features": [{
            "type": "Feature", "geometry": {"type": "Point", "coordinates": [row["longitude"], row["latitude"]]},
            "properties": {key: value for key, value in row.items() if key not in {"longitude", "latitude"}},
        } for row in rows],
    }, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    ranked_graph = output_dir / "graph.graphml"
    with tempfile.NamedTemporaryFile(dir=output_dir, prefix=".graph.", suffix=".graphml", delete=False) as stream:
        temporary = Path(stream.name)
    nx.write_graphml(graph, temporary, encoding="utf-8", prettyprint=False, infer_numeric_types=True)
    os.replace(temporary, ranked_graph)

    result = {
        "schema_version": 1, "input_graph": str(graphml), "input_graph_sha256": sha256_file(graphml),
        "bc250": str(bc250), "bc250_sha256": sha256_file(bc250), "candidate_count": len(rows),
        "city_point_count": len(cities), "scenarios": SCENARIOS,
        "outputs": {name: {"path": str(path), "sha256": sha256_file(path)} for name, path in {
            "table": table, "geojson": geojson, "graph": ranked_graph,
        }.items()},
        "top_10_robust": [{key: row[key] for key in (
            "robust_rank", "node_id", "name", "kind", "mean_scenario_rank", "rank_range",
            "rank_balanced", "rank_altitude_priority", "rank_logistics_rf_priority",
        )} for row in rows[:10]],
        "screening_semantics": SEMANTICS,
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graphml", type=Path, required=True)
    parser.add_argument("--bc250", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.graphml, args.bc250, args.output_dir, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
