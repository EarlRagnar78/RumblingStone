"""Test di comportamento per validate_docs.py (gate anti-deriva doc<->filesystem).

Copre i casi che rendono il gate affidabile: deve **trovare** un percorso
inventato e deve **tacere** su citazioni legittime (abbreviazioni ADR, modelli
di nome, segnaposto, direttive di esclusione). Un validatore che dà falsi
positivi viene disattivato dopo due settimane: i casi negativi qui sotto sono
quelli che ne difendono la credibilità.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_docs as vd  # noqa: E402


class TestTreeParsing(unittest.TestCase):
    def test_ricostruisce_i_percorsi_annidati(self):
        text = "```\ncampaign/\n├── state.md\n└── lore/\n    └── house-rules.md\n```\n"
        got = [p for _, p in vd.paths_from_tree_blocks(text)]
        self.assertIn("campaign/state.md", got)
        self.assertIn("campaign/lore/house-rules.md", got)

    def test_ignora_i_commenti_a_destra(self):
        text = "```\ncampaign/                 # commento con parole/slash\n```\n"
        self.assertEqual([p for _, p in vd.paths_from_tree_blocks(text)], ["campaign"])


class TestFalsiPositivi(unittest.TestCase):
    """Ogni caso qui è una citazione legittima: il gate NON deve segnalarla."""

    def test_abbreviazione_adr_accettata(self):
        # `plans/adr/ADR-0003` designa senza ambiguità un solo file.
        self.assertTrue(vd._exists("plans/adr/ADR-0003"))

    def test_prefisso_ambiguo_rifiutato(self):
        # `plans/adr/ADR-00` corrisponde a molti file: ambiguità = errore.
        self.assertFalse(vd._exists("plans/adr/ADR-00"))

    def test_modelli_di_nome_non_sono_percorsi(self):
        for tmpl in ("campaign/sessions/YYYY-MM-DD_session-N.md",
                     "campaign/npcs/[name-kebab-case].md"):
            self.assertTrue(
                vd.PLACEHOLDER.search(tmpl) or vd.NAME_TEMPLATE.search(tmpl),
                f"{tmpl} dovrebbe essere riconosciuto come modello",
            )

    def test_mirror_generati_esclusi(self):
        self.assertTrue(vd._is_generated_mirror(".claude/skills/x"))
        self.assertFalse(vd._is_generated_mirror(".github/workflows/ci.yml"))


class TestDirettiveDiEsclusione(unittest.TestCase):
    def test_ignore_su_singola_riga(self):
        text = "a\n`campaign/inesistente/` <!-- validate-docs: ignore -->\nb\n"
        self.assertEqual(vd.ignored_lines(text), {2})

    def test_ignore_a_blocco(self):
        text = ("a\n<!-- validate-docs: ignore-begin -->\nx\ny\n"
                "<!-- validate-docs: ignore-end -->\nb\n")
        self.assertEqual(vd.ignored_lines(text), {2, 3, 4, 5})


class TestGateReale(unittest.TestCase):
    def test_il_repo_e_pulito(self):
        """Il gate deve essere verde sul repo: è la condizione per tenerlo in CI."""
        tops = vd._toplevel_dirs()
        problems = []
        for d in vd.DEFAULT_DOCS:
            problems.extend(vd.check_doc(d, tops))
        self.assertEqual(problems, [], f"percorsi citati e inesistenti: {problems}")

    def test_trova_un_percorso_inventato(self):
        """Caso negativo: un documento che asserisce una cartella inesistente fallisce."""
        doc = ROOT / "scripts" / "tests" / "fixtures" / "_tmp_validate_docs.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text("```\ncampaign/\n└── npcs/\n```\n", encoding="utf-8")
        try:
            problems = vd.check_doc(str(doc.relative_to(ROOT)), vd._toplevel_dirs())
            self.assertTrue(any(p["path"] == "campaign/npcs" for p in problems))
        finally:
            doc.unlink()


if __name__ == "__main__":
    unittest.main()
