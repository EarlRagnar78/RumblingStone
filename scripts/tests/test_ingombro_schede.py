"""Ogni scheda del repo dichiara taglia, spazio e portata, e i tre tornano con
la tabella dell'SRD (ADR-0128). Cricchetto a zero: una scheda nuova senza i
tre campi, o con uno spazio che non è quello della sua taglia, ferma la CI."""
import doctest
import subprocess
import unittest
from pathlib import Path

from dmcore import statblock as S

ROOT = Path(__file__).resolve().parents[2]
FUORI = ("plans/", "docs/", "skills/")


def schede():
    nomi = subprocess.run(["git", "ls-files", "-z", "*.md"], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout.split("\0")
    for n in nomi:
        if not n or n.endswith(".hb.md") or "_ARCHIVIO" in n or n.startswith(FUORI):
            continue
        righe = (ROOT / n).read_text(encoding="utf-8").split("\n")
        i = 0
        while i < len(righe):
            if righe[i].strip() != S.APERTURA:
                i += 1
                continue
            j = next(k for k in range(i + 1, len(righe)) if righe[k].strip() == S.CHIUSURA)
            yield n, i + 1, S.leggi("\n".join(righe[i:j + 1]))
            i = j + 1


class TestIngombro(unittest.TestCase):
    def test_doctest(self):
        self.assertEqual(doctest.testmod(S).failed, 0)

    def test_tabella_srd(self):
        t = S.taglie()["taglie"]
        self.assertEqual((t["Media"]["spazio"], t["Media"]["alta"]), (1.5, 1.5))
        self.assertEqual((t["Grande"]["spazio"], t["Grande"]["alta"], t["Grande"]["lunga"]), (3.0, 3.0, 1.5))
        self.assertEqual((t["Enorme"]["spazio"], t["Enorme"]["alta"], t["Enorme"]["lunga"]), (4.5, 4.5, 3.0))
        self.assertEqual(t["Minuscola"]["alta"], 0.0)

    def test_ogni_scheda_dichiara_taglia_spazio_e_portata(self):
        difetti = [f"{n}:{riga} {sb.nome or ''}: {d}"
                   for n, riga, sb in schede() for d in S.difetti_ingombro(sb)]
        self.assertEqual(difetti, [], "\n".join(difetti[:40]))

    def test_la_riga_del_riquadro_conta_i_quadretti(self):
        sb = S.Statblocco(taglia="Enorme", spazio="4,5 m", portata="3 m (4,5 m con il morso)")
        self.assertEqual(S.ingombro(sb), "**Taglia** Enorme · **Spazio** 4,5 m (3×3 quadretti) · "
                                         "**Portata** 3 m (2 quadretti); 4,5 m (3 quadretti) con il morso")


if __name__ == "__main__":
    unittest.main()
