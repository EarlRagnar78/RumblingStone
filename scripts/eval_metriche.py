#!/usr/bin/env python3
"""eval_metriche.py — le metriche di un classificatore contro un set d'oro (ADR-0154).

Libreria di sola stdlib per ogni componente del repo che assegna un'etichetta
e ha un set d'oro con cui confrontarsi: l'instradamento degli agenti, i
rilevatori, i verificatori. Le metriche sono quelle standard e seguono le
convenzioni di scikit-learn, così un numero di qui si può rifare là:

- **0/0 vale 0** in precision, recall e F1 (sklearn ``zero_division=0``).
- **macro-F1** è la media delle F1 sulle classi presenti nell'oro **o** nelle
  predizioni (sklearn ``labels=`` unione delle due): una classe che il
  classificatore inventa e l'oro non ha entra con F1 0.
- **F1** di una classe è ``2·tp / (2·tp + fp + fn)``, uguale a ``2PR/(P+R)``
  dove è definita e 0 dove non lo è.
- **micro-F1** su etichette singole coincide con l'accuracy.

I valori escono come ``fractions.Fraction``: i cancelli confrontano conteggi
interi o frazioni, mai float. Solo Wilson e i rapporti stampati sono float.

Le etichette si ordinano con ``sorted``: matrice e rapporti sono deterministici.
Il bootstrap usa ``random.Random(seme)`` e prende gli indici con
``int(rng.random() * n)``, mai ``choices`` o ``randrange``, i cui algoritmi
possono cambiare fra versioni di Python: lo stesso seme dà lo stesso
intervallo su 3.13 e 3.14.

    python3 scripts/eval_metriche.py     # stampa l'esempio a tre classi dei test
"""
from __future__ import annotations

import json
import math
import random
import sys
from collections import Counter
from fractions import Fraction
from statistics import NormalDist
from typing import Sequence

Z95 = NormalDist().inv_cdf(0.975)


def _pari(oro: Sequence[str], pred: Sequence[str]) -> None:
    if len(oro) != len(pred):
        raise ValueError(f"oro e predizioni di lunghezza diversa: {len(oro)} e {len(pred)}")


def etichette(oro: Sequence[str], pred: Sequence[str]) -> "list[str]":
    """Le classi dell'oro e delle predizioni, unite e ordinate."""
    return sorted(set(oro) | set(pred))


def matrice_confusione(oro: Sequence[str], pred: Sequence[str],
                       classi: "Sequence[str] | None" = None) -> "tuple[list[str], list[list[int]]]":
    """Righe: l'oro; colonne: la predizione; nell'ordine di ``classi`` (default: ``etichette``)."""
    _pari(oro, pred)
    classi = list(classi) if classi is not None else etichette(oro, pred)
    pos = {c: i for i, c in enumerate(classi)}
    m = [[0] * len(classi) for _ in classi]
    for o, p in zip(oro, pred):
        m[pos[o]][pos[p]] += 1
    return classi, m


def _div(a: int, b: int) -> Fraction:
    return Fraction(a, b) if b else Fraction(0)


def per_classe(oro: Sequence[str], pred: Sequence[str]) -> "dict[str, dict]":
    """Precision, recall, F1 (Fraction) e supporto (quanti nell'oro) per ogni classe."""
    classi, m = matrice_confusione(oro, pred)
    out: "dict[str, dict]" = {}
    for i, c in enumerate(classi):
        tp = m[i][i]
        fn = sum(m[i]) - tp
        fp = sum(r[i] for r in m) - tp
        out[c] = {"precision": _div(tp, tp + fp), "recall": _div(tp, tp + fn),
                  "f1": _div(2 * tp, 2 * tp + fp + fn), "supporto": tp + fn}
    return out


def macro_f1(oro: Sequence[str], pred: Sequence[str]) -> Fraction:
    pc = per_classe(oro, pred)
    if not pc:
        return Fraction(0)
    return sum((v["f1"] for v in pc.values()), Fraction(0)) / len(pc)


def micro_f1(oro: Sequence[str], pred: Sequence[str]) -> Fraction:
    classi, m = matrice_confusione(oro, pred)
    tp = sum(m[i][i] for i in range(len(classi)))
    errori = len(oro) - tp  # ogni errore è un fp per una classe e un fn per un'altra
    return _div(2 * tp, 2 * tp + 2 * errori)


def giusti(oro: Sequence[str], pred: Sequence[str]) -> int:
    _pari(oro, pred)
    return sum(o == p for o, p in zip(oro, pred))


def accuracy(oro: Sequence[str], pred: Sequence[str]) -> Fraction:
    return _div(giusti(oro, pred), len(oro))


def giusti_indulgenti(oro: Sequence[str], pred: Sequence[str],
                      accettabili: "Sequence[Sequence[str]]") -> int:
    """Giusto se la predizione è l'atteso o una delle sue accettabili."""
    _pari(oro, pred)
    _pari(oro, accettabili)
    return sum(p == o or p in acc for o, p, acc in zip(oro, pred, accettabili))


def accuracy_indulgente(oro: Sequence[str], pred: Sequence[str],
                        accettabili: "Sequence[Sequence[str]]") -> Fraction:
    return _div(giusti_indulgenti(oro, pred, accettabili), len(oro))


def wilson(k: int, n: int, z: float = Z95) -> "tuple[float, float]":
    """Intervallo di Wilson senza correzione di continuità (scipy ``method="wilson"``).

    Con n = 0 non c'è informazione: (0, 1)."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    z2 = z * z
    den = 1 + z2 / n
    centro = (p + z2 / (2 * n)) / den
    mezzo = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / den
    # con k = 0 il limite basso è 0 esatto, con k = n l'alto è 1: il float lascerebbe 1e-17
    basso = 0.0 if k == 0 else max(0.0, centro - mezzo)
    alto = 1.0 if k == n else min(1.0, centro + mezzo)
    return basso, alto


def kappa_cohen(a: Sequence[str], b: Sequence[str]) -> Fraction:
    """Kappa di Cohen fra due etichettature degli stessi casi.

    Se l'accordo atteso è 1 (entrambe costanti sulla stessa classe) il kappa
    non è definito: per convenzione vale 1 se l'accordo osservato è pieno."""
    _pari(a, b)
    n = len(a)
    if n == 0:
        return Fraction(0)
    po = Fraction(sum(x == y for x, y in zip(a, b)), n)
    ca, cb = Counter(a), Counter(b)
    pe = sum((Fraction(ca[c] * cb[c], n * n) for c in set(ca) | set(cb)), Fraction(0))
    if pe == 1:
        return Fraction(1) if po == 1 else Fraction(0)
    return (po - pe) / (1 - pe)


def _indici(rng: random.Random, n: int) -> "list[int]":
    return [int(rng.random() * n) for _ in range(n)]


def bootstrap_macro_f1(oro: Sequence[str], pred: Sequence[str], campioni: int = 1000,
                       seme: int = 0, livello: Fraction = Fraction(95, 100)) -> dict:
    """Intervallo percentile della macro-F1 su ``campioni`` ricampionamenti con reinserimento.

    Il quantile basso è il valore in posizione ``floor(α/2 · (B−1))`` dei valori
    ordinati, l'alto in ``ceil((1−α/2) · (B−1))``: niente interpolazione."""
    _pari(oro, pred)
    stima = macro_f1(oro, pred)
    n = len(oro)
    if n == 0 or campioni <= 0:
        return {"stima": stima, "basso": stima, "alto": stima, "campioni": 0, "seme": seme}
    rng = random.Random(seme)
    valori = []
    for _ in range(campioni):
        idx = _indici(rng, n)
        valori.append(macro_f1([oro[i] for i in idx], [pred[i] for i in idx]))
    valori.sort()
    alfa = 1 - Fraction(livello)
    basso = valori[math.floor(alfa / 2 * (campioni - 1))]
    alto = valori[math.ceil((1 - alfa / 2) * (campioni - 1))]
    return {"stima": stima, "basso": basso, "alto": alto, "campioni": campioni, "seme": seme}


def maggioritaria(oro: Sequence[str]) -> "str | None":
    """La classe più frequente; a pari frequenza la prima in ordine alfabetico."""
    if not oro:
        return None
    conta = Counter(oro)
    return min(conta, key=lambda c: (-conta[c], c))


def frazione(x: Fraction) -> dict:
    """Una Fraction per JSON: la frazione esatta e il valore a 4 cifre."""
    return {"frazione": f"{x.numerator}/{x.denominator}", "valore": round(float(x), 4)}


def rapporto(oro: Sequence[str], pred: Sequence[str],
             accettabili: "Sequence[Sequence[str]] | None" = None,
             campioni: int = 1000, seme: int = 0) -> dict:
    """Tutte le metriche di una valutazione, pronte per ``json.dumps``."""
    accettabili = accettabili if accettabili is not None else [[] for _ in oro]
    n = len(oro)
    k = giusti(oro, pred)
    ki = giusti_indulgenti(oro, pred, accettabili)
    classi, m = matrice_confusione(oro, pred)
    boot = bootstrap_macro_f1(oro, pred, campioni=campioni, seme=seme)
    return {
        "n": n,
        "giusti": k,
        "accuracy": frazione(_div(k, n)),
        "wilson95": [round(v, 4) for v in wilson(k, n)],
        "giusti_indulgenti": ki,
        "accuracy_indulgente": frazione(_div(ki, n)),
        "wilson95_indulgente": [round(v, 4) for v in wilson(ki, n)],
        "macro_f1": frazione(macro_f1(oro, pred)),
        "macro_f1_bootstrap95": {"basso": round(float(boot["basso"]), 4),
                                 "alto": round(float(boot["alto"]), 4),
                                 "campioni": boot["campioni"], "seme": boot["seme"]},
        "micro_f1": frazione(micro_f1(oro, pred)),
        "classi": classi,
        "matrice": m,
        "per_classe": {c: {"precision": round(float(v["precision"]), 4),
                           "recall": round(float(v["recall"]), 4),
                           "f1": round(float(v["f1"]), 4), "supporto": v["supporto"]}
                       for c, v in per_classe(oro, pred).items()},
    }


def main() -> int:
    oro = ["a", "a", "a", "b", "b", "c"]
    pred = ["a", "a", "b", "b", "c", "c"]
    print(json.dumps(rapporto(oro, pred, campioni=200), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
