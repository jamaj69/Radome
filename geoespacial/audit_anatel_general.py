#!/usr/bin/env python3
"""Audita por streaming os arquivos menores do pacote geral da Anatel."""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import tempfile
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

from audit_anatel_spectrum import emission_bandwidth_hz, number
from build_canonical_smp import deterministic_gzip_csv, sha256_file


DATASETS = {
    "sarc": "Estacoes_SARC.csv",
    "fixed_broadband": "Estacoes_Banda_Larga_Fixa.csv",
    "fixed_telephony": "Estacoes_Telefonia_Fixa.csv",
    "sle": "Estacoes_SLE.csv",
}
INVALID_TEXT = {"", "N/I", "USUÁRIO INFORMOU ERRADO", "USUARIO INFORMOU ERRADO"}
OUTPUT_FIELDS = (
    "dataset", "source_row_number", "source_member", "service",
    "service_code_name", "station_number", "station_name", "entity", "origin",
    "validity_status", "station_class_code", "station_class", "direction",
    "rf_role_evidence", "emission_designation", "necessary_bandwidth_hz",
    "frequency_mhz", "transmitter_power_w", "polarization", "antenna_gain_db",
    "front_to_back_db", "half_power_beamwidth_deg", "elevation_angle_deg",
    "azimuth_deg", "antenna_height_m", "latitude", "longitude", "ibge_code",
    "state",
)
NUMERIC_FIELDS = {
    "frequency_mhz": "Frequência (MHz)",
    "transmitter_power_w": "Potência do Transmissor (W)",
    "antenna_gain_db": "Ganho da Antena (dB)",
    "front_to_back_db": "Frente Costa da Antena (dBi)",
    "half_power_beamwidth_deg": "Ângulo de Meia Potência da Antena (graus)",
    "elevation_angle_deg": "Ângulo de Elevação (graus)",
    "azimuth_deg": "Azimute (graus)",
    "antenna_height_m": "Altura da Antena (m)",
}


def usable_text(value: str | None) -> str:
    cleaned = (value or "").strip()
    return "" if cleaned.upper() in INVALID_TEXT else cleaned


def rf_role(direction: str, station_class_code: str) -> str:
    if direction == "Transmissão":
        return "explicit_transmission_direction"
    if direction == "Recepção":
        return "explicit_reception_direction"
    if station_class_code in {"TX", "TE"}:
        return "transmitter_station_class"
    if station_class_code == "FR":
        return "receiver_only_station_class"
    if station_class_code in {"BR", "XR"}:
        return "repeater_station_class"
    return "unknown"


def sorted_counter(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))


def audit_member(archive: ZipFile, dataset: str, member: str, output: Path) -> dict:
    counters = {
        name: Counter() for name in (
            "services", "service_codes", "validity_statuses", "station_classes",
            "directions", "origins", "rf_roles",
        )
    }
    availability = Counter()
    records = valid_coordinates = valid_ibge_codes = active_potential_emitters = 0
    frequency_min = frequency_max = power_min = power_max = None

    with archive.open(member) as raw, deterministic_gzip_csv(output, OUTPUT_FIELDS) as writer:
        reader = csv.DictReader(
            io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""), delimiter=";"
        )
        missing_columns = {
            source for source in NUMERIC_FIELDS.values() if source not in (reader.fieldnames or [])
        }
        if missing_columns:
            raise ValueError(f"Colunas ausentes em {member}: {sorted(missing_columns)}")
        for source_row_number, record in enumerate(reader, 1):
            records += 1
            service = usable_text(record.get("Serviço"))
            service_code = usable_text(record.get("Código e Nome do Serviço"))
            status = usable_text(record.get("Status da Validade da Estação"))
            class_code = usable_text(record.get("Tipo Classe Estação"))
            station_class = usable_text(record.get("Classe Estação"))
            direction = usable_text(record.get("Direção de Comunicação"))
            origin = usable_text(record.get("Origem"))
            role = rf_role(direction, class_code)
            for key, value in (
                ("services", service), ("service_codes", service_code),
                ("validity_statuses", status), ("station_classes", class_code),
                ("directions", direction), ("origins", origin), ("rf_roles", role),
            ):
                counters[key][value or "N/I"] += 1

            numeric = {key: number(record.get(source, "")) for key, source in NUMERIC_FIELDS.items()}
            for key, value in numeric.items():
                availability[key] += int(value is not None)
            frequency = numeric["frequency_mhz"]
            power = numeric["transmitter_power_w"]
            if frequency is not None and frequency > 0:
                frequency_min = frequency if frequency_min is None else min(frequency_min, frequency)
                frequency_max = frequency if frequency_max is None else max(frequency_max, frequency)
            if power is not None and power >= 0:
                power_min = power if power_min is None else min(power_min, power)
                power_max = power if power_max is None else max(power_max, power)

            latitude = number(record.get("Latitude (graus)", ""))
            longitude = number(record.get("Longitude (graus)", ""))
            coordinates_valid = (
                latitude is not None and longitude is not None
                and -90 <= latitude <= 90 and -180 <= longitude <= 180
            )
            valid_coordinates += int(coordinates_valid)
            ibge_code = usable_text(record.get("Código IBGE do Município"))
            valid_ibge_codes += int(len(ibge_code) == 7 and ibge_code.isdigit())
            designation = usable_text(record.get("Designação Emissão"))
            bandwidth = emission_bandwidth_hz(designation) if designation else None
            availability["emission_designation"] += int(bool(designation))
            availability["parsed_necessary_bandwidth"] += int(bandwidth is not None)
            availability["polarization"] += int(bool(usable_text(record.get("Polarização"))))
            potential_emitter = role in {
                "explicit_transmission_direction", "transmitter_station_class",
                "repeater_station_class",
            }
            active_potential_emitters += int(status == "Ativo" and potential_emitter)

            writer.writerow({
                "dataset": dataset, "source_row_number": source_row_number,
                "source_member": member, "service": service,
                "service_code_name": service_code,
                "station_number": usable_text(record.get("Número da Estação")),
                "station_name": usable_text(record.get("Nome Indicativo")),
                "entity": usable_text(record.get("Nome Entidade")), "origin": origin,
                "validity_status": status, "station_class_code": class_code,
                "station_class": station_class, "direction": direction,
                "rf_role_evidence": role, "emission_designation": designation,
                "necessary_bandwidth_hz": "" if bandwidth is None else bandwidth,
                **{key: "" if value is None else value for key, value in numeric.items()},
                "polarization": usable_text(record.get("Polarização")),
                "latitude": "" if latitude is None else latitude,
                "longitude": "" if longitude is None else longitude,
                "ibge_code": ibge_code, "state": usable_text(record.get("UF")),
            })

    return {
        "source_member": member,
        "source_member_crc32": f"{archive.getinfo(member).CRC:08x}",
        "records": records,
        "valid_coordinate_records": valid_coordinates,
        "valid_ibge_code_records": valid_ibge_codes,
        "active_potential_emitter_records": active_potential_emitters,
        "frequency_min_mhz": frequency_min,
        "frequency_max_mhz": frequency_max,
        "transmitter_power_min_w": power_min,
        "transmitter_power_max_w": power_max,
        "available_fields": dict(sorted(availability.items())),
        **{key: sorted_counter(value) for key, value in counters.items()},
        "normalized_output": f"outputs/anatel_general_audit/{dataset}.csv.gz",
    }


def audit(source_zip: Path, output_dir: Path, report: Path) -> dict:
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="anatel-general-", dir=output_dir.parent) as temporary:
        staging = Path(temporary)
        with ZipFile(source_zip) as archive:
            missing = set(DATASETS.values()) - set(archive.namelist())
            if missing:
                raise ValueError(f"Arquivos ausentes no pacote Anatel: {sorted(missing)}")
            datasets = {
                dataset: audit_member(archive, dataset, member, staging / f"{dataset}.csv.gz")
                for dataset, member in DATASETS.items()
            }
        result = {
            "schema_version": 1,
            "source_file": str(source_zip),
            "source_sha256": sha256_file(source_zip),
            "records": sum(item["records"] for item in datasets.values()),
            "scope": list(DATASETS),
            "classification_rule": "RF role uses explicit communication direction first, then exclusive transmitter/receiver or repeater station class; unknown is not inferred as emission",
            "datasets": datasets,
        }
        report_bytes = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        (staging / "summary.json").write_bytes(report_bytes)
        output_dir.mkdir(parents=True, exist_ok=True)
        for name in (*[f"{dataset}.csv.gz" for dataset in DATASETS], "summary.json"):
            os.replace(staging / name, output_dir / name)
        report.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(prefix=f".{report.name}.", dir=report.parent, delete=False) as temp:
            temp.write(report_bytes)
            temp_path = Path(temp.name)
        os.replace(temp_path, report)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.source, args.output_dir, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
