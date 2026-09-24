#!/usr/bin/env python3
"""build_booklet_html.py — booklet HTML sfogliabile in stile «pergamena Homebrewery».

È il builder CANONICO dello stile usato per l'artefatto del Palio di
Channathgate (K-B3.7) e per i booklet di sessione: converte una lista di
master markdown in UNA pagina HTML autonoma (CSS incorporato, SVG inline,
immagini raster embeddate come data-URI), con copertina, tab per capitolo
e cornici stile Manuale del Giocatore.

I markdown restano i MASTER (ADR-0003): l'HTML è un artefatto generato,
rigenerabile in qualunque momento. Zero dipendenze obbligatorie (stdlib);
Pillow è OPZIONALE e serve solo a ricomprimere i dipinti >600 KB per
tenere il file leggero — senza Pillow l'immagine viene embeddata com'è.

Uso:
    python3 scripts/build_booklet_html.py MANIFEST.json [--out FILE.html]
    python3 scripts/build_booklet_html.py MANIFEST.json --format hb    # .hb.md V3
    python3 scripts/build_booklet_html.py MANIFEST.json --format both
    python3 scripts/dm.py booklet MANIFEST.json            (equivalente)

Doppia via (ADR-0013): lo STESSO manifest genera sia l'HTML autonomo
(immagini incorporate, zero server) sia il sorgente Homebrewery V3
``<out>.hb.md`` per l'editor a due pannelli self-hosted (nativo o Docker,
``dm.py hype``). Nel .hb.md le immagini restano riferimenti relativi.

Il manifest (JSON, percorsi relativi alla SUA cartella):
{
  "brand":    "RUMBLING STONE · ARC-07",
  "title":    "Lo Scontro con Terros",
  "subtitle": "sottotitolo in corsivo",
  "banner":   "BOOKLET DI SESSIONE",
  "meta":     "riga piccola in fondo alla copertina",
  "header":   "riga descrittiva sotto il titolo della pagina",
  "footer":   "etichetta a piè di pagina (capitoli DM)",
  "player_footer": "titolo EVOCATIVO per il piè delle pagine ✉ giocatore
                    (ADR-0013: mai il titolo reale; default: footer)",
  "intro_md": "intro-copertina.md",              # opzionale
  "cover_image": "immagini/tavola.png",           # opzionale
  "out":      "NOME-BOOKLET.html",                # opzionale (default: <stem>.html)
  "chapters": [
    {"title": "I · Regia", "file": "regia.md", "tag": "dm"},
    {"title": "Hint — Thorik", "file": "hint-thorik.md", "tag": "player"}
  ]
}
"tag": "dm" stampa ⚠ SOLO DM sul foglio; "player" stampa ✉ HANDOUT GIOCATORE;
assente = nessuna etichetta.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore.testo import riscala_link  # noqa: E402

# ---------------------------------------------------------------------------
# Lo stile «pergamena» canonico (identico all'anteprima visiva e all'artefatto
# del Palio). Se lo tocchi, tocchi TUTTI i booklet futuri: fallo di proposito.
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent

# ── la tipografia ────────────────────────────────────────────────────────────
# Fino al 2026-08-22 questi booklet usavano **Georgia**, che è un font di
# sistema: su una macchina che non ce l'ha il PDF cambia faccia, ed è il difetto
# [2] del capitolato del Drappo. La catena di stampa lo aveva già chiuso
# (ADR-0020) e questa no — cioè lo stesso capitolo, dato a due giocatori,
# usciva con due tipografie diverse.
#
# I `.woff2` stanno in `scripts/fonts/web/` (OFL, con la loro licenza accanto) e
# vengono incorporati in base64: un booklet è **un file solo** che si manda per
# posta, e un file solo non può andare a prendersi i font da qualche parte.
FONTS_WEB = ROOT / "scripts" / "fonts" / "web"
FACCE = (
    ("EB Garamond", "ebgaramond.woff2", "normal", "400 700"),
    ("EB Garamond", "ebgaramond-italic.woff2", "italic", "400 700"),
    ("Cinzel", "cinzel.woff2", "normal", "400 700"),
)


INCORPORA_FONT = True


def css_font_face() -> str:
    """Le `@font-face` col woff2 in base64, o stringa vuota se i file non ci sono."""
    if not INCORPORA_FONT:
        return ""
    fuori = []
    for famiglia, file, stile, peso in FACCE:
        f = FONTS_WEB / file
        if not f.is_file():
            print(f"  ⚠ font mancante: {f.relative_to(ROOT)} — il booklet userà i font di "
                  f"sistema (vedi scripts/fonts/README.md)", file=sys.stderr)
            return ""
        b64 = base64.b64encode(f.read_bytes()).decode()
        fuori.append(
            "@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;"
            "src:url(data:font/woff2;base64,%s) format('woff2');}" % (famiglia, stile, peso, b64)
        )
    return "\n".join(fuori)


CSS = """
  :root{
    --chrome-bg:#efe9dd; --chrome-ink:#3a3126; --chrome-line:#d8cdb8;
    --tab-bg:#e2d8c2; --tab-active:#58180D; --tab-active-ink:#f5edd6;
    --sheet:#EEE5CE; --ink:#2b241c; --rubric:#58180D; --brass:#c9ad6a;
    --note-bg:#e0e5c1; --desc-bg:#faf3e3; --banner:#B31515; --banner-ink:#f7ecd4;
    --shadow:0 10px 26px rgba(43,36,28,.35);
  }
  @media (prefers-color-scheme: dark){
    :root{ --chrome-bg:#221e19; --chrome-ink:#d8cdb8; --chrome-line:#3b342b;
           --tab-bg:#2f2921; --shadow:0 12px 30px rgba(0,0,0,.6); }
  }
  :root[data-theme="dark"]{ --chrome-bg:#221e19; --chrome-ink:#d8cdb8; --chrome-line:#3b342b;
           --tab-bg:#2f2921; --shadow:0 12px 30px rgba(0,0,0,.6); }
  :root[data-theme="light"]{ --chrome-bg:#efe9dd; --chrome-ink:#3a3126; --chrome-line:#d8cdb8;
           --tab-bg:#e2d8c2; --shadow:0 10px 26px rgba(43,36,28,.35); }

  body{ background:var(--chrome-bg); color:var(--chrome-ink);
        font-family:'EB Garamond',Georgia,'Times New Roman',serif; margin:0; }
  header.top{ padding:1.4rem 1rem .6rem; text-align:center; }
  header.top h1{ font-size:1.15rem; margin:0; letter-spacing:.06em; text-transform:uppercase; }
  header.top p{ margin:.35rem auto 0; max-width:46rem; font-size:.9rem; opacity:.8; font-style:italic; }

  nav.tabs{ display:flex; gap:.5rem; justify-content:center; flex-wrap:wrap;
            padding:.8rem 1rem 1.2rem; position:sticky; top:0;
            background:var(--chrome-bg); border-bottom:1px solid var(--chrome-line); z-index:5;
            max-width:64rem; margin:0 auto;}
  nav.tabs button{ font:inherit; font-size:.72rem; letter-spacing:.05em;
      padding:.35rem .6rem; border:1px solid var(--chrome-line);
      background:var(--tab-bg); color:var(--chrome-ink); cursor:pointer; border-radius:2px;}
  nav.tabs button[aria-selected="true"]{ background:var(--tab-active); color:var(--tab-active-ink);
      border-color:var(--tab-active); }
  nav.tabs button:focus-visible{ outline:2px solid var(--rubric); outline-offset:2px; }

  main{ display:flex; flex-direction:column; align-items:center; gap:2rem; padding:2rem .8rem 4rem; }
  section.pane{ display:none; flex-direction:column; gap:2rem; align-items:center; width:100%; }
  section.pane.on{ display:flex; }

  .sheet{ background:var(--sheet); color:var(--ink); width:min(52rem,100%);
      box-shadow:var(--shadow); padding:2.6rem 2.8rem 3.4rem; position:relative;
      background-image:radial-gradient(ellipse at 18% 8%, rgba(201,173,106,.16), transparent 55%),
                       radial-gradient(ellipse at 85% 95%, rgba(88,24,13,.07), transparent 50%);
      border:1px solid #d9ccab; }
  .sheet, .sheet table{ font-size:.94rem; line-height:1.45; }

  .cover{ text-align:center; display:flex; flex-direction:column; justify-content:center;
          min-height:34rem; gap:1rem;}
  .cover .brand{ letter-spacing:.35em; font-size:.8rem; color:var(--rubric); }
  .cover h2{ font-variant:small-caps; font-size:2.6rem; margin:.1em 0; color:var(--rubric);
             line-height:1.05; text-wrap:balance;}
  .cover h3{ font-style:italic; font-weight:normal; font-size:1.25rem; margin:0; }
  .rule{ border:none; height:3px; width:60%; margin:0.6rem auto;
         background:linear-gradient(90deg,transparent,var(--rubric),transparent); }
  .banner{ display:inline-block; margin:0 auto; background:var(--banner); color:var(--banner-ink);
      padding:.35rem 1.6rem; letter-spacing:.25em; font-size:.85rem;
      clip-path:polygon(4% 0,96% 0,100% 50%,96% 100%,4% 100%,0 50%); }
  .covermeta{ font-size:.8rem; font-style:italic; opacity:.85; max-width:34rem; margin:1.6rem auto 0;
      border-top:1px solid var(--brass); padding-top:.8rem;}

  .colophon{ max-width:34rem; margin:0 auto; }
  .colophon h4{ font-variant:small-caps; letter-spacing:.25em; color:var(--brass);
      text-align:center; font-size:.8rem; margin:0 0 .2rem; font-weight:normal; }
  .colophon .rule{ width:30%; margin-bottom:1.4rem; }
  .colophon dl{ display:grid; grid-template-columns:8.5rem 1fr; gap:.45rem .9rem; margin:0; }
  .colophon dt{ font-variant:small-caps; letter-spacing:.08em; color:var(--brass); font-size:.8rem; }
  .colophon dd{ margin:0; font-size:.92rem; }
  .colophon .licenza{ margin-top:1.3rem; padding-top:.8rem; border-top:1px solid var(--brass);
      font-style:italic; font-size:.85rem; opacity:.9; }
  .colophon .nota{ font-size:.8rem; opacity:.8; margin-top:.6rem; }

  .twocol{ column-count:2; column-gap:2.2rem; }
  @media (max-width:44rem){ .twocol{ column-count:1; } .sheet{ padding:1.6rem 1.2rem 2.4rem; } }
  .twocol > *{ break-inside:avoid; }

  .sheet h2.sec{ font-variant:small-caps; color:var(--rubric); font-size:1.5rem;
      margin:1.1rem 0 .3rem; border-bottom:2px solid var(--brass); padding-bottom:.15rem;
      column-span:all; text-wrap:balance;}
  .sheet h3.sub{ font-variant:small-caps; color:var(--rubric); font-size:1.12rem; margin:.9rem 0 .25rem;}
  .sheet h4.sub4{ font-variant:small-caps; color:var(--rubric); font-size:1rem; margin:.7rem 0 .2rem;}
  .sheet p{ margin:.45rem 0; text-align:justify; hyphens:auto;}
  .sheet .lede::first-letter{ font-size:3.1em; float:left; line-height:.82;
      padding:.04em .08em 0 0; color:var(--rubric); font-family:'Cinzel',Georgia,serif;}
  .sheet ul{ margin:.4rem 0 .7rem 1.2rem; padding:0;}
  .sheet ol{ margin:.4rem 0 .7rem 1.4rem; padding:0;}
  .sheet li{ margin:.22rem 0;}
  .atmo{ font-style:italic; text-align:center; margin:1rem 0;}

  .tablewrap{ overflow-x:auto; margin:.6rem 0 1rem; column-span:all;}
  .sheet table{ border-collapse:collapse; width:100%; min-width:34rem;}
  .sheet th{ background:var(--rubric); color:var(--banner-ink); text-align:left;
      padding:.3rem .55rem; font-variant:small-caps; font-weight:normal; letter-spacing:.04em;}
  .sheet td{ padding:.3rem .55rem; vertical-align:top; border-bottom:1px solid #d6c69c;}
  .sheet tbody tr:nth-child(odd){ background:rgba(201,173,106,.14); }

  .note,.desc{ padding:.8rem 1rem; margin:.9rem 0; break-inside:avoid; }
  .note{ background:var(--note-bg); border-top:3px solid var(--rubric);
         border-bottom:3px solid var(--rubric); box-shadow:2px 2px 0 rgba(43,36,28,.15);}
  .desc{ background:var(--desc-bg); border:2px solid var(--brass); position:relative;}
  .desc::before,.desc::after{ content:"❧"; position:absolute; color:var(--brass); font-size:.9rem;}
  .desc::before{ top:-2px; left:6px;} .desc::after{ bottom:-2px; right:6px; transform:rotate(180deg);}
  .note h4,.desc h4{ margin:.1rem 0 .35rem; font-variant:small-caps; color:var(--rubric); font-size:1rem;}
  .readaloud{ font-style:italic; }
  .vague{ font-style:italic; font-size:.86rem; opacity:.9; }

  pre.mono{ background:rgba(201,173,106,.18); border:1px solid var(--brass); padding:.6rem .8rem;
      overflow-x:auto; font-size:.8rem; line-height:1.35; font-family:ui-monospace,Consolas,monospace;}
  .figure{ margin:.8rem auto; text-align:center; }
  .figure svg{ max-width:100%; height:auto; border:1px solid var(--brass); background:#efe6cf;}
  .figure img{ max-width:100%; height:auto; border:1px solid var(--brass);}
  .figure.placeholder{ border:2px dashed var(--brass); padding:1.6rem; background:rgba(201,173,106,.12);}

  .pagefoot{ display:flex; justify-content:space-between; align-items:baseline;
      margin-top:2.2rem; border-top:1px solid var(--brass); padding-top:.5rem;
      font-size:.72rem; letter-spacing:.14em; color:var(--rubric); font-variant:small-caps;}
  .pagefoot .n{ font-family:'Cinzel',Georgia,serif; font-size:1rem; font-variant-numeric:tabular-nums;}
  .dmtag{ position:absolute; top:.9rem; right:1rem; font-size:.62rem; letter-spacing:.2em;
      color:var(--banner); border:1px solid var(--banner); padding:.15rem .5rem; }
  .pgtag{ position:absolute; top:.9rem; right:1rem; font-size:.62rem; letter-spacing:.2em;
      color:#2f5d31; border:1px solid #2f5d31; padding:.15rem .5rem; }
  .caption{ font-size:.78rem; text-align:center; opacity:.75; max-width:40rem; font-style:italic;}
  .printbtn{ position:fixed; right:1rem; bottom:1rem; z-index:9; font:inherit; font-size:.8rem;
      padding:.5rem .9rem; border:1px solid var(--chrome-line); border-radius:4px; cursor:pointer;
      background:var(--tab-active); color:var(--tab-active-ink); box-shadow:var(--shadow);}

  /* ── Stampa / PDF A4 (ADR-0013 §5): via testata e tab, resta SOLO la
     scheda attiva, pergamena a piena pagina, colori esatti. ───────────── */
  @media print{
    @page{ size:A4; margin:0; }
    header.top, nav.tabs, .printbtn{ display:none !important; }
    body{ background:var(--sheet); }
    main{ display:block; padding:0; }
    section.pane{ display:none; }
    section.pane.on{ display:block; }
    .sheet{ width:100%; box-sizing:border-box; min-height:calc(100vh - 2px);
            box-shadow:none; border:none; margin:0;
            padding:14mm 16mm 16mm; break-after:page;
            -webkit-print-color-adjust:exact; print-color-adjust:exact; }
    .sheet:last-child{ break-after:auto; }
    .tablewrap{ overflow-x:visible; }
    .sheet table{ min-width:0; }
    /* le mappe ASCII/emoji non hanno scrollbar su carta: si riducono
       quanto basta per stare nel foglio senza tagli */
    pre.mono{ font-size:.6rem; line-height:1.3; overflow:visible; }
  }
"""

TAGS = {"dm": '<span class="dmtag">⚠ SOLO DM</span>',
        "player": '<span class="pgtag">✉ HANDOUT GIOCATORE</span>'}

_SVG_CACHE: dict[Path, str] = {}


def load_svg(path: Path) -> str:
    if path not in _SVG_CACHE:
        try:
            s = path.read_text(encoding="utf-8")
            s = re.sub(r"<\?xml[^>]*\?>", "", s)
            s = re.sub(r'(<svg[^>]*?)\swidth="[^"]*"', r"\1", s, count=1)
            s = re.sub(r'(<svg[^>]*?)\sheight="[^"]*"', r"\1", s, count=1)
            _SVG_CACHE[path] = f'<div class="figure">{s}</div>'
        except OSError:
            _SVG_CACHE[path] = ""
    return _SVG_CACHE[path]


def inline_md(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*\*([^*]+)\*\*\*", r"<strong><em>\1</em></strong>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)  # link -> solo testo
    return s


def img_html(alt: str, src: str, base: Path) -> str:
    p = (base / src).resolve()
    if p.suffix.lower() == ".svg" and p.exists():
        return load_svg(p)
    if p.exists() and p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
        data = p.read_bytes()
        mime = mimetypes.guess_type(p.name)[0] or "image/png"
        if len(data) > 600_000:  # ricomprimi i dipinti per l'embed (Pillow opzionale)
            try:
                import io

                from PIL import Image

                im = Image.open(p).convert("RGB")
                im.thumbnail((1400, 1400), Image.LANCZOS)
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=82, optimize=True)
                data, mime = buf.getvalue(), "image/jpeg"
            except ImportError:
                pass
        b64 = base64.b64encode(data).decode()
        return (f'<div class="figure"><img alt="{html.escape(alt)}" '
                f'src="data:{mime};base64,{b64}"></div>')
    return (f'<div class="figure placeholder"><p class="vague">🖼 '
            f'<strong>{html.escape(alt or "tavola")}</strong><br>'
            f"<code>{html.escape(src)}</code><br>"
            f"la tavola apparirà qui appena il file sarà nel repo</p></div>")



# I prop sono sorgenti HOMEBREWERY (.hb.md): la loro sintassi a blocchi va
# tradotta o buttata, se no finisce STAMPATA LETTERALE — «{{descriptive»,
# «{{margin-top:60px}}» in mezzo al testo del contratto.
_HB_AUTO = re.compile(r"^\{\{[^{}\n]*\}\}\s*$")
_HB_APRE = re.compile(r"^\{\{(descriptive|note)\b[^}]*$")
_HB_ALTRO = re.compile(r"^\{\{\w[^}]*$")


def spoglia_homebrewery(testo: str) -> str:
    fuori, pila = [], []
    for ln in testo.split("\n"):
        s = ln.strip()
        if _HB_AUTO.match(s):                       # riga auto-chiusa: impaginazione
            continue
        m = _HB_APRE.match(s)
        if m:
            fuori.append('<div class="hb-' + m.group(1) + '">')
            pila.append("chiudi")
            continue
        if _HB_ALTRO.match(s):
            pila.append("scarta")
            continue
        if s == "}}":
            if pila and pila.pop() == "chiudi":
                fuori.append("</div>")
            continue
        fuori.append(re.sub(r"\{\{[^{}\n]*\}\}", "", ln))
    return "\n".join(fuori)

def md_to_html(md: str, base: Path) -> str:
    """Convertitore markdown→HTML minimale ma fedele ai master del repo:
    heading, tabelle, citazioni (→ cornice .desc), liste, code fence
    (→ blocco mono per le mappe ASCII), immagini (SVG inline / data-URI)."""
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    lines = md.splitlines()
    out: list[str] = []
    i, n = 0, len(lines)
    para: list[str] = []
    quote: list[str] = []
    ul: list[str] = []
    ol: list[str] = []
    table: list[str] = []
    code: list[str] | None = None

    def flush_para() -> None:
        if para:
            out.append(f'<p>{inline_md(" ".join(para))}</p>')
            para.clear()

    def flush_quote() -> None:
        # Le righe consecutive di un blockquote sono UN paragrafo (lazy
        # continuation md): unite prima di inline_md, così enfasi/citazioni
        # che proseguono a capo (\*«…\n…»\*) vengono chiuse correttamente.
        if quote:
            groups: list[list[str]] = [[]]
            for q in quote:
                if q.strip():
                    groups[-1].append(q.strip())
                elif groups[-1]:
                    groups.append([])
            inner = [f'<p class="readaloud">{inline_md(" ".join(g))}</p>'
                     for g in groups if g]
            out.append('<div class="desc">' + "".join(inner) + "</div>")
            quote.clear()

    def flush_ul() -> None:
        if ul:
            out.append("<ul>" + "".join(f"<li>{inline_md(x)}</li>" for x in ul) + "</ul>")
            ul.clear()

    def flush_ol() -> None:
        if ol:
            out.append("<ol>" + "".join(f"<li>{inline_md(x)}</li>" for x in ol) + "</ol>")
            ol.clear()

    def flush_table() -> None:
        if not table:
            return
        rows = [r for r in table if not re.match(r"^\s*\|?[\s:|-]+\|?\s*$", r)]
        parts = ['<div class="tablewrap"><table>']
        for k, r in enumerate(rows):
            cells = [c.strip() for c in r.strip().strip("|").split("|")]
            tag = "th" if k == 0 else "td"
            row = "<tr>" + "".join(f"<{tag}>{inline_md(c)}</{tag}>" for c in cells) + "</tr>"
            if k == 0 and len(rows) > 1:
                parts.append(f"<thead>{row}</thead><tbody>")
            else:
                parts.append(row)
        parts.append("</tbody></table></div>" if len(rows) > 1 else "</table></div>")
        out.append("".join(parts))
        table.clear()

    def flush_all() -> None:
        flush_para(); flush_quote(); flush_ul(); flush_ol(); flush_table()

    while i < n:
        ln = lines[i]
        if code is not None:
            if ln.strip().startswith("```"):
                out.append('<pre class="mono">' + html.escape("\n".join(code)) + "</pre>")
                code = None
            else:
                code.append(ln)
            i += 1
            continue
        s = ln.strip()
        if s.startswith("```"):
            flush_all()
            code = []
            i += 1
            continue
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", s)
        if m:
            flush_all()
            out.append(img_html(m.group(1), m.group(2), base))
            i += 1
            continue
        if not s:
            flush_all()
            i += 1
            continue
        if s.startswith("#"):
            flush_all()
            level = len(s) - len(s.lstrip("#"))
            text = inline_md(s.lstrip("#").strip())
            if level <= 2:
                out.append(f'<h2 class="sec">{text}</h2>')
            elif level == 3:
                out.append(f'<h3 class="sub">{text}</h3>')
            else:
                out.append(f'<h4 class="sub4">{text}</h4>')
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            flush_all()
            out.append('<hr class="rule">')
            i += 1
            continue
        if s.startswith(">"):
            flush_para(); flush_ul(); flush_ol(); flush_table()
            quote.append(s.lstrip(">").strip())
            i += 1
            continue
        if s.startswith("|"):
            flush_para(); flush_quote(); flush_ul(); flush_ol()
            table.append(s)
            i += 1
            continue
        m = re.match(r"^[-*+]\s+(.*)$", s)
        if m:
            flush_para(); flush_quote(); flush_ol(); flush_table()
            ul.append(m.group(1))
            i += 1
            continue
        m = re.match(r"^\d+[.)]\s+(.*)$", s)
        if m:
            flush_para(); flush_quote(); flush_ul(); flush_table()
            ol.append(m.group(1))
            i += 1
            continue
        if ul and (ln.startswith("  ") or ln.startswith("\t")):
            ul[-1] += " " + s
            i += 1
            continue
        if ol and (ln.startswith("  ") or ln.startswith("\t")):
            ol[-1] += " " + s
            i += 1
            continue
        para.append(s)
        i += 1
    flush_all()
    return "\n".join(out)


# Stesse voci e stesso ordine della catena di stampa (`VOCI_COLOPHON` in
# export_booklet_typst.py). Due catene che ordinano diversamente i crediti
# producono due edizioni diverse dello stesso volume: e' esattamente la
# divergenza che ADR-0020 aveva promesso di chiudere.
VOCI_COLOPHON = (
    ("edizione", "Edizione"),
    ("versione", "Versione"),
    ("data", "Data"),
    ("autori", "A cura di"),
    ("basato_su", "Basato su"),
)


def colophon_html(mf: dict, footer: str) -> str:
    """La pagina dei crediti, o stringa vuota se il manifest non ne dichiara una.

    Come in stampa: nessun valore dedotto: la data si scrive nel manifest, non
    si prende dall'orologio.
    """
    col = mf.get("colophon")
    if not isinstance(col, dict) or not col:
        return ""
    righe = "".join(
        f"<dt>{html.escape(etichetta)}</dt><dd>{html.escape(str(col[chiave]))}</dd>"
        for chiave, etichetta in VOCI_COLOPHON if col.get(chiave)
    )
    if not righe and not col.get("licenza") and not col.get("nota"):
        return ""
    licenza = (f'<p class="licenza">{html.escape(col["licenza"])}</p>'
               if col.get("licenza") else "")
    nota = f'<p class="nota">{html.escape(col["nota"])}</p>' if col.get("nota") else ""
    return (f'<div class="sheet"><div class="colophon"><h4>Colophon</h4>'
            f'<hr class="rule">'
            f'{f"<dl>{righe}</dl>" if righe else ""}{licenza}{nota}</div>'
            f'<div class="pagefoot"><span>{html.escape(footer)}</span></div></div>')


def build(manifest_path: Path, out_override: Path | None = None) -> Path:
    font_face = css_font_face()
    base = manifest_path.parent
    mf = json.loads(manifest_path.read_text(encoding="utf-8"))
    title = mf.get("title", "Booklet")
    footer = mf.get("footer", title)

    cover_img = ""
    if mf.get("cover_image"):
        cover_img = img_html(title, mf["cover_image"], base)
    intro_html = ""
    if mf.get("intro_md"):
        p = base / mf["intro_md"]
        intro_html = f'<div class="sheet">{md_to_html(p.read_text(encoding="utf-8"), p.parent)}' \
                     f'<div class="pagefoot"><span>{html.escape(footer)}</span>' \
                     f'<span class="n">1</span></div></div>'

    cover = f"""
<section class="pane on" id="c0">
  <div class="sheet cover">
    <div class="brand">{html.escape(mf.get("brand", "RUMBLING STONE"))}</div>
    <h2>{html.escape(title)}</h2>
    <h3>{html.escape(mf.get("subtitle", ""))}</h3>
    <hr class="rule">
    <div><span class="banner">{html.escape(mf.get("banner", "BOOKLET"))}</span></div>
    {cover_img}
    <p class="covermeta">{html.escape(mf.get("meta", ""))}</p>
  </div>
  {colophon_html(mf, footer)}
  {intro_html}
</section>"""

    # Anti-spoiler (ADR-0013 §3): le pagine ✉ dei giocatori NON devono mai
    # portare il titolo reale del booklet DM nel piè di pagina — usano il
    # titolo evocativo `player_footer` (fallback: footer, per i booklet
    # il cui titolo non è uno spoiler, es. il Palio).
    player_footer = mf.get("player_footer", footer)

    panes = [cover]
    tabs = ['<button role="tab" aria-selected="true" data-pane="c0">Copertina</button>']
    for k, ch in enumerate(mf["chapters"], 1):
        p = base / ch["file"]
        body = md_to_html(spoglia_homebrewery(p.read_text(encoding="utf-8")), p.parent)
        tag = TAGS.get(ch.get("tag", ""), "")
        foot = player_footer if ch.get("tag") == "player" else footer
        tabs.append(f'<button role="tab" aria-selected="false" data-pane="c{k}">'
                    f'{html.escape(ch["title"])}</button>')
        panes.append(f"""
<section class="pane" id="c{k}">
  <div class="sheet">{tag}
    <div class="chapter-body">{body}</div>
    <div class="pagefoot"><span>{html.escape(foot)} · {html.escape(ch["title"])}</span>
    <span class="n">{k + 1}</span></div>
  </div>
</section>""")

    page = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{font_face}{CSS}</style>
</head>
<body>
<header class="top">
  <h1>{html.escape(title)}</h1>
  <p>{html.escape(mf.get("header", ""))}</p>
</header>
<nav class="tabs" role="tablist">{"".join(tabs)}</nav>
<main>{"".join(panes)}</main>
<button class="printbtn" onclick="window.print()" title="Stampa/salva in PDF SOLO la scheda aperta (A4)">🖨 Salva PDF</button>
<script>
  const tabs=document.querySelectorAll('nav.tabs button');
  function show(id){{
    tabs.forEach(x=>x.setAttribute('aria-selected',x.dataset.pane===id));
    document.querySelectorAll('section.pane').forEach(p=>p.classList.toggle('on',p.id===id));
    window.scrollTo({{top:0}});
  }}
  tabs.forEach(b=>b.addEventListener('click',()=>{{
    show(b.dataset.pane); history.replaceState(null,'','#'+b.dataset.pane);
  }}));
  // deep-link #cN: apre direttamente quella scheda (usato anche
  // dall'export PDF headless — ADR-0013 §5)
  if(location.hash && document.getElementById(location.hash.slice(1)))
    show(location.hash.slice(1));
</script>
</body>
</html>
"""
    out = out_override or (base / mf.get("out", manifest_path.stem.replace(".manifest", "") + ".html"))
    out.write_text(page, encoding="utf-8")
    return out


HB_TAGS = {"dm": "{{note\n##### ⚠ SOLO DM\nQuesto capitolo è materiale del DM: non mostrarlo ai giocatori.\n}}",
           "player": "{{note\n##### ✉ HANDOUT GIOCATORE\nPagina da consegnare al giocatore indicato, in privato.\n}}"}


def build_hb(manifest_path: Path, out_override: Path | None = None) -> Path:
    """Via Homebrewery (ADR-0013): stesso manifest → sorgente V3 .hb.md
    per l'editor self-hosted (nativo o Docker, ``dm.py hype``)."""
    base = manifest_path.parent
    mf = json.loads(manifest_path.read_text(encoding="utf-8"))
    title = mf.get("title", "Booklet")
    parts = [
        f"<!-- GENERATO da scripts/build_booklet_html.py --format hb (ADR-0013).\n"
        f"     Manifest: {manifest_path.name} — i capitoli CITANO i master (ADR-0003).\n"
        f"     Le immagini restano riferimenti relativi al repo: per la resa con\n"
        f"     immagini incorporate usa la via HTML (--format html). -->\n",
        "{{frontCover}}\n",
        "{{logo ![](/assets/naturalCritLogoRed.svg)}}\n",
        f"# {mf.get('brand', 'RUMBLING STONE').split('·')[0].strip()}",
        f"## {title}",
        "___\n",
        f"### {mf.get('subtitle', '')}\n",
        f"{{{{banner {mf.get('banner', 'BOOKLET')}}}}}\n",
        f"{{{{footnote\n  {mf.get('meta', '')}\n}}}}\n",
    ]
    # La destinazione si calcola PRIMA di incorporare i capitoli: serve a
    # riscalare i loro link relativi. Un capitolo in `07_arco/X.md` che linka
    # `../plans/adr/Y.md` punta alla radice del repo; incorporato alla lettera
    # in `07_arco/homebrew/sessione/BOOKLET.hb.md` — due livelli piu' in basso —
    # lo stesso link finisce su `07_arco/homebrew/plans/adr/Y.md`, che non
    # esiste. Erano **41 link rotti su 44** in otto booklet (lotto E1).
    html_out = out_override or (base / mf.get("out", manifest_path.stem.replace(".manifest", "") + ".html"))
    stem = html_out.name[:-5] if html_out.name.endswith(".html") else html_out.name
    out = html_out.parent / (stem + ".hb.md")
    dest = out.resolve().parent

    def _incorpora(sorgente: Path) -> str:
        return riscala_link(sorgente.read_text(encoding="utf-8"),
                            sorgente.resolve().parent, dest)

    if mf.get("intro_md"):
        parts += ["\\page\n", _incorpora(base / mf["intro_md"])]
    for ch in mf["chapters"]:
        parts.append("\n\\page\n")
        parts.append(f"# {ch['title']}\n")
        tag = HB_TAGS.get(ch.get("tag", ""))
        if tag:
            parts.append(tag + "\n")
        parts.append(_incorpora(base / ch["file"]))
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("manifest", help="manifest JSON del booklet (vedi docstring)")
    ap.add_argument("--out", help="file HTML di output (default: dal manifest)")
    ap.add_argument("--no-font-embed", action="store_true",
                    help="non incorporare i caratteri: file molto più leggero, ma il "
                         "booklet cambia faccia dove EB Garamond non è installato")
    ap.add_argument("--format", choices=["html", "hb", "both"], default="html",
                    help="html = pagina autonoma con immagini incorporate; "
                         "hb = sorgente Homebrewery V3 (.hb.md) per il self-hosted/Docker; "
                         "both = entrambi (ADR-0013)")
    args = ap.parse_args(argv)
    global INCORPORA_FONT
    INCORPORA_FONT = not args.no_font_embed
    mp = Path(args.manifest)
    if not mp.exists():
        print(f"ERRORE: manifest non trovato: {mp}", file=sys.stderr)
        return 2
    if args.format in ("html", "both"):
        out = build(mp, Path(args.out) if args.out else None)
        print(f"OK {out} ({out.stat().st_size / 1024:.0f} KB)")
    if args.format in ("hb", "both"):
        out = build_hb(mp, Path(args.out) if args.out else None)
        print(f"OK {out} ({out.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
