"""Monta e renderiza uma cena Blender da Terra curva e três sítios candidatos."""
import argparse, json, math, sys
from pathlib import Path

import bpy
from mathutils import Vector

EARTH_RADIUS_UNITS = 25.0

def position(latitude, longitude, elevation_m):
    lat, lon = math.radians(latitude), math.radians(longitude)
    radius = EARTH_RADIUS_UNITS + elevation_m / 120000.0
    return Vector((radius * math.cos(lat) * math.cos(lon), radius * math.cos(lat) * math.sin(lon), radius * math.sin(lat)))

def material(name, color, metallic=0.0):
    item = bpy.data.materials.new(name); item.diffuse_color = (*color, 1); item.metallic = metallic; item.roughness = 0.55; return item

def geo_position(longitude, latitude, offset=.03): return position(latitude, longitude, offset * 120000)
def add_curve(points, name, color):
    curve=bpy.data.curves.new(name,"CURVE"); curve.dimensions="3D"; curve.bevel_depth=.012; spline=curve.splines.new("POLY"); spline.points.add(len(points)-1)
    for point, coordinate in zip(spline.points,points): point.co=(*geo_position(*coordinate),1)
    obj=bpy.data.objects.new(name,curve); bpy.context.collection.objects.link(obj); obj.data.materials.append(material(name,color)); return obj
def add_overlays(overlays):
    for ring in overlays["state_boundaries"]: add_curve(ring,"State boundary",(.95,.75,.15))
    for ring in overlays["international_boundaries"]: add_curve(ring,"International boundary",(.96,.15,.12))
    elevations=[point["elevation_m"] for point in overlays["altitude_samples"]]; low,high=min(elevations),max(elevations)
    for point in overlays["altitude_samples"]:
        t=(point["elevation_m"]-low)/max(1,high-low); color=(t,.08,1-t)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.045,location=geo_position(point["longitude"],point["latitude"],.08)); bpy.context.object.data.materials.append(material("Altitude heat",color))
def add_terrain(terrain):
    for site in terrain["sites"]:
        vertices=[position(lat,lon,elevation*2) for lon,lat,elevation in site["vertices"]]; width,height=site["width"],site["height"]
        faces=[(y*width+x,y*width+x+1,(y+1)*width+x+1,(y+1)*width+x) for y in range(height-1) for x in range(width-1)]
        mesh=bpy.data.meshes.new(f"TOPODATA | {site['name']}"); mesh.from_pydata(vertices,[],faces); obj=bpy.data.objects.new(f"TOPODATA terrain | {site['name']}",mesh); bpy.context.collection.objects.link(obj); obj.data.materials.append(material("TOPODATA terrain",(.20,.36,.12)))

def add_radome(site, earth):
    point = position(site["latitude"], site["longitude"], site["terrain_elevation_m"]); normal = point.normalized()
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.24, location=point + normal * 0.20)
    dome = bpy.context.object; dome.name = f"RADOME | {site['name']}"; dome.data.materials.append(material("Radome white", (0.92, .94, .96)))
    dome.rotation_mode = "QUATERNION"; dome.rotation_quaternion = normal.to_track_quat("Z", "Y")
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=.055, depth=.42, location=point + normal * .05)
    mast = bpy.context.object; mast.name = f"Mast | {site['name']}"; mast.data.materials.append(material("Mast", (.12,.16,.18), .7)); mast.rotation_mode="QUATERNION"; mast.rotation_quaternion=normal.to_track_quat("Z","Y")
    bpy.ops.object.text_add(location=point + normal * .55); label=bpy.context.object; label.name=f"Label | {site['name']}"; label.data.body=f"{site['name']}\\n{site['terrain_elevation_m']:.0f} m | incidências: {site['geometric_illuminator_incidence_count']}"; label.data.align_x="CENTER"; label.data.size=.22; label.data.materials.append(material("Label", (1,.82,.2))); label.rotation_mode="QUATERNION"; label.rotation_quaternion=normal.to_track_quat("Z","Y")

def build(selection, overlays, terrain, blend, render):
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=EARTH_RADIUS_UNITS, location=(0,0,0)); earth=bpy.context.object; earth.name="Earth | spherical topographic context"; earth.data.materials.append(material("Earth", (.055,.18,.09)))
    add_overlays(overlays); add_terrain(terrain); site_points = [position(site["latitude"], site["longitude"], site["terrain_elevation_m"]*2) for site in selection["selected_sites"]]
    for site in selection["selected_sites"]: add_radome(site, earth)
    bpy.ops.object.light_add(type="SUN", location=(0,0,0)); bpy.context.object.data.energy=2.2; bpy.context.object.rotation_euler=(math.radians(25), math.radians(-20), math.radians(-30))
    bpy.ops.object.light_add(type="AREA", location=(35,-35,30)); bpy.context.object.data.energy=900; bpy.context.object.data.shape="DISK"; bpy.context.object.data.size=25
    target = sum(site_points, Vector()) / len(site_points); outward = target.normalized()
    bpy.ops.object.camera_add(location=outward * 55 + Vector((7, -7, 5))); camera=bpy.context.object; bpy.context.scene.camera=camera; direction=target-camera.location; camera.rotation_euler=direction.to_track_quat("-Z","Y").to_euler(); camera.data.lens=52
    scene=bpy.context.scene; scene.render.engine="BLENDER_EEVEE"; scene.render.resolution_x=1600; scene.render.resolution_y=1000; scene.render.resolution_percentage=100; scene.render.image_settings.file_format="PNG"; scene.render.filepath=str(render); scene.world.color=(.008,.012,.025)
    bpy.ops.wm.save_as_mainfile(filepath=str(blend)); bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--selection",type=Path,required=True); parser.add_argument("--overlays",type=Path,required=True); parser.add_argument("--terrain",type=Path,required=True); parser.add_argument("--blend",type=Path,required=True); parser.add_argument("--render",type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index("--") + 1:]); args.blend=args.blend.resolve(); args.render=args.render.resolve(); args.selection=args.selection.resolve(); args.overlays=args.overlays.resolve(); args.terrain=args.terrain.resolve(); args.blend.parent.mkdir(parents=True,exist_ok=True); args.render.parent.mkdir(parents=True,exist_ok=True); build(json.loads(args.selection.read_text(encoding="utf-8")),json.loads(args.overlays.read_text(encoding="utf-8")),json.loads(args.terrain.read_text(encoding="utf-8")),args.blend,args.render)
