"""Il registro delle letture a freddo: avviso finche' manca l'impronta, poi blocca da solo.

L4 di PIANO-AGENT-SKILLS-ESTERNE (D26 di PIANO-LETTORE, D4 del 2026-10-01).
Ogni test costruisce un repo finto con un master e il suo registro, e guarda
il cancello dal lato che morde: un master sotto cancello che cambia, un 🟠
senza stato, una «sola forma» che copre il cambio, un master nuovo che non
rimette in avviso gli altri.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _modulo():
    spec = importlib.util.spec_from_file_location("registro_letture", ROOT / "scripts" / "registro_letture.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _sha(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


class TestRegistroVero(unittest.TestCase):
    def test_il_registro_del_repo_passa_oggi(self):
        self.assertEqual(_modulo().main(["--check"]), 0)


class TestCancello(unittest.TestCase):
    TESTO = "# Master\n\n### SCENA 1 — Una porta\n\nTesto.\n"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "arco").mkdir()
        self.rel = "arco/ARC99-DEF-1-PROVA.md"
        (self.root / self.rel).write_text(self.TESTO, encoding="utf-8")
        self.RL = _modulo()
        self.RL.ROOT = self.root
        self.RL.REGISTRO = self.root / "registro.json"

    def tearDown(self):
        self.tmp.cleanup()

    def _registro(self, rilievi=None, sola_forma=None, impronta="ok", ruoli=("lettore", "playtester", "dm")):
        imp = _sha(self.TESTO) if impronta == "ok" else impronta
        letture = [{"ruolo": r, "data": "2026-10-01", "impronta": imp, "rilievi": rilievi or []}
                   for r in ruoli]
        dati = {"master": {self.rel: {"letture": letture, "sola_forma": sola_forma or []}}}
        self.RL.REGISTRO.write_text(json.dumps(dati), encoding="utf-8")

    def test_senza_il_dm_a_freddo_resta_in_avviso(self):
        # D9 del 2026-10-01: il DM a freddo e' il terzo ruolo obbligatorio
        self._registro(ruoli=("lettore", "playtester"))
        (self.root / self.rel).write_text(self.TESTO + "Un refuso corretto.\n", encoding="utf-8")
        self.assertEqual(self.RL.main(["--check"]), 0)

    def test_allineato_passa(self):
        self._registro()
        self.assertEqual(self.RL.main(["--check"]), 0)

    def test_master_cambiato_dopo_la_lettura_morde(self):
        self._registro()
        (self.root / self.rel).write_text(self.TESTO + "Un refuso corretto.\n", encoding="utf-8")
        self.assertEqual(self.RL.main(["--check"]), 1)

    def test_la_sola_forma_copre_il_cambio(self):
        self._registro()
        nuovo = self.TESTO + "Un refuso corretto.\n"
        (self.root / self.rel).write_text(nuovo, encoding="utf-8")
        self.assertEqual(self.RL.main(["--sola-forma", self.rel, "--ragione", "un refuso"]), 0)
        self.assertEqual(self.RL.main(["--check"]), 0)

    def test_un_arancio_senza_stato_morde(self):
        self._registro(rilievi=[{"n": 3, "gravita": "🟠", "stato": None}])
        self.assertEqual(self.RL.main(["--check"]), 1)

    def test_un_residuo_senza_ragione_morde_e_con_ragione_passa(self):
        self._registro(rilievi=[{"n": 3, "gravita": "🟠", "stato": "residuo"}])
        self.assertEqual(self.RL.main(["--check"]), 1)
        self._registro(rilievi=[{"n": 3, "gravita": "🟠", "stato": "residuo", "ragione": "è canone"}])
        self.assertEqual(self.RL.main(["--check"]), 0)

    def test_senza_impronta_e_avviso_non_blocco(self):
        self._registro(rilievi=[{"n": 3, "gravita": "🔴", "stato": None}], impronta=None)
        self.assertEqual(self.RL.main(["--check"]), 0)

    def test_un_master_nuovo_senza_letture_non_rimette_in_avviso_gli_altri(self):
        self._registro()
        (self.root / "arco" / "ARC99-DEF-2-NUOVO.md").write_text("# Nuovo\n", encoding="utf-8")
        (self.root / self.rel).write_text(self.TESTO + "cambiato\n", encoding="utf-8")
        self.assertEqual(self.RL.main(["--check"]), 1)

    def test_non_si_registra_la_lettura_di_un_altro_testo(self):
        self._registro()
        corsa = self.root / "corsa" / "lettore"
        corsa.mkdir(parents=True)
        (corsa / "stato.json").write_text(json.dumps({"impronta_master": _sha("altro"), "smesso_a": None}),
                                          encoding="utf-8")
        self.assertEqual(self.RL.main(["--registra", self.rel, "--ruolo", "lettore", "--corsa", str(corsa)]), 1)

    def test_il_confronto_mette_le_due_letture_affiancate(self):
        a, b = self.root / "a", self.root / "b"
        for cartella, ago in ((a, "-1"), (b, "+2")):
            cartella.mkdir()
            (cartella / "diario.jsonl").write_text(json.dumps(
                {"titolo": "SCENA 1", "diario": f"ago={ago} | …", "smesso": False}) + "\n", encoding="utf-8")
        uscita = self.RL.confronta(a, b)
        self.assertIn("SCENA 1", uscita)
        self.assertIn("-1", uscita)
        self.assertIn("+2", uscita)


if __name__ == "__main__":
    unittest.main()
