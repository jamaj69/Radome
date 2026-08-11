#!/usr/bin/env /usr/bin/python3
"""Inventaria radiodifusão Anatel e liga sítios licenciados aos municípios."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

import networkx as nx


UF_CODE = {
    "RO": "11", "AC": "12", "AM": "13", "RR": "14", "PA": "15", "AP": "16", "TO": "17",
    "MA": "21", "PI": "22", "CE": "23", "RN": "24", "PB": "25", "PE": "26", "AL": "27",
    "SE": "28", "BA": "29", "MG": "31", "ES": "32", "RJ": "33", "SP": "35", "PR": "41",
    "SC": "42", "RS": "43", "MS": "50", "MT": "51", "GO": "52", "DF": "53",
}


def normalize_name(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value).casefold()
    plain = "".join(char for char in decomposed if not unicodedata.combining(char))
    return " ".join(plain.replace("'", " ").replace("-", " ").split())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def municipality_index(gpkg: Path):
    from osgeo import ogr

    source = ogr.Open(str(gpkg))
    layer = source.GetLayerByName("lml_municipio_a")
    names = {}
    polygons = []
    for feature in layer:
        code = str(feature.GetField("geocodigo") or "")
        if len(code) != 7:
            continue
        names[(normalize_name(feature.GetField("nome") or ""), code[:2])] = code
        polygons.append((code, feature.GetGeometryRef().Clone()))
    return names, polygons


def spatial_code(longitude: float, latitude: float, polygons) -> str | None:
    from osgeo import ogr

    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(longitude, latitude)
    for code, polygon in polygons:
        if polygon.Contains(point) or polygon.Intersects(point):
            return code
    return None


def build(zip_path: Path, gpkg: Path, output_dir: Path, licensed_status: str = "C4") -> dict:
    names, polygons = municipality_index(gpkg)
    all_statuses: Counter[str] = Counter()
    all_status_descriptions: Counter[str] = Counter()
    all_services: Counter[str] = Counter()
    rows = valid_coordinates = licensed_rows = name_matches = spatial_matches = 0
    sites = defaultdict(lambda: {
        "records": 0, "codes": Counter(), "services": set(), "channels": set(), "frequencies": set(),
        "entities": set(), "classes": set(), "categories": set(), "purposes": set(), "erp": [],
    })
    with ZipFile(zip_path) as archive:
        member = archive.getinfo("TV_FM_OM.csv")
        with archive.open(member) as raw:
            reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""), delimiter=";")
            columns = reader.fieldnames
            for record in reader:
                rows += 1
                status = record["Sigla Status"].strip() or "N/I"
                all_statuses[status] += 1
                all_status_descriptions[record["Status Descrição"].strip() or "N/I"] += 1
                all_services[record["SiglaServico"].strip() or "N/I"] += 1
                try:
                    latitude = float(record["Latitude Decimal SRD"].replace(",", "."))
                    longitude = float(record["Longitude Decimal SRD"].replace(",", "."))
                except ValueError:
                    continue
                if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                    continue
                valid_coordinates += 1
                if status != licensed_status:
                    continue
                licensed_rows += 1
                uf = record["srd_planobasico_SiglaUF"].strip()
                key = (normalize_name(record["srd_planobasico_NomeMunicipio"]), UF_CODE.get(uf, ""))
                code = names.get(key)
                if code:
                    name_matches += 1
                else:
                    code = spatial_code(longitude, latitude, polygons)
                    spatial_matches += int(code is not None)
                site_key = (round(latitude, 5), round(longitude, 5))
                site = sites[site_key]
                site["records"] += 1
                if code:
                    site["codes"][code] += 1
                for source, target in (
                    ("SiglaServico", "services"), ("Canal", "channels"), ("Frequência", "frequencies"),
                    ("Entidade", "entities"), ("Classe", "classes"), ("Categoria da Estação", "categories"),
                    ("Finalidade", "purposes"),
                ):
                    value = record[source].strip()
                    if value:
                        site[target].add(value)
                try:
                    site["erp"].append(float(record["ERP"].replace(",", ".")))
                except ValueError:
                    pass

    graph = nx.Graph(scope="Brazil", source="Anatel radiodifusao", active_filter="Sigla Status = C4")
    site_rows = []
    missing_codes = conflicting_codes = 0
    for (latitude, longitude), site in sorted(sites.items()):
        codes = site["codes"].most_common()
        code = codes[0][0] if codes else ""
        missing_codes += int(not code)
        conflicting_codes += int(len(codes) > 1)
        identifier = f"broadcast_site:{latitude:.5f}:{longitude:.5f}"
        attributes = {
            "kind": "radiodifusao",
            "ibge_code": code,
            "x_longitude": longitude,
            "y_latitude": latitude,
            "record_count": site["records"],
            "services": "|".join(sorted(site["services"])),
            "channels": "|".join(sorted(site["channels"])),
            "frequencies_mhz": "|".join(sorted(site["frequencies"])),
            "entities": "|".join(sorted(site["entities"])),
            "classes": "|".join(sorted(site["classes"])),
            "categories": "|".join(sorted(site["categories"])),
            "purposes": "|".join(sorted(site["purposes"])),
            "max_erp": max(site["erp"]) if site["erp"] else -1,
            "municipal_code_conflict": len(codes) > 1,
        }
        graph.add_node(identifier, **attributes)
        if code:
            municipal_id = f"municipio:{code}"
            graph.add_node(municipal_id, kind="municipio", ibge_code=code)
            graph.add_edge(identifier, municipal_id, relation="located_in")
        site_rows.append({"node_id": identifier, **attributes})

    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "broadcast_site_nodes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(site_rows[0]))
        writer.writeheader()
        writer.writerows(site_rows)
    nx.write_graphml(graph, output_dir / "broadcast_municipal_network.graphml")
    summary = {
        "source_size_bytes": zip_path.stat().st_size,
        "source_sha256": sha256(zip_path),
        "csv_uncompressed_size_bytes": member.file_size,
        "columns": columns,
        "record_count": rows,
        "valid_coordinate_record_count": valid_coordinates,
        "licensed_record_count": licensed_rows,
        "licensed_site_count": len(sites),
        "municipality_name_matches": name_matches,
        "municipality_spatial_fallback_matches": spatial_matches,
        "sites_without_municipal_code": missing_codes,
        "sites_with_conflicting_municipal_codes": conflicting_codes,
        "services_all_records": dict(all_services.most_common()),
        "status_codes_all_records": dict(all_statuses.most_common()),
        "status_descriptions_all_records": dict(all_status_descriptions.most_common()),
        "active_filter": "Sigla Status == C4 (Canal Licenciado)",
        "interpretation": "Canais vagos, pendentes, suspensos ou aguardando licenciamento ficam no inventario, nao no grafo de iluminadores ativos.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path, required=True)
    parser.add_argument("--bc250", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--licensed-status", default="C4")
    args = parser.parse_args()
    print(json.dumps(build(args.zip, args.bc250, args.output_dir, args.licensed_status), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
