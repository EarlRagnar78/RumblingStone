"""La documentazione segue la struttura (ADR-0153): un agente, uno script, un
workflow o un hook nuovo è citato nel suo indice, o la PR si ferma.

Tutti i casi girano in un repo git temporaneo: niente si scrive nel repo vero.
"""
from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import documentazione_allineata as da  # noqa: E402

SETTINGS = {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
    {"type": "command", "command": "python3 $CLAUDE_PROJECT_DIR/scripts/vecchio_hook.py --hook"}]}]}}


def _git(radice: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(radice), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def _scrivi(radice: Path, percorso: str, testo: str) -> None:
    p = radice / percorso
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(testo, encoding="utf-8")


def _commit(radice: Path, messaggio: str) -> str:
    _git(radice, "add", "-A")
    _git(radice, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", messaggio)
    return _git(radice, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path: Path) -> "tuple[Path, str]":
    """Un repo con un agente, uno script, un workflow e un hook già citati."""
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _scrivi(r, ".claude/agents/vecchio-agente.md", "---\nname: vecchio-agente\n---\n")
    _scrivi(r, "scripts/vecchio.py", "print()\n")
    _scrivi(r, "scripts/vecchio_hook.py", "print()\n")
    _scrivi(r, ".github/workflows/ci.yml", "on: push\n")
    _scrivi(r, ".claude/settings.json", json.dumps(SETTINGS))
    _scrivi(r, "AGENTS.md", "Agenti: `vecchio-agente`.\n")
    _scrivi(r, "docs/INDEX.md", "`vecchio.py`, `vecchio_hook.py`, `ci.yml`\n")
    _scrivi(r, "docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md", "Hook: `vecchio_hook.py`.\n")
    return r, _commit(r, "base")


def _esegui(*argv: str) -> "tuple[int, str]":
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        codice = da.main(list(argv))
    return codice, out.getvalue()


def test_agente_e_script_nuovi_non_citati_fermano(repo) -> None:
    r, base = repo
    _scrivi(r, ".claude/agents/nuovo-agente.md", "---\nname: nuovo-agente\n---\n")
    _scrivi(r, "scripts/nuovo.py", "print()\n")
    _commit(r, "struttura nuova")
    codice, out = _esegui("--rispetto-a", base, "--radice", str(r))
    assert codice == 1
    assert ".claude/agents/nuovo-agente.md" in out and "AGENTS.md" in out
    assert "scripts/nuovo.py" in out and "docs/INDEX.md" in out
    assert "autore-documenti" in out


def test_struttura_nuova_citata_passa(repo) -> None:
    r, base = repo
    _scrivi(r, ".claude/agents/nuovo-agente.md", "---\nname: nuovo-agente\n---\n")
    _scrivi(r, "scripts/nuovo.py", "print()\n")
    _scrivi(r, "scripts/lancia.sh", "true\n")
    _scrivi(r, ".github/workflows/notte.yml", "on: schedule\n")
    _scrivi(r, "AGENTS.md", "Agenti: `vecchio-agente`, `nuovo-agente`.\n")
    _scrivi(r, "docs/INDEX.md", "`vecchio.py`, `vecchio_hook.py`, `ci.yml`, "
                                "`nuovo.py`, `lancia.sh`, `notte.yml`\n")
    _commit(r, "struttura nuova e citata")
    assert _esegui("--rispetto-a", base, "--radice", str(r))[0] == 0


def test_un_file_fuori_dalla_struttura_non_conta(repo) -> None:
    r, base = repo
    _scrivi(r, "plans/x.json", "{}\n")
    _scrivi(r, "scripts/tests/test_nuovo.py", "def test(): pass\n")
    _scrivi(r, "scripts/lib/aiuto.py", "x = 1\n")
    _commit(r, "file non strutturali")
    assert _esegui("--rispetto-a", base, "--radice", str(r))[0] == 0


def test_il_nome_si_cerca_intero(repo) -> None:
    # «nuovo-agente-bis» citato non vale per «nuovo-agente».
    r, base = repo
    _scrivi(r, ".claude/agents/nuovo-agente.md", "x\n")
    _scrivi(r, "AGENTS.md", "Agenti: `vecchio-agente`, `nuovo-agente-bis`.\n")
    _commit(r, "agente citato male")
    assert _esegui("--rispetto-a", base, "--radice", str(r))[0] == 1


def test_hook_nuovo_non_citato_ferma(repo) -> None:
    r, base = repo
    d = json.loads(json.dumps(SETTINGS))
    d["hooks"]["Stop"] = [{"hooks": [
        {"type": "command", "command": "python3 $CLAUDE_PROJECT_DIR/scripts/vecchio.py --stop"}]}]
    _scrivi(r, ".claude/settings.json", json.dumps(d))
    _commit(r, "hook nuovo")
    codice, out = _esegui("--rispetto-a", base, "--radice", str(r))
    assert codice == 1
    assert "vecchio.py" in out and "GUIDA-CONFIGURAZIONE-CLAUDE.md" in out


def test_hook_nuovo_citato_passa(repo) -> None:
    r, base = repo
    d = json.loads(json.dumps(SETTINGS))
    d["hooks"]["SessionStart"] = [{"hooks": [
        {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/avvio.sh"}]}]
    _scrivi(r, ".claude/settings.json", json.dumps(d))
    _scrivi(r, "docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md",
            "Hook: `vecchio_hook.py`, `avvio.sh`.\n")
    _commit(r, "hook nuovo e citato")
    assert _esegui("--rispetto-a", base, "--radice", str(r))[0] == 0


def test_il_debito_vecchio_non_ferma_la_pr(repo) -> None:
    r, _ = repo
    _scrivi(r, "scripts/scordato.py", "print()\n")
    base = _commit(r, "debito vecchio")
    _scrivi(r, "plans/y.json", "{}\n")
    _commit(r, "lavoro che non tocca la struttura")
    assert _esegui("--rispetto-a", base, "--radice", str(r))[0] == 0


def test_riferimento_inesistente_e_errore_d_uso(repo) -> None:
    r, _ = repo
    assert _esegui("--rispetto-a", "non-esiste", "--radice", str(r))[0] == 2


def test_debito_in_json(repo) -> None:
    r, _ = repo
    _scrivi(r, "scripts/scordato.py", "print()\n")
    _scrivi(r, ".claude/agents/agente-scordato.md", "x\n")
    _scrivi(r, "plans/adr/ADR-0001-primo.md", "# ADR\n")
    _scrivi(r, "plans/adr/ADR-0002-secondo.md", "# ADR\n")
    _scrivi(r, "docs/explanation/ARCHITETTURA.md", "Vedi ADR-0001.\n")
    _commit(r, "debito")
    codice, out = _esegui("--debito", "--json", "--radice", str(r))
    assert codice == 0
    d = json.loads(out)
    percorsi = {s["percorso"] for s in d["scoperti"]}
    assert percorsi == {"scripts/scordato.py", ".claude/agents/agente-scordato.md"}
    assert {s["tipo"] for s in d["scoperti"]} == {"script", "agente"}
    assert len(d["adr_fuori_indice"]) == 2
    assert d["totale"] == 4
    assert d["architettura"] == {"ultimo_adr_citato": "0001", "ultimo_adr": "0002"}


def test_debito_check_a_cricchetto(repo) -> None:
    r, _ = repo
    _scrivi(r, "scripts/scordato.py", "print()\n")
    _scrivi(r, "plans/debito-documentazione.json", json.dumps({"tetto": 1, "misurato": "t"}))
    _commit(r, "debito al tetto")
    assert _esegui("--debito", "--check", "--radice", str(r))[0] == 0
    _scrivi(r, "scripts/scordato2.py", "print()\n")
    codice, out = _esegui("--debito", "--check", "--radice", str(r))
    assert codice == 1
    assert "tetto" in out


def test_l_adr_si_conta_con_validate_docs() -> None:
    """Una norma, un rilevatore: gli ADR fuori indice sono quelli di validate_docs."""
    import validate_docs as vd
    attesi = [x["path"] for x in vd.indice_adr()]
    assert da.adr_fuori_indice(da.ROOT) == attesi
