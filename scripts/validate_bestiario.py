#!/usr/bin/env python3
"""validate_bestiario.py — Gate CI per la libreria Bestiario/ (piano libreria, L0).

Fa rispettare lo standard della libreria di mostri/villain/PNG (T-D12):

  1. La struttura standard esiste (mostri/ villain/ png/ pregen-pcgen/ tokens/)
     e le locazioni legacy NON esistono più (Armate-UNITA-NUOVE, Monsters_Sheets,
     PNG/ a repo root).
  2. Ogni STATBLOCK (`*-crN*.md` in mostri|villain|png) rispetta il formato:
     - filename kebab-case minuscolo con CR (`nome-crN.md`, `05` = ½);
     - header obbligatori: **Faction**, **Role**, **Environment**, **CR**,
       **Source**, **Status**;
     - CR del filename coerente col CR dichiarato nell'header;
     - stato dichiarato nel titolo o nell'header ([ACCEPTED]/[INFERRED]/Status).
  3. Ogni DOSSIER (gli altri .md in villain|png) ha un titolo H1.
  4. `mostri/` contiene SOLO statblock (+ README*).
  5. `scripts/monster_catalog.yaml` è in sync con la libreria (rigenerazione
     in-memory riproduce il file committato) — chi tocca uno statblock e
     dimentica `python3 scripts/build_monster_catalog.py` rompe la CI.

Uso: python3 scripts/validate_bestiario.py [--help]
Exit 0 = tutto ok; exit 1 = violazioni (elencate su stderr).
"""
import re
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEST = ROOT / "Bestiario"

STATBLOCK_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
HAS_CR_RE = re.compile(r"-cr(\d+)")
REQUIRED_HEADERS = ["**Faction**", "**Role**", "**Environment**", "**CR**",
                    "**Source**", "**Status**"]
LEGACY_PATHS = [
    "00_Red Hand Of Doom/Armate-UNITA-NUOVE",
    "00_Red Hand Of Doom/Monsters_Sheets",
    "PNG",
]
SUBDIRS = ["mostri", "villain", "png", "pregen-pcgen", "tokens"]

errors: list[str] = []


def err(msg: str):
    errors.append(msg)


def filename_cr(name: str):
    m = HAS_CR_RE.search(name)
    if not m:
        return None
    raw = m.group(1)
    if raw.startswith("0") and len(raw) > 1:   # cr05 = CR 1/2, cr025 = CR 1/4
        return int(raw) / (10 ** (len(raw) - 1))
    return float(raw)


def header_cr(text: str):
    m = re.search(r"\*\*CR\*\*[:\s]*([\d]+(?:[.,]\d+)?(?:/\d+)?)", text)
    if not m:
        return None
    val = m.group(1).replace(",", ".")
    if "/" in val:
        num, den = val.split("/")
        return float(num) / float(den)
    return float(val)


def check_statblock(path: Path):
    rel = path.relative_to(ROOT)
    name = path.name
    if not STATBLOCK_RE.match(name):
        err(f"{rel}: filename non kebab-case minuscolo (`nome-crN.md`)")
    text = path.read_text(encoding="utf-8", errors="replace")
    for h in REQUIRED_HEADERS:
        if h not in text:
            err(f"{rel}: header obbligatorio mancante: {h}")
    f_cr, h_cr = filename_cr(name), header_cr(text)
    if f_cr is not None and h_cr is not None and abs(f_cr - h_cr) > 0.01:
        err(f"{rel}: CR filename ({f_cr:g}) ≠ CR header ({h_cr:g})")
    if h_cr is None:
        err(f"{rel}: CR non leggibile dall'header **CR**")
    first = text.splitlines()[0] if text.splitlines() else ""
    if not (re.search(r"\[(ACCEPTED|INFERRED)", first)
            or re.search(r"\*\*Status\*\*[:\s]*\S", text)):
        err(f"{rel}: stato non dichiarato ([ACCEPTED]/[INFERRED] nel titolo o **Status** valorizzato)")


def check_dossier(path: Path):
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"^#\s+\S", text, re.MULTILINE):
        err(f"{rel}: dossier senza titolo H1")


def is_statblock(path: Path) -> bool:
    return bool(HAS_CR_RE.search(path.name.lower())) and path.suffix == ".md" \
        and path.name == path.name.lower()


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0

    # 1. struttura + legacy
    if not BEST.is_dir():
        print("✗ validate_bestiario: cartella Bestiario/ assente", file=sys.stderr)
        return 1
    for sub in SUBDIRS:
        if not (BEST / sub).is_dir():
            err(f"Bestiario/{sub}/ mancante (struttura standard T-D12)")
    for legacy in LEGACY_PATHS:
        if (ROOT / legacy).exists():
            err(f"locazione legacy ancora presente: {legacy} (va spostata in Bestiario/)")

    # 2-4. statblock e dossier
    for sub in ("mostri", "villain", "png"):
        d = BEST / sub
        if not d.is_dir():
            continue
        for path in sorted(d.rglob("*.md")):
            if path.name.startswith("README"):
                continue
            if is_statblock(path):
                check_statblock(path)
            else:
                if sub == "mostri":
                    err(f"{path.relative_to(ROOT)}: in mostri/ sono ammessi solo statblock `-crN.md` (+ README)")
                check_dossier(path)

    # 5. catalogo in sync
    build = ROOT / "scripts" / "build_monster_catalog.py"
    cat = ROOT / "scripts" / "monster_catalog.yaml"
    if build.exists() and cat.exists():
        before = cat.read_bytes()
        r = subprocess.run([sys.executable, str(build)], capture_output=True)
        if r.returncode != 0:
            err("build_monster_catalog.py fallisce: " + r.stderr.decode()[-200:])
        else:
            after = cat.read_bytes()
            if before != after:
                cat.write_bytes(before)  # ripristina per non sporcare il worktree
                err("scripts/monster_catalog.yaml NON in sync: rigenerare con "
                    "`python3 scripts/build_monster_catalog.py` e committare")

    if errors:
        print(f"✗ validate_bestiario: {len(errors)} violazioni", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        return 1
    n_stat = sum(1 for s in ("mostri", "villain", "png")
                 for p in (BEST / s).rglob("*.md")
                 if not p.name.startswith("README") and is_statblock(p))
    print(f"✓ validate_bestiario: struttura ok, {n_stat} statblock validi, catalogo in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
