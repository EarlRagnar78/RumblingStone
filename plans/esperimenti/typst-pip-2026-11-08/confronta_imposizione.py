#!/usr/bin/env python3
"""pdfcpu contro pdfimpose: le stesse pagine su ogni mezza facciata? (ADR-0116, seconda parte)

    python3 confronta_imposizione.py VOLUME-STAMPA.pdf LIBRETTO-pdfcpu.pdf LIBRETTO-pdfimpose.pdf

Ogni mezza facciata dei due libretti si riconosce dalla pagina sorgente con più
parole in comune (Jaccard). Stampa una riga JSON: pagine, facciate, formato dei
fogli, se le coppie di pagine sono le stesse e il Jaccard più basso trovato.
I libretti si fanno con `pdfcpu booklet -c disable -- "formsize:A4, border:off,
margin:0" OUT 2 IN` e `python -m pdfimpose saddle --signature 2x1 --output OUT IN`.
"""
from __future__ import annotations

import json
import sys

import pymupdf


def meta(p):
    w, h = p.rect.width, p.rect.height
    if w > h:
        return [pymupdf.Rect(0, 0, w / 2, h), pymupdf.Rect(w / 2, 0, w, h)]
    return [pymupdf.Rect(0, 0, w, h / 2), pymupdf.Rect(0, h / 2, w, h)]


def mappa(doc, pagine):
    out = []
    for p in doc:
        riga = []
        for r in meta(p):
            parole = set(p.get_text(clip=r).split())
            if not parole:
                riga.append(None)
                continue
            j = [len(parole & s) / max(1, len(parole | s)) for s in pagine]
            migliore = max(range(len(pagine)), key=j.__getitem__)
            riga.append((migliore + 1, round(j[migliore], 2)))
        out.append(riga)
    return out


def main() -> int:
    src, a, b = (pymupdf.open(x) for x in sys.argv[1:4])
    pagine = [set(p.get_text().split()) for p in src]
    ma, mb = mappa(a, pagine), mappa(b, pagine)

    def coppie(m):
        return [sorted(x[0] for x in r if x) for r in m]
    diverse = [(i, x, y) for i, (x, y) in enumerate(zip(coppie(ma), coppie(mb))) if x != y]
    minimo = min([x[1] for r in ma + mb for x in r if x] or [1])
    print(json.dumps({
        "pagine_sorgente": len(src), "facciate": [len(a), len(b)],
        "formato_a": [round(a[0].rect.width, 1), round(a[0].rect.height, 1)],
        "formato_b": [round(b[0].rect.width, 1), round(b[0].rect.height, 1)],
        "stesse_coppie": coppie(ma) == coppie(mb), "coppie_diverse": diverse[:5],
        "jaccard_min": minimo}))
    return 0 if not diverse else 1


if __name__ == "__main__":
    sys.exit(main())
