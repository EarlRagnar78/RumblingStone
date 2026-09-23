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
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import tabelle as T  # noqa: E402
from dmcore import lettura_creatura as L  # noqa: E402

# ---------------------------------------------------------------------------
# Le classi: dado, TS buoni, BAB. Stanno in `dmcore.progressione` (ADR-0066),
# con le due classi di prestigio SRD che compaiono nel Bestiario; i nomi di
# prima restano come alias finche' il lotto E8 non li toglie.
# ---------------------------------------------------------------------------
from dmcore import progressione as P  # noqa: E402
from dmcore.progressione import CLASSE_LIVELLO, Gruppo  # noqa: E402,F401

_PRESTIGIO = P.PRESTIGIO
_classe = P.classe
_NOMI = P.NOMI_DI_CLASSE

#: La scheda come la legge questo verificatore sta in `dmcore.lettura_creatura`
#: (ADR-0066, D1: il verificatore condivide il lettore); i nomi restano
#: importabili da qui fino al lotto E8.
from dmcore.lettura_creatura import (  # noqa: E402,F401
    TS_CAMPO, ATTRIBUTI, MISCHIA, TALENTI, RESISTENZA, talenti, Scheda, provenienza,
    _attributi, DV_PROSA, DV_ACCANTO_AI_PF, LIVELLO_IGNOTO, dv_totali, dadi_di_pf,
    composizione, leggi, NON_MORTO_PF1E, PF1E, non_morto_pf1e,
)


BAB, LOTTA, LOTTA_TAGLIA = L.BAB_SCRITTO, L.LOTTA_SCRITTA, L.LOTTA_TAGLIA
FOCALIZZATA = re.compile(r"\b(?:Weapon Focus|Arma Focalizzata)\b", re.I)
ACCURATA = re.compile(r"\b(?:Weapon Finesse|Arma Accurata)\b", re.I)
LOTTA_MIGLIORATA = L.LOTTA_MIGLIORATA
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


def verifica(s: Scheda, attr: "dict | None" = None) -> dict:
    """Ogni identita': (dichiarato, atteso, scarto) o None se non verificabile."""
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
        extra = 4 if LOTTA_MIGLIORATA.search(s.testo) else 0     # afferrare migliorato no
        attesi = [b + mod(attr.get("For")) + LOTTA_TAGLIA.get(taglia, 0) + extra for b in babs]
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
                 + (1 if FOCALIZZATA.search(s.testo) else 0))
        att = min((b + fisso for b in babs), key=lambda a: abs(dich - a))
        d = dich - att
        out["attacco"] = (dich, att, 0 if -1 <= d <= 2 else d)
    if not s.composizione_nota:
        return out
    if s.ts:
        lo, hi = ts_attesi(s, attr)
        for nome, dich, a, b in zip(("Temp", "Rifl", "Vol"), s.ts, lo, hi):
            d = 0 if a <= dich <= b + 4 else (dich - a if dich < a else dich - b - 4)
            out[nome] = (dich, a if a == b else f"{a}..{b}", d)
    return out


def scarti(esito: dict) -> dict:
    return {k: v for k, v in esito.items() if isinstance(v, tuple) and v[2] != 0}


def con_template(attr: dict, nome: str) -> dict:
    return {k: (v + TEMPLATE[nome].get(k, 0) if isinstance(v, int) else v)
            for k, v in attr.items()}


numeri_della_fonte = L.numeri_della_fonte


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


def giudica(s: Scheda) -> dict:
    esito = verifica(s)
    esito.update(verifica_variante_advanced(s))
    fuori = scarti(esito)
    spiegazione = None
    # la variante in prosa si confronta con la sua regola, e un'ipotesi di
    # template su caratteristiche **scelte** non spiega niente
    if fuori and s.provenienza != "generate" and not any(k.startswith("variante") for k in fuori):
        for nome in TEMPLATE:
            if not scarti(verifica(s, con_template(s.attributi, nome))):
                spiegazione = nome
                break
    come_la_fonte = []
    if fuori and s.provenienza == "trascritte":
        fonte = numeri_della_fonte(s.testo)
        come_la_fonte = [k for k, v in fuori.items() if fonte.get(k) == v[0]]
    decisione = decisioni_aperte().get(s.file.name) if fuori else None
    percorso = s.file.relative_to(ROOT) if s.file.is_relative_to(ROOT) else s.file
    return {"file": str(percorso), "provenienza": s.provenienza,
            "verificabile": bool(esito), "esito": esito, "scarti": fuori,
            "template": spiegazione, "come_la_fonte": come_la_fonte,
            "decisione": decisione, "template_dichiarati": template_dichiarati(s.testo)}


def tutte() -> "list[dict]":
    fuori = []
    for p in sorted(ROOT.glob("Bestiario/**/*-cr*.md")):
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
MARCA_PF = "> [INFERRED — needs DM confirmation] `pf-dado` "
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
    args = ap.parse_args(argv)
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
