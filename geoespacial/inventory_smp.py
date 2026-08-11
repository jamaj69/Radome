#!/usr/bin/env python3
"""Resume o CSV oficial de estações SMP sem extrair o arquivo de quase 1 GB."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
from zipfile import ZipFile


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inventory(path: Path, coordinate_decimals: int = 5) -> dict:
    rows = valid_coordinates = 0
    stations: set[str] = set()
    coordinates: set[tuple[float, float]] = set()
    station_sites: set[tuple[tuple[float, float], str]] = set()
    situations: Counter[str] = Counter()
    technologies: Counter[str] = Counter()
    generations: Counter[str] = Counter()
    operators: Counter[str] = Counter()
    states: Counter[str] = Counter()

    with ZipFile(path) as archive:
        members = archive.infolist()
        if len(members) != 1:
            raise ValueError("O ZIP SMP deve conter exatamente um CSV")
        member = members[0]
        with archive.open(member) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
            reader = csv.DictReader(text, delimiter=";")
            required = {"Número Estação", "Latitude decimal", "Longitude decimal", "Situacao"}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise ValueError(f"Colunas SMP ausentes: {sorted(missing)}")
            columns = reader.fieldnames
            for record in reader:
                rows += 1
                situation = record["Situacao"].strip() or "N/I"
                situations[situation] += 1
                station = record["Número Estação"].strip()
                if station:
                    stations.add(station)
                try:
                    latitude = float(record["Latitude decimal"].replace(",", "."))
                    longitude = float(record["Longitude decimal"].replace(",", "."))
                except ValueError:
                    continue
                if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                    continue
                if latitude == 0 and longitude == 0:
                    continue
                valid_coordinates += 1
                site = (round(latitude, coordinate_decimals), round(longitude, coordinate_decimals))
                coordinates.add(site)
                if station:
                    station_sites.add((site, station))
                technologies[record.get("Tecnologia", "").strip() or "N/I"] += 1
                generations[record.get("Geração", "").strip() or "N/I"] += 1
                operator = record.get("Empresa Estação", "").strip() or record.get("Entidade", "").strip()
                operators[operator or "N/I"] += 1
                states[record.get("UF", "").strip() or "N/I"] += 1

    return {
        "schema_version": 1,
        "source_file": str(path),
        "source_size_bytes": path.stat().st_size,
        "source_sha256": file_sha256(path),
        "csv_member": member.filename,
        "csv_uncompressed_size_bytes": member.file_size,
        "columns": columns,
        "record_count": rows,
        "valid_coordinate_record_count": valid_coordinates,
        "unique_station_number_count": len(stations),
        "coordinate_rounding_decimals": coordinate_decimals,
        "approximate_physical_site_count": len(coordinates),
        "unique_station_site_pair_count": len(station_sites),
        "situations": dict(sorted(situations.items())),
        "technologies": dict(technologies.most_common()),
        "generations": dict(generations.most_common()),
        "operators": dict(operators.most_common()),
        "states": dict(sorted(states.items())),
        "interpretation": (
            "A contagem de sitios e uma aproximacao por coordenada arredondada; setores, "
            "frequencias, tecnologias, operadoras co-localizadas e pequenas divergencias "
            "cadastrais exigem consolidacao espacial antes do uso como torres fisicas."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--coordinate-decimals", type=int, default=5)
    args = parser.parse_args()
    result = inventory(args.zip, args.coordinate_decimals)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Inventário SMP gravado em {args.output}")


if __name__ == "__main__":
    main()
