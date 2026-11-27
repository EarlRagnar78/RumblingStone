"""I requisiti delle classi di prestigio (ADR-0126, lotto 3-bis)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dmcore import prestigio as PR  # noqa: E402

RADICE = Path(__file__).resolve().parents[2]
ALLINEAMENTI = ["LG", "NG", "CG", "LN", "N", "CN", "LE", "NE", "CE"]


def in_regola(req: dict) -> dict:
    """I fatti di un personaggio che ha tutti i requisiti della classe."""
    return {
        "bab_prima": req.get("bab", 0), "gradi_massimi": 40,
        "abilita": {PR.senza_parentesi(a): 40 for gr in req.get("abilita", ()) for a in gr["fra"]},
        "talenti": {PR.senza_parentesi(t) for gr in req.get("talenti", ()) for t in gr["fra"]},
        "razza": (req.get("razza") or [""])[0],
        "razze_it": {PR.senza_parentesi(r): () for r in req.get("razza", ())},
        "allineamento": (req.get("allineamento") or ["N"])[0],
        "classi": {"wizard": 20, "cleric": 20}, "car": {},
    }


def campi(scarti: "list[dict]") -> "set[str]":
    return {x["campo"] for x in scarti}


class TestDati(unittest.TestCase):
    def test_le_classi_dell_srd(self):
        a = PR.classe("assassin")
        self.assertEqual(a["allineamento"], ["LE", "NE", "CE"])
        self.assertEqual(a["abilita"], [{"quanti": 3, "fra": {"disguise": 4, "hide": 8, "move silently": 8}}])
        self.assertEqual(a["non_verificati"], 1)          # lo speciale (uccidere per entrare) non si copia
        d = PR.classe("Dwarven Defender")
        self.assertEqual((d["bab"], d["razza"], d["allineamento"]), (7, ["dwarf"], ["LG", "LN", "LE"]))
        self.assertEqual([g["fra"] for g in d["talenti"]], [["dodge"], ["endurance"], ["toughness"]])
        self.assertEqual(PR.classe("archmage")["incantesimi"], [{"tipo": "arcane", "livello": 7}])
        self.assertEqual(PR.classe("mystic theurge")["incantesimi"],
                         [{"tipo": "divine", "livello": 2}, {"tipo": "arcane", "livello": 2}])

    def test_pf1e_ha_i_suoi_numeri(self):
        # PRD: l'assassino chiede Camuffare 2 e Furtività 5, non i gradi della 3.5
        a = PR.classe("assassin", "pf1e")
        self.assertEqual(a["abilita"], [{"quanti": 2, "fra": {"disguise": 2, "stealth": 5}}])
        self.assertEqual(len(PR.requisiti("pf1e")["prestigio"]), 10)
        self.assertIsNone(PR.classe("blackguard", "pf1e"))

    def test_l_srd_vince_sui_manuali(self):
        fonti = {c["fonte"] for c in PR.requisiti()["prestigio"].values()}
        self.assertIn("SRD 3.5, Prestige Classes", fonti)
        self.assertEqual(PR.classe("blackguard")["fonte"], "SRD 3.5, Prestige Classes")
        self.assertGreater(len(PR.requisiti()["prestigio"]), 450)

    def test_solo_nomi_e_numeri(self):
        # nessun testo dei manuali: un nome di talento, abilità o razza è corto e non ha frasi
        for nome, c in PR.requisiti()["prestigio"].items():
            self.assertLessEqual(set(c), {"fonte", "non_verificati", "bab", "abilita", "talenti", "razza",
                                          "allineamento", "incantesimi", "diverge", "avanza"}, nome)
            # l'avanzamento d'incantatore (lotto 3-ter): un tipo di una parola o due e dei numeri
            self.assertLessEqual(set(c.get("avanza", {})), {"tipo", "livelli", "diverge"}, nome)
            self.assertLess(len(c.get("avanza", {}).get("tipo", "")), 30, nome)
            voci = [t for g in c.get("talenti", ()) for t in g["fra"]] + c.get("razza", []) \
                + [a for g in c.get("abilita", ()) for a in g["fra"]]
            for v in voci:
                self.assertLess(len(v), 70, f"{nome}: {v}")
                self.assertNotRegex(v, r"[.;:]|\bmust\b|\bthe character\b", f"{nome}: {v}")

    def test_ogni_classe_si_giudica_e_ogni_requisito_tolto_si_vede(self):
        """Per tutte le classi dei dati: chi ha i requisiti passa, e togliere un
        requisito qualunque dà uno scarto su quel requisito."""
        viste = 0
        tutte = [(s, n, r) for s in ("dnd35", "pf1e") for n, r in PR.requisiti(s)["prestigio"].items()]
        for sistema, nome, req in tutte:
            buoni = in_regola(req)
            self.assertEqual(PR.giudica(req, buoni, sistema)[0], [], nome)
            rotture = []
            if req.get("bab"):
                rotture.append(("bab", {"bab_prima": req["bab"] - 1}))
            if "abilita" in req:
                minimo = min(sorted(gr["fra"].values())[gr["quanti"] - 1] for gr in req["abilita"])
                rotture.append(("gradi.massimo", {"gradi_massimi": minimo - 1}))
                rotture.append(("gradi", {"abilita": {}}))
            if "talenti" in req:
                rotture.append(("talenti", {"talenti": set()}))
            if "razza" in req:
                rotture.append(("razza", {"razza": "xyz"}))
            if "allineamento" in req and len(req["allineamento"]) < 9:
                rotture.append(("allineamento", {"allineamento": next(a for a in ALLINEAMENTI
                                                                      if a not in req["allineamento"])}))
            if "incantesimi" in req:
                rotture.append(("incantesimi", {"classi": {"fighter": 20}}))
            for campo, cambio in rotture:
                self.assertIn(campo, campi(PR.giudica(req, {**buoni, **cambio}, sistema)[0]), f"{sistema} {nome}: {campo}")
                viste += 1
        self.assertGreater(viste, 1200)


class TestGiudizi(unittest.TestCase):
    def test_lo_slot_dei_soli_incantesimi_bonus_conta(self):
        # paladino 8: la tabella dà 0 di 2°, lo slot viene dalla Saggezza a 14
        req = {"incantesimi": [{"tipo": "divine", "livello": 2}]}
        self.assertEqual(PR.giudica(req, {"classi": {"paladin": 8}, "car": {"Sag": 14}})[0], [])
        self.assertEqual(campi(PR.giudica(req, {"classi": {"paladin": 8}, "car": {"Sag": 12}})[0]), {"incantesimi"})
        self.assertEqual(campi(PR.giudica(req, {"classi": {"wizard": 20}, "car": {"Int": 20}})[0]), {"incantesimi"})

    def test_la_classe_sconosciuta_non_e_una_violazione(self):
        req = {"incantesimi": [{"tipo": "arcane", "livello": 3}]}
        scarti, nv = PR.giudica(req, {"classi": {"warmage": 9}, "classi_ignote": True})
        self.assertEqual((scarti, campi(nv)), ([], {"incantesimi"}))

    def test_un_talento_non_letto_lascia_il_dubbio(self):
        req = {"talenti": [{"quanti": 1, "fra": ["cleave"]}]}
        scarti, nv = PR.giudica(req, {"talenti": {"power attack"}, "talenti_ignoti": True})
        self.assertEqual((scarti, campi(nv)), ([], {"talenti"}))
        self.assertEqual(campi(PR.giudica(req, {"talenti": {"power attack"}})[0]), {"talenti"})

    def test_il_teurgo_vuole_tutte_e_due_le_magie(self):
        req = PR.classe("mystic theurge")
        fatti = {**in_regola(req), "classi": {"cleric": 3}, "car": {"Sag": 14}}
        self.assertEqual([x["atteso"] for x in PR.giudica(req, fatti)[0]], ["arcane 2°"])
        fatti["classi"] = {"cleric": 3, "wizard": 3}
        self.assertEqual(PR.giudica(req, fatti)[0], [])

    def test_la_classe_senza_dati_si_dichiara(self):
        self.assertEqual(campi(PR.giudica({"fonte": "x", "non_verificati": 0}, {})[1]), {"speciali"})

    def test_la_parentesi_del_talento_non_si_giudica(self):
        req = {"talenti": [{"quanti": 1, "fra": ["weapon focus (warhammer)"]}]}
        self.assertEqual(PR.giudica(req, {"talenti": {"weapon focus"}})[0], [])

    def test_quanti_fra(self):
        req = {"abilita": [{"quanti": 1, "fra": {"craft (gemcutting)": 8, "craft (stonecarving)": 8}}]}
        self.assertEqual(PR.giudica(req, {"gradi_massimi": 12, "abilita": {"craft": 9}})[0], [])
        self.assertEqual(campi(PR.giudica(req, {"gradi_massimi": 12, "abilita": {"craft": 7}})[0]), {"gradi"})

    def test_i_gradi_prima_dell_ingresso(self):
        # assassino dopo 4 livelli: il massimo dei gradi è 7, Nascondersi ne chiede 8
        req = PR.classe("assassin")
        fatti = {**in_regola(req), "gradi_massimi": 7}
        s = PR.giudica(req, fatti)[0]
        self.assertEqual([(x["campo"], x["scritto"], x["atteso"]) for x in s], [("gradi.massimo", 7, 8)])

    def test_la_penalita_di_armatura_lascia_il_dubbio(self):
        req = {"abilita": [{"quanti": 1, "fra": {"hide": 5}}]}
        scarti, nv = PR.giudica(req, {"gradi_massimi": 9, "abilita": {"hide": 2}, "incerte": {"hide"}})
        self.assertEqual((scarti, campi(nv)), ([], {"gradi"}))

    def test_la_razza_senza_nome_italiano_resta_dubbia(self):
        req = {"razza": ["svirfneblin"]}
        self.assertEqual(campi(PR.giudica(req, {"razza": "Umanoide Medio (gnomo)"})[1]), {"razza"})
        req = {"razza": ["dwarf"]}
        it = {"dwarf": ("nano",)}
        self.assertEqual(PR.giudica(req, {"razza": "Umanoide Medio (nano)", "razze_it": it}), ([], []))
        self.assertEqual(campi(PR.giudica(req, {"razza": "Medium humanoid (orc)", "razze_it": it})[0]), {"razza"})


class TestScheda(unittest.TestCase):
    def _con(self, nome: str, prima: str, dopo: str):
        import verifica_scheda as V
        p = next((RADICE / "Bestiario").rglob(nome))
        testo = p.read_text(encoding="utf-8")
        self.assertIn(prima, testo)
        with tempfile.TemporaryDirectory() as d:
            q = Path(d) / nome
            q.write_text(testo.replace(prima, dopo), encoding="utf-8")
            return V.prestigio(q)

    def test_il_berserker_senza_un_talento(self):
        v, _ = self._con("krusk-sfondacancelli-cr14.md", "Ira Distruttiva", "Robustezza")
        self.assertEqual([x["regola"] for x in v], ["prestigio.talenti"])

    def test_il_berserker_in_regola(self):
        import verifica_scheda as V
        self.assertEqual(V.prestigio(next((RADICE / "Bestiario").rglob("krusk-sfondacancelli-cr14.md"))), ([], []))

    def test_i_requisiti_speciali_restano_fra_i_non_verificabili(self):
        import verifica_scheda as V
        v, nv = V.prestigio(next((RADICE / "Bestiario").rglob("rurik-gorunn-cr10.md")))
        self.assertEqual(v, [])
        self.assertEqual([x["regola"] for x in nv], ["prestigio.speciali"])


class TestCancello(unittest.TestCase):
    """Le violazioni trovate nel Bestiario aspettano il DM: cambiare i livelli di
    un PNG è una scelta sua. Nessun'altra scheda ne ha."""

    IN_ATTESA: "set[str]" = set()

    def test_il_bestiario_non_ha_altre_violazioni(self):
        import verifica_scheda as V
        trovate, attese = [], set()
        for p in sorted((RADICE / "Bestiario").rglob("*.md")):
            v = V.prestigio(p)[0]
            if p.name in self.IN_ATTESA:
                attese |= {p.name} if v else set()
            else:
                trovate += [f"{x['file']}:{x['riga']} {x['testo']}" for x in v]
        self.assertEqual(trovate, [])
        self.assertEqual(attese, self.IN_ATTESA, "una scheda in attesa è stata corretta: toglierla dall'elenco")


if __name__ == "__main__":
    unittest.main()
