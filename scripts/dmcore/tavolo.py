"""
tavolo — quello che il repo sa già del gruppo, e che gli strumenti chiedevano
a mano (rilievo del DM, 2026-09-03).

`campaign/state.md` dichiara nell'intestazione il livello medio del gruppo:

    **Party APL:** 13 (ARC-07 D8 — livello reale già raggiunto durante l'Arco 07)

È prosa del DM, fuori dalle regioni ``auto:``, quindi nessuno script la
sovrascrive: è la dichiarazione di chi ha l'autorità per farla. Eppure
`suggest_encounter` pretendeva `--el` a ogni chiamata e `suggest_loot`, quando
non trovava un EL, ripiegava su un **10 scritto nel codice**. Il numero c'era e
nessuno lo leggeva.

⚠️ **APL non è EL, e questo modulo non finge il contrario.** Un incontro di EL
pari all'APL è lo scontro «medio» del manuale: quello che consuma un quarto
delle risorse e che nessuno ricorda. Il boss di fine arco sta tre o quattro
gradini sopra. Quello che si trova qui è un **punto di partenza dichiarato**,
buono per la domanda «cosa metto davanti al gruppo stasera», non la scelta di
regia — quella resta `--el`.

Per questo `origine_el()` restituisce anche **da dove** viene il numero, e i
chiamanti lo stampano: un default silenzioso è come ci si era arrivati.

Solo stdlib.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

from . import REPO

__all__ = ["APL_RE", "Origine", "leggi_apl", "origine_el"]

#: `**Party APL:** 13 (…)` — il numero, ignorando la parentesi di contesto.
APL_RE = re.compile(r"^\*\*Party APL:\*\*\s*(\d+(?:[.,]\d+)?)", re.MULTILINE)

STATE = REPO / "campaign" / "state.md"


class Origine(NamedTuple):
    """Un EL e la ragione per cui è quello.

    `etichetta` è pensata per finire in un output che il DM legge: se il
    numero non è quello che si aspettava, deve poter capire perché senza
    aprire il codice.
    """

    el: float
    etichetta: str


def leggi_apl(state: Path | None = None) -> float | None:
    """Il `Party APL` dichiarato in `state.md`, o `None` se non c'è.

    Non alza: un repo appena clonato, o uno state.md ancora da compilare, sono
    casi normali e chi chiama ha un livello sotto a cui scendere.
    """
    percorso = state or STATE
    try:
        testo = percorso.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    m = APL_RE.search(testo)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", "."))
    except ValueError:  # pragma: no cover — la regex non lo permette
        return None


def origine_el(esplicito: float | None = None,
               dal_file: float | None = None,
               state: Path | None = None) -> Origine | None:
    """Da dove viene l'EL, in ordine di autorità decrescente.

    1. `esplicito` — l'ha scritto il DM sulla riga di comando, e vince sempre;
    2. `dal_file` — il ``**Combined EL**`` di un output di `suggest_encounter`,
       cioè un numero calcolato sui mostri veri di quello scontro;
    3. il `Party APL` di `state.md`, che è un punto di partenza, non una scelta;
    4. `None` — e allora chi chiama deve rifiutare, non inventare.

    Il quarto caso esiste perché sia un rifiuto e non un numero: era il difetto.
    """
    if esplicito is not None:
        return Origine(float(esplicito), "da --el")
    if dal_file is not None:
        return Origine(float(dal_file), "dal file di incontro")
    apl = leggi_apl(state)
    if apl is not None:
        return Origine(apl, "Party APL da campaign/state.md — è un punto di "
                            "partenza, non la scelta di regia: usa --el per un boss")
    return None
