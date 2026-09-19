#!/usr/bin/env python3
"""
validate_skills.py — CI gate for the RumblingStone skill trees.

Checks (hard errors, exit 1):
  1. Every skills/<name>/SKILL.md has YAML frontmatter with:
     - name  == directory name
     - description (non-empty)
  2. Every markdown link [text](path) in skills/**/*.md that points to a
     relative path resolves to an existing file/dir (repo-relative fallback).
  3. Every data YAML in scripts/ (catalogs, alliances, loot, map templates)
     parses with yaml.safe_load.
  4. AGENTS.md routes every skill, both directions (ADR-0041):
     - every skills/<name>/ with a SKILL.md is cited in AGENTS.md
     - every skills/<name>/ cited in AGENTS.md exists on disk

Warnings (printed, exit 0):
  - reference files not mentioned anywhere in their skill's SKILL.md
    (orphaned references an agent would never load).

Usage:  python3 scripts/validate_skills.py [--repo-root PATH]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")

DATA_YAML_GLOBS = [
    "scripts/*.yaml",
    "scripts/map_templates/*.yaml",
]


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def check_skills(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skills_dir = root / "skills"
    skill_dirs = sorted(d for d in skills_dir.iterdir() if d.is_dir())
    if not skill_dirs:
        return ["no skill directories found under skills/"], warnings

    for skill in skill_dirs:
        skill_md = skill / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{skill.relative_to(root)}: missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        rel = skill_md.relative_to(root)
        if fm is None:
            errors.append(f"{rel}: missing or unparseable YAML frontmatter")
            continue
        if fm.get("name") != skill.name:
            errors.append(
                f"{rel}: frontmatter name {fm.get('name')!r} != directory name {skill.name!r}"
            )
        if not str(fm.get("description") or "").strip():
            errors.append(f"{rel}: frontmatter description missing/empty")

        # Orphaned reference files (warning only)
        refs_dir = skill / "references"
        if refs_dir.is_dir():
            for ref in sorted(refs_dir.glob("*.md")):
                if ref.name not in text:
                    warnings.append(
                        f"{ref.relative_to(root)}: not mentioned in {skill.name}/SKILL.md"
                    )
    return errors, warnings


def check_links(root: Path) -> list[str]:
    errors: list[str] = []
    for md in sorted((root / "skills").rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if re.match(r"^[a-z][a-z0-9+.-]*:", target):  # URL scheme
                continue
            # resolve relative to the file, then repo root as fallback
            cands = [md.parent / target, root / target]
            if not any(c.exists() for c in cands):
                errors.append(
                    f"{md.relative_to(root)}: broken relative link -> {target}"
                )
    return errors


def check_yaml_data(root: Path) -> list[str]:
    errors: list[str] = []
    for pattern in DATA_YAML_GLOBS:
        for path in sorted(root.glob(pattern)):
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                errors.append(f"{path.relative_to(root)}: YAML parse error: {exc}")
    return errors


SKILL_REF_RE = re.compile(r"skills/([A-Za-z0-9_-]+)/")


def check_agents_routing(root: Path) -> list[str]:
    """ADR-0041: AGENTS.md instrada ogni skill, e non ne cita di inesistenti.

    Il controllo e' bidirezionale di proposito. La direzione skill -> documento
    prende l'omissione (una skill nuova che nessuno ha instradato). La direzione
    documento -> skill prende il residuo (una skill rinominata o rimossa che
    lascia in AGENTS.md un puntatore morto). Il gate non giudica il testo:
    sa contare, e conta la sola cosa che si e' rotta davvero.
    """
    errors: list[str] = []
    agents = root / "AGENTS.md"
    if not agents.exists():
        return ["AGENTS.md: assente — non si puo' verificare l'instradamento (ADR-0041)"]
    text = agents.read_text(encoding="utf-8")

    on_disk = {d.name for d in (root / "skills").iterdir()
               if d.is_dir() and (d / "SKILL.md").exists()}
    cited = set(SKILL_REF_RE.findall(text))

    for name in sorted(on_disk - cited):
        errors.append(
            f"AGENTS.md: la skill 'skills/{name}/' esiste ma non e' instradata "
            f"(ADR-0041 — aggiungila alla tabella per compito e all'inventario)"
        )
    for name in sorted(cited - on_disk):
        errors.append(
            f"AGENTS.md: cita 'skills/{name}/' che non esiste su disco "
            f"(ADR-0041 — puntatore morto: rinominata o rimossa?)"
        )
    return errors


def check_orchestrazione(root: Path) -> list[str]:
    """ADR-0058: ogni skill sta in **uno** strato, e ogni conflitto ha un vincitore.

    🔴 **Il difetto che presidia.** Le regole di precedenza fra skill esistevano
    gia' — in **cinque punti diversi** di `AGENTS.md`, tutte in prosa: «la
    coerenza batte lo stile», «sopra `narrative-style`, che resta il fondo»,
    «regole opposte», «le righe si sommano», «read-aloud ceilings winning any
    conflict». Prosa sparsa non si puo' verificare, e una skill nuova poteva
    nascere senza che nessuno decidesse dove sta.

    Tre controlli, e nessuno giudica il testo:

    1. **Copertura**: ogni skill su disco compare in **esattamente uno** strato.
       Una skill nuova non collocata e' rossa; una collocata due volte anche.
    2. **Onesta'**: gli strati non nominano skill inesistenti.
    3. **Conflitti**: ogni riga della tabella dei conflitti nomina skill vere e
       porta un vincitore dichiarato.
    """
    errors: list[str] = []
    f = root / "skills" / "ORCHESTRAZIONE.md"
    if not f.exists():
        return ["skills/ORCHESTRAZIONE.md: assente (ADR-0058)"]
    text = f.read_text(encoding="utf-8")

    def _tabella(marca: str) -> "list[str]":
        i = text.find(marca)
        if i < 0:
            return []
        fine = text.find("\n## ", i)
        return [r for r in text[i:fine if fine > 0 else len(text)].splitlines()
                if r.startswith("|")]

    righe_strati = _tabella("<!-- orchestrazione: strati -->")
    if not righe_strati:
        return ["ORCHESTRAZIONE.md: manca il marcatore «orchestrazione: strati»"]

    on_disk = {d.name for d in (root / "skills").iterdir()
               if d.is_dir() and (d / "SKILL.md").exists()}

    collocate: "dict[str, list[str]]" = {}
    for riga in righe_strati:
        celle = [c.strip() for c in riga.strip("|").split("|")]
        if len(celle) < 3 or celle[0].startswith(("---", "Strato")):
            continue
        strato = celle[0]
        for nome in SKILL_REF_RE.findall(riga) or re.findall(r"`([a-z0-9-]+)`", celle[2]):
            collocate.setdefault(nome, []).append(strato)

    for nome in sorted(on_disk - set(collocate)):
        errors.append(
            f"ORCHESTRAZIONE.md: la skill '{nome}' non sta in nessuno strato "
            "(ADR-0058 — una skill senza posto nella gerarchia viene saltata "
            "o caricata a caso)")
    for nome in sorted(set(collocate) - on_disk):
        errors.append(f"ORCHESTRAZIONE.md: lo strato cita '{nome}', che non esiste")
    for nome, strati in sorted(collocate.items()):
        if len(strati) > 1:
            errors.append(
                f"ORCHESTRAZIONE.md: '{nome}' sta in {len(strati)} strati "
                f"({', '.join(strati)}) — la gerarchia deve essere una sola")

    righe_conf = _tabella("<!-- orchestrazione: conflitti -->")
    if not righe_conf:
        errors.append("ORCHESTRAZIONE.md: manca il marcatore «orchestrazione: conflitti»")
    for riga in righe_conf:
        celle = [c.strip() for c in riga.strip("|").split("|")]
        if len(celle) < 4 or celle[0].startswith(("---", "#")):
            continue
        # ⚠️ La tabella usa i nomi CORTI («indagine», «narrative-style»), che e'
        # come il repo li scrive in prosa. Il gate risolve il prefisso invece di
        # pretendere nomi lunghi: una tabella illeggibile non la rilegge nessuno.
        for nome in re.findall(r"`([a-z0-9-]+)`", celle[1]):
            if nome not in on_disk and f"rumblingstone-{nome}" not in on_disk:
                errors.append(
                    f"ORCHESTRAZIONE.md conflitto {celle[0]}: cita '{nome}', "
                    "che non e' una skill")
        if not celle[2]:
            errors.append(
                f"ORCHESTRAZIONE.md conflitto {celle[0]}: nessun vincitore "
                "dichiarato — un conflitto senza risoluzione si ridiscute ogni volta")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
    )
    ap.add_argument("--json", action="store_true",
                    help="emette il report in JSON (opt-in) invece del testo")
    args = ap.parse_args()
    root = args.repo_root.resolve()

    skill_errors, warnings = check_skills(root)
    link_errors = check_links(root)
    yaml_errors = check_yaml_data(root)
    routing_errors = check_agents_routing(root)
    orch_errors = check_orchestrazione(root)
    errors = (skill_errors + link_errors + yaml_errors + routing_errors
              + orch_errors)
    n_skills = len(list((root / "skills").glob("*/SKILL.md")))

    if args.json:
        print(json.dumps({
            "tool": "validate_skills", "ok": not errors,
            "skills": n_skills, "errors": errors, "warnings": warnings,
        }, indent=2, ensure_ascii=False))
        return 1 if errors else 0

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    print(
        f"\nvalidate_skills: {n_skills} skills checked — "
        f"{len(errors)} error(s), {len(warnings)} warning(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
