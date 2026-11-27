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


class TestPrePush(unittest.TestCase):
    """--pre-push: solo i gate bloccanti e veloci, quelli che il hook lancia a ogni push."""

    def setUp(self):
        self.ci = Path(tempfile.mkdtemp()) / "ci.yml"
        self.ci.write_text(CI_FINTA + """      - name: Un gate lento
        run: python scripts/lento.py
      - name: I test
        run: python -m pytest -q scripts/tests
""", encoding="utf-8")

    def _stato(self, **kw):
        elenco = G.passi(self.ci, base="mio-ramo")
        G.filtra(elenco, lenti={"Un gate lento": (60, "rende i booklet")}, **kw)
        return {v["nome"]: v["salta"] for v in elenco}

    def test_pre_push_tiene_solo_i_gate_bloccanti_e_veloci(self):
        s = self._stato(pre_push=True)
        self.assertIsNone(s["Un gate"])
        self.assertIsNone(s["La disciplina dei piani"])
        self.assertEqual(s["Un avviso"], "--pre-push: non bloccante")
        self.assertEqual(s["Un gate lento"], "--pre-push: lento (60 s, rende i booklet)")
        self.assertEqual(s["I test"], "--rapido")

    def test_senza_pre_push_il_lento_e_l_avviso_girano(self):
        s = self._stato()
        self.assertIsNone(s["Un gate lento"])
        self.assertIsNone(s["Un avviso"])
        self.assertIsNone(s["I test"])

    def test_ogni_lento_dichiarato_esiste_in_ci_e_ha_tempo_e_motivo(self):
        nomi = {v["nome"] for v in G.passi()}
        for nome, (secondi, motivo) in G.LENTI.items():
            self.assertIn(nome, nomi, f"LENTI cita un passo che ci.yml non ha più: {nome}")
            self.assertGreater(secondi, 0)
            self.assertTrue(motivo.strip())


class TestPromozioniDelCanaleTesting(unittest.TestCase):
    """Le promozioni testing → stable del 2026-11-25 (ADR-0099): il passo promosso
    blocca (niente continue-on-error), e il passo che aveva solo il ruolo di
    canale esce. Ogni prova è di una candidata sola, per toglierla da sola."""

    def _passo(self, comando):
        trovati = [v for v in G.passi() if comando in v["run"]]
        self.assertEqual(len(trovati), 1, f"in ci.yml un solo passo con «{comando}»")
        return trovati[0]

    def test_il_cancello_dei_numeri_blocca(self):          # ADR-0118
        self.assertFalse(self._passo("conformita_statblocchi.py --cancello-numeri")["avviso"])

    def test_le_marche_sulle_righe_cambiate_bloccano(self):  # ADR-0109
        self.assertFalse(self._passo("controlla_marche.py")["avviso"])

    def test_la_d_eufonica_non_ha_piu_un_passo_suo(self):   # ADR-0120
        self.assertEqual([v["nome"] for v in G.passi() if "--d-eufonica" in v["run"]], [])
        self.assertFalse(self._passo("validate_lingua.py")["avviso"])


if __name__ == "__main__":
    unittest.main()
