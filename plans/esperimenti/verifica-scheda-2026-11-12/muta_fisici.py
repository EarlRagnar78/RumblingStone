#!/usr/bin/env python3
"""muta_fisici.py — quanti prerequisiti fisici rotti apposta vede `verifica_talenti`.

Per ogni scheda del Bestiario con un talento che chiede volo, taglia o attacchi
naturali (e che oggi li ha), si toglie il fatto dalla scheda in una copia:
via la velocità di volo, taglia portata a Small, attacchi naturali ridotti al
solo primo. Si conta quante volte la verifica se ne accorge.

Uso: python3 muta_fisici.py   (stampa la tabella e scrive misure-fisici.json)
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_talenti as VT  # noqa: E402

MUTAZIONI = {
    "volo tolto": (r"fly speed", lambda t: re.sub(r",?\s*\b(?:volare|volo|fly)\s+\d+(?:[.,]\d+)?\s*(?:m|ft)\b(?:\s*\([^)]*\))?", "", t, flags=re.I)),
    "taglia Small": (r"or larger", lambda t: re.sub(r"\b(Large|Huge|Gargantuan|Colossal|Grande|Enorme|Mastodontic[oa]|Colossale)\b", "Small", t)),
    # tutti gli attacchi naturali diventano armi, tranne il morso
    "attacchi naturali diventati armi": (r"natural (?:attacks|weapons)", lambda t: re.sub(
        r"\b(?:\d\s+)?(?:artigli\w*|coda|ali|schiant\w+|claws?|tail(?: slap)?|wings?|slams?)(\s*[+-]\d)", r"spada\1", t, flags=re.I)),
}


def main() -> int:
    conto = {k: [0, 0] for k in MUTAZIONI}
    with tempfile.TemporaryDirectory() as tmp:
        for p in sorted((ROOT / "Bestiario").rglob("*-cr*.md")):
            f = VT.leggi(p)
            if not f or VT.verifica(f)[0]:
                continue
            chiesti = {str(v["atteso"]).lower() for r in f["talenti"]
                       for v in VT.T.violazioni(r["sistema"], r["en"], VT.T.Stato(car=f["car"], bab=99, livelli=f["livelli"],
                                                                              lic=99, talenti=[], dv=f["dv"]))
                       if v["regola"] == "altro"}
            testo = p.read_text(encoding="utf-8")
            for nome, (chiave, muta) in MUTAZIONI.items():
                if not any(re.search(chiave, c) and VT.giudica_altro(c, f["fisici"]) == (True, VT.giudica_altro(c, f["fisici"])[1])
                           for c in chiesti if VT.giudica_altro(c, f["fisici"])):
                    continue
                nuovo = muta(testo)
                if nuovo == testo:
                    continue
                q = Path(tmp) / p.name
                q.write_text(nuovo, encoding="utf-8")
                g = VT.leggi(q)
                conto[nome][1] += 1
                conto[nome][0] += bool(g and any(v["regola"] == "fisico" for v in VT.verifica(g)[0]))
    for k, (visti, tot) in conto.items():
        print(f"{k:28} {visti:3}/{tot:3}")
    (Path(__file__).parent / "misure-fisici.json").write_text(json.dumps(conto, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
