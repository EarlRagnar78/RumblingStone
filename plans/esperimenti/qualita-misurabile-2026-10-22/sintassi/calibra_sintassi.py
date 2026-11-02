"""Le misure di scripts/misura_sintassi.py sulle 38 coppie votate alla cieca.

Stessa prova di ../calibra_prosa.py: per ogni misura, quante volte è più alta
nella versione vincente, più bassa, pari, e il p binomiale a due code.
`rip_fra_box%` non si calcola su un testo isolato: al suo posto c'è
`rip_interna%`. Rifare:

    python3 plans/esperimenti/qualita-misurabile-2026-10-22/sintassi/calibra_sintassi.py \
        plans/esperimenti/qualita-misurabile-2026-10-22/COPPIE-VOTATE.json
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import misura_sintassi as ms  # noqa: E402

CHIAVI = ["sogg_preverbale", "agg_complesso", "stare_gerundio", "pron_soggetto", "calchi",
          "calchi‰", "possessivi_corpo", "profondita_max", "profondita_media", "livelli_max",
          "frasi_oltre2%", "lungh_dip", "mattr_lemmi", "rip_interna%"]


def p_binomiale(up: int, dn: int) -> float:
    nn, hi = up + dn, max(up, dn)
    if not nn:
        return 1.0
    return min(1.0, 2 * sum(math.comb(nn, i) for i in range(hi, nn + 1)) / 2 ** nn)


def misure(testo, nlp):
    m = ms.analizza(testo, nlp)
    m["calchi‰"] = 1000 * m["calchi"] / max(1, m["parole"])
    return m


def main():
    nlp = ms.carica_nlp()
    if nlp is None:
        print("spaCy assente: calibrazione saltata")
        return 0
    righe = json.load(open(sys.argv[1], encoding="utf-8"))
    coppie = [(misure(r["win"], nlp), misure(r["lose"], nlp)) for r in righe]
    print(f"Calibrazione delle misure sintattiche ({ms.MODELLO}) su {len(coppie)} coppie votate\n")
    print(f"{'metrica':18} vinc>perd vinc<perd pari  accordo  p(binom)")
    for k in CHIAVI:
        up = dn = eq = 0
        for w, l in coppie:
            a, b = w[k], l[k]
            if abs(a - b) < 1e-9:
                eq += 1
            elif a > b:
                up += 1
            else:
                dn += 1
        nn = up + dn
        acc = max(up, dn) / nn if nn else 0
        print(f"{k:18} {up:9} {dn:9} {eq:5}  {acc:6.2f}  {p_binomiale(up, dn):.3f}")
    tot = {k: (sum(w[k] for w, _ in coppie), sum(l[k] for _, l in coppie)) for k in CHIAVI[:7]}
    print("\nTotali dei rilievi (vincenti / perdenti): "
          + ", ".join(f"{k} {a:g}/{b:g}" for k, (a, b) in tot.items() if k != "calchi‰"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
