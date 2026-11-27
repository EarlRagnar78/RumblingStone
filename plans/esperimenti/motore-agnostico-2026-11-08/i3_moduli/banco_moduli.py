#!/usr/bin/env python3
"""banco_moduli.py — indagine I3 di PIANO-MOTORE-AGNOSTICO-D20: come un plugin porta il suo codice.

Un algoritmo che non si riduce a dati (oggi `METODI` di suggest_encounter:
«potenze» del 3.5 e «somma_px» del PF1e) deve vivere nel plugin del sistema e
non nel nucleo. Il banco prova tre modi di caricarlo, in un repo temporaneo con
due plugin (dnd35 e pf1e) che hanno ognuno `codice/metodi.py` con lo STESSO nome
di modulo e la STESSA funzione `combina`, ma algoritmi diversi:

    importlib   registro per nome in sistema.toml (`[moduli] combina = "metodi:combina"`),
                file caricato con importlib.util.spec_from_file_location solo da
                sistemi/<id>/codice/ (libreria standard)
    entry_point gruppo `rumblingstone.metodi` di importlib.metadata, il meccanismo
                PyPA dei plugin installati; il banco crea il dist-info a mano, perché
                nella skill impacchettata non c'è pip
    pluggy      hookspec `metodi_incontro` di pluggy 1.7 (pytest, tox); pluggy non
                trova i file, quindi i moduli li trova il caricatore importlib e
                pluggy fa solo da registro dei ganci

Criteri:
    (a) correttezza   il metodo caricato dal plugin dà lo stesso EL di METODI su
                      tutte le liste di 1-3 GS (28 valori, con ripetizione: 4.494 liste)
    (b) isolamento    i due `metodi.combina` non si pestano (stesso nome di modulo)
    (c) ostili        12 dichiarazioni che puntano fuori da sistemi/<id>/codice/
                      (percorsi, moduli della libreria standard, symlink, dunder,
                      non chiamabili): ognuna va RIFIUTATA senza eseguire codice
                      che stia fuori da quella cartella
    (d) determinismo  due caricamenti danno lo stesso registro, nello stesso ordine
    (e) costo         righe del caricatore; dipendenze da portare nel pacchetto

    python3 banco_moduli.py                      # tabella
    python3 banco_moduli.py --json RISULTATI.json
"""
from __future__ import annotations

import argparse
import importlib.metadata as md
import importlib.util
import inspect
import itertools
import json
import os
import re
import sys
import tempfile
import tomllib
from pathlib import Path

QUI = Path(__file__).resolve().parent
REPO = QUI.parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import suggest_encounter as SE  # noqa: E402

GS = [0.125, 0.25, 0.5] + list(range(1, 26))
LISTE = [list(c) for n in (1, 2, 3) for c in itertools.combinations_with_replacement(GS, n)]

# ------------------------------------------------------------ il repo finto

def _sorgente_metodi(sistema: str) -> str:
    """Il modulo del plugin: l'algoritmo copiato dal nucleo, con lo stesso nome `combina`."""
    if sistema == "dnd35":
        corpo = inspect.getsource(SE.combine_el).replace("def combine_el(", "def _potenze(")
        return ("import math\n\nCOSTANTE = 2\n\n" + corpo +
                "\n\ndef combina(dati):\n    return lambda crs: _potenze(crs, dati.get('raddoppio', 2))\n")
    corpo = inspect.getsource(SE._px_pf1e) + "\n\n" + inspect.getsource(SE.combina_gs_pf1e)
    corpo = corpo.replace('''    if tab is None:
        from dmcore import sistemi as S
        tab = S.dati("pf1e", "incontri.livello")["px_per_gs"]
''', "")
    return ("COSTANTE = 3\n\n" + corpo +
            "\n\ndef combina(dati):\n    return lambda crs: combina_gs_pf1e(crs, dati['px_per_gs'])\n")


OSTILI = {
    "risale con ..": "../../../scripts/suggest_encounter:combine_el",
    "percorso assoluto": "/etc/passwd:x",
    "modulo della libreria standard": "os:system",
    "modulo builtins": "builtins:exec",
    "modulo con punto": "metodi.sotto:combina",
    "funzione dunder": "metodi:__builtins__",
    "attributo di un attributo": "metodi:math.sqrt",
    "funzione che non c'è": "metodi:non_esiste",
    "non chiamabile": "metodi:COSTANTE",
    "modulo che non c'è": "mancante:combina",
    "symlink fuori dalla cartella": "fuori:combine_el",
    "vuota": "",
}


def costruisci(base: Path) -> Path:
    root = base / "repo"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "suggest_encounter.py").write_text("def combine_el(c, r=2):\n    return 0\n")
    for sid in ("dnd35", "pf1e"):
        cod = root / "sistemi" / sid / "codice"
        cod.mkdir(parents=True)
        (cod / "metodi.py").write_text(_sorgente_metodi(sid), encoding="utf-8")
        (cod / "fuori.py").symlink_to(root / "scripts" / "suggest_encounter.py")
        (root / "sistemi" / sid / "sistema.toml").write_text(
            f'id = "{sid}"\n\n[moduli]\ncombina = "metodi:combina"\n', encoding="utf-8")
    return root


# ------------------------------------------------------------ i tre caricatori

NOME = re.compile(r"^[a-z_][a-z0-9_]*$")


class Importlib:
    nome = "importlib (registro per nome, libreria standard)"
    dipendenze = "nessuna (libreria standard)"

    def __init__(self, root: Path):
        self.root = root

    def risolvi(self, sid: str, ref: str):
        # --- inizio caricatore (le righe contate in (e))
        mod, sep, fun = ref.partition(":")
        if not sep or not NOME.match(mod) or not NOME.match(fun) or fun.startswith("__"):
            raise ValueError(f"«{ref}»: serve «modulo:funzione», nomi semplici")
        cartella = (self.root / "sistemi" / sid / "codice").resolve()
        file = (cartella / f"{mod}.py").resolve()  # resolve() segue i symlink
        if file.parent != cartella or not file.is_file():
            raise ValueError(f"«{ref}»: {mod}.py non è in sistemi/{sid}/codice/")
        spec = importlib.util.spec_from_file_location(f"rs_plugin.{sid}.{mod}", file)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        f = getattr(modulo, fun, None)
        if not inspect.isfunction(f) or f.__module__ != modulo.__name__:
            raise ValueError(f"«{ref}»: {fun} non è una funzione definita in {mod}.py")
        return f
        # --- fine caricatore

    def registro(self, sid: str, dich: dict) -> dict:
        return {k: self.risolvi(sid, v) for k, v in sorted(dich.items())}


class EntryPoint:
    nome = "entry point (importlib.metadata, PyPA)"
    dipendenze = "nessuna, ma serve un dist-info installato per ogni plugin"

    def __init__(self, root: Path):
        self.root = root
        self.siti = root.parent / "siti"

    def risolvi(self, sid: str, ref: str):
        # --- inizio caricatore
        sito = self.siti / sid
        dist = sito / f"rs_plugin_{sid}-0.dist-info"
        dist.mkdir(parents=True, exist_ok=True)
        (dist / "METADATA").write_text(f"Metadata-Version: 2.1\nName: rs-plugin-{sid}\nVersion: 0\n")
        (dist / "entry_points.txt").write_text(f"[rumblingstone.metodi]\ncombina = {ref}\n")
        cod = str(self.root / "sistemi" / sid / "codice")
        sys.path.insert(0, cod)
        try:
            eps = [e for d in md.distributions(path=[str(sito)]) for e in d.entry_points
                   if e.group == "rumblingstone.metodi" and e.name == "combina"]
            f = eps[0].load()
        finally:
            sys.path.remove(cod)
        if not callable(f):
            raise ValueError(f"«{ref}»: non chiamabile")
        return f
        # --- fine caricatore

    def registro(self, sid: str, dich: dict) -> dict:
        return {k: self.risolvi(sid, v) for k, v in sorted(dich.items())}


class Pluggy:
    nome = "pluggy 1.7 (ganci) sopra importlib"
    dipendenze = "pluggy (MIT, puro Python, 2.094 righe)"

    def __init__(self, root: Path):
        import pluggy
        self.pluggy = pluggy
        self.base = Importlib(root)

    def registro(self, sid: str, dich: dict) -> dict:
        # --- inizio caricatore
        pluggy = self.pluggy
        spec = pluggy.HookspecMarker("rumblingstone")
        impl = pluggy.HookimplMarker("rumblingstone")

        class Spec:
            @spec
            def metodi_incontro(self):
                """{nome: funzione} che il plugin offre"""

        pm = pluggy.PluginManager("rumblingstone")
        pm.add_hookspecs(Spec)
        funzioni = {k: self.base.risolvi(sid, v) for k, v in sorted(dich.items())}

        class Plugin:
            @impl
            def metodi_incontro(self):
                return funzioni

        pm.register(Plugin(), name=sid)
        out = {}
        for d in pm.hook.metodi_incontro():
            out.update(d)
        return out
        # --- fine caricatore


def righe(cls) -> int:
    src = inspect.getsource(cls).splitlines()
    dentro, n = False, 0
    for r in src:
        if "--- inizio caricatore" in r:
            dentro = True
            continue
        if "--- fine caricatore" in r:
            dentro = False
            continue
        if dentro and r.strip() and not r.strip().startswith("#"):
            n += 1
    return n


# ------------------------------------------------------------ il banco

def _dati(sid: str) -> dict:
    return tomllib.loads((REPO / "sistemi" / sid / "dati" / "incontri.toml").read_text(encoding="utf-8"))


def prova(cls, base: Path) -> dict:
    root = costruisci(base)
    car = cls(root)
    ris: dict = {"nome": cls.nome, "dipendenze": cls.dipendenze, "righe_caricatore": righe(cls)}
    # (a) e (b)
    giuste, isolati = {}, True
    for sid, metodo in (("dnd35", "potenze"), ("pf1e", "somma_px")):
        dich = tomllib.loads((root / "sistemi" / sid / "sistema.toml").read_text())["moduli"]
        f = car.registro(sid, dich)["combina"](_dati(sid))
        atteso = SE.METODI[metodo](_dati(sid))
        giuste[sid] = sum(f(c) == atteso(c) for c in LISTE)
    a = car.registro("dnd35", {"combina": "metodi:combina"})["combina"]
    b = car.registro("pf1e", {"combina": "metodi:combina"})["combina"]
    isolati = a is not b and a.__globals__.get("COSTANTE") == 2 and b.__globals__.get("COSTANTE") == 3
    ris["correttezza"] = {k: f"{v}/{len(LISTE)}" for k, v in giuste.items()}
    ris["isolamento"] = isolati
    # (c)
    rifiutate, accettate = [], []
    for nome, ref in OSTILI.items():
        prima = set(sys.modules)
        try:
            f = car.registro("dnd35", {"combina": ref})["combina"]
            accettate.append(f"{nome} → {getattr(f, '__module__', '?')}.{getattr(f, '__name__', '?')}")
        except Exception as ex:  # noqa: BLE001
            caricato = sorted(m for m in set(sys.modules) - prima if m.startswith(("rs_plugin", "fuori", "metodi")))
            rifiutate.append(f"{nome}: {type(ex).__name__}" + (f" (dopo aver eseguito {caricato})" if caricato else ""))
        for m in [m for m in sys.modules if m in ("metodi", "fuori", "mancante") or m.startswith("rs_plugin")]:
            del sys.modules[m]
    ris["ostili_rifiutate"] = f"{len(rifiutate)}/{len(OSTILI)}"
    ris["ostili_accettate"] = accettate
    ris["rifiuti"] = rifiutate
    # (d)
    r1 = car.registro("pf1e", {"z": "metodi:combina", "a": "metodi:combina"})
    r2 = car.registro("pf1e", {"a": "metodi:combina", "z": "metodi:combina"})
    ris["determinismo"] = list(r1) == list(r2) == ["a", "z"]
    return ris


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    out = []
    for cls in (Importlib, EntryPoint, Pluggy):
        try:
            cls.__init__  # noqa: B018
            with tempfile.TemporaryDirectory() as t:
                out.append(prova(cls, Path(t)))
        except ImportError as ex:
            out.append({"nome": cls.nome, "saltato": str(ex)})
    for r in out:
        if "saltato" in r:
            print(f"{r['nome']}: saltato ({r['saltato']})")
            continue
        print(f"{r['nome']}\n    correttezza {r['correttezza']}  isolamento {r['isolamento']}  "
              f"ostili rifiutate {r['ostili_rifiutate']}  determinismo {r['determinismo']}  "
              f"righe {r['righe_caricatore']}  dipendenze: {r['dipendenze']}")
        for x in r["ostili_accettate"]:
            print(f"      ACCETTATA: {x}")
    if a.json:
        a.json.write_text(json.dumps({"python": sys.version.split()[0], "liste": len(LISTE), "risultati": out},
                                     ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
