#!/usr/bin/env python3
"""Inventaria cadastros oficiais de infraestrutura sem carregar geometrias.

O script lê os arquivos brutos já baixados da ANAC e da Anatel e o documento
GetCapabilities do WFS do DECEA. O produto versionável registra proveniência,
datas, hashes, contagens e esquemas; os arquivos volumosos permanecem em
``data/raw``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


DECEA_RELEVANT_LAYERS = {
    "ICA:airport": "aerodromos",
    "ICA:heliport": "helipontos",
    "ICA:rwydirection": "cabeceiras_de_pistas",
    "ICA:runway": "pistas",
    "ICA:runway_v2": "pistas_v2",
    "ICA:opea": "obstaculos_espaco_aereo",
    "ICA:vor": "auxilios_vor",
    "ICA:ndb": "auxilios_ndb",
    "ICA:navaids": "auxilios_navegacao",
    "ICA:CTR": "zonas_de_controle",
    "ICA:TMA": "areas_de_controle_terminal",
    "ICA:zida": "zona_identificacao_defesa_aerea",
    "ICA:airport_heliport": "aerodromos_e_helipontos_aixm",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_anac_csv(path: Path) -> dict:
    raw = path.read_bytes()
    encoding = "utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "latin-1"
    lines = raw.decode(encoding).splitlines()
    updated = lines[0].strip() if lines else None
    header = next(csv.reader([lines[1]], delimiter=";")) if len(lines) > 1 else []
    return {
        "file": str(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
        "encoding": encoding,
        "source_timestamp": updated,
        "record_count": max(0, len(lines) - 2),
        "columns": header,
    }


def read_anatel_zip(path: Path) -> dict:
    members = []
    with ZipFile(path) as archive:
        for info in archive.infolist():
            with archive.open(info) as stream:
                header = stream.readline().decode("utf-8-sig", errors="replace").strip()
            members.append(
                {
                    "name": info.filename,
                    "size_bytes": info.file_size,
                    "compressed_size_bytes": info.compress_size,
                    "columns": next(csv.reader([header], delimiter=";")),
                }
            )
    return {
        "file": str(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
        "uncompressed_size_bytes": sum(item["size_bytes"] for item in members),
        "members": members,
        "contains_dedicated_smp_resource": any("SMP" in item["name"].upper() for item in members),
    }


def read_decea_capabilities(path: Path) -> dict:
    root = ET.parse(path).getroot()
    available = {}
    for feature in root.findall(".//{*}FeatureType"):
        name_element = feature.find("{*}Name")
        title_element = feature.find("{*}Title")
        if name_element is None or not name_element.text:
            continue
        available[name_element.text.strip()] = (
            title_element.text.strip() if title_element is not None and title_element.text else ""
        )
    selected = [
        {
            "name": name,
            "title": available[name],
            "role": role,
        }
        for name, role in DECEA_RELEVANT_LAYERS.items()
        if name in available
    ]
    return {
        "capabilities_file": str(path),
        "feature_type_count": len(available),
        "selected_layer_count": len(selected),
        "selected_layers": selected,
        "missing_expected_layers": sorted(set(DECEA_RELEVANT_LAYERS) - set(available)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anac-dir", type=Path, required=True)
    parser.add_argument("--anatel-zip", type=Path, required=True)
    parser.add_argument("--decea-capabilities", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    anac_files = sorted(args.anac_dir.glob("*.csv"))
    if not anac_files:
        raise SystemExit(f"Nenhum CSV da ANAC encontrado em {args.anac_dir}")
    result = {
        "schema_version": 1,
        "anac": [read_anac_csv(path) for path in anac_files],
        "anatel": read_anatel_zip(args.anatel_zip),
        "decea": read_decea_capabilities(args.decea_capabilities),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Inventário gravado em {args.output}")


if __name__ == "__main__":
    main()
