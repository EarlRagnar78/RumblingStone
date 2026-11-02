"""Pezzi comuni delle piante di città (palette, SVG a mano, scala, rosa): deterministico."""
import math
import random

FONT = "Georgia,'Liberation Serif','DejaVu Serif',serif"
COL = {
    "carta": "#efe4c8", "carta2": "#e6d8b4", "inchiostro": "#3a2f22", "sbiadito": "#6b5a3a",
    "campo": "#dfe0b0", "campo2": "#d3d59c", "prato": "#c9d6a0", "bosco": "#8fae6e", "bosco2": "#6f8f52",
    "acqua": "#7fb2c9", "acqua_s": "#3f7d99", "golena": "#b9d3cf",
    "strada": "#efe2c2", "strada_bordo": "#b49a6c", "selciato": "#e8dcc0",
    "casa": "#b8664a", "casa_s": "#7a3d2a", "corte": "#e3d3a8", "giardino": "#a9bf86",
    "pubblico": "#c99a5b", "pubblico_s": "#6d4b25", "sacro": "#d9c48f", "sacro_s": "#6d5525",
    "mura": "#5b4a3a", "torre": "#4a3b2d", "fossato": "#9cc0c4", "fossato_s": "#5d8d93",
    "marker": "#7a1f1a", "marker_t": "#fff8e8", "tenda": "#e9dfc2", "tenda_s": "#8a7350",
    "isoipsa": "#a0835a",
}


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


class Svg:
    def __init__(self, w, h, ox, oy, k):
        self.w, self.h, self.ox, self.oy, self.k = w, h, ox, oy, k
        self.out = []

    def p(self, x, y):
        return (self.ox + x * self.k, self.oy + y * self.k)

    def pt(self, x, y):
        a, b = self.p(x, y)
        return f"{a:.1f},{b:.1f}"

    def add(self, s):
        self.out.append(s)

    def rect_m(self, x0, y0, x1, y1, fill, stroke="none", sw=0.6, extra=""):
        a, b = self.p(min(x0, x1), min(y0, y1))
        w, h = abs(x1 - x0) * self.k, abs(y1 - y0) * self.k
        self.add(f'<rect x="{a:.1f}" y="{b:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def poly_m(self, pts, fill, stroke="none", sw=0.6, extra="", chiuso=True):
        d = "M" + " L".join(self.pt(x, y) for x, y in pts) + (" Z" if chiuso else "")
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def line_m(self, pts, stroke, sw, extra=""):
        d = "M" + " L".join(self.pt(x, y) for x, y in pts)
        self.add(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
                 f'stroke-linejoin="round" stroke-linecap="round" {extra}/>')

    def text(self, x, y, s, size=12, anchor="start", fill=None, weight="normal", style="normal",
             extra=""):
        fill = fill or COL["inchiostro"]
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
                 f'text-anchor="{anchor}" fill="{fill}" font-weight="{weight}" '
                 f'font-style="{style}" {extra}>{esc(s)}</text>')

    def text_m(self, x, y, s, **kw):
        a, b = self.p(x, y)
        self.text(a, b, s, **kw)

    def marker(self, x, y, n):
        a, b = self.p(x, y)
        r = 7.5 if n < 10 else 8.5
        self.add(f'<g><circle cx="{a:.1f}" cy="{b:.1f}" r="{r}" fill="{COL["marker"]}" '
                 f'stroke="{COL["marker_t"]}" stroke-width="1.4"/>'
                 f'<text x="{a:.1f}" y="{b + 3.6:.1f}" font-family="{FONT}" font-size="10" '
                 f'font-weight="bold" text-anchor="middle" fill="{COL["marker_t"]}">{n}</text></g>')

    def svg(self, titolo, desc):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}" role="img" aria-label="{esc(titolo)}">\n'
                f'<title>{esc(titolo)}</title>\n<desc>{esc(desc)}</desc>\n')
        return head + "\n".join(self.out) + "\n</svg>\n"


def isolato(s, rng, x0, y0, x1, y1, prof=(10, 16), lotto=(7, 16)):
    """Un isolato di case: un anello di lotti sul fronte strada, corti e orti dentro."""
    if x1 - x0 < 6 or y1 - y0 < 6:
        return
    s.rect_m(x0, y0, x1, y1, COL["casa"], COL["casa_s"], 0.7)
    w, h = x1 - x0, y1 - y0
    d = rng.uniform(*prof)
    if w > 2 * d + 6 and h > 2 * d + 6:
        # il cuore dell'isolato: corti e orti
        cx0, cy0, cx1, cy1 = x0 + d, y0 + d, x1 - d, y1 - d
        s.rect_m(cx0, cy0, cx1, cy1, COL["giardino"] if rng.random() < 0.55 else COL["corte"],
                 COL["casa_s"], 0.4)
        # qualche casa a corte che entra nel cuore
        for _ in range(int((cx1 - cx0) * (cy1 - cy0) / 900)):
            bx = rng.uniform(cx0, cx1 - 8)
            by = rng.uniform(cy0, cy1 - 8)
            s.rect_m(bx, by, min(bx + rng.uniform(6, 12), cx1), min(by + rng.uniform(6, 10), cy1),
                     COL["casa"], COL["casa_s"], 0.4)
        # i confini dei lotti sul fronte
        x = x0 + rng.uniform(*lotto)
        while x < x1 - 4:
            s.line_m([(x, y0), (x, y0 + d)], COL["casa_s"], 0.5)
            s.line_m([(x, y1), (x, y1 - d)], COL["casa_s"], 0.5)
            x += rng.uniform(*lotto)
        y = y0 + d + rng.uniform(*lotto)
        while y < y1 - d - 4:
            s.line_m([(x0, y), (x0 + d, y)], COL["casa_s"], 0.5)
            s.line_m([(x1, y), (x1 - d, y)], COL["casa_s"], 0.5)
            y += rng.uniform(*lotto)
    else:
        # isolato stretto: solo lotti in fila
        if w >= h:
            x = x0 + rng.uniform(*lotto)
            while x < x1 - 4:
                s.line_m([(x, y0), (x, y1)], COL["casa_s"], 0.5)
                x += rng.uniform(*lotto)
            if h > 14:
                s.line_m([(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)], COL["casa_s"], 0.5)
        else:
            y = y0 + rng.uniform(*lotto)
            while y < y1 - 4:
                s.line_m([(x0, y), (x1, y)], COL["casa_s"], 0.5)
                y += rng.uniform(*lotto)
            if w > 14:
                s.line_m([((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)], COL["casa_s"], 0.5)


def tenda(s, x, y, r=2.2):
    s.poly_m([(x - r, y + r), (x, y - r), (x + r, y + r)], COL["tenda"], COL["tenda_s"], 0.6)


def barra_scala(s, x, y, metri, passo, etichetta="m"):
    """Barra di scala in px a partire da (x, y), lunga `metri`."""
    k = s.k
    n = int(metri / passo)
    for i in range(n):
        fill = COL["inchiostro"] if i % 2 == 0 else COL["carta"]
        s.add(f'<rect x="{x + i * passo * k:.1f}" y="{y:.1f}" width="{passo * k:.1f}" height="6" '
              f'fill="{fill}" stroke="{COL["inchiostro"]}" stroke-width="0.8"/>')
    for i in range(n + 1):
        s.text(x + i * passo * k, y + 18, f"{int(i * passo)}", size=10, anchor="middle")
    s.text(x + n * passo * k + 10, y + 7, etichetta, size=11)


def rosa(s, x, y, r=26):
    s.add(f'<g stroke="{COL["inchiostro"]}" stroke-width="1">'
          f'<circle cx="{x}" cy="{y}" r="{r}" fill="none"/>'
          f'<path d="M{x},{y - r - 6} L{x + 6},{y} L{x},{y + r} L{x - 6},{y} Z" fill="{COL["carta2"]}"/>'
          f'<path d="M{x},{y - r - 6} L{x + 6},{y} L{x - 6},{y} Z" fill="{COL["marker"]}"/>'
          f'<path d="M{x - r},{y} L{x},{y - 5} L{x + r},{y} L{x},{y + 5} Z" fill="{COL["carta2"]}"/></g>')
    s.text(x, y - r - 10, "N", size=15, anchor="middle", weight="bold")


def area_poligono(pts):
    a = 0
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % len(pts)]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2


def perimetro(pts):
    return sum(math.dist(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))


def lungo(pts, passo, partenza=0.0):
    """Punti ogni `passo` metri lungo il poligono chiuso: (x, y, normale_x, normale_y, s)."""
    out = []
    segs = []
    tot = 0
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        L = math.dist(a, b)
        segs.append((a, b, L, tot))
        tot += L
    d = partenza
    while d < tot - 1e-6:
        for a, b, L, s0 in segs:
            if s0 <= d < s0 + L:
                t = (d - s0) / L
                x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                tx, ty = (b[0] - a[0]) / L, (b[1] - a[1]) / L
                out.append((x, y, ty, -tx, d))  # normale a sinistra del verso
                break
        d += passo
    return out, tot


def rng_for(nome):
    return random.Random(nome)
