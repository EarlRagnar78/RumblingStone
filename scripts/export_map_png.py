#!/usr/bin/env python3
"""
export_map_png.py — rasterize a rendered map SVG to a hi-res PNG.

Use for printing, VTT import, or as the structural input of the optional
ComfyUI "hero map" pass (see skill `rumblingstone-mapmaking`,
`references/hero-map-comfyui.md`).

The PNG is a LOCAL artifact: do not commit it — the deterministic SVG in
`rendered/` stays the canonical generated file (validate_maps.py).

Rendering is delegated to a headless Chromium/Chrome found on the machine
(no Python dependencies). Pass --browser to point at a specific binary.

Usage:
    python3 scripts/export_map_png.py rendered/<mappa>.svg
    python3 scripts/export_map_png.py <mappa>.svg --scale 3 -o out.png
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

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


def find_browser(explicit: str | None) -> str:
    for cand in ([explicit] if explicit else []) + BROWSER_CANDIDATES:
        if not cand:
            continue
        path = shutil.which(cand) or (cand if Path(cand).exists() else None)
        if path:
            return path
    print("ERRORE: nessun Chromium/Chrome trovato. Installa un browser o "
          "passa --browser /percorso/chrome (o env MAP_PNG_BROWSER).",
          file=sys.stderr)
    raise SystemExit(1)


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
    ap.add_argument("--browser", help="binario Chromium/Chrome da usare")
    args = ap.parse_args()

    svg = Path(args.svg).resolve()
    if not svg.exists():
        print(f"ERRORE: {svg} non esiste", file=sys.stderr)
        return 1
    out = Path(args.out) if args.out else svg.with_suffix(".png")
    w, h = svg_size(svg)
    sw, sh = round(w * args.scale), round(h * args.scale)

    browser = find_browser(args.browser)
    cmd = [
        browser, "--headless", "--no-sandbox", "--disable-gpu",
        "--hide-scrollbars", f"--force-device-scale-factor={args.scale}",
        f"--screenshot={out}", f"--window-size={w},{h}", svg.as_uri(),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not out.exists():
        print(res.stderr.strip() or "screenshot fallito", file=sys.stderr)
        return 1
    print(f"✓ {out}  ({sw}×{sh} px, scala {args.scale}x — artefatto locale, non committare)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
