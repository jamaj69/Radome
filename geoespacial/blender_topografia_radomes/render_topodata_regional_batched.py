"""Renderiza a superfície regional TOPODATA com montagem batelada no Blender."""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy
from mathutils import Vector

from terrain_mesh_geometry import local_coordinates
import render_topodata_local_terrain as local_scene


def blue_marble_uv(longitude, latitude):
    """UV equiretangular da Blue Marble global para uma coordenada WGS84."""
    return (longitude + 180.0) / 360.0, (latitude + 90.0) / 180.0


def make_mesh(terrain, exaggeration, texture):
    """Monta vértices, faces e cores por ``foreach_set`` em uma única etapa."""
    longitudes, latitudes = terrain["longitude_samples"], terrain["latitude_samples"]
    elevations = terrain["elevations_m"]
    reference_lon = (longitudes[0] + longitudes[-1]) / 2
    reference_lat = (latitudes[0] + latitudes[-1]) / 2
    valid = [value for row in elevations for value in row if value is not None]
    reference_elevation = min(valid)
    low, high = min(valid), max(valid)
    vertices, colors, uvs, index = [], [], [], {}
    for row, latitude in enumerate(latitudes):
        for column, longitude in enumerate(longitudes):
            elevation = elevations[row][column]
            if elevation is None:
                continue
            east, north = local_coordinates(longitude, latitude, reference_lon, reference_lat)
            index[(row, column)] = len(vertices)
            vertices.append((east, north, (elevation - reference_elevation) * exaggeration))
            colors.extend(local_scene.elevation_color(elevation, low, high))
            uvs.append(blue_marble_uv(longitude, latitude))
    faces = []
    for row in range(len(latitudes) - 1):
        for column in range(len(longitudes) - 1):
            corners = [(row, column), (row, column + 1), (row + 1, column + 1), (row + 1, column)]
            if all(corner in index for corner in corners):
                faces.append(tuple(index[corner] for corner in corners))
    mesh = bpy.data.meshes.new("TOPODATA regional subamostrado")
    mesh.vertices.add(len(vertices))
    mesh.vertices.foreach_set("co", [component for vertex in vertices for component in vertex])
    mesh.loops.add(len(faces) * 4); mesh.polygons.add(len(faces))
    mesh.loops.foreach_set("vertex_index", [item for face in faces for item in face])
    mesh.polygons.foreach_set("loop_start", [number * 4 for number in range(len(faces))])
    mesh.polygons.foreach_set("loop_total", [4] * len(faces)); mesh.update(calc_edges=True)
    uv_layer = mesh.uv_layers.new(name="NASA Blue Marble WGS84")
    uv_layer.data.foreach_set("uv", [component for face in faces for vertex in face for component in uvs[vertex]])
    attribute = mesh.color_attributes.new("TOPODATA elevation", "BYTE_COLOR", "POINT")
    attribute.data.foreach_set("color", colors)
    object_ = bpy.data.objects.new("Superfície regional TOPODATA", mesh)
    bpy.context.collection.objects.link(object_)
    object_.data.materials.append(local_scene.orthophoto_material(texture))
    return object_, (reference_lon, reference_lat, reference_elevation), vertices


def grid_elevation(terrain, longitude, latitude):
    longitudes, latitudes = terrain["longitude_samples"], terrain["latitude_samples"]
    column = min(range(len(longitudes)), key=lambda item: abs(longitudes[item] - longitude))
    row = min(range(len(latitudes)), key=lambda item: abs(latitudes[item] - latitude))
    return terrain["elevations_m"][row][column]


def position(reference, longitude, latitude, elevation, exaggeration):
    lon0, lat0, low = reference
    east, north = local_coordinates(longitude, latitude, lon0, lat0)
    return Vector((east, north, (elevation - low) * exaggeration))


def emission(name, color, strength):
    material = bpy.data.materials.new(name); material.use_nodes = True
    node = material.node_tree.nodes.get("Principled BSDF")
    node.inputs["Base Color"].default_value = (*color, 1); node.inputs["Emission"].default_value = (*color, 1)
    node.inputs["Emission Strength"].default_value = strength; node.inputs["Roughness"].default_value = .4
    return material


def add_curve(name, points, material, bevel, z_offset, terrain, reference, exaggeration):
    if len(points) < 2:
        return
    curve = bpy.data.curves.new(name, "CURVE"); curve.dimensions = "3D"; curve.resolution_u = 1; curve.bevel_depth = bevel
    spline = curve.splines.new("POLY"); spline.points.add(len(points) - 1)
    for point, (longitude, latitude) in zip(spline.points, points):
        elevation = grid_elevation(terrain, longitude, latitude)
        point.co = (*position(reference, longitude, latitude, elevation, exaggeration)[:2], (elevation - reference[2]) * exaggeration + z_offset, 1)
    object_ = bpy.data.objects.new(name, curve); bpy.context.collection.objects.link(object_); object_.data.materials.append(material)


def add_boundaries(data, terrain, reference, exaggeration, span):
    if not data:
        return
    municipal = emission("IBGE municipal", (.12, .10, .08), .25)
    state = emission("IBGE estadual", (1.0, .66, .08), 1.2)
    for number, points in enumerate(data["municipal_boundaries"]):
        add_curve(f"Município {number}", points, municipal, span / 1800, span / 800, terrain, reference, exaggeration)
    for number, points in enumerate(data["state_boundaries"]):
        add_curve(f"Estado {number}", points, state, span / 950, span / 550, terrain, reference, exaggeration)


def add_radome(site, terrain, reference, exaggeration, radius, label_material):
    elevation = grid_elevation(terrain, site["longitude"], site["latitude"])
    base = position(reference, site["longitude"], site["latitude"], elevation, exaggeration)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=radius, location=base + Vector((0, 0, radius * 1.5)))
    dome = bpy.context.object; dome.name = f"Radome | {site['display_name']}"; dome.data.materials.append(emission(f"Radome {site['name']}", (1.0, .3, .03), 1.3))
    bpy.ops.mesh.primitive_torus_add(major_radius=radius * 1.35, minor_radius=radius * .14, major_segments=32, minor_segments=8, location=base + Vector((0, 0, radius * .22)))
    bpy.context.object.data.materials.append(emission(f"Anel {site['name']}", (1.0, .85, .18), 1.5))
    bpy.ops.object.text_add(location=base + Vector((radius * 1.8, radius * .9, radius * 3.2)))
    label = bpy.context.object; label.name = f"Rótulo | {site['display_name']}"; label.data.body = site["display_name"]
    label.data.align_x = "LEFT"; label.data.size = radius * .75; label.data.extrude = radius * .025; label.data.materials.append(label_material)


def build(terrain, boundaries, texture, blend, render, exaggeration=1.5, samples=128):
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
    _, reference, vertices = make_mesh(terrain, exaggeration, texture)
    x_values, y_values = [vertex[0] for vertex in vertices], [vertex[1] for vertex in vertices]
    x_span, y_span = max(x_values) - min(x_values), max(y_values) - min(y_values)
    span = max(x_span, y_span)
    add_boundaries(boundaries, terrain, reference, exaggeration, span)
    labels = emission("Rótulos", (1, 1, 1), 1.5)
    for site in terrain["sites"]:
        add_radome(site, terrain, reference, exaggeration, span / 115, labels)
    target = Vector(((min(x_values) + max(x_values)) / 2, (min(y_values) + max(y_values)) / 2, max(vertex[2] for vertex in vertices) / 2))
    bpy.ops.object.camera_add(location=(0, 0, target.z + span * 1.3))
    camera = bpy.context.object; bpy.context.scene.camera = camera; camera.data.type = "ORTHO"
    # Na câmera ortográfica do Blender, ``ortho_scale`` corresponde à altura
    # visível. A moldura WGS84 já contém a margem cartográfica desejada; não
    # acrescentamos uma segunda margem de câmera, que deixaria o fundo cinza
    # aparente ao redor da superfície.
    image_height = 2400
    image_width = max(1, round(image_height * x_span / y_span))
    camera.data.ortho_scale = y_span
    # A cena regional mede centenas de quilômetros. O padrão de 1 km do
    # Blender recortava toda a superfície antes da câmera, produzindo apenas
    # o fundo cinza. Mantemos uma folga para relevo, marcadores e divisas.
    camera.data.clip_start = 1.0
    camera.data.clip_end = span * 4.0
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.light_add(type="SUN", location=camera.location)
    sun = bpy.context.object; sun.data.energy = 2.2; sun.rotation_euler = (target - sun.location).to_track_quat("-Z", "Y").to_euler()
    output = bpy.context.scene; output.render.engine = "BLENDER_EEVEE"; output.eevee.taa_render_samples = samples
    output.view_settings.look = "Medium High Contrast"; output.world.color = (.018, .025, .035)
    output.render.resolution_x, output.render.resolution_y, output.render.resolution_percentage = image_width, image_height, 100
    output.render.image_settings.file_format = "PNG"; output.render.filepath = str(render)
    bpy.ops.wm.save_as_mainfile(filepath=str(blend)); bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--terrain", type=Path, required=True); parser.add_argument("--boundaries", type=Path, required=True)
    parser.add_argument("--texture", type=Path, required=True, help="Blue Marble global em projeção equiretangular")
    parser.add_argument("--blend", type=Path, required=True); parser.add_argument("--render", type=Path, required=True)
    parser.add_argument("--vertical-exaggeration", type=float, default=1.5); parser.add_argument("--samples", type=int, default=128)
    arguments = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    build(json.loads(arguments.terrain.read_text()), json.loads(arguments.boundaries.read_text()), arguments.texture.resolve(), arguments.blend.resolve(), arguments.render.resolve(), arguments.vertical_exaggeration, arguments.samples)
