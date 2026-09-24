#!/usr/bin/env python3
"""validate_tipografia.py — tre misure sull'artefatto, non sulle intenzioni.

Lotto G2. Le prime due catene del repo controllano che il volume **compili**;
nessuna controlla che sia **leggibile**. Sono cose diverse, e la seconda non si
vede da un exit code.

    1. gerarchia dei titoli   nessun livello salta il precedente
    2. caratteri per riga     misurati sulle metriche VERE del font
    3. daltonismo             due colori distinti che diventano lo stesso

Perche' proprio queste tre. Ognuna nasce da un difetto trovato davvero:

**Gerarchia.** Nell'HTML dell'Abbazia una voce d'area era un `<h4>` sotto un
`<h2>`: una scelta *visiva* — un titolo piu' piccolo. In un documento strutturato
e' un ramo dell'albero che non esiste, e si vede nei **segnalibri del PDF**, che
sono la ragione per cui ADR-0020 esiste. veraPDF lo dice con le stesse parole
(PDF/UA 7.4.2-1) sugli stessi tre punti: due misure indipendenti, stesso numero.

**Caratteri per riga.** La misura tipografica classica (45-75 per colonna; sotto
i 45 il testo si spezza, sopra i 75 l'occhio perde la riga di ritorno). Non si
stima: si calcola dalla **larghezza di colonna** del tema e dalle **avanzate
reali** dei glifi, lette dalla tabella `hmtx` del font che stiamo davvero
incorporando. Un font cambiato o un corpo ritoccato lo spostano, e nessuno se ne
accorgerebbe fino alla stampa.

**Daltonismo.** Circa un uomo su dodici non distingue rosso e verde. Una mappa
che usa il rosso per «nemico» e il verde per «alleato» funziona per undici
persone su dodici e per la dodicesima e' una mappa senza informazione. Si
simulano le tre dicromazie e si cercano le coppie di colori che nella visione
normale sono distinte e nella simulazione collassano.

Uso:

    python3 scripts/validate_tipografia.py                 # tutto
    python3 scripts/validate_tipografia.py --solo titoli   # titoli|righe|colori
    python3 scripts/validate_tipografia.py --strict        # i rilievi diventano errori

⚠️ **Non bloccante alla prima passata**, come `validate_lingua` e
`validate_bestiario --rules`: un gate rumoroso viene disattivato entro una
settimana, e allora non trova piu' nemmeno i difetti veri.

Solo stdlib.
"""
from __future__ import annotations

import argparse
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --- 1. gerarchia -----------------------------------------------------------
# ⚠️ Il perimetro e' **i capitoli dichiarati in un manifest**, non tutto il
# markdown del repo. La ragione del controllo sono i segnalibri del PDF, e un
# file che non entra in nessuna catena non ha segnalibri: segnalarlo sarebbe
# chiedere di sistemare qualcosa per cui non esiste un artefatto.
# Fuori restano anche i `#####` dei `.hb.md`, che nello stile Homebrewery sono
# etichette piccole e non titoli — punirli vorrebbe dire punire una convenzione.

# --- 2. caratteri per riga --------------------------------------------------
# I numeri del tema (`scripts/typst/tema-rumblingstone.typ`). Stanno qui perche'
# un .typ non si importa da Python; il test li riconfronta col file, cosi' se il
# tema cambia e questi no, il controllo diventa rosso invece che bugiardo.
PAGINA_MM = 210.0
MARGINE_INTERNO_MM, MARGINE_ESTERNO_MM = 20.0, 15.0
COLONNE = 2
GUTTER_MM = PAGINA_MM * 0.04      # default di Typst per `columns`
CORPO_PT = 10.2
FONT_TESTO = ROOT / "scripts" / "fonts" / "EBGaramond[wght].ttf"
#: Sotto i 45 il testo si spezza in singhiozzi; sopra i 75 l'occhio perde la riga
#: di ritorno. In due colonne si sta volentieri nella parte bassa.
CPL_MIN, CPL_MAX = 45.0, 75.0

# --- 3. daltonismo ----------------------------------------------------------
#: Matrici di simulazione (Viénot, Brettel & Mollon 1999) in spazio LMS.
DICROMAZIE = {
    "protanopia":   ((0.0, 2.02344, -2.52581), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
    "deuteranopia": ((1.0, 0.0, 0.0), (0.494207, 0.0, 1.24827), (0.0, 0.0, 1.0)),
    "tritanopia":   ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (-0.395913, 0.801109, 0.0)),
}
#: Sotto questa distanza due colori sono «lo stesso colore» a occhio.
SOGLIA_VICINI = 26.0
#: Un colore troppo simile a un altro *gia' in visione normale* non e' un
#: problema di daltonismo: e' una sfumatura voluta. Si guardano solo le coppie
#: che partono ben distinte.
SOGLIA_DISTINTI = 60.0


# ===========================================================================
# 1. Gerarchia dei titoli
# ===========================================================================
def salti_di_titolo(testo: str) -> list[tuple[int, int, int, str]]:
    """(riga, livello precedente, livello trovato, testo) per ogni salto."""
    fuori, prec, in_fence = [], 0, False
    for n, riga in enumerate(testo.splitlines(), 1):
        if riga.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6}) +(.*)$", riga)
        if not m:
            continue
        liv = len(m.group(1))
        if prec and liv > prec + 1:
            fuori.append((n, prec, liv, m.group(2)[:48]))
        prec = liv
    return fuori


def capitoli_impaginati() -> list[Path]:
    """I master markdown citati come capitolo da un manifest di volume."""
    import json
    fuori: set[Path] = set()
    for mp in sorted(ROOT.rglob("*.manifest.json")):
        try:
            man = json.loads(mp.read_text(encoding="utf-8"))
        except Exception:
            continue
        for c in man.get("chapters", []):
            f = (mp.parent / c.get("file", "")).resolve()
            if f.is_file() and f.suffix == ".md":
                fuori.add(f)
    return sorted(fuori)


def check_titoli(rilievi: list[str]) -> int:
    n = 0
    for f in capitoli_impaginati():
        rel = f.relative_to(ROOT)
        n += 1
        for riga, prec, liv, tit in salti_di_titolo(f.read_text(encoding="utf-8", errors="ignore")):
            rilievi.append(
                f"{rel}:{riga}: titolo h{liv} dopo h{prec} — salta h{prec + 1}. "
                f"Nei segnalibri del PDF diventa un ramo che non esiste  «{tit}»")
    return n


# ===========================================================================
# 2. Caratteri per riga
# ===========================================================================
def _tabelle(dati: bytes) -> dict[str, tuple[int, int]]:
    num = struct.unpack(">H", dati[4:6])[0]
    fuori = {}
    for i in range(num):
        o = 12 + i * 16
        tag = dati[o:o + 4].decode("latin-1")
        off, lung = struct.unpack(">II", dati[o + 8:o + 16])
        fuori[tag] = (off, lung)
    return fuori


def metriche(font: Path) -> tuple[int, dict[int, int]]:
    """(unitsPerEm, {codepoint: avanzata}) letti da `head`, `cmap` e `hmtx`.

    Niente librerie: sono tre tabelle e si leggono con `struct`. Il punto e'
    misurare **il font che incorporiamo davvero**, non uno simile.
    """
    d = font.read_bytes()
    t = _tabelle(d)
    upem = struct.unpack(">H", d[t["head"][0] + 18:t["head"][0] + 20])[0]
    n_hm = struct.unpack(">H", d[t["hhea"][0] + 34:t["hhea"][0] + 36])[0]
    hmtx = t["hmtx"][0]
    avanzate = [struct.unpack(">H", d[hmtx + i * 4:hmtx + i * 4 + 2])[0] for i in range(n_hm)]

    # cmap: si cerca un sottotavola formato 4 (BMP), che copre il latino.
    co = t["cmap"][0]
    n_sub = struct.unpack(">H", d[co + 2:co + 4])[0]
    mappa: dict[int, int] = {}
    for i in range(n_sub):
        pid, eid, off = struct.unpack(">HHI", d[co + 4 + i * 8:co + 12 + i * 8])
        s = co + off
        if struct.unpack(">H", d[s:s + 2])[0] != 4:
            continue
        seg2 = struct.unpack(">H", d[s + 6:s + 8])[0]
        seg = seg2 // 2
        fine = [struct.unpack(">H", d[s + 14 + j * 2:s + 16 + j * 2])[0] for j in range(seg)]
        inizio = [struct.unpack(">H", d[s + 16 + seg2 + j * 2:s + 18 + seg2 + j * 2])[0]
                  for j in range(seg)]
        delta = [struct.unpack(">h", d[s + 16 + seg2 * 2 + j * 2:s + 18 + seg2 * 2 + j * 2])[0]
                 for j in range(seg)]
        base_ro = s + 16 + seg2 * 3
        ro = [struct.unpack(">H", d[base_ro + j * 2:base_ro + 2 + j * 2])[0] for j in range(seg)]
        for j in range(seg):
            for c in range(inizio[j], min(fine[j], 0x2FFF) + 1):
                if ro[j] == 0:
                    g = (c + delta[j]) & 0xFFFF
                else:
                    pos = base_ro + j * 2 + ro[j] + (c - inizio[j]) * 2
                    if pos + 2 > len(d):
                        continue
                    g = struct.unpack(">H", d[pos:pos + 2])[0]
                    if g:
                        g = (g + delta[j]) & 0xFFFF
                if g:
                    mappa[c] = g
        break
    ultima = avanzate[-1] if avanzate else upem // 2
    return upem, {c: (avanzate[g] if g < len(avanzate) else ultima) for c, g in mappa.items()}


def larghezza_colonna_pt() -> float:
    utile = PAGINA_MM - MARGINE_INTERNO_MM - MARGINE_ESTERNO_MM
    return ((utile - GUTTER_MM * (COLONNE - 1)) / COLONNE) * 72.0 / 25.4


def caratteri_per_riga(campione: str, font: Path = FONT_TESTO,
                       corpo: float = CORPO_PT) -> tuple[float, float]:
    """(caratteri per riga, avanzata media in pt) su un campione di testo vero."""
    upem, av = metriche(font)
    usati = [av[ord(c)] for c in campione if ord(c) in av]
    if not usati:
        raise ValueError("nessun carattere del campione è nel font")
    media_pt = (sum(usati) / len(usati)) / upem * corpo
    return larghezza_colonna_pt() / media_pt, media_pt


def _campione_vero() -> str:
    """Prosa italiana del repo, non un pangramma: le frequenze contano."""
    pezzi = []
    for f in sorted(ROOT.glob("10-stand-alone/*/*.md")):
        t = re.sub(r"[`#*|>\[\]()!]", "", f.read_text(encoding="utf-8", errors="ignore"))
        pezzi.append(re.sub(r"\s+", " ", t))
        if sum(len(x) for x in pezzi) > 40000:
            break
    return "".join(pezzi) or "il mare ha restituito un corpo alla base della scogliera"


def check_righe(rilievi: list[str]) -> str:
    if not FONT_TESTO.is_file():
        rilievi.append(f"font assente: {FONT_TESTO.relative_to(ROOT)}")
        return "font assente"
    cpl, media = caratteri_per_riga(_campione_vero())
    nota = (f"{cpl:.1f} caratteri per riga · colonna {larghezza_colonna_pt():.1f} pt · "
            f"avanzata media {media:.2f} pt · EB Garamond {CORPO_PT} pt")
    if not (CPL_MIN <= cpl <= CPL_MAX):
        dove = "sotto" if cpl < CPL_MIN else "sopra"
        rilievi.append(
            f"caratteri per riga {cpl:.1f}: {dove} la finestra {CPL_MIN:.0f}-{CPL_MAX:.0f}. "
            + ("Righe troppo corte: il testo si legge a singhiozzi e i trattini si moltiplicano."
               if cpl < CPL_MIN else
               "Righe troppo lunghe: l'occhio perde la riga di ritorno."))
    return nota


# ===========================================================================
# 3. Daltonismo
# ===========================================================================
def _srgb_lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lin_srgb(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def simula(rgb: tuple[int, int, int], tipo: str) -> tuple[int, int, int]:
    """Il colore come lo vede un dicromate. Viénot/Brettel, via LMS."""
    r, g, b = (_srgb_lin(x / 255) for x in rgb)
    L = 17.8824 * r + 43.5161 * g + 4.11935 * b
    M = 3.45565 * r + 27.1554 * g + 3.86714 * b
    S = 0.0299566 * r + 0.184309 * g + 1.46709 * b
    m = DICROMAZIE[tipo]
    L2 = m[0][0] * L + m[0][1] * M + m[0][2] * S
    M2 = m[1][0] * L + m[1][1] * M + m[1][2] * S
    S2 = m[2][0] * L + m[2][1] * M + m[2][2] * S
    r2 = 0.0809444479 * L2 - 0.130504409 * M2 + 0.116721066 * S2
    g2 = -0.0102485335 * L2 + 0.0540193266 * M2 - 0.113614708 * S2
    b2 = -0.000365296938 * L2 - 0.00412161469 * M2 + 0.693511405 * S2
    return tuple(round(_lin_srgb(x) * 255) for x in (r2, g2, b2))


def _lab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    r, g, b = (_srgb_lin(x / 255) for x in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116  # noqa: E731
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def distanza(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    la, lb = _lab(a), _lab(b)
    return sum((x - y) ** 2 for x, y in zip(la, lb)) ** 0.5


_ESA = re.compile(r"#([0-9a-fA-F]{6})\b")


def colori_di(svg: str) -> dict[str, int]:
    """I colori esadecimali usati come riempimento o tratto, con la frequenza."""
    fuori: dict[str, int] = {}
    for m in re.finditer(r'(?:fill|stroke)="\s*(#[0-9a-fA-F]{6})\s*"', svg):
        c = m.group(1).lower()
        fuori[c] = fuori.get(c, 0) + 1
    return fuori


def _rgb(esa: str) -> tuple[int, int, int]:
    return tuple(int(esa[i:i + 2], 16) for i in (1, 3, 5))


def collassi(svg: str, minimo_usi: int = 2) -> list[tuple[str, str, str, float, float]]:
    """Coppie che in visione normale sono distinte e in dicromia diventano una.

    `minimo_usi` esclude i colori comparsi una volta sola: un tratto isolato non
    porta informazione, e segnalarlo sarebbe rumore.
    """
    usati = [c for c, n in colori_di(svg).items() if n >= minimo_usi]
    fuori = []
    for i, a in enumerate(usati):
        for b in usati[i + 1:]:
            ra, rb = _rgb(a), _rgb(b)
            d0 = distanza(ra, rb)
            if d0 < SOGLIA_DISTINTI:
                continue
            for tipo in DICROMAZIE:
                d1 = distanza(simula(ra, tipo), simula(rb, tipo))
                if d1 < SOGLIA_VICINI:
                    fuori.append((a, b, tipo, d0, d1))
    return fuori


def check_colori(rilievi: list[str]) -> int:
    """Raggruppa per **coppia di colori**, non per file.

    Le tavole del repo condividono la palette: senza raggruppare, la stessa
    coppia esce dodici volte e il referto diventa illeggibile — che e' il modo in
    cui un gate utile si fa disattivare. Una coppia, i file in cui compare.
    """
    n = 0
    per_coppia: dict[tuple[str, str, str], tuple[float, float, list[str]]] = {}
    for f in sorted(ROOT.rglob("*.svg")):
        rel = f.relative_to(ROOT)
        if ".git" in str(rel) or "/web/" in str(rel):
            continue
        n += 1
        for a, b, tipo, d0, d1 in collassi(f.read_text(encoding="utf-8", errors="ignore")):
            k = (a, b, tipo)
            voce = per_coppia.setdefault(k, (d0, d1, []))
            voce[2].append(rel.name)
    for (a, b, tipo), (d0, d1, files) in sorted(per_coppia.items(),
                                                key=lambda kv: -len(kv[1][2])):
        dove = (files[0] if len(files) == 1
                else f"{len(files)} tavole, fra cui {files[0]}")
        rilievi.append(
            f"{a} e {b} sono distinti (Δ{d0:.0f}) ma in **{tipo}** diventano lo "
            f"stesso colore (Δ{d1:.0f}) — se distinguono due cose diverse, per "
            f"chi ha questa dicromia la tavola le perde · {dove}")
    return n


# ===========================================================================
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--solo", choices=("titoli", "righe", "colori"), action="append")
    ap.add_argument("--strict", action="store_true", help="i rilievi diventano errori")
    a = ap.parse_args(argv)
    quali = set(a.solo or ("titoli", "righe", "colori"))

    rilievi: list[str] = []
    parti = []
    if "titoli" in quali:
        n = check_titoli(rilievi)
        parti.append(f"{n} master markdown")
    if "righe" in quali:
        parti.append(check_righe(rilievi))
    if "colori" in quali:
        n = check_colori(rilievi)
        parti.append(f"{n} tavole SVG")

    if rilievi:
        print(f"  ⚠ validate_tipografia: {len(rilievi)} rilievi")
        for r in rilievi[:40]:
            print(f"  - {r}")
        if len(rilievi) > 40:
            print(f"  … e altri {len(rilievi) - 40}")
        print("  (non bloccante: misura la leggibilità, che nessun exit code vede)")
        return 1 if a.strict else 0
    print("✓ validate_tipografia: " + " · ".join(parti))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
