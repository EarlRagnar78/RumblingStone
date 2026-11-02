"""`dm.py session end` non dice «committate» quando un passo è fallito.

Il 2026-10-11, provando il flusso su un ramo di gruppo nuovo (ADR-0090),
`state_apply.py` è uscito con 2 per un percorso sbagliato e `dm.py` ha
stampato lo stesso «✓ session end: … applicate e committate». Il DM avrebbe
chiuso il terminale con il log non committato.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import dm  # noqa: E402


def _args() -> argparse.Namespace:
    return argparse.Namespace(action="end", session="log.md", yes=True,
                              last_n=1, hype=False, pg=None, group=None)


def _fine(codici: dict) -> "tuple[int, str, str]":
    """Lancia `session end` con `run` finto: ogni script esce col suo codice."""
    def finto(script, *a, **k):
        return codici.get(script, 0)
    out, err = io.StringIO(), io.StringIO()
    with mock.patch.object(dm, "run", side_effect=finto), \
            contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = dm.cmd_session(_args(), [])
    return rc, out.getvalue(), err.getvalue()


class TestSessionEnd(unittest.TestCase):
    def test_state_apply_fallito_non_e_un_successo(self):
        rc, out, err = _fine({"state_apply.py": 2})
        self.assertEqual(rc, 2)
        self.assertNotIn("committate", out)
        self.assertIn("incompleto", err)

    def test_tutto_bene_resta_come_prima(self):
        rc, out, _ = _fine({})
        self.assertEqual(rc, 0)
        self.assertIn("✓ session end", out)

    def test_guardia_del_ramo_ferma_tutto(self):
        rc, out, _ = _fine({"campaign_branch.py": 1})
        self.assertEqual(rc, 1)
        self.assertNotIn("session end", out)


if __name__ == "__main__":
    unittest.main()
