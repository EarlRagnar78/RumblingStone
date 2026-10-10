#!/usr/bin/env python3
"""Misura: hypothesis contro un generatore a seme fisso in libreria standard,
sullo stesso insieme di proprieta', su mutanti del grafo del collaudo.
Riproduce RISULTATI.md §3. Non scrive niente nel repo (i mutanti vanno in una
cartella temporanea).

    python3 plans/esperimenti/dipendenze-e-asset-2026-10/bench_mutanti.py

Le proprieta' sono tre, tutte dall'SRD o dalla geometria:

  P1  le zone non dipendono dal nord: ruotare la griglia di 90 gradi lascia
      uguale la partizione in componenti;
  P2  la regola dell'angolo: una mossa diagonale ammessa non ha un muro su
      nessuno dei due lati ortogonali;
  P3  una porta e' un varco: sostituire una porta con un pavimento non cambia
      le componenti.

Ogni mutante e' un errore plausibile, scritto a mano nel testo del modulo.
Stesso budget per i due generatori: 1.500 griglie per proprieta'.
"""
from __future__ import annotations

import importlib.util
import random
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
SORGENTE = (REPO / "scripts" / "collaudo_mappe.py").read_text(encoding="utf-8")
SIMBOLI = ["🏰", "⬜", "⬜", "🚪", "🕳", "🟫"]
BUDGET = 1500

MUTANTI = {
    "diagonale sempre ammessa": (
        "if dx and dy and (angolo(self.G.at(x + dx, y)) or angolo(self.G.at(x, y + dy))):",
        "if False:"),
    "angolo: and invece di or": (
        "(angolo(self.G.at(x + dx, y)) or angolo(self.G.at(x, y + dy)))",
        "(angolo(self.G.at(x + dx, y)) and angolo(self.G.at(x, y + dy)))"),
    "la porta blocca": (
        "and not porta(c)\n", "\n"),
    "la fossa ferma la diagonale": (
        "return murario(c) and c != FUORI",
        "return (murario(c) or c == '🕳') and c != FUORI"),
    "un vicino perso (dx da -1 a 1 escluso)": (
        "for dx in (-1, 0, 1):", "for dx in (0, 1):"),
    "componenti senza la coda": (
        "                        coda.append(b)\n", "                        pass\n"),
}


def carica(testo: str, nome: str):
    d = Path(tempfile.mkdtemp())
    p = d / f"{nome}.py"
    p.write_text(testo, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(nome, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def partizione(M, righe):
    g = {"rows": {i + 1: r for i, r in enumerate(righe)}, "annotations": [], "local_legend": {},
         "title": "prova"}
    c = M.Collaudo(Path("prova.md"), 1, g, {})
    perc = c.percorribili()
    comp = c.componenti(perc)
    gruppi = {}
    for p, k in comp.items():
        gruppi.setdefault(k, set()).add(p)
    return c, perc, {frozenset(v) for v in gruppi.values()}


def ruota(righe):
    n = len(righe)
    return [[righe[n - 1 - x][y] for x in range(n)] for y in range(n)]


def p1(M, g):
    n = len(g)
    _, _, a = partizione(M, g)
    _, _, b = partizione(M, ruota(g))
    # (x, y) in g va in (n-1-y, x) nella ruotata
    a_r = {frozenset((n - 1 - y, x) for x, y in s) for s in a}
    return a_r == b


def p2(M, g):
    c, perc, _ = partizione(M, g)
    for x, y in perc:
        for q in c.vicini(x, y, perc):
            dx, dy = q[0] - x, q[1] - y
            if dx and dy and (M.murario(c.G.at(x + dx, y)) and c.G.at(x + dx, y) != M.FUORI
                              or M.murario(c.G.at(x, y + dy)) and c.G.at(x, y + dy) != M.FUORI):
                return False
        # e ogni vicino ortogonale percorribile c'e'
        for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if q in perc and q not in set(c.vicini(x, y, perc)):
                return False
    return True


def p3(M, g):
    _, _, a = partizione(M, g)
    _, _, b = partizione(M, [[("⬜" if s == "🚪" else s) for s in r] for r in g])
    return a == b


PROPRIETA = (p1, p2, p3)


def con_seme(M) -> bool:
    rng = random.Random(20261008)
    for prop in PROPRIETA:
        for _ in range(BUDGET):
            n = rng.randint(3, 7)
            g = [[rng.choice(SIMBOLI) for _ in range(n)] for _ in range(n)]
            if not prop(M, g):
                return True
    return False


def con_hypothesis(M):
    from hypothesis import given, settings, strategies as st, HealthCheck
    griglie = st.integers(3, 7).flatmap(
        lambda n: st.lists(st.lists(st.sampled_from(SIMBOLI), min_size=n, max_size=n), min_size=n, max_size=n))
    preso, minimo = False, None
    for prop in PROPRIETA:
        @settings(max_examples=BUDGET, deadline=None, database=None,
                  suppress_health_check=list(HealthCheck))
        @given(griglie)
        def t(g):
            assert prop(M, g)
        try:
            t()
        except AssertionError as e:
            preso = True
            minimo = getattr(e, "__notes__", None)
            break
    return preso, minimo


def main() -> int:
    originale = carica(SORGENTE, "cm_originale")
    print(f"originale: seme {'ROSSO' if con_seme(originale) else 'verde'} · "
          f"hypothesis {'ROSSO' if con_hypothesis(originale)[0] else 'verde'}")
    s = h = 0
    for i, (nome, (da, a)) in enumerate(MUTANTI.items()):
        assert da in SORGENTE, nome
        M = carica(SORGENTE.replace(da, a, 1), f"cm_mut{i}")
        rs, (rh, nota) = con_seme(M), con_hypothesis(M)
        s += rs
        h += rh
        es = (nota or [""])[0].replace("\n", " ")[:70] if nota else ""
        print(f"  {nome:42s} seme {'preso' if rs else 'MANCATO'} · hypothesis "
              f"{'preso' if rh else 'MANCATO'}  {es}")
    print(f"presi: seme {s}/{len(MUTANTI)} · hypothesis {h}/{len(MUTANTI)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
