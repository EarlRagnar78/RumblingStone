"""L'eco di un blocco di decisioni: il rilevatore e i suoi confini.

L9 di PIANO-AGENT-SKILLS-ESTERNE (D6 del 2026-10-01). Fissano quando la norma
scatta (due o piu' chiusure nella stessa data, da DATA_INIZIO in poi), cosa
chiede (il marker e i quattro campi) e cosa non tocca (le chiusure di prima).
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import eco_decisioni as E  # noqa: E402

TABELLA = """# Piano finto

<!-- decisioni-dm: FINTO -->

| # | Lotto | Domanda |
|---|---|---|
| ~~D1~~ | L1 | ✅ **Decisa il {d1}**: sì. Era: **Uno?** |
| ~~D2~~ | L2 | ✅ **Decisa il {d2}**: no. Era: **Due?** |
| D3 | L3 | **Tre?** |

{eco}
"""

ECO = """<!-- eco: FINTO 2026-10-02 -->
- **Decise**: D1, D2
- **Aperte**: D3
- **Cambiate**: nessuna
- **Dedotto da me**: niente
"""


class TestEco(unittest.TestCase):
    def _radice(self, d1="2026-10-02", d2="2026-10-02", eco=""):
        self.tmp = tempfile.TemporaryDirectory()
        r = Path(self.tmp.name)
        (r / "plans").mkdir()
        (r / "plans" / "PIANO-FINTO.md").write_text(TABELLA.format(d1=d1, d2=d2, eco=eco), encoding="utf-8")
        return r

    def tearDown(self):
        self.tmp.cleanup()

    def test_due_chiusure_senza_eco_bocciano(self):
        problemi, _, _ = E.esamina(self._radice())
        self.assertEqual(len(problemi), 1)
        self.assertIn("manca", problemi[0])
        self.assertEqual(E.main(["--check", "--radice", self.tmp.name]), 1)

    def test_con_l_eco_passa(self):
        problemi, a_posto, _ = E.esamina(self._radice(eco=ECO))
        self.assertEqual(problemi, [])
        self.assertEqual(len(a_posto), 1)

    def test_un_campo_mancante_si_nomina(self):
        problemi, _, _ = E.esamina(self._radice(eco=ECO.replace("- **Dedotto da me**: niente\n", "")))
        self.assertIn("Dedotto da me", problemi[0])

    def test_una_chiusura_sola_non_chiede_eco(self):
        problemi, a_posto, _ = E.esamina(self._radice(d2="2026-10-03"))
        self.assertEqual((problemi, a_posto), ([], []))

    def test_prima_della_norma_si_conta_e_non_blocca(self):
        problemi, _, prima = E.esamina(self._radice(d1="2026-09-30", d2="2026-09-30"))
        self.assertEqual((problemi, prima), ([], 1))

    def test_l_eco_di_un_altra_data_non_vale(self):
        problemi, _, _ = E.esamina(self._radice(eco=ECO.replace("2026-10-02 -->", "2026-10-05 -->")))
        self.assertEqual(len(problemi), 1)


class TestRepo(unittest.TestCase):
    def test_il_repo_ha_le_sue_eco(self):
        self.assertEqual(E.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
