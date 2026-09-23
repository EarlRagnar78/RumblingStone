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
import genera_attributi as GA  # noqa: E402


def scheda(corpo: str, prosa: str = "", titolo: str = "# Prova") -> C.Scheda:
    """Una scheda finta su disco, letta dal lettore vero."""
    d = Path(tempfile.mkdtemp())
    p = d / "prova-cr3.md"
    p.write_text(f"{titolo}\n\n```statblocco\n{corpo}\n```\n\n{prosa}\n", encoding="utf-8")
    return C.leggi(p)


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
        self.assertEqual(C.dv_totali(t), 7)

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
        self.assertTrue(C.LOTTA_MIGLIORATA.search("Talenti: Lottare Migliorato"))


class TestIlTemplateSpiegaLoScarto(unittest.TestCase):
    def test_advanced_su_caratteristiche_non_potenziate(self):
        # pf, TS e lotta con +4 a tutto, caratteristiche della base: e' un Advanced
        s = scheda("gs: 4\ntipo: Large giant, 4 HD\nca: 18\npf: 34\npf-dado: 4d8+16\n"
                   "ts: Temp +8, Rifl +2, Vol +3\nattributi: For 21 Des 8 Cos 15 Int 6 Sag 10 Car 7",
                   "**hp 34** (4 HD). BAB +3; Lotta +14.")
        g = C.giudica(s)
        self.assertTrue(g["scarti"])
        self.assertEqual(g["template"], "Advanced")


class TestPfDado(unittest.TestCase):
    def test_la_formula_scritta_vince(self):
        t = "pf-dado: 4d8\n**DV 4d8 + 6d12**. **hp 77**"
        self.assertEqual(GA.dadi_vita(t)[0], [(4, 8), (6, 12)])
        self.assertIn("formula scritta", GA.pf_dado_sospetto(t, 9))

    def test_robustezza_e_robustezza_migliorata_non_sono_lo_stesso_talento(self):
        self.assertEqual(GA.robustezza("Talenti: Robustezza", 5), 3)
        self.assertEqual(GA.robustezza("Talenti: Robustezza Migliorata", 5), 5)
        self.assertEqual(GA.robustezza("Talenti: Robustezza, Robustezza Migliorata", 5), 8)

    def test_il_gs_si_legge_se_non_lo_passano(self):
        # `1d8+2` per un chierico di 3° passava per dadi vita a chi non dava il GS
        self.assertIsNotNone(GA.pf_dado_sospetto("gs: 4\npf-dado: 1d8+2\n"))

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
        self.assertIn("goblin-warrior1-cr05.md", C.decisioni_aperte())


if __name__ == "__main__":
    unittest.main()
