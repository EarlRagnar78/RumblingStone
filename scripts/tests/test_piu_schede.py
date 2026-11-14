#!/usr/bin/env python3
"""Un file con più schede si giudica scheda per scheda: velocità, linguaggi, abilità (ADR-0126)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import verifica_scheda as V  # noqa: E402
from tests.test_difese import SCHEDA  # noqa: E402


def master(verifica, *schede: "tuple[str, str]", classe: str = "Fighter 3", cambia=None) -> "tuple[list, list]":
    """Un master di prova: una scheda per coppia (razza, coda), coi titoli «Scheda 1», «Scheda 2»…"""
    pezzi = [SCHEDA.format(coda=coda, titolo=f"Scheda {k + 1}", tipo=f"Medium humanoid ({razza})", classe=classe,
                           dadi="3d10+6").replace("# Scheda", "## Scheda") for k, (razza, coda) in enumerate(schede)]
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / "master.md"
        testo = "# Arco di prova\n\n" + "\n\n".join(pezzi)
        q.write_text(cambia(testo) if cambia else testo, encoding="utf-8")
        return verifica(q)


class TestLinguaggi(unittest.TestCase):
    def test_il_nano_senza_il_nanico_esce_col_suo_titolo(self):
        buona, manca = "**Linguaggi** Comune, Nanico", "**Linguaggi** Comune, Gigante"
        v, n = master(V.linguaggi, ("dwarf", buona), ("dwarf", manca), ("dwarf", buona))
        self.assertEqual([(x["scheda"], x["regola"]) for x in v], [("Scheda 2 [INFERRED]", "tratti.linguaggi")])
        self.assertEqual(n, [])
        self.assertGreater(v[0]["riga"], SCHEDA.count("\n"))

    def test_la_razza_e_quella_della_scheda_non_del_file(self):
        v, _ = master(V.linguaggi, ("human", "**Linguaggi** Comune"), ("dwarf", "**Linguaggi** Comune"))
        self.assertEqual([x["scheda"] for x in v], ["Scheda 2 [INFERRED]"])


class TestVelocita(unittest.TestCase):
    def test_il_nano_a_nove_metri_esce_col_suo_titolo(self):
        # la scheda di prova scrive «velocita: 9 m»: giusta per l'umano, non per il nano (6 m)
        v, n = master(V.velocita, ("human", ""), ("dwarf", ""), ("human", ""))
        self.assertEqual([(x["scheda"], x["atteso"], x["ha"]) for x in v], [("Scheda 2 [INFERRED]", 20, 30)])
        self.assertEqual(n, [])
        self.assertGreater(v[0]["riga"], SCHEDA.count("\n"))


class TestAbilita(unittest.TestCase):
    def test_i_gradi_oltre_il_massimo_escono_col_loro_titolo(self):
        # la riga delle abilità sta nel recinto: «Scalare +25» chiede più gradi del massimo di un guerriero di 3°
        v, _ = master(V.abilita, ("human", ""), ("human", "<troppa>"), ("human", ""),
                      cambia=lambda t: t.replace("Scalare +5\n  - Talenti: Attacco Poderoso, Incalzare\n```\n<troppa>",
                                                 "Scalare +25\n  - Talenti: Attacco Poderoso, Incalzare\n```\n"))
        self.assertTrue(v)
        self.assertEqual({x["scheda"] for x in v}, {"Scheda 2 [INFERRED]"})
        self.assertIn("gradi.massimo", {x["regola"] for x in v})
        self.assertGreater(min(x["riga"] for x in v), SCHEDA.count("\n"))


if __name__ == "__main__":
    unittest.main()
