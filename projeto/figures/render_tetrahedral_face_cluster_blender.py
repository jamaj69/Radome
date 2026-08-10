"""Render a contiguous cluster of 2 m tetrahedral radome face modules."""

import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_paths import build_output


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "geometry"))

from verify_tetrahedral_face_geometry import PYRAMID_HEIGHT_M, face_edge_key, tetrahedral_modules


OUTPUT = str(build_output("fig16_tetrahedral_face_cluster.png"))
BLEND_OUTPUT = str(build_output("radome_tetrahedral_face_cluster.blend"))
CLUSTER_SIZE = 7


def material(name, color, metallic=0.0, roughness=0.45, alpha=1.0):
    result = bpy.data.materials.new(name)
    result.diffuse_color = (*color, alpha)
    result.use_nodes = True
    shader = result.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1.0)
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Alpha"].default_value = alpha
    if alpha < 1.0:
        result.blend_method = "BLEND"
        result.use_screen_refraction = True
    return result


def triangle(name, points, face_material):
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata([tuple(point) for point in points], [], [(0, 1, 2)])
    mesh.update()
    result = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(result)
    result.data.materials.append(face_material)
    return result


def cylinder_between(name, start, end, radius, cylinder_material, vertices=16):
    start, end = Vector(start), Vector(end)
    direction = end - start
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=direction.length,
        location=(start + end) / 2.0,
    )
    result = bpy.context.object
    result.name = name
    result.rotation_mode = "QUATERNION"
    result.rotation_quaternion = direction.to_track_quat("Z", "Y")
    result.data.materials.append(cylinder_material)
    return result


def arrow(name, start, direction, arrow_material, length=0.58):
    start = Vector(start)
    direction = Vector(direction).normalized()
    shaft_end = start + direction * (length * 0.78)
    tip = start + direction * length
    cylinder_between(name + " shaft", start, shaft_end, 0.018, arrow_material, 12)
    bpy.ops.mesh.primitive_cone_add(
        vertices=16,
        radius1=0.065,
        radius2=0.0,
        depth=length * 0.22,
        location=(shaft_end + tip) / 2.0,
    )
    cone = bpy.context.object
    cone.name = name + " arrowhead"
    cone.rotation_mode = "QUATERNION"
    cone.rotation_quaternion = direction.to_track_quat("Z", "Y")
    cone.data.materials.append(arrow_material)


def oriented_box(name, location, tangent_u, tangent_v, normal, dimensions, box_material):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    result = bpy.context.object
    result.name = name
    result.rotation_euler = Matrix((Vector(tangent_u), Vector(tangent_v), Vector(normal))).transposed().to_euler()
    result.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    result.data.materials.append(box_material)
    bevel = result.modifiers.new("Conductive enclosure edge", "BEVEL")
    bevel.width = 0.018
    bevel.segments = 2
    return result


def select_contiguous_cluster(modules, count):
    edge_faces = {}
    for index, module in enumerate(modules):
        face = module["face"]
        for start, end in zip(face, face[1:] + face[:1]):
            edge_faces.setdefault(face_edge_key(start, end), []).append(index)
    adjacency = {index: set() for index in range(len(modules))}
    for uses in edge_faces.values():
        if len(uses) == 2:
            adjacency[uses[0]].add(uses[1])
            adjacency[uses[1]].add(uses[0])
    seed = max(range(len(modules)), key=lambda index: dot(modules[index]["center"], (1.0, -0.35, 0.55)))
    selected = []
    queue = [seed]
    while queue and len(selected) < count:
        current = queue.pop(0)
        if current in selected:
            continue
        selected.append(current)
        queue.extend(sorted(adjacency[current] - set(selected)))
    return selected


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def point_camera(camera, target):
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

aperture_material = material("External RF aperture", (0.78, 0.86, 0.88), roughness=0.28, alpha=0.48)
frame_material = material("Structural edge frame", (0.08, 0.12, 0.14), metallic=0.82, roughness=0.22)
faraday_material = material("Independent Faraday side wall", (0.23, 0.30, 0.31), metallic=0.72, roughness=0.3, alpha=0.38)
module_u_material = material("Shielded ADC ASIC U", (0.84, 0.39, 0.12), metallic=0.58, roughness=0.25)
module_v_material = material("Shielded ADC ASIC V", (0.12, 0.48, 0.67), metallic=0.58, roughness=0.25)
antenna_u_material = material("Orthogonal antenna U", (0.94, 0.28, 0.12), metallic=0.65, roughness=0.22)
antenna_v_material = material("Orthogonal antenna V", (0.08, 0.66, 0.88), metallic=0.65, roughness=0.22)
normal_material = material("Face normal", (0.28, 0.82, 0.40), roughness=0.3)
seam_material = material("RF gasket seam", (0.93, 0.67, 0.10), metallic=0.55, roughness=0.28)
power_material = material("Shielded DC power route", (0.96, 0.68, 0.08), metallic=0.38, roughness=0.3)
fibre_material = material("Optical fibre route", (0.72, 0.24, 0.82), roughness=0.24)
free_core_material = material("Reserved internal service core", (0.20, 0.62, 0.48), roughness=0.35, alpha=0.10)

_, _, modules = tetrahedral_modules(apex_depth_m=PYRAMID_HEIGHT_M)
selected_indices = select_contiguous_cluster(modules, CLUSTER_SIZE)
selected_modules = [modules[index] for index in selected_indices]

side_walls = []
outer_edges = {}
for module in selected_modules:
    face = tuple(Vector(point) for point in module["face"])
    center = Vector(module["center"])
    normal = Vector(module["normal"])
    tangent_u = Vector(module["tangent_u"])
    tangent_v = Vector(module["tangent_v"])
    apex = Vector(module["apex"])
    module_id = module["id"]

    aperture = triangle(f"{module_id} external open RF face", face, aperture_material)
    solidify = aperture.modifiers.new("Thin dielectric RF window", "SOLIDIFY")
    solidify.thickness = 0.025

    for start, end in zip(face, face[1:] + face[:1]):
        edge_key = face_edge_key(start, end)
        edge_record = outer_edges.setdefault(edge_key, {"start": start, "end": end, "apices": []})
        edge_record["apices"].append(apex)
        side_walls.append((module_id, start, end, apex))

    antenna_plane = center + normal * 0.16
    element_45 = (tangent_u + tangent_v).normalized()
    element_135 = (-tangent_u + tangent_v).normalized()
    cylinder_between(f"{module_id} VHF element at 45 degrees", antenna_plane - element_45 * 0.46, antenna_plane + element_45 * 0.46, 0.022, antenna_u_material)
    cylinder_between(f"{module_id} UHF element at 135 degrees", antenna_plane - element_135 * 0.46, antenna_plane + element_135 * 0.46, 0.022, antenna_v_material)
    cylinder_between(f"{module_id} sealed feedthrough", center - normal * 0.12, antenna_plane, 0.035, seam_material)

    electronics_center = center - normal * 0.28
    oriented_box(
        f"{module_id} shielded ADC ASIC polarization U",
        electronics_center + tangent_u * 0.24,
        tangent_u,
        tangent_v,
        normal,
        (0.34, 0.22, 0.15),
        module_u_material,
    )
    oriented_box(
        f"{module_id} shielded ADC ASIC polarization V",
        electronics_center - tangent_u * 0.24,
        tangent_u,
        tangent_v,
        normal,
        (0.34, 0.22, 0.15),
        module_v_material,
    )

    vector_origin = center + normal * 0.28
    arrow(f"{module_id} tangent U", vector_origin, tangent_u, antenna_u_material)
    arrow(f"{module_id} tangent V", vector_origin, tangent_v, antenna_v_material)
    arrow(f"{module_id} outward normal", vector_origin, normal, normal_material, 0.48)

for wall_index, (module_id, start, end, apex) in enumerate(side_walls):
    wall = triangle(f"{module_id} independent Faraday side wall {wall_index:02d}", (start, end, apex), faraday_material)
    solidify = wall.modifiers.new("Conductive wall thickness", "SOLIDIFY")
    solidify.thickness = 0.012
    wire = wall.modifiers.new("Faraday mesh visualization", "WIREFRAME")
    wire.thickness = 0.008

for edge_index, edge_record in enumerate(outer_edges.values()):
    start, end = edge_record["start"], edge_record["end"]
    cylinder_between(f"Outer structural seam rail {edge_index:02d}", start, end, 0.032, frame_material)
    cylinder_between(f"Conductive RF gasket {edge_index:02d}", Vector(start) * 0.985, Vector(end) * 0.985, 0.015, seam_material)
    if len(edge_record["apices"]) == 2:
        apex_a, apex_b = edge_record["apices"]
        channel_axis = (apex_b - apex_a).normalized()
        channel_start = (Vector(start) + Vector(end)) / 2.0
        channel_end = (apex_a + apex_b) / 2.0
        cylinder_between(
            f"Inter-cell shielded DC route {edge_index:02d}",
            channel_start + channel_axis * 0.035,
            channel_end + channel_axis * 0.035,
            0.018,
            power_material,
            12,
        )
        cylinder_between(
            f"Inter-cell optical fibre route {edge_index:02d}",
            channel_start - channel_axis * 0.035,
            channel_end - channel_axis * 0.035,
            0.014,
            fibre_material,
            12,
        )

minimum_free_core_radius = min(Vector(module["center"]).dot(Vector(module["normal"])) for module in modules) - PYRAMID_HEIGHT_M
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=minimum_free_core_radius, location=(0.0, 0.0, 0.0))
free_core = bpy.context.object
free_core.name = f"Reserved internal service core radius {minimum_free_core_radius:.3f} m"
free_core.data.materials.append(free_core_material)
core_wire = free_core.modifiers.new("Internal clearance envelope", "WIREFRAME")
core_wire.thickness = 0.008

cluster_center = sum((Vector(module["center"]) for module in selected_modules), Vector()) / len(selected_modules)
view_direction = cluster_center.normalized()
bpy.ops.object.camera_add(location=cluster_center + view_direction * 8.2 + Vector((0.5, -1.2, 1.1)))
camera = bpy.context.object
camera.name = "Tetrahedral face cluster camera"
camera.data.lens = 53
point_camera(camera, cluster_center * 0.72)
bpy.context.scene.camera = camera

bpy.ops.object.light_add(type="AREA", location=cluster_center + view_direction * 5.0 + Vector((1.0, -2.0, 3.0)))
key_light = bpy.context.object
key_light.name = "Key area light"
key_light.data.energy = 1100
key_light.data.shape = "DISK"
key_light.data.size = 5.0
point_camera(key_light, cluster_center)
bpy.ops.object.light_add(type="AREA", location=cluster_center - view_direction * 2.0 + Vector((-2.0, 2.0, 1.0)))
fill_light = bpy.context.object
fill_light.name = "Interior fill light"
fill_light.data.energy = 650
fill_light.data.size = 4.0
point_camera(fill_light, cluster_center * 0.45)

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1200
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = OUTPUT
scene.render.film_transparent = False
scene.world.color = (0.025, 0.032, 0.036)
scene.view_settings.look = "Medium High Contrast"

bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUTPUT)
bpy.ops.render.render(write_still=True)
print(f"Selected contiguous modules: {', '.join(module['id'] for module in selected_modules)}")
print(f"Pyramid normal height: {PYRAMID_HEIGHT_M:.3f} m")
print(f"Reserved free-core radius: {minimum_free_core_radius:.3f} m")
print(f"Wrote {BLEND_OUTPUT}")
print(f"Wrote {OUTPUT}")
