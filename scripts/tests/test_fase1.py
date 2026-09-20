"""La sesta regola d'oro, provata all'indietro.

Un cancello che non si e' mai visto bocciare non e' un cancello: e' una
speranza con un exit code. Questi test lo fanno bocciare apposta, e poi
verificano che i quattro passi non siano vuoti sul repo vero.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FASE1 = ROOT / "scripts" / "fase1.py"


def corri(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(FASE1), *args],
                          capture_output=True, text=True, cwd=ROOT)


def test_su_un_file_vivo_esce_zero():
    r = corri("--check", "plans/INDEX.md")
    assert r.returncode == 0, r.stdout + r.stderr


def test_su_un_archivio_dichiarato_morde():
    """Il difetto vero del 2026-09-20: nove box contati dentro uno snapshot."""
    snap = next(ROOT.rglob("_SNAPSHOT-STORICO.md"), None)
    assert snap is not None, "il repo non ha piu' nessuno snapshot dichiarato"
    bersaglio = next(f for f in sorted(snap.parent.glob("*.md"))
                     if f.name != "_SNAPSHOT-STORICO.md")
    r = corri("--check", str(bersaglio.relative_to(ROOT)))
    assert r.returncode == 1, "un archivio dichiarato deve far uscire 1"
    assert "archivi dichiarati" in r.stdout


def test_un_modello_che_non_pesca_niente_e_rumoroso():
    """La lezione di `misura_craft.espandi`: uno zero muto e' peggio di un errore."""
    r = corri("cartella-che-non-esiste/**/*.md")
    assert r.returncode != 0
    assert "non pesca niente" in (r.stdout + r.stderr)


def test_i_quattro_passi_ci_sono_tutti():
    r = corri("plans/INDEX.md")
    for passo in ("1 · IL REGISTRO DELLE NORME",
                  "2 · L'ALGORITMO A STRATI",
                  "3 · I DATI CHE IL REPO GIA' POSSIEDE",
                  "4 · LE MISURE DI OGGI"):
        assert passo in r.stdout, f"passo mancante: {passo}"


def test_nessun_passo_torna_vuoto_sul_repo_vero():
    """Un passo vuoto e' un bersaglio che nessun dato del repo conosce."""
    r = corri("07_il Portale Della Forgia Eterna/ARC07-DEF-4-*.md")
    assert "con un misuratore vero" in r.stdout
    assert "Nomi propri della campagna: **3" in r.stdout, "il registro dei nomi si e' svuotato"
    assert "box read-aloud" in r.stdout
    assert "L0 · CANONE" in r.stdout


def test_riconosce_il_registro_di_chi_legge():
    """ADR-0035: un bersaglio misto dichiara che sono due lotti, non uno."""
    r = corri("plans/INDEX.md", "07_il Portale Della Forgia Eterna/ARC07-DEF-4-*.md")
    assert "parlano al TAVOLO" in r.stdout
    assert "parlano al REPO" in r.stdout
    assert "due lotti" in r.stdout


def test_la_sesta_regola_nomina_un_comando_che_esiste():
    """ADR-0053 applicata ad `AGENTS.md`: un rimando inventato e' un difetto."""
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "scripts/fase1.py" in agents, "la sesta regola non nomina il suo comando"
    assert FASE1.exists()
