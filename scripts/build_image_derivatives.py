#!/usr/bin/env python3
"""build_image_derivatives.py — le versioni da impaginazione delle immagini raster.

I master generati escono a 1700-2800 px e pesano 5-8 MB l'uno: giusto per l'archivio
e per una stampa vera, **sbagliato dentro un booklet**. Venti immagini così fanno un
PDF da 120 MB che non si apre sul telefono e un HTML che non si manda per posta.

Questo tool produce accanto ai master una cartella `web/` con le stesse immagini
ridimensionate al lato lungo utile e ricompresse. **I master non si toccano**: la
derivata è un artefatto, e si rifà quando serve (ADR-0003).

Regola di dimensionamento — viene dalla destinazione, non da un numero a caso:
  · ritratti e copertina  → 1400 px sul lato lungo (a 300 dpi è una mezza pagina A4)
  · tavole d'ambiente     → 1800 px (occupano la larghezza delle due colonne)
  · spot quadrati         →  900 px (stanno in una colonna)

Rigenera con:
    python3 scripts/build_image_derivatives.py <cartella>
    python3 scripts/build_image_derivatives.py <cartella> --max 1600 --quality 82

Formati dei master accettati: **PNG e WebP**. Il WebP c'è perché le immagini della
campagna (ARC-07) sono nate così, ed è il formato che la catena di stampa gestisce
peggio: Typst lo decodifica e ricomprime, mentre il JPEG lo incorpora così com'è.
Una derivata JPEG serve quindi ai WebP **più** che ai PNG.

Dipendenze: stdlib + **Pillow**. Se manca, lo script dice come installarlo ed esce
pulito: i booklet continuano a usare i segnaposto vettoriali.
Exit code: 0 = ok · 1 = Pillow assente · 2 = cartella mancante.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

INSTALLA = """\
Serve Pillow per ridimensionare le immagini:

    pip install pillow          (oppure: sudo dnf install python3-pillow)

Senza, i master restano dove sono e i booklet usano i segnaposto vettoriali.
"""

# Lato lungo per famiglia di immagine, dedotto dal prefisso del nome file.
LATI = {
    "tavola-": 1800,
    "spot-": 900,
}
DEFAULT = 1400


def lato_per(nome: str, default: int) -> int:
    for prefisso, px in LATI.items():
        if nome.startswith(prefisso):
            return px
    return default


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cartella", help="cartella dei master (PNG o WebP)")
    ap.add_argument("--max", type=int, default=DEFAULT,
                    help=f"lato lungo per ritratti e copertina (default {DEFAULT})")
    ap.add_argument("--quality", type=int, default=88, help="qualità JPEG (default 88)")
    args = ap.parse_args()

    src = Path(args.cartella)
    if not src.is_dir():
        print(f"✗ cartella non trovata: {src}", file=sys.stderr)
        return 2

    try:
        from PIL import Image, PngImagePlugin
    except ImportError:
        print(INSTALLA, file=sys.stderr)
        return 1

    # I PNG generati portano un manifesto di provenienza C2PA firmato, che è un
    # chunk di testo da decine di KB. Il limite prudenziale di Pillow (1 MB
    # decompresso) lo rifiuta e l'apertura fallisce: qui lo alziamo perché quel
    # chunk è esattamente ciò che vogliamo conservare, non un allegato sospetto.
    PngImagePlugin.MAX_TEXT_CHUNK = 64 * 1024 * 1024

    out = src / "web"
    out.mkdir(exist_ok=True)
    tot_prima = tot_dopo = 0
    n = 0
    masters = sorted(f for f in src.iterdir()
                     if f.is_file() and f.suffix.lower() in (".png", ".webp"))
    for master in masters:
        lato = lato_per(master.stem, args.max)
        with Image.open(master) as im:
            im = im.convert("RGB")
            if max(im.size) > lato:
                scala = lato / max(im.size)
                im = im.resize((round(im.width * scala), round(im.height * scala)),
                               Image.LANCZOS)
            # JPEG e non WebP: Typst incorpora il JPEG nel PDF **così com'è**
            # (DCTDecode), mentre un WebP lo deve decodificare e ricomprimere —
            # e un fascicolo di sei ritratti passava da 300 KB a 10 MB.
            dest = out / f"{master.stem}.jpg"
            im.save(dest, "JPEG", quality=args.quality, optimize=True, progressive=True)
        tot_prima += master.stat().st_size
        tot_dopo += dest.stat().st_size
        n += 1

    if not n:
        print(f"  ⚠ nessun master PNG o WebP in {src}")
        return 0
    print(f"✓ build_image_derivatives: {n} immagini → {out.relative_to(Path.cwd()) if out.is_relative_to(Path.cwd()) else out}"
          f"  ({tot_prima // 1024 // 1024} MB → {tot_dopo // 1024 // 1024} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
