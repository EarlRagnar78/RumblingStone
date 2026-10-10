#!/usr/bin/env python3
"""Misura: i muri dell'export UVTT, oggi e con shapely. Riproduce RISULTATI.md §2.

    python3 plans/esperimenti/dipendenze-e-asset-2026-10/bench_uvtt.py

`export_uvtt.extract_walls` fonde gia' i lati di cella collineari in segmenti
dritti. shapely (`linemerge`) unirebbe i segmenti che si toccano negli angoli
in polilinee. Si conta quanti oggetti `line_of_sight` escono e quanti segmenti
(coppie di punti consecutivi) contengono, che e' cio' che un VTT trasforma in
muri. Non scrive niente nel repo.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import collaudo_mappe as C  # noqa: E402
import export_uvtt as U  # noqa: E402


def main() -> int:
    from shapely.geometry import LineString, MultiLineString
    from shapely.ops import linemerge

    oggi_obj = oggi_seg = sh_obj = sh_seg = 0
    t_sh = 0.0
    for f in C.bersagli([]):
        try:
            testo = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for g in C.R.extract_maps(testo):
            muri = U.extract_walls(U._grid_matrix(g))
            oggi_obj += len(muri)
            oggi_seg += sum(len(m) - 1 for m in muri)
            if not muri:
                continue
            t = time.perf_counter()
            fuso = linemerge(MultiLineString([LineString([(p["x"], p["y"]) for p in m]) for m in muri]))
            linee = list(fuso.geoms) if hasattr(fuso, "geoms") else [fuso]
            t_sh += time.perf_counter() - t
            sh_obj += len(linee)
            # un VTT fa un muro per ogni coppia di punti; i punti collineari di
            # una polilinea fusa non aggiungono muri se si semplifica
            sh_seg += sum(len(linea.simplify(0).coords) - 1 for linea in linee)
    print(f"oggi:    {oggi_obj} oggetti line_of_sight, {oggi_seg} segmenti (muri nel VTT)")
    print(f"shapely: {sh_obj} polilinee, {sh_seg} segmenti (muri nel VTT) · {t_sh * 1000:.0f} ms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
