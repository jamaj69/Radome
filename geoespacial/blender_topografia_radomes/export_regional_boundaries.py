"""Exporta divisas BC250 para a extensão inteira da cena regional."""
import argparse
import json
from pathlib import Path

from export_local_boundaries import boundary_parts


def build(bc250, terrain, output):
    from osgeo import ogr
    source = ogr.Open(str(bc250))
    municipalities = source.GetLayerByName("lml_municipio_a")
    states = source.GetLayerByName("lml_unidade_federacao_a")
    if municipalities is None or states is None:
        raise ValueError("BC250 sem limites municipais ou estaduais")
    west, south, east, north = json.loads(terrain.read_text(encoding="utf-8"))["bbox_wgs84"]
    result = {
        "schema_version": 1,
        "bbox_wgs84": [west, south, east, north],
        "municipal_boundaries": boundary_parts(municipalities, west, south, east, north, 12),
        "state_boundaries": boundary_parts(states, west, south, east, north, 3),
        "semantics": "Divisas municipais e estaduais do IBGE BC250 para sobreposição cartográfica regional; não alteram o DEM.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bc250", type=Path, required=True)
    parser.add_argument("--terrain", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    build(arguments.bc250, arguments.terrain, arguments.output)
