"""La vista di chi scorre: il DM a freddo vede il master come chi lo sfoglia.

L5 di PIANO-AGENT-SKILLS-ESTERNE (D2 del 2026-10-01). I test fissano le cose
che la vista promette: la serata dichiarata in testa, la prima frase di ogni
scena e non il suo corpo, le CD con le parole che le precedono, e un master
che non dichiara la serata lo dice invece di tacere.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))


def _modulo():
    spec = importlib.util.spec_from_file_location("vista_di_chi_scorre", ROOT / "scripts" / "vista_di_chi_scorre.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V = _modulo()

MASTER = """# ARC-99 · DEF-1 — Prova

## §0 — QUICKSTART DM

> 🧭 **La serata in tre frasi.** I PG difendono il guado. All'alba arriva il
> capitano nemico. Se il guado cade, il villaggio brucia.

Testo del quickstart.

### SCENA 1 — Il guado

**In scena** — Dove: il guado — Chi: la sentinella

Il fiume corre basso sotto la luna. SEGRETO-DEL-CORPO che chi scorre non vede.

Una prova di Nuotare CD 15 per attraversare.

### SCENA 2 — L'alba

| Tabella | non è prosa |
|---|---|

Il capitano arriva con venti uomini. Altro testo nascosto.
"""


class TestVista(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.master = Path(self.tmp.name) / "ARC99-DEF-1-PROVA.md"
        self.master.write_text(MASTER, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_la_serata_dal_riquadro(self):
        v = V.vista(self.master)
        self.assertIn("riquadro", v["serata"]["fonte"])
        self.assertIn("difendono il guado", v["serata"]["testo"])

    def test_la_prima_frase_e_non_il_corpo(self):
        v = V.vista(self.master)
        self.assertEqual([s["titolo"] for s in v["scene"]], ["SCENA 1 — Il guado", "SCENA 2 — L'alba"])
        self.assertEqual(v["scene"][0]["prima_frase"], "Il fiume corre basso sotto la luna.")
        self.assertNotIn("SEGRETO-DEL-CORPO", V.in_chiaro(v))

    def test_la_riga_in_scena_resta_a_parte(self):
        s = V.vista(self.master)["scene"][0]
        self.assertTrue(s["in_scena"].startswith("In scena — Dove: il guado"))

    def test_salta_le_tabelle(self):
        self.assertTrue(V.vista(self.master)["scene"][1]["prima_frase"].startswith("Il capitano arriva"))

    def test_la_cd_porta_le_parole_prima(self):
        cd = V.vista(self.master)["cd"]
        self.assertEqual(cd[0]["cd"], 15)
        self.assertIn("Nuotare", cd[0]["prima"])

    def test_senza_serata_lo_dice(self):
        self.master.write_text("# Titolo\n\n### SCENA 1 — Sola\n\nUna frase.\n", encoding="utf-8")
        self.assertIn("LA SERATA: il master non la dichiara", V.in_chiaro(V.vista(self.master)))

    def test_i_master_veri_hanno_tutti_una_prima_frase(self):
        for f in sorted((ROOT / "07_il Portale Della Forgia Eterna").glob("ARC07-DEF-*.md")):
            v = V.vista(f)
            self.assertTrue(v["scene"], f.name)
            vuote = [s["titolo"] for s in v["scene"] if not s["prima_frase"]]
            self.assertEqual(vuote, [], f.name)


if __name__ == "__main__":
    unittest.main()
