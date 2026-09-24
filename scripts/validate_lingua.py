#!/usr/bin/env python3
"""validate_lingua.py — i refusi che una macchina trova meglio di un revisore.

Perché esiste. Il repo ha la **norma** redazionale (`editorial-standards.md` nella
skill di stile) e non aveva nessun controllo che la applicasse alla lingua. Un
`perchè` con l'accento sbagliato non rompe niente, non fa fallire nessun test, e
arriva stampato sul tavolo — dove lo vedono quattro persone.

Cosa NON fa, di proposito: non giudica lo stile, non conta le ripetizioni, non
propone sinonimi. Le regole qui dentro hanno una sola proprietà: **o sono errori
o non sono niente**. Un validatore di lingua che discute viene disattivato entro
una settimana, e allora non trova più nemmeno i refusi veri.

Cosa salta: blocchi di codice (``` e indentati), `codice inline`, URL, percorsi,
front-matter YAML. Lì le virgolette dritte e i doppi spazi sono corretti.

Uso:
    python3 scripts/validate_lingua.py                 # tutto il contenuto
    python3 scripts/validate_lingua.py FILE…           # solo questi
    python3 scripts/validate_lingua.py --strict        # i warning diventano errori
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Cartelle di contenuto: gli archi, la campagna, i moduli, il bestiario, i PG.
CONTENUTO = ("00_", "01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_",
             "10-stand-alone", "STANDALONE-", "campaign", "Bestiario", "PG")

# Errori veri: nessuno di questi è una scelta di stile.
ERRORI: list[tuple[str, str]] = [
    (r"\bperch[èé]?\b(?<=perchè)", "«perchè» → perché (accento acuto)"),
    (r"\b(?:poi|ben|fin|affin|cosic|seb ben)?ch[è]\b", "«…chè» → …ché (accento acuto)"),
    (r"\bn[è]\b", "«nè» → né (accento acuto)"),
    (r"\bs[è]\s+stess", "«sè stesso» → sé stesso (accento acuto)"),
    (r"\bp[òo]'?\b(?<=pò)", "«pò» → po' (apostrofo, non accento)"),
    (r"\bqual'è\b", "«qual'è» → qual è (nessun apostrofo)"),
    (r"\bun'(?=[aeiou]?\s*(?:uomo|altro|anno|attimo|amico|errore|istante))"
     r"(?:uomo|altro|anno|attimo|amico|errore|istante)",
     "«un'» davanti a nome maschile → un (senza apostrofo)"),
    (r"\bdaccordo\b", "«daccordo» → d'accordo"),
    (r"\bad\s+(?=[bcdfglmnpqrstvz])", "«ad» davanti a consonante → a"),
    (r"\bed\s+(?=[bcdfglmnpqrstvz])", "«ed» davanti a consonante → e"),
    (r"\s+[,;:!?](?:\s|$)", "spazio prima della punteggiatura"),
    (r"[a-zàèéìòù]{2}  +[a-zàèéìòù]", "doppio spazio fra parole"),
]

# Segnalati ma non bloccanti: veri, ma con casi legittimi di confine.
AVVISI: list[tuple[str, str]] = [
    (r'(?<![=(])"[A-Za-zÀ-ù]', 'virgolette dritte → «» (o " " tipografiche)'),
    (r"(?<![A-Za-z])E'\s", "«E'» → È (maiuscola accentata)"),
]

CODE_FENCE = re.compile(r"^\s*```")
# Da mascherare: codice inline, tag, URL, link, nomi di file — e le **guide
# alla pronuncia** (`*nè-this*`), dove l'accento grave è messo apposta per dire
# il suono. Segnalarle sarebbe corretto in teoria e sbagliato in pratica: è la
# riga che la `module-standard` §15 chiede di scrivere.
INLINE = re.compile(
    r"`[^`]*`|<[^>]+>|https?://\S+|\[[^\]]*\]\([^)]*\)"
    r"|[\w./-]+\.(?:md|py|json|svg|html|typ)"
    r"|\*[A-Za-zÀ-ù]+(?:-[A-Za-zÀ-ù]+)+\*"
)


def righe_da_controllare(testo: str):
    """(numero, riga ripulita). Salta i blocchi di codice e il front-matter."""
    dentro_fence = False
    righe = testo.splitlines()
    inizio = 0
    if righe and righe[0].strip() == "---":              # front-matter YAML
        for i, r in enumerate(righe[1:], 2):
            if r.strip() == "---":
                inizio = i
                break
    for n, riga in enumerate(righe[inizio:], inizio + 1):
        if CODE_FENCE.match(riga):
            dentro_fence = not dentro_fence
            continue
        if dentro_fence or riga.startswith("    ") or riga.startswith("\t"):
            continue
        # Il mascheramento conserva la LUNGHEZZA: sostituire con uno spazio
        # creerebbe i doppi spazi che poi segnaleremmo come refuso — ed è
        # successo alla prima passata, su 423 falsi positivi.
        yield n, INLINE.sub(lambda m: "x" * len(m.group(0)), riga)


def controlla(f: Path) -> tuple[list[str], list[str]]:
    errori: list[str] = []
    avvisi: list[str] = []
    testo = f.read_text(encoding="utf-8", errors="ignore")
    rel = f.relative_to(ROOT) if ROOT in f.parents else f
    for n, riga in righe_da_controllare(testo):
        for pattern, perche in ERRORI:
            if re.search(pattern, riga, re.I):
                errori.append(f"{rel}:{n}: {perche} — «{riga.strip()[:70]}»")
        for pattern, perche in AVVISI:
            if re.search(pattern, riga):
                avvisi.append(f"{rel}:{n}: {perche}")
    return errori, avvisi


def file_di_contenuto() -> list[Path]:
    out: list[Path] = []
    for d in ROOT.iterdir():
        if not d.is_dir() or not d.name.startswith(CONTENUTO):
            continue
        out.extend(p for p in d.rglob("*.md") if not p.name.endswith(".hb.md"))
    return sorted(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*", help="file da controllare (default: tutto il contenuto)")
    ap.add_argument("--strict", action="store_true", help="gli avvisi diventano errori")
    args = ap.parse_args(argv)

    bersagli = [Path(f).resolve() for f in args.files] if args.files else file_di_contenuto()
    errori: list[str] = []
    avvisi: list[str] = []
    for f in bersagli:
        if not f.is_file():
            continue
        e, a = controlla(f)
        errori += e
        avvisi += a

    if args.strict:
        errori += avvisi
        avvisi = []
    for a in avvisi[:20]:
        print(f"  ⚠ {a}")
    if len(avvisi) > 20:
        print(f"  ⚠ … e altri {len(avvisi) - 20} avvisi")
    if errori:
        print(f"✗ validate_lingua: {len(errori)} refusi in {len(bersagli)} file")
        for e in errori[:60]:
            print(f"  - {e}")
        if len(errori) > 60:
            print(f"  … e altri {len(errori) - 60}")
        return 1
    print(f"✓ validate_lingua: {len(bersagli)} file — nessun refuso"
          + (f" ({len(avvisi)} avvisi)" if avvisi else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
