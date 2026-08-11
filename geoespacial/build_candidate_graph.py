#!/usr/bin/env python3
"""Build a preliminary capital/airport coverage graph for continental Brazil."""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import subprocess
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image

from preselect_bc250 import Point, distance_km

EARTH_RADIUS_M = 6_371_008.8
TERRARIUM_URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"


def read_layer(gpkg: Path, layer: str, where: str | None = None) -> list[dict[str, object]]:
    command = ["ogr2ogr", "-f", "GeoJSON", "/vsistdout/", str(gpkg), layer]
    if where:
        command.extend(["-where", where])
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)["features"]


def tile_pixel(longitude: float, latitude: float, zoom: int) -> tuple[int, int, int, int]:
    scale = 2**zoom
    x_float = (longitude + 180.0) / 360.0 * scale
    latitude_rad = math.radians(max(min(latitude, 85.05112878), -85.05112878))
    y_float = (1.0 - math.asinh(math.tan(latitude_rad)) / math.pi) / 2.0 * scale
    x_tile, y_tile = int(x_float), int(y_float)
    return x_tile, y_tile, int((x_float - x_tile) * 256), int((y_float - y_tile) * 256)


def terrain_elevation(longitude: float, latitude: float, zoom: int, cache: Path) -> float:
    x_tile, y_tile, pixel_x, pixel_y = tile_pixel(longitude, latitude, zoom)
    target = cache / str(zoom) / str(x_tile) / f"{y_tile}.png"
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(TERRARIUM_URL.format(z=zoom, x=x_tile, y=y_tile), timeout=120) as response:
            target.write_bytes(response.read())
    with Image.open(target) as image:
        red, green, blue = image.convert("RGB").getpixel((pixel_x, pixel_y))
    return red * 256.0 + green + blue / 256.0 - 32768.0


def horizon_km(height_m: float, effective_radius_factor: float) -> float:
    height = max(height_m, 0.0)
    radius = EARTH_RADIUS_M * effective_radius_factor
    return math.sqrt(2.0 * radius * height + height * height) / 1000.0


def node_id(kind: str, feature: dict[str, object]) -> str:
    properties = feature["properties"]
    # Airport code fields may contain repeated placeholders such as "NI".
    # Capital geocodes are stable; every other feature uses its unique OGR id.
    if kind == "capital":
        stable = properties.get("geocodigo")
    else:
        coordinates = feature.get("geometry", {}).get("coordinates", [])
        stable = f"{coordinates[0]:.8f}:{coordinates[1]:.8f}" if len(coordinates) >= 2 else None
    if stable is None:
        raise ValueError(f"feature without stable identifier: {feature}")
    return f"{kind}:{stable}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bc250", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--terrain-cache", type=Path, required=True)
    parser.add_argument("--terrain-zoom", type=int, default=8)
    parser.add_argument("--target-altitude-m", type=float, default=3000.0)
    parser.add_argument("--radome-height-agl-m", type=float, default=15.0)
    parser.add_argument("--earth-radius-factor", type=float, default=4.0 / 3.0)
    args = parser.parse_args()

    capitals = read_layer(args.bc250, "lml_capital_p", "geocodigo IS NOT NULL")
    airports = read_layer(args.bc250, "aer_complexo_aeroportuario_p")
    cities = read_layer(args.bc250, "lml_cidade_p", "geocodigo IS NOT NULL")
    city_points = [Point(feature["properties"]["nome"], *feature["geometry"]["coordinates"][:2]) for feature in cities]

    graph = nx.Graph(
        scope="continental_brazil",
        radius_model="geometric_upper_bound_without_intermediate_terrain_occlusion",
        target_altitude_m=args.target_altitude_m,
        effective_earth_radius_factor=args.earth_radius_factor,
    )
    node_features = []
    for kind, features in (("capital", capitals), ("airport", airports)):
        for feature in features:
            longitude, latitude = feature["geometry"]["coordinates"][:2]
            elevation = terrain_elevation(longitude, latitude, args.terrain_zoom, args.terrain_cache)
            coverage_radius = horizon_km(elevation + args.radome_height_agl_m, args.earth_radius_factor) + horizon_km(
                args.target_altitude_m, args.earth_radius_factor
            )
            origin = Point(str(feature["properties"].get("nome") or "sem nome"), longitude, latitude)
            covered_cities = [city for city in city_points if distance_km(origin, city) <= coverage_radius]
            identifier = node_id(kind, feature)
            attributes = {
                "name": origin.name,
                "kind": kind,
                "longitude": longitude,
                "latitude": latitude,
                "terrain_elevation_m": round(elevation, 2),
                "terrain_source": f"Mapzen Terrain Tiles terrarium z{args.terrain_zoom}",
                "radome_height_agl_m": args.radome_height_agl_m,
                "target_altitude_m": args.target_altitude_m,
                "coverage_radius_km": round(coverage_radius, 3),
                "nearby_city_count": len(covered_cities),
                "radius_status": "geometric_upper_bound_topographic_occlusion_pending",
            }
            graph.add_node(identifier, **attributes)
            node_features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                "properties": {"node_id": identifier, **attributes},
            })

    nodes = list(graph.nodes(data=True))
    for index, (left_id, left) in enumerate(nodes):
        left_point = Point(left["name"], left["longitude"], left["latitude"])
        left_ground_horizon = horizon_km(left["terrain_elevation_m"] + args.radome_height_agl_m, args.earth_radius_factor)
        for right_id, right in nodes[index + 1:]:
            right_point = Point(right["name"], right["longitude"], right["latitude"])
            separation = distance_km(left_point, right_point)
            right_ground_horizon = horizon_km(right["terrain_elevation_m"] + args.radome_height_agl_m, args.earth_radius_factor)
            if separation <= left_ground_horizon + right_ground_horizon:
                graph.add_edge(left_id, right_id, distance_km=round(separation, 3), status="curvature_only_terrain_pending")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(graph, args.output_dir / "candidate_graph.graphml")
    (args.output_dir / "candidate_nodes.geojson").write_text(json.dumps({
        "type": "FeatureCollection", "name": "candidate_nodes", "features": node_features,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = [{"node_id": node, "degree": graph.degree(node), **attributes} for node, attributes in graph.nodes(data=True)]
    rows.sort(key=lambda row: (int(row["nearby_city_count"]), int(row["degree"])), reverse=True)
    with (args.output_dir / "candidate_nodes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

    positions = {node: (data["longitude"], data["latitude"]) for node, data in graph.nodes(data=True)}
    sizes = [max(30.0, graph.nodes[node]["coverage_radius_km"] ** 1.35) for node in graph]
    colours = ["#d88132" if graph.nodes[node]["kind"] == "capital" else "#4f8fbd" for node in graph]
    figure, axis = plt.subplots(figsize=(12, 12))
    nx.draw_networkx_edges(graph, positions, ax=axis, width=.35, alpha=.20, edge_color="#54606b")
    nx.draw_networkx_nodes(graph, positions, ax=axis, node_size=sizes, node_color=colours, alpha=.72, linewidths=.4, edgecolors="#243746")
    axis.set_title("Grafo preliminar de candidatos — capitais e aeroportos\nraio do nó ∝ horizonte geométrico a 3.000 m; bloqueio topográfico pendente")
    axis.set_xlabel("longitude"); axis.set_ylabel("latitude"); axis.grid(alpha=.15)
    figure.tight_layout(); figure.savefig(args.output_dir / "candidate_graph.png", dpi=180); plt.close(figure)

    summary = {
        "capital_nodes": len(capitals), "airport_nodes": len(airports),
        "nodes": graph.number_of_nodes(), "curvature_candidate_edges": graph.number_of_edges(),
        "connected_components": nx.number_connected_components(graph),
        "isolated_nodes": len(list(nx.isolates(graph))),
        "target_altitude_m": args.target_altitude_m,
        "radius_status": "geometric upper bound; intermediate terrain viewshed pending",
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
