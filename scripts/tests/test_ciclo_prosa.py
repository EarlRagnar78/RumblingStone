"""Test di ciclo_prosa.py (L12 di PIANO-AGENT-SKILLS-ESTERNE, ADR-0077)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import ciclo_prosa as cp  # noqa: E402

BOX = (
    "> **Read-aloud (LotR lead).** *Entrate nella sala. Un altare di basalto\n"
    "> sta al centro, e ti è sembrato più grande da fuori.*\n"
)


_REGISTRO_TMP = tempfile.TemporaryDirectory()
_PATCH_REGISTRO = mock.patch.object(cp, "REGISTRO", Path(_REGISTRO_TMP.name) / "miglioramenti.json")


def setUpModule():
    # applica() scrive nel registro dei miglioramenti: nei test mai quello vero
    _PATCH_REGISTRO.start()


def tearDownModule():
    _PATCH_REGISTRO.stop()
    _REGISTRO_TMP.cleanup()


def _norme(testo):
    return sorted(s.norma for s in cp.segnala(testo))


class TestSegnala(unittest.TestCase):
    def test_p1_e_sembra_sulla_loro_riga(self):
        seg = {s.norma: s for s in cp.segnala(BOX)}
        self.assertEqual(seg["P1"].riga, 1)
        self.assertEqual(seg["sembra/pare"].riga, 2)

    def test_un_tic_minore_da_solo_non_conta(self):
        # Humanizer, «weak alone»: un «nel cuore di» è italiano corretto.
        self.assertNotIn("tic minori in gruppo", _norme("Nel cuore della notte il campo dorme.\n"))

    def test_due_tic_minori_diversi_si(self):
        testo = "La forgia rappresenta il patto. Non è un muro: è una porta.\n\nNon è un dono: è un debito.\n"
        self.assertIn("tic minori in gruppo", _norme(testo))

    def test_un_antitesi_sola_nel_documento_non_e_un_tic(self):
        # La soglia di validate_prosa: piu' di una per documento.
        testo = "La forgia rappresenta il patto. Non è un muro: è una porta.\n"
        self.assertNotIn("tic minori in gruppo", _norme(testo))

    def test_il_trattino_conta_oltre_il_tre_per_cento(self):
        rado = "La forgia rappresenta il patto " + "e la pietra " * 20 + "— e resta."
        self.assertEqual(cp.tic_deboli(rado), ["copula elusa"])
        self.assertEqual(cp.tic_deboli("La forgia rappresenta — il patto."),
                         ["copula elusa", "trattino come respiro"])

    def test_lo_stesso_trattino_non_conta_due_volte(self):
        # «Non è X — è Y» è un'antitesi, non un'antitesi più un trattino.
        self.assertEqual(cp.tic_deboli("Non è una porta — è un muro."), ["antitesi"])

    def test_un_elenco_sono_voci_separate(self):
        righe = ["- La forgia rappresenta il patto.", "- Un vero e proprio muro."]
        self.assertEqual(cp._paragrafi(righe), [(0, 0), (1, 1)])

    def test_i_pg_non_sono_nomi_nuovi(self):
        box = "> *Thorik e Hella guardano l'altare.*\n"
        self.assertNotIn("box con più nomi propri", _norme(box))

    def test_l_etichetta_non_porta_trattini(self):
        self.assertEqual(cp._paragrafi(["**Read-aloud (X) — la sala.**"]), [(0, 0)])
        self.assertEqual(_norme("> **Read-aloud (X) — la sala.** *Non è una sala: è una tomba.*\n"), [])


class TestRevisione(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.orig, self.risc = d / "orig.md", d / "risc.md"
        self.orig.write_text("Prima riga.\n\n" + BOX + "\nCD 15 per aprire.\n", encoding="utf-8")
        self.risc.write_text("Prima riga.\n\n" + BOX.replace(
            "Entrate nella sala. ", "").replace("e ti è sembrato più grande da fuori", "e il fumo lo copre")
            + "\nCD 15 per aprire.\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_le_modifiche_vicine_sono_una(self):
        prima, dopo = self.orig.read_text(), self.risc.read_text()
        mods, marcato = cp._modifiche(prima, dopo, cp.segnala(prima))
        self.assertEqual(len(mods), 2)
        self.assertIn("{~~", marcato)
        self.assertIn("{>>#1<<}", marcato)

    def test_ogni_modifica_porta_la_sua_norma(self):
        prima, dopo = self.orig.read_text(), self.risc.read_text()
        mods, _ = cp._modifiche(prima, dopo, cp.segnala(prima))
        self.assertEqual([m.norme for m in mods], [["P1"], ["sembra/pare"]])

    def test_un_numero_cambiato_boccia_la_revisione(self):
        self.risc.write_text(self.risc.read_text().replace("CD 15", "CD 18"))
        testo, ok = cp.revisione(self.orig, self.risc)
        self.assertFalse(ok)
        self.assertIn("Nessun fatto cambia** (nomi propri, numeri, CD): NO", testo)

    def test_la_revisione_buona_passa(self):
        testo, ok = cp.revisione(self.orig, self.risc)
        self.assertTrue(ok)
        self.assertIn("| [ ] | 1 |", testo)

    def _revisione_su_disco(self, spunta):
        testo, _ = cp.revisione(self.orig, self.risc)
        for n in spunta:
            testo = testo.replace(f"| [ ] | {n} |", f"| [x] | {n} |")
        rev = Path(self.tmp.name) / "REVISIONE.md"
        rev.write_text(testo, encoding="utf-8")
        return rev

    def test_applica_solo_le_spuntate(self):
        rev = self._revisione_su_disco([1])
        with mock.patch.object(cp, "_ramo", return_value="claude/prova"):
            self.assertEqual(cp.applica(rev, "2026-10-02"), 0)
        nuovo = self.orig.read_text()
        self.assertTrue(nuovo.startswith("<!-- revisione-testo: r1 · 2026-10-02 -->"))
        self.assertNotIn("Entrate", nuovo)
        self.assertIn("sembrato", nuovo)          # la 2 non era spuntata

    def test_non_si_applica_su_main(self):
        rev = self._revisione_su_disco([1, 2])
        with mock.patch.object(cp, "_ramo", return_value="main"):
            self.assertEqual(cp.applica(rev, "2026-10-02"), 1)
        self.assertIn("Entrate", self.orig.read_text())

    def test_non_si_applica_due_volte(self):
        rev = self._revisione_su_disco([1])
        with mock.patch.object(cp, "_ramo", return_value="claude/prova"):
            self.assertEqual(cp.applica(rev, "2026-10-02"), 0)
            self.assertEqual(cp.applica(rev, "2026-10-02"), 1)


class TestLaRigaDiRevisione(unittest.TestCase):
    def test_sale_di_uno(self):
        t = "<!-- revisione-testo: r3 · 2026-09-01 -->\n# Titolo\n"
        self.assertEqual(cp.alza_revisione(t, "2026-10-02"),
                         "<!-- revisione-testo: r4 · 2026-10-02 -->\n# Titolo\n")

    def test_dopo_il_frontmatter(self):
        t = "---\ntitolo: x\n---\n# Titolo\n"
        self.assertTrue(cp.alza_revisione(t, "2026-10-02").startswith("---\ntitolo: x\n---\n<!-- revisione"))


class TestLaLettura(unittest.TestCase):
    def test_gulpease_sulla_formula(self):
        # 1 frase, 7 parole, 48 lettere: 89 + (300 - 480) / 7 = 63,3
        self.assertEqual(cp.lettura("Il guardiano attraversa lentamente la sala abbandonata.\n")["gulpease"], 63.3)

    def test_la_scala_si_ferma_a_cento(self):
        self.assertEqual(cp.lettura("Il cane dorme. Il gatto no.\n")["gulpease"], 100.0)

    def test_frasi_tutte_uguali_hanno_ritmo_zero(self):
        self.assertEqual(cp.lettura("Il cane dorme. Il gatto beve. Il topo corre.\n")["ritmo"], 0.0)

    def test_si_legge_il_box_se_c_e(self):
        testo = "Una nota lunghissima per il DM, che non si legge.\n\n> *Il cane dorme.*\n"
        self.assertEqual(cp.lettura(testo)["frasi"], 1)


class TestLApplicazioneAutomatica(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.orig, self.risc = d / "orig.md", d / "risc.md"
        self.orig.write_text("> *La sala sembra vuota. Un altare.*\n\nNota per il DM.\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def _mods(self, dopo):
        self.risc.write_text(dopo, encoding="utf-8")
        prima = self.orig.read_text()
        mods, _ = cp._modifiche(prima, dopo, cp.segnala(prima))
        return prima, mods

    def test_motivata_e_innocua_va_da_sola(self):
        prima, mods = self._mods("> *La sala è vuota. Un altare.*\n\nNota per il DM.\n")
        self.assertEqual(cp.automatiche(prima, self.risc.read_text(), mods), {1})

    def test_non_motivata_resta_al_lettore(self):
        prima, mods = self._mods("> *La sala sembra vuota. Un altare.*\n\nNota per il master.\n")
        self.assertEqual(cp.automatiche(prima, self.risc.read_text(), mods), set())

    def test_se_cambia_un_fatto_resta_al_lettore(self):
        self.orig.write_text("> *La sala sembra vuota. Un altare.*\n\nCD 15.\n", encoding="utf-8")
        prima, mods = self._mods("> *La sala è vuota, CD 18. Un altare.*\n\nCD 15.\n")
        self.assertEqual(cp.automatiche(prima, self.risc.read_text(), mods), set())

    def test_applica_auto_lo_scrive_nel_documento(self):
        self.risc.write_text("> *La sala è vuota. Un altare.*\n\nNota per il DM.\n", encoding="utf-8")
        testo, _ = cp.revisione(self.orig, self.risc)
        rev = Path(self.tmp.name) / "REVISIONE.md"
        rev.write_text(testo, encoding="utf-8")
        with mock.patch.object(cp, "_ramo", return_value="claude/prova"):
            self.assertEqual(cp.applica(rev, "2026-10-02", auto=True), 0)
        self.assertIn("| [x] auto | 1 |", rev.read_text())
        self.assertIn("è vuota", self.orig.read_text())


class TestLanguageTool(unittest.TestCase):
    """Il secondo lettore (ADR-0079): locale, tre regole, righe giuste."""

    def _risposta(self, matches):
        import io
        import json as _json
        finto = mock.MagicMock()
        finto.__enter__.return_value = io.StringIO(_json.dumps({"matches": matches}))
        return finto

    def test_senza_server_non_segnala_niente(self):
        with mock.patch.object(cp.urllib.request, "urlopen", side_effect=OSError("rete")):
            self.assertEqual(cp.languagetool("Testo.", "http://localhost:8081"), [])

    def test_le_risposte_diventano_segnalazioni(self):
        m = {"offset": 7, "message": "Concordanza", "rule": {"id": "ARTICOLATA_SOSTANTIVO"},
             "replacements": [{"value": "le case"}]}
        with mock.patch.object(cp.urllib.request, "urlopen", return_value=self._risposta([m])):
            seg = cp.languagetool("Riga.\nla case", "http://localhost:8081")
        self.assertEqual((seg[0].riga, seg[0].norma), (2, "secondo lettore"))
        self.assertIn("ARTICOLATA_SOSTANTIVO", seg[0].dettaglio)
        self.assertIn("le case", seg[0].dettaglio)

    def test_gli_offset_sono_in_utf16(self):
        """Un'emoji sono due unità per LanguageTool: la riga non deve scivolare."""
        testo = "🔥🔥🔥🔥\nab\nc\nd\ne"
        m = {"offset": 4 * 2 + 1 + 3, "message": "x", "rule": {"id": "R"}, "replacements": []}
        with mock.patch.object(cp.urllib.request, "urlopen", return_value=self._risposta([m])):
            seg = cp.languagetool(testo, "http://localhost:8081")
        self.assertEqual(seg[0].riga, 3)

    def test_un_server_fuori_dalla_macchina_e_rifiutato(self):
        """Il testo della campagna non va a un servizio esterno."""
        with mock.patch.object(cp.urllib.request, "urlopen") as u:
            self.assertEqual(cp.languagetool("Testo.", "https://api.languagetool.org"), [])
            u.assert_not_called()

    def test_si_chiedono_solo_le_tre_regole(self):
        with mock.patch.object(cp.urllib.request, "urlopen", return_value=self._risposta([])) as u:
            cp.languagetool("Testo.", "http://127.0.0.1:8081")
        corpo = u.call_args[0][1].decode()
        self.assertIn("enabledOnly=true", corpo)
        for regola in cp.REGOLE_LANGUAGETOOL:
            self.assertIn(regola, corpo)

    def test_il_testo_piano_tiene_i_numeri_di_riga(self):
        md = "---\ntitolo: x\n---\n# Titolo\n\n| a | b |\n```\ncodice\n```\n- una `x` due\n"
        piano = cp.testo_piano(md).split("\n")
        self.assertEqual(len(piano), len(md.split("\n")))
        self.assertEqual(piano[3], "Titolo")
        self.assertEqual(piano[5], "")                    # la tabella
        self.assertEqual(piano[9], "una § due")           # il codice non è una parola


class TestIlDocumentoBastaASeStesso(unittest.TestCase):
    def test_andata_e_ritorno(self):
        prima = "Uno due tre.\n\n> *La sala sembra vuota.*\n\nFine.\n"
        dopo = "Uno tre quattro.\n\n> *La sala è vuota.*\n\nFine, davvero.\n"
        _, marcato = cp._modifiche(prima, dopo, cp.segnala(prima))
        self.assertEqual(cp.dal_markup(marcato), (prima, dopo))

    def test_applica_senza_il_riscritto(self):
        with tempfile.TemporaryDirectory() as d:
            orig, risc = Path(d) / "o.md", Path(d) / "r.md"
            orig.write_text("> *La sala sembra vuota.*\n", encoding="utf-8")
            risc.write_text("> *La sala è vuota.*\n", encoding="utf-8")
            testo, _ = cp.revisione(orig, risc)
            risc.unlink()
            rev = Path(d) / "R.md"
            rev.write_text(testo.replace("| [ ] | 1 |", "| [x] | 1 |"), encoding="utf-8")
            with mock.patch.object(cp, "_ramo", return_value="claude/prova"):
                self.assertEqual(cp.applica(rev, "2026-10-02"), 0)
            self.assertIn("è vuota", orig.read_text())

    def test_un_testo_con_segni_di_revisione_non_si_rivede(self):
        with tempfile.TemporaryDirectory() as d:
            orig, risc = Path(d) / "o.md", Path(d) / "r.md"
            orig.write_text("Un {++segno++} vecchio.\n", encoding="utf-8")
            risc.write_text("Un segno.\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                cp.revisione(orig, risc)


if __name__ == "__main__":
    unittest.main()


class TestIlMiglioramento(unittest.TestCase):
    """Di quanto migliora, non solo «non peggiora» (ADR-0077, estensione del 2026-10-03)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.orig, self.risc = d / "orig.md", d / "risc.md"
        self.prima = "Prima riga.\n\n" + BOX + "\nCD 15 per aprire.\n"
        self.dopo = self.prima.replace("Entrate nella sala. ", "").replace(
            "e ti è sembrato più grande da fuori", "e il fumo lo copre")
        self.orig.write_text(self.prima, encoding="utf-8")
        self.risc.write_text(self.dopo, encoding="utf-8")
        self.registro = Path(self.tmp.name) / "miglioramenti.json"
        self._p = mock.patch.object(cp, "REGISTRO", self.registro)
        self._p.start()

    def tearDown(self):
        self._p.stop()
        self.tmp.cleanup()

    def test_conta_norma_per_norma(self):
        mig = cp.miglioramento(self.prima, self.dopo, self.orig)
        self.assertEqual(mig["segnalazioni"], [2, 0])
        self.assertEqual(mig["norme"], {"P1": [1, 0], "sembra/pare": [1, 0]})
        self.assertEqual(cp.peggiora(mig), [])

    def test_il_punteggio_mqm_sale(self):
        mig = cp.miglioramento(self.prima, self.dopo, self.orig)
        self.assertIsNotNone(mig["mqm"])
        self.assertGreater(mig["mqm"][1], mig["mqm"][0])   # il P1 è una norma pesata

    def test_una_norma_che_cresce_e_un_peggioramento(self):
        mig = cp.miglioramento(self.dopo, self.prima, self.orig)   # al contrario
        self.assertIn("P1 0 → 1", cp.peggiora(mig))

    def test_il_documento_dice_di_quanto(self):
        testo, ok = cp.revisione(self.orig, self.risc)
        self.assertTrue(ok)
        self.assertIn("## Di quanto migliora", testo)
        self.assertIn("**punteggio MQM**", testo)
        self.assertIn("Il punteggio MQM non scende**: sì", testo)

    def test_applica_scrive_il_registro(self):
        testo, _ = cp.revisione(self.orig, self.risc)
        rev = Path(self.tmp.name) / "REVISIONE.md"
        rev.write_text(testo.replace("| [ ] | 1 |", "| [x] | 1 |").replace("| [ ] | 2 |", "| [x] | 2 |"),
                       encoding="utf-8")
        with mock.patch.object(cp, "_ramo", return_value="claude/prova"):
            self.assertEqual(cp.applica(rev, "2026-10-03"), 0)
        voci = cp._leggi_registro()
        self.assertEqual(len(voci), 1)
        self.assertEqual(voci[0]["modifiche"], 2)
        self.assertEqual(voci[0]["segnalazioni"], [2, 0])
        self.assertEqual(cp.registro_cmd(check=True), 0)

    def test_il_cancello_morde(self):
        cp.registra({"data": "2026-10-03", "file": "x.md", "modifiche": 1,
                     "segnalazioni": [1, 2], "mqm": [90.0, 89.0]})
        self.assertEqual(cp.registro_cmd(check=True), 1)

    def test_misura_boccia_un_fatto_cambiato(self):
        self.risc.write_text(self.dopo.replace("CD 15", "CD 18"), encoding="utf-8")
        self.assertEqual(cp.misura_cmd(self.orig, self.risc), 1)

    def test_misura_promuove_il_buon_giro(self):
        self.assertEqual(cp.misura_cmd(self.orig, self.risc), 0)

    def test_il_lotto_scrive_pacchetti_e_classifica(self):
        giocato = Path(self.tmp.name) / "ARC07-DEF-1-PROVA.md"
        giocato.write_text(self.prima, encoding="utf-8")
        uscita = Path(self.tmp.name) / "lotto"
        self.assertEqual(cp.lotto([self.orig, giocato], uscita), 0)
        self.assertTrue((uscita / "LOTTO.md").exists())
        pac = (uscita / "PACCHETTO-ARC07-DEF-1-PROVA.md").read_text(encoding="utf-8")
        self.assertIn("già letto al tavolo (D9)", pac)
        self.assertIn("| 1 |", pac)
        self.assertNotIn("già letto", (uscita / "PACCHETTO-orig.md").read_text(encoding="utf-8"))

    def test_un_file_pulito_non_ha_pacchetto(self):
        pulito = Path(self.tmp.name) / "pulito.md"
        pulito.write_text("Una riga.\n", encoding="utf-8")
        uscita = Path(self.tmp.name) / "lotto"
        cp.lotto([pulito], uscita)
        self.assertFalse((uscita / "PACCHETTO-pulito.md").exists())
        self.assertIn("pulito.md", (uscita / "LOTTO.md").read_text(encoding="utf-8"))


class TestRigenera(unittest.TestCase):
    """L'originale cambia dopo la revisione: `rigenera` riporta le stesse modifiche."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.orig, self.risc = d / "orig.md", d / "risc.md"
        self.prima = "Prima riga.\n\n" + BOX + "\nCD 15 per aprire.\n"
        self.orig.write_text(self.prima, encoding="utf-8")
        self.risc.write_text(self.prima.replace("e ti è sembrato più grande da fuori",
                                                "e il fumo lo copre"), encoding="utf-8")
        testo, _ = cp.revisione(self.orig, self.risc)
        self.rev = d / "REVISIONE.md"
        self.rev.write_text(testo, encoding="utf-8")
        self._p = mock.patch.object(cp, "REGISTRO", d / "miglioramenti.json")
        self._p.start()

    def tearDown(self):
        self._p.stop()
        self.tmp.cleanup()

    def test_riporta_le_modifiche_sul_testo_di_oggi(self):
        self.orig.write_text("Una riga nuova in testa.\n" + self.prima, encoding="utf-8")
        with mock.patch.object(cp, "_ramo", return_value="claude/prova"):
            self.assertEqual(cp.applica(self.rev, "2026-10-10"), 1)   # rifiuta, giustamente
            self.assertEqual(cp.rigenera(self.rev), 0)
            rev = self.rev.read_text(encoding="utf-8")
            self.assertIn("| [ ] | 1 |", rev)                         # le spunte ripartono
            self.rev.write_text(rev.replace("| [ ] |", "| [x] |"), encoding="utf-8")
            self.assertEqual(cp.applica(self.rev, "2026-10-10"), 0)
        nuovo = self.orig.read_text(encoding="utf-8")
        self.assertIn("Una riga nuova in testa.", nuovo)
        self.assertIn("il fumo lo copre", nuovo)

    def test_non_indovina_se_il_punto_e_ambiguo(self):
        doppio = self.prima + "\n" + BOX
        self.orig.write_text(doppio, encoding="utf-8")
        self.assertEqual(cp.rigenera(self.rev), 1)

    def test_originale_invariato_non_fa_niente(self):
        prima = self.rev.read_text(encoding="utf-8")
        self.assertEqual(cp.rigenera(self.rev), 0)
        self.assertEqual(self.rev.read_text(encoding="utf-8"), prima)


class TestDettagliNellaBattutaAccanto(unittest.TestCase):
    """DEF-4 Scena 11 nella #251: il grido di Aegis Fang esce dal box e diventa
    la battuta prima del box. Le parole ci sono ancora."""

    PRIMA = ("## Scena 11\n\n"
             "> 🎚️ **Se e solo se Thorik tiene Aegis Fang in mano** — *un secondo box, corto,\n"
             "> e a lui soltanto*: **AEGIS FANG (non canta: urla, dentro il cranio):**\n"
             "> *«SANGUE ANTICO. ARTEFICE DI LACRIME.»* — *e per un istante la Corona ti\n"
             "> mostra due immagini sovrapposte: questo drago adesso, e un altro drago sopra\n"
             "> mura che bruciano, che non hai mai visto.*\n")
    DOPO = ("## Scena 11\n\n"
            "**AEGIS FANG (non canta: urla, dentro il cranio):** *«SANGUE ANTICO. ARTEFICE\n"
            "DI LACRIME.»*\n\n"
            "> **Read-aloud (Mercer lead) — la visione, solo per Thorik.** *Per un istante\n"
            "> la Corona ti mostra due immagini sovrapposte: questo drago adesso, e un altro\n"
            "> drago sopra mura che bruciano, mura che non hai mai visto.*\n")

    def test_il_grido_passato_alla_battuta_non_impoverisce(self):
        self.assertEqual(cp.box_impoveriti(self.PRIMA, self.DOPO), [])

    def test_senza_la_battuta_il_box_e_impoverito(self):
        senza = self.DOPO.split("\n\n", 2)
        senza = senza[0] + "\n\n" + senza[2]
        self.assertEqual(len(cp.box_impoveriti(self.PRIMA, senza)), 1)


class TestConfronta(unittest.TestCase):
    def test_un_file_senza_versione_di_prima_non_si_confronta(self):
        with tempfile.TemporaryDirectory(dir=cp.RADICE) as d:
            f = Path(d) / "nuovo.md"
            f.write_text("> *Un box nuovo.*\n", encoding="utf-8")
            with mock.patch("builtins.print"):
                self.assertEqual(cp.confronta_cmd("HEAD", [f]), 0)

    def test_un_file_uguale_non_peggiora(self):
        f = cp.RADICE / "07_il Portale Della Forgia Eterna" / "ARC07-HANDOUTS.md"
        with mock.patch("builtins.print") as stampa:
            self.assertEqual(cp.confronta_cmd("HEAD", [f]), 0)
        self.assertIn("1 file su 1", stampa.call_args_list[-1].args[0])


class TestConfrontaNumeriAggiunti(unittest.TestCase):
    def test_un_numero_solo_aggiunto_non_peggiora(self):
        with tempfile.TemporaryDirectory(dir=cp.RADICE) as d:
            f = Path(d) / "x.md"
            prima, dopo = "Il muro regge.\n", "Il muro regge (Scalare CD 25).\n"
            with mock.patch("subprocess.run") as run:
                run.return_value = mock.Mock(returncode=0, stdout=prima)
                f.write_text(dopo, encoding="utf-8")
                with mock.patch("builtins.print") as stampa:
                    esito = cp.confronta_cmd("HEAD", [f])
            self.assertEqual(esito, 0, stampa.call_args_list)
            self.assertIn("solo aggiunti", stampa.call_args_list[0].args[0])

    def test_un_numero_cambiato_peggiora(self):
        with tempfile.TemporaryDirectory(dir=cp.RADICE) as d:
            f = Path(d) / "x.md"
            with mock.patch("subprocess.run") as run:
                run.return_value = mock.Mock(returncode=0, stdout="Scalare CD 20.\n")
                f.write_text("Scalare CD 25.\n", encoding="utf-8")
                with mock.patch("builtins.print"):
                    self.assertEqual(cp.confronta_cmd("HEAD", [f]), 1)
