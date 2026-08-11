#!/usr/bin/env /home/python/pyenv/bin/python
"""Analisa a triangulação basal dos candidatos sem promover visada ou iluminação."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np
from scipy.spatial import Delaunay

from build_canonical_smp import sha256_file
from enrich_candidate_geospatial_context import coordinates, deterministic_gzip_csv


EARTH_RADIUS_KM = 6371.0088
PROJECTION_CENTRE = (-54.0, -15.0)
SEMANTICS = (
    "Delaunay baseline in Lambert azimuthal equal-area projection; mesh edges use "
    "curvature-only candidate upper bounds pending terrain; illuminator membership "
    "is geometric and does not assert RF illumination or echo detectability"
)
CANDIDATE_TYPES = {"capital", "airport", "candidate_radome_gap"}


def lambert_azimuthal_equal_area(longitude: float, latitude: float) -> tuple[float, float]:
    lon0, lat0 = map(math.radians, PROJECTION_CENTRE)
    lon, lat = math.radians(longitude), math.radians(latitude)
    denominator = 1 + math.sin(lat0) * math.sin(lat) + math.cos(lat0) * math.cos(lat) * math.cos(lon - lon0)
    scale = math.sqrt(2 / denominator)
    x = EARTH_RADIUS_KM * scale * math.cos(lat) * math.sin(lon - lon0)
    y = EARTH_RADIUS_KM * scale * (math.cos(lat0) * math.sin(lat) - math.sin(lat0) * math.cos(lat) * math.cos(lon - lon0))
    return x, y


def triangle_quality(points: np.ndarray) -> dict[str, float]:
    sides = [float(np.linalg.norm(points[(index + 1) % 3] - points[index])) for index in range(3)]
    angles = []
    for opposite, adjacent_a, adjacent_b in ((sides[1], sides[0], sides[2]), (sides[2], sides[0], sides[1]), (sides[0], sides[1], sides[2])):
        cosine = (adjacent_a**2 + adjacent_b**2 - opposite**2) / (2 * adjacent_a * adjacent_b)
        angles.append(math.degrees(math.acos(max(-1.0, min(1.0, cosine)))))
    first = points[1] - points[0]
    second = points[2] - points[0]
    area = abs(float(first[0] * second[1] - first[1] * second[0])) / 2
    return {
        "projected_area_km2": area, "minimum_angle_deg": min(angles),
        "maximum_edge_km": max(sides), "minimum_edge_km": min(sides),
        "edge_aspect_ratio": max(sides) / min(sides),
    }


def face_status(available_edge_count: int) -> str:
    if available_edge_count == 3:
        return "triangle_k3_curvature_pending"
    if available_edge_count == 2:
        return "triangle_two_edge_curvature_pending"
    return "triangle_sparse_curvature_pending"


def read_grid(path: Path) -> list[dict]:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build(graphml: Path, grid: Path, output_dir: Path, report: Path) -> dict:
    graph = nx.read_graphml(graphml, force_multigraph=True)
    candidates = []
    infrastructure = []
    for identifier, attributes in sorted(graph.nodes(data=True)):
        node_type = str(attributes.get("node_type", ""))
        if node_type in CANDIDATE_TYPES:
            latitude, longitude = coordinates(attributes)
            candidates.append({"node_id": identifier, "name": attributes.get("name", ""), "longitude": longitude, "latitude": latitude})
        elif node_type in {"torre_smp", "radiodifusao", "anatel_cadastral_endpoint"}:
            latitude, longitude = coordinates(attributes)
            infrastructure.append((longitude, latitude, node_type))
    projected = np.array([lambert_azimuthal_equal_area(row["longitude"], row["latitude"]) for row in candidates])
    triangulation = Delaunay(projected)

    available_edges = set()
    for origin, destination, attributes in graph.edges(data=True):
        if attributes.get("relation") == "candidate_visibility_upper_bound":
            available_edges.add(tuple(sorted((str(origin), str(destination)))))

    faces = []
    simplex_to_face = {}
    stable_simplices = sorted(
        ((tuple(sorted(candidates[index]["node_id"] for index in simplex)), simplex_index, simplex) for simplex_index, simplex in enumerate(triangulation.simplices)),
        key=lambda item: item[0],
    )
    for position, (vertex_ids, simplex_index, simplex) in enumerate(stable_simplices, 1):
        digest = hashlib.sha1("|".join(vertex_ids).encode()).hexdigest()[:12]
        face_id = f"triangle:{digest}"
        simplex_to_face[simplex_index] = position - 1
        edge_count = sum(tuple(sorted((vertex_ids[left], vertex_ids[right]))) in available_edges for left, right in ((0, 1), (1, 2), (0, 2)))
        vertices = [candidates[index] for index in simplex]
        quality = triangle_quality(projected[simplex])
        faces.append({
            "face_id": face_id, "vertex_ids": "|".join(vertex_ids),
            "vertex_names": "|".join(sorted(str(vertex["name"]) for vertex in vertices)),
            "available_curvature_edge_count": edge_count, "face_status": face_status(edge_count),
            **{key: round(value, 6) for key, value in quality.items()},
            "smp_site_count": 0, "broadcast_site_count": 0, "radio_link_endpoint_count": 0,
            "continental_grid_cell_count": 0, "continental_grid_area_km2": 0.0,
            "mesh_semantics": SEMANTICS,
            "_coordinates": [[vertex["longitude"], vertex["latitude"]] for vertex in vertices],
        })

    if infrastructure:
        emitter_points = np.array([lambert_azimuthal_equal_area(longitude, latitude) for longitude, latitude, _ in infrastructure])
        emitter_simplices = triangulation.find_simplex(emitter_points)
        count_field = {"torre_smp": "smp_site_count", "radiodifusao": "broadcast_site_count", "anatel_cadastral_endpoint": "radio_link_endpoint_count"}
        for simplex_index, (_, _, node_type) in zip(emitter_simplices, infrastructure, strict=True):
            if simplex_index >= 0:
                faces[simplex_to_face[int(simplex_index)]][count_field[node_type]] += 1

    grid_rows = read_grid(grid)
    grid_points = np.array([lambert_azimuthal_equal_area(float(row["longitude"]), float(row["latitude"])) for row in grid_rows])
    grid_simplices = triangulation.find_simplex(grid_points)
    outside_cells = outside_area = 0.0
    for simplex_index, cell in zip(grid_simplices, grid_rows, strict=True):
        area = float(cell["approximate_area_km2"])
        if simplex_index < 0:
            outside_cells += 1
            outside_area += area
        else:
            face = faces[simplex_to_face[int(simplex_index)]]
            face["continental_grid_cell_count"] += 1
            face["continental_grid_area_km2"] += area
    for face in faces:
        face["continental_grid_area_km2"] = round(face["continental_grid_area_km2"], 6)

    output_dir.mkdir(parents=True, exist_ok=True)
    table = output_dir / "triangular_faces.csv.gz"
    public_faces = [{key: value for key, value in face.items() if key != "_coordinates"} for face in faces]
    deterministic_gzip_csv(table, public_faces, list(public_faces[0]))
    geojson = output_dir / "triangular_mesh.geojson"
    geojson.write_text(json.dumps({
        "type": "FeatureCollection", "name": "candidate_triangular_mesh",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4674"}},
        "features": [{
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [[*face["_coordinates"], face["_coordinates"][0]]]},
            "properties": {key: value for key, value in face.items() if key != "_coordinates"},
        } for face in faces],
    }, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")

    status_counts = Counter(face["face_status"] for face in faces)
    total_grid_area = sum(float(row["approximate_area_km2"]) for row in grid_rows)
    result = {
        "schema_version": 1, "input_graph": str(graphml), "input_graph_sha256": sha256_file(graphml),
        "input_grid": str(grid), "input_grid_sha256": sha256_file(grid),
        "projection": "Lambert azimuthal equal-area sphere R=6371.0088 km, centre 54W 15S",
        "candidate_vertex_count": len(candidates), "delaunay_face_count": len(faces),
        "face_status_counts": dict(sorted(status_counts.items())),
        "continental_grid_cell_count": len(grid_rows), "grid_cells_inside_mesh_count": len(grid_rows) - int(outside_cells),
        "grid_cells_outside_mesh_count": int(outside_cells),
        "area_weighted_mesh_fraction": (total_grid_area - outside_area) / total_grid_area,
        "faces_with_smp": sum(face["smp_site_count"] > 0 for face in faces),
        "faces_with_broadcast": sum(face["broadcast_site_count"] > 0 for face in faces),
        "faces_with_radio_link_endpoint": sum(face["radio_link_endpoint_count"] > 0 for face in faces),
        "infrastructure_inside_mesh_counts": {
            "torre_smp": sum(face["smp_site_count"] for face in faces),
            "radiodifusao": sum(face["broadcast_site_count"] for face in faces),
            "anatel_cadastral_endpoint": sum(face["radio_link_endpoint_count"] for face in faces),
        },
        "outputs": {name: {"path": str(path), "sha256": sha256_file(path)} for name, path in {"table": table, "geojson": geojson}.items()},
        "mesh_semantics": SEMANTICS,
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graphml", type=Path, required=True)
    parser.add_argument("--grid", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.graphml, args.grid, args.output_dir, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
