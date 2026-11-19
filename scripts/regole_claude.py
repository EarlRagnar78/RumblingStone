#!/usr/bin/env python3
"""Ricava da AGENTS.md le regole di Claude Code in `.claude/rules/` (ADR-0141).

AGENTS.md resta la fonte unica: lo leggono anche Codex, Copilot e gli altri
agenti. Claude Code invece carica le regole di `.claude/rules/` solo quando
legge un file che corrisponde al loro `paths:`; quelle senza `paths:` entrano
al primo file letto nel repo. Così le sezioni che servono solo a certi file
non occupano il contesto degli altri compiti.

La tabella SEZIONI dice dove va ogni sezione. Il controllo è deterministico:
ogni sezione di AGENTS.md finisce in una regola sola, e le regole rimesse
insieme danno di nuovo AGENTS.md riga per riga.

Uso:
  python3 scripts/regole_claude.py            # scrive .claude/rules/
  python3 scripts/regole_claude.py --check    # esce 1 se le regole non sono allineate
  python3 scripts/regole_claude.py --misura   # caratteri caricati per compito tipo
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / "AGENTS.md"
DEST = ROOT / ".claude" / "rules"
PREFISSO = "rs-"

CONTENUTI = ["0[0-9]_*/**", "10-stand-alone/**", "campaign/**", "Bestiario/**", "PG/**"]
SKILL = ["skills/**", "scripts/build-skills.sh", "scripts/sync-skills.sh",
         "scripts/validate_skills.py", ".claude/**"]
CONFIG = [".claude/**", ".mcp.json", "scripts/mcp_server.py", "scripts/claude-progetto.sh",
          "scripts/tools.manifest.json", "scripts/regole_claude.py"]

# (file della regola, paths o None = sempre, titoli delle sezioni «## » o «### »).
# Il preambolo (prima del primo titolo) va nella regola che ha "" fra i titoli.
SEZIONI: list[tuple[str, list[str] | None, list[str]]] = [
    ("nucleo", None, [
        "", "## What This Repo Contains", "## Skills",
        "### 🥇 REGOLA D'ORO DELLA PROSA — una skill non è il suo `SKILL.md`",
        "### Cosa carico, in base a cosa sto per fare", "### Quando un agente risponde",
        "## For AI Agents: Key DO / DON'T",
    ]),
    ("inventario-skill", SKILL, ["### Inventario completo"]),
    ("campagna", CONTENUTI, ["## Campaign-Specific Conventions", "## Rules Adjudication Policy"]),
    ("strumenti-esterni", CONFIG, ["## Strumenti esterni: server MCP e skill dei plugin"]),
    ("agenti-supportati", SKILL + CONTENUTI, ["## Supported Agents"]),
]

# Compiti tipo per --misura: un file che il compito apre per primo.
COMPITI = {
    "script del repo": "scripts/dm.py",
    "piano o ADR": "plans/INDEX.md",
    "master d'arco": "07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md",
    "skill": "skills/rumblingstone-campaign/SKILL.md",
    "configurazione Claude": ".claude/settings.json",
}


def sezioni(testo: str) -> list[tuple[str, str]]:
    """Divide AGENTS.md ai titoli «## » fuori dai blocchi di codice.

    Un «### » apre una sezione sua solo se la tabella SEZIONI lo nomina;
    altrimenti resta dentro il «## » che lo precede.
    """
    nominati = {t for _, _, ts in SEZIONI for t in ts if t.startswith("### ")}
    pezzi: list[tuple[str, list[str]]] = [("", [])]
    in_codice = False
    for riga in testo.splitlines(keepends=True):
        if riga.lstrip().startswith("```"):
            in_codice = not in_codice
        if not in_codice and (re.match(r"## ", riga) or riga.rstrip("\n") in nominati):
            pezzi.append((riga.rstrip("\n"), []))
        pezzi[-1][1].append(riga)
    return [(titolo, "".join(righe)) for titolo, righe in pezzi]


def regole(testo: str) -> dict[str, str]:
    pezzi = sezioni(testo)
    titoli = [t for t, _ in pezzi]
    assegnati = [t for _, _, ts in SEZIONI for t in ts]
    mancanti = [t for t in titoli if t not in assegnati]
    doppi = sorted({t for t in assegnati if assegnati.count(t) > 1})
    inesistenti = [t for t in assegnati if t not in titoli]
    if mancanti or doppi or inesistenti:
        raise SystemExit(
            "regole_claude: la tabella SEZIONI non copre AGENTS.md esattamente una volta\n"
            f"  sezioni senza regola: {mancanti}\n  assegnate due volte: {doppi}\n"
            f"  titoli che AGENTS.md non ha: {inesistenti}")
    uscita: dict[str, str] = {}
    for nome, paths, ts in SEZIONI:
        corpo = "".join(c for t, c in pezzi if t in ts)
        testa = ""
        if paths:
            testa = "---\npaths:\n" + "".join(f'  - "{p}"\n' for p in paths) + "---\n"
        avviso = ("<!-- Generato da scripts/regole_claude.py da AGENTS.md (ADR-0141): "
                  "si corregge AGENTS.md, poi si rigenera. I percorsi sono dalla radice del repo. -->\n")
        uscita[f"{PREFISSO}{nome}.md"] = testa + avviso + corpo
    return uscita


def carica(file: str) -> list[str]:
    """Le regole che Claude Code carica quando apre `file` (percorso dalla radice del repo)."""
    caricate = []
    for nome, paths, _ in SEZIONI:
        if paths is None or any(fnmatch.fnmatch(file, p) for p in paths):
            caricate.append(f"{PREFISSO}{nome}.md")
    return caricate


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="esce 1 se .claude/rules/ non è allineata")
    ap.add_argument("--misura", action="store_true", help="caratteri caricati per compito tipo")
    a = ap.parse_args()
    testo = AGENTS.read_text(encoding="utf-8")
    nuove = regole(testo)
    if a.misura:
        tot = len(testo)
        print(f"AGENTS.md intero: {tot} caratteri")
        print("| compito | primo file | regole caricate | caratteri | rispetto ad AGENTS.md |")
        print("|---|---|---|---|---|")
        for compito, file in COMPITI.items():
            cs = carica(file)
            n = sum(len(nuove[c]) for c in cs)
            print(f"| {compito} | `{file}` | {', '.join(c[len(PREFISSO):-3] for c in cs)} | {n} | {100 * (n - tot) / tot:+.0f}% |")
        return 0
    attuali = {p.name: p.read_text(encoding="utf-8") for p in DEST.glob(f"{PREFISSO}*.md")}
    if a.check:
        if attuali != nuove:
            diverse = sorted(set(attuali) ^ set(nuove) | {k for k in nuove if attuali.get(k) != nuove[k]})
            print(f"regole_claude: .claude/rules/ non allineata ad AGENTS.md: {diverse}\n"
                  "  rigenera con: python3 scripts/regole_claude.py", file=sys.stderr)
            return 1
        print(f"✓ regole_claude: {len(nuove)} regole allineate ad AGENTS.md")
        return 0
    DEST.mkdir(parents=True, exist_ok=True)
    for vecchia in set(attuali) - set(nuove):
        (DEST / vecchia).unlink()
    for nome, corpo in nuove.items():
        (DEST / nome).write_text(corpo, encoding="utf-8")
    print(f"regole_claude: scritte {len(nuove)} regole in {DEST.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
