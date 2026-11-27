"""sistemi/d20/codice/incontri.py — il metodo «potenze» per l'EL (F5 di ADR-0112).

Il codice di un plugin sta qui, non nel nucleo: `dmcore.sistemi.modulo(id,
"potenze")` lo carica per nome dal registro `[moduli]` del `sistema.toml`
(importlib, solo file di questa cartella). Solo libreria standard.

In 3.5 raddoppiare le creature di pari GS alza l'EL di 2 (DMG 3.5 p. 49).
La potenza scala come 2^(GS/r) e l'EL dell'incontro è

    EL = r · log2( Σ 2^(GS/r) )

con r = `raddoppio` del plugin (3.5: 2). Due GS 10 → 2·log2(2·2^5) = 12.
"""
from __future__ import annotations

import math


def el_potenze(crs: "list[float]", raddoppio: float = 2.0) -> float:
    """L'EL di un incontro: r · log2(Σ 2^(GS/r)); 0 senza creature."""
    if not crs:
        return 0.0
    r = float(raddoppio)
    return r * math.log2(sum(2 ** (c / r) for c in crs))


def potenze(dati: dict):
    """Il combinatore GS → EL col `raddoppio` di `incontri.livello`."""
    raddoppio = dati.get("raddoppio", 2)
    return lambda crs: el_potenze(crs, raddoppio)
