#!/usr/bin/env python3
"""validate_corredo.py — il corredo della serata è completo, e i suoi PDF sono buoni.

Perché esiste. Il 2026-09-25 il DM ha chiesto che «genera il booklet» faccia
uscire da solo tutto quello che serve alla serata, riveduto con le regole in
vigore. Misurato quel giorno: **nessuna norma elencava il corredo**. Il booklet
del DM aveva la sua tecnica in nove passi (`rumblingstone-editoria` §2-bis), ma
il volume dei fogli da consegnare, gli echi per PG, le carte e i prompt delle
immagini li teneva insieme solo la memoria di chi li aveva scritti. La norma è
in `skills/rumblingstone-automation/SKILL.md`, «Il corredo della serata»; questo
script è la sua misura (ADR-0056: una norma senza misura non esiste).

Il corredo si dichiara in un file `*.corredo.json` accanto al booklet del DM
(contratto: `schemas/corredo_serata.schema.json`). Controlla, e boccia se:

1. **manca un pezzo**: un manifest, un file di echi, una carta, un handout, un
   file di prompt;
2. **un PG non ha i suoi echi**, o i suoi echi non stanno nel volume dei fogli;
3. **un foglio ✉ sta in un volume che non è quello dei giocatori**: il
   booklet del DM lo cita per titolo, non lo ristampa (ADR-0070);
4. **il volume dei fogli contiene un capitolo del DM**: è uno spoiler stampato;
5. **un'immagine dei prompt non c'è**, o non ha la sua riga nella tabella
   «Confronto immagine-scheda» del file dei prompt;
6. **un box read-aloud supera le 12 righe** in un capitolo che va in stampa,
   misurato con `misura_craft.box_read_aloud` sul testo senza lo storico
   (quello che si stampa, ADR-0069);
7. **lo stesso capitolo sta in due volumi** del corredo: una pagina si stampa
   una volta (ADR-0070);
8. con `--stampa`: **un volume non compila** (`validate_booklets`), oppure il
   PDF ha **righe di testo che si sovrappongono**, **testo a meno di 30 pt
   dal bordo del foglio** (`rumblingstone-editoria` §4, «Il controllo a
   vista») o **apparato di lavoro stampato** oltre il tetto dichiarato per quel
   volume in `scripts/apparato-residui.json` (ADR-0070).

Il punto 8 legge il PDF con PyMuPDF, che è fra le dipendenze di sviluppo
(`requirements-dev.txt`, D7 di CICLO-SESSIONE) e gira in CI. Senza, la misura
si **dichiara saltata** e non si finge fatta; con `--rigoroso` un salto è
rosso. La compilazione, invece, c'è sempre dove c'è `typst`.

Uso:
    python3 scripts/validate_corredo.py                    # ogni corredo del repo
    python3 scripts/validate_corredo.py C.corredo.json     # solo questo
    python3 scripts/validate_corredo.py C.corredo.json --stampa [--rigoroso]
    python3 scripts/validate_corredo.py C.corredo.json --pdf   # misura i PDF già fatti
    python3 scripts/validate_corredo.py --json

Exit code: 0 = corredo completo · 1 = almeno un pezzo mancante o difettoso ·
2 = uso errato (file inesistente).
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import misura_craft as mc  # noqa: E402
import validate_booklets as vb  # noqa: E402
from dmcore.testo import togli_storico  # noqa: E402

SCHEMA = ROOT / "scripts" / "schemas" / "corredo_serata.schema.json"
ESPORTATORE = ROOT / "scripts" / "export_booklet_typst.py"

#: Il margine del «controllo a vista» di `rumblingstone-editoria` §4: testo
#: più vicino di così al bordo del foglio è uscito dalla colonna.
MARGINE_PT = 30.0
#: Due righe si sovrappongono se l'intersezione è alta più di metà della riga
#: più bassa e larga più di 2 pt. Tarato sui tre volumi della serata ARC-07
#: (168 pagine, 0 rilievi) e su un PDF con due righe sovrapposte apposta.
QUOTA_ALTEZZA = 0.5
LARGHEZZA_MIN_PT = 2.0

IMG_ID = re.compile(r"<!--\s*img id=([\w-]+)")
ESTENSIONI = (".jpg", ".jpeg", ".png", ".webp")
CONFRONTO = re.compile(r"^#{2,4} .*[Cc]onfronto immagine-scheda.*$", re.M)


# ─────────────────────────────────────────────── i pezzi del corredo

def _rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def capitoli(manifest: Path) -> "list[tuple[Path, str]]":
    """(file risolto, tag) di ogni capitolo, più l'introduzione come `dm`."""
    man = json.loads(manifest.read_text(encoding="utf-8"))
    fuori = [((manifest.parent / c["file"]).resolve(), c.get("tag", "dm"))
             for c in man.get("chapters", []) if isinstance(c, dict) and "file" in c]
    if man.get("intro_md"):
        fuori.append(((manifest.parent / man["intro_md"]).resolve(), "dm"))
    return fuori


def immagine_di(id_img: str, cartella: Path) -> "Path | None":
    """Il file di un blocco `img`: col nome dell'id, o senza il prefisso
    `ritratto-` dentro `ritratti/` (la convenzione di ARC-07 e del Drappo)."""
    nomi = {id_img}
    if id_img.startswith("ritratto-"):
        nomi.add(id_img[len("ritratto-"):])
    for f in sorted(cartella.rglob("*")):
        if f.suffix.lower() in ESTENSIONI and f.stem in nomi:
            return f
    return None


def righe_del_confronto(testo: str) -> "str | None":
    """Il testo della sezione «Confronto immagine-scheda», fino al titolo dopo."""
    m = CONFRONTO.search(testo)
    if not m:
        return None
    livello = len(m.group(0)) - len(m.group(0).lstrip("#"))
    resto = testo[m.end():]
    fine = re.search(rf"^#{{1,{livello}}} ", resto, re.M)
    return resto[:fine.start()] if fine else resto


def controlla_immagini(prompt: Path) -> "list[str]":
    errori: "list[str]" = []
    testo = prompt.read_text(encoding="utf-8")
    ids = IMG_ID.findall(testo)
    if not ids:
        return [f"{_rel(prompt)}: nessun blocco «img id=…» — non è un file di prompt"]
    confronto = righe_del_confronto(testo)
    if confronto is None:
        errori.append(f"{_rel(prompt)}: manca la sezione «Confronto immagine-scheda» "
                      "(rumblingstone-art-direction §7-bis, passo 4)")
    for i in ids:
        if immagine_di(i, prompt.parent) is None:
            errori.append(f"{_rel(prompt)}: l'immagine «{i}» non c'è — generata e mai "
                          "esportata, o scartata senza sostituta")
        if confronto is not None and not re.search(rf"^\|.*`{re.escape(i)}`", confronto, re.M):
            errori.append(f"{_rel(prompt)}: «{i}» non ha la sua riga nel confronto "
                          "immagine-scheda")
    return errori


def box_troppo_lunghi(f: Path) -> "list[str]":
    """I box oltre il tetto, sul testo che va in stampa."""
    testo = togli_storico(f.read_text(encoding="utf-8"))
    fuori = []
    righe = testo.splitlines()
    for b in mc.box_read_aloud(testo):
        if len(b) > mc.TETTO_RIGHE:
            n = righe.index(b[0]) + 1 if b[0] in righe else 0
            fuori.append(f"{_rel(f)}: un box di {len(b)} righe (tetto {mc.TETTO_RIGHE}), "
                         f"quello che apre con «{b[0][:50].strip()}…» (~r.{n} senza storico)")
    return fuori


def controlla_corredo(cp: Path) -> "tuple[list[str], list[str]]":
    """(errori, avvisi) di un corredo, senza compilare niente."""
    errori: "list[str]" = []
    avvisi: "list[str]" = []
    rel = _rel(cp)
    try:
        dato = json.loads(cp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{rel}: JSON non valido — {e}"], []
    vb._controlla_oggetto(dato, json.loads(SCHEMA.read_text(encoding="utf-8")), rel, errori)
    if errori:
        return errori, avvisi
    base = cp.parent

    def esiste(chiave: str, percorso: str) -> "Path | None":
        p = (base / percorso).resolve()
        if not p.is_file():
            errori.append(f"{rel}: manca il pezzo «{chiave}» — {percorso}")
            return None
        return p

    dm = esiste("booklet_dm", dato["booklet_dm"])
    fogli = esiste("fogli_giocatori", dato["fogli_giocatori"])
    extra = [esiste("approfondimento", a) for a in dato.get("approfondimento", [])]
    manifest = [m for m in (dm, fogli, *extra) if m]

    for m in manifest:
        e, _ = vb.controlla_manifest(m, vb.carica_schema())
        errori += e
    if errori:
        return errori, avvisi

    nei_fogli = {f for f, _ in capitoli(fogli)} if fogli else set()
    if fogli:
        for f, tag in capitoli(fogli):
            if tag != "player":
                errori.append(f"{rel}: il volume dei fogli contiene un capitolo del DM "
                              f"({_rel(f)}, tag «{tag}»): è uno spoiler stampato")
    # I fogli ✉ stanno solo nel volume dei giocatori (ADR-0070): il booklet del
    # DM e i volumi di approfondimento li citano per titolo, non li ristampano.
    for m in (dm, *extra):
        if not m:
            continue
        for f, tag in capitoli(m):
            if tag == "player":
                errori.append(f"{rel}: {m.name} stampa il foglio ✉ {_rel(f)}: i fogli "
                              "stanno solo nel volume dei giocatori, qui si citano per titolo")

    for pg in dato["pg"]:
        eco = dato["echi"].get(pg)
        if not eco:
            errori.append(f"{rel}: {pg} non ha i suoi echi")
            continue
        p = esiste(f"echi di {pg}", eco)
        if p and fogli and p not in nei_fogli:
            errori.append(f"{rel}: gli echi di {pg} ({eco}) non sono nel volume dei fogli")
    for pg in sorted(set(dato["echi"]) - set(dato["pg"])):
        avvisi.append(f"{rel}: echi per «{pg}», che non è fra i PG della serata")

    for pezzo in dato["carte_e_handout"]:
        p = esiste("carte_e_handout", pezzo)
        if p and fogli and p not in nei_fogli:
            errori.append(f"{rel}: «{pezzo}» è nel corredo ma non nel volume dei fogli")

    for pr in dato["immagini"]["prompt"]:
        p = esiste("immagini.prompt", pr)
        if p:
            errori += controlla_immagini(p)

    # Una pagina si stampa una volta (ADR-0070): lo stesso capitolo in due
    # volumi dello stesso corredo va su carta due volte.
    dove_sta: "dict[Path, list[str]]" = {}
    for m in manifest:
        for f, _ in capitoli(m):
            dove_sta.setdefault(f, []).append(m.name)
    for f, volumi in sorted(dove_sta.items()):
        if len(volumi) > 1:
            errori.append(f"{rel}: {_rel(f)} si stampa {len(volumi)} volte "
                          f"({', '.join(volumi)}): una pagina va in un volume solo")

    visti: "set[Path]" = set()
    for m in manifest:
        for f, _ in capitoli(m):
            if f in visti or not f.is_file():
                continue
            visti.add(f)
            errori += box_troppo_lunghi(f)
    return errori, avvisi


# ─────────────────────────────────────────────── il PDF

def sovrapposizioni(righe: "list[tuple[tuple[float, float, float, float], str]]") -> "list[tuple[str, str]]":
    """Le coppie di righe di testo che si sovrappongono sulla stessa pagina.

    `righe` sono (x0, y0, x1, y1) e testo. Funzione pura: si prova senza PDF.
    """
    fuori = []
    for (a, ta), (b, tb) in itertools.combinations(righe, 2):
        larga = min(a[2], b[2]) - max(a[0], b[0])
        alta = min(a[3], b[3]) - max(a[1], b[1])
        if larga <= LARGHEZZA_MIN_PT or alta <= 0:
            continue
        if alta > QUOTA_ALTEZZA * min(a[3] - a[1], b[3] - b[1]):
            fuori.append((ta, tb))
    return fuori


def fuori_margine(righe, larghezza: float, altezza: float) -> "list[str]":
    """Le righe di testo a meno di `MARGINE_PT` dal bordo del foglio."""
    return [t for (x0, y0, x1, y1), t in righe
            if x0 < MARGINE_PT or y0 < MARGINE_PT
            or x1 > larghezza - MARGINE_PT or y1 > altezza - MARGINE_PT]


# ─────────────────────────────────────────────── l'apparato in stampa (ADR-0070)
#
# Le firme delle classi A (metadati del repo), B (storia sfuggita al marcatore)
# e D (rimandi interni), cercate nel testo che il PDF stampa davvero. Non si
# cercano nei sorgenti: la stessa riga può stamparsi in un volume e non in un
# altro (un rimando tradotto, un blocco tolto), e conta la carta.
#
# ⚠️ I falsi positivi sono dichiarati, non nascosti: un nome di file dentro la
# finzione, un «#1» che non è un rimando. Per questo ogni volume ha un tetto in
# `scripts/apparato-residui.json`, con il perché, come `RESIDUI` di
# `test_storico.py`; il bersaglio è zero.
FIRME_APPARATO = (
    ("A", "intestazione di lavorazione",
     r"MASTER DEFINITIVO|Sostituisce e fonde|FILE-FONTE|ASSORBITI DA QUESTO|standard AP"
     r"|a consolidamento"),
    ("A", "promemoria di sistema", r"MAI 5e|CD non DC"),
    ("A", "nome di file", r"\b[\w'.…-]+\.(?:md|json|ya?ml|py|typ)\b"),
    ("A", "percorso o comando del repo",
     r"_ARCHIVIO/|\bscripts/|\bpython3\b|\bplans/|\bBestiario/"),
    ("A", "sigla di file", r"\bARC\d\d-[A-Z]{3,}"),
    ("A", "decisione del repo", r"\b(?:canone|Ordine) D\d{1,2}\b|\(D\d{1,2}(?:/D\d{1,2})?\)"),
    ("B", "storia delle scelte", r"Correzione canone|prima diceva|su decisione del DM"),
    ("D", "rimando a un master",
     r"\bmaster\s*#\s*\d|\bDEF-\d\b|(?<![\w#])#[1-9] (?=Scena|§|Appendice|Atto)"),
)
_FIRME = [(c, n, re.compile(rx)) for c, n, rx in FIRME_APPARATO]
RESIDUI_APPARATO = ROOT / "scripts" / "apparato-residui.json"


def normalizza_pagina(testo: str) -> str:
    """Il testo di una pagina come lo legge chi la guarda: parole intere.

    Typst spezza le parole lunghe con un trattino morbido e i percorsi con uno
    spazio di larghezza zero; senza toglierli, «MA-/STER» e «_​ARCHIVIO/​» non
    si riconoscono.
    """
    testo = testo.replace("\u200b", "").replace("\u00ad\n", "").replace("\u00ad", "")
    return re.sub(r"\s+", " ", testo)


def rilievi_apparato(pagine: "list[str]") -> "list[tuple[int, str, str, str]]":
    """(pagina, classe, firma, estratto) per ogni apparato stampato. Pura.

    Due firme sullo stesso punto contano una volta.
    """
    fuori = []
    for n, grezzo in enumerate(pagine, 1):
        testo = normalizza_pagina(grezzo)
        prese: "list[tuple[int, int]]" = []
        for classe, nome, rx in _FIRME:
            for m in rx.finditer(testo):
                if any(a < m.end() and m.start() < b for a, b in prese):
                    continue
                prese.append((m.start(), m.end()))
                fuori.append((n, classe, nome, testo[max(0, m.start() - 30):m.end() + 30]))
    return fuori


def tetto_apparato(manifest: Path) -> "tuple[int, str]":
    """Il tetto dichiarato per questo volume (0 se non è dichiarato) e il perché."""
    if not RESIDUI_APPARATO.is_file():
        return 0, ""
    dati = json.loads(RESIDUI_APPARATO.read_text(encoding="utf-8")).get("volumi", {})
    voce = dati.get(_rel(manifest))
    return (voce["tetto"], voce.get("perche", "")) if voce else (0, "")


def controlla_apparato(manifest: Path, pagine: "list[str]") -> "list[str]":
    """Il volume sta sotto il suo tetto, e il tetto non è più alto del vero."""
    rilievi = rilievi_apparato(pagine)
    tetto, _ = tetto_apparato(manifest)
    nome = _rel(manifest)
    if len(rilievi) > tetto:
        primi = "; ".join(f"p.{p} {c} {f}: «{e.strip()}»" for p, c, f, e in rilievi[:6])
        return [f"{nome}: {len(rilievi)} rilievi d'apparato in stampa, tetto {tetto} "
                f"(ADR-0070) — {primi}"]
    if len(rilievi) < tetto:
        return [f"{nome}: {len(rilievi)} rilievi d'apparato e il tetto dice {tetto}: "
                "abbassalo in scripts/apparato-residui.json, il tetto si "
                "deriva e non si ricorda"]
    return []


def testo_del_pdf(pdf: Path) -> "list[str] | None":
    """Il testo di ogni pagina, o None se PyMuPDF non c'è."""
    try:
        import pymupdf  # noqa: PLC0415
    except ImportError:
        return None
    with pymupdf.open(pdf) as doc:
        return [pagina.get_text() for pagina in doc]


def misura_pdf(pdf: Path, manifest: "Path | None" = None) -> "tuple[list[str], str]":
    """(difetti, nota). La nota non è vuota quando la misura è saltata.

    Con il manifest misura anche l'apparato stampato contro il tetto del volume.
    """
    try:
        import pymupdf  # noqa: PLC0415
    except ImportError:
        return [], ("PyMuPDF assente: sovrapposizioni, margini e apparato NON "
                    "misurati (pip install -r requirements-dev.txt)")
    difetti = []
    if manifest is not None:
        difetti += controlla_apparato(manifest, testo_del_pdf(pdf) or [])
    with pymupdf.open(pdf) as doc:
        for n, pagina in enumerate(doc, 1):
            righe = []
            for blocco in pagina.get_text("dict")["blocks"]:
                for riga in blocco.get("lines", []):
                    t = "".join(s["text"] for s in riga["spans"]).strip()
                    # Il versale d'apertura è una lettera sola a più di 20 pt,
                    # e il riquadro del suo glifo scende sulle righe accanto per
                    # costruzione: non è una sovrapposizione (trovato sul
                    # volume del −1000, pagina 40, e guardato a vista).
                    if len(t) <= 1 and max((s["size"] for s in riga["spans"]), default=0) > 20:
                        continue
                    if t:
                        righe.append((tuple(riga["bbox"]), t))
            for ta, tb in sovrapposizioni(righe):
                difetti.append(f"{pdf.name} p.{n}: righe sovrapposte «{ta[:30]}» / «{tb[:30]}»")
            for t in fuori_margine(righe, pagina.rect.width, pagina.rect.height):
                difetti.append(f"{pdf.name} p.{n}: testo a meno di {MARGINE_PT:.0f} pt "
                               f"dal bordo «{t[:40]}»")
    return difetti, ""


def stampa(manifest: Path) -> "tuple[list[str], str]":
    """Compila il volume, lo misura, e toglie il PDF se prima non c'era."""
    pdf = manifest.parent / f"{manifest.stem.replace('.manifest', '')}-STAMPA.pdf"
    cera_prima = pdf.is_file()
    try:
        esito = subprocess.run([sys.executable, str(ESPORTATORE), str(manifest), "--all"],
                               capture_output=True, text=True, cwd=ROOT)
        if esito.returncode != 0 or not pdf.is_file():
            coda = (esito.stderr or esito.stdout).strip().splitlines()[-4:]
            return [f"{_rel(manifest)}: la stampa fallisce — " + " / ".join(coda)], ""
        return misura_pdf(pdf, manifest)
    finally:
        if not cera_prima:
            pdf.unlink(missing_ok=True)


def manifest_del_corredo(cp: Path) -> "list[Path]":
    dato = json.loads(cp.read_text(encoding="utf-8"))
    return [(cp.parent / m).resolve() for m in
            (dato["booklet_dm"], dato["fogli_giocatori"], *dato.get("approfondimento", []))]


def corredi_del_repo() -> "list[Path]":
    return sorted(p for p in ROOT.glob("**/*.corredo.json") if "/build/" not in p.as_posix())


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("corredo", nargs="*", help="i file *.corredo.json (default: tutti)")
    ap.add_argument("--stampa", action="store_true",
                    help="compila ogni volume con typst e misura il PDF")
    ap.add_argument("--pdf", action="store_true",
                    help="misura i PDF -STAMPA.pdf già compilati accanto ai manifest, "
                         "senza ricompilarli (è il passo finale di `dm.py corredo`)")
    ap.add_argument("--rigoroso", action="store_true",
                    help="con --stampa o --pdf: una misura saltata (typst o PyMuPDF assente) è rossa")
    ap.add_argument("--json", action="store_true", help="esito machine-readable su stdout")
    args = ap.parse_args(argv)

    elenco = [Path(c).resolve() for c in args.corredo] or corredi_del_repo()
    for c in elenco:
        if not c.is_file():
            print(f"✗ corredo non trovato: {c}", file=sys.stderr)
            return 2

    errori: "list[str]" = []
    avvisi: "list[str]" = []
    note: "list[str]" = []
    compilati = 0
    for c in elenco:
        e, a = controlla_corredo(c)
        errori += e
        avvisi += a
        if args.pdf and not e:
            for m in manifest_del_corredo(c):
                pdf = m.parent / f"{m.stem.replace('.manifest', '')}-STAMPA.pdf"
                if not pdf.is_file():
                    errori.append(f"{_rel(m)}: il PDF da stampa non c'è ({pdf.name})")
                    continue
                d, nota = misura_pdf(pdf, m)
                errori += d
                compilati += 1
                if nota and nota not in note:
                    note.append(nota)
        elif args.stampa and not e:
            if not shutil.which("typst"):
                note.append("typst assente: i volumi NON sono stati compilati")
                continue
            for m in manifest_del_corredo(c):
                d, nota = stampa(m)
                errori += d
                compilati += 1
                if nota and nota not in note:
                    note.append(nota)
    if args.rigoroso and note:
        errori += [f"misura saltata con --rigoroso: {n}" for n in note]

    if args.json:
        print(json.dumps({"corredi": len(elenco), "errori": errori, "avvisi": avvisi,
                          "compilati": compilati, "misure_saltate": note},
                         ensure_ascii=False, indent=2))
        return 1 if errori else 0
    for a in avvisi:
        print(f"  · {a}")
    for n in note:
        print(f"  ⚠ {n}", file=sys.stderr)
    for e in errori:
        print(f"  ✗ {e}", file=sys.stderr)
    if errori:
        print(f"✗ validate_corredo: {len(errori)} difetti in {len(elenco)} corredi",
              file=sys.stderr)
        return 1
    coda = f", {compilati} volumi compilati e misurati" if compilati else ""
    print(f"✓ validate_corredo: {len(elenco)} corredi completi{coda}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
