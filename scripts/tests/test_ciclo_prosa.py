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
        testo = "La forgia rappresenta un vero e proprio patto fra i clan.\n"
        self.assertIn("tic minori in gruppo", _norme(testo))

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
