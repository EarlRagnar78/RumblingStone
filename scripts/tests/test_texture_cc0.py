"""Il tema texture (D13-D15 di RESA-ASSET): texture CC0 di Poly Haven nei
terreni, velate del colore della pergamena, in `rendered-texture/`.

Le texture vere non si scaricano in CI: qui sono finte, fatte con Pillow, e
passano dalla stessa strada di chi le ha già scaricate (`--da-cartella`)."""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import build_texture_cc0 as B  # noqa: E402
import render_map_svg as R  # noqa: E402

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None

STANZA = ["🏰🏰🏰🏰🏰🏰", "🏰⬜⬜⬜⬜🏰", "🏰⬜⬜🟦⬜🏰", "🏰🏰🏰🏰🏰🏰"]


def _griglia(tipo="@tipo tattica interni"):
    corpo = ["## MAPPA PROVA", "", "```", "COL →  A B C D E F"]
    corpo += [f"{i:02d}    {r}" for i, r in enumerate(STANZA, 1)]
    corpo += ["", "@north N", tipo, "```", ""]
    return R.extract_maps("\n".join(corpo))[0]


@unittest.skipIf(Image is None, "Pillow assente")
class TestTexture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.vecchi = (B.USCITA, B.INDICE, R.TEXTURE_CC0)
        B.USCITA = self.tmp / "texture-cc0"
        B.INDICE = B.USCITA / "indice.json"
        R.TEXTURE_CC0 = B.USCITA
        sorgenti = self.tmp / "scaricate"
        sorgenti.mkdir()
        for n, tid in enumerate(B._ids()):
            Image.new("RGB", (64, 64), (40 + n * 15, 90, 120)).save(sorgenti / f"{tid}_diff_1k.jpg")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(B.costruisci(sorgenti), 0)

    def tearDown(self):
        B.USCITA, B.INDICE, R.TEXTURE_CC0 = self.vecchi

    def test_le_tessere_combaciano_con_l_indice(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(B.controlla(), 0)
        indice = json.loads(B.INDICE.read_text(encoding="utf-8"))
        self.assertTrue(all(v["licenza"] == "CC0 1.0" for v in indice["texture"].values()))

    def test_una_tessera_toccata_e_bocciata(self):
        (B.USCITA / "stone_tiles_02.webp").write_bytes(b"altro")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(B.controlla(), 1)

    def test_il_tema_texture_mette_le_texture_e_la_velatura(self):
        svg = R.render_svg(_griglia(), "prova.md", "texture")
        self.assertIn("data:image/webp;base64,", svg)
        self.assertIn(f'opacity="{R.VELATURA}"', svg)
        self.assertIn("Texture CC0 1.0 da Poly Haven", svg)

    def test_il_muro_e_muratura_negli_interni_e_roccia_in_caverna(self):
        self.assertIn("castle_brick_07", R.render_svg(_griglia(), "p.md", "texture"))
        caverna = R.render_svg(_griglia("@tipo tattica caverna"), "p.md", "texture")
        self.assertIn("rock_wall_10", caverna)
        self.assertNotIn("castle_brick_07", caverna)

    def test_l_acqua_resta_vettoriale(self):
        svg = R.render_svg(_griglia(), "p.md", "texture")
        self.assertIn(R.PATTERNS["t_deep"], svg)

    def test_la_pergamena_non_cambia(self):
        g = _griglia()
        self.assertNotIn("data:image/webp", R.render_svg(g, "p.md"))
        self.assertEqual(R.render_svg(g, "p.md"), R.render_svg(g, "p.md", "pergamena"))

    def test_il_tema_texture_e_deterministico(self):
        g = _griglia()
        self.assertEqual(R.render_svg(g, "p.md", "texture"), R.render_svg(g, "p.md", "texture"))


@unittest.skipIf(Image is None, "Pillow assente")
class TestValidateMaps(TestTexture):
    """`validate_maps` e il gemello texture (D14)."""

    def _repo(self):
        import validate_maps as V
        # il renderer che validate_maps usa davvero: un altro test può averne
        # ricaricato il modulo, e allora non è lo stesso oggetto di R
        vecchio = V.R.TEXTURE_CC0
        V.R.TEXTURE_CC0 = B.USCITA
        self.addCleanup(setattr, V.R, "TEXTURE_CC0", vecchio)
        radice = self.tmp / "repo"
        (radice / "arco" / "rendered").mkdir(parents=True)
        md = radice / "arco" / "STANZA.md"
        corpo = ["## MAPPA PROVA", "", "```", "COL →  A B C D E F"]
        corpo += [f"{i:02d}    {r}" for i, r in enumerate(STANZA, 1)]
        corpo += ["", "@north N", "@tipo tattica interni", "```", ""]
        md.write_text("\n".join(corpo), encoding="utf-8")
        for n, t in V.render_master(md).items():
            (radice / "arco" / "rendered" / n).write_text(t, encoding="utf-8")
        return V, radice, md

    def test_un_gemello_mancante_e_un_errore(self):
        V, radice, _ = self._repo()
        errori, _ = V.check_tema_texture(radice, [radice / "arco" / "rendered"])
        self.assertTrue(any("mancante" in e for e in errori))

    def test_un_gemello_allineato_passa(self):
        V, radice, md = self._repo()
        tdir = radice / "arco" / "rendered-texture"
        tdir.mkdir()
        for n, t in V.render_master(md, "texture").items():
            (tdir / n).write_text(t, encoding="utf-8")
        errori, totale = V.check_tema_texture(radice, [radice / "arco" / "rendered"])
        self.assertEqual((errori, totale), ([], 1))

    def test_senza_texture_una_cartella_texture_e_un_errore(self):
        V, radice, md = self._repo()
        tdir = radice / "arco" / "rendered-texture"
        tdir.mkdir()
        for n, t in V.render_master(md, "texture").items():
            (tdir / n).write_text(t, encoding="utf-8")
        V.R.TEXTURE_CC0 = self.tmp / "nessuna"
        errori, _ = V.check_tema_texture(radice, [radice / "arco" / "rendered"])
        self.assertTrue(any("senza le texture" in e for e in errori))


class TestSenzaTexture(unittest.TestCase):
    def test_senza_texture_il_check_passa_e_lo_dice(self):
        vecchi = (B.USCITA, B.INDICE)
        B.USCITA = Path(tempfile.mkdtemp()) / "nessuna"
        B.INDICE = B.USCITA / "indice.json"
        try:
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(B.controlla(), 0)
            self.assertIn("non ancora scaricate", out.getvalue())
        finally:
            B.USCITA, B.INDICE = vecchi

    def test_le_tessere_non_sono_ignorate_da_git(self):
        """Il 2026-10-09 un *.webp globale nel .gitignore ha fatto entrare
        l'indice senza le tessere."""
        import subprocess
        r = subprocess.run(["git", "check-ignore", "-q", "scripts/texture-cc0/prova.webp"],
                           cwd=SCRIPTS.parent, capture_output=True)
        self.assertEqual(r.returncode, 1, "scripts/texture-cc0/*.webp è ignorato da git")

    def test_un_indice_senza_tessere_vale_come_niente(self):
        vecchio = R.TEXTURE_CC0
        cartella = Path(tempfile.mkdtemp())
        (cartella / "indice.json").write_text(json.dumps({"terreni": {"⬜": "x"}, "texture": {"x": {}}}),
                                              encoding="utf-8")
        try:
            R.TEXTURE_CC0 = cartella
            self.assertIsNone(R._texture_cc0())
        finally:
            R.TEXTURE_CC0 = vecchio

    def test_un_tema_sconosciuto_e_un_errore(self):
        with self.assertRaises(ValueError):
            R.render_svg(_griglia(), "p.md", "acquerello")

    def test_le_chiavi_sono_terreni_e_non_si_ripetono(self):
        chiavi = [k for k, _ in B.TEXTURE]
        self.assertEqual(len(chiavi), len(set(chiavi)))
        for k in chiavi:
            simbolo = k.split("@")[0]
            self.assertEqual(R.SYMBOLS[simbolo]["mode"], "fill", k)


if __name__ == "__main__":
    unittest.main()


class TestCerca(unittest.TestCase):
    CATALOGO = {
        "roof_slates_02": {"name": "Roof Slates 02", "tags": ["slate"], "categories": ["roofing"],
                           "download_count": 900},
        "red_slate_roof_tiles_01": {"name": "Red Slate Roof Tiles", "tags": ["red"],
                                    "categories": ["roofing", "tiles"], "download_count": 3000},
        "rock_face_03": {"name": "Rock Face 03", "tags": ["cliff"], "categories": ["rock"],
                         "download_count": 5000},
    }

    def test_tutte_le_parole_e_poi_i_download(self):
        import build_texture_cc0 as T
        trovate = T.cerca(self.CATALOGO, ["roof", "slate"])
        self.assertEqual([t[0] for t in trovate], ["red_slate_roof_tiles_01", "roof_slates_02"])

    def test_le_categorie_contano(self):
        import build_texture_cc0 as T
        self.assertEqual([t[0] for t in T.cerca(self.CATALOGO, ["ROCK"])], ["rock_face_03"])


class TestControLeScelte(unittest.TestCase):
    """La scelta del DM sui terreni vincola TEXTURE: --check la fa valere."""

    def _scheda(self, scelte):
        p = Path(tempfile.mkdtemp()) / "scheda.json"
        p.write_text(json.dumps({"preferenze_terreni": scelte}), encoding="utf-8")
        return p

    def test_la_texture_scelta_dev_essere_in_texture(self):
        tex = (("⛰", "rock_face_03"), ("🔳", "plank_flooring"))
        errori = B.contro_le_scelte(tex, self._scheda({"⛰": "texture:lichen_rock",
                                                       "🔳": "texture:plank_flooring"}))
        self.assertEqual(len(errori), 1)
        self.assertIn("⛰: il DM ha scelto lichen_rock", errori[0])

    def test_nessuna_va_bene_toglie_la_texture(self):
        tex = (("⛰", "rock_face_03"),)
        self.assertIn("cerca altre candidate", B.contro_le_scelte(tex, self._scheda({"⛰": "nessuna"}))[0])
        self.assertEqual(B.contro_le_scelte((), self._scheda({"⛰": "nessuna", "🔳": "senza"})), [])

    def test_non_vedo_differenze_non_obbliga(self):
        self.assertEqual(B.contro_le_scelte((("⛰", "x"),), self._scheda({"⛰": "uguali"})), [])
