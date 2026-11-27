"""dmcore.formule — le formule del sistema come dati (F3 di ADR-0112).

Una formula sta nei dati del plugin (`formule.regole`, oggi
`sistemi/d20/dati/formule.toml`) scritta come nel manuale, per esempio
`(punteggio - 10) // 2`, e si valuta qui con **simpleeval ristretto**: la
libreria è portata dentro il pacchetto (`dmcore/_vendor/`, versione e sha256 in
`LIBRERIE.toml`), e la lista bianca è quella misurata da I1 (7/7 formule su 598
casi, 50/50 espressioni ostili rifiutate).

    formula("modificatore")(punteggio=14)        → 2
    formula("ts_buono", "pf1e")(dv=6)            → 5   (pf1e eredita da d20)

Ogni formula dichiara i suoi `ingressi`: un nome in più, un nodo fuori lista o
un risultato non intero sono errori, e `problemi()` li trova in CI
(`sistemi.py --check`) invece che al tavolo. Solo libreria standard più il
file portato dentro.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from . import sistemi as _S
from ._vendor import simpleeval as _se

CAPACITA = "formule.regole"

#: I nodi e gli operatori ammessi (I1, «simpleeval ristretto»). Niente
#: attributi, indici, stringhe composte, assegnazioni, potenze, cicli.
NODI = frozenset({"Expression", "Expr", "BinOp", "UnaryOp", "Constant", "Name", "Load", "Call",
                  "IfExp", "Compare"})
OPERATORI = frozenset({"Add", "Sub", "Mult", "FloorDiv", "Mod", "USub", "UAdd",
                       "Gt", "GtE", "Lt", "LtE", "Eq", "NotEq"})
FUNZIONI = {"max": max, "min": min}


class ErroreFormula(ValueError):
    """Formula scritta male o chiamata con ingressi sbagliati."""


def controlla(espressione: str, ingressi: "tuple[str, ...]") -> "list[str]":
    """I difetti di una formula, senza valutarla: sintassi, nodi, nomi."""
    try:
        albero = ast.parse(espressione, mode="eval")
    except SyntaxError as e:
        return [f"sintassi: {e.msg}"]
    fuori = []
    for n in ast.walk(albero):
        tipo = type(n).__name__
        if tipo not in NODI and tipo not in OPERATORI:
            fuori.append(f"nodo non ammesso: {tipo}")
        elif isinstance(n, ast.Constant) and type(n.value) is not int:
            fuori.append(f"costante non intera: {n.value!r}")
        elif isinstance(n, ast.Call):
            if not (isinstance(n.func, ast.Name) and n.func.id in FUNZIONI) or n.keywords:
                fuori.append(f"chiamata non ammessa: {ast.unparse(n.func)}")
        elif isinstance(n, ast.Name) and n.id not in ingressi and n.id not in FUNZIONI:
            fuori.append(f"nome non dichiarato negli ingressi: {n.id}")
    return sorted(set(fuori))


@dataclass(frozen=True)
class Formula:
    nome: str
    espressione: str
    ingressi: "tuple[str, ...]"
    fonte: str = ""

    def __call__(self, **valori: int) -> int:
        if set(valori) != set(self.ingressi):
            raise ErroreFormula(f"{self.nome}: ingressi {sorted(valori)}, attesi {list(self.ingressi)}")
        for k, v in valori.items():
            if type(v) is not int:
                raise ErroreFormula(f"{self.nome}: {k} = {v!r} non è un intero")
        r = _valutatore(self.espressione, tuple(sorted(valori.items())))
        if type(r) is not int:
            raise ErroreFormula(f"{self.nome}: risultato non intero ({type(r).__name__})")
        return r


def _ristretto(nomi: dict) -> "_se.SimpleEval":
    s = _se.SimpleEval(names=nomi, functions=dict(FUNZIONI))
    s.nodes = {k: v for k, v in s.nodes.items() if k.__name__ in NODI}
    s.operators = {k: v for k, v in s.operators.items() if k.__name__ in OPERATORI}
    return s


@cache
def _analizzata(espressione: str):
    return _se.SimpleEval().parse(espressione)


def _valutatore(espressione: str, valori: "tuple[tuple[str, int], ...]") -> int:
    return _ristretto(dict(valori)).eval(espressione, previously_parsed=_analizzata(espressione))


@cache
def _formule(id_: str, root: Path) -> "dict[str, Formula]":
    d = _S.regole(id_, root).dati(CAPACITA).get("formule", {})
    fuori = {}
    for nome, v in d.items():
        f = Formula(nome, v["espressione"], tuple(v.get("ingressi", ())), v.get("fonte", ""))
        difetti = controlla(f.espressione, f.ingressi)
        if difetti:
            raise ErroreFormula(f"{id_}: formula «{nome}»: " + "; ".join(difetti))
        fuori[nome] = f
    return fuori


def formule(id_: str = "d20", root: "Path | None" = None) -> "dict[str, Formula]":
    """Tutte le formule del sistema `id_`, controllate."""
    return _formule(id_, (root or _S.ROOT).resolve())


def formula(nome: str, id_: str = "d20", root: "Path | None" = None) -> Formula:
    """La formula `nome` del sistema `id_`."""
    f = formule(id_, root)
    if nome not in f:
        raise ErroreFormula(f"{id_}: nessuna formula «{nome}» (ci sono: {', '.join(sorted(f))})")
    return f[nome]


def problemi(root: "Path | None" = None) -> "list[str]":
    """I difetti delle formule di ogni plugin che copre `formule.regole` coi dati."""
    r = (root or _S.ROOT).resolve()
    fuori = []
    for id_ in sorted(_S.carica(r)[2]):
        c = _S.capacita(id_, CAPACITA, r)
        if c.modo != "dati" or c.da != id_:
            continue
        for nome, v in _S.dati(id_, CAPACITA, r).get("formule", {}).items():
            if "espressione" not in v:
                fuori.append(f"{id_}: formula «{nome}» senza espressione")
                continue
            for d in controlla(v["espressione"], tuple(v.get("ingressi", ()))):
                fuori.append(f"{id_}: formula «{nome}»: {d}")
    return fuori
