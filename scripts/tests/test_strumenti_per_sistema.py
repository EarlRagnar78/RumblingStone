"""F4 di ADR-0112: gli strumenti usano le regole del sistema del file.

Tre cose da provare:

1. uno strumento scritto sulle tabelle 3.5 sa dire, per un sistema, quali
   regole gli mancano (`sistemi.regole_diverse`), e su un file 3.5 non salta
   niente;
2. il rapporto dei master conta i pf con le regole del sistema del file: in
   PF1e il primo dado di classe al massimo e i dadi dopo a mezza in su (card F4
   2), in 3.5 a mezza in giù;
3. un conto senza regola nel sistema non si fa, e il rapporto lo dice (card F4
   3). Con ADR-0119 le tre regole che mancavano in PF1e (lotta → BMC/DMC,
   scurovisione, corrompere l'acqua) vengono dal PRD: non si salta più niente,
   e la lotta 3.5 in PF1e «non si applica» (test_conformita_pf1e.py).

Le uscite 3.5 identiche le provano `impronta_creature --confronta` e
`impronte.py --confronta`, non questo file.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import conformita_statblocchi as C  # noqa: E402
from dmcore import sistemi as S  # noqa: E402

STRUMENTI = ("conformita_statblocchi", "derive_statblocks", "genera_attributi",
             "genera_creatura", "impronta_creature", "validate_bestiario")

LADRO = (
    "## Ladro\n\n```statblocco\nnome: Ladro\ngs: 3\ntipo: Umano ladro 4 · NM\nca: 14\n"
    "pf: {pf}\npf-dado: 4d8+4\nts: Tempra +2\nattributi: For 12 Des 18 Cos 12 Int 13 Sag 12 Car 10\n"
    "sensi: Percezione +8\n```\n**Difesa** **CA 14** · **pf {pf}** (4d8+4)\n"
)
ORCO = (
    "## Orco\n\n```statblocco\nnome: Orco\ngs: 1\ntipo: Orco guerriero 1\nca: 13\n"
    "pf: 6\npf-dado: 1d10+1\nts: Tempra +3\nattributi: For 17 Des 11 Cos 12 Int 7 Sag 8 Car 6\n"
    "sensi: Percezione −1\n```\n"
)
LOTTATORE = (
    "## Bruto\n\n**PF:** 15 (2d8+6)\n**CA:** 12 (+2 naturale)\n"
    "**Caratteristiche:** For 18 Des 10 Cos 17\n**Attacco Base:** +1\n**Lotta:** +99\n"
)


class LeRegoleCheMancano(unittest.TestCase):

    def test_ogni_strumento_ha_le_sue_capacita_nel_manifest(self):
        for s in STRUMENTI:
            with self.subTest(strumento=s):
                self.assertTrue(S.capacita_chieste(s))

    def test_sul_3_5_non_manca_niente(self):
        for s in STRUMENTI:
            with self.subTest(strumento=s):
                self.assertEqual(S.regole_diverse("dnd35", s), [])

    def test_in_pf1e_mancano_le_tabelle_di_costruzione(self):
        self.assertIn("creature.costruzione", S.regole_diverse("pf1e", "conformita_statblocchi"))
        self.assertIn("creature.costruzione", S.regole_diverse("pf1e", "derive_statblocks"))

    def test_bersagli_e_campi_sono_gli_stessi(self):
        # validate_bestiario chiede bersagli per GS e campi: il 3.5 li eredita
        # da PF1e e da d20, quindi una scheda PF1e si controlla uguale
        self.assertEqual(S.regole_diverse("pf1e", "validate_bestiario"), [])

    def test_uno_strumento_sconosciuto_non_chiede_niente(self):
        self.assertEqual(S.regole_diverse("pf1e", "non-esiste"), [])


class IPuntiFeritaDelSistema(unittest.TestCase):

    def test_pf1e_mezzi_in_su(self):
        # 8 + ⌈3 × 4,5⌉ + 4 = 26 (Sfregio del Drappo)
        self.assertEqual(C.conti_dei_recinti(LADRO.format(pf=26), "pf1e"), [])
        (x,) = C.conti_dei_recinti(LADRO.format(pf=25), "pf1e")
        self.assertEqual((x["campo"], x["scritto"]), ("pf", 25))

    def test_dnd35_mezzi_in_giu(self):
        # 8 + ⌊3 × 4,5⌋ + 4 = 25
        self.assertEqual(C.conti_dei_recinti(LADRO.format(pf=25), "dnd35"), [])
        (x,) = C.conti_dei_recinti(LADRO.format(pf=26), "dnd35")
        self.assertEqual((x["campo"], x["scritto"]), ("pf", 26))

    def test_il_predefinito_resta_il_3_5(self):
        self.assertEqual(C.conti_dei_recinti(LADRO.format(pf=26)),
                         C.conti_dei_recinti(LADRO.format(pf=26), "dnd35"))


class IContiSenzaRegola(unittest.TestCase):

    def test_la_scurovisione_pf1e_viene_dal_prd(self):
        (x,) = C.conti_dei_recinti(ORCO, "dnd35")
        self.assertEqual(x["campo"], "sensi")
        (y,) = C.conti_dei_recinti(ORCO, "pf1e")
        self.assertEqual((y["campo"], y["atteso"], y["conto"]), ("sensi", "scurovisione 18 m", "scurovisione"))

    def test_la_lotta_si_controlla_solo_in_3_5(self):
        blocchi = list(C._blocchi_del_master(LOTTATORE))
        self.assertEqual([x["campo"] for b in blocchi for x in C.conti_del_master(b, "dnd35")], ["Lotta"])
        self.assertEqual([x for b in blocchi for x in C.conti_del_master(b, "pf1e")], [])
        self.assertIn("lotta", C.regole_conformita("pf1e")["conti"]["non_applicabili"])

    def test_i_saltati_si_dicono(self):
        self.assertEqual(C.conti_saltati("dnd35"), {})
        # ADR-0119: in PF1e non manca più nessuna regola
        self.assertEqual(C.conti_saltati("pf1e"), {})

    def test_i_moduli_pf1e_entrano_nel_rapporto(self):
        pf1e = [p for p in C.master_di_default() if S.sistema_di(p) == "pf1e"]
        if not pf1e:
            self.skipTest("nessun modulo PF1e con statblocchi")
        self.assertEqual(C.saltati_master(pf1e), [])
        self.assertGreaterEqual(len(pf1e), 2)

    def test_il_cancello_dei_moduli_e_verde(self):
        # card F4 1 del 2026-11-08: «Sì, e blocca la CI»
        self.assertEqual(C.main(["--cancello-moduli"]), 0)

    def test_il_cancello_blocca_uno_scarto(self):
        vero = C.rapporto_master
        try:
            C.rapporto_master = lambda files: [{"file": "x.md", "riga": 1, "titolo": "X", "campo": "pf",
                                                "scritto": 34, "atteso": 35, "nota": "prova"}]
            self.assertEqual(C.main(["--cancello-moduli"]), 1)
        finally:
            C.rapporto_master = vero


if __name__ == "__main__":
    unittest.main()
