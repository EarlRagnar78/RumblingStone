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

Con `--rules` (usato in CI come **warning**, non gate) aggiunge controlli di
aderenza alle regole 3.5/campagna: (a) GS dichiarato vs benchmark PF1e
Monster-Statistics-by-CR (hp/AC entro tolleranza larga); (b) `**Status**:
inferred` ⇒ deve esserci un marcatore `[INFERRED]` nel corpo; (c) se il file
menziona un boost, deve avere una riga `Boost log:`.

Uso: python3 scripts/validate_bestiario.py [--rules] [--help]
Exit 0 = struttura ok (gli avvisi --rules NON fanno fallire); exit 1 = violazioni.
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
warnings: list[str] = []


def err(msg: str):
    errors.append(msg)


def warn(msg: str):
    warnings.append(msg)


# PF1e Monster-Statistics-by-CR benchmark (semplificato: hp medio e AC media
# per CR, tolleranze larghe). Fonte: skills/pathfinder-1e-srd (monster-advancement).
# Solo per il warning di --rules: un GS palesemente fuori scala va rivisto.
PF_BENCH = {  # cr: (hp_min, hp_max, ac_min, ac_max)
    1: (10, 25, 11, 16), 2: (16, 40, 12, 17), 3: (22, 55, 13, 18),
    4: (28, 70, 14, 19), 5: (34, 85, 15, 20), 6: (40, 100, 16, 21),
    7: (46, 120, 17, 22), 8: (52, 140, 18, 23), 9: (60, 160, 18, 24),
    10: (68, 185, 19, 25), 11: (76, 210, 20, 26), 12: (84, 240, 21, 27),
    13: (94, 270, 22, 28), 14: (104, 300, 22, 29), 15: (116, 340, 23, 30),
    16: (128, 380, 24, 31), 17: (140, 420, 25, 32), 18: (152, 470, 26, 33),
}


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


CATALOG_IDS: dict = {}


def check_rules(path: Path):
    """Controlli di aderenza alle regole (--rules, solo warning)."""
    rel = str(path.relative_to(ROOT))
    text = path.read_text(encoding="utf-8", errors="replace")
    low = text.lower()
    # (1) benchmark GS vs hp/AC (tolleranza larga: segnala solo fuori scala)
    cr = header_cr(text)
    if cr is not None and int(cr) in PF_BENCH:
        hp_min, hp_max, ac_min, ac_max = PF_BENCH[int(cr)]
        m_hp = re.search(r"\bhp\s*(\d+)", low)
        if m_hp:
            hp = int(m_hp.group(1))
            if hp < hp_min * 0.5 or hp > hp_max * 1.5:
                warn(f"{rel}: hp {hp} fuori scala per CR {cr:g} (atteso ~{hp_min}-{hp_max})")
        m_ac = re.search(r"\bac\s*(\d+)", low)
        if m_ac:
            ac = int(m_ac.group(1))
            if ac < ac_min - 4 or ac > ac_max + 4:
                warn(f"{rel}: AC {ac} fuori scala per CR {cr:g} (atteso ~{ac_min}-{ac_max})")
    # (2) policy flag: Status inferred ⇒ deve esserci un marcatore [INFERRED]
    m_status = re.search(r"\*\*Status\*\*[:\s]*([a-z\-]+)", low)
    if m_status and m_status.group(1).startswith("inferred") and "[inferred" not in low:
        warn(f"{rel}: Status=inferred ma manca un marcatore [INFERRED] nel corpo")
    # (3) Boost log obbligatorio se il file dichiara un boost
    if re.search(r"\bboost(ato|ed|are)?\b", low) and "boost log" not in low:
        warn(f"{rel}: menziona un boost ma non ha una riga `Boost log:`")


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0
    do_rules = "--rules" in sys.argv

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
                if do_rules:
                    check_rules(path)
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
                import difflib
                diff = list(difflib.unified_diff(
                    before.decode("utf-8", "replace").splitlines(),
                    after.decode("utf-8", "replace").splitlines(),
                    "committato", "rigenerato", lineterm="", n=1))[:24]
                cat.write_bytes(before)  # ripristina per non sporcare il worktree
                err("scripts/monster_catalog.yaml NON in sync: rigenerare con "
                    "`python3 scripts/build_monster_catalog.py` e committare. "
                    "Prime differenze:\n      " + "\n      ".join(diff))

    if do_rules and warnings:
        print(f"⚠ validate_bestiario --rules: {len(warnings)} avvisi (non bloccanti)", file=sys.stderr)
        for w in warnings:
            print("  ~", w, file=sys.stderr)

    if errors:
        print(f"✗ validate_bestiario: {len(errors)} violazioni", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        return 1
    n_stat = sum(1 for s in ("mostri", "villain", "png")
                 for p in (BEST / s).rglob("*.md")
                 if not p.name.startswith("README") and is_statblock(p))
    extra = f"; {len(warnings)} avvisi --rules" if do_rules else ""
    print(f"✓ validate_bestiario: struttura ok, {n_stat} statblock validi, catalogo in sync{extra}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
