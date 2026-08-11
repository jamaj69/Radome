#!/usr/bin/env python3
"""Baixa camadas WFS DECEA de modo atômico e grava manifesto com hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


WFS_URL = "https://geoaisweb.decea.mil.br/geoserver/wfs"


def request_url(request: str, **parameters: str) -> str:
    query = {"service": "WFS", "version": "2.0.0", "request": request, **parameters}
    return f"{WFS_URL}?{urllib.parse.urlencode(query)}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download_atomic(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=f".{target.name}.", delete=False) as temporary:
        temporary_path = Path(temporary.name)
        try:
            with urllib.request.urlopen(url, timeout=180) as response:
                while block := response.read(1024 * 1024):
                    temporary.write(block)
            temporary.flush()
            temporary_path.replace(target)
        except BaseException:
            temporary_path.unlink(missing_ok=True)
            raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("layers", nargs="+", help="nomes como ICA:vor")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    entries = []
    for qualified_name in args.layers:
        short_name = qualified_name.split(":", 1)[-1]
        data_target = args.output_dir / f"{short_name}.geojson"
        schema_target = args.output_dir / f"{short_name}.xsd"
        data_url = request_url("GetFeature", typeNames=qualified_name, outputFormat="application/json")
        schema_url = request_url("DescribeFeatureType", typeNames=qualified_name)
        download_atomic(data_url, data_target)
        download_atomic(schema_url, schema_target)
        data = json.loads(data_target.read_text(encoding="utf-8"))
        entries.append({
            "layer": qualified_name,
            "data_url": data_url,
            "schema_url": schema_url,
            "data_file": str(data_target),
            "schema_file": str(schema_target),
            "feature_count": len(data.get("features", [])),
            "data_sha256": sha256(data_target),
            "schema_sha256": sha256(schema_target),
        })
    result = {
        "schema_version": 1,
        "authority": "DECEA / ICA GEOAISWEB",
        "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
        "layers": entries,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({item["layer"]: item["feature_count"] for item in entries}, indent=2))


if __name__ == "__main__":
    main()
