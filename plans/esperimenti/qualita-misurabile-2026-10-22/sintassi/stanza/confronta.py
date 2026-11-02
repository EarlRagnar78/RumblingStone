"""spaCy (it_core_news_md) contro Stanza (it, combined) sulle misure di
scripts/misura_sintassi.py: stessi rilevatori, cambia solo il parser.

    python3 plans/esperimenti/qualita-misurabile-2026-10-22/sintassi/stanza/confronta.py base   > RILIEVI.json
    python3 plans/esperimenti/qualita-misurabile-2026-10-22/sintassi/stanza/confronta.py coppie COPPIE.json > CALIBRAZIONE.txt

Stanza entra attraverso spacy-stanza, che ne fa un Doc di spaCy: i rilevatori
non cambiano di una riga. Il modello Stanza (Apache 2.0) sta in ~/.cache/stanza,
mai nel repo. `STANZA_PACKAGE=default_accurate` prova la variante transformer
(ELECTRA italiano); dietro il proxy serve `HF_HUB_DISABLE_XET=1`.
`BACKEND=spacy-lg` prova spaCy `it_core_news_lg` (aggiunto il 2026-10-23).
"""
import json
import logging
import os
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
logging.getLogger("stanza").setLevel(logging.ERROR)

QM = Path(__file__).resolve().parents[2]
ROOT = QM.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(QM / "sintassi"))
import misura_sintassi as ms  # noqa: E402
from calibra_sintassi import CHIAVI, p_binomiale  # noqa: E402


def stanza_nlp():
    import spacy_stanza
    pk = os.environ.get("STANZA_PACKAGE", "")
    kw = {"package": pk} if pk else {}
    return spacy_stanza.load_pipeline("it", processors="tokenize,mwt,pos,lemma,depparse",
                                      download_method=None, logging_level="ERROR", **kw)


def parser(nome):
    if nome == "spacy":
        return ms.carica_nlp()
    if nome == "spacy-lg":   # it_core_news_lg, stessa licenza del md, fuori dal repo
        import spacy
        return spacy.load("it_core_news_lg", exclude=["ner"])
    return stanza_nlp()


def base(nomi):
    out = {}
    for nome in nomi:
        nlp = parser(nome)
        t0, ril = time.time(), []
        for f in ms.BASE:
            d = ms.misura_file(ROOT / f, nlp)
            for b in d["per_box"]:
                for k, v in b["rilievi"].items():
                    for x in v:
                        ril.append({"file": Path(f).stem[:24], "riga": b["riga"], "tipo": k, "testo": x})
        out[nome] = {"secondi": round(time.time() - t0, 1), "rilievi": ril}
    return out


def coppie(nomi, percorsi):
    righe = [r for p in percorsi for r in json.load(open(p, encoding="utf-8"))]
    for nome in nomi:
        nlp = parser(nome)
        t0 = time.time()
        cc = []
        for r in righe:
            w, l = ms.analizza(r["win"], nlp), ms.analizza(r["lose"], nlp)
            for m in (w, l):
                m["calchi‰"] = 1000 * m["calchi"] / max(1, m["parole"])
            cc.append((w, l))
        sec = time.time() - t0
        print(f"\n== {nome}: {len(cc)} coppie, {sec:.1f} s\n")
        print(f"{'metrica':18} vinc>perd vinc<perd pari  accordo  p(binom)")
        for k in CHIAVI:
            up = sum(w[k] > l[k] + 1e-9 for w, l in cc)
            dn = sum(w[k] < l[k] - 1e-9 for w, l in cc)
            eq = len(cc) - up - dn
            nn = up + dn
            print(f"{k:18} {up:9} {dn:9} {eq:5}  {max(up, dn) / nn if nn else 0:6.2f}  {p_binomiale(up, dn):.3f}")


if __name__ == "__main__":
    nomi = os.environ.get("BACKEND", "spacy,stanza").split(",")
    if sys.argv[1] == "base":
        print(json.dumps(base(nomi), ensure_ascii=False, indent=1))
    else:
        coppie(nomi, sys.argv[2:])
