#!/usr/bin/env python3
"""build_chapter_marks.py — i fregi di capitolo, in SVG, disegnati da zero.

Un manuale d'avventura pubblicato apre ogni capitolo con un **segno**: un piccolo
emblema che dice al lettore dov'è prima ancora che legga il titolo. Questo
generatore produce quel segno per due serie **distinte e non intercambiabili**:

  · `campagna` — un fregio per arco (`00_`–`09_`), sul tema dell'arco;
  · `drappo`   — un fregio per capitolo del modulo autoconclusivo.

I disegni sono **originali**: primitive geometriche (cerchi, archi, polilinee)
composte qui dentro. Nessun asset di terzi, nessuna licenza da citare — per
questo il generatore esiste invece di prendere icone altrove.

Ogni fregio è un medaglione circolare monocromatico, leggibile a **14 mm**:
è la misura a cui finisce stampato accanto al titolo di capitolo.

Rigenera con:
    python3 scripts/build_chapter_marks.py --serie drappo -o <cartella>
    python3 scripts/build_chapter_marks.py --serie campagna -o <cartella>
    python3 scripts/build_chapter_marks.py --all           # entrambe, nei posti canonici
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INK = "#6b4f2a"          # la seppia dei booklet: un solo inchiostro, come in stampa
BOX = 96                 # viewBox quadrato; il centro è (48, 48)
C = BOX / 2

# Destinazioni canoniche di --all
DEST = {
    "drappo": "STANDALONE-Il-Drappo-di-Tarsilia/ALLEGATI/tavole/fregi",
    "campagna": "docs/assets/fregi",
}


# ── primitive ────────────────────────────────────────────────────────────────

def ring() -> str:
    """La cornice comune a tutti i fregi: è ciò che li rende una serie."""
    return (
        f'<circle cx="{C}" cy="{C}" r="45" fill="none" stroke="{INK}" stroke-width="1.6"/>'
        f'<circle cx="{C}" cy="{C}" r="41" fill="none" stroke="{INK}" stroke-width="0.8"/>'
    )


def p(d: str, w: float = 3.0, fill: str = "none") -> str:
    return (
        f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{w}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
    )


def circ(cx: float, cy: float, r: float, w: float = 3.0, fill: str = "none") -> str:
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="{w}"/>'


def line(x1: float, y1: float, x2: float, y2: float, w: float = 3.0) -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" '
        f'stroke-width="{w}" stroke-linecap="round"/>'
    )


# ── i glifi ──────────────────────────────────────────────────────────────────
# Ognuno disegna dentro il riquadro 96×96, lasciando libero il bordo per il ring.

GLIFI = {
    # — serie del Drappo —
    "ruota": lambda: circ(C, C, 26, 2.6) + circ(C, C, 12, 2.2)
    + line(C, 22, C, 36) + line(C, 60, C, 74) + line(22, C, 36, C) + line(60, C, 74, C),
    "scudo": lambda: p("M30 28 H66 V52 Q66 68 48 74 Q30 68 30 52 Z", 2.8)
    + line(48, 28, 48, 74, 2.2),
    "ferro": lambda: p("M32 68 Q26 40 48 28 Q70 40 64 68", 4.0)
    + circ(34, 62, 2.2, 1.6, INK) + circ(62, 62, 2.2, 1.6, INK)
    + circ(33, 50, 2.2, 1.6, INK) + circ(63, 50, 2.2, 1.6, INK),
    "sorte": lambda: p("M34 44 H62 L58 72 H38 Z", 2.8) + line(31, 44, 65, 44, 2.8)
    + circ(48, 30, 6, 2.6),
    # La cena: una coppa sola, larga e frontale. Due coppe affiancate a 14 mm
    # diventano due stanghette — provato, sembrava un «77».
    "coppa": lambda: p("M30 30 H66 Q66 52 48 56 Q30 52 30 30 Z", 2.8)
    + line(48, 56, 48, 68, 3.0) + p("M34 72 Q48 66 62 72", 3.0)
    + line(30, 38, 66, 38, 1.8),
    # Lo Stacco: il canapo teso fra due paletti. La fune «libera» non si leggeva.
    # Lo Stacco: il pennone del traguardo con la bandierina a punta, e la pista
    # che passa sotto. Il canapo «disegnato» dava una M: due tentativi buttati,
    # e la lezione è che a 14 mm vince la sagoma, non la fedeltà all'oggetto.
    "traguardo": lambda: line(34, 20, 34, 70, 3.4)
    + p("M34 24 L68 34 L34 44 Z", 2.8)
    + p("M20 70 Q48 78 76 70", 2.6) + line(28, 70, 40, 70, 3.0),
    "chiave": lambda: circ(36, 42, 9, 2.8) + p("M42 48 L70 70 M62 62 L68 56 M56 56 L62 50", 2.8),
    "candela": lambda: p("M40 44 H56 V70 H40 Z", 2.6) + line(36, 70, 60, 70, 2.6)
    + p("M48 42 Q42 34 48 24 Q54 34 48 42", 2.4),
    "maschera": lambda: p("M24 40 Q48 30 72 40 Q68 60 48 62 Q28 60 24 40 Z", 2.8)
    + circ(38, 45, 3.2, 2.0, INK) + circ(58, 45, 3.2, 2.0, INK),
    "lanterna": lambda: p("M38 34 H58 L62 44 V66 H34 V44 Z", 2.6)
    + p("M42 26 Q48 20 54 26", 2.4) + line(48, 26, 48, 34, 2.0)
    + circ(48, 54, 7, 2.2),
    "cassetta": lambda: p("M26 44 H70 V70 H26 Z", 2.8)
    + p("M26 44 Q48 30 70 44", 2.8) + line(26, 54, 70, 54, 2.0)
    + p("M44 52 H52 V60 H44 Z", 2.2),
    # Elmo a barile: cupola, feritoia, base. Senza la feritoia sembrava un arco.
    "elmo": lambda: p("M30 48 Q30 26 48 26 Q66 26 66 48 V66 Q48 72 30 66 Z", 2.8)
    + p("M34 44 H62", 4.5) + line(48, 50, 48, 64, 2.0)
    + circ(40, 57, 1.8, 1.4, INK) + circ(56, 57, 1.8, 1.4, INK),
    # Spade incrociate con elsa e pomo: due rette sole facevano una X qualunque.
    "spade": lambda: p("M26 74 L62 28 M34 28 L70 74", 3.4)
    + line(24, 58, 42, 76, 2.6) + line(54, 76, 72, 58, 2.6)
    + p("M60 24 L66 30", 3.4) + p("M30 24 L36 30", 3.4),
    "clessidra": lambda: p("M32 26 H64 L48 48 L64 70 H32 L48 48 Z", 2.8)
    + line(28, 26, 68, 26, 3.0) + line(28, 70, 68, 70, 3.0),
    "sigillo": lambda: circ(48, 42, 15, 2.8) + circ(48, 42, 8, 1.8)
    + p("M38 56 L34 76 L48 68 L62 76 L58 56", 2.6),
    "mappa": lambda: p("M22 32 L40 26 L58 34 L74 28 V64 L58 70 L40 62 L22 68 Z", 2.6)
    + line(40, 26, 40, 62, 1.8) + line(58, 34, 58, 70, 1.8),
    "libro": lambda: p("M24 30 Q36 24 48 30 Q60 24 72 30 V68 Q60 62 48 68 Q36 62 24 68 Z", 2.8)
    + line(48, 30, 48, 68, 2.2),
    "foglio": lambda: p("M32 24 H58 L66 34 V72 H32 Z", 2.8) + p("M58 24 V34 H66", 2.0)
    + line(39, 46, 59, 46, 2.0) + line(39, 54, 59, 54, 2.0) + line(39, 62, 51, 62, 2.0),
    "lettera": lambda: p("M24 34 H72 V66 H24 Z", 2.8) + p("M24 34 L48 52 L72 34", 2.4),
    # — serie della campagna —
    "mano": lambda: p("M36 70 V46 Q36 40 41 40 Q46 40 46 46 V30 Q46 24 51 24 Q56 24 56 30 V44"
                      " Q62 40 66 44 Q70 48 66 56 L60 70 Z", 2.8),
    # Piccone: il becco va CURVATO in giù alle estremità, se no è una T.
    "piccone": lambda: p("M20 46 Q30 26 48 30 Q66 26 76 46", 3.4)
    + p("M20 46 Q28 36 34 34 M76 46 Q68 36 62 34", 2.4)
    + line(48, 30, 48, 76, 3.4),
    "fungo": lambda: p("M22 48 Q26 28 48 28 Q70 28 74 48 Z", 2.8)
    + p("M40 48 V64 Q48 72 56 64 V48", 2.6)
    + circ(36, 40, 3, 1.8, INK) + circ(56, 38, 3.5, 1.8, INK),
    "torre": lambda: p("M32 38 H64 V74 H32 Z", 2.8)
    + p("M28 38 V28 H36 V34 H44 V28 H52 V34 H60 V28 H68 V38", 2.6)
    + p("M42 74 V56 Q48 50 54 56 V74", 2.2),
    "lapide": lambda: p("M32 74 V40 Q48 26 64 40 V74 Z", 2.8)
    + line(48, 44, 48, 60, 2.4) + line(40, 50, 56, 50, 2.4),
    "runa": lambda: p("M34 26 V70 M62 26 V70 M34 34 L62 48 M34 62 L62 48", 3.0),
    "corona": lambda: p("M26 62 L30 32 L40 46 L48 28 L56 46 L66 32 L70 62 Z", 2.8)
    + line(26, 70, 70, 70, 3.0),
    # Incudine: corno a sinistra, vita stretta, base larga. La sagoma è tutto.
    "incudine": lambda: p(
        "M16 44 Q28 38 38 38 H74 V50 H54 Q48 50 48 56 V62 H62 V72 H30 V62 H44 V56"
        " Q44 50 38 50 H16 Z", 2.8
    ),
    # Martelli incrociati: un martello solo, di profilo, legge come un cartello.
    "martello": lambda: p("M22 66 L58 26 M38 26 L74 66", 3.4)
    + p("M52 20 H68 L72 26 L64 34 H50 Z", 2.8)
    + p("M28 20 H44 L46 34 H32 L24 26 Z", 2.8),
    "bandiera": lambda: line(32, 22, 32, 76, 3.0)
    + p("M32 28 Q48 20 64 28 Q64 44 64 48 Q48 40 32 48 Z", 2.6),
}

SERIE = {
    "drappo": [
        ("00-hub", "ruota"), ("contrade", "scudo"), ("regole-corsa", "ferro"),
        ("giorno-1", "sorte"), ("giorno-2", "coppa"), ("giorno-3", "traguardo"),
        ("luoghi", "chiave"), ("iniziazione", "candela"), ("villain", "maschera"),
        ("guida-dm", "lanterna"), ("cassetta-dm", "cassetta"), ("pregen", "elmo"),
        ("statblocchi", "spade"), ("playtest", "clessidra"), ("ip", "sigillo"),
        ("mappe", "mappa"), ("stato-modulo", "libro"), ("feedback", "foglio"),
        ("volantino", "lettera"),
    ],
    "campagna": [
        ("arco-00-red-hand", "mano"), ("arco-01-miniera", "piccone"),
        ("arco-02-funghi", "fungo"), ("arco-03-cittadella", "torre"),
        ("arco-04-tomba", "lapide"), ("arco-05-runica", "runa"),
        ("arco-06-corona", "corona"), ("arco-07-forgia", "incudine"),
        ("arco-08-hammerfist", "martello"), ("arco-09-continuazione", "bandiera"),
    ],
}


def svg(glifo: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BOX} {BOX}" '
        f'width="{BOX}" height="{BOX}" role="img">\n'
        f"  {ring()}\n  {GLIFI[glifo]()}\n</svg>\n"
    )


def emit(serie: str, out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    for nome, glifo in SERIE[serie]:
        (out / f"fregio-{nome}.svg").write_text(svg(glifo), encoding="utf-8")
    return len(SERIE[serie])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--serie", choices=sorted(SERIE), help="quale serie generare")
    ap.add_argument("-o", "--out", help="cartella di destinazione")
    ap.add_argument("--all", action="store_true", help="entrambe le serie, nei posti canonici")
    args = ap.parse_args()

    if args.all:
        for s, d in DEST.items():
            n = emit(s, ROOT / d)
            print(f"✓ build_chapter_marks: {n} fregi «{s}» → {d}")
        return 0
    if not args.serie:
        ap.error("serve --serie oppure --all")
    dest = Path(args.out) if args.out else ROOT / DEST[args.serie]
    n = emit(args.serie, dest)
    print(f"✓ build_chapter_marks: {n} fregi «{args.serie}» → {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
