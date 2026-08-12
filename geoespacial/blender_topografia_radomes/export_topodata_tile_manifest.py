"""Indexa folhas TOPODATA em blocos de 30 m que cabem no Blender.

O manifesto contém somente metadados e janelas. As cotas são lidas sob demanda
por ``export_topodata_tile_window.py``; portanto, não há mosaico nacional em RAM.
"""
import argparse
import json
from pathlib import Path

from osgeo import gdal

from topodata_tile_plan import windows

gdal.PushErrorHandler("CPLQuietErrorHandler")


def build(terrain_root, output, cells=720):
    if cells < 2:
        raise ValueError("--cells deve ser pelo menos 2")
    tiles = []
    for path in sorted(terrain_root.glob("*.tif")):
        dataset = gdal.Open(str(path))
        if dataset is None:
            continue
        transform = dataset.GetGeoTransform()
        for column, row, width, height in windows(dataset.RasterXSize, dataset.RasterYSize, cells):
            tiles.append({
                "source": str(path.resolve()), "source_name": path.name,
                "column": column, "row": row, "width": width, "height": height,
                "cells": [width - 1, height - 1],
                "origin_wgs84": [transform[0] + column * transform[1], transform[3] + row * transform[5]],
                "sample_spacing_arc_seconds": [abs(transform[1]) * 3600, abs(transform[5]) * 3600],
            })
    result = {
        "schema_version": 1, "tile_cells": cells, "tiles": tiles,
        "semantics": (
            "Plano de blocos TOPODATA de resolução nativa (~30 m). Blocos vizinhos compartilham uma borda; "
            "cada bloco é carregado e descartado individualmente pelo renderizador, sem montar uma malha nacional."
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--terrain-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cells", type=int, default=720, help="Quadrículas por lado do bloco")
    arguments = parser.parse_args()
    build(arguments.terrain_root, arguments.output, arguments.cells)
