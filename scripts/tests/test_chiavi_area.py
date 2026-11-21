"""Le chiavi d'area sulle piante (ADR-0122, S2): la terza parte di `@zone`
è la chiave che il testo usa nei titoli, e la pianta stampa quella al posto
della lettera."""

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import render_map_svg as R  # noqa: E402


class TestChiaviArea(unittest.TestCase):
    def test_terza_parte_di_zone(self):
        ann = R.parse_annotations(["@zone A1-B2 ; Telo est ; c1", "@zone C3-C3 ; Palo"])
        self.assertEqual(ann["zones"][0]["codice"], "C1")
        self.assertIsNone(ann["zones"][1]["codice"])

    def test_un_punto_e_virgola_nel_testo_non_e_una_chiave(self):
        ann = R.parse_annotations(["@zone K5-L7 ; Rocce di copertura (+4 CA; riparo per Nascondersi)",
                                   "@zone S15-AT32 ; Mercato coperto; dal tetto si vede la pista"])
        self.assertEqual([z["codice"] for z in ann["zones"]], [None, None])

    def test_lettera_o_chiave(self):
        ann = R.parse_annotations(["@zone A1-B2 ; Telo est ; C1", "@zone C3-C3 ; Palo"])
        self.assertEqual(R._lettera_zona(0, ann["zones"][0]), "C1")
        self.assertEqual(R._lettera_zona(1, ann["zones"][1]), "b")
        self.assertEqual(R._lettera_zona(1), "b")

    def test_le_piante_di_arc07_hanno_le_chiavi(self):
        radice = SCRIPTS.parent / "07_il Portale Della Forgia Eterna" / "Mappe"
        for nome, attese in (("ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.md", {"C1", "C2", "C3", "C4", "C5", "C6"}),
                             ("ARC07-MAPPE-M7H-QUARTIERE-DEL-COMANDO.md", {"C1", "C2", "C3", "C4", "C5", "H1"})):
            righe = [r for r in (radice / nome).read_text(encoding="utf-8").splitlines() if r.startswith("@zone")]
            codici = {R.parse_annotations([r])["zones"][0]["codice"] for r in righe}
            self.assertEqual(codici, attese, nome)

    def test_lo_schema_delle_mappe_dichiara_la_chiave(self):
        """Lo schema ha `additionalProperties: false`: senza `codice` dichiarato,
        le piante M7-C e M7-H non passano più la validazione dello schema."""
        import json
        import re
        schema = json.loads((SCRIPTS / "schemas" / "tactical_map.schema.json").read_text(encoding="utf-8"))
        radice = SCRIPTS.parent / "07_il Portale Della Forgia Eterna" / "Mappe"
        for chiave in ("structures", "hazards"):
            voce = schema["properties"][chiave]["items"]["properties"]["codice"]
            self.assertEqual(voce["pattern"], "^[A-Z]{1,2}[0-9]{1,2}$")
            for nome in ("ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.json", "ARC07-MAPPE-M7H-QUARTIERE-DEL-COMANDO.json"):
                spec = json.loads((radice / nome).read_text(encoding="utf-8"))
                for obj in spec.get(chiave, []) or []:
                    if "codice" in obj:
                        self.assertRegex(obj["codice"], voce["pattern"], nome)
                        self.assertTrue(R._CHIAVE_AREA.fullmatch(obj["codice"]), nome)


if __name__ == "__main__":
    unittest.main()
