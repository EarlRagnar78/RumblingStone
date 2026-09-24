"""Il gate dei moduli standalone scritti in HTML (`10-stand-alone/*/`).

Perché esiste. Fino al 2026-09-02 questa famiglia di moduli non aveva **nessun**
controllo: la CI conosceva solo `STANDALONE-*`, e `L'abbazia Della Rotta Sicura`
— quattro file, ~2.750 righe — non era vista da niente. Un'ancora rotta o un id
duplicato si sarebbero scoperti al tavolo.

Questi test provano il gate su cartelle temporanee, non sull'Abbazia: un test che
dipende dal contenuto di un modulo vero diventa rosso il giorno in cui il DM lo
riscrive, che è l'opposto di ciò che serve.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from validate_standalone import check_aree_ambigue, check_html_module  # noqa: E402

BUONA = """<!DOCTYPE html><html lang="it"><head><title>Modulo</title></head>
<body><h1 id="titolo">Modulo</h1>
<p><a href="#titolo">su</a></p>
</body></html>"""


def _modulo(tmp: Path, **pagine: str) -> Path:
    mod = tmp / "Modulo di prova"
    mod.mkdir()
    for nome, html in pagine.items():
        (mod / f"{nome}.html").write_text(html, encoding="utf-8")
    return mod


class TestGateHtml(unittest.TestCase):

    def _esegui(self, **pagine: str) -> tuple[list[str], list[str]]:
        with tempfile.TemporaryDirectory() as d:
            mod = _modulo(Path(d), **pagine)
            errori: list[str] = []
            avvisi: list[str] = []
            check_html_module(mod, errori, avvisi)
            return errori, avvisi

    def test_una_pagina_sana_passa(self):
        errori, _ = self._esegui(indice=BUONA)
        self.assertEqual(errori, [])

    def test_senza_title_e_un_errore(self):
        errori, _ = self._esegui(indice=BUONA.replace("<title>Modulo</title>", ""))
        self.assertTrue(any("<title>" in e for e in errori), errori)

    def test_un_title_vuoto_non_conta_come_title(self):
        errori, _ = self._esegui(indice=BUONA.replace("<title>Modulo</title>",
                                                      "<title>   </title>"))
        self.assertTrue(any("<title>" in e for e in errori), errori)

    def test_senza_h1_e_un_errore(self):
        errori, _ = self._esegui(indice=BUONA.replace("<h1 id=", "<div id="))
        self.assertTrue(any("<h1>" in e for e in errori), errori)

    def test_ancora_interna_inesistente(self):
        errori, _ = self._esegui(indice=BUONA.replace('href="#titolo"', 'href="#fantasma"'))
        self.assertTrue(any("ancora inesistente" in e for e in errori), errori)

    def test_id_duplicato(self):
        errori, _ = self._esegui(indice=BUONA.replace("</body>", '<p id="titolo">bis</p></body>'))
        self.assertTrue(any("id duplicato" in e for e in errori), errori)

    def test_link_relativo_rotto(self):
        errori, _ = self._esegui(indice=BUONA.replace("</body>", '<a href="manca.html">x</a></body>'))
        self.assertTrue(any("link rotto" in e for e in errori), errori)

    def test_link_a_un_altro_file_del_modulo_con_ancora_buona(self):
        # rinomino l'id E l'ancora che lo punta: cambiarne uno solo
        # sarebbe il difetto che questo gate esiste per trovare.
        altra = BUONA.replace('id="titolo"', 'id="appendice"')\
                     .replace('href="#titolo"', 'href="#appendice"')
        errori, _ = self._esegui(
            indice=BUONA.replace("</body>", '<a href="appendice.html#appendice">x</a></body>'),
            appendice=altra,
        )
        self.assertEqual(errori, [])

    def test_ancora_inesistente_nel_file_di_destinazione(self):
        errori, _ = self._esegui(
            indice=BUONA.replace("</body>", '<a href="appendice.html#fantasma">x</a></body>'),
            appendice=BUONA,
        )
        self.assertTrue(any("ancora inesistente" in e for e in errori), errori)

    def test_i_link_esterni_non_si_verificano(self):
        errori, _ = self._esegui(
            indice=BUONA.replace("</body>", '<a href="https://esempio.invalid/x">x</a></body>'))
        self.assertEqual(errori, [])

    def test_termine_5e_nel_testo(self):
        errori, _ = self._esegui(indice=BUONA.replace("<p>", "<p>Usa un'azione bonus. "))
        self.assertTrue(any("termine vietato" in e for e in errori), errori)

    def test_un_termine_5e_dentro_uno_script_non_e_testo_di_gioco(self):
        errori, _ = self._esegui(
            indice=BUONA.replace("</body>", "<script>var x='azione bonus';</script></body>"))
        self.assertEqual(errori, [])

    def test_una_cartella_senza_html_e_un_errore(self):
        errori, _ = self._esegui()
        self.assertTrue(any("nessun file .html" in e for e in errori), errori)

    def test_il_modulo_a_solo_html_resta_dichiarato_come_tale(self):
        # Non è un errore: è l'avviso che impedisce di dimenticare che questo
        # modulo sta fuori da ADR-0003 e da entrambe le catene di impaginazione.
        _, avvisi = self._esegui(indice=BUONA)
        self.assertTrue(any("nessun master markdown" in a for a in avvisi), avvisi)


class TestNumerazioneAree(unittest.TestCase):
    """La numerazione delle aree: l'ambiguità vera, e i due modi di vederne una falsa."""

    def _w(self, **pagine: str) -> list[str]:
        with tempfile.TemporaryDirectory() as d:
            mod = _modulo(Path(d), **pagine)
            w: list[str] = []
            check_aree_ambigue(sorted(mod.glob("*.html")), "Modulo", w)
            return w

    def test_lo_stesso_numero_nudo_in_due_file_e_ambiguo(self):
        w = self._w(uno="<p>si torna in area 6 dopo</p>", due="<p>la chiave è in area 6</p>")
        self.assertTrue(any("«area 6»" in x and "2 file" in x for x in w), w)

    def test_col_prefisso_di_livello_non_e_piu_ambiguo(self):
        # È la correzione che l'indice maestro dell'Abbazia prescrive: i numeri
        # restano, cambia il prefisso — A6 (sacrestia) e B6 (cappella del borgo).
        w = self._w(uno="<p>si torna in A6 dopo</p>", due="<p>la chiave è in B6</p>")
        self.assertEqual(w, [])

    def test_due_celle_di_tabella_non_sono_una_frase(self):
        # Il falso positivo vero, trovato sull'Abbazia: dopo aver tolto i tag,
        # `…quella stanza</td><td>3</td>` diventava «stanza 3». Non è un rimando:
        # è una colonna accanto a un'altra.
        w = self._w(uno="<table><tr><td>due percorsi verso quella stanza</td><td>3</td></tr></table>",
                    due="<p>si torna in A3</p>")
        self.assertEqual(w, [])

    def test_un_rimando_vero_sulla_stessa_riga_si_vede_ancora(self):
        w = self._w(uno="<p>due percorsi verso la stanza 3 del piano</p>",
                    due="<p>si scende alla stanza 3 dal chiostro</p>")
        self.assertTrue(any("«area 3»" in x for x in w), w)

    def test_menzione_fra_virgolette_non_e_un_rimando(self):
        # Un documento che *spiega* il difetto scrive «area 17» apposta. Contarlo
        # vorrebbe dire chiedergli di riscrivere la spiegazione.
        w = self._w(uno="<p>Al tavolo &laquo;area 17&raquo; era ambiguo fra tre stanze.</p>",
                    due="<p>si sale in A17</p>")
        self.assertEqual(w, [])

    def test_le_entita_html_sono_testo(self):
        # Se `_testo` non le sciogliesse, la menzione qui sopra passerebbe per uso.
        w = self._w(uno="<p>&laquo;area 9&raquo; non voleva dire niente</p>",
                    due="<p>&laquo;area 9&raquo; nemmeno qui</p>")
        self.assertEqual(w, [])


if __name__ == "__main__":
    unittest.main()
