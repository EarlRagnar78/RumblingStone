#!/usr/bin/env python3
"""render_map_pianta.py — il tema «pianta» delle mappe tattiche (ADR-0102).

Disegna un master a griglia-emoji con lo stile delle piante delle città della
valle (Rethmar, Dauth, Channathgate): carta chiara, roccia piena a tratteggio,
bordo della pietra viva rotto dove la roccia guarda una caverna o la terra e
dritto dove guarda un pavimento costruito, lastricato a corsi sfalsati, ciottoli
e crepe nelle caverne, croste sulla lava, increspature sull'acqua; i luoghi
numerati sono cerchi rossi con l'elenco sotto la mappa, come sulle piante, e la
scala è in metri.

Non cambia niente del master: ogni quadretto resta dove il master lo mette, la
roccia si sposta al più di un quarto di quadretto dal suo bordo, e oggetti di
scena, porte e segnalini sono quelli di `render_map_svg.py` (stessi simboli,
stessa rotazione delle chiusure). Il tema si sceglie con
`render_map_svg.py --tema pianta` e scrive in `rendered-pianta/`.

Solo libreria standard, come il renderer: la geometria resta sulla griglia e i
ritagli li fa l'SVG con i clipPath.
"""
from __future__ import annotations

import math
import random
import re

import render_map_svg as R
from dmcore import chiusure, legenda

CELL = R.CELL
MARGIN = 46
C = {
    "carta": "#f3e8cb", "piatto": "#eadcb8", "inchiostro": "#2e2316", "sbiadito": "#7a6a50",
    "roccia": "#7d6d58", "roccia_t": "#55493a", "lastre": "#e4d7b6", "lastre_b": "#b6a37c",
    "caverna": "#d8c9a3", "ciottoli": "#a8956d", "crepe": "#8b7a58",
    "lava": "#e8762b", "lava_c": "#5a2a12", "lava_b": "#ffcf6a",
    "acqua": "#8fbcd8", "acqua_b": "#3f7fa8", "marker": "#7a1f1f", "marker_t": "#fbf1dc",
}
COLORE = {
    "t_floor": C["lastre"], "t_dais": "#d9c48f", "t_cave": C["caverna"], "t_earth": "#cfb98d",
    "t_sand": "#e8d8a6", "t_grass": "#c4cf94", "t_veg": "#b3c588", "t_forest": "#a9bd82",
    "t_lava": C["lava"], "t_lethal": "#c0392b", "t_water": C["acqua"], "t_deep": "#5f97c0",
    "t_shallow": "#a9cfe0", "t_sewer": "#93a88f", "t_void": "#221c14", "t_telo": "#e6d7b2",
    "t_wall": C["roccia"], "t_struct": "#8a7a62", "t_mountain": "#8d7d63", "t_pillar": "#8a7a62",
}
# la roccia: dove guarda queste superfici il bordo si rompe (pietra viva)
NATURALI = {"t_cave", "t_earth", "t_sand", "t_grass", "t_veg", "t_forest", "t_lava", "t_water",
            "t_deep", "t_shallow", "t_void", "t_lethal"}
ROCCIA = {"t_wall", "t_mountain"}          # massa di roccia o muratura a tratteggio
BLOCCHI = {"t_struct", "t_pillar"}          # muratura a blocchi, bordo sempre dritto
ACQUE = {"t_water", "t_deep", "t_shallow", "t_sewer"}
AMPIEZZA = 0.24                             # spostamento massimo del bordo, in quadretti


def _n(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _corto(nome: str, n: int) -> str:
    """La voce di legenda che sta nella colonna: prima via la parentesi, poi si
    taglia all'ultima parola intera con i puntini, mai a metà parola."""
    if len(nome) <= n:
        return nome
    if "(" in nome and len(base := nome.split("(")[0].rstrip(" ,;:")) <= n:
        return base
    return nome[:n - 1].rsplit(" ", 1)[0].rstrip(" ,;:(") + "…"


def _rumore(x: float, y: float, seme: float) -> float:
    """Rumore liscio e deterministico in [-1, 1]: lo stesso punto, lo stesso valore."""
    v = (math.sin(x * 1.7 + y * 0.9 + seme) * 0.5 + math.sin(x * 3.1 - y * 2.3 + seme * 1.3) * 0.3
         + math.sin(x * 6.7 + y * 5.9 + seme * 0.7) * 0.2)
    return max(-1.0, min(1.0, v))


def _anello(loop, naturale, ox, oy, seme):
    """Un contorno di celle in px: i lati naturali divisi e spostati lungo la normale."""
    out = []
    n = len(loop)
    for i in range(n):
        a, b = loop[i], loop[(i + 1) % n]
        nat = naturale(a, b)
        passi = 4 if nat else 1
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = dy / L, -dx / L
        for k in range(passi):
            t = k / passi
            x, y = a[0] + dx * t, a[1] + dy * t
            if nat and k > 0:
                d = _rumore(x, y, seme) * AMPIEZZA
                x, y = x + nx * d, y + ny * d
            out.append((ox + x * CELL, oy + y * CELL))
    return out


def _d(pts) -> str:
    return "M" + "L".join(f"{_n(x)} {_n(y)}" for x, y in pts) + "Z"


def _celle_path(celle, ox, oy) -> str:
    return "".join(_d([(ox + x * CELL, oy + y * CELL) for x, y in R._dedup_collinear(lp)])
                   for lp in R._trace_loops(celle))


def _testo(x, y, t, size=11, anchor="start", fill=None, weight="normal", style="normal", alone=False):
    h = f' stroke="{C["carta"]}" stroke-width="3" paint-order="stroke"' if alone else ""
    return (f'<text x="{_n(x)}" y="{_n(y)}" font-size="{_n(size)}" text-anchor="{anchor}" '
            f'fill="{fill or C["inchiostro"]}" font-weight="{weight}" font-style="{style}"{h}>'
            f'{R._esc(str(t))}</text>')


def _a_capo(t: str, larghezza: int) -> list[str]:
    righe, riga = [], ""
    for p in t.split():
        if riga and len(riga) + 1 + len(p) > larghezza:
            righe.append(riga)
            riga = p
        else:
            riga = f"{riga} {p}".strip()
    return righe + ([riga] if riga else [])


def render_pianta(grid: dict, source_name: str, stampa: bool = False, parte: str = "mappa") -> str:
    """`stampa`: il modo di stampa di render_map_svg (LARGHEZZA_STAMPA_PT), con
    `parte` "mappa" o "legenda" (luoghi, zone, percorsi e legenda)."""
    rows = grid["rows"]
    row_nums = sorted(rows)
    nr = len(row_nums)
    nc = max(len(c) for c in rows.values())
    gw, gh = nc * CELL, nr * CELL
    scala = grid.get("scale_m") or 1.5
    ann = R.parse_annotations(grid.get("annotations", []) or [])
    base = R._resolve_bases(rows, nc)
    seme = sum(ord(ch) for ch in grid["title"]) % 997 / 10
    rng = random.Random(int(seme * 10))
    simboli = R.SYMBOLS
    luci = legenda.luci()
    locale = grid.get("local_legend") or {}

    def em(r, c):
        if not (0 <= r < nr) or c < 0:
            return None
        riga = rows[row_nums[r]]
        return riga[c] if c < len(riga) else None

    def pat(r, c):
        return base[row_nums[r]][c] if 0 <= r < nr and 0 <= c < nc else None

    # un oggetto o un'unità eredita il terreno della cella a sinistra
    # (_resolve_bases): accanto a un pilastro finirebbe sulla roccia, accanto a
    # una colata nella lava. Qui prende il piano più comune fra i quattro vicini.
    def diretto(r, c):
        e = em(r, c)
        sp = simboli.get(e) if e else None
        return sp["pat"] if sp and sp["mode"] == "fill" else None
    base = {rn: list(v) for rn, v in base.items()}
    for r in range(nr):
        for c in range(nc):
            p = pat(r, c)
            if p is None or diretto(r, c):
                continue
            piani = [q for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))
                     if (q := diretto(rr, cc)) and q not in ROCCIA and q not in BLOCCHI and q != "t_pillar"]
            if piani:
                # a parità resta il terreno di prima, poi l'ordine alfabetico
                base[row_nums[r]][c] = max(sorted(set(piani)), key=lambda q: (piani.count(q), q == p))

    usati = sorted({e for r in range(nr) for c in range(nc) if (e := em(r, c))})
    # sotto un pilastro isolato c'è il pavimento dei vicini
    per_pat: dict[str, set] = {}
    pilastri = set()
    for r in range(nr):
        for c in range(nc):
            p = pat(r, c)
            if p is None:
                continue
            per_pat.setdefault(p, set()).add((r, c))
            if p == "t_pillar":
                pilastri.add((r, c))
    roccia = set().union(*(per_pat.get(p, set()) for p in ROCCIA))
    blocchi = set().union(*(per_pat.get(p, set()) for p in BLOCCHI))
    solidi = roccia | blocchi

    def piano_vicino(r, c):
        for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1), (r - 1, c - 1), (r + 1, c + 1)):
            p = pat(rr, cc)
            if p and p not in ROCCIA and p not in BLOCCHI and p != "t_telo":
                return p
        return "t_floor"
    sotto = {}
    for (r, c) in blocchi:
        sotto.setdefault(piano_vicino(r, c), set()).add((r, c))

    # ---- impaginazione: titolo, piatto, elenco dei luoghi e legenda sotto
    width = max(MARGIN * 2 + gw, 760)
    ox = MARGIN + (width - 2 * MARGIN - gw) / 2
    oy = 82
    colonne = 3 if width >= 980 else 2
    largo = (width - 2 * MARGIN) / colonne
    car = int(largo / 6.3)
    righe_luoghi = []
    for m in ann["marks"]:
        righe_luoghi.append((m["n"], _a_capo(m["text"], car - 4)))
    leg = [e for e in usati if e in simboli] + [e for e in usati if e not in simboli]
    y_sb = oy + gh + 30
    y_l = y_sb + 34
    h_luoghi = 0
    if righe_luoghi:
        per_col = math.ceil(len(righe_luoghi) / colonne)
        cols = [righe_luoghi[i:i + per_col] for i in range(0, len(righe_luoghi), per_col)]
        h_luoghi = 26 + max(sum(len(t) * 13 + 6 for _, t in col) for col in cols)
    y_leg = y_l + h_luoghi + (10 if righe_luoghi else 0)
    righe_leg = math.ceil(len(leg) / colonne)
    height = int(y_leg + 26 + righe_leg * 19 + 22)
    u = width / R.LARGHEZZA_STAMPA_PT
    cz = R.CORPO_STAMPA_PT * u
    sfalsa = nc > 26
    voci_st: list[tuple[str, str, list[str]]] = []
    if stampa and parte == "legenda":
        k_leg = R.CORPO_STAMPA_PT * u / 9.5
        larga_v = width / k_leg
        # la voce intera, a capo nella colonna: la parentesi porta la regola
        # (copertura, blocca la vista) e in stampa non si taglia
        mezza = (larga_v - 28) / 2
        car_l = int((mezza - 30) / 5.5)
        voci_leg = [(e, _a_capo(_nome_voce(e, simboli, locale), car_l)) for e in leg]
        alti = [19 + 13 * (len(t) - 1) for _, t in voci_leg]
        taglio = _taglio(alti)
        h_leg = 26 + max(sum(alti[:taglio]), sum(alti[taglio:])) + 10
        # luoghi, zone e percorsi su una colonna; su due se la legenda non
        # starebbe più nella pagina (21 cm) a 7,4 pt
        for col_v in (1, 2):
            larga_c = (larga_v - 28) / col_v
            car_v = (larga_c - 24 - (10 if col_v > 1 else 0)) / 5.5
            voci_st = [("mark", str(m["n"]), _a_capo(
                f"{R.col_label(m['coord'][0])}{m['coord'][1]} — {m['text']}", car_v)) for m in ann["marks"]]
            voci_st += [("zona", R._lettera_zona(iz), _a_capo(R._testi_indicazioni(
                {"marks": [], "paths": [], "zones": [z]})[0], car_v)) for iz, z in enumerate(ann["zones"])]
            voci_st += [("path", pa["color"], _a_capo(R._testi_indicazioni(
                {"marks": [], "paths": [pa], "zones": []})[0], car_v)) for pa in ann["paths"]]
            alti_v = [15 + 13 * (len(t) - 1) for _, _, t in voci_st]
            taglio_v = _taglio(alti_v) if col_v > 1 else len(alti_v)
            alto_v = 30 + 26 + max(sum(alti_v[:taglio_v]), sum(alti_v[taglio_v:]))
            y_leg_v = alto_v + 16 if voci_st else 22
            height = round((y_leg_v + h_leg) * k_leg)
            if height <= width * 590 / R.LARGHEZZA_STAMPA_PT:
                break
    elif stampa:
        # una mappa alta la pagina la stringerebbe in altezza (21 cm, 595 pt) e
        # le scritte tornerebbero sotto i 7 pt: allora si allarga il foglio
        # finché il rapporto è quello della pagina, con la mappa al centro
        testa = 23 + (16.5 if sfalsa else 8.5) + 11 + 12
        if gh > (590 - testa) * u:
            width = round(R.LARGHEZZA_STAMPA_PT * gh / (590 - testa))
            ox = MARGIN + (width - 2 * MARGIN - gw) / 2
            u = width / R.LARGHEZZA_STAMPA_PT
            cz = R.CORPO_STAMPA_PT * u
        oy = round(23 * u + (16.5 if sfalsa else 8.5) * u)
        y_sb = round(oy + gh + 11 * u)
        height = round(y_sb + 12 * u)

    o: list[str] = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{_n(width)}" height="{height}" '
                    f'viewBox="0 0 {_n(width)} {height}" font-family="{R.FONT}">']
    defs = ["<defs>", R._stile_font()]
    defs.append(f'<clipPath id="pt-telaio"><rect x="{_n(ox)}" y="{oy}" width="{gw}" height="{gh}"/></clipPath>')
    defs.append('<filter id="pt-ombra" x="-10%" y="-10%" width="120%" height="120%">'
                '<feGaussianBlur stdDeviation="2.6"/></filter>')
    defs.append('<filter id="pt-grana" x="0" y="0" width="100%" height="100%"><feTurbulence '
                'type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/><feColorMatrix '
                'values="0 0 0 0 0.3 0 0 0 0 0.24 0 0 0 0 0.14 0 0 0 0.09 0"/><feComposite '
                'operator="over" in2="SourceGraphic"/></filter>')
    defs.append('<radialGradient id="pt-luce"><stop offset="0" stop-color="#ffd27a" stop-opacity="0.5"/>'
                '<stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>')

    # ---- la roccia: contorni con i lati naturali rotti
    def naturale_tra(a, b):
        # il lato a→b di un contorno di celle solide (y in giù): fuori è la cella a
        # sinistra del verso, dentro quella a destra. Si frastaglia la roccia viva
        # e la roccia che dà su un terreno naturale; mai i blocchi squadrati.
        (x0, y0), (x1, y1) = a, b
        if y0 == y1:
            c = min(x0, x1)
            fuori, dentro = (y0 - 1, c), (y0, c)
            if x1 < x0:
                fuori, dentro = dentro, fuori
        else:
            r = min(y0, y1)
            fuori, dentro = (r, x0), (r, x0 - 1)
            if y1 < y0:
                fuori, dentro = dentro, fuori
        p_dentro = pat(*dentro)
        if p_dentro in BLOCCHI:
            return False
        return p_dentro == "t_mountain" or pat(*fuori) in NATURALI

    anelli_roccia = [_anello(lp, naturale_tra, ox, oy, seme) for lp in R._trace_loops(roccia)] if roccia else []
    d_roccia = "".join(_d(a) for a in anelli_roccia)
    if d_roccia:
        defs.append(f'<clipPath id="pt-roccia"><path d="{d_roccia}" clip-rule="evenodd"/></clipPath>')
    pav = per_pat.get("t_floor", set()) | per_pat.get("t_dais", set()) | sotto.get("t_floor", set())
    if pav:
        defs.append(f'<clipPath id="pt-pav"><path d="{_celle_path(pav, ox, oy)}" clip-rule="evenodd"/></clipPath>')
    calpestabile = {(r, c) for r in range(nr) for c in range(nc)} - solidi
    if calpestabile:
        defs.append(f'<clipPath id="pt-cam"><path d="{_celle_path(calpestabile, ox, oy)}" '
                    f'clip-rule="evenodd"/></clipPath>')
    props = set()
    for e in usati:
        sp = simboli.get(e)
        if sp and sp.get("prop"):
            props.update(R.VARIANTS.get(sp["prop"], [sp["prop"]]))
    for p in sorted(props):
        defs.append(R.PROPS[p])
    for col in sorted({simboli[e]["fill"] for e in usati if e in simboli and simboli[e]["mode"] == "unit"}):
        defs.append(R._unit_gradient(col))
    noto = {e: v for e in usati if e not in simboli and (v := R._simbolo_noto(e))}
    for e in sorted(noto):
        defs.append(noto[e][1])
    defs.append("</defs>")
    o.extend(defs)
    w = o.append
    if stampa and parte == "legenda":
        w(f'<rect width="{_n(width)}" height="{height}" fill="{C["carta"]}"/>')
        w(f'<g transform="scale({R._n(k_leg)})">')
        if voci_st:
            w(_testo(14, 30, "Luoghi, zone e percorsi", 13.5, weight="bold"))
        for kk, (tipo, segno, righe) in enumerate(voci_st):
            x = 14 + (kk >= taglio_v) * larga_c
            yy = 56 + sum(alti_v[taglio_v if kk >= taglio_v else 0:kk])
            if tipo == "mark":
                w(f'<circle cx="{_n(x + 8)}" cy="{_n(yy - 4)}" r="8" fill="{C["marker"]}"/>')
                w(_testo(x + 8, yy - 0.5, segno, 9.5, "middle", C["marker_t"], "bold"))
            elif tipo == "zona":
                w(f'<rect x="{_n(x)}" y="{_n(yy - 12)}" width="16" height="14" rx="2" fill="none" '
                  f'stroke="{C["marker"]}" stroke-width="1.4" stroke-dasharray="4 3"/>')
                w(_testo(x + 8, yy - 1.5, segno, 9.5, "middle", C["marker"], style="italic"))
            else:
                w(f'<line x1="{_n(x)}" y1="{_n(yy - 4)}" x2="{_n(x + 16)}" y2="{_n(yy - 4)}" stroke="{segno}" '
                  f'stroke-width="2" stroke-dasharray="6 3"/>')
            for j, riga in enumerate(righe):
                w(_testo(x + 24, yy + j * 13, riga, 11))
        w(_testo(14, y_leg_v + 8, "Legenda", 13.5, weight="bold"))
        for kk, (e, righe) in enumerate(voci_leg):
            cx_ = 14 + (kk >= taglio) * mezza
            yy = y_leg_v + 30 + sum(alti[taglio if kk >= taglio else 0:kk])
            _voce_legenda(w, e, cx_, yy, simboli, noto, locale, righe=righe)
        w("</g>")
        w("</svg>")
        return "\n".join(o)

    # ---- carta, titolo
    w(f'<rect width="{_n(width)}" height="{height}" fill="{C["carta"]}" filter="url(#pt-grana)"/>')
    if stampa:
        corpo = 9 * u
        comprimi = R._corpo_titolo(grid["title"], width - 2 * MARGIN - 24, corpo)[0] < corpo
        spazio_t = width - 2 * MARGIN - 24
    else:
        corpo, comprimi = R._corpo_titolo(grid["title"], width - 2 * MARGIN, 21.0)
        spazio_t = width - 2 * MARGIN
    stretto = (f' textLength="{_n(spazio_t)}" lengthAdjust="spacingAndGlyphs"' if comprimi else "")
    w(f'<text x="{MARGIN}" y="{_n(12 * u) if stampa else 34}" font-size="{_n(corpo)}" font-weight="bold" '
      f'fill="{C["inchiostro"]}"{stretto}>{R._esc(grid["title"])}</text>')
    lato = f"{nc * scala:g} × {nr * scala:g} m · quadretto di {scala:g} m · {nc}×{nr} quadretti"
    w(_testo(MARGIN, 21 * u if stampa else 54, lato.replace(".", ","), cz if stampa else 12,
             fill=C["sbiadito"], style="italic"))

    # ---- pavimenti
    w(f'<rect x="{_n(ox)}" y="{oy}" width="{gw}" height="{gh}" fill="{C["piatto"]}"/>')
    w('<g clip-path="url(#pt-telaio)">')
    regioni = {p: set(v) for p, v in per_pat.items() if p not in ROCCIA and p not in BLOCCHI}
    for p, v in sotto.items():
        regioni.setdefault(p, set()).update(v)
    ordine = [p for p in R.Z_ORDER if p in regioni] + sorted(p for p in regioni if p not in R.Z_ORDER)
    for p in ordine:
        col = COLORE.get(p) or C["lastre"]
        d = _celle_path(regioni[p], ox, oy)
        # il bordo largo dello stesso colore copre la roccia che si ritira
        w(f'<path d="{d}" fill="{col}" fill-rule="evenodd" stroke="{col}" stroke-width="{_n(CELL * 0.6)}" '
          f'stroke-linejoin="round"/>')
    for p in ordine:
        celle = sorted(regioni[p])
        if p in ("t_floor", "t_dais"):
            continue
        if p in ("t_cave", "t_earth"):
            for (r, c) in celle:
                for _ in range(3):
                    x = ox + (c + rng.random()) * CELL
                    y = oy + (r + rng.random()) * CELL
                    rr = rng.uniform(0.7, 2.3)
                    w(f'<ellipse cx="{_n(x)}" cy="{_n(y)}" rx="{_n(rr)}" ry="{_n(rr * 0.7)}" '
                      f'fill="{C["ciottoli"]}" stroke="{C["sbiadito"]}" stroke-width="0.35" opacity="0.8"/>')
                if rng.random() < 0.3:
                    x, y = ox + (c + rng.random()) * CELL, oy + (r + rng.random()) * CELL
                    a = rng.uniform(0, 6.28)
                    pts = [(x, y)]
                    for _ in range(rng.randint(3, 5)):
                        a += rng.uniform(-0.9, 0.9)
                        x, y = x + math.cos(a) * rng.uniform(3, 7), y + math.sin(a) * rng.uniform(3, 7)
                        pts.append((x, y))
                    w(f'<polyline points="{" ".join(f"{_n(a_)},{_n(b_)}" for a_, b_ in pts)}" fill="none" '
                      f'stroke="{C["crepe"]}" stroke-width="0.6" opacity="0.7"/>')
        elif p == "t_sand":
            for (r, c) in celle:
                for _ in range(6):
                    w(f'<circle cx="{_n(ox + (c + rng.random()) * CELL)}" cy="{_n(oy + (r + rng.random()) * CELL)}" '
                      f'r="0.6" fill="#b49a66" opacity="0.7"/>')
        elif p in ("t_grass", "t_veg"):
            for (r, c) in celle:
                for _ in range(3):
                    x, y = ox + (c + rng.random()) * CELL, oy + (r + rng.random()) * CELL
                    w(f'<path d="M{_n(x)} {_n(y)}l-1.6 -3.2M{_n(x)} {_n(y)}l0 -3.8M{_n(x)} {_n(y)}l1.6 -3.2" '
                      f'stroke="#869a5c" stroke-width="0.7" fill="none" stroke-linecap="round"/>')
        elif p == "t_forest":
            for (r, c) in celle:
                cx, cy = ox + (c + 0.5) * CELL + rng.uniform(-3, 3), oy + (r + 0.5) * CELL + rng.uniform(-3, 3)
                w(R._canopy(round(cx, 1), round(cy, 1), round(CELL * rng.uniform(0.42, 0.55), 1)))
        elif p == "t_lava":
            for (r, c) in celle:
                for _ in range(2):
                    x, y = ox + (c + rng.random()) * CELL, oy + (r + rng.random()) * CELL
                    k = rng.randint(5, 7)
                    rr = rng.uniform(2.5, 6.5)
                    pts = [(x + math.cos(i * 6.28 / k) * rr * rng.uniform(0.6, 1.2),
                            y + math.sin(i * 6.28 / k) * rr * rng.uniform(0.6, 1.2)) for i in range(k)]
                    w(f'<path d="{_d(pts)}" fill="{C["lava_c"]}" opacity="0.75" stroke="{C["lava_b"]}" '
                      f'stroke-width="0.6"/>')
        elif p in ACQUE:
            for (r, c) in celle:
                x, y = ox + (c + rng.uniform(0.1, 0.6)) * CELL, oy + (r + rng.uniform(0.2, 0.8)) * CELL
                w(f'<path d="M{_n(x)} {_n(y)}q3 -2.4 6 0t6 0" fill="none" stroke="{C["acqua_b"]}" '
                  f'stroke-width="0.7" opacity="0.6"/>')
        elif p == "t_void":
            pass
        elif p == "t_lethal":
            d = "".join(f"M{_n(ox + c * CELL)} {_n(oy + (r + 1) * CELL)}l{CELL} {-CELL}" for (r, c) in celle)
            w(f'<path d="{d}" stroke="#7a1f1f" stroke-width="1.2" opacity="0.5"/>')
        elif p == "t_telo":
            pass
    # lastricato: corsi di lastre sfalsate, mezzo quadretto per uno
    if pav:
        h = CELL / 2
        d = []
        for k in range(int(gh / h) + 1):
            y = oy + k * h
            d.append(f"M{_n(ox)} {_n(y)}h{gw}")
            x = ox - CELL + (k % 2) * CELL * 0.5
            while x < ox + gw:
                x += CELL * rng.choice((0.75, 1.0, 1.0, 1.25))
                d.append(f"M{_n(x)} {_n(y)}v{_n(h)}")
        w(f'<path d="{"".join(d)}" stroke="{C["lastre_b"]}" stroke-width="0.7" fill="none" clip-path="url(#pt-pav)"/>')
        usura = []
        for (r, c) in sorted(pav):
            if rng.random() < 0.12:
                usura.append(f'<rect x="{_n(ox + c * CELL + rng.uniform(0, CELL / 2))}" '
                             f'y="{_n(oy + r * CELL + (rng.random() < 0.5) * h)}" width="{_n(CELL * 0.75)}" '
                             f'height="{_n(h)}" fill="#8a7550" opacity="0.08"/>')
        o.extend(usura)
        dais = per_pat.get("t_dais", set())
        if dais:
            w(f'<path d="{_celle_path(dais, ox, oy)}" fill="none" stroke="{C["sbiadito"]}" stroke-width="1.6"/>')
    # acque e lava: la riva
    for p in [*sorted(ACQUE), "t_lava", "t_void"]:
        if p in regioni:
            col = C["lava_b"] if p == "t_lava" else (C["inchiostro"] if p == "t_void" else C["acqua_b"])
            w(f'<path d="{R._region_path(regioni[p], ox, oy)}" fill="none" stroke="{col}" stroke-width="1.3" '
              f'opacity="0.85"/>')
    # teli di tenda
    if "t_telo" in regioni:
        telo = regioni["t_telo"]
        d = _celle_path(telo, ox, oy)
        w(f'<path d="{d}" fill="#1d160d" opacity="0.3" filter="url(#pt-ombra)" transform="translate(2,3)"/>')
        w(f'<path d="{d}" fill="{COLORE["t_telo"]}" stroke="{C["inchiostro"]}" stroke-width="1.6"/>')
        cuciture = "".join(f"M{_n(ox + c * CELL)} {_n(oy + r * CELL + CELL / 2)}h{CELL}" for (r, c) in sorted(telo))
        w(f'<path d="{cuciture}" stroke="#b9a578" stroke-width="0.7" fill="none"/>')

    # ---- la roccia
    if d_roccia:
        w(f'<path d="{d_roccia}" fill="#1d160d" fill-rule="evenodd" opacity="0.35" filter="url(#pt-ombra)" '
          f'transform="translate(1.5,2.5)"/>')
        w(f'<path d="{d_roccia}" fill="{C["roccia"]}" fill-rule="evenodd"/>')
        # tratteggio: gruppi di tratti fitti lungo il bordo e radi dentro (alla Dyson)
        vicino = {(r, c) for (r, c) in roccia
                  if any((rr, cc) not in solidi and 0 <= rr < nr and 0 <= cc < nc
                         for rr in (r - 1, r, r + 1) for cc in (c - 1, c, c + 1))}
        tratti = []
        passo = CELL / 4
        for (r, c) in sorted(roccia):
            fitto = (r, c) in vicino
            for i in range(4):
                for j in range(4):
                    if not fitto and rng.random() > 0.16:
                        continue
                    x = ox + c * CELL + (i + 0.5) * passo + rng.uniform(-2, 2)
                    y = oy + r * CELL + (j + 0.5) * passo + rng.uniform(-2, 2)
                    a = rng.uniform(0, math.pi)
                    for k in (-1, 0, 1) if fitto else (-0.5, 0.5):
                        dx, dy = math.cos(a) * 3.0, math.sin(a) * 3.0
                        sx, sy = -math.sin(a) * k * 1.9, math.cos(a) * k * 1.9
                        tratti.append(f"M{_n(x - dx + sx)} {_n(y - dy + sy)}L{_n(x + dx + sx)} {_n(y + dy + sy)}")
        w(f'<path d="{"".join(tratti)}" stroke="{C["roccia_t"]}" stroke-width="0.85" stroke-linecap="round" '
          f'fill="none" clip-path="url(#pt-roccia)"/>')
        w(f'<path d="{d_roccia}" fill="none" stroke="{C["inchiostro"]}" stroke-width="2" stroke-linejoin="round"/>')
    # muratura a blocchi e pilastri: conci dritti
    if blocchi:
        d = _celle_path(blocchi, ox, oy)
        w(f'<path d="{d}" fill="#1d160d" opacity="0.3" filter="url(#pt-ombra)" transform="translate(2,3)"/>')
        w(f'<path d="{d}" fill="{COLORE["t_struct"]}" fill-rule="evenodd" stroke="{C["inchiostro"]}" '
          f'stroke-width="1.6"/>')
        conci = []
        for (r, c) in sorted(blocchi):
            x, y = ox + c * CELL, oy + r * CELL
            conci.append(f"M{_n(x)} {_n(y + CELL / 2)}h{CELL}M{_n(x + CELL * (0.5 if r % 2 else 0.25))} {_n(y)}"
                         f"v{_n(CELL / 2)}M{_n(x + CELL * (0.75 if r % 2 else 0.5))} {_n(y + CELL / 2)}v{_n(CELL / 2)}")
        w(f'<path d="{"".join(conci)}" stroke="#5f523f" stroke-width="0.7" fill="none" opacity="0.8"/>')

    # ---- griglia: chiara dove si cammina, appena accennata sulla roccia
    gd = "".join(f"M{_n(ox + c * CELL)} {oy}v{gh}" for c in range(nc + 1)) + \
        "".join(f"M{_n(ox)} {oy + r * CELL}h{gw}" for r in range(nr + 1))
    if calpestabile:
        w(f'<path d="{gd}" stroke="{C["inchiostro"]}" stroke-width="0.5" opacity="0.24" fill="none" '
          f'clip-path="url(#pt-cam)"/>')
    w(f'<path d="{gd}" stroke="{C["carta"]}" stroke-width="0.5" opacity="0.1" fill="none"/>')

    # ---- oggetti di scena e segnalini, come nel renderer (porte girate sul muro)
    def at(c_, r_):
        return em(r_, c_)
    versi = chiusure.versi_dichiarati(grid.get("annotations", []) or [])
    aloni = []
    for r, rn in enumerate(row_nums):
        for c in range(nc):
            e = em(r, c)
            if e is None:
                continue
            sp = simboli.get(e)
            x, y = ox + c * CELL, oy + r * CELL
            cx, cy = x + CELL / 2, y + CELL / 2
            if e in luci:
                aloni.append((cx, cy, luci[e][0]))
            if sp and sp["mode"] == "unit":
                rr = CELL * 0.36
                w(f'<circle cx="{_n(cx + 1.2)}" cy="{_n(cy + 2)}" r="{_n(rr)}" fill="#1d160d" opacity="0.3"/>')
                w(f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{_n(rr)}" fill="url(#{R._grad_id(sp["fill"])})" '
                  f'stroke="{C["inchiostro"]}" stroke-width="1.4"/>')
            elif sp and sp.get("prop"):
                var = R.VARIANTS.get(sp["prop"], [sp["prop"]])
                prop = var[(r * 7 + c * 13) % len(var)]
                ns = chiusure.e_chiusura(e) and chiusure.asse_da_disegnare(
                    at, c, r, R.col_label(c), rn, versi) == chiusure.NS
                rx_, ry_ = (4.5, 9) if ns else (9, 4.5)
                w(f'<ellipse cx="{_n(cx + 1)}" cy="{_n(cy + 3)}" rx="{rx_}" ry="{ry_}" fill="#1d160d" opacity="0.18"/>')
                ruota = f' transform="rotate(90 {_n(cx)} {_n(cy)})"' if ns else ""
                w(f'<use href="#{prop}" x="{_n(x)}" y="{_n(y)}" width="{CELL}" height="{CELL}"{ruota}/>')
            elif sp is None:
                if e in noto:
                    w(f'<use href="#{noto[e][0]}" x="{_n(x + 5)}" y="{_n(y + 5)}" width="{CELL - 10}" '
                      f'height="{CELL - 10}"/>')
                else:
                    w(f'<text x="{_n(cx)}" y="{_n(cy + 6)}" font-size="17" text-anchor="middle">{e}</text>')
    for cx, cy, q in aloni:
        w(f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{_n(CELL * min(3.0, max(1.2, q / 3)))}" fill="url(#pt-luce)"/>')

    # ---- zone, percorsi e luoghi numerati
    r0 = row_nums[0]

    def centro(cella):
        c_, rn_ = cella
        return ox + c_ * CELL + CELL / 2, oy + (rn_ - r0) * CELL + CELL / 2
    for iz, z in enumerate(ann["zones"]):
        (ax, ay), (bx, by) = z["a"], z["b"]
        x0, y0 = ox + min(ax, bx) * CELL, oy + (min(ay, by) - r0) * CELL
        w(f'<rect x="{_n(x0)}" y="{_n(y0)}" width="{_n((abs(bx - ax) + 1) * CELL)}" '
          f'height="{_n((abs(by - ay) + 1) * CELL)}" fill="none" stroke="{C["marker"]}" stroke-width="1.4" '
          f'stroke-dasharray="6 4" opacity="0.85"/>')
        if stampa:
            w(f'<rect x="{_n(x0 + 2)}" y="{_n(y0 + 2)}" width="{_n(cz * 0.9)}" height="{_n(cz * 1.05)}" '
              f'rx="2" fill="{C["carta"]}" opacity="0.9"/>')
            w(_testo(x0 + 2 + cz * 0.45, y0 + 2 + cz * 0.8, R._lettera_zona(iz), cz, "middle",
                     C["marker"], style="italic"))
        else:
            w(_testo(x0 + 4, y0 + 13, z["text"], 10.5, fill=C["marker"], weight="bold", alone=True))
    for p in ann["paths"]:
        pts = [centro(c_) for c_ in p["coords"]]
        if p["loop"]:
            pts.append(pts[0])
        d = "M" + "L".join(f"{_n(x)} {_n(y)}" for x, y in pts)
        w(f'<path d="{d}" fill="none" stroke="{C["carta"]}" stroke-width="3.6" opacity="0.6" '
          f'stroke-linejoin="round"/>')
        w(f'<path d="{d}" fill="none" stroke="{p["color"]}" stroke-width="1.9" stroke-dasharray="7 4" '
          f'stroke-linejoin="round" stroke-linecap="round"/>')
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        w(R._arrowhead(x1, y1, x2, y2, p["color"]))
    for m in ann["marks"]:
        cx, cy = centro(m["coord"])
        bx, by = cx + CELL * 0.32, cy - CELL * 0.32
        w(f'<circle cx="{_n(bx)}" cy="{_n(by)}" r="{_n(cz * 0.68) if stampa else 8.5}" fill="{C["marker"]}" '
          f'stroke="{C["marker_t"]}" stroke-width="1.4"/>')
        w(_testo(bx, by + (cz * 0.36 if stampa else 3.6), m["n"], cz if stampa else 10, "middle",
                 C["marker_t"], "bold"))
    w("</g>")

    # ---- cornice, coordinate, rosa, scala
    w(f'<rect x="{_n(ox)}" y="{oy}" width="{gw}" height="{gh}" fill="none" stroke="{C["inchiostro"]}" '
      f'stroke-width="2"/>')
    for c in range(nc):
        if stampa:
            w(_testo(ox + c * CELL + CELL / 2, oy - (10.5 if sfalsa and c % 2 else 2.5) * u, R.col_label(c),
                     cz, "middle", C["sbiadito"]))
        else:
            w(_testo(ox + c * CELL + CELL / 2, oy - 7, R.col_label(c), 9, "middle", C["sbiadito"]))
    for r, rn in enumerate(row_nums):
        if stampa:
            w(_testo(ox - 4, oy + r * CELL + CELL / 2 + 0.36 * cz, f"{rn:02d}", cz, "end", C["sbiadito"]))
        else:
            w(_testo(ox - 7, oy + r * CELL + CELL / 2 + 3, f"{rn:02d}", 9, "end", C["sbiadito"]))
    if stampa:
        w(R._compass_svg(ox + gw - 26, oy + 34, 15, ann["north"], cz))
    else:
        w(R._compass_svg(ox + gw - 24, oy + 26, 15, ann["north"]))
    passo_m = next(v for v in (1.5, 3, 7.5, 15, 30, 75, 150) if v * 5 >= nc * scala / 4 or v == 150)
    seg = passo_m / scala * CELL
    n_seg = max(2, min(5, int(gw / seg)))
    for i in range(n_seg):
        w(f'<rect x="{_n(ox + i * seg)}" y="{y_sb - 6}" width="{_n(seg)}" height="6" '
          f'fill="{C["inchiostro"] if i % 2 == 0 else C["carta"]}" stroke="{C["inchiostro"]}" stroke-width="0.8"/>')
    for i in range(n_seg + 1):
        w(_testo(ox + i * seg, y_sb + (cz if stampa else 12), f"{i * passo_m:g}".replace(".", ","),
                 cz if stampa else 9.5, "middle"))
    w(_testo(ox + n_seg * seg + 14, y_sb, "metri", cz if stampa else 10.5, style="italic"))
    if stampa:
        w("</svg>")
        # niente filtri (render_map_svg, LARGHEZZA_STAMPA_PT)
        return "\n".join(re.sub(r' filter="url\(#[\w-]+\)"', "", r) for r in o)

    # ---- luoghi e legenda
    if righe_luoghi:
        w(_testo(MARGIN, y_l + 8, "Luoghi", 13.5, weight="bold"))
        per_col = math.ceil(len(righe_luoghi) / colonne)
        for k, (n, testo) in enumerate(righe_luoghi):
            cx_ = MARGIN + (k // per_col) * largo
            prima = righe_luoghi[(k // per_col) * per_col:k]
            yy = y_l + 30 + sum(len(t) * 13 + 6 for _, t in prima)
            w(f'<circle cx="{_n(cx_ + 8)}" cy="{_n(yy - 4)}" r="8" fill="{C["marker"]}"/>')
            w(_testo(cx_ + 8, yy - 0.5, n, 9.5, "middle", C["marker_t"], "bold"))
            for j, riga in enumerate(testo):
                w(_testo(cx_ + 22, yy + j * 13, riga, 10.5))
    w(_testo(MARGIN, y_leg + 8, "Legenda", 13.5, weight="bold"))
    for k, e in enumerate(leg):
        cx_ = MARGIN + (k // righe_leg) * largo
        yy = y_leg + 30 + (k % righe_leg) * 19
        _voce_legenda(w, e, cx_, yy, simboli, noto, locale, int(car) - 4)
    w("</svg>")
    return "\n".join(o)


def _taglio(alti: list[float]) -> int:
    """Dove spezzare un elenco in due colonne di altezza simile."""
    acc = 0.0
    for i, a in enumerate(alti):
        if acc >= sum(alti) / 2:
            return i
        acc += a
    return len(alti)


def _nome_voce(e, simboli, locale) -> str:
    """Il nome di un simbolo: quello del glossario, poi la legenda del master."""
    return (simboli.get(e) or {}).get("it") or locale.get(e) or e


def _voce_legenda(w, e, cx_, yy, simboli, noto, locale, car=0, righe=None) -> None:
    """Una voce della legenda: il segno a sinistra, il nome accorciato a `car`,
    oppure intero su più `righe` (modo stampa)."""
    sp = simboli.get(e)
    nome = _nome_voce(e, simboli, locale)
    if sp and sp["mode"] == "fill":
        col = COLORE.get(sp.get("pat"), sp.get("fill", C["lastre"]))
        w(f'<rect x="{_n(cx_)}" y="{_n(yy - 11)}" width="16" height="13" fill="{col}" '
          f'stroke="{C["inchiostro"]}" stroke-width="0.8"/>')
    elif sp and sp["mode"] == "unit":
        w(f'<circle cx="{_n(cx_ + 8)}" cy="{_n(yy - 4.5)}" r="7" fill="url(#{R._grad_id(sp["fill"])})" '
          f'stroke="{C["inchiostro"]}"/>')
    elif sp and sp.get("prop"):
        var = R.VARIANTS.get(sp["prop"], [sp["prop"]])
        w(f'<use href="#{var[0]}" x="{_n(cx_ - 2)}" y="{_n(yy - 15)}" width="20" height="20"/>')
    elif e in noto:
        w(f'<use href="#{noto[e][0]}" x="{_n(cx_)}" y="{_n(yy - 13)}" width="16" height="16"/>')
    for j, riga in enumerate(righe or [_corto(nome, car)]):
        w(_testo(cx_ + 24, yy + j * 13, riga, 10.5))
