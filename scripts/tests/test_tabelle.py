"""Le tabelle contro le loro ancore.

Il criterio del piano: *ogni riga cita la sua fonte; un test confronta la tabella
con le righe d'ancora della skill*. Non è una formalità. Le tabelle sono state
battute a mano da un manuale: l'unico modo per accorgersi di una cifra sbagliata
è confrontarla con una copia scritta altrove, in un altro momento, per un altro
scopo. Le skill sono quella copia.

Un test che ricalcolasse la tabella dalla tabella stessa non troverebbe niente —
e questo è il motivo per cui le ancore vengono lette dal markdown delle skill, e
non da una costante Python accanto a quella che dovrebbero controllare.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import tabelle  # noqa: E402

# ⚠️ `skills/`, non `.claude/skills/`. La seconda è un **mirror generato e
# ignorato da git** (`dm.py skills build`): esiste sulla macchina di chi lavora e
# NON nel checkout della CI, dove questo test è morto con FileNotFoundError.
# Peggio: tre modifiche a quei file — le righe d'ancora del chierico e due
# sezioni di skill — erano state scritte nel mirror, e non sarebbero mai entrate
# nel repo. Il file di verità sta in `skills/`.
#: Il percorso proibito, composto invece che scritto: altrimenti l'unica cosa
#: che il controllo troverebbe sarebbe la propria parola d'ordine.
MIRROR = ".claude/" + "skills"

SKILL_35 = ROOT / "skills/dnd-35-srd/references/classes.md"
SKILL_PF = ROOT / "skills/pathfinder-1e-srd/references/monster-advancement.md"


def _righe_markdown(testo: str, dopo: str) -> list[list[str]]:
    """Le righe della prima tabella markdown che segue un'intestazione."""
    coda = testo[testo.index(dopo):]
    righe = []
    for riga in coda.splitlines():
        riga = riga.strip()
        if not riga.startswith("|"):
            if righe:
                break
            continue
        celle = [c.strip() for c in riga.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in celle):
            continue
        righe.append(celle)
    return righe[1:]  # senza l'intestazione


def _slot(testo: str) -> tuple[int, ...]:
    """«6/6/6/6/5/3» o «4 | 4 | 3 | - | -» → la tupla degli slot."""
    pezzi = re.split(r"[/|]", testo)
    fuori = []
    for p in pezzi:
        p = p.strip()
        if p in {"-", "—", ""}:
            fuori.append(0)
        elif p.isdigit():
            fuori.append(int(p))
    while fuori and fuori[-1] == 0:
        fuori.pop()
    return tuple(fuori)


def _senza_coda(slot: tuple[int, ...]) -> tuple[int, ...]:
    """La griglia senza gli zeri in coda, per confrontarla con l'ancora.

    Le griglie tengono lo zero del livello che «si apre» (un bardo di 10° ha
    `3/3/3/2/0`: il 4° livello esiste ma è vuoto finché non arriva il bonus di
    caratteristica). `_slot` quegli zeri li toglie leggendo il markdown, e il
    confronto deve togliere gli stessi da tutt'e due i lati.
    """
    fuori = list(slot)
    while fuori and fuori[-1] == 0:
        fuori.pop()
    return tuple(fuori)


class AncoreIncantatori(unittest.TestCase):
    """Le griglie degli incantesimi contro le righe scritte nella skill 3.5."""

    @classmethod
    def setUpClass(cls):
        cls.testo = SKILL_35.read_text(encoding="utf-8")

    def test_stregone_incantesimi_al_giorno(self):
        righe = _righe_markdown(self.testo, "Verified anchor rows (SRD Table: The Sorcerer")
        self.assertTrue(righe, "la skill non ha piu' le righe d'ancora dello stregone")
        for cella in righe:
            liv, al_giorno = int(cella[0]), _slot(cella[1])
            with self.subTest(livello=liv):
                self.assertEqual(tabelle.STREGONE[liv], al_giorno)

    def test_stregone_incantesimi_conosciuti(self):
        righe = _righe_markdown(self.testo, "Verified anchor rows (SRD Table: The Sorcerer")
        for cella in righe:
            liv, conosciuti = int(cella[0]), _slot(cella[2])
            with self.subTest(livello=liv):
                self.assertEqual(tabelle.STREGONE_CONOSCIUTI[liv], conosciuti)

    def test_mago(self):
        righe = _righe_markdown(self.testo, "**Spells /day**:")
        self.assertTrue(righe, "la skill non ha piu' la tabella del mago")
        for cella in righe:
            liv = int(cella[0])
            with self.subTest(livello=liv):
                self.assertEqual(tabelle.MAGO[liv], _slot(" | ".join(cella[1:])))

    def test_chierico_e_druido(self):
        """Il chierico ha un'ancora in repo solo da quando serve al generatore."""
        righe = _righe_markdown(self.testo, "Verified anchor rows (SRD Table: The Cleric")
        self.assertTrue(righe, "la skill non ha le righe d'ancora del chierico")
        for cella in righe:
            liv = int(cella[0])
            with self.subTest(livello=liv):
                self.assertEqual(tabelle.CHIERICO[liv], _slot(cella[1]))
        self.assertIs(tabelle.DRUIDO, tabelle.CHIERICO,
                      "in 3.5 chierico e druido hanno la stessa griglia")

    def test_bardo(self):
        """Il bardo serviva davvero: `lomyn-redtongue-bardo4-cr3` è nel
        Bestiario, e fino al lotto I il generatore non sapeva costruirlo."""
        righe = _righe_markdown(self.testo, "Verified anchor rows (SRD Table: The Bard")
        self.assertTrue(righe, "la skill non ha le righe d'ancora del bardo")
        for cella in righe:
            liv = int(cella[0])
            with self.subTest(livello=liv):
                self.assertEqual(_senza_coda(tabelle.BARDO[liv]), _slot(cella[1]))
                self.assertEqual(_senza_coda(tabelle.BARDO_CONOSCIUTI[liv]),
                                 _slot(cella[2]))

    def test_ranger_e_paladino(self):
        """Le due griglie con lo zero finto in testa.

        L'ancora scrive la riga come la stampa il SRD — dal 1° livello — mentre
        la griglia porta uno zero davanti per tenere l'indice allineato con
        quelle degli altri incantatori. Il confronto deve togliere quello zero,
        o il test controllerebbe due cose diverse e non se ne accorgerebbe.
        """
        righe = _righe_markdown(self.testo, "Verified anchor rows (SRD Table: The Ranger")
        self.assertTrue(righe, "la skill non ha le righe d'ancora del ranger")
        for cella in righe:
            liv = int(cella[0])
            with self.subTest(livello=liv):
                self.assertEqual(_senza_coda(tabelle.RANGER[liv][1:]), _slot(cella[1]))
        self.assertIs(tabelle.PALADINO, tabelle.RANGER,
                      "nel SRD ranger e paladino hanno la stessa griglia")
        for liv in range(1, 21):
            with self.subTest(livello=liv, cosa="nessun incantesimo di livello 0"):
                self.assertEqual(tabelle.RANGER[liv][0], 0)

    def test_il_livello_dell_incantatore_di_ranger_e_paladino(self):
        """`livello − 3`, e non il livello di classe.

        Confonderli darebbe un paladino di 12° che lancia da 12°, con la CD
        sbagliata di due punti — il genere di errore che al tavolo non si vede
        finché qualcuno non supera un tiro salvezza che avrebbe dovuto fallire.
        """
        self.assertEqual(tabelle.livello_incantatore("paladino", 12), 9)
        self.assertEqual(tabelle.livello_incantatore("ranger", 4), 1)
        self.assertEqual(tabelle.livello_incantatore("ranger", 3), 0)
        for classe in ("mago", "chierico", "druido", "bardo", "stregone"):
            with self.subTest(classe=classe):
                self.assertEqual(tabelle.livello_incantatore(classe, 12), 12)

    def test_il_paladino_lancia_su_saggezza(self):
        """Il difetto che il repo aveva importato da PF1e.

        `classes.md` diceva «CHA-based» per il paladino: è la regola di
        Pathfinder. Nel SRD 3.5 la CD di un incantesimo da paladino è
        10 + livello + modificatore di **Saggezza**; il Carisma gli serve per
        Grazia Divina, Imposizione delle Mani e Punizione. Preso per Carisma,
        ogni paladino generato sarebbe uscito con la CD sbagliata e la
        caratteristica sbagliata al primo posto della matrice élite.
        """
        for classe in ("ranger", "paladin", "paladino"):
            with self.subTest(classe=classe):
                self.assertEqual(tabelle.INCANTATORI[classe][1], "sag")
        self.assertIn("WIS-based", self.testo)
        self.assertNotIn(
            "**Spellcasting**: Divine, 1st–4th level spells, CHA-based", self.testo,
            "la riga sbagliata è tornata nella skill")

    def test_le_griglie_sono_complete_e_monotone(self):
        """Vent'anni di livelli, e nessuna classe che perde slot salendo."""
        for nome, (griglia, _, _) in tabelle.INCANTATORI.items():
            with self.subTest(classe=nome):
                self.assertEqual(sorted(griglia), list(range(1, 21)))
                for liv in range(2, 21):
                    prima = tabelle.livello_massimo(griglia, liv - 1)
                    dopo = tabelle.livello_massimo(griglia, liv)
                    self.assertGreaterEqual(dopo, prima)

    def test_l_adepto_dichiara_di_non_avere_ancora(self):
        """La riga che non ho potuto controllare deve dirlo lei, non io."""
        self.assertIn("adept", tabelle.INCANTATORI_SENZA_ANCORA)
        self.assertLessEqual(tabelle.livello_massimo(tabelle.ADEPTO, 20), 5,
                             "l'adepto non supera il 5° livello d'incantesimo")


class AncorePerGS(unittest.TestCase):
    """La tabella PF1e per GS contro Table 1–1 come sta nella skill."""

    def test_le_righe_verificate_coincidono_con_la_skill(self):
        righe = _righe_markdown(SKILL_PF.read_text(encoding="utf-8"),
                                "| CR | AC | hp | High attack |")
        visti = set()
        for cella in righe:
            gs = int(cella[0])
            visti.add(gs)
            atteso = tabelle.PER_GS[gs]
            with self.subTest(gs=gs):
                self.assertEqual(atteso[0], int(cella[1]), "CA")
                self.assertEqual(atteso[1], int(cella[2]), "pf")
                self.assertEqual(atteso[2], int(cella[3]), "attacco")
                self.assertEqual(atteso[4], int(cella[5]), "CD primaria")
        self.assertEqual(visti, set(tabelle.PER_GS_VERIFICATE),
                         "le righe verificate devono essere ESATTAMENTE quelle "
                         "che la skill scrive: ne' meno (perderemmo un controllo) "
                         "ne' di piu' (ci fideremmo di una riga non vista)")

    def test_riga_gs_dice_se_e_verificata(self):
        riga, verificata = tabelle.riga_gs(13)
        self.assertTrue(verificata)
        self.assertEqual(riga["pf"], 180)
        _, verificata = tabelle.riga_gs(3)
        self.assertFalse(verificata, "GS 3 e' estrapolato e deve dichiararlo")

    def test_la_tabella_cresce(self):
        """Nessun GS che costa meno del precedente: sarebbe un errore di battitura."""
        for gs in range(2, 21):
            for campo in ("ca", "pf", "attacco", "cd"):
                with self.subTest(gs=gs, campo=campo):
                    self.assertGreaterEqual(tabelle.riga_gs(gs)[0][campo],
                                            tabelle.riga_gs(gs - 1)[0][campo])


class IlMirrorNonEUnaFonte(unittest.TestCase):
    """Nessun codice committato deve leggere da `.claude/skills/`.

    Il difetto che questo previene e' costato una CI rossa e — molto peggio —
    **tre modifiche perdute**. `.claude/skills/` e' un mirror rigenerato da
    `dm.py skills build` e ignorato da git: esiste sulla macchina di chi lavora
    e non nel checkout della CI. Scriverci dentro sembra funzionare (i test
    passano in locale, l'agente rilegge quello che ha scritto) e non lascia
    traccia nel repo. E' un fallimento silenzioso in tutte e due le direzioni:
    chi legge trova un file che in CI non c'e', chi scrive perde il lavoro.

    La fonte e' `skills/`. Sempre.
    """

    def test_nessuno_script_legge_dal_mirror(self):
        # Con `ast`, non con una ricerca di testo: la prima versione di questo
        # controllo segnalava il proprio commento e la propria riga di ricerca.
        # Un guardiano che accusa sé stesso è un guardiano che verrà spento.
        # Quello che conta è una **stringa usata come percorso**, non la parola
        # in una spiegazione.
        import ast
        radice = Path(__file__).resolve().parents[2]
        colpevoli = []
        for f in (radice / "scripts").rglob("*.py"):
            albero = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
            docstring = set()
            for n in ast.walk(albero):
                if not isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef,
                                      ast.AsyncFunctionDef)) or not n.body:
                    continue
                primo = n.body[0]
                if (isinstance(primo, ast.Expr)
                        and isinstance(primo.value, ast.Constant)
                        and isinstance(primo.value.value, str)):
                    docstring.add(id(primo.value))
            # Seconda esenzione, della stessa famiglia della prima: una stringa
            # PASSATA a una funzione che riconosce il mirror non lo legge — gli
            # chiede se lo e', ed e' il codice che serve a escluderlo. Trovata
            # dal test su `validate_docs._is_generated_mirror(".claude/skills/x")`.
            interrogazioni = set()
            for nodo in ast.walk(albero):
                if isinstance(nodo, ast.Call):
                    nome = getattr(nodo.func, "attr", None) or getattr(nodo.func, "id", "")
                    if "mirror" in (nome or "").lower():
                        for arg in nodo.args:
                            interrogazioni.add(id(arg))
            for nodo in ast.walk(albero):
                if (isinstance(nodo, ast.Constant) and isinstance(nodo.value, str)
                        and MIRROR in nodo.value
                        and id(nodo) not in docstring
                        and id(nodo) not in interrogazioni):
                    colpevoli.append(f"{f.relative_to(radice)}:{nodo.lineno}")
        self.assertEqual(colpevoli, [],
                         "questi leggono dal mirror invece che da skills/: "
                         + ", ".join(colpevoli))

    def test_le_ancore_che_uso_stanno_nel_repo(self):
        """Se un'ancora sparisce dal repo, il test deve dirlo qui e non in CI."""
        import subprocess
        radice = Path(__file__).resolve().parents[2]
        for f in (SKILL_35, SKILL_PF):
            with self.subTest(file=f.name):
                self.assertTrue(f.exists(), f)
                tracciato = subprocess.run(
                    ["git", "ls-files", "--error-unmatch", str(f.relative_to(radice))],
                    cwd=radice, capture_output=True)
                self.assertEqual(tracciato.returncode, 0,
                                 f"{f} non e' tracciato da git: in CI non ci sara'")


class Provenienza(unittest.TestCase):
    def test_ogni_tabella_dichiara_la_fonte(self):
        for nome in ("TIPI", "CLASSI", "TAGLIE", "ARMATURE", "ELITE", "BASIC",
                     "INCANTESIMI", "PER_GS", "PASSI_GS"):
            with self.subTest(tabella=nome):
                self.assertIn(nome, tabelle.PROVENIENZA)
                self.assertTrue(tabelle.PROVENIENZA[nome].strip())

    def test_la_fonte_dice_quale_sistema(self):
        """Il punto della gerarchia: si vede a colpo d'occhio cosa viene da dove."""
        for nome, fonte in tabelle.PROVENIENZA.items():
            with self.subTest(tabella=nome):
                self.assertTrue("SRD" in fonte or "PF1e" in fonte, fonte)

    def test_derive_statblocks_usa_le_stesse_tabelle(self):
        """Due copie divergono. E' successo al manifest dei tool."""
        import derive_statblocks as d
        self.assertIs(d.TIPI, tabelle.TIPI)
        self.assertIs(d.CLASSI, tabelle.CLASSI)
        self.assertIs(d.PER_GS_VERIFICATE, tabelle.PER_GS_VERIFICATE)


if __name__ == "__main__":
    unittest.main()
