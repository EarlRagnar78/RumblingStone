"""Le abilità di classe e il margine vero dei gradi (ADR-0126, lotto 6, prima parte).

Chi ha soltanto livelli di classe, tutti con l'elenco nel plugin, ha il massimo
dimezzato e il costo doppio nelle abilità che non sono di nessuna delle sue
classi; se è di una delle sette razze dell'SRD il margine fisso lascia il posto
a razza e sinergie contate voce per voce."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402
from dmcore import sistemi as S  # noqa: E402

SERGENTE = ROOT / "Bestiario" / "mostri" / "hobgoblin-sergente-cr5.md"   # Fighter 5: Intimidate +7, Listen +3, Spot +3


def _prova(nome: str, testo: str) -> "tuple[list[dict], list[dict]]":
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / nome
        p.write_text(testo, encoding="utf-8")
        return V.abilita(p)


def _umano(testo: str) -> str:
    """Il sergente riscritto come umano, senza la parola «razziale» nelle note."""
    t = re.sub(r"(?i)hobgoblin", "Umano", testo)
    t = re.sub(r"(?i)goblinoid[ei]?", "umano", t)
    return re.sub(r"(?i)razzial\w*|racial", "di razza", t)


class TestDati(unittest.TestCase):
    def setUp(self):
        self.r = S.dati("dnd35", "creature.gradi")

    def test_abilita_di_classe_dall_srd(self):
        d = self.r["di_classe"]
        self.assertEqual(d["warrior"], ["climb", "handle animal", "intimidate", "jump", "ride", "swim"])
        self.assertIn("spellcraft", d["wizard"])
        self.assertIn("knowledge", d["wizard"])                  # tutte le Conoscenze
        self.assertIn("knowledge (religion)", d["cleric"])       # solo alcune
        self.assertNotIn("listen", d["fighter"])
        self.assertIn("hide", d["arcane archer"])                # il punto di troppo della fonte non spezza l'elenco
        self.assertNotIn("expert", d)                            # ne sceglie dieci: nessun elenco
        self.assertEqual(self.r["fuori_classe"], {"costo": 2, "massimo_diviso": 2})

    def test_domini_sinergie_e_razze(self):
        self.assertEqual(self.r["di_dominio"]["trickery"], ["bluff", "disguise", "hide"])
        self.assertEqual(self.r["sinergie"]["diplomacy"], ["bluff", "knowledge", "sense motive"])
        self.assertEqual(self.r["sinergie"]["tumble"], ["jump"])
        self.assertEqual(self.r["razze"]["elf"], {"listen": 2, "search": 2, "spot": 2})
        self.assertEqual(self.r["razze"]["human"], {})
        senza_dv = set(S.dati("dnd35", "creature.costruzione")["mdl"]["razze"]) - {"merfolk"}
        self.assertEqual(set(self.r["razze"]), (set(self.r["razze_nomi"]) - {"altre"}) | senza_dv)

    def test_razza_e_taglia_si_sommano(self):
        """Lotto 6, terza parte: il +4 di taglia a Nascondersi dei Piccoli e le razze senza dadi vita razziali."""
        self.assertEqual(self.r["razze"]["halfling"]["hide"], 4)
        self.assertEqual(self.r["razze"]["gnome"], {"craft": 2, "hide": 4, "listen": 2})
        self.assertEqual(self.r["razze"]["hobgoblin"], {"move silently": 4})
        self.assertEqual(self.r["razze"]["goblin"], {"hide": 4, "move silently": 4, "ride": 4})
        self.assertEqual(self.r["razze"]["orc"], {})
        self.assertEqual(self.r["razze"]["drow"], self.r["razze"]["elf"])                 # sottorazza: tiene l'elfo
        self.assertEqual(self.r["razze"]["duergar"]["move silently"], 4)
        self.assertEqual(self.r["razze"]["duergar"]["appraise"], 2)                       # dal nano
        self.assertEqual(self.r["razze"]["svirfneblin"]["hide"], 8)                       # +4 sottoterra, +4 di taglia
        self.assertEqual(self.r["salto"], {"velocita": 30, "ogni": 10, "meno": 6, "piu": 4})

    def test_ogni_abilita_dei_dati_ha_la_sua_chiave(self):
        chiave = self.r["chiave"]
        nomi = [a for v in self.r["di_classe"].values() for a in v]
        nomi += [a for v in self.r["di_dominio"].values() for a in v]
        nomi += list(self.r["sinergie"]) + [a for v in self.r["sinergie"].values() for a in v]
        nomi += [a for v in self.r["razze"].values() for a in v]
        self.assertEqual([a for a in nomi if a.split(" (")[0] not in chiave], [])


class TestRazza(unittest.TestCase):
    def setUp(self):
        self.r = S.dati("dnd35", "creature.gradi")

    def test_le_sette_razze(self):
        for dove, attesa in (("Medium humanoid (human)", "human"), ("umanoide (nano) Guerriero 6", "dwarf"),
                             ("Elfa, Maga 5", "elf"), ("druido mezzelfo", "half-elf"),
                             ("Half-Elf (elf/human) Bard 8", "half-elf"), ("Mezzorco Barbaro 4", "half-orc")):
            with self.subTest(dove=dove):
                self.assertEqual(V._razza_srd(dove, self.r), attesa)

    def test_sottorazze_e_razze_d_altre_pagine_non_si_riconoscono(self):
        for dove in ("umanoide (nano) duergar Ladro 1", "Drow umanoide (elfo) Fighter 3", "Hobgoblin Fighter 5",
                     "umanoide (orco) Barbaro 2", "Aberrazione", "nano ed elfo insieme"):
            with self.subTest(dove=dove):
                self.assertIsNone(V._razza_srd(dove, self.r))


class TestFuoriClasse(unittest.TestCase):
    def setUp(self):
        self.testo = SERGENTE.read_text(encoding="utf-8")

    def test_la_scheda_vera_e_pulita(self):
        self.assertEqual(V.abilita(SERGENTE), ([], []))

    def test_abilita_fuori_classe_sopra_la_meta_del_massimo(self):
        # Ascoltare non è del guerriero: con 5 dadi vita il massimo è (5 + 3) / 2 = 4
        viol, _ = _prova(SERGENTE.name, self.testo.replace("Listen +3", "Listen +15"))
        self.assertEqual([(v["regola"], v["abilita"], v["atteso"], v["ha"]) for v in viol],
                         [("gradi.massimo.fuori_classe", "listen", "4", 5)])

    def test_la_stessa_altezza_in_un_abilita_di_classe_passa(self):
        # Intimidire è del guerriero: gli stessi 5 gradi minimi stanno sotto il massimo di 8
        viol, _ = _prova(SERGENTE.name, self.testo.replace("Intimidate +7", "Intimidate +14"))
        self.assertEqual(viol, [])

    def test_i_gradi_fuori_classe_costano_il_doppio(self):
        # 5 dadi vita, 2 punti per livello, Int 10: 16 punti. Due abilità fuori classe a 4 gradi
        # minimi ne chiedono 16 da sole, più Intimidire: senza il costo doppio ne basterebbero 8
        viol, _ = _prova(SERGENTE.name, self.testo.replace("Listen +3", "Listen +14").replace("Spot +3", "Spot +14")
                         .replace("Intimidate +7", "Intimidate +12"))
        self.assertEqual([v["regola"] for v in viol], ["gradi.punti"])

    def test_classe_senza_elenco_non_giudica_fuori_classe(self):
        viol, _ = _prova(SERGENTE.name, self.testo.replace("Fighter 5", "Expert 5").replace("Listen +3", "Listen +15"))
        self.assertNotIn("gradi.massimo.fuori_classe", {v["regola"] for v in viol})


class TestMargineVero(unittest.TestCase):
    def setUp(self):
        self.testo = SERGENTE.read_text(encoding="utf-8")

    def test_umano_senza_sinergie_ha_il_margine_del_solo_oggetto(self):
        # Intimidire +10 con Carisma 8: 10 + 1 − 2 = 9 gradi, il massimo è 8
        viol, _ = _prova("umano-sergente-cr5.md", _umano(self.testo).replace("Intimidate +7", "Intimidate +10"))
        self.assertEqual([(v["regola"], v["ha"], v["atteso"]) for v in viol], [("gradi.massimo", 9, 8)])
        self.assertEqual(_prova("umano-sergente-cr5.md", _umano(self.testo).replace("Intimidate +7", "Intimidate +9"))[0], [])

    def test_la_sinergia_conta_solo_se_la_fonte_e_scritta(self):
        # Raggirare dà +2 a Intimidire: con Raggirare nella riga il margine sale a 4
        con = _umano(self.testo).replace("Intimidate +7", "Bluff +1, Intimidate +10")
        self.assertEqual(_prova("umano-sergente-cr5.md", con)[0], [])

    def test_hobgoblin_senza_la_parola_razziale_ha_il_margine_contato(self):
        """Lotto 6, terza parte: l'hobgoblin ha +4 razziale a Muoversi Silenziosamente e niente a Intimidire."""
        pulita = re.sub(r"(?i)razzial\w*|racial", "di razza", self.testo)
        self.assertEqual(_prova(SERGENTE.name, pulita)[0], [])
        viol, _ = _prova(SERGENTE.name, pulita.replace("Intimidate +7", "Intimidate +10"))
        self.assertEqual([(v["regola"], v["ha"], v["atteso"]) for v in viol], [("gradi.massimo", 9, 8)])

    def test_la_velocita_conta_a_saltare(self):
        """SRD, Saltare: +4 ogni 10 piedi sopra i 30, −6 ogni 10 sotto. Umano Fighter 5, For 14 (+2),
        massimo 8, 20 piedi di velocità (la penalità dell'armatura qui non si legge e non conta)."""
        def gradi(salto: str, velocita: str = "20 ft") -> list:
            testo = _umano(self.testo).replace("Intimidate +7", f"Jump {salto}")
            self.assertIn("velocita: 20 ft (armored)", testo)
            testo = testo.replace("velocita: 20 ft (armored)", f"velocita: {velocita} (armored)")
            return [v["ha"] for v in _prova("umano-sergente-cr5.md", testo)[0]]
        self.assertEqual(gradi("+6"), [])                    # 6 − 2 − 2 di margine + 6 di velocità = 8
        self.assertEqual(gradi("+7"), [9])
        self.assertEqual(gradi("+12", "30 ft"), [])          # a 30 piedi la velocità non conta
        self.assertEqual(gradi("+13", "30 ft"), [9])
        self.assertEqual(gradi("+16", "40 ft"), [])          # +4 sopra i 30
        self.assertEqual(gradi("+17", "12 m"), [9])

    def test_chi_non_e_di_una_razza_dell_srd_tiene_il_margine_di_prima(self):
        # lo stesso +10 sull'hobgoblin vero non è una violazione
        self.assertEqual(_prova(SERGENTE.name, self.testo.replace("Intimidate +7", "Intimidate +10"))[0], [])


# Guerriero 4 umano, For 16: Scalare e Nuotare sono di classe, massimo 7 gradi, margine 2 (oggetto).
# Senza armatura Scalare regge fino a +12 (7 + 3 + 2).
ARMATO = """# Prova [INFERRED]
**Faction**: none | **Role**: brute | **Environment**: any | **CR**: 4

```statblocco
gs: 4
tipo: Medium humanoid (human), Fighter 4, LN
ca: {ca}
ca-dettaglio: {dettaglio}
pf: 30
pf-dado: 4d10+8
ts: Temp +6, Rifl +2, Vol +2
attributi: For 16 Des 12 Cos 14 Int 10 Sag 12 Car 8
velocita: 6 m
iniziativa: +1
attacchi:
  - Mischia spada lunga +7 (1d8+3/19-20)
voci:
  - Abilità: {abilita}
  - Talenti: Attacco Poderoso, Incalzare, Arma Focalizzata (spada lunga), Iniziativa Migliorata, Robustezza
```
"""


def _armato(abilita: str, dettaglio: str = "contatto 11, colto alla sprovvista 18 (+8 full plate, +1 Des)",
            ca: int = 19, coda: str = "") -> "list[tuple]":
    viol, nv = _prova("prova-cr4.md", ARMATO.format(ca=ca, dettaglio=dettaglio, abilita=abilita) + coda)
    if any(x["regola"] in ("lettura", "sistema") for x in nv):
        raise AssertionError(f"il conto dei gradi non parte: {nv}")
    return [(v["regola"], v.get("abilita"), v["ha"]) for v in viol]


class TestPenalitaDiArmatura(unittest.TestCase):
    """Lotto 6, seconda parte: l'armatura abbassa il bonus scritto, quindi alza i gradi minimi."""

    def test_i_dati_dall_srd(self):
        pp = S.dati("dnd35", "creature.gradi")["penalita_di_prova"]
        self.assertEqual(pp["abilita"], ["balance", "climb", "escape artist", "hide", "jump", "move silently",
                                         "sleight of hand", "swim", "tumble"])
        self.assertEqual(pp["doppia"], ["swim"])
        self.assertEqual(pp["armature"]["full plate"], {"ca": 8, "des_max": 1, "penalita": 6})
        self.assertEqual(pp["armature"]["leather"]["penalita"], 0)
        self.assertEqual(pp["scudi"]["shield, tower"], {"ca": 4, "penalita": 10})   # il «+4³» della tabella è 4
        self.assertEqual(len(pp["armature"]), 12)
        coppie = [(v["ca"], v["des_max"]) for v in pp["armature"].values()]
        self.assertEqual(len(set(coppie)), 12)      # bonus e Des massima bastano a riconoscere l'armatura

    def test_l_armatura_completa_toglie_cinque_a_scalare(self):
        # perfetta: 6 − 1 = 5. Scalare +7: 7 − 3 − 2 + 5 = 7 gradi, il massimo
        self.assertEqual(_armato("Scalare +7, Intimidire +6"), [])
        self.assertEqual(_armato("Scalare +8, Intimidire +6"), [("gradi.massimo", "climb", 8)])

    def test_senza_armatura_lo_stesso_bonus_passa(self):
        self.assertEqual(_armato("Scalare +12", "contatto 11, colto alla sprovvista 10 (+1 Des)", 11), [])
        self.assertEqual(_armato("Scalare +13", "contatto 11, colto alla sprovvista 10 (+1 Des)", 11),
                         [("gradi.massimo", "climb", 8)])

    def test_un_abilita_che_non_la_subisce_non_cambia(self):
        # Intimidire (Car −1): 7 + (−1) + 2 = +8 è il tetto con e senza armatura
        self.assertEqual(_armato("Intimidire +8"), [])
        self.assertEqual(_armato("Intimidire +9"), [("gradi.massimo", "intimidate", 8)])

    def test_a_nuotare_vale_doppia(self):
        self.assertEqual(_armato("Nuotare +2"), [])                       # 2 − 3 − 2 + 10 = 7
        self.assertEqual(_armato("Nuotare +3"), [("gradi.massimo", "swim", 8)])

    def test_lo_scudo_si_somma(self):
        d = "contatto 11, colto alla sprovvista 20 (+8 full plate, +2 scudo pesante, +1 Des)"
        self.assertEqual(_armato("Scalare +6", d, 21), [])                # 5 + 1 = 6 di penalità
        self.assertEqual(_armato("Scalare +7", d, 21), [("gradi.massimo", "climb", 8)])

    def test_il_mithral_toglie_tre(self):
        d = "contatto 11, colto alla sprovvista 18 (+8 full plate di mithral, +1 Des)"
        self.assertEqual(_armato("Scalare +9", d), [])                    # 6 − 3 = 3 di penalità
        self.assertEqual(_armato("Scalare +10", d), [("gradi.massimo", "climb", 8)])

    def test_il_cuoio_non_ha_penalita(self):
        d = "contatto 11, colto alla sprovvista 12 (+2 leather, +1 Des)"
        self.assertEqual(_armato("Scalare +12", d, 13), [])

    def test_con_due_righe_di_ca_non_si_conta(self):
        # due schede nel file: non si sa di chi è la riga delle abilità, si resta al conto di prima
        coda = "\n**CA** 15 (+4 chain shirt, +1 Des)\n"
        self.assertEqual(_armato("Scalare +12", coda=coda), [])
        self.assertEqual(V._penalita_di_prova("ca-dettaglio: (+8 full plate)" + coda,
                                              S.dati("dnd35", "creature.gradi"), "dnd35"), (0, ""))

    def test_la_penalita_letta(self):
        r = S.dati("dnd35", "creature.gradi")
        for riga, attesa in (("ca-dettaglio: contatto 10 (armatura completa +1, scudo pesante +1, −1 Des)", 6),
                             ("ca-dettaglio: (+4 giaco di maglia, +2 Des)", 1),
                             ("**AC** 17 (+5 breastplate, +2 Dex)", 3),
                             ("ca-dettaglio: (+3 Des, +2 naturale)", 0)):
            with self.subTest(riga=riga):
                self.assertEqual(V._penalita_di_prova(riga, r, "dnd35")[0], attesa)

    def test_pf1e_non_ha_la_tabella_e_non_conta(self):
        self.assertEqual(V._penalita_di_prova("ca-dettaglio: (+9 full plate)", S.dati("pf1e", "creature.gradi"),
                                              "pf1e"), (0, ""))


if __name__ == "__main__":
    unittest.main()
