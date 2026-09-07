#!/usr/bin/env python3
"""render_map_blender.py — la mappa in volume: geometria dal JSON, render ortografico.

In un modulo pubblicato la tavola della locanda e la pianta della locanda sono
**la stessa stanza**. Nel repo erano due cose scollegate: la pianta nasce da un
contratto JSON, l'illustrazione da un prompt, e nessuno garantiva che le curve
fossero al posto giusto.

Questo tool chiude quel divario usando Blender per la cosa in cui è imbattibile —
**la geometria** — e non per disegnare: i ritratti li fa meglio un generatore.
La pianta è la stessa che rende l'SVG (stesso `paint()`, stesso vocabolario di
simboli), estrusa in altezza e ripresa con una camera ortografica.

    mappa.json → compile_map_json.paint() → griglia → solidi → Blender → PNG
                          ↑
                  la STESSA usata da render_map_svg.py

Due usi, e il secondo è quello che vale di più:

1. **la veduta**: un colpo d'occhio in volume della pianta esatta;
2. **il passo di PROFONDITÀ** (`--profondita`), che si dà in pasto a ControlNet
   depth in ComfyUI: l'illustrazione generata eredita la pianta reale, con le
   curve al posto giusto. È il pezzo che distingue un AP pubblicato.

Uso:
    python3 scripts/render_map_blender.py mappa.json --piano-solo   # il piano, senza Blender
    python3 scripts/render_map_blender.py mappa.json                # veduta ortografica
    python3 scripts/render_map_blender.py mappa.json --profondita   # per ControlNet depth
    python3 scripts/render_map_blender.py mappa.json --vista tre-quarti

Input:  un JSON conforme a `scripts/schemas/tactical_map.schema.json`
Output: `<cartella>/rendered/blender/<slug>[-depth].png` (gitignorato: è
        presentazione, non master) e il piano di scena `.piano.json` accanto

Dipendenze: **sola stdlib** nel driver. Il render vuole il binario `blender`
(GPL, https://blender.org); se manca, il tool dice come si installa ed esce
pulito — il piano di scena resta scritto e riutilizzabile.

Le **unità non entrano mai** nel render: i token sono un livello da VTT, e una
tavola d'illustrazione con i segnalini sopra non è una tavola.

Exit code: 0 = ok · 1 = binario assente, JSON non valido o render fallito ·
2 = uso errato (file mancante).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COSTRUTTORE = ROOT / "scripts" / "blender" / "costruisci_mappa.py"
TEXTURE_DIR = ROOT / "scripts" / "blender" / "texture"


def _carica(nome: str, percorso: Path):
    """Importa un modulo del repo per percorso, senza pacchetto."""
    spec = importlib.util.spec_from_file_location(nome, percorso)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nome] = modulo
    spec.loader.exec_module(modulo)
    return modulo


cmj = _carica("compile_map_json", ROOT / "scripts" / "compile_map_json.py")
rms = _carica("render_map_svg", ROOT / "scripts" / "render_map_svg.py")

INSTALLA = """\
Il binario «blender» non è nel PATH. È GPL e gira anche headless:

  Fedora/Bazzite  flatpak install flathub org.blender.Blender
                  (poi: flatpak run org.blender.Blender -b …, oppure --blender <cmd>)
  Arch            pacman -S blender
  Debian/Ubuntu   apt install blender
  Tutti           https://www.blender.org/download/  (tarball portabile)

Il piano di scena è stato scritto lo stesso: quando installi Blender, il render
riparte da lì senza rifare niente.
"""

# ── Quanto è alto ogni simbolo ───────────────────────────────────────────────
# In METRI, non in quadretti: un muro è alto 4 m che la griglia sia da 1,5 m o
# da 3. Zero = superficie piatta (si vede il colore, non un volume); negativo =
# scavato. Sono i valori che rendono leggibile una vista dall'alto: contano i
# RAPPORTI fra le altezze, non la loro esattezza archeologica.
ALTEZZE: dict[str, float] = {
    # scavi
    "🕳": -2.5,   # voragine
    "🟦": -0.6,   # acqua profonda
    "🌊": -0.3,   # acqua corrente
    # superfici piatte: restano a zero e parlano col colore
    "🟩": 0.0, "🟫": 0.0, "🟨": 0.0, "⬜": 0.0, "🟧": 0.0, "🟥": 0.0,
    # rilievi bassi
    "🌿": 0.4, "🪨": 0.9, "❄": 0.1, "🕸": 0.6,
    # arredo e ingombri
    "📦": 1.1, "🏺": 0.9, "🛏": 0.5, "🪓": 1.6, "⚰": 0.8, "🏮": 1.4, "🗿": 2.2,
    # strutture
    "⬛": 3.2,    # edificio, tenda, dais
    "🏰": 4.0,    # muro / roccia solida
    "🏛": 5.5,    # edificio / tempio
    "🗼": 9.0,    # torre
    "🟪": 5.0,    # pilastro
    "⛰": 7.0,    # creste rocciose
    "🌲": 5.0,    # chioma
    "🌳": 5.5,
    "🌉": 0.8,    # ponte: impalcato appena sopra il piano
}
# Le porte sono un varco, non un volume: se fossero alte quanto il muro, la
# pianta perderebbe l'unica informazione che una porta porta.
PIATTI = {"🚪", "⬇", "🎯", "⭐", "✨", "⚔", "🖼"}
ALTEZZA_ICONA_DEFAULT = 0.6

# Chiave di texture per famiglia di superficie. NON è uno slug di Poly Haven:
# è il nome della cartella che il DM riempie con l'asset che sceglie, verificando
# la licenza del singolo file. Vedi scripts/blender/texture/README.md.
TEXTURE: dict[str, str] = {
    "🟩": "erba", "🌿": "erba", "🌲": "fogliame", "🌳": "fogliame",
    "🟫": "terra-battuta", "🟨": "sabbia", "⬜": "pavimento",
    "🏰": "muratura", "⬛": "legno", "🏛": "pietra-chiara", "🟪": "pietra-chiara",
    "⛰": "roccia", "🪨": "roccia", "🟦": "acqua", "🌊": "acqua",
}

# Il LOCK DI LUCE del set (skill rumblingstone-art-direction §4): dichiarato una
# volta e riusato per tutte le mappe di un modulo. Luci che arrivano da parti
# diverse nella stessa città sono la prima cosa che l'occhio nota.
LUCE_AZIMUT = 315.0     # da nord-ovest
LUCE_ELEVAZIONE = 55.0  # sole alto di tardo pomeriggio


def altezza(simbolo: str) -> float:
    if simbolo in PIATTI:
        return 0.0
    if simbolo in ALTEZZE:
        return ALTEZZE[simbolo]
    voce = rms.SYMBOLS.get(simbolo, {})
    if voce.get("mode") == "unit":
        return 0.0  # i token non entrano nel render, ma non devono farlo fallire
    return ALTEZZA_ICONA_DEFAULT if voce else 0.0


def colore(simbolo: str) -> str:
    """Il colore lo dà il renderer SVG: una sola fonte di verità per due catene.

    È il difetto raccontato in PROCEDURA.md §7 — un generatore andato alla deriva
    dai file che generava — evitato per costruzione invece che per disciplina.
    """
    return rms.SYMBOLS.get(simbolo, {}).get("fill", "#b3c489")


# ── Dalla griglia ai solidi ──────────────────────────────────────────────────


def unisci(griglia: list[list[str]]) -> list[tuple[str, int, int, int, int]]:
    """Fonde le celle uguali in rettangoli: `(simbolo, x, y, larghezza, altezza)`.

    Una griglia 64×46 sono 2.944 cubi; unendo prima le corse orizzontali e poi le
    corse verticali identiche si scende di un ordine di grandezza, e Blender
    apre la scena invece di masticarla. È la stessa idea del *greedy meshing* dei
    voxel, nella sua forma più semplice — che qui basta perché le mappe sono
    fatte di rettangoli, non di nuvole di punti.
    """
    corse: list[tuple[str, int, int, int, int]] = []
    for y, riga in enumerate(griglia):
        x = 0
        while x < len(riga):
            simbolo = riga[x]
            fine = x
            while fine + 1 < len(riga) and riga[fine + 1] == simbolo:
                fine += 1
            corse.append((simbolo, x, y, fine - x + 1, 1))
            x = fine + 1

    # seconda passata: due corse identiche e allineate, su righe adiacenti, sono
    # un rettangolo solo
    per_riga: dict[int, list] = {}
    for corsa in corse:
        per_riga.setdefault(corsa[2], []).append(corsa)

    fusi: list[tuple[str, int, int, int, int]] = []
    consumate: set[tuple[str, int, int, int, int]] = set()
    for corsa in corse:
        if corsa in consumate:
            continue
        simbolo, x, y, larghezza, _ = corsa
        alta = 1
        while True:
            candidata = (simbolo, x, y + alta, larghezza, 1)
            if candidata in per_riga.get(y + alta, []) and candidata not in consumate:
                consumate.add(candidata)
                alta += 1
            else:
                break
        fusi.append((simbolo, x, y, larghezza, alta))
    return fusi


def pianta_sola(spec: dict, con_insidie: bool) -> dict:
    """Lo spec senza il livello tattico: resta la **pianta**, che è ciò che si estrude.

    Le **unità** non sono geometria: sono token, e appartengono al VTT. Le
    **insidie** sono note del DM — la mappa in versione giocatore del Lotto 7 le
    toglie per la stessa ragione: un'illustrazione con sopra i segnalini non è
    un'illustrazione.

    Non è solo una questione di gusto: un token in mezzo a una riga **spezza le
    corse** e impedisce di fondere i rettangoli, quindi togliere il livello
    tattico rende anche la scena molto più leggera.
    """
    pianta = dict(spec)
    pianta["units"] = []
    if not con_insidie:
        pianta["hazards"] = []
    return pianta


def piano_di_scena(spec: dict, args) -> dict:
    """Il contratto fra questo driver e lo script che gira dentro Blender.

    Sta in un file perché il driver è stdlib e Blender ha il suo Python: l'unico
    canale onesto fra i due è un JSON su disco, che si può anche leggere quando
    qualcosa non torna.
    """
    colonne, righe = cmj.validate(spec)
    griglia = cmj.paint(pianta_sola(spec, args.con_insidie), colonne, righe)
    scala = float(spec.get("scale_m_per_square", 1.5))

    # Ogni cella diventa un solido, **terreno di base compreso**: non c'è un piano
    # di appoggio sotto. Con un piano, una voragine o uno specchio d'acqua
    # resterebbero coperti dal piano stesso e il passo di profondità li leggerebbe
    # piatti — cioè proprio l'informazione per cui il passo esiste.
    solidi = []
    for simbolo, x, y, larghezza, profondita in unisci(griglia):
        h = altezza(simbolo)
        solidi.append(
            {
                "simbolo": simbolo,
                "x_m": x * scala,
                "y_m": y * scala,
                "larghezza_m": larghezza * scala,
                "profondita_m": profondita * scala,
                "altezza_m": h,
                "colore": colore(simbolo),
                "texture": TEXTURE.get(simbolo),
            }
        )

    larghezza_m = colonne * scala
    profondita_m = righe * scala
    lato_lungo = max(larghezza_m, profondita_m)

    return {
        "piano_version": "1.0",
        "generato_da": "scripts/render_map_blender.py — non modificare a mano",
        "titolo": spec.get("title", "mappa"),
        "slug": rms.nome_mappa(spec.get("title", "mappa")),
        "scala_m_per_quadretto": scala,
        "griglia": [colonne, righe],
        "spessore_lastra_m": 0.02,
        "terreno_base": {
            "simbolo": spec.get("base_terrain", "🟩"),
            "colore": colore(spec.get("base_terrain", "🟩")),
            "larghezza_m": larghezza_m,
            "profondita_m": profondita_m,
        },
        "solidi": solidi,
        "camera": {
            "tipo": args.vista,
            "scala_orto_m": lato_lungo * 1.05,
            "altezza_m": lato_lungo,
        },
        "luce": {
            "azimut": args.luce_azimut,
            "elevazione": args.luce_elevazione,
            "intensita": 3.0,
            "nota": "lock di luce del set: si cambia per TUTTE le mappe del modulo, o per nessuna",
        },
        "render": {
            "larghezza_px": args.larghezza,
            "altezza_px": int(args.larghezza * profondita_m / larghezza_m) if larghezza_m else args.larghezza,
            "campioni": args.campioni,
            "profondita": bool(args.profondita),
        },
        "texture_dir": str(TEXTURE_DIR),
        "uscita": None,  # riempita da main()
    }


# ── CLI ──────────────────────────────────────────────────────────────────────


def costruisci_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="render_map_blender.py",
        description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("mappa", type=Path, help="Il JSON della mappa (contratto tactical_map).")
    p.add_argument("-o", "--out", type=Path, default=None,
                   help="PNG di uscita (default: <cartella>/rendered/blender/<slug>.png).")
    p.add_argument("--vista", choices=["orto", "tre-quarti"], default="orto",
                   help="orto = ortografica dall'alto (default) - tre-quarti = prospettica.")
    p.add_argument("--profondita", action="store_true",
                   help="Rende il passo di PROFONDITÀ invece della veduta: è l'input di ControlNet depth.")
    p.add_argument("--larghezza", type=int, default=2048, metavar="PX",
                   help="Larghezza del render in pixel (default: 2048).")
    p.add_argument("--campioni", type=int, default=64,
                   help="Campioni per pixel (default: 64).")
    p.add_argument("--luce-azimut", type=float, default=LUCE_AZIMUT,
                   help=f"Direzione della luce in gradi (default: {LUCE_AZIMUT}, da nord-ovest).")
    p.add_argument("--luce-elevazione", type=float, default=LUCE_ELEVAZIONE,
                   help=f"Altezza della luce in gradi (default: {LUCE_ELEVAZIONE}).")
    p.add_argument("--con-insidie", action="store_true",
                   help="Tiene le insidie nella pianta (default: fuori, sono note del DM).")
    p.add_argument("--blender", default="blender", help="Comando di Blender, se non è nel PATH.")
    p.add_argument("--piano-solo", action="store_true",
                   help="Scrive il piano di scena ed esce: nessun Blender, nessun render.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = costruisci_parser().parse_args(argv)

    if not args.mappa.is_file():
        print(f"✗ mappa non trovata: {args.mappa}", file=sys.stderr)
        return 2

    try:
        spec = cmj.normalize_units(json.loads(args.mappa.read_text(encoding="utf-8")))
        piano = piano_di_scena(spec, args)
    except (json.JSONDecodeError, ValueError, KeyError, SystemExit) as e:
        print(f"✗ JSON di mappa non valido: {e}", file=sys.stderr)
        return 1

    suffisso = "-depth" if args.profondita else ""
    uscita = args.out or (args.mappa.parent / "rendered" / "blender" / f"{piano['slug']}{suffisso}.png")
    piano["uscita"] = str(uscita.resolve())

    percorso_piano = uscita.parent / f"{piano['slug']}.piano.json"
    uscita.parent.mkdir(parents=True, exist_ok=True)
    percorso_piano.write_text(json.dumps(piano, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    solidi = len(piano["solidi"])
    celle = piano["griglia"][0] * piano["griglia"][1]
    print(f"piano: {solidi} solidi da {celle} celle ({100 * solidi // celle}%) → {percorso_piano}")

    if args.piano_solo:
        return 0

    if not shutil.which(args.blender):
        print(INSTALLA, file=sys.stderr)
        return 1

    comando = [args.blender, "-b", "-noaudio", "-P", str(COSTRUTTORE), "--", "--piano", str(percorso_piano)]
    esito = subprocess.run(comando, capture_output=True, text=True)
    if esito.returncode != 0:
        print(esito.stdout[-2000:], file=sys.stderr)
        print(esito.stderr[-2000:], file=sys.stderr)
        print(f"✗ Blender è uscito con {esito.returncode}", file=sys.stderr)
        return 1
    if not uscita.exists():
        print(f"✗ Blender è finito ma {uscita} non c'è. Log:\n{esito.stdout[-1500:]}", file=sys.stderr)
        return 1

    print(f"✓ {uscita} ({uscita.stat().st_size // 1024} KiB)")
    if args.profondita:
        print(
            "Ora si dà a ControlNet depth in ComfyUI (scripts/comfyui-local/): "
            "l'illustrazione eredita la pianta esatta invece di inventarsela."
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
