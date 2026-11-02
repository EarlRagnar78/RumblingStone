"""domande_developer: ogni regola morde, e il cancello del repo è verde.

Come per copertura_scene: un caso che deve far scattare la regola e uno che
deve lasciarla zitta. I casi del mondo vero stanno nella calibrazione
(`plans/esperimenti/domande-developer-def4/`).
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import domande_developer as dd  # noqa: E402

#: In una scena a parte, perché la sua CD non risponda per la scena sotto esame.
TUTTI_I_TS = "\n\n### SCENA 99 — I tiri\n\nTempra CD 15, Riflessi CD 15, Volontà CD 15.\n"


def regole(testo, profilo=None):
    return [(r, s) for r, s, _ in dd.analizza(testo + TUTTI_I_TS, profilo)]


class TestD2D4IlLuogoSorvegliato(unittest.TestCase):

    CAMPO = "### SCENA 1 — Il campo\n\nQuattro guardie di ronda e una pattuglia di lupi.\n"

    def test_senza_risposte_scattano_tutte_e_tre(self):
        r = [x[0] for x in regole(self.CAMPO)]
        self.assertEqual(r.count("D2"), 3)
        self.assertIn("D4", r)

    def test_con_le_risposte_tace(self):
        testo = self.CAMPO + ("Se volano, i lupi fiutano a 9 m. Chi è invisibile passa, ma "
                              "l'allarme arriva in 2 round. Col silenzio, li sente solo il lupo.\n")
        self.assertEqual(regole(testo), [])

    def test_sentinella_maiuscola_e_un_nome(self):
        testo = "### SCENA 1 — Il tempio\n\nLa Sentinella di Mithral. La Sentinella si sveglia.\n"
        self.assertEqual(regole(testo), [])


class TestD1IlNemicoInVolo(unittest.TestCase):

    DRAGO = "### SCENA 1 — Il duello\n\nSkullcrusher, GS 12, resta in volo sopra le mura.\n"

    def test_niente_per_chi_resta_a_terra(self):
        self.assertIn(("D1", "SCENA 1"), regole(self.DRAGO))

    def test_a_terra_nella_descrizione_non_basta(self):
        testo = self.DRAGO + "Dove atterra, la pietra fuma a terra.\n"
        self.assertIn(("D1", "SCENA 1"), regole(testo))

    def test_la_risposta_scritta_tace(self):
        testo = self.DRAGO + "Chi non vola può tirare le catene degli arpioni.\n"
        self.assertNotIn(("D1", "SCENA 1"), regole(testo))


class TestD3ITreTiriSalvezza(unittest.TestCase):

    def test_manca_riflessi(self):
        fuori = dd.analizza("### SCENA 1 — X\n\nTempra CD 15. Volontà CD 18.\n")
        self.assertEqual([d for r, _, d in fuori if r == "D3"], ["nessun effetto chiede un TS su Riflessi"])

    def test_il_modulo_di_rito_dichiara_i_suoi(self):
        fuori = dd.analizza("### SCENA 1 — X\n\nVolontà CD 18.\n", {"ts_voluti": ["Volontà"]})
        self.assertEqual([r for r, _, _ in fuori if r == "D3"], [])


class TestD5IlBoss(unittest.TestCase):

    def test_boss_senza_soglia(self):
        testo = "## §8 — BOSS: Terros\n\nTerros attacca ogni round con il pugno.\n"
        self.assertIn(("D5", "§8 — BOSS: Terros"), regole(testo, {"scena": r"^## §\d+"}))

    def test_boss_con_soglia(self):
        testo = "## §8 — BOSS: Terros\n\nA 80 pf esita, e da lì cambia tattica.\n"
        self.assertNotIn("D5", [r for r, _ in regole(testo, {"scena": r"^## §\d+"})])

    def test_boss_dichiarato_da_una_tabella(self):
        testo = ("### SCENA 11 — Il duello\n\nIl drago colpisce.\n\n### SCENA 12 — Dopo\n\nx\n\n"
                 "| Scena 11: Skullcrusher (GS 12) | boss | 2.700 |\n")
        self.assertIn(("D5", "SCENA 11"), regole(testo))


class TestD6LoSkillChallenge(unittest.TestCase):

    def test_mezzo_scritto(self):
        testo = "### SCENA 1 — Il guado\n\n#### Skill challenge\n\nSi attraversa il fiume.\n"
        det = [d for r, _, d in dd.analizza(testo + TUTTI_I_TS) if r == "D6"]
        self.assertTrue(det and "quanti successi" in det[0] and "cosa si tira" in det[0])

    def test_scritto_per_intero(self):
        testo = ("### SCENA 1 — Il guado\n\n**6 successi prima di 3 fallimenti.** Ogni PG contribuisce: "
                 "Nuotare CD 15. Ogni successo avvicina la riva; ogni fallimento costa 1d6 danni.\n")
        self.assertNotIn("D6", [r for r, _ in regole(testo)])

    def test_numeri_diversi_in_due_punti(self):
        testo = ("### SCENA 1 — Il guado\n\n6 successi prima di 3 fallimenti. Ogni PG: Nuotare CD 15; "
                 "ogni successo avvicina; un fallimento costa.\n\n## Quick reference\n\n"
                 "Guado: 5 successi / 3 fallimenti\n")
        self.assertIn(("D6", "—"), regole(testo))

    def test_abilita_5e_in_35(self):
        self.assertIn("D6-5E", [r for r, _ in regole("Furtività CD 15 per entrare.")])

    def test_percezione_esiste_in_pf1e(self):
        self.assertNotIn("D6-5E", [r for r, _ in regole("Percezione CD 15.", {"sistema": "pf1e"})])
        self.assertIn("D6-5E", [r for r, _ in regole("Atletica CD 15.", {"sistema": "pf1e"})])

    def test_percezione_tremorica_non_e_un_abilita(self):
        self.assertNotIn("D6-5E", [r for r, _ in regole("Percezione tremorica 18 m.")])


class TestIlRepo(unittest.TestCase):

    def test_il_cancello_e_verde(self):
        self.assertEqual(dd.main(["--check"]), 0)

    def test_ogni_residuo_ha_la_ragione(self):
        for r in dd.carica_config()["residui"]:
            self.assertTrue(r.get("ragione"), r)

    def test_il_difetto_di_def4_e_chiuso_nel_testo(self):
        """Il playtester #42 (Tordek contro il drago in quota) era aperto fino al
        2026-09-27: la Scena 11 adesso dice cosa fa chi non vola, e nessun
        residuo deve più coprirlo."""
        master = ROOT / "07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md"
        rilievi = dd.analizza(master.read_text(encoding="utf-8"))
        self.assertNotIn(("D1", "SCENA 11"), [(r, s) for r, s, _ in rilievi])
        self.assertFalse([x for x in dd.carica_config()["residui"]
                          if x["regola"] == "D1" and x["scena"] == "SCENA 11"])


if __name__ == "__main__":
    unittest.main()


class TestD9IlSegretoELaDivinazione(unittest.TestCase):

    SEGRETI = ("### SCENA 1 — La locanda\n\nIl segreto di Varis è nel registro.\n\n"
               "### SCENA 2 — Il tempio\n\n#### Nodo d'indizio — la lapide\n")

    def test_al_tredicesimo_senza_blocco_scatta(self):
        self.assertIn(("D9", "—"), regole(self.SEGRETI))

    def test_il_blocco_in_forma_fissa_tace(self):
        testo = self.SEGRETI + "\n**Se lo divinano** — *comunione* dice il nome del mandante.\n"
        self.assertNotIn(("D9", "—"), regole(testo))

    def test_sotto_il_nono_livello_tace(self):
        self.assertNotIn(("D9", "—"), regole(self.SEGRETI, {"apl": 5}))

    def test_un_segreto_solo_non_basta(self):
        testo = "### SCENA 1 — La locanda\n\nIl segreto di Varis è nel registro.\n"
        self.assertNotIn(("D9", "—"), regole(testo))


class TestD10LaRigaDiScala(unittest.TestCase):

    SCONTRO = "### SCENA 1 — Le mura\n\nZog'tar e quattro guardie, EL 14.\n"

    def test_scontro_senza_scala_scatta(self):
        self.assertIn(("D10", "SCENA 1"), regole(self.SCONTRO))

    def test_con_la_riga_tace(self):
        testo = self.SCONTRO + "Con tre PG manca il sergente, che resta al corno.\n"
        self.assertNotIn(("D10", "SCENA 1"), regole(testo))


class TestD15LOrdaDiGsBasso(unittest.TestCase):

    ORDA = "### SCENA 1 — Il guado\n\nDodici hobgoblin guerrieri, EL 12.\n"

    def test_orda_senza_risposta_scatta(self):
        self.assertIn(("D15", "SCENA 1"), regole(self.ORDA))

    def test_le_ondate_tacciono(self):
        testo = self.ORDA + "Arrivano in tre ondate di quattro, a 30 m l'una dall'altra.\n"
        self.assertNotIn(("D15", "SCENA 1"), regole(testo))

    def test_sotto_il_nono_livello_tace(self):
        self.assertNotIn(("D15", "SCENA 1"), regole(self.ORDA, {"apl": 4}))


class TestD16IlPgFuoriGioco(unittest.TestCase):

    STREGA = "### SCENA 1 — La torre\n\nLa strega, GS 13, lancia *dominare persone* sul guerriero.\n"

    def test_senza_uscita_scatta(self):
        self.assertIn(("D16", "SCENA 1"), regole(self.STREGA))

    def test_il_nuovo_ts_tace(self):
        testo = self.STREGA + "Ogni ordine contrario alla sua natura concede un nuovo TS.\n"
        self.assertNotIn(("D16", "SCENA 1"), regole(testo))

    def test_stordito_non_conta(self):
        testo = "### SCENA 1 — La torre\n\nIl gigante, GS 13: chi è colpito resta stordito.\n"
        self.assertNotIn(("D16", "SCENA 1"), regole(testo))


class TestD18LaDomandaDellaScena(unittest.TestCase):

    SCONTRO = "### SCENA 1 — Il pilastro\n\nGli Xorn, EL 13. Con tre PG manca il terzo Xorn.\n"

    def test_scontro_senza_domanda_scatta(self):
        self.assertIn(("D18", "SCENA 1"), regole(self.SCONTRO))

    def test_la_riga_in_forma_fissa_tace(self):
        testo = self.SCONTRO + "\n**Domanda:** gli Xorn lasciano passare il gruppo col mithral?\n"
        self.assertNotIn(("D18", "SCENA 1"), regole(testo))

    def test_la_posta_senza_punto_di_domanda_non_basta(self):
        testo = self.SCONTRO + "\n**Posta in gioco:** il mithral del gruppo.\n"
        self.assertIn(("D18", "SCENA 1"), regole(testo))

    def test_la_scena_sociale_conta(self):
        testo = "### SCENA 1 — Il mercante\n\nDiplomazia CD 15 per lo sconto.\n"
        self.assertIn(("D18", "SCENA 1"), regole(testo))

    def test_la_scena_raccontata_tace(self):
        testo = "### SCENA 1 — Il viaggio\n\nTre giorni di marcia fra i pini.\n"
        self.assertNotIn(("D18", "SCENA 1"), regole(testo))


class TestD19LaSceltaCheSiVede(unittest.TestCase):

    def test_scelta_senza_conseguenza_scatta(self):
        testo = ("### SCENA 1 — La gemma\n\n- **Se Tordek la tocca**, la voce arriva a lui.\n"
                 "- **Se la distruggono**, la voce tace.\n")
        self.assertIn(("D19", "SCENA 1"), regole(testo))

    def test_il_rimando_a_una_scena_tace(self):
        testo = ("### SCENA 1 — La targa\n\n- **Se prendono il Nome** → il re li riconosce "
                 "nella Scena 4.\n- **Se non lo prendono**, non perdono niente.\n")
        self.assertNotIn(("D19", "SCENA 1"), regole(testo))

    def test_le_opzioni_contano(self):
        testo = "### SCENA 1 — Il rito\n\n- **Opzione A — l'oro**: pagano.\n- **Opzione B — il corpo**: soffre.\n"
        self.assertIn(("D19", "SCENA 1"), regole(testo))

    def test_una_condizione_del_mondo_non_e_una_scelta(self):
        testo = "### SCENA 1 — Il corno\n\n- **Se il corno suona di notte**, il drago arriva.\n"
        self.assertNotIn(("D19", "SCENA 1"), regole(testo))

    def test_nello_scontro_il_se_tattico_tace(self):
        testo = ("### SCENA 1 — Terros\n\nTerros, GS 15. Con tre PG perde un'azione.\n\n"
                 "**Se Artemis vola invisibile**, Terros la sente con Ascoltare.\n")
        self.assertNotIn(("D19", "SCENA 1"), regole(testo))

    def test_il_titolo_vale_fino_al_titolo_dopo(self):
        testo = ("### SCENA 1 — La caverna\n\n#### Se i PG…\n\n| Fanno | Succede |\n|---|---|\n"
                 "| chiudono la porta | gli orchi tornano all'alba, carry-over |\n")
        self.assertNotIn(("D19", "SCENA 1"), regole(testo))


class TestD20IlPresagioDelBoss(unittest.TestCase):

    def _modulo(self, prima):
        return (prima + "### SCENA 9 — BOSS: Skullcrusher\n\nA metà dei pf esita e fugge.\n")

    def test_boss_senza_presagio_scatta(self):
        testo = self._modulo("### SCENA 1 — Il bosco\n\nNebbia.\n\n### SCENA 2 — Le mura\n\nPietra.\n\n")
        self.assertIn(("D20", "SCENA 9"), regole(testo))

    def test_due_scene_che_lo_nominano_tacciono(self):
        testo = self._modulo("### SCENA 1 — Il bosco\n\nDurin parla di Skullcrusher.\n\n"
                             "### SCENA 2 — Le mura\n\nLe ossa che ha lasciato Skullcrusher.\n\n")
        self.assertNotIn(("D20", "SCENA 9"), regole(testo))

    def test_l_indizio_senza_nome_si_dichiara_nel_profilo(self):
        testo = self._modulo("### SCENA 1 — Il bosco\n\nUn'ombra: il drago passa.\n\n"
                             "### SCENA 2 — Le mura\n\nIl drago brucia una torre.\n\n")
        self.assertIn(("D20", "SCENA 9"), regole(testo))
        self.assertNotIn(("D20", "SCENA 9"), regole(testo, {"presagi": {"SCENA 9": ["drago"]}}))


    def test_d20_e_un_indicatore_e_non_blocca(self):
        """Lotto 7e (2026-10-22): D20 non calibrata (0 veri su 2) resta fuori da
        --check. Un suo rilievo non dichiarato si stampa e non fa rosso."""
        from unittest import mock
        self.assertIn("D20", dd.INDICATORI)
        modulo = {"file": "finto.md"}
        with mock.patch.object(dd.cs, "moduli", return_value=[modulo]), \
                mock.patch.object(dd.cs, "carica_config", return_value={}), \
                mock.patch.object(Path, "exists", return_value=True), \
                mock.patch.object(Path, "read_text", return_value="x"), \
                mock.patch.object(dd, "analizza",
                                  return_value=[("D20", "SCENA 9", "boss senza presagio"),
                                                ("D10", "SCENA 2", "senza scala")]):
            trovati, nuovi, scaduti = dd.esegui({"residui": []})
        self.assertEqual(len(trovati), 2)
        self.assertEqual([t[1] for t in nuovi], ["D10"])
        self.assertEqual(scaduti, [])

class TestD21LaReteDegliIndizi(unittest.TestCase):

    CONCLUSIONE = "<!-- conclusione C1: la profezia parla dei PG -->\n\n"

    def test_senza_marcatura_tace(self):
        testo = "### SCENA 1 — La targa\n\nUn indizio, e un nodo d'indizio.\n"
        self.assertNotIn("D21", [r for r, _ in regole(testo)])

    def test_tre_indizi_da_tre_scene_tacciono(self):
        testo = self.CONCLUSIONE + "".join(
            f"### SCENA {n} — X\n\nIndizio. <!-- indizio C1 -->\n\n" for n in (1, 2, 3))
        self.assertNotIn("D21", [r for r, _ in regole(testo)])

    def test_tre_indizi_in_un_nodo_solo_scattano(self):
        testo = self.CONCLUSIONE + "### SCENA 1 — X\n\n" + "Uno. <!-- indizio C1 -->\n" * 3
        det = [d for r, _, d in dd.analizza(testo + TUTTI_I_TS) if r == "D21"]
        self.assertTrue(det and "3 indizi da 1 nodi" in det[0])

    def test_due_nodi_nella_stessa_scena_contano(self):
        testo = (self.CONCLUSIONE + "### SCENA 1 — X\n\n#### 🔍 Nodo d'indizio — la targa\n\n"
                 "<!-- indizio C1 --> <!-- indizio C1 -->\n\n#### 🔍 Nodo d'indizio — il re\n\n"
                 "<!-- indizio C1 -->\n")
        self.assertNotIn("D21", [r for r, _ in regole(testo)])

    def test_un_indizio_senza_conclusione_scatta(self):
        testo = "### SCENA 1 — X\n\n<!-- indizio C7 -->\n"
        self.assertIn(("D21", "—"), regole(testo))
