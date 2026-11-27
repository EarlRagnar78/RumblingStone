"""F3 di ADR-0112: le formule d20 sono dati, e danno gli stessi numeri di prima.

Ogni formula di `sistemi/d20/dati/formule.toml` si confronta con la funzione
Python che ha sostituito, su tutto il dominio del banco I1 (punteggi 0-60, DV
0-40, livelli d'incantesimo 0-9, modificatori −10…+20). Le 50 espressioni
ostili di I1 devono essere rifiutate dal controllo e dal valutatore. Il file
portato dentro (`dmcore/_vendor/simpleeval.py`) deve avere lo sha256 scritto in
`LIBRERIE.toml`.
"""
from __future__ import annotations

import hashlib
import sys
import tomllib
import unittest
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import caratteristiche as C  # noqa: E402
from dmcore import creature_pf1e as CP  # noqa: E402
from dmcore import formule as F  # noqa: E402
from dmcore import tabelle as T  # noqa: E402

VENDOR = ROOT / "scripts" / "dmcore" / "_vendor"

#: Le funzioni com'erano prima di F3 (copiate dal codice del 2026-11-08).
PRIMA = {
    "modificatore": (lambda punteggio: (punteggio - 10) // 2, {"punteggio": range(0, 61)}),
    "ts_buono": (lambda dv: 2 + dv // 2, {"dv": range(0, 41)}),
    "ts_cattivo": (lambda dv: dv // 3, {"dv": range(0, 41)}),
    "cd_incantesimo": (lambda livello, modificatore: 10 + livello + modificatore,
                       {"livello": range(0, 10), "modificatore": range(-5, 21)}),
    "punteggio_minimo": (lambda modificatore: max(1, 10 + 2 * modificatore),
                         {"modificatore": range(-10, 21)}),
    "livello_incantatore_ridotto": (lambda livello: max(0, livello - 3), {"livello": range(0, 41)}),
    # «Table: Ability Modifiers and Bonus Spells»: nessuno sotto il livello, poi uno ogni quattro punti
    "incantesimi_bonus": (lambda livello, modificatore: 0 if livello < 1 or modificatore < livello
                          else 1 + (modificatore - livello) // 4,
                          {"livello": range(0, 10), "modificatore": range(-5, 21)}),
    "punteggio_per_lanciare": (lambda livello: 10 + livello, {"livello": range(0, 10)}),
}

#: Le 50 ostili del banco I1 (`i1_formule/banco_formule.py`).
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


def _casi(dominio: dict):
    nomi = list(dominio)
    for valori in product(*dominio.values()):
        yield dict(zip(nomi, valori))


class LeFormuleDannoINumeriDiPrima(unittest.TestCase):

    def test_ogni_formula_ha_il_suo_confronto(self):
        self.assertEqual(set(F.formule("d20")), set(PRIMA))

    def test_stesso_numero_su_tutto_il_dominio(self):
        for sistema in ("d20", "dnd35", "pf1e"):
            for nome, (prima, dominio) in PRIMA.items():
                f = F.formula(nome, sistema)
                diversi = [c for c in _casi(dominio) if f(**c) != prima(**c)]
                self.assertEqual(diversi, [], f"{sistema} {nome}")

    def test_le_funzioni_del_nucleo_usano_la_formula(self):
        for p in range(0, 61):
            self.assertEqual(T.mod(p), (p - 10) // 2)
            self.assertEqual(CP._mod(p), (p - 10) // 2)
        for dv in range(0, 41):
            self.assertEqual((T.ts_buono(dv), T.ts_cattivo(dv)), (2 + dv // 2, dv // 3))
        for m in range(-10, 21):
            self.assertEqual(C.da_modificatore(m), max(1, 10 + 2 * m))
        self.assertEqual(T.cd_incantesimo(9, 8), 27)
        for liv in range(0, 41):
            self.assertEqual(T.livello_incantatore("ranger", liv), max(0, liv - 3))
            self.assertEqual(T.livello_incantatore("mago", liv), liv)


class LeFormuleSonoChiuse(unittest.TestCase):

    def test_il_controllo_rifiuta_le_ostili(self):
        passate = [e for e in OSTILI if not F.controlla(e, ("dv",))]
        self.assertEqual(passate, [])

    def test_il_valutatore_rifiuta_le_ostili(self):
        """Anche senza il controllo: errore, oppure un risultato non intero che `Formula` scarta."""
        passate = []
        for e in OSTILI:
            try:
                r = F._valutatore(e, (("dv", 3),))
            except Exception:  # noqa: BLE001 — ogni rifiuto va bene
                continue
            if type(r) is int:
                passate.append(e)
        self.assertEqual(passate, [])

    def test_ingressi_sbagliati(self):
        f = F.formula("modificatore")
        for valori in ({}, {"punteggio": 14, "altro": 1}, {"punteggio": 14.0}, {"punteggio": True}):
            with self.subTest(valori=valori), self.assertRaises(F.ErroreFormula):
                f(**valori)

    def test_nome_non_dichiarato(self):
        self.assertIn("nome non dichiarato negli ingressi: dv", F.controlla("dv + 1", ("punteggio",)))

    def test_il_plugin_non_ha_difetti(self):
        self.assertEqual(F.problemi(), [])


class LaLibreriaPortataDentro(unittest.TestCase):

    def test_sha256_come_in_librerie_toml(self):
        librerie = tomllib.loads((VENDOR / "LIBRERIE.toml").read_text(encoding="utf-8"))
        for nome, v in librerie.items():
            self.assertTrue((VENDOR / v["file_licenza"]).is_file(), nome)
            for f, atteso in v["file"].items():
                with self.subTest(libreria=nome, file=f):
                    self.assertEqual(hashlib.sha256((VENDOR / f).read_bytes()).hexdigest(), atteso)


if __name__ == "__main__":
    unittest.main()
