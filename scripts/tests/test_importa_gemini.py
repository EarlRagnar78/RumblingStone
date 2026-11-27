"""Import delle chat di Gemini esportate a mano (AI Studio e Takeout) in Markdown.

Campioni sintetici: i formati sono quelli noti di AI Studio (`chunkedPrompt.chunks`) e di
«La mia attività» di Takeout (`title`, `time`, `safeHtmlItem`). I pensieri del modello non
entrano, le chat non finiscono mai dentro il repo.
"""
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import importa_gemini as ig  # noqa: E402

AISTUDIO = {
    "runSettings": {"model": "models/gemini-2.5-pro"},
    "systemInstruction": {"text": "Sei il DM di Hammerfist."},
    "chunkedPrompt": {"chunks": [
        {"text": "Scrivi la scheda di Krusk", "role": "user"},
        {"text": "ragiono sulla scheda...", "role": "model", "isThought": True},
        {"text": "Krusk, orco barbaro 9, sfida Thorik.", "role": "model"},
        {"role": "user", "driveImage": {"id": "x"}},
        {"role": "model", "parts": [{"text": "pensiero", "thought": True}, {"text": "Fatto."}]},
    ]},
}

TAKEOUT_JSON = [
    {"header": "Gemini Apps", "title": "Prompted Chi è Zalkatar?", "time": "2026-05-03T20:11:00.000Z",
     "products": ["Gemini Apps"], "safeHtmlItem": [{"html": "<p>Zalkatar è un <b>lich</b>.</p><ul><li>uno</li></ul>"}]},
    {"header": "Gemini Apps", "title": "Prompted Ciao", "time": "2026-05-03T19:00:00.000Z"},
    {"header": "Gemini Apps", "title": "Hai inviato il prompt Tordek e Hella", "time": "2026-05-04T08:00:00.000Z",
     "safeHtmlItem": [{"html": "Nani."}]},
]

TAKEOUT_HTML = """<html><body><div class="outer-cell mdl-cell"><div class="mdl-grid">
<div class="header-cell mdl-cell"><p class="mdl-typography--title">App Gemini<br></p></div>
<div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">Prompted Chi guida la Mano Rossa?<br>3 mag 2026, 20:11:00 CEST<br><p>Azarr Kul, &egrave; un mezzodrago.</p></div>
<div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1 mdl-typography--text-right"></div>
</div></div></body></html>"""


class TestAiStudio(unittest.TestCase):
    def test_turni_senza_pensieri(self):
        c = ig.chat_aistudio("Krusk", json.dumps(AISTUDIO).encode())
        self.assertEqual([chi for chi, _ in c["turni"]], ["DM", "Gemini", "DM", "Gemini"])
        testi = "\n".join(t for _, t in c["turni"])
        self.assertNotIn("ragiono", testi)
        self.assertNotIn("pensiero", testi)
        self.assertIn("[allegato: driveImage]", testi)
        self.assertEqual(c["modello"], "models/gemini-2.5-pro")

    def test_file_non_chat_saltato(self):
        self.assertIsNone(ig.chat_aistudio("x.json", b'{"altro": 1}'))
        self.assertIsNone(ig.chat_aistudio("foto.png", b"\x89PNG"))

    def test_zip_e_indice(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            with zipfile.ZipFile(t / "studio.zip", "w") as z:
                z.writestr("Google AI Studio/Krusk", json.dumps(AISTUDIO))
                z.writestr("Google AI Studio/note.txt", "niente")
            self.assertEqual(ig.main(["aistudio", str(t / "studio.zip"), "--out", str(t / "md")]), 0)
            indice = json.loads((t / "md" / "indice.json").read_text())
            self.assertEqual(len(indice), 1)
            self.assertEqual(indice[0]["parole"], {"Hammerfist": 1, "Thorik": 1})
            self.assertIn("Sei il DM", (t / "md" / indice[0]["file"]).read_text())
            self.assertTrue((t / "md" / "INDICE.md").exists())


class TestTakeout(unittest.TestCase):
    def test_json_per_giorno(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            cart = t / "Takeout" / "La mia attività" / "App Gemini"
            cart.mkdir(parents=True)
            (cart / "MyActivity.json").write_text(json.dumps(TAKEOUT_JSON), encoding="utf-8")
            chat = ig.chat_takeout(t / "Takeout")
            self.assertEqual([c["data"] for c in chat], ["2026-05-03", "2026-05-04"])
            primo = chat[0]["turni"]
            self.assertTrue(primo[0][1].endswith("Ciao"))           # in ordine di ora
            self.assertIn("Chi è Zalkatar?", primo[1][1])
            self.assertNotIn("Prompted", primo[1][1])
            self.assertIn("- uno", primo[2][1])
            self.assertIn("Tordek e Hella", chat[1]["turni"][0][1])

    def test_html(self):
        voci = ig.voci_takeout_html(TAKEOUT_HTML.encode())
        self.assertEqual(len(voci), 1)
        self.assertEqual(voci[0]["prompt"], "Chi guida la Mano Rossa?")
        self.assertIn("Azarr Kul, è un mezzodrago.", voci[0]["risposta"])

    def test_html_data_iso_e_giorno(self):
        # prima la data restava «3 mag 2026, ...»: tutto finiva in gemini-senza-data, in ordine alfabetico
        self.assertEqual(ig.ora_iso("3 mag 2026, 20:11:00 CEST"), "2026-05-03T20:11:00")
        self.assertEqual(ig.ora_iso("May 3, 2026, 8:11:00\u202fPM CEST"), "2026-05-03T20:11:00")
        self.assertEqual(ig.ora_iso("Dec 1, 2026, 12:05:09 AM UTC"), "2026-12-01T00:05:09")
        self.assertEqual(ig.ora_iso("3 xyz 2026, 20:11:00"), "3 xyz 2026, 20:11:00")
        with tempfile.TemporaryDirectory() as t:
            cart = Path(t) / "Takeout" / "Le mie attività" / "App Gemini"
            cart.mkdir(parents=True)
            (cart / "LeMieAttività.html").write_text(TAKEOUT_HTML, encoding="utf-8")
            chat = ig.chat_takeout(Path(t) / "Takeout")
            self.assertEqual([c["data"] for c in chat], ["2026-05-03"])

    def test_takeout_intero_solo_gemini(self):
        # un Takeout intero ha «La mia attività» di ogni prodotto: Ricerca e YouTube non sono chat di Gemini
        with tempfile.TemporaryDirectory() as t:
            base = Path(t) / "Takeout" / "My Activity"
            (base / "Search").mkdir(parents=True)
            (base / "Gemini Apps").mkdir()
            (base / "Search" / "MyActivity.json").write_text(json.dumps(
                [{"header": "Search", "title": "Searched for Thorik", "time": "2026-05-01T10:00:00.000Z"}]))
            (base / "Gemini Apps" / "MyActivity.json").write_text(json.dumps(TAKEOUT_JSON + [
                {"header": "YouTube", "title": "Watched Tordek", "time": "2026-05-09T10:00:00.000Z"}]))
            chat = ig.chat_takeout(Path(t) / "Takeout")
            self.assertEqual([c["data"] for c in chat], ["2026-05-03", "2026-05-04"])
            # un file dato da solo si legge anche se il nome non dice Gemini
            solo = Path(t) / "attivita.json"
            solo.write_text(json.dumps(TAKEOUT_JSON))
            self.assertEqual(len(ig.chat_takeout(solo)), 2)

    def test_niente_riconosciuto_esce_3(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            (t / "vuota").mkdir()
            self.assertEqual(ig.main(["takeout", str(t / "vuota"), "--out", str(t / "md")]), 3)


class TestFuoriDalRepo(unittest.TestCase):
    def test_rifiuta_uscita_nel_repo(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "Krusk"
            f.write_text(json.dumps(AISTUDIO))
            self.assertEqual(ig.main(["aistudio", str(f), "--out", str(REPO / "plans" / "tmp-gemini")]), 2)
            self.assertFalse((REPO / "plans" / "tmp-gemini").exists())


if __name__ == "__main__":
    unittest.main()
