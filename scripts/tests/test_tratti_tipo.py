"""I tratti del tipo nei mostri generati (lotto 5 delle regole complete, 2026-11-10).

I difetti che questi test esistono per impedire:

- un non morto o un costrutto con un punteggio di Costituzione e i pf che ne
  vengono (SRD «Types»: «No Constitution score»); prima del 2026-11-10 un non
  morto di GS 7 usciva con Cos 18 e 108 pf;
- una melma, un parassita o un costrutto con Int 8 e sette talenti («Mindless
  creatures do not gain feats or skills»);
- un costrutto senza i pf bonus della sua taglia (Construct Traits);
- un modificatore di Tempra preso da una Costituzione che non c'è;
- il template Advanced che dà pf a chi non ha Costituzione.

Solo `unittest`.
"""
from __future__ import annotations

import random
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import genera_creatura as G  # noqa: E402
from dmcore import creature_pf1e as CP  # noqa: E402


def _car(sb) -> dict:
    return dict(re.findall(r"(For|Des|Cos|Int|Sag|Car)\s+(\S+)", sb.attributi))


def _mostro(tipo, gs=7, taglia="medium", **kw):
    return G.genera(gs, tipo=tipo, taglia=taglia, ruolo="bruto", rng=random.Random(1), **kw)


class Dati(unittest.TestCase):
    def test_tratti_e_tabella_del_costrutto(self):
        self.assertEqual(G.tratti_del_tipo("undead"), {"senza_cos": True, "senza_int": False, "pf_bonus": 0})
        self.assertEqual(G.tratti_del_tipo("melma"), {"senza_cos": False, "senza_int": True, "pf_bonus": 0})
        self.assertEqual(G.tratti_del_tipo("construct", "grande")["pf_bonus"], 30)
        self.assertEqual([G.tratti_del_tipo("construct", t)["pf_bonus"] for t in
                          ("fine", "tiny", "small", "medium", "huge", "gargantuan", "colossal")],
                         [0, 0, 10, 20, 40, 60, 80])
        self.assertEqual(G.tratti_del_tipo("humanoid"), {"senza_cos": False, "senza_int": False, "pf_bonus": 0})


class Generatore(unittest.TestCase):
    def test_non_morto_senza_costituzione(self):
        sb, conto = _mostro("undead")
        self.assertEqual(_car(sb)["Cos"], "—")
        dv = int(sb.pf_dado.split("d")[0])
        self.assertEqual(int(sb.pf), int(dv * 6.5) + 3)          # dadi + Robustezza
        self.assertTrue(any("mancano" in r for r in conto.righe), conto.righe)
        possente = 2 if any("Tempra possente" in v for v in sb.voci) else 0
        self.assertRegex(sb.ts, r"Temp \+%d\b" % (dv // 3 + possente))  # niente Cos

    def test_costrutto_senza_mente_col_bonus_di_taglia(self):
        for taglia, bonus in (("medium", 20), ("large", 30), ("tiny", 0)):
            with self.subTest(taglia=taglia):
                sb, _ = _mostro("construct", taglia=taglia)
                c = _car(sb)
                self.assertEqual((c["Cos"], c["Int"]), ("—", "—"))
                dv = int(sb.pf_dado.split("d")[0])
                self.assertEqual(int(sb.pf), int(dv * 5.5) + bonus)
                self.assertIn("Talenti: —", sb.voci)
                self.assertRegex(sb.ts, r"Temp \+%d\b" % (dv // 3))

    def test_melma_e_parassita_senza_talenti(self):
        for tipo in ("ooze", "vermin"):
            with self.subTest(tipo=tipo):
                sb, _ = _mostro(tipo)
                self.assertEqual(_car(sb)["Int"], "—")
                self.assertIn("Talenti: —", sb.voci)
                self.assertNotEqual(_car(sb)["Cos"], "—")

    def test_gli_altri_tipi_restano_come_prima(self):
        for tipo in ("humanoid", "giant", "dragon", "aberration"):
            with self.subTest(tipo=tipo):
                c = _car(_mostro(tipo)[0])
                self.assertTrue(c["Cos"].isdigit() and c["Int"].isdigit(), c)

    def test_advanced_non_da_pf_senza_costituzione(self):
        base, _ = _mostro("undead")
        cattivo, _ = _mostro("undead", piu_cattivi=True)
        self.assertEqual(_car(cattivo)["Cos"], "—")
        self.assertEqual(int(cattivo.pf), int(base.pf))

    def test_pf1e_non_morto_col_carisma_e_costrutto_col_bonus(self):
        bersaglio = G.bersaglio_di(7, "bruto", piu_cattivi=False)[0]["pf"]
        sb, _ = _mostro("undead", talenti=None)
        pf, _ = CP.converti(sb, "undead", "medium", pf_bersaglio=bersaglio)
        car = int(_car(pf)["Car"])
        dv = int(pf.pf_dado.split("d")[0])
        self.assertEqual(int(pf.pf), int(dv * 4.5 + (car - 10) // 2 * dv))
        sb, _ = _mostro("construct", talenti=None)
        pf, conto = CP.converti(sb, "construct", "medium")
        self.assertTrue(pf.pf_dado.endswith("+20"), pf.pf_dado)
        self.assertTrue(any("gradi di abilità" in r and "= 0" in r for r in conto), conto)


if __name__ == "__main__":
    unittest.main()
