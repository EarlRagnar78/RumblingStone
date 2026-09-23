"""L'impronta delle creature: il collaudo del lotto E di PIANO-QUALITA-DEL-CODICE.

Il lotto sposta in `dmcore/` codice che decide numeri (il lettore delle schede,
la base dei TS, la scelta delle caratteristiche). Uno spostamento non cambia
niente, e questo test lo verifica: rigenera l'impronta di
`scripts/impronta_creature.py` e la confronta con quella committata.

⚠️ **L'impronta non si rigenera mai per far passare questo test** (§8.5). Se
cade, lo spostamento ha cambiato un comportamento, e il messaggio dice su quale
scheda e su quale lettura. Si rigenera solo in un commit suo, che dice quali
chiavi cambiano e perche' (il sotto-lotto E6, se D2 cambia una tabella).
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import impronta_creature as I  # noqa: E402


class TestImprontaCreature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ora = I.testo(I.impronta())

    def test_identica_alla_fixture(self):
        committata = I.FIXTURE.read_text(encoding="utf-8")
        if self.ora == committata:
            return
        diff = I.differenze(json.loads(committata), json.loads(self.ora))
        self.fail("l'impronta delle creature e' cambiata:\n  " + "\n  ".join(diff))

    def test_deterministica(self):
        """Due esecuzioni nello stesso processo danno lo stesso testo: senza,
        un confronto rosso non direbbe se ha cambiato il codice o l'orologio."""
        self.assertEqual(self.ora, I.testo(I.impronta()))

    def test_copre_quello_che_promette(self):
        d = json.loads(self.ora)
        self.assertGreaterEqual(len(d["bestiario"]), 100)
        self.assertEqual(len(d["creature"]), 20 * len(I.GC.RUOLI) * len(I.FORME) * 2)
        con_letture = [v for v in d["bestiario"].values() if "letture" in v]
        self.assertGreaterEqual(len(con_letture), 100)
        self.assertTrue(any(v["letture"]["tetti_dai_ts"] for v in con_letture))
        self.assertTrue(any("con_attributi" in v for v in d["apply_ts"].values()))

    def test_differenze_nomina_la_chiave(self):
        vecchia = {"a": {"b": [1, 2], "c": 3}}
        nuova = {"a": {"b": [1, 5], "c": 3, "d": 0}}
        self.assertEqual(I.differenze(vecchia, nuova), ["/a/b[1]: 2 → 5", "/a/d: nuova"])


if __name__ == "__main__":
    unittest.main()
