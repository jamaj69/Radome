import bpy
import math
import sys
from pathlib import Path
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_paths import build_output

OUTPUT = str(build_output("fig15_aircraft_two_radomes_100km.png"))
BLEND = str(build_output("radome_two_nodes_aircraft_100km.blend"))

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

def mat(name, color, metallic=0.0, roughness=0.5, alpha=1.0):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, alpha)
    material.use_nodes = True
    shader = material.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1.0)
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Alpha"].default_value = alpha
    if alpha < 1:
        material.blend_method = "BLEND"
    return material

ground_mat = mat("Terrain", (0.68, 0.72, 0.74), roughness=0.9)
radome_mat = mat("Radome shell", (0.18, 0.58, 0.82), roughness=0.3, alpha=0.48)
frame_mat = mat("Radome frame", (0.03, 0.18, 0.30), metallic=0.25, roughness=0.3)
concrete_mat = mat("Concrete base", (0.58, 0.61, 0.63), roughness=0.85)
aircraft_mat = mat("Aircraft", (0.92, 0.63, 0.16), metallic=0.25, roughness=0.28)
signal_mat = mat("RF signal", (0.95, 0.55, 0.08), roughness=0.25)
line_a_mat = mat("Node A line", (0.2, 0.75, 0.95), roughness=0.3)
line_b_mat = mat("Node B line", (0.95, 0.35, 0.3), roughness=0.3)

def cylinder(name, a, b, radius, material, vertices=16):
    a, b = Vector(a), Vector(b)
    direction = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=direction.length, location=(a + b) / 2)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = direction.to_track_quat("Z", "Y")
    return obj

def radome(name, location, color):
    # Stations are enlarged symbolically so they remain legible at 100 km scale.
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=7.5, location=location)
    shell = bpy.context.object
    shell.name = name + " transparent radome"
    shell.data.materials.append(color)
    wire = shell.modifiers.new("Geodesic frame", "WIREFRAME")
    wire.thickness = 0.045
    shell.data.materials.append(frame_mat)
    wire.material_offset = 1
    bpy.ops.mesh.primitive_cube_add(size=1, location=(location[0], location[1], location[2] - 7.7))
    base = bpy.context.object
    base.name = name + " concrete base"
    base.dimensions = (12.0, 12.0, 3.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    base.data.materials.append(concrete_mat)
    return Vector(location)

# Conceptual scene scale: one Blender unit represents one kilometre.
node_a = radome("NODE A", (-50, 0, 2.2), radome_mat)
node_b = radome("NODE B", (50, 0, 2.2), radome_mat)
cylinder("100 km baseline", (-50, 0, -0.72), (50, 0, -0.72), 0.16, frame_mat)

# Aircraft at altitude and offset from the baseline.
aircraft = Vector((0, 18, 18))
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=1.25, location=aircraft)
bpy.context.object.name = "Aircraft transmitter"
bpy.context.object.scale = (3.0, 0.8, 0.35)
bpy.context.object.data.materials.append(aircraft_mat)
# wings and tail.
cylinder("Aircraft wing", aircraft + Vector((-4.0, 0, 0)), aircraft + Vector((4.0, 0, 0)), 0.28, aircraft_mat)
cylinder("Aircraft longitudinal body", aircraft + Vector((0, -3.0, 0)), aircraft + Vector((0, 3.0, 0)), 0.34, aircraft_mat)

# Signal paths and angular observation cones.
cylinder("Signal path A", aircraft, node_a + Vector((0, 0, 1.2)), 0.22, line_a_mat)
cylinder("Signal path B", aircraft, node_b + Vector((0, 0, 1.2)), 0.22, line_b_mat)

# Observation cones as transparent triangular surfaces.
def cone_surface(name, node, target, width, material):
    direction = (target - node).normalized()
    side = direction.cross(Vector((0, 0, 1)))
    if side.length < 0.1:
        side = direction.cross(Vector((0, 1, 0)))
    side.normalize()
    p1 = target + side * width
    p2 = target - side * width
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata([node, p1, p2], [], [(0, 1, 2)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
cone_surface("AOA cone Node A", node_a, aircraft, 5.0, line_a_mat)
cone_surface("AOA cone Node B", node_b, aircraft, 5.0, line_b_mat)

# Ground plane.
bpy.ops.mesh.primitive_plane_add(size=180, location=(0, 0, -1.5))
plane = bpy.context.object
plane.name = "Terrain plane"
plane.data.materials.append(ground_mat)

# Lighting and camera.
bpy.ops.object.light_add(type="AREA", location=(0, -25, 85))
key = bpy.context.object
key.data.energy = 4800
key.data.size = 35
key.rotation_euler = (math.radians(18), 0, 0)
bpy.ops.object.light_add(type="AREA", location=(45, 15, 28))
fill = bpy.context.object
fill.data.energy = 2800
fill.data.size = 25
fill.rotation_euler = (math.radians(35), 0, math.radians(130))

def point_camera(camera, target):
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()

bpy.ops.object.camera_add(location=(0, -135, 82))
camera = bpy.context.object
camera.name = "Two-node validation camera"
point_camera(camera, (0, 5, 5))
camera.data.type = "ORTHO"
camera.data.ortho_scale = 116
bpy.context.scene.camera = camera

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1600
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = OUTPUT
scene.render.film_transparent = False
scene.world.color = (0.72, 0.78, 0.82)
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.72, 0.78, 0.82, 1.0)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.8
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"
scene.view_settings.exposure = 1.0
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
bpy.ops.render.render(write_still=True)
