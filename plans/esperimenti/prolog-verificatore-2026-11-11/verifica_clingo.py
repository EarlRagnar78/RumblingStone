#!/usr/bin/env python3
"""verifica_clingo.py — le stesse regole in ASP (clingo, Potassco, MIT), dentro Python.

clingo esiste come ruota PyPI per Python 3.13 (manylinux), quindi si porta nel
pacchetto come le altre librerie (regola del 2026-11-08); SWI-Prolog no, è un
binario di sistema. Stessi fatti di verifica_prolog.py, stessa uscita.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import clingo

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))
import verifica_prolog as VP  # noqa: E402

REGOLE = r"""
car_di(F,C,V) :- scheda(F,_), car(F,C,V).
car_di(F,C,10) :- scheda(F,_), req_car(_,_,C,_), not car(F,C,_).
liv_di(F,C,N) :- livello(F,C,N).
liv_di(F,"character",N) :- dv(F,N).
classe_nota(F,C) :- liv_di(F,C,_).

violazione(F,T,car(C),A,H) :- ha(F,T), scheda(F,S), req_car(S,T,C,A), car_di(F,C,H), H < A.
violazione(F,T,bab,A,H)    :- ha(F,T), scheda(F,S), req_bab(S,T,A), bab(F,H), H < A.
violazione(F,T,lic,A,H)    :- ha(F,T), scheda(F,S), req_lic(S,T,A), lic(F,H), H < A.
violazione(F,T,classe(C),A,H) :- ha(F,T), scheda(F,S), req_classe(S,T,C,A), liv_di(F,C,H), H < A.
violazione(F,T,classe(C),A,0) :- ha(F,T), scheda(F,S), req_classe(S,T,C,A), not classe_nota(F,C).
violazione(F,T,talento,P,assente) :- ha(F,T), scheda(F,S), req_talento(S,T,P), not ha(F,P).
cap_ok(F,Cap) :- scheda(F,S), cap_da(S,Cap,C,L), liv_di(F,C,N), N >= L.
violazione(F,T,capacita,Cap,assente) :- ha(F,T), scheda(F,S), req_cap(S,T,Cap), not cap_ok(F,Cap).
#show violazione/5.
"""


def verifica(schede: list[dict]) -> list[dict]:
    ctl = clingo.Control(["--warn=none"])
    fatti = VP.fatti_dati({s["sistema"] for s in schede}) + VP.fatti_schede(schede)
    # in ASP le costanti fra apici sono stringhe: "…"
    testo = "\n".join(f.replace("\\'", "’") for f in fatti)
    testo = testo.replace("'", '"')
    ctl.add("base", [], testo + REGOLE)
    ctl.ground([("base", [])])
    out = []
    with ctl.solve(yield_=True) as h:
        for m in h:
            for a in m.symbols(shown=True):
                f, t, r, att, ha = a.arguments
                s = lambda x: x.string if x.type == clingo.SymbolType.String else str(x)  # noqa: E731
                out.append({"file": s(f), "talento": s(t), "regola": str(r).replace('"', "'"),
                            "atteso": s(att), "ha": s(ha)})
    return out


if __name__ == "__main__":
    schede = json.load(open(sys.argv[1], encoding="utf-8"))
    t0 = time.perf_counter()
    v = verifica(schede)
    ms = (time.perf_counter() - t0) * 1000
    json.dump({"motore": "clingo", "ms": round(ms, 1), "violazioni": v},
              sys.stdout, ensure_ascii=False, indent=1)
