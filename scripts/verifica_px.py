#!/usr/bin/env python3
"""verifica_px.py — il registro dei PX torna con le somme, le soglie e i livelli?

Perché esiste
  `campaign/REGISTRO-PX.md` è la copia in testo del foglio dei PX: righe per
  scontro, una tabella dei totali, il livello dai PX e il livello al tavolo.
  Fino al 2026-11-20 nessuno script sommava le righe: i totali e i livelli li
  controllava solo chi rileggeva (un modello o il DM). È un fatto numerico, e
  un fatto numerico si verifica con un conto (ADR-0148).

Le quattro regole, tutte deterministiche
  R1 somma       per ogni colonna, la somma delle righe è il totale «PX».
  R2 soglia      il «Livello dai PX» è quello della tabella dei PX del 3.5
                 (livello n da n·(n-1)/2 · 1.000 PX). [Private source: PHB 3.5,
                 Table 3–2]: la tabella non è nell'SRD (lo dice anche
                 skills/dnd-35-srd/references/core-mechanics.md).
  R3 un livello  si sale di un livello alla volta e i PX eccedenti si fermano
                 a 1 sotto la soglia del livello dopo [Private source: DMG 3.5,
                 cap. 2, Experience Points]. Quindi
                 soglia(livello al tavolo) ≤ PX < soglia(livello al tavolo + 2).
  R4 tavolo      il «Livello al tavolo» di un PG è il suo livello effettivo in
                 `campaign/state.yaml` (`party[].classe`): l'«ECL N» se scritto,
                 altrimenti la somma dei livelli di classe più l'eventuale
                 «LA +N» (SRD, Monsters as Races: i PX seguono l'ECL). Un PG
                 dei totali con un livello al tavolo e senza riga in state.yaml
                 è una violazione; un PNG si scrive con «—» al tavolo.

Uso
  python3 scripts/verifica_px.py                    # il registro del repo
  python3 scripts/verifica_px.py FILE [--state S]   # un altro registro
  python3 scripts/verifica_px.py --json             # uscita strutturata

Esce 1 se una regola è violata. Ogni violazione porta regola, atteso, ha,
fonte e file:riga, come verifica_scheda (ADR-0124). Solo stdlib più PyYAML.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRO = ROOT / "campaign" / "REGISTRO-PX.md"
STATE = ROOT / "campaign" / "state.yaml"
FONTE_SOGLIE = "[Private source] PHB 3.5, Table 3–2: Experience and Level-Dependent Benefits"
FONTE_UN_LIVELLO = "[Private source] DMG 3.5, cap. 2, Experience Points: un livello alla volta"
FONTE_ECL = "SRD 3.5, Monsters as Races: i PX seguono l'ECL"


@dataclass
class Violazione:
    regola: str
    colonna: str
    atteso: str
    ha: str
    fonte: str
    dove: str


def soglia(livello: int) -> int:
    """PX minimi per il livello, tabella SRD 3.5."""
    return livello * (livello - 1) // 2 * 1000


def livello_da_px(px: int) -> int:
    n = 1
    while soglia(n + 1) <= px:
        n += 1
    return n


def numero(cella: str) -> "int | None":
    """«104.999» → 104999, «-4.968» → -4968, «» → None, «14°» → 14."""
    testo = cella.strip().replace("°", "").replace("−", "-").replace("–", "-")
    if not testo or testo in {"—", "-"}:
        return None
    testo = testo.replace(".", "").replace(" ", "")
    return int(testo) if re.fullmatch(r"-?\d+", testo) else None


def _celle(riga: str) -> "list[str]":
    return [c.strip() for c in riga.strip().strip("|").split("|")]


def leggi(testo: str) -> dict:
    """Le righe di scontro, la tabella dei totali e le colonne, con i numeri di riga."""
    colonne: "list[str]" = []
    righe: "list[tuple[int, list[int | None]]]" = []
    totali: "dict[str, tuple[int, list[str]]]" = {}
    nomi_totali: "list[str]" = []
    intestazioni_diverse: "list[tuple[int, list[str]]]" = []
    sezione = ""
    for n, riga in enumerate(testo.splitlines(), 1):
        if riga.startswith("## "):
            sezione = riga[3:].strip()
            continue
        if not riga.startswith("|") or set(riga) <= set("|-: "):
            continue
        celle = _celle(riga)
        if sezione == "Totali":
            if not celle[0]:
                nomi_totali = celle[1:]
            else:
                totali[celle[0]] = (n, celle[1:])
            continue
        if celle[0] == "Riga":
            if colonne and celle[2:] != colonne:
                # le somme vanno per posizione: un ordine diverso darebbe i PX di uno a un altro
                intestazioni_diverse.append((n, celle[2:]))
            colonne = colonne or celle[2:]
            continue
        if re.fullmatch(r"\d+", celle[0]) and colonne:
            righe.append((n, [numero(c) for c in celle[2:2 + len(colonne)]]))
    return {"colonne": colonne, "righe": righe, "totali": totali,
            "nomi_totali": nomi_totali, "intestazioni_diverse": intestazioni_diverse}


def livelli_al_tavolo(state: Path) -> "dict[str, int]":
    try:
        import yaml
    except ImportError:  # pragma: no cover
        return {}
    dati = yaml.safe_load(state.read_text(encoding="utf-8")) or {}
    esito = {}
    for pg in dati.get("party", []) or []:
        esito[str(pg.get("pg"))] = livello_effettivo(str(pg.get("classe", "")))
    return esito


def livello_effettivo(classe: str) -> int:
    """«Fighter 4 / Monk 9» → 13; «Warlock 13 (ECL 15)» → 15; «Half-Ogre (LA +2) Fighter 1» → 3."""
    ecl = re.search(r"\bECL\s*(\d{1,2})\b", classe)
    if ecl:
        return int(ecl.group(1))
    la = sum(int(x) for x in re.findall(r"\bLA\s*\+\s*(\d)\b", classe))
    senza_la = re.sub(r"\(?\bLA\s*\+\s*\d\)?", "", classe)
    # i numeri che non sono livelli: GS/CR e punteggi di caratteristica
    senza_la = re.sub(r"\b(CR|GS|Str|Dex|Con|Int|Wis|Cha|For|Des|Cos|Sag|Car)\s*\d+", "", senza_la)
    # un numero subito dopo un nome di classe; non quelli dei DV razziali
    livelli = re.findall(r"[A-Za-zÀ-ÿ]\s*(\d{1,2})(?!\d)(?!\s*(?:DV|HD|dadi))", senza_la)
    return sum(int(x) for x in livelli) + la


def verifica(registro: Path, state: "Path | None" = STATE) -> "list[Violazione]":
    testo = registro.read_text(encoding="utf-8")
    dati = leggi(testo)
    nome = registro.name
    viol: "list[Violazione]" = []
    colonne, nomi = dati["colonne"], dati["nomi_totali"]
    if not colonne or "PX" not in dati["totali"]:
        return [Violazione("forma", "—", "tabelle «Riga» e «Totali» con la riga PX",
                           "non trovate", "campaign/REGISTRO-PX.md", nome)]
    for riga, cols in dati["intestazioni_diverse"]:
        viol.append(Violazione("forma", "—", " | ".join(colonne), " | ".join(cols),
                               "le tabelle «Riga» hanno tutte le colonne nello stesso ordine",
                               f"{nome}:{riga}"))
    abbreviate = dict(zip(colonne, nomi))  # Th → Thorik, nell'ordine delle colonne
    if len(nomi) != len(colonne):
        viol.append(Violazione("forma", "—", f"{len(colonne)} colonne nei totali",
                               str(len(nomi)), "campaign/REGISTRO-PX.md", nome))
    riga_px, celle_px = dati["totali"]["PX"]
    riga_liv, celle_liv = dati["totali"].get("Livello dai PX", (0, []))
    riga_tav, celle_tav = dati["totali"].get("Livello al tavolo", (0, []))
    tavolo_state = livelli_al_tavolo(state) if state and state.exists() else {}
    for i, col in enumerate(colonne):
        pg = abbreviate.get(col, col)
        somma = sum(v[i] for _, v in dati["righe"] if i < len(v) and v[i] is not None)
        totale = numero(celle_px[i]) if i < len(celle_px) else None
        if totale != somma:
            viol.append(Violazione("R1 somma", pg, f"{somma:,}".replace(",", "."),
                                   celle_px[i] if i < len(celle_px) else "—",
                                   "somma delle righe del registro", f"{nome}:{riga_px}"))
        px = somma
        if i < len(celle_liv):
            dichiarato = numero(celle_liv[i])
            if dichiarato is not None and dichiarato != livello_da_px(px):
                viol.append(Violazione("R2 soglia", pg, f"{livello_da_px(px)}°", celle_liv[i],
                                       FONTE_SOGLIE, f"{nome}:{riga_liv}"))
        tavolo = numero(celle_tav[i]) if i < len(celle_tav) else None
        if tavolo is not None and px >= soglia(tavolo + 2):
            viol.append(Violazione("R3 un livello", pg, f"PX < {soglia(tavolo + 2):,}".replace(",", "."),
                                   f"{px:,}".replace(",", "."), FONTE_UN_LIVELLO,
                                   f"{nome}:{riga_px}"))
        if tavolo is not None and px < soglia(tavolo):
            viol.append(Violazione("R3 un livello", pg,
                                   f"PX ≥ {soglia(tavolo):,} per il {tavolo}°".replace(",", "."),
                                   f"{px:,}".replace(",", "."), FONTE_SOGLIE, f"{nome}:{riga_tav}"))
        if tavolo is not None and tavolo_state and pg not in tavolo_state:
            viol.append(Violazione("R4 tavolo", pg, "una riga in state.yaml party[] (o «—» se è un PNG)",
                                   "nessuna", "campaign/state.yaml", f"{nome}:{riga_tav}"))
        elif tavolo is not None and pg in tavolo_state and tavolo_state[pg] != tavolo:
            viol.append(Violazione("R4 tavolo", pg, f"{tavolo_state[pg]}° (state.yaml, party.classe)",
                                   f"{tavolo}°", FONTE_ECL, f"{nome}:{riga_tav}"))
    return viol


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("registro", nargs="?", type=Path, default=REGISTRO)
    ap.add_argument("--state", type=Path, default=STATE)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    viol = verifica(a.registro, a.state)
    if not a.state.exists():
        print(f"⚠ {a.state} non esiste: R4 (livelli al tavolo) non controllata", file=sys.stderr)
    if a.json:
        print(json.dumps([asdict(v) for v in viol], ensure_ascii=False, indent=2))
    elif viol:
        for v in viol:
            print(f"✗ {v.regola} · {v.colonna}: atteso {v.atteso}, ha {v.ha} "
                  f"({v.fonte}) — {v.dove}")
    else:
        print(f"✓ {a.registro.name}: somme, soglie, un livello alla volta"
              + (" e livelli al tavolo tornano" if a.state.exists() else " tornano (R4 non controllata)"))
    return 1 if viol else 0


if __name__ == "__main__":
    sys.exit(main())
