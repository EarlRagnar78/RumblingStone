#!/usr/bin/env python3
"""Banco del lotto 3-bis (ADR-0126): requisiti di una classe di prestigio tolti apposta.

Le schede del Bestiario con una classe di prestigio sono poche. A ognuna si
toglie un requisito per volta, in una copia:

* `allineamento`: la sigla diventa una che la classe non ammette;
* `razza`: la razza fra parentesi diventa «orc»;
* `talento`: un talento richiesto sparisce da tutte le righe che lo scrivono;
* `abilità`: un'abilità richiesta sparisce dalle righe delle abilità;
* `livelli`: i livelli passano dalle altre classi alla classe di prestigio,
  finché prima dell'ingresso ne resta uno solo.

Una copia conta come trovata se compare una violazione `prestigio.*` che prima
non c'era. Le schede che hanno già una violazione restano nel conto.
Il giudizio su tutte le classi dei dati (ogni requisito tolto si vede) sta in
`scripts/tests/test_prestigio.py`: qui si misura la lettura delle schede vere.

Uso: python3 muta_prestigio.py  (scrive misure-prestigio.json accanto)
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import lessico_regole as LR  # noqa: E402
import verifica_scheda as V  # noqa: E402
from dmcore import prestigio as PR  # noqa: E402

ALLINEAMENTI = ["LG", "NG", "CG", "LN", "N", "CN", "LE", "NE", "CE"]


def _esito(testo: str, p: Path) -> set:
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / p.name
        q.write_text(testo, encoding="utf-8")
        v, _ = V.prestigio(q)
    return {(x["regola"], str(x["ha"]), str(x["atteso"])) for x in v}


def mutazioni(testo: str, p: Path):
    s = V.L.leggi(p)
    f = V.VT.leggi(p) or {}
    sistema = V.VT.sistema_di(p, testo)
    livelli = dict(f.get("livelli") or V.L.livelli_di_classe(s))
    for nome, n in livelli.items():
        en = V._prestigio_en(nome, sistema)
        if en is None:
            continue
        req = PR.classe(en, sistema)
        sigla = (f.get("fisici") or {}).get("allineamento")
        if "allineamento" in req and sigla and len(req["allineamento"]) < 9:
            altra = next(a for a in ALLINEAMENTI if a not in req["allineamento"])
            scritta = f"(?:{sigla}|{sigla.translate(str.maketrans('GE', 'BM'))})"       # «NM» è NE
            yield "allineamento", re.sub(rf"(?m)^((?:tipo|\*\*Tipo\*\*):.*?)\b{scritta}\b\s*$", rf"\g<1>{altra}", testo)
        if "razza" in req:
            yield "razza", re.sub(r"(?mi)^(tipo:[^(\n]*\()[^)]*\)", r"\1orc)", testo)
        for gruppo in req.get("talenti", ()):
            for t in gruppo["fra"] if gruppo["quanti"] == len(gruppo["fra"]) else ():
                nuovo, tolti = testo, 0
                for pezzo in {x for r in testo.splitlines() if re.search(r"Talenti|Feats", r)
                              for x in re.split(r"[,·;]|\*\*|:", r)}:
                    pulito = re.sub(r"\s*[\[(].*$", "", pezzo).strip()
                    r = V.VT.risolvi(sistema, pulito) if pulito else None
                    if r and PR.senza_parentesi(r["en"]) == PR.senza_parentesi(t):
                        nuovo = re.sub(rf"{re.escape(pulito)}(?! (?:potenziat|superior|migliorat))", "Correre", nuovo)
                        tolti += 1
                if tolti:
                    yield "talento", nuovo
        for gruppo in req.get("abilita", ()):
            for a in gruppo["fra"] if gruppo["quanti"] == len(gruppo["fra"]) else ():
                nuovo = testo
                for nome_it, _, bonus in {x for r in testo.splitlines() if (m := V.RIGA_ABILITA.search(r))
                                          for x in V.VOCE_ABILITA.findall(re.sub(r"[*_`]", "", m.group(1)))}:
                    k = V._abilita_it().get(LR.norma(nome_it.strip()), nome_it.strip().lower())
                    if k == PR.senza_parentesi(a):
                        nuovo = re.sub(rf"{re.escape(nome_it.strip())}(\s*\([^)]*\))?\s*{re.escape(bonus)},?\s*", "", nuovo)
                if nuovo != testo:
                    yield "abilità", nuovo
        altre = [(c, v) for c, v in V.L.livelli_di_classe(s).items() if c != nome.lower() and v > 1]
        if altre and ({"bab", "abilita", "incantesimi"} & set(req)):
            nuovo, presi = testo, 0
            for c, v in altre:
                nuovo = re.sub(rf"(?i)\b({re.escape(c)}) {v}\b", r"\1 1", nuovo)
                presi += v - 1
            nuovo = re.sub(rf"(?i)\b({re.escape(nome)}) {n}\b", rf"\1 {n + presi}", nuovo)
            yield "livelli", nuovo


def main() -> int:
    esiti: dict[str, list[int]] = {}
    schede, gia, perse = 0, 0, []
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        testo = p.read_text(encoding="utf-8")
        s = V.L.leggi(p)
        if s is None:
            continue
        prima = None
        for nome, mutata in mutazioni(testo, p):
            if prima is None:
                prima = _esito(testo, p)
                schede += 1
                gia += bool(prima)
            e = esiti.setdefault(nome, [0, 0])
            e[1] += 1
            if mutata != testo and _esito(mutata, p) - prima:
                e[0] += 1
            else:
                perse.append(f"{p.name}: {nome}" + (" (la copia è uguale)" if mutata == testo else ""))
    tot = [sum(e[0] for e in esiti.values()), sum(e[1] for e in esiti.values())]
    fuori = {"schede_con_classe_di_prestigio": schede, "gia_in_violazione": gia,
             "per_mutazione": {k: f"{a}/{b}" for k, (a, b) in sorted(esiti.items())},
             "trovate": f"{tot[0]}/{tot[1]}", "perse": perse}
    (Path(__file__).parent / "misure-prestigio.json").write_text(
        json.dumps(fuori, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(fuori, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
