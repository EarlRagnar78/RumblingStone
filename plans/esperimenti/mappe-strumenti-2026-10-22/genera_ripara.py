#!/usr/bin/env python3
"""
genera_ripara.py — generatore a seme + riparatore deterministico + misura.

Prova del 2026-10-22 (RICERCA-STRUMENTI-MAPPE.md §5). Scrive solo sotto la
cartella --out; i master del repo si leggono e basta.

Tre pezzi, ognuno deterministico:

1. GENERATORE (solo per luoghi nuovi). `bsp`: partizione binaria dello spazio,
   stanze nelle foglie, corridoi sull'albero ricoprente minimo dei centri (Prim,
   pareggi per coordinate): esce un albero, senza anelli, apposta. `grotta`:
   automa cellulare 4-5 (riempimento 45%, 5 passi), si tiene la regione piu'
   grande. Seme in `random.Random(seme)`; PG nella stanza piu' a ovest, nemici
   nella piu' lontana a passi, obiettivo nella foglia piu' isolata.
2. RIPARATORE. Ricerca locale a salita (hill climbing) sul voto di
   qualita_mappe.py: a ogni passo prova un insieme chiuso di mosse ordinate
   (aprire un muro sottile fra due tratti lontani, aprire un ingresso sul
   bordo, posare un blocco 4×2 o 3×3, posare una copertura, chiudere un vicolo
   vuoto), tiene la mossa che alza di piu' il voto senza far comparire un
   errore, a parita' quella che viene prima nell'ordine. Le celle FISSE
   (canone: creature, oggetti, porte, scale, la cornice) non si toccano.
3. MISURA. Voto e rilievi prima e dopo; l'elenco delle celle cambiate in A1.

Uso:
    python3 genera_ripara.py genera --tipo bsp|grotta --seme N [--out DIR]
    python3 genera_ripara.py ripara FILE.md[:N] [--out DIR] [--passi 8]
    python3 genera_ripara.py prova --out DIR     # tutto il giro del rapporto, due volte
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
import sys
from collections import deque
from pathlib import Path

from _comune import C, F, Q, QUI, R, REPO, griglia_md, impronta, mappe_di, voto_di


def errore(codice: str) -> bool:
    return C.CLASSE.get(codice) == "E" or Q.CLASSE.get(codice) == "E"

MURO, PAV_I, PAV_C = "🏰", "⬜", "🟤"
PAVIMENTI = {"⬜", "🟤", "🟫", "🟩"}


# --------------------------------------------------------------------------- generatori
def bsp(seme: int, W=30, H=22, minimo=6):
    rnd = random.Random(seme)
    g = [[MURO] * W for _ in range(H)]
    foglie = []

    def dividi(x, y, w, h, prof):
        if prof > 4 or (w < 2 * minimo and h < 2 * minimo):
            foglie.append((x, y, w, h))
            return
        orizz = h > w if abs(h - w) > 2 else rnd.random() < 0.5
        if orizz and h >= 2 * minimo:
            t = rnd.randint(minimo, h - minimo)
            dividi(x, y, w, t, prof + 1)
            dividi(x, y + t, w, h - t, prof + 1)
        elif w >= 2 * minimo:
            t = rnd.randint(minimo, w - minimo)
            dividi(x, y, t, h, prof + 1)
            dividi(x + t, y, w - t, h, prof + 1)
        else:
            foglie.append((x, y, w, h))

    dividi(1, 1, W - 2, H - 2, 0)
    stanze = []
    for x, y, w, h in foglie:
        rw, rh = rnd.randint(3, max(3, w - 2)), rnd.randint(3, max(3, h - 2))
        rx, ry = x + rnd.randint(0, w - rw - 1), y + rnd.randint(0, h - rh - 1)
        for yy in range(ry, ry + rh):
            for xx in range(rx, rx + rw):
                g[yy][xx] = PAV_I
        stanze.append((rx, ry, rw, rh))
    centri = [(x + w // 2, y + h // 2) for x, y, w, h in stanze]
    # Prim, con i pareggi decisi dalle coordinate
    dentro, archi = {0}, []
    while len(dentro) < len(centri):
        best = min(((abs(centri[a][0] - centri[b][0]) + abs(centri[a][1] - centri[b][1]), a, b)
                    for a in dentro for b in range(len(centri)) if b not in dentro))
        archi.append((best[1], best[2]))
        dentro.add(best[2])
    for a, b in archi:
        (x1, y1), (x2, y2) = centri[a], centri[b]
        for xx in range(min(x1, x2), max(x1, x2) + 1):
            g[y1][xx] = PAV_I
        for yy in range(min(y1, y2), max(y1, y2) + 1):
            g[yy][x2] = PAV_I
    _popola(g, centri, rnd)
    return g, ["@north N", "@tipo tattica interni"], f"BSP seme {seme}"


def grotta(seme: int, W=32, H=24):
    rnd = random.Random(seme)
    g = [[MURO if (x in (0, W - 1) or y in (0, H - 1) or rnd.random() < 0.45) else PAV_C
          for x in range(W)] for y in range(H)]
    for _ in range(5):
        n = [[sum(g[y + dy][x + dx] == MURO for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                  if 0 <= x + dx < W and 0 <= y + dy < H) if 0 < x < W - 1 and 0 < y < H - 1 else 9
              for x in range(W)] for y in range(H)]
        g = [[MURO if n[y][x] >= 5 else PAV_C for x in range(W)] for y in range(H)]
    # la regione piu' grande, le altre si chiudono
    viste, migliore = set(), set()
    for y in range(H):
        for x in range(W):
            if g[y][x] == PAV_C and (x, y) not in viste:
                reg, coda = {(x, y)}, deque([(x, y)])
                while coda:
                    a, b = coda.popleft()
                    for q in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                        if q not in reg and 0 <= q[0] < W and 0 <= q[1] < H and g[q[1]][q[0]] == PAV_C:
                            reg.add(q)
                            coda.append(q)
                viste |= reg
                if len(reg) > len(migliore) or (len(reg) == len(migliore) and min(reg) < min(migliore)):
                    migliore = reg
    g = [[PAV_C if (x, y) in migliore else MURO for x in range(W)] for y in range(H)]
    celle = sorted(migliore)
    centri = [celle[0], celle[len(celle) // 2], celle[-1]]
    _popola(g, centri, rnd)
    return g, ["@north N", "@tipo tattica caverna"], f"GROTTA seme {seme}"


def _popola(g, centri, rnd):
    """PG a ovest, nemici nella stanza piu' lontana a passi, obiettivo accanto."""
    H, W = len(g), len(g[0])
    start = min(centri)
    dist = {start: 0}
    coda = deque([start])
    while coda:
        a, b = coda.popleft()
        for q in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
            if q not in dist and 0 <= q[0] < W and 0 <= q[1] < H and g[q[1]][q[0]] in PAVIMENTI:
                dist[q] = dist[(a, b)] + 1
                coda.append(q)
    lontano = max(centri, key=lambda c: (dist.get(c, -1), c))

    def posa(centro, simbolo, n):
        cx, cy = centro
        anelli = sorted(((abs(x - cx) + abs(y - cy), y, x) for y in range(H) for x in range(W)
                         if g[y][x] in PAVIMENTI))
        for _, y, x in anelli[:n]:
            g[y][x] = simbolo
    posa(start, "🔵", 4)
    posa(lontano, "🔴", 4)
    posa((lontano[0] + 1, lontano[1] + 1), "⭐", 1)


# --------------------------------------------------------------------------- riparatore
def _fisse(g, canone: bool):
    """Le celle che il riparatore non tocca. Sempre: creature, icone, porte,
    scale e la cornice esterna salvo le aperture di ingresso. Con il canone,
    anche il pavimento a contatto di un oggetto o di una creatura."""
    H, W = len(g), len(g[0])
    fisse = set()
    for y in range(H):
        for x in range(W):
            c = g[y][x]
            if c not in PAVIMENTI and c != MURO:
                fisse.add((x, y))
                if canone:
                    fisse |= {(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    return fisse


def _dist(g, start):
    H, W = len(g), len(g[0])
    ok = lambda c: c not in (MURO,) and not F.get(c, {}).get("blocks_movement")  # noqa: E731
    d = {start: 0}
    coda = deque([start])
    while coda:
        a, b = coda.popleft()
        for q in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
            if q not in d and 0 <= q[0] < W and 0 <= q[1] < H and ok(g[q[1]][q[0]]):
                d[q] = d[(a, b)] + 1
                coda.append(q)
    return d


SFRUTTA_INGRESSI = False


def _dentro(x, y, W, H):
    """La cella interna davanti a una cella della cornice."""
    return (x, 1) if y == 0 else (x, H - 2) if y == H - 1 else (1, y) if x == 0 else (W - 2, y)


def _mosse(g, fisse, ambiente):
    """Le mosse candidate, in ordine fisso. Ogni mossa e' (nome, [(x, y, nuovo)])."""
    H, W = len(g), len(g[0])
    pav = PAV_C if ambiente == "caverna" else PAV_I
    cop = "🪨" if ambiente == "caverna" else "🧱"
    blocco = "🔺" if ambiente == "caverna" else "📦"
    libero = lambda x, y: 0 <= x < W and 0 <= y < H and not F.get(g[y][x], {}).get("blocks_movement")  # noqa: E731
    out = []
    # 1. scavare un passaggio dritto di 1-4 celle di muro fra due tratti lontani
    #    (scorciatoia di Jaquays, anello di Dormans)
    cand = []
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if not libero(x, y) or g[y][x] == MURO:
                continue
            for dx, dy in ((1, 0), (0, 1)):
                tratto = []
                a, b = x + dx, y + dy
                while 0 < a < W - 1 and 0 < b < H - 1 and g[b][a] == MURO and (a, b) not in fisse and len(tratto) < 4:
                    tratto.append((a, b))
                    a, b = a + dx, b + dy
                if tratto and libero(a, b) and g[b][a] != MURO:
                    d = _dist(g, (x, y)).get((a, b), 999)
                    guadagno = d - (len(tratto) + 1)
                    if guadagno >= 8:
                        cand.append((-guadagno, len(tratto), y, x, tuple(tratto)))
    out += [(f"scava{len(t)}", [(a, b, pav) for a, b in t]) for _, _, _, _, t in sorted(cand)[:12]]
    # 2. ingresso sul bordo: un muro della cornice con il pavimento dietro
    cand = []
    for x, y, nx, ny in ([(x, 0, x, 1) for x in range(1, W - 1)] + [(x, H - 1, x, H - 2) for x in range(1, W - 1)]
                         + [(0, y, 1, y) for y in range(1, H - 1)] + [(W - 1, y, W - 2, y) for y in range(1, H - 1)]):
        if g[y][x] == MURO and (x, y) not in fisse and g[ny][nx] in PAVIMENTI:
            cand.append((y, x))
    # un ingresso nuovo sta ad almeno 10 passi da quelli che ci sono: due varchi
    # nella stessa stanza contano due «tratti» per lo strumento, ma per Jaquays
    # sono un ingresso solo (la prima versione del riparatore l'aveva sfruttato)
    aperti = [(x, y) for x in range(W) for y in (0, H - 1) if libero(x, y)] + \
             [(x, y) for y in range(H) for x in (0, W - 1) if libero(x, y)]
    vicini_aperti = {}
    for o in aperti:
        for c, d in _dist(g, o).items():
            vicini_aperti[c] = min(d, vicini_aperti.get(c, 999))
    if SFRUTTA_INGRESSI:
        lontani = cand
    else:
        lontani = [(y, x) for y, x in cand if vicini_aperti.get(_dentro(x, y, W, H), 999) >= 10]
    out += [("ingresso", [(x, y, pav)]) for y, x in lontani[:: max(1, len(lontani) // 6)][:6]]
    # 3. un blocco 4x2, 2x4 o 3x3 nel pavimento, staccato da tutto di un quadretto
    cand = []
    for bw, bh in ((4, 2), (2, 4), (3, 3)):
        for y in range(2, H - bh - 1):
            for x in range(2, W - bw - 1):
                zona = [(x + i, y + j) for i in range(-1, bw + 1) for j in range(-1, bh + 1)]
                if all(g[b][a] in PAVIMENTI and (a, b) not in fisse for a, b in zona):
                    # piu' lontano dai muri e' meglio: il giro attorno resta largo
                    cx, cy = x + bw / 2, y + bh / 2
                    cand.append((abs(cx - W / 2) + abs(cy - H / 2), y, x, bw, bh))
    for _, y, x, bw, bh in sorted(cand)[:8]:
        out.append((f"blocco{bw}x{bh}", [(x + i, y + j, blocco) for i in range(bw) for j in range(bh)]))
    # 4. una copertura dove manca nel raggio di 2
    cand = []
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if g[y][x] in PAVIMENTI and (x, y) not in fisse:
                vicino = any(F.get(g[b][a], {}).get("cover") in ("half", "three_quarters", "total")
                             for a in range(max(0, x - 2), min(W, x + 3)) for b in range(max(0, y - 2), min(H, y + 3)))
                if not vicino:
                    cand.append((y, x))
    out += [("copertura", [(x, y, cop)]) for y, x in cand[:: max(1, len(cand) // 8)][:8]]
    # 5. chiudere un vicolo cieco vuoto
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if g[y][x] in PAVIMENTI and (x, y) not in fisse:
                n4 = sum(libero(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if n4 == 1:
                    out.append(("chiudi", [(x, y, MURO)]))
    return out


def _avvicinamento(m: dict, amb) -> float:
    """Quanto la mappa si avvicina alle soglie dello standard che il voto vede
    solo a scatti (0 o tutto). Serve a uscire dai plateau della salita: un
    secondo ingresso vale il rilievo solo quando c'e', ma il primo passo verso
    di esso si deve poter premiare [INFERRED: scelta di progetto, non una
    metrica pubblicata]. Ordinato dopo il voto, mai al posto suo."""
    s = 0.0
    if amb in ("interni", "caverna"):
        s += min(m.get("ingressi", 0), 2)
        s += min(m.get("anelli_strutturali", 0), 1)
    dist = m.get("distanza_min_m")
    if dist is not None:
        s -= max(0.0, dist - 54) / 54
    s -= max(0, m.get("vicoli_vuoti", 0) - 2) * 0.25
    s += min(m.get("copertura", 0.0), 0.5)
    return round(s, 4)


def _grid_dict(g, ann, titolo):
    testo = griglia_md(titolo, g, ann)
    return R.extract_maps(testo)[0], testo


def ripara(g, ann, titolo, file_ctx: Path, canone: bool, passi=8):
    g = [list(r) for r in g]
    amb = next((a.split()[2] for a in ann if a.startswith("@tipo") and len(a.split()) > 2), None)
    fisse = _fisse(g, canone)
    gd, _ = _grid_dict(g, ann, titolo)
    voto0, ril0, m0 = voto_di(file_ctx, 1, gd, metriche=True)
    e0 = sum(1 for r in ril0 if errore(r))
    storia, voto, ril, valutate = [], voto0, ril0, 0
    corrente = (voto0, _avvicinamento(m0, amb))
    for _ in range(passi):
        migliore = None
        for nome, cambi in _mosse(g, fisse, amb):
            prova = [r[:] for r in g]
            for x, y, s in cambi:
                prova[y][x] = s
            gd, _ = _grid_dict(prova, ann, titolo)
            v, r, m = voto_di(file_ctx, 1, gd, metriche=True)
            valutate += 1
            e = sum(1 for k in r if errore(k))
            punteggio = (v, _avvicinamento(m, amb))
            if e > e0 or v < voto or punteggio <= corrente:
                continue
            chiave = (punteggio, -len(cambi))
            if migliore is None or chiave > migliore[0]:
                migliore = (chiave, nome, cambi, prova, r)
        if migliore is None:
            break
        ((v, avv), _), nome, cambi, g, ril = migliore
        storia.append({"mossa": nome, "celle": [f"{R.col_label(x)}{y + 1:02d}={s}" for x, y, s in cambi],
                       "voto": v, "avvicinamento": avv})
        voto, corrente = v, (v, avv)
        fisse |= {(x, y) for x, y, _ in cambi}
    return g, {"voto_prima": voto0, "rilievi_prima": ril0, "voto_dopo": voto, "rilievi_dopo": ril,
               "mosse": storia, "valutazioni": valutate}


def _righe_da_grid(gdict):
    G = C.Griglia(gdict)
    return [[G.at(x, y) for x in range(G.W)] for y in range(G.H)]


# --------------------------------------------------------------------------- prova
CANONE = "07_il Portale Della Forgia Eterna/Mappe/hammerfist-372-1372/M7-F-fucina-grande-372.md"
GEMELLA = "07_il Portale Della Forgia Eterna/Mappe/hammerfist-372-1372/M7-E-gallerie-372.md"


def giro(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    esito = {"generate": [], "canone": None}
    for tipo, semi in (("bsp", (1, 2, 3)), ("grotta", (1, 2, 3))):
        for s in semi:
            g, ann, titolo = (bsp if tipo == "bsp" else grotta)(s)
            f = out / f"gen-{tipo}-{s}.md"
            dopo, rap = ripara(g, ann, titolo, f, canone=False)
            f.write_text(griglia_md(titolo, g, ann), encoding="utf-8")
            (out / f"gen-{tipo}-{s}-riparata.md").write_text(griglia_md(titolo + " (riparata)", dopo, ann),
                                                              encoding="utf-8")
            rap.update({"tipo": tipo, "seme": s})
            esito["generate"].append(rap)
    # canone: una copia, con la gemella accanto perche' @collega la trovi
    src = REPO / CANONE
    copia = out / src.name
    shutil.copyfile(src, copia)
    shutil.copyfile(REPO / GEMELLA, out / Path(GEMELLA).name)
    gd = mappe_di(copia)[0]
    righe = _righe_da_grid(gd)
    ann = list(gd["annotations"])
    dopo, rap = ripara(righe, ann, gd["title"], copia, canone=True)
    (out / (src.stem + "-riparata.md")).write_text(griglia_md(gd["title"], dopo, ann), encoding="utf-8")
    rap["file"] = CANONE
    esito["canone"] = rap
    return esito


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("genera")
    a1.add_argument("--tipo", choices=("bsp", "grotta"), required=True)
    a1.add_argument("--seme", type=int, required=True)
    a1.add_argument("--out", default=str(QUI / "out"))
    a2 = sub.add_parser("ripara")
    a2.add_argument("file")
    a2.add_argument("--out", default=str(QUI / "out"))
    a2.add_argument("--passi", type=int, default=8)
    a3 = sub.add_parser("prova")
    a3.add_argument("--out", default=str(QUI / "out" / "pipeline"))
    a = ap.parse_args(argv)
    if a.cmd == "genera":
        g, ann, titolo = (bsp if a.tipo == "bsp" else grotta)(a.seme)
        dopo, rap = ripara(g, ann, titolo, Path(a.out) / "gen.md", canone=False)
        print(griglia_md(titolo, dopo, ann))
        print(json.dumps(rap, ensure_ascii=False, indent=1))
    elif a.cmd == "ripara":
        p, _, n = a.file.partition(":")
        f = Path(p).resolve()
        gd = mappe_di(f)[int(n or 1) - 1]
        dopo, rap = ripara(_righe_da_grid(gd), list(gd["annotations"]), gd["title"], f, canone=True,
                           passi=a.passi)
        print(griglia_md(gd["title"], dopo, list(gd["annotations"])))
        print(json.dumps(rap, ensure_ascii=False, indent=1))
    else:
        out = Path(a.out)
        e1 = giro(out / "giro1")
        e2 = giro(out / "giro2")
        h1, h2 = impronta(e1), impronta(e2)
        file_uguali = all((out / "giro1" / p.name).read_bytes() == p.read_bytes()
                          for p in sorted((out / "giro2").iterdir()))
        e1["determinismo"] = {"giro1": h1, "giro2": h2, "rapporti_identici": h1 == h2,
                              "file_identici": file_uguali}
        (out / "esito.json").write_text(json.dumps(e1, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(json.dumps(e1, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
