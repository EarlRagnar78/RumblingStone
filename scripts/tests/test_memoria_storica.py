"""Test di memoria_storica.py (ADR-0127): la storia che esce dalla memoria corta."""
from __future__ import annotations

import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import memoria_storica as ms  # noqa: E402

TESTO = """# Memoria storica

Intestazione con un esempio che non è una voce: ### MS-9999 · finto

## Voci

### MS-0001 · 2026-10-19 · Duello con Skullcrusher

- **Data:** 2026-10-19
- **PR:** #257 #242
- **ADR:** —
- **Temi:** arc07 skullcrusher
- **Origine:** memoria del progetto
- **Testo:** Virata al posto di Ghermire; la presa in bocca è di Fauci (PR #242).

### MS-0002 · 2026-10-23 · Città della valle

- **Data:** 2026-10-23
- **PR:** —
- **ADR:** ADR-0102
- **Temi:** mappe citta
- **Origine:** memoria del progetto
- **Testo:** Rethmar capitale, Channathgate la più popolosa.
"""


class TestLettura(unittest.TestCase):
    def setUp(self):
        self.voci = ms.leggi(TESTO)

    def test_legge_le_voci_e_i_campi(self):
        self.assertEqual([v.id for v in self.voci], ["MS-0001", "MS-0002"])
        self.assertEqual(self.voci[0].pr, {257, 242})
        self.assertEqual(self.voci[1].adr, {102})
        self.assertEqual(self.voci[1].temi, ["mappe", "citta"])

    def test_filtri(self):
        self.assertEqual([v.id for v in ms.filtra(self.voci, pr=242)], ["MS-0001"])
        self.assertEqual([v.id for v in ms.filtra(self.voci, adr=102)], ["MS-0002"])
        self.assertEqual([v.id for v in ms.filtra(self.voci, tema="ARC07")], ["MS-0001"])
        self.assertEqual([v.id for v in ms.filtra(self.voci, da="2026-10-20")], ["MS-0002"])
        self.assertEqual([v.id for v in ms.filtra(self.voci, a="2026-10-20")], ["MS-0001"])

    def test_le_parole_non_badano_ad_accenti_e_maiuscole(self):
        self.assertEqual([v.id for v in ms.filtra(self.voci, ["citta", "CHANNATHGATE"])], ["MS-0002"])
        self.assertEqual(ms.filtra(self.voci, ["citta", "Fauci"]), [])

    def test_il_numero_della_pr_non_prende_un_prefisso(self):
        self.assertEqual(ms.filtra(self.voci, pr=24), [])


class TestCancello(unittest.TestCase):
    def test_file_in_forma_passa(self):
        self.assertEqual(ms.controlla(TESTO, "vedi MEMORIA-STORICA.md"), [])

    def test_numeri_fuori_sequenza(self):
        e = ms.controlla(TESTO.replace("MS-0002", "MS-0003"), None)
        self.assertTrue(any("fuori sequenza" in x for x in e), e)

    def test_campo_mancante_e_data_sbagliata(self):
        rotto = TESTO.replace("- **Temi:** mappe citta\n", "").replace("2026-10-23 · Città", "23/10 · Città")
        e = ms.controlla(rotto, None)
        self.assertTrue(any("Temi" in x for x in e), e)
        self.assertTrue(any("AAAA-MM-GG" in x for x in e), e)

    def test_il_changelog_deve_portare_al_file(self):
        e = ms.controlla(TESTO, "nessun collegamento")
        self.assertTrue(any("CHANGELOG" in x for x in e), e)

    def test_il_file_vero_e_in_forma(self):
        self.assertEqual(ms.main(["--check"]), 0)


class TestRiga(unittest.TestCase):
    def test_json_e_data_non_valida(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "M.md"
            f.write_text(TESTO, encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(ms.main(["--file", str(f), "--json", "--pr", "257"]), 0)
            self.assertIn('"id": "MS-0001"', out.getvalue())
            self.assertEqual(ms.main(["--file", str(f), "--da", "19/10"]), 2)


def _git(d: Path, *a: str) -> str:
    return subprocess.run(["git", "-C", str(d), *a], check=True, capture_output=True, text=True,
                          env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
                               "GIT_COMMITTER_EMAIL": "t@t", "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                               "HOME": str(d), "GIT_CONFIG_NOSYSTEM": "1"}).stdout


class TestPrDalMerge(unittest.TestCase):
    """ADR-0137: una voce scritta con «PR: —» si trova col numero del merge che l'ha portata."""

    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.d = Path(self.t.name)
        _git(self.d, "init", "-q", "-b", "main")
        f = self.d / "plans" / "MEMORIA-STORICA.md"
        f.parent.mkdir()
        f.write_text(TESTO, encoding="utf-8")
        _git(self.d, "add", ".")
        _git(self.d, "commit", "-qm", "inizio")
        _git(self.d, "checkout", "-qb", "ramo")
        f.write_text(TESTO + "\n### MS-0003 · 2026-11-18 · Voce senza numero\n\n- **Data:** 2026-11-18\n"
                     "- **PR:** —\n- **ADR:** —\n- **Temi:** prova\n- **Origine:** riga in `plans/CHANGELOG.md`\n- **Testo:** x\n",
                     encoding="utf-8")
        _git(self.d, "commit", "-qam", "voce")
        _git(self.d, "checkout", "-q", "main")
        _git(self.d, "merge", "-q", "--no-ff", "ramo", "-m", "Merge pull request #501 from x/ramo")
        self.f = f

    def tearDown(self):
        self.t.cleanup()

    def test_la_mappa_viene_dal_merge(self):
        m = ms.pr_dai_merge(self.d, self.f)
        self.assertEqual(m, {"MS-0003": {501}})

    def test_la_riga_di_comando_trova_la_voce_senza_numero(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(ms.main(["--file", str(self.f), "--pr", "501", "--elenco"]), 0)
        self.assertEqual(out.getvalue().split()[0], "MS-0003")
        out = io.StringIO()
        with redirect_stdout(out):
            ms.main(["--file", str(self.f), "--pr", "501", "--elenco", "--senza-git"])
        self.assertEqual(out.getvalue(), "")

    def test_senza_git_la_mappa_e_vuota(self):
        self.assertEqual(ms.pr_dai_merge(self.d / "non-esiste", self.f), {})


class TestConfrontaMemoria(unittest.TestCase):
    def test_trova_cio_che_il_repo_non_ha(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            _git(d, "init", "-q", "-b", "main")
            (d / "a.md").write_text("PR #123 e ADR-0042 stanno qui, e la #9990", encoding="utf-8")
            _git(d, "add", ".")
            _git(d, "commit", "-qm", "x")
            mem = d / "mem"
            mem.mkdir()
            (mem / "MEMORY.md").write_text("- #123 e ADR-0042 noti\n- #999 solo in memoria\n- una regola in prosa\n",
                                           encoding="utf-8")
            (mem / "nota-x.md").write_text("---\nname: nota-x\n---\nniente gettoni\n", encoding="utf-8")
            r = ms.confronta_memoria(mem, d, storica="cita nota-x")
            self.assertEqual(r["righe"], 4)
            self.assertEqual(r["righe_con_gettoni"], 2)
            self.assertEqual([s["mancano"] for s in r["righe_scoperte"]], [["#999"]])
            self.assertEqual(r["note_citate"], 1)


class TestTettoMemoria(unittest.TestCase):
    """ADR-0139: la memoria del 2026-11-19 era a 16.878 byte; il tetto esce 1 prima del limite."""

    def _mem(self, d: Path, testo: str) -> Path:
        (d / "MEMORY.md").write_text(testo, encoding="utf-8")
        return d

    def test_sotto_e_sopra_il_tetto(self):
        with tempfile.TemporaryDirectory() as t:
            d = self._mem(Path(t), "- una regola\n")
            self.assertEqual(ms.main(["--tetto-memoria", str(d)]), 0)
            self._mem(d, "- riga lunga " + "x" * 200 + "\n" + "- corta\n" * 10)
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(ms.main(["--tetto-memoria", str(d), "--tetto", "100"]), 1)
            self.assertIn("r.1 (", buf.getvalue())

    def test_conta_byte_non_caratteri(self):
        with tempfile.TemporaryDirectory() as t:
            d = self._mem(Path(t), "è" * 60)  # 60 caratteri, 120 byte
            r = ms.misura_memoria(d, tetto=100)
            self.assertEqual(r["byte"], 120)
            self.assertTrue(r["sopra_tetto"])
            self.assertFalse(r["sopra_limite"])

    def test_la_memoria_oltre_il_limite_lo_dice(self):
        with tempfile.TemporaryDirectory() as t:
            d = self._mem(Path(t), "x" * (ms.LIMITE_MEMORIA + 1))
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(ms.main(["--tetto-memoria", str(d)]), 1)
            self.assertIn("OLTRE IL LIMITE", buf.getvalue())

    def test_manca_memory_md(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(ms.main(["--tetto-memoria", t]), 2)


if __name__ == "__main__":
    unittest.main()
