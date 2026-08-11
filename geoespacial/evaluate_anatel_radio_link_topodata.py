#!/usr/bin/env python3
"""Repete terreno, curvatura e Fresnel dos candidatos com TOPODATA."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import os
import tempfile
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

from PIL import Image

from audit_anatel_spectrum import number
from build_canonical_smp import deterministic_gzip_csv, sha256_file
from evaluate_anatel_radio_link_terrain import FIELDS, classify, profile


class Topodata:
    """Amostrador de GeoTIFFs com cache LRU limitado."""

    def __init__(self, root: Path, index_path: Path, cache_size: int = 6):
        self.root = root
        self.cache_size = cache_size
        index = json.loads(index_path.read_text(encoding="utf-8"))
        self.tiles = []
        for feature in index["features"]:
            ring = feature["geometry"]["coordinates"][0]
            west = min(point[0] for point in ring)
            east = max(point[0] for point in ring)
            south = min(point[1] for point in ring)
            north = max(point[1] for point in ring)
            properties = feature["properties"]
            self.tiles.append((west, south, east, north, properties["geotiff"], properties["pixel_size_x_degrees"], properties["pixel_size_y_degrees"]))
        self.images: OrderedDict[str, Image.Image] = OrderedDict()

    def _image(self, name: str) -> Image.Image | None:
        if name in self.images:
            self.images.move_to_end(name)
            return self.images[name]
        path = self.root / name
        if not path.is_file():
            return None
        image = Image.open(path)
        self.images[name] = image
        if len(self.images) > self.cache_size:
            _, old = self.images.popitem(last=False)
            old.close()
        return image

    def __call__(self, latitude: float, longitude: float) -> float | None:
        epsilon = 1e-9
        for west, south, east, north, name, pixel_x, pixel_y in self.tiles:
            if west - epsilon <= longitude <= east + epsilon and south - epsilon <= latitude <= north + epsilon:
                image = self._image(name)
                if image is None:
                    return None
                x = min(image.width - 1, max(0, int(math.floor((longitude - west) / pixel_x))))
                y = min(image.height - 1, max(0, int(math.floor((north - latitude) / pixel_y))))
                value = float(image.getpixel((x, y)))
                return None if not math.isfinite(value) or value <= -9999 else value
        return None

    def close(self) -> None:
        for image in self.images.values():
            image.close()
        self.images.clear()


def prior_statuses(path: Path | None) -> dict[str, tuple[str, str]]:
    if path is None:
        return {}
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        return {row["candidate_id"]: (row["terrain_status_k1"], row["terrain_status_k4_3"]) for row in csv.DictReader(stream)}


def evaluate(geometry: Path, keys: Path, emissions: Path, terrain_root: Path, terrain_index: Path, output: Path, report: Path, preliminary: Path | None = None) -> dict:
    selected = {}
    with gzip.open(geometry, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["geometry_status"] == "azimuth_consistent_15deg":
                selected[(row["link_family"], row["service_fistel"], row["rf_act_number"])] = row
    source_rows = {}
    groups = defaultdict(list)
    with gzip.open(keys, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            key = (row["link_family"], row["service_fistel"], row["rf_act_number"])
            if key in selected:
                source_rows[row["source_row_number"]] = key
    with gzip.open(emissions, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            key = source_rows.get(row["source_row_number"])
            if key:
                groups[key].append(row)

    terrain = Topodata(terrain_root, terrain_index)
    previous = prior_statuses(preliminary)
    counts, counts43, transitions, transitions43 = Counter(), Counter(), Counter(), Counter()
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix="link-topodata-", dir=output.parent) as directory:
            staged = Path(directory) / output.name
            with deterministic_gzip_csv(staged, FIELDS) as writer:
                for key in sorted(selected):
                    geometry_row = selected[key]
                    a = tuple(map(float, geometry_row["coordinate_a"].split(",")))
                    b = tuple(map(float, geometry_row["coordinate_b"].split(",")))
                    endpoint = defaultdict(lambda: {"tx": set(), "rx": set(), "height": []})
                    for emission in groups[key]:
                        coordinate = (number(emission["latitude"]), number(emission["longitude"]))
                        frequency = number(emission["frequency_mhz"])
                        height = number(emission["antenna_height_m"])
                        if frequency is not None:
                            endpoint[coordinate]["tx" if emission["direction"] == "Transmissão" else "rx"].add(frequency)
                        if height is not None:
                            endpoint[coordinate]["height"].append(height)
                    reciprocal = (endpoint[a]["tx"] & endpoint[b]["rx"]) | (endpoint[b]["tx"] & endpoint[a]["rx"])
                    frequency = min(reciprocal)
                    height_a = max(endpoint[a]["height"] or [0])
                    height_b = max(endpoint[b]["height"] or [0])
                    distance = float(geometry_row["distance_km"])
                    k1 = profile(a, b, distance, height_a, height_b, frequency, terrain, k=1)
                    k43 = profile(a, b, distance, height_a, height_b, frequency, terrain, k=4 / 3)
                    status1, status43 = classify(k1), classify(k43)
                    counts[status1] += 1
                    counts43[status43] += 1
                    candidate_id = geometry_row["candidate_id"]
                    if candidate_id in previous:
                        transitions[(previous[candidate_id][0], status1)] += 1
                        transitions43[(previous[candidate_id][1], status43)] += 1
                    writer.writerow({
                        "candidate_id": candidate_id, "link_family": key[0], "service_fistel": key[1], "rf_act_number": key[2],
                        "distance_km": distance, "minimum_reciprocal_frequency_mhz": frequency,
                        "antenna_height_a_m": height_a, "antenna_height_b_m": height_b,
                        "terrain_samples": k1["samples"], "missing_samples": max(k1["missing"], k43["missing"]),
                        "minimum_los_clearance_k1_m": "" if k1["los"] is None else k1["los"],
                        "minimum_fresnel60_clearance_k1_m": "" if k1["fresnel"] is None else k1["fresnel"],
                        "minimum_los_clearance_k4_3_m": "" if k43["los"] is None else k43["los"],
                        "minimum_fresnel60_clearance_k4_3_m": "" if k43["fresnel"] is None else k43["fresnel"],
                        "terrain_status_k1": status1, "terrain_status_k4_3": status43,
                        "pairing_status": "not_performed", "terrain_source": "TOPODATA/INPE numeric altitude GeoTIFF",
                        "height_semantics": "maximum registered antenna height per endpoint; optimistic upper bound",
                    })
            os.replace(staged, output)
    finally:
        terrain.close()

    def transition_rows(counter: Counter) -> list[dict]:
        return [{"from": old, "to": new, "count": count} for (old, new), count in sorted(counter.items())]

    result = {
        "schema_version": 1, "geometry_file": str(geometry), "geometry_sha256": sha256_file(geometry),
        "terrain_index": str(terrain_index), "terrain_index_sha256": sha256_file(terrain_index),
        "candidate_groups": len(selected), "status_k1": dict(sorted(counts.items())), "status_k4_3": dict(sorted(counts43.items())),
        "sample_spacing_km": 1.0, "curvature_models": [1.0, 4 / 3], "fresnel_clearance_fraction": 0.6,
        "terrain_semantics": "TOPODATA numeric altitude; missing coverage fails closed",
        "antenna_height_semantics": "maximum per endpoint is optimistic", "pairing_status": "not_performed",
        "preliminary_file": None if preliminary is None else str(preliminary),
        "transitions_from_preliminary_k1": transition_rows(transitions),
        "transitions_from_preliminary_k4_3": transition_rows(transitions43), "output": str(output),
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(prefix=f".{report.name}.", dir=report.parent, delete=False) as stream:
        stream.write(payload)
        temporary = Path(stream.name)
    os.replace(temporary, report)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--geometry", type=Path, required=True)
    parser.add_argument("--keys", type=Path, required=True)
    parser.add_argument("--emissions", type=Path, required=True)
    parser.add_argument("--terrain-root", type=Path, required=True)
    parser.add_argument("--terrain-index", type=Path, required=True)
    parser.add_argument("--preliminary", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(evaluate(args.geometry, args.keys, args.emissions, args.terrain_root, args.terrain_index, args.output, args.report, args.preliminary), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
