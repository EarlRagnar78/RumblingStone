"""Il tiro del mucchio di d10 del plugin di prova, in probabilità esatte.

`successi(dati)` restituisce una funzione `n → {successi: probabilità}` per un
mucchio di `n` d10, con i parametri del plugin (soglia, rilancio, uno_annulla).
Le probabilità sono `Fraction`: il rilancio è infinito in teoria, quindi la
catena si ferma dopo `RILANCI` rilanci e la massa che resta (al più
(1/10)**RILANCI per dado) si somma all'ultimo valore, così il totale è 1.
Con «uno annulla» non si rilancia, e un totale sotto zero è il disastro
(nessun successo e almeno un 1 in più).
"""
from __future__ import annotations

from fractions import Fraction

RILANCI = 40


def _un_dado(soglia, rilancio, uno_annulla):
    d = Fraction(1, 10)
    if uno_annulla:
        uno = d
        succ = d * (11 - soglia)
        return {-1: uno, 0: 1 - uno - succ, 1: succ}
    p_r = d * (11 - rilancio) if rilancio else Fraction(0)
    p_s = d * (11 - soglia) - p_r
    p_f = 1 - p_s - p_r
    fuori = {0: p_f}
    for k in range(1, RILANCI + 1):
        fuori[k] = p_r ** k * p_f + p_r ** (k - 1) * p_s
    fuori[RILANCI] += p_r ** RILANCI * (1 - p_f)  # la coda: tutto quello che rilancia ancora
    return {k: v for k, v in fuori.items() if v}


def _somma(a, b):
    c = {}
    for i, p in a.items():
        for j, q in b.items():
            c[i + j] = c.get(i + j, 0) + p * q
    return c


def successi(dati):
    soglia = int(dati.get("soglia", 8))
    rilancio = dati.get("rilancio")
    uno = bool(dati.get("uno_annulla", False))
    dado = _un_dado(soglia, int(rilancio) if rilancio else None, uno)

    def distribuzione(n):
        tot = {0: Fraction(1)}
        for _ in range(int(n)):
            tot = _somma(tot, dado)
        return dict(sorted(tot.items()))
    return distribuzione
