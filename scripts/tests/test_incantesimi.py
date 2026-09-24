"""Le liste del generatore contro le liste di classe scritte nella skill.

Il criterio d'accettazione del lotto I: *ogni incantesimo di ogni lista
appartiene davvero a quella classe, verificato da un test; nessuna classe riceve
la lista di un'altra.*

Come per `test_tabelle.py`, il controllo vale solo se le due copie sono scritte
in posti diversi e per scopi diversi. Qui però non sono due copie della stessa
cosa, ed è meglio così:

    skills/dnd-35-srd/references/spells.md   *cosa quella classe PUÒ lanciare*
                                             — un fatto di regole, dal SRD
    scripts/dmcore/incantesimi.py            *cosa un controllore SCEGLIE*
                                             — una scelta di progetto

Il test verifica un'inclusione fra le due. Un errore di trascrizione da una parte
sola lo fa cadere; e soprattutto lo fa cadere il difetto per cui il lotto esiste,
cioè un druido a cui tocca la *palla di fuoco*.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import incantesimi as INC  # noqa: E402
from dmcore import tabelle as T  # noqa: E402

#: ⚠️ `skills/`, non `.claude/skills/` — la seconda è un mirror generato e
#: ignorato da git, che nella CI non esiste. Stessa trappola di `test_tabelle`.
ANCORA = ROOT / "skills/dnd-35-srd/references/spells.md"
ANCORA_PF = ROOT / "skills/pathfinder-1e-srd/references/conversion-guide.md"

#: intestazione nella skill → le classi che quella lista serve. Mago e stregone
#: stanno sotto la stessa perché nel SRD hanno la stessa lista.
INTESTAZIONI = {
    "Mago / Stregone": ("mago", "stregone"),
    "Chierico": ("chierico",),
    "Druido": ("druido",),
    "Bardo": ("bardo",),
    "Ranger": ("ranger",),
    "Paladino": ("paladino",),
}


#: Le classi come le intitola la sezione PF1e → la chiave del generatore.
INTESTAZIONI_PF = {
    "Mago / Stregone": ("mago", "stregone"),
    "Chierico": ("chierico",), "Druido": ("druido",), "Bardo": ("bardo",),
    "Ranger": ("ranger",), "Paladino": ("paladino",),
}


def _sezione(testo: str, dopo: str, intestazioni: dict,
             separatore: str = ",") -> dict[str, dict[int, set[str]]]:
    """Le righe `- **N**: a, b, c` sotto ogni `### Classe`, dopo un titolo.

    ⚠️ Il separatore è un parametro perché le due ancore non possono usarne uno
    solo: i nomi PF1e portano la virgola **dentro** — *pain strike, mass* —, e
    spezzarli lì corrompeva l'ancora in silenzio, con sette voci che diventavano
    «mass», «greater» e «lesser». Il test passava lo stesso, perché quelle voci
    fantasma non le cercava nessuno: erano *in più*, non *in meno*. È il modo in
    cui un'ancora smette di ancorare senza che niente lo dica.
    """
    coda = testo[testo.index(dopo):]
    fuori: dict[str, dict[int, set[str]]] = {}
    corrente: tuple[str, ...] = ()
    for riga in coda.splitlines():
        if riga.startswith("### "):
            corrente = intestazioni.get(riga[4:].strip(), ())
            for c in corrente:
                fuori.setdefault(c, {})
            continue
        m = re.match(r"- \*\*(\d)\*\*:\s*(.+)", riga.strip())
        if not m or not corrente:
            continue
        voci = {v.strip() for v in m.group(2).split(separatore) if v.strip()}
        for c in corrente:
            fuori[c][int(m.group(1))] = voci
    return fuori


def _ancora_pf1e() -> dict[str, dict[int, set[str]]]:
    """Le liste APG, cioè quello che PF1e aggiunge alla 3.5."""
    return _sezione(ANCORA_PF.read_text(encoding="utf-8"),
                    "## PF1e spell lists", INTESTAZIONI_PF, separatore=" · ")


def _ancora() -> dict[str, dict[int, set[str]]]:
    """classe → livello → gli incantesimi che quella classe può lanciare."""
    testo = ANCORA.read_text(encoding="utf-8")
    sezione = testo[testo.index("## Liste di classe"):]
    fuori: dict[str, dict[int, set[str]]] = {}
    corrente: tuple[str, ...] = ()
    for riga in sezione.splitlines():
        if riga.startswith("### "):
            corrente = INTESTAZIONI.get(riga[4:].strip(), ())
            for c in corrente:
                fuori.setdefault(c, {})
            continue
        m = re.match(r"- \*\*(\d)\*\*:\s*(.+)", riga.strip())
        if not m or not corrente:
            continue
        livello = int(m.group(1))
        voci = {v.strip() for v in m.group(2).split(",") if v.strip()}
        for c in corrente:
            fuori[c][livello] = voci
    return fuori


class OgniSceltaStaNellaListaDiQuellaClasse(unittest.TestCase):
    """Il test per cui il lotto I esiste."""

    @classmethod
    def setUpClass(cls):
        cls.ancora = _ancora()

    def test_la_skill_ha_ancora_le_sei_liste(self):
        """Se l'ancora sparisce, il test deve dirlo qui e non passare a vuoto."""
        self.assertEqual(sorted(self.ancora), sorted(INC.LISTE),
                         "le classi nella skill e quelle nel generatore non "
                         "coincidono più")
        for classe, per_livello in self.ancora.items():
            with self.subTest(classe=classe):
                self.assertTrue(per_livello, f"l'ancora di {classe} è vuota")

    def test_ogni_incantesimo_scelto_appartiene_a_quella_classe(self):
        for classe, funzioni in INC.LISTE.items():
            for funzione, per_livello in funzioni.items():
                for livello, voci in per_livello.items():
                    ammessi = self.ancora[classe].get(livello, set())
                    for voce in voci:
                        with self.subTest(classe=classe, funzione=funzione,
                                          livello=livello, incantesimo=voce):
                            self.assertIn(
                                voce, ammessi,
                                f"«{voce}» non è sulla lista di {classe} al "
                                f"{livello}° livello. O è di un'altra classe, o "
                                f"è al livello sbagliato — sono i due modi in "
                                f"cui il generatore sbagliava prima del lotto I")

    def test_nessuna_classe_riceve_la_lista_di_un_altra(self):
        """Il difetto originale, preso di petto invece che per inclusione.

        Sono gli incantesimi che le due schede rotte del Bestiario si erano
        trovate addosso.

        ⚠️ *Dito della morte* **non** è in questa lista, e la ragione vale più
        del test: il piano lo citava come «incantesimo da mago» dato a un
        druido, e non è vero. È sulla lista del druido all'**8°** livello (per
        il mago sta al 7°). Il difetto su quella scheda non era la classe
        sbagliata: era il **livello** sbagliato — che è l'altro modo in cui una
        lista per ruolo sbagliava, meno vistoso e più difficile da vedere al
        tavolo. Lo controlla `test_dito_della_morte_sta_all_ottavo_dal_druido`.
        """
        proibiti = {
            "druido": ["armatura magica", "sonno",
                       "benedizione", "santuario", "scudo della fede",
                       "palla di fuoco"],
            "chierico": ["palla di fuoco", "armatura magica", "intralciare"],
            "bardo": ["palla di fuoco", "benedizione", "corteccia"],
            "paladino": ["palla di fuoco", "intralciare"],
        }
        for classe, elenco in proibiti.items():
            tutti = {v for f in INC.LISTE[classe].values()
                     for voci in f.values() for v in voci}
            for voce in elenco:
                with self.subTest(classe=classe, incantesimo=voce):
                    self.assertNotIn(voce, tutti,
                                     f"un {classe} non lancia «{voce}»")

    def test_dito_della_morte_sta_all_ottavo_dal_druido(self):
        """L'errore di livello, che è il gemello silenzioso dell'errore di lista.

        Lo stesso incantesimo sta al 7° per il mago e all'8° per il druido.
        Sceglierlo dalla riga sbagliata dà una creatura che lancia un incantesimo
        che le spetta, un livello prima di quando le spetta — e al tavolo non se
        ne accorge nessuno finché non conta gli slot.
        """
        ancora = _ancora()
        self.assertIn("dito della morte", ancora["druido"][8])
        self.assertNotIn("dito della morte", ancora["druido"][7])
        self.assertIn("dito della morte", ancora["mago"][7])
        for funzione, per_livello in INC.LISTE["druido"].items():
            with self.subTest(funzione=funzione):
                self.assertNotIn("dito della morte", per_livello.get(7, []))

    def test_le_ventuno_celle_della_matrice_approvata(self):
        celle = {(c, f) for c, ff in INC.LISTE.items() for f in ff}
        self.assertEqual(len(celle), 21,
                         "la matrice approvata dal DM ha 21 celle")
        self.assertIs(INC.LISTE["mago"], INC.LISTE["stregone"],
                      "mago e stregone condividono la lista: nel SRD è la "
                      "stessa, e due copie divergerebbero")

    def test_ogni_funzione_copre_tutti_i_livelli_che_la_classe_lancia(self):
        """Una lista che si ferma al 6° per una classe che arriva al 9° darebbe
        un arcimago con gli slot alti vuoti e nessun avviso."""
        massimo_di_classe = {
            c: T.livello_massimo(T.INCANTATORI[c][0], 20) for c in INC.LISTE
        }
        for classe, funzioni in INC.LISTE.items():
            atteso = set(range(1, massimo_di_classe[classe] + 1))
            for funzione, per_livello in funzioni.items():
                with self.subTest(classe=classe, funzione=funzione):
                    self.assertTrue(
                        atteso <= set(per_livello),
                        f"a {classe}/{funzione} mancano i livelli "
                        f"{sorted(atteso - set(per_livello))}")

    def test_ranger_e_paladino_non_hanno_incantesimi_di_livello_zero(self):
        for classe in ("ranger", "paladino"):
            for funzione, per_livello in INC.LISTE[classe].items():
                with self.subTest(classe=classe, funzione=funzione):
                    self.assertNotIn(0, per_livello)
                    self.assertLessEqual(max(per_livello), 4)


class IlRipiegoRestaDentroLaClasse(unittest.TestCase):
    """La regola che sostituisce `LISTA_DI_RIPIEGO`, e che è tutto il punto."""

    def test_una_cella_che_non_esiste_ripiega_sulla_stessa_classe(self):
        # un mago «supporto» non c'è nel gioco
        lista, usata = INC.cella("mago", "supporto")
        self.assertNotEqual(usata, "supporto")
        self.assertIn(usata, INC.LISTE["mago"])
        self.assertIs(lista, INC.LISTE["mago"][usata])

    def test_il_ripiego_non_prende_mai_da_un_altra_classe(self):
        for classe in INC.LISTE:
            for funzione in INC.FUNZIONI:
                lista, usata = INC.cella(classe, funzione)
                with self.subTest(classe=classe, funzione=funzione):
                    self.assertIs(lista, INC.LISTE[classe][usata])

    def test_i_nomi_inglesi_trovano_la_stessa_lista(self):
        for inglese, italiano in (("wizard", "mago"), ("druid", "druido"),
                                  ("cleric", "chierico"), ("bard", "bardo"),
                                  ("paladin", "paladino")):
            with self.subTest(classe=inglese):
                self.assertIs(INC.cella(inglese, "controllore")[0],
                              INC.cella(italiano, "controllore")[0])

    def test_l_adepto_resta_dichiarato_scoperto(self):
        """L'unico residuo del lotto I, e deve restare visibile."""
        self.assertIn("adepto", INC.SENZA_LISTA)
        self.assertNotIn("adepto", INC.LISTE)
        righe, note = INC.scegli("adepto", "supporto", (3, 3, 2), _rng())
        self.assertEqual(righe, [])
        self.assertEqual(note, [])


class LaVariantePF1e(unittest.TestCase):

    def test_ogni_riga_pf1e_sta_sulla_lista_di_quella_classe(self):
        """La stessa disciplina delle liste 3.5, applicata a PF1e.

        La prima versione di questo test controllava solo che il nome PRD
        *comparisse* nella guida di conversione — cioè in una tabella scritta a
        mano insieme alle righe che doveva controllare. Non è un'ancora: è la
        stessa fonte due volte. Ora il confronto è con le liste dell'Advanced
        Player's Guide trascritte dalla pagina, e il controllo ha trovato tre
        errori veri (vedi la nota su `PF1E_SOLO`).
        """
        ancora = _ancora_pf1e()
        self.assertTrue(ancora, "la sezione delle liste PF1e è sparita dalla skill")
        for classe, per_livello in INC.PF1E_SOLO.items():
            for livello, voci in per_livello.items():
                ammessi = ancora[classe].get(livello, set())
                for _, prd in voci:
                    with self.subTest(classe=classe, livello=livello, incantesimo=prd):
                        self.assertIn(
                            prd, ammessi,
                            f"«{prd}» non è sulla lista APG di {classe} al "
                            f"{livello}° livello. È lo stesso difetto delle "
                            f"liste 3.5, su un'altra fonte")

    def test_l_ancora_pf1e_non_ha_voci_spezzate(self):
        """La guardia sul difetto del separatore.

        Nessuna voce può essere un suffisso nudo: se «mass» compare da sola,
        vuol dire che un nome è stato tagliato in due e l'ancora sta
        controllando qualcosa che non esiste.
        """
        ancora = _ancora_pf1e()
        for classe, per_livello in ancora.items():
            for livello, voci in per_livello.items():
                for v in voci:
                    with self.subTest(classe=classe, livello=livello, voce=v):
                        self.assertNotIn(v, {"mass", "greater", "lesser"})

    def test_il_chierico_dichiara_i_suoi_buchi(self):
        """Tre livelli scoperti, e devono restare scoperti.

        Al 1°, 6° e 7° l'APG non aggiunge al chierico niente che cambi un
        incontro. Riempirli per far quadrare la tabella darebbe una variante
        «più cattiva» che non è più cattiva — il modo peggiore di sbagliare,
        perché non si vede.
        """
        self.assertEqual(sorted(INC.PF1E_SOLO["chierico"]), [2, 3, 4, 5, 8, 9])

    def test_non_promuove_gli_incantesimi_che_pf1e_ha_indebolito(self):
        """Il modo peggiore di sbagliare: vendere come «più cattivo» qualcosa
        che PF1e ha reso più debole. La guida del repo li elenca."""
        indeboliti = {"grease", "glitterdust", "black tentacles",
                      "finger of death", "polymorph"}
        tutti = {prd for c in INC.PF1E_SOLO.values()
                 for v in c.values() for _, prd in v}
        self.assertEqual(tutti & indeboliti, set())

    def test_sostituisce_e_non_aggiunge_slot(self):
        """Il numero di slot è quello della tabella SRD e non si tocca."""
        slot = T.MAGO[9]
        base, _ = INC.scegli("mago", "blaster", slot, _rng())
        pf, note = INC.scegli("mago", "blaster", slot, _rng(), pf1e=True)
        self.assertEqual(len(base), len(pf))
        self.assertTrue(note)
        for riga_base, riga_pf in zip(base, pf):
            self.assertEqual(len(riga_base.split(",")), len(riga_pf.split(",")))

    def test_mago_e_stregone_condividono_anche_le_righe_pf1e(self):
        self.assertIs(INC.PF1E_SOLO["mago"], INC.PF1E_SOLO["stregone"])

    def test_lo_stesso_seme_da_la_stessa_lista(self):
        a, _ = INC.scegli("druido", "controllore", T.CHIERICO[12], _rng(11))
        b, _ = INC.scegli("druido", "controllore", T.CHIERICO[12], _rng(11))
        self.assertEqual(a, b)


def _rng(seme: int = 1):
    import random
    return random.Random(seme)


if __name__ == "__main__":
    unittest.main()
