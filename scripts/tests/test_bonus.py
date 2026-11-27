"""dmcore.bonus — cumulo dei bonus per tipo (ADR-0126, lotto 1)."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import bonus as B  # noqa: E402
from dmcore import lettura_creatura as L  # noqa: E402
import conformita_statblocchi as C  # noqa: E402

V = B.Voce


class TestSomma(unittest.TestCase):
    def test_stesso_tipo_vale_il_piu_alto(self):
        tot, contate, scartate = B.somma([V(1, "resistenza", "a"), V(3, "resistenza", "b")])
        assert tot == 3 and [v.sorgente for v in contate] == ["b"] and len(scartate) == 1

    def test_tipi_diversi_si_sommano(self):
        assert B.somma([V(2, "resistenza", "a"), V(1, "fortuna", "b"), V(2, "sacro", "c")])[0] == 5

    def test_senza_tipo_schivare_circostanza_razziale_si_sommano(self):
        for tipo in ("senza_tipo", "schivare", "circostanza", "razziale"):
            assert B.somma([V(2, tipo, "a"), V(2, tipo, "b")])[0] == 4, tipo

    def test_l_ordine_non_cambia_il_totale(self):
        voci = [V(1, "fortuna", "a"), V(2, "resistenza", "b"), V(1, "resistenza", "c"),
                V(2, "senza_tipo", "d")]
        assert B.somma(voci) == B.somma(voci) and B.somma(voci)[0] == B.somma(voci[::-1])[0] == 5


class TestDichiarati(unittest.TestCase):
    def test_mantello_e_talento(self):
        t = B.totali("Equipaggiamento mantello della resistenza +2 · Talenti Volontà di Ferro")
        assert t == {"Temp": 2, "Rifl": 2, "Vol": 4}

    def test_due_resistenze_non_si_sommano(self):
        t = B.totali("mantello della resistenza +1, veste dell'arcimago")
        assert t == {"Temp": 4, "Rifl": 4, "Vol": 4}

    def test_fortuna_e_resistenza_si_sommano(self):
        assert B.totali("cloak of resistance +1, luckstone")["Vol"] == 2

    def test_dichiarazione_esplicita_nella_riga_dei_ts(self):
        t = B.totali("TS Temp +5, Rifl +3, Vol +6 (+1 fortuna a tutti; +2 sacro alla Volontà)")
        assert t == {"Temp": 1, "Rifl": 1, "Vol": 3}

    def test_il_bonus_a_condizione_non_entra(self):
        riga = "TS Temp +5, Rifl +3, Vol +6 (+2 razziale vs incantesimi, +2 morale contro la paura)"
        assert B.totali(riga) == {}

    def test_la_dichiarazione_fuori_dalla_riga_dei_ts_non_entra(self):
        assert B.totali("Attacco: ascia +9 (+1 fortuna a tutti)") == {}

    def test_esplicita_e_oggetto_dello_stesso_tipo_non_raddoppiano(self):
        riga = ("TS Temp +5, Rifl +3, Vol +6 (+1 resistenza a tutti dal mantello)\n"
                "Equipaggiamento mantello della resistenza +1")
        assert B.totali(riga) == {"Temp": 1, "Rifl": 1, "Vol": 1}

    def test_halfling_solo_nella_riga_del_tipo(self):
        assert B.totali("tipo: Small humanoid (halfling), Rogue 3")["Rifl"] == 1
        assert B.totali("Odia gli halfling del porto.") == {}

    def test_ogni_sorgente_ha_fonte_e_tipo_noto(self):
        r = B.regole()
        tipi = set(r["tipi"].values())
        for s in r["sorgenti"]:
            assert s["fonte"] and s["tipo"] in tipi and s["campi"], s["nome"]


class TestLettore(unittest.TestCase):
    def test_talenti_tiene_iniziativa_e_ignora_le_note(self):
        testo = "Talenti Iniziativa Migliorata\n> mantello della resistenza +5 (nota)"
        assert L.talenti(testo) == {"init": 4}


class TestSevero(unittest.TestCase):
    def _scheda(self, ts, extra=""):
        testo = ("```statblocco\nnome: Prova\ngs: 3\ntipo: Medium humanoid (human), Fighter 3, LN\n"
                 "pf: 25\n" f"ts: {ts}\n"
                 "attributi: For 14 Des 12 Cos 12 Int 10 Sag 10 Car 10\n```\n" + extra)
        return L.leggi_testo(testo, ROOT / "Bestiario" / "prova-cr3.md")

    def test_un_punto_in_piu_senza_dichiarazione_e_uno_scarto(self):
        s = self._scheda("Temp +4, Rifl +2, Vol +2")
        assert C.scarti(C.verifica(s, severo=True)).keys() == {"Vol"}
        assert not C.scarti(C.verifica(s))

    def test_lo_stesso_punto_dichiarato_torna(self):
        s = self._scheda("Temp +5, Rifl +3, Vol +2", "Equipaggiamento mantello della resistenza +1\n")
        assert not C.scarti(C.verifica(s, severo=True))

    def test_tiri_salvezza_condivisi_non_si_giudicano_verso_l_alto(self):
        s = self._scheda("Temp +9, Rifl +2, Vol +1", "Capacità speciali condividere tiri salvezza\n")
        assert not C.scarti(C.verifica(s, severo=True))


class TestAttaccoSevero(unittest.TestCase):
    def _scheda(self, mischia, talenti_):
        testo = ("```statblocco\nnome: Prova\ngs: 8\ntipo: Medium humanoid (dwarf), Fighter 8, LG\n"
                 "pf: 60\nts: Temp +8, Rifl +3, Vol +2\n"
                 "attributi: For 16 Des 12 Cos 14 Int 10 Sag 10 Car 10\nbab: +8\n"
                 f"attacchi:\n  - Mischia {mischia}\n  - Distanza balista +9 (3d8)\n```\n**Talenti** {talenti_}\n")
        return L.leggi_testo(testo, ROOT / "Bestiario" / "prova-cr8.md")

    def test_potenziamento_in_mezzo_al_nome_e_focalizzata_superiore(self):
        s = self._scheda("martello da guerra +1 gelido +14/+9 (1d8+4)",
                         "Arma Focalizzata (martello da guerra), Arma Focalizzata Superiore (martello da guerra)")
        self.assertNotIn("attacco", C.scarti(C.verifica(s, severo=True)))

    def test_focalizzata_su_un_altra_arma_non_conta(self):
        s = self._scheda("ascia da battaglia perfetta +12/+7 (1d8+3)", "Arma Focalizzata (balista)")
        self.assertNotIn("attacco", C.scarti(C.verifica(s, severo=True)))
        s = self._scheda("ascia da battaglia perfetta +13/+8 (1d8+3)", "Arma Focalizzata (balista)")
        self.assertIn("attacco", C.scarti(C.verifica(s, severo=True)))
