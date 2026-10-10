#!/usr/bin/env python3
"""Misura in sola lettura: l'asse delle chiusure nel corpus, e chi lo sbagliava.

Riproduce i numeri di RISULTATI.md §1. Non scrive niente nel repo. Solo
libreria standard.

    python3 -I plans/esperimenti/orientamento-e-dipendenze-2026-10/misura_assi.py

Per ogni cella con `posa: nel_muro` o `recinto` (porte, grate, finestre,
sbarre) confronta tre letture:

  - l'asse di `dmcore.chiusure` (ADR-0083), la regola nuova;
  - la regola che `export_uvtt.py` usava fino al 2026-10-08: «muro sopra *o*
    sotto» = muro nord-sud;
  - il renderer di prima, che disegnava ogni chiusura come in un muro
    est-ovest.

Il corpus e' quello di `collaudo_mappe.py` (niente archivi, fixture, derivati).
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import collaudo_mappe as C  # noqa: E402
import export_uvtt as U  # noqa: E402
from dmcore import chiusure as K  # noqa: E402


def regola_uvtt_vecchia(M, x, y) -> str:
    return K.NS if (U._is_wall(M, x, y - 1) or U._is_wall(M, x, y + 1)) else K.EO


def main() -> int:
    assi, simboli = Counter(), Counter()
    uvtt, render = Counter(), Counter()
    mappe_ns: Counter = Counter()
    n_mappe = 0
    for f in C.bersagli([]):
        try:
            testo = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, g in enumerate(C.R.extract_maps(testo), 1):
            n_mappe += 1
            G = C.Griglia(g)
            M = U._grid_matrix(g)

            def at(x, y, G=G):
                c = G.at(x, y)
                return None if c == C.FUORI else c
            for x, y, c in G.tutte():
                if not K.e_chiusura(c):
                    continue
                simboli[c] += 1
                a = K.asse(at, x, y)
                assi[str(a)] += 1
                if a == K.NS:
                    mappe_ns[(str(f.relative_to(REPO)), i)] += 1
                if a in (K.EO, K.NS):
                    render["giusto" if a == K.EO else "di traverso"] += 1
                    if M[y][x] in U.DOOR_SYMS:
                        uvtt["giusto" if regola_uvtt_vecchia(M, x, y) == a else "di traverso"] += 1
    print(f"corpus: {n_mappe} mappe · chiusure per simbolo: {dict(simboli)}")
    print(f"asse (dmcore.chiusure): EO {assi['EO']} · NS {assi['NS']} · "
          f"ambigue {assi['?']} · senza muro {assi['None']}")
    print(f"renderer di prima, sulle chiusure con un asse: {dict(render)}")
    print(f"export_uvtt di prima, sulle porte con un asse: {dict(uvtt)}")
    print(f"mappe con almeno una chiusura nord-sud: {len(mappe_ns)}")
    for (file, i), k in sorted(mappe_ns.items()):
        print(f"  {k:3d}  {file} #{i}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
