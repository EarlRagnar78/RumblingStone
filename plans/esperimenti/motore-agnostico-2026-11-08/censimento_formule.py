#!/usr/bin/env python3
"""censimento_formule.py — quanto il motore sa ancora di un gioco (F0 di PIANO-MOTORE-AGNOSTICO-D20).

Conta, con l'AST di Python e non con espressioni regolari, cinque misure:

    A1  chiamate a `dati("<sistema>", …)` eseguite all'import di un modulo
        (fuori da ogni funzione): il motore che sceglie il gioco da solo
    A2  script (test esclusi) che importano i moduli del nucleo con regole
        (`dmcore.tabelle`, `incantesimi`, `progressione`, `caratteristiche`)
    A3  funzioni di `scripts/dmcore/` il cui corpo è un solo `return` di
        aritmetica pura (numeri, nomi, + − * // % e max/min/int/abs/round):
        le formule del sistema scritte in Python. È un elenco di candidate:
        la tabella `NON_FORMULE` qui sotto toglie, con il motivo, quelle che
        aritmetica sono ma regole di gioco no
    A4  capacità di un plugin attivo ancora dichiarate `codice`
    A5  strumenti che dipendono dal sistema e importano il nucleo senza mai
        chiamare `sistema_di` (quindi usano il predefinito anche su un file
        di un altro sistema)

    python3 plans/esperimenti/motore-agnostico-2026-11-08/censimento_formule.py          # tabella
    python3 plans/esperimenti/motore-agnostico-2026-11-08/censimento_formule.py --json F # dati
    python3 plans/esperimenti/motore-agnostico-2026-11-08/censimento_formule.py --check  # cricchetto

`--check` confronta con `CENSIMENTO.json` accanto ed esce 1 se una misura
sale. Quando una fase la fa scendere, si riscrive il file con `--json`.

Solo libreria standard; uscita deterministica (file in ordine, nessun seme).
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
QUI = Path(__file__).resolve().parent
RIFERIMENTO = QUI / "CENSIMENTO.json"

NUCLEO_CON_REGOLE = ("tabelle", "incantesimi", "progressione", "caratteristiche")
FUNZIONI_ARITMETICHE = {"max", "min", "int", "abs", "round"}

#: Funzioni aritmetiche che non sono regole del sistema, con il motivo.
NON_FORMULE: dict[str, str] = {
    "scripts/dmcore/tabelle.py:media_dado": "media di un dado (faccia+1)/2: matematica, non regola",
}


def _rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def _file_python() -> list[Path]:
    out = []
    for p in sorted(SCRIPTS.rglob("*.py")):
        parti = p.relative_to(SCRIPTS).parts
        if parti[0] in ("tests", "Old", "terzi") or "__pycache__" in parti:
            continue
        out.append(p)
    return out


def _albero(p: Path) -> ast.Module | None:
    try:
        return ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
    except (SyntaxError, UnicodeDecodeError):
        return None


def _nome_chiamata(c: ast.Call) -> str:
    f = c.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return ""


def a1_caricamenti_all_import(alberi: dict[str, ast.Module]) -> list[str]:
    """`dati("id", …)` con id letterale, in istruzioni di modulo (non in def/class)."""
    trovati = []
    for rel, t in alberi.items():
        for stmt in t.body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            for n in ast.walk(stmt):
                if (isinstance(n, ast.Call) and _nome_chiamata(n) == "dati" and n.args
                        and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str)):
                    trovati.append(f"{rel}:{n.lineno} «{n.args[0].value}»")
    return sorted(trovati)


def _importa_nucleo(t: ast.Module) -> bool:
    for n in ast.walk(t):
        if isinstance(n, ast.ImportFrom) and n.module:
            mod = n.module
            if mod == "dmcore" and any(a.name in NUCLEO_CON_REGOLE for a in n.names):
                return True
            if mod.startswith("dmcore.") and mod.split(".", 1)[1] in NUCLEO_CON_REGOLE:
                return True
        if isinstance(n, ast.Import):
            if any(a.name.startswith("dmcore.") and a.name.split(".", 1)[1] in NUCLEO_CON_REGOLE
                   for a in n.names):
                return True
    return False


def a2_importatori(alberi: dict[str, ast.Module]) -> list[str]:
    return sorted(rel for rel, t in alberi.items()
                  if not rel.startswith("scripts/dmcore/") and _importa_nucleo(t))


def _aritmetica_pura(e: ast.expr) -> bool:
    for n in ast.walk(e):
        if isinstance(n, (ast.BinOp, ast.UnaryOp, ast.Name, ast.Constant, ast.Load,
                          ast.operator, ast.unaryop)):
            continue
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in FUNZIONI_ARITMETICHE:
            continue
        return False
    return any(isinstance(n, ast.BinOp) for n in ast.walk(e))


def a3_formule(alberi: dict[str, ast.Module]) -> list[str]:
    out = []
    for rel, t in alberi.items():
        if not rel.startswith("scripts/dmcore/"):
            continue
        for f in t.body:
            if not isinstance(f, ast.FunctionDef):
                continue
            corpo = [s for s in f.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
            if len(corpo) == 1 and isinstance(corpo[0], ast.Return) and corpo[0].value is not None \
                    and _aritmetica_pura(corpo[0].value):
                chiave = f"{rel}:{f.name}"
                if chiave not in NON_FORMULE:
                    out.append(chiave)
    return sorted(out)


def a4_capacita_in_codice() -> list[str]:
    sys.path.insert(0, str(SCRIPTS))
    from dmcore import sistemi as S  # noqa: E402
    import tomllib
    catalogo = tomllib.loads((ROOT / "sistemi" / "catalogo.toml").read_text(encoding="utf-8"))["capacita"]
    out = []
    for sis in S.attivi():
        for nome in sorted(catalogo):
            if S.capacita(sis, nome).modo == "codice":
                out.append(f"{sis}:{nome}")
    return out


def a5_senza_sistema_del_file(alberi: dict[str, ast.Module]) -> list[str]:
    out = []
    for rel in a2_importatori(alberi):
        t = alberi[rel]
        if not any(isinstance(n, ast.Call) and _nome_chiamata(n) == "sistema_di" for n in ast.walk(t)):
            out.append(rel)
    return out


def censisci() -> dict:
    alberi = {}
    for p in _file_python():
        t = _albero(p)
        if t is not None:
            alberi[_rel(p)] = t
    elenchi = {
        "A1_caricamenti_all_import": a1_caricamenti_all_import(alberi),
        "A2_importatori_del_nucleo": a2_importatori(alberi),
        "A3_formule_in_python": a3_formule(alberi),
        "A4_capacita_in_codice": a4_capacita_in_codice(),
        "A5_strumenti_senza_sistema_del_file": a5_senza_sistema_del_file(alberi),
    }
    return {"file_letti": len(alberi),
            "misure": {k: len(v) for k, v in elenchi.items()},
            "elenchi": elenchi}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", metavar="FILE", help="scrive il censimento in FILE")
    ap.add_argument("--check", action="store_true", help="esce 1 se una misura sale rispetto a CENSIMENTO.json")
    a = ap.parse_args(argv)
    c = censisci()
    if a.json:
        Path(a.json).write_text(json.dumps(c, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if a.check:
        rif = json.loads(RIFERIMENTO.read_text(encoding="utf-8"))["misure"]
        salite = [f"{k}: {rif.get(k)} → {v}" for k, v in c["misure"].items() if v > rif.get(k, 0)]
        if salite:
            print("✗ censimento_formule: misure salite\n  " + "\n  ".join(salite))
            return 1
        print("✓ censimento_formule: nessuna misura sale — " +
              ", ".join(f"{k.split('_', 1)[0]} {v}" for k, v in c["misure"].items()))
        return 0
    if not a.json:
        for k, v in c["elenchi"].items():
            print(f"{k}: {len(v)}")
            for r in v:
                print(f"  {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
