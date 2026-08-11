#!/usr/bin/env python3
"""Extrai famílias explicitamente rotuladas como radioenlace, sem pareá-las."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from build_canonical_smp import deterministic_gzip_csv, sha256_file


SERVICES = {
    "Telefonia Fixa - Radioenlace": "stfc",
    "Banda Larga Fixa - Radioenlace": "scm",
    "Telefonia Móvel - Radioenlace": "smp",
}
FIELDS = (
    "link_family", "source_row_number", "station_number", "station_name",
    "entity", "service", "service_code_name", "origin", "validity_status",
    "station_class_code", "station_class", "direction", "rf_role_evidence",
    "emission_designation", "necessary_bandwidth_hz", "frequency_mhz",
    "transmitter_power_w", "polarization", "antenna_gain_db",
    "front_to_back_db", "half_power_beamwidth_deg", "elevation_angle_deg",
    "azimuth_deg", "antenna_height_m", "latitude", "longitude", "ibge_code",
    "state", "source_member",
)


def extract(source: Path, output: Path, report: Path) -> dict:
    counts = Counter()
    directions: dict[str, Counter[str]] = defaultdict(Counter)
    classes: dict[str, Counter[str]] = defaultdict(Counter)
    statuses: dict[str, Counter[str]] = defaultdict(Counter)
    stations: dict[str, set[str]] = defaultdict(set)
    coordinates: dict[str, set[tuple[str, str]]] = defaultdict(set)
    station_directions: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="anatel-links-", dir=output.parent) as temporary:
        staged = Path(temporary) / output.name
        with gzip.open(source, "rt", encoding="utf-8", newline="") as stream, deterministic_gzip_csv(staged, FIELDS) as writer:
            for record in csv.DictReader(stream):
                family = SERVICES.get(record.get("service", ""))
                if family is None:
                    continue
                counts[family] += 1
                direction = record.get("direction", "") or "N/I"
                station = record.get("station_number", "")
                latitude = record.get("latitude", "")
                longitude = record.get("longitude", "")
                directions[family][direction] += 1
                classes[family][record.get("station_class_code", "") or "N/I"] += 1
                statuses[family][record.get("validity_status", "") or "N/I"] += 1
                if station:
                    stations[family].add(station)
                    station_directions[family][station].add(direction)
                if latitude and longitude:
                    coordinates[family].add((latitude, longitude))
                writer.writerow({field: (family if field == "link_family" else record.get(field, "")) for field in FIELDS})
        os.replace(staged, output)

    families = {}
    for family in sorted(counts):
        both = sum({"Transmissão", "Recepção"} <= value for value in station_directions[family].values())
        families[family] = {
            "records": counts[family],
            "unique_station_numbers": len(stations[family]),
            "unique_coordinate_pairs": len(coordinates[family]),
            "station_numbers_with_tx_and_rx": both,
            "directions": dict(sorted(directions[family].items())),
            "station_classes": dict(sorted(classes[family].items())),
            "validity_statuses": dict(sorted(statuses[family].items())),
        }
    result = {
        "schema_version": 1,
        "source_file": str(source),
        "source_sha256": sha256_file(source),
        "selection_rule": "exact service label in STFC/SCM/SMP radio-link families; no endpoint pairing",
        "records": sum(counts.values()),
        "families": families,
        "pairing_status": "not_performed",
        "pairing_gate": "requires source cadastral keys, Tx/Rx reciprocity and geometric validation",
        "output": str(output),
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report_bytes = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with tempfile.NamedTemporaryFile(prefix=f".{report.name}.", dir=report.parent, delete=False) as temporary:
        temporary.write(report_bytes)
        temporary_report = Path(temporary.name)
    os.replace(temporary_report, report)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(extract(args.source, args.output, args.report), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
