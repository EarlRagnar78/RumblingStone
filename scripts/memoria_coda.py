#!/usr/bin/env python3
"""memoria_coda.py — il cancello della coda della memoria storica (ADR-0138).

ADR-0137 chiede a ogni thread una voce di memoria storica anche per il lavoro
che non finisce in una PR (scelta su card, dato verificato, file solo nella
cartella condivisa, thread che si risolve). La voce va in un file per thread
nella coda, fuori dal repo: `/mnt/project-files/memoria-storica-coda/`. Il DM,
il 2026-11-18: «aggiungi anche il cancello di verifica per il punto 3 per
superare dall'inizio il limite trovato». Questo script è quel cancello:

    python3 scripts/memoria_coda.py DIR --check
        la forma di tutte le voci in coda (esce 1 se una è scritta male)
    python3 scripts/memoria_coda.py DIR --thread "Titolo del thread"
        prima di risolvere un thread: esce 1 se non ha una voce, né in coda
        né già nel repo
    python3 scripts/memoria_coda.py DIR --threads elenco.json [--dal AAAA-MM-GG]
        la routine: i thread risolti dal giorno dato senza voce (esce 1)
    python3 scripts/memoria_coda.py DIR --piega [--data AAAA-MM-GG]
        porta nel repo le voci della coda non ancora presenti, numerandole
        dopo l'ultima, e controlla il file intero prima di scriverlo

Il file di un thread si chiama come il titolo, in minuscolo, senza accenti e
con i trattini: «Fissare lo standard del volume» → `fissare-lo-standard-del-volume.md`
(`--nome "Titolo"` lo stampa). Una voce in coda ha la testa `### MS-???? ·
data · titolo` e gli stessi campi obbligatori del file storico; piegandola
prende il numero e il campo `Coda`, così una seconda piega la salta e
`--thread` la ritrova anche dopo.

Cosa NON vede: la CI del repo non vede la coda né i thread, quindi questo
script lo lancia chi risolve un thread e la routine del lunedì. Non sa se una
card è stata chiusa dentro un thread ancora aperto, né se la voce dice tutto.

Solo stdlib, nessuna rete. Scrive solo con `--piega`.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import memoria_storica as ms  # noqa: E402

TESTA_CODA = re.compile(r"^### MS-\?{4} · (\S+) · (.+?)\s*$")
TESTA_QUALSIASI = re.compile(r"^### MS-")
DAL = "2026-11-18"      # il giorno in cui la regola è entrata nelle istruzioni del progetto
IGNORATI = {"LEGGIMI.md", "README.md"}


def nome_file(titolo: str) -> str:
    """Il nome del file di coda di un thread, senza estensione."""
    s = unicodedata.normalize("NFKD", titolo.casefold())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def leggi_coda(testo: str) -> "tuple[list[dict], list[str]]":
    """Le voci di un file di coda e i difetti di forma (senza il nome del file)."""
    voci, errori = [], []
    corrente = None
    for n, r in enumerate(testo.splitlines(), 1):
        if TESTA_QUALSIASI.match(r):
            m = TESTA_CODA.match(r)
            if not m:
                errori.append(f"riga {n}: testa «{r.strip()[:60]}» non è «### MS-???? · AAAA-MM-GG · titolo»")
                corrente = None
                continue
            corrente = {"data": m.group(1), "titolo": m.group(2), "riga": n, "campi": {}, "righe": []}
            voci.append(corrente)
            continue
        if corrente is None:
            continue
        corrente["righe"].append(r)
        c = ms.CAMPO.match(r)
        if c:
            corrente["campi"][c.group(1).strip()] = c.group(2).strip()
    for v in voci:
        dove = f"riga {v['riga']} «{v['titolo'][:40]}»"
        try:
            date.fromisoformat(v["data"])
        except ValueError:
            errori.append(f"{dove}: data «{v['data']}» non è AAAA-MM-GG")
        for c in ms.OBBLIGATORI:
            if c not in v["campi"]:
                errori.append(f"{dove}: manca il campo «{c}»")
        if v["campi"].get("Data") and v["campi"]["Data"] != v["data"]:
            errori.append(f"{dove}: il campo Data non è la data della testa")
        if "Testo" in v["campi"] and len(v["campi"]["Testo"]) < 40:
            errori.append(f"{dove}: Testo troppo corto per dire una decisione (meno di 40 caratteri)")
        pr, adr = v["campi"].get("PR", "—"), v["campi"].get("ADR", "—")
        if pr != "—" and not re.search(r"#\d+", pr):
            errori.append(f"{dove}: PR senza numeri #NNN (o «—»)")
        if adr != "—" and not re.search(r"ADR-\d{4}", adr):
            errori.append(f"{dove}: ADR senza numeri ADR-NNNN (o «—»)")
        if "Coda" in v["campi"]:
            errori.append(f"{dove}: il campo «Coda» lo scrive la piega, non il thread")
    return voci, errori


def file_di_coda(cartella: Path) -> "list[Path]":
    return [f for f in sorted(cartella.glob("*.md")) if f.name not in IGNORATI]


def controlla_coda(cartella: Path) -> "tuple[dict[str, list[dict]], list[str]]":
    """Tutte le voci per file (nome senza estensione) e tutti i difetti."""
    per_file, errori = {}, []
    for f in file_di_coda(cartella):
        if f.stem != nome_file(f.stem):
            errori.append(f"{f.name}: il nome non è nella forma dei titoli (atteso {nome_file(f.stem)}.md)")
        voci, e = leggi_coda(f.read_text(encoding="utf-8", errors="replace"))
        per_file[f.stem] = voci
        errori += [f"{f.name}: {x}" for x in e]
        if not voci and not e:
            errori.append(f"{f.name}: nessuna voce «### MS-???? · data · titolo»")
    return per_file, errori


def gia_nel_repo(storica: str) -> "tuple[set[tuple[str, str, str]], set[str]]":
    """(coda, data, titolo) delle voci piegate e i nomi di coda che hanno già una voce."""
    chiavi, nomi = set(), set()
    for v in ms.leggi(storica):
        c = v.campi.get("Coda", "").strip("` ")
        if c:
            chiavi.add((c, v.data, v.titolo))
            nomi.add(c)
    return chiavi, nomi


def thread_senza_voce(titoli: "list[str]", per_file: "dict[str, list[dict]]", nomi_repo: "set[str]") -> "list[str]":
    return [t for t in titoli if not per_file.get(nome_file(t)) and nome_file(t) not in nomi_repo]


def risolti(dati, dal: str) -> "list[str]":
    """I titoli dei thread risolti da `dal` in poi, da un elenco JSON.

    Accetta la forma di list_threads ({"sessions": [...]}) o una lista di
    oggetti con title, resolved e resolved_at.
    """
    righe = dati.get("sessions", dati.get("threads", [])) if isinstance(dati, dict) else dati
    fuori = []
    for r in righe:
        if r.get("resolved") and str(r.get("resolved_at", ""))[:10] >= dal and r.get("title"):
            fuori.append(r["title"])
    return fuori


def piega(per_file: "dict[str, list[dict]]", storica: str) -> "tuple[str, list[str]]":
    """Il file storico con le voci nuove in coda, e i loro id."""
    chiavi, _ = gia_nel_repo(storica)
    prossimo = max((v.numero for v in ms.leggi(storica)), default=0) + 1
    nuove = sorted(((v["data"], nome, v["riga"], v) for nome, voci in per_file.items() for v in voci
                    if (nome, v["data"], v["titolo"]) not in chiavi), key=lambda x: x[:3])
    testo, ids = storica.rstrip("\n") + "\n", []
    for _, nome, _, v in nuove:
        ident = f"MS-{prossimo:04d}"
        corpo = "\n".join(v["righe"]).strip("\n")
        testo += f"\n### {ident} · {v['data']} · {v['titolo']}\n\n{corpo}\n- **Coda:** `{nome}`\n"
        ids.append(ident)
        prossimo += 1
    return testo, ids


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cartella", nargs="?", type=Path, help="La cartella della coda, un file .md per thread.")
    ap.add_argument("--check", action="store_true", help="La forma di tutte le voci in coda: esce 1 se una è scritta male.")
    ap.add_argument("--thread", action="append", default=[], metavar="TITOLO",
                    help="Titolo di un thread che deve avere una voce (in coda o già piegata). Ripetibile.")
    ap.add_argument("--threads", type=Path, metavar="JSON",
                    help="Elenco dei thread (forma di list_threads): esce 1 se un thread risolto da --dal non ha voce.")
    ap.add_argument("--dal", default=DAL, help=f"Con --threads: solo i thread risolti da questo giorno (default {DAL}).")
    ap.add_argument("--piega", action="store_true",
                    help="Porta in plans/MEMORIA-STORICA.md le voci della coda non ancora presenti, numerate.")
    ap.add_argument("--nome", metavar="TITOLO", help="Stampa il nome del file di coda per un titolo ed esce.")
    ap.add_argument("--json", action="store_true", help="Uscita machine-readable.")
    ap.add_argument("--file", type=Path, default=ms.FILE, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)

    if a.nome:
        print(nome_file(a.nome) + ".md")
        return 0
    try:
        date.fromisoformat(a.dal)
    except ValueError:
        print(f"data non valida: {a.dal} (serve AAAA-MM-GG)", file=sys.stderr)
        return 2
    if a.cartella is None or not a.cartella.is_dir():
        print(f"manca la cartella della coda: {a.cartella}", file=sys.stderr)
        return 2
    if not a.file.is_file():
        print(f"manca {a.file}", file=sys.stderr)
        return 2
    storica = a.file.read_text(encoding="utf-8")
    per_file, errori = controlla_coda(a.cartella)
    _, nomi_repo = gia_nel_repo(storica)

    titoli = list(a.thread)
    if a.threads:
        try:
            titoli += risolti(json.loads(a.threads.read_text(encoding="utf-8")), a.dal)
        except (OSError, ValueError, AttributeError) as e:
            print(f"elenco dei thread illeggibile: {e}", file=sys.stderr)
            return 2
    mancano = thread_senza_voce(titoli, per_file, nomi_repo)

    piegate: "list[str]" = []
    if a.piega and not errori:
        nuovo, piegate = piega(per_file, storica)
        if piegate:
            difetti = ms.controlla(nuovo, None)
            if difetti:
                errori += [f"dopo la piega: {d}" for d in difetti]
                piegate = []
            else:
                a.file.write_text(nuovo, encoding="utf-8")

    voci_tot = sum(len(v) for v in per_file.values())
    if a.json:
        print(json.dumps({"file": len(per_file), "voci": voci_tot, "errori": errori,
                          "thread_controllati": titoli, "thread_senza_voce": mancano,
                          "piegate": piegate}, ensure_ascii=False, indent=1))
    else:
        for e in errori:
            print(f"✗ {e}")
        for t in mancano:
            print(f"✗ thread senza voce: «{t}» (atteso {a.cartella / (nome_file(t) + '.md')})")
        if a.piega and not errori:
            print(f"✓ piegate {len(piegate)} voci: {', '.join(piegate) or 'nessuna nuova'}")
        if not errori and not mancano:
            print(f"✓ coda della memoria storica: {len(per_file)} file, {voci_tot} voci in forma"
                  + (f", {len(titoli)} thread controllati" if titoli else ""))
    return 1 if errori or mancano else 0


if __name__ == "__main__":
    sys.exit(main())
