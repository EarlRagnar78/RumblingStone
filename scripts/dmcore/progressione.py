"""dmcore.progressione — le regole di classe e di tipo delle creature, senza caratteristiche.

ADR-0066, `PIANO-QUALITA-DEL-CODICE` §8 (lotto E).

Qui stanno le cose che chi genera e chi verifica devono vedere **uguali**,
perche' sono regole del SRD 3.5 e non scelte: i gruppi di dadi vita (una classe,
o i DV razziali del tipo), i nomi con cui le schede scrivono le classi, le due
classi di prestigio SRD che compaiono nel Bestiario, la base dei tiri salvezza
(buono 2 + L/2, cattivo L/3) e il BAB atteso.

Lo importano tutti: `genera_attributi`, `conformita_statblocchi`,
`derive_statblocks`, `genera_creatura` e gli altri due moduli del lotto. Non
importa niente che scelga.

🔎 **Perche' la base dei TS sta qui e non solo in `dmcore.tabelle`.** Le due
formule (`ts_buono`, `ts_cattivo`) erano gia' in `tabelle`; ma quattro script
ci costruivano sopra la base in quattro modi, e il verificatore la riscriveva
a mano (`2 + g.n // 2`). La regola che conta e' quella dei **gruppi**: i DV
di ogni classe si sommano, e i DV razziali dell'umanoide hanno un TS buono che
varia (SRD), quindi danno una fascia e non un numero.

Solo stdlib.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass

from dmcore import tabelle as T

__all__ = ["TS", "Gruppo", "ABBREVIAZIONI", "PRESTIGIO", "DADO_DI_CLASSE",
           "NOMI_DI_CLASSE", "CLASSE_LIVELLO", "classe", "ts_base_di", "ts_base",
           "bab_atteso"]

#: I tre tiri salvezza, nell'ordine in cui le schede li scrivono.
TS = ("temp", "rifl", "vol")

#: Le abbreviazioni con cui le schede scrivono le classi.
ABBREVIAZIONI = {"ftr": "fighter", "wiz": "wizard", "clr": "cleric", "rog": "rogue",
                 "rgr": "ranger", "brb": "barbarian", "bbn": "barbarian",
                 "sor": "sorcerer", "mnk": "monk", "drd": "druid", "pal": "paladin",
                 "guerrier": "guerriero", "chieric": "chierico", "barbar": "barbaro",
                 "ladr": "ladro", "stregon": "stregone", "monac": "monaco",
                 "druid": "druid", "magi": "mago"}

#: Le due classi di prestigio SRD che compaiono nel Bestiario e non stanno in
#: `dmcore.tabelle`: (dado dei DV, TS buoni, BAB per livello).
PRESTIGIO = {"blackguard": (10, ("temp",), 1.0), "assassin": (6, ("rifl",), 0.75)}

#: Il dado dei DV per ogni nome con cui una scheda scrive una classe.
DADO_DI_CLASSE = {**{n: d for n, (d, _) in T.CLASSI.items()},
                  **{n: v[0] for n, v in PRESTIGIO.items()},
                  **{a: T.CLASSI[n][0] for a, n in ABBREVIAZIONI.items()}}

NOMI_DI_CLASSE = sorted(set(T.CLASSI) | set(PRESTIGIO) | set(ABBREVIAZIONI),
                        key=len, reverse=True)
#: «Fighter 3», «Clr. 5», «Guerriero 4»: una classe e il suo livello.
CLASSE_LIVELLO = re.compile(
    r"\b(" + "|".join(map(re.escape, NOMI_DI_CLASSE)) + r")\w*\.?\s*(\d{1,2})\b", re.I)


def classe(nome: str) -> "tuple[int, tuple, float] | None":
    """(dado dei DV, TS buoni, BAB per livello) di una classe, o None se non e' SRD."""
    n = nome.lower()
    n = ABBREVIAZIONI.get(n, n)
    if n in PRESTIGIO:
        return PRESTIGIO[n]
    if n in T.CLASSI:
        dado, buoni = T.CLASSI[n]
        return dado, buoni, T.BAB_CLASSE.get(n, 0.75)
    return None


@dataclass
class Gruppo:
    """Un gruppo di dadi vita: una classe, o i DV razziali del tipo."""
    nome: str
    n: int
    dado: int
    buoni: tuple
    bab: float


def ts_base_di(n: int, buoni) -> "dict[str, int]":
    """La base dei TS di **un** gruppo di `n` DV: buono 2 + n/2, cattivo n/3."""
    return {k: T.ts_buono(n) if k in buoni else T.ts_cattivo(n) for k in TS}


def ts_base(gruppi: "list[Gruppo]") -> "tuple[dict[str, int], dict[str, int]]":
    """(minimo, massimo) della base dei TS, sommata sui gruppi.

    I DV razziali dell'**umanoide** hanno un TS buono che «varia» (SRD, e la
    skill `dnd-35-srd` lo scrive cosi'): lo gnoll ha buona la Tempra, il
    bugbear i Riflessi. Per quei DV il minimo li conta tutti cattivi e il
    massimo tutti buoni; per gli altri gruppi minimo e massimo coincidono.
    """
    lo = dict.fromkeys(TS, 0)
    hi = dict(lo)
    for g in gruppi:
        if g.nome == "humanoid":
            tutti_cattivi, tutti_buoni = ts_base_di(g.n, ()), ts_base_di(g.n, TS)
        else:
            tutti_cattivi = tutti_buoni = ts_base_di(g.n, g.buoni)
        for k in TS:
            lo[k] += tutti_cattivi[k]
            hi[k] += tutti_buoni[k]
    return lo, hi


def bab_atteso(gruppi: "list[Gruppo]") -> int:
    """La somma dei BAB di classe e di tipo, ciascuno arrotondato in basso (SRD)."""
    return sum(math.floor(g.n * g.bab) for g in gruppi)
