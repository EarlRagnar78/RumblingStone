"""Il rilascio è una PR (ADR-0100): release_plan.py sceglie tag e commit,
release_notes.py prende le note dal CHANGELOG. Su repo git temporanei, mai
sul repo reale; più due controlli sul repo vero (CHANGELOG e versione
d'accordo)."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import release_notes as rn  # noqa: E402
import release_plan as rp  # noqa: E402


def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


CHANGELOG = """# Changelog

## [Non rilasciato]

## [1.1.0] - 2026-11-01

### Aggiunto
- una cosa nuova

## [1.0.0] - 2026-10-23

- il primo
"""


class TestLeNote(unittest.TestCase):
    def test_la_versione_piu_recente_e_la_prima_con_un_numero(self):
        self.assertEqual(rp.newest_release(CHANGELOG), "1.1.0")
        self.assertIsNone(rp.newest_release("# C\n\n## [Non rilasciato]\n"))

    def test_la_sezione_si_ferma_alla_successiva(self):
        self.assertEqual(rn.section(CHANGELOG, "1.1.0"), "### Aggiunto\n- una cosa nuova")
        self.assertEqual(rn.section(CHANGELOG, "1.0.0"), "- il primo")
        self.assertIsNone(rn.section(CHANGELOG, "9.9.9"))

    def test_il_blocco_delle_impronte_resta(self):
        body = "vecchio testo" + rn.VERIFY + "\n\nabc  x.tar.gz"
        nuovo = rn.refreshed(body, "testo corretto")
        self.assertTrue(nuovo.startswith("testo corretto"))
        self.assertIn("abc  x.tar.gz", nuovo)
        self.assertIsNone(rn.refreshed(nuovo, "testo corretto"))


class TestIlPiano(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        _git(self.repo, "init", "-q", "-b", "main")
        _git(self.repo, "config", "user.email", "t@t")
        _git(self.repo, "config", "user.name", "t")
        (self.repo / "scripts" / "dmcore").mkdir(parents=True)
        (self.repo / "skills").mkdir()
        self._scrivi("0.9.0", "skill 1")
        self.vecchio = self._commit("prima")

    def tearDown(self):
        self._tmp.cleanup()

    def _scrivi(self, versione, skill):
        (self.repo / rp.VERSION_FILE).write_text(f'__version__ = "{versione}"\n')
        (self.repo / "skills" / "S.md").write_text(skill)

    def _commit(self, msg):
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-qm", msg)
        return _git(self.repo, "rev-parse", "HEAD")

    def test_il_tag_va_sul_commit_che_alza_la_versione(self):
        self._scrivi("1.0.0", "skill 2")
        rilascio = self._commit("rilascio 1.0.0")
        (self.repo / "skills" / "S.md").write_text("skill 3, dopo")
        self._commit("dopo")
        p = rp.plan(str(self.repo), "1.0.0")
        self.assertEqual((p["release"], p["tag"], p["sha"]), ("true", "v1.0.0", rilascio))

    def test_se_i_pacchetti_non_cambiano_si_etichetta_la_testa(self):
        self._scrivi("1.0.0", "skill 2")
        self._commit("rilascio 1.0.0")
        (self.repo / "NOTE.md").write_text("solo documenti")
        testa = self._commit("documenti")
        self.assertEqual(rp.plan(str(self.repo), "1.0.0")["sha"], testa)

    def test_un_tag_esistente_vuol_dire_gia_rilasciata(self):
        self._scrivi("1.0.0", "skill 2")
        self._commit("rilascio 1.0.0")
        _git(self.repo, "tag", "v1.0.0")
        self.assertEqual(rp.plan(str(self.repo), "1.0.0")["release"], "false")
        self.assertEqual(rp.plan(str(self.repo), "1.0.0", explicit=True)["release"], "true")

    def test_una_versione_mai_scritta_si_ferma(self):
        with self.assertRaises(SystemExit):
            rp.plan(str(self.repo), "2.0.0")

    def test_workflow_cambiati_dopo_il_rilascio_lo_dice(self):
        self._scrivi("1.0.0", "skill 2")
        self._commit("rilascio 1.0.0")
        (self.repo / ".github" / "workflows").mkdir(parents=True)
        (self.repo / ".github" / "workflows" / "ci.yml").write_text("name: CI\n")
        (self.repo / "skills" / "S.md").write_text("skill 3, dopo")
        self._commit("workflow e skill dopo")
        self.assertEqual(rp.plan(str(self.repo), "1.0.0")["workflows_differ"], "true")


class TestLaCostruzioneERiproducibile(unittest.TestCase):
    """Misurato il 2026-10-23: due costruzioni dello stesso commit davano
    index.json diversi (l'ora di oggi e i domini da un set)."""

    def test_con_source_date_epoch_l_ora_e_fissa(self):
        import os
        import index_skills
        vecchio = os.environ.get("SOURCE_DATE_EPOCH")
        os.environ["SOURCE_DATE_EPOCH"] = "1761177600"
        try:
            self.assertEqual(index_skills._quando(), "2025-10-23T00:00:00+00:00")
        finally:
            if vecchio is None:
                del os.environ["SOURCE_DATE_EPOCH"]
            else:
                os.environ["SOURCE_DATE_EPOCH"] = vecchio

    def test_i_domini_escono_in_ordine(self):
        import index_skills
        testo = " ".join(kw for kws in index_skills.DOMAIN_KEYWORDS.values() for kw in kws)
        domini = index_skills.infer_domains_from_content("x.md", testo)
        self.assertEqual(domini, sorted(domini))
        self.assertGreater(len(domini), 1)


class TestSulRepoVero(unittest.TestCase):
    def test_il_changelog_e_la_versione_vanno_d_accordo(self):
        """La sezione più recente del CHANGELOG è la versione nel codice: chi
        apre una sezione nuova alza anche __version__, e viceversa."""
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        codice = (ROOT / rp.VERSION_FILE).read_text(encoding="utf-8")
        self.assertEqual(rp.newest_release(changelog), rp.current_version(codice))

    def test_la_sezione_non_rilasciata_ce(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [Non rilasciato]", changelog)


if __name__ == "__main__":
    unittest.main()
