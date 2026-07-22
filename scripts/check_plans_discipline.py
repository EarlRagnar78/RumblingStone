#!/usr/bin/env python3
"""
check_plans_discipline.py — gate della "regola d'oro" dei piani (ADR-0009).

Blocca (exit 1) un range di commit che modifica file STRUTTURALI del repo
senza aggiornare plans/CHANGELOG.md nello stesso range. Strutturale =
scripts/, skills/, Script/, .github/, plans/adr/ (l'infrastruttura).
Il contenuto di campagna (campaign/, archi 00_-09_, Bestiario/, PG/) NON
è strutturale: le sessioni giocate al tavolo non richiedono changelog.

Promemoria ADR (warning, exit 0): se il range introduce una nuova skill,
un nuovo script top-level o tocca i workflow CI senza toccare plans/adr/,
stampa l'invito a valutare un ADR. Non bloccante: «serve un ADR?» non è
decidibile da uno script — la decisione resta umana.

Dove gira:
  - CI (.github/workflows/ci.yml), solo su pull_request, contro il base ref;
  - hook pre-push locale (installato da scripts/install-git-hooks.sh);
    bypass consapevole: `git push --no-verify`.

Uso:
  python3 scripts/check_plans_discipline.py --base origin/main
"""
from __future__ import annotations

import argparse
import subprocess
import sys

CHANGELOG = "plans/CHANGELOG.md"
STRUCTURAL_PREFIXES = ("scripts/", "skills/", "Script/", ".github/", "plans/adr/")
ADR_PREFIX = "plans/adr/"


def git(args: list[str], cwd: str) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def changed_files(base: str, head: str, cwd: str) -> list[tuple[str, str]]:
    """[(status, path)] tra merge-base(base, head) e head."""
    merge_base = git(["merge-base", base, head], cwd)
    out = git(["diff", "--name-status", f"{merge_base}..{head}"], cwd)
    rows: list[tuple[str, str]] = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status, path = parts[0][:1], parts[-1]  # per R100 conta la destinazione
        rows.append((status, path))
    return rows


def needs_adr_reminder(rows: list[tuple[str, str]]) -> list[str]:
    reasons = []
    for status, path in rows:
        if status == "A" and path.startswith("skills/") and path.endswith("/SKILL.md"):
            reasons.append(f"nuova skill: {path}")
        if status == "A" and path.startswith("scripts/") and path.count("/") == 1 \
                and (path.endswith(".py") or path.endswith(".sh")):
            reasons.append(f"nuovo script top-level: {path}")
        if path.startswith(".github/workflows/"):
            reasons.append(f"workflow CI modificato: {path}")
    return reasons


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--base", default="origin/main", help="ref di confronto (default: origin/main)")
    ap.add_argument("--head", default="HEAD", help="ref da verificare (default: HEAD)")
    ap.add_argument("--repo-root", default=".", help="root del repo git")
    args = ap.parse_args()

    try:
        rows = changed_files(args.base, args.head, args.repo_root)
    except subprocess.CalledProcessError:
        # Clone shallow o ref assente: meglio un gate saltato E dichiarato
        # che un falso rosso — la CI usa fetch-depth: 0 apposta.
        print(f"⚠ check_plans_discipline: impossibile calcolare il diff "
              f"{args.base}..{args.head} (clone shallow? ref mancante?) — gate SALTATO")
        return 0

    paths = [p for _, p in rows]
    structural = [p for p in paths if p.startswith(STRUCTURAL_PREFIXES)]
    if not structural:
        print("✓ check_plans_discipline: nessun file strutturale nel range — ok")
        return 0

    if CHANGELOG not in paths:
        print("✗ REGOLA D'ORO VIOLATA (skill rumblingstone-plans / ADR-0009):")
        print(f"  il range modifica {len(structural)} file strutturali ma NON tocca {CHANGELOG}.")
        for p in structural[:15]:
            print(f"    - {p}")
        if len(structural) > 15:
            print(f"    … e altri {len(structural) - 15}")
        print("  Aggiungi la riga di tracciatura: | data | piano | lotto | PR/commit | esito |")
        print("  (e aggiorna plans/INDEX.md se il lavoro chiude/avanza un piano).")
        return 1

    print(f"✓ check_plans_discipline: {len(structural)} file strutturali + riga in {CHANGELOG} — ok")

    reasons = needs_adr_reminder(rows)
    if reasons and not any(p.startswith(ADR_PREFIX) for p in paths):
        print("⚠ PROMEMORIA ADR (non bloccante): il range contiene scelte potenzialmente")
        print("  strutturali senza alcun tocco a plans/adr/ — valuta se serve un ADR:")
        for r in sorted(set(reasons)):
            print(f"    - {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
