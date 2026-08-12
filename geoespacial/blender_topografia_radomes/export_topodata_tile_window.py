"""Materializa sob demanda um único bloco do manifesto TOPODATA."""
import argparse
import json
from pathlib import Path

from osgeo import gdal

from terrain_mesh_geometry import vertices_from_window

gdal.PushErrorHandler("CPLQuietErrorHandler")


def build(manifest, tile_index, output):
    plan = json.loads(manifest.read_text(encoding="utf-8"))
    try:
        tile = plan["tiles"][tile_index]
    except IndexError as error:
        raise ValueError(f"Índice de bloco inexistente: {tile_index}; total {len(plan['tiles'])}") from error
    dataset = gdal.Open(tile["source"])
    if dataset is None:
        raise ValueError(f"Folha TOPODATA indisponível: {tile['source']}")
    values = dataset.GetRasterBand(1).ReadAsArray(tile["column"], tile["row"], tile["width"], tile["height"])
    vertices, width, height = vertices_from_window(values, dataset.GetGeoTransform(), tile["column"], tile["row"], 1)
    center = vertices[(height // 2) * width + width // 2]
    site = {
        "name": f"{tile['source_name']}_{tile['row']}_{tile['column']}",
        "display_name": f"{tile['source_name']} | bloco {tile_index}",
        "longitude": center[0], "latitude": center[1], "tile": tile["source_name"],
        "width": width, "height": height, "vertices": vertices,
        "sample_spacing_arc_seconds": tile["sample_spacing_arc_seconds"][0],
        "semantics": "Cada vértice é uma cota TOPODATA nativa; este bloco é uma parte sobreposta de uma folha.",
    }
    result = {"schema_version": 1, "tile_index": tile_index, "tile": tile, "sites": [site], "semantics": plan["semantics"]}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--tile-index", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    build(arguments.manifest, arguments.tile_index, arguments.output)
