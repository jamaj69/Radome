#!/usr/bin/env /home/python/pyenv/bin/python
"""Seleciona folhas TOPODATA que intersectam células continentais descobertas."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from build_canonical_smp import sha256_file
from select_topodata_route_tiles import tile_name


def cell_sample_points(latitude: float, longitude: float, resolution_deg: float) -> list[tuple[float, float]]:
    """Retorna centro e cantos internos suficientes para células menores que uma folha."""
    if resolution_deg <= 0 or resolution_deg > 1:
        raise ValueError("resolution_deg deve estar em (0, 1]")
    half = resolution_deg / 2
    epsilon = min(1e-9, resolution_deg / 1_000_000)
    offset = half - epsilon
    return [
        (latitude, longitude),
        (latitude - offset, longitude - offset),
        (latitude - offset, longitude + offset),
        (latitude + offset, longitude - offset),
        (latitude + offset, longitude + offset),
    ]


def select(grid: Path, manifest: Path, output: Path, resolution_deg: float = 0.25) -> dict:
    inventory = json.loads(manifest.read_text(encoding="utf-8"))
    available = {item["name"]: item for item in inventory["archives"]}
    selected_names: set[str] = set()
    missing_names: set[str] = set()
    uncovered_by_uf: Counter[str] = Counter()
    tiles_by_uf: dict[str, set[str]] = defaultdict(set)
    uncovered_cell_count = 0

    with gzip.open(grid, "rt", encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            if int(row["covering_candidate_count"]) != 0:
                continue
            uncovered_cell_count += 1
            uf = row["uf"]
            uncovered_by_uf[uf] += 1
            latitude = float(row["latitude"])
            longitude = float(row["longitude"])
            for point in cell_sample_points(latitude, longitude, resolution_deg):
                name = tile_name(*point)
                if name in available:
                    selected_names.add(name)
                    tiles_by_uf[uf].add(name)
                else:
                    missing_names.add(name)

    archives = [available[name] for name in sorted(selected_names)]
    result = {
        "schema_version": 1,
        "grid_file": str(grid),
        "grid_sha256": sha256_file(grid),
        "manifest_file": str(manifest),
        "manifest_sha256": sha256_file(manifest),
        "resolution_deg": resolution_deg,
        "uncovered_cell_count": uncovered_cell_count,
        "uncovered_cells_by_uf": dict(sorted(uncovered_by_uf.items())),
        "selected_archive_count": len(archives),
        "selected_listed_size_bytes": sum(item["listed_size_bytes"] for item in archives),
        "selected_archives_by_uf": {uf: len(names) for uf, names in sorted(tiles_by_uf.items())},
        "missing_archive_names": sorted(missing_names),
        "archives": archives,
        "selection_semantics": (
            "TOPODATA archives intersecting uncovered 0.25-degree continental grid cells; "
            "selection does not establish terrain suitability, viewshed, or RF coverage"
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(prefix=f".{output.name}.", dir=output.parent, delete=False) as temporary:
        temporary.write(payload)
        temporary_path = Path(temporary.name)
    os.replace(temporary_path, output)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resolution-deg", type=float, default=0.25)
    args = parser.parse_args()
    print(json.dumps(select(args.grid, args.manifest, args.output, args.resolution_deg), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
