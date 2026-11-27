"""sistemi/pf1e/codice/incontri.py — il metodo «somma_px» per il GS di un incontro (F5 di ADR-0112).

Il codice di un plugin sta qui, non nel nucleo: `dmcore.sistemi.modulo(id,
"somma_px")` lo carica per nome dal registro `[moduli]` del `sistema.toml`
(importlib, solo file di questa cartella). Solo libreria standard.

PRD PF1e, «Designing Encounters»: un incontro vale la somma dei PE delle
creature (Experience Point Awards), e il suo GS è il più alto il cui valore in
PE non supera la somma. Due GS 10 → 19.200 PE → GS 12; tre → 28.800 → GS 13.
"""
from __future__ import annotations


def px_per_gs(cr: float, tab: "dict[str, int]") -> int:
    """PE di una creatura PF1e per GS. Sopra il GS più alto della tabella i PE
    raddoppiano ogni 2 GS, come fanno fino a lì."""
    if cr < 1:
        chiave = f"1/{round(1 / cr)}" if cr > 0 else "1/8"
        return tab.get(chiave, tab["1/8"])
    c = int(round(cr))
    if str(c) in tab:
        return tab[str(c)]
    alto = max(int(k) for k in tab if "/" not in k)
    return tab[str(alto - (c - alto) % 2)] * 2 ** ((c - alto + 1) // 2) if c > alto else tab["1"]


def gs_somma_px(crs: "list[float]", tab: "dict[str, int]") -> float:
    """Il GS di un incontro dalla somma dei PE; 0 senza creature."""
    if not crs:
        return 0.0
    tot = sum(px_per_gs(c, tab) for c in crs)
    gs = 0.0
    for chiave, px in tab.items():
        a, _, b = chiave.partition("/")
        v = int(a) / int(b) if b else float(a)
        if px <= tot and v > gs:
            gs = v
    alto = max(int(k) for k in tab if "/" not in k)
    while gs >= alto and px_per_gs(gs + 1, tab) <= tot:
        gs += 1
    return gs


def somma_px(dati: dict):
    """Il combinatore GS → GS dell'incontro con i `px_per_gs` di `incontri.livello`."""
    tab = dati["px_per_gs"]
    return lambda crs: gs_somma_px(crs, tab)
