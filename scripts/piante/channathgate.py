#!/usr/bin/env python3
"""Channathgate v3: la città APERTA sul Cannath (modello persiano: arg murato sulla terrazza, maidan,
bazar coperto, chahar bagh, qanat; rioni sciolti con fossi, muri d'orto e porte di quartiere; dogane ad
arco sulle strade), una taglia sopra la v2: grande città DMG 3.5, ~25.000 abitanti su ~250 ha. Stesso impianto,
coordinate di progetto moltiplicate per FS = sqrt(250/150); nucleo del bazar più grande e più fitto, due rabad
nuovi, giardini al margine. Motore: piante/organica.py. Uso: python3 scripts/genera_pianta_citta.py channathgate"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shapely import affinity  # noqa: E402
from shapely.geometry import LineString, Point, Polygon, box  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

from comune import COL  # noqa: E402
import organica as O  # noqa: E402

# ---------------------------------------------------------------- obiettivi (rivedibili)
ETTARI_ABITATO = 250.0      # abitato complessivo: grande città (scelta del DM, 2026-10-22)
ABITANTI = 25000
ETTARI_ARG = 5.0            # l'arg murato sulla sua terrazza
ETTARI_NUCLEO = 66.0        # nucleo del bazar, fitto
DENS = {"nucleo": 215, "rione": 72, "giardini": 30, "arg": 60}   # abitanti/ha [INFERRED]
PASSO_TORRI_ARG = 34.0
SEME = 1372
FS = math.sqrt(ETTARI_ABITATO / 150.0)      # fattore lineare sulla v2

OUT = sys.argv[1]
S = 0.6 / FS                   # px per metro
X0, Y0, X1, Y1 = -1050 * FS, -800 * FS, 1070 * FS, 830 * FS
OX0, OY0 = 24, 78
MW, MH = (X1 - X0) * S, (Y1 - Y0) * S
W = int(OX0 + MW + 340)
H = int(OY0 + MH + 26)
F = "font-family=\"Georgia,'Liberation Serif',serif\""
OXm, OYm = OX0 - X0 * S, OY0 - Y0 * S          # traslazione metri -> px


class _S:      # quel che serve a organica.Disegno
    def __init__(self):
        self.out = []
        self.ox, self.oy = OXm, OYm

    def add(self, x):
        self.out.append(x)


sv = _S()
w = sv.add
D = O.Disegno(sv, S)
rng = random.Random(SEME)


def P(x, y):
    return (OXm + x * S, OYm + y * S)


# ---------------------------------------------------------------- il fiume, a ovest, da sud (lago) a nord
FIUME_C = [(-723, 1033), (-775, 723), (-826, 491), (-788, 258), (-762, 52), (-800, -181), (-788, -413), (-723, -646),
           (-671, -955)]
ASSE = O.catmull(FIUME_C, 10)
FW = 80
FIUME = LineString(ASSE).buffer(FW / 2, cap_style=2)
DARSENA = Polygon([(-826, 129), (-932, 116), (-953, 248), (-839, 266)]).union(Polygon([(-852, 142), (-775, 142), (-775, 258), (-852, 258)]))
ACQUA = FIUME.union(DARSENA)

# ---------------------------------------------------------------- nucleo, arg, maidan, bazar
CINTA_K = [(529, -13), (491, 194), (387, 338), (194, 411), (-52, 421), (-284, 387), (-452, 278),
           (-532, 77), (-514, -142), (-411, -307), (-219, -411), (26, -426), (258, -387), (426, -265), (510, -142)]
nuc0 = Polygon(O.catmull(CINTA_K, 8, True))
NUCLEO = affinity.scale(nuc0, math.sqrt(ETTARI_NUCLEO * 1e4 / nuc0.area), math.sqrt(ETTARI_NUCLEO * 1e4 / nuc0.area),
                        origin=(0, 0))
arg0 = Polygon([(219, 226), (426, 181), (510, 297), (387, 426), (194, 432), (155, 323)])
ARG = affinity.scale(arg0, math.sqrt(ETTARI_ARG * 1e4 / arg0.area), math.sqrt(ETTARI_ARG * 1e4 / arg0.area),
                     origin=arg0.centroid)
ARG = Polygon(O.chaikin(list(ARG.exterior.coords)[:-1], 1, chiuso=True))
ARG = affinity.scale(ARG, math.sqrt(ETTARI_ARG * 1e4 / ARG.area), math.sqrt(ETTARI_ARG * 1e4 / ARG.area), origin=ARG.centroid)
TERRAZZA = ARG.buffer(16, join_style=2)
MAID = (-39, -13, 130, 320)
cx, cy, mw, ml = MAID
MAIDAN = box(cx - mw / 2, cy - ml / 2, cx + mw / 2, cy + ml / 2)
ARCATE = MAIDAN.buffer(11, join_style=2).difference(MAIDAN)
for gx, gy in ((cx, cy - ml / 2), (cx, cy + ml / 2), (cx - mw / 2, cy - 20), (cx + mw / 2, cy - 20), (cx - mw / 2, cy + 80)):
    ARCATE = ARCATE.difference(Point(gx, gy).buffer(9))
GONFALONIERE = box(cx - 32, cy + ml / 2 + 13, cx + 32, cy + ml / 2 + 47)
TEMPIO = (cx + mw / 2 + 36, cy + 20)
BAZAR = [(-39, -222), (-103, -265), (-219, -294), (-338, -307), (-465, -346), (-581, -426), (-684, -496)]
BAZAR_L = LineString(O.catmull(BAZAR, 8))
CARAV = [box(-323, -387, -266, -333), box(-181, -253, -129, -204), box(671, -46, 731, 10), box(-620, -387, -563, -338)]

# ---------------------------------------------------------------- i rioni (le posizioni della pianta del DM)
RIONI = {  # nome: (contorno, colore di contrada, contrada, tipo)
    "Golden Plume": ([(607, -336), (826, -387), (1059, -297), (1110, -77), (1059, 155), (891, 271), (671, 297), (555, 219), (584, -13), (555, -194)], "#1f7a44", "l'Oca", "giardini"),
    "Silver Weft": ([(-387, -426), (-207, -491), (52, -510), (297, -465), (387, -555), (232, -723), (-52, -788), (-336, -723), (-491, -555)], "#b8a80f", "il Bruco", "rione"),
    "Gilded Horn": ([(-723, -620), (-542, -529), (-452, -387), (-568, -232), (-607, -52), (-607, 103), (-704, 116), (-723, -181), (-742, -413)], "#2a6fb0", "l'Unicorno", "rione"),
    "Quill-Wood Refuge": ([(-865, -723), (-852, -426), (-859, -181), (-904, -77), (-1084, -103), (-1162, -336), (-1136, -607), (-1007, -775)], "#6b4a1f", "l'Istrice", "tende"),
    "Tidal Crest": ([(-839, -52), (-820, 155), (-852, 336), (-891, 542), (-981, 723), (-1162, 671), (-1188, 387), (-1136, 103), (-1059, -39)], "#1f6f8a", "l'Onda", "rione"),
    "Rabad Nord-Est": ([(x * FS, y * FS) for x, y in [(430, -560), (600, -640), (800, -600), (900, -470), (860, -380), (700, -390), (520, -420)]], "#7a6a50", "rabad", "rione"),
    "Rabad Sud-Est": ([(x * FS, y * FS) for x, y in [(330, 470), (480, 430), (620, 490), (650, 610), (560, 700), (400, 700), (310, 600)]], "#7a6a50", "rabad", "rione"),
    "Whispering Shadows": ([(-555, 374), (-387, 426), (-155, 491), (77, 503), (245, 529), (232, 723), (0, 826), (-297, 800), (-542, 671), (-607, 491)], "#1a1a1a", "la Civetta", "rione"),
}
NUCLEO_RIONI = {"Iron Bastion": ("#8a1f2b", "la Torre"), "Spell-Wyrm Spires": ("#8a2f5f", "il Drago")}
SPOSTA = 1.13      # i rioni si staccano dal nucleo: fra l'uno e l'altro, orti e frutteti


def mv(rione, x, y):
    """Un punto di un rione, spostato come il rione."""
    x, y = x * FS, y * FS        # coordinate della v2
    c = Polygon(O.catmull(RIONI[rione][0], 8, True)).centroid
    return (x + (c.x - cx) * (SPOSTA - 1), y + (c.y - cy) * (SPOSTA - 1))


GIARDINI = [(*mv("Golden Plume", 600, -150), 140, 110), (*mv("Golden Plume", 660, 40), 120, 120), (297, 26, 84, 76),
            (*mv("Quill-Wood Refuge", -770, -380), 84, 76), (*mv("Rabad Nord-Est", 760, -480), 110, 90),
            (*mv("Rabad Sud-Est", 470, 600), 100, 100)]
CB = [box(gx - gw / 2, gy - gh / 2, gx + gw / 2, gy + gh / 2) for gx, gy, gw, gh in GIARDINI]
vx_, vy_ = mv("Whispering Shadows", -300, 602)
VALERIUS = box(vx_ - 30, vy_ - 22, vx_ + 30, vy_ + 22)
STALLE = box(-607, -473, -555, -436)


def blob(pts, f):
    p = Polygon(O.catmull(pts, 8, True))
    c = p.centroid
    p = affinity.translate(p, (c.x - cx) * (SPOSTA - 1), (c.y - cy) * (SPOSTA - 1))
    return affinity.scale(p, f, f, origin=p.centroid)


def costruisci_rioni(f):
    out = {}
    for k, (pts, col, contr, tipo) in RIONI.items():
        out[k] = blob(pts, f).difference(ACQUA.buffer(10)).difference(NUCLEO.buffer(55)).difference(TERRAZZA.buffer(45))
    # niente sovrapposizioni fra rioni
    nomi = list(out)
    for i, a in enumerate(nomi):
        for b in nomi[i + 1:]:
            out[b] = out[b].difference(out[a].buffer(50))
    return out


# la taglia dei rioni è scelta perché l'abitato faccia ETTARI_ABITATO
f = 1.0
for _ in range(30):
    RB = costruisci_rioni(f)
    tot = (unary_union(list(RB.values())).area + NUCLEO.union(TERRAZZA).area) / 1e4
    f *= math.sqrt(ETTARI_ABITATO / tot) ** 0.8
    if abs(tot - ETTARI_ABITATO) < 0.5:
        break
ABITATO = unary_union(list(RB.values()) + [NUCLEO, TERRAZZA])

# ---------------------------------------------------------------- quartieri, vie, lotti
INVILUPPO = ABITATO.buffer(70).buffer(-40).difference(ACQUA).intersection(box(X0, Y0, X1, Y1))
C = O.Citta(SEME, INVILUPPO, (cx, cy), n=int(420 * FS * FS), r_centro=42, r_bordo=95, raggio=900 * FS, passi_lloyd=2)
C.vietato = [MAIDAN, ARCATE, GONFALONIERE, TERRAZZA, Point(TEMPIO).buffer(26), VALERIUS, STALLE] + CB + CARAV
MAIDAN_N, MAIDAN_S, MAIDAN_E = (cx, cy - ml / 2), (cx, cy + ml / 2), (cx + mw / 2, cy - 20)


def uscita(da, verso, rione, oltre=10):
    """Dove la strada da `da` verso `verso` esce dal rione: lì sta la dogana."""
    ln = LineString([da, verso])
    x = ln.intersection(RB[rione])
    pts = [q for g in O.linee(x) for q in g.coords] or [verso]
    q = max(pts, key=lambda t: math.dist(t, da))
    L = math.dist(da, verso)
    return (q[0] + (verso[0] - da[0]) / L * oltre, q[1] + (verso[1] - da[1]) / L * oltre)


ARCHI = {   # dogane ad arco sulle strade
    "Alba": (-692, -506), "Porto": (-707, 108),
    "Terra": uscita(MAIDAN_E, (1291, -116), "Golden Plume"),
    "Nord": uscita(MAIDAN_N, (52, -1033), "Silver Weft"),
    "Sud": uscita(MAIDAN_S, (-245, 1072), "Whispering Shadows")}
BAZ = C.via(list(BAZAR_L.coords), 9.0, "maestra")
C.via_maestra(ARCHI["Porto"], (cx - mw / 2, cy + 80), 8.0)
C.via_maestra(ARCHI["Terra"], MAIDAN_E, 8.0)
C.via_maestra(ARCHI["Nord"], MAIDAN_N, 7.5)
C.via_maestra(ARCHI["Sud"], MAIDAN_S, 7.5)
C.via_maestra((ARG.centroid.x - 80, ARG.centroid.y - 60), (cx + mw / 2, cy + 120), 6.0)
C.vie_dei_quartieri(sec=(3.6, 4.8), vicolo=2.4, p_vicolo=0.3)
C.via([(-692, -506), (-846, -465)], 8.0, "maestra")         # il ponte dell'Alba
C.via([(-707, 108), (-846, 138)], 8.0, "maestra")            # il ponte del Porto


def quale(c):
    p = Point(c)
    if NUCLEO.contains(p) or TERRAZZA.contains(p):
        return "nucleo"
    for k, g in RB.items():
        if g.contains(p):
            return k
    return None


def tipo_di(q, c):
    r = quale(c)
    if r is None:
        if q.area < 4500 and ABITATO.buffer(60).contains(Point(c)):      # ritagli piccoli: case sparse
            return {"area_min": 260, "vuoto": 0.3, "p_corte": 0.8, "area_vicolo": 5000, "corte": 4.5}
        return {"tipo": "orti"}
    if r == "nucleo":
        d = math.dist(c, (cx, cy))
        return {"area_min": 125 + 55 * min(1, d / (400 * FS)), "vuoto": 0.02, "p_corte": 0.3, "area_vicolo": 2400,
                "vicolo": 2.4, "corte": 4.0}
    tipo = RIONI[r][3]
    if tipo == "tende" and c[0] > -830 * FS:
        return {"tipo": "tende"}
    if tipo == "giardini":
        return {"area_min": 380, "vuoto": 0.35, "p_corte": 0.9, "area_vicolo": 5000, "vicolo": 2.6, "corte": 5.0}
    return {"area_min": 230, "vuoto": 0.14, "p_corte": 0.7, "area_vicolo": 3600, "vicolo": 2.4, "corte": 4.5}


C.costruisci(tipo_di, anello=0, margine_vietato=3.0)
# i lotti cadono dentro l'abitato: i ritagli dei quartieri di confine restano orti
dentro = ABITATO.buffer(4)
C.edifici = [e for e in C.edifici if dentro.contains(e.representative_point())]
MIS = C.misure()

# abitanti stimati per rione dall'area dei quartieri costruiti
ab = 0
aree = {}
for q, tipo, area_q in C.tipi:
    r = quale((q.centroid.x, q.centroid.y))
    if r is None:
        continue
    kind = "nucleo" if r == "nucleo" else RIONI[r][3]
    aree[kind] = aree.get(kind, 0) + q.intersection(ABITATO).area / 1e4
for kind, a in aree.items():
    ab += a * DENS.get(kind, 0) if kind != "tende" else a * DENS["rione"] * 0.5   # profughi esclusi
ab += ETTARI_ARG * DENS["arg"]
AB_STIMA = ab

# ---------------------------------------------------------------- arg: mura, torri, porta
porta_arg = ARG.exterior.interpolate(ARG.exterior.project(Point(ARG.centroid.x - 120, ARG.centroid.y - 80)))
PORTA_ARG = (porta_arg.x, porta_arg.y)
TORRI_ARG, L_ARG = O.cinta(ARG, [(PORTA_ARG[0], PORTA_ARG[1], 7)], passo=PASSO_TORRI_ARG, angolo_min=25)

# ---------------------------------------------------------------- fuori: strade, campi, qanat
STRADE_F = {
    "dawn_o": [(-846, -465), (-981, -542), (-1123, -568), (X0 - 20, -607)],
    "porto_o": [(-846, 138), (-981, 155), (X0 - 20, 207)],
    "terra": [ARCHI["Terra"], (X1 + 20, -129)],
    "nord": [ARCHI["Nord"], (ARCHI["Nord"][0] + 10, ARCHI["Nord"][1] - 60), (52, Y0 - 20)],
    "sud": [ARCHI["Sud"], (ARCHI["Sud"][0] - 10, ARCHI["Sud"][1] + 60), (-258, Y1 + 20)],
    "rabad_ne": [ARCHI["Terra"], (ARCHI["Terra"][0] - 20, -420), mv("Rabad Nord-Est", 640, -470)],
    "rabad_se": [(ARG.centroid.x + 60, ARG.centroid.y + 90), (560, 520), mv("Rabad Sud-Est", 470, 560)],
}
SF = {k: LineString(O.ondula(v, random.Random(i), 3)) for i, (k, v) in enumerate(STRADE_F.items())}
FINESTRA = box(X0, Y0, X1, Y1)
area_campi = (FINESTRA.difference(INVILUPPO.buffer(12)).difference(ACQUA.buffer(12))
              .difference(unary_union([l.buffer(6) for l in SF.values()])))
CAMPI = O.campi(area_campi, random.Random(SEME + 7), cella=150, striscia=(12, 26))
QANAT = [[(1162, 826), (981, 607), (826, 426), (671, 323), (542, 271)], [(1162, 491), (1033, 297), (930, 155), (852, 129)]]

# ================================================================= disegno
w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
  f'aria-label="Channathgate, pianta della città aperta: arg murato, maidan, bazar coperto, giardini, qanat, darsena sul fiume a ovest">')
w('<title>Channathgate — pianta della città (RumblingStone)</title>')
w('<desc>Pianta originale di Channathgate, città aperta sul Cannath, v3 organica, grande città. Scala in metri, nord in alto. '
  'Pianta, misure e posizioni sono canone.</desc>')
w('<defs>'
  '<pattern id="tende" width="7" height="6" patternUnits="userSpaceOnUse"><rect width="7" height="6" fill="#e4d6b4"/>'
  '<path d="M1 5 L3 1.5 L5 5 Z" fill="#b9a27a" stroke="#7a6545" stroke-width="0.25"/></pattern>'
  '<pattern id="frutteto" width="9" height="9" patternUnits="userSpaceOnUse"><rect width="9" height="9" fill="#c9d6a0"/>'
  '<circle cx="4.5" cy="4.5" r="2.6" fill="#9db77a" stroke="#6f8f52" stroke-width="0.3"/></pattern>'
  '<pattern id="scarpa" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
  '<rect width="4" height="4" fill="#d6c59a"/><line x1="0" y1="0" x2="0" y2="4" stroke="#8d6a3f" stroke-width="1.2"/></pattern>'
  '<filter id="halo"><feMorphology operator="dilate" radius="1.8" in="SourceAlpha" result="d"/><feFlood flood-color="#f6eedb"/>'
  '<feComposite in2="d" operator="in"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
  '</defs>')
w(f'<rect width="{W}" height="{H}" fill="{COL["carta"]}"/>')
x0p, y0p = P(X0, Y0)
w(f'<clipPath id="tav"><rect x="{x0p}" y="{y0p}" width="{MW}" height="{MH}"/></clipPath>')
w(f'<text x="{OX0}" y="38" {F} font-size="28" font-weight="bold" fill="#3a2a16" letter-spacing="2">CHANNATHGATE</text>')
w(f'<text x="{OX0}" y="60" {F} font-size="13.5" font-style="italic" fill="#5a4630">pianta della città aperta · Flamerule 1372 DR · '
  f'la città del Palio, sul Cannath appena uscito dal lago · la pianta del DM (channathgate-mappa.png) resta l\'illustrazione</text>')
w('<g clip-path="url(#tav)">')
D.apri()
D.area(FINESTRA, "#e8e3bf")
TINTE = ["#dcdcab", "#d4d69e", "#e2deb6", "#d0d8a8"]
for i in range(4):
    D.area([p for p, j in CAMPI if j == i], TINTE[i], "#c2b98a", 0.45)
# qanat
for q in QANAT:
    dense = LineString(O.catmull(q, 10))
    D.linea(dense, "#5f8fb0", 1.6, 'stroke-dasharray="3 6"')
    D.cerchi([(dense.interpolate(d).x, dense.interpolate(d).y, 3.4) for d in range(20, int(dense.length), 45)],
             "#efe4c8", "#6b5a3a", 1.0)
# strade di campagna
for ln in SF.values():
    D.linea(ln, COL["strada_bordo"], 10)
for ln in SF.values():
    D.linea(ln, COL["strada"], 8)
# l'abitato: fondo strada, orti fra i rioni, isolati, case
D.area(INVILUPPO, COL["strada"])
for q, tipo, area_q in C.tipi:
    if tipo == "orti":
        D.area(area_q, "url(#frutteto)", "#8a7350", 0.7)
D.area([b for b in C.isolati], COL["corte"])
r2 = random.Random(5)
D.area([v for v in C.vuoti if v.area > 40 and not NUCLEO.contains(v.representative_point()) and r2.random() < 0.35], "#b9c995")
D.area(C.cortili, "#e9dcbc")
# il campo profughi dell'Istrice
for q, tipo, area_q in C.tipi:
    if tipo == "tende":
        D.area(area_q, "url(#tende)", "#7a6545", 0.5)
D.area(C.strade_unite({"maestra"}).intersection(INVILUPPO), COL["selciato"], COL["strada_bordo"], 0.5)
D.area(C.edifici, "#c79f6b", "#7d5c35", 0.5)
# fiume e darsena
D.area(ACQUA, "#8fbcd8", "#3f7fa8", 1.6)
for k in range(5):
    D.linea(LineString([(-932, 145 + k * 22), (-890, 145 + k * 22)]), "#6b4a2a", 2.4, cap="butt")
D.area([affinity.rotate(box(bx - 9, by - 3.5, bx + 9, by + 3.5), a) for bx, by, a in ((-834, 168, 80), (-911, 214, 0), (-896, 155, 0))],
       "#7a5532", "none")
D.area(affinity.rotate(box(-833, 771, -717, 782), -12), "#6b5a44", "#3a2a16", 0.8)      # le chiuse
for a, b in (((-846, -465), (-692, -506)), ((-846, 138), (-707, 108))):          # ponti
    D.linea(LineString([a, b]), "#7a6a50", 12, cap="butt")
    D.linea(LineString([a, b]), "#d9c7a0", 9, cap="butt")
# confini dei rioni: fossi e muri d'orto, col colore della contrada
for k, g in RB.items():
    col = RIONI[k][1]
    D.linea(g.boundary, col, 2.2, 'stroke-dasharray="7 5" opacity="0.85"')
# porte di quartiere dove le vie maestre passano il confine dei rioni
pq = []
for ln, wd, t in C.vie:
    if t != "maestra":
        continue
    for g in list(RB.values()) + [NUCLEO]:
        x = ln.intersection(g.boundary)
        for p in getattr(x, "geoms", [x]):
            if isinstance(p, Point):
                pq.append((p.x, p.y))
D.cerchi([(x, y, 3.2) for x, y in pq], "#5b4a3a", "#2e2316", 0.6)
# chahar bagh: muro, quattro parti, canali in croce, padiglione
for g in CB:
    D.area(g, "#9cbf77", "#5b4a3a", 2.2)
    x0_, y0_, x1_, y1_ = g.bounds
    xm, ym = (x0_ + x1_) / 2, (y0_ + y1_) / 2
    D.area([box(a + 4, b + 4, a + (x1_ - x0_) / 2 - 4, b + (y1_ - y0_) / 2 - 4) for a in (x0_, xm) for b in (y0_, ym)], "#7fa85a")
    D.linea([LineString([(xm, y0_ + 2), (xm, y1_ - 2)]), LineString([(x0_ + 2, ym), (x1_ - 2, ym)])], "#5f9fc8", 3.2, cap="butt")
    D.area(box(xm - 6, ym - 6, xm + 6, ym + 6), "#e9dcbc", "#6b5a44", 0.8)
# caravanserragli
for g in CARAV:
    x0_, y0_, x1_, y1_ = g.bounds
    D.area(g.difference(g.buffer(-9, join_style=2)), "#b98c5a", "#4e3a24", 1.0)
    D.area(g.buffer(-9, join_style=2), "#ecdcb6", "#4e3a24", 0.6)
D.area(STALLE, "#b48a5a", "#4e3a24", 1.0)
# il maidan: arcate a due piani, la pista del Palio, il Gonfaloniere, il tempio
D.area(MAIDAN, "#efe2bf", "#6b5a44", 1.5)
D.area(ARCATE, "#b98c5a", "#4e3a24", 1.0)
pista = box(cx - mw / 2 + 14, cy - ml / 2 + 14, cx + mw / 2 - 14, cy + ml / 2 - 14).buffer(-30).buffer(30)
D.linea(pista.exterior, "#c9a25e", 9, cap="butt")
D.area(GONFALONIERE, "#b98c5a", "#4e3a24", 1.4)
D.area(GONFALONIERE.buffer(-9), "#ecdcb6", "#4e3a24", 0.6)
D.cerchi([(TEMPIO[0], TEMPIO[1], 20)], "#4f9aa0", "#2d5f63", 1.6)
# il bazar coperto: le cupole lungo la via
cup = [(BAZAR_L.interpolate(d).x, BAZAR_L.interpolate(d).y, 4.2) for d in range(6, int(BAZAR_L.length) - 4, 13)]
D.linea(BAZAR_L, "#8d6a3f", 11, cap="butt")
D.linea(BAZAR_L, "#d2ad78", 8, cap="butt")
D.cerchi(cup, "#e6c995", "#8d6a3f", 0.7)
# l'arg: terrazza alta 15 m con la scarpa, mura proprie, torri, palazzo
D.area(TERRAZZA.difference(ARG), "url(#scarpa)", "#6b5a44", 1.0)
D.area(ARG, "#dccaa0")
ac = ARG.centroid
PAL = box(ac.x - 40, ac.y - 30, ac.x + 50, ac.y + 30)
D.area(PAL, "#a77a4e", "#3a2a16", 1.4)
D.area(PAL.buffer(-11, join_style=2), "#e9dcbc", "#3a2a16", 0.6)
D.area([box(ac.x - 90, ac.y + 40, ac.x - 30, ac.y + 56), box(ac.x + 60, ac.y - 70, ac.x + 76, ac.y - 10)],
       "#b98c5a", "#3a2a16", 1.0)
D.area(box(ac.x - 20, ac.y + 44, ac.x + 50, ac.y + 82).intersection(ARG.buffer(-8)), "#9cbf77", "#5b4a3a", 1.0)
D.linea(ARG.exterior, "#3a2a16", 5.5)
D.linea(ARG.exterior, "#a88a5e", 3.5)
D.cerchi([(x, y, 4.6) for x, y in TORRI_ARG], "#8d6a3f", "#3a2a16", 1.2)
nx, ny = O.normale_fuori(ARG, *PORTA_ARG)
tx, ty = -ny, nx
D.area([affinity.rotate(box(PORTA_ARG[0] + sg * tx * 7 - 5, PORTA_ARG[1] + sg * ty * 7 - 5,
                            PORTA_ARG[0] + sg * tx * 7 + 5, PORTA_ARG[1] + sg * ty * 7 + 5), math.degrees(math.atan2(ty, tx)))
        for sg in (-1, 1)], "#7d6040", "#3a2a16", 1.2)
D.linea(LineString([(PORTA_ARG[0] - nx * 4, PORTA_ARG[1] - ny * 4), (PORTA_ARG[0] + nx * 30, PORTA_ARG[1] + ny * 30)]),
        "#d9c7a0", 6, cap="butt")
# le dogane ad arco sulle strade
for nome, (gx, gy) in ARCHI.items():
    ln = min((l for l, _, t in C.vie if t == "maestra"), key=lambda l: l.distance(Point(gx, gy)))
    s0 = ln.project(Point(gx, gy))
    a, b = ln.interpolate(max(0, s0 - 2)), ln.interpolate(min(ln.length, s0 + 2))
    ux, uy = b.x - a.x, b.y - a.y
    L = math.hypot(ux, uy) or 1
    ux, uy = ux / L, uy / L
    for sg in (-1, 1):
        px_, py_ = gx - uy * sg * 7.5, gy + ux * sg * 7.5
        D.area(affinity.rotate(box(px_ - 3.5, py_ - 3.5, px_ + 3.5, py_ + 3.5), math.degrees(math.atan2(uy, ux))),
               "#7d6040", "#3a2a16", 1.2)
    D.area(box(gx + uy * 9 - 6, gy - ux * 9 - 4, gx + uy * 9 + 6, gy - ux * 9 + 4) if False else Polygon(), "none")
# tenuta di Valerius
D.area(VALERIUS, "#8faa66", "#1a1a1a", 2.0)
D.area(box(-403, 767, -372, 788), "#5a4a3a")
D.chiudi()
w('</g>')

# ================================================================= etichette
E = O.Etichette()


def T(x, y, s, size=12, fill="#2e2316", anchor="middle", weight="normal", style="normal", spacing=0, rot=None, halo=True):
    X, Y = P(x, y)
    if rot is None:
        E.testo(X, Y, s, size + spacing * 0.8, anchor)
    tr = f' transform="rotate({rot} {X:.1f} {Y:.1f})"' if rot is not None else ""
    hl = ' filter="url(#halo)"' if halo else ""
    w(f'<text x="{X:.1f}" y="{Y:.1f}" {F} font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
      f'font-style="{style}" letter-spacing="{spacing}"{tr}{hl}>{s}</text>')


def N(x, y, k):
    X, Y = P(x, y)
    E.prendi(X - 9, Y - 9, X + 9, Y + 9, f"marker {k}")
    w(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="9" fill="#3a2a16" stroke="#f6eedb" stroke-width="1.2"/><text x="{X:.1f}" y="{Y + 3.8:.1f}" {F} '
      f'font-size="10.5" font-weight="bold" fill="#f6eedb" text-anchor="middle">{k}</text>')


LAB = [  # (x, y, rione, contrada)
    (-303, -77, "THE IRON BASTION", "la Torre"),
    (278, -194, "THE SPELL-WYRM SPIRES", "il Drago"),
    (*mv("Golden Plume", 665, -255), "THE GOLDEN PLUME", "l'Oca"),
    (*mv("Silver Weft", 0, -470), "THE SILVER WEFT", "il Bruco"),
    (*mv("Gilded Horn", -505, -200), "THE GILDED HORN", "l'Unicorno"),
    (-1078, -826, "THE QUILL-WOOD REFUGE", "l'Istrice"),
    (-1110, 491, "THE TIDAL CREST", "l'Onda"),
    (*mv("Whispering Shadows", -140, 470), "THE WHISPERING SHADOWS", "la Civetta"),
    (*mv("Rabad Nord-Est", 640, -585), "RABAD NORD-EST", "sobborgo senza contrada"),
    (*mv("Rabad Sud-Est", 470, 500), "RABAD SUD-EST", "sobborgo senza contrada"),
]
for x, y, a, b in LAB:
    rot = -90 if a == "THE GILDED HORN" else None
    big = rot is None and x > -800 * FS
    T(x, y, a, 13.5 if big else (12 if rot is None else 11), "#2a1c0e", weight="bold", spacing=2 if big else 1, rot=rot)
    if rot is None:
        T(x, y + 32, b, 12, "#4e3a24", style="italic")
    else:
        T(x + 23, y, b, 11, "#4e3a24", style="italic", rot=rot)
T(-49, -13, "THE SOVEREIGN RING", 12, "#2a1c0e", weight="bold", spacing=2, rot=-90)
T(-15, -13, "il Campo · Piazza del Guado", 10.5, "#4e3a24", style="italic", rot=-90)
T(ac.x, ac.y + 140, "ARG · The Seat", 11, "#2a1c0e", weight="bold", spacing=1.5)
T(-790, 607, "fiume Cannath", 13, "#1f5f86", style="italic", spacing=1, rot=-80)
T(-762, -852, "▲ a Cannathcross e a Rethmar", 11, "#1f5f86", style="italic", anchor="start")
T(-762, 1039, "▼ dal lago di Channathgate, ~7 km a sud", 11, "#1f5f86", style="italic", anchor="end")
T(-1343, -646, "Dawn Way ◂ Rethmar, 35 mi", 11, "#7a2418", style="italic", anchor="start")
T(X1 - 10, -128, "Dawn Way ▸ Swagdar", 11, "#7a2418", style="italic", anchor="end")
T(ARCHI["Nord"][0] + 30, Y0 + 30, "▲ strada di Cannathcross", 11, "#7a2418", style="italic", anchor="start")
T(-180, Y1 - 14, "▼ strada del lago", 11, "#7a2418", style="italic", anchor="start")
T(1110, 671, "qanat dalle Brown Hills", 11, "#2f6f96", style="italic", anchor="end", rot=-48)
for nome in ("Nord", "Sud"):
    gx, gy = ARCHI[nome]
    T(gx + 16, gy + 4, "dogana", 10, "#4e3a24", style="italic", anchor="start")

NUM = [
    (1, ac.x, ac.y, "Palazzo dei Nove (The Seat), l'arg murato sulla terrazza alta 15 m"),
    (2, cx, cy + 146, "Sovereign Ring: maidan in pendenza, pista del Palio"),
    (3, cx, cy + ml / 2 + 30, "Palazzo del Gonfaloniere, sul lato sud del Campo"),
    (4, -219, -323, f"bazar coperto ({BAZAR_L.length:.0f} m), dal Campo all'arco dell'Alba"),
    (5, ARCHI["Alba"][0] + 10, ARCHI["Alba"][1] - 24, "Arco dell'Alba: dogana sulla Dawn Way, al ponte (verso Rethmar)"),
    (6, ARCHI["Porto"][0] + 22, ARCHI["Porto"][1] + 16, "Arco del Porto, al ponte: il Golem d'Assedio della Torre"),
    (7, ARCHI["Terra"][0] - 6, ARCHI["Terra"][1] + 24, "Arco di Terra: dogana sulla Dawn Way, verso est"),
    (8, -896, 287, "Darsena della Marea Montante"),
    (9, *mv("Tidal Crest", -760, 60), "Ai Tre Remi, la locanda dell'Onda"),
    (10, *mv("Golden Plume", 600, -60), "la Piuma d'Oro, banca, e La Piuma"),
    (11, -323, 155, "Il Guanto, la locanda della Torre"),
    (12, 297, -46, "giardino e foresteria delle Guglie"),
    (13, *mv("Silver Weft", -120, -440), "La Gora, mercato nero del Bruco"),
    (14, *mv("Whispering Shadows", 120, 520), "Le Stanze Cieche"),
    (15, *mv("Gilded Horn", -505, -40), "Il Loggione, teatri dell'Unicorno"),
    (16, *mv("Quill-Wood Refuge", -800, -250), "dormitorio e campo profughi dell'Istrice"),
    (17, -581, -411, "stalle della Dawn Way, all'arco dell'Alba"),
    (18, -775, 826, "le chiuse a monte dell'Onda"),
    (19, vx_, vy_ + 40, "tenuta del Conte Valerius"),
    (20, *mv("Golden Plume", 660, 40), "chahar bagh, i giardini murati"),
    (21, 542, 297, "ab-anbar: la cisterna del qanat"),
    (22, TEMPIO[0], TEMPIO[1], "tempio sul Campo"),
]
TENDE = unary_union([a for q, t, a in C.tipi if t == "tende"])
_t = TENDE.centroid if not TENDE.is_empty else None
NUM[15] = (16, _t.x, _t.y, NUM[15][3]) if _t else NUM[15]
for k, x, y, _ in NUM:
    N(x, y, k)
w(f'<rect x="{x0p}" y="{y0p}" width="{MW}" height="{MH}" fill="none" stroke="#3a2a16" stroke-width="3"/>')

# ================================================================= pannello
px = x0p + MW + 22
py = y0p


def PT(x, y, s, size=12, fill="#2e2316", weight="normal", style="normal", anchor="start"):
    w(f'<text x="{x:.1f}" y="{y:.1f}" {F} font-size="{size}" fill="{fill}" font-weight="{weight}" font-style="{style}" text-anchor="{anchor}">{s}</text>')


rx, ry = px + 278, py + 70
w(f'<path d="M{rx} {ry-32} L{rx+9} {ry} L{rx} {ry-6} Z" fill="#3a2a16"/><path d="M{rx} {ry-32} L{rx-9} {ry} L{rx} {ry-6} Z" fill="#a08660" stroke="#3a2a16"/>'
  f'<path d="M{rx} {ry+22} L{rx+7} {ry} L{rx} {ry+4} Z" fill="#a08660" stroke="#3a2a16"/><path d="M{rx} {ry+22} L{rx-7} {ry} L{rx} {ry+4} Z" fill="#3a2a16"/>')
PT(rx, ry - 37, "N", 17, weight="bold", anchor="middle")
PT(px, py + 14, "Scala", 14, weight="bold")
sy = py + 26
for i, v in enumerate([0, 100, 200, 300, 400]):
    x = px + v * S
    if i < 4:
        w(f'<rect x="{x:.1f}" y="{sy}" width="{100*S:.1f}" height="7" fill="{"#3a2a16" if i % 2 == 0 else "#fbf6ea"}" stroke="#3a2a16"/>')
    PT(x, sy + 21, str(v), 10.5, anchor="middle")
PT(px + 400 * S + 6, sy + 8, "metri", 11, style="italic")


def mille(n):
    return f"{n:,.0f}".replace(",", ".")


yy = sy + 50
PT(px, yy, "Misure", 14, weight="bold")
for line in [f"abitato: {ABITATO.area / 1e4:.0f} ha, città aperta, senza cinta",
             f"  nucleo del bazar {NUCLEO.area / 1e4:.0f} ha · arg {ARG.area / 1e4:.1f} ha murato",
             f"  mura dell'arg {L_ARG:.0f} m, {len(TORRI_ARG)} torri + 2 alla porta",
             f"edifici: {mille(MIS['edifici'])} (lotto medio {MIS['lotto_medio']:.0f} m²)",
             f"abitanti: ~{mille(ABITANTI)} (stima per rione ~{mille(round(AB_STIMA, -2))})",
             f"  nucleo {DENS['nucleo']}/ha, rioni {DENS['rione']}/ha, giardini {DENS['giardini']}/ha",
             "Taglia: grande città della DMG 3.5, più della",
             "  Dennovar del libro (11.600): scelta del DM,",
             "  2026-10-22, perché la valle regga l'orda;",
             "  densità da Medieval Demographics Made Easy",
             "Assedio: senza cinta, reggerebbe solo l'arg",
             "  e, quartiere per quartiere, i muri dei rioni",
             "Pianta, misure e posizioni sono canone."]:
    yy += 15
    PT(px, yy, line, 10.8, style="italic" if line.startswith(("Pianta", "Taglia", "  Den", "  202", "  den", "Assedio", "  e, q")) else "normal")
yy += 24
PT(px, yy, "Luoghi", 14, weight="bold")
for k, _, _, lab in NUM:
    yy += 16
    w(f'<circle cx="{px+8}" cy="{yy-4}" r="7.5" fill="#3a2a16"/><text x="{px+8}" y="{yy-0.5}" {F} font-size="9" font-weight="bold" fill="#f6eedb" text-anchor="middle">{k}</text>')
    PT(px + 21, yy, lab, 10.2)
yy += 24
PT(px, yy, "Legenda", 14, weight="bold")
LEG = [("#c79f6b", "case a corte (nucleo, rioni)"), ("url(#frutteto)", "orti e frutteti fra i rioni"),
       ("url(#tende)", "campo profughi"), ("#9cbf77", "giardino murato (chahar bagh)"), ("#8fbcd8", "fiume, darsena"),
       ("#d4d69e", "campi irrigui"), ("url(#scarpa)", "scarpa della terrazza dell'arg")]
for fill, lab in LEG:
    yy += 18
    w(f'<rect x="{px}" y="{yy-11}" width="24" height="14" fill="{fill}" stroke="#6b5a44"/>')
    PT(px + 32, yy, lab, 10.8)
yy += 18
w(f'<rect x="{px+3}" y="{yy-9}" width="6" height="6" fill="#7d6040" stroke="#3a2a16"/><rect x="{px+15}" y="{yy-9}" width="6" height="6" fill="#7d6040" stroke="#3a2a16"/>')
PT(px + 32, yy, "dogana ad arco sulla strada", 10.8)
yy += 18
w(f'<line x1="{px}" y1="{yy-4}" x2="{px+24}" y2="{yy-4}" stroke="#6b4a1f" stroke-width="1.6" stroke-dasharray="6 4"/><circle cx="{px+12}" cy="{yy-4}" r="2.4" fill="#5b4a3a"/>')
PT(px + 32, yy, "fosso e muro del rione; porta di quartiere", 10.8)
yy += 18
w(f'<line x1="{px}" y1="{yy-4}" x2="{px+24}" y2="{yy-4}" stroke="#5f8fb0" stroke-dasharray="2 4"/><circle cx="{px+12}" cy="{yy-4}" r="2.6" fill="#efe4c8" stroke="#6b5a3a"/>')
PT(px + 32, yy, "qanat, con i pozzi", 10.8)
yy += 22
for line in ["Le posizioni dei rioni sono quelle della pianta del DM;",
             "le porte di quartiere si chiudono la notte."]:
    PT(px, yy, line, 10, style="italic")
    yy += 13
w('</svg>')
open(OUT, "w", encoding="utf-8").write("\n".join(sv.out))
print(f"abitato {ABITATO.area / 1e4:.1f} ha (nucleo {NUCLEO.area / 1e4:.1f}, arg {ARG.area / 1e4:.2f}, fattore rioni {f:.2f}); "
      f"aree per tipo {({k: round(v, 1) for k, v in aree.items()})}; abitanti stimati {AB_STIMA:.0f}")
print(f"edifici {MIS['edifici']}, lotto medio {MIS['lotto_medio']:.0f} m², impronta {MIS['impronta_ha']:.1f} ha; "
      f"arg: mura {L_ARG:.0f} m, torri {len(TORRI_ARG)} + 2 alla porta; bazar {BAZAR_L.length:.0f} m; "
      f"quartieri {len(C.quartieri)}; W {W} H {H}; yy fine {yy}")
