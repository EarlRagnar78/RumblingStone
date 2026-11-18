#!/usr/bin/env python3
"""leggi_ollama.py — il lettore del RAG su una GPU locale, via Ollama, solo stdlib.

Serve per rifare la lettura di estrai_rag.py su un'altra macchina (la RTX 4050
dell'ASUS, la Dell) senza torch né transformers: il recupero resta quello del
container, cambia solo chi risponde SÌ/NO.

  1. nel container:  python estrai_rag.py --radice DIR --out X.json --k 20 \
                       --modello ollama:qwen2.5:7b --domande-out misure/domande-ollama.json
                     (già fatto il 2026-11-15: 636 domande, 556 sul repo e 80 sui mutanti)
  2. sulla macchina: python3 leggi_ollama.py misure/domande-ollama.json --modello qwen2.5:7b \
                       --out misure/risposte-qwen2.5-7b.json
  3. nel container:  python estrai_rag.py ... --modello ollama:qwen2.5:7b \
                       --cache misure/cache-llm.json --unisci misure/risposte-qwen2.5-7b.json

Greedy (temperature 0, seed 0), al massimo 3 token, come con transformers. Le
risposte si salvano ogni 20 e all'uscita, anche su errore: una corsa interrotta
riparte da dove era.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path


def chiedi(url: str, modello: str, sistema: str, utente: str, timeout: float) -> str:
    corpo = json.dumps({"model": modello, "stream": False,
                        "messages": [{"role": "system", "content": sistema},
                                     {"role": "user", "content": utente}],
                        "options": {"temperature": 0, "seed": 0, "num_predict": 3}}).encode()
    req = urllib.request.Request(f"{url}/api/chat", data=corpo, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)["message"]["content"].strip()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("domande", type=Path)
    ap.add_argument("--modello", required=True, help="nome Ollama, per esempio qwen2.5:7b")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--url", default="http://127.0.0.1:11434")
    ap.add_argument("--timeout", type=float, default=300)
    a = ap.parse_args(argv)
    domande = json.loads(a.domande.read_text(encoding="utf-8"))
    risposte = json.loads(a.out.read_text(encoding="utf-8")) if a.out.exists() else {}
    t0, nuove = time.time(), 0
    try:
        for d in domande:
            # la chiave è quella della cache di estrai_rag.py per «ollama:<modello>»: così lo stesso
            # file di domande serve per qualunque modello, non solo per quello con cui è stato scritto
            h = hashlib.sha256(("ollama:" + a.modello + d["utente"]).encode()).hexdigest()
            if h in risposte:
                continue
            risposte[h] = chiedi(a.url, a.modello, d["sistema"], d["utente"], a.timeout)
            nuove += 1
            if nuove % 20 == 0:
                a.out.write_text(json.dumps(risposte, ensure_ascii=False), encoding="utf-8")
                sec = time.time() - t0
                print(f"  {len(risposte)}/{len(domande)}  {sec / nuove:.2f} s a domanda", file=sys.stderr, flush=True)
    finally:  # anche su errore del server o Ctrl-C: le risposte già avute non si perdono
        if nuove:
            a.out.write_text(json.dumps(risposte, ensure_ascii=False), encoding="utf-8")
    sec = time.time() - t0
    print(f"✓ {len(risposte)}/{len(domande)} risposte, {nuove} nuove in {sec:.0f} s"
          + (f" ({sec / nuove:.2f} s a domanda)" if nuove else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
