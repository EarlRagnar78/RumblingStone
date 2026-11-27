"""Il danno delle armi ricostruito dalla tabella (ADR-0126, lotto 2)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dmcore import danno as D  # noqa: E402


def campi(esito):
    return sorted(x["campo"] for x in esito[0])


class TestTabella(unittest.TestCase):
    def test_le_armi_dell_srd_ci_sono_coi_nomi_italiani(self):
        self.assertEqual(D.arma_di("Mischia spada lunga perfetta")["nome"], "Longsword")
        self.assertEqual(D.arma_di("Mischia ascia da guerra nanica +3")["nome"], "Waraxe, dwarven")
        self.assertEqual(D.arma_di("greataxe")["dado"], "1d12")
        self.assertIsNone(D.arma_di("Mischia morso"))

    def test_il_nome_piu_lungo_vince(self):
        self.assertEqual(D.arma_di("mazzafrusto pesante")["nome"], "Flail, heavy")
        self.assertEqual(D.arma_di("arco corto composito")["nome"], "Shortbow, composite")

    def test_il_dado_segue_la_taglia(self):
        self.assertEqual(D.dado_per_taglia("1d10", 1), "2d8")      # randello pesante di un ogre
        self.assertEqual(D.dado_per_taglia("1d12", 1), "3d6")
        self.assertEqual(D.dado_per_taglia("1d8", -1), "1d6")
        self.assertEqual(D.dado_per_taglia("2d6", 2), "4d6")

    def test_la_taglia_dal_tipo_o_dalla_ca(self):
        self.assertEqual(D.passi_di_taglia("Large giant, NE"), 1)
        self.assertEqual(D.passi_di_taglia("Small humanoid (goblinoid)"), -1)
        self.assertEqual(D.passi_di_taglia("", "(-1 size, +8 natural)"), 1)
        self.assertEqual(D.passi_di_taglia("umanoide"), 0)


class TestLettura(unittest.TestCase):
    def test_dado_bonus_e_critico(self):
        a = D.leggi("Mischia ascia bipenne +1 +13/+8 (1d12+10/x3)")[0]
        self.assertEqual((a.dado, a.bonus, a.minaccia, a.moltiplicatore), ("1d12", 10, 20, 3))
        a = D.leggi("Mischia spadone +2 +21 (2d6+11, 19-20/×2, +2d6 contro i buoni)")[0]
        self.assertEqual((a.dado, a.bonus, a.minaccia, a.moltiplicatore), ("2d6", 11, 19, 2))
        a = D.leggi("Mischia martello da guerra +1 gelido +14/+9 (1d8+3 +1d6 freddo/x3)")[0]
        self.assertEqual((a.bonus, a.moltiplicatore), (3, 3))

    def test_una_riga_a_condizione_non_si_giudica(self):
        attacchi = D.leggi("Mischia ascia a due mani +1 +29 (3d6+20, 20/×3) in Ira; +26 (3d6+16) fuori dall'Ira")
        self.assertTrue(attacchi[0].nome.startswith("\0"))
        self.assertFalse(attacchi[1].nome.startswith("\0"))
        self.assertIn("ascia a due mani", attacchi[1].nome)
        self.assertEqual(attacchi[1].moltiplicatore, 3)       # il critico della stessa arma


class TestGiudizio(unittest.TestCase):
    def test_un_attacco_giusto_non_ha_scarti(self):
        self.assertEqual(D.giudica("Mischia ascia bipenne +1 +13/+8 (1d12+7/x3)", 4)[0], [])
        self.assertEqual(D.giudica("Mischia spada lunga +9 (1d8+2/19-20)", 2)[0], [])

    def test_il_dado_sbagliato(self):
        self.assertEqual(campi(D.giudica("Mischia spada lunga +9 (1d10+2/19-20)", 2)), ["danno.dado"])
        self.assertEqual(D.giudica("Mischia randello pesante +15 (2d8+10)", 7, "Large giant")[0], [])

    def test_il_critico_non_scritto_o_sbagliato(self):
        esito = D.giudica("Mischia spada lunga +9 (1d8+2)", 2)
        self.assertEqual(campi(esito), ["danno.critico"])
        self.assertEqual(esito[0][0]["atteso"], "19-20/x2")
        self.assertEqual(campi(D.giudica("Mischia ascia bipenne +9 (1d12+3/x2)", 2)), ["danno.critico"])
        self.assertEqual(D.giudica("Mischia mazza pesante +9 (1d8+2)", 2)[0], [])     # 20/x2 si può tacere

    def test_critico_migliorato_e_arma_affilata_raddoppiano_la_minaccia(self):
        riga = "Mischia spada lunga +9 (1d8+2/17-20)"
        self.assertEqual(campi(D.giudica(riga, 2)), ["danno.critico"])
        self.assertEqual(D.giudica(riga, 2, talenti="Critico Migliorato (spada lunga)")[0], [])
        self.assertEqual(D.giudica("Mischia spada lunga affilata +9 (1d8+2/17-20)", 2)[0], [])
        self.assertEqual(campi(D.giudica(riga, 2, talenti="Critico Migliorato (pugnale)")), ["danno.critico"])

    def test_due_mani_una_volta_e_mezza(self):
        self.assertEqual(campi(D.giudica("Mischia mazzafrusto pesante +13 (1d10+3/19-20)", 3)), ["danno.bonus"])
        self.assertEqual(D.giudica("Mischia mazzafrusto pesante +13 (1d10+4/19-20)", 3)[0], [])

    def test_a_una_mano_senza_scudo_valgono_le_due_letture(self):
        self.assertEqual(D.giudica("Mischia spada lunga +9 (1d8+6/19-20)", 4, scudo=False)[0], [])
        self.assertEqual(campi(D.giudica("Mischia spada lunga +9 (1d8+6/19-20)", 4, scudo=True)), ["danno.bonus"])

    def test_arma_specializzata_solo_sulla_sua_arma(self):
        riga = "Mischia spada lunga +9 (1d8+4/19-20)"
        self.assertEqual(D.giudica(riga, 2, talenti="Arma Specializzata (spada lunga)")[0], [])
        self.assertEqual(campi(D.giudica(riga, 2, talenti="Arma Specializzata (ascia bipenne)")), ["danno.bonus"])

    def test_la_mano_secondaria_prende_meta_forza(self):
        riga = "Mischia spada corta +1 +12/+7 (1d6+4/19-20) e spada corta +1 +12 (1d6+2/19-20)"
        self.assertEqual(D.giudica(riga, 3, talenti="Combattere con Due Armi")[0], [])

    def test_archi_e_balestre(self):
        self.assertEqual(D.giudica("Distanza arco lungo +6 (1d8/x3)", 2)[0], [])
        self.assertEqual(campi(D.giudica("Distanza arco lungo +6 (1d8+2/x3)", 2)), ["danno.bonus"])
        self.assertEqual(D.giudica("Distanza arco lungo composito +6 (1d8+2/x3)", 2)[0], [])
        self.assertEqual(D.giudica("Distanza balestra leggera +6 (1d8/19-20)", 3)[0], [])
        self.assertEqual(D.giudica("Distanza giavellotto +9 (1d6+3)", 3)[0], [])

    def test_lo_scudo_non_da_potenziamento_al_danno(self):
        self.assertEqual(D.giudica("Mischia colpo di scudo pesante +1 +12 (1d4+2)", 2)[0], [])

    def test_l_attacco_naturale_e_l_arma_ignota_non_sono_violazioni(self):
        scarti, nv = D.giudica("Mischia morso +6 (1d8+3); Mischia nerbo +5 (1d3)", 3)
        self.assertEqual(scarti, [])
        self.assertEqual(len(nv), 2)

    def test_specialista_del_martello_vale_solo_sul_martello_da_guerra(self):
        riga = "Mischia martello da guerra +2 +15 (1d8+7/x3)"
        self.assertEqual(D.giudica(riga, 3, talenti="specialista del martello")[0], [])
        self.assertEqual(campi(D.giudica("Mischia mazza pesante +15 (1d8+5)", 3, talenti="specialista del martello")),
                         ["danno.bonus"])


class TestCancello(unittest.TestCase):
    """Quello che il controllo ha trovato è stato corretto: da qui in poi è un cancello."""

    #: scarti veri che aspettano il DM: nessuno (Balvar corretto il 2026-11-13 col master di ARC-07)
    IN_ATTESA: "set[str]" = set()

    def test_il_bestiario_non_ha_scarti_di_danno(self):
        import verifica_scheda as V
        radice = Path(__file__).resolve().parents[2]
        trovate = []
        for p in sorted((radice / "Bestiario").rglob("*.md")):
            if p.name not in self.IN_ATTESA:
                trovate += [f"{x['file']}:{x['riga']} {x['testo']}" for x in V.danno(p)[0]]
        self.assertEqual(trovate, [])

    def test_il_plugin_e_quello_che_l_estrattore_scrive(self):
        import tomllib
        radice = Path(__file__).resolve().parents[2]
        d = tomllib.loads((radice / "sistemi/dnd35/dati/armi.toml").read_text(encoding="utf-8"))
        self.assertEqual(len(d["armi"]), 72)
        self.assertEqual(len({a["nome"] for a in d["armi"]}), 72)


if __name__ == "__main__":
    unittest.main()
