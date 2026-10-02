"""Test di ciclo_prosa.py (L12 di PIANO-AGENT-SKILLS-ESTERNE, ADR-0077)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import ciclo_prosa as cp  # noqa: E402

BOX = (
    "> **Read-aloud (LotR lead).** *Entrate nella sala. Un altare di basalto\n"
    "> sta al centro, e ti è sembrato più grande da fuori.*\n"
)


def _norme(testo):
    return sorted(s.norma for s in cp.segnala(testo))


class TestSegnala(unittest.TestCase):
    def test_p1_e_sembra_sulla_loro_riga(self):
        seg = {s.norma: s for s in cp.segnala(BOX)}
        self.assertEqual(seg["P1"].riga, 1)
        self.assertEqual(seg["sembra/pare"].riga, 2)

    def test_un_tic_minore_da_solo_non_conta(self):
        # Humanizer, «weak alone»: un «nel cuore di» è italiano corretto.
        self.assertNotIn("tic minori in gruppo", _norme("Nel cuore della notte il campo dorme.\n"))

    def test_due_tic_minori_diversi_si(self):
        testo = "La forgia rappresenta un vero e proprio patto fra i clan.\n"
        self.assertIn("tic minori in gruppo", _norme(testo))

    def test_lo_stesso_trattino_non_conta_due_volte(self):
        # «Non è X — è Y» è un'antitesi, non un'antitesi più un trattino.
        self.assertEqual(cp.tic_deboli("Non è una porta — è un muro."), ["antitesi"])

    def test_un_elenco_sono_voci_separate(self):
        righe = ["- La forgia rappresenta il patto.", "- Un vero e proprio muro."]
        self.assertEqual(cp._paragrafi(righe), [(0, 0), (1, 1)])

    def test_i_pg_non_sono_nomi_nuovi(self):
        box = "> *Thorik e Hella guardano l'altare.*\n"
        self.assertNotIn("box con più nomi propri", _norme(box))

    def test_l_etichetta_non_porta_trattini(self):
        self.assertEqual(cp._paragrafi(["**Read-aloud (X) — la sala.**"]), [(0, 0)])
        self.assertEqual(_norme("> **Read-aloud (X) — la sala.** *Non è una sala: è una tomba.*\n"), [])


class TestRevisione(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.orig, self.risc = d / "orig.md", d / "risc.md"
        self.orig.write_text("Prima riga.\n\n" + BOX + "\nCD 15 per aprire.\n", encoding="utf-8")
        self.risc.write_text("Prima riga.\n\n" + BOX.replace(
            "Entrate nella sala. ", "").replace("e ti è sembrato più grande da fuori", "e il fumo lo copre")
            + "\nCD 15 per aprire.\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_le_modifiche_vicine_sono_una(self):
        prima, dopo = self.orig.read_text(), self.risc.read_text()
        mods, marcato = cp._modifiche(prima, dopo, cp.segnala(prima))
        self.assertEqual(len(mods), 2)
        self.assertIn("{~~", marcato)
        self.assertIn("{>>#1<<}", marcato)

    def test_ogni_modifica_porta_la_sua_norma(self):
        prima, dopo = self.orig.read_text(), self.risc.read_text()
        mods, _ = cp._modifiche(prima, dopo, cp.segnala(prima))
        self.assertEqual([m.norme for m in mods], [["P1"], ["sembra/pare"]])

    def test_un_numero_cambiato_boccia_la_revisione(self):
        self.risc.write_text(self.risc.read_text().replace("CD 15", "CD 18"))
        testo, ok = cp.revisione(self.orig, self.risc)
        self.assertFalse(ok)
        self.assertIn("Nessun fatto cambia** (nomi propri, numeri, CD): NO", testo)

    def test_la_revisione_buona_passa(self):
        testo, ok = cp.revisione(self.orig, self.risc)
        self.assertTrue(ok)
        self.assertIn("| [ ] | 1 |", testo)

    def _revisione_su_disco(self, spunta):
        testo, _ = cp.revisione(self.orig, self.risc)
        for n in spunta:
            testo = testo.replace(f"| [ ] | {n} |", f"| [x] | {n} |")
        rev = Path(self.tmp.name) / "REVISIONE.md"
        rev.write_text(testo, encoding="utf-8")
        return rev

    def test_applica_solo_le_spuntate(self):
        rev = self._revisione_su_disco([1])
        with mock.patch.object(cp, "_ramo", return_value="claude/prova"):
            self.assertEqual(cp.applica(rev, "2026-10-02"), 0)
        nuovo = self.orig.read_text()
        self.assertTrue(nuovo.startswith("<!-- revisione-testo: r1 · 2026-10-02 -->"))
        self.assertNotIn("Entrate", nuovo)
        self.assertIn("sembrato", nuovo)          # la 2 non era spuntata

    def test_non_si_applica_su_main(self):
        rev = self._revisione_su_disco([1, 2])
        with mock.patch.object(cp, "_ramo", return_value="main"):
            self.assertEqual(cp.applica(rev, "2026-10-02"), 1)
        self.assertIn("Entrate", self.orig.read_text())

    def test_non_si_applica_due_volte(self):
        rev = self._revisione_su_disco([1])
        with mock.patch.object(cp, "_ramo", return_value="claude/prova"):
            self.assertEqual(cp.applica(rev, "2026-10-02"), 0)
            self.assertEqual(cp.applica(rev, "2026-10-02"), 1)


class TestLaRigaDiRevisione(unittest.TestCase):
    def test_sale_di_uno(self):
        t = "<!-- revisione-testo: r3 · 2026-09-01 -->\n# Titolo\n"
        self.assertEqual(cp.alza_revisione(t, "2026-10-02"),
                         "<!-- revisione-testo: r4 · 2026-10-02 -->\n# Titolo\n")

    def test_dopo_il_frontmatter(self):
        t = "---\ntitolo: x\n---\n# Titolo\n"
        self.assertTrue(cp.alza_revisione(t, "2026-10-02").startswith("---\ntitolo: x\n---\n<!-- revisione"))


if __name__ == "__main__":
    unittest.main()
