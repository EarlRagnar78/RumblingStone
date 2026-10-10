#!/usr/bin/env python3
"""
asset_2mtt.py — installa e controlla i pacchetti di 2-Minute Tabletop per il
tema dipinto delle mappe (R4 di PIANO-RESA-E-ASSET-DELLE-MAPPE, D9).

Il download non si automatizza: anche i pacchetti gratuiti passano dalla cassa
del sito e i link arrivano per email, e la licenza chiede di mandare chi vuole i
file al sito invece di ridistribuirli. Il DM scarica lo zip; questo script fa
il resto:

    installa <zip> --categoria base|premium [--nome NOME]
        estrae in asset-esterni/2mtt/<nome>/ (ignorata da git) solo le immagini
        e i testi di licenza, rifiuta i percorsi assoluti, «..» e i link, e
        scrive pacchetto.json con categoria, impronta dello zip e dei file
    stato
        i pacchetti installati, con categoria e numero di file
    controlla
        la tabella committata scripts/asset-2mtt.json: ogni simbolo punta a un
        file che c'è, in un pacchetto di categoria «base». Senza pacchetti
        installati (la CI) controlla solo la forma della tabella

La categoria la dichiara il DM, perché decide la licenza (pagina «General
Licensing and Attribution» del sito, letta il 2026-10-09):

- **base**: i contenuti a offerta libera, anche a 0 $, sotto CC BY-NC 4.0. Si
  possono usare in un progetto gratuito con il credito su ogni pagina;
- **premium**: Patron Pack, pacchetti a pagamento come il «Plus», avventure e
  token. Nessuna licenza: solo al tavolo e in video. Nessuna mappa che esce
  dal repo li può contenere, e `controlla` boccia la tabella che li usa.

Libreria standard, nessuna rete. Exit: 0 ok · 1 difetto · 2 errore d'uso.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

RADICE = Path(__file__).resolve().parent
REPO = RADICE.parent
CARTELLA = REPO / "asset-esterni" / "2mtt"
TABELLA = RADICE / "asset-2mtt.json"

CATEGORIE = ("base", "premium")
IMMAGINI = {".png", ".webp", ".jpg", ".jpeg"}
TESTI = {".txt", ".pdf", ".md"}
TETTO_BYTE = 4 * 1024 ** 3  # uno zip che si espande oltre 4 GB non è un pacchetto di asset


def _impronta(dati: bytes) -> str:
    return hashlib.sha256(dati).hexdigest()


def _nome_valido(nome: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9][a-z0-9-]{1,60}", nome))


def _membri_sicuri(z: zipfile.ZipFile) -> tuple[list[zipfile.ZipInfo], list[str]]:
    """(i membri da estrarre, i motivi per cui altri sono stati rifiutati)."""
    tenuti, scarti = [], []
    totale = 0
    for info in z.infolist():
        if info.is_dir():
            continue
        p = PurePosixPath(info.filename.replace("\\", "/"))
        if p.is_absolute() or ".." in p.parts or re.match(r"^[A-Za-z]:", info.filename):
            raise ValueError(f"percorso pericoloso nello zip: {info.filename}")
        if stat.S_ISLNK(info.external_attr >> 16):
            raise ValueError(f"link simbolico nello zip: {info.filename}")
        if p.name.startswith(".") or "__MACOSX" in p.parts:
            continue
        estensione = p.suffix.lower()
        if estensione not in IMMAGINI | TESTI:
            scarti.append(info.filename)
            continue
        totale += info.file_size
        if totale > TETTO_BYTE:
            raise ValueError("lo zip si espande oltre 4 GB: non è un pacchetto di asset")
        tenuti.append(info)
    return tenuti, scarti


def installa(zip_path: Path, categoria: str, nome: str | None) -> int:
    if categoria not in CATEGORIE:
        print(f"✗ categoria: una di {', '.join(CATEGORIE)}", file=sys.stderr)
        return 2
    nome = nome or re.sub(r"[^a-z0-9]+", "-", zip_path.stem.lower()).strip("-")
    if not _nome_valido(nome):
        print(f"✗ nome «{nome}»: minuscole, cifre e trattini; passalo con --nome", file=sys.stderr)
        return 2
    try:
        z = zipfile.ZipFile(zip_path)
    except (OSError, zipfile.BadZipFile) as e:
        print(f"✗ {zip_path}: {e}", file=sys.stderr)
        return 1
    with z:
        try:
            membri, scarti = _membri_sicuri(z)
        except ValueError as e:
            print(f"✗ rifiutato: {e}", file=sys.stderr)
            return 1
        if not any(PurePosixPath(m.filename).suffix.lower() in IMMAGINI for m in membri):
            print("✗ nessuna immagine nello zip: non è un pacchetto di asset", file=sys.stderr)
            return 1
        dest = CARTELLA / nome
        dest.mkdir(parents=True, exist_ok=True)
        file = []
        for m in membri:
            dati = z.read(m)
            rel = PurePosixPath(m.filename.replace("\\", "/"))
            out = dest.joinpath(*rel.parts)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(dati)
            file.append({"file": rel.as_posix(), "byte": len(dati), "sha256": _impronta(dati)})
    pacchetto = {
        "nome": nome,
        "categoria": categoria,
        "licenza": ("CC BY-NC 4.0, credito su ogni pagina in cui compare la mappa"
                    if categoria == "base" else
                    "nessuna licenza: solo al tavolo e in video, mai in ciò che esce dal repo"),
        "credito": "Map made with assets by https://2minutetabletop.com/",
        "zip": zip_path.name,
        "zip_sha256": _impronta(zip_path.read_bytes()),
        "file": sorted(file, key=lambda f: f["file"]),
        "scartati": sorted(scarti),
    }
    (dest / "pacchetto.json").write_text(json.dumps(pacchetto, ensure_ascii=False, indent=1) + "\n",
                                         encoding="utf-8")
    immagini = sum(1 for f in file if PurePosixPath(f["file"]).suffix.lower() in IMMAGINI)
    print(f"✓ {nome} ({categoria}): {immagini} immagini in {dest.relative_to(REPO)}"
          + (f", {len(scarti)} file non immagine lasciati fuori" if scarti else ""))
    if categoria == "premium":
        print("  ⚠ premium: resta al tuo tavolo. Nessuna mappa che esce dal repo può usarlo")
    return 0


def pacchetti() -> dict[str, dict]:
    fuori = {}
    if CARTELLA.is_dir():
        for p in sorted(CARTELLA.glob("*/pacchetto.json")):
            dati = json.loads(p.read_text(encoding="utf-8"))
            fuori[dati["nome"]] = dati
    return fuori


def stato() -> int:
    installati = pacchetti()
    if not installati:
        print("○ 2-Minute Tabletop: nessun pacchetto installato (asset-esterni/2mtt/). "
              "Guida: docs/guides/GUIDA-MAPPE.md §5.2")
        return 0
    for nome, p in installati.items():
        print(f"✓ {nome}: {p['categoria']}, {len(p['file'])} file")
    return 0


def controlla() -> int:
    errori = []
    try:
        tabella = json.loads(TABELLA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"✗ {TABELLA.relative_to(REPO)}: {e}")
        return 1
    for campo in ("credito", "licenza", "simboli"):
        if campo not in tabella:
            errori.append(f"manca il campo «{campo}»")
    simboli = tabella.get("simboli", {})
    voci = []
    for sim, voce in simboli.items():
        if not (isinstance(voce, dict) and voce.get("pacchetto") and voce.get("file")):
            errori.append(f"{sim}: serve {{\"pacchetto\": …, \"file\": …}}")
            continue
        voci.append((sim, voce))
    installati = pacchetti()
    if installati:
        for sim, voce in voci:
            p = installati.get(voce["pacchetto"])
            if p is None:
                errori.append(f"{sim}: il pacchetto «{voce['pacchetto']}» non è installato")
            elif p["categoria"] != "base":
                errori.append(f"{sim}: «{voce['pacchetto']}» è premium, la licenza non lo ammette "
                              "in ciò che esce dal repo")
            elif voce["file"] not in {f["file"] for f in p["file"]}:
                errori.append(f"{sim}: «{voce['file']}» non è in «{voce['pacchetto']}»")
    for e in errori:
        print(f"✗ asset_2mtt: {e}")
    if not errori:
        dove = "sui pacchetti installati" if installati else "solo la forma: nessun pacchetto installato"
        print(f"✓ asset_2mtt: {len(voci)} simboli nella tabella ({dove})")
    return 1 if errori else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    sub = ap.add_subparsers(dest="azione", required=True)
    p = sub.add_parser("installa", help="estrae uno zip scaricato dal DM")
    p.add_argument("zip", type=Path)
    p.add_argument("--categoria", required=True, choices=CATEGORIE,
                   help="base = offerta libera, CC BY-NC · premium = a pagamento, solo al tavolo")
    p.add_argument("--nome", help="nome del pacchetto (default: dal nome dello zip)")
    sub.add_parser("stato", help="i pacchetti installati")
    sub.add_parser("controlla", help="la tabella simbolo → file contro i pacchetti e la licenza")
    args = ap.parse_args(argv)
    if args.azione == "installa":
        return installa(args.zip, args.categoria, args.nome)
    return stato() if args.azione == "stato" else controlla()


if __name__ == "__main__":
    sys.exit(main())
