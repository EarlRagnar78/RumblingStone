"""quiz_lettura: il confronto con la chiave, le tre classi, e le chiavi del repo.

I casi vengono dalla prima esecuzione su DEF-4: «12» che accettava «120 minuti»,
«runa» che avrebbe accettato «runaio», «avi» che la chiave non conosceva.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import quiz_lettura as ql  # noqa: E402


def chiave(n=10, **kw):
    base = {"stato": "bozza",
            "domande": [{"id": f"q{i}", "domanda": f"domanda {i}", "accettate": [["x"]]}
                        for i in range(1, n + 1)]}
    base.update(kw)
    return base


class TestIlConfronto(unittest.TestCase):

    def test_la_radice_accetta_le_desinenze(self):
        self.assertTrue(ql.giusta("Le tacche sono otto", [["tacch", "otto"]]))

    def test_maiuscole_e_accenti_non_contano(self):
        self.assertTrue(ql.giusta("RE THORÈK comanda", [["thorek"]]))

    def test_servono_tutte_le_parole_di_un_alternativa(self):
        self.assertFalse(ql.giusta("uccidere Zog'tar", [["zog", "notte"]]))
        self.assertTrue(ql.giusta("uccidere Zog'tar di notte", [["zog", "notte"]]))

    def test_basta_una_delle_alternative(self):
        self.assertTrue(ql.giusta("lo salvano gli avi", [["antenat"], ["avi", "salv"]]))

    def test_un_numero_combacia_esatto(self):
        self.assertFalse(ql.giusta("120 minuti", [["12", "minut"]]))
        self.assertTrue(ql.giusta("12 minuti", [["12", "minut"]]))

    def test_la_radice_composta_non_confonde_runa_e_runaio(self):
        acc = [["runa", "vincol"], ["catena"]]
        self.assertFalse(ql.giusta("un runaio esiliato", acc))
        self.assertTrue(ql.giusta("una runa-vincolo sulla scaglia", acc))

    def test_non_lo_so_e_sbagliata(self):
        self.assertFalse(ql.giusta("non lo so", [["thorek"]]))


class TestLeTreClassi(unittest.TestCase):

    def setUp(self):
        self.k = {"domande": [{"id": "q1", "domanda": "?", "accettate": [["thorek"]]}]}

    def test_dagli_appunti(self):
        r = ql.classifica(self.k, {"q1": "Re Thorek"}, {"q1": "Re Thorek"})
        self.assertEqual(r[0]["esito"], ql.GIUSTA_APPUNTI)

    def test_solo_a_libro_aperto(self):
        r = ql.classifica(self.k, {"q1": "non lo so"}, {"q1": "Re Thorek"})
        self.assertEqual(r[0]["esito"], ql.SOLO_APERTO)

    def test_sbagliata_anche_aperto(self):
        r = ql.classifica(self.k, {"q1": "non lo so"}, {"q1": "il capitano"})
        self.assertEqual(r[0]["esito"], ql.SBAGLIATA)

    def test_senza_libro_aperto_non_si_decide(self):
        r = ql.classifica(self.k, {}, None)
        self.assertEqual(r[0]["esito"], ql.NON_MISURATA)


class TestLaChiave(unittest.TestCase):

    def test_una_chiave_buona_passa(self):
        self.assertEqual(ql.problemi_della_chiave(chiave()), [])

    def test_lo_stato_e_obbligatorio(self):
        self.assertTrue(ql.problemi_della_chiave(chiave(stato="definitiva")))

    def test_troppe_poche_domande(self):
        self.assertTrue(ql.problemi_della_chiave(chiave(n=9)))
        self.assertTrue(ql.problemi_della_chiave(chiave(n=16)))

    def test_id_ripetuto(self):
        k = chiave()
        k["domande"][1]["id"] = "q1"
        self.assertTrue(ql.problemi_della_chiave(k))

    def test_alternativa_vuota(self):
        k = chiave()
        k["domande"][0]["accettate"] = [[]]
        self.assertTrue(ql.problemi_della_chiave(k))

    def test_il_modulo_deve_esistere(self):
        self.assertTrue(ql.problemi_della_chiave(chiave(modulo="non/esiste.md")))


class TestIlRepo(unittest.TestCase):

    def test_le_chiavi_del_repo_sono_ben_formate(self):
        self.assertEqual(ql.main(["--check"]), 0)

    def test_l_esperimento_di_def4_si_rigenera(self):
        """I numeri di plans/esperimenti/quiz-def4/RISULTATI.md escono dai file.
        La versione «riquadro» usa le risposte a libro aperto di «dopo»."""
        d = ROOT / "plans" / "esperimenti" / "quiz-def4"
        import json
        k = json.loads((ROOT / "plans" / "quiz" / "ARC07-DEF-4.json").read_text(encoding="utf-8"))
        conti = {}
        for v, aperto in (("prima", "prima"), ("dopo", "dopo"), ("riquadro", "dopo")):
            app = json.loads((d / f"{v}-RISPOSTE-APPUNTI.json").read_text(encoding="utf-8"))
            ape = json.loads((d / f"{aperto}-RISPOSTE-APERTO.json").read_text(encoding="utf-8"))
            righe = ql.classifica(k, app, ape)
            conti[v] = tuple(sum(r["esito"] == e for r in righe)
                             for e in (ql.GIUSTA_APPUNTI, ql.SOLO_APERTO, ql.SBAGLIATA))
        self.assertEqual(conti, {"prima": (6, 4, 4), "dopo": (6, 8, 0), "riquadro": (6, 8, 0)})

    def test_la_chiave_di_def4_e_approvata(self):
        import json
        k = json.loads((ROOT / "plans" / "quiz" / "ARC07-DEF-4.json").read_text(encoding="utf-8"))
        self.assertEqual(k["stato"], "approvata")


if __name__ == "__main__":
    unittest.main()
