#!/usr/bin/env python3
"""Normaliza o cadastro SMP no esquema canônico sítio--antena--emissão."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import os
import tempfile
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from zipfile import ZipFile

from audit_anatel_spectrum import emission_bandwidth_hz, number, positive_frequency


SITE_FIELDS = (
    "site_id", "latitude", "longitude", "coordinate_rounding_decimals",
    "ibge_code", "municipal_code_conflict", "source_record_count",
    "station_count", "antenna_proxy_count", "source_dataset",
)
ANTENNA_FIELDS = (
    "antenna_id", "site_id", "station_number", "sector", "operators",
    "source_record_count", "entity_semantics", "physical_identity_confidence",
    "source_dataset",
)
EMISSION_FIELDS = (
    "emission_id", "source_row_number", "site_id", "antenna_id",
    "station_number", "sector", "ibge_code", "operator", "generation",
    "technology", "technology_5g_type", "station_band", "station_subband",
    "tx_center_mhz", "rx_center_mhz", "emission_designation",
    "necessary_bandwidth_hz", "tx_occupied_lower_mhz",
    "tx_occupied_upper_mhz", "situation", "source_dataset",
)
SOURCE_DATASET = "anatel_estacoes_smp"


def canonical_coordinate(value: str, decimals: int) -> float | None:
    parsed = number(value)
    if parsed is None:
        return None
    return round(parsed, decimals)


def stable_identifier(prefix: str, *parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return f"{prefix}:{hashlib.blake2b(payload, digest_size=12).hexdigest()}"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


@contextmanager
def deterministic_gzip_csv(path: Path, fieldnames: tuple[str, ...]):
    """Abre CSV gzip reproduzível, sem nome ou horário variável no cabeçalho."""
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as text:
                writer = csv.DictWriter(text, fieldnames=fieldnames, lineterminator="\n")
                writer.writeheader()
                yield writer


def dominant_code(counts: Counter[str]) -> tuple[str, bool]:
    if not counts:
        return "", False
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ordered[0][0], len(ordered) > 1


def build(
    source_zip: Path, output_dir: Path, decimals: int = 5,
    report: Path | None = None,
) -> dict:
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="canonical-smp-", dir=output_dir.parent) as temporary:
        staging = Path(temporary)
        sites: dict[tuple[float, float], dict] = {}
        antennas: dict[str, dict] = {}
        source_records = emission_records = invalid_coordinates = 0

        with ZipFile(source_zip) as archive, archive.open("Estacoes_SMP.csv") as raw:
            reader = csv.DictReader(
                io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""), delimiter=";"
            )
            with deterministic_gzip_csv(staging / "emissions.csv.gz", EMISSION_FIELDS) as writer:
                for source_row_number, record in enumerate(reader, 1):
                    source_records += 1
                    latitude = canonical_coordinate(record.get("Latitude decimal", ""), decimals)
                    longitude = canonical_coordinate(record.get("Longitude decimal", ""), decimals)
                    valid = (
                        latitude is not None and longitude is not None
                        and -90 <= latitude <= 90 and -180 <= longitude <= 180
                    )
                    site_id = antenna_id = ""
                    station = record.get("Número Estação", "").strip()
                    sector = record.get("NumSetor", "").strip()
                    operator = record.get("Empresa Estação", "").strip()
                    ibge_code = record.get("Código IBGE", "").strip()
                    if valid:
                        key = (latitude, longitude)
                        site_id = f"smp_site:{latitude:.{decimals}f}:{longitude:.{decimals}f}"
                        site = sites.setdefault(key, {
                            "site_id": site_id, "codes": Counter(), "records": 0,
                            "stations": set(), "antennas": set(),
                        })
                        site["records"] += 1
                        if len(ibge_code) == 7:
                            site["codes"][ibge_code] += 1
                        if station:
                            site["stations"].add(station)
                        antenna_id = stable_identifier("smp_antenna", site_id, station, sector)
                        antenna = antennas.setdefault(antenna_id, {
                            "site_id": site_id, "station": station, "sector": sector,
                            "operators": set(), "records": 0,
                        })
                        antenna["records"] += 1
                        if operator:
                            antenna["operators"].add(operator)
                        site["antennas"].add(antenna_id)
                    else:
                        invalid_coordinates += 1

                    designation = record.get("Designação Emissão", "").strip()
                    bandwidth = emission_bandwidth_hz(designation)
                    tx = number(record.get("FreqTxMHz", ""))
                    rx = number(record.get("FreqRxMHz", ""))
                    valid_tx = positive_frequency(tx)
                    half_mhz = bandwidth / 2e6 if bandwidth is not None else None
                    writer.writerow({
                        "emission_id": f"smp_emission:{source_row_number:08d}",
                        "source_row_number": source_row_number,
                        "site_id": site_id,
                        "antenna_id": antenna_id,
                        "station_number": station,
                        "sector": sector,
                        "ibge_code": ibge_code,
                        "operator": operator,
                        "generation": record.get("Geração", "").strip() or "N/I",
                        "technology": record.get("Tecnologia", "").strip() or "N/I",
                        "technology_5g_type": record.get("Tipo de Tecnologia 5G", "").strip(),
                        "station_band": record.get("Faixa Estação", "").strip(),
                        "station_subband": record.get("Subfaixa Estação", "").strip(),
                        "tx_center_mhz": "" if tx is None else tx,
                        "rx_center_mhz": "" if rx is None else rx,
                        "emission_designation": designation,
                        "necessary_bandwidth_hz": "" if bandwidth is None else bandwidth,
                        "tx_occupied_lower_mhz": "" if valid_tx is None or half_mhz is None else valid_tx - half_mhz,
                        "tx_occupied_upper_mhz": "" if valid_tx is None or half_mhz is None else valid_tx + half_mhz,
                        "situation": record.get("Situacao", "").strip(),
                        "source_dataset": SOURCE_DATASET,
                    })
                    emission_records += 1

        conflicts = sites_without_code = 0
        with deterministic_gzip_csv(staging / "sites.csv.gz", SITE_FIELDS) as writer:
            for (latitude, longitude), site in sorted(sites.items()):
                code, conflict = dominant_code(site["codes"])
                conflicts += int(conflict)
                sites_without_code += int(not code)
                writer.writerow({
                    "site_id": site["site_id"], "latitude": latitude,
                    "longitude": longitude, "coordinate_rounding_decimals": decimals,
                    "ibge_code": code, "municipal_code_conflict": conflict,
                    "source_record_count": site["records"],
                    "station_count": len(site["stations"]),
                    "antenna_proxy_count": len(site["antennas"]),
                    "source_dataset": SOURCE_DATASET,
                })

        with deterministic_gzip_csv(staging / "antennas.csv.gz", ANTENNA_FIELDS) as writer:
            for antenna_id, antenna in sorted(antennas.items()):
                writer.writerow({
                    "antenna_id": antenna_id, "site_id": antenna["site_id"],
                    "station_number": antenna["station"], "sector": antenna["sector"],
                    "operators": "|".join(sorted(antenna["operators"])),
                    "source_record_count": antenna["records"],
                    "entity_semantics": "cadaster_proxy_station_sector_at_rounded_site",
                    "physical_identity_confidence": "low",
                    "source_dataset": SOURCE_DATASET,
                })

        site_assignment_records = sum(site["records"] for site in sites.values())
        antenna_assignment_records = sum(antenna["records"] for antenna in antennas.values())
        summary = {
            "schema_version": 1,
            "source_dataset": SOURCE_DATASET,
            "source_file": str(source_zip),
            "source_sha256": sha256_file(source_zip),
            "coordinate_rounding_decimals": decimals,
            "source_records": source_records,
            "site_records": len(sites),
            "antenna_proxy_records": len(antennas),
            "emission_records": emission_records,
            "site_assignment_records": site_assignment_records,
            "antenna_assignment_records": antenna_assignment_records,
            "invalid_coordinate_records": invalid_coordinates,
            "sites_without_municipal_code": sites_without_code,
            "sites_with_conflicting_municipal_codes": conflicts,
            "zero_loss": source_records == emission_records,
            "all_emissions_have_site": invalid_coordinates == 0,
            "all_emissions_have_antenna_proxy": invalid_coordinates == 0,
            "site_cardinality_consistent": site_assignment_records == emission_records,
            "antenna_cardinality_consistent": antenna_assignment_records == emission_records,
            "antenna_semantics": "proxy cadastral; estação + setor + sítio arredondado, não identificação física comprovada",
            "relationships": {
                "antenna_site": "many-to-one via site_id",
                "emission_antenna": "many-to-one via antenna_id",
                "emission_source": "one-to-one via source_row_number",
            },
            "products": {
                "sites": "outputs/canonical_smp/sites.csv.gz",
                "antennas": "outputs/canonical_smp/antennas.csv.gz",
                "emissions": "outputs/canonical_smp/emissions.csv.gz",
            },
        }
        summary_bytes = (json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        (staging / "summary.json").write_bytes(summary_bytes)
        output_dir.mkdir(parents=True, exist_ok=True)
        for name in ("sites.csv.gz", "antennas.csv.gz", "emissions.csv.gz", "summary.json"):
            os.replace(staging / name, output_dir / name)
        if report is not None:
            report.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                prefix=f".{report.name}.", dir=report.parent, delete=False
            ) as temporary_report:
                temporary_report.write(summary_bytes)
                temporary_report_path = Path(temporary_report.name)
            os.replace(temporary_report_path, report)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smp", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--coordinate-decimals", type=int, default=5)
    args = parser.parse_args()
    summary = build(args.smp, args.output_dir, args.coordinate_decimals, args.report)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not summary["zero_loss"]:
        raise SystemExit("A migração SMP perdeu registros")


if __name__ == "__main__":
    main()
