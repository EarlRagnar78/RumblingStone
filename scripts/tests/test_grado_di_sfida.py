"""Il grado di sfida (ADR-0126, lotto 5, seconda parte): conto puro, lettura della scheda, Bestiario."""
from __future__ import annotations

import sys
import tempfile
import unittest
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verifica_scheda as V  # noqa: E402
from dmcore import gs as GS  # noqa: E402
from dmcore import sistemi as S  # noqa: E402

RADICE = Path(__file__).resolve().parents[2]
T35 = S.dati("dnd35", "creature.costruzione")["gs"]
TPF = S.dati("pf1e", "creature.costruzione")["gs"]

SCHEDA = """# {titolo}

```statblocco
gs: {gs}
tipo: {tipo}
pf: 30
pf-dado: {dadi}
attributi: For 14 Des 12 Cos 12 Int 10 Sag 10 Car 10
```
"""


def giudica(gs, tipo, dadi, titolo="Prova", nome="prova-cr1.md"):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / nome
        p.write_text(SCHEDA.format(gs=gs, tipo=tipo, dadi=dadi, titolo=titolo), encoding="utf-8")
        return V.grado_di_sfida(p)


class Conto(unittest.TestCase):
    def uno(self, esito):
        self.assertEqual(esito["min"], esito["max"], esito)
        return esito["min"]

    def test_classe_da_pg_vale_il_livello(self):
        self.assertEqual(self.uno(GS.atteso({"fighter": 6}, 0, None, "humanoid (human)", T35)), 6)

    def test_classe_da_png_vale_un_grado_in_meno(self):
        """SRD: hobgoblin combattente di 1° GS 1/2; di 3° GS 2."""
        self.assertEqual(self.uno(GS.atteso({"warrior": 1}, 0, None, "hobgoblin", T35)), F(1, 2))
        self.assertEqual(self.uno(GS.atteso({"warrior": 3}, 0, None, "hobgoblin", T35)), 2)

    def test_le_razze_con_la_loro_riga_nell_srd(self):
        """monsters-*.md: drow e duergar +1 con classi da PG, pari al livello con classi da PNG;
        goblin −2 e coboldo −3 con classi da PNG (blocchi SRD: goblin 1/3, coboldo 1/4, drow 1)."""
        self.assertEqual(self.uno(GS.atteso({"rogue": 1}, 0, None, "humanoid (dwarf, duergar)", T35)), 2)
        self.assertEqual(self.uno(GS.atteso({"warrior": 1}, 0, None, "humanoid (elf) drow", T35)), 1)
        self.assertEqual(self.uno(GS.atteso({"warrior": 1}, 0, None, "goblin", T35)), F(1, 3))
        self.assertEqual(self.uno(GS.atteso({"warrior": 1}, 0, None, "kobold", T35)), F(1, 4))

    def test_hobgoblin_non_e_un_goblin(self):
        self.assertIsNone(GS.razza("Medium humanoid (goblinoid) hobgoblin", T35))

    def test_pf1e_scala_di_uno_e_di_due(self):
        self.assertEqual(self.uno(GS.atteso({"fighter": 6}, 0, None, "human", TPF)), 5)
        self.assertEqual(self.uno(GS.atteso({"fighter": 1}, 0, None, "human", TPF)), F(1, 2))
        self.assertEqual(self.uno(GS.atteso({"warrior": 1}, 0, None, "human", TPF)), F(1, 3))
        self.assertEqual(self.uno(GS.atteso({"warrior": 2}, 0, None, "human", TPF)), F(1, 2))

    def test_classi_miste_e_razze_fuori_fonte_non_si_giudicano(self):
        self.assertIn("perche", GS.atteso({"rogue": 4, "expert": 4}, 0, None, "human", T35))
        self.assertIn("perche", GS.atteso({"fighter": 3}, 0, None, "githyanki", T35))
        self.assertIn("perche", GS.atteso({"fighter": 3}, 0, None, "Medium humanoid (extraplanar)", T35))

    def test_il_mezzorco_non_e_un_modello_il_mezzo_immondo_si(self):
        self.assertIsNone(GS.modello("Medium humanoid (orc), mezzorco, half-orc", T35))
        self.assertIsNotNone(GS.modello("segugio infernale mezzo-immondo", T35))
        # dal lotto 5, settima parte, il mezzo-immondo ha il suo conto: guerriero di 3°, +1 fino a 4 dadi vita
        self.assertEqual(GS.atteso({"fighter": 3}, 0, None, "half-fiend human", T35)["min"], 4)
        self.assertIn("perche", GS.atteso({"fighter": 3}, 0, None, "human, pseudonatural template", T35))

    def test_creatura_base_con_livelli_e_una_forbice(self):
        """SRD, improving-monsters.md: ogre GS 3 con 4 DV; Barbaro 6 associato dà 9, non associato
        3 + 4×½ + 2 = 7."""
        ogre = {"gs": 3, "dv": 4}
        e = GS.atteso({"barbarian": 6}, 4, ogre, "Large giant", T35)
        self.assertEqual((e["min"], e["max"]), (7, 9))
        e = GS.atteso({"warrior": 2}, 4, ogre, "Large giant", T35)   # da PNG: sempre non associati
        self.assertEqual((e["min"], e["max"]), (4, 4))

    def test_creatura_base_senza_livelli_e_avanzata(self):
        ogre = {"gs": 3, "dv": 4}
        self.assertEqual(self.uno(GS.atteso({}, 4, ogre, "Large giant", T35)), 3)
        self.assertIn("perche", GS.atteso({}, 8, ogre, "Large giant", T35))
        self.assertIn("perche", GS.atteso({}, 6, None, "Medium plant", T35))


class Scheda(unittest.TestCase):
    def test_scarto_e_riga(self):
        v, nv = giudica("1", "Medium humanoid (dwarf, duergar), Rogue 1, LE", "1d6+2")
        self.assertEqual([(x["regola"], x["atteso"], x["ha"], x["riga"]) for x in v], [("numero.gs", "2", "1", 4)])
        self.assertEqual(nv, [])

    def test_giusta(self):
        self.assertEqual(giudica("2", "Medium humanoid (dwarf, duergar), Rogue 1, LE", "1d6+2"), ([], []))
        self.assertEqual(giudica("1/2", "Medium humanoid (goblinoid), hobgoblin, Warrior 1, LE", "1d8+1"), ([], []))

    def test_la_frazione_si_legge_dalla_riga(self):
        v, _ = giudica("1/2", "Small humanoid (goblinoid), goblin, Warrior 1, NE", "1d8+1")
        self.assertEqual([(x["atteso"], x["ha"]) for x in v], [("1/3", "1/2")])

    def test_la_classe_di_prestigio_scritta_nel_tipo_conta(self):
        """«Bardo 12 / Cantore delle tempeste 2»: 14 livelli: la classe che nessuna tabella conosce conta come classe da PG."""
        self.assertEqual(giudica("14", "Medium humanoid (elf), Bardo 12 / Cantore delle tempeste 2, NB", "14d6+42"),
                         ([], []))

    def test_senza_dadi_non_si_giudica(self):
        v, nv = giudica("7", "Large monstrous humanoid", "")
        self.assertEqual(v, [])
        self.assertEqual(len(nv), 1)

    def test_base_riconosciuta_dal_nome_col_tipo_e_i_dadi(self):
        v, nv = giudica("12", "Huge outsider (chaotic, evil, extraplanar), 12d8+96", "12d8+96",
                        titolo="Bebilith guardiano", nome="bebilith-guardiano-cr12.md")
        self.assertEqual(nv, [])
        self.assertEqual([(x["atteso"], x["ha"]) for x in v], [("10", "12")])

    def test_avanzata_per_dadi_vita(self):
        # SRD, «Improved Monster CR Increase»: drago +1 ogni 2 DV aggiunti, gigante +1 ogni 4
        drago = {"gs": 13, "dv": 20, "tipo": "dragon"}
        e = GS.atteso({}, 22, drago, "drago verde adulto", T35, dichiarata=True, stessa_taglia=True)
        self.assertEqual((e["min"], e["max"], e["regola"]), (14, 14, "gs.base.avanzata"))
        ogre = {"gs": 3, "dv": 4, "tipo": "giant"}
        e = GS.atteso({}, 8, ogre, "ogre", T35, dichiarata=True, stessa_taglia=False)
        self.assertEqual((e["min"], e["max"]), (4, 5))            # +1 se è cresciuta di taglia
        # trovata solo per nome (un flind non è uno gnoll avanzato), o con livelli di classe: non si conta
        self.assertIn("perche", GS.atteso({}, 8, ogre, "ogre", T35))
        self.assertIn("perche", GS.atteso({"barbarian": 2}, 8, ogre, "ogre", T35, dichiarata=True))
        self.assertIn("perche", GS.atteso({}, 3, ogre, "ogre", T35, dichiarata=True))   # meno dadi vita della base


class Modelli(unittest.TestCase):
    """I modelli dell'SRD col conto scritto nella riga «Challenge Rating» (lotto 5, settima parte)."""

    def test_scheletro_e_zombi_dai_dadi_vita(self):
        e = GS.atteso({}, 16, None, "Large undead, skeleton template", T35)
        self.assertEqual((e["min"], e["max"], e["regola"]), (7, 7, "gs.modello.dv"))
        self.assertEqual(GS.atteso({}, 1, None, "scheletro umano", T35)["min"], GS.frazione("1/3"))
        self.assertEqual(GS.atteso({}, 4, None, "zombi di ogre", T35)["min"], 1)
        self.assertIn("perche", GS.atteso({}, 24, None, "skeleton", T35))              # oltre i 20 dadi vita
        self.assertIn("perche", GS.atteso({"fighter": 2}, 4, None, "skeleton", T35))   # i livelli si perdono

    def test_base_piu_aumento(self):
        ogre = {"gs": 3, "dv": 4, "tipo": "giant"}
        self.assertEqual(GS.atteso({}, 4, ogre, "ogre mezzo-immondo", T35)["min"], 4)      # fino a 4 DV: +1
        self.assertEqual(GS.atteso({}, 4, ogre, "ogre immondo", T35)["min"], 4)            # da 4 a 7 DV: +1
        self.assertEqual(GS.atteso({}, 4, ogre, "half-dragon ogre", T35)["min"], 5)        # +2
        self.assertEqual(GS.atteso({}, 4, ogre, "ghost ogre (template)", T35)["min"], 5)
        # hobgoblin con sei livelli da PG, mezzo-immondo: 6, più 2 fra 5 e 10 dadi vita
        e = GS.atteso({"dragon shaman": 6}, 0, None, "hobgoblin mezzo-immondo, Dragon Shaman 6", T35)
        self.assertEqual((e["min"], e["max"], e["regola"]), (8, 8, "gs.modello"))
        # mezzo-drago: mai sotto 3
        self.assertEqual(GS.atteso({"warrior": 1}, 0, None, "half-dragon kobold warrior", T35)["min"], 3)

    def test_il_nome_della_scheda_trova_la_base(self):
        """«Hell Hound» nel titolo è «hellhound» nei dati (`[gs.nomi_base]`): 3, più 1 da mezzo-immondo con 4 dadi vita."""
        tipo = "Medium outsider (evil, extraplanar, fire, lawful), 4 HD, LE"
        self.assertEqual(giudica("4", tipo, "4d8+8", titolo="Hell Hound mezzo-immondo", nome="hell-hound-cr4.md"), ([], []))
        v, _ = giudica("6", tipo, "4d8+8", titolo="Hell Hound mezzo-immondo", nome="hell-hound-cr6.md")
        self.assertEqual([(x["atteso"], x["ha"]) for x in v], [("4", "6")])

    def test_base_dichiarata_avanzata_col_modello(self):
        """Gufo gigante (3, 4 DV) avanzato a 8 DV: +1 ogni 3 dadi vita; celestiale con 8 dadi vita: +2."""
        scheda = SCHEDA.replace("# {titolo}\n", "# {titolo}\n**Faction**: prova | **CR**: {gs} | **Source**: SRD 3.5 (gufo "
                                "gigante, avanzamento a 8 DV, modello celestiale) | **Status**: prova\n").replace(
            "pf: 30\n", "ca: 16\nca-dettaglio: (-1 taglia, +4 Des, +3 naturale)\npf: 52\nts: Temp +7, Rifl +10, Vol +4\n")
        with tempfile.TemporaryDirectory() as d:
            for gs, attese in (("6", []), ("7", [("6", "7")])):
                p = Path(d) / f"gufo-cr{gs}.md"
                p.write_text(scheda.format(gs=gs, tipo="Large magical beast (extraplanar), 8 DV, NB", dadi="8d10+8",
                                           titolo="Gufo gigante celestiale"), encoding="utf-8")
                v, nv = V.grado_di_sfida(p)
                self.assertEqual(([(x["atteso"], x["ha"]) for x in v], nv), (attese, []))

    def test_due_modelli_o_un_avanzamento_non_si_contano(self):
        ogre = {"gs": 3, "dv": 4, "tipo": "giant"}
        for dove in ("ogre mezzo-immondo avanzato", "ogre celestiale mezzo-drago", "ogre licantropo", "vampire spawn",
                     "ogre mezzo-immondo in sella"):
            self.assertIn("perche", GS.atteso({}, 4, ogre, dove, T35), dove)


class Bestiario(unittest.TestCase):
    #: scarti veri in attesa della decisione del DM (card del thread delle regole): oggi nessuno.
    #: Arbitrax e Tyrgarun sono chiusi dalle risposte del DM del 2026-11-14 (RC-002; molto vecchio, GS 19)
    #: Skeletal Dire Lion chiuso dalla risposta del DM del 2026-11-14 (16 dadi vita, GS 7)
    IN_ATTESA: "set[str]" = set()

    def test_il_bestiario_non_ha_altri_scarti(self):
        trovate, attese = [], set()
        for p in sorted((RADICE / "Bestiario").rglob("*.md")):
            v = V.grado_di_sfida(p)[0]
            if p.name in self.IN_ATTESA:
                attese |= {p.name} if v else set()
            else:
                trovate += [f"{x['file']}:{x['riga']} {x['testo']}" for x in v]
        self.assertEqual(trovate, [])
        self.assertEqual(attese, self.IN_ATTESA, "una scheda in attesa è stata corretta: toglierla dall'elenco")


if __name__ == "__main__":
    unittest.main()
