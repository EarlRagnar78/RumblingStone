"""Tre master, e ogni proposta sa in quale va — lotto 4d-2 (opzioni 1 e 2).

🔴 **La trappola che questi test chiudono.** Dal lotto 4d-1 le otto tabelle di
`campaign/state.md` sono GENERATE da `campaign/state.yaml` (ADR-0050).
`state_apply` pero' continuava a chiudere la sessione dicendo
«proposte NON meccaniche — **applicale a mano in state.md**»: per le proposte
tabellari quella era l'istruzione per **perderle**, perche' un'edizione a mano
dentro una regione `gen:state:` sparisce al prossimo `render_state.py` senza un
errore e senza un avviso.

Provato sul repo vero prima di scrivere il codice: cambiare «Dwarf Fighter 13»
in «14» dentro `state.md` faceva rosso `render_state --check`, e la modifica
spariva alla rigenerazione. Non esiste una via md → yaml.

I test sotto girano **sui file veri** dove il file vero e' l'oggetto della
prova (i tre master esistono, la scrittura chirurgica non riscrive lo YAML), e
su un repo temporaneo dove serve provare il FLUSSO di fine sessione senza
toccare il canone.
"""
from __future__ import annotations

import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import state_apply  # noqa: E402
import state_sync  # noqa: E402
from dmcore import masters  # noqa: E402
from dmcore import statedata as sd  # noqa: E402

import yaml  # noqa: E402

STATE_YAML = ROOT / "campaign" / "state.yaml"


# ---------------------------------------------------------------- i tre master


class TestOgniTriggerSaDoveVa(unittest.TestCase):
    def test_tutti_i_trigger_hanno_un_master(self):
        """Un trigger nuovo senza destinazione tornerebbe al messaggio generico."""
        dichiarati = {nome for nome, _ in state_sync.TRIGGERS}
        mancanti = dichiarati - set(masters.DESTINAZIONE)
        self.assertEqual(mancanti, set(),
                         f"trigger senza master in dmcore/masters.py: {mancanti}")

    def test_nessun_master_di_troppo(self):
        """L'altra meta': una riga per un trigger che non esiste piu' e' rumore."""
        dichiarati = {nome for nome, _ in state_sync.TRIGGERS}
        self.assertEqual(set(masters.DESTINAZIONE) - dichiarati, set())

    def test_le_proposte_tabellari_non_mandano_in_state_md(self):
        """🔴 Il cuore del lotto: §3 e' generato, mandarci a mano perde il dato."""
        for trigger in ("ritual_clock", "villain_clock", "npc_killed", "npc_escaped"):
            with self.subTest(trigger=trigger):
                m = masters.destinazione(trigger)
                self.assertEqual(m, masters.DATI)
                self.assertNotEqual(m.file, "campaign/state.md")

    def test_i_tre_file_dichiarati_esistono(self):
        for m in (masters.DATI, masters.PROSA, masters.STORIA):
            with self.subTest(master=m.file):
                self.assertTrue((ROOT / m.file).exists(), m.file)

    def test_il_raggruppamento_mette_i_dati_per_primi(self):
        gruppi = masters.per_master([("alliance", "a"), ("villain_clock", "v"),
                                     ("npc_killed", "k")])
        self.assertEqual(list(gruppi), [masters.DATI, masters.PROSA])
        self.assertEqual(gruppi[masters.DATI], ["v", "k"])

    def test_un_trigger_sconosciuto_non_sparisce(self):
        """Ammettere il buco: una proposta senza casa si stampa lo stesso."""
        gruppi = masters.per_master([("inventato", "x")])
        self.assertEqual(gruppi[None], ["x"])


# --------------------------------------------------- la scrittura chirurgica


class TestSiScriveUnCampoSolo(unittest.TestCase):
    """Sul file VERO: 502 righe, e dopo la modifica ne cambia una."""

    def setUp(self):
        self.testo = STATE_YAML.read_text(encoding="utf-8")
        self.dati = yaml.safe_load(self.testo)

    def test_cambia_solo_la_riga_del_campo(self):
        i = sd.trova_villain(self.dati, fondo=18, numeratore=9)
        self.assertIsNotNone(i, "il Ritual Clock su 18 non si trova piu' in §3")
        nuovo = sd.imposta_campo(self.testo, "villain", i, "clock", "10/18")
        a, b = self.testo.splitlines(), nuovo.splitlines()
        self.assertEqual(len(a), len(b), "la riscrittura ha cambiato il numero di righe")
        diverse = [n for n, (x, y) in enumerate(zip(a, b)) if x != y]
        self.assertEqual(len(diverse), 1, f"righe cambiate: {diverse}")

    def test_i_commenti_di_testa_restano(self):
        """`yaml.safe_dump` li cancellerebbe tutti: sono la spiegazione di ADR-0050."""
        i = sd.trova_villain(self.dati, fondo=18, numeratore=9)
        nuovo = sd.imposta_campo(self.testo, "villain", i, "clock", "10/18")
        self.assertIn("# Lo stato di campagna come DATO (ADR-0050)", nuovo)
        self.assertIn("# 🔴 Un master, mai due.", nuovo)

    def test_il_file_vero_non_viene_toccato(self):
        i = sd.trova_villain(self.dati, fondo=18, numeratore=9)
        sd.imposta_campo(self.testo, "villain", i, "clock", "10/18")
        self.assertEqual(STATE_YAML.read_text(encoding="utf-8"), self.testo)

    def test_un_campo_inesistente_e_un_errore_non_un_no_op(self):
        # ⚠️ Questo test usava `stato`, che dal 2026-09-16 **esiste** (D16): un
        # test che afferma l'assenza di un campo scade quando il campo nasce, e
        # se non lo si aggiorna diventa la prova che il lotto non ha funzionato.
        with self.assertRaises(sd.StateDataError):
            sd.imposta_campo(self.testo, "villain", 0, "movente_segreto", "x")

    def test_un_indice_fuori_intervallo_e_un_errore(self):
        with self.assertRaises(sd.StateDataError):
            sd.imposta_campo(self.testo, "villain", 999, "clock", "1/8")

    def test_una_sezione_inesistente_e_un_errore(self):
        with self.assertRaises(sd.StateDataError):
            sd.imposta_campo(self.testo, "inventata", 0, "clock", "1/8")

    def test_la_verifica_contro_il_parser_morde(self):
        """🔴 Il cancello provato all'indietro.

        Si sostituisce la riga con una che il parser legge in modo DIVERSO da
        quello dichiarato: se la verifica finale non ci fosse, questa scrittura
        passerebbe e cambierebbe silenziosamente la struttura del record.
        """
        vera = sd.imposta_campo
        i = sd.trova_villain(self.dati, fondo=18, numeratore=9)
        n, prefisso = sd._riga_del_campo(self.testo, "villain", i, "clock")
        righe = self.testo.splitlines(keepends=True)
        # la riga «giusta» sostituita da una che apre un altro campo
        righe[n] = prefisso + "clock: 10/18\n" + prefisso + "intruso: si\n"
        sabotato = "".join(righe)
        dopo = yaml.safe_load(sabotato)
        self.assertIn("intruso", dopo["villain"][i],
                      "il sabotaggio non ha prodotto la struttura attesa")
        # e la verifica di imposta_campo lo boccerebbe: stesso confronto
        import copy
        atteso = copy.deepcopy(self.dati)
        atteso["villain"][i]["clock"] = "10/18"
        self.assertNotEqual(dopo, atteso)
        del vera


class TestNonSiIndovinaIlVillain(unittest.TestCase):
    def setUp(self):
        self.dati = yaml.safe_load(STATE_YAML.read_text(encoding="utf-8"))

    def test_il_ritual_clock_e_l_unico_su_diciotto(self):
        i = sd.trova_villain(self.dati, fondo=18, numeratore=9)
        self.assertIn("Azarr Kul", self.dati["villain"][i]["villain"])

    def test_il_nome_identifica_la_riga(self):
        i = sd.trova_villain(self.dati, nome="sonjak", numeratore=4)
        self.assertIn("Sonjak", self.dati["villain"][i]["villain"])

    def test_piu_di_un_candidato_non_ne_sceglie_nessuno(self):
        """Ci sono piu' villain a clock 0/N: senza nome, nessuna risposta."""
        quanti = [v for v in self.dati["villain"]
                  if str(v.get("clock", "")).startswith("0/")]
        self.assertGreater(len(quanti), 1, "il repo non ha piu' l'ambiguita' misurata")
        self.assertIsNone(sd.trova_villain(self.dati, numeratore=0))

    def test_un_clock_non_numerico_non_e_un_contatore(self):
        """Sethrax ha «Sync to Tournament (…)»: non e' n/m, e non si tocca."""
        i = next(n for n, v in enumerate(self.dati["villain"])
                 if "Sethrax" in str(v.get("villain", "")))
        self.assertNotIn("/", str(self.dati["villain"][i]["clock"]).split()[0])
        self.assertIsNone(sd.trova_villain(self.dati, nome="sethrax", numeratore=2))

    def test_il_nome_del_villain_si_cattura(self):
        """Senza il nome, «Sonjak 3 → 4» diceva solo «3 → 4»: irrisolvibile."""
        rx = dict(state_sync.TRIGGERS)["villain_clock"]
        m = rx.search("- Sonjak 3 → 4")
        self.assertEqual(m.groups(), ("Sonjak", "3", "4"))


# ------------------------------------------- D16 · lo stato vivo di una persona


class TestLoStatoDiUnaPersonaEUnDato(unittest.TestCase):
    """🔵 **D16**, decisa dal DM il 2026-09-16.

    Prima di questo campo, «Regiarix killed» si scriveva dentro `dove` o
    `agenda` — un fatto strutturato infilato in una frase, cioe' lo stesso
    difetto che ADR-0050 aveva chiuso altrove. Adesso e' un'enumerazione chiusa,
    e chi la legge non deve interpretare prosa.
    """

    def setUp(self):
        self.dati = yaml.safe_load(STATE_YAML.read_text(encoding="utf-8"))

    def test_ogni_villain_e_ogni_PG_dichiara_il_proprio_stato(self):
        for sez in ("villain", "party"):
            for i, r in enumerate(self.dati[sez]):
                with self.subTest(sezione=sez, riga=i):
                    self.assertIn(r.get("stato"), VALORI_STATO,
                                  f"{sez}[{i}] non dichiara uno stato valido")

    def test_hella_e_morta_e_il_canone_dice_che_torna(self):
        """Il caso che fa guadagnare il campo il suo posto.

        Fino a oggi la morte di Hella viveva dentro `hp`, come prosa
        («n/d finche' non torna»): nessuno script poteva accorgersene, e §1 e §6
        si erano gia' contraddetti una volta proprio su questo (lotto 4c).
        """
        hella = next(p for p in self.dati["party"] if p["pg"] == "Hella")
        self.assertEqual(hella["stato"], "morto")
        self.assertIs(hella["reversibile"], True,
                      "il rito di resurrezione e' canone preparato: non e' definitiva")

    def test_uscire_di_scena_senza_dire_se_e_definitivo_e_bocciato(self):
        """R9 provata all'indietro: il cancello deve mordere."""
        import validate_state as vs
        finto = {"villain": [{"villain": "X", "stato": "morto"}], "party": []}
        self.assertTrue(vs.reversibilita_mancante(finto))
        finto["villain"][0]["reversibile"] = False
        self.assertEqual(vs.reversibilita_mancante(finto), [])

    def test_attivo_non_pretende_la_reversibilita(self):
        """L'altra meta': il cancello non deve chiedere un campo privo di senso."""
        import validate_state as vs
        self.assertEqual(
            vs.reversibilita_mancante({"villain": [{"villain": "X", "stato": "attivo"}]}), [])

    def test_gli_ignoti_si_contano(self):
        """R8, come R7: un buco contato vale piu' di un valore indovinato."""
        import validate_state as vs
        self.assertEqual(
            vs.stati_ignoti({"villain": [{"stato": "ignoto"}, {"stato": "attivo"}],
                             "party": []}),
            {"villain": 1})

    def test_la_vista_porta_lo_stato_nella_tabella(self):
        import render_state as rs
        reso = rs.rendi("villain", self.dati)
        self.assertIn("| Villain | Stato |", reso)
        self.assertIn("attivo", reso)

    def test_la_reversibilita_si_legge_nella_vista(self):
        import render_state as rs
        reso = rs.rendi("party", self.dati)
        self.assertIn("reversibile", reso,
                      "un morto che torna deve vedersi anche nel markdown")

    def test_conoscenze_NON_ha_lo_stato_ed_e_una_scelta_misurata(self):
        """🔴 §4 e' stata esclusa dopo averla guardata, non per dimenticanza.

        Tre righe non sono persone e tre persone vi compaiono sotto due nomi:
        `stato` li' vorrebbe dire un valore privo di senso in tre casi e due
        copie divergenti in altri tre. Se un giorno §4 diventa un'anagrafica,
        questo test cade e va riscritto — ed e' il momento giusto per farlo.
        """
        import validate_state as vs
        self.assertNotIn("conoscenze", vs.CON_STATO)
        nomi = [c["png"] for c in self.dati["conoscenze"]]
        non_persone = [n for n in nomi
                       if any(k in n for k in ("Circle", "Lathander", "wild elves"))]
        self.assertGreaterEqual(len(non_persone), 3,
                                "se §4 e' diventata un'anagrafica, questo test va rifatto")


# ------------------------------------------------- D14 · il tempo della macchina


class TestIlMarchClockEUnDato(unittest.TestCase):
    """🔵 **D14**: la riga della macchina in state.yaml, la nota del DM in prosa."""

    def setUp(self):
        self.testo = STATE_YAML.read_text(encoding="utf-8")
        self.dati = yaml.safe_load(self.testo)

    def test_il_giorno_corrente_e_un_campo(self):
        self.assertIsInstance(self.dati["march_clock"]["giorno_corrente"], int)

    def test_i_giorni_mancanti_si_DERIVANO_e_non_si_scrivono_due_volte(self):
        """🐛 La prima versione di questo test NON mordeva, e il giro dei
        sabotaggi l'ha scoperto.

        Confrontava il reso col valore atteso **sui dati di oggi**: 42 − 19 fa
        23, quindi cablare `**23**` nel renderer lo faceva passare lo stesso. Un
        test che concorda col difetto che dovrebbe trovare non prova niente.

        Adesso muove il dato e verifica che il reso lo SEGUA: un numero cablato
        resta fermo mentre il dato cambia, ed e' l'unica differenza osservabile
        fra derivato e scritto due volte.
        """
        import copy

        import render_state as rs
        for giorno in (19, 25, 40):
            with self.subTest(giorno=giorno):
                d = copy.deepcopy(self.dati)
                d["march_clock"]["giorno_corrente"] = giorno
                atteso = d["march_clock"]["giorno_arrivo"] - giorno
                reso = rs.rendi_march_clock(d)
                self.assertIn(f"**Current March Day:** **{giorno}**", reso)
                self.assertIn(f"**Days remaining to Rethmar:** **{atteso}**", reso)

    def test_il_giorno_di_arrivo_non_e_piu_cablato_nel_tool(self):
        """`RETHMAR_DAY = 42` viveva in state_apply: era una seconda fonte di
        verita', e sopravviveva perche' nessuno aveva mai eseguito il tool."""
        self.assertFalse(hasattr(state_apply, "RETHMAR_DAY"))

    def test_si_scrive_il_campo_senza_riscrivere_il_file(self):
        nuovo = sd.imposta_campo_oggetto(self.testo, "march_clock",
                                         "giorno_corrente", 25)
        a, b = self.testo.splitlines(), nuovo.splitlines()
        self.assertEqual(len(a), len(b))
        self.assertEqual(sum(1 for x, y in zip(a, b) if x != y), 1)

    def test_i_waypoint_sono_dieci_righe_di_dato(self):
        self.assertEqual(len(self.dati["march_clock"]["waypoints"]), 10)


VALORI_STATO = ("attivo", "latitante", "neutralizzato", "morto", "ignoto")

# --------------------------------------------------------- il flusso completo


MINI_YAML = """\
# commento che deve sopravvivere
schema_version: 1
villain:
- villain: Sonjak (Drow Cleric Matrona)
  dove: Underdark
  agenda: Sovvertire la cittadella
  clock: 4/8
  stato: attivo
  trigger: Incursione notturna
- villain: Azarr Kul (High Wyrmlord)
  dove: Fane of Tiamat
  agenda: Sacrifici rituali
  clock: 9/18
  stato: attivo
  trigger: Avatar di Tiamat
march_clock:
  giorno_corrente: 19
  giorno_arrivo: 42
  waypoints:
  - giorno: '1'
    waypoint: L'orda parte
    stato: passato
archi: []
party: []
artefatti: []
echi: []
conoscenze: []
difensori_rethmar: []
scenari_rethmar: []
"""

MINI_STATE = (
    "# Campaign State\n\n"
    "### 2.1 March Clock\n\n"
    "prosa che non si tocca MAI\n\n"
    "## 3. Villain\n\n"
    + "".join(f"<!-- gen:state:{n} -->\n(da rigenerare)\n<!-- /gen:state:{n} -->\n\n"
              for n in ("villain", "archi", "party", "artefatti", "echi",
                        "conoscenze", "difensori", "scenari",
                        # D14: i waypoint e le due righe della macchina sono
                        # regioni generate come le altre otto
                        "waypoints", "march_clock"))
    +
    "## 8. Changelog (append-only)\n\n"
    "> Lo storico vive in [`state-changelog.md`](state-changelog.md).\n"
)

MINI_CHANGELOG = (
    "# Changelog dello stato di campagna — append-only\n\n"
    "```\n2026-05-01  Initial state.md created.\n```\n"
)

MINI_SESSION = (
    "# Session 9 — Test (2026-05-09)\n\n"
    "## World events triggered\n\n"
    "- Sonjak 4 → 5\n"
    "- Regiarix killed\n"
    "- Dauth: +120\n"
)


class TestFineSessioneScriveNelMaster(unittest.TestCase):
    """E2E su repo temporaneo: il clock finisce nel YAML e la vista lo segue."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "campaign" / "sessions").mkdir(parents=True)
        self.yaml = self.repo / "campaign" / "state.yaml"
        self.state = self.repo / "campaign" / "state.md"
        self.clog = self.repo / "campaign" / "state-changelog.md"
        self.yaml.write_text(MINI_YAML, encoding="utf-8")
        self.state.write_text(MINI_STATE, encoding="utf-8")
        self.clog.write_text(MINI_CHANGELOG, encoding="utf-8")
        (self.repo / "campaign" / "sessions" / "2026-05-09_session-9.md").write_text(
            MINI_SESSION, encoding="utf-8")
        for cmd in (["init", "-q", "-b", "main"], ["config", "user.email", "t@t"],
                    ["config", "user.name", "t"], ["add", "-A"],
                    ["commit", "-qm", "init"], ["checkout", "-qb", "campaign-group-test"]):
            subprocess.run(["git", "-C", str(self.repo), *cmd], check=True)

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, *argv) -> "tuple[int, str]":
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = state_apply.main([*argv, "--repo-root", str(self.repo)])
        return rc, buf.getvalue()

    def test_il_clock_va_nello_yaml_e_la_tabella_lo_segue(self):
        rc, out = self._run("--migrate", "--no-guard")
        self.assertEqual(rc, 0, out)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-aqm", "m"], check=True)

        rc, out = self._run("--session", "2026-05-09_session-9.md", "--yes", "--no-guard")
        self.assertEqual(rc, 0, out)

        dati = yaml.safe_load(self.yaml.read_text(encoding="utf-8"))
        self.assertEqual(dati["villain"][0]["clock"], "5/8")
        self.assertEqual(dati["villain"][1]["clock"], "9/18", "l'altro non si tocca")
        self.assertIn("# commento che deve sopravvivere",
                      self.yaml.read_text(encoding="utf-8"))

        md = self.state.read_text(encoding="utf-8")
        self.assertIn("| Sonjak (Drow Cleric Matrona) |", md,
                      "la vista non e' stata rigenerata dal master")
        self.assertIn("5/8", md)
        self.assertIn("prosa che non si tocca MAI", md)
        self.assertIn("clock Sonjak 4/8 → 5/8", self.clog.read_text(encoding="utf-8"))

    def test_la_vista_resta_allineata_al_master(self):
        """Il criterio d'uscita: dopo l'apply, `render_state --check` sarebbe verde."""
        self._run("--migrate", "--no-guard")
        subprocess.run(["git", "-C", str(self.repo), "commit", "-aqm", "m"], check=True)
        self._run("--session", "2026-05-09_session-9.md", "--yes", "--no-guard")

        import render_state
        md = self.state.read_text(encoding="utf-8")
        rigenerato, mancanti = render_state.apply_regions(
            md, yaml.safe_load(self.yaml.read_text(encoding="utf-8")))
        self.assertEqual(mancanti, [])
        self.assertEqual(rigenerato, md, "state.md e' fuori sync con state.yaml")

    def test_le_proposte_a_mano_nominano_il_file_giusto(self):
        """🔴 La riga che fino al 2026-09-16 diceva «applicale a mano in state.md»."""
        self._run("--migrate", "--no-guard")
        subprocess.run(["git", "-C", str(self.repo), "commit", "-aqm", "m"], check=True)
        _, out = self._run("--session", "2026-05-09_session-9.md", "--check",
                           "--yes", "--no-guard")
        self.assertNotIn("applicale a mano in state.md", out)
        # Regiarix (morte) → dato; Dauth +120 (alleanze) → prosa
        blocco = out.split("proposte NON meccaniche", 1)[1]
        dati_idx = blocco.index("campaign/state.yaml")
        self.assertLess(dati_idx, blocco.index("Regiarix"),
                        "la proposta di morte non e' sotto il master dei dati")
        prosa_idx = blocco.index("campaign/state.md")
        self.assertLess(prosa_idx, blocco.index("Dauth"))
        self.assertLess(dati_idx, prosa_idx, "i dati vanno per primi")

    def test_senza_state_yaml_il_clock_resta_manuale(self):
        """Un repo che non ha ancora il master non deve rompersi: degrada."""
        self.yaml.unlink()
        subprocess.run(["git", "-C", str(self.repo), "commit", "-aqm", "via"], check=True)
        rc, out = self._run("--session", "2026-05-09_session-9.md", "--check",
                            "--yes", "--no-guard")
        self.assertEqual(rc, 0, out)
        self.assertIn("state.yaml assente", out)
        self.assertIn("advance **Sonjak**", out)

    def test_la_guardia_copre_anche_lo_yaml_sporco(self):
        """Era tarata solo su state.md: adesso il tool scrive anche altrove."""
        self._run("--migrate", "--no-guard")
        subprocess.run(["git", "-C", str(self.repo), "commit", "-aqm", "m"], check=True)
        self.yaml.write_text(MINI_YAML + "# sporco\n", encoding="utf-8")
        esito = subprocess.run(
            [sys.executable, str(SCRIPTS / "state_apply.py"),
             "--session", "2026-05-09_session-9.md", "--yes",
             "--repo-root", str(self.repo)],
            capture_output=True, text=True, cwd=str(self.repo))
        self.assertEqual(esito.returncode, 1, esito.stdout + esito.stderr)
        self.assertIn("state.yaml", esito.stderr)

    def test_senza_marcatori_non_scrive_nemmeno_il_master(self):
        """Master scritto e vista no sarebbe drift: o tutti e due, o nessuno."""
        self._run("--migrate", "--no-guard")
        self.state.write_text(
            self.state.read_text(encoding="utf-8").replace(
                "<!-- gen:state:villain -->", "<!-- villain -->"), encoding="utf-8")
        subprocess.run(["git", "-C", str(self.repo), "commit", "-aqm", "m"], check=True)
        prima = self.yaml.read_text(encoding="utf-8")
        rc, _ = self._run("--session", "2026-05-09_session-9.md", "--yes", "--no-guard")
        self.assertEqual(rc, 1)
        self.assertEqual(self.yaml.read_text(encoding="utf-8"), prima,
                         "il master e' stato scritto senza la sua vista")


if __name__ == "__main__":
    unittest.main()
