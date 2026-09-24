"""Test del wizard di fine sessione (Lotto B): answers-file → log canonico
che gli altri script capiscono (state_sync, update_xp, visibility)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import session_wizard  # noqa: E402
from dmcore import visibility  # noqa: E402
from state_sync import extract_events  # noqa: E402

ANSWERS = {
    "date": "2026-08-01",
    "number": 4,
    "title": "Il Guado dei Non-Morti",
    "players": "Marco (Thorik), Luca (Tordek)",
    "location": "Blackfens",
    "in_world": "from Day 20 to Day 21",
    "summary": ["Il party ha attraversato il guado.", "Poi la palude."],
    "decisions": ["Thorik guida la colonna"],
    "xp_lines": ["Pattuglia (EL 11) → 3.300 / 4"],
    "xp_total": 825,
    "loot": ["Anello +1 → Tordek"],
    "march_clock": "Day 20 → Day 21 (+1)",
    "hooks": ["Voci di razorfiend a est"],
    "dm_notes": ["Segreto: Sal avanza"],
    "splits": [{"pgs": "Tordek", "place": "Riva nord",
                "body": ["Tordek nota impronte drow."]}],
}


class TestSessionWizard(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "campaign" / "sessions").mkdir(parents=True)
        subprocess.run(["git", "-C", str(self.repo), "init", "-q", "-b", "main"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "t@t"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "t"], check=True)
        (self.repo / "x").write_text("x")
        subprocess.run(["git", "-C", str(self.repo), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "init"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "checkout", "-qb",
                        "campaign-group-test"], check=True)
        self.answers = self.repo / "answers.json"
        self.answers.write_text(json.dumps(ANSWERS), encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_wizard_writes_canonical_log(self):
        rc = session_wizard.main(["--answers", str(self.answers),
                                  "--repo-root", str(self.repo)])
        self.assertEqual(rc, 0)
        out = self.repo / "campaign" / "sessions" / "2026-08-01_session-4.md"
        text = out.read_text(encoding="utf-8")

        # header + formato canonico che update_xp/state_sync capiscono
        self.assertIn("# Session 4 — Il Guado dei Non-Morti (2026-08-01)", text)
        self.assertIn("- **Total**: 825 xp a testa", text)
        ev = extract_events(out)
        kinds = [k for k, _, _ in ev["hits"]]
        self.assertIn("march_clock", kinds)  # "Day 20 → Day 21" riconosciuto

        # split e note DM al posto giusto
        blocks = visibility.for_pg(text, "Tordek")
        self.assertEqual(len(blocks), 1)
        self.assertIn("impronte drow", blocks[0].body)
        self.assertEqual(visibility.for_pg(text, "Thorik"), [])
        self.assertIn("## DM notes", text)
        self.assertTrue(text.index("## DM notes") > text.index("## Split"))

        # commit automatico eseguito
        log = subprocess.run(["git", "-C", str(self.repo), "log", "-1", "--format=%s"],
                             capture_output=True, text=True, check=True).stdout
        self.assertIn("Session 4", log)

    def test_wizard_refuses_overwrite(self):
        self.assertEqual(session_wizard.main(
            ["--answers", str(self.answers), "--repo-root", str(self.repo)]), 0)
        self.assertEqual(session_wizard.main(
            ["--answers", str(self.answers), "--repo-root", str(self.repo)]), 1)

    def test_wizard_blocked_on_main(self):
        subprocess.run(["git", "-C", str(self.repo), "checkout", "-q", "main"], check=True)
        rc = session_wizard.main(["--answers", str(self.answers),
                                  "--repo-root", str(self.repo)])
        self.assertEqual(rc, 1)


class TestIlWizardScriveIlDelta(unittest.TestCase):
    """Lotto 4e-2: le risposte diventano un front-matter, sui master VERI.

    Il wizard risolve i nomi contro `campaign/state.yaml` mentre il DM e' li',
    e `state_apply` legge il risultato senza passare dalla regex.
    """

    ROOT = SCRIPTS.parent

    def setUp(self):
        import shutil
        import yaml
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "campaign" / "sessions").mkdir(parents=True)
        for nome in ("state.md", "state.yaml", "state-changelog.md"):
            shutil.copy(self.ROOT / "campaign" / nome, self.repo / "campaign" / nome)
        for cmd in (["init", "-q", "-b", "main"], ["config", "user.email", "t@t"],
                    ["config", "user.name", "t"], ["add", "-A"],
                    ["commit", "-qm", "init"], ["checkout", "-qb", "campaign-group-test"]):
            subprocess.run(["git", "-C", str(self.repo), *cmd], check=True)
        self.dati = yaml.safe_load((self.repo / "campaign" / "state.yaml")
                                   .read_text(encoding="utf-8"))
        v = {r["png_id"]: r for r in self.dati["villain"]}
        self.gha = int(str(v["ghaurush"]["clock"]).partition("/")[0])
        self.rit = int(str(v["azarr-kul"]["clock"]).partition("/")[0])
        self.day = self.dati["march_clock"]["giorno_corrente"]

    def tearDown(self):
        self._tmp.cleanup()

    def _risposte(self, **extra):
        a = dict(ANSWERS, number=5, splits=[], dm_notes=[],
                 march_clock=f"Day {self.day} → Day {self.day + 1} (+1)",
                 ritual_clock=f"{self.rit}/18 → {self.rit + 1}/18",
                 villain_clocks=f"Ghaurush {self.gha}→{self.gha + 1}, Pinco 1→2",
                 png_status="Ushgar morto")
        a.update(extra)
        return a

    def test_le_risposte_diventano_dati_per_png_id(self):
        import session_wizard as sw
        delta, avvisi = sw.delta_dalle_risposte(self._risposte(), self.dati)
        self.assertEqual(delta["march_clock"], {"da": self.day, "a": self.day + 1})
        self.assertEqual({c["png_id"] for c in delta["clock"]}, {"ghaurush", "azarr-kul"})
        self.assertEqual(delta["stato"], [{"png_id": "ushgar", "stato": "morto"}])
        self.assertEqual(len(avvisi), 1)
        self.assertIn("Pinco", avvisi[0])

    def test_una_voce_che_non_torna_resta_prosa_e_non_trascina_le_altre(self):
        import session_wizard as sw
        sbagliato = f"Ghaurush {self.gha + 3}→{self.gha + 4}"
        delta, avvisi = sw.delta_dalle_risposte(
            self._risposte(villain_clocks=sbagliato), self.dati)
        self.assertEqual([c["png_id"] for c in delta["clock"]], ["azarr-kul"])
        self.assertIn("stato", delta)
        self.assertTrue(any("state.yaml dice" in x for x in avvisi))

    def test_un_nome_ambiguo_non_sceglie(self):
        import session_wizard as sw
        delta, avvisi = sw.delta_dalle_risposte(
            self._risposte(png_status="Illithid morto"), self.dati)
        self.assertNotIn("stato", delta)
        self.assertTrue(any("ambiguo" in x for x in avvisi))

    def test_dal_wizard_a_state_apply_senza_regex(self):
        import state_apply
        import yaml
        risposte = self.repo / "r.json"
        risposte.write_text(json.dumps(self._risposte()), encoding="utf-8")
        self.assertEqual(session_wizard.main(
            ["--answers", str(risposte), "--repo-root", str(self.repo)]), 0)
        log = self.repo / "campaign" / "sessions" / "2026-08-01_session-5.md"
        self.assertTrue(log.read_text(encoding="utf-8").startswith("---\n"))
        self.assertEqual(state_apply.main(
            ["--session", log.name, "--yes", "--no-guard",
             "--repo-root", str(self.repo)]), 0)
        dopo = yaml.safe_load((self.repo / "campaign" / "state.yaml")
                              .read_text(encoding="utf-8"))
        v = {r["png_id"]: r for r in dopo["villain"]}
        self.assertEqual(str(v["ghaurush"]["clock"]).partition("/")[0], str(self.gha + 1))
        self.assertEqual(str(v["azarr-kul"]["clock"]), f"{self.rit + 1}/18")
        self.assertEqual(v["ushgar"]["stato"], "morto")
        self.assertEqual(dopo["march_clock"]["giorno_corrente"], self.day + 1)

    def test_senza_state_yaml_il_log_esce_senza_front_matter(self):
        (self.repo / "campaign" / "state.yaml").unlink()
        risposte = self.repo / "r.json"
        risposte.write_text(json.dumps(self._risposte()), encoding="utf-8")
        self.assertEqual(session_wizard.main(
            ["--answers", str(risposte), "--repo-root", str(self.repo), "--no-commit"]), 0)
        log = self.repo / "campaign" / "sessions" / "2026-08-01_session-5.md"
        self.assertTrue(log.read_text(encoding="utf-8").startswith("# Session 5"))


if __name__ == "__main__":
    unittest.main()
