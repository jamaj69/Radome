"""Exporta limites BC250 e amostras de altitude para a cena Blender."""
import argparse, csv, gzip, json
from pathlib import Path
from osgeo import ogr

def rings(layer, stride=12):
    output=[]
    for feature in layer:
        geometry=feature.GetGeometryRef()
        for polygon_index in range(geometry.GetGeometryCount()):
            polygon=geometry.GetGeometryRef(polygon_index)
            ring=polygon.GetGeometryRef(0)
            points=[ring.GetPoint(index)[:2] for index in range(0, ring.GetPointCount(), stride)]
            if len(points)>2: output.append(points+[points[0]])
    return output

def build(bc250, ranking, output):
    source=ogr.Open(str(bc250)); states=rings(source.GetLayerByName("lml_unidade_federacao_a")); countries=rings(source.GetLayerByName("lml_pais_a"), 8)
    with gzip.open(ranking,"rt",encoding="utf-8",newline="") as stream:
        points=[{"longitude":float(row["longitude"]),"latitude":float(row["latitude"]),"elevation_m":float(row["terrain_elevation_m"])} for row in csv.DictReader(stream)]
    data={"schema_version":1,"state_boundaries":states,"international_boundaries":countries,"altitude_samples":points,"semantics":"BC250 political boundaries; altitude heat points from preliminary candidate elevations, not a national DEM or RF result"}
    output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--bc250",type=Path,required=True);p.add_argument("--ranking",type=Path,required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args();build(a.bc250,a.ranking,a.output)
