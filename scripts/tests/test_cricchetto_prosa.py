"""Il cricchetto della prosa: sui file di gioco cambiati nessuna norma MQM peggiora (ADR-0146)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cricchetto_prosa as cp  # noqa: E402

BOX_CORTO = "> *Il vento porta cenere dalla valle.*\n"
BOX_LUNGO = "".join(f"> *Riga {i} del box che non finisce mai.*\n" for i in range(14))
STATBLOCK = "**CA** 18\n**pf** 45 (6d10+12)\n"


def test_box_oltre_tetto_aggiunto_peggiora():
    peggiori = cp.confronta("Bestiario/mostri/x.md", STATBLOCK, STATBLOCK + "\n" + BOX_LUNGO)
    assert "box_oltre_12_righe" in peggiori


def test_box_corto_aggiunto_non_peggiora():
    assert cp.confronta("Bestiario/mostri/x.md", STATBLOCK, STATBLOCK + "\n" + BOX_CORTO) == {}


def test_misto_senza_prosa_nuova_non_si_controlla():
    # anche se la scheda aveva già un box lungo, un ritocco allo statblock passa
    prima = BOX_LUNGO + "\n" + STATBLOCK
    dopo = BOX_LUNGO + "\n" + STATBLOCK.replace("45", "52")
    assert cp.da_controllare("Bestiario/mostri/x.md", prima, dopo) is False


def test_prosa_pura_si_controlla_sempre():
    assert cp.da_controllare("campaign/recaps/r.md", "a\n", "b\n") is True


def test_misto_con_box_nuovo_si_controlla():
    assert cp.da_controllare("Bestiario/mostri/x.md", STATBLOCK, STATBLOCK + BOX_CORTO) is True


def test_file_nuovo_confronta_col_vuoto():
    assert "box_oltre_12_righe" in cp.confronta("campaign/recaps/r.md", None, BOX_LUNGO)


def test_un_difetto_tolto_e_uno_aggiunto_altrove_si_vede():
    prima = BOX_LUNGO
    dopo = BOX_CORTO + "\n" + BOX_LUNGO + "\n" + BOX_LUNGO
    assert cp.confronta("campaign/recaps/r.md", prima, dopo)["box_oltre_12_righe"] == (1, 2)


def test_esito_esce_1_solo_se_qualcosa_peggiora(monkeypatch):
    monkeypatch.setattr(cp, "coppie", lambda rev: [("campaign/recaps/r.md", BOX_CORTO, BOX_LUNGO)])
    assert cp.main(["--rispetto-a", "origin/main"]) == 1
    monkeypatch.setattr(cp, "coppie", lambda rev: [("campaign/recaps/r.md", BOX_LUNGO, BOX_CORTO)])
    assert cp.main(["--rispetto-a", "origin/main"]) == 0


def test_nessun_file_cambiato_passa(monkeypatch):
    monkeypatch.setattr(cp, "coppie", lambda rev: [])
    assert cp.main(["--rispetto-a", "origin/main"]) == 0
