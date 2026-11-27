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

from functools import cache as _cache

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





_PIGRE = ("PRESTIGIO", "DADO_DI_CLASSE", "NOMI_DI_CLASSE", "CLASSE_LIVELLO", "MANUALI")


def manuale_affidabile(v: dict) -> bool:
    """Una classe dei manuali i cui numeri si possono usare per un conto."""
    return ({"dv", "bab", "ts_buoni"} <= set(v) and not v.get("diverge")
            and not v.get("ts_medi") and not v.get("bab_irregolare"))


@_cache
def _derivate() -> dict:
    """Le costanti che vengono dai dati di un sistema, lette alla prima richiesta
    e non all'import (F2 di ADR-0112)."""
    #: Le due classi di prestigio SRD che compaiono nel Bestiario e non stanno in
    #: `dmcore.tabelle`: (dado dei DV, TS buoni, BAB per livello).
    #: Stanno in `[prestigio]` del plugin dnd35 (ADR-0111, L5b).
    PRESTIGIO = {k: (v["dv"], tuple(v["ts_buoni"]), v["bab"])
                 for k, v in T._DATI["prestigio"].items()}
    MANUALI: set = set()
    #: Le classi dei manuali 3.5 fuori SRD (`classi_manuali.toml`, ADR-0124 §8):
    #: entrano solo quelle con dado, BAB e tiri salvezza regolari e su cui le
    #: fonti non divergono; un nome dell'SRD vince sempre. Le altre restano
    #: sconosciute, cioè «non verificabili» per chi controlla.
    for k, v in T._DATI.get("classi_manuali", {}).items():
        # «Red Wizard 7», «Sun Soul Monk 3»: finché il nome finisce con una classe
        # dell'SRD la scheda si legge come prima (quella classe), per non cambiare
        # il livello d'incantatore delle schede che già si leggevano.
        if k.split()[-1] in T.CLASSI and " " in k:
            continue
        if k not in PRESTIGIO and k not in T.CLASSI and manuale_affidabile(v):
            PRESTIGIO[k] = (v["dv"], tuple(v["ts_buoni"]), v["bab"])
            MANUALI.add(k)
            if v.get("it") and v["it"] not in PRESTIGIO and v["it"] not in T.CLASSI:
                PRESTIGIO[v["it"]] = PRESTIGIO[k]   # «Berserker Furioso» = Frenzied Berserker
                MANUALI.add(v["it"])
    #: Il dado dei DV per ogni nome con cui una scheda scrive una classe.
    DADO_DI_CLASSE = {**{n: d for n, (d, _) in T.CLASSI.items()},
                      **{n: v[0] for n, v in PRESTIGIO.items()},
                      **{a: T.CLASSI[n][0] for a, n in ABBREVIAZIONI.items()}}
    NOMI_DI_CLASSE = sorted(set(T.CLASSI) | set(PRESTIGIO) | set(ABBREVIAZIONI),
                            key=len, reverse=True)
    #: «Fighter 3», «Clr. 5», «Guerriero 4»: una classe e il suo livello.
    # I nomi dell'SRD valgono anche da radice («Guerrier-a», «Clr.»); quelli dei
    # manuali solo interi: «tempest» non è «tempeste».
    CLASSE_LIVELLO = re.compile(
        r"\b(" + "|".join(re.escape(n) + (r"(?!\w)" if n in MANUALI else "") for n in NOMI_DI_CLASSE)
        + r")\w*\.?\s*(\d{1,2})\b", re.I)
    luogo = locals()
    return {n: luogo[n] for n in _PIGRE}


def __getattr__(nome: str):
    if nome in _PIGRE:
        return _derivate()[nome]
    raise AttributeError(f"module {__name__!r} has no attribute {nome!r}")



def classe(nome: str) -> "tuple[int, tuple, float] | None":
    """(dado dei DV, TS buoni, BAB per livello) di una classe, o None se non e' SRD."""
    n = nome.lower()
    n = ABBREVIAZIONI.get(n, n)
    if n in _derivate()["PRESTIGIO"]:
        return _derivate()["PRESTIGIO"][n]
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
