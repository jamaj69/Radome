import bpy
import math
from mathutils import Vector

OUTPUT = "/home/jamaj/src/Radome/projeto/figures/fig15_aircraft_two_radomes_100km.png"
BLEND = "/home/jamaj/src/Radome/projeto/figures/radome_two_nodes_aircraft_100km.blend"

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

ground_mat = mat("Terrain", (0.07, 0.11, 0.13), roughness=0.9)
radome_mat = mat("Radome shell", (0.2, 0.55, 0.72), roughness=0.35, alpha=0.38)
frame_mat = mat("Radome frame", (0.08, 0.25, 0.35), metallic=0.45, roughness=0.3)
concrete_mat = mat("Concrete base", (0.35, 0.38, 0.4), roughness=0.85)
aircraft_mat = mat("Aircraft", (0.72, 0.76, 0.8), metallic=0.45, roughness=0.28)
signal_mat = mat("RF signal", (0.95, 0.55, 0.08), roughness=0.25)
line_a_mat = mat("Node A line", (0.2, 0.75, 0.95), roughness=0.3)
line_b_mat = mat("Node B line", (0.95, 0.35, 0.3), roughness=0.3)
panel_mat = mat("Panel", (0.12, 0.22, 0.30), metallic=0.2, roughness=0.45)
white_mat = mat("Text", (0.9, 0.95, 1.0), roughness=0.4)
white_shader = white_mat.node_tree.nodes.get("Principled BSDF")
white_shader.inputs["Emission"].default_value = (0.9, 0.95, 1.0, 1.0)
white_shader.inputs["Emission Strength"].default_value = 2.5

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

def text(body, location, size=0.25, material=white_mat, align="CENTER"):
    curve = bpy.data.curves.new(body, "FONT")
    curve.body = body
    curve.align_x = align
    curve.size = size
    curve.extrude = 0.005
    obj = bpy.data.objects.new(body, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(material)
    return obj

def radome(name, location, color):
    # Stations are enlarged symbolically so they remain legible at 100 km scale.
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=5.0, location=location)
    shell = bpy.context.object
    shell.name = name + " transparent radome"
    shell.data.materials.append(color)
    wire = shell.modifiers.new("Geodesic frame", "WIREFRAME")
    wire.thickness = 0.018
    shell.data.materials.append(frame_mat)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(location[0], location[1], location[2] - 5.15))
    base = bpy.context.object
    base.name = name + " concrete base"
    base.dimensions = (8.0, 8.0, 2.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    base.data.materials.append(concrete_mat)
    text(name, (location[0], location[1] - 6.2, location[2] + 6.0), 0.42, white_mat)
    return Vector(location)

# Conceptual scene scale: one Blender unit represents one kilometre.
node_a = radome("NODE A", (-50, 0, 2.2), radome_mat)
node_b = radome("NODE B", (50, 0, 2.2), radome_mat)
text("100 km baseline / linha de base", (0, 1.1, -1.3), 0.28, line_a_mat)
cylinder("100 km baseline", (-50, 0, -0.72), (50, 0, -0.72), 0.035, line_a_mat)

# Aircraft at altitude and offset from the baseline.
aircraft = Vector((0, 18, 18))
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=0.65, location=aircraft)
bpy.context.object.name = "Aircraft transmitter"
bpy.context.object.scale = (2.6, 0.65, 0.25)
bpy.context.object.data.materials.append(aircraft_mat)
# wings and tail.
cylinder("Aircraft wing", aircraft + Vector((-2.0, 0, 0)), aircraft + Vector((2.0, 0, 0)), 0.11, aircraft_mat)
cylinder("Aircraft longitudinal body", aircraft + Vector((0, -1.8, 0)), aircraft + Vector((0, 1.8, 0)), 0.14, aircraft_mat)
text("ADS-B aircraft / aeronave ADS-B", aircraft + Vector((0, 0, 1.4)), 0.28, white_mat)

# Signal paths and angular observation cones.
cylinder("Signal path A", aircraft, node_a + Vector((0, 0, 1.2)), 0.045, line_a_mat)
cylinder("Signal path B", aircraft, node_b + Vector((0, 0, 1.2)), 0.045, line_b_mat)
text("1090 MHz ADS-B / 1090ES\nP_A, AOA_A, t_A, f_DA", (-31, 10, 12), 0.22, line_a_mat)
text("1090 MHz ADS-B / 1090ES\nP_B, AOA_B, t_B, f_DB", (31, 10, 12), 0.22, line_b_mat)

# Observation cones as transparent triangular surfaces.
def cone_surface(name, node, target, width, material):
    direction = (target - node).normalized()
    side = direction.cross(Vector((0, 0, 1)))
    if side.length < 0.1:
        side = direction.cross(Vector((0, 1, 0)))
    side.normalize()
    p1 = node + side * width
    p2 = node - side * width
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata([node, p1, p2], [], [(0, 1, 2)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
cone_surface("AOA cone Node A", node_a, aircraft, 3.0, line_a_mat)
cone_surface("AOA cone Node B", node_b, aircraft, 3.0, line_b_mat)

# Measurement panel.
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -7.0, 7.5))
panel = bpy.context.object
panel.name = "Observable fusion panel"
panel.dimensions = (38, 0.25, 11.5)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
panel.data.materials.append(panel_mat)
text("ADS-B 1090ES PASSIVE MULTISTATIC CONSISTENCY CHECK", (0, -7.25, 10.8), 0.42, white_mat)
text("Received power: P_A / P_B", (-15.5, -7.3, 8.9), 0.38, line_a_mat, "LEFT")
text("Angles: AOA_A / AOA_B", (-15.5, -7.3, 8.1), 0.38, line_b_mat, "LEFT")
text("Time: TDOA = t_A - t_B", (-15.5, -7.3, 7.3), 0.38, white_mat, "LEFT")
text("Doppler: FDOA = f_DA - f_DB", (2.0, -7.3, 8.1), 0.38, white_mat, "LEFT")
text("Altitude/state: hypothesis + covariance", (2.0, -7.3, 7.3), 0.38, white_mat, "LEFT")
text("Result: consistency track, not blind truth validation", (0, -7.3, 6.25), 0.32, white_mat)
text("978 MHz UAT: contextual alternative, mainly US general aviation", (0, -7.3, 5.65), 0.25, white_mat)
text("Independent UHF TV / UHF TV independente: direct reference or bistatic illuminator", (0, -7.3, 5.05), 0.22, white_mat)

# Ground plane.
bpy.ops.mesh.primitive_plane_add(size=180, location=(0, 0, -1.5))
plane = bpy.context.object
plane.name = "Terrain plane"
plane.data.materials.append(ground_mat)

# Lighting and camera.
bpy.ops.object.light_add(type="AREA", location=(0, -20, 80))
key = bpy.context.object
key.data.energy = 3200
key.data.size = 35
key.rotation_euler = (math.radians(18), 0, 0)
bpy.ops.object.light_add(type="AREA", location=(45, 15, 28))
fill = bpy.context.object
fill.data.energy = 1800
fill.data.size = 25
fill.rotation_euler = (math.radians(35), 0, math.radians(130))

def point_camera(camera, target):
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()

bpy.ops.object.camera_add(location=(0, -120, 65))
camera = bpy.context.object
camera.name = "Two-node validation camera"
point_camera(camera, (0, 5, 7))
camera.data.type = "ORTHO"
camera.data.ortho_scale = 120
bpy.context.scene.camera = camera

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1600
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = OUTPUT
scene.render.film_transparent = False
scene.world.color = (0.055, 0.08, 0.10)
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.055, 0.08, 0.10, 1.0)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.45
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"
scene.view_settings.exposure = 1.5
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
bpy.ops.render.render(write_still=True)
