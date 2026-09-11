#!/usr/bin/env python3
"""validate_docs.py — gate anti-deriva fra la documentazione e il filesystem.

Scopo
  Verifica che ogni percorso del repo **citato** nei documenti d'ingresso
  (`AGENTS.md`, `README.md`, `docs/INDEX.md`) esista davvero. Nasce dal finding
  T4 dell'audit 2026-08-05: `AGENTS.md` documentava `campaign/npcs/`,
  `campaign/locations/` e `campaign/encounters/` — nessuna delle tre esiste, i
  PNG vivono in `Bestiario/png/` — e istruiva gli agenti a cercarle.

  È la stessa cura che l'audit di luglio (F4) ha applicato alla tool map:
  la prosa scritta a mano **deriva** dal codice, quindi va verificata da un gate.

Cosa controlla
  1. **Blocchi-albero** nei fence markdown (righe con `├──`/`└──`): ricostruisce
     il percorso completo da indentazione + connettore e ne verifica l'esistenza.
  2. **Link markdown relativi** nei documenti in elenco.
  3. **Path inline** in backtick, solo quando sono inequivocabili: il primo
     segmento deve essere una directory top-level esistente del repo.
  4. **Percorsi assoluti alla macchina di chi scrive** (`/home/<utente>/…`), che
     rendono un documento vero solo su un computer — solo con `--sorgenti`.

  Fuori scope per costruzione (niente falsi positivi): URL, ancore, glob
  (`*`, `?`), segnaposto (`<...>`, `[...]`, `percorso/relativo/...`), i path
  che il documento marca esplicitamente come esempio, e — dal lotto 4b — i link
  citati **dentro i backtick**: `` `![alt](path)` `` è un esempio di sintassi,
  non un'asserzione che `path` esista.

Uso
  python3 scripts/validate_docs.py [--verbose] [--json] [--doc FILE ...]
  python3 scripts/validate_docs.py --sorgenti

Input   AGENTS.md, README.md, docs/INDEX.md (override con --doc); con
        `--sorgenti`, tutti i markdown scritti a mano del repo (§SORGENTI)
Output  stdout testuale, oppure JSON con --json
Exit    0 = tutti i percorsi esistono · 1 = percorsi inesistenti · 2 = errore d'uso
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_DOCS = ["AGENTS.md", "README.md", "docs/INDEX.md"]

# Righe di un albero: "├── nome/", "└── nome.md", con indentazione "│   " o "    ".
TREE_LINE = re.compile(r"^(?P<indent>(?:[│|]\s{3}|\s{4})*)(?P<conn>[├└][─-]{2}\s+)?(?P<name>[^\s#`]+)")
LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
INLINE = re.compile(r"`([^`\n]+)`")

# Un path inline è considerato tale solo se assomiglia a un percorso e non a prosa.
PLACEHOLDER = re.compile(r"[<>\[\]{}*?]|^\.{1,2}$|^percorso/|^path/|^nome-|^\[")

# Modelli di nome, non percorsi reali: `campaign/sessions/YYYY-MM-DD_session-N.md`,
# `campaign/npcs/[name-kebab-case].md`. Sono convenzioni di naming, non asserzioni
# sull'esistenza di un file.
NAME_TEMPLATE = re.compile(r"YYYY|MM-DD|_session-N|-N\.|\bN\.md$|kebab-case")

# Direttive di esclusione. Servono ai passaggi in cui un documento **cita un
# percorso per dire che non esiste** (le note storiche del lotto G2): senza una
# via d'uscita esplicita, il gate impedirebbe di documentare i propri errori.
#   <!-- validate-docs: ignore -->              → salta la riga su cui compare
#   <!-- validate-docs: ignore-begin --> … end  → salta l'intervallo
IGNORE_LINE = "<!-- validate-docs: ignore -->"
IGNORE_BEGIN = "<!-- validate-docs: ignore-begin -->"
IGNORE_END = "<!-- validate-docs: ignore-end -->"

# Nei file non-markdown la direttiva vive in un commento della lingua ospite.
IGNORE_LINE_ALT = "validate-docs: ignore"

# Un percorso dentro il checkout personale di qualcuno: il documento e' vero su
# un solo computer. Non e' un percorso inesistente — e' un percorso che non puo'
# esistere altrove — quindi ha una diagnosi sua.
#
# ⚠️ Il controllo NON e' «qualsiasi /home/»: al primo giro ha segnalato undici
# righe di `converters/*/DEPLOYMENT.md` — `User=htmlconverter` in una unit
# systemd, `ENV PATH=/home/converter/...` in un Dockerfile, il path standard di
# Homebrew su Linux. Quelle sono destinazioni di deploy su un server, non la
# scrivania di chi scrive, e sono corrette. Il segno che distingue le due cose
# e' il **nome del repo dentro il percorso**.
NOME_REPO = "RumblingStone"

# L'indice degli ADR: un elenco a mano accanto a una cartella. Al lotto 4b si era
# fermato ad ADR-0020 mentre la cartella era a 0048 — **ventotto assenze**, che il
# controllo sui percorsi non vede perche' i percorsi citati esistono tutti. E' la
# forma esatta di ADR-0041 (13 skill elencate su 18 esistenti).
INDICE_ADR = "docs/INDEX.md"
CARTELLA_ADR = "plans/adr"
LINK_ADR = re.compile(r"\(\.\./plans/adr/(ADR-\d{4}[^)]*\.md)\)")
TOKEN_HOME = re.compile(r"/home/[A-Za-z0-9._][A-Za-z0-9._-]*/[^\s`'\"()\[\]<>]*")

# --- SORGENTI ---------------------------------------------------------------
# Scritto a mano = tutto tranne cio' che una macchina rigenera o che arriva da
# terzi. I mirror per-agente li riconosce gia' `_is_generated_mirror`.
ESCLUSI_PREFISSO = (
    "build/",
    "homebrew/",
    "scripts/typst/packages/",   # pacchetti vendored, ADR-0026: non sono nostri
)
ESCLUSI_FRAMMENTO = ("/homebrew/",)
ESCLUSI_SUFFISSO = (".hb.md",)


def _e_generato(rel: str) -> bool:
    """Vero se il file e' un artefatto rigenerabile o vendored, non un sorgente."""
    return (
        _is_generated_mirror(rel)
        or rel.startswith(ESCLUSI_PREFISSO)
        or rel.endswith(ESCLUSI_SUFFISSO)
        or any(f in rel for f in ESCLUSI_FRAMMENTO)
    )


def sorgenti(*estensioni: str) -> list[str]:
    """I file tracciati con quelle estensioni, meno i generati e i vendored.

    Enumera da `git ls-files`, non da un elenco scritto a mano: e' la quarta
    regola di ADR-0045 — un lotto che lavora su un insieme dichiara da dove lo
    conta. `-z` perche' nel repo ci sono nomi con spazi (gli archi 00-09).
    """
    modelli = [f"*{e}" for e in (estensioni or (".md",))]
    out = subprocess.run(["git", "ls-files", "-z", *modelli],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return sorted(f for f in out.split("\0") if f and not _e_generato(f))


def ignored_lines(text: str) -> set[int]:
    """Numeri di riga (1-based) esclusi dai controlli via direttiva."""
    out: set[int] = set()
    in_block = False
    for lineno, raw in enumerate(text.splitlines(), start=1):
        if IGNORE_BEGIN in raw:
            in_block = True
            out.add(lineno)
            continue
        if IGNORE_END in raw:
            in_block = False
            out.add(lineno)
            continue
        if in_block or IGNORE_LINE in raw or IGNORE_LINE_ALT in raw:
            out.add(lineno)
    return out


def percorsi_assoluti(rel: str) -> list[dict]:
    """Le righe che cablano il checkout personale di qualcuno.

    Chi *descrive* il difetto invece di commetterlo esce con la direttiva:
    `<!-- validate-docs: ignore -->` nei markdown, lo stesso testo dentro un
    commento nelle altre lingue. Senza una via d'uscita esplicita il gate
    impedirebbe di documentare i propri errori — e' la stessa scelta gia' fatta
    per i percorsi inesistenti.

    ⚠️ **Limite dichiarato**: un percorso personale che non nomina il repo
    (`/home/tizio/appunti.md`) non viene visto. E' il prezzo di non avere undici
    falsi positivi sui deploy dei convertitori, e vale lo stesso limite di
    ADR-0043: il gate copre il caso che si e' presentato davvero.
    """
    testo = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
    salta = ignored_lines(testo)
    fuori: list[dict] = []
    for lineno, riga in enumerate(testo.splitlines(), start=1):
        if lineno in salta:
            continue
        for token in TOKEN_HOME.findall(riga):
            if NOME_REPO not in token:
                continue
            fuori.append({"doc": rel, "line": lineno, "path": token,
                          "source": "assoluto",
                          "reason": "percorso dentro un checkout personale"})
            break
    return fuori


def _toplevel_dirs() -> set[str]:
    return {p.name for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")}


def _exists(rel: str) -> bool:
    """Un percorso esiste se il file/dir c'è.

    Accetta anche la **citazione abbreviata** in uso nel repo per gli ADR e simili:
    `plans/adr/ADR-0003` designa senza ambiguità `ADR-0003-markdown-master-...md`.
    Vale solo se il prefisso identifica **un solo** file nella cartella: due match
    sono un'ambiguità, e un'ambiguità va segnalata come errore.
    """
    p = ROOT / rel
    if p.exists():
        return True
    parent, stem = p.parent, p.name
    if "." in stem or not parent.is_dir():
        return False
    matches = [c for c in parent.iterdir() if c.name.startswith(stem)]
    return len(matches) == 1


def _is_generated_mirror(rel: str) -> bool:
    """I mirror per-agente sono artefatti gitignored: citarli è corretto anche se assenti."""
    first = rel.split("/", 1)[0]
    return first.startswith(".") and first not in {".github", ".gitignore"}


def paths_from_tree_blocks(text: str) -> list[tuple[int, str]]:
    """Percorsi ricostruiti dai blocchi-albero. Ritorna [(riga, percorso)]."""
    out: list[tuple[int, str]] = []
    in_fence = False
    stack: list[str] = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            stack = []
            continue
        if not in_fence:
            continue
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        m = TREE_LINE.match(line)
        if not m:
            continue
        name = m.group("name")
        if PLACEHOLDER.search(name) or NAME_TEMPLATE.search(name) or name in {"...", "…"}:
            continue
        depth = (len(m.group("indent")) // 4 + 1) if m.group("conn") else 0
        stack = stack[:depth]
        clean = name.rstrip("/")
        stack.append(clean)
        # Solo le foglie e i rami citati esplicitamente contano come asserzioni.
        out.append((lineno, "/".join(stack)))
    return out


def senza_code_span(riga: str) -> str:
    """La riga con i tratti fra backtick svuotati, lunghezza conservata.

    Un link dentro i backtick e' un **esempio di sintassi**, non un rimando:
    `![alt](path)` non asserisce che `path` esista. Prima del lotto 4b il gate
    non lo sapeva e produceva nove hit su ventisei — fra cui, per intero, la
    riga di `plans/CHANGELOG.md` che descriveva proprio questo difetto nel
    convertitore Typst. Si svuota invece di togliere per non spostare le colonne.
    """
    fuori, dentro = [], False
    for pezzo in re.split(r"(`+)", riga):
        if pezzo.startswith("`"):
            fuori.append(pezzo)
            dentro = not dentro
        else:
            fuori.append(" " * len(pezzo) if dentro else pezzo)
    return "".join(fuori)


def paths_from_links(text: str, doc: Path) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for lineno, riga in enumerate(text.splitlines(), start=1):
        raw = senza_code_span(riga)
        for _, tgt in LINK.findall(raw):
            if tgt.startswith(("http://", "https://", "#", "mailto:")):
                continue
            t = urllib.parse.unquote(tgt.split("#", 1)[0].strip())
            if not t or PLACEHOLDER.search(t) or NAME_TEMPLATE.search(t):
                continue
            rel = (doc.parent / t).resolve()
            try:
                out.append((lineno, str(rel.relative_to(ROOT))))
            except ValueError:
                continue
    return out


def paths_from_inline(text: str, tops: set[str]) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        for span in INLINE.findall(raw):
            s = span.strip()
            if "/" not in s or " " in s or PLACEHOLDER.search(s) or NAME_TEMPLATE.search(s):
                continue
            first = s.split("/", 1)[0]
            if first not in tops:
                continue
            out.append((lineno, s.rstrip("/")))
    return out


def indice_adr() -> list[dict]:
    """Gli ADR che esistono su disco e non compaiono in `docs/INDEX.md` §4.

    Un'assenza, non un percorso sbagliato: nessun link e' rotto, manca una riga.
    L'insieme si conta da `plans/adr/` — quarta regola di ADR-0045 — invece di
    fidarsi dell'elenco che si sta controllando.
    """
    indice = ROOT / INDICE_ADR
    cartella = ROOT / CARTELLA_ADR
    if not indice.exists() or not cartella.is_dir():
        return []
    citati = set(LINK_ADR.findall(indice.read_text(encoding="utf-8", errors="ignore")))
    esistenti = {f.name for f in cartella.glob("ADR-*.md")}
    return [{"doc": INDICE_ADR, "line": 0, "path": f"{CARTELLA_ADR}/{nome}",
             "source": "indice", "reason": "ADR esistente e non elencato"}
            for nome in sorted(esistenti - citati)]


def check_doc(doc_rel: str, tops: set[str], solo_link: bool = False) -> list[dict]:
    """I percorsi citati e inesistenti di un documento.

    `solo_link` restringe al controllo dei link markdown. Serve a `--sorgenti`:
    alberi e path inline sono tarati sui tre documenti d'ingresso, e scatenarli
    su seicento file aprirebbe una superficie di falsi positivi che nessuno ha
    misurato — l'errore che il lotto 4a aveva evitato apposta.
    """
    doc = ROOT / doc_rel
    if not doc.exists():
        return [{"doc": doc_rel, "line": 0, "path": doc_rel, "source": "doc", "reason": "documento assente"}]
    text = doc.read_text(encoding="utf-8", errors="ignore")
    skip = ignored_lines(text)
    found: list[dict] = []
    seen: set[tuple[str, str]] = set()
    controlli = [("link", paths_from_links(text, doc))]
    if not solo_link:
        controlli = [("tree", paths_from_tree_blocks(text)),
                     *controlli,
                     ("inline", paths_from_inline(text, tops))]
    for source, items in controlli:
        for lineno, rel in items:
            if lineno in skip or (source, rel) in seen:
                continue
            seen.add((source, rel))
            if _is_generated_mirror(rel) or _exists(rel):
                continue
            found.append({"doc": doc_rel, "line": lineno, "path": rel, "source": source,
                          "reason": "percorso inesistente"})
    return found


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="validate_docs.py",
        description="Verifica che i percorsi citati nei documenti d'ingresso esistano davvero.",
    )
    ap.add_argument("--doc", action="append", metavar="FILE",
                    help="Documento da controllare (ripetibile). Default: AGENTS.md, README.md, docs/INDEX.md.")
    ap.add_argument("--sorgenti", action="store_true",
                    help="Tutti i markdown scritti a mano: link relativi + percorsi assoluti. "
                         "Esclude generati, mirror per-agente e pacchetti vendored.")
    ap.add_argument("--verbose", action="store_true", help="Elenca anche i percorsi verificati con successo.")
    ap.add_argument("--json", action="store_true", help="Report in JSON (opt-in).")
    args = ap.parse_args(argv)

    if args.sorgenti and args.doc:
        ap.error("--sorgenti enumera l'insieme da solo: non si combina con --doc")

    tops = _toplevel_dirs()
    problems: list[dict] = []

    if args.sorgenti:
        docs = sorgenti(".md")
        for d in docs:
            problems.extend(check_doc(d, tops, solo_link=True))
        # I path assoluti si cercano anche negli script: e' li' che fanno danno.
        for d in sorgenti(".md", ".py"):
            problems.extend(percorsi_assoluti(d))
        problems.extend(indice_adr())
    else:
        docs = args.doc or DEFAULT_DOCS
        for d in docs:
            problems.extend(check_doc(d, tops))

    problems.sort(key=lambda p: (p["doc"], p["line"], p["path"]))

    if args.json:
        print(json.dumps({"report_version": 1, "docs": docs, "problems": problems},
                         indent=2, ensure_ascii=False, sort_keys=False))
        return 1 if problems else 0

    assoluti = [p for p in problems if p["source"] == "assoluto"]
    mancanti = [p for p in problems if p["source"] == "indice"]
    inesistenti = [p for p in problems if p["source"] not in {"assoluto", "indice"}]

    if not problems:
        coda = ", nessun percorso inesistente ne' assoluto" if args.sorgenti else ", nessun percorso inesistente"
        print(f"✓ validate_docs: {len(docs)} documenti{coda}")
        if args.verbose:
            for d in docs:
                print(f"  · {d}")
        return 0

    print(f"✗ validate_docs: {len(problems)} percorsi da correggere\n", file=sys.stderr)
    for p in problems:
        print(f"  {p['doc']}:{p['line']}  [{p['source']}]  {p['path']}", file=sys.stderr)
    if inesistenti:
        print("\nLa documentazione asserisce una struttura che il filesystem non ha.",
              file=sys.stderr)
        print("Correggere il documento (o creare il percorso). Finding T4, audit 2026-08-05.",
              file=sys.stderr)
    if mancanti:
        print(f"\n{len(mancanti)} ADR esistono e non sono elencati in {INDICE_ADR} §4.",
              file=sys.stderr)
        print("Un indice a mano accanto a una cartella si sfasa. Aggiungere la riga.",
              file=sys.stderr)
    if assoluti:
        print("\nUn percorso assoluto rende il documento vero su un solo computer.",
              file=sys.stderr)
        print("Renderlo relativo alla radice del repo. Se la riga *descrive* il difetto",
              file=sys.stderr)
        print("invece di commetterlo, marcarla: <!-- validate-docs: ignore -->",
              file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
