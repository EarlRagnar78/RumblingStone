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

ROOT = Path(__file__).resolve().parent.parent
TEMA = ROOT / "scripts" / "typst" / "tema-rumblingstone.typ"
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

_SPECIALI = ("\\", "#", "$", "@", "<", ">", "*", "_", "`")


def _esc(s: str) -> str:
    for ch in _SPECIALI:
        s = s.replace(ch, f"\x00{ord(ch)}\x00")
    return s


def _unesc(s: str) -> str:
    return re.sub(r"\x00(\d+)\x00", lambda m: "\\" + chr(int(m.group(1))), s)


def inline(s: str) -> str:
    """Grassetto, corsivo, codice e link, nell'ordine che evita le collisioni."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)  # link → solo il testo
    out = []
    for p in re.split(r"(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)", s):
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append('#raw("' + p[1:-1].replace('"', '\\"') + '")')
        elif p.startswith("**") and p.endswith("**"):
            out.append("*" + _esc(p[2:-2]) + "*")     # in Typst * = grassetto
        elif p.startswith("*") and p.endswith("*") and len(p) > 2:
            out.append("_" + _esc(p[1:-1]) + "_")     # in Typst _ = corsivo
        else:
            out.append(_esc(p))
    return _unesc("".join(out))


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


# ── assemblaggio ─────────────────────────────────────────────────────────────

def capitoli(man: dict, base: Path, tutti: bool) -> list[tuple[str, Path]]:
    fuori = []
    for c in man.get("chapters", []):
        if not tutti and c.get("tag") != "player":
            continue
        f = (base / c["file"]).resolve()
        if f.exists():
            fuori.append((c.get("title") or f.stem, f))
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


def sorgente(man: dict, base: Path, tutti: bool) -> str:
    parti = [
        f'#import "{typ_path(TEMA)}": *',
        "#show: libro.with(",
        f'  titolo: {json.dumps(man.get("title", ""), ensure_ascii=False)},',
        f'  sottotitolo: {json.dumps(man.get("subtitle", ""), ensure_ascii=False)},',
        f'  brand: {json.dumps(man.get("brand", ""), ensure_ascii=False)},',
        f'  meta: {json.dumps(man.get("banner", ""), ensure_ascii=False)},',
        f'  capitolo: {json.dumps(man.get("footer", ""), ensure_ascii=False)},',
        ")",
        "",
    ]
    for titolo, f in capitoli(man, base, tutti):
        fr = fregio_per(titolo, f, base)
        parti.append(f"#capitolo-aperto({json.dumps(titolo, ensure_ascii=False)}, "
                     f"{'none' if not fr else json.dumps(fr, ensure_ascii=False)})")
        corpo = md_to_typ(f.read_text(encoding="utf-8"))
        corpo = re.sub(r"\A\s*=\s[^\n]*\n", "", corpo)   # il titolo lo dà il manifest
        parti.append(corpo)
        parti.append("")
    return "\n".join(parti)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("manifest", help="il manifest del booklet (lo stesso dell'HTML)")
    ap.add_argument("--all", action="store_true", help="tutti i capitoli, ⚠ DM inclusi")
    ap.add_argument("--keep-typ", action="store_true", help="conserva il sorgente .typ generato")
    ap.add_argument("--list", action="store_true", help="elenca i capitoli e esci")
    args = ap.parse_args()

    mp = Path(args.manifest).resolve()
    if not mp.is_file():
        print(f"✗ manifest non trovato: {mp}", file=sys.stderr)
        return 2
    man = json.loads(mp.read_text(encoding="utf-8"))
    base = mp.parent

    if args.list:
        for t, f in capitoli(man, base, True):
            print(f"  {t}  ←  {f.relative_to(ROOT) if ROOT in f.parents else f}")
        return 0

    binario = shutil.which("typst")
    if not binario:
        print(INSTALLA, file=sys.stderr)
        return 1

    typ = base / f"{mp.stem.replace('.manifest', '')}.typ"
    pdf = base / f"{mp.stem.replace('.manifest', '')}-STAMPA.pdf"
    typ.write_text(sorgente(man, base, args.all), encoding="utf-8")

    base_cmd = [binario, "compile", "--font-path", str(FONTS), "--root", str(ROOT)]
    esito = subprocess.run(base_cmd + [str(typ), str(pdf)], capture_output=True, text=True)

    # Typst 0.15.1 ha un bug interno nella costruzione dell'albero dei tag PDF
    # («internal error: parent group») su documenti con float dentro strutture
    # annidate. I tag sono accessibilità, non impaginazione: se inciampa lì,
    # si riprova senza — e lo si DICE, invece di consegnare un PDF diverso da
    # quello che il comando promette.
    degradato = False
    if esito.returncode != 0 and "internal error" in esito.stderr and "tags" in esito.stderr:
        degradato = True
        esito = subprocess.run(base_cmd + ["--no-pdf-tags", str(typ), str(pdf)],
                               capture_output=True, text=True)

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
