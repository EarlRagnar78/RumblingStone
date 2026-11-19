"""Misura dei rimandi fra capitoli in un booklet stampato (prova del 2026-11-19).

Per ogni «cap. V Scena 6», «capitolo III, §8», «il §13 del capitolo III» nel
testo del PDF dice: il capitolo esiste? il titolo citato sta dentro quel
capitolo (dai segnalibri)? il rimando porta il numero di pagina giusto?

    python3 misura_rimandi.py VOLUME-STAMPA.pdf [--elenco]
"""
import re
import sys

import pymupdf

ROM = r"(?P<rom>[IVXLC]+)\b"
CHIAVE = (r"(?P<key>§\d+(?:\.\d+)?(?:-(?:bis|ter))?|Scen[ae]\s+\d+(?:\s*(?:e|-|–)\s*\d+)?|[Aa]ppendice\s+[A-Z](?:\.\d+)?|«[^»]{3,60}»)")
AVANTI = re.compile(r"(?<!\w)(?:capp?\.|capitol[oi])\s+" + ROM + r"(?:,?\s+" + CHIAVE + r"(?![\w-]))?(?P<pag>,\s*p\.\s*(?P<n>\d+))?")
INDIETRO = re.compile(r"(?<![\w§])" + CHIAVE + r"\s+(?:del|di)\s+(?:capp?\.|capitolo)\s+" + ROM + r"(?P<pag>,\s*p\.\s*(?P<n>\d+))?")


def norm(s):
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("­", "")).strip().upper()


def chiave(k):
    k = re.sub(r"\s+", " ", k)
    if m := re.match(r"[Ss]cen[ae] (\d+)", k):
        return [f"SCENA {m.group(1)}"]
    if m := re.match(r"[Aa]ppendice ([A-Z](?:\.\d+)?)", k):
        return [m.group(1)]
    k = k.strip("«»")
    return [k, k[1:] + "."] if k.startswith("§") else [k]


def inizia(t, k):
    t, k = norm(t), norm(k)
    return t.startswith(k) and (len(t) == len(k) or not re.match(r"[\w-]", t[len(k)]))


def main(pdf, elenco=False):
    d = pymupdf.open(pdf)
    capitoli = {}   # rom -> (pagina, [(titolo, pagina)])
    attuale = None
    for lvl, t, p in d.get_toc():
        m = re.match(r"([IVXLC]+) ·", t)
        if lvl == 1 and m:
            attuale = m.group(1)
            capitoli[attuale] = (p, [])
        elif lvl == 1 and re.match(r"(Appendice:|Indice|Dove siamo|Il foglio)", t):
            attuale = None
        elif attuale:
            capitoli[attuale][1].append((t, p))
    testo = re.sub(r"-\s*\n\s*", "", "\n".join(pg.get_text() for pg in d))
    testo = re.sub(r"\s+", " ", testo.replace("­", ""))
    tot = senza_cap = sbagliati = con_pag = pag_giuste = 0
    righe = []
    presi = [(m.start(), m.end()) for m in INDIETRO.finditer(testo)]
    trovati_tutti = list(INDIETRO.finditer(testo)) + [
        m for m in AVANTI.finditer(testo) if not any(a <= m.start() < b for a, b in presi)]
    if True:
        for m in trovati_tutti:
            rom, key = m.group("rom"), m.group("key")
            tot += 1
            if rom not in capitoli:
                senza_cap += 1
                righe.append(("capitolo assente", m.group(0)))
                continue
            p_cap, titoli = capitoli[rom]
            atteso = p_cap
            if key:
                trovati = [p for t, p in titoli if any(inizia(t, k) for k in chiave(key))]
                if not trovati:
                    sbagliati += 1
                    righe.append(("titolo non nel capitolo", m.group(0)))
                    continue
                atteso = trovati[0]
            # senza titolo citato vale qualunque pagina del capitolo (la scheda,
            # la pagina delle mappe): fino all'apertura del capitolo dopo
            fine = min([p for p, _ in capitoli.values() if p > p_cap], default=10**6)
            if m.group("pag"):
                con_pag += 1
                n = int(m.group("n"))
                if n == atteso or (not key and p_cap <= n < fine):
                    pag_giuste += 1
                else:
                    righe.append((f"pagina {m.group('n')} invece di {atteso}", m.group(0)))
    print(f"{pdf.split('/')[-1]}: rimandi {tot} · capitolo assente {senza_cap} · "
          f"titolo non in quel capitolo {sbagliati} · con pagina {con_pag} · pagina giusta {pag_giuste}")
    if elenco:
        for c, r in righe:
            print(f"  {c:28} {r}")


if __name__ == "__main__":
    main(sys.argv[1], "--elenco" in sys.argv)
