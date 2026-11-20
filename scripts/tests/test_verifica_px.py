"""verifica_px.py: il registro dei PX del repo torna, e ogni errore inserito si vede (ADR-0148).

La misura sui mutanti è quella dichiarata nell'ADR: ogni cella di ogni riga
cambiata di 1.000 PX deve far scattare R1, e sul registro vero non ci sono
falsi allarmi. R2, R3 e R4 hanno test propri, non una misura sui mutanti.
"""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verifica_px as V  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REGISTRO = ROOT / "campaign" / "REGISTRO-PX.md"
STATE = ROOT / "campaign" / "state.yaml"

MINI = """# Registro

## Totali

| | Thorik | Hella |
|---|---:|---:|
| PX | 3.500 | 1.000 |
| Livello dai PX | 3° | 2° |
| Livello al tavolo | 3° | 2° |

## Arco

| Riga | Scontro o evento | Th | He |
|---:|---|---:|---:|
| 1 | Partenza | 3.000 | 1.000 |
| 2 | Orchi | 500 |  |
"""

STATE_MINI = """party:
- pg: Thorik
  classe: Dwarf Fighter 3
- pg: Hella
  classe: Human Druid 1 / Ranger 1
"""


def _scrivi(d: Path, registro: str, state: str = STATE_MINI) -> "tuple[Path, Path]":
    r, s = d / "REGISTRO-PX.md", d / "state.yaml"
    r.write_text(registro, encoding="utf-8")
    s.write_text(state, encoding="utf-8")
    return r, s


class TestSoglie(unittest.TestCase):
    def test_tabella_srd(self) -> None:
        # PHB 3.5, Table 3–2 (non SRD): 2° = 1.000, 13° = 78.000, 14° = 91.000, 15° = 105.000
        self.assertEqual([V.soglia(n) for n in (1, 2, 13, 14, 15)], [0, 1000, 78000, 91000, 105000])
        self.assertEqual(V.livello_da_px(104999), 14)
        self.assertEqual(V.livello_da_px(105000), 15)
        self.assertEqual(V.livello_da_px(86354), 13)

    def test_numeri_italiani(self) -> None:
        self.assertEqual(V.numero("104.999"), 104999)
        self.assertEqual(V.numero("-4.968"), -4968)
        self.assertEqual(V.numero("14°"), 14)
        self.assertIsNone(V.numero(""))
        self.assertIsNone(V.numero("—"))


class TestRegistroDelRepo(unittest.TestCase):
    def test_nessuna_violazione(self) -> None:
        self.assertEqual(V.verifica(REGISTRO, STATE), [])

    def test_le_colonne_e_le_righe_ci_sono(self) -> None:
        dati = V.leggi(REGISTRO.read_text(encoding="utf-8"))
        self.assertEqual(dati["colonne"], ["Th", "To", "Ar", "He", "Jo"])
        self.assertGreater(len(dati["righe"]), 90)


class TestRegole(unittest.TestCase):
    def test_mini_pulito(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(V.verifica(*_scrivi(Path(t), MINI)), [])

    def test_r1_somma(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            v = V.verifica(*_scrivi(Path(t), MINI.replace("| 2 | Orchi | 500 |", "| 2 | Orchi | 600 |")))
            self.assertEqual([x.regola for x in v], ["R1 somma"])
            self.assertEqual((v[0].colonna, v[0].atteso, v[0].ha), ("Thorik", "3.600", "3.500"))
            self.assertRegex(v[0].dove, r"REGISTRO-PX\.md:7$")

    def test_r2_soglia(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            v = V.verifica(*_scrivi(Path(t), MINI.replace("| Livello dai PX | 3° |", "| Livello dai PX | 4° |")))
            self.assertEqual([x.regola for x in v], ["R2 soglia"])

    def test_r3_un_livello_alla_volta(self) -> None:
        testo = MINI.replace("| 2 | Orchi | 500 |", "| 2 | Orchi | 7.500 |").replace(
            "| PX | 3.500 |", "| PX | 10.500 |").replace("| Livello dai PX | 3° |", "| Livello dai PX | 5° |")
        with tempfile.TemporaryDirectory() as t:
            v = V.verifica(*_scrivi(Path(t), testo))
            self.assertEqual([x.regola for x in v], ["R3 un livello"])

    def test_r4_livello_al_tavolo(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            v = V.verifica(*_scrivi(Path(t), MINI, STATE_MINI.replace("Fighter 3", "Fighter 4")))
            self.assertEqual([x.regola for x in v], ["R4 tavolo"])

    def test_r3_livello_al_tavolo_oltre_i_px(self) -> None:
        testo = MINI.replace("| Livello al tavolo | 3° |", "| Livello al tavolo | 9° |")
        with tempfile.TemporaryDirectory() as t:
            v = V.verifica(*_scrivi(Path(t), testo, STATE_MINI.replace("Fighter 3", "Fighter 9")))
            self.assertEqual([x.regola for x in v], ["R3 un livello"])

    def test_r4_pg_senza_riga_in_state(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            v = V.verifica(*_scrivi(Path(t), MINI, "party:\n- pg: Thorik\n  classe: Dwarf Fighter 3\n"))
            self.assertEqual([(x.regola, x.colonna) for x in v], [("R4 tavolo", "Hella")])

    def test_livello_effettivo(self) -> None:
        casi = {"Dream Dwarf Ranger 1 / Druid 12": 13, "Dwarf Fighter 4 / Monk 9": 13,
                "Human Warlock 13 (ECL 15)": 15, "Dwarf Fighter 13, 3 DV razziali": 13,
                "Ranger1/Druid12": 13, "Half-Ogre (LA +2) Fighter 1": 3}
        for classe, atteso in casi.items():
            with self.subTest(classe=classe):
                self.assertEqual(V.livello_effettivo(classe), atteso)

    def test_colonne_in_ordine_diverso_sono_una_violazione(self) -> None:
        righe = [l for l in MINI.splitlines() if l.startswith("| Riga")]
        self.assertTrue(righe, "il mini-registro ha un'intestazione «Riga»")
        cols = [c.strip() for c in righe[0].strip("|").split("|")]
        invertita = "| " + " | ".join(cols[:2] + cols[2:][::-1]) + " |"
        testo = MINI + "\n" + invertita + "\n"
        with tempfile.TemporaryDirectory() as d:
            v = V.verifica(*_scrivi(Path(d), testo, STATE_MINI))
            self.assertIn("forma", [x.regola for x in v])

    def test_numeri_che_non_sono_livelli(self) -> None:
        self.assertEqual(V.livello_effettivo("Human Warlock 13 (CR 13)"), 13)
        self.assertEqual(V.livello_effettivo("Dwarf Fighter 13, Str 18"), 13)

    def test_meno_con_il_trattino_medio(self) -> None:
        self.assertEqual(V.numero("\u2013500"), -500)

    def test_forma_mancante(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            v = V.verifica(*_scrivi(Path(t), "# vuoto\n"))
            self.assertEqual([x.regola for x in v], ["forma"])

    def test_uscita_json_e_codice(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            r, s = _scrivi(Path(t), MINI.replace("| 2 | Orchi | 500 |", "| 2 | Orchi | 600 |"))
            self.assertEqual(V.main([str(r), "--state", str(s), "--json"]), 1)
            r, s = _scrivi(Path(t), MINI)
            self.assertEqual(V.main([str(r), "--state", str(s)]), 0)


class TestMutantiSulRegistroVero(unittest.TestCase):
    """Ogni cella numerica del registro vero, cambiata di 1.000, deve far scattare R1."""

    def test_ogni_cella_cambiata_si_vede(self) -> None:
        righe = REGISTRO.read_text(encoding="utf-8").splitlines()
        state = STATE.read_text(encoding="utf-8")
        mutanti = trovati = 0
        with tempfile.TemporaryDirectory() as t:
            for i, riga in enumerate(righe):
                if not re.match(r"^\| \d+ \|", riga):
                    continue
                celle = riga.split("|")
                for j in range(3, len(celle) - 1):
                    valore = V.numero(celle[j])
                    if valore is None:
                        continue
                    nuovo = f"{valore + 1000:,}".replace(",", ".")
                    copia = celle[:j] + [f" {nuovo} "] + celle[j + 1:]
                    testo = "\n".join(righe[:i] + ["|".join(copia)] + righe[i + 1:]) + "\n"
                    mutanti += 1
                    r, _ = _scrivi(Path(t), testo, state)
                    if any(v.regola == "R1 somma" for v in V.verifica(r, None)):
                        trovati += 1
        self.assertGreater(mutanti, 300)
        self.assertEqual(trovati, mutanti)
        print(f"\nverifica_px: {trovati}/{mutanti} mutanti trovati")


if __name__ == "__main__":
    unittest.main()
