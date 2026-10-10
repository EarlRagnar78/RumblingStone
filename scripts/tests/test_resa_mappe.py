"""La resa uniforme delle mappe (ADR-0085): font incorporati, ripiego Noto per
le emoji locali, titoli che stanno nel foglio, prop senza doppioni.

Il caso che ha fatto nascere il primo test: il 2026-10-08 un prop nuovo e' stato
aggiunto con la chiave `pr_crystal`, che esisteva gia' (il glifo di 🔮). Un
dizionario Python con due chiavi uguali tiene l'ultima senza dire niente, e il
cristallo magico di tutte le mappe e' cambiato faccia. L'ha visto solo il PNG.
"""

import ast
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import render_map_svg as R  # noqa: E402
from dmcore import legenda  # noqa: E402


def _griglia(righe, legenda_locale=""):
    corpo = ["## MAPPA PROVA", "", "```",
             "COL →  " + " ".join(chr(65 + i) for i in range(len(righe[0])))]
    corpo += [f"{i:02d}    {r}" for i, r in enumerate(righe, 1)]
    if legenda_locale:
        corpo.append("LEGENDA · " + legenda_locale)
    corpo += ["```", ""]
    return R.extract_maps("\n".join(corpo))[0]


class TestProp(unittest.TestCase):
    def test_nessuna_chiave_doppia_nei_dizionari_del_renderer(self):
        albero = ast.parse((SCRIPTS / "render_map_svg.py").read_text(encoding="utf-8"))
        for nodo in ast.walk(albero):
            if isinstance(nodo, ast.Dict):
                chiavi = [k.value for k in nodo.keys if isinstance(k, ast.Constant)]
                doppie = {k for k in chiavi if chiavi.count(k) > 1}
                self.assertFalse(doppie, f"chiavi ripetute: {doppie}")

    def test_ogni_prop_della_legenda_esiste(self):
        for sim, spec in legenda.simboli().items():
            if spec.get("prop"):
                self.assertIn(spec["prop"], R.PROPS, f"{sim}: manca il prop {spec['prop']}")

    def test_i_due_universali_nuovi_hanno_glifi_diversi_dai_vicini(self):
        """Il cristallo gigante non e' il cristallo magico, e la stalagmite non e' la roccia."""
        sim = legenda.simboli()
        self.assertNotEqual(sim["🔷"]["prop"], sim["🔮"]["prop"])
        self.assertNotEqual(sim["🔺"]["prop"], sim["🪨"]["prop"])


class TestFont(unittest.TestCase):
    def test_i_font_viaggiano_dentro_l_svg(self):
        svg = R.render_svg(_griglia(["🏰🏰🏰🏰🏰", "🏰⬜⬜⬜🏰", "🏰🏰🏰🏰🏰"]), "prova.md")
        self.assertIn("font-family:'EB Garamond'", svg)
        self.assertIn("font-family:'Cinzel'", svg)
        self.assertEqual(svg.count("@font-face"), 2)

    def test_il_grassetto_va_in_cinzel(self):
        svg = R.render_svg(_griglia(["🏰🏰🏰🏰🏰", "🏰⬜⬜⬜🏰", "🏰🏰🏰🏰🏰"]), "prova.md")
        self.assertIn('text[font-weight="bold"]{font-family:Cinzel', svg)

    def test_un_titolo_corto_resta_a_19(self):
        self.assertEqual(R._corpo_titolo("Cella", 400), (19.0, False))

    def test_un_titolo_lungo_si_stringe(self):
        corpo, comprimi = R._corpo_titolo("Stanza della Corona — 15 m × 19,5 m", 300)
        self.assertLess(corpo, 19)
        self.assertFalse(comprimi)

    def test_un_titolo_lunghissimo_si_comprime_e_non_scende_sotto_11(self):
        corpo, comprimi = R._corpo_titolo("Una stanza " * 20, 300)
        self.assertEqual((corpo, comprimi), (11.0, True))

    def test_il_titolo_compresso_ha_textlength(self):
        g = _griglia(["🏰🏰🏰🏰🏰", "🏰⬜⬜⬜🏰", "🏰🏰🏰🏰🏰"])
        g["title"] = "Un titolo lunghissimo che non sta in nessun foglio stretto " * 3
        self.assertIn('lengthAdjust="spacingAndGlyphs"', R.render_svg(g, "prova.md"))


class TestRipiegoNoto(unittest.TestCase):
    def test_un_emoji_locale_si_disegna_con_noto(self):
        svg = R.render_svg(_griglia(["🏰🏰🏰🏰🏰", "🏰⬜💠⬜🏰", "🏰🏰🏰🏰🏰"], "💠 cristallo vivente"),
                           "prova.md")
        self.assertIn('<symbol id="nt_1f4a0"', svg)
        self.assertIn('href="#nt_1f4a0"', svg)
        self.assertNotIn('font-size="17"', svg)

    def test_senza_il_file_resta_il_testo(self):
        svg = R.render_svg(_griglia(["🏰🏰🏰🏰🏰", "🏰⬜🧿⬜🏰", "🏰🏰🏰🏰🏰"], "🧿 occhio"), "prova.md")
        self.assertIn('font-size="17"', svg)

    def test_due_emoji_locali_non_si_pestano_gli_id(self):
        svg = R.render_svg(_griglia(["🏰🏰🏰🏰🏰", "🏰💠⬜📜🏰", "🏰🏰🏰🏰🏰"], "💠 cristallo · 📜 pergamena"),
                           "prova.md")
        ids = re.findall(r'\bid="([^"]+)"', svg)
        self.assertEqual(len(ids), len(set(ids)))

    def test_ogni_emoji_locale_del_corpus_ha_il_suo_file(self):
        r = subprocess.run([sys.executable, str(SCRIPTS / "build_emoji_noto.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_la_licenza_sta_accanto_ai_file(self):
        cartella = SCRIPTS / "emoji-noto"
        self.assertIn("Apache License", (cartella / "LICENSE").read_text(encoding="utf-8"))
        self.assertIn("Noto Emoji", (cartella / "CREDITS.md").read_text(encoding="utf-8"))


class TestSottoinsiemi(unittest.TestCase):
    def test_i_sottoinsiemi_combaciano_con_copertura(self):
        r = subprocess.run([sys.executable, str(SCRIPTS / "build_font_mappe.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_senza_sottoinsiemi_il_renderer_non_si_rompe(self):
        vecchio = R.FONT_MAPPE
        try:
            R.FONT_MAPPE = Path(tempfile.mkdtemp())
            self.assertEqual(R._stile_font(), "")
            self.assertEqual(R._corpo_titolo("x" * 200, 100), (19.0, False))
        finally:
            R.FONT_MAPPE = vecchio


class TestTipo(unittest.TestCase):
    """`@tipo <tipo> <ambiente>` (D18): la categoria decide i controlli e il corredo."""

    STANZA = ["🏰🏰🏰🚪🏰🏰", "🏰⬜⬜⬜⬜🏰", "🏰⬜🔵⬜⬜🏰", "🏰⬜⬜🔴⬜🏰", "🏰🏰🏰🏰🏰🏰"]

    def setUp(self):
        sys.path.insert(0, str(SCRIPTS / "tests"))
        from test_collaudo_mappe import _codici, _master
        self._codici, self._master = _codici, _master
        self.tmp = Path(tempfile.mkdtemp())

    def test_senza_tipo_un_avviso(self):
        p = self._master(self.tmp, "a.md", self.STANZA, ["@north N"])
        self.assertIn("tipo/mancante", self._codici(p))

    def test_tipo_e_ambiente_letti(self):
        import collaudo_mappe as C
        p = self._master(self.tmp, "b.md", self.STANZA, ["@north N", "@tipo tattica interni"])
        g = R.extract_maps(p.read_text(encoding="utf-8"))[0]
        dato = C.Collaudo(p, 1, g, {}).esegui().come_dato()
        self.assertEqual((dato["tipo"], dato["ambiente"]), ("tattica", "interni"))
        self.assertNotIn("tipo/mancante", self._codici(p))

    def test_un_tipo_sbagliato_e_un_errore_e_non_spegne_i_controlli(self):
        p = self._master(self.tmp, "c.md", self.STANZA, ["@tipo tatica interni"])
        codici = self._codici(p)
        self.assertIn("tipo/illeggibile", codici)
        self.assertIn("nord/mancante", codici)

    def test_un_ambiente_sbagliato_e_un_errore(self):
        p = self._master(self.tmp, "d.md", self.STANZA, ["@north N", "@tipo tattica palude"])
        self.assertIn("tipo/illeggibile", self._codici(p))

    def test_il_compilatore_scrive_la_direttiva(self):
        import compile_map_json as J
        spec = {"title": "Prova del tipo", "map_size": [6, 5], "tipo": "tattica", "ambiente": "caverna"}
        self.assertIn("@tipo tattica caverna", J._annotation_lines(spec))

    def test_il_compilatore_rifiuta_un_ambiente_fuori_elenco(self):
        import compile_map_json as J
        with self.assertRaises(J.SpecError):
            J.validate({"title": "Prova del tipo", "map_size": [6, 5], "tipo": "tattica", "ambiente": "palude"})

    def test_ogni_mappa_del_corpus_ha_la_sua_categoria(self):
        import collaudo_mappe as C
        senza = []
        for f in C.bersagli([]):
            for i, g in enumerate(R.extract_maps(f.read_text(encoding="utf-8")), 1):
                if not C.direttive(g["annotations"])["tipo"]:
                    senza.append(f"{f.relative_to(C.REPO)} #{i}")
        self.assertEqual(senza, [], "mappe senza @tipo: classificale (D18)")


if __name__ == "__main__":
    unittest.main()
