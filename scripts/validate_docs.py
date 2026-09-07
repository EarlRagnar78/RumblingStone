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

  Fuori scope per costruzione (niente falsi positivi): URL, ancore, glob
  (`*`, `?`), segnaposto (`<...>`, `[...]`, `percorso/relativo/...`), e i path
  che il documento marca esplicitamente come esempio.

Uso
  python3 scripts/validate_docs.py [--verbose] [--json] [--doc FILE ...]

Input   AGENTS.md, README.md, docs/INDEX.md (override con --doc)
Output  stdout testuale, oppure JSON con --json
Exit    0 = tutti i percorsi esistono · 1 = percorsi inesistenti · 2 = errore d'uso
"""
from __future__ import annotations

import argparse
import json
import re
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
        if in_block or IGNORE_LINE in raw:
            out.add(lineno)
    return out


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


def paths_from_links(text: str, doc: Path) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
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


def check_doc(doc_rel: str, tops: set[str]) -> list[dict]:
    doc = ROOT / doc_rel
    if not doc.exists():
        return [{"doc": doc_rel, "line": 0, "path": doc_rel, "source": "doc", "reason": "documento assente"}]
    text = doc.read_text(encoding="utf-8", errors="ignore")
    skip = ignored_lines(text)
    found: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for source, items in (
        ("tree", paths_from_tree_blocks(text)),
        ("link", paths_from_links(text, doc)),
        ("inline", paths_from_inline(text, tops)),
    ):
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
    ap.add_argument("--verbose", action="store_true", help="Elenca anche i percorsi verificati con successo.")
    ap.add_argument("--json", action="store_true", help="Report in JSON (opt-in).")
    args = ap.parse_args(argv)

    docs = args.doc or DEFAULT_DOCS
    tops = _toplevel_dirs()

    problems: list[dict] = []
    for d in docs:
        problems.extend(check_doc(d, tops))
    problems.sort(key=lambda p: (p["doc"], p["line"], p["path"]))

    if args.json:
        print(json.dumps({"report_version": 1, "docs": docs, "problems": problems},
                         indent=2, ensure_ascii=False, sort_keys=False))
        return 1 if problems else 0

    if not problems:
        print(f"✓ validate_docs: {len(docs)} documenti, nessun percorso inesistente")
        if args.verbose:
            for d in docs:
                print(f"  · {d}")
        return 0

    print(f"✗ validate_docs: {len(problems)} percorsi citati e inesistenti\n", file=sys.stderr)
    for p in problems:
        print(f"  {p['doc']}:{p['line']}  [{p['source']}]  {p['path']}", file=sys.stderr)
    print("\nLa documentazione asserisce una struttura che il filesystem non ha.",
          file=sys.stderr)
    print("Correggere il documento (o creare il percorso). Finding T4, audit 2026-08-05.",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
