#!/usr/bin/env python3
"""Genera la serie Golarion degli stemmi, riusando le figure game-icons della serie Faerûn.

Uso:  python3 build_golarion_shields.py
Legge ../NN-*.svg, ne estrae transform e path delle icone, e riscrive gli 8 file
qui accanto con livree, simboli divini e titoli di Golarion. Vedi README.md.
"""
import pathlib, re

FR  = pathlib.Path(__file__).resolve().parent.parent   # ../  = serie Faerûn
GOL = pathlib.Path(__file__).resolve().parent           # questa cartella

SHIELD = "M20 20 H180 V150 Q180 210 100 232 Q20 210 20 150 Z"
STAR   = "M0 -16 L4.5 -4.5 L16 -4.5 L6.5 3 L10 15 L0 7.5 L-10 15 L-6.5 3 L-16 -4.5 L-4.5 -4.5 Z"

def figura(shield):
    """(transform, path-d, commento-icona) dal blocco FIGURA della serie Faerûn"""
    t = (FR / shield).read_text()
    m = re.search(r'<!-- FIGURA(.*?)-->\n(.*?)<!-- /FIGURA -->', t, re.S)
    tr = re.search(r'<g transform="([^"]+)">', m.group(2)).group(1)
    d  = re.search(r'<path d="([^"]+)"', m.group(2)).group(1)
    return tr, d, m.group(1).strip()

# Cartiglio identico su tutti gli scudi, da filo a filo del bordo esterno (PROCEDURA.md §5).
BX, BW = 17, 166
FONT = 'Georgia,&quot;Liberation Serif&quot;,&quot;DejaVu Serif&quot;,serif'

# Larghezze naturali misurate con tools/measure_shields.py. Bloccano il testo dentro il
# cartiglio con qualunque font: senza, i ripieghi più larghi di Georgia lo facevano uscire.
# ⚠️ Se cambi un motto o un titolo, rimisura e aggiorna qui.
TL_MOTTO = {"01-oca":127.0,"02-torre":115.4,"03-bruco":104.9,"04-istrice":116.0,
            "05-drago":148.8,"06-civetta":119.7,"07-unicorno":140.4,"08-onda":148.6}
TL_TITOLO = {"01-oca":87.0,"02-torre":143.0,"03-bruco":124.0,"04-istrice":136.0,
             "05-drago":105.0,"06-civetta":127.0,"07-unicorno":123.0,"08-onda":118.0}


def svg(out, label, livrea, cid, campo, campo2, bordo, fig_fill, shield_src,
        defs="", sotto="", sopra="", banner_fill="#111", motto_fill="#eee",
        motto="", titolo="", titolo_fill="#333", bfs=11.5, tfs=12):
    tr, d, icona = figura(shield_src)
    dx = f'<defs><clipPath id="{cid}"><path d="{SHIELD}"/></clipPath>{defs}</defs>'
    (GOL / out).write_text(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 240" width="200" height="240" role="img" aria-label="{label}">
  <!-- LIVREA GOLARION · {livrea} -->
  {dx}
  <path d="{SHIELD}" fill="{campo}" stroke="{bordo}" stroke-width="6"/>
  <g clip-path="url(#{cid})">
    <path d="M100 20 H180 V150 Q180 210 100 232 Z" fill="{campo2}"/>
{sotto}    <!-- FIGURA · {icona} -->
    <g fill="{fig_fill}"><g transform="{tr}"><path d="{d}"/></g></g>
    <!-- /FIGURA -->
{sopra}  </g>
  <path d="{SHIELD}" fill="none" stroke="{bordo}" stroke-width="6"/>
  <rect x="{BX}" y="182" width="{BW}" height="26" rx="4" fill="{banner_fill}" opacity="0.85"/>
  <text x="100" y="200" font-family="{FONT}" font-size="{bfs}" fill="{motto_fill}" text-anchor="middle" font-style="italic" textLength="{TL_MOTTO[out[:-4]]:.1f}" lengthAdjust="spacingAndGlyphs">{motto}</text>
  <text x="100" y="14" font-family="{FONT}" font-size="{tfs}" fill="{titolo_fill}" text-anchor="middle" font-weight="bold" textLength="{TL_TITOLO[out[:-4]]:.1f}" lengthAdjust="spacingAndGlyphs">{titolo}</text>
</svg>
""")
    print("OK", out)

ORO, ORO_S, ARG = "#dfa93b", "#8a6416", "#d7dce2"

# 1 · ABADAR — chiavi, città, ricchezza, legge. Campo di marmo, oca di lapis.
tr, d, _ = figura("01-oca.svg")
svg("01-oca.svg", "Stemma dell'Oca — The Golden Plume (Abadar)",
    "The Golden Plume (Abadar): marmo e lapis, bordata d'oro brunito",
    "ga1", "#ded3ba", "#d2c6ab", ORO_S, "#22406e", "01-oca.svg",
    defs=f'<clipPath id="ga1-or"><rect x="406" y="84" width="92" height="74"/>'
         f'<rect x="188" y="450" width="234" height="62"/></clipPath>',
    sopra=f'    <g fill="{ORO}"><g transform="{tr}" clip-path="url(#ga1-or)"><path d="{d}"/></g></g>\n'
          '    <!-- chiave d\'oro di Abadar -->\n'
          f'    <g transform="translate(44 150)" fill="{ORO}" stroke="{ORO_S}" stroke-width="1.5">'
          '<circle cx="0" cy="-10" r="7" fill="none" stroke-width="4"/>'
          '<rect x="-2.5" y="-4" width="5" height="26"/><rect x="-2.5" y="12" width="11" height="4.5"/>'
          '<rect x="-2.5" y="19" width="9" height="4.5"/></g>\n',
    banner_fill="#3a2c12", motto_fill=ORO, motto="Al suono dell'oro, all'armi",
    titolo="L'OCA · Abadar", titolo_fill="#22406e", bfs=12)

# 2 · GORUM + IOMEDAE — ferro e spada raggiante. Torre muragliata d'argento.
tr, d, _ = figura("02-torre.svg")
corsi = []
y, riga = 62, 0
while y < 492:
    corsi.append(f'<line x1="80" y1="{y}" x2="430" y2="{y}"/>')
    for x in range(84 + (0 if riga % 2 == 0 else 42), 430, 84):
        corsi.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+38}"/>')
    y += 38; riga += 1
svg("02-torre.svg", "Stemma della Torre — The Iron Bastion (Gorum/Iomedae)",
    "The Iron Bastion (Gorum/Iomedae): ferro rugginoso e argento, bordata d'oro",
    "gt2", "#5a4438", "#4a382e", ORO, "#e4e9ec", "02-torre.svg",
    defs=f'<clipPath id="gt2-conci"><path d="{d}" transform="{tr}"/></clipPath>',
    sopra=f'    <g clip-path="url(#gt2-conci)" stroke="#9aa6ad" stroke-width="1" fill="none">'
          f'<g transform="{tr}"><g stroke-width="4">{"".join(corsi)}</g></g></g>\n'
          '    <!-- spada raggiante di Iomedae sul portone -->\n'
          f'    <g transform="translate(100 150)" fill="{ORO}" stroke="{ORO_S}" stroke-width="1">'
          '<circle cx="0" cy="0" r="11" fill="none" stroke-width="2.5" stroke-dasharray="3 3"/>'
          '<path d="M0 -9 L2 -4 V7 h3 l-5 6 -5 -6 h3 V-4 Z"/></g>\n',
    banner_fill="#241a14", motto_fill="#e4e9ec", motto="Oltre il ferro, la volontà",
    titolo="LA TORRE · Gorum/Iomedae", titolo_fill="#5a4438", bfs=12, tfs=11)

# 3 · NORGORBER — segreti, veleno, omicidio. Maschera nera; il verde-veleno è suo.
svg("03-bruco.svg", "Stemma del Bruco — The Silver Weft (Norgorber)",
    "The Silver Weft (Norgorber): argento sericeo e nero-fumo, listata di verde-veleno",
    "gb3", "#a9b2b8", "#97a1a8", "#23272b", "#2b3036", "03-bruco.svg",
    sotto='    <!-- banda di seta -->\n'
          '    <path d="M40 158 q50 -40 118 -30 q-40 30 -118 30z" fill="#6e767c" stroke="#3a4046" stroke-width="2"/>\n'
          '    <path d="M46 154 q40 -20 96 -22" stroke="#3a4046" stroke-width="1.5" fill="none"/>\n',
    sopra='    <!-- maschera nera di Norgorber -->\n'
          '    <g transform="translate(150 156)" fill="#101216" stroke="#74d98a" stroke-width="1.4">'
          '<path d="M-13 -9 q13 -5 26 0 q1 12 -5 17 q-8 5 -16 0 q-6 -5 -5 -17z"/>'
          '<ellipse cx="-6" cy="-1" rx="3.2" ry="2.2" fill="#74d98a" stroke="none"/>'
          '<ellipse cx="6" cy="-1" rx="3.2" ry="2.2" fill="#74d98a" stroke="none"/></g>\n',
    banner_fill="#14171a", motto_fill="#74d98a", motto="Nell'ombra mi rivolto",
    titolo="IL BRUCO · Norgorber", titolo_fill="#23272b", bfs=12)

# 4 · SARENRAE + ERASTIL — redenzione e comunità. Catene sciolte in oro solare, ankh.
svg("04-istrice.svg", "Stemma dell'Istrice — The Quill-Wood Refuge (Sarenrae/Erastil)",
    "The Quill-Wood Refuge (Sarenrae/Erastil): verde legnoferro e bruno di terra, bordata d'oro solare",
    "gi4", "#2e4a34", "#27402c", "#e0a83c", "#efe6cf", "04-istrice.svg",
    sotto='    <!-- campagna di bruno di terra -->\n'
          '    <path d="M20 164 H180 V150 Q180 210 100 232 Q20 210 20 150 Z" fill="#7a5230"/>\n',
    sopra='    <!-- catene spezzate, sciolte nell\'oro solare di Sarenrae -->\n'
          '    <g stroke="#e0a83c" stroke-width="3" fill="none"><circle cx="42" cy="172" r="6"/>'
          '<circle cx="53" cy="178" r="6"/><circle cx="158" cy="172" r="6"/><circle cx="147" cy="178" r="6"/></g>\n'
          '    <!-- ankh di Sarenrae -->\n'
          '    <g transform="translate(42 52)" fill="none" stroke="#e0a83c" stroke-width="3.4" stroke-linecap="round">'
          '<ellipse cx="0" cy="-7" rx="6" ry="7.5"/><path d="M0 0 V16 M-7 6 H7"/></g>\n',
    banner_fill="#1a2a1e", motto_fill="#efe6cf", motto="Pungo solo chi mi assale",
    titolo="L'ISTRICE · Sarenrae/Erastil", titolo_fill="#2e4a34", tfs=10.5)

# 5 · NETHYS — la dualità: il campo stesso è la sua faccia mezza nera e mezza bianca.
svg("05-drago.svg", "Stemma del Drago — The Spell-Wyrm Spires (Nethys)",
    "The Spell-Wyrm Spires (Nethys): partita di nero e d'argento, listata di viola arcano",
    "gd5", "#141418", "#e6e6e2", "#7b52c0", "#7b52c0", "05-drago.svg",
    sopra='    <!-- soffio d\'arcano verso il lato chiaro -->\n'
          '    <path d="M127 124 q12 12 12 24" fill="none" stroke="#dfa93b" stroke-width="3" stroke-dasharray="3 3"/>\n'
          f'    <g transform="translate(141,163)" fill="{ORO}" stroke="{ORO_S}" stroke-width="1"><path d="{STAR}"/></g>\n',
    banner_fill="#1a1030", motto_fill="#d8ccf0", motto="Il cuore che arde parla in fiamme",
    titolo="IL DRAGO · Nethys", titolo_fill="#7b52c0", bfs=11)

# 6 · CALISTRIA — vendetta, inganno, spie. Disco a fasce di vespa al posto del disco di Shar.
svg("06-civetta.svg", "Stemma della Civetta — The Whispering Shadows (Calistria)",
    "The Whispering Shadows (Calistria): nero e giallo-vespa, listata d'argento freddo",
    "gc6", "#101014", "#d9a521", "#aeb8c8", "#e4e8f0", "06-civetta.svg",
    defs='<clipPath id="gc6-vespa"><circle cx="100" cy="150" r="30"/></clipPath>',
    sotto='    <!-- disco della vespa di Calistria -->\n'
          '    <circle cx="100" cy="150" r="30" fill="#141414"/>\n'
          '    <g clip-path="url(#gc6-vespa)" fill="#d9a521">'
          '<rect x="70" y="126" width="60" height="9"/><rect x="70" y="144" width="60" height="9"/>'
          '<rect x="70" y="162" width="60" height="9"/></g>\n'
          '    <circle cx="100" cy="150" r="30" fill="none" stroke="#aeb8c8" stroke-width="2"/>\n',
    banner_fill="#000", motto_fill="#aeb8c8", motto="Guardo dove la notte tace",
    titolo="LA CIVETTA · Calistria", titolo_fill="#8a6a12")

# 7 · SHELYN — bellezza, arte, musica. Rosa di Shelyn; il corno resta d'oro.
svg("07-unicorno.svg", "Stemma dell'Unicorno — The Gilded Horn (Shelyn)",
    "The Gilded Horn (Shelyn): rosa di Shelyn e argento, con l'oro del corno",
    "gu7", "#b8496e", "#a33d5f", ARG, "#f7f2f4", "07-unicorno.svg",
    sopra='    <!-- il corno dorato che dà il nome al distretto -->\n'
          f'    <path d="M113 72 L156 44" fill="none" stroke="{ORO}" stroke-width="5" stroke-linecap="round"/>\n',
    banner_fill="#3d1424", motto_fill=ORO, motto="Ferisce e sana il corno che porto",
    titolo="L'UNICORNO · Shelyn", titolo_fill="#b8496e", bfs=10.5)

# 8 · GOZREH + DESNA — mare/cielo e luna/stelle. Falce e tre stelle di Desna.
svg("08-onda.svg", "Stemma dell'Onda — The Tidal Crest (Gozreh/Desna)",
    "The Tidal Crest (Gozreh/Desna): verde-fiume e argento lunare, bordata di blu profondo, stellata",
    "go8", "#e2ecec", "#e2ecec", "#123a5c", "#123a5c", "08-onda.svg",
    sotto='    <!-- bande d\'onda -->\n'
          '    <path d="M20 118 q20 -14 40 0 q20 14 40 0 q20 -14 40 0 q20 14 40 0 V232 H20 Z" fill="#2e8c7e"/>\n'
          '    <path d="M20 150 q20 -14 40 0 q20 14 40 0 q20 -14 40 0 q20 14 40 0 V232 H20 Z" fill="#1d6b63"/>\n'
          '    <path d="M20 182 q20 -14 40 0 q20 14 40 0 q20 -14 40 0 q20 14 40 0 V232 H20 Z" fill="#124240"/>\n'
          '    <!-- falce e stelle di Desna -->\n'
          f'    <path d="M48 44 a13 13 0 1 0 5 22 a10 10 0 1 1 -5 -22z" fill="{ORO}" stroke="{ORO_S}" stroke-width="1.8"/>\n'
          f'    <g fill="{ORO}" stroke="{ORO_S}" stroke-width="0.8">'
          f'<g transform="translate(74,34) scale(0.30)"><path d="{STAR}"/></g>'
          f'<g transform="translate(36,74) scale(0.24)"><path d="{STAR}"/></g>'
          f'<g transform="translate(66,66) scale(0.19)"><path d="{STAR}"/></g></g>\n',
    banner_fill="#0c2a3e", motto_fill="#cfe0d6", motto="Il cielo mi colora, il fiume mi arma",
    titolo="L'ONDA · Gozreh/Desna", titolo_fill="#123a5c", bfs=10.5, tfs=11)
