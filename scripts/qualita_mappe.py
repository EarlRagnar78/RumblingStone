#!/usr/bin/env python3
"""
qualita_mappe.py — quanto e' buona una mappa tattica, misurato sulla griglia (ADR-0098).

Il collaudo (``collaudo_mappe.py``, ADR-0082) dice se una mappa si gioca. Questo
strumento la misura: lo spazio libero, gli anelli, gli ingressi, i vicoli
ciechi, i passaggi in fila indiana, la copertura, la distanza fra le fazioni,
la taglia delle creature, la scala dichiarata contro quella disegnata, la
densita' dei simboli. Le soglie e le loro fonti stanno in
``skills/rumblingstone-mapmaking/references/standard-qualita-mappe.md``.

Due classi di rilievo, come nel collaudo:

  E · errore   un fatto che non dipende dal gusto: l'intestazione dice una
               misura e la griglia un'altra, una direttiva punta fuori griglia.
  A · avviso   una soglia di mestiere, con la sua fonte. Non blocca mai.

Il punteggio parte da 100 e perde i pesi dei rilievi non derogati, compresi
quelli del collaudo. Le deroghe sono le stesse: ``@deroga <codice> ; <motivo>``.

Uso:
    python3 scripts/qualita_mappe.py                    # tutto il corpus
    python3 scripts/qualita_mappe.py FILE.md [...]      # solo questi master
    python3 scripts/qualita_mappe.py --classifica       # tabella dal peggiore
    python3 scripts/qualita_mappe.py --json OUT.json    # rapporto per macchine
    python3 scripts/qualita_mappe.py --strict FILE.md   # esce 1 se c'e' un E
    python3 scripts/qualita_mappe.py --json OUT.json --profonde
                                       # piu' le metriche profonde, solo nel JSON

Exit: 0 rapporto prodotto (anche con rilievi) · 1 rilievi E con --strict ·
2 errore d'uso o dipendenze mancanti. In sola lettura.
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

RADICE = Path(__file__).resolve().parent
sys.path.insert(0, str(RADICE))
import collaudo_mappe as C  # noqa: E402

F, MODO, FUORI = C.F, C.MODO, C.FUORI
UNITA = {s for s, m in MODO.items() if m == "unit"}
PG = "🔵"
NEMICI = {"🔴", "⚫", "🟡", "🟣"}
# Flip-Mat Enormous: 30" x 46" a quadretti da 1" (Paizo). Due tappeti sono il
# tetto di un campo tattico: oltre, la mappa e' strategica o va divisa.
FLIPMAT_ENORMOUS = 30 * 46
SCALA_TATTICA = 1.5
# Un PG Medio a 9 m (30 ft) fa 6 quadretti per azione di movimento, 12 col
# doppio movimento: tre round di doppio movimento sono 54 m.
QUADRETTI_PER_ROUND = 12
CREATURE_GRANDI = re.compile(
    r"\b(drag|wyrm|treant|gigant|ogre|ogro|troll|behir|idra|hydra|razorfiend|"
    r"manticor|vivern|wyvern|colosso|elementale\s+(anzian|enorm|grand|maggior))", re.I)
# «Cristallo gigante», «fungo gigante»: oggetti, non creature
NON_CREATURE = re.compile(r"cristall|\balber[oi]\b|fung|statua|roccia|rocce|masso|sassi|pietra|colonna|pilastr|"
                          r"impronta|recinto|tana|nido|atterraggio|\b(medio|piccolo|minuscolo)\b", re.I)
FORTIFICAZIONE = re.compile(r"fortezz|castell|\bmura\b|bastion|torrion|cortina|cinta", re.I)
# Due varchi a meno di 10 passi sono lo stesso ingresso (RICERCA-STRUMENTI-MAPPE.md
# §5 e §6.3): un riparatore automatico apriva due varchi a due quadretti l'uno
# dall'altro nella stessa stanza e il rilievo `struttura/un-ingresso` spariva.
PASSI_FRA_INGRESSI = 10
# le metriche profonde gia' calcolate, per impronta della griglia
_PROFONDE: dict = {}

# Pesi del punteggio. Euristici e dichiarati: dicono quanto un rilievo
# allontana la mappa dallo standard, non quanto vale la mappa.
PESI = {
    # errori di questo strumento
    "scala/dichiarata": 12,
    "direttive/fuori-griglia": 12,
    # coerenza
    "scala/tattica-non-a-1-5": 3,
    "scala/titolo": 4,
    "dimensioni/oltre-tavolo": 4,
    "funzione/blocco-pieno": 6,
    "oggetti/telo-enorme": 4,
    "oggetti/tende-a-grappolo": 3,
    "oggetti/fuoco-enorme": 2,
    "oggetti/fuoco-sotto-il-telo": 2,
    "oggetti/porta-enorme": 2,
    "coerenza/mura-sottili": 3,
    "taglia/non-entra": 5,
    "taglia/non-dichiarata": 4,
    # giocabilita'
    "fazioni/lontane": 4,
    "fazioni/a-contatto": 1,
    "spazio/affollato": 3,
    "spazio/disperso": 2,
    "struttura/un-ingresso": 3,
    "struttura/senza-anelli": 3,
    "struttura/vicoli-ciechi": 2,
    "struttura/fila-indiana": 2,
    # leggibilita'
    "lettura/troppi-simboli": 2,
    "lettura/legenda-locale-lunga": 1,
    "lettura/affollata": 2,
    # rilievo e contesto
    "contesto/quota-illeggibile": 12,
    "contesto/quota-mancante": 1,
    "contesto/quote-discordi": 3,
}
CLASSE = {c: "A" for c in PESI}
CLASSE.update({"scala/dichiarata": "E", "direttive/fuori-griglia": "E",
               "contesto/quota-illeggibile": "E"})
# `@quota 320 m ; s.l.m.`, `@dislivello +120 m ; sulla piana`: numero, unita', riferimento
MISURA_QUOTA = re.compile(r"^\s*([+\-−]?\d+(?:[.,]\d+)?)\s*(m|metri|ft|piedi)?\b\s*(.*)$", re.I)
PIEDE_M = 0.3048
TOLLERANZA_QUOTA_M = 5
AMBIENTI_CON_QUOTA = ("esterno", "abitato")
TATTICI = {c for c in PESI if c.split("/")[0] in ("fazioni", "spazio", "struttura", "taglia")} | {
    "scala/tattica-non-a-1-5", "dimensioni/oltre-tavolo"}
# Il collaudo pesa nel punteggio: ogni suo errore quanto un errore di qui, i
# suoi avvisi poco, perche' M1, M2 e M4 non sono calibrate.
PESO_E_COLLAUDO = 12
TETTO_E_COLLAUDO = 48
PESI_A_COLLAUDO = {"ingombro/grande": 4, "zone/separate": 2, "m1/copertura": 2,
                   "m2/vuoto": 2, "m4/esposizione": 2}
PESO_A_COLLAUDO = 1
BANDE = ((90, "buona"), (75, "da ritoccare"), (55, "da rivedere"), (0, "da rifare"))


def _distinti(ingressi: list[set], perc: set) -> int:
    """Quanti ingressi distinti: due varchi contano come due solo se stanno ad
    almeno PASSI_FRA_INGRESSI passi l'uno dall'altro, o se non si raggiungono.

    Un passo e' lo spostamento fra due celle percorribili che hanno un lato in
    comune (4-connessione, niente diagonale): la misura di ``genera_ripara.py``
    in RICERCA-STRUMENTI-MAPPE.md §5. La distanza fra due varchi e' quella
    fra le loro celle piu' vicine. I varchi piu' vicini si uniscono, anche a
    catena (A vicino a B, B vicino a C: un ingresso solo)."""
    n = len(ingressi)
    padre = list(range(n))
    # una scala o un portale disegnati su una cella che blocca restano raggiungibili
    ammesse = perc.union(*ingressi) if ingressi else perc

    def radice(i):
        while padre[i] != i:
            padre[i] = padre[padre[i]]
            i = padre[i]
        return i
    for i in range(n):
        dist = {c: 0 for c in ingressi[i]}
        frontiera = sorted(dist)
        for passo in range(1, PASSI_FRA_INGRESSI):
            nuova = []
            for x, y in frontiera:
                for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if q in ammesse and q not in dist:
                        dist[q] = passo
                        nuova.append(q)
            frontiera = nuova
        for j in range(i + 1, n):
            if any(c in dist for c in ingressi[j]):
                padre[radice(j)] = radice(i)
    return len({radice(i) for i in range(n)})


def banda(voto: int) -> str:
    return next(nome for soglia, nome in BANDE if voto >= soglia)


def _numero(s: str) -> float:
    return float(s.replace(",", "."))


class Qualita:
    """Le metriche di una griglia gia' collaudata."""

    def __init__(self, collaudo: "C.Collaudo"):
        self.c = collaudo
        self.G = collaudo.G
        self.d = collaudo.d
        self.g = collaudo.G.g
        self.tattica = collaudo.tattica
        self.rilievi: list[dict] = []
        self.m: dict = {}

    # --- rilievi --------------------------------------------------------------
    def rileva(self, codice: str, cella, messaggio: str):
        if codice in TATTICI and not self.tattica:
            return
        motivo = self.d["deroghe"].get(codice)
        derogato = motivo is not None and len(motivo) >= C.MOTIVO_MINIMO
        self.rilievi.append({
            "codice": codice, "classe": CLASSE[codice],
            "cella": C.a1(*cella, self.G.righe) if cella else None,
            "messaggio": messaggio, "deroga": motivo if derogato else None})

    # --- calcolo --------------------------------------------------------------
    def esegui(self) -> "Qualita":
        np, _, ndimage = C._dipendenze()
        G = self.G
        perc = self.c.percorribili()
        comp = self.c.componenti(perc)
        celle = sum(len(r) for r in G.celle)
        P = np.zeros((G.H, G.W), dtype=bool)
        for x, y in perc:
            P[y, x] = True
        scala = self.g.get("scale_m") or SCALA_TATTICA
        self.m.update({"celle": celle, "scala_m": scala,
                       "area_m2": round(celle * scala * scala),
                       "libere": round(len(perc) / celle, 3) if celle else 0.0,
                       "flipmat": round(celle / FLIPMAT_ENORMOUS, 2)})

        self._coerenza(np, ndimage, scala)
        self._mura(np)
        self._direttive()
        self._contesto()
        self._lettura(perc)
        if perc:
            self._struttura(np, ndimage, P, perc, comp)
            self._fazioni(perc, comp, scala)
            self._taglie(perc)
            self._copertura(perc)
        return self

    def _coerenza(self, np, ndimage, scala):
        G, g = self.G, self.g
        dich = g.get("declared_dims")
        if dich and tuple(dich) != (G.W, G.H):
            self.rileva("scala/dichiarata", None,
                        f"l'intestazione dice {dich[0]} col × {dich[1]} righe, la griglia ne ha "
                        f"{G.W} × {G.H}: l'SVG stampa una misura falsa")
        if self.d["tipo"] in (None, "tattica") and g.get("scale_m") and g["scale_m"] != SCALA_TATTICA:
            self.rileva("scala/tattica-non-a-1-5", None,
                        f"tattica a {g['scale_m']:g} m per quadretto: le miniature stanno su 1,5 m. "
                        "Dichiara @tipo strategica, o ridisegna la parte dello scontro a 1,5 m")
        m = re.search(r"(\d+(?:[.,]\d+)?)\s*m\s*[×x]\s*(\d+(?:[.,]\d+)?)\s*m\b", g.get("title", ""))
        if m:
            a, b = _numero(m.group(1)), _numero(m.group(2))
            w, h = G.W * scala, G.H * scala

            def vicino(p, q):
                return abs(p - q) <= 0.15 * max(p, q)
            if not ((vicino(a, w) and vicino(b, h)) or (vicino(a, h) and vicino(b, w))):
                self.rileva("scala/titolo", None,
                            f"il titolo dice {a:g} × {b:g} m, la griglia misura {w:g} × {h:g} m "
                            f"a {scala:g} m per quadretto")
        titolo = g.get("title", "")
        q = re.search(r"(\d+(?:[.,]\d+)?)\s*m\s*/\s*(?:sq|quadrett|cella)|1\s*(?:sq|quadretto)\s*=\s*"
                      r"(\d+(?:[.,]\d+)?)\s*m", titolo, re.I)
        if q:
            dichiarata = _numero(q.group(1) or q.group(2))
            if abs(dichiarata - scala) > 0.01:
                self.rileva("scala/titolo", None,
                            f"il titolo dice {dichiarata:g} m per quadretto, l'intestazione {scala:g}: "
                            "il renderer usa l'intestazione dentro il recinto")
        if self.d["tipo"] in (None, "tattica") and re.search(r"strateg", titolo, re.I):
            self.rileva("scala/titolo", None,
                        "il titolo dice «strategica», la mappa e' collaudata come tattica: "
                        "scrivi @tipo strategica e la scala vera nell'intestazione")
        if self.m["celle"] > 2 * FLIPMAT_ENORMOUS:
            self.rileva("dimensioni/oltre-tavolo", None,
                        f"{G.W} × {G.H} = {self.m['celle']} quadretti, {self.m['flipmat']} Flip-Mat "
                        "Enormous: oltre due tappeti lo scontro si divide in carte o diventa strategico")

        # i simboli dicono la funzione: ⬛ muratura piena, 🎪 telo, ⛺ tenda piccola, 🔥 fuoco
        def blocchi(simboli, conn=4):
            M = np.zeros((G.H, G.W), dtype=bool)
            for x, y, c in G.tutte():
                if c in simboli:
                    M[y, x] = True
            struttura = np.ones((3, 3), dtype=bool) if conn == 8 else None
            lab, k = ndimage.label(M, structure=struttura)
            return [np.argwhere(lab == i) for i in range(1, k + 1)]

        if self.d["ambiente"] in ("esterno", "abitato", None):
            pieni = blocchi({"⬛"})
            if pieni:
                piu = max(pieni, key=len)
                if len(piu) >= 60 and len(piu) >= 0.25 * self.m["celle"]:
                    y, x = piu[0]
                    self.rileva("funzione/blocco-pieno", (int(x), int(y)),
                                f"un blocco di ⬛ di {len(piu)} celle, il {len(piu) / self.m['celle']:.0%} "
                                "della mappa: e' muratura piena, e SVG e UVTT ne fanno un muro. "
                                "Tende, recinti e cortili vanno disegnati con il loro simbolo")
        for b in blocchi({"🎪"}):
            alto = int(b[:, 0].max() - b[:, 0].min() + 1)
            largo = int(b[:, 1].max() - b[:, 1].min() + 1)
            if max(alto, largo) * scala > 18:
                y, x = b[0]
                self.rileva("oggetti/telo-enorme", (int(x), int(y)),
                            f"un telo di {largo} × {alto} quadretti ({largo * scala:g} × {alto * scala:g} m): "
                            "un palo regge 9-10 m, un padiglione a tre pali 16,5 m")
        for b in blocchi({"⛺"}):
            if len(b) >= 4:
                y, x = b[0]
                self.rileva("oggetti/tende-a-grappolo", (int(x), int(y)),
                            f"{len(b)} ⛺ attaccate: ⛺ e' una tenda piccola sola. Una tenda grande e' "
                            "🎪 riempito; tende distinte hanno 1 quadretto vuoto attorno per i tiranti")
        for b in blocchi({"🔥", "💥"}):
            if len(b) >= 5 and self.d["ambiente"] != "caverna":
                y, x = b[0]
                self.rileva("oggetti/fuoco-enorme", (int(x), int(y)),
                            f"un fuoco di {len(b)} celle: un falo' da campo sta in 1-2 quadretti. "
                            "Se e' un incendio, scrivilo nella legenda e deroga")
        teli = {(x, y) for x, y, c in G.tutte() if c in ("🎪", "⛺")}
        for x, y, c in G.tutte():
            if c == "🔥" and any((x + dx, y + dy) in teli for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                self.rileva("oggetti/fuoco-sotto-il-telo", (x, y),
                            "un fuoco a 1,5 m da un telo: nessun accampamento lo fa (tiranti, scintille)")
                break
        for b in blocchi({"🚪", "🔒"}):
            if len(b) >= 4:
                y, x = b[0]
                self.rileva("oggetti/porta-enorme", (int(x), int(y)),
                            f"una porta di {len(b)} quadretti ({len(b) * scala:g} m): una porta e' 1-2, "
                            "un portone da carro 2-3")

    def _mura(self, np):
        """Le mura di una fortezza hanno uno spessore: una cortina e' 2-4 quadretti."""
        G, g = self.G, self.g
        if "🏰" in G.locali or not FORTIFICAZIONE.search(g.get("title", "")):
            return
        if self.d["ambiente"] not in ("esterno", "abitato"):
            return
        M = np.zeros((G.H, G.W), dtype=bool)
        for x, y, c in G.tutte():
            if c == "🏰":
                M[y, x] = True
        if M.sum() < 20:
            return
        sottili = 0
        for y, x in np.argwhere(M):
            o = sum(1 for dx in (-1, 1) if 0 <= x + dx < G.W and M[y, x + dx])
            v = sum(1 for dy in (-1, 1) if 0 <= y + dy < G.H and M[y + dy, x])
            # una cella di un muro spesso 1: muro su un solo asse
            if (o and not v) or (v and not o):
                sottili += 1
        frazione = sottili / int(M.sum())
        self.m["mura_sottili"] = round(frazione, 2)
        if frazione > 0.8:
            self.rileva("coerenza/mura-sottili", None,
                        f"il {frazione:.0%} delle mura e' spesso un quadretto (1,5 m): una cortina di castello "
                        "e' 2-4 quadretti, con il camminamento in cima")

    def _direttive(self):
        """Ogni coordinata scritta in una direttiva sta dentro la griglia."""
        G = self.G

        def fuori(tok: str) -> bool:
            tok = tok.strip()
            if not re.fullmatch(r"[A-Za-z]{1,2}\d{1,3}", tok):
                return False  # non e' una coordinata (es. «loop»): non si giudica
            pos = C._cella(tok, G.righe)
            return pos is None or pos[0] >= len(G.celle[pos[1]])
        for riga in self.g.get("annotations", []):
            s = riga.strip()
            tipo, _, resto = s[1:].partition(" ")
            tipo, parti = tipo.lower(), [p.strip() for p in resto.split(";")]
            celle: list[str] = []
            if tipo in ("mark",) and len(parti) >= 2:
                celle = [parti[1]]
            elif tipo == "path" and len(parti) >= 2:
                celle = parti[1].split()
            elif tipo == "zone" and parti:
                celle = parti[0].split("-")
            elif tipo in ("taglia", "collega", "verso") and parti:
                celle = [parti[0]]
            sbagliate = [t for t in celle if fuori(t)]
            if sbagliate:
                self.rileva("direttive/fuori-griglia", None,
                            f"«{s[:70]}»: {', '.join(sbagliate)} fuori dalla griglia "
                            f"({C.R.col_label(G.W - 1)}{G.righe[-1]:02d} e' l'ultima cella)")

    def _contesto(self):
        """`@quota`, `@dislivello` e `@luogo`: la mappa dice dove sta nel mondo."""
        dichiarate: dict = {}
        for riga in self.g.get("annotations", []):
            s = riga.strip()
            tipo, _, resto = s[1:].partition(" ")
            tipo = tipo.lower()
            if tipo == "luogo" and resto.strip():
                self.m["luogo"] = resto.strip()
            if tipo not in ("quota", "dislivello"):
                continue
            valore, _, rif = resto.partition(";")
            mm = MISURA_QUOTA.match(valore)
            if not mm:
                self.rileva("contesto/quota-illeggibile", None,
                            f"«{s[:70]}»: serve un numero in metri o piedi, es. `@{tipo} 120 m ; "
                            f"{'sulla piana di Talar' if tipo == 'dislivello' else 's.l.m.'}`")
                continue
            metri = _numero(mm.group(1).replace("−", "-"))
            if (mm.group(2) or "m").lower() in ("ft", "piedi"):
                metri *= PIEDE_M
            dichiarate[tipo] = {"m": round(metri, 1),
                                "riferimento": (rif.strip() or mm.group(3).strip()) or None}
        self.m.update({k: v for k, v in dichiarate.items()})
        serve = self.d["ambiente"] in AMBIENTI_CON_QUOTA or self.d["tipo"] == "strategica"
        mancano = [t for t in ("quota", "dislivello") if t not in dichiarate]
        if serve and mancano:
            self.rileva("contesto/quota-mancante", None,
                        f"manca {' e '.join('@' + t for t in mancano)}: una mappa all'aperto dice a che "
                        "altezza sta e quanto sale o scende rispetto a cio' che la circonda "
                        "(es. `@quota 450 m ; s.l.m.` e `@dislivello +120 m ; sulla piana`)")

    def _lettura(self, perc):
        G = self.G
        simboli = Counter(c for _, _, c in G.tutte() if c and c not in UNITA)
        icone = sum(1 for x, y, c in G.tutte() if (x, y) in perc and MODO.get(c) == "icon")
        self.m["simboli"] = len(simboli)
        self.m["simboli_locali"] = len([s for s in simboli if s not in F])
        self.m["densita_icone"] = round(icone / len(perc), 3) if perc else 0.0
        if len(simboli) > 18:
            self.rileva("lettura/troppi-simboli", None,
                        f"{len(simboli)} simboli diversi: oltre 18 il giocatore smette di leggere la legenda")
        if self.m["simboli_locali"] > 8:
            self.rileva("lettura/legenda-locale-lunga", None,
                        f"{self.m['simboli_locali']} simboli locali: usa prima quelli universali di legend.yaml")
        if perc and self.m["densita_icone"] > 0.30:
            self.rileva("lettura/affollata", None,
                        f"il {self.m['densita_icone']:.0%} del pavimento porta un'icona: il terreno non si legge")

    # --- struttura: anelli, ingressi, vicoli, larghezze -------------------------
    def _struttura(self, np, ndimage, P, perc, comp):
        G = self.G
        # anelli: i buchi dello spazio percorribile (primo numero di Betti), cioe'
        # gli ostacoli chiusi su ogni lato da celle percorribili. Il muro tocca il
        # muro anche in diagonale, perche' la diagonale non passa l'angolo (SRD).
        B = ~P
        lab, k = ndimage.label(B, structure=np.ones((3, 3), dtype=bool))
        bordo = set(np.unique(np.concatenate([lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]])))
        tattici, strutturali = 0, 0
        for i in range(1, k + 1):
            if i in bordo:
                continue
            tattici += 1
            buco = lab == i
            giro = ndimage.binary_dilation(buco, structure=np.ones((3, 3), dtype=bool)) & P
            if buco.sum() >= 4 and giro.sum() >= 16:
                strutturali += 1
        self.m["anelli"] = tattici
        self.m["anelli_strutturali"] = strutturali

        # ingressi: tratti percorribili del bordo, scale e botole, portali
        giro_bordo = ([(x, 0) for x in range(G.W)] + [(G.W - 1, y) for y in range(1, G.H)]
                      + [(x, G.H - 1) for x in range(G.W - 2, -1, -1)]
                      + [(0, y) for y in range(G.H - 2, 0, -1)])
        aperti = [p in perc for p in giro_bordo]
        passaggi = [{(x, y)} for x, y, c in G.tutte()
                    if F.get(c, {}).get("posa") == "fra_livelli" or c in ("🌀", "🪜")]
        if all(aperti):
            # tutto il bordo e' aperto: un campo aperto, quattro lati
            varchi = 4 + len(passaggi)
            self.m["ingressi"] = 4 + _distinti(passaggi, perc)
        else:
            tratti = []
            for i, a in enumerate(aperti):
                if not a:
                    continue
                if aperti[i - 1] and tratti:
                    tratti[-1].add(giro_bordo[i])
                else:
                    tratti.append({giro_bordo[i]})
            # il giro e' chiuso: un tratto che passa dall'ultima cella alla prima e' uno solo
            if len(tratti) > 1 and aperti[0] and aperti[-1]:
                tratti[0] |= tratti.pop()
            varchi = len(tratti) + len(passaggi)
            self.m["ingressi"] = _distinti(tratti + passaggi, perc)
        self.m["varchi"] = varchi
        self.m["bordo_aperto"] = round(sum(aperti) / len(aperti), 2) if aperti else 0.0

        # larghezza locale: il tratto piu' corto fra orizzontale e verticale
        oriz = np.zeros((G.H, G.W), dtype=int)
        vert = np.zeros((G.H, G.W), dtype=int)
        for y in range(G.H):
            x = 0
            while x < G.W:
                if P[y, x]:
                    x2 = x
                    while x2 < G.W and P[y, x2]:
                        x2 += 1
                    oriz[y, x:x2] = x2 - x
                    x = x2
                else:
                    x += 1
        for x in range(G.W):
            y = 0
            while y < G.H:
                if P[y, x]:
                    y2 = y
                    while y2 < G.H and P[y2, x]:
                        y2 += 1
                    vert[y:y2, x] = y2 - y
                    y = y2
                else:
                    y += 1
        larg = np.minimum(oriz, vert)
        self.larghezza = larg
        stretti = int(((larg == 1) & P).sum())
        self.m["fila_indiana"] = round(stretti / len(perc), 3)
        creature = sum(1 for _, _, c in G.tutte() if c in UNITA)
        if creature >= 6 and self.m["fila_indiana"] > 0.5:
            self.rileva("struttura/fila-indiana", None,
                        f"il {self.m['fila_indiana']:.0%} del percorribile e' largo un quadretto, con "
                        f"{creature} creature: si combatte in fila indiana, uno alla volta")

        # vicoli ciechi: celle con un solo vicino ortogonale percorribile, lontane
        # dal bordo e senza niente di notevole entro 2 quadretti
        def notevole(c) -> bool:
            return c not in (None, FUORI) and (MODO.get(c) in ("icon", "unit") or c not in F)
        vicoli, vuoti = 0, []
        for x, y in sorted(perc):
            if x in (0, G.W - 1) or y in (0, G.H - 1):
                continue
            n4 = sum((x + dx, y + dy) in perc for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if n4 != 1:
                continue
            vicoli += 1
            if not any(notevole(G.at(x + dx, y + dy)) for dx in range(-2, 3) for dy in range(-2, 3)):
                vuoti.append((x, y))
        self.m["vicoli_ciechi"] = vicoli
        self.m["vicoli_vuoti"] = len(vuoti)

        amb = self.d["ambiente"]
        if amb in ("interni", "caverna"):
            if self.m["ingressi"] < 2 and len(perc) >= 150:
                self.rileva("struttura/un-ingresso", None,
                            f"{self.m['ingressi']} ingresso su {len(perc)} celle percorribili: "
                            "chi difende sa da dove si entra (Jaquays: piu' ingressi)")
            if strutturali == 0 and len(perc) >= 300:
                self.rileva("struttura/senza-anelli", None,
                            "nessun anello attorno a un blocco di muro: ogni percorso torna indietro "
                            "sui suoi passi (Jaquays, Dormans: almeno un anello)")
        if len(vuoti) >= 3:
            self.rileva("struttura/vicoli-ciechi", vuoti[0],
                        f"{len(vuoti)} vicoli ciechi senza niente in fondo: un corridoio che non porta "
                        "a niente chiede una ragione (un deposito, una latrina, una porta segreta)")

    # --- fazioni ----------------------------------------------------------------
    def _distanze(self, origini, perc):
        """Dijkstra dalle origini con la diagonale a 1,5 (5-10-5) e il costo del terreno."""
        dist = {o: 0.0 for o in origini}
        coda = [(0.0, o) for o in origini]
        heapq.heapify(coda)
        while coda:
            d, (x, y) = heapq.heappop(coda)
            if d > dist.get((x, y), math.inf):
                continue
            for q in self.c.vicini(x, y, perc):
                passo = 1.5 if q[0] != x and q[1] != y else 1.0
                costo = F.get(self.G.at(*q), {}).get("move_cost") or 1
                nd = d + passo * max(1, costo)
                if nd < dist.get(q, math.inf):
                    dist[q] = nd
                    heapq.heappush(coda, (nd, q))
        return dist

    def _fazioni(self, perc, comp, scala):
        G = self.G
        pg = [(x, y) for x, y, c in G.tutte() if c == PG]
        nemici = [(x, y) for x, y, c in G.tutte() if c in NEMICI]
        creature = sum(1 for _, _, c in G.tutte() if c in UNITA)
        self.m["pg"], self.m["nemici"], self.m["creature"] = len(pg), len(nemici), creature
        if creature:
            self.m["celle_per_creatura"] = round(len(perc) / creature, 1)
            if creature >= 4 and self.m["celle_per_creatura"] < 4:
                self.rileva("spazio/affollato", None,
                            f"{self.m['celle_per_creatura']} celle libere per creatura: non c'e' spazio "
                            "per muoversi, aggirare o ritirarsi")
            if creature >= 4 and self.m["celle_per_creatura"] > 150 and self.m["celle"] > FLIPMAT_ENORMOUS:
                self.rileva("spazio/disperso", None,
                            f"{self.m['celle_per_creatura']} celle libere per creatura su una mappa piu' "
                            "grande di un Flip-Mat Enormous: lo scontro occupa un angolo")
        if not (pg and nemici):
            return
        dist = self._distanze(pg, perc)
        verso = [dist[n] for n in nemici if n in dist]
        if not verso:
            return
        minimo = min(verso)
        self.m["distanza_min_q"] = round(minimo, 1)
        self.m["distanza_min_m"] = round(minimo * scala, 1)
        self.m["distanza_media_m"] = round(sum(verso) / len(verso) * scala, 1)
        self.m["round_al_contatto"] = math.ceil(max(0.0, minimo - 1) * scala / SCALA_TATTICA
                                                / QUADRETTI_PER_ROUND)
        if minimo * scala > QUADRETTI_PER_ROUND * 3 * SCALA_TATTICA:
            self.rileva("fazioni/lontane", None,
                        f"il nemico piu' vicino e' a {minimo * scala:.0f} m di cammino dai PG: oltre tre "
                        "round di doppio movimento prima del contatto")
        if minimo <= 1.0:
            self.rileva("fazioni/a-contatto", None,
                        "PG e nemici partono adiacenti: e' un'imboscata o un errore di posa?")
        self.m["strozzatura"] = self._strozzatura(pg, nemici, perc)

    def _strozzatura(self, pg, nemici, perc):
        """Il passaggio piu' stretto del cammino piu' largo fra PG e nemici."""
        larg = self.larghezza
        padre = {}

        def trova(a):
            while padre[a] != a:
                padre[a] = padre[padre[a]]
                a = padre[a]
            return a
        ordine = sorted(perc, key=lambda p: -int(larg[p[1], p[0]]))
        pg_s, nem_s = set(pg), set(nemici)
        radici_pg: set = set()
        for p in ordine:
            padre[p] = p
            for q in self.c.vicini(*p, perc):
                if q in padre:
                    padre[trova(q)] = trova(p)
            radici_pg = {trova(a) for a in pg_s if a in padre}
            if radici_pg & {trova(b) for b in nem_s if b in padre}:
                return int(larg[p[1], p[0]])
        return None

    def _taglie(self, perc):
        G = self.G
        dichiarate = {C._cella(cella, G.righe): t for cella, t in self.d["taglia"]}
        for pos, taglia in dichiarate.items():
            lato = C.INGOMBRO.get(taglia.split()[0] if taglia else "")
            if not pos or not lato:
                continue
            x0, y0 = pos
            se = G.at(x0, y0)

            def libera(x, y):
                # la creatura sta sulle celle sue: il treant 🌳 blocca gli altri, non se stesso
                return (x, y) in perc or G.at(x, y) in (se,) or G.at(x, y) in UNITA
            entra = any(all(libera(x0 - i + a, y0 - j + b) for a in range(lato) for b in range(lato))
                        for i in range(lato) for j in range(lato))
            if not entra:
                self.rileva("taglia/non-entra", pos,
                            f"una creatura {taglia} ({lato}×{lato}) non ha {lato}×{lato} quadretti liberi "
                            "attorno alla sua cella: la miniatura non sta sulla mappa")
        grandi = {k for k, v in G.locali.items()
                  if CREATURE_GRANDI.search(v) and not NON_CREATURE.search(v)}
        if not NON_CREATURE.search(G.locali.get("🌳", "")):
            grandi.add("🌳")  # il treant della legenda universale e' Enorme (SRD)
        visti = set()
        for x, y, c in G.tutte():
            if c not in grandi or c in visti or (x, y) in dichiarate:
                continue
            blocco = sum(1 for dx in (0, 1) for dy in (0, 1) if G.at(x + dx, y + dy) == c)
            if blocco == 4:
                continue  # disegnata 2×2: la taglia si vede
            visti.add(c)
            nome = G.locali.get(c, "treant")[:40]
            self.rileva("taglia/non-dichiarata", (x, y),
                        f"«{c}» ({nome}) e' su un quadretto e non ha @taglia: un drago o un treant "
                        "e' Grande o piu', 2×2 o 3×3")

    def _copertura(self, perc):
        G = self.G
        riparo = {(x, y) for x, y, c in G.tutte()
                  if F.get(c, {}).get("cover") in ("half", "three_quarters", "total")}
        coperte = sum(1 for x, y in perc
                      if any((x + dx, y + dy) in riparo for dx in (-1, 0, 1) for dy in (-1, 0, 1)))
        self.m["copertura"] = round(coperte / len(perc), 3)
        if G.W >= 12 and G.H >= 12:
            m1, m2 = self.c._copertura_e_vuoto(perc)
            self.m["m1"], self.m["m2"] = round(m1, 3), round(m2, 3)

    # --- punteggio ----------------------------------------------------------------
    def penalita(self) -> dict:
        e_coll = [r for r in self.c.rilievi if r["classe"] == "E" and not r["deroga"]]
        a_coll = [r for r in self.c.rilievi if r["classe"] == "A" and not r["deroga"]]
        miei = [r for r in self.rilievi if not r["deroga"]]
        return {
            "collaudo_errori": min(TETTO_E_COLLAUDO, PESO_E_COLLAUDO * len(e_coll)),
            "collaudo_avvisi": sum(PESI_A_COLLAUDO.get(r["codice"], PESO_A_COLLAUDO) for r in a_coll),
            "qualita": sum(PESI[r["codice"]] for r in miei),
        }

    def voto(self) -> int:
        return max(0, 100 - sum(self.penalita().values()))

    def impronta(self) -> str:
        """La stessa griglia con le stesse direttive: una copia (Atlante e master)."""
        righe = "\n".join("".join(r) for r in self.G.celle) + "\n" + "\n".join(self.g.get("annotations", []))
        return hashlib.sha1(righe.encode("utf-8")).hexdigest()[:12]

    def profonde(self) -> dict:
        """Le metriche di configurazione senza soglia (qualita_mappe_profonde.py).
        Si calcolano a parte e non entrano mai nel voto ne' nei rilievi. Solo
        sulle tattiche: le miniature non camminano su una strategica, e la VGA
        di 7.000 celle costa minuti. Le copie della stessa griglia si misurano
        una volta."""
        if not self.tattica:
            return {"saltata": f"mappa {self.d['tipo']}: le metriche profonde misurano le tattiche"}
        chiave = self.impronta()
        if chiave not in _PROFONDE:
            import qualita_mappe_profonde as P
            _PROFONDE[chiave] = P.misura(self.c, F, MODO, FUORI)
        return _PROFONDE[chiave]

    def come_dato(self, profonde: bool = False) -> dict:
        base = self.c.come_dato()
        dato = {"file": base["file"], "mappa": base["mappa"], "titolo": base["titolo"],
                "tipo": base["tipo"], "ambiente": base["ambiente"], "dimensioni": base["dimensioni"],
                "impronta": self.impronta(), "voto": self.voto(), "banda": banda(self.voto()),
                "penalita": self.penalita(), "metriche": self.m,
                "rilievi": self.rilievi,
                "rilievi_collaudo": [r for r in self.c.rilievi if not r["deroga"]]}
        if profonde:
            dato["profonde"] = self.profonde()
        return dato


def misura(file: Path, corpus: dict) -> list[Qualita]:
    testo = file.read_text(encoding="utf-8")
    mappe = C.R.extract_maps(testo)
    corpus[file.resolve()] = mappe
    return [Qualita(C.Collaudo(file, i, g, corpus).esegui()).esegui() for i, g in enumerate(mappe, 1)]


def confronta_luoghi(esiti: list[Qualita]) -> None:
    """Le mappe con lo stesso `@luogo` dichiarano la stessa quota, entro 5 m."""
    per_luogo: dict = {}
    for q in esiti:
        luogo, quota = q.m.get("luogo"), q.m.get("quota")
        if luogo and quota:
            per_luogo.setdefault(luogo.casefold(), []).append(q)
    for gruppo in per_luogo.values():
        quote = [q.m["quota"]["m"] for q in gruppo]
        if max(quote) - min(quote) <= TOLLERANZA_QUOTA_M:
            continue
        for q in gruppo:
            altre = ", ".join(f"{Path(o.c.come_dato()['file']).name} {o.m['quota']['m']:g} m"
                              for o in gruppo if o is not q)
            q.rileva("contesto/quote-discordi", None,
                     f"@luogo «{q.m['luogo']}» a {q.m['quota']['m']:g} m, ma {altre}: lo stesso posto "
                     "ha una quota sola (un punto diverso dello stesso sito prende un @luogo suo)")


def _riga_metriche(m: dict) -> str:
    parti = [f"libere {m.get('libere', 0):.0%}"]
    for chiave, nome in (("anelli_strutturali", "anelli"), ("ingressi", "ingressi"),
                         ("vicoli_vuoti", "vicoli vuoti"), ("copertura", "copertura"),
                         ("distanza_min_m", "PG-nemici m"), ("strozzatura", "strozzatura"),
                         ("celle_per_creatura", "celle/creatura"), ("flipmat", "Flip-Mat")):
        v = m.get(chiave)
        if v is None:
            continue
        parti.append(f"{nome} {v:.0%}" if chiave == "copertura" else f"{nome} {v}")
    return " · ".join(parti)


def classifica(esiti: list[Qualita]) -> str:
    """La tabella dal peggiore; le copie identiche di una griglia su una riga."""
    gruppi: dict = {}
    for q in esiti:
        gruppi.setdefault(q.impronta(), []).append(q)
    righe = ["| # | Voto | Banda | Mappa | Copie | Rilievi principali |", "|---|---:|---|---|---:|---|"]
    ordinati = sorted(gruppi.values(), key=lambda qs: (qs[0].voto(), qs[0].G.g["title"]))
    for i, qs in enumerate(ordinati, 1):
        q = qs[0]
        cod = Counter(r["codice"] for r in q.rilievi + q.c.rilievi if not r["deroga"])
        top = ", ".join(f"{k}×{v}" if v > 1 else k for k, v in cod.most_common(4))
        titolo = q.G.g["title"][:60].replace("|", "/")
        righe.append(f"| {i} | {q.voto()} | {banda(q.voto())} | {titolo} | {len(qs)} | {top or '—'} |")
    return "\n".join(righe)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="Exit: 0 rapporto · 1 rilievi E con --strict · 2 errore d'uso")
    ap.add_argument("files", nargs="*", help="master markdown da misurare (default: il corpus)")
    ap.add_argument("--json", metavar="OUT", help="scrive metriche, rilievi e voto in JSON")
    ap.add_argument("--classifica", action="store_true",
                    help="stampa la tabella markdown dal voto peggiore, copie identiche unite")
    ap.add_argument("--strict", action="store_true", help="esce 1 se resta un rilievo E non derogato")
    ap.add_argument("--solo-errori", action="store_true", help="nel testo mostra solo i rilievi E")
    ap.add_argument("--profonde", action="store_true",
                    help="aggiunge al JSON le metriche profonde (space syntax, simmetria, pattern 2x2): "
                         "senza soglia, fuori dal voto; vuole --json")
    args = ap.parse_args(argv)
    if args.profonde and not args.json:
        ap.error("--profonde scrive solo nel JSON: aggiungi --json OUT")

    try:
        C._dipendenze()
    except ImportError:
        print("✗ qualita_mappe ha bisogno di tcod, scipy e numpy (ADR-0084): "
              "pip install -r requirements-dev.txt", file=sys.stderr)
        return 2
    file = C.bersagli(args.files)
    mancanti = [f for f in file if not f.exists()]
    if mancanti:
        print(f"✗ file non trovato: {mancanti[0]}", file=sys.stderr)
        return 2
    corpus: dict = {}
    esiti: list[Qualita] = []
    for f in file:
        try:
            esiti += misura(f, corpus)
        except (UnicodeDecodeError, OSError):
            continue
    confronta_luoghi(esiti)

    errori = sum(1 for q in esiti for r in q.rilievi if r["classe"] == "E" and not r["deroga"])
    avvisi = sum(1 for q in esiti for r in q.rilievi if r["classe"] == "A" and not r["deroga"])
    if args.classifica:
        print(classifica(esiti))
    else:
        for q in esiti:
            mostra = [r for r in q.rilievi if not args.solo_errori or r["classe"] == "E"]
            if args.solo_errori and not mostra:
                continue
            d = q.c.come_dato()
            print(f"\n{d['file']} · mappa {q.c.indice} · {q.G.g['title'][:60]}"
                  f" · voto {q.voto()} ({banda(q.voto())})")
            if not args.solo_errori:
                print(f"  {_riga_metriche(q.m)}")
            for r in mostra:
                dove = f" {r['cella']}" if r["cella"] else ""
                dero = f"  (deroga: {r['deroga']})" if r["deroga"] else ""
                print(f"  {r['classe']} {r['codice']}{dove}: {r['messaggio']}{dero}")
    voti = [q.voto() for q in esiti]
    media = sum(voti) / len(voti) if voti else 0
    print(f"\nqualita_mappe: {len(esiti)} mappe · {errori} errori · {avvisi} avvisi · voto medio {media:.0f}"
          " · soglie in references/standard-qualita-mappe.md", file=sys.stderr if args.classifica else sys.stdout)
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"schema": "map_quality/1", "mappe": [q.come_dato(args.profonde) for q in esiti]},
            ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 1 if args.strict and errori else 0


if __name__ == "__main__":
    sys.exit(main())
