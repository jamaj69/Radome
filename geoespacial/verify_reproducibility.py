#!/usr/bin/env python3
"""Executa o pipeline duas vezes e compara SHA-256 dos produtos declarados."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


PRODUCTS = (
    "reports/preselection_bc250/candidates.csv",
    "reports/preselection_bc250/candidates.geojson",
    "reports/candidate_graph/candidate_graph.graphml",
    "reports/candidate_graph/candidate_graph.png",
    "reports/candidate_graph/candidate_nodes.csv",
    "reports/candidate_graph/candidate_nodes.geojson",
    "reports/candidate_graph/summary.json",
    "outputs/canonical_smp/sites.csv.gz",
    "outputs/canonical_smp/antennas.csv.gz",
    "outputs/canonical_smp/emissions.csv.gz",
    "outputs/canonical_smp/summary.json",
    "reports/canonical_smp/summary.json",
    "outputs/anatel_general_audit/sarc.csv.gz",
    "outputs/anatel_general_audit/fixed_broadband.csv.gz",
    "outputs/anatel_general_audit/fixed_telephony.csv.gz",
    "outputs/anatel_general_audit/sle.csv.gz",
    "outputs/anatel_general_audit/summary.json",
    "reports/anatel_general_audit/summary.json",
    "outputs/canonical_fixed_emitters/sites.csv.gz",
    "outputs/canonical_fixed_emitters/antennas.csv.gz",
    "outputs/canonical_fixed_emitters/emissions.csv.gz",
    "outputs/canonical_fixed_emitters/summary.json",
    "reports/canonical_fixed_emitters/summary.json",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def snapshot(root: Path) -> dict[str, str]:
    missing = [relative for relative in PRODUCTS if not (root / relative).is_file()]
    if missing:
        raise FileNotFoundError(f"produtos ausentes: {', '.join(missing)}")
    return {relative: sha256(root / relative) for relative in PRODUCTS}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=Path("reports/reproducibility.json"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    command = [sys.executable, str(root / "run_pipeline.py"), "--skip-tests"]
    snapshots = []
    for _ in range(2):
        subprocess.run(command, cwd=root, check=True)
        snapshots.append(snapshot(root))
    differences = {
        relative: {"run_1": snapshots[0][relative], "run_2": snapshots[1][relative]}
        for relative in PRODUCTS if snapshots[0][relative] != snapshots[1][relative]
    }
    result = {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "pipeline_command": command,
        "product_count": len(PRODUCTS),
        "byte_reproducible": not differences,
        "hashes": snapshots[1],
        "differences": differences,
    }
    target = args.report if args.report.is_absolute() else root / args.report
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if differences:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
