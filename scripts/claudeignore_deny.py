#!/usr/bin/env python3
"""Traduce `.claudeignore` nelle regole `Read(...)` di `permissions.deny` (ADR-0142).

Claude Code non legge `.claudeignore` (provato il 2026-11-19: un file elencato
lì si apre comunque). Il meccanismo documentato è `permissions.deny` con
regole `Read(...)`, che valgono anche per Grep e Glob. `.claudeignore` resta
la fonte, scritta con la sintassi di `.gitignore`; questo script ne ricava le
regole in `.claude/settings.json` e `--check` le tiene allineate.

Restano leggibili apposta le voci di ESCLUSE, ognuna con il perché.

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

# Voci di .claudeignore che NON diventano un divieto, con il motivo.
_IMMAGINI = "le immagini si aprono apposta per la direzione artistica e le mappe; Grep salta i binari da solo"
_DOCUMENTI = "i PDF e gli ODS si aprono apposta (booklet, registro PX); Grep salta i binari da solo"
ESCLUSE: dict[str, str] = {
    ".claude/.skills-sync-status": "AGENTS.md chiede di leggerlo prima di generare contenuto di campagna",
    ".claude/skills/": "gli specchi delle skill per Claude: i references/ si leggono da lì; .gitignore li toglie già da Grep",
    **{p: _IMMAGINI for p in ("*.png", "*.gif", "*.bmp", "*.tif", "*.tiff", "*.psd", "*.ico")},
    **{p: _DOCUMENTI for p in ("*.pdf", "*.PDF", "*.ods", "*.odt", "*.xlsx", "*.xls", "*.docx")},
}


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


def regole(testo: str) -> list[str]:
    return [regola(v) for v in voci(testo) if v not in ESCLUSE]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="esce 1 se settings.json non è allineato")
    a = ap.parse_args()
    nuove = regole(SORGENTE.read_text(encoding="utf-8"))
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
              f"({len(ESCLUSE)} voci lasciate leggibili apposta)")
        return 0
    cfg["permissions"]["deny"] = attese
    SETTINGS.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"claudeignore_deny: {len(nuove)} regole Read in {SETTINGS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
