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
        s = scheda("gs: 10\ntipo: Medium humanoid (dwarf), Paladin 8 / Martello di Nessuno 2\n"
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

    def test_il_talento_di_una_variante_non_e_della_scheda(self):
        # hobgoblin regolare (audit del 2026-11-18): la Volontà di Ferro sta
        # solo nella riga della variante «Combattente GS2»; contarla dava Vol +1≠3
        testo = ("Talenti: Allerta, Arma Focalizzata (spada lunga); mantello della resistenza +1\n"
                 "**Variante «Combattente GS2»**: Volontà di Ferro al posto di Arma Focalizzata.")
        self.assertEqual(LC.talenti(testo).get("Vol"), 1)
        corpo = ("gs: 2\ntipo: Medium humanoid (goblinoid), Warrior 3\nca: 19\npf: 23\n"
                 "ts: Temp +6, Rifl +3, Vol +1\nattributi: For 13 Des 13 Cos 14 Int 10 Sag 9 Car 8\n"
                 "voci:\n  - Talenti: Allerta, Arma Focalizzata (spada lunga)\n"
                 "  - Altro equipaggiamento: mantello della resistenza +1")
        s = scheda(corpo, "**hp 23** (3 HD)\n**Variante «Combattente GS2»**: Volontà di Ferro al posto di "
                   "Arma Focalizzata.", titolo="# Hobgoblin (Warrior 3)")
        self.assertNotIn("Vol", C.scarti(C.verifica(s)))

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
        # i numeri di Khorn com'erano quando il difetto e' stato trovato, con le
        # caratteristiche generate: dal 2026-10-16 la scheda vera le ha scritte a
        # mano, e la ricostruzione legge la Cos invece della Tempra.
        s = scheda("gs: 8\ntipo: Medium humanoid (dwarf), Fighter 8, LG\npf: 76\n"
                   "pf-dado: 1d8+6\nts: Temp +9, Rifl +3, Vol +4\n"
                   "attributi: For 16 Des 4 Cos 16 Int 9 Sag 11 Car 15\n"
                   "attacchi:\n  - Mischia martello da guerra +1 +14/+9 (1d8+6/x3)")
        s.provenienza = "generate"
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


class TestStatblocchiNeiMaster(unittest.TestCase):
    """D7 di MASTER-DEF: i conti degli statblocchi scritti nei master."""

    FAUCI = (
        "#### FAUCI DI PALUDE\n"
        "**Caratteristiche:** For 31, Des 10, Cos 25, Int 16, Sag 17, Car 16\n"
        "**Iniziativa:** +4;\n"
        "**CA:** 29 (-2 taglia, +21 naturale), contatto 8\n"
        "**PF:** {pf} (25d12+175)\n"
        "**Attacco Base:** +25;\n"
        "**Lotta:** +43\n"
        "**Talenti:** Allerta, Iniziativa Migliorata\n"
    )

    def conti(self, testo):
        return [x for b in C._blocchi_del_master(testo) for x in C.conti_del_master(b)]

    def test_la_scheda_giusta_torna(self):
        self.assertEqual(self.conti(self.FAUCI.format(pf=337)), [])

    def test_i_pf_vecchi_di_fauci_non_tornano(self):
        # il 312 della Guida DM prima della #241: 25d12 fanno 162 di media
        (x,) = self.conti(self.FAUCI.format(pf=312))
        self.assertEqual((x["campo"], x["scritto"], x["atteso"]), ("PF", 312, 337))

    def test_il_potenziamento_dell_armatura_non_e_una_voce(self):
        testo = ("#### TEMPESTAS\n**Caratteristiche:** For 10, Des 16\n"
                 "**CA:** 20 (+6 giaco di maglia +2, +3 Des, +1 deflessione), contatto 14\n"
                 "**PF:** 91 (14d6+42)\n")
        self.assertEqual(self.conti(testo), [])

    def test_la_lotta_conta_la_taglia(self):
        testo = self.FAUCI.format(pf=337).replace("+43", "+35")
        (x,) = self.conti(testo)
        self.assertEqual((x["campo"], x["atteso"]), ("Lotta", 43))

    def test_e_un_rapporto_non_un_cancello(self):
        self.assertEqual(C.main(["--master", str(ROOT / "08_La Battaglia Di Hammerfist" / "ARC08-01-GUIDA-DM.md")]), 0)


class TestRecintiNeiMaster(unittest.TestCase):
    """2026-11-03: i boss recintati di ADR-0091 (Skullcrusher, Zog'tar) e le loro CD."""

    DRAGO = (
        "### A.1 · Adulto\n\n```statblocco\nnome: Drago\ngs: 14\n"
        "tipo: Drago Enorme (acqua)\nca: 33\n"
        "ca-dettaglio: contatto 10, impreparato 31 (−2 taglia, +2 DES, +23 nat)\n"
        "pf: 297\npf-dado: 22d12+154\nts: Temp +20\n"
        "attributi: For 31 Des 14 Cos 25 Int 18 Sag 19 Car 18\n"
        "sensi: scurovisione 36 m\n```\n"
        "**Difesa** **CA 33** (−2 taglia, +2 DES, +23 nat) · **pf 297** (22d12+154)\n\n"
        "**Attacco** **Schiacciare** 2d8+15, Riflessi CD 28 · **Soffio acido** (Sop) linea, "
        "Riflessi CD {soffio} dimezza · **Capacità magiche** 1/giorno *corrompere l'acqua* (CD 25)\n\n"
        "**Statistiche** For 31 · **Talenti** Capacità Focalizzata (soffio), Virata\n\n"
        "**Capacità speciali**\n- **Presenza Terrificante** (Str): Volontà CD 25.\n"
    )
    VECCHIO = (
        "\n### A.1-bis · Vecchio\n\n```statblocco\nnome: Vecchio\ngs: 17\n"
        "tipo: Drago Enorme (acqua)\nca: 36\npf: 337\npf-dado: 25d12+175\nts: Temp +21\n"
        "attributi: For 33 Des 14 Cos 25 Int 18 Sag 19 Car 18\nsensi: come A.1\n```\n"
        "**Attacco** come A.1 · **Soffio acido** linea, Riflessi CD 31 · "
        "**Capacità magiche** come A.1, ma *oscurità* con raggio 24 m\n\n"
        "**Statistiche** For 33 · **Talenti** quelli di A.1\n\n"
        "**Capacità speciali**\n- **Presenza Terrificante**: Volontà CD 26.\n"
    )

    def test_il_drago_giusto_torna(self):
        self.assertEqual(C.conti_dei_recinti(self.DRAGO.format(soffio=30)), [])

    def test_la_cd_del_soffio_senza_il_talento_contato(self):
        (x,) = C.conti_dei_recinti(self.DRAGO.format(soffio=28))
        self.assertEqual((x["campo"], x["scritto"], x["atteso"]), ("CD soffio", 28, 30))

    def test_corrompere_l_acqua_ereditato_dall_adulto(self):
        # il difetto trovato dal playtester il 2026-11-03: «come A.1» porta la CD 25
        # dell'Adulto nel Vecchio, dove la presenza è CD 26
        (x,) = C.conti_dei_recinti(self.DRAGO.format(soffio=30) + self.VECCHIO)
        self.assertEqual((x["scritto"], x["atteso"]), (25, 26))
        self.assertIn("come A.1", x["campo"])

    def test_la_cd_riscritta_nella_voce_ereditata_vale(self):
        # la forma della PR #305: «come A.1, ma … *corrompere l'acqua* a CD 26»
        vecchio = self.VECCHIO.replace("con raggio 24 m", "con raggio 24 m e *corrompere l'acqua* a CD 26")
        self.assertEqual(C.conti_dei_recinti(self.DRAGO.format(soffio=30) + vecchio), [])
        sbagliata = self.VECCHIO.replace("con raggio 24 m", "con raggio 24 m e *corrompere l'acqua* a CD 25")
        (x,) = C.conti_dei_recinti(self.DRAGO.format(soffio=30) + sbagliata)
        self.assertEqual((x["campo"], x["scritto"]), ("CD corrompere l'acqua", 25))

    def test_la_prosa_che_non_torna_col_recinto(self):
        testo = self.DRAGO.format(soffio=30).replace("**CA 33**", "**CA 35**")
        (x,) = C.conti_dei_recinti(testo)
        self.assertEqual(x["campo"], "CA (prosa)")

    def test_la_scurovisione_che_manca(self):
        testo = self.DRAGO.format(soffio=30).replace("sensi: scurovisione 36 m\n", "")
        (x,) = C.conti_dei_recinti(testo)
        self.assertEqual(x["campo"], "sensi")

    #: Il cricchetto: i rilievi veri di oggi, per file, col perché. Uno in più è
    #: rosso. Le correzioni sono canone e le decide il DM : quando scendono, il tetto si abbassa a mano.
    # 2026-11-03, scelta del DM: tutti i conti all'SRD (Treant 95, scurovisione
    # di Durin e delle wyvern); Balvar 101 è giusto col primo dado al massimo dei
    # PNG con classi. 2026-11-08, F4 di ADR-0112: le schede PF1e entrano nel
    # rapporto; l'Asservito armato è passato a 35 pf con la scelta del DM
    # (mezze in su dopo il primo dado di classe).
    # 2026-11-09, ADR-0118: il rapporto conta anche l'attacco. Gorthak (+21 contro
    # +20) e Madre Dana (+18 contro +17) non tornano, nelle due copie della
    # scheda: sono nella baseline del cancello dei numeri, e li decide il DM.
    RESIDUI: dict = {}

    def test_png_con_classi_primo_dado_al_massimo(self):
        # Balvar: 13d8+39, primo dado 8 e gli altri alla media = 101 (DMG 3.5, cap. 4)
        con = ("### A.4 · X\n\n```statblocco\nnome: X\ngs: 13\ntipo: Umanoide Medio (nano), Chierico 9 / Runecaster 4\nca: 24\n"
               "pf: 101\npf-dado: 13d8+39\nts: Temp +13\nattributi: For 12\n```\n")
        senza = con.replace("Umanoide Medio (nano), Chierico 9 / Runecaster 4", "Vegetale Grande")
        conti = C.conti_dei_recinti
        self.assertEqual([x for x in conti(con) if x["campo"] == "pf"], [])
        self.assertEqual([x["atteso"] for x in conti(senza) if x["campo"] == "pf"], [97])

    def test_il_cricchetto_dei_master(self):
        r = C.rapporto_master(C.master_di_default())
        per_file = {}
        for x in r:
            per_file[Path(x["file"]).name] = per_file.get(Path(x["file"]).name, 0) + 1
        for nome, n in per_file.items():
            self.assertLessEqual(n, self.RESIDUI.get(nome, 0),
                                 f"{nome}: {n} conti che non tornano, il tetto è {self.RESIDUI.get(nome, 0)}")


class TestCancelloDeiNumeri(unittest.TestCase):
    """ADR-0118: un numero entra solo se la regola lo ricostruisce, esatto."""

    CAR = "For 31, Des 10, Cos 25, Int 16, Sag 17, Car 16"

    def test_il_morso_di_fauci(self):
        # BAB +25, For +10, Enorme −2: +33; con Arma Focalizzata (morso) +34
        self.assertEqual(C.attacco_atteso("Morso +33 in mischia (2d8+10/19-20)", 25, self.CAR, "Allerta", -2)[:2],
                         (33, 33))
        self.assertEqual(C.attacco_atteso("Morso +34 in mischia (2d8+10)", 25, self.CAR,
                                          "Arma Focalizzata (morso)", -2)[:2], (34, 34))

    def test_il_numero_gonfiato_non_torna(self):
        scritto, atteso, _ = C.attacco_atteso("Morso +37 in mischia (2d8+10)", 25, self.CAR, "Allerta", -2)
        self.assertNotEqual(scritto, atteso)

    def test_arma_magica_e_focalizzata_superiore(self):
        # Grimjaw: BAB +13, For 22 (+6), spada +1, Arma Focalizzata e Superiore: +22
        r = C.attacco_atteso("*Spada Bastarda Demoniaca +1* +22 in mischia (1d10+9)", 13, "For 22, Des 13",
                             "Arma Focalizzata (Spada Bastarda), Arma Focalizzata Superiore (Spada Bastarda)", 0)
        self.assertEqual(r[:2], (22, 22))

    def test_a_distanza_conta_la_destrezza(self):
        # Dara: BAB +11 (8+3), Des 18 (+4), arco +3, Arma Focalizzata: +19
        r = C.attacco_atteso("*Arco Lungo Composito Potente (+3) +3* +19 a distanza (1d8+6/x3)", 11,
                             "For 16, Des 18", "Arma Focalizzata (arco lungo)", 0)
        self.assertEqual(r[:2], (19, 19))

    def test_il_potenziamento_in_mezzo_al_nome(self):
        # Karkilan: «grande ascia +1 a due mani»: BAB +7, For +6, Grande −1, +1
        r = C.attacco_atteso("grande ascia +1 a due mani +13/+8 (3d6+10/x3)", 7, "For 23", "Attacco Poderoso", -1)
        self.assertEqual(r[:2], (13, 13))
        # Rurik: «martello da guerra +1 gelido»
        r = C.attacco_atteso("martello da guerra +1 gelido +14/+9 (1d8+3)", 10, "For 14",
                             "Arma Focalizzata (martello da guerra)", 0)
        self.assertEqual(r[:2], (14, 14))

    def test_l_equipaggiamento_non_e_un_attacco(self):
        """Senza `attacchi:` la voce «Altro equipaggiamento: … ascia +1 (…)» non è l'attacco della scheda."""
        testo = ("# Portalame (Fighter 6)\n\n```statblocco\ngs: 6\ntipo: Medium humanoid (goblinoid), Fighter 6, LE\n"
                 "pf: 50\nattributi: For 16 Des 16 Cos 15 Int 10 Sag 12 Car 8\nvoci:\n"
                 "  - Altro equipaggiamento: giaco di maglia +1, doppia ascia orchesca +1 (una testa perfetta)\n"
                 "  - Talenti: Arma Focalizzata (ascia) +1 (già contato)\n{attacco}```\n")
        with tempfile.TemporaryDirectory() as d:
            q = Path(d) / "portalame-cr6.md"
            q.write_text(testo.format(attacco=""), encoding="utf-8")
            self.assertEqual(C._attacco_di_scheda(LC.leggi(q)), "")
            q.write_text(testo.format(attacco="  - Morso +9 (1d6+3)\n"), encoding="utf-8")
            self.assertEqual(C._attacco_di_scheda(LC.leggi(q)), "Morso +9 (1d6+3)")

    def test_arma_focalizzata_vale_per_la_sua_arma(self):
        # Karkator: il talento è sul tentacolo, il morso non lo prende
        testo = "  - Morso +17 (2d8+9)\n  - 4 tentacoli +16 (2d6+4)\nTalenti Arma Focalizzata (tentacolo)"
        self.assertEqual(C.attacco_atteso("Morso +17 (2d8+9)", 12, "For 29", testo, -4)[:2], (17, 17))
        # il nome inglese del talento su una riga italiana vale: non c'è un'altra arma che lo porti
        testo = "  - Mischia spada lunga perfetta +9 (1d8+4)\nFeats: Weapon Focus (longsword)"
        self.assertEqual(C.attacco_atteso("spada lunga perfetta +9 (1d8+4)", 5, "For 14", testo, 0)[:2], (9, 9))

    def test_in_ira_conta_la_forza_dell_ira(self):
        # Zog'tar: BAB +15, For 36 in Ira (+13), Grande −1, ascia +1, Arma Focalizzata: +29
        testo = "For 30 (36 in Ira), Des 20 · Talenti Arma Focalizzata (ascia)"
        riga = "ascia a due mani +1 +29/+24/+19 (3d6+20, 20/×3) in Ira; +26/+21/+16 (3d6+16) fuori dall'Ira"
        self.assertEqual(C.attacco_atteso(riga, 15, "For 30 Des 20", testo, -1)[:2], (29, 29))
        self.assertEqual(C.attacco_atteso("ascia a due mani +1 +26 (3d6+16)", 15, "For 30 Des 20", testo, -1)[:2],
                         (26, 26))

    def test_addestramento_nelle_armi_pf1e_solo_se_scritto(self):
        # Skum guerriero 8: BAB +10, For +5, tridente +1, Focalizzata e Superiore, addestramento +1
        testo = ("addestramento nelle armi (lance) +1 · Talenti Arma Focalizzata (tridente), "
                 "Arma Focalizzata Superiore (tridente)")
        self.assertEqual(C.attacco_atteso("Tridente +1 +19/+14 (1d8+9)", 10, "For 21", testo, 0)[:2], (19, 19))
        senza = testo.replace("addestramento nelle armi (lance) +1 · ", "")
        self.assertEqual(C.attacco_atteso("Tridente +1 +19/+14 (1d8+9)", 10, "For 21", senza, 0)[:2], (19, 18))

    def test_perfetta_da_maestro_pf1e(self):
        r = C.attacco_atteso("pugnale da maestro +5 (1d4+1)", 3, "For 12, Des 10", "", 0)
        self.assertEqual(r[:2], (5, 5))

    UNITA = ("### **OROG GUARDIE NERE**\n\n> Uno contro uno: `Bestiario/mostri/orog-guardia-nera-guerriero6-cr7.md`\n\n"
             "**AU (Ascia Bipenne+1):** +{au} | **Danno:** 1d12+7\n\n---\n"
             "### **FANTERIA SENZA SCHEDA**\n\n**AU (Spada):** +10 | **Danno:** 1d8\n")

    def test_l_au_e_l_attacco_della_creatura_singola(self):
        # orog: ascia +14 nella scheda uno contro uno (+13 fino al 2026-11-20), quindi AU +14 (ARC08-02 §4).
        # Il «+2 effetto massa» è della variante 2d6: +16 non torna.
        r = C.numeri_delle_unita(ROOT / "prova.md", self.UNITA.format(au=14))
        self.assertEqual([x["titolo"] for x in r], ["FANTERIA SENZA SCHEDA"])
        r = C.numeri_delle_unita(ROOT / "prova.md", self.UNITA.format(au=16))
        orog = [x for x in r if x["titolo"] == "OROG GUARDIE NERE"]
        self.assertEqual((orog[0]["scritto"], orog[0]["atteso"]), (16, 14))

    def test_l_unita_senza_scheda_non_ha_conto(self):
        r = C.numeri_delle_unita(ROOT / "prova.md", self.UNITA.format(au=14))
        self.assertIsNone(r[0]["atteso"])

    def test_la_balista_toglie_quattro_a_chi_e_medio(self):
        # SRD 3.5, Siege Engines: -4 a una creatura Media, -6 a una Piccola, niente a una Grande
        f = C.attacco_atteso
        riga, tal = "Distanza balista pesante perfetta +10 (3d8+2/19-20)", "Arma Focalizzata (balista), Arma Focalizzata Superiore (balista)"
        self.assertEqual(f(riga, 8, "For 13 Des 17", tal, 0)[:2], (10, 10))
        self.assertEqual(f(riga, 8, "For 13 Des 17", tal, 1)[1], 9)      # Piccola: +1 di taglia, -6
        self.assertEqual(f(riga, 8, "For 13 Des 17", tal, -1)[1], 13)    # Grande: -1 di taglia, niente penalità
        # l'ingegnere Esperto 4 che la punta da solo arriva a +3, non a +10
        self.assertEqual(f("Distanza balista pesante perfetta +10 (3d8)", 3, "For 12 Des 14", "Arma Focalizzata (balista)", 0)[1], 3)

    SINGOLA = ("#### **GIGANTI DELLE COLLINE (8 creature)**\n```\nSTATISTICHE UNITÀ (1 Gigante per unità):\n"
               "- Attacco Unità: +{au} (Randello, 2d8+12)\n---\nSTATISTICHE CREATURA SINGOLA (Gigante delle Colline):\n"
               "CM Gigante Grande; \nAttacco Base +{bab}, \nAtt Randello enorme +{att} (2d8+12); \n"
               "Att a distanza Lancio massi +8 (2d6+8); \nFor 27, Des 8, Cos 19, Int 6, Sag 10, Car 7.\n```\n")

    def test_la_creatura_singola_di_una_guida(self):
        # gigante delle colline: BAB +9, For 27 (+8), Grande −1: randello +16, e l'AU è +16
        f = C.numeri_delle_singole
        self.assertEqual(f(ROOT / "prova.md", self.SINGOLA.format(au=16, bab=9, att=16)), [])
        r = f(ROOT / "prova.md", self.SINGOLA.format(au=14, bab=8, att=14))
        self.assertEqual([(x["campo"], x["scritto"], x["atteso"]) for x in r], [("attacco", 14, 15)])
        r = f(ROOT / "prova.md", self.SINGOLA.format(au=18, bab=9, att=16))
        self.assertEqual([(x["campo"], x["scritto"], x["atteso"]) for x in r], [("AU", 18, 16)])
        # l'etichetta sceglie l'attacco: i massi sono +8
        self.assertEqual(C._attacco_della_singola(next(C._singole(self.SINGOLA.format(au=16, bab=9, att=16)))[4],
                                                  "Lancio Massi")[:2], (8, 8))

    def test_il_cancello_sul_repo_e_verde(self):
        self.assertEqual(C.cancello_numeri(), 0)


class TestIFileGeneratiRestanoFuori(unittest.TestCase):
    def test_le_cartelle_di_gitignore_restano_fuori(self):
        # Nei thread l'avvio costruisce le skill in build/ (ignorata da git):
        # 112 copie di SKILL.md facevano rosso il cancello sul repo, 2026-11-19.
        import subprocess
        radice = Path(tempfile.mkdtemp())
        subprocess.run(["git", "init", "-q", str(radice)], check=True)
        (radice / ".gitignore").write_text("build/\n", encoding="utf-8")
        (radice / "build").mkdir()
        (radice / "build" / "copia.md").write_text("x", encoding="utf-8")
        (radice / "nuovo.md").write_text("x", encoding="utf-8")
        (radice / "tracciato.md").write_text("x", encoding="utf-8")
        subprocess.run(["git", "-C", str(radice), "add", "tracciato.md"], check=True)
        trovati = [q.relative_to(radice).as_posix() for q in C.md_del_repo(radice)]
        self.assertEqual(trovati, ["nuovo.md", "tracciato.md"])

    def test_memoria_non_e_un_file_di_schede(self):
        # MEMORIA.md ripete le ultime righe di plans/CHANGELOG.md: una riga che nomina
        # il BAB lo faceva entrare tra i «file con numeri che nessun conto legge»
        self.assertIn("MEMORIA.md", C.FUORI_DAI_NUMERI)
        _, scoperti = C.numeri_dei_file()
        self.assertNotIn("MEMORIA.md", scoperti)
