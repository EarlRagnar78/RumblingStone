"""Il kit delle prove sulla RTX 4050 salva in un log tutto quello che scrive (richiesta del DM, 2026-11-19).

Prima di questa modifica, di una prova lanciata da kit.sh restavano solo i file che la prova
scriveva da sé: l'uscita e gli errori andavano sul terminale e si perdevano. Qui si lancia il kit
con una prova finta (righe su stdout e stderr, un avviso, un traceback, uscita 3) e si controlla
che ogni riga finisca nel log della sessione e in quello della prova, che gli avvisi finiscano in
avvisi.txt, che il terminale continui a vedere tutto e che il codice d'uscita sia scritto.
"""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
PROVE = REPO / "scripts" / "prove-4050"

FINTA = """#!/usr/bin/env bash
for i in $(seq 1 20); do echo "MARCA-OUT-$i"; done
for i in $(seq 1 10); do echo "MARCA-ERR-$i" >&2; done
echo "AVVISO: MARCA-WARN-1" >&2
python3 -c 'raise RuntimeError("MARCA-TRACEBACK")'
exit 3
"""
MANIFESTO = ('{"prove":[{"id":"finta","script":"finta.sh","uscita":"finta","thread":"x",'
             '"server_ctx":null,"box":null,"minuti_stimati":1,"interattiva":false,"file_attesi":["esito.txt"]}]}')
MARCHE = [f"MARCA-OUT-{i}" for i in range(1, 21)] + [f"MARCA-ERR-{i}" for i in range(1, 11)] + [
    "MARCA-WARN-1", "MARCA-TRACEBACK"]


class TestLogDelKit(unittest.TestCase):
    def setUp(self):
        self.t = Path(tempfile.mkdtemp())
        self.k = self.t / "scripts" / "prove-4050"
        shutil.copytree(PROVE, self.k, ignore=shutil.ignore_patterns("__pycache__"))
        (self.k / "prove.json").write_text(MANIFESTO, encoding="utf-8")
        f = self.k / "finta.sh"
        f.write_text(FINTA, encoding="utf-8")
        f.chmod(0o755)
        (self.t / "os").write_text("ID=bazzite\n")
        (self.t / "ver").write_text("Linux version 6.17\n")
        self.ris = self.t / "ris"
        self.env = {k: v for k, v in os.environ.items() if k not in ("RS_SENZA_BOX", "RS_LOG", "PROVE_GIORNO")}
        self.env.update(RS_OS_RELEASE=str(self.t / "os"), RS_PROC_VERSION=str(self.t / "ver"),
                        PROVE_DIR=str(self.ris), PROVE_GIORNO="2026-11-19")
        self.log = self.ris / "2026-11-19" / "log"

    def tearDown(self):
        shutil.rmtree(self.t, ignore_errors=True)

    def kit(self, *arg):
        return subprocess.run([str(self.k / "kit.sh"), *arg], capture_output=True, text=True,
                              env=self.env, timeout=120)

    def test_ogni_riga_della_prova_finisce_nel_log_della_prova(self):
        r = self.kit("esegui", "finta")
        testo = (self.log / "finta.log").read_text(encoding="utf-8")
        mancano = [m for m in MARCHE if m not in testo]
        self.assertEqual(mancano, [], r.stderr)
        self.assertIn("uscita 3", testo)

    def test_il_log_della_sessione_tiene_tutto_una_volta_sola(self):
        self.kit("esegui", "finta")
        sessioni = sorted(self.log.glob("kit-esegui-*.log"))
        self.assertEqual(len(sessioni), 1, list(self.log.iterdir()))
        testo = sessioni[0].read_text(encoding="utf-8")
        self.assertIn("################ finta", testo)
        for m in MARCHE:
            self.assertEqual(testo.count(m + "\n"), 1, m)
        # in testa: comando, data, sistema; in coda: il codice d'uscita del kit
        prima = testo.splitlines()[0]
        self.assertIn("kit", prima)
        self.assertIn("bazzite", prima)
        self.assertRegex(testo.splitlines()[-1], r"^# uscita \d+")

    def test_il_terminale_vede_ancora_tutto_e_stderr_resta_stderr(self):
        r = self.kit("esegui", "finta")
        self.assertIn("MARCA-OUT-20", r.stdout)
        self.assertIn("MARCA-ERR-10", r.stderr)
        self.assertNotIn("MARCA-ERR-10", r.stdout)
        self.assertIn("log/", r.stdout + r.stderr)   # il kit dice dove sono i log

    def test_avvisi_ed_errori_raccolti(self):
        self.kit("esegui", "finta")
        avvisi = (self.log / "avvisi.txt").read_text(encoding="utf-8")
        self.assertIn("MARCA-WARN-1", avvisi)
        self.assertIn("MARCA-TRACEBACK", avvisi)
        self.assertIn("finta.log", avvisi)          # dice da che file viene la riga
        self.assertNotIn("MARCA-OUT-1\n", avvisi)

    def test_installa_registra_anche_con_mostra(self):
        r = subprocess.run([str(self.k / "installa.sh"), "--mostra"], capture_output=True, text=True,
                           env=self.env, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        log = sorted(self.log.glob("installa-*.log"))
        self.assertEqual(len(log), 1)
        self.assertIn("==> 1/4", log[0].read_text(encoding="utf-8"))

    def test_kit_installa_non_apre_due_log(self):
        self.kit("installa", "--mostra")
        self.assertEqual(len(list(self.log.glob("*.log"))), 1, list(self.log.iterdir()))

    def test_una_prova_lanciata_da_sola_registra(self):
        r = subprocess.run([str(self.k / "controlla.sh")], capture_output=True, text=True,
                           env=self.env, timeout=60)
        log = sorted(self.log.glob("controlla-*.log"))
        self.assertEqual(len(log), 1, r.stderr)
        self.assertIn("GPU", log[0].read_text(encoding="utf-8"))

    def test_riporta_mette_i_log_nell_archivio(self):
        self.kit("esegui", "finta")
        subprocess.run([str(self.k / "riporta.sh"), "2026-11-19"], capture_output=True, text=True,
                       env=self.env, timeout=60)
        elenco = subprocess.run(["tar", "-tzf", str(self.ris / "prove-4050-2026-11-19.tar.gz")],
                                capture_output=True, text=True).stdout
        self.assertIn("2026-11-19/log/finta.log", elenco)
        self.assertIn("2026-11-19/log/avvisi.txt", elenco)

    def test_piano_non_scrive_log(self):
        """piano e aiuto leggono soltanto: niente cartella log per un'occhiata allo stato."""
        self.kit("piano")
        self.assertFalse(self.log.exists())

    def test_terminale_rimesso_a_posto_sul_terminale_vero(self):
        """Col log, stdout è una pipe verso tee: stty va chiesto al terminale salvato prima."""
        testo = (PROVE / "kit.sh").read_text(encoding="utf-8")
        corpo = testo[testo.index("terminale_a_posto() {"):testo.index("ferma_server() {")]
        self.assertIn("stty sane", corpo)
        self.assertIn("RS_FD_TERMINALE", corpo)


class TestTranscriptWindows(unittest.TestCase):
    def test_start_transcript_e_uscite_di_wsl_nel_transcript(self):
        testo = (PROVE / "installa-windows.ps1").read_text(encoding="utf-8-sig")
        self.assertIn("Start-Transcript", testo)
        self.assertIn("Stop-Transcript", testo)
        # In Windows PowerShell 5.1 l'uscita di un eseguibile nativo non entra nel transcript se non
        # passa dalla pipeline: ogni wsl.exe che lancia il kit va mandato a Out-Host.
        for riga in testo.splitlines():
            if "wsl.exe -d $Distro -- bash -lc" in riga and not riga.lstrip().startswith("#"):
                self.assertIn("| Out-Host", riga, riga)
        # mai 2>&1 su un nativo: con ErrorActionPreference=Stop la prima riga di stderr ferma tutto
        self.assertNotIn("wsl.exe -d $Distro -- bash -lc $installa 2>&1", testo)


if __name__ == "__main__":
    unittest.main()
