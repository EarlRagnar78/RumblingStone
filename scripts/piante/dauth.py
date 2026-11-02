"""Dauth v3: la città murata sullo sperone, una taglia sopra la v2 (piccola città DMG 3.5, ~7.000 abitanti),
perché regga l'urto della Mano Rossa. Stesso impianto della v2, coordinate di progetto moltiplicate per
F = sqrt(42/17): lo sperone si allarga, le quote restano. Uso: python3 scripts/genera_pianta_citta.py dauth"""
import math
import random
import sys

from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union
from shapely import affinity

from comune import COL, Svg, barra_scala, rosa, lungo
import organica as O

# ---------------------------------------------------------------- obiettivi (rivedibili)
ETTARI_DENTRO = 42.0        # piccola città: ~42 ha dentro le mura (scelta del DM, 2026-10-22)
ABITANTI = 7000             # ~167 ab./ha
PASSO_TORRI = 70.0          # torri sui fianchi ripidi (nord, est, sud)
PASSO_TORRI_OVEST = 40.0    # torri fitte sul fronte della sella
UOMINI_PER_METRO = 0.8      # regola del Burghal Hidage
SEME = 1372
F = math.sqrt(ETTARI_DENTRO / 17.0)      # fattore lineare sulla v2

OUT = sys.argv[1]
W, H = 1360, 1206
K = 1.1 / F
MX0, MY0, MX1, MY1 = -620 * F, -285 * F, 520 * F, 412 * F
OX, OY = 50 - MX0 * K, 84 - MY0 * K
s = Svg(W, H, OX, OY, K)
D = O.Disegno(s, K)
rng = random.Random(SEME)

# ---------------------------------------------------------------- la cinta
BASE = [(-400, -150), (-300, -190), (-140, -205), (40, -198), (200, -180), (330, -140), (400, -70),
        (410, 20), (350, 120), (220, 180), (40, 200), (-120, 198), (-270, 175), (-380, 110), (-415, 0)]
SC = math.sqrt(ETTARI_DENTRO * 1e4 / Polygon(BASE).area) * 1.0013    # la spezzatura delle mura toglie lo 0,26%
MURA = [(x * SC, y * SC) for x, y in BASE]
# le mura seguono il ciglio: piccole spezzature fra un angolo e l'altro
fine = []
r0 = random.Random(SEME + 1)
for i in range(len(MURA)):
    a, b = MURA[i], MURA[(i + 1) % len(MURA)]
    fine.append(a)
    L = math.dist(a, b)
    nseg = max(1, int(L / 55))
    for t in range(1, nseg):
        u = t / nseg
        nx, ny = (b[1] - a[1]) / L, -(b[0] - a[0]) / L
        j = r0.uniform(-3.5, 3.5)
        fine.append((a[0] + (b[0] - a[0]) * u + nx * j, a[1] + (b[1] - a[1]) * u + ny * j))
CINTA = Polygon(fine)
AREA = CINTA.area


def su_mura(i, t):
    a, b = MURA[i], MURA[(i + 1) % len(MURA)]
    p = Point(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    q = CINTA.exterior.interpolate(CINTA.exterior.project(p))
    return (q.x, q.y)


PORTE = {   # nome: (punto, maggiore)
    "Porta Sud": (su_mura(10, 0.4375), True),
    "Porta Nord": (su_mura(2, 0.5), True),
    "Porta Est": (su_mura(6, 0.55), False),   # ridotta a postierla: 3 porte maggiori
    "Porta Ovest": (su_mura(13, 0.45), True),
    "poterna": (su_mura(0, 0.12), False),
    "postierla nord-est": (su_mura(4, 0.6), False),
    "postierla sud-est": (su_mura(8, 0.45), False),
    "postierla sud-ovest": (su_mura(11, 0.6), False),
    "postierla nord": (su_mura(1, 0.55), False),
}
P = {k: v[0] for k, v in PORTE.items()}

# ---------------------------------------------------------------- i luoghi fissi (metri reali)
ARENA = (-24, -19)
PIAZZA = Polygon([(-107, -74), (-31, -82), (60, -77), (66, 3), (57, 28), (-31, 35), (-101, 28), (-110, -22)])
RIQ = {
    "mercato": box(-97, -141, 41, -97),
    "chiesa": box(82, -101, 163, -72),
    "chiostro": box(82, -63, 148, 6),
    "tyr": box(-192, -69, -126, -13),
    "lega": box(-82, 50, 35, 91),
    "palazzo": box(-333, -163, -245, -82),
    "vargen": box(-236, 44, -176, 101),
    "caserma_sud": box(22, 151, 110, 198),
    "caserma_nord": Polygon([(-38, -236), (16, -234), (16, -198), (-38, -198)]),
}
PIAZZETTA_SUD = Polygon([(-82, 182), (13, 176), (6, 222), (-75, 222)])
GIARDINO_PALAZZO = (-295, -35)        # il quartiere sotto il palazzo diventa giardino
ORTO_CHIOSTRO = (207, -25)            # l'orto dei semplici dell'ospedale

# ---------------------------------------------------------------- i quartieri e le vie
C = O.Citta(SEME, CINTA, ARENA, n=int(34 * F * F), r_centro=52, r_bordo=95, raggio=320 * F, passi_lloyd=2)
C.vietato = [PIAZZA, PIAZZETTA_SUD] + list(RIQ.values())
for nome in ("Porta Sud", "Porta Nord", "Porta Ovest"):
    C.via_maestra(P[nome], ARENA, larghezza=7.0)
C.via_maestra(P["Porta Est"], ARENA, larghezza=4.5)
C.via_maestra(P["poterna"], C.rete.nodi[C.rete.vicino(RIQ["palazzo"].centroid.coords[0])], larghezza=4.0)
for nome in ("postierla nord-est", "postierla sud-est", "postierla sud-ovest", "postierla nord"):
    k = C.rete.vicino(P[nome])
    C.via([P[nome], C.rete.nodi[k]], 3.5, "secondaria")
C.vie_dei_quartieri(sec=(4.0, 5.0), vicolo=2.5, p_vicolo=0.22)


def tipo_di(q, c):
    if q.contains(Point(GIARDINO_PALAZZO)):
        return {"tipo": "giardino"}
    if q.contains(Point(ORTO_CHIOSTRO)):
        return {"tipo": "orti"}
    d = math.dist(c, ARENA)
    t = min(1.0, d / (300 * F))
    return {"area_min": 105 + 90 * t, "vuoto": 0.03 + 0.05 * t, "p_corte": 0.45 + 0.3 * t,
            "area_vicolo": 2200 + 1200 * t, "vicolo": 2.4}


C.costruisci(tipo_di, anello=4.5, margine_vietato=3.0)
MIS = C.misure()

# ---------------------------------------------------------------- fuori: strade, borgo, campi
FUORI = {
    "sud": [P["Porta Sud"], (63, 283), (-63, 325), (38, 371), (-31, 412), (-35, 472), (-28, 660)],
    "stalle": [(-33, 527), (-141, 538), (-283, 553)],
    "est": [P["Porta Est"], (550, -13), (637, 28), (739, 72)],
    "nord": [P["Porta Nord"], (-57, -283), (38, -321), (-38, -365), (9, -412), (0, -472)],
    "ovest": [P["Porta Ovest"], (-550, 101), (-676, 126), (-817, 149), (-975, 176)],
}
STRADE_F = {k: LineString(O.catmull(v, 6)) for k, v in FUORI.items()}
# il fossato ovest, sulla sella
segs_ovest = LineString([MURA[12], MURA[13], MURA[14], MURA[0], MURA[1]])
FOSSO = segs_ovest.buffer(26, cap_style=2).difference(CINTA.buffer(10))
BOSCO = Polygon(O.catmull([(-904, -204), (-739, -236), (-637, -149), (-629, 0), (-676, 94), (-817, 82),
                           (-927, -31)], 6, chiuso=True))
QUERCIA = (-767, -63)
COLLINA_C = (-1195, -63)
CITTA_B = CINTA.buffer(30)
borgo = []
vietato_borgo = unary_union([CINTA.buffer(16), BOSCO] + [l.buffer(3.0) for l in STRADE_F.values()])
rb = random.Random(SEME + 5)
for nome, ln in STRADE_F.items():
    L0 = 30 if nome != "sud" else ln.project(Point(-33, 412))
    lun = {"sud": 420, "est": 160, "nord": 120, "ovest": 140, "stalle": 300}[nome]
    L0 = 8 if nome == "stalle" else L0
    p0 = 0.95 if nome in ("sud", "stalle") else 0.0       # il borgo sta solo fuori dalla Porta Sud
    borgo += O.borgo_lungo(ln, rb, inizio=L0, lunghezza=lun, larghezza=6, p0=p0, decad=260, seconda_fila=0.9,
                           vietato=vietato_borgo, gia=borgo)
STALLE = [box(x, 563, x + 17, 577) for x in range(-236, -110, 21)]
AMBITO_BORGO = unary_union([b.buffer(14) for b in borgo + STALLE])
FINESTRA = box(MX0, MY0, MX1, MY1)
COLLINE = Point(COLLINA_C).buffer(1, 32)
COLLINE = affinity.scale(COLLINE, 300 * F, 230 * F)
area_campi = (FINESTRA.difference(CINTA.buffer(45)).difference(FOSSO.buffer(6)).difference(BOSCO.buffer(8))
              .difference(AMBITO_BORGO).difference(affinity.scale(COLLINE, 0.6, 0.6))
              .difference(unary_union([l.buffer(6) for l in STRADE_F.values()])))


def verso(p):
    c = p.centroid
    if c.y > 63:                       # terrazze sul versante dolce, lungo le isoipse
        return rng.uniform(-10, 10) + (c.x / 63)
    return rng.uniform(0, 180)


CAMPI_T = O.campi(area_campi, random.Random(SEME + 7), cella=140, striscia=(9, 20), angoli=verso)
# i campi stanno sul versante dolce a sud e oltre la sella; i fianchi ripidi a nord e a est sono pascolo
DOLCE = Polygon(O.catmull([(-1006, 63), (-660, 189), (-314, 275), (0, 299), (377, 236), (629, 110), (880, 16)], 6)
                + [(880, 786), (-1006, 786)])
PASCOLO = area_campi.difference(DOLCE)
PASCOLO = PASCOLO.difference(affinity.scale(COLLINE, 1.0, 1.0))
CAMPI = [(p, j) for p, j in CAMPI_T if not PASCOLO.contains(p.representative_point())]

# ================================================================= disegno
s.add(f'<rect width="{W}" height="{H}" fill="{COL["carta"]}"/>')
fx0, fy0 = s.p(MX0, MY0)
s.add(f'<defs><clipPath id="finestra"><rect x="{fx0:.1f}" y="{fy0:.1f}" width="{(MX1 - MX0) * K:.1f}" '
      f'height="{(MY1 - MY0) * K:.1f}"/></clipPath></defs>')
s.add('<g clip-path="url(#finestra)">')
D.apri()
D.area(FINESTRA, COL["campo"])
# le colline ovest, più alte della città
for f, sc in ((1.0, "#d8d2a2"), (0.78, "#d2c995"), (0.55, "#cbbf89"), (0.32, "#c3b47d")):
    D.area(affinity.scale(COLLINE, f, f), sc, COL["isoipsa"], 0.8)
# campi
TINTE = ["#dcdcab", "#d4d69e", "#e2deb6", "#d0d8a8"]
for i in range(4):
    D.area([p for p, j in CAMPI if j == i], TINTE[i], "#c2b98a", 0.45)
D.area(PASCOLO.buffer(-2), "#d3dbad")
D.cerchi(O.alberi(PASCOLO.buffer(-4), random.Random(21), passo=26, r=(2, 3.6), p=0.35), "#a8bd84", COL["bosco2"], 0.4)
# isoipse attorno allo sperone (come nella v1: ripide a nord e a est, dolci a sud, aperte a ovest)
CX, CY = AREA_C = (CINTA.centroid.x, CINTA.centroid.y)
fianchi = lungo(list(CINTA.exterior.coords)[:-1], 6)[0]
etich_quote = []
for liv, calo in ((530, 10), (520, 20), (510, 30), (500, 40), (490, 50), (480, 60), (470, 70)):
    tratti, cur = [], []
    for x, y, _, _, _ in fianchi:
        vx, vy = x - CX, y - CY
        L = math.hypot(vx, vy)
        ct, st = vx / L, vy / L
        if ct < -0.72:
            if len(cur) > 1:
                tratti.append(cur)
            cur = []
            continue
        f = 1.7 + 3.6 * max(0.0, st) ** 2
        d = calo * f + 12
        cur.append((x + ct * d, y + st * d))
    if len(cur) > 1:
        tratti.append(cur)
    for t in tratti:
        D.linea(LineString(O.chaikin(t, 2)), COL["isoipsa"], 0.8 if liv % 50 else 1.3, 'opacity="0.85"')
    for tr in tratti:
        for x, y in tr:
            if 205 * F < x < 205 * F + 18 and y > 0 and y < MY1 - 12:
                etich_quote.append((x + 3, y + 3, f"{liv} m"))
                break
# bosco
D.area(BOSCO, "#b9c995", COL["bosco2"], 0.6)
D.cerchi(O.alberi(BOSCO, random.Random(3), passo=11, r=(4, 6.5)), COL["bosco"], COL["bosco2"], 0.6)
D.cerchi([(QUERCIA[0], QUERCIA[1], 11)], "#5f7f45", COL["bosco2"], 1.0)
D.cerchi(O.alberi(affinity.scale(COLLINE, 0.9, 0.9).difference(affinity.scale(COLLINE, 0.6, 0.6)),
                  random.Random(4), passo=18, r=(3, 5), p=0.35), COL["bosco"], COL["bosco2"], 0.5)
# strade fuori
for ln in STRADE_F.values():
    D.linea(ln, COL["strada_bordo"], 7.5)
for ln in STRADE_F.values():
    D.linea(ln, COL["strada"], 5.5)
# fossato, e il ponte della Porta Ovest
D.area(FOSSO, "#c9bb92", "#8a7350", 0.9)
for g in O.linee(STRADE_F["ovest"].intersection(FOSSO.buffer(2))):
    D.linea(g, COL["inchiostro"], 7.2, cap="butt")
    D.linea(g, "#d9c9a0", 5.6, cap="butt")
# il condotto sotterraneo dal boschetto alla cisterna della piazza
CONDOTTO = LineString([QUERCIA, (-660, -47), (-472, -57), (-251, -50), (-91, -60)])
# borgo e stalle
D.area(borgo + STALLE, COL["casa"], COL["casa_s"], 0.6)
D.area(STALLE, "#b9a37a", COL["casa_s"], 0.6)

# ---- dentro le mura
D.area(CINTA, COL["strada"])
D.area(C.isolati, COL["corte"], "none")
r2 = random.Random(9)
D.area([v for v in C.vuoti if r2.random() < 0.4 and v.area > 30], COL["giardino"])
for tipo, g, q in C.speciali:
    if tipo == "giardino":
        D.area(g, COL["giardino"], COL["pubblico_s"], 0.8)
        D.cerchi(O.alberi(g.buffer(-4), random.Random(11), passo=9, r=(2.5, 4)), COL["bosco"], COL["bosco2"], 0.5)
    elif tipo == "orti":
        D.area(g, "#c7cf96", COL["pubblico_s"], 0.8)
        D.area([p for p, _ in O.campi(g.buffer(-2), random.Random(12), cella=40, striscia=(3, 5), siepe=1)],
               "#b4c27f", "#8f9a5e", 0.4)
STRADE_M = C.strade_unite({"maestra"}).intersection(CINTA)
D.area(STRADE_M, COL["selciato"], COL["strada_bordo"], 0.6)
D.area(C.edifici, COL["casa"], COL["casa_s"], 0.55)
# piazze
D.area([PIAZZA, PIAZZETTA_SUD], COL["selciato"], COL["strada_bordo"], 0.9)
# arena del Torneo: 74 x 48 m, gradinate, sabbia, piattaforma rotante
arena = affinity.scale(Point(ARENA).buffer(1, 48), 37, 24)
D.area(arena, "#a9825a", COL["pubblico_s"], 1.0)
D.area(affinity.scale(Point(ARENA).buffer(1, 48), 26, 14), "#e6d6ae", COL["pubblico_s"], 1.0)
D.cerchi([(ARENA[0], ARENA[1], 6)], "#cdb98c", COL["inchiostro"], 1.0)
D.cerchi([(ARENA[0], ARENA[1], 1.6)], COL["marker"])


def edificio(g, fill=None, stroke=None, corte=None):
    D.area(g, fill or COL["pubblico"], stroke or COL["pubblico_s"], 1.0)
    if corte is not None:
        D.area(corte, COL["corte"], stroke or COL["pubblico_s"], 0.7)


edificio(RIQ["mercato"], corte=box(-85, -129, 28, -110))
D.cerchi([(x, -104, 0.9) for x in range(-91, 38, 6)], COL["pubblico_s"])
edificio(RIQ["chiesa"], COL["sacro"], COL["sacro_s"])
edificio(RIQ["chiostro"], COL["sacro"], COL["sacro_s"], corte=box(99, -46, 130, -11))
CIST_OSP = (115, -28)
edificio(RIQ["tyr"], COL["sacro"], COL["sacro_s"], corte=box(-176, -57, -145, -25))
edificio(RIQ["lega"], corte=box(-63, 60, -22, 82))
edificio(RIQ["palazzo"], corte=box(-311, -141, -267, -104))
D.area(box(-343, -173, -321, -151), COL["torre"], COL["inchiostro"], 0.8)
edificio(RIQ["vargen"], corte=box(-220, 60, -192, 85))
edificio(RIQ["caserma_sud"], corte=box(38, 163, 94, 185))
edificio(RIQ["caserma_nord"], corte=box(-25, -225, 3, -209))
CIST = {16: (-91, -60), 17: (-63, 204)}
D.cerchi([(x, y, 5.5) for x, y in CIST.values()], "#bcd6dd", "#3f7d99", 1.2)
D.linea(Point(CIST_OSP).buffer(9), "#3f7d99", 1.0, 'stroke-dasharray="3 2"')
D.linea(CONDOTTO, "#3f7d99", 1.4, 'stroke-dasharray="6 4"')

# ---- mura, torri, porte
porte_g = [(x, y, 6 if m else 2) for (x, y), m in PORTE.values()]
torri_n, LMURA = 0, CINTA.length
# fronte ovest (sella): torri più fitte; altrove ogni ~40 m
ovest = CINTA.intersection(segs_ovest.buffer(30))
T1, _ = O.cinta(CINTA, porte_g, passo=PASSO_TORRI, angolo_min=20)
T1 = [t for t in T1 if not ovest.contains(Point(t))]
ring = CINTA.exterior
T2 = []
for seg in O.linee(ring.intersection(segs_ovest.buffer(30))):
    n = max(1, math.ceil(seg.length / PASSO_TORRI_OVEST))
    for i in range(n + 1):
        p = seg.interpolate(seg.length * i / n)
        if all(math.dist((p.x, p.y), (gx, gy)) > r + 6 for gx, gy, r in porte_g):
            T2.append((p.x, p.y))
TORRI = T1 + T2
D.linea(CINTA.exterior, COL["inchiostro"], 4.4)
D.linea(CINTA.exterior, COL["mura"], 3.0)
tc = []
for x, y in TORRI:
    nx, ny = O.normale_fuori(CINTA, x, y)
    tc.append((x + nx * 2.5, y + ny * 2.5, 4.3))
D.cerchi(tc, COL["torre"], COL["inchiostro"], 0.8)
porte_torri = 0
for nome, ((gx, gy), magg) in PORTE.items():
    nx, ny = O.normale_fuori(CINTA, gx, gy)
    tx, ty = -ny, nx
    if magg:
        for sg in (-1, 1):
            cx, cy = gx + tx * sg * 6.8 + nx * 3, gy + ty * sg * 6.8 + ny * 3
            sq = affinity.rotate(box(cx - 4.5, cy - 4.5, cx + 4.5, cy + 4.5), math.degrees(math.atan2(ty, tx)))
            D.area(sq, COL["torre"], COL["inchiostro"], 0.9)
            porte_torri += 1
        D.linea(LineString([(gx - nx * 4, gy - ny * 4), (gx + nx * 7, gy + ny * 7)]), COL["strada"], 4.5, cap="butt")
    else:
        D.linea(LineString([(gx - nx * 3, gy - ny * 3), (gx + nx * 3, gy + ny * 3)]), COL["strada"], 1.6, cap="butt")
D.chiudi()
s.add('</g>')
N_TORRI = len(TORRI) + porte_torri

# ================================================================= etichette e luoghi
E = O.Etichette()
lbl = 'stroke="#f6ecd2" stroke-width="3" paint-order="stroke"'
lbl0 = 'stroke="#efe4c8" stroke-width="2.5" paint-order="stroke"'
for x, y, t in etich_quote:
    s.text_m(x, y, t, size=9, fill=COL["isoipsa"], extra=lbl0)


def scritta(x, y, t, size=12, **kw):
    a, b = s.p(x, y)
    E.testo(a, b, t, size, kw.get("anchor", "start"))
    s.text_m(x, y, t, size=size, **kw)


for x, y, t in ((-322, -201, "QUARTIERE ALTO"), (322, -94, "QUARTIERE MERCANTILE"), (-236, 163, "QUARTIERE SUD")):
    scritta(x, y, t, size=12, anchor="middle", weight="bold", fill="#4a2d1e",
            extra='letter-spacing="2" opacity="0.9" stroke="#f6ecd2" stroke-width="3" paint-order="stroke"')
scritta(-817, -406, "colline ovest (l'eremo di Suora Voryn)", size=12, style="italic", anchor="middle", extra=lbl)
scritta(-770, -264, "Boschetto di Nonna Faggia", size=12.5, weight="bold", anchor="middle", fill="#2f4a22", extra=lbl)
scritta(-585, -308, "sella", size=11, style="italic", anchor="middle", extra=lbl)
scritta(-594, 236, "fossato ovest", size=11.5, style="italic", anchor="middle", extra=lbl)
scritta(-13, 635, "dalla piana a sud", size=12, style="italic", extra=lbl)
scritta(726, 110, "strada a est, verso la piana", size=12, style="italic", anchor="end", extra=lbl)
scritta(22, -412, "strada a nord", size=12, style="italic", extra=lbl)
scritta(-962, 207, "verso le colline ovest", size=11.5, style="italic", extra=lbl)
scritta(519, -354, "versante ripido", size=12, style="italic", anchor="middle", fill="#7a6240", extra=lbl)
scritta(393, 472, "versante dolce, coltivato a terrazze", size=12, style="italic", anchor="middle",
        fill="#7a6240", extra=lbl)



def sul_muro(x, y, dentro=8):
    """Il punto delle mura più vicino a (x, y), spostato appena dentro: il numero sta sulla cinta."""
    q = CINTA.exterior.interpolate(CINTA.exterior.project(Point(x, y)))
    nx, ny = O.normale_fuori(CINTA, q.x, q.y)
    return q.x - nx * dentro, q.y - ny * dentro


LUOGHI = [
    (1, P["Porta Sud"][0] + 20, P["Porta Sud"][1] + 12, "Porta Sud e la piazzetta dietro la porta: la breccia (Carta A)"),
    (2, *sul_muro(189, 286), "Bastioni sud: il Razorfiend e le baliste (Carta B)"),
    (3, 115, -28, "Chiostro di Ilmater, ospedale da campo (Carta C); sotto, la cisterna grande e il cunicolo"),
    (4, *sul_muro(-560, -63), "Mura ovest: le lance di Khorn (Carta D)"),
    (5, P["poterna"][0] - 24, P["poterna"][1] - 6, "La cellula nelle mura: corpo di guardia e poterna sul fossato (Carta E)"),
    (6, ARENA[0], ARENA[1], "Piazza del Torneo: l'arena, la piattaforma rotante, l'Orbe; i dormitori sotto le gradinate"),
    (7, -28, -119, "Mercato Basso, sotto le arcate; sopra, la locanda Le Arcate"),
    (8, -159, -41, "Tempio di Tyr (l'Alta Sacerdotessa Lyala Berthand)"),
    (9, -24, 71, "Sala della Lega Mercantile: la cena delle fazioni"),
    (10, -289, -123, "Palazzo del Sovrintendente e del Consiglio"),
    (11, -206, 72, "Casa Vargen"),
    (12, 66, 174, "Caserma sud: le 150 lance, se arrivano col sigillo"),
    (13, -11, -217, "Porta Nord, con la caserma e la stalla (il sergente Verric)"),
    (14, P["Porta Est"][0] + 22, P["Porta Est"][1] - 14, "Porta Est, ridotta a postierla: la mulattiera per la piana"),
    (15, P["Porta Ovest"][0] - 26, P["Porta Ovest"][1] - 12, "Porta Ovest, verso il boschetto e le colline"),
    (16, CIST[16][0], CIST[16][1], "Cisterna della piazza"),
    (17, CIST[17][0], CIST[17][1], "Cisterna della Porta Sud"),
    (18, -393, -53, "Il condotto dal boschetto alle cisterne (sotto terra)"),
    (19, QUERCIA[0], QUERCIA[1], "La quercia madre del boschetto (Hella)"),
    (20, -236, 605, "Borgo dei carrettieri e stalle dei mercanti: Il Barcone, il magazzino della Rete Nera"),
    (21, 119, 365, "La rampa della Porta Sud, dalla piana"),
]
for nome in ("postierla nord", "postierla nord-est", "postierla sud-est", "postierla sud-ovest"):
    gx, gy = P[nome]
    nx, ny = O.normale_fuori(CINTA, gx, gy)
    LUOGHI.append((22, gx + nx * 15, gy + ny * 15, None))
for n, x, y, _ in LUOGHI:
    a, b = s.p(x, y)
    E.prendi(a - 8, b - 8, a + 8, b + 8, f"marker {n}")
    s.marker(x, y, n)
LEG = [(n, t) for n, _, _, t in LUOGHI if t] + [(22, "Postierle (quattro)")]

# ---------------------------------------------------------------- cornice e testi
s.add(f'<rect x="{fx0:.1f}" y="{fy0:.1f}" width="{(MX1 - MX0) * K:.1f}" height="{(MY1 - MY0) * K:.1f}" fill="none" '
      f'stroke="{COL["inchiostro"]}" stroke-width="2"/>')
s.text(W / 2, 34, "DAUTH — pianta della città murata", size=24, anchor="middle", weight="bold")
ABIT_T = f"{ABITANTI:,.0f}".replace(",", ".")
s.text(W / 2, 60, f"Il Torneo e l'assedio del Giorno 3 · {AREA / 1e4:.0f} ettari dentro le mura, circa {ABIT_T} abitanti · "
       f"mura di " + f"{LMURA / 1000:.2f}".replace(".", ",") + f" km, alte 12 m e spesse 3 · {N_TORRI} torri · 9 porte "
       f"(3 maggiori, la poterna della Carta E, 5 postierle)", size=13, anchor="middle",
       fill=COL["sbiadito"])
rosa(s, fx0 + (MX1 - MX0) * K - 50, fy0 + 52)
yL = fy0 + (MY1 - MY0) * K + 22
barra_scala(s, 60, yL - 6, 300, 50, "metri")
s.text(360, yL + 1, f"{MIS['edifici']} edifici dentro le mura (lotto medio {MIS['lotto_medio']:.0f} m²), "
       f"{len(borgo) + len(STALLE)} nel borgo e fuori porta", size=11, fill=COL["sbiadito"], style="italic")
righe = (len(LEG) + 1) // 2
for i, (n, t) in enumerate(LEG):
    c, r = divmod(i, righe)
    x, y = 60 + c * 650, yL + 32 + r * 15.5
    s.add(f'<circle cx="{x + 7}" cy="{y - 4}" r="7" fill="{COL["marker"]}"/>')
    s.text(x + 7, y - 0.5, str(n), size=9, anchor="middle", weight="bold", fill=COL["marker_t"])
    s.text(x + 20, y, t, size=11)
yQ = yL + 32 + righe * 15.5 + 8
quote = [
    "Il rilievo   isoipse ogni 10 m · piazza del Torneo 548 m s.l.m. · Porta Sud 530 m, +40 m sulla piana a sud",
    "Lo sperone sale verso ovest: dentro le mura ovest 556 m, la sella oltre il fossato 552 m. A nord e a est il versante cade ripido; a sud la rampa scende al borgo (490 m).",
    "Carte tattiche: A @quota 530 m (+40 m sulla piana); B @quota 544 m, il camminamento (+12 m sul piede delle mura); D @quota 556 m (+4 m sulla sella oltre il fossato).",
    f"Niente fiume: l'acqua viene dalle colline ovest per il condotto sotto il boschetto e si tiene nelle cisterne. Torri ogni {PASSO_TORRI_OVEST:.0f} m sulla sella, ogni {PASSO_TORRI:.0f} m altrove.",
    "Difensori (regola del Burghal Hidage, 0,8 uomini per metro): ~" + f"{round(LMURA * UOMINI_PER_METRO, -2):,.0f}".replace(",", ".") +
    f" per le mura; leva degli uomini abili (18%) ~{ABITANTI * 0.18:,.0f}".replace(",", ".") +
    ", più guarnigione, 300 mercenari e 150 lance se arrivano. Non basta per tutto il giro: tengono i fianchi ripidi. [INFERRED]",
    f"Taglia: piccola città della DMG 3.5, più grande del borgo del libro perché regga l'urto della Mano Rossa (scelta del DM, 2026-10-22); densità {ABITANTI / (AREA / 1e4):.0f} ab./ha da Medieval Demographics Made Easy. Pianta, vie e quote sono canone.",
]
for i, t in enumerate(quote):
    s.text(60, yQ + i * 14.5, t, size=10.5, fill=COL["inchiostro"] if i else COL["marker"],
           weight="bold" if i == 0 else "normal")
desc = ("Pianta originale di Dauth (ARC-09, P2B), città murata in altura, v3 organica, piccola città. @quota 548 m ; s.l.m., la "
        "piazza del Torneo. @dislivello +40 m ; la Porta Sud sulla piana a "
        "sud. Scala in metri, nord in alto.")
open(OUT, "w", encoding="utf-8").write(s.svg("Dauth, pianta della città", desc))
print(f"area dentro le mura {AREA / 1e4:.2f} ha; mura {LMURA:.0f} m; torri {N_TORRI} ({len(TORRI)} di cinta + "
      f"{porte_torri} alle porte); edifici {MIS['edifici']} (lotto medio {MIS['lotto_medio']:.0f} m², "
      f"impronta {MIS['impronta_ha']:.1f} ha); borgo {len(borgo)} + stalle {len(STALLE)}; quartieri {len(C.quartieri)}; "
      f"fine testo y={yQ + len(quote) * 16:.0f}")
