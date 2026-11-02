"""organica: motore per piante di città "organiche" (sul modello del Medieval Fantasy City Generator
di Watabou, rifatto da zero). Tutto in metri: 1 unità = 1 m, x verso est, y verso sud.

Pezzi:
  semi()/lloyd()/celle()      quartieri = celle di Voronoi da semi più fitti al centro, rilassate
  Rete                        il grafo dei bordi dei quartieri: le vie ci corrono sopra
  Citta                       quartieri, vie maestre (porta -> piazza), vie secondarie, vicoli, lotti
  lotti()                     bisezione ricorsiva lungo il lato più lungo, con vicoli e corti vuote
  cinta()                     mura con torri ogni ~40 m e varchi alle porte
  borgo_lungo()               sobborghi a nastro lungo le strade fuori porta, che si diradano
  campi()                     campi a strisce in celle di Voronoi grandi
  Disegno                     scrive i path SVG in metri dentro un <g transform> (scala reale)
Deterministico: ogni passo prende un random.Random con seme fisso.
"""
import heapq
import math
import random

import numpy as np
from scipy.spatial import Voronoi
from shapely import affinity
from shapely.geometry import (LineString, MultiPolygon, Point, Polygon, GeometryCollection, box,
                              MultiLineString)
from shapely.ops import split, unary_union
from shapely.prepared import prep
from shapely.strtree import STRtree


# ------------------------------------------------------------------ geometria di base
def poligoni(g, minimo=0.0):
    """Appiattisce una geometria in una lista di Polygon non vuoti."""
    if g is None or g.is_empty:
        return []
    if isinstance(g, Polygon):
        return [g] if g.area > minimo else []
    if hasattr(g, "geoms"):
        out = []
        for h in g.geoms:
            out += poligoni(h, minimo)
        return out
    return []


def linee(g):
    if g is None or g.is_empty:
        return []
    if isinstance(g, LineString):
        return [g]
    if hasattr(g, "geoms"):
        out = []
        for h in g.geoms:
            out += linee(h)
        return out
    return []


def chaikin(pts, it=2, chiuso=False):
    pts = [tuple(p) for p in pts]
    for _ in range(it):
        out = [] if chiuso else [pts[0]]
        n = len(pts)
        rng_ = range(n) if chiuso else range(n - 1)
        for i in rng_:
            a, b = pts[i], pts[(i + 1) % n]
            out.append((a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25))
            out.append((a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75))
        if not chiuso:
            out.append(pts[-1])
        pts = out
    return pts


def catmull(pts, n=8, chiuso=False):
    """Spline di Catmull-Rom che passa per i punti dati."""
    P = [tuple(p) for p in pts]
    if chiuso:
        P = P[-1:] + P + P[:2]
    else:
        P = [P[0]] + P + [P[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    if not chiuso:
        out.append(P[-2])
    return out


def ondula(pts, rng, ampiezza=6.0, passo=25.0):
    """Ricampiona una polilinea e la fa ondeggiare un poco di lato (strade di campagna)."""
    L = LineString(pts)
    n = max(2, int(L.length / passo))
    out = []
    fase = rng.uniform(0, 6.28)
    for i in range(n + 1):
        d = L.length * i / n
        p = L.interpolate(d)
        q = L.interpolate(min(L.length, d + 1))
        r = L.interpolate(max(0, d - 1))
        tx, ty = q.x - r.x, q.y - r.y
        tl = math.hypot(tx, ty) or 1
        w = 0 if i in (0, n) else ampiezza * (math.sin(fase + i * 1.3) * 0.6 + rng.uniform(-0.4, 0.4))
        out.append((p.x - ty / tl * w, p.y + tx / tl * w))
    return catmull(out, 6)


def lato_corto(p):
    r = p.minimum_rotated_rectangle
    c = list(r.exterior.coords)
    if len(c) < 4:
        return 0.0
    return min(math.dist(c[0], c[1]), math.dist(c[1], c[2]))


# ------------------------------------------------------------------ semi e Voronoi
def semi(regione, rng, n, r_centro, r_bordo, centro=None, raggio=None, fissi=(), tentativi=None):
    """Semi alla Poisson con raggio variabile: più fitti (r_centro) al centro, più radi (r_bordo) fuori."""
    minx, miny, maxx, maxy = regione.bounds
    c = centro or (regione.centroid.x, regione.centroid.y)
    R = raggio or max(maxx - minx, maxy - miny) / 2
    pr = prep(regione)
    pts = [tuple(p) for p in fissi]
    tentativi = tentativi or n * 400

    def r_di(x, y):
        t = min(1.0, math.dist((x, y), c) / R)
        return r_centro + (r_bordo - r_centro) * t

    arr = np.array(pts) if pts else np.zeros((0, 2))
    for _ in range(tentativi):
        if len(pts) >= n:
            break
        x, y = rng.uniform(minx, maxx), rng.uniform(miny, maxy)
        if not pr.contains(Point(x, y)):
            continue
        r = r_di(x, y)
        if len(arr) and np.min(np.hypot(arr[:, 0] - x, arr[:, 1] - y)) < r:
            continue
        pts.append((x, y))
        arr = np.array(pts)
    return pts


def celle(pts, regione):
    """Celle di Voronoi dei semi, tagliate sulla regione (None se la cella cade fuori)."""
    arr = np.array(pts, dtype=float)
    minx, miny, maxx, maxy = regione.bounds
    D = 10 * max(maxx - minx, maxy - miny) + 1000
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    finti = np.array([[cx - D, cy - D], [cx + D, cy - D], [cx + D, cy + D], [cx - D, cy + D]])
    vor = Voronoi(np.vstack([arr, finti]))
    out = []
    for i in range(len(pts)):
        reg = vor.regions[vor.point_region[i]]
        if not reg or -1 in reg:
            out.append(None)
            continue
        poly = Polygon(vor.vertices[reg]).intersection(regione)
        out.append(poly if not poly.is_empty and poly.area > 1 else None)
    return out


def lloyd(pts, regione, passi=2, fissi=0):
    """Rilassamento di Lloyd; i primi `fissi` semi non si muovono."""
    pts = list(pts)
    for _ in range(passi):
        cc = celle(pts, regione)
        pts = [p if (i < fissi or c is None) else (c.centroid.x, c.centroid.y)
               for i, (p, c) in enumerate(zip(pts, cc))]
    return pts


# ------------------------------------------------------------------ il grafo dei bordi
def chiave(p):
    return (round(p[0], 1), round(p[1], 1))


class Rete:
    """Grafo dei bordi delle celle. I nodi sono i vertici di Voronoi; gli archi sui confini della
    regione (le mura) sono marcati come `bordo`."""

    def __init__(self, polys, regione):
        self.nodi = {}
        self.adj = {}
        self.uso = {}
        bordo_reg = regione.boundary
        for poly in polys:
            for p in poligoni(poly):
                c = list(p.exterior.coords)
                for a, b in zip(c[:-1], c[1:]):
                    ka, kb = chiave(a), chiave(b)
                    if ka == kb:
                        continue
                    self.nodi[ka], self.nodi[kb] = a, b
                    self.adj.setdefault(ka, set()).add(kb)
                    self.adj.setdefault(kb, set()).add(ka)
                    e = frozenset((ka, kb))
                    self.uso[e] = self.uso.get(e, 0) + 1
        self.bordo = set()
        for e in self.uso:
            ka, kb = tuple(e)
            m = Point((ka[0] + kb[0]) / 2, (ka[1] + kb[1]) / 2)
            if m.distance(bordo_reg) < 0.5:
                self.bordo.add(e)
        self.preferiti = set()

    def interni(self):
        return [e for e in self.uso if e not in self.bordo]

    def componente(self, k):
        vis, st = {k}, [k]
        while st:
            u = st.pop()
            for v in self.adj[u]:
                if v not in vis:
                    vis.add(v)
                    st.append(v)
        return vis

    def vicino(self, p, solo_interni=True, escludi=None, fra=None):
        best, bd = None, 1e18
        for k, q in self.nodi.items():
            if fra is not None and k not in fra:
                continue
            if solo_interni and all(frozenset((k, j)) in self.bordo for j in self.adj[k]):
                continue
            if escludi is not None and escludi.contains(Point(q)):
                continue
            d = math.dist(p, q)
            if d < bd:
                best, bd = k, d
        return best

    def cammino(self, a, b, pena_bordo=6.0, sconto=0.55):
        dist = {a: 0.0}
        prev = {}
        h = [(0.0, a)]
        while h:
            d, u = heapq.heappop(h)
            if u == b:
                break
            if d > dist.get(u, 1e18):
                continue
            for v in self.adj[u]:
                e = frozenset((u, v))
                w = math.dist(self.nodi[u], self.nodi[v])
                if e in self.bordo:
                    w *= pena_bordo
                if e in self.preferiti:
                    w *= sconto
                nd = d + w
                if nd < dist.get(v, 1e18):
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(h, (nd, v))
        if b not in dist:
            return None
        path = [b]
        while path[-1] != a:
            path.append(prev[path[-1]])
        path.reverse()
        for u, v in zip(path[:-1], path[1:]):
            self.preferiti.add(frozenset((u, v)))
        return path


# ------------------------------------------------------------------ i lotti
def lotti(blocco, rng, area_min, caos=0.45, var=0.6, vuoto=0.05, vicolo=2.4, area_vicolo=2600,
          p_corte=0.55):
    """Divide un isolato in lotti alla Watabou: taglio perpendicolare al lato più lungo, a un punto
    a caso verso la metà e con un piccolo angolo; i pezzi grandi tagliati lasciando un vicolo.
    Ritorna (edifici, vuoti): i lotti interni che non toccano la strada restano spesso corti/orti."""
    edifici, vuoti = [], []
    contorno = blocco.exterior

    def taglia(p, con_vicolo):
        c = list(p.exterior.coords)
        i = max(range(len(c) - 1), key=lambda j: math.dist(c[j], c[j + 1]))
        a, b = c[i], c[i + 1]
        L = math.dist(a, b)
        if L < 1e-6:
            return [p]
        t = 0.5 + (rng.random() - 0.5) * 0.8 * caos
        ang = (rng.random() - 0.5) * (math.pi / 6) * caos if p.area > area_min * 4 else 0.0
        cx, cy = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        nx, ny = -dy, dx
        ca, sa = math.cos(ang), math.sin(ang)
        nx, ny = nx * ca - ny * sa, nx * sa + ny * ca
        D = 4 * (p.length + 10)
        ln = LineString([(cx - nx * D, cy - ny * D), (cx + nx * D, cy + ny * D)])
        try:
            if con_vicolo:
                parti = poligoni(p.difference(ln.buffer(vicolo / 2, cap_style=2)), 0.5)
            else:
                parti = poligoni(split(p, ln), 0.5)
        except Exception:
            return [p]
        return parti

    def ric(p, prof=0):
        if prof > 30:
            edifici.append(p)
            return
        alley = p.area > area_vicolo * (0.6 + rng.random() * 0.8)
        parti = taglia(p, alley)
        if len(parti) < 2:
            edifici.append(p)
            return
        for h in parti:
            soglia = area_min * 2 ** (4 * var * (rng.random() - 0.5))
            if h.area < soglia:
                if h.area < 12 or lato_corto(h) < 3.0:
                    vuoti.append(h)
                elif rng.random() < vuoto:
                    vuoti.append(h)
                else:
                    edifici.append(h)
            else:
                ric(h, prof + 1)

    if blocco.area < area_min * 0.5 or lato_corto(blocco) < 4:
        if blocco.area > 25 and lato_corto(blocco) >= 4:
            edifici.append(blocco)
        return edifici, vuoti
    ric(blocco)
    # i lotti chiusi nel cuore dell'isolato diventano spesso corti e orti
    fuori = []
    tenuti = []
    cb = contorno.buffer(0.6)
    for e in edifici:
        if not e.intersects(cb) and rng.random() < p_corte:
            fuori.append(e)
        else:
            tenuti.append(e)
    return tenuti, vuoti + fuori


def casa_a_corte(lotto, prof=4.0, minimo=24):
    """Casa a corte (persiana): il lotto meno il cortile centrale."""
    dentro = lotto.buffer(-prof, join_style=2)
    if dentro.is_empty or dentro.area < minimo:
        return lotto, None
    return lotto.difference(dentro), dentro


# ------------------------------------------------------------------ la città
class Citta:
    """Quartieri di Voronoi dentro `regione` con vie maestre, secondarie, vicoli e lotti.

    regione   : Polygon/MultiPolygon dell'abitato (dentro le mura, o l'insieme dei rioni)
    centro    : (x, y) del cuore, verso cui i quartieri si infittiscono
    n         : numero di quartieri cercati
    r_centro, r_bordo : distanza minima fra i semi al centro e al bordo (m)
    """

    def __init__(self, seme, regione, centro, n, r_centro, r_bordo, raggio=None, passi_lloyd=2,
                 fissi=()):
        self.rng = random.Random(seme)
        self.regione = regione
        self.centro = centro
        pts = semi(regione, self.rng, n, r_centro, r_bordo, centro, raggio, fissi)
        pts = lloyd(pts, regione, passi_lloyd, fissi=len(fissi))
        self.semi = pts
        cc = celle(pts, regione)
        self.quartieri = [c for c in cc if c is not None]
        self.rete = Rete(self.quartieri, regione)
        self.vie = []          # (LineString, larghezza, tipo)
        self.vietato = []      # geometrie dove non si costruisce (piazze, edifici speciali...)
        self.vuote = []        # vie maestre già tracciate, per i calcoli

    # -------------------------------------------------- vie maestre
    def via_maestra(self, porta, meta, larghezza=7.0, liscia=2, dentro=None, raggio_porta=70):
        """Dalla porta al nodo più vicino alla meta, lungo i bordi dei quartieri, poi lisciata."""
        b = self.rete.vicino(meta)
        a = self.rete.vicino(porta, fra=self.rete.componente(b))
        path = self.rete.cammino(a, b)
        pts = [porta] + [self.rete.nodi[k] for k in path] + [meta]
        # togli i nodi troppo vicini alla porta che farebbero gomito
        pulita = [pts[0]]
        for q in pts[1:]:
            if math.dist(q, pulita[-1]) > 4:
                pulita.append(q)
        pts = chaikin(pulita, liscia)
        ln = LineString(pts)
        self.vie.append((ln, larghezza, "maestra"))
        return ln

    def via(self, pts, larghezza, tipo="secondaria", liscia=0):
        if liscia:
            pts = chaikin(pts, liscia)
        ln = LineString(pts)
        self.vie.append((ln, larghezza, tipo))
        return ln

    # -------------------------------------------------- vie sui bordi dei quartieri
    def vie_dei_quartieri(self, sec=(4.0, 5.0), vicolo=2.6, p_vicolo=0.25, centrale=None):
        """Ogni bordo interno fra due quartieri è una via: secondaria (4-5 m) o vicolo (2-3 m)."""
        rng = self.rng
        c = self.centro
        Rm = max(1.0, max(math.dist(c, q) for q in self.rete.nodi.values()))
        for e in self.rete.interni():
            ka, kb = tuple(e)
            a, b = self.rete.nodi[ka], self.rete.nodi[kb]
            if e in self.rete.preferiti:
                continue
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            t = math.dist(m, c) / Rm
            if rng.random() < p_vicolo * (0.5 + t):
                w, tipo = vicolo, "vicolo"
            else:
                w, tipo = sec[1] - (sec[1] - sec[0]) * t, "secondaria"
            self.vie.append((LineString([a, b]), w, tipo))

    def strade_unite(self, tipi=None):
        g = [ln.buffer(w / 2, cap_style=1, join_style=1, quad_segs=4)
             for ln, w, t in self.vie if tipi is None or t in tipi]
        return unary_union(g) if g else Polygon()

    # -------------------------------------------------- i lotti, quartiere per quartiere
    def costruisci(self, tipo_di, anello=4.0, margine_vietato=2.5):
        """tipo_di(quartiere, centroide) -> dict con 'tipo' ('case', 'giardino', 'orti', 'vuoto',
        'tende', 'campo', 'piazza') e i parametri di lotti(). Ritorna una lista di strati."""
        strade = self.strade_unite()
        vietato = unary_union([g.buffer(margine_vietato) for g in self.vietato]) if self.vietato else Polygon()
        dentro = self.regione.buffer(-anello, join_style=2) if anello else self.regione
        self.edifici, self.cortili, self.isolati, self.speciali = [], [], [], []
        self.vuoti = []
        self.tipi = []
        for q in self.quartieri:
            cen = (q.centroid.x, q.centroid.y)
            par = dict(tipo_di(q, cen) or {})
            tipo = par.pop("tipo", "case")
            corte = par.pop("corte", None)
            area_q = q.difference(strade).difference(vietato).intersection(dentro)
            self.tipi.append((q, tipo, area_q))
            if tipo != "case":
                self.speciali.append((tipo, area_q, q))
                continue
            for blocco in poligoni(area_q, 20):
                blocco = blocco.buffer(0)
                self.isolati.append(blocco)
                ed, vu = lotti(blocco, self.rng, **par)
                self.vuoti += vu
                for e in ed:
                    if corte:
                        e2, cort = casa_a_corte(e, corte)
                        self.edifici.append(e2)
                        if cort is not None:
                            self.cortili.append(cort)
                    else:
                        self.edifici.append(e)
        return self

    def misure(self):
        n = len(self.edifici)
        lot_area = [e.area for e in self.edifici]
        return {
            "edifici": n,
            "lotto_medio": (sum(lot_area) / n) if n else 0,
            "impronta_ha": sum(lot_area) / 1e4,
        }


# ------------------------------------------------------------------ mura e torri
def cinta(contorno, porte, passo=40.0, raggio_porta=9.0, angolo_min=12):
    """Torri sugli angoli della cinta (svolta > angolo_min gradi) e intermedie a passo uguale
    non oltre `passo`. porte: lista di (x, y, raggio_varco). Ritorna (torri, lunghezza)."""
    c = list(contorno.exterior.coords)[:-1]
    n = len(c)
    angoli = []
    for i in range(n):
        a, b, d = c[i - 1], c[i], c[(i + 1) % n]
        v1 = (b[0] - a[0], b[1] - a[1])
        v2 = (d[0] - b[0], d[1] - b[1])
        ang = abs(math.degrees(math.atan2(v1[0] * v2[1] - v1[1] * v2[0], v1[0] * v2[0] + v1[1] * v2[1])))
        if ang >= angolo_min:
            angoli.append(i)
    if not angoli:
        angoli = list(range(0, n, max(1, n // 8)))
    ring = LineString(c + [c[0]])
    posiz = [ring.project(Point(c[i])) for i in angoli]
    L = ring.length
    pts = []
    for j in range(len(posiz)):
        s0 = posiz[j]
        s1 = posiz[(j + 1) % len(posiz)]
        if s1 <= s0:
            s1 += L
        k = max(1, math.ceil((s1 - s0) / passo))
        for t in range(k):
            pts.append((s0 + (s1 - s0) * t / k) % L)
    torri = []
    pts = sorted(set(round(x, 2) for x in pts))
    tenuti = []
    for sp in pts:
        if tenuti and sp - tenuti[-1] < passo * 0.45:
            continue
        tenuti.append(sp)
    if len(tenuti) > 1 and (tenuti[0] + L - tenuti[-1]) < passo * 0.45:
        tenuti.pop()
    for sp in tenuti:
        p = ring.interpolate(sp)
        if any(math.dist((p.x, p.y), (gx, gy)) < r + raggio_porta * 0.6 for gx, gy, r in porte):
            continue
        torri.append((p.x, p.y))
    return torri, L


def normale_fuori(poly, x, y):
    """Normale uscente dal contorno nel punto più vicino a (x, y)."""
    ring = poly.exterior
    s = ring.project(Point(x, y))
    a = ring.interpolate(max(0, s - 2))
    b = ring.interpolate(min(ring.length, s + 2))
    tx, ty = b.x - a.x, b.y - a.y
    L = math.hypot(tx, ty) or 1
    nx, ny = ty / L, -tx / L
    if poly.contains(Point(x + nx * 3, y + ny * 3)):
        nx, ny = -nx, -ny
    return nx, ny


# ------------------------------------------------------------------ i borghi lungo le strade
def borgo_lungo(strada, rng, inizio=10.0, lunghezza=300.0, larghezza=7.0, p0=0.9, decad=150.0,
                fronte=(8, 14), profondita=(9, 16), seconda_fila=0.25, vietato=None, gia=None):
    """Case a nastro sui due lati di una strada fuori porta; si diradano con la distanza."""
    ln = strada if isinstance(strada, LineString) else LineString(strada)
    vt = prep(vietato) if vietato is not None and not vietato.is_empty else None
    case = []
    occ = list(gia or [])
    tree_items = []

    def libero(p):
        if vt is not None and vt.intersects(p):
            return False
        for q in occ[-80:]:
            if q.intersects(p):
                return False
        for q in tree_items:
            if q.distance(p) < 0.01 and q.intersects(p):
                return False
        return True

    for lato in (1, -1):
        s = inizio + rng.uniform(0, 4)
        fine = min(ln.length, inizio + lunghezza)
        while s < fine:
            f = rng.uniform(*fronte)
            p = ln.interpolate(s)
            q = ln.interpolate(min(ln.length, s + 1))
            tx, ty = q.x - p.x, q.y - p.y
            tl = math.hypot(tx, ty) or 1
            tx, ty = tx / tl, ty / tl
            nx, ny = -ty * lato, tx * lato
            prob = p0 * math.exp(-(s - inizio) / decad)
            if rng.random() < prob:
                d = rng.uniform(*profondita)
                arretra = larghezza / 2 + rng.uniform(0.5, 2.5)
                righe = [arretra]
                if rng.random() < seconda_fila * prob:
                    righe.append(arretra + d + rng.uniform(4, 12))
                for r0 in righe:
                    x0, y0 = p.x + nx * r0, p.y + ny * r0
                    poly = Polygon([(x0, y0), (x0 + tx * f, y0 + ty * f),
                                    (x0 + tx * f + nx * d, y0 + ty * f + ny * d), (x0 + nx * d, y0 + ny * d)])
                    poly = affinity.rotate(poly, rng.uniform(-4, 4), origin="centroid")
                    if libero(poly.buffer(0.8)):
                        # a volte la casa ha un annesso dietro
                        case.append(poly)
                        occ.append(poly)
                        if rng.random() < 0.35:
                            ann = Polygon([(x0 + nx * (d + 0.0), y0 + ny * (d + 0.0)),
                                           (x0 + nx * (d + 0.0) + tx * f * 0.5, y0 + ny * (d + 0.0) + ty * f * 0.5),
                                           (x0 + nx * (d + 5) + tx * f * 0.5, y0 + ny * (d + 5) + ty * f * 0.5),
                                           (x0 + nx * (d + 5), y0 + ny * (d + 5))])
                            if libero(ann.buffer(0.3)):
                                case.append(ann)
                                occ.append(ann)
            s += f + rng.uniform(0.0, 3.0) + (0 if rng.random() < prob else rng.uniform(5, 25))
    return case


# ------------------------------------------------------------------ i campi
def campi(regione, rng, cella=170.0, striscia=(10.0, 24.0), siepe=2.0, angoli=None):
    """Campi a strisce: celle di Voronoi grandi, ognuna arata in un verso. Ritorna [(poly, indice)]."""
    if regione.is_empty:
        return []
    pts = semi(regione, rng, 4000, cella, cella, tentativi=20000)
    if len(pts) < 2:
        return [(regione, 0)]
    cc = celle(pts, regione)
    out = []
    for c in cc:
        if c is None:
            continue
        for p in poligoni(c.buffer(-siepe, join_style=2), 30):
            if angoli:
                ang = angoli(p)
            else:
                ang = rng.uniform(0, 180)
            kind = rng.random()
            if kind < 0.16:      # prato o pascolo, senza strisce
                out.append((p, 3))
                continue
            r = affinity.rotate(p, -ang, origin=(0, 0))
            minx, miny, maxx, maxy = r.bounds
            y = miny
            j = 0
            base = rng.randrange(3)
            while y < maxy:
                w = rng.uniform(*striscia)
                st = box(minx - 1, y, maxx + 1, y + w).intersection(r)
                for s in poligoni(st, 2):
                    out.append((affinity.rotate(s, ang, origin=(0, 0)), (base + j) % 3))
                y += w
                j += 1 + (1 if rng.random() < 0.3 else 0)
    return out


def alberi(regione, rng, passo=9.0, r=(3.0, 5.5), p=0.85):
    """Chiome sparse in una regione: [(x, y, r)]."""
    out = []
    minx, miny, maxx, maxy = regione.bounds
    pr = prep(regione)
    y = miny
    while y < maxy:
        x = minx + rng.uniform(0, passo)
        while x < maxx:
            px, py = x + rng.uniform(-passo / 3, passo / 3), y + rng.uniform(-passo / 3, passo / 3)
            if rng.random() < p and pr.contains(Point(px, py)):
                out.append((px, py, rng.uniform(*r)))
            x += passo
        y += passo * 0.87
    return out


# ------------------------------------------------------------------ il disegno
def d_poly(p, prec=1):
    f = f"{{:.{prec}f}}"
    out = []
    for ring in [p.exterior] + list(p.interiors):
        c = list(ring.coords)[:-1]
        if len(c) < 3:
            continue
        out.append("M" + " ".join(f.format(x) + "," + f.format(y) for x, y in c) + "Z")
    return "".join(out)


def d_line(l, prec=1):
    f = f"{{:.{prec}f}}"
    return "M" + " ".join(f.format(x) + "," + f.format(y) for x, y in l.coords)


def d_geom(g, prec=1):
    if isinstance(g, (list, tuple)):
        return "".join(d_geom(h, prec) for h in g)
    if g is None or g.is_empty:
        return ""
    if isinstance(g, Polygon):
        return d_poly(g, prec)
    if isinstance(g, LineString):
        return d_line(g, prec)
    if hasattr(g, "geoms"):
        return "".join(d_geom(h, prec) for h in g.geoms)
    return ""


class Disegno:
    """Strati SVG in metri. Ogni chiamata aggiunge un <path> (molti poligoni in un solo path)."""

    def __init__(self, svg, k):
        self.s = svg          # comune.Svg: ha ox, oy, k
        self.k = k

    def apri(self, clip=None):
        c = f' clip-path="url(#{clip})"' if clip else ""
        self.s.add(f'<g transform="translate({self.s.ox:.2f},{self.s.oy:.2f}) scale({self.k})"{c}>')

    def chiudi(self):
        self.s.add('</g>')

    def px(self, w):
        """Spessore di tratto: da px a metri."""
        return w / self.k

    def area(self, g, fill, stroke="none", sw_px=0.0, extra="", prec=1):
        d = d_geom(g, prec)
        if d:
            self.s.add(f'<path d="{d}" fill="{fill}" fill-rule="evenodd" stroke="{stroke}" '
                       f'stroke-width="{sw_px / self.k:.3f}" stroke-linejoin="round" {extra}/>')

    def linea(self, g, stroke, w_m, extra="", cap="round", prec=1):
        d = d_geom(g, prec)
        if d:
            self.s.add(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{w_m:.2f}" '
                       f'stroke-linejoin="round" stroke-linecap="{cap}" {extra}/>')

    def cerchi(self, pts, fill, stroke="none", sw_px=0.0, extra=""):
        """pts: [(x, y, r)] in metri, uniti in un solo path."""
        parts = []
        for x, y, r in pts:
            parts.append(f"M{x - r:.1f},{y:.1f}a{r:.1f},{r:.1f} 0 1,0 {2 * r:.1f},0a{r:.1f},{r:.1f} 0 1,0 {-2 * r:.1f},0")
        if parts:
            self.s.add(f'<path d="{"".join(parts)}" fill="{fill}" stroke="{stroke}" '
                       f'stroke-width="{sw_px / self.k:.3f}" {extra}/>')


class Etichette:
    """Registro dei riquadri di testo e marcatori (in px), per segnalare le sovrapposizioni."""

    def __init__(self):
        self.box = []

    def prendi(self, x0, y0, x1, y1, nome):
        for bx0, by0, bx1, by1, n in self.box:
            if x0 < bx1 and bx0 < x1 and y0 < by1 and by0 < y1:
                print(f"  ! sovrapposizione: {nome} con {n}")
        self.box.append((x0, y0, x1, y1, nome))

    def testo(self, x, y, s, size, anchor="middle"):
        w = len(s) * size * 0.55
        x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
        self.prendi(x0, y - size * 0.8, x0 + w, y + size * 0.25, s[:18])
