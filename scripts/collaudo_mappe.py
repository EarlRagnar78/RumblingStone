#!/usr/bin/env python3
"""
collaudo_mappe.py — la mappa si collauda come grafo prima che come immagine (ADR-0082).

Legge le griglie-emoji dei master con il parser del renderer e la legenda
funzionale (``scripts/legend.json``, ADR-0048), costruisce il grafo delle celle
percorribili con le regole di movimento dell'SRD (diagonale 5-10-5, niente
diagonale oltre l'angolo di un muro) e risponde alle domande che nessun altro
script fa: ci si arriva? la porta sta nel muro? la scala ha la sua gemella? ci
passa una creatura Grande? la versione per i giocatori mostra un segreto?

Due classi di rilievo (ADR-0082 §3, D3 di PIANO-COLLAUDO-E-GENERAZIONE-MAPPE):

  E · errore   un fatto che non dipende dal gusto. Conta nella «distanza dalla
               giocabilita'» ed entrera' in CI a tetto (lotto V4).
  A · avviso   un'opinione informata: soglie euristiche finche' non calibrate.
               Non blocca mai.

Direttive nella griglia (righe che iniziano con ``@``; il renderer le ignora):

  @tipo tattica|strategica|schema      una vista strategica o uno schema non
                                       riceve i controlli tattici
  @deroga <codice> ; <motivo>          sospende un codice su questa mappa; un
                                       motivo sotto i 15 caratteri vale assente
  @collega <A1> ; <file.md>[#N] <A1>   una tessera fra livelli e la sua gemella
                                       (N = numero della mappa nel file, da 1)
  @collega <A1> ; fuori mappa ; <motivo>  il livello collegato non ha una
                                       griglia; motivo di almeno 15 caratteri
  @taglia <A1> ; Grande|Enorme         la creatura in quella cella non e' Media
  @vista giocatori                     la versione per i giocatori (D9)
  @north <dir>                         il nord, obbligatorio nelle tattiche

Uso:
    python3 scripts/collaudo_mappe.py                 # tutto il corpus
    python3 scripts/collaudo_mappe.py FILE.md [...]   # solo questi master
    python3 scripts/collaudo_mappe.py --json OUT.json # rapporto per macchine
    python3 scripts/collaudo_mappe.py --strict FILE   # esce 1 se c'e' un E

Exit: 0 rapporto prodotto (anche con rilievi) · 1 rilievi E con --strict ·
2 errore d'uso. Solo libreria standard; nessuna scrittura nel repo.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, deque
from pathlib import Path

RADICE = Path(__file__).resolve().parent
REPO = RADICE.parent
sys.path.insert(0, str(RADICE))
import render_map_svg as R  # noqa: E402
from dmcore import chiusure, legenda  # noqa: E402

LEG = json.loads(legenda.DERIVATO.read_text(encoding="utf-8"))["symbols"]
F = {s: v.get("function", {}) for s, v in LEG.items()}
MODO = {s: v["render"]["mode"] for s, v in LEG.items()}

# Il corpus della campagna: niente derivati generati, archivi, fixture ed esempi.
ESCLUSI = ("/.git/", "/build/", "/node_modules/", "/.claude/", "/pregen-pcgen/",
           ".hb.md", "_ARCHIVIO", "_SNAPSHOT", "/scripts/", "/docs/")

# Pesi della distanza dalla giocabilita' (FI-2Pop, ADR-0082 §7). Euristici e
# dichiarati: dicono quale errore pesa di piu', non quanto vale una mappa.
PESI = {
    "simbolo/ignoto": 1,
    "legenda/funzione-opposta": 5,
    "nord/mancante": 1,
    "posa/nel-muro": 3,
    "posa/fra-livelli": 5,
    "posa/solo-master": 10,
    "posa/verso-illeggibile": 1,
    "tipo/illeggibile": 1,
    "raggiungibile/unita": 5,
    "raggiungibile/obiettivo": 5,
}
CLASSE = {codice: "E" for codice in PESI}
CLASSE.update({
    "zone/separate": "A",
    "ingombro/grande": "A",
    "posa/sul-pavimento": "A",
    "posa/recinto": "A",
    "posa/asse-ambiguo": "A",
    "posa/verso-contro-muri": "A",
    "m1/copertura": "A",
    "m2/vuoto": "A",
    "m4/esposizione": "A",
    "tipo/mancante": "A",
})
TATTICI = {"nord/mancante", "posa/nel-muro", "posa/recinto", "posa/sul-pavimento",
           "posa/asse-ambiguo", "posa/verso-contro-muri",
           "raggiungibile/unita", "raggiungibile/obiettivo", "zone/separate",
           "ingombro/grande", "m1/copertura", "m2/vuoto", "m4/esposizione"}
OBIETTIVI = {"⭐", "🎯", "💎", "🏺", "🧰"}
INGOMBRO = {"grande": 2, "enorme": 3}
FUORI = "FUORI"
MOTIVO_MINIMO = 15


def _dipendenze():
    """numpy, tcod e scipy.ndimage: obbligatorie per il collaudo (ADR-0084),
    che gira in CI e nelle mani di chi disegna, non al tavolo. Importate qui
    perche' chi importa il modulo per il resto (i test, l'MCP) non le paghi."""
    import numpy
    import tcod
    import tcod.map  # noqa: F401
    from scipy import ndimage
    return numpy, tcod, ndimage


def n(c):
    return c.replace("️", "") if c else c


def a1(x: int, y: int, righe: list[int]) -> str:
    return f"{R.col_label(x)}{righe[y]:02d}"


def _cella(token: str, righe: list[int]):
    """'D16' -> (x, y) nell'indice della griglia letta, o None."""
    m = re.fullmatch(r"([A-Za-z]{1,2})(\d{1,3})", token.strip())
    if not m:
        return None
    x = R.col_index(m.group(1))
    num = int(m.group(2))
    if num not in righe:
        return None
    return x, righe.index(num)


def direttive(annotazioni: list[str]) -> dict:
    d = {"tipo": None, "ambiente": None, "tipo_grezzo": None, "deroghe": {}, "collega": [],
         "taglia": [], "giocatori": False, "north": False}
    for riga in annotazioni:
        s = riga.strip()
        tipo, _, resto = s[1:].partition(" ")
        tipo = tipo.lower()
        parti = [p.strip() for p in resto.split(";")]
        if tipo == "tipo":
            # `@tipo tattica caverna`: il tipo decide i controlli, l'ambiente il corredo
            parole = resto.strip().lower().split()
            d["tipo_grezzo"] = resto.strip() or None
            d["tipo"] = parole[0] if parole else None
            d["ambiente"] = parole[1] if len(parole) > 1 else None
        elif tipo == "deroga" and parti and parti[0]:
            d["deroghe"][parti[0]] = parti[1] if len(parti) > 1 else ""
        elif tipo == "collega" and len(parti) >= 2:
            # (cella, gemella, motivo): il motivo serve solo a «fuori mappa»
            d["collega"].append((parti[0], parti[1], parti[2] if len(parti) > 2 else ""))
        elif tipo == "taglia" and len(parti) >= 2:
            d["taglia"].append((parti[0], parti[1].lower()))
        elif tipo == "vista" and resto.strip().lower().startswith("giocator"):
            d["giocatori"] = True
        elif tipo == "north":
            d["north"] = True
    return d


class Griglia:
    def __init__(self, g: dict):
        self.g = g
        self.righe = sorted(g["rows"])
        self.celle = [[n(c) for c in g["rows"][k]] for k in self.righe]
        self.H = len(self.celle)
        self.W = max(len(r) for r in self.celle)
        self.locali = {n(k): v for k, v in g["local_legend"].items()}

    def at(self, x: int, y: int):
        if not (0 <= y < self.H and 0 <= x < len(self.celle[y])):
            return FUORI
        return self.celle[y][x]

    def tutte(self):
        for y in range(self.H):
            for x in range(len(self.celle[y])):
                yield x, y, self.celle[y][x]


def porta(c) -> bool:
    return c not in (None, FUORI) and bool(F.get(c, {}).get("door"))


def blocca(c) -> bool:
    """Blocca il movimento. Le porte si considerano aperte."""
    return c not in (None, FUORI) and bool(F.get(c, {}).get("blocks_movement")) and not porta(c)


def murario(c) -> bool:
    """Un muro vero: blocca movimento e vista, e non e' un varco."""
    if c == FUORI:
        return True
    f = F.get(c, {})
    return bool(f.get("blocks_movement")) and bool(f.get("blocks_sight")) and not f.get("door")


def angolo(c) -> bool:
    """Ferma la diagonale (SRD): un muro si', una fossa o una creatura no."""
    return murario(c) and c != FUORI


class Collaudo:
    def __init__(self, file: Path, indice: int, g: dict, corpus: dict):
        self.file = file
        self.indice = indice
        self.G = Griglia(g)
        self.d = direttive(g["annotations"])
        self.corpus = corpus
        self.rilievi: list[dict] = []
        self.assi: Counter = Counter()
        # un tipo che non si legge non spegne i controlli: resta tattica
        self.tattica = self.d["tipo"] not in ("strategica", "schema")

    # --- grafo ---------------------------------------------------------------
    def percorribili(self) -> set:
        return {(x, y) for x, y, c in self.G.tutte() if not blocca(c)}

    def vicini(self, x, y, perc):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0 or (x + dx, y + dy) not in perc:
                    continue
                if dx and dy and (angolo(self.G.at(x + dx, y)) or angolo(self.G.at(x, y + dy))):
                    continue
                yield x + dx, y + dy

    def componenti(self, perc) -> dict:
        comp, k = {}, 0
        for c in sorted(perc):
            if c in comp:
                continue
            comp[c] = k
            coda = deque([c])
            while coda:
                a = coda.popleft()
                for b in self.vicini(*a, perc):
                    if b not in comp:
                        comp[b] = k
                        coda.append(b)
            k += 1
        return comp

    # --- rilievi ---------------------------------------------------------------
    def rileva(self, codice: str, cella, messaggio: str):
        if codice in TATTICI and not self.tattica:
            return
        motivo = self.d["deroghe"].get(codice)
        derogato = motivo is not None and len(motivo) >= MOTIVO_MINIMO
        self.rilievi.append({
            "codice": codice, "classe": CLASSE[codice],
            "cella": a1(*cella, self.G.righe) if cella else None,
            "messaggio": messaggio,
            "deroga": motivo if derogato else None,
        })

    def esegui(self) -> "Collaudo":
        G = self.G
        perc = self.percorribili()
        comp = self.componenti(perc)

        # simboli e legenda
        ignoti = Counter()
        for x, y, c in G.tutte():
            if c not in F and c not in G.locali and MODO.get(c) != "unit":
                ignoti[c] += 1
                if ignoti[c] == 1:
                    self.rileva("simbolo/ignoto", (x, y),
                                f"«{c}» non e' nella legenda universale ne' in quella locale")
        for k, v in G.locali.items():
            if k not in F:
                continue
            f, low = F[k], v.lower()
            if (f.get("blocks_movement") and not f.get("door")
                    and re.search(r"paviment|terra|passagg|corridoio|sentiero|strada|impronta", low)) or \
               (not f.get("blocks_movement") and re.search(r"\bmur|parete|pilastr|colonn", low)):
                self.rileva("legenda/funzione-opposta", None,
                            f"la legenda locale dice «{k} = {v[:50]}», la universale "
                            f"«{LEG[k].get('label', '')}»: si cambia il simbolo, non la legenda")

        if not self.d["tipo"]:
            self.rileva("tipo/mancante", None,
                        "la mappa non dichiara @tipo: si collauda come tattica. "
                        f"@tipo <{'|'.join(legenda.TIPI_MAPPA)}> [{'|'.join(legenda.AMBIENTI_MAPPA)}]")
        elif (self.d["tipo"] not in legenda.TIPI_MAPPA
              or (self.d["ambiente"] and self.d["ambiente"] not in legenda.AMBIENTI_MAPPA)):
            self.rileva("tipo/illeggibile", None,
                        f"@tipo {self.d['tipo_grezzo']}: il tipo e' uno di {', '.join(legenda.TIPI_MAPPA)}, "
                        f"l'ambiente uno di {', '.join(legenda.AMBIENTI_MAPPA)}")

        if not self.d["north"]:
            self.rileva("nord/mancante", None,
                        "la mappa tattica non dichiara @north: il nord e' implicito in alto")

        # posa · una fila di porte (🚪🚪🚪) e' un varco solo: si collauda una volta
        file_viste: set = set()
        for x, y, c in G.tutte():
            f = F.get(c, {})
            posa = f.get("posa")
            if posa == "nel_muro" and (x, y) not in file_viste:
                fila = self._fila(x, y)
                file_viste |= fila
                self._nel_muro(x, y, c, fila)
            elif posa == "fra_livelli":
                self._fra_livelli(x, y, c)
            elif posa == "sul_pavimento" and f.get("blocks_movement"):
                vic = {comp[p] for p in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)) if p in comp}
                if len(vic) > 1:
                    self.rileva("posa/sul-pavimento", (x, y),
                                f"«{c}» separa due zone percorribili: chiude l'unico varco")
            if f.get("solo_master") and self.d["giocatori"]:
                self.rileva("posa/solo-master", (x, y),
                            f"«{c}» compare nella versione per i giocatori (D9): va disegnata come muro")
        self._recinti(perc, comp)
        self._assi(self.G.g.get("annotations", []))

        # raggiungibilita'
        taglie = Counter(comp[c] for c in perc)
        grandi = [k for k, t in taglie.items() if t >= 4]
        if len(grandi) > 1:
            self.rileva("zone/separate", None,
                        f"{len(grandi)} zone percorribili non collegate (>= 4 celle ciascuna)")
        pg = [(x, y) for x, y, c in G.tutte() if c == "🔵"]
        base = {comp[p] for p in pg if p in comp} or ({max(taglie, key=taglie.get)} if taglie else set())
        isolate: dict = {}
        for x, y, c in G.tutte():
            if (x, y) not in comp or comp[(x, y)] in base:
                continue
            if (MODO.get(c) == "unit" and c != "🔵") or c in OBIETTIVI:
                tipo = "obiettivo" if c in OBIETTIVI else "unita"
                isolate.setdefault((tipo, comp[(x, y)]), []).append((x, y, c))
        for (tipo, _zona), celle in sorted(isolate.items(), key=lambda kv: kv[1][0][1:2] + kv[1][0][0:1]):
            x, y, c = celle[0]
            simboli = "".join(sorted({cc for _, _, cc in celle}))
            if tipo == "unita":
                self.rileva("raggiungibile/unita", (x, y),
                            f"{len(celle)} unita' ({simboli}) in una zona che i PG non raggiungono")
            else:
                self.rileva("raggiungibile/obiettivo", (x, y),
                            f"{len(celle)} obiettivi ({simboli}) che non si raggiungono dalla zona dei PG")
        self._taglie(perc, base, comp)

        # metriche dell'audit (solo mappe >= 12x12)
        if G.W >= 12 and G.H >= 12 and perc:
            m1, m2 = self._copertura_e_vuoto(perc)
            if m1 < 0.60:
                self.rileva("m1/copertura", None,
                            f"M1 = {m1:.2f}: solo il {m1:.0%} del percorribile ha una copertura entro "
                            "2 quadretti (soglia euristica 0,60, non calibrata)")
            if m2 > 0.20:
                self.rileva("m2/vuoto", None,
                            f"M2 = {m2:.2f}: il piu' grande spazio aperto senza coperture e' il "
                            f"{m2:.0%} del percorribile (soglia euristica 0,20, non calibrata)")
            m4 = self._esposizione(perc)
            if m4 is not None and m4 > 0.45:
                self.rileva("m4/esposizione", None,
                            f"M4 = {m4:.2f}: da una cella qualunque si vede in media il {m4:.0%} "
                            "del percorribile (soglia euristica 0,45, non calibrata)")
        return self

    def _assi(self, annotazioni):
        """L'asse di ogni chiusura (ADR-0083): lo stesso dato che il renderer
        e l'export UVTT usano per disegnarla."""
        G = self.G

        def at(x, y):
            c = G.at(x, y)
            return None if c == FUORI else c
        dichiarati = chiusure.versi_dichiarati(annotazioni)
        for riga in chiusure.verso_illeggibile(annotazioni):
            self.rileva("posa/verso-illeggibile", None,
                        f"«{riga}» non si legge: @verso <cella> ; NS|EO")
        visti = set()
        for x, y, c in G.tutte():
            if not chiusure.e_chiusura(c):
                continue
            chiave = (R.col_label(x).upper(), G.righe[y])
            visti.add(chiave)
            dai_muri = chiusure.asse(at, x, y)
            if chiave in dichiarati:
                self.assi["dichiarate"] += 1
                if dai_muri in (chiusure.EO, chiusure.NS) and dai_muri != dichiarati[chiave]:
                    self.rileva("posa/verso-contro-muri", (x, y),
                                f"«{c}»: @verso dice {dichiarati[chiave]}, i muri intorno dicono "
                                f"{dai_muri}. Vince la direttiva: e' davvero quello che vuoi?")
                continue
            if dai_muri == chiusure.AMBIGUO:
                self.assi["ambigue"] += 1
                self.rileva("posa/asse-ambiguo", (x, y),
                            f"«{c}» ha muri e passaggi su tutti e due gli assi: si disegna est-ovest. "
                            f"Se non va, @verso {a1(x, y, G.righe)} ; NS")
            elif dai_muri is None:
                self.assi["senza_muro"] += 1
            else:
                self.assi[dai_muri] += 1
        for col, riga in sorted(set(dichiarati) - visti):
            self.rileva("posa/verso-illeggibile", None,
                        f"@verso {col}{riga:02d}: in quella cella non c'e' una porta, una grata o sbarre")

    def _fila(self, x, y) -> set:
        fila, coda = {(x, y)}, deque([(x, y)])
        while coda:
            a, b = coda.popleft()
            for q in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                if q not in fila and F.get(self.G.at(*q), {}).get("posa") == "nel_muro":
                    fila.add(q)
                    coda.append(q)
        return fila

    def _nel_muro(self, x, y, c, fila=frozenset()):
        G = self.G
        fila = fila or {(x, y)}
        quante = f" (fila di {len(fila)})" if len(fila) > 1 else ""

        def capo(dx, dy):
            xx, yy = x, y
            while F.get(G.at(xx, yy), {}).get("posa") == "nel_muro":
                xx, yy = xx + dx, yy + dy
            return G.at(xx, yy)

        oriz = murario(capo(-1, 0)) and murario(capo(1, 0))
        vert = murario(capo(0, -1)) and murario(capo(0, 1))
        if not (oriz or vert):
            self.rileva("posa/nel-muro", (x, y), f"«{c}»{quante} non sta fra due muri (o un muro e il bordo)")
            return

        def lati(px, py):
            return [G.at(px, py - 1), G.at(px, py + 1)] if oriz else [G.at(px - 1, py), G.at(px + 1, py)]
        # una fila e' un varco solo: basta che una delle sue celle si attraversi
        if all(all(murario(s) or s == FUORI for s in lati(px, py)) for px, py in fila):
            self.rileva("posa/nel-muro", (x, y), f"«{c}»{quante} e' murata: nessuno dei due lati e' percorribile")

    def _fra_livelli(self, x, y, c):
        qui = a1(x, y, self.G.righe)
        # per posizione, non per stringa: «B2» e «B02» sono la stessa cella
        voci = [(dest, motivo) for orig, dest, motivo in self.d["collega"]
                if _cella(orig, self.G.righe) == (x, y)]
        if not voci:
            self.rileva("posa/fra-livelli", (x, y),
                        f"«{c}» non dichiara la sua gemella: manca @collega {qui} ; <file.md>[#N] <cella>")
            return
        verso = F[c].get("verso")
        for dest, motivo in voci:
            if dest.lower() == "fuori mappa":
                # D12: il livello 0 di Hammerfist non ha una griglia. Si dichiara, con
                # un motivo, come una deroga: senza, e' una scala che non porta a niente
                if len(motivo) < MOTIVO_MINIMO:
                    self.rileva("posa/fra-livelli", (x, y),
                                f"@collega {qui} ; fuori mappa: serve il motivo "
                                f"(almeno {MOTIVO_MINIMO} caratteri)")
                continue
            trovata, esito = self._gemella(dest)
            if not trovata:
                self.rileva("posa/fra-livelli", (x, y), f"@collega {qui}: {esito}")
                continue
            vg = F.get(esito, {}).get("verso")
            if esito != "🪜" and vg == verso:
                self.rileva("posa/fra-livelli", (x, y),
                            f"«{c}» ({verso}) e la gemella «{esito}» vanno nello stesso verso")

    def _gemella(self, dest: str) -> tuple[bool, str]:
        """(True, simbolo della gemella) oppure (False, perche' non c'e')."""
        m = re.fullmatch(r"(.+?)(?:#(\d+))?\s+([A-Za-z]{1,2}\d{1,3})", dest.strip())
        if not m:
            return False, f"destinazione illeggibile «{dest}»"
        nome, num, cella = m.group(1).strip(), int(m.group(2) or 1), m.group(3)
        if nome in ("stessa", "questa"):
            griglia = self.G
        else:
            percorso = (REPO / nome) if not Path(nome).is_absolute() else Path(nome)
            if not percorso.exists():
                percorso = self.file.parent / nome
            if not percorso.exists():
                return False, f"il file «{nome}» non esiste"
            mappe = self.corpus.get(percorso.resolve())
            if mappe is None:
                mappe = R.extract_maps(percorso.read_text(encoding="utf-8"))
                self.corpus[percorso.resolve()] = mappe
            if not (1 <= num <= len(mappe)):
                return False, f"«{nome}» non ha la mappa #{num}"
            griglia = Griglia(mappe[num - 1])
        pos = _cella(cella, griglia.righe)
        if not pos:
            return False, f"la cella {cella} non esiste nella mappa di destinazione"
        bersaglio = griglia.at(*pos)
        if bersaglio != "🪜" and F.get(bersaglio, {}).get("posa") != "fra_livelli":
            return False, f"in {cella} c'e' «{bersaglio}», non una scala, una botola o un pozzo"
        return True, bersaglio

    def _recinti(self, perc, comp):
        G = self.G
        zone_con_sbarre = set()
        for x, y, c in G.tutte():
            if F.get(c, {}).get("posa") == "recinto":
                for p in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if p in comp:
                        zone_con_sbarre.add(comp[p])
        if len(zone_con_sbarre) < 2:
            return  # le sbarre non separano niente: nessun recinto da collaudare
        for k in sorted(zone_con_sbarre):
            celle = [p for p, v in comp.items() if v == k]
            varchi = any(porta(G.at(px + a, py + b)) for px, py in celle
                         for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if not varchi:
                x, y = celle[0]
                self.rileva("posa/recinto", (x, y),
                            "una zona chiusa da sbarre non ha porta ne' grata: cella murata?")

    def _taglie(self, perc, base, comp):
        G = self.G
        for coord, taglia in self.d["taglia"]:
            lato = INGOMBRO.get(taglia.split()[0] if taglia else "")
            pos = _cella(coord, G.righe)
            if not lato or not pos:
                continue
            ok = self._ingombro_raggiunge(pos, lato, perc, base, comp)
            if not ok:
                self.rileva("ingombro/grande", pos,
                            f"una creatura {taglia} in {coord} non raggiunge la zona dei PG "
                            f"con un ingombro di {lato}×{lato}")

    def _ingombro_raggiunge(self, pos, lato, perc, base, comp) -> bool:
        def libero(x, y):
            return all((x + i, y + j) in perc for i in range(lato) for j in range(lato))
        partenze = [(pos[0] - i, pos[1] - j) for i in range(lato) for j in range(lato)
                    if libero(pos[0] - i, pos[1] - j)]
        visti, coda = set(partenze), deque(partenze)
        while coda:
            x, y = coda.popleft()
            for i in range(lato):
                for j in range(lato):
                    if comp.get((x + i, y + j)) in base and self.G.at(x + i, y + j) == "🔵":
                        return True
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + dx, y + dy)
                if q not in visti and libero(*q):
                    visti.add(q)
                    coda.append(q)
        return not any(self.G.at(x, y) == "🔵" for x, y, _ in self.G.tutte())

    def _esposizione(self, perc) -> float | None:
        """M4 esatta (ADR-0084): da ogni cella percorribile, la frazione del
        percorribile che si vede, con lo shadowcasting simmetrico di tcod.
        Nessun campionamento: tutte le celle, ogni volta."""
        np, tcod, _ = _dipendenze()
        G = self.G
        trasp = np.array([[not F.get(G.at(x, y), {}).get("blocks_sight") and G.at(x, y) != FUORI
                           for x in range(G.W)] for y in range(G.H)], dtype=bool)
        maschera = np.zeros((G.H, G.W), dtype=bool)
        for x, y in perc:
            maschera[y, x] = True
        origini = [(x, y) for x, y in perc if trasp[y, x]]
        if not origini:
            return None
        totale = int(maschera.sum())
        somma = 0
        for x, y in origini:
            vista = tcod.map.compute_fov(trasp, (y, x), radius=0, light_walls=True,
                                         algorithm=tcod.constants.FOV_SYMMETRIC_SHADOWCAST)
            somma += int((vista & maschera).sum())
        return somma / (len(origini) * totale)

    def _copertura_e_vuoto(self, perc) -> tuple[float, float]:
        """M1 e M2 con scipy.ndimage (ADR-0084): M1 la frazione del percorribile
        con una copertura entro 2 quadretti (Chebyshev), M2 il piu' grande
        spazio aperto senza coperture, a 4-connessione. Stesso risultato del
        calcolo a mano di prima, sei volte piu' veloce."""
        np, _, ndimage = _dipendenze()
        G = self.G
        P = np.zeros((G.H, G.W), dtype=bool)
        K = np.zeros((G.H, G.W), dtype=bool)
        for x, y, c in G.tutte():
            if F.get(c, {}).get("cover") in ("half", "three_quarters", "total"):
                K[y, x] = True
        for x, y in perc:
            P[y, x] = True
        vicino = ndimage.binary_dilation(K, structure=np.ones((5, 5), dtype=bool)) & P
        etichette, quante = ndimage.label(P & ~vicino)
        piu = int(np.bincount(etichette.ravel())[1:].max()) if quante else 0
        totale = int(P.sum())
        return int(vicino.sum()) / totale, piu / totale

    def distanza(self) -> int:
        return sum(PESI[r["codice"]] for r in self.rilievi
                   if r["classe"] == "E" and not r["deroga"])

    def come_dato(self) -> dict:
        return {"file": str(self.file.relative_to(REPO)) if self.file.is_relative_to(REPO) else str(self.file),
                "mappa": self.indice, "titolo": self.G.g["title"][:90],
                "tipo": self.d["tipo"] or "tattica (implicita)",
                "ambiente": self.d["ambiente"],
                "dimensioni": [self.G.W, self.G.H],
                "distanza_giocabilita": self.distanza(),
                "chiusure": {k: self.assi.get(k, 0)
                             for k in ("EO", "NS", "ambigue", "senza_muro", "dichiarate")},
                "rilievi": self.rilievi}


def bersagli(argomenti: list[str]) -> list[Path]:
    if argomenti:
        return [Path(a).resolve() for a in argomenti]
    return sorted(p for p in REPO.rglob("*.md") if not any(s in str(p) for s in ESCLUSI))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="Exit: 0 rapporto · 1 rilievi E con --strict · 2 errore d'uso")
    ap.add_argument("files", nargs="*", help="master markdown da collaudare (default: il corpus)")
    ap.add_argument("--json", metavar="OUT", help="scrive il rapporto in JSON (map_findings.schema.json)")
    ap.add_argument("--strict", action="store_true", help="esce 1 se resta un rilievo E non derogato")
    ap.add_argument("--solo-errori", action="store_true", help="nel testo mostra solo i rilievi E")
    args = ap.parse_args(argv)

    try:
        _dipendenze()
    except ImportError:
        print("✗ collaudo_mappe ha bisogno di tcod, scipy e numpy (ADR-0084): "
              "pip install -r requirements-dev.txt", file=sys.stderr)
        return 2
    file = bersagli(args.files)
    mancanti = [f for f in file if not f.exists()]
    if mancanti:
        print(f"✗ file non trovato: {mancanti[0]}", file=sys.stderr)
        return 2
    corpus: dict = {}
    esiti = []
    for f in file:
        try:
            testo = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        mappe = R.extract_maps(testo)
        corpus[f.resolve()] = mappe
        for i, g in enumerate(mappe, 1):
            esiti.append(Collaudo(f, i, g, corpus).esegui())

    errori = sum(1 for e in esiti for r in e.rilievi if r["classe"] == "E" and not r["deroga"])
    avvisi = sum(1 for e in esiti for r in e.rilievi if r["classe"] == "A" and not r["deroga"])
    for e in esiti:
        mostra = [r for r in e.rilievi if not args.solo_errori or r["classe"] == "E"]
        if not mostra:
            continue
        print(f"\n{e.come_dato()['file']} · mappa {e.indice} · {e.G.g['title'][:60]}"
              f" · distanza {e.distanza()}")
        for r in mostra:
            dove = f" {r['cella']}" if r["cella"] else ""
            dero = f"  (deroga: {r['deroga']})" if r["deroga"] else ""
            print(f"  {r['classe']} {r['codice']}{dove}: {r['messaggio']}{dero}")
    print(f"\ncollaudo_mappe: {len(esiti)} mappe · {errori} errori · {avvisi} avvisi"
          " · le soglie M1, M2 e M4 sono euristiche, non calibrate")
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"schema": "map_findings/1", "mappe": [e.come_dato() for e in esiti]},
            ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 1 if args.strict and errori else 0


if __name__ == "__main__":
    sys.exit(main())
