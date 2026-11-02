#!/usr/bin/env python3
"""
qualita_mappe_profonde.py — le metriche di configurazione di una mappa, senza soglia.

Le chiama ``qualita_mappe.py --profonde`` e finiscono solo nel JSON, sotto la
chiave ``profonde`` di ogni mappa. Non toccano il voto ne' i rilievi: nessuna
fonte da' una soglia per le battlemap, e il metodo di Smith e Whitehead (2010)
vuole metriche per confrontare le mappe fra loro e le versioni di una mappa.

Da ``plans/esperimenti/mappe-strumenti-2026-10-22/metriche_nuove.py`` (commit
ffe206b5, RICERCA-STRUMENTI-MAPPE.md §3), riscritto in libreria standard:

1. Space syntax (Hillier e Hanson 1984; Turner et al. 2001, VGA) sul grafo di
   visibilita' e su quello di movimento delle celle percorribili: profondita'
   media MD = somma delle distanze / (k-1), RA = 2(MD-1)/(k-2), integrazione
   = D_k / RA con il D_k di Hillier e Hanson; intelligibilita' = r^2 fra
   connettivita' e integrazione (Hillier 1996). k e' la dimensione della
   componente del nodo; sotto 4 nodi le formule non valgono e il nodo si salta.
2. Correlazione fra vista e accesso: r di Pearson fra l'integrazione di ogni
   cella alla vista e quella a piedi (la «visibility/accessibility
   discrepancy» di Martin 2014; la formula e' della ricerca, non di Martin).
3. Simmetria (Summerville et al. 2017): quota di celle uguali allo specchio
   sinistra-destra, alto-basso e alla rotazione di 180 gradi, sulle classi di
   cella.
4. Diversita' dei pattern 2x2 (Lucas e Volz 2019): quante finestre 2x2
   distinte ci sono e l'entropia di Shannon, in bit, della loro distribuzione.

La vista e' lo shadowcasting simmetrico di Albert Ford
(https://www.albertford.com/shadowcasting/, CC0), lo stesso algoritmo di
``tcod.constants.FOV_SYMMETRIC_SHADOWCAST`` che il collaudo usa per M4, scritto
qui con le frazioni come coppie di interi. I cammini minimi sono BFS con gli
insiemi di nodi come bit di un intero: niente numpy ne' scipy, che stanno in
requirements-dev.txt e non in requirements.txt.

Deterministico: l'ordine dei nodi e' quello delle celle ordinate, i numeri
escono arrotondati. In sola lettura; non ha una riga di comando sua.
"""
from __future__ import annotations

import math
from collections import Counter

# Le classi di cella su cui si misurano simmetria e pattern (le stesse della
# ricerca, `_comune.classe`):
#   M muro · O ostacolo che non ferma la vista · P porta · S scala o botola
#   H pericolo · K copertura senza blocco · U creatura · . pavimento · V fuori
CLASSI = "MOPSHKU.V"
DECIMALI = 4


# --------------------------------------------------------------------------- vista
def _arrotonda_su(num: int, den: int) -> int:
    """floor(num/den + 1/2) con den > 0, in interi."""
    return (2 * num + den) // (2 * den)


def _arrotonda_giu(num: int, den: int) -> int:
    """ceil(num/den - 1/2) con den > 0, in interi."""
    return -((den - 2 * num) // (2 * den))


def campo_visivo(trasparente: list, origine: tuple[int, int]) -> set:
    """Le celle (x, y) visibili da ``origine`` con lo shadowcasting simmetrico
    di Albert Ford. ``trasparente[y][x]`` dice se la cella lascia passare la
    vista; fuori dalla griglia la vista si ferma. I muri visti sono nel campo
    (come ``light_walls=True`` di tcod), il raggio e' illimitato."""
    H = len(trasparente)
    W = len(trasparente[0]) if H else 0
    ox, oy = origine
    visti = {origine}
    # i quattro quadranti: x = ox + ar*r + ac*c, y = oy + br*r + bc*c
    for ar, ac, br, bc in ((0, 1, -1, 0), (1, 0, 0, 1), (0, 1, 1, 0), (-1, 0, 0, 1)):
        # una riga: profondita', pendenza d'inizio e di fine come (num, den)
        pila = [(1, -1, 1, 1, 1)]
        while pila:
            prof, sn, sd, en, ed = pila.pop()
            c_min = _arrotonda_su(prof * sn, sd)
            c_max = _arrotonda_giu(prof * en, ed)
            prima = None  # None, True (muro) o False (pavimento)
            for c in range(c_min, c_max + 1):
                x = ox + ar * prof + ac * c
                y = oy + br * prof + bc * c
                dentro = 0 <= x < W and 0 <= y < H
                muro = not (dentro and trasparente[y][x])
                if dentro and (muro or (c * sd >= prof * sn and c * ed <= prof * en)):
                    visti.add((x, y))
                if prima is True and not muro:
                    sn, sd = 2 * c - 1, 2 * prof
                elif prima is False and muro:
                    pila.append((prof + 1, sn, sd, 2 * c - 1, 2 * prof))
                prima = muro
            if prima is False:
                pila.append((prof + 1, sn, sd, en, ed))
    return visti


# --------------------------------------------------------------------------- grafo
def _bit(maschera: int):
    while maschera:
        basso = maschera & -maschera
        yield basso.bit_length() - 1
        maschera ^= basso


def d_k(k: int) -> float | None:
    """Il D_k di Hillier e Hanson (1984): la RA della radice di un diamante di
    k nodi, che normalizza la RA fra sistemi di grandezza diversa."""
    if k < 4:
        return None
    return 2 * (k * (math.log2((k + 2) / 3) - 1) + 1) / ((k - 1) * (k - 2))


def per_nodo(adiacenza: list[int]) -> tuple[list, list, list]:
    """Per ogni nodo: connettivita' (grado), profondita' media e integrazione
    HH, sulla componente del nodo. ``adiacenza[i]`` e' l'intero i cui bit sono
    i vicini di i; il grafo e' non orientato. None dove k < 4 o RA = 0."""
    n = len(adiacenza)
    tutti = (1 << n) - 1
    grado = [a.bit_count() for a in adiacenza]
    md: list = [None] * n
    integ: list = [None] * n
    for s in range(n):
        visti = frontiera = 1 << s
        somma, passo = 0, 0
        while frontiera:
            passo += 1
            nuova = 0
            restano = tutti & ~visti
            # BFS nei due versi (Beamer 2012): dalla frontiera in avanti, o dai
            # nodi non ancora visti all'indietro quando sono meno. Stesso
            # risultato; sul grafo di visibilita', fitto, e' molte volte piu' veloce.
            if frontiera.bit_count() <= restano.bit_count():
                for i in _bit(frontiera):
                    nuova |= adiacenza[i]
                nuova &= restano
            else:
                for i in _bit(restano):
                    if adiacenza[i] & frontiera:
                        nuova |= 1 << i
            somma += passo * nuova.bit_count()
            visti |= nuova
            frontiera = nuova
        k = visti.bit_count()
        if k < 4:
            continue
        md[s] = somma / (k - 1)
        ra = 2 * (md[s] - 1) / (k - 2)
        if ra > 0:
            integ[s] = d_k(k) / ra
    return grado, md, integ


def pearson(a: list, b: list) -> float | None:
    """r di Pearson sulle coppie in cui nessuno dei due e' None; None con meno
    di tre coppie o con una delle due serie costante."""
    coppie = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(coppie) < 3:
        return None
    ma = sum(x for x, _ in coppie) / len(coppie)
    mb = sum(y for _, y in coppie) / len(coppie)
    sab = sum((x - ma) * (y - mb) for x, y in coppie)
    saa = sum((x - ma) ** 2 for x, _ in coppie)
    sbb = sum((y - mb) ** 2 for _, y in coppie)
    if saa <= 1e-12 * len(coppie) or sbb <= 1e-12 * len(coppie):
        return None
    return sab / math.sqrt(saa * sbb)


def _r(v):
    return None if v is None else round(v, DECIMALI)


def sintassi(adiacenza: list[int]) -> dict:
    """Le misure di space syntax di un grafo, riassunte sulla mappa."""
    grado, md, integ = per_nodo(adiacenza)
    n = len(adiacenza)
    mds = [v for v in md if v is not None]
    ins = [v for v in integ if v is not None]
    r = pearson(grado, integ)
    return {
        "nodi": n,
        "connettivita_media": _r(sum(grado) / n) if n else None,
        "profondita_media": _r(sum(mds) / len(mds)) if mds else None,
        "integrazione_media": _r(sum(ins) / len(ins)) if ins else None,
        "integrazione_min": _r(min(ins)) if ins else None,
        "integrazione_max": _r(max(ins)) if ins else None,
        "intelligibilita_r2": _r(r * r) if r is not None else None,
    }, integ


# --------------------------------------------------------------------------- classi
def classe(c, F: dict, MODO: dict, FUORI) -> str:
    """La classe di una cella (vedi CLASSI), dalla legenda funzionale."""
    if c in (None, FUORI):
        return "V"
    f = F.get(c, {})
    if MODO.get(c) == "unit":
        return "U"
    if f.get("door"):
        return "P"
    if f.get("posa") == "fra_livelli":
        return "S"
    if f.get("blocks_movement") and f.get("blocks_sight"):
        return "M"
    if f.get("blocks_movement"):
        return "O"
    if f.get("hazard"):
        return "H"
    if f.get("cover") in ("half", "three_quarters", "total"):
        return "K"
    return "."


def simmetria(righe: list[str]) -> dict:
    """Quota di celle uguali alla loro immagine: specchio sinistra-destra
    (``orizzontale``), alto-basso (``verticale``), rotazione di 180 gradi."""
    H = len(righe)
    if not H:
        return {"orizzontale": None, "verticale": None, "rotazione": None}
    W = max(len(r) for r in righe)
    A = [r.ljust(W, "V") for r in righe]
    tot = W * H
    oriz = sum(A[y][x] == A[y][W - 1 - x] for y in range(H) for x in range(W))
    vert = sum(A[y][x] == A[H - 1 - y][x] for y in range(H) for x in range(W))
    rot = sum(A[y][x] == A[H - 1 - y][W - 1 - x] for y in range(H) for x in range(W))
    return {"orizzontale": _r(oriz / tot), "verticale": _r(vert / tot), "rotazione": _r(rot / tot)}


def pattern_2x2(righe: list[str]) -> dict:
    """Le finestre 2x2 sulle classi (Lucas e Volz 2019): quante, quante
    distinte, e l'entropia di Shannon in bit della loro distribuzione."""
    H = len(righe)
    W = max((len(r) for r in righe), default=0)
    A = [r.ljust(W, "V") for r in righe]
    conta = Counter(A[y][x:x + 2] + A[y + 1][x:x + 2] for y in range(H - 1) for x in range(W - 1))
    tot = sum(conta.values())
    if not tot:
        return {"finestre": 0, "distinti": 0, "entropia_bit": None}
    h = -sum(v / tot * math.log2(v / tot) for _, v in sorted(conta.items()))
    return {"finestre": tot, "distinti": len(conta), "entropia_bit": _r(abs(h))}


# --------------------------------------------------------------------------- mappa
def misura(collaudo, F: dict, MODO: dict, FUORI) -> dict:
    """Tutte le metriche profonde di una mappa gia' collaudata."""
    G = collaudo.G
    perc = sorted(collaudo.percorribili(), key=lambda p: (p[1], p[0]))
    indice = {c: i for i, c in enumerate(perc)}
    n = len(perc)

    trasparente = [[c != FUORI and not F.get(c, {}).get("blocks_sight") for c in
                    (G.at(x, y) for x in range(G.W))] for y in range(G.H)]
    numero = [[None] * G.W for _ in range(G.H)]
    for i, (x, y) in enumerate(perc):
        numero[y][x] = i
    # le righe della matrice d'adiacenza come byte, poi un intero per riga:
    # i bit si posano uno alla volta senza rifare ogni volta l'intero
    righe = [bytearray((n + 7) // 8) for _ in range(n)]
    for i, (x, y) in enumerate(perc):
        if not trasparente[y][x]:
            continue
        byte_i, bit_i = i >> 3, 1 << (i & 7)
        riga_i = righe[i]
        for a, b in campo_visivo(trasparente, (x, y)):
            j = numero[b][a]
            if j is not None and j != i:
                riga_i[j >> 3] |= 1 << (j & 7)
                righe[j][byte_i] |= bit_i  # la vista e' reciproca
    vista = [int.from_bytes(r, "little") for r in righe]
    passi = [0] * n
    insieme = set(perc)
    for i, (x, y) in enumerate(perc):
        for q in collaudo.vicini(x, y, insieme):
            passi[i] |= 1 << indice[q]

    vis, int_vis = sintassi(vista)
    acc, int_acc = sintassi(passi)
    classi = ["".join(classe(G.at(x, y), F, MODO, FUORI) for x in range(G.W)) for y in range(G.H)]
    return {
        "vista": vis,
        "accesso": acc,
        "vista_accesso_r": _r(pearson(int_vis, int_acc)),
        "simmetria": simmetria(classi),
        "pattern_2x2": pattern_2x2(classi),
    }
