#!/usr/bin/env python3
"""
export_map_png.py — rasterize a rendered map SVG to a hi-res PNG.

Use for printing, VTT import, or as the structural input of the optional
ComfyUI "hero map" pass (see skill `rumblingstone-mapmaking`,
`references/hero-map-comfyui.md`).

The PNG is a LOCAL artifact: do not commit it — the deterministic SVG in
`rendered/` stays the canonical generated file (validate_maps.py).

Rendering is delegated to an external rasterizer found on the machine (no
Python dependencies), in this order:

  1. **Inkscape** (`--renderer inkscape`) — an SVG renderer proper: it honours
     the parts of the spec a browser treats as web page (markers, patterns,
     `text-anchor` on rotated labels) and takes the output size directly,
     without a viewport. Preferred when present.
  2. **Chromium/Chrome headless** (`--renderer browser`) — the historical
     backend, kept because every machine that builds the booklets already
     has it.

`--renderer auto` (default) picks Inkscape if installed, the browser
otherwise. If neither is there the script says which binary to install and
exits non-zero without leaving a half-written file (ADR-0012 §degradazione).

Usage:
    python3 scripts/export_map_png.py rendered/<mappa>.svg
    python3 scripts/export_map_png.py <mappa>.svg --scale 3 -o out.png
    python3 scripts/export_map_png.py <mappa>.svg --renderer browser
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import struct
import subprocess
import sys
import zlib
from pathlib import Path

INKSCAPE_CANDIDATES = [
    os.environ.get("MAP_PNG_INKSCAPE", ""),
    "inkscape",
    "/Applications/Inkscape.app/Contents/MacOS/inkscape",
    r"C:\Program Files\Inkscape\bin\inkscape.exe",
]

BROWSER_CANDIDATES = [
    os.environ.get("MAP_PNG_BROWSER", ""),
    "/opt/pw-browsers/chromium",
    "chromium",
    "chromium-browser",
    "google-chrome",
    "google-chrome-stable",
    "chrome",
    "msedge",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]


def find_binary(explicit: str | None, candidates: list[str]) -> str | None:
    """Primo binario esistente fra quello esplicito e i candidati. None se nessuno."""
    for cand in ([explicit] if explicit else []) + candidates:
        if not cand:
            continue
        path = shutil.which(cand) or (cand if Path(cand).exists() else None)
        if path:
            return path
    return None


def find_browser(explicit: str | None) -> str:
    path = find_binary(explicit, BROWSER_CANDIDATES)
    if path:
        return path
    print("ERRORE: nessun Chromium/Chrome trovato. Installa un browser o "
          "passa --browser /percorso/chrome (o env MAP_PNG_BROWSER).",
          file=sys.stderr)
    raise SystemExit(1)


def find_inkscape(explicit: str | None) -> str:
    path = find_binary(explicit, INKSCAPE_CANDIDATES)
    if path:
        return path
    print("ERRORE: Inkscape non trovato. Installalo (dnf/apt install inkscape, "
          "brew install --cask inkscape) oppure passa --inkscape /percorso/inkscape "
          "(o env MAP_PNG_INKSCAPE). Con --renderer browser usa invece Chromium.",
          file=sys.stderr)
    raise SystemExit(1)


def pick_renderer(mode: str, inkscape: str | None, browser: str | None) -> tuple[str, str]:
    """(motore, binario). In 'auto' vince Inkscape se c'e', altrimenti il browser."""
    if mode == "inkscape":
        return "inkscape", find_inkscape(inkscape)
    if mode == "browser":
        return "browser", find_browser(browser)
    found = find_binary(inkscape, INKSCAPE_CANDIDATES)
    if found:
        return "inkscape", found
    found = find_binary(browser, BROWSER_CANDIDATES)
    if found:
        return "browser", found
    print("ERRORE: nessun rasterizzatore trovato. Installa Inkscape "
          "(dnf/apt install inkscape) oppure un Chromium/Chrome headless.",
          file=sys.stderr)
    raise SystemExit(1)


def run_inkscape(binary: str, svg: Path, out: Path, sw: int, sh: int) -> int:
    cmd = [
        binary, "--export-type=png", f"--export-filename={out}",
        f"--export-width={sw}", f"--export-height={sh}", str(svg),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not out.exists():
        print(res.stderr.strip() or "export Inkscape fallito", file=sys.stderr)
        return 1
    return 0


#: Il Chromium headless «nuovo» toglie alla finestra una fascia per la cornice
#: che non disegna (88 px con Chromium 140): con --window-size alto quanto
#: l'SVG, il fondo della mappa (la legenda) usciva tagliato. La finestra si apre
#: più alta di questo margine e il PNG si riporta all'altezza dell'SVG.
MARGINE_FINESTRA = 240


def taglia_png(path: Path, altezza: int) -> None:
    """Tiene le prime `altezza` righe di un PNG non interlacciato, con la sola
    libreria standard: i filtri di una riga guardano solo la riga sopra, quindi
    togliere righe dal fondo lascia valide quelle che restano."""
    dati = path.read_bytes()
    pezzi, i = [], 8
    while i < len(dati):
        n = struct.unpack(">I", dati[i:i + 4])[0]
        pezzi.append((dati[i + 4:i + 8], dati[i + 8:i + 8 + n]))
        i += 12 + n
    ihdr = pezzi[0][1]
    larg, alt, prof, colore, _, _, interl = struct.unpack(">IIBBBBB", ihdr)
    if interl or alt <= altezza:
        return
    canali = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[colore]
    riga = 1 + (larg * canali * prof + 7) // 8
    grezzi = zlib.decompress(b"".join(d for t, d in pezzi if t == b"IDAT"))
    nuovo_ihdr = struct.pack(">IIBBBBB", larg, altezza, prof, colore, *ihdr[10:13])

    def pezzo(tipo: bytes, d: bytes) -> bytes:
        return struct.pack(">I", len(d)) + tipo + d + struct.pack(">I", zlib.crc32(tipo + d))
    corpo = [pezzo(b"IHDR", nuovo_ihdr)]
    corpo += [pezzo(t, d) for t, d in pezzi[1:] if t not in (b"IDAT", b"IEND")]
    corpo += [pezzo(b"IDAT", zlib.compress(grezzi[:riga * altezza], 9)), pezzo(b"IEND", b"")]
    path.write_bytes(dati[:8] + b"".join(corpo))


def run_browser(binary: str, svg: Path, out: Path, w: int, h: int, scale: float) -> int:
    cmd = [
        binary, "--headless", "--no-sandbox", "--disable-gpu",
        "--hide-scrollbars", f"--force-device-scale-factor={scale}",
        f"--screenshot={out}", f"--window-size={w},{h + MARGINE_FINESTRA}", svg.as_uri(),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not out.exists():
        print(res.stderr.strip() or "screenshot fallito", file=sys.stderr)
        return 1
    taglia_png(out, round(h * scale))
    return 0


def svg_size(svg_path: Path) -> tuple[int, int]:
    head = svg_path.read_text(encoding="utf-8")[:600]
    w = re.search(r'width="(\d+)"', head)
    h = re.search(r'height="(\d+)"', head)
    if not (w and h):
        print(f"ERRORE: width/height non trovati in {svg_path}", file=sys.stderr)
        raise SystemExit(1)
    return int(w.group(1)), int(h.group(1))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", help="SVG generato da render_map_svg.py")
    ap.add_argument("-o", "--out", help="PNG di destinazione (default: accanto all'SVG)")
    ap.add_argument("--scale", type=float, default=2.0,
                    help="fattore di scala (default 2.0 ≈ 300 dpi al tavolo; 3 per A3)")
    ap.add_argument("--renderer", choices=("auto", "inkscape", "browser"),
                    default="auto",
                    help="motore di rasterizzazione (default: auto — Inkscape se c'e')")
    ap.add_argument("--browser", help="binario Chromium/Chrome da usare")
    ap.add_argument("--inkscape", help="binario Inkscape da usare")
    args = ap.parse_args()

    svg = Path(args.svg).resolve()
    if not svg.exists():
        print(f"ERRORE: {svg} non esiste", file=sys.stderr)
        return 1
    out = Path(args.out) if args.out else svg.with_suffix(".png")
    w, h = svg_size(svg)
    sw, sh = round(w * args.scale), round(h * args.scale)

    engine, binary = pick_renderer(args.renderer, args.inkscape, args.browser)
    if engine == "inkscape":
        rc = run_inkscape(binary, svg, out, sw, sh)
    else:
        rc = run_browser(binary, svg, out, w, h, args.scale)
    if rc != 0:
        return rc
    print(f"✓ {out}  ({sw}×{sh} px, scala {args.scale}x, motore {engine} — "
          f"artefatto locale, non committare)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
