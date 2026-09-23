"""`derive_statblocks --apply-ts` scrive i TS **e le caratteristiche da cui vengono**.

🔴 **D11, deciso dal DM il 2026-09-23**: *«tienila, ma deve scrivere anche le
caratteristiche da cui deriva, perché non contraddica genera_attributi»*.

Il 2 settembre l'opzione ha scritto i TS di otto schede con una matrice sua
(For, Cos, Des in ordine fisso); poi `genera_attributi` ha messo accanto
caratteristiche **diverse**, e il razorfiend verde si è trovato con TS da Cos 13
e `attributi` con Cos 18, mentre la formula del DM diceva Cos 20.

Le prove sotto verificano le tre cose che rendono il blocco coerente:

1. i TS scritti tornano con le caratteristiche scritte, secondo un verificatore
   **indipendente** (`conformita_statblocchi`, che non condivide il conto);
2. `genera_attributi`, rileggendo il file finito, produce **le stesse**
   caratteristiche: il suo `--check` lo tratta come un blocco suo;
3. i TS della matrice non entrano nella scelta delle caratteristiche. La prima
   stesura li lasciava nel blocco provvisorio, il tetto dei TS li leggeva, e la
   Cos del sergente scendeva da 14 a 12 per far tornare un numero che nessuno
   aveva scelto.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import conformita_statblocchi as C  # noqa: E402
import derive_statblocks as D  # noqa: E402
import genera_attributi as GA  # noqa: E402
from dmcore.statblock import estrai  # noqa: E402

SCHEDA = """\
# Sergente di Prova
**Faction**: red-hand | **Role**: melee-heavy | **Environment**: any | **CR**: 3

Medium humanoid (hobgoblin), Fighter 3, LE. **hp 28**; **AC 17** (+1 Des, +4 giaco di maglia, \
+2 scudo pesante), touch 11, flat-footed 16. Vel 9 m.
**Mischia** spada lunga +6 (1d8+3).
"""


def scrivi(testo: str = SCHEDA) -> Path:
    """Quello che fa `main --apply-ts` su una scheda: deriva, legge, scrive."""
    f = Path(tempfile.mkdtemp()) / "sergente-prova-cr3.md"
    f.write_text(testo, encoding="utf-8")
    L = D.leggi_scheda(f)
    sb, _, manca = D.deriva(L)
    assert not manca, manca
    letto, _ = estrai(testo)
    for campo in ("ca", "pf", "ts", "gs", "tipo", "ca_dettaglio", "velocita", "iniziativa"):
        if getattr(letto, campo):
            setattr(sb, campo, getattr(letto, campo))
    f.write_text(D.con_attributi(f, sb, L), encoding="utf-8")
    return f


class TestLeCaratteristicheVengonoScritte(unittest.TestCase):
    def setUp(self):
        self.f = scrivi()
        self.t = self.f.read_text(encoding="utf-8")

    def test_il_blocco_porta_attributi_e_la_marca_di_genera_attributi(self):
        self.assertRegex(self.t, r"(?m)^attributi: For \d+ Des \d+ Cos \d+")
        self.assertIn(GA.MARCA, self.t)
        self.assertIn("derivati dalle tabelle: ts, attributi", self.t)

    def test_un_verificatore_indipendente_li_trova_coerenti(self):
        g = C.giudica(C.leggi(self.f))
        self.assertEqual(g["provenienza"], "generate")
        self.assertTrue(g["verificabile"])
        self.assertEqual(g["scarti"], {})
        self.assertEqual({k for k in g["esito"] if k in ("Temp", "Rifl", "Vol")},
                         {"Temp", "Rifl", "Vol"})

    def test_genera_attributi_li_riproduce_rileggendo_il_file(self):
        v, _ = GA.genera(self.f.name, "melee-heavy", 3.0, self.t)
        scritta = next(r for r in self.t.splitlines() if r.startswith("attributi:"))
        self.assertEqual(GA.riga_attributi(v), scritta)

    def test_i_ts_della_matrice_non_scelgono_le_caratteristiche(self):
        # la prova che morde: la prima stesura dava Cos 12 (tetto dai TS della
        # matrice, Temp +4); senza, la Cos e' quella dell'array e la Tempra la segue
        self.assertIn("Cos 14", self.t)
        self.assertRegex(self.t, r"(?m)^ts: Temp \+5,")
        self.assertNotIn("⚠ Des al più", self.t)


if __name__ == "__main__":
    unittest.main()
