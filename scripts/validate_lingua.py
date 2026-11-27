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

Cosa salta: blocchi di codice (``` e rientrati, come li legge CommonMark),
`codice inline`, URL, percorsi, front-matter YAML. Lì le virgolette dritte e i
doppi spazi sono corretti. Una riga rientrata che è il seguito di un elenco o di
un paragrafo è prosa, e si legge.

Una citazione alla lettera si marca sulla sua riga con `<!-- sic -->`: la *d*
eufonica lì non si segnala, e il conto delle righe marcate si stampa.

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

try:                                   # opzionale, con degradazione dichiarata
    from markdown_it import MarkdownIt
    _MD = MarkdownIt("commonmark").enable("table")
except ImportError:                    # pragma: no cover - dipende dall'ambiente
    _MD = None

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
    # Il segno che occupa da solo una cella di tabella («| ? |») e il rapporto
    # fra due numeri («5.8 : 1») hanno lo spazio davanti di diritto: la corsa di
    # spazi deve partire da una parola, e i due punti fra cifre non contano.
    (r"(?<![|\s])(?:(?<=\d)(?!\s+:\s*\d)|(?<!\d))\s+[,;:!?](?:\s|$)",
     "spazio prima della punteggiatura"),
    (r"[a-zàèéìòù]{2}  +[a-zàèéìòù]", "doppio spazio fra parole"),
]

# Segnalati ma non bloccanti: veri, ma con casi legittimi di confine.
AVVISI: list[tuple[str, str]] = [
    (r'(?<![=(])"[A-Za-zÀ-ù]', 'virgolette dritte → «» (o " " tipografiche)'),
    (r"(?<![A-Za-z])E'\s", "«E'» → È (maiuscola accentata)"),
    # L'apostrofo non sostituisce l'accento («e'», «gia'», «perche'»). Solo le
    # parole che un apostrofo finale non può che storpiare: *po'* e *da'* sono
    # corretti e non stanno in lista. Una regex sola trova le stesse righe di
    # LanguageTool (GR_04_002) e altre 58, senza i falsi *Da'* (ADR-0079).
    (r"(?<![\w'’])(?:e|(?i:gia|piu|puo|cosi|perche|pero|citta|poiche|cioe|"
     r"verra|andra|potra|fara|dira|dara|stara|virtu|liberta|qualita|facolta|"
     r"universita|eta|novita|difficolta|possibilita|realta|identita|"
     r"finche|benche|anziche|affinche|giacche|dopodiche|"
     r"caffe|te|ahime|lunedi|martedi|mercoledi|giovedi|venerdi))'(?![\w'’])",
     "apostrofo al posto dell'accento («e'» → è, «gia'» → già, «perche'» → perché)"),
]

# La *d* eufonica (CODA D3, 2026-11-08; editorial-standards.md): *ad* ed *ed*
# solo davanti alla stessa vocale. Manca in «a area», «e Elementali»; avanza in
# «ad ogni», «ed infine», «fino ad ora». Resta solo *ad esempio* (e *ad es.*),
# come in LanguageTool, che boccia anche *ad eccezione* e *ad oggi*. È la sua
# regola ST_03_001, misurata
# contro questa regex in plans/esperimenti/d-eufonica-2026-11-09/.
# Maiuscole: «A» solo a inizio di frase (non la lettera di «Unità A attacca»),
# «E» solo fra parole tutte maiuscole («CAOS E EROISMO»), non le lettere
# («§7.E Echo», «N, E e O»). *O o…* resta fuori: *od* è arcaico e la norma non
# lo chiede.
_V_A, _V_E = "aàáAÀÁ", "eèéEÈÉ"
_V_NON_A, _V_NON_E = "eèéiìíoòóuùúEÈÉIÌÍOÒÓUÙÚ", "aàáiìíoòóuùúAÀÁIÌÍOÒÓUÙÚ"
_ENF = r"[*_]{0,3}"                 # «e *esplosione*»: il corsivo non conta
_D_MANCA = re.compile(rf"(?<![\w'’])(?:a (?={_ENF}[{_V_A}])|e (?={_ENF}[{_V_E}])"
                      r"|(?:(?<=^)|(?<=[.!?:»\"*>-]\s))A (?=[AÀÁ](?:[a-zà-ù]|[A-Z]{2}))"
                      r"|(?<=[A-ZÀ-Ù]{2}\s)E (?=[EÈÉ][A-ZÀ-Ù]))")
_D_AVANZA = re.compile(rf"(?<![\w'’])(?:[Aa]d (?={_ENF}[{_V_NON_A}])|[Ee]d (?={_ENF}[{_V_NON_E}]))")
_D_LOCUZIONI = re.compile(r"[Aa]d (?:esempio|es\.)")
_D_CODA = re.compile(r"(?<![\w'’])([AaEe]d?)[*_]{0,3}\s*$")     # «…e» a fine riga
_D_TESTA = re.compile(r"^[\s>*_-]*")


def d_eufonica(riga: str) -> list[str]:
    """Le forme della *d* eufonica fuori norma in una riga, come «a area → ad»."""
    out = [f"«{m.group(0)}…» → {m.group(0).strip()}{'D' if riga[m.end():m.end() + 2].isupper() else 'd'}"
           for m in _D_MANCA.finditer(riga)]
    out += [f"«{m.group(0)}…» → {m.group(0)[0]}" for m in _D_AVANZA.finditer(riga)
            if not _D_LOCUZIONI.match(riga, m.start())]
    return out


def d_eufonica_righe(righe) -> list[tuple[int, str]]:
    """(numero, forma) su tutte le righe, anche quando la congiunzione chiude una
    riga e la parola dopo apre la seguente («Pietra e / evocato»)."""
    out: list[tuple[int, str]] = []
    prima: tuple[int, str] | None = None
    for n, riga in righe:
        out += [(n, f) for f in d_eufonica(riga)]
        if prima and riga.strip():
            unite = prima[1] + " " + riga[_D_TESTA.match(riga).end():]
            out += [(prima[0], f + " (a capo)") for f in d_eufonica(unite)]
        m = _D_CODA.search(riga)
        prima = (n, m.group(1)) if m and riga.strip() else None
    return out


# Né spazio, né lettera, né punteggiatura: il codice mascherato non deve
# somigliare a niente che le regole qui sopra cerchino.
MASCHERA = "¤"

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


_ELENCO = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")


def _codice_senza_parser(righe: list[str]) -> set[int]:
    """La regola di ripiego, solo stdlib: i recinti, e le righe rientrate di
    quattro spazi che aprono dopo una riga vuota fuori da una voce d'elenco."""
    codice: set[int] = set()
    recinto = in_elenco = in_blocco = False
    vuota_prima = True
    for n, riga in enumerate(righe, 1):
        if CODE_FENCE.match(riga):
            recinto = not recinto
            in_blocco = vuota_prima = False
            codice.add(n)
            continue
        if recinto:
            codice.add(n)
            continue
        if not riga.strip():
            vuota_prima = True
            continue
        if riga.startswith("    ") or riga.startswith("\t"):
            if in_blocco or (vuota_prima and not in_elenco):
                in_blocco = True
                codice.add(n)
        else:
            in_elenco = bool(_ELENCO.match(riga))
            in_blocco = False
        vuota_prima = False
    return codice


def righe_di_codice(righe: list[str]) -> set[int]:
    """I numeri (da 1) delle righe che sono codice: recinti e blocchi rientrati.

    Lo dice il parser CommonMark di riferimento, markdown-it-py (ADR-0120,
    emendamento 2026-11-11). Una riga rientrata di quattro spazi è codice solo
    se CommonMark la legge così: il seguito di una voce d'elenco o di un
    paragrafo è prosa. Fino al 2026-11-11 si saltava ogni riga rientrata, e
    1.309 righe di prosa su 1.484 non le leggeva nessun controllo.

    Senza markdown-it-py si ripiega su `_codice_senza_parser` (degradazione
    dichiarata di ADR-0037): stesso richiamo sul banco di semina, 184 righe
    classificate in altro modo, quasi tutte in un file d'archivio coi recinti
    rotti."""
    if _MD is None:
        return _codice_senza_parser(righe)
    codice: set[int] = set()
    for tok in _MD.parse("\n".join(righe)):
        if tok.map and tok.type in ("fence", "code_block"):
            codice.update(range(tok.map[0] + 1, tok.map[1] + 1))
    return codice


def righe_da_controllare(testo: str):
    """(numero, riga ripulita). Salta i blocchi di codice e il front-matter."""
    righe = testo.splitlines()
    inizio = 0
    if righe and righe[0].strip() == "---":              # front-matter YAML
        for i, r in enumerate(righe[1:], 2):
            if r.strip() == "---":
                inizio = i
                break
    codice = righe_di_codice([""] * inizio + righe[inizio:])
    for n, riga in enumerate(righe[inizio:], inizio + 1):
        if n in codice:
            continue
        # Il mascheramento conserva la LUNGHEZZA: sostituire con uno spazio
        # creerebbe i doppi spazi che poi segnaleremmo come refuso — ed è
        # successo alla prima passata, su 423 falsi positivi. E non usa una
        # lettera: con la «x» il codice diventava una parola, e i due spazi
        # prima di un'ancora `[…]` in un titolo sembravano un refuso (7 casi).
        yield n, INLINE.sub(lambda m: MASCHERA * len(m.group(0)), riga)


SIC = re.compile(r"<!--\s*sic\s*-->")


def righe_sic(testo: str) -> set[int]:
    """Le righe marcate `<!-- sic -->`: citazioni alla lettera, dove la forma
    della fonte resta com'è."""
    return {n for n, r in enumerate(testo.splitlines(), 1) if SIC.search(r)}


def controlla(f: Path) -> tuple[list[str], list[str]]:
    """(errori, avvisi) di un file. La *d* eufonica fuori norma è un errore:
    ADR-0120, stable dal 2026-11-25 dopo il canale testing di ADR-0099."""
    errori: list[str] = []
    avvisi: list[str] = []
    testo = f.read_text(encoding="utf-8", errors="ignore")
    rel = f.relative_to(ROOT) if ROOT in f.parents else f
    righe = list(righe_da_controllare(testo))
    sic = righe_sic(testo)
    for n, forma in d_eufonica_righe(righe):
        if n in sic:
            continue
        errori.append(
            f"{rel}:{n}: d eufonica fuori norma (ad/ed solo davanti alla stessa vocale) — {forma}")
    for n, riga in righe:
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
        # `_testi-altrui/`: conversioni di manuali e siti altrui (RICERCA-ARCHI-SENZA-TESTO
        # D12), tenute come sono; i loro refusi sono della fonte e non si correggono.
        out.extend(p for p in d.rglob("*.md")
                   if not p.name.endswith(".hb.md") and "_testi-altrui" not in p.parts)
    return sorted(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*", help="file da controllare (default: tutto il contenuto)")
    ap.add_argument("--strict", action="store_true", help="gli avvisi diventano errori")
    ap.add_argument("--avvisi", action="store_true",
                    help="elenca gli avvisi; senza, se ne stampa solo il conto per tipo")
    args = ap.parse_args(argv)

    bersagli = [Path(f).resolve() for f in args.files] if args.files else file_di_contenuto()
    errori: list[str] = []
    avvisi: list[str] = []
    marcate = 0
    for f in bersagli:
        if not f.is_file():
            continue
        marcate += len(righe_sic(f.read_text(encoding="utf-8", errors="ignore")))
        e, a = controlla(f)
        errori += e
        avvisi += a

    if args.strict:
        errori += avvisi
        avvisi = []
    # Gli avvisi sono fermi da un mese (2.450 il 2026-09-24, 2.442 il
    # 2026-10-22) e i primi venti stampati in CI non li legge nessuno. Dal
    # 2026-10-22 (lotto 7e di AVVENTURE-COMMUNITY) se ne stampa il conto per
    # tipo; l'elenco con --avvisi.
    if args.avvisi:
        for a in avvisi:
            print(f"  ⚠ {a}")
    elif avvisi:
        per_tipo: dict[str, int] = {}
        for a in avvisi:
            tipo = re.sub(r"^.*?:\d+: ", "", a)   # «file:riga: perché»
            tipo = tipo.split(" — «")[0]           # senza la forma trovata
            per_tipo[tipo] = per_tipo.get(tipo, 0) + 1
        print("  ⚠ avvisi (--avvisi per l'elenco): " + " · ".join(
            f"{n} {tipo}" for tipo, n in sorted(per_tipo.items(), key=lambda kv: -kv[1])))
    if marcate:
        print(f"  ℹ {marcate} righe marcate <!-- sic -->: lì la d eufonica non si segnala")
    if _MD is None:
        print("  ℹ markdown-it-py non installato: il codice rientrato si riconosce con la regola di ripiego")
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
