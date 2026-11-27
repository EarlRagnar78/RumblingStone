#!/usr/bin/env python3
"""Banco del lotto 3 (ADR-0126): errori messi apposta negli incantesimi.

Per ogni lista di incantesimi che `verifica_scheda` sa leggere (classe, livello
e caratteristica), si scrive una copia della scheda con un solo errore:

* `cd +1`, `cd -1`: una CD scritta nella lista cambia di uno;
* `slot +1`, `slot -1`: un numero di «N/N+1/… al giorno» o della parentesi
  «(5+1)» di una riga cambia di uno;
* `uno in più`: la riga prende un incantesimo in più;
* `livello`: la riga più alta della lista sale di due livelli.

Una copia conta come trovata se compare una violazione che prima non c'era
(riga, regola, valore scritto). Le liste di cui non si legge classe, livello o
caratteristica restano nel conto, in una colonna a parte.

Uso: python3 muta_magia.py  (scrive misure-magia.json accanto)
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
from dmcore import magia as M  # noqa: E402


def _esito(testo: str, p: Path) -> "tuple[set, int]":
    with tempfile.TemporaryDirectory(dir=p.parent) as d:
        q = Path(d) / p.name
        q.write_text(testo, encoding="utf-8")
        v, n = V.incantatori(q)
    return {(x["riga"], x["regola"], str(x["ha"])) for x in v}, len(n)


def mutazioni(testo: str, p: Path):
    righe = testo.split("\n")
    sis = V.VT.sistema_di(p, testo)

    def con(i: int, nuova: str) -> str:
        return "\n".join(righe[:i] + [nuova] + righe[i + 1:])

    teste: dict[int, list[int]] = {}
    for i, r in enumerate(righe):
        m = M.RIGA.match(r)
        if not m or "*" not in m.group("resto") or re.match(r"\d", m.group("resto")):
            continue
        t = V._testa_della_lista(righe, i)
        if t is None:
            continue
        teste.setdefault(t, []).append(i)
        for k in re.finditer(r"\b(CD|DC) (\d+)", r):
            for nome, d in (("cd +1", 1), ("cd -1", -1)):
                yield nome, con(i, r[:k.start(2)] + str(int(k.group(2)) + d) + r[k.end(2):])
        if re.fullmatch(r"\s*\d+\s*(?:\+\s*(?:\d+|D))?\s*", m.group("par") or ""):
            a, b = m.span("par")
            n = re.match(r"\s*(\d+)", r[a:b])
            for nome, d in (("slot +1", 1), ("slot -1", -1)):
                yield nome, con(i, r[:a] + str(int(n.group(1)) + d) + r[a + n.end():])
        yield "uno in più", con(i, r.rstrip() + ", *incantesimo in più*")
    for t, lista in teste.items():
        k = M._AL_GIORNO.search(righe[t])
        if k:
            for n in re.finditer(r"(?<![+\d])\d+", k.group(1)):
                a = k.start(1) + n.start()
                for nome, d in (("slot +1", 1), ("slot -1", -1)):
                    if int(n.group(0)) + d >= 0:
                        yield nome, con(t, righe[t][:a] + str(int(n.group(0)) + d) + righe[t][a + len(n.group(0)):])
        alta = max(lista, key=lambda i: int(M.RIGA.match(righe[i]).group("liv")))
        m = M.RIGA.match(righe[alta])
        liv = int(m.group("liv"))
        if liv + 2 <= 9 and V._classe_che_lancia(righe, alta, sis) not in (None,):
            yield "livello", con(alta, righe[alta][:m.start("liv")] + str(liv + 2) + righe[alta][m.end("liv"):])


def main() -> int:
    conto: dict = {}
    radici = [ROOT / "Bestiario"] + sorted(ROOT.glob("0*"))
    for p in sorted(q for r in radici for q in r.rglob("*.md")):
        testo = p.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"incantesimi|spells", testo, re.I):
            continue
        base, _ = _esito(testo, p)
        for nome, mutato in mutazioni(testo, p):
            dopo, _ = _esito(mutato, p)
            c = conto.setdefault(nome, {"mutanti": 0, "trovati": 0, "lista_non_letta": 0, "persi": []})
            c["mutanti"] += 1
            if dopo - base:
                c["trovati"] += 1
            elif not _giudicata(testo, mutato, p):
                c["lista_non_letta"] += 1     # classe, livello o caratteristica non si leggono
            else:
                c["persi"].append(p.name)
    for nome, c in sorted(conto.items()):
        print(f"{nome:12} {c['trovati']:3}/{c['mutanti']:3}  lista non letta {c['lista_non_letta']:3}  persi {len(c['persi']):3}")
    tot = {k: sum(c[k] if k != "persi" else len(c[k]) for c in conto.values())
           for k in ("trovati", "mutanti", "lista_non_letta", "persi")}
    print("totale", tot)
    (Path(__file__).parent / "misure-magia.json").write_text(
        json.dumps({"campi": conto, "totale": tot}, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8")
    return 0


def _giudicata(testo: str, mutato: str, p: Path) -> bool:
    """La riga cambiata sta in una lista che il verificatore giudica?"""
    a, b = testo.split("\n"), mutato.split("\n")
    i = next(k for k in range(len(a)) if a[k] != b[k])
    t = i if not M.RIGA.match(a[i]) else V._testa_della_lista(a, i)
    return t is not None and t in _lette(testo, p)


_CACHE: dict = {}


def _lette(testo: str, p: Path) -> set:
    """Le intestazioni delle liste che il verificatore giudica (non finite fra i non verificabili)."""
    if p not in _CACHE:
        with tempfile.TemporaryDirectory(dir=p.parent) as d:
            q = Path(d) / p.name
            q.write_text(testo, encoding="utf-8")
            _, n = V.incantatori(q)
        fuori = {x["riga"] - 1 for x in n if x["regola"] == "numero.incantesimi"}
        righe = testo.split("\n")
        tutte = {V._testa_della_lista(righe, i) for i, r in enumerate(righe)
                 if M.RIGA.match(r) and "*" in M.RIGA.match(r).group("resto")}
        _CACHE[p] = {t for t in tutte if t is not None} - fuori
    return _CACHE[p]


if __name__ == "__main__":
    sys.exit(main())
