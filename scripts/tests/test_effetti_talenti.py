"""Gli effetti dei talenti sulle abilità nel conto dei gradi (ADR-0126, lotto 4)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verifica_scheda as V  # noqa: E402
from dmcore import sistemi as S  # noqa: E402

# Barbaro 4, Int 10: massimo 7 gradi; margine 4 (sinergia 2, razza 2): uno gnoll, che non è in nessuna
# tabella delle razze (l'orco dal lotto 6 terza parte ha il margine contato). Barbaro e non guerriero
# perché Ascoltare e Scalare devono essere abilità di classe (lotto 6: fuori classe il massimo è la metà).
# Ascoltare (Sag +1): 12 senza talenti. Scalare (For +3): 14 senza talenti.
SCHEDA = """# Prova [INFERRED]
**Faction**: none | **Role**: brute | **Environment**: any | **CR**: 4

```statblocco
gs: 4
tipo: Medium humanoid (gnoll), Barbarian 4, CE
ca: 14
pf: 34
pf-dado: 4d12+8
ts: Temp +6, Rifl +2, Vol +2
attributi: For 16 Des 12 Cos 14 Int 10 Sag 12 Car 8
velocita: 9 m
iniziativa: +1
attacchi:
  - Mischia spada lunga +7 (1d8+3/19-20)
voci:
  - Abilità: {abilita}
  - Talenti: {talenti}
```
"""


def fuori_massimo(abilita: str, talenti: str) -> "list[str]":
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / "prova-cr4.md"
        q.write_text(SCHEDA.format(abilita=abilita, talenti=talenti), encoding="utf-8")
        if V.VT.leggi(q) is None:
            raise AssertionError("la scheda di prova non si legge")
        v, n = V.abilita(q)
    if any(x["regola"] in ("lettura", "sistema") for x in n):
        raise AssertionError(f"il conto dei gradi non parte: {n}")
    return [x["abilita"] for x in v if x["regola"] == "gradi.massimo"]


class TestIlBonusVaSoloAlleSueAbilita(unittest.TestCase):
    def test_senza_talenti_d_abilita(self):
        self.assertEqual(fuori_massimo("Ascoltare +12, Scalare +14", "Attacco Poderoso, Incalzare"), [])
        self.assertEqual(fuori_massimo("Ascoltare +13, Scalare +15", "Attacco Poderoso, Incalzare"), ["listen", "climb"])

    def test_allerta_alza_ascoltare_e_non_scalare(self):
        self.assertEqual(fuori_massimo("Ascoltare +14, Scalare +14", "Allerta, Incalzare"), [])
        self.assertEqual(fuori_massimo("Ascoltare +15, Scalare +14", "Allerta, Incalzare"), ["listen"])
        # prima il talento dava 3 punti di margine a tutte: Scalare +15 passava
        self.assertEqual(fuori_massimo("Ascoltare +14, Scalare +15", "Allerta, Incalzare"), ["climb"])

    def test_abilita_focalizzata_vale_per_l_abilita_scelta(self):
        self.assertEqual(fuori_massimo("Ascoltare +15, Scalare +14", "Abilità Focalizzata (Ascoltare), Incalzare"), [])
        self.assertEqual(fuori_massimo("Ascoltare +16, Scalare +15", "Abilità Focalizzata (Ascoltare), Incalzare"),
                         ["listen", "climb"])

    def test_i_bonus_di_due_talenti_sulla_stessa_abilita_si_sommano(self):
        self.assertEqual(fuori_massimo("Ascoltare +17", "Abilità Focalizzata (Ascoltare), Allerta"), [])
        self.assertEqual(fuori_massimo("Ascoltare +18", "Abilità Focalizzata (Ascoltare), Allerta"), ["listen"])

    def test_senza_l_abilita_scelta_il_bonus_vale_per_tutte(self):
        self.assertEqual(fuori_massimo("Ascoltare +15, Scalare +17", "Abilità Focalizzata, Incalzare"), [])
        self.assertEqual(fuori_massimo("Scalare +18", "Abilità Focalizzata, Incalzare"), ["climb"])


class TestFuoriDallaRigaDeiTalenti(unittest.TestCase):
    def test_il_talento_nominato_altrove_vale_sulle_sue_abilita(self):
        regole = S.dati("dnd35", "creature.gradi")
        per, a_tutte = V._talenti_d_abilita(["Incalzare"], "Ascoltare +3, Osservare +3 (Allerta dal famiglio)",
                                            "dnd35", regole, 5)
        self.assertEqual((per, a_tutte), ({"listen": 2, "spot": 2}, 0))

    def test_la_riga_dei_talenti_vince_sul_resto_del_testo(self):
        regole = S.dati("dnd35", "creature.gradi")
        per, _ = V._talenti_d_abilita(["Furtivo"], "un passo agile, Allerta", "dnd35", regole, 5)
        self.assertEqual(per, {"hide": 2, "move silently": 2})


class TestIDati(unittest.TestCase):
    def test_pf1e_il_bonus_cresce_con_dieci_gradi(self):
        regole = S.dati("pf1e", "creature.gradi")
        e, chiave = regole["effetti_talenti"], regole["chiave"]
        self.assertEqual(V._bonus_dei_talenti(["Skill Focus (Stealth)"], "pf1e", e, chiave, 9), ({"stealth": 3}, 0))
        self.assertEqual(V._bonus_dei_talenti(["Skill Focus (Stealth)"], "pf1e", e, chiave, 10), ({"stealth": 6}, 0))
        self.assertEqual(V._bonus_dei_talenti(["Alertness"], "pf1e", e, chiave, 12),
                         ({"perception": 4, "sense motive": 4}, 0))

    def test_ogni_abilita_dei_dati_e_un_abilita_del_plugin(self):
        # Autoipnosi manca dalle abilità 3.5 del plugin (gradi.toml): dichiarato nell'ADR-0126
        mancanti = {"dnd35": {"autohypnosis"}, "pf1e": set()}
        for sistema in ("dnd35", "pf1e"):
            regole = S.dati(sistema, "creature.gradi")
            chiave = regole["chiave"]
            self.assertTrue(regole["effetti_talenti"])
            for nome, e in regole["effetti_talenti"].items():
                self.assertTrue(e.get("a_scelta") or len(e["abilita"]) == 2, nome)
                self.assertTrue(e["fonte"], nome)
                fuori = {a for a in e.get("abilita", []) if not any(a == k or a.startswith(k + " ") for k in chiave)}
                self.assertLessEqual(fuori, mancanti[sistema], f"{sistema}: {nome}")

    def test_i_talenti_dei_dati_sono_talenti_del_plugin(self):
        for sistema in ("dnd35", "pf1e"):
            for nome in S.dati(sistema, "creature.gradi")["effetti_talenti"]:
                self.assertIsNotNone(V.VT.risolvi(sistema, nome), f"{sistema}: {nome}")


if __name__ == "__main__":
    unittest.main()
