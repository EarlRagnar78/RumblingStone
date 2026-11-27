"""Gli indicatori adottati dalla seconda tornata (RICERCA-GUARDRAIL §8):
ripetizioni fra box frase per frase e box «telecomando» al plurale."""
from __future__ import annotations

import doctest
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import misura_box_telecomando as tel  # noqa: E402
import misura_ripetizioni_frasi as rip  # noqa: E402


class TestRipetizioni(unittest.TestCase):

    FR = [("DEF-5.md", 0, "Il rosso vi stringe in un filo tirato attraverso mille anni, e non fa male."),
          ("ARC08-11.md", 3, "Il rosso vi tira attraverso le ere, non c'è dolore, solo vertigine."),
          ("ARC08-15-HANDOUTS-GIOCATORE.md", 1, "Sei la migliore esploratrice di Hammerfist, occhi acuti come lame."),
          ("ARC08-01.md", 2, "Sei la migliore esploratrice di Hammerfist, una nana dagli occhi acuti come lame.")]

    def test_la_parafrasi_resta_l_handout_no(self):
        sim = [[1, .83, .1, .1], [.83, 1, .1, .1], [.1, .1, 1, .95], [.1, .1, .95, 1]]
        c = rip.coppie(self.FR, sim, 0.80)
        self.assertEqual([(x["a"], x["b"]) for x in c], [("DEF-5.md", "ARC08-11.md")])

    def test_sotto_soglia_niente(self):
        sim = [[1, .79, 0, 0], [.79, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        self.assertEqual(rip.coppie(self.FR, sim, 0.80), [])

    def test_la_copia_la_vedono_gia_i_quattro_grammi(self):
        a = ("A.md", 0, "il vento tra le lame crea una melodia triste ma orgogliosa")
        b = ("B.md", 0, "il vento tra le lame crea una melodia triste ma fiera")
        self.assertFalse(rip.tieni(a, b))

    def test_senza_modello_esce_con_due(self):
        import builtins
        vero = builtins.__import__

        def finto(nome, *a, **k):
            if nome == "sentence_transformers":
                raise ImportError(nome)
            return vero(nome, *a, **k)
        builtins.__import__ = finto
        try:
            self.assertEqual(rip.main([]), 2)
        finally:
            builtins.__import__ = vero

    def test_la_soglia_e_un_coseno(self):
        for x in ("1.5", "-2", "nan"):
            with self.assertRaises(SystemExit):
                rip.main(["--soglia", x])

    def test_doctest(self):
        self.assertEqual(doctest.testmod(rip).failed, 0)


class TestTelecomando(unittest.TestCase):

    def test_il_plurale_che_decide_per_il_gruppo(self):
        self.assertEqual(tel.colpi("> *Sorride, e capite che lui ne guadagnerà.*"), ["capite"])
        self.assertEqual(tel.colpi("> *Anche se sapete che è stata qui per millenni.*"), ["sapete"])

    def test_il_singolare_e_l_eco_personale(self):
        # la prima configurazione: 13 falsi su 15 erano echi per un PG
        self.assertEqual(tel.colpi("> *La ricordi coperta del sangue di Hella, e capisci.*"), [])

    def test_voi_da_la_scelta(self):
        self.assertEqual(tel.colpi("> *Quale rumore lo sapete voi.*"), [])

    def test_anche_voi_che_resta_un_colpo(self):
        self.assertEqual(tel.colpi("> *Capite anche voi che non c'è ritorno.*"), ["capite"])
        self.assertEqual(tel.colpi("> *Sapete voi che cosa vuole.*"), ["sapete"])

    def test_le_battute_dei_png_no(self):
        self.assertEqual(tel.colpi("> *«Capite che non tornerò» dice Durin.*"), [])

    def test_il_cancello_sul_repo(self):
        # 2026-11-03: i 2 veri corretti nel testo, restano i 2 accettati. Un
        # box nuovo che dice al gruppo cosa capisce boccia la CI.
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            esito = tel.main(["--check"])
        self.assertEqual(esito, 0, buf.getvalue())

    def test_il_cancello_boccia_un_colpo_nuovo(self):
        import io
        import tempfile
        from contextlib import redirect_stdout
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "NUOVO.md"
            f.write_text("> *Sorride, e capite che lui ne guadagnerà.*\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(tel.main(["--check", str(f)]), 1)

    def test_doctest(self):
        self.assertEqual(doctest.testmod(tel).failed, 0)


if __name__ == "__main__":
    unittest.main()
