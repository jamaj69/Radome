#!/usr/bin/env /home/python/pyenv/bin/python
"""Seleciona folhas TOPODATA necessárias aos anéis multiescala das sementes."""

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
from consolidate_topodata_gap_candidates import RADII_KM, destination
from select_topodata_route_tiles import tile_name


def requirements(
    seeds: Path, azimuth_count: int = 36
) -> tuple[int, Counter[str], dict[str, set[str]]]:
    if azimuth_count < 8:
        raise ValueError("azimuth_count deve ser >= 8")
    point_counts: Counter[str] = Counter()
    seed_ids: defaultdict[str, set[str]] = defaultdict(set)
    seed_count = 0
    with gzip.open(seeds, "rt", encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            seed_count += 1
            seed_id = row.get("seed_id") or f"seed:{seed_count}"
            latitude, longitude = float(row["latitude"]), float(row["longitude"])
            centre_name = tile_name(latitude, longitude)
            point_counts[centre_name] += 1
            seed_ids[centre_name].add(seed_id)
            for radius in RADII_KM:
                for index in range(azimuth_count):
                    name = tile_name(
                        *destination(
                            latitude,
                            longitude,
                            radius,
                            index * 360.0 / azimuth_count,
                        )
                    )
                    point_counts[name] += 1
                    seed_ids[name].add(seed_id)
    return seed_count, point_counts, dict(seed_ids)


def required_names(seeds: Path, azimuth_count: int = 36) -> tuple[int, set[str]]:
    seed_count, point_counts, _ = requirements(seeds, azimuth_count)
    return seed_count, set(point_counts)


def select(seeds: Path, manifest: Path, existing_dir: Path, output: Path, azimuth_count: int = 36) -> dict:
    inventory = json.loads(manifest.read_text(encoding="utf-8"))
    available = {item["name"]: item for item in inventory["archives"]}
    seed_count, point_counts, seed_ids = requirements(seeds, azimuth_count)
    names = set(point_counts)
    missing_official = sorted(names - available.keys())
    selected_names = sorted(names & available.keys())
    existing_names = {path.name for path in existing_dir.glob("*.zip") if path.is_file()}
    new_names = sorted(set(selected_names) - existing_names)
    archives = [available[name] for name in selected_names]
    result = {
        "schema_version": 1, "seeds_file": str(seeds), "seeds_sha256": sha256_file(seeds),
        "manifest_file": str(manifest), "manifest_sha256": sha256_file(manifest),
        "existing_directory": str(existing_dir), "seed_count": seed_count,
        "ring_radii_km": list(RADII_KM), "azimuth_count": azimuth_count,
        "evaluated_point_count": seed_count * (1 + len(RADII_KM) * azimuth_count),
        "selected_archive_count": len(archives),
        "selected_listed_size_bytes": sum(item["listed_size_bytes"] for item in archives),
        "already_local_archive_count": len(set(selected_names) & existing_names),
        "new_archive_count": len(new_names),
        "new_listed_size_bytes": sum(available[name]["listed_size_bytes"] for name in new_names),
        "new_archive_names": new_names, "missing_archive_names": missing_official,
        "missing_archive_details": [
            {
                "name": name,
                "evaluated_point_count": point_counts[name],
                "affected_seed_count": len(seed_ids[name]),
                "affected_seed_ids": sorted(seed_ids[name]),
            }
            for name in missing_official
        ],
        "archives": archives,
        "selection_semantics": (
            "TOPODATA archives containing seed centres and 36 geodesic samples at 5, 10 and 25 km; "
            "selection only completes terrain sampling and makes no site, visibility or RF claim"
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(prefix=f".{output.name}.", dir=output.parent, delete=False) as target:
        target.write(payload)
        temporary = Path(target.name)
    os.replace(temporary, output)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--existing-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--azimuth-count", type=int, default=36)
    args = parser.parse_args()
    print(json.dumps(select(args.seeds, args.manifest, args.existing_dir, args.output, args.azimuth_count), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
