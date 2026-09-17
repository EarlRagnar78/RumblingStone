"""Il lotto H sul Bestiario: leggere prima di derivare, e non derivare mai alla cieca.

La lezione di H1, che questi test tengono ferma: **il debito non era dove
sembrava**. Delle 75 schede «da migrare», cinque non erano creature (un organo
collegiale, una popolazione di profughi, un aggregato di combattimento di massa,
due dossier che puntano altrove) e dieci avevano i numeri **già scritti**, in
dialetti che il lettore non conosceva — «hp ~30», «Punti Ferita: 60», «Grado di
Sfida (GS): 9», «TS +2/+9/+1».

Derivare sopra quei numeri avrebbe sostituito valori del DM con valori calcolati.
È il danno esatto che ADR-0021 teme, e questi test lo rendono impossibile.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from dmcore.statblock import estrai  # noqa: E402
import derive_statblocks as D  # noqa: E402
import extract_statblocks as E  # noqa: E402


class TestDialetti(unittest.TestCase):
    """Ogni dialetto qui sotto e' stato trovato in una scheda vera."""

    def _l(self, testo: str):
        return estrai(testo)[0]

    def test_tilde_approssimativa(self):
        # «hp ~30»: dieci schede risultavano senza numeri per una tilde.
        sb = self._l("Medium humanoid, Warrior 4. hp ~30 (4d8+8); AC ~16 (cotta).")
        self.assertEqual((sb.pf, sb.ca), ("30", "16"))

    def test_la_tilde_resta_dichiarata(self):
        # Trascrivere «hp ~30» come «pf: 30» promuove una stima a fatto.
        sb = self._l("hp ~30; AC ~16.")
        self.assertIn("approssimati", sb.fonte)

    def test_dialetto_italiano_esteso(self):
        sb = self._l("**Punti Ferita:** 60 (8d8 + 8 Cos)\n"
                     "**Classe Armatura:** 19\n"
                     "**Tiri Salvezza:** Tempra +7, Riflessi +10, Volontà +6 (+2 vs incantamento)")
        self.assertEqual((sb.pf, sb.ca), ("60", "19"))
        self.assertEqual(sb.ts, "Temp +7, Rifl +10, Vol +6")

    def test_gs_fra_parentesi(self):
        # «**Grado di Sfida (GS):** 9» — la parentesi rendeva invisibili 9 schede.
        self.assertEqual(self._l("**Grado di Sfida (GS):** 9").gs, "9")

    def test_ts_con_le_barre(self):
        self.assertEqual(self._l("PF 33; CA 16; TS +2/+9/+1;").ts,
                         "Temp +2, Rifl +9, Vol +1")

    def test_hp_in_parentesi_con_testo_dopo(self):
        sb = self._l("Large undead HD 16d12 (104 HP with skeleton template). AC 15.")
        self.assertEqual((sb.pf, sb.ca), ("104", "15"))


class TestNonCreature(unittest.TestCase):
    def test_il_marcatore_toglie_la_scheda_dal_debito(self):
        self.assertTrue(E.e_non_creatura("# Consiglio [NON-CREATURA]\n\ntesto"))
        self.assertFalse(E.e_non_creatura("# Un orco\n\ntesto"))

    def test_il_marcatore_vale_solo_in_testa(self):
        # In fondo a un file lungo non e' una dichiarazione: e' una menzione.
        self.assertFalse(E.e_non_creatura("# Titolo\n" + "\n" * 20 + "[NON-CREATURA]"))

    def test_su_una_non_creatura_non_si_scrive_mai_un_blocco(self):
        testo = "# Consiglio [NON-CREATURA]\n\nSette seggi."
        self.assertEqual(E.inserisci(testo, None), testo)

    def test_quali_schede_del_bestiario_sono_marcate(self):
        """L'elenco e' chiuso di proposito: il marcatore toglie schede dal conto
        del debito, e un elenco aperto sarebbe il modo per farlo sparire invece
        che estinguerlo. Aggiungerne una e' una riga qui **e** una scelta.

        La sesta e' arrivata chiudendo il lotto I: «Duergar della Scala di
        Ossa» non e' una creatura ma un **set d'incontro** di quattro PNG
        nominati, e il suo «GS 11» e' il livello dell'incontro.

        La settima e' del 2026-09-17: `Zhentarim_Dauth.md` e' il **dossier di
        una fazione** — chi sono gli Zhentarim a Dauth, cosa vogliono dal
        mercato nero extraplanare, e perche' la Mano Rossa minaccia anche loro.
        Non ha statistiche perche' non e' nessuno in particolare: le schede dei
        suoi membri stanno negli statblocchi d'arco, e ognuna dichiara
        `**Faction**: zhentarim`.

        L'ottava e' dello stesso giorno, e nasce da una riga di canone del DM:
        `Zalkatar.md` e' il **dossier del conclave della Torre Invisibile**.
        Zalkatar una scheda ce l'ha — GS 13, nell'arco P2A — ma questo file non
        la duplica: registra che **lui e' «il Padrone delle Menti»** del
        laboratorio di ARC-04, e quindi il compratore degli schiavi drow di
        Sonjak, l'innestatore delle Yochlol half-illithid che uccidono Hella, e
        il proprietario della stanza in cui l'Anello di Artemis si e' risvegliato.
        E' un dossier di fazione, non una creatura: le sue creature dichiarano
        `**Faction**: illithid-zalkatar`.
        """
        attese = {"Consiglio_Rethmar.md", "Profughi_Guado_di_Drellin.md",
                  "ondata-giganti-fanteria-cr15.md", "Witchwood_e_Tiri_Kitor.md",
                  "Secondo_Anello_Rethmar.md", "duergar-scala-di-ossa-cr11.md",
                  "Zhentarim_Dauth.md", "Zalkatar.md"}
        trovate = {f.name for f in (REPO / "Bestiario").rglob("*.md")
                   if E.e_non_creatura(f.read_text(encoding="utf-8"))}
        self.assertEqual(attese, trovate)

    def test_i_rimandi_puntano_tutti_a_qualcosa_che_esiste(self):
        """Il marcatore [RIMANDO] e' l'altro modo di togliere una scheda dal
        conto, ed e' quello piu' facile da abusare: basta dire «i numeri stanno
        altrove» e nessuno controlla. Qui si controlla."""
        rimandi = [f for f in (REPO / "Bestiario").rglob("*.md")
                   if E.e_rimando(f.read_text(encoding="utf-8"))]
        self.assertGreater(len(rimandi), 20, "il lotto I ne ha marcate 27")
        for f in rimandi:
            with self.subTest(scheda=f.name):
                guasto = E.rimando_valido(f, f.read_text(encoding="utf-8"))
                self.assertIsNone(guasto, guasto)

    def test_il_debito_del_bestiario_e_chiuso(self):
        """157 su 157 **sistemate**: col blocco, coi numeri altrove, o non
        creature. Non «migrate»: sistemate. La differenza e' il lotto I."""
        schede = E.schede()
        aperte = []
        for f in schede:
            testo = f.read_text(encoding="utf-8")
            if (E.APERTURA in testo or E.e_non_creatura(testo)
                    or E.e_rimando(testo)):
                continue
            aperte.append(f.name)
        self.assertEqual(aperte, [], f"schede ancora aperte: {aperte}")


class TestDerivazione(unittest.TestCase):
    def test_non_esiste_un_apply_generico(self):
        # Si scrive SOLO con `--apply-ts`, e solo i TS. Un `--apply` che scriva
        # CA e pf non deve esistere: quelli dipendono da equipaggiamento e
        # Costituzione, che da una scheda in prosa non si leggono.
        import contextlib, io
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            D.main(["--apply"])

    def test_senza_tipo_ne_classe_non_si_deriva(self):
        L = D.Lettura(nome="x", gs=5, dv=4, dado=8, tipo=None)
        sb, _, manca = D.deriva(L)
        self.assertIsNone(sb)
        self.assertTrue(any("tipo" in m for m in manca), manca)

    def test_senza_gs_la_proposta_esce_ma_senza_collaudo(self):
        # La guardia **annota**, non sopprime: sopprimere produceva zero
        # proposte, e uno strumento che non dice niente non fa correggere niente.
        L = D.Lettura(nome="x", gs=None, dv=8, dado=8, tipo="humanoid", armatura=(5, 2))
        sb, conti, manca = D.deriva(L)
        self.assertIsNotNone(sb)
        self.assertFalse(any("collaudo" in c for c in conti), conti)

    def test_un_risultato_assurdo_esce_MARCATO_fuori_bersaglio(self):
        # CA 11 per un mostro di GS 9 e' il modo in cui questa derivazione
        # sbaglia: non rumoroso, ma con l'aria di un conto. Perciò la proposta
        # esce **con scritto sopra** che è fuori bersaglio, invece di sparire.
        L = D.Lettura(nome="x", gs=9, dv=2, dado=8, tipo="humanoid", taglia="large")
        sb, conti, _ = D.deriva(L)
        self.assertIsNotNone(sb)
        self.assertIn("FUORI BERSAGLIO", sb.fonte)
        self.assertEqual(sb.fonte.count("FUORI BERSAGLIO"), 1, "avviso duplicato")

    def test_la_stessa_classe_con_due_livelli_si_rifiuta(self):
        # «Chierico 10 / Prestige …» e più avanti «Chierico 13»: la scheda
        # descrive la build in due modi, e sommarli dava Tempra +17 per un GS 13.
        import tempfile
        d = Path(tempfile.mkdtemp()); f = d / "x-cr13.md"
        f.write_text("# X\n\nChierico 10 / Prestige (Matrona). "
                     "Poi: Chierico 13, domini.", encoding="utf-8")
        sb, _, manca = D.deriva(D.leggi_scheda(f))
        self.assertIsNone(sb)
        self.assertTrue(any("due modi" in m for m in manca), manca)

    def test_le_righe_non_verificate_della_tabella_sono_dichiarate(self):
        # Non tutte le righe per GS sono verificate contro la fonte: alcune le
        # ho interpolate io, e un giudizio duro non si dà su una riga così.
        self.assertTrue(D.PER_GS_VERIFICATE < set(D.PER_GS))
        L = D.Lettura(nome="x", gs=9, dv=2, dado=8, tipo="humanoid", taglia="large")
        self.assertIn("interpolata", D.deriva(L)[0].fonte)

    def test_le_matrici_sono_quelle_del_SRD(self):
        self.assertEqual(D.ELITE, (15, 14, 13, 12, 10, 8))
        self.assertEqual(D.BASIC, (13, 12, 11, 10, 9, 8))

    def test_i_ts_base_seguono_le_progressioni_srd(self):
        self.assertEqual([D.ts_buono(n) for n in (1, 5, 10, 20)], [2, 4, 7, 12])
        self.assertEqual([D.ts_cattivo(n) for n in (1, 3, 9, 20)], [0, 1, 3, 6])

    def test_i_dv_non_si_contano_due_volte(self):
        # «Orco Regular (Warrior 4)» nel titolo e «Warrior 4» nella prosa sono
        # la stessa cosa: la prima versione contava 12 DV e 48 pf per un GS 3.
        import tempfile
        d = Path(tempfile.mkdtemp()); f = d / "orco-cr3.md"
        f.write_text("# Orco Regular (Warrior 4)\n\nMedium humanoid, Warrior 4. 4d8+8.",
                     encoding="utf-8")
        L = D.leggi_scheda(f)
        self.assertEqual(L.classi, [("warrior", 4)])
        self.assertIsNone(L.dv, "i DV razziali si sommavano ai livelli di classe")


if __name__ == "__main__":
    unittest.main()
