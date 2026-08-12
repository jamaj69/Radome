"""Exporta grades TOPODATA para malhas Blender com uma cota por vértice."""
import argparse
import json
from pathlib import Path

from osgeo import gdal
from terrain_mesh_geometry import vertices_from_window

gdal.PushErrorHandler("CPLQuietErrorHandler")


def tile_for(root, longitude, latitude):
    """Abre a folha que contém a coordenada geográfica solicitada."""
    for path in sorted(root.glob("*.tif")):
        dataset = gdal.Open(str(path))
        transform = dataset.GetGeoTransform()
        west, north = transform[0], transform[3]
        east = west + dataset.RasterXSize * transform[1]
        south = north + dataset.RasterYSize * transform[5]
        if west <= longitude <= east and south <= latitude <= north:
            return dataset, path
    raise ValueError(f"Nenhuma folha TOPODATA cobre {longitude}, {latitude}")


def build(selection, terrain_root, output, size=241, step=1):
    if size < 3 or step < 1:
        raise ValueError("size deve ser pelo menos 3 e step deve ser positivo")
    sites = []
    for site in json.loads(selection.read_text(encoding="utf-8"))["selected_sites"]:
        dataset, path = tile_for(terrain_root, site["longitude"], site["latitude"])
        transform = dataset.GetGeoTransform()
        column = int((site["longitude"] - transform[0]) / transform[1])
        row = int((site["latitude"] - transform[3]) / transform[5])
        half = size // 2
        first_column, first_row = column - half, row - half
        if first_column < 0 or first_row < 0 or first_column + size > dataset.RasterXSize or first_row + size > dataset.RasterYSize:
            raise ValueError(f"Janela {size}x{size} excede os limites de {path.name}")
        values = dataset.GetRasterBand(1).ReadAsArray(first_column, first_row, size, size)
        vertices, width, height = vertices_from_window(values, transform, first_column, first_row, step)
        sites.append({
            "name": site["name"], "display_name": site["display_name"],
            "longitude": site["longitude"], "latitude": site["latitude"],
            "tile": path.name, "width": width, "height": height,
            "sample_spacing_arc_seconds": abs(transform[1]) * 3600 * step,
            "vertices": vertices,
        })
    result = {
        "schema_version": 2,
        "sites": sites,
        "semantics": "Cada vertice e uma amostra TOPODATA; as faces devem usar as cotas sem interpolacao vertical. A exageracao vertical, quando usada no Blender, e apenas visual.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--terrain-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--size", type=int, default=241, help="Lado da janela DEM em celulas")
    parser.add_argument("--step", type=int, default=1, help="Passo de amostragem em celulas")
    arguments = parser.parse_args()
    build(arguments.selection, arguments.terrain_root, arguments.output, arguments.size, arguments.step)
