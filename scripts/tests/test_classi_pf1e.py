"""Le classi, le griglie e le armature del plugin PF1e (ADR-0119, lotto 2).

I file sono generati da `estrai_prd_pf1e.py` (che ha il suo `--check` in
`test_sistemi_pf1e.py`). Qui le righe sono scritte a mano, lette dalle tabelle del Core Rulebook nel PRD,
non rilette dal generatore: se la lettura delle tabelle cambia, il test lo vede.
"""
from __future__ import annotations

import tomllib
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATI = REPO / "sistemi" / "pf1e" / "dati"


def _toml(nome: str) -> dict:
    return tomllib.loads((DATI / nome).read_text(encoding="utf-8"))


class Classi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = _toml("classi.toml")
        cls.c = cls.d["classi"]

    def test_tutte_le_classi_del_prd(self):
        per_gruppo = {}
        for v in self.c.values():
            per_gruppo[v["gruppo"]] = per_gruppo.get(v["gruppo"], 0) + 1
        self.assertEqual(per_gruppo, {"base": 21, "ibrida": 10, "png": 5, "prestigio": 18, "alternativa": 1})

    def test_righe_note_del_core_rulebook(self):
        attese = {
            "barbarian": (12, 1.0, ["temp"], 4), "bard": (8, 0.75, ["rifl", "vol"], 6),
            "cleric": (8, 0.75, ["temp", "vol"], 2), "druid": (8, 0.75, ["temp", "vol"], 4),
            "fighter": (10, 1.0, ["temp"], 2), "monk": (8, 0.75, ["temp", "rifl", "vol"], 4),
            "paladin": (10, 1.0, ["temp", "vol"], 2), "ranger": (10, 1.0, ["temp", "rifl"], 6),
            "rogue": (8, 0.75, ["rifl"], 8), "sorcerer": (6, 0.5, ["vol"], 2),
            "wizard": (6, 0.5, ["vol"], 2),
            # PNG
            "adept": (6, 0.5, ["vol"], 2), "aristocrat": (8, 0.75, ["vol"], 4),
            "commoner": (6, 0.5, [], 2), "expert": (8, 0.75, ["vol"], 6), "warrior": (10, 1.0, ["temp"], 2),
            # prestigio: in PF1e il TS buono parte da +1, non da +2
            "assassin": (8, 0.75, ["rifl"], 4), "duelist": (10, 1.0, ["rifl"], 4),
            "eldritch knight": (10, 1.0, ["temp"], 2), "mystic theurge": (6, 0.5, ["vol"], 2),
            "shadowdancer": (8, 0.75, ["rifl"], 6),
        }
        for nome, (dv, bab, ts, gradi) in attese.items():
            v = self.c[nome]
            self.assertEqual((v["dv"], v["bab"], v["ts_buoni"], v["gradi"]), (dv, bab, ts, gradi), nome)

    def test_il_dado_vita_pf1e_non_e_quello_3_5(self):
        # le differenze che contano per chi prima usava le tabelle 3.5
        self.assertEqual([self.c[k]["dv"] for k in ("bard", "rogue", "ranger", "sorcerer", "wizard")],
                         [8, 8, 10, 6, 6])

    def test_ogni_classe_ha_il_nome_italiano(self):
        self.assertEqual(sorted(self.d["alias"].values()), sorted(self.c))
        self.assertEqual(self.d["alias"]["guerriero"], "fighter")
        self.assertEqual(self.d["alias"]["chierico"], "cleric")

    def test_i_livelli(self):
        for nome, v in self.c.items():
            self.assertEqual(v["livelli"], 10 if v["gruppo"] == "prestigio" else 20, nome)


class Griglie(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = _toml("classi.toml")
        cls.g, cls.i = cls.d["griglie"], cls.d["incantatori"]

    def test_al_giorno_righe_note(self):
        attese = {
            ("wizard", 1): [3, 1], ("wizard", 5): [4, 3, 2, 1], ("wizard", 20): [4] * 10,
            # il +1 di dominio non è nella griglia
            ("cleric", 1): [3, 1], ("cleric", 9): [4, 4, 4, 3, 2, 1], ("druid", 20): [4] * 10,
            # nessun livello 0 al giorno: lo 0 in testa è d'allineamento
            ("sorcerer", 1): [0, 3], ("sorcerer", 4): [0, 6, 3], ("sorcerer", 20): [0] + [6] * 9,
            ("bard", 1): [0, 1], ("bard", 4): [0, 3, 1], ("bard", 20): [0, 5, 5, 5, 5, 5, 5],
            # ranger e paladino: «0» al 4° vuol dire solo gli incantesimi bonus
            ("paladin", 4): [0, 0], ("paladin", 5): [0, 1], ("paladin", 20): [0, 4, 4, 3, 3],
            ("ranger", 7): [0, 1, 0], ("ranger", 13): [0, 3, 2, 1, 0], ("ranger", 20): [0, 4, 4, 3, 3],
            ("adept", 1): [3, 1], ("adept", 20): [3, 3, 3, 3, 3, 2],
        }
        for (nome, liv), riga in attese.items():
            self.assertEqual(self.g[nome][str(liv)], riga, f"{nome} {liv}°")

    def test_ranger_e_paladino_non_lanciano_prima_del_quarto(self):
        for nome in ("ranger", "paladin", "antipaladin", "bloodrager"):
            self.assertEqual(min(int(k) for k in self.g[nome]), 4, nome)

    def test_conosciuti_righe_note(self):
        con = self.d["conosciuti"]
        self.assertEqual(con["sorcerer"]["1"], [4, 2])
        self.assertEqual(con["sorcerer"]["20"], [9, 5, 5, 4, 4, 4, 3, 3, 3, 3])
        self.assertEqual(con["bard"]["1"], [4, 2])
        self.assertEqual(con["bard"]["10"], [6, 5, 5, 4, 2])
        self.assertEqual(con["bard"]["20"], [6, 6, 6, 6, 6, 5, 5])
        self.assertEqual(sorted(con), ["bard", "bloodrager", "hunter", "inquisitor", "oracle", "skald",
                                       "sorcerer", "summoner"])

    def test_le_bandiere(self):
        self.assertTrue(self.i["cleric"]["slot_di_dominio"])
        self.assertFalse(self.i["druid"]["slot_di_dominio"])
        self.assertEqual(sorted(k for k, v in self.i.items() if v["estratti"]), ["alchemist", "investigator"])
        # trucchetti e orazioni: chi li ha (a volontà in PF1e) e chi no
        senza_zero = sorted(k for k, v in self.i.items() if not v["livello_zero"])
        self.assertEqual(senza_zero, ["alchemist", "antipaladin", "bloodrager", "investigator", "paladin", "ranger"])

    def test_ogni_rimando_esiste_e_le_righe_crescono(self):
        for nome, v in self.i.items():
            for campo, tab in (("griglia", "griglie"), ("conosciuti", "conosciuti"), ("preparati", "preparati")):
                if campo not in v:
                    continue
                righe = self.d[tab][v[campo]]
                lunghezze = [len(righe[k]) for k in sorted(righe, key=int)]
                self.assertEqual(lunghezze, sorted(lunghezze), f"{nome} {tab}")
                self.assertEqual(max(int(k) for k in righe), 20, f"{nome} {tab}")

    def test_prestigio_che_avanza_gli_incantesimi(self):
        av = self.d["avanza_incantatore"]
        self.assertEqual(av["mystic theurge"], list(range(1, 11)))
        self.assertEqual(av["eldritch knight"], list(range(2, 11)))
        self.assertEqual(av["dragon disciple"], [2, 3, 4, 6, 7, 8, 10])
        self.assertNotIn("assassin", av)


class Armature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = _toml("creature.toml")

    def test_armature_del_core_rulebook(self):
        a = self.c["armature"]
        self.assertEqual(len(a), 12)
        attese = {"padded": (1, 8, 0), "leather": (2, 6, 0), "studded leather": (3, 5, -1),
                  "chain shirt": (4, 4, -2), "hide": (4, 4, -3), "scale mail": (5, 3, -4),
                  "chainmail": (6, 2, -5), "breastplate": (6, 3, -4), "splint mail": (7, 0, -7),
                  "banded mail": (7, 1, -6), "half-plate": (8, 0, -7), "full plate": (9, 1, -6)}
        for nome, (ca, des, prova) in attese.items():
            v = a[nome]
            self.assertEqual((v["ca"], v["des_max"], v["prova"]), (ca, des, prova), nome)

    def test_le_armature_che_cambiano_dal_3_5(self):
        # rispetto al 3.5 cambiano l'armatura completa (9), la cotta di maglia (6) e la pelle (4)
        a = self.c["armature"]
        self.assertEqual((a["full plate"]["ca"], a["chainmail"]["ca"], a["hide"]["ca"],
                          a["scale mail"]["ca"], a["splint mail"]["ca"], a["banded mail"]["ca"],
                          a["half-plate"]["ca"], a["breastplate"]["ca"]), (9, 6, 4, 5, 7, 7, 8, 6))

    def test_pf_bonus_dei_costrutti_dalle_schede_del_bestiary(self):
        # la tabella nel PSRD-Data non c'è: i numeri vengono dalle schede (golem di ferro
        # Large 18d10+30, oggetto animato Small 2d10+10, homunculus Tiny 2d10)
        p = self.c["pf_bonus_costrutti"]
        self.assertEqual(p, {"fine": 0, "diminutive": 0, "tiny": 0, "small": 10, "medium": 20,
                             "large": 30, "huge": 40, "gargantuan": 60, "colossal": 80})
        # Fine e Diminutive non hanno schede: vengono dalla tabella del PRD pubblicato
        # («—»), che per le altre taglie concorda con le schede (l'estrattore lo esige)
        self.assertEqual(set(p), set(self.c["taglie"]))

    def test_scudi(self):
        s = self.c["scudi"]
        self.assertEqual({k: v["ca"] for k, v in s.items()},
                         {"buckler": 1, "shield, light wooden": 1, "shield, light steel": 1,
                          "shield, heavy wooden": 2, "shield, heavy steel": 2, "shield, tower": 4})
        self.assertEqual(s["shield, tower"]["des_max"], 2)
        self.assertEqual(s["shield, tower"]["prova"], -10)

    def test_tipi_e_taglie_restano(self):
        self.assertEqual(len(self.c["tipi"]), 13)
        self.assertEqual(len(self.c["taglie"]), 9)



class ListeDiClasse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = _toml("liste_incantesimi.toml")
        cls.l = cls.d["liste"]

    def test_ogni_incantatore_ha_la_sua_lista(self):
        self.assertEqual(sorted(self.l), sorted(_toml("classi.toml")["incantatori"]))

    def test_incantesimi_noti_al_loro_livello(self):
        attesi = [("wizard", 0, "Detect Magic"), ("wizard", 1, "Magic Missile"), ("wizard", 3, "Fireball"),
                  ("wizard", 9, "Wish"), ("sorcerer", 3, "Fireball"), ("cleric", 1, "Cure Light Wounds"),
                  ("cleric", 9, "Miracle"), ("druid", 1, "Entangle"), ("bard", 1, "Cure Light Wounds"),
                  ("bard", 3, "Haste"), ("paladin", 1, "Bless"), ("ranger", 1, "Entangle"),
                  ("adept", 3, "Lightning Bolt"), ("witch", 1, "Cure Light Wounds"), ("magus", 1, "Shocking Grasp"),
                  ("alchemist", 1, "Cure Light Wounds"), ("antipaladin", 1, "Inflict Light Wounds")]
        for classe, livello, nome in attesi:
            self.assertIn(nome, self.l[classe][str(livello)], f"{classe} {livello}°")

    def test_il_livello_cambia_con_la_classe(self):
        # lo stesso incantesimo a livelli diversi: è il motivo per cui la lista è per classe
        self.assertIn("Haste", self.l["wizard"]["3"])
        self.assertIn("Haste", self.l["summoner"]["2"])
        self.assertNotIn("Fireball", self.l["cleric"].get("3", []))

    def test_stregone_e_mago_hanno_la_stessa_lista(self):
        self.assertEqual(self.l["sorcerer"], self.l["wizard"])

    def test_i_livelli_stanno_nella_griglia_della_classe(self):
        inc = _toml("classi.toml")
        for classe, livelli in self.l.items():
            tetto = max(len(r) for r in inc["griglie"][classe].values()) - 1
            self.assertLessEqual(max(int(k) for k in livelli), tetto, classe)

    def test_ogni_nome_ha_il_libro_e_nessun_mitico(self):
        nomi = {n for livelli in self.l.values() for voci in livelli.values() for n in voci}
        self.assertEqual(nomi, set(self.d["libro"]))
        self.assertEqual([n for n in nomi if n.startswith("Mythic ")], [])
        self.assertEqual(sum(1 for v in self.d["libro"].values() if v == "cr"), 623)

    def test_il_warpriest_si_ferma_al_sesto(self):
        # il PRD gli copia la lista del chierico fino al 9°: i livelli sopra la griglia non entrano
        self.assertEqual(max(int(k) for k in self.l["warpriest"]), 6)
        self.assertEqual(self.l["warpriest"]["6"], self.l["cleric"]["6"])

    def test_nomi_italiani(self):
        it = self.d["nomi_it"]
        self.assertEqual(it["Fireball"], "Palla di Fuoco")
        self.assertLessEqual(set(it), set(self.d["libro"]))
        self.assertGreater(len(it), 1400)


if __name__ == "__main__":
    unittest.main()
