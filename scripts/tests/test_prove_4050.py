"""Le prove sul portatile con la RTX 4050 (docs/how-to/GUIDA-PROVE-PORTATILE-4050.md).

Il container non ha una GPU: qui si controlla quello che si può controllare senza.
Gli script sono shell valida ed eseguibili, la guida nomina ogni script, il file delle
domande del lettore combacia con la cache di estrai_rag.py, e leggi_ollama.py scrive
le risposte con la chiave di quella cache per qualunque modello.
"""
import hashlib
import http.server
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
PROVE = REPO / "scripts" / "prove-4050"
GUIDA = REPO / "docs" / "how-to" / "GUIDA-PROVE-PORTATILE-4050.md"
GRAFO = REPO / "plans" / "esperimenti" / "grafo-eventi-2026-11-12"
DOMANDE = GRAFO / "misure" / "domande-ollama.json"
IMMAGINI = REPO / "plans" / "esperimenti" / "immagini-posa-4050-2026-11-15" / "dati"


class TestScript(unittest.TestCase):
    def test_shell_valida_ed_eseguibile(self):
        script = sorted(PROVE.glob("*.sh"))
        self.assertGreaterEqual(len(script), 6)
        for s in script:
            r = subprocess.run(["bash", "-n", str(s)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, f"{s.name}: {r.stderr}")
            if s.name != "comune.sh":
                self.assertTrue(s.stat().st_mode & 0o111, f"{s.name} non è eseguibile")

    def test_la_guida_nomina_ogni_script(self):
        testo = GUIDA.read_text(encoding="utf-8")
        for s in PROVE.glob("*.sh"):
            if s.name != "comune.sh":
                self.assertIn(f"scripts/prove-4050/{s.name}", testo)

    def test_pipeline_immagini_compila(self):
        for f in ("esegui_gpu.py", "pipeline_scena.py", "misura_immagini.py", "rifinitura.py"):
            compile((IMMAGINI / f).read_text(encoding="utf-8"), f, "exec")
        scene = json.loads((IMMAGINI / "scene.json").read_text(encoding="utf-8"))
        nomi = {s["nome"] for s in scene}
        self.assertIn("thorik_posa_artemis", nomi)  # la scena di serie di immagini.sh
        for s in scene:
            for chiave in ("riferimento", "posa_png", "scena_sfondo", "stile"):
                if s.get(chiave):
                    self.assertTrue((IMMAGINI / s[chiave]).exists(), f"{s['nome']}: manca {s[chiave]}")


class TestDomandeLettore(unittest.TestCase):
    def test_chiavi_come_la_cache_di_estrai_rag(self):
        domande = json.loads(DOMANDE.read_text(encoding="utf-8"))
        self.assertGreater(len(domande), 100)
        for d in domande:
            atteso = hashlib.sha256(("ollama:qwen2.5:7b" + d["utente"]).encode()).hexdigest()
            self.assertEqual(d["h"], atteso)
            self.assertTrue(d["sistema"])


class _Finto(http.server.BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        corpo = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        assert corpo["options"]["temperature"] == 0
        risposta = json.dumps({"message": {"content": "SÌ"}}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(risposta)))
        self.end_headers()
        self.wfile.write(risposta)

    def log_message(self, *a):
        pass


class TestLeggiOllama(unittest.TestCase):
    def test_chiave_per_qualunque_modello_e_ripresa(self):
        server = http.server.HTTPServer(("127.0.0.1", 0), _Finto)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            with tempfile.TemporaryDirectory() as t:
                t = Path(t)
                domande = [{"h": "x", "sistema": "s", "utente": f"domanda {i}"} for i in range(3)]
                (t / "d.json").write_text(json.dumps(domande))
                out = t / "r.json"
                url = f"http://127.0.0.1:{server.server_port}"
                cmd = [sys.executable, str(GRAFO / "leggi_ollama.py"), str(t / "d.json"),
                       "--modello", "gemma4:e4b-it-qat", "--out", str(out), "--url", url]
                subprocess.run(cmd, check=True, capture_output=True)
                r = json.loads(out.read_text())
                attese = {hashlib.sha256(("ollama:gemma4:e4b-it-qat" + d["utente"]).encode()).hexdigest()
                          for d in domande}
                self.assertEqual(set(r), attese)
                p = subprocess.run(cmd, check=True, capture_output=True, text=True)
                self.assertIn("0 nuove", p.stderr + p.stdout)
        finally:
            server.shutdown()


if __name__ == "__main__":
    unittest.main()
