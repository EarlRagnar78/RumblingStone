"""I link relativi sopravvivono al cambio di cartella (lotto E1, 2026-09-12).

Il difetto: i due generatori di booklet **concatenavano il markdown sorgente
alla lettera**. Un capitolo in `07_arco/X.md` che linka `../plans/adr/Y.md`
punta alla radice del repo; incorporato in
`07_arco/homebrew/sessione/BOOKLET.hb.md` — due livelli piu' in basso — lo
stesso link finisce su `07_arco/homebrew/plans/adr/Y.md`, che non esiste.
Erano **41 link rotti su 44** in otto booklet.

⚠️ **La parte pericolosa non e' riscrivere: e' riscrivere troppo.** Un URL
assoluto, un'ancora o un segnaposto mai compilato **non sono percorsi**, e
toccarli produrrebbe link rotti dove prima non ce n'erano. Meta' dei test qui
sotto serve a quello.
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore.testo import link_e_relativo, riscala_link  # noqa: E402


class TestRiscalaQuelCheDeve(unittest.TestCase):
    def test_scende_di_un_livello(self):
        self.assertEqual(riscala_link("[a](../plans/x.md)", "07_arco", "07_arco/homebrew"),
                         "[a](../../plans/x.md)")

    def test_scende_di_due(self):
        self.assertEqual(
            riscala_link("[a](../plans/x.md)", "07_arco", "07_arco/homebrew/sessione"),
            "[a](../../../plans/x.md)")

    def test_risale(self):
        self.assertEqual(riscala_link("[a](img/x.png)", "07_arco/homebrew", "07_arco"),
                         "[a](homebrew/img/x.png)")

    def test_stessa_cartella_non_tocca_niente(self):
        testo = "[a](x.md) e ![b](img/y.png)"
        self.assertEqual(riscala_link(testo, "07_arco", "07_arco"), testo)

    def test_le_immagini_come_i_link(self):
        self.assertEqual(riscala_link("![i](img/a.png)", "07_arco", "07_arco/homebrew"),
                         "![i](../img/a.png)")

    def test_l_ancora_sopravvive(self):
        self.assertEqual(riscala_link("[a](../p/x.md#sez)", "07_arco", "07_arco/hb"),
                         "[a](../../p/x.md#sez)")

    def test_il_titolo_fra_virgolette_resta(self):
        self.assertEqual(riscala_link('[a](../p/x.md "T")', "07_arco", "07_arco/hb"),
                         '[a](../../p/x.md "T")')


class TestNonRiscalaQuelCheNonDeve(unittest.TestCase):
    """L'altra meta': riscrivere troppo romperebbe link che funzionavano."""

    def test_url_assoluti_intoccati(self):
        for dest in ("https://x.dev/a", "http://x.dev", "mailto:a@b.it", "//cdn.x/y"):
            testo = f"[a]({dest})"
            self.assertEqual(riscala_link(testo, "07_arco", "07_arco/hb"), testo, dest)

    def test_ancore_e_percorsi_assoluti_intoccati(self):
        for dest in ("#sezione", "/assets/logo.svg"):
            testo = f"[a]({dest})"
            self.assertEqual(riscala_link(testo, "07_arco", "07_arco/hb"), testo, dest)

    def test_i_segnaposto_non_si_inventano(self):
        """`URL` e' un buco del template: riscriverlo sarebbe inventare."""
        for dest in ("URL", "TODO", "{{percorso}}"):
            testo = f"![bg]({dest})"
            self.assertEqual(riscala_link(testo, "07_arco", "07_arco/hb"), testo, dest)

    def test_il_predicato_e_esplicito(self):
        self.assertTrue(link_e_relativo("../plans/x.md"))
        self.assertTrue(link_e_relativo("img/a.png"))
        for no in ("https://x.dev", "#s", "/x", "URL", "mailto:a@b", ""):
            self.assertFalse(link_e_relativo(no), no)


class TestSulRepoVero(unittest.TestCase):
    def test_nessun_link_rotto_nei_booklet(self):
        """Il criterio d'uscita del lotto E1: 0 su **tutti** i .hb.md."""
        import validate_docs as vd
        tops = vd._toplevel_dirs()
        rotti = []
        elencati = subprocess.run(["git", "ls-files", "-z", "*.hb.md"],
                                  cwd=ROOT, capture_output=True, text=True).stdout
        for f in elencati.split("\0"):
            if f:
                rotti += vd.check_doc(f, tops, solo_link=True)
        self.assertEqual(rotti, [], f"link rotti negli artefatti generati: {rotti}")

    def test_il_generatore_li_riscala_davvero(self):
        """Prova che morde: senza la riscalatura il link uscirebbe rotto."""
        senza = "[a](../plans/adr/ADR-0013-standard-generazione-booklet-sessioni.md)"
        # com'era prima della correzione: copiato alla lettera due livelli sotto
        rotto = (ROOT / "07_il Portale Della Forgia Eterna" / "homebrew" / "x" /
                 "../plans/adr/ADR-0013-standard-generazione-booklet-sessioni.md")
        self.assertFalse(rotto.exists(), "il percorso rotto non deve esistere")
        # con la correzione
        con = riscala_link(senza, "07_il Portale Della Forgia Eterna",
                           "07_il Portale Della Forgia Eterna/homebrew/x")
        dest = con[con.index("(") + 1:con.rindex(")")]
        self.assertTrue((ROOT / "07_il Portale Della Forgia Eterna" / "homebrew" / "x"
                         / dest).resolve().exists(), f"dopo la riscalatura: {dest}")


if __name__ == "__main__":
    unittest.main()
