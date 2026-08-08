#!/usr/bin/env python3
"""Verify the C2 candidate geodesic radome geometry.

The model is a class-I, frequency-2 subdivision of a regular icosahedron:
each triangular macroface is split at edge midpoints into four triangles and
all new vertices are projected to a common sphere.
"""

from __future__ import annotations

import math


FREQUENCY = 2
CUT_LATITUDE_DEG = -35.0
REFERENCE_EDGE_M = 2.0


def normalize(point):
    length = math.sqrt(sum(component * component for component in point))
    return tuple(component / length for component in point)


def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def regular_icosahedron():
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    vertices = []
    for point in (
        (0, 1, phi),
        (0, -1, phi),
        (0, 1, -phi),
        (0, -1, -phi),
        (1, phi, 0),
        (-1, phi, 0),
        (1, -phi, 0),
        (-1, -phi, 0),
        (phi, 0, 1),
        (-phi, 0, 1),
        (phi, 0, -1),
        (-phi, 0, -1),
    ):
        vertices.append(normalize(point))

    pair_distances = []
    for i, vertex_a in enumerate(vertices):
        for j, vertex_b in enumerate(vertices[i + 1 :], i + 1):
            pair_distances.append((distance(vertex_a, vertex_b), i, j))

    base_edge_length = min(item[0] for item in pair_distances)
    edges = {
        tuple(sorted((i, j)))
        for edge_length, i, j in pair_distances
        if abs(edge_length - base_edge_length) < 1e-9
    }

    faces = []
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            for k in range(j + 1, len(vertices)):
                if (
                    tuple(sorted((i, j))) in edges
                    and tuple(sorted((j, k))) in edges
                    and tuple(sorted((i, k))) in edges
                ):
                    faces.append((i, j, k))

    return vertices, edges, faces


def subdivide_frequency_2(vertices, edges, faces):
    if FREQUENCY != 2:
        raise ValueError("This verifier currently fixes the C2 candidate at frequency 2.")

    subdivided_vertices = list(vertices)
    midpoint_index = {}
    for edge in sorted(edges):
        i, j = edge
        midpoint = normalize(tuple((vertices[i][axis] + vertices[j][axis]) / 2.0 for axis in range(3)))
        midpoint_index[edge] = len(subdivided_vertices)
        subdivided_vertices.append(midpoint)

    subdivided_faces = []
    for i, j, k in faces:
        midpoint_ij = midpoint_index[tuple(sorted((i, j)))]
        midpoint_jk = midpoint_index[tuple(sorted((j, k)))]
        midpoint_ki = midpoint_index[tuple(sorted((k, i)))]
        subdivided_faces.extend(
            [
                (i, midpoint_ij, midpoint_ki),
                (midpoint_ij, j, midpoint_jk),
                (midpoint_ki, midpoint_jk, k),
                (midpoint_ij, midpoint_jk, midpoint_ki),
            ]
        )

    return subdivided_vertices, subdivided_faces


def face_edges(faces):
    edges = set()
    for face in faces:
        for start, end in ((face[0], face[1]), (face[1], face[2]), (face[2], face[0])):
            edges.add(tuple(sorted((start, end))))
    return edges


def grouped_lengths(vertices, edges):
    groups = {}
    for edge in edges:
        edge_length = round(distance(vertices[edge[0]], vertices[edge[1]]), 12)
        groups[edge_length] = groups.get(edge_length, 0) + 1
    return sorted(groups.items())


def main():
    base_vertices, base_edges, base_faces = regular_icosahedron()
    vertices, faces = subdivide_frequency_2(base_vertices, base_edges, base_faces)
    edges = face_edges(faces)

    euler = len(vertices) - len(edges) + len(faces)
    if (len(base_vertices), len(base_edges), len(base_faces)) != (12, 30, 20):
        raise SystemExit("Base icosahedron topology check failed.")
    if (len(vertices), len(edges), len(faces), euler) != (42, 120, 80, 2):
        raise SystemExit("Frequency-2 geodesic topology check failed.")

    edge_classes = grouped_lengths(vertices, edges)
    shortest_unit_edge = edge_classes[0][0]
    radius_for_reference_edge = REFERENCE_EDGE_M / shortest_unit_edge
    diameter_for_reference_edge = 2.0 * radius_for_reference_edge
    cut_latitude_rad = math.radians(CUT_LATITUDE_DEG)
    cut_z = radius_for_reference_edge * math.sin(cut_latitude_rad)
    support_radius = radius_for_reference_edge * math.cos(cut_latitude_rad)

    print("RADOME C2 geometry verifier")
    print(f"base: V={len(base_vertices)} E={len(base_edges)} F={len(base_faces)}")
    print(f"class-I frequency={FREQUENCY}")
    print(f"closed mesh: V={len(vertices)} E={len(edges)} F={len(faces)} Euler={euler}")
    print("unit-radius chord classes:")
    for edge_length, count in edge_classes:
        print(f"  {edge_length:.12f}: {count} edges")
    print(f"if shortest chord is {REFERENCE_EDGE_M:.3f} m:")
    print(f"  R={radius_for_reference_edge:.4f} m")
    print(f"  D={diameter_for_reference_edge:.4f} m")
    print(f"  cut z/R={math.sin(cut_latitude_rad):.6f}")
    print(f"  cut z={cut_z:.4f} m")
    print(f"  support ring radius={support_radius:.4f} m")
    print(f"  support ring diameter={2.0 * support_radius:.4f} m")


if __name__ == "__main__":
    main()
