"""`validate_prosa --prima-dopo`: la riscrittura è migliorata o no?

Scritto **prima** dell'implementazione, e il caso di prova non è inventato: è
`05-ECHI-HELLA.md`, riscritto il 2026-09-02 e giudicato migliore dal DM. Tre
versioni in git, un giudizio umano su quale sia la buona. È l'unico metro vero
che questo repo abbia per la qualità della prosa.

## Perché una soglia assoluta non funziona, e un confronto sì

Tutte le misure assolute provate su questo corpus hanno fallito, e vale la pena
che restino scritte perché non tornino:

- **burstiness** (varianza della lunghezza delle frasi, la proposta più citata
  in letteratura): sulla riscrittura approvata **peggiora** — CV 0.55 → 0.47 —
  perché la riscrittura ha tolto i frammenti brevi, e togliere frammenti riduce
  la varianza. La metrica premia esattamente il tic che §9 vieta;
- **densità di frasi corte** come soglia di repo: il file peggiore (75%) è fatto
  di grida (*«PORTATORE MALEDETTO!»*) e note telegrafiche di regia (*«Treant lo
  lancia»*), non di frammenti narrativi;
- **aperture ripetute**: tre occorrenze in tutto il corpus. Troppo rare.

Le stesse misure **dentro un solo testo, fra due versioni**, non hanno il
problema: grida e note di regia ci sono prima e dopo, quindi si annullano. Quello
che resta è ciò che la riscrittura ha cambiato.
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import validate_prosa as P  # noqa: E402

#: Le tre versioni dell'eco di Hella, dalla più vecchia alla riscrittura
#: approvata dal DM il 2026-09-02.
ECHI = "07_il Portale Della Forgia Eterna/homebrew/sessione-terros/05-ECHI-HELLA.md"
ORIGINALE = "e7ed6b8"
INTERMEDIA = "f14f1b8"
APPROVATA = "67a6d21"


def _versione(sha: str) -> str | None:
    fuori = subprocess.run(["git", "show", f"{sha}:{ECHI}"],
                           cwd=REPO, capture_output=True, text=True)
    return fuori.stdout if fuori.returncode == 0 else None


class ImisuriChiTracciaLaQualita(unittest.TestCase):
    """Il criterio: la versione approvata deve misurare meglio della sua."""

    @classmethod
    def setUpClass(cls):
        cls.prima = _versione(INTERMEDIA)
        cls.dopo = _versione(APPROVATA)
        if cls.prima is None or cls.dopo is None:
            raise unittest.SkipTest("storia git non disponibile in questo checkout")

    def test_i_frammenti_brevi_calano(self):
        """Il tic che la riscrittura ha davvero tolto: *«Sono tuoi.»*,
        *«Non sai se lui ha sentito.»*"""
        self.assertLess(P.conta_tic(self.dopo)["frammenti"],
                        P.conta_tic(self.prima)["frammenti"])

    def test_le_aperture_ripetute_calano(self):
        """*«Nessuno va spiegato. Nessuno va interpretato ad alta voce.»*"""
        self.assertLessEqual(P.conta_tic(self.dopo)["aperture_ripetute"],
                             P.conta_tic(self.prima)["aperture_ripetute"])

    def test_il_verdetto_complessivo_e_migliorata(self):
        verdetto = P.confronta(self.prima, self.dopo)
        self.assertGreater(verdetto["migliorati"], verdetto["peggiorati"],
                           f"la riscrittura approvata dal DM deve misurare "
                           f"meglio: {verdetto}")

    def test_il_confronto_e_antisimmetrico(self):
        """Invertendo le due versioni il verdetto si capovolge. Senza questo,
        un confronto che dice sempre «migliorata» passerebbe il test sopra."""
        dritto = P.confronta(self.prima, self.dopo)
        rovescio = P.confronta(self.dopo, self.prima)
        self.assertEqual(dritto["migliorati"], rovescio["peggiorati"])
        self.assertEqual(dritto["peggiorati"], rovescio["migliorati"])

    def test_un_testo_con_se_stesso_non_cambia(self):
        v = P.confronta(self.dopo, self.dopo)
        self.assertEqual((v["migliorati"], v["peggiorati"]), (0, 0))


class LaBurstinessNonEUnObiettivo(unittest.TestCase):
    """⚠️ Questo test esiste per impedire una regressione di *progetto*.

    La varianza della lunghezza delle frasi è la misura più citata in
    letteratura e sembra la scelta ovvia. Su questo corpus va nella direzione
    sbagliata, e la prova è la riscrittura che il DM ha approvato. Se qualcuno
    fra sei mesi la propone di nuovo, questo test è il controesempio già
    scritto.
    """

    @classmethod
    def setUpClass(cls):
        cls.prima = _versione(INTERMEDIA)
        cls.dopo = _versione(APPROVATA)
        if cls.prima is None or cls.dopo is None:
            raise unittest.SkipTest("storia git non disponibile in questo checkout")

    def test_la_riscrittura_approvata_ha_burstiness_PEGGIORE(self):
        self.assertLess(P.burstiness(self.dopo), P.burstiness(self.prima),
                        "se questo test cade, la burstiness ha smesso di "
                        "contraddire il giudizio del tavolo e la decisione di "
                        "non usarla come soglia va riesaminata")

    def test_non_e_fra_i_tic_contati(self):
        self.assertNotIn("burstiness", P.conta_tic(self.dopo),
                         "misurabile sì, obiettivo no")


class ContaTic(unittest.TestCase):
    def test_i_frammenti_sono_le_frasi_corte(self):
        self.assertEqual(P.conta_tic("Uno due tre quattro cinque sei sette otto. "
                                     "Ed ecco.")["frammenti"], 1)

    def test_le_frasi_di_una_parola_sola_NON_contano(self):
        """⚠️ Scritto dopo aver misurato, e contro la mia prima versione.

        Il test originale usava «Corta.» e pretendeva che contasse: una frase di
        una parola è il frammento per eccellenza. Misurando il corpus, le frasi
        di una parola nei read-aloud sono **279 e quasi tutte artefatti**: «È…»,
        «Solo…», «Ma…», cioè la prima metà di una frase spezzata dai puntini di
        sospensione. Contarle vorrebbe dire inventare 279 tic che non ci sono.

        Il caso vero — la riscrittura di Hella — toglieva «Sono tuoi.» e «Non
        sai se lui ha sentito.», due e sei parole: il filtro non lo perde."""
        self.assertEqual(P.conta_tic("È... Solo... Ma...")["frammenti"], 0)
        self.assertEqual(P.conta_tic("Sono tuoi.")["frammenti"], 1)

    def test_le_aperture_ripetute_sono_consecutive(self):
        tre = "Nessuno va spiegato. Nessuno va detto. Nessuno va scritto."
        self.assertEqual(P.conta_tic(tre)["aperture_ripetute"], 2)
        sparse = "Nessuno va spiegato. Il sole scende. Nessuno va detto."
        self.assertEqual(P.conta_tic(sparse)["aperture_ripetute"], 0)

    def test_l_antitesi_e_contata(self):
        self.assertEqual(
            P.conta_tic("Non è collera: è peso.")["antitesi"], 1)

    def test_su_testo_vuoto_non_esplode(self):
        for vuoto in ("", "   ", "\n\n"):
            with self.subTest(testo=repr(vuoto)):
                self.assertEqual(P.conta_tic(vuoto)["frammenti"], 0)
                self.assertIsNone(P.burstiness(vuoto))


class IlProfiloDelleLunghezze(unittest.TestCase):
    """Il profilo è **informazione, non punteggio**, ed è l'unica parte della
    burstiness che è sopravvissuta alla verifica.

    Il ragionamento sta in ADR-0036: il coefficiente di variazione comprime in un
    numero solo due cose opposte — il ritmo vero (periodi ampi chiusi da una
    frase secca) e il tic dell'IA (una raffica di stoccate da due parole) — e
    quel numero, sulla riscrittura che il DM ha approvato, va nella direzione
    sbagliata. Le lunghezze **in ordine di lettura** non comprimono niente: si
    vede a occhio quale frase è sparita e quale è stata rifusa.

    Perciò questi test controllano una cosa sola oltre alla forma: che il profilo
    **non entri nel verdetto**. Se ci entrasse, avremmo rimesso dentro dalla
    finestra la misura che abbiamo buttato dalla porta.
    """

    @classmethod
    def setUpClass(cls):
        cls.prima = _versione(INTERMEDIA)
        cls.dopo = _versione(APPROVATA)
        if cls.prima is None or cls.dopo is None:
            raise unittest.SkipTest("storia git non disponibile in questo checkout")

    def test_sono_le_lunghezze_in_ordine_di_lettura(self):
        """L'ordine è il punto: un profilo ordinato per lunghezza sarebbe un
        istogramma, e un istogramma non dice **dove** cade la frase corta —
        che è l'unica cosa che distingue il ritmo dal tic."""
        p = P.profilo_lunghezze("Uno due tre quattro cinque sei. Uno due tre.")
        self.assertEqual(p["lunghezze"], [6, 3])

    def test_su_hella_si_vedono_i_frammenti_spariti(self):
        """Il caso che ha insegnato la lezione, e la ragione per cui il profilo
        esiste: la riscrittura ha tolto le frasi da 3, 6, 7 e 8 parole
        (*«Nessuno va spiegato.»*, *«Odore di pietra bagnata e di pelo caldo.»*)
        rifondendole dentro periodi. Il profilo lo mostra; il CV lo nasconde,
        perché la media sale più in fretta dello scarto."""
        a = P.profilo_lunghezze(self.prima)["lunghezze"]
        b = P.profilo_lunghezze(self.dopo)["lunghezze"]
        self.assertTrue({3, 6, 7, 8} <= set(a), a)
        self.assertFalse({3, 6, 7, 8} & set(b), b)

    def test_media_e_scarto_ricostruiscono_la_burstiness(self):
        """Se i due si separassero, il profilo racconterebbe una storia e la
        funzione un'altra."""
        p = P.profilo_lunghezze(self.dopo)
        self.assertAlmostEqual(p["scarto"] / p["media"], P.burstiness(self.dopo),
                               places=9)

    def test_su_testo_senza_frasi_e_None(self):
        for vuoto in ("", "   ", "\n\n"):
            with self.subTest(testo=repr(vuoto)):
                self.assertIsNone(P.profilo_lunghezze(vuoto))

    def test_il_profilo_NON_entra_nel_verdetto(self):
        """Il guardiano di questo lotto. Il verdetto resta deciso dai cinque tic
        contati; media, scarto e lunghezze non votano."""
        v = P.confronta(self.prima, self.dopo)
        for chiave in ("media", "scarto", "lunghezze", "burstiness", "profilo"):
            self.assertNotIn(chiave, v["delta"])

    def test_le_righe_sono_troncate_se_il_testo_e_lungo(self):
        """Un file di 215 frasi stamperebbe 215 numeri, e un profilo che non si
        legge non serve a niente."""
        lungo = " ".join("Uno due tre quattro." for _ in range(P.PROFILO_MAX + 20))
        numeri, coda = P.righe_profilo("dopo", lungo)
        self.assertEqual(len([t for t in numeri.split() if t.isdigit()]),
                         P.PROFILO_MAX)
        self.assertIn("+20", numeri)
        self.assertIn("media", coda)


class LaRigaDiComandoConProfilo(unittest.TestCase):
    def test_il_profilo_compare_sui_file_nominati(self):
        if _versione(APPROVATA) is None:
            self.skipTest("storia git non disponibile")
        righe = P.rapporto_confronto(REPO / ECHI, INTERMEDIA, profilo=True)
        testo = "\n".join(righe)
        self.assertIn("media", testo)
        self.assertIn("scarto", testo)

    def test_su_una_scansione_intera_il_profilo_non_compare(self):
        """`--prima-dopo` senza file confronta tutto il contenuto: 255 file per
        tre righe l'uno non è un rapporto, è un muro."""
        if _versione(APPROVATA) is None:
            self.skipTest("storia git non disponibile")
        righe = P.rapporto_confronto(REPO / ECHI, INTERMEDIA)
        self.assertEqual(len(righe), 1)
        self.assertNotIn("scarto", righe[0])


class LaRigaDiComando(unittest.TestCase):
    def test_prima_dopo_su_un_file_tracciato(self):
        if _versione(APPROVATA) is None:
            self.skipTest("storia git non disponibile")
        self.assertEqual(P.main(["--prima-dopo", "--rispetto-a", INTERMEDIA, ECHI]), 0)

    def test_un_file_non_tracciato_non_fa_esplodere(self):
        self.assertEqual(P.main(["--prima-dopo", "--rispetto-a", "HEAD",
                                 "file-che-non-esiste.md"]), 0)


if __name__ == "__main__":
    unittest.main()
