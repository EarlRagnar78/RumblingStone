#!/usr/bin/env python3
"""Genera l'armoriale di Channathgate: una pagina autonoma con i 16 scudi inline.

Uso:  python3 tools/build_armorial.py [file-di-uscita.html]

Legge gli SVG da ../ (serie Faerûn) e ../golarion/ (serie Golarion) e li incorpora
come SVG inline — nessun file esterno, la pagina è autoportante. Le due tabelle
ARMS e GOL qui sotto sono l'unica fonte dei testi: motti, livree, esadecimali e
attribuzioni. Se cambi uno stemma, aggiorna la riga corrispondente.

La pagina è tematizzata per chiaro e scuro. Gli scudi sono montati su pergamena in
entrambi i temi perché i titoli sono dipinti dentro gli SVG nei colori del booklet,
e su fondo scuro sparirebbero.
"""
import pathlib, re, html

import sys

BASE = pathlib.Path(__file__).resolve().parent.parent      # ../ = cartella stemmi/
OUT  = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "ARMORIALE.html"

ARMS = [
 ("01-oca.svg", "L'Oca", "The Golden Plume", "Waukeen",
  "Al suono dell'oro, all'armi",
  "Porpora e oro, bordata di bianco perla",
  "Banchieri e aristocrazia terriera. Oca beccata e membrata d'oro. Il suo voto è la resa.",
  "goose", "Delapouite",
  [("#4a2560","porpora"),("#dfa93b","oro"),("#f0eada","perla")]),

 ("02-torre.svg", "La Torre", "The Iron Bastion", "Torm · Tempus",
  "Oltre il ferro, la volontà",
  "Acciaio brunito e scarlatto, bordata d'argento",
  "Veterani e fabbri d'armi. Torre muragliata: i giunti sono un argento più scuro del suo.",
  "white-tower", "Lorc",
  [("#3c4854","acciaio"),("#a6242c","scarlatto"),("#8d9aa6","giunti")]),

 ("03-bruco.svg", "Il Bruco", "The Silver Weft", "Mask",
  "Nell'ombra mi rivolto",
  "Argento sericeo e nero-fumo, listata di verde-veleno",
  "Ricettatori e contrabbandieri. Il verde-veleno è la Piaga Chimica dei Canali.",
  "caterpillar", "Delapouite",
  [("#a9b2b8","argento"),("#23272b","nero-fumo"),("#74d98a","veleno")]),

 ("04-istrice.svg", "L'Istrice", "The Quill-Wood Refuge", "Ilmater · Chauntea",
  "Pungo solo chi mi assale",
  "Verde legnoferro e bruno di terra, bordata d'avorio",
  "Gli ottocento profughi di Drellin's Ferry. Le catene spezzate sono di rosso Ilmater.",
  "porcupine", "Caro Asercion",
  [("#2e4a34","legnoferro"),("#7a5230","bruno"),("#e8dfc6","avorio")]),

 ("05-drago.svg", "Il Drago", "The Spell-Wyrm Spires", "Mystra",
  "Il cuore che arde parla in fiamme",
  "Blu notte e argento, listata di viola arcano",
  "Speziali e accademia arcana. Il drago soffia verso la stella d'oro di Mystra.",
  "spiked-dragon-head", "Delapouite",
  [("#1b2a5a","blu notte"),("#c7d0de","argento"),("#dfa93b","oro")]),

 ("06-civetta.svg", "La Civetta", "The Whispering Shadows", "Shar",
  "Guardo dove la notte tace",
  "Nero e viola di Shar, listata d'argento freddo",
  "Nobiltà decaduta, burocrati, spie. La civetta sta davanti al disco nero di Shar.",
  "barn-owl", "Caro Asercion",
  [("#101014","nero"),("#4b2a6b","viola di Shar"),("#aeb8c8","argento freddo")]),

 ("07-unicorno.svg", "L'Unicorno", "The Gilded Horn", "Sune · Milil",
  "Ferisce e sana il corno che porto",
  "Cremisi di Sune e argento di Milil, con l'oro dell'arpa",
  "Sarti, falegnami, menestrelli. Il rione più bello e il più codardo: l'ago della bilancia.",
  "unicorn", "Delapouite",
  [("#9e1f3d","cremisi"),("#d7dce2","argento"),("#dfa93b","oro")]),

 ("08-onda.svg", "L'Onda", "The Tidal Crest", "Valkur · Selûne",
  "Il cielo mi colora, il fiume mi arma",
  "Verde-fiume e argento lunare, bordata di blu profondo",
  "Barcaioli e portuali del Cannath, sotto la falce d'oro di Selûne. Evacua i civili.",
  "big-wave", "Lorc",
  [("#1d6b63","verde-fiume"),("#123a5c","blu profondo"),("#dfa93b","oro")]),
]

GOL = [
 ("01-oca.svg",      "Abadar",            "marmo e lapis, bordata d'oro brunito",
  "Città, ricchezza, legge, mercanti. La moneta di Waukeen diventa la sua chiave d'oro."),
 ("02-torre.svg",    "Iomedae · Gorum",   "ferro rugginoso e argento, bordata d'oro",
  "Onore e giustizia più la guerra: la stessa coppia dovere/battaglia. Spada raggiante sul portone."),
 ("03-bruco.svg",    "Norgorber",         "argento sericeo e nero-fumo, listata di verde-veleno",
  "Segreti, furto, omicidio — ed è il dio del veleno, che giustifica il verde meglio dell'originale."),
 ("04-istrice.svg",  "Sarenrae · Erastil","verde legnoferro e bruno di terra, bordata d'oro solare",
  "Guarigione e comunità. Le catene si sciolgono nell'oro solare, e l'ankh sale in capo."),
 ("05-drago.svg",    "Nethys",            "partita di nero e d'argento, listata di viola arcano",
  "La faccia mezza nera e mezza bianca non è un emblema: è la partizione stessa dello scudo."),
 ("06-civetta.svg",  "Calistria",         "nero e giallo-vespa, listata d'argento freddo",
  "Vendetta, inganno, spie: il mestiere reale del distretto. Il disco porta le fasce della vespa."),
 ("07-unicorno.svg", "Shelyn",            "rosa di Shelyn e argento, con l'oro del corno",
  "Bellezza, arte e musica in una divinità sola: copre sia Sune sia Milil."),
 ("08-onda.svg",     "Gozreh · Desna",    "verde-fiume e argento lunare, bordata di blu profondo, stellata",
  "Mare e cielo più luna, stelle e viaggio. Desna e Selûne sono quasi la stessa dea."),
]

def inline_gol(fn):
    s = (BASE / "golarion" / fn).read_text()
    s = re.sub(r'\s(?:width|height)="\d+"', '', s, count=2)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    return s.strip()

def inline(fn):
    s = (BASE / fn).read_text()
    s = re.sub(r'\s(?:width|height)="\d+"', '', s, count=2)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    return s.strip()

cards = []
for fn, it, en, god, motto, blazon, note, icon, author, sw in ARMS:
    chips = "".join(
        f'<li><span class="sw" style="--c:{c}"></span>'
        f'<span class="swn">{html.escape(n)}</span>'
        f'<span class="swh">{c}</span></li>' for c, n in sw)
    cards.append(f"""<article class="arm">
  <div class="shield">{inline(fn)}</div>
  <div class="blazon">
    <p class="eyebrow">{html.escape(god)}</p>
    <h2>{html.escape(en)}</h2>
    <p class="it">{html.escape(it)}</p>
    <p class="motto">&ldquo;{html.escape(motto)}&rdquo;</p>
    <p class="livery">{html.escape(blazon)}</p>
    <ul class="swatches">{chips}</ul>
    <p class="note">{html.escape(note)}</p>
    <p class="credit"><span>{html.escape(icon)}</span> &middot; {html.escape(author)}</p>
  </div>
</article>""")

gol_cards = []
for (fn, it, en, fgod, motto, fblazon, fnote, icon, author, sw), (_, ggod, gblazon, gnote) in zip(ARMS, GOL):
    gol_cards.append(f"""<article class="arm duo">
  <div class="pair">
    <div class="shield">{inline(fn)}<span class="tag">Faer&ucirc;n</span></div>
    <div class="shield">{inline_gol(fn)}<span class="tag">Golarion</span></div>
  </div>
  <div class="blazon">
    <p class="eyebrow">{html.escape(fgod)} &rarr; {html.escape(ggod)}</p>
    <h2>{html.escape(en)}</h2>
    <p class="livery">{html.escape(gblazon)}</p>
    <p class="note">{html.escape(gnote)}</p>
  </div>
</article>""")

page = f"""<title>Armoriale di Channathgate</title>
<style>
:root {{
  --ground:#e6e4da; --surface:#f2f1e9; --sunk:#dcdad0;
  --ink:#1b2027; --ink-soft:#565d59; --ink-faint:#7d847e;
  --brass:#8e7134; --rule:#c6c3b4; --shadow:rgba(27,32,39,.14);
  --vellum:#efe6cf; --vellum-edge:#d3c7a4;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:Optima,"Gill Sans","Gill Sans MT","Trebuchet MS","Segoe UI",sans-serif;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}}
@media (prefers-color-scheme:dark) {{
  :root:not([data-theme="light"]) {{
    --ground:#12151a; --surface:#1a1e25; --sunk:#0d1014;
    --ink:#e5e7e0; --ink-soft:#a3aaa4; --ink-faint:#7c837d;
    --brass:#c6a25e; --rule:#2f363d; --shadow:rgba(0,0,0,.5);
  }}
}}
:root[data-theme="dark"] {{
  --ground:#12151a; --surface:#1a1e25; --sunk:#0d1014;
  --ink:#e5e7e0; --ink-soft:#a3aaa4; --ink-faint:#7c837d;
  --brass:#c6a25e; --rule:#2f363d; --shadow:rgba(0,0,0,.5);
}}

*,*::before,*::after {{ box-sizing:border-box; }}
body {{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:var(--sans); font-size:16px; line-height:1.6;
  -webkit-font-smoothing:antialiased;
}}
.wrap {{ max-width:1180px; margin:0 auto; padding:clamp(2rem,5vw,4.5rem) clamp(1.1rem,4vw,2.5rem) 4rem; }}

header.top {{ display:flex; flex-direction:column; gap:.9rem; padding-bottom:1.6rem;
  border-bottom:1px solid var(--rule); }}
.kicker {{ font-size:.72rem; letter-spacing:.19em; text-transform:uppercase;
  color:var(--brass); margin:0; font-weight:600; }}
h1 {{ font-family:var(--serif); font-weight:400; font-size:clamp(2.1rem,5.6vw,3.4rem);
  line-height:1.05; margin:0; text-wrap:balance; letter-spacing:-.012em; }}
.standfirst {{ margin:0; max-width:63ch; color:var(--ink-soft); font-size:1.02rem; }}
.standfirst b {{ color:var(--ink); font-weight:600; }}

.roll {{ display:grid; gap:1.5rem; margin-top:2.4rem;
  grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); }}

.arm {{ background:var(--surface); border:1px solid var(--rule); border-radius:3px;
  padding:1.5rem 1.4rem 1.3rem; display:flex; flex-direction:column; gap:1.1rem;
  box-shadow:0 1px 2px var(--shadow); }}
.shield {{ display:flex; justify-content:center; background:var(--vellum);
  border:1px solid var(--vellum-edge); border-radius:2px; padding:.7rem 0 .55rem;
  position:relative; }}
.pair {{ display:grid; grid-template-columns:1fr 1fr; gap:.55rem; }}
.pair .shield svg {{ width:100%; max-width:118px; }}
.tag {{ position:absolute; left:0; right:0; bottom:.25rem; text-align:center;
  font-size:.58rem; letter-spacing:.13em; text-transform:uppercase; color:var(--ink-faint); }}
.duo .blazon {{ gap:.4rem; }}
h2.sec {{ font-family:var(--serif); font-weight:400; font-size:clamp(1.5rem,3.4vw,2.1rem);
  margin:0; letter-spacing:-.01em; }}
.secintro {{ margin:0; max-width:63ch; color:var(--ink-soft); font-size:.95rem; }}
.sechead {{ display:flex; flex-direction:column; gap:.6rem; margin-top:3.4rem;
  padding-top:1.6rem; border-top:1px solid var(--rule); }}
.shield svg {{ width:152px; height:auto; display:block;
  filter:drop-shadow(0 2px 5px rgba(60,48,24,.28)); }}

.blazon {{ display:flex; flex-direction:column; gap:.5rem; }}
.eyebrow {{ margin:0; font-size:.68rem; letter-spacing:.15em; text-transform:uppercase;
  color:var(--brass); font-weight:600; }}
.arm h2 {{ font-family:var(--serif); font-weight:400; font-size:1.42rem; line-height:1.15;
  margin:0; letter-spacing:-.008em; text-wrap:balance; }}
.it {{ margin:-.28rem 0 0; font-size:.86rem; color:var(--ink-faint); font-style:italic; }}
.motto {{ margin:.35rem 0 0; font-family:var(--serif); font-style:italic;
  font-size:1rem; color:var(--ink); line-height:1.4; text-wrap:balance; }}
.livery {{ margin:.15rem 0 0; font-size:.82rem; color:var(--ink-soft); }}

.swatches {{ list-style:none; margin:.25rem 0 0; padding:0; display:flex;
  flex-direction:column; gap:.28rem; }}
.swatches li {{ display:flex; align-items:center; gap:.5rem; font-size:.72rem; }}
.sw {{ width:15px; height:15px; flex:none; border-radius:2px; background:var(--c);
  border:1px solid var(--rule); }}
.swn {{ color:var(--ink-soft); flex:1; }}
.swh {{ font-family:var(--mono); font-size:.68rem; color:var(--ink-faint);
  font-variant-numeric:tabular-nums; text-transform:uppercase; }}

.note {{ margin:.5rem 0 0; padding-top:.7rem; border-top:1px solid var(--rule);
  font-size:.83rem; color:var(--ink-soft); line-height:1.5; }}
.credit {{ margin:0; font-size:.7rem; color:var(--ink-faint); letter-spacing:.03em; }}
.credit span {{ font-family:var(--mono); color:var(--ink-soft); }}

footer.colophon {{ margin-top:3rem; padding-top:1.5rem; border-top:1px solid var(--rule);
  display:flex; flex-direction:column; gap:.7rem; max-width:70ch; }}
.colophon h3 {{ font-family:var(--serif); font-weight:400; font-size:1.1rem; margin:0; }}
.colophon p {{ margin:0; font-size:.85rem; color:var(--ink-soft); }}
code {{ font-family:var(--mono); font-size:.86em; color:var(--ink); }}
.colophon a {{ color:var(--brass); text-decoration:underline; text-underline-offset:2px; }}
.colophon a:focus-visible {{ outline:2px solid var(--brass); outline-offset:3px; }}

@media (prefers-reduced-motion:no-preference) {{
  .arm {{ animation:rise .5s cubic-bezier(.2,.7,.3,1) backwards; }}
  .arm:nth-child(1) {{ animation-delay:.02s }} .arm:nth-child(2) {{ animation-delay:.06s }}
  .arm:nth-child(3) {{ animation-delay:.10s }} .arm:nth-child(4) {{ animation-delay:.14s }}
  .arm:nth-child(5) {{ animation-delay:.18s }} .arm:nth-child(6) {{ animation-delay:.22s }}
  .arm:nth-child(7) {{ animation-delay:.26s }} .arm:nth-child(8) {{ animation-delay:.30s }}
  @keyframes rise {{ from {{ opacity:0; transform:translateY(9px) }} to {{ opacity:1; transform:none }} }}
}}
</style>

<div class="wrap">
  <header class="top">
    <p class="kicker">Palio di Channathgate &middot; ARC-09 P2D &middot; 1372 DR</p>
    <h1>Armoriale delle otto contrade</h1>
    <p class="standfirst">Gli stemmi dopo la ricolorazione: ogni distretto porta una livrea
    derivata dalla <b>divinità patrona</b> e dal suo <b>nome faerûniano</b>, non più dai
    colori della contrada senese di partenza. <b>Nessuna</b> delle otto combinazioni
    coincide con quelle delle diciassette contrade reali.</p>
  </header>

  <main class="roll">
{chr(10).join(cards)}
  </main>

  <header class="sechead">
    <p class="kicker">Variante d'ambientazione &middot; Pathfinder / Golarion</p>
    <h2 class="sec">Gli stessi otto, sotto un altro cielo</h2>
    <p class="secintro"><code>AVVENTURA</code> &sect;1 registra che le divinit&agrave; faer&ucirc;niane
    sono una <b>riconversione da Golarion</b> — ma il pantheon di partenza non era documentato
    da nessuna parte. Questa serie lo ricostruisce dal <b>ruolo</b> di ogni distretto. Stesse
    figure, stesse meccaniche 3.5: cambiano divinit&agrave;, livrea e simbolo in campo.</p>
  </header>

  <main class="roll">
{chr(10).join(gol_cards)}
  </main>

  <footer class="colophon">
    <h3>Colophon</h3>
    <p>Scudi, livree, cartigli e simboli divini — moneta di Waukeen, guanto di Torm, stella
    di Mystra, disco di Shar, falce di Selûne, catene di Ilmater, corno dorato dell'Unicorno —
    sono originali della campagna.</p>
    <p><em>Icons made by Lorc, Delapouite and Caro Asercion</em> —
    <a href="https://game-icons.net">game-icons.net</a> — CC BY 3.0. Le figure sono state
    ricolorate, scalate e ritagliate dal riquadro originale. Attribuzione completa in
    <code>P2D-Palio-Allegati/stemmi/CREDITS.md</code>.</p>
    <p><b>Oro araldico</b> <code>#DFA93B</code> lega quattro scudi con lo stesso metallo:
    becco e zampe dell'Oca, stella di Mystra, falce di Sel&ucirc;ne, corno dell'Unicorno.
    Stella e falce sono canonicamente d'argento — l'oro &egrave; una scelta del DM, presa
    per leggibilit&agrave;. La Civetta resta interamente d'argento.</p>
    <p>Gli scudi sono montati su pergamena in entrambi i temi: i titoli sono dipinti
    dentro gli SVG nei colori del booklet, e su fondo scuro sparirebbero.</p>
    <p>In archivio e non usata: <code>stone-tower</code> (Lorc), variante alternativa per
    la Torre.</p>
    <p><b>Nomi e simboli delle divinit&agrave; di Golarion sono IP di Paizo Inc.</b> — uso
    non commerciale, da tavolo, nel perimetro della <em>Community Use Policy</em>. La serie
    Golarion <b>non</b> rende commercializzabile l'arco: il blocco assorbente resta l'IP
    Wizards of the Coast del resto della campagna.</p>
  </footer>
</div>
"""
OUT.write_text(page)
print(f"scritto {OUT}  ({len(page)//1024} KB)")
