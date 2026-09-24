"""Il CR del catalogo viene dal blocco, non dalla prima creatura nominata nel testo.

🐛 **Il difetto, misurato il 2026-09-23.** `extract_cr` provava i suoi modelli in
un ordine fisso su tutto il testo, «CR» prima di «GS». Una scheda che scrive il
proprio livello come «GS 15» e nomina un'altra creatura con «CR 18» finiva nel
catalogo col CR dell'altra. Tre schede su tre casi misurati:

| scheda | catalogo | blocco | di chi era il CR |
|---|---:|---:|---|
| Azarr Kul | 18 | **15** | Tyrgarun, il drago blu che non e' la sua cavalcatura |
| Sonjak | 14 | **13** | Urialle, la yochlol che manda |
| Lythiel | 5 | **8** | Inathiel, il suo gufo |

`suggest_encounter` e il server MCP leggono il catalogo: Lythiel risultava un
alleato da GS 5.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import build_monster_catalog as B  # noqa: E402

SCHEDA = ("# Azarr Kul\n\n```statblocco\ngs: 15\nca: 28\npf: 119\n```\n\n"
          "**Grado di Sfida (GS):** 15\n\n### Tyrgarun (Drago Blu Vecchio, CR 18)\n")


class TestGsDalBlocco(unittest.TestCase):
    def test_il_blocco_batte_la_creatura_nominata(self):
        # la prova che morde: senza il blocco, vince il «CR 18» di Tyrgarun
        self.assertEqual(B.extract_cr(SCHEDA), 15.0)
        self.assertEqual(B.extract_cr(SCHEDA.replace("gs: 15\n", "")), 18.0)

    def test_mezzo_grado(self):
        self.assertEqual(B.extract_cr("```statblocco\ngs: 1/2\nca: 12\n```\n"), 0.5)

    def test_senza_blocco_resta_il_testo(self):
        self.assertEqual(B.extract_cr("**CR**: 7\n"), 7.0)

    def test_le_tre_schede_vere(self):
        import yaml
        cat = yaml.safe_load((ROOT / "scripts/monster_catalog.yaml").read_text(encoding="utf-8"))
        per_file = {r["source_file"]: r["cr"] for r in cat["monsters"]}
        for f, gs in (("Bestiario/villain/Azarr_Kul/Azarr_Kul/Azarr_Kul.md", 15.0),
                      ("Bestiario/villain/Sonjak/Sonjak.md", 13.0),
                      ("Bestiario/png/Lythiel/Lythiel.md", 8.0)):
            self.assertEqual(per_file[f], gs, f)


if __name__ == "__main__":
    unittest.main()
