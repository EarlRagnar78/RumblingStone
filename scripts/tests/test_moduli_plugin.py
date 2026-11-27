"""F5 di ADR-0112: gli algoritmi di sistema sono codice dei plugin, non del nucleo.

Tre prove:

1. i metodi «potenze» (d20) e «somma_px» (pf1e), caricati dal registro
   `[moduli]` del plugin, danno lo stesso numero delle funzioni che stavano in
   `suggest_encounter` (copiate qui com'erano al 2026-11-08) su tutte le 4.494
   liste di 1-3 GS del banco I3;
2. il caricatore rifiuta le 12 dichiarazioni ostili del banco I3 senza eseguire
   niente fuori da `sistemi/<id>/codice/`, e due plugin con un modulo dallo
   stesso nome non si scambiano il codice;
3. nel nucleo e in `suggest_encounter` non c'è più un algoritmo che combina i GS.
"""
from __future__ import annotations

import ast
import itertools
import math
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import suggest_encounter as SE  # noqa: E402
from dmcore import sistemi as S  # noqa: E402

GS = [0.125, 0.25, 0.5] + list(range(1, 26))
LISTE = [list(c) for n in (1, 2, 3) for c in itertools.combinations_with_replacement(GS, n)]


# ---- com'erano in suggest_encounter prima di F5 -----------------------------
def _prima_potenze(crs, raddoppio=2.0):
    if not crs:
        return 0.0
    r = float(raddoppio)
    return r * math.log2(sum(2 ** (c / r) for c in crs))


def _prima_px(cr, tab):
    if cr < 1:
        chiave = f"1/{round(1 / cr)}" if cr > 0 else "1/8"
        return tab.get(chiave, tab["1/8"])
    c = int(round(cr))
    if str(c) in tab:
        return tab[str(c)]
    alto = max(int(k) for k in tab if "/" not in k)
    return tab[str(alto - (c - alto) % 2)] * 2 ** ((c - alto + 1) // 2) if c > alto else tab["1"]


def _prima_somma_px(crs, tab):
    if not crs:
        return 0.0
    tot = sum(_prima_px(c, tab) for c in crs)
    gs = 0.0
    for chiave, px in tab.items():
        a, _, b = chiave.partition("/")
        v = int(a) / int(b) if b else float(a)
        if px <= tot and v > gs:
            gs = v
    alto = max(int(k) for k in tab if "/" not in k)
    while gs >= alto and _prima_px(gs + 1, tab) <= tot:
        gs += 1
    return gs


#: Le 12 dichiarazioni ostili del banco I3 (`i3_moduli/banco_moduli.py`).
OSTILI = {
    "risale con ..": "../../../scripts/suggest_encounter:combine_el",
    "percorso assoluto": "/etc/passwd:x",
    "modulo della libreria standard": "os:system",
    "modulo builtins": "builtins:exec",
    "modulo con punto": "incontri.sotto:potenze",
    "funzione dunder": "incontri:__builtins__",
    "attributo di un attributo": "incontri:math.sqrt",
    "funzione che non c'è": "incontri:non_esiste",
    "non chiamabile": "incontri:COSTANTE",
    "modulo che non c'è": "mancante:potenze",
    "symlink fuori dalla cartella": "fuori:combine_el",
    "vuota": "",
}


class GliStessiNumeri(unittest.TestCase):

    def test_potenze_su_tutte_le_liste(self):
        for r in (2, 3):
            f = S.modulo("d20", "potenze")({"raddoppio": r})
            diversi = [c for c in LISTE if f(c) != _prima_potenze(c, r)]
            self.assertEqual(diversi, [], f"raddoppio {r}")

    def test_somma_px_su_tutte_le_liste(self):
        tab = S.dati("pf1e", "incontri.livello")["px_per_gs"]
        f = S.modulo("pf1e", "somma_px")({"px_per_gs": tab})
        self.assertEqual([c for c in LISTE if f(c) != _prima_somma_px(c, tab)], [])

    def test_combinatore_di_ogni_sistema(self):
        tab = S.dati("pf1e", "incontri.livello")["px_per_gs"]
        for c in LISTE:
            self.assertEqual(SE.combinatore("dnd35")(c), _prima_potenze(c, 2))
            self.assertEqual(SE.combinatore("pf1e")(c), _prima_somma_px(c, tab))
            self.assertEqual(SE.combine_el(c), _prima_potenze(c, 2))
            self.assertEqual(SE.combina_gs_pf1e(c), _prima_somma_px(c, tab))

    def test_il_modulo_si_cerca_nella_famiglia(self):
        # dnd35 non dichiara moduli: «potenze» arriva dalla famiglia d20
        self.assertIs(S.modulo("dnd35", "potenze"), S.modulo("d20", "potenze"))
        self.assertIn("somma_px", S.moduli("pf1e"))
        self.assertIn("potenze", S.moduli("pf1e"))  # anche pf1e è della famiglia d20
        with self.assertRaises(S.ErroreSistemi):
            S.modulo("dnd35", "somma_px")


class IlCaricatoreEChiuso(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT / "sistemi", self.root / "sistemi")
        shutil.copy(ROOT / "sistemi.toml", self.root / "sistemi.toml")
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "suggest_encounter.py").write_text(
            "raise SystemExit('eseguito fuori dalla cartella')\n", encoding="utf-8")
        cod = self.root / "sistemi" / "d20" / "codice"
        (cod / "fuori.py").symlink_to(self.root / "scripts" / "suggest_encounter.py")
        (cod / "incontri.py").write_text(
            (cod / "incontri.py").read_text(encoding="utf-8") + "\nCOSTANTE = 1\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_le_ostili_sono_rifiutate(self):
        passate = []
        for nome, rif in OSTILI.items():
            try:
                S._risolvi("d20", rif, self.root.resolve())
            except S.ErroreSistemi:
                continue
            passate.append(nome)
        self.assertEqual(passate, [])

    def test_due_plugin_con_lo_stesso_modulo_restano_separati(self):
        r = self.root.resolve()
        potenze = S._risolvi("d20", "incontri:potenze", r)
        somma = S._risolvi("pf1e", "incontri:somma_px", r)
        self.assertNotEqual(potenze.__module__, somma.__module__)
        self.assertEqual(S._risolvi("d20", "incontri:potenze", r)({"raddoppio": 2})([10, 10]), 12.0)
        tab = S.dati("pf1e", "incontri.livello", r)["px_per_gs"]
        self.assertEqual(somma({"px_per_gs": tab})([10, 10]), 12.0)

    def test_il_controllo_trova_un_modulo_rotto(self):
        p = self.root / "sistemi" / "pf1e" / "sistema.toml"
        p.write_text(p.read_text(encoding="utf-8").replace(
            'somma_px = "incontri:somma_px"', 'somma_px = "os:system"'), encoding="utf-8")
        S._carica.cache_clear()
        try:
            self.assertTrue(any("[moduli] somma_px" in x for x in S.problemi(self.root)))
        finally:
            S._carica.cache_clear()

    def test_il_repo_non_ha_moduli_rotti(self):
        self.assertFalse([x for x in S.problemi() if "[moduli]" in x])


class NessunAlgoritmoNelNucleo(unittest.TestCase):

    def test_suggest_encounter_non_combina_i_gs(self):
        albero = ast.parse((ROOT / "scripts" / "suggest_encounter.py").read_text(encoding="utf-8"))
        nomi = {n.id for n in ast.walk(albero) if isinstance(n, ast.Name)}
        attributi = {n.attr for n in ast.walk(albero) if isinstance(n, ast.Attribute)}
        self.assertNotIn("METODI", nomi)
        self.assertNotIn("log2", attributi)
        self.assertNotIn("_px_pf1e", {f.name for f in albero.body if isinstance(f, ast.FunctionDef)})

    def test_dmcore_non_ha_metodi_di_incontro(self):
        for f in (ROOT / "scripts" / "dmcore").glob("*.py"):
            testo = f.read_text(encoding="utf-8")
            with self.subTest(file=f.name):
                self.assertNotIn("log2(", testo)
                self.assertNotIn("px_per_gs(", testo)


if __name__ == "__main__":
    unittest.main()
