#!/usr/bin/env python3
"""Traduce `.claudeignore` nelle regole `Read(...)` di `permissions.deny` (ADR-0142).

Claude Code non legge `.claudeignore` (provato il 2026-11-19: un file elencato
lì si apre comunque). Il meccanismo documentato è `permissions.deny` con
regole `Read(...)`, che valgono anche per Grep e Glob. `.claudeignore` resta
la fonte, scritta con la sintassi di `.gitignore`; questo script ne ricava le
regole in `.claude/settings.json` e `--check` le tiene allineate.

Restano leggibili apposta le voci che in `.claudeignore` stanno sotto un
commento «# leggibile: motivo»: la marca vale fino alla prima riga vuota o al
primo altro commento, e il motivo è obbligatorio.

Uso:
  python3 scripts/claudeignore_deny.py           # aggiorna .claude/settings.json
  python3 scripts/claudeignore_deny.py --check   # esce 1 se non è allineato
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SORGENTE = ROOT / ".claudeignore"
SETTINGS = ROOT / ".claude" / "settings.json"

MARCA = "# leggibile:"


def voci(testo: str) -> list[str]:
    out = []
    for riga in testo.splitlines():
        riga = riga.strip()
        if not riga or riga.startswith("#"):
            continue
        if riga.startswith("!"):
            raise SystemExit(f"claudeignore_deny: le negazioni non hanno un equivalente deny: {riga}")
        out.append(riga)
    return out


def regola(voce: str) -> str:
    """Una voce in sintassi gitignore diventa una regola Read di Claude Code.

    Con una barra prima della fine la voce è ancorata alla radice del repo
    («/x», relativa alla cartella del progetto); senza, vale a ogni livello
    («**/x»). Una cartella («x/») diventa «x/**».
    """
    corpo = voce.rstrip("/")
    cartella = voce.endswith("/")
    ancorata = "/" in corpo
    if corpo.startswith("**/"):
        percorso = corpo
    elif ancorata:
        percorso = "/" + corpo.lstrip("/")
    else:
        percorso = "**/" + corpo
    if cartella:
        percorso += "/**"
    return f"Read({percorso})"


def leggibili(testo: str) -> dict[str, str]:
    """Le voci sotto una marca «# leggibile: motivo», con il loro motivo."""
    out: dict[str, str] = {}
    motivo = None
    for riga in testo.splitlines():
        riga = riga.strip()
        if riga.startswith(MARCA):
            motivo = riga[len(MARCA):].strip()
            if not motivo:
                raise SystemExit("claudeignore_deny: «# leggibile:» senza motivo")
        elif not riga or riga.startswith("#"):
            motivo = None
        elif motivo is not None:
            out[riga] = motivo
    return out


def regole(testo: str) -> list[str]:
    salta = leggibili(testo)
    return [regola(v) for v in voci(testo) if v not in salta]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="esce 1 se settings.json non è allineato")
    a = ap.parse_args()
    testo = SORGENTE.read_text(encoding="utf-8")
    nuove = regole(testo)
    cfg = json.loads(SETTINGS.read_text(encoding="utf-8"))
    deny = cfg.setdefault("permissions", {}).setdefault("deny", [])
    altre = [r for r in deny if not r.startswith("Read(")]
    attese = altre + nuove
    if a.check:
        if deny != attese:
            print("claudeignore_deny: permissions.deny non è allineato a .claudeignore\n"
                  "  rigenera con: python3 scripts/claudeignore_deny.py", file=sys.stderr)
            return 1
        print(f"✓ claudeignore_deny: {len(nuove)} regole Read allineate a .claudeignore "
              f"({len(leggibili(testo))} voci lasciate leggibili apposta)")
        return 0
    cfg["permissions"]["deny"] = attese
    SETTINGS.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"claudeignore_deny: {len(nuove)} regole Read in {SETTINGS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
