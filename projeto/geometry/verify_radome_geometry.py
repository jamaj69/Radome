#!/home/python/pyenv/bin/python
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
BASE_WIDTH_M = 4.0
BASE_DEPTH_M = 4.0
SUPPORT_TRANSITION_PLAN_M = 6.6
SUPPORT_RADIAL_MARGIN_M = 0.30


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
        for start, end in zip(face, face[1:] + face[:1]):
            edges.add(tuple(sorted((start, end))))
    return edges


def grouped_lengths(vertices, edges):
    groups = {}
    for edge in edges:
        edge_length = round(distance(vertices[edge[0]], vertices[edge[1]]), 12)
        groups[edge_length] = groups.get(edge_length, 0) + 1
    return sorted(groups.items())


def clip_segment_to_cut(point_a, point_b, cut_z):
    fraction = (cut_z - point_a[2]) / (point_b[2] - point_a[2])
    return tuple(point_a[axis] + fraction * (point_b[axis] - point_a[axis]) for axis in range(3))


def clip_polygon_to_cut(polygon, cut_z):
    clipped = []
    for index, point_a in enumerate(polygon):
        point_b = polygon[(index + 1) % len(polygon)]
        a_inside = point_a[2] >= cut_z - 1e-12
        b_inside = point_b[2] >= cut_z - 1e-12
        if a_inside and b_inside:
            clipped.append(point_b)
        elif a_inside and not b_inside:
            clipped.append(clip_segment_to_cut(point_a, point_b, cut_z))
        elif not a_inside and b_inside:
            clipped.append(clip_segment_to_cut(point_a, point_b, cut_z))
            clipped.append(point_b)
    return clipped


def clipped_mesh(vertices, faces, cut_z):
    polygons = []
    for face in faces:
        polygon = clip_polygon_to_cut([vertices[index] for index in face], cut_z)
        if len(polygon) >= 3:
            polygons.append(polygon)

    vertex_index = {}
    clipped_vertices = []
    clipped_faces = []
    for polygon in polygons:
        face_indices = []
        for point in polygon:
            key = tuple(round(component, 10) for component in point)
            if key not in vertex_index:
                vertex_index[key] = len(clipped_vertices)
                clipped_vertices.append(point)
            face_indices.append(vertex_index[key])
        clipped_faces.append(tuple(face_indices))

    return clipped_vertices, clipped_faces


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
    base_edge_unit = grouped_lengths(base_vertices, base_edges)[0][0]
    shortest_unit_edge = edge_classes[0][0]
    radius_for_reference_edge = REFERENCE_EDGE_M / shortest_unit_edge
    diameter_for_reference_edge = 2.0 * radius_for_reference_edge
    cut_latitude_rad = math.radians(CUT_LATITUDE_DEG)
    cut_z_over_r = math.sin(cut_latitude_rad)
    cut_z = radius_for_reference_edge * cut_z_over_r
    support_radius = radius_for_reference_edge * math.cos(cut_latitude_rad)
    support_diameter = 2.0 * support_radius
    segment_height = radius_for_reference_edge - cut_z
    minimum_direct_square = support_diameter + 2.0 * SUPPORT_RADIAL_MARGIN_M
    direct_base_support_ok = BASE_WIDTH_M >= minimum_direct_square and BASE_DEPTH_M >= minimum_direct_square
    transition_support_ok = SUPPORT_TRANSITION_PLAN_M >= minimum_direct_square
    cut_vertices, cut_faces = clipped_mesh(vertices, faces, cut_z_over_r)
    cut_edges = face_edges(cut_faces)
    cut_edge_use = {}
    for face in cut_faces:
        for start, end in zip(face, face[1:] + face[:1]):
            edge = tuple(sorted((start, end)))
            cut_edge_use[edge] = cut_edge_use.get(edge, 0) + 1
    boundary_edges = [edge for edge, use_count in cut_edge_use.items() if use_count == 1]
    boundary_vertices = {index for edge in boundary_edges for index in edge}
    cut_euler = len(cut_vertices) - len(cut_edges) + len(cut_faces)
    if cut_euler != 1:
        raise SystemExit("Cut radome topology check failed.")
    if not transition_support_ok:
        raise SystemExit("Support transition envelope check failed.")

    print("RADOME C2 geometry verifier")
    print(f"base: V={len(base_vertices)} E={len(base_edges)} F={len(base_faces)}")
    print(f"class-I frequency={FREQUENCY}")
    print(f"closed mesh: V={len(vertices)} E={len(edges)} F={len(faces)} Euler={euler}")
    print("unit-radius chord classes:")
    for edge_length, count in edge_classes:
        print(
            f"  {edge_length:.12f}: {count} edges "
            f"({edge_length * radius_for_reference_edge:.4f} m at reference scale)"
        )
    print(f"if shortest chord is {REFERENCE_EDGE_M:.3f} m:")
    print(f"  R={radius_for_reference_edge:.4f} m")
    print(f"  D={diameter_for_reference_edge:.4f} m")
    print(f"  macroface chord={base_edge_unit * radius_for_reference_edge:.4f} m")
    print(f"  cut z/R={cut_z_over_r:.6f}")
    print(f"  cut z={cut_z:.4f} m")
    print(f"  spherical segment height={segment_height:.4f} m")
    print(f"  support ring radius={support_radius:.4f} m")
    print(f"  support ring diameter={support_diameter:.4f} m")
    print(f"  4.0 m x 4.0 m base direct support ok={direct_base_support_ok}")
    print(
        f"  transition square={SUPPORT_TRANSITION_PLAN_M:.2f} m, "
        f"minimum with margin={minimum_direct_square:.4f} m, "
        f"transition ok={transition_support_ok}"
    )
    print(
        "cut mesh: "
        f"V={len(cut_vertices)} E={len(cut_edges)} F={len(cut_faces)} "
        f"Euler={cut_euler} boundary_edges={len(boundary_edges)} "
        f"boundary_vertices={len(boundary_vertices)}"
    )


if __name__ == "__main__":
    main()
