"""verifica_rimandi.py: i «FILE §N» e «vedi §N» puntano a sezioni vere (ADR-0148).

Tre misure, come le dichiara l'ADR: il repo di oggi non ha violazioni nuove;
ogni rimando che oggi torna, spostato su un § che il bersaglio non ha, si vede
(mutanti); le voci in attesa del DM esistono ancora.
"""
from __future__ import annotations

import io
import re
import sys
import unittest
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verifica_rimandi as V  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


class TestSezioni(unittest.TestCase):
    def test_titoli_con_paragrafo_e_con_numero(self) -> None:
        testo = "# Titolo\n## §0 — Quickstart\n## 4. Il mazzo\n### 7) Fine\n```\n## §9 dentro il codice\n```\n"
        self.assertEqual(V.sezioni(testo), {"0", "4", "7"})

    def test_un_nome_ambiguo_non_si_giudica(self) -> None:
        tutti = ["a/ARC08-02-UNO.md", "b/ARC08-02-DUE.md", "c/state.md"]
        idx = V.indice_nomi(tutti)
        self.assertEqual(V.risolvi("state.md", idx, tutti)[0], "c/state.md")
        self.assertIsNone(V.risolvi("ARC08-02", idx, tutti)[0])
        self.assertEqual(V.risolvi("ARC08-02-UN", idx, tutti)[0], "a/ARC08-02-UNO.md")


# Canale testing di ADR-0099 fino alla promozione: in CI il passo dedicato avvisa
# e non blocca, e pytest non deve bloccare al suo posto.
PROMOZIONE = date(2026, 12, 4)


class TestRepo(unittest.TestCase):
    @unittest.skipIf(date.today() < PROMOZIONE, "verifica_rimandi in testing fino al 2026-12-04 (ADR-0148)")
    def test_nessuna_violazione_nuova(self) -> None:
        with redirect_stdout(io.StringIO()) as out:
            rc = V.main(["--check"])
        self.assertEqual(rc, 0, out.getvalue())
        self.assertIn(" 0 violazioni", out.getvalue())

    def test_le_voci_in_attesa_esistono_ancora(self) -> None:
        for (file, testo) in V.IN_ATTESA:
            with self.subTest(file=file):
                self.assertIn(testo, (ROOT / file).read_text(encoding="utf-8"),
                              "corretta? togli la voce da IN_ATTESA")


class TestMutanti(unittest.TestCase):
    """Ogni rimando che torna, spostato su un § assente, deve diventare una violazione."""

    def test_rimandi_spostati(self) -> None:
        tutti = V._md_del_repo()
        idx = V.indice_nomi(tutti)
        cache: "dict[str, set[str]]" = {}
        scelti = [f for f in tutti if V.RADICI.match(f) and not V.ESCLUSI.search(f)]
        buoni = [r for f in scelti for r in V.rimandi(f, idx, tutti, cache) if r.esito == "ok"]
        self.assertGreater(len(buoni), 100)
        mutanti = trovati = 0
        per_file: "dict[str, list]" = {}
        for r in buoni:
            per_file.setdefault(r.file, []).append(r)
        for file, lista in per_file.items():
            righe = (ROOT / file).read_text(encoding="utf-8", errors="replace").splitlines()
            for r in lista[:3]:  # tre per file: abbastanza, e il test resta veloce
                assente = str(max(int(x) for x in cache[r.bersaglio]) + 7)
                nuova = righe[r.riga - 1].replace(r.testo, r.testo[: -len(r.sezione)] + assente, 1)
                if nuova == righe[r.riga - 1]:
                    continue
                testo = "\n".join(righe[: r.riga - 1] + [nuova] + righe[r.riga:]) + "\n"
                mutanti += 1
                esiti = V.rimandi(file, idx, tutti, cache, testo)
                if any(e.riga == r.riga and e.esito == "violazione"
                       and re.search(re.escape(assente) + r"$", e.testo) for e in esiti):
                    trovati += 1
        print(f"\nverifica_rimandi: {trovati}/{mutanti} mutanti trovati")
        self.assertGreater(mutanti, 50)
        self.assertEqual(trovati, mutanti)


if __name__ == "__main__":
    unittest.main()
