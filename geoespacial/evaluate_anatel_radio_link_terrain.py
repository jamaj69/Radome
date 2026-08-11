#!/usr/bin/env python3
"""Avalia terreno, curvatura e Fresnel dos candidatos sem criar arestas."""
from __future__ import annotations
import argparse,csv,gzip,json,math,os,tempfile
from collections import Counter,defaultdict
from pathlib import Path
from PIL import Image
from audit_anatel_spectrum import number
from build_candidate_graph import EARTH_RADIUS_M,tile_pixel
from build_canonical_smp import deterministic_gzip_csv,sha256_file

C=299_792_458.0
FIELDS=("candidate_id","link_family","service_fistel","rf_act_number","distance_km","minimum_reciprocal_frequency_mhz","antenna_height_a_m","antenna_height_b_m","terrain_samples","missing_samples","minimum_los_clearance_k1_m","minimum_fresnel60_clearance_k1_m","minimum_los_clearance_k4_3_m","minimum_fresnel60_clearance_k4_3_m","terrain_status_k1","terrain_status_k4_3","pairing_status","terrain_source","height_semantics")

class Terrarium:
 def __init__(self,root:Path,zoom:int):self.root=root;self.zoom=zoom;self.images={}
 def __call__(self,lat,lon):
  x,y,px,py=tile_pixel(lon,lat,self.zoom);path=self.root/str(self.zoom)/str(x)/f"{y}.png"
  if not path.is_file():return None
  if path not in self.images:self.images[path]=Image.open(path).convert("RGB")
  r,g,b=self.images[path].getpixel((px,py));return r*256+g+b/256-32768
 def close(self):
  for image in self.images.values():image.close()

def interpolate(a,b,f):
 lat1,lon1=map(math.radians,a);lat2,lon2=map(math.radians,b)
 v1=(math.cos(lat1)*math.cos(lon1),math.cos(lat1)*math.sin(lon1),math.sin(lat1));v2=(math.cos(lat2)*math.cos(lon2),math.cos(lat2)*math.sin(lon2),math.sin(lat2));omega=math.acos(max(-1,min(1,sum(x*y for x,y in zip(v1,v2)))))
 if omega==0:return a
 s=math.sin(omega);v=tuple(math.sin((1-f)*omega)/s*x+math.sin(f*omega)/s*y for x,y in zip(v1,v2));return math.degrees(math.atan2(v[2],math.hypot(v[0],v[1]))),math.degrees(math.atan2(v[1],v[0]))

def profile(a,b,distance_km,height_a,height_b,frequency_mhz,sampler,spacing_km=1.0,k=1.0):
 n=max(3,math.ceil(distance_km/spacing_km)+1);terrain=[sampler(*interpolate(a,b,i/(n-1))) for i in range(n)]
 missing=sum(x is None for x in terrain)
 if missing:return {"samples":n,"missing":missing,"los":None,"fresnel":None}
 top_a=terrain[0]+height_a;top_b=terrain[-1]+height_b;D=distance_km*1000;wavelength=C/(frequency_mhz*1e6);los=[];fresnel=[]
 for i,z in enumerate(terrain[1:-1],1):
  f=i/(n-1);d1=f*D;d2=D-d1;line=top_a+(top_b-top_a)*f;bulge=d1*d2/(2*EARTH_RADIUS_M*k);clear=line-z-bulge;r=math.sqrt(wavelength*d1*d2/D);los.append(clear);fresnel.append(clear-.6*r)
 return {"samples":n,"missing":0,"los":min(los),"fresnel":min(fresnel)}

def classify(result):
 if result["missing"]:return "terrain_missing"
 if result["fresnel"]>=0:return "fresnel60_clear"
 if result["los"]>=0:return "los_clear_fresnel_obstructed"
 return "terrain_or_curvature_obstructed"

def evaluate(geometry:Path,keys:Path,emissions:Path,cache:Path,output:Path,report:Path,zoom=8):
 selected={}
 with gzip.open(geometry,"rt",encoding="utf-8",newline="") as s:
  for r in csv.DictReader(s):
   if r["geometry_status"]=="azimuth_consistent_15deg":selected[(r["link_family"],r["service_fistel"],r["rf_act_number"])]=r
 rows={};groups=defaultdict(list)
 with gzip.open(keys,"rt",encoding="utf-8",newline="") as s:
  for r in csv.DictReader(s):
   k=(r["link_family"],r["service_fistel"],r["rf_act_number"])
   if k in selected:rows[r["source_row_number"]]=k
 with gzip.open(emissions,"rt",encoding="utf-8",newline="") as s:
  for r in csv.DictReader(s):
   k=rows.get(r["source_row_number"])
   if k:groups[k].append(r)
 terrain=Terrarium(cache,zoom);counts=Counter();counts43=Counter();output.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(prefix="link-terrain-",dir=output.parent) as d:
  staged=Path(d)/output.name
  with deterministic_gzip_csv(staged,FIELDS) as w:
   for k in sorted(selected):
    g=selected[k];a=tuple(map(float,g["coordinate_a"].split(",")));b=tuple(map(float,g["coordinate_b"].split(",")));by=defaultdict(lambda:{"tx":set(),"rx":set(),"height":[]})
    for r in groups[k]:
     coord=(number(r["latitude"]),number(r["longitude"]));freq=number(r["frequency_mhz"]);h=number(r["antenna_height_m"])
     if freq is not None:by[coord]["tx" if r["direction"]=="Transmissão" else "rx"].add(freq)
     if h is not None:by[coord]["height"].append(h)
    reciprocal=(by[a]["tx"]&by[b]["rx"])|(by[b]["tx"]&by[a]["rx"]);freq=min(reciprocal);ha=max(by[a]["height"] or [0]);hb=max(by[b]["height"] or [0]);dist=float(g["distance_km"])
    p1=profile(a,b,dist,ha,hb,freq,terrain,k=1);p43=profile(a,b,dist,ha,hb,freq,terrain,k=4/3);missing=max(p1["missing"],p43["missing"])
    status=classify(p1);status43=classify(p43);counts[status]+=1;counts43[status43]+=1
    w.writerow({"candidate_id":g["candidate_id"],"link_family":k[0],"service_fistel":k[1],"rf_act_number":k[2],"distance_km":dist,"minimum_reciprocal_frequency_mhz":freq,"antenna_height_a_m":ha,"antenna_height_b_m":hb,"terrain_samples":p1["samples"],"missing_samples":missing,"minimum_los_clearance_k1_m":"" if p1["los"] is None else p1["los"],"minimum_fresnel60_clearance_k1_m":"" if p1["fresnel"] is None else p1["fresnel"],"minimum_los_clearance_k4_3_m":"" if p43["los"] is None else p43["los"],"minimum_fresnel60_clearance_k4_3_m":"" if p43["fresnel"] is None else p43["fresnel"],"terrain_status_k1":status,"terrain_status_k4_3":status43,"pairing_status":"not_performed","terrain_source":f"Mapzen Terrarium z{zoom}; preliminary","height_semantics":"maximum registered antenna height per endpoint; optimistic upper bound"})
  os.replace(staged,output)
 terrain.close();result={"schema_version":1,"geometry_file":str(geometry),"geometry_sha256":sha256_file(geometry),"candidate_groups":len(selected),"status_k1":dict(sorted(counts.items())),"status_k4_3":dict(sorted(counts43.items())),"terrain_zoom":zoom,"sample_spacing_km":1.0,"curvature_models":[1.0,4/3],"fresnel_clearance_fraction":0.6,"terrain_semantics":"preliminary Mapzen Terrarium; missing tiles fail closed; replace with TOPODATA","antenna_height_semantics":"maximum per endpoint is optimistic","pairing_status":"not_performed","output":str(output)}
 report.parent.mkdir(parents=True,exist_ok=True);payload=(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode()
 with tempfile.NamedTemporaryFile(prefix=f".{report.name}.",dir=report.parent,delete=False) as t:t.write(payload);tmp=Path(t.name)
 os.replace(tmp,report);return result
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--geometry",type=Path,required=True);p.add_argument("--keys",type=Path,required=True);p.add_argument("--emissions",type=Path,required=True);p.add_argument("--terrain-cache",type=Path,required=True);p.add_argument("--output",type=Path,required=True);p.add_argument("--report",type=Path,required=True);a=p.parse_args();print(json.dumps(evaluate(a.geometry,a.keys,a.emissions,a.terrain_cache,a.output,a.report),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
