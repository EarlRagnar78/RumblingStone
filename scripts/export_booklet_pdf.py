#!/usr/bin/env python3
"""export_booklet_pdf.py — PDF A4 delle schede di un booklet pergamena (ADR-0013 §5).

Prende il MANIFEST di un booklet (lo stesso di ``build_booklet_html.py``) e
salva UN PDF PER SCHEDA usando Chromium/Chrome headless: la resa è identica
al browser (stessa pagina HTML, CSS di stampa canonico — niente testata né
tab, pergamena a piena pagina A4). Di default esporta le sole pagine ✉
``tag: player`` (hint, echi, teaser): quelle che si stampano o si inviano.

Il PDF si può fare anche SENZA questo script: apri l'HTML nel browser,
clicca la scheda, poi «🖨 Salva PDF» (o Ctrl+P) → destinazione «Salva come
PDF», formato A4, margini «Nessuno», «Grafica di sfondo» attiva.

Uso:
    python3 scripts/export_booklet_pdf.py MANIFEST.json               # pagine player
    python3 scripts/export_booklet_pdf.py MANIFEST.json --all         # tutte le schede
    python3 scripts/export_booklet_pdf.py MANIFEST.json --pane c2 c3  # schede scelte
    python3 scripts/export_booklet_pdf.py MANIFEST.json --list        # elenca le schede
    python3 scripts/dm.py booklet MANIFEST.json --pdf                 # build+export

Output: ``<cartella del manifest>/pdf/<NN>-<titolo-slug>.pdf`` (la cartella
``pdf/`` è un artefatto locale: NON si committa, vedi .gitignore).

Dipendenze: stdlib + un binario Chromium/Chrome (cercato in PATH, in
``$BOOKLET_CHROME`` e nei percorsi Playwright tipo /opt/pw-browsers).
Exit code: 0 = ok · 1 = browser non trovato / export fallito · 2 = uso errato.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

BROWSER_CANDIDATES = [
    os.environ.get("BOOKLET_CHROME", ""),
    "chromium", "chromium-browser", "google-chrome", "google-chrome-stable",
    "chrome", "/opt/pw-browsers/chromium",
]


def find_browser() -> str | None:
    for c in BROWSER_CANDIDATES:
        if not c:
            continue
        p = shutil.which(c) or (c if Path(c).is_file() and os.access(c, os.X_OK) else None)
        if p:
            return p
    return None


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s or "scheda"


def panes_of(mf: dict) -> list[tuple[str, str, str]]:
    """[(pane_id, titolo, tag)] — c0 è la copertina, i capitoli partono da c1."""
    out = [("c0", "Copertina", "")]
    for k, ch in enumerate(mf["chapters"], 1):
        out.append((f"c{k}", ch["title"], ch.get("tag", "")))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("manifest", help="manifest *.manifest.json del booklet")
    ap.add_argument("--pane", nargs="+", help="ID scheda da esportare (es. c2 c3)")
    ap.add_argument("--all", action="store_true", help="tutte le schede, copertina inclusa")
    ap.add_argument("--list", action="store_true", help="elenca le schede e i loro ID")
    ap.add_argument("--outdir", help="cartella di output (default: <manifest dir>/pdf/)")
    ap.add_argument("--browser", help="binario Chromium/Chrome da usare")
    args = ap.parse_args(argv)

    mp = Path(args.manifest)
    if not mp.exists():
        print(f"ERRORE: manifest non trovato: {mp}", file=sys.stderr)
        return 2
    mf = json.loads(mp.read_text(encoding="utf-8"))
    panes = panes_of(mf)

    if args.list:
        for pid, title, tag in panes:
            mark = {"player": "✉", "dm": "⚠"}.get(tag, " ")
            print(f"  {pid:>4}  {mark}  {title}")
        return 0

    html = mp.parent / mf.get("out", mp.stem.replace(".manifest", "") + ".html")
    if not html.exists():
        print(f"ERRORE: HTML non trovato ({html}) — genera prima con "
              f"build_booklet_html.py / dm.py booklet", file=sys.stderr)
        return 2

    browser = args.browser or find_browser()
    if not browser:
        print("ERRORE: nessun Chromium/Chrome trovato (PATH, $BOOKLET_CHROME, "
              "/opt/pw-browsers). In alternativa: apri l'HTML nel browser, scegli "
              "la scheda e usa «🖨 Salva PDF» (Ctrl+P, A4, sfondi attivi).",
              file=sys.stderr)
        return 1

    if args.pane:
        wanted = {p.lower() for p in args.pane}
        selected = [p for p in panes if p[0] in wanted]
        missing = wanted - {p[0] for p in selected}
        if missing:
            print(f"ERRORE: schede inesistenti: {', '.join(sorted(missing))} "
                  f"(usa --list)", file=sys.stderr)
            return 2
    elif args.all:
        selected = panes
    else:
        selected = [p for p in panes if p[2] == "player"]
        if not selected:
            print("Nessuna pagina ✉ player nel manifest: usa --all o --pane (vedi --list).",
                  file=sys.stderr)
            return 2

    outdir = Path(args.outdir) if args.outdir else mp.parent / "pdf"
    outdir.mkdir(parents=True, exist_ok=True)

    ok = True
    for i, (pid, title, _tag) in enumerate(selected):
        out = outdir / f"{i:02d}-{slug(title)}.pdf"
        url = html.resolve().as_uri() + "#" + pid
        cmd = [browser, "--headless", "--disable-gpu", "--no-sandbox",
               "--no-pdf-header-footer", "--virtual-time-budget=4000",
               f"--print-to-pdf={out}", url]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 and out.exists() and out.stat().st_size > 0:
            print(f"OK {out} ({out.stat().st_size / 1024:.0f} KB) ← {title}")
        else:
            ok = False
            print(f"✗ export fallito per {pid} ({title}): "
                  f"{(r.stderr or r.stdout).strip()[:300]}", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
