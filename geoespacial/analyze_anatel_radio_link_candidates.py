#!/usr/bin/env python3
"""Particiona grupos cadastrais de radioenlace sem criar arestas."""
from __future__ import annotations
import argparse,csv,gzip,json,math,os,tempfile
from collections import Counter,defaultdict
from pathlib import Path
from audit_anatel_spectrum import number
from build_canonical_smp import deterministic_gzip_csv,sha256_file,stable_identifier

FIELDS=("candidate_id","link_family","service_fistel","rf_act_number","status","coordinate_count","station_count","record_count","coordinate_a","coordinate_b","distance_km","reciprocal_frequency_count","pairing_status")

def distance(a,b):
    lat1,lon1=map(math.radians,a); lat2,lon2=map(math.radians,b); dlat=lat2-lat1; dlon=lon2-lon1
    h=math.sin(dlat/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 6371.0088*2*math.asin(math.sqrt(h))

def analyze(source:Path,output:Path,report:Path)->dict:
    groups=defaultdict(lambda:{"coords":defaultdict(lambda:{"tx":set(),"rx":set()}),"stations":set(),"records":0})
    with gzip.open(source,"rt",encoding="utf-8",newline="") as stream:
        for r in csv.DictReader(stream):
            key=(r["link_family"],r["service_fistel"],r["rf_act_number"]); g=groups[key]; g["records"]+=1; g["stations"].add(r["station_number"])
            lat=number(r["latitude"]); lon=number(r["longitude"]); freq=number(r["frequency_mhz"])
            if lat is None or lon is None: continue
            side=g["coords"][(lat,lon)]
            if freq is not None and r["direction"]=="Transmissão": side["tx"].add(freq)
            if freq is not None and r["direction"]=="Recepção": side["rx"].add(freq)
    counts=Counter(); reciprocal_total=0; output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="link-candidates-",dir=output.parent) as d:
        staged=Path(d)/output.name
        with deterministic_gzip_csv(staged,FIELDS) as writer:
            for key,g in sorted(groups.items()):
                coords=sorted(g["coords"]); reciprocal=set(); dist=""; a=b=""
                if len(coords)==1: status="single_coordinate"
                elif len(coords)>2: status="ambiguous_multiple_coordinates"
                else:
                    ca,cb=coords; reciprocal=(g["coords"][ca]["tx"]&g["coords"][cb]["rx"])|(g["coords"][cb]["tx"]&g["coords"][ca]["rx"])
                    status="two_coordinate_reciprocal" if reciprocal else "two_coordinate_nonreciprocal"; dist=distance(ca,cb); a=f"{ca[0]},{ca[1]}"; b=f"{cb[0]},{cb[1]}"
                counts[status]+=1; reciprocal_total+=len(reciprocal)
                writer.writerow({"candidate_id":stable_identifier("anatel_link_group",*key),"link_family":key[0],"service_fistel":key[1],"rf_act_number":key[2],"status":status,"coordinate_count":len(coords),"station_count":len(g["stations"]),"record_count":g["records"],"coordinate_a":a,"coordinate_b":b,"distance_km":dist,"reciprocal_frequency_count":len(reciprocal),"pairing_status":"not_performed"})
        os.replace(staged,output)
    result={"schema_version":1,"source_file":str(source),"source_sha256":sha256_file(source),"groups":len(groups),"partition":dict(sorted(counts.items())),"partition_consistent":sum(counts.values())==len(groups),"reciprocal_frequency_matches":reciprocal_total,"pairing_status":"not_performed","output":str(output)}
    report.parent.mkdir(parents=True,exist_ok=True); payload=(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode()
    with tempfile.NamedTemporaryFile(prefix=f".{report.name}.",dir=report.parent,delete=False) as t:t.write(payload); tmp=Path(t.name)
    os.replace(tmp,report); return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--source",type=Path,required=True);p.add_argument("--output",type=Path,required=True);p.add_argument("--report",type=Path,required=True);a=p.parse_args();print(json.dumps(analyze(a.source,a.output,a.report),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
