#!/usr/bin/env python3
"""banco_formule.py — indagine I1 di PIANO-MOTORE-AGNOSTICO-D20: quale linguaggio per le formule.

Mette alla prova ogni motore di espressioni installato su cinque criteri:

    (a) correttezza  ogni formula d20 di oggi, scritta come espressione, dà lo
                     stesso numero della funzione Python che sostituirebbe, su
                     TUTTO il dominio (punteggi 0-60, DV e livelli 0-40, ...)
    (b) sicurezza    50 espressioni ostili (import, attributi magici, cicli,
                     numeri enormi, chiamate libere): ognuna deve essere
                     RIFIUTATA (eccezione) entro 2 s e 256 MiB, in un processo
                     a parte con limiti del sistema operativo
    (c) determinismo stesso risultato in 100 valutazioni ripetute
    (d) impacchettabile  puro Python, dipendenze, licenza (dai metadati
                     installati): si può portare dentro la skill come fa
                     iemod-fetch, senza pip né librerie compilate?
    (e) costo        microsecondi per valutazione (mediana di 2.000)

Motori: `ast` della libreria standard (valutatore a lista bianca scritto qui,
il controllo), simpleeval, asteval, cel-python (CEL puro Python),
common-expression-language (CEL in Rust). Quelli non installati sono saltati
e il rapporto lo dice.

Per CEL le formule hanno un dialetto suo: CEL non ha `//` (la divisione
intera tronca verso zero) né `max`. Il banco usa la traduzione più fedele che
CEL permette e conta quante formule hanno dovuto cambiare forma.

    python3 banco_formule.py                      # tabella
    python3 banco_formule.py --json RISULTATI.json

Deterministico: domini e casi fissi, nessun seme.
"""
from __future__ import annotations

import argparse
import ast
import importlib.metadata as md
import json
import operator
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path

QUI = Path(__file__).resolve().parent

# ---------------------------------------------------------------- le formule
# nome: (espressione Python-like, espressione CEL, funzione di riferimento, dominio)
# I riferimenti copiano le funzioni di scripts/dmcore (tabelle, caratteristiche,
# progressione) al commit e06c2cf; il test d'accompagnamento lo verifica.

def _rif_mod(punteggio): return (punteggio - 10) // 2
def _rif_ts_buono(dv): return 2 + dv // 2
def _rif_ts_cattivo(dv): return dv // 3
def _rif_cd(livello, modificatore): return 10 + livello + modificatore
def _rif_da_mod(m): return max(1, 10 + 2 * m)
def _rif_liv_ridotto(livello): return max(0, livello - 3)
def _rif_bab(n, num, den):
    import math
    return math.floor(n * (num / den))


def _griglia(**assi):
    chiavi = list(assi)
    out = [{}]
    for k in chiavi:
        out = [dict(d, **{k: v}) for d in out for v in assi[k]]
    return out


FORMULE = {
    "mod": ("(punteggio - 10) // 2",
            "punteggio >= 10 ? (punteggio - 10) / 2 : -((11 - punteggio) / 2)",
            _rif_mod, _griglia(punteggio=range(0, 61))),
    "ts_buono": ("2 + dv // 2", "2 + dv / 2", _rif_ts_buono, _griglia(dv=range(0, 41))),
    "ts_cattivo": ("dv // 3", "dv / 3", _rif_ts_cattivo, _griglia(dv=range(0, 41))),
    "cd_incantesimo": ("10 + livello + modificatore", "10 + livello + modificatore",
                       _rif_cd, _griglia(livello=range(0, 10), modificatore=range(-5, 21))),
    "da_modificatore": ("max(1, 10 + 2 * m)", "10 + 2 * m > 1 ? 10 + 2 * m : 1",
                        _rif_da_mod, _griglia(m=range(-10, 21))),
    "livello_incantatore_ridotto": ("max(0, livello - 3)", "livello - 3 > 0 ? livello - 3 : 0",
                                    _rif_liv_ridotto, _griglia(livello=range(0, 41))),
    "bab_gruppo": ("n * num // den", "n * num / den", _rif_bab,
                   [dict(d, num=num, den=den) for d in _griglia(n=range(0, 41))
                    for num, den in ((1, 1), (3, 4), (1, 2))]),
}

# ------------------------------------------------------------- le ostili
OSTILI = [
    "__import__('os').system('true')", "().__class__", "().__class__.__bases__[0].__subclasses__()",
    "dv.__class__", "dv.__add__(1)", "open('/etc/passwd')", "exec('1')", "eval('1')",
    "globals()", "locals()", "vars()", "getattr(dv, 'real')", "type(dv)", "dir()",
    "compile('1','x','eval')", "lambda: 1", "(lambda x: x)(1)", "[i for i in range(10)]",
    "{i: i for i in range(3)}", "{i for i in range(3)}", "(i for i in range(3))",
    "10 ** 10 ** 10", "9 ** 9 ** 9", "2 ** 100000000", "'a' * 10 ** 10", "[0] * 10 ** 10",
    "range(10 ** 12)", "list(range(10 ** 9))", "max(*[1] * 10 ** 8)", "sum(range(10 ** 12))",
    "import os", "from os import system", "while True: pass", "for i in range(10**12): pass",
    "def f(): pass", "class A: pass", "x = 1", "del dv", "f'{dv}'", "'%s' % dv",
    "(x := 1)", "print(1)", "input()", "breakpoint()", "__builtins__",
    "dv.real", "dv[0]", "sorted", "help()", "quit()",
]
assert len(OSTILI) == 50

# ------------------------------------------------------------- i motori

_OP = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod}
_FUNZ = {"max": max, "min": min}


class ValutatoreAst:
    """Il controllo: aritmetica intera su nomi noti, max/min, niente altro."""
    nome = "ast (stdlib, lista bianca)"
    distribuzione = None

    def valuta(self, espr: str, nomi: dict):
        return self._e(ast.parse(espr, mode="eval").body, nomi)

    def _e(self, n, nomi):
        if isinstance(n, ast.Constant) and type(n.value) is int and abs(n.value) < 10 ** 6:
            return n.value
        if isinstance(n, ast.Name) and n.id in nomi:
            return nomi[n.id]
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -self._e(n.operand, nomi)
        if isinstance(n, ast.BinOp) and type(n.op) in _OP:
            return _OP[type(n.op)](self._e(n.left, nomi), self._e(n.right, nomi))
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in _FUNZ
                and not n.keywords and all(not isinstance(a, ast.Starred) for a in n.args)):
            return _FUNZ[n.func.id](*(self._e(a, nomi) for a in n.args))
        raise ValueError(f"non ammesso: {ast.dump(n)[:60]}")


class Simpleeval:
    nome, distribuzione = "simpleeval", "simpleeval"

    def __init__(self):
        import simpleeval
        self.m = simpleeval

    def valuta(self, espr, nomi):
        return self.m.SimpleEval(names=nomi, functions={"max": max, "min": min}).eval(espr)


class SimpleevalRistretto:
    """simpleeval configurato con la sua API pubblica: solo nodi e operatori aritmetici, solo interi."""
    nome, distribuzione = "simpleeval ristretto (config)", "simpleeval"
    NODI = ("BinOp", "UnaryOp", "Constant", "Name", "Call", "Expr", "IfExp", "Compare")
    OPERATORI = ("Add", "Sub", "Mult", "FloorDiv", "Mod", "USub", "Gt", "GtE", "Lt", "LtE", "Eq", "NotEq")

    def __init__(self):
        import simpleeval
        self.m = simpleeval

    def valuta(self, espr, nomi):
        s = self.m.SimpleEval(names=nomi, functions={"max": max, "min": min})
        s.nodes = {k: v for k, v in s.nodes.items() if k.__name__ in self.NODI}
        s.operators = {k: v for k, v in s.operators.items() if k.__name__ in self.OPERATORI}
        r = s.eval(espr)
        if type(r) is not int:
            raise TypeError(f"risultato non intero: {type(r).__name__}")
        return r


class Asteval:
    nome, distribuzione = "asteval", "asteval"

    def __init__(self):
        import asteval
        self.m = asteval

    def valuta(self, espr, nomi):
        a = self.m.Interpreter(minimal=True, use_numpy=False, with_import=False,
                               with_importfrom=False, raise_errors=True)
        a.symtable.update(nomi)
        return a.eval(espr, show_errors=False, raise_errors=True)


class CelPython:
    nome, distribuzione, cel = "cel-python (CEL)", "cel-python", True

    def __init__(self):
        import celpy
        self.m = celpy

    def valuta(self, espr, nomi):
        env = self.m.Environment()
        prg = env.program(env.compile(espr))
        out = prg.evaluate({k: self.m.celtypes.IntType(v) for k, v in nomi.items()})
        if isinstance(out, Exception):
            raise out
        return int(out)


class CelRust:
    nome, distribuzione, cel = "common-expression-language (CEL, Rust)", "common-expression-language", True

    def __init__(self):
        import cel
        self.m = cel

    def valuta(self, espr, nomi):
        return int(self.m.evaluate(espr, nomi))


MOTORI = {"ast": ValutatoreAst, "simpleeval": Simpleeval, "simpleeval-ristretto": SimpleevalRistretto,
          "asteval": Asteval,
          "cel-python": CelPython, "cel-rust": CelRust}


def _crea(chiave):
    try:
        return MOTORI[chiave]()
    except ImportError:
        return None


# ------------------------------------------------------------- le prove

def correttezza(m):
    esiti, cambiate = {}, 0
    for nome, (py, cel, rif, dominio) in FORMULE.items():
        espr = cel if getattr(m, "cel", False) else py
        cambiate += espr != py
        errati = []
        for nomi in dominio:
            atteso = rif(**nomi)
            try:
                avuto = m.valuta(espr, dict(nomi))
            except Exception as e:  # noqa: BLE001
                avuto = f"errore {type(e).__name__}"
            if avuto != atteso:
                errati.append({"valori": nomi, "atteso": atteso, "avuto": avuto})
        esiti[nome] = {"casi": len(dominio), "errati": len(errati), "primi_errati": errati[:3]}
    return esiti, cambiate


def cel_ingenuo(m):
    """La traduzione letterale (// → /, come farebbe chi scrive la regola): quanti casi sbaglia."""
    py, _cel, rif, dominio = FORMULE["mod"]
    espr = py.replace("//", "/")
    return sum(1 for nomi in dominio if m.valuta(espr, dict(nomi)) != rif(**nomi))


def _uno_ostile(chiave, i):
    """Nel processo figlio: valuta l'ostile i, stampa ACCETTATA o RIFIUTATA."""
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (256 * 2 ** 20, 256 * 2 ** 20))
    m = _crea(chiave)
    try:
        r = m.valuta(OSTILI[i], {"dv": 3})
        print("ACCETTATA", repr(r)[:40])
    except BaseException as e:  # noqa: BLE001
        print("RIFIUTATA", type(e).__name__)


def sicurezza(chiave):
    accettate = []
    for i, e in enumerate(OSTILI):
        try:
            out = subprocess.run([sys.executable, __file__, "--uno", chiave, str(i)],
                                 capture_output=True, text=True, timeout=2).stdout.strip()
        except subprocess.TimeoutExpired:
            out = "TEMPO SCADUTO"
        if not out.startswith("RIFIUTATA"):
            accettate.append({"espressione": e, "esito": out or "processo morto"})
    return accettate


def determinismo(m):
    py, cel, rif, dominio = FORMULE["mod"]
    espr = cel if getattr(m, "cel", False) else py
    valori = {m.valuta(espr, {"punteggio": 7}) for _ in range(100)}
    return len(valori) == 1


def costo_us(m):
    py, cel, *_ = FORMULE["ts_buono"]
    espr = cel if getattr(m, "cel", False) else py
    tempi = []
    for _ in range(2000):
        t = time.perf_counter_ns()
        m.valuta(espr, {"dv": 13})
        tempi.append(time.perf_counter_ns() - t)
    return round(statistics.median(tempi) / 1000, 1)


def impacchettabile(m):
    if m.distribuzione is None:
        return {"puro_python": True, "dipendenze": [], "licenza": "PSF (libreria standard)", "versione": sys.version.split()[0]}
    d = md.distribution(m.distribuzione)
    file = [str(f) for f in (d.files or [])]
    compilati = [f for f in file if f.endswith((".so", ".pyd", ".dylib"))]
    lic = d.metadata.get("License-Expression") or d.metadata.get("License") or ""
    if not lic:
        lic = "; ".join(c.split("::")[-1].strip() for c in d.metadata.get_all("Classifier") or [] if "License" in c)
    dip = [r.split(";")[0].strip() for r in (d.requires or []) if "extra ==" not in r]
    return {"puro_python": not compilati, "dipendenze": dip, "licenza": lic, "versione": d.version}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    ap.add_argument("--uno", nargs=2)
    a = ap.parse_args(argv)
    if a.uno:
        _uno_ostile(a.uno[0], int(a.uno[1]))
        return 0
    ris = {"python": sys.version.split()[0], "motori": {}}
    for chiave in MOTORI:
        m = _crea(chiave)
        if m is None:
            ris["motori"][chiave] = {"installato": False}
            continue
        corr, cambiate = correttezza(m)
        acc = sicurezza(chiave)
        ris["motori"][chiave] = {
            "nome": m.nome, "installato": True,
            "formule_corrette": sum(1 for v in corr.values() if v["errati"] == 0),
            "formule": len(FORMULE), "formule_riscritte_per_il_dialetto": cambiate,
            "casi_errati": sum(v["errati"] for v in corr.values()), "correttezza": corr,
            "ostili_accettate": len(acc), "ostili": len(OSTILI), "dettaglio_ostili": acc,
            "deterministico": determinismo(m), "us_per_valutazione": costo_us(m),
            "impacchettabile": impacchettabile(m),
        }
        if getattr(m, "cel", False):
            ris["motori"][chiave]["mod_tradotto_alla_lettera_casi_errati"] = cel_ingenuo(m)
    if a.json:
        Path(a.json).write_text(json.dumps(ris, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{'motore':42} {'formule ok':>10} {'riscritte':>9} {'ostili passate':>14} {'det.':>5} {'µs':>7}  pacchetto")
    for k, v in ris["motori"].items():
        if not v["installato"]:
            print(f"{k:42} non installato")
            continue
        p = v["impacchettabile"]
        pac = ("puro Python" if p["puro_python"] else "COMPILATO") + f", {len(p['dipendenze'])} dip., {p['licenza']}"
        print(f"{v['nome']:42} {v['formule_corrette']:>4}/{v['formule']:<5} {v['formule_riscritte_per_il_dialetto']:>9} "
              f"{v['ostili_accettate']:>8}/{v['ostili']:<5} {'sì' if v['deterministico'] else 'NO':>5} {v['us_per_valutazione']:>7}  {pac}")
    return 0


if __name__ == "__main__":
    os.environ.setdefault("PYTHONHASHSEED", "0")
    sys.exit(main())
