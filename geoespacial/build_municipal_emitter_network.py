#!/usr/bin/env /usr/bin/python3
"""Constrói nós municipais e liga sítios SMP ao código IBGE correspondente."""

from __future__ import annotations

import argparse
import csv
import io
import json
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

import networkx as nx

from build_candidate_graph import terrain_elevation


def read_population(path: Path) -> dict[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    series = data[0]["resultados"][0]["series"]
    return {item["localidade"]["id"]: int(item["serie"]["2022"]) for item in series}


def municipal_features(gpkg: Path) -> tuple[dict[str, dict], dict[str, tuple[float, float]]]:
    # GDAL bindings are provided by the system Python used for the full build.
    # Keeping the import local lets pure aggregation helpers be unit-tested in
    # the shared project environment, where ``osgeo`` may not be installed.
    from osgeo import ogr, osr

    source = ogr.Open(str(gpkg))
    if source is None:
        raise ValueError(f"Não foi possível abrir {gpkg}")
    municipalities = {}
    source_srs = osr.SpatialReference()
    source_srs.ImportFromEPSG(4674)
    area_srs = osr.SpatialReference()
    area_srs.ImportFromEPSG(5880)
    transform = osr.CoordinateTransformation(source_srs, area_srs)
    for feature in source.GetLayerByName("lml_municipio_a"):
        code = str(feature.GetField("geocodigo") or "")
        if len(code) != 7:
            continue
        geometry = feature.GetGeometryRef().Clone()
        geometry.Transform(transform)
        municipalities[code] = {
            "name": feature.GetField("nome"),
            "area_km2": geometry.GetArea() / 1_000_000.0,
            "reference_year": feature.GetField("anodereferencia"),
        }
    seats = {}
    for feature in source.GetLayerByName("lml_cidade_p"):
        code = str(feature.GetField("geocodigo") or "")
        if code not in municipalities:
            continue
        point = feature.GetGeometryRef()
        seats[code] = (point.GetX(), point.GetY())
    return municipalities, seats


def read_smp_sites(path: Path, decimals: int = 5) -> dict[tuple[float, float], dict]:
    sites: dict[tuple[float, float], dict] = defaultdict(
        lambda: {
            "records": 0,
            "codes": Counter(),
            "stations": set(),
            "operators": set(),
            "technologies": set(),
            "generations": set(),
        }
    )
    with ZipFile(path) as archive, archive.open("Estacoes_SMP.csv") as raw:
        reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""), delimiter=";")
        for record in reader:
            try:
                latitude = float(record["Latitude decimal"].replace(",", "."))
                longitude = float(record["Longitude decimal"].replace(",", "."))
            except ValueError:
                continue
            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                continue
            key = (round(latitude, decimals), round(longitude, decimals))
            site = sites[key]
            site["records"] += 1
            for field, target in (
                ("Número Estação", "stations"),
                ("Empresa Estação", "operators"),
                ("Tecnologia", "technologies"),
                ("Geração", "generations"),
            ):
                value = record.get(field, "").strip()
                if value:
                    site[target].add(value)
            code = record.get("Código IBGE", "").strip()
            if len(code) == 7:
                site["codes"][code] += 1
    return sites


def dominant_code(counts: Counter[str]) -> tuple[str | None, bool]:
    if not counts:
        return None, False
    return counts.most_common(1)[0][0], len(counts) > 1


def write_network(
    municipalities: dict[str, dict],
    seats: dict[str, tuple[float, float]],
    populations: dict[str, int],
    sites: dict[tuple[float, float], dict],
    terrain_cache: Path,
    output_dir: Path,
    terrain_zoom: int,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    graph = nx.Graph(scope="Brazil", municipal_key="IBGE 7-digit code")
    municipality_rows = []
    for code, data in sorted(municipalities.items()):
        if code not in seats:
            continue
        longitude, latitude = seats[code]
        elevation = terrain_elevation(longitude, latitude, terrain_zoom, terrain_cache)
        population = populations.get(code)
        attributes = {
            "kind": "municipio",
            "ibge_code": code,
            "name": data["name"],
            "x_longitude": longitude,
            "y_latitude": latitude,
            "z_elevation_m": round(elevation, 2),
            "z_source": f"Mapzen Terrarium z{terrain_zoom}; replace with TOPODATA",
            "population_2022": population if population is not None else -1,
            "area_km2": round(data["area_km2"], 3),
            "visual_size": round(data["area_km2"], 3),
            "visual_size_semantics": "municipal_area_km2",
        }
        graph.add_node(f"municipio:{code}", **attributes)
        municipality_rows.append(attributes)

    tower_rows = []
    conflicts = missing_codes = unknown_codes = 0
    for index, ((latitude, longitude), site) in enumerate(sorted(sites.items()), 1):
        code, conflict = dominant_code(site["codes"])
        conflicts += int(conflict)
        missing_codes += int(code is None)
        unknown_codes += int(code is not None and code not in municipalities)
        tower_id = f"smp_site:{latitude:.5f}:{longitude:.5f}"
        attributes = {
            "kind": "torre_smp",
            "ibge_code": code or "",
            "x_longitude": longitude,
            "y_latitude": latitude,
            "record_count": site["records"],
            "station_count": len(site["stations"]),
            "operators": "|".join(sorted(site["operators"])),
            "technologies": "|".join(sorted(site["technologies"])),
            "generations": "|".join(sorted(site["generations"])),
            "municipal_code_conflict": conflict,
        }
        graph.add_node(tower_id, **attributes)
        if code in municipalities:
            graph.add_edge(tower_id, f"municipio:{code}", relation="located_in")
        tower_rows.append({"node_id": tower_id, **attributes})

    def write_csv(path: Path, rows: list[dict]) -> None:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    write_csv(output_dir / "municipality_nodes.csv", municipality_rows)
    write_csv(output_dir / "smp_site_nodes.csv", tower_rows)
    nx.write_graphml(graph, output_dir / "municipal_emitter_network.graphml")
    summary = {
        "municipality_nodes": len(municipality_rows),
        "municipalities_without_census_2022_population": sum(row["population_2022"] < 0 for row in municipality_rows),
        "smp_site_nodes": len(tower_rows),
        "smp_sites_without_municipal_code": missing_codes,
        "smp_sites_with_unknown_municipal_code": unknown_codes,
        "smp_sites_with_conflicting_codes": conflicts,
        "located_in_edges": graph.number_of_edges(),
        "node_size_semantics": "municipal area in square kilometres",
        "altitude_status": "preliminary terrain sample; TOPODATA replacement pending",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bc250", type=Path, required=True)
    parser.add_argument("--population", type=Path, required=True)
    parser.add_argument("--smp", type=Path, required=True)
    parser.add_argument("--terrain-cache", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--terrain-zoom", type=int, default=8)
    args = parser.parse_args()
    municipalities, seats = municipal_features(args.bc250)
    summary = write_network(
        municipalities,
        seats,
        read_population(args.population),
        read_smp_sites(args.smp),
        args.terrain_cache,
        args.output_dir,
        args.terrain_zoom,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
