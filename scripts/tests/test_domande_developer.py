"""domande_developer: ogni regola morde, e il cancello del repo è verde.

Come per copertura_scene: un caso che deve far scattare la regola e uno che
deve lasciarla zitta. I casi del mondo vero stanno nella calibrazione
(`plans/esperimenti/domande-developer-def4/`).
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import domande_developer as dd  # noqa: E402

#: In una scena a parte, perché la sua CD non risponda per la scena sotto esame.
TUTTI_I_TS = "\n\n### SCENA 99 — I tiri\n\nTempra CD 15, Riflessi CD 15, Volontà CD 15.\n"


def regole(testo, profilo=None):
    return [(r, s) for r, s, _ in dd.analizza(testo + TUTTI_I_TS, profilo)]


class TestD2D4IlLuogoSorvegliato(unittest.TestCase):

    CAMPO = "### SCENA 1 — Il campo\n\nQuattro guardie di ronda e una pattuglia di lupi.\n"

    def test_senza_risposte_scattano_tutte_e_tre(self):
        r = [x[0] for x in regole(self.CAMPO)]
        self.assertEqual(r.count("D2"), 2)
        self.assertIn("D4", r)

    def test_con_le_risposte_tace(self):
        testo = self.CAMPO + ("Se volano, i lupi fiutano a 9 m. Chi è invisibile passa, ma "
                              "l'allarme arriva in 2 round.\n")
        self.assertEqual(regole(testo), [])

    def test_sentinella_maiuscola_e_un_nome(self):
        testo = "### SCENA 1 — Il tempio\n\nLa Sentinella di Mithral. La Sentinella si sveglia.\n"
        self.assertEqual(regole(testo), [])


class TestD1IlNemicoInVolo(unittest.TestCase):

    DRAGO = "### SCENA 1 — Il duello\n\nSkullcrusher, GS 12, resta in volo sopra le mura.\n"

    def test_niente_per_chi_resta_a_terra(self):
        self.assertIn(("D1", "SCENA 1"), regole(self.DRAGO))

    def test_a_terra_nella_descrizione_non_basta(self):
        testo = self.DRAGO + "Dove atterra, la pietra fuma a terra.\n"
        self.assertIn(("D1", "SCENA 1"), regole(testo))

    def test_la_risposta_scritta_tace(self):
        testo = self.DRAGO + "Chi non vola può tirare le catene degli arpioni.\n"
        self.assertNotIn(("D1", "SCENA 1"), regole(testo))


class TestD3ITreTiriSalvezza(unittest.TestCase):

    def test_manca_riflessi(self):
        fuori = dd.analizza("### SCENA 1 — X\n\nTempra CD 15. Volontà CD 18.\n")
        self.assertEqual([d for r, _, d in fuori if r == "D3"], ["nessun effetto chiede un TS su Riflessi"])

    def test_il_modulo_di_rito_dichiara_i_suoi(self):
        fuori = dd.analizza("### SCENA 1 — X\n\nVolontà CD 18.\n", {"ts_voluti": ["Volontà"]})
        self.assertEqual([r for r, _, _ in fuori if r == "D3"], [])


class TestD5IlBoss(unittest.TestCase):

    def test_boss_senza_soglia(self):
        testo = "## §8 — BOSS: Terros\n\nTerros attacca ogni round con il pugno.\n"
        self.assertIn(("D5", "§8 — BOSS: Terros"), regole(testo, {"scena": r"^## §\d+"}))

    def test_boss_con_soglia(self):
        testo = "## §8 — BOSS: Terros\n\nA 80 pf esita, e da lì cambia tattica.\n"
        self.assertNotIn("D5", [r for r, _ in regole(testo, {"scena": r"^## §\d+"})])

    def test_boss_dichiarato_da_una_tabella(self):
        testo = ("### SCENA 11 — Il duello\n\nIl drago colpisce.\n\n### SCENA 12 — Dopo\n\nx\n\n"
                 "| Scena 11: Skullcrusher (GS 12) | boss | 2.700 |\n")
        self.assertIn(("D5", "SCENA 11"), regole(testo))


class TestD6LoSkillChallenge(unittest.TestCase):

    def test_mezzo_scritto(self):
        testo = "### SCENA 1 — Il guado\n\n#### Skill challenge\n\nSi attraversa il fiume.\n"
        det = [d for r, _, d in dd.analizza(testo + TUTTI_I_TS) if r == "D6"]
        self.assertTrue(det and "quanti successi" in det[0] and "cosa si tira" in det[0])

    def test_scritto_per_intero(self):
        testo = ("### SCENA 1 — Il guado\n\n**6 successi prima di 3 fallimenti.** Ogni PG contribuisce: "
                 "Nuotare CD 15. Ogni successo avvicina la riva; ogni fallimento costa 1d6 danni.\n")
        self.assertNotIn("D6", [r for r, _ in regole(testo)])

    def test_numeri_diversi_in_due_punti(self):
        testo = ("### SCENA 1 — Il guado\n\n6 successi prima di 3 fallimenti. Ogni PG: Nuotare CD 15; "
                 "ogni successo avvicina; un fallimento costa.\n\n## Quick reference\n\n"
                 "Guado: 5 successi / 3 fallimenti\n")
        self.assertIn(("D6", "—"), regole(testo))

    def test_abilita_5e_in_35(self):
        self.assertIn("D6-5E", [r for r, _ in regole("Furtività CD 15 per entrare.")])

    def test_percezione_esiste_in_pf1e(self):
        self.assertNotIn("D6-5E", [r for r, _ in regole("Percezione CD 15.", {"sistema": "pf1e"})])
        self.assertIn("D6-5E", [r for r, _ in regole("Atletica CD 15.", {"sistema": "pf1e"})])

    def test_percezione_tremorica_non_e_un_abilita(self):
        self.assertNotIn("D6-5E", [r for r, _ in regole("Percezione tremorica 18 m.")])


class TestIlRepo(unittest.TestCase):

    def test_il_cancello_e_verde(self):
        self.assertEqual(dd.main(["--check"]), 0)

    def test_ogni_residuo_ha_la_ragione(self):
        for r in dd.carica_config()["residui"]:
            self.assertTrue(r.get("ragione"), r)

    def test_il_difetto_di_def4_e_chiuso_nel_testo(self):
        """Il playtester #42 (Tordek contro il drago in quota) era aperto fino al
        2026-09-27: la Scena 11 adesso dice cosa fa chi non vola, e nessun
        residuo deve più coprirlo."""
        master = ROOT / "07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md"
        rilievi = dd.analizza(master.read_text(encoding="utf-8"))
        self.assertNotIn(("D1", "SCENA 11"), [(r, s) for r, s, _ in rilievi])
        self.assertFalse([x for x in dd.carica_config()["residui"]
                          if x["regola"] == "D1" and x["scena"] == "SCENA 11"])


if __name__ == "__main__":
    unittest.main()
