#!/usr/bin/env python3
"""misura_prima_dopo.py — i 40 casi con la ricerca di prima e con il lessico.

Prima = la ricerca per titolo di ``riscontro_srd.py regola`` (com'era su main il
2026-11-07): un titolo Markdown o un grassetto uguale al nome, nell'SRD 3.5;
il nome della sezione, nel PRD PF1e. Dopo = ``lessico_regole.risolvi``.
Un caso è giusto se le due fonti danno esattamente il titolo atteso (o niente).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import lessico_regole as L  # noqa: E402
import riscontro_srd as R  # noqa: E402


def prima(nome: str, cache: Path) -> dict:
    out = {"srd35": None, "pf1": None}
    base = R.assicura(R.SRD35, cache, rete=False)
    titolo = re.compile(rf"^(?:#{{1,6}}\s*{re.escape(nome)}\s*$|\*\*{re.escape(nome)}:?\*\*:?)", re.I | re.M)
    for rel in sorted(R.SRD35.file):
        if titolo.search((base / rel).read_text(encoding="utf-8")):
            out["srd35"] = nome
            break
    base = R.assicura(R.PF1, cache, rete=False)
    for db in sorted(R.PF1.file):
        if R.sezioni_pf1(base / db, nome):
            out["pf1"] = nome
            break
    return out


def main() -> int:
    cache = R.cartella_cache(None)
    casi = json.loads((Path(__file__).parent / "casi.json").read_text(encoding="utf-8"))["casi"]
    idx, ita = L.carica_indice(cache, rete=False), L.mappa_italiana(L.carica_tabella())
    righe, conti = [], {"prima": 0, "dopo": 0}
    for c in casi:
        p = prima(c["termine"], cache)
        d = L.risolvi(c["termine"], idx, ita)
        ok = {k: all(L.norma(r[f] or "") == L.norma(c.get(f) or "") for f in ("srd35", "pf1"))
              for k, r in (("prima", p), ("dopo", d))}
        for k in conti:
            conti[k] += ok[k]
        righe.append((c["termine"], ok["prima"], ok["dopo"], c.get("perche", "")))
    for t, a, b, perche in righe:
        print(f"{'✓' if a else '✗'} {'✓' if b else '✗'}  {t}  {perche}")
    print(f"\nprima {conti['prima']}/{len(casi)} · dopo {conti['dopo']}/{len(casi)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
