"""`dm.py sistemi`: i sistemi di gioco da un solo ingresso (ADR-0111, ADR-0002).

Il sottocomando non ha logica: passa i flag a `scripts/sistemi.py`. Quindi si
prova che non si metta in mezzo: stesso aiuto, stesso risultato, stesso codice
d'uscita dello script, e che il manifest dei tool lo conosca.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _esegui(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=REPO)


class TestNonSiMetteInMezzo(unittest.TestCase):
    def test_l_aiuto_e_quello_dello_script(self):
        diretto = _esegui("scripts/sistemi.py", "--help")
        via_dm = _esegui("scripts/dm.py", "sistemi", "--help")
        self.assertEqual(via_dm.returncode, diretto.returncode)
        self.assertEqual(via_dm.stdout, diretto.stdout)
        self.assertIn("usage: sistemi.py", via_dm.stdout)

    def test_il_sistema_di_un_file(self):
        # il Drappo è PF1e in sistemi.toml, un file fuori da [moduli] è il predefinito
        for percorso in ("10-stand-alone/Il-Drappo-di-Tarsilia/README.md", "README.md"):
            with self.subTest(percorso=percorso):
                diretto = _esegui("scripts/sistemi.py", "--di", percorso)
                via_dm = _esegui("scripts/dm.py", "sistemi", "--di", percorso)
                self.assertEqual(via_dm.returncode, 0)
                self.assertEqual(via_dm.stdout, diretto.stdout)
        self.assertEqual(_esegui("scripts/dm.py", "sistemi", "--di",
                                 "10-stand-alone/Il-Drappo-di-Tarsilia/README.md").stdout.strip(),
                         "pf1e")

    def test_il_codice_d_uscita_passa(self):
        # un flag che sistemi.py non conosce: argparse esce 2, e dm.py con lui
        diretto = _esegui("scripts/sistemi.py", "--nessuno")
        via_dm = _esegui("scripts/dm.py", "sistemi", "--nessuno")
        self.assertEqual(diretto.returncode, 2)
        self.assertEqual(via_dm.returncode, diretto.returncode)

    def test_la_riga_del_tramite_va_su_stderr(self):
        # chi legge --json da stdout non deve trovarci «[dm] → …»
        via_dm = _esegui("scripts/dm.py", "sistemi", "--json")
        self.assertEqual(via_dm.returncode, 0)
        json.loads(via_dm.stdout)
        self.assertIn("[dm] → ", via_dm.stderr)


class TestRegistrazione(unittest.TestCase):
    def test_sistemi_e_nel_manifest_dei_tool(self):
        d = json.loads((REPO / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
        dm_t = next(t for t in d["tools"] if t["id"] == "dm")
        self.assertIn("sistemi", dm_t["args"][0]["choices"])

    def test_ogni_sottocomando_di_dm_e_nel_manifest(self):
        # un sottocomando che il manifest non conosce è invisibile al server MCP
        sys.path.insert(0, str(REPO / "scripts"))
        import argparse

        import dm  # noqa: PLC0415

        catturati: list[str] = []
        originale = argparse._SubParsersAction.add_parser

        def spia(self, name, **kw):
            catturati.append(name)
            return originale(self, name, **kw)

        argparse._SubParsersAction.add_parser = spia
        try:
            with self.assertRaises(SystemExit):
                dm.main(["--version"])
        finally:
            argparse._SubParsersAction.add_parser = originale
        d = json.loads((REPO / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
        scelte = set(next(t for t in d["tools"] if t["id"] == "dm")["args"][0]["choices"])
        self.assertTrue(catturati)
        self.assertEqual(set(catturati) - scelte, set())


if __name__ == "__main__":
    unittest.main()
