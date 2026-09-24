#!/usr/bin/env python3
"""validate_standalone.py — gate CI per i moduli autoconclusivi (`STANDALONE-*/`).

`validate_modules.py` copre solo i master `ARC*-DEF-*.md` della campagna: i moduli
standalone avevano **zero gate**. Questo script chiude il buco con controlli che una
regex può fare bene e un revisore umano fa male:

  1. **File obbligatori** — un modulo standalone senza guida DM o senza nota IP non
     è un modulo, è una bozza.
  2. **Riferimenti incrociati** — ogni `` `FILE.md` `` e ogni link relativo citato
     dentro il modulo deve esistere. È il difetto che si crea da solo rinominando.
  3. **Schede pregenerate** — ogni scheda ha le sezioni che servono al tavolo
     (Difesa / Attacco / Statistiche / Equipaggiamento) e dichiara un GS.
  4. **Termini vietati** — meccaniche 5e in un modulo 3.5/PF1e (vantaggio,
     svantaggio, azione bonus, reazione, DC al posto di CD).
  5. **Read-aloud** — ogni file-giornata deve avere almeno un box di prosa: un
     modulo senza testo da leggere ad alta voce non si gioca, si riassume.
  6. **I due contatori** — devono essere dichiarati con il valore di partenza.
  7. **Generatori locali** (ADR-0017 §4) — i `.py` sotto la cartella del modulo devono
     essere stdlib-only, avere una docstring, essere citati in un `.md` e compilare.

**Due famiglie di moduli, due serie di controlli.** I moduli `STANDALONE-*/` hanno
master markdown e prendono i sette controlli qui sopra. I moduli sotto
`10-stand-alone/*/` sono scritti direttamente in **HTML** — un supporto fuori da
ADR-0003 e da entrambe le catene di impaginazione — e fino al 2026-09-02 non
avevano **nessun** gate: la CI conosceva solo `STANDALONE-*`, e ~2.750 righe di
modulo non erano viste da niente. Su HTML valgono i controlli che hanno senso:
titolo e `<h1>`, link relativi risolvibili, ancore che esistono davvero, `id`
non duplicati, e gli stessi termini 5e vietati.

⚠ Questo script dà all'HTML **un gate**, non una promozione: non lo porta dentro
la catena di stampa. La conversione a master markdown + manifest è una decisione
a parte (`PIANO-CHIUSURA-CATENA-EDITORIALE`, lotto F4).

Esce con codice 1 se trova errori: è pensato per la CI.

Uso:
    python3 scripts/validate_standalone.py            # tutti i moduli, di entrambe le famiglie
    python3 scripts/validate_standalone.py --dir X    # solo quello
"""
from __future__ import annotations

import argparse
import re
from html import unescape  # le entita' («, ») sono testo, non markup
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# File che un modulo autoconclusivo deve avere per essere giocabile senza altro.
REQUIRED = {
    "hub": r"^00-.*\.md$",
    "guida del DM": r"^0?7-GUIDA-DM.*\.md$",
    "schede pregenerate": r"^PREGEN-.*\.md$",
    "statblocchi": r"^STATBLOCCHI.*\.md$",
    "nota IP": r"^IP-E-LICENZE\.md$",
}
# Almeno un file-giornata/capitolo di sessione.
SESSION_RE = re.compile(r"^0[1-3]-GIORNO-.*\.md$")

# Meccaniche 5e: non hanno posto in un modulo 3.5 o PF1e.
# ⚠ Solo le forme che sono DAVVERO la meccanica 5e. In italiano «una Lunghezza di
# vantaggio» è lingua normale: bandirla sarebbe un falso positivo, e un validatore
# che grida al lupo viene disattivato entro una settimana.
BANNED = {
    r"\bazione bonus\b": "azione bonus (5e) → azione veloce",
    r"\bcon (?:un )?vantaggio\b": "tirare «con vantaggio» (5e) → nessun equivalente",
    r"\bcon (?:uno )?svantaggio\b": "tirare «con svantaggio» (5e) → nessun equivalente",
    r"\blair action": "lair action (5e)",
    r"(?<![A-Za-z])DC\s+\d": "DC → CD (Classe Difficoltà)",
}

PREGEN_SECTIONS = ("Difesa", "Attacco", "Statistiche", "Equipaggiamento")

# I moduli a supporto HTML: una cartella per modulo sotto questa radice.
HTML_ROOT = "10-stand-alone"


def module_dirs(only: str | None) -> list[Path]:
    if only:
        p = (ROOT / only).resolve()
        return [p] if p.is_dir() and not _e_html(p) else []
    return sorted(d for d in ROOT.iterdir() if d.is_dir() and d.name.startswith("STANDALONE-"))


def _e_html(d: Path) -> bool:
    """Vero se la cartella è un modulo a supporto HTML (`10-stand-alone/<nome>/`)."""
    radice = (ROOT / HTML_ROOT).resolve()
    return radice in d.resolve().parents


def html_module_dirs(only: str | None) -> list[Path]:
    if only:
        p = (ROOT / only).resolve()
        return [p] if p.is_dir() and _e_html(p) else []
    radice = ROOT / HTML_ROOT
    if not radice.is_dir():
        return []
    return sorted(d for d in radice.iterdir() if d.is_dir() and any(d.glob("*.html")))


def check_required(mod: Path, errors: list[str]) -> None:
    names = [p.name for p in mod.glob("*.md")]
    for label, pattern in REQUIRED.items():
        if not any(re.match(pattern, n) for n in names):
            errors.append(f"{mod.name}: manca il file obbligatorio — {label} (`{pattern}`)")
    if not any(SESSION_RE.match(n) for n in names):
        errors.append(f"{mod.name}: nessun file-giornata (`0N-GIORNO-*.md`)")


_BASENAMES: set[str] | None = None


def _repo_basenames() -> set[str]:
    """Tutti i nomi-file del repo, per accettare le citazioni per nome corto.

    Il repo cita spesso un file col solo basename (`CREDITS.md`, `render_map_svg.py`)
    o con un percorso abbreviato con i puntini. Pretendere il percorso completo
    produrrebbe decine di falsi positivi e nessun difetto vero.
    """
    global _BASENAMES
    if _BASENAMES is None:
        _BASENAMES = {
            p.name for p in ROOT.rglob("*")
            if p.is_file() and ".git" not in p.parts and "node_modules" not in p.parts
        }
    return _BASENAMES


def check_crossrefs(mod: Path, errors: list[str]) -> None:
    """Ogni `FILE.md` citato fra backtick, e ogni link relativo, deve esistere."""
    backtick = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|json|svg|py))`")
    link = re.compile(r"\]\((?!https?:|#)([^)\s]+)\)")
    for f in sorted(mod.rglob("*.md")):
        if f.name.endswith(".hb.md"):
            continue  # artefatti Homebrewery: generati, non fonti
        text = f.read_text(encoding="utf-8", errors="ignore")
        for m in backtick.finditer(text):
            ref = m.group(1)
            if "*" in ref or ref.startswith(("<", ".")):
                continue  # glob, placeholder, o suffissi tipo `.hb.md`
            if (f.parent / ref).exists() or (mod / ref).exists() or (ROOT / ref).exists():
                continue
            if Path(ref).name in _repo_basenames():
                continue  # citato per nome corto: esiste altrove nel repo
            errors.append(f"{f.relative_to(ROOT)}: riferimento inesistente `{ref}`")
        for m in link.finditer(text):
            ref = m.group(1).split("#")[0]
            if not ref:
                continue
            if (f.parent / ref).exists() or (ROOT / ref).exists():
                continue
            errors.append(f"{f.relative_to(ROOT)}: link rotto ({ref}){_perche_manca(ref)}")


def _perche_manca(ref: str) -> str:
    """La riga in più quando il file manca per un motivo che si ripete.

    Le derivate leggere delle immagini (`.../web/*.jpg`) sono generate e
    finiscono sotto la regola `*.jpg` del `.gitignore`: su una macchina che le
    ha appena rigenerate il master «funziona», in un clone fresco il link è
    rotto. Dire solo «link rotto» manda a cercare un errore di battitura che
    non c'è — è successo due volte, su due rami diversi.
    """
    p = Path(ref)
    if p.suffix.lower() in (".jpg", ".jpeg", ".webp") and "web" in p.parts:
        return ("  ← derivata generata: o la committi (serve un'eccezione «!» nel "
                ".gitignore, che blocca *.jpg) o il master punta al PNG originale")
    return ""


def check_pregen(mod: Path, errors: list[str], warnings: list[str]) -> None:
    for f in mod.glob("PREGEN-*.md"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        sheets = re.findall(r"^##\s+\d+\s+·\s+(.+)$", text, re.M)
        if not sheets:
            errors.append(f"{f.relative_to(ROOT)}: nessuna scheda riconosciuta (`## N · NOME`)")
            return
        for sec in PREGEN_SECTIONS:
            found = len(re.findall(rf"^###\s+{sec}\b", text, re.M))
            # Equipaggiamento sta in grassetto nel corpo, non come heading
            if sec == "Equipaggiamento":
                found = text.count("**Equipaggiamento**")
            if found < len(sheets):
                errors.append(
                    f"{f.relative_to(ROOT)}: sezione «{sec}» presente {found} volte "
                    f"su {len(sheets)} schede"
                )
        if len(re.findall(r"\*\*GS \d", text)) < len(sheets):
            warnings.append(f"{f.relative_to(ROOT)}: non tutte le schede dichiarano un GS")


def check_banned(mod: Path, errors: list[str]) -> None:
    for f in sorted(mod.rglob("*.md")):
        if f.name.endswith(".hb.md"):
            continue  # generati dai sorgenti: il difetto va segnalato una volta sola
        text = f.read_text(encoding="utf-8", errors="ignore")
        for pattern, why in BANNED.items():
            for m in re.finditer(pattern, text, re.I):
                line = text[: m.start()].count("\n") + 1
                errors.append(f"{f.relative_to(ROOT)}:{line}: termine vietato — {why}")


def check_readaloud(mod: Path, errors: list[str]) -> None:
    for f in sorted(mod.glob("*.md")):
        if not SESSION_RE.match(f.name):
            continue
        blocks = len(re.findall(r"^>\s*\*", f.read_text(encoding="utf-8", errors="ignore"), re.M))
        if blocks < 3:
            errors.append(
                f"{f.relative_to(ROOT)}: solo {blocks} righe di read-aloud "
                f"(minimo 3 per un file-giornata)"
            )


def check_counters(mod: Path, errors: list[str]) -> None:
    joined = "\n".join(
        f.read_text(encoding="utf-8", errors="ignore") for f in mod.glob("*.md")
    )
    for name in ("Morale", "Onore"):
        if not re.search(rf"{name}[^\n]*parte da", joined):
            errors.append(f"{mod.name}: il contatore «{name}» non dichiara il valore di partenza")


def check_generators(mod: Path, errors: list[str], warnings: list[str]) -> None:
    """I generatori locali al modulo (ADR-0017 §4): stdlib, docstring, citati, compilano.

    Un modulo autoconclusivo possiede i propri generatori — stanno sotto la sua
    cartella e non in `scripts/`, quindi ADR-0012 non li copre. Le quattro condizioni
    che li tengono vivi si verificano qui.
    """
    import py_compile
    import tempfile

    third_party = re.compile(
        r"^\s*(?:import|from)\s+(cairosvg|PIL|numpy|yaml|requests|lxml|jinja2|bs4)\b", re.M
    )
    docs = "\n".join(
        f.read_text(encoding="utf-8", errors="ignore") for f in mod.rglob("*.md")
    )
    for gen in sorted(mod.rglob("*.py")):
        rel = gen.relative_to(ROOT)
        src = gen.read_text(encoding="utf-8", errors="ignore")
        if not re.match(r'^(#![^\n]*\n)?\s*"""', src):
            errors.append(f"{rel}: generatore senza docstring di modulo (ADR-0017 §4.2)")
        if third_party.search(src):
            errors.append(f"{rel}: generatore non stdlib-only (ADR-0017 §4.1)")
        if gen.name not in docs:
            errors.append(f"{rel}: generatore mai citato in un .md del modulo (ADR-0017 §4.3)")
        try:
            with tempfile.NamedTemporaryFile(suffix=".pyc", delete=True) as tmp:
                py_compile.compile(str(gen), cfile=tmp.name, doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{rel}: non compila — {exc.msg.splitlines()[0]}")
        if "rigenera" not in src.lower() and "regenera" not in src.lower():
            warnings.append(f"{rel}: la docstring non dice come si rigenera")


# ─────────────────────────────────────────────────────────────────────────────
# Moduli a supporto HTML (`10-stand-alone/*/`)
# ─────────────────────────────────────────────────────────────────────────────

def _rel(f: Path) -> str:
    """Percorso leggibile: relativo alla radice quando ci sta dentro, altrimenti
    il percorso pieno. Serve a poter provare i controlli su una cartella
    temporanea senza che il messaggio d'errore sollevi ValueError."""
    try:
        return str(f.relative_to(ROOT))
    except ValueError:
        return str(f)


_TAG = re.compile(r"<[^>]+>")
_STILE = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
_HREF = re.compile(r'href\s*=\s*"([^"]+)"', re.I)
_ID = re.compile(r'\bid\s*=\s*"([^"]+)"', re.I)
_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
_H1 = re.compile(r"<h1\b", re.I)
# «area 17» senza prefisso di livello. Il dry-run dell'Abbazia aveva trovato
# «16, 17, 18 usati tre volte su tre documenti» e l'aveva corretto nelle chiavi
# con i prefissi (A3, C19, G27) — ma i rimandi in prosa erano rimasti nudi.
# Fra la parola e il numero si ammettono **solo spazi**, mai un a capo. Un
# rimando vero (`area 17`) sta dentro una frase; un a capo, dopo `_testo`, vuol
# dire che in mezzo c'era un tag — cioe' che «stanza» e «3» stanno in due celle
# diverse della stessa tabella e non sono una frase. Con `\s+` il controllo
# leggeva `…verso quella stanza</td><td>3</td>` come «stanza 3» e segnalava un
# rimando che nel documento non esiste.
_AREA_NUDA = re.compile(r"\b(?:area|stanza|luogo)[ \t\u00a0]+(\d{1,3})\b", re.I)

# Menzione, non uso: «area 17» fra virgolette e' il documento che *parla* del
# rimando invece di farlo — ed e' esattamente cosi' che l'indice maestro
# dell'Abbazia descrive il difetto che ha corretto. Segnalarlo vorrebbe dire
# chiedere di riscrivere la spiegazione del difetto per farla assomigliare a un
# difetto in meno.
_MENZIONE = re.compile(r"[«\"\u201c\u2018']\s*$")


def _testo(html: str) -> str:
    """Il testo leggibile: via script, style e tag.

    I tag diventano **a capo**, non spazi: cosi' due celle di tabella restano due
    righe e non si saldano in una frase che nessuno ha scritto.
    """
    return unescape(_TAG.sub("\n", _STILE.sub("\n", html)))


def _ancore(html: str) -> set[str]:
    return set(_ID.findall(html))


def check_aree_ambigue(pagine: list[Path], nome: str, warnings: list[str]) -> None:
    """Lo stesso numero d'area citato senza prefisso in più file dello stesso modulo.

    Non è un errore di sintassi: è un'ambiguità. «area 6» in due documenti o è la
    stessa stanza — e allora il rimando funziona — o sono due stanze diverse, e
    allora il DM apre il file sbagliato mentre il tavolo aspetta. Dal di fuori i
    due casi sono indistinguibili, ed è esattamente per questo che serve il
    prefisso di livello.

    ⚠ **Warning, non errore**, come `validate_bestiario --rules`: la convenzione
    nasce oggi e il contenuto esistente la rispetta a metà. Diventa bloccante il
    giorno in cui il rumore è a zero — non prima, o il gate viene disattivato.
    """
    per_numero: dict[str, set[str]] = {}
    nude = 0
    for f in pagine:
        testo = _testo(f.read_text(encoding="utf-8", errors="ignore"))
        for m in _AREA_NUDA.finditer(testo):
            if _MENZIONE.search(testo[max(0, m.start() - 2):m.start()]):
                continue  # menzione fra virgolette, non un rimando
            per_numero.setdefault(m.group(1), set()).add(f.name)
            nude += 1
    ambigue = sorted((n, sorted(fs)) for n, fs in per_numero.items() if len(fs) > 1)
    for numero, files in ambigue:
        warnings.append(
            f"{nome}: «area {numero}» senza prefisso in {len(files)} file "
            f"({', '.join(files)}) — o è la stessa stanza o sono due, e da fuori "
            f"non si distingue: serve il prefisso di livello (A{numero}, C{numero}…)"
        )
    if nude and not ambigue:
        warnings.append(f"{nome}: {nude} rimandi «area N» senza prefisso di livello")


def check_html_module(mod: Path, errors: list[str], warnings: list[str]) -> None:
    """Un modulo scritto in HTML: che almeno stia in piedi da solo.

    Non si pretende validità XHTML — sarebbe una dipendenza e un mare di rumore.
    Si pretende ciò che rompe la lettura al tavolo: un titolo, un `<h1>`, i link
    che portano da qualche parte, le ancore che esistono e nessun `id` doppio (un
    `id` ripetuto rende ambigua ogni ancora che lo punta, ed è esattamente il
    difetto che il dry-run dell'Abbazia aveva trovato a mano sulla numerazione
    delle aree).
    """
    pagine = sorted(mod.glob("*.html"))
    if not pagine:
        errors.append(f"{mod.name}: nessun file .html nel modulo")
        return

    ancore: dict[Path, set[str]] = {}
    for f in pagine:
        html = f.read_text(encoding="utf-8", errors="ignore")
        rel = _rel(f)

        m = _TITLE.search(html)
        if not m or not m.group(1).strip():
            errors.append(f"{rel}: manca il <title> (è il nome che il DM vede nella scheda)")
        if not _H1.search(html):
            errors.append(f"{rel}: nessun <h1> (una pagina senza titolo in testa non si sfoglia)")

        visti: set[str] = set()
        for ident in _ID.findall(html):
            if ident in visti:
                errors.append(f"{rel}: id duplicato «{ident}» — ogni ancora che lo punta è ambigua")
            visti.add(ident)
        ancore[f] = visti

    for f in pagine:
        html = f.read_text(encoding="utf-8", errors="ignore")
        rel = _rel(f)
        for href in _HREF.findall(html):
            href = href.strip()
            if not href or href.startswith(("http://", "https://", "mailto:", "data:", "javascript:")):
                continue
            percorso, _, frammento = href.partition("#")
            bersaglio = f
            if percorso:
                cand = (f.parent / percorso).resolve()
                if not cand.is_file():
                    errors.append(f"{rel}: link rotto → {href}")
                    continue
                bersaglio = cand
            if frammento and frammento not in ancore.get(bersaglio, _ancore(
                    bersaglio.read_text(encoding="utf-8", errors="ignore"))):
                errors.append(f"{rel}: ancora inesistente → {href}")

    check_aree_ambigue(pagine, mod.name, warnings)

    testo = "\n".join(_testo(f.read_text(encoding="utf-8", errors="ignore")) for f in pagine)
    for pattern, why in BANNED.items():
        if re.search(pattern, testo, re.I):
            errors.append(f"{mod.name}: termine vietato nel testo — {why}")

    # Non è un errore, ma va detto a ogni passata: questo modulo non ha un
    # master markdown, quindi non entra in nessuna delle due catene e non può
    # avere un colophon. Il silenzio lo farebbe sembrare normale.
    if not any(mod.rglob("*.md")):
        warnings.append(
            f"{mod.name}: modulo a solo HTML — nessun master markdown (ADR-0003), "
            f"quindi fuori da entrambe le catene di impaginazione e senza colophon "
            f"(decisione aperta: PIANO-CHIUSURA-CATENA-EDITORIALE, lotto F4)"
        )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dir", help="valida solo questa cartella (relativa alla radice)")
    args = ap.parse_args()

    mods = module_dirs(args.dir)
    html_mods = html_module_dirs(args.dir)
    if not mods and not html_mods:
        print("✓ validate_standalone: nessun modulo da validare")
        return 0

    errors: list[str] = []
    warnings: list[str] = []
    for mod in html_mods:
        check_html_module(mod, errors, warnings)
    for mod in mods:
        check_required(mod, errors)
        check_crossrefs(mod, errors)
        check_pregen(mod, errors, warnings)
        check_banned(mod, errors)
        check_readaloud(mod, errors)
        check_counters(mod, errors)
        check_generators(mod, errors, warnings)

    for w in warnings:
        print(f"  ⚠ {w}")
    if errors:
        print(f"✗ validate_standalone: {len(errors)} violazioni")
        for e in errors:
            print(f"  - {e}")
        return 1

    n_files = sum(len(list(m.rglob("*.md"))) for m in mods)
    n_html = sum(len(list(m.glob("*.html"))) for m in html_mods)
    pezzi = []
    if mods:
        pezzi.append(f"{len(mods)} markdown ({n_files} file): struttura, riferimenti, "
                     f"schede e read-aloud ok")
    if html_mods:
        pezzi.append(f"{len(html_mods)} HTML ({n_html} pagine): titoli, link, ancore e id ok")
    print(
        f"✓ validate_standalone: " + " · ".join(pezzi)
        + (f" ({len(warnings)} warning)" if warnings else "")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
