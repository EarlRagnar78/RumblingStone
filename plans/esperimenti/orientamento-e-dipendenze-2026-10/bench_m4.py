#!/usr/bin/env python3
"""Misura: M4 esatta (visibilita' da OGNI cella) su tutto il corpus, in libreria
standard e con tcod. Riproduce RISULTATI.md §3. Non scrive niente nel repo.

    python3 plans/esperimenti/orientamento-e-dipendenze-2026-10/bench_m4.py

La versione stdlib e' lo shadowcasting simmetrico di Albert Ford, scritto dalla
descrizione, con le pendenze in aritmetica intera (niente `Fraction`, che lo
rendeva sette volte piu' lento). Su un campione di celle si verifica che dia lo
stesso insieme visibile di tcod, poi si cronometrano le due su tutte le celle.
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import collaudo_mappe as C  # noqa: E402


def opaca(c) -> bool:
    return c == C.FUORI or bool(C.F.get(c, {}).get("blocks_sight"))


def fov_stdlib(orig, blocca, W, H):
    vis = {orig}
    ox, oy = orig
    quadranti = ((lambda r, c: (ox + c, oy - r)), (lambda r, c: (ox + r, oy + c)),
                 (lambda r, c: (ox + c, oy + r)), (lambda r, c: (ox - r, oy + c)))
    for tr in quadranti:
        pila = [(1, -1, 1, 1, 1)]  # profondita', pendenza iniziale e finale come num/den
        while pila:
            d, sn, sd, en, ed = pila.pop()
            lo = math.floor((2 * d * sn + sd) / (2 * sd))
            hi = math.ceil((2 * d * en - ed) / (2 * ed))
            prec = None
            for col in range(lo, hi + 1):
                x, y = tr(d, col)
                dentro = 0 <= x < W and 0 <= y < H
                muro = (not dentro) or blocca(x, y)
                simmetrica = col * sd >= d * sn and col * ed <= d * en
                if dentro and (muro or simmetrica):
                    vis.add((x, y))
                if prec is True and not muro:
                    sn, sd = 2 * col - 1, 2 * d
                if prec is False and muro:
                    pila.append((d + 1, sn, sd, 2 * col - 1, 2 * d))
                prec = muro
            if prec is False and d < 2 * max(W, H):
                pila.append((d + 1, sn, sd, en, ed))
    return vis


def main() -> int:
    mappe = []
    for f in C.bersagli([]):
        try:
            testo = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        mappe += [C.Griglia(g) for g in C.R.extract_maps(testo)]

    t0, n = time.time(), 0
    risultati = []
    for G in mappe:
        def bl(x, y, G=G):
            return opaca(G.at(x, y))
        celle = [(x, y) for x, y, c in G.tutte() if not opaca(c)]
        for i, p in enumerate(celle):
            v = fov_stdlib(p, bl, G.W, G.H)
            n += 1
            if i % 97 == 0:
                risultati.append((G, p, v))
    print(f"stdlib: {n} celle in {time.time() - t0:.1f} s")

    try:
        import numpy as np
        import tcod
    except ImportError:
        print("tcod non installato: pip install -r requirements-dev.txt")
        return 0
    t0, n = time.time(), 0
    for G in mappe:
        tr = np.array([[not opaca(G.at(x, y)) for x in range(G.W)] for y in range(G.H)], dtype=bool)
        for y, x in zip(*np.nonzero(tr)):
            tcod.map.compute_fov(tr, (int(y), int(x)), algorithm=tcod.constants.FOV_SYMMETRIC_SHADOWCAST)
            n += 1
    print(f"tcod:   {n} celle in {time.time() - t0:.1f} s")

    uguali, inter, unione = 0, 0, 0
    for G, p, v in risultati:
        tr = np.array([[not opaca(G.at(x, y)) for x in range(G.W)] for y in range(G.H)], dtype=bool)
        m = tcod.map.compute_fov(tr, (p[1], p[0]), algorithm=tcod.constants.FOV_SYMMETRIC_SHADOWCAST)
        vt = {(x, y) for y in range(G.H) for x in range(G.W) if m[y, x]}
        uguali += vt == v
        inter += len(vt & v)
        unione += len(vt | v)
    print(f"accordo su {len(risultati)} celle campione: {uguali} insiemi identici, "
          f"Jaccard {inter / unione:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
