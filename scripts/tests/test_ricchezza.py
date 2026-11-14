"""Il valore dell'equipaggiamento contro quello di un PNG del suo livello (ADR-0126, lotto 8).

I prezzi vengono dalle tabelle degli oggetti magici dell'SRD; il valore per
livello dalla Tabella 4-23 del DMG 3.5 (solo i numeri)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402
from dmcore import sistemi as S  # noqa: E402


def giudica(coda: str, **kw) -> "tuple[list, list]":
    """(violazioni, non verificabili) della sola verifica `ricchezza` sulla scheda di prova."""
    import tempfile
    from tests.test_difese import SCHEDA
    d = {"titolo": "Prova", "tipo": "Medium humanoid (human)", "classe": "Fighter 3", "dadi": "3d10+6"}
    d.update(kw)
    with tempfile.TemporaryDirectory() as t:
        q = Path(t) / "prova-cr4.md"
        q.write_text(SCHEDA.format(coda=coda, **d), encoding="utf-8")
        if V.L.leggi(q) is None:
            raise AssertionError("la scheda di prova non si legge")
        return V.ricchezza(q)


class TestDati(unittest.TestCase):
    def setUp(self):
        self.d = S.dati("dnd35", "creature.costruzione")["oggetti"]

    def test_tabella_dei_png(self):
        t = self.d["png"]["per_livello"]
        self.assertEqual(len(t), 20)
        self.assertEqual((t[0], t[9], t[19]), (900, 16000, 220000))
        self.assertEqual(t, sorted(t))

    def test_potenziamento(self):
        self.assertEqual(self.d["potenziamento"]["arma"][:5], [2000, 8000, 18000, 32000, 50000])
        self.assertEqual(self.d["potenziamento"]["armatura"], [1000, 4000, 9000, 16000, 25000])

    def test_prezzi_dell_srd(self):
        p = self.d["prezzi"]
        self.assertEqual(p["ring of protection +3"], 18000)
        self.assertEqual(p["cloak of resistance +5"], 25000)
        self.assertEqual(p["amulet of health +6"], 36000)
        self.assertEqual(p["gauntlets of ogre power"], 4000)
        self.assertEqual(p["boots of speed"], 12000)
        self.assertGreater(len(p), 600)

    def test_ogni_nome_ha_un_prezzo(self):
        for v in self.d["nomi"]:
            nomi = [v["nome"].replace("N", str(n)) for n in range(1, 7)] if "N" in v["nome"] else [v["nome"]]
            self.assertTrue(any(n in self.d["prezzi"] for n in nomi), v["nome"])

    def test_pf1e_ha_la_14_9_ma_non_i_prezzi(self):
        pf = S.dati("pf1e", "creature.costruzione")["oggetti"]
        self.assertEqual(set(pf), {"png"})
        self.assertNotIn("per_livello", pf["png"])


class TestOggetti(unittest.TestCase):
    def setUp(self):
        self.d = S.dati("dnd35", "creature.costruzione")["oggetti"]

    def trova(self, riga: str) -> list:
        return sorted(V._oggetti_col_prezzo(riga, self.d, "dnd35"))

    def test_nomi_italiani_e_inglesi(self):
        self.assertEqual(self.trova("*anello di protezione +2*, *mantello della resistenza +1*"),
                         [("cloak of resistance +1", 1000), ("ring of protection +2", 8000)])
        self.assertEqual(self.trova("Ring of Protection +1, Cloak of Charisma +4"),
                         [("cloak of charisma +4", 16000), ("ring of protection +1", 2000)])

    def test_armature_e_armi_col_solo_potenziamento(self):
        self.assertEqual([mo for _, mo in self.trova("corazza di piastre +1, picca lunga +1")], [1350, 2305])

    def test_capacita_speciali_attaccate_al_nome_o_al_bonus(self):
        # animato +2 e sacrilego +2: (2 + 2)² × 1000 e × 2000; infuocata e affilata: (1 + 2)² × 2000;
        # in più il prezzo dell'oggetto comune e la fattura perfetta (scudo 7 + 150, spadone 50 + 300)
        self.assertEqual([mo for _, mo in self.trova("**Scudo Pesante +2 animato**")], [16157])
        self.assertEqual([mo for _, mo in self.trova("**Spadone Sacrilego +2**")], [32350])
        self.assertEqual([mo for _, mo in self.trova("spada lunga +1 infuocata e affilata")], [18315])
        self.assertEqual([mo for _, mo in self.trova("longsword +1 flaming")], [8315])
        self.assertEqual([mo for _, mo in self.trova("+1 flaming longsword")], [8315])
        # limite dichiarato: la capacità prima del nome col bonus dopo non si legge, resta il potenziamento
        self.assertEqual([mo for _, mo in self.trova("flaming longsword +1")], [2315])

    def test_una_parola_lontana_non_e_una_capacita(self):
        # «Cerchio Sacro» è un nome proprio: l'arco resta un +1
        self.assertEqual([mo for _, mo in self.trova("Arco lungo composito +1 di tasso del Cerchio Sacro")], [2400])

    def test_oltre_il_piu_dieci_resta_il_potenziamento(self):
        self.assertEqual([mo for _, mo in self.trova("spada lunga +5 vorpal sacrilega")], [50315])

    def test_pozioni_pergamene_e_bacchette(self):
        self.assertEqual(self.trova("3 pozioni di *cura ferite leggere*"),
                         [("3 × potion of cure light wounds (potion)", 150)])
        self.assertEqual(self.trova("due pergamene di palla di fuoco"), [("2 × fireball", 750)])
        self.assertEqual(self.trova("potion of cure moderate wounds x2"),
                         [("2 × potion of cure moderate wounds (potion)", 600)])
        # una bacchetta vale per le cariche scritte; senza cariche non si conta
        self.assertEqual(self.trova("bacchetta di dardo incantato (20 cariche)"), [("wand of magic missile (1st)", 300)])
        self.assertEqual(self.trova("bacchetta di dardo incantato"), [])
        self.assertEqual(self.trova("pozione di un liquido verde"), [])

    def test_bastoni_solo_con_le_cariche(self):
        self.assertEqual(self.trova("**bastone del fuoco** (*mani brucianti*, *palla di fuoco* — 10 cariche)"),
                         [("staff of fire (10 cariche)", 3550)])
        self.assertEqual(self.trova("staff of fire (50 charges)"), [("staff of fire (50 cariche)", 17750)])
        self.assertEqual(self.trova("bastone del fuoco, bastone ferrato (3 cariche), bastone di cedro"), [])

    def test_adamantio_e_mithral(self):
        self.assertEqual(self.d["materiali"], {"adamantine": {"leggera": 5000, "media": 10000, "pesante": 15000, "arma": 3000},
                                               "mithral": {"leggera": 1000, "media": 4000, "pesante": 9000, "scudo": 1000}})
        self.assertEqual(self.trova("Armatura completa +1 di mithral"), [("armatura completa +1 di mithral (armatura)", 11500)])
        self.assertEqual(self.trova("+1 mithral full plate"), [("full plate +1 di mithral (armatura)", 11500)])
        self.assertEqual(self.trova("Mithral chainmail"), [("chainmail di mithral (armatura)", 4150)])
        self.assertEqual(self.trova("spada lunga di adamantio +1, scudo pesante di mithral"),
                         [("scudo pesante di mithral (armatura)", 1007), ("spada lunga +1 di adamantio (arma)", 5015)])
        # la tabella non ha il prezzo di un'arma di mithral né di uno scudo di adamantio; un oggetto
        # che non è un'arma o un'armatura della tabella non si conta: resta il prezzo dell'oggetto comune
        self.assertEqual(self.trova("mithral dagger, scudo pesante di adamantio, Corona di Adamantio"),
                         [("dagger (arma)", 2), ("scudo pesante (armatura)", 7)])
        # il materiale lontano dal nome non conta
        self.assertEqual(self.trova("spada lunga +1 presa nelle miniere di mithral"), [("spada lunga +1 (arma)", 2315)])

    def test_nomi_del_lessico(self):
        self.assertEqual(self.trova("Bracciali dell'arciere superiori, Stivali elfici"),
                         [("boots of elvenkind", 2500), ("bracers of archery, greater", 25000)])

    def test_un_nome_italiano_di_una_parola_non_basta(self):
        self.assertEqual(self.trova("un ventaglio di seta, un mantello"), [])
        self.assertEqual(self.trova("Wind fan"), [("wind fan", 5500)])

    def test_tabelle_delle_capacita_e_delle_pergamene(self):
        c = self.d["capacita"]
        self.assertEqual((c["arma"]["keen"], c["arma"]["vorpal"], c["armatura"]["animated"]),
                         ({"bonus": 1}, {"bonus": 5}, {"bonus": 2}))
        self.assertEqual(c["armatura"]["glamered"], {"mo": 2700})
        self.assertEqual((self.d["pergamene"]["fireball"], self.d["pergamene"]["cure light wounds"]), (375, 25))

    def test_oggetti_comuni_e_fattura_perfetta(self):
        self.assertEqual(self.trova("spada lunga perfetta, armatura completa, 2 pozioni"),
                         [("armatura completa (armatura)", 1500), ("spada lunga perfetta (arma)", 315)])
        self.assertEqual(self.trova("masterwork composite longbow, mwk rapier"),
                         [("composite longbow perfetta (arma)", 400), ("rapier perfetta (arma)", 320)])
        # un oggetto magico porta con sé il prezzo comune e la fattura: armatura completa 1.500 + 150 + 1.000
        self.assertEqual(self.trova("armatura completa +1, scudo pesante +1, ascia da guerra nanica +1"),
                         [("armatura completa +1 (armatura)", 2650), ("ascia da guerra nanica +1 (arma)", 2330),
                          ("scudo pesante +1 (armatura)", 1157)])
        # un nome corto da solo può essere un'altra cosa; chi costa meno di 1 mo non si conta
        self.assertEqual(self.trova("pelle di worg, rete da pesca, randello, bastone ferrato"), [])
        self.assertEqual((self.d["perfetta"], self.d["comuni"]["scudi"]),
                         ({"arma": 300, "armatura": 150}, {"1": 3, "2": 7, "4": 30}))

    def test_senza_bonus_non_ha_prezzo(self):
        self.assertEqual(self.trova("mantello del carisma +3"), [])

    def test_righe_dell_equipaggiamento(self):
        testo = ("**Equipaggiamento** anello di protezione +1\n\n### Equipaggiamento\n- mantello della resistenza +1\n"
                 "| **Anello di Protezione +2** | nota |\n### Tattiche\n- anello di protezione +5\n"
                 "> era: Equipaggiamento anello di protezione +4\n")
        self.assertEqual([n for n, _ in V._righe_dell_equipaggiamento(testo)], [1, 4, 5])


class TestRicchezza(unittest.TestCase):
    def test_sotto_la_tabella(self):
        self.assertEqual(giudica("**Equipaggiamento** spada lunga +1, 2 pozioni"), ([], []))
        self.assertEqual(giudica(""), ([], []))

    def test_sopra_la_tabella(self):
        v, n = giudica("**Equipaggiamento** amuleto della salute +2")
        self.assertEqual(n, [])
        self.assertEqual(len(v), 1)
        self.assertEqual((v[0]["regola"], v[0]["atteso"], v[0]["ha"]),
                         ("equipaggiamento.valore", "al più 2500 mo", "almeno 4000 mo"))

    def test_il_livello_alza_il_limite(self):
        coda = "**Equipaggiamento** amuleto della salute +2"
        self.assertEqual(giudica(coda, classe="Fighter 5", dadi="5d10+10"), ([], []))

    def test_razza_fuori_dalle_sette(self):
        v, n = giudica("**Equipaggiamento** anello di protezione +2", tipo="Medium humanoid (goblinoid)")
        self.assertEqual(v, [])
        self.assertEqual(len(n), 1)
        self.assertIn("modificatore di livello", n[0]["testo"])

    def test_razza_senza_dadi_vita_razziali(self):
        # hobgoblin: livello effettivo 3 + 1 = 4, 3300 mo; drow: 3 + 2 = 5, 4300 mo
        coda = "**Equipaggiamento** amuleto della salute +2"
        v, n = giudica(coda, titolo="Sergente hobgoblin", tipo="Medium humanoid (goblinoid)")
        self.assertEqual(n, [])
        self.assertEqual(v[0]["atteso"], "al più 3300 mo")
        self.assertEqual(giudica(coda, titolo="Esploratrice drow", tipo="Medium humanoid (elf, drow)"), ([], []))
        v, n = giudica(coda, titolo="Predone orco", tipo="Medium humanoid (orc)")
        self.assertEqual(v[0]["atteso"], "al più 2500 mo")

    def test_un_modello_non_si_giudica(self):
        coda = "**Equipaggiamento** amuleto della salute +2"
        v, n = giudica(coda, titolo="Hobgoblin mezzo-drago", tipo="Medium humanoid (goblinoid)")
        self.assertEqual(v, [])
        self.assertEqual(len(n), 1)

    def test_tabella_dei_modificatori_di_livello(self):
        d = S.dati("dnd35", "creature.costruzione")["mdl"]
        self.assertEqual({k: v["mdl"] for k, v in d["razze"].items()},
                         {"aasimar": 1, "drow": 2, "duergar": 1, "goblin": 0, "hobgoblin": 1, "kobold": 0,
                          "merfolk": 1, "orc": 0, "svirfneblin": 3, "tiefling": 1})
        self.assertEqual(set(d["nomi"]), set(d["razze"]))

    def test_una_riga_di_storia_non_conta(self):
        self.assertEqual(giudica("> era: Equipaggiamento anello di protezione +5"), ([], []))


class TestImprovingMonsters(unittest.TestCase):
    """SRD, «Improving Monsters»: l'equipaggiamento di un PNG spetta a chi avanza per classe."""
    CODA = "**Fonte**: SRD *{}*\n\n**Equipaggiamento** amuleto della salute +6"

    def test_chi_avanza_per_classe_nei_dati(self):
        b = S.dati("dnd35", "creature.base")["creature_base"]
        per_classe = {n for n, v in b.items() if v.get("avanza") == "classe"}
        self.assertEqual(len(per_classe), 52)
        self.assertLessEqual({"ogre", "gnoll", "bugbear", "troll", "hill giant", "medusa", "rakshasa"}, per_classe)
        self.assertFalse({"owlbear", "wolf", "aboleth", "hell hound"} & per_classe)

    def test_un_mostro_che_avanza_per_dadi_vita_ha_un_tesoro(self):
        v, n = giudica(self.CODA.format("Owlbear"), tipo="Large magical beast", classe="", dadi="5d10+25")
        self.assertEqual(v, [])
        self.assertEqual([x["regola"] for x in n], ["equipaggiamento.da_png"])
        self.assertIn("Improving Monsters", n[0]["testo"])

    def test_chi_avanza_per_classe_si_giudica(self):
        v, n = giudica(self.CODA.format("Ogre"), tipo="Large giant", classe="", dadi="4d8+11")
        self.assertEqual(n, [])
        self.assertEqual(v[0]["atteso"], "al più 5600 mo")  # 4 dadi vita + 2 di modificatore di livello

    def test_coi_livelli_di_classe_si_giudica(self):
        v, n = giudica(self.CODA.format("Ogre"), tipo="Large giant", classe="Barbarian 2", dadi="4d8+2d12+11")
        self.assertEqual(v[0]["atteso"], "al più 9400 mo")


class TestPngPF1e(unittest.TestCase):
    """Core Rulebook PF1e, Tabella 14-9, e i PNG dei Codex (ADR-0134)."""

    def setUp(self):
        self.c = S.dati("pf1e", "creature.costruzione")

    def test_tabella_14_9(self):
        t = self.c["oggetti"]["png"]
        self.assertEqual((len(t["base"]), len(t["eroico"])), (20, 20))
        self.assertEqual((t["base"][0], t["base"][19], t["eroico"][0], t["eroico"][19]), (260, 123000, 390, 159000))
        self.assertEqual(t["eroico"][:19], t["base"][1:])
        cat = t["categorie"]
        self.assertEqual(set(cat), {"armi", "protezione", "magia", "uso_limitato", "attrezzatura"})
        for i, totale in enumerate(t["base"] + t["eroico"][-1:]):
            # la quarta riga del manuale somma 1750 contro un totale di 1650: si tiene com'è scritta
            self.assertEqual(sum(cat[k][i] for k in cat), totale + (100 if i == 3 else 0), i)

    def test_png_dei_codex(self):
        png = self.c["codex"]
        self.assertEqual(len(png), 454)
        self.assertEqual({x["libro"] for x in png}, {"npc", "mc"})
        guerrieri = {x["livello"]: x for x in png if x["libro"] == "npc" and list(x["classi"]) == ["fighter"]}
        self.assertEqual(sorted(guerrieri), list(range(1, 21)))
        self.assertTrue(all(x["combattimento"] or x["altro"] for x in png))

class TestDoveStaScritto(unittest.TestCase):
    """Le forme di ADR-0091 e le due voci scelte dal DM il 2026-11-13."""

    def test_dentro_la_riga_delle_statistiche(self):
        v, _ = giudica("**Statistiche** For 16 · BAB +3 · **Equipaggiamento** amuleto della salute +2 · "
                       "**Linguaggi** Comune, anello di protezione +5")
        self.assertEqual(v[0]["ha"], "almeno 4000 mo")   # l'anello sta fra i linguaggi: non è equipaggiamento

    def test_le_due_voci(self):
        v, _ = giudica("**Statistiche** For 16 · **Equipaggiamento da combattimento** 2 pozioni di cura ferite "
                       "leggere · **Altro equipaggiamento** amuleto della salute +2")
        self.assertEqual(v[0]["ha"], "almeno 4100 mo")
        v, _ = giudica("- Altro equipaggiamento: amuleto della salute +2")
        self.assertEqual(v[0]["ha"], "almeno 4000 mo")

    def test_recinto_e_prosa_si_contano_una_volta(self):
        from tests.test_difese import SCHEDA
        import tempfile
        testo = SCHEDA.format(titolo="Prova", tipo="Medium humanoid (human)", classe="Fighter 3", dadi="3d10+6",
                              coda="**Statistiche** For 16 · **Altro equipaggiamento** amuleto della salute +2")
        testo = testo.replace("  - Talenti:", "  - Altro equipaggiamento: amuleto della salute +2\n  - Talenti:")
        with tempfile.TemporaryDirectory() as d:
            q = Path(d) / "prova-cr4.md"
            q.write_text(testo, encoding="utf-8")
            v, _ = V.ricchezza(q)
        self.assertEqual(v[0]["ha"], "almeno 4000 mo")

    def test_materiale_dello_scudo_fra_nome_e_bonus(self):
        d = S.dati("dnd35", "creature.costruzione")["oggetti"]
        self.assertEqual(V._oggetti_col_prezzo("scudo pesante d'acciaio +2", d, "dnd35"),
                         [("scudo pesante +2 (armatura)", 4157)])

    def test_il_dm_dichiara_lo_scarto(self):
        coda = ("**Equipaggiamento** amuleto della salute +2\n\n"
                "> Equipaggiamento sopra la tabella: scelta del DM (2026-11-14), conta nel GS.")
        self.assertEqual(giudica(coda), ([], []))


class Bestiario(unittest.TestCase):
    #: schede che superano la Tabella 4-23 col prezzo base e le voci lette da questa PR (ADR-0134):
    #: una card per scheda al DM, le schede non si toccano qui
    IN_ATTESA: "set[str]" = set()

    def test_il_bestiario_non_ha_altri_scarti(self):
        trovate, attese = [], set()
        for p in sorted((ROOT / "Bestiario").rglob("*.md")):
            v = V.ricchezza(p)[0]
            if p.name in self.IN_ATTESA:
                attese |= {p.name} if v else set()
            else:
                trovate += [f"{x['file']}:{x['riga']} {x['testo']}" for x in v]
        self.assertEqual(trovate, [])
        self.assertEqual(attese, self.IN_ATTESA, "una scheda in attesa è stata corretta: toglierla dall'elenco")


if __name__ == "__main__":
    unittest.main()
