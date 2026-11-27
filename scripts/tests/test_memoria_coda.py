"""Test di memoria_coda.py (ADR-0138): il cancello della coda della memoria storica."""
from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import memoria_coda as mc  # noqa: E402
import memoria_storica as ms  # noqa: E402

STORICA = """# Memoria storica

## Voci

### MS-0001 · 2026-10-19 · Una voce vecchia

- **Data:** 2026-10-19
- **PR:** #257
- **ADR:** —
- **Temi:** arc07
- **Origine:** memoria del progetto
- **Testo:** Virata al posto di Ghermire; la presa in bocca è di Fauci.
"""

VOCE = """### MS-???? · 2026-11-18 · Il rilascio aspetta le promozioni

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** —
- **Temi:** rilascio card
- **Origine:** card nel thread «Audit»
- **Testo:** il rilascio 1.1.0 si fa dopo le promozioni a stable, con una card prima del tag.
"""


class Base(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        d = Path(self.t.name)
        self.coda = d / "coda"
        self.coda.mkdir()
        self.f = d / "MEMORIA-STORICA.md"
        self.f.write_text(STORICA, encoding="utf-8")
        (self.coda / "LEGGIMI.md").write_text("### MS-???? · non è una voce\n", encoding="utf-8")

    def tearDown(self):
        self.t.cleanup()

    def scrivi(self, titolo: str, testo: str = VOCE) -> Path:
        f = self.coda / (mc.nome_file(titolo) + ".md")
        f.write_text(testo, encoding="utf-8")
        return f

    def gira(self, *argv: str) -> "tuple[int, str]":
        out = io.StringIO()
        with redirect_stdout(out):
            rc = mc.main([str(self.coda), "--file", str(self.f), *argv])
        return rc, out.getvalue()


class TestNome(unittest.TestCase):
    def test_il_nome_del_file_viene_dal_titolo(self):
        self.assertEqual(mc.nome_file("Fissare lo standard del volume dei booklet"),
                         "fissare-lo-standard-del-volume-dei-booklet")
        self.assertEqual(mc.nome_file("  Città: «d» eufonica!  "), "citta-d-eufonica")


class TestForma(Base):
    def test_coda_vuota_e_coda_in_forma_passano(self):
        self.assertEqual(self.gira("--check")[0], 0)
        self.scrivi("Audit settimanale")
        rc, out = self.gira("--check")
        self.assertEqual(rc, 0, out)
        self.assertIn("1 file, 1 voci", out)

    def test_i_difetti_che_devono_fallire(self):
        casi = {
            "testa col numero": VOCE.replace("MS-????", "MS-0007"),
            "data sbagliata": VOCE.replace("· 2026-11-18 ·", "· 18/11 ·"),
            "campo mancante": VOCE.replace("- **Temi:** rilascio card\n", ""),
            "testo vuoto di sostanza": VOCE.split("- **Testo:**")[0] + "- **Testo:** fatto\n",
            "data diversa dal campo": VOCE.replace("- **Data:** 2026-11-18", "- **Data:** 2026-11-17"),
            "campo Coda scritto a mano": VOCE + "- **Coda:** `x`\n",
            "file senza voci": "solo due righe di appunti\n",
            "PR senza numero": VOCE.replace("- **PR:** —", "- **PR:** la solita"),
        }
        for nome, testo in casi.items():
            with self.subTest(nome):
                f = self.scrivi("Audit settimanale", testo)
                rc, out = self.gira("--check")
                self.assertEqual(rc, 1, out)
                self.assertIn("✗", out)
                f.unlink()

    def test_il_nome_del_file_fuori_forma_fallisce(self):
        (self.coda / "Audit Settimanale.md").write_text(VOCE, encoding="utf-8")
        rc, out = self.gira("--check")
        self.assertEqual(rc, 1)
        self.assertIn("audit-settimanale.md", out)


class TestThread(Base):
    def test_un_thread_senza_file_fallisce_e_con_la_voce_passa(self):
        rc, out = self.gira("--thread", "Audit settimanale")
        self.assertEqual(rc, 1)
        self.assertIn("thread senza voce", out)
        self.scrivi("Audit settimanale")
        self.assertEqual(self.gira("--thread", "Audit settimanale")[0], 0)
        self.assertEqual(self.gira("--thread", "Audit settimanale", "--thread", "Un altro")[0], 1)

    def test_elenco_dei_thread_solo_i_risolti_dal_giorno(self):
        elenco = Path(self.t.name) / "t.json"
        elenco.write_text(json.dumps({"sessions": [
            {"title": "Risolto prima", "resolved": True, "resolved_at": "2026-11-17T10:00:00Z"},
            {"title": "Aperto", "state": "working"},
            {"title": "Risolto dopo", "resolved": True, "resolved_at": "2026-11-19T10:00:00Z"},
            {"title": "Audit settimanale", "resolved": True, "resolved_at": "2026-11-18T10:00:00Z"},
        ]}), encoding="utf-8")
        self.scrivi("Audit settimanale")
        rc, out = self.gira("--threads", str(elenco), "--json")
        r = json.loads(out)
        self.assertEqual(rc, 1)
        self.assertEqual(r["thread_senza_voce"], ["Risolto dopo"])
        self.assertEqual(r["thread_controllati"], ["Risolto dopo", "Audit settimanale"])
        self.assertEqual(self.gira("--threads", str(elenco), "--dal", "2026-11-20")[0], 0)
        self.assertEqual(self.gira("--threads", str(Path(self.t.name) / "manca.json"))[0], 2)


class TestPiega(Base):
    def test_piega_numera_scrive_e_non_ripete(self):
        self.scrivi("Audit settimanale", VOCE + "\n" + VOCE.replace("Il rilascio aspetta", "Seconda scelta: aspetta")
                    .replace("2026-11-18", "2026-11-17"))
        self.scrivi("Un altro thread", VOCE.replace("Il rilascio", "Altro"))
        rc, out = self.gira("--piega")
        self.assertEqual(rc, 0, out)
        testo = self.f.read_text(encoding="utf-8")
        self.assertEqual(ms.controlla(testo, None), [])
        voci = ms.leggi(testo)
        self.assertEqual([v.id for v in voci], ["MS-0001", "MS-0002", "MS-0003", "MS-0004"])
        self.assertEqual(voci[1].data, "2026-11-17")           # in ordine di data
        self.assertEqual(voci[1].campi["Coda"], "`audit-settimanale`")
        self.assertNotIn("MS-????", testo)
        rc, out = self.gira("--piega")                          # la seconda non aggiunge nulla
        self.assertEqual(rc, 0)
        self.assertIn("nessuna nuova", out)
        self.assertEqual(self.f.read_text(encoding="utf-8"), testo)

    def test_dopo_la_piega_il_thread_ha_la_voce_anche_a_coda_svuotata(self):
        f = self.scrivi("Audit settimanale")
        self.gira("--piega")
        f.unlink()
        self.assertEqual(self.gira("--thread", "Audit settimanale")[0], 0)

    def test_con_un_difetto_la_piega_non_scrive(self):
        self.scrivi("Audit settimanale", VOCE.replace("- **Temi:** rilascio card\n", ""))
        rc, _ = self.gira("--piega")
        self.assertEqual(rc, 1)
        self.assertEqual(self.f.read_text(encoding="utf-8"), STORICA)


class TestCancelloDelRepo(unittest.TestCase):
    def test_una_testa_senza_numero_nel_file_storico_fallisce(self):
        e = ms.controlla(STORICA + "\n" + VOCE, None)
        self.assertTrue(any("MS-????" in x for x in e), e)

    def test_il_file_vero_non_ne_ha(self):
        self.assertEqual(ms.main(["--check"]), 0)

    def test_uso_sbagliato(self):
        self.assertEqual(mc.main(["/non/esiste", "--check"]), 2)
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(mc.main(["--nome", "Rendere obbligatoria la memoria storica"]), 0)
        self.assertEqual(out.getvalue().strip(), "rendere-obbligatoria-la-memoria-storica.md")


if __name__ == "__main__":
    unittest.main()
