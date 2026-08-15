#!/usr/bin/env python3
"""validate_standalone.py — gate CI per i moduli autoconclusivi (`STANDALONE-*/`).

`validate_modules.py` copre solo i master `ARC*-DEF-*.md` della campagna: i moduli
standalone avevano **zero gate**. Questo script chiude il buco con controlli che una
regex può fare bene e un revisore umano fa male:

  1. **File obbligatori** — un modulo standalone senza guida DM o senza nota IP non
     è un modulo, è una bozza.
  2. **Riferimenti incrociati** — ogni `` `FILE.md` `` e ogni link relativo citato
     dentro il modulo deve esistere. È il difetto che si crea da solo rinominando.
  3. **Schede pregenerate** — ogni scheda ha le sezioni che servono al tavolo
     (Difesa / Attacco / Statistiche / Equipaggiamento) e dichiara un GS.
  4. **Termini vietati** — meccaniche 5e in un modulo 3.5/PF1e (vantaggio,
     svantaggio, azione bonus, reazione, DC al posto di CD).
  5. **Read-aloud** — ogni file-giornata deve avere almeno un box di prosa: un
     modulo senza testo da leggere ad alta voce non si gioca, si riassume.
  6. **I due contatori** — devono essere dichiarati con il valore di partenza.

Esce con codice 1 se trova errori: è pensato per la CI.

Uso:
    python3 scripts/validate_standalone.py            # tutti i moduli STANDALONE-*
    python3 scripts/validate_standalone.py --dir X    # solo quello
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# File che un modulo autoconclusivo deve avere per essere giocabile senza altro.
REQUIRED = {
    "hub": r"^00-.*\.md$",
    "guida del DM": r"^0?7-GUIDA-DM.*\.md$",
    "schede pregenerate": r"^PREGEN-.*\.md$",
    "statblocchi": r"^STATBLOCCHI.*\.md$",
    "nota IP": r"^IP-E-LICENZE\.md$",
}
# Almeno un file-giornata/capitolo di sessione.
SESSION_RE = re.compile(r"^0[1-3]-GIORNO-.*\.md$")

# Meccaniche 5e: non hanno posto in un modulo 3.5 o PF1e.
# ⚠ Solo le forme che sono DAVVERO la meccanica 5e. In italiano «una Lunghezza di
# vantaggio» è lingua normale: bandirla sarebbe un falso positivo, e un validatore
# che grida al lupo viene disattivato entro una settimana.
BANNED = {
    r"\bazione bonus\b": "azione bonus (5e) → azione veloce",
    r"\bcon (?:un )?vantaggio\b": "tirare «con vantaggio» (5e) → nessun equivalente",
    r"\bcon (?:uno )?svantaggio\b": "tirare «con svantaggio» (5e) → nessun equivalente",
    r"\blair action": "lair action (5e)",
    r"(?<![A-Za-z])DC\s+\d": "DC → CD (Classe Difficoltà)",
}

PREGEN_SECTIONS = ("Difesa", "Attacco", "Statistiche", "Equipaggiamento")


def module_dirs(only: str | None) -> list[Path]:
    if only:
        p = (ROOT / only).resolve()
        return [p] if p.is_dir() else []
    return sorted(d for d in ROOT.iterdir() if d.is_dir() and d.name.startswith("STANDALONE-"))


def check_required(mod: Path, errors: list[str]) -> None:
    names = [p.name for p in mod.glob("*.md")]
    for label, pattern in REQUIRED.items():
        if not any(re.match(pattern, n) for n in names):
            errors.append(f"{mod.name}: manca il file obbligatorio — {label} (`{pattern}`)")
    if not any(SESSION_RE.match(n) for n in names):
        errors.append(f"{mod.name}: nessun file-giornata (`0N-GIORNO-*.md`)")


_BASENAMES: set[str] | None = None


def _repo_basenames() -> set[str]:
    """Tutti i nomi-file del repo, per accettare le citazioni per nome corto.

    Il repo cita spesso un file col solo basename (`CREDITS.md`, `render_map_svg.py`)
    o con un percorso abbreviato con i puntini. Pretendere il percorso completo
    produrrebbe decine di falsi positivi e nessun difetto vero.
    """
    global _BASENAMES
    if _BASENAMES is None:
        _BASENAMES = {
            p.name for p in ROOT.rglob("*")
            if p.is_file() and ".git" not in p.parts and "node_modules" not in p.parts
        }
    return _BASENAMES


def check_crossrefs(mod: Path, errors: list[str]) -> None:
    """Ogni `FILE.md` citato fra backtick, e ogni link relativo, deve esistere."""
    backtick = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|json|svg|py))`")
    link = re.compile(r"\]\((?!https?:|#)([^)\s]+)\)")
    for f in sorted(mod.rglob("*.md")):
        if f.name.endswith(".hb.md"):
            continue  # artefatti Homebrewery: generati, non fonti
        text = f.read_text(encoding="utf-8", errors="ignore")
        for m in backtick.finditer(text):
            ref = m.group(1)
            if "*" in ref or ref.startswith(("<", ".")):
                continue  # glob, placeholder, o suffissi tipo `.hb.md`
            if (f.parent / ref).exists() or (mod / ref).exists() or (ROOT / ref).exists():
                continue
            if Path(ref).name in _repo_basenames():
                continue  # citato per nome corto: esiste altrove nel repo
            errors.append(f"{f.relative_to(ROOT)}: riferimento inesistente `{ref}`")
        for m in link.finditer(text):
            ref = m.group(1).split("#")[0]
            if not ref:
                continue
            if (f.parent / ref).exists() or (ROOT / ref).exists():
                continue
            errors.append(f"{f.relative_to(ROOT)}: link rotto ({ref})")


def check_pregen(mod: Path, errors: list[str], warnings: list[str]) -> None:
    for f in mod.glob("PREGEN-*.md"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        sheets = re.findall(r"^##\s+\d+\s+·\s+(.+)$", text, re.M)
        if not sheets:
            errors.append(f"{f.relative_to(ROOT)}: nessuna scheda riconosciuta (`## N · NOME`)")
            return
        for sec in PREGEN_SECTIONS:
            found = len(re.findall(rf"^###\s+{sec}\b", text, re.M))
            # Equipaggiamento sta in grassetto nel corpo, non come heading
            if sec == "Equipaggiamento":
                found = text.count("**Equipaggiamento**")
            if found < len(sheets):
                errors.append(
                    f"{f.relative_to(ROOT)}: sezione «{sec}» presente {found} volte "
                    f"su {len(sheets)} schede"
                )
        if len(re.findall(r"\*\*GS \d", text)) < len(sheets):
            warnings.append(f"{f.relative_to(ROOT)}: non tutte le schede dichiarano un GS")


def check_banned(mod: Path, errors: list[str]) -> None:
    for f in sorted(mod.rglob("*.md")):
        if f.name.endswith(".hb.md"):
            continue  # generati dai sorgenti: il difetto va segnalato una volta sola
        text = f.read_text(encoding="utf-8", errors="ignore")
        for pattern, why in BANNED.items():
            for m in re.finditer(pattern, text, re.I):
                line = text[: m.start()].count("\n") + 1
                errors.append(f"{f.relative_to(ROOT)}:{line}: termine vietato — {why}")


def check_readaloud(mod: Path, errors: list[str]) -> None:
    for f in sorted(mod.glob("*.md")):
        if not SESSION_RE.match(f.name):
            continue
        blocks = len(re.findall(r"^>\s*\*", f.read_text(encoding="utf-8", errors="ignore"), re.M))
        if blocks < 3:
            errors.append(
                f"{f.relative_to(ROOT)}: solo {blocks} righe di read-aloud "
                f"(minimo 3 per un file-giornata)"
            )


def check_counters(mod: Path, errors: list[str]) -> None:
    joined = "\n".join(
        f.read_text(encoding="utf-8", errors="ignore") for f in mod.glob("*.md")
    )
    for name in ("Morale", "Onore"):
        if not re.search(rf"{name}[^\n]*parte da", joined):
            errors.append(f"{mod.name}: il contatore «{name}» non dichiara il valore di partenza")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dir", help="valida solo questa cartella (relativa alla radice)")
    args = ap.parse_args()

    mods = module_dirs(args.dir)
    if not mods:
        print("✓ validate_standalone: nessun modulo STANDALONE-* da validare")
        return 0

    errors: list[str] = []
    warnings: list[str] = []
    for mod in mods:
        check_required(mod, errors)
        check_crossrefs(mod, errors)
        check_pregen(mod, errors, warnings)
        check_banned(mod, errors)
        check_readaloud(mod, errors)
        check_counters(mod, errors)

    for w in warnings:
        print(f"  ⚠ {w}")
    if errors:
        print(f"✗ validate_standalone: {len(errors)} violazioni")
        for e in errors:
            print(f"  - {e}")
        return 1

    n_files = sum(len(list(m.rglob("*.md"))) for m in mods)
    print(
        f"✓ validate_standalone: {len(mods)} modulo/i, {n_files} file — "
        f"struttura, riferimenti, schede e read-aloud ok"
        + (f" ({len(warnings)} warning)" if warnings else "")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
