#!/usr/bin/env python3
"""
ridondanza.py — le misure di fazioni_liapis.py dicono qualcosa che qualita_mappe.py
non dice già? Spearman fra ogni misura nuova e le metriche esistenti, sulle
stesse mappe. |rho| >= 0,8 = doppione. Sola lettura.

Uso: python3 ridondanza.py LIAPIS.json QUALITA.json
"""
import json
import sys


def ranghi(v):
    ordine = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[ordine[j + 1]] == v[ordine[i]]:
            j += 1
        for k in range(i, j + 1):
            r[ordine[k]] = (i + j) / 2
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = ranghi(a), ranghi(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return None if den == 0 else num / den


def main():
    L = json.load(open(sys.argv[1], encoding="utf-8"))
    Q = {(m["file"], m["mappa"]): m for m in json.load(open(sys.argv[2], encoding="utf-8"))["mappe"]}
    nuove = ["area_pg", "bilancio_area", "esplorazione_pg", "bilancio_esplorazione", "tiro_scoperto"]
    vecchie = ["voto", "distanza_min_q", "copertura", "m1", "m2", "libere", "anelli", "celle_per_creatura"]
    coppie = [(l, Q[(l["file"], l["mappa"])]) for l in L if (l["file"], l["mappa"]) in Q]
    print(f"mappe: {len(coppie)}")
    print("| nuova \\ esistente | " + " | ".join(vecchie) + " |")
    print("|---" * (len(vecchie) + 1) + "|")
    for n in nuove:
        celle = []
        for v in vecchie:
            xs, ys = [], []
            for l, q in coppie:
                a = l.get(n)
                b = q["voto"] if v == "voto" else q["metriche"].get(v)
                if a is not None and b is not None:
                    xs.append(a)
                    ys.append(b)
            rho = spearman(xs, ys) if len(xs) >= 4 else None
            celle.append("—" if rho is None else f"{rho:+.2f}")
        print(f"| {n} | " + " | ".join(celle) + " |")


main()
