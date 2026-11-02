#!/usr/bin/env python3
"""
fazioni_liapis.py — prova della ricerca in rete del 2026-10-23 (non adottata).

Misura su ogni mappa tattica con PG (🔵) e nemici le grandezze di Liapis,
Yannakakis e Togelius, *Towards a Generic Method of Evaluating Game Levels*
(AIIDE 2013), con le due fazioni al posto delle basi, e una misura di linea di
tiro sull'avvicinamento che lo standard ADR-0098 non calcola:

  area_pg, area_nem   quota del percorribile «sicura» per la fazione:
                      s = (d_altra - d_mia) / (d_altra + d_mia) >= 0,35
                      (eq. 1 di Liapis 2013, soglia C_s = 0,35)
  bilancio_area       b_a = 1 - |A_pg - A_nem| / max(A_pg, A_nem)
  esplorazione_pg/nem riempimento a 4 direzioni dalla fazione finché tocca
                      l'altra, sul percorribile (eq. 2); bilancio come sopra
  tiro_avvicinamento  quota delle celle del cammino più corto PG -> nemico più
                      vicino che almeno un nemico vede (shadowcasting
                      simmetrico di tcod, come M4 del collaudo)
  tiro_scoperto       di quelle, la quota senza copertura a contatto
  tiro_sull_area_pg   quota dell'area sicura dei PG vista da almeno un nemico

Le distanze sono quelle del collaudo (otto direzioni, la diagonale non passa
l'angolo di un muro, ogni passo vale uno). Deterministico, sola lettura.

Uso:
    python3 fazioni_liapis.py FILE.md [...]              # versione nel disco
    python3 fazioni_liapis.py --rev d726e6a2 FILE.md     # versione di un commit
    python3 fazioni_liapis.py --json OUT.json ...
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from collections import deque
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "scripts"))

import collaudo_mappe as C  # noqa: E402
import qualita_mappe as Q  # noqa: E402

PG, NEMICI = Q.PG, Q.NEMICI
CS = 0.35


def bfs(starts, perc, vicini):
    dist = {s: 0 for s in starts if s in perc}
    coda = deque(dist)
    while coda:
        a = coda.popleft()
        for b in vicini(*a):
            if b not in dist:
                dist[b] = dist[a] + 1
                coda.append(b)
    return dist


def esplora(starts, mete, perc):
    """Riempimento a 4 direzioni dalle partenze fino alla prima meta (Liapis)."""
    visti = set(s for s in starts if s in perc)
    coda = deque(sorted(visti))
    mete = set(mete)
    while coda:
        a = coda.popleft()
        if a in mete:
            return len(visti)
        x, y = a
        for b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if b in perc and b not in visti:
                visti.add(b)
                coda.append(b)
    return len(visti)


def bil(a, b):
    m = max(a, b)
    return 1.0 if m == 0 else 1 - abs(a - b) / m


def misura(file: Path, indice: int, g: dict) -> dict | None:
    col = C.Collaudo(file, indice, g, {})
    if not col.tattica:
        return None
    G = col.G
    pg = [(x, y) for x, y, c in G.tutte() if c == PG]
    nem = [(x, y) for x, y, c in G.tutte() if c in NEMICI]
    if not (pg and nem):
        return None
    # le creature stanno su celle percorribili
    perc = col.percorribili() | set(pg) | set(nem)

    def vicini(x, y):
        return col.vicini(x, y, perc)

    dp, dn = bfs(pg, perc, vicini), bfs(nem, perc, vicini)
    P = len(perc)
    sp = sn = 0
    for t in perc:
        a, b = dp.get(t), dn.get(t)
        if a is None and b is None:
            continue
        if b is None or (a is not None and a + b > 0 and (b - a) / (a + b) >= CS):
            sp += 1
        elif a is None or (a + b > 0 and (a - b) / (a + b) >= CS):
            sn += 1
    ep = esplora(pg, nem, perc) / P
    en = esplora(nem, pg, perc) / P

    import numpy as np
    import tcod
    trasp = np.array([[not C.F.get(G.at(x, y), {}).get("blocks_sight") and G.at(x, y) != C.FUORI
                       for x in range(G.W)] for y in range(G.H)], dtype=bool)
    vista = np.zeros((G.H, G.W), dtype=bool)
    for x, y in nem:
        vista |= tcod.map.compute_fov(trasp, (y, x), radius=0, light_walls=True,
                                      algorithm=tcod.constants.FOV_SYMMETRIC_SHADOWCAST)
    copertura = {(x, y) for x, y, c in G.tutte()
                 if C.F.get(c, {}).get("cover") in ("half", "three_quarters", "total")}

    def coperta(x, y):
        return any((x + dx, y + dy) in copertura for dx in (-1, 0, 1) for dy in (-1, 0, 1))

    # cammino più corto da un PG al nemico più vicino, ricostruito sulle distanze dn
    raggiunti = [n for n in nem if n in dp]
    tiro = scoperto = None
    lung = None
    if raggiunti:
        inizio = min((p for p in pg if p in dn), key=lambda p: (dn[p], p), default=None)
        if inizio is not None:
            cam = [inizio]
            while dn[cam[-1]] > 0:
                cam.append(min((b for b in vicini(*cam[-1]) if dn.get(b, 1e9) < dn[cam[-1]]),
                               key=lambda b: (dn[b], b)))
            interni = cam[1:-1] or cam
            visti = [c for c in interni if vista[c[1], c[0]]]
            lung = len(cam) - 1
            tiro = len(visti) / len(interni)
            scoperto = (sum(1 for c in visti if not coperta(*c)) / len(visti)) if visti else 0.0
    area_pg_celle = [t for t in perc if (dp.get(t) is not None) and (
        dn.get(t) is None or (dp[t] + dn[t] > 0 and (dn[t] - dp[t]) / (dp[t] + dn[t]) >= CS))]
    tiro_area = (sum(1 for x, y in area_pg_celle if vista[y, x]) / len(area_pg_celle)) if area_pg_celle else None
    r = lambda v: None if v is None else round(v, 3)  # noqa: E731
    return {"titolo": G.g["title"][:70], "celle": P, "pg": len(pg), "nemici": len(nem),
            "area_pg": r(sp / P), "area_nem": r(sn / P), "bilancio_area": r(bil(sp, sn)),
            "esplorazione_pg": r(ep), "esplorazione_nem": r(en), "bilancio_esplorazione": r(bil(ep, en)),
            "cammino_passi": lung, "tiro_avvicinamento": r(tiro), "tiro_scoperto": r(scoperto),
            "tiro_sull_area_pg": r(tiro_area)}


def leggi(file: Path, rev: str | None, tmp: Path) -> Path:
    if rev is None:
        return file
    rel = file.resolve().relative_to(REPO)
    testo = subprocess.run(["git", "-C", str(REPO), "show", f"{rev}:{rel.as_posix()}"],
                           capture_output=True, text=True, check=True).stdout
    out = tmp / rev / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(testo, encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="+", type=Path)
    ap.add_argument("--rev")
    ap.add_argument("--json", type=Path)
    a = ap.parse_args(argv)
    righe = []
    with tempfile.TemporaryDirectory() as t:
        for f in a.file:
            src = leggi(f, a.rev, Path(t))
            for i, g in enumerate(C.R.extract_maps(src.read_text(encoding="utf-8")), 1):
                m = misura(src, i, g)
                if m:
                    m.update(file=f.as_posix(), mappa=i)
                    righe.append(m)
    chiavi = ["area_pg", "area_nem", "bilancio_area", "esplorazione_pg", "esplorazione_nem",
              "bilancio_esplorazione", "cammino_passi", "tiro_avvicinamento", "tiro_scoperto",
              "tiro_sull_area_pg"]
    print("| file | # | titolo | " + " | ".join(chiavi) + " |")
    print("|---" * (3 + len(chiavi)) + "|")
    for m in righe:
        print(f"| {Path(m['file']).name} | {m['mappa']} | {m['titolo'][:40]} | "
              + " | ".join("—" if m[k] is None else str(m[k]) for k in chiavi) + " |")
    if a.json:
        a.json.write_text(json.dumps(righe, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
