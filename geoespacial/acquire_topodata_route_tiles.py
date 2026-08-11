#!/usr/bin/env python3
"""Baixa e valida, de forma retomavel, as folhas TOPODATA selecionadas."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_archive(path: Path) -> list[str]:
    """Valida estrutura, CRC e presenca do GeoTIFF de altitude."""
    with zipfile.ZipFile(path) as archive:
        corrupt_member = archive.testzip()
        if corrupt_member:
            raise ValueError(f"CRC invalido no membro {corrupt_member}")
        members = archive.namelist()
    if not any(name.lower().endswith((".tif", ".tiff")) for name in members):
        raise ValueError("ZIP TOPODATA sem GeoTIFF")
    return members


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as stream:
        stream.write(payload)
        temporary = Path(stream.name)
    os.replace(temporary, path)


def acquire_archive(url: str, target: Path, timeout: int = 300) -> dict:
    """Reutiliza um ZIP valido ou o baixa para arquivo temporario atomico."""
    if target.exists():
        members = validate_archive(target)
        return {
            "status": "reused",
            "actual_size_bytes": target.stat().st_size,
            "sha256": sha256_file(target),
            "zip_member_count": len(members),
        }

    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=f".{target.name}.", suffix=".part", delete=False) as stream:
        temporary = Path(stream.name)
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "RADOME-geospatial-research/1.0"})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                while block := response.read(1024 * 1024):
                    stream.write(block)
            stream.flush()
            members = validate_archive(temporary)
            digest = sha256_file(temporary)
            size = temporary.stat().st_size
            os.replace(temporary, target)
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    return {"status": "downloaded", "actual_size_bytes": size, "sha256": digest, "zip_member_count": len(members)}


def acquire_selection(selection_path: Path, output_dir: Path, report_path: Path, limit: int | None = None) -> dict:
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    archives = selection["archives"]
    chosen = archives if limit is None else archives[:limit]
    results: list[dict] = []

    def report() -> dict:
        completed = sum(item["status"] in {"downloaded", "reused"} for item in results)
        failed = sum(item["status"] == "failed" for item in results)
        value = {
            "schema_version": 1,
            "selection_file": str(selection_path),
            "selection_sha256": sha256_file(selection_path),
            "output_directory": str(output_dir),
            "requested_archive_count": len(chosen),
            "selection_archive_count": len(archives),
            "completed_archive_count": completed,
            "failed_archive_count": failed,
            "pending_archive_count": len(chosen) - completed - failed,
            "complete": completed == len(chosen) and failed == 0,
            "actual_size_bytes": sum(item.get("actual_size_bytes", 0) for item in results),
            "missing_archive_names_from_selection": selection.get("missing_archive_names", []),
            "updated_at_utc": datetime.now(timezone.utc).isoformat(),
            "archives": results,
        }
        atomic_json(report_path, value)
        return value

    report()
    for archive in chosen:
        item = {"name": archive["name"], "url": archive["url"], "listed_size_bytes": archive.get("listed_size_bytes")}
        try:
            item.update(acquire_archive(archive["url"], output_dir / archive["name"]))
        except Exception as error:  # registra a falha e permite retomar o lote
            item.update(status="failed", error=f"{type(error).__name__}: {error}")
        results.append(item)
        report()
    return report()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    result = acquire_selection(args.selection, args.output_dir, args.report, args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["complete"] else 1)


if __name__ == "__main__":
    main()
