"""Extrai malhas TOPODATA locais, com altitude real, para a cena Blender."""
import argparse, json
from pathlib import Path
from osgeo import gdal

def tile_for(root, lon, lat):
    for path in sorted(root.glob("*.tif")):
        dataset=gdal.Open(str(path)); transform=dataset.GetGeoTransform(); width,height=dataset.RasterXSize,dataset.RasterYSize
        if transform[0] <= lon <= transform[0]+width*transform[1] and transform[3]+height*transform[5] <= lat <= transform[3]: return dataset,path
    raise ValueError(f"no TOPODATA tile covers {lon}, {lat}")

def build(selection, terrain_root, output, size=160, step=2):
    sites=[]
    for site in json.loads(selection.read_text(encoding="utf-8"))["selected_sites"]:
        dataset,path=tile_for(terrain_root,site["longitude"],site["latitude"]); transform=dataset.GetGeoTransform(); col=int((site["longitude"]-transform[0])/transform[1]); row=int((site["latitude"]-transform[3])/transform[5]); half=size//2; values=dataset.GetRasterBand(1).ReadAsArray(col-half,row-half,size,size)
        vertices=[]
        for y in range(0,size,step):
            for x in range(0,size,step): vertices.append([transform[0]+(col-half+x)*transform[1],transform[3]+(row-half+y)*transform[5],float(values[y,x])])
        sites.append({"name":site["name"],"tile":path.name,"width":size//step,"height":size//step,"vertices":vertices})
    output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps({"schema_version":1,"sites":sites,"semantics":"TOPODATA local DEM meshes projected onto curved Earth; vertical exaggeration is visual only"}),encoding="utf-8")

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--selection",type=Path,required=True);p.add_argument("--terrain-root",type=Path,required=True);p.add_argument("--output",type=Path,required=True);p.add_argument("--size",type=int,default=160);p.add_argument("--step",type=int,default=2);a=p.parse_args();build(a.selection,a.terrain_root,a.output,a.size,a.step)
