#!/usr/bin/env python3
"""provenienza_immagini.py — l'etichetta di provenienza nelle copie da impaginazione.

I master generati portano un manifesto C2PA firmato da chi li ha generati (Google,
OpenAI): dentro c'è la «sorgente digitale» IPTC, cioè la dichiarazione standard che
l'immagine è fatta da un modello. Le copie leggere di `web/`, quelle che finiscono
nei booklet, la perdevano: `build_image_derivatives` ricomprime e i metadati
restano indietro (ADR-0132).

Questo strumento legge la sorgente digitale dal manifesto del master e la scrive
nella copia come XMP, col campo `Iptc4xmpExt:DigitalSourceType` dello standard
IPTC Photo Metadata: è il campo che leggono Google, Meta e i lettori C2PA. La
copia **non si ricomprime**: si aggiunge un segmento al file JPEG e i pixel
restano identici.

Non indovina: una copia prende l'etichetta solo se il master ha il manifesto
firmato. Dove l'origine è scritta a mano in PROVENIENZA.txt, o non si sa, la
copia resta senza e il rapporto lo dice.

    python3 scripts/provenienza_immagini.py                 # rapporto su tutte le web/
    python3 scripts/provenienza_immagini.py CARTELLA --scrivi
    python3 scripts/provenienza_immagini.py --check         # cancello: esce 1 se manca

Dipendenze: stdlib + Pillow (solo per aprire i PNG dei master).
Exit code: 0 = ok · 1 = `--check` e un'etichetta manca o non torna.
"""
from __future__ import annotations

import argparse
import binascii
import hashlib
import json
import re
import struct
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent

#: il vocabolario IPTC della sorgente digitale (NewsCodes «digitalsourcetype»)
BASE = "http://cv.iptc.org/newscodes/digitalsourcetype/"
GENERATA = "trainedAlgorithmicMedia"
COMPOSTA = "compositeWithTrainedAlgorithmicMedia"

_XMP_TESTA = b"http://ns.adobe.com/xap/1.0/\x00"
_TERMINE = re.compile(rb"digitalsourcetype/([A-Za-z]+)", re.I)
_NEL_XMP = re.compile(r'Iptc4xmpExt:DigitalSourceType="' + re.escape(BASE) + r'([A-Za-z]+)"')
_C2PA = (b"c2pa", b"jumb")
_ESA = re.compile(r"[0-9a-fA-F]+")


class Voce(NamedTuple):
    copia: str
    master: str          # "" se il master non c'è
    firmata: bool        # il master ha un manifesto C2PA
    attesa: str          # il termine IPTC che la copia deve dichiarare, "" se nessuno
    scritta: str         # il termine che la copia dichiara oggi, "" se nessuno

    @property
    def a_posto(self) -> bool:
        return self.attesa == self.scritta


def _blocchi(master: Path) -> list[bytes]:
    """Il file, più i manifesti che un PNG tiene scritti in esadecimale.

    Gemini mette il manifesto C2PA in un blocco di testo del PNG («Raw profile
    type app11»), in esadecimale: cercarlo nei byte del file non lo trova.
    """
    dati = master.read_bytes()
    fuori = [dati]
    if master.suffix.lower() == ".png":
        try:
            from PIL import Image, PngImagePlugin
            PngImagePlugin.MAX_TEXT_CHUNK = 64 * 1024 * 1024
            with Image.open(master) as im:
                testi = [v for v in im.info.values() if isinstance(v, str) and len(v) > 64]
        except Exception:  # noqa: BLE001 — un master illeggibile non ha etichetta
            testi = []
        for t in testi:
            # «\napp11\n   <lunghezza>\n<esadecimale…>»: l'intestazione ha
            # cifre sue, quindi si prendono solo le righe lunghe di esadecimale
            esa = "".join(r for r in t.split() if len(r) > 16 and _ESA.fullmatch(r))
            try:
                fuori.append(binascii.unhexlify(esa[: len(esa) // 2 * 2]))
            except binascii.Error:
                pass
    return fuori


def sorgente_del_master(master: Path) -> tuple[bool, str]:
    """(ha il manifesto C2PA, termine IPTC da dichiarare) letti dal master."""
    firmata, termini = False, set()
    for b in _blocchi(master):
        if any(m in b for m in _C2PA):
            firmata = True
            # il manifesto è CBOR: dopo il termine viene la chiave successiva,
            # attaccata («…Mediajparameters»); si tiene il termine noto più lungo
            for t in _TERMINE.findall(b):
                t = t.decode()
                for noto in (COMPOSTA, GENERATA, "composite"):
                    if t.startswith(noto):
                        termini.add(noto)
                        break
    if not firmata or GENERATA not in termini and COMPOSTA not in termini:
        return firmata, ""
    return True, COMPOSTA if COMPOSTA in termini or "composite" in termini else GENERATA


def pacchetto_xmp(termine: str, master: Path) -> bytes:
    impronta = hashlib.sha256(master.read_bytes()).hexdigest()
    return (
        '<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>'
        '<x:xmpmeta xmlns:x="adobe:ns:meta/">'
        '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
        '<rdf:Description rdf:about=""'
        ' xmlns:Iptc4xmpExt="http://iptc.org/std/Iptc4xmpExt/2008-02-29/"'
        ' xmlns:dc="http://purl.org/dc/elements/1.1/"'
        f' Iptc4xmpExt:DigitalSourceType="{BASE}{termine}"'
        f' dc:source="{master.name} sha256:{impronta}"/>'
        "</rdf:RDF></x:xmpmeta>"
        '<?xpacket end="w"?>'
    ).encode("utf-8")


def _segmenti(jpeg: bytes):
    """(marcatore, inizio, fine) dei segmenti prima dei dati dell'immagine."""
    if jpeg[:2] != b"\xff\xd8":
        raise ValueError("non è un JPEG")
    i = 2
    while i + 4 <= len(jpeg) and jpeg[i] == 0xFF:
        m = jpeg[i + 1]
        if m == 0xDA or 0xD0 <= m <= 0xD9:
            break
        lung = struct.unpack(">H", jpeg[i + 2:i + 4])[0]
        yield m, i, i + 2 + lung
        i += 2 + lung


def leggi_etichetta(jpeg: bytes) -> str:
    """Il termine IPTC che il JPEG dichiara nel suo XMP, "" se non c'è."""
    for m, a, z in _segmenti(jpeg):
        if m == 0xE1 and jpeg[a + 4:a + 4 + len(_XMP_TESTA)] == _XMP_TESTA:
            trovato = _NEL_XMP.search(jpeg[a:z].decode("utf-8", "replace"))
            return trovato.group(1) if trovato else ""
    return ""


def etichetta_jpeg(jpeg: bytes, xmp: bytes) -> bytes:
    """Il JPEG con quel pacchetto XMP, senza toccare i dati dell'immagine.

    Toglie un XMP che c'era già e mette il nuovo dopo i segmenti APP0/APP1
    d'apertura (JFIF, Exif), dove lo standard XMP lo vuole.
    """
    corpo = _XMP_TESTA + xmp
    if len(corpo) + 2 > 0xFFFF:
        raise ValueError("pacchetto XMP troppo lungo per un segmento JPEG")
    nuovo = b"\xff\xe1" + struct.pack(">H", len(corpo) + 2) + corpo
    fuori, dove = bytearray(jpeg[:2]), 2
    resto = 2
    for m, a, z in _segmenti(jpeg):
        e_xmp = m == 0xE1 and jpeg[a + 4:a + 4 + len(_XMP_TESTA)] == _XMP_TESTA
        if not e_xmp:
            fuori += jpeg[a:z]
            if m == 0xE0 or m == 0xE1:
                dove = len(fuori)
        resto = z
    fuori[dove:dove] = nuovo
    return bytes(fuori) + jpeg[resto:]


def _master_di(copia: Path) -> Path | None:
    for est in (".png", ".webp", ".PNG", ".WEBP"):
        m = copia.parent.parent / (copia.stem + est)
        if m.is_file():
            return m
    return None


def esamina(cartella: Path) -> list[Voce]:
    """Una voce per ogni `web/*.jpg` della cartella dei master."""
    voci = []
    for copia in sorted((cartella / "web").glob("*.jpg")):
        master = _master_di(copia)
        firmata, attesa = sorgente_del_master(master) if master else (False, "")
        voci.append(Voce(str(copia.relative_to(ROOT)) if copia.is_relative_to(ROOT) else str(copia),
                         master.name if master else "", firmata, attesa,
                         leggi_etichetta(copia.read_bytes())))
    return voci


def scrivi(cartella: Path) -> int:
    """Mette l'etichetta attesa nelle copie che non l'hanno; quante ne ha toccate."""
    n = 0
    for copia in sorted((cartella / "web").glob("*.jpg")):
        master = _master_di(copia)
        if master is None:
            continue
        _, attesa = sorgente_del_master(master)
        dati = copia.read_bytes()
        if attesa and leggi_etichetta(dati) != attesa:
            copia.write_bytes(etichetta_jpeg(dati, pacchetto_xmp(attesa, master)))
            n += 1
    return n


def cartelle_web() -> list[Path]:
    """Le cartelle dei master che hanno una `web/` tracciata da git."""
    r = subprocess.run(["git", "ls-files", "-z", "--", "*/web/*.jpg"], cwd=ROOT,
                       capture_output=True, check=False)
    nomi = r.stdout.decode("utf-8", "replace").split("\0")
    return sorted({(ROOT / n).parent.parent for n in nomi if n})


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cartelle", nargs="*", help="cartelle dei master (default: tutte quelle con web/)")
    ap.add_argument("--scrivi", action="store_true", help="scrive l'etichetta nelle copie")
    ap.add_argument("--check", action="store_true", help="esce 1 se un'etichetta manca o non torna")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    cartelle = [Path(c).resolve() for c in args.cartelle] or cartelle_web()
    if args.scrivi:
        n = sum(scrivi(c) for c in cartelle)
        print(f"✓ provenienza_immagini: etichetta scritta in {n} copie")
    voci = [v for c in cartelle for v in esamina(c)]
    firmate = [v for v in voci if v.attesa]
    a_posto = [v for v in firmate if v.a_posto]
    storte = [v for v in voci if not v.a_posto]
    if args.json:
        print(json.dumps({"copie": len(voci), "master_firmati": len(firmate),
                          "etichettate": len(a_posto),
                          "senza_origine_firmata": len(voci) - len(firmate),
                          "voci": [v._asdict() for v in voci]}, ensure_ascii=False, indent=1))
    else:
        for v in storte:
            print(f"  ✗ {v.copia}: attesa «{v.attesa or 'nessuna'}», scritta «{v.scritta or 'nessuna'}»")
        print(f"{'✓' if not storte else '✗'} provenienza_immagini: {len(voci)} copie, "
              f"{len(firmate)} con master firmato C2PA, {len(a_posto)} con l'etichetta IPTC; "
              f"{len(voci) - len(firmate)} senza origine firmata (restano senza)")
    return 1 if args.check and storte else 0


if __name__ == "__main__":
    sys.exit(main())
