"""La regola di degradazione pulita: se il binario manca, si esce PRIMA di scrivere.

Il difetto che questi test esistono per impedire non è un crash: è un PDF di 40
pagine su 96, scritto a metà e indistinguibile da uno buono finché non lo si
apre. Per questo `esigi()` deve alzare `SystemExit` — non ritornare `None` a un
chiamante che poi decide, perché è nel «poi decide» che il file di destinazione
è già stato aperto.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import io
import re
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import binari  # noqa: E402


class TestEsigi(unittest.TestCase):
    def test_se_manca_esce_con_MANCA_e_non_ritorna(self):
        err = io.StringIO()
        with mock.patch.object(binari.shutil, "which", return_value=None):
            with self.assertRaises(SystemExit) as cm, redirect_stderr(err):
                binari.esigi(binari.PDFCPU)
        self.assertEqual(cm.exception.code, binari.MANCA)
        self.assertNotEqual(binari.MANCA, 1, "MANCA deve restare distinto da «ho provato e fallito»")

    def test_se_c_e_ritorna_il_percorso_e_non_stampa_niente(self):
        err = io.StringIO()
        with mock.patch.object(binari.shutil, "which", return_value="/usr/local/bin/pdfcpu"):
            with redirect_stderr(err):
                self.assertEqual(binari.esigi(binari.PDFCPU), "/usr/local/bin/pdfcpu")
        self.assertEqual(err.getvalue(), "")

    def test_trova_non_esce_mai(self):
        # `stato()` e `dm.py doctor` devono poter guardare senza morire.
        with mock.patch.object(binari.shutil, "which", return_value=None):
            self.assertIsNone(binari.trova(binari.TYPST))
            self.assertEqual([p for _, p in binari.stato()], [None] * len(binari.TUTTI))


class TestMessaggio(unittest.TestCase):
    def test_dice_le_tre_cose(self):
        # nome, come installarlo, e cosa resta possibile senza.
        for b in binari.TUTTI:
            m = binari.messaggio(b)
            self.assertIn(f"«{b.nome}»", m, f"{b.nome}: il messaggio non nomina il binario")
            self.assertIn(b.installa.strip().splitlines()[0].strip(), m,
                          f"{b.nome}: il messaggio non dice come installarlo")
            self.assertIn(b.ripiego, m, f"{b.nome}: il messaggio non dice cosa resta possibile")

    def test_ogni_binario_cita_il_suo_adr_e_l_adr_esiste(self):
        # Una dipendenza binaria senza ADR è una dipendenza entrata di nascosto.
        for b in binari.TUTTI:
            self.assertRegex(b.adr, r"^ADR-\d{4}$")
            trovati = list((REPO / "plans" / "adr").glob(f"{b.adr}-*.md"))
            self.assertTrue(trovati, f"{b.nome} cita {b.adr}, che non esiste in plans/adr/")
            self.assertIn(b.adr, binari.messaggio(b))

    def test_licenza_dichiarata_e_aperta(self):
        for b in binari.TUTTI:
            self.assertIn(b.licenza, ("Apache-2.0", "MIT", "BSD-3-Clause"),
                          f"{b.nome}: licenza {b.licenza} non è fra quelle accettate")


class TestUsoNegliScript(unittest.TestCase):
    def test_l_exporter_usa_la_regola_condivisa_e_non_una_sua_copia(self):
        # Con due copie della regola diventano due regole, e una delle due
        # invecchia in silenzio.
        src = (REPO / "scripts" / "export_booklet_typst.py").read_text(encoding="utf-8")
        self.assertIn("binari.esigi(binari.TYPST)", src)
        self.assertNotRegex(src, r'shutil\.which\(\s*"typst"',
                            "l'exporter ha di nuovo una sua copia della ricerca del binario")

    def test_nessuno_script_cerca_pdfcpu_a_mano(self):
        for f in (REPO / "scripts").glob("*.py"):
            if f.name == "binari.py":
                continue
            src = f.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r'which\(\s*["\']pdfcpu', src),
                              f"{f.name} cerca pdfcpu senza passare da binari.esigi()")


if __name__ == "__main__":
    unittest.main()
