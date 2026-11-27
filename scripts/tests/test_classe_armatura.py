"""La CA ricostruita dalle voci (ADR-0126, lotto 1-bis)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dmcore import classe_armatura as CA  # noqa: E402


def campi(esito):
    return sorted(x["campo"] for x in esito[0])


class TestLettura(unittest.TestCase):
    def test_armatura_e_scudo_dalla_tabella(self):
        voci = CA.leggi("(+9 +1 full plate, +3 +1 heavy shield, +1 Dex)")
        self.assertEqual([(v.tipo, v.valore) for v in voci], [("armatura", 9), ("scudo", 3), ("des", 1)])
        self.assertEqual([v.atteso for v in voci[:2]], [9, 3])

    def test_il_mithral_alza_la_destrezza_massima(self):
        normale = CA.leggi("(+8 full plate, +1 Dex)")[0]
        mithral = CA.leggi("(+8 mithral full plate, +3 Dex)")[0]
        self.assertEqual(mithral.des_max, normale.des_max + 2)

    def test_una_clausola_a_condizione_non_entra(self):
        voci = CA.leggi("(+4 chain shirt, +2 Dex, +1 dodge vs giants)")
        self.assertNotIn("schivare", [v.tipo for v in voci])

    def test_senza_parentesi_non_ci_sono_voci(self):
        self.assertEqual(CA.leggi("contatto 12, sprovvista 14"), [])


class TestSomma(unittest.TestCase):
    def test_stesso_tipo_vale_il_piu_alto(self):
        voci = [CA.VoceCA(2, "deviazione", "anello"), CA.VoceCA(1, "deviazione", "incantesimo")]
        totale, scartate = CA.somma(voci)
        self.assertEqual(totale, 2)
        self.assertEqual([v.valore for v in scartate], [1])

    def test_schivare_si_somma(self):
        self.assertEqual(CA.somma([CA.VoceCA(1, "schivare", "a"), CA.VoceCA(1, "schivare", "b")])[0], 2)


class TestGiudizio(unittest.TestCase):
    def test_una_ca_giusta_non_ha_scarti(self):
        esito = CA.giudica(23, "(+9 +1 full plate, +3 +1 heavy shield, +1 Dex) touch 11, flat-footed 22", 1)
        self.assertEqual(esito, ([], []))

    def test_la_somma_sbagliata_e_uno_scarto(self):
        esito = CA.giudica(24, "(+9 +1 full plate, +3 +1 heavy shield, +1 Dex)", 1)
        self.assertEqual(campi(esito), ["CA"])
        self.assertEqual(esito[0][0]["atteso"], 23)

    def test_il_bonus_fuori_tabella_e_uno_scarto_anche_se_la_somma_torna(self):
        esito = CA.giudica(24, "(+10 +1 full plate, +3 +1 heavy shield, +1 Dex)", 1)
        self.assertEqual(campi(esito), ["CA.armatura"])

    def test_la_destrezza_oltre_il_massimo_dell_armatura(self):
        esito = CA.giudica(21, "(+8 full plate, +3 Dex)", 3)
        self.assertIn("CA.des", campi(esito))

    def test_contatto_e_sprovvista(self):
        esito = CA.giudica(19, "(+4 chain shirt, +3 Dex, +2 deflection) touch 16, flat-footed 16", 3)
        self.assertEqual(campi(esito), ["CA.contatto"])
        self.assertEqual(esito[0][0]["atteso"], 15)
        esito = CA.giudica(19, "(+4 chain shirt, +3 Dex, +2 deflection) touch 15, flat-footed 17", 3)
        self.assertEqual(campi(esito), ["CA.sprovvista"])

    def test_schivare_prodigioso_tiene_la_destrezza(self):
        dettaglio = "(+4 chain shirt, +3 Dex) touch 13, flat-footed 17"
        self.assertEqual(campi(CA.giudica(17, dettaglio, 3)), ["CA.sprovvista"])
        self.assertEqual(CA.giudica(17, dettaglio, 3, testo="Schivare prodigioso"), ([], []))

    def test_senza_voci_non_e_verificabile_e_lo_dice(self):
        scarti, nv = CA.giudica(18, "contatto 12", 2)
        self.assertEqual(scarti, [])
        self.assertEqual(len(nv), 1)

    def test_i_nomi_senza_numeri_non_sono_un_conto(self):
        scarti, nv = CA.giudica(18, "(full plate, heavy shield)", 0)
        self.assertEqual(scarti, [])
        self.assertEqual(len(nv), 1)


class TestCancello(unittest.TestCase):
    """Quello che il controllo ha trovato è stato corretto: da qui in poi è un cancello."""

    def test_il_bestiario_non_ha_scarti_di_ca_di_sensi_o_di_cd(self):
        import verifica_scheda as V
        radice = Path(__file__).resolve().parents[2]
        trovate = []
        for p in sorted((radice / "Bestiario").rglob("*.md")):
            trovate += [f"{x['file']}:{x['riga']} {x['testo']}" for x in V.classe_armatura(p)[0]]
        self.assertEqual(trovate, [])

    def test_i_dadi_vita_di_piu_classi_si_sommano(self):
        import conformita_statblocchi as C
        from types import SimpleNamespace
        self.assertEqual(C._dv(SimpleNamespace(pf_dado="12d8+4d10+80")), 16)


if __name__ == "__main__":
    unittest.main()
