#!/usr/bin/env python3
"""costruisci_mappa.py — costruisce e rende la scena dentro Blender.

⚠️ **Non si lancia a mano.** Gira solo dentro Blender, che ha il suo Python e la
sua `bpy`:

    blender -b -noaudio -P scripts/blender/costruisci_mappa.py -- --piano <piano.json>

Il driver è [`scripts/render_map_blender.py`](../render_map_blender.py): legge il
JSON della mappa, risolve la geometria con lo **stesso** `paint()` che alimenta
l'SVG, e scrive il piano di scena che questo file consuma. La separazione è
voluta: tutta la logica che si può provare senza una GPU sta di là, sotto test;
qui resta solo ciò che richiede Blender per esistere.

Cosa costruisce, e perché così:

- **nessun piano di appoggio**: ogni cella è un solido, terreno di base
  compreso. Con un piano sotto, una voragine o uno specchio d'acqua resterebbero
  coperti e il passo di profondità li leggerebbe piatti;
- **un oggetto per simbolo**, non uno per cella: le celle uguali sono già fuse in
  rettangoli dal driver, e raggrupparle per materiale tiene la scena leggera;
- **niente UV**: i materiali usano la proiezione a scatola sulle coordinate
  oggetto, che su volumi squadrati è indistinguibile da una mappatura fatta a
  mano e non richiede di srotolare niente.

Exit code: 0 = ok · 1 = piano illeggibile o render fallito.
"""
import json
import math
import sys
from pathlib import Path

try:
    import bpy
    import mathutils
except ImportError:  # pragma: no cover - fuori da Blender non esiste
    print(
        "Questo script gira solo dentro Blender:\n"
        "  blender -b -noaudio -P scripts/blender/costruisci_mappa.py -- --piano <piano.json>\n"
        "Per il piano di scena da solo usa: python3 scripts/render_map_blender.py <mappa.json> --piano-solo",
        file=sys.stderr,
    )
    raise SystemExit(1)

SPESSORE_MIN = 0.02
ESTENSIONI = (".png", ".jpg", ".jpeg", ".exr", ".tif", ".tiff")


def argomenti() -> dict:
    """Blender passa alla scena tutto ciò che segue `--`."""
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if "--piano" not in argv:
        print("manca --piano <file>", file=sys.stderr)
        raise SystemExit(1)
    return {"piano": Path(argv[argv.index("--piano") + 1])}


def scena_vuota() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def motore(scena, campioni: int) -> str:
    """EEVEE se c'è, Cycles come rete di sicurezza.

    Il nome dell'engine EEVEE è cambiato fra le versioni di Blender
    (`BLENDER_EEVEE` → `BLENDER_EEVEE_NEXT`), quindi si prova invece di
    assumere: una mappa non vale il costo di Cycles, ma un errore di stringa non
    vale il costo di non renderla affatto.
    """
    for nome in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
        try:
            scena.render.engine = nome
        except TypeError:
            continue
        if nome == "CYCLES":
            scena.cycles.samples = campioni
        else:
            try:
                scena.eevee.taa_render_samples = campioni
            except AttributeError:
                pass
        return nome
    return scena.render.engine


def rgb(esadecimale: str) -> tuple[float, float, float, float]:
    """Da `#rrggbb` a lineare: Blender lavora in lineare, il CSS in sRGB.

    Saltare la conversione è l'errore che fa uscire tutte le mappe slavate.
    """
    e = esadecimale.lstrip("#")
    canali = [int(e[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    lineare = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in canali]
    return (*lineare, 1.0)


def trova_texture(cartella: Path, chiave: str | None) -> Path | None:
    """La prima immagine dentro `texture/<chiave>/`, se il DM ce l'ha messa.

    Assente = si usa il colore piatto. È voluto: la catena deve produrre una
    mappa leggibile su una macchina appena clonata, senza scaricare niente.
    """
    if not chiave:
        return None
    percorso = cartella / chiave
    if not percorso.is_dir():
        return None
    for file in sorted(percorso.iterdir()):
        if file.suffix.lower() in ESTENSIONI and "color" in file.stem.lower():
            return file
    for file in sorted(percorso.iterdir()):
        if file.suffix.lower() in ESTENSIONI:
            return file
    return None


def materiale(nome: str, colore: str, texture: Path | None, scala_uv: float):
    mat = bpy.data.materials.new(nome)
    mat.use_nodes = True
    nodi = mat.node_tree.nodes
    collegamenti = mat.node_tree.links
    bsdf = nodi.get("Principled BSDF")
    if bsdf is None:
        return mat
    bsdf.inputs["Base Color"].default_value = rgb(colore)
    for etichetta, valore in (("Roughness", 0.85), ("Specular IOR Level", 0.2), ("Specular", 0.2)):
        if etichetta in bsdf.inputs:
            bsdf.inputs[etichetta].default_value = valore

    if texture is None:
        return mat

    immagine = nodi.new("ShaderNodeTexImage")
    immagine.image = bpy.data.images.load(str(texture))
    immagine.projection = "BOX"        # niente UV da srotolare
    immagine.projection_blend = 0.25
    coordinate = nodi.new("ShaderNodeTexCoord")
    mappatura = nodi.new("ShaderNodeMapping")
    mappatura.inputs["Scale"].default_value = (scala_uv, scala_uv, scala_uv)
    collegamenti.new(coordinate.outputs["Object"], mappatura.inputs["Vector"])
    collegamenti.new(mappatura.outputs["Vector"], immagine.inputs["Vector"])
    collegamenti.new(immagine.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def scatola(x, y, larghezza, profondita, z0, z1, base_v: int):
    """Gli otto vertici e le sei facce di un parallelepipedo, già indicizzati."""
    verti = [
        (x, y, z0), (x + larghezza, y, z0), (x + larghezza, y + profondita, z0), (x, y + profondita, z0),
        (x, y, z1), (x + larghezza, y, z1), (x + larghezza, y + profondita, z1), (x, y + profondita, z1),
    ]
    b = base_v
    facce = [
        (b + 0, b + 1, b + 2, b + 3), (b + 7, b + 6, b + 5, b + 4),
        (b + 0, b + 4, b + 5, b + 1), (b + 1, b + 5, b + 6, b + 2),
        (b + 2, b + 6, b + 7, b + 3), (b + 3, b + 7, b + 4, b + 0),
    ]
    return verti, facce


def costruisci(piano: dict) -> None:
    """Un oggetto per simbolo: le celle sono già fuse, i materiali si condividono."""
    cartella_texture = Path(piano.get("texture_dir", ""))
    spessore = piano.get("spessore_lastra_m", SPESSORE_MIN)
    scala = piano.get("scala_m_per_quadretto", 1.5)
    profondita_mappa = piano["terreno_base"]["profondita_m"]

    gruppi: dict[str, list[dict]] = {}
    for solido in piano["solidi"]:
        gruppi.setdefault(solido["simbolo"], []).append(solido)

    for indice, (simbolo, solidi) in enumerate(gruppi.items()):
        verti, facce = [], []
        for s in solidi:
            h = s["altezza_m"]
            # h > 0: volume pieno da terra, così ha fianchi e proietta ombra.
            # h <= 0: lastra sottile alla sua quota — dall'alto la profondità
            #         letta è quella giusta, e una voragine resta una voragine.
            z0, z1 = (0.0, h) if h > 0 else (h, h + spessore)
            # L'asse Y di Blender sale, quello della griglia scende: senza questo
            # ribaltamento la mappa esce speculare, ed è l'errore che non si nota
            # finché qualcuno non cerca la curva nord a sud.
            y = profondita_mappa - s["y_m"] - s["profondita_m"]
            v, f = scatola(s["x_m"], y, s["larghezza_m"], s["profondita_m"], z0, z1, len(verti))
            verti += v
            facce += f

        mesh = bpy.data.meshes.new(f"mappa_{indice}")
        mesh.from_pydata(verti, [], facce)
        mesh.update()
        for poligono in mesh.polygons:
            poligono.use_smooth = False   # spigoli netti: sono muri, non colline
        oggetto = bpy.data.objects.new(f"{simbolo or 'base'}_{indice}", mesh)
        bpy.context.scene.collection.objects.link(oggetto)

        primo = solidi[0]
        oggetto.data.materials.append(
            materiale(
                f"mat_{indice}",
                primo["colore"],
                trova_texture(cartella_texture, primo.get("texture")),
                1.0 / max(scala * 2, 0.001),
            )
        )


def punta_verso(oggetto, bersaglio) -> None:
    direzione = mathutils.Vector(bersaglio) - oggetto.location
    oggetto.rotation_euler = direzione.to_track_quat("-Z", "Y").to_euler()


def inquadra(piano: dict) -> None:
    larghezza = piano["terreno_base"]["larghezza_m"]
    profondita = piano["terreno_base"]["profondita_m"]
    centro = (larghezza / 2, profondita / 2, 0.0)
    spec = piano["camera"]

    dati = bpy.data.cameras.new("camera")
    camera = bpy.data.objects.new("camera", dati)
    bpy.context.scene.collection.objects.link(camera)
    bpy.context.scene.camera = camera

    if spec["tipo"] == "orto":
        dati.type = "ORTHO"
        dati.ortho_scale = spec["scala_orto_m"]
        camera.location = (centro[0], centro[1], spec["altezza_m"])
        camera.rotation_euler = (0.0, 0.0, 0.0)   # -Z guarda già a picco
    else:
        dati.type = "PERSP"
        dati.lens = 45
        distanza = spec["scala_orto_m"]
        camera.location = (
            centro[0] - distanza * 0.55,
            centro[1] - distanza * 0.75,
            distanza * 0.65,
        )
        punta_verso(camera, centro)

    dati.clip_end = max(spec["altezza_m"] * 4, 1000)


def illumina(piano: dict) -> None:
    """Il lock di luce del set: azimut ed elevazione arrivano dal piano, non da qui.

    Sono gli stessi numeri per tutte le mappe di un modulo (skill
    rumblingstone-art-direction §4): luci che arrivano da parti diverse nella
    stessa città sono la prima cosa che l'occhio nota quando non torna.
    """
    spec = piano["luce"]
    larghezza = piano["terreno_base"]["larghezza_m"]
    profondita = piano["terreno_base"]["profondita_m"]
    centro = mathutils.Vector((larghezza / 2, profondita / 2, 0.0))
    raggio = max(larghezza, profondita)

    azimut = math.radians(spec["azimut"])
    elevazione = math.radians(spec["elevazione"])
    dati = bpy.data.lights.new("sole", type="SUN")
    dati.energy = spec["intensita"]
    dati.angle = math.radians(2.0)     # ombre appena morbide: a picco, nette stancano
    sole = bpy.data.objects.new("sole", dati)
    bpy.context.scene.collection.objects.link(sole)
    sole.location = centro + mathutils.Vector((
        raggio * math.cos(elevazione) * math.sin(azimut),
        raggio * math.cos(elevazione) * math.cos(azimut),
        raggio * math.sin(elevazione),
    ))
    punta_verso(sole, centro)

    mondo = bpy.data.worlds.new("mondo")
    bpy.context.scene.world = mondo
    mondo.use_nodes = True
    sfondo = mondo.node_tree.nodes.get("Background")
    if sfondo:
        sfondo.inputs["Color"].default_value = (0.62, 0.60, 0.55, 1.0)
        sfondo.inputs["Strength"].default_value = 0.45


def compositore_profondita(scena) -> None:
    """Il passo Z diventa un'immagine leggibile da ControlNet depth.

    Due passaggi che non sono opzionali: **Normalizza**, perché il pass Z è in
    metri e un PNG no; e **Inverti**, perché ControlNet si aspetta il vicino
    CHIARO mentre il pass Z ha il vicino piccolo, quindi scuro. Saltare
    l'inversione dà un'immagine che sembra giusta e guida il modello al
    contrario.
    """
    scena.view_layers[0].use_pass_z = True
    scena.use_nodes = True
    albero = scena.node_tree
    albero.nodes.clear()

    strati = albero.nodes.new("CompositorNodeRLayers")
    normalizza = albero.nodes.new("CompositorNodeNormalize")
    inverti = albero.nodes.new("CompositorNodeInvert")
    uscita = albero.nodes.new("CompositorNodeComposite")

    uscita_z = strati.outputs.get("Depth") or strati.outputs.get("Z")
    albero.links.new(uscita_z, normalizza.inputs[0])
    albero.links.new(normalizza.outputs[0], inverti.inputs["Color"])
    albero.links.new(inverti.outputs[0], uscita.inputs["Image"])
    # In profondità il colore non conta: si spegne la vista per non pagarla.
    scena.render.film_transparent = False


def rendi(piano: dict) -> None:
    scena = bpy.context.scene
    spec = piano["render"]
    scena.render.resolution_x = spec["larghezza_px"]
    scena.render.resolution_y = spec["altezza_px"]
    scena.render.resolution_percentage = 100
    scena.render.image_settings.file_format = "PNG"
    scena.render.image_settings.color_mode = "RGB"
    scena.render.film_transparent = False
    motore(scena, spec["campioni"])

    if spec["profondita"]:
        compositore_profondita(scena)
        scena.render.image_settings.color_depth = "16"

    uscita = Path(piano["uscita"])
    uscita.parent.mkdir(parents=True, exist_ok=True)
    # Blender aggiunge lui l'estensione: passargliela produce «...png.png».
    scena.render.filepath = str(uscita.with_suffix(""))
    scena.render.use_file_extension = True
    bpy.ops.render.render(write_still=True)


def main() -> int:
    args = argomenti()
    try:
        piano = json.loads(args["piano"].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"piano illeggibile: {e}", file=sys.stderr)
        return 1

    scena_vuota()
    costruisci(piano)
    inquadra(piano)
    illumina(piano)
    rendi(piano)
    print(f"reso {piano['uscita']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
