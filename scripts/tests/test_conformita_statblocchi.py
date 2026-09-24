"""Le identita' del 3.5 sugli statblocchi, e i falsi positivi che le hanno insegnate.

⚠️ **Quasi ogni prova qui sotto e' un errore del verificatore, non delle schede.**
La prima stesura segnava 23 statblocchi «da correggere»; dopo aver guardato i
numeri uno per uno ne restavano 11, e il resto erano regole scritte male: i DV
razziali del minotauro letti come totali, la «Robustezza Migliorata» contata
come Robustezza, l'errata del retriever letta come dato. Una prova per ciascuno.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import conformita_statblocchi as C  # noqa: E402
from dmcore import lettura_creatura as LC  # noqa: E402


def scheda(corpo: str, prosa: str = "", titolo: str = "# Prova") -> LC.Scheda:
    """Una scheda finta su disco, letta dal lettore vero."""
    d = Path(tempfile.mkdtemp())
    p = d / "prova-cr3.md"
    p.write_text(f"{titolo}\n\n```statblocco\n{corpo}\n```\n\n{prosa}\n", encoding="utf-8")
    return LC.leggi(p)


class TestLeIdentitaDelSRD(unittest.TestCase):
    def test_un_guerriero_che_torna(self):
        s = scheda("gs: 3\ntipo: Medium humanoid (human), Fighter 3\nca: 18\npf: 28\n"
                   "pf-dado: 3d10+6\nts: Temp +5, Rifl +2, Vol +1\n"
                   "attributi: For 16 Des 12 Cos 14 Int 10 Sag 10 Car 8",
                   "BAB +3; Lotta +6.")
        self.assertEqual(C.scarti(C.verifica(s)), {})

    def test_un_bab_sbagliato_e_un_errore_solo(self):
        # un Ladro 1 ha BAB +0: il +1 e' il caso del duergar, e la lotta che lo
        # segue non deve contare come secondo errore
        s = scheda("gs: 1\ntipo: Medium humanoid, Rogue 1\nca: 15\npf: 8\npf-dado: 1d6+2\n"
                   "ts: Temp +2, Rifl +4, Vol +0\nattributi: For 12 Des 15 Cos 15 Int 14 Sag 10 Car 4",
                   "BAB +1; Lotta +2.")
        self.assertEqual(set(C.scarti(C.verifica(s))), {"BAB"})

    def test_i_pf_si_tirano_e_la_fascia_e_quella_legale(self):
        # Morlin: 93 pf dove la media ne da' 84, legale perche' tirati
        s = scheda("gs: 12\ntipo: Medium humanoid (dwarf), Cleric 6 / Expert 6\nca: 23\npf: 93\n"
                   "pf-dado: 6d8+6d6+36\nts: Temp +10, Rifl +3, Vol +14\n"
                   "attributi: For 16 Des 8 Cos 16 Int 10 Sag 19 Car 10")
        self.assertNotIn("pf", C.scarti(C.verifica(s)))

    def test_pf_fuori_dalla_fascia_legale(self):
        s = scheda("gs: 12\ntipo: Medium humanoid, Druid 12\nca: 19\npf: 120\npf-dado: 12d8\n"
                   "ts: Temp +9, Rifl +5, Vol +12\nattributi: For 14 Des 12 Cos 13 Int 8 Sag 18 Car 10")
        self.assertIn("pf", C.scarti(C.verifica(s)))


class TestIFalsiPositiviGiaTrovati(unittest.TestCase):
    def test_i_dv_razziali_nel_tipo_non_sono_il_totale(self):
        # «Minotauro (6 HD) / Barbarian 1», e il totale 7 sta accanto ai pf
        t = "tipo: Large monstrous humanoid, Minotauro (6 HD) / Barbarian 1\n**hp 67** (7 HD)"
        self.assertEqual(LC.dv_totali(t), 7)

    def test_una_classe_non_srd_rende_la_composizione_ignota(self):
        s = scheda("gs: 10\ntipo: Medium humanoid (dwarf), Paladin 8 / Hammer of Moradin 2\n"
                   "ca: 20\npf: 80\nts: Temp +13, Rifl +3, Vol +8\n"
                   "attributi: For 14 Des 8 Cos 14 Int 10 Sag 14 Car 14")
        self.assertFalse(s.composizione_nota)

    def test_l_umanoide_da_un_dv_senza_classe_non_si_giudica(self):
        # un 1 DV umanoide ha un livello di classe al posto del DV razziale
        s = scheda("gs: 1\ntipo: Medium humanoid (elf)\nca: 15\npf: 5\npf-dado: 1d8+1\n"
                   "ts: Temp +3, Rifl +2, Vol +2\nattributi: For 13 Des 15 Cos 12 Int 12 Sag 13 Car 12",
                   "BAB/Grapple: +1/+2")
        self.assertFalse(s.composizione_nota)
        self.assertNotIn("BAB", C.verifica(s))

    def test_le_errata_non_sono_il_dato(self):
        s = scheda("gs: 11\ntipo: Huge construct\nca: 21\npf: 135\npf-dado: 10d10+80\n"
                   "ts: Temp +3, Rifl +6, Vol +3\nattributi: For 31 Des 17 Cos — Int — Sag 11 Car 1\n"
                   "voci:\n  - ⚠ La prosa diceva BAB +10: il SRD dice BAB +7.",
                   "BAB +7; Lotta +25.")
        self.assertEqual(s.bab, 7)

    def test_il_tipo_umanoide_ha_il_ts_buono_che_varia(self):
        # SRD: lo gnoll ha buona la Tempra, il bugbear i Riflessi
        s = scheda("gs: 3\ntipo: Medium humanoid (gnoll) HD 3d8+6 (19 HP)\nca: 18\npf: 19\n"
                   "pf-dado: 3d8+6\nts: Temp +5, Rifl +2, Vol +1\n"
                   "attributi: For 17 Des 12 Cos 14 Int 10 Sag 10 Car 9")
        self.assertEqual(C.scarti(C.verifica(s)), {})

    def test_lottare_migliorato_si_riconosce_anche_in_italiano(self):
        self.assertTrue(LC.LOTTA_MIGLIORATA.search("Talenti: Lottare Migliorato"))


class TestIlTemplateSpiegaLoScarto(unittest.TestCase):
    def test_advanced_su_caratteristiche_non_potenziate(self):
        # pf, TS e lotta con +4 a tutto, caratteristiche della base: e' un Advanced
        s = scheda("gs: 4\ntipo: Large giant, 4 HD\nca: 18\npf: 34\npf-dado: 4d8+16\n"
                   "ts: Temp +8, Rifl +2, Vol +3\nattributi: For 21 Des 8 Cos 15 Int 6 Sag 10 Car 7",
                   "**hp 34** (4 HD). BAB +3; Lotta +14.")
        g = C.giudica(s)
        self.assertTrue(g["scarti"])
        self.assertEqual(g["template"], "Advanced")


class TestITalentiMordono(unittest.TestCase):
    """Il DM: «forse l'intuizione per trovare questi errori sono i talenti»."""

    def test_volonta_di_ferro_alza_il_minimo(self):
        # Mira Serani: «Vol +8 (Ferrea Volonta')» col talento che non contava
        corpo = ("gs: 8\ntipo: Medium magical beast, 9 DV (3 aranea + 6 Stregone)\nca: 15\npf: 47\n"
                 "ts: Temp +7, Rifl +7, Vol +8\nattributi: For 11 Des 15 Cos 14 Int 14 Sag 13 Car 16\n"
                 "voci:\n  - Talenti: Ferrea Volontà")
        s = scheda(corpo, "**hp 47** (9 HD)", titolo="# Mira (Stregone 6)")
        self.assertIn("Vol", C.scarti(C.verifica(s)))

    def test_iniziativa_migliorata_scritta_compressa(self):
        # «Iniziativa/Scacciare Migliorato» sono due talenti in una parola
        self.assertEqual(LC.talenti("Talenti: Iniziativa/Scacciare Migliorato")["init"], 4)

    def test_iniziativa_e_un_identita(self):
        s = scheda("gs: 3\nca: 14\npf: 15\niniziativa: -1\nts: Temp +6, Rifl +0, Vol +0\n"
                   "attributi: For 14 Des 10 Cos 16 Int 2 Sag 11 Car 9\nvoci:\n  - Talenti: Allerta")
        self.assertEqual(C.verifica(s)["iniziativa"][2], -1)

    def test_senza_elenco_di_talenti_il_piu_quattro_non_si_giudica(self):
        # il razorfiend rosso eredita Iniziativa Migliorata dalla base nera
        s = scheda("gs: 9\nca: 24\npf: 115\niniziativa: +5\nts: Temp +12, Rifl +8, Vol +9\n"
                   "attributi: For 22 Des 12 Cos 20 Int 8 Sag 13 Car 12")
        self.assertEqual(C.verifica(s)["iniziativa"][2], 0)

    def test_la_lotta_si_verifica_anche_senza_composizione(self):
        # BAB, For e taglia sono scritti: i DV non servono
        s = scheda("gs: 1\nca: 15\npf: 5\nts: Temp +3, Rifl +2, Vol +0\n"
                   "attributi: For 8 Des 14 Cos 12 Int 12 Sag 10 Car 12",
                   "**Size/Type**: Small humanoid | **BAB/Grapple**: +0/-4")
        self.assertEqual(C.verifica(s)["lotta"][2], 1)


class TestLaVarianteAdvanced(unittest.TestCase):
    def test_la_ca_conta_anche_la_destrezza(self):
        # Ghaurush «Cenere Piena» scriveva CA 23: +2 naturale, dimenticata la Des
        corpo = ("gs: 16\nca: 21\npf: 107\npf-dado: 5d8+8d4+65\nts: Temp +11, Rifl +3, Vol +11\n"
                 "attributi: For 21 Des 10 Cos 21 Int 14 Sag 14 Car 22")
        prosa = "**Variante «Cenere Piena» (Advanced) — CR 17**: **hp 133, CA 23**."
        esito = C.verifica_variante_advanced(scheda(corpo, "DV 5d8 + 8d4. " + prosa))
        self.assertEqual(esito["variante pf"][2], 0)
        self.assertEqual(esito["variante CA"][2], -2)
        self.assertEqual(esito["variante GS"][2], 0)

    def test_la_marca_non_e_la_variante(self):
        corpo = ("gs: 16\nca: 21\npf: 107\npf-dado: 5d8+8d4+65\nts: Temp +11, Rifl +3, Vol +11\n"
                 "attributi: For 21 Des 10 Cos 21 Int 14 Sag 14 Car 22")
        prosa = ("> [INFERRED] variante Advanced, CA 23 → 25\n\n"
                 "**Variante (Advanced) — CR 17**: **hp 133, CA 25**.")
        self.assertEqual(C.verifica_variante_advanced(scheda(corpo, "DV 5d8 + 8d4.\n\n" + prosa))["variante CA"][2], 0)

    def test_un_template_non_spiega_caratteristiche_scelte(self):
        s = scheda("gs: 4\ntipo: Large giant, 4 HD\nca: 18\npf: 34\npf-dado: 4d8+16\n"
                   "ts: Temp +8, Rifl +2, Vol +3\nattributi: For 21 Des 8 Cos 15 Int 6 Sag 10 Car 7",
                   "**hp 34** (4 HD). BAB +3; Lotta +14.")
        s.provenienza = "generate"
        self.assertIsNone(C.giudica(s)["template"])


class TestPfDado(unittest.TestCase):
    def test_la_formula_scritta_vince(self):
        t = "pf-dado: 4d8\n**DV 4d8 + 6d12**. **hp 77**"
        self.assertEqual(LC.dadi_vita(t)[0], [(4, 8), (6, 12)])
        self.assertIn("formula scritta", LC.pf_dado_sospetto(t, 9))

    def test_robustezza_e_robustezza_migliorata_non_sono_lo_stesso_talento(self):
        self.assertEqual(LC.robustezza("Talenti: Robustezza", 5), 3)
        self.assertEqual(LC.robustezza("Talenti: Robustezza Migliorata", 5), 5)
        self.assertEqual(LC.robustezza("Talenti: Robustezza, Robustezza Migliorata", 5), 8)

    def test_il_gs_si_legge_se_non_lo_passano(self):
        # `1d8+2` per un chierico di 3° passava per dadi vita a chi non dava il GS
        self.assertIsNotNone(LC.pf_dado_sospetto("gs: 4\npf-dado: 1d8+2\n"))

    def test_la_ricostruzione_dalle_classi(self):
        s = scheda("gs: 12\ntipo: Medium humanoid (dwarf), Cleric 6 / Expert 6\nca: 23\npf: 93\n"
                   "pf-dado: 1d8+7\nts: Temp +10, Rifl +3, Vol +14\n"
                   "attributi: For 16 Des 8 Cos 16 Int 10 Sag 19 Car 10",
                   "**hp 93** (12 HD)")
        s.provenienza = "trascritte"
        c = C.pf_dado_corretto(s)
        self.assertEqual(c["nuovo"], "6d8+6d6+36")
        self.assertTrue(c["legale"])


class TestIlRepoVero(unittest.TestCase):
    def test_il_cancello_e_verde(self):
        self.assertEqual(C.controlla_pf_dado(), [])

    def test_nessuno_statblocco_resta_da_correggere(self):
        # quelli che restano sono decisioni del DM, registrate nel piano
        r = C.riepilogo(C.tutte())
        self.assertEqual(r["da_correggere"], 0)

    def test_le_decisioni_aperte_hanno_una_casa(self):
        # ogni decisione aperta punta a uno statblocco che esiste
        nomi = {p.name for p in ROOT.glob("Bestiario/**/*.md")}
        for f in C.decisioni_aperte():
            self.assertIn(f, nomi)

    def test_una_decisione_chiusa_non_scusa_piu(self):
        # D1 (goblin, For 11) e' barrata dal 2026-09-23: il goblin torna a
        # essere giudicato, e se non tornasse sarebbe «da correggere»
        self.assertNotIn("goblin-warrior1-cr05.md", C.decisioni_aperte())
        g = next(x for x in C.tutte() if x["file"].endswith("goblin-warrior1-cr05.md"))
        self.assertIsNone(g["decisione"])
        self.assertEqual(g["scarti"], {})


class TestIncorporeo(unittest.TestCase):
    def test_l_incorporeo_attacca_con_la_destrezza(self):
        # SRD: senza Forza, la mischia di un incorporeo usa la Des. BAB +4 (non
        # morto 9 DV), Des 18 (+4), Grande −1 → +7. Con la Forza «—» dava +3
        s = scheda("gs: 8\ntipo: Large undead (incorporeal), 9d12\nca: 20\npf: 58\n"
                   "pf-dado: 9d12\nts: Temp +3, Rifl +7, Vol +7\n"
                   "attributi: For — Des 18 Cos — Int 11 Sag 12 Car 24\n"
                   "attacchi:\n  - Mischia morso incorporeo +7 (2d6)")
        self.assertEqual(C.verifica(s)["attacco"], (7, 7, 0))

    def test_un_corporeo_senza_accurata_usa_la_forza(self):
        s = scheda("gs: 3\ntipo: Medium humanoid (human), Fighter 3\nca: 16\npf: 28\n"
                   "pf-dado: 3d10+6\nts: Temp +5, Rifl +2, Vol +1\n"
                   "attributi: For 16 Des 18 Cos 14 Int 10 Sag 10 Car 8\n"
                   "attacchi:\n  - Mischia spada lunga +6 (1d8+3)")
        self.assertEqual(C.verifica(s)["attacco"][1], 6)     # BAB 3 + For 3, non Des 4


class TestNonMortoPF1e(unittest.TestCase):
    """D5: il fantasma PF1e ha d8, BAB 3/4 e il Carisma al posto della Costituzione."""
    CORPO = ("gs: 8\ntipo: Large undead (incorporeal){pf1e}, 9d8\nca: 20\npf: 103\n"
             "pf-dado: 9d8+63\nts: Temp +10, Rifl +7, Vol +7\n"
             "attributi: For — Des 18 Cos — Int 11 Sag 12 Car 24")

    def test_dichiarato_torna(self):
        e = C.verifica(scheda(self.CORPO.format(pf1e=", fantasma PF1e")))
        self.assertEqual({k: v[2] for k, v in e.items() if isinstance(v, tuple)},
                         {"pf": 0, "Temp": 0, "Rifl": 0, "Vol": 0})

    def test_senza_dichiarazione_e_un_non_morto_3_5(self):
        # la prova che morde: senza «PF1e» il Carisma non entra, e Tempra e pf non tornano
        e = C.verifica(scheda(self.CORPO.format(pf1e="")))
        self.assertTrue(any(v[2] for k, v in e.items() if isinstance(v, tuple) and k in ("pf", "Temp")))


class TestIlGiroCircolare(unittest.TestCase):
    """🐛 Il bonus di `pf-dado` ricavato dai pf, e la Cos ricavata da quel bonus.

    Khorn scrive «8d10+24, Cos 16» e Tempra +9; la ricostruzione supponeva la
    media dei pf e gli dava `8d10+32`, e il generatore ne ricavava Cos 18.
    """

    def test_la_tempra_viene_prima_della_media(self):
        s = LC.leggi(ROOT / "Bestiario/png/Khorn/khorn-ufficiale-hammerfist-cr8.md")
        c = C.pf_dado_corretto(s, forza=True)
        self.assertEqual(c["nuovo"], "8d10+24")
        self.assertIn("dalla Tempra +9", c["bonus"])

    @staticmethod
    def _guerriero(pf: int, temp: str) -> LC.Scheda:
        s = scheda(f"gs: 4\ntipo: Medium humanoid (human), Fighter 4\npf: {pf}\n"
                   f"pf-dado: 1d8+4\nts: Temp {temp}, Rifl +1, Vol +1\n"
                   "attributi: For 16 Des 12 Cos 10 Int 10 Sag 10 Car 8\n"
                   "attacchi:\n  - Mischia spada lunga +6 (1d8+4)")
        s.provenienza = "generate"
        return s

    def test_dentro_la_fascia_vince_la_tempra(self):
        c = C.pf_dado_corretto(self._guerriero(30, "+5"), forza=True)
        self.assertEqual(c["nuovo"], "4d10+4")        # Guerriero 4 (+4) → Cos +1
        self.assertIn("dalla Tempra +5", c["bonus"])

    def test_fuori_fascia_si_torna_ai_pf(self):
        # la prova che morde: la Tempra dice Cos +0, ma 4d10 non arrivano a 41
        c = C.pf_dado_corretto(self._guerriero(41, "+4"), forza=True)
        self.assertIn("dai pf 41", c["bonus"])


if __name__ == "__main__":
    unittest.main()
