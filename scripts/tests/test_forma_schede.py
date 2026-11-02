"""La forma delle schede di PNG e villain (ADR-0091): `validate_bestiario --forma`.

Il conto deve mordere su una sezione mancante e su una fuori ordine, lasciare
passare il dossier breve e saltare i rimandi. E le tre schede di prova devono
restare nella forma: sono l'esempio che la guida cita.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import validate_bestiario as V  # noqa: E402

STAT_OK = """# Tizio — prova (umano, Guerriero 1)
**Faction**: x | **Role**: x | **Environment**: x | **CR**: 1 | **Source**: x | **Status**: inferred

**Difesa** CA 10
**Attacco** Vel 9 m
**Statistiche** For 10
**Capacità speciali** Nessuna.
**Tattiche** [DA SCRIVERE — prova]
"""

DOSSIER_OK = """# Tizio [RIMANDO]
**Key stats**: → `tizio-cr1.md`

## Chi è
x
## Aspetto e voce
x
## Cosa vuole
x
## Nella campagna
x
## In combattimento
x
## Esiti possibili
x
## Fonti e canone
x
"""


class TestForma(unittest.TestCase):
    def scrivi(self, nome: str, testo: str) -> Path:
        d = Path(tempfile.mkdtemp())
        p = d / nome
        p.write_text(testo, encoding="utf-8")
        return p

    def test_statblocco_nella_forma(self):
        f = V.forma(self.scrivi("tizio-cr1.md", STAT_OK))
        self.assertEqual((f["mancano"], f["fuori_ordine"]), ([], []))

    def test_statblocco_senza_tattiche_morde(self):
        testo = STAT_OK.replace("**Tattiche** [DA SCRIVERE — prova]\n", "")
        f = V.forma(self.scrivi("tizio-cr1.md", testo))
        self.assertEqual(f["mancano"], ["Tattiche"])

    def test_statblocco_fuori_ordine_morde(self):
        testo = STAT_OK.replace("**Difesa** CA 10\n", "") + "**Difesa** CA 10\n"
        f = V.forma(self.scrivi("tizio-cr1.md", testo))
        self.assertEqual(f["fuori_ordine"], ["Difesa"])

    def test_pointer_non_si_conta(self):
        testo = "# Tizio [POINTER — canonical file]\n**Status**: POINTER\n"
        self.assertIsNone(V.forma(self.scrivi("tizio-cr1.md", testo)))

    def test_dossier_nella_forma(self):
        f = V.forma(self.scrivi("Tizio.md", DOSSIER_OK))
        self.assertEqual((f["tipo"], f["mancano"], f["fuori_ordine"]), ("dossier", [], []))

    def test_dossier_senza_cosa_vuole_morde(self):
        testo = DOSSIER_OK.replace("## Cosa vuole\nx\n", "")
        self.assertEqual(V.forma(self.scrivi("Tizio.md", testo))["mancano"], ["Cosa vuole"])

    def test_in_combattimento_solo_se_rimanda(self):
        testo = DOSSIER_OK.replace(" [RIMANDO]", "").replace("## In combattimento\nx\n", "")
        self.assertEqual(V.forma(self.scrivi("Tizio.md", testo))["mancano"], [])

    def test_dossier_fuori_ordine_morde(self):
        testo = DOSSIER_OK.replace("## Chi è\nx\n", "") + "## Chi è\nx\n"
        self.assertEqual(V.forma(self.scrivi("Tizio.md", testo))["fuori_ordine"], ["Chi è"])

    def test_dossier_breve_passa(self):
        testo = "# Tizio\n**Role**: ally\n**Status**: vivo\n"
        f = V.forma(self.scrivi("Tizio.md", testo))
        self.assertEqual((f["tipo"], f["mancano"]), ("breve", []))

    def test_i_dossier_di_gruppo_restano_fuori(self):
        # decisione del DM del 2026-10-15: restano come sono, non si contano
        for nome in V.DOSSIER_DI_GRUPPO:
            with self.subTest(nome=nome):
                self.assertIsNone(V.forma(self.scrivi(nome, "# Gruppo\n## Altro\nx\n")))

    def test_le_schede_di_prova_restano_nella_forma(self):
        for rel in (
            "Bestiario/png/Lorana/Lorana/Lorana.md",
            "Bestiario/png/Lorana/capitana-lorana-cr7.md",
            "Bestiario/villain/Ushgar_Occhio_Reso/Ushgar_Occhio_Reso.md",
            "Bestiario/villain/Ushgar_Occhio_Reso/ushgar-occhio-reso-cr13.md",
            "Bestiario/villain/balvar-fuocospento-cr13.md",
        ):
            with self.subTest(rel=rel):
                f = V.forma(REPO / rel)
                self.assertEqual((f["mancano"], f["fuori_ordine"]), ([], []))

    def test_con_json_il_rapporto_e_json(self):
        # chi chiede --forma --json deve poter leggere l'uscita con un parser JSON
        import contextlib
        import io
        import json
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = V.main(["--forma", "--json"])
        self.assertEqual(rc, 0)
        report = json.loads(buf.getvalue())
        self.assertEqual(report["rapporto"], "forma")
        self.assertEqual(set(report["conti"]), {"statblocco", "dossier", "breve"})


if __name__ == "__main__":
    unittest.main()
