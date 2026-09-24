"""Il travaso HTML → master markdown: i modi in cui perde roba senza dirlo.

Un convertitore rumoroso si aggiusta; uno silenzioso consegna un master a cui
manca qualcosa, e il buco si scopre al tavolo. Ogni test qui sotto nasce da un
difetto **vero**, trovato guardando la pagina impaginata dell'Abbazia e non
leggendo il codice:

- il `viewBox` minuscolato (SVG e' XML: `viewbox` non esiste), che toglieva alla
  tavola la sua scala e, con `patternUnits`, trasformava il riempimento del mare
  in **un quadratino azzurro nell'angolo**;
- `<path/></path>`, XML non valido, perche' `html.parser` consegna un elemento
  autochiuso come start **e** end;
- i `<defs>` condivisi lasciati indietro, che rendevano ogni tavola dipendente da
  un file che non c'e' piu';
- il `<br>` dentro una cella, che sparava i nomi **fuori** dalla tabella;
- «** **» fra due neretti adiacenti, cancellato insieme allo spazio: `megereGrinza`.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from import_html_module import _generato, converti  # noqa: E402

TESTA = '<!DOCTYPE html><html lang="it"><head><title>T</title></head><body><div class="page">'
CODA = "</div></body></html>"


def _conv(corpo: str) -> tuple[str, list[Path]]:
    """Converte un frammento e restituisce (markdown, tavole scritte)."""
    d = Path(tempfile.mkdtemp())
    src = d / "prova.html"
    src.write_text(TESTA + corpo + CODA, encoding="utf-8")
    md, _ = converti(src, d, d / "tavole", dry=False)
    return md, sorted((d / "tavole").glob("*.svg"))


class TestTavole(unittest.TestCase):
    SVG = ('<svg width="0" height="0"><defs>'
           '<pattern id="wat" width="20" height="14" patternUnits="userSpaceOnUse">'
           '<rect width="20" height="14" fill="#b9d3e0"/></pattern></defs></svg>'
           '<figure><svg viewBox="0 0 100 50" preserveAspectRatio="xMidYMid meet">'
           '<rect x="0" y="0" width="100" height="50" fill="url(#wat)"/>'
           '<path d="M0 0 L9 4"/></svg>'
           "<figcaption>Il mare</figcaption></figure>")

    def test_la_tavola_esce_in_un_file_e_il_markdown_la_cita(self):
        md, tavole = _conv(self.SVG)
        self.assertEqual(len(tavole), 1)
        self.assertIn("![Il mare](tavole/", md)

    def test_la_tavola_e_xml_valido(self):
        # `<path .../>` arrivava come start+end e usciva `<path/></path>`.
        _, tavole = _conv(self.SVG)
        ET.parse(tavole[0])  # solleva se non lo e'

    def test_gli_attributi_svg_mantengono_le_maiuscole(self):
        # `html.parser` minuscola tutto; XML e' case-sensitive. Senza questo la
        # tavola perde scala e riempimenti, e il file resta comunque «valido».
        _, tavole = _conv(self.SVG)
        t = tavole[0].read_text(encoding="utf-8")
        for a in ("viewBox", "preserveAspectRatio", "patternUnits"):
            self.assertIn(a, t, f"{a} minuscolato")
        self.assertNotIn("viewbox", t)

    def test_la_tavola_e_autonoma_porta_con_se_i_defs(self):
        _, tavole = _conv(self.SVG)
        t = tavole[0].read_text(encoding="utf-8")
        usati = set(re.findall(r"url\(#([\w-]+)\)", t))
        definiti = set(re.findall(r'id="([\w-]+)"', t))
        self.assertTrue(usati <= definiti, f"riferimenti pendenti: {usati - definiti}")

    def test_i_defs_condivisi_non_finiscono_nel_testo(self):
        md, _ = _conv(self.SVG)
        self.assertNotIn("pattern", md)


class TestStruttura(unittest.TestCase):
    def test_br_dentro_una_cella_resta_nella_cella(self):
        # Il difetto vero: `<td><b>Dama Orsola Rive</b><br>guerriero 5</td>`
        # perdeva il nome dalla tabella e lo accodava a un paragrafo di nomi.
        md, _ = _conv("<table><tr><td><b>Orsola</b><br>guerriero 5</td>"
                      "<td>Capoguardia</td></tr></table>")
        riga = next(l for l in md.splitlines() if "Orsola" in l)
        self.assertTrue(riga.startswith("|"), f"il nome è uscito dalla tabella: {riga!r}")
        self.assertIn("guerriero 5", riga)

    def test_br_in_uno_statblocco_separa_le_righe(self):
        # Uno statblocco unito in un paragrafo unico non si consulta piu'.
        md, _ = _conv('<div class="sb"><b>PF</b> 45<br><b>CA</b> 23<br><b>TS</b> +5</div>')
        corpo = md[md.index("{{note"):]
        self.assertEqual(len([l for l in corpo.splitlines() if l.startswith("**")]), 3)

    def test_due_neretti_adiacenti_non_si_incollano(self):
        md, _ = _conv("<p><b>concilio di megere</b> <b>Grinza</b> (GS 4)</p>")
        self.assertNotIn("megereGrinza", md)
        self.assertIn("megere** **Grinza", md)

    def test_un_neretto_vuoto_non_produce_asterischi_orfani(self):
        md, _ = _conv("<p>prima<b></b>dopo</p>")
        self.assertNotIn("****", md)
        self.assertIn("primadopo", md)

    def test_il_read_aloud_diventa_un_blockquote(self):
        # Sta su `<p class="ra">`, non su un div: la prima versione non lo
        # vedeva e appiattiva **undici** blocchi di read-aloud in prosa
        # normale. Al tavolo e' la differenza fra cio' che si legge ad alta
        # voce e cio' che si riassume.
        md, _ = _conv('<p class="ra">Il corridoio scende, e il silenzio cambia.</p>')
        self.assertTrue(any(l.startswith("> *") for l in md.splitlines()), md)

    def test_un_read_aloud_dentro_un_avviso_resta_una_citazione(self):
        # `⚠ > *…*` non e' un blockquote: e' una riga che comincia per «⚠».
        md, _ = _conv('<div class="warn"><p class="ra">Tre colpi. Non forti.</p></div>')
        self.assertTrue(any(l.startswith("> *") for l in md.splitlines()), md)
        self.assertNotIn("⚠ >", md)

    def test_un_paragrafo_normale_non_diventa_read_aloud(self):
        md, _ = _conv('<p class="ra">Letto.</p><p>Non letto.</p>')
        righe = [l for l in md.splitlines() if l.strip()]
        self.assertEqual(righe, ["> *Letto.*", "Non letto."])

    def test_la_barra_meta_non_si_butta_via(self):
        # Diceva «Sostituisce: Tavola I»: e' il rapporto fra due documenti,
        # non impaginazione.
        md, _ = _conv('<div class="meta"><span><b>Sostituisce:</b> Tavola I</span>'
                      "<span><b>Aggiunge:</b> 17 aree</span></div>")
        self.assertIn("Sostituisce:", md)
        self.assertIn("Aggiunge:", md)
        self.assertNotIn("Tavola I**Aggiunge", md)

    def test_titolo_e_sottotitolo_escono_dal_corpo(self):
        md, _ = _conv('<h1>Il Titolo</h1><p class="sub">Il sottotitolo</p><p>Corpo.</p>')
        self.assertTrue(md.startswith("# Il Titolo\n"))
        self.assertIn("*Il sottotitolo*", md)


class TestArtefatti(unittest.TestCase):
    def test_un_html_generato_dalla_catena_non_e_una_sorgente(self):
        # Lanciato due volte, il convertitore si mangiava il proprio output.
        d = Path(tempfile.mkdtemp())
        gen = d / "g.html"
        gen.write_text('<style>@font-face{}</style><div class="pagefoot">1</div>', encoding="utf-8")
        sorg = d / "s.html"
        sorg.write_text(TESTA + "<p>vero</p>" + CODA, encoding="utf-8")
        self.assertTrue(_generato(gen))
        self.assertFalse(_generato(sorg))


if __name__ == "__main__":
    unittest.main()
