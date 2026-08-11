#!/usr/bin/env python3
"""Orquestra o pipeline geoespacial preliminar usando somente pontos Python."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SYSTEM_PYTHON = Path("/usr/bin/python3")


def run(command: list[str], cwd: Path) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-tests", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    bc250 = root / "data/raw/ibge/bc250/bc250_2026-03-03.gpkg"
    smp = root / "data/raw/anatel/estacoes_smp.zip"
    anatel_general = root / "data/raw/anatel/estacoes_licenciadas.zip"
    if not bc250.is_file():
        raise SystemExit(f"BC250 ausente: {bc250}; consulte data/manifests/sources.json")
    if not smp.is_file():
        raise SystemExit(f"SMP ausente: {smp}; consulte data/manifests/sources.json")
    if not anatel_general.is_file():
        raise SystemExit(f"Pacote geral Anatel ausente: {anatel_general}; consulte data/manifests/sources.json")
    if not args.skip_tests:
        run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], root)
    # O Python do sistema fornece GDAL/OGR e as demais dependências GIS locais.
    run([str(SYSTEM_PYTHON), "preselect_bc250.py", str(bc250), "--output-dir", "reports/preselection_bc250"], root)
    run([
        str(SYSTEM_PYTHON), "build_candidate_graph.py", str(bc250),
        "--terrain-cache", "data/raw/mapzen/terrarium",
        "--output-dir", "reports/candidate_graph",
    ], root)
    run([
        sys.executable, "build_canonical_smp.py", "--smp", str(smp.relative_to(root)),
        "--output-dir", "outputs/canonical_smp",
        "--report", "reports/canonical_smp/summary.json",
    ], root)
    run([
        sys.executable, "audit_anatel_general.py", "--source",
        str(anatel_general.relative_to(root)),
        "--output-dir", "outputs/anatel_general_audit",
        "--report", "reports/anatel_general_audit/summary.json",
    ], root)
    run([
        sys.executable, "extract_anatel_radio_links.py",
        "--source", "outputs/anatel_general_audit/mosaico_stel.csv.gz",
        "--output", "outputs/anatel_radio_links/emissions.csv.gz",
        "--report", "reports/anatel_radio_links/summary.json",
    ], root)
    run([
        sys.executable, "build_canonical_fixed_emitters.py",
        "--sarc", "outputs/anatel_general_audit/sarc.csv.gz",
        "--fixed-broadband", "outputs/anatel_general_audit/fixed_broadband.csv.gz",
        "--output-dir", "outputs/canonical_fixed_emitters",
        "--report", "reports/canonical_fixed_emitters/summary.json",
    ], root)
    print("Pipeline geoespacial preliminar concluído.")


if __name__ == "__main__":
    main()
