"""Il lavoro che entra in un thread trova il suo agente e la sua catena (ADR-0146)."""
from __future__ import annotations

import contextlib
import io
import json
import shutil
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
        }
        for testo, atteso in casi.items():
            with self.subTest(testo=testo):
                self.assertEqual(ia.scegli(testo)[:1], [atteso])

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

    def test_input_rotto_non_blocca(self) -> None:
        self.assertEqual(ia.hook_prompt("non è json"), 0)
        self.assertEqual(ia.hook_stop("non è json"), 0)

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
        self.assertEqual(ia.riepilogo(ia.REGISTRO), {"suggeriti": 1, "turni": 1, "seguiti": 1})

    def test_agenti_contati_solo_dopo_l_ultimo_messaggio(self) -> None:
        t = self.tmp / "t.jsonl"
        righe = [
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "cartografo"}}]}},
            {"type": "user", "message": {"content": "altro lavoro"}},
        ]
        t.write_text("".join(json.dumps(r) + "\n" for r in righe), encoding="utf-8")
        self.assertEqual(ia.agenti_chiamati(str(t)), [])


if __name__ == "__main__":
    unittest.main()
