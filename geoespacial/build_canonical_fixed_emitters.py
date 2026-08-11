#!/usr/bin/env python3
"""Migra transmissores/repetidores ativos SARC/SCM ao esquema canônico."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import tempfile
from collections import Counter
from pathlib import Path

from audit_anatel_spectrum import number
from build_canonical_smp import deterministic_gzip_csv, sha256_file, stable_identifier


INPUTS = ("sarc", "fixed_broadband")
EMITTER_ROLES = {
    "explicit_transmission_direction",
    "transmitter_station_class",
    "repeater_station_class",
}
SITE_FIELDS = (
    "site_id", "latitude", "longitude", "coordinate_rounding_decimals",
    "ibge_code", "municipal_code_conflict", "source_record_count",
    "antenna_proxy_count", "datasets", "source_dataset",
)
ANTENNA_FIELDS = (
    "antenna_id", "site_id", "station_number", "datasets", "polarizations",
    "azimuth_deg", "elevation_angle_deg", "antenna_height_m", "antenna_gain_db",
    "source_record_count", "entity_semantics", "physical_identity_confidence",
    "source_dataset",
)
EMISSION_FIELDS = (
    "emission_id", "dataset", "source_member", "source_row_number", "site_id",
    "antenna_id", "station_number", "entity", "service", "service_code_name",
    "rf_role_evidence", "validity_status", "frequency_mhz",
    "emission_designation", "necessary_bandwidth_hz", "transmitter_power_w",
    "polarization", "antenna_gain_db", "front_to_back_db",
    "half_power_beamwidth_deg", "azimuth_deg", "elevation_angle_deg",
    "antenna_height_m", "ibge_code", "state", "quantitative_rf_ready",
    "source_dataset",
)
SOURCE_DATASET = "anatel_general_fixed_emitters"


def exclusion_reason(record: dict[str, str]) -> str | None:
    if record.get("validity_status") != "Ativo":
        return "not_active"
    role = record.get("rf_role_evidence", "")
    if role in EMITTER_ROLES:
        return None
    if role in {"explicit_reception_direction", "receiver_only_station_class"}:
        return "receiver_only"
    return "unknown_rf_role"


def canonical_number(value: str) -> str:
    parsed = number(value)
    return "" if parsed is None else str(parsed)


def antenna_signature(record: dict[str, str], site_id: str) -> tuple[str, ...]:
    return (
        record.get("dataset", ""), site_id, record.get("station_number", ""),
        record.get("polarization", ""), canonical_number(record.get("azimuth_deg", "")),
        canonical_number(record.get("elevation_angle_deg", "")),
        canonical_number(record.get("antenna_height_m", "")),
        canonical_number(record.get("antenna_gain_db", "")),
    )


def build(inputs: dict[str, Path], output_dir: Path, report: Path, decimals: int = 5) -> dict:
    if set(inputs) != set(INPUTS):
        raise ValueError(f"Entradas esperadas: {INPUTS}")
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="canonical-fixed-", dir=output_dir.parent) as temporary:
        staging = Path(temporary)
        sites: dict[tuple[float, float], dict] = {}
        antennas: dict[str, dict] = {}
        source_counts = Counter()
        selected_counts = Counter()
        quantitative_ready_counts = Counter()
        exclusions: dict[str, Counter[str]] = {dataset: Counter() for dataset in INPUTS}
        selected_missing = {dataset: Counter() for dataset in INPUTS}

        with deterministic_gzip_csv(staging / "emissions.csv.gz", EMISSION_FIELDS) as writer:
            for dataset in INPUTS:
                with gzip.open(inputs[dataset], "rt", encoding="utf-8", newline="") as stream:
                    for record in csv.DictReader(stream):
                        source_counts[dataset] += 1
                        reason = exclusion_reason(record)
                        if reason is not None:
                            exclusions[dataset][reason] += 1
                            continue
                        latitude = number(record.get("latitude", ""))
                        longitude = number(record.get("longitude", ""))
                        if latitude is None or longitude is None or not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                            exclusions[dataset]["invalid_coordinates"] += 1
                            continue
                        latitude = round(latitude, decimals)
                        longitude = round(longitude, decimals)
                        site_id = f"anatel_site:{latitude:.{decimals}f}:{longitude:.{decimals}f}"
                        site = sites.setdefault((latitude, longitude), {
                            "site_id": site_id, "codes": Counter(), "records": 0,
                            "antennas": set(), "datasets": set(),
                        })
                        site["records"] += 1
                        site["datasets"].add(dataset)
                        ibge_code = record.get("ibge_code", "").strip()
                        if len(ibge_code) == 7 and ibge_code.isdigit():
                            site["codes"][ibge_code] += 1

                        signature = antenna_signature(record, site_id)
                        antenna_id = stable_identifier("anatel_antenna", *signature)
                        antenna = antennas.setdefault(antenna_id, {
                            "site_id": site_id, "station": record.get("station_number", ""),
                            "datasets": set(), "polarizations": set(), "records": 0,
                            "azimuth": signature[4], "elevation": signature[5],
                            "height": signature[6], "gain": signature[7],
                        })
                        antenna["records"] += 1
                        antenna["datasets"].add(dataset)
                        if record.get("polarization"):
                            antenna["polarizations"].add(record["polarization"])
                        site["antennas"].add(antenna_id)

                        selected_counts[dataset] += 1
                        for field in ("frequency_mhz", "transmitter_power_w", "emission_designation"):
                            selected_missing[dataset][field] += int(not record.get(field, "").strip())
                        quantitative_ready = all(record.get(field, "").strip() for field in (
                            "frequency_mhz", "transmitter_power_w", "antenna_height_m",
                        ))
                        quantitative_ready_counts[dataset] += int(quantitative_ready)
                        source_row = record.get("source_row_number", "")
                        writer.writerow({
                            "emission_id": stable_identifier("anatel_emission", dataset, source_row),
                            "dataset": dataset, "source_member": record.get("source_member", ""),
                            "source_row_number": source_row, "site_id": site_id,
                            "antenna_id": antenna_id, "station_number": record.get("station_number", ""),
                            "entity": record.get("entity", ""), "service": record.get("service", ""),
                            "service_code_name": record.get("service_code_name", ""),
                            "rf_role_evidence": record.get("rf_role_evidence", ""),
                            "validity_status": record.get("validity_status", ""),
                            "frequency_mhz": record.get("frequency_mhz", ""),
                            "emission_designation": record.get("emission_designation", ""),
                            "necessary_bandwidth_hz": record.get("necessary_bandwidth_hz", ""),
                            "transmitter_power_w": record.get("transmitter_power_w", ""),
                            "polarization": record.get("polarization", ""),
                            "antenna_gain_db": record.get("antenna_gain_db", ""),
                            "front_to_back_db": record.get("front_to_back_db", ""),
                            "half_power_beamwidth_deg": record.get("half_power_beamwidth_deg", ""),
                            "azimuth_deg": record.get("azimuth_deg", ""),
                            "elevation_angle_deg": record.get("elevation_angle_deg", ""),
                            "antenna_height_m": record.get("antenna_height_m", ""),
                            "ibge_code": ibge_code, "state": record.get("state", ""),
                            "quantitative_rf_ready": quantitative_ready,
                            "source_dataset": SOURCE_DATASET,
                        })

        conflicts = 0
        with deterministic_gzip_csv(staging / "sites.csv.gz", SITE_FIELDS) as writer:
            for (latitude, longitude), site in sorted(sites.items()):
                codes = sorted(site["codes"].items(), key=lambda item: (-item[1], item[0]))
                code = codes[0][0] if codes else ""
                conflict = len(codes) > 1
                conflicts += int(conflict)
                writer.writerow({
                    "site_id": site["site_id"], "latitude": latitude, "longitude": longitude,
                    "coordinate_rounding_decimals": decimals, "ibge_code": code,
                    "municipal_code_conflict": conflict, "source_record_count": site["records"],
                    "antenna_proxy_count": len(site["antennas"]),
                    "datasets": "|".join(sorted(site["datasets"])),
                    "source_dataset": SOURCE_DATASET,
                })

        with deterministic_gzip_csv(staging / "antennas.csv.gz", ANTENNA_FIELDS) as writer:
            for antenna_id, antenna in sorted(antennas.items()):
                writer.writerow({
                    "antenna_id": antenna_id, "site_id": antenna["site_id"],
                    "station_number": antenna["station"],
                    "datasets": "|".join(sorted(antenna["datasets"])),
                    "polarizations": "|".join(sorted(antenna["polarizations"])),
                    "azimuth_deg": antenna["azimuth"], "elevation_angle_deg": antenna["elevation"],
                    "antenna_height_m": antenna["height"], "antenna_gain_db": antenna["gain"],
                    "source_record_count": antenna["records"],
                    "entity_semantics": "cadaster_proxy_station_and_antenna_attributes_at_rounded_site",
                    "physical_identity_confidence": "medium",
                    "source_dataset": SOURCE_DATASET,
                })

        datasets = {}
        for dataset in INPUTS:
            excluded = sum(exclusions[dataset].values())
            datasets[dataset] = {
                "source_records": source_counts[dataset],
                "selected_emission_records": selected_counts[dataset],
                "site_records": sum(dataset in site["datasets"] for site in sites.values()),
                "antenna_proxy_records": sum(dataset in antenna["datasets"] for antenna in antennas.values()),
                "quantitative_rf_ready_records": quantitative_ready_counts[dataset],
                "excluded_records": excluded,
                "exclusion_reasons": dict(sorted(exclusions[dataset].items())),
                "selected_missing_fields": dict(sorted(selected_missing[dataset].items())),
                "partition_consistent": source_counts[dataset] == selected_counts[dataset] + excluded,
            }
        selected_total = sum(selected_counts.values())
        site_assignments = sum(site["records"] for site in sites.values())
        antenna_assignments = sum(antenna["records"] for antenna in antennas.values())
        result = {
            "schema_version": 1,
            "source_dataset": SOURCE_DATASET,
            "input_files": {dataset: {"path": str(inputs[dataset]), "sha256": sha256_file(inputs[dataset])} for dataset in INPUTS},
            "selection_rule": "validity_status=Ativo and RF role evidence is explicit transmission, transmitter class, or repeater class",
            "site_records": len(sites), "antenna_proxy_records": len(antennas),
            "emission_records": selected_total, "site_assignment_records": site_assignments,
            "antenna_assignment_records": antenna_assignments,
            "sites_with_conflicting_municipal_codes": conflicts,
            "site_cardinality_consistent": site_assignments == selected_total,
            "antenna_cardinality_consistent": antenna_assignments == selected_total,
            "all_partitions_consistent": all(item["partition_consistent"] for item in datasets.values()),
            "datasets": datasets,
            "antenna_semantics": "proxy cadastral por estação e atributos de antena no sítio arredondado; não identidade física comprovada",
            "quantitative_rf_ready_semantics": "frequência, potência e altura de antena presentes; ainda requer validação regulatória e de propagação",
        }
        report_bytes = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        (staging / "summary.json").write_bytes(report_bytes)
        output_dir.mkdir(parents=True, exist_ok=True)
        for name in ("sites.csv.gz", "antennas.csv.gz", "emissions.csv.gz", "summary.json"):
            os.replace(staging / name, output_dir / name)
        report.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(prefix=f".{report.name}.", dir=report.parent, delete=False) as temp:
            temp.write(report_bytes)
            temp_path = Path(temp.name)
        os.replace(temp_path, report)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sarc", type=Path, required=True)
    parser.add_argument("--fixed-broadband", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = build({"sarc": args.sarc, "fixed_broadband": args.fixed_broadband}, args.output_dir, args.report)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["all_partitions_consistent"]:
        raise SystemExit("Partição SARC/SCM inconsistente")


if __name__ == "__main__":
    main()
