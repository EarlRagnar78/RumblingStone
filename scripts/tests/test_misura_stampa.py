"""Le misure di stampa di un booklet (scripts/misura_stampa.py).

Il PDF di prova si costruisce con PyMuPDF: una riga nel margine, una scritta
da 5 pt, un font non incorporato, un riquadro che si spezza fra due pagine.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import misura_stampa as ms  # noqa: E402

try:
    import pymupdf
except ImportError:  # pragma: no cover
    pymupdf = None


class TestSegnaposti(unittest.TestCase):

    def test_coppie_e_riquadro_spezzato(self):
        schede = ms.accoppia_segnaposti([
            ["sb-inizio", "Xorn", 3], ["sb-fine", "Xorn", 3],
            ["sb-inizio", "Terros", 38], ["sb-fine", "Terros", 39],
        ])
        self.assertEqual(schede, [{"nome": "Xorn", "da": 3, "a": 3},
                                  {"nome": "Terros", "da": 38, "a": 39}])

    def test_una_fine_senza_inizio_non_conta(self):
        self.assertEqual(ms.accoppia_segnaposti([["sb-fine", "X", 1]]), [])


class TestTetti(unittest.TestCase):

    def test_sopra_il_tetto_e_booklet_nuovo(self):
        v = {m: 0 for m in ms.CON_TETTO} | {"font_non_incorporati": [], "schede_spezzate": 2}
        registrati = {"a": {"tetti": {m: 0 for m in ms.CON_TETTO} | {"schede_spezzate": 1}}}
        fuori = ms.sopra_il_tetto(registrati, {"a": v, "b": v})
        self.assertEqual(len(fuori), 2)
        self.assertIn("schede_spezzate = 2, il tetto è 1", fuori[0])
        self.assertIn("booklet nuovo", fuori[1])

    def test_sotto_il_tetto_passa(self):
        v = {m: 0 for m in ms.CON_TETTO} | {"font_non_incorporati": []}
        self.assertEqual(ms.sopra_il_tetto({"a": {"tetti": {m: 1 for m in ms.CON_TETTO}}}, {"a": v}), [])


@unittest.skipIf(pymupdf is None, "serve PyMuPDF")
class TestPdf(unittest.TestCase):

    def setUp(self):
        self.cartella = Path(__file__).parent / "_tmp_misura_stampa"
        self.cartella.mkdir(exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.cartella, ignore_errors=True)

    def test_margine_corpo_minimo_e_spezzate(self):
        doc = pymupdf.open()
        for _ in range(2):
            doc.new_page(width=595.28, height=841.89)
        pt = 72 / 2.54
        # Pagina 1 (destra): interno a sinistra, 2 cm. Una riga nel margine
        # interno e una regolare.
        doc[0].insert_text((1.0 * pt, 200), "fuori dalla gabbia", fontsize=10)
        doc[0].insert_text((2.2 * pt, 220), "dentro la gabbia", fontsize=10)
        doc[1].insert_text((2.2 * pt, 220), "scritta minuscola di una mappa", fontsize=5)
        doc[1].insert_text((2.2 * pt, 240), "12", fontsize=5)   # i numeri soli non contano
        pdf = self.cartella / "prova.pdf"
        doc.save(pdf)
        v = ms.misura_pdf(pdf, [{"nome": "Terros", "da": 1, "a": 2}])
        self.assertEqual(v["pagine"], 2)
        self.assertEqual(v["fuori_margine"], 1)
        self.assertEqual(v["testi_sotto_minimo"], 1)
        self.assertEqual(v["schede_spezzate"], 1)
        # PyMuPDF scrive con l'Helvetica di base, non incorporata: è proprio
        # il caso che una copisteria rifiuta.
        self.assertEqual(v["font_non_incorporati"], ["Helvetica"])

    def test_rimandi_di_pagina(self):
        """Un rimando giusto per tipo e uno sbagliato per tipo."""
        doc = pymupdf.open()
        for _ in range(3):
            doc.new_page(width=595.28, height=841.89)
        doc[0].insert_text((60, 100), "Xorn", fontsize=10)
        doc[0].insert_text((60, 112), "scheda a pagina 2", fontsize=10)
        doc[0].insert_text((60, 200), "Terros", fontsize=10)
        doc[0].insert_text((60, 212), "scheda a pagina 3", fontsize=10)      # Terros non è a p. 3
        doc[1].insert_text((60, 100), "Xorn", fontsize=10)
        doc[1].insert_text((60, 300), "continua a pagina 3", fontsize=10)    # niente «(segue)» a p. 3
        doc[1].insert_text((60, 400), "continua nella colonna accanto", fontsize=10)  # né a p. 2
        doc[2].insert_text((60, 100), "Drago", fontsize=10)
        pdf = self.cartella / "rimandi.pdf"
        doc.save(pdf)
        sbagliati = ms.rimandi_sbagliati(pymupdf.open(pdf))
        self.assertEqual([s[2] for s in sbagliati],
                         ["scheda a pagina 3", "continua a pagina 3", "continua nella colonna accanto"])
        doc = pymupdf.open(pdf)
        doc[2].insert_text((60, 130), "Terros (segue)", fontsize=10)
        doc[1].insert_text((300, 100), "Xorn (segue)", fontsize=10)
        pdf2 = self.cartella / "rimandi-giusti.pdf"
        doc.save(pdf2)
        self.assertEqual(ms.rimandi_sbagliati(pymupdf.open(pdf2)), [])

    def test_la_pagina_pari_ha_l_interno_a_destra(self):
        area = pymupdf.Rect(0, 0, 595.28, 841.89)
        dispari, pari = ms.area_di_stampa(area, 1, "a4"), ms.area_di_stampa(area, 2, "a4")
        self.assertGreater(dispari.x0, pari.x0)
        self.assertGreater(dispari.x1, pari.x1)


@unittest.skipIf(pymupdf is None or not shutil.which("typst"), "serve typst")
class TestSegnapostiNelTema(unittest.TestCase):
    """Il riquadro vero del tema lascia i due segnaposti e la misura li legge."""

    def test_un_riquadro_breve_non_si_spezza(self):
        import export_booklet_typst as ex
        corpo = ("```statblocco\nnome: Xorn\ngs: 6\nca: 24\npf: 52\nts: Temp +8\n```\n")
        typ = ROOT / "scripts" / "tests" / "_tmp_segnaposti.typ"
        typ.write_text(f'#import "../typst/tema-rumblingstone.typ": *\n{ex.md_to_typ(corpo)}\n',
                       encoding="utf-8")
        try:
            self.assertEqual(ms.interroga_schede(typ), [{"nome": "Xorn", "da": 1, "a": 1}])
        finally:
            typ.unlink(missing_ok=True)

    def test_appendice_una_scheda_per_creatura_e_tattica_nell_incontro(self):
        """ADR-0105 punto 7: due comparse della stessa creatura danno due righe
        con la loro tattica e un solo riquadro intero in appendice."""
        import export_booklet_typst as ex
        xorn = "```statblocco\nnome: Xorn\ngs: 6\nca: 24\npf: 52\nts: Temp +8\ntattica: {t}\n```\n"
        corpo = xorn.format(t="Sale dal pavimento.") + "\nTesto.\n\n" + xorn.format(t="Fugge nella roccia.")
        typ = ROOT / "scripts" / "tests" / "_tmp_appendice.typ"
        pdf = typ.with_suffix(".pdf")
        typ.write_text('#import "../typst/tema-rumblingstone.typ": *\n'
                       '#modo-schede.update("appendice")\n'
                       f'{ex.md_to_typ(corpo)}\n#appendice-creature()\n', encoding="utf-8")
        try:
            self.assertEqual(ms.interroga_schede(typ), [{"nome": "Xorn", "da": 2, "a": 2}])
            self.assertEqual(ex.compila("typst", typ, pdf)[0].returncode, 0)
            testo = "".join(p.get_text() for p in pymupdf.open(pdf))
            self.assertEqual(testo.count("scheda a pagina 2"), 2)
            self.assertIn("Sale dal pavimento.", testo)
            self.assertIn("Fugge nella roccia.", testo)
            self.assertEqual(testo.count("Appendice: le creature"), 1)
        finally:
            typ.unlink(missing_ok=True)
            pdf.unlink(missing_ok=True)


class TestAppendiceHtml(unittest.TestCase):
    """Le stesse due comparse nella via HTML e Homebrewery."""

    def test_html_e_homebrewery(self):
        import build_booklet_html as bh
        xorn = "```statblocco\nnome: Xorn\ngs: 6\nca: 24\npf: 52\nts: Temp +8\ntattica: {t}\n```"
        bh.APPENDICE = {}
        try:
            righe = [bh.statblocco_html(xorn.format(t=t)[14:-4]) for t in ("Sale.", "Fugge.")]
            self.assertEqual(len(bh.APPENDICE), 1)
            self.assertTrue(all('class="sb-riga"' in r for r in righe))
            self.assertIn("Fugge.", righe[1])
            self.assertNotIn("Sale.", next(iter(bh.APPENDICE.values()))[2])
        finally:
            bh.APPENDICE = None
        bh.APPENDICE_HB = {}
        try:
            hb = bh.statblocchi_homebrewery(xorn.format(t="Sale.") + "\n\n" + xorn.format(t="Fugge."))
            self.assertEqual(len(bh.APPENDICE_HB), 1)
            self.assertEqual(hb.count("*scheda in appendice*"), 2)
            self.assertNotIn("{{monster", hb)
        finally:
            bh.APPENDICE_HB = None


if __name__ == "__main__":
    unittest.main()
