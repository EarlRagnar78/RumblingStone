"""Tratti esterni per il modello di preferenza della pipeline di prosa
(richiesta del thread della #264, 2026-10-23): per ogni coppia di
pipeline/VOTI.json, sulla vincente e sulla perdente,

1. le misure di `misura_sintassi.analizza` con il parser Stanza (spacy-stanza);
2. la perplessità media per token con Qwen2.5-0.5B (Apache 2.0, multilingue),
   segnale grezzo di «suona naturale» contro «suona tradotto». Minerva-350M
   (italiano, Apache 2.0) chiede il login su Hugging Face; il GPT-2 italiano
   di GroNLP non dichiara licenza.

    HF_HUB_DISABLE_XET=1 python3 .../stanza/tratti_esterni.py VOTI.json > tratti-esterni.json

I modelli stanno nelle cache (~/.cache/stanza, ~/.cache/huggingface), mai nel repo.
"""
import json
import math
import sys

from confronta import ms, stanza_nlp

LM = "Qwen/Qwen2.5-0.5B"
NUMERICHE = ("parole", "frasi", "sogg_preverbale", "agg_complesso", "stare_gerundio",
             "pron_soggetto", "calchi", "possessivi_corpo", "profondita_max",
             "profondita_media", "livelli_max", "frasi_oltre2%", "lungh_dip",
             "mattr_lemmi", "rip_interna%")


def perplessita(testi):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(LM)
    lm = AutoModelForCausalLM.from_pretrained(LM, torch_dtype=torch.float32).eval()
    out = []
    for t in testi:
        ids = tok(t, return_tensors="pt").input_ids[:, :1024]
        with torch.no_grad():
            nll = lm(ids, labels=ids).loss.item()
        out.append({"ppl": round(math.exp(nll), 2), "nll_token": round(nll, 4),
                    "token": int(ids.shape[1])})
    return out


def main():
    coppie = json.load(open(sys.argv[1], encoding="utf-8"))["coppie"]
    nlp = stanza_nlp()
    testi = [(c["id"], ruolo, c[ruolo]) for c in coppie for ruolo in ("vincente", "perdente")]
    ppl = perplessita([t for _, _, t in testi])
    res = {"_nota": f"Stanza 1.15 (combined_charlm) via spacy-stanza; perplessità con {LM}. "
                    "Rigenera: tratti_esterni.py in sintassi/stanza/ della PR #270."}
    for (cid, ruolo, testo), p in zip(testi, ppl):
        m = ms.analizza(testo, nlp)
        res.setdefault(cid, {})[ruolo] = {**{"stanza_" + k: m[k] for k in NUMERICHE}, **p}
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
