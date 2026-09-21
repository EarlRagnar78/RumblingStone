"""P1 — il read-aloud che presuppone un'azione del giocatore, provato all'indietro.

Meta' delle prove verifica che il rilevatore **taccia**: la seconda persona e'
legittima nel dialogo e nella visione, e un rilevatore che segnala tutto viene
spento dopo una settimana.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import misura_craft as mc  # noqa: E402


class TestP1(unittest.TestCase):

    def test_segnala_un_senso_presupposto(self):
        t = "> *La sala e' buia, e sentite il freddo salire dalle pietre.*\n"
        self.assertEqual(len(mc.box_con_p1(t)), 1)

    def test_segnala_un_azione_presupposta(self):
        t = "> *Entrate nella sala, e al centro c'e' un altare.*\n"
        self.assertEqual(len(mc.box_con_p1(t)), 1)

    def test_tace_sulla_descrizione_oggettiva(self):
        """La forma corretta secondo la norma: il box descrive quello che c'e'."""
        t = "> *Al centro della sala, un altare. Il freddo sale dalle pietre.*\n"
        self.assertEqual(mc.box_con_p1(t), [])

    def test_il_participio_non_e_una_seconda_persona(self):
        """Il falso positivo vero: «conta le candele avanzate»."""
        t = "> *Nonna Grasa conta le candele avanzate e ne restano undici.*\n"
        self.assertEqual(mc.box_con_p1(t), [])

    def test_non_guarda_fuori_dai_box(self):
        """La norma parla dei read-aloud, non della prosa di regia."""
        t = "Il DM chiede ai giocatori se entrate o aspettate.\n"
        self.assertEqual(mc.box_con_p1(t), [])

    def test_l_etichetta_non_conta(self):
        """`**Read-aloud (X).**` e' rivolta al DM e non si legge ad alta voce."""
        t = "> **Read-aloud (Mercer lead).** *Al centro, un altare di basalto.*\n"
        self.assertEqual(mc.box_con_p1(t), [])

    def test_gli_archivi_e_i_prompt_sono_fuori(self):
        snapshot = mc.cartelle_snapshot()
        self.assertTrue(snapshot, "il repo non ha piu' nessuno snapshot dichiarato")
        for f in mc.file_di_gioco_p1():
            self.assertFalse(any(s in f.parents for s in snapshot), f)
            self.assertNotIn("Immagini", f.parts, f)
            self.assertNotIn("_ARCHIVIO", f.parts, f)

    def test_il_conteggio_sul_repo_e_quello_pubblicato(self):
        """Se questo cambia, il piano 2C va rimisurato prima di proseguire."""
        tot = sum(len(mc.box_con_p1(f.read_text(encoding="utf-8", errors="replace")))
                  for f in mc.file_di_gioco_p1())
        self.assertGreater(tot, 0, "il rilevatore non pesca piu' niente: verificalo")
        self.assertLess(tot, 200, f"{tot} rilievi: il rilevatore si e' allargato")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
