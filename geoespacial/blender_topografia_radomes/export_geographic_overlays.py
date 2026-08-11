"""Exporta limites BC250 e amostras diagnósticas para a cena Blender."""
import argparse
import csv
import gzip
import json
from pathlib import Path

from osgeo import ogr


def line_parts(geometry, stride):
    """Extrai segmentos de LineString/MultiLineString, preservando só linhas."""
    if geometry is None or geometry.IsEmpty():
        return []
    flattened = ogr.GT_Flatten(geometry.GetGeometryType())
    if flattened == ogr.wkbLineString:
        points = [geometry.GetPoint(index)[:2] for index in range(0, geometry.GetPointCount(), stride)]
        if geometry.GetPointCount() > 1 and points[-1] != geometry.GetPoint(geometry.GetPointCount() - 1)[:2]:
            points.append(geometry.GetPoint(geometry.GetPointCount() - 1)[:2])
        return [points] if len(points) > 1 else []
    output = []
    for index in range(geometry.GetGeometryCount()):
        output.extend(line_parts(geometry.GetGeometryRef(index), stride))
    return output


def polygon_boundaries(layer, stride):
    output = []
    for feature in layer:
        output.extend(line_parts(feature.GetGeometryRef().Boundary(), stride))
    return output


def coordinate_key(point):
    return round(point[0], 7), round(point[1], 7)


def merge_line_parts(parts, stride):
    """Reconstrói longas fronteiras a partir dos microsegmentos da sobreposição."""
    endpoints = {}
    for index, part in enumerate(parts):
        endpoints.setdefault(coordinate_key(part[0]), []).append(index)
        endpoints.setdefault(coordinate_key(part[-1]), []).append(index)
    unused = set(range(len(parts)))
    output = []
    while unused:
        index = next(iter(unused))
        line = list(parts[index])
        unused.remove(index)
        while True:
            candidates = [candidate for candidate in endpoints[coordinate_key(line[-1])] if candidate in unused]
            if not candidates:
                break
            candidate = candidates[0]
            part = parts[candidate]
            if coordinate_key(part[-1]) == coordinate_key(line[-1]):
                part = list(reversed(part))
            line.extend(part[1:])
            unused.remove(candidate)
        reduced = line[::stride]
        if reduced[-1] != line[-1]:
            reduced.append(line[-1])
        if len(reduced) > 1:
            output.append(reduced)
    return output


def brazil_international_boundaries(country_layer, stride):
    countries = [(feature.GetField("nome"), feature.GetGeometryRef().Clone()) for feature in country_layer]
    brazil = next((geometry for name, geometry in countries if name == "Brasil"), None)
    if brazil is None:
        raise ValueError("feição Brasil ausente na camada lml_pais_a")
    boundary = brazil.Boundary()
    parts = []
    for name, geometry in countries:
        if name != "Brasil":
            parts.extend(line_parts(boundary.Intersection(geometry.Boundary()), 1))
    return merge_line_parts(parts, stride)


def build(bc250, ranking, output):
    source = ogr.Open(str(bc250))
    if source is None:
        raise ValueError(f"não foi possível abrir BC250: {bc250}")
    states = source.GetLayerByName("lml_unidade_federacao_a")
    countries = source.GetLayerByName("lml_pais_a")
    if states is None or countries is None:
        raise ValueError("camadas BC250 obrigatórias ausentes")
    with gzip.open(ranking, "rt", encoding="utf-8", newline="") as stream:
        points = [{"longitude": float(row["longitude"]), "latitude": float(row["latitude"]),
                   "elevation_m": float(row["terrain_elevation_m"])} for row in csv.DictReader(stream)]
    data = {
        "schema_version": 2,
        "state_boundaries": polygon_boundaries(states, 12),
        "international_boundaries": brazil_international_boundaries(countries, 8),
        "altitude_samples": points,
        "semantics": "BC250 state boundaries and Brazil terrestrial international borders; altitude points are diagnostic candidate elevations, not a national DEM or RF result",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bc250", type=Path, required=True)
    parser.add_argument("--ranking", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    build(arguments.bc250, arguments.ranking, arguments.output)
