"""Ogni pagina viva di un artefatto porta la sua immagine dentro, e leggera (ADR-0072).

Il DM, il 2026-09-25: le schede vecchie avevano l'immagine incorporata
nell'HTML, e questo ne manteneva il flavour e il layout; le nuove la
collegavano o non l'avevano. Misurato quel giorno su `main`: su 36 pagine vive,
**22 senza immagine**, 12 con un file accanto che si perde appena la pagina
esce dalla sua cartella, 2 con l'immagine dentro. E le schede vecchie la
incorporavano a piena risoluzione: 1,1-2,7 MB a pagina.

Il test fallisce se una pagina viva del registro:

* collega un'immagine come file (`<img src="…">` che non è un `data:`);
* supera il tetto di peso;
* è nel JSON delle immagini ma non porta l'immagine marcata con la sua chiave;
* non ha immagine e non è fra le mancanti dichiarate, con la ragione.

Solo libreria standard: gira sotto `unittest` e sotto `pytest`, e non serve
Pillow (quello serve solo a chi rigenera).
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "PG" / "Artefatti"
PAGINE_DIR = BASE / "Artefatti-Pg"
CONFIG = BASE / "immagini-artefatti.json"
MATRICE = BASE / "ARTEFATTI-MATRICE-VERSIONI.md"
MARKER = "<!-- versioni-artefatti -->"
TETTO_KB = 300
RE_IMG = re.compile(r'<img\b[^>]*\bsrc="([^"]*)"')
RE_MARCATA = re.compile(r'<img [^>]*data-immagine-artefatto="([^"]+)"')


def pagine_vive() -> "list[Path]":
    dopo = MATRICE.read_text(encoding="utf-8").split(MARKER, 1)[1].lstrip("\n").splitlines()
    out = []
    for riga in dopo:
        if not riga.startswith("|"):
            break
        celle = [c.strip().strip("`") for c in riga.strip().strip("|").split("|")]
        if len(celle) < 5 or celle[0] == "Artefatto" or celle[0].startswith("---"):
            continue
        out += [PAGINE_DIR / c for c in celle[2:4] if c not in ("—", "-", "")]
    return out


def chiave(p: Path) -> str:
    return re.sub(r"(_DM)?\.html$", "", p.relative_to(PAGINE_DIR).as_posix())


class TestImmaginiArtefatti(unittest.TestCase):

    def setUp(self):
        self.cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.pagine = pagine_vive()

    def test_le_sorgenti_esistono(self):
        for k, info in self.cfg["immagini"].items():
            self.assertTrue((ROOT / info["file"]).exists(), f"{k}: manca {info['file']}")
        for pag, k in self.cfg["pagine"].items():
            self.assertIn(k, self.cfg["immagini"], f"{pag} chiede l'immagine «{k}», che non è dichiarata")

    def test_nessuna_immagine_collegata(self):
        for p in self.pagine:
            srcs = RE_IMG.findall(p.read_text(encoding="utf-8"))
            fuori = [s for s in srcs if not s.startswith("data:")]
            self.assertFalse(fuori, f"{p.relative_to(ROOT)} collega {fuori}: "
                                    "python3 scripts/incorpora_immagini_artefatti.py")

    def test_il_peso(self):
        for p in self.pagine:
            kb = p.stat().st_size // 1024
            self.assertLessEqual(kb, TETTO_KB, f"{p.relative_to(ROOT)} pesa {kb} KB")

    def test_ogni_pagina_ha_la_sua_immagine_o_la_ragione(self):
        for p in self.pagine:
            testo = p.read_text(encoding="utf-8")
            k = chiave(p)
            atteso = self.cfg["pagine"].get(k)
            if atteso:
                m = RE_MARCATA.search(testo)
                self.assertTrue(m and m.group(1) == atteso,
                                f"{p.relative_to(ROOT)}: manca l'immagine «{atteso}» incorporata")
            elif not RE_IMG.search(testo):
                self.assertIn(k, self.cfg["mancanti"],
                              f"{p.relative_to(ROOT)} non ha immagine e non è fra le mancanti dichiarate")

    def test_il_parser_morde(self):
        """Una pagina finta con un'immagine collegata deve essere vista."""
        finto = '<img class="x" src="collana.jpg" alt="">'
        self.assertEqual(RE_IMG.findall(finto), ["collana.jpg"])
        self.assertFalse(RE_IMG.findall(finto)[0].startswith("data:"))


if __name__ == "__main__":
    unittest.main()
