#!/usr/bin/env python3
"""Extrai ZIP para diretório novo, bloqueando caminhos inseguros e sobrescrita."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZipFile


def safe_destination(root: Path, member: str) -> Path:
    destination = (root / member).resolve()
    if root.resolve() not in destination.parents and destination != root.resolve():
        raise ValueError(f"membro ZIP inseguro: {member}")
    return destination


def extract(archive_path: Path, output_dir: Path) -> list[dict]:
    output_dir.mkdir(parents=True, exist_ok=True)
    extracted = []
    with ZipFile(archive_path) as archive:
        for info in archive.infolist():
            destination = safe_destination(output_dir, info.filename)
            if destination.exists() and not destination.is_dir():
                raise FileExistsError(f"destino já existe: {destination}")
            if info.is_dir():
                destination.mkdir(parents=True, exist_ok=True)
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as source, destination.open("xb") as target:
                while block := source.read(1024 * 1024):
                    target.write(block)
            extracted.append({"member": info.filename, "target": str(destination), "size_bytes": info.file_size})
    return extracted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    result = {"archive": str(args.archive), "files": extract(args.archive, args.output_dir)}
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"files": len(result["files"])}, indent=2))


if __name__ == "__main__":
    main()
