"""Il cricchetto della prosa: sui file di gioco cambiati nessuna norma MQM peggiora (ADR-0146)."""
from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cricchetto_prosa as cp  # noqa: E402

BOX_CORTO = "> *Il vento porta cenere dalla valle.*\n"
BOX_LUNGO = "".join(f"> *Riga {i} del box che non finisce mai.*\n" for i in range(14))
STATBLOCK = "**CA** 18\n**pf** 45 (6d10+12)\n"
SCHEDA = "Bestiario/mostri/x.md"
RECAP = "campaign/recaps/r.md"


class TestCricchetto(unittest.TestCase):
    def test_box_oltre_tetto_aggiunto_peggiora(self) -> None:
        self.assertIn("box_oltre_12_righe",
                      cp.confronta(SCHEDA, STATBLOCK, STATBLOCK + "\n" + BOX_LUNGO))

    def test_box_corto_aggiunto_non_peggiora(self) -> None:
        self.assertEqual(cp.confronta(SCHEDA, STATBLOCK, STATBLOCK + "\n" + BOX_CORTO), {})

    def test_misto_senza_prosa_nuova_non_si_controlla(self) -> None:
        prima = BOX_LUNGO + "\n" + STATBLOCK
        dopo = BOX_LUNGO + "\n" + STATBLOCK.replace("45", "52")
        self.assertFalse(cp.da_controllare(SCHEDA, prima, dopo))

    def test_prosa_pura_si_controlla_sempre(self) -> None:
        self.assertTrue(cp.da_controllare(RECAP, "a\n", "b\n"))

    def test_misto_con_box_nuovo_si_controlla(self) -> None:
        self.assertTrue(cp.da_controllare(SCHEDA, STATBLOCK, STATBLOCK + BOX_CORTO))

    def test_file_nuovo_confronta_col_vuoto(self) -> None:
        self.assertIn("box_oltre_12_righe", cp.confronta(RECAP, None, BOX_LUNGO))

    def test_un_difetto_tolto_e_due_aggiunti_si_vede(self) -> None:
        dopo = BOX_CORTO + "\n" + BOX_LUNGO + "\n" + BOX_LUNGO
        self.assertEqual(cp.confronta(RECAP, BOX_LUNGO, dopo)["box_oltre_12_righe"], (1, 2))

    def test_esce_1_solo_se_qualcosa_peggiora(self) -> None:
        casi = (([(RECAP, BOX_CORTO, BOX_LUNGO)], 1), ([(RECAP, BOX_LUNGO, BOX_CORTO)], 0), ([], 0))
        for coppie, atteso in casi:
            with self.subTest(atteso=atteso), mock.patch.object(cp, "coppie", return_value=coppie), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cp.main(["--rispetto-a", "origin/main"]), atteso)


if __name__ == "__main__":
    unittest.main()
