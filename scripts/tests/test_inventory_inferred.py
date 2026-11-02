"""Test per inventory_inferred.py (finding C4, lotto G4).

Il test che conta è quello sulla **classificazione**. Un ratchet che conta
insieme i marcatori dei documenti vivi e quelli dei changelog produce un numero
che non può scendere — si smaltisce un debito, si scrive nel changelog che l'hai
smaltito, e il totale resta uguale. Un gate così viene disattivato entro una
settimana, ed è la stessa dinamica del finding T3.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import inventory_inferred as inv  # noqa: E402


class TestClassificazione(unittest.TestCase):
    """La distinzione che rende il ratchet capace di scendere."""

    def test_i_documenti_vivi_sono_debito_aperto(self):
        for rel in ("campaign/state.yaml",
                    "07_il Portale/ARC07-DEF-1.md",
                    "Bestiario/png/Lorana/Lorana.md",
                    "PG/Artefatti/x.md"):
            self.assertEqual(inv.classe(rel), "aperti", rel)

    def test_i_piani_e_i_changelog_sono_storici(self):
        """Raccontano un debito, non lo aprono."""
        for rel in ("plans/PIANO-X.md", "plans/CHANGELOG.md",
                    "campaign/state-changelog.md"):
            self.assertEqual(inv.classe(rel), "storici", rel)

    def test_i_documenti_di_audit_sono_meta(self):
        """Citano il marcatore per misurarlo."""
        self.assertEqual(inv.classe("docs/audit/AUDIT-2026-08-SINTESI.md"), "meta")

    def test_la_documentazione_normale_non_e_meta(self):
        """Solo `docs/audit/`: una guida che marca un'inferenza ha un debito vero."""
        self.assertEqual(inv.classe("docs/guides/GUIDA-IMMAGINI.md"), "aperti")


class TestScansione(unittest.TestCase):
    def test_riconosce_nudi_e_parlanti(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.md"
            f.write_text("a `[INFERRED]` b\n"
                         "c `[INFERRED — needs DM confirmation]` d\n"
                         "e `[INFERRED: durata 3 round]` f\n", encoding="utf-8")
            voci = inv.scansiona(Path(d))
            self.assertEqual(len(voci), 3)
            note = [v["nota"] for v in voci]
            self.assertEqual(note[0], "", "il marcatore nudo non ha nota")
            self.assertEqual(note[1], "needs DM confirmation")
            self.assertEqual(note[2], "durata 3 round")

    def test_piu_marcatori_sulla_stessa_riga_contano_tutti(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "x.md").write_text("[INFERRED] e [INFERRED]\n", encoding="utf-8")
            self.assertEqual(len(inv.scansiona(Path(d))), 2)

    def test_ignora_le_cartelle_generate(self):
        with tempfile.TemporaryDirectory() as d:
            gen = Path(d) / "build"
            gen.mkdir()
            (gen / "x.md").write_text("[INFERRED]\n", encoding="utf-8")
            self.assertEqual(inv.scansiona(Path(d)), [])


class TestRatchet(unittest.TestCase):
    """Nessun test scrive nel repo: la baseline è un file temporaneo."""

    def _check(self, testo: str, baseline: int | None) -> int:
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "vivo.md").write_text(testo, encoding="utf-8")
            b = Path(d) / "baseline.json"
            if baseline is not None:
                b.write_text(json.dumps({"aperti": baseline}) + "\n", encoding="utf-8")
            with mock.patch.object(inv, "BASELINE", b):
                return inv.main(["--check", "--path", d])

    def test_check_fallisce_se_sale(self):
        self.assertEqual(self._check("[INFERRED]\n" * 5, 0), 1)

    def test_check_passa_se_resta_o_scende(self):
        self.assertEqual(self._check("[INFERRED]\n" * 5, 5), 0)
        self.assertEqual(self._check("[INFERRED]\n" * 2, 5), 0)

    def test_senza_baseline_e_errore_d_uso(self):
        self.assertEqual(self._check("[INFERRED]\n", None), 2)

    def test_la_baseline_del_repo_esiste(self):
        """Il confronto col repo vero lo fa la CI, non pytest: è un gate in prova
        (ADR-0099) e un [INFERRED] in più non deve fermare i test di tutti."""
        self.assertTrue(inv.BASELINE.exists(), "baseline assente: eseguire --update-baseline")
        self.assertIsInstance(json.loads(inv.BASELINE.read_text(encoding="utf-8"))["aperti"], int)


class TestInventarioGenerato(unittest.TestCase):
    """L'inventario si genera a richiesta e non si committa: resterebbe indietro
    al primo [INFERRED] tolto o aggiunto."""

    def test_dichiara_di_essere_generato_e_conta_solo_gli_aperti(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "vivo.md").write_text("[INFERRED]\n[INFERRED: quanti pf]\n", encoding="utf-8")
            (Path(d) / "CHANGELOG.md").write_text("[INFERRED]\n", encoding="utf-8")
            out = Path(d) / "inv.md"
            self.assertEqual(inv.main(["--path", d, "--out", str(out)]), 0)
            testo = out.read_text(encoding="utf-8")
            self.assertIn("GENERATO", testo.splitlines()[0])
            self.assertIn("| **aperti** | **2** |", testo)
            self.assertIn("| storici | 1 |", testo)


if __name__ == "__main__":
    unittest.main()
