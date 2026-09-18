"""Il metro del mestiere, e le cinque volte che al primo giro diceva il falso.

Il DM il 2026-09-18: *«c'e' un modo di misurare che il nuovo stile a 9 pilastri
e le altre cose inserite sono presenti in quella parte, in che percentuale»*.

🔴 **La prima tabella invertiva la verita'.** Non per un bug di sintassi: per il
difetto di ADR-0053 — *un matcher largo traveste l'ignoranza*. Ogni classe di
test qui sotto fissa **una** di quelle cinque bugie, e la fissa **dal lato che
morde**: un rilevatore che tornasse largo torna rosso qui.

⚠️ Il sesto difetto non era nei rilevatori ma nei **bersagli**: misuravo 6 file
del Palio su 15 e 1 di ARC-08 su 23, e la tabella non lo diceva. Gli zeri
sembravano assenze di mestiere ed erano assenze di misura.
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _mc():
    spec = importlib.util.spec_from_file_location(
        "misura_craft", ROOT / "scripts" / "misura_craft.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MC = _mc()
RX = {nome: rx for nome, rx, _ in MC.CONGEGNI}


def conta(congegno: str, testo: str) -> int:
    return len(RX[congegno].findall(testo))


class TestReadAloudNonEUnaNotaEditoriale(unittest.TestCase):
    """🐛 `^>` prendeva QUALSIASI citazione. DEF-1 segnava 183 read-aloud e
    sono `> **Sistema: D&D 3.5 SRD**`; l'Abbazia ne segnava 11 ed erano tutti
    prosa vera. Il numero diceva il contrario del vero."""

    NOTA = "> **Sistema: D&D 3.5 SRD** (al massimo Pathfinder 1e)\n"
    PROSA = "> *La mattina sulla soglia dell'osteria c'e' del sale grosso.*\n"

    def test_la_nota_editoriale_non_conta(self):
        self.assertEqual(conta("read-aloud narrativo", self.NOTA), 0)

    def test_la_prosa_in_corsivo_conta(self):
        """Il lato che morde: stringere non deve aver spento il rilevatore."""
        self.assertEqual(conta("read-aloud narrativo", self.PROSA), 1)

    def test_sul_documento_vero_il_banco_resta_intero(self):
        """L'Abbazia perde **zero** read-aloud passando al metro stretto: e'
        la prova che i suoi 11 erano tutti veri e i 183 di DEF-1 no."""
        testo, _, _ = MC.carica(MC.BERSAGLI["★ Abbazia (stand-alone)"])
        largo = len(__import__("re").findall(r"^>\s*[*_]*[A-ZÀ-Ù«\"]", testo,
                                            __import__("re").M))
        self.assertEqual(conta("read-aloud narrativo", testo), 11)
        self.assertEqual(largo, 11, "il banco e' il caso in cui i due metri "
                                    "coincidono: se diverge, la prova non vale piu'")


class TestLoSpotlightNonELaFormattazione(unittest.TestCase):
    """🐛 Pretendeva il **grassetto**. Il Palio nomina tutti e quattro i PG e
    non li scrive mai in grassetto: segnava 0. Misurava il markdown."""

    def test_il_PG_conta_anche_senza_grassetto(self):
        self.assertEqual(conta("spotlight per PG", "Tordek si fa avanti."), 1)

    def test_il_PG_in_grassetto_conta_ancora(self):
        self.assertEqual(conta("spotlight per PG", "**Hella** tace."), 1)


class TestEcoConosceIlPlurale(unittest.TestCase):
    """🐛 Il Palio ha un **file intero** chiamato `PALIO-CONSEGUENZE-ECHI.md`
    e segnava **zero echi**: il rilevatore non conosceva il plurale."""

    def test_echi_al_plurale_conta(self):
        self.assertGreaterEqual(conta("eco / conseguenze a distanza",
                                      "Echi (stile BG3) e echi RP"), 2)

    def test_il_palio_non_e_piu_a_zero_echi(self):
        testo, _, _ = MC.carica(MC.BERSAGLI["★ Palio di Channathgate"])
        self.assertGreater(conta("eco / conseguenze a distanza", testo), 0,
                           "il banco degli echi torna a dichiarare zero echi")


class TestIlDialogoHaDueConvenzioni(unittest.TestCase):
    """🐛 Il rilevatore pretendeva `Nome: «…»`: **zero in tutti i 12 bersagli**.

    ⚠️ **E la diagnosi che avevo dato era sbagliata a sua volta.** Avevo
    concluso «una forma inventata, che nessun documento usa». È il contrario:
    `editorial-standards.md` §2 la **prescrive** — `**NOME (registro/tono):**
    *«battuta»*` — e la si trova **sei volte in tutto il repo**. Il congegno
    `dialogo nella forma dichiarata` misura adesso proprio quello; questo qui
    conta le battute **comunque scritte**, che è un'altra domanda.

    ⚠️ E le virgolette dritte non sono automaticamente dialogo: nel Palio
    `"…"` da' **128 hit** e sono **titoli di canzoni**. Il discrimine e'
    >=3 parole **e** punteggiatura di frase."""

    def test_le_guillemette_contano(self):
        self.assertEqual(conta("battute di dialogo", "«Il Signore aspetta.»"), 1)

    def test_la_battuta_fra_virgolette_dritte_conta(self):
        self.assertEqual(
            conta("battute di dialogo", '"Ci pensate. Il banco resta qui."'), 1)

    def test_il_titolo_di_canzone_NON_conta(self):
        """Il lato che morde, ed e' quello che ha ucciso 106 falsi positivi."""
        for titolo in ('"L\'Aria dei Conti"', '"Il Lamento del Traghetto"',
                       '"Bastone-di-Serpente"', '"Disguise Self psionico"'):
            with self.subTest(titolo=titolo):
                self.assertEqual(conta("battute di dialogo", titolo), 0)

    def test_nessun_bersaglio_e_piu_a_zero_per_forma_inventata(self):
        """La Torre resta a zero — ma per un fatto, non per il metro: non ha
        **nessun** dialogo, ne' `«…»` ne' dritto. Gli altri devono averne."""
        vivi = 0
        for nome in MC.BERSAGLI:
            testo, _, _ = MC.carica(MC.BERSAGLI[nome])
            if conta("battute di dialogo", testo):
                vivi += 1
        self.assertGreaterEqual(vivi, 8, "il rilevatore e' tornato a non "
                                         "riconoscere nessuna convenzione")


class TestIlPilastroDichiarato(unittest.TestCase):
    """🔎 La risposta vera alla domanda del DM.

    La *fusion rule* dice «UN pilastro guida, al piu' due di supporto». I
    documenti che la applicano **la scrivono**: `(Casa di Davide lead)`,
    `(BG3 lead)`, `(Mercer support)`. Si conta quella marca."""

    def test_la_marca_del_pilastro_conta(self):
        self.assertEqual(
            conta("PILASTRO dichiarato (lead/support)",
                  "### 🌙 HELLA — la seconda vita alla prova (BG3 lead)"), 1)

    def test_il_support_tattico_NON_conta(self):
        """🔴 Il lato che morde: nel repo «support» e' quasi sempre un ruolo di
        combattimento. Senza il nome del pilastro dentro la parentesi, il
        rilevatore ripescherebbe «healing support» e direbbe una bugia."""
        for falso in ("un chierico da healing support", "ranged support",
                      "Kitor full support", "blaster e support"):
            with self.subTest(falso=falso):
                self.assertEqual(
                    conta("PILASTRO dichiarato (lead/support)", falso), 0)

    def test_solo_DEF_2_5_dichiarano_i_pilastri(self):
        """Il fatto misurato, e vale come non-regressione del canone: la marca
        esiste **solo** in DEF-2..DEF-5. Se un giorno comparisse altrove, e'
        perche' qualcuno ha portato lo stile — e questo test va aggiornato
        **di proposito**, non per caso."""
        con, senza = [], []
        for nome in MC.BERSAGLI:
            testo, _, _ = MC.carica(MC.BERSAGLI[nome])
            (con if conta("PILASTRO dichiarato (lead/support)", testo) else senza
             ).append(nome)
        self.assertEqual(sorted(con), ["DEF-2 Ritorno e affreschi",
                                       "DEF-3 Resurrezione Hella",
                                       "DEF-4 Viaggio 1.000 anni",
                                       "DEF-5 Ritorno Hammerfist"])
        self.assertIn("★ Abbazia (stand-alone)", senza)
        self.assertIn("DEF-1 Piano della Terra", senza)


class TestGliStandardRedazionaliScrittiEMaiApplicati(unittest.TestCase):
    """🔎 Il DM il 2026-09-18: *«parti da quello che è definito davvero per la
    parte di scrittura, stile e linea editoriale, e che c'è davvero nel repo
    skills»*. Partendo da lì si trova che gli standard esistono, sono
    **numerici**, e nessun cancello li guarda.

    `validate_modules.py` conta le occorrenze della **parola** «read-aloud» e
    si ferma a cinque: un master con cinque menzioni e **zero box** passa.
    """

    def test_la_regia_etichettata_e_la_forma_prescritta(self):
        """`editorial-standards` §2 chiede `**Read-aloud (pilastro lead).**`."""
        self.assertEqual(
            conta("regia etichettata **Read-aloud (X)**",
                  "> **Read-aloud (LotR lead).** *La sala si apre.*"), 1)
        self.assertEqual(conta("regia etichettata **Read-aloud (X)**",
                               "> **Read-aloud.** *senza pilastro*"), 0)

    def test_il_dialogo_prescritto_non_e_una_forma_inventata(self):
        """🔴 Correzione a una mia conclusione sbagliata.

        Avevo scritto che `Nome: «…»` era «una forma che nessun documento
        usa». È il contrario: `editorial-standards` §2 la **prescrive** come
        `**NOME (registro/tono):** *«battuta»*`. Il fatto misurato non è che
        la forma sia inventata — è che **quasi nessuno la segue**: esiste
        sei volte in tutto il repo.
        """
        self.assertEqual(
            conta("dialogo nella forma dichiarata",
                  '**BALVAR (stanco, passato remoto):** *«Fu una notte lunga.»*'), 1)

    def test_i_box_non_contano_le_note_editoriali(self):
        """🐛 Trovato due volte, la seconda in `box_read_aloud`.

        Scritta larga (`^>\\s*[*_]`), la funzione apriva un box su
        `> **Sostituisce e fonde**` e dava **51 box «con parentesi» su 67**
        in DEF-1: erano note di redazione, non letture.
        """
        nota = "> **Sistema: D&D 3.5 SRD** (max PF1e), MAI 5e.\n"
        prosa = "> *La sala si apre, e l'aria sa di ferro.*\n"
        self.assertEqual(len(MC.box_read_aloud(nota)), 0)
        self.assertEqual(len(MC.box_read_aloud(prosa)), 1)

    def test_il_tetto_delle_dodici_righe_morde(self):
        corto = "> *" + "riga.*\n> *".join(["a"] * 5) + "*\n"
        lungo = "> *" + "riga.*\n> *".join(["a"] * 20) + "*\n"
        self.assertEqual(MC.difetti_dei_box(corto)["oltre 12 righe"], 0)
        self.assertEqual(MC.difetti_dei_box(lungo)["oltre 12 righe"], 1)

    def test_l_abbazia_rispetta_il_proprio_standard(self):
        """Il banco misurato contro la norma che il repo dichiara: **zero**
        box oltre il tetto e **zero** con parentesi, su undici. È la ragione
        per cui è un banco, e la prova che il metro non è impossibile."""
        testo, _, _ = MC.carica(MC.BERSAGLI["★ Abbazia (stand-alone)"])
        d = MC.difetti_dei_box(testo)
        self.assertGreaterEqual(d["box"], 10)
        self.assertEqual(d["oltre 12 righe"], 0)
        self.assertEqual(d["con parentesi"], 0)

    def test_ADR_0014_e_stato_applicato_a_un_documento_solo(self):
        """🔎 Il fatto che il DM sospettava, misurato.

        `ADR-0014` (regia sensoriale obbligatoria) fu applicato nel commit
        `d9c357b` a **ARC07-DEF-1 e basta**. Questo test non impone che resti
        così: impone che **cambiarlo sia deliberato**.

        ✅ **Ed è successo il 2026-09-18, poche ore dopo.** La riscrittura di
        DEF-4 ha portato la regia di round nel **secondo** documento del repo,
        e questo cancello è diventato rosso — che era esattamente il suo scopo.
        Aggiornato a mano, di proposito. Il prossimo a farlo diventare rosso
        sarà DEF-5 o la Battaglia Finale, e si aggiungerà allo stesso modo.
        """
        con = []
        for nome in MC.BERSAGLI:
            testo, _, _ = MC.carica(MC.BERSAGLI[nome])
            if conta("regia di round (una battuta per attore)", testo):
                con.append(nome)
        self.assertEqual(sorted(con), ["DEF-1 Piano della Terra",
                                       "DEF-4 Viaggio 1.000 anni"],
                         "la regia di round e' comparsa altrove (bene!) oppure "
                         "e' sparita da uno dei due (male): aggiornare di proposito")


class TestIlBoxETICHETTATOEUnBoxAnchEsso(unittest.TestCase):
    """🔴 **Il difetto piu' grave dello strumento, e il terzo della stessa
    famiglia.** Trovato il 2026-09-18 **usando** lo strumento per riscrivere
    DEF-4: i numeri non si muovevano mentre il testo cambiava.

    `editorial-standards.md` §2 **prescrive** la forma
    `> **Read-aloud (pilastro lead).** *prosa*`. Il rilevatore contava solo i
    box che cominciano con prosa in corsivo **nuda**, e saltava tutti quelli
    etichettati — cioe' **i migliori**, quelli scritti a norma.

    ⚠️ **Ha reso false tre cifre gia' pubblicate**: «DEF-4 ha 5 read-aloud»
    (ne ha 15), «DEF-5 ne ha zero» (ne ha 4), «DEF-4 ha il divario piu' grave
    col Palio» (era gia' **sopra** il Palio in densita'). Reggono invece le
    due piu' forti: la Torre e la Battaglia Finale sono davvero a **zero**.
    """

    ETICHETTATO = "> **Read-aloud (LotR lead).** *La sala si apre.*\n"
    NUDO = "> *La sala si apre.*\n"
    NOTA = "> **Sistema: D&D 3.5 SRD** (max PF1e).\n"

    def test_il_box_etichettato_conta(self):
        self.assertEqual(conta("read-aloud narrativo", self.ETICHETTATO), 1)

    def test_il_box_nudo_conta_ancora(self):
        self.assertEqual(conta("read-aloud narrativo", self.NUDO), 1)

    def test_la_nota_editoriale_resta_fuori(self):
        """Il lato che morde da sopra: allargare per prendere gli etichettati
        non deve far rientrare le note, che erano il difetto **originale**."""
        self.assertEqual(conta("read-aloud narrativo", self.NOTA), 0)

    def test_anche_box_read_aloud_riconosce_l_etichetta(self):
        """La funzione gemella aveva lo stesso buco: `--box` misurava DEF-4
        su **2** box invece che su 12."""
        self.assertEqual(len(MC.box_read_aloud(self.ETICHETTATO)), 1)
        self.assertEqual(len(MC.box_read_aloud(self.NOTA)), 0)

    def test_l_etichetta_non_conta_come_prosa_da_leggere(self):
        """🔴 Il terzo strato dello stesso difetto. `**Read-aloud (Salvatore
        lead)**` e' rivolta al DM e non si legge ad alta voce: contarne le
        parentesi e i nomi dei pilastri faceva risultare **peggiore** ogni box
        scritto nella forma prescritta. DEF-4 segnava 9 box «con parentesi»
        e ne ha **2**."""
        d = MC.difetti_dei_box(self.ETICHETTATO)
        self.assertEqual(d["con parentesi"], 0,
                         "le parentesi dell'etichetta sono tornate a contare")
        self.assertEqual(d[">1 nome proprio"], 0,
                         "«LotR» e' un nome di pilastro, non un nome proprio "
                         "della scena")

    def test_i_numeri_veri_dei_read_aloud(self):
        """Le cifre corrette, fissate perche' non si possa tornare indietro
        in silenzio. Se cambiano, e' perche' qualcuno ha scritto o tolto
        prosa — e allora si aggiornano **di proposito**."""
        for nome, atteso in (("★ Abbazia (stand-alone)", 11),
                             ("★ Palio di Channathgate", 41),
                             ("ARC-09 Torre di Zalkatar", 0),
                             ("ARC-09 Battaglia Finale", 0)):
            with self.subTest(bersaglio=nome):
                testo, _, _ = MC.carica(MC.BERSAGLI[nome])
                self.assertEqual(conta("read-aloud narrativo", testo), atteso)


class TestIBersagliNonSiCampionanoInSilenzio(unittest.TestCase):
    """🔴 Il difetto che non era in nessun rilevatore.

    Misuravo **6 file del Palio su 15**, **1 di ARC-08 su 23**, **4 del Torneo
    su 22** — e la tabella stampava zeri che sembravano assenze di mestiere.
    E' la stessa forma del censimento tarato sul campione."""

    def test_un_modello_che_non_pesca_niente_e_un_errore(self):
        """Il lato che morde: prima un percorso sbagliato spariva in silenzio."""
        with self.assertRaises(SystemExit):
            MC.espandi(["07_il Portale Della Forgia Eterna/QUESTO-NON-ESISTE-*.md"])

    def test_ogni_bersaglio_pesca_i_file_che_dice(self):
        atteso = {"★ Palio di Channathgate": 15, "ARC-09 Torneo di Dauth": 22,
                  "ARC-09 Torre di Zalkatar": 12, "ARC-09 Battaglia Finale": 16,
                  "ARC-08 Hammerfist": 13}
        for nome, n in atteso.items():
            with self.subTest(bersaglio=nome):
                self.assertEqual(len(MC.espandi(MC.BERSAGLI[nome])), n)

    def test_le_versioni_superate_restano_fuori(self):
        """Un `DEPRECATO` o una `ERRATA-` non dicono niente sul documento vivo,
        e ARC-08 ne ha **quattro** che gonfierebbero ogni conteggio."""
        presi = {f.name for f in MC.espandi(MC.BERSAGLI["ARC-08 Hammerfist"])}
        self.assertTrue(presi, "nessun file: il modello si e' rotto")
        for nome in presi:
            self.assertNotIn("DEPRECATO", nome)
            self.assertNotIn("ERRATA-", nome)


if __name__ == "__main__":
    unittest.main()
