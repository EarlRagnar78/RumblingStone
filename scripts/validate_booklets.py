#!/usr/bin/env python3
"""validate_booklets.py — il gate dei booklet: manifest, immagini, e la stampa vera.

Perché esiste. I booklet li leggono **due catene** — `build_booklet_html.py`
(schermo/Homebrewery, ADR-0013) e `export_booklet_typst.py` (stampa, ADR-0020) —
e fino al 2026-08-22 nessuno verificava né che le due leggessero le stesse
chiavi né che il volume da stampa compilasse. Il risultato: due booklet della
campagna non avevano **mai** compilato, e tredici immagini del Palio uscivano
in stampa come testo (`!Stemma Oca`). Difetti così non si scoprono guardando il
codice: si scoprono compilando.

Cosa controlla, in ordine di quanto fa male se salta:

1. **il manifest** contro `schemas/booklet_manifest.schema.json` — chiavi note,
   tipi, valori ammessi. Una chiave scritta male è una funzione che sparisce in
   silenzio;
2. **i file esistono** — capitoli, copertina, introduzione;
3. **le immagini dei master esistono** — è il controllo che avrebbe fermato il
   Palio: un `![...](...)` che punta a un file assente diventa un buco;
4. **la parità fra le catene** — quali chiavi consuma ognuna, e quali restano
   inattive da una parte (avviso, non errore: `header` in stampa *deve* restare
   inattiva, perché lì la testatina segue il capitolo);
5. **la stampa** (`--stampa`, richiede il binario `typst`) — compila ogni
   manifest e verifica che il PDF esista, non sia un guscio vuoto e **abbia i
   segnalibri**. È il gate che in CI trasforma «compilava sul portatile del DM»
   in un fatto verificato.

Uso:
    python3 scripts/validate_booklets.py                 # tutti i manifest del repo
    python3 scripts/validate_booklets.py M.manifest.json # solo questo
    python3 scripts/validate_booklets.py --stampa        # + compila davvero
    python3 scripts/validate_booklets.py --json          # esito machine-readable

Dipendenze: stdlib. `--stampa` richiede il binario `typst` (Apache 2.0) e senza
di quello **salta** il controllo dichiarandolo, invece di fingere di averlo fatto.

Exit code: 0 = tutto verde · 1 = almeno un errore · 2 = uso errato.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "scripts" / "schemas" / "booklet_manifest.schema.json"
ESPORTATORE = ROOT / "scripts" / "export_booklet_typst.py"

# Chi consuma cosa. La fonte di verità è lo schema (campo `description`), qui
# c'è la lettura operativa: se una chiave non compare in nessuna delle due, è
# una chiave morta e va tolta dal manifest.
SOLO_HTML = {"header", "player_footer", "cover_tag", "out"}
SOLO_STAMPA = {"front_matter", "carta", "capolettera", "fregio"}

IMMAGINE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def carica_schema() -> dict:
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


def _tipo_ok(valore, atteso: str) -> bool:
    return {
        "string": isinstance(valore, str),
        "boolean": isinstance(valore, bool),
        "array": isinstance(valore, list),
        "object": isinstance(valore, dict),
    }.get(atteso, True)


def _controlla_oggetto(dato: dict, schema: dict, dove: str, errori: list[str]) -> None:
    """Il sottoinsieme di JSON Schema che questi manifest usano davvero.

    Niente libreria esterna: `required`, `additionalProperties`, `type`, `enum`
    e `anyOf` coprono per intero il contratto. Aggiungere una regola qui è
    meglio che aggiungere una dipendenza al repo.
    """
    for chiave in schema.get("required", []):
        if chiave not in dato:
            errori.append(f"{dove}: manca la chiave obbligatoria «{chiave}»")
    proprieta = schema.get("properties", {})
    if schema.get("additionalProperties") is False:
        for chiave in dato:
            if chiave not in proprieta:
                errori.append(f"{dove}: chiave sconosciuta «{chiave}» "
                              f"(nessuna delle due catene la legge: o è un refuso o va tolta)")
    for chiave, valore in dato.items():
        sotto = proprieta.get(chiave)
        if not sotto:
            continue
        if "type" in sotto and not _tipo_ok(valore, sotto["type"]):
            errori.append(f"{dove}.{chiave}: atteso {sotto['type']}, trovato {type(valore).__name__}")
            continue
        if "enum" in sotto and valore not in sotto["enum"]:
            errori.append(f"{dove}.{chiave}: valore «{valore}» non ammesso "
                          f"(ammessi: {', '.join(map(str, sotto['enum']))})")
        if sotto.get("type") == "array" and isinstance(valore, list):
            for i, voce in enumerate(valore):
                if isinstance(voce, dict) and isinstance(sotto.get("items"), dict):
                    _controlla_oggetto(voce, sotto["items"], f"{dove}.{chiave}[{i}]", errori)
        # Un oggetto annidato (`colophon`) va sotto contratto come tutto il resto:
        # senza questa riga un refuso fra le sue chiavi passerebbe in silenzio —
        # cioe' proprio il difetto che lo schema esiste per impedire.
        if sotto.get("type") == "object" and isinstance(valore, dict):
            _controlla_oggetto(valore, sotto, f"{dove}.{chiave}", errori)


def controlla_manifest(mp: Path, schema: dict) -> tuple[list[str], list[str]]:
    """(errori, avvisi) di un manifest: struttura, file, immagini, parità."""
    errori: list[str] = []
    avvisi: list[str] = []
    rel = mp.relative_to(ROOT) if ROOT in mp.parents else mp
    try:
        man = json.loads(mp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{rel}: JSON non valido — {e}"], []
    base = mp.parent

    _controlla_oggetto(man, schema, str(rel), errori)

    for chiave in ("cover_image", "intro_md", "fregio"):
        if man.get(chiave) and not (base / man[chiave]).resolve().is_file():
            errori.append(f"{rel}.{chiave}: file mancante «{man[chiave]}»")

    for i, cap in enumerate(man.get("chapters", [])):
        if not isinstance(cap, dict) or "file" not in cap:
            continue
        f = (base / cap["file"]).resolve()
        if not f.is_file():
            errori.append(f"{rel}.chapters[{i}]: master mancante «{cap['file']}»")
            continue
        # Le immagini dei master: il controllo che avrebbe fermato il Palio.
        for alt, src in IMMAGINE.findall(f.read_text(encoding="utf-8")):
            if re.match(r"^[a-z]+://", src):
                avvisi.append(f"{rel}: immagine remota in «{cap['file']}» ({src}): "
                              f"in stampa non entra")
                continue
            if not (f.parent / src).resolve().is_file():
                errori.append(f"{rel}: immagine mancante «{src}» "
                              f"(citata in {cap['file']}, alt «{alt}»)")

    inattive_stampa = sorted(set(man) & SOLO_HTML)
    if inattive_stampa:
        avvisi.append(f"{rel}: chiavi che valgono solo per la catena HTML "
                      f"({', '.join(inattive_stampa)}) — in stampa restano inattive")
    return errori, avvisi


def prova_stampa(mp: Path) -> list[str]:
    """Compila il volume e verifica che sia un volume: pagine e segnalibri.

    Il PDF esce accanto al manifest, dove l'esportatore lo mette sempre. Se non
    c'era prima, viene tolto dopo il controllo: un gate non lascia artefatti
    nell'albero di lavoro di chi lo esegue.
    """
    rel = mp.relative_to(ROOT) if ROOT in mp.parents else mp
    pdf = mp.parent / f"{mp.stem.replace('.manifest', '')}-STAMPA.pdf"
    cera_prima = pdf.is_file()
    try:
        esito = subprocess.run(
            [sys.executable, str(ESPORTATORE), str(mp), "--all"],
            capture_output=True, text=True, cwd=ROOT,
        )
        if esito.returncode != 0:
            coda = (esito.stderr or esito.stdout).strip().splitlines()[-6:]
            return [f"{rel}: la stampa fallisce — " + " / ".join(coda)]
        if not pdf.is_file():
            return [f"{rel}: la stampa dice di essere riuscita ma il PDF non c'è"]
        dati = pdf.read_bytes()
        problemi = []
        if len(dati) < 20_000:
            problemi.append(f"{rel}: PDF di {len(dati)} byte — è un guscio, non un volume")
        man = json.loads(mp.read_text(encoding="utf-8"))
        if man.get("front_matter", True) and b"/Outlines" not in dati:
            problemi.append(f"{rel}: PDF senza segnalibri — l'indice del volume è la "
                            f"ragione per cui esiste questa catena")
        return problemi
    finally:
        if not cera_prima:
            pdf.unlink(missing_ok=True)


def manifest_del_repo() -> list[Path]:
    fuori = []
    for p in sorted(ROOT.glob("**/*.manifest.json")):
        if p.name == "tools.manifest.json" or "/build/" in p.as_posix():
            continue
        fuori.append(p)
    return fuori


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("manifest", nargs="*", help="i manifest da controllare (default: tutti)")
    ap.add_argument("--stampa", action="store_true",
                    help="compila davvero ogni volume con typst e controlla i segnalibri")
    ap.add_argument("--spiega", action="store_true",
                    help="elenca per esteso gli avvisi di parità fra le due catene")
    ap.add_argument("--json", action="store_true", help="esito machine-readable su stdout")
    args = ap.parse_args()

    elenco = [Path(m).resolve() for m in args.manifest] or manifest_del_repo()
    for m in elenco:
        if not m.is_file():
            print(f"✗ manifest non trovato: {m}", file=sys.stderr)
            return 2
    schema = carica_schema()

    errori: list[str] = []
    avvisi: list[str] = []
    for m in elenco:
        e, a = controlla_manifest(m, schema)
        errori += e
        avvisi += a

    stampati = 0
    saltata = ""
    if args.stampa:
        binario = shutil.which("typst")
        if not binario:
            saltata = ("il binario «typst» non è nel PATH: controllo di stampa SALTATO "
                       "(vedi docs/guides/GUIDA-BOOKLET-E-PDF.md §4)")
        elif not errori:
            for m in elenco:
                errori += prova_stampa(m)
                stampati += 1
        else:
            saltata = "errori di manifest: la stampa non è stata provata"

    if args.json:
        print(json.dumps({
            "manifest": len(elenco), "errori": errori, "avvisi": avvisi,
            "stampati": stampati, "stampa_saltata": saltata,
        }, ensure_ascii=False, indent=2))
        return 1 if errori else 0

    if args.spiega:
        for a in avvisi:
            print(f"  · {a}")
    elif avvisi:
        print(f"  · {len(avvisi)} avvisi di parità fra le due catene (--spiega per l'elenco)")
    for e in errori:
        print(f"  ✗ {e}", file=sys.stderr)
    if saltata:
        print(f"  ⚠ {saltata}", file=sys.stderr)
    if errori:
        print(f"✗ validate_booklets: {len(errori)} errori su {len(elenco)} manifest",
              file=sys.stderr)
        return 1
    coda = f", {stampati} compilati davvero" if stampati else ""
    print(f"✓ validate_booklets: {len(elenco)} manifest{coda} — ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
