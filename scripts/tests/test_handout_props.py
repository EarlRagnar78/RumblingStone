"""La guardia anti-regia degli handout: cosa NON deve finire in mano ai giocatori.

Nasce da un difetto vero (piano TRAVASO, lotto A5): la nota finale di
`ARC07-HANDOUTS.md` — quella che avverte di non rivelare il carry-over
Skullcrusher→Fauci — è finita STAMPATA dentro la carta delle Benedizioni,
perché apparteneva all'ultima sezione del file e il filtro non la conosceva.
Una guardia anti-spoiler che finisce nel prop è esattamente il difetto che
doveva impedire.
"""
import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
TOOL = REPO / "scripts" / "hype_homebrew.py"

spec = importlib.util.spec_from_file_location("hype_homebrew", TOOL)
hh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hh)


class TestStripRegiaDM(unittest.TestCase):
    def test_toglie_la_nota_anti_spoiler(self):
        testo = ("> *Il drago taglia il cielo.*\n\n"
                 "> **Nota anti-spoiler (B4)**: ferire Skullcrusher modifica Fauci.\n")
        fuori = hh.strip_dm_staging(testo)
        self.assertIn("Il drago taglia il cielo", fuori)
        self.assertNotIn("Skullcrusher", fuori)

    def test_toglie_quando_darlo(self):
        testo = ("> **Quando darlo**: all'arrivo nella Sala.\n\n"
                 "> *Otto affreschi, e uno è vuoto.*\n")
        fuori = hh.strip_dm_staging(testo)
        self.assertNotIn("Quando darlo", fuori)
        self.assertIn("uno è vuoto", fuori)

    def test_toglie_i_blockquote_che_citano_un_file_del_repo(self):
        """Nessun giocatore deve leggere il nome di un master sulla sua carta."""
        testo = ("> *La benedizione pesa come una mano sulla spalla.*\n\n"
                 "> (Valori dal master; verifica in `ERRATA-ARC07-35-Verification.md`.)\n")
        fuori = hh.strip_dm_staging(testo)
        self.assertIn("come una mano sulla spalla", fuori)
        self.assertNotIn("ERRATA", fuori)

    def test_non_tocca_la_finzione(self):
        """Il filtro deve essere cieco al testo in-fiction, anche lungo."""
        testo = ("> *Dalle Cronache di Thorgrim Barbadiferro, incise nella pietra:*\n"
                 "> *«Furono Quattro Eroi venuti da un tempo che non era ancora.»*\n")
        self.assertEqual(hh.strip_dm_staging(testo).strip(), testo.strip())


class TestPropDiARC07(unittest.TestCase):
    """I prop generati dell'arco non contengono regia né spoiler (lotto A5)."""

    PROPS = sorted((REPO / "07_il Portale Della Forgia Eterna" / "homebrew").glob("HANDOUT-*.hb.md"))

    def test_esistono(self):
        self.assertGreaterEqual(len(self.PROPS), 4, "i prop dell'arco non sono stati generati")

    def test_nessuno_contiene_regia_o_spoiler(self):
        for f in self.PROPS:
            testo = f.read_text(encoding="utf-8")
            corpo = "\n".join(ln for ln in testo.splitlines() if not ln.startswith("     "))
            for vietato in ("Quando darlo", "Nota anti-spoiler", "SOLO DM"):
                self.assertNotIn(vietato, corpo, f"{f.name} contiene regia DM: «{vietato}»")


if __name__ == "__main__":
    unittest.main()
