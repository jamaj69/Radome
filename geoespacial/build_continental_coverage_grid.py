#!/usr/bin/env /usr/bin/python3
"""Constrói grade continental e diagnostica lacunas dos candidatos iniciais."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx

from build_canonical_smp import sha256_file
from enrich_candidate_geospatial_context import deterministic_gzip_csv, distance_km


SEMANTICS = (
    "cell-centre incidence within preliminary curvature-only candidate radius; "
    "not terrain viewshed, RF coverage, or operational service area"
)
EARTH_RADIUS_KM = 6371.0088
CANDIDATE_TYPES = {"capital", "airport", "candidate_radome_gap"}


def approximate_cell_area_km2(latitude: float, resolution_deg: float) -> float:
    angular = math.radians(resolution_deg)
    north = math.radians(min(90.0, latitude + resolution_deg / 2))
    south = math.radians(max(-90.0, latitude - resolution_deg / 2))
    return EARTH_RADIUS_KM**2 * angular * (math.sin(north) - math.sin(south))


def covering_candidates(latitude: float, longitude: float, candidates: list[dict]) -> list[str]:
    return [
        str(candidate["node_id"]) for candidate in candidates
        if distance_km(latitude, longitude, float(candidate["latitude"]), float(candidate["longitude"]))
        <= float(candidate["coverage_radius_km"])
    ]


def optimization_score(attributes: dict, original_candidate_count: int) -> float:
    """Preserva ranking original ou a pontuação de terreno sem misturar escalas."""
    if attributes.get("node_type") == "candidate_radome_gap":
        return max(0.0, min(1.0, float(attributes.get("terrain_score", 0.0))))
    rank = int(attributes["robust_rank"])
    return 1.0 - (rank - 1) / max(1, original_candidate_count - 1)


def federation_units(gpkg: Path):
    from osgeo import ogr

    source = ogr.Open(str(gpkg))
    if source is None:
        raise ValueError(f"não foi possível abrir {gpkg}")
    layer = source.GetLayerByName("lml_unidade_federacao_a")
    if layer is None:
        raise ValueError("camada lml_unidade_federacao_a ausente na BC250")
    units = []
    for feature in layer:
        geometry = feature.GetGeometryRef()
        if geometry is not None:
            units.append({
                "code": str(feature.GetField("geocodigo") or ""),
                "uf": str(feature.GetField("sigla") or ""),
                "name": str(feature.GetField("nome") or ""),
                "geometry": geometry.Clone(), "envelope": geometry.GetEnvelope(),
            })
    return units


def containing_unit(longitude: float, latitude: float, units) -> dict | None:
    from osgeo import ogr

    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(longitude, latitude)
    for unit in units:
        west, east, south, north = unit["envelope"]
        if west <= longitude <= east and south <= latitude <= north:
            geometry = unit["geometry"]
            if geometry.Contains(point) or geometry.Intersects(point):
                return unit
    return None


def build(graphml: Path, bc250: Path, output_dir: Path, report: Path, resolution_deg: float = 0.25) -> dict:
    if resolution_deg <= 0 or resolution_deg > 2:
        raise ValueError("resolution_deg deve estar em (0, 2]")
    graph = nx.read_graphml(graphml, force_multigraph=True)
    original_candidate_count = sum(
        attributes.get("node_type") in {"capital", "airport"}
        for _, attributes in graph.nodes(data=True)
    )
    candidates = []
    for identifier, attributes in sorted(graph.nodes(data=True)):
        if attributes.get("node_type") in CANDIDATE_TYPES:
            candidates.append({
                "node_id": identifier, "latitude": float(attributes["latitude"]),
                "longitude": float(attributes["longitude"]),
                "coverage_radius_km": float(attributes["coverage_radius_km"]),
                "node_type": str(attributes["node_type"]),
                "score": optimization_score(attributes, original_candidate_count),
            })
    units = federation_units(bc250)
    west = math.floor(min(unit["envelope"][0] for unit in units) / resolution_deg) * resolution_deg
    east = min(-34.0, math.ceil(max(unit["envelope"][1] for unit in units) / resolution_deg) * resolution_deg)
    south = math.floor(min(unit["envelope"][2] for unit in units) / resolution_deg) * resolution_deg
    north = math.ceil(max(unit["envelope"][3] for unit in units) / resolution_deg) * resolution_deg

    rows = []
    covers_by_candidate: dict[str, list[str]] = defaultdict(list)
    latitude = south + resolution_deg / 2
    while latitude < north:
        longitude = west + resolution_deg / 2
        while longitude < east:
            unit = containing_unit(longitude, latitude, units)
            if unit is not None:
                cell_id = f"cell:{latitude:+09.4f}:{longitude:+010.4f}"
                covering = covering_candidates(latitude, longitude, candidates)
                for identifier in covering:
                    covers_by_candidate[identifier].append(cell_id)
                rows.append({
                    "cell_id": cell_id, "longitude": round(longitude, 6), "latitude": round(latitude, 6),
                    "uf_code": unit["code"], "uf": unit["uf"],
                    "approximate_area_km2": round(approximate_cell_area_km2(latitude, resolution_deg), 6),
                    "covering_candidate_count": len(covering),
                    "covering_candidate_ids": "|".join(covering), "coverage_semantics": SEMANTICS,
                })
            longitude += resolution_deg
        latitude += resolution_deg

    peer_los: dict[str, set[str]] = defaultdict(set)
    for origin, destination, attributes in graph.edges(data=True):
        if attributes.get("relation") == "candidate_visibility_upper_bound":
            peer_los[str(origin)].add(str(destination))
    ranked = {str(candidate["node_id"]): candidate for candidate in candidates}
    instance = {
        "schema_version": 1, "coverage_semantics": SEMANTICS,
        "required_cells": [row["cell_id"] for row in rows],
        "candidates": [{
            "id": identifier, "covers": covers_by_candidate.get(identifier, []),
            "peer_los": sorted(peer_los.get(identifier, set())), "peer_los_exempt": False,
            "score": round(float(ranked[identifier]["score"]), 9),
        } for identifier in sorted(ranked)],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    table = output_dir / "continental_grid.csv.gz"
    deterministic_gzip_csv(table, rows, list(rows[0]))
    instance_path = output_dir / "coverage_instance.json"
    instance_path.write_text(json.dumps(instance, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    geojson = output_dir / "continental_grid.geojson"
    geojson.write_text(json.dumps({
        "type": "FeatureCollection", "name": "continental_geometric_coverage_grid",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4674"}},
        "features": [{
            "type": "Feature", "geometry": {"type": "Point", "coordinates": [row["longitude"], row["latitude"]]},
            "properties": {key: value for key, value in row.items() if key not in {"longitude", "latitude", "covering_candidate_ids"}},
        } for row in rows],
    }, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")

    total_area = sum(row["approximate_area_km2"] for row in rows)
    covered_area = sum(row["approximate_area_km2"] for row in rows if row["covering_candidate_count"] > 0)
    by_uf = {}
    for uf in sorted({row["uf"] for row in rows}):
        selected = [row for row in rows if row["uf"] == uf]
        area = sum(row["approximate_area_km2"] for row in selected)
        covered = sum(row["approximate_area_km2"] for row in selected if row["covering_candidate_count"] > 0)
        by_uf[uf] = {
            "cell_count": len(selected),
            "uncovered_cell_count": sum(row["covering_candidate_count"] == 0 for row in selected),
            "area_weighted_coverage_fraction": covered / area if area else 0.0,
        }
    coverage_histogram = Counter(int(row["covering_candidate_count"]) for row in rows)
    result = {
        "schema_version": 1, "input_graph": str(graphml), "input_graph_sha256": sha256_file(graphml),
        "bc250": str(bc250), "bc250_sha256": sha256_file(bc250),
        "resolution_deg": resolution_deg, "candidate_count": len(candidates), "cell_count": len(rows),
        "covered_cell_count": sum(row["covering_candidate_count"] > 0 for row in rows),
        "uncovered_cell_count": sum(row["covering_candidate_count"] == 0 for row in rows),
        "single_coverage_cell_count": sum(row["covering_candidate_count"] == 1 for row in rows),
        "redundant_coverage_cell_count": sum(row["covering_candidate_count"] >= 2 for row in rows),
        "area_weighted_coverage_fraction": covered_area / total_area,
        "coverage_count_histogram": {str(key): value for key, value in sorted(coverage_histogram.items())},
        "by_uf": by_uf,
        "outputs": {name: {"path": str(path), "sha256": sha256_file(path)} for name, path in {
            "table": table, "geojson": geojson, "optimization_instance": instance_path,
        }.items()},
        "coverage_semantics": SEMANTICS,
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
    parser.add_argument("--resolution-deg", type=float, default=0.25)
    args = parser.parse_args()
    print(json.dumps(build(args.graphml, args.bc250, args.output_dir, args.report, args.resolution_deg), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
