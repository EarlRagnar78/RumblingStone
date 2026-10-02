#!/usr/bin/env python3
"""incorpora_immagini_artefatti.py — l'immagine dell'artefatto dentro la sua pagina.

Le schede vecchie degli artefatti avevano l'immagine incorporata nell'HTML: un
file solo, che si stampa e si passa a un giocatore senza portarsi dietro una
cartella. Ma la incorporavano a piena risoluzione (PNG da 1-2,7 MB a pagina).
Le schede nuove la collegavano come file accanto, o non l'avevano affatto.

Questo tool fa la cosa giusta per tutte, e la fa sempre allo stesso modo
(ADR-0072):

  · legge `PG/Artefatti/immagini-artefatti.json` (quale immagine per quale
    pagina) e il registro delle pagine vive in `ARTEFATTI-MATRICE-VERSIONI.md` §0;
  · riduce l'immagine a 480 px sul lato lungo e la ricomprime in **webp**
    (qualità 72: 20-60 KB, invece di un megabyte);
  · la mette **dentro** la pagina come `data:` URI, sotto la testata, marcata
    `data-immagine-artefatto="<chiave>"`. Rilanciato, la sostituisce e non la
    duplica;
  · un `<img src="file.jpg">` relativo già presente viene incorporato allo
    stesso modo, anche senza voce nel JSON.

Le immagini sorgente restano file nella cartella: sono i master, e questo
tool non li tocca.

Uso:
    python3 scripts/incorpora_immagini_artefatti.py            # scrive
    python3 scripts/incorpora_immagini_artefatti.py --check    # esce 1 se una pagina va rifatta

Dipendenze: stdlib + **Pillow** (è già fra i requisiti opzionali). Senza,
`--check` funziona lo stesso; scrivere no.
Exit code: 0 = ok · 1 = pagine da rifare (--check) o Pillow assente.
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "PG" / "Artefatti"
PAGINE_DIR = BASE / "Artefatti-Pg"
CONFIG = BASE / "immagini-artefatti.json"
MATRICE = BASE / "ARTEFATTI-MATRICE-VERSIONI.md"
MARKER = "<!-- versioni-artefatti -->"
LATO = 480
QUALITA = 72

STILE = ("display:block;margin:10px auto 16px auto;width:230px;max-width:60%;height:auto;"
         "border:2px solid #8B4513;border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,0.3);")
RE_MARCATA = re.compile(r'<img [^>]*data-immagine-artefatto="([^"]+)"[^>]*>')
RE_RELATIVA = re.compile(r'(<img\b[^>]*?\bsrc=")(?!data:|https?:)([^"]+)(")')


def pagine_vive() -> list[Path]:
    """Le pagine che il registro §0 dichiara vive (colonne giocatore e DM)."""
    testo = MATRICE.read_text(encoding="utf-8")
    dopo = testo.split(MARKER, 1)[1].lstrip("\n").splitlines()
    pagine = []
    for riga in dopo:
        if not riga.startswith("|"):
            break
        celle = [c.strip().strip("`") for c in riga.strip().strip("|").split("|")]
        if len(celle) < 5 or celle[0] in ("Artefatto",) or celle[0].startswith("---"):
            continue
        for c in celle[2:4]:
            if c not in ("—", "-", ""):
                pagine.append(PAGINE_DIR / c)
    return pagine


def chiave_pagina(p: Path) -> str:
    rel = p.relative_to(PAGINE_DIR).as_posix()
    return re.sub(r"(_DM)?\.html$", "", rel)


def webp_data_uri(sorgente: Path) -> str:
    from PIL import Image  # noqa: WPS433 — dipendenza opzionale, vedi docstring
    im = Image.open(sorgente)
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
    im.thumbnail((LATO, LATO))
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=QUALITA, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def tag(chiave: str, uri: str, alt: str) -> str:
    alt = alt.replace('"', "&quot;")
    return f'<img data-immagine-artefatto="{chiave}" src="{uri}" alt="{alt}" style="{STILE}">'


def inserisci_dopo_testata(testo: str, img: str) -> str:
    """Sotto la testata (<div class="header">…</div>), o in cima al body."""
    m = re.search(r'<div class="header">', testo)
    if m:
        # la testata si chiude al primo </div> allo stesso rientro dell'apertura
        riga = testo.rfind("\n", 0, m.start()) + 1
        rientro = testo[riga:m.start()]
        fine = testo.find("\n" + rientro + "</div>", m.end())
        if fine != -1:
            punto = fine + len("\n" + rientro + "</div>")
            return testo[:punto] + "\n\n" + rientro + img + testo[punto:]
    m = re.search(r"<body[^>]*>", testo)
    return testo[:m.end()] + "\n    " + img + testo[m.end():]


def elabora(pagina: Path, cfg: dict, cache: dict, scrivi: bool) -> bool:
    """True se la pagina cambia (o cambierebbe)."""
    testo = pagina.read_text(encoding="utf-8")
    nuovo = testo
    chiave_img = cfg["pagine"].get(chiave_pagina(pagina))

    def uri_di(chiave: str) -> str:
        if chiave not in cache:
            cache[chiave] = webp_data_uri(ROOT / cfg["immagini"][chiave]["file"])
        return cache[chiave]

    if chiave_img:
        info = cfg["immagini"][chiave_img]
        if not scrivi:
            m = RE_MARCATA.search(nuovo)
            return not (m and m.group(1) == chiave_img and not RE_RELATIVA.search(nuovo))
        # le <img> relative della stessa immagine si tolgono: la marcata le sostituisce
        nuovo = re.sub(r'\s*<img\b[^>]*\bsrc="(?!data:)[^"]+"[^>]*>', "", nuovo)
        img = tag(chiave_img, uri_di(chiave_img), info["alt"])
        if RE_MARCATA.search(nuovo):
            nuovo = RE_MARCATA.sub(lambda _m: img, nuovo, count=1)
        else:
            nuovo = inserisci_dopo_testata(nuovo, img)
    elif RE_RELATIVA.search(nuovo):
        if not scrivi:
            return True

        def incorpora(m: re.Match) -> str:
            f = (pagina.parent / m.group(2)).resolve()
            return m.group(1) + webp_data_uri(f) + m.group(3)
        nuovo = RE_RELATIVA.sub(incorpora, nuovo)
    if nuovo != testo:
        if scrivi:
            pagina.write_text(nuovo, encoding="utf-8")
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="non scrive; esce 1 se una pagina va rifatta")
    args = ap.parse_args()
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    if not args.check:
        try:
            import PIL  # noqa: F401
        except ImportError:
            print("Serve Pillow per convertire le immagini:  pip install pillow", file=sys.stderr)
            return 1
    cache: dict = {}
    cambiate = [p for p in pagine_vive() if elabora(p, cfg, cache, scrivi=not args.check)]
    for p in cambiate:
        print(("da rifare: " if args.check else "incorporata: ") + p.relative_to(ROOT).as_posix())
    if args.check and cambiate:
        print(f"✗ {len(cambiate)} pagine senza la loro immagine incorporata: "
              "python3 scripts/incorpora_immagini_artefatti.py", file=sys.stderr)
        return 1
    print(f"✓ incorpora_immagini_artefatti: {len(pagine_vive())} pagine vive, "
          f"{len(cambiate)} {'da rifare' if args.check else 'aggiornate'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
