#!/usr/bin/env bash
# Renderiza a cena no host, onde o Blender pode acessar a GPU do usuário.
# Este wrapper apenas orquestra pontos de entrada Python versionados.
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$project_root"

python_bin="/home/python/pyenv/bin/python"
system_python="/usr/bin/python3"
subproject="geoespacial/blender_topografia_radomes"
build="$subproject/build"

command -v blender >/dev/null || { echo "Blender não encontrado no PATH." >&2; exit 1; }
"$system_python" -c "import osgeo" || { echo "GDAL/OSGeo não disponível em $system_python." >&2; exit 1; }

if command -v nvidia-smi >/dev/null; then
    echo "GPU disponível no host:"
    nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
fi

"$python_bin" "$subproject/select_visual_sites.py" \
    --ranking geoespacial/outputs/candidate_ranking/candidate_ranking.csv.gz \
    --output "$build/selected_sites.json"

"$system_python" "$subproject/export_geographic_overlays.py" \
    --bc250 geoespacial/data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
    --ranking geoespacial/outputs/candidate_ranking/candidate_ranking.csv.gz \
    --output "$build/overlays.json"

exec blender -b --python "$subproject/render_curved_earth_radomes.py" -- \
    --selection "$build/selected_sites.json" \
    --overlays "$build/overlays.json" \
    --terrain "$build/topodata_terrain.json" \
    --texture "$subproject/assets/nasa_blue_marble_topography_bathymetry_april_5400x2700.jpg" \
    --blend "$build/earth_radomes.blend" \
    --render "$build/earth_radomes.png" \
    --overview
