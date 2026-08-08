import bpy
import math
from mathutils import Vector

OUTPUT = "/home/jamaj/src/Radome/projeto/figures/fig13_radome_blender.png"
INTERNAL_OUTPUT = "/home/jamaj/src/Radome/projeto/figures/fig14_radome_interior_blender.png"

# Reset scene.
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    pass

# Materials.
def material(name, color, metallic=0.0, roughness=0.45, alpha=1.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, alpha)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Alpha"].default_value = alpha
    if alpha < 1.0:
        bsdf.inputs["Transmission"].default_value = 0.08
        mat.blend_method = "BLEND"
        mat.use_screen_refraction = True
        mat.show_transparent_back = True
        mat.node_tree.nodes.get("Principled BSDF").inputs["IOR"].default_value = 1.45
    return mat

shell_mat = material("Radome dielectric shell", (0.22, 0.52, 0.68), metallic=0.0, roughness=0.35, alpha=0.18)
frame_mat = material("Geodesic frame", (0.10, 0.28, 0.40), metallic=0.35, roughness=0.3)
face_mat = material("Highlighted RF face", (0.92, 0.42, 0.12), metallic=0.05, roughness=0.35, alpha=0.74)
dielectric_mat = material("Dielectric layer", (0.72, 0.83, 0.88), roughness=0.38, alpha=0.82)
core_mat = material("Honeycomb core", (0.95, 0.73, 0.36), roughness=0.55)
shield_mat = material("Shielded RF module", (0.18, 0.34, 0.42), metallic=0.65, roughness=0.28)
internal_module_mat = material("Internal band module highlight", (0.72, 0.28, 0.08), metallic=0.35, roughness=0.3)
board_mat = material("RF PCB", (0.08, 0.33, 0.20), roughness=0.4)
ffasic_mat = material("FFASIC central module", (0.38, 0.25, 0.62), metallic=0.3, roughness=0.28)
yagi_mat = material("Yagi aluminium", (0.67, 0.70, 0.72), metallic=0.82, roughness=0.2)
yagi_gold = material("Yagi bracket", (0.82, 0.50, 0.06), metallic=0.65, roughness=0.25)
yagi_cross_mat = material("Crossed Yagi aluminium", (0.32, 0.58, 0.82), metallic=0.78, roughness=0.22)
mast_mat = material("Mast", (0.20, 0.22, 0.24), metallic=0.7, roughness=0.25)
white_mat = material("White", (0.92, 0.94, 0.95), roughness=0.45)
base_mat = material("Concrete base", (0.42, 0.45, 0.47), roughness=0.88)
opening_mat = material("Access opening", (0.015, 0.02, 0.025), roughness=0.5)
warning_mat = material("Access frame", (0.82, 0.42, 0.06), metallic=0.3, roughness=0.35)

# Geometry helpers.
def cylinder_between(name, a, b, radius, mat, vertices=20):
    a, b = Vector(a), Vector(b)
    direction = b - a
    midpoint = (a + b) / 2
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=direction.length, location=midpoint)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = direction.to_track_quat("Z", "Y")
    return obj

def triangle_mesh(name, points, mat, bevel=0.0):
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(points, [], [(0, 1, 2)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    if bevel:
        mod = obj.modifiers.new("Edge bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    return obj

def text_obj(body, location, size=0.20, color_mat=white_mat, align="CENTER"):
    curve = bpy.data.curves.new(body, "FONT")
    curve.body = body
    curve.align_x = align
    curve.size = size
    curve.extrude = 0.004
    obj = bpy.data.objects.new(body, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(color_mat)
    # Keep labels approximately facing the camera through a track quaternion later.
    return obj

# Radome shell: equator as the mid-plane and lower cut at latitude 35 S.
shell_center = Vector((-3.7, 0.0, 0.0))
radius = 2.75
segments = 24
rings = 7
lower_cut_latitude = math.radians(-35.0)
cut_polar_angle = math.pi / 2.0 - lower_cut_latitude
shell_vertices = [shell_center + Vector((0, 0, radius))]
shell_faces = []
for ring in range(1, rings + 1):
    theta = cut_polar_angle * ring / rings
    for segment in range(segments):
        phi = 2.0 * math.pi * segment / segments
        shell_vertices.append(shell_center + Vector((radius * math.sin(theta) * math.cos(phi), radius * math.sin(theta) * math.sin(phi), radius * math.cos(theta))))
for segment in range(segments):
    shell_faces.append((0, 1 + segment, 1 + (segment + 1) % segments))
for ring in range(rings - 1):
    start = 1 + ring * segments
    next_start = start + segments
    for segment in range(segments):
        a = start + segment
        b = start + (segment + 1) % segments
        c = next_start + (segment + 1) % segments
        d = next_start + segment
        shell_faces.extend([(a, b, c), (a, c, d)])
shell_mesh = bpy.data.meshes.new("Upper radome cut at latitude 35 S")
shell_mesh.from_pydata(shell_vertices, [], shell_faces)
shell_mesh.update()
shell = bpy.data.objects.new("Transparent upper geodesic radome shell", shell_mesh)
bpy.context.collection.objects.link(shell)
shell.data.materials.append(shell_mat)
wire = shell.modifiers.new("Geodesic frame", "WIREFRAME")
wire.thickness = 0.012
wire.material_offset = 0
shell.data.materials.append(frame_mat)

# Supporting reinforced-concrete cuboid and visible maintenance/access opening.
cut_height = radius * math.sin(lower_cut_latitude)
base_width = 4.0
base_depth = 4.0
base_height = 3.0
bpy.ops.mesh.primitive_cube_add(size=1, location=shell_center + Vector((0, 0, cut_height - base_height / 2)))
base = bpy.context.object
base.name = "Reinforced concrete radome base 4x4x2 m"
base.dimensions = (base_width, base_depth, base_height)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
base.data.materials.append(base_mat)
base_bevel = base.modifiers.new("Concrete edge bevel", "BEVEL")
base_bevel.width = 0.10
base_bevel.segments = 3
bpy.ops.mesh.primitive_cube_add(size=1, location=shell_center + Vector((0, -base_depth / 2 - 0.02, cut_height - base_height + 0.85)))
opening = bpy.context.object
opening.name = "Concrete base interior access opening"
opening.dimensions = (1.70, 0.08, 2.20)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
opening.data.materials.append(opening_mat)
for x in (-0.92, 0.92):
    cylinder_between("Access opening vertical frame", shell_center + Vector((x, -base_depth / 2 - 0.08, cut_height - base_height + 0.05)), shell_center + Vector((x, -base_depth / 2 - 0.08, cut_height - base_height + 2.25)), 0.035, warning_mat)
cylinder_between("Access opening top frame", shell_center + Vector((-0.92, -base_depth / 2 - 0.08, cut_height - base_height + 2.25)), shell_center + Vector((0.92, -base_depth / 2 - 0.08, cut_height - base_height + 2.25)), 0.035, warning_mat)

# Highlighted face on right/front of radome.
face_center = Vector((-1.22, -1.05, 1.25))
face_normal = (face_center - shell_center).normalized()
edge_a = Vector((-1.32, -1.55, 1.45))
edge_b = Vector((-1.25, -0.40, 1.48))
edge_c = Vector((-1.05, -1.00, 2.45))
triangle_mesh("Highlighted radome face", [edge_a, edge_b, edge_c], face_mat, 0.015)

# Exploded triangular pyramid: the triangular face is on the outer surface
# (x=0) and the apex points inward (-X), into the radome volume.
offset = Vector((1.55, 0.0, 0.4))
base = [offset + Vector((0.0, -1.20, -0.85)), offset + Vector((0.0, 1.20, -0.85)), offset + Vector((0.0, 0.0, 1.22))]
apex = offset + Vector((-1.35, 0.0, 0.0))
for i in range(3):
    triangle_mesh("Pyramid structural side", [base[i], base[(i + 1) % 3], apex], dielectric_mat, 0.025)
triangle_mesh("Outer triangular RF face", base, face_mat, 0.025)

# Exploded layers just behind the external face, separated toward the interior (-X).
for index, (x, mat, name) in enumerate([(0.18, dielectric_mat, "Dielectric skin and honeycomb"), (0.42, board_mat, "RF aperture and PCB"), (0.68, shield_mat, "Shielded ADC ASIC band modules")]):
    x = -x
    scale = 0.72
    layer = [offset + Vector((x, p.y * scale, p.z * scale)) for p in [Vector((0, -1.2, -0.85)), Vector((0, 1.2, -0.85)), Vector((0, 0, 1.22))]]
    triangle_mesh(name, layer, mat, 0.015)

# FFASIC central face module: box behind the band layers.
bpy.ops.mesh.primitive_cube_add(size=1, location=offset + Vector((0.93, 0.0, 0.0)))
ffasic = bpy.context.object
ffasic.name = "FFASIC central face module"
ffasic.dimensions = (0.28, 0.62, 0.62)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
ffasic.data.materials.append(ffasic_mat)

# Internal joints: structural triangular frame and node plates.
for a, b in [(base[0], base[1]), (base[1], base[2]), (base[2], base[0])]:
    cylinder_between("Internal sealed structural joint", a + Vector((0.06, 0, 0)), b + Vector((0.06, 0, 0)), 0.035, frame_mat)
for point in base:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.09, location=point + Vector((0.08, 0, 0)))
    bpy.context.object.name = "Internal node plate"
    bpy.context.object.data.materials.append(frame_mat)

# External crossed Yagis: both booms continue from the same apex-support axis.
# Their transverse elements occupy orthogonal planes, producing two distinct
# linear polarizations while preserving independent band dimensions.
yagi_x = offset.x + 0.32
mast_base = apex
mast_top = Vector((yagi_x, 0.0, 0.0))
cylinder_between("Antenna support from inward pyramid apex", mast_base, mast_top, 0.065, mast_mat)
boom_end = Vector((offset.x + 2.75, 0.0, 0.0))
def crossed_yagi(prefix, color_mat, element_axis, offset_y=0.0, offset_z=0.0, scale=1.0):
    boom_start = Vector((yagi_x, offset_y, offset_z))
    cylinder_between(prefix + " boom", boom_start, boom_end + Vector((0, offset_y, offset_z)), 0.04, color_mat)
    lengths = [(0.62, 1.00), (1.03, 0.86), (1.43, 0.74), (1.83, 0.62), (2.23, 0.52), (2.62, 0.45)]
    for x, half in lengths:
        x_position = offset.x + x
        half *= scale
        if element_axis == "y":
            a = Vector((x_position, offset_y - half, offset_z))
            b = Vector((x_position, offset_y + half, offset_z))
        else:
            a = Vector((x_position, offset_y, offset_z - half))
            b = Vector((x_position, offset_y, offset_z + half))
        cylinder_between(prefix + " transverse element", a, b, 0.022, color_mat)
    loop_x = offset.x + 1.35
    half = 0.58 * scale
    if element_axis == "y":
        loop_points = [Vector((loop_x, offset_y - half, offset_z - 0.12)), Vector((loop_x, offset_y + half, offset_z - 0.12)), Vector((loop_x, offset_y + half, offset_z + 0.12)), Vector((loop_x, offset_y - half, offset_z + 0.12))]
    else:
        loop_points = [Vector((loop_x, offset_y - 0.12, offset_z - half)), Vector((loop_x, offset_y - 0.12, offset_z + half)), Vector((loop_x, offset_y + 0.12, offset_z + half)), Vector((loop_x, offset_y + 0.12, offset_z - half))]
    for start, end in zip(loop_points, loop_points[1:] + loop_points[:1]):
        cylinder_between(prefix + " folded driven element", start, end, 0.032, yagi_gold)

crossed_yagi("Yagi A VHF-low polarization-Y", yagi_mat, "y", offset_z=0.10, scale=1.0)
crossed_yagi("Yagi B VHF-high polarization-Z", yagi_cross_mat, "z", offset_y=0.10, scale=0.62)
# Shared feed bracket at the external face interface.
cylinder_between("Crossed Yagi feed bracket", Vector((yagi_x, 0, 0)), Vector((offset.x + 1.38, 0, 0)), 0.035, yagi_gold)
bpy.ops.mesh.primitive_cube_add(size=1, location=offset + Vector((1.37, 0, -0.85)))
bracket = bpy.context.object
bracket.name = "Yagi base bracket"
bracket.dimensions = (0.18, 0.38, 0.22)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bracket.data.materials.append(yagi_gold)

# Fibres and power leaving FFASIC.
central = offset + Vector((0.93, 0.0, 0.0))
cylinder_between("Optical fibre", central, central + Vector((0.45, -1.3, -0.8)), 0.022, material("Fibre", (0.08, 0.55, 0.48), metallic=0.1, roughness=0.3))
cylinder_between("DC power", central, central + Vector((0.45, 1.3, -0.75)), 0.028, material("DC", (0.8, 0.35, 0.08), metallic=0.1, roughness=0.35))

# Deliberately omit world-space labels and schematic interior ribs/modules from
# the perspective render. The technical callouts belong in separate diagrams.

# Ground plane and lighting.
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, cut_height - base_height - 0.22))
plane = bpy.context.object
plane.name = "Ground"
plane.data.materials.append(material("Ground material", (0.025, 0.04, 0.055), metallic=0.0, roughness=0.55))

bpy.ops.object.light_add(type="AREA", location=(1, -6, 10))
key = bpy.context.object
key.name = "Key light"
key.data.energy = 1200
key.data.shape = "DISK"
key.data.size = 6
key.rotation_euler = (math.radians(20), 0, math.radians(10))

bpy.ops.object.light_add(type="AREA", location=(-6, 4, 5))
fill = bpy.context.object
fill.data.energy = 850
fill.data.size = 5
fill.rotation_euler = (math.radians(65), 0, math.radians(-55))

bpy.ops.object.light_add(type="AREA", location=(7, 2, 5))
rim = bpy.context.object
rim.data.energy = 950
rim.data.size = 4
rim.rotation_euler = (math.radians(55), 0, math.radians(125))

# Camera.
def point_camera(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()

bpy.ops.object.camera_add(location=(12.5, -16.5, 7.0))
camera = bpy.context.object
camera.name = "Technical camera"
point_camera(camera, (0.3, 0.0, -0.65))
camera.data.lens = 52
bpy.context.scene.camera = camera

scene = bpy.context.scene

# Use NVIDIA CUDA explicitly for Cycles rendering.
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1280
scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = OUTPUT
scene.render.film_transparent = False
scene.world.color = (0.008, 0.015, 0.025)
scene.view_settings.view_transform = "Filmic"
scene.view_settings.look = "Medium High Contrast"
scene.render.resolution_percentage = 100
bpy.ops.wm.save_as_mainfile(filepath="/home/jamaj/src/Radome/projeto/figures/radome_v1_3d.blend")
bpy.ops.render.render(write_still=True)

# Second render: camera physically inside the transparent shell, looking toward
# the internal core and the mounted face modules.
bpy.ops.object.camera_add(location=(-4.85, -0.65, 2.75))
internal_camera = bpy.context.object
internal_camera.name = "Internal inspection camera"
point_camera(internal_camera, (-2.55, 2.15, 2.5))
internal_camera.data.lens = 26
scene.camera = internal_camera
scene.render.resolution_x = 1400
scene.render.resolution_y = 900
scene.render.filepath = INTERNAL_OUTPUT
# Keep the shell context visible without allowing it to occlude the interior.
shell_mat.diffuse_color = (0.22, 0.52, 0.68, 0.045)
shell_mat.node_tree.nodes.get("Principled BSDF").inputs["Alpha"].default_value = 0.045
for obj in bpy.data.objects:
    if obj.name.startswith("Internal service ring"):
        obj.hide_render = True
bpy.ops.render.render(write_still=True)
