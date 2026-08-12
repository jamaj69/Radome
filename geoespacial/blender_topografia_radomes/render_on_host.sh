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
terrain_root="geoespacial/data/processed/topodata/radio_link_routes"
hillshade_raw="geoespacial/data/raw/topodata/hillshade"
hillshade_processed="geoespacial/data/processed/topodata/hillshade"

command -v blender >/dev/null || { echo "Blender não encontrado no PATH." >&2; exit 1; }
"$system_python" -c "import osgeo" || { echo "GDAL/OSGeo não disponível em $system_python." >&2; exit 1; }

if command -v nvidia-smi >/dev/null; then
    echo "GPU disponível no host:"
    if nvidia-smi --query-gpu=name,driver_version --format=csv,noheader; then
        # Eevee usa o contexto OpenGL/EGL. Estas variáveis selecionam explicitamente
        # a implementação NVIDIA em hosts híbridos ou com múltiplas GPUs.
        export __NV_PRIME_RENDER_OFFLOAD=1
        export __GLX_VENDOR_LIBRARY_NAME=nvidia
        export DRI_PRIME=1
    else
        echo "GPU não acessível neste processo; continuando com o Blender." >&2
    fi
fi

"$python_bin" "$subproject/select_visual_sites.py" \
    --ranking geoespacial/outputs/candidate_ranking/candidate_ranking.csv.gz \
    --output "$build/selected_sites.json"

"$system_python" "$subproject/export_geographic_overlays.py" \
    --bc250 geoespacial/data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
    --ranking geoespacial/outputs/candidate_ranking/candidate_ranking.csv.gz \
    --output "$build/overlays.json"

if [[ "${1:-}" == "--regional-terrain" ]]; then
    "$system_python" "$subproject/export_regional_topodata_terrain.py" \
        --selection "$build/selected_sites.json" --terrain-root "$terrain_root" \
        --output "$build/topodata_regional_terrain.json" --spacing-degrees "${2:-0.02}" --margin-degrees "${3:-0.25}" --allow-gaps
    "$system_python" "$subproject/export_regional_boundaries.py" \
        --bc250 geoespacial/data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
        --terrain "$build/topodata_regional_terrain.json" --output "$build/topodata_regional_boundaries.json"
    exec blender -b --python "$subproject/render_topodata_regional_batched.py" -- \
        --terrain "$build/topodata_regional_terrain.json" --boundaries "$build/topodata_regional_boundaries.json" \
        --blend "$build/topodata_regional_radomes.blend" --render "$build/topodata_regional_radomes.png" \
        --vertical-exaggeration 1.5 --samples 128
fi

if [[ "${1:-}" == "--topodata-tile" ]]; then
    "$system_python" "$subproject/export_topodata_tile_manifest.py" \
        --terrain-root "$terrain_root" --output "$build/topodata_tile_manifest.json" --cells "${2:-720}"
    "$system_python" "$subproject/export_topodata_tile_window.py" \
        --manifest "$build/topodata_tile_manifest.json" --tile-index "${3:-0}" \
        --output "$build/topodata_tile_window.json"
    exec blender -b --python "$subproject/render_topodata_local_terrain_batched.py" -- \
        --terrain "$build/topodata_tile_window.json" \
        --blend "$build/topodata_tile_${3:-0}.blend" \
        --render "$build/topodata_tile_${3:-0}.png" \
        --site-index 0 --vertical-exaggeration 1.5 --samples 128 --top-down
fi

if [[ "${1:-}" == "--topodata-tile-range" ]]; then
    cells="${2:-720}"
    first="${3:-0}"
    count="${4:?Informe a quantidade finita de blocos a renderizar.}"
    "$system_python" "$subproject/export_topodata_tile_manifest.py" \
        --terrain-root "$terrain_root" --output "$build/topodata_tile_manifest.json" --cells "$cells"
    last=$((first + count - 1))
    for index in $(seq "$first" "$last"); do
        "$system_python" "$subproject/export_topodata_tile_window.py" \
            --manifest "$build/topodata_tile_manifest.json" --tile-index "$index" \
            --output "$build/topodata_tile_window.json"
        blender -b --python "$subproject/render_topodata_local_terrain_batched.py" -- \
            --terrain "$build/topodata_tile_window.json" \
            --blend "$build/topodata_tile_${index}.blend" \
            --render "$build/topodata_tile_${index}.png" \
            --site-index 0 --vertical-exaggeration 1.5 --samples 128 --top-down
    done
    exit 0
fi

"$system_python" "$subproject/export_topodata_terrain_mesh.py" \
    --selection "$build/selected_sites.json" \
    --terrain-root "$terrain_root" \
    --output "$build/topodata_terrain.json" --size 721

"$system_python" "$subproject/export_local_boundaries.py" \
    --bc250 geoespacial/data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
    --terrain "$build/topodata_terrain.json" --output "$build/topodata_local_boundaries.json"

if [[ "${1:-}" == "--topodata-rs" || "${1:-}" == "--topodata-rs-batched" ]]; then
    "$python_bin" "$subproject/acquire_topodata_hillshade.py" \
        --selection "$build/selected_sites.json" --terrain "$build/topodata_terrain.json" \
        --output-dir "$hillshade_raw" --receipt "$build/topodata_hillshade_receipt.json"
    "$python_bin" geoespacial/extract_topodata_route_tiles.py \
        --receipt "$build/topodata_hillshade_receipt.json" --archive-dir "$hillshade_raw" \
        --target-dir "$hillshade_processed" --report "$build/topodata_hillshade_extraction.json" \
        --index "$build/topodata_hillshade_index.geojson" --index-name topodata_hillshade
    "$system_python" "$subproject/export_topodata_terrain_mesh.py" \
        --selection "$build/selected_sites.json" --terrain-root "$terrain_root" \
        --output "$build/topodata_terrain.json" --size 721 --shade-root "$hillshade_processed" \
        --shade-output-dir "$build/topodata_hillshade_windows"
    "$system_python" "$subproject/export_local_boundaries.py" \
        --bc250 geoespacial/data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
        --terrain "$build/topodata_terrain.json" --output "$build/topodata_local_boundaries.json"
    renderer="$subproject/render_topodata_local_terrain.py"
    blend="$build/topodata_rs_terrain.blend"
    image="$build/topodata_rs_terrain.png"
    if [[ "${1:-}" == "--topodata-rs-batched" ]]; then
        renderer="$subproject/render_topodata_local_terrain_batched.py"
        blend="$build/topodata_rs_batched.blend"
        image="$build/topodata_rs_batched.png"
    fi
    exec blender -b --python "$renderer" -- \
        --terrain "$build/topodata_terrain.json" --blend "$blend" \
        --render "$image" --site-index "${2:-0}" \
        --vertical-exaggeration 1.5 --samples 128 --top-down --boundaries "$build/topodata_local_boundaries.json"
fi

if [[ "${1:-}" == "--local-terrain" ]]; then
    exec blender -b --python "$subproject/render_topodata_local_terrain.py" -- \
        --terrain "$build/topodata_terrain.json" \
        --blend "$build/topodata_local_terrain.blend" \
        --render "$build/topodata_local_terrain.png" \
        --site-index "${2:-0}" \
        --vertical-exaggeration 1.5 \
        --samples 128 --boundaries "$build/topodata_local_boundaries.json"
fi

if [[ "${1:-}" == "--top-down" ]]; then
    exec blender -b --python "$subproject/render_topodata_local_terrain.py" -- \
        --terrain "$build/topodata_terrain.json" \
        --blend "$build/topodata_top_down.blend" \
        --render "$build/topodata_top_down.png" \
        --site-index "${2:-0}" \
        --vertical-exaggeration 1.5 \
        --samples 128 \
        --top-down \
        --boundaries "$build/topodata_local_boundaries.json" \
        --orthophoto "${3:-$subproject/assets/nasa_blue_marble_topography_bathymetry_april_5400x2700.jpg}"
fi

exec blender -b --python "$subproject/render_curved_earth_radomes.py" -- \
    --selection "$build/selected_sites.json" \
    --overlays "$build/overlays.json" \
    --terrain "$build/topodata_terrain.json" \
    --texture "$subproject/assets/nasa_blue_marble_topography_bathymetry_april_5400x2700.jpg" \
    --blend "$build/earth_radomes.blend" \
    --render "$build/earth_radomes.png" \
    --overview
