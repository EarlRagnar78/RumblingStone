#!/usr/bin/env python3
"""Migrazione delle forme vecchie di canone alla grammatica di GUIDA-MARCATURE.

ADR-0109, scheda 2 = A: fuori da `plans/` le forme vecchie passano alla
grammatica, con il conto prima e dopo. Qui solo le sostituzioni meccaniche e
sicure; le righe di regola e i modelli si riscrivono a mano nello stesso commit.

  [ACCEPTED — DM-canon 2026-05-05]        → [CANONE — DM 2026-05-05]
  [ACCEPTED — DM-canon 2026-05-05, D10]   → [CANONE — DM 2026-05-05, D10]
  [ACCEPTED — DM-canon] · [ACCEPTED]      → [CANONE — DM <data>]
  (decisione DM 2026-09-24)               → [CANONE — DM 2026-09-24]
  *(decisione DM 2026-07-04: testo)*      → [CANONE — DM 2026-07-04: testo]

<data> per le marche senza data: la data che il file stesso dà alla scelta
(«Approvato dal DM il **2026-08-05**», o un'altra marca datata nello stesso
file, o il dossier nella stessa cartella), altrimenti la data del primo commit
che ha messo `ACCEPTED` nel file. Il rapporto dice quale, riga per riga.

Non tocca: `plans/`, archivi, changelog, volumi generati (.html, .svg, .json,
.hb.md), righe dentro `<!-- storico -->`, e gli script (si rigenerano).

Uso:  python3 migra_marche.py            # rapporto, nessuna scrittura
      python3 migra_marche.py --scrivi   # applica e scrive il rapporto
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QUI = Path(__file__).resolve().parent

SALTA = ("plans/", "scripts/", ".github/", "docs/audit/", "docs/reference/GUIDA-MARCATURE.md")
SALTA_PARTI = {"_ARCHIVIO", "Old", "_testi-altrui"}

DATATA = re.compile(r"\[ACCEPTED\s*[—-]\s*DM-canon\s+(\d{4}-\d{2}-\d{2})([^\]\n]*)\]")
SENZA_DATA = re.compile(r"\[ACCEPTED(?:\s*[—-]\s*DM-canon)?\]")
MENZIONE = re.compile(r"((?:marcat\w*|flagg\w*|\bgli|\bo|\btutti)\s*`?)\[ACCEPTED(?:\s*[—-]\s*DM-canon)?\]")
DECISIONE = re.compile(r"(\*?)\(decisione DM (\d{4}-\d{2}-\d{2})([^()\n]*)\)(\*?)")
DATA_NEL_FILE = re.compile(r"(?:DM il \*\*|DM-canon |CANONE — DM )(\d{4}-\d{2}-\d{2})")

VECCHIE = {
    "ACCEPTED": re.compile(r"\[ACCEPTED"),
    "decisione DM datata": re.compile(r"\(decisione DM \d{4}"),
    "needs DM confirmation": re.compile(r"needs DM\s+confirmation"),
}


def file_da_migrare() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "-z", "*.md", "*.yaml", "*.yml"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout.split("\0")
    scelti = []
    for rel in filter(None, out):
        if rel.startswith(SALTA) or rel.endswith(".hb.md") or "CHANGELOG" in rel \
                or rel.endswith("state-changelog.md"):
            continue
        if SALTA_PARTI & set(rel.split("/")):
            continue
        scelti.append(ROOT / rel)
    return scelti


def data_comparsa(rel: str) -> str:
    """Data del primo commit che ha messo `ACCEPTED` nel file (segue i rinomini)."""
    r = subprocess.run(["git", "log", "--follow", "--reverse", "--format=%as", "-S", "ACCEPTED",
                        "--", rel], cwd=ROOT, capture_output=True, text=True)
    righe = r.stdout.split()
    return righe[0] if righe else ""


def data_della_cartella(p: Path) -> str:
    """«Approvato dal DM il **data**» nel dossier della stessa cartella."""
    for altro in sorted(p.parent.glob("*.md")):
        m = re.search(r"DM il \*\*(\d{4}-\d{2}-\d{2})", altro.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return m.group(1)
    return ""


def conta(paths: list[Path]) -> Counter:
    c: Counter = Counter()
    for p in paths:
        t = p.read_text(encoding="utf-8", errors="ignore")
        for nome, rx in VECCHIE.items():
            c[nome] += len(rx.findall(t))
    return c


def migra(p: Path, scrivi: bool) -> list[dict]:
    rel = str(p.relative_to(ROOT))
    testo = p.read_text(encoding="utf-8")
    date_file = DATA_NEL_FILE.findall(testo)
    data_file = date_file[0] if date_file else ""
    righe = testo.split("\n")
    cambi = []
    dentro_storico = False
    for i, riga in enumerate(righe):
        nuova = riga
        if "<!-- storico" in riga and "<!-- /storico" not in riga:
            dentro_storico = True
        if dentro_storico or "<!-- storico" in riga:
            if "<!-- /storico" in riga:
                dentro_storico = False
            continue
        nuova = DATATA.sub(lambda m: f"[CANONE — DM {m.group(1)}{m.group(2)}]", nuova)
        # «o marcate `[ACCEPTED]`», «tutti gli [ACCEPTED]»: nomina la marca, non la mette.
        nuova = MENZIONE.sub(lambda m: m.group(1) + "[CANONE — DM data]", nuova)
        if SENZA_DATA.search(nuova):
            if data_file:
                data, da = data_file, "file"
            elif data_della_cartella(p):
                data, da = data_della_cartella(p), "dossier"
            else:
                data, da = data_comparsa(rel), "comparsa"
            nuova = SENZA_DATA.sub(f"[CANONE — DM {data}]", nuova)
        else:
            da = ""
        nuova = DECISIONE.sub(lambda m: f"[CANONE — DM {m.group(2)}{m.group(3)}]", nuova)
        if nuova != riga:
            cambi.append({"file": rel, "riga": i + 1, "data_da": da or "scritta",
                          "prima": riga.strip()[:160], "dopo": nuova.strip()[:160]})
            righe[i] = nuova
    if scrivi and cambi:
        p.write_text("\n".join(righe), encoding="utf-8")
    return cambi


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scrivi", action="store_true")
    a = ap.parse_args()
    paths = file_da_migrare()
    prima = conta(paths)
    cambi = [c for p in paths for c in migra(p, a.scrivi)]
    dopo = conta(paths) if a.scrivi else None
    da = Counter(c["data_da"] for c in cambi)
    print(f"file guardati {len(paths)} · righe cambiate {len(cambi)} in "
          f"{len({c['file'] for c in cambi})} file · data: {dict(da)}")
    print("prima:", dict(prima))
    if dopo is not None:
        print("dopo: ", dict(dopo))
        (QUI / "migrazione.json").write_text(json.dumps(
            {"prima": prima, "dopo": dopo, "data_da": da, "cambi": cambi},
            ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
