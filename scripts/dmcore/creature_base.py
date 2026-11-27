"""dmcore.creature_base — la creatura base di una scheda (ADR-0126, lotto 5).

Un «Ogre + Barbaro 6» porta con sé i numeri dell'ogre: i dadi vita razziali,
l'armatura naturale, il dado degli attacchi naturali. I dati sono quelli dei
blocchi di statistiche dell'SRD (capacità `creature.base` del plugin).

La creatura base non si indovina dal nome della scheda: si legge solo dove la
scheda la **dichiara** come fonte («SRD *Ogre* + …», «MM p.33 Centaur + …»).
Un archetipo (scheletro, immondo, mezzo-drago…) cambia taglia, dadi e attacchi:
con un archetipo dichiarato la base non si usa e il giudizio resta al DM.
"""
from __future__ import annotations

import functools
import re

from dmcore import sistemi as S

__all__ = ["tabella", "creatura", "dichiarata", "drago", "attacco_naturale"]

#: dopo queste parole la fonte nomina la creatura: «SRD», «MM», «MM p.33», «Monster Manual»
_PRIMA = r"(?:\bsrd(?:\s+3\.5)?|\bmm(?:\s+i)?|\bmonster manual(?:\s+i)?)(?:\s+p\.?\s*\d+)?\s*[:,]?\s*(?:\(\s*)?(?:base\s+)?[*_]{0,2}"
_ARCHETIPO = re.compile(
    r"template|archetipo|skeleton|scheletr|zombi|fiendish|immond|celestial|half-|mezzo-|mezz[oa] |ghost|"
    r"spettral|vampir|lich|lycanthrop|licantrop|were\w+|mannar|advanced|avanzat|innest|graft|pseudonatural", re.I)
#: i modelli dell'SRD che lasciano dadi vita, armatura naturale e attacchi della base come sono
#: (celestial-creature.md e fiendish-creature.md: cambiano qualità speciali, tipo e grado di sfida)
_SENZA_NUMERI = re.compile(r"(?<!half-)(?<!mezzo-)(?<!mezzo )(?<!mezza )\b(?:celestial[ei]?|fiendish|immond[oaie])\b", re.I)
#: il nome italiano o inglese dell'attacco nella scheda → il nome nell'SRD
_ATTACCHI = (
    (r"\bmors[oi]\b|\bbite\b|\bzann[ae]\b", ("bite",)),
    (r"\bartigli[oe]?\b|\bclaws?\b", ("claw", "talon", "foreclaw")),
    (r"\bschiant[oi]\b|\bslam\b", ("slam",)),
    (r"\bincornata\b|\bgore\b|\bcorn[ao]\b", ("gore", "horn", "butt")),
    (r"\bpungiglione\b|\bsting\b", ("sting",)),
    (r"\btentacol[oi]\b|\btentacles?\b", ("tentacle",)),
    (r"\bzoccol[oi]\b|\bhoo(?:f|ves)\b", ("hoof",)),
    (r"\bal[ai]\b|\bwings?\b|colpo d'ala", ("wing",)),
    (r"\bschiacciament[oi]\b|\bschiacciare\b|\bcrush\b", ("crush",)),
    (r"spazzata|tail sweep", ("tail sweep",)),
    (r"\bcoda\b|\btail\b", ("tail slap", "tail")),
)


@functools.cache
def tabella(sistema: str = "dnd35") -> dict:
    """Le creature base del `sistema` (capacità `creature.base`); vuota se il sistema non l'ha."""
    try:
        return S.dati(sistema, "creature.base").get("creature_base", {})
    except S.ErroreSistemi:
        return {}


@functools.cache
def _nomi(sistema: str) -> "tuple[tuple[str, str], ...]":
    """(come si scrive, chiave) dal nome più lungo: «bear, black» vale anche «black bear»."""
    out = {}
    for k in tabella(sistema):
        out[k] = k
        if ", " in k:
            a, b = k.split(", ", 1)
            out.setdefault(f"{b} {a}", k)
    try:  # i nomi italiani o scritti diversamente dall'SRD («gufo gigante», «hell hound»)
        altri = (S.dati(sistema, "creature.costruzione").get("gs") or {}).get("nomi_base") or {}
    except S.ErroreSistemi:
        altri = {}
    for scritto, k in altri.items():
        if k in out:
            out.setdefault(scritto, k)
    return tuple(sorted(out.items(), key=lambda kv: -len(kv[0])))


def creatura(nome: str, sistema: str = "dnd35") -> "dict | None":
    return tabella(sistema).get((nome or "").strip().lower())


def dichiarata(fonte: str, sistema: str = "dnd35", col_modello: bool = False) -> "tuple[str, dict] | None":
    """La creatura base che la riga `fonte` dichiara, o None.

    None anche quando la fonte nomina un archetipo: la base c'è, ma i suoi
    numeri non valgono più così come sono. `col_modello` la rende lo stesso:
    serve a chi sa applicare il modello sopra quei numeri."""
    testo = _SENZA_NUMERI.sub(" ", (fonte or "").lower())
    if not testo.strip() or (_ARCHETIPO.search(testo) and not col_modello):
        return None
    for scritto, chiave in _nomi(sistema):
        if re.search(_PRIMA + re.escape(scritto) + r"s?\b", testo):
            return chiave, tabella(sistema)[chiave]
    return None


_COLORE_EN = r"(?:red|blue|green|black|white|brass|bronze|copper|gold|silver)"
_COLORE_IT = r"(?:ross[oa]|blu|azzurr[oa]|verde|ner[oa]|bianc[oa]|d'ottone|di bronzo|di rame|d'oro|d'argento)"
#: il colore sta accanto alla parola: «drago rosso», «red dragon», «drago vecchio blu»
_DRAGO_VERO = re.compile(
    rf"\b{_COLORE_EN}\s+(?:\w+\s+){{0,2}}dragon\b|\b(?:drago|dragonessa|dragone)\s+(?:\w+\s+)?{_COLORE_IT}(?![\w'])|"
    rf"\bdragon\s*\(\s*{_COLORE_EN}\b", re.I)


#: le dodici categorie d'età dei draghi veri, dalla più lunga: «giovane adulto» prima di «adulto»
_ETA_DRAGO = (
    ("great wyrm", r"great wyrm|grande dragone"), ("wyrmling", r"wyrmling|cucciol[oa]"), ("wyrm", r"wyrm"),
    ("ancient", r"ancient|antic[oa]"), ("very old", r"very old|molto vecchi[oa]"),
    ("mature adult", r"mature adult|adult[oa] matur[oa]"), ("young adult", r"young adult|giovane adult[oa]"),
    ("very young", r"very young|molto giovane"), ("old", r"old|vecchi[oa]"), ("adult", r"adult|adult[oa]"),
    ("juvenile", r"juvenile|adolescente"), ("young", r"young|giovane"),
)
_COLORI = (("red", r"red|ross[oa]"), ("blue", r"blue|blu|azzurr[oa]"), ("green", r"green|verde"),
           ("black", r"black|ner[oa]"), ("white", r"white|bianc[oa]"), ("brass", r"brass|d'ottone"),
           ("bronze", r"bronze|di bronzo"), ("copper", r"copper|di rame"), ("gold", r"gold|d'oro"),
           ("silver", r"silver|d'argento"))


def eta_del_drago(testo: str, sistema: str = "dnd35") -> "tuple[str, str, dict] | None":
    """(colore, età, voce) del drago vero che il `testo` dichiara con colore e categoria d'età
    («Drago Rosso (Young Adult)», «Blue Old Dragon»), o None se manca una delle due."""
    try:
        per_eta = S.dati(sistema, "creature.base").get("draghi_eta", {})
    except S.ErroreSistemi:
        return None
    vero = _DRAGO_VERO.search(testo or "")
    if not vero or not per_eta:
        return None
    colore = next((c for c, schema in _COLORI if re.search(rf"(?<![\w'])(?:{schema})(?![\w'])", vero.group(0), re.I)), None)
    eta = next((e for e, schema in _ETA_DRAGO if re.search(rf"(?<!\w)(?:{schema})(?!\w)", testo, re.I)), None)
    if not colore or not eta or eta not in per_eta.get(colore, {}):
        return None
    return colore, eta, per_eta[colore][eta]


def drago(testo: str, taglia: "str | None", sistema: str = "dnd35") -> "tuple[str, dict] | None":
    """La «base» di un drago vero di quella `taglia`: gli attacchi naturali, che per i draghi
    cromatici e metallici vengono dalla taglia. Se il `testo` dice anche la categoria d'età e la
    taglia è quella dell'età, la base porta dadi vita, armatura naturale, caratteristiche e grado
    di sfida di quel drago. Viverne, draghi tartaruga e mezzi-draghi sono di tipo drago ma hanno
    i loro dadi: senza un colore nel `testo` non si usa."""
    try:
        per_taglia = S.dati(sistema, "creature.base").get("draghi", {})
    except S.ErroreSistemi:
        return None
    if not taglia or taglia not in per_taglia or not _DRAGO_VERO.search(testo or ""):
        return None
    voce = {"taglia": taglia, "tipo": "dragon", "attacchi": per_taglia[taglia]}
    quale = eta_del_drago(testo, sistema)
    if quale and quale[2]["taglia"] == taglia:
        colore, eta, dati = quale
        return f"{eta} {colore} dragon", dict(voce, dado=12, drago=True, **{k: dati[k] for k in ("dv", "naturale", "car", "gs")})
    return f"drago {taglia}", voce


def attacco_naturale(nome: str, base: dict) -> "dict | None":
    """L'attacco naturale della `base` che il `nome` scritto nella scheda indica."""
    attacchi = base.get("attacchi") or {}
    for schema, chiavi in _ATTACCHI:
        if re.search(schema, nome, re.I):
            return next((dict(attacchi[k], nome=k) for k in chiavi if k in attacchi), None)
    return None
