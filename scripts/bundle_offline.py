#!/usr/bin/env python3
"""bundle_offline.py — le wheel di requirements.txt in un zip per piattaforma, per stampare senza rete.

Sul modello dei bundle di gsamuele78/iemod-fetch (ADR-0113 §bundle, ADR-0116).
Da quando typst e l'imposizione arrivano da PyPI (il modulo `typst` e
`pdfimpose`), tutto ciò che serve per fare un volume da stampa è una wheel:
il bundle è quindi solo `pip download` più un zip riproducibile.

    python3 scripts/bundle_offline.py costruisci --uscita dist
    python3 scripts/bundle_offline.py costruisci --piattaforma linux-x64 --uscita dist
    python3 scripts/bundle_offline.py installa rumblingstone-offline-linux-x64-v1.2.0.zip

Dentro il zip: `ruote/*.whl`, `requirements.txt` e `BUNDLE.json`, che elenca
ogni file col suo sha256. `installa` verifica ogni wheel contro BUNDLE.json e
poi fa `pip install --no-index --find-links` sul requirements.txt del bundle:
nessuna rete. Il zip è riproducibile (nomi in ordine, data da
SOURCE_DATE_EPOCH, permessi fissi); il workflow Release lo mette in SHA256SUMS
e lo attesta con Sigstore.

Solo stdlib (più pip, per scaricare e installare).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REQUISITI = REPO / "requirements.txt"
MANIFEST = "BUNDLE.json"
PYTHON = "3.13"  # binari.PYTHON_MINIMO: le wheel cp313

#: Le etichette di piattaforma delle wheel (PEP 425), per `pip download --platform`.
PIATTAFORME = {
    "linux-x64": ["manylinux_2_28_x86_64", "manylinux_2_17_x86_64", "manylinux2014_x86_64"],
    "linux-arm64": ["manylinux_2_28_aarch64", "manylinux_2_17_aarch64", "manylinux2014_aarch64"],
    "macos-arm64": ["macosx_11_0_arm64", "macosx_12_0_arm64", "macosx_14_0_arm64"],
    "windows-x64": ["win_amd64"],
}


def nome_zip(piatt: str) -> str:
    return f"rumblingstone-offline-{piatt}.zip"


def scarica_ruote(piatt: str, cartella: Path, requisiti: Path = REQUISITI) -> None:
    """`pip download` delle wheel di `requisiti` per `piatt`, solo binarie."""
    cmd = [sys.executable, "-m", "pip", "download", "--quiet", "--only-binary=:all:",
           "--python-version", PYTHON, "--implementation", "cp", "-d", str(cartella),
           "-r", str(requisiti)]
    for etichetta in PIATTAFORME[piatt]:
        cmd += ["--platform", etichetta]
    subprocess.run(cmd, check=True)


def _data_zip() -> tuple[int, int, int, int, int, int]:
    epoch = int(os.environ.get("SOURCE_DATE_EPOCH", "315532800"))  # 1980-01-01
    return time.gmtime(max(epoch, 315532800))[:6]


def costruisci(piatt: str, ruote: Path, uscita: Path, requisiti: Path = REQUISITI) -> Path:
    """Scrive `rumblingstone-offline-<piatt>.zip` con le wheel di `ruote`."""
    file: dict[str, bytes] = {"requirements.txt": requisiti.read_bytes()}
    for w in sorted(ruote.glob("*.whl")):
        file[f"ruote/{w.name}"] = w.read_bytes()
    if len(file) == 1:
        raise ValueError(f"nessuna wheel in {ruote}")
    manifest = {
        "piattaforma": piatt,
        "python": PYTHON,
        "file": {n: hashlib.sha256(d).hexdigest() for n, d in sorted(file.items())},
    }
    file[MANIFEST] = (json.dumps(manifest, indent=1, sort_keys=True, ensure_ascii=False)
                      + "\n").encode()
    uscita.mkdir(parents=True, exist_ok=True)
    zp = uscita / nome_zip(piatt)
    radice = zp.stem
    data = _data_zip()
    with zipfile.ZipFile(zp, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for nome in sorted(file):
            info = zipfile.ZipInfo(f"{radice}/{nome}", date_time=data)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, file[nome], compresslevel=9)
    return zp


def estrai_verificato(zp: Path, cartella: Path) -> Path:
    """Estrae il bundle in `cartella` verificando ogni file contro BUNDLE.json.

    Ritorna il requirements.txt estratto. Alza ValueError al primo sha256 diverso.
    """
    with zipfile.ZipFile(zp) as z:
        nomi = z.namelist()
        manifest_n = next((n for n in nomi if n.endswith("/" + MANIFEST)), None)
        if manifest_n is None:
            raise ValueError(f"{zp.name}: manca {MANIFEST}")
        radice = manifest_n[: -len(MANIFEST)]
        attesi = json.loads(z.read(manifest_n))["file"]
        for rel, sha in attesi.items():
            n = radice + rel
            if n not in nomi:
                raise ValueError(f"{rel}: in {MANIFEST} ma non nel zip")
            dati = z.read(n)
            if hashlib.sha256(dati).hexdigest() != sha:
                raise ValueError(f"{rel}: sha256 diverso da {MANIFEST}")
            dest = cartella / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(dati)
    return cartella / "requirements.txt"


def installa(zp: Path) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        try:
            req = estrai_verificato(zp, Path(tmp))
        except ValueError as e:
            print(f"✗ {e}", file=sys.stderr)
            return 1
        r = subprocess.run([sys.executable, "-m", "pip", "install", "--no-index",
                            "--find-links", str(Path(tmp) / "ruote"), "-r", str(req)])
    print(f"{'✓' if r.returncode == 0 else '✗'} {zp.name}: pip uscito con {r.returncode}")
    return 0 if r.returncode == 0 else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = ap.add_subparsers(dest="azione", required=True)
    c = sub.add_parser("costruisci", help="pip download e zip, per piattaforma")
    c.add_argument("--piattaforma", action="append", choices=sorted(PIATTAFORME),
                   help="ripetibile; default: tutte")
    c.add_argument("--uscita", type=Path, default=REPO / "dist")
    i = sub.add_parser("installa", help="pip install --no-index dalle wheel del bundle")
    i.add_argument("bundle", type=Path)
    sub.add_parser("elenco", help="le piattaforme e le loro etichette di wheel")
    a = ap.parse_args(argv)
    if a.azione == "elenco":
        for p, tag in PIATTAFORME.items():
            print(f"{p:12} {' '.join(tag)}")
        return 0
    if a.azione == "installa":
        return installa(a.bundle)
    for piatt in a.piattaforma or sorted(PIATTAFORME):
        with tempfile.TemporaryDirectory() as tmp:
            scarica_ruote(piatt, Path(tmp))
            zp = costruisci(piatt, Path(tmp), a.uscita)
        print(f"✓ {zp.name} ({zp.stat().st_size // 1024} KiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
