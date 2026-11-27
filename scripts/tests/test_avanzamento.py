"""L'avanzamento d'incantatore delle classi di prestigio (ADR-0126, lotto 3-ter)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verifica_scheda as V  # noqa: E402
from dmcore import prestigio as PR  # noqa: E402

SCHEDA = """# Prova

**Sistema:** D&D 3.5

tipo: Medium humanoid (human), {tipo}, N

**Caratteristiche** For 10, Des 10, Cos 10, Int 10, Sag 18, Car 10

**Incantesimi da chierico** ({testa}):
- 3° (CD 17): *preghiera*, *dissolvi magie*, *animare morti* (D)
- 0: *guida*
"""
# chierico di 5°, Sag 18: 5/4+1/3+1/2+1
CINQUE = "5/4+1/3+1/2+1 al giorno"


def giudica(tipo: str, testa: str):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "prova.md"
        p.write_text(SCHEDA.format(tipo=tipo, testa=testa), encoding="utf-8")
        v, n = V.incantatori(p)
    return [(x["regola"], x["ha"], x["atteso"]) for x in v], [x["testo"] for x in n]


class TestLaListaSiLanciaDalLivelloCheLeClassiDanno(unittest.TestCase):
    def test_il_loremaster_avanza_a_ogni_livello(self):
        self.assertEqual(giudica("Chierico 3 / Loremaster 2", f"LI 5°; {CINQUE}"), ([], []))

    def test_l_assassino_non_avanza(self):
        v, _ = giudica("Chierico 3 / Assassin 2", f"LI 5°; {CINQUE}")
        self.assertIn(("numero.incantesimi.livello_incantatore", 5, 3), v)

    def test_il_cavaliere_mistico_non_avanza_una_lista_divina(self):
        v, _ = giudica("Chierico 3 / Eldritch Knight 2", f"LI 5°; {CINQUE}")
        self.assertIn(("numero.incantesimi.livello_incantatore", 5, 3), v)

    def test_senza_livello_scritto_la_lista_prende_quello_delle_classi(self):
        # prima la lista si giudicava da chierico 3 e gli slot di 5° erano violazioni
        self.assertEqual(giudica("Chierico 3 / Loremaster 2", CINQUE), ([], []))

    def test_senza_classe_di_prestigio_non_cambia_nulla(self):
        self.assertEqual(giudica("Chierico 5", f"LI 5°; {CINQUE}"), ([], []))

    def test_una_classe_dei_manuali_senza_avanzamento_e_un_dubbio(self):
        v, n = giudica("Chierico 3 / Hammer of Moradin 2", f"LI 5°; {CINQUE}")
        self.assertFalse([x for x in v if x[0].endswith("livello_incantatore")])
        self.assertTrue(any("non giudicabile" in x for x in n))


class TestAvanzamento(unittest.TestCase):
    def test_i_tipi(self):
        self.assertEqual(PR.avanzamento("wizard", [("eldritch knight", 2)], [])[::2], (1, None))
        self.assertEqual(PR.avanzamento("cleric", [("eldritch knight", 5)], [])[::2], (0, None))
        self.assertEqual(PR.avanzamento("wizard", [("archmage", 3)], [])[::2], (3, None))
        self.assertEqual(PR.avanzamento("wizard", [("assassin", 4)], [])[::2], (0, None))

    def test_il_teurgo_mistico_avanza_una_arcana_e_una_divina(self):
        self.assertEqual(PR.avanzamento("wizard", [("mystic theurge", 4)], ["cleric"])[::2], (4, None))
        self.assertEqual(PR.avanzamento("cleric", [("mystic theurge", 4)], ["wizard"])[::2], (4, None))
        self.assertIsNotNone(PR.avanzamento("wizard", [("mystic theurge", 4)], ["sorcerer"])[2])

    def test_due_classi_che_possono_prendere_il_livello_sono_un_dubbio(self):
        piu, _, dubbio = PR.avanzamento("wizard", [("loremaster", 2)], ["cleric"])
        self.assertEqual(piu, 2)
        self.assertIn("cleric", dubbio)

    def test_pf1e(self):
        self.assertEqual(PR.avanzamento("wizard", [("dragon disciple", 5)], [], "pf1e")[::2], (3, None))


class TestIDati(unittest.TestCase):
    def test_la_forma(self):
        for sistema in ("dnd35", "pf1e"):
            dati = PR.requisiti(sistema)["prestigio"]
            con = {k: v["avanza"] for k, v in dati.items() if "avanza" in v}
            self.assertTrue(con, sistema)
            for nome, a in con.items():
                if a.get("diverge"):
                    continue
                self.assertTrue(a["tipo"], nome)
                self.assertTrue(a["livelli"] and a["livelli"] == sorted(set(a["livelli"])), nome)

    def test_le_classi_dell_srd(self):
        d = PR.requisiti("dnd35")["prestigio"]
        self.assertEqual(d["archmage"]["avanza"], {"tipo": "arcane", "livelli": [1, 2, 3, 4, 5]})
        self.assertEqual(d["mystic theurge"]["avanza"]["tipo"], "both")
        self.assertEqual(d["eldritch knight"]["avanza"]["livelli"][0], 2)
        for senza in ("assassin", "blackguard", "shadowdancer", "dwarven defender"):
            self.assertNotIn("avanza", d[senza], senza)


if __name__ == "__main__":
    unittest.main()
