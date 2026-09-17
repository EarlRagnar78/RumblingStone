"""Chi ha statistiche in un arco dev'essere raggiungibile — lotto 4d-5.

🔴 **Il difetto misurato il 2026-09-17.** Diciannove documenti dell'arco 09
portano statblocchi in prosa — Taglia/Tipo, DV, CA, TS — scritti dal DM. Ma
`build_monster_catalog.py` e `suggest_encounter.py` costruiscono il pool degli
incontri scansionando i file **con la forma dello statblock**, e quella forma
d'arco non sempre la ha. Risultato: **47 fra PNG, villain e creature** avevano
statistiche complete e **nessuno strumento le raggiungeva**.

Fra questi il campione del Torneo di Dauth (Monk 14), il boss dei campi drow
(GS 13), e il Drago Rosso che guida l'invasione (GS 15).

La correzione segue il pattern gia' in uso nel repo (`capitana-lorana-cr7.md`):
una voce **POINTER** nel Bestiario che rimanda al file d'arco. Le statistiche
restano dove il DM le ha scritte — duplicarle creerebbe la seconda copia che
ADR-0021 vieta.

⚠️ **Questo test e' il presidio.** Senza, il prossimo documento d'arco con
statblocchi esce dal pool in silenzio, esattamente come questi quarantasette.

🔎 E il cancello se l'e' guadagnato subito: una volta scritto giusto ha trovato
da solo **tre file** che la ricerca a mano aveva saltato — i villain iconici del
torneo, le comparse dell'arena, i nemici della Quest di Hella.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import yaml  # noqa: E402

from dmcore.censimento import STATBLOCCO as STAT, documenti_con_statistiche  # noqa: E402

CATALOGO = yaml.safe_load(
    (ROOT / "scripts" / "monster_catalog.yaml").read_text(encoding="utf-8"))["monsters"]

#: 🔴 **Il censimento e' rinato il 2026-09-17, e il difetto era qui.** Questo
#: file cercava una forma sola di statblocco — quella con il trattino, la sola
#: che avevo sotto gli occhi scrivendolo. Il repo ne usa **tre**, e le altre due
#: nascondevano quindici documenti, fra cui un'avventura stand-alone intera.
#: Le tre forme, e la regola sugli archivi, stanno adesso in `dmcore.censimento`
#: con la misura scritta accanto.

#: Documenti che portano marche meccaniche ma **non sono roster di creature**.
#: Si dichiarano con il motivo, come `perche_senza_scheda` nell'anagrafica PNG
#: (ADR-0053): un'esclusione senza motivo scritto e' indistinguibile da una
#: dimenticanza, ed e' cosi' che questo cancello aveva perso l'Abbazia.
FUORI_RAGGIO = {
    "06_Stanza-corona-di-adamantio/StanzaCoronaDiAdamantio/00-La Corona di Adamantio-ogetto&Prove/000_Guida_Dm_Corona_adamantio_ogetto_prove_rituali_sfide.md":
        "guida all'artefatto: le marche sono bonus di gemme e CD di rituali, non creature",
    "06_Stanza-corona-di-adamantio/StanzaCoronaDiAdamantio/00-La Corona di Adamantio-ogetto&Prove/00_corona_di_adamantio_momento_risveglio_1_prova_scheda_giocatore.md":
        "scheda per il giocatore della Corona: poteri dell'artefatto, nessuna creatura",
    "07_il Portale Della Forgia Eterna/PortaleForgia-P1-REVISED-Corretta.md":
        "schede dei PG (§1 «Il party degli avventurieri»): i PG non stanno nel Bestiario",
    "08_La Battaglia Di Hammerfist/mass_combat_guide_Dm.md":
        "sistema di combattimento di massa: le statistiche sono esempi di unita', non un roster",
    "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P1C-Rituale-COMPLETO-SCALE.md":
        "regia del rituale; i drow delle tre ondate hanno schede proprie in Bestiario/mostri/drow-*",
}

#: Dove una voce puo' dichiarare il proprio bersaglio.
_INTESTAZIONI = ("**Source**", "**Key stats**", "**File correlati**")
_CITAZIONE = re.compile(r"`([^`]+\.md)`")


def _documenti_raggiunti() -> "set[str]":
    """Percorsi d'arco che uno strumento puo' davvero aprire.

    ⚠️ Si **risolve** il percorso, non si cerca la sottostringa. La prima
    stesura confrontava stringhe, e undici voci che citavano
    ``08_.../ARC08-01-GUIDA-DM.md`` risultavano agganciate: un umano capisce
    quei puntini, `Path.exists()` no. Erano POINTER che non puntavano.
    """
    raggiunti = {m["source_file"] for m in CATALOGO}
    for b in (ROOT / "Bestiario").rglob("*.md"):
        for riga in b.read_text(encoding="utf-8", errors="replace").splitlines():
            if not riga.startswith(_INTESTAZIONI):
                continue
            for citato in _CITAZIONE.findall(riga):
                for cand in (ROOT / citato, b.parent / citato, b.parent.parent / citato):
                    if cand.exists():
                        raggiunti.add(str(cand.resolve().relative_to(ROOT.resolve())))
                        break
    return raggiunti


def _documenti_con_statistiche() -> "list[Path]":
    return [ROOT / r for r in documenti_con_statistiche(ROOT)]


class TestOgniStatblocDArcoEraggiungibile(unittest.TestCase):
    def test_ogni_documento_con_statistiche_ha_un_aggancio(self):
        """🔴 Il cancello del lotto.

        Un documento d'arco con quattro o piu' marche di statblocco descrive
        creature giocabili. Se nessuna voce del catalogo lo cita come `Source`,
        quelle creature non esistono per `suggest_encounter`: il DM le ha
        scritte e il tavolo non le vedra' mai.
        """
        # ⚠️ Il catalogo registra come `source_file` il file SCANSIONATO — cioe'
        # la voce del Bestiario, non l'arco a cui rimanda. L'aggancio si cerca
        # quindi nella riga `**Source**` delle voci, che e' dove il POINTER
        # dichiara il proprio bersaglio. (La prima versione di questo test
        # cercava nel campo sbagliato e dava per scoperti quattro file agganciati.)
        #
        # E la seconda via: `build_monster_catalog` raggiunge DIRETTAMENTE alcuni
        # file d'arco, quando la loro forma gli basta (Zalkatar, Regiarix, il
        # Treant Corrotto). Un documento raggiungibile per quella strada non ha
        # bisogno di un POINTER: il criterio e' «gli strumenti ci arrivano»,
        # non «esiste una voce nel Bestiario».
        raggiunti = _documenti_raggiunti()
        orfani = []
        for p in _documenti_con_statistiche():
            rel = str(p.relative_to(ROOT))
            if rel in raggiunti or rel in FUORI_RAGGIO:
                continue
            orfani.append(rel)
        self.assertEqual(orfani, [],
                         "documenti d'arco con statistiche che nessuna voce del "
                         "Bestiario aggancia — servono voci POINTER, oppure una "
                         "riga in FUORI_RAGGIO che dica PERCHE' non e' un roster:\n  "
                         + "\n  ".join(orfani))

    def test_ogni_esclusione_dichiarata_e_vera(self):
        """Un'esclusione e' un'affermazione, e si prova — come R13 sui buchi.

        🔴 `FUORI_RAGGIO` dice «questo documento porta numeri ma non creature».
        Se il file sparisce o viene rinominato, l'esclusione resta e copre il
        nulla; se il documento smette di essere escluso dal censimento, la riga
        e' morta. Entrambi i casi vanno visti il giorno stesso.
        """
        censiti = set(documenti_con_statistiche(ROOT))
        for rel, motivo in FUORI_RAGGIO.items():
            with self.subTest(doc=rel.rsplit("/", 1)[-1]):
                self.assertTrue((ROOT / rel).exists(), f"escluso un file inesistente: {rel}")
                self.assertIn(rel, censiti,
                              "questa riga non esclude piu' niente: il censimento "
                              "non raccoglie piu' il documento")
                self.assertGreater(len(motivo), 30, "il motivo va scritto per esteso")

    def test_i_pointer_non_duplicano_le_statistiche(self):
        """ADR-0021: una voce POINTER rimanda, non copia.

        Se un giorno qualcuno ci incolla dentro i numeri, il Bestiario e l'arco
        diventano due copie che divergono alla prima errata — ed e' il difetto
        che il pattern POINTER esiste per non avere.
        """
        for p in (ROOT / "Bestiario").rglob("*.md"):
            testo = p.read_text(encoding="utf-8", errors="replace")
            if "[POINTER" not in testo.split("\n", 1)[0]:
                continue
            with self.subTest(voce=str(p.relative_to(ROOT))):
                self.assertLess(len(STAT.findall(testo)), 2,
                                "un POINTER porta statistiche: o e' una scheda "
                                "vera, o e' una copia che divergera'")
                self.assertIn("**Source**", testo)

    def test_il_pool_degli_incontri_e_cresciuto_e_resta_grande(self):
        """Il guadagno pratico, fissato: 305 → 352 (lotto 4d-5) → **372** (4d-6).

        ⚠️ La soglia si alza quando il pool cresce: lasciarla sotto il valore
        vero renderebbe il cancello piu' debole di quanto puo' essere.
        """
        self.assertGreaterEqual(len(CATALOGO), 372)

    def test_i_pointer_d_arco_puntano_a_file_che_esistono(self):
        """Stessa disciplina di R11 sull'anagrafica: un percorso si prova."""
        for m in CATALOGO:
            fonte = ROOT / m["source_file"]
            with self.subTest(voce=m["name"][:40]):
                self.assertTrue(fonte.exists(), m["source_file"])


class TestINomiCheIlTornEoHaPortato(unittest.TestCase):
    """Che i nominati siano davvero entrati, non solo il conteggio."""

    NOMI = ("Grandmaster Rihan", "Tetsu", "Lady Koryn", "Ironclad Bruiser",
            "Mistress of Mirrors", "Thrain Ironfist", "Grom Skullcrusher",
            "Zhen Windwhisper", "Kira", "Xilthra", "Killiar Arrowswift",
            "Saarvith")

    def test_ogni_individuo_nominato_e_nel_catalogo(self):
        nomi = " · ".join(m["name"] for m in CATALOGO)
        for n in self.NOMI:
            with self.subTest(png=n):
                self.assertIn(n, nomi)

    def test_grom_non_e_l_ogre_skullcrusher(self):
        """Due «Skullcrusher» diversi: il barbaro GS 14 del torneo e l'ogre GS 5.

        E' la forma d'errore che il lotto precedente ha documentato — un nome
        che combacia per somiglianza e porta alla creatura sbagliata.
        """
        grom = [m for m in CATALOGO if "Grom Skullcrusher" in m["name"]]
        ogre = [m for m in CATALOGO if m["name"].startswith("Ogre Skullcrusher")]
        self.assertEqual(len(grom), 1)
        self.assertTrue(ogre)
        self.assertNotEqual(grom[0]["cr"], ogre[0]["cr"])


class TestIlCatalogoLeggeQuelCheEDichiarato(unittest.TestCase):
    """🔴 Il difetto trovato aggiungendo una fazione — 2026-09-17.

    `build_monster_catalog.py` **indovinava** fazione, ruolo e ambiente da
    euristiche su parole chiave, e **ignorava le intestazioni** che ogni
    statblocco dichiara e che `validate_bestiario` pretende. Due valori per lo
    stesso fatto: quello scritto nel file e quello nel catalogo — e negli
    strumenti finiva il secondo.

    Si e' visto assegnando `zhentarim` ai combattenti del Torneo: l'intestazione
    diceva `zhentarim`, il catalogo registrava `dauth-defender`, e il file
    *sembrava* giusto a chiunque lo aprisse.

    Rimisurato dopo la correzione: **56 fazioni, 138 ruoli e 77 ambienti**
    erano sbagliati. Fra questi «Aberrazione Fungina Alfa» marcata
    `drow-sonjak` (la parola «drow» compariva nel testo) e il Grell della Torre
    Invisibile marcato `mountain`.
    """

    def test_la_fazione_dichiarata_finisce_nel_catalogo(self):
        indice = {m["source_file"]: m for m in CATALOGO}
        controllati = 0
        for p in (ROOT / "Bestiario").rglob("*-cr*.md"):
            rel = str(p.relative_to(ROOT))
            m = indice.get(rel)
            if not m:
                continue
            testa = p.read_text(encoding="utf-8", errors="replace")[:600]
            dich = re.search(r"\*\*Faction\*\*:\s*([A-Za-z0-9_-]+)", testa)
            if not dich:
                continue
            controllati += 1
            atteso = dich.group(1).lower()
            # un solo alias dichiarato: `mano-rossa` e' l'italiano di `red-hand`
            atteso = {"mano-rossa": "red-hand"}.get(atteso, atteso)
            with self.subTest(voce=m["name"][:40]):
                self.assertEqual(m["faction"], atteso)
        self.assertGreater(controllati, 140, "quasi nessuna scheda dichiara: "
                           "il test non sta provando quello che dice")

    def test_gli_zhentarim_del_torneo_sono_una_fazione_vera(self):
        """Canone dichiarato dal DM il 2026-09-17: emissari della Rete Nera,
        interessati al mercato nero extraplanare, minacciati anch'essi dalla
        Mano Rossa."""
        z = [m for m in CATALOGO if m["faction"] == "zhentarim"]
        self.assertGreaterEqual(len(z), 15)
        nomi = " · ".join(m["name"] for m in z)
        for atteso in ("Grandmaster Rihan", "Lady Koryn", "Kragar"):
            with self.subTest(png=atteso):
                self.assertIn(atteso, nomi)

    def test_la_mano_rossa_non_si_spacca_in_due_nomi(self):
        """L'alias evita una regressione vera: prima della correzione
        l'euristica normalizzava tutto, e leggere le intestazioni avrebbe
        separato le sei creature che dichiarano `mano-rossa` dalle 68 che
        dichiarano `red-hand`."""
        fazioni = {m["faction"] for m in CATALOGO}
        self.assertNotIn("mano-rossa", fazioni)
        self.assertGreaterEqual(
            len([m for m in CATALOGO if m["faction"] == "red-hand"]), 74)

    def test_le_voci_dell_abbazia_sono_entrate(self):
        """🔴 Un'avventura **intera** stava fuori dal censimento fino al 4d-6.

        `10-stand-alone/L'Abbazia della Rotta Sicura` sono 1.419 righe con un
        appendice di statblocchi tutto suo, e non aveva **una sola** voce nel
        Bestiario. Non e' sfuggita per poco: il matcher pretendeva il trattino
        (`- CA:`) e l'Abbazia scrive `**CA** 15`, quindi il documento valeva
        zero marche su zero e usciva dal conteggio in silenzio.
        """
        nomi = " · ".join(m["name"] for m in CATALOGO)
        for atteso in ("Padre Anselmo Grifo", "Ghebro Malaluna", "Grinza",
                       "Marea", "Madre Ilaria Sonda", "Tiberio Sarda"):
            with self.subTest(soggetto=atteso):
                self.assertIn(atteso, nomi)

    def test_il_dossier_di_fazione_non_finge_di_essere_una_creatura(self):
        d = ROOT / "Bestiario" / "villain" / "Zhentarim_Dauth" / "Zhentarim_Dauth.md"
        self.assertTrue(d.exists())
        self.assertIn("[NON-CREATURA]", d.read_text(encoding="utf-8").split("\n")[0])

if __name__ == "__main__":
    unittest.main()
