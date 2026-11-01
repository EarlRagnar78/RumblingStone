#!/usr/bin/env python3
"""build_tavole.py — le tavole vettoriali del Drappo di Tarsilia.

Genera, in questa cartella:
  · tarsilia-citta.svg        mappa della città: fiume, cinque ponti, otto rioni, la Ruota
  · il-drappo.svg             il telo dipinto del premio, con le nove facce in basso a destra
  · ritratto-<pg>.svg  (×6)   cornice-ritratto stampabile per le sei schede

Sono **artefatti generati**: si rigenerano con `python3 build_tavole.py`, non si
modificano a mano. Le livree vengono dalla serie Golarion degli stemmi
(vedi ../../CONTRADE-DI-TARSILIA.md §1) così le due fonti non divergono.

Niente dipendenze: solo stdlib.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent

# ── livree delle otto contrade (dalla serie Golarion) ────────────────────────
CONTRADE = [
    ("Oca",      "Abadar",            "#ded3ba", "#22406e", "#8a6416"),
    ("Torre",    "Iomedae · Gorum",   "#5a4438", "#e4e9ec", "#dfa93b"),
    ("Bruco",    "Norgorber",         "#a9b2b8", "#23272b", "#74d98a"),
    ("Istrice",  "Sarenrae · Erastil","#2e4a34", "#7a5230", "#e0a83c"),
    ("Drago",    "Nethys",            "#141418", "#e6e6e2", "#7b52c0"),
    ("Civetta",  "Calistria",         "#101014", "#d9a521", "#aeb8c8"),
    ("Leocorno", "Shelyn",            "#b8496e", "#d7dce2", "#dfa93b"),
    ("Onda",     "Gozreh · Desna",    "#1d6b63", "#e2ecec", "#123a5c"),
]

PARCHMENT = "#efe3c6"
INK = "#2c2313"
INK_SOFT = "#5b4a2c"
WATER = "#6aa5c4"

FONT = "Georgia,'Liberation Serif','DejaVu Serif',serif"


def head(w, h, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="{FONT}">\n'
        f'<title>{title}</title>\n'
        '<defs>\n'
        '<pattern id="grain" width="6" height="6" patternUnits="userSpaceOnUse">'
        '<rect width="6" height="6" fill="none"/>'
        '<circle cx="1.5" cy="1.5" r="0.5" fill="#000" opacity="0.05"/>'
        '<circle cx="4.5" cy="3.5" r="0.4" fill="#000" opacity="0.04"/></pattern>\n'
        '<radialGradient id="vign" cx="50%" cy="45%" r="72%">'
        '<stop offset="60%" stop-color="#000" stop-opacity="0"/>'
        '<stop offset="100%" stop-color="#3a2c14" stop-opacity="0.30"/></radialGradient>\n'
        '</defs>\n'
        f'<rect width="{w}" height="{h}" fill="{PARCHMENT}"/>\n'
        f'<rect width="{w}" height="{h}" fill="url(#grain)"/>\n'
    )


def foot(w, h, note=""):
    s = f'<rect width="{w}" height="{h}" fill="url(#vign)"/>\n'
    s += (f'<rect x="10" y="10" width="{w-20}" height="{h-20}" fill="none" '
          f'stroke="{INK}" stroke-width="3"/>\n'
          f'<rect x="17" y="17" width="{w-34}" height="{h-34}" fill="none" '
          f'stroke="{INK}" stroke-width="1"/>\n')
    if note:
        s += (f'<text x="{w/2}" y="{h-26}" text-anchor="middle" font-size="11" '
              f'fill="{INK_SOFT}" font-style="italic">{note}</text>\n')
    return s + '</svg>\n'


def txt(x, y, s, size=13, fill=INK, anchor="start", weight="normal", style="normal", ls=0):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" font-style="{style}" '
            f'letter-spacing="{ls}">{s}</text>\n')


# ═══════════════════════════════════════════════════════════════════ CITTÀ ══
def citta():
    W, H = 1080, 760
    s = head(W, H, "Tarsilia — la città")
    # il Sellen — la riva nord sta a y=520, quella sud a y=660
    s += (f'<path d="M0 520 C 180 492, 320 548, 520 536 '
          f'C 720 524, 880 566, {W} 546 L {W} 668 L 0 668 Z" fill="{WATER}" opacity="0.55"/>\n')
    s += (f'<path d="M0 520 C 180 492, 320 548, 520 536 '
          f'C 720 524, 880 566, {W} 546" fill="none" stroke="#3d708f" stroke-width="2"/>\n')
    for off in (34, 62, 92):
        s += (f'<path d="M0 {520+off} C 200 {496+off}, 340 {550+off}, 540 {538+off} '
              f'C 740 {526+off}, 900 {566+off}, {W} {550+off}" fill="none" '
              f'stroke="#ffffff" stroke-width="1" opacity="0.24"/>\n')
    s += f'<rect x="0" y="660" width="{W}" height="{H-660}" fill="#c9b58e" opacity="0.6"/>\n'
    s += txt(240, 652, "il Sellen", 24, "#123a5c", anchor="middle", style="italic", ls=4, weight="bold")
    s += txt(W - 56, 700, "verso Cassomir, tre giorni di barca", 12, INK_SOFT,
             anchor="end", style="italic")

    # mura verso terra (nord)
    s += (f'<path d="M40 120 L 260 74 L 560 62 L 860 82 L 1040 128" fill="none" '
          f'stroke="{INK}" stroke-width="7" stroke-linecap="round"/>\n')
    for x, y in ((150, 96), (410, 66), (710, 70), (960, 104)):
        s += (f'<rect x="{x-11}" y="{y-13}" width="22" height="26" fill="#8d8271" '
              f'stroke="{INK}" stroke-width="2"/>\n')
    s += txt(560, 46, "MURA VERSO TERRA", 13, INK_SOFT, anchor="middle", ls=4)

    # la Ruota — piazza centrale
    cx, cy = 540, 300
    s += (f'<ellipse cx="{cx}" cy="{cy}" rx="152" ry="112" fill="#b08d68" '
          f'stroke="{INK}" stroke-width="3"/>\n')
    s += (f'<rect x="{cx-78}" y="{cy-52}" width="156" height="104" rx="6" '
          f'fill="#6b5b47" stroke="{INK}" stroke-width="2.5"/>\n')
    s += txt(cx, cy - 4, "MERCATO", 12, "#f0e6cf", anchor="middle", weight="bold", ls=2)
    s += txt(cx, cy + 14, "DEL GRANO", 12, "#f0e6cf", anchor="middle", weight="bold", ls=2)
    s += txt(cx, cy - 132, "LA RUOTA", 19, INK, anchor="middle", weight="bold", ls=5)
    s += txt(cx, cy + 150, "tre giri \u00b7 novanta secondi", 12, INK_SOFT,
             anchor="middle", style="italic")
    s += (f'<circle cx="{cx}" cy="{cy-112}" r="9" fill="#b94a3c" stroke="{INK}" stroke-width="2"/>\n')
    s += txt(cx - 20, cy - 118, "curva nord", 11, "#7d2f26", anchor="end", weight="bold")
    s += (f'<circle cx="{cx}" cy="{cy+112}" r="9" fill="#b94a3c" stroke="{INK}" stroke-width="2"/>\n')
    s += txt(cx + 20, cy + 116, "curva sud", 11, "#7d2f26", weight="bold")

    # i cinque ponti — attraversano davvero il fiume
    ponti = [(150, "Ponte Storto"), (330, "Ponte dei Tini"), (560, "Ponte del Teatro"),
             (760, "Ponte Vecchio"), (930, "il Quinto Ponte")]
    for x, nome in ponti:
        s += (f'<rect x="{x-11}" y="498" width="22" height="176" fill="#e6ccb2" '
              f'stroke="{INK}" stroke-width="2"/>\n')
        s += (f'<text x="{x}" y="586" font-size="11" fill="{INK}" text-anchor="middle" '
              f'transform="rotate(-90 {x} 586)">{nome}</text>\n')
    s += txt(930, 700, "(dondola)", 11, "#7d2f26", anchor="middle", style="italic")

    # gli otto rioni
    pos = [(140, 190), (300, 150), (790, 152), (950, 194),
           (150, 350), (300, 400), (790, 398), (950, 348)]
    ordine = [0, 1, 6, 4, 3, 2, 5, 7]
    for (x, y), idx in zip(pos, ordine):
        nome, dio, c1, c2, c3 = CONTRADE[idx]
        big = (nome == "Istrice")
        w_, h_ = (128, 84) if big else (110, 70)
        s += (f'<rect x="{x-w_//2}" y="{y-h_//2}" width="{w_}" height="{h_}" rx="5" '
              f'fill="{c1}" stroke="{INK}" stroke-width="{3 if big else 2}"/>\n')
        s += (f'<rect x="{x-w_//2}" y="{y-h_//2}" width="{w_}" height="12" rx="2" fill="{c2}"/>\n')
        s += (f'<rect x="{x-w_//2}" y="{y+h_//2-7}" width="{w_}" height="7" fill="{c3}"/>\n')
        light = c1 in ("#ded3ba", "#a9b2b8", "#e4e9ec")
        fg = INK if light else "#f4ecd8"
        s += txt(x, y + 6, nome.upper(), 15 if big else 13, fg, anchor="middle",
                 weight="bold", ls=2)
        s += txt(x, y + 22, dio, 8.5, fg, anchor="middle", style="italic")
        if big:
            s += txt(x, y - h_ // 2 - 8, "\u2605 la vostra contrada", 11, "#7d2f26",
                     anchor="middle", weight="bold")

    # il bosco di spini
    s += (f'<path d="M52 236 q 22 -30 44 0 q 22 -30 44 0 q 22 -30 44 0" fill="none" '
          f'stroke="#2e4a34" stroke-width="3"/>\n')
    s += txt(56, 268, "il bosco di spini", 12, "#2e4a34", style="italic")
    # il canale dei tintori
    s += (f'<path d="M240 442 L 372 500" stroke="{WATER}" stroke-width="9" opacity="0.75"/>\n')
    s += txt(200, 452, "canale dei tintori", 10, "#1d4a63", anchor="end", style="italic")

    # titolo
    s += txt(54, 46, "TARSILIA", 34, INK, weight="bold", ls=8)
    s += txt(54, 68, "città‑stato del Regno dei Fiumi · quattromila anime · otto contrade",
             12.5, INK_SOFT, style="italic")

    return s + foot(W, H, "Il Drappo di Tarsilia · tavola generata — build_tavole.py")


# ═══════════════════════════════════════════════════════════════════ DRAPPO ══
def drappo():
    W, H = 520, 900
    s = head(W, H, "Il Drappo di Tarsilia")
    # il telo
    s += (f'<path d="M60 70 L 460 70 L 460 790 L 260 850 L 60 790 Z" fill="#e8dcc0" '
          f'stroke="{INK}" stroke-width="3"/>\n')
    # asta
    s += f'<rect x="46" y="52" width="428" height="16" rx="4" fill="#7a5230" stroke="{INK}" stroke-width="2"/>\n'
    # cielo dipinto
    s += '<rect x="66" y="76" width="388" height="250" fill="#c9d9e2"/>\n'
    s += '<circle cx="360" cy="140" r="34" fill="#f2d98a" opacity="0.8"/>\n'
    # la piazza dipinta, in stile votivo naïf
    s += '<ellipse cx="260" cy="430" rx="168" ry="104" fill="#b08d68" stroke="#6b5b47" stroke-width="3"/>\n'
    s += '<rect x="192" y="392" width="136" height="76" fill="#6b5b47"/>\n'
    # otto cavalli stilizzati sull'anello
    import math
    for i in range(8):
        a = math.radians(200 + i * 20)
        x = 260 + 150 * math.cos(a)
        y = 430 + 92 * math.sin(a)
        c1 = CONTRADE[i][2]
        s += (f'<g transform="translate({x:.0f},{y:.0f})">'
              f'<ellipse cx="0" cy="0" rx="15" ry="7" fill="#5a4438"/>'
              f'<rect x="-4" y="-13" width="8" height="12" rx="3" fill="{c1}" '
              f'stroke="#2c2313" stroke-width="1"/></g>\n')
    # le nove facce, in basso a destra
    s += '<rect x="286" y="560" width="164" height="196" fill="#dccfae" opacity="0.5"/>\n'
    for i in range(9):
        col, row = i % 3, i // 3
        x = 316 + col * 52
        y = 600 + row * 60
        s += (f'<g transform="translate({x},{y})">'
              f'<circle cx="0" cy="0" r="19" fill="#e7d3b4" stroke="#6b5b47" stroke-width="1.6"/>'
              f'<circle cx="-6" cy="-3" r="2.1" fill="#3b2e1e"/>'
              f'<circle cx="6" cy="-3" r="2.1" fill="#3b2e1e"/>'
              f'<path d="M-7 8 q 7 {4 if i % 2 else -3} 14 0" fill="none" stroke="#3b2e1e" '
              f'stroke-width="1.6" stroke-linecap="round"/>'
              f'<path d="M-19 -4 q 19 -22 38 0" fill="none" stroke="#6b5b47" stroke-width="2"/>'
              f'</g>\n')
    s += txt(368, 782, "nove", 11, "#7d2f26", anchor="middle", style="italic")
    # folla generica a sinistra, deliberatamente sciatta
    for i in range(22):
        x = 86 + (i % 11) * 17
        y = 600 + (i // 11) * 44
        s += f'<circle cx="{x}" cy="{y}" r="9" fill="#cbb894" stroke="#a89572" stroke-width="1"/>\n'
    # cartiglio
    s += (f'<rect x="66" y="336" width="388" height="40" fill="#f4ecd8" opacity="0.85" '
          f'stroke="#6b5b47" stroke-width="1"/>\n')
    s += txt(260, 363, "VA' E TORNA VINCITORE", 19, INK, anchor="middle", weight="bold", ls=3)
    s += txt(260, 40, "IL DRAPPO", 26, INK, anchor="middle", weight="bold", ls=6)
    return s + foot(W, H, "dipinto da Lino Rasca — guardate in basso a destra")


# ════════════════════════════════════════════════════════════════ RITRATTI ══
PG = [
    # id, nome, ufficio, classe, tratto visivo, palette (capelli, incarnato, veste)
    ("vanna", "VANNA CORSARI", "il Capitano", "umana guerriera 3",
     "mani rovinate dalla resina", "#3a2c22", "#d9b391", "#2e4a34"),
    ("nocca", "NOCCA PETTIROSSO", "il Fantino", "halfling ranger 3",
     "scalzo, sempre", "#7a4a24", "#e0bd97", "#7a5230"),
    ("ombra", "OMBRA DEI SALICI", "lo Stalliere", "umana druida 3",
     "treccia grigia, mano ferma sul collo del cavallo", "#8a8478", "#d6ae8c", "#4a5f3c"),
    ("tesio", "TESIO MARCA", "il Tenente", "umano mago 3",
     "dita macchiate d'inchiostro, un corvo sull'avambraccio", "#241f1a", "#dbb694", "#3a3550"),
    ("berenice", "BERENICE SALLO", "l'Alfiere", "mezzelfa barda 3",
     "sta cantando, non posa", "#4a2f1e", "#e2c19d", "#b8496e"),
    ("melchio", "FRA' MELCHIO VANZI", "il Vicario", "umano chierico 3",
     "il registro tenuto contro il petto", "#9a958c", "#d3a988", "#8a6416"),
]


def ritratto(pid, nome, ufficio, classe, tratto, capelli, pelle, veste):
    W, H = 420, 560
    s = head(W, H, f"{nome} — {ufficio}")
    # scudo dell'Istrice in filigrana
    s += ('<g opacity="0.13" transform="translate(110,120) scale(1.0)">'
          '<path d="M20 20 H180 V150 Q180 210 100 232 Q20 210 20 150 Z" fill="#2e4a34"/></g>\n')
    # tondo del ritratto
    cx, cy, r = 210, 216, 128
    s += f'<circle cx="{cx}" cy="{cy}" r="{r+9}" fill="#d8c8a4" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#c9b58e"/>\n'
    s += f'<clipPath id="cl-{pid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>\n'
    s += f'<g clip-path="url(#cl-{pid})">\n'
    # spalle / veste
    s += f'<path d="M{cx-118} {cy+140} q 118 -96 236 0 v 80 h -236 Z" fill="{veste}"/>\n'
    # collo e testa
    s += f'<rect x="{cx-20}" y="{cy+16}" width="40" height="46" fill="{pelle}"/>\n'
    s += f'<ellipse cx="{cx}" cy="{cy-8}" rx="52" ry="62" fill="{pelle}"/>\n'
    # capelli
    s += (f'<path d="M{cx-54} {cy-14} q 6 -76 54 -76 q 48 0 54 76 '
          f'q -18 -34 -54 -34 q -36 0 -54 34 Z" fill="{capelli}"/>\n')
    # occhi e bocca, minimi
    s += f'<circle cx="{cx-19}" cy="{cy-12}" r="4" fill="#2b2118"/>\n'
    s += f'<circle cx="{cx+19}" cy="{cy-12}" r="4" fill="#2b2118"/>\n'
    s += (f'<path d="M{cx-14} {cy+26} q 14 8 28 0" fill="none" stroke="#8a5a44" '
          f'stroke-width="2.4" stroke-linecap="round"/>\n')
    s += '</g>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="2"/>\n'
    # targa
    s += (f'<rect x="30" y="378" width="360" height="106" fill="#f4ecd8" opacity="0.92" '
          f'stroke="{INK}" stroke-width="2"/>\n')
    s += txt(210, 408, nome, 20, INK, anchor="middle", weight="bold", ls=1.5)
    s += txt(210, 432, ufficio.upper(), 13, "#7d2f26", anchor="middle", weight="bold", ls=4)
    s += txt(210, 456, classe, 12.5, INK_SOFT, anchor="middle", style="italic")
    s += txt(210, 474, f"«{tratto}»", 11.5, INK_SOFT, anchor="middle", style="italic")
    s += txt(210, 52, "IL DRAPPO DI TARSILIA", 12, INK_SOFT, anchor="middle", ls=5)
    s += txt(210, 74, "contrada dell'Istrice", 13, "#2e4a34", anchor="middle", weight="bold")
    return s + foot(W, H, "segnaposto vettoriale — sostituibile col ritratto generato")


def main():
    written = []
    (OUT / "tarsilia-citta.svg").write_text(citta(), encoding="utf-8")
    written.append("tarsilia-citta.svg")
    (OUT / "il-drappo.svg").write_text(drappo(), encoding="utf-8")
    written.append("il-drappo.svg")
    for args in PG:
        name = f"ritratto-{args[0]}.svg"
        (OUT / name).write_text(ritratto(*args), encoding="utf-8")
        written.append(name)
    for w in written:
        print("✓", w)


if __name__ == "__main__":
    main()
