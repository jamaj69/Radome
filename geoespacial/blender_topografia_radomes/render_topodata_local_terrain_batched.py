"""Alternativa acelerada: constrói a malha TOPODATA com ``foreach_set``."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy
from terrain_mesh_geometry import terrain_geometry
import render_topodata_local_terrain as scene


def add_terrain_batched(site, vertical_exaggeration, orthophoto=None):
    vertices, faces, reference = terrain_geometry(site, vertical_exaggeration)
    mesh = bpy.data.meshes.new(f"TOPODATA batched grid | {site['display_name']}")
    mesh.vertices.add(len(vertices))
    mesh.vertices.foreach_set("co", [coordinate for vertex in vertices for coordinate in vertex])
    loop_count = len(faces) * 4
    mesh.loops.add(loop_count)
    mesh.polygons.add(len(faces))
    mesh.loops.foreach_set("vertex_index", [index for face in faces for index in face])
    mesh.polygons.foreach_set("loop_start", [index * 4 for index in range(len(faces))])
    mesh.polygons.foreach_set("loop_total", [4] * len(faces))
    mesh.update(calc_edges=True)

    x_values, y_values = [vertex[0] for vertex in vertices], [vertex[1] for vertex in vertices]
    min_x, max_x, min_y, max_y = min(x_values), max(x_values), min(y_values), max(y_values)
    uv = mesh.uv_layers.new(name="Orthophoto UV")
    uv.data.foreach_set("uv", [component for face in faces for index in face for component in (
        (vertices[index][0] - min_x) / max(max_x - min_x, 1),
        (vertices[index][1] - min_y) / max(max_y - min_y, 1),
    )])
    elevations = [vertex[2] for vertex in site["vertices"]]
    low, high = min(elevations), max(elevations)
    colors = mesh.color_attributes.new("TOPODATA elevation", "BYTE_COLOR", "POINT")
    colors.data.foreach_set("color", [component for elevation in elevations for component in scene.elevation_color(elevation, low, high)])
    terrain = bpy.data.objects.new(f"Terrain batched surface | {site['display_name']}", mesh)
    bpy.context.collection.objects.link(terrain)
    terrain.data.materials.append(scene.orthophoto_material(orthophoto) if orthophoto else scene.elevation_material())
    return terrain, reference


def build(terrain, blend, render, site_index=0, vertical_exaggeration=1.5, samples=128,
          top_down=False, orthophoto=None, boundaries=None):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    site = terrain["sites"][site_index]
    if orthophoto is None and site.get("hillshade_texture"):
        orthophoto = Path(site["hillshade_texture"])
    _, reference = add_terrain_batched(site, vertical_exaggeration, orthophoto)
    target = scene.add_radome(site, reference, vertical_exaggeration)
    scene.add_boundaries(boundaries, site, vertical_exaggeration)
    vertices, _, _ = terrain_geometry(site, vertical_exaggeration)
    span = max(max(abs(vertex[0]), abs(vertex[1])) for vertex in vertices) * 2
    camera = scene.add_camera(target, span, top_down)
    bpy.ops.object.light_add(type="SUN", location=camera.location * 3)
    sun = bpy.context.object; sun.data.energy = 3.0; sun.rotation_euler = (target - sun.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.light_add(type="AREA", location=camera.location * .7)
    fill = bpy.context.object; fill.data.energy, fill.data.size = 1500, span; fill.rotation_euler = (target - fill.location).to_track_quat("-Z", "Y").to_euler()
    output = bpy.context.scene
    output.render.engine = "BLENDER_EEVEE"; output.eevee.taa_render_samples = samples
    output.view_settings.look = "Medium High Contrast"
    output.render.resolution_x, output.render.resolution_y = 2400, 1500
    output.render.resolution_percentage = 100; output.render.image_settings.file_format = "PNG"; output.render.filepath = str(render)
    output.world.color = (.025, .035, .05)
    bpy.ops.wm.save_as_mainfile(filepath=str(blend)); bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--terrain", type=Path, required=True); parser.add_argument("--blend", type=Path, required=True); parser.add_argument("--render", type=Path, required=True)
    parser.add_argument("--site-index", type=int, default=0); parser.add_argument("--vertical-exaggeration", type=float, default=1.5); parser.add_argument("--samples", type=int, default=128)
    parser.add_argument("--top-down", action="store_true"); parser.add_argument("--orthophoto", type=Path); parser.add_argument("--boundaries", type=Path)
    arguments = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    build(json.loads(arguments.terrain.read_text()), arguments.blend.resolve(), arguments.render.resolve(), arguments.site_index, arguments.vertical_exaggeration, arguments.samples, arguments.top_down, arguments.orthophoto.resolve() if arguments.orthophoto else None, json.loads(arguments.boundaries.read_text()) if arguments.boundaries else None)
