"""I rimandi con il numero di pagina (ADR-0144).

Tre livelli: il traduttore dei rimandi (`dmcore.testo`), l'esportatore che
accoda `#rif-pagina` (`export_booklet_typst.numera_rimandi`) e il tema che lo
risolve in «, p. N». I casi vengono dal booklet della serata di ARC-07, dove
su main 8 rimandi su 107 puntavano a un titolo che nel capitolo non c'era.
"""

import doctest
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import export_booklet_typst as E  # noqa: E402
from dmcore import testo  # noqa: E402


class TestDoctest(unittest.TestCase):
    def test_doctest_dei_due_moduli(self):
        for modulo in (testo, E):
            esito = doctest.testmod(modulo, verbose=False)
            self.assertEqual(esito.failed, 0, modulo.__name__)


class TestNumeraRimandi(unittest.TestCase):
    def test_scena_e_paragrafo(self):
        out = E.numera_rimandi("vedi cap. V Scena 6, poi il §13 del capitolo III.")
        self.assertIn('#rif-pagina("V", "SCENA 6");', out)
        self.assertIn('#rif-pagina("III", "§13");', out)

    def test_dentro_una_stringa_non_tocca(self):
        self.assertEqual(E.numera_rimandi('#f(nota: "cap. V")'), '#f(nota: "cap. V")')

    def test_dentro_un_blocco_di_codice_non_tocca(self):
        typ = "```\ncap. V Scena 6\n```"
        self.assertEqual(E.numera_rimandi(typ), typ)

    def test_romani_nudi_solo_se_chiesti(self):
        riga = "solo se (I, Atto I; III)."
        self.assertEqual(E.numera_rimandi(riga), riga)
        self.assertIn('#rif-pagina("III", "")', E.numera_rimandi(riga, romani=True))


class TestCapitoloDellaParte(unittest.TestCase):
    """Il master separato dalla sua parte da un a capo, e «§7 di `DEF-4`»."""

    def test_a_capo_fra_master_e_parte(self):
        self.assertIsNotNone(testo._PARTE.match("\nAppendice C.3"))

    def test_forma_con_il_paragrafo_prima(self):
        self.assertIsNotNone(testo._PARTE_PRIMA.search("il §7 di "))


class TestTemaRisolveLaPagina(unittest.TestCase):
    def test_pagina_giusta_e_niente_sulla_stessa_pagina(self):
        try:
            import typst
            import pymupdf
        except ImportError as e:  # pragma: no cover
            self.skipTest(f"manca {e.name}")
        sorgente = (
            '#import "/scripts/typst/tema-rumblingstone.typ": rif-pagina\n'
            '= I · Primo\n'
            'Vedi cap. II Scena 6#rif-pagina("II", "SCENA 6"); e cap. II#rif-pagina("II", "");.\n'
            '#pagebreak()\n= II · Secondo\n#pagebreak()\n'
            '== Scena 6 — la tenda\nqui cap. II Scena 6#rif-pagina("II", "SCENA 6");.\n'
        )
        (REPO / "build").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=REPO / "build") as d:
            f = Path(d) / "prova.typ"
            f.write_text(sorgente, encoding="utf-8")
            pdf = typst.compile(str(f), root=str(REPO))
        pagine = [p.get_text().replace("\n", " ") for p in pymupdf.open(stream=pdf)]
        self.assertIn("Scena 6, p.\xa03", pagine[0])
        self.assertIn("cap. II, p.\xa02", pagine[0])
        self.assertNotIn("p.\xa0", pagine[2])


if __name__ == "__main__":
    unittest.main()
