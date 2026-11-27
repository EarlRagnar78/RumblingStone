"""dmcore.chi_si_incontra: chi si incontra sta nel capitolo (ADR-0107).

Il caso vero è la serata del 2026-11-02: il capitolo del barile cita Zog'tar
sessanta volte e la sua scheda d'entrata, il suo riquadro e la mappa della
tenda stanno in un altro master. Qui lo stesso caso in piccolo.
"""
from __future__ import annotations

import doctest
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import chi_si_incontra as csi  # noqa: E402

MASTER = """# Il master

### SCENA 7 — La tenda

**In scena** — Dove: la tenda — Chi: Zog'tar

**Scheda d'entrata — Zog'tar Deatheye, il generale** *(statistiche:
Appendice A)*

| | |
|---|---|
| **Aspetto** | mezzo-ogre in mithral annerito |
| **Vuole** | Hammerfist |

![Zog'tar Deatheye, il generale](Immagini/zogtar.jpg)

**Mappa M7-C** (Appendice D). I PG entrano da nord.
""" + "\n" * 300 + """
## Appendice A

```statblocco
nome: Zog'tar Deatheye, generale dell'orda
gs: 15
ca: 26
pf: 283
```

**Difesa** CA 26 · pf 283

**Tattiche** Carica chi ha l'arma più grande.

## Appendice D

![M7-C — La tenda del comando](Mappe/m7c.svg)
"""

BARILE = """# Il barile

Il barile cade sulla tenda di Zog'tar. """ + "Zog'tar grida. " * 12 + """
Si tira l'iniziativa. Le coordinate sono quelle di M7-C.
"""


class TestChiSiIncontra(unittest.TestCase):

    def setUp(self):
        self.tmp = TemporaryDirectory()
        d = Path(self.tmp.name)
        (d / "arco").mkdir()
        (d / "arco" / "MASTER.md").write_text(MASTER, encoding="utf-8")
        (d / "arco" / "Mappe").mkdir()
        (d / "arco" / "Mappe" / "m7c.svg").write_text("<svg/>", encoding="utf-8")
        (d / "arco" / "serata").mkdir()
        self.barile = d / "arco" / "serata" / "BARILE.md"
        self.barile.write_text(BARILE, encoding="utf-8")
        self.master = d / "arco" / "MASTER.md"
        self.idx = csi.indice_del_repo(d)

    def tearDown(self):
        self.tmp.cleanup()

    def test_indice(self):
        self.assertIn("zogtar", self.idx.entrate)
        self.assertIn("zogtar", self.idx.riquadri)
        self.assertIn("M7-C", self.idx.mappe)

    def test_nel_master_il_riquadro_va_accanto_alla_scheda(self):
        md, fatto = csi.arricchisci(MASTER, self.master, self.idx)
        righe = md.split("\n")
        scheda = next(i for i, r in enumerate(righe) if r.startswith("**Scheda d'entrata"))
        riquadro = next(i for i, r in enumerate(righe) if r.startswith("```statblocco"))
        self.assertLess(riquadro - scheda, 20)
        self.assertNotIn("**Chi è**", md)                    # non si inventa dal titolo
        self.assertIn("*(statistiche: qui sotto)*", md)
        self.assertIn("Carica chi ha l'arma", md)            # la tattica viaggia col riquadro
        self.assertEqual(md.count("```statblocco"), 1)       # spostato, non copiato
        self.assertIn("il riquadro è accanto alla sua scheda d'entrata", md)
        self.assertTrue(any("mappa M7-C" in x for x in fatto))

    def test_il_capitolo_del_barile_riceve_zogtar_e_la_mappa(self):
        md, fatto = csi.arricchisci(BARILE, self.barile, self.idx)
        self.assertIn("### Chi si incontra in questo capitolo", md)
        self.assertIn("Scheda d'entrata — Zog'tar", md)
        self.assertIn("```statblocco", md)
        # i percorsi delle immagini rifatti dal capitolo che le riceve
        self.assertIn("](../Immagini/zogtar.jpg)", md)
        self.assertIn("](../Mappe/m7c.svg)", md)

    def test_una_pianta_che_non_esiste_non_entra(self):
        (Path(self.tmp.name) / "arco" / "Mappe" / "m7c.svg").unlink()
        self.assertNotIn("M7-C", csi.indice_del_repo(Path(self.tmp.name)).mappe)

    def test_sotto_soglia_niente(self):
        md, fatto = csi.arricchisci("# X\n\nZog'tar passa.\n", self.barile, self.idx)
        self.assertEqual(fatto, [])

    def test_i_pg_non_si_portano(self):
        md, fatto = csi.arricchisci(BARILE, self.barile, self.idx, pg={"zogtar"})
        self.assertNotIn("Chi si incontra", md)

    def test_la_scheda_col_segno_di_blocco_si_riconosce(self):
        # la #305 mette `<!-- blocco: … -->` fra titolo e tabella, per
        # `componenti.py --includi`: la scheda è la stessa
        con = MASTER.replace("Appendice A)*\n\n| | |", "Appendice A)*\n\n<!-- blocco: zogtar-chi -->\n| | |", 1)
        con = con.replace("| **Vuole** | Hammerfist |\n", "| **Vuole** | Hammerfist |\n<!-- /blocco -->\n", 1)
        self.assertIn("<!-- blocco: zogtar-chi -->", con)
        p = csi.schede_entrata(con.split("\n"), self.master)
        self.assertEqual([x.nome for x in p], ["Zog'tar Deatheye, il generale"])
        self.assertTrue(any(r.startswith("![") for r in p[0].righe))   # il ritratto viene con lei

    def test_chi_ha_gia_il_riquadro_nel_capitolo_non_si_riporta(self):
        # il capitolo «Chi c'è stanotte» della #305 ha già il riquadro di Zog'tar
        capitolo = BARILE + "\n```statblocco\nnome: Zog'tar Deatheye, generale dell'orda\ngs: 15\n```\n"
        md, fatto = csi.arricchisci(capitolo, self.barile, self.idx)
        self.assertNotIn("Chi si incontra in questo capitolo", md)
        self.assertEqual(md.count("```statblocco"), 1)

    def test_doctest(self):
        self.assertEqual(doctest.testmod(csi).failed, 0)


if __name__ == "__main__":
    unittest.main()
