#!/usr/bin/env python3
"""export_booklet_typst.py — l'edizione da stampa: UN volume, segnalibri veri (ADR-0020).

`export_booklet_pdf.py` stampa con Chromium e produce **un PDF per scheda**: va
benissimo per mandare una pagina a un giocatore, ma il browser impagina pagine
web, non libri — niente controllo su vedove e orfane, niente crenatura fine,
niente indice cliccabile degno, e i font restano quelli di sistema.

Questo esportatore affianca quella catena **senza sostituirla**: legge lo stesso
manifest, converte i master markdown in sorgente Typst e produce **un volume
unico** con tipografia embedded (EB Garamond + Cinzel, OFL, in `typst/fonts/`),
due colonne, fregi di capitolo e segnalibri PDF generati dagli heading.

    schermo  →  build_booklet_html.py  →  .html + .hb.md      (invariato)
    stampa   →  export_booklet_typst.py →  un PDF con indice   (questo)

**Le schede pregenerate non sono un capitolo.** Un capitolo di manuale si legge;
una scheda si tiene in mano per tre sessioni. Un capitolo del manifest marcato
`"layout": "schede"` viene quindi impaginato con `typst/scheda-pg.typ`: **una
pagina A4 per personaggio**, fascia alta col ritratto, pannello sinistro con chi
sei, pannello destro con lo statblocco, e in fondo «come si gioca in un minuto».
I dati arrivano dagli stessi master markdown del tavolo (ADR-0003) — nessuna
copia dei numeri da qualche parte, quindi nessuna copia che possa restare
vecchia.

Uso:
    python3 scripts/export_booklet_typst.py MANIFEST.json            # solo pagine ✉ player
    python3 scripts/export_booklet_typst.py MANIFEST.json --all      # tutto, DM incluso
    python3 scripts/export_booklet_typst.py MANIFEST.json --keep-typ # conserva il sorgente .typ
    python3 scripts/export_booklet_typst.py MANIFEST.json --list     # elenca i capitoli

Dipendenze: stdlib + il binario `typst` (https://github.com/typst/typst,
Apache 2.0). Se manca, lo script **dice come installarlo ed esce pulito**, senza
lasciare file a metà: la catena HTML continua a funzionare da sola.

Rigenera l'esemplare con:
    python3 scripts/export_booklet_typst.py \\
        STANDALONE-Il-Drappo-di-Tarsilia/homebrew/DRAPPO-BOOKLET-DM.manifest.json --all

Exit code: 0 = ok · 1 = binario assente o compilazione fallita · 2 = uso errato.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore.schede import Scheda, SchedaError, leggi_schede  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEMA = ROOT / "scripts" / "typst" / "tema-rumblingstone.typ"
SCHEDA_PG = ROOT / "scripts" / "typst" / "scheda-pg.typ"
FONTS = ROOT / "scripts" / "typst" / "fonts"

INSTALLA = """\
Il binario «typst» non è nel PATH. È un singolo eseguibile, Apache 2.0:

  Linux/macOS   curl -sSL https://github.com/typst/typst/releases/latest/download/\\
                  typst-x86_64-unknown-linux-musl.tar.xz | tar xJ
                  sudo install typst-*/typst /usr/local/bin/
  Fedora/Bazzite  brew install typst        (oppure il tarball qui sopra)
  Arch            pacman -S typst
  Windows         winget install --id Typst.Typst

Niente panico se non lo installi: `export_booklet_pdf.py` continua a produrre i
PDF per capitolo con Chromium. Questo esportatore serve al volume da stampa.
"""


def typ_path(p: Path) -> str:
    """Con `--root`, in Typst i percorsi assoluti sono RELATIVI ALLA RADICE.

    Passare il percorso del filesystem fa cercare `/home/...` dentro la radice e
    fallisce: è l'errore che si prende chiunque monti Typst la prima volta.
    """
    return "/" + p.resolve().relative_to(ROOT).as_posix()


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-") or "capitolo"


# ── markdown → Typst ─────────────────────────────────────────────────────────
# Copre il sottoinsieme che i master del repo usano davvero. Ogni caso in più va
# aggiunto QUI e non nel .typ generato, che è un artefatto.

# `~` in Typst è uno spazio unificatore e `[` `]` delimitano il contenuto: se non
# si scappano, `+ ~200 mo` si stampa «+  200 mo» — il numero resta, la tilde
# sparisce, e nessuno se ne accorge finché non lo legge un giocatore.
_SPECIALI = ("\\", "#", "$", "@", "<", ">", "*", "_", "`", "[", "]", "~")


def _esc(s: str) -> str:
    for ch in _SPECIALI:
        s = s.replace(ch, f"\x00{ord(ch)}\x00")
    return s


def _unesc(s: str) -> str:
    return re.sub(r"\x00(\d+)\x00", lambda m: "\\" + chr(int(m.group(1))), s)


# L'ordine delle alternative è la regola: `**a *b***` chiude grassetto e corsivo
# sullo stesso asterisco, quindi la variante che finisce con `***` va provata
# PRIMA di quella che finisce con `**` — altrimenti la chiusura si mangia due
# asterischi su tre e il terzo resta stampato sulla pagina.
_ENFASI = re.compile(r"(`[^`]+`|\*\*\*.+?\*\*\*|\*\*.+?\*\*\*|\*\*.+?\*\*|\*[^*]+\*)")


def _inline(s: str) -> str:
    """Il corpo ricorsivo di `inline`: ricorsivo perché l'enfasi si annida.

    `**bacchetta di *cura ferite leggere*, 25 cariche**` è grassetto **con
    dentro** un corsivo: trattandolo a un livello solo, il corsivo interno
    faceva chiudere il grassetto nel punto sbagliato e il resto della riga —
    tutto l'equipaggiamento — usciva in corsivo con un asterisco orfano in coda.
    """
    fuori = []
    for p in _ENFASI.split(s):
        if not p:
            continue
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            fuori.append('#raw("' + p[1:-1].replace('"', '\\"') + '")')
        elif p.startswith("***") and p.endswith("***") and len(p) > 6:
            fuori.append("*_" + _inline(p[3:-3]) + "_*")
        elif p.startswith("**") and p.endswith("**") and len(p) > 4:
            fuori.append("*" + _inline(p[2:-2]) + "*")     # in Typst * = grassetto
        elif p.startswith("*") and p.endswith("*") and len(p) > 2:
            fuori.append("_" + _esc(p[1:-1]) + "_")        # in Typst _ = corsivo
        else:
            fuori.append(_esc(p))
    return "".join(fuori)


def inline(s: str) -> str:
    """Grassetto, corsivo, codice e link, nell'ordine che evita le collisioni."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)  # link → solo il testo
    return _unesc(_inline(s))


def _celle(riga: str) -> list[str]:
    return [c.strip() for c in riga.strip().strip("|").split("|")]


_BLOCCO = re.compile(r"^(#{1,4}\s|>|---+\s*$|\s*[-*]\s+|\s*\d+\.\s+|\s*\||```)")


def md_to_typ(md: str) -> str:
    righe = md.split("\n")
    out: list[str] = []
    i = 0
    while i < len(righe):
        ln = righe[i]

        if ln.startswith("```"):                       # blocco di codice
            i += 1
            blocco = []
            while i < len(righe) and not righe[i].startswith("```"):
                blocco.append(righe[i])
                i += 1
            i += 1
            testo = "\n".join(blocco).replace("`", "\u0060")
            out.append("#block(breakable: true)[#raw(\"" + testo.replace('"', '\\"').replace("\n", "\\n") + "\", block: true)]")
            continue

        if ln.strip().startswith("|") and i + 1 < len(righe) and re.match(
            r"^\s*\|[\s:|-]+\|\s*$", righe[i + 1]
        ):
            testa = _celle(ln)
            i += 2
            corpo = []
            while i < len(righe) and righe[i].strip().startswith("|"):
                corpo.append(_celle(righe[i]))
                i += 1
            n = len(testa)
            out.append(f"#tabella({n},")
            out += [f"  [*{inline(h)}*]," if h.strip() else "  []," for h in testa]
            for r in corpo:
                out += [f"  [{inline(c)}]," for c in (r + [""] * n)[:n]]
            out.append(")")
            continue

        if ln.startswith(">"):                         # read-aloud o nota di regia
            blocco, aloud = [], False
            while i < len(righe) and righe[i].startswith(">"):
                t = righe[i].lstrip(">").strip()
                if t.startswith("*") and not t.startswith("**"):
                    aloud = True
                blocco.append(t)
                i += 1
            testo = " ".join(x for x in blocco if x)
            out.append(("#leggi[" if aloud else "#nota[") + inline(testo) + "]")
            continue

        if re.match(r"^#{1,4}\s", ln):
            lvl = len(ln) - len(ln.lstrip("#"))
            out.append("=" * lvl + " " + inline(ln[lvl:].strip()))
        elif re.match(r"^---+\s*$", ln):
            out.append("#fregio()")
        elif re.match(r"^\s*[-*]\s+", ln) or re.match(r"^\s*\d+\.\s+", ln):
            # Anche la voce di elenco assorbe le righe di continuazione: nei
            # master vanno spesso a capo, e trattarle come paragrafi a sé
            # staccava la coda della frase dal suo punto elenco.
            segno = "-" if re.match(r"^\s*[-*]\s+", ln) else "+"
            voce = [re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", ln)]
            while i + 1 < len(righe) and righe[i + 1].strip() and not _BLOCCO.match(righe[i + 1]):
                i += 1
                voce.append(righe[i].strip())
            out.append(f"{segno} " + inline(" ".join(voce)))
        elif ln.strip() == "":
            out.append("")
        else:
            # Il paragrafo si accorpa PRIMA dell'inline: nei master il grassetto
            # va spesso a capo, e riga per riga risulterebbe sbilanciato — il
            # difetto si vede come `**testo**` stampato letterale.
            para = [ln]
            while i + 1 < len(righe) and righe[i + 1].strip() and not _BLOCCO.match(righe[i + 1]):
                i += 1
                para.append(righe[i])
            out.append(inline(" ".join(x.strip() for x in para)))
        i += 1
    return "\n".join(out)


# ── le schede pregenerate ────────────────────────────────────────────────────
# Qui il convertitore generico non basta. Per mettere la CA in un riquadro, i sei
# attributi in una griglia e i legami in una colonna a parte bisogna sapere
# **quale numero è quale**: lo sa `dmcore.schede`, che legge i master. Questo
# pezzo traduce il risultato in una chiamata a `#scheda()` e nient'altro — la
# forma sta tutta in `typst/scheda-pg.typ`.

def _riga(md: str) -> str:
    """Un campo di prosa (anche andato a capo nel master) → contenuto Typst."""
    return "[" + inline(" ".join(md.split())) + "]"


def _blocco(md: str) -> str:
    """Un campo con struttura (gli slot degli incantesimi) → contenuto Typst."""
    return "[" + md_to_typ(md).strip() + "]"


def _str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def _tuple_str(righe) -> str:
    """Array Typst di tuple di stringhe, con la virgola finale che serve a 1 solo elemento."""
    return "(" + "".join("(" + ", ".join(_str(x) for x in r) + "), " for r in righe) + ")"


def _tuple_corpo(righe, come=_riga) -> str:
    """Array Typst di tuple `(etichetta, contenuto)`."""
    return "(" + "".join(f"({_str(e)}, {come(c)}), " for e, c in righe) + ")"


def _scheda_typ(s: Scheda, indice: int, totale: int, piede: str) -> str:
    # L'equipaggiamento sta col background — è la roba che il personaggio ha
    # addosso, non un numero da consultare in combattimento. Tutto il resto
    # (talenti, abilità, incantesimi, capacità di classe) va nello statblocco.
    equip = s.voce("equipaggiamento")
    destra = [(v.etichetta, v.corpo) for v in s.voci if v is not equip]

    campi: list[str] = [
        f"nome: {_str(s.nome)}",
        f"ruolo: {_str(s.ruolo)}",
        f"numero: {_str(s.numero or str(indice))}",
        f"totale: {_str(str(totale))}",
        f"classe: {_str(s.classe)}",
        f"rapide: {_tuple_str(s.rapide)}",
        f"ca: {_str(s.ca)}",
        f"pf: {_str(s.pf)}",
        f"pf-dado: {_str(s.pf_dado)}",
        f"ts: {_tuple_str(s.ts)}",
        f"attributi: {_tuple_str(s.attributi)}",
        f"manovre: {_tuple_str(s.manovre)}",
        "attacchi: (" + "".join(
            f"({_riga(riga)}, {'true' if rientro else 'false'}), " for riga, rientro in s.attacchi
        ) + ")",
        f"destra: {_tuple_corpo(destra, _blocco)}",
        f"retro: {_tuple_corpo([(v.etichetta, v.corpo) for v in s.voci_retro])}",
        f"legami: {_tuple_corpo(s.legami)}",
        f"piede: {_str(piede)}",
    ]
    for chiave, valore, come in (
        ("occhiello", s.occhiello, _riga),
        ("ca-dettaglio", s.ca_dettaglio, _riga),
        ("ts-nota", s.ts_nota, _riga),
        ("ad-alta-voce", s.ad_alta_voce, _riga),
        ("equipaggiamento", equip.corpo if equip else "", _blocco),
        ("problema", s.problema, _riga),
        ("minuto", s.minuto, _riga),
    ):
        if valore.strip():
            campi.append(f"{chiave}: {come(valore)}")
    if s.ritratto is not None:
        campi.append(f"ritratto: {_str(typ_path(s.ritratto))}")

    return "#scheda(\n  " + ",\n  ".join(campi) + ",\n)"


def schede_di(cap: dict, base: Path, f: Path) -> list[tuple[str, str]]:
    """Le schede di un capitolo `"layout": "schede"`, una per elemento.

    Tenerle separate serve a `--per-scheda`: un PDF per giocatore si ottiene
    compilando **un sorgente che contiene solo quella scheda**, non ritagliando
    la pagina N dal volume. Il ritaglio per numero regge finché ogni scheda sta
    in una pagina sola — cioè finché qualcuno non allunga un equipaggiamento.
    """
    retro = cap.get("retro")
    ritratti = cap.get("ritratti") or []
    if isinstance(ritratti, str):
        ritratti = [ritratti]
    elenco = leggi_schede(
        f,
        (base / retro).resolve() if retro else None,
        [(base / d).resolve() for d in ritratti],
    )
    mancanti = [s.nome for s in elenco if s.ritratto is None]
    if mancanti:
        print(f"  ⚠ schede senza ritratto: {', '.join(mancanti)}", file=sys.stderr)
    piede = cap.get("footer", "")
    return [
        (f"{s.numero or i}-{slug(s.nome)}", _scheda_typ(s, i, len(elenco), piede))
        for i, s in enumerate(elenco, 1)
    ]


def schede(cap: dict, base: Path, f: Path) -> str:
    """Il sorgente Typst di tutte le schede del capitolo, in fila."""
    return "\n\n".join(corpo for _, corpo in schede_di(cap, base, f))


# ── assemblaggio ─────────────────────────────────────────────────────────────

def capitoli(man: dict, base: Path, tutti: bool) -> list[tuple[dict, str, Path]]:
    fuori = []
    for c in man.get("chapters", []):
        if not tutti and c.get("tag") != "player":
            continue
        f = (base / c["file"]).resolve()
        if f.exists():
            fuori.append((c, c.get("title") or f.stem, f))
        else:
            print(f"  ⚠ capitolo mancante, saltato: {c['file']}", file=sys.stderr)
    return fuori


def fregio_per(titolo: str, file: Path, base: Path) -> str | None:
    """Il fregio del capitolo, se la sua cartella ne ha uno con un nome affine."""
    for d in (base.parent / "ALLEGATI" / "tavole" / "fregi", ROOT / "docs" / "assets" / "fregi"):
        if not d.is_dir():
            continue
        chiave = slug(file.stem)
        for svg in sorted(d.glob("fregio-*.svg")):
            nome = svg.stem[len("fregio-"):]
            if nome and (nome in chiave or chiave.startswith(nome)):
                return typ_path(svg)
    return None


def intestazione(man: dict, apparato: bool | None = None) -> list[str]:
    """Import e `#show: libro.with(...)`: la testa di ogni sorgente generato."""
    if apparato is None:
        apparato = bool(man.get("front_matter", True))
    return [
        f'#import "{typ_path(TEMA)}": *',
        f'#import "{typ_path(SCHEDA_PG)}": scheda',
        "#show: libro.with(",
        f'  titolo: {json.dumps(man.get("title", ""), ensure_ascii=False)},',
        f'  sottotitolo: {json.dumps(man.get("subtitle", ""), ensure_ascii=False)},',
        f'  brand: {json.dumps(man.get("brand", ""), ensure_ascii=False)},',
        f'  meta: {json.dumps(man.get("banner", ""), ensure_ascii=False)},',
        f'  capitolo: {json.dumps(man.get("footer", ""), ensure_ascii=False)},',
        f'  apparato: {"true" if apparato else "false"},',
        ")",
        "",
    ]


def sorgente(man: dict, base: Path, tutti: bool) -> str:
    parti = intestazione(man)
    for cap, titolo, f in capitoli(man, base, tutti):
        if cap.get("layout") == "schede":
            parti.append(schede(cap, base, f))
            parti.append("")
            continue
        fr = fregio_per(titolo, f, base)
        parti.append(f"#capitolo-aperto({json.dumps(titolo, ensure_ascii=False)}, "
                     f"{'none' if not fr else json.dumps(fr, ensure_ascii=False)})")
        corpo = md_to_typ(f.read_text(encoding="utf-8"))
        corpo = re.sub(r"\A\s*=\s[^\n]*\n", "", corpo)   # il titolo lo dà il manifest
        parti.append(corpo)
        parti.append("")
    return "\n".join(parti)


def compila(binario: str, typ: Path, pdf: Path) -> tuple[subprocess.CompletedProcess, bool]:
    """Un `typst compile`, col ripiego sui tag PDF dichiarato dal chiamante.

    Typst 0.15.1 ha un bug interno nella costruzione dell'albero dei tag PDF
    («internal error: parent group») su documenti con float dentro strutture
    annidate. I tag sono accessibilità, non impaginazione: se inciampa lì si
    riprova senza — e lo si DICE, invece di consegnare un PDF diverso da quello
    che il comando promette.
    """
    cmd = [binario, "compile", "--font-path", str(FONTS), "--root", str(ROOT)]
    esito = subprocess.run(cmd + [str(typ), str(pdf)], capture_output=True, text=True)
    if esito.returncode != 0 and "internal error" in esito.stderr and "tags" in esito.stderr:
        return subprocess.run(cmd + ["--no-pdf-tags", str(typ), str(pdf)],
                              capture_output=True, text=True), True
    return esito, False


def per_scheda(man: dict, base: Path, tutti: bool, binario: str, nome: str,
               tieni_typ: bool) -> int:
    """Un PDF per scheda in `<manifest>/schede/`, da mandare a un giocatore solo.

    Non è una comodità: sulla scheda c'è «la cosa che non dici». Girare il
    volume intero nel gruppo brucia i sei segreti prima della prima serata —
    il fascicolo completo è per il DM e per la stampante, i singoli per i
    giocatori. Perciò qui l'apparato è **sempre** spento: una copertina e un
    indice su un foglio solo non hanno senso.
    """
    fuori = base / "schede"
    trovate: list[tuple[str, str]] = []
    for cap, _, f in capitoli(man, base, tutti):
        if cap.get("layout") == "schede":
            trovate += schede_di(cap, base, f)
    if not trovate:
        print("✗ --per-scheda: nessun capitolo «\"layout\": \"schede\"» nel manifest.\n"
              "  È la chiave che accende l'impaginazione a scheda — vedi "
              "docs/guides/GUIDA-BOOKLET-E-PDF.md §1.2.", file=sys.stderr)
        return 2

    fuori.mkdir(exist_ok=True)
    testa = intestazione(man, apparato=False)
    for etichetta, corpo in trovate:
        typ = fuori / f"{nome}-{etichetta}.typ"
        pdf = typ.with_suffix(".pdf")
        typ.write_text("\n".join(testa + [corpo, ""]), encoding="utf-8")
        esito, _ = compila(binario, typ, pdf)
        if not tieni_typ:
            typ.unlink(missing_ok=True)
        if esito.returncode != 0:
            print(esito.stderr.strip()[:2000], file=sys.stderr)
            print(f"✗ --per-scheda: compilazione fallita su {etichetta}", file=sys.stderr)
            return 1
    print(f"✓ --per-scheda: {len(trovate)} schede → {fuori.relative_to(ROOT)}/ "
          f"(una a testa, senza frontespizio)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("manifest", help="il manifest del booklet (lo stesso dell'HTML)")
    ap.add_argument("--all", action="store_true", help="tutti i capitoli, ⚠ DM inclusi")
    ap.add_argument("--keep-typ", action="store_true", help="conserva il sorgente .typ generato")
    ap.add_argument("--list", action="store_true", help="elenca i capitoli e esci")
    ap.add_argument("--per-scheda", action="store_true",
                    help="in più, un PDF per ogni scheda in schede/ (da mandare a un giocatore solo)")
    args = ap.parse_args()

    mp = Path(args.manifest).resolve()
    if not mp.is_file():
        print(f"✗ manifest non trovato: {mp}", file=sys.stderr)
        return 2
    man = json.loads(mp.read_text(encoding="utf-8"))
    base = mp.parent

    if args.list:
        for cap, t, f in capitoli(man, base, True):
            marchio = "  [schede]" if cap.get("layout") == "schede" else ""
            print(f"  {t}{marchio}  ←  {f.relative_to(ROOT) if ROOT in f.parents else f}")
        return 0

    binario = shutil.which("typst")
    if not binario:
        print(INSTALLA, file=sys.stderr)
        return 1

    typ = base / f"{mp.stem.replace('.manifest', '')}.typ"
    pdf = base / f"{mp.stem.replace('.manifest', '')}-STAMPA.pdf"
    try:
        src = sorgente(man, base, args.all)
    except SchedaError as e:
        print(f"✗ export_booklet_typst: {e}", file=sys.stderr)
        return 1
    typ.write_text(src, encoding="utf-8")

    esito, degradato = compila(binario, typ, pdf)

    if not args.keep_typ:
        typ.unlink(missing_ok=True)
    if esito.returncode != 0:
        print(esito.stderr.strip()[:4000], file=sys.stderr)
        print("✗ export_booklet_typst: compilazione fallita", file=sys.stderr)
        return 1
    if degradato:
        print("  ⚠ tag PDF disattivati: bug interno di typst sull'albero dei tag.\n"
              "    Il volume è completo e i segnalibri ci sono; manca il livello di\n"
              "    accessibilità per i lettori di schermo. Riprovare a ogni aggiornamento\n"
              "    di typst — la riga di fallback si toglie il giorno che compila.",
              file=sys.stderr)

    n = len(capitoli(man, base, args.all))
    print(f"✓ export_booklet_typst: {n} capitoli → {pdf.relative_to(ROOT)} "
          f"({pdf.stat().st_size // 1024} KB, un volume con segnalibri)")

    if args.per_scheda:
        return per_scheda(man, base, args.all, binario,
                          mp.stem.replace(".manifest", ""), args.keep_typ)
    return 0


if __name__ == "__main__":
    sys.exit(main())
