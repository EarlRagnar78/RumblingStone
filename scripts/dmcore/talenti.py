"""dmcore/talenti.py — quanti talenti ha un PNG o un mostro, e quali può prendere.

Lotto 3 delle regole complete (richiesta del DM del 2026-11-10). Prima il
generatore dava un solo «talento firma», senza contarli e senza prerequisiti.
Qui la regola del manuale, con i dati della capacità `creature.talenti`
(`sistemi/<sistema>/dati/talenti.toml`, generato da SRD e PRD):

- **quanti**: 3.5 1 + 1 ogni 3 livelli del personaggio (SRD «Experience and
  Level-Dependent Benefits»); PF1e uno a ogni livello dispari (PRD «Character
  Advancement»). I DV razziali contano come livelli. In più i talenti bonus delle
  classi (colonna «Special») e quelli che la tabella concede per nome.
- **quali**: solo talenti di cui il PNG ha tutti i prerequisiti (caratteristiche,
  BAB, livello d'incantatore, livelli di classe, capacità di classe, altri talenti
  presi prima). Un talento con prerequisiti che la regola non sa leggere (`altro`)
  o che chiede gradi in un'abilità non si sceglie.
- **in che ordine**: prima i concessi, poi i bonus (dalla lista della classe), poi
  i generali; dentro ogni gruppo la preferenza del ruolo (scelta di design,
  dichiarata in `PREFERENZE`), poi i talenti senza prerequisiti, poi il resto.

Gli effetti sui numeri che un blocco scrive (iniziativa, pf, TS, attacco, CA)
li calcola `effetti`, e sono gli stessi che il cancello delle schede riconosce.
"""
from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from functools import lru_cache

from . import sistemi as _S

#: Preferenze per ruolo, in inglese (nomi della fonte). Non sono regole: dicono
#: quale talento lecito il generatore prova per primo. I talenti che un sistema
#: non ha si saltano.
PREFERENZE: "dict[str, list[str]]" = {
    "bruto": ["Power Attack", "Cleave", "Improved Bull Rush", "Weapon Focus", "Toughness",
              "Great Cleave", "Improved Overrun", "Great Fortitude", "Improved Initiative", "Iron Will",
              "Weapon Specialization", "Improved Critical", "Diehard", "Endurance"],
    "schermagliatore": ["Dodge", "Mobility", "Improved Initiative", "Weapon Finesse", "Spring Attack",
                        "Combat Reflexes", "Lightning Reflexes", "Weapon Focus", "Two-Weapon Fighting",
                        "Improved Feint", "Combat Expertise", "Iron Will", "Toughness"],
    "tiratore": ["Point-Blank Shot", "Point Blank Shot", "Precise Shot", "Rapid Shot", "Deadly Aim",
                 "Far Shot", "Weapon Focus", "Manyshot", "Improved Initiative", "Dodge",
                 "Lightning Reflexes", "Shot on the Run", "Iron Will", "Toughness"],
    "comandante": ["Improved Initiative", "Iron Will", "Weapon Focus", "Power Attack", "Combat Reflexes",
                   "Toughness", "Leadership", "Persuasive", "Great Fortitude", "Lightning Reflexes"],
    "controllore": ["Spell Focus", "Combat Casting", "Improved Initiative", "Greater Spell Focus",
                    "Spell Penetration", "Extend Spell", "Silent Spell", "Still Spell", "Toughness",
                    "Iron Will", "Lightning Reflexes", "Dodge"],
    "blaster": ["Spell Focus", "Improved Initiative", "Combat Casting", "Empower Spell", "Spell Penetration",
                "Point-Blank Shot", "Point Blank Shot", "Precise Shot", "Maximize Spell", "Toughness",
                "Iron Will", "Lightning Reflexes"],
    "supporto": ["Combat Casting", "Improved Initiative", "Extend Spell", "Toughness", "Iron Will",
                 "Great Fortitude", "Spell Focus", "Selective Channeling", "Extra Channel", "Dodge"],
}

#: talenti che servono a tutti: il ripiego quando la preferenza del ruolo è finita
RIPIEGO = ["Improved Initiative", "Toughness", "Iron Will", "Great Fortitude", "Lightning Reflexes",
           "Dodge", "Combat Reflexes", "Alertness", "Endurance", "Diehard", "Blind-Fight"]


def _k(nome: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", nome.lower().replace("’", "'").replace("'", "")).strip()


@lru_cache(maxsize=None)
def dati(sistema: str) -> dict:
    """I dati dei talenti del sistema. `talenti_manuali` (i manuali 3.5 fuori
    SRD, dai dati PCGen) si fonde sotto `talenti`: un nome dell'SRD vince. Il
    generatore sceglie solo dai libri base (`_ordine`), quindi i talenti dei
    manuali servono alla verifica, non alla scelta (ADR-0124)."""
    d = dict(_S.regole(sistema).dati("creature.talenti"))
    if d.get("talenti_manuali"):
        d["talenti"] = {**d.pop("talenti_manuali"), **d["talenti"]}
    return d


def _per_chiave(sistema: str) -> "dict[str, str]":
    d = dati(sistema)["talenti"]
    out = {_k(n): n for n in d}
    out.update({_k(v["it"]): n for n, v in d.items() if v.get("it")})
    # «Incantesimi focalizzati (invocazione)», «Competenza nelle armature (leggere)»:
    # la scheda scrive la scelta fra parentesi, il nome si cerca senza (ADR-0124)
    for n, v in d.items():
        if v.get("it"):
            out.setdefault(_k(re.sub(r"\s*\(.*\)$", "", v["it"])), n)
    return out


def nome_inglese(sistema: str, nome: str) -> "str | None":
    """Il nome della fonte di un talento, dal nome inglese o italiano."""
    return _per_chiave(sistema).get(_k(re.sub(r"\s*\(.*\)$", "", nome)))


def italiano(sistema: str, en: str) -> str:
    return dati(sistema)["talenti"].get(en, {}).get("it") or en


# ------------------------------------------------------------------ quanti

def generali(sistema: str, livello_personaggio: int) -> int:
    n = max(1, livello_personaggio)
    return 1 + n // 3 if sistema == "dnd35" else (n + 1) // 2


def bonus_di_classe(sistema: str, livelli: "dict[str, int]") -> "list[tuple[str, int]]":
    """[(classe, livello di classe)] di ogni talento bonus, in ordine."""
    b = dati(sistema)["bonus"]
    return [(cl, lv) for cl, n in livelli.items() for lv in b.get(cl, {}).get("livelli", []) if lv <= n]


def concessi(sistema: str, livelli: "dict[str, int]") -> "list[tuple[str, str]]":
    b = dati(sistema)["bonus"]
    return [(cl, t) for cl, n in livelli.items()
            for lv, nomi in sorted(b.get(cl, {}).get("concessi", {}).items(), key=lambda kv: int(kv[0]))
            if int(lv) <= n for t in nomi]


def quanti(sistema: str, livelli: "dict[str, int]", dv_razziali: int = 0) -> int:
    """Tutti i talenti di un PNG: generali + bonus + concessi (la misura del lotto 3)."""
    tot = sum(livelli.values()) + dv_razziali
    return generali(sistema, tot) + len(bonus_di_classe(sistema, livelli)) + len(concessi(sistema, livelli))


# ------------------------------------------------------------------ prerequisiti

@dataclass
class Stato:
    """Quello che serve per i prerequisiti: caratteristiche (For, Des, Cos, Int, Sag, Car)."""
    car: "dict[str, int]"
    bab: int
    livelli: "dict[str, int]" = field(default_factory=dict)
    lic: int = 0
    talenti: "list[str]" = field(default_factory=list)
    #: dadi vita totali (classi + razziali): il «livello del personaggio» dei
    #: prerequisiti `character` (Leadership). 0 = la somma dei livelli di classe.
    dv: int = 0


#: Le classi base 3.5 in inglese e in italiano. I dati 3.5 usano l'italiano per
#: `[capacita]` e `[bonus]` e l'inglese per i prerequisiti `classe` (fighter 4
#: di Weapon Specialization): un nome vale per l'altro (ADR-0124, D1).
CLASSI_EN_IT = {"barbarian": "barbaro", "bard": "bardo", "cleric": "chierico", "druid": "druido",
                "fighter": "guerriero", "monk": "monaco", "paladin": "paladino", "ranger": "ranger",
                "rogue": "ladro", "sorcerer": "stregone", "wizard": "mago"}
_ALIAS = {**CLASSI_EN_IT, **{it: en for en, it in CLASSI_EN_IT.items()}}


def livelli_di(s: Stato) -> "dict[str, int]":
    """I livelli di classe sotto tutti e due i nomi, più `character` (ADR-0124, D1 e D2)."""
    out: dict[str, int] = {}
    for cl, n in s.livelli.items():
        for nome in {cl, _ALIAS.get(cl, cl)}:
            out[nome] = max(out.get(nome, 0), n)
    out["character"] = max(s.dv, sum(s.livelli.values()), s.livelli.get("character", 0))
    return out


def violazioni(sistema: str, en: str, s: Stato) -> "list[dict]":
    """I prerequisiti che il PNG non ha, uno per voce: `regola`, `atteso`, `ha`, `testo`.

    È la stessa regola di `manca`, in forma strutturata: la usa
    `verifica_talenti.py`, che la restituisce all'agente via MCP (ADR-0124).
    `regola` è una di car, bab, lic, classe, talento, capacita, gradi, altro,
    fonte; `gradi` e `altro` sono prerequisiti che i dati non sanno leggere.
    """
    t = dati(sistema)["talenti"].get(en)
    if t is None:
        return [{"regola": "fonte", "atteso": en, "ha": None, "testo": "non è un talento della fonte"}]
    liv = livelli_di(s)
    out: list[dict] = []

    def v(regola: str, atteso, ha, testo: str) -> None:
        out.append({"regola": regola, "atteso": atteso, "ha": ha, "testo": testo})

    for c, soglia in t.get("car", {}).items():
        if s.car.get(c, 10) < soglia:
            v(f"car.{c}", soglia, s.car.get(c, 10), f"{c} {soglia} (ha {s.car.get(c, 10)})")
    if s.bab < t.get("bab", 0):
        v("bab", t["bab"], s.bab, f"BAB +{t['bab']} (ha {s.bab:+d})")
    if s.lic < t.get("lic", 0):
        v("lic", t["lic"], s.lic, f"livello d'incantatore {t['lic']} (ha {s.lic})")
    for cl, soglia in t.get("classe", {}).items():
        if liv.get(cl, 0) < soglia:
            v(f"classe.{cl}", soglia, liv.get(cl, 0), f"{cl} {soglia}° livello")
    for p in t.get("talenti", []):
        if p not in s.talenti:
            v("talento", p, None, p)
    caps = dati(sistema).get("capacita", {})
    for cap in t.get("capacita", []):
        if not any(liv.get(cl, 0) >= lv for cl, lv in caps.get(cap, {}).items()):
            v("capacita", cap, None, cap)
    if t.get("gradi"):
        v("gradi", t["gradi"], None, "gradi in " + ", ".join(t["gradi"]))
    for a in t.get("altro", []):
        v("altro", a, None, a)
    return out


def manca(sistema: str, en: str, s: Stato) -> "list[str]":
    """I prerequisiti che il PNG non ha (vuota = può prenderlo)."""
    return [x["testo"] for x in violazioni(sistema, en, s)]


def bonus_senza_prerequisiti(sistema: str, en: str, livelli: "dict[str, int]") -> "str | None":
    """La classe che concede `en` come talento bonus **senza prerequisiti**, o None.

    Il monaco (Lotta Migliorata al 1°, Sbilanciare Migliorato al 6°) e il ranger
    (stile di combattimento) prendono i loro talenti bonus anche senza i
    prerequisiti: una scheda che li elenca non è illegale.
    """
    b = dati(sistema)["bonus"]
    for cl, n in livelli.items():
        voce = b.get(cl) or b.get(_ALIAS.get(cl, cl))
        if not voce or not voce.get("senza_prerequisiti"):
            continue
        liste = [nomi for lv, nomi in voce.get("nomi", {}).items() if int(lv) <= n]
        for stile in voce.get("stili", {}).values():
            if isinstance(stile, dict):
                liste += [nomi for lv, nomi in stile.items() if str(lv).isdigit() and int(lv) <= n]
            elif isinstance(stile, list):
                liste.append(stile)
        if any(en in nomi for nomi in liste):
            return cl
    return None


def _lista_bonus(sistema: str, classe: str, livello: int, stile: "str | None") -> "tuple[set | None, bool]":
    """(talenti ammessi o None = qualsiasi del tipo, senza_prerequisiti) per un bonus."""
    b = dati(sistema)["bonus"][classe]
    t = dati(sistema)["talenti"]
    if str(livello) in b.get("scelte", {}):          # «chooses either Precise Shot or Outflank»
        return set(b["scelte"][str(livello)]), b.get("senza_prerequisiti", False)
    if str(livello) in b.get("tipi_livello", {}):    # «receives a teamwork feat as a bonus feat»
        tipi = set(b["tipi_livello"][str(livello)])
        return {n for n, v in t.items() if tipi & set(v.get("tipi", []))}, False
    nomi_per_lv = b.get("stili", {}).get(stile, {}) if stile else b.get("nomi", {})
    if not nomi_per_lv and b.get("stili"):
        nomi_per_lv = next(iter(b["stili"].values()))
    ammessi = set()
    for lv, nomi in nomi_per_lv.items():
        if int(lv) <= livello and (b.get("cumulativa", True) or int(lv) == livello):
            ammessi |= set(nomi)
    for n, v in t.items():
        if set(v.get("tipi", [])) & set(b.get("tipi", [])):
            ammessi.add(n)
    if not ammessi:
        return None, False
    return ammessi, b.get("senza_prerequisiti", False)


def _ordine(sistema: str, ruolo: str, rng: random.Random) -> "list[str]":
    d = dati(sistema)["talenti"]
    chiavi = _per_chiave(sistema)
    pref = [chiavi[_k(n)] for n in PREFERENZE.get(ruolo, []) + RIPIEGO if _k(n) in chiavi]
    base = [n for n in sorted(d) if d[n]["libro"] in ("cr", "srd")]
    rng.shuffle(base)
    visti, out = set(), []
    for n in pref + base:
        if n not in visti:
            visti.add(n)
            out.append(n)
    return out


@dataclass
class Scelta:
    talenti: "list[tuple[str, str]]"   # (nome inglese, origine: concesso / bonus classe / generale)
    note: "list[str]"


def scegli(sistema: str, ruolo: str, s: Stato, *, dv_razziali: int = 0, firma: "str | None" = None,
           stile: "str | None" = None, rng: "random.Random | None" = None,
           obbligati: "list[str] | None" = None, esclusi: "tuple[str, ...]" = ()) -> Scelta:
    rng = rng or random.Random(0)
    presi: "list[tuple[str, str]]" = []
    note: "list[str]" = []
    s.talenti = list(s.talenti)

    def prendi(en: str, origine: str) -> None:
        presi.append((en, origine))
        s.talenti.append(en)

    for cl, en in concessi(sistema, s.livelli):
        prendi(en, f"concesso da {cl}")
    ordine = _ordine(sistema, ruolo, rng)
    ordine = [n for n in ordine if n not in esclusi]   # talenti che sul blocco non farebbero niente
    if obbligati:   # requisiti di una classe di prestigio: prima di tutto il resto, nell'ordine dato
        ordine = list(obbligati) + [n for n in ordine if n not in obbligati]
    if firma:
        en = nome_inglese(sistema, firma)
        if en is None:
            note.append(f"«{firma}» non è un talento: resta nel carattere, non tra i talenti")
        elif en in esclusi:
            note.append(f"«{italiano(sistema, en)}» non preso: sul blocco non farebbe niente")
        else:
            m = manca(sistema, en, Stato(s.car, s.bab, s.livelli, s.lic, s.talenti))
            if m:
                note.append(f"«{italiano(sistema, en)}» non preso: mancano {', '.join(m)}")
            ordine = list(obbligati or []) + [en] + [n for n in ordine if n != en and n not in (obbligati or [])]
    for cl, lv in bonus_di_classe(sistema, s.livelli):
        ammessi, senza = _lista_bonus(sistema, cl, lv, stile)
        if ammessi is None:
            note.append(f"talento bonus di {cl} al {lv}°: la lista non è nei dati, preso tra i generali")
            ammessi, senza = set(dati(sistema)["talenti"]), False
        for en in ordine + sorted(ammessi):
            if en in ammessi and en not in esclusi and en not in s.talenti and (senza or not manca(sistema, en, s)):
                prendi(en, f"bonus {cl} {lv}°")
                break
        else:
            note.append(f"talento bonus di {cl} al {lv}°: nessun talento lecito nella lista")
    for _ in range(generali(sistema, sum(s.livelli.values()) + dv_razziali)):
        for en in ordine:
            if en not in s.talenti and not manca(sistema, en, s):
                prendi(en, "generale")
                break
        else:
            note.append("talento generale: nessuno lecito")
    return Scelta(presi, note)


# ------------------------------------------------------------------ effetti

def effetti(sistema: str, talenti: "list[str]", dv: int) -> "dict[str, int]":
    """Gli effetti fissi sui numeri del blocco: iniziativa, pf, temp/rifl/vol, attacco, ca."""
    t = set(talenti)
    e = {"iniziativa": 0, "pf": 0, "temp": 0, "rifl": 0, "vol": 0, "attacco": 0, "ca": 0}
    if "Improved Initiative" in t:
        e["iniziativa"] += 4
    if "Toughness" in t:
        e["pf"] += 3 if sistema == "dnd35" else max(3, dv)
    if "Improved Toughness" in t:
        e["pf"] += dv
    if "Great Fortitude" in t:
        e["temp"] += 2
    if "Lightning Reflexes" in t:
        e["rifl"] += 2
    if "Iron Will" in t:
        e["vol"] += 2
    if "Weapon Focus" in t:
        e["attacco"] += 1
    if "Dodge" in t and sistema == "pf1e":
        e["ca"] += 1   # PF1e: +1 schivare alla CA; nel 3.5 è contro un solo avversario
    return e


# ------------------------------------------------------------------ requisiti delle classi di prestigio

def _livello_massimo(classe: str, livello: int, costruzione: dict) -> int:
    """Il livello d'incantesimo più alto che la classe lancia a quel livello (0 = nessuno).

    Dalla griglia del PRD (`classi.toml`): una colonna presente vale anche con 0
    slot, perché nel PRD lo 0 è «solo con gli incantesimi bonus».
    """
    inc = costruzione.get("incantatori", {}).get(classe)
    if not inc:
        return 0
    riga = costruzione.get("griglie", {}).get(inc["griglia"], {}).get(str(min(livello, 20)))
    if not riga:
        return 0
    return len(riga) - 1   # l'indice è il livello d'incantesimo, con o senza trucchetti


def prestigio(sistema: str, classi: "list[tuple[str, int]]", costruzione: dict
              ) -> "tuple[list[str], list[str]]":
    """(talenti che i requisiti obbligano a prendere, righe del conto) per le classi di prestigio.

    Lo stato è quello delle classi elencate **prima** della classe di prestigio:
    BAB, livello d'incantesimo arcano e divino, capacità. Gradi e il resto non
    si possono verificare qui e il conto lo dice.
    """
    req = dati(sistema).get("requisiti", {})
    caps = dati(sistema).get("capacita", {})
    obbligati: "list[str]" = []
    righe: "list[str]" = []
    for i, (cl, _lv) in enumerate(classi):
        r = req.get(cl)
        if r is None:
            continue
        prima = classi[:i]
        bab = sum(int(costruzione["classi"][c]["bab"] * n) for c, n in prima)
        lv_inc = {"arcani": 0, "divini": 0}
        for c, n in prima:
            for tipo, chiave in (("arcani", "cast arcane spells"), ("divini", "cast divine spells")):
                if c in caps.get(chiave, {}):
                    lv_inc[tipo] = max(lv_inc[tipo], _livello_massimo(c, n, costruzione))
        ok, no = [], []
        if r.get("bab"):
            (ok if bab >= r["bab"] else no).append(f"BAB +{r['bab']} (ha {bab:+d})")
        for tipo, n in r.get("incantesimi", {}).items():
            (ok if lv_inc[tipo] >= n else no).append(f"incantesimi {tipo} di {n}° (arriva al {lv_inc[tipo]}°)")
        for cap in r.get("capacita", []):
            ha = any(dict(prima).get(c, 0) >= lv for c, lv in caps.get(cap, {}).items())
            (ok if ha else no).append(cap)
        for t in r.get("talenti", []):
            obbligati.append(t)
        for scelta in r.get("oppure", []):
            obbligati.append(scelta[0])
        talenti_txt = [italiano(sistema, t) for t in r.get("talenti", [])] + \
            [" o ".join(italiano(sistema, x) for x in s) for s in r.get("oppure", [])]
        pezzi = [f"✓ {x}" for x in ok] + [f"✗ {x}" for x in no]
        if talenti_txt:
            pezzi.append(f"talenti richiesti, presi per primi: {', '.join(talenti_txt)}")
        for t, arma in r.get("armi", {}).items():
            pezzi.append(f"{italiano(sistema, t)} con {arma}")
        righe.append(f"requisiti di {cl} (PRD, {r['fonte']}): " + ("; ".join(pezzi) or "nessuno che si conti"))
        if no:
            righe.append(f"⚠ {cl}: con le classi messe prima non si entra ({', '.join(no)}); "
                         "metti prima le classi che danno il requisito")
        da_dm = [f"{k} {v}" for k, v in r.get("gradi", {}).items()] + r.get("altro", [])
        if da_dm:
            righe.append(f"{cl}, da verificare dal DM: " + "; ".join(da_dm))
    return obbligati, righe
