#!/usr/bin/env python3
"""validate_modules.py — lint deterministico dei MASTER DEFINITIVI (ARC*-DEF-*).

Review automatica e SENZA token (niente LLM): verifica che ogni master
definitivo rispetti la checklist della skill `rumblingstone-module-standard`
(sezioni obbligatorie, niente terminologia 5e/deprecata, mappe in scala).
Stesso stile degli altri validator del repo (exit 1 = errori bloccanti;
i warning non bloccano).

Uso:  python scripts/validate_modules.py [--verbose]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOB = "ARC*-DEF-*.md"

# --- Sezioni obbligatorie (checklist skill, §Struttura 1-14) -----------------
REQUIRED = [
    (r"^## INDICE", "INDICE del modulo"),
    (r"QUICKSTART", "Quickstart DM"),
    (r"QUICK-REFERENCE", "Quick-Reference stampabile"),
    (r"HIGHLIGHT", "Highlight asimmetrici per PG"),
    (r"Tattiche .*round", "Tattiche round-per-round (stile RHoD)"),
    (r"Scalare lo scontro", "Sidebar scaling (stile RHoD)"),
    (r"Contingenze", "Contingenze «Se i PG fanno X»"),
    (r"[Ss]confitta", "Ramo sconfitta (mai TPK gratuito)"),
    (r"Sviluppi", "Riga Sviluppi negli incontri"),
    (r"ECHI|Echo Ledger", "Echo Ledger / conseguenze"),
    (r"Budget PX|PX .*sezione", "Budget PX sezione-per-sezione"),
    (r"[Tt]esoro PREGENERATO|Tesoro pregenerato", "Tesoro pregenerato itemizzato"),
    (r"HANDOUT", "Handout & Asset"),
    (r"### MAPPA", "Mappe ASCII ultra-clear"),
    (r"1,5 m", "Scala 1,5 m/quadretto dichiarata"),
    (r"Pathfinder 1e|PF1e", "Box supporto PF1e (dove il 3.5 è vago)"),
]

# --- Termini banditi (5e / canone deprecato) ---------------------------------
# Una riga che contiene un termine bandito è ESENTE se contiene anche un
# marcatore di divieto/deprecazione (es. la frase che vieta il termine stesso).
BANNED = [
    (r"\bbonus action\b", "terminologia 5e (bonus action → azione veloce/swift)"),
    (r"\blair action", "terminologia 5e (lair action → attacco speciale con ricarica)"),
    (r"\bazioni? del covo\b", "terminologia 5e (azione del covo)"),
    (r"\bDC\s?[0-9]", "usare CD, non DC (convenzione repo)"),
    (r"\bNymeria\b", "canone deprecato (il compagno è DURIK, D14)"),
    (r"\bSkulldark\b|\bInfernotooth\b", "canone deprecato (il drago è SKULLCRUSHER, D6)"),
    (r"[Cc]ane da [Gg]uerra .*(COSTRUTTO|animato)", "canone deprecato (Durik è compagno VIVENTE riforgiato)"),
]
EXEMPT = re.compile(
    r"niente|MAI 5e|mai 5e|rimoss|vietat|deprecat|non usare|→|banditi|Errato"
    r"|errato|convenzione|usava|avevano|superat|storic|fonte|era(no)? ",
)


def check_file(path: Path, verbose: bool) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []
    warnings: list[str] = []

    for pattern, label in REQUIRED:
        if not re.search(pattern, text, re.MULTILINE):
            errors.append(f"sezione mancante: {label} (pattern /{pattern}/)")

    for pattern, label in BANNED:
        rx = re.compile(pattern)
        for i, line in enumerate(lines, 1):
            if rx.search(line) and not EXEMPT.search(line):
                errors.append(f"r.{i}: termine bandito — {label}: «{line.strip()[:80]}»")

    n_readaloud = len(re.findall(r"[Rr]ead-aloud", text))
    if n_readaloud < 5:
        warnings.append(f"solo {n_readaloud} read-aloud (attesi ≥5 per un master AP-quality)")
    if "[INFERRED" not in text:
        warnings.append("nessun flag [INFERRED]: verificare che ogni fatto nuovo sia attestato")
    if verbose:
        print(f"  {path.name}: {n_readaloud} read-aloud, "
              f"{len(re.findall(r'### MAPPA', text))} mappe")

    return errors, warnings


def main() -> int:
    verbose = "--verbose" in sys.argv
    masters = sorted(ROOT.glob(f"**/{GLOB}"))
    masters = [m for m in masters if "_ARCHIVIO" not in m.parts and "build" not in m.parts]
    if not masters:
        print("✓ validate_modules: nessun master ARC*-DEF-* nel repo — ok")
        return 0

    total_err = 0
    for m in masters:
        errors, warnings = check_file(m, verbose)
        rel = m.relative_to(ROOT)
        for w in warnings:
            print(f"  ⚠ {rel}: {w}")
        for e in errors:
            print(f"  ✗ {rel}: {e}")
        total_err += len(errors)

    if total_err:
        print(f"✗ validate_modules: {len(masters)} master, {total_err} errore/i "
              f"(checklist skill rumblingstone-module-standard)")
        return 1
    print(f"✓ validate_modules: {len(masters)} master conformi alla checklist "
          f"module-standard — 0 errori")
    return 0


if __name__ == "__main__":
    sys.exit(main())
