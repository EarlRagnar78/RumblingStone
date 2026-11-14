"""I linguaggi automatici di una scheda (ADR-0126, lotto 7, quarta parte).

La razza dà i suoi linguaggi e il druido il Druidico: i nomi vengono dalla
tabella `[linguaggi]` del plugin 3.5, estratta dall'SRD."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402
from dmcore import sistemi as S  # noqa: E402
from tests.test_difese import SCHEDA  # noqa: E402


def giudica(coda: str, razza: str = "dwarf", classe: str = "Fighter 3", dadi: str = "3d10+6",
            titolo: str = "Prova") -> list:
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / "prova-cr4.md"
        q.write_text(SCHEDA.format(titolo=titolo, tipo=f"Medium humanoid ({razza})", classe=classe, dadi=dadi,
                                   coda=coda), encoding="utf-8")
        if V.L.leggi(q) is None:
            raise AssertionError("la scheda di prova non si legge")
        v, n = V.linguaggi(q)
    assert n == []
    return [(x["regola"], x["atteso"], x["testo"]) for x in v]


class TestDati(unittest.TestCase):
    def test_razze_e_druido(self):
        d = S.dati("dnd35", "creature.costruzione")["linguaggi"]
        self.assertEqual(d["razze"], {"dwarf": ["Common", "Dwarven"], "elf": ["Common", "Elven"],
                                      "gnome": ["Common", "Gnome"], "half-elf": ["Common", "Elven"],
                                      "half-orc": ["Common", "Orc"], "halfling": ["Common", "Halfling"],
                                      "human": ["Common"],
                                      "aasimar": ["Common", "Celestial"], "drow": ["Common", "Elven", "Undercommon"],
                                      "duergar": ["Common", "Dwarven", "Undercommon"],
                                      "goblin": ["Common", "Goblin"], "hobgoblin": ["Common", "Goblin"],
                                      "kobold": ["Draconic"], "orc": ["Common", "Orc"],
                                      "svirfneblin": ["Undercommon", "Gnome", "Common"],
                                      "tiefling": ["Common", "Infernal"]})
        self.assertEqual(d["classi"], {"druid": ["Druidic"]})
        for voci in list(d["razze"].values()) + list(d["classi"].values()):
            self.assertLessEqual(set(voci), set(d["nomi"]))

    def test_pf1e_non_ha_la_tabella(self):
        self.assertNotIn("linguaggi", S.dati("pf1e", "creature.costruzione"))


class TestLinguaggi(unittest.TestCase):
    def test_nano_in_regola(self):
        self.assertEqual(giudica("**Linguaggi** Comune, Nanico, Gigante"), [])
        self.assertEqual(giudica("Scurovisione 18 m. Linguaggi: Comune, Nanico."), [])
        self.assertEqual(giudica("**Languages**: Common, Dwarven"), [])

    def test_nano_senza_il_nanico(self):
        v = giudica("**Linguaggi** Comune, Gigante")
        self.assertEqual(len(v), 1)
        self.assertEqual(v[0][:2], ("tratti.linguaggi", ["Common", "Dwarven"]))
        self.assertIn("non ha Dwarven", v[0][2])

    def test_mezzorco_e_umano(self):
        self.assertEqual(giudica("**Linguaggi** Comune, Orchesco", razza="half-orc"), [])
        self.assertEqual(len(giudica("**Linguaggi** Comune, Goblin", razza="half-orc")), 1)
        self.assertEqual(giudica("**Linguaggi** Comune, Shaaran", razza="human"), [])
        self.assertEqual(len(giudica("**Linguaggi** Shaaran", razza="human")), 1)

    def test_razze_senza_dadi_vita_razziali(self):
        """Hobgoblin, orco, drow, duergar, coboldo: SRD, capitolo dei mostri, «… as Characters»."""
        hob = {"razza": "goblinoid", "titolo": "Hobgoblin sergente"}
        self.assertEqual(giudica("**Linguaggi** Comune, Goblin", **hob), [])
        v = giudica("**Linguaggi** Comune, Infernale", **hob)
        self.assertEqual(len(v), 1)
        self.assertEqual(v[0][1], ["Common", "Goblin"])
        self.assertIn("hobgoblin", v[0][2])
        orco = {"razza": "orc", "titolo": "Orco razziatore"}
        self.assertEqual(giudica("**Linguaggi** Comune, Orchesco", **orco), [])
        self.assertEqual(len(giudica("**Linguaggi** Orchesco", **orco)), 1)
        drow = {"razza": "elf", "titolo": "Drow esploratrice"}
        self.assertEqual(giudica("**Linguaggi** Comune, Elfico, Sottocomune", **drow), [])
        self.assertIn("Undercommon", giudica("**Linguaggi** Comune, Elfico", **drow)[0][2])
        duergar = {"razza": "dwarf", "titolo": "Duergar guardia"}
        self.assertIn("Undercommon", giudica("**Linguaggi** Comune, Nanico", **duergar)[0][2])
        coboldo = {"razza": "reptilian", "titolo": "Coboldo stregone"}
        self.assertEqual(giudica("**Linguaggi** Draconico", **coboldo), [])
        self.assertEqual(len(giudica("**Linguaggi** Comune", **coboldo)), 1)

    def test_un_modello_nel_titolo_ferma_il_giudizio(self):
        self.assertEqual(giudica("**Linguaggi** Infernale", razza="goblinoid", titolo="Hobgoblin mezzo-immondo"), [])

    def test_il_druido_ha_il_druidico(self):
        d = {"razza": "human", "classe": "Druid 5", "dadi": "5d8+10"}
        self.assertEqual(giudica("**Linguaggi** Comune, Druidico, Silvano", **d), [])
        v = giudica("**Linguaggi** Comune, Silvano", **d)
        self.assertEqual(len(v), 1)
        self.assertIn("Druidic", v[0][2])

    def test_chi_non_scrive_la_riga_non_si_giudica(self):
        self.assertEqual(giudica(""), [])

    def test_due_righe_o_una_riga_di_storia(self):
        self.assertEqual(giudica("**Linguaggi** Comune\n**Linguaggi** Gigante"), [])
        self.assertEqual(giudica("**Linguaggi** Comune, Nanico\n> era: Linguaggi Comune"), [])

    def test_una_razza_fuori_dalla_tabella(self):
        self.assertEqual(giudica("**Linguaggi** Goblin", razza="goblinoid"), [])
        self.assertEqual(giudica("**Linguaggi** Gnoll", razza="gnoll", titolo="Gnoll predone"), [])
        # il drow è nella tabella dal lotto delle razze senza dadi vita razziali
        self.assertEqual(len(giudica("**Linguaggi** Sottocomune", razza="elf, drow")), 1)


class Bestiario(unittest.TestCase):
    def test_il_bestiario_non_ha_scarti(self):
        trovate = []
        for p in sorted((ROOT / "Bestiario").rglob("*.md")):
            trovate += [f"{x['file']}:{x['riga']} {x['testo']}" for x in V.linguaggi(p)[0]]
        self.assertEqual(trovate, [])


if __name__ == "__main__":
    unittest.main()
