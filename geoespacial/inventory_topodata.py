#!/usr/bin/env python3
"""Inventory TOPODATA numeric-altitude GeoTIFF archives from the official index."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

INDEX_URL = "https://www.dsr.inpe.br/topodata/data/geotiff/"
ROW = re.compile(
    r'href="(?P<name>[^"]+ZN\.zip)".*?'
    r'<td align="right">\s*(?P<size>[0-9.]+)(?P<unit>[KMG])</td>',
    re.IGNORECASE,
)
MULTIPLIER = {"K": 1024, "M": 1024**2, "G": 1024**3}


def parse_index(html: str) -> list[dict[str, object]]:
    archives: dict[str, dict[str, object]] = {}
    for match in ROW.finditer(html):
        name = match.group("name")
        size = int(float(match.group("size")) * MULTIPLIER[match.group("unit").upper()])
        archives[name] = {"name": name, "url": INDEX_URL + name, "listed_size_bytes": size}
    if not archives:
        raise ValueError("no TOPODATA altitude archives found in remote index")
    return [archives[name] for name in sorted(archives)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with urllib.request.urlopen(INDEX_URL, timeout=120) as response:
        html = response.read().decode("utf-8", errors="replace")
    archives = parse_index(html)
    payload = {
        "schema_version": 1,
        "source": INDEX_URL,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "product_suffix": "ZN",
        "product": "numeric altitude GeoTIFF archive",
        "archive_count": len(archives),
        "listed_total_size_bytes": sum(item["listed_size_bytes"] for item in archives),
        "archives": archives,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
