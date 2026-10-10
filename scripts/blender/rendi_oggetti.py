#!/usr/bin/env python3
"""rendi_oggetti.py — rende dall'alto i modelli 3D CC0 degli oggetti di scena.

⚠️ **Non si lancia a mano.** Gira dentro Blender, oppure con il modulo `bpy`
installato nel Python che lo esegue (R4-ter di PIANO-RESA-E-ASSET, D17):

    blender -b --factory-startup -noaudio -P scripts/blender/rendi_oggetti.py -- <lavoro.json>
    python3 scripts/blender/rendi_oggetti.py <lavoro.json>        # con `pip install bpy`

Il driver è [`scripts/build_oggetti_cc0.py`](../build_oggetti_cc0.py): scarica i
modelli, ne verifica l'impronta e scrive il lavoro che questo file consuma.
Qui resta solo ciò che richiede Blender per esistere.

I lock sono gli stessi per ogni modello, ed è quello che tiene insieme il set
(`rumblingstone-art-direction` §4). Arrivano dal lavoro, scritti dal driver:

- **camera** ortografica, zenitale, il nord in alto; l'inquadratura è una cella;
- **scala**: l'impronta del modello, sul suo lato più lungo, occupa la stessa
  frazione della cella per ogni oggetto (D20); l'asse lungo va est-ovest, e un
  oggetto orientabile come il muretto ha anche la sua tessera nord-sud, resa
  girando il modello e non l'immagine;
- **luce**: un sole da nord-ovest, alto, sempre lo stesso, e un fondo tenue;
  l'ombra cade a sud-est come l'ombra disegnata dei glifi della pergamena;
- **ombra** su un piano che la raccoglie e resta trasparente;
- **colore** in trasformazione «Standard», senza curve: il colore del
  materiale arriva com'è, e la velatura del tema texture fa il resto.

Exit code: 0 = ok · 1 = lavoro illeggibile, modello che non si importa, render fallito.
"""
import json
import math
import sys
from pathlib import Path

try:
    import bpy
    import mathutils
except ImportError:  # pragma: no cover - fuori da Blender non esiste
    print("Questo script gira dentro Blender o con il modulo bpy:\n"
          "  python3 scripts/build_oggetti_cc0.py --rendi    (il driver lo chiama da sé)",
          file=sys.stderr)
    sys.exit(1)


def _argomenti() -> Path:
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] if "--" in argv else argv[1:]
    if len(argv) != 1:
        raise SystemExit("uso: rendi_oggetti.py <lavoro.json>")
    return Path(argv[0])


def _ha_denoiser() -> bool:
    """OpenImageDenoise c'è in questa build? Il Blender di Debian 13 (4.3) è
    compilato senza, e con `use_denoising` acceso il render si ferma («Failed to
    denoise, build has no OpenImageDenoise support»): il 2026-10-09, sulla
    macchina del DM. Senza denoiser la tessera esce con un po' più di grana, e
    l'indice lo scrive."""
    return bool(getattr(bpy.app.build_options, "openimagedenoise", True))


def _scena_vuota():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy.context.scene


def _impostazioni(scena, lock: dict) -> None:
    scena.render.engine = "CYCLES"
    scena.cycles.device = "CPU"
    scena.cycles.samples = int(lock["campioni"])
    scena.cycles.seed = int(lock["seme"])
    scena.cycles.use_denoising = bool(lock.get("denoise", True)) and _ha_denoiser()
    scena.render.film_transparent = True
    scena.render.resolution_x = scena.render.resolution_y = int(lock["lato_render"])
    scena.render.resolution_percentage = 100
    scena.render.image_settings.file_format = "PNG"
    scena.render.image_settings.color_mode = "RGBA"
    scena.render.image_settings.color_depth = "8"
    scena.view_settings.view_transform = "Standard"
    scena.view_settings.look = "None"
    scena.view_settings.exposure = 0.0
    scena.view_settings.gamma = 1.0


def _luce_e_camera(scena, lock: dict) -> None:
    mondo = bpy.data.worlds.new("fondo")
    mondo.use_nodes = True
    sfondo = mondo.node_tree.nodes["Background"]
    sfondo.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
    sfondo.inputs[1].default_value = float(lock["fondo"])
    scena.world = mondo

    sole = bpy.data.lights.new("sole", type="SUN")
    sole.energy = float(lock["sole"])
    sole.angle = math.radians(float(lock["sole_morbidezza_gradi"]))
    ogg = bpy.data.objects.new("sole", sole)
    # azimut misurato dal nord in senso orario: la luce VIENE da lì
    az = math.radians(float(lock["sole_azimut_gradi"]))
    el = math.radians(float(lock["sole_elevazione_gradi"]))
    verso = mathutils.Vector((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)))
    ogg.rotation_euler = (-verso).to_track_quat("-Z", "Y").to_euler()
    scena.collection.objects.link(ogg)

    cam = bpy.data.cameras.new("zenit")
    cam.type = "ORTHO"
    cam.ortho_scale = 1.0
    cam.clip_start, cam.clip_end = 0.01, 100.0
    cam_ogg = bpy.data.objects.new("zenit", cam)
    cam_ogg.location = (0.0, 0.0, 20.0)
    cam_ogg.rotation_euler = (0.0, 0.0, 0.0)      # guarda giù, il nord (+Y) in alto
    scena.collection.objects.link(cam_ogg)
    scena.camera = cam_ogg

    bpy.ops.mesh.primitive_plane_add(size=4.0, location=(0.0, 0.0, 0.0))
    piano = bpy.context.active_object
    piano.name = "raccoglie-ombra"
    piano.is_shadow_catcher = True


def _importa(percorso: Path) -> list:
    prima = set(bpy.data.objects)
    suffisso = percorso.suffix.lower()
    if suffisso in (".gltf", ".glb"):
        bpy.ops.import_scene.gltf(filepath=str(percorso))
    elif suffisso == ".obj":
        bpy.ops.wm.obj_import(filepath=str(percorso))
    elif suffisso == ".fbx":
        bpy.ops.import_scene.fbx(filepath=str(percorso))
    else:
        raise ValueError(f"formato non previsto: {percorso.name}")
    nuovi = [o for o in bpy.data.objects if o not in prima]
    if not any(o.type == "MESH" for o in nuovi):
        raise ValueError(f"{percorso.name}: nessuna mesh")
    return nuovi


def _scatola(oggetti: list) -> tuple:
    bpy.context.view_layer.update()
    punti = [o.matrix_world @ mathutils.Vector(v) for o in oggetti if o.type == "MESH"
             for v in o.bound_box]
    lo = mathutils.Vector((min(p.x for p in punti), min(p.y for p in punti), min(p.z for p in punti)))
    hi = mathutils.Vector((max(p.x for p in punti), max(p.y for p in punti), max(p.z for p in punti)))
    return lo, hi


def _metti_in_cella(oggetti: list, impronta: float, asse: str = "ew") -> dict:
    """Centra, appoggia a terra, gira l'asse lungo a est-ovest (o a nord-sud per
    la seconda tessera di un oggetto orientabile), scala l'impronta."""
    radice = bpy.data.objects.new("modello", None)
    bpy.context.scene.collection.objects.link(radice)
    for o in oggetti:
        if o.parent is None:
            o.parent = radice
    lo, hi = _scatola(oggetti)
    girato = (hi.y - lo.y) > (hi.x - lo.x) * 1.05
    if girato != (asse == "ns"):
        radice.rotation_euler = (0.0, 0.0, math.radians(90.0))
        lo, hi = _scatola(oggetti)
    lato = max(hi.x - lo.x, hi.y - lo.y)
    s = impronta / lato
    radice.scale = (s, s, s)
    lo, hi = _scatola(oggetti)
    centro = (lo + hi) / 2
    radice.location = (radice.location.x - centro.x, radice.location.y - centro.y,
                       radice.location.z - lo.z)
    bpy.context.view_layer.update()
    return {"scala": round(s, 6), "girato": girato,
            "impronta_m": [round(hi.x - lo.x, 4), round(hi.y - lo.y, 4)],
            "lato_originale_m": round(lato, 4)}


def main() -> int:
    try:
        lavoro = json.loads(_argomenti().read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"✗ rendi_oggetti: {e}", file=sys.stderr)
        return 1
    lock = lavoro["lock"]
    esiti = {}
    for voce in lavoro["modelli"]:
        scena = _scena_vuota()
        _impostazioni(scena, lock)
        _luce_e_camera(scena, lock)
        try:
            oggetti = _importa(Path(voce["modello"]))
            misura = _metti_in_cella(oggetti, float(voce.get("impronta", lock["impronta"])),
                                     voce.get("asse", "ew"))
            scena.render.filepath = voce["uscita"]
            bpy.ops.render.render(write_still=True)
        except (RuntimeError, ValueError) as e:
            print(f"✗ {voce['tessera']}: {e}", file=sys.stderr)
            return 1
        esiti[voce["tessera"]] = misura
        print(f"✓ {voce['tessera']}: scala {misura['scala']}, "
              f"lato originale {misura['lato_originale_m']} m")
    Path(lavoro["esiti"]).write_text(json.dumps(esiti, indent=1) + "\n", encoding="utf-8")
    print(f"Blender {bpy.app.version_string}")
    if lock.get("denoise", True) and not _ha_denoiser():
        print("○ questa build di Blender non ha OpenImageDenoise: tessere rese senza denoise")
    return 0


if __name__ == "__main__":
    sys.exit(main())
