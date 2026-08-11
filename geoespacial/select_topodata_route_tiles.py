#!/usr/bin/env python3
"""Seleciona folhas TOPODATA que intersectam rotas candidatas."""
from __future__ import annotations
import argparse,csv,gzip,json,math,os,tempfile
from pathlib import Path
from build_canonical_smp import sha256_file
from evaluate_anatel_radio_link_terrain import interpolate

def tile_name(latitude:float,longitude:float)->str:
 if latitude>0: lat=math.ceil(latitude);hem="N"
 else: lat=math.floor(abs(latitude));hem="S"
 west=math.ceil(abs(longitude)/1.5-1e-12)*1.5
 lon=f"{int(west):02d}_" if west.is_integer() else f"{int(west):02d}5"
 return f"{lat:02d}{hem}{lon}ZN.zip"

def select(routes:Path,manifest:Path,output:Path,spacing_km=1.0)->dict:
 inventory=json.loads(manifest.read_text(encoding="utf-8"));available={x["name"]:x for x in inventory["archives"]};selected=set();route_count=0;missing=set()
 with gzip.open(routes,"rt",encoding="utf-8",newline="") as s:
  for r in csv.DictReader(s):
   if r["geometry_status"]!="azimuth_consistent_15deg":continue
   route_count+=1;a=tuple(map(float,r["coordinate_a"].split(",")));b=tuple(map(float,r["coordinate_b"].split(",")));distance=float(r["distance_km"]);n=max(2,math.ceil(distance/spacing_km)+1)
   for i in range(n):
    name=tile_name(*interpolate(a,b,i/(n-1)))
    (selected if name in available else missing).add(name)
 items=[available[name] for name in sorted(selected)];result={"schema_version":1,"route_file":str(routes),"route_sha256":sha256_file(routes),"manifest_file":str(manifest),"manifest_sha256":sha256_file(manifest),"route_count":route_count,"sample_spacing_km":spacing_km,"selected_archive_count":len(items),"selected_listed_size_bytes":sum(x["listed_size_bytes"] for x in items),"missing_archive_names":sorted(missing),"archives":items,"selection_semantics":"great-circle samples at <=1 km mapped to official 1 degree by 1.5 degree TOPODATA upper-left naming"}
 output.parent.mkdir(parents=True,exist_ok=True);payload=(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode()
 with tempfile.NamedTemporaryFile(prefix=f".{output.name}.",dir=output.parent,delete=False) as t:t.write(payload);tmp=Path(t.name)
 os.replace(tmp,output);return result
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--routes",type=Path,required=True);p.add_argument("--manifest",type=Path,required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args();print(json.dumps(select(a.routes,a.manifest,a.output),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
