"""P1 — il read-aloud che presuppone un'azione del giocatore, provato all'indietro.

Meta' delle prove verifica che il rilevatore **taccia**: la seconda persona e'
legittima nel dialogo e nella visione, e un rilevatore che segnala tutto viene
spento dopo una settimana.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import misura_craft as mc  # noqa: E402

#: I 22 rilievi che **restano apposta** a lotto 2C chiuso, file per file.
#: Non sono un residuo tollerato: sono cinque classi di cose che il rilevatore
#: non sa distinguere dalla narrazione, e che la norma non riguarda.
#:
#:   * **dialogo** (12) — Moradin, Aegis Fang, Mask e Lathander, Re Thorek,
#:     Nania, Lythiel, Tempestas, la cellula di Dauth: parlano in seconda
#:     persona al loro interlocutore, ed e' il loro registro;
#:   * **canto** (1) — la ballata del Palio e' un testo cantato a qualcuno;
#:   * **visione interiore** (2) — il sogno di Thorik in DEF-2, il flash della
#:     visione di Moradin in P2;
#:   * **falso positivo del rilevatore** (6) — «chiunque lo *guardi*» e
#:     «chiunque *tocchi*» sono terza persona congiuntiva; «*VEDI* PARTE 2»,
#:     «*Vedi* CONTRADE-STEMMI-CANTI» e «*vedi* `ARC07-DEF-1`» sono rimandi per
#:     il DM finiti dentro un box; «da dove *arrivi* la voce» e' una
#:     similitudine al congiuntivo;
#:   * **condizionale che la scelta la lascia** (1) — «Non parla finche' tu non
#:     la *prendi*» e' la forma che la norma chiede, e viene contata lo stesso.
ATTESI = {
    "PortaleForgia-P2-REVISED-Corretta-PARTE1.md": 4,
    "PortaleForgia-P1-REVISED-Corretta.md": 3,
    "Arco-Post-Hammerfist-HOOKS-Hella-SacredForest.md": 2,
    "ARC07-DEF-2-RITORNO-E-AFFRESCHI.md": 1,
    "ARC07-DEF-3-RESURREZIONE-HELLA.md": 1,
    "PortaleForgia-P2-REVISED-Corretta-PARTE2.md": 1,
    "CORREZIONE-Boss-Fauci.md": 1,
    "ARC08-01-GUIDA-DM.md": 1,
    "Arco-Post-Hammerfist-P2B-Torneo-DAUTH-SUBQUEST-Artemis.md": 1,
    "Arco-Post-Hammerfist-P2D-PALIO-PROVE-AMMISSIONE.md": 1,
    "Arco-Post-Hammerfist-P2D-PALIO-BALLATE.md": 1,
    "Arco-Post-Hammerfist-P2D-PALIO-DM-MASTER-REFERENCE.md": 1,
    "Arco-Post-Hammerfist-HOOKS-Artemis-TorreInvisibile.md": 1,
    "Arco-Post-Hammerfist-HANDOUTS.md": 1,
    "00_corona_di_adamantio_i_rituali_descrizioni_interventi_divini.md": 1,
    "05_Bracieri_Gemelli_Scheda_PG_Completa.md": 1,
}


class TestP1(unittest.TestCase):

    def test_segnala_un_senso_presupposto(self):
        t = "> *La sala e' buia, e sentite il freddo salire dalle pietre.*\n"
        self.assertEqual(len(mc.box_con_p1(t)), 1)

    def test_segnala_un_azione_presupposta(self):
        t = "> *Entrate nella sala, e al centro c'e' un altare.*\n"
        self.assertEqual(len(mc.box_con_p1(t)), 1)

    def test_tace_sulla_descrizione_oggettiva(self):
        """La forma corretta secondo la norma: il box descrive quello che c'e'."""
        t = "> *Al centro della sala, un altare. Il freddo sale dalle pietre.*\n"
        self.assertEqual(mc.box_con_p1(t), [])

    def test_il_participio_non_e_una_seconda_persona(self):
        """Il falso positivo vero: «conta le candele avanzate»."""
        t = "> *Nonna Grasa conta le candele avanzate e ne restano undici.*\n"
        self.assertEqual(mc.box_con_p1(t), [])

    def test_non_guarda_fuori_dai_box(self):
        """La norma parla dei read-aloud, non della prosa di regia."""
        t = "Il DM chiede ai giocatori se entrate o aspettate.\n"
        self.assertEqual(mc.box_con_p1(t), [])

    def test_l_etichetta_non_conta(self):
        """`**Read-aloud (X).**` e' rivolta al DM e non si legge ad alta voce."""
        t = "> **Read-aloud (Mercer lead).** *Al centro, un altare di basalto.*\n"
        self.assertEqual(mc.box_con_p1(t), [])

    def test_gli_archivi_e_i_prompt_sono_fuori(self):
        snapshot = mc.cartelle_snapshot()
        self.assertTrue(snapshot, "il repo non ha piu' nessuno snapshot dichiarato")
        for f in mc.file_di_gioco_p1():
            self.assertFalse(any(s in f.parents for s in snapshot), f)
            self.assertNotIn("Immagini", f.parts, f)
            self.assertNotIn("_ARCHIVIO", f.parts, f)

    def test_il_conteggio_sul_repo_e_quello_pubblicato(self):
        """Se questo cambia, il piano 2C va rimisurato prima di proseguire."""
        tot = sum(len(mc.box_con_p1(f.read_text(encoding="utf-8", errors="replace")))
                  for f in mc.file_di_gioco_p1())
        self.assertGreater(tot, 0, "il rilevatore non pesca piu' niente: verificalo")
        self.assertLess(tot, 200, f"{tot} rilievi: il rilevatore si e' allargato")

    def test_ogni_residuo_e_uno_dei_ventidue_dichiarati(self):
        """Il cancello del lotto 2C: chiuso il lotto, un rilievo nuovo e' un difetto.

        I 22 che restano sono **elencati uno per uno** in
        `plans/PIANO-QUATTRO-ORDINI-2026-09-20.md` §2C, con la loro classe:
        dialogo, canto, visione interiore, condizionale, falso positivo del
        rilevatore. Se questo test diventa rosso ci sono due casi, e vanno
        distinti prima di toccare il numero:

        * **un file ha un rilievo in piu'** -> quasi sempre un read-aloud nuovo
          che decide per il giocatore. Si corregge il testo, non il test.
        * **un file ha un rilievo in meno** -> qualcuno ha riscritto una delle
          esenzioni. Si aggiorna ATTESI **e** l'elenco nel piano, insieme.

        Abbassare il numero senza aprire i file e' esattamente l'errore che la
        FASE 3 del piano vieta: restringere il metro per far scendere la misura.
        """
        conteggio = {}
        for f in mc.file_di_gioco_p1():
            n = len(mc.box_con_p1(f.read_text(encoding="utf-8", errors="replace")))
            if n:
                conteggio[f.name] = n
        self.assertEqual(conteggio, ATTESI)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
