"""dmcore.classe_armatura — la CA di una scheda 3.5 ricostruita dalle sue voci (ADR-0126, lotto 1-bis).

SRD 3.5, «Armor Class»: 10 + armatura + scudo + Des + taglia + naturale +
deviazione + schivare. Due bonus dello stesso tipo non si sommano (`dmcore.bonus`
dice quali sì): un'armatura e i bracciali dell'armatura valgono il più alto.

`leggi(dettaglio)` trasforma la parentesi della CA in voci col tipo;
`giudica(...)` confronta la CA scritta, il contatto e il colto alla sprovvista
con il conto, e ogni voce d'armatura o di scudo con la tabella del plugin
(`creature.costruzione`: bonus base più potenziamento, Des massima).

Quello che il lettore non riconosce non diventa un numero inventato: la voce
resta «ignota» e la CA della scheda è non verificabile, col motivo.
"""
from __future__ import annotations

import functools
import re
from dataclasses import dataclass

from dmcore import sistemi as S

__all__ = ["VoceCA", "tabelle", "leggi", "somma", "giudica"]

#: I tipi che si sommano fra loro; degli altri vale il più alto.
SI_SOMMANO = frozenset({"des", "taglia", "schivare", "senza_tipo", "armatura_in_piu", "scudo_in_piu",
                        "naturale_in_piu"})
#: I tipi che non contano per la CA di contatto (SRD, «Touch Attacks»).
NON_A_CONTATTO = frozenset({"armatura", "scudo", "naturale", "potenziamento_naturale",
                            "armatura_in_piu", "scudo_in_piu", "naturale_in_piu"})

_NUM = re.compile(r"[+\-−]\s*\d+")
_CONDIZIONE = re.compile(r"(?<!\w)(?:vs|contro|against|quando|solo|se)(?!\w)", re.I)
#: Nomi che le schede usano e la tabella del plugin non ha, col nome della tabella.
_ALIAS = {
    "studded": "studded leather", "large shield": "heavy shield",
    "mithral chain": "chain shirt", "camicia di mithral": "camicia di maglia",
    "piastre complete": "armatura completa", "pelle": "armatura di pelle",
    "giaco di cuoio borchiato": "cuoio borchiato", "mezza armatura": "half-plate",
    "heavy steel shield": "heavy shield", "heavy wooden shield": "heavy shield",
    "light steel shield": "light shield", "light wooden shield": "light shield",
}
#: «scudo» e «shield» da soli non dicono se leggero (+1) o pesante (+2).
_GENERICI = frozenset({"shield", "scudo"})
#: Armature con un nome che la tabella non ha: non si indovinano dal pezzo di nome che c'è.
_FUORI_TABELLA = re.compile(r"\b(?:rinforzat[oa]|reinforced)\b", re.I)
_MITHRAL = re.compile(r"\bmithr[ai]l\b", re.I)
_REGOLE = (  # (schema, tipo): la prima che corrisponde decide
    (re.compile(r"\b(?:taglia|size)\b", re.I), "taglia"),
    (re.compile(r"\b(?:amuleto|amulet|pelle coriacea|barkskin)\b", re.I), "potenziamento_naturale"),
    (re.compile(r"\bnatural\w*\s+(?:migliorata|improved)|improved natural", re.I), "naturale_in_piu"),
    (re.compile(r"\bnatural", re.I), "naturale"),
    (re.compile(r"\b(?:deflessione|deviazione|deflect\w*|anello|ring)\b", re.I), "deviazione"),
    (re.compile(r"\b(?:schivare|dodge)\b", re.I), "schivare"),
    (re.compile(r"\b(?:ottimizzazione delle armature|armor optimization)", re.I), "armatura_in_piu"),
    (re.compile(r"\b(?:specializzazione nello scudo|shield specialization)", re.I), "scudo_in_piu"),
    (re.compile(r"\b(?:sag|wis|monaco|monk)\b", re.I), "senza_tipo"),
)
_INCANTESIMO_SCUDO = re.compile(r"\bscudo\b.*\*|\bshield\b.*\*", re.I)
_ARMATURA_GENERICA = re.compile(r"\b(?:armatura|armor|bracciali|bracers|tuta)\b", re.I)
_DES = re.compile(r"\b(?:des|dex)\b", re.I)
#: Le voci si separano con virgole e punti e virgola, o davanti a un numero seguito dal suo tipo
#: («10 +1 naturale +2 Des», senza virgole).
_TAGLIO = re.compile(r"[,;]|(?<=\w)\s+(?=[+\-]\s*\d+\s+(?:des|dex|natural\w*|taglia|size|deflessione|deviazione)\b)", re.I)
#: «cotta di maglia + Des»: la Destrezza è nominata senza numero.
_DES_SENZA_NUMERO = re.compile(r"\+\s*(?:des|dex)\b", re.I)


@dataclass(frozen=True)
class VoceCA:
    valore: "int | None"       # None: la voce c'è ma il lettore non ne ricava un numero
    tipo: str                  # armatura, scudo, des, taglia, naturale, … oppure «ignota»
    testo: str
    atteso: "int | None" = None    # per armature e scudi: base della tabella più potenziamento
    des_max: "int | None" = None
    oppure: "int | None" = None   # «scudo pesante +2»: il +2 può essere il totale, non il potenziamento


@functools.lru_cache(maxsize=None)
def tabelle(sistema: str = "dnd35") -> "tuple[dict, dict]":
    d = S.dati(sistema, "creature.costruzione")
    armature = {k.lower(): (v["ca"], v["des_max"]) for k, v in d["armature"].items()}
    scudi = {k.lower(): (v, None) for k, v in d["scudi"].items()}
    for alias, vero in _ALIAS.items():
        for t in (armature, scudi):
            if vero in t:
                t.setdefault(alias, t[vero])
    return armature, scudi


def _int(s: str) -> int:
    return int(s.replace("−", "-").replace(" ", ""))


def _oggetto(clausola: str, tabella: dict) -> "tuple[str, int, int | None, int, int] | None":
    """(nome, base, des_max, inizio, fine) dell'oggetto col nome più lungo, a parola intera."""
    basso = clausola.lower()
    for nome in sorted(tabella, key=len, reverse=True):
        m = re.search(rf"(?<![\w]){re.escape(nome)}(?![\w])", basso)
        if m:
            return nome, tabella[nome][0], tabella[nome][1], m.start(), m.end()
    return None


def _voce_oggetto(clausola: str, tipo: str, trovato) -> VoceCA:
    nome, base, des_max, inizio, fine = trovato
    prima = [_int(n) for n in _NUM.findall(clausola[:inizio])]
    dopo = [_int(n) for n in _NUM.findall(clausola[fine:])]
    # «+8 +1 full plate»: totale dichiarato e potenziamento; «+6 giaco +2»: lo stesso;
    # «armatura completa +1»: solo il potenziamento; «+5 breastplate»: solo il totale
    scritto = prima[0] if prima else None
    pot = prima[1] if len(prima) > 1 else (dopo[0] if dopo else 0)
    if des_max is not None and _MITHRAL.search(clausola):
        des_max += 2            # SRD, Special Materials, mithral: Des massima +2
    atteso = base + pot
    forse_base = scritto == base and len(prima) == 1 and bool(dopo) and pot > 0
    if nome in _GENERICI and scritto is not None and scritto - pot in (1, 2):
        atteso = scritto        # «+1 shield»: leggero o pesante, la scheda non lo dice
    # due letture lecite, che il conto della CA decide: «scudo pesante +2» (potenziamento o
    # totale) e «+5 corazza di piastre +1» (il primo numero è il totale o la base)
    oppure = base if (scritto is None and not prima and dopo and dopo[0] == base) else (
        atteso if forse_base else None)
    return VoceCA(scritto if scritto is not None else atteso, tipo, clausola.strip(), atteso, des_max, oppure)


def leggi(dettaglio: str, sistema: str = "dnd35") -> "list[VoceCA]":
    """Le voci della prima parentesi di `ca-dettaglio` che elenca dei bonus."""
    armature, scudi = tabelle(sistema)
    testo = (dettaglio or "").replace("−", "-")
    testo = re.sub(r"\[[^\]]*\]", "", testo)                 # «[+5 base, +2 corteccia]»: è il dettaglio di una voce
    fuori: "list[VoceCA]" = []
    for dentro in re.findall(r"\(([^()]*)\)", testo):
        voci = []
        for clausola in re.split(_TAGLIO, dentro):
            c = clausola.strip()
            if not c:
                continue
            numeri = [_int(n) for n in _NUM.findall(c)]
            if numeri and _CONDIZIONE.search(c):
                continue                                      # «+1 vs trappole»: a condizione
            if "*" in c and numeri:                           # un incantesimo: vale quanto scrive
                tipo = ("scudo" if _INCANTESIMO_SCUDO.search(c) else
                        next((t for r, t in _REGOLE if r.search(c)), "armatura"))
                voci.append(VoceCA(numeri[0], tipo, c))
                continue
            if _DES.search(c) and not _oggetto(c, armature):
                if numeri or re.fullmatch(r"\+?\s*(?:des|dex)", c, re.I):
                    voci.append(VoceCA(numeri[0] if numeri else None, "des", c))
                continue
            regola = next((t for r, t in _REGOLE if r.search(c)), None)
            if regola:
                if numeri:
                    voci.append(VoceCA(numeri[0], regola, c))
                continue                                      # «schivare prodigioso»: non è un numero
            scudo, armatura = _oggetto(c, scudi), _oggetto(c, armature)
            if _FUORI_TABELLA.search(c):
                scudo = armatura = None
            if scudo:
                voci.append(_voce_oggetto(c, "scudo", scudo))
            elif armatura:
                senza = _DES_SENZA_NUMERO.sub("", c)
                voci.append(_voce_oggetto(senza, "armatura", armatura))
                if senza != c:
                    voci.append(VoceCA(None, "des", "Des"))
            elif numeri and _ARMATURA_GENERICA.search(c):
                voci.append(VoceCA(numeri[0], "armatura", c))
            elif numeri:
                voci.append(VoceCA(None, "ignota", c))
        if any(v.valore is not None or v.tipo == "ignota" for v in voci):
            fuori += voci
            break
    return fuori


def somma(voci: "list[VoceCA]", esclusi: frozenset = frozenset()) -> "tuple[int, list[VoceCA]]":
    """(totale dei bonus, voci scartate perché dello stesso tipo di una più alta)."""
    totale, migliore, scartate = 0, {}, []
    for v in voci:
        if v.valore is None or v.tipo in esclusi:
            continue
        if v.tipo in SI_SOMMANO:
            totale += v.valore
        elif v.tipo not in migliore or v.valore > migliore[v.tipo].valore:
            if v.tipo in migliore:
                scartate.append(migliore[v.tipo])
            migliore[v.tipo] = v
        else:
            scartate.append(v)
    return totale + sum(v.valore for v in migliore.values()), scartate


_CONTATTO = re.compile(r"\b(?:contatto|touch)\s+(\d+)", re.I)
_SPROVVISTA = re.compile(r"\b(?:sprovvista|flat-footed|ff)\s+(\d+)", re.I)
_SCHIVARE_PRODIGIOSO = re.compile(r"schivare prodigioso|uncanny dodge|mai colto alla sprovvista", re.I)


def giudica(ca: "int | None", dettaglio: str, mod_des: "int | None" = None, testo: str = "",
            sistema: str = "dnd35") -> "tuple[list[dict], list[dict]]":
    """(scarti, non verificabili). Ogni scarto: campo, scritto, atteso, nota."""
    scarti, nv = [], []
    if ca is None:
        return scarti, nv
    voci = leggi(dettaglio, sistema)
    if not voci:
        nv.append({"campo": "CA", "nota": "la scheda non elenca le voci della CA: il conto non parte"})
        return scarti, nv
    for v in voci:
        if v.atteso is not None and v.valore != v.atteso and v.oppure is None:
            scarti.append({"campo": f"CA.{v.tipo}", "scritto": v.valore, "atteso": v.atteso,
                           "nota": f"«{v.testo}»: bonus base della tabella più il potenziamento"})
    if not any(_NUM.search(v.testo) for v in voci):
        nv.append({"campo": "CA", "nota": "la parentesi nomina gli oggetti senza i bonus: non è un conto della CA"})
        return [], nv
    ignote = [v.testo for v in voci if v.tipo == "ignota"]
    if ignote:
        nv.append({"campo": "CA", "nota": "voci che il lettore non riconosce: " + "; ".join(ignote)})
        return scarti, nv
    tetto = min((v.des_max for v in voci if v.des_max is not None), default=None)
    lecito = None if mod_des is None else (mod_des if tetto is None else min(mod_des, tetto))
    # la Destrezza nominata senza numero («cotta di maglia + Des») vale il modificatore lecito
    voci = [VoceCA(lecito, v.tipo, v.testo) if (v.tipo == "des" and v.valore is None) else v for v in voci]
    if any(v.tipo == "des" and v.valore is None for v in voci):
        nv.append({"campo": "CA", "nota": "Destrezza nominata senza numero e caratteristiche non leggibili"})
        return scarti, nv
    totale, scartate = somma(voci)
    # «scudo pesante +2»: se il numero è il bonus base, può essere il totale e non il potenziamento
    letture = [totale]
    ambigue = [v for v in voci if v.oppure is not None]
    if ambigue:
        letture.append(somma([VoceCA(v.oppure, v.tipo, v.testo) if v.oppure is not None else v for v in voci])[0])
    come = ", ".join(f"{v.valore:+d} {v.tipo.replace('_', ' ')}" for v in voci if v.valore is not None)
    if scartate:
        come += "; non si sommano: " + ", ".join(f"{v.valore:+d} {v.tipo} ({v.testo})" for v in scartate)
    if ca not in [10 + t for t in letture]:
        scarti.append({"campo": "CA", "scritto": ca, "atteso": 10 + totale, "nota": "10 " + come})
    elif ca != 10 + totale:
        voci = [VoceCA(v.oppure, v.tipo, v.testo) if v.oppure is not None else v for v in voci]
    else:
        for v in ambigue:
            if v.valore != v.atteso:     # la CA torna col primo numero come totale: manca il potenziamento
                scarti.append({"campo": f"CA.{v.tipo}", "scritto": v.valore, "atteso": v.atteso,
                               "nota": f"«{v.testo}»: bonus base della tabella più il potenziamento"})
    des = [v for v in voci if v.tipo == "des"]
    if des and lecito is not None and des[0].valore > lecito:
        scarti.append({"campo": "CA.des", "scritto": des[0].valore, "atteso": lecito,
                       "nota": f"modificatore di Destrezza {mod_des:+d}"
                               + (f", Des massima dell'armatura {tetto:+d}" if tetto is not None else "")})
    # contatto e sprovvista si derivano dalla CA **scritta**: un errore di somma è già uno scarto suo
    mc = _CONTATTO.search(dettaglio or "")
    if mc:
        atteso = ca - somma(voci)[0] + somma(voci, NON_A_CONTATTO)[0]
        if int(mc.group(1)) != atteso:
            scarti.append({"campo": "CA.contatto", "scritto": int(mc.group(1)), "atteso": atteso,
                           "nota": "CA senza armatura, scudo e armatura naturale"})
    ms = _SPROVVISTA.search(dettaglio or "")
    if ms:
        schiva = sum(v.valore for v in voci if v.tipo == "schivare")
        destrezza = sum(max(0, v.valore) for v in des)
        leciti = {ca - schiva - destrezza}
        if _SCHIVARE_PRODIGIOSO.search((dettaglio or "") + " " + testo):
            leciti.add(ca - schiva)              # schivare prodigioso: tiene la Destrezza
        if int(ms.group(1)) not in leciti:
            scarti.append({"campo": "CA.sprovvista", "scritto": int(ms.group(1)), "atteso": min(leciti),
                           "nota": "CA senza Destrezza e schivare"})
    return scarti, nv
