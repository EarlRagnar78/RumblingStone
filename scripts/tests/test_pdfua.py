"""PDF/UA-1 (ISO 14289-1) nell'edizione da stampa (ADR-0129).

Typst verifica da sé, alla compilazione, gli obblighi di PDF/UA-1 che dipendono
dal documento: il primo titolo è di livello 1, nessun titolo salta un livello,
ogni immagine ha un testo alternativo o è un artefatto, lingua e titolo del
documento ci sono. Se uno manca rifiuta di compilare. Questi test sono il
cancello: il tema e il convertitore devono restare in grado di produrre
PDF/UA-1, e un booklet vero (il più piccolo con schede e immagini) lo è.
La conformità piena la misura veraPDF fuori dalla CI
(`plans/esperimenti/pdfua-2026-11-13/`).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import export_booklet_typst as ex  # noqa: E402
import typst_motore as tm  # noqa: E402

TESTA = ('#import "/scripts/typst/tema-rumblingstone.typ": *\n'
         '#show: libro.with(titolo: "Prova", sottotitolo: "", brand: "", banner: "", meta: "",\n'
         '  capitolo: "Prova", apparato: false)\n')


def _compila(corpo: str, pdfua: bool = True, solo_repo: bool = False,
             file: dict[str, str] | None = None, pdfa: str = "") -> tuple[tm.Esito, bytes]:
    with tempfile.TemporaryDirectory(dir=REPO) as d:
        for nome, testo in (file or {}).items():
            (Path(d) / nome).write_text(testo, encoding="utf-8")
        typ, pdf = Path(d) / "p.typ", Path(d) / "p.pdf"
        typ.write_text(TESTA + corpo, encoding="utf-8")
        e = tm.compila(typ, pdf, root=REPO, font=ex.FONTS, pacchetti=ex.PACCHETTI,
                       solo_font_del_repo=solo_repo, pdfua=pdfua, pdfa=pdfa)
        return e, (pdf.read_bytes() if pdf.exists() else b"")


class TestTitoliSenzaSalti(unittest.TestCase):
    def test_un_salto_sale_di_livello_e_ricorda_il_disegno(self):
        src, n = ex.titoli_senza_salti('#capitolo-aperto("I", none)\n=== Chi si incontra\n== Dopo\n')
        self.assertEqual(n, 1)
        self.assertIn("#heading(depth: 2)[Chi si incontra] <come-3>", src)
        self.assertIn("\n== Dopo", src)

    def test_sotto_la_profondita_dell_indice_resta_fuori(self):
        src, n = ex.titoli_senza_salti("= A\n== B\n==== C\n")
        self.assertEqual(n, 1)
        self.assertIn("#heading(depth: 3, outlined: false, bookmarked: true)[C] <come-4>", src)

    def test_una_scheda_apre_al_livello_1(self):
        src, n = ex.titoli_senza_salti("== A\n#scheda(\n  nome: [X],\n)\n=== B\n")
        self.assertEqual(n, 1)

    def test_senza_salti_non_cambia_nulla(self):
        testo = "= A\n== B\n=== C\n== D\n= E\n"
        self.assertEqual(ex.titoli_senza_salti(testo), (testo, 0))

    def test_un_titolo_con_etichetta_non_si_tocca(self):
        testo = "= A\n=== B <x>\n"
        self.assertEqual(ex.titoli_senza_salti(testo), (testo, 0))


class TestTitoliAnnidati(unittest.TestCase):
    """ADR-0145: i segnalibri seguono la gerarchia, capitolo → sezioni →
    sottosezioni, come nei PDF di Paizo e di Wizards; prima erano piatti."""

    def test_dopo_il_primo_capitolo_i_titoli_scendono_di_un_livello(self):
        src = ex.titoli_annidati('#capitolo-aperto("I", none)\n= A\n#capitolo-aperto("II", none)\n= B\n')
        self.assertEqual(src.count("#set heading(offset: 1)"), 1)
        self.assertLess(src.index('#capitolo-aperto("I"'), src.index("#set heading(offset: 1)"))
        self.assertLess(src.index("#set heading(offset: 1)"), src.index("= A"))

    def test_senza_capitoli_non_cambia_nulla(self):
        testo = "= A\n== B\n"
        self.assertEqual(ex.titoli_annidati(testo), testo)

    def test_dentro_il_capitolo_annidato_il_primo_titolo_e_di_profondita_1(self):
        """Con `offset: 1` il capitolo è il livello 1 e un `==` subito sotto
        sarebbe il 3: PDF/UA-1 lo rifiuta. Sale a profondità 1 e si disegna
        come prima."""
        src, n = ex.titoli_senza_salti(ex.titoli_annidati('#capitolo-aperto("I", none)\n== A\n=== B\n'))
        self.assertEqual(n, 2)
        self.assertIn("#heading(depth: 1)[A] <come-2>", src)
        self.assertIn("#heading(depth: 2)[B] <come-3>", src)

    def test_le_sezioni_sorelle_restano_sorelle(self):
        src, n = ex.titoli_senza_salti(ex.titoli_annidati(
            '#capitolo-aperto("I", none)\n== A\n=== a\n== B\n#capitolo-aperto("II", none)\n= C\n'))
        self.assertIn("#heading(depth: 1)[A] <come-2>", src)
        self.assertIn("#heading(depth: 2)[a] <come-3>", src)
        self.assertIn("#heading(depth: 1)[B] <come-2>", src)
        self.assertIn("\n= C", src)
        self.assertEqual(n, 3)

    def test_il_numero_del_titolo_resta(self):
        src, _ = ex.titoli_senza_salti(ex.titoli_annidati(
            '#capitolo-aperto("I", none)\n== 7. In numeri\n== - trattino\n'))
        self.assertIn("#heading(depth: 1)[7\\. In numeri] <come-2>", src)
        self.assertIn("#heading(depth: 1)[\\- trattino] <come-2>", src)

    def test_due_volte_e_come_una(self):
        una = ex.titoli_annidati('#capitolo-aperto("I", none)\n= A\n')
        self.assertEqual(ex.titoli_annidati(una), una)


@unittest.skipUnless(tm.disponibile(), "typst assente")
class TestIlTemaProducePdfUa(unittest.TestCase):
    def test_segnalibri_annidati(self):
        import pymupdf
        corpo = ex.titoli_annidati('#capitolo-aperto("I · Apertura", none)\n= Sezione\nTesto.\n'
                                   '== Sotto\nAltro.\n#capitolo-aperto("II · Poi", none)\n= Altra\nFine.\n')
        e, pdf = _compila(corpo)
        self.assertTrue(e.ok, e.errore)
        self.assertTrue(e.pdfua, e.motivo_pdfua)
        toc = [(l, t) for l, t, _ in pymupdf.open(stream=pdf, filetype="pdf").get_toc()]
        self.assertEqual(toc, [(1, "I · Apertura"), (2, "Sezione"), (3, "Sotto"),
                               (1, "II · Poi"), (2, "Altra")])

    def test_il_numero_nel_segnalibro_resta(self):
        import pymupdf
        corpo, _ = ex.titoli_senza_salti(ex.titoli_annidati(
            '#capitolo-aperto("I", none)\n== 7. In numeri\nTesto.\n'))
        e, pdf = _compila(corpo)
        self.assertTrue(e.ok and e.pdfua, e.errore or e.motivo_pdfua)
        toc = [(l, t) for l, t, _ in pymupdf.open(stream=pdf, filetype="pdf").get_toc()]
        self.assertEqual(toc, [(1, "I"), (2, "7. In numeri")])

    def test_capitolo_con_titolo_muto_e_salto_riparato(self):
        corpo = ('#capitolo-aperto("I · Apertura", none)\n'
                 '#heading(depth: 2)[Chi si incontra] <come-3>\n'
                 'Testo.\n== Sezione\nAltro testo.\n')
        e, _ = _compila(corpo)
        self.assertTrue(e.ok, e.errore)
        self.assertTrue(e.pdfua, e.motivo_pdfua)

    def test_hide_del_titolo_era_il_difetto(self):
        """Il modo di prima: typst lo rifiuta, e l'esito lo dice invece di fallire."""
        e, _ = _compila("#hide(heading(level: 1)[Nascosto])\n== Dopo\nTesto.\n")
        self.assertTrue(e.ok, e.errore)
        self.assertFalse(e.pdfua)
        self.assertIn("first heading", e.motivo_pdfua)

    def test_senza_pdfua_si_compila_come_prima(self):
        e, _ = _compila("= Uno\nTesto.\n", pdfua=False)
        self.assertTrue(e.ok and not e.pdfua and not e.motivo_pdfua)


SVG_LEGENDA = ('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="40">'
               '<text x="5" y="25" font-family="Georgia,serif" font-size="14">'
               '⏳ Forgia ▸ DC 24 🔮</text></svg>')


@unittest.skipUnless(tm.disponibile(), "typst assente")
class TestEmojiDaiFontDelRepo(unittest.TestCase):
    """ADR-0130: emoji e simboli escono dai font del repo, anche dentro le SVG."""

    def test_emoji_e_simboli_coi_soli_font_del_repo(self):
        corpo = ("= Prova\n⚔️ 🛡️ 🔮 ⏳ ⬦ ► ▸ ☐ ① ★ ⟺ ⟶ testo.\n"
                 '#image("mappa.svg", alt: "Legenda")\n')
        e, pdf = _compila(corpo, solo_repo=True, file={"mappa.svg": SVG_LEGENDA})
        self.assertTrue(e.ok, e.errore)
        self.assertTrue(e.pdfua, e.motivo_pdfua)
        self.assertIn(b"NotoColorEmoji", pdf)
        for di_sistema in (b"Unifont", b"FreeSans", b"Inter-", b"Liberation"):
            self.assertNotIn(di_sistema, pdf)

    def test_l_esportatore_usa_i_soli_font_del_repo(self):
        sorgente = (REPO / "scripts/export_booklet_typst.py").read_text(encoding="utf-8")
        self.assertIn("solo_font_del_repo=True", sorgente)
        self.assertTrue((REPO / "scripts/fonts/NotoColorEmoji.ttf").exists())


@unittest.skipUnless(tm.disponibile(), "typst assente")
class TestPdfA(unittest.TestCase):
    """ADR-0131: PDF/A-2a insieme a PDF/UA-1, col ripiego dichiarato."""

    def test_capitolo_esce_pdf_a_2a_e_ua_1(self):
        corpo = "= Prova\nTesto ⚔️ ⬦.\n" '#image("mappa.svg", alt: "Legenda")\n'
        e, pdf = _compila(corpo, solo_repo=True, pdfa=ex.PDFA, file={"mappa.svg": SVG_LEGENDA})
        self.assertTrue(e.ok, e.errore)
        self.assertEqual((e.pdfua, e.pdfa, e.motivo_pdfa), (True, "a-2a", ""))
        self.assertIn(b"pdfaid:part", pdf)

    def test_senza_pdfa_il_pdf_non_lo_dichiara(self):
        e, pdf = _compila("= Prova\nTesto.\n", solo_repo=True)
        self.assertTrue(e.ok and e.pdfua and not e.pdfa)
        self.assertNotIn(b"pdfaid:part", pdf)

    def test_un_rifiuto_del_pdfa_ricade_sul_solo_ua_e_lo_dice(self):
        chiamate = []

        def finto(typ, pdf, *, standard=None, **kw):
            chiamate.append(standard)
            if standard and len(standard) == 2:
                return tm.Esito(False, "PDF/A-2a error: prova\naltro", False)
            return tm.Esito(True, "", False)

        vero = tm._compila
        tm._compila = finto
        try:
            e = tm.compila(Path("a.typ"), Path("a.pdf"), root=REPO, font=ex.FONTS,
                           pacchetti=ex.PACCHETTI, pdfua=True, pdfa="a-2a")
        finally:
            tm._compila = vero
        self.assertEqual(chiamate, [["ua-1", "a-2a"], ["ua-1"]])
        self.assertTrue(e.ok and e.pdfua)
        self.assertEqual((e.pdfa, e.motivo_pdfa), ("", "PDF/A-2a error: prova"))

    def test_l_esportatore_chiede_pdf_a_2a(self):
        self.assertEqual(ex.PDFA, "a-2a")


@unittest.skipUnless(tm.disponibile(), "typst assente")
class TestUnBookletVero(unittest.TestCase):
    """Il fascicolo delle schede del Drappo: schede PG con ritratto, titoli muti."""

    MANIFEST = REPO / "10-stand-alone/Il-Drappo-di-Tarsilia/homebrew/DRAPPO-SCHEDE-PG.manifest.json"

    def test_esce_pdf_ua_1(self):
        pdf = self.MANIFEST.parent / "DRAPPO-SCHEDE-PG-STAMPA.pdf"
        c_era = pdf.exists()
        r = subprocess.run([sys.executable, str(REPO / "scripts/export_booklet_typst.py"),
                            str(self.MANIFEST), "--all"], capture_output=True, text=True, cwd=REPO)
        try:
            self.assertEqual(r.returncode, 0, r.stderr[-2000:])
            self.assertIn("PDF/UA-1", r.stdout)
            self.assertIn("PDF/A-2a", r.stdout)
            self.assertNotIn("non è PDF/UA-1", r.stderr)
        finally:
            if not c_era:
                pdf.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
