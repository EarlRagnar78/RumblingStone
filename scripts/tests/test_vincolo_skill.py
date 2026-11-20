"""Prove dell'hook che vincola le scritture di prosa alla skill giusta (ADR-0146)."""
from __future__ import annotations

import contextlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import vincolo_skill as vs  # noqa: E402

BOX = "> *Il vento porta odore di cenere dalla valle.*\n"
STATBLOCK = "**CA** 18 (+2 Des, +6 armatura)\n**pf** 45 (6d10+12)\n"
HANDOUT = "07_il Portale Della Forgia Eterna/ARC07-HANDOUTS.md"
SCHEDA = "Bestiario/mostri/hobgoblin-cr1.md"


def _skill(nome: str) -> dict:
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": nome}}]}}


def _lettura(percorso: str) -> dict:
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Read", "input": {"file_path": percorso}}]}}


class _ConCartella(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        patcher = mock.patch.object(vs, "REGISTRO", self.tmp / "reg.jsonl")
        patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def trascrizione(self, righe: "list[dict]") -> Path:
        t = self.tmp / "sessione.jsonl"
        t.write_text("".join(json.dumps(r) + "\n" for r in righe), encoding="utf-8")
        return t

    @staticmethod
    def evento(t: Path, file: str, testo: str, tool: str = "Edit", **extra) -> dict:
        inp = {"file_path": str(vs.ROOT / file)}
        inp["content" if tool == "Write" else "new_string"] = testo
        return {"hook_event_name": "PreToolUse", "tool_name": tool,
                "tool_input": inp, "transcript_path": str(t), **extra}


class TestClasse(unittest.TestCase):
    def test_classi(self) -> None:
        attese = {
            "07_il Portale Della Forgia Eterna/homebrew/volume-arco/00-INTRO-VOLUME.md": "prosa",
            HANDOUT: "prosa",
            "campaign/recaps/recap-2026-05-05.md": "prosa",
            "07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md": "misto",
            SCHEDA: "misto",
            "07_il Portale Della Forgia Eterna/homebrew/x/ARC07.hb.md": None,
            "09_Continuazione/_ARCHIVIO/vecchio.md": None,
            "plans/adr/ADR-0146-x.md": "documento",
            "scripts/misura_craft.py": None,
        }
        for f, c in attese.items():
            with self.subTest(f=f):
                self.assertEqual(vs.classe(f), c)

    def test_ogni_modello_di_prosa_pura_pesca_almeno_un_file(self) -> None:
        """Un modello che non pesca niente si traveste da repo pulito."""
        tutti = [p.relative_to(vs.ROOT).as_posix() for p in vs.ROOT.rglob("*.md")
                 if ".git" not in p.parts]
        for modello in vs.PROSA_PURA:
            with self.subTest(modello=modello):
                self.assertTrue(any(re.search(modello, f) for f in tutti))


class TestDecisione(_ConCartella):
    def test_prosa_senza_skill_si_blocca(self) -> None:
        d = vs.decidi(self.evento(self.trascrizione([]), HANDOUT, "Una lettera sigillata."))
        self.assertEqual(d["esito"], "blocca")
        self.assertIn("rumblingstone-narrative-style", d["motivo"])

    def test_prosa_con_skill_passa_anche_col_prefisso_del_repo(self) -> None:
        for nome in ("rumblingstone-narrative-style", "RumblingStone:rumblingstone-narrative-style"):
            with self.subTest(nome=nome):
                t = self.trascrizione([_skill(nome)])
                self.assertNotEqual(vs.decidi(self.evento(t, HANDOUT, "Una lettera."))["esito"],
                                    "blocca")

    def test_comando_slash_vale_come_skill(self) -> None:
        riga = {"type": "user", "message": {"content":
                "<command-name>/rumblingstone-narrative-style</command-name>"}}
        t = self.trascrizione([riga])
        self.assertNotEqual(vs.decidi(self.evento(t, HANDOUT, "x"))["esito"], "blocca")

    def test_misto_senza_box_passa_senza_skill(self) -> None:
        d = vs.decidi(self.evento(self.trascrizione([]), SCHEDA, STATBLOCK))
        self.assertEqual(d["esito"], "passa")

    def test_misto_con_box_si_blocca_con_edit_e_con_write(self) -> None:
        for tool in ("Edit", "Write"):
            with self.subTest(tool=tool):
                d = vs.decidi(self.evento(self.trascrizione([]), SCHEDA, BOX, tool=tool))
                self.assertEqual(d["esito"], "blocca")

    def test_multiedit_con_box_si_blocca(self) -> None:
        ev = {"tool_name": "MultiEdit", "transcript_path": str(self.trascrizione([])),
              "tool_input": {"file_path": str(vs.ROOT / SCHEDA),
                             "edits": [{"old_string": "a", "new_string": BOX}]}}
        self.assertEqual(vs.decidi(ev)["esito"], "blocca")

    def test_references_non_letti_si_ricordano(self) -> None:
        t = self.trascrizione([_skill("rumblingstone-narrative-style")])
        d = vs.decidi(self.evento(t, SCHEDA, BOX))
        self.assertEqual(d["esito"], "ricorda")
        self.assertIn("italiano-nativo.md", d["motivo"])

    def test_references_letti_niente_promemoria(self) -> None:
        righe = [_skill("rumblingstone-narrative-style")] + [
            _lettura(f"/x/RumblingStone/skills/rumblingstone-narrative-style/references/{r}")
            for r in vs.REFERENCES_PROSA]
        d = vs.decidi(self.evento(self.trascrizione(righe), SCHEDA, BOX))
        self.assertEqual(d["esito"], "passa")

    def test_documento_senza_skill_ricorda_non_blocca(self) -> None:
        d = vs.decidi(self.evento(self.trascrizione([]), "plans/adr/ADR-0146-x.md", "Contesto."))
        self.assertEqual(d["esito"], "ricorda")
        self.assertIn("rumblingstone-prosa-documenti", d["motivo"])

    def test_agente_con_skill_precaricata_passa(self) -> None:
        agenti = self.tmp / "agents"
        agenti.mkdir()
        (agenti / "autore-prosa-gioco.md").write_text(
            "---\nname: autore-prosa-gioco\nskills:\n  - rumblingstone-narrative-style\n"
            "---\nCorpo.\n", encoding="utf-8")
        with mock.patch.object(vs, "AGENTI", agenti):
            ev = self.evento(self.trascrizione([]), HANDOUT, "Lettera.",
                             agent_id="a1", agent_type="autore-prosa-gioco")
            self.assertNotEqual(vs.decidi(ev)["esito"], "blocca")

    def test_agente_generico_senza_skill_si_blocca(self) -> None:
        ev = self.evento(self.trascrizione([]), HANDOUT, "Lettera.",
                         agent_id="a1", agent_type="general-purpose")
        self.assertEqual(vs.decidi(ev)["esito"], "blocca")

    def test_skill_caricata_dal_sottoagente_nella_sua_trascrizione(self) -> None:
        t = self.trascrizione([])
        sub = self.tmp / "sessione" / "subagents"
        sub.mkdir(parents=True)
        (sub / "agent-a1.jsonl").write_text(
            json.dumps(_skill("rumblingstone-narrative-style")) + "\n", encoding="utf-8")
        ev = self.evento(t, HANDOUT, "Lettera.", agent_id="a1", agent_type="general-purpose")
        self.assertNotEqual(vs.decidi(ev)["esito"], "blocca")

    def test_trascrizione_mancante_non_rompe(self) -> None:
        d = vs.decidi(self.evento(self.tmp / "manca.jsonl", HANDOUT, "Lettera."))
        self.assertEqual(d["esito"], "blocca")

    def test_file_fuori_dal_repo_passa(self) -> None:
        ev = {"tool_name": "Write", "transcript_path": str(self.trascrizione([])),
              "tool_input": {"file_path": "/tmp/x/ARC07-HANDOUTS.md", "content": BOX}}
        self.assertEqual(vs.decidi(ev)["esito"], "passa")


class TestUscitaDellHook(_ConCartella):
    def test_blocco_esce_2_con_motivo_su_stderr(self) -> None:
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            codice = vs.esegui_hook(json.dumps(self.evento(self.trascrizione([]), HANDOUT, "x")))
        self.assertEqual(codice, 2)
        self.assertIn("rumblingstone-narrative-style", err.getvalue())

    def test_promemoria_esce_0_con_contesto(self) -> None:
        out = io.StringIO()
        ev = self.evento(self.trascrizione([]), "plans/adr/ADR-0146-x.md", "Contesto.")
        with contextlib.redirect_stdout(out):
            self.assertEqual(vs.esegui_hook(json.dumps(ev)), 0)
        dato = json.loads(out.getvalue())["hookSpecificOutput"]
        self.assertEqual(dato["hookEventName"], "PreToolUse")
        self.assertIn("prosa-documenti", dato["additionalContext"])

    def test_ogni_decisione_vincolata_va_nel_registro(self) -> None:
        t = self.trascrizione([])
        with contextlib.redirect_stderr(io.StringIO()):
            vs.esegui_hook(json.dumps(self.evento(t, SCHEDA, STATBLOCK)))
            vs.esegui_hook(json.dumps(self.evento(t, SCHEDA, BOX)))
        righe = [json.loads(r) for r in vs.REGISTRO.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([r["esito"] for r in righe], ["passa", "blocca"])

    def test_input_rotto_non_blocca_mai(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(vs.esegui_hook("non è json"), 0)

    def test_riepilogo_conta_gli_esiti(self) -> None:
        reg = self.tmp / "r.jsonl"
        reg.write_text("".join(json.dumps({"esito": e}) + "\n"
                               for e in ("blocca", "passa", "passa")), encoding="utf-8")
        self.assertEqual(vs.riepilogo(reg), {"blocca": 1, "passa": 2, "ricorda": 0})

    def test_cambiati_tiene_solo_prosa_e_misti(self) -> None:
        uscita = mock.Mock(stdout="scripts/x.py\nplans/INDEX.md\ncampaign/recaps/r.md\n"
                                  "Bestiario/mostri/a.md\n")
        with mock.patch.object(subprocess, "run", return_value=uscita):
            self.assertEqual(vs.cambiati("origin/main"),
                             ["campaign/recaps/r.md", "Bestiario/mostri/a.md"])


if __name__ == "__main__":
    unittest.main()
