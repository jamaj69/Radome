"""Monta uma visão continental cartográfica da Terra curva e três candidatos.

O relevo TOPODATA e os pontos de cota são diagnósticos locais: eles só entram
quando solicitados explicitamente, pois não são legíveis na escala continental.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


EARTH_RADIUS_UNITS = 25.0
ELEVATION_UNITS_PER_M = 1 / 5000
LABEL_LAYOUT = ((-1.10, 0.72), (1.12, 0.22), (0.02, -0.92))


def position(latitude, longitude, elevation_m):
    lat, lon = math.radians(latitude), math.radians(longitude)
    radius = EARTH_RADIUS_UNITS + elevation_m * ELEVATION_UNITS_PER_M
    return Vector((
        radius * math.cos(lat) * math.cos(lon),
        radius * math.cos(lat) * math.sin(lon),
        radius * math.sin(lat),
    ))


def material(name, color, metallic=0.0):
    item = bpy.data.materials.new(name)
    item.diffuse_color = (*color, 1)
    item.metallic = metallic
    item.roughness = 0.55
    return item


def earth_material(texture):
    item = bpy.data.materials.new("NASA Blue Marble topography and bathymetry")
    item.use_nodes = True
    nodes, links = item.node_tree.nodes, item.node_tree.links
    image = nodes.new("ShaderNodeTexImage")
    image.image = bpy.data.images.load(str(texture), check_existing=True)
    shader = nodes.get("Principled BSDF")
    links.new(image.outputs["Color"], shader.inputs["Base Color"])
    links.new(image.outputs["Color"], shader.inputs["Emission"])
    shader.inputs["Emission Strength"].default_value = 0.08
    shader.inputs["Roughness"].default_value = 0.78
    return item


def label_material(name, color, emission=0.0):
    item = bpy.data.materials.new(name)
    item.use_nodes = True
    shader = item.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Emission"].default_value = (*color, 1)
    shader.inputs["Emission Strength"].default_value = emission
    shader.inputs["Roughness"].default_value = 0.65
    return item


def geo_position(longitude, latitude, offset=.03):
    return position(latitude, longitude, offset / ELEVATION_UNITS_PER_M)


def add_curve(points, name, color, bevel_depth):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 2
    curve.bevel_depth = bevel_depth
    curve.resolution_u = 2
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, coordinate in zip(spline.points, points):
        point.co = (*geo_position(*coordinate), 1)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material(name, color))
    return obj


def add_line(start, end, name, color, bevel_depth):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = bevel_depth
    spline = curve.splines.new("POLY")
    spline.points.add(1)
    spline.points[0].co = (*start, 1)
    spline.points[1].co = (*end, 1)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material(name, color))
    return obj


def add_overlays(overlays, show_altitude_points=False):
    for ring in overlays["state_boundaries"]:
        add_curve(ring, "State boundary", (.89, .89, .82), .0025)
    for ring in overlays["international_boundaries"]:
        add_curve(ring, "International boundary", (.98, .75, .08), .004)
    if not show_altitude_points:
        return
    elevations = [point["elevation_m"] for point in overlays["altitude_samples"]]
    low, high = min(elevations), max(elevations)
    for point in overlays["altitude_samples"]:
        ratio = (point["elevation_m"] - low) / max(1, high - low)
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=1,
            radius=.018,
            location=geo_position(point["longitude"], point["latitude"], .08),
        )
        bpy.context.object.data.materials.append(
            material("Altitude diagnostic point", (ratio, .08, 1 - ratio))
        )


def add_terrain(terrain):
    for site in terrain["sites"]:
        vertices = [position(lat, lon, elevation) for lon, lat, elevation in site["vertices"]]
        width, height = site["width"], site["height"]
        faces = [
            (y * width + x, y * width + x + 1, (y + 1) * width + x + 1, (y + 1) * width + x)
            for y in range(height - 1) for x in range(width - 1)
        ]
        mesh = bpy.data.meshes.new(f"TOPODATA | {site['name']}")
        mesh.from_pydata(vertices, [], faces)
        obj = bpy.data.objects.new(f"TOPODATA terrain | {site['name']}", mesh)
        bpy.context.collection.objects.link(obj)
        obj.data.materials.append(material("TOPODATA terrain", (.20, .36, .12)))


def add_radome(site, camera, label_index, label_text):
    point = position(site["latitude"], site["longitude"], site["terrain_elevation_m"])
    normal = point.normalized()
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=.035, location=point + normal * .04)
    dome = bpy.context.object
    dome.name = f"RADOME | {site['name']}"
    dome.data.materials.append(material("Radome white", (.92, .94, .96)))
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=.010, depth=.07, location=point + normal * .015)
    mast = bpy.context.object
    mast.name = f"Mast | {site['name']}"
    mast.data.materials.append(material("Mast", (.12, .16, .18), .7))
    mast.rotation_mode = "QUATERNION"
    mast.rotation_quaternion = normal.to_track_quat("Z", "Y")

    camera_basis = camera.matrix_world.to_3x3()
    right = camera_basis @ Vector((1, 0, 0))
    up = camera_basis @ Vector((0, 1, 0))
    horizontal, vertical = LABEL_LAYOUT[label_index]
    anchor = point + normal * .055
    # Keep callouts in a common plane in front of the globe.  Moving them only
    # along a local surface tangent can put the far edge behind the Earth.
    camera_depth = (camera.location - point).normalized()
    label_position = anchor + right * horizontal + up * vertical + camera_depth * 1.20
    facing = (camera.location - label_position).normalized()
    add_line(anchor, label_position - facing * .012, f"Leader | {site['name']}", (.96, .96, .92), .002)

    bpy.ops.object.text_add(location=label_position + facing * .003)
    label = bpy.context.object
    label.name = f"Label | {site['name']}"
    label.data.body = f"{site['display_name']}\\n{site['terrain_elevation_m']:.0f} m"
    label.data.align_x = "CENTER"
    label.data.align_y = "CENTER"
    label.data.size = .32
    label.data.resolution_u = 16
    label.data.space_line = .82
    label.data.materials.append(label_text)
    label.rotation_mode = "QUATERNION"
    label.rotation_quaternion = facing.to_track_quat("Z", "Y")


def add_camera(target, overview):
    outward = target.normalized()
    location = outward * 72 if overview else outward * 55 + Vector((7, -7, 5))
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = 38 if overview else 52
    return camera


def build(selection, overlays, terrain, texture, blend, render, overview=False,
          include_local_terrain=False, show_altitude_points=False):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=192, ring_count=128, radius=EARTH_RADIUS_UNITS)
    earth = bpy.context.object
    earth.name = "Earth | NASA Blue Marble context"
    earth.data.materials.append(earth_material(texture))
    add_overlays(overlays, show_altitude_points)
    if include_local_terrain:
        add_terrain(terrain)
    site_points = [position(site["latitude"], site["longitude"], site["terrain_elevation_m"])
                   for site in selection["selected_sites"]]
    target = sum(site_points, Vector()) / len(site_points)
    camera = add_camera(target, overview)
    text = label_material("Black labels", (.003, .003, .003), 0.0)
    for index, site in enumerate(selection["selected_sites"]):
        add_radome(site, camera, index, text)
    bpy.ops.object.light_add(type="SUN", location=camera.location * 8)
    sun = bpy.context.object
    sun.name = "Sun | camera-side illumination"
    sun.data.energy = 2.4
    sun.rotation_euler = (target - sun.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.light_add(type="AREA", location=camera.location * .92)
    fill = bpy.context.object
    fill.name = "Camera-side fill"
    fill.data.energy = 420
    fill.data.shape = "DISK"
    fill.data.size = 30
    fill.rotation_euler = (target - fill.location).to_track_quat("-Z", "Y").to_euler()
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 64
    scene.view_settings.look = "Medium High Contrast"
    scene.view_settings.exposure = .25
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(render)
    scene.world.color = (.015, .02, .04)
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--overlays", type=Path, required=True)
    parser.add_argument("--terrain", type=Path, required=True)
    parser.add_argument("--texture", type=Path, required=True)
    parser.add_argument("--blend", type=Path, required=True)
    parser.add_argument("--render", type=Path, required=True)
    parser.add_argument("--overview", action="store_true")
    parser.add_argument("--include-local-terrain", action="store_true")
    parser.add_argument("--show-altitude-points", action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    for field in ("blend", "render", "selection", "overlays", "terrain", "texture"):
        setattr(args, field, getattr(args, field).resolve())
    args.blend.parent.mkdir(parents=True, exist_ok=True)
    args.render.parent.mkdir(parents=True, exist_ok=True)
    build(
        json.loads(args.selection.read_text(encoding="utf-8")),
        json.loads(args.overlays.read_text(encoding="utf-8")),
        json.loads(args.terrain.read_text(encoding="utf-8")),
        args.texture, args.blend, args.render, args.overview,
        args.include_local_terrain, args.show_altitude_points,
    )
