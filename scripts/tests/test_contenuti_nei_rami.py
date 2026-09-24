"""contenuti_nei_rami.py: i file che esistono in un ramo e mai su `main`.

Lotto 4i-2 di PIANO-RIPRESA-PR-ABBANDONATE. I test girano in un repository
temporaneo: il clone vero conosce rami diversi da una macchina all'altra, e
un test che dipende da quali rami ci sono e' un test che mente.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import contenuti_nei_rami as C  # noqa: E402


def _git(radice: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=radice, capture_output=True, text=True,
                          check=True).stdout


def _repo(radice: Path) -> None:
    """main con `a.md` e un file poi tolto; il ramo `pr/1` con tre casi."""
    _git(radice, "init", "-q", "-b", "main")
    _git(radice, "config", "user.email", "t@t")
    _git(radice, "config", "user.name", "t")
    (radice / "a.md").write_text("contenuto di a\n", encoding="utf-8")
    (radice / "tolto.md").write_text("c'era\n", encoding="utf-8")
    _git(radice, "add", ".")
    _git(radice, "commit", "-q", "-m", "base")
    (radice / "tolto.md").unlink()
    _git(radice, "commit", "-q", "-am", "tolto")
    _git(radice, "update-ref", "refs/remotes/origin/main", "HEAD")

    _git(radice, "checkout", "-q", "-b", "ramo")
    (radice / "perso.md").write_text("mai arrivato\n", encoding="utf-8")        # perso
    (radice / "rinominato.md").write_text("contenuto di a\n", encoding="utf-8")  # stesso blob di a.md
    (radice / "tolto.md").write_text("riscritto\n", encoding="utf-8")           # percorso gia' in main
    _git(radice, "add", ".")
    _git(radice, "commit", "-q", "-m", "ramo")
    _git(radice, "update-ref", "refs/remotes/pr/1", "HEAD")
    _git(radice, "checkout", "-q", "main")


class TestMaiArrivati(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.radice = Path(self._tmp.name)
        _repo(self.radice)
        self._patch = mock.patch.object(C, "ROOT", self.radice)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        self._tmp.cleanup()

    def test_solo_il_file_mai_visto_ne_per_nome_ne_per_contenuto(self):
        refs = C.riferimenti("origin/main")
        self.assertEqual(refs, ["pr/1"])
        self.assertEqual(C.mai_arrivati("origin/main", refs), {"perso.md": ["pr/1"]})

    def test_check_e_rosso_se_il_file_non_ha_posto(self):
        reg = self.radice / "registro.json"
        reg.write_text(json.dumps({"rami": [], "file": []}), encoding="utf-8")
        with mock.patch.object(C, "REGISTRO", reg), mock.patch("sys.stdout"):
            self.assertEqual(C.main(["--check"]), 1)
            self.assertEqual(C.main([]), 0, "senza --check misura e basta")

    def test_check_e_verde_quando_il_registro_gli_da_un_posto(self):
        reg = self.radice / "registro.json"
        reg.write_text(json.dumps({"rami": [], "file": [
            {"percorso": "perso.md", "stato": "da-decidere", "dove": "D99"}]}), encoding="utf-8")
        with mock.patch.object(C, "REGISTRO", reg), mock.patch("sys.stdout"):
            self.assertEqual(C.main(["--check"]), 0)


class TestCloneSenzaBase(unittest.TestCase):
    def test_senza_origin_main_non_e_un_errore(self):
        """Il checkout della CI non ha sempre `origin/main`: si dice e si esce 0."""
        with tempfile.TemporaryDirectory() as tmp:
            radice = Path(tmp)
            _git(radice, "init", "-q", "-b", "main")
            with mock.patch.object(C, "ROOT", radice), mock.patch("sys.stdout"):
                self.assertEqual(C.main(["--check"]), 0)


class TestPosto(unittest.TestCase):
    REG = {
        "rami": [{"ref": ["pr/9", "origin/x"], "stato": "in-volo", "dove": "piano"},
                 {"ref": "origin/campaign-group-*", "stato": "partita", "dove": "ADR-0007"}],
        "file": [{"percorso": "f.md", "stato": "portato", "dove": "ADR-1"}],
    }

    def test_il_file_vince_sul_ramo(self):
        self.assertEqual(C.posto("f.md", ["pr/9"], self.REG)["stato"], "portato")

    def test_un_ramo_scoperto_basta_a_lasciarlo_senza_posto(self):
        """La copia nel ramo scoperto potrebbe essere l'unica diversa."""
        self.assertIsNotNone(C.posto("g.md", ["pr/9", "origin/x"], self.REG))
        self.assertIsNone(C.posto("g.md", ["pr/9", "pr/10"], self.REG))

    def test_i_modelli_di_ramo(self):
        self.assertEqual(C.posto("h.md", ["origin/campaign-group-tavolo2"], self.REG)["stato"],
                         "partita")

    def test_una_voce_che_non_trova_piu_niente_e_scaduta(self):
        esito = C.confronta({"g.md": ["pr/9"]}, self.REG)
        self.assertEqual(esito["scadute"], ["f.md"])
        self.assertEqual(esito["senza_posto"], [])


class TestRegistro(unittest.TestCase):
    def _scrivi(self, dati: dict) -> Path:
        tmp = Path(tempfile.mkdtemp()) / "r.json"
        tmp.write_text(json.dumps(dati), encoding="utf-8")
        return tmp

    def test_stato_ignoto_e_rifiutato(self):
        p = self._scrivi({"file": [{"percorso": "x", "stato": "boh", "dove": "y"}]})
        with self.assertRaises(ValueError):
            C.leggi_registro(p)

    def test_senza_chi_ne_risponde_e_rifiutato(self):
        p = self._scrivi({"rami": [{"ref": "pr/1", "stato": "in-volo"}]})
        with self.assertRaises(ValueError):
            C.leggi_registro(p)

    def test_il_registro_del_repo_e_valido(self):
        dati = C.leggi_registro()
        self.assertTrue(dati["rami"] and dati["file"])

    def test_ogni_da_decidere_rimanda_a_una_decisione_aperta(self):
        """Un «da decidere» senza la sua D<n> e' una domanda che nessuno fara'."""
        piano = (ROOT / "plans" / "PIANO-RIPRESA-PR-ABBANDONATE.md").read_text(encoding="utf-8")
        import re
        for voce in C.leggi_registro()["file"]:
            if voce["stato"] != "da-decidere":
                continue
            d = re.search(r"\bD\d+\b", voce["dove"])
            self.assertIsNotNone(d, voce["percorso"])
            self.assertIn(f"| {d.group()} |", piano, f"{d.group()} non e' aperta nel piano")


if __name__ == "__main__":
    unittest.main()
