import csv
import gzip
import tempfile
import unittest
from pathlib import Path

from audit_anatel_general import OUTPUT_FIELDS
from build_canonical_fixed_emitters import build, exclusion_reason
from build_canonical_smp import deterministic_gzip_csv


def record(**updates):
    result = {field: "" for field in OUTPUT_FIELDS}
    result.update({
        "source_row_number": "1", "source_member": "source.csv",
        "station_number": "10", "service": "Teste", "entity": "Entidade",
        "validity_status": "Ativo", "rf_role_evidence": "explicit_transmission_direction",
        "frequency_mhz": "1000.0", "transmitter_power_w": "5.0",
        "antenna_height_m": "20.0", "latitude": "-10.0", "longitude": "-40.0",
        "ibge_code": "1234567",
    })
    result.update(updates)
    return result


def write_input(path: Path, rows: list[dict]) -> None:
    with deterministic_gzip_csv(path, OUTPUT_FIELDS) as writer:
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


class CanonicalFixedEmittersTest(unittest.TestCase):
    def test_partition_priority_and_roles(self):
        self.assertEqual(exclusion_reason(record(validity_status="Vencido")), "not_active")
        self.assertEqual(exclusion_reason(record(rf_role_evidence="explicit_reception_direction")), "receiver_only")
        self.assertEqual(exclusion_reason(record(rf_role_evidence="unknown")), "unknown_rf_role")
        self.assertIsNone(exclusion_reason(record(rf_role_evidence="repeater_station_class")))

    def test_build_preserves_partition_and_relations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sarc = root / "sarc.csv.gz"
            scm = root / "scm.csv.gz"
            write_input(sarc, [record(), record(source_row_number="2", validity_status="Vencido")])
            write_input(scm, [
                record(source_row_number="1", station_number="20", longitude="-41"),
                record(source_row_number="2", station_number="21", rf_role_evidence="explicit_reception_direction"),
                record(source_row_number="3", station_number="22", rf_role_evidence="unknown"),
            ])
            summary = build({"sarc": sarc, "fixed_broadband": scm}, root / "out", root / "report.json")
            self.assertEqual(summary["emission_records"], 2)
            self.assertEqual(summary["datasets"]["sarc"]["quantitative_rf_ready_records"], 1)
            self.assertEqual(summary["datasets"]["sarc"]["site_records"], 1)
            self.assertTrue(summary["all_partitions_consistent"])
            self.assertTrue(summary["site_cardinality_consistent"])
            self.assertTrue(summary["antenna_cardinality_consistent"])
            self.assertEqual(len(read_rows(root / "out/emissions.csv.gz")), 2)
            self.assertEqual(len(read_rows(root / "out/sites.csv.gz")), 2)

    def test_outputs_are_byte_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sarc = root / "sarc.csv.gz"
            scm = root / "scm.csv.gz"
            write_input(sarc, [record()])
            write_input(scm, [record(station_number="20")])
            inputs = {"sarc": sarc, "fixed_broadband": scm}
            build(inputs, root / "one", root / "one.json")
            build(inputs, root / "two", root / "two.json")
            for name in ("sites.csv.gz", "antennas.csv.gz", "emissions.csv.gz", "summary.json"):
                self.assertEqual((root / "one" / name).read_bytes(), (root / "two" / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
