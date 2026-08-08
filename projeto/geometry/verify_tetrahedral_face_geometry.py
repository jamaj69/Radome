#!/usr/bin/env python3
"""Verify an 80-face radome assembled from inward regular tetrahedra.

Each regular icosahedron macroface is subdivided in its own plane into four
equilateral receiver faces.  Unlike spherical projection, this construction
preserves a 2 m edge on every receiver face and therefore permits regular
2 m tetrahedral modules.
"""

from __future__ import annotations

import itertools
import math


FACE_EDGE_M = 2.0
MACRO_EDGE_M = 2.0 * FACE_EDGE_M
TOLERANCE_M = 1e-8


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def subtract(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(point, factor):
    return tuple(component * factor for component in point)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def length(vector):
    return math.sqrt(dot(vector, vector))


def normalize(vector):
    magnitude = length(vector)
    return scale(vector, 1.0 / magnitude)


def midpoint(a, b):
    return scale(add(a, b), 0.5)


def centroid(points):
    return scale(tuple(sum(point[axis] for point in points) for axis in range(3)), 1.0 / len(points))


def regular_icosahedron(edge_length):
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    vertices = [
        (0, 1, phi), (0, -1, phi), (0, 1, -phi), (0, -1, -phi),
        (1, phi, 0), (-1, phi, 0), (1, -phi, 0), (-1, -phi, 0),
        (phi, 0, 1), (-phi, 0, 1), (phi, 0, -1), (-phi, 0, -1),
    ]
    unit_edge = min(
        length(subtract(vertices[i], vertices[j]))
        for i in range(len(vertices))
        for j in range(i + 1, len(vertices))
    )
    vertices = [scale(vertex, edge_length / unit_edge) for vertex in vertices]
    edges = {
        (i, j)
        for i in range(len(vertices))
        for j in range(i + 1, len(vertices))
        if abs(length(subtract(vertices[i], vertices[j])) - edge_length) < TOLERANCE_M
    }
    faces = [
        (i, j, k)
        for i in range(len(vertices))
        for j in range(i + 1, len(vertices))
        for k in range(j + 1, len(vertices))
        if (i, j) in edges and (j, k) in edges and (i, k) in edges
    ]
    return vertices, faces


def outward_triangle(points):
    a, b, c = points
    normal = cross(subtract(b, a), subtract(c, a))
    if dot(normal, centroid(points)) < 0.0:
        return (a, c, b)
    return tuple(points)


def tetrahedral_modules(common_apex=False):
    vertices, macrofaces = regular_icosahedron(MACRO_EDGE_M)
    receiver_faces = []
    modules = []
    tetrahedron_height = FACE_EDGE_M * math.sqrt(2.0 / 3.0)
    for macroface_index, macroface in enumerate(macrofaces):
        a, b, c = (vertices[index] for index in macroface)
        ab, bc, ca = midpoint(a, b), midpoint(b, c), midpoint(c, a)
        subdivisions = ((a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca))
        for local_index, points in enumerate(subdivisions):
            face = outward_triangle(points)
            face_center = centroid(face)
            tangent_u = normalize(subtract(face[1], face[0]))
            outward_normal = normalize(cross(subtract(face[1], face[0]), subtract(face[2], face[0])))
            tangent_v = normalize(cross(outward_normal, tangent_u))
            apex = (0.0, 0.0, 0.0) if common_apex else subtract(face_center, scale(outward_normal, tetrahedron_height))
            receiver_faces.append(face)
            modules.append(
                {
                    "id": f"M{macroface_index:02d}-{local_index}",
                    "macroface": macroface_index,
                    "face": face,
                    "apex": apex,
                    "center": face_center,
                    "normal": outward_normal,
                    "tangent_u": tangent_u,
                    "tangent_v": tangent_v,
                    "tetrahedron": (*face, apex),
                }
            )
    return vertices, receiver_faces, modules


def module_collisions(modules):
    collisions = []
    for left, right in itertools.combinations(modules, 2):
        overlaps, penetration = tetrahedra_overlap(left["tetrahedron"], right["tetrahedron"])
        if overlaps:
            collisions.append((left["id"], right["id"], penetration))
    return collisions


def tetrahedron_axes(tetrahedron):
    face_indices = ((0, 1, 2), (0, 1, 3), (1, 2, 3), (2, 0, 3))
    edge_indices = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    face_normals = [
        cross(subtract(tetrahedron[j], tetrahedron[i]), subtract(tetrahedron[k], tetrahedron[i]))
        for i, j, k in face_indices
    ]
    edges = [subtract(tetrahedron[j], tetrahedron[i]) for i, j in edge_indices]
    return face_normals, edges


def tetrahedra_overlap(a, b):
    normals_a, edges_a = tetrahedron_axes(a)
    normals_b, edges_b = tetrahedron_axes(b)
    axes = normals_a + normals_b + [cross(edge_a, edge_b) for edge_a in edges_a for edge_b in edges_b]
    minimum_penetration = math.inf
    for axis in axes:
        if length(axis) < TOLERANCE_M:
            continue
        axis = normalize(axis)
        projection_a = [dot(point, axis) for point in a]
        projection_b = [dot(point, axis) for point in b]
        penetration = min(max(projection_a), max(projection_b)) - max(min(projection_a), min(projection_b))
        if penetration <= TOLERANCE_M:
            return False, penetration
        minimum_penetration = min(minimum_penetration, penetration)
    return True, minimum_penetration


def face_edge_key(a, b):
    return tuple(sorted(tuple(round(component, 8) for component in point) for point in (a, b)))


def main():
    vertices, receiver_faces, regular_modules = tetrahedral_modules()
    _, _, fitted_modules = tetrahedral_modules(common_apex=True)
    edge_lengths = []
    edge_uses = {}
    for face_index, face in enumerate(receiver_faces):
        for a, b in zip(face, face[1:] + face[:1]):
            edge_lengths.append(length(subtract(a, b)))
            edge_uses.setdefault(face_edge_key(a, b), []).append(face_index)

    tetrahedron_edges = []
    for module in regular_modules:
        tetrahedron_edges.extend(
            length(subtract(module["tetrahedron"][i], module["tetrahedron"][j]))
            for i, j in itertools.combinations(range(4), 2)
        )

    regular_collisions = module_collisions(regular_modules)
    fitted_collisions = module_collisions(fitted_modules)

    circumradius = max(length(vertex) for vertex in vertices)
    inradius = min(dot(module["center"], module["normal"]) for module in regular_modules)
    regular_apex_radii = [length(module["apex"]) for module in regular_modules]
    fitted_lateral_edges = [
        length(vertex)
        for module in fitted_modules
        for vertex in module["face"]
    ]
    shared_edges = sum(1 for uses in edge_uses.values() if len(uses) == 2)
    boundary_edges = sum(1 for uses in edge_uses.values() if len(uses) == 1)

    if len(receiver_faces) != 80 or len(regular_modules) != 80:
        raise SystemExit("Expected 80 tetrahedral face modules.")
    if max(abs(value - FACE_EDGE_M) for value in edge_lengths + tetrahedron_edges) > TOLERANCE_M:
        raise SystemExit("A 2 m edge constraint failed.")
    if boundary_edges != 0 or shared_edges != 120:
        raise SystemExit("Closed receiver-face adjacency failed.")
    if fitted_collisions:
        raise SystemExit("Common-apex tetrahedral partition unexpectedly overlaps.")

    print("RADOME regular-tetrahedral face verifier")
    print(f"receiver faces: {len(receiver_faces)}")
    print(f"shared outer edges: {shared_edges}; boundary edges: {boundary_edges}")
    print(f"all face and tetrahedron edges: {FACE_EDGE_M:.4f} m")
    print(f"macroface edge: {MACRO_EDGE_M:.4f} m")
    print(f"envelope circumradius: {circumradius:.4f} m")
    print(f"envelope inradius: {inradius:.4f} m")
    print(f"tetrahedron inward height: {FACE_EDGE_M * math.sqrt(2.0 / 3.0):.4f} m")
    print(f"regular-tetrahedron apex radius range: {min(regular_apex_radii):.4f}..{max(regular_apex_radii):.4f} m")
    print(f"regular-tetrahedron volumetric collisions: {len(regular_collisions)}")
    for left, right, penetration in regular_collisions[:5]:
        print(f"  {left} x {right}: SAT penetration >= {penetration:.6f} m")
    print("buildable common-apex partition:")
    print(f"  volumetric module collisions: {len(fitted_collisions)}")
    print(f"  shared Faraday side-wall interfaces: {shared_edges}")
    print(f"  lateral edge range: {min(fitted_lateral_edges):.4f}..{max(fitted_lateral_edges):.4f} m")
    if regular_collisions:
        print("finding: all-six-edges-at-2 m is incompatible with the closed inward assembly")
        print("adopted interpretation: 2 m external face edges with tetrahedra sharing the structural centre")


if __name__ == "__main__":
    main()