#!/usr/bin/env python3
"""
hype_homebrew.py — Veste Homebrewery V3 per recap e handout (Lotti K-B1/K-B2).

Prende il recap spoiler-safe già generato da `session_recap.py` (MAI
rigenera o duplica il suo filtro: regola d'oro 5 del piano DM-TOOLKIT) e
lo avvolge in markdown **Homebrewery V3** — copertina, due colonne stile
Manuale del Giocatore, box-nota per i presagi — pronto da incollare su
https://homebrewery.naturalcrit.com/ (bottone "New", incolla, condividi).

Modalità:
  (default)              ultimo campaign/recaps/recap-*.md → .hb.md
  --recap FILE           recap specifico
  --handout TIPO --da F  handout giocatori dai template (Lotto K-B2)

Output:
  campaign/recaps/homebrew/recap-YYYY-MM-DD.hb.md   (recap-hype)
  <sorgente>.hb.md accanto al --da, o --out          (handout)

Filosofia (ADR-0003): il markdown del repo è il MASTER; questo file è un
artefatto generato — si rigenera, non si edita a mano. Zero dipendenze
esterne (stdlib), deterministico, niente AI.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RECAPS = REPO / "campaign" / "recaps"
TEMPLATES = REPO / "campaign" / "templates" / "homebrew"

GENERATED_HEADER = (
    "<!-- Auto-generated — do not edit by hand.\n"
    "     Sorgente: {src}\n"
    "     Rigenera con: {regen}\n"
    "     Incolla tutto su https://homebrewery.naturalcrit.com/ (New brew). -->\n\n"
)

# righe di testo (circa) che entrano in una pagina V3 a due colonne
LINES_PER_PAGE = 110


def rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(REPO))
    except ValueError:
        return str(p)


def die(msg: str) -> "sys.NoReturn":
    print(f"[hype] ✗ {msg}", file=sys.stderr)
    raise SystemExit(1)


def guard_spoiler_safe(text: str, src: Path) -> None:
    """Cintura oltre alle bretelle: mai impaginare materiale DM-private."""
    if re.search(r"^##\s*DM notes", text, flags=re.M | re.I):
        die(f"{src} contiene una sezione DM-private: non è un file player-facing")


def latest_recap() -> Path:
    cands = sorted(RECAPS.glob("recap-????-??-??.md"))
    if not cands:
        die("nessun recap in campaign/recaps/ — genera prima con `dm.py recap`")
    return cands[-1]


# ------------------------------------------------------------- recap mode


def build_cover(title: str, subtitle: str, meta: str) -> str:
    return f"""{{{{frontCover}}}}

{{{{logo ![](/assets/naturalCritLogoRed.svg)}}}}

# {title}
## {subtitle}
___

{{{{banner HYPE!}}}}

{{{{footnote
  {meta}
}}}}

<!-- Copertina: per lo sfondo carica un'immagine dell'arco (prompt in
     campaign/ai-media-prompts/) sul brew e inserisci qui:
     ![background](URL){{position:absolute,top:0,left:0,height:100%}} -->

\\page
"""


def wrap_section(heading: str, body: list[str]) -> str:
    """Sezioni con vesti dedicate: presagi in nota, congedo in descrittivo."""
    text = "\n".join(body).strip("\n")
    if re.match(r"V\.\s", heading):  # Sussurri nel vento
        return f"{{{{note\n##### {heading}\n{text}\n}}}}\n"
    if re.match(r"VI\.\s", heading):  # La prossima alba
        return f"{{{{descriptive\n##### {heading}\n{text}\n}}}}\n"
    return f"## {heading}\n{text}\n"


def paginate(blocks: list[str]) -> str:
    """Homebrewery V3 non manda a capo pagina da solo: \\page euristico."""
    out: list[str] = []
    lines_on_page = 0
    footer = "{{pageNumber,auto}}\n{{footnote CRONACHE DEI CUSTODI ETERNI}}\n"
    for block in blocks:
        n = block.count("\n") + 2
        if lines_on_page and lines_on_page + n > LINES_PER_PAGE:
            out.append(footer + "\n\\page\n")
            lines_on_page = 0
        out.append(block)
        lines_on_page += n
    out.append(footer)
    return "\n".join(out)


def hype_recap(recap_path: Path, out: Path | None) -> Path:
    text = recap_path.read_text(encoding="utf-8")
    guard_spoiler_safe(text, recap_path)

    lines = text.splitlines()
    title = "Cronache dei Custodi Eterni"
    subtitle = "Recap & Preludio"
    meta = ""
    body_start = 0
    for i, ln in enumerate(lines):
        m = re.match(r"#\s+(.*)", ln)
        if m:
            parts = [p.strip() for p in m.group(1).split("—", 1)]
            title = parts[0]
            if len(parts) > 1:
                subtitle = parts[1]
            body_start = i + 1
            continue
        if ln.startswith("*Generato") or ln.startswith("**Data in-mondo**"):
            meta += re.sub(r"[*]", "", ln) + " · "
            body_start = i + 1
        elif ln.strip() == "---" and body_start == i:
            body_start = i + 1
        elif body_start and ln.strip() and not ln.startswith(("*", "#", "-")):
            break

    # spezza il corpo in sezioni "## ..."
    blocks: list[str] = []
    heading: str | None = None
    acc: list[str] = []
    for ln in lines[body_start:]:
        if heading is None and ln.strip() in {"---", "___", ""} and not acc:
            continue  # separatori orfani prima della prima sezione
        m = re.match(r"##\s+(.*)", ln)
        if m:
            if heading is not None:
                blocks.append(wrap_section(heading, acc))
            elif acc and any(s.strip() for s in acc):
                blocks.append("\n".join(acc).strip("\n"))
            heading, acc = m.group(1).strip(), []
        else:
            acc.append(ln)
    if heading is not None:
        blocks.append(wrap_section(heading, acc))

    hb = (
        GENERATED_HEADER.format(src=rel(recap_path), regen="python3 scripts/dm.py recap --hype")
        + build_cover(title, subtitle, meta.rstrip(" ·"))
        + paginate(blocks)
    )

    if out is None:
        outdir = RECAPS / "homebrew"
        outdir.mkdir(parents=True, exist_ok=True)
        out = outdir / (recap_path.stem + ".hb.md")
    out.write_text(hb, encoding="utf-8")
    print(f"[hype] ✓ {rel(out)} — incolla su homebrewery.naturalcrit.com")
    return out


# ------------------------------------------------------------- chronology


def update_chronology() -> Path:
    """Rigenera l'indice-cronologia degli handout (feedback DM 2026-07-12):
    i recap ordinati per data reale + Giorno di Marcia in-mondo (calendario
    di Faerûn: l'etichetta Harptos piena appare quando session_recap.py ha
    l'ancora MARCH_DAY1_HARPTOS impostata), più il materiale senza data."""
    outdir = RECAPS / "homebrew"
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for f in sorted(outdir.glob("recap-????-??-??.hb.md")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        m_day = re.search(r'(?:Giorno\s+(\d+)\s+della\s+Marcia|'
                          r'(\d+\s+\w+)\s+\(Giorno\s+\d+\s+della\s+Marcia\))', text)
        giorno = ""
        if m_day:
            giorno = (f"Giorno {m_day.group(1)}" if m_day.group(1)
                      else m_day.group(2))
        m_month = re.search(r'Data in-mondo\s*:?\**\s*([^·\n]+)', text)
        mese = m_month.group(1).strip().rstrip("*") if m_month else ""
        real = f.stem.replace("recap-", "").replace(".hb", "")
        rows.append((real, giorno, mese, f.name))

    extra = [p for p in sorted(REPO.rglob("*.hb.md"))
             if "templates" not in p.parts and p.parent != outdir]

    lines = [
        "<!-- Auto-generated — do not edit by hand.",
        "     Rigenerato da scripts/hype_homebrew.py a ogni recap/handout.",
        "     Ordina gli handout man mano che le sessioni avanzano. -->",
        "",
        "{{wide",
        "# Cronache dei Custodi Eterni — Cronologia degli handout",
        "}}",
        "",
        "*Il tempo di Faerûn scorre col calendario di Harptos; la campagna",
        "conta i **Giorni della Marcia**. Consegna (e rileggi) gli handout",
        "in quest'ordine.*",
        "",
        "## Recap di sessione (in ordine di tempo)",
        "",
        "| # | Data reale | Tempo in-mondo | Mese (Faerûn) | File |",
        "|:-:|:--|:--|:--|:--|",
    ]
    for i, (real, giorno, mese, name) in enumerate(sorted(rows), 1):
        lines.append(f"| {i} | {real} | {giorno or '—'} | {mese or '—'} | `{name}` |")
    lines += [
        "",
        "## Materiale senza data (si consegna quando i fascicoli lo dicono)",
        "",
    ]
    for p in extra:
        lines.append(f"- `{rel(p)}`")
    lines += ["", "{{pageNumber,auto}}",
              "{{footnote CRONACHE DEI CUSTODI ETERNI · CRONOLOGIA}}", ""]

    out = outdir / "00-CRONOLOGIA.hb.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[hype] ✓ {rel(out)} — cronologia handout aggiornata")
    return out


# ----------------------------------------------------------- handout mode


def extract_section(text: str, sezione: str) -> str:
    """Estrae la sola sezione `## …sezione…` (fino al prossimo ##)."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"##\s", ln) and sezione.lower() in ln.lower():
            start = i
            break
    if start is None:
        die(f"sezione '{sezione}' non trovata nel file sorgente")
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"##?\s", lines[j]) and not lines[j].startswith("###"):
            end = j
            break
    return "\n".join(lines[start:end])


def strip_dm_staging(text: str) -> str:
    """Toglie i paragrafi-blockquote di regia DM ('Quando darlo', fonti)."""
    paragraphs = re.split(r"\n\s*\n", text)
    kept = [p for p in paragraphs
            if not (p.lstrip().startswith(">") and re.search(
                r"\*\*Quando darlo\*\*|Come si usa questa scheda", p))]
    return "\n\n".join(kept)


def hype_handout(tipo: str, da: str | None, out: str | None,
                 sezione: str | None = None) -> Path:
    tpl = TEMPLATES / f"{tipo}.hb.md"
    if not tpl.exists():
        die(f"template mancante: {rel(tpl)} (Lotto K-B2)")
    template = tpl.read_text(encoding="utf-8")
    # il commento d'uso appartiene al template master, non all'artefatto
    template = re.sub(r"^\s*<!--.*?-->\s*", "", template, flags=re.S)

    if da:
        src = Path(da)
        if not src.exists():
            die(f"file sorgente non trovato: {da}")
        content = src.read_text(encoding="utf-8")
        guard_spoiler_safe(content, src)
        if sezione:
            content = extract_section(content, sezione)
            m = re.match(r"##\s+(.*)", content)
            titolo = re.sub(r"^HANDOUT\s*\d+\s*—\s*", "", m.group(1).strip()) if m else sezione
            body = re.sub(r"^##\s+.*\n", "", content, count=1)
        else:
            body = re.sub(r"^#\s+.*\n", "", content, count=1)  # H1 → lo mette il template
            m = re.match(r"#\s+(.*)", content)
            titolo = m.group(1).strip() if m else src.stem.replace("-", " ").title()
        body = strip_dm_staging(body)
        # separatori orfani in testa/coda (--- ereditati dal file sorgente)
        body = re.sub(r"^(\s*(---|___)\s*\n)+", "", body)
        body = re.sub(r"(\n(---|___)\s*)+\s*$", "\n", body)
    else:
        body = "_(compila: passa un file markdown con `--da`)_"
        titolo = tipo.replace("-", " ").title()

    regen = f"python3 scripts/dm.py handout --tipo {tipo}" + (f" --da {da}" if da else "")
    hb = GENERATED_HEADER.format(src=da or f"template {tipo}", regen=regen) + (
        template.replace("[[TITOLO]]", titolo)
                .replace("[[CONTENUTO]]", body.strip())
                .replace("[[DATA]]", date.today().isoformat())
    )

    out_path = Path(out) if out else (Path(da).with_suffix(".hb.md") if da
                                      else REPO / f"{tipo}.hb.md")
    out_path.write_text(hb, encoding="utf-8")
    print(f"[hype] ✓ {out_path} — incolla su homebrewery.naturalcrit.com")
    return out_path


# ------------------------------------------------------------------ main


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="hype_homebrew.py",
        description="Recap e handout in veste Homebrewery V3 (artefatti generati).",
    )
    ap.add_argument("--recap", help="file recap specifico (default: l'ultimo)")
    ap.add_argument("--handout", metavar="TIPO",
                    help="genera un handout: lettera, profezia, avviso-torneo, scheda-artefatto")
    ap.add_argument("--da", help="(handout) file markdown sorgente col contenuto")
    ap.add_argument("--sezione", help="(handout) estrai solo la sezione '## …' che contiene questo testo")
    ap.add_argument("--out", help="file di output esplicito")
    ap.add_argument("--cronologia", action="store_true",
                    help="rigenera solo l'indice-cronologia degli handout")
    args = ap.parse_args(argv)

    if args.cronologia:
        update_chronology()
        return 0
    if args.handout:
        hype_handout(args.handout, args.da, args.out, args.sezione)
    else:
        recap = Path(args.recap) if args.recap else latest_recap()
        if not recap.exists():
            die(f"recap non trovato: {recap}")
        hype_recap(recap, Path(args.out) if args.out else None)
    update_chronology()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
