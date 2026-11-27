"""extract_scene_prompts: l'etichetta di regia esce intera (CODA-SECONDO-LETTORE D2).

Il campo «Etichetta regia» di `PROMPT-IMMAGINI-07ILP.md` era troncato in 32
righe su 46: il grassetto del read-aloud si leggeva fino al primo «*» e poi
si toglievano le parentesi dai bordi, così da `(Salvatore lead) — la Sala.`
restava `Salvatore lead) — la Sala.` e da `**Read-aloud.**` restava `.`.
Il DM ha scelto di correggere lo script e non le righe a mano (2026-11-08).
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import extract_scene_prompts as esp  # noqa: E402


class TestParseLabel(unittest.TestCase):
    CASI = {
        " (LotR lead, Salvatore support) — la Sala.": "LotR lead, Salvatore support — la Sala",
        " (Salvatore lead) — l'attraversamento.": "Salvatore lead — l'attraversamento",
        " (Andor lead).": "Andor lead",
        " (scena (A6) del tempo, Andor lead) — il ritorno.": "scena (A6) del tempo, Andor lead — il ritorno",
        ".": "scena",
        "": "scena",
        " — la soglia.": "la soglia",
        " (*Salvatore* lead) — *la Sala*.": "Salvatore lead — la Sala",
    }

    def test_casi(self):
        for raw, atteso in self.CASI.items():
            with self.subTest(raw=raw):
                self.assertEqual(esp.parse_label(raw), atteso)

    def test_parentesi_mai_chiusa_non_perde_testo(self):
        self.assertEqual(esp.parse_label(" (Salvatore lead, la Sala."), "Salvatore lead, la Sala")


def _arco(tmp: Path, box: str) -> Path:
    arc = tmp / "07_arco"
    arc.mkdir()
    (arc / "ARC07-DEF-1.md").write_text(
        "## §1 — La Sala\n\n" + box + "\n> seconda riga del box\n", encoding="utf-8")
    return arc


class TestEstrazione(unittest.TestCase):
    def test_corsivo_dentro_il_grassetto_non_tronca(self):
        with tempfile.TemporaryDirectory() as t:
            arc = _arco(Path(t), "> **Read-aloud (*LotR* lead) — la Sala.** *Il primo sonno vero.*")
            (scena,) = esp.extract_scenes(arc)
            self.assertEqual(scena["label"], "LotR lead — la Sala")
            self.assertTrue(scena["excerpt"].startswith("Il primo sonno vero"))


class TestFusione(unittest.TestCase):
    """Rigenerando, i campi meccanici si rifanno e il prompt scritto resta."""

    def _gira(self, arc: Path, out: Path) -> str:
        self.assertEqual(esp.main([str(arc), "-o", str(out)]), 0)
        return out.read_text(encoding="utf-8")

    def test_scheda_compilata_prende_l_etichetta_nuova(self):
        with tempfile.TemporaryDirectory() as t:
            arc = _arco(Path(t), "> **Read-aloud (LotR lead) — la Sala.** *Il primo sonno.*")
            out = Path(t) / "PROMPT.md"
            doc = self._gira(arc, out)
            doc = doc.replace("- **Etichetta regia**: LotR lead — la Sala",
                              "- **Etichetta regia**: lead) — la Sala.")
            doc = doc.replace("[DA SCRIVERE", "[PROMPT SCRITTO DAL DM").replace(
                "DA SCRIVERE", "scritto")
            out.write_text(doc, encoding="utf-8")
            nuovo = self._gira(arc, out)
            self.assertIn("- **Etichetta regia**: LotR lead — la Sala\n", nuovo)
            self.assertIn("PROMPT SCRITTO DAL DM", nuovo)
            self.assertNotIn(esp.MANUAL_HEADER, nuovo)
            self.assertEqual(self._gira(arc, out), nuovo, "non è idempotente")

    def test_sezione_rinominata_ritrova_la_sua_scena(self):
        with tempfile.TemporaryDirectory() as t:
            box = "> **Read-aloud (LotR lead) — la Sala.** *Il primo sonno vero dopo giorni di marcia.*"
            arc = _arco(Path(t), box)
            out = Path(t) / "PROMPT.md"
            doc = self._gira(arc, out).replace("[DA SCRIVERE", "[PROMPT SCRITTO DAL DM").replace(
                "DA SCRIVERE", "scritto")
            out.write_text(doc, encoding="utf-8")
            md = arc / "ARC07-DEF-1.md"
            md.write_text(md.read_text(encoding="utf-8").replace("La Sala", "La Sala Grande", 1),
                          encoding="utf-8")
            nuovo = self._gira(arc, out)
            self.assertIn("`[1-la-sala-grande]`", nuovo)
            self.assertNotIn("`[1-la-sala]`", nuovo)
            self.assertIn("PROMPT SCRITTO DAL DM", nuovo)
            self.assertNotIn(esp.MANUAL_HEADER, nuovo)

    def test_scheda_orfana_va_in_coda_senza_residuo_del_troncamento(self):
        with tempfile.TemporaryDirectory() as t:
            arc = _arco(Path(t), "> **Read-aloud (LotR lead) — la Sala.** *Il primo sonno.*")
            out = Path(t) / "PROMPT.md"
            self._gira(arc, out)
            orfana = ("### 09 · §9 — Sparita  `[9-sparita]`\n\n"
                      "- **Fonte**: `ALTRO.md` — §9 — Sparita\n"
                      "- **Etichetta regia**: Salvatore — il ritorno).\n"
                      "- **Stato**: ✅ generata\n")
            out.write_text(out.read_text(encoding="utf-8") + "\n" + orfana, encoding="utf-8")
            nuovo = self._gira(arc, out)
            self.assertIn(esp.MANUAL_HEADER, nuovo)
            self.assertIn("- **Etichetta regia**: Salvatore — il ritorno\n", nuovo)


if __name__ == "__main__":
    unittest.main()
