#!/usr/bin/env python3
"""conta_marche.py — la parte deterministica della prova A/B di ADR-0109.

Per ogni risposta (file .md) conta le marche INFERRED e quante seguono la
grammatica di GUIDA-MARCATURE: una domanda (c'è un «?») e una base («base:»).
Il giudizio sulle invenzioni non marcate lo dà il giudice cieco; questo script
conta solo ciò che si conta senza giudizio.

Uso: python3 conta_marche.py <cartella delle risposte> [--json]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARCA = re.compile(r"\[INFERRED(?P<coda>[^\]\n]*(?:\n[^\]\n]*){0,3})\]")
GRAMMATICA = re.compile(r"^\s*—\s*[^;]*\?\s*;\s*base:\s*\S", re.S)
VECCHIE = re.compile(r"needs DM\s+confirmation", re.I)


def conta(testo: str) -> dict:
    marche = [m.group("coda") for m in MARCA.finditer(testo)]
    return {
        "inferred": len(marche),
        "grammatica_nuova": sum(1 for c in marche if GRAMMATICA.search(c)),
        "nude": sum(1 for c in marche if not c.strip()),
        "forma_vecchia": sum(1 for c in marche if VECCHIE.search(c)),
        "con_base": sum(1 for c in marche if "base:" in c),
        "parole": len(testo.split()),
    }


if __name__ == "__main__":
    cartella = Path(sys.argv[1])
    righe = {p.stem: conta(p.read_text(encoding="utf-8", errors="ignore")) for p in sorted(cartella.glob("*.md"))}
    if "--json" in sys.argv:
        print(json.dumps(righe, ensure_ascii=False, indent=1))
    else:
        for k, v in righe.items():
            print(k, v)
