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
  R2 soglia      il «Livello dai PX» è quello della tabella SRD 3.5 dei PX
                 (livello n da n·(n-1)/2 · 1.000 PX).
  R3 un livello  regola SRD 3.5: si sale di un livello alla volta, i PX
                 eccedenti si fermano a 1 sotto la soglia del livello dopo.
                 Quindi PX < soglia(livello al tavolo + 2).
  R4 tavolo      il «Livello al tavolo» di un PG è la somma dei livelli di
                 classe di `campaign/state.yaml` (`party[].classe`).

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
FONTE_SOGLIE = "SRD 3.5, Table: Experience and Level-Dependent Benefits"
FONTE_UN_LIVELLO = "SRD 3.5, Experience Points: «one level at a time»"


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
    testo = cella.strip().replace("°", "").replace("−", "-")
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
            colonne = celle[2:]
            continue
        if re.fullmatch(r"\d+", celle[0]) and colonne:
            righe.append((n, [numero(c) for c in celle[2:2 + len(colonne)]]))
    return {"colonne": colonne, "righe": righe, "totali": totali,
            "nomi_totali": nomi_totali}


def livelli_al_tavolo(state: Path) -> "dict[str, int]":
    try:
        import yaml
    except ImportError:  # pragma: no cover
        return {}
    dati = yaml.safe_load(state.read_text(encoding="utf-8")) or {}
    esito = {}
    for pg in dati.get("party", []) or []:
        classe = str(pg.get("classe", ""))
        esito[str(pg.get("pg"))] = sum(int(x) for x in re.findall(r"\b(\d{1,2})\b", classe))
    return esito


def verifica(registro: Path, state: "Path | None" = STATE) -> "list[Violazione]":
    testo = registro.read_text(encoding="utf-8")
    dati = leggi(testo)
    nome = registro.name
    viol: "list[Violazione]" = []
    colonne, nomi = dati["colonne"], dati["nomi_totali"]
    if not colonne or "PX" not in dati["totali"]:
        return [Violazione("forma", "—", "tabelle «Riga» e «Totali» con la riga PX",
                           "non trovate", "campaign/REGISTRO-PX.md", nome)]
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
        if tavolo is not None and pg in tavolo_state and tavolo_state[pg] != tavolo:
            viol.append(Violazione("R4 tavolo", pg, f"{tavolo_state[pg]}° (state.yaml, party.classe)",
                                   f"{tavolo}°", "campaign/state.yaml", f"{nome}:{riga_tav}"))
    return viol


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("registro", nargs="?", type=Path, default=REGISTRO)
    ap.add_argument("--state", type=Path, default=STATE)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    viol = verifica(a.registro, a.state)
    if a.json:
        print(json.dumps([asdict(v) for v in viol], ensure_ascii=False, indent=2))
    elif viol:
        for v in viol:
            print(f"✗ {v.regola} · {v.colonna}: atteso {v.atteso}, ha {v.ha} "
                  f"({v.fonte}) — {v.dove}")
    else:
        print(f"✓ {a.registro.name}: somme, soglie, un livello alla volta e livelli al tavolo tornano")
    return 1 if viol else 0


if __name__ == "__main__":
    sys.exit(main())
