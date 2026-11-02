"""Il tema pianta (ADR-0102): le mappe tattiche nello stile delle piante delle
città, in `rendered-pianta/`, adottato una cartella alla volta; e il comando
che rigenera le piante di Rethmar, Dauth e Channathgate."""

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock
from xml.dom import minidom

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import genera_pianta_citta as G  # noqa: E402
import render_map_pianta as P  # noqa: E402
import render_map_svg as R  # noqa: E402

CAVERNA = ["⛰⛰⛰⛰⛰⛰", "⛰🟤🟤🟤🟤⛰", "⛰🟤🔥🟤🟤⛰", "⛰⛰⛰⛰⛰⛰"]
STANZA = ["🏰🏰🏰🏰🏰🏰", "🏰⬜⬜⬜⬜🏰", "🏰⬜⬜🟦⬜🏰", "🏰🏰🏰🏰🏰🏰"]


def _testo(righe, tipo):
    corpo = ["## MAPPA PROVA", "", "```", "COL →  A B C D E F"]
    corpo += [f"{i:02d}    {r}" for i, r in enumerate(righe, 1)]
    corpo += ["", "@north N", tipo, "@mark 1 ; B2 ; Il punto", "```", ""]
    return "\n".join(corpo)


def _griglia(righe=STANZA, tipo="@tipo tattica interni"):
    return R.extract_maps(_testo(righe, tipo))[0]


class TestRender(unittest.TestCase):
    def test_e_un_svg_ben_formato_e_deterministico(self):
        g = _griglia(CAVERNA, "@tipo tattica caverna")
        svg = R.render_svg(g, "p.md", "pianta")
        minidom.parseString(svg)
        self.assertEqual(svg, R.render_svg(g, "p.md", "pianta"))

    def test_ha_la_roccia_tratteggiata_e_i_luoghi(self):
        svg = R.render_svg(_griglia(CAVERNA, "@tipo tattica caverna"), "p.md", "pianta")
        self.assertIn('id="pt-roccia"', svg)
        self.assertIn("Luoghi", svg)
        self.assertIn("Il punto", svg)

    def test_il_lastricato_ha_la_sua_trama(self):
        svg = R.render_svg(_griglia(), "p.md", "pianta")
        self.assertIn('id="pt-pav"', svg)

    def test_non_e_la_pergamena(self):
        g = _griglia()
        self.assertNotEqual(R.render_svg(g, "p.md", "pianta"), R.render_svg(g, "p.md"))

    def test_un_oggetto_accanto_al_muro_sta_sul_pavimento(self):
        # _resolve_bases dà alla statua il terreno a sinistra, cioè il muro:
        # nella pianta la roccia non deve allargarsi sotto la statua
        import re
        con = ["🏰🏰🏰🏰🏰🏰", "🏰🗿⬜⬜⬜🏰", "🏰⬜⬜⬜⬜🏰", "🏰🏰🏰🏰🏰🏰"]
        senza = ["🏰🏰🏰🏰🏰🏰", "🏰⬜⬜⬜⬜🏰", "🏰⬜⬜⬜⬜🏰", "🏰🏰🏰🏰🏰🏰"]

        def roccia(righe):
            svg = R.render_svg(_griglia(righe), "p.md", "pianta")
            return re.search(r'<clipPath id="pt-roccia"><path d="([^"]+)"', svg).group(1)
        self.assertEqual(roccia(con), roccia(senza))


class TestVociDiLegenda(unittest.TestCase):
    def test_una_voce_corta_resta_com_e(self):
        self.assertEqual(P._corto("statua", 20), "statua")

    def test_prima_cade_la_parentesi(self):
        self.assertEqual(P._corto("statua dei re (copertura totale)", 20), "statua dei re")

    def test_mai_a_meta_parola(self):
        v = P._corto("bracieri su treppiede accesi tutta la notte", 20)
        self.assertTrue(v.endswith("…"))
        self.assertLessEqual(len(v), 20)
        self.assertTrue("bracieri su treppiede accesi tutta la notte".startswith(v[:-1]))
        self.assertEqual(v[:-1], v[:-1].rstrip())


class TestValidateMaps(unittest.TestCase):
    """Il gemello pianta si pretende solo dove la cartella c'è."""

    def _repo(self):
        import validate_maps as V
        radice = Path(tempfile.mkdtemp()) / "repo"
        (radice / "arco" / "rendered").mkdir(parents=True)
        md = radice / "arco" / "STANZA.md"
        md.write_text(_testo(STANZA, "@tipo tattica interni"), encoding="utf-8")
        for n, t in V.render_master(md).items():
            (radice / "arco" / "rendered" / n).write_text(t, encoding="utf-8")
        return V, radice, md

    def test_senza_cartella_nessuno_lo_pretende(self):
        V, radice, _ = self._repo()
        self.assertEqual(V.check_tema_pianta([radice / "arco" / "rendered"]), ([], 0))

    def test_una_cartella_vuota_vuole_tutte_le_mappe(self):
        V, radice, _ = self._repo()
        (radice / "arco" / "rendered-pianta").mkdir()
        errori, _ = V.check_tema_pianta([radice / "arco" / "rendered"])
        self.assertTrue(any("mancante" in e for e in errori))

    def test_un_gemello_allineato_passa_e_uno_toccato_no(self):
        V, radice, md = self._repo()
        tdir = radice / "arco" / "rendered-pianta"
        tdir.mkdir()
        for n, t in V.render_master(md, "pianta").items():
            (tdir / n).write_text(t, encoding="utf-8")
        self.assertEqual(V.check_tema_pianta([radice / "arco" / "rendered"]), ([], 1))
        svg = next(tdir.glob("*.svg"))
        svg.write_text(svg.read_text(encoding="utf-8").replace("Luoghi", "Posti"), encoding="utf-8")
        errori, _ = V.check_tema_pianta([radice / "arco" / "rendered"])
        self.assertTrue(any("NON allineato" in e for e in errori))


class TestPianteCitta(unittest.TestCase):
    def test_ogni_citta_ha_il_suo_programma(self):
        for programma, _ in G.CITTA.values():
            self.assertTrue((G.PIANTE / programma).is_file(), programma)

    def test_senza_le_librerie_esce_con_2_e_dice_cosa_installare(self):
        err = io.StringIO()
        with mock.patch.object(G, "mancanti", return_value=["shapely"]), redirect_stderr(err):
            self.assertEqual(G.main(["--tutte", "--check"]), 2)
        self.assertIn("requirements-dev.txt", err.getvalue())


if __name__ == "__main__":
    unittest.main()
