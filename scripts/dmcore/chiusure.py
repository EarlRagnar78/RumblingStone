"""
chiusure — l'asse di una porta, di una grata o di una fila di sbarre, ricavato
dai quattro vicini (ADR-0083).

Una porta disegnata in una griglia emoji non dice in che verso sta: lo dice il
muro intorno. Muri (o il bordo, o un'altra chiusura) a ovest e a est, e un
passaggio a nord o a sud, vogliono una porta in un muro **est-ovest**: si
attraversa andando da nord a sud. Il caso ruotato di 90° è un muro
**nord-sud**. Quando le due letture valgono entrambe, decide da che parti si
passa davvero; quando non decide neanche quello, l'asse è ambiguo e il DM lo
scrive con ``@verso``.

Prima di questo modulo la stessa domanda aveva tre risposte, e tutte diverse:
``collaudo_mappe`` calcolava l'asse e lo buttava via, ``export_uvtt`` usava
«muro sopra *o* sotto» (13 portali su 96 girati di traverso in Foundry, misura
del 2026-10-08), il renderer non se la poneva e disegnava ogni porta nello
stesso verso (36 su 96 di traverso). Adesso c'è una risposta, e i tre la
leggono.

L'idea viene dalle regole di terreno di *Battle for Wesnoth*, che scelgono la
variante di un muro o di un cancello guardando le tessere vicine. Non c'è
codice né arte di Wesnoth qui: l'algoritmo è scritto dalla descrizione, per
una griglia quadrata.

Solo stdlib. Legge le funzioni dei simboli da ``legend.json`` (ADR-0048).
"""

from __future__ import annotations

import re
from typing import Callable, Optional

from . import legenda

EO = "EO"   # la chiusura sta in un muro est-ovest: il glifo come è disegnato
NS = "NS"   # la chiusura sta in un muro nord-sud: il glifo ruotato di 90°
AMBIGUO = "?"

POSE = ("nel_muro", "recinto")

_VERSI = {"EO": EO, "OE": EO, "EST-OVEST": EO, "NS": NS, "SN": NS, "NORD-SUD": NS}
_CELLA = re.compile(r"^([A-Za-z]{1,2})(\d{1,3})$")


def _n(c: Optional[str]) -> Optional[str]:
    return c.replace("️", "") if c else c


def _funzioni() -> dict[str, dict]:
    return {s: v.get("function", {}) for s, v in legenda._dati()["symbols"].items()}


def e_chiusura(c: Optional[str]) -> bool:
    """Porta, grata, finestra, sbarre: una tessera che ha un verso."""
    return _funzioni().get(_n(c) or "", {}).get("posa") in POSE


def _linea(c: Optional[str]) -> bool:
    """Continua il muro: il bordo, la muratura vera, o un'altra chiusura."""
    if c is None:
        return True
    f = _funzioni().get(_n(c), {})
    if f.get("posa") in POSE:
        return True
    return bool(f.get("blocks_movement")) and bool(f.get("blocks_sight")) and not f.get("door")


def _passa(c: Optional[str]) -> bool:
    if c is None:
        return False
    f = _funzioni().get(_n(c), {})
    return not f.get("blocks_movement") or bool(f.get("door"))


def asse(at: Callable[[int, int], Optional[str]], x: int, y: int) -> Optional[str]:
    """``EO``, ``NS``, ``AMBIGUO`` o ``None`` (nessun muro intorno).

    ``at(x, y)`` restituisce il simbolo della cella, ``None`` fuori dalla
    griglia: il bordo vale come muro, come in ``collaudo_mappe``.
    """
    w, e, n, s = at(x - 1, y), at(x + 1, y), at(x, y - 1), at(x, y + 1)
    eo = _linea(w) and _linea(e) and (_passa(n) or _passa(s))
    ns = _linea(n) and _linea(s) and (_passa(w) or _passa(e))
    if eo and not ns:
        return EO
    if ns and not eo:
        return NS
    if eo and ns:
        da_nord_a_sud = _passa(n) and _passa(s)
        da_ovest_a_est = _passa(w) and _passa(e)
        if da_nord_a_sud and not da_ovest_a_est:
            return EO
        if da_ovest_a_est and not da_nord_a_sud:
            return NS
        return AMBIGUO
    return None


def versi_dichiarati(annotazioni: list[str]) -> dict[tuple[str, int], str]:
    """Le direttive ``@verso <A1> ; NS|EO``, come {(colonna, riga stampata): asse}.

    Una direttiva con un verso che non si legge vale come assente: il collaudo
    lo dice (``posa/verso-illeggibile``), il renderer la ignora.
    """
    fuori: dict[tuple[str, int], str] = {}
    for riga in annotazioni or []:
        s = riga.strip()
        if not s.lower().startswith("@verso"):
            continue
        parti = [p.strip() for p in s[len("@verso"):].split(";")]
        if len(parti) < 2:
            continue
        m = _CELLA.match(parti[0])
        verso = _VERSI.get(parti[1].upper().replace(" ", ""))
        if m and verso:
            fuori[(m.group(1).upper(), int(m.group(2)))] = verso
    return fuori


def verso_illeggibile(annotazioni: list[str]) -> list[str]:
    """Le righe ``@verso`` che ``versi_dichiarati`` scarta, per il collaudo."""
    cattive = []
    for riga in annotazioni or []:
        s = riga.strip()
        if not s.lower().startswith("@verso"):
            continue
        parti = [p.strip() for p in s[len("@verso"):].split(";")]
        if (len(parti) < 2 or not _CELLA.match(parti[0])
                or parti[1].upper().replace(" ", "") not in _VERSI):
            cattive.append(s)
    return cattive


def asse_da_disegnare(at, x: int, y: int, colonna: str, riga: int,
                      dichiarati: dict[tuple[str, int], str]) -> str:
    """L'asse con cui il renderer e l'export disegnano: la direttiva vince,
    poi i vicini; un caso che resta aperto si disegna come oggi, ``EO``."""
    if (colonna.upper(), riga) in dichiarati:
        return dichiarati[(colonna.upper(), riga)]
    a = asse(at, x, y)
    return a if a in (EO, NS) else EO
