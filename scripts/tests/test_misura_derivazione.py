"""misura_derivazione: i due assi (testo e impianto) non si confondono.

Il rischio da fermare è quello di ADR-0053, un matcher largo che traveste
l'ignoranza: un testo riscritto da capo deve risultare lontano anche se
racconta la stessa cosa, e un concetto rinominato non deve passare per
«stesso nome» solo perché esiste in tutti e due.
"""
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _md():
    spec = importlib.util.spec_from_file_location(
        "misura_derivazione", ROOT / "scripts" / "misura_derivazione.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


A = {"a.md": "# Giorno 1 la Tratta\n\nLa Tratta assegna i cavalli alle contrade "
             "davanti a tutta la piazza, e il Morale del rione sale o scende. "
             "Il fantino col nerbo colpisce chi gli sta accanto alla Mossa."}
B_COPIA = {"b.md": A["a.md"]}
B_RISCRITTO = {"b.md": "# Giorno 1 la Sorte\n\nLa Sorte dà a ogni rione un animale "
                       "estratto in pubblico; chi perde la faccia perde il Morale. "
                       "Allo Stacco si usa lo scudiscio sul vicino."}


class Testo(unittest.TestCase):
    def test_copia_integrale_e_tutta_contenuta(self):
        r = _md().misura_testo(A, B_COPIA)
        self.assertEqual(r["B_contenuto_in_A"], 1.0)
        self.assertEqual(r["frasi_B_quasi_da_A"], r["frasi_B"])

    def test_riscrittura_non_condivide_testo(self):
        r = _md().misura_testo(A, B_RISCRITTO)
        self.assertEqual(r["B_contenuto_in_A"], 0.0)
        self.assertEqual(r["frasi_B_quasi_da_A"], 0)


class Impianto(unittest.TestCase):
    CONCETTI = [
        {"id": "partenza", "dimensione": "scene", "A": [r"\bMossa\b"], "B": [r"\bStacco\b"]},
        {"id": "morale", "dimensione": "regole", "A": [r"\bMorale\b"]},
        {"id": "tratta", "dimensione": "scene", "A": [r"\bTratta\b"], "B": ["Sorte"],
         "maiuscole": True},
        {"id": "solo-a", "dimensione": "regole", "A": [r"\bnerbo\b"], "B": ["frusta"]},
    ]

    def _stati(self, b):
        r = _md().misura_concetti(A, b, self.CONCETTI)
        return {x["id"]: x["stato"] for x in r["righe"]}

    def test_rinominato_non_e_stesso_nome(self):
        s = self._stati(B_RISCRITTO)
        self.assertEqual(s["partenza"], "rinominato")
        self.assertEqual(s["morale"], "stesso nome")
        self.assertEqual(s["solo-a"], "solo A")

    def test_maiuscole_ignora_il_verbo(self):
        # «tratta» verbo minuscolo non deve far passare la Tratta per stesso nome
        b = {"b.md": "Il fantino non tratta. La Sorte decide."}
        self.assertEqual(self._stati(b)["tratta"], "rinominato")


class Ripetibile(unittest.TestCase):
    def test_corrispondenze_drappo_palio_stessa_uscita(self):
        cfg_path = ROOT / "plans/esperimenti/drappo-palio-2026-11-01/corrispondenze.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        md = _md()
        uno = md.rapporto_md(md.misura(cfg))
        due = md.rapporto_md(md.misura(cfg))
        # Solo la ripetibilità: MISURA.md è la fotografia del 2026-11-01 e
        # invecchia di proposito quando il Drappo o il Palio cambiano.
        self.assertEqual(uno, due)


if __name__ == "__main__":
    unittest.main()
