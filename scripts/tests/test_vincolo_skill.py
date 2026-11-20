"""Prove dell'hook che vincola le scritture di prosa alla skill giusta (ADR-0146)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import vincolo_skill as vs  # noqa: E402

BOX = "> *Il vento porta odore di cenere dalla valle.*\n"
STATBLOCK = "**CA** 18 (+2 Des, +6 armatura)\n**pf** 45 (6d10+12)\n"


def _trascrizione(tmp_path: Path, righe: "list[dict]") -> Path:
    t = tmp_path / "sessione.jsonl"
    t.write_text("\n".join(json.dumps(r) for r in righe) + "\n", encoding="utf-8")
    return t


def _skill(nome: str) -> dict:
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": nome}}]}}


def _lettura(percorso: str) -> dict:
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Read", "input": {"file_path": percorso}}]}}


def _evento(t: Path, file: str, testo: str, tool: str = "Edit", **extra) -> dict:
    inp = {"file_path": str(vs.ROOT / file)}
    if tool == "Write":
        inp["content"] = testo
    else:
        inp["new_string"] = testo
    return {"hook_event_name": "PreToolUse", "tool_name": tool,
            "tool_input": inp, "transcript_path": str(t), **extra}


class TestClasse:
    def test_introduzione_del_volume_e_prosa(self):
        f = "07_il Portale Della Forgia Eterna/homebrew/volume-arco/00-INTRO-VOLUME.md"
        assert vs.classe(f) == "prosa"

    def test_handout_e_prosa(self):
        assert vs.classe("07_il Portale Della Forgia Eterna/ARC07-HANDOUTS.md") == "prosa"

    def test_recap_e_prosa(self):
        assert vs.classe("campaign/recaps/recap-2026-05-05.md") == "prosa"

    def test_master_e_misto(self):
        assert vs.classe("07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md") == "misto"

    def test_scheda_del_bestiario_e_mista(self):
        assert vs.classe("Bestiario/mostri/hobgoblin-cr1.md") == "misto"

    def test_hb_generato_non_si_vincola(self):
        assert vs.classe("07_il Portale Della Forgia Eterna/homebrew/x/ARC07.hb.md") is None

    def test_archivio_non_si_vincola(self):
        assert vs.classe("09_Continuazione/_ARCHIVIO/vecchio.md") is None

    def test_adr_e_documento(self):
        assert vs.classe("plans/adr/ADR-0146-x.md") == "documento"

    def test_codice_non_si_vincola(self):
        assert vs.classe("scripts/misura_craft.py") is None


class TestDecisione:
    def test_prosa_senza_skill_si_blocca(self, tmp_path):
        t = _trascrizione(tmp_path, [])
        f = "07_il Portale Della Forgia Eterna/ARC07-HANDOUTS.md"
        d = vs.decidi(_evento(t, f, "Una lettera sigillata."))
        assert d["esito"] == "blocca"
        assert "rumblingstone-narrative-style" in d["motivo"]

    def test_prosa_con_skill_passa(self, tmp_path):
        t = _trascrizione(tmp_path, [_skill("rumblingstone-narrative-style")])
        f = "07_il Portale Della Forgia Eterna/ARC07-HANDOUTS.md"
        assert vs.decidi(_evento(t, f, "Una lettera."))["esito"] in ("passa", "ricorda")

    def test_skill_col_prefisso_del_repo_vale(self, tmp_path):
        t = _trascrizione(tmp_path, [_skill("RumblingStone:rumblingstone-narrative-style")])
        f = "campaign/recaps/recap-2026-05-05.md"
        assert vs.decidi(_evento(t, f, "Recap."))["esito"] != "blocca"

    def test_misto_senza_box_passa_senza_skill(self, tmp_path):
        t = _trascrizione(tmp_path, [])
        f = "Bestiario/mostri/hobgoblin-cr1.md"
        assert vs.decidi(_evento(t, f, STATBLOCK))["esito"] == "passa"

    def test_misto_con_box_si_blocca(self, tmp_path):
        t = _trascrizione(tmp_path, [])
        f = "Bestiario/mostri/hobgoblin-cr1.md"
        assert vs.decidi(_evento(t, f, BOX))["esito"] == "blocca"

    def test_write_con_box_si_blocca(self, tmp_path):
        t = _trascrizione(tmp_path, [])
        f = "07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md"
        assert vs.decidi(_evento(t, f, BOX, tool="Write"))["esito"] == "blocca"

    def test_references_non_letti_si_ricordano(self, tmp_path):
        t = _trascrizione(tmp_path, [_skill("rumblingstone-narrative-style")])
        f = "Bestiario/mostri/hobgoblin-cr1.md"
        d = vs.decidi(_evento(t, f, BOX))
        assert d["esito"] == "ricorda"
        assert "italiano-nativo.md" in d["motivo"]

    def test_references_letti_niente_promemoria(self, tmp_path):
        righe = [_skill("rumblingstone-narrative-style")] + [
            _lettura(f"/x/RumblingStone/skills/rumblingstone-narrative-style/references/{r}")
            for r in vs.REFERENCES_PROSA]
        t = _trascrizione(tmp_path, righe)
        f = "Bestiario/mostri/hobgoblin-cr1.md"
        assert vs.decidi(_evento(t, f, BOX))["esito"] == "passa"

    def test_documento_senza_skill_ricorda_non_blocca(self, tmp_path):
        t = _trascrizione(tmp_path, [])
        d = vs.decidi(_evento(t, "plans/adr/ADR-0146-x.md", "Contesto."))
        assert d["esito"] == "ricorda"
        assert "rumblingstone-prosa-documenti" in d["motivo"]

    def test_agente_con_skill_precaricata_passa(self, tmp_path, monkeypatch):
        agenti = tmp_path / "agents"
        agenti.mkdir()
        (agenti / "autore-prosa-gioco.md").write_text(
            "---\nname: autore-prosa-gioco\nskills:\n  - rumblingstone-narrative-style\n"
            "---\nCorpo.\n", encoding="utf-8")
        monkeypatch.setattr(vs, "AGENTI", agenti)
        t = _trascrizione(tmp_path, [])
        f = "07_il Portale Della Forgia Eterna/ARC07-HANDOUTS.md"
        ev = _evento(t, f, "Lettera.", agent_id="a1", agent_type="autore-prosa-gioco")
        assert vs.decidi(ev)["esito"] != "blocca"

    def test_agente_generico_senza_skill_si_blocca(self, tmp_path):
        t = _trascrizione(tmp_path, [])
        f = "07_il Portale Della Forgia Eterna/ARC07-HANDOUTS.md"
        ev = _evento(t, f, "Lettera.", agent_id="a1", agent_type="general-purpose")
        assert vs.decidi(ev)["esito"] == "blocca"

    def test_skill_caricata_dal_sottoagente_nella_sua_trascrizione(self, tmp_path):
        t = _trascrizione(tmp_path, [])
        sub = tmp_path / "sessione" / "subagents"
        sub.mkdir(parents=True)
        (sub / "agent-a1.jsonl").write_text(
            json.dumps(_skill("rumblingstone-narrative-style")) + "\n", encoding="utf-8")
        f = "07_il Portale Della Forgia Eterna/ARC07-HANDOUTS.md"
        ev = _evento(t, f, "Lettera.", agent_id="a1", agent_type="general-purpose")
        assert vs.decidi(ev)["esito"] != "blocca"

    def test_trascrizione_mancante_non_rompe(self, tmp_path):
        f = "07_il Portale Della Forgia Eterna/ARC07-HANDOUTS.md"
        d = vs.decidi(_evento(tmp_path / "manca.jsonl", f, "Lettera."))
        assert d["esito"] == "blocca"

    def test_file_fuori_dal_repo_passa(self, tmp_path):
        t = _trascrizione(tmp_path, [])
        ev = {"tool_name": "Write", "transcript_path": str(t),
              "tool_input": {"file_path": "/tmp/x/ARC07-HANDOUTS.md", "content": BOX}}
        assert vs.decidi(ev)["esito"] == "passa"


class TestUscitaDellHook:
    def test_blocco_esce_2_con_motivo_su_stderr(self, tmp_path, capsys, monkeypatch):
        monkeypatch.setattr(vs, "REGISTRO", tmp_path / "reg.jsonl")
        t = _trascrizione(tmp_path, [])
        ev = _evento(t, "07_il Portale Della Forgia Eterna/ARC07-HANDOUTS.md", "Lettera.")
        assert vs.esegui_hook(json.dumps(ev)) == 2
        assert "rumblingstone-narrative-style" in capsys.readouterr().err

    def test_promemoria_esce_0_con_contesto(self, tmp_path, capsys, monkeypatch):
        monkeypatch.setattr(vs, "REGISTRO", tmp_path / "reg.jsonl")
        t = _trascrizione(tmp_path, [])
        ev = _evento(t, "plans/adr/ADR-0146-x.md", "Contesto.")
        assert vs.esegui_hook(json.dumps(ev)) == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["hookEventName"] == "PreToolUse"
        assert "prosa-documenti" in out["hookSpecificOutput"]["additionalContext"]

    def test_ogni_decisione_vincolata_va_nel_registro(self, tmp_path, monkeypatch):
        reg = tmp_path / "reg.jsonl"
        monkeypatch.setattr(vs, "REGISTRO", reg)
        t = _trascrizione(tmp_path, [])
        vs.esegui_hook(json.dumps(_evento(t, "Bestiario/mostri/hobgoblin-cr1.md", STATBLOCK)))
        vs.esegui_hook(json.dumps(_evento(t, "Bestiario/mostri/hobgoblin-cr1.md", BOX)))
        righe = [json.loads(r) for r in reg.read_text(encoding="utf-8").splitlines()]
        assert [r["esito"] for r in righe] == ["passa", "blocca"]

    def test_input_rotto_non_blocca_mai(self, tmp_path, monkeypatch):
        monkeypatch.setattr(vs, "REGISTRO", tmp_path / "reg.jsonl")
        assert vs.esegui_hook("non è json") == 0

    def test_riepilogo_conta_gli_esiti(self, tmp_path):
        reg = tmp_path / "reg.jsonl"
        reg.write_text("\n".join(json.dumps(r) for r in [
            {"esito": "blocca", "classe": "prosa"},
            {"esito": "passa", "classe": "misto"},
            {"esito": "passa", "classe": "misto"}]) + "\n", encoding="utf-8")
        assert vs.riepilogo(reg) == {"blocca": 1, "passa": 2, "ricorda": 0}


def test_cambiati_tiene_solo_prosa_e_misti(monkeypatch):
    class R:
        stdout = "scripts/x.py\nplans/INDEX.md\ncampaign/recaps/r.md\nBestiario/mostri/a.md\n"
    import subprocess
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: R())
    assert vs.cambiati("origin/main") == ["campaign/recaps/r.md", "Bestiario/mostri/a.md"]


@pytest.mark.parametrize("modello", vs.PROSA_PURA)
def test_ogni_modello_di_prosa_pura_pesca_almeno_un_file(modello):
    """Un modello che non pesca niente si traveste da repo pulito (MS, diciottesimo caso)."""
    tutti = [p.relative_to(vs.ROOT).as_posix() for p in vs.ROOT.rglob("*.md")
             if ".git" not in p.parts]
    import re
    assert any(re.search(modello, f) for f in tutti), modello
