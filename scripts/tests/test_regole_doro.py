"""Il cancello sulle regole d'oro, provato all'indietro.

Ogni test sabota la tabella in un modo diverso e verifica che il gate se ne
accorga. Un cancello che non si e' mai visto bocciare non e' un cancello.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_skills as vs  # noqa: E402


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """Una copia minima del repo: solo cio' che il controllo guarda."""
    (tmp_path / "skills").mkdir()
    (tmp_path / "scripts").mkdir()
    for nome in ("fase1.py", "misura_craft.py", "validate_skills.py",
                 "validate_norme_editoriali.py"):
        (tmp_path / "scripts" / nome).write_text("", encoding="utf-8")
    shutil.copy(ROOT / "skills" / "REGOLE-DORO.md", tmp_path / "skills")
    shutil.copy(ROOT / "AGENTS.md", tmp_path / "AGENTS.md")
    return tmp_path


def riscrivi(repo: Path, prima: str, dopo: str) -> None:
    f = repo / "skills" / "REGOLE-DORO.md"
    t = f.read_text(encoding="utf-8")
    assert prima in t, f"il fixture non contiene piu': {prima[:50]}"
    f.write_text(t.replace(prima, dopo, 1), encoding="utf-8")


def test_il_repo_vero_e_verde():
    assert vs.check_regole_doro(ROOT) == []


def test_la_copia_di_prova_e_verde(repo):
    """Senza questo, ogni test sotto proverebbe solo che il fixture e' rotto."""
    assert vs.check_regole_doro(repo) == []


def test_file_assente(tmp_path):
    (tmp_path / "skills").mkdir()
    errori = vs.check_regole_doro(tmp_path)
    assert errori and "assente" in errori[0]


def test_marcatore_rimosso(repo):
    riscrivi(repo, "<!-- regole-doro: tabella -->", "")
    errori = vs.check_regole_doro(repo)
    assert any("manca il marcatore" in e for e in errori)


def test_id_nudo_senza_la_lettera(repo):
    """Il difetto misurato: «4» significa tre cose diverse in AGENTS.md."""
    riscrivi(repo, "| **G4** |", "| **4** |")
    errori = vs.check_regole_doro(repo)
    assert any("non e' nella forma **G<numero>**" in e for e in errori)


def test_momento_inventato(repo):
    riscrivi(repo, "| **G2** | 🟨 DURANTE |", "| **G2** | 🟪 QUANDO CAPITA |")
    errori = vs.check_regole_doro(repo)
    assert any("momento" in e and "non previsto" in e for e in errori)


def test_comando_che_non_esiste(repo):
    """ADR-0053 applicata alle regole d'oro: un rimando inventato e' un difetto."""
    riscrivi(repo, "`python3 scripts/fase1.py <bersagli>`",
             "`python3 scripts/fase1_inesistente.py <bersagli>`")
    errori = vs.check_regole_doro(repo)
    assert any("non esiste" in e for e in errori)


def test_regola_senza_verificatore(repo):
    riscrivi(repo,
             "| **G3** | 🟥 DOPO | ho introdotto una **norma** nuova | la riga nel registro, con chi la misura | [`skills/REGISTRO-NORME-EDITORIALI.md`](REGISTRO-NORME-EDITORIALI.md) | `scripts/validate_norme_editoriali.py` |",
             "| **G3** | 🟥 DOPO | ho introdotto una **norma** nuova | la riga nel registro, con chi la misura | [`skills/REGISTRO-NORME-EDITORIALI.md`](REGISTRO-NORME-EDITORIALI.md) |  |")
    errori = vs.check_regole_doro(repo)
    assert any("nessun verificatore" in e for e in errori)


def test_id_duplicato_e_buco_nella_sequenza(repo):
    riscrivi(repo, "| **G1** |", "| **G2** |")
    errori = vs.check_regole_doro(repo)
    assert any("compare due volte" in e for e in errori)
    assert any("id mancanti" in e for e in errori)


def test_conflitto_senza_verdetto(repo):
    riscrivi(repo, "| **R1** | **G5 vs G1** | **G5 prima** |",
             "| **R1** | **G5 vs G1** |  |")
    errori = vs.check_regole_doro(repo)
    assert any("nessun verdetto" in e for e in errori)


def test_il_ponte_con_la_narrazione(repo):
    """Una regola nella tabella e non in AGENTS.md e' una regola senza il perche'."""
    agents = repo / "AGENTS.md"
    agents.write_text(agents.read_text(encoding="utf-8").replace("`G6`", "`GX`"),
                      encoding="utf-8")
    errori = vs.check_regole_doro(repo)
    assert any("G6" in e and "narrazione" in e for e in errori)


def test_ogni_regola_ha_un_momento_e_il_ciclo_e_completo():
    """I tre momenti esistono tutti: un ciclo con un buco non e' un ciclo."""
    t = (ROOT / "skills" / "REGOLE-DORO.md").read_text(encoding="utf-8")
    for momento in vs.MOMENTI:
        assert momento in t, f"nessuna regola nel momento {momento}"
