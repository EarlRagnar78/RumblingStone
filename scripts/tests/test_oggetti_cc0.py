"""Gli oggetti di scena del tema texture (R4-ter, D17 di RESA-ASSET): tessere
webp rese dall'alto da modelli 3D CC0, al posto dei glifi, solo nel tema texture.

I modelli veri non si scaricano in CI e Blender non c'è: la cache è finta (un
glTF qualunque con la sua `fonte.json`) e Blender è uno script che disegna un
PNG con Pillow. Passano dalla stessa strada di chi ha scaricato e reso davvero."""

import io
import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import build_oggetti_cc0 as B  # noqa: E402
import render_map_svg as R  # noqa: E402

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None

BLENDER_FINTO = '''
import json, sys
from pathlib import Path
from PIL import Image
lavoro = json.loads(Path(sys.argv[1]).read_text())
esiti = {}
for n, v in enumerate(lavoro["modelli"]):
    lato = lavoro["lock"]["lato_render"]
    im = Image.new("RGBA", (lato, lato), (0, 0, 0, 0))
    im.paste((90 + n * 20, 70, 50, 255), (lato // 4, lato // 4, 3 * lato // 4, 3 * lato // 4))
    im.save(v["uscita"])
    esiti[v["tessera"]] = {"scala": 1.0, "girato": False, "impronta_m": [0.76, 0.76],
                           "lato_originale_m": 1.0}
Path(lavoro["esiti"]).write_text(json.dumps(esiti))
print("Blender finto")
'''

STANZA = ["🏰🏰🏰🏰🏰🏰🏰", "🏰⬜🪨🗿⬜🧱🏰", "🏰🚪🏮🔥🛏🧱🏰", "🏰🧱🧱⬜⬜⬜🏰",
          "🏰🏰🏰🏰🏰🏰🏰"]


def _griglia():
    corpo = ["## MAPPA PROVA", "", "```", "COL →  A B C D E F G"]
    corpo += [f"{i:02d}    {r}" for i, r in enumerate(STANZA, 1)]
    corpo += ["", "@north N", "@tipo tattica interni", "```", ""]
    return R.extract_maps("\n".join(corpo))[0]


def _cache_finta(cache: Path, pid: str) -> None:
    d = cache / "polyhaven" / pid
    d.mkdir(parents=True)
    (d / f"{pid}_1k.gltf").write_text('{"asset": {"version": "2.0"}}')
    file = {f"{pid}_1k.gltf": {"url": "finto",
                               "md5": hashlib.md5((d / f"{pid}_1k.gltf").read_bytes()).hexdigest()}}
    (d / "fonte.json").write_text(json.dumps({
        "fonte": "Poly Haven", "id": pid, "pagina": "finta", "licenza": "CC0 1.0",
        "modello": f"{pid}_1k.gltf", "file": file}))


@unittest.skipIf(Image is None, "Pillow assente")
class TestOggetti(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.vecchi = (B.CACHE, B.USCITA, B.INDICE, R.OGGETTI_CC0)
        B.CACHE = self.tmp / "cache"
        B.USCITA = self.tmp / "oggetti-cc0"
        B.INDICE = B.USCITA / "indice.json"
        R.OGGETTI_CC0 = B.USCITA
        for pid in B.PILOTA:
            _cache_finta(B.CACHE, pid)
        finto = self.tmp / "blender_finto.py"
        finto.write_text(BLENDER_FINTO, encoding="utf-8")
        self.vecchio_comando = B.comando_blender
        B.comando_blender = lambda _esplicito: [sys.executable, str(finto)]
        with redirect_stdout(io.StringIO()):
            self.assertEqual(B.main(["--rendi", "--prova"]), 0)
        # D23: la misura non le boccia e il DM le ha preferite al glifo
        self.vecchia_scheda = B.SCHEDA_RESA
        B.SCHEDA_RESA = self.tmp / "scheda-resa.json"
        simboli = self._indice()["simboli"]
        self._scrivi_scheda({s: {"interni": "vince"} for s in simboli},
                            {s: {"interni": "tessera"} for s in simboli})

    def _scrivi_scheda(self, candidati, preferenze):
        B.SCHEDA_RESA.write_text(json.dumps({"candidati": candidati, "preferenze_dm": preferenze}),
                                 encoding="utf-8")

    def tearDown(self):
        B.CACHE, B.USCITA, B.INDICE, R.OGGETTI_CC0 = self.vecchi
        B.comando_blender = self.vecchio_comando
        B.SCHEDA_RESA = self.vecchia_scheda

    def test_senza_il_confronto_del_dm_e_bocciata(self):
        simboli = self._indice()["simboli"]
        self._scrivi_scheda({s: {"interni": "vince"} for s in simboli}, {})
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(B.controlla(), 1)
        self.assertIn("non l'ha ancora confrontata", out.getvalue())

    def test_se_il_dm_preferisce_il_glifo_e_bocciata(self):
        simboli = self._indice()["simboli"]
        pref = {s: {"interni": "tessera"} for s in simboli}
        pref["🛏"] = {"interni": "glifo"}
        self._scrivi_scheda({s: {"interni": "vince"} for s in simboli}, pref)
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(B.controlla(), 1)
        self.assertIn("🛏: il DM ha preferito il glifo", out.getvalue())

    def test_se_la_misura_la_boccia_e_bocciata(self):
        simboli = self._indice()["simboli"]
        cand = {s: {"interni": "vince"} for s in simboli}
        cand["🪨"] = {"interni": "perde", "esterno": "vince"}
        self._scrivi_scheda(cand, {s: {"interni": "tessera"} for s in simboli})
        with redirect_stdout(io.StringIO()):
            self.assertEqual(B.controlla(), 1)

    def test_adotta_toglie_le_tessere_che_il_dm_non_ha_preferito(self):
        simboli = self._indice()["simboli"]
        pref = {s: {"interni": "tessera"} for s in simboli}
        pref["🧱"] = {"interni": "glifo"}
        self._scrivi_scheda({s: {"interni": "vince"} for s in simboli}, pref)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(B.main(["--adotta"]), 0)
            self.assertEqual(B.controlla(), 0)
        indice = self._indice()
        self.assertNotIn("🧱", indice["simboli"])
        self.assertNotIn("namaqualand_rocks_01-ns", indice["tessere"])
        self.assertEqual(indice["orientabili"], [])
        self.assertFalse((B.USCITA / "namaqualand_rocks_01.webp").exists())
        self.assertIn("🛏", indice["simboli"])

    def test_adotta_copia_le_candidate_approvate_al_posto_delle_vecchie(self):
        cand = self.tmp / "cand"
        cand.mkdir()
        (cand / "zenitale-letto-a.webp").write_bytes(b"letto generato")
        (cand / "zenitale-botte-a.webp").write_bytes(b"botte generata")
        voce = {"fonte": "ComfyUI", "licenza": B.LICENZA_GENERATA, "provenienza": "sdxl seme 1"}
        (cand / "indice.json").write_text(json.dumps({
            "simboli": {"🛏": ["zenitale-letto-a"], "🛢": ["zenitale-botte-a"]},
            "tessere": {"zenitale-letto-a": voce, "zenitale-botte-a": voce}}), encoding="utf-8")
        simboli = self._indice()["simboli"]
        pref = {s: {"interni": "tessera"} for s in simboli}
        pref["🛢"] = {"interni": "glifo"}
        self._scrivi_scheda({s: {"interni": "vince"} for s in simboli}, pref)
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(B.main(["--adotta", str(cand)]), 0)
        indice = self._indice()
        self.assertEqual(indice["simboli"]["🛏"], ["zenitale-letto-a"])
        self.assertNotIn("GothicBed_01", indice["tessere"])
        self.assertEqual((B.USCITA / "zenitale-letto-a.webp").read_bytes(), b"letto generato")
        self.assertNotIn("zenitale-botte-a", indice["tessere"])
        self.assertIn('("🛏", "zenitale-letto-a"),', out.getvalue())

    def test_nessuna_va_bene_butta_la_tessera_e_la_dice_da_rifare(self):
        simboli = self._indice()["simboli"]
        pref = {s: {"interni": "tessera"} for s in simboli}
        pref["🛏"] = {"interni": "nessuna"}
        self._scrivi_scheda({s: {"interni": "vince"} for s in simboli}, pref)
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(B.main(["--adotta"]), 0)
        self.assertNotIn("🛏", self._indice()["simboli"])
        self.assertFalse((B.USCITA / "GothicBed_01.webp").exists())
        self.assertIn("Da rifare, perché nessuna andava bene: 🛏", out.getvalue())

    def test_non_vedo_differenze_lascia_il_glifo(self):
        simboli = self._indice()["simboli"]
        pref = {s: {"interni": "tessera"} for s in simboli}
        pref["🛏"] = {"interni": "uguali"}
        self._scrivi_scheda({s: {"interni": "vince"} for s in simboli}, pref)
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(B.controlla(), 1)
        self.assertIn("non vede differenze", out.getvalue())

    def test_la_scelta_di_un_altra_fonte_non_approva_questa(self):
        simboli = self._indice()["simboli"]
        pref = {s: {"interni": f"tessera:{B.fonte_di(B.USCITA, s)}"} for s in simboli}
        pref["🛏"] = {"interni": "tessera:ComfyUI"}
        self._scrivi_scheda({s: {"interni": "vince"} for s in simboli}, pref)
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(B.controlla(), 1)
        self.assertIn("🛏: il DM ha preferito la tessera di un'altra fonte", out.getvalue())
        self.assertEqual(out.getvalue().count("✗"), 1)

    def test_adotta_prende_da_una_cartella_solo_cio_che_il_dm_ha_scelto_di_quella_fonte(self):
        cand = self.tmp / "comfy"
        cand.mkdir()
        voce = {"fonte": "ComfyUI", "licenza": B.LICENZA_GENERATA, "provenienza": "sdxl seme 1"}
        for k in ("zenitale-letto-a", "zenitale-statua-a"):
            (cand / f"{k}.webp").write_bytes(k.encode())
        (cand / "indice.json").write_text(json.dumps({
            "simboli": {"🛏": ["zenitale-letto-a"], "🗿": ["zenitale-statua-a"]},
            "tessere": {"zenitale-letto-a": voce, "zenitale-statua-a": voce}}), encoding="utf-8")
        self.assertEqual(B.fonte_di(cand, "🛏"), "ComfyUI")
        simboli = self._indice()["simboli"]
        pref = {s: {"interni": f"tessera:{B.fonte_di(B.USCITA, s)}"} for s in simboli}
        pref["🛏"] = {"interni": "tessera:ComfyUI"}     # 🗿 resta alla tessera CC0
        self._scrivi_scheda({s: {"interni": "vince"} for s in simboli}, pref)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(B.main(["--adotta", str(cand)]), 0)
            self.assertEqual(B.main(["--adotta"]), 0)    # l'ordine non conta
        indice = self._indice()
        self.assertEqual(indice["simboli"]["🛏"], ["zenitale-letto-a"])
        self.assertEqual(indice["simboli"]["🗿"], ["gothic_statue"])
        self.assertNotIn("zenitale-statua-a", indice["tessere"])

    def _indice(self):
        return json.loads(B.INDICE.read_text(encoding="utf-8"))

    def test_le_tessere_combaciano_con_l_indice(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(B.controlla(), 0)
        indice = self._indice()
        self.assertEqual(set(indice["tessere"]), set(B.PILOTA) | {"namaqualand_rocks_01-ns"})
        self.assertEqual(indice["simboli"]["🪨"], ["boulder_01", "namaqualand_boulders_01"])
        self.assertTrue(all(v["licenza"] == "CC0 1.0" and v["verificato"]
                            for v in indice["tessere"].values()))

    def test_una_tessera_toccata_e_bocciata(self):
        (B.USCITA / "gothic_statue.webp").write_bytes(b"altro")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(B.controlla(), 1)

    def test_un_modello_non_verificato_e_bocciato(self):
        indice = self._indice()
        indice["tessere"]["gothic_statue"]["verificato"] = False
        B.INDICE.write_text(json.dumps(indice), encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(B.controlla(), 1)

    def test_un_orientabile_senza_la_tessera_nord_sud_e_bocciato(self):
        (B.USCITA / "namaqualand_rocks_01-ns.webp").unlink()
        indice = self._indice()
        del indice["tessere"]["namaqualand_rocks_01-ns"]
        B.INDICE.write_text(json.dumps(indice), encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(B.controlla(), 1)

    def test_un_simbolo_che_resta_glifo_e_bocciato(self):
        indice = self._indice()
        indice["simboli"]["🚪"] = ["gothic_statue"]
        B.INDICE.write_text(json.dumps(indice), encoding="utf-8")
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(B.controlla(), 1)
        self.assertIn("resta glifo", out.getvalue())

    def test_un_file_della_cache_toccato_ferma_il_render(self):
        (B.CACHE / "polyhaven" / "gothic_statue" / "gothic_statue_1k.gltf").write_text("{}")
        err = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(err):
            self.assertEqual(B.main(["--rendi", "--prova"]), 1)
        self.assertIn("MD5", err.getvalue())

    def test_il_tema_texture_usa_le_tessere(self):
        svg = R.render_svg(_griglia(), "p.md", "texture")
        for k in ("boulder_01", "gothic_statue", "stone_fire_pit", "GothicBed_01"):
            self.assertIn(f'id="oc_{k}"', svg)
        self.assertIn("Oggetti di scena da modelli 3D CC0 1.0", svg)
        # i glifi sostituiti non entrano più nelle definizioni
        self.assertNotIn('id="pr_statue"', svg)

    def test_il_muretto_ha_due_tessere_e_segue_i_vicini(self):
        indice = self._indice()
        self.assertEqual(indice["orientabili"], ["namaqualand_rocks_01"])
        self.assertIn("namaqualand_rocks_01-ns", indice["tessere"])
        self.assertEqual(indice["simboli"]["🧱"], ["namaqualand_rocks_01"])
        svg = R.render_svg(_griglia(), "p.md", "texture")
        # F2-F3 è un tratto nord-sud, B4-C4 un tratto est-ovest
        self.assertIn('id="oc_namaqualand_rocks_01-ns"', svg)
        self.assertIn('id="oc_namaqualand_rocks_01"', svg)
        self.assertEqual(svg.count('href="#oc_namaqualand_rocks_01-ns"'), 2)
        self.assertEqual(svg.count('href="#oc_namaqualand_rocks_01"'), 3)   # due celle + legenda

    def test_il_braciere_tiene_la_fiamma_sopra_la_tessera(self):
        svg = R.render_svg(_griglia(), "p.md", "texture")
        dopo = svg.split('href="#oc_stone_fire_pit"', 1)[1]
        self.assertTrue(dopo.split("/>", 1)[1].lstrip().startswith('<use href="#pr_fire"'))

    def test_porte_e_fuoco_restano_glifi(self):
        svg = R.render_svg(_griglia(), "p.md", "texture")
        self.assertIn('id="pr_door"', svg)
        self.assertIn('id="pr_fire"', svg)

    def test_la_pergamena_non_cambia(self):
        svg = R.render_svg(_griglia(), "p.md")
        self.assertNotIn("oc_", svg)
        self.assertNotIn("data:image/webp", svg)

    def test_il_tema_texture_e_deterministico(self):
        g = _griglia()
        self.assertEqual(R.render_svg(g, "p.md", "texture"), R.render_svg(g, "p.md", "texture"))

    def test_la_misura_dello_stile_c_e_per_ogni_tessera(self):
        misure = B.misura_stile()
        self.assertEqual(set(misure), set(B.PILOTA) | {"namaqualand_rocks_01-ns"})
        m = misure["gothic_statue"]
        self.assertAlmostEqual(m["copertura"], 0.25, delta=0.05)
        self.assertEqual(m["saturazione"] > 0, True)


class TestSenzaTessere(unittest.TestCase):
    def test_senza_tessere_il_check_passa_e_lo_dice(self):
        vecchi = (B.USCITA, B.INDICE)
        B.USCITA = Path(tempfile.mkdtemp()) / "nessuna"
        B.INDICE = B.USCITA / "indice.json"
        try:
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(B.controlla(), 0)
            self.assertIn("non ancora fatte", out.getvalue())
        finally:
            B.USCITA, B.INDICE = vecchi

    def test_senza_tessere_il_tema_texture_tiene_i_glifi(self):
        vecchio = R.OGGETTI_CC0
        try:
            R.OGGETTI_CC0 = Path(tempfile.mkdtemp())
            svg = R.render_svg(_griglia(), "p.md", "texture")
            self.assertNotIn("oc_", svg)
            self.assertIn('id="pr_statue"', svg)
        finally:
            R.OGGETTI_CC0 = vecchio

    def test_le_tessere_non_sono_ignorate_da_git(self):
        r = subprocess.run(["git", "check-ignore", "-q", "scripts/oggetti-cc0/prova.webp"],
                           cwd=SCRIPTS.parent, capture_output=True)
        self.assertEqual(r.returncode, 1, "scripts/oggetti-cc0/*.webp è ignorato da git")

    def test_i_modelli_restano_fuori_da_git(self):
        r = subprocess.run(["git", "check-ignore", "-q",
                            "asset-esterni/oggetti-cc0/polyhaven/x/x_1k.gltf"],
                           cwd=SCRIPTS.parent, capture_output=True)
        self.assertEqual(r.returncode, 0, "i modelli scaricati finirebbero in git")

    def test_la_tabella_e_fatta_di_oggetti(self):
        tessere = [k for *_, k in B.tabella()]
        self.assertEqual(len(tessere), len(set(tessere)))
        for s, _, _, k in B.tabella():
            self.assertTrue(R.SYMBOLS[s].get("prop"), s)
            self.assertFalse(R.resta_glifo(s), f"{s} resta glifo, non può avere una tessera")
        self.assertTrue(set(B.PILOTA) <= set(tessere))
        self.assertTrue(set(B.GLTF_FISSATI) <= set(B.PILOTA))

    def test_le_chiusure_restano_glifi(self):
        for s in "🚪🔒❔🥅🪟⛓":
            self.assertTrue(R.resta_glifo(s), s)

    def test_i_cercati_in_quaternius_non_sono_gia_coperti(self):
        coperti = {s for s, *_ in B.OGGETTI}
        for s in B.CERCATI_IN_QUATERNIUS:
            self.assertNotIn(s, coperti)
            self.assertFalse(R.resta_glifo(s), s)


class TestQuaternius(unittest.TestCase):
    def _zip(self, licenza="Creative Commons Zero, CC0", extra=None):
        p = Path(tempfile.mkdtemp()) / "Fantasy Props MegaKit[Standard].zip"
        with zipfile.ZipFile(p, "w") as z:
            if licenza is not None:
                z.writestr("License.txt", licenza)
            z.writestr("glTF/Anvil.gltf", json.dumps({"buffers": [{"uri": "Anvil.bin"}],
                                                      "images": [{"uri": "../Textures/T.png"}]}))
            z.writestr("glTF/Anvil.bin", b"\0\1")
            z.writestr("Textures/T.png", b"png")
            for nome, dati in (extra or {}).items():
                z.writestr(nome, dati)
        return p

    def setUp(self):
        self.vecchi = (B.CACHE, B.QUATERNIUS_ZIP_SHA256, B.QUATERNIUS)
        B.CACHE = Path(tempfile.mkdtemp()) / "cache"

    def tearDown(self):
        B.CACHE, B.QUATERNIUS_ZIP_SHA256, B.QUATERNIUS = self.vecchi

    def test_l_elenco_dice_impronta_licenza_e_modelli(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(B.elenca_quaternius(self._zip()), 0)
        self.assertIn("sha256:", out.getvalue())
        self.assertIn("dice CC0", out.getvalue())
        self.assertIn("glTF/Anvil.gltf", out.getvalue())

    def test_senza_impronta_fissata_si_ferma_e_la_stampa(self):
        z = self._zip()
        B.QUATERNIUS_ZIP_SHA256 = ""
        with self.assertRaisesRegex(ValueError, hashlib.sha256(z.read_bytes()).hexdigest()):
            B.estrai_quaternius(z)

    def test_un_altro_zip_e_bocciato(self):
        B.QUATERNIUS_ZIP_SHA256 = "0" * 64
        with self.assertRaisesRegex(ValueError, "Pro"):
            B.estrai_quaternius(self._zip())

    def test_senza_licenza_cc0_e_bocciato(self):
        z = self._zip(licenza="All rights reserved")
        B.QUATERNIUS_ZIP_SHA256 = hashlib.sha256(z.read_bytes()).hexdigest()
        with self.assertRaisesRegex(ValueError, "CC0"):
            B.estrai_quaternius(z)

    def test_estrae_il_modello_con_le_texture_richiamate(self):
        z = self._zip()
        B.QUATERNIUS_ZIP_SHA256 = hashlib.sha256(z.read_bytes()).hexdigest()
        B.QUATERNIUS = (("⚒", "glTF/Anvil.gltf"),)
        fonte, = B.estrai_quaternius(z)
        self.assertEqual(fonte["licenza"], "CC0 1.0")
        self.assertEqual(set(fonte["file"]), {"glTF/Anvil.gltf", "glTF/Anvil.bin", "Textures/T.png"})
        verificata = B.verifica_in_cache("quaternius-anvil")
        self.assertTrue(Path(verificata["_cartella"], "Textures", "T.png").exists())

    def test_un_percorso_che_esce_dalla_cartella_e_rifiutato(self):
        with self.assertRaises(ValueError):
            B._percorso_sicuro(Path("/tmp/x"), "../fuori.txt")
        with self.assertRaises(ValueError):
            B._percorso_sicuro(Path("/tmp/x"), "/assoluto")


if __name__ == "__main__":
    unittest.main()


class TestComandoBlender(unittest.TestCase):
    """Il modulo bpy, la cui versione fissa requirements-completo, viene prima del
    programma della distribuzione (il 2026-10-09 il Blender di Debian, senza
    OpenImageDenoise, veniva preso al posto del bpy del .venv)."""

    def setUp(self):
        self.vecchi = (B.importlib.util.find_spec, B.shutil.which)

    def tearDown(self):
        B.importlib.util.find_spec, B.shutil.which = self.vecchi

    def test_bpy_prima_del_programma(self):
        B.importlib.util.find_spec = lambda n: object() if n == "bpy" else None
        B.shutil.which = lambda n: "/usr/bin/blender"
        self.assertEqual(B.comando_blender(None), [sys.executable, str(B.SCENA)])

    def test_senza_bpy_il_programma(self):
        B.importlib.util.find_spec = lambda n: None
        B.shutil.which = lambda n: "/usr/bin/blender"
        self.assertEqual(B.comando_blender(None)[0], "blender")

    def test_esplicito_vince_su_tutto(self):
        self.assertEqual(B.comando_blender("flatpak run org.blender.Blender")[:3],
                         ["flatpak", "run", "org.blender.Blender"])


class TestAdottaSenzaTessere(unittest.TestCase):
    def test_un_messaggio_e_non_un_traceback(self):
        vecchi = (B.USCITA, B.INDICE)
        B.USCITA = Path(tempfile.mkdtemp()) / "vuota"
        B.INDICE = B.USCITA / "indice.json"
        err = io.StringIO()
        try:
            with redirect_stdout(io.StringIO()), redirect_stderr(err):
                self.assertEqual(B.main(["--adotta"]), 1)
        finally:
            B.USCITA, B.INDICE = vecchi
        self.assertIn("prima le tessere", err.getvalue())
