#!/usr/bin/env python3
"""Il barile sulla tenda di Zog'tar: simulazione Monte Carlo del round di sorpresa.

Simula lo sgancio del barile da 48 m sulla tenda del comando (M7-C), con le
regole di ARC07-BARILE-SULLA-TENDA.md, versione del 2026-10-26 (SRD 3.5 con le
variazioni segnate): niente tiro per colpire, deviazione 1d8 per la direzione
e 1d4−1 quadretti; il barile e le fiale si rompono sempre (prendono anche loro
il danno della caduta); due palle di fuoco da 6d6 (Riflessi CD 14) dall'angolo
della casella d'impatto; oggetto in caduta 15d6 (SRD 3.5); l'olio come arma a
spargimento e come pinta versata (SRD 3.5); danno massiccio (SRD 3.5). Poi la
fine del primo round: l'olio che brucia, chi prende fuoco.

Le posizioni sono quelle della disposizione A di M7-C. Le colonne partono da
A = 0 e le righe da 01 = 0; ogni casella è 1,5 m.

Uso:
    python3 simula_barile.py              # tabella completa, 20.000 prove
    python3 simula_barile.py --prove 2000 --seme 7
"""
from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass, field

# ---------------------------------------------------------------- creature


@dataclass
class Creatura:
    nome: str
    caselle: list[tuple[int, int]]
    pf: int
    rifl: int
    temp: int
    rd: int = 0
    dentro: bool = True  # sotto il telo
    pf_ora: int = 0
    morto: bool = False
    in_fiamme: bool = False
    inzuppato: bool = False
    note: list[str] = field(default_factory=list)

    def centro(self) -> tuple[float, float]:
        xs = [c for c, _ in self.caselle]
        ys = [r for _, r in self.caselle]
        return (min(xs) + max(xs) + 1) / 2, (min(ys) + max(ys) + 1) / 2


def c(col: str, riga: int) -> tuple[int, int]:
    """'O', 13 -> (14, 12)."""
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return n - 1, riga - 1


def disposizione() -> list[Creatura]:
    """Disposizione A di M7-C (Scena 7): tutti svegli tranne il sacerdote."""
    return [
        Creatura("Zog'tar", [c("O", 13), c("P", 13), c("O", 14), c("P", 14)],
                 pf=283, rifl=9, temp=18, rd=3),
        Creatura("Guardia M13", [c("M", 13)], pf=60, rifl=3, temp=8),
        Creatura("Guardia N13", [c("N", 13)], pf=60, rifl=3, temp=8),
        Creatura("Guardia Q14", [c("Q", 14)], pf=60, rifl=3, temp=8),
        Creatura("Guardia M14", [c("M", 14)], pf=60, rifl=3, temp=8),
        # Dorme: indifeso, Destrezza 0 (SRD), quindi Riflessi +4 diventa −1 [INFERRED: Des +0].
        Creatura("Sacerdote", [c("N", 14)], pf=38, rifl=-1, temp=4),
        Creatura("Balvar", [c("R", 14)], pf=101, rifl=8, temp=13),
        Creatura("Grask", [c("P", 16)], pf=6, rifl=1, temp=3, dentro=False),
    ]


# Interno della tenda: J10-R14; telo: I9-S15; colmo sulla riga 12, da J a R.
INTERNO = {(x, y) for x in range(9, 18) for y in range(9, 14)}
TELO = {(x, y) for x in range(8, 19) for y in range(8, 15)}
COLMO = {(x, 11) for x in range(9, 18)}
BRACIERI = {c("L", 10), c("K", 14)}

MIRE = {
    "centro": (13.5, 11.5),   # il palo centrale, N12: il punto più alto del telo
    "seggio": (15.0, 13.0),   # l'incrocio al centro del seggio di Zog'tar
}

# ---------------------------------------------------------------- dadi


def d(n: int, f: int, rng: random.Random) -> int:
    return sum(rng.randint(1, f) for _ in range(n))


# ---------------------------------------------------------------- la quota

SCALA_DADI = [1, 2, 3, 4, 6, 8, 10, 12]   # 1 vuol dire nessuna deviazione


def piedi(quota_m: float) -> float:
    return quota_m / 0.3048


def dadi_oggetto_in_caduta(quota_m: float, libbre: float) -> int:
    """SRD 3.5, «Falling Objects»: quanti d6 fa a chi sta sotto."""
    ft = piedi(quota_m)
    if libbre >= 200:
        return 0 if ft < 10 else min(20, int(libbre // 200) + int((ft - 10) // 10))
    passo = next(p for lim, p in ((100, 20), (50, 30), (30, 40), (10, 50), (5, 60), (1, 70))
                 if libbre > lim)
    return min(20, int(ft // passo))


def dadi_caduta_propria(quota_m: float) -> int:
    """Il danno che prende l'oggetto stesso: 1d6 ogni 3 m, come chi cade (SRD)."""
    return min(20, int(piedi(quota_m) // 10))


def dado_deviazione(quota_m: float, pesante: bool = True, visto: bool = True) -> int:
    """Un gradino ogni 15 m di caduta; uno in più se è leggero, uno se è al buio."""
    gradino = int(quota_m // 15) + (0 if pesante else 1) + (0 if visto else 1)
    return SCALA_DADI[min(gradino, len(SCALA_DADI) - 1)]


def probabilita_legno(quota_m: float, prove: int = 20000, seme: int = 24) -> float:
    """Quante volte la botte spezza un palo o la trave (durezza 5, 60 pf), in percentuale."""
    rng = random.Random(seme)
    dadi = dadi_oggetto_in_caduta(quota_m - ALTEZZA_COLMO, 205)
    ok = sum(d(dadi, 6, rng) + d(rng.randint(1, 4), 8, rng) - DUREZZA_LEGNO >= PF_LEGNO
             for _ in range(prove))
    return 100 * ok / prove


def tempo_di_caduta(quota_m: float) -> float:
    return math.sqrt(2 * quota_m / 9.81) * 1.01


DIREZIONI = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def devia(p: tuple[float, float], caselle: int, rng: random.Random) -> tuple[float, float]:
    dx, dy = rng.choice(DIREZIONI)
    return p[0] + dx * caselle, p[1] + dy * caselle


def casella(p: tuple[float, float]) -> tuple[int, int]:
    return int(math.floor(p[0])), int(math.floor(p[1]))


def distanza_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1]) * 1.5


def nell_area(cr: Creatura, centro: tuple[float, float], raggio_m: float) -> bool:
    """La creatura è nell'area se il centro di una sua casella è nel raggio."""
    return any(distanza_m((x + 0.5, y + 0.5), centro) <= raggio_m for x, y in cr.caselle)


# ---------------------------------------------------------------- una prova


@dataclass
class Parametri:
    mira: str = "centro"
    fiale: int = 2
    dado_deviazione: int = 4     # 1d4−1 quadretti: chi sgancia sta fermo in aria
    in_volo: bool = False         # chi sgancia si muove: +6 quadretti in avanti (verso est)
    dadi_caduta: int = 15        # 15d6 sopra i 200 libbre, 7d6 sotto (SRD 3.5)
    cd_fiala: int = 14
    massiccio_unico: bool = True  # le fiale contano come un'esplosione sola per i 50 danni
    quota: float | None = None    # se c'è, decide i dadi della caduta e della deviazione
    inzuppato_brucia: bool = True  # chi è nel cuore prende fuoco senza TS (variazione)
    forno: bool = True            # la tenda fa da forno: chi è sotto il telo è nell'area (variazione)
    rostri: bool = True           # le lame sotto la botte: 1d4 da 1d8 sul colpo diretto (variazione)


ALTEZZA_COLMO = 6.0  # la trave del colmo e la cima dei pali
DUREZZA_LEGNO = 5    # SRD, legno
PF_LEGNO = 60        # SRD: 10 pf per pollice; palo e trave da 15 cm, cioè 6 pollici
RAGGIO_FUOCO = 6.0   # palla di fuoco: 20 piedi
RAGGIO_OLIO = 7.0    # all'aperto: 105 pinte, cuore 3 × 3 a 5 pinte e 60 quadretti a 1 pinta


def sotto_olio(cr: Creatura, punto: tuple[int, int]) -> bool:
    """Dentro la tenda l'olio copre tutto il pavimento; all'aperto, fino a 7 m."""
    if punto in TELO:
        return cr.dentro
    return nell_area(cr, (punto[0] + 0.5, punto[1] + 0.5), RAGGIO_OLIO)


def prova(par: Parametri, rng: random.Random) -> dict:
    crs = disposizione()
    for cr in crs:
        cr.pf_ora = cr.pf
    esito: dict = {"colmo": False, "intera": False}
    quota_reale = par.quota if par.quota is not None else 48.0
    if par.quota is not None:
        quota = par.quota
        par = Parametri(**{**par.__dict__, "dadi_caduta": dadi_oggetto_in_caduta(quota, 205),
                           "dado_deviazione": dado_deviazione(quota), "quota": None})
        # La botte si apre se il danno della sua caduta passa durezza 5 e 10 pf (SRD).
        # Se regge, le palle di fuoco la aprono, e l'olio esce solo al round dopo.
        esito["intera"] = d(dadi_caduta_propria(quota), 6, rng) - 5 < 10

    # 1. Lo sgancio non è un attacco: niente tiro per colpire, l'invisibilità resta.
    #    Deviazione come le armi a spargimento che mancano (SRD): 1d8 la direzione,
    #    e la distanza 1d4−1 quadretti (variazione: 1 quadretto ogni 15 m di caduta).
    p = MIRE[par.mira]
    passi = rng.randint(1, par.dado_deviazione) - 1
    if passi:
        p = devia(p, passi, rng)
    if par.in_volo:
        p = (p[0] + 6, p[1])
    punto = casella(p)
    esito["punto"] = punto
    esito["deviazione"] = passi
    # L'origine delle palle di fuoco è un angolo della casella d'impatto (SRD: le
    # aree partono da un incrocio della griglia).
    origine = (punto[0] + rng.randint(0, 1), punto[1] + rng.randint(0, 1))

    # 2. Il legno. Sulla riga 12 la botte prende un palo in cima o la trave del
    #    colmo, a 6 m: cade 6 m in meno, e il danno della caduta va al legno (SRD,
    #    oggetti: durezza 5 e 10 pf per pollice; palo e trave da 15 cm, 60 pf),
    #    con le lame dei rostri. Se passa, il legno si spezza e la tenda crolla
    #    subito; se no, la botte gli si apre sopra: sotto niente colpo diretto.
    sulla_trave = False
    if punto in COLMO or punto in {c("K", 12), c("N", 12), c("Q", 12)}:
        dadi_legno = dadi_oggetto_in_caduta(quota_reale - ALTEZZA_COLMO, 205)
        dn = d(dadi_legno, 6, rng) + (d(rng.randint(1, 4), 8, rng) if par.rostri else 0)
        if dn - DUREZZA_LEGNO >= PF_LEGNO:
            esito["colmo"] = True
        else:
            sulla_trave = True
        # la botte prende il danno della sua caduta fino al legno (SRD): sotto i 18 m può reggere
        esito["intera"] = d(dadi_caduta_propria(quota_reale - ALTEZZA_COLMO), 6, rng) - 5 < 10

    # 3. Il colpo diretto: una creatura sola, quella nella casella. Niente TS.
    #    Il telo di pelle toglie 3 (durezza 2 e 1 pf, SRD); i rostri sono lame di
    #    spada, e cadono con la botte: 1d4 lame da 1d8 (variazione, la fossa con
    #    gli spuntoni dell'SRD rovesciata). Tutto insieme è un attacco solo.
    colpito = None if sulla_trave else next((cr for cr in crs if punto in cr.caselle), None)
    danno_per: dict[str, list[int]] = {cr.nome: [] for cr in crs}
    if colpito:
        dn = d(par.dadi_caduta, 6, rng) - (3 if punto in TELO else 0)
        if par.rostri:
            dn += d(rng.randint(1, 4), 8, rng)
        danno_per[colpito.nome].append(max(0, dn - colpito.rd))
        esito["colpito"] = colpito.nome

    # 4. Le fiale si rompono tutte all'impatto: una palla di fuoco ciascuna.
    fuoco_per: dict[str, int] = {cr.nome: 0 for cr in crs}
    for _ in range(par.fiale):
        for cr in crs:
            if nell_area(cr, origine, RAGGIO_FUOCO) or (par.forno and cr.dentro and punto in TELO):
                dn = d(6, 6, rng)
                if rng.randint(1, 20) + cr.rifl >= par.cd_fiala:
                    dn //= 2
                fuoco_per[cr.nome] += dn
                if not par.massiccio_unico:
                    danno_per[cr.nome].append(dn)
    if par.massiccio_unico:
        for cr in crs:
            if fuoco_per[cr.nome]:
                danno_per[cr.nome].append(fuoco_per[cr.nome])

    # 5. L'olio. Dentro la tenda il telo lo ferma: copre tutto il pavimento, J10-R14.
    #    Chi è nel cuore (la casella d'impatto e le otto attorno) è colpito in pieno
    #    come da un'ampolla d'olio (SRD, fuoco dell'alchimista: 1d6 ora, 1d6 il round
    #    dopo); chi è sul resto del pavimento prende lo spruzzo, 1 danno. Fuori dal
    #    telo l'olio arriva solo col cuore.
    cuore = {(punto[0] + i, punto[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1)}
    for cr in crs:
        if esito["intera"]:
            break
        if any(q in cuore for q in cr.caselle):
            cr.inzuppato = True
            danno_per[cr.nome].append(d(1, 6, rng))
        elif sotto_olio(cr, punto):
            danno_per[cr.nome].append(1)

    # 6. Danni del round di sorpresa e danno massiccio (SRD 3.5: 50 da un solo attacco).
    for cr in crs:
        for dn in danno_per[cr.nome]:
            cr.pf_ora -= dn
            if dn >= 50 and cr.pf_ora > -10:
                if rng.randint(1, 20) == 1 or rng.randint(1, 20) + cr.temp < 15:
                    cr.morto = True
                    cr.note.append("danno massiccio")
        if cr.pf_ora <= -10:
            cr.morto = True

    # 7. Fine del primo round. La palla di fuoco accende l'olio (SRD: incendia i
    #    combustibili). Chi è nell'olio che brucia prende 1d3 (SRD, la pinta versata)
    #    e tira Riflessi CD 15 per non prendere fuoco (SRD); chi è inzuppato prende
    #    il secondo 1d6 dell'ampolla e, con la variazione, brucia senza TS.
    for cr in crs:
        if cr.morto:
            continue
        if esito["intera"] or not (cr.inzuppato or sotto_olio(cr, punto)):
            if esito["colmo"] and cr.dentro:
                cr.pf_ora -= d(2, 6, rng)
                cr.morto = cr.morto or cr.pf_ora <= -10
            continue
        cr.pf_ora -= d(1, 3, rng)
        if cr.inzuppato:
            cr.pf_ora -= d(1, 6, rng)
        if (cr.inzuppato and par.inzuppato_brucia) or rng.randint(1, 20) + cr.rifl < 15:
            cr.in_fiamme = True
            cr.pf_ora -= d(1, 6, rng)
        if esito["colmo"] and cr.dentro:
            cr.pf_ora -= d(2, 6, rng)  # il telo in fiamme crolla addosso (stato F, regola della casa)
        if cr.pf_ora <= -10:
            cr.morto = True

    esito["creature"] = {cr.nome: (cr.pf_ora, cr.morto, cr.in_fiamme) for cr in crs}
    return esito


def conta_olio() -> tuple[int, int]:
    """All'aperto: quadretti coperti dal cuore e dal resto, 1 pinta a quadretto."""
    o = (10.5, 10.5)
    area = [(x, y) for x in range(2, 20) for y in range(2, 20)
            if distanza_m((x + 0.5, y + 0.5), o) <= RAGGIO_OLIO]
    return 9, len(area) - 9


# ---------------------------------------------------------------- tabella


def riassumi(par: Parametri, n: int, seme: int) -> list[str]:
    rng = random.Random(seme)
    nomi = [cr.nome for cr in disposizione()]
    morti = {k: 0 for k in nomi}
    fuori = {k: 0 for k in nomi}  # a 0 pf o meno
    pf_zog = []
    pf_tutti: dict[str, list[int]] = {k: [] for k in nomi}
    in_fiamme = {k: 0 for k in nomi}
    colmo = 0
    devs = [0, 0, 0, 0]
    colpiti: dict[str, int] = {}
    for _ in range(n):
        e = prova(par, rng)
        colmo += e["colmo"]
        devs[e["deviazione"]] += 1
        if "colpito" in e:
            colpiti[e["colpito"]] = colpiti.get(e["colpito"], 0) + 1
        for k, (pf, morto, brucia) in e["creature"].items():
            pf_tutti[k].append(pf)
            in_fiamme[k] += brucia
            morti[k] += morto
            fuori[k] += (pf <= 0)
        pf_zog.append(e["creature"]["Zog'tar"][0])
    pf_zog.sort()
    pct = lambda x: f"{100 * x / n:.0f}%"  # noqa: E731
    righe = [
        f"### Mira: {par.mira} · fiale sul barile: {par.fiale} · caduta {par.dadi_caduta}d6"
        + (" · chi sgancia è in volo" if par.in_volo else ""),
        "",
        f"- palo o colmo spezzato, la tenda giù subito: {pct(colmo)}; deviazione 0/1/2/3 quadretti: "
        + " / ".join(pct(v) for v in devs),
        "- colpo diretto del barile: " + (", ".join(
            f"{k} {pct(v)}" for k, v in sorted(colpiti.items(), key=lambda kv: -kv[1])) or "nessuno"),
        f"- Zog'tar alla fine del round 1: mediana {pf_zog[n // 2]} pf su 283 "
        f"(10° percentile {pf_zog[n // 10]})",
        "",
        "| Chi | pf pieni | pf alla fine del round 1 (mediana) | in fiamme | a 0 pf o meno | morto |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    pieni = {cr.nome: cr.pf for cr in disposizione()}
    for k in nomi:
        v = sorted(pf_tutti[k])
        righe.append(f"| {k} | {pieni[k]} | {v[n // 2]} | {pct(in_fiamme[k])} | {pct(fuori[k])} | {pct(morti[k])} |")
    righe.append("")
    return righe


# ---------------------------------------------------------------- il palo centrale

NOMI_DIR = ["nord", "nord-est", "est", "sud-est", "sud", "sud-ovest", "ovest", "nord-ovest"]
PALI = {c("K", 12): "il palo ovest", c("N", 12): "il palo centrale", c("Q", 12): "il palo est"}


def nome_casella(q: tuple[int, int]) -> str:
    return f"{chr(65 + q[0])}{q[1] + 1}"


def tabella_palo(forno: bool = True) -> list[str]:
    """Le 25 cadute possibili mirando a N12: dove, che cosa prende, chi è nel cuore e nel fuoco."""
    crs = disposizione()
    righe = [
        "| d8 · metri | Casella | Probabilità | Che cosa prende | Nel cuore dell'olio | Fuori dalle palle di fuoco |",
        "|---|---|---:|---|---|---|",
    ]
    mira = c("N", 12)
    rotto = f"{probabilita_legno(48.0):.0f}%"
    casi = [(None, 0)] + [(i, k) for k in (1, 2, 3) for i in range(8)]
    for i, k in casi:
        if i is None:
            q, etichetta, prob = mira, "nessuna deviazione", "25%"
        else:
            dx, dy = DIREZIONI[i]
            q = (mira[0] + dx * k, mira[1] + dy * k)
            metri = math.hypot(dx, dy) * k * 1.5
            etichetta, prob = f"{i + 1} {NOMI_DIR[i]} · {metri:.1f} m".replace(".", ","), "3,1%"
        chi = next((cr.nome for cr in crs if q in cr.caselle), None)
        if q in PALI:
            prende = f"{PALI[q]}, in cima: lo spezza il {rotto}, e la tenda crolla; se no la botte gli si apre sopra"
        elif chi:
            prende = f"**{chi}**, 15d6 − 3 + 1d4 × 1d8"
        elif q in COLMO:
            prende = f"la trave del colmo: la spezza il {rotto}, e la tenda crolla; se no la botte le si apre sopra, e sotto niente colpo diretto"
        elif q[1] in (8, 14) or q[0] in (8, 18):
            prende = "il telo, sul bordo: metà olio fuori"
        else:
            prende = "il pavimento"
        cuore = {(q[0] + a, q[1] + b) for a in (-1, 0, 1) for b in (-1, 0, 1)}
        nel_cuore = [cr.nome for cr in crs if any(x in cuore for x in cr.caselle)]
        angoli = [(q[0] + a, q[1] + b) for a in (0, 1) for b in (0, 1)]
        dentro = [cr for cr in crs if forno and cr.dentro and q in TELO]
        fuori_sempre = [cr.nome for cr in crs if cr not in dentro
                        and not any(nell_area(cr, o, RAGGIO_FUOCO) for o in angoli)]
        fuori_forse = [cr.nome for cr in crs if cr not in dentro and cr.nome not in fuori_sempre
                       and not all(nell_area(cr, o, RAGGIO_FUOCO) for o in angoli)]
        fuori = ", ".join(fuori_sempre) or "nessuno"
        if fuori_forse:
            fuori += " · secondo l'angolo: " + ", ".join(fuori_forse)
        righe.append(f"| {etichetta} | {nome_casella(q)} | {prob} | {prende} | "
                     f"{', '.join(nel_cuore) or 'nessuno'} | {fuori} |")
    return righe


# ---------------------------------------------------------------- la quota, riga per riga

QUOTE = (48, 42, 36, 30, 27, 24, 18, 12, 9)


def tabella_quote() -> list[str]:
    righe = [
        "| Quota | Caduta | Botte: danno a chi sta sotto | 50 o più | La botte si apre | Spezza un palo o la trave | Deviazione: botte nella luce / al buio | Barilotto: danno, deviazione nella luce |",
        "|---|---|---|---:|---:|---:|---|---|",
    ]
    rng = random.Random(1)
    for q in QUOTE:
        n = dadi_oggetto_in_caduta(q, 205)
        p50 = sum(d(n, 6, rng) >= 50 for _ in range(20000)) / 200 if n else 0
        apre = sum(d(dadi_caduta_propria(q), 6, rng) - 5 >= 10 for _ in range(20000)) / 200
        dv, db = dado_deviazione(q), dado_deviazione(q, visto=False)
        dl = dado_deviazione(q, pesante=False)
        fmt = lambda x: "nessuna" if x == 1 else f"1d{x}−1"  # noqa: E731
        nb = dadi_oggetto_in_caduta(q, 31)
        righe.append(
            f"| {q} m | {tempo_di_caduta(q):.1f} s".replace(".", ",") + f" | **{n}d6** | {p50:.0f}% | {apre:.0f}% | {probabilita_legno(q):.0f}% "
            f"| {fmt(dv)} / {fmt(db)} | {nb}d6 · {fmt(dl)} |".replace("0d6", "niente"))
    return righe


def riassunto_quote(prove: int, seme: int) -> list[str]:
    righe = [
        "| Quota | La tenda giù subito | La botte resta intera | Zog'tar, pf (mediana) | Il sacerdote morto | Una guardia a terra (M13) | Grask morto |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for q in QUOTE:
        rng = random.Random(seme)
        colmo = intera = sac = gua = gra = 0
        zog = []
        for _ in range(prove):
            e = prova(Parametri(mira="centro", quota=q), rng)
            colmo += e["colmo"]
            intera += e["intera"]
            zog.append(e["creature"]["Zog'tar"][0])
            sac += e["creature"]["Sacerdote"][1]
            gua += e["creature"]["Guardia M13"][0] <= 0
            gra += e["creature"]["Grask"][1]
        zog.sort()
        pct = lambda x: f"{100 * x / prove:.0f}%"  # noqa: E731
        righe.append(f"| {q} m | {pct(colmo)} | {pct(intera)} | {zog[prove // 2]} | {pct(sac)} | {pct(gua)} | {pct(gra)} |")
    return righe


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--prove", type=int, default=20000)
    ap.add_argument("--seme", type=int, default=24)
    ap.add_argument("--caduta", type=int, default=15, help="dadi dell'oggetto in caduta (15 o 7)")
    ap.add_argument("--regole-srd", action="store_true",
                    help="ogni fiala è un attacco a sé per il danno massiccio, chi è inzuppato "
                         "tira il TS per non prendere fuoco, la palla di fuoco resta di 6 m "
                         "anche sotto il telo (lettura RAW)")
    ap.add_argument("--quote", action="store_true", help="la tabella per quota di sgancio")
    ap.add_argument("--palo", action="store_true", help="solo la tabella delle cadute mirando a N12")
    a = ap.parse_args()
    if a.quote:
        print("\n".join(tabella_quote() + [""] + riassunto_quote(a.prove, a.seme)))
        return
    if a.palo:
        print("\n".join(tabella_palo(forno=not a.regole_srd)))
        return
    cuore, resto = conta_olio()
    out = [f"<!-- generato da simula_barile.py --prove {a.prove} --seme {a.seme} "
           f"--caduta {a.caduta}{' --regole-srd' if a.regole_srd else ''} -->", "",
           f"All'aperto l'olio della botte coprirebbe {cuore + resto} quadretti: il cuore di "
           f"{cuore} (5 pinte a quadretto) e {resto} attorno (1 pinta a quadretto), "
           f"{cuore * 5 + resto} pinte su 105. Dentro la tenda il telo lo ferma, e copre "
           f"tutto il pavimento (45 quadretti).", ""]
    for mira in ("centro", "seggio"):
        for fiale in (1, 2, 3):
            par = Parametri(mira=mira, fiale=fiale, dadi_caduta=a.caduta,
                            massiccio_unico=not a.regole_srd, inzuppato_brucia=not a.regole_srd,
                            forno=not a.regole_srd)
            out += riassumi(par, a.prove, a.seme)
    out += riassumi(Parametri(mira="seggio", in_volo=True, dadi_caduta=a.caduta,
                              massiccio_unico=not a.regole_srd,
                              inzuppato_brucia=not a.regole_srd,
                              forno=not a.regole_srd), a.prove, a.seme)
    print("\n".join(out))


if __name__ == "__main__":
    main()
