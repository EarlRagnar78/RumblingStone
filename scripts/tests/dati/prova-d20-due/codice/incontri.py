"""Il metodo «piu_forte» del plugin finto prova-d20-due (F6 di ADR-0112).

EL = il GS più alto + (numero di creature − 1); 0 senza creature. Regola
inventata per il test: serve solo a mostrare che un algoritmo nuovo entra dal
plugin senza toccare il nucleo.
"""
from __future__ import annotations


def piu_forte(dati: dict):
    return lambda crs: float(max(crs) + len(crs) - 1) if crs else 0.0
