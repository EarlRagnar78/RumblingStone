#!/usr/bin/env python3
"""conformita_statblocchi.py — pf, TS, BAB, lotta e attacco tornano con le caratteristiche?

## Perche' esiste

`RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI` §5 elencava tre identita' del 3.5
che nessuno controllava, perche' mancavano le caratteristiche. ADR-0064 le ha
scritte in tutti i 108 statblocchi. Questo e' il controllo che quelle righe
rendono possibile:

| identita' | la regola SRD 3.5 |
|---|---|
| **pf** | media dei dadi vita + DV × mod Cos (+3 per Robustezza) |
| **TS** | base di classe e di tipo (buono 2 + L/2, cattivo L/3) + Cos / Des / Sag |
| **BAB** | somma dei BAB di classe e di tipo, ciascuno arrotondato in basso |
| **lotta** | BAB + mod For + modificatore speciale di taglia |
| **attacco** | BAB + mod For (o Des con Arma Accurata) + taglia + bonus dell'arma |
| **iniziativa** | mod Des (+4 con Iniziativa Migliorata) |
| **variante Advanced** | pf +2 per DV, CA +4, GS +1 rispetto allo statblocco base |

🔎 **I talenti, su suggerimento del DM** (2026-09-23): Tempra Possente,
Riflessi Fulminei, Volonta' di Ferro, Iniziativa Migliorata e il mantello
della resistenza entrano nel conto. Alzano il **minimo** atteso, e cosi' si
vede la scheda che elenca un talento e non ne conta il bonus (Mira Serani,
«Vol +8 (Ferrea Volonta')»). Lotta, attacco e iniziativa si controllano anche
senza la composizione dei DV, perche' usano il BAB scritto.

## Il principio: si verifica solo dove il dato non e' una scelta

Ogni scarto si legge insieme alla **provenienza** delle caratteristiche:

* **trascritte** dalla fonte o **scritte a mano**: sono il dato. Se pf o TS non
  tornano, a sbagliare e' lo statblocco, e va corretto;
* **generate** dall'array (ADR-0064): sono una scelta. Uno scarto dice qualcosa
  sul generatore prima che sulla scheda, e non autorizza a toccare i numeri.

## Il template spiega lo scarto?

Il DM, il 2026-09-23: *«c'era una forma di generazione che prendeva spunto da
PF1e per fare incontri piu' forti senza aumentare il GS: controlla se sono
questi i casi che non tornano»*. Per ogni scheda che non torna si rifanno i
conti **con le caratteristiche potenziate** dai due template semplici PF1e che
il repo usa: **Advanced** (+4 a tutte) e **Giant** (For e Cos +4, Des −2). Se
con uno dei due tutto torna, lo scarto e' un potenziamento e non un errore.

## Cosa NON verifica, dichiarato

Oggetti magici diversi dal mantello della resistenza, talenti diversi da
quelli elencati sopra, bonus razziali ai TS, incantesimi attivi, la
non-competenza nelle armi esotiche. Per questo un TS **sopra** l'atteso di 1-4
punti e' accettato; e' un TS **sotto** l'atteso a non avere spiegazione. Una
scheda che non elenca i suoi talenti non si giudica sul +4 dell'iniziativa.

## Uso

    python3 scripts/conformita_statblocchi.py              # rapporto per file
    python3 scripts/conformita_statblocchi.py --riepilogo  # solo i conti
    python3 scripts/conformita_statblocchi.py --json       # per chi elabora
    python3 scripts/conformita_statblocchi.py --master [FILE ...]  # i master, solo rapporto
"""
from __future__ import annotations

import argparse
import json
import functools
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import tabelle as T  # noqa: E402
from dmcore import lettura_creatura as L  # noqa: E402

# ---------------------------------------------------------------------------
# Le classi (dado, TS buoni, BAB) stanno in `dmcore.progressione`, e la scheda
# come la legge questo verificatore in `dmcore.lettura_creatura` (ADR-0066, D1:
# il verificatore condivide il lettore). Qui si importa solo quello che il
# verificatore usa; il resto si chiama dal modulo, con `P.` e `L.`.
# ---------------------------------------------------------------------------
from dmcore import progressione as P  # noqa: E402
from dmcore import sistemi as S  # noqa: E402
from dmcore import statblock as SB  # noqa: E402
from dmcore.lettura_creatura import (  # noqa: E402
    TS_CAMPO, Scheda, dadi_di_pf, leggi, non_morto_pf1e, talenti,
)


FOCALIZZATA = re.compile(r"\b(?:Weapon Focus|Arma Focalizzata)\b", re.I)
ACCURATA = re.compile(r"\b(?:Weapon Finesse|Arma Accurata)\b", re.I)
TS_CONDIVISI = re.compile(
    r"share saving throws|condivid\w+\s+(?:i\s+)?tiri salvezza"
    r"|condivide\s+(?:la|i)\s+(?:tempra|riflessi|volont[aà])\s+base", re.I)
PERFETTA = re.compile(r"\b(?:perfett[oa]|masterwork|mwk)\b", re.I)

#: I template semplici PF1e (skill `pathfinder-1e-srd`, «rebuild rules»), come
#: variazione delle caratteristiche. Advanced e' quello di `genera_creatura
#: --piu-cattivi`; Giant e' quello del bruto deforme.
TEMPLATE = {
    "Advanced": {"For": 4, "Des": 4, "Cos": 4, "Int": 4, "Sag": 4, "Car": 4},
    "Giant": {"For": 4, "Des": -2, "Cos": 4},
    "Young": {"For": -4, "Des": 4, "Cos": -4},
}

INIZIATIVA = re.compile(r"^iniziativa:\s*([+-]?\d+)", re.M)


def mod(v):
    return T.mod(v) if isinstance(v, int) else 0


# ---------------------------------------------------------------------------
# Le identita'
# ---------------------------------------------------------------------------
def bab_atteso(s: Scheda) -> int:
    return P.bab_atteso(s.gruppi)


#: SRD 3.5, tipo Costrutto: pf bonus per taglia (al posto della Costituzione).
COSTRUTTO_PF = {8: 0, 4: 0, 2: 0, 1: 10, 0: 20, -1: 30, -2: 40, -4: 60, -8: 80}


def cos_o_car(s: "Scheda", attr: dict) -> int:
    """Il modificatore che fa da Costituzione: il Carisma per un non morto PF1e."""
    return mod(attr.get("Car")) if non_morto_pf1e(s.tipo) else mod(attr.get("Cos"))


def pf_bonus(s: Scheda, attr: dict) -> "int | None":
    """Il bonus fisso ai pf: DV × mod Cos, +3 per Robustezza. None se non si sa."""
    if T.normalizza_tipo(s.tipo) == "construct":
        return None         # la fonte SRD scrive bonus che la tabella per taglia non spiega
    dv = sum(g.n for g in s.gruppi)
    return dv * cos_o_car(s, attr) + L.robustezza(s.testo, dv)


def pf_attesi(s: Scheda, attr: dict) -> "dict | None":
    """La media, e la **fascia legale**: in 3.5 i pf si tirano.

    🔴 La media e' la convenzione del Manuale dei Mostri, non la regola: PCGen
    tira i dadi, e Morlin ha 93 pf dove la media ne da' 84-88. Un pf fuori
    media e' un'informazione; un pf fuori dalla fascia che i dadi possono
    dare e' un errore.
    """
    bonus = pf_bonus(s, attr)
    if bonus is None:
        scritti = dadi_di_pf(s.testo)
        m = L.PF_DADO.search(s.testo)
        if not (scritti and m):
            return None
        bonus = sum(int(x.replace(" ", "")) for x in
                    L.BONUS_DADO.findall(L.PEZZO_DADO.sub("", m.group(1))))
    media = sum(g.n * (g.dado + 1) / 2 for g in s.gruppi)
    return {"media": math.floor(media + bonus),
            "minimo": sum(g.n for g in s.gruppi) + bonus,
            "massimo": sum(g.n * g.dado for g in s.gruppi) + bonus}


def ts_attesi(s: Scheda, attr: dict) -> "tuple[tuple, tuple]":
    """(minimo, massimo) atteso per Temp, Rifl, Vol.

    I DV razziali dell'**umanoide** hanno un TS buono che «varia» (SRD, e la
    skill `dnd-35-srd` lo scrive cosi'): lo gnoll ha buona la Tempra, il
    bugbear i Riflessi. Per quei DV il minimo li conta tutti cattivi e il
    massimo tutti buoni.
    """
    lo, hi = P.ts_base(s.gruppi)
    mods = [cos_o_car(s, attr), mod(attr.get("Des")), mod(attr.get("Sag"))]
    # Grazia divina (paladino) e Benedizione oscura (blackguard): Car a tutti i TS
    if any(g.nome.lower() in ("paladin", "paladino", "pal", "blackguard") and g.n >= 2
           for g in s.gruppi):
        mods = [m + max(0, mod(attr.get("Car"))) for m in mods]
    extra = talenti(s.testo)
    mods = [m + extra.get(c, 0) for m, c in zip(mods, ("Temp", "Rifl", "Vol"))]
    return (tuple(lo[k] + m for k, m in zip(lo, mods)),
            tuple(hi[k] + m for k, m in zip(hi, mods)))


def attacco_dichiarato(riga: str) -> "tuple[int, int] | None":
    """(bonus d'attacco, bonus di potenziamento dell'arma) dalla prima mischia."""
    m = re.search(r"([+-]\d+)(?:/[+-]\d+)*\s*\(", riga)
    if not m:
        return None
    prima = riga[:m.start()]
    pot = re.search(r"\+(\d)\s*$", prima.strip())
    return int(m.group(1)), (int(pot.group(1)) if pot else 0)


def verifica(s: Scheda, attr: "dict | None" = None, severo: bool = False) -> dict:
    """Ogni identita': (dichiarato, atteso, scarto) o None se non verificabile.

    `severo` toglie la tolleranza a tiri salvezza e attacco (DM, 2026-11-12: «un
    +4 è un bonus importante»): ogni punto in più dell'atteso deve venire da un
    talento o da un oggetto che la scheda dichiara. Senza `severo` un tiro
    salvezza fino a +4 sopra l'atteso e un attacco fra −1 e +2 passano."""
    attr = attr or s.attributi
    out = {}
    mi = INIZIATIVA.search(s.testo)
    if mi and isinstance(attr.get("Des"), int):
        # iniziativa = mod Des (+4 Iniziativa Migliorata): non dipende da
        # classi ne' DV, e nessuno la controllava
        att = mod(attr["Des"]) + talenti(s.testo).get("init", 0)
        d = int(mi.group(1)) - att
        if d == 4 and not re.search(r"\b(?:Talenti|Feats)\b", L.senza_note(s.testo), re.I):
            d = 0     # la scheda non elenca i talenti: il +4 non si verifica
        out["iniziativa"] = (int(mi.group(1)), att, d)
    dadi_scritti = any(g.bab < 0 for g in s.gruppi)
    atteso = pf_attesi(s, attr) if (s.gruppi and s.pf is not None
                                    and (s.composizione_nota or dadi_scritti)) else None
    if atteso:
        lo, hi = atteso["minimo"], atteso["massimo"]
        scarto = 0 if lo <= s.pf <= hi else (s.pf - lo if s.pf < lo else s.pf - hi)
        out["pf"] = (s.pf, f"{lo}-{hi}", scarto)
        out["pf_media"] = atteso["media"]
    # lotta e attacco tornano se tornano con **uno dei due** BAB, lo scritto o
    # il calcolato: un BAB sbagliato e' un errore solo, non tre. E si
    # controllano **anche senza composizione**: lotta = BAB + For + taglia usa
    # tre numeri che la scheda scrive, e il BAB scritto basta.
    bab = bab_atteso(s) if s.composizione_nota else None
    babs = ({bab} if bab is not None else set()) | ({s.bab} if s.bab is not None else set())
    if s.bab is not None and bab is not None:
        out["BAB"] = (s.bab, bab, s.bab - bab)
    taglia = L.taglia_di(s.testo) or L.taglia_di(f"tipo: {s.tipo}")
    if s.lotta is not None and babs:
        extra = 4 if L.LOTTA_MIGLIORATA.search(s.testo) else 0     # afferrare migliorato no
        attesi = [b + mod(attr.get("For")) + L.LOTTA_TAGLIA.get(taglia, 0) + extra for b in babs]
        att = min(attesi, key=lambda a: abs(s.lotta - a))
        out["lotta"] = (s.lotta, att, s.lotta - att)
    a = attacco_dichiarato(s.mischia) if s.mischia else None
    if a and babs:
        dich, pot = a
        # SRD, sottotipo incorporeo: senza Forza, gli attacchi in mischia usano
        # la Destrezza. Il leone spettrale (D5) risultava +3 invece di +7.
        incorporeo = re.search(r"\bincorpore", s.tipo, re.I)
        car = "Des" if (incorporeo or (ACCURATA.search(s.testo)
                                       and mod(attr.get("Des")) > mod(attr.get("For")))) else "For"
        fisso = (mod(attr.get(car)) + taglia + pot
                 + (1 if not pot and PERFETTA.search(s.mischia) else 0)
                 + (1 if FOCALIZZATA.search(s.testo) else 0)
                 + talenti(s.testo).get("attacco", 0))
        att = min((b + fisso for b in babs), key=lambda a: abs(dich - a))
        if severo and not incorporeo:
            # senza tolleranza serve il conto fine di `attacco_atteso`: il
            # potenziamento in mezzo al nome («+1 gelido»), Arma Focalizzata
            # solo sull'arma che nomina, Arma Focalizzata Superiore
            righe_car = " ".join(f"{k} {v}" for k, v in attr.items() if isinstance(v, int))
            fini = [x[1] for x in (attacco_atteso(s.mischia, b, righe_car, L.senza_note(s.testo), taglia)
                                   for b in babs) if x]
            if fini:
                extra = talenti(s.testo).get("attacco", 0)
                att = min((f + extra for f in fini), key=lambda a: abs(dich - a))
        d = dich - att
        out["attacco"] = (dich, att, d if severo or not -1 <= d <= 2 else 0)
    if not s.composizione_nota:
        return out
    if s.ts:
        lo, hi = ts_attesi(s, attr)
        # SRD, cavalcatura del paladino e famiglio («Share Saving Throws»): per
        # ogni TS vale la base più alta fra la sua e quella del padrone, che
        # non è in questa scheda. Sopra l'atteso non si può giudicare.
        condivisi = bool(TS_CONDIVISI.search(L.senza_note(s.testo)))
        for nome, dich, a, b in zip(("Temp", "Rifl", "Vol"), s.ts, lo, hi):
            if condivisi and dich > b:
                out[nome] = (dich, f"{a} o la base del padrone", 0)
                continue
            largo = 0 if severo else 4
            d = 0 if a <= dich <= b + largo else (dich - a if dich < a else dich - b - largo)
            out[nome] = (dich, a if a == b else f"{a}..{b}", d)
    return out


def scarti(esito: dict) -> dict:
    return {k: v for k, v in esito.items() if isinstance(v, tuple) and v[2] != 0}


def con_template(attr: dict, nome: str) -> dict:
    return {k: (v + TEMPLATE[nome].get(k, 0) if isinstance(v, int) else v)
            for k, v in attr.items()}


PIANO_DECISIONI = ROOT / "plans" / "RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI.md"


def decisioni_aperte() -> dict:
    """{nome del file: D<n>} per le decisioni ancora aperte (ADR-0047).

    La fonte e' la tabella del piano, marcata `decisioni-dm`: una decisione
    barrata (`~~D1~~`) e' chiusa e il suo statblocco torna a essere giudicato.
    """
    fuori, dentro = {}, False
    for riga in PIANO_DECISIONI.read_text(encoding="utf-8").splitlines():
        if riga.strip() == "<!-- decisioni-dm: CONFORMITA-STATBLOCCHI -->":
            dentro = True
            continue
        m = re.match(r"^\|\s*(D\d+)\s*\|\s*`([^`]+)`", riga) if dentro else None
        if m:
            fuori[m.group(2) + ".md"] = m.group(1)
    return fuori


VARIANTE = re.compile(r"^.*\bVariante\b.*\bAdvanced\b.*$", re.M | re.I)


def verifica_variante_advanced(s: Scheda) -> dict:
    """La variante Advanced che una scheda descrive in prosa torna con la regola?

    PF1e, rebuild: +4 a tutte le caratteristiche e +2 di armatura naturale,
    quindi **pf +2 per DV** (Cos +4) e **CA +4** (+2 naturale, +2 da Des +4),
    e GS +1. 🔎 Il primo caso misurato, Ghaurush «Cenere Piena», scrive CA 23:
    conta l'armatura naturale e dimentica la Destrezza.
    """
    m = VARIANTE.search(L.senza_note(s.testo))
    if not m or s.pf is None:
        return {}
    riga, out = m.group(0), {}
    dv = sum(g.n for g in s.gruppi) or sum(n for n, _ in (L.dadi_vita(s.testo) or ([], 0, ""))[0])
    ca = re.search(r"^ca:\s*(\d+)", s.testo, re.M)
    mp, mc = re.search(r"\bhp\s*(\d+)", riga), re.search(r"\bCA\s*(\d+)", riga)
    if mp and dv:
        att = s.pf + 2 * dv
        out["variante pf"] = (int(mp.group(1)), att, int(mp.group(1)) - att)
    if mc and ca:
        att = int(ca.group(1)) + 4
        out["variante CA"] = (int(mc.group(1)), att, int(mc.group(1)) - att)
    mg = re.search(r"\bCR\s*(\d+)", riga)
    if mg:
        att = int(s.gs) + 1
        out["variante GS"] = (int(mg.group(1)), att, int(mg.group(1)) - att)
    return out


def template_dichiarati(testo: str) -> "list[str]":
    """I template che la scheda dichiara in Source, Boost log o titolo."""
    righe = [r for r in testo.splitlines()
             if r.startswith(("# ", "**Faction**", "**Source**", "Boost log"))]
    fuori = []
    for nome, regex in (("Advanced", r"\bAdvanced\b"), ("Giant", r"\*?\bGiant\b\*?\s*\(|template semplice PF1e \*\*Giant"),
                        ("Young", r"\bYoung\b(?! Adult)"), ("Skeleton", r"\bSkeleton\b"),
                        ("Ghost", r"\bGhost template\b"), ("Mezzo-immondo", r"mezzo-immondo|half-fiend")):
        if any(re.search(regex, r, re.I) for r in righe):
            fuori.append(nome)
    return fuori


def giudica(s: Scheda, severo: bool = False) -> dict:
    esito = verifica(s, severo=severo)
    esito.update(verifica_variante_advanced(s))
    fuori = scarti(esito)
    spiegazione = None
    # la variante in prosa si confronta con la sua regola, e un'ipotesi di
    # template su caratteristiche **scelte** non spiega niente
    if fuori and s.provenienza != "generate" and not any(k.startswith("variante") for k in fuori):
        for nome in TEMPLATE:
            if not scarti(verifica(s, con_template(s.attributi, nome), severo=severo)):
                spiegazione = nome
                break
    come_la_fonte = []
    if fuori and s.provenienza == "trascritte":
        fonte = L.numeri_della_fonte(s.testo)
        come_la_fonte = [k for k, v in fuori.items() if fonte.get(k) == v[0]]
    decisione = decisioni_aperte().get(s.file.name) if fuori else None
    percorso = s.file.relative_to(ROOT) if s.file.is_relative_to(ROOT) else s.file
    return {"file": str(percorso), "provenienza": s.provenienza,
            "verificabile": bool(esito), "esito": esito, "scarti": fuori,
            "template": spiegazione, "come_la_fonte": come_la_fonte,
            "decisione": decisione, "template_dichiarati": template_dichiarati(s.testo)}


#: F4 di ADR-0112: le schede di un sistema che non legge le tabelle 3.5 di
#: questo verificatore si saltano, e si dice perché (`saltate()`).
STRUMENTO = "conformita_statblocchi"
_SALTATE: "dict[str, list[str]]" = {}


def del_sistema(p: Path) -> bool:
    """True se le tabelle 3.5 del verificatore valgono per il sistema del file `p`."""
    sistema = S.sistema_di(p)
    diverse = S.regole_diverse(sistema, STRUMENTO)
    if diverse:
        rel = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
        _SALTATE[rel] = [sistema] + diverse
    return not diverse


def saltate() -> "dict[str, list[str]]":
    """{file: [sistema, capacità diverse…]} delle schede saltate fin qui."""
    return dict(_SALTATE)


def tutte() -> "list[dict]":
    fuori = []
    for p in sorted(ROOT.glob("Bestiario/**/*-cr*.md")):
        if not del_sistema(p):
            continue
        s = leggi(p)
        if s:
            fuori.append(giudica(s))
    return fuori


def riepilogo(giudizi: "list[dict]") -> dict:
    conto = {"statblocchi": len(giudizi), "verificabili": 0, "tornano": 0,
             "spiegati_da_template": 0, "come_la_fonte": 0, "decisioni_aperte": 0,
             "da_correggere": 0,
             "del_generatore": 0}
    for g in giudizi:
        if not g["verificabile"]:
            continue
        conto["verificabili"] += 1
        if not g["scarti"]:
            conto["tornano"] += 1
        elif g["template"]:
            conto["spiegati_da_template"] += 1
        elif g["come_la_fonte"] and set(g["come_la_fonte"]) == set(g["scarti"]):
            conto["come_la_fonte"] += 1
        elif g["decisione"]:
            conto["decisioni_aperte"] += 1
        elif g["provenienza"] == "generate":
            conto["del_generatore"] += 1
        else:
            conto["da_correggere"] += 1
    return conto


# ---------------------------------------------------------------------------
# La correzione di `pf-dado`
# ---------------------------------------------------------------------------
#: La marca delle righe `pf-dado` riscritte da qui: specifica, come quella di
#: genera_attributi, perche' un secondo giro deve riconoscerle.
MARCA_PF = "> [GENERATO] `pf-dado` "
AFFIDABILI = ("trascritte", "copiate", "a mano")


def _formula(dadi: list, bonus: int) -> str:
    testo = "+".join(f"{n}d{f}" for n, f in dadi)
    return testo + (f"{bonus:+d}" if bonus else "")


def pf_dado_corretto(s: Scheda, forza: bool = False) -> "dict | None":
    """Il `pf-dado` giusto per una scheda il cui campo non registra i DV.

    I **dadi**: la formula che la scheda scrive («DV 4d8 + 6d12»), altrimenti
    le classi del `tipo` coi dadi SRD piu' i DV razziali dichiarati. Il
    **bonus**: quello scritto nella formula; altrimenti DV × mod Cos (+3 per
    Robustezza) se la Cos e' un dato; se e' generata, si ricava dai pf, perche'
    i pf sono il numero del DM e la Cos generata no. None se i dadi non si
    ricostruiscono senza indovinare.
    """
    motivo = L.pf_dado_sospetto(s.testo, s.gs)
    if (not motivo and not forza) or s.pf is None or not L.PF_DADO.search(s.testo):
        return None
    dv = L.dadi_vita(s.testo)
    if forza and dv and dv[2] == "pf-dado":
        # la ricostruzione non puo' partire dal campo che sta verificando
        dv = None
    if dv and dv[2] == "formula scritta":
        dadi, bonus, da_dove = dv[0], dv[1], "dalla formula che la scheda scrive"
    elif s.composizione_nota and s.gruppi and all(g.bab >= 0 for g in s.gruppi):
        # stesse facce in un gruppo solo, come scrive l'SRD («8d10», non «6d10+2d10»)
        facce = {}
        for g in s.gruppi:
            facce[g.dado] = facce.get(g.dado, 0) + g.n
        dadi, bonus = [(n, f) for f, n in facce.items()], None
        da_dove = "dalle classi del `tipo` coi dadi SRD" + (
            " e dai DV razziali dichiarati" if any(g.nome.lower() in T.TIPI for g in s.gruppi) else "")
    else:
        return None
    hd = sum(n for n, _ in dadi)
    media = sum(n * (f + 1) / 2 for n, f in dadi)
    robusto = L.robustezza(s.testo, sum(n for n, _ in dadi))
    tipo = T.normalizza_tipo(s.tipo)
    if bonus is not None:
        da_bonus = "è quello scritto nella formula"
    elif tipo == "undead":
        bonus, da_bonus = 0, "è zero: un non morto non ha Costituzione"
    elif tipo == "construct":
        return None
    elif s.provenienza in AFFIDABILI and isinstance(s.attributi.get("Cos"), int):
        bonus = hd * mod(s.attributi["Cos"]) + robusto
        da_bonus = f"da Cos {s.attributi['Cos']}" + (
            " e Robustezza Migliorata" if L.ROBUSTEZZA_MIGLIORATA.search(s.testo)
            else " e Robustezza" if robusto else "")
    else:
        # 🐛 **Il giro circolare** (2026-09-23): il bonus si ricavava dai pf
        # **supponendo la media**, e poi `genera_attributi.cos_da_pf` ricavava
        # la Cos da questo bonus. Il generatore confermava se stesso, e Khorn,
        # che scrive «8d10+24, Cos 16» e Tempra +9, finiva con Cos 18. In 3.5
        # i pf **si tirano**, e la media e' una convenzione; la Tempra e'
        # un'identita' esatta. Viene prima lei, se i pf stanno nella fascia.
        tetto = L.tetti_dai_ts(str(s.file), s.testo).get("Cos")
        m = tetto[0] if tetto else None
        if m is not None and L.plausibile(m, s.gs) and \
                hd + hd * m + robusto <= s.pf <= sum(n * f for n, f in dadi) + hd * m + robusto:
            bonus = hd * m + robusto
            temp = TS_CAMPO.search(s.testo).group(1)
            da_bonus = f"ricavato dalla Tempra {temp} (la Cos di questa scheda è generata)"
        else:
            m = round((s.pf - media - robusto) / hd)
            if not L.plausibile(m, s.gs):
                return None
            bonus = hd * m + robusto
            da_bonus = f"ricavato dai pf {s.pf} (la Cos di questa scheda è generata)"
    nuovo = _formula(dadi, bonus)
    vecchio = L.PF_DADO.search(s.testo).group(1).strip()
    lo, hi = hd + bonus, sum(n * f for n, f in dadi) + bonus
    return {"file": s.file, "vecchio": vecchio, "nuovo": nuovo, "motivo": motivo,
            "dadi": da_dove, "bonus": da_bonus, "media": math.floor(media + bonus),
            "pf": s.pf, "legale": lo <= s.pf <= hi, "fascia": (lo, hi)}


def _togli_pf_dado(p: Path, s: Scheda) -> dict:
    """Il campo porta un'arma e i DV non si ricostruiscono: si toglie.

    E' la regola che `dmcore/statblock.py` scrive da settembre, «meglio nessun
    dado vita che un dado vita preso da un attacco». I dadi di una classe di
    prestigio non SRD non si indovinano.
    """
    vecchio = L.PF_DADO.search(s.testo).group(1).strip()
    motivo = L.pf_dado_sospetto(s.testo, s.gs)
    t = p.read_text(encoding="utf-8")
    t = re.sub(r"^pf-dado:.*\n", "", t, count=1, flags=re.M)
    marca = (f"{MARCA_PF}tolto da `scripts/conformita_statblocchi.py`: portava «{vecchio}», "
             f"che non sono i dadi vita ({motivo}). I dadi non si ricostruiscono senza "
             "inventare: la composizione delle classi non e' leggibile o comprende una classe "
             "non SRD. Da completare a mano.")
    m = L.BLOCCO.search(t)
    fine = t.index("```", m.end(1)) + 3
    p.write_text(t[:fine] + "\n\n" + marca + t[fine:], encoding="utf-8")
    return {"file": p, "vecchio": vecchio, "nuovo": "(tolto)", "media": "-", "pf": s.pf,
            "legale": True, "fascia": None}


RIGA_MARCA_PF = re.compile("^" + re.escape(MARCA_PF) + r"corretto.*$", re.M)


def _marca_corretto(c: dict, arma: str) -> str:
    marca = (f"{MARCA_PF}corretto da `scripts/conformita_statblocchi.py`: era "
             f"«{c['vecchio']}», {arma}. I dadi vengono {c['dadi']}, il bonus {c['bonus']}.")
    if not c["legale"]:
        marca += (f" ⚠ I pf {c['pf']} stanno fuori dalla fascia che questi dadi possono "
                  f"dare ({c['fascia'][0]}-{c['fascia'][1]}): da verificare.")
    return marca


def rigenera_pf_dado(scrivi: bool) -> "list[dict]":
    """Riscrive i soli `pf-dado` gia' corretti da qui, se la regola ora da' altro.

    Serve quando cambia un ingresso della ricostruzione: la provenienza della
    Cos (una scheda che scrive le sue caratteristiche), un talento letto meglio.
    Il valore originale resta nella marca: «era …» non si perde mai.
    """
    fatte = []
    for p in sorted(ROOT.glob("Bestiario/**/*-cr*.md")):
        if not del_sistema(p):
            continue
        t = p.read_text(encoding="utf-8")
        vecchia = RIGA_MARCA_PF.search(t)
        s = leggi(p) if vecchia else None
        c = pf_dado_corretto(s, forza=True) if s else None
        ora = L.PF_DADO.search(t)
        if not (c and ora):
            continue
        m = re.search(r"era «([^»]+)», ([^.]+)\.", vecchia.group(0))
        c["vecchio"], arma = m.group(1), m.group(2)
        nuova = _marca_corretto(c, arma)
        if c["nuovo"] == ora.group(1).strip() and nuova == vecchia.group(0):
            continue
        fatte.append(c)
        if scrivi:
            t = re.sub(r"^pf-dado:.*$", lambda _: f"pf-dado: {c['nuovo']}", t, count=1, flags=re.M)
            t = RIGA_MARCA_PF.sub(lambda _: nuova, t, count=1)
            p.write_text(t, encoding="utf-8")
    return fatte


def correggi_pf_dado(scrivi: bool) -> "list[dict]":
    fatte = rigenera_pf_dado(scrivi)
    for p in sorted(ROOT.glob("Bestiario/**/*-cr*.md")):
        if not del_sistema(p):
            continue
        s = leggi(p)
        c = pf_dado_corretto(s) if s else None
        if not c and s and L.pf_dado_sospetto(s.testo, s.gs):
            if scrivi:
                fatte.append(_togli_pf_dado(p, s))
            else:
                fatte.append({"file": p, "vecchio": L.PF_DADO.search(s.testo).group(1).strip(),
                              "nuovo": "(da togliere)", "media": "-", "pf": s.pf,
                              "legale": True, "fascia": None})
            continue
        if not c:
            continue
        fatte.append(c)
        if not scrivi:
            continue
        t = p.read_text(encoding="utf-8")
        t = re.sub(r"^pf-dado:.*$", lambda _: f"pf-dado: {c['nuovo']}", t, count=1, flags=re.M)
        arma = "il danno di un'arma, che resta in `attacchi`" if "sembra" in c["motivo"] or \
            "dado solo" in c["motivo"] or "classi del tipo tirano" in c["motivo"] or \
            "dichiara" in c["motivo"] else "una parte sola dei dadi vita"
        marca = _marca_corretto(c, arma)
        m = L.BLOCCO.search(t)
        fine = t.index("```", m.end(1)) + 3
        t = t[:fine] + "\n\n" + marca + t[fine:]
        p.write_text(t, encoding="utf-8")
    return fatte


def controlla_pf_dado() -> "list[str]":
    """Il gate: ogni `pf-dado` riscritto da qui e' ancora quello che la regola da'."""
    problemi = []
    for p in sorted(ROOT.glob("Bestiario/**/*-cr*.md")):
        if not del_sistema(p):
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        if MARCA_PF + "corretto" in t:
            s = leggi(p)
            c = pf_dado_corretto(s, forza=True) if s else None
            ora = L.PF_DADO.search(t)
            if not c or not ora or c["nuovo"] != ora.group(1).strip() or \
                    f"il bonus {c['bonus']}." not in t:
                problemi.append(f"{p.name}: pf-dado «{ora.group(1).strip() if ora else '—'}», "
                                f"la regola da' «{c['nuovo'] if c else 'niente'}»")
        if MARCA_PF + "tolto" in t and L.PF_DADO.search(t):
            problemi.append(f"{p.name}: il `pf-dado` tolto e' tornato")
        if t.count(MARCA_PF) > 1:
            problemi.append(f"{p.name}: due marche `pf-dado` — la correzione non e' idempotente")
        if L.pf_dado_sospetto(t):
            problemi.append(f"{p.name}: {L.pf_dado_sospetto(t)}")
    return problemi


# ---------------------------------------------------------------------------
# Gli statblocchi scritti nei master (D7 di MASTER-DEF, 2026-10-18)
# ---------------------------------------------------------------------------
#: Nel giro su ARC-07 sei delle nove discrepanze con l'SRD erano aritmetica
#: (CA, pf, lotta) dentro i master, dove questo controllo non guardava. I master
#: scrivono lo statblocco nella forma `**Campo:** valore`, non in quella del
#: Bestiario, quindi qui si leggono solo i quattro conti che non chiedono la
#: composizione delle classi. E' un **rapporto**: segnala, non blocca la CI,
#: perche' i master hanno proprietari diversi (ARC-07 e' di un altro thread).
CAMPO_MASTER = re.compile(
    r"^\*\*(Caratteristiche|Iniziativa|CA|PF|Attacco Base|Lotta|Talenti|Attacco|Attacco Completo):\*\*\s*(.*)$")
TITOLO = re.compile(r"^#{2,6}\s+(.+?)\s*$")
DADI = re.compile(r"(\d+)d(\d+)")
#: Il modificatore speciale di taglia per la lotta (SRD, Combat II), letto dal
#: modificatore di taglia alla CA: Piccola +1 → −4, Grande −1 → +4, Enorme −2 → +8,
#: Mastodontica −4 → +12, Colossale −8 → +16.
LOTTA_DA_CA = {1: -4, 2: -8, 4: -12, 0: 0, -1: 4, -2: 8, -4: 12, -8: 16}


def _blocchi_del_master(testo: str):
    """Ogni gruppo di righe `**Campo:**` contigue (fino a 40 righe) che ha almeno pf e CA."""
    righe = testo.split("\n")
    titolo, blocco = "", None
    for n, r in enumerate(righe, 1):
        t = TITOLO.match(r)
        if t:
            if blocco and "PF" in blocco["campi"]:
                yield blocco
            titolo, blocco = re.sub(r"[*#]", "", t.group(1)).strip(), None
            continue
        m = CAMPO_MASTER.match(r.strip())
        if not m:
            continue
        nome, valore = m.groups()
        if blocco is None or nome in blocco["campi"] or n - blocco["ultima"] > 40:
            if blocco and "PF" in blocco["campi"]:
                yield blocco
            blocco = {"titolo": titolo, "riga": n, "campi": {}, "ultima": n}
        blocco["campi"][nome] = (n, valore)
        blocco["ultima"] = n
    if blocco and "PF" in blocco["campi"]:
        yield blocco


#: Il primo attacco di una riga «Attacco»: il bonus, e quello che gli sta
#: davanti (il nome dell'arma, che puo' portare il potenziamento «+1»).
PRIMO_ATTACCO = re.compile(
    r"([+-]\d+)(?:/[+-]\d+)*\s*(?:in mischia|a distanza|di contatto|contatto)?\s*\(")
DISTANZA = re.compile(r"a distanza|\b(?:arco|balestra|balist[ae]|giavellott|fionda|dardi?)\b", re.I)
#: SRD 3.5, *Siege Engines*, ballista: «a Medium creature takes a -4 penalty on
#: attack rolls when using a ballista, and a Small creature takes a -6 penalty».
BALISTA = re.compile(r"\bbalist[ae]\b", re.I)
FOCALIZZATA_SUP = re.compile(
    r"\b(?:Greater Weapon Focus|Arma Focalizzata Superiore)\b(?:\s*[(:]\s*([^),;·\n]+))?", re.I)


def attacco_atteso(riga: str, bab: int, car: str, talenti_: str,
                   taglia: int) -> "tuple[int, int, str] | None":
    """(scritto, atteso, come) del primo attacco della riga, o None se non si legge.

    SRD 3.5, *Attack Bonus*: BAB + mod For in mischia (Des a distanza o con
    Arma Accurata) + modificatore di taglia + potenziamento dell'arma (+1 se
    perfetta e senza potenziamento) + 1 con Arma Focalizzata, + 1 ancora con
    Arma Focalizzata Superiore. Gli altri bonus (morale, oggetti, incantesimi)
    la scheda li deve scrivere: un numero che la regola non spiega e' uno scarto.
    """
    m = PRIMO_ATTACCO.search(riga)
    if not m:
        return None
    prima = riga[:m.start()].strip().strip("*").strip()
    arma = _nome_dell_arma(prima)
    pot = re.search(r"\+(\d)\b(?!\s*/)", arma)
    pot = int(pot.group(1)) if pot else 0
    a_distanza = bool(DISTANZA.search(riga[:m.end()]))
    in_ira = bool(IN_IRA.search(arma) or IN_IRA.match(riga[m.end():].split(";")[0].rsplit(")", 1)[-1]))
    car_ = car
    if in_ira:
        ira = FOR_IN_IRA.search(car + " " + talenti_)
        if ira:
            car_ = f"For {ira.group(1)} " + re.sub(r"For\s+\d+", "", car)
    f, d = _mod_caratteristica(car_, "For"), _mod_caratteristica(car_, "Des")
    if a_distanza or (ACCURATA.search(talenti_) and d is not None and f is not None and d > f):
        quale, mc = "Des", d
    else:
        quale, mc = "For", f
    if mc is None:
        return None
    perfetta = 1 if not pot and (PERFETTA.search(arma) or re.search(r"\bda maestro\b", arma, re.I)) else 0
    foc = (1 if _focalizzata_su(FOCALIZZATA_BASE, arma, talenti_) else 0) \
        + (1 if _focalizzata_su(FOCALIZZATA_SUP, arma, talenti_) else 0)
    adde = ADDESTRAMENTO.search(talenti_)
    adde = int(adde.group(1)) if adde else 0
    balista = 0
    if BALISTA.search(arma):
        balista = -4 if taglia == 0 else -6 if taglia > 0 else 0
    atteso = bab + mc + taglia + pot + perfetta + foc + adde + balista
    come = (f"BAB {bab:+d}, {quale} {mc:+d}{' in Ira' if in_ira and car_ != car else ''}, "
            f"taglia {taglia:+d}, arma {pot + perfetta:+d}, talenti {foc:+d}"
            + (f", addestramento nelle armi {adde:+d}" if adde else "")
            + (f", balista puntata da una creatura più piccola di Grande {balista:+d}" if balista else ""))
    return int(m.group(1)), atteso, come


#: «in Ira» accanto al primo attacco, e la Forza che la scheda dichiara in Ira.
IN_IRA = re.compile(r"\s*\**\s*in Ira\b", re.I)
FOR_IN_IRA = re.compile(r"For\s+\d+\s*\((\d+) in Ira\)", re.I)
#: PF1e, *weapon training* del guerriero: vale solo se la scheda lo scrive.
ADDESTRAMENTO = re.compile(r"addestramento nelle armi[^·\n+]*\+(\d)", re.I)
#: Arma Focalizzata senza la Superiore, col nome dell'arma fra parentesi o dopo i due punti.
FOCALIZZATA_BASE = re.compile(
    r"\b(?<!Greater )(?:Weapon Focus|Arma Focalizzata)\b(?! Superiore)(?:\s*[(:]\s*([^),;·\n]+))?", re.I)


def _nome_dell_arma(prima: str) -> str:
    """L'ultimo nome d'arma davanti al bonus: quello che sta dopo l'ultimo separatore."""
    senza = re.sub(r"\([^)]*\)", "", prima)
    return re.split(r";|·|\*\*|\boppure\b|\be\b(?=\s+\w+\s+[+-]?\d)|:", senza)[-1].strip()


def _focalizzata_su(talento: "re.Pattern", arma: str, testo: str) -> bool:
    """Il talento conta per quest'arma. Se nomina un'altra arma che la scheda usa, no."""
    trovati = list(talento.finditer(testo))
    if not trovati:
        return False
    for t in trovati:
        nome = (t.group(1) or "").strip().lower() if talento.groups else ""
        if not nome:
            return True
        radice = re.split(r"\s+", nome)[0][:-1] or nome
        if radice in arma.lower():
            return True
        righe = [r for r in testo.split("\n") if PRIMO_ATTACCO.search(r)]
        # le voci «  - …» del recinto sono nella lingua della riga che si giudica
        righe = [r for r in righe if r.lstrip().startswith("- ")] or righe
        attacchi = " ".join(re.sub(r"\([^)]*\)", "", r.lower()) for r in righe)
        if radice not in attacchi:
            return True          # l'arma del talento non è fra gli attacchi: nome tradotto, vale
    return False


def _mod_caratteristica(car: str, quale: str) -> "int | None":
    m = re.search(quale + r"\s+(\d+)", car)
    return mod(int(m.group(1))) if m else None


@functools.cache
def regole_conformita(sistema: str = "dnd35") -> dict:
    """I conti che si fanno nel `sistema` e come si arrotondano i pf (`creature.conformita`)."""
    return S.dati(sistema, "creature.conformita")


def fa(sistema: str, conto: str) -> bool:
    return conto in regole_conformita(sistema).get("conti", {}).get("fatti", ())


def in_prova(sistema: str, conto: str) -> bool:
    """ADR-0119: un conto nuovo si fa, ma il cancello lo stampa come avviso finché è in prova."""
    return conto in regole_conformita(sistema).get("conti", {}).get("in_prova", ())


def controlla(sistema: str, conto: str) -> bool:
    return fa(sistema, conto) or in_prova(sistema, conto)


def conti_saltati(sistema: str) -> "dict[str, str]":
    """{conto: perché} dei conti che nel `sistema` non hanno ancora la regola."""
    return dict(regole_conformita(sistema).get("conti", {}).get("mancanti", {}))


def _arrotonda(modo: str):
    return math.ceil if modo == "su" else math.floor


def conti_del_master(blocco: dict, sistema: str = "dnd35") -> "list[dict]":
    c = {k: v[1] for k, v in blocco["campi"].items()}
    fuori = []
    media_pf = _arrotonda(regole_conformita(sistema)["punti_ferita"]["media"])

    def scarto(campo, scritto, atteso, nota=""):
        fuori.append({"campo": campo, "riga": blocco["campi"][campo][0],
                      "scritto": scritto, "atteso": atteso, "nota": nota})

    # pf: la media dei dadi, arrotondata in basso sul totale, piu' il bonus
    m = re.match(r"\s*(\d+)\s*\(([^)]*)\)", c.get("PF", ""))
    if m and fa(sistema, "pf"):
        dentro = m.group(2).split(";")[-1]
        dadi = DADI.findall(dentro)
        bonus = re.search(r"\d+d\d+\s*([+-]\s*\d+)\s*$", dentro.strip())
        if dadi and (bonus or re.fullmatch(r"[\dd+\s]+", dentro.strip())):
            media = media_pf(sum(int(n) * (int(f) + 1) / 2 for n, f in dadi))
            atteso = media + (int(bonus.group(1).replace(" ", "")) if bonus else 0)
            if atteso != int(m.group(1)):
                scarto("PF", int(m.group(1)), atteso, f"media dei dadi {media}")
    # CA: 10 piu' le voci fra parentesi, se la parentesi le elenca
    m = re.match(r"\s*(\d+)\s*\(([^)]*)\)", c.get("CA", ""))
    taglia_ca = 0
    if m and fa(sistema, "CA") and not re.search(r"forma|con \*", m.group(2)):
        # una voce e' un numero col segno seguito dal suo nome («+6 giaco di
        # maglia +2»: il +2 e' il potenziamento, gia' dentro il +6)
        voci = re.findall(r"([+-]\s*\d+)\s+[^\W\d_]", m.group(2).replace("−", "-"))
        tg = re.search(r"([+-]\d+)\s*taglia", m.group(2).replace("−", "-"))
        taglia_ca = int(tg.group(1)) if tg else 0
        if voci:
            atteso = 10 + sum(int(v.replace(" ", "")) for v in voci)
            if atteso != int(m.group(1)):
                scarto("CA", int(m.group(1)), atteso, "10 più le voci fra parentesi")
    car = c.get("Caratteristiche", "")
    # iniziativa: mod Des, +4 con Iniziativa Migliorata (solo se i talenti sono scritti)
    m = re.match(r"\s*([+-]\d+)", c.get("Iniziativa", ""))
    des = _mod_caratteristica(car, "Des")
    if m and des is not None and "Talenti" in c and fa(sistema, "iniziativa"):
        atteso = des + (4 if re.search(r"Iniziativa Migliorata|Improved Initiative", c["Talenti"]) else 0)
        if int(m.group(1)) < atteso:
            scarto("Iniziativa", int(m.group(1)), atteso, "mod Des, +4 con Iniziativa Migliorata")
    # lotta: BAB + mod For + taglia
    mb = re.match(r"\s*\+?(\d+)", c.get("Attacco Base", ""))
    ml = re.match(r"\s*([+-]\d+)", c.get("Lotta", ""))
    forza = _mod_caratteristica(car, "For")
    if mb and ml and forza is not None and taglia_ca in LOTTA_DA_CA and fa(sistema, "lotta"):
        atteso = int(mb.group(1)) + forza + LOTTA_DA_CA[taglia_ca]
        if int(ml.group(1)) != atteso:
            scarto("Lotta", int(ml.group(1)), atteso, "BAB + For + taglia")
    # attacco (ADR-0118): BAB + For o Des + taglia + arma + talenti, esatto
    riga_att = "Attacco" if "Attacco" in c else "Attacco Completo" if "Attacco Completo" in c else None
    if riga_att and mb and fa(sistema, "attacco"):
        conto = attacco_atteso(c[riga_att], int(mb.group(1)), car, c.get("Talenti", ""), taglia_ca)
        if conto and conto[0] != conto[1]:
            scarto(riga_att, conto[0], conto[1], conto[2])
    return fuori


# ---------------------------------------------------------------------------
# Gli statblocchi recintati nei master (ADR-0091), 2026-11-03
# ---------------------------------------------------------------------------
#: Il controllo qui sopra legge solo la forma `**Campo:**`. I master di ARC-07
#: scrivono i boss nella forma di ADR-0091: un recinto ```statblocco``` e,
#: sotto, le righe **Difesa** / **Attacco** / **Statistiche** / **Capacità
#: speciali**. Diciannove blocchi, fra cui Skullcrusher e Zog'tar, non li
#: guardava nessuno. La lettura del DM e del playtester del 2026-11-03 ci ha
#: trovato due CD dell'Adulto rimaste nel Vecchio tramite «come A.1» e una
#: scurovisione mancante. Questi conti sono quelli che una regola SRD fissa:
#:
#: | conto | la regola |
#: |---|---|
#: | pf | media dei dadi di `pf-dado` più il bonus |
#: | CA | 10 più le voci di `ca-dettaglio` |
#: | recinto e prosa | la CA e i pf della riga **Difesa** sono quelli del recinto |
#: | CD del soffio e dello schiacciare | 10 + ½ DV + mod COS (+2 con Capacità Focalizzata) |
#: | CD della presenza terrificante o minacciosa | 10 + ½ DV + mod CAR |
#: | CD di *corrompere l'acqua* | quella della presenza terrificante (SRD, *Dragon, True*, drago nero) |
#: | «come A.n» | una voce ereditata con una CD non vale più se DV o caratteristiche cambiano |
#: | scurovisione | i tipi che nell'SRD la hanno la scrivono nei sensi |
#:
#: ⚠️ Quando i talenti sono ereditati («quelli di A.1») il +2 di Capacità
#: Focalizzata non si sa: si accettano tutte e due le CD, e lo si dice.
RECINTO = re.compile(r"^```statblocco\s*$")
_ETICHETTA_PROSA = re.compile(r"^\*\*(Difesa|Attacco|Statistiche|Iniziativa|Capacità speciali|Tattiche)\*\*")
#: I tipi che nell'SRD 3.5 hanno scurovisione, con la voce che lo dice.
#: Un nome per riga, per poterlo controllare: orco e ogre (18 m, *Orc*, *Ogre*),
#: nano e duergar (18 m, razze e *Dwarf*), drago (36 m, *Dragon* tipo), troll
#: (27 m, *Troll*), gnoll e goblin (18 m), gigante (18 m, *Giant* tipo).
SCUROVISIONE_SRD = re.compile(
    r"\b(?:Orc[oh]i?|Ogre|Nan[oi]|Duergar|Drag[oh]i?|Troll|Gnoll|Goblin|Gigante)\b", re.I)


def _int(s: str) -> "int | None":
    m = re.match(r"\s*([+-]?\d+)", s or "")
    return int(m.group(1)) if m else None


def _recinti_del_master(testo: str):
    """Ogni recinto ```statblocco``` con il titolo sopra e la prosa sotto.

    La prosa finisce al titolo dopo o al recinto dopo: e' la parte che il DM
    legge, e le CD stanno li', non nel recinto.
    """
    righe = testo.split("\n")
    titolo, i = "", 0
    while i < len(righe):
        t = TITOLO.match(righe[i])
        if t:
            titolo = re.sub(r"[*#`]", "", t.group(1)).strip()
        if not RECINTO.match(righe[i]):
            i += 1
            continue
        try:
            fine = next(j for j in range(i + 1, len(righe)) if righe[j].strip() == "```")
        except StopIteration:
            return
        try:
            sb = SB.leggi("\n".join(righe[i:fine + 1]))
        except SB.StatblockError:
            sb = None
        j = fine + 1
        while j < len(righe) and not TITOLO.match(righe[j]) and not RECINTO.match(righe[j]):
            j += 1
        if sb is not None:
            yield {"titolo": titolo, "riga": i + 1, "sb": sb,
                   "prosa": "\n".join(righe[fine + 1:j]), "riga_prosa": fine + 2}
        i = j


def _dv(sb) -> "int | None":
    # tutti i gruppi di dadi: «12d8+4d10+80» sono 16 DV, non 12 (lotto 1-bis di ADR-0126:
    # la CD del soffio di Azarr Kul risultava 21 invece di 23)
    dadi = re.findall(r"(\d+)d\d+", (sb.pf_dado or "").split("(")[0])
    if dadi:
        return sum(int(n) for n in dadi)
    m = re.match(r"\s*(\d+)\s*DV", sb.pf_dado or "")
    return int(m.group(1)) if m else None


def _voce_bold(prosa: str, nome: str) -> "str | None":
    """Il testo dopo `**nome…**` fino al prossimo « · » o alla fine della riga."""
    m = re.search(r"\*\*(" + nome + r")[^*]*\*\*([^\n]*)", prosa, re.I)
    if not m:
        return None
    return m.group(2).split(" · ")[0]


def _cd(testo: "str | None") -> "int | None":
    m = re.search(r"\bCD\s+(\d+)", testo or "")
    return int(m.group(1)) if m else None


def conti_del_recinto(b: dict, fratelli: "dict[str, dict]" = None,
                      sistema: str = "dnd35") -> "list[dict]":
    """I conti di un recinto che una regola del `sistema` fissa (tabella qui sopra).

    Quali conti valgono e come si arrotondano i pf lo dice il plugin
    (`creature.conformita`): un conto senza regola nel sistema non si fa.
    """
    sb, prosa, fuori = b["sb"], b["prosa"], []
    regole_pf = regole_conformita(sistema)["punti_ferita"]

    def scarto(campo, scritto, atteso, nota, conto=None):
        x = {"campo": campo, "riga": b["riga"], "scritto": scritto, "atteso": atteso, "nota": nota}
        # il conto resta scritto anche dopo la promozione (testing → stable):
        # `prova` dice solo che non blocca ancora (ADR-0119)
        if conto:
            x["conto"] = conto
            if not fa(sistema, conto):
                x["prova"] = conto
        fuori.append(x)

    pf = _int(sb.pf)
    m = re.fullmatch(r"\s*(\d+)d(\d+)\s*(?:([+-])\s*(\d+))?\s*", sb.pf_dado or "")
    if m and pf is not None and fa(sistema, "pf"):
        n, f = int(m.group(1)), int(m.group(2))
        bonus = int(m.group(4) or 0) * (-1 if m.group(3) == "-" else 1)
        atteso = _arrotonda(regole_pf["media"])(n * (f + 1) / 2) + bonus
        # PNG con livelli di classe: il primo dado al massimo (DMG 3.5, cap. 4;
        # in PF1e i dadi dopo il primo a mezza in su, dati del plugin)
        con_classe = re.search(r"[^\W\d_]+ \d+\b", sb.tipo or "")
        massimo = f + _arrotonda(regole_pf["mezzi_dopo_il_primo"])((n - 1) * (f + 1) / 2) + bonus
        if regole_pf["primo_dado_di_classe"] != "massimo":
            massimo = atteso
        if atteso != pf and not (con_classe and massimo == pf):
            nota = f"media di {sb.pf_dado}"
            if con_classe and massimo != atteso:
                nota += f", oppure {massimo} col primo dado di classe al massimo"
            scarto("pf", pf, atteso, nota)
    ca = _int(sb.ca)
    par = re.search(r"\(([^)]*)\)", (sb.ca_dettaglio or "").replace("−", "-"))
    if ca is not None and par and fa(sistema, "CA") and not re.search(r"forma|con \*", par.group(1)):
        voci = re.findall(r"([+-]\s*\d+)\s+[^\W\d_]", par.group(1))
        if voci:
            atteso = 10 + sum(int(v.replace(" ", "")) for v in voci)
            if atteso != ca:
                scarto("CA", ca, atteso, "10 più le voci di ca-dettaglio")
    difesa = re.search(r"^\*\*Difesa\*\*[^\n]*", prosa, re.M)
    if difesa and fa(sistema, "prosa"):
        d = difesa.group(0)
        mca = re.search(r"\*\*CA (\d+)\*\*", d)
        mpf = re.search(r"\*\*pf (\d+)\*\*", d)
        if mca and ca is not None and int(mca.group(1)) != ca:
            scarto("CA (prosa)", int(mca.group(1)), ca, "la riga Difesa contro il recinto")
        if mpf and pf is not None and int(mpf.group(1)) != pf:
            scarto("pf (prosa)", int(mpf.group(1)), pf, "la riga Difesa contro il recinto")
    car = sb.attributi or ""
    cos, cari, dv = _mod_caratteristica(car, "Cos"), _mod_caratteristica(car, "Car"), _dv(sb)
    talenti = _voce_bold(prosa, "Talenti") or ""
    ereditati = bool(re.search(r"quelli di|come A\.", talenti))
    focus = bool(re.search(r"Capacità Focalizzata \(soffio\)", talenti))
    presenza = None
    if dv is not None and fa(sistema, "CD"):
        for nome, mod, gruppo in (("Soffio(?! aderente)", cos, "soffio"),
                                  ("Schiacciare", cos, "schiacciare"),
                                  ("Presenza (?:Terrificante|Minacciosa)", cari, "presenza")):
            scritto = _cd(_voce_bold(prosa, nome))
            if scritto is None or mod is None:
                continue
            atteso = 10 + dv // 2 + mod
            ammessi = {atteso}
            if gruppo == "soffio":
                if focus:
                    ammessi = {atteso + 2}
                elif ereditati:
                    ammessi = {atteso, atteso + 2}
            if gruppo == "presenza":
                presenza = scritto
            if scritto not in ammessi:
                nota = f"10 + ½ DV ({dv // 2}) + mod {'COS' if mod is cos else 'CAR'} ({mod:+d})"
                if gruppo == "soffio" and focus:
                    nota += " + 2 Capacità Focalizzata"
                scarto(f"CD {gruppo}", scritto, sorted(ammessi)[-1], nota)
    mc = re.search(r"corrompere l'acqua\*?[^.·\n]{0,12}?CD (\d+)", prosa)
    if mc and presenza is not None and int(mc.group(1)) != presenza and controlla(sistema, "corrompere_acqua"):
        scarto("CD corrompere l'acqua", int(mc.group(1)), presenza,
               (regole_conformita(sistema).get("corrompere_acqua", {}).get("fonte")
                or "SRD, drago nero") + ": la CD della presenza terrificante", "corrompere_acqua")
    # «come A.n»: una voce ereditata che porta una CD del blocco di prima
    ereditate = fa(sistema, "ereditate") and controlla(sistema, "corrompere_acqua")
    for voce, rif in re.findall(r"\*\*([^*]+)\*\*\s*come (A\.\d+(?:-bis)?)\b", prosa) if ereditate else ():
        padre = (fratelli or {}).get(rif)
        if not padre or presenza is None:
            continue
        mia = _voce_bold(prosa, re.escape(voce.strip())) or ""
        if re.search(r"corrompere l'acqua\*?[^.·\n]{0,12}?CD \d+", mia):
            continue  # la voce eredita, ma riscrive la CD per conto suo
        sua = _voce_bold(padre["prosa"], re.escape(voce.strip()))
        cd_padre = _cd(sua)
        pres_padre = _cd(_voce_bold(padre["prosa"], "Presenza (?:Terrificante|Minacciosa)"))
        if cd_padre is not None and pres_padre is not None and pres_padre != presenza \
                and "corrompere l'acqua" in (sua or ""):
            scarto(f"CD in «{voce.strip()} come {rif}»", cd_padre, presenza,
                   f"ereditata da {rif}, dove la presenza è CD {pres_padre}: "
                   "corrompere l'acqua segue la presenza", "corrompere_acqua")
    # scurovisione: il tipo la ha nell'SRD, i sensi la scrivono
    sensi = " ".join([sb.sensi or "", _voce_bold(prosa, "Sensi") or ""])
    if re.search(r"come A\.", sensi):
        rif = re.search(r"come (A\.\d+(?:-bis)?)", sensi).group(1)
        if rif in fratelli:
            sensi += " " + (fratelli[rif]["sb"].sensi or "")
        else:
            sensi += " scurovisione"   # la scheda madre sta in un altro file (un booklet la include a pezzi)
    tipo = sb.tipo or ""
    # una forma temporanea («pf: quelli di Hella») tiene i sensi di chi la prende
    forma = _int(sb.pf) is None
    sensi_dati = "sensi" in regole_conformita(sistema)
    if not forma and not sensi_dati and fa(sistema, "scurovisione") and SCUROVISIONE_SRD.search(tipo) \
            and not re.search(r"scurovisione", sensi, re.I):
        scarto("sensi", "senza scurovisione", "scurovisione",
               f"il tipo «{SCUROVISIONE_SRD.search(tipo).group(0)}» la ha nell'SRD")
    if not forma and sensi_dati:
        for x in conti_dei_sensi(b, sensi, sistema):
            scarto(*x)
    if not forma:
        for x in conti_di_classe(b, sistema):
            scarto(*x)
    return fuori


# ---------------------------------------------------------------------------
# Le regole di classe e di tipo PF1e (ADR-0119), 2026-11-09
# ---------------------------------------------------------------------------
#: Il cancello dei moduli saltava lotta (BMC/DMC), scurovisione e corrompere
#: l'acqua perché la regola PF1e non era nei dati del plugin; e sulle schede
#: recintate non contava BAB, TS, contatto e colto alla sprovvista, iniziativa,
#: Schivare, visione crepuscolare, incanalare energia. Le regole vengono dal
#: PRD (conformita_prd.toml, generato) e dalle scelte in conformita.toml:
#:
#: | conto | la regola (PRD PF1e) |
#: |---|---|
#: | BAB | somma, classe per classe, di L × progressione (+ i DV razziali del tipo) |
#: | TS | base di classi e DV razziali + caratteristica + Tempra Possente / Riflessi Fulminei / Volontà di Ferro + mantello della resistenza |
#: | BMC | BAB + For (Des se Minuscola o più piccola, o con Manovre Agili) + taglia |
#: | DMC | 10 + BAB + For + Des + taglia + i bonus di deviazione, schivare, sacro… della CA |
#: | contatto_sprovvista | CA − armatura − scudo − naturale; CA − Des − schivare |
#: | iniziativa_recinto | mod Des, +4 con Iniziativa Migliorata |
#: | schivare | il talento Schivare è +1 di schivare nella CA |
#: | scurovisione, visione_crepuscolare | dal tipo, dal sottotipo o dalla razza del Bestiario |
#: | incanalare | (L+1)/2 d6, CD 10 + ½ L + Car, 3 + Car al giorno |
TS_NOMI = (("temp", r"Tem(?:pra)?\.?"), ("rifl", r"Rif(?:lessi)?\.?"), ("vol", r"Vol(?:ontà)?\.?"))
TS_FORMULA = {"buono": lambda L: 2 + L // 2, "scarso": lambda L: L // 3,
              "buono_prestigio": lambda L: (L + 1) // 2, "scarso_prestigio": lambda L: (L + 1) // 3}


def _numero_bold(prosa: str, etichette: str) -> "int | None":
    """Il numero dopo `**BAB**`, `BMC`, `CMD`… nella prosa (bold o no)."""
    m = re.search(r"(?<![\w])(?:" + etichette + r")\b\**\s*([+\-−]?\d+)", prosa)
    return int(m.group(1).replace("−", "-")) if m else None


def _talenti_scritti(prosa: str) -> "list[str] | None":
    """I talenti della riga **Talenti**, uno per voce (None se la riga non c'è)."""
    m = re.search(r"\*\*Talenti\*\*(.*?)(?=\*\*|\n|$)", prosa)
    if not m:
        return None
    testo = re.sub(r"\*\([^)]*\)\*|\([^)]*\)", "", m.group(1))
    return [v.strip(" *·,.") for v in re.split(r"[·,]", testo) if v.strip(" *·,.")]


def _cerca_nel_tipo(testo: str, alias: dict) -> "list[tuple[str, str]]":
    """[(chiave italiana, valore)] degli alias che compaiono nel testo, i più lunghi prima, senza sovrapposizioni."""
    fuori, preso = [], [False] * len(testo)
    for k in sorted(alias, key=len, reverse=True):
        for m in re.finditer(r"(?<![\w])" + re.escape(k) + r"(?![\w])", testo, re.I):
            if not any(preso[m.start():m.end()]):
                fuori.append((k, alias[k], m.start(), m.end()))
                for i in range(m.start(), m.end()):
                    preso[i] = True
    return [(k, v) for k, v, *_ in sorted(fuori, key=lambda x: x[2])]


def _livelli_di_classe(testo: str, regole: dict) -> "list[tuple[str, int]]":
    """[(classe PRD, livello)] da «Umano ladro 4», «Umana esperta 6», «Skum guerriero 8»."""
    alias = dict(regole.get("alias_classi", {}))
    for k, v in list(alias.items()):  # il femminile: esperta, chierica, guerriera
        if k.endswith("o"):
            alias.setdefault(k[:-1] + "a", v)
    fuori, preso = [], [False] * len(testo)
    for k in sorted(alias, key=len, reverse=True):
        for m in re.finditer(r"(?<![\w])" + re.escape(k) + r"\s+(\d+)\b", testo, re.I):
            if not any(preso[m.start():m.end()]):
                fuori.append((m.start(), alias[k], int(m.group(1))))
                for i in range(m.start(), m.end()):
                    preso[i] = True
    return [(c, n) for _, c, n in sorted(fuori)]


def _tipo_e_razza(sb, regole: dict):
    """(tipo PRD, sottotipi PRD, razza italiana del Bestiario) dalla riga `tipo`."""
    tipo_txt = (sb.tipo or "").split("·")[0]
    tipi = _cerca_nel_tipo(tipo_txt, regole.get("alias_tipo", {}))
    razze_core = _cerca_nel_tipo(tipo_txt, regole.get("alias_razze", {}))
    bestiario = _cerca_nel_tipo(" ".join([tipo_txt, sb.nome or ""]), regole.get("sensi", {}).get("razze", {}))
    tipo = tipi[0][1] if tipi else ("humanoid" if razze_core or bestiario else None)
    return tipo, [v for _, v in razze_core], (bestiario[0][0] if bestiario else None)


def _taglia(sb, regole: dict, sistema: str) -> "tuple[str, dict] | None":
    taglie = S.dati(sistema, "creature.costruzione").get("taglie", {})
    for _, t in _cerca_nel_tipo((sb.tipo or "").split("·")[0], regole.get("alias_taglie", {})):
        return t, taglie.get(t, {})
    m = re.search(r"([+-]\d+)\s*taglia", (sb.ca_dettaglio or "").replace("−", "-"))
    if m:
        for t, v in taglie.items():
            if v.get("ca_attacco") == int(m.group(1)):
                return t, v
    return "medium", taglie.get("medium", {})


def _voci_ca(sb) -> "list[tuple[int, str]]":
    """Le voci (valore, nome) della parentesi di `ca-dettaglio`, prima del «;»."""
    testo = (sb.ca_dettaglio or "").split(";")[0].replace("−", "-")
    par = re.search(r"\(([^)]*)\)", testo)
    if not par:
        return [(int(v.replace(" ", "")), n.strip().lower()) for v, n in
                re.findall(r"([+-]\s*\d+)\s+([^\W\d_][^,;+()-]*)", testo)]
    return [(int(v.replace(" ", "")), n.strip().lower()) for v, n in
            re.findall(r"([+-]\s*\d+)\s+([^\W\d_][^,;+]*)", par.group(1))]


def _classe_della_voce(nome: str, regole_ca: dict) -> "str | None":
    if re.match(r"des\b", nome):
        return "des"
    if "taglia" in nome:
        return "taglia"
    for chiave in ("schivare", "deviazione", "naturale", "scudo", "armatura"):
        if any(re.search(r"\b" + re.escape(p), nome) for p in regole_ca.get(chiave, ())):
            return chiave
    return nome.split()[0] if nome else None


def conti_dei_sensi(b: dict, sensi: str, sistema: str) -> "list[tuple]":
    """Scurovisione e visione crepuscolare dal tipo, dai sottotipi e dalla razza (PRD)."""
    regole = regole_conformita(sistema)
    dati = regole.get("sensi", {})
    tipo, sottotipi, razza = _tipo_e_razza(b["sb"], regole)
    voci = []
    if razza:
        voci.append((f"la razza «{razza}» ({dati['razze'][razza].get('fonte', 'Bestiario')})", dati["razze"][razza]))
    for st in sottotipi:
        if st in dati.get("sottotipi", {}):
            voci.append((f"il sottotipo «{st}» (Bestiary, sezione {dati['sottotipi'][st]['sezione']})",
                         dati["sottotipi"][st]))
    if tipo in dati.get("tipi", {}):
        voci.append((f"il tipo «{tipo}» (Bestiary, sezione {dati['tipi'][tipo]['sezione']})", dati["tipi"][tipo]))
    fuori = []
    dv = max(((v.get("scurovisione", 0), perche) for perche, v in voci), default=(0, ""))
    if dv[0] and controlla(sistema, "scurovisione"):
        m = re.search(r"scurovisione\s+(\d+)\s*m", sensi, re.I)
        if not re.search(r"scurovisione", sensi, re.I):
            fuori.append(("sensi", "senza scurovisione", f"scurovisione {dv[0]} m",
                          f"{dv[1]} la dà nel PRD", "scurovisione"))
        elif m and int(m.group(1)) < dv[0]:
            fuori.append(("sensi", f"scurovisione {m.group(1)} m", f"scurovisione {dv[0]} m",
                          f"{dv[1]} la dà nel PRD", "scurovisione"))
    ll = next((perche for perche, v in voci if v.get("crepuscolare")), None)
    if ll and controlla(sistema, "visione_crepuscolare") and not re.search(r"crepuscolare", sensi, re.I):
        fuori.append(("sensi", "senza visione crepuscolare", "visione crepuscolare",
                      f"{ll} la dà nel PRD", "visione_crepuscolare"))
    return fuori


def conti_di_classe(b: dict, sistema: str) -> "list[tuple]":
    """BAB, TS, BMC, DMC, contatto e sprovvista, iniziativa, Schivare, incanalare (ADR-0119)."""
    regole = regole_conformita(sistema)
    if "classi" not in regole:
        return []
    sb, prosa, fuori = b["sb"], b["prosa"], []
    car = sb.attributi or ""
    m_ = {k: _mod_caratteristica(car, k) for k in ("For", "Des", "Cos", "Int", "Sag", "Car")}
    talenti_ = _talenti_scritti(prosa)
    tal = set(talenti_ or ())
    tipo, _, _ = _tipo_e_razza(sb, regole)
    tipi = S.dati(sistema, "creature.costruzione").get("tipi", {})
    # Le classi stanno nella riga `tipo`; solo se lì non ce n'è si guarda il nome.
    # Mai tutti e due: «mago 5» scritto in entrambi contava dieci livelli, i DV
    # razziali uscivano negativi e BAB e TS non partivano.
    classi = (_livelli_di_classe((sb.tipo or "").split("·")[0], regole)
              or _livelli_di_classe(sb.nome or "", regole))
    dv = sum(int(n) for n, _ in DADI.findall(sb.pf_dado or ""))
    razziali = dv - sum(n for _, n in classi) if dv else None
    if razziali is None and classi and _tipo_e_razza(sb, regole)[1]:
        razziali = 0  # le razze del Core non hanno DV razziali (Core, «Races»)
    noto = bool(classi) or (razziali and tipo in tipi)
    # BAB e TS: le classi del PRD più i DV razziali del tipo
    bab_atteso = ts_base = None
    if noto and razziali is not None and razziali >= 0 and (razziali == 0 or tipo in tipi):
        bab_atteso = sum(math.floor(regole["classi"][c]["bab"] * n) for c, n in classi)
        base = {"temp": 0, "rifl": 0, "vol": 0}
        for c, n in classi:
            for chiave, prog in zip(("temp", "rifl", "vol"), regole["classi"][c]["ts"]):
                base[chiave] += TS_FORMULA[prog](n)
        scelte = [()]
        if razziali:
            t = tipi[tipo]
            bab_atteso += math.floor(t["bab"] * razziali)
            for chiave in ("temp", "rifl", "vol"):
                base[chiave] += TS_FORMULA["buono" if chiave in t["ts_buoni"] else "scarso"](razziali)
            if t.get("ts_a_scelta"):
                import itertools
                scelte = list(itertools.combinations(("temp", "rifl", "vol"), t["ts_a_scelta"]))
        ts_base = [{k: v + ((TS_FORMULA["buono"](razziali) - TS_FORMULA["scarso"](razziali))
                            if k in sc else 0) for k, v in base.items()} for sc in scelte]
    bab_scritto = _numero_bold(prosa, r"BAB|Attacco Base")
    if bab_atteso is not None and bab_scritto is not None and bab_scritto != bab_atteso \
            and controlla(sistema, "BAB"):
        desc = " + ".join([f"{c} {n}" for c, n in classi] + ([f"{razziali} DV {tipo}"] if razziali else []))
        fuori.append(("BAB", bab_scritto, bab_atteso, f"PRD, tabelle delle classi e dei tipi: {desc}", "BAB"))
    bab = bab_scritto if bab_scritto is not None else bab_atteso
    # TS
    ts_scritti = {k: _int(re.search(rx + r"\s*([+\-−]\d+)", sb.ts or "").group(1).replace("−", "-"))
                  for k, rx in TS_NOMI if re.search(rx + r"\s*([+\-−]\d+)", sb.ts or "")}
    if ts_base and len(ts_scritti) == 3 and None not in (m_["Des"], m_["Sag"]) \
            and controlla(sistema, "TS"):
        r_ts = regole.get("ts", {})
        car_ts = {"temp": m_["Car"] if tipo == "undead" else (m_["Cos"] or 0),
                  "rifl": m_["Des"], "vol": m_["Sag"]}
        extra = {k: 2 * any(n in tal and v == k for n, v in r_ts.get("talenti", {}).items())
                 for k in car_ts}
        res = re.search(re.escape(r_ts.get("resistenza", "mantello della resistenza")) + r"\s*\+(\d+)",
                        prosa, re.I)
        res = int(res.group(1)) if res else 0
        attesi = [{k: tb[k] + car_ts[k] + extra[k] + res for k in tb} for tb in ts_base]
        # senza la riga **Talenti** un talento può solo aggiungere: si controlla il minimo
        sotto = talenti_ is None and any(all(ts_scritti[k] >= a[k] for k in a) for a in attesi)
        if ts_scritti not in attesi and not sotto:
            att = attesi[0]
            for k in ("temp", "rifl", "vol"):
                if all((a[k] > ts_scritti[k]) if talenti_ is None else (a[k] != ts_scritti[k]) for a in attesi):
                    nota = (f"base {ts_base[0][k]} + {'Car' if k == 'temp' and tipo == 'undead' else {'temp': 'Cos', 'rifl': 'Des', 'vol': 'Sag'}[k]}"
                            f" {car_ts[k]:+d}" + (f" + talento {extra[k]:+d}" if extra[k] else "")
                            + (f" + resistenza +{res}" if res else ""))
                    fuori.append((f"TS {k}", ts_scritti[k], att[k], nota, "TS"))
    # CA: Schivare, contatto, sprovvista
    ca = _int(sb.ca)
    voci = _voci_ca(sb)
    regole_ca = regole.get("ca", {})
    per_classe: "dict[str, int]" = {}
    for v, n in voci:
        k = _classe_della_voce(n, regole_ca)
        per_classe[k] = per_classe.get(k, 0) + v
    if ca is not None and talenti_ is not None and regole_ca.get("talento_schivare") in tal \
            and "schivare" not in per_classe and controlla(sistema, "schivare"):
        fuori.append(("CA", ca, ca + 1, "talento Schivare: +1 di schivare alla CA, che ca-dettaglio non scrive",
                      "schivare"))
    mc = re.search(r"contatto\s+(\d+)", sb.ca_dettaglio or "")
    ms = re.search(r"sprovvista\s+(\d+)", sb.ca_dettaglio or "")
    if ca is not None and voci and controlla(sistema, "contatto_sprovvista"):
        if mc:
            atteso = ca - sum(per_classe.get(k, 0) for k in ("armatura", "scudo", "naturale"))
            if int(mc.group(1)) != atteso:
                fuori.append(("CA contatto", int(mc.group(1)), atteso, "CA − armatura − scudo − naturale",
                              "contatto_sprovvista"))
        if ms:
            atteso = ca - max(per_classe.get("des", 0), 0) - per_classe.get("schivare", 0)
            if int(ms.group(1)) != atteso:
                fuori.append(("CA colto alla sprovvista", int(ms.group(1)), atteso, "CA − Des − schivare",
                              "contatto_sprovvista"))
    # BMC e DMC
    nome_taglia, taglia = _taglia(sb, regole, sistema)
    r_bmc = regole.get("bmc", {})
    it_taglie = {v: k for k, v in regole.get("alias_taglie", {}).items()}
    piccola = it_taglie.get(nome_taglia, nome_taglia) in r_bmc.get("piu_piccole_con_des", ())
    if bab is not None and m_["For"] is not None and m_["Des"] is not None and "bmc_dmc" in taglia:
        agile = piccola or bool(tal & set(r_bmc.get("des_al_posto_della_for", ())))
        bmc_atteso = bab + (m_["Des"] if agile else m_["For"]) + taglia["bmc_dmc"]
        bmc = _numero_bold(prosa, r"BMC|CMB")
        if bmc is not None and bmc != bmc_atteso and controlla(sistema, "BMC"):
            fuori.append(("BMC", bmc, bmc_atteso,
                          f"BAB {bab:+d} + {'Des' if agile else 'For'} + taglia {nome_taglia} {taglia['bmc_dmc']:+d}",
                          "BMC"))
        dmc = _numero_bold(prosa, r"DMC|CMD")
        extra_ca = sum(v for k, v in per_classe.items() if k in r_bmc.get("bonus_ca_in_dmc", ()))
        dmc_atteso = 10 + bab + m_["For"] + m_["Des"] + taglia["bmc_dmc"] + extra_ca
        if dmc is not None and dmc != dmc_atteso and controlla(sistema, "DMC"):
            fuori.append(("DMC", dmc, dmc_atteso,
                          f"10 + BAB {bab:+d} + For {m_['For']:+d} + Des {m_['Des']:+d} + taglia "
                          f"{taglia['bmc_dmc']:+d}" + (f" + deviazione/schivare/… {extra_ca:+d}" if extra_ca else ""),
                          "DMC"))
    # iniziativa nel recinto
    ini = _int(sb.iniziativa)
    if ini is not None and m_["Des"] is not None and controlla(sistema, "iniziativa_recinto"):
        atteso = m_["Des"] + (4 if "Iniziativa Migliorata" in tal else 0)
        if (ini != atteso) if talenti_ is not None else (ini < atteso):
            fuori.append(("iniziativa", ini, atteso, "mod Des, +4 con Iniziativa Migliorata", "iniziativa_recinto"))
    # pf: il bonus di pf-dado e le schede con dadi di più tipi
    m_pf = re.fullmatch(r"\s*((?:\d+d\d+\s*\+\s*)*\d+d\d+)\s*(?:([+-])\s*(\d+))?\s*", sb.pf_dado or "")
    if m_pf and dv:
        bonus = int(m_pf.group(3) or 0) * (-1 if m_pf.group(2) == "-" else 1)
        r_pf = regole.get("pf_bonus", {})
        car_pf = m_["Car"] if tipo == "undead" else m_["Cos"]
        if car_pf is not None and tipo != "construct" and talenti_ is not None and controlla(sistema, "pf_bonus"):
            robustezza = max(r_pf.get("robustezza_minimo", 3), dv) if r_pf.get("talento_robustezza") in tal else 0
            minimo = dv * car_pf + robustezza
            # classe preferita: +1 pf per livello, a scelta (Core, «Favored Class»)
            massimo = minimo + sum(n for _, n in classi)
            if not minimo <= bonus <= massimo:
                nota = f"DV {dv} × {'Car' if tipo == 'undead' else 'Cos'} {car_pf:+d}"
                if robustezza:
                    nota += f" + Robustezza {robustezza}"
                if massimo > minimo:
                    nota += f" (+ fino a {massimo - minimo} di classe preferita)"
                fuori.append(("pf-dado bonus", bonus, minimo if bonus < minimo else massimo, nota, "pf_bonus"))
        dadi = DADI.findall(sb.pf_dado or "")
        pf = _int(sb.pf)
        if len(dadi) > 1 and pf is not None and controlla(sistema, "pf_misti"):
            regole_pf = regole["punti_ferita"]
            media = _arrotonda(regole_pf["media"])(sum(int(n) * (int(f) + 1) / 2 for n, f in dadi))
            ammessi = {media + bonus}
            if classi and not razziali:  # il primo dado è di classe: al massimo
                n0, f0 = int(dadi[0][0]), int(dadi[0][1])
                resto = (n0 - 1) * (f0 + 1) / 2 + sum(int(n) * (int(f) + 1) / 2 for n, f in dadi[1:])
                ammessi.add(f0 + _arrotonda(regole_pf["mezzi_dopo_il_primo"])(resto) + bonus)
            if pf not in ammessi:
                fuori.append(("pf", pf, min(ammessi), f"media di {sb.pf_dado}", "pf_misti"))
    # CD degli incantesimi: «(LI 13°, CD 16 + livello)» = 10 + mod della caratteristica della classe
    r_inc = regole.get("incantesimi", {}).get("caratteristica", {})
    mli = re.search(r"\(LI\s+(\d+)°?,\s*CD\s+(\d+)\s*\+\s*livello\)", prosa)
    incantatori = [(c, n) for c, n in classi if c in r_inc]
    if mli and incantatori and controlla(sistema, "cd_incantesimi"):
        c, n = max(incantatori, key=lambda x: x[1])
        mod_c = m_.get(r_inc[c])
        if mod_c is not None and int(mli.group(2)) != 10 + mod_c:
            fuori.append(("CD incantesimi", int(mli.group(2)), 10 + mod_c,
                          f"10 + {r_inc[c]} {mod_c:+d} + livello dell'incantesimo ({c})", "cd_incantesimi"))
        if int(mli.group(1)) != n:
            fuori.append(("LI", int(mli.group(1)), n, f"livello dell'incantatore = livello di {c}",
                          "cd_incantesimi"))
    # incanalare energia
    livello = sum(n for c, n in classi if c in regole.get("incanalare", {}).get("classi", ()))
    mi = re.search(r"incanalare energia[^(\n]*?(\d+)/giorno\*?\s*\((\d+)d6,\s*CD\s+(\d+)\)", prosa, re.I)
    if livello and mi and m_["Car"] is not None and controlla(sistema, "incanalare"):
        usi, dadi, cd = (int(x) for x in mi.groups())
        for campo, scritto, atteso, nota in (
                ("incanalare usi", usi, 3 + m_["Car"], "3 + Car"),
                ("incanalare dadi", dadi, (livello + 1) // 2, "(livello + 1) / 2 d6"),
                ("incanalare CD", cd, 10 + livello // 2 + m_["Car"], f"10 + ½ livello ({livello // 2}) + Car")):
            if scritto != atteso:
                fuori.append((campo, scritto, atteso, nota, "incanalare"))
    return fuori


def _sigla(titolo: str) -> "str | None":
    m = re.match(r"(A\.\d+(?:-bis)?)\b", titolo)
    return m.group(1) if m else None


def conti_dei_recinti(testo: str, sistema: str = "dnd35") -> "list[dict]":
    blocchi = list(_recinti_del_master(testo))
    fratelli = {_sigla(b["titolo"]): b for b in blocchi if _sigla(b["titolo"])}
    fuori = []
    for b in blocchi:
        for x in conti_del_recinto(b, fratelli, sistema):
            fuori.append({"titolo": b["titolo"], **x})
    return fuori


def rapporto_master(files: "list[Path]") -> "list[dict]":
    esito = []
    for p in files:
        testo = p.read_text(encoding="utf-8", errors="replace")
        sistema = S.sistema_di(p)
        for b in _blocchi_del_master(testo):
            for x in conti_del_master(b, sistema):
                percorso = p.relative_to(ROOT) if p.is_relative_to(ROOT) else p
                esito.append({"file": str(percorso), "titolo": b["titolo"], **x})
        for x in conti_dei_recinti(testo, sistema):
            percorso = p.relative_to(ROOT) if p.is_relative_to(ROOT) else p
            esito.append({"file": str(percorso), **x})
    return esito


def saltati_master(files: "list[Path]") -> "list[dict]":
    """I conti che non si fanno sui file di un sistema che non ha ancora la regola."""
    fuori = []
    for p in files:
        sistema = S.sistema_di(p)
        percorso = p.relative_to(ROOT) if p.is_relative_to(ROOT) else p
        for conto, motivo in sorted(conti_saltati(sistema).items()):
            fuori.append({"file": str(percorso), "sistema": sistema, "conto": conto, "motivo": motivo})
    return fuori


def master_di_default() -> "list[Path]":
    """I DEF e ARC-08, più le schede ```statblocco``` dei moduli di un altro sistema.

    F4 di ADR-0112: i moduli che `sistemi.toml` [moduli] dà a un sistema
    diverso dal predefinito (oggi il Drappo e il Giardino PF1e) entrano nel
    rapporto con le regole del loro sistema.
    """
    fuori = []
    for p in sorted(ROOT.glob("0[0-9]_*/*.md")):
        if "_ARCHIVIO" in p.parts:
            continue
        if "DEF-" in p.name or p.parent.name.startswith("08_"):
            fuori.append(p)
    predefinito = S.predefinito()
    for cartella, sistema in sorted(S.carica()[0].get("moduli", {}).items()):
        if sistema == predefinito:
            continue
        for p in sorted((ROOT / cartella).rglob("*.md")):
            if "_ARCHIVIO" in p.parts or "homebrew" in p.parts:
                continue
            if re.search(r"^```statblocco\s*$", p.read_text(encoding="utf-8", errors="replace"), re.M):
                fuori.append(p)
    return fuori


# ---------------------------------------------------------------------------
# Il cancello dei numeri (ADR-0118, scelta del DM del 2026-11-09)
# ---------------------------------------------------------------------------
#: «Valori sempre i più forti, ma calcolati e non inventati; se la versione
#: PF1e è più forte usa PF1e, ma deve essere compliant con le regole» (DM).
#: Un numero di una scheda entra solo se la regola del suo sistema lo
#: ricostruisce. Il cancello mette insieme tutti i conti che questo script sa
#: fare, **esatti** (senza la fascia di tolleranza del rapporto), su:
#:
#: * le schede del Bestiario (ogni scarto di `giudica`, più l'attacco esatto);
#: * gli statblocchi dei master nella forma `**Campo:**`, attacco compreso;
#: * i recinti ```statblocco``` dei master e dei moduli, attacco compreso;
#: * le unità di massa: AU = attacco della creatura singola (`ARC08-02` §4:
#:   «AU e DU sono i valori medi di attacco e CA dell'unità»). Il «+2 effetto
#:   massa» di `mass_combat_guide_Dm.md` è della variante 2d6, non del d20;
#: * i blocchi «STATISTICHE CREATURA SINGOLA» delle guide: l'attacco, da
#:   «Attacco Base» e dalle caratteristiche che il blocco scrive.
#:
#: E conta i file con numeri di combattimento che nessun conto legge ancora
#: (`non_coperti`). E' un **cricchetto**: gli scarti e i file scoperti di oggi
#: stanno in `docs/audit/numeri-baseline.json`; uno nuovo fa fallire, uno
#: risolto va tolto con `--aggiorna-numeri`, che non aggiunge mai niente.
BASELINE_NUMERI = ROOT / "docs" / "audit" / "numeri-baseline.json"
#: Le righe che dicono «qui ci sono numeri di combattimento».
NUMERI_DI_COMBATTIMENTO = re.compile(
    r"\bAttacco Base\b|\bBAB\b|\bBase Attack\b|\bAttacco Completo\b|\bFull Attack\b"
    r"|\*\*AU\b|\bAttacco Unità\b|^```statblocco", re.I | re.M)
#: Dove non si cercano: archivi, piani, documenti, skill, prove, codice.
#: `MEMORIA.md` è generato dalle ultime righe di `plans/CHANGELOG.md` (già fuori): una
#: riga di changelog che nomina il BAB non è una scheda.
#: I testi d'altri (`_testi-altrui/`, P28) non sono nostri, e un booklet `.hb.md` si
#: genera dai master: lo copre il conto sul master.
FUORI_DAI_NUMERI = ("_ARCHIVIO", "plans/", "docs/", ".github/", "skills/", "evals/",
                    "scripts/", "node_modules/", "sistemi/", "_testi-altrui/", ".hb.md",
                    "CHANGELOG.md", "MEMORIA.md")
#: L'AU di un'unità e il rimando alla sua scheda uno contro uno.
AU_UNITA = re.compile(r"^\*\*AU(?:\s*\(([^)]*)\))?:\*\*\s*\+?(-?\d+)", re.M)
UNO_CONTRO_UNO = re.compile(r"[Uu]no contro uno:?\**\s*`([^`]+\.md)`(?:\s*§\s*«([^»]+)»)?")
TITOLO_UNITA = re.compile(r"^#{2,4}\s+\**(.+?)\**\s*$", re.M)


#: Le voci del blocco che elencano oggetti, talenti o abilità: un «+1» lì è un potenziamento, non un attacco
_VOCE_NON_ATTACCO = re.compile(r"(?:altro\s+|other\s+)?(?:equipaggiamento|equipment|possessions|gear|tesoro|treasure|"
                               r"talenti|feats|abilit[àa]|skills)\b", re.I)


def _attacco_di_scheda(s: Scheda) -> str:
    """La riga del primo attacco in mischia, o del primo attacco qualunque. Le voci
    dell'equipaggiamento non contano: «doppia ascia orchesca +1 (…)» è un oggetto."""
    if s.mischia:
        return s.mischia
    blocco = L.BLOCCO.search(s.testo)
    voci = re.findall(r"^\s*-\s*(.+)$", blocco.group(1), re.M) if blocco else []
    for v in voci:
        if not re.match(r"(?:Distanza|Ranged)\b", v, re.I) and not _VOCE_NON_ATTACCO.match(v) and PRIMO_ATTACCO.search(v):
            return v
    return ""


def attacco_esatto(s: Scheda) -> "tuple[int, int, str] | None":
    """(scritto, atteso, come) dell'attacco di una scheda, senza tolleranza."""
    riga = _attacco_di_scheda(s)
    babs = set()
    if s.composizione_nota and s.gruppi:
        babs.add(bab_atteso(s))
    if s.bab is not None:
        babs.add(s.bab)
    if not riga or not babs:
        return None
    car = " ".join(f"{k} {v}" for k, v in s.attributi.items() if isinstance(v, int))
    taglia = L.taglia_di(s.testo) or L.taglia_di(f"tipo: {s.tipo}") or 0
    incorporeo = re.search(r"\bincorpore", s.tipo or "", re.I)
    conti = []
    for b in sorted(babs):
        c = attacco_atteso(riga, b, car, s.testo if not incorporeo else "Arma Accurata " + s.testo, taglia)
        if c:
            conti.append(c)
    if not conti:
        return None
    return min(conti, key=lambda c: abs(c[0] - c[1]))


def _scarto(file, titolo, campo, scritto, atteso, come) -> dict:
    return {"file": file, "titolo": titolo, "campo": campo,
            "scritto": scritto, "atteso": atteso, "come": come}


def _rel(p: Path) -> str:
    return str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)


def numeri_del_bestiario() -> "list[dict]":
    fuori = []
    for p in sorted(ROOT.glob("Bestiario/**/*-cr*.md")):
        s = leggi(p)
        if not s:
            continue
        sistema = S.sistema_di(p)
        titolo = p.stem
        if sistema == S.predefinito():
            g = giudica(s)
            spiegato = g["template"] or g["decisione"] or (
                g["come_la_fonte"] and set(g["come_la_fonte"]) == set(g["scarti"]))
            if not spiegato and g["provenienza"] != "generate":
                for k, v in g["scarti"].items():
                    if k != "attacco":
                        fuori.append(_scarto(_rel(p), titolo, k, v[0], v[1], "conto di giudica"))
        if not fa(sistema, "attacco"):
            continue
        a = attacco_esatto(s)
        if a and a[0] != a[1]:
            fuori.append(_scarto(_rel(p), titolo, "attacco", a[0], a[1], a[2]))
    return fuori


def numeri_dei_recinti(p: Path, testo: str, sistema: str) -> "list[dict]":
    fuori = [_scarto(_rel(p), x["titolo"], x["campo"], x["scritto"], x["atteso"], x.get("nota", ""))
             for x in conti_dei_recinti(testo, sistema)]
    if not fa(sistema, "attacco"):
        return fuori
    righe = testo.split("\n")
    for b in _recinti_del_master(testo):
        i = b["riga"] - 1
        fine = next(j for j in range(i + 1, len(righe)) if righe[j].strip() == "```")
        s = L.leggi_testo("\n".join(righe[i:fine + 1]) + "\n" + b["prosa"], p)
        a = attacco_esatto(s) if s else None
        if a and a[0] != a[1]:
            fuori.append(_scarto(_rel(p), b["titolo"], "attacco", a[0], a[1], a[2]))
    return fuori


def _unita(testo: str):
    """(titolo, riga, arma, AU, rimando o None) per ogni unità con una riga **AU**."""
    titoli = [(m.start(), m.group(1).strip()) for m in TITOLO_UNITA.finditer(testo)]
    for m in AU_UNITA.finditer(testo):
        inizio = max((s for s, _ in titoli if s < m.start()), default=0)
        fine = min((s for s, _ in titoli if s > m.start()), default=len(testo))
        titolo = next((t for s, t in titoli if s == inizio), "")
        rim = UNO_CONTRO_UNO.search(testo[inizio:fine])
        yield (re.sub(r"[*#]", "", titolo).strip(), testo.count("\n", 0, m.start()) + 1,
               m.group(1) or "", int(m.group(2)),
               (rim.group(1) + ("§" + rim.group(2) if rim.group(2) else "")) if rim else None)


#: Il blocco «STATISTICHE CREATURA SINGOLA» di una guida: la scheda uno contro
#: uno in forma compatta, dentro lo stesso recinto dell'unità.
SINGOLA = re.compile(r"^```\n((?:(?!^```).*\n)*?)STATISTICHE CREATURA SINGOLA[^\n]*\n((?:(?!^```).*\n)*?)^```", re.M)
AU_DEL_RECINTO = re.compile(r"Attacco Unità:\s*\+?(-?\d+)(?:\s*\(([^)]*)\))?")
ATT_SINGOLA = re.compile(r"^Att(?:acco)? (?!Base|Completo|Unità)(.+)$", re.M)
TAGLIA_SINGOLA = {"minuscol[oaie]": 2, "piccol[oaie]": 1, "grand[ei]": -1, "enorm[ei]": -2, "mastodontic[oaih]+": -4}


def _singole(testo: str):
    """(titolo, riga, AU o None, etichetta, corpo) dei blocchi «creatura singola»."""
    titoli = [(m.start(), m.group(1).strip()) for m in TITOLO_UNITA.finditer(testo)]
    for m in SINGOLA.finditer(testo):
        titolo = max(((s, t_) for s, t_ in titoli if s < m.start()), default=(0, ""))[1]
        au = AU_DEL_RECINTO.search(m.group(1))
        yield (re.sub(r"[*#]", "", titolo).strip(), testo.count("\n", 0, m.start()) + 1,
               int(au.group(1)) if au else None, (au.group(2) or "") if au else "", m.group(2))


def _attacco_della_singola(corpo: str, etichetta: str = "") -> "tuple | None":
    """(scritto, atteso o None, come) dell'attacco di un blocco «creatura singola».

    Con un'etichetta («Lancio Massi») sceglie l'attacco che la nomina; se no il primo.
    """
    voci = [v for r in ATT_SINGOLA.findall(corpo) for v in re.split(r"\s+(?:e|o)\s+(?=[A-Z])|;", r) if v.strip()]
    voci = [v for v in voci if PRIMO_ATTACCO.search(v)]
    if not voci:
        return None
    parole = [w.lower()[:-1] for w in re.findall(r"\w{4,}", etichetta)]
    riga = next((v for v in voci if any(w in v.lower() for w in parole)), voci[0])
    scritto = int(PRIMO_ATTACCO.search(riga).group(1))
    bab = re.search(r"Attacco Base\s*\+?(-?\d+)", corpo)
    car = re.search(r"^For \d+.*$", corpo, re.M)
    if not bab or not car:
        return scritto, None, "il blocco non scrive «Attacco Base» o le caratteristiche"
    basso = corpo.lower()
    # la taglia è quella della riga del tipo («CM Gigante Grande;»), non di un'arma «grande»
    tipo = next((r for r in basso.split("\n") if re.search(r"\b(umanoide|gigante|bestia|drago|non morto)\b", r)), "")
    taglia = next((v for k, v in TAGLIA_SINGOLA.items() if re.search(rf"\b{k}\b", tipo)), 0)
    a = attacco_atteso(riga, int(bab.group(1)), car.group(0), corpo, taglia)
    if a and "gigante" in tipo and re.search(r"\bmass[oi]\b", riga, re.I):
        # SRD 3.5, Giant, Rock Throwing: +1 razziale ai tiri per colpire con i massi
        a = (a[0], a[1] + 1, a[2] + ", +1 razziale ai massi")
    return a if a else (scritto, None, "l'attacco non si legge")


def numeri_delle_singole(p: Path, testo: str) -> "list[dict]":
    fuori = []
    for titolo, _, au, etichetta, corpo in _singole(testo):
        a = _attacco_della_singola(corpo)
        if a is None:
            continue
        if a[1] is None or a[0] != a[1]:
            fuori.append(_scarto(_rel(p), titolo, "attacco", a[0], a[1], a[2]))
        if au is not None:
            b = _attacco_della_singola(corpo, etichetta) or a
            if au != b[0]:
                fuori.append(_scarto(_rel(p), titolo, "AU", au, b[0],
                                     f"attacco {b[0]:+d} della creatura singola" + _come_media()))
    return fuori


def _come_media() -> str:
    return " (ARC08-02 §4: l'AU è l'attacco medio dell'unità)"


def numeri_delle_unita(p: Path, testo: str) -> "list[dict]":
    fuori = []
    for titolo, riga, arma, au, rimando in _unita(testo):
        if not rimando:
            fuori.append(_scarto(_rel(p), titolo, "AU", au, None,
                                 "manca la scheda uno contro uno («Uno contro uno: `…`»)"))
            continue
        file_, _, sezione = rimando.partition("§")
        f = ROOT / file_
        if sezione:
            corpo = next((c for t_, _, _, _, c in _singole(f.read_text(encoding="utf-8")) if t_.startswith(sezione)),
                         None) if f.exists() else None
            a = _attacco_della_singola(corpo, arma) if corpo else None
        else:
            s = leggi(f) if f.exists() else None
            a = attacco_esatto(s) if s else None
        if not a:
            fuori.append(_scarto(_rel(p), titolo, "AU", au, None,
                                 f"la scheda {rimando} non ha un attacco che si legge"))
            continue
        atteso = a[0]
        if au != atteso:
            fuori.append(_scarto(_rel(p), titolo, "AU", au, atteso,
                                 f"attacco {a[0]:+d} di {rimando}" + _come_media()))
    return fuori


def md_del_repo(radice: Path = ROOT) -> "list[Path]":
    """I .md tracciati più i nuovi non ignorati, come `validate_docs.sorgenti`:
    le cartelle di `.gitignore` (build/, gli specchi delle skill) restano fuori.
    Fuori da un clone git, tutti i .md."""
    import subprocess
    try:
        uscite = [subprocess.run(["git", "ls-files", "-z", *extra, "*.md"], cwd=radice,
                                 capture_output=True, text=True, check=True).stdout
                  for extra in ((), ("--others", "--exclude-standard"))]
    except (OSError, subprocess.CalledProcessError):
        return sorted(radice.rglob("*.md"))
    nomi = {n for u in uscite for n in u.split("\0") if n}
    return sorted(radice / n for n in nomi if (radice / n).is_file())


def numeri_dei_file() -> "tuple[list[dict], list[str]]":
    """Gli scarti di master, moduli e unità, e i file con numeri che nessuno legge."""
    scarti_, scoperti = [], []
    for p in md_del_repo():
        r = _rel(p)
        if r.startswith(FUORI_DAI_NUMERI) or any(x in r for x in FUORI_DAI_NUMERI) \
                or r.startswith("Bestiario/"):
            continue
        testo = p.read_text(encoding="utf-8", errors="replace")
        if not NUMERI_DI_COMBATTIMENTO.search(testo):
            continue
        sistema = S.sistema_di(p)
        letti = 0
        for b in _blocchi_del_master(testo):
            letti += 1
            for x in conti_del_master(b, sistema):
                scarti_.append(_scarto(r, b["titolo"], x["campo"], x["scritto"], x["atteso"], x["nota"]))
        recinti = list(_recinti_del_master(testo))
        letti += len(recinti)
        if recinti:
            scarti_.extend(numeri_dei_recinti(p, testo, sistema))
        unita = list(_unita(testo))
        singole = list(_singole(testo))
        letti += len(unita) + len(singole)
        scarti_.extend(numeri_delle_unita(p, testo))
        scarti_.extend(numeri_delle_singole(p, testo))
        if not letti:
            scoperti.append(r)
    return scarti_, scoperti


def _chiave(x: dict) -> str:
    return f"{x['file']} | {x['titolo']} | {x['campo']} | {x['scritto']}"


def stato_dei_numeri() -> dict:
    scarti_, scoperti = numeri_dei_file()
    scarti_ = numeri_del_bestiario() + scarti_
    return {"scarti": scarti_, "non_coperti": scoperti}


def cancello_numeri(aggiorna: bool = False) -> int:
    stato = stato_dei_numeri()
    chiavi = sorted({_chiave(x) for x in stato["scarti"]})
    scoperti = sorted(set(stato["non_coperti"]))
    base = json.loads(BASELINE_NUMERI.read_text(encoding="utf-8")) if BASELINE_NUMERI.exists() else None
    if base is None and aggiorna != "inizio":
        print(f"✗ manca {BASELINE_NUMERI.relative_to(ROOT)}")
        return 1
    if aggiorna == "inizio":
        base = {"scarti": chiavi, "non_coperti": scoperti}
        _scrivi_baseline(base)
        print(f"✓ baseline dei numeri scritta: {len(chiavi)} scarti, {len(scoperti)} file non coperti")
        return 0
    nuovi = [x for x in stato["scarti"] if _chiave(x) not in set(base["scarti"])]
    nuovi_scoperti = [f for f in scoperti if f not in set(base["non_coperti"])]
    risolti = [k for k in base["scarti"] if k not in set(chiavi)]
    coperti = [f for f in base["non_coperti"] if f not in set(scoperti)]
    for x in nuovi:
        atteso = "senza conto" if x["atteso"] is None else f"atteso {x['atteso']:+d}"
        print(f"✗ {x['file']} [{x['titolo'][:50]}] {x['campo']} {x['scritto']:+d}, {atteso} ({x['come']})")
    for f in nuovi_scoperti:
        print(f"✗ {f}: numeri di combattimento che nessun conto legge (forma `**Campo:**`, "
              "recinto ```statblocco``` o riga **AU** con la scheda uno contro uno)")
    if aggiorna:
        if nuovi or nuovi_scoperti:
            print("✗ --aggiorna-numeri toglie solo quello che è risolto: prima correggi i nuovi")
            return 1
        _scrivi_baseline({"scarti": chiavi, "non_coperti": scoperti})
        print(f"✓ baseline aggiornata: {len(risolti)} scarti risolti, {len(coperti)} file coperti")
        return 0
    if risolti or coperti:
        print(f"✗ {len(risolti)} scarti e {len(coperti)} file della baseline sono risolti: "
              "python3 scripts/conformita_statblocchi.py --aggiorna-numeri")
    if nuovi or nuovi_scoperti or risolti or coperti:
        return 1
    print(f"✓ cancello dei numeri: nessuno scarto nuovo ({len(chiavi)} in baseline, "
          f"{len(scoperti)} file non ancora coperti)")
    return 0


def _scrivi_baseline(base: dict) -> None:
    out = {"_cos_e": ("Il cricchetto del cancello dei numeri (ADR-0118): gli scarti di oggi fra un "
                      "numero scritto e la regola che lo calcola, e i file con numeri che nessun conto "
                      "legge. Scende soltanto: --aggiorna-numeri toglie il risolto e non aggiunge. "
                      "Lo legge scripts/conformita_statblocchi.py --cancello-numeri."),
           "scarti": base["scarti"], "non_coperti": base["non_coperti"]}
    BASELINE_NUMERI.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--riepilogo", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--correggi-pf-dado", action="store_true",
                    help="riscrive i `pf-dado` che non registrano i dadi vita (idempotente)")
    ap.add_argument("--proponi-pf-dado", action="store_true",
                    help="come sopra, ma stampa senza scrivere")
    ap.add_argument("--check", action="store_true",
                    help="gate: ogni `pf-dado` registra i dadi vita, e quelli riscritti tornano")
    ap.add_argument("--master", nargs="*", metavar="FILE",
                    help="rapporto sugli statblocchi scritti nei master (default: i DEF e ARC-08, "
                         "più i moduli di un altro sistema); non e' un cancello, esce sempre 0")
    ap.add_argument("--cancello-moduli", action="store_true",
                    help="cancello (in CI): ogni conto delle schede dei moduli di un sistema "
                         "diverso dal predefinito (oggi il Drappo e il Giardino PF1e) torna")
    ap.add_argument("--severo", action="store_true",
                    help="con --cancello-moduli: anche i conti `in_prova` bloccano (ADR-0119, "
                         "la prova della promozione)")
    ap.add_argument("--cancello-numeri", action="store_true",
                    help="cancello (ADR-0118): ogni numero calcolabile di Bestiario, master, moduli e "
                         "unità torna con la regola, salvo gli scarti della baseline")
    ap.add_argument("--aggiorna-numeri", action="store_true",
                    help="toglie dalla baseline dei numeri gli scarti risolti (non ne aggiunge)")
    ap.add_argument("--baseline-numeri-iniziale", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    if args.baseline_numeri_iniziale:
        return cancello_numeri("inizio")
    if args.cancello_numeri or args.aggiorna_numeri:
        return cancello_numeri(aggiorna=args.aggiorna_numeri)
    if args.cancello_moduli:
        files = [p for p in master_di_default() if S.sistema_di(p) != S.predefinito()]
        r = rapporto_master(files)
        bloccano = [x for x in r if args.severo or "prova" not in x]
        for x in r:
            segno = "✗" if x in bloccano else "⚠"
            prova = f" [in prova: {x['prova']}]" if "prova" in x else ""
            print(f"{segno} {x['file']}:{x['riga']} [{x['titolo'][:50]}] {x['campo']} "
                  f"{x['scritto']} ≠ {x['atteso']} ({x['nota']}){prova}")
        saltati = sorted({x["conto"] for x in saltati_master(files)})
        if bloccano:
            return 1
        avvisi = len(r) - len(bloccano)
        print(f"✓ conformita_statblocchi: {len(files)} moduli di un altro sistema, ogni conto torna"
              + (f" (saltati perché manca la regola: {', '.join(saltati)})" if saltati else "")
              + (f"; {avvisi} avvisi dai conti in prova (ADR-0119)" if avvisi else ""))
        return 0
    if args.master is not None:
        files = [Path(f).resolve() for f in args.master] or master_di_default()
        r = rapporto_master(files)
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=1))
            return 0
        for x in r:
            prova = f" [in prova: {x['prova']}]" if "prova" in x else ""
            print(f"  {x['file']}:{x['riga']} [{x['titolo'][:50]}] {x['campo']} "
                  f"{x['scritto']} ≠ {x['atteso']} ({x['nota']}){prova}")
        for x in saltati_master(files):
            print(f"  ⏭ {x['file']} ({x['sistema']}): conto «{x['conto']}» saltato, {x['motivo']}")
        print(f"STATBLOCCHI NEI MASTER — {len(files)} file, {len(r)} conti che non tornano "
              "(rapporto, non cancello: D7 di MASTER-DEF)")
        return 0
    if args.check:
        problemi = controlla_pf_dado()
        for x in problemi:
            print(f"✗ {x}")
        if problemi:
            return 1
        print("✓ conformita_statblocchi: ogni `pf-dado` registra i dadi vita, "
              "e ogni correzione e' riproducibile")
        return 0
    if args.correggi_pf_dado or args.proponi_pf_dado:
        fatte = correggi_pf_dado(scrivi=args.correggi_pf_dado)
        for c in fatte:
            nota = "" if c["legale"] else f"  ⚠ pf {c['pf']} fuori {c['fascia']}"
            print(f"  {c['file'].name:44s} {c['vecchio']:>10s} → {c['nuovo']:<18s} "
                  f"(media {c['media']}, pf {c['pf']}){nota}")
        print(f"{'✓ corretti' if args.correggi_pf_dado else 'PROPOSTA:'} {len(fatte)} `pf-dado`")
        return 0
    g = tutte()
    if args.json:
        print(json.dumps({"riepilogo": riepilogo(g), "schede": g}, ensure_ascii=False, indent=1))
        return 0
    r = riepilogo(g)
    print(f"CONFORMITA' 3.5 — {r['statblocchi']} statblocchi, {r['verificabili']} verificabili")
    print(f"  tornano {r['tornano']} · spiegati da un template PF1e {r['spiegati_da_template']} · "
          f"uguali alla fonte {r['come_la_fonte']} · decisioni aperte al DM {r['decisioni_aperte']} · "
          f"da correggere {r['da_correggere']} · scarti su caratteristiche generate "
          f"{r['del_generatore']}")
    if args.riepilogo:
        return 0
    for x in g:
        if not x["scarti"]:
            continue
        etichetta = (f"template {x['template']}" if x["template"] else
                     "come la fonte" if x["come_la_fonte"] and set(x["come_la_fonte"]) == set(x["scarti"]) else
                     f"decisione {x['decisione']}" if x["decisione"] else
                     "del generatore" if x["provenienza"] == "generate" else "DA CORREGGERE")
        voci = " · ".join(f"{k} {v[0]:+d}≠{v[1]}" if k != "pf" else f"pf {v[0]}≠{v[1]}"
                          for k, v in x["scarti"].items())
        print(f"  [{etichetta}] {x['file']} ({x['provenienza']}): {voci}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
