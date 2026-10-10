#!/usr/bin/env python3
"""Quanti simboli-oggetto usa il corpus delle mappe nel tema texture, e in quante celle.

Riproducibile: python3 plans/esperimenti/oggetti-cc0-2026-10/misura_simboli.py
Conta le celle delle griglie dei master che hanno un SVG in rendered-texture/
(gli stessi che rigenera `render_map_svg.py --tutti-i-master --tema texture`).
"""
import collections
import json
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RADICE / "scripts"))
import render_map_svg as r  # noqa: E402

master = sorted({p.parent.parent / f"{p.name.split('_map')[0]}.md"
                 for p in RADICE.glob("**/rendered-texture/*_map[0-9][0-9]_*.svg")})
master = [m for m in master if m.exists()]
celle = collections.Counter()
mappe = collections.Counter()
n_mappe = 0
for m in master:
    for g in r.extract_maps(m.read_text(encoding="utf-8")):
        n_mappe += 1
        visti = set()
        for riga in g["rows"].values():
            for e in riga:
                s = r.SYMBOLS.get(e)
                if s and s.get("prop"):
                    celle[e] += 1
                    visti.add(e)
        for e in visti:
            mappe[e] += 1
oggetti = [e for e, s in r.SYMBOLS.items() if s.get("prop")]
out = {"master": len(master), "mappe": n_mappe, "simboli_oggetto": len(oggetti),
       "usati": len(celle),
       "per_simbolo": [{"simbolo": e, "prop": r.SYMBOLS[e]["prop"], "celle": celle[e],
                        "mappe": mappe[e]} for e in sorted(oggetti, key=lambda e: -celle[e])]}
if "--json" in sys.argv:
    print(json.dumps(out, ensure_ascii=False, indent=1))
else:
    print(f"{out['master']} master, {out['mappe']} mappe; {out['usati']} simboli-oggetto usati su {out['simboli_oggetto']}")
    for v in out["per_simbolo"]:
        print(f"{v['simbolo']}\t{v['prop']}\t{v['celle']}\t{v['mappe']}")
