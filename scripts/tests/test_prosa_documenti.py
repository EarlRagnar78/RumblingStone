"""`validate_prosa --documenti`: i tic delle guide, degli ADR e dei piani.

Bersaglio diverso dalla prosa di gioco, quindi tic diversi. In una guida non ci
sono read-aloud; quello che tradisce la macchina è il trattino lungo usato come
respiro e il numero annunciato prima dell'elenco.

Le soglie sono tarate sulla distribuzione reale del repo, non scelte a occhio:
mediana 82 trattini ogni mille righe di prosa e quartile alto 118 al momento
della taratura, mediana 73 dopo la ripulitura del lotto D. Questi test tengono
ferma quella taratura: una soglia che segnala tutto è una soglia che verrà
spenta, e con lei i rilievi buoni.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import validate_prosa as P  # noqa: E402


@contextmanager
def documento(testo: str, nome: str = "PIANO-PROVA.md"):
    d = Path(tempfile.mkdtemp(prefix="doc-"))
    try:
        f = d / nome
        f.write_text(testo, encoding="utf-8")
        yield f
    finally:
        shutil.rmtree(d, ignore_errors=True)


def _righe(quante: int, testo: str = "Una riga di prosa qualunque, senza tic.") -> str:
    return "\n".join(f"{testo} ({i})" for i in range(quante))


class Trattino(unittest.TestCase):
    def test_sotto_soglia_non_si_dice_niente(self):
        """⚠️ 12 trattini, non 5, ed è il punto.

        La prima versione ne usava cinque su sessanta righe: sotto la soglia di
        densità, ma anche sotto il **minimo di dieci occorrenze**, ed era quello
        a tenerla quieta. Abbassando la soglia da 150 a 5 il test restava verde:
        non stava misurando la densità. Trovato mutando il validatore.

        Dodici trattini su cento righe fanno 120/1000 — sopra il minimo, sotto
        la soglia. Ora è la densità a decidere."""
        testo = _righe(88) + "\n" + "\n".join(["Testo con — un trattone."] * 12)
        with documento(testo) as f:
            self.assertEqual(P.controlla_documento(f), [])

    def test_poche_occorrenze_non_fanno_densita(self):
        """Otto trattini in cinquanta righe fanno 160/1000: SOPRA la soglia di
        densità e sotto il minimo di dieci. Deve tacere lo stesso.

        Anche questo caso l'ha trovato una mutazione: la prima versione usava
        tre trattini su quarantacinque righe, che stanno sotto tutte e due le
        condizioni, e azzerare il minimo non la faceva cadere. Per fissare il
        minimo serve un caso in cui è l'unica cosa che tiene quieto il rilievo."""
        testo = _righe(42) + "\n" + "\n".join(["Testo con — un trattone."] * 8)
        with documento(testo) as f:
            self.assertEqual(P.controlla_documento(f), [])

    def test_sopra_soglia_si_segnala(self):
        # 20 trattini su 60 righe = 333/1000.
        testo = _righe(40) + "\n" + "\n".join(["Testo con — un trattone."] * 20)
        with documento(testo) as f:
            fuori = P.controlla_documento(f)
        self.assertTrue(any("trattini lunghi" in r for r in fuori), fuori)

    def test_le_tabelle_non_contano(self):
        """Il difetto della prima misura: contando le tabelle, il CHANGELOG
        risultava il file peggiore del repo con 2.819 trattini ogni mille
        righe. In una cella «—» vuol dire «niente», ed è la notazione giusta."""
        tabella = "\n".join(["| voce | — | — | — |"] * 40)
        with documento(_righe(45) + "\n" + tabella) as f:
            self.assertEqual(P.controlla_documento(f), [])

    def test_il_codice_non_conta(self):
        codice = "```\n" + "\n".join(["comando --opzione — nota"] * 30) + "\n```"
        with documento(_righe(45) + "\n" + codice) as f:
            self.assertEqual(P.controlla_documento(f), [])

    def test_i_titoli_e_le_citazioni_non_contano(self):
        rumore = "\n".join(["## Titolo — con trattone", "> citazione — con trattone"] * 15)
        with documento(_righe(45) + "\n" + rumore) as f:
            self.assertEqual(P.controlla_documento(f), [])

    def test_un_documento_corto_non_si_misura(self):
        """Sotto quaranta righe la densità è un artefatto: tre trattini in
        dieci righe fanno 300/1000 e non vogliono dire niente."""
        with documento("Testo con — trattone.\n" * 10) as f:
            self.assertEqual(P.controlla_documento(f), [])


    def test_l_intervallo_numerico_non_e_un_trattone(self):
        """`3–4 ore` e `GS 17–19` sono intervalli, e la lineetta enne ci va.

        Contarli chiederebbe di sbagliare la punteggiatura per far tacere il
        gate. Trenta intervalli su cinquanta righe restano zero rilievi."""
        testo = _righe(50) + "\n" + "\n".join(["Tre sessioni da 3–4 ore, GS 17–19."] * 15)
        with documento(testo) as f:
            self.assertEqual(P.controlla_documento(f), [])

    def test_il_respiro_fra_due_numeri_resta_contato(self):
        """L'esclusione è per la enne senza spazi, non per «numero — numero»."""
        testo = _righe(50) + "\n" + "\n".join(["Chiuso 2026-09-03 — 157 su 157."] * 15)
        with documento(testo) as f:
            fuori = P.controlla_documento(f)
        self.assertTrue(any("trattini lunghi" in r for r in fuori), fuori)


class ConteggioAnnunciato(unittest.TestCase):
    def test_si_segnala_oltre_la_soglia(self):
        testo = (_righe(45) + "\nCambiano tre cose.\nE per due ragioni.\n"
                 "Restano quattro punti.\nPoi cinque domande.")
        with documento(testo) as f:
            fuori = P.controlla_documento(f)
        self.assertTrue(any("numero annunciato" in r for r in fuori), fuori)

    def test_una_volta_o_due_va_bene(self):
        with documento(_righe(45) + "\nCambiano tre cose.\nE per due ragioni.") as f:
            self.assertEqual(P.controlla_documento(f), [])

    def test_il_messaggio_porta_gli_esempi(self):
        """Un rilievo che non dice dove guardare non fa correggere niente."""
        testo = (_righe(45) + "\nCambiano tre cose.\nE per due ragioni.\n"
                 "Restano quattro punti.")
        with documento(testo) as f:
            fuori = P.controlla_documento(f)
        riga = next(r for r in fuori if "numero annunciato" in r)
        self.assertIn("«tre cose»", riga)

    def test_due_punti_e_la_punteggiatura_non_un_conteggio(self):
        """«due punti» è il nome del segno `:`, e il gate lo contava.

        Il rilievo su `PIANO-PROSA-CHE-NON-SEMBRI-GENERATA.md` era fatto di due
        occorrenze su tre di questa forma, dentro la frase che prescrive proprio
        quel segno come antidoto al trattone. Cercate tutte le occorrenze nei
        documenti: nessuna annuncia un elenco."""
        testo = (_righe(45) + "\nIl segno giusto è due punti.\n"
                 "Anche qui vanno i due punti.\nE altrove due punti ancora.")
        with documento(testo) as f:
            self.assertEqual(P.controlla_documento(f), [])

    def test_il_conteggio_citato_non_e_il_conteggio_commesso(self):
        """Un documento che parla del tic lo cita, e citarlo non è commetterlo.

        Senza questa esclusione il gate segnalava proprio i file che scrivono la
        norma: il piano, la skill e il changelog che portano gli esempi come
        prova."""
        testo = (_righe(45) + "\nIl tic suona come «tre cose» in apertura.\n"
                 "Oppure come «due ragioni» dette prima dell'elenco.\n"
                 "O ancora `quattro punti`, annunciati e poi elencati.")
        with documento(testo) as f:
            self.assertEqual(P.controlla_documento(f), [])

    def test_il_conteggio_fuori_dalle_virgolette_si_conta_lo_stesso(self):
        """L'esclusione è per la citazione, non per il documento che ne parla."""
        testo = (_righe(45) + "\nIl tic suona come «tre cose» in apertura.\n"
                 "Cambiano tre cose.\nE per due ragioni.\nRestano quattro punti.")
        with documento(testo) as f:
            fuori = P.controlla_documento(f)
        self.assertTrue(any("numero annunciato" in r for r in fuori), fuori)

    def test_gli_altri_nomi_col_numero_due_restano_contati(self):
        """L'esclusione è la sola coppia «due punti», non la parola «due»."""
        testo = (_righe(45) + "\nCambiano due cose.\nE per due ragioni.\n"
                 "Restano due modi.")
        with documento(testo) as f:
            fuori = P.controlla_documento(f)
        self.assertTrue(any("numero annunciato" in r for r in fuori), fuori)


class Antitesi(unittest.TestCase):
    def test_tre_volte_si_segnalano(self):
        tic = "Non è un errore: è un'abitudine."
        with documento(_righe(45) + "\n" + "\n".join([tic] * 3)) as f:
            fuori = P.controlla_documento(f)
        self.assertTrue(any("antitesi" in r for r in fuori), fuori)

    def test_due_volte_no(self):
        tic = "Non è un errore: è un'abitudine."
        with documento(_righe(45) + "\n" + "\n".join([tic] * 2)) as f:
            self.assertEqual(P.controlla_documento(f), [])


class IlPerimetro(unittest.TestCase):
    def test_i_documenti_del_repo_si_trovano(self):
        trovati = {p.relative_to(REPO).as_posix() for p in P.documenti()}
        for atteso in ("README.md", "AGENTS.md", "plans/INDEX.md",
                       "docs/guides/GUIDA-BESTIARIO.md"):
            with self.subTest(file=atteso):
                self.assertIn(atteso, trovati)

    def test_il_contenuto_di_gioco_resta_fuori(self):
        """I due modi non si toccano: in un read-aloud i trattini e le
        maiuscole hanno regole loro, e misurarli qui sarebbe contarli due volte
        con soglie diverse."""
        for p in P.documenti():
            rel = p.relative_to(REPO).as_posix()
            with self.subTest(file=rel):
                self.assertFalse(rel[:3].rstrip("_").isdigit(), rel)

    def test_le_due_modalita_hanno_soglie_diverse(self):
        """Nel read-aloud l'antitesi passa una volta sola; in un piano da
        seicento righe due sono tollerabili."""
        self.assertGreater(P.SOGLIE_DOC["antitesi"], P.SOGLIE["antitesi"])


class LaRigaDiComando(unittest.TestCase):
    def test_documenti_non_e_bloccante_per_difetto(self):
        self.assertEqual(P.main(["--documenti"]), 0)

    def test_con_strict_diventa_bloccante(self):
        """Il repo ha 54 rilievi aperti: con --strict deve uscire 1."""
        self.assertEqual(P.main(["--documenti", "--strict"]), 1)

    def test_su_un_file_solo(self):
        with documento(_righe(45) + "\n" + "\n".join(["Con — trattone."] * 20)) as f:
            self.assertEqual(P.main(["--documenti", str(f)]), 0)


if __name__ == "__main__":
    unittest.main()
