"""bundle_offline: zip riproducibile, ogni wheel verificata prima di installare (ADR-0116)."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import bundle_offline as B  # noqa: E402


def _ruote(d: Path) -> Path:
    r = d / "ruote"
    r.mkdir()
    (r / "a-1.0-py3-none-any.whl").write_bytes(b"uno")
    (r / "b-2.0-cp313-cp313-win_amd64.whl").write_bytes(b"due")
    return r


class TestCostruisci(unittest.TestCase):
    def test_due_costruzioni_danno_gli_stessi_byte(self):
        with tempfile.TemporaryDirectory() as t, mock.patch.dict(os.environ, {"SOURCE_DATE_EPOCH": "1794131399"}):
            d = Path(t)
            r = _ruote(d)
            a = B.costruisci("windows-x64", r, d / "o1").read_bytes()
            b = B.costruisci("windows-x64", r, d / "o2").read_bytes()
        self.assertEqual(a, b)

    def test_senza_wheel_non_si_costruisce(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            (d / "vuota").mkdir()
            with self.assertRaises(ValueError):
                B.costruisci("linux-x64", d / "vuota", d / "o")

    def test_il_zip_porta_requirements_e_le_impronte(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            zp = B.costruisci("linux-x64", _ruote(d), d / "o")
            nomi = zipfile.ZipFile(zp).namelist()
        radice = "rumblingstone-offline-linux-x64/"
        self.assertIn(radice + "requirements.txt", nomi)
        self.assertIn(radice + B.MANIFEST, nomi)
        self.assertIn(radice + "ruote/a-1.0-py3-none-any.whl", nomi)


class TestVerifica(unittest.TestCase):
    def test_una_wheel_cambiata_non_si_estrae(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            zp = B.costruisci("linux-x64", _ruote(d), d / "o")
            rotto = d / "rotto.zip"
            with zipfile.ZipFile(zp) as zin, zipfile.ZipFile(rotto, "w") as zout:
                for n in zin.namelist():
                    dati = b"altro" if n.endswith("a-1.0-py3-none-any.whl") else zin.read(n)
                    zout.writestr(n, dati)
            (d / "x").mkdir()
            with self.assertRaises(ValueError) as e:
                B.estrai_verificato(rotto, d / "x")
        self.assertIn("sha256", str(e.exception))

    def test_un_bundle_buono_si_estrae(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            zp = B.costruisci("linux-x64", _ruote(d), d / "o")
            (d / "x").mkdir()
            req = B.estrai_verificato(zp, d / "x")
            self.assertEqual(req.read_bytes(), B.REQUISITI.read_bytes())
            self.assertTrue((d / "x" / "ruote" / "b-2.0-cp313-cp313-win_amd64.whl").is_file())


class TestRequisiti(unittest.TestCase):
    def test_typst_e_pdfimpose_sono_nel_bundle_perche_sono_in_requirements(self):
        righe = B.REQUISITI.read_text(encoding="utf-8").splitlines()
        self.assertTrue(any(r.startswith("typst==") for r in righe))
        self.assertTrue(any(r.startswith("pdfimpose==") for r in righe))


if __name__ == "__main__":
    unittest.main()
