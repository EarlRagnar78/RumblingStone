"""Le carte da tavolo del Drappo (voce B3): dati dai master, forma da carte-tavolo.typ.

Il cancello ha tre parti. I dati: ogni numero sulla carta viene da una tabella
o da una frase del master, e un master che cambia forma ferma la lettura invece
di stampare carte vecchie. Il sorgente: trentasei carte, nove per foglio. La
stampa: il foglio compila PDF/UA-1 e PDF/A-2a coi soli font del repo, come i
booklet del volume.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import export_booklet_typst as ex  # noqa: E402
import typst_motore as tm  # noqa: E402
from dmcore import carte_tavolo as ct  # noqa: E402

DRAPPO = REPO / "10-stand-alone" / "Il-Drappo-di-Tarsilia"
REGOLE = DRAPPO / "REGOLE-DELLA-CORSA-PF1E.md"
CONTRADE = DRAPPO / "CONTRADE-DI-TARSILIA.md"
MANIFEST = DRAPPO / "homebrew" / "DRAPPO-CARTE-DA-TAVOLO.manifest.json"


class TestDatiDalMaster(unittest.TestCase):
    def test_otto_contrade_con_stemma(self):
        c = ct.contrade(CONTRADE)
        self.assertEqual([x.nome for x in c],
                         ["Oca", "Torre", "Bruco", "Istrice", "Drago", "Civetta", "Leocorno", "Onda"])
        self.assertTrue(all(x.stemma is not None and x.stemma.is_file() for x in c))
        self.assertEqual(c[3].motto, "Chi non ha niente divide lo stesso")

    def test_tratti_e_cd_come_nel_master(self):
        self.assertEqual([(t.nome, t.cd) for t in ct.tratti(REGOLE)],
                         [("Dritto", "12"), ("Curva Nord", "17"), ("Curva Sud", "15")])
        self.assertEqual(ct.giri(REGOLE), 3)
        self.assertEqual(ct.cavalli_alle_funi(REGOLE), 7)

    def test_posti_e_finte(self):
        self.assertEqual(len(ct.posti(REGOLE)), 6)
        self.assertEqual(len(ct.finte(REGOLE)), 3)

    def test_frase_presa_intera(self):
        self.assertEqual(ct.frase(REGOLE, "§4", "Costa **Morale"),
                         "Costa **Morale −2** e un nemico per tutta la vita.")

    def test_master_cambiato_ferma_la_lettura(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "r.md"
            f.write_text(REGOLE.read_text(encoding="utf-8").replace(
                "Sette cavalli entrano", "I cavalli entrano"), encoding="utf-8")
            with self.assertRaises(ct.CarteError):
                ct.cavalli_alle_funi(f)
            with self.assertRaises(ct.CarteError):
                ct.frase(f, "§4", "una frase che non c'è")


class TestSorgente(unittest.TestCase):
    def setUp(self):
        self.man = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.src = ex.sorgente(self.man, MANIFEST.parent, False)

    def test_quattro_fogli_trentasei_carte(self):
        self.assertEqual(self.src.count("#foglio-carte("), 4)
        self.assertEqual(len(re.findall(r"carta-\w+\(", self.src)), 36)

    def test_mazzetti(self):
        conta = {m: len(re.findall(rf"carta-{m}\(", self.src))
                 for m in ("contrada", "funi", "rincorsa", "tratto", "posto", "patto")}
        self.assertEqual(conta, {"contrada": 8, "funi": 7, "rincorsa": 1, "tratto": 9,
                                 "posto": 6, "patto": 5})

    def test_cd_dei_tratti_dal_master(self):
        self.assertEqual(re.findall(r'carta-tratto\(giro: "(\w+)", nome: "([^"]+)", cd: "(\d+)"', self.src)[:3],
                         [("I", "Dritto", "12"), ("I", "Curva Nord", "17"), ("I", "Curva Sud", "15")])

    def test_il_manifest_senza_contrade_si_ferma(self):
        man = json.loads(json.dumps(self.man))
        del man["chapters"][0]["contrade"]
        with self.assertRaises(ct.CarteError):
            ex.sorgente(man, MANIFEST.parent, False)


@unittest.skipUnless(tm.disponibile(), "typst assente")
class TestStampa(unittest.TestCase):
    def test_pdf_ua_1_e_pdf_a_2a_coi_soli_font_del_repo(self):
        man = json.loads(MANIFEST.read_text(encoding="utf-8"))
        src = ex.sorgente(man, MANIFEST.parent, False)
        with tempfile.TemporaryDirectory(dir=MANIFEST.parent) as d:
            typ, pdf = Path(d) / "c.typ", Path(d) / "c.pdf"
            typ.write_text(src, encoding="utf-8")
            e = tm.compila(typ, pdf, root=REPO, font=ex.FONTS, pacchetti=ex.PACCHETTI,
                           solo_font_del_repo=True, pdfua=True, pdfa=ex.PDFA)
            self.assertTrue(e.ok, e.errore)
            self.assertEqual((e.pdfua, e.pdfa, e.senza_tag), (True, "a-2a", False), e.motivo_pdfa)
            try:
                import pymupdf
            except ImportError:
                return
            doc = pymupdf.open(pdf)
            self.assertEqual(len(doc), 4)
            testo = doc[0].get_text()
            # le scritte del Palio dentro gli scudi non arrivano sulla carta
            self.assertNotIn("Pungo solo chi mi assale", testo)
            self.assertIn("Chi non ha niente divide lo stesso", testo)


if __name__ == "__main__":
    unittest.main()
