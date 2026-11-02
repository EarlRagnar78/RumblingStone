"""Rethmar v3: la città murata sul Cannath, una taglia sopra la v2 (grande città DMG 3.5, ~18.000 abitanti),
perché regga l'assedio dell'orda della Mano Rossa (~10.000). Stesso impianto della v2 (Brindol re-immaginata da
antariuk, guardata e non ricalcata), tutte le coordinate di progetto moltiplicate per F = sqrt(110/50).
Uso: python3 scripts/genera_pianta_citta.py rethmar (scrive la pianta canonica)"""
import math
import random
import sys

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

from comune import COL, Svg, barra_scala, rosa
import organica as O

# ---------------------------------------------------------------- obiettivi (rivedibili)
ETTARI_DENTRO = 110.0       # grande città: ~110 ha dentro le mura (scelta del DM, 2026-10-22)
DENS_DENTRO = 140           # ab./ha dentro le mura
ABITANTI_DENTRO = 15400     # 110 ha x 140
ABITANTI_TOTALI = 18000     # con i sobborghi (~25 ha) alla testa del ponte e sulla Dawn Way
PASSO_TORRI = 45.0          # mura di terra (ovest, sud, est)
PASSO_TORRI_FIUME = 60.0    # muro sul fiume, a nord
UOMINI_PER_METRO = 0.8      # regola del Burghal Hidage (una guarnigione di 4 uomini ogni 5,5 m circa)
SEME = 1373
F = math.sqrt(ETTARI_DENTRO / 50.0)      # fattore lineare sulla v2

OUT = sys.argv[1]
K = 0.8 / F
MX0, MY0, MX1, MY1 = -790 * F, -520 * F, 800 * F, 445 * F
W = int((MX1 - MX0) * K + 100)
H = 1206
OX, OY = 50 - MX0 * K, 84 - MY0 * K
s = Svg(W, H, OX, OY, K)
D = O.Disegno(s, K)
rng = random.Random(SEME)

# ---------------------------------------------------------------- la cinta (impianto in pixel della carta di riferimento)
PX = [(300, 268), (200, 318), (95, 372), (100, 470), (115, 555), (118, 700), (135, 885), (400, 925), (700, 938),
      (905, 942), (1150, 935), (1400, 920), (1462, 880), (1470, 640), (1480, 375), (1385, 165), (1250, 172),
      (1100, 195), (960, 232), (820, 285), (710, 318), (560, 305), (420, 282)]
M_PX = 0.3048 * 1000 / 385          # 1000 ft = 385 px
base = Polygon([((x - 790) * M_PX, (y - 560) * M_PX) for x, y in PX])
sc = math.sqrt(ETTARI_DENTRO * 1e4 / base.area)
c0 = base.centroid
CINTA = affinity.scale(base, sc, sc, origin=c0)
CINTA = Polygon(O.chaikin(list(CINTA.exterior.coords)[:-1], 1, chiuso=True))
_r = math.sqrt(ETTARI_DENTRO * 1e4 / CINTA.area)
CINTA = affinity.scale(CINTA, _r, _r, origin=c0)

AREA = CINTA.area


def su(px, py):
    """Un punto della carta di riferimento, portato in metri e agganciato alle mura."""
    p = Point(c0.x + ((px - 790) * M_PX - c0.x) * sc, c0.y + ((py - 560) * M_PX - c0.y) * sc)
    q = CINTA.exterior.interpolate(CINTA.exterior.project(p))
    return (q.x, q.y)


PORTE = {"Ovest": su(115, 555), "Est": su(1480, 375), "Nord": su(710, 318), "Sud": su(905, 942),
         "poterna": su(430, 284)}
# il muro sul fiume: dall'angolo nord-est all'angolo nord-ovest
NE, NO = su(1385, 165), su(300, 268)
ring = CINTA.exterior
sa, sb = ring.project(Point(NE)), ring.project(Point(NO))
MURO_FIUME = LineString([ring.interpolate(sa + (sb - sa) * t / 80) for t in range(81)])

# ---------------------------------------------------------------- il fiume, a nord, da est verso ovest
LARGH_FIUME = 74
riva = MURO_FIUME.offset_curve(-22) if MURO_FIUME.offset_curve(-22).centroid.y < MURO_FIUME.centroid.y else MURO_FIUME.offset_curve(22)
rc = list(riva.coords)
if rc[0][0] < rc[-1][0]:
    rc = rc[::-1]          # da est a ovest
rc = rc[::4] + [rc[-1]]
ASSE = [(MX1 + 60, rc[0][1] - 70)] + [(x, y - LARGH_FIUME / 2) for x, y in rc] + [(MX0 - 60, rc[-1][1] + 10)]
ASSE = O.catmull(O.chaikin(ASSE, 2), 3)
FIUME = LineString(ASSE).buffer(LARGH_FIUME / 2, cap_style=2)
FIUME = FIUME.difference(CINTA.buffer(14))
GUADI = {"Ovest": -700 * F, "Est": 735 * F}


def asse_a(x):
    best = min(ASSE, key=lambda p: abs(p[0] - x))
    return best


# ---------------------------------------------------------------- dentro: i luoghi fissi
FORO = Polygon([(-196, -258), (-107, -276), (-33, -273), (18, -237), (6, -187), (-86, -175), (-181, -196)])
FORO = FORO.intersection(CINTA.buffer(-8))
VERDE = unary_union([affinity.scale(Point(-65, 122).buffer(1, 48), 176 * F, 66 * F),
                     affinity.scale(Point(-53, 12).buffer(1, 40), 62 * F, 44 * F)])
PARCHI = [Polygon(O.catmull([(-596, 77), (-489, 59), (-389, 104), (-371, 222), (-418, 285), (-549, 276), (-608, 178)], 5, True)),
          Polygon(O.catmull([(282, -77), (371, -86), (383, -6), (291, 3)], 4, True)),
          Polygon(O.catmull([(344, 27), (448, 15), (460, 142), (356, 154)], 4, True)),
          Polygon(O.catmull([(-249, 291), (-125, 282), (-104, 356), (-237, 365)], 4, True))]
RING = O.catmull([(F * (-40 + 250 * math.cos(a)), F * (60 + 160 * math.sin(a)))
                  for a in [i * 2 * math.pi / 14 for i in range(14)]], 6, chiuso=True)
RIQ = {
    "municipio": box(-163, -169, -92, -133),
    "biblioteca": box(33, -261, 86, -217),
    "chiostro": box(86, 59, 151, 122),
    "magazzini": unary_union([box(59, 279 + i * 18, 148, 292 + i * 18) for i in range(3)]),
    "granai": unary_union([box(-418, -297 + i * 17, -335, -283 + i * 17) for i in range(3)]),
    "polveri": box(-581, -222, -504, -154),
    "arsenale": box(430, -193, 513, -128),
    "piazzetta_o": box(-771, -39, -709, 33),
    "piazzale_e": box(730, -255, 789, -175),
    "lorana": Polygon([(534, 222), (742, 208), (749, 389), (543, 400)]),
}
RIQ["piazzetta_o"] = RIQ["piazzetta_o"].intersection(CINTA)
RIQ["piazzale_e"] = RIQ["piazzale_e"].intersection(CINTA)
TEMPIO = (18, 98)
CATTEDRALE = (-133, 163)
TORRIONE = (-53, 0)
IMMERSTAL = (581, -148)

# ---------------------------------------------------------------- quartieri e vie
C = O.Citta(SEME, CINTA, (-89, -59), n=int(64 * F * F), r_centro=72, r_bordo=105, raggio=520 * F, passi_lloyd=2)
C.vietato = [FORO, VERDE] + PARCHI + [g for k, g in RIQ.items()]
foro_c = (FORO.centroid.x, FORO.centroid.y)
C.via_maestra(PORTE["Nord"], foro_c, 8.0)
C.via_maestra(PORTE["Ovest"], foro_c, 8.0)
C.via_maestra(PORTE["Est"], foro_c, 8.0)
C.via_maestra(PORTE["Sud"], (59, 237), 8.0)
C.via_maestra((59, 237), foro_c, 7.0)
C.via(RING + [RING[0]], 6.0, "maestra")           # la vecchia via ad anello
C.via([PORTE["poterna"], C.rete.nodi[C.rete.vicino(PORTE["poterna"])]], 3.0)
C.vie_dei_quartieri(sec=(4.0, 5.0), vicolo=2.6, p_vicolo=0.22)


def tipo_di(q, c):
    d = math.dist(c, foro_c)
    t = min(1.0, d / (550 * F))
    return {"area_min": 120 + 90 * t, "vuoto": 0.03 + 0.04 * t, "p_corte": 0.4 + 0.3 * t,
            "area_vicolo": 2400 + 1400 * t, "vicolo": 2.5}


C.costruisci(tipo_di, anello=5.0, margine_vietato=3.0)
MIS = C.misure()

# ---------------------------------------------------------------- fuori le mura
nx_, ny_ = O.normale_fuori(CINTA, *PORTE["Nord"])
PONTE = LineString([PORTE["Nord"], (PORTE["Nord"][0] + nx_ * 150, PORTE["Nord"][1] + ny_ * 150)])
PONTE = LineString([PORTE["Nord"], (PONTE.coords[1][0], PONTE.coords[1][1])])
# il ponte finisce sulla riva nord
fine_ponte = PONTE.intersection(FIUME)
yn = min(p[1] for g in O.linee(fine_ponte) for p in g.coords) - 4
xn = PORTE["Nord"][0] + (yn - PORTE["Nord"][1]) * nx_ / ny_
TESTA_N = (xn, yn)
STRADE_F = {
    "dawn_o": O.ondula([PORTE["Ovest"], (-890, 0), (-1023, 21), (MX0 - 20, 44)], random.Random(1), 4),
    "dawn_e": O.ondula([PORTE["Est"], (890, -222), (1038, -237), (MX1 + 20, -260)], random.Random(2), 4),
    "sud": O.ondula([PORTE["Sud"], (148, 534), (163, 593), (187, MY1 + 20)], random.Random(3), 3),
    "rhest": O.ondula([TESTA_N, (xn - 6, yn - 40), (xn - 40, yn - 110), (xn - 90, MY0 - 20)], random.Random(4), 4),
}
for nome, gx in GUADI.items():
    a = asse_a(gx)
    lato = -1 if nome == "Ovest" else 1
    STRADE_F[f"guado_{nome}_s"] = O.ondula([(gx, a[1] + 30), (gx + lato * 40, a[1] + 140),
                                            (gx + lato * 80, -59 if nome == "Ovest" else -297)], random.Random(5), 4)
    STRADE_F[f"guado_{nome}_n"] = O.ondula([(gx, a[1] - 30), (gx - 10, a[1] - 120), (gx - 30, MY0 - 20)],
                                           random.Random(6), 4)
SF = {k: LineString(v) for k, v in STRADE_F.items()}
# il borgo alla testa del ponte, sulla riva nord: un piccolo quartiere organico
BORGO_N = Polygon(O.catmull([(xn - 290, yn - 4), (xn + 250, yn - 20), (xn + 210, yn - 200), (xn + 20, yn - 320),
                             (xn - 210, yn - 260)], 5, True)).difference(FIUME.buffer(6))
CB = O.Citta(SEME + 2, BORGO_N, TESTA_N, n=30, r_centro=55, r_bordo=70, passi_lloyd=1)
CB.via([TESTA_N, (xn - 6, yn - 40), (xn - 40, yn - 110), (xn - 90, yn - 200), (xn - 130, yn - 330)], 7.0, "maestra", liscia=2)
CB.vie_dei_quartieri(sec=(4, 4.5), p_vicolo=0.1)
CB.costruisci(lambda q, c: {"area_min": 170, "vuoto": 0.12, "p_corte": 0.7}, anello=2)
vietato_b = unary_union([CINTA.buffer(18), FIUME.buffer(4), BORGO_N.buffer(4)] + [l.buffer(3.2) for l in SF.values()])
NECRO = Polygon([(222, 512), (445, 497), (460, 638), (237, 653)])
vietato_b = vietato_b.union(NECRO.buffer(6))
rb = random.Random(SEME + 9)
borgo = []
for nome, lun, p0 in (("dawn_o", 640, 1.0), ("dawn_e", 600, 1.0), ("sud", 380, 0.95)):
    borgo += O.borgo_lungo(SF[nome], rb, inizio=22, lunghezza=lun, larghezza=7, p0=p0, decad=520,
                           seconda_fila=1.0, vietato=vietato_b, gia=borgo)
SOBBORGHI = borgo + CB.edifici
AREA_SOBB = unary_union([b.buffer(14) for b in borgo] + [BORGO_N]).area
# la campagna
FINESTRA = box(MX0, MY0, MX1, MY1)
GOLENE = []
for nome, gx in GUADI.items():
    a = asse_a(gx)
    GOLENE.append(affinity.scale(Point(gx, a[1]).buffer(1, 40), 150 * F, 95 * F).difference(FIUME))
BOSCO = Polygon(O.catmull([(831, 237), (1038, 163), (MX1 + 30, 208), (MX1 + 30, MY1 + 30), (890, MY1 + 30), (801, 475)], 5, True))
area_campi = (FINESTRA.difference(CINTA.buffer(40)).difference(FIUME.buffer(8)).difference(BOSCO)
              .difference(unary_union(GOLENE)).difference(unary_union([b.buffer(14) for b in SOBBORGHI]))
              .difference(BORGO_N.buffer(10)).difference(NECRO.buffer(10))
              .difference(unary_union([l.buffer(6) for l in SF.values()])))
CAMPI = O.campi(area_campi, random.Random(SEME + 7), cella=135, striscia=(10, 22))
LORANA_FUORI = Polygon([(831, -445), (1009, -489), (1068, -341), (890, -297)]).difference(FIUME.buffer(6)).difference(
    SF["dawn_e"].buffer(8))

# ================================================================= disegno
s.add(f'<rect width="{W}" height="{H}" fill="{COL["carta"]}"/>')
fx0, fy0 = s.p(MX0, MY0)
s.add('<defs>'
      f'<clipPath id="finestra"><rect x="{fx0:.1f}" y="{fy0:.1f}" width="{(MX1 - MX0) * K:.1f}" height="{(MY1 - MY0) * K:.1f}"/></clipPath>'
      f'<pattern id="allaga" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">'
      f'<rect width="6" height="6" fill="{COL["golena"]}"/><line x1="0" y1="0" x2="0" y2="6" '
      f'stroke="{COL["acqua_s"]}" stroke-width="0.8" opacity="0.5"/></pattern>'
      '<marker id="freccia" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" '
      'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#e8f2f6"/></marker>'
      '</defs>')
s.add('<g clip-path="url(#finestra)">')
D.apri()
D.area(FINESTRA, COL["campo"])
TINTE = ["#dcdcab", "#d4d69e", "#e2deb6", "#d0d8a8"]
for i in range(4):
    D.area([p for p, j in CAMPI if j == i], TINTE[i], "#c2b98a", 0.45)
D.area(BOSCO, "#b9c995")
D.cerchi(O.alberi(BOSCO, random.Random(3), passo=13, r=(4, 7)), COL["bosco"], COL["bosco2"], 0.6)
D.area(GOLENE, "url(#allaga)", COL["acqua_s"], 0.8, 'stroke-dasharray="4 3"')
# strade fuori
for ln in SF.values():
    D.linea(ln, COL["strada_bordo"], 8.5)
for k, ln in SF.items():
    D.linea(ln, COL["strada"], 6.5 if not k.startswith("guado") else 4.5)
# fiume
D.area(FIUME, COL["acqua"], COL["acqua_s"], 1.4)
for nome, gx in GUADI.items():
    a = asse_a(gx)
    D.area(affinity.rotate(box(gx - 12, a[1] - 46, gx + 12, a[1] + 46), 8), "#d8c79a", "#8a7350", 0.8, 'opacity="0.9"')
for x in (-420 * F, 330 * F):
    a = asse_a(x)
    D.linea(LineString([(x + 40, a[1]), (x - 40, a[1])]), "#e8f2f6", 2.2, 'marker-end="url(#freccia)"')
# la riva sotto le mura: banchina
BANCHINA = CINTA.buffer(16).difference(CINTA).intersection(MURO_FIUME.buffer(17)).difference(FIUME)
D.area(BANCHINA, COL["selciato"], COL["strada_bordo"], 0.5)
# il ponte, con le statue, e la torre della riva nord
ponte = LineString([(PORTE["Nord"][0] + nx_ * 6, PORTE["Nord"][1] + ny_ * 6), TESTA_N])
D.linea(ponte, COL["inchiostro"], 11, cap="butt")
D.linea(ponte, "#cbbf9f", 9, cap="butt")
L = ponte.length
D.cerchi([(ponte.interpolate(d).x + sx * 6, ponte.interpolate(d).y, 1.8) for d in (22, 48) for sx in (-1, 1)],
         "#f3ecd8", COL["inchiostro"], 0.9)
D.area(box(xn - 9, yn - 14, xn + 9, yn + 2), COL["torre"], COL["inchiostro"], 0.8)
# il mercato del ponte sulla banchina
x0p, y0p = PORTE["Nord"]
banc = [box(x0p + dx, y0p - 18, x0p + dx + 6, y0p - 14) for dx in range(-60, 60, 9) if abs(dx + 3) > 12]
D.area(banc, COL["tenda"], COL["tenda_s"], 0.5)
# necropoli
D.area(NECRO, COL["prato"], COL["sbiadito"], 0.8, 'stroke-dasharray="3 2"')
D.area([box(232 + i * 10.5 + rng.uniform(-1.5, 1.5), 522 + j * 11 + rng.uniform(-1.5, 1.5),
            235 + i * 10.5, 524 + j * 11) for i in range(20) for j in range(12)], "#8f8574")
# il campo di Lorana fuori le mura
D.area(LORANA_FUORI, COL["prato"], COL["sbiadito"], 0.6, 'stroke-dasharray="3 2"')
tende = []
for x in range(830, 1070, 9):
    for y in range(-490, -296, 9):
        if LORANA_FUORI.contains(Point(x, y)) and rng.random() < 0.75:
            x1, y1 = x + rng.uniform(-2, 2), y + rng.uniform(-2, 2)
            tende.append(Polygon([(x1 - 2.4, y1 + 2.4), (x1, y1 - 2.4), (x1 + 2.4, y1 + 2.4)]))
D.area(tende, COL["tenda"], COL["tenda_s"], 0.5)
# sobborghi
D.area(BORGO_N, COL["strada"])
D.area(CB.isolati, COL["corte"])
D.area(SOBBORGHI, COL["casa"], COL["casa_s"], 0.5)

# ---- dentro le mura
D.area(CINTA, COL["strada"])
D.area(C.isolati, COL["corte"])
r2 = random.Random(9)
D.area([v for v in C.vuoti if r2.random() < 0.4 and v.area > 30], COL["giardino"])
D.area(C.strade_unite({"maestra"}).intersection(CINTA.buffer(-1)), COL["selciato"], COL["strada_bordo"], 0.5)
D.area(C.edifici, COL["casa"], COL["casa_s"], 0.5)
# il verde centrale e i parchi
D.area([VERDE] + PARCHI, "#b7c98f", "#7d8f55", 0.8)
alb = []
for i, g in enumerate([VERDE] + PARCHI):
    alb += O.alberi(g.buffer(-5), random.Random(30 + i), passo=17, r=(3, 5.5), p=0.45)
alb = [a for a in alb if math.dist(a[:2], TEMPIO) > 42 and math.dist(a[:2], CATTEDRALE) > 40
       and math.dist(a[:2], TORRIONE) > 32]
D.cerchi(alb, COL["bosco"], COL["bosco2"], 0.6)
# vialetti nel verde
D.linea(LineString(O.catmull([(-311, 133), (-222, 104), (-133, 154), (-30, 122), (18, 98), (133, 107), (190, 136)], 6)),
        "#e8dcc0", 3.0)
D.linea(LineString([TORRIONE, (-36, 59), TEMPIO]), "#e8dcc0", 3.0)
D.area([FORO, RIQ["piazzetta_o"], RIQ["piazzale_e"]], COL["selciato"], COL["strada_bordo"], 0.9)
fc = FORO.centroid
D.cerchi([(fc.x + dx, fc.y + dy, 2.2) for dx in (-59, 59) for dy in (-21, 21)], "#f3ecd8", COL["inchiostro"], 0.9)
D.linea(Point(fc.x, fc.y).buffer(7), COL["marker"], 0.9, 'stroke-dasharray="2 2"')


def edificio(g, fill=None, stroke=None, corte=None):
    D.area(g, fill or COL["pubblico"], stroke or COL["pubblico_s"], 1.0)
    if corte is not None:
        D.area(corte, COL["corte"], stroke or COL["pubblico_s"], 0.7)


edificio(RIQ["municipio"], corte=box(-151, -160, -116, -142))
edificio(RIQ["biblioteca"], corte=box(44, -249, 68, -228))
edificio(RIQ["chiostro"], COL["sacro"], COL["sacro_s"], corte=box(101, 74, 136, 107))
edificio(RIQ["magazzini"])
edificio(RIQ["granai"])
D.area(RIQ["polveri"], COL["selciato"], COL["strada_bordo"], 0.6)
edificio(box(-561, -202, -525, -175), "#9c8f86", "#3d3530")
edificio(RIQ["arsenale"], corte=box(448, -178, 495, -142))
# il tempio di Rethmar: pianta a croce sulla sua piazza
tx, ty = TEMPIO
D.area(Point(TEMPIO).buffer(34), COL["selciato"], COL["strada_bordo"], 0.6)
edificio(unary_union([box(tx - 22, ty - 8, tx + 22, ty + 8), box(tx - 8, ty - 20, tx + 8, ty + 20)]), COL["sacro"], COL["sacro_s"])
D.cerchi([(tx, ty, 6)], "#e9dcb6", COL["sacro_s"], 0.8)
# la cattedrale di Lathander, abside a est
cx, cy = CATTEDRALE
edificio(unary_union([box(cx - 26, cy - 10, cx + 18, cy + 10), Point(cx + 18, cy).buffer(10)]), COL["sacro"], COL["sacro_s"])
edificio(box(cx - 32, cy - 6, cx - 24, cy + 6), COL["sacro"], COL["sacro_s"])
# il torrione: mastio quadrato con quattro torrette
kx, ky = TORRIONE
edificio(box(kx - 26, ky - 22, kx + 26, ky + 22), COL["selciato"], COL["mura"])
edificio(box(kx - 14, ky - 13, kx + 14, ky + 13), COL["pubblico"], COL["inchiostro"])
D.area([box(kx + sx * 26 - 4, ky + sy * 22 - 4, kx + sx * 26 + 4, ky + sy * 22 + 4) for sx in (-1, 1) for sy in (-1, 1)],
       COL["torre"], COL["inchiostro"], 0.8)
# i rifugiati di Lorana dentro le mura
D.area(RIQ["lorana"], COL["prato"], COL["sbiadito"], 0.6)
tende = []
for x in range(534, 750, 8):
    for y in range(208, 400, 8):
        if RIQ["lorana"].buffer(-3).contains(Point(x, y)) and rng.random() < 0.8:
            x1, y1 = x + rng.uniform(-1.5, 1.5), y + rng.uniform(-1.5, 1.5)
            tende.append(Polygon([(x1 - 2.4, y1 + 2.4), (x1, y1 - 2.4), (x1 + 2.4, y1 + 2.4)]))
D.area(tende, COL["tenda"], COL["tenda_s"], 0.5)
D.cerchi([(IMMERSTAL[0], IMMERSTAL[1], 7)], "#9b4a3a", COL["inchiostro"], 1.0)

# ---- mura, torri, porte
porte_g = [(x, y, 6 if k != "poterna" else 2) for k, (x, y) in PORTE.items()]
T_terra, LMURA = O.cinta(CINTA, porte_g, passo=PASSO_TORRI, angolo_min=25)
fiume_z = MURO_FIUME.buffer(3)
T_terra = [t for t in T_terra if not fiume_z.contains(Point(t))]
T_fiume = []
n = max(1, math.ceil(MURO_FIUME.length / PASSO_TORRI_FIUME))
for i in range(1, n):
    p = MURO_FIUME.interpolate(MURO_FIUME.length * i / n)
    if all(math.dist((p.x, p.y), (gx, gy)) > r + 8 for gx, gy, r in porte_g):
        T_fiume.append((p.x, p.y))
TORRI = T_terra + T_fiume
D.linea(CINTA.exterior, COL["inchiostro"], 4.6)
D.linea(CINTA.exterior, COL["mura"], 3.0)
quadre = []
for x, y in TORRI:
    nx, ny = O.normale_fuori(CINTA, x, y)
    ang = math.degrees(math.atan2(ny, nx))
    quadre.append(affinity.rotate(box(x + nx * 2 - 3.5, y + ny * 2 - 3.5, x + nx * 2 + 3.5, y + ny * 2 + 3.5), ang))
D.area(quadre, COL["torre"], COL["inchiostro"], 0.6)
porte_torri = 0
for nome, (gx, gy) in PORTE.items():
    nx, ny = O.normale_fuori(CINTA, gx, gy)
    tx_, ty_ = -ny, nx
    if nome == "poterna":
        D.linea(LineString([(gx - nx * 3, gy - ny * 3), (gx + nx * 3, gy + ny * 3)]), COL["strada"], 1.8, cap="butt")
        continue
    ang = math.degrees(math.atan2(ty_, tx_))
    for sg in (-1, 1):
        cx_, cy_ = gx + tx_ * sg * 7.2 + nx * 2.5, gy + ty_ * sg * 7.2 + ny * 2.5
        D.area(affinity.rotate(box(cx_ - 4.5, cy_ - 5.5, cx_ + 4.5, cy_ + 5.5), ang), COL["torre"], COL["inchiostro"], 0.9)
        porte_torri += 1
    D.linea(LineString([(gx - nx * 5, gy - ny * 5), (gx + nx * 8, gy + ny * 8)]), COL["strada"], 5.0, cap="butt")
D.chiudi()
s.add('</g>')
N_TORRI = len(TORRI) + porte_torri

# ================================================================= etichette e luoghi
E = O.Etichette()
lbl = 'stroke="#f6ecd2" stroke-width="3" paint-order="stroke"'


def scritta(x, y, t, size=12, **kw):
    a, b = s.p(x, y)
    E.testo(a, b, t, size, kw.get("anchor", "start"))
    s.text_m(x, y, t, size=size, **kw)


QL = 'letter-spacing="2" opacity="0.9" stroke="#f6ecd2" stroke-width="3" paint-order="stroke"'
for x, y, t in ((-623, -89, "QUARTIERE OVEST"), (-334, -172, "QUARTIERE BASSO"), (-445, 330, "QUARTIERE NOBILE"),
                (-30, 397, "QUARTIERE ALTO"), (445, -297, "QUARTIERE DEI MESTIERI"), (371, -30, "QUARTIERE MERCANTILE"),
                (638, 163, "QUARTIERE SUD-EST")):
    scritta(x, y, t, size=12, anchor="middle", weight="bold", fill="#4a2d1e", extra=QL)
a = asse_a(-300 * F)
scritta(-680 * F, a[1] + 5, "Fiume Cannath  ⟵ da Channathgate (est), scende verso Talar (ovest)", size=13, style="italic",
        fill="#1f4f66", weight="bold", extra='stroke="#cfe6ef" stroke-width="3" paint-order="stroke"')
scritta(MX0 + 12, 77, "Dawn Way ⟶ Drellin's Ferry (50 mi)", size=11.5, style="italic", extra=lbl)
scritta(MX1 - 10, -290, "Dawn Way ⟶ Channathgate (35 mi)", size=11.5, style="italic", anchor="end", extra=lbl)
scritta(xn - 100, MY0 + 22, "Rhest Trail, verso nord", size=11.5, style="italic", anchor="end", extra=lbl)
scritta(200, MY1 - 10, "strada sud"
, size=11.5, style="italic", extra=lbl)
scritta(1023, 489, "il bosco a est", size=11.5, style="italic", anchor="middle", extra=lbl)
for nome, gx in GUADI.items():
    a = asse_a(gx)
    dy = 125 * F if nome == "Ovest" else -100 * F
    gx = gx if nome == "Ovest" else gx - 75 * F
    scritta(gx, a[1] + dy, f"Guado {nome}", size=12, weight="bold", anchor="middle", fill="#1f4f66", extra=lbl)
    scritta(gx, a[1] + dy + 20 * F, "prati allagabili (Marea Montante)", size=10.5, style="italic", anchor="middle",
            fill="#1f4f66", extra=lbl)
scritta(xn + 70, yn - 150, "borgo del ponte", size=11, style="italic", extra=lbl)

px_, py_ = PORTE["Nord"]


def sul_muro(x, y, dentro=9):
    """Il punto delle mura più vicino a (x, y), spostato appena dentro: il numero sta sulla cinta."""
    q = CINTA.exterior.interpolate(CINTA.exterior.project(Point(x, y)))
    nx, ny = O.normale_fuori(CINTA, q.x, q.y)
    return q.x - nx * dentro, q.y - ny * dentro


LUOGHI = [
    (1, PORTE["Ovest"][0] - 26, PORTE["Ovest"][1] - 16, "Porta Ovest (Cannath Gate): la Dawn Way da Drellin's Ferry. Settore A, Ondata 1; Carta 7"),
    (2, PORTE["Est"][0] + 30, PORTE["Est"][1] + 34, "Porta Est (Dawn Gate): la Dawn Way per Channathgate; i rifugiati della Carta 3"),
    (3, px_ + 22, py_ + 14, "Porta Nord, sul ponte (King's Gate): la finta della Carta 14"),
    (4, PORTE["Sud"][0] + 24, PORTE["Sud"][1] + 16, "Porta Sud"),
    (5, PORTE["poterna"][0] - 4, PORTE["poterna"][1] - 26, "Poterna (sabotaggio drow, d12 n. 8)"),
    (6, *sul_muro(-389, 472), "Mura sud: la breccia del Settore C (Ondata 3)"),
    (7, xn + 20, (yn + py_) / 2, "Ponte sul Cannath, con le statue"),
    (8, FORO.bounds[0] + 34, (FORO.bounds[1] + FORO.bounds[3]) / 2 + 4, "Mercato del Ponte, nel foro alla testa del ponte"),
    (9, xn + 22, yn - 8, "Torre del ponte, riva nord"),
    (10, GUADI["Ovest"], asse_a(GUADI["Ovest"])[1], "Guado Ovest (a valle)"),
    (11, GUADI["Est"], asse_a(GUADI["Est"])[1], "Guado Est (a monte)"),
    (12, 949, -389, "Il campo di Lorana, fuori dalle mura verso il fiume"),
    (13, fc.x - 16, fc.y + 2, "Il foro (la piazza grande, dietro la porta del ponte): il Circolo degli Otto, le quattro statue"),
    (14, -128, -151, "Municipio e Sala del Consiglio; i suoi tetti (Carta 2)"),
    (15, 59, -239, "Biblioteca municipale (Pyriel; Sertieren ospite)"),
    (16, TEMPIO[0], TEMPIO[1], "Tempio di Rethmar e piazza del tempio; sotto, le cripte (Fase 0, Carta 1)"),
    (17, 119, 90, "Chiostro-ospedale del Tempio e la sua foresteria (Carta 11)"),
    (18, CATTEDRALE[0] - 4, CATTEDRALE[1], "Cattedrale di Lathander (Tredora Occhidoro)"),
    (19, TORRIONE[0], TORRIONE[1], "Torrione cittadino: Guardia del Leone, segrete, sala del comando (Carta 14)"),
    (20, -740, -3, "Piazzetta della Porta Ovest (Carta 7)"),
    (21, 104, 311, "Magazzini della gilda di Thornwall"),
    (22, 208, 249, "La Bilancia (locanda)"),
    (23, -291, -222, "Il Ponte Nuovo, la mescita di Kellin"),
    (24, -377, -267, "Granai del quartiere basso"),
    (25, -543, -188, "Magazzino delle polveri e condotti (Carta 5)"),
    (26, 472, -160, "Arsenale e fucina cittadina (Carta 4)"),
    (27, IMMERSTAL[0] + 15, IMMERSTAL[1] - 13, "Torre di Immerstal il Rosso"),
    (28, 282, -148, "Bottega di Varis «Seta-Argento»"),
    (29, 644, 306, "I rifugiati di Lorana (circa 800)"),
    (30, 341, 575, "Necropoli, sul fianco della città (Carta 10)"),
    (31, 759, -215, "Piazzale della Porta Est (Carta 3)"),
]
for n, x, y, _ in LUOGHI:
    a, b = s.p(x, y)
    E.prendi(a - 8, b - 8, a + 8, b + 8, f"marker {n}")
    s.marker(x, y, n)

# ---------------------------------------------------------------- cornice e testi
s.add(f'<rect x="{fx0:.1f}" y="{fy0:.1f}" width="{(MX1 - MX0) * K:.1f}" height="{(MY1 - MY0) * K:.1f}" fill="none" '
      f'stroke="{COL["inchiostro"]}" stroke-width="2"/>')
s.text(W / 2, 34, "RETHMAR — pianta della città sul Cannath", size=24, anchor="middle", weight="bold")
def mille(n):
    return f"{n:,.0f}".replace(",", ".")


s.text(W / 2, 60, f"Day 42, l'assedio · {AREA / 1e4:.0f} ettari dentro le mura, circa {mille(ABITANTI_DENTRO)} abitanti "
       f"(~{mille(ABITANTI_TOTALI)} con i sobborghi) · {N_TORRI} torri su " + f"{LMURA / 1000:.1f}".replace(".", ",") +
       " km di mura · 4 porte a torri gemelle e una poterna", size=13, anchor="middle", fill=COL["sbiadito"])
rosa(s, fx0 + (MX1 - MX0) * K - 50, fy0 + (MY1 - MY0) * K - 60)
yL = fy0 + (MY1 - MY0) * K + 22
barra_scala(s, 60, yL - 6, 600, 100, "metri")
s.text(560, yL + 1, f"{MIS['edifici']} edifici dentro le mura (lotto medio {MIS['lotto_medio']:.0f} m²), "
       f"{len(SOBBORGHI)} nei sobborghi (~{AREA_SOBB / 1e4:.0f} ha) · {len(C.quartieri)} quartieri", size=11,
       fill=COL["sbiadito"], style="italic")
righe = (len(LUOGHI) + 2) // 3
cw = (W - 100) / 3
for i, (n, _, _, t) in enumerate(LUOGHI):
    c, r = divmod(i, righe)
    x, y = 60 + c * cw, yL + 32 + r * 15.5
    s.add(f'<circle cx="{x + 7:.1f}" cy="{y - 4:.1f}" r="7" fill="{COL["marker"]}"/>')
    s.text(x + 7, y - 0.5, str(n), size=9, anchor="middle", weight="bold", fill=COL["marker_t"])
    s.text(x + 20, y, t, size=10 if len(t) > 70 else 10.5)
yQ = yL + 32 + righe * 15.5 + 8
quote = [
    "Il rilievo   @quota 250 m s.l.m., il foro   ·   @dislivello +8 m sul Cannath in magra (242 m)",
    "La piana sale piano verso sud: Porta Nord 248 m, Porta Sud 252 m. Golene a 243-244 m, i guadi hanno 0,6-0,9 m d'acqua in magra; con la Marea Montante (+1,5 m) non si passano.",
    f"Mura di pietra alte 6 m e spesse 3 (Brindol). Torri ogni ~{PASSO_TORRI:.0f} m sui tre lati di terra, ogni ~{PASSO_TORRI_FIUME:.0f} m sul fiume. Vie maestre 8 m, la vecchia via ad anello 6 m, secondarie 4-5 m, vicoli 2,5 m.",
    "Difensori (regola del Burghal Hidage, " + f"{UOMINI_PER_METRO:.1f}".replace(".", ",") + f" uomini per metro): ~{mille(round(LMURA * UOMINI_PER_METRO, -2))} per " + f"{LMURA / 1000:.1f}".replace(".", ",") + " km di mura; " +
    f"leva degli uomini abili (18%) ~{mille(round(ABITANTI_TOTALI * 0.18, -2))}, più la guarnigione e gli alleati. [INFERRED — needs DM confirmation]",
    "Taglia: grande città della DMG 3.5, più grande della Brindol del libro (≈ 8.400 ab.) perché regga l'orda di ~10.000 (scelta del DM, 2026-10-22); densità 140 ab./ha da Medieval Demographics Made Easy.",
    "Impianto sulla Brindol re-immaginata da antariuk (guardata, non ricalcata); pianta originale col motore organica. Pianta, quote e posizioni dei luoghi sono canone.",
]
for i, t in enumerate(quote):
    s.text(60, yQ + i * 14.5, t, size=10.5, fill=COL["inchiostro"] if i else COL["marker"],
           weight="bold" if i == 0 else "normal")
desc = ("Pianta originale di Rethmar per l'assedio del Day 42 (ARC-09), v3 organica, grande città. @quota 250 m ; s.l.m., il foro. "
        "@dislivello +8 m ; sul Cannath in magra. Scala in metri, nord in alto.")
open(OUT, "w", encoding="utf-8").write(s.svg("Rethmar, pianta della città", desc))
print(f"area dentro le mura {AREA / 1e4:.2f} ha; mura {LMURA:.0f} m; torri {N_TORRI} ({len(T_terra)} terra + "
      f"{len(T_fiume)} fiume + {porte_torri} alle porte); edifici {MIS['edifici']} (lotto medio {MIS['lotto_medio']:.0f} m², "
      f"impronta {MIS['impronta_ha']:.1f} ha); sobborghi {len(SOBBORGHI)} edifici, ~{AREA_SOBB / 1e4:.1f} ha; "
      f"quartieri {len(C.quartieri)}; muro sul fiume {MURO_FIUME.length:.0f} m; W {W}; fine testo y={yQ + len(quote) * 14.5:.0f}")

