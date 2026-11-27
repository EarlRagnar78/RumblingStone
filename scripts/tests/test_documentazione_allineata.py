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

import shutil
import tempfile
import unittest

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


def _repo(tmp_path: Path) -> "tuple[Path, str]":
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


class _ConCartella(unittest.TestCase):
    """Una cartella temporanea per test, tolta alla fine."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)


def _esegui(*argv: str) -> "tuple[int, str]":
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        codice = da.main(list(argv))
    return codice, out.getvalue()


class TestRispettoAEDebito(_ConCartella):
    """--rispetto-a e --debito in un repo git temporaneo."""

    def setUp(self) -> None:
        super().setUp()
        self.repo = _repo(self.tmp)

    def test_agente_e_script_nuovi_non_citati_fermano(self) -> None:
        repo = self.repo
        r, base = repo
        _scrivi(r, ".claude/agents/nuovo-agente.md", "---\nname: nuovo-agente\n---\n")
        _scrivi(r, "scripts/nuovo.py", "print()\n")
        _commit(r, "struttura nuova")
        codice, out = _esegui("--rispetto-a", base, "--radice", str(r))
        assert codice == 1
        assert ".claude/agents/nuovo-agente.md" in out and "AGENTS.md" in out
        assert "scripts/nuovo.py" in out and "docs/INDEX.md" in out
        assert "autore-documenti" in out

    def test_struttura_nuova_citata_passa(self) -> None:
        repo = self.repo
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

    def test_un_file_fuori_dalla_struttura_non_conta(self) -> None:
        repo = self.repo
        r, base = repo
        _scrivi(r, "plans/x.json", "{}\n")
        _scrivi(r, "scripts/tests/test_nuovo.py", "def test(): pass\n")
        _scrivi(r, "scripts/lib/aiuto.py", "x = 1\n")
        _commit(r, "file non strutturali")
        assert _esegui("--rispetto-a", base, "--radice", str(r))[0] == 0

    def test_il_nome_si_cerca_intero(self) -> None:
        repo = self.repo
        # «nuovo-agente-bis» citato non vale per «nuovo-agente».
        r, base = repo
        _scrivi(r, ".claude/agents/nuovo-agente.md", "x\n")
        _scrivi(r, "AGENTS.md", "Agenti: `vecchio-agente`, `nuovo-agente-bis`.\n")
        _commit(r, "agente citato male")
        assert _esegui("--rispetto-a", base, "--radice", str(r))[0] == 1

    def test_hook_nuovo_non_citato_ferma(self) -> None:
        repo = self.repo
        r, base = repo
        d = json.loads(json.dumps(SETTINGS))
        d["hooks"]["Stop"] = [{"hooks": [
            {"type": "command", "command": "python3 $CLAUDE_PROJECT_DIR/scripts/vecchio.py --stop"}]}]
        _scrivi(r, ".claude/settings.json", json.dumps(d))
        _commit(r, "hook nuovo")
        codice, out = _esegui("--rispetto-a", base, "--radice", str(r))
        assert codice == 1
        assert "vecchio.py" in out and "GUIDA-CONFIGURAZIONE-CLAUDE.md" in out

    def test_hook_nuovo_citato_passa(self) -> None:
        repo = self.repo
        r, base = repo
        d = json.loads(json.dumps(SETTINGS))
        d["hooks"]["SessionStart"] = [{"hooks": [
            {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/avvio.sh"}]}]
        _scrivi(r, ".claude/settings.json", json.dumps(d))
        _scrivi(r, "docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md",
                "Hook: `vecchio_hook.py`, `avvio.sh`.\n")
        _commit(r, "hook nuovo e citato")
        assert _esegui("--rispetto-a", base, "--radice", str(r))[0] == 0

    def test_il_debito_vecchio_non_ferma_la_pr(self) -> None:
        repo = self.repo
        r, _ = repo
        _scrivi(r, "scripts/scordato.py", "print()\n")
        base = _commit(r, "debito vecchio")
        _scrivi(r, "plans/y.json", "{}\n")
        _commit(r, "lavoro che non tocca la struttura")
        assert _esegui("--rispetto-a", base, "--radice", str(r))[0] == 0

    def test_riferimento_inesistente_e_errore_d_uso(self) -> None:
        repo = self.repo
        r, _ = repo
        assert _esegui("--rispetto-a", "non-esiste", "--radice", str(r))[0] == 2

    def test_debito_in_json(self) -> None:
        repo = self.repo
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

    def test_debito_check_a_cricchetto(self) -> None:
        repo = self.repo
        r, _ = repo
        _scrivi(r, "scripts/scordato.py", "print()\n")
        _scrivi(r, "plans/debito-documentazione.json", json.dumps({"tetto": 1, "misurato": "t"}))
        _commit(r, "debito al tetto")
        assert _esegui("--debito", "--check", "--radice", str(r))[0] == 0
        _scrivi(r, "scripts/scordato2.py", "print()\n")
        codice, out = _esegui("--debito", "--check", "--radice", str(r))
        assert codice == 1
        assert "tetto" in out

    def test_l_adr_si_conta_con_validate_docs(self) -> None:
        """Una norma, un rilevatore: gli ADR fuori indice sono quelli di validate_docs."""
        import validate_docs as vd
        attesi = [x["path"] for x in vd.indice_adr()]
        assert da.adr_fuori_indice(da.ROOT) == attesi


# --- --attiva: la routine del lunedì chiama autore-documenti solo se serve ---

OGGI = "2026-11-27"


def _commit_il(radice: Path, data: str, messaggio: str = "x") -> str:
    """Un commit con la data scritta, per i conti a 14 e 30 giorni."""
    import os
    env = dict(os.environ, GIT_AUTHOR_DATE=f"{data}T12:00:00", GIT_COMMITTER_DATE=f"{data}T12:00:00")
    subprocess.run(["git", "-C", str(radice), "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", str(radice), "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-q", "-m", messaggio], check=True, env=env)
    return _git(radice, "rev-parse", "HEAD")


def _adr(radice: Path, n: int, data: str) -> None:
    _scrivi(radice, f"plans/adr/ADR-{n:04d}-titolo-{n}.md",
            f"# ADR-{n:04d} — titolo {n}\n\n**Data**: {data}\n")


def _allineato(tmp_path: Path) -> Path:
    """Un repo tutto in ordine il giorno OGGI: niente da attivare."""
    r = tmp_path / "allineato"
    r.mkdir()
    _git(r, "init", "-q")
    _scrivi(r, ".claude/agents/vecchio-agente.md", "x\n")
    _scrivi(r, "scripts/vecchio.py", "print()\n")
    _scrivi(r, ".github/workflows/ci.yml", "on: push\n")
    _scrivi(r, ".claude/settings.json", json.dumps(SETTINGS))
    _scrivi(r, "scripts/vecchio_hook.py", "print()\n")
    _adr(r, 1, "2026-10-01")
    _adr(r, 2, "2026-10-02")
    _scrivi(r, "AGENTS.md", "`vecchio-agente`\n")
    _scrivi(r, "docs/INDEX.md", "`vecchio.py` `vecchio_hook.py` `ci.yml`\n"
                                "[a](../plans/adr/ADR-0001-titolo-1.md) [b](../plans/adr/ADR-0002-titolo-2.md)\n")
    _scrivi(r, "docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md", "`vecchio_hook.py`\n")
    _scrivi(r, "docs/explanation/ARCHITETTURA.md", "ADR-0001, ADR-0002\n")
    _scrivi(r, "plans/debito-documentazione.json", json.dumps(
        {"tetto": 0, "misurato": "t", "token_per_attivazione": 174239, "token_fonte": "misura"}))
    _commit_il(r, "2026-10-02", "base")
    return r


def _attiva(r: Path) -> dict:
    codice, out = _esegui("--attiva", "--json", "--oggi", OGGI, "--radice", str(r))
    assert codice == 0
    return json.loads(out)


class TestAttiva(_ConCartella):
    """--attiva in un repo git temporaneo."""

    def setUp(self) -> None:
        super().setUp()
        self.allineato = _allineato(self.tmp)

    def test_attiva_tutto_in_ordine_non_attiva(self) -> None:
        allineato = self.allineato
        d = _attiva(allineato)
        assert d == {"attiva": False, "motivi": [], "lavoro": [], "stima_token": 0}

    def test_attiva_un_agente_scoperto_attiva(self) -> None:
        allineato = self.allineato
        r = allineato
        _scrivi(r, ".claude/agents/nuovo-agente.md", "x\n")
        _commit_il(r, "2026-11-26")
        d = _attiva(r)
        assert d["attiva"] is True
        assert d["stima_token"] == 174239
        assert any("agente" in m for m in d["motivi"])
        assert {"file": "AGENTS.md", "cosa": "citare `nuovo-agente` (.claude/agents/nuovo-agente.md)"} in d["lavoro"]

    def test_attiva_architettura_indietro_di_tre(self) -> None:
        allineato = self.allineato
        r = allineato
        for n in (3, 4, 5):
            _adr(r, n, "2026-11-26")
        _scrivi(r, "docs/INDEX.md", (r / "docs/INDEX.md").read_text() + "".join(
            f"[x](../plans/adr/ADR-{n:04d}-titolo-{n}.md)\n" for n in (3, 4, 5)))
        _commit_il(r, "2026-11-26")
        d = _attiva(r)
        assert d["attiva"] is True
        assert any("ARCHITETTURA" in m for m in d["motivi"])
        cose = [x["cosa"] for x in d["lavoro"] if x["file"] == "docs/explanation/ARCHITETTURA.md"]
        assert any("ADR-0003" in c and "ADR-0005" in c for c in cose)

    def test_attiva_un_adr_indietro_vecchio_attiva_uno_recente_no(self) -> None:
        allineato = self.allineato
        r = allineato
        _adr(r, 3, "2026-11-20")
        _scrivi(r, "docs/INDEX.md", (r / "docs/INDEX.md").read_text()
                + "[x](../plans/adr/ADR-0003-titolo-3.md)\n")
        # ARCHITETTURA toccata nel periodo, senza citare ADR-0003: vale solo l'età.
        _scrivi(r, "docs/explanation/ARCHITETTURA.md", "ADR-0001, ADR-0002, rivista\n")
        _commit_il(r, "2026-11-20")
        assert _attiva(r)["attiva"] is False          # 7 giorni
        _adr(r, 3, "2026-11-01")
        _commit_il(r, "2026-11-21")
        assert _attiva(r)["attiva"] is True           # 26 giorni

    def test_attiva_solo_script_vecchi_scoperti_non_attiva(self) -> None:
        allineato = self.allineato
        r = allineato
        _scrivi(r, "scripts/scordato.py", "print()\n")
        _scrivi(r, "scripts/scordato2.py", "print()\n")
        _scrivi(r, "docs/INDEX.md", (r / "docs/INDEX.md").read_text() + "\n")
        _scrivi(r, "plans/debito-documentazione.json", json.dumps(
            {"tetto": 2, "misurato": "t", "token_per_attivazione": 174239, "token_fonte": "misura"}))
        _commit_il(r, "2026-11-20")
        assert _attiva(r)["attiva"] is False

    def test_attiva_debito_oltre_il_tetto(self) -> None:
        allineato = self.allineato
        r = allineato
        _scrivi(r, "scripts/scordato.py", "print()\n")
        _scrivi(r, "docs/INDEX.md", (r / "docs/INDEX.md").read_text() + "\n")
        _commit_il(r, "2026-11-20")
        d = _attiva(r)
        assert d["attiva"] is True
        assert any("tetto" in m for m in d["motivi"])
        assert any("scordato.py" in x["cosa"] for x in d["lavoro"] if x["file"] == "docs/INDEX.md")

    def test_attiva_indice_fermo_da_30_giorni_con_struttura_nuova(self) -> None:
        allineato = self.allineato
        # Uno script aggiunto 10 giorni fa, docs/INDEX.md fermo dal 2 ottobre: anche
        # sotto il tetto (alzato a 1) serve un'occhiata all'indice.
        r = allineato
        _scrivi(r, "plans/debito-documentazione.json", json.dumps(
            {"tetto": 1, "misurato": "t", "token_per_attivazione": 174239, "token_fonte": "misura"}))
        _scrivi(r, "scripts/nuovo.py", "print()\n")
        _commit_il(r, "2026-11-17")
        d = _attiva(r)
        assert d["attiva"] is True
        assert any("docs/INDEX.md" in m and "30 giorni" in m for m in d["motivi"])

    def test_attiva_testo_dice_il_motivo(self) -> None:
        allineato = self.allineato
        _scrivi(allineato, ".claude/agents/nuovo-agente.md", "x\n")
        _commit_il(allineato, "2026-11-26")
        codice, out = _esegui("--attiva", "--oggi", OGGI, "--radice", str(allineato))
        assert codice == 0
        assert "autore-documenti" in out and "AGENTS.md" in out
