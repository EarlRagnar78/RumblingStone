"""Il ponte fra i rilevatori che esistono e il punteggio che li pesa.

🔴 **Il difetto, e perche' era invisibile per un mese.** Il DM, il 2026-09-21:
*«4 entrano nel punteggio [...] serve un rilevatore per tutte le norme»*. La
diagnosi era giusta e la causa era un'altra: `validate_prosa` misurava **sei**
di quelle norme da settembre. Non mancava il rilevatore — mancava il **nome**.
`controlla()` restituiva stringhe gia' formattate in italiano, e contarle per
norma avrebbe voluto dire riconoscere la frase con cui erano scritte.

La cura e' la forma di sempre per un misuratore: **una sola computazione, due
viste**. `rilievi()` produce record `(chiave, messaggio)`; `controlla()` ne
stampa i messaggi ed e' rimasta identica a se stessa, byte per byte, su tutto
il repo.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import misura_craft as mc  # noqa: E402
import punteggio_mqm as pm  # noqa: E402
import validate_prosa as vp  # noqa: E402

SPEC = pm.carica_specifiche()


class TestLeDueVisteNonDivergono(unittest.TestCase):
    """`controlla()` e' esattamente la proiezione di `rilievi()`."""

    def _campione(self) -> "list[Path]":
        # deterministico: i primi file di gioco in ordine alfabetico
        return sorted(vp.file_di_gioco())[:40]

    def test_controlla_e_la_proiezione_di_rilievi(self):
        for f in self._campione():
            self.assertEqual(vp.controlla(f), [m for _, m in vp.rilievi(f)], f)

    def test_ogni_rilievo_dichiara_una_chiave_nota(self):
        for f in self._campione():
            for chiave, _ in vp.rilievi(f):
                self.assertIn(chiave, vp.NORME, f"{f}: chiave «{chiave}» fuori elenco")

    def test_e_idempotente(self):
        """Due esecuzioni sullo stesso file danno la stessa lista, in ordine."""
        for f in self._campione()[:10]:
            self.assertEqual(vp.rilievi(f), vp.rilievi(f), f)


class TestIlPonteRegge(unittest.TestCase):
    def test_ogni_norma_della_specifica_ha_un_rilevatore_che_la_produce(self):
        """ADR-0053 applicato al ponte: una chiave pesata che nessun rilevatore
        emette varrebbe **zero per sempre**, cioe' sarebbe copertura finta."""
        prodotte = set()
        for f in sorted(vp.file_di_gioco())[:120]:
            testo = f.read_text(encoding="utf-8", errors="replace")
            for fn in pm.RILEVATORI:
                prodotte |= set(fn(testo, f))
        mancanti = set(SPEC["norme"]) - prodotte
        self.assertEqual(mancanti, set(), f"chiavi pesate che nessuno emette: {mancanti}")

    def test_i_rilevatori_non_emettono_chiavi_che_la_specifica_non_conosce(self):
        f = sorted(vp.file_di_gioco())[0]
        testo = f.read_text(encoding="utf-8", errors="replace")
        for fn in pm.RILEVATORI:
            for chiave in fn(testo, f):
                self.assertIn(chiave, SPEC["norme"],
                              f"{fn.__name__} emette «{chiave}», non pesata")

    def test_le_norme_pesate_sono_piu_delle_quattro_di_partenza(self):
        """Il numero non si congela — aggiungerne e' bene — ma scendere sotto
        le 11 del 2026-09-21 vorrebbe dire che qualcuno ha staccato il ponte."""
        self.assertGreaterEqual(len(SPEC["norme"]), 11, SPEC["norme"].keys())

    def test_non_e_piu_tutto_minore(self):
        """🔎 Il difetto che il DM ha nominato: tre norme su quattro erano
        `minore`, quindi il punteggio non poteva bocciare quasi niente."""
        pesi = [SPEC["severita"][n["severita"]]["peso"] for n in SPEC["norme"].values()]
        self.assertGreaterEqual(sum(1 for p in pesi if p >= 5), 3,
                                "il punteggio e' tornato a misurare solo il bordo")


class TestP1EntraNelPunteggio(unittest.TestCase):
    def test_il_rilevatore_p1_e_quello_vero(self):
        """Una norma, un rilevatore: il punteggio riusa `box_con_p1`, non una
        copia. Se riscrivesse la regex, i due numeri divergerebbero in silenzio."""
        f = ROOT / "07_il Portale Della Forgia Eterna" / "PortaleForgia-P1-REVISED-Corretta.md"
        testo = f.read_text(encoding="utf-8")
        self.assertEqual(pm._p1(testo, f)["read_aloud_presuppone"],
                         len(mc.box_con_p1(testo)))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
