"""ambiente.py: il registro possiede solo ciò che ha installato, e rimuovi toglie solo quello.

È il criterio di qualità di A5c (PIANO-AMBIENTE): installa un pacchetto che
mancava e uno che c'era; rimuovi toglie il primo, lascia il secondo, e lo stato
di dpkg torna quello di partenza. Qui con un sistema finto: niente sudo in CI.
"""

import json
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import ambiente as A  # noqa: E402

DIPENDENZE = {"maven": ["libmaven"], "blender": ["libblend"]}


class Finto(A.Sistema):
    def __init__(self, installati, rdepends=None, risposte=True):
        self.installati = dict(installati)
        self.rdep = rdepends or {}
        self.risposte = risposte
        self.comandi = []
        self.pip_pkgs = {"pytest": "9"}

    def os_release(self):
        return {"ID": "debian", "PRETTY_NAME": "Debian 13"}

    def dpkg(self):
        return dict(self.installati)

    def dipendono_da(self, p):
        return set(self.rdep.get(p, ()))

    def pip(self):
        return dict(self.pip_pkgs)

    def chiedi(self, domanda):
        return self.risposte

    def esegui(self, cmd, *, cattura=True, env=None):
        self.comandi.append(cmd)
        out = ""
        if cmd[:3] == ["apt-get", "-s", "install"]:
            out = "\n".join(f"Inst {p} (1)" for p in cmd[4:] for p in [p, *DIPENDENZE.get(p, [])])
        elif cmd[:3] == ["apt-get", "-s", "remove"]:
            out = "\n".join(f"Remv {p} [1]" for p in cmd[3:])
        elif cmd[:3] == ["sudo", "apt-get", "install"]:
            for p in cmd[5:]:
                self.installati[p] = "1"
                for d in DIPENDENZE.get(p, []):
                    self.installati[d] = "1"
        elif cmd[:3] == ["sudo", "apt-get", "remove"]:
            for p in cmd[4:]:
                self.installati.pop(p, None)
        elif cmd[1:4] == ["-m", "pip", "install"]:
            self.pip_pkgs.update({"bpy": "5", "torch": "2"})
        elif cmd[1:4] == ["-m", "pip", "uninstall"]:
            for p in cmd[5:]:
                self.pip_pkgs.pop(p, None)
        return types.SimpleNamespace(returncode=0, stdout=out, stderr="")


class TestRegistro(unittest.TestCase):
    def setUp(self):
        self.stato = Path(tempfile.mkdtemp()) / "stato.json"

    def _zitto(self, f, *a):
        with redirect_stdout(StringIO()):
            return f(*a)

    def test_installa_possiede_solo_cio_che_mancava_e_rimuovi_torna_al_punto_di_partenza(self):
        prima = {"chromium": "150", "webp": "1.5"}
        sis = Finto(prima)
        self._zitto(A.installa_apt, sis, ["chromium", "maven"], self.stato, True)
        posseduti = A.leggi_stato(self.stato)["passi"][0]["posseduti"]
        self.assertEqual(set(posseduti), {"maven", "libmaven"})
        self.assertEqual(self._zitto(A.rimuovi, sis, self.stato, True, False), 0)
        self.assertEqual(sis.dpkg(), prima)
        self.assertEqual(A.leggi_stato(self.stato)["passi"], [])

    def test_un_pacchetto_nostro_da_cui_dipende_altro_resta(self):
        sis = Finto({}, rdepends={"libmaven": ["eclipse"]})
        self._zitto(A.installa_apt, sis, ["maven"], self.stato, True)
        sis.installati["eclipse"] = "4"  # installato dopo, a mano
        out = StringIO()
        with redirect_stdout(out):
            A.rimuovi(sis, self.stato, True, False)
        self.assertIn("libmaven", sis.installati)
        self.assertNotIn("maven", sis.installati)
        self.assertIn("libmaven resta: ne dipende eclipse", out.getvalue())

    def test_mai_autoremove_ne_purge(self):
        sis = Finto({})
        self._zitto(A.installa_apt, sis, ["maven"], self.stato, True)
        self._zitto(A.rimuovi, sis, self.stato, True, False)
        piatti = [" ".join(c) for c in sis.comandi]
        self.assertFalse(any("autoremove" in c or "purge" in c for c in piatti))

    def test_senza_conferma_non_installa_e_non_registra(self):
        sis = Finto({}, risposte=False)
        self._zitto(A.installa_apt, sis, ["maven"], self.stato, False)
        self.assertNotIn("maven", sis.installati)
        self.assertFalse(self.stato.exists())

    def test_pip_possiede_solo_i_pacchetti_nuovi(self):
        sis = Finto({})
        self._zitto(A.installa_pip, sis, self.stato)
        self.assertEqual(A.leggi_stato(self.stato)["passi"][0]["posseduti"], ["bpy", "torch"])
        self._zitto(A.rimuovi, sis, self.stato, True, False)
        self.assertEqual(sis.pip(), {"pytest": "9"})

    def test_typst_si_toglie_solo_se_e_ancora_il_file_installato(self):
        f = Path(tempfile.mkdtemp()) / "typst"
        f.write_bytes(b"altro")
        A.aggiungi(self.stato, {"tipo": "typst", "file": str(f), "sha256": "0" * 64})
        self._zitto(A.rimuovi, Finto({}), self.stato, True, False)
        self.assertTrue(f.exists())

    def test_adotta_prende_le_transazioni_dal_giorno_e_solo_cio_che_ce_ancora(self):
        history = (
            "Start-Date: 2026-10-08  10:00:00\nCommandline: apt install vecchio\n"
            "Install: vecchio:amd64 (1)\nEnd-Date: 2026-10-08  10:00:01\n\n"
            "Start-Date: 2026-10-09  12:00:00\nCommandline: apt install maven webp\n"
            "Install: maven:amd64 (3.9.9-1), libmaven:all (1, automatic), webp:amd64 (1.5), "
            "tolto:amd64 (2)\nEnd-Date: 2026-10-09  12:01:00\n")
        sis = Finto({"vecchio": "1", "maven": "3.9.9-1", "libmaven": "1", "webp": "1.5"})
        self.assertEqual(A.adotta_apt(sis, history, "2026-10-09"),
                         {"maven": "3.9.9-1", "libmaven": "1", "webp": "1.5"})

    def test_la_versione_di_typst_e_quella_della_ci(self):
        self.assertRegex(A.versione_typst(), r"^\d+\.\d+\.\d+$")

    def test_il_registro_e_per_clone(self):
        self.assertNotEqual(A.percorso_stato(Path("/a")), A.percorso_stato(Path("/b")))


if __name__ == "__main__":
    unittest.main()
