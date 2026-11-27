#!/usr/bin/env python3
"""typst da PyPI (typst-py) contro la CLI di mise.lock, sugli stessi sorgenti.

Nata come prova della scelta del DM del 2026-11-08 («Prova pip in testing,
poi decidi»), poi «applicalo se funziona, come standard» (ADR-0116): PyPI è lo
standard e questa misura tiene d'occhio che il ripiego (la CLI) dia gli stessi
PDF, anche dopo ogni aggiornamento di typst.

Per ogni manifest dei booklet: `export_booklet_typst.py --all --keep-typ`
con `RUMBLINGSTONE_TYPST=cli` compila con la CLI (quella di mise.lock) e lascia il `.typ`; lo stesso `.typ`
si compila con `typst.compile()` del pacchetto PyPI, con gli stessi font,
radice, pacchetti e data. Poi si confrontano:

- numero di pagine;
- testo estratto pagina per pagina (PyMuPDF);
- ogni pagina rasterizzata a 72 dpi in grigio (sha256 dei pixel);
- i byte del file (solo informativo: la compressione delle immagini può
  cambiare senza cambiare un pixel).

Uscita 1 se un booklet differisce in pagine, testo o pixel, o se una delle due
compilazioni fallisce. Rapporto JSON con --json, tabella markdown su stdout.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from importlib import metadata
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))

import export_booklet_typst as ex  # noqa: E402
import pymupdf  # noqa: E402
import typst  # noqa: E402


def manifest_booklet() -> list[Path]:
    nomi = subprocess.run(["git", "ls-files", "-z", "*.manifest.json"], cwd=REPO,
                          capture_output=True, text=True, check=True).stdout.split("\0")
    return [REPO / n for n in nomi if n and not n.startswith("scripts/")]


def impronta(pdf: Path) -> dict:
    doc = pymupdf.open(pdf)
    testo = [p.get_text() for p in doc]
    pixel = [hashlib.sha256(p.get_pixmap(dpi=72, colorspace=pymupdf.csGRAY).samples).hexdigest()
             for p in doc]
    return {"pagine": len(doc), "testo": testo, "pixel": pixel,
            "sha": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "creatore": doc.metadata.get("creator", "")}


def compila_py(typ: Path, pdf: Path, ts: int) -> float:
    t0 = time.monotonic()
    opz = dict(output=str(pdf), root=str(ex.ROOT), font_paths=[str(ex.FONTS)],
               package_path=str(ex.PACCHETTI), timestamp=ts)
    try:
        typst.compile(str(typ), **opz)
    except typst.TypstError as e:  # lo stesso ripiego di export_booklet_typst.compila
        if "tags" not in str(e):
            raise
        typst.compile(str(typ), pdf_tags=False, **opz)
    return time.monotonic() - t0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", type=Path, help="rapporto completo")
    a = ap.parse_args()
    ts = int(os.environ.get("SOURCE_DATE_EPOCH") or subprocess.run(
        ["git", "log", "-1", "--format=%ct"], cwd=REPO, capture_output=True, text=True).stdout)
    # La CLI per l'export: dal 2026-11-08 la catena usa PyPI (ADR-0116).
    env = dict(os.environ, SOURCE_DATE_EPOCH=str(ts), RUMBLINGSTONE_TYPST="cli")
    righe, rossi = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        for man in manifest_booklet():
            base = man.name.removesuffix(".manifest.json")
            typ, pdf_cli = man.with_name(base + ".typ"), man.with_name(base + "-STAMPA.pdf")
            pdf_py = Path(tmp) / (base + ".pdf")
            r = {"booklet": str(man.relative_to(REPO))}
            t0 = time.monotonic()
            e = subprocess.run([sys.executable, str(REPO / "scripts/export_booklet_typst.py"), str(man),
                                "--all", "--keep-typ"], cwd=REPO, env=env, capture_output=True, text=True)
            r["s_cli_con_export"] = round(time.monotonic() - t0, 2)
            if e.returncode or not typ.exists():
                r["esito"] = "CLI fallita: " + e.stderr[-300:]
                rossi += 1; righe.append(r); continue
            try:
                r["s_py"] = round(compila_py(typ, pdf_py, ts), 2)
            except Exception as exc:  # noqa: BLE001 - il rapporto deve dire quale booklet
                r["esito"] = f"PyPI fallita: {exc}"[:400]
                rossi += 1; righe.append(r); continue
            c, p = impronta(pdf_cli), impronta(pdf_py)
            r.update(pagine=c["pagine"], creatore_cli=c["creatore"], creatore_py=p["creatore"],
                     stesse_pagine=c["pagine"] == p["pagine"],
                     testo_diverso=sum(x != y for x, y in zip(c["testo"], p["testo"])),
                     pixel_diversi=sum(x != y for x, y in zip(c["pixel"], p["pixel"])),
                     stessi_byte=c["sha"] == p["sha"])
            ok = r["stesse_pagine"] and not r["testo_diverso"] and not r["pixel_diversi"]
            r["esito"] = "uguale" if ok else "DIVERSO"
            rossi += not ok
            righe.append(r)
    print("| booklet | pagine | testo ≠ | pixel ≠ | stessi byte | esito |")
    print("|---|---:|---:|---:|---|---|")
    for r in righe:
        print(f"| {Path(r['booklet']).name} | {r.get('pagine', '–')} | {r.get('testo_diverso', '–')} | "
              f"{r.get('pixel_diversi', '–')} | {r.get('stessi_byte', '–')} | {r['esito']} |")
    tot = sum(r.get("pagine", 0) for r in righe)
    print(f"\n{len(righe)} booklet, {tot} pagine, {rossi} diversi o falliti; typst-py {metadata.version("typst")}")
    if a.json:
        a.json.write_text(json.dumps(righe, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return 1 if rossi else 0


if __name__ == "__main__":
    sys.exit(main())
