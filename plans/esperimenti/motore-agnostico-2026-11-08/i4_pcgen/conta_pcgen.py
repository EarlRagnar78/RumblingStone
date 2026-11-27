#!/usr/bin/env python3
"""conta_pcgen.py — indagine I4 di PIANO-MOTORE-AGNOSTICO-D20: quanto PCGen ha migrato al formulario nuovo.

Legge un clone di https://github.com/PCGen/pcgen (anche parziale: bastano
system/gameModes/<modo> e le cartelle di data/ nominate qui sotto) e conta, per
ogni insieme di dati, le righe con il formulario vecchio (`BONUS:`, espressioni
JEP) e quelle con il nuovo (`MODIFY:`/`MODIFYOTHER:`, variabili dichiarate con
scope in `*variables.lst`). Conta anche le formule che il game mode scrive come
testo (`SPELLBASEDC:`, `SPELLRANGE:`, `MINXP:` …), lasciando fuori i numeri soli,
che sono righe di tabella.

    git clone --depth 1 --filter=blob:none --sparse https://github.com/PCGen/pcgen.git pcgen
    git -C pcgen sparse-checkout set system/gameModes/35e system/gameModes/Pathfinder \\
        data/pathfinder/paizo/roleplaying_game/core_rulebook data/35e/wizards_of_the_coast/rsrd
    python3 conta_pcgen.py pcgen --json RISULTATI.json
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

INSIEMI = {
    "PF1e Core Rulebook": "data/pathfinder/paizo/roleplaying_game/core_rulebook",
    "3.5 RSRD": "data/35e/wizards_of_the_coast/rsrd",
}
MODI = {"35e": "system/gameModes/35e", "Pathfinder": "system/gameModes/Pathfinder"}
FORMULE_MODO = ("SPELLBASEDC", "SPELLBASECONCENTRATION", "SPELLRANGE", "MINXP", "CSKILLMAX",
                "CCSKILLMAX", "CRFORMULA", "STATMOD", "BABMAXATT", "BONUSFEATLEVELSTARTINTERVAL")


def conta(cartella: Path) -> dict:
    vecchio = nuovo = variabili = 0
    file = sorted(cartella.rglob("*.lst"))
    for f in file:
        for r in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if r.lstrip().startswith("#"):
                continue
            vecchio += len(re.findall(r"(?:^|\t)BONUS:", r))
            nuovo += len(re.findall(r"(?:^|\t)MODIFY(?:OTHER)?:", r))
            if f.name.endswith("variables.lst") and re.match(r"^(GLOBAL|LOCAL|CHANNEL):", r):
                variabili += 1
    tot = vecchio + nuovo
    return {"file_lst": len(file), "BONUS": vecchio, "MODIFY": nuovo, "variabili_dichiarate": variabili,
            "quota_nuovo_%": round(100 * nuovo / tot, 2) if tot else None}


def formule_modo(cartella: Path) -> list[str]:
    out = []
    for f in sorted(cartella.glob("*.lst")):
        for r in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if r.startswith("#"):
                continue
            for campo in r.split("\t"):
                k, _, v = campo.partition(":")
                if k in FORMULE_MODO and v and not re.fullmatch(r"[0-9|]+", v):  # i numeri soli sono tabelle
                    out.append(f"{f.name} {k}:{v}")
    return sorted(set(out))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("clone", type=Path)
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    commit = subprocess.run(["git", "-C", str(a.clone), "log", "-1", "--format=%H %cs"],
                            capture_output=True, text=True).stdout.strip()
    ris = {"commit_pcgen": commit,
           "insiemi": {n: conta(a.clone / p) for n, p in INSIEMI.items() if (a.clone / p).is_dir()},
           "formule_nel_game_mode": {n: formule_modo(a.clone / p) for n, p in MODI.items() if (a.clone / p).is_dir()}}
    print(f"PCGen {commit}")
    for n, c in ris["insiemi"].items():
        print(f"  {n:22} {c}")
    for n, fs in ris["formule_nel_game_mode"].items():
        print(f"  game mode {n}: {len(fs)} formule scritte come testo")
    if a.json:
        a.json.write_text(json.dumps(ris, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
