"""R4-ter con Blender vero: la scena, la luce e l'impronta su modelli procedurali.

`test_oggetti_cc0` sostituisce Blender con uno script finto e prova la catena
attorno alla scena. Questo prova la scena: crea due modelli glTF con bpy (una
roccia e un muretto orientabile), li mette nella cache come se venissero da
Poly Haven e li rende con `build_oggetti_cc0 --rendi --prova`. Non serve rete.

Gira solo dove `bpy` c'è (`pip install bpy`, Python 3.13): in CI si salta,
sulla macchina del DM dice se la scena funziona prima di scaricare i modelli
veri. È la prova fatta a mano il 2026-10-09 (9 tessere in 18 s), messa dove
non si perde.
"""

import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import build_oggetti_cc0 as B  # noqa: E402

BPY = importlib.util.find_spec("bpy") is not None

FAI_MODELLI = r'''
import bpy, sys
out = sys.argv[1]
def materiale(nome, rgb):
    m = bpy.data.materials.new(nome); m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*rgb, 1)
    return m
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=0.6, location=(0, 0, 0.3))
o = bpy.context.active_object; o.scale = (1.0, 0.7, 0.45)
o.data.materials.append(materiale("pietra", (0.4, 0.38, 0.35)))
bpy.ops.export_scene.gltf(filepath=f"{out}/roccia.gltf", export_format="GLTF_SEPARATE")
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.075))
o = bpy.context.active_object; o.scale = (1.45, 0.22, 0.15)
o.data.materials.append(materiale("pietre", (0.3, 0.28, 0.25)))
bpy.ops.export_scene.gltf(filepath=f"{out}/fila.gltf", export_format="GLTF_SEPARATE")
'''

FORME = {"boulder_01": "roccia", "namaqualand_rocks_01": "fila"}


@unittest.skipUnless(BPY, "serve bpy (pip install bpy, Python 3.13)")
class TestBlenderVero(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.vecchi = (B.CACHE, B.USCITA, B.INDICE, B.PILOTA)
        B.CACHE, B.USCITA = self.tmp / "cache", self.tmp / "tessere"
        B.INDICE, B.PILOTA = B.USCITA / "indice.json", tuple(FORME)
        modelli = self.tmp / "modelli"
        modelli.mkdir()
        fai = self.tmp / "fai_modelli.py"
        fai.write_text(FAI_MODELLI, encoding="utf-8")
        subprocess.run([sys.executable, str(fai), str(modelli)], check=True, capture_output=True)
        for pid, forma in FORME.items():
            d = B.CACHE / "polyhaven" / pid
            d.mkdir(parents=True)
            g = json.loads((modelli / f"{forma}.gltf").read_text(encoding="utf-8"))
            g["buffers"][0]["uri"] = f"{pid}.bin"
            (d / f"{pid}_1k.gltf").write_text(json.dumps(g), encoding="utf-8")
            (d / f"{pid}.bin").write_bytes((modelli / f"{forma}.bin").read_bytes())
            file = {n: {"url": "procedurale", "md5": hashlib.md5((d / n).read_bytes()).hexdigest()}
                    for n in (f"{pid}_1k.gltf", f"{pid}.bin")}
            (d / "fonte.json").write_text(json.dumps({
                "fonte": "PROVA procedurale", "id": pid, "pagina": "-", "licenza": "CC0 1.0",
                "modello": f"{pid}_1k.gltf", "file": file}), encoding="utf-8")

    def tearDown(self):
        B.CACHE, B.USCITA, B.INDICE, B.PILOTA = self.vecchi

    def test_la_scena_rende_tessere_con_la_figura_al_centro_e_il_fondo_trasparente(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(B.main(["--rendi", "--prova"]), 0)
        from PIL import Image
        indice = json.loads(B.INDICE.read_text(encoding="utf-8"))
        self.assertEqual(indice["orientabili"], ["namaqualand_rocks_01"])
        for k in ("boulder_01", "namaqualand_rocks_01", "namaqualand_rocks_01-ns"):
            im = Image.open(B.USCITA / f"{k}.webp").convert("RGBA")
            self.assertEqual(im.size, (B.LATO, B.LATO))
            alfa = im.getchannel("A")
            self.assertLess(alfa.getpixel((0, 0)), 16, f"{k}: l'angolo deve essere trasparente (al più un velo d'ombra)")
            self.assertGreater(alfa.getpixel((B.LATO // 2, B.LATO // 2)), 200, f"{k}: il centro è vuoto")
        # il muretto nord-sud è quello est-ovest girato: più alto che largo
        def sagoma(k):  # solo la figura: l'ombra è un velo leggero su tutta la tessera
            a = Image.open(B.USCITA / f"{k}.webp").getchannel("A")
            return a.point(lambda v: 255 if v > 128 else 0).getbbox()
        ew, ns = sagoma("namaqualand_rocks_01"), sagoma("namaqualand_rocks_01-ns")
        self.assertGreater(ew[2] - ew[0], ew[3] - ew[1])
        self.assertGreater(ns[3] - ns[1], ns[2] - ns[0])


if __name__ == "__main__":
    unittest.main()
