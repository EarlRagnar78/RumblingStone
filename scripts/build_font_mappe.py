#!/usr/bin/env python3
"""
build_font_mappe.py — i sottoinsiemi dei font dei volumi che le mappe incorporano
(ADR-0085).

Le mappe chiedevano Georgia, che su Linux e in CI diventa DejaVu Serif: la
stessa mappa cambiava faccia da una macchina all'altra, e non aveva quella dei
volumi. Questo script ricava da `scripts/fonts/` (OFL 1.1) due woff2 piccoli,
a peso fisso e con i soli caratteri dell'italiano e la punteggiatura delle
mappe, e li scrive in `scripts/fonts/mappe/`: EB Garamond regolare per il
testo, Cinzel grassetto per titoli ed etichette in grassetto.

Misurato il 2026-10-08: i tre font variabili (anche il corsivo) pesavano 96 KB,
128 KB in base64 per ogni SVG; fissati i pesi e tolto il corsivo, 32 KB. Il renderer li incorpora in base64 in ogni SVG e
resta in libreria standard: fonttools serve solo qui.

    python3 scripts/build_font_mappe.py           # rigenera i due woff2 e copertura.json
    python3 scripts/build_font_mappe.py --check   # esce 1 se manca un file o la copertura

Esce con 2 se fonttools manca (`pip install -r requirements-dev.txt`).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent
FONTS = RADICE / "fonts"
USCITA = FONTS / "mappe"
COPERTURA = USCITA / "copertura.json"

# latino di base e Latin-1 (l'italiano e i nomi di Faerûn), lineette e
# virgolette tipografiche, frecce, il meno e il circa delle quote (×, ° e ½
# stanno gia' nel Latin-1)
UNICODE = ("U+0020-007E,U+00A0-00FF,U+0152-0153,U+2013-2014,U+2018-201E,"
           "U+2022,U+2026,U+2190-2193,U+2212,U+2248")

FONT = (
    # (sorgente variabile, nome del file, famiglia, peso fissato)
    ("EBGaramond[wght].ttf", "ebgaramond-400.woff2", "EB Garamond", 400),
    ("Cinzel[wght].ttf", "cinzel-700.woff2", "Cinzel", 700),
)


def _codici() -> list[int]:
    out = []
    for parte in UNICODE.split(","):
        a, _, b = parte[2:].partition("-")
        out += range(int(a, 16), int(b or a, 16) + 1)
    return out


def costruisci() -> int:
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
        from fontTools.varLib import instancer
    except ImportError:
        print("✗ build_font_mappe ha bisogno di fonttools: pip install -r requirements-dev.txt",
              file=sys.stderr)
        return 2
    import tempfile
    USCITA.mkdir(exist_ok=True)
    copertura = {}
    for sorgente, nome, famiglia, peso in FONT:
        dest = USCITA / nome
        with tempfile.TemporaryDirectory() as tmp:
            fisso = Path(tmp) / "fisso.ttf"
            fonte = TTFont(FONTS / sorgente, recalcTimestamp=False)
            istanza = instancer.instantiateVariableFont(fonte, {"wght": peso})
            istanza.recalcTimestamp = False
            istanza.save(fisso)
            subset.main([str(fisso), f"--unicodes={UNICODE}", "--flavor=woff2",
                         f"--output-file={dest}", "--layout-features=kern,liga",
                         "--no-hinting", "--desubroutinize", "--drop-tables+=DSIG",
                         "--name-IDs=1,2,3,4,6", "--no-recalc-timestamp"])
        ttf = TTFont(dest)
        cmap = ttf.getBestCmap()
        em = ttf["head"].unitsPerEm
        hmtx = ttf["hmtx"].metrics
        avanzi = {str(c): round(hmtx[cmap[c]][0] / em, 4) for c in _codici() if c in cmap}
        copertura[nome] = {"famiglia": famiglia, "peso": peso, "sorgente": sorgente,
                           "licenza": f"OFL 1.1, scripts/fonts/OFL-{sorgente.split('[')[0].split('-')[0]}.txt",
                           "byte": dest.stat().st_size,
                           "caratteri": sorted(c for c in _codici() if c in cmap),
                           # larghezza di ogni carattere in em: il renderer misura
                           # i titoli senza fonttools e li stringe se non entrano
                           "avanzi": avanzi}
        print(f"✓ {nome}: {dest.stat().st_size} byte, {len(copertura[nome]['caratteri'])} caratteri")
    COPERTURA.write_text(json.dumps(copertura, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


def controlla() -> int:
    if not COPERTURA.exists():
        print(f"✗ manca {COPERTURA.relative_to(RADICE.parent)}: python3 scripts/build_font_mappe.py")
        return 1
    dati = json.loads(COPERTURA.read_text(encoding="utf-8"))
    errori = [n for n in (f[1] for f in FONT) if n not in dati or not (USCITA / n).exists()]
    errori += [f"{n} (byte diversi da copertura.json)" for n in dati
               if (USCITA / n).exists() and (USCITA / n).stat().st_size != dati[n]["byte"]]
    for e in errori:
        print(f"✗ build_font_mappe: {e}")
    if not errori:
        print(f"✓ build_font_mappe: {len(dati)} font per le mappe, "
              f"{sum(d['byte'] for d in dati.values())} byte")
    return 1 if errori else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--check", action="store_true", help="verifica che i file ci siano e combacino")
    args = ap.parse_args(argv)
    return controlla() if args.check else costruisci()


if __name__ == "__main__":
    sys.exit(main())
