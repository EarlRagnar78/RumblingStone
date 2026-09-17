"""Test E2E di state_apply su un mini-repo temporaneo: migrazione marker,
applicazione March Clock dalla sessione di prova, idempotenza, prosa intatta."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import state_apply  # noqa: E402
from dmcore.regions import find_regions  # noqa: E402

# ⚠️ Dal 2026-09-16 (decisione D14) in state.md non c'e' piu' NIENTE che la
# macchina marchi con `auto:`. Il March Day e' un campo di state.yaml e la sua
# riga si rigenera come le tabelle; la nota del DM resta prosa, accanto. Il
# fixture lo rispecchia, altrimenti proverebbe un'architettura che non esiste.
MINI_STATE = (
    "# Campaign State\n\n"
    "## §0 Campaign Status At-a-Glance\n\n"
    "prosa dashboard\n\n"
    "### 2.1 March Clock — Official AP Waypoints\n\n"
    + "".join(f"<!-- gen:state:{n} -->\n(da rigenerare)\n<!-- /gen:state:{n} -->\n\n"
              for n in ("march_clock", "waypoints", "archi", "party", "artefatti",
                        "echi", "villain", "conoscenze", "difensori", "scenari"))
    + 
    "prosa che non si tocca MAI\n\n"
    "## 8. Changelog (append-only)\n\n"
    "> Lo storico vive in [`state-changelog.md`](state-changelog.md).\n"
)

# Dal 2026-09-16 (lotto 4d-2) lo storico e' un file a se': erano 1.179 righe,
# il 71% di state.md. Il fixture lo rispecchia, altrimenti proverebbe
# un'architettura che non esiste piu'.
MINI_CHANGELOG = (
    "# Changelog dello stato di campagna — append-only\n\n"
    "Testo di cornice.\n\n"
    "```\n"
    "2026-05-01  Initial state.md created.\n"
    "```\n"
)

# Il master dei fatti: senza, il March Clock degrada a proposta manuale e
# questo test non proverebbe piu' la via di scrittura che il flusso usa davvero.
MINI_YAML = """\
march_clock:
  giorno_corrente: 19
  giorno_arrivo: 42
  waypoints:
  - giorno: '42'
    waypoint: Rethmar
    stato: pending
archi: []
party: []
artefatti: []
echi: []
villain: []
conoscenze: []
difensori_rethmar: []
scenari_rethmar: []
"""

MINI_SESSION = (
    "# Session 3 — Test (2026-05-03)\n\n"
    "**Players present**: A (Thorik)\n\n"
    "## World events triggered\n\n"
    "- **March Clock**: Day 19 → Day 20 (+1)\n"
    "- **Ritual Clock Azarr Kul**: 9/18 → 9/18 (no change)\n"
)


class TestStateApply(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "campaign" / "sessions").mkdir(parents=True)
        self.state = self.repo / "campaign" / "state.md"
        self.state.write_text(MINI_STATE, encoding="utf-8")
        self.yaml = self.repo / "campaign" / "state.yaml"
        self.yaml.write_text(MINI_YAML, encoding="utf-8")
        self.changelog = self.repo / "campaign" / "state-changelog.md"
        self.changelog.write_text(MINI_CHANGELOG, encoding="utf-8")
        (self.repo / "campaign" / "sessions" / "2026-05-03_session-3.md").write_text(
            MINI_SESSION, encoding="utf-8")
        subprocess.run(["git", "-C", str(self.repo), "init", "-q", "-b", "main"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "t@t"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "t"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "init"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "checkout", "-qb",
                        "campaign-group-test"], check=True)

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, *argv):
        return state_apply.main([*argv, "--repo-root", str(self.repo)])

    def test_full_flow(self):
        # 1. migrazione marker (idempotente)
        self.assertEqual(self._run("--migrate", "--no-guard"), 0)
        text = self.state.read_text(encoding="utf-8")
        clog = self.changelog.read_text(encoding="utf-8")
        # ⚠️ In state.md non resta nessuna regione `auto:` (D14): la macchina
        # scrive nel master e la vista si rigenera. Lo storico ha la sua.
        self.assertEqual(set(find_regions(text)), set())
        self.assertEqual(set(find_regions(clog)), {"changelog"})
        self.assertEqual(self._run("--migrate", "--no-guard"), 0)  # 2° run: no-op
        self.assertEqual(text, self.state.read_text(encoding="utf-8"))
        self.assertEqual(clog, self.changelog.read_text(encoding="utf-8"))

        subprocess.run(["git", "-C", str(self.repo), "commit", "-aqm", "markers"],
                       check=True)

        # 2. --check non scrive
        before = self.state.read_text(encoding="utf-8")
        before_clog = self.changelog.read_text(encoding="utf-8")
        self.assertEqual(self._run("--session", "2026-05-03_session-3.md",
                                   "--check", "--yes", "--no-guard"), 0)
        self.assertEqual(before, self.state.read_text(encoding="utf-8"))
        self.assertEqual(before_clog, self.changelog.read_text(encoding="utf-8"))

        # 3. applicazione reale
        self.assertEqual(self._run("--session", "2026-05-03_session-3.md",
                                   "--yes", "--no-guard"), 0)
        after = self.state.read_text(encoding="utf-8")
        after_clog = self.changelog.read_text(encoding="utf-8")
        # Il numero adesso passa dal MASTER: si scrive in state.yaml e la vista
        # lo riporta in state.md (D14). Verificare solo il markdown proverebbe
        # meta' della catena.
        self.assertIn("giorno_corrente: 20", self.yaml.read_text(encoding="utf-8"))
        self.assertIn("**Current March Day:** **20**", after)
        self.assertIn("**22**", after)                       # 42 - 20
        self.assertIn("prosa che non si tocca MAI", after)
        # la voce di changelog finisce nell'ALTRO file
        self.assertIn("March Clock Day 19 → Day 20", after_clog)
        self.assertNotIn("March Clock Day 19 → Day 20", after,
                         "la voce non deve finire anche in state.md: due storici divergono")
        self.assertIn("2026-05-01  Initial state.md created.", after_clog)

        # 4. la prosa fuori dalle regioni è byte-identica, in ENTRAMBI i file
        import re
        # Si mascherano TUTTE le regioni generate, non solo quella del clock: al
        # primo apply la vista si rigenera per intero, e confrontare solo una
        # regione farebbe passare per «prosa toccata» il lavoro del renderer.
        rx = re.compile(r"<!-- gen:state:(\w+) -->\n.*?\n<!-- /gen:state:\1 -->", re.S)
        self.assertEqual(rx.sub("<REGIONE>", before), rx.sub("<REGIONE>", after),
                         "fuori dalle regioni generate non si tocca niente")
        cl_b, cl_a = find_regions(before_clog), find_regions(after_clog)
        self.assertEqual(before_clog[:cl_b["changelog"].start],
                         after_clog[:cl_a["changelog"].start])
        self.assertEqual(before_clog[cl_b["changelog"].end:],
                         after_clog[cl_a["changelog"].end:])

        # 5. idempotenza: ri-applicare la stessa sessione non duplica nulla
        subprocess.run(["git", "-C", str(self.repo), "commit", "-aqm", "apply"],
                       check=True)
        self.assertEqual(self._run("--session", "2026-05-03_session-3.md",
                                   "--yes", "--no-guard"), 0)
        self.assertEqual(
            self.changelog.read_text(encoding="utf-8").count("March Clock Day 19 → Day 20"), 1)

    def test_guard_blocks_main(self):
        subprocess.run(["git", "-C", str(self.repo), "checkout", "-q", "main"], check=True)
        rc = self._run("--session", "2026-05-03_session-3.md", "--yes")
        self.assertEqual(rc, 1)
        self.assertNotIn("**20**", self.state.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
