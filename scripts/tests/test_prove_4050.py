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
            if s.name not in ("comune.sh", "ospite.sh"):
                self.assertTrue(s.stat().st_mode & 0o111, f"{s.name} non è eseguibile")

    def test_la_guida_nomina_ogni_script(self):
        testo = GUIDA.read_text(encoding="utf-8")
        for s in PROVE.glob("*.sh"):
            if s.name not in ("comune.sh", "ospite.sh"):  # librerie, non prove
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

    def test_torch_sotto_la_2_8_viene_segnalato(self):
        self.assertTrue(self.df.torch_vecchio("2.6.0+cu124"))
        self.assertFalse(self.df.torch_vecchio("2.8.0"))
        self.assertFalse(self.df.torch_vecchio("2.14.1+cu126"))
        self.assertFalse(self.df.torch_vecchio("assente"))

    def test_clone_di_comfyui_separato_da_quello_delle_immagini(self):
        """esegui_gpu.py mette i suoi nodi in «ComfyUI» solo quando lo crea: questa prova non deve crearlo."""
        sorgente = (PROVE / "drappo_flux.py").read_text(encoding="utf-8")
        self.assertIn('lavoro / "ComfyUI-flux"', sorgente)
        self.assertNotIn('lavoro / "ComfyUI"', sorgente)
        self.assertIn('lavoro / "ComfyUI"', (IMMAGINI / "esegui_gpu.py").read_text(encoding="utf-8"))

    def test_affianca_apre_ogni_gemini_di_serie(self):
        """il-drappo.png ha un blocco C2PA oltre il limite di serie di Pillow: il 18/11 la prova si fermava lì."""
        try:
            import PIL  # noqa: F401
        except ImportError:
            self.skipTest("Pillow non installato")
        with tempfile.TemporaryDirectory() as d:
            for ident in self.df.SOLO_DEFAULT.split(","):
                gem = self.df.GEMINI / f"{ident}.png"
                dest = Path(d) / f"confronto-{ident}.jpg"
                self.assertTrue(self.df.affianca(gem, [gem], dest), ident)
                self.assertGreater(dest.stat().st_size, 10_000)

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

    def test_libero_impaginato_male_si_legge_lo_stesso(self):
        """Grassetto, elenco numerato, titoli: S8 deve vedere comunque la *palla di fuoco*."""
        import coerenza_campagna as C
        blocco = self.S.genera("mago:7", 7, "controllore", 11)
        forme = {
            "grassetto": "**Prima del combattimento**: lancia *palla di fuoco*.\n**Morale**: fugge.",
            "numeri": "1. *Prima del combattimento*: lancia *palla di fuoco*.\n2. *Morale*: fugge.",
            "titoli": "### Prima del combattimento\nLancia *palla di fuoco*.\n### Morale\nFugge.",
            "elenco": "- *Prima del combattimento*: lancia *palla di fuoco*.\n- *Morale*: fugge.",
        }
        with tempfile.TemporaryDirectory() as t:
            for nome, testo in forme.items():
                tatt, motivo = self.S.valido_libero(testo)
                self.assertIsNotNone(tatt, f"{nome}: {motivo}")
                f = Path(t) / f"{nome}.md"
                f.write_text(f"# x\n\n{blocco}\n\n**Tattiche**\n{tatt}\n", encoding="utf-8")
                self.assertEqual(len(C.verifica_tattiche([f])["violazioni"]), 1, nome)
        self.assertEqual(self.S.valido_libero(" \n```\n")[0], None)

    def test_campi_non_testuali_non_fanno_cadere_la_misura(self):
        v = self.S.voci(self.S.genera("mago:7", 7, "controllore", 11))
        p = {"azione": "ragnatela", "bersaglio": 5, "perche": None}
        tatt, motivo = self.S.in_markdown(json.dumps({"prima": [p], "durante": [p], "morale": [p]}), v)
        self.assertIsNone(tatt)
        self.assertIn("non sono testo", motivo)
        p = {"azione": "ragnatela", "bersaglio": "il\ngruppo", "perche": "li ferma\n- e basta"}
        tatt, _ = self.S.in_markdown(json.dumps({"prima": [p], "durante": [p], "morale": [p]}), v)
        self.assertEqual(len(tatt.splitlines()), 3)

    def test_tetto_dei_token_e_troncate(self):
        """12 passi pieni devono stare nel tetto; una risposta troncata si conta."""
        self.assertGreaterEqual(self.S.GETTONI, 12 * 90)
        riga = {"braccio": "vincolato", "valida": False, "s8": 0, "fuori_lista": [], "menzioni": 0,
                "copertura": 0, "secondi": 1, "token": 1, "ns": 1, "troncata": True}
        s = self.S.riassumi([riga, dict(riga, braccio="libero", valida=True, s8=1, troncata=False)])
        self.assertEqual(s["vincolato"]["troncate"], 1)
        self.assertEqual(s["libero"]["troncate"], 0)
        self.assertFalse(s["migliora"])

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


OS_RELEASE = {
    "bazzite": 'NAME="Bazzite"\nID=bazzite\nID_LIKE="fedora"\nVERSION_ID="43"\n',
    "debian": 'PRETTY_NAME="Debian GNU/Linux 13 (trixie)"\nID=debian\nVERSION_ID="13"\n',
    "cachyos": 'NAME="CachyOS Linux"\nID=cachyos\nID_LIKE=arch\nBUILD_ID=rolling\n',
    "arch": 'NAME="EndeavourOS"\nID=endeavouros\nID_LIKE="arch"\n',
    "ubuntu": 'NAME="Ubuntu"\nID=ubuntu\nID_LIKE=debian\nVERSION_ID="24.04"\n',
}


def _bash(script: str, os_release: str, wsl: bool = False, extra: dict | None = None):
    import os
    with tempfile.TemporaryDirectory() as t:
        f = Path(t) / "os-release"
        f.write_text(os_release)
        v = Path(t) / "version"
        v.write_text("Linux version 6.6 (microsoft-standard-WSL2)" if wsl else "Linux version 6.17")
        env = {k: x for k, x in os.environ.items() if k != "RS_SENZA_BOX"}
        env.update(RS_OS_RELEASE=str(f), RS_PROC_VERSION=str(v), PROVE_DIR=t, **(extra or {}))
        return subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=env)


class TestKitMultiSistema(unittest.TestCase):
    """ADR-0136: lo stesso kit su Bazzite, Debian 13, CachyOS e WSL2 (Windows)."""

    def test_sistema_e_modo(self):
        attesi = {"bazzite": "bazzite box", "debian": "debian box", "cachyos": "cachyos box",
                  "arch": "arch box", "ubuntu": "ubuntu box"}
        for nome, testo in OS_RELEASE.items():
            r = _bash(f'. "{PROVE}/ospite.sh"; echo "$(rs_sistema) $(rs_modo)"', testo)
            self.assertEqual(r.stdout.strip(), attesi[nome], nome)
        r = _bash(f'. "{PROVE}/ospite.sh"; echo "$(rs_sistema) $(rs_modo)"', OS_RELEASE["ubuntu"], wsl=True)
        self.assertEqual(r.stdout.strip(), "wsl diretto")
        r = _bash(f'. "{PROVE}/ospite.sh"; echo "$(rs_modo)"; nel_box qualunque echo dentro',
                  OS_RELEASE["debian"], extra={"RS_SENZA_BOX": "1"})
        self.assertEqual(r.stdout.split(), ["diretto", "dentro"])

    def test_installa_per_sistema(self):
        attesi = {"bazzite": ["niente da installare", "distrobox create --name comfyui"],
                  "debian": ["apt-get install -y distrobox podman", "fedora-toolbox:43"],
                  "cachyos": ["pacman -S --needed --noconfirm distrobox podman", "chwd -a"],
                  "arch": ["pacman -S", "nvidia-open"]}
        for nome, frasi in attesi.items():
            r = _bash(f'"{PROVE}/installa.sh" --mostra --driver', OS_RELEASE[nome])
            self.assertEqual(r.returncode, 0, f"{nome}: {r.stderr}")
            for frase in frasi:
                self.assertIn(frase, r.stdout, nome)
        r = _bash(f'"{PROVE}/installa.sh" --mostra', OS_RELEASE["ubuntu"], wsl=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("ollama.com/install.sh", r.stdout)
        self.assertIn("nvidia-cuda-toolkit", r.stdout)
        self.assertIn("modo diretto: nessun box", r.stdout)
        self.assertNotIn("distrobox create", r.stdout)
        r = _bash(f'"{PROVE}/installa.sh" --mostra', 'ID=gentoo\n')
        self.assertEqual(r.returncode, 3)

    def test_manifesto_script_e_guida(self):
        m = json.loads((PROVE / "prove.json").read_text(encoding="utf-8"))
        ids = [p["id"] for p in m["prove"]]
        self.assertEqual(len(ids), len(set(ids)))
        guida = GUIDA.read_text(encoding="utf-8")
        sys.path.insert(0, str(PROVE))
        import verifica
        for p in m["prove"]:
            s = PROVE / p["script"]
            self.assertTrue(s.exists(), p["script"])
            self.assertIn(p["id"], verifica.CONTROLLI)
            self.assertIn(f"scripts/prove-4050/{p['script']}", guida)
        for f in ("kit.sh", "installa.sh", "installa-windows.ps1", "verifica.py"):
            self.assertIn(f"scripts/prove-4050/{f}", guida)

    def _podman_finto(self, t: Path, corpo: str) -> dict:
        (t / "bin").mkdir()
        for nome, testo in (("podman", corpo), ("distrobox", 'echo "ENTRATO $*"')):
            f = t / "bin" / nome
            f.write_text("#!/usr/bin/env bash\n" + testo + "\n")
            f.chmod(0o755)
        import os
        return {"PATH": f"{t / 'bin'}:{os.environ['PATH']}", "RS_BOX_ATTESA": "1", "STATO": str(t / "stato")}

    def test_box_spento_si_accende_senza_restare_appesi(self):
        """nel_box accende il box con podman e legge il log, invece di lasciarlo fare a distrobox enter."""
        podman = ('case "$1" in\n'
                  '  inspect) [ -f "$STATO" ] && echo true || echo false ;;\n'
                  '  start) touch "$STATO" ;;\n'
                  '  logs) echo container_setup_done ;;\n'
                  'esac')
        with tempfile.TemporaryDirectory() as t:
            extra = self._podman_finto(Path(t), podman)
            r = _bash(f'. "{PROVE}/ospite.sh"; nel_box whisper echo ciao', OS_RELEASE["bazzite"], extra=extra)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("avvio il box 'whisper'", r.stderr)
            self.assertIn("ENTRATO enter whisper -- echo ciao", r.stdout)
            # a box acceso non si aspetta niente
            r = _bash(f'. "{PROVE}/ospite.sh"; nel_box whisper echo ciao', OS_RELEASE["bazzite"], extra=extra)
            self.assertNotIn("avvio il box", r.stderr)
        with tempfile.TemporaryDirectory() as t:
            extra = self._podman_finto(Path(t), "exit 125")   # il box non esiste
            r = _bash(f'. "{PROVE}/ospite.sh"; nel_box whisper echo ciao', OS_RELEASE["bazzite"], extra=extra)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("non c'è", r.stderr)
            self.assertNotIn("ENTRATO", r.stdout)

    def test_box_rimasto_a_meta_si_riconosce(self):
        """2026-11-18: macchina spenta durante il primo avvio del box comfyui. installa lo rifà."""
        casi = {  # log del box, StartedAt, a metà?
            "finito": ("container_setup_done", "2026-11-18 23:40:00", False),
            "interrotto": ("Setting up host's nvidia integration...", "2026-11-18 23:40:00", True),
            "mai acceso": ("", "0001-01-01 00:00:00", True),
            "log spento": ("", "2026-11-18 23:40:00", False),
        }
        for nome, (log, avviato, atteso) in casi.items():
            podman = ('case "$1" in\n'
                      '  container) exit 0 ;;\n'
                      f'  logs) echo -n "{log}" ;;\n'
                      f'  inspect) echo "{avviato}" ;;\n'
                      'esac')
            with tempfile.TemporaryDirectory() as t:
                extra = self._podman_finto(Path(t), podman)
                r = _bash(f'. "{PROVE}/ospite.sh"; box_a_meta comfyui && echo META || echo INTERO',
                          OS_RELEASE["bazzite"], extra=extra)
                self.assertEqual(r.stdout.strip(), "META" if atteso else "INTERO", nome)
        with tempfile.TemporaryDirectory() as t:   # il box non c'è: niente da rifare
            extra = self._podman_finto(Path(t), "exit 1")
            r = _bash(f'. "{PROVE}/ospite.sh"; box_a_meta comfyui && echo META || echo INTERO',
                      OS_RELEASE["bazzite"], extra=extra)
            self.assertEqual(r.stdout.strip(), "INTERO")
        testo = (PROVE / "installa.sh").read_text(encoding="utf-8")
        self.assertLess(testo.index('box_a_meta "$b"'), testo.index("setup-distrobox.sh\"\n"))

    def test_pulisci_chiede_conferma_e_lascia_i_dati(self):
        """kit.sh pulisci toglie solo i box, e solo dopo un sì (o con --si)."""
        podman = ('case "$1" in\n'
                  '  container) [ "$3" = whisper ] && exit 1; exit 0 ;;\n'
                  '  rm) echo "PODMAN-RM $*" ;;\n'
                  'esac')
        with tempfile.TemporaryDirectory() as t:
            extra = self._podman_finto(Path(t), podman)
            dati = Path(t) / "dati"
            dati.mkdir()
            (dati / "modello.gguf").write_text("x")
            extra["LLM_DIR"] = str(dati)
            kit = f'"{PROVE}/kit.sh"'
            # senza terminale e senza --si non toglie niente
            r = _bash(f"{kit} pulisci < /dev/null", OS_RELEASE["bazzite"], extra=extra)
            self.assertEqual(r.returncode, 2, r.stderr)
            self.assertNotIn("ENTRATO rm", r.stdout)
            # con --si toglie i box che ci sono (whisper non c'è) e dice cosa resta
            r = _bash(f"{kit} pulisci --si", OS_RELEASE["bazzite"], extra=extra)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("tolto: llm-locale", r.stdout)
            self.assertIn("tolto: comfyui", r.stdout)
            self.assertNotIn("tolto: whisper", r.stdout)
            self.assertIn(str(dati), r.stdout)
            self.assertTrue((dati / "modello.gguf").exists())
            # un solo box, a scelta
            r = _bash(f"{kit} pulisci --si comfyui", OS_RELEASE["bazzite"], extra=extra)
            self.assertIn("tolto: comfyui", r.stdout)
            self.assertNotIn("tolto: llm-locale", r.stdout)
            # un nome che non è un box del kit non si tocca
            r = _bash(f"{kit} pulisci --si fedora-mio", OS_RELEASE["bazzite"], extra=extra)
            self.assertEqual(r.returncode, 2)
        # su WSL2 non ci sono box
        r = _bash(f'"{PROVE}/kit.sh" pulisci --si', OS_RELEASE["ubuntu"], wsl=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("non ci sono box", r.stdout)

    def test_terminale_rimesso_a_posto_dopo_il_server(self):
        """Primo giro sull'ASUS: spento Ollama il terminale restava grezzo e verifica.md usciva a scaletta."""
        testo = (PROVE / "kit.sh").read_text(encoding="utf-8")
        self.assertIn("stty sane", testo)
        # mai quando l'uscita va in un file o in una pipe; col log aperto il terminale è RS_FD_TERMINALE
        self.assertIn('local fd="${RS_FD_TERMINALE:-1}"', testo)
        self.assertIn('[ -t "$fd" ]', testo)
        corpo = testo[testo.index("ferma_server() {"):testo.index("\ntrap 'codice_kit")]
        self.assertIn("terminale_a_posto", corpo)
        self.assertEqual(testo.count('ferma_server; terminale_a_posto\n    python3 "$HERE/verifica.py"'), 2)
        # senza terminale non chiama stty e non fallisce
        with tempfile.TemporaryDirectory() as t:
            extra = self._podman_finto(Path(t), "exit 0")
            f = Path(t) / "bin" / "stty"
            f.write_text("#!/usr/bin/env bash\necho STTY-CHIAMATO\n")
            f.chmod(0o755)
            r = _bash(f'"{PROVE}/kit.sh" verifica', OS_RELEASE["bazzite"], extra=extra)
            self.assertNotIn("STTY-CHIAMATO", r.stdout)

    def test_script_windows_con_bom(self):
        """Windows PowerShell 5.1 legge un .ps1 senza BOM come ANSI e storpia le lettere accentate."""
        dati = (PROVE / "installa-windows.ps1").read_bytes()
        self.assertTrue(dati.startswith(b"\xef\xbb\xbf"))
        dati.decode("utf-8")
        self.assertIn(b"$LASTEXITCODE -ne 0", dati)

    def test_giro_oltre_la_mezzanotte_in_una_cartella(self):
        """kit.sh fissa il giorno alla partenza: le prove lanciate dopo mezzanotte scrivono lì."""
        r = _bash(f'. "{PROVE}/comune.sh"; echo "$GIORNO"', OS_RELEASE["debian"],
                  extra={"PROVE_GIORNO": "2026-11-17"})
        self.assertEqual(r.stdout.strip(), "2026-11-17")
        self.assertIn('export PROVE_GIORNO="$GIORNO"', (PROVE / "kit.sh").read_text(encoding="utf-8"))

    FLATPAK = 'NAME="Freedesktop SDK"\nVERSION_ID="25.08"\nID=org.freedesktop.platform\n'

    def test_sandbox_flatpak_ferma_subito(self):
        """Primo giro del DM (2026-11-18): dal terminale di un'app Flatpak il kit vedeva «altro 25.08»."""
        r = _bash(f'. "{PROVE}/ospite.sh"; rs_sistema', self.FLATPAK)
        self.assertEqual(r.stdout.strip(), "flatpak")
        for comando in ("kit.sh piano", "kit.sh esegui controlla", "installa.sh --mostra", "controlla.sh"):
            r = _bash(f'"{PROVE}/"{comando}', self.FLATPAK)
            self.assertEqual(r.returncode, 5, (comando, r.stdout, r.stderr))
            self.assertIn("sandbox Flatpak", r.stderr)
            self.assertIn("flatpak-spawn --host", r.stderr)
            self.assertNotIn("################", r.stdout)
        # il file della sandbox basta, anche con un os-release normale
        with tempfile.NamedTemporaryFile() as f:
            r = _bash(f'"{PROVE}/kit.sh" piano', OS_RELEASE["bazzite"], extra={"RS_FLATPAK_INFO": f.name})
            self.assertEqual(r.returncode, 5)
        r = _bash(f'"{PROVE}/kit.sh" piano', OS_RELEASE["bazzite"])
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_piano_senza_risultati(self):
        r = _bash(f'"{PROVE}/kit.sh" piano', OS_RELEASE["debian"])
        self.assertEqual(r.returncode, 0, r.stderr)
        for p in json.loads((PROVE / "prove.json").read_text(encoding="utf-8"))["prove"]:
            self.assertRegex(r.stdout, rf"{p['id']}\s+\d+\s+non fatta")


class TestVerifica(unittest.TestCase):
    """verifica.py su risultati finti: cosa conta come ok, ko, da completare, non fatta."""

    def setUp(self):
        sys.path.insert(0, str(PROVE))
        import verifica
        self.v = verifica
        self.m = json.loads((PROVE / "prove.json").read_text(encoding="utf-8"))
        self.t = tempfile.TemporaryDirectory()
        self.r = Path(self.t.name)

    def tearDown(self):
        self.t.cleanup()

    def scrivi(self, rel: str, testo) -> None:
        f = self.r / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(testo if isinstance(testo, str) else json.dumps(testo), encoding="utf-8")

    GPU = "## prima\nname, memory.used [MiB], memory.total [MiB]\nNVIDIA GeForce RTX 4050 Laptop GPU, 5200 MiB, 6141 MiB, 90 %, 70\n"

    def test_tutto_non_fatto(self):
        e = self.v.verifica(self.r, self.m)
        self.assertTrue(all(x["stato"] == "non fatta" for x in e.values()))

    def test_prova_lanciata_e_mai_partita_e_ko(self):
        """Il kit ha registrato un'uscita con errore e non c'è nessun risultato: ko, non «non fatta»."""
        self.scrivi("kit.tsv", "lettore-coerenza\t3\t0\t22:00:00\n")
        e = self.v.verifica(self.r, self.m)
        self.assertEqual(e["lettore-coerenza"]["stato"], "ko")
        self.assertIn("non è partita", e["lettore-coerenza"]["note"][0])
        self.assertEqual(e["prosa"]["stato"], "non fatta")

    def test_lettore_completo_e_interrotto(self):
        self.scrivi("lettore-coerenza/esito.txt", "modello: qwen2.5:7b\ndomande: 3\nminuti: 4\n")
        self.scrivi("lettore-coerenza/gpu.txt", self.GPU)
        self.scrivi("lettore-coerenza/ollama-ps.json", {"models": [{"size": 100, "size_vram": 100}]})
        self.scrivi("lettore-coerenza/risposte-qwen2.5-7b.json", {"a": "SÌ", "b": "NO", "c": "NO"})
        e = self.v.verifica(self.r, self.m)["lettore-coerenza"]
        self.assertEqual(e["stato"], "ok", e)
        self.assertEqual(e["numeri"]["in_vram"], 1.0)
        self.scrivi("lettore-coerenza/risposte-qwen2.5-7b.json", {"a": "SÌ"})
        self.assertEqual(self.v.verifica(self.r, self.m)["lettore-coerenza"]["stato"], "ko")

    def test_trascrizione_sulla_cpu_e_ko(self):
        base = "trascrizione-gpu/"
        self.scrivi(base + "esito.txt", "backend: vulkan\nsecondi: 60\nvolte_tempo_reale: 10.8\n")
        for f in ("grezza.txt", "riferimento.txt", "whisper.log"):
            self.scrivi(base + f, "le autorità locali")
        self.scrivi(base + "dispositivo.txt", "ggml_vulkan: 0 = NVIDIA GeForce RTX 4050 Laptop GPU\n")
        self.assertEqual(self.v.verifica(self.r, self.m)["trascrizione-gpu"]["stato"], "ok")
        self.scrivi(base + "misura.txt", '{"errori": 23, "wer": 0.025}')
        self.assertEqual(self.v.verifica(self.r, self.m)["trascrizione-gpu"]["numeri"]["wer"], 0.025)
        self.assertEqual(self.v.verifica(self.r, self.m)["trascrizione-gpu"]["stato"], "ok")
        self.scrivi(base + "misura.txt", '{"errori": 87, "wer": 0.086}')
        self.assertEqual(self.v.verifica(self.r, self.m)["trascrizione-gpu"]["stato"], "ko")
        self.scrivi(base + "misura.txt", '{"wer": 0.02}')
        self.scrivi(base + "dispositivo.txt", "no GPU found\n")
        e = self.v.verifica(self.r, self.m)["trascrizione-gpu"]
        self.assertEqual(e["stato"], "ko")
        self.assertIn("CPU", e["note"][0])

    def test_trascrizione_sulla_scheda_integrata_e_ko(self):
        """Il log elenca la NVIDIA ma la sua memoria non sale: ha lavorato un'altra scheda."""
        base = "trascrizione-gpu/"
        for f in ("grezza.txt", "riferimento.txt", "whisper.log"):
            self.scrivi(base + f, "le autorità locali")
        self.scrivi(base + "dispositivo.txt",
                    "ggml_vulkan: 0 = Intel(R) Graphics\nggml_vulkan: 1 = NVIDIA GeForce RTX 4050 Laptop GPU\n")
        self.scrivi(base + "esito.txt", "backend: vulkan\nvram_prima_mib: 300\nvram_picco_mib: 1400\n")
        e = self.v.verifica(self.r, self.m)["trascrizione-gpu"]
        self.assertEqual((e["stato"], e["numeri"]["vram_salita_mib"]), ("ok", 1100), e)
        self.scrivi(base + "esito.txt", "backend: vulkan\nvram_prima_mib: 300\nvram_picco_mib: 310\n")
        e = self.v.verifica(self.r, self.m)["trascrizione-gpu"]
        self.assertEqual(e["stato"], "ko")
        self.assertIn("un'altra scheda", e["note"][0])
        # senza nvidia-smi i due campi sono vuoti: il controllo non scatta
        self.scrivi(base + "esito.txt", "backend: vulkan\nvram_prima_mib: \nvram_picco_mib: \n")
        self.assertEqual(self.v.verifica(self.r, self.m)["trascrizione-gpu"]["stato"], "ok")

    def test_drappo_e_codice_del_kit(self):
        self.scrivi("drappo-flux/esito.txt", "tavole: il-drappo\nsemi: 2\n")
        self.scrivi("drappo-flux/confronto.html", "<html>")
        self.scrivi("drappo-flux/flux/seme-0/il-drappo.png", "png")
        self.scrivi("drappo-flux/flux/seme-1/il-drappo.png", "png")
        righe = [{"id": "il-drappo", "seme": s, "esito": "ok", "vram_picco_mib": 5800,
                  "ram_comfyui_picco_mib": 9000, "file": f"flux/seme-{s}/il-drappo.png"} for s in (0, 1)]
        self.scrivi("drappo-flux/riepilogo.json", {"immagini": righe, "cpu": False, "minuti_totali": 9})
        e = self.v.verifica(self.r, self.m)["drappo-flux"]
        self.assertEqual(e["stato"], "ok", e)
        self.assertEqual(e["numeri"]["vram_picco_mib"], 5800)
        self.scrivi("kit.tsv", "drappo-flux\t1\t9\t22:00:00\n")
        self.assertEqual(self.v.verifica(self.r, self.m)["drappo-flux"]["stato"], "ko")

    def test_prosa_da_completare(self):
        self.scrivi("prosa/esito.txt", "modello: gemma4:12b-it-qat\nminuti: 80\n")
        self.scrivi("prosa/gpu.txt", self.GPU)
        self.scrivi("prosa/L-gemma412bitqat-1/S02.md", "testo")
        self.scrivi("prosa/foglio-gemma412bitqat-1.md", "Preferito: 1\nPreferito:\n")
        self.assertEqual(self.v.verifica(self.r, self.m)["prosa"]["stato"], "da completare")
        self.scrivi("prosa/foglio-gemma412bitqat-1.md", "Preferito: 1\nPreferito: =\n")
        self.assertEqual(self.v.verifica(self.r, self.m)["prosa"]["stato"], "ok")

    def test_schede_e_main(self):
        s = {"schede": 2, "ripetizioni": 1, "migliora": False,
             "libero": {"risposte": 2, "valide": 2}, "vincolato": {"risposte": 1, "valide": 1}}
        self.scrivi("schede-vincolate/esito.txt", "modello: qwen2.5:7b\n")
        self.scrivi("schede-vincolate/gpu.txt", self.GPU)
        self.scrivi("schede-vincolate/risposte.json", {})
        self.scrivi("schede-vincolate/misure.json", {"sintesi": s, "righe": []})
        self.assertEqual(self.v.verifica(self.r, self.m)["schede-vincolate"]["stato"], "ko")
        self.assertEqual(self.v.main([str(self.r), "--quiet"]), 1)
        self.assertTrue((self.r / "verifica.md").exists())


if __name__ == "__main__":
    unittest.main()
