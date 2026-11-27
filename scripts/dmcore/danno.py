"""dmcore.danno — il danno di un'arma ricostruito dalla tabella (ADR-0126, lotto 2).

SRD 3.5, *Equipment* («Table: Weapons», «Weapon Size») e *Combat* («Damage»):

* il **dado** è quello della tabella per la taglia Media, portato alla taglia
  di chi impugna;
* il **bonus** è il modificatore di Forza (una volta e mezza a due mani, la
  metà con la mano secondaria; niente con archi e balestre, ma la penalità di
  Forza vale per gli archi non compositi), più il potenziamento dell'arma, più
  i talenti che la scheda dichiara (Arma Specializzata e Superiore);
* il **critico** è quello della tabella; l'intervallo raddoppia con Critico
  Migliorato o con un'arma affilata.

Qui si giudicano le armi della tabella. Un attacco naturale, un'arma dei
manuali, una riga a condizione («in ira», «con Attacco Poderoso») non si
giudicano: l'attacco naturale e l'arma ignota tornano come non verificabili.
"""
from __future__ import annotations

import functools
import re
from dataclasses import dataclass

from dmcore import sistemi as S

__all__ = ["Attacco", "tabella", "arma_di", "passi_di_taglia", "dado_per_taglia", "leggi", "giudica"]

_ATTACCO = re.compile(
    r"(?P<prima>[^;()]*?)(?P<bonus>[+-]\d+(?:\s*/\s*[+-]\d+)*)\s*"
    r"(?:in mischia|a distanza|mischia|distanza|melee|ranged)?\s*\((?P<danno>[^()]*)\)", re.I)
_DADO = re.compile(r"^\s*(\d+d\d+|\d+)\s*([+-]\s*\d+)?")
_CRITICO = re.compile(r"(?:(\d+)\s*-\s*20)\s*(?:/?\s*[x×]\s*(\d))?|[x×]\s*(\d)")
_CONDIZIONE = re.compile(
    r"\bin ira\b|\bira\b|frenesia|poderoso|power attack|\bcon\s+\w+\s+(?:poderoso|rapido)|carica|"
    r"\bse\b|\bquando\b|\bcontro\b|\bvs\b|nemico prescelto|punire|smite", re.I)
_DOPO_IN_IRA = re.compile(r"\s*,?\s*(?:in ira|entro|contro|vs|se|quando|alla carica|in carica|con)\b", re.I)
_DUE_MANI = re.compile(r"a due mani|two-handed|2 mani", re.I)
_SECONDARIA = re.compile(r"mano secondaria|secondari[ao]|off-?hand|\bTWF\b", re.I)
_NATURALI = re.compile(
    r"\b(?:mors[oi]|artigli[oe]?|schiant[oi]|coda|incornata|pungiglione|tentacol[oi]|zoccol[oi]|ala|ali|"
    r"colpo d'ala|speronata|stritolamento|bite|claws?|slam|gore|sting|tail|wing|tocco|raggi[oi]|roccia|"
    r"rocce|massi|ragnatela|soffio|zann[ae]|corn[ao]|pugn[oi] )\b", re.I)
_AFFILATA = re.compile(r"\b(?:affilat[ao]|keen)\b", re.I)
_CRITICO_MIGLIORATO = re.compile(r"(?:improved critical|critico migliorato)(?:\s*[(:]\s*([^),;·\n]+))?", re.I)
_COMPOSITO = re.compile(r"composit[oe]", re.I)
_POTENZIAMENTO = re.compile(r"(?<![\d/])\+(\d)\b(?!\s*/)")


@dataclass(frozen=True)
class Attacco:
    nome: str            # il testo davanti al bonus
    dado: str
    bonus: int
    minaccia: "int | None"
    moltiplicatore: "int | None"
    testo: str           # la parentesi del danno
    seconda: bool = False  # viene dopo «e» nella stessa riga: con due armi è la mano secondaria


@functools.lru_cache(maxsize=None)
def tabella(sistema: str = "dnd35") -> dict:
    d = S.dati(sistema, "creature.armi")
    nomi = {}
    for a in d["armi"]:
        for n in a["nomi"]:
            nomi[n.lower()] = a
    schema = re.compile(r"(?<!\w)(" + "|".join(sorted((re.escape(n) for n in nomi), key=len, reverse=True))
                        + r")(?!\w)", re.I)
    taglie = re.compile(r"(?<!\w)(" + "|".join(sorted(map(re.escape, d["taglie"]), key=len, reverse=True))
                        + r")(?!\w)", re.I)
    sorgenti = [dict(s, _re=re.compile(s["schema"] + r"(?:\s*[(:]\s*([^),;·\n]+))?", re.I))
                for s in d.get("sorgenti", [])]
    return {"nomi": nomi, "schema": schema, "scala": d["scala"], "taglie": d["taglie"],
            "taglie_re": taglie, "sorgenti": sorgenti}


def arma_di(nome: str, sistema: str = "dnd35") -> "dict | None":
    t = tabella(sistema)
    m = t["schema"].search(nome)
    return t["nomi"][m.group(1).lower()] if m else None


_TAGLIA_IN_CA = re.compile(r"([+-]\d+)\s*(?:taglia|size)", re.I)
_PASSI_DA_CA = {8: -4, 4: -3, 2: -2, 1: -1, -1: 1, -2: 2, -4: 3, -8: 4}


def passi_di_taglia(tipo: str, ca_dettaglio: str = "", sistema: str = "dnd35") -> int:
    """Passi rispetto alla taglia Media: dalla riga `tipo:`, o dalla voce di taglia della CA."""
    t = tabella(sistema)
    m = t["taglie_re"].search((tipo or "").split("·")[0])
    if m:
        return t["taglie"][m.group(1).lower()]
    m = _TAGLIA_IN_CA.search((ca_dettaglio or "").replace("−", "-"))
    return _PASSI_DA_CA.get(int(m.group(1)), 0) if m else 0


def dado_per_taglia(dado: str, passi: int, sistema: str = "dnd35") -> "str | None":
    scala = tabella(sistema)["scala"]
    for _ in range(abs(passi)):
        dado = scala["su" if passi > 0 else "giu"].get(dado)
        if dado is None:
            return None
    return dado


def leggi(riga: str) -> "list[Attacco]":
    """Gli attacchi di una riga `attacchi`, uno per parentesi di danno."""
    fuori = []
    testo = (riga or "").replace("−", "-").replace("–", "-")
    for m in _ATTACCO.finditer(testo):
        prima = re.split(r"\be\b|\boppure\b|\bo\b|·|—|:", m.group("prima"))[-1].strip()
        intera = m.group("prima")
        d = _DADO.match(m.group("danno"))
        if not d:
            continue
        resto = m.group("danno")[d.end():]
        c = _CRITICO.search(re.sub(r"\d+d\d+", "", resto))
        minaccia = molt = None
        if c:
            minaccia = int(c.group(1)) if c.group(1) else 20
            molt = int(c.group(2) or c.group(3) or 2)
        nome = prima if prima else intera.strip()
        if not re.search(r"[^\W\d_]{3}", nome) and fuori:
            nome = fuori[-1].nome.lstrip("\0")      # «; +26/+21 (3d6+16)»: la stessa arma di prima
            if minaccia is None:
                minaccia, molt = fuori[-1].minaccia, fuori[-1].moltiplicatore
        dopo = re.split(r"[;·(]", testo[m.end():])[0]
        if "—" in intera or _CONDIZIONE.search(intera.split(";")[-1]) or _DOPO_IN_IRA.match(dopo):
            nome = "\0" + nome            # a condizione: non si giudica
        seconda = bool(re.search(r"\be\s+[^;]*$", intera)) and bool(fuori)
        fuori.append(Attacco(nome, d.group(1), int((d.group(2) or "0").replace(" ", "")),
                             minaccia, molt, m.group("danno"), seconda))
    return fuori


def _talento_su(schema: "re.Pattern", arma: dict, talenti: str) -> str:
    """«si» se il talento nomina quest'arma, «forse» se non nomina nessun'arma, «no» altrimenti."""
    esito = "no"
    for m in schema.finditer(talenti):
        su = (m.group(m.lastindex) if m.lastindex else None) or ""
        if any(n in su.lower() for n in arma["nomi"]):
            return "si"
        if not su.strip():
            esito = "forse"
    return esito


_DUE_ARMI = re.compile(r"two-weapon fighting|combattere con due armi", re.I)
_MONACO = re.compile(r"\b(?:monaco|monk)\b", re.I)
_SENZ_ARMI = "Unarmed strike"


_NATURALE_MIGLIORATO = re.compile(r"improved natural attack|attacco naturale migliorato", re.I)


def giudica(riga: str, mod_for: "int | None", tipo: str = "", talenti: str = "", scudo: bool = True,
            ca_dettaglio: str = "", sistema: str = "dnd35",
            creatura: "tuple[str, dict] | None" = None) -> "tuple[list[dict], list[dict]]":
    """(scarti, non verificabili) degli attacchi con un'arma della tabella.

    Con una `creatura` base (nome, voce di `creature.base`) della stessa taglia
    della scheda, anche il dado degli attacchi naturali che la base ha."""
    from dmcore import creature_base as CB
    scarti, nv = [], []
    t = tabella(sistema)
    passi = passi_di_taglia(tipo, ca_dettaglio, sistema)
    due_armi = bool(_DUE_ARMI.search(talenti))
    for a in leggi(riga):
        if a.nome.startswith("\0"):
            continue
        arma = arma_di(a.nome, sistema)
        if arma is None:
            if not _NATURALI.search(a.nome):
                nv.append({"campo": "danno", "nota": f"«{a.nome.strip()}»: arma che la tabella non ha"})
                continue
            nat = CB.attacco_naturale(a.nome, creatura[1]) if creatura else None
            if nat is None:
                nv.append({"campo": "danno", "nota": f"«{a.nome.strip()}»: attacco naturale, il dado viene dalla creatura"})
                continue
            leciti = {nat["dado"]}
            if _NATURALE_MIGLIORATO.search(talenti):      # il dado sale come per una taglia in più
                leciti.add(dado_per_taglia(nat["dado"], 1, sistema) or nat["dado"])
            if a.dado not in leciti:
                scarti.append({"parentesi": a.testo, "campo": "danno.dado", "scritto": a.dado, "atteso": nat["dado"],
                               "nota": f"«{a.nome.strip()}»: {nat['nome']} della creatura base {creatura[0]}"})
            continue
        chi = a.nome.strip()
        if arma["nome"] == _SENZ_ARMI and _MONACO.search(tipo + " " + talenti):
            nv.append({"campo": "danno", "nota": f"«{chi}»: colpo senz'armi del monaco, il dado viene dalla classe"})
            continue
        # dado
        atteso = dado_per_taglia(arma["dado"], passi, sistema)
        if atteso and a.dado != atteso:
            scarti.append({"parentesi": a.testo, "campo": "danno.dado", "scritto": a.dado, "atteso": atteso,
                           "nota": f"«{chi}»: {arma['nome']} {arma['dado']} per taglia Media"
                                   + (f", {passi:+d} di taglia" if passi else "")})
        # critico
        base = arma["minaccia"]
        doppia = 21 - 2 * (21 - base)
        migliorato = _talento_su(_CRITICO_MIGLIORATO, arma, talenti)
        if _AFFILATA.search(chi) or migliorato == "si":
            minacce = {doppia}
        elif migliorato == "forse":
            minacce = {base, doppia}
        else:
            minacce = {base}
        scritto = (a.minaccia or 20, a.moltiplicatore or 2)
        if scritto[0] not in minacce or scritto[1] != arma["moltiplicatore"]:
            def forma(mi, mo):
                return (f"{mi}-20/" if mi < 20 else "") + f"x{mo}"
            scarti.append({"parentesi": a.testo, "campo": "danno.critico", "scritto": forma(*scritto) if a.minaccia else "non scritto",
                           "atteso": forma(doppia if minacce == {doppia} else base, arma["moltiplicatore"]),
                           "nota": f"«{chi}»: {arma['nome']}"})
        # bonus
        if mod_for is None:
            nv.append({"campo": "danno", "nota": f"«{chi}»: Forza non leggibile, il bonus non si giudica"})
            continue
        pot = _POTENZIAMENTO.search(chi)
        pot = int(pot.group(1)) if pot and not arma["nome"].startswith(("Shield", "Spiked shield")) else 0
        esiti = [(s["valore"], ("si" if arma["nome"] in s["armi"] and s["_re"].search(talenti) else "no")
                  if "armi" in s else _talento_su(s["_re"], arma, talenti)) for s in t["sorgenti"]]
        spec = sum(v for v, e in esiti if e == "si")
        forse = sum(v for v, e in esiti if e == "forse")
        distanza = arma["impugnatura"] == "distanza" and not arma["nome"] in ("Javelin", "Dart", "Sling", "Bolas", "Shuriken (5)")
        if distanza:
            composito = bool(_COMPOSITO.search(chi)) or "composite" in arma["nome"]
            forze = {min(mod_for, 0)} if not composito else set(range(min(mod_for, 0), max(mod_for, 0) + 1))
            if "Crossbow" in arma["nome"]:
                forze = {0}
        elif _SECONDARIA.search(chi + " " + a.testo) or (due_armi and a.seconda):
            forze = {mod_for // 2 if mod_for > 0 else mod_for}
        elif arma["impugnatura"] == "due mani" or _DUE_MANI.search(chi):
            forze = {mod_for * 3 // 2 if mod_for > 0 else mod_for}
        elif arma["impugnatura"] == "una mano" and not scudo and not arma.get("gittata"):
            forze = {mod_for, mod_for * 3 // 2 if mod_for > 0 else mod_for}   # a una mano o a due: tutte e due legali
        else:
            forze = {mod_for}
        leciti = {f + pot + spec for f in forze} | {f + pot + spec + forse for f in forze}
        if a.bonus not in leciti:
            atteso_b = max(leciti)
            scarti.append({"parentesi": a.testo, "campo": "danno.bonus", "scritto": a.bonus, "atteso": atteso_b,
                           "nota": f"«{chi}»: Forza {max(forze):+d}"
                                   + (f", potenziamento {pot:+d}" if pot else "")
                                   + (f", talenti {spec:+d}" if spec else "")})
    return scarti, nv
