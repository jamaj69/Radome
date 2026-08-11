#!/usr/bin/env python3
"""Adquire um arquivo HTTP de forma atômica, verifica hash e grava recibo."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def acquire(url: str, target: Path, expected_sha256: str | None = None) -> dict:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=f".{target.name}.", delete=False) as temporary:
        temporary_path = Path(temporary.name)
        try:
            with urllib.request.urlopen(url, timeout=300) as response:
                while block := response.read(1024 * 1024):
                    temporary.write(block)
            temporary.flush()
            digest = file_sha256(temporary_path)
            if expected_sha256 and digest.lower() != expected_sha256.lower():
                raise ValueError(f"SHA-256 divergente: esperado {expected_sha256}, obtido {digest}")
            temporary_path.replace(target)
        except BaseException:
            temporary_path.unlink(missing_ok=True)
            raise
    return {
        "url": url, "target": str(target), "size_bytes": target.stat().st_size,
        "sha256": digest, "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = acquire(args.url, args.target, args.expected_sha256)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
