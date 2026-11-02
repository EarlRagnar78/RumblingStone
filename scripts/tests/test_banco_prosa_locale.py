"""Test di banco_prosa_locale.py (ADR-0089, I2): tutto cio' che gira senza il modello."""
from __future__ import annotations

import http.server
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import banco_prosa_locale as bl  # noqa: E402


def _casi():
    return json.loads(bl.CASI.read_text(encoding="utf-8"))["casi"]


class TestEstratto(unittest.TestCase):
    def test_il_titolo_che_comincia_col_punto_vince(self):
        testo = ("# M\n### A.1 · Skullcrusher (Scena 11)\nstatistiche\n"
                 "### SCENA 11 — Il duello\nla scena\n### SCENA 12 — Dopo\naltro\n")
        e = bl.estratto(testo, "Scena 11", 1000)
        assert e.startswith("### SCENA 11"), e
        assert "SCENA 12" not in e

    def test_senza_punto_l_inizio_del_file_entro_il_tetto(self):
        assert bl.estratto("x" * 50, None, 10) == "x" * 10

    def test_i_casi_veri_trovano_la_loro_scena(self):
        trovati = {c["id"]: bl.componi(c, "pieno", 12000)[1] for c in _casi()}
        for cid, titolo in (("S01", "ZONA 2"), ("S02", "SCENA 11"), ("S03", "SCENA 7"),
                            ("S06", "SCENA 3"), ("S09", "SCENA 4")):
            assert f"### {titolo}" in trovati[cid], cid


class TestComposizione(unittest.TestCase):
    def test_gioco_e_documenti_non_si_mescolano(self):
        # ADR-0035: una sola delle due skill di prosa per volta.
        per_id = {c["id"]: c for c in _casi()}
        s_gioco, _ = bl.componi(per_id["S01"], "pieno", 100)
        s_doc, _ = bl.componi(per_id["S05"], "pieno", 100)
        gioco, doc = "===== skills/rumblingstone-narrative-style/", "===== skills/rumblingstone-prosa-documenti/"
        assert gioco in s_gioco and doc not in s_gioco
        assert doc in s_doc and gioco not in s_doc

    def test_contesto_ridotto_e_piu_corto(self):
        c = _casi()[0]
        assert len(bl.componi(c, "ridotto", 100)[0]) < len(bl.componi(c, "pieno", 100)[0])


class _Finto(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        corpo = json.dumps({"choices": [{"message": {"content": "<think>x</think>Testo."}}],
                            "usage": {"completion_tokens": 1}}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(corpo)


class TestServizio(unittest.TestCase):
    def test_pulisci_il_pensiero_di_gemma_anche_vuoto(self):
        assert bl.pulisci("<|channel>thought\n<channel|>Il testo.") == "Il testo."
        assert bl.pulisci("<|channel>thought\npenso\n<channel|>\n\nIl testo.") == "Il testo."

    def test_chiama_toglie_il_ragionamento(self):
        srv = http.server.HTTPServer(("127.0.0.1", 0), _Finto)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            testo, uso, fine = bl.chiama(f"http://127.0.0.1:{srv.server_port}/v1", "m", "s",
                                         "u", 0.7, 1, 10, 10)
        finally:
            srv.shutdown()
        assert testo == "Testo.\n" and uso == {"completion_tokens": 1} and fine is None

    def test_senza_servizio_esce_3_e_non_scrive(self):
        with tempfile.TemporaryDirectory() as d:
            vecchio = bl.CORSE
            bl.CORSE = Path(d)
            try:
                rc = bl.main(["corsa", "--url", "http://127.0.0.1:9/v1", "--modello", "m",
                              "--insieme", "verifica", "--timeout", "2"])
            finally:
                bl.CORSE = vecchio
            assert rc == 3
            assert list(Path(d).iterdir()) == []


class TestGuasti(unittest.TestCase):
    """I numeri veri della prima corsa sull'ASUS (2026-10-10)."""

    def test_prompt_tagliato_a_meta(self):
        # S02: 86.587 caratteri, il server ne ha contati 12.291 token
        assert bl.avvisi(86587, {"prompt_tokens": 12291}, "stop", "x")
        # S01: 75.236 caratteri, 21.931 token: intero
        assert not bl.avvisi(75236, {"prompt_tokens": 21931}, "stop", "x")

    def test_risposta_al_tetto_o_vuota(self):
        assert bl.avvisi(100, {}, "length", "x") == ["risposta interrotta al tetto di token"]
        assert bl.avvisi(100, {}, "stop", "\n") == ["risposta vuota"]

    def test_il_contesto_corto_ferma_la_corsa_prima(self):
        rc = bl.main(["corsa", "--url", "http://127.0.0.1:9/v1", "--modello", "m",
                      "--caso", "S02", "--ctx", "24576"])
        assert rc == 4

    def test_una_corsa_guasta_resta_fuori_dal_voto(self):
        class Vuoto(_Finto):
            def do_POST(self):
                self.rfile.read(int(self.headers["Content-Length"]))
                corpo = json.dumps({"choices": [{"message": {"content": ""},
                                                 "finish_reason": "length"}]}).encode()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(corpo)
        srv = http.server.HTTPServer(("127.0.0.1", 0), Vuoto)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        with tempfile.TemporaryDirectory() as d:
            vecchie = bl.CORSE, bl.PROVE
            bl.CORSE, bl.PROVE = Path(d) / "corse", Path(d) / "prove"
            try:
                rc = bl.main(["corsa", "--url", f"http://127.0.0.1:{srv.server_port}/v1",
                              "--modello", "m", "--insieme", "verifica"])
                assert rc == 5
                assert not bl.CORSE.exists()
                meta = json.loads((bl.PROVE / "L-locale-1" / "corsa.json").read_text())
                assert set(meta["fuori_dal_voto"]) == {"S06", "S07", "S08", "S09", "S10"}
            finally:
                bl.CORSE, bl.PROVE = vecchie
                srv.shutdown()

    def test_i_casi_veri_stanno_in_32k(self):
        for c in _casi():
            assert bl.stima_token(*bl.componi(c, "pieno", 12000)) + 3000 <= 32768, c["id"]


class TestEsito(unittest.TestCase):
    def test_wilson(self):
        lo, hi = bl.wilson(10, 10)
        assert round(lo, 2) == 0.72 and hi == 1.0
        assert round(bl.wilson(0, 10)[1], 2) == 0.28

    def test_kappa_e_il_paradosso(self):
        # Preferenze sbilanciate: 80% d'accordo e κ zero. Per questo si stampano tutti e due.
        assert bl.kappa(["a"] * 10, ["a"] * 8 + ["b"] * 2) == 0.0
        assert bl.kappa(["a", "b", "a", "b"], ["a", "b", "a", "b"]) == 1.0

    def test_dal_foglio_alla_condizione(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "f.md"
            f.write_text("## S01 · x\nPreferito: 2\n## S02 · y\nPreferito: =\n", encoding="utf-8")
            chiave = {"ordine": {"S01": ["b", "a"], "S02": ["a", "b"]}}
            assert bl.in_condizione(bl.leggi_preferenze(f), chiave) == {"S01": "a", "S02": "="}


if __name__ == "__main__":
    unittest.main()
