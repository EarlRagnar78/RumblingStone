#!/usr/bin/env python3
"""
release_notes.py — le note di rilascio vengono dal CHANGELOG.md di progetto,
e gli restano allineate (ADR-0100).

Ripreso da iemod-fetch (tools/release_notes.py, MIT, stesso autore).

    python3 scripts/release_notes.py notes VERSIONE   # stampa la sezione
    python3 scripts/release_notes.py sync             # corregge le note pubblicate

`sync` gira nel workflow Release a ogni push su main che tocca il CHANGELOG:
ogni sezione `## [X.Y.Z]` che ha un rilascio vX.Y.Z pubblicato si confronta con
il testo di quel rilascio, e un testo che non corrisponde più si riscrive dalla
sezione. Il blocco «Verifica lo scaricamento» resta quello con cui il rilascio
è stato costruito, perché le sue impronte appartengono ai pacchetti. Modificare
un rilascio non crea ref, quindi basta GITHUB_TOKEN.

Exit: 0 ok · 2 errore d'uso · altro: l'errore di `gh`. Solo stdlib (più `gh`
per `sync`, che c'è sui runner di GitHub).
"""
from __future__ import annotations

import re
import subprocess
import sys

CHANGELOG = "CHANGELOG.md"
VERIFY = "\n\n### Verifica lo scaricamento"
_HEADING = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)


def versions(changelog: str) -> list[str]:
    return _HEADING.findall(changelog)


def section(changelog: str, version: str) -> str | None:
    m = re.search(rf"^## \[{re.escape(version)}\].*?$(.*?)(?=^## \[|\Z)",
                  changelog, re.DOTALL | re.MULTILINE)
    return m.group(1).strip() if m else None


def refreshed(body: str, text: str) -> str | None:
    """Il testo che `text` richiede, o None se il rilascio lo dice già."""
    cut = body.find(VERIFY)
    wanted = text + (body[cut:] if cut >= 0 else "")
    return None if wanted.strip() == body.strip() else wanted


def _gh(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=False)


def sync(changelog: str) -> int:
    for version in versions(changelog):
        tag = f"v{version}"
        shown = _gh("release", "view", tag, "--json", "body", "--jq", ".body")
        if shown.returncode != 0:
            continue                                   # non (ancora) rilasciata
        wanted = refreshed(shown.stdout.rstrip("\n"), section(changelog, version) or "")
        if wanted is None:
            continue
        edited = subprocess.run(["gh", "release", "edit", tag, "--notes-file", "-"],
                                input=wanted, text=True, check=False)
        if edited.returncode != 0:
            return edited.returncode
        print(f"{tag}: note aggiornate dal CHANGELOG.md")
    return 0


def main(argv: list[str]) -> int:
    if argv[1:] in (["--help"], ["-h"]):
        print(__doc__)
        return 0
    with open(CHANGELOG, encoding="utf-8") as fh:
        changelog = fh.read()
    if len(argv) == 3 and argv[1] == "notes":
        version = argv[2].lstrip("v")
        print(section(changelog, version) or f"Vedi CHANGELOG.md per la {version}.")
        return 0
    if len(argv) == 2 and argv[1] == "sync":
        return sync(changelog)
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
