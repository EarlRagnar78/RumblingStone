"""Lo storico ha un file suo, e la via di scrittura lo segue — lotto 4d-2.

§8 di `campaign/state.md` erano **1.179 righe, il 71%** del file: lo stato vivo
non si leggeva piu' perche' la storia gli stava sopra. Adesso vivono in
`campaign/state-changelog.md`, e `state_apply` ci appende.

🔴 **Questi test girano sui FILE VERI, non su fixture, ed e' il punto.** La
PR #99 ha registrato un difetto proprio: *«lo split dello storico aveva rotto
`state_apply --migrate`. La CI non l'aveva vista perche' quei test girano su
fixture»*. Un fixture costruito per passare prova che il codice funziona sul
fixture.
"""
from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import state_apply as sa  # noqa: E402

STATE = ROOT / "campaign" / "state.md"
CHANGELOG = ROOT / "campaign" / "state-changelog.md"


class TestLoStoricoHaUnFileSuo(unittest.TestCase):
    def test_il_file_esiste_ed_e_grosso(self):
        self.assertTrue(CHANGELOG.exists(), "campaign/state-changelog.md")
        self.assertGreater(len(CHANGELOG.read_text(encoding="utf-8").splitlines()), 1000)

    def test_state_md_e_tornato_leggibile(self):
        """Era 1.657 righe, di cui 1.179 di storico."""
        righe = len(STATE.read_text(encoding="utf-8").splitlines())
        self.assertLess(righe, 600, f"state.md e' a {righe} righe: lo storico e' rientrato?")

    def test_la_sezione_8_e_un_puntatore_non_un_buco(self):
        """Chi apre il file e cerca lo storico va mandato dove e' finito."""
        testo = STATE.read_text(encoding="utf-8")
        self.assertIn("## 8. Changelog", testo)
        self.assertIn("state-changelog.md", testo)

    def test_lo_storico_non_e_rimasto_anche_in_state_md(self):
        """Due storici divergono: e' il difetto C2, e non si ricrea qui."""
        testo = STATE.read_text(encoding="utf-8")
        self.assertNotIn("2026-05-01  Initial state.md created", testo)
        self.assertIn("2026-05-01  Initial state.md created",
                      CHANGELOG.read_text(encoding="utf-8"))


ANCORA = "2026-05-01  Initial state.md created"


class TestLoSpostamentoNonHaRiscrittoNiente(unittest.TestCase):
    """Il criterio d'uscita: le righe spostate sono quelle di prima.

    Confrontate contro **git**, non contro una copia fatta al momento: e' la
    sola prova che non si e' perso o riordinato niente per strada.

    🐛 **E la prima versione di questo test era vera una volta sola.**
    Confrontava contro `HEAD`, che al momento in cui l'ho scritto era ancora il
    commit *prima* dello split. Committando, `HEAD` e' diventato lo split
    stesso e §8 di `state.md` un puntatore: il test e' passato in locale e ha
    fatto **rossa la CI**, per sempre. Un test ancorato alla POSIZIONE di un
    commit misura quando lo esegui, non cosa afferma.

    Adesso il commit di riferimento si trova per **contenuto**: l'ultimo in cui
    `state.md` conteneva ancora la prima riga dello storico.
    """

    def _commit_prima_dello_split(self) -> "str | None":
        sha = subprocess.run(
            ["git", "log", "--format=%H", "--", "campaign/state.md"],
            cwd=ROOT, capture_output=True, text=True).stdout.split()
        for s in sha:
            testo = subprocess.run(["git", "show", f"{s}:campaign/state.md"],
                                   cwd=ROOT, capture_output=True, text=True).stdout
            if ANCORA in testo:
                return s
        return None

    def _sezione_8_di(self, ref: str) -> list[str]:
        testo = subprocess.run(["git", "show", f"{ref}:campaign/state.md"],
                               cwd=ROOT, capture_output=True, text=True).stdout
        if ANCORA not in testo:
            self.skipTest(f"{ref} non porta lo storico in state.md")
        return testo.split("## 8. Changelog (append-only)", 1)[1].strip("\n").splitlines()

    def test_le_righe_sono_identiche_a_quelle_di_prima_dello_split(self):
        ref = self._commit_prima_dello_split()
        if ref is None:
            self.skipTest("nessun commit con lo storico dentro state.md "
                          "(clone shallow?)")
        prima = self._sezione_8_di(ref)
        nuovo = CHANGELOG.read_text(encoding="utf-8").splitlines()
        # il corpo comincia dopo l'intestazione e le righe di citazione
        i = next(n for n, r in enumerate(nuovo)
                 if r.strip() and not r.startswith(("#", ">")))
        corpo = nuovo[i:]
        while corpo and not corpo[-1].strip():
            corpo.pop()
        # i marcatori auto: sono aggiunti dalla migrazione, non sono contenuto
        corpo = [r for r in corpo if not r.startswith("<!-- auto:")]
        self.assertEqual(corpo, prima,
                         "lo spostamento ha riscritto qualcosa")


class TestLaViaDiScritturaFunziona(unittest.TestCase):
    """Provata sul file vero, in memoria: si legge il canone, non lo si tocca."""

    def test_la_regione_changelog_e_marcata(self):
        regioni = sa.find_regions(CHANGELOG.read_text(encoding="utf-8"))
        self.assertIn("changelog", regioni)

    def test_append_scrive_dentro_la_regione_e_in_coda(self):
        testo = CHANGELOG.read_text(encoding="utf-8")
        nuovo = sa.append_changelog(testo, "2099-01-01  voce di prova.")
        self.assertNotEqual(nuovo, testo)
        self.assertIn("2099-01-01  voce di prova.", nuovo)
        regione = sa.find_regions(nuovo)["changelog"].content(nuovo)
        self.assertIn("2099-01-01  voce di prova.", regione,
                      "la voce deve finire DENTRO la regione marcata")
        ultima = [r for r in regione.splitlines() if r.strip() and r.strip() != "```"][-1]
        self.assertEqual(ultima.strip(), "2099-01-01  voce di prova.",
                         "e in coda: un changelog e' append-only")
        self.assertEqual(CHANGELOG.read_text(encoding="utf-8"), testo,
                         "il file vero non deve essere stato toccato")

    def test_la_migrazione_e_idempotente(self):
        testo = CHANGELOG.read_text(encoding="utf-8")
        _, aggiunti = sa.migrate_changelog(testo)
        self.assertEqual(aggiunti, [], "rilanciare --migrate non deve raddoppiare i marker")

    def test_marca_l_ultimo_blocco_non_il_primo(self):
        """Lo storico ha TRE blocchi fenced: marcare il primo scriverebbe le
        voci nuove in mezzo a quelle del maggio 2026."""
        senza = CHANGELOG.read_text(encoding="utf-8").replace(
            "<!-- auto:begin key=changelog -->\n", "").replace(
            "<!-- auto:end key=changelog -->\n", "")
        marcato, aggiunti = sa.migrate_changelog(senza)
        self.assertEqual(aggiunti, ["changelog"])
        regione = sa.find_regions(marcato)["changelog"].content(marcato)
        self.assertNotIn("2026-05-01  Initial state.md created", regione,
                         "la regione non deve coprire il primo blocco")


class TestIlMarchClockNonSiMarcaPiuPerchePercheNonServe(unittest.TestCase):
    """🔵 **D14, chiusa dal DM il 2026-09-16.** Questa classe provava un RIFIUTO.

    `migrate()` presumeva che «`**Current March Day:**`» fosse una riga a se'; il
    lotto 4c l'aveva resa l'inizio di un **paragrafo di cinque righe** che spiega
    perche' il Giorno 19 e' un bersaglio e non un passato. Marcandone solo la
    prima, `apply_march_clock` l'avrebbe sostituita lasciando le altre quattro
    **orfane a meta' frase**, e il lotto 4d-2 scelse di **rifiutare** invece di
    indovinare dove finisse il paragrafo.

    Il rifiuto era la cosa giusta, ma era un blocco. Il DM l'ha sciolto: il
    numero e' un **dato** (`march_clock.giorno_corrente`) e la sua riga si
    rigenera come le tabelle; la spiegazione resta **prosa**, sotto e fuori
    dalla regione. Non condividono piu' una riga, quindi non si contendono piu'
    uno scrittore.

    ⚠️ I test sotto non sono i vecchi «resi verdi»: quelli provavano che il
    rifiuto scattasse, e quel comportamento non esiste piu'. Provano che la
    separazione **c'e' davvero nel file vero** — perche' se un giorno qualcuno
    riportasse i due dentro la stessa riga, si tornerebbe al blocco senza che
    nessuno se ne accorga.
    """

    def test_in_state_md_non_resta_nessuna_regione_auto(self):
        """Marcarne una dentro una regione `gen:` sarebbe due scrittori sullo
        stesso testo: il difetto dei due master, ricreato dalla sua correzione."""
        self.assertEqual(sa.find_regions(STATE.read_text(encoding="utf-8")), {})

    def test_migrate_non_ha_piu_niente_da_marcare_e_lo_dice(self):
        testo, aggiunti = sa.migrate(STATE.read_text(encoding="utf-8"))
        self.assertEqual(aggiunti, [])
        self.assertEqual(testo, STATE.read_text(encoding="utf-8"))

    def test_la_riga_della_macchina_e_dentro_la_regione_generata(self):
        testo = STATE.read_text(encoding="utf-8")
        regione = re.search(
            r"<!-- gen:state:march_clock -->\n(.*?)\n<!-- /gen:state:march_clock -->",
            testo, re.S)
        self.assertIsNotNone(regione, "la regione march_clock non c'e' piu'")
        self.assertIn("**Current March Day:**", regione.group(1))

    def test_la_nota_del_DM_e_FUORI_dalla_regione(self):
        """🔴 Il cuore di D14: se la spiegazione rientrasse nella regione, il
        primo aggiornamento la cancellerebbe."""
        testo = STATE.read_text(encoding="utf-8")
        regione = re.search(
            r"<!-- gen:state:march_clock -->\n(.*?)\n<!-- /gen:state:march_clock -->",
            testo, re.S).group(1)
        ancora = "punto di sincronia previsto"
        self.assertIn(ancora, testo, "la nota del DM e' sparita dal canone")
        self.assertNotIn(ancora, regione,
                         "la nota del DM e' finita DENTRO la regione generata: "
                         "il prossimo render_state la cancella")

    def test_la_via_di_scrittura_dello_storico_resta_accesa(self):
        """L'altra meta': togliere il march-clock non deve spegnere il changelog."""
        esito = subprocess.run(
            [sys.executable, "scripts/state_apply.py", "--migrate", "--no-guard"],
            cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(
            CHANGELOG.read_text(encoding="utf-8").count(
                "<!-- auto:begin key=changelog -->"), 1, esito.stdout + esito.stderr)


if __name__ == "__main__":
    unittest.main()
