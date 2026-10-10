"""Test di memoria.py (ADR-0087): la memoria del lavoro, generata dal repo."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import memoria as me  # noqa: E402


class TestLaListaViva(unittest.TestCase):
    TESTO = ("## 0 · 🧭 Adesso\n\n| | Cosa | Classe | Dove | Da dove |\n|---|---|---|---|---|\n"
             "| ✅ | fatto | M | §1 | fatto |\n"
             "| ▶ | **in corso** con `a|b` | K | [X](PIANO-X.md) | agente |\n"
             "| 🙋 | al DM | K | §4 | DM |\n\n## 1 · Altro\n")

    def test_tiene_solo_cio_che_non_e_fatto(self):
        viva = me.lista_viva(self.TESTO)
        self.assertEqual(len(viva["▶"]), 1)
        self.assertEqual(len(viva["🙋"]), 1)
        self.assertNotIn("✅", viva)

    def test_il_codice_in_linea_non_spezza_le_celle(self):
        self.assertEqual(me.lista_viva(self.TESTO)["▶"][0][0], "**in corso** con `a|b`")


class TestITesti(unittest.TestCase):
    def test_i_link_di_plans_si_riscrivono_dalla_radice(self):
        self.assertEqual(me._dalla_radice("vedi [X](PIANO-X.md) e [A](adr/ADR-1.md)"),
                         "vedi [X](plans/PIANO-X.md) e [A](plans/adr/ADR-1.md)")
        self.assertEqual(me._dalla_radice("[D](../docs/a.md) [W](https://x.y)"),
                         "[D](docs/a.md) [W](https://x.y)")

    def test_il_taglio_non_spezza_un_link(self):
        s = me._corto("parole " * 20 + "[un link lungo](PIANO-LUNGO.md) e poi", 150)
        self.assertNotIn("[un link", s)
        self.assertTrue(s.endswith("…"))

    def test_il_taglio_non_lascia_codice_aperto(self):
        s = me._corto("x " * 40 + "`codice lungo che non finisce`", 90)
        self.assertEqual(s.count("`") % 2, 0)


class TestSulRepoVero(unittest.TestCase):
    def test_e_deterministica(self):
        self.assertEqual(me.rendi(), me.rendi())

    def test_la_memoria_committata_e_allineata(self):
        self.assertEqual(me.main(["--check"]), 0,
                         "MEMORIA.md è indietro: `python3 scripts/memoria.py`")

    def test_ogni_link_esiste(self):
        import re
        testo = me.rendi()
        for link in re.findall(r"\]\(([^)#\s]+)\)", testo):
            if link.startswith("http"):
                continue
            with self.subTest(link=link):
                self.assertTrue((me.RADICE / link).exists(), link)
