import csv
import gzip
import io
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from build_canonical_smp import build, stable_identifier


HEADER = [
    "Número Estação", "NumSetor", "Latitude decimal", "Longitude decimal",
    "Código IBGE", "Empresa Estação", "Geração", "Tecnologia",
    "Tipo de Tecnologia 5G", "Faixa Estação", "Subfaixa Estação",
    "FreqTxMHz", "FreqRxMHz", "Designação Emissão", "Situacao",
]


def write_fixture(path: Path, rows: list[list[str]]) -> None:
    text = io.StringIO(newline="")
    writer = csv.writer(text, delimiter=";", lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    with ZipFile(path, "w") as archive:
        archive.writestr("Estacoes_SMP.csv", text.getvalue())


def read_gzip_csv(path: Path) -> list[dict[str, str]]:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


class CanonicalSmpTest(unittest.TestCase):
    def test_preserves_every_source_record_and_relations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "smp.zip"
            rows = [
                ["10", "1", "-10.123456", "-40.654321", "1234567", "OP", "4G", "LTE", "", "700", "A", "778", "723", "10M0G7W", "Licenciada"],
                ["10", "1", "-10.123456", "-40.654321", "1234567", "OP", "4G", "LTE", "", "700", "A", "788", "733", "10M0G7W", "Licenciada"],
                ["10", "2", "-10.123456", "-40.654321", "7654321", "OP", "5G", "NR", "SA", "3500", "N", "3500", "3500", "100MG7W", "Licenciada"],
            ]
            write_fixture(source, rows)
            summary = build(source, root / "out")
            sites = read_gzip_csv(root / "out/sites.csv.gz")
            antennas = read_gzip_csv(root / "out/antennas.csv.gz")
            emissions = read_gzip_csv(root / "out/emissions.csv.gz")
            self.assertTrue(summary["zero_loss"])
            self.assertEqual(summary["source_records"], 3)
            self.assertEqual(summary["emission_records"], 3)
            self.assertEqual(summary["site_assignment_records"], 3)
            self.assertEqual(summary["antenna_assignment_records"], 3)
            self.assertTrue(summary["site_cardinality_consistent"])
            self.assertTrue(summary["antenna_cardinality_consistent"])
            self.assertEqual(len(sites), 1)
            self.assertEqual(len(antennas), 2)
            self.assertEqual(len(emissions), 3)
            self.assertEqual(summary["sites_with_conflicting_municipal_codes"], 1)
            self.assertEqual({row["site_id"] for row in emissions}, {sites[0]["site_id"]})
            self.assertEqual({row["antenna_id"] for row in emissions}, {row["antenna_id"] for row in antennas})

    def test_invalid_coordinate_keeps_emission_without_inventing_site(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "smp.zip"
            write_fixture(source, [["10", "", "invalid", "-40", "", "OP", "2G", "GSM", "", "850", "A", "874.5", "829.5", "200KG7W", "Licenciada"]])
            summary = build(source, root / "out")
            emission = read_gzip_csv(root / "out/emissions.csv.gz")[0]
            self.assertTrue(summary["zero_loss"])
            self.assertEqual(summary["invalid_coordinate_records"], 1)
            self.assertEqual(emission["site_id"], "")
            self.assertEqual(emission["antenna_id"], "")

    def test_outputs_are_byte_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "smp.zip"
            write_fixture(source, [["10", "1", "-10", "-40", "1234567", "OP", "4G", "LTE", "", "700", "A", "778", "723", "10M0G7W", "Licenciada"]])
            build(source, root / "first")
            build(source, root / "second")
            for name in ("sites.csv.gz", "antennas.csv.gz", "emissions.csv.gz", "summary.json"):
                self.assertEqual((root / "first" / name).read_bytes(), (root / "second" / name).read_bytes())

    def test_identifier_is_stable_and_separates_sectors(self):
        one = stable_identifier("antenna", "site", "station", "1")
        self.assertEqual(one, stable_identifier("antenna", "site", "station", "1"))
        self.assertNotEqual(one, stable_identifier("antenna", "site", "station", "2"))


if __name__ == "__main__":
    unittest.main()
