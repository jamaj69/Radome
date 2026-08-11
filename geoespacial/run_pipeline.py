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
    if not bc250.is_file():
        raise SystemExit(f"BC250 ausente: {bc250}; consulte data/manifests/sources.json")
    if not args.skip_tests:
        run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], root)
    # O Python do sistema fornece GDAL/OGR e as demais dependências GIS locais.
    run([str(SYSTEM_PYTHON), "preselect_bc250.py", str(bc250), "--output-dir", "reports/preselection_bc250"], root)
    run([
        str(SYSTEM_PYTHON), "build_candidate_graph.py", str(bc250),
        "--terrain-cache", "data/raw/mapzen/terrarium",
        "--output-dir", "reports/candidate_graph",
    ], root)
    print("Pipeline geoespacial preliminar concluído.")


if __name__ == "__main__":
    main()
