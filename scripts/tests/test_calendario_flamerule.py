"""Cancello del calendario: la campagna comincia il 1° Flamerule 1372.

Decisione del DM del 2026-07-12 (campaign/state-changelog.md), confermata sulle
card del 2026-11-18: Giorno di Marcia 1 = 1° Flamerule, quindi il Giorno 30 è
il 30 Flamerule. «Mirtul» nei testi di gioco era un residuo di prima: legava
al mese sbagliato la scadenza della Torre Invisibile e la data della lettera
di Brenna. Questo test impedisce che torni.
"""
import re
import unittest
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]

# Cartelle del canone di gioco: gli archi numerati, il Bestiario, lo stato.
CARTELLE = re.compile(r"^(\d\d_.*|Bestiario|campaign)$")

# Storia che non si riscrive: il registro dei cambi di stato cita il nome vecchio.
ESENTI = {"campaign/state-changelog.md"}

# La PR #472 (carta del cielo e handout 7) è su main dal 18/11: nessuna riga in attesa.
IN_ATTESA: dict[str, int] = {}


def _file_del_canone():
    for cartella in sorted(RADICE.iterdir()):
        if not cartella.is_dir() or not CARTELLE.match(cartella.name):
            continue
        for percorso in sorted(cartella.rglob("*")):
            if percorso.suffix in (".md", ".yaml", ".yml") and percorso.is_file():
                yield percorso


class TestCalendarioFlamerule(unittest.TestCase):
    def test_nessun_mirtul_nei_testi_di_gioco(self):
        trovati = {}
        for percorso in _file_del_canone():
            relativo = percorso.relative_to(RADICE).as_posix()
            if relativo in ESENTI:
                continue
            quante = len(re.findall(r"mirtul", percorso.read_text(encoding="utf-8"), re.I))
            if quante > IN_ATTESA.get(relativo, 0):
                trovati[relativo] = quante
        self.assertEqual(
            trovati,
            {},
            "«Mirtul» in un testo di gioco: la campagna comincia il 1° Flamerule "
            "(Giorno di Marcia N = N Flamerule fino al 30)",
        )

    def test_l_ancora_degli_script_e_flamerule(self):
        recap = (RADICE / "scripts" / "session_recap.py").read_text(encoding="utf-8")
        self.assertIn('MARCH_DAY1_HARPTOS: "tuple[str, int] | None" = ("Flamerule", 1)', recap)


if __name__ == "__main__":
    unittest.main()
