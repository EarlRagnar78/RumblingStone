"""Gli agenti di `.claude/agents/`: tre classi, skill che esistono, verificatori in sola lettura (ADR-0146)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import vincolo_skill as vs  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AGENTI = sorted((ROOT / ".claude" / "agents").glob("*.md"))
CLASSI = {"Autori", "Tecnici", "Verificatori"}
SKILL = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}


def _frontmatter(f: Path) -> "dict[str, str]":
    m = re.match(r"---\n(.*?)\n---", f.read_text(encoding="utf-8"), re.S)
    assert m, f"{f.name}: manca il frontmatter"
    return dict(re.findall(r"^(\w+): ?(.*)$", m.group(1), re.M))


def test_sono_dieci():
    assert len(AGENTI) == 10, [f.name for f in AGENTI]


@pytest.mark.parametrize("f", AGENTI, ids=lambda f: f.stem)
def test_nome_descrizione_classe(f):
    fm = _frontmatter(f)
    assert fm["name"] == f.stem
    assert len(fm["description"]) > 40
    classe = re.search(r"<!-- Classe: (\w+)", f.read_text(encoding="utf-8"))
    assert classe and classe.group(1) in CLASSI


@pytest.mark.parametrize("f", AGENTI, ids=lambda f: f.stem)
def test_le_skill_precaricate_esistono(f):
    precaricate = vs.precaricate(f.stem)
    assert precaricate, f"{f.name}: nessuna skill precaricata"
    assert precaricate <= SKILL, precaricate - SKILL


def test_i_verificatori_non_scrivono():
    for f in AGENTI:
        if "Classe: Verificatori" in f.read_text(encoding="utf-8"):
            strumenti = _frontmatter(f).get("tools", "")
            assert strumenti, f"{f.name}: un verificatore elenca i suoi strumenti"
            assert not re.search(r"\b(Edit|Write|MultiEdit|NotebookEdit)\b", strumenti), f.name


def test_le_due_prose_non_si_mescolano():
    """narrative-style e prosa-documenti sono mutuamente esclusive (ADR-0035)."""
    for f in AGENTI:
        s = vs.precaricate(f.stem)
        assert not {"rumblingstone-narrative-style", "rumblingstone-prosa-documenti"} <= s, f.name


def test_l_agente_nominato_dall_hook_precarica_la_skill_di_prosa():
    assert vs.SKILL_PROSA in vs.precaricate("autore-prosa-gioco")


def test_ogni_skill_obbligatoria_ha_un_agente():
    """L0, L1 e L2 di ORCHESTRAZIONE: nessuna resta senza un agente che la carica."""
    obbligatorie = {"rumblingstone-campaign", "rumblingstone-narrative-style",
                    "rumblingstone-prosa-documenti", "rumblingstone-indagine",
                    "rumblingstone-module-standard", "npc-villain-boosting"}
    coperte = set().union(*(vs.precaricate(f.stem) for f in AGENTI))
    # l'indagine si carica su richiesta dall'autore della prosa: lo dice il suo corpo
    assert "rumblingstone-indagine" in (ROOT / ".claude/agents/autore-prosa-gioco.md").read_text(
        encoding="utf-8")
    assert obbligatorie - coperte == {"rumblingstone-indagine"}
