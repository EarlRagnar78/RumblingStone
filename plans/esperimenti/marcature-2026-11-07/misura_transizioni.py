#!/usr/bin/env python3
"""misura_transizioni.py — che fine fanno le righe marcate [INFERRED] (ADR-0109).

Legge `git log -p` dei `.md` e, per ogni riga tolta che portava `[INFERRED…]`,
cerca nello stesso blocco del diff la riga aggiunta più simile. Tolte le marche,
confronta testo e numeri. Coppie uguali ripetute (volumi .hb.md) contate una
volta sola.

Esiti:
  ->CANONE uguale / cambiata   il DM ha deciso; il testo è rimasto o è cambiato
  ->senza marca                la riga nuova non porta né INFERRED né CANONE
  riscritta/spostata           nessuna riga simile (rapporto < 0,5)
  rimossa senza sostituto      il blocco del diff non aggiunge righe

Uso: python3 plans/esperimenti/marcature-2026-11-07/misura_transizioni.py [--json]
"""
from __future__ import annotations

import difflib
import json
import re
import subprocess
import sys
from collections import Counter

INF = re.compile(r"\[INFERRED[^\]]*\]")
CAN = re.compile(r"\[(?:CANONE|ACCEPTED)[^\]]*\]")
GEN = re.compile(r"\[GENERATO[^\]]*\]")


def norm(s: str) -> str:
    for r in (INF, CAN, GEN):
        s = r.sub("", s)
    s = re.sub(r"\*\*|`|_", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def misura() -> tuple[Counter, Counter]:
    log = subprocess.run(
        ["git", "log", "-p", "--no-merges", "-U0", "--format=@@COMMIT %H", "--", "*.md"],
        capture_output=True, text=True, errors="ignore", check=True).stdout
    esiti, numeri, visti = Counter(), Counter(), set()
    meno: list[str] = []
    piu: list[str] = []

    def chiudi():
        for r in (x for x in meno if INF.search(x)):
            if not piu:
                esiti["rimossa senza sostituto"] += 1
                continue
            best = max(piu, key=lambda p: difflib.SequenceMatcher(None, norm(r), norm(p)).ratio())
            if difflib.SequenceMatcher(None, norm(r), norm(best)).ratio() < 0.5:
                esiti["riscritta/spostata"] += 1
                continue
            if INF.search(best) and not CAN.search(best):
                continue  # ancora INFERRED: non è una transizione
            dove = "->CANONE" if CAN.search(best) else "->GENERATO" if GEN.search(best) else "->senza marca"
            chiave = (norm(r), norm(best))
            if chiave in visti:
                continue
            visti.add(chiave)
            esiti[f"{dove} {'uguale' if chiave[0] == chiave[1] else 'cambiata'}"] += 1
            stessi = Counter(re.findall(r"\d+", chiave[0])) == Counter(re.findall(r"\d+", chiave[1]))
            numeri[f"{dove} {'numeri uguali' if stessi else 'numeri cambiati'}"] += 1
        meno.clear()
        piu.clear()

    for riga in log.splitlines():
        if riga.startswith(("@@", "diff ")):
            chiudi()
        elif riga.startswith(("---", "+++")):
            continue
        elif riga.startswith("-"):
            meno.append(riga[1:])
        elif riga.startswith("+"):
            piu.append(riga[1:])
    chiudi()
    return esiti, numeri


if __name__ == "__main__":
    e, n = misura()
    if "--json" in sys.argv:
        print(json.dumps({"esiti": e, "numeri": n}, ensure_ascii=False, indent=1))
    else:
        for k, v in sorted(e.items()):
            print(f"{v:5d}  {k}")
        for k, v in sorted(n.items()):
            print(f"{v:5d}  {k}")
