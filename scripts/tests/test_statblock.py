"""Il blocco statistiche: lettura, estrazione dalla prosa, e il gate del GS.

Il rischio vero di questo formato non è che non si legga: è che si legga
**male** e che un numero sbagliato finisca in un riquadro dall'aria autorevole.
Perciò qui si controlla soprattutto ciò che il lettore NON deve fare — dedurre,
completare, indovinare.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import extract_statblocks as E  # noqa: E402
from dmcore.statblock import StatblockError, estrai, leggi, rendi, togli_blocco  # noqa: E402

COMPATTO = """\
# Myconid Worker (operaio) [TRANSCRIBED]
**Faction**: aberration | **Role**: fodder | **CR**: 2 | **Status**: transcribed

Small plant, 4d8+16. **hp 34**; **AC 15** (+1 taglia, +4 naturale), touch 11, flat-footed 15. Vel 6 m. TS Temp +6, Rifl +1, Vol +2. BAB +3; Lotta +0.
**Mischia** schianto +5 (1d4+1). Scurovisione 18 m. Talenti: Allerta, Resistenza Fisica.
"""

INGLESE = """\
# Blue (Psionic Goblinoid) [ACCEPTED]
**Faction**: red-hand | **CR**: 1 | **Status**: inferred
**Size/Type**: Small humanoid | **HD**: 1d8+1 (5 HP)
**AC**: 15 (+1 size, +2 Dex, +2 leather) | **Init**: +2 | **Speed**: 30 ft
**Saves**: Fort +3, Ref +2, Will +0 | **BAB/Grapple**: +0/-4
"""


class TestLettura(unittest.TestCase):

    def test_giro_completo(self):
        sb, mancanti = estrai(COMPATTO)
        self.assertEqual(mancanti, [])
        riletto = leggi(rendi(sb))
        self.assertEqual((riletto.ca, riletto.pf, riletto.gs), ("15", "34", "2"))
        self.assertEqual(riletto.ts, "Temp +6, Rifl +1, Vol +2")

    def test_nessun_blocco_non_e_un_errore(self):
        self.assertIsNone(leggi("# scheda\n\nsolo prosa\n"))

    def test_blocco_rotto_solleva(self):
        for rotto in ("```statblocco\ngs: 2\n",                    # mai chiuso
                      "```statblocco\ngs: 2\nca: 15\npf: 3\nts: x\nqualcosa: 1\n```",  # campo ignoto
                      "```statblocco\ngs: 2\n```"):                # obbligatori mancanti
            with self.subTest(rotto=rotto[:40]):
                with self.assertRaises(StatblockError):
                    leggi(rotto)

    def test_togli_blocco(self):
        testo = "# t\n\n" + rendi(estrai(COMPATTO)[0]) + "\n\nprosa\n"
        self.assertNotIn("```statblocco", togli_blocco(testo))
        self.assertIn("prosa", togli_blocco(testo))


class TestEstrazione(unittest.TestCase):

    def test_i_dadi_vita_non_sono_i_dadi_di_danno(self):
        """`4d8+16` sono i DV; `1d4+1` è il danno dello schianto."""
        sb, _ = estrai(COMPATTO)
        self.assertEqual(sb.pf_dado, "4d8+16")

    def test_l_attacco_finisce_dove_finisce_la_frase(self):
        sb, _ = estrai(COMPATTO)
        self.assertEqual(sb.attacchi, ["Mischia schianto +5 (1d4+1)"])

    def test_dialetto_inglese(self):
        sb, mancanti = estrai(INGLESE)
        self.assertEqual(mancanti, [])
        self.assertEqual((sb.ca, sb.pf, sb.iniziativa, sb.velocita),
                         ("15", "5", "+2", "30 ft"))
        self.assertEqual(sb.ts, "Temp +3, Rifl +2, Vol +0")
        self.assertEqual(sb.ca_dettaglio, "(+1 size, +2 Dex, +2 leather)")   # niente | Init

    def test_niente_e_meglio_di_un_numero_inventato(self):
        sb, mancanti = estrai("# x\n\nUn mostro senza numeri.\n")
        self.assertIn("ca", mancanti)
        self.assertEqual(sb.ca, "")

    def test_il_gs_fuori_dalla_finestra_col_secondo_ramo(self):
        """🐛 «→ CR 12» in testa al dossier: il ripiego prendeva `group(1)`, che era None."""
        testo = (REPO / "Bestiario/villain/Sethrax_il_Velato/Sethrax.md").read_text(encoding="utf-8")
        sb, _ = estrai(togli_blocco(testo))
        self.assertEqual(sb.gs, "12")
        self.assertEqual(sb.ts, "Temp +5, Rifl +5, Vol +11")

    def test_mezzo_grado_di_sfida(self):
        sb, _ = estrai("**CR**: 1/2\n\nAC 12. hp 5. TS Temp +2, Rifl +0, Vol +0.")
        self.assertEqual(sb.gs, "1/2")


class TestGate(unittest.TestCase):

    def test_gs_del_blocco_contro_gs_del_nome(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "tizio-cr7.md"
            f.write_text("# t\n\n```statblocco\ngs: 5\nca: 18\npf: 60\nts: Temp +7, Rifl +4, Vol +5\n```\n",
                         encoding="utf-8")
            self.assertTrue(any("rimasto indietro" in p for p in E.controlla(f)))

    DOSSIER = ("# t\n\n```statblocco\ngs: 7\nca: 18\npf: 62\nts: {ts}\n```\n\n{nota}"
               "**Grado di Sfida (GS):** {gs}\n\n**Punti Ferita:** 62\n**CA:** 18\n"
               "- **Tempra:** +7 (+5 Base, +2 Cos)\n- **Riflessi:** +4 (+2 Base, +2 Des)\n"
               "- **Volontà:** +5 (+2 Base, +2 Sag, +1 talento)\n")

    def _problemi(self, **kw):
        campi = {"ts": "Temp +7, Rifl +4, Vol +5", "nota": "", "gs": "7"} | kw
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "lorana-cr7.md"
            f.write_text(self.DOSSIER.format(**campi), encoding="utf-8")
            return E.controlla(f)

    def test_il_blocco_rimasto_indietro_rispetto_alla_prosa(self):
        """La prova che morde: i TS derivati di Lorana contro quelli scritti dal DM."""
        self.assertEqual(self._problemi(), [])
        p = self._problemi(ts="Temp +6, Rifl +2, Vol +5")
        self.assertTrue(any("`ts` del blocco" in x for x in p), p)

    def test_una_marca_non_e_prosa(self):
        # 🐛 Ghaurush: «CA 23 → 25» sta in una marca, e il lettore la leggeva
        p = self._problemi(nota="> [INFERRED] correzione: CA 23 → **25**, pf 99.\n\n")
        self.assertEqual(p, [])

    def test_una_forbice_di_gs_non_si_confronta(self):
        # Il Collezionista: «GS 17-19» in prosa, 18 nel blocco per scelta
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "collezionista.md"
            f.write_text(self.DOSSIER.format(ts="Temp +7, Rifl +4, Vol +5", nota="", gs="6-8"),
                         encoding="utf-8")
            self.assertEqual(E.controlla(f), [])

    def test_un_altra_forma_non_e_la_prosa_del_blocco(self):
        # D7: il druido combatte in forma d'orso (il blocco) e ha una forma
        # umana con TS suoi, in una sezione a parte
        forma = "\n## Forma umana\n\n- **Tempra:** +3 (+1 Base)\n- **Riflessi:** +1\n- **Volontà:** +2\n"
        self.assertEqual(self._problemi(nota="", gs="7").__len__(), 0)
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "lorana-cr7.md"
            f.write_text(self.DOSSIER.format(ts="Temp +7, Rifl +4, Vol +5", nota="", gs="7") + forma,
                         encoding="utf-8")
            self.assertEqual(E.controlla(f), [])
            # la prova che morde: la stessa sezione senza intestazione di forma e' prosa
            f.write_text(self.DOSSIER.format(ts="Temp +3, Rifl +1, Vol +2", nota="", gs="7"),
                         encoding="utf-8")
            self.assertTrue(any("`ts` del blocco" in x for x in E.controlla(f)))

    def test_frazioni_equivalenti(self):
        self.assertEqual(E.gs_numerico("1/2"), E.gs_numerico("0.5"))
        self.assertEqual(E.gs_numerico("05"), 0.5)

    def test_inserimento_idempotente(self):
        sb, _ = estrai(COMPATTO)
        una = E.inserisci(COMPATTO, sb)
        self.assertEqual(una, E.inserisci(una, sb))
        self.assertEqual(una.count("```statblocco"), 1)
        # il blocco sta DOPO l'intestazione, non prima del titolo
        self.assertTrue(una.startswith("# Myconid"))


class TestBestiarioVero(unittest.TestCase):
    """Sul Bestiario committato: i blocchi già scritti devono restare validi."""

    def test_check_verde(self):
        problemi = [p for f in E.schede() for p in E.controlla(f)]
        self.assertEqual(problemi, [])

    def test_almeno_meta_libreria_migrata(self):
        conblocco = sum(1 for f in E.schede()
                        if "```statblocco" in f.read_text(encoding="utf-8"))
        self.assertGreaterEqual(conblocco, 80)


if __name__ == "__main__":
    unittest.main()
