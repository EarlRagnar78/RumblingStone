"""misura_sintassi: i calchi di Cerruti e i tratti sintattici con spaCy.

Le prove che chiedono il parser saltano se spaCy o `it_core_news_md` mancano;
quelle sulla degradazione e sull'estrazione dei box girano sempre.
"""

import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import misura_sintassi as M  # noqa: E402

NLP = M.carica_nlp()


class TestSenzaParser(unittest.TestCase):
    def test_senza_spacy_salta_ed_esce_zero(self):
        out = io.StringIO()
        with mock.patch.object(M, "carica_nlp", return_value=None), redirect_stdout(out):
            self.assertEqual(M.main([]), 0)
        self.assertIn("misura saltata", out.getvalue())

    def test_file_assente_esce_due(self):
        with redirect_stderr(io.StringIO()):
            self.assertEqual(M.main(["--file", "/non/esiste.md"]), 2)

    def test_box_con_riga(self):
        testo = "# T\n\n> *Un box.*\n> *Seconda riga.*\n\ntesto\n\n> **Nota** no\n\n> *Altro box qui.*\n"
        self.assertEqual(M.box_con_riga(testo),
                         [(3, "Un box. Seconda riga."), (10, "Altro box qui.")])


@unittest.skipUnless(NLP, "spaCy o it_core_news_md assenti")
class TestCalchi(unittest.TestCase):
    def a(self, testo):
        return M.analizza(testo, NLP)

    def test_soggetto_preverbale_indefinito(self):
        self.assertEqual(self.a("Un campanello suonò nel buio.")["sogg_preverbale"], 1)
        self.assertEqual(self.a("Nel buio suonò un campanello.")["sogg_preverbale"], 0)

    def test_soggetto_definito_non_conta(self):
        self.assertEqual(self.a("Il campanello suonò nel buio.")["sogg_preverbale"], 0)

    def test_anticausativo_con_si(self):
        self.assertEqual(self.a("Una porta si apre sulla sinistra.")["sogg_preverbale"], 1)

    def test_stare_gerundio_anche_al_passato(self):
        self.assertEqual(self.a("Il nano stava camminando nel buio.")["stare_gerundio"], 1)
        self.assertEqual(self.a("Il nano cammina nel buio.")["stare_gerundio"], 0)

    def test_aggettivo_complesso_anteposto(self):
        self.assertGreaterEqual(self.a("Una molto antica pietra giace qui.")["agg_complesso"], 1)
        self.assertEqual(self.a("La più antica pietra giace qui.")["agg_complesso"], 0)

    def test_pronome_soggetto_e_focus(self):
        self.assertEqual(self.a("Lui si voltò verso la porta.")["pron_soggetto"], 1)
        self.assertEqual(self.a("Anche lui si voltò verso la porta.")["pron_soggetto"], 0)

    def test_pronome_fuori_dal_totale(self):
        m = self.a("Lui si voltò verso la porta.")
        self.assertEqual(m["calchi"], 0)

    def test_possessivi_dalla_regex_di_validate_prosa(self):
        self.assertEqual(self.a("Alzò la sua mano verso il cielo.")["possessivi_corpo"], 1)


@unittest.skipUnless(NLP, "spaCy o it_core_news_md assenti")
class TestTratti(unittest.TestCase):
    def test_livelli_di_subordinate(self):
        semplice = M.analizza("La sala è buia. Il fuoco è spento.", NLP)
        self.assertEqual(semplice["livelli_max"], 0)
        incassata = M.analizza("Vedi la sala che il fuoco ha annerito quando la montagna "
                               "crollò perché i nani avevano scavato troppo.", NLP)
        self.assertGreaterEqual(incassata["livelli_max"], 2)

    def test_misure_numeriche(self):
        m = M.analizza("La pietra è fredda. La pietra è antica e la pietra canta.", NLP)
        self.assertGreater(m["rip_interna%"], 0)
        self.assertTrue(0 < m["mattr_lemmi"] <= 1)
        self.assertGreater(m["lungh_dip"], 0)
        self.assertGreaterEqual(m["profondita_max"], 1)

    def test_file_e_ripetizione_fra_box(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("> *La pietra canta nel buio.*\n\nx\n\n> *La pietra tace nel buio.*\n")
        try:
            d = M.misura_file(Path(f.name), NLP)
        finally:
            Path(f.name).unlink()
        self.assertEqual(d["box"], 2)
        self.assertGreater(d["per_box"][0]["rip_fra_box%"], 0)
        self.assertIn("calchi_per_1000_parole", d["medie"])


if __name__ == "__main__":
    unittest.main()
