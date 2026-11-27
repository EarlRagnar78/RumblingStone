"""Le creature base (ADR-0126, lotto 5): dati, dichiarazione nella fonte, giudizi."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verifica_scheda as V  # noqa: E402
from dmcore import creature_base as CB  # noqa: E402
from dmcore import danno as D  # noqa: E402

SCHEDA = """# {titolo}
**Faction**: prova | **CR**: 5 | **Source**: {fonte} | **Status**: prova

```statblocco
gs: 5
tipo: {tipo}
ca: 17
ca-dettaglio: ({ca})
pf: 40
pf-dado: {dadi}
ts: Temp +6, Rifl +2, Vol +2
attributi: For 21 Des 10 Cos 15 Int 6 Sag 10 Car 7
attacchi:
  - {attacco}
```
"""


def giudica(**campi) -> "tuple[list[dict], list[dict]]":
    dati = dict(titolo="Prova", fonte="SRD *Ogre* + Barbaro 2", tipo="Large giant, CE",
                ca="-1 taglia, +5 naturale, +3 pelle", dadi="4d8+2d12+18", attacco="Mischia randello +9 (2d8+7)")
    dati.update(campi)
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "prova.md"
        p.write_text(SCHEDA.format(**dati), encoding="utf-8")
        bv, bn = V.creatura_base(p)
        dv, dn = V.danno(p)
    return bv + dv, bn + dn


def regole(voci: "list[dict]") -> "set[str]":
    return {x["regola"] for x in voci}


class TestDati(unittest.TestCase):
    def test_forma(self):
        tab = CB.tabella("dnd35")
        self.assertGreater(len(tab), 400)
        for nome, v in tab.items():
            self.assertTrue({"taglia", "tipo", "dv", "dado", "naturale", "fonte"} <= set(v), nome)
            self.assertIn(v["dado"], (4, 6, 8, 10, 12), nome)
            for a in (v.get("attacchi") or {}).values():
                self.assertRegex(a["dado"], r"^\d+d\d+$", nome)

    def test_valori_noti_dell_srd(self):
        ogre = CB.creatura("ogre")
        self.assertEqual((ogre["taglia"], ogre["dv"], ogre["dado"], ogre["naturale"], ogre["mdl"]),
                         ("Large", 4, 8, 5, 2))
        self.assertEqual(CB.creatura("gnoll")["naturale"], 1)
        self.assertEqual(CB.creatura("troll")["attacchi"]["claw"], {"dado": "1d6", "n": 2})

    def test_pf1e_ha_le_sue_creature(self):
        tab = CB.tabella("pf1e")
        self.assertGreater(len(tab), 1000)
        ogre = tab["ogre"]
        self.assertEqual((ogre["taglia"], ogre["tipo"], ogre["dv"], ogre["dado"], ogre["naturale"]),
                         ("Large", "humanoid", 4, 8, 5))
        self.assertEqual(tab["troll"]["attacchi"]["bite"]["dado"], "1d8")     # 3.5: 1d6
        self.assertIsNone(CB.drago("Red Dragon", "Huge", "pf1e"))             # la tabella per taglia è del 3.5

    def test_solo_nomi_e_numeri(self):
        testo = (Path(__file__).resolve().parents[2] / "sistemi/dnd35/dati/creature_base.toml").read_text("utf-8")
        for riga in testo.splitlines():
            if riga and not riga.startswith(("#", "[")):
                valori = re.findall(r'= "([^"]*)"', riga)
                self.assertTrue(all(len(v) < 40 for v in valori), riga[:80])


class TestDichiarazione(unittest.TestCase):
    def test_la_fonte_dichiara_la_base(self):
        for fonte, attesa in (("SRD *Ogre* (CR 3) + Barbaro 6", "ogre"), ("MM p.33 Centaur + PHB Ranger 4", "centaur"),
                              ("MM Gnoll + PHB Warrior 2", "gnoll"), ("SRD *Ogre Mage* + stregone", "ogre mage")):
            self.assertEqual(CB.dichiarata(fonte)[0], attesa, fonte)

    def test_un_archetipo_o_un_altro_manuale_non_dichiarano(self):
        for fonte in ("MM Dire Lion + skeleton template", "MM II p.104 Flind", "Races of Faerûn", "",
                      "SRD *Stone Giant* + template semplice PF1e"):
            self.assertIsNone(CB.dichiarata(fonte), fonte)

    def test_celestiale_e_immondo_lasciano_i_numeri_della_base(self):
        """SRD, celestial e fiendish creature: dadi vita, armatura naturale e attacchi restano quelli della base."""
        for fonte, attesa in (("SRD 3.5 (gufo gigante, avanzamento a 8 DV, modello celestiale)", "owl, giant"),
                              ("SRD *Ogre* immondo", "ogre"), ("MM Fiendish Dire Wolf", "dire wolf"),
                              ("SRD Hell Hound celestiale", "hellhound")):
            self.assertEqual((CB.dichiarata(fonte) or [None])[0], attesa, fonte)
        # i «mezzi» cambiano armatura naturale e caratteristiche: non dichiarano
        for fonte in ("SRD *Ogre* mezzo-immondo", "SRD half-celestial ogre", "SRD ogre mezzo celestiale"):
            self.assertIsNone(CB.dichiarata(fonte), fonte)

    def test_la_fonte_dichiara_l_avanzamento(self):
        gufo = dict(tipo="Large magical beast (extraplanar), 8 DV, NB", ca="-1 taglia, +4 Des, +3 naturale",
                    attacco="Mischia morso +6 (1d8+2)")
        fonte = "SRD 3.5 (gufo gigante, avanzamento a 8 DV, modello celestiale)"
        self.assertEqual(giudica(fonte=fonte, dadi="8d10+8", **gufo), ([], []))
        # i dadi scritti non sono quelli dichiarati, o la fonte non dichiara l'avanzamento
        for f, dadi in ((fonte, "9d10+9"), ("SRD 3.5 (gufo gigante, modello celestiale)", "8d10+8")):
            viol, _ = giudica(fonte=f, dadi=dadi, **gufo)
            self.assertEqual(regole(viol), {"numero.dv.razziali"}, (f, dadi))
        # il dado del morso resta quello della base
        viol, _ = giudica(fonte=fonte, dadi="8d10+8", **dict(gufo, attacco="Mischia morso +6 (1d6+2)"))
        self.assertEqual(regole(viol), {"numero.danno.dado"})

    def test_il_tipo_deve_essere_quello_della_base(self):
        # «MM Rakshasa + Rogue 3» su un umanoide è il cultista di un rakshasa
        viol, nv = giudica(fonte="MM Rakshasa + PHB Rogue 3", tipo="Medium humanoid, LE", dadi="3d6+6")
        self.assertEqual(regole(viol) & {"numero.dv.razziali", "numero.CA.naturale"}, set())

    def test_il_dm_dichiara_la_variante(self):
        """Armatura naturale e grado di sfida fuori dalla base: una riga col numero e «DM» o «RC-NNN» (RC-002)."""
        self.assertIn("numero.CA.naturale", regole(giudica(ca="-1 taglia, +8 naturale")[0]))
        riga = "> Armatura naturale diversa dalla base: +8 contro +5, scelta del DM (RC-002)."
        self.assertTrue(V._variante_del_dm(V._VARIANTE_NATURALE, riga, "+8"))
        # il numero dichiarato deve essere quello della scheda, e deve dirlo il DM
        self.assertFalse(V._variante_del_dm(V._VARIANTE_NATURALE, riga, "+9"))
        self.assertFalse(V._variante_del_dm(V._VARIANTE_NATURALE, riga.replace("del DM (RC-002)", "nostra"), "+8"))
        riga = "> Grado di sfida diverso dalla regola: 15 contro il 13 dell'SRD, scelta del DM (RC-002)."
        self.assertTrue(V._variante_del_dm(V._VARIANTE_GS, riga, "15"))
        self.assertFalse(V._variante_del_dm(V._VARIANTE_GS, riga, "13"))
        self.assertFalse(V._variante_del_dm(V._VARIANTE_GS, riga, "5"))

    def test_drago_vero_solo_col_colore_accanto(self):
        self.assertIsNotNone(CB.drago("Huge dragon (fire) — Drago Rosso", "Huge"))
        self.assertIsNotNone(CB.drago("Blue Old Dragon", "Huge"))
        self.assertIsNone(CB.drago("progenie azzurra di Tiamat (drago)", "Large"))
        self.assertIsNone(CB.drago("Large dragon (earth)", "Large"))


class TestGiudizi(unittest.TestCase):
    def test_scheda_in_regola(self):
        viol, _ = giudica()
        self.assertEqual(regole(viol) & {"numero.dv.razziali", "numero.CA.naturale"}, set())

    def test_dadi_vita_razziali_mancanti(self):
        viol, _ = giudica(dadi="2d8+2d12+12")
        self.assertIn("numero.dv.razziali", regole(viol))

    def test_armatura_naturale_col_modello(self):
        """SRD, riga «Armor Class» dei modelli: mezzi +1/+4, lich almeno +5, vampiro +6, scheletro e zombi per taglia."""
        def nat(**campi):
            viol, nv = giudica(fonte="prova", dadi="6d8", **campi)
            return ([v for v in viol if v["regola"] == "numero.CA.naturale"],
                    [v for v in nv if v["regola"] == "numero.CA.naturale"])
        # razza della fonte con soli livelli di classe: la base è 0 (il coboldo +1), il conto è esatto
        self.assertEqual(nat(tipo="Medium outsider (native), hobgoblin mezzo-immondo, Guerriero 6, LM", ca="+3 Des, +1 naturale"), ([], []))
        v, _ = nat(tipo="Medium outsider (native), hobgoblin mezzo-immondo, Guerriero 6, LM", ca="+3 Des, +3 naturale")
        self.assertEqual((v[0]["atteso"], v[0]["ha"]), (1, 3))
        self.assertEqual(nat(tipo="Small dragon, coboldo mezzo-drago, Stregone 6, LM", ca="+1 taglia, +5 naturale"), ([], []))
        self.assertEqual(nat(tipo="Medium undead, human vampire, Guerriero 6, LM", ca="+6 naturale"), ([], []))
        self.assertEqual(nat(tipo="Medium undead, umano lich, Mago 11, NM", ca="+5 naturale"), ([], []))
        # lo scheletro ha il numero della taglia, qualunque sia la base; lo zombi sta sopra la base
        v, _ = nat(tipo="Large undead, skeleton, NM", ca="-1 taglia, +4 naturale")
        self.assertEqual((v[0]["atteso"], v[0]["ha"]), (2, 4))
        self.assertEqual(nat(tipo="Huge undead, skeleton, NM", ca="-2 taglia, +3 naturale"), ([], []))
        v, _ = nat(tipo="Large undead, zombie, NM", ca="-1 taglia, +2 naturale")
        self.assertEqual(v[0]["atteso"], "almeno +3")
        # base fuori dai dati: sopra il minimo del modello non si giudica
        v, n = nat(tipo="Large outsider, troll half-fiend, CM", ca="-1 taglia, +6 naturale")
        self.assertEqual((v, len(n)), ([], 1))
        v, _ = nat(tipo="Large dragon, troll half-dragon, CM", ca="-1 taglia, +3 naturale")
        self.assertEqual(v[0]["atteso"], "almeno +4")
        # la CA senza addendi non è un conto; con gli addendi e senza la naturale è una violazione
        v, n = nat(tipo="Medium outsider, hobgoblin half-fiend, Guerriero 6, LM", ca="contatto 11, alla sprovvista 16")
        self.assertEqual((v, len(n)), ([], 1))
        v, _ = nat(tipo="Medium outsider, hobgoblin half-fiend, Guerriero 6, LM", ca="+3 Des, +5 armatura")
        self.assertEqual(v[0]["ha"], "nessuna")
        # la variante del DM si dichiara come per la base
        riga = "> Armatura naturale diversa dalla base: +4 contro +2, scelta del DM (RC-099)."
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "prova.md"
            p.write_text(SCHEDA.format(titolo="Prova", fonte="prova", tipo="Large undead, skeleton, NM",
                                       ca="-1 taglia, +4 naturale", dadi="6d12", attacco="Mischia artiglio +5 (1d6+4)")
                         + "\n" + riga + "\n", encoding="utf-8")
            self.assertNotIn("numero.CA.naturale", regole(V.creatura_base(p)[0]))
        # la base che la fonte dichiara, con la stessa taglia: l'ogre dell'SRD ha +5, il mezzo-immondo +1
        def nat_fonte(ca, tipo="Large outsider, half-fiend, CM", fonte="SRD *Ogre* + half-fiend"):
            viol, nv = giudica(fonte=fonte, dadi="6d8", tipo=tipo, ca=ca)
            return ([v for v in viol if v["regola"] == "numero.CA.naturale"],
                    [v for v in nv if v["regola"] == "numero.CA.naturale"])
        self.assertEqual(nat_fonte("-1 taglia, +6 naturale"), ([], []))
        v, _ = nat_fonte("-1 taglia, +8 naturale")
        self.assertEqual((v[0]["atteso"], v[0]["ha"]), (6, 8))
        # con un'altra taglia la base non vale: resta il minimo del modello
        v, n = nat_fonte("-2 taglia, +8 naturale", tipo="Huge outsider, half-fiend, CM")
        self.assertEqual((v, len(n)), ([], 1))
        # fantasma, celestiale e immondo non hanno una regola loro
        self.assertEqual(nat(tipo="Medium undead, human ghost, Guerriero 6, LM", ca="+4 naturale"), ([], []))

    def test_caratteristiche_col_modello(self):
        """SRD, riga «Abilities» dei modelli: punteggi tolti e fissati sempre, aumenti sopra la base dichiarata."""
        def car(attributi, tipo, fonte="prova", dopo=""):
            with tempfile.TemporaryDirectory() as d:
                p = Path(d) / "prova.md"
                p.write_text(SCHEDA.replace("For 21 Des 10 Cos 15 Int 6 Sag 10 Car 7", attributi).format(
                    titolo="Prova", fonte=fonte, tipo=tipo, ca="-1 taglia, +2 naturale", dadi="8d12",
                    attacco="Mischia artiglio +5 (1d6+4)") + dopo, encoding="utf-8")
                viol, nv = V.creatura_base(p)
            return ([v for v in viol if v["regola"] == "numero.caratteristiche.modello"],
                    [v for v in nv if v["regola"] == "numero.caratteristiche.modello"])
        leone = "MM Dire Lion + Skeleton template"
        # il leone crudele dell'SRD ha Des 15 e Car 10: lo scheletro ha Des 17, niente Cos e Int, Sag 10, Car 1
        self.assertEqual(car("For 25 Des 17 Cos — Int — Sag 10 Car 1", "Large undead, skeleton, NM", leone), ([], []))
        v, _ = car("For 25 Des 15 Cos — Int — Sag 10 Car 10", "Large undead, skeleton, NM", leone)
        self.assertEqual((v[0]["ha"], v[0]["atteso"]), ("Des 15, Car 10", "Des almeno 17, Car 1"))
        # sopra il minimo si può stare: un punto ogni quattro dadi vita, gli oggetti
        self.assertEqual(car("For 27 Des 18 Cos — Int — Sag 10 Car 1", "Large undead, skeleton, NM", leone), ([], []))
        # senza la base restano i punteggi tolti e fissati; gli aumenti non si riscontrano e lo si dice
        v, n = car("For 25 Des 15 Cos 14 Int 2 Sag 12 Car 1", "Large undead, zombie, NM")
        self.assertEqual((v[0]["ha"], v[0]["atteso"], len(n)), ("Cos 14, Int 2, Sag 12", "Cos —, Int —, Sag 10", 1))
        v, n = car("For 20 Des 14 Cos — Int 16 Sag 14 Car 18", "Medium undead, human vampire, Guerriero 6, LM")
        self.assertEqual((v, len(n)), ([], 1))
        v, _ = car("For 20 Des 14 Cos 12 Int 16 Sag 14 Car 18", "Medium undead, umano lich, Mago 11, NM")
        self.assertEqual(v[0]["atteso"], "Cos —")
        # celestiale e immondo: Intelligenza almeno 3, niente altro
        v, n = car("For 18 Des 17 Cos 12 Int 2 Sag 14 Car 10", "Large magical beast, celestial, NB")
        self.assertEqual((v[0]["atteso"], n), ("Int almeno 3", []))
        # i mezzi sopra la base dichiarata: l'ogre dell'SRD ha For 21, Des 8, Cos 15, Int 6, Sag 10, Car 7
        v, _ = car("For 25 Des 12 Cos 17 Int 10 Sag 10 Car 9", "Large outsider, half-fiend, CM", "SRD *Ogre* + half-fiend")
        self.assertEqual(v, [])
        v, _ = car("For 21 Des 12 Cos 17 Int 10 Sag 10 Car 9", "Large outsider, half-fiend, CM", "SRD *Ogre* + half-fiend")
        self.assertEqual((v[0]["ha"], v[0]["atteso"]), ("For 21", "For almeno 25"))
        # coi livelli di classe o con un'altra taglia i punteggi di partenza non sono quelli dell'SRD
        v, n = car("For 21 Des 12 Cos 17 Int 10 Sag 10 Car 9", "Large outsider, half-fiend, Barbaro 2, CM", "SRD *Ogre* + half-fiend")
        self.assertEqual((v, len(n)), ([], 1))
        v, n = car("For 21 Des 12 Cos 17 Int 10 Sag 10 Car 9", "Huge outsider, half-fiend, CM", "SRD *Ogre* + half-fiend")
        self.assertEqual((v, len(n)), ([], 1))
        # la variante del DM
        riga = "\n> Caratteristiche diverse dal modello: Car 10 contro 1, scelta del DM (RC-099).\n"
        self.assertEqual(car("For 25 Des 17 Cos — Int — Sag 10 Car 10", "Large undead, skeleton, NM", leone, riga), ([], []))
        # la base senza modello resta quella di prima: la fonte con un archetipo non la dichiara
        self.assertIsNone(CB.dichiarata(leone))
        self.assertEqual(CB.dichiarata(leone, col_modello=True)[0], "dire lion")

    def test_armatura_naturale_diversa(self):
        viol, _ = giudica(ca="-1 taglia, +7 naturale, +3 pelle")
        v = next(x for x in viol if x["regola"] == "numero.CA.naturale")
        self.assertEqual((v["ha"], v["atteso"]), (7, 5))

    def test_taglia_diversa_resta_dubbio(self):
        viol, nv = giudica(tipo="Huge giant, CE", ca="-2 taglia, +8 naturale")
        self.assertNotIn("numero.CA.naturale", regole(viol))
        self.assertIn("numero.CA.naturale", regole(nv))

    def test_dado_dell_attacco_naturale(self):
        troll = ("troll", CB.creatura("troll"))
        scarti, nv = D.giudica("Mischia 2 artigli +9 (1d6+6)", 6, "Large giant", creatura=troll)
        self.assertEqual((scarti, nv), ([], []))
        scarti, _ = D.giudica("Mischia 2 artigli +9 (1d8+6)", 6, "Large giant", creatura=troll)
        self.assertEqual([(x["campo"], x["scritto"], x["atteso"]) for x in scarti], [("danno.dado", "1d8", "1d6")])

    def test_attacco_naturale_migliorato_alza_di_un_passo(self):
        troll = ("troll", CB.creatura("troll"))
        scarti, _ = D.giudica("Mischia 2 artigli +9 (1d8+6)", 6, "Large giant",
                              talenti="Attacco Naturale Migliorato (artigli)", creatura=troll)
        self.assertEqual(scarti, [])

    def test_senza_base_resta_il_dubbio_di_prima(self):
        _, nv = D.giudica("Mischia morso +9 (1d8+6)", 6, "Large giant")
        self.assertIn("il dado viene dalla creatura", nv[0]["nota"])
        _, nv = D.giudica("Mischia pungiglione +9 (1d8+6)", 6, "Large giant", creatura=("troll", CB.creatura("troll")))
        self.assertIn("il dado viene dalla creatura", nv[0]["nota"])

    def test_drago_vero_dalla_taglia(self):
        viol, nv = giudica(titolo="Prova, Drago Rosso", fonte="PCGen", tipo="Huge dragon (fire), 19 HD, LE",
                           ca="-2 taglia, +20 naturale", dadi="19d12+95",
                           attacco="Mischia morso +27 (2d8+10); 2 artigli +22 (2d6+5); 2 ali +22 (1d8+5); coda +22 (2d6+15)")
        self.assertEqual(regole(viol), set())
        self.assertFalse([x for x in nv if "naturale" in x["testo"]])
        viol, _ = giudica(titolo="Prova, Drago Rosso", fonte="PCGen", tipo="Huge dragon (fire), 19 HD, LE",
                          ca="-2 taglia, +20 naturale", dadi="19d12+95", attacco="Mischia morso +27 (4d6+10)")
        self.assertIn("numero.danno.dado", regole(viol))

    def test_drago_vero_con_la_categoria_d_eta(self):
        # colore ed età scritti: la base porta dadi vita, armatura naturale e grado di sfida dell'SRD
        nome, voce = CB.drago("Prova, Drago Rosso (Young Adult)", "Huge")
        self.assertEqual((nome, voce["dv"], voce["naturale"], voce["gs"]), ("young adult red dragon", 19, 18, 13))
        self.assertEqual(CB.drago("drago rosso adulto maturo", "Huge")[0], "mature adult red dragon")
        self.assertEqual(CB.drago("Blue Old Dragon", "Huge")[0], "old blue dragon")
        self.assertEqual(CB.drago("drago verde molto vecchio", "Huge")[0], "very old green dragon")
        # la taglia non è quella dell'età, o l'età non è scritta: restano solo gli attacchi della taglia
        self.assertNotIn("dv", CB.drago("Drago Rosso (Young Adult)", "Large")[1])
        self.assertNotIn("dv", CB.drago("Drago Rosso", "Huge")[1])
        # 120 voci: dieci colori per dodici età
        from dmcore import sistemi as S
        eta = S.dati("dnd35", "creature.base")["draghi_eta"]
        self.assertEqual((len(eta), {len(v) for v in eta.values()}), (10, {12}))
        # l'armatura naturale è quella dell'età; i dadi vita in più sono un avanzamento, non un errore
        viol, _ = giudica(titolo="Prova, Drago Rosso (Young Adult)", fonte="PCGen", tipo="Huge dragon (fire), 19 HD, LE",
                          ca="-2 taglia, +18 naturale", dadi="19d12+95")
        self.assertEqual(regole(viol) & {"numero.dv.razziali", "numero.CA.naturale"}, set())
        viol, _ = giudica(titolo="Prova, Drago Rosso (Young Adult)", fonte="PCGen", tipo="Huge dragon (fire), 19 HD, LE",
                          ca="-2 taglia, +24 naturale", dadi="19d12+95")
        self.assertIn("numero.CA.naturale", regole(viol))
        viol, nv = giudica(titolo="Prova, Drago Rosso (Young Adult)", fonte="PCGen", tipo="Huge dragon (fire), 21 HD, LE",
                           ca="-2 taglia, +18 naturale", dadi="21d12+105")
        self.assertNotIn("numero.dv.razziali", regole(viol))
        self.assertTrue([x for x in nv if "avanzato per dadi vita" in x["testo"]])
        # un modello dichiarato nel tipo («Avanzato», +2 di armatura naturale) non è una violazione
        viol, nv = giudica(titolo="Prova, Drago Rosso (Young Adult)", fonte="PCGen",
                           tipo="Huge dragon (fire), 19 HD, LE, Avanzato", ca="-2 taglia, +20 naturale", dadi="19d12+95")
        self.assertNotIn("numero.CA.naturale", regole(viol))
        self.assertTrue([x for x in nv if "cambia col modello" in x["testo"]])


if __name__ == "__main__":
    unittest.main()
