"""copertura_scene: le regole mordono, e il cancello del repo è verde (ADR-0073).

Ogni regola ha un caso finto che deve farla scattare e uno che deve lasciarla
zitta: un rilevatore che non si è mai visto fallire non si sa se funziona.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import copertura_scene as cs  # noqa: E402

SEVERO = {"regole": ["C1", "C2"], "contratto": True}
LEGGERO = {"regole": ["C1", "C2"], "contratto": False}

BUONA = """### SCENA 1 — La cappella

**In scena** — Dove: la cappella — Chi: Sorella Brynja · la guardia della porta

> **Read-aloud (LotR lead) — la cappella.** *Un'incudine al posto dell'altare.*

**Scheda d'entrata — Sorella Brynja, la chierica**

| | |
|---|---|
| **Aspetto** | nana giovane |

**Comparse**

| Chi | Com'è | Come parla |
|---|---|---|
| la guardia della porta | vecchio, zoppo | a monosillabi |

**BRYNJA:** *«Trenta.»*

### SCENA 2 — Il campo
"""


def regole(testo: str, profilo: dict) -> "list[tuple[str, str, str]]":
    return cs.analizza(testo, profilo, [])


class TestLeRegoleMordono(unittest.TestCase):

    def test_la_scena_scritta_bene_passa(self):
        ril = [r for r in regole(BUONA, SEVERO) if r[1] == "SCENA 1"]
        self.assertEqual(ril, [])

    def test_C1_scena_senza_box(self):
        ril = regole(BUONA, LEGGERO)
        self.assertIn(("C1", "SCENA 2", "nessun box read-aloud"), ril)

    def test_C2_chi_parla_senza_scheda(self):
        t = BUONA.replace("**BRYNJA:**", "**GUNNVOR:**")
        self.assertIn(("C2", "SCENA 1", "GUNNVOR"), regole(t, LEGGERO))

    def test_C3_manca_la_riga_in_scena(self):
        t = BUONA.replace("**In scena**", "**Chi c'è**")
        self.assertIn(("C3", "SCENA 1", "manca la riga **In scena**"), regole(t, SEVERO))

    def test_C3_luogo_senza_box(self):
        t = BUONA.replace("Dove: la cappella", "Dove: la cappella · le gallerie")
        self.assertTrue(any(r[0] == "C3" and "gallerie" in r[2] for r in regole(t, SEVERO)))

    def test_C3_persona_senza_scheda_ne_comparsa(self):
        t = BUONA.replace("· la guardia della porta —", "· l'araldo —").replace(
            "Chi: Sorella Brynja · la guardia della porta", "Chi: Sorella Brynja · l'araldo")
        self.assertTrue(any(r[0] == "C3" and "araldo" in r[2] for r in regole(t, SEVERO)))

    def test_C4_scheda_fuori_dal_contratto(self):
        t = BUONA.replace("Chi: Sorella Brynja · la guardia della porta", "Chi: la guardia della porta")
        self.assertTrue(any(r[0] == "C4" and "brynja" in r[2] for r in regole(t, SEVERO)))

    def test_lo_storico_non_conta(self):
        t = BUONA.replace("**BRYNJA:**", "<!-- storico -->\n**GUNNVOR:** *«x»*\n<!-- /storico -->\n**BRYNJA:**")
        self.assertNotIn(("C2", "SCENA 1", "GUNNVOR"), regole(t, LEGGERO))


class TestIlRepo(unittest.TestCase):

    def test_il_cancello_e_verde(self):
        _, nuovi, scaduti = cs.esegui(cs.carica_config())
        self.assertEqual(nuovi, [], "rilievi non dichiarati: python3 scripts/copertura_scene.py")
        self.assertEqual(scaduti, [], "residui che non si verificano più: vanno tolti")

    def test_ogni_residuo_ha_la_ragione(self):
        for r in cs.carica_config()["residui"]:
            self.assertTrue(r.get("perche", "").strip(), f"residuo senza ragione: {r}")

    def test_ogni_master_senza_contratto_dice_perche(self):
        for m in cs.carica_config()["moduli"]:
            if not m.get("contratto"):
                self.assertTrue(m.get("perche", "").strip(), f"{m['file']}: senza contratto e senza ragione")


class TestLaCopiaDiBalvar(unittest.TestCase):
    """Il DM vuole i numeri di Balvar nel modulo, non solo nel Bestiario
    (2026-09-26). Una seconda copia diverge alla prima errata: questo test è
    il prezzo della ripetizione, e la rende sicura."""

    #: I numeri, non le etichette: il Bestiario scrive «hp 96», il modulo «pf 96».
    NUMERI = (r"(?:pf|hp):? 96", r"ca:? 24", r"vol \+17", r"sag 20", r"bab \+8",
              r"lotta \+9", r"\+10/\+5 \(1d8\+2\)")

    def test_i_numeri_sono_gli_stessi(self):
        import re
        bestiario = (ROOT / "Bestiario/villain/balvar-fuocospento-cr13.md").read_text(encoding="utf-8")
        modulo = (ROOT / "07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md").read_text(encoding="utf-8")
        a4 = modulo.split("### A.4 · Balvar Fuocospento", 1)[1].split("### A.5", 1)[0]
        piano = lambda s: re.sub(r"[*_`]", "", s).lower()
        for n in self.NUMERI:
            self.assertRegex(piano(bestiario), n, f"il Bestiario non dice più «{n}»")
            self.assertRegex(piano(a4), n, f"DEF-4 A.4 non dice più «{n}»: allinea le due copie")


if __name__ == "__main__":
    unittest.main()
