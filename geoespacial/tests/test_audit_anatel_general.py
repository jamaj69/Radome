import csv
import gzip
import io
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from audit_anatel_general import DATASETS, audit, rf_role, usable_text


FIELDS = [
    "Número da Estação", "Nome Indicativo", "Nome Entidade",
    "Código e Nome do Serviço", "Serviço", "Origem",
    "Status da Validade da Estação", "Tipo Classe Estação", "Classe Estação",
    "Designação Emissão", "Polarização", "Ganho da Antena (dB)",
    "Frente Costa da Antena (dBi)", "Ângulo de Meia Potência da Antena (graus)",
    "Ângulo de Elevação (graus)", "Azimute (graus)", "Altura da Antena (m)",
    "Frequência (MHz)", "Direção de Comunicação", "Potência do Transmissor (W)",
    "Latitude (graus)", "Longitude (graus)", "Código IBGE do Município", "UF",
]


def csv_bytes(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter=";", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8-sig")


def row(**updates):
    result = {field: "" for field in FIELDS}
    result.update({
        "Número da Estação": "10", "Serviço": "Teste", "Origem": "STEL",
        "Status da Validade da Estação": "Ativo", "Tipo Classe Estação": "TX",
        "Classe Estação": "Estação Exclusivamente Transmissora",
        "Designação Emissão": "10M0G7W", "Polarização": "V",
        "Ganho da Antena (dB)": "10,5", "Altura da Antena (m)": "20",
        "Frequência (MHz)": "1000,5", "Direção de Comunicação": "N/I",
        "Potência do Transmissor (W)": "5,5", "Latitude (graus)": "-10",
        "Longitude (graus)": "-40", "Código IBGE do Município": "1234567",
    })
    result.update(updates)
    return result


class AnatelGeneralAuditTest(unittest.TestCase):
    def test_role_uses_direction_before_station_class(self):
        self.assertEqual(rf_role("Transmissão", "FR"), "explicit_transmission_direction")
        self.assertEqual(rf_role("Recepção", "TX"), "explicit_reception_direction")
        self.assertEqual(rf_role("", "BR"), "repeater_station_class")
        self.assertEqual(rf_role("", "FX"), "unknown")

    def test_invalid_placeholders_are_not_data(self):
        self.assertEqual(usable_text("N/I"), "")
        self.assertEqual(usable_text("Usuário informou errado"), "")
        self.assertEqual(usable_text("  Ativo "), "Ativo")

    def test_audit_preserves_records_and_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.zip"
            rows = [row(), row(**{"Número da Estação": "11", "Direção de Comunicação": "Recepção", "Tipo Classe Estação": "FR"})]
            with ZipFile(source, "w") as archive:
                for member in DATASETS.values():
                    archive.writestr(member, csv_bytes(rows))
            first = audit(source, root / "out1", root / "report1.json")
            second = audit(source, root / "out2", root / "report2.json")
            self.assertEqual(first["records"], 6)
            for dataset in DATASETS:
                self.assertEqual(first["datasets"][dataset]["records"], 2)
                self.assertEqual(first["datasets"][dataset]["active_potential_emitter_records"], 1)
                self.assertEqual((root / "out1" / f"{dataset}.csv.gz").read_bytes(), (root / "out2" / f"{dataset}.csv.gz").read_bytes())
                with gzip.open(root / "out1" / f"{dataset}.csv.gz", "rt", encoding="utf-8") as stream:
                    self.assertEqual(sum(1 for _ in csv.DictReader(stream)), 2)
            self.assertEqual((root / "report1.json").read_bytes(), (root / "report2.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
