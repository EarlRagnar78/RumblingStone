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


class TestDrappoFlux(unittest.TestCase):
    """Il collaudo della D2: i pesi che drappo_flux.py scarica sono quelli che il grafo carica."""

    def setUp(self):
        sys.path.insert(0, str(PROVE))
        sys.path.insert(0, str(REPO / "scripts"))
        import comfyui_batch
        import drappo_flux
        self.cb, self.df = comfyui_batch, drappo_flux

    def test_pesi_del_grafo_e_del_download_coincidono(self):
        mod = self.cb.MODELLI[self.df.MODELLO]
        nomi = {n for _, n, *_ in self.df.PESI}
        self.assertEqual(nomi, {mod["checkpoint"], mod["clip"], mod["vae"]})
        sha = {n: s for _, n, _, _, s, _ in self.df.PESI}
        self.assertEqual(sha[mod["checkpoint"]], mod["sha256"])
        for _, n, _, _, s, byte in self.df.PESI:
            self.assertRegex(s, r"^[0-9a-f]{64}$", n)
            self.assertGreater(byte, 10**8, n)

    def test_nessun_peso_vietato(self):
        for _, nome, repo, f, *_ in self.df.PESI:
            for vietato in self.cb.PESI_VIETATI:
                self.assertNotIn(vietato, f"{nome} {repo} {f}".lower())

    def test_tavole_di_serie_esistono_e_hanno_la_gemini(self):
        noti = {i.ident for i in self.cb.leggi_immagini(self.cb.PROMPTS_DEFAULT.read_text(encoding="utf-8"))}
        for ident in self.df.SOLO_DEFAULT.split(","):
            self.assertIn(ident, noti)
            self.assertTrue((self.df.GEMINI / f"{ident}.png").exists(), ident)
        self.assertIn(self.df.SOLO_DEFAULT, (PROVE / "drappo-flux.sh").read_text(encoding="utf-8"))

    def test_impronta_ricordata_solo_se_giusta(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "peso.safetensors"
            f.write_bytes(b"abc")
            giusto = hashlib.sha256(b"abc").hexdigest()
            self.assertFalse(self.df.peso_verificato(f, "0" * 64))
            self.assertFalse(f.with_name(f.name + ".sha256").exists())
            self.assertTrue(self.df.peso_verificato(f, giusto))
            self.assertTrue(self.df.peso_verificato(f, giusto))  # dalla nota
            self.assertFalse(self.df.peso_verificato(Path(d) / "manca", giusto))

    def test_pagina_di_confronto(self):
        with tempfile.TemporaryDirectory() as d:
            righe = [{"id": "il-drappo", "seme": 0, "secondi": 9.5, "file": "flux/seme-0/il-drappo.png"},
                     {"id": "il-drappo", "seme": 1, "secondi": 0, "file": None}]
            self.df.pagina(righe, Path(d), ["il-drappo"], 2)
            testo = (Path(d) / "confronto.html").read_text(encoding="utf-8")
            self.assertIn("A · Gemini", testo)
            self.assertIn("flux/seme-0/il-drappo.png", testo)
            self.assertIn("seme 1: fallita", testo)


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


VINCOLATA = REPO / "plans" / "esperimenti" / "decodifica-vincolata-2026-11-17"


class _FintoTattiche(http.server.BaseHTTPRequestHandler):
    """Un Ollama finto: il libero nomina sempre *palla di fuoco*, che nessuna scheda
    del campione ha; il vincolato sceglie la prima azione dell'enum."""
    chiamate: list = []

    def do_POST(self):  # noqa: N802
        corpo = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        type(self).chiamate.append(corpo)
        fmt = corpo.get("format")
        if fmt:
            enum = fmt["properties"]["prima"]["items"]["properties"]["azione"]["enum"]
            passo = {"azione": enum[0], "bersaglio": "il mago", "perche": "lo tiene lontano"}
            testo = json.dumps({"prima": [passo], "durante": [passo], "morale": [passo]})
        else:
            testo = ("- *Prima del combattimento*: lancia *palla di fuoco* sul gruppo.\n"
                     "- *Durante il combattimento*: attacca.\n- *Morale*: fugge.")
        risposta = json.dumps({"message": {"content": testo}, "eval_count": 50,
                               "eval_duration": 10 ** 9}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(risposta)))
        self.end_headers()
        self.wfile.write(risposta)

    def log_message(self, *a):
        pass


class TestSchedeVincolate(unittest.TestCase):
    """La tecnica 3 (decodifica vincolata): la misura senza GPU, con un Ollama finto."""

    def setUp(self):
        sys.path.insert(0, str(VINCOLATA))
        import schede_vincolate
        self.S = schede_vincolate

    def test_voci_e_schema_di_una_scheda(self):
        v = self.S.voci(self.S.genera("chierico:8", 8, "controllore", 3))
        self.assertIn("oscurità", v["incantesimi"])
        self.assertTrue(any(t.startswith("Incantesimi focalizzati") for t in v["talenti"]))
        self.assertEqual(v["attacchi"], ["attacco con bastone ferrato"])
        enum = self.S.schema(v)["properties"]["durante"]["items"]["properties"]["azione"]["enum"]
        self.assertTrue(set(v["incantesimi"]) <= set(enum))
        self.assertIn("fuggire", enum)

    def test_json_fuori_schema_non_vale(self):
        v = {"incantesimi": ["comando"], "talenti": [], "attacchi": []}
        self.assertIsNone(self.S.in_markdown("{non json", v)[0])
        passo = {"azione": "palla di fuoco", "bersaglio": "x", "perche": "y"}
        self.assertIn("fuori dallo schema", self.S.in_markdown(
            json.dumps({"prima": [passo], "durante": [passo], "morale": [passo]}), v)[1])

    def test_copertura_zero_non_migliora(self):
        # il libero non nomina nessuna voce e sbaglia; il vincolato non sbaglia ma
        # scrive solo azioni comuni: non è un miglioramento
        base = {"valida": True, "secondi": 1, "token": 1, "ns": 1, "fuori_lista": [], "menzioni": 0}
        righe = [dict(base, braccio="libero", s8=1, copertura=0),
                 dict(base, braccio="vincolato", s8=0, copertura=0)]
        self.assertFalse(self.S.riassumi(righe)["migliora"])
        righe[1]["copertura"] = 1
        self.assertTrue(self.S.riassumi(righe)["migliora"])

    def test_misura_completa_e_ripresa(self):
        server = http.server.HTTPServer(("127.0.0.1", 0), _FintoTattiche)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            with tempfile.TemporaryDirectory() as t:
                out = Path(t) / "ris"
                cmd = [sys.executable, str(VINCOLATA / "schede_vincolate.py"), "--modello", "finto",
                       "--out", str(out), "--quante", "2", "--ripetizioni", "1",
                       "--url", f"http://127.0.0.1:{server.server_port}"]
                subprocess.run(cmd, check=True, capture_output=True)
                self.assertEqual(len(_FintoTattiche.chiamate), 4)
                self.assertTrue(all("format" in c for c in _FintoTattiche.chiamate[1::2]))
                s = json.loads((out / "misure.json").read_text())["sintesi"]
                self.assertEqual(s["libero"]["violazioni_s8"], 2)
                self.assertEqual(s["vincolato"]["violazioni_s8"], 0)
                self.assertEqual(s["vincolato"]["valide"], 2)
                self.assertGreater(s["libero"]["fuori_lista"], 0)
                self.assertTrue(s["migliora"])
                subprocess.run(cmd, check=True, capture_output=True)
                self.assertEqual(len(_FintoTattiche.chiamate), 4)   # tutto dalla cache
        finally:
            server.shutdown()


if __name__ == "__main__":
    unittest.main()
