#!/usr/bin/env python3
"""Misura: networkx e scipy contro la libreria standard, sui compiti veri del
collaudo. Riproduce RISULTATI.md §1. Non scrive niente nel repo.

    python3 plans/esperimenti/dipendenze-e-asset-2026-10/bench_grafi.py

Compiti, sulle mappe del corpus di `collaudo_mappe.py`:

  V7  strozzature (punti d'articolazione) e anelli mu = E - V + C del grafo
      delle celle percorribili, con le regole di movimento dell'SRD
      (diagonale vietata oltre l'angolo di un muro): networkx contro Tarjan
      scritto in casa.
  M1  la frazione del percorribile con una copertura entro 2 quadretti, e
  M2  il piu' grande spazio aperto senza coperture: scipy.ndimage contro il
      codice che `collaudo_mappe.py` aveva prima di adottare scipy, qui copiato.

Per ogni compito: tempo su tutto il corpus (migliore di 5 giri), accordo dei
risultati, righe di codice della versione in casa.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import collaudo_mappe as C  # noqa: E402


def corpus():
    out = []
    for f in C.bersagli([]):
        try:
            testo = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, g in enumerate(C.R.extract_maps(testo), 1):
            col = C.Collaudo(f, i, g, {})
            perc = col.percorribili()
            archi = {(p, q) for p in perc for q in col.vicini(*p, perc) if p < q}
            out.append((col, perc, archi))
    return out


# --- V7 in casa: Tarjan iterativo, 30 righe ------------------------------------
def articolazioni(nodi, adiac) -> set:
    disc, low, punti, t = {}, {}, set(), 0
    for r in nodi:
        if r in disc:
            continue
        disc[r] = low[r] = t
        t += 1
        figli_radice = 0
        pila = [(r, None, iter(adiac[r]))]
        while pila:
            v, padre, it = pila[-1]
            w = next(it, None)
            if w is None:
                pila.pop()
                if padre is not None:
                    low[padre] = min(low[padre], low[v])
                    if pila[-1][1] is not None and low[v] >= disc[padre]:
                        punti.add(padre)
                continue
            if w == padre:
                continue
            if w in disc:
                low[v] = min(low[v], disc[w])
            else:
                disc[w] = low[w] = t
                t += 1
                if v == r:
                    figli_radice += 1
                pila.append((w, v, iter(adiac[w])))
        if figli_radice > 1:
            punti.add(r)
    return punti


def v7_casa(perc, archi):
    adiac = {p: [] for p in perc}
    for a, b in archi:
        adiac[a].append(b)
        adiac[b].append(a)
    punti = articolazioni(sorted(perc), adiac)
    visti, comp = set(), 0
    for p in perc:
        if p in visti:
            continue
        comp += 1
        coda = [p]
        visti.add(p)
        while coda:
            x = coda.pop()
            for y in adiac[x]:
                if y not in visti:
                    visti.add(y)
                    coda.append(y)
    return punti, len(archi) - len(perc) + comp


def v7_networkx(perc, archi):
    import networkx as nx
    g = nx.Graph()
    g.add_nodes_from(perc)
    g.add_edges_from(archi)
    return set(nx.articulation_points(g)), g.number_of_edges() - g.number_of_nodes() + nx.number_connected_components(g)


# --- M1 e M2: il codice di oggi, e scipy ---------------------------------------
def m1m2_casa(col, perc):
    G = col.G
    cop = {(x, y) for x, y, c in G.tutte() if C.F.get(c, {}).get("cover") in ("half", "three_quarters", "total")}
    vicino = {(x, y) for x, y in perc if any((x + a, y + b) in cop for a in range(-2, 3) for b in range(-2, 3))}
    return len(vicino) / len(perc), vuoto(perc - vicino) / len(perc)


def vuoto(aperto) -> int:
    """Il calcolo di M2 che `collaudo_mappe` usava prima di scipy (ADR-0084)."""
    visti, piu = set(), 0
    for c in aperto:
        if c in visti:
            continue
        visti.add(c)
        coda, k = [c], 0
        while coda:
            a = coda.pop()
            k += 1
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                b = (a[0] + d[0], a[1] + d[1])
                if b in aperto and b not in visti:
                    visti.add(b)
                    coda.append(b)
        piu = max(piu, k)
    return piu


def m1m2_scipy(col, perc):
    import numpy as np
    from scipy import ndimage
    G = col.G
    P = np.zeros((G.H, G.W), bool)
    K = np.zeros((G.H, G.W), bool)
    for x, y, c in G.tutte():
        if C.F.get(c, {}).get("cover") in ("half", "three_quarters", "total"):
            K[y, x] = True
    for x, y in perc:
        P[y, x] = True
    vicino = ndimage.binary_dilation(K, structure=np.ones((5, 5), bool)) & P
    aperto = P & ~vicino
    lab, n = ndimage.label(aperto)
    piu = int(np.bincount(lab.ravel())[1:].max()) if n else 0
    return vicino.sum() / P.sum(), piu / P.sum()


def cronometra(f, giri=5):
    meglio = None
    for _ in range(giri):
        t = time.perf_counter()
        r = f()
        d = time.perf_counter() - t
        meglio = d if meglio is None or d < meglio else meglio
    return meglio, r


def main() -> int:
    mappe = corpus()
    print(f"corpus: {len(mappe)} mappe, {sum(len(p) for _, p, _ in mappe)} celle percorribili, "
          f"{sum(len(a) for _, _, a in mappe)} archi")

    tc, rc = cronometra(lambda: [v7_casa(p, a) for _, p, a in mappe])
    tn, rn = cronometra(lambda: [v7_networkx(p, a) for _, p, a in mappe])
    uguali = sum(a == b for a, b in zip(rc, rn))
    strozz = sum(len(r[0]) for r in rc)
    print(f"V7 strozzature e anelli · in casa {tc * 1000:.0f} ms · networkx {tn * 1000:.0f} ms · "
          f"risultati identici su {uguali}/{len(mappe)} mappe · {strozz} strozzature in tutto")

    grandi = [(c, p) for c, p, _ in mappe if c.G.W >= 12 and c.G.H >= 12 and p]
    tc, rc = cronometra(lambda: [m1m2_casa(c, p) for c, p in grandi])
    ts, rs = cronometra(lambda: [m1m2_scipy(c, p) for c, p in grandi])
    diff = max(max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a, b in zip(rc, rs))
    print(f"M1+M2 su {len(grandi)} mappe · in casa {tc * 1000:.0f} ms · scipy {ts * 1000:.0f} ms · "
          f"differenza massima {diff:.6f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
