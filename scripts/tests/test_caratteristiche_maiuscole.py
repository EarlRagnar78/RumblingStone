"""La norma WotC sulle maiuscole, provata all'indietro.

Il punto di questi test non e' che il controllo passi: e' che **distingua**.
La ragione per cui la norma era stata archiviata come non misurabile e' che
*forza* e' anche un sostantivo comune, e un rilevatore che lo ignora segnala
piu' rumore che errori. Quindi meta' dei test verifica che il controllo
**taccia** dove deve tacere.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate_prosa.py"


def corri(tmp_path: Path, testo: str) -> subprocess.CompletedProcess:
    f = tmp_path / "prova.md"
    f.write_text(testo, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--caratteristiche", str(f)],
        capture_output=True, text=True, cwd=ROOT)


# ── quello che DEVE segnalare ────────────────────────────────────────────

def test_prova_minuscola_con_una_cd(tmp_path):
    r = corri(tmp_path, "Il nano tenta una prova di forza, CD 18, per sollevarlo.\n")
    assert r.returncode == 1
    assert "prova di forza" in r.stdout


def test_abilita_col_modificatore_minuscola(tmp_path):
    r = corri(tmp_path, "**Abilita**: nuotare +9, Scalare +6\n")
    assert r.returncode == 1
    assert "nuotare +9" in r.stdout


def test_punteggio_di_caratteristica_minuscolo(tmp_path):
    r = corri(tmp_path, "| forza 25 | Des 14 |\n")
    assert r.returncode == 1


def test_bonus_di_caratteristica_minuscolo(tmp_path):
    r = corri(tmp_path, "- CA 15 (bonus di destrezza +2)\n")
    assert r.returncode == 1


# ── quello che deve TACERE, ed e' il motivo per cui la norma esiste ──────

def test_il_sostantivo_comune_non_conta(tmp_path):
    """2.014 occorrenze nude nel repo: se queste passano, il controllo e' morto."""
    r = corri(tmp_path, "La forza dell'orda era nella sua destrezza di manovra,\n"
                        "e il carisma del capitano teneva insieme la saggezza dei vecchi.\n")
    assert r.returncode == 0, r.stdout


def test_prova_senza_una_cd_non_conta(tmp_path):
    """«prove di saggezza e spiritualita'» e' una descrizione, non un tiro."""
    r = corri(tmp_path, "Ambientazione: antica foresta sacra, prove di saggezza e spiritualita'.\n")
    assert r.returncode == 0, r.stdout


def test_lo_spazio_dopo_il_segno_non_conta(tmp_path):
    """Il falso positivo vero: «40.500 mo in oggetti di artigianato + 1 Sacrificio»."""
    r = corri(tmp_path, "**Costo:** 40.500 mo in oggetti di artigianato + 1 Sacrificio Personale.\n")
    assert r.returncode == 0, r.stdout


def test_il_bonus_di_intuizione_non_e_un_abilita(tmp_path):
    """In 3.5 «intuizione» e' un TIPO di bonus; l'abilita' e' Percepire Intenzioni."""
    r = corri(tmp_path, "Concede un bonus di intuizione +4 alle prove di Artigianato.\n")
    assert r.returncode == 0, r.stdout


def test_la_forma_corretta_passa(tmp_path):
    r = corri(tmp_path, "Prova di Forza CD 25; **Nuotare** +9; bonus di Destrezza +3; For 25.\n")
    assert r.returncode == 0, r.stdout


# ── il repo vero ─────────────────────────────────────────────────────────

def test_il_repo_e_a_zero():
    r = subprocess.run([sys.executable, str(SCRIPT), "--caratteristiche"],
                       capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout


def test_gli_archivi_sono_fuori():
    """Il passo 3 della sesta regola: `_SNAPSHOT-STORICO.md` esclude la cartella."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import validate_prosa as vp

    snapshot = {p.parent for p in ROOT.rglob("_SNAPSHOT-STORICO.md")}
    assert snapshot, "il repo non ha piu' nessuno snapshot dichiarato"
    for f in vp.file_di_gioco():
        assert not any(s in f.parents for s in snapshot), f
        assert "_ARCHIVIO" not in f.parts, f
