#!/usr/bin/env python3
"""validate_bestiario.py — Gate CI per la libreria Bestiario/ (piano libreria, L0).

Fa rispettare lo standard della libreria di mostri/villain/PNG (T-D12):

  1. La struttura standard esiste (mostri/ villain/ png/ pregen-pcgen/ tokens/)
     e le locazioni legacy NON esistono più (Armate-UNITA-NUOVE, Monsters_Sheets,
     PNG/ a repo root).
  2. Ogni STATBLOCK (`*-crN*.md` in mostri|villain|png) rispetta il formato:
     - filename kebab-case minuscolo con CR (`nome-crN.md`, `05` = ½);
     - header obbligatori: **Faction**, **Role**, **Environment**, **CR**,
       **Source**, **Status**;
     - CR del filename coerente col CR dichiarato nell'header;
     - stato dichiarato nel titolo o nell'header ([ACCEPTED]/[INFERRED]/Status).
  3. Ogni DOSSIER (gli altri .md in villain|png) ha un titolo H1.
  4. `mostri/` contiene SOLO statblock (+ README*).
  5. `scripts/monster_catalog.yaml` è in sync con la libreria (rigenerazione
     in-memory riproduce il file committato) — chi tocca uno statblock e
     dimentica `python3 scripts/build_monster_catalog.py` rompe la CI.

Con `--rules` (usato in CI come **warning**, non gate) aggiunge controlli di
aderenza alle regole 3.5/campagna: (a) GS dichiarato vs benchmark PF1e
Monster-Statistics-by-CR (hp/AC entro tolleranza larga); (b) `**Status**:
inferred` ⇒ deve esserci un marcatore `[INFERRED]` nel corpo; (c) se il file
menziona un boost, deve avere una riga `Boost log:`.

Uso: python3 scripts/validate_bestiario.py [--rules] [--help]
Exit 0 = struttura ok (gli avvisi --rules NON fanno fallire); exit 1 = violazioni.
"""
import re
import sys
import json
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEST = ROOT / "Bestiario"

STATBLOCK_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
HAS_CR_RE = re.compile(r"-cr(\d+)")
REQUIRED_HEADERS = ["**Faction**", "**Role**", "**Environment**", "**CR**",
                    "**Source**", "**Status**"]
LEGACY_PATHS = [
    "00_Red Hand Of Doom/Armate-UNITA-NUOVE",
    "00_Red Hand Of Doom/Monsters_Sheets",
    "PNG",
]
SUBDIRS = ["mostri", "villain", "png", "pregen-pcgen", "tokens"]

errors: list[str] = []
warnings: list[str] = []


def err(msg: str):
    errors.append(msg)


def warn(msg: str):
    warnings.append(msg)


# PF1e Monster-Statistics-by-CR benchmark (semplificato: hp medio e AC media
# per CR, tolleranze larghe). Fonte: skills/pathfinder-1e-srd (monster-advancement).
# Solo per il warning di --rules: un GS palesemente fuori scala va rivisto.
#: Il benchmark PF1e per GS. Fino al 2026-09-23 era una tabella di fasce
#: scritta qui, senza fonte dichiarata, e diversa da quella di `dmcore`. Ora
#: le fasce si ricavano dalla Tabella 1–1 in `pf1e-statistiche-per-gs.yaml`
#: con la tolleranza scritta nello stesso file: un dato, un posto.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore.tabelle import TABELLA_1_1, TOLLERANZA_PER_GS  # noqa: E402


def banda(cr: float):
    """(pf minimo, pf massimo, CA minima, CA massima) per un GS, o None."""
    riga = TABELLA_1_1.get(int(cr)) if cr >= 1 else TABELLA_1_1.get(0.5)
    if not riga:
        return None
    t = TOLLERANZA_PER_GS
    return (riga["pf"] * t["pf_rapporto_min"], riga["pf"] * t["pf_rapporto_max"],
            riga["ca"] - t["ca_sotto"], riga["ca"] + t["ca_sopra"], riga["pf"], riga["ca"])


def filename_cr(name: str):
    m = HAS_CR_RE.search(name)
    if not m:
        return None
    raw = m.group(1)
    if raw.startswith("0") and len(raw) > 1:   # cr05 = CR 1/2, cr025 = CR 1/4
        return int(raw) / (10 ** (len(raw) - 1))
    return float(raw)


def header_cr(text: str):
    m = re.search(r"\*\*CR\*\*[:\s]*([\d]+(?:[.,]\d+)?(?:/\d+)?)", text)
    if not m:
        return None
    val = m.group(1).replace(",", ".")
    if "/" in val:
        num, den = val.split("/")
        return float(num) / float(den)
    return float(val)


def check_statblock(path: Path):
    rel = path.relative_to(ROOT)
    name = path.name
    if not STATBLOCK_RE.match(name):
        err(f"{rel}: filename non kebab-case minuscolo (`nome-crN.md`)")
    text = path.read_text(encoding="utf-8", errors="replace")
    for h in REQUIRED_HEADERS:
        if h not in text:
            err(f"{rel}: header obbligatorio mancante: {h}")
    f_cr, h_cr = filename_cr(name), header_cr(text)
    if f_cr is not None and h_cr is not None and abs(f_cr - h_cr) > 0.01:
        err(f"{rel}: CR filename ({f_cr:g}) ≠ CR header ({h_cr:g})")
    if h_cr is None:
        err(f"{rel}: CR non leggibile dall'header **CR**")
    first = text.splitlines()[0] if text.splitlines() else ""
    if not (re.search(r"\[(ACCEPTED|INFERRED)", first)
            or re.search(r"\*\*Status\*\*[:\s]*\S", text)):
        err(f"{rel}: stato non dichiarato ([ACCEPTED]/[INFERRED] nel titolo o **Status** valorizzato)")


def check_dossier(path: Path):
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"^#\s+\S", text, re.MULTILINE):
        err(f"{rel}: dossier senza titolo H1")


ARCHIVI = {"_ARCHIVIO", "Old"}


def in_archivio(path) -> bool:
    """Vero se il file sta in una cartella d'archivio.

    Gli archivi contengono **copie** di file vivi. Chi *indicizza* deve
    saltarle, o ogni copia diventa un record doppio: e' successo il 2026-09-12,
    quando dodici istantanee fecero passare il catalogo da 305 a 311 record e
    resero rosso questo gate con un doppione di «Battaglia Finale - Fase 0».
    ⚠️ La regola vale per chi indicizza, **non** per chi sorveglia: la
    decisione **D1** tiene apposta `_ARCHIVIO/` dentro il raggio di
    `validate_maps`, perche' li' lo scopo e' che nessun master sfugga.
    """
    return bool(ARCHIVI.intersection(path.parts))


def is_statblock(path: Path) -> bool:
    return bool(HAS_CR_RE.search(path.name.lower())) and path.suffix == ".md" \
        and path.name == path.name.lower()


CATALOG_IDS: dict = {}


#: 🔴 **I campi che il repo usa davvero.** Il blocco ```statblocco``` scrive
#: `pf:` e `ca:` in italiano — `gs`, `ca`, `pf` e `ts` sono presenti nel **98%**
#: dei 110 statblocchi veri. Le due regex che stavano qui cercavano `hp N` e
#: `ac N`: leggevano il **49%** e il **58%**, e il loro «zero avvisi» era meta'
#: libreria mai guardata.
#:
#: ⚠️ **Non leggevano spazzatura, e va detto**: sui 53 file dove entrambe le
#: forme comparivano il numero estratto coincideva **sempre** col `pf:`
#: canonico, 53 su 53. Il difetto era **copertura**, non correttezza.
#: Ventunesimo caso della famiglia «un criterio che non pesca si traveste da
#: repo pulito» — RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI §4.
PF_CAMPO = {
    "pf": re.compile(r"^pf:\s*(\d+)", re.M),
    "ca": re.compile(r"^ca:\s*(\d+)", re.M),
}
#: La forma vecchia resta come ripiego per i pochi file che non hanno il blocco.
PF_RIPIEGO = {
    "pf": re.compile(r"\bhp\s*(\d+)"),
    "ca": re.compile(r"\bac\s*(\d+)"),
}
CA_DETTAGLIO = re.compile(r"^ca-dettaglio:\s*(.+)$", re.M)
CA_VOCI = re.compile(r"(touch|contatto|flat-?footed|colto alla sprovvista)\s*(\d+)", re.I)


def valore(text: str, campo: str):
    """Il valore canonico, col ripiego sulla forma vecchia. Deterministico."""
    m = PF_CAMPO[campo].search(text)
    if m:
        return int(m.group(1))
    m = PF_RIPIEGO[campo].search(text.lower())
    return int(m.group(1)) if m else None


def check_rules(path: Path):
    """Controlli di aderenza alle regole (--rules, solo warning)."""
    rel = str(path.relative_to(ROOT))
    text = path.read_text(encoding="utf-8", errors="replace")
    low = text.lower()
    # I puntatori NON portano numeri per progetto (ADR-0021): i loro valori
    # stanno nel file d'arco, e cercarli qui darebbe avvisi su un'assenza voluta.
    if "[POINTER" in text or "[RIMANDO]" in text:
        return
    # (1) benchmark GS vs pf/CA (tolleranza larga: segnala solo fuori scala)
    cr = header_cr(text)
    b = banda(cr) if cr is not None else None
    if b:
        pf_min, pf_max, ca_min, ca_max, pf_t, ca_t = b
        hp = valore(text, "pf")
        if hp is not None and not (pf_min <= hp <= pf_max):
            warn(f"{rel}: pf {hp} fuori scala per GS {cr:g} (Tabella 1–1: {pf_t}, "
                 f"fascia {pf_min:.0f}-{pf_max:.0f})")
        ac = valore(text, "ca")
        if ac is not None and not (ca_min <= ac <= ca_max):
            warn(f"{rel}: CA {ac} fuori scala per GS {cr:g} (Tabella 1–1: {ca_t}, "
                 f"fascia {ca_min:.0f}-{ca_max:.0f})")
    # (1-bis) coerenza INTERNA della CA: in 3.5 la CA di contatto e quella da
    # colto alla sprovvista sono la CA piena meno alcuni bonus, quindi non
    # possono superarla. E' un'identita', non un benchmark: non ha tolleranza.
    ac = valore(text, "ca")
    d = CA_DETTAGLIO.search(text)
    if ac is not None and d:
        for etichetta, val in CA_VOCI.findall(d.group(1)):
            if int(val) > ac:
                warn(f"{rel}: CA {ac} ma «{etichetta} {val}» — in 3.5 contatto e "
                     "sprovvista tolgono bonus, non ne aggiungono")
    # (1-ter) `pf-dado` deve registrare i dadi vita. Il 2026-09-23 non lo
    # faceva in 46 statblocchi su 95: 26 portavano il danno di un'arma, 20 una
    # parte sola dei dadi. Corretti da conformita_statblocchi.py, che ora ne fa
    # un cancello; qui resta l'avviso con la ragione. Il controllo vive in
    # genera_attributi.py: una norma, un rilevatore.
    from genera_attributi import pf_dado_sospetto
    motivo = pf_dado_sospetto(text, cr)
    if motivo:
        warn(f"{rel}: {motivo} — `pf-dado` non registra i dadi vita")
    # (2) policy flag: Status inferred ⇒ deve esserci un marcatore [INFERRED]
    m_status = re.search(r"\*\*Status\*\*[:\s]*([a-z\-]+)", low)
    if m_status and m_status.group(1).startswith("inferred") and "[inferred" not in low:
        warn(f"{rel}: Status=inferred ma manca un marcatore [INFERRED] nel corpo")
    # (3) Boost log obbligatorio se il file dichiara un boost
    if re.search(r"\bboost(ato|ed|are)?\b", low) and "boost log" not in low:
        warn(f"{rel}: menziona un boost ma non ha una riga `Boost log:`")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Gate CI della libreria Bestiario/ (struttura, naming, CR, catalogo in sync).",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--rules", action="store_true",
                    help="controlli di regole PF1e (avvisi non bloccanti)")
    ap.add_argument("--json", action="store_true",
                    help="emette il report in JSON (opt-in) invece del testo")
    args = ap.parse_args(argv)
    do_rules = args.rules

    # 1. struttura + legacy
    if not BEST.is_dir():
        print("✗ validate_bestiario: cartella Bestiario/ assente", file=sys.stderr)
        return 1
    for sub in SUBDIRS:
        if not (BEST / sub).is_dir():
            err(f"Bestiario/{sub}/ mancante (struttura standard T-D12)")
    for legacy in LEGACY_PATHS:
        if (ROOT / legacy).exists():
            err(f"locazione legacy ancora presente: {legacy} (va spostata in Bestiario/)")

    # 2-4. statblock e dossier
    for sub in ("mostri", "villain", "png"):
        d = BEST / sub
        if not d.is_dir():
            continue
        for path in sorted(d.rglob("*.md")):
            if path.name.startswith("README") or in_archivio(path):
                continue
            if is_statblock(path):
                check_statblock(path)
                if do_rules:
                    check_rules(path)
            else:
                if sub == "mostri":
                    err(f"{path.relative_to(ROOT)}: in mostri/ sono ammessi solo statblock `-crN.md` (+ README)")
                check_dossier(path)

    # 5. catalogo in sync
    build = ROOT / "scripts" / "build_monster_catalog.py"
    cat = ROOT / "scripts" / "monster_catalog.yaml"
    if build.exists() and cat.exists():
        before = cat.read_bytes()
        r = subprocess.run([sys.executable, str(build)], capture_output=True)
        if r.returncode != 0:
            err("build_monster_catalog.py fallisce: " + r.stderr.decode()[-200:])
        else:
            after = cat.read_bytes()
            if before != after:
                import difflib
                diff = list(difflib.unified_diff(
                    before.decode("utf-8", "replace").splitlines(),
                    after.decode("utf-8", "replace").splitlines(),
                    "committato", "rigenerato", lineterm="", n=1))[:24]
                cat.write_bytes(before)  # ripristina per non sporcare il worktree
                err("scripts/monster_catalog.yaml NON in sync: rigenerare con "
                    "`python3 scripts/build_monster_catalog.py` e committare. "
                    "Prime differenze:\n      " + "\n      ".join(diff))

    n_stat = sum(1 for s in ("mostri", "villain", "png")
                 for p in (BEST / s).rglob("*.md")
                 if not p.name.startswith("README") and not in_archivio(p)
                 and is_statblock(p))

    if args.json:
        report = {
            "tool": "validate_bestiario",
            "ok": not errors,
            "statblocks": n_stat,
            "errors": errors,
            "warnings": warnings if do_rules else [],
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1 if errors else 0

    if do_rules and warnings:
        print(f"⚠ validate_bestiario --rules: {len(warnings)} avvisi (non bloccanti)", file=sys.stderr)
        for w in warnings:
            print("  ~", w, file=sys.stderr)

    if errors:
        print(f"✗ validate_bestiario: {len(errors)} violazioni", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        return 1
    extra = f"; {len(warnings)} avvisi --rules" if do_rules else ""
    print(f"✓ validate_bestiario: struttura ok, {n_stat} statblock validi, catalogo in sync{extra}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
