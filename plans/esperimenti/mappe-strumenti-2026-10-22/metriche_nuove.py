#!/usr/bin/env python3
"""
metriche_nuove.py — le metriche che qualita_mappe.py non calcola, su mappe vere.

Prova del 2026-10-22 (RICERCA-STRUMENTI-MAPPE.md §2). In sola lettura.

1. Space syntax, VGA (Turner et al. 2001; Hillier e Hanson 1984): il grafo di
   visibilita' delle celle percorribili, con lo shadowcasting simmetrico di tcod
   come M4 del collaudo. Per ogni cella: connettivita' (= area dell'isovista in
   celle), profondita' media MD, RA = 2(MD-1)/(k-2), D_k di Hillier e Hanson,
   integrazione HH = D_k / RA. Sulla mappa: integrazione media, intelligibilita'
   (r² fra connettivita' e integrazione, Hillier 1996), clustering medio
   (Turner 2001).
2. Lo stesso sul grafo di movimento (diagonale con la regola degli angoli del
   collaudo): integrazione d'accesso. Il confronto fra le due e' la
   «visibility/accessibility discrepancy» di Martin (2014), qui resa come
   correlazione fra le due integrazioni [INFERRED: Martin non da' una formula
   unica nell'abstract].
3. Simmetria (Summerville et al. 2017): quota di celle uguali allo specchio
   orizzontale, verticale e alla rotazione di 180°, sulle classi di cella.
4. Diversita' dei pattern (Lucas e Volz 2019): distribuzione delle finestre 2×2
   sulle classi di cella; entropia in bit e KL simmetrizzata (pesi 0,5/0,5 come
   ETPKLDiv) contro il corpus della campagna, epsilon 1e-6.
5. Leniency adattata (Smith e Whitehead 2010) [INFERRED: i pesi del platform
   tradotti in tattica]: +1 per nemico e per cella di pericolo maggiore o letale,
   +0,5 per pericolo minore, -0,5 per cella di copertura; per 100 celle
   percorribili.

Uso:
    python3 metriche_nuove.py FILE.md[:N] [...]  [--json OUT]
    python3 metriche_nuove.py --prova            # le tre mappe del rapporto, due volte
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import tcod
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, shortest_path

from _comune import C, F, FUORI, REPO, collaudo, griglia_classi, impronta, mappe_di

PROVA = [
    ("07_il Portale Della Forgia Eterna/Mappe/Portale-Forgia-L2-REVISED-UltraClear.md", 1),
    ("07_il Portale Della Forgia Eterna/Mappe/hammerfist-372-1372/M7-F-fucina-grande-372.md", 1),
    ("07_il Portale Della Forgia Eterna/Mappe/ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.md", 1),
]
NEMICI = {"🔴", "⚫", "🟡", "🟣"}
EPS = 1e-6


def d_k(k: int) -> float:
    """Il valore D di Hillier e Hanson (1984) per k nodi: la RA del nodo radice
    di un diamante di k nodi. Formula di Krüger (1989) [INFERRED: riportata da
    memoria, verificata solo sul valore di Ostwald 2011, D_7 = 0,34]."""
    if k <= 3:
        return float("nan")
    return 2 * (k * (math.log2((k + 2) / 3) - 1) + 1) / ((k - 1) * (k - 2))


def sintassi(adj: np.ndarray) -> dict:
    """Integrazione HH, MD, connettivita', clustering su un grafo (matrice booleana)."""
    n = adj.shape[0]
    if n < 4:
        return {}
    g = csr_matrix(adj.astype(np.int8))
    ncomp, lab = connected_components(g, directed=False)
    dist = shortest_path(g, unweighted=True, directed=False)
    conn = adj.sum(axis=1).astype(float)
    integ = np.full(n, np.nan)
    md = np.full(n, np.nan)
    for c in range(ncomp):
        idx = np.where(lab == c)[0]
        k = len(idx)
        if k < 4:
            continue
        sub = dist[np.ix_(idx, idx)]
        md_c = sub.sum(axis=1) / (k - 1)
        ra = 2 * (md_c - 1) / (k - 2)
        md[idx] = md_c
        with np.errstate(divide="ignore"):
            integ[idx] = np.where(ra > 0, d_k(k) / ra, np.nan)
    # clustering di Turner: archi fra i vicini visibili / k(k-1)
    clus = np.zeros(n)
    A = adj.astype(np.int32)
    for i in range(n):
        nb = np.where(adj[i])[0]
        k = len(nb)
        if k >= 2:
            clus[i] = A[np.ix_(nb, nb)].sum() / (k * (k - 1))
    ok = ~np.isnan(integ)
    r2 = float(np.corrcoef(conn[ok], integ[ok])[0, 1] ** 2) if ok.sum() > 2 and np.std(integ[ok]) > 0 else None
    return {"componenti": int(ncomp), "connettivita_media": round(float(conn.mean()), 2),
            "md_media": round(float(np.nanmean(md)), 3),
            "integrazione_media": round(float(np.nanmean(integ)), 3),
            "integrazione_min": round(float(np.nanmin(integ)), 3),
            "integrazione_max": round(float(np.nanmax(integ)), 3),
            "intelligibilita_r2": None if r2 is None else round(r2, 3),
            "clustering_medio": round(float(clus.mean()), 3), "_integ": integ}


def metriche(file: Path, indice: int, g: dict, riferimento: Counter | None) -> dict:
    co = collaudo(file, indice, g)
    G = co.G
    perc = sorted(co.percorribili())
    pos = {c: i for i, c in enumerate(perc)}
    n = len(perc)
    trasp = np.array([[not F.get(G.at(x, y), {}).get("blocks_sight") and G.at(x, y) != FUORI
                       for x in range(G.W)] for y in range(G.H)], dtype=bool)
    # grafo di visibilita'
    V = np.zeros((n, n), dtype=bool)
    for i, (x, y) in enumerate(perc):
        if not trasp[y, x]:
            continue
        vista = tcod.map.compute_fov(trasp, (y, x), radius=0, light_walls=True,
                                     algorithm=tcod.constants.FOV_SYMMETRIC_SHADOWCAST)
        for j, (a, b) in enumerate(perc):
            if j != i and vista[b, a]:
                V[i, j] = True
    V = V | V.T
    # grafo di movimento
    M = np.zeros((n, n), dtype=bool)
    sp = set(perc)
    for i, c in enumerate(perc):
        for v in co.vicini(*c, sp):
            M[i, pos[v]] = True
    vis = sintassi(V)
    acc = sintassi(M)
    vad = None
    if vis and acc:
        a, b = vis.pop("_integ"), acc.pop("_integ")
        ok = ~np.isnan(a) & ~np.isnan(b)
        if ok.sum() > 2 and np.std(a[ok]) > 0 and np.std(b[ok]) > 0:
            vad = round(float(np.corrcoef(a[ok], b[ok])[0, 1]), 3)
    scala = g.get("scale_m") or 1.5
    isovista_m2 = round(vis.get("connettivita_media", 0) * scala * scala, 1) if vis else None

    # simmetria sulle classi
    K = griglia_classi(G)
    A = np.array([list(r.ljust(G.W, "V")) for r in K])
    sim = {"orizzontale": float((A == A[:, ::-1]).mean()), "verticale": float((A == A[::-1, :]).mean()),
           "rotazione": float((A == A[::-1, ::-1]).mean())}
    sim = {k: round(v, 3) for k, v in sim.items()}

    # pattern 2x2
    pat = pattern(A)
    tot = sum(pat.values())
    H = -sum((v / tot) * math.log2(v / tot) for v in pat.values())
    kl = None
    if riferimento:
        kl = round(kl_simm(pat, riferimento), 4)

    # leniency adattata
    pen = 0.0
    for x, y, c in G.tutte():
        f = F.get(c, {})
        if c in NEMICI:
            pen += 1
        hz = (f.get("hazard") or {}).get("severity")
        if hz in ("major", "lethal"):
            pen += 1
        elif hz == "minor":
            pen += 0.5
        if f.get("cover") in ("half", "three_quarters") and not f.get("blocks_movement"):
            pen -= 0.5
    len_100 = round(100 * pen / n, 2) if n else None

    return {"file": str(file.relative_to(REPO)) if file.is_relative_to(REPO) else str(file),
            "mappa": indice, "titolo": g["title"][:70], "celle_percorribili": n,
            "vga": vis, "accesso": acc, "vad_r": vad, "isovista_media_m2": isovista_m2,
            "simmetria": sim, "pattern_2x2": {"distinti": len(pat), "entropia_bit": round(H, 3),
                                              "kl_vs_corpus": kl},
            "leniency_per_100": len_100}


def pattern(A: np.ndarray, k: int = 2) -> Counter:
    h, w = A.shape
    return Counter("".join(A[y:y + k, x:x + k].ravel()) for y in range(h - k + 1) for x in range(w - k + 1))


def kl(p: Counter, q: Counter) -> float:
    tp, tq = sum(p.values()), sum(q.values())
    chiavi = sorted(set(p) | set(q))
    s = 0.0
    for c in chiavi:
        pp = (p.get(c, 0) + EPS) / (tp + EPS * len(chiavi))
        qq = (q.get(c, 0) + EPS) / (tq + EPS * len(chiavi))
        s += pp * math.log(pp / qq)
    return s


def kl_simm(p: Counter, q: Counter) -> float:
    return 0.5 * kl(p, q) + 0.5 * kl(q, p)


def corpus_pattern() -> Counter:
    """Le finestre 2x2 di tutte le tattiche del corpus del collaudo (sola lettura)."""
    tot = Counter()
    for f in C.bersagli([]):
        if "/plans/esperimenti/" in str(f):  # le prove (anche queste) non sono il corpus
            continue
        try:
            for g in mappe_di(f):
                d = C.direttive(g["annotations"])
                if d["tipo"] in ("strategica", "schema"):
                    continue
                G = C.Griglia(g)
                A = np.array([list(r.ljust(G.W, "V")) for r in griglia_classi(G)])
                if A.shape[0] >= 2 and A.shape[1] >= 2:
                    tot.update(pattern(A))
        except Exception:  # noqa: BLE001 — un master illeggibile non ferma la prova
            continue
    return tot


def bersagli(argomenti):
    out = []
    for a in argomenti:
        p, _, n = a.partition(":")
        out.append((REPO / p if not Path(p).is_absolute() else Path(p), int(n) if n else None))
    return out


def esegui(lista, rif) -> list[dict]:
    esiti = []
    for file, n in lista:
        mappe = mappe_di(file)
        for i, g in enumerate(mappe, 1):
            if n is None or i == n:
                esiti.append(metriche(file, i, g, rif))
    return esiti


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--json")
    ap.add_argument("--prova", action="store_true", help="le tre mappe del rapporto, due giri")
    a = ap.parse_args(argv)
    lista = bersagli([f"{p}:{n}" for p, n in PROVA]) if a.prova or not a.files else bersagli(a.files)
    rif = corpus_pattern()
    esiti = esegui(lista, rif)
    if a.prova:
        secondo = esegui(lista, corpus_pattern())
        print(f"giro 1 {impronta(esiti)} · giro 2 {impronta(secondo)} · "
              f"{'identici' if esiti == secondo else 'DIVERSI'}", file=sys.stderr)
    out = json.dumps(esiti, ensure_ascii=False, indent=1)
    if a.json:
        Path(a.json).write_text(out + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
