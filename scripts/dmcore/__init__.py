"""
dmcore — libreria condivisa del toolkit DM RumblingStone (Lotto A del
piano AUTOMAZIONE-STATO-SESSIONI; ADR-0007).

Raccoglie la logica riusata da più script (`campaign_branch.py`,
`state_apply.py`, `next_session.py`) così che nessuno script la
duplichi e `dm.py` resti puro orchestratore (ADR-0002).

Moduli:
    regions  — regioni marcate ``<!-- auto:begin/end -->`` nei file canone
    gitio    — helper git (branch corrente, guardia anti-main, commit)
    config   — configurazione gruppo (campaign/group.yaml, parser stdlib)

Solo stdlib; nessun modulo scrive file al momento dell'import.
"""

from __future__ import annotations

from pathlib import Path

__version__ = "0.1.0"

#: Root del repository (…/scripts/dmcore/__init__.py → parents[2])
REPO = Path(__file__).resolve().parents[2]
