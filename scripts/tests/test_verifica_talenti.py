"""verifica_talenti.py e la regola strutturata dei prerequisiti (ADR-0124).

Tre cose:
- D1 e D2, i difetti trovati misurando Prolog contro Python: le classi 3.5 in
  italiano contro i prerequisiti in inglese, e il livello del personaggio di
  Leadership che nessuno scriveva;
- la forma dell'uscita che l'agente legge via MCP (regola, atteso, ha, riga);
- il giro di correzione: una scheda segnalata, corretta, torna pulita.
"""
from __future__ import annotations

import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from dmcore import talenti as TL  # noqa: E402
import verifica_talenti as V  # noqa: E402

CAR = {"For": 16, "Des": 13, "Cos": 14, "Int": 13, "Sag": 10, "Car": 10}
KRUSK = REPO / "Bestiario/villain/krusk-sfondacancelli-cr14.md"


class Regola(unittest.TestCase):
    def test_d1_guerriero_in_italiano_prende_specializzazione(self):
        for livelli in ({"guerriero": 4}, {"fighter": 4}):
            s = TL.Stato(car=CAR, bab=4, livelli=livelli, talenti=["Weapon Focus"])
            self.assertEqual(TL.manca("dnd35", "Weapon Specialization", s), [], livelli)

    def test_d1_guerriero_3_non_la_prende(self):
        s = TL.Stato(car=CAR, bab=3, livelli={"guerriero": 3}, talenti=["Weapon Focus"])
        v = TL.violazioni("dnd35", "Weapon Specialization", s)
        self.assertEqual([(x["regola"], x["atteso"], x["ha"]) for x in v], [("classe.fighter", 4, 3)])

    def test_d2_leadership_conta_il_livello_del_personaggio(self):
        self.assertEqual(TL.manca("dnd35", "Leadership", TL.Stato(car=CAR, bab=4, livelli={"guerriero": 6})), [])
        self.assertEqual(TL.manca("dnd35", "Leadership", TL.Stato(car=CAR, bab=4, dv=6)), [])
        v = TL.violazioni("dnd35", "Leadership", TL.Stato(car=CAR, bab=4, livelli={"guerriero": 5}))
        self.assertEqual([(x["regola"], x["atteso"], x["ha"]) for x in v], [("classe.character", 6, 5)])

    def test_manca_e_violazioni_dicono_lo_stesso(self):
        s = TL.Stato(car={**CAR, "For": 12}, bab=2, talenti=[])
        v = TL.violazioni("dnd35", "Great Cleave", s)
        self.assertEqual([x["testo"] for x in v], TL.manca("dnd35", "Great Cleave", s))
        self.assertIn(("car.For", 13, 12), [(x["regola"], x["atteso"], x["ha"]) for x in v])
        self.assertIn(("bab", 4, 2), [(x["regola"], x["atteso"], x["ha"]) for x in v])

    def test_bonus_del_monaco_senza_prerequisiti(self):
        self.assertEqual(TL.bonus_senza_prerequisiti("dnd35", "Improved Trip", {"monk": 6}), "monk")
        self.assertIsNone(TL.bonus_senza_prerequisiti("dnd35", "Improved Trip", {"monk": 5}))
        self.assertIsNone(TL.bonus_senza_prerequisiti("dnd35", "Improved Trip", {"fighter": 6}))


def _r(en: str) -> dict:
    return {"en": en, "sistema": "dnd35", "fonte": "srd", "verificabile": True}


class Strumento(unittest.TestCase):
    def _esegui(self, *argv) -> "tuple[int, dict]":
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = V.main([*argv, "--json"])
        return rc, json.loads(buf.getvalue())

    def _sporca(self, tmp) -> Path:
        """Krusk con un talento in più di cui non ha il prerequisito (Tiro Preciso senza
        Tiro Ravvicinato). Il suo «Duro a morire» non è più l'esempio: lo dà il Berserker
        Furioso al 1° livello (ADR-0124 §11)."""
        p = Path(tmp) / KRUSK.name
        p.write_text(KRUSK.read_text(encoding="utf-8").replace("Duro a morire", "Duro a morire, Tiro Preciso", 1),
                     encoding="utf-8")
        return p

    def test_scheda_vera_pulita(self):
        rc, d = self._esegui(str(KRUSK), "--check")
        self.assertEqual((rc, d["violazioni"]), (0, []))

    def test_uscita_per_l_agente(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self._sporca(tmp)
            rc, d = self._esegui(str(p))
            self.assertEqual(rc, 0)
            v = d["violazioni"]
            self.assertEqual([(x["talento"], x["regola"], x["atteso"]) for x in v],
                             [("Precise Shot", "talento", "Point Blank Shot")])
            riga = p.read_text(encoding="utf-8").splitlines()[v[0]["riga"] - 1]
            self.assertIn("Tiro Preciso", riga)

    def test_giro_di_correzione(self):
        """Segnalata, corretta come dice la violazione, pulita: --check passa da 1 a 0."""
        with tempfile.TemporaryDirectory() as tmp:
            p = self._sporca(tmp)
            self.assertEqual(self._esegui(str(p), "--check")[0], 1)
            testo = p.read_text(encoding="utf-8").replace("Tiro Preciso", "Tiro Ravvicinato, Tiro Preciso", 1)
            p.write_text(testo, encoding="utf-8")
            rc, d = self._esegui(str(p), "--check")
            self.assertEqual((rc, d["violazioni"]), (0, []))

    def test_competenza_della_classe_non_e_una_violazione(self):
        f = {"file": "x.md", "riga": 1, "sistema": "dnd35", "car": CAR, "bab": 8,
             "livelli": {"fighter": 8}, "dv": 8, "lic": 0, "talenti": [_r("Improved Shield Bash")], "senza_regole": [], "ignoti": []}
        self.assertEqual(V.verifica(f), ([], []))
        f["livelli"] = {}
        self.assertEqual([x["regola"] for x in V.verifica(f)[0]], ["talento"])

    def test_senza_classi_il_livello_d_incantatore_non_si_giudica(self):
        f = {"file": "x.md", "riga": 1, "sistema": "dnd35", "car": CAR, "bab": 5,
             "livelli": {}, "dv": 11, "lic": 0, "talenti": [_r("Scribe Scroll")], "senza_regole": [], "ignoti": []}
        viol, nv = V.verifica(f)
        self.assertEqual((viol, [x["regola"] for x in nv]), ([], ["lic"]))

    def test_cascata_srd_poi_manuali_35(self):
        # SRD 3.5, anche i talenti dei mostri; poi i manuali 3.5 (nome sì, prerequisiti no)
        self.assertEqual(V.risolvi("dnd35", "Colpo terrificante")["fonte"], "srd-mostri")
        self.assertEqual(V.risolvi("dnd35", "Incantesimi Focalizzati")["en"], "Spell Focus")
        # manuali 3.5: i prerequisiti vengono dai dati PCGen (talenti_manuali.toml)
        r = V.risolvi("dnd35", "Robustezza Migliorata")
        self.assertEqual((r["en"], r["verificabile"], r["fonte"]),
                         ("Improved Toughness", True, "3.5 Complete Warrior"))
        # un manuale che i dati PCGen non coprono: nome sì, prerequisiti no
        r = V.risolvi("dnd35", "Abjurative Potency")
        self.assertEqual((r["verificabile"], r["fonte"][:3]), (False, "3.5"))
        # l'inglese fra parentesi decide quando l'italiano non è in lessico
        self.assertEqual(V.risolvi("dnd35", "Rune Incise (Inscribe Rune)")["en"], "Inscribe Rune")
        self.assertIsNone(V.risolvi("dnd35", "Virata"))

    def test_cascata_ultima_fonte_pf1e(self):
        # un talento che nessun libro 3.5 ha si verifica col PRD PF1e
        r = V.risolvi("dnd35", "Furious Focus")
        self.assertEqual((r["sistema"], r["verificabile"]), ("pf1e", True))
        self.assertTrue(r["fonte"].startswith("pf1e"))

    def test_talento_di_manuale_non_e_ne_buono_ne_sbagliato(self):
        f = {"file": "x.md", "riga": 1, "sistema": "dnd35", "car": CAR, "bab": 8, "livelli": {"fighter": 8},
             "dv": 8, "lic": 0, "talenti": [], "senza_regole": [V.risolvi("dnd35", "Abjurative Potency")],
             "ignoti": []}
        viol, nv = V.verifica(f)
        self.assertEqual((viol, [(x["regola"], x["talento"]) for x in nv]), ([], [("fonte", "Abjurative Potency")]))

    def test_prerequisiti_dei_manuali_35(self):
        # Critico Poderoso (Complete Warrior): Arma Focalizzata e BAB +4
        st = TL.Stato(car=CAR, bab=3, livelli={"fighter": 3}, talenti=[], dv=3)
        self.assertEqual(sorted(x["regola"] for x in TL.violazioni("dnd35", "Power Critical", st)),
                         ["bab", "talento"])
        # Ira Intimidatoria chiede l'ira: un guerriero no, un barbaro sì
        self.assertEqual([x["regola"] for x in TL.violazioni("dnd35", "Intimidating Rage", st)], ["capacita"])
        st = TL.Stato(car=CAR, bab=3, livelli={"barbarian": 3}, talenti=[], dv=3)
        self.assertEqual(TL.violazioni("dnd35", "Intimidating Rage", st), [])
        # un nome dell'SRD non viene mai sostituito dal manuale
        self.assertEqual(TL.dati("dnd35")["talenti"]["Power Attack"]["libro"], "srd")

    def test_classe_che_la_lettura_non_conosce(self):
        f = {"file": "x.md", "riga": 1, "sistema": "dnd35", "car": CAR, "bab": 5, "livelli": {"paladin": 8},
             "dv": 10, "lic": 4, "talenti": [V.risolvi("dnd35", "Divine Armor")], "senza_regole": [],
             "ignoti": [], "classi_ignote": ["Hammer of Moradin 2"]}
        viol, nv = V.verifica(f)
        self.assertEqual(viol, [])
        self.assertIn("Hammer of Moradin 2", nv[0]["nota"])

    def test_percorso_inesistente(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(V.main(["non/esiste.md"]), 2)



class PrerequisitiFisici(unittest.TestCase):
    """Movimento, taglia, tipo e attacchi naturali letti dalla scheda (ADR-0124 §9)."""

    FATTI = {"movimenti": {"volo": 60}, "taglia": -2, "tipo": "dragon", "attacchi_naturali": 4,
             "attacco_completo": True, "armatura_naturale": True, "soffio": True,
             "ts_base": {"temp": 5, "rifl": 1, "vol": 1}}

    def test_soddisfatti(self):
        import verifica_talenti as VT
        for p in ("Fly speed", "fly speed 20", "Size Huge or larger", "size Large or larger",
                  "Three or more natural attacks", "Natural armor", "breath weapon", "dragon type",
                  "Base Fortitude save bonus +2"):
            self.assertTrue(VT.giudica_altro(p, self.FATTI)[0], p)

    def test_violati_con_il_fatto_che_la_scheda_ha(self):
        import verifica_talenti as VT
        a_terra = {**self.FATTI, "movimenti": {}, "taglia": 0, "attacchi_naturali": 1}
        self.assertEqual(VT.giudica_altro("Fly speed", a_terra), (False, "nessuna velocità di volo"))
        self.assertEqual(VT.giudica_altro("size Large or larger", a_terra), (False, "taglia medium"))
        self.assertFalse(VT.giudica_altro("Three or more natural attacks", a_terra)[0])
        self.assertFalse(VT.giudica_altro("Base Reflex save bonus +2", a_terra)[0])

    def test_senza_la_riga_non_si_giudica(self):
        import verifica_talenti as VT
        vuoti = {"movimenti": None, "taglia": None, "tipo": None, "attacchi_naturali": None,
                 "armatura_naturale": None, "soffio": False, "ts_base": None}
        for p in ("Fly speed", "size Large or larger", "Three or more natural attacks", "Natural armor",
                  "breath weapon", "Base Will save bonus +4", "Member of the Ankheg Tribe"):
            self.assertIsNone(VT.giudica_altro(p, vuoti), p)
        # l'attacco singolo non prova che gli attacchi naturali siano pochi
        solo_singolo = {**self.FATTI, "attacchi_naturali": 1, "attacco_completo": False}
        self.assertIsNone(VT.giudica_altro("Three or more natural attacks", solo_singolo))

    def test_dalla_scheda_vera(self):
        import verifica_talenti as VT
        f = VT.leggi(Path(__file__).resolve().parents[2] / "Bestiario" / "mostri" / "abishai-azzurro-mano-cr11.md")
        self.assertEqual(f["fisici"]["movimenti"], {"volo": 60})
        self.assertEqual(f["fisici"]["attacchi_naturali"], 4)
        viol, nv = VT.verifica(f)
        self.assertFalse([v for v in viol + nv if v["talento"] in ("Flyby Attack", "Multiattack")])

if __name__ == "__main__":
    unittest.main()


class RazzaEAllineamento(unittest.TestCase):
    """Razza, sottotipo e allineamento come prerequisito (ADR-0124 §11)."""

    VUOTI = {"movimenti": None, "taglia": None, "attacchi_naturali": None, "armatura_naturale": None,
             "soffio": False, "ts_base": None}
    NANO = {**VUOTI, "sottotipi": {"dwarf", "hill"}, "allineamento": "LG", "tipo": "humanoid"}

    def test_razza(self):
        self.assertEqual(V.giudica_altro("PRERACE:1,Dwarf", self.NANO), (True, "sottotipo dwarf"))
        self.assertEqual(V.giudica_altro("dwarf", self.NANO), (True, "sottotipo dwarf"))
        self.assertEqual(V.giudica_altro("gnome", self.NANO), (False, "razza dwarf"))
        self.assertEqual(V.giudica_altro("PRERACE:1,Human", {**self.NANO, "sottotipi": {"umano"}})[0], True)

    def test_razza_che_la_riga_non_scrive(self):
        # il drow è scritto «(elf)»: non si sa; senza sottotipi non si sa
        self.assertIsNone(V.giudica_altro("drow", {**self.NANO, "sottotipi": {"elf"}}))
        self.assertIsNone(V.giudica_altro("dwarf", {**self.NANO, "sottotipi": None}))
        self.assertIsNone(V.giudica_altro("dwarf", {**self.VUOTI, "sottotipi": {"earth"}, "allineamento": None, "tipo": "giant"}))

    def test_sottotipo(self):
        fuoco = {**self.VUOTI, "sottotipi": {"fire", "extraplanar"}, "allineamento": "LE", "tipo": "outsider"}
        self.assertTrue(V.giudica_altro("fire subtype", fuoco)[0])
        self.assertFalse(V.giudica_altro("incorporeal subtype", fuoco)[0])
        self.assertIsNone(V.giudica_altro("dragonblood subtype", fuoco))

    def test_allineamento(self):
        self.assertEqual(V.giudica_altro("any good alignment", self.NANO), (True, "allineamento LG"))
        self.assertFalse(V.giudica_altro("nongood", self.NANO)[0])
        self.assertFalse(V.giudica_altro("evil alignment", self.NANO)[0])
        self.assertTrue(V.giudica_altro("nonlawful alignment", {**self.NANO, "allineamento": "CE"})[0])
        self.assertFalse(V.giudica_altro("PREALIGN:LE,NE,CE", self.NANO)[0])
        self.assertTrue(V.giudica_altro("nongood", {**self.NANO, "allineamento": "N"})[0])
        self.assertIsNone(V.giudica_altro("evil alignment", {**self.NANO, "allineamento": None}))

    def test_letti_dalla_scheda(self):
        f = V.leggi(REPO / "Bestiario/png/rurik-gorunn-cr10.md")
        self.assertEqual(f["fisici"]["sottotipi"], {"dwarf"})
        self.assertEqual(f["fisici"]["allineamento"], "LG")


class EccezioniDichiarate(unittest.TestCase):
    """Talenti che una regola dà senza prerequisiti (ADR-0124 §11)."""

    def _scheda(self, tipo, talenti, attributi="For 25 Des 8 Cos 17 Int 4 Sag 10 Car 5"):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        p = tmp / "prova-cr8.md"
        p.write_text(f"# Prova\n\n```statblocco\ngs: 8\ntipo: {tipo}\nattributi: {attributi}\n"
                     f"voci:\n  - Talenti: {talenti}\n```\n", encoding="utf-8")
        return V.verifica(V.leggi(p))

    def test_talento_bonus_della_creatura(self):
        viol, _ = self._scheda("Large giant, 8 DV, CE", "Attacco Poderoso, Lottare Migliorato")
        self.assertTrue([v for v in viol if v["talento"] == "Improved Grapple"])
        viol, _ = self._scheda("Large giant, 8 DV, CE", "Attacco Poderoso, Lottare Migliorato (B)")
        self.assertFalse(viol)

    def test_il_bonus_non_vale_per_chi_ha_solo_classi(self):
        viol, _ = self._scheda("Medium humanoid (human), Guerriero 8, N", "Attacco Poderoso, Lottare Migliorato (B)")
        self.assertTrue([v for v in viol if v["talento"] == "Improved Grapple"])

    def test_ex_paladino_tiene_i_livelli(self):
        """«ex-Paladin 7 / Blackguard 3»: sette livelli da paladino, nessuna classe ignota."""
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        p = tmp / "prova-cr10.md"
        p.write_text("# Prova\n\n```statblocco\ngs: 10\ntipo: Medium humanoid (dwarf), ex-Paladin 7 / Blackguard 3, LE\n"
                     "pf-dado: 10d10+30\nattributi: For 18 Des 12 Cos 16 Int 10 Sag 16 Car 16\n"
                     "voci:\n  - Talenti: Attacco Poderoso\n```\n", encoding="utf-8")
        f = V.leggi(p)
        self.assertEqual(f["livelli"].get("paladin"), 7)
        self.assertFalse([c for c in f["classi_ignote"] if "paladin" in c.lower()])

    def test_la_pietra_ioun_arancione_alza_il_livello_dell_incantatore(self):
        """SRD, orange prism: +1 al livello dell'incantatore. Paladino 8: 4, con la pietra 5."""
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        base = ("# Prova\n\n```statblocco\ngs: 8\ntipo: Medium humanoid (dwarf), Paladin 8, LG\n"
                "attributi: For 14 Des 8 Cos 14 Int 10 Sag 14 Car 14\nvoci:\n  - Talenti: Volontà di Ferro\n```\n")
        senza, con = tmp / "senza-cr8.md", tmp / "con-cr8.md"
        senza.write_text(base, encoding="utf-8")
        con.write_text(base + "\nEquipaggiamento: *pietra ioun, prisma arancione*.\n", encoding="utf-8")
        self.assertEqual(V.leggi(senza)["lic"], 4)
        self.assertEqual(V.leggi(con)["lic"], 5)

    def test_talento_che_la_classe_del_manuale_concede(self):
        self.assertEqual(V.talenti_concessi({"frenzied berserker": 1}), {"Diehard"})
        self.assertEqual(V.talenti_concessi({"fighter": 4}), set())

    def test_talento_equivalente(self):
        """Expeditious Dodge vale Dodge come prerequisito: Mobility non è una violazione."""
        viol, _ = self._scheda("Medium humanoid (human), Guerriero 4, N", "Expeditious Dodge, Mobility",
                               "For 14 Des 15 Cos 12 Int 10 Sag 10 Car 10")
        self.assertFalse([v for v in viol if v["talento"] == "Mobility"])
