"""Le correzioni del 2026-11-18 agli script delle prove sulla RTX 4050 (lettore, immagini).

Senza GPU si controlla la logica che ha sbagliato o poteva sbagliare: gli argomenti con cui
parte ComfyUI, il lettore che non perde le risposte se il server cade, la porta del server
passata al lettore.
"""
import http.server
import importlib.util
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
PROVE = REPO / "scripts" / "prove-4050"
GRAFO = REPO / "plans" / "esperimenti" / "grafo-eventi-2026-11-12"
IMMAGINI = REPO / "plans" / "esperimenti" / "immagini-posa-4050-2026-11-15" / "dati"


def _esegui_gpu():
    spec = importlib.util.spec_from_file_location("esegui_gpu", IMMAGINI / "esegui_gpu.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class TestArgomentiComfy(unittest.TestCase):
    def test_cpu_e_lowvram_mai_insieme(self):
        # ComfyUI mette --cpu e le opzioni di VRAM nello stesso gruppo esclusivo: insieme non parte
        m = _esegui_gpu()
        a = m.argomenti_comfy(8188, True, "--lowvram --preview-method none")
        self.assertIn("--cpu", a)
        self.assertNotIn("--lowvram", a)
        self.assertIn("--preview-method", a)

    def test_gpu_tiene_lowvram(self):
        m = _esegui_gpu()
        a = m.argomenti_comfy(8188, False, "--lowvram")
        self.assertIn("--lowvram", a)
        self.assertNotIn("--cpu", a)
        self.assertEqual(a[:5], ["main.py", "--listen", "127.0.0.1", "--port", "8188"])

    def test_immagini_sh_profilo_leggero_sulla_gpu_senza_lowvram(self):
        testo = (PROVE / "immagini.sh").read_text(encoding="utf-8")
        self.assertIn("RS_COMFY_DEVICE=gpu", testo)
        self.assertIn('if [ "$PROFILO" = gpu ]; then COMFY_ARGS="${RS_COMFY_ARGS---lowvram}"', testo)
        self.assertIn("su_cpu = a.profilo == \"cpu\" and os.environ.get(\"RS_COMFY_DEVICE\") != \"gpu\"",
                      (IMMAGINI / "esegui_gpu.py").read_text(encoding="utf-8"))

    def test_immagini_sh_rifiuta_profilo_e_semi_sbagliati(self):
        for extra in (["--profilo", "tpu"], ["--semi", "due"], ["--semi", "0"]):
            r = subprocess.run(["bash", str(PROVE / "immagini.sh"), *extra], capture_output=True, text=True,
                               env={"PATH": "/usr/bin:/bin", "HOME": tempfile.gettempdir(), "RS_SENZA_BOX": "1"})
            self.assertEqual(r.returncode, 2, f"{extra}: {r.stderr}")


class TestIndicePyTorch(unittest.TestCase):
    def test_niente_cu124(self):
        # cu124 si ferma a torch 2.6.0; il ComfyUI fissato dà la 2.7 come minimo e vuole la 2.8
        for f in (PROVE / "immagini.sh", REPO / "scripts" / "comfyui-local" / "setup-distrobox.sh"):
            testo = f.read_text(encoding="utf-8")
            self.assertNotIn("whl/cu124", testo, f.name)
            self.assertIn("whl/cu126", testo, f.name)

    def test_un_venv_con_torch_vecchio_si_aggiorna(self):
        testo = (PROVE / "immagini.sh").read_text(encoding="utf-8")
        self.assertIn("v < (2, 8)", testo)
        self.assertIn("pip install -q --upgrade torch torchvision --index-url '$TORCH_INDEX'", testo)
        self.assertNotIn("torchaudio", testo)  # su cu126 è ferma alla 2.11 e riporterebbe indietro torch


class _CadeAllaQuarta(http.server.BaseHTTPRequestHandler):
    viste = 0

    def do_POST(self):  # noqa: N802
        self.rfile.read(int(self.headers["Content-Length"]))
        type(self).viste += 1
        if type(self).viste >= 4:
            self.send_error(500)
            return
        risposta = json.dumps({"message": {"content": "NO"}}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(risposta)))
        self.end_headers()
        self.wfile.write(risposta)

    def log_message(self, *a):
        pass


class TestLettoreNonPerdeRisposte(unittest.TestCase):
    def test_server_che_cade_le_risposte_avute_restano(self):
        _CadeAllaQuarta.viste = 0
        server = http.server.HTTPServer(("127.0.0.1", 0), _CadeAllaQuarta)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            with tempfile.TemporaryDirectory() as t:
                t = Path(t)
                (t / "d.json").write_text(json.dumps(
                    [{"h": "x", "sistema": "s", "utente": f"domanda {i}"} for i in range(10)]))
                out = t / "r.json"
                r = subprocess.run([sys.executable, str(GRAFO / "leggi_ollama.py"), str(t / "d.json"),
                                    "--modello", "qwen2.5:7b", "--out", str(out),
                                    "--url", f"http://127.0.0.1:{server.server_port}"], capture_output=True)
                self.assertNotEqual(r.returncode, 0)
                self.assertEqual(len(json.loads(out.read_text())), 3)  # meno di 20: prima andavano perse
        finally:
            server.shutdown()

    def test_lettore_coerenza_passa_la_porta(self):
        testo = (PROVE / "lettore-coerenza.sh").read_text(encoding="utf-8")
        self.assertIn('--url "http://127.0.0.1:$LLM_PORTA"', testo)


if __name__ == "__main__":
    unittest.main()
