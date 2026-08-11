#!/usr/bin/env python3
"""Audita tecnologia e espectro declarado nas bases SMP e radiodifusão."""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile


DESIGNATION_BANDWIDTH = re.compile(r"^(\d{1,4})([HKGMT])([0-9]{0,3})")
UNIT_HZ = {"H": 1.0, "K": 1e3, "M": 1e6, "G": 1e9, "T": 1e12}


def emission_bandwidth_hz(designation: str) -> float | None:
    """Decodifica a largura necessária no início da designação ITU."""
    match = DESIGNATION_BANDWIDTH.match(designation.strip().upper())
    if not match:
        return None
    integer, unit, fraction = match.groups()
    mantissa = float(integer)
    if fraction:
        mantissa += int(fraction) / (10 ** len(fraction))
    return mantissa * UNIT_HZ[unit]


def number(value: str) -> float | None:
    try:
        return float(value.strip().replace(",", "."))
    except (AttributeError, ValueError):
        return None


def update_range(summary: dict, prefix: str, value: float | None) -> None:
    if value is None:
        summary[f"missing_{prefix}"] += 1
        return
    low, high = f"{prefix}_min_mhz", f"{prefix}_max_mhz"
    summary[low] = value if summary[low] is None else min(summary[low], value)
    summary[high] = value if summary[high] is None else max(summary[high], value)


def positive_frequency(value: float | None) -> float | None:
    return value if value is not None and value > 0 else None


def audit_smp(path: Path, output: Path) -> dict:
    fields = [
        "station_number", "sector", "ibge_code", "operator", "generation",
        "technology", "technology_5g_type", "station_band", "station_subband",
        "tx_center_mhz", "rx_center_mhz", "emission_designation",
        "necessary_bandwidth_hz", "tx_occupied_lower_mhz", "tx_occupied_upper_mhz",
        "situation",
    ]
    generations: dict[str, dict] = defaultdict(lambda: {
        "records": 0, "tx_min_mhz": None, "tx_max_mhz": None,
        "rx_min_mhz": None, "rx_max_mhz": None, "missing_tx": 0,
        "missing_rx": 0, "missing_designation": 0, "unparsed_designation": 0,
        "nonpositive_tx": 0, "nonpositive_rx": 0,
        "technologies": Counter(), "technology_5g_types": Counter(),
        "station_bands": Counter(), "designations": Counter(),
    })
    total = parsed = 0
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path) as archive, archive.open("Estacoes_SMP.csv") as raw, gzip.open(
        output, "wt", encoding="utf-8", newline=""
    ) as target:
        reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""), delimiter=";")
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        for record in reader:
            total += 1
            generation = record.get("Geração", "").strip() or "N/I"
            technology = record.get("Tecnologia", "").strip() or "N/I"
            designation = record.get("Designação Emissão", "").strip()
            tx = number(record.get("FreqTxMHz", ""))
            rx = number(record.get("FreqRxMHz", ""))
            bandwidth = emission_bandwidth_hz(designation)
            data = generations[generation]
            data["records"] += 1
            data["technologies"][technology] += 1
            data["technology_5g_types"][record.get("Tipo de Tecnologia 5G", "").strip() or "N/I"] += 1
            data["station_bands"][record.get("Faixa Estação", "").strip() or "N/I"] += 1
            data["designations"][designation or "N/I"] += 1
            data["missing_designation"] += int(not designation)
            data["unparsed_designation"] += int(bool(designation) and bandwidth is None)
            data["nonpositive_tx"] += int(tx is not None and tx <= 0)
            data["nonpositive_rx"] += int(rx is not None and rx <= 0)
            update_range(data, "tx", positive_frequency(tx))
            update_range(data, "rx", positive_frequency(rx))
            if bandwidth is not None:
                parsed += 1
            half_mhz = bandwidth / 2e6 if bandwidth is not None else None
            valid_tx = positive_frequency(tx)
            writer.writerow({
                "station_number": record.get("Número Estação", ""),
                "sector": record.get("NumSetor", ""),
                "ibge_code": record.get("Código IBGE", ""),
                "operator": record.get("Empresa Estação", ""),
                "generation": generation,
                "technology": technology,
                "technology_5g_type": record.get("Tipo de Tecnologia 5G", ""),
                "station_band": record.get("Faixa Estação", ""),
                "station_subband": record.get("Subfaixa Estação", ""),
                "tx_center_mhz": "" if tx is None else tx,
                "rx_center_mhz": "" if rx is None else rx,
                "emission_designation": designation,
                "necessary_bandwidth_hz": "" if bandwidth is None else bandwidth,
                "tx_occupied_lower_mhz": "" if valid_tx is None or half_mhz is None else valid_tx - half_mhz,
                "tx_occupied_upper_mhz": "" if valid_tx is None or half_mhz is None else valid_tx + half_mhz,
                "situation": record.get("Situacao", ""),
            })
    serializable = {}
    for generation, data in sorted(generations.items()):
        serializable[generation] = {
            **{key: value for key, value in data.items() if not isinstance(value, Counter)},
            "technologies": dict(data["technologies"].most_common()),
            "technology_5g_types": dict(data["technology_5g_types"].most_common()),
            "station_bands": dict(data["station_bands"].most_common()),
            "top_designations": dict(data["designations"].most_common(20)),
        }
    return {
        "records": total,
        "records_with_parsed_necessary_bandwidth": parsed,
        "normalized_emissions_gzip": str(output),
        "semantics": {
            "FreqTxMHz": "centro da emissão da estação SMP",
            "FreqRxMHz": "centro recebido pela estação; não é emissão da ERB",
            "necessary_bandwidth": "decodificada do prefixo da Designação Emissão ITU",
            "occupied_interval": "centro Tx ± metade da largura necessária; não inclui máscara fora de faixa",
        },
        "generations": serializable,
    }


def audit_broadcast(path: Path, output: Path) -> dict:
    fields = ["record_id", "service", "status", "channel", "source_frequency_value", "source_frequency_unit", "center_frequency_mhz", "ibge_municipality", "entity", "erp_source_value", "spectrum_status"]
    services: dict[str, dict] = defaultdict(lambda: {
        "records": 0, "licensed_records": 0, "center_min_mhz": None,
        "center_max_mhz": None, "licensed_center_min_mhz": None,
        "licensed_center_max_mhz": None, "missing_center": 0,
        "missing_licensed_center": 0,
        "source_units": Counter(), "statuses": Counter(),
    })
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path) as archive, archive.open("TV_FM_OM.csv") as raw, gzip.open(
        output, "wt", encoding="utf-8", newline=""
    ) as target:
        reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""), delimiter=";")
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        for record in reader:
            service = record.get("SiglaServico", "").strip() or "N/I"
            status = record.get("Sigla Status", "").strip() or "N/I"
            source_frequency = number(record.get("Frequência", ""))
            source_unit = "kHz" if service == "OM" else "MHz"
            center_mhz = source_frequency / 1000 if source_frequency is not None and source_unit == "kHz" else source_frequency
            data = services[service]
            data["records"] += 1
            data["licensed_records"] += int(status == "C4")
            data["statuses"][status] += 1
            data["source_units"][source_unit] += 1
            update_range(data, "center", center_mhz)
            if status == "C4":
                update_range(data, "licensed_center", center_mhz)
            writer.writerow({
                "record_id": record.get("_id", ""), "service": service,
                "status": status, "channel": record.get("Canal", ""),
                "source_frequency_value": "" if source_frequency is None else source_frequency,
                "source_frequency_unit": source_unit,
                "center_frequency_mhz": "" if center_mhz is None else center_mhz,
                "ibge_municipality": record.get("Município-UF", ""),
                "entity": record.get("Entidade", ""),
                "erp_source_value": record.get("ERP", ""),
                "spectrum_status": "center_frequency_only_bandwidth_absent_from_source",
            })
    serializable = {}
    for service, data in sorted(services.items()):
        serializable[service] = {
            **{key: value for key, value in data.items() if not isinstance(value, Counter)},
            "statuses": dict(data["statuses"].most_common()),
            "source_units": dict(data["source_units"].most_common()),
        }
    return {
        "records": sum(data["records"] for data in services.values()),
        "normalized_emissions_gzip": str(output),
        "spectrum_limitation": "a fonte declara canal e frequência, mas não largura/designação de emissão; limites ocupados não são calculáveis só com este CSV",
        "services": serializable,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smp", type=Path, required=True)
    parser.add_argument("--broadcast", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = {
        "smp": audit_smp(args.smp, args.output_dir / "smp_emissions.csv.gz"),
        "broadcast": audit_broadcast(args.broadcast, args.output_dir / "broadcast_emissions.csv.gz"),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"smp_records": result["smp"]["records"], "broadcast_records": result["broadcast"]["records"]}, indent=2))


if __name__ == "__main__":
    main()
