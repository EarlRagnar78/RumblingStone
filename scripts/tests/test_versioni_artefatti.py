"""Le pagine degli artefatti dicono la versione che la matrice registra (ADR-0071).

Il DM, il 2026-09-25: *«una validazione simile forse è già presente nello
storico, ma non c'è stato mai un versionamento, che credo sia la scelta
migliore per gestire questi artefatti complessi»*. Il difetto che l'aveva
reso necessario: la pagina a due gemme della Corona portava ancora i Doni
superati del 2026-09-12, e niente diceva quale delle quattro pagine HTML della
cartella fosse quella viva.

La regola: ogni pagina viva di un artefatto porta
`<meta name="versione-artefatto" content="<artefatto> · S<stadio> · r<rev> · <data>">`,
e la stessa stringa sta nella tabella marcata `<!-- versioni-artefatti -->` di
`PG/Artefatti/ARTEFATTI-MATRICE-VERSIONI.md`. Questo test fallisce se:

* una riga della tabella nomina una pagina che non esiste;
* la versione della pagina non è quella della riga;
* una pagina porta una versione che la tabella non registra (una pagina viva
  che il registro non conosce);
* una pagina archiviata porta ancora la meta (l'archivio non è vivo).

Solo libreria standard: gira sotto `unittest` e sotto `pytest`.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRICE = ROOT / "PG" / "Artefatti" / "ARTEFATTI-MATRICE-VERSIONI.md"
CARTELLA = ROOT / "PG" / "Artefatti" / "Artefatti-Pg"
MARKER = "<!-- versioni-artefatti -->"
META = re.compile(r'<meta name="versione-artefatto" content="([^"]+)">')
FORMA = re.compile(r"^[a-z]+ · S\d · r\d+ · \d{4}-\d{2}-\d{2}$")


def righe_registro(testo: str) -> "list[dict[str, str]]":
    """Le righe della tabella che segue il marker, fino alla prima riga vuota."""
    if MARKER not in testo:
        return []
    dopo = testo.split(MARKER, 1)[1].lstrip("\n").splitlines()
    righe = []
    for riga in dopo:
        if not riga.startswith("|"):
            break
        celle = [c.strip() for c in riga.strip().strip("|").split("|")]
        if not celle or celle[0].startswith("---") or celle[0] == "Artefatto":
            continue
        artefatto, stadio, giocatore, dm, versione = celle[:5]
        righe.append({"artefatto": artefatto, "stadio": stadio,
                      "giocatore": giocatore.strip("`"), "dm": dm.strip("`"),
                      "versione": versione.strip("`")})
    return righe


def pagine_con_meta() -> "dict[Path, str]":
    fuori = {}
    for p in CARTELLA.rglob("*.html"):
        m = META.search(p.read_text(encoding="utf-8", errors="replace"))
        if m:
            fuori[p] = m.group(1)
    return fuori


class TestVersioniArtefatti(unittest.TestCase):

    def setUp(self):
        self.righe = righe_registro(MATRICE.read_text(encoding="utf-8"))

    def test_il_registro_esiste(self):
        self.assertTrue(self.righe, f"manca la tabella dopo {MARKER} in {MATRICE.name}")

    def test_forma_della_versione(self):
        for r in self.righe:
            self.assertRegex(r["versione"], FORMA, r)

    def test_ogni_pagina_registrata_esiste_e_dice_la_sua_versione(self):
        for r in self.righe:
            for chiave in ("giocatore", "dm"):
                nome = r[chiave]
                if nome in ("—", "-", ""):
                    continue
                p = CARTELLA / nome
                self.assertTrue(p.exists(), f"{nome}: la matrice la registra, il file non c'è")
                m = META.search(p.read_text(encoding="utf-8"))
                self.assertIsNotNone(m, f"{nome}: manca la meta versione-artefatto")
                self.assertEqual(m.group(1), r["versione"], f"{nome}: versione diversa dalla matrice")

    def test_nessuna_pagina_viva_fuori_registro(self):
        registrate = set()
        for r in self.righe:
            for chiave in ("giocatore", "dm"):
                if r[chiave] not in ("—", "-", ""):
                    registrate.add((CARTELLA / r[chiave]).resolve())
        for p, versione in pagine_con_meta().items():
            if "_ARCHIVIO" in p.parts:
                self.fail(f"{p.relative_to(ROOT)}: pagina archiviata con la meta di una pagina viva")
            self.assertIn(p.resolve(), registrate,
                          f"{p.relative_to(ROOT)} porta {versione!r} ma la matrice non la registra")

    def test_il_parser_morde(self):
        """La tabella finta con una pagina inesistente deve dare una riga da controllare."""
        finto = f"x\n{MARKER}\n| Artefatto | Stadio | G | DM | Versione | Stato |\n|---|---|---|---|---|---|\n" \
                "| corona | 9 | `non/esiste.html` | — | `corona · S9 · r1 · 2026-01-01` | ⬜ |\n\nfine"
        righe = righe_registro(finto)
        self.assertEqual(len(righe), 1)
        self.assertFalse((CARTELLA / righe[0]["giocatore"]).exists())


if __name__ == "__main__":
    unittest.main()
