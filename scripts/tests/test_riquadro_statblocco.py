"""Il riquadro unico delle creature in stampa (ADR-0105).

I casi vengono dalla conversione di ARC-07: la scheda di Balvar nel volume,
con le note del Bestiario fra il blocco e le righe leggibili; il PG senza GS;
il paragrafo «I conti» che cita CA e pf senza essere una scheda.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import statblock as sb  # noqa: E402
import build_booklet_html as bh  # noqa: E402
import export_booklet_typst as ex  # noqa: E402
import misura_statblocchi_booklet as mis  # noqa: E402

BLOCCO = """```statblocco
nome: Xorn standard (2)
gs: 6
tipo: Esterno (Terra) Medio
ca: 24
pf: 52
pf-dado: 7d8+21
ts: Temp +8, Rifl +5, Vol +5
attributi: For 17 Des 10 Cos 17
attacchi:
  - Morso +10 (4d6+3)
```"""

LEGGIBILE = """**Difesa** **CA 24** · **pf 52** · TS Tempra +8

**Attacco** **Mischia** morso +10 (4d6+3)

**Capacità speciali**
- **Scavare**: 6 m.
  continua sulla riga dopo.

**Tattiche** Sotto 15 pf scavano via."""


class TestSezioni(unittest.TestCase):

    def test_legge_le_fasce_e_si_ferma_dopo(self):
        righe = (LEGGIBILE + "\n\nUn paragrafo di regia.").split("\n")
        sezioni, fine = sb.sezioni_leggibili(righe, 0)
        self.assertEqual([s.etichetta for s in sezioni],
                         ["Difesa", "Attacco", "Capacità speciali", "Tattiche"])
        self.assertEqual(sezioni[2].voci, ["**Scavare**: 6 m. continua sulla riga dopo."])
        self.assertEqual(righe[fine].strip() or righe[fine + 1].strip(), "Un paragrafo di regia.")

    def test_senza_sezione_non_consuma_niente(self):
        self.assertEqual(sb.sezioni_leggibili(["", "Testo."], 0), ([], 0))

    def test_accosta_porta_su_le_righe_leggibili(self):
        testo = BLOCCO + "\n\nNota del DM sui conti.\n\n" + LEGGIBILE + "\n"
        accostato = sb.accosta_parte_leggibile(testo).split("\n")
        chiusura = accostato.index("```", 1)
        self.assertTrue(accostato[chiusura + 1].startswith("**Difesa**"))
        self.assertIn("Nota del DM sui conti.", accostato[chiusura + 2:])

    def test_le_caratteristiche_con_parentesi_restano(self):
        self.assertEqual(sb.senza_caratteristiche("For 30 (36 in Ira), Des 10 · Talenti"),
                         "For 30 (36 in Ira), Des 10 · Talenti")
        self.assertEqual(sb.senza_caratteristiche("For 17, Des 10, Cos 17 · Talenti x"),
                         "For 17, Des 10, Cos 17 · Talenti x")
        self.assertEqual(sb.senza_caratteristiche(
            "For 12, Des 10, Cos 18, Int 13, Sag 20, con il +4 della Collana, Car 12"),
            "For 12, Des 10, Cos 18, Int 13, Sag 20, con il +4 della Collana, Car 12")
        self.assertEqual(sb.senza_caratteristiche(
            "For 34 (+12), Des 8 (−1), Cos 25 (+7), Int 10, Sag 15 (+2), Car 11 · BAB +22").strip(" ·"),
            "BAB +22")


class TestEtichettaGs(unittest.TestCase):

    def test_numero_testo_e_trattino(self):
        self.assertEqual(sb.etichetta_gs("12"), "GS 12")
        self.assertEqual(sb.etichetta_gs("~10"), "GS ~10")
        self.assertEqual(sb.etichetta_gs("PG di 13°"), "PG di 13°")
        self.assertEqual(sb.etichetta_gs("—"), "")


class TestLeTreUscite(unittest.TestCase):

    def test_html_ha_le_fasce(self):
        corpo = BLOCCO.split("\n", 1)[1].rsplit("\n", 1)[0]
        sezioni, _ = sb.sezioni_leggibili(LEGGIBILE.split("\n"), 0)
        out = bh.statblocco_html(corpo, "", sezioni)
        self.assertIn('class="statblocco"', out)
        self.assertIn("GS 6", out)
        for fascia in ("Difesa", "Attacco", "Capacità speciali", "Tattiche"):
            self.assertIn(fascia, out)

    def test_homebrewery_usa_il_riquadro_monster(self):
        out = bh.statblocchi_homebrewery(BLOCCO + "\n" + LEGGIBILE + "\n")
        self.assertIn("{{monster,frame", out)
        self.assertNotIn("```statblocco", out)

    def test_typst_chiama_il_riquadro_con_le_sezioni(self):
        out = ex.md_to_typ(BLOCCO + "\n" + LEGGIBILE + "\n")
        self.assertEqual(out.count("#statblocco("), 1)
        self.assertIn('"Difesa":', out)
        self.assertNotIn("Sotto 15 pf scavano via.\n\n", out.split("#statblocco(", 1)[0])


class TestLaMisura(unittest.TestCase):

    def test_riquadro_e_forme_libere(self):
        md = (BLOCCO + "\n" + LEGGIBILE + "\n\n"
              "**Orco** CA 15 · 20 pf · ascia +5 (1d12+3)\n\n"
              "```\nGOBLIN · CA 15 · PF 5 · TS Temp +2\n```\n")
        forme = [f for f, _ in mis.censisci(md)]
        self.assertEqual(forme, ["riquadro", "prosa", "griglia"])

    def test_i_conti_e_la_regia_non_contano(self):
        md = ("**I conti.** CA 10 − 1 + 15 = 24, 90 pf, schianto +18 (2d8+9).\n\n"
              "- Round 1: colpisce contro CA 18, 30 pf, +12 (2d6).\n")
        self.assertEqual(mis.censisci(md), [])


if __name__ == "__main__":
    unittest.main()
