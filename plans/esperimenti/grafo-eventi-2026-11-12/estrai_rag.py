#!/usr/bin/env python3
"""estrai_rag.py — l'estrattore con recupero (RAG) per le stesse regole di grafo.py.

Il collo di bottiglia misurato da ADR-0125 è leggere il fatto nella prosa: una
parafrasi d'autore sfugge alle parole chiave. Qui il fatto si cerca come lo
cercherebbe un sistema RAG:

1. **recupero**: per ogni coppia (PNG, fatto) che il grafo rende verificabile, e
   per ogni fatto con un'origine dopo il Day 0, si interrogano solo le frasi delle
   scene in cui la regola potrebbe scattare (il giorno della scena lo dice il
   grafo). Ricerca ibrida: BM25 più embedding multilingue (intfloat/
   multilingual-e5-small, MIT), fusione per rango reciproco, prime K frasi;
2. **lettura**: un modello aperto locale (Qwen/Qwen2.5-3B-Instruct, Apache-2.0,
   su CPU, decodifica greedy, quindi ripetibile) risponde SÌ o NO alla domanda
   «in questa frase, il PNG mostra di sapere il fatto?»;
3. **regole**: le citazioni accettate vanno alle stesse regole deterministiche
   di grafo.py (T0, T1 anche per catena, T3). Il modello estrae, non giudica.

La descrizione del PNG viene da state.yaml (nome e agenda in `villain`), non è
scritta per i mutanti; la descrizione del fatto è una riga per fatto in FATTI_IT.

Uso (nel venv con torch e transformers)
  python estrai_rag.py --radice DIR --out CITAZIONI.json [--k 5] [--cache CACHE.json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time
from pathlib import Path

import yaml

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))
import grafo  # noqa: E402

FATTI_IT = {
    "F_custodi": "il gruppo dei quattro eroi ha il titolo di Custodi Eterni di Hammerfist, dato dal re dopo l'assedio",
    "F_guerrieri": "il gruppo ha liberato i Guerrieri di Cristallo nella miniera",
    "F_gemme": "il gruppo possiede tutte e tre le gemme della Corona",
    "F_corona": "il gruppo possiede la Corona di Adamantio",
    "F_artefatti_quali": "quali artefatti precisi porta il gruppo (Aegis Fang, la Corona, l'Anello, la Collana)",
    "F_sal_vatore": "la vera identità temporale di Salvatore (Vatore)",
    "F_anello": "Artemis porta l'Anello dell'Illuminazione Caotica",
    "F_bracieri": "Tordek porta i Bracieri Gemelli, chiavi planari della Forgia Eterna",
    "F_lorana_viva": "la capitana Lorana è viva e si trova a Rethmar",
    "F_mira_impostora": "la figlia di Lorana, Mira, è stata uccisa e sostituita da un'aranea",
    "F_rete_varis": "la rete delle statue viventi porta a Varis, Sal e il Collezionista",
    "F_xal_piano": "il piano d'invasione separato di Xal'thor",
    "F_thorik_risorto": "Thorik è morto ed è stato riportato in vita al Guado",
    "F_seme_porta": "l'Orbe delle Otto Porte di Dauth emette un Seme di Porta estraibile",
    "F_aeleth_morto": "Aeleth Verdebronzo è morto",
}


def passaggi(radice: Path, g: dict) -> list[dict]:
    out = []
    for p in grafo.file_corpus(radice):
        rel = str(p.relative_to(radice))
        w = grafo.finestra(rel, g)
        if not w:
            continue
        fence = False
        for n, riga in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if riga.lstrip().startswith("```"):
                fence = not fence
                continue
            if fence or grafo.cc.STORICO_RIGA.search(riga) or grafo.cc.HEADING.match(riga):
                continue
            for fr in re.split(r"(?<=[.;!?])\s+", riga):
                t = re.sub(r"[*_`>|#]", " ", fr).strip()
                if len(t) >= 25:
                    out.append({"file": rel, "riga": n, "testo": t[:400], "lo": w[0], "hi": w[1]})
    return out


def descr_png(state: dict) -> dict[str, str]:
    d = {p["id"]: p["nome"] for p in state.get("png") or []}
    for v in state.get("villain") or []:
        if v.get("png_id") in d:
            agenda = re.sub(r"[*`]", "", str(v.get("agenda") or ""))[:160]
            d[v["png_id"]] = f"{re.sub(r'[*`]', '', str(v['villain']))[:120]}; {agenda}"
    return d


def interrogazioni(g: dict, state: dict) -> list[dict]:
    """Le domande che il grafo rende verificabili, con la condizione sulla scena."""
    da, _ = grafo.chiusura(g)
    orig = {f: v["origine"] for f, v in g["fatti"].items()}
    dp = descr_png(state)
    q = []
    for n in g["non_sa"]:
        q.append({"png": n["png"], "fatto": n["fatto"], "regola": "T3",
                  "scena": lambda lo, hi, fino=n.get("fino_a", grafo.INF): lo < fino})
    negati = {(n["png"], n["fatto"]) for n in g["non_sa"]}
    for (p, f), giorno in da.items():
        if giorno > 0 and (p, f) not in negati:
            q.append({"png": p, "fatto": f, "regola": "T1", "scena": lambda lo, hi, gg=giorno: hi < gg})
    for f, o in orig.items():
        if o > 0:
            q.append({"png": None, "fatto": f, "regola": "T0", "scena": lambda lo, hi, oo=o: hi < oo})
    for x in q:
        chi = dp.get(x["png"], x["png"]) if x["png"] else None
        x["chi"] = chi
        x["testo"] = (f"{chi} sa che {FATTI_IT[x['fatto']]}" if chi
                      else f"come cosa già avvenuta: {FATTI_IT[x['fatto']]}")
    return q


def _tok(s: str) -> list[str]:
    return re.findall(r"[a-zà-ÿ']{3,}", s.lower())


class Bm25:
    def __init__(self, docs: list[list[str]], k1=1.5, b=0.75):
        self.docs, self.k1, self.b = docs, k1, b
        self.avg = sum(map(len, docs)) / max(1, len(docs))
        df: dict[str, int] = {}
        for d in docs:
            for t in set(d):
                df[t] = df.get(t, 0) + 1
        self.idf = {t: math.log(1 + (len(docs) - n + 0.5) / (n + 0.5)) for t, n in df.items()}
        self.tf = [{} for _ in docs]
        for i, d in enumerate(docs):
            for t in d:
                self.tf[i][t] = self.tf[i].get(t, 0) + 1

    def punteggi(self, q: list[str], idx: list[int]) -> dict[int, float]:
        out = {}
        for i in idx:
            s = 0.0
            L = len(self.docs[i])
            for t in q:
                f = self.tf[i].get(t)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * L / self.avg))
            out[i] = s
        return out


SISTEMA = "Sei un lettore attento di testi di una campagna di D&D. Rispondi solo SÌ o NO."


def domanda(x: dict, p: dict) -> str:
    """Il testo della domanda al lettore: identico per transformers e per Ollama."""
    if x["png"]:
        return (f"Personaggio: {x['chi']}\nFatto: {FATTI_IT[x['fatto']]}\n\nFrase: «{p['testo']}»\n\n"
                f"Secondo questa frase, il personaggio sa già il fatto, o agisce o parla come chi lo sa? "
                f"Rispondi solo SÌ o NO.")
    return (f"Fatto: {FATTI_IT[x['fatto']]}\n\nFrase: «{p['testo']}»\n\n"
            f"Questa frase presenta il fatto come già vero nel momento della scena (non come futuro, "
            f"ipotesi o rimando)? Rispondi solo SÌ o NO.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--cache", type=Path, default=QUI / "misure" / "cache-llm.json")
    ap.add_argument("--modello", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--embed", default="intfloat/multilingual-e5-small")
    ap.add_argument("--domande-out", type=Path,
                    help="scrive le domande non in cache ed esce (per leggi_ollama.py su un'altra macchina)")
    ap.add_argument("--unisci", type=Path, nargs="*", default=[],
                    help="risposte di leggi_ollama.py da mettere in cache prima della lettura")
    a = ap.parse_args(argv)

    import torch
    from sentence_transformers import SentenceTransformer
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.set_num_threads(4)
    torch.manual_seed(0)

    g = grafo.carica()
    state = yaml.safe_load((grafo.REPO / "campaign" / "state.yaml").read_text(encoding="utf-8"))
    P = passaggi(a.radice, g)
    Q = interrogazioni(g, state)
    t0 = time.time()
    emb = SentenceTransformer(a.embed, device="cpu")
    ve = emb.encode([f"passage: {p['testo']}" for p in P], batch_size=64, normalize_embeddings=True,
                    show_progress_bar=False)
    vq = emb.encode([f"query: {x['testo']}" for x in Q], normalize_embeddings=True, show_progress_bar=False)
    bm = Bm25([_tok(p["testo"]) for p in P])
    t_rec = time.time() - t0

    cand = []
    for qi, x in enumerate(Q):
        idx = [i for i, p in enumerate(P) if x["scena"](p["lo"], p["hi"])]
        if not idx:
            continue
        sb = bm.punteggi(_tok(x["testo"]), idx)
        se = {i: float(ve[i] @ vq[qi]) for i in idx}
        rb = {i: r for r, i in enumerate(sorted(idx, key=lambda i: -sb[i]))}
        re_ = {i: r for r, i in enumerate(sorted(idx, key=lambda i: -se[i]))}
        rrf = sorted(idx, key=lambda i: -(1 / (60 + rb[i]) + 1 / (60 + re_[i])))
        for i in rrf[:a.k]:
            cand.append((qi, i))

    cache = json.loads(a.cache.read_text(encoding="utf-8")) if a.cache.exists() else {}
    for f in a.unisci:
        cache |= json.loads(f.read_text(encoding="utf-8"))
    if a.domande_out:
        da_fare = {}
        for qi, i in cand:
            dom = domanda(Q[qi], P[i])
            h = hashlib.sha256((a.modello + dom).encode()).hexdigest()
            if h not in cache:
                da_fare[h] = {"h": h, "sistema": SISTEMA, "utente": dom}
        old = json.loads(a.domande_out.read_text(encoding="utf-8")) if a.domande_out.exists() else []
        tutte = {d["h"]: d for d in old} | da_fare
        a.domande_out.write_text(json.dumps(list(tutte.values()), ensure_ascii=False, indent=0),
                                 encoding="utf-8")
        print(f"✓ {len(da_fare)} domande nuove, {len(tutte)} nel file {a.domande_out}")
        return 0
    if a.modello.startswith("ollama:") and any(
            hashlib.sha256((a.modello + domanda(Q[qi], P[i])).encode()).hexdigest() not in cache
            for qi, i in cand):
        sys.exit("ERRORE: risposte di Ollama mancanti in cache: prima --domande-out, poi leggi_ollama.py")
    tok = mod = None
    cit, letti, nuovi, traccia = [], 0, 0, []
    t1 = time.time()
    for qi, i in cand:
        x, p = Q[qi], P[i]
        dom = domanda(x, p)
        h = hashlib.sha256((a.modello + dom).encode()).hexdigest()
        if h not in cache:
            if mod is None:
                tok = AutoTokenizer.from_pretrained(a.modello)
                mod = AutoModelForCausalLM.from_pretrained(a.modello, torch_dtype=torch.bfloat16)
                mod.eval()
            msgs = [{"role": "system", "content": SISTEMA}, {"role": "user", "content": dom}]
            enc = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt",
                                          return_dict=True)
            with torch.no_grad():
                o = mod.generate(**enc, max_new_tokens=3, do_sample=False)
            cache[h] = tok.decode(o[0][enc["input_ids"].shape[1]:], skip_special_tokens=True).strip()
            nuovi += 1
            if nuovi % 20 == 0:
                a.cache.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
                print(f"  {nuovi} letture nuove, {time.time() - t1:.0f} s", file=sys.stderr, flush=True)
        letti += 1
        traccia.append({"domanda": x["regola"], "png": x["png"], "fatto": x["fatto"], "file": p["file"],
                        "riga": p["riga"], "risposta": cache[h]})
        if cache[h].upper().startswith("S"):
            cit.append({"png": x["png"], "fatto": x["fatto"], "giorno_da": p["lo"], "giorno_a": p["hi"],
                        "file": p["file"], "riga": p["riga"], "testo": p["testo"][:240],
                        "estrattore": "rag", "domanda": x["regola"]})
    a.cache.parent.mkdir(parents=True, exist_ok=True)
    a.cache.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    viol = grafo.regole_python(g, cit)
    a.out.write_text(json.dumps({"citazioni": cit, "violazioni": viol, "letture": traccia, "misure": {
        "passaggi": len(P), "domande": len(Q), "candidati": len(cand), "letture_llm": letti,
        "letture_nuove": nuovi, "secondi_recupero": round(t_rec, 1),
        "secondi_lettura": round(time.time() - t1, 1), "k": a.k, "modello": a.modello, "embed": a.embed}},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ {len(P)} passaggi, {len(Q)} domande, {len(cand)} candidati, {len(cit)} citazioni, "
          f"{len(viol)} violazioni")
    return 0


if __name__ == "__main__":
    sys.exit(main())
