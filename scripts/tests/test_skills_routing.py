"""Il gate di ADR-0041: AGENTS.md instrada ogni skill, in tutte e due le direzioni.

Il test non guarda il testo della sezione — non saprebbe dire se una riga
descrive bene una skill. Guarda l'invariante che si e' rotto davvero: l'elenco
di AGENTS.md aveva tredici voci a fronte di diciotto directory con un SKILL.md,
e le cinque mancanti erano tutte skill nate dopo l'ultima riscrittura.
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
import validate_skills  # noqa: E402


class TestInstradamentoSkill(unittest.TestCase):
    def test_il_repo_reale_e_instradato_per_intero(self):
        """Nessuna skill orfana e nessun puntatore morto, qui e adesso."""
        self.assertEqual(validate_skills.check_agents_routing(ROOT), [])

    def test_ogni_skill_su_disco_compare_in_agents(self):
        """La direzione che ha preso l'omissione delle cinque skill."""
        su_disco = {d.name for d in (ROOT / "skills").iterdir()
                    if d.is_dir() and (d / "SKILL.md").exists()}
        testo = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        mancanti = sorted(n for n in su_disco if f"skills/{n}/" not in testo)
        self.assertEqual(mancanti, [], f"skill non instradate in AGENTS.md: {mancanti}")

    def test_una_skill_nuova_non_instradata_rompe_il_gate(self):
        """Il gate morde: senza questo il test sopra passerebbe anche vuoto."""
        with tempfile.TemporaryDirectory() as tmp:
            finto = Path(tmp) / "repo"
            (finto / "skills" / "zz-nuova").mkdir(parents=True)
            (finto / "skills" / "zz-nuova" / "SKILL.md").write_text(
                "---\nname: zz-nuova\ndescription: prova\n---\n", encoding="utf-8")
            (finto / "AGENTS.md").write_text("## Skills\n\nnessuna riga.\n",
                                             encoding="utf-8")
            errori = validate_skills.check_agents_routing(finto)
            self.assertTrue(any("zz-nuova" in e and "non e' instradata" in e
                                for e in errori), errori)

    def test_un_puntatore_morto_rompe_il_gate(self):
        """L'altra direzione: la skill rinominata che lascia il link vecchio."""
        with tempfile.TemporaryDirectory() as tmp:
            finto = Path(tmp) / "repo"
            (finto / "skills" / "esiste").mkdir(parents=True)
            (finto / "skills" / "esiste" / "SKILL.md").write_text(
                "---\nname: esiste\ndescription: prova\n---\n", encoding="utf-8")
            (finto / "AGENTS.md").write_text(
                "## Skills\n\n`skills/esiste/` e `skills/sparita/`\n", encoding="utf-8")
            errori = validate_skills.check_agents_routing(finto)
            self.assertTrue(any("sparita" in e and "non esiste su disco" in e
                                for e in errori), errori)

    def test_senza_agents_md_il_gate_non_tace(self):
        """Un gate che si spegne quando manca il file e' un gate che non c'e'."""
        with tempfile.TemporaryDirectory() as tmp:
            finto = Path(tmp) / "repo"
            (finto / "skills").mkdir(parents=True)
            self.assertNotEqual(validate_skills.check_agents_routing(finto), [])


if __name__ == "__main__":
    unittest.main()
