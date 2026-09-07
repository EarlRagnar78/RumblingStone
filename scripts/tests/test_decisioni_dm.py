"""Test del gate sulle decisioni aperte al DM (ADR-0047).

Il difetto che questo gate chiude non era una svista: `STATO-E-ORDINE` §4 era
scritto a mano, e il 2026-09-06 dava D1 aperta (decisa il giorno prima), non
elencava D6 (decisa due giorni prima), e conteneva **D7-D10 che non esistevano
in nessun piano**. Quindi qui non basta provare che il generatore generi: si
prova che il controllo **morde** su tutte e tre le forme dello sfasamento.
"""
import importlib.util
import io
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
MODULO = REPO / "scripts" / "decisioni_dm.py"

spec = importlib.util.spec_from_file_location("decisioni_dm", MODULO)
dd = importlib.util.module_from_spec(spec)
sys.modules["decisioni_dm"] = dd
spec.loader.exec_module(dd)


def _finto(root: Path, nome: str, corpo: str) -> None:
    (root / "plans").mkdir(parents=True, exist_ok=True)
    (root / "plans" / nome).write_text(corpo, encoding="utf-8")


class TestLetturaDelleFonti(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_legge_una_tabella_marcata(self):
        _finto(self.root, "PIANO-X.md",
               "# X\n\n<!-- decisioni-dm: X -->\n\n| # | Fase | Domanda |\n|---|---|---|\n"
               "| D1 | F1 | prima |\n| D2 | F2 | seconda |\n")
        d, e = dd.leggi_fonti(self.root)
        self.assertEqual(e, [])
        self.assertEqual([x.ident for x in d], ["D1", "D2"])
        self.assertTrue(all(x.aperta for x in d))

    def test_il_barrato_e_il_segno_di_chiusa(self):
        """Lo stato si legge da un segno, non si deduce dal testo."""
        _finto(self.root, "PIANO-X.md",
               "<!-- decisioni-dm: X -->\n\n| # | F | D |\n|---|---|---|\n"
               "| ~~D1~~ | F1 | decisa ieri |\n| D2 | F2 | aperta |\n")
        d, _ = dd.leggi_fonti(self.root)
        self.assertEqual([(x.ident, x.aperta) for x in d], [("D1", False), ("D2", True)])

    def test_una_tabella_senza_marker_non_conta(self):
        """`D<n>` non e' globale: in REVISIONE-ARC07 sono 17 decisioni gia' prese,
        e contarle qui accavallerebbe il Rubino con la griglia di P1C."""
        _finto(self.root, "PIANO-X.md", "<!-- decisioni-dm: X -->\n\n| # | F | D |\n|---|---|---|\n| D1 | F | x |\n")
        _finto(self.root, "PIANO-ALTRO.md",
               "# Decisioni acquisite\n\n| # | Decisione | Fonte |\n|---|---|---|\n| D1 | canone | DM |\n")
        d, e = dd.leggi_fonti(self.root)
        self.assertEqual(e, [])
        self.assertEqual(len(d), 1)
        self.assertEqual(d[0].piano, "X")

    def test_l_identita_e_piano_piu_numero(self):
        _finto(self.root, "A.md", "<!-- decisioni-dm: A -->\n\n| # | F | D |\n|---|---|---|\n| D1 | F | a |\n")
        _finto(self.root, "B.md", "<!-- decisioni-dm: B -->\n\n| # | F | D |\n|---|---|---|\n| D1 | F | b |\n")
        d, e = dd.leggi_fonti(self.root)
        self.assertEqual(e, [])
        self.assertEqual(sorted(x.chiave for x in d), ["A#D1", "B#D1"])

    def test_due_tabelle_con_la_stessa_etichetta_sono_un_errore(self):
        _finto(self.root, "A.md", "<!-- decisioni-dm: X -->\n\n| # | F | D |\n|---|---|---|\n| D1 | F | a |\n")
        _finto(self.root, "B.md", "<!-- decisioni-dm: X -->\n\n| # | F | D |\n|---|---|---|\n| D1 | F | b |\n")
        _, e = dd.leggi_fonti(self.root)
        self.assertTrue(any("duplicata" in x for x in e), e)

    def test_il_marker_citato_dentro_una_frase_non_conta(self):
        """Trovato dal gate su se stesso: la riga di CHANGELOG che racconta
        ADR-0047 cita il marker fra backtick, e senza l'ancoraggio a inizio riga
        diventava una tabella fantasma in un file che non ne ha nessuna."""
        _finto(self.root, "CHANGELOG.md",
               "| data | piano | lotto | rif | conta solo cio' che porta il marker "
               "`<!-- decisioni-dm: ... -->`, e l'identita' e' piano#Dn |\n")
        _finto(self.root, "A.md", "<!-- decisioni-dm: A -->\n\n| # | F | D |\n|---|---|---|\n| D1 | F | a |\n")
        d, e = dd.leggi_fonti(self.root)
        self.assertEqual(e, [])
        self.assertEqual([x.piano for x in d], ["A"])

    def test_un_marker_senza_tabella_e_un_errore(self):
        """Il caso che farebbe sparire in silenzio le decisioni di un piano."""
        _finto(self.root, "A.md", "<!-- decisioni-dm: A -->\n\nsolo prosa, nessuna riga.\n")
        _, e = dd.leggi_fonti(self.root)
        self.assertTrue(any("senza nessuna riga" in x for x in e), e)


class TestIlGateMorde(unittest.TestCase):
    """Le tre forme dello sfasamento vero del 2026-09-06."""

    def _decisioni(self, *triple):
        return [dd.Decisione(p, i, ap, "F", "testo") for p, i, ap in triple]

    def test_una_decisa_che_l_aggregato_da_ancora_aperta(self):
        prima = dd.rendi(self._decisioni(("P", "D1", True)))
        dopo = dd.rendi(self._decisioni(("P", "D1", False)))
        self.assertNotEqual(prima, dopo)

    def test_una_decisione_che_l_aggregato_non_elenca(self):
        senza = dd.rendi(self._decisioni(("P", "D1", True)))
        con = dd.rendi(self._decisioni(("P", "D1", True), ("P", "D6", True)))
        self.assertNotEqual(senza, con)
        self.assertIn("D6", con)
        self.assertNotIn("D6", senza)

    def test_una_riga_dell_aggregato_senza_fonte_sparisce(self):
        """D7-D10 esistevano SOLO nell'aggregato: rigenerando devono sparire,
        a meno che qualcuno non dia loro una casa in un piano."""
        reso = dd.rendi(self._decisioni(("P", "D1", True)))
        self.assertNotIn("D7", reso)

    def test_le_aperte_stanno_in_cima(self):
        reso = dd.rendi(self._decisioni(("P", "D1", False), ("P", "D2", True)))
        self.assertLess(reso.index("**D2**"), reso.index("~~D1~~"))

    def test_il_conteggio_e_scritto_e_non_va_indovinato(self):
        reso = dd.rendi(self._decisioni(("P", "D1", True), ("P", "D2", True), ("P", "D3", False)))
        self.assertIn("**2 aperte** · 1 chiuse", reso)


class TestSulRepoVero(unittest.TestCase):
    def test_il_repo_e_allineato(self):
        err = io.StringIO()
        with __import__("contextlib").redirect_stdout(io.StringIO()), \
                __import__("contextlib").redirect_stderr(err):
            codice = dd.main(["--check"])
        self.assertEqual(codice, 0, err.getvalue())

    def test_ogni_decisione_aperta_ha_un_piano_che_la_contiene(self):
        decisioni, errori = dd.leggi_fonti(REPO)
        self.assertEqual(errori, [])
        self.assertTrue(decisioni)
        for d in decisioni:
            self.assertTrue(d.piano and d.ident, d.chiave)

    def test_senza_argomenti_e_uso_errato(self):
        with __import__("contextlib").redirect_stdout(io.StringIO()):
            self.assertEqual(dd.main([]), 2)


if __name__ == "__main__":
    unittest.main()
