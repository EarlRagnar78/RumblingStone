"""F6 di ADR-0112: la seconda prova del nove.

La prima (L8, `test_sistemi_prova_del_nove.py`) ha mostrato che un sistema
d20 che cambia **dati** entra senza toccare il codice. Questa prova lo stesso
per le due cose che F3 e F5 hanno tolto dal nucleo:

- una **formula** diversa (TS buono `3 + dv // 2` invece di `2 + dv // 2`),
  scritta nei dati del plugin;
- un **algoritmo** suo per l'EL («piu_forte»: GS più alto + creature − 1),
  scritto in `codice/` del plugin.

Si prende un repo temporaneo con `sistemi/`, `sistemi.toml` e il manifest, ci
si copia il plugin finto `scripts/tests/dati/prova-d20-due/` e una riga in
`sistemi.toml`. Gli strumenti veri, senza cambiarne una riga, devono dare
esattamente quello che le regole del plugin dicono, e il 3.5 deve restare
com'era. File del nucleo toccati: zero per costruzione, perché il test scrive
solo dentro il repo temporaneo.
"""
from __future__ import annotations

import itertools
import shutil
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import sistemi as CLI  # noqa: E402
import suggest_encounter as SE  # noqa: E402
from dmcore import formule as F  # noqa: E402
from dmcore import sistemi as S  # noqa: E402

FINTO = REPO / "scripts" / "tests" / "dati" / "prova-d20-due"
ID = "prova-d20-due"
GS = [0.5] + list(range(1, 21))
LISTE = [list(c) for n in (1, 2, 3) for c in itertools.combinations_with_replacement(GS, n)]


def _file_dei_plugin() -> "set[str]":
    fuori = set()
    for f in (REPO / "sistemi").glob("*/sistema.toml"):
        for c in tomllib.loads(f.read_text(encoding="utf-8")).get("capacita", {}).values():
            fuori.update(c.get("dati", []))
            fuori.update(v.split(":", 1)[0] for v in c.get("codice", []))
    return fuori


class ProvaDelNove2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        r = cls.root = Path(cls._tmp.name)
        shutil.copytree(REPO / "sistemi", r / "sistemi")
        for rel in _file_dei_plugin() | {"scripts/tools.manifest.json"}:
            (r / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / rel, r / rel)
        for d in (REPO / "skills").iterdir():
            if (d / "SKILL.md").is_file():
                (r / "skills" / d.name).mkdir(parents=True)
                (r / "skills" / d.name / "SKILL.md").write_text("", encoding="utf-8")
        shutil.copytree(FINTO, r / "sistemi" / ID)
        cfg = (REPO / "sistemi.toml").read_text(encoding="utf-8")
        letto = tomllib.loads(cfg)
        for cartella in {**letto.get("moduli", {}), **letto.get("ambientazioni", {}).get("moduli", {})}:
            (r / cartella).mkdir(parents=True)
        (r / "moduli-di-prova").mkdir()
        cfg = cfg.replace('attivi = ["dnd35", "pf1e"]', f'attivi = ["dnd35", "pf1e", "{ID}"]')
        cfg = cfg.replace("[moduli]\n", f'[moduli]\n"moduli-di-prova" = "{ID}"\n')
        (r / "sistemi.toml").write_text(cfg, encoding="utf-8")
        cls._root_vero = S.ROOT
        S.ROOT = r
        S._carica.cache_clear()

    @classmethod
    def tearDownClass(cls):
        S.ROOT = cls._root_vero
        S._carica.cache_clear()
        cls._tmp.cleanup()

    def test_il_cancello_resta_verde(self):
        self.assertIn(ID, S.attivi())
        self.assertEqual(S.problemi(self.root, CLI.strumenti(self.root)), [])
        self.assertEqual(F.problemi(self.root), [])

    def test_il_file_prende_il_sistema_nuovo(self):
        self.assertEqual(S.sistema_di("moduli-di-prova/capitolo.md"), ID)

    def test_la_formula_cambia_esattamente_come_dice_il_plugin(self):
        nuovo, vecchio = F.formula("ts_buono", ID), F.formula("ts_buono", "dnd35")
        for dv in range(0, 41):
            self.assertEqual(nuovo(dv=dv), 3 + dv // 2)
            self.assertEqual(nuovo(dv=dv) - vecchio(dv=dv), 1)

    def test_le_altre_formule_restano_quelle_d20(self):
        for nome, f in F.formule(ID).items():
            if nome == "ts_buono":
                continue
            self.assertEqual(f.espressione, F.formula(nome, "d20").espressione, nome)

    def test_l_algoritmo_del_plugin_arriva_in_suggest_encounter(self):
        el = SE.combinatore(ID)
        for crs in LISTE:
            self.assertEqual(el(crs), float(max(crs) + len(crs) - 1))
        self.assertEqual(el([10, 10]), 11.0)          # 3.5: 12
        self.assertEqual(SE.combinatore("dnd35")([10, 10]), 12.0)

    def test_il_codice_del_plugin_resta_nel_plugin(self):
        f = S.modulo(ID, "piu_forte")
        self.assertTrue(f.__module__.startswith("rs_plugin.prova_d20_due."))
        self.assertIn("potenze", S.moduli(ID))       # la famiglia resta visibile
        self.assertNotIn("piu_forte", S.moduli("dnd35"))

    def test_il_plugin_finto_porta_solo_dati_e_il_suo_codice(self):
        file = sorted(str(p.relative_to(FINTO)) for p in FINTO.rglob("*")
                      if p.is_file() and "__pycache__" not in p.parts)
        self.assertEqual(file, ["codice/incontri.py", "dati/formule.toml", "dati/incontri.toml",
                                "sistema.toml"])


if __name__ == "__main__":
    unittest.main()
