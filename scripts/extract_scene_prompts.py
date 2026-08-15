#!/usr/bin/env python3
"""extract_scene_prompts.py — estrae le SCENE illustrabili di un arco e genera
lo scheletro del file dei prompt immagine (ADR-0015).

Divisione del lavoro (come per le mappe): **lo script fa la parte meccanica**
— trovare tutti i read-aloud, incrociarli con l'atlante asset e con le
immagini già presenti, dire cosa è scoperto — **l'agente (o il DM) scrive i
prompt**, che sono lavoro creativo e non si generano con una regex.

Cosa estrae:
  1. ogni blocco **read-aloud** dei master dell'arco (blockquote etichettato
     `Read-aloud`/`Read aloud`), con file, sezione `§` di appartenenza e un
     estratto: è la descrizione-sorgente da cui nasce il prompt;
  2. le voci dell'**atlante asset** (`ARC*-ATLANTE-ASSET.md`), per sapere
     quali scene hanno GIÀ un'immagine;
  3. il contenuto di `Immagini/`, per la copertura reale.

Output: un file markdown con una **scheda per scena**, precompilata con
fonte ed estratto e con i campi del prompt da riempire (ADR-0015 §2).
Se il file esiste già, le schede con un prompt scritto **non vengono
sovrascritte**: si aggiungono solo le scene nuove (idempotente).

Uso:
    python3 scripts/extract_scene_prompts.py "07_il Portale Della Forgia Eterna"
    python3 scripts/extract_scene_prompts.py <arco> --list          # solo elenco
    python3 scripts/extract_scene_prompts.py <arco> -o <file.md>
    python3 scripts/dm.py prompts <arco>                            # equivalente

Exit code: 0 = ok · 1 = nessuna scena trovata · 2 = uso errato/arco assente.
Dipendenze: solo stdlib.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

READ_ALOUD = re.compile(r"^>\s*\*\*Read[- ]aloud([^*]*)\*\*\.?\s*(.*)$", re.I)
HEADING = re.compile(r"^(#{1,4})\s+(.*)$")
IMG_EXT = {".webp", ".png", ".jpg", ".jpeg"}


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s or "scena"


def clean(s: str) -> str:
    """Toglie marcatori markdown da un estratto, per leggibilità."""
    s = re.sub(r"[*_`]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def extract_scenes(arc_dir: Path) -> list[dict]:
    """[{file, section, label, excerpt}] — read-aloud in ordine deterministico."""
    scenes: list[dict] = []
    for md in sorted(arc_dir.glob("*.md")):
        if md.name.startswith(("PIANO-", "ERRATA", "CORREZIONE")):
            continue
        section = ""
        lines = md.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, line in enumerate(lines):
            h = HEADING.match(line)
            if h:
                section = clean(h.group(2))
                continue
            m = READ_ALOUD.match(line)
            if not m:
                continue
            # il corpo del box: righe blockquote successive
            body = [m.group(2)]
            for nxt in lines[i + 1:]:
                if not nxt.startswith(">"):
                    break
                body.append(nxt.lstrip("> ").rstrip())
            excerpt = clean(" ".join(body))
            scenes.append({
                "file": md.name,
                "section": section,
                "label": clean(m.group(1)).strip("() ") or "scena",
                "excerpt": excerpt[:600],
            })
    return scenes


def existing_images(arc_dir: Path) -> list[str]:
    img_dir = arc_dir / "Immagini"
    if not img_dir.is_dir():
        return []
    return sorted(p.name for p in img_dir.iterdir() if p.suffix.lower() in IMG_EXT)


def assign_keys(scenes: list[dict]) -> None:
    """Chiave stabile e UNIVOCA per scena (due read-aloud nella stessa sezione
    prendono `-2`, `-3`…): è l'ancora con cui si ritrovano le schede già
    compilate quando si rigenera."""
    seen: dict[str, int] = {}
    for s in scenes:
        base = slug(s["section"])[:60]
        seen[base] = seen.get(base, 0) + 1
        s["key"] = base if seen[base] == 1 else f"{base}-{seen[base]}"


def card(scene: dict, n: int) -> str:
    """Scheda-scena precompilata (i campi del prompt li riempie l'agente)."""
    key = scene["key"]
    return f"""### {n:02d} · {scene['section']}  `[{key}]`

- **Fonte**: `{scene['file']}` — {scene['section']}
- **Etichetta regia**: {scene['label']}
- **Destinatario**: `[da decidere: pg | dm]`  ·  **Formato**: `[16:9 splash | 3:4 handout | 1:1 token]`
- **Stato**: ⬜ prompt da scrivere

> *Estratto sorgente (da cui ricavare il prompt — non è il prompt):*
> {scene['excerpt']}

**Prompt (EN)**
```text
[DA SCRIVERE — vedi ADR-0015 §2: paragrafo scena + paragrafo direzione
artistica; scala per paragone, materiali, luce, mood; niente nomi di
artisti viventi]
```

**Da evitare**: `text, letters, watermark, signature, modern objects, cartoon`
**Note di coerenza d'arco**: vedi «Bibbia visiva» in testa a questo file.

"""


def build_document(arc_name: str, scenes: list[dict], images: list[str]) -> str:
    head = f"""# Prompt immagine — {arc_name}

> **Generato da** `scripts/extract_scene_prompts.py` (parte meccanica) e
> **completato a mano/da agente** (i prompt). Standard: **ADR-0015**.
> Rigenerando, le schede con un prompt già scritto NON vengono toccate.
>
> ⚖️ **Confini IP** (ADR-0005): si descrivono convenzioni di stile — mai
> «in the style of <artista vivente>», mai immagini altrui come reference.
> 🔒 **Spoiler**: le schede marcate `dm` non si mostrano ai giocatori prima
> del loro momento (ADR-0013 §3).

## Bibbia visiva dell'arco (compilare una volta, vale per tutte le scene)

- **Palette**: `[es. mithral argento · verde smeraldo · nero-violetto]`
- **Luce**: `[es. due sole sorgenti: gemma verde + rune; buio esterno]`
- **Resa**: `illustrazione dipinta digitale, manuale fantasy classico anni 2000,
  pennellata visibile, alto dettaglio su pietra e metallo`
- **Coerenza**: genera prima la scena-madre, poi le altre chiedendo
  *«same world, same palette and lighting as the previous image»*.

## Copertura attuale

- Scene con read-aloud trovate: **{len(scenes)}**
- Immagini già presenti in `Immagini/`: **{len(images)}**

<details><summary>Immagini esistenti</summary>

{chr(10).join(f'- `{i}`' for i in images) if images else '_(nessuna)_'}

</details>

---

## Schede-scena

"""
    return head + "".join(card(s, i) for i, s in enumerate(scenes, 1))


MANUAL_HEADER = "## Schede aggiunte a mano (oggetti, artefatti, ritratti)\n"


def merge_with_existing(new_doc: str, out: Path) -> str:
    """Non perde MAI lavoro già fatto (ADR-0015 §4).

    - scheda già compilata la cui chiave esiste ancora fra le scene estratte
      → sostituisce quella nuova (vuota) con quella scritta;
    - scheda compilata **senza** corrispondenza fra le scene (aggiunta a mano
      per un artefatto/ritratto, o scena rimossa dal master) → viene
      **riportata in coda**, non buttata.
    """
    if not out.exists():
        return new_doc
    old = out.read_text(encoding="utf-8")
    new_keys = set(re.findall(r"`\[([a-z0-9-]+)\]`", new_doc))
    kept, carried = 0, []
    card_re = re.compile(r"^### [^\n]*`\[([a-z0-9-]+)\]`[^\n]*\n.*?(?=\n### |\n## |\Z)",
                         re.S | re.M)
    for m in card_re.finditer(old):
        block, key = m.group(0).rstrip() + "\n", m.group(1)
        if "DA SCRIVERE" in block:
            continue
        if key in new_keys:
            new_doc = re.sub(
                rf"^### [^\n]*`\[{re.escape(key)}\]`[^\n]*\n.*?(?=\n### |\n## |\Z)",
                lambda _m: block, new_doc, count=1, flags=re.S | re.M)
            kept += 1
        else:
            carried.append(block)
    if carried:
        new_doc = new_doc.rstrip() + "\n\n---\n\n" + MANUAL_HEADER + "\n" + "\n".join(carried) + "\n"
    if kept or carried:
        print(f"[prompts] conservate {kept} schede compilate, riportate {len(carried)} schede a mano")
    return new_doc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("arc", help="cartella dell'arco (es. \"07_il Portale Della Forgia Eterna\")")
    ap.add_argument("-o", "--output", help="file di output (default: <arco>/Immagini/PROMPT-IMMAGINI-<ARCO>.md)")
    ap.add_argument("--list", action="store_true", help="elenca soltanto le scene trovate")
    args = ap.parse_args(argv)

    arc_dir = (ROOT / args.arc) if not Path(args.arc).is_absolute() else Path(args.arc)
    if not arc_dir.is_dir():
        print(f"ERRORE: arco non trovato: {arc_dir}", file=sys.stderr)
        return 2

    scenes = extract_scenes(arc_dir)
    if not scenes:
        print(f"Nessun read-aloud trovato in {arc_dir.name}", file=sys.stderr)
        return 1

    if args.list:
        for i, s in enumerate(scenes, 1):
            print(f"  {i:02d}  {s['file']:<44} {s['section'][:60]}")
        return 0

    assign_keys(scenes)
    images = existing_images(arc_dir)
    doc = build_document(arc_dir.name, scenes, images)

    tag = re.sub(r"[^A-Z0-9]", "", arc_dir.name.upper())[:5] or "ARCO"
    out = Path(args.output) if args.output else arc_dir / "Immagini" / f"PROMPT-IMMAGINI-{tag}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = merge_with_existing(doc, out).rstrip() + "\n"   # idempotenza byte-per-byte
    out.write_text(doc, encoding="utf-8")
    print(f"OK {out} — {len(scenes)} scene, {len(images)} immagini esistenti")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
