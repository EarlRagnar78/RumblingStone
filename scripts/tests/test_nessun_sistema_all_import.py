"""F2 di ADR-0112: nessun modulo del nucleo carica un sistema all'import.

Il sistema lo sceglie chi calcola (`dmcore.sistemi.regole(id)` o
`regole_di(file)`), non l'ordine in cui Python carica i moduli. La prova si
fa in un interprete nuovo: si sostituisce `sistemi.dati` con una spia, si
importano **tutti** i moduli di `dmcore`, e la spia non deve essere chiamata.
I nomi di sempre (`T.TIPI`, `I.LISTE`, …) restano e caricano alla prima
richiesta; le impronte dei valori stanno in `test_sistemi_creature.py`.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from dmcore import sistemi as S  # noqa: E402

SPIA = r"""
import importlib, json, pkgutil, sys, traceback
sys.path.insert(0, sys.argv[1])
from dmcore import sistemi as S
chiamate = []
originale = S.dati
def spia(*a, **k):
    chi = [f"{f.filename.rsplit('/scripts/', 1)[-1]}:{f.lineno}"
           for f in traceback.extract_stack()[:-1] if f.name == "<module>"]
    chiamate.append([list(map(str, a)), chi[-1] if chi else "?"])
    return originale(*a, **k)
S.dati = spia
import dmcore
errori = []
for m in sorted(pkgutil.iter_modules(dmcore.__path__), key=lambda m: m.name):
    try:
        importlib.import_module(f"dmcore.{m.name}")
    except ImportError as e:   # dipendenze facoltative (tcod, typst…): non sono sistemi
        errori.append([m.name, str(e)])
print(json.dumps({"chiamate": chiamate, "errori": errori}))
"""


class NessunSistemaAllImport(unittest.TestCase):

    def test_importare_dmcore_non_legge_nessun_sistema(self):
        r = subprocess.run([sys.executable, "-c", SPIA, str(SCRIPTS)],
                           capture_output=True, text=True, cwd=ROOT, check=True)
        esito = json.loads(r.stdout.strip().splitlines()[-1])
        self.assertEqual(esito["chiamate"], [],
                         "un modulo di dmcore legge un sistema all'import: "
                         + "; ".join(f"{a} da {dove}" for a, dove in esito["chiamate"]))

    def test_i_nomi_di_sempre_arrivano_alla_prima_richiesta(self):
        from dmcore import incantesimi as I
        from dmcore import tabelle as T
        self.assertIs(T.TIPI, T.di("dnd35")["TIPI"])
        self.assertIs(T.DRUIDO, T.CHIERICO)
        self.assertIs(I.LISTE["mago"], I.LISTE["stregone"])
        with self.assertRaises(AttributeError):
            T.NON_ESISTE  # noqa: B018

    def test_ogni_nome_di_all_si_trova(self):
        from dmcore import caratteristiche, lettura_creatura, progressione
        for m in (caratteristiche, lettura_creatura, progressione):
            for nome in m.__all__:
                with self.subTest(modulo=m.__name__, nome=nome):
                    getattr(m, nome)


class ContestoEsplicito(unittest.TestCase):

    def test_regole_di_un_sistema(self):
        r = S.regole("pf1e")
        self.assertEqual(r.id, "pf1e")
        self.assertIs(r, S.regole("pf1e"))
        self.assertEqual(r.dati("fonti.regole")["chiave"], S.dati("pf1e", "fonti.regole")["chiave"])

    def test_un_sistema_sconosciuto_fallisce_subito(self):
        with self.assertRaises(S.ErroreSistemi):
            S.regole("gurps")

    def test_regole_del_file(self):
        drappo = next((ROOT / "10-stand-alone").glob("Il-Drappo-di-Tarsilia*"), None)
        if drappo is None:
            self.skipTest("manca il Drappo")
        self.assertEqual(S.regole_di(drappo.relative_to(ROOT)).id, S.sistema_di(drappo.relative_to(ROOT)))


if __name__ == "__main__":
    unittest.main()
