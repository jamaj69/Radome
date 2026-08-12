"""Cria uma cena local Blender cuja superficie segue cada cota TOPODATA."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy
from mathutils import Vector
from terrain_mesh_geometry import local_coordinates, terrain_geometry


def elevation_color(elevation, low, high):
    ratio = (elevation - low) / max(high - low, 1)
    return (.08 + .52 * ratio, .18 + .38 * ratio, .06 + .10 * ratio, 1)


def material(name, color, metallic=0.0, roughness=.6):
    item = bpy.data.materials.new(name)
    item.diffuse_color = (*color, 1)
    item.metallic = metallic
    item.roughness = roughness
    return item


def elevation_material():
    item = bpy.data.materials.new("Terrain elevation material")
    item.use_nodes = True
    nodes, links = item.node_tree.nodes, item.node_tree.links
    color = nodes.new("ShaderNodeVertexColor")
    color.layer_name = "TOPODATA elevation"
    shader = nodes.get("Principled BSDF")
    links.new(color.outputs["Color"], shader.inputs["Base Color"])
    shader.inputs["Roughness"].default_value = .72
    return item


def orthophoto_material(image_path):
    """Materializa uma ortoimagem georreferenciada na mesma janela da malha."""
    item = bpy.data.materials.new("Local orthophoto texture")
    item.use_nodes = True
    nodes, links = item.node_tree.nodes, item.node_tree.links
    image = nodes.new("ShaderNodeTexImage")
    image.image = bpy.data.images.load(str(image_path), check_existing=True)
    shader = nodes.get("Principled BSDF")
    links.new(image.outputs["Color"], shader.inputs["Base Color"])
    shader.inputs["Roughness"].default_value = .68
    return item


def add_terrain(site, vertical_exaggeration, orthophoto=None):
    vertices, faces, reference = terrain_geometry(site, vertical_exaggeration)
    mesh = bpy.data.meshes.new(f"TOPODATA grid | {site['display_name']}")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    uv_map = mesh.uv_layers.new(name="Orthophoto UV")
    x_values, y_values = [vertex[0] for vertex in vertices], [vertex[1] for vertex in vertices]
    min_x, max_x, min_y, max_y = min(x_values), max(x_values), min(y_values), max(y_values)
    for polygon in mesh.polygons:
        for loop_index, vertex_index in zip(polygon.loop_indices, polygon.vertices):
            x, y, _ = vertices[vertex_index]
            uv_map.data[loop_index].uv = ((x - min_x) / max(max_x - min_x, 1), (y - min_y) / max(max_y - min_y, 1))
    elevations = [vertex[2] for vertex in site["vertices"]]
    colors = mesh.color_attributes.new("TOPODATA elevation", "BYTE_COLOR", "POINT")
    for index, elevation in enumerate(elevations):
        colors.data[index].color = elevation_color(elevation, min(elevations), max(elevations))
    terrain = bpy.data.objects.new(f"Terrain surface | {site['display_name']}", mesh)
    bpy.context.collection.objects.link(terrain)
    terrain.data.materials.append(orthophoto_material(orthophoto) if orthophoto else elevation_material())
    wire = terrain.copy()
    wire.data = terrain.data.copy()
    wire.name = f"Terrain grid | {site['display_name']}"
    wire.data.materials.clear()
    wire.data.materials.append(material("Terrain grid material", (.04, .055, .025), roughness=.42))
    modifier = wire.modifiers.new("Grid edges", "WIREFRAME")
    modifier.thickness = .65
    modifier.use_even_offset = True
    bpy.context.collection.objects.link(wire)
    return terrain, reference


def nearest_vertex(site):
    return min(site["vertices"], key=lambda vertex: (vertex[0] - site["longitude"]) ** 2 + (vertex[1] - site["latitude"]) ** 2)


def add_radome(site, reference_elevation, vertical_exaggeration):
    longitude, latitude, elevation = nearest_vertex(site)
    east, north = local_coordinates(longitude, latitude, site["longitude"], site["latitude"])
    ground = (elevation - reference_elevation) * vertical_exaggeration
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=18, depth=4, location=(east, north, ground + 2))
    base = bpy.context.object
    base.name = f"Radome base | {site['display_name']}"
    base.data.materials.append(material("Radome concrete base", (.22, .24, .24), .15))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=(east, north, ground + 16))
    dome = bpy.context.object
    dome.name = f"Radome | {site['display_name']}"
    dome.scale = (14, 14, 14)
    dome.data.materials.append(material("Radome shell", (.92, .94, .96), .05, .3))
    return Vector((east, north, ground))


def add_camera(target, span, top_down):
    if top_down:
        bpy.ops.object.camera_add(location=target + Vector((0, 0, span * 1.35)))
        camera = bpy.context.object
        camera.name = "Top-down terrain inspection camera"
        camera.data.type = "ORTHO"
        camera.data.ortho_scale = span * 1.15
        camera.data.clip_end = span * 4
        camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
        bpy.context.scene.camera = camera
        return camera
    bpy.ops.object.camera_add(location=target + Vector((span * .85, -span * 1.05, span * .72)))
    camera = bpy.context.object
    camera.name = "Local terrain inspection camera"
    camera.data.lens = 48
    camera.data.clip_end = span * 4
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = camera
    return camera


def build(terrain, blend, render, site_index=0, vertical_exaggeration=1.5, samples=128,
          top_down=False, orthophoto=None):
    if not 0 <= site_index < len(terrain["sites"]):
        raise ValueError("site-index fora do intervalo")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    site = terrain["sites"][site_index]
    if orthophoto is None and site.get("hillshade_texture"):
        orthophoto = Path(site["hillshade_texture"])
    _, reference = add_terrain(site, vertical_exaggeration, orthophoto)
    target = add_radome(site, reference, vertical_exaggeration)
    vertices, _, _ = terrain_geometry(site, vertical_exaggeration)
    span = max(max(abs(vertex[0]), abs(vertex[1])) for vertex in vertices) * 2
    camera = add_camera(target, span, top_down)
    bpy.ops.object.light_add(type="SUN", location=camera.location * 3)
    sun = bpy.context.object
    sun.name = "Sun | camera-side local terrain"
    sun.data.energy = 3.0
    sun.rotation_euler = (target - sun.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.light_add(type="AREA", location=camera.location * .7)
    fill = bpy.context.object
    fill.data.energy, fill.data.size = 1_500, span
    fill.rotation_euler = (target - fill.location).to_track_quat("-Z", "Y").to_euler()
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = samples
    scene.view_settings.look = "Medium High Contrast"
    scene.render.resolution_x, scene.render.resolution_y = 2400, 1500
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(render)
    scene.world.color = (.025, .035, .05)
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--terrain", type=Path, required=True)
    parser.add_argument("--blend", type=Path, required=True)
    parser.add_argument("--render", type=Path, required=True)
    parser.add_argument("--site-index", type=int, default=0)
    parser.add_argument("--vertical-exaggeration", type=float, default=1.5)
    parser.add_argument("--samples", type=int, default=128)
    parser.add_argument("--top-down", action="store_true")
    parser.add_argument("--orthophoto", type=Path, help="Imagem ortorretificada da mesma janela DEM")
    arguments = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    build(json.loads(arguments.terrain.read_text(encoding="utf-8")), arguments.blend.resolve(), arguments.render.resolve(), arguments.site_index, arguments.vertical_exaggeration, arguments.samples, arguments.top_down, arguments.orthophoto.resolve() if arguments.orthophoto else None)
