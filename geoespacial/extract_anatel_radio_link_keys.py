#!/usr/bin/env python3
"""Recupera chaves cadastrais brutas dos radioenlaces e valida o extrato."""

from __future__ import annotations

import argparse, csv, gzip, io, json, os, tempfile
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

from audit_anatel_spectrum import number
from build_canonical_smp import deterministic_gzip_csv, sha256_file
from extract_anatel_radio_links import SERVICES

MEMBER = "Estacoes_Mosaico_STEL.csv"
FIELDS = (
    "link_family", "source_row_number", "identification_type", "entity_document",
    "entity", "service_fistel", "station_number", "rf_act_number", "service",
    "service_code_name", "origin", "validity_status", "station_class_code",
    "direction", "frequency_mhz", "latitude", "longitude", "ibge_code",
    "antenna_type_code", "antenna_homologation_code", "antenna_product_code",
    "transmitter_homologation_code", "transmitter_product_code",
)
RAW = {
    "identification_type": "Tipo de Identificação", "entity_document": "CNPJ ou CPF",
    "entity": "Nome Entidade", "service_fistel": "Fistel do Serviço da Estação",
    "station_number": "Número da Estação", "rf_act_number": "Número do Ato de RF",
    "service": "Serviço", "service_code_name": "Código e Nome do Serviço",
    "origin": "Origem", "validity_status": "Status da Validade da Estação",
    "station_class_code": "Tipo Classe Estação", "direction": "Direção de Comunicação",
    "frequency_mhz": "Frequência (MHz)", "latitude": "Latitude (graus)",
    "longitude": "Longitude (graus)", "ibge_code": "Código IBGE do Município",
    "antenna_type_code": "Código do Tipo Antena",
    "antenna_homologation_code": "Código de Homologação da Antena",
    "antenna_product_code": "Código de Produto da Antena",
    "transmitter_homologation_code": "Código de Homologação do Equipamento Transmissor",
    "transmitter_product_code": "Código de Produto do Transmissor",
}
COMPARE = ("station_number", "service", "service_code_name", "origin", "validity_status", "station_class_code", "direction", "frequency_mhz", "latitude", "longitude", "ibge_code")
NUMERIC_COMPARE = {"frequency_mhz", "latitude", "longitude"}


def clean(value: str | None) -> str:
    return (value or "").strip()


def extract(source_zip: Path, normalized: Path, output: Path, report: Path) -> dict:
    expected = {}
    with gzip.open(normalized, "rt", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            expected[int(row["source_row_number"])] = row
    availability = Counter()
    family_counts = Counter()
    mismatches = Counter()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="anatel-link-keys-", dir=output.parent) as directory:
        staged = Path(directory) / output.name
        with ZipFile(source_zip) as archive, archive.open(MEMBER) as raw, deterministic_gzip_csv(staged, FIELDS) as writer:
            reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""), delimiter=";")
            for row_number, row in enumerate(reader, 1):
                family = SERVICES.get(clean(row.get("Serviço")))
                if family is None:
                    continue
                values = {field: clean(row.get(source)) for field, source in RAW.items()}
                family_counts[family] += 1
                reference = expected.get(row_number)
                if reference is None:
                    mismatches["missing_normalized_row"] += 1
                else:
                    for field in COMPARE:
                        equivalent = (
                            number(values[field]) == number(reference.get(field, ""))
                            if field in NUMERIC_COMPARE else values[field] == clean(reference.get(field))
                        )
                        if not equivalent:
                            mismatches[field] += 1
                for field in ("service_fistel", "rf_act_number", "antenna_homologation_code", "antenna_product_code", "transmitter_homologation_code", "transmitter_product_code"):
                    availability[field] += bool(values[field])
                writer.writerow({"link_family": family, "source_row_number": row_number, **values})
        os.replace(staged, output)
    result = {
        "schema_version": 1, "source_file": str(source_zip), "source_sha256": sha256_file(source_zip),
        "source_member": MEMBER, "normalized_file": str(normalized), "normalized_sha256": sha256_file(normalized),
        "records": sum(family_counts.values()), "family_records": dict(sorted(family_counts.items())),
        "normalized_records": len(expected), "row_equivalence_mismatches": dict(sorted(mismatches.items())),
        "row_equivalence_confirmed": not mismatches and sum(family_counts.values()) == len(expected),
        "key_availability": dict(sorted(availability.items())), "pairing_status": "not_performed",
        "output": str(output),
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(prefix=f".{report.name}.", dir=report.parent, delete=False) as temporary:
        temporary.write(payload); staged_report = Path(temporary.name)
    os.replace(staged_report, report)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True); parser.add_argument("--normalized", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True); parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(); print(json.dumps(extract(args.source, args.normalized, args.output, args.report), ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
