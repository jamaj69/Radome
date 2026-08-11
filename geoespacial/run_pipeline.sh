#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BC250="${SCRIPT_DIR}/data/raw/ibge/bc250/bc250_2026-03-03.gpkg"

if [[ ! -f "${BC250}" ]]; then
  echo "BC250 ausente: ${BC250}" >&2
  echo "Consulte data/manifests/sources.json para a URL e o SHA-256." >&2
  exit 2
fi

cd "${SCRIPT_DIR}"
/home/python/pyenv/bin/python -m unittest discover -s tests -v
/usr/bin/python3 preselect_bc250.py "${BC250}" --output-dir reports/preselection_bc250
/home/python/pyenv/bin/python build_candidate_graph.py "${BC250}" \
  --terrain-cache data/raw/mapzen/terrarium \
  --output-dir reports/candidate_graph

echo "Pipeline geoespacial preliminar concluído."
