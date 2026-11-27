"""La minaccia di un incontro nel sistema a mucchio di d10 di prova.

Al posto dell'EL: la somma dei successi attesi dei mucchi d'attacco delle
creature (il numero che gli strumenti d20 leggono come GS qui è il numero di
dadi). Successi attesi per dado, con soglia s e rilancio r:
(11 − s) / 10 / (1 − (11 − r) / 10). Con 8 e 10: 0,3 / 0,9 = 1/3.
Con «uno annulla» (niente rilancio): (11 − s) / 10 − 1/10. Con 6: 0,4.
"""
from __future__ import annotations


def minaccia(dati):
    soglia = int(dati.get("soglia", 8))
    rilancio = dati.get("rilancio")
    p_s = (11 - soglia) / 10
    if dati.get("uno_annulla"):      # ogni 1 toglie un successo, niente rilancio
        per_dado = p_s - 0.1
    else:
        p_r = (11 - int(rilancio)) / 10 if rilancio else 0.0
        per_dado = p_s / (1 - p_r)
    return lambda mucchi: float(sum(mucchi) * per_dado) if mucchi else 0.0
