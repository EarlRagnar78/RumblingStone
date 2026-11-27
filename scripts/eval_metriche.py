#!/usr/bin/env python3
"""eval_metriche.py — le metriche di un classificatore contro un set d'oro (ADR-0154).

Un involucro sottile delle librerie che la comunità usa per questo, per ogni
componente del repo che assegna un'etichetta e ha un set d'oro: l'instradamento
degli agenti, i rilevatori, i verificatori.

- **scikit-learn** (``sklearn.metrics``): ``confusion_matrix``,
  ``precision_recall_fscore_support``, ``f1_score`` macro e micro,
  ``accuracy_score``, ``cohen_kappa_score``, ``classification_report``;
  ``sklearn.dummy.DummyClassifier(strategy="most_frequent")`` per la baseline.
- **scipy** (``scipy.stats``): ``binomtest(k, n).proportion_ci(method="wilson")``
  e ``bootstrap(method="percentile")``.

Le convenzioni che passiamo a ogni chiamata, perché un numero di qui si rifà là:
``labels=`` l'unione ordinata delle classi di oro e predizioni (una classe che
il classificatore inventa entra nella macro con F1 0) e ``zero_division=0``.

Qui resta solo ciò che le librerie non danno: l'accuracy indulgente con le
«accettabili» del set d'oro, i casi vuoti (sklearn rifiuta un insieme vuoto) e
il formato del rapporto, e la macro-F1 come frazione esatta ricavata dai
conteggi interi di ``confusion_matrix`` (``macro_f1_esatta``), perché i cancelli
confrontano interi e frazioni, mai i float che sklearn restituisce. Nel
rapporto ogni float esce arrotondato a quattro cifre, così il JSON è identico
fra due esecuzioni; i conteggi restano interi.

Gli import di sklearn e scipy stanno dentro le funzioni: ``instradamento_agenti``
importa questo modulo nel percorso degli hook, che girano a ogni messaggio e non
devono pagare il secondo d'import di sklearn.

Canale: testing (ADR-0099), scikit-learn fissato in ``requirements-dev.txt``.

    python3 scripts/eval_metriche.py     # stampa l'esempio a tre classi dei test
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from typing import Sequence

CIFRE = 4


def _pari(oro: Sequence[str], pred: Sequence[str]) -> None:
    if len(oro) != len(pred):
        raise ValueError(f"oro e predizioni di lunghezza diversa: {len(oro)} e {len(pred)}")


def _q(x) -> float:
    """Un float a quattro cifre fisse, come Python e non come numpy."""
    return round(float(x), CIFRE)


def etichette(oro: Sequence[str], pred: Sequence[str]) -> "list[str]":
    """Le classi dell'oro e delle predizioni, unite e ordinate: il ``labels=`` di ogni chiamata."""
    return sorted(set(oro) | set(pred))


def matrice_confusione(oro: Sequence[str], pred: Sequence[str],
                       classi: "Sequence[str] | None" = None) -> "tuple[list[str], list[list[int]]]":
    """Righe: l'oro; colonne: la predizione; nell'ordine di ``classi`` (default: ``etichette``)."""
    _pari(oro, pred)
    classi = list(classi) if classi is not None else etichette(oro, pred)
    if not oro:
        return classi, [[0] * len(classi) for _ in classi]
    from sklearn.metrics import confusion_matrix
    return classi, confusion_matrix(oro, pred, labels=classi).tolist()


def per_classe(oro: Sequence[str], pred: Sequence[str]) -> "dict[str, dict]":
    """Precision, recall, F1 e supporto (quanti nell'oro) per ogni classe."""
    _pari(oro, pred)
    classi = etichette(oro, pred)
    if not classi:
        return {}
    from sklearn.metrics import precision_recall_fscore_support
    p, r, f, s = precision_recall_fscore_support(oro, pred, labels=classi, average=None,
                                                 zero_division=0)
    return {c: {"precision": float(p[i]), "recall": float(r[i]), "f1": float(f[i]),
                "supporto": int(s[i])} for i, c in enumerate(classi)}


def _f1(oro: Sequence[str], pred: Sequence[str], media: str) -> float:
    _pari(oro, pred)
    if not oro:
        return 0.0
    from sklearn.metrics import f1_score
    return float(f1_score(oro, pred, labels=etichette(oro, pred), average=media,
                          zero_division=0))


def macro_f1(oro: Sequence[str], pred: Sequence[str]) -> float:
    return _f1(oro, pred, "macro")


def macro_f1_esatta(oro: Sequence[str], pred: Sequence[str]) -> Fraction:
    """La macro-F1 come frazione esatta, dai conteggi interi di ``confusion_matrix``.

    È la sola formula che resta nostra, ``2·tp / (2·tp + fp + fn)`` per classe e
    la media sulle classi: serve ai cancelli, che confrontano interi e frazioni e
    mai float. Un test la tiene uguale a ``f1_score(average="macro")``."""
    classi, m = matrice_confusione(oro, pred)
    if not classi:
        return Fraction(0)
    tot = Fraction(0)
    for i in range(len(classi)):
        tp = m[i][i]
        den = sum(m[i]) + sum(r[i] for r in m)  # (tp + fn) + (tp + fp)
        tot += Fraction(2 * tp, den) if den else Fraction(0)
    return tot / len(classi)


def micro_f1(oro: Sequence[str], pred: Sequence[str]) -> float:
    """Su etichette singole coincide con l'accuracy."""
    return _f1(oro, pred, "micro")


def giusti(oro: Sequence[str], pred: Sequence[str]) -> int:
    _pari(oro, pred)
    if not oro:
        return 0
    from sklearn.metrics import accuracy_score
    return int(accuracy_score(oro, pred, normalize=False))


def accuracy(oro: Sequence[str], pred: Sequence[str]) -> float:
    _pari(oro, pred)
    if not oro:
        return 0.0
    from sklearn.metrics import accuracy_score
    return float(accuracy_score(oro, pred))


def giusti_indulgenti(oro: Sequence[str], pred: Sequence[str],
                      accettabili: "Sequence[Sequence[str]]") -> int:
    """Giusto se la predizione è l'atteso o una delle sue accettabili (nostra: niente libreria)."""
    _pari(oro, pred)
    _pari(oro, accettabili)
    return sum(p == o or p in acc for o, p, acc in zip(oro, pred, accettabili))


def accuracy_indulgente(oro: Sequence[str], pred: Sequence[str],
                        accettabili: "Sequence[Sequence[str]]") -> Fraction:
    n = len(oro)
    return Fraction(giusti_indulgenti(oro, pred, accettabili), n) if n else Fraction(0)


def wilson(k: int, n: int, livello: float = 0.95) -> "tuple[float, float]":
    """Intervallo di Wilson senza correzione di continuità, da ``scipy.stats.binomtest``.

    Con n = 0 non c'è informazione: (0, 1)."""
    if n == 0:
        return 0.0, 1.0
    from scipy.stats import binomtest
    ci = binomtest(k, n).proportion_ci(confidence_level=livello, method="wilson")
    return float(ci.low), float(ci.high)


def kappa_cohen(a: Sequence[str], b: Sequence[str]) -> float:
    """Kappa di Cohen fra due etichettature degli stessi casi (``cohen_kappa_score``).

    Se l'accordo atteso è 1 (entrambe costanti sulla stessa classe) sklearn lo
    dichiara indefinito; qui vale 1, la convenzione di prima, con
    ``replace_undefined_by=1.0``."""
    _pari(a, b)
    if not a:
        return 0.0
    import warnings
    from sklearn.exceptions import UndefinedMetricWarning
    from sklearn.metrics import cohen_kappa_score
    with warnings.catch_warnings():  # il caso indefinito è quello che replace_undefined_by copre
        warnings.filterwarnings("ignore", message="A single label was found", category=UserWarning)
        warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
        return float(cohen_kappa_score(a, b, labels=etichette(a, b), replace_undefined_by=1.0))


def bootstrap_macro_f1(oro: Sequence[str], pred: Sequence[str], campioni: int = 1000,
                       seme: int = 0, livello: float = 0.95) -> dict:
    """Intervallo percentile della macro-F1 con ``scipy.stats.bootstrap``.

    Si ricampionano gli indici dei casi (oro e predizione restano in coppia) con
    ``numpy.random.default_rng(seme)``; ogni ricampionamento usa le classi che
    contiene (oro o predizione), come la stima: una classe che sparisce dal
    ricampionamento non entra nella sua media. I quantili
    sono quelli di scipy (``np.percentile``, con interpolazione). Con meno di due
    casi scipy non ricampiona: l'intervallo è la stima."""
    _pari(oro, pred)
    stima = macro_f1(oro, pred)
    n = len(oro)
    if n < 2 or campioni <= 0:
        return {"stima": stima, "basso": stima, "alto": stima, "campioni": 0, "seme": seme}
    import numpy as np
    from scipy.stats import bootstrap
    from sklearn.metrics import f1_score
    o, p = np.asarray(oro, dtype=object), np.asarray(pred, dtype=object)

    def statistica(idx) -> float:
        idx = np.asarray(idx, dtype=int)
        oi, pi = list(o[idx]), list(p[idx])
        return f1_score(oi, pi, labels=etichette(oi, pi), average="macro", zero_division=0)

    ci = bootstrap((np.arange(n),), statistica, n_resamples=campioni, method="percentile",
                   confidence_level=livello, rng=np.random.default_rng(seme),
                   vectorized=False).confidence_interval
    return {"stima": stima, "basso": float(ci.low), "alto": float(ci.high),
            "campioni": campioni, "seme": seme}


def _dummy(addestramento: Sequence[str]):
    from sklearn.dummy import DummyClassifier
    return DummyClassifier(strategy="most_frequent").fit([[0]] * len(addestramento),
                                                         list(addestramento))


def maggioritaria(addestramento: Sequence[str]) -> "str | None":
    """La classe più frequente, da ``DummyClassifier(strategy="most_frequent")``.

    A pari frequenza vince la prima di ``classes_``, che sklearn ordina con
    ``np.unique``: l'ordine dei code point, lo stesso di ``sorted``."""
    if not addestramento:
        return None
    return str(_dummy(addestramento).predict([[0]])[0])


def baseline_maggioritaria(addestramento: Sequence[str], n: int) -> "list[str]":
    """La baseline addestrata su ``addestramento`` (il dev) e applicata a ``n`` casi (il test)."""
    if not addestramento or n == 0:
        return []
    return [str(x) for x in _dummy(addestramento).predict([[0]] * n)]


def rapporto_testo(oro: Sequence[str], pred: Sequence[str]) -> str:
    """Il ``classification_report`` di sklearn, a quattro cifre."""
    from sklearn.metrics import classification_report
    return classification_report(oro, pred, labels=etichette(oro, pred), digits=CIFRE,
                                 zero_division=0)


def frazione(k: "int | Fraction", n: int = 1) -> dict:
    """Per JSON: la frazione esatta (``k/n``, o una Fraction) e il valore a quattro cifre."""
    x = Fraction(k, n) if n else Fraction(0)
    return {"frazione": f"{x.numerator}/{x.denominator}", "valore": _q(x)}


def rapporto(oro: Sequence[str], pred: Sequence[str],
             accettabili: "Sequence[Sequence[str]] | None" = None,
             campioni: int = 1000, seme: int = 0) -> dict:
    """Tutte le metriche di una valutazione, pronte per ``json.dumps``.

    Con ``campioni=0`` niente bootstrap e niente chiave ``macro_f1_bootstrap95``:
    l'intervallo dipende dal generatore di numpy, e un JSON che deve restare
    identico fra versioni (o un cancello) non lo porta."""
    accettabili = accettabili if accettabili is not None else [[] for _ in oro]
    n = len(oro)
    k = giusti(oro, pred)
    ki = giusti_indulgenti(oro, pred, accettabili)
    classi, m = matrice_confusione(oro, pred)
    esatta = macro_f1_esatta(oro, pred)
    out = {
        "n": n,
        "giusti": k,
        "accuracy": frazione(k, n),
        "wilson95": [_q(v) for v in wilson(k, n)],
        "giusti_indulgenti": ki,
        "accuracy_indulgente": frazione(ki, n),
        "wilson95_indulgente": [_q(v) for v in wilson(ki, n)],
        "macro_f1": frazione(esatta),
        "micro_f1": {"valore": _q(micro_f1(oro, pred))},
        "classi": classi,
        "matrice": m,
        "per_classe": {c: {"precision": _q(v["precision"]), "recall": _q(v["recall"]),
                           "f1": _q(v["f1"]), "supporto": v["supporto"]}
                       for c, v in per_classe(oro, pred).items()},
    }
    if campioni > 0:
        boot = bootstrap_macro_f1(oro, pred, campioni=campioni, seme=seme)
        out["macro_f1_bootstrap95"] = {"basso": _q(boot["basso"]), "alto": _q(boot["alto"]),
                                       "campioni": boot["campioni"], "seme": boot["seme"]}
    return out


def main(argv: "list[str] | None" = None) -> int:
    """L'esempio a tre classi dei test: JSON su stdout (come dichiara il manifest), o testo con --testo."""
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--testo", action="store_true", help="il rapporto leggibile invece del JSON")
    args = ap.parse_args(argv)
    oro = ["a", "a", "a", "b", "b", "c"]
    pred = ["a", "a", "b", "b", "c", "c"]
    if args.testo:
        print(rapporto_testo(oro, pred))
    else:
        print(json.dumps(rapporto(oro, pred, campioni=200), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
