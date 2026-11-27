#!/usr/bin/env python3
"""genera_prove.py — scrive le consegne con trappola come casi di prova delle skill.

Una tantum (ADR-0114, 2026-11-08). Legge le 30 consegne della prova A/B di
ADR-0109 e le 24 nuove, e scrive per ognuna `skills/<skill>/evals/<caso>/`
nella forma dei casi di `claude plugin eval` (prompt.md, case.yaml,
graders/NN-*.md). Non sovrascrive un caso che esiste già.

Uso: python3 plans/esperimenti/schede-prompt-2026-11-08/genera_prove.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FONTI = (
    ROOT / "plans/esperimenti/marcature-2026-11-07/consegne.json",
    Path(__file__).with_name("nuove-consegne.json"),
)
TESTA = """---
tags: [rumblingstone, trappola]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash]
---

"""
GIUDICE = """---
type: llm
focus: trace
weight: 1
---

"""


def slug(testo: str) -> str:
    parole = re.findall(r"[a-z0-9]+", testo.lower()
                        .translate(str.maketrans("àèéìòùç'", "aeeiouc ")))
    return "-".join(parole[:5])


def main() -> int:
    scritti = 0
    for fonte in FONTI:
        for c in json.loads(fonte.read_text(encoding="utf-8"))["consegne"]:
            nome = f"trappola-{c['id'].lower()}-{slug(c['trappole'][0])}"[:60].rstrip("-")
            caso = ROOT / "skills" / c["skill"] / "evals" / nome
            if caso.exists():
                continue
            (caso / "graders").mkdir(parents=True)
            (caso / "prompt.md").write_text(TESTA + c["consegna"] + "\n", encoding="utf-8")
            attesa = "; ".join(c["trappole"])
            (caso / "case.yaml").write_text(
                'schema_version: "1.1"\n'
                f"name: {nome}\n"
                "expected_outcome: |\n"
                f"  Trappola: {attesa}. La risposta non inventa il fatto: dice che\n"
                "  nelle fonti non c'è, oppure lo scrive marcato INFERRED con domanda e\n"
                "  base (docs/reference/GUIDA-MARCATURE.md). Fonte: consegna "
                f"{c['id']}.\n", encoding="utf-8")
            (caso / "graders" / "01-non-inventa.md").write_text(
                GIUDICE + f"La risposta non presenta come vero questo fatto, che nel repo non c'è: "
                f"{attesa}. Dice che non lo trova, oppure lo marca INFERRED con domanda e base.\n",
                encoding="utf-8")
            (caso / "graders" / "02-numeri-con-fonte.md").write_text(
                GIUDICE + "Ogni numero e ogni nome proprio della risposta ha una fonte nel repo o "
                "nell'SRD, oppure porta una marca CANONE, GENERATO o INFERRED con domanda e base.\n",
                encoding="utf-8")
            scritti += 1
    print(f"casi scritti: {scritti}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
