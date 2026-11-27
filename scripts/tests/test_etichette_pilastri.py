"""Le etichette dei pilastri di stile restano nel sorgente e non si stampano.

Scelta di Jfs del 2026-11-19 (card del thread della prosa): «Read-aloud
(Andor lead)» e «(pilastro GoT)» servono a chi scrive e a `misura_craft`, al
tavolo sono rumore. Il filtro è `dmcore.testo.togli_etichette_pilastri`, che
`leggi_per_la_stampa` applica a ogni capitolo di ogni volume.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from dmcore.testo import _PILASTRO, togli_etichette_pilastri  # noqa: E402

ETICHETTA = re.compile(rf"\([^()\n]*\b(?:{_PILASTRO}\s+(?:lead|support)|pilastro\s+{_PILASTRO})\b[^()\n]*\)", re.I)


class TestFiltro(unittest.TestCase):
    def test_il_pilastro_vero_resta(self):
        testo = "Gli Xorn mangiano il pilastro di mithral (MAPPA T-2, G08)."
        self.assertEqual(togli_etichette_pilastri(testo), testo)

    def test_le_altre_parentesi_restano(self):
        testo = "Un chierico (support/buff) e un mago (blaster e support)."
        self.assertEqual(togli_etichette_pilastri(testo), testo)

    def test_due_volte_e_come_una(self):
        una = togli_etichette_pilastri("Read-aloud (LotR lead, Salvatore support, per Tordek) — la")
        self.assertEqual(una, "Read-aloud (per Tordek) — la")
        self.assertEqual(togli_etichette_pilastri(una), una)


class TestNelleStampe(unittest.TestCase):
    def test_nessun_volume_generato_le_stampa(self):
        """I `.hb.md` sono l'uscita della catena di stampa, tenuta allineata in CI."""
        trovate = {}
        for hb in sorted(REPO.rglob("*.hb.md")):
            if "_ARCHIVIO" in hb.parts or "build" in hb.relative_to(REPO).parts[:1]:
                continue
            n = len(ETICHETTA.findall(hb.read_text(encoding="utf-8")))
            if n:
                trovate[hb.relative_to(REPO).as_posix()] = n
        self.assertEqual(trovate, {})


if __name__ == "__main__":
    unittest.main()
