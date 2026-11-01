#!/usr/bin/env python3
"""render_schemi.py — gli schemi di ARC-07 che non stanno su una griglia (ADR-0106 §5).

T-1 (il Piano della Terra, distanze non in scala), T-4 (sezione verticale
dell'approccio al Tempio) e M7-A (Hammerfist ≈372 DR, vista strategica non in
scala) non sono griglie: il renderer non li legge. Lo stesso vale per i tre
schemi della stand alone «Il Giardino di Sale e Calce» (GS-0 i collegamenti,
GS-S1 la sezione della cisterna, GS-S2 l'incontro coi Ragni delle Catene), che
vanno in `10-stand-alone/Il Giardino di Sale e Calce/Mappe/schemi/`. Per scelta di Jfs del
2026-10-30 diventano schemi disegnati nello stile della pianta (stessa carta,
stesso inchiostro, stessi cerchi rossi numerati, corpo minimo 7,4 pt alla
larghezza della pagina) senza griglia. Il contenuto è quello delle griglie
ASCII dei master DEF-1 e DEF-4, che restano come apparato.

Come per le mappe, l'SVG non si ritocca a mano: si cambia questo script e si
rigenera.

    python3 scripts/render_schemi.py           # scrive gli SVG
    python3 scripts/render_schemi.py --check   # esce 1 se un SVG non è allineato

Solo libreria standard; uscita byte-deterministica.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.sax.saxutils import escape

RADICE = Path(__file__).resolve().parent
sys.path.insert(0, str(RADICE))
import render_map_pianta as P  # noqa: E402
import render_map_svg as R  # noqa: E402

CARTELLA = RADICE.parent / "07_il Portale Della Forgia Eterna" / "Mappe" / "schemi"
W = R.LARGHEZZA_STAMPA_PT          # 1 unità = 1 pt alla larghezza della gabbia
CORPO = R.CORPO_STAMPA_PT          # 7,4 pt, il corpo minimo
C = P.C


class Foglio:
    def __init__(self, h: float):
        self.h = h
        self.o: list[str] = []

    def t(self, x, y, s, size=CORPO, anchor="start", fill=None, weight="normal", style="normal",
          fam=None):
        f = f' font-family="{fam}"' if fam else ""
        self.o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
                      f'fill="{fill or C["inchiostro"]}" font-weight="{weight}" font-style="{style}"{f}>'
                      f'{escape(s)}</text>')

    def righe(self, x, y, righe, size=CORPO, passo=None, **kw):
        for i, r in enumerate(righe):
            self.t(x, y + i * (passo or size * 1.22), r, size, **kw)

    def el(self, s: str):
        self.o.append(s)

    def num(self, n, x, y):
        self.o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{C["marker"]}" stroke="{C["marker_t"]}" '
                      f'stroke-width="1"/>')
        self.t(x, y + 2.6, str(n), 7.4, "middle", C["marker_t"], "bold")

    def titolo(self, testo, sotto):
        self.t(14, 20, testo, 11, fam="Cinzel", weight="bold")
        self.t(14, 32, sotto, CORPO, style="italic", fill=C["sbiadito"])

    def legenda(self, y, voci, colonne=1):
        """L'elenco dei numeri sotto lo schema, come sulle piante."""
        larg = (W - 28) / colonne
        per = -(-len(voci) // colonne)
        alt = y
        # a capo per colonna: ogni voce prende le righe che le servono
        for c in range(colonne):
            yy = y
            for n, testo in voci[c * per:(c + 1) * per]:
                x = 14 + c * larg
                self.num(n, x + 6, yy - 2.6)
                rr = P._a_capo(testo, int((larg - 22) / (CORPO * 0.43)))
                self.righe(x + 16, yy, rr)
                yy += len(rr) * CORPO * 1.22 + 3
            alt = max(alt, yy)
        return alt

    def svg(self) -> str:
        defs = ["<defs>", R._stile_font(),
                f'<pattern id="sc-roccia" width="6" height="6" patternUnits="userSpaceOnUse" '
                f'patternTransform="rotate(35)"><rect width="6" height="6" fill="{C["roccia"]}"/>'
                f'<line x1="0" y1="0" x2="0" y2="6" stroke="{C["roccia_t"]}" stroke-width="1.1"/></pattern>',
                f'<pattern id="sc-onde" width="18" height="7" patternUnits="userSpaceOnUse">'
                f'<rect width="18" height="7" fill="#b9b2a2"/><path d="M0 4 q4.5 -3 9 0 t9 0" fill="none" '
                f'stroke="#857d6c" stroke-width="0.8"/></pattern>',
                f'<pattern id="sc-punti" width="5" height="5" patternUnits="userSpaceOnUse">'
                f'<rect width="5" height="5" fill="{C["caverna"]}"/><circle cx="2.5" cy="2.5" r="0.6" '
                f'fill="{C["ciottoli"]}"/></pattern>',
                f'<marker id="sc-freccia" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
                f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{C["inchiostro"]}"/></marker>',
                f'<marker id="sc-freccia-r" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
                f'markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{C["marker"]}"/></marker>',
                "</defs>"]
        testa = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:g}" height="{self.h:g}" '
                 f'viewBox="0 0 {W:g} {self.h:g}" font-family="{R.FONT}">')
        fondo = f'<rect width="{W:g}" height="{self.h:g}" fill="{C["carta"]}"/>'
        return "\n".join([testa, *defs, fondo, *self.o, "</svg>"]) + "\n"


def _cristallo(f, x, y, h, fill="#cfd8d6"):
    w = h * 0.32
    f.el(f'<path d="M{x:.1f} {y:.1f} l{-w:.1f} {-h * 0.25:.1f} l0 {-h * 0.55:.1f} l{w:.1f} {-h * 0.2:.1f} '
         f'l{w:.1f} {h * 0.2:.1f} l0 {h * 0.55:.1f} z" fill="{fill}" stroke="{C["inchiostro"]}" '
         f'stroke-width="0.8"/>')
    f.el(f'<path d="M{x:.1f} {y:.1f} l0 {-h:.1f}" stroke="{C["sbiadito"]}" stroke-width="0.5"/>')


def _tenda(f, x, y, s=5.5):
    f.el(f'<path d="M{x - s:.1f} {y:.1f} L{x:.1f} {y - s * 1.1:.1f} L{x + s:.1f} {y:.1f} z" '
         f'fill="{C["t_telo"] if "t_telo" in C else "#e6d7b2"}" stroke="{C["inchiostro"]}" stroke-width="0.6"/>')


def _fuoco(f, x, y):
    f.el(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="{C["lava"]}" stroke="{C["lava_c"]}" '
         f'stroke-width="0.5"/>')


def _albero(f, x, y, r=5):
    f.el(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#a9bd82" stroke="#5d6b3f" stroke-width="0.7"/>')


# ----------------------------------------------------------------------------- T-1
def t1() -> str:
    f = Foglio(330)
    f.titolo("T-1 · Il Piano della Terra: dall'arrivo al Tempio",
             "schema, non in scala · gravità 2×: ci si muove lenti ovunque (§3)")
    y0, y1 = 48, 222          # la fascia del paesaggio
    f.el(f'<rect x="14" y="{y0}" width="{W - 28:g}" height="{y1 - y0}" fill="url(#sc-punti)" '
         f'stroke="{C["inchiostro"]}" stroke-width="1.2"/>')
    # l'oceano di roccia, a destra
    f.el(f'<rect x="352" y="150" width="{W - 14 - 352:g}" height="{y1 - 150}" fill="url(#sc-onde)"/>')
    # 1 la piattaforma
    f.el(f'<rect x="26" y="112" width="62" height="44" rx="4" fill="#dfe6e4" stroke="{C["inchiostro"]}" '
         f'stroke-width="1"/>')
    for i in range(3):
        for j in range(2):
            f.el(f'<circle cx="{38 + i * 19}" cy="{124 + j * 20}" r="4" fill="#f4f0d8" stroke="#9aa9a6"/>')
    # 2 i ponti di pietra galleggiante
    for i, (x, y) in enumerate(((94, 128), (108, 120), (122, 130))):
        f.el(f'<rect x="{x}" y="{y}" width="12" height="7" fill="{C["lastre"]}" stroke="{C["inchiostro"]}" '
             f'stroke-width="0.7"/>')
    # 3 la foresta di cristalli
    for x, y, h in ((146, 118, 34), (160, 150, 44), (176, 108, 30), (190, 140, 50), (206, 116, 38),
                    (220, 160, 34), (232, 128, 46)):
        _cristallo(f, x, y, h)
    f.el(f'<rect x="196" y="164" width="8" height="18" fill="{C["roccia"]}" stroke="{C["inchiostro"]}" '
         f'stroke-width="0.7" stroke-dasharray="2 1.5"/>')
    # 4 il campo dei cristalli viventi
    f.el(f'<ellipse cx="300" cy="120" rx="40" ry="30" fill="#d9e3dc" stroke="{C["inchiostro"]}" '
         f'stroke-width="0.9"/>')
    for x, y in ((280, 112), (318, 108), (286, 136), (314, 134)):
        _cristallo(f, x, y + 6, 14, "#b9e0d4")
    _cristallo(f, 300, 132, 24, "#e6c3e8")
    # 5 il Tempio sopra l'oceano
    f.el(f'<rect x="410" y="62" width="58" height="58" fill="#d6dde3" stroke="{C["inchiostro"]}" '
         f'stroke-width="1.2" transform="rotate(8 439 91)"/>')
    f.el(f'<rect x="425" y="113" width="26" height="9" fill="{C["acqua_b"]}" stroke="{C["inchiostro"]}" '
         f'stroke-width="0.7" transform="rotate(8 439 91)"/>')
    f.el(f'<line x1="439" y1="128" x2="439" y2="168" stroke="{C["inchiostro"]}" stroke-width="0.7" '
         f'stroke-dasharray="2 2" marker-start="url(#sc-freccia)" marker-end="url(#sc-freccia)"/>')
    f.t(444, 152, "50 m", CORPO, style="italic")
    # la via, tratteggiata
    f.el(f'<path d="M88 134 C120 126 140 190 200 194 S270 172 300 152 S360 110 400 100" fill="none" '
         f'stroke="{C["marker"]}" stroke-width="1.4" stroke-dasharray="5 3" marker-end="url(#sc-freccia-r)"/>')
    f.t(250, 214, "Aegis Fang vibra verso il Tempio", CORPO, "middle", C["marker"], style="italic")
    for n, x, y in ((1, 57, 104), (2, 115, 112), (3, 190, 82), (4, 300, 84), (5, 381, 182), (6, 470, 60)):
        f.num(n, x, y)
    # l'asse delle distanze
    ya = 236
    f.el(f'<line x1="57" y1="{ya}" x2="470" y2="{ya}" stroke="{C["inchiostro"]}" stroke-width="0.8"/>')
    for x, s in ((57, "0 m"), (190, "300 m – 1 km"), (300, "1 – 1,5 km"), (420, "1,5 – 2 km")):
        f.el(f'<line x1="{x}" y1="{ya - 3}" x2="{x}" y2="{ya + 3}" stroke="{C["inchiostro"]}"/>')
        f.t(x, ya + 12, s, CORPO, "middle")
    f.legenda(262, [
        (1, "Arrivo: la piattaforma di cristallo, con i cristalli luminescenti"),
        (2, "Ponti di pietra galleggiante"),
        (3, "Foresta di cristalli giganti (30-60 m). Agguato dei 3 Xorn, le Fauci di Diamante: T-2. "
            "Il pilastro tratteggiato è quello corroso dagli Xorn"),
        (4, "Campo dei Cristalli Viventi, con la Madre Cristallo al centro: la skill challenge, T-3"),
        (5, "Oceano di roccia grigia, liquida ma cede"),
        (6, "Il Tempio di mithral, cubo di 100 m che ruota di un giro all'ora; il portale (in blu) è "
            "sulla faccia inferiore, verso l'oceano: T-4, T-5, T-6"),
    ], colonne=2)
    return f.svg()


# ----------------------------------------------------------------------------- T-4
def t4() -> str:
    f = Foglio(372)
    f.titolo("T-4 · L'approccio al Tempio di mithral",
             "sezione verticale, non in scala · l'«alto» è relativo: sopra comanda la gravità del Tempio")
    # il Tempio
    f.el(f'<rect x="90" y="46" width="330" height="62" fill="#d6dde3" stroke="{C["inchiostro"]}" '
         f'stroke-width="1.3"/>')
    for i in range(6):
        f.el(f'<line x1="{120 + i * 50}" y1="54" x2="{140 + i * 50}" y2="54" stroke="{C["sbiadito"]}" '
             f'stroke-width="0.8"/>')
    f.t(255, 74, "IL TEMPIO DI MITHRAL", 9, "middle", fam="Cinzel", weight="bold")
    f.t(255, 88, "cubo di 100 m che ruota · gravità propria · i corridoi ruotano di 90° ogni 20 m", CORPO,
        "middle", style="italic")
    f.el(f'<rect x="222" y="104" width="66" height="9" fill="{C["acqua_b"]}" stroke="{C["inchiostro"]}" '
         f'stroke-width="0.8"/>')
    f.t(296, 103, "il portale, sulla faccia inferiore", CORPO, style="italic")
    # l'oceano
    yo = 250
    f.el(f'<rect x="14" y="{yo}" width="{W - 28:g}" height="44" fill="url(#sc-onde)" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.9"/>')
    f.t(W / 2, yo + 27, "OCEANO DI ROCCIA · grigia, liquida ma cede", 8, "middle", fam="Cinzel")
    # la quota
    f.el(f'<line x1="58" y1="113" x2="58" y2="{yo}" stroke="{C["inchiostro"]}" stroke-width="0.8" '
         f'marker-start="url(#sc-freccia)" marker-end="url(#sc-freccia)"/>')
    f.t(52, 185, "50 m", 8, "end", style="italic")
    # la gravità del Tempio
    ycat = yo - (yo - 113) * 0.4
    f.el(f'<rect x="150" y="113" width="210" height="{ycat - 113:.1f}" fill="#c9d3ea" fill-opacity="0.45"/>')
    f.el(f'<line x1="150" y1="{ycat:.1f}" x2="360" y2="{ycat:.1f}" stroke="{C["acqua_b"]}" '
         f'stroke-width="0.9" stroke-dasharray="4 3"/>')
    f.t(262, ycat - 4, "da qui comanda la gravità del Tempio", CORPO, "start", C["acqua_b"], style="italic")
    f.el(f'<line x1="330" y1="{ycat - 12:.1f}" x2="330" y2="128" stroke="{C["acqua_b"]}" stroke-width="1.2" '
         f'marker-end="url(#sc-freccia)"/>')
    # la corda e il salto
    f.el(f'<line x1="255" y1="113" x2="255" y2="{yo}" stroke="{C["inchiostro"]}" stroke-width="1.1"/>')
    f.el(f'<path d="M232 {yo} C226 {yo - 40} 236 {ycat + 20:.1f} 250 {ycat:.1f}" fill="none" '
         f'stroke="{C["marker"]}" stroke-width="1.3" stroke-dasharray="4 2.5" marker-end="url(#sc-freccia-r)"/>')
    f.el(f'<path d="M250 {ycat:.1f} C246 {ycat - 30:.1f} 244 140 246 116" fill="none" stroke="{C["marker"]}" '
         f'stroke-width="1.3" marker-end="url(#sc-freccia-r)"/>')
    f.num(1, 214, yo - 30)
    f.num(2, 236, ycat + 8)
    f.num(3, 268, 150)
    # i tre sulla roccia
    for x, n in ((200, "Thorik"), (232, "Tordek"), (290, "Artemis")):
        f.el(f'<circle cx="{x}" cy="{yo - 6}" r="5" fill="#4a7fc0" stroke="{C["inchiostro"]}" stroke-width="0.8"/>')
        f.t(x, yo - 14, n, CORPO, "middle")
    yl = f.legenda(312, [
        (1, "Tordek salta: Saltare CD 25 (prendendo 10 fa 26). Le Rune di Attracco si colpiscono "
            "all'arrivo"),
        (2, "A circa 20 m la gravità del Tempio lo cattura: «cade» verso il portale"),
        (3, "Gli altri salgono la corda: Scalare CD 15"),
    ], colonne=1)
    f.t(14, yl + 8, "Ruoli: Thorik l'ancora (FOR CD 20) · Artemis il traghettatore (vola col cavo) · "
        "Tordek il navigatore", CORPO, style="italic")
    f.h = round(yl + 16)
    return f.svg()


# ----------------------------------------------------------------------------- M7-A
def m7a() -> str:
    f = Foglio(700)
    f.titolo("M7-A · Hammerfist ≈372 DR: la fortezza, il campo dell'orda, le mura",
             "vista strategica, non in scala · il duello è su M7-B, la tenda su M7-C")
    x0, x1 = 14, W - 14
    # la montagna
    f.el(f'<path d="M{x0} 44 L{x1} 44 L{x1} 78 Q{W / 2} 96 {x0} 78 z" fill="url(#sc-roccia)" '
         f'stroke="{C["inchiostro"]}" stroke-width="1"/>')
    f.t(W / 2, 62, "LA MONTAGNA · dentro, le sale scendono (M7-S)", 8, "middle", C["carta"], fam="Cinzel")
    # la fortezza
    fx, fy, fw, fh = 120, 92, 220, 82
    f.el(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{C["lastre"]}" stroke="{C["inchiostro"]}" '
         f'stroke-width="3.2"/>')
    f.el(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="#fbf7ea" stroke-width="1.2"/>')
    f.el(f'<rect x="{fx + fw / 2 - 12}" y="{fy - 10}" width="24" height="18" fill="#efe6cf" '
         f'stroke="{C["inchiostro"]}" stroke-width="1.2"/>')
    f.el(f'<rect x="{fx + fw - 10}" y="{fy + fh - 12}" width="18" height="18" fill="#efe6cf" '
         f'stroke="{C["inchiostro"]}" stroke-width="1.2"/>')
    f.el(f'<rect x="{fx + 60}" y="{fy + 26}" width="100" height="40" fill="{C["piatto"]}" '
         f'stroke="{C["sbiadito"]}" stroke-width="0.8" stroke-dasharray="3 2"/>')
    f.t(fx + 110, fy + 50, "cortile interno, +100", CORPO, "middle", style="italic")
    f.el(f'<rect x="{fx + fw / 2 - 9}" y="{fy + fh - 3}" width="18" height="6" fill="{C["lastre_b"]}" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.8"/>')
    f.el(f'<rect x="{fx + fw - 34}" y="{fy + fh - 3}" width="7" height="6" fill="{C["carta"]}" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.8"/>')
    for i in range(3):
        f.el(f'<path d="M{fx + fw + 2} {fy + 22 + i * 14} l7 4 l-7 4" fill="none" stroke="{C["inchiostro"]}" '
             f'stroke-width="0.9"/>')
    # la spianata e i tornanti
    sy = 196
    f.el(f'<path d="M{fx + fw / 2} {fy + fh + 3} L{fx + fw / 2 - 18} {sy}" stroke="{C["inchiostro"]}" '
         f'stroke-width="2.2" stroke-dasharray="1 2.5"/>')
    f.el(f'<rect x="{fx + 30}" y="{sy}" width="{fw - 60}" height="22" fill="url(#sc-punti)" '
         f'stroke="{C["sbiadito"]}" stroke-width="0.8"/>')
    f.t(fx + fw / 2, sy + 15, "SPIANATA DEGLI ARIETI, +80", 7.6, "middle", fam="Cinzel")
    f.el(f'<path d="M{fx + fw / 2} {sy + 22} l-30 10 l60 10 l-60 10 l60 10 l-30 8" fill="none" '
         f'stroke="{C["inchiostro"]}" stroke-width="1.6"/>')
    # il bosco a est e il portale
    for x, y in ((398, 108), (414, 96), (430, 112), (446, 98), (462, 110), (406, 128), (424, 134), (442, 126),
                 (460, 136), (476, 122)):
        _albero(f, x, y)
    f.el(f'<path d="M440 154 l3 6 l6 1 l-5 4 l1 6 l-5 -3 l-5 3 l1 -6 l-5 -4 l6 -1 z" fill="#ffd27a" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.7"/>')
    # la piana dell'orda
    py = 272
    f.el(f'<rect x="{x0}" y="{py}" width="{x1 - x0}" height="{560 - py}" fill="{C["caverna"]}" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.8"/>')
    f.t(x0 + 6, py + 11, "la piana dell'orda, quota 0 · le tende da 500 m a 1 km dalle mura", CORPO,
        style="italic", fill=C["sbiadito"])
    # il blocco del comando
    bx, by, bw, bh = 150, 380, 196, 100
    for x, y in [(x, y) for x in range(26, 476, 30) for y in range(298, 548, 26)]:
        if bx - 18 < x < bx + bw + 18 and by - 20 < y < by + bh + 20:
            continue
        if any(abs(x - gx) < 34 and abs(y - gy) < 22 for gx, gy in ((40, 330), (456, 330), (40, 520), (456, 520))):
            continue
        _tenda(f, x + (y // 26 % 2) * 8, y)
        if (x + y) % 4 == 0:
            _fuoco(f, x + 10 + (y // 26 % 2) * 8, y - 2)
    f.el(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{C["piatto"]}" stroke="{C["inchiostro"]}" '
         f'stroke-width="1.6"/>')
    f.el(f'<line x1="{bx}" y1="{by + bh / 2}" x2="{bx + bw}" y2="{by + bh / 2}" stroke="{C["inchiostro"]}" '
         f'stroke-width="1"/><line x1="{bx + bw / 2}" y1="{by}" x2="{bx + bw / 2}" y2="{by + bh / 2 - 14}" '
         f'stroke="{C["inchiostro"]}" stroke-width="1"/>')
    for x, y in [(bx + 18 + i * 22, by + 18) for i in range(8) if i not in (3, 4)] + \
                [(bx + 18 + i * 22, by + 70) for i in range(8) if i not in (3, 4)]:
        f.el(f'<rect x="{x - 4}" y="{y - 4}" width="8" height="8" fill="#8a7a62" stroke="{C["inchiostro"]}" '
             f'stroke-width="0.6"/>')
    f.el(f'<rect x="{bx + bw / 2 - 26}" y="{by + bh / 2 - 14}" width="52" height="28" fill="#e6d7b2" '
         f'stroke="{C["inchiostro"]}" stroke-width="2"/>')
    f.t(bx + bw / 2, by + bh / 2 + 3, "COMANDO", 7.6, "middle", fam="Cinzel", weight="bold")
    # i posti di guardia
    for n, x, y in (("GP1", 40, 330), ("GP2", 456, 330), ("GP3", 40, 520), ("GP4", 456, 520)):
        f.el(f'<rect x="{x - 4}" y="{y - 4}" width="8" height="8" fill="{C["inchiostro"]}"/>')
        f.t(x, y + 14, n, CORPO, "middle", weight="bold")
    # le colline a sud
    f.el(f'<path d="M{x0} 560 Q90 548 160 560 T300 560 T{x1} 560" fill="none" stroke="{C["sbiadito"]}" '
         f'stroke-width="1"/>')
    f.t(W / 2, 572, "a sud, oltre il campo: le colline dove dorme il drago", CORPO, "middle", style="italic",
        fill=C["sbiadito"])
    # la via dei PG
    f.el(f'<path d="M{fx + fw - 30} {fy + fh + 4} C372 210 394 250 400 300 S410 360 380 368 '
         f'L{bx + bw / 2 + 30} 368 L{bx + bw / 2 + 4} {by + bh / 2 - 15}" fill="none" stroke="{C["marker"]}" '
         f'stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#sc-freccia-r)"/>')
    # i numeri
    for n, x, y in ((1, fx + fw / 2, fy - 18), (2, fx + 18, fy + 18), (3, fx + 110, fy + 38),
                    (4, fx + fw / 2 + 16, fy + fh + 10), (5, fx + fw - 30, fy + fh + 14), (6, fx + fw + 18, fy + 32),
                    (7, fx + fw + 12, fy + fh - 2), (8, fx + fw / 2 - 34, sy + 30), (9, fx + fw / 2 + 44, sy + 46),
                    (10, 456, 168), (11, 410, 316), (12, 60, 420), (13, bx + 16, by + 34),
                    (14, bx + bw / 2 + 36, by + bh / 2), (15, 300, 528)):
        f.num(n, x, y)
    f.h = 584
    return f.svg()


def m7a_legenda() -> str:
    """La pagina dopo lo schema, come la legenda delle piante: i numeri e il profilo."""
    f = Foglio(600)
    f.titolo("M7-A · Indicazioni e profilo",
             "i numeri dello schema · le quote del DM, sulla piana dell'orda")
    yl = f.legenda(52, [
        (1, "Torre nord, +120: la porta che entra nella montagna; le campane"),
        (2, "Zona 1, Hammerfist giovane: mura bianche e nuove, sicura. La fucina originale e la statua del re"),
        (3, "Il cortile interno, +100: il duello con Skullcrusher, che entra dall'alto (M7-B)"),
        (4, "La porta e la targa. La rampa finale di 20 m fino alla spianata è un'inferenza da confermare"),
        (5, "La postierla"),
        (6, "Zona 3, le mura all'alba: le scale d'assedio sul tratto est (inferenza da confermare)"),
        (7, "La torre est"),
        (8, "La spianata degli arieti, +80, nuda"),
        (9, "La strada a tornanti, circa 500 m dal ciglio alla piana"),
        (10, "Il bosco a est e il portale d'arrivo, a circa 500 m (Scene 1-2)"),
        (11, "La via dei PG (tratteggio rosso): dalla postierla giù per il fianco est, 100 m di dislivello, "
             "lungo il lato est del campo, circa 1 km fino alla tenda; all'alba si risale lo stesso fianco"),
        (12, "Zona 2, il mare di tende: i clan degli orchi a gruppi attorno al fuoco della banda "
             "(copertura); 10.000 dormono"),
        (13, "Le lance hobgoblin: quattro tende attorno al fuoco, ad anello attorno al capo; le vie battute "
             "dividono cinque blocchi"),
        (14, "La tenda del comando, sola nel suo spiazzo: Zog'tar e 4 guardie (Scena 8, M7-C)"),
        (15, "Vatore, fra le tende (Scena 9)"),
    ], colonne=2)
    # il profilo nord → sud
    yp = yl + 14
    f.t(14, yp, "IL PROFILO, DA NORD A SUD (le quote del DM sulla piana dell'orda)", 8, fam="Cinzel",
        weight="bold")
    base, k = yp + 92, 0.62
    pts = [(40, 120), (64, 120), (64, 100), (150, 100), (180, 80), (290, 80), (420, 0), (482, 0)]
    d = " ".join(f"{'M' if i == 0 else 'L'}{x} {base - q * k:.1f}" for i, (x, q) in enumerate(pts))
    f.el(f'<path d="{d} L482 {base + 4} L40 {base + 4} z" fill="url(#sc-roccia)" stroke="{C["inchiostro"]}" '
         f'stroke-width="1"/>')
    for q, s in ((120, "+120 m torre nord"), (100, "+100 m porta, cortile"), (80, "+80 m spianata"),
                 (0, "0 m piana")):
        f.t(36, base - q * k + 3, s.split(" ", 2)[0] + " " + s.split(" ", 2)[1], CORPO, "end")
    f.t(68, base - 120 * k + 2, "torre nord", CORPO, style="italic")
    f.t(104, base - 100 * k - 4, "porta e targa · cortile (M7-B)", CORPO, style="italic")
    f.t(196, base - 80 * k - 4, "spianata degli arieti", CORPO, style="italic")
    f.t(176, base - 80 * k + 12, "rampa, 20 m", CORPO, style="italic", fill=C["carta"])
    f.t(360, base - 40 * k - 2, "tornanti", CORPO, style="italic")
    for x in (430, 452, 470):
        _tenda(f, x, base - 1, 4.5)
    f.t(452, base - 10, "COMANDO", CORPO, "middle", fam="Cinzel")
    f.el(f'<line x1="290" y1="{base + 14}" x2="420" y2="{base + 14}" stroke="{C["inchiostro"]}" '
         f'stroke-width="0.7" marker-start="url(#sc-freccia)" marker-end="url(#sc-freccia)"/>')
    f.t(355, base + 25, "circa 500 m di tornanti", CORPO, "middle")
    f.el(f'<line x1="420" y1="{base + 14}" x2="482" y2="{base + 14}" stroke="{C["inchiostro"]}" '
         f'stroke-width="0.7" marker-end="url(#sc-freccia)"/>')
    f.t(451, base + 25, "le tende, fino a 1 km", CORPO, "middle")
    f.h = round(base + 34)
    return f.svg()


# ============================================================================= Il Giardino di Sale e Calce
# Gli schemi della stand alone (10-stand-alone/Il Giardino di Sale e Calce): i
# collegamenti fra le aree (GS-0), la sezione della cisterna (GS-S1) e
# l'incontro coi Ragni delle Catene in sezione (GS-S2). Le quote sono quelle
# delle mappe GS-1…GS-6; le posizioni in orizzontale delle sezioni sono
# proiettate su un solo piano e valgono come indicazione.
CARTELLA_GSC = RADICE.parent / "10-stand-alone" / "Il Giardino di Sale e Calce" / "Mappe" / "schemi"
ARIA = "#efe5c9"


def _lettera(f, s, x, y):
    """Il cerchio rosso degli ingressi, con la lettera."""
    f.el(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7.5" fill="{C["marker"]}" stroke="{C["marker_t"]}" '
         f'stroke-width="1"/>')
    f.t(x, y + 3, s, 8.5, "middle", C["marker_t"], "bold", fam="Cinzel")


def _nodo(f, x, y, cod, righe, w=100, el=None):
    """Un'area del modulo: codice, nome, eventuale scontro (bordo rosso)."""
    n = len(righe) + (1 if el else 0)
    h = 14 + n * CORPO * 1.22
    bordo = C["marker"] if el else C["inchiostro"]
    f.el(f'<rect x="{x - w / 2:.1f}" y="{y - h / 2:.1f}" width="{w}" height="{h:.1f}" rx="4" '
         f'fill="{C["piatto"]}" stroke="{bordo}" stroke-width="{1.6 if el else 1}"/>')
    yy = y - h / 2 + 10
    f.t(x, yy, cod, 8, "middle", fam="Cinzel", weight="bold")
    for r in righe:
        yy += CORPO * 1.22
        f.t(x, yy, r, CORPO, "middle")
    if el:
        yy += CORPO * 1.22
        f.t(x, yy, el, CORPO, "middle", C["marker"], "bold")
    return h


def _via(f, punti, tratteggio=False, colore=None):
    d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}" for i, (x, y) in enumerate(punti))
    ds = ' stroke-dasharray="4 2.5"' if tratteggio else ""
    f.el(f'<path d="{d}" fill="none" stroke="{colore or C["inchiostro"]}" stroke-width="1.1"{ds}/>')


def gs0() -> str:
    f = Foglio(700)
    f.titolo("GS-0 · Come si collegano le aree, e i tre ingressi da Rethmar",
             "schema, non in scala · in alto la città, poi le quote della cisterna · bordo rosso: c'è uno scontro")
    # il righello delle quote
    quote = ((70, "Rethmar"), (126, "sotto le vie"), (184, "+15 m"), (250, "+6 m"), (310, "0"),
             (356, "−6 m"), (414, "−12 m"), (474, "Sottosuolo"))
    f.el(f'<line x1="44" y1="60" x2="44" y2="484" stroke="{C["sbiadito"]}" stroke-width="0.8"/>')
    for y, s in quote:
        f.el(f'<line x1="41" y1="{y}" x2="47" y2="{y}" stroke="{C["sbiadito"]}" stroke-width="0.8"/>')
        f.t(39, y + 2.6, s, CORPO, "end", C["sbiadito"], style="italic")
    f.el(f'<line x1="47" y1="98" x2="{W - 14:g}" y2="98" stroke="{C["roccia_t"]}" stroke-width="0.8" '
         f'stroke-dasharray="1.5 2"/>')
    f.t(W - 16, 95, "il suolo della città", CORPO, "end", C["sbiadito"], style="italic")
    # le vie prima dei nodi, così i nodi le coprono
    _via(f, [(100, 70), (100, 126)])
    _via(f, [(262, 70), (262, 126)])
    _via(f, [(420, 70), (420, 126)])
    _via(f, [(100, 126), (100, 250), (120, 250)])                       # A2 la galleria di servizio
    _via(f, [(262, 126), (262, 184)])                                    # la gabbia
    _via(f, [(160, 184), (262, 184), (374, 184)])                        # i nidi
    _via(f, [(236, 194), (200, 240)])                                    # le scale a pioli
    _via(f, [(262, 194), (262, 356)], tratteggio=True)                   # le catene
    _via(f, [(175, 250), (360, 250)])                                    # il ponte maestro
    _via(f, [(175, 250), (175, 310)])                                    # le scalette
    _via(f, [(175, 310), (262, 356)])                                    # a nuoto alla vasca
    _via(f, [(262, 356), (262, 414)], colore=C["acqua_b"])               # il sifone
    _via(f, [(350, 250), (310, 400)])                                    # la chiocciola
    _via(f, [(420, 126), (420, 414)], colore=C["acqua_b"])               # sfioratore e galleria
    _via(f, [(262, 414), (420, 414)])                                    # la rampa
    _via(f, [(420, 414), (420, 474)])                                    # lo scavo
    _via(f, [(420, 474), (420, 494)], tratteggio=True)
    # le etichette delle vie
    f.righe(104, 205, ["A2 · la galleria di servizio,", "400 m in discesa, 5 minuti"], style="italic")
    f.righe(266, 150, ["la gabbia, 6 m:", "la fune si può tagliare"], style="italic")
    f.t(212, 229, "scale a pioli, 9 m", CORPO, "end", style="italic")
    f.righe(266, 282, ["le catene fino all'acqua,", "Scalare CD 15"], style="italic")
    f.t(271, 262, "ponte maestro, 39 m", CORPO, "middle", style="italic")
    f.t(179, 284, "scalette", CORPO, style="italic")
    f.t(214, 338, "a nuoto", CORPO, "end", style="italic")
    f.righe(258, 382, ["il sifone, 6 m: Nuotare CD 15,", "due round in apnea"], anchor="end",
            style="italic", fill=C["acqua_b"])
    f.righe(340, 312, ["T3 · la scala a", "chiocciola, 18 m"], style="italic")
    f.righe(424, 182, ["lo sfioratore, 60 m,", "acqua alla cintura;", "poi la galleria,", "300 m"],
            style="italic", fill=C["acqua_b"])
    f.t(346, 410, "la rampa", CORPO, "middle", style="italic")
    f.t(424, 500, "2 km verso i campi di Sonjak", CORPO, "end", style="italic")
    # i nodi
    _nodo(f, 100, 70, "La Cattedrale", ["di Lathander, n. 18", "Tredora ha la chiave"])
    _nodo(f, 262, 70, "Il Mercato del Ponte", ["n. 8 e 13, il pozzo grande", "Kesk e i facchini di Sal"],
          w=120)
    _nodo(f, 420, 70, "Il Ponte", ["n. 7, la seconda pila", "il gorgo contro corrente"])
    _nodo(f, 100, 126, "A1 · La cripta", ["6 m sotto la navata", "la porta col sole"])
    _nodo(f, 262, 126, "C1-C2 · La gabbia", ["l'argano della gilda"], w=104)
    _nodo(f, 420, 126, "B1 · Lo sfioratore", ["la paratoia, l'argano"], w=104)
    _nodo(f, 262, 184, "G1 · Le passerelle", ["catene e vuoto"], w=104, el="EL 12 · due ragni")
    _nodo(f, 160, 184, "G2 · Nido ovest", ["il tesoro dei morti"], w=86)
    _nodo(f, 374, 184, "G3 · Nido est", ["sopra la Torre"], w=86)
    _nodo(f, 175, 250, "G4 · Il ponte maestro", ["G7, le paratoie sul ponte nord"], w=116)
    _nodo(f, 360, 250, "T1-T2 · La Torre", ["l'officina, lo studio"], w=104, el="EL 15 · Tariq e due skum")
    _nodo(f, 175, 310, "G5 · Le navate", ["1 m d'acqua, gli asserviti"], w=116, el="EL 12 · tre chuul, a scelta")
    _nodo(f, 262, 356, "G6 · La vasca", ["6 m d'acqua torbida"], w=104)
    _nodo(f, 262, 414, "S1-S2 · Il Santuario", ["la vasca del Cuore"], w=110, el="EL 16 · Karkator")
    _nodo(f, 420, 414, "B2 · La galleria", ["di drenaggio, la canaletta"], w=110, el="EL 9 · un chuul")
    _nodo(f, 420, 474, "B3 · Lo scavo", ["otto asserviti in catene"], w=110)
    _lettera(f, "A", 54, 62)
    _lettera(f, "C", 206, 62)
    _lettera(f, "B", 374, 62)
    f.h = 510
    return f.svg()


def gs0_legenda() -> str:
    f = Foglio(400)
    f.titolo("GS-0 · I tre ingressi", "dove si arriva, chi aspetta, in che ordine vengono gli scontri")
    yl = f.legenda(56, [
        ("A", "La cripta della Cattedrale. Si arriva a +6 m sul ponte maestro, sotto le feritoie della "
              "Torre: ragni e chuul si possono evitare. Se Fratello Odo non è scoperto, la Torre è avvisata."),
        ("B", "Lo sfioratore, nascosto: senza uno dei tre indizi non c'è. Si arriva a −12 m nella galleria, "
              "si passa il chuul e lo scavo, e si prende Karkator alle spalle; Tariq scende la chiocciola al "
              "secondo round."),
        ("C", "Il pozzo grande del mercato. Si arriva a +15 m in mezzo ai Ragni delle Catene, ed è la "
              "strada più lunga: il rumore allerta la Torre (GS-S2)."),
        ("→", "Il sifone e la chiocciola sono le due strade dalla cisterna al Santuario. Chi passa dal "
              "sifone arriva nell'acqua di Karkator, che la sente da quando i PG toccano la vasca."),
    ], colonne=1)
    f.h = round(yl + 6)
    return f.svg()


def _y_s1(q: float) -> float:
    return 60 + (30 - q) * 4


def _x_s1(cella: float) -> float:
    return 150 + cella * 6


def _catena(f, x, y0, y1, colore=None):
    f.el(f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y1:.1f}" stroke="{colore or "#5b5348"}" '
         f'stroke-width="1" stroke-dasharray="2 1.2"/>')


def _ragno(f, x, y, s=9.0, etereo=False):
    """Un Ragno delle Catene (Enorme): corpo, otto zampe; tratteggiato se etereo."""
    tr = ' stroke-dasharray="2 1.5"' if etereo else ""
    riemp = "none" if etereo else "#3b332b"
    for i in range(4):
        dy = (i - 1.5) * s * 0.28
        for sx in (-1, 1):
            f.el(f'<path d="M{x:.1f} {y + dy:.1f} q{sx * s * 0.6:.1f} {-s * 0.45:.1f} {sx * s * 1.05:.1f} '
                 f'{s * 0.25 + dy * 0.4:.1f}" fill="none" stroke="#3b332b" stroke-width="0.9"{tr}/>')
    f.el(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{s * 0.42:.1f}" ry="{s * 0.34:.1f}" fill="{riemp}" '
         f'stroke="#3b332b" stroke-width="0.9"{tr}/>')


def _pg(f, x, y, nome=None, colore="#4a7fc0", r=3.6):
    f.el(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{colore}" stroke="{C["inchiostro"]}" '
         f'stroke-width="0.7"/>')
    if nome:
        f.t(x, y - r - 2.5, nome, CORPO, "middle")


def _nido(f, x0, x1, y0, y1):
    f.el(f'<path d="M{x0:.1f} {y0:.1f} Q{(x0 + x1) / 2:.1f} {y1 + 6:.1f} {x1:.1f} {y0:.1f}" fill="#d9d2c2" '
         f'fill-opacity="0.8" stroke="#5b5348" stroke-width="0.7"/>')
    for i in range(5):
        xx = x0 + (x1 - x0) * (i + 0.5) / 5
        f.el(f'<line x1="{xx:.1f}" y1="{y0:.1f}" x2="{(x0 + x1) / 2:.1f}" y2="{y1:.1f}" stroke="#5b5348" '
             f'stroke-width="0.5"/>')


def gs_s1() -> str:
    f = Foglio(700)
    f.titolo("GS-S1 · La Grande Cisterna in sezione, da ovest a est",
             "quote in scala (1 m = 4 pt) dentro la cisterna · la galleria e la riva non sono in scala · "
             "gli elementi sono proiettati su un piano")
    Y, X = _y_s1, _x_s1
    # la roccia e il suolo
    f.el(f'<path d="M14 {Y(23):.1f} L108 {Y(23):.1f} L140 {Y(21):.1f} L396 {Y(21):.1f} L436 {Y(13):.1f} '
         f'L436 {Y(9):.1f} L482 {Y(9):.1f} L482 {Y(-24):.1f} L14 {Y(-24):.1f} z" fill="url(#sc-roccia)" '
         f'stroke="{C["inchiostro"]}" stroke-width="1"/>')
    # il Cannath (in magra a +13: il foro sta 8 m sopra il fiume) e il ponte
    f.el(f'<rect x="436" y="{Y(13):.1f}" width="46" height="{Y(9) - Y(13):.1f}" fill="url(#sc-onde)"/>')
    f.el(f'<rect x="396" y="{Y(21) - 3:.1f}" width="86" height="3" fill="{C["lastre_b"]}" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.8"/>')
    f.el(f'<rect x="452" y="{Y(21):.1f}" width="12" height="{Y(9) - Y(21):.1f}" fill="{C["lastre_b"]}" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.8"/>')
    f.t(470, Y(21) - 6, "il Ponte", CORPO, "middle", style="italic")
    f.t(459, Y(10.6) + 2, "Cannath, +13", CORPO, "middle", style="italic")
    # la Cattedrale e la cripta
    f.el(f'<path d="M30 {Y(23):.1f} L30 {Y(29):.1f} L64 {Y(32):.1f} L98 {Y(29):.1f} L98 {Y(23):.1f} z" '
         f'fill="{C["piatto"]}" stroke="{C["inchiostro"]}" stroke-width="0.9"/>')
    f.t(64, Y(25), "Cattedrale", CORPO, "middle", style="italic")
    f.el(f'<rect x="40" y="{Y(21):.1f}" width="50" height="{Y(17) - Y(21):.1f}" fill="{ARIA}" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.9"/>')
    f.el(f'<line x1="44" y1="{Y(23):.1f}" x2="44" y2="{Y(21):.1f}" stroke="{C["inchiostro"]}" stroke-width="0.8"/>')
    # la galleria di servizio (non in scala): dalla cripta al cornicione ovest
    gal = [(90, Y(17.5)), (118, Y(14)), (126, Y(12.6))]
    gal2 = [(134, Y(11.2)), (150, Y(6.4))]
    for tratto in (gal, gal2):
        _via(f, tratto, colore=ARIA)
        d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}" for i, (x, y) in enumerate(tratto))
        f.el(f'<path d="{d}" fill="none" stroke="{ARIA}" stroke-width="7"/>')
        f.el(f'<path d="{d}" fill="none" stroke="{C["inchiostro"]}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    f.t(129, Y(12) + 2, "≈", 9, "middle", weight="bold")
    # le piazze e le case sopra la cisterna
    for x0, w, h in ((150, 30, 9), (184, 24, 7), (300, 26, 8), (330, 30, 10), (364, 26, 7)):
        f.el(f'<path d="M{x0} {Y(21):.1f} l0 {-h} l{w / 2:.1f} -5 l{w / 2:.1f} 5 l0 {h} z" fill="{C["piatto"]}" '
             f'stroke="{C["inchiostro"]}" stroke-width="0.7"/>')
    f.t(X(20) + 3, Y(21) - 20, "il Mercato del Ponte, +21", CORPO, "middle", style="italic")
    f.el(f'<path d="M{X(20) - 9:.1f} {Y(21):.1f} l0 -9 l21 0 l0 9 M{X(20) - 11:.1f} {Y(21) - 9:.1f} '
         f'l25 0" fill="none" stroke="{C["inchiostro"]}" stroke-width="1"/>')
    # la cisterna: l'aria, l'acqua, la vasca
    f.el(f'<rect x="{X(1):.1f}" y="{Y(18):.1f}" width="{X(39) - X(1):.1f}" height="{Y(0) - Y(18):.1f}" '
         f'fill="{ARIA}" stroke="{C["inchiostro"]}" stroke-width="1.2"/>')
    f.el(f'<rect x="{X(1):.1f}" y="{Y(1):.1f}" width="{X(39) - X(1):.1f}" height="{Y(0) - Y(1):.1f}" '
         f'fill="{C["acqua"]}"/>')
    f.el(f'<rect x="{X(14):.1f}" y="{Y(0):.1f}" width="{X(26) - X(14):.1f}" height="{Y(-6) - Y(0):.1f}" '
         f'fill="{C["acqua"]}" stroke="{C["inchiostro"]}" stroke-width="0.9"/>')
    # il pozzo grande attraverso la volta, e la gabbia
    f.el(f'<rect x="{X(20) - 2:.1f}" y="{Y(21):.1f}" width="10" height="{Y(18) - Y(21):.1f}" fill="{ARIA}"/>')
    f.el(f'<line x1="{X(20) + 3:.1f}" y1="{Y(21):.1f}" x2="{X(20) + 3:.1f}" y2="{Y(16.6):.1f}" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.6"/>')
    f.el(f'<rect x="{X(20) - 2:.1f}" y="{Y(16.6):.1f}" width="10" height="{Y(15) - Y(16.6):.1f}" fill="none" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.9"/>')
    # i pilastri, sullo sfondo
    for c in (5, 15, 25):
        f.el(f'<rect x="{X(c):.1f}" y="{Y(18):.1f}" width="6" height="{Y(1) - Y(18):.1f}" fill="{C["roccia"]}" '
             f'fill-opacity="0.35"/>')
    # la Torre delle Volte
    f.el(f'<rect x="{X(27):.1f}" y="{Y(12):.1f}" width="{X(39) - X(27):.1f}" height="{Y(0) - Y(12):.1f}" '
         f'fill="{C["lastre"]}" stroke="{C["inchiostro"]}" stroke-width="1.3"/>')
    for q in (6,):
        f.el(f'<line x1="{X(27):.1f}" y1="{Y(q):.1f}" x2="{X(39):.1f}" y2="{Y(q):.1f}" '
             f'stroke="{C["inchiostro"]}" stroke-width="1"/>')
    f.t(X(27) + 3, Y(9) + 2, "officina", CORPO, style="italic")
    f.t(X(34) + 2, Y(3) + 2, "chiuse", CORPO, style="italic")
    for x in (X(29), X(36)):
        f.el(f'<rect x="{x:.1f}" y="{Y(13.6):.1f}" width="5" height="6.4" fill="{C["marker"]}" '
             f'fill-opacity="0.8"/>')
    # la chiocciola, fino al Santuario
    f.el(f'<rect x="{X(32):.1f}" y="{Y(6):.1f}" width="8" height="{Y(-12) - Y(6):.1f}" fill="{ARIA}" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.7"/>')
    for i in range(12):
        y = Y(6) + i * (Y(-12) - Y(6)) / 12
        f.el(f'<line x1="{X(32):.1f}" y1="{y + 6:.1f}" x2="{X(32) + 8:.1f}" y2="{y:.1f}" '
             f'stroke="{C["sbiadito"]}" stroke-width="0.6"/>')
    # le passerelle, il ponte maestro, i cornicioni
    f.el(f'<rect x="{X(1):.1f}" y="{Y(15):.1f}" width="{X(39) - X(1):.1f}" height="2" fill="#8a6d47"/>')
    for c in (10, 20, 30):
        f.el(f'<rect x="{X(c):.1f}" y="{Y(15) - 1:.1f}" width="6" height="4" fill="#8a6d47"/>')
    f.el(f'<rect x="{X(1):.1f}" y="{Y(6):.1f}" width="{X(27) - X(1):.1f}" height="2.5" fill="{C["lastre_b"]}" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.5"/>')
    for i in range(26):
        f.el(f'<line x1="{X(1 + i) + 3:.1f}" y1="{Y(6):.1f}" x2="{X(1 + i) + 3:.1f}" y2="{Y(7):.1f}" '
             f'stroke="{C["inchiostro"]}" stroke-width="0.5"/>')
    # le catene e i nidi
    for c, fondo in ((7, 1), (13, 1), (17, 1), (24, 1), (33, 12)):
        _catena(f, X(c) + 3, Y(18), Y(fondo))
    _nido(f, X(2), X(8), Y(18), Y(15.5))
    _nido(f, X(31), X(38), Y(18), Y(15.5))
    _ragno(f, X(5), Y(16.3), 9)
    _ragno(f, X(26), Y(13.5), 9, etereo=True)
    # il Santuario di Sale: la volta a −1, che scende a −7 sotto la vasca e tocca l'acqua al sifone
    gr = [(X(6), Y(-12)), (X(6), Y(-3)), (X(8), Y(-1)), (X(13), Y(-1)), (X(13.5), Y(-7)),
          (X(19), Y(-7)), (X(19), Y(-12.2)), (X(21.2), Y(-12.2)), (X(21.2), Y(-7)), (X(26.5), Y(-7)),
          (X(27), Y(-1)), (X(32), Y(-1)), (X(35), Y(-4)), (X(35), Y(-12))]
    d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}" for i, (x, y) in enumerate(gr))
    f.el(f'<path d="{d} z" fill="{ARIA}" stroke="{C["inchiostro"]}" stroke-width="1.1"/>')
    f.el(f'<rect x="{X(12):.1f}" y="{Y(-12):.1f}" width="{X(30) - X(12):.1f}" height="{Y(-21) - Y(-12):.1f}" '
         f'fill="{C["acqua"]}" stroke="{C["inchiostro"]}" stroke-width="0.9"/>')
    f.el(f'<rect x="{X(19):.1f}" y="{Y(-6):.1f}" width="{X(21.2) - X(19):.1f}" height="{Y(-12.2) - Y(-6):.1f}" '
         f'fill="{C["acqua"]}" stroke="{C["inchiostro"]}" stroke-width="0.6"/>')
    f.el(f'<path d="M{X(23.5):.1f} {Y(-12):.1f} l4 -2 l8 0 l4 2 z" fill="#dfe6e4" stroke="{C["inchiostro"]}" '
         f'stroke-width="0.7"/>')
    f.el(f'<circle cx="{X(24.5) + 2:.1f}" cy="{Y(-12) - 5:.1f}" r="3" fill="#8fe0a8" stroke="#2f6b3f" '
         f'stroke-width="0.8"/>')
    for c, h in ((8, 6), (10, 4), (31, 5), (33, 7)):
        _cristallo(f, X(c), Y(-12), h * 2.4, "#eef0ea")
    # Karkator nella vasca
    f.el(f'<path d="M{X(14):.1f} {Y(-16):.1f} q18 -8 46 -2 q12 3 22 0 l-6 6 q-30 6 -62 -4 z" fill="#c9c7bd" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.8"/>')
    # la galleria di drenaggio verso il fiume (non in scala)
    # sale di 25 m in 300 m: la sorgente del Santuario è in pressione e l'acqua la risale
    f.el(f'<path d="M{X(35):.1f} {Y(-10):.1f} L392 {Y(-2):.1f} M402 {Y(0.6):.1f} L428 {Y(13.6):.1f}" '
         f'fill="none" stroke="{ARIA}" stroke-width="9"/>')
    f.el(f'<path d="M{X(35):.1f} {Y(-12):.1f} L392 {Y(-4):.1f} M402 {Y(-1.4):.1f} L432 {Y(12.6):.1f}" '
         f'fill="none" stroke="{C["acqua_b"]}" stroke-width="1.6"/>')
    f.el(f'<path d="M428 {Y(13):.1f} l0 -5 a4.5 4.5 0 0 1 9 0 l0 5" fill="{C["acqua"]}" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.9"/>')
    f.t(397, Y(-1) + 3, "≈", 9, "middle", weight="bold")
    _via(f, [(372, Y(-10.6)), (370, Y(-18)), (368, Y(-22))], tratteggio=True)
    f.el(f'<line x1="368" y1="{Y(-21):.1f}" x2="367" y2="{Y(-23.6):.1f}" stroke="{C["inchiostro"]}" '
         f'stroke-width="0.8" marker-end="url(#sc-freccia)"/>')
    # il righello delle quote
    for q, s in ((21, "+21"), (18, "+18"), (15, "+15"), (12, "+12"), (6, "+6"), (0, "0"), (-6, "−6"),
                 (-12, "−12"), (-21, "−21")):
        f.el(f'<line x1="{X(39) + 6:.1f}" y1="{Y(q):.1f}" x2="{X(39) + 10:.1f}" y2="{Y(q):.1f}" '
             f'stroke="{C["inchiostro"]}" stroke-width="0.6"/>')
    for q, s in ((18, "+18"), (15, "+15"), (12, "+12"), (6, "+6"), (0, "0"), (-6, "−6"), (-12, "−12")):
        f.t(X(1) - 4, Y(q) + 2.6, s, CORPO, "end", C["carta"] if q in (18,) else C["carta"], "bold")
    # i numeri
    for n, x, y in ((1, 64, Y(19)), (2, 112, Y(18)), (3, X(20) - 12, Y(16)), (4, X(5), Y(13.4)),
                    (5, X(26) - 2, Y(10.6)), (6, X(10), Y(8.6)), (7, X(33), Y(14.8)), (8, X(8), Y(3)),
                    (9, X(16), Y(-3)), (10, X(19) - 7, Y(-9.5)), (11, X(25), Y(-9.5)), (12, X(15), Y(-18.6)),
                    (13, X(33) + 13, Y(-6)), (14, 414, Y(-4)), (15, 384, Y(-19)), (16, 444, Y(17.4))):
        f.num(n, x, y)
    f.h = round(Y(-24) + 8)
    return f.svg()


def gs_s1_legenda() -> str:
    f = Foglio(500)
    f.titolo("GS-S1 · Indicazioni", "i numeri della sezione · le quote valgono per tutte le piante GS-1…GS-6")
    yl = f.legenda(56, [
        (1, "La cripta della Cattedrale (ingresso A): 6 m sotto la navata, nel quartiere alto"),
        (2, "A2, la galleria di servizio: 400 m in discesa fino al cornicione ovest, a +6 (non in scala)"),
        (3, "Il pozzo grande del Mercato (ingresso C): la gabbia scende 6 m e attraversa la volta"),
        (4, "G2, il nido ovest, e un Ragno delle Catene sulla sua seta (GS-S2)"),
        (5, "Un ragno etereo sotto le passerelle: passa nel Materiale con un'azione gratuita"),
        (6, "Le passerelle a +15, senza parapetto. Sotto, la quota media a +6 e il fondo a 0"),
        (7, "G3, il nido est, sopra la Torre. Una catena tocca il terrazzo a +12"),
        (8, "Il ponte maestro a +6, 39 m dal cornicione ovest alla porta della Torre"),
        (9, "G6, la vasca centrale: 6 m d'acqua torbida, fino a −6. Le navate attorno hanno 1 m d'acqua"),
        (10, "Il sifone: 6 m in giù dal fondo della vasca; sbocca sotto il lembo di roccia che tocca "
             "l'acqua del Santuario"),
        (11, "L'isolotto e il Cuore di Selenite, mezzo metro sopra l'acqua"),
        (12, "Karkator nella vasca salmastra, profonda 9 m. La volta della grotta è a −1: sopra c'è un metro "
             "di roccia e poi il fondo delle navate"),
        (13, "T3, la scala a chiocciola: 18 m da +6 a −12, attorno a un pozzo aperto (6d6 a chi ci cade)"),
        (14, "B2, la galleria di drenaggio: 300 m in salita fino al fiume, non in scala. Sale di 25 m, e l'acqua "
             "la risale perché la sorgente del Santuario è in pressione"),
        (15, "B3, lo scavo dei drow: due chilometri verso sud e il Sottosuolo"),
        (16, "B1, lo sfioratore (ingresso B): la bocca sotto la seconda pila del Ponte, sul pelo del Cannath (+13)"),
    ], colonne=1)
    f.h = round(yl + 6)
    return f.svg()


def _pannello(f, y0, titolo, k=7.0):
    """Una fetta della cisterna fra +18 e 0, a tutta larghezza (1,5 m = 10,5 pt)."""
    def Y(q):
        return y0 + 14 + (18.5 - q) * k

    def X(c):
        return 34 + c * 10.8
    f.t(14, y0 + 8, titolo, 8.5, fam="Cinzel", weight="bold")
    f.el(f'<clipPath id="sc-pann-{int(y0)}"><rect x="{X(1):.1f}" y="{Y(18):.1f}" width="{X(39) - X(1):.1f}" '
         f'height="{Y(0) - Y(18):.1f}"/></clipPath>')
    f.el(f'<rect x="{X(1):.1f}" y="{Y(18):.1f}" width="{X(39) - X(1):.1f}" height="{Y(0) - Y(18):.1f}" '
         f'fill="{ARIA}" stroke="{C["inchiostro"]}" stroke-width="1"/>')
    f.el(f'<rect x="{X(1):.1f}" y="{Y(1):.1f}" width="{X(39) - X(1):.1f}" height="{Y(0) - Y(1):.1f}" '
         f'fill="{C["acqua"]}"/>')
    f.el(f'<rect x="{X(14):.1f}" y="{Y(1):.1f}" width="{X(26) - X(14):.1f}" height="{Y(0) - Y(1):.1f}" '
         f'fill="{C["acqua_b"]}" fill-opacity="0.6"/>')
    f.el(f'<rect x="{X(27):.1f}" y="{Y(12):.1f}" width="{X(39) - X(27):.1f}" height="{Y(0) - Y(12):.1f}" '
         f'fill="{C["lastre"]}" stroke="{C["inchiostro"]}" stroke-width="1"/>')
    f.t((X(27) + X(39)) / 2, Y(8), "la Torre", CORPO, "middle", style="italic")
    f.el(f'<rect x="{X(1):.1f}" y="{Y(6):.1f}" width="{X(27) - X(1):.1f}" height="2.5" fill="{C["lastre_b"]}"/>')
    f.t(X(3), Y(6) - 3, "ponte maestro, +6", CORPO, style="italic")
    f.el(f'<rect x="{X(1):.1f}" y="{Y(15):.1f}" width="{X(39) - X(1):.1f}" height="2.5" fill="#8a6d47"/>')
    f.t(X(1) - 3, Y(15) + 2.6, "+15", CORPO, "end")
    f.t(X(1) - 3, Y(6) + 2.6, "+6", CORPO, "end")
    f.t(X(1) - 3, Y(0) + 1, "0", CORPO, "end")
    f.t(X(1) - 3, Y(18) + 4, "+18", CORPO, "end")
    for c, fondo in ((7, 1), (13, 1), (17, 1), (24, 1), (33, 12)):
        _catena(f, X(c) + 5, Y(18), Y(fondo))
    _nido(f, X(2), X(8), Y(18), Y(15.6))
    _nido(f, X(31), X(38), Y(18), Y(15.6))
    f.el(f'<rect x="{X(20) - 2:.1f}" y="{Y(17):.1f}" width="13" height="{Y(15) - Y(17):.1f}" fill="none" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.9"/>')
    f.el(f'<line x1="{X(20) + 4.5:.1f}" y1="{Y(18):.1f}" x2="{X(20) + 4.5:.1f}" y2="{Y(17):.1f}" '
         f'stroke="{C["inchiostro"]}" stroke-width="0.7"/>')
    return X, Y


def _freccia(f, x0, y0, x1, y1, rossa=True, tratteggio=True, curva=0.0):
    col = C["marker"] if rossa else C["inchiostro"]
    mk = "sc-freccia-r" if rossa else "sc-freccia"
    ds = ' stroke-dasharray="4 2.5"' if tratteggio else ""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - curva
    f.el(f'<path d="M{x0:.1f} {y0:.1f} Q{mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="{col}" '
         f'stroke-width="1.2"{ds} marker-end="url(#{mk})"/>')


def gs_s2() -> str:
    f = Foglio(700)
    f.titolo("GS-S2 · L'incontro coi Ragni delle Catene, in sezione",
             "G1, quota alta · tre momenti dello scontro · in scala, 1,5 m = 10,8 pt · tratteggio: etereo")
    PASSO = 150
    # round 1
    X, Y = _pannello(f, 42, "Round 1 · le catene vibrano")
    for c, n in ((20, None), (21.2, None), (22.4, None)):
        _pg(f, X(c), Y(15) - 4, n)
    _pg(f, X(27), Y(15) - 4, "Thorik")
    _ragno(f, X(5), Y(16.4), 15)
    _ragno(f, X(34.5), Y(16.4), 15)
    _ragno(f, X(13), Y(13.4), 15, etereo=True)
    _ragno(f, X(29), Y(13.4), 15, etereo=True)
    _freccia(f, X(6.5), Y(15.5), X(11.6), Y(13.6), rossa=False, curva=-8)
    _freccia(f, X(33.5), Y(15.5), X(30.4), Y(13.6), rossa=False, curva=-8)
    f.num(1, X(27), Y(15) - 22)
    f.num(2, X(5), Y(13.2))
    f.num(3, X(21), Y(11.8))
    # round 2
    X, Y = _pannello(f, 42 + PASSO, "Round 2 · alle spalle dell'isolato")
    for c in (20, 21.2, 22.4):
        _pg(f, X(c), Y(15) - 4)
    _pg(f, X(27), Y(15) - 4, "Thorik")
    _ragno(f, X(29.8), Y(15) - 7, 15)
    _ragno(f, X(24) + 5, Y(12), 15)
    _freccia(f, X(24) + 12, Y(12.4), X(26.6), Y(15) - 6, curva=10)
    f.el(f'<path d="M{X(26.2):.1f} {Y(15) + 2.5:.1f} l3 -6 l3 6 l3 -6 l3 6" fill="none" stroke="{C["marker"]}" '
         f'stroke-width="1.1"/>')
    f.num(4, X(29.8), Y(15) - 22)
    f.num(5, X(22.3), Y(11))
    f.num(6, X(24), Y(17.4))
    # round 3
    X, Y = _pannello(f, 42 + 2 * PASSO, "Dal round 3 · il volatore")
    for c in (20, 21.2, 22.4):
        _pg(f, X(c), Y(15) - 4)
    _pg(f, X(27), Y(15) - 4, "Thorik")
    f.el(f'<path d="M{X(26.2):.1f} {Y(15) + 2.5:.1f} l3 -6 l3 6 l3 -6 l3 6" fill="none" stroke="{C["marker"]}" '
         f'stroke-width="1.1"/>')
    _ragno(f, X(29.8), Y(15) - 7, 15)
    _pg(f, X(19), Y(9.5), "Artemis", "#6a4fa0")
    _ragno(f, X(13) + 5, Y(8), 15)
    clip = f' clip-path="url(#sc-pann-{42 + 2 * PASSO})"'
    f.el(f'<circle cx="{X(13) + 5:.1f}" cy="{Y(8):.1f}" r="{8 * 10.8:.1f}" fill="none" stroke="{C["marker"]}" '
         f'stroke-width="0.7" stroke-dasharray="1.5 2.5"{clip}/>')
    _freccia(f, X(13) + 12, Y(8.4), X(18.6), Y(9.6), curva=8)
    f.el(f'<line x1="{X(19):.1f}" y1="{Y(9.5) + 4:.1f}" x2="{X(19):.1f}" y2="{Y(1):.1f}" stroke="{C["marker"]}" '
         f'stroke-width="0.8" stroke-dasharray="1 2"/>')
    f.el(f'<circle cx="{X(10):.1f}" cy="{Y(15):.1f}" r="{4 * 10.8:.1f}" fill="#b9b6a2" fill-opacity="0.45" '
         f'stroke="{C["sbiadito"]}" stroke-width="0.7" stroke-dasharray="3 2"{clip}/>')
    f.num(7, X(13) + 5, Y(5.6))
    f.num(8, X(19) + 12, Y(8.2))
    f.num(9, X(10), Y(12.4))
    f.num(10, X(13) + 5 + 60, Y(8) - 60)
    f.h = 42 + 3 * PASSO + 4
    return f.svg()


def gs_s2_legenda() -> str:
    f = Foglio(500)
    f.titolo("GS-S2 · Lo scontro coi Ragni delle Catene", "i numeri dei tre momenti · conti in appendice, Ragno delle Catene")
    yl = f.legenda(56, [
        (1, "Chi cammina oltre 3 m dalla gabbia, o tocca una catena, fa vibrare la rete: i ragni non sono "
            "sorpresi, salvo silenzio o volo"),
        (2, "I due ragni sono sui nidi, a ovest e a est, fra le passerelle e la volta"),
        (3, "Azione di movimento: passano nell'Etereo. Poi si muovono di 12 m sotto le passerelle, dove "
            "nessuno li vede"),
        (4, "Il ragno est torna nel Materiale alle spalle del PG più isolato (azione gratuita) e morde: "
            "+20, 1d8+12 e veleno, Tempra CD 24, 2d6 Cos"),
        (5, "Il ragno ovest resta a distanza e lancia le catene (15 m, incremento 3 m)"),
        (6, "Il colpito è ancorato alla passerella: Artista della Fuga CD 22 o Forza CD 26; le catene "
            "hanno durezza 10 e 20 pf"),
        (7, "Un ragno tiene l'ancorato, l'altro sale una catena (12 m a round) verso chi vola"),
        (8, "Le catene raggiungono anche il volatore: resta appeso dov'è e non cade"),
        (9, "Se la Torre è allertata, Tariq lancia nube acida su un incrocio: 2d6 acido a round, "
            "occultamento oltre 1,5 m"),
        (10, "Risonanza delle catene (in punteggiato, 12 m): chi vola fa Tempra CD 22 o è assordato per "
             "1d4 round. Sotto il 25% dei pf i ragni se ne vanno nell'Etereo e riferiscono a Tariq"),
    ], colonne=1)
    yl += 4
    f.t(14, yl + 6, "Chi cade dalle passerelle: 3 m sul tetto della Torre (1d6), 9 m su un ponte o un cornicione "
        "(3d6), 15 m sul fondo sotto un metro d'acqua (5d6).", CORPO, style="italic")
    f.t(14, yl + 6 + CORPO * 1.3, "EL 12 con i due ragni. Chi arriva da A o da B può non incontrarli mai.",
        CORPO, style="italic")
    f.h = round(yl + 6 + CORPO * 1.3 + 8)
    return f.svg()


# --- GS-R: Rethmar, il foro e i tre ingressi, sulla pianta canonica della città
PIANTA_RETHMAR = (RADICE.parent / "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist" / "Mappe" / "rethmar"
                  / "rethmar-pianta.svg")
# La trasformazione metri → pixel della pianta (scripts/piante/rethmar.py: K, OX, OY). Se la pianta canonica cambia
# taglia, questi tre numeri vanno ripresi da lì: genera_pianta_citta.py --check lo segnala per primo.
R_K, R_OX, R_OY = 0.5393598899705937, 682.0, 500.0
R_X0, R_Y0, R_LATO = -350.0, -390.0, 580.0        # la finestra, in metri: dal Ponte Nuovo alla Cattedrale
R_TOP = 44.0


def _r_px(x: float, y: float) -> tuple[float, float]:
    """Un punto della città (metri della pianta) nel foglio dello schema."""
    s = W / R_LATO
    return (x - R_X0) * s, R_TOP + (y - R_Y0) * s


def gs_r() -> str:
    import re
    f = Foglio(R_TOP + W + 4)
    f.titolo("GS-R · Rethmar: il foro, la Cattedrale, il Ponte e i tre ingressi",
             "sulla pianta canonica della città · in rosso gli ingressi, in blu quello che sta sotto le strade")
    sorgente = PIANTA_RETHMAR.read_text(encoding="utf-8")
    dentro = re.sub(r"^<svg[^>]*>|</svg>\s*$", "", sorgente.strip())
    dentro = re.sub(r"<title>.*?</title>|<desc>.*?</desc>", "", dentro, flags=re.S)
    vx, vy = R_OX + R_X0 * R_K, R_OY + R_Y0 * R_K
    lato = R_LATO * R_K

    def nella_finestra(m) -> str:
        """Le scritte della pianta che la finestra taglierebbe a metà non vanno in stampa."""
        x, y, corpo, ancora = float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4)
        largo = len(re.sub(r"<[^>]+>", "", m.group(5))) * corpo * 0.62
        sx = {"start": 0.0, "middle": 0.5, "end": 1.0}.get(ancora, 0.0) * largo
        dentro_ = (x - sx >= vx + 3 and x - sx + largo <= vx + lato - 3
                   and y - corpo >= vy + 3 and y + 3 <= vy + lato)
        return m.group(0) if dentro_ else ""
    dentro = re.sub(r'<text x="([\d.]+)" y="([\d.]+)"[^>]*?font-size="([\d.]+)"[^>]*?text-anchor="(\w+)"[^>]*>(.*?)</text>',
                    nella_finestra, dentro, flags=re.S)
    f.el(f'<svg x="0" y="{R_TOP:g}" width="{W:g}" height="{W:g}" viewBox="{vx:.2f} {vy:.2f} {lato:.2f} {lato:.2f}">'
         f'{dentro}</svg>')
    f.el(f'<rect x="0" y="{R_TOP:g}" width="{W:g}" height="{W:g}" fill="none" stroke="{C["inchiostro"]}" '
         f'stroke-width="1.2"/>')
    P_ = _r_px
    alone = 'stroke="#f6ecd2" stroke-width="2.6" paint-order="stroke"'

    def scritta(x, y, testo, anchor="start", fill=None, size=CORPO, weight="normal"):
        f.el(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-style="italic" '
             f'font-weight="{weight}" fill="{fill or C["inchiostro"]}" {alone}>{escape(testo)}</text>')

    # la cisterna sotto il foro, 57 × 37,5 m
    cx, cy = -87.7, -226.5
    x0, y0 = P_(cx - 28.5, cy - 18.75)
    x1, y1 = P_(cx + 28.5, cy + 18.75)
    f.el(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" fill="{C["acqua"]}" '
         f'fill-opacity="0.45" stroke="{C["acqua_b"]}" stroke-width="1.4" stroke-dasharray="4 2.5"/>')
    # A: la galleria di servizio, dalla cripta della Cattedrale al cornicione ovest (circa 400 m)
    a0, a1 = P_(-133, 163), P_(cx - 28.5, cy)
    f.el(f'<path d="M{a0[0]:.1f} {a0[1]:.1f} L{a1[0]:.1f} {a1[1]:.1f}" fill="none" stroke="{C["acqua_b"]}" '
         f'stroke-width="1.6" stroke-dasharray="5 3"/>')
    # B: la galleria di drenaggio, dal Santuario alla bocca sotto la seconda pila (circa 300 m)
    via = [P_(x, y) for x, y in ((-60, -226), (10, -212), (45, -250), (5, -292), (-60, -300), (-110, -293))]
    d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}" for i, (x, y) in enumerate(via))
    f.el(f'<path d="{d}" fill="none" stroke="{C["acqua_b"]}" stroke-width="1.6" stroke-dasharray="5 3"/>')
    # le lettere degli ingressi
    for s_, (x, y) in (("A", P_(-112, 150)), ("B", P_(-124, -300)), ("C", P_(cx + 17, cy + 8))):
        _lettera(f, s_, x, y)
    # le scritte
    tx, ty = P_(cx - 28, cy + 30)
    scritta(tx, ty, "la Grande Cisterna, 21 m sotto il foro", fill=C["acqua_b"])
    tx, ty = P_(-128, 40)
    scritta(tx, ty, "galleria di servizio, 400 m", "end", C["acqua_b"])
    tx, ty = P_(52, -270)
    scritta(tx, ty, "galleria di drenaggio, 300 m", fill=C["acqua_b"])
    tx, ty = P_(-140, -310)
    scritta(tx, ty, "la bocca dello sfioratore", "end", C["marker"])
    tx, ty = P_(-200, -195)
    scritta(tx, ty, "Mira Serani, sopra lo speziale", "end")
    tx, ty = P_(25, -190)
    scritta(tx, ty, "la bottega di Tariq")
    # la barra di scala, 100 m
    bx, by = 16.0, R_TOP + W - 16
    lung = 100 * W / R_LATO
    f.el(f'<rect x="{bx - 4:.1f}" y="{by - 14:.1f}" width="{lung + 30:.1f}" height="22" fill="#f6ecd2" '
         f'fill-opacity="0.85"/>')
    f.el(f'<path d="M{bx:.1f} {by:.1f} l{lung:.1f} 0 M{bx:.1f} {by - 3:.1f} l0 6 M{bx + lung:.1f} {by - 3:.1f} '
         f'l0 6" stroke="{C["inchiostro"]}" stroke-width="1.2"/>')
    f.t(bx + lung / 2, by - 5, "100 m", CORPO, "middle")
    return f.svg()


def gs_r_legenda() -> str:
    f = Foglio(400)
    f.titolo("GS-R · Indicazioni", "le lettere sono gli ingressi del modulo; i numeri sono quelli della pianta di Rethmar")
    yl = f.legenda(56, [
        ("A", "La Cattedrale di Lathander, nel quartiere alto: dalla cripta parte la galleria di servizio, 400 m in "
              "discesa fino al cornicione ovest della cisterna (GS-1)"),
        ("B", "Lo sfioratore: la bocca sotto la seconda pila del Ponte, sul pelo del Cannath. La galleria di "
              "drenaggio gira a est del foro, sotto la biblioteca, e scende per 300 m fino al Santuario (GS-1b, GS-6)"),
        ("C", "Il pozzo grande nel foro, sopra il centro della cisterna: la gabbia della gilda (GS-1c)"),
        ("7", "Il Ponte sul Cannath, con le statue. Il gorgo contro corrente è a valle del pilone sud"),
        ("8", "Il Mercato del Ponte, nel foro: la fila per l'acqua, Kesk Martellacqua all'argano"),
        ("18", "La Cattedrale: Tredora Occhidoro, e Fratello Odo nella sacrestia"),
        ("23", "Il Ponte Nuovo, la mescita di Kellin: lì si trova Sal"),
        ("·", "Gli altri numeri sono quelli della pianta di Rethmar di ARC-09 (Porta Nord 3, foro 13, "
              "Municipio 14, Tempio 16, Torrione 19)"),
    ], colonne=1)
    f.h = round(yl + 6)
    return f.svg()


SCHEMI = {
    "T-1-piano-della-terra.svg": t1,
    "T-4-approccio-al-tempio.svg": t4,
    "M7-A-hammerfist-372.svg": m7a,
    "M7-A-hammerfist-372_legenda.svg": m7a_legenda,
    CARTELLA_GSC / "GS-R-rethmar-ingressi.svg": gs_r,
    CARTELLA_GSC / "GS-R-rethmar-ingressi_legenda.svg": gs_r_legenda,
    CARTELLA_GSC / "GS-0-collegamenti.svg": gs0,
    CARTELLA_GSC / "GS-0-collegamenti_legenda.svg": gs0_legenda,
    CARTELLA_GSC / "GS-S1-sezione-cisterna.svg": gs_s1,
    CARTELLA_GSC / "GS-S1-sezione-cisterna_legenda.svg": gs_s1_legenda,
    CARTELLA_GSC / "GS-S2-ragni-delle-catene.svg": gs_s2,
    CARTELLA_GSC / "GS-S2-ragni-delle-catene_legenda.svg": gs_s2_legenda,
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="verifica senza scrivere")
    args = ap.parse_args(argv)
    errori = 0
    for nome, fn in SCHEMI.items():
        p = CARTELLA / nome      # una Path assoluta (gli schemi del Giardino) resta com'è
        svg = fn()
        if args.check:
            if not p.exists() or p.read_text(encoding="utf-8") != svg:
                print(f"✗ {p.relative_to(RADICE.parent)} non è allineato: python3 scripts/render_schemi.py")
                errori += 1
        else:
            p.parent.mkdir(exist_ok=True)
            p.write_text(svg, encoding="utf-8")
            print(f"✓ {p.relative_to(RADICE.parent)}")
    if args.check and not errori:
        print(f"✓ render_schemi: {len(SCHEMI)} schemi allineati")
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main())
