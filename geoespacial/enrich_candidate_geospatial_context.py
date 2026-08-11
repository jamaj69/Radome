#!/usr/bin/env /usr/bin/python3
"""Vincula candidatos a municípios e conta infraestrutura no raio geométrico."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import os
import tempfile
from collections import Counter
from pathlib import Path

import networkx as nx

from build_canonical_smp import sha256_file


EARTH_RADIUS_KM = 6371.0088
CANDIDATE_TYPES = {"capital", "airport"}
INFRASTRUCTURE_TYPES = {
    "torre_smp": "nearby_smp_site_count",
    "radiodifusao": "nearby_broadcast_site_count",
    "anatel_cadastral_endpoint": "nearby_radio_link_endpoint_count",
}
PROXIMITY_SEMANTICS = (
    "great-circle distance within candidate preliminary curvature-only radius; "
    "terrain visibility and RF illumination not evaluated"
)


def coordinates(attributes: dict) -> tuple[float, float]:
    latitude = attributes.get("latitude", attributes.get("y_latitude"))
    longitude = attributes.get("longitude", attributes.get("x_longitude"))
    return float(latitude), float(longitude)


def distance_km(latitude: float, longitude: float, other_latitude: float, other_longitude: float) -> float:
    lat1, lat2 = math.radians(latitude), math.radians(other_latitude)
    delta_latitude = lat2 - lat1
    delta_longitude = math.radians(other_longitude - longitude)
    value = math.sin(delta_latitude / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_longitude / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(min(1.0, math.sqrt(value)))


def municipality_polygons(gpkg: Path):
    from osgeo import ogr

    source = ogr.Open(str(gpkg))
    if source is None:
        raise ValueError(f"não foi possível abrir {gpkg}")
    layer = source.GetLayerByName("lml_municipio_a")
    if layer is None:
        raise ValueError("camada lml_municipio_a ausente na BC250")
    polygons = []
    for feature in layer:
        code = str(feature.GetField("geocodigo") or "")
        if len(code) == 7 and feature.GetGeometryRef() is not None:
            polygons.append((code, feature.GetGeometryRef().Clone()))
    return polygons


def containing_municipality(longitude: float, latitude: float, polygons) -> str | None:
    from osgeo import ogr

    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(longitude, latitude)
    for code, polygon in polygons:
        envelope = polygon.GetEnvelope()  # minx, maxx, miny, maxy
        if not (envelope[0] <= longitude <= envelope[1] and envelope[2] <= latitude <= envelope[3]):
            continue
        if polygon.Contains(point) or polygon.Intersects(point):
            return code
    return None


def deterministic_gzip_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as raw:
        temporary = Path(raw.name)
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with __import__("io").TextIOWrapper(compressed, encoding="utf-8", newline="") as text:
                writer = csv.DictWriter(text, fieldnames=fields, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
    os.replace(temporary, path)


def build(graphml: Path, bc250: Path, output: Path, table: Path, report: Path) -> dict:
    graph = nx.read_graphml(graphml, force_multigraph=True)
    polygons = municipality_polygons(bc250)
    infrastructure: dict[str, list[tuple[float, float]]] = {kind: [] for kind in INFRASTRUCTURE_TYPES}
    for _, attributes in graph.nodes(data=True):
        kind = str(attributes.get("node_type", ""))
        if kind in infrastructure:
            infrastructure[kind].append(coordinates(attributes))

    candidates = []
    missing_municipality = 0
    for identifier, attributes in sorted(graph.nodes(data=True)):
        kind = str(attributes.get("node_type", ""))
        if kind not in CANDIDATE_TYPES:
            continue
        latitude, longitude = coordinates(attributes)
        radius = float(attributes["coverage_radius_km"])
        code = containing_municipality(longitude, latitude, polygons)
        if code is None:
            missing_municipality += 1
        counts = {
            field: sum(distance_km(latitude, longitude, other_latitude, other_longitude) <= radius for other_latitude, other_longitude in infrastructure[node_type])
            for node_type, field in INFRASTRUCTURE_TYPES.items()
        }
        attributes.update(
            canonical_municipality_code=code or "",
            proximity_semantics=PROXIMITY_SEMANTICS,
            **counts,
        )
        if code:
            municipal_id = f"municipio:{code}"
            if municipal_id not in graph:
                raise ValueError(f"município canônico ausente do grafo: {municipal_id}")
            graph.add_edge(
                identifier, municipal_id, key=f"candidate_municipality:{identifier}",
                relation="located_in", source_layer="candidate_municipality_bc250",
                directed_semantics=True, operational_edge=False,
                association_method="BC250 point-in-polygon",
            )
        candidates.append({
            "node_id": identifier, "kind": kind, "name": attributes.get("name", ""),
            "longitude": longitude, "latitude": latitude,
            "terrain_elevation_m": attributes.get("terrain_elevation_m", ""),
            "coverage_radius_km": radius, "canonical_municipality_code": code or "",
            **counts, "proximity_semantics": PROXIMITY_SEMANTICS,
        })

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, prefix=f".{output.name}.", suffix=".graphml", delete=False) as stream:
        temporary = Path(stream.name)
    try:
        nx.write_graphml(graph, temporary, encoding="utf-8", prettyprint=False, infer_numeric_types=True)
        os.replace(temporary, output)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    fields = list(candidates[0])
    deterministic_gzip_csv(table, candidates, fields)

    relation_counts = Counter(str(data.get("relation") or data.get("edge_type") or "unknown") for _, _, data in graph.edges(data=True))
    result = {
        "schema_version": 1,
        "input_graph": str(graphml), "input_graph_sha256": sha256_file(graphml),
        "bc250": str(bc250), "bc250_sha256": sha256_file(bc250),
        "output_graph": str(output), "output_graph_sha256": sha256_file(output),
        "candidate_table": str(table), "candidate_table_sha256": sha256_file(table),
        "candidate_count": len(candidates),
        "candidate_type_counts": dict(sorted(Counter(row["kind"] for row in candidates).items())),
        "candidate_municipality_match_count": len(candidates) - missing_municipality,
        "candidate_municipality_missing_count": missing_municipality,
        "infrastructure_node_counts": {kind: len(values) for kind, values in sorted(infrastructure.items())},
        "proximity_count_totals": {field: sum(int(row[field]) for row in candidates) for field in INFRASTRUCTURE_TYPES.values()},
        "edge_relation_counts": dict(sorted(relation_counts.items())),
        "operational_edge_count": sum(bool(data.get("operational_edge")) for _, _, data in graph.edges(data=True)),
        "proximity_semantics": PROXIMITY_SEMANTICS,
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graphml", type=Path, required=True)
    parser.add_argument("--bc250", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--table", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.graphml, args.bc250, args.output, args.table, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
