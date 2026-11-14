"""La scheda in una pagina a una colonna va su due colonne nel riquadro (ADR-0133).

Burnt Offerings e Red Hand of Doom stampano la scheda sempre in una colonna di
due. Nelle pagine a una colonna dei booklet il riquadro era largo tutta la
pagina, con righe da 130 caratteri e più: il tema divide il corpo in due
colonne pari. Il test compila il riquadro vero e legge dal PDF dove
cominciano le righe.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import typst_motore  # noqa: E402

try:
    import pymupdf
except ImportError:  # pragma: no cover
    pymupdf = None

QUI = Path(__file__).parent


def _scheda(nome: str, parole: int) -> str:
    quarto = " ".join(["parola"] * (parole // 4))
    return (f'#statblocco(nome: "{nome}", gs: "GS 5", ca: "13", pf: "40", ts: "+2", '
            f'sezioni: ("Difesa": [{quarto}], "Attacco": [{quarto}], '
            f'"Statistiche": [{quarto}], "Capacità speciali": [{quarto} ultimaparola]))\n')


def _righe(pdf: Path) -> list[tuple[int, float, int]]:
    """(pagina, x d'inizio, caratteri) di ogni riga del corpo della scheda."""
    righe = []
    for n, pagina in enumerate(pymupdf.open(pdf), 1):
        for blocco in pagina.get_text("dict")["blocks"]:
            for riga in blocco.get("lines", []):
                testo = "".join(s["text"] for s in riga["spans"]).strip()
                if testo.startswith("parola"):
                    righe.append((n, round(riga["bbox"][0] / 20) * 20, len(testo)))
    return righe


@unittest.skipIf(pymupdf is None or not typst_motore.disponibile(), "servono typst e PyMuPDF")
class TestSchedaDueColonne(unittest.TestCase):

    def _compila(self, nome: str, corpo: str) -> Path:
        import export_booklet_typst as ex
        typ = QUI / f"_tmp_{nome}.typ"
        pdf = typ.with_suffix(".pdf")
        typ.write_text(f'#import "../typst/tema-rumblingstone.typ": *\n{corpo}', encoding="utf-8")
        self.addCleanup(typ.unlink, missing_ok=True)
        self.addCleanup(pdf.unlink, missing_ok=True)
        esito = ex.compila("typst", typ, pdf)[0]
        self.assertEqual(esito.returncode, 0, esito.stderr[-800:])
        return pdf

    def test_pagina_a_una_colonna_il_corpo_va_su_due(self):
        righe = _righe(self._compila("col_una", _scheda("Media", 600)))
        self.assertEqual(len({x for _, x, _ in righe}), 2, "il corpo deve cominciare in due colonne")
        self.assertLess(max(c for _, _, c in righe), 90, "le righe restano sotto i 90 caratteri")

    def test_scheda_bassa_resta_intera(self):
        righe = _righe(self._compila("col_bassa", _scheda("Bassa", 24)))
        self.assertEqual(len({x for _, x, _ in righe}), 1)

    def test_pagina_a_due_colonne_non_cambia(self):
        righe = _righe(self._compila("col_due", "#set page(columns: 2)\n" + _scheda("Media", 600)))
        # la scheda si può spezzare fra le due colonne della pagina, ma dentro
        # una colonna il corpo comincia in un punto solo
        larghezza = pymupdf.open(QUI / "_tmp_col_due.pdf")[0].rect.width
        sinistra = {x for _, x, _ in righe if x < larghezza / 2}
        destra = {x for _, x, _ in righe if x >= larghezza / 2}
        self.assertLessEqual(len(sinistra), 1)
        self.assertLessEqual(len(destra), 1)

    def test_scheda_piu_alta_di_una_pagina_non_perde_testo(self):
        pdf = self._compila("col_alta", _scheda("Altissima", 4000))
        righe = _righe(pdf)
        pagine = sorted({n for n, _, _ in righe})
        self.assertGreater(len(pagine), 1, "la scheda deve passare alla pagina dopo")
        for n in pagine:
            self.assertEqual(len({x for p, x, _ in righe if p == n}), 2, f"pagina {n}: due colonne")
        testo = " ".join(p.get_text() for p in pymupdf.open(pdf))
        self.assertEqual(testo.split().count("parola"), 4000)
        self.assertIn("ultimaparola", testo)


if __name__ == "__main__":
    unittest.main()
