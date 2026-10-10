"""gate_locale.py: i passi vengono da ci.yml, e quelli che qui non hanno senso si saltano dicendolo."""

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import gate_locale as G  # noqa: E402

CI_FINTA = """
jobs:
  validate:
    steps:
      - uses: actions/checkout@v4
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Un gate
        run: python scripts/qualcosa.py --check
      - name: Un avviso
        continue-on-error: true
        run: python scripts/rumoroso.py
      - name: La disciplina dei piani
        if: github.event_name == 'pull_request'
        run: python scripts/check_plans_discipline.py --base "origin/${{ github.base_ref }}"
      - name: Solo sui push
        if: github.event_name == 'push'
        run: echo push
      - name: Un segreto
        run: echo ${{ secrets.TOKEN }}
"""


class TestPassi(unittest.TestCase):
    def setUp(self):
        self.ci = Path(tempfile.mkdtemp()) / "ci.yml"
        self.ci.write_text(CI_FINTA, encoding="utf-8")
        self.passi = {p["nome"]: p for p in G.passi(self.ci, base="mio-ramo")}

    def test_i_passi_uses_non_ci_sono(self):
        self.assertEqual(len(self.passi), 6)

    def test_chi_installa_si_salta(self):
        self.assertEqual(self.passi["Install dependencies"]["salta"], "installa")

    def test_continue_on_error_e_un_avviso(self):
        self.assertTrue(self.passi["Un avviso"]["avviso"])
        self.assertFalse(self.passi["Un gate"]["avviso"])

    def test_la_condizione_sulla_pr_vale_anche_qui_col_ramo_base(self):
        p = self.passi["La disciplina dei piani"]
        self.assertIsNone(p["salta"])
        self.assertIn('--base "origin/mio-ramo"', p["run"])

    def test_altre_condizioni_e_altre_espressioni_si_saltano(self):
        self.assertIn("condizione", self.passi["Solo sui push"]["salta"])
        self.assertIn("secrets.TOKEN", self.passi["Un segreto"]["salta"])

    def test_uno_strumento_installato_da_un_passo_saltato_e_assente_si_riconosce(self):
        elenco = [{"nome": "Install strumentoinesistente (versione fissata)", "salta": "installa"},
                  {"nome": "Install dependencies", "salta": "installa"},
                  {"nome": "Install bash", "salta": "installa"}]
        self.assertEqual(G.mancanti(elenco), {"strumentoinesistente"})

    def test_la_ci_vera_si_legge(self):
        nomi = [p["nome"] for p in G.passi()]
        self.assertTrue(any("misura_resa" in n for n in nomi))


if __name__ == "__main__":
    unittest.main()
