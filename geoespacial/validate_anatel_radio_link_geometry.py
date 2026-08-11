#!/usr/bin/env python3
"""Avalia reciprocidade espectral e alinhamento de azimute sem formar enlaces."""

from __future__ import annotations
import argparse,csv,gzip,json,math,os,tempfile
from collections import Counter,defaultdict
from pathlib import Path
from audit_anatel_spectrum import number
from build_canonical_smp import deterministic_gzip_csv,sha256_file

THRESHOLDS=(5,10,15,30)
FIELDS=("candidate_id","link_family","service_fistel","rf_act_number","coordinate_a","coordinate_b","distance_km","bearing_a_to_b_deg","bearing_b_to_a_deg","reciprocal_paths","evaluable_paths","minimum_two_end_error_deg","aligned_paths_5deg","aligned_paths_10deg","aligned_paths_15deg","aligned_paths_30deg","geometry_status","pairing_status")

def bearing(a,b):
 lat1,lon1=map(math.radians,a);lat2,lon2=map(math.radians,b);dlon=lon2-lon1
 return (math.degrees(math.atan2(math.sin(dlon)*math.cos(lat2),math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(dlon)))+360)%360
def angular_error(a,b): return abs((a-b+180)%360-180)

def validate(candidates:Path,keys:Path,emissions:Path,output:Path,report:Path)->dict:
 selected={}
 with gzip.open(candidates,"rt",encoding="utf-8",newline="") as s:
  for r in csv.DictReader(s):
   if r["status"]=="two_coordinate_reciprocal": selected[(r["link_family"],r["service_fistel"],r["rf_act_number"])]=r
 group_by_row={};groups=defaultdict(list)
 with gzip.open(keys,"rt",encoding="utf-8",newline="") as s:
  for r in csv.DictReader(s):
   k=(r["link_family"],r["service_fistel"],r["rf_act_number"])
   if k in selected: group_by_row[r["source_row_number"]]=k
 azimuth={}
 with gzip.open(emissions,"rt",encoding="utf-8",newline="") as s:
  for r in csv.DictReader(s):
   k=group_by_row.get(r["source_row_number"])
   if k: groups[k].append(r)
 counts=Counter();aligned=Counter();distances=[];output.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(prefix="link-geometry-",dir=output.parent) as d:
  staged=Path(d)/output.name
  with deterministic_gzip_csv(staged,FIELDS) as w:
   for k in sorted(selected):
    source=selected[k];coords=sorted({(number(r["latitude"]),number(r["longitude"])) for r in groups[k]});a,b=coords;ba=bearing(a,b);bb=bearing(b,a);dist=number(source["distance_km"]);distances.append(dist)
    sides={a:defaultdict(lambda:defaultdict(list)),b:defaultdict(lambda:defaultdict(list))}
    for r in groups[k]:
     coord=(number(r["latitude"]),number(r["longitude"]));freq=number(r["frequency_mhz"]);az=number(r["azimuth_deg"])
     if freq is not None and az is not None:sides[coord][r["direction"]][freq].append(az)
    paths=[]
    for origin,target,desired in ((a,b,ba),(b,a,bb)):
     other=b if origin==a else a
     for freq,azs in sides[origin]["Transmissão"].items():
      remote=sides[other]["Recepção"].get(freq,[])
      if remote: paths.append(max(min(angular_error(x,desired) for x in azs),min(angular_error(x,bearing(other,origin)) for x in remote)))
    evaluation={t:sum(error<=t for error in paths) for t in THRESHOLDS}; minimum=min(paths) if paths else None
    status="azimuth_consistent_15deg" if evaluation[15] else ("azimuth_inconsistent_15deg" if paths else "azimuth_not_evaluable")
    counts[status]+=1
    for t,v in evaluation.items():aligned[t]+=int(v>0)
    w.writerow({"candidate_id":source["candidate_id"],"link_family":k[0],"service_fistel":k[1],"rf_act_number":k[2],"coordinate_a":source["coordinate_a"],"coordinate_b":source["coordinate_b"],"distance_km":dist,"bearing_a_to_b_deg":ba,"bearing_b_to_a_deg":bb,"reciprocal_paths":source["reciprocal_frequency_count"],"evaluable_paths":len(paths),"minimum_two_end_error_deg":"" if minimum is None else minimum,**{f"aligned_paths_{t}deg":evaluation[t] for t in THRESHOLDS},"geometry_status":status,"pairing_status":"not_performed"})
  os.replace(staged,output)
 result={"schema_version":1,"candidate_file":str(candidates),"candidate_sha256":sha256_file(candidates),"key_file":str(keys),"key_sha256":sha256_file(keys),"emission_file":str(emissions),"emission_sha256":sha256_file(emissions),"candidate_groups":len(selected),"status":dict(sorted(counts.items())),"sensitivity_groups_with_at_least_one_aligned_path":{str(t):aligned[t] for t in THRESHOLDS},"distance_km":{"min":min(distances),"max":max(distances),"mean":sum(distances)/len(distances)},"threshold_semantics":"15 degrees is a provisional reporting marker; all sensitivity thresholds are published","pairing_status":"not_performed","output":str(output)}
 report.parent.mkdir(parents=True,exist_ok=True);payload=(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode()
 with tempfile.NamedTemporaryFile(prefix=f".{report.name}.",dir=report.parent,delete=False) as t:t.write(payload);tmp=Path(t.name)
 os.replace(tmp,report);return result
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--candidates",type=Path,required=True);p.add_argument("--keys",type=Path,required=True);p.add_argument("--emissions",type=Path,required=True);p.add_argument("--output",type=Path,required=True);p.add_argument("--report",type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.candidates,a.keys,a.emissions,a.output,a.report),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
