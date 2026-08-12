"""Geometria pura para a exportação e a inspeção de malhas TOPODATA."""
import math


def sampled_indices(size, step):
    return list(range(0, size, step))


def vertices_from_window(values, transform, first_column, first_row, step):
    """Converte cada amostra de uma janela DEM em [longitude, latitude, cota]."""
    rows, columns = values.shape
    vertices = []
    for row in sampled_indices(rows, step):
        for column in sampled_indices(columns, step):
            elevation = float(values[row, column])
            if not math.isfinite(elevation):
                raise ValueError("A janela TOPODATA contém uma cota não finita")
            longitude = transform[0] + (first_column + column + .5) * transform[1]
            latitude = transform[3] + (first_row + row + .5) * transform[5]
            vertices.append([longitude, latitude, elevation])
    return vertices, len(sampled_indices(columns, step)), len(sampled_indices(rows, step))


def local_coordinates(longitude, latitude, reference_longitude, reference_latitude):
    """Projeta uma pequena janela geográfica em metros locais (leste, norte)."""
    east = (longitude - reference_longitude) * 111_320 * math.cos(math.radians(reference_latitude))
    north = (latitude - reference_latitude) * 110_574
    return east, north


def terrain_geometry(site, vertical_exaggeration):
    """Gera vértices e quadriláteros, preservando cada cota DEM em Z."""
    reference = min(vertex[2] for vertex in site["vertices"])
    vertices = []
    for longitude, latitude, elevation in site["vertices"]:
        east, north = local_coordinates(longitude, latitude, site["longitude"], site["latitude"])
        vertices.append((east, north, (elevation - reference) * vertical_exaggeration))
    width, height = site["width"], site["height"]
    faces = []
    for row in range(height - 1):
        for column in range(width - 1):
            lower_left = row * width + column
            lower_right = lower_left + 1
            upper_left = (row + 1) * width + column
            upper_right = upper_left + 1
            faces.append((lower_left, lower_right, upper_right, upper_left))
    return vertices, faces, reference
