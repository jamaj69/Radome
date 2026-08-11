#!/usr/bin/env /home/python/pyenv/bin/python
"""Gera uma semente de terreno alto por célula continental descoberta."""

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

import numpy as np
from PIL import Image

from build_canonical_smp import deterministic_gzip_csv, sha256_file


SEMANTICS = (
    "highest valid TOPODATA pixel centre inside each uncovered grid cell; "
    "relative relief is cell maximum minus cell minimum, not topographic prominence; "
    "not a validated radome site, viewshed, line of sight, or RF coverage"
)


def pixel_window(
    tile_west: float,
    tile_north: float,
    pixel_x: float,
    pixel_y: float,
    width: int,
    height: int,
    cell_west: float,
    cell_south: float,
    cell_east: float,
    cell_north: float,
) -> tuple[int, int, int, int]:
    """Retorna janela semiaberta de pixels cujos centros caem dentro da célula."""
    x0 = max(0, math.ceil((cell_west - tile_west) / pixel_x - 0.5 - 1e-9))
    x1 = min(width, math.floor((cell_east - tile_west) / pixel_x - 0.5 + 1e-9) + 1)
    y0 = max(0, math.ceil((tile_north - cell_north) / pixel_y - 0.5 - 1e-9))
    y1 = min(height, math.floor((tile_north - cell_south) / pixel_y - 0.5 + 1e-9) + 1)
    return x0, y0, max(x0, x1), max(y0, y1)


def load_tiles(index_path: Path) -> list[dict]:
    index = json.loads(index_path.read_text(encoding="utf-8"))
    tiles = []
    for feature in index["features"]:
        ring = feature["geometry"]["coordinates"][0]
        properties = feature["properties"]
        tiles.append({
            "west": min(point[0] for point in ring),
            "south": min(point[1] for point in ring),
            "east": max(point[0] for point in ring),
            "north": max(point[1] for point in ring),
            "geotiff": properties["geotiff"],
            "pixel_x": float(properties["pixel_size_x_degrees"]),
            "pixel_y": float(properties["pixel_size_y_degrees"]),
        })
    return sorted(tiles, key=lambda item: item["geotiff"])


def intersecting(tile: dict, west: float, south: float, east: float, north: float) -> bool:
    return tile["west"] < east and tile["east"] > west and tile["south"] < north and tile["north"] > south


def seed_cell(row: dict, tiles: list[dict], terrain_root: Path, resolution_deg: float) -> dict:
    latitude = float(row["latitude"])
    longitude = float(row["longitude"])
    half = resolution_deg / 2
    west, east = longitude - half, longitude + half
    south, north = latitude - half, latitude + half
    best: tuple[float, float, float, str] | None = None
    valid_count = 0
    elevation_sum = 0.0
    minimum = math.inf
    source_tiles = []

    for tile in tiles:
        if not intersecting(tile, west, south, east, north):
            continue
        path = terrain_root / tile["geotiff"]
        if not path.is_file():
            continue
        with Image.open(path) as image:
            x0, y0, x1, y1 = pixel_window(
                tile["west"], tile["north"], tile["pixel_x"], tile["pixel_y"],
                image.width, image.height, west, south, east, north,
            )
            if x0 >= x1 or y0 >= y1:
                continue
            values = np.asarray(image.crop((x0, y0, x1, y1)), dtype=np.float64)
        valid = np.isfinite(values) & (values > -9999)
        if not valid.any():
            continue
        source_tiles.append(tile["geotiff"])
        selected = values[valid]
        valid_count += int(selected.size)
        elevation_sum += float(selected.sum())
        minimum = min(minimum, float(selected.min()))
        maximum = float(selected.max())
        positions = np.argwhere(valid & (values == maximum))
        for local_y, local_x in positions:
            x = x0 + int(local_x)
            y = y0 + int(local_y)
            candidate_longitude = tile["west"] + (x + 0.5) * tile["pixel_x"]
            candidate_latitude = tile["north"] - (y + 0.5) * tile["pixel_y"]
            candidate = (maximum, -candidate_latitude, -candidate_longitude, tile["geotiff"])
            if best is None or candidate > best:
                best = candidate

    if best is None:
        return {
            "seed_id": f"gap-seed:{row['cell_id']}", "cell_id": row["cell_id"], "uf": row["uf"],
            "cell_longitude": longitude, "cell_latitude": latitude, "longitude": "", "latitude": "",
            "elevation_m": "", "cell_minimum_m": "", "cell_mean_m": "", "relative_relief_m": "",
            "valid_pixel_count": 0, "source_tiles": "", "terrain_status": "missing", "semantics": SEMANTICS,
        }

    maximum, negative_latitude, negative_longitude, _ = best
    return {
        "seed_id": f"gap-seed:{row['cell_id']}", "cell_id": row["cell_id"], "uf": row["uf"],
        "cell_longitude": longitude, "cell_latitude": latitude,
        "longitude": round(-negative_longitude, 9), "latitude": round(-negative_latitude, 9),
        "elevation_m": round(maximum, 3), "cell_minimum_m": round(minimum, 3),
        "cell_mean_m": round(elevation_sum / valid_count, 3),
        "relative_relief_m": round(maximum - minimum, 3), "valid_pixel_count": valid_count,
        "source_tiles": "|".join(sorted(set(source_tiles))), "terrain_status": "available", "semantics": SEMANTICS,
    }


def generate(
    grid: Path,
    terrain_root: Path,
    terrain_index: Path,
    output_dir: Path,
    report_path: Path,
    resolution_deg: float = 0.25,
) -> dict:
    if resolution_deg <= 0 or resolution_deg > 1:
        raise ValueError("resolution_deg deve estar em (0, 1]")
    tiles = load_tiles(terrain_index)
    with gzip.open(grid, "rt", encoding="utf-8", newline="") as source:
        cells = [row for row in csv.DictReader(source) if int(row["covering_candidate_count"]) == 0]
    rows = [seed_cell(row, tiles, terrain_root, resolution_deg) for row in cells]
    output_dir.mkdir(parents=True, exist_ok=True)
    table = output_dir / "gap_seeds.csv.gz"
    with deterministic_gzip_csv(table, tuple(rows[0])) as writer:
        writer.writerows(rows)
    geojson = output_dir / "gap_seeds.geojson"
    features = [{
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [row["longitude"], row["latitude"]]},
        "properties": {key: value for key, value in row.items() if key not in {"longitude", "latitude", "semantics"}},
    } for row in rows if row["terrain_status"] == "available"]
    geojson.write_text(json.dumps({
        "type": "FeatureCollection", "name": "topodata_gap_candidate_seeds",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": features,
    }, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    status_counts = Counter(row["terrain_status"] for row in rows)
    available = [row for row in rows if row["terrain_status"] == "available"]
    report = {
        "schema_version": 1, "grid_file": str(grid), "grid_sha256": sha256_file(grid),
        "terrain_index": str(terrain_index), "terrain_index_sha256": sha256_file(terrain_index),
        "resolution_deg": resolution_deg, "uncovered_cell_count": len(cells), "seed_count": len(available),
        "status_counts": dict(sorted(status_counts.items())),
        "seed_count_by_uf": dict(sorted(Counter(row["uf"] for row in available).items())),
        "elevation_range_m": [min(float(row["elevation_m"]) for row in available), max(float(row["elevation_m"]) for row in available)],
        "relative_relief_range_m": [min(float(row["relative_relief_m"]) for row in available), max(float(row["relative_relief_m"]) for row in available)],
        "outputs": {"table": {"path": str(table), "sha256": sha256_file(table)}, "geojson": {"path": str(geojson), "sha256": sha256_file(geojson)}},
        "semantics": SEMANTICS,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(prefix=f".{report_path.name}.", dir=report_path.parent, delete=False) as target:
        target.write(payload)
        temporary = Path(target.name)
    os.replace(temporary, report_path)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid", type=Path, required=True)
    parser.add_argument("--terrain-root", type=Path, required=True)
    parser.add_argument("--terrain-index", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--resolution-deg", type=float, default=0.25)
    args = parser.parse_args()
    print(json.dumps(generate(args.grid, args.terrain_root, args.terrain_index, args.output_dir, args.report, args.resolution_deg), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
