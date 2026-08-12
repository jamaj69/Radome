"""Recorta divisas municipais e estaduais do BC250 para cada janela TOPODATA."""
import argparse
import json
from pathlib import Path

def line_parts(geometry, stride=3):
    from osgeo import ogr
    if geometry is None or geometry.IsEmpty():
        return []
    flat = ogr.GT_Flatten(geometry.GetGeometryType())
    if flat == ogr.wkbLineString:
        points = [geometry.GetPoint(index)[:2] for index in range(0, geometry.GetPointCount(), stride)]
        last = geometry.GetPoint(geometry.GetPointCount() - 1)[:2]
        if points and points[-1] != last:
            points.append(last)
        return [points] if len(points) > 1 else []
    return [part for index in range(geometry.GetGeometryCount()) for part in line_parts(geometry.GetGeometryRef(index), stride)]


def boundary_parts(layer, west, south, east, north, stride):
    from osgeo import ogr
    layer.SetSpatialFilterRect(west, south, east, north)
    window = ogr.CreateGeometryFromWkt(
        f"POLYGON (({west} {south}, {east} {south}, {east} {north}, {west} {north}, {west} {south}))"
    )
    parts = []
    for feature in layer:
        boundary = feature.GetGeometryRef().Boundary()
        clipped = boundary.Intersection(window)
        parts.extend(line_parts(clipped, stride))
    layer.SetSpatialFilter(None)
    return parts


def bounds(site):
    longitudes = [vertex[0] for vertex in site["vertices"]]
    latitudes = [vertex[1] for vertex in site["vertices"]]
    return min(longitudes), min(latitudes), max(longitudes), max(latitudes)


def build(bc250, terrain, output):
    from osgeo import ogr
    source = ogr.Open(str(bc250))
    municipalities = source.GetLayerByName("lml_municipio_a")
    states = source.GetLayerByName("lml_unidade_federacao_a")
    if municipalities is None or states is None:
        raise ValueError("BC250 sem limites municipais ou estaduais")
    sites = []
    for site in json.loads(terrain.read_text(encoding="utf-8"))["sites"]:
        west, south, east, north = bounds(site)
        sites.append({
            "display_name": site["display_name"], "bbox_wgs84": [west, south, east, north],
            "municipal_boundaries": boundary_parts(municipalities, west, south, east, north, 3),
            "state_boundaries": boundary_parts(states, west, south, east, north, 2),
        })
    result = {
        "schema_version": 1, "sites": sites,
        "semantics": "Limites municipais e estaduais do IBGE BC250, recortados na janela TOPODATA local; linhas são cartográficas e não ajustam a altitude.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bc250", type=Path, required=True)
    parser.add_argument("--terrain", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    build(arguments.bc250, arguments.terrain, arguments.output)
