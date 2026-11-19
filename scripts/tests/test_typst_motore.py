"""typst_motore: il pacchetto PyPI è lo standard, la CLI il ripiego (ADR-0116)."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import binari  # noqa: E402
import typst_motore as tm  # noqa: E402

FONT = REPO / "scripts" / "fonts"
PACCHETTI = REPO / "scripts" / "typst" / "packages"
DOC = ('#set page(width: 10cm, height: 6cm)\n'
       '#let c = sys.inputs.at("colore", default: "nero")\n'
       'Pietra #c <segno>\n')


class TestScelta(unittest.TestCase):
    def test_senza_variabile_vince_pypi_se_c_e(self):
        with mock.patch.object(tm, "_typst", object()), mock.patch.dict(os.environ, {tm.VARIABILE: ""}):
            self.assertEqual(tm.motore(), "pypi")

    def test_senza_pypi_si_ripiega_sulla_cli(self):
        with mock.patch.object(tm, "_typst", None), mock.patch.object(binari, "trova", return_value="/x/typst"), \
                mock.patch.dict(os.environ, {tm.VARIABILE: ""}):
            self.assertEqual(tm.motore(), "cli")

    def test_cli_chiesta_vince_su_pypi(self):
        with mock.patch.object(tm, "_typst", object()), mock.patch.object(binari, "trova", return_value="/x/typst"), \
                mock.patch.dict(os.environ, {tm.VARIABILE: "cli"}):
            self.assertEqual(tm.motore(), "cli")

    def test_pypi_chiesta_vieta_il_ripiego(self):
        with mock.patch.object(tm, "_typst", None), mock.patch.object(binari, "trova", return_value="/x/typst"), \
                mock.patch.dict(os.environ, {tm.VARIABILE: "pypi"}):
            self.assertIsNone(tm.motore())

    def test_senza_niente_esce_con_il_codice_di_binari(self):
        with mock.patch.object(tm, "_typst", None), mock.patch.object(binari, "trova", return_value=None), \
                mock.patch.dict(os.environ, {tm.VARIABILE: ""}), mock.patch("sys.stderr"):
            with self.assertRaises(SystemExit) as e:
                tm.esigi()
        self.assertEqual(e.exception.code, binari.MANCA)


class TestStessoRisultato(unittest.TestCase):
    """Lo stesso .typ con i due motori: stesso testo, stessa query, stessi ingressi."""

    def _con(self, motore: str, d: Path):
        typ, pdf = d / "p.typ", d / f"p-{motore}.pdf"
        typ.write_text(DOC, encoding="utf-8")
        with mock.patch.dict(os.environ, {tm.VARIABILE: motore, "SOURCE_DATE_EPOCH": "1794131399"}):
            if tm.motore() != motore:
                self.skipTest(f"motore {motore} assente")
            e = tm.compila(typ, pdf, root=d, font=FONT, pacchetti=PACCHETTI, solo_font_del_repo=True,
                           ingressi={"colore": "verde"})
            self.assertTrue(e.ok, e.errore)
            q = tm.valuta(typ, "query(<segno>).map(m => m.location().page())", root=d, font=FONT,
                          pacchetti=PACCHETTI, solo_font_del_repo=True)
        return pdf, q

    def test_pypi_e_cli_danno_lo_stesso_pdf(self):
        try:
            import pymupdf
        except ImportError:
            self.skipTest("PyMuPDF assente")
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            pa, qa = self._con("pypi", d)
            pb, qb = self._con("cli", d)
            ta = [p.get_text() for p in pymupdf.open(pa)]
            tb = [p.get_text() for p in pymupdf.open(pb)]
        self.assertEqual(ta, tb)
        self.assertIn("verde", ta[0])
        self.assertEqual(qa, qb)
        self.assertEqual(qa, [1])

    def test_un_errore_di_sorgente_non_e_un_successo(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            (d / "x.typ").write_text("#nonesiste()\n", encoding="utf-8")
            if not tm.disponibile():
                self.skipTest("typst assente")
            e = tm.compila(d / "x.typ", d / "x.pdf", root=d, font=FONT, pacchetti=PACCHETTI)
        self.assertFalse(e.ok)
        self.assertIn("nonesiste", e.errore)


class TestRequisito(unittest.TestCase):
    def test_typst_e_fissato_in_requirements(self):
        righe = (REPO / "requirements.txt").read_text(encoding="utf-8").splitlines()
        self.assertTrue(any(r.startswith("typst==") for r in righe),
                        "ADR-0020 §3 e ADR-0116: typst a versione fissata in requirements.txt")


if __name__ == "__main__":
    unittest.main()


# Un rimando che si sposta da solo: il numero della pagina del segno decide se
# prima del segno c'è una pagina in più, e la pagina in più cambia il numero.
OSCILLA = ('#set page(width: 10cm, height: 6cm)\n'
           '#context if calc.even(counter(page).at(<segno>).first()) { pagebreak() }\n'
           'Rimando a p. #context counter(page).at(<segno>).first()\n'
           '#pagebreak()\n'
           'Segno <segno>\n')


class TestNumeriInstabili(unittest.TestCase):
    """Un numero di pagina che non converge si vede negli avvisi (2026-11-19).

    Prima il ramo PyPI buttava via gli avvisi, e misura_stampa non vedeva il
    volume d'arco di ARC-07 con 15 rimandi su 242 sbagliati di una pagina.
    """

    def _compila(self, motore: str, sorgente: str) -> tm.Esito:
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            (d / "p.typ").write_text(sorgente, encoding="utf-8")
            with mock.patch.dict(os.environ, {tm.VARIABILE: motore}):
                if tm.motore() != motore:
                    self.skipTest(f"motore {motore} assente")
                return tm.compila(d / "p.typ", d / "p.pdf", root=d, font=FONT, pacchetti=PACCHETTI)

    def test_pypi_vede_il_numero_instabile(self):
        e = self._compila("pypi", OSCILLA)
        self.assertTrue(e.ok, e.errore)
        self.assertTrue(tm.numeri_instabili(e), e.avvisi)

    def test_cli_vede_il_numero_instabile(self):
        e = self._compila("cli", OSCILLA)
        self.assertTrue(e.ok, e.errore)
        self.assertTrue(tm.numeri_instabili(e), e.avvisi)

    def test_un_documento_stabile_non_ha_numeri_instabili(self):
        e = self._compila("pypi", DOC.replace('Pietra', 'Pietra, p. #context counter(page).at(<segno>).first()'))
        self.assertTrue(e.ok, e.errore)
        self.assertEqual(tm.numeri_instabili(e), [])

    def test_gli_altri_avvisi_non_contano(self):
        e = tm.Esito(True, "", False, avvisi=("a measured element did not stabilize · x",
                                              "document did not converge within five attempts"))
        self.assertEqual(tm.numeri_instabili(e), [])
