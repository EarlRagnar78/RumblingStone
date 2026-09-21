"""Il cancello sulle regole d'oro, provato all'indietro.

Ogni prova sabota la tabella in un modo diverso e verifica che il gate se ne
accorga. Un cancello che non si e' mai visto bocciare non e' un cancello.

⚠️ **`unittest`, non pytest.** La CI gira `python -m unittest discover` e
pytest **non e' installato** (ADR-0037, stdlib-only; PIANO-QUALITA-DEL-CODICE
dice no a pytest come dipendenza). La prima stesura di questo file usava le
fixture di pytest: in locale passava, in CI il modulo non si importava
nemmeno.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_skills as vs  # noqa: E402


class TestRegoleDoro(unittest.TestCase):
    """Una copia minima del repo: solo cio' che il controllo guarda."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "skills").mkdir()
        (self.repo / "scripts").mkdir()
        for nome in ("fase1.py", "misura_craft.py", "validate_skills.py",
                     "validate_norme_editoriali.py"):
            (self.repo / "scripts" / nome).write_text("", encoding="utf-8")
        shutil.copy(ROOT / "skills" / "REGOLE-DORO.md", self.repo / "skills")
        shutil.copy(ROOT / "AGENTS.md", self.repo / "AGENTS.md")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def riscrivi(self, prima: str, dopo: str) -> None:
        f = self.repo / "skills" / "REGOLE-DORO.md"
        t = f.read_text(encoding="utf-8")
        self.assertIn(prima, t, "il fixture non contiene piu' la stringa da sabotare")
        f.write_text(t.replace(prima, dopo, 1), encoding="utf-8")

    # ── il repo vero, e il fixture ───────────────────────────────────────

    def test_il_repo_vero_e_verde(self):
        self.assertEqual(vs.check_regole_doro(ROOT), [])

    def test_la_copia_di_prova_e_verde(self):
        """Senza questo, ogni prova sotto direbbe solo che il fixture e' rotto."""
        self.assertEqual(vs.check_regole_doro(self.repo), [])

    # ── i sabotaggi ──────────────────────────────────────────────────────

    def test_file_assente(self):
        with tempfile.TemporaryDirectory() as d:
            vuoto = Path(d)
            (vuoto / "skills").mkdir()
            errori = vs.check_regole_doro(vuoto)
        self.assertTrue(errori)
        self.assertIn("assente", errori[0])

    def test_marcatore_rimosso(self):
        self.riscrivi("<!-- regole-doro: tabella -->", "")
        self.assertTrue(any("manca il marcatore" in e
                            for e in vs.check_regole_doro(self.repo)))

    def test_id_nudo_senza_la_lettera(self):
        """Il difetto misurato: «4» significa tre cose diverse in AGENTS.md."""
        self.riscrivi("| **G4** |", "| **4** |")
        self.assertTrue(any("non e' nella forma **G<numero>**" in e
                            for e in vs.check_regole_doro(self.repo)))

    def test_momento_inventato(self):
        self.riscrivi("| **G2** | 🟨 DURANTE |", "| **G2** | 🟪 QUANDO CAPITA |")
        errori = vs.check_regole_doro(self.repo)
        self.assertTrue(any("momento" in e and "non previsto" in e for e in errori))

    def test_comando_che_non_esiste(self):
        """ADR-0053 applicata alle regole d'oro: un rimando inventato e' un difetto."""
        self.riscrivi("`python3 scripts/fase1.py <bersagli>`",
                      "`python3 scripts/fase1_inesistente.py <bersagli>`")
        self.assertTrue(any("non esiste" in e
                            for e in vs.check_regole_doro(self.repo)))

    def test_regola_senza_verificatore(self):
        f = self.repo / "skills" / "REGOLE-DORO.md"
        righe = f.read_text(encoding="utf-8").splitlines()
        for i, r in enumerate(righe):
            if r.startswith("| **G3** |"):
                celle = r.strip("|").split("|")
                celle[-1] = "  "
                righe[i] = "|" + "|".join(celle) + "|"
                break
        else:  # pragma: no cover
            self.fail("la riga G3 non c'e' piu'")
        f.write_text("\n".join(righe), encoding="utf-8")
        self.assertTrue(any("nessun verificatore" in e
                            for e in vs.check_regole_doro(self.repo)))

    def test_id_duplicato_e_buco_nella_sequenza(self):
        self.riscrivi("| **G1** |", "| **G2** |")
        errori = vs.check_regole_doro(self.repo)
        self.assertTrue(any("compare due volte" in e for e in errori))
        self.assertTrue(any("id mancanti" in e for e in errori))

    def test_conflitto_senza_verdetto(self):
        self.riscrivi("| **R1** | **G5 vs G1** | **G5 prima** |",
                      "| **R1** | **G5 vs G1** |  |")
        self.assertTrue(any("nessun verdetto" in e
                            for e in vs.check_regole_doro(self.repo)))

    def test_il_ponte_con_la_narrazione(self):
        """Una regola nella tabella e non in AGENTS.md e' una regola senza il perche'."""
        agents = self.repo / "AGENTS.md"
        agents.write_text(agents.read_text(encoding="utf-8").replace("`G6`", "`GX`"),
                          encoding="utf-8")
        errori = vs.check_regole_doro(self.repo)
        self.assertTrue(any("G6" in e and "narrazione" in e for e in errori))

    # ── il ciclo ─────────────────────────────────────────────────────────

    def test_ogni_momento_del_ciclo_e_popolato(self):
        """Un ciclo con un buco non e' un ciclo."""
        t = (ROOT / "skills" / "REGOLE-DORO.md").read_text(encoding="utf-8")
        for momento in vs.MOMENTI:
            self.assertIn(momento, t, f"nessuna regola nel momento {momento}")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
