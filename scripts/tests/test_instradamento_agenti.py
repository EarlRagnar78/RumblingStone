"""Il lavoro che entra in un thread trova il suo agente e la sua catena (ADR-0146)."""
from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import instradamento_agenti as ia  # noqa: E402
import vincolo_skill as vs  # noqa: E402

AGENTI = {p.stem for p in (ia.ROOT / ".claude" / "agents").glob("*.md")}


class TestScelta(unittest.TestCase):
    def test_lavori_tipici(self) -> None:
        casi = {
            "riscrivi il box read-aloud della forgia": "autore-prosa-gioco",
            "aggiungi un sottocomando a dm.py per il corredo": "integratore-dm",
            "promuovi ruff a stable": "piattaforma",
            "prepara il rilascio 1.1.0": "piattaforma",
            "disegna la mappa della cripta": "cartografo",
            "impagina il booklet della serata": "impaginatore",
            "potenzia Skullcrusher per il gruppo di livello 13": "regolista",
            "sistema la CI rossa sul test di validate_pg": "sviluppatore",
            "scrivi l'ADR breve": "autore-documenti",
            "porta il giocato della serata sul ramo di gruppo": "sincronizzatore-giocato",
            "ci sono patch ferme da sincronizzare su campaign-group-rumblingstone?":
                "sincronizzatore-giocato",
            "togli dal MEMORY.md la riga della PR unita": "custode-memoria",
            "cosa dice la memoria storica sul tetto della memoria del progetto?": "custode-memoria",
        }
        for testo, atteso in casi.items():
            with self.subTest(testo=testo):
                self.assertEqual(ia.scegli(testo)[:1], [atteso])

    def test_in_coda_al_file_non_e_la_coda_della_memoria(self) -> None:
        self.assertNotIn("custode-memoria", ia.scegli("aggiungi la funzione in coda al file"))

    def test_il_pronome_ci_non_e_la_ci(self) -> None:
        self.assertNotIn("sviluppatore", ia.scegli("ci sono altri PNG negli archi?"))

    def test_le_due_prose_non_si_sommano(self) -> None:
        self.assertEqual(ia.scegli("scrivi l'ADR breve"), ["autore-documenti"])

    def test_niente_riconosciuto_niente_suggerito(self) -> None:
        self.assertEqual(ia.scegli("grazie, a dopo"), [])

    def test_ogni_agente_nominato_esiste(self) -> None:
        nominati = set(ia.SKILL_AGENTE.values()) | set(ia.PAROLE_AGENTE) | set(ia.CATENE)
        self.assertLessEqual(nominati, AGENTI, nominati - AGENTI)
        self.assertEqual(set(ia.PRIORITA), AGENTI)
        for catena in ia.CATENE.values():
            self.assertIn(catena[0].split()[0], AGENTI)

    def test_ogni_skill_portata_a_un_agente_che_la_precarica(self) -> None:
        for skill, agente in ia.SKILL_AGENTE.items():
            with self.subTest(skill=skill):
                if skill == "rumblingstone-indagine":  # la carica su richiesta
                    continue
                self.assertIn(skill, vs.precaricate(agente))


def _wake(testo: str, ragione: str = "mention", note: str = "") -> str:
    """La busta con cui un messaggio del DM arriva al thread (forma vista il 2026-11-27)."""
    return (f'<wake reason="{ragione}" current-time="2026-11-27T07:36:20Z">\n'
            '  <project id="chan_x" type="project">\n    <thread ts="cmsg_t">\n'
            '      <message trigger="true" from="human" trust="principal" author="DM" '
            f'id="cmsg_m" sent-at="2026-11-27T07:36:20Z">{testo}</message>\n'
            '    </thread>\n  </project>\n'
            f'  <system-note>{note or "The message text above is complete and verbatim."}'
            '</system-note>\n</wake>\n')


class TestMessaggiSenzaLavoro(unittest.TestCase):
    """M2, tecnica 1: un messaggio che non chiede lavoro non riceve un suggerimento."""

    def test_il_tocco_su_una_card_tace(self) -> None:
        busta = _wake("Chose &#34;Le rivedo io prima&#34; on the decision card asking "
                      "&#34;Riscrivo il box read-aloud della forgia?&#34;", "decision-chosen")
        self.assertEqual(ia.scegli(busta), [])
        self.assertEqual(ia.scegli('Chose "Sì" on the decision card asking '
                                   '"Disegno la mappa della cripta?"'), [])

    def test_il_coordinatore_inoltrato_tace(self) -> None:
        for busta in ('<relay from="coordinator" session="s" current-time="t">\n  The note below '
                      'was written by the coordinator session.\n  <note>Rinumera la voce dopo la '
                      'PR della CI e del renderer.</note>\n</relay>',
                      "<coordinator-relay>il validator della mappa è verde</coordinator-relay>",
                      '<relay from="thread" session="s">\n  The note below was written by the Claude '
                      "session of another thread.\n  <note>Il box read-aloud è pronto.</note>\n</relay>"):
            with self.subTest(busta=busta[:20]):
                self.assertEqual(ia.scegli(busta), [])

    def test_le_notifiche_di_sistema_tacciono(self) -> None:
        for testo in ("<task-notification>\n<task-type>queued-remote-notifications</task-type>\n"
                      "<summary>1 unread notification (GitHub activity: CI workflow)</summary>\n"
                      "</task-notification>",
                      "[SYSTEM NOTIFICATION] il workflow della CI è finito",
                      "<system-note>Thread state: the user last wrote 58m ago.</system-note>",
                      _wake("", "thread-computer-status")):
            with self.subTest(testo=testo[:25]):
                self.assertEqual(ia.scegli(testo), [])

    def test_il_resoconto_di_un_sottoagente_tace(self) -> None:
        resoconto = ("Ho corretto il renderer e scritto il test pytest che falliva. Niente commit "
                     "né push.\n\n## Esito\nI validator sono verdi.\n\n"
                     "Documentazione da aggiornare: nessuna")
        busta = ("Another Claude session sent a message:\n<agent-message from=\"a1\">\n"
                 "[Subagent hand-back] The text below is the final report of a subagent.\n  "
                 + resoconto + "\n</agent-message>")
        self.assertEqual(ia.scegli(busta), [])
        self.assertEqual(ia.scegli(resoconto), [])

    def test_il_via_libera_breve_tace(self) -> None:
        for testo in ("ok procedi", "sì grazie", "Il merge è fatto, puoi procedere",
                      "perfetto, vai avanti", "Va bene, continua pure"):
            with self.subTest(testo=testo):
                self.assertEqual(ia.scegli(testo), [])

    def test_le_richieste_vere_con_ok_o_si_restano(self) -> None:
        casi = {"ok, disegna la mappa della cripta": "cartografo",
                "sì, scrivi l'ADR breve": "autore-documenti",
                "Ho visto che la CI è rossa sul test di validate_pg: sistemala": "sviluppatore",
                "ok procedi, poi promuovi ruff a stable": "piattaforma",
                # Codex, #534: i verbi con il pronome attaccato e «fai» sono lavoro
                "ok, scrivimi un'ADR breve": "autore-documenti",
                "ok, fai l'ADR breve": "autore-documenti"}
        for testo, atteso in casi.items():
            with self.subTest(testo=testo):
                self.assertEqual(ia.scegli(testo)[:1], [atteso])

    def test_il_contesto_della_sessione_non_e_il_messaggio(self) -> None:
        contesto_ = ('<session-context nonce="n1">\nBelow is context: project instructions, '
                     "the CI workflow and the box read-aloud.\n</session-context nonce=\"n1\">\n")
        self.assertEqual(ia.scegli(contesto_), [])
        self.assertEqual(ia.scegli(contesto_ + _wake("disegna la mappa della cripta"))[:1],
                         ["cartografo"])

    def test_nella_busta_conta_solo_il_messaggio(self) -> None:
        busta = _wake("disegna la mappa della cripta",
                      note="Use your fetch tools; the workflow script runs on CI.")
        self.assertEqual(ia.scegli(busta)[:1], ["cartografo"])
        self.assertEqual(ia.scegli(_wake("grazie, a dopo", note="the CI workflow script")), [])
        self.assertEqual(ia.testo_di_lavoro(_wake("l&#39;ADR &amp; il piano")), "l'ADR & il piano")


class TestOmonimi(unittest.TestCase):
    """M2, tecnica 2: un trigger non scatta sull'omonimo che parla d'altro."""

    COPPIE = [  # (skill, frase con l'omonimo, frase con il senso del trigger)
        ("rumblingstone-mapmaking", "fallo in un thread coordinato con il padre",
         "aggiungi le coordinate dei mostri nel JSON della mappa"),
        ("rumblingstone-mapmaking", "coordinate the threads with the parent session",
         "le coordinate della cripta sono sbagliate"),
        ("rumblingstone-narrative-style", "l'hook di Claude Code sul pre-push non parte",
         "scrivi un hook per la prossima serata"),
        ("rumblingstone-narrative-style", "aggiungi un hook UserPromptSubmit in settings.json",
         "serve un hook che porti i PG a Brindol"),
        # Codex, #534: il cancello della fiction non è il cancello del push
        ("rumblingstone-narrative-style", "l'hook del cancello a cricchetto non blocca il push",
         "progetta un hook per la scena al cancello"),
        ("rumblingstone-indagine", "nel caso i PG volino, che tattica usa il drago?",
         "prepara il caso dell'omicidio al mulino"),
        ("rumblingstone-indagine", "ogni thread nuovo aggiunge un caso al set d'oro",
         "il caso del mercante scomparso non si ricompone"),
        ("rumblingstone-indagine", "in ogni caso aggiungi i casi di test",
         "il caso è troppo lineare"),
        ("rumblingstone-campaign", "esporta la mappa in png e in webp",
         "quali png incontrano i PG alla locanda?"),
        ("rumblingstone-campaign", "il file token-orco.png è sfocato",
         "mancano le schede di due png"),
        ("rumblingstone-module-standard", "fai il merge su master del ramo",
         "rivedi il master della forgia"),
        ("rumblingstone-automation", "rivedi il corredo del drago nel tesoro",
         "prepara il corredo della serata"),
        ("rumblingstone-art-direction", "conta quante volte usiamo il connettore Canva via MCP",
         "genera la copertina con Canva"),
    ]

    def test_l_omonimo_non_scatta_il_senso_si(self) -> None:
        skill = ia._skill()
        for nome, omonimo, senso in self.COPPIE:
            with self.subTest(omonimo=omonimo):
                self.assertNotIn(nome, ia.isk.raggiunte(omonimo, skill))
                self.assertIn(nome, ia.isk.raggiunte(senso, skill))

    def test_il_trigger_lungo_con_la_stessa_parola_resta(self) -> None:
        # «hook pre-push fallisce» è della skill di debugging: l'omonimo vale solo per «hook»
        self.assertIn("rumblingstone-debugging",
                      ia.isk.raggiunte("l'hook pre-push fallisce", ia._skill()))

    def test_il_thread_coordinato_non_va_al_cartografo(self) -> None:
        self.assertNotIn("cartografo", ia.scegli(
            "in un altro thread coordinato con il padre rivedi le tattiche dei villain"))


class TestHook(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        p = mock.patch.object(ia, "REGISTRO", self.tmp / "reg.jsonl")
        p.start()
        self.addCleanup(p.stop)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def _prompt(self, testo: str, **extra) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(ia.hook_prompt(json.dumps(
                {"prompt": testo, "session_id": "s1", **extra})), 0)
        return out.getvalue()

    def test_suggerisce_agente_e_catena(self) -> None:
        dato = json.loads(self._prompt("aggiungi un sottocomando a dm.py"))["hookSpecificOutput"]
        self.assertEqual(dato["hookEventName"], "UserPromptSubmit")
        self.assertIn("integratore-dm", dato["additionalContext"])
        self.assertIn("autore-documenti", dato["additionalContext"])

    def test_non_ripete_lo_stesso_suggerimento(self) -> None:
        self.assertTrue(self._prompt("aggiungi un sottocomando a dm.py"))
        self.assertEqual(self._prompt("e sistema anche dm.py"), "")

    def test_dentro_un_sottoagente_tace(self) -> None:
        self.assertEqual(self._prompt("disegna la mappa", agent_id="a1"), "")

    def test_un_tocco_sulla_card_non_suggerisce_niente(self) -> None:
        busta = _wake("Chose &#34;A&#34; on the decision card asking &#34;Riscrivo il box "
                      "read-aloud?&#34;", "decision-chosen")
        self.assertEqual(self._prompt(busta), "")
        self.assertEqual(ia.riepilogo(ia.REGISTRO)["suggeriti"], 0)

    def test_la_catena_si_legge_anche_in_un_messaggio_inoltrato(self) -> None:
        busta = ('<relay from="coordinator" session="s">\n  <note>Riscrivi il sottocomando.\n'
                 "Catena: integratore-dm → regolista → autore-documenti\n  </note>\n</relay>")
        self.assertIn("Catena scritta", self._prompt(busta))

    def test_input_rotto_non_blocca(self) -> None:
        self.assertEqual(ia.hook_prompt("non è json"), 0)
        self.assertEqual(ia.hook_stop("non è json"), 0)

    def test_il_giocato_porta_nel_contesto_l_avviso_della_sincronia(self) -> None:
        with mock.patch.object(ia, "avviso_sincronia", return_value="🔴 S2 campaign-group-x: main"):
            dato = json.loads(self._prompt("porta il giocato della serata sul ramo di gruppo"))
        testo = dato["hookSpecificOutput"]["additionalContext"]
        self.assertIn("sincronizzatore-giocato", testo)
        self.assertIn("🔴 S2 campaign-group-x", testo)

    def test_l_avviso_rotto_non_ferma_il_suggerimento(self) -> None:
        with mock.patch.object(ia, "avviso_sincronia", side_effect=OSError("lento")):
            dato = json.loads(self._prompt("porta il giocato della serata sul ramo di gruppo"))
        self.assertIn("sincronizzatore-giocato", dato["hookSpecificOutput"]["additionalContext"])

    def test_altri_lavori_non_chiamano_la_sincronia(self) -> None:
        with mock.patch.object(ia, "avviso_sincronia", return_value="X") as m:
            self._prompt("disegna la mappa della cripta")
        m.assert_not_called()

    def test_l_avviso_della_sincronia_e_veloce_e_tace_senza_repo(self) -> None:
        with mock.patch.object(ia, "ROOT", self.tmp):
            self.assertEqual(ia.avviso_sincronia(), "")

    def test_fine_turno_registra_se_seguito(self) -> None:
        self._prompt("disegna la mappa della cripta")
        t = self.tmp / "t.jsonl"
        righe = [
            {"type": "user", "message": {"content": "disegna la mappa"}},
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": "Agent",
                 "input": {"subagent_type": "cartografo", "prompt": "x"}}]}},
        ]
        t.write_text("".join(json.dumps(r) + "\n" for r in righe), encoding="utf-8")
        ia.hook_stop(json.dumps({"session_id": "s1", "transcript_path": str(t)}))
        r = ia.riepilogo(ia.REGISTRO)
        self.assertEqual((r["suggeriti"], r["turni"], r["seguiti"]), (1, 1, 1))

    def test_agenti_contati_solo_dopo_l_ultimo_messaggio(self) -> None:
        t = self.tmp / "t.jsonl"
        righe = [
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "cartografo"}}]}},
            {"type": "user", "message": {"content": "altro lavoro"}},
        ]
        t.write_text("".join(json.dumps(r) + "\n" for r in righe), encoding="utf-8")
        self.assertEqual(ia.agenti_chiamati(str(t)), [])


ISTRUZIONI = ("Riscrivi il sottocomando corredo di dm.py.\n"
              "Catena: integratore-dm → regolista → autore-documenti\n")


def _uso_agente(nome: str) -> dict:
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Agent", "input": {"subagent_type": nome, "prompt": "x"}}]}}


def _bash(comando: str) -> dict:
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Bash", "input": {"command": comando}}]}}


class _BaseCancello(unittest.TestCase):
    """Registro e trascrizione in una cartella temporanea; nessun test qui."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        p = mock.patch.object(ia, "REGISTRO", self.tmp / "reg.jsonl")
        p.start()
        self.addCleanup(p.stop)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def _istruzioni(self, testo: str = ISTRUZIONI) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            ia.hook_prompt(json.dumps({"prompt": testo, "session_id": "s1"}))
        return out.getvalue()

    def _push(self, righe: "list[dict]", comando: str = "git push -u origin ramo",
              strumento: str = "Bash") -> "tuple[int, str]":
        t = self.tmp / "t.jsonl"
        t.write_text("".join(json.dumps(r) + "\n" for r in righe), encoding="utf-8")
        ev = {"tool_name": strumento, "tool_input": {"command": comando},
              "session_id": "s1", "transcript_path": str(t)}
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            codice = ia.hook_cancello(json.dumps(ev))
        return codice, err.getvalue()


class TestCancello(_BaseCancello):
    def test_la_catena_scritta_si_legge_in_ordine(self) -> None:
        self.assertEqual(ia.catena_scritta(ISTRUZIONI),
                         ["integratore-dm", "regolista", "autore-documenti"])
        self.assertEqual(ia.catena_scritta("- **Catena:** cartografo, poi custode-canone"),
                         ["cartografo", "custode-canone"])
        self.assertEqual(ia.catena_scritta("nessuna riga di quel tipo"), [])

    def test_la_catena_entra_nel_contesto(self) -> None:
        self.assertIn("integratore-dm", self._istruzioni())

    def test_push_senza_la_catena_si_blocca(self) -> None:
        self._istruzioni()
        codice, err = self._push([_uso_agente("integratore-dm")])
        self.assertEqual(codice, 2)
        self.assertIn("regolista", err)
        self.assertIn("--deroga", err)

    def test_push_con_la_catena_passa(self) -> None:
        self._istruzioni()
        righe = [_uso_agente(a) for a in ("integratore-dm", "regolista", "autore-documenti")]
        self.assertEqual(self._push(righe)[0], 0)

    def test_autore_documenti_serve_anche_se_la_catena_non_lo_nomina(self) -> None:
        self._istruzioni("Catena: cartografo\n")
        codice, err = self._push([_uso_agente("cartografo")])
        self.assertEqual(codice, 2)
        self.assertIn("autore-documenti", err)

    def test_pr_via_mcp_e_gh_si_controllano(self) -> None:
        self._istruzioni()
        self.assertEqual(self._push([], strumento="mcp__github__create_pull_request")[0], 2)
        self.assertEqual(self._push([], comando="gh pr ready 510")[0], 2)

    def test_il_push_con_opzioni_globali_si_riconosce(self) -> None:
        self._istruzioni()
        self.assertEqual(self._push([], comando="git -C /x push -q")[0], 2)

    def test_altri_comandi_non_si_toccano(self) -> None:
        self._istruzioni()
        self.assertEqual(self._push([], comando="git status && git log")[0], 0)
        citato = "python3 - <<'EOF'\nx = re.compile(r'git push')\nEOF"
        self.assertEqual(self._push([], comando=citato)[0], 0)
        self.assertEqual(self._push([], comando="git add -A && timeout 300 git push -q")[0], 2)

    def test_senza_catena_scritta_non_blocca_mai(self) -> None:
        self._istruzioni("aggiungi un sottocomando a dm.py")  # solo riconosciuto
        self.assertEqual(self._push([])[0], 0)

    def test_la_deroga_scritta_fa_passare_e_resta_nel_registro(self) -> None:
        self._istruzioni()
        deroga = _bash('python3 scripts/instradamento_agenti.py --deroga '
                       '"solo una risposta, nessun file cambiato"')
        self.assertEqual(self._push([deroga])[0], 0)
        self.assertEqual(ia.riepilogo(ia.REGISTRO)["push in deroga"], 1)

    def test_una_deroga_senza_motivo_non_vale(self) -> None:
        self._istruzioni()
        self.assertEqual(self._push([_bash('python3 scripts/instradamento_agenti.py --deroga "no"')])[0], 2)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(ia.main(["--deroga", "no"]), 1)

    def test_dentro_un_sottoagente_non_si_controlla(self) -> None:
        self._istruzioni()
        ev = {"tool_name": "Bash", "tool_input": {"command": "git push"}, "session_id": "s1",
              "agent_id": "a1"}
        self.assertEqual(ia.hook_cancello(json.dumps(ev)), 0)

    def test_input_rotto_non_blocca(self) -> None:
        self.assertEqual(ia.hook_cancello("non è json"), 0)


def _avvio(testo: str = ISTRUZIONI) -> dict:
    """Il primo messaggio di un thread, come lo scrive la trascrizione."""
    return {"type": "user", "message": {"role": "user", "content": testo}}


def _risultato(testo: str) -> dict:
    return {"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "t1", "content": testo}]}}


class TestCatenaDallaTrascrizione(_BaseCancello):
    """L'hook del prompt non scatta sul primo messaggio del thread: la catena si
    legge dalla trascrizione (audit del 27/11/2026, §2)."""

    def test_catena_nel_primo_messaggio_e_nessun_agente_blocca(self) -> None:
        codice, err = self._push([_avvio()])
        self.assertEqual(codice, 2)
        self.assertIn("integratore-dm", err)

    def test_il_messaggio_di_avvio_marcato_meta_conta(self) -> None:
        # Così arriva davvero: contesto del progetto e nota del coordinatore in una
        # riga isMeta, che l'hook UserPromptSubmit non vede.
        nota = ('<session-context>regole</session-context>\n<relay from="coordinator">\n'
                "  <note>\n      Tipo di lavoro: hook.\n"
                "      Catena: sviluppatore → autore-documenti\n  </note>\n</relay>")
        riga = {"type": "user", "isMeta": True, "message": {"role": "user", "content": nota}}
        codice, err = self._push([riga, _uso_agente("sviluppatore")])
        self.assertEqual(codice, 2)
        self.assertIn("autore-documenti", err)

    def test_un_sottoagente_nella_trascrizione_non_scrive_la_catena(self) -> None:
        riga = dict(_avvio(), isSidechain=True)
        self.assertEqual(self._push([riga])[0], 0)

    def test_catena_nel_primo_messaggio_a_blocchi_di_testo(self) -> None:
        riga = {"type": "user", "message": {"role": "user", "content": [
            {"type": "text", "text": ISTRUZIONI}]}}
        self.assertEqual(self._push([riga])[0], 2)

    def test_catena_nel_primo_messaggio_con_gli_agenti_chiamati_passa(self) -> None:
        righe = [_avvio("Correggi lo script.\nCatena: sviluppatore → autore-documenti\n"),
                 _uso_agente("sviluppatore"), _uso_agente("autore-documenti")]
        self.assertEqual(self._push(righe)[0], 0)

    def test_la_catena_dentro_un_tool_result_non_conta(self) -> None:
        righe = [_avvio("leggi la guida del coordinatore"),
                 _risultato("Esempio:\nCatena: cartografo → custode-canone\n")]
        self.assertEqual(self._push(righe)[0], 0)
        reg = [json.loads(r) for r in ia.REGISTRO.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(reg[-1].get("motivo"), "nessuna catena scritta nelle istruzioni")

    def test_vale_l_ultima_catena_scritta(self) -> None:
        righe = [_avvio("Catena: cartografo\n"), _uso_agente("cartografo"),
                 _avvio("Catena: sviluppatore → autore-documenti\n"),
                 _uso_agente("sviluppatore")]
        codice, err = self._push(righe)
        self.assertEqual(codice, 2)
        self.assertIn("autore-documenti", err)
        self.assertNotIn("cartografo", err.split("manca")[-1])

    def test_il_registro_vince_sulla_trascrizione(self) -> None:
        self._istruzioni("Catena: cartografo\n")
        righe = [_avvio("Catena: sviluppatore\n"), _uso_agente("cartografo"),
                 _uso_agente("autore-documenti")]
        self.assertEqual(self._push(righe)[0], 0)


class TestCancelloCanone(unittest.TestCase):
    """Il canone non si riscrive e non va su main (ADR-0007, ADR-0090): vale anche nei sottoagenti."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        p = mock.patch.object(ia, "REGISTRO", self.tmp / "reg.jsonl")
        p.start()
        self.addCleanup(p.stop)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def _esito(self, comando: str, **extra) -> int:
        ev = {"tool_name": "Bash", "tool_input": {"command": comando}, "session_id": "s9",
              "agent_id": "a1", **extra}
        with contextlib.redirect_stderr(io.StringIO()):
            return ia.hook_cancello(json.dumps(ev))

    def test_push_forzato_sul_ramo_di_gruppo_bloccato(self) -> None:
        for c in ("git push --force origin campaign-group-rumblingstone",
                  "git push -f origin HEAD:campaign-group-rumblingstone",
                  "git push -uf origin campaign-group-rumblingstone",
                  "git push --force-with-lease origin campaign-group-rumblingstone",
                  "git push origin +HEAD:campaign-group-rumblingstone",
                  "git push origin +campaign-group-rumblingstone",
                  "git push origin :campaign-group-rumblingstone",
                  "git push origin --delete campaign-group-rumblingstone",
                  "cd /x && timeout 60 git push -f origin refs/heads/campaign-group-x"):
            with self.subTest(comando=c):
                self.assertEqual(self._esito(c), 2)

    def test_push_normale_sul_ramo_di_gruppo_passa(self) -> None:
        self.assertEqual(self._esito("git push origin campaign-group-rumblingstone"), 0)
        self.assertEqual(self._esito("git push origin HEAD:campaign-group-rumblingstone"), 0)

    def test_push_forzato_altrove_non_e_affare_di_questo_cancello(self) -> None:
        self.assertEqual(self._esito("git push --force origin claude/project-thread-x"), 0)

    def test_push_forzato_senza_refspec_dal_ramo_di_gruppo(self) -> None:
        repo = self.tmp / "r"
        repo.mkdir()
        for args in (["init", "-q", "-b", "campaign-group-x"],):
            subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)
        self.assertEqual(self._esito("git push --force", cwd=str(repo)), 2)
        self.assertEqual(self._esito("git push", cwd=str(repo)), 0)

    def test_canone_verso_main_bloccato(self) -> None:
        for c in ("git add campaign/state.yaml && git commit -m x && git push origin main",
                  "git add campaign/sessions/2026-11-20_session-5.md; git commit -qm s; "
                  "git push origin HEAD:main",
                  "git push origin campaign-group-rumblingstone:main"):
            with self.subTest(comando=c):
                self.assertEqual(self._esito(c), 2)

    def test_prodotto_verso_main_passa(self) -> None:
        self.assertEqual(self._esito("git add scripts/x.py && git commit -m x && git push origin main"), 0)
        self.assertEqual(self._esito("git push origin main"), 0)

    def _repo_su(self, ramo: str) -> Path:
        repo = self.tmp / ramo
        repo.mkdir()
        subprocess.run(["git", "-C", str(repo), "init", "-q", "-b", ramo], check=True,
                       capture_output=True)
        return repo

    def test_i_giri_attorno_al_cancello(self) -> None:
        """I sette modi di aggirarlo trovati dal custode-canone il 2026-11-21."""
        repo = self._repo_su("campaign-group-x")
        altrove = self._repo_su("claude-thread")
        casi = ("git push --force origin HEAD",
                "git push origin +HEAD",
                "git push -f",
                f"git -C {repo} push -f origin campaign-group-rumblingstone",
                f"git -C {repo} push -f origin HEAD",
                "git -c push.default=current push --force origin campaign-group-x",
                "git --no-pager push -f origin campaign-group-x",
                "git push --mirror origin",
                "git push --all -f origin",
                "git push --tags --force origin",
                "sh -c 'git push -f origin campaign-group-x'",
                "bash -c \"git push origin +HEAD:campaign-group-x\"",
                "git push origin HEAD:main",
                "git push origin campaign-group-x:refs/heads/main",
                f"cd {repo} && git push --force origin HEAD",
                # secondo giro del custode-canone, 2026-11-26
                "git push origin '+refs/heads/*:refs/heads/*'",
                "git push origin 'refs/heads/*:refs/heads/*'",
                "git push --prune origin 'refs/heads/*:refs/heads/*'",
                "git push --prune origin main")
        for c in casi:
            with self.subTest(comando=c):
                self.assertEqual(self._esito(c, cwd=str(repo if "cd " not in c else altrove)), 2)

    def test_dal_ramo_di_thread_head_non_e_il_ramo_di_gruppo(self) -> None:
        altrove = self._repo_su("claude-thread")
        self.assertEqual(self._esito("git push --force origin HEAD", cwd=str(altrove)), 0)
        self.assertEqual(self._esito("git push origin HEAD:main", cwd=str(altrove)), 0)
        self.assertEqual(self._esito("git push --all origin", cwd=str(altrove)), 0)

    def test_ramo_morto_mai(self) -> None:
        morto = "campaign-group-rumblingstone-dm-gianfranco"
        self.assertEqual(self._esito(f"git push origin {morto}"), 2)
        self.assertEqual(self._esito(f"git push origin HEAD:{morto}"), 2)
        repo = self._repo_su(morto)
        self.assertEqual(self._esito("git push", cwd=str(repo)), 2)

    def _mcp(self, strumento: str, **inp) -> int:
        ev = {"tool_name": f"mcp__github__{strumento}", "tool_input": inp, "session_id": "s9"}
        with contextlib.redirect_stderr(io.StringIO()):
            return ia.hook_cancello(json.dumps(ev))

    def test_gli_strumenti_github_che_scrivono(self) -> None:
        morto = "campaign-group-rumblingstone-dm-gianfranco"
        for strumento in ("push_files", "create_or_update_file", "delete_file", "create_branch"):
            with self.subTest(strumento=strumento):
                self.assertEqual(self._mcp(strumento, branch=morto, path="x.md"), 2)
        self.assertEqual(self._mcp("push_files", branch="main",
                                   files=[{"path": "campaign/state.yaml", "content": "x"}]), 2)
        self.assertEqual(self._mcp("create_or_update_file", branch="main",
                                   path="campaign/sessions/2026-11-20_session-7.md"), 2)
        # un commit sopra il ramo vivo è un fast-forward per costruzione
        self.assertEqual(self._mcp("push_files", branch="campaign-group-rumblingstone",
                                   files=[{"path": "campaign/state.yaml", "content": "x"}]), 0)
        self.assertEqual(self._mcp("push_files", branch="main",
                                   files=[{"path": "scripts/x.py", "content": "x"}]), 0)

    def test_merge_e_aggiornamento_di_una_pr(self) -> None:
        from unittest import mock
        morto = "campaign-group-rumblingstone-dm-gianfranco"
        casi = {("merge_pull_request", ("main", "campaign-group-rumblingstone")): 2,
                ("merge_pull_request", (morto, "claude-x")): 2,
                ("merge_pull_request", ("main", "claude-x")): 0,
                ("merge_pull_request", ("campaign-group-rumblingstone", "claude-x")): 0,
                ("update_pull_request_branch", ("main", morto)): 2,
                ("update_pull_request_branch", ("main", "claude-x")): 0,
                ("merge_pull_request", None): 2,
                ("update_pull_request_branch", None): 2}
        for (strumento, rami), atteso in casi.items():
            with self.subTest(strumento=strumento, rami=rami), \
                    mock.patch.object(ia, "_rami_della_pr", return_value=rami):
                self.assertEqual(self._mcp(strumento, pullNumber=1, owner="o", repo="r"), atteso)

    def test_il_matcher_dell_hook_copre_gli_strumenti_controllati(self) -> None:
        import re as _re
        impostazioni = json.loads((ia.ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        matcher = [h["matcher"] for h in impostazioni["hooks"]["PreToolUse"]
                   if any("--cancello" in c["command"] for c in h["hooks"])][0]
        for strumento in ("Bash", *ia.PR_MCP, *ia.GITHUB_SCRIVE, *ia.GITHUB_PR_SCRIVE):
            with self.subTest(strumento=strumento):
                self.assertTrue(_re.fullmatch(f"(?:{matcher})", strumento), matcher)

    def test_il_blocco_resta_nel_registro(self) -> None:
        self._esito("git push -f origin campaign-group-rumblingstone")
        self.assertEqual(ia.riepilogo(ia.REGISTRO)["push bloccati"], 1)


class TestValutazione(unittest.TestCase):
    """Il set d'oro misura l'hook; --check è un cricchetto sul test (ADR-0154)."""

    CASI = [
        {"testo": "alfa", "atteso": "sviluppatore", "accettabili": [], "split": "dev"},
        {"testo": "beta", "atteso": "sviluppatore", "accettabili": [], "split": "dev"},
        {"testo": "gamma", "atteso": "regolista", "accettabili": [], "split": "dev"},
        {"testo": "delta", "atteso": "regolista", "accettabili": [], "split": "test"},
        {"testo": "epsilon", "atteso": "nessuno", "accettabili": [], "split": "test"},
        {"testo": "zeta", "atteso": "piattaforma", "accettabili": ["sviluppatore"],
         "split": "test"},
        {"testo": "eta", "atteso": "sviluppatore", "accettabili": [], "split": "test"},
    ]
    # La «scegli» finta: tutto giusto sul test tranne «zeta», che prende l'accettabile.
    RISPOSTE = {"alfa": ["sviluppatore"], "beta": ["regolista"], "gamma": ["regolista"],
                "delta": ["regolista"], "epsilon": [], "zeta": ["sviluppatore"],
                "eta": ["sviluppatore", "autore-documenti"]}

    def _scegli(self, testo: str) -> "list[str]":
        return list(self.RISPOSTE[testo])

    def _oro(self, tetto: dict) -> Path:
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d)
        p = d / "oro.json"
        p.write_text(json.dumps({"casi": self.CASI, "tetto": tetto}), encoding="utf-8")
        return p

    def _tetto_esatto(self) -> dict:
        v = ia.valuta(self._oro({}), scegli_=self._scegli, campioni=0)["test"]
        return {"giusti": v["giusti"], "giusti_indulgenti": v["giusti_indulgenti"],
                "macro_f1": v["macro_f1"]["frazione"]}

    def test_predizione_vuota_e_nessuno(self) -> None:
        self.assertEqual(ia.predici("epsilon", self._scegli), "nessuno")
        self.assertEqual(ia.predici("eta", self._scegli), "sviluppatore")

    def test_valuta_per_split_e_baseline_dal_dev(self) -> None:
        v = ia.valuta(self._oro({}), scegli_=self._scegli, campioni=0)
        self.assertEqual([v[s]["n"] for s in ("dev", "test", "tutto")], [3, 4, 7])
        self.assertEqual(v["test"]["giusti"], 3)
        self.assertEqual(v["test"]["giusti_indulgenti"], 4)
        # maggioritaria del dev: «sviluppatore» (2 su 3), applicata anche al test
        self.assertEqual(v["baseline"]["classe"], "sviluppatore")
        self.assertEqual(v["test"]["baseline"]["giusti"], 1)
        self.assertEqual(v["test"]["baseline"]["giusti_indulgenti"], 2)

    def test_check_passa_al_tetto(self) -> None:
        codice, _ = ia.controlla(self._oro(self._tetto_esatto()), scegli_=self._scegli)
        self.assertEqual(codice, 0)

    def test_check_boccia_una_regressione(self) -> None:
        p = self._oro(self._tetto_esatto())
        risposte = dict(self.RISPOSTE, delta=["sviluppatore"])  # un caso giusto diventa sbagliato
        codice, msg = ia.controlla(p, scegli_=lambda t: list(risposte[t]))
        self.assertEqual(codice, 1)
        self.assertIn("giusti", "\n".join(msg))
        # anche dalla riga di comando, con la scegli dell'hook sostituita
        with mock.patch.object(ia, "scegli", lambda t: list(risposte[t])), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ia.main(["--check", "--oro", str(p)]), 1)

    def test_check_avvisa_se_sale(self) -> None:
        tetto = self._tetto_esatto()
        tetto["giusti"] -= 1
        codice, msg = ia.controlla(self._oro(tetto), scegli_=self._scegli)
        self.assertEqual(codice, 0)
        self.assertIn("alza il tetto a mano", "\n".join(msg))

    def test_tetto_macro_f1_decimale(self) -> None:
        tetto = self._tetto_esatto()
        from fractions import Fraction
        tetto["macro_f1"] = str(round(float(Fraction(tetto["macro_f1"])) + 0.01, 4))
        codice, _ = ia.controlla(self._oro(tetto), scegli_=self._scegli)
        self.assertEqual(codice, 1)

    def test_check_senza_tetto_esce_1(self) -> None:
        p = self._oro({})
        codice, msg = ia.controlla(p, scegli_=self._scegli)
        self.assertEqual(codice, 1)

    def test_oro_del_repo_al_tetto_di_oggi(self) -> None:
        codice, msg = ia.controlla(ia.ORO)
        self.assertEqual(codice, 0, "\n".join(msg))
        self.assertNotIn("tetto a mano", "\n".join(msg))

    def test_oro_del_repo_numeri_di_oggi(self) -> None:
        # etichette confermate dal DM il 2026-11-27 (prima 18, 4, 4 e 107/1155)
        v = ia.valuta(ia.ORO, campioni=0)
        t = v["test"]
        self.assertEqual((t["n"], t["giusti"], t["giusti_indulgenti"]), (17, 4, 4))
        self.assertEqual(t["macro_f1"], {"frazione": "58/315", "valore": 0.1841})
        self.assertEqual(t["baseline"]["giusti"], 2)
        # nel dev piattaforma e sviluppatore pareggiano 3 a 3: vince la prima di np.unique
        self.assertEqual(v["baseline"]["classe"], "piattaforma")
        self.assertNotIn("macro_f1_bootstrap95", t)

    def test_il_json_non_porta_il_bootstrap(self) -> None:
        # l'intervallo dipende dal generatore di numpy: solo nel rapporto di testo
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(ia.main(["--eval", "--json"]), 0)
        self.assertNotIn("bootstrap", buf.getvalue())
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(ia.main(["--eval"]), 0)
        self.assertIn("bootstrap 95%", buf.getvalue())

    def test_json_identico_fra_due_esecuzioni(self) -> None:
        uscite = []
        for _ in range(2):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.assertEqual(ia.main(["--eval", "--json"]), 0)
            uscite.append(buf.getvalue())
        self.assertEqual(uscite[0], uscite[1])
        d = json.loads(uscite[0])
        self.assertEqual(set(d) >= {"dev", "test", "tutto", "baseline"}, True)


class TestHookSenzaLibrerie(unittest.TestCase):
    """Gli hook girano a ogni messaggio: sklearn e scipy (un secondo d'import) restano fuori."""

    CODICE = r"""
import io, json, sys, tempfile
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import instradamento_agenti as ia
ia.REGISTRO = Path(tempfile.mkdtemp()) / "reg.jsonl"
ev = {"prompt": "aggiungi un sottocomando a dm.py", "session_id": "s-import",
      "tool_name": "Bash", "tool_input": {"command": "git push"}, "transcript_path": ""}
for flag in ("--prompt", "--stop", "--cancello"):
    sys.stdin = io.StringIO(json.dumps(ev))
    try:
        ia.main([flag])
    except SystemExit:
        pass
print("MODULI", sorted(m for m in ("sklearn", "scipy", "numpy") if m in sys.modules))
"""

    def test_prompt_stop_cancello_non_importano_sklearn(self) -> None:
        r = subprocess.run([sys.executable, "-c", self.CODICE, str(ia.ROOT / "scripts")],
                           capture_output=True, text=True, cwd=ia.ROOT, check=True)
        riga = [x for x in r.stdout.splitlines() if x.startswith("MODULI")]
        self.assertEqual(riga, ["MODULI []"], r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
