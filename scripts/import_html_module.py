"""import_html_module.py — un modulo scritto in HTML diventa un master markdown.

Perche' esiste (ADR-0003, lotto F4). `10-stand-alone/L'abbazia Della Rotta
Sicura/` e' nato come quattro pagine HTML autonome, con lo stile dentro il file e
le tavole disegnate in SVG in linea. E' bello e si apre nel browser, ma sta
**fuori da entrambe le catene**: niente colophon, niente edizione da stampa,
niente segnalibri, e ogni modifica di stile va rifatta quattro volte. Il repo ha
gia' deciso il contrario: il markdown e' il master, l'impaginato e' un artefatto.

Questo convertitore fa il travaso **una volta sola**, e non e' un `pandoc`
generico: conosce il vocabolario di questa famiglia di documenti e lo traduce in
quello che le due catene sanno gia' leggere.

    .ra          il read-aloud            →  blockquote (la cornice `.desc`)
    .warn .adr   avvisi e note di regia   →  {{note ...}}
    .mech .sb    meccanica e statblocchi  →  {{note ...}} con l'etichetta in neretto
    .entry       una voce d'area          →  #### <codice> Nome
    figure+svg   una tavola in linea      →  file .svg separato + ![didascalia]()
    .meta .cols  impaginazione            →  scartati (li rifa' la catena)

Le tavole SVG **escono dal documento**: e' la parte che conta. Un disegno dentro
la prosa non si puo' riusare, non si puo' aprire in un editor vettoriale e non si
puo' citare da un altro file. Fuori, diventa un asset come gli altri.

    python3 scripts/import_html_module.py "10-stand-alone/L'abbazia Della Rotta Sicura"
    python3 scripts/import_html_module.py <cartella> --dry-run    # non scrive niente

⚠️ **Non e' idempotente sul contenuto gia' convertito**: si lancia sull'HTML
originale, si rilegge l'output, e da li' in poi il master e' il markdown. L'HTML
resta nel repo come *edizione di riferimento* finche' il DM non dice il
contrario — cancellarlo e' una decisione sua, non di questo script.

Solo stdlib.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore.testo import slug  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Blocchi che diventano una cornice `{{note}}` nella catena. La chiave e'
# l'etichetta che si antepone in neretto, perche' «attenzione» e «meccanica» non
# sono la stessa cosa e il lettore deve continuare a distinguerle.
CORNICI = {
    "warn": "⚠ ",
    "adr": "",
    "mech": "",
    "sb": "",
    "note": "",
    "find": "",
    "myst": "",
    "meta": "",
}
#: Contenitori di sola impaginazione: si scartano, il loro contenuto no.
TRASPARENTI = {"page", "cols", "wrap", "entry", "chips"}
#: Blocchi che non sono contenuto: spariscono con tutto quello che hanno dentro.
#: Vuoto per ora — e ci resta finche' non c'e' un caso vero. `meta` ci stava, ed
#: era un errore: quella barra dice *«Sostituisce: Tavola I e il blocco Il conto
#: che non torna»*, cioe' il rapporto fra un'appendice e il documento
#: principale. Buttarla via non toglieva impaginazione, toglieva informazione.
SCARTA: set[str] = set()

#: SVG e' XML, e XML e' **case-sensitive**; `html.parser` invece minuscola tutto.
#: Senza questa tabella la tavola estratta perde il `viewBox` (e si impagina alla
#: dimensione naturale) e i `patternUnits`, che tornano al default
#: `objectBoundingBox`: il riempimento del mare smette di essere una texture e
#: diventa **un quadratino azzurro nell'angolo**. Il file resta XML valido e
#: nessun controllo se ne accorge — si vede solo guardando la pagina.
CAMEL = {n.lower(): n for n in (
    "viewBox preserveAspectRatio patternUnits patternTransform patternContentUnits "
    "gradientUnits gradientTransform spreadMethod clipPathUnits maskUnits "
    "maskContentUnits filterUnits primitiveUnits markerWidth markerHeight "
    "markerUnits refX refY stdDeviation baseFrequency numOctaves startOffset "
    "textLength lengthAdjust pathLength attributeName repeatCount keyTimes "
    "keySplines calcMode xChannelSelector yChannelSelector edgeMode targetX "
    "targetY surfaceScale specularConstant specularExponent diffuseConstant "
    "kernelMatrix tableValues limitingConeAngle pointsAtX pointsAtY pointsAtZ "
    "requiredFeatures requiredExtensions systemLanguage baseProfile "
    "linearGradient radialGradient clipPath textPath foreignObject "
    "feGaussianBlur feTurbulence feColorMatrix feComposite feOffset feBlend "
    "feDisplacementMap feMerge feMergeNode feFlood feDropShadow"
).split()}


def _camel(nome: str) -> str:
    """Il nome com'e' scritto nello standard SVG, non come l'ha minuscolato il parser."""
    return CAMEL.get(nome, nome)


#: Elementi SVG (e HTML) senza contenuto: si autochiudono e non prendono mai un
#: tag di chiusura. `html.parser` li consegna come start **e** end, e senza
#: questa lista la tavola estratta esce con `<path/></path>` — XML non valido, e
#: il difetto non si vede finche' non la apri in un lettore severo.
VUOTI = {"path", "rect", "circle", "line", "polygon", "polyline", "ellipse",
         "use", "stop", "image", "br", "img", "hr", "input", "meta", "link"}

_SPAZI = re.compile(r"[ \t ]+")


def _pulisci(s: str) -> str:
    return _SPAZI.sub(" ", s).strip()


class Convertitore(HTMLParser):
    """Da HTML a markdown, per il vocabolario di questa famiglia di documenti.

    Non e' un convertitore generale e non finge di esserlo: davanti a un tag che
    non conosce lascia passare il contenuto e **lo dice** (`self.ignoti`), invece
    di inventare una traduzione. Un travaso silenzioso e' peggio di uno rumoroso.
    """

    def __init__(self, tavole_dir: Path, prefisso: str, dry: bool) -> None:
        super().__init__(convert_charrefs=True)
        self.tavole_dir, self.prefisso, self.dry = tavole_dir, prefisso, dry
        self.out: list[str] = []
        self.buf: list[str] = []
        self.ignoti: set[str] = set()
        self.tavole: list[str] = []
        self.titolo = ""
        self.sottotitolo = ""
        self.meta: list[str] = []
        self._in_body = False
        self._scarta = 0
        self._svg: list[str] | None = None
        #: I <defs> condivisi in testa al documento (pattern di riempimento,
        #: marker delle frecce). Nell'HTML stavano in un <svg width="0"> a parte
        #: e ogni tavola li citava con url(#rock). Una tavola estratta che li
        #: lasciasse indietro si aprirebbe **senza i riempimenti**, e il difetto
        #: non si vede finche' non apri il file: per questo si copiano dentro
        #: ogni tavola, che cosi' e' autonoma davvero.
        self.defs = ""
        self._raccogli_defs = False
        self._cornice: list[str] | None = None
        self._etichetta = ""
        self._meta_bar = False
        self._ra = False
        self._lista: str | None = None
        self._tab: list[list[str]] | None = None
        self._cella: list[str] | None = None
        self._h: int | None = None
        self._sub = False
        self._meta = 0
        self._caption: list[str] | None = None
        self._pre = False

    # ---- utilita' -------------------------------------------------------
    def _testo(self) -> str:
        t = _pulisci("".join(self.buf))
        self.buf.clear()
        return t

    def _chiudi_enfasi(self, marca: str) -> None:
        """Chiude un neretto/corsivo, **oppure** ne annulla l'apertura se e' vuoto.

        `<b></b>` esiste nei documenti veri (una cella che doveva avere
        un'etichetta e non ce l'ha). Lasciarlo passare produce `****`, che il
        markdown legge come l'inizio di un neretto che non finisce piu'.
        """
        if self.buf and self.buf[-1] == marca:
            self.buf.pop()
            return
        self.buf.append(marca)

    def _emetti(self, s: str) -> None:
        dove = self._cornice if self._cornice is not None else self.out
        if s or (dove and dove[-1] != ""):
            dove.append(s)

    def _chiudi_para(self) -> None:
        t = self._testo()
        if t:
            self._emetti(t)
            self._emetti("")

    # ---- tag ------------------------------------------------------------
    def handle_starttag(self, tag: str, attrs_l: list[tuple[str, str | None]]) -> None:
        attrs = {k: (v or "") for k, v in attrs_l}
        cls = set(attrs.get("class", "").split())

        if tag == "body":
            self._in_body = True
            return
        if not self._in_body or self._scarta:
            if self._scarta and tag == "div":
                self._scarta += 1
            return

        if self._svg is not None:                      # dentro una tavola
            self._svg.append(self._raw_tag(tag, attrs_l))
            return

        if tag == "svg":
            if attrs.get("width") == "0":              # <defs> condivisi, non una tavola
                self._svg, self._raccogli_defs = [], True
                return
            self._svg = [self._raw_tag(tag, attrs_l)]
            return

        if tag in ("script", "style"):
            self._scarta = 1
            return

        if tag == "div":
            if cls & SCARTA:
                self._scarta = 1
                return
            for c in cls:
                if c in CORNICI:
                    self._chiudi_para()
                    self._cornice, self._etichetta = [], CORNICI[c]
                    self._meta_bar = c == "meta"
                    return
            if not (cls & TRASPARENTI):
                self.ignoti.add(f"div.{'.'.join(sorted(cls)) or '?'}")
            return

        if tag in ("h1", "h2", "h3", "h4", "h5"):
            self._chiudi_para()
            self._h = int(tag[1])
            return
        if tag == "p":
            self._chiudi_para()
            self._sub = "sub" in cls
            # Il read-aloud. E' la cosa che si LEGGE al tavolo, ed e' l'unica
            # classe di questo vocabolario che ha gia' una forma nel repo: il
            # blockquote, che entrambe le catene rendono come cornice `.desc`.
            # Lasciarla cadere in un paragrafo qualunque significa consegnare al
            # DM un master in cui non si distingue piu' cosa si legge ad alta
            # voce e cosa si riassume.
            self._ra = "ra" in cls
            return
        if tag in ("ul", "ol"):
            self._chiudi_para()
            self._lista = "-" if tag == "ul" else "1."
            return
        if tag == "li":
            self.buf.clear()
            return
        if tag == "table":
            self._chiudi_para()
            self._tab = []
            return
        if tag == "tr" and self._tab is not None:
            self._tab.append([])
            return
        if tag in ("th", "td") and self._tab is not None:
            self._cella = []
            self.buf.clear()
            return
        if tag == "figcaption":
            self._caption = []
            self.buf.clear()
            return
        if tag in ("b", "strong"):
            self.buf.append("**")
            return
        if tag in ("i", "em"):
            self.buf.append("*")
            return
        if tag == "code":
            self.buf.append("`")
            return
        if tag == "br":
            # Uno statblocco e' fatto di righe: «PF …», «Att …», «TS …». Il
            # <br> le separava. Se lo si lascia diventare uno spazio, la catena
            # unisce tutto in un paragrafo unico e lo statblocco smette di
            # essere consultabile — che al tavolo e' l'unica cosa che deve fare.
            # Ogni segmento esce come riga a se': la cornice le tiene insieme.
            #
            # Ma **non dentro una cella o una voce di elenco**: li' una riga
            # markdown non ci sta, e chiudere il paragrafo sparerebbe il testo
            # fuori dal blocco. Era il difetto vero — `<td><b>Dama Orsola
            # Rive</b><br>guerriero 5</td>` perdeva il nome dalla tabella e lo
            # accodava, insieme agli altri due, a un paragrafo di nomi incollati.
            if self._cella is not None or self._lista:
                self.buf.append(" · ")
                return
            self._chiudi_para()
            return
        if tag == "a":
            self.buf.append("[")
            self._href = attrs.get("href", "")
            return
        if tag == "img":
            self._emetti(f"![{attrs.get('alt','')}]({attrs.get('src','')})")
            return
        if tag == "pre":
            self._pre = True
            self._chiudi_para()
            self._emetti("```")
            return
        if tag == "span":
            if "nm" in cls:          # il nome di uno statblocco
                self.buf.append("**")
                self._nm = True
            elif self._meta_bar:     # una voce della barra: riga a se'
                self._chiudi_para()
            return
        if tag in ("figure", "dl", "dt", "dd", "small", "sup", "tbody",
                   "thead", "input", "hr", "u", "s"):
            return
        self.ignoti.add(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == "body":
            self._in_body = False
            return
        if not self._in_body:
            return
        if self._scarta:
            if tag in ("div", "svg", "script", "style"):
                self._scarta -= 1
            return

        if self._svg is not None:
            if tag not in VUOTI:
                self._svg.append(f"</{_camel(tag)}>")
            if tag == "svg":
                if self._raccogli_defs:
                    corpo = "".join(self._svg)
                    m = re.search(r"<defs>(.*)</defs>", corpo, re.S)
                    self.defs = m.group(1) if m else ""
                    self._svg, self._raccogli_defs = None, False
                else:
                    self._salva_tavola()
            return

        if tag in ("h1", "h2", "h3", "h4", "h5") and self._h:
            t = self._testo()
            if self._h == 1 and not self.titolo:
                self.titolo = t
            else:
                self._emetti("#" * self._h + " " + t)
                self._emetti("")
            self._h = None
            return
        if tag == "p":
            t = self._testo()
            if self._sub and not self.sottotitolo:
                self.sottotitolo = t
            elif t and self._ra:
                self._emetti(f"> *{t}*")
                self._emetti("")
            elif t:
                self._emetti(t)
                self._emetti("")
            self._sub = self._ra = False
            return
        if tag == "li" and self._lista:
            t = self._testo()
            if t:
                self._emetti(f"{self._lista} {t}")
            return
        if tag in ("ul", "ol"):
            self._lista = None
            self._emetti("")
            return
        if tag in ("th", "td") and self._cella is not None:
            if self._tab and self._tab[-1] is not None:
                self._tab[-1].append(self._testo().replace("|", "\\|") or " ")
            self._cella = None
            return
        if tag == "table" and self._tab is not None:
            self._tabella()
            return
        if tag == "figcaption":
            t = self._testo()
            if t and self.tavole:
                # la didascalia sostituisce l'alt della riga ![] appena emessa
                for i in range(len(self.out) - 1, -1, -1):
                    if self.out[i].startswith("!["):
                        src = self.out[i].split("](", 1)[1]
                        self.out[i] = f"![{t}]({src}"
                        break
            self._caption = None
            return
        if tag in ("b", "strong"):
            self._chiudi_enfasi("**")
            return
        if tag == "span" and getattr(self, "_nm", False):
            self._chiudi_enfasi("**")
            self._nm = False
            return
        if tag in ("i", "em"):
            self._chiudi_enfasi("*")
            return
        if tag == "code":
            self._chiudi_enfasi("`")
            return
        if tag == "a":
            self.buf.append(f"]({self._href})")
            return
        if tag == "pre":
            self._emetti(self._testo())
            self._emetti("```")
            self._emetti("")
            self._pre = False
            return
        if tag == "div" and self._cornice is not None:
            self._chiudi_para()
            self._meta_bar = False
            corpo = [x for x in self._cornice if x.strip()]
            self._cornice = None
            if corpo:
                if self._etichetta:
                    # Mai davanti a un blockquote: `⚠ > *…*` non e' piu' una
                    # citazione, e' una riga di testo che comincia per «⚠ >».
                    # Succede quando un read-aloud sta dentro un riquadro
                    # d'avviso — e succede davvero, tre volte nell'Abbazia.
                    if corpo[0].startswith(">"):
                        corpo.insert(0, self._etichetta.strip())
                    else:
                        corpo[0] = self._etichetta + corpo[0]
                self.out.append("{{note")
                self.out.extend(corpo)
                self.out.append("}}")
                self.out.append("")
            return

    def handle_data(self, data: str) -> None:
        if not self._in_body or self._scarta:
            return
        if self._svg is not None:
            self._svg.append(data)
            return
        self.buf.append(data if self._pre else data.replace("\n", " "))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """`<path ... />` e' gia' chiuso: non deve arrivargli anche un `</path>`."""
        if self._svg is not None:
            self._svg.append(self._raw_tag(tag, attrs))
            return
        self.handle_starttag(tag, attrs)
        if tag not in VUOTI:
            self.handle_endtag(tag)

    # ---- pezzi ----------------------------------------------------------
    @staticmethod
    def _raw_tag(tag: str, attrs: list[tuple[str, str | None]]) -> str:
        a = "".join(f' {_camel(k)}="{v}"' for k, v in attrs if v is not None)
        return f"<{_camel(tag)}{a}{'/>' if tag in VUOTI else '>'}"

    def _salva_tavola(self) -> None:
        assert self._svg is not None
        n = len(self.tavole) + 1
        nome = f"{self.prefisso}-tavola-{n}.svg"
        corpo = "".join(self._svg)
        corpo = corpo.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        if self.defs:
            i = corpo.index(">") + 1
            corpo = corpo[:i] + f"<defs>{self.defs}</defs>" + corpo[i:]
        if not self.dry:
            self.tavole_dir.mkdir(parents=True, exist_ok=True)
            (self.tavole_dir / nome).write_text(
                '<?xml version="1.0" encoding="UTF-8"?>\n' + corpo + "\n",
                encoding="utf-8")
        self.tavole.append(nome)
        self._svg = None
        self._chiudi_para()
        self._emetti(f"![Tavola {n}]({self.tavole_dir.name}/{nome})")
        self._emetti("")

    def _tabella(self) -> None:
        righe = [r for r in (self._tab or []) if r]
        self._tab = None
        if not righe:
            return
        larg = max(len(r) for r in righe)
        righe = [r + [" "] * (larg - len(r)) for r in righe]
        self._emetti("| " + " | ".join(righe[0]) + " |")
        self._emetti("|" + "---|" * larg)
        for r in righe[1:]:
            self._emetti("| " + " | ".join(r) + " |")
        self._emetti("")

    @staticmethod
    def _compatta_titoli(testo: str) -> str:
        """Nessun livello di titolo salta il precedente.

        Nell'HTML l'`<h4>` di una voce d'area sotto un `<h2>` era una scelta
        **visiva** — un titolo piu' piccolo. In un documento strutturato e' un
        difetto: `h2 → h4` salta l'h3, e chi legge col lettore di schermo, o
        guarda i segnalibri del PDF, trova un ramo dell'albero che non esiste.
        veraPDF lo dice con le stesse parole (PDF/UA 7.4.2-1) su tre punti di
        questo modulo, e sono gli stessi tre.
        """
        fuori, prec = [], 0
        for riga in testo.split("\n"):
            m = re.match(r"^(#{1,6}) (.*)$", riga)
            if m:
                liv = len(m.group(1))
                if prec and liv > prec + 1:
                    liv = prec + 1
                prec = liv
                riga = "#" * liv + " " + m.group(2)
            fuori.append(riga)
        return "\n".join(fuori)

    def markdown(self) -> str:
        self._chiudi_para()
        testo = self._compatta_titoli("\n".join(self.out))
        testo = re.sub(r"\n{3,}", "\n\n", testo)
        # NIENTE ripulitura di «** **» qui. C'era, ed era sbagliata: fra due
        # neretti adiacenti (`<span class="nm">…megere</span> <b>Grinza</b>`)
        # cancellava lo spazio insieme agli asterischi e produceva
        # «megereGrinza» — una parola che non esiste, dentro un nome proprio.
        # Un neretto vuoto si evita all'origine: vedi `_chiudi_enfasi`.
        testo = re.sub(r" +([,.;:!?»])", r"\1", testo)
        testo = re.sub(r"(?m)^[ \t]+", "", testo)   # rientri lasciati dai <br>
        testo = re.sub(r"(?m)[ \t]+$", "", testo)
        return testo.strip() + "\n"


#: La firma della catena HTML nei suoi artefatti. Vale piu' di un nome di file:
#: il nome lo cambia chiunque, questo no.
_FIRME = ("@font-face", 'class="pagefoot"', 'class="chapter-body"')


def _generato(f: Path) -> bool:
    """Vero se questo HTML l'ha prodotto `build_booklet_html.py`."""
    testa = f.read_text(encoding="utf-8", errors="ignore")[:20000]
    return sum(s in testa for s in _FIRME) >= 2


def converti(sorgente: Path, dest: Path, tavole: Path, dry: bool) -> tuple[str, Convertitore]:
    c = Convertitore(tavole, slug(sorgente.stem), dry)
    c.feed(sorgente.read_text(encoding="utf-8"))
    corpo = c.markdown()
    testa = f"# {c.titolo}\n\n" if c.titolo else ""
    if c.sottotitolo:
        testa += f"*{c.sottotitolo}*\n\n"
    return testa + corpo, c


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("modulo", type=Path, help="cartella del modulo HTML")
    ap.add_argument("--dry-run", action="store_true", help="non scrive niente")
    ap.add_argument("--force", action="store_true",
                    help="sovrascrive master markdown gia' esistenti (li perde)")
    ap.add_argument("--manifest", action="store_true",
                    help="scrive anche un manifest di partenza accanto ai master")
    a = ap.parse_args(argv)

    mod = a.modulo if a.modulo.is_absolute() else ROOT / a.modulo
    if not mod.is_dir():
        print(f"✗ import_html_module: {a.modulo} non è una cartella", file=sys.stderr)
        return 1
    # Un HTML generato dalla catena non e' una sorgente da riconvertire: senza
    # questo filtro il convertitore, lanciato due volte, si mangia il proprio
    # output e produce un master markdown fatto di `div.sheet` e `div.pagefoot`.
    pagine = [f for f in sorted(mod.glob("*.html")) if not _generato(f)]
    if not pagine:
        print(f"✗ import_html_module: nessun .html in {a.modulo}", file=sys.stderr)
        return 1

    # Il travaso e' **una volta sola**. Dal momento in cui esiste, il master e'
    # il markdown: ci si correggono le chiavi d'area, ci si rilegge la prosa, e
    # rilanciare il convertitore vorrebbe dire buttare via quel lavoro senza
    # dirlo. L'HTML resta come edizione di riferimento, non come sorgente viva.
    gia = [f for p in pagine if (f := mod / f"{p.stem}.md").exists()]
    if gia and not (a.force or a.dry_run):
        print("✗ import_html_module: esistono gia' dei master markdown — il "
              "travaso e' una volta sola.\n  " +
              "\n  ".join(str(f.relative_to(mod)) for f in gia) +
              "\n  Se sai cosa stai facendo: --force (perdi le modifiche fatte "
              "sul markdown).", file=sys.stderr)
        return 1

    tavole = mod / "tavole"
    fatti, ignoti = [], set()
    for p in pagine:
        md, c = converti(p, mod, tavole, a.dry_run)
        out = mod / f"{p.stem}.md"
        if not a.dry_run:
            out.write_text(md, encoding="utf-8")
        ignoti |= c.ignoti
        fatti.append((out, c, len(md.splitlines())))
        print(f"  {p.name} → {out.name}  ({len(md.splitlines())} righe, "
              f"{len(c.tavole)} tavole estratte)")

    if a.manifest and not a.dry_run:
        capitoli = [{"title": c.titolo or o.stem, "file": o.name, "tag": "dm"}
                    for o, c, _ in fatti]
        principale = max(fatti, key=lambda x: x[2])[1]
        mf = {
            "title": principale.titolo or mod.name,
            "subtitle": principale.sottotitolo,
            "chapters": capitoli,
        }
        (mod / f"{slug(mod.name)}.manifest.json").write_text(
            json.dumps(mf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  manifest di partenza: {slug(mod.name)}.manifest.json")

    if ignoti:
        print(f"  ⚠ tag/classi non tradotti (contenuto lasciato passare): "
              f"{', '.join(sorted(ignoti))}")
    print(f"{'· dry-run ·' if a.dry_run else '✓'} import_html_module: "
          f"{len(fatti)} pagine convertite")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
