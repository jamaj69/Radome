#!/usr/bin/env python3
"""Extrai atomicamente os GeoTIFFs TOPODATA e cria um indice espacial auditavel."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as stream:
        stream.write(payload)
        temporary = Path(stream.name)
    os.replace(temporary, path)


def inspect_geotiff(path: Path) -> dict:
    with Image.open(path) as image:
        if image.format != "TIFF":
            raise ValueError("membro extraido nao e TIFF")
        scale = image.tag_v2.get(33550)
        tiepoint = image.tag_v2.get(33922)
        if not scale or len(scale) < 2 or not tiepoint or len(tiepoint) < 6:
            raise ValueError("GeoTIFF sem PixelScale ou Tiepoint")
        width, height = image.size
        pixel_x, pixel_y = float(scale[0]), float(scale[1])
        west, north = float(tiepoint[3]), float(tiepoint[4])
        east, south = west + width * pixel_x, north - height * pixel_y
        sample = image.getpixel((width // 2, height // 2))
    return {
        "width": width,
        "height": height,
        "pixel_size_x_degrees": pixel_x,
        "pixel_size_y_degrees": pixel_y,
        "bbox_wgs84": [west, south, east, north],
        "center_sample_m": float(sample),
    }


def extract_archive(archive_path: Path, target_dir: Path) -> dict:
    with zipfile.ZipFile(archive_path) as archive:
        members = [item for item in archive.infolist() if not item.is_dir() and item.filename.lower().endswith((".tif", ".tiff"))]
        if len(members) != 1:
            raise ValueError(f"esperado exatamente um GeoTIFF, encontrados {len(members)}")
        member = members[0]
        member_name = Path(member.filename).name
        if member_name != member.filename:
            raise ValueError("caminho interno inesperado no ZIP")
        target = target_dir / member_name
        if target.exists():
            metadata = inspect_geotiff(target)
            return {"status": "reused", "geotiff": target.name, "geotiff_size_bytes": target.stat().st_size, "geotiff_sha256": sha256_file(target), **metadata}

        target_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=target_dir, prefix=f".{member_name}.", suffix=".part", delete=False) as output:
            temporary = Path(output.name)
            try:
                with archive.open(member) as source:
                    shutil.copyfileobj(source, output, length=1024 * 1024)
                output.flush()
                metadata = inspect_geotiff(temporary)
                digest = sha256_file(temporary)
                size = temporary.stat().st_size
                os.replace(temporary, target)
            except BaseException:
                temporary.unlink(missing_ok=True)
                raise
    return {"status": "extracted", "geotiff": target.name, "geotiff_size_bytes": size, "geotiff_sha256": digest, **metadata}


def feature(item: dict) -> dict:
    west, south, east, north = item["bbox_wgs84"]
    return {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [[[west, south], [east, south], [east, north], [west, north], [west, south]]]},
        "properties": {key: value for key, value in item.items() if key != "bbox_wgs84"},
    }


def extract_receipt(receipt_path: Path, archive_dir: Path, target_dir: Path, report_path: Path, index_path: Path) -> dict:
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    results: list[dict] = []
    for source in receipt["archives"]:
        item = {"archive": source["name"], "archive_sha256": source["sha256"]}
        archive_path = archive_dir / source["name"]
        try:
            if sha256_file(archive_path) != source["sha256"]:
                raise ValueError("SHA-256 do ZIP diverge do recibo de aquisicao")
            item.update(extract_archive(archive_path, target_dir))
        except Exception as error:
            item.update(status="failed", error=f"{type(error).__name__}: {error}")
        results.append(item)

    completed = sum(item["status"] in {"extracted", "reused"} for item in results)
    failed = len(results) - completed
    report = {
        "schema_version": 1,
        "acquisition_receipt": str(receipt_path),
        "acquisition_receipt_sha256": sha256_file(receipt_path),
        "requested_archive_count": len(results),
        "completed_archive_count": completed,
        "failed_archive_count": failed,
        "complete": failed == 0,
        "geotiff_size_bytes": sum(item.get("geotiff_size_bytes", 0) for item in results),
        "missing_archive_names_from_selection": receipt.get("missing_archive_names_from_selection", []),
        "crs": "EPSG:4326",
        "pixel_interpretation": "PixelIsArea",
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        "tiles": results,
    }
    atomic_json(report_path, report)
    index = {"type": "FeatureCollection", "name": "topodata_radio_link_tiles", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": [feature(item) for item in results if item["status"] in {"extracted", "reused"}]}
    atomic_json(index_path, index)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--archive-dir", type=Path, required=True)
    parser.add_argument("--target-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    args = parser.parse_args()
    result = extract_receipt(args.receipt, args.archive_dir, args.target_dir, args.report, args.index)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["complete"] else 1)


if __name__ == "__main__":
    main()
