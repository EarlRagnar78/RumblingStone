#!/usr/bin/env python3
"""
coperture_cpsat.py — dove posare il minimo di coperture, con un solver a vincoli.

Prova del 2026-10-22 (RICERCA-STRUMENTI-MAPPE.md §5.3). OR-Tools CP-SAT
(Apache-2.0), un thread e seme fisso: stesso input, stessa soluzione.

Il problema, scritto come vincoli invece che come ricerca:
  - variabili: una per cella di pavimento libera (niente creature, oggetti,
    porte, scale, e niente celle a contatto con loro);
  - M1 del collaudo >= soglia: almeno la quota data del percorribile ha una
    copertura entro 2 quadretti (Chebyshev);
  - due coperture nuove non si toccano (leggibilita', Reynolds);
  - la densita' di icone resta sotto il 30% (lettura/affollata);
  - obiettivo: il numero minimo di coperture.
Accanto, l'avido classico (la cella che copre di piu', pareggi per coordinate),
per vedere quanto guadagna l'ottimo. Poi si rimisura con qualita_mappe.py.

Uso:
    python3 coperture_cpsat.py FILE.md[:N] [--m1 0.60] [--out FILE_NUOVO.md]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ortools.sat.python import cp_model

from _comune import C, F, MODO, R, REPO, collaudo, griglia_md, impronta, mappe_di, voto_di

PAVIMENTI = {"⬜", "🟤", "🟫", "🟩"}


def problema(G, perc):
    cop_esistenti = {(x, y) for x, y, c in G.tutte()
                     if F.get(c, {}).get("cover") in ("half", "three_quarters", "total")}
    vietate = set()
    for x, y, c in G.tutte():
        if (c not in PAVIMENTI and not F.get(c, {}).get("blocks_movement")) or MODO.get(c) == "unit" \
                or F.get(c, {}).get("door") or F.get(c, {}).get("posa") == "fra_livelli":
            vietate |= {(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    cand = sorted((x, y) for x, y in perc if G.at(x, y) in PAVIMENTI and (x, y) not in vietate)
    vicino = lambda a, b: max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= 2  # noqa: E731
    gia = {p for p in perc if any(vicino(p, k) for k in cop_esistenti)}
    return cand, gia, vicino


def risolvi(G, perc, soglia, icone_max):
    cand, gia, vicino = problema(G, perc)
    da_coprire = sorted(set(perc) - gia)
    serve = max(0, int(-(-soglia * len(perc) // 1)) - len(gia))
    m = cp_model.CpModel()
    x = {c: m.NewBoolVar(f"k{c[0]}_{c[1]}") for c in cand}
    cop = {p: m.NewBoolVar(f"c{p[0]}_{p[1]}") for p in da_coprire}
    for p in da_coprire:
        vic = [x[c] for c in cand if vicino(p, c)]
        if vic:
            m.AddBoolOr(vic).OnlyEnforceIf(cop[p])
        else:
            m.Add(cop[p] == 0)
    # una cella su cui si posa una copertura resta percorribile (🪨/🧱 non bloccano)
    m.Add(sum(cop.values()) >= serve)
    for a in cand:
        for b in cand:
            if a < b and max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= 1:
                m.AddBoolOr([x[a].Not(), x[b].Not()])
    m.Add(sum(x.values()) <= icone_max)
    m.Minimize(sum(x.values()))
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 1
    s.parameters.random_seed = 0
    # tempo deterministico, non di orologio: con il tetto a secondi veri la
    # soluzione dipenderebbe dalla velocita' della macchina
    s.parameters.max_deterministic_time = 5.0
    st = s.Solve(m)
    scelte = sorted(c for c in cand if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) and s.Value(x[c]))
    return {"stato": s.StatusName(st), "posate": scelte, "candidate": len(cand), "da_coprire": serve,
            "tempo_s": round(s.WallTime(), 3)}


def avido(G, perc, soglia):
    cand, gia, vicino = problema(G, perc)
    coperte, scelte, cand = set(gia), [], list(cand)
    obiettivo = soglia * len(perc)
    while len(coperte) < obiettivo and cand:
        best = max(cand, key=lambda c: (sum(1 for p in perc if p not in coperte and vicino(p, c)), -c[1], -c[0]))
        guadagno = {p for p in perc if p not in coperte and vicino(p, best)}
        if not guadagno:
            break
        scelte.append(best)
        coperte |= guadagno
        cand = [c for c in cand if max(abs(c[0] - best[0]), abs(c[1] - best[1])) > 1]
    return sorted(scelte)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("file")
    ap.add_argument("--m1", type=float, default=0.60)
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    p, _, n = a.file.partition(":")
    f = Path(p).resolve()
    i = int(n or 1)
    g = mappe_di(f)[i - 1]
    co = collaudo(f, i, g)
    G, perc = co.G, sorted(co.percorribili())
    amb = co.d["ambiente"]
    simbolo = "🪨" if amb == "caverna" else "🧱"
    icone = sum(1 for x, y in perc if MODO.get(G.at(x, y)) == "icon")
    icone_max = max(0, int(0.30 * len(perc)) - icone)
    v0, r0, m0 = voto_di(f, i, g, metriche=True)
    esiti = [risolvi(G, perc, a.m1, icone_max) for _ in range(2)]
    gr = avido(G, perc, a.m1)
    righe = [[G.at(x, y) for x in range(G.W)] for y in range(G.H)]
    for x, y in esiti[0]["posate"]:
        righe[y][x] = simbolo
    testo = griglia_md(g["title"], righe, list(g["annotations"]))
    nuovo = R.extract_maps(testo)[0]
    v1, r1, m1 = voto_di(f, i, nuovo, metriche=True)
    if a.out:
        Path(a.out).write_text(testo, encoding="utf-8")
    out = {"file": f.name, "simbolo": simbolo, "soglia_m1": a.m1,
           "prima": {"voto": v0, "m1": m0.get("m1"), "m2": m0.get("m2"), "rilievi": r0},
           "cpsat": {k: v for k, v in esiti[0].items() if k != "posate"} | {
               "n": len(esiti[0]["posate"]), "celle": [f"{R.col_label(x)}{y + 1:02d}" for x, y in esiti[0]["posate"]]},
           "avido_n": len(gr),
           "dopo": {"voto": v1, "m1": m1.get("m1"), "m2": m1.get("m2"), "rilievi": r1},
           "due_giri_identici": esiti[0]["posate"] == esiti[1]["posate"]}
    out["impronta"] = impronta({k: v for k, v in out.items() if k != "cpsat"} | {"celle": out["cpsat"]["celle"]})
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
