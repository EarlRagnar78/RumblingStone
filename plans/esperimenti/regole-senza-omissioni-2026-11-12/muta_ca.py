#!/usr/bin/env python3
"""Banco del lotto 1-bis (ADR-0126): errori messi apposta nella CA delle schede del Bestiario.

Per ogni scheda che `verifica_scheda` giudica senza violazioni di CA si scrive
una copia con un solo errore e si conta se la verifica lo vede:

* `ca +1`, `ca -2`: la CA scritta non è più la somma delle voci;
* `voce +1`: il primo bonus di armatura o di scudo sale di uno, e la CA con lui
  (la somma torna, la tabella no);
* `contatto +1`, `sprovvista +1`: dove la scheda li scrive;
* `sensi`: la scurovisione tolta a chi la ha per razza.

Uso: python3 muta_ca.py  (scrive misure-ca.json accanto)
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402


def _viol(testo: str, nome: str, regole: tuple) -> bool:
    with tempfile.TemporaryDirectory(dir=ROOT / "Bestiario") as d:
        p = Path(d) / nome
        p.write_text(testo, encoding="utf-8")
        v, _ = V.classe_armatura(p)
    return any(x["regola"].startswith(regole) for x in v)


def mutazioni(testo: str):
    m = re.search(r"^ca: (\d+)$", testo, re.M)
    if not m:
        return
    ca = int(m.group(1))
    yield "ca +1", testo[:m.start()] + f"ca: {ca + 1}" + testo[m.end():], ("numero.CA",)
    yield "ca -2", testo[:m.start()] + f"ca: {ca - 2}" + testo[m.end():], ("numero.CA",)
    d = re.search(r"^ca-dettaglio: .*$", testo, re.M)
    if d:
        riga = d.group(0)
        v = re.search(r"\+(\d+)(?=(?: \+\d+)? (?:MW |mw |mithral )?(?:full plate|breastplate|chain shirt|hide|"
                      r"armatura completa|giaco di maglia|cotta di maglia|corazza di piastre|cuoio borchiato|"
                      r"banded mail|half-plate|heavy shield|light shield|scudo pesante|scudo leggero))", riga)
        if v:
            nuova = riga[:v.start()] + f"+{int(v.group(1)) + 1}" + riga[v.end():]
            t = testo.replace(riga, nuova, 1)
            t = re.sub(r"^ca: \d+$", f"ca: {ca + 1}", t, count=1, flags=re.M)
            yield "voce +1", t, ("numero.CA",)
        for nome, schema in (("contatto +1", r"(contatto|touch) (\d+)"),
                             ("sprovvista +1", r"(sprovvista|flat-footed) (\d+)")):
            c = re.search(schema, riga)
            if c:
                nuova = riga[:c.start(2)] + str(int(c.group(2)) + 1) + riga[c.end(2):]
                yield nome, testo.replace(riga, nuova, 1), ("numero.CA",)
    s = re.search(r"^sensi: .*scurovisione.*\n", testo, re.M)
    if s:
        yield "sensi", testo[:s.start()] + testo[s.end():], ("numero.sensi",)


def main() -> int:
    conto: dict = {}
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        testo = p.read_text(encoding="utf-8")
        v, nv = V.classe_armatura(p)
        if v:
            continue
        ca_verificabile = not any(x["regola"] == "numero.CA" for x in nv)
        for nome, mutato, regole in mutazioni(testo):
            if nome != "sensi" and not ca_verificabile:
                continue
            c = conto.setdefault(nome, {"mutanti": 0, "trovati": 0, "persi": []})
            c["mutanti"] += 1
            if _viol(mutato, p.name, regole):
                c["trovati"] += 1
            else:
                c["persi"].append(p.name)
    tot_m = sum(c["mutanti"] for c in conto.values())
    tot_t = sum(c["trovati"] for c in conto.values())
    for nome, c in conto.items():
        print(f"{nome:14} {c['trovati']:3}/{c['mutanti']:3}")
    print(f"totale {tot_t}/{tot_m}")
    (Path(__file__).parent / "misure-ca.json").write_text(
        json.dumps(conto, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
