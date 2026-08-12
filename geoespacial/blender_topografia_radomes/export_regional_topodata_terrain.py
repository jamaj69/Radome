"""Mosaica amostras TOPODATA para uma superfície regional Blender.

Não produz uma malha nacional de 30 m. A saída usa uma grade explicitamente
reduzida, suficiente para enquadrar os três marcadores em uma única cena.
"""
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from osgeo import gdal

from regional_terrain_geometry import grid_shape, regional_bounds

gdal.PushErrorHandler("CPLQuietErrorHandler")


def tile_catalog(root):
    """Abre uma vez as folhas e registra suas extensões geográficas."""
    catalog = []
    for path in sorted(root.glob("*.tif")):
        dataset = gdal.Open(str(path))
        if dataset is None:
            continue
        transform = dataset.GetGeoTransform()
        west, north = transform[0], transform[3]
        east = west + dataset.RasterXSize * transform[1]
        south = north + dataset.RasterYSize * transform[5]
        catalog.append((path, dataset, min(west, east), min(south, north), max(west, east), max(south, north)))
    return catalog


def covering_tile(catalog, longitude, latitude):
    for item in catalog:
        _, _, west, south, east, north = item
        if west <= longitude <= east and south <= latitude <= north:
            return item
    return None


def sample_grid(catalog, longitudes, latitudes, allow_gaps=False):
    """Lê blocos por folha, evitando uma chamada GDAL por vértice."""
    groups = defaultdict(list)
    for row, latitude in enumerate(latitudes):
        for column, longitude in enumerate(longitudes):
            item = covering_tile(catalog, longitude, latitude)
            if item is None:
                if allow_gaps:
                    continue
                raise ValueError(f"TOPODATA não cobre {longitude:.5f}, {latitude:.5f}")
            groups[item[0]].append((row, column, item))

    elevations = [[None for _ in longitudes] for _ in latitudes]
    for records in groups.values():
        _, dataset, *_ = records[0][2]
        transform = dataset.GetGeoTransform()
        samples = []
        for row, column, _ in records:
            pixel_column = min(dataset.RasterXSize - 1, max(0, int((longitudes[column] - transform[0]) / transform[1])))
            pixel_row = min(dataset.RasterYSize - 1, max(0, int((latitudes[row] - transform[3]) / transform[5])))
            samples.append((row, column, pixel_row, pixel_column))
        first_row, last_row = min(item[2] for item in samples), max(item[2] for item in samples)
        first_column, last_column = min(item[3] for item in samples), max(item[3] for item in samples)
        values = dataset.GetRasterBand(1).ReadAsArray(
            first_column, first_row, last_column - first_column + 1, last_row - first_row + 1
        )
        no_data = dataset.GetRasterBand(1).GetNoDataValue()
        for row, column, pixel_row, pixel_column in samples:
            value = float(values[pixel_row - first_row, pixel_column - first_column])
            if not math.isfinite(value) or (no_data is not None and value == no_data):
                raise ValueError(f"Cota TOPODATA inválida em {longitudes[column]:.5f}, {latitudes[row]:.5f}")
            elevations[row][column] = value
    return elevations


def build(selection, terrain_root, output, spacing_degrees=.02, margin_degrees=.25, allow_gaps=False):
    selected = json.loads(selection.read_text(encoding="utf-8"))["selected_sites"]
    bounds = regional_bounds(selected, margin_degrees)
    longitudes, latitudes = grid_shape(bounds, spacing_degrees)
    catalog = tile_catalog(terrain_root)
    if not catalog:
        raise ValueError(f"Nenhuma folha GeoTIFF em {terrain_root}")
    elevations = sample_grid(catalog, longitudes, latitudes, allow_gaps)
    missing_samples = sum(value is None for row in elevations for value in row)
    result = {
        "schema_version": 1,
        "sites": selected,
        "bbox_wgs84": list(bounds),
        "longitude_samples": longitudes,
        "latitude_samples": latitudes,
        "elevations_m": elevations,
        "sample_spacing_degrees": spacing_degrees,
        "missing_sample_count": missing_samples,
        "semantics": (
            "Superfície regional TOPODATA subamostrada para visualização: cada vértice preserva a cota da amostra "
            "TOPODATA mais próxima; ela não substitui as malhas locais de 30 m. Exageração vertical é apenas visual."
        ),
    }
    # A proveniência é obtida de forma determinística pela extensão usada, sem
    # serializar objetos GDAL no artefato JSON.
    result["source_tiles"] = sorted({item[0].name for item in catalog if item[4] >= bounds[0] and item[2] <= bounds[2] and item[5] >= bounds[1] and item[3] <= bounds[3]})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--terrain-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--spacing-degrees", type=float, default=.02)
    parser.add_argument("--margin-degrees", type=float, default=.25)
    parser.add_argument("--allow-gaps", action="store_true", help="Registra lacunas como faces ausentes, sem interpolar cotas")
    arguments = parser.parse_args()
    build(arguments.selection, arguments.terrain_root, arguments.output, arguments.spacing_degrees, arguments.margin_degrees, arguments.allow_gaps)
