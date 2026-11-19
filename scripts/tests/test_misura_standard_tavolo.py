"""misura_standard_tavolo: lo standard minimo del DM del 2026-11-02, misurato.

Il caso vero è la serata di *Notte e Alba*: Zog'tar ha la scheda d'entrata e
il ritratto nella Scena 7 di un capitolo, e il capitolo del barile, dove si
gioca, ne parla sessanta volte senza dire com'è né cosa vuole. Qui lo stesso
caso in piccolo, con un booklet finto di due capitoli.
"""
from __future__ import annotations

import doctest
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import misura_standard_tavolo as mst  # noqa: E402

CAP_COMPLETO = """# La tenda

### SCENA 7 — La tenda del comando

**Scheda d'entrata — Zog'tar Deatheye, il generale**

| | |
|---|---|
| **Chi è** | il generale dell'orda |
| **Aspetto** | mezzo-ogre in mithral annerito |
| **Vuole** | Hammerfist |

![Zog'tar Deatheye, il generale](Immagini/zogtar.jpg)

![M7-C](Mappe/rendered-stampa-pianta/m7c.svg)

```statblocco
nome: Zog'tar Deatheye, il generale
gs: 15
ca: 30
pf: 283
```
**Tattiche** *Durante il combattimento* Zog'tar carica.

Si tira l'iniziativa. Zog'tar ride.
"""

CAP_BARILE = """# Il barile

Il barile cade sulla tenda di Zog'tar. Zog'tar si sveglia.
Si tira l'iniziativa: Zog'tar grida.
"""


def booklet(tmp: Path, schede: str = "appendice") -> Path:
    (tmp / "a.md").write_text(CAP_COMPLETO, encoding="utf-8")
    (tmp / "b.md").write_text(CAP_BARILE, encoding="utf-8")
    man = {"title": "prova", "schede": schede, "chapters": [
        {"title": "I · La tenda", "file": "a.md", "tag": "dm"},
        {"title": "II · Il barile", "file": "b.md", "tag": "dm"},
        {"title": "III · Ai giocatori", "file": "b.md", "tag": "player"},
    ]}
    mp = tmp / "prova.manifest.json"
    mp.write_text(json.dumps(man), encoding="utf-8")
    return mp


class TestLoStandardMinimo(unittest.TestCase):

    def test_capitolo_completo_e_capitolo_vuoto(self):
        with TemporaryDirectory() as d:
            r = mst.misura_booklet(booklet(Path(d)), {"zogtar"})
        per_cap = {c["capitolo"]: c for c in r["coppie"]}
        self.assertEqual(set(per_cap), {"I · La tenda", "II · Il barile"})
        tenda, barile = per_cap["I · La tenda"], per_cap["II · Il barile"]
        self.assertTrue(tenda["completa"])
        self.assertEqual(tenda["num"], "rimando")       # le schede vanno in appendice
        self.assertFalse(barile["completa"])
        self.assertEqual(barile["presenti"], 0)

    def test_con_le_schede_nel_capitolo_i_numeri_sono_qui(self):
        with TemporaryDirectory() as d:
            r = mst.misura_booklet(booklet(Path(d), schede="qui"), {"zogtar"})
        self.assertEqual(r["coppie"][0]["num"], "qui")

    def test_la_mappa_si_cerca_nel_capitolo_dello_scontro(self):
        with TemporaryDirectory() as d:
            r = mst.misura_booklet(booklet(Path(d)), {"zogtar"})
        self.assertEqual({m["capitolo"]: m["mappa"] for m in r["mappe"]},
                         {"I · La tenda": "qui", "II · Il barile": "manca"})

    def test_sotto_soglia_non_compare(self):
        with TemporaryDirectory() as d:
            r = mst.misura_booklet(booklet(Path(d)), {"zogtar"}, soglia=10)
        self.assertEqual(r["coppie"], [])

    def test_doctest(self):
        self.assertEqual(doctest.testmod(mst).failed, 0)


class TestAdozioneAdr0107(unittest.TestCase):
    """ADR-0107 adottata il 2026-11-03 dove la misura migliora e niente
    peggiora (PDF prima e dopo, `misura_distanza_pagine.py`). Togliere il modo
    da uno di questi booklet è rosso; Terros resta fuori perché peggiora."""

    ADOTTATI = (
        "07_il Portale Della Forgia Eterna/homebrew/sessione-notte-e-alba/ARC07-NOTTE-E-ALBA-BOOKLET.manifest.json",
        "07_il Portale Della Forgia Eterna/homebrew/sessione-resurrezione-mille-anni/ARC07-SERATA-RESURREZIONE-BOOKLET.manifest.json",
        "07_il Portale Della Forgia Eterna/homebrew/volume-mille-anni/ARC07-MILLE-ANNI-VOLUME.manifest.json",
        "07_il Portale Della Forgia Eterna/homebrew/sessione-ritorno-forgia/ARC07-RITORNO-FORGIA-BOOKLET.manifest.json",
        "10-stand-alone/Il-Drappo-di-Tarsilia/homebrew/DRAPPO-BOOKLET-DM.manifest.json",
        "10-stand-alone/L'abbazia Della Rotta Sicura/homebrew/abbazia-rotta-sicura.manifest.json",
    )

    def test_i_booklet_adottati_tengono_il_modo(self):
        for rel in self.ADOTTATI:
            with self.subTest(rel=rel):
                man = json.loads((ROOT / rel).read_text(encoding="utf-8"))
                self.assertEqual(man.get("schede"), "entrambe")
                self.assertIs(man.get("chi_si_incontra"), True)


class TestNoteDiLavoro(unittest.TestCase):
    """Le note di lavoro che vanno in stampa («[INFERRED…]», «va riscontrato»): cricchetto.

    La lettura del DM del 2026-11-03 le ha trovate nel booklet della serata. Il
    bersaglio è zero; oggi si contano per volume, e una in più è rossa. Le tolgono
    le decisioni del DM nei master, non questo ramo.
    """

    TETTI = {
        "ARC07-NOTTE-E-ALBA-BOOKLET.manifest.json": 18,  # 19 prima della #305
        "ARC07-NOTTE-E-ALBA-SERATA.manifest.json": 1,    # la stessa del volume, Scena 11 (ADR-0122)
        "ARC07-SERATA-RESURREZIONE-BOOKLET.manifest.json": 19,
        "ARC07-MILLE-ANNI-VOLUME.manifest.json": 18,
        "ARC07-SESSIONE-TERROS-BOOKLET.manifest.json": 3,
        "giardino-sale-calce-pf1e.manifest.json": 1,
    }

    def test_la_nota_si_riconosce(self):
        testo = "CD 21 `[INFERRED — needs DM confirmation]`, va riscontrato su d20srd. CD 22."
        trovate = [m.group(0) for m in mst.NOTA_DI_LAVORO.finditer(testo)]
        self.assertEqual(len(trovate), 2)

    def test_il_cricchetto_dei_volumi(self):
        nomi = mst.persone_con_nome()
        for mp in mst.manifesti_dm():
            n = len(mst.misura_booklet(mp, nomi)["note_di_lavoro"])
            self.assertLessEqual(n, self.TETTI.get(mp.name, 0), f"{mp.name}: {n} note di lavoro in stampa")


if __name__ == "__main__":
    unittest.main()
