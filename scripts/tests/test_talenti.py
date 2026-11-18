"""I talenti dei PNG generati: quanti, quali, e con i prerequisiti (lotto 3 delle regole complete).

I difetti che questi test esistono per impedire:

- un PNG con un solo «talento firma» dove la regola gliene dà sette (il guerriero 7
  del 3.5 prima del 2026-11-10);
- un talento preso senza i prerequisiti (Sbilanciare Migliorato con Int 8);
- i talenti bonus di classe dimenticati quando la tabella non li chiama «bonus feat»
  (il Colpo Senz'Armi Migliorato del monaco, il talento di squadra del tattico del
  cavaliere, lo stile del ranger 3.5);
- un talento mitico dato a un PNG che non ha gradi mitici;
- i dati dei talenti scritti a mano invece che dal PRD/SRD (il --check, quando le
  fonti sono in cache).

Solo `unittest`.
"""
from __future__ import annotations

import os
import random
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from dmcore import talenti as TL  # noqa: E402
import genera_creatura as G  # noqa: E402

ESTRATTORE = REPO / "plans/esperimenti/regole-complete-2026-11-10/estrai_talenti.py"
CACHE = Path(os.environ.get("RUMBLINGSTONE_SRD_CACHE", Path.home() / ".cache/rumblingstone/srd"))


def _talenti(blocco) -> "list[str]":
    riga = next(v for v in blocco.voci if v.startswith("Talenti:"))
    return [t.strip() for t in re.split(r",\s*(?![^()]*\))", riga.split(":", 1)[1]) if t.strip()]


class Dati(unittest.TestCase):
    @unittest.skipUnless((CACHE / "PSRD-Data-76ea47846041").is_dir()
                         and (CACHE / "srd-v3.5-md-c7f30a0ce11a").is_dir(),
                         "PRD o SRD non in cache (riscontro_srd.py scarica)")
    def test_i_dati_sono_quelli_delle_fonti(self):
        r = subprocess.run([sys.executable, str(ESTRATTORE), "--check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_numero_generale_dei_due_manuali(self):
        # 3.5: 1 + 1 ogni 3 livelli; PF1e: 1 ogni livello dispari
        self.assertEqual([TL.generali("dnd35", n) for n in (1, 3, 6, 7, 20)], [1, 2, 3, 3, 7])
        self.assertEqual([TL.generali("pf1e", n) for n in (1, 2, 3, 7, 20)], [1, 1, 2, 4, 10])

    def test_prerequisiti_letti_dalla_fonte(self):
        for sistema in ("dnd35", "pf1e"):
            s = TL.Stato(car={"Int": 8, "For": 16}, bab=7, livelli={})
            m = TL.manca(sistema, "Improved Trip", s)
            self.assertTrue(any(x.startswith("Int 13") for x in m), m)
            self.assertIn("Combat Expertise", m)
            s = TL.Stato(car={"Int": 13}, bab=7, livelli={}, talenti=["Combat Expertise"])
            self.assertEqual(TL.manca(sistema, "Improved Trip", s), [])

    def test_talento_mitico_mai_lecito(self):
        s = TL.Stato(car={"For": 20}, bab=20, livelli={"fighter": 20}, talenti=["Power Attack"])
        self.assertTrue(TL.manca("pf1e", "Power Attack, Mythic", s))

    def test_bonus_dal_testo_delle_capacita(self):
        d = TL.dati("pf1e")["bonus"]
        self.assertIn("Improved Unarmed Strike", d["monk"]["concessi"]["1"])
        self.assertIn("Improved Unarmed Strike", d["brawler"]["concessi"]["1"])
        self.assertEqual(d["cavalier"]["tipi_livello"]["1"], ["Teamwork"])
        self.assertEqual(sorted(d["hunter"]["scelte"]["2"]), ["Outflank", "Precise Shot"])
        self.assertTrue(d["monk"]["senza_prerequisiti"])
        self.assertNotIn("shaman", d)   # la Mobilità è dell'animale di uno spirito, non dello sciamano
        d3 = TL.dati("dnd35")["bonus"]
        self.assertIn("Improved Unarmed Strike", d3["monaco"]["concessi"]["1"])
        self.assertEqual(d3["ranger"]["stili"]["Archery"]["2"], ["Rapid Shot"])


class Generatore(unittest.TestCase):
    def test_guerriero_7_del_35_ha_sette_talenti_leciti(self):
        sb, conto = G.genera(7, classe=G._classe("guerriero:7"), rng=random.Random(1), talenti="dnd35")
        nomi = _talenti(sb)
        self.assertEqual(len(nomi), 7, nomi)
        self.assertEqual(TL.quanti("dnd35", {"guerriero": 7}), 7)
        self.assertNotIn("Sbilanciare migliorato", nomi)   # Int 8 nel profilo del bruto

    def test_fighter_7_pf1e_e_monaco(self):
        from dmcore import sistemi as S
        from dmcore import creature_pf1e as CP
        for cl, n in (("fighter", 8), ("monk", 9), ("cavalier", 6), ("wizard", 6), ("cleric", 4)):
            classi = CP.leggi_classi(f"{cl}:7", S.dati("pf1e", "creature.costruzione"))
            sb, _ = G.genera_png_pf1e(7, classi=classi, rng=random.Random(1))
            self.assertEqual(len(_talenti(sb)), n, (cl, _talenti(sb)))

    def test_ogni_talento_generale_ha_i_prerequisiti(self):
        rng = random.Random(3)
        for ruolo in ("bruto", "tiratore", "controllore", "comandante"):
            st = TL.Stato(car={"For": 14, "Des": 15, "Cos": 12, "Int": 10, "Sag": 10, "Car": 8},
                          bab=5, livelli={"fighter": 5})
            scelta = TL.scegli("pf1e", ruolo, st, rng=rng)
            presi: "list[str]" = []
            for en, origine in scelta.talenti:
                if origine == "generale":
                    s = TL.Stato(st.car, st.bab, st.livelli, st.lic, list(presi))
                    self.assertEqual(TL.manca("pf1e", en, s), [], (ruolo, en))
                presi.append(en)

    def test_effetti_sui_numeri(self):
        e = TL.effetti("pf1e", ["Improved Initiative", "Toughness", "Iron Will"], dv=7)
        self.assertEqual((e["iniziativa"], e["pf"], e["vol"]), (4, 7, 2))
        self.assertEqual(TL.effetti("dnd35", ["Toughness"], dv=7)["pf"], 3)


class Focalizzati(unittest.TestCase):
    """Incantesimi focalizzati nel generatore (2026-11-17): il nome scriveva «(bene, caos,
    legge o male)» invece della scuola, e il talento finiva anche su mostri che non
    lanciano nulla (card del DM: si prende il talento seguente del ruolo)."""

    SCUOLE = {"abiurazione", "evocazione", "divinazione", "ammaliamento", "invocazione",
              "illusione", "necromanzia", "trasmutazione"}

    def _focalizzati(self, sb):
        return [t for t in _talenti(sb) if t.lower().startswith("incantesimi focalizzati")]

    def test_nome_italiano_senza_le_varianti_d_allineamento(self):
        self.assertEqual(TL.italiano("dnd35", "Spell Focus"), "Incantesimi focalizzati")

    def test_mago_controllore_ha_una_scuola_e_la_stessa_nel_superiore(self):
        sb, _ = G.genera(9, ruolo="controllore", classe=G._classe("mago:9"), rng=random.Random(3),
                         talenti="dnd35")
        foc = self._focalizzati(sb)
        self.assertEqual(len(foc), 2, foc)
        scuole = {re.search(r"\((\w+)\)$", t).group(1) for t in foc}
        self.assertEqual(len(scuole), 1, foc)
        self.assertLessEqual(scuole, self.SCUOLE)

    def test_mago_blaster_focalizza_l_invocazione(self):
        sb, _ = G.genera(9, ruolo="blaster", classe=G._classe("mago:9"), rng=random.Random(3), talenti="dnd35")
        self.assertIn("Incantesimi focalizzati (invocazione)", _talenti(sb))

    def test_mostro_senza_incantesimi_prende_un_altro_talento(self):
        for seme in range(5):
            sb, _ = G.genera(9, ruolo="controllore", rng=random.Random(seme), talenti="dnd35")
            self.assertEqual(self._focalizzati(sb), [], _talenti(sb))

    def test_la_nota_nel_conto_solo_se_l_esclusione_cambia_la_scelta(self):
        # impronte.py, 2026-11-18: la nota usciva su ogni blocco senza incantesimi
        nota = "niente Incantesimi focalizzati"
        for ruolo, attesa in (("bruto", False), ("tiratore", False), ("controllore", True)):
            for seme in range(3):
                _, c = G.genera(9, ruolo=ruolo, rng=random.Random(seme), talenti="dnd35")
                self.assertEqual(any(nota in r for r in c.righe), attesa, (ruolo, seme))

    def test_nome_con_la_virgola_dentro(self):
        voci = ["Preparati — 8°: labirinto, parola del potere, stordire · 3°: palla di fuoco"]
        self.assertEqual(G.incantesimi_del_blocco(voci),
                         [(8, "labirinto"), (8, "parola del potere, stordire"), (3, "palla di fuoco")])

    def test_parita_vince_la_scuola_del_livello_piu_alto(self):
        # sonno (ammaliamento, 1°) contro palla di fuoco (invocazione, 3°)
        self.assertEqual(G.scuola_prevalente([(1, "sonno"), (3, "palla di fuoco")])[0], "invocazione")
        self.assertEqual(G.scuola_prevalente([(1, "sonno"), (2, "risata incontenibile di Tasha"),
                                               (3, "palla di fuoco")])[0], "ammaliamento")

    def test_incantesimo_dell_apg_ha_la_scuola_del_prd(self):
        self.assertEqual(G.scuola_prevalente([(1, "stumble gap")])[0], "evocazione")

    def test_incantesimi_delle_liste_pf1e_hanno_la_scuola_del_prd(self):
        # ricontrollo del 2026-11-18: 912 voci delle liste PF1e non avevano scuola
        self.assertEqual(G.scuola_prevalente([(1, "Spezzalinee")])[0], "trasmutazione")
        self.assertEqual(G.scuola_prevalente([(1, "Linebreaker")])[0], "trasmutazione")
        self.assertEqual(G.scuola_prevalente([(1, "Blurred Movement")])[0], "illusione")
        # «universal» non si focalizza, e un nome ignoto non ha scuola
        self.assertIsNone(G.scuola_prevalente([(9, "Wish")])[0])
        self.assertIsNone(G.scuola_prevalente([(1, "nome inventato")])[0])
        from dmcore import sistemi as S
        pf = S.dati("pf1e", "creature.liste_incantesimi")
        usati = {n for liv in pf["liste"].values() for voci in liv.values() for n in voci}
        self.assertEqual(usati - set(pf["scuole"]), set())

    def test_senza_scuola_nelle_tabelle_prende_un_altro_talento(self):
        # revisione di Codex sulla #468: il talento usciva senza scuola sull'alchimista PF1e.
        # Dal 2026-11-18 i suoi estratti hanno la scuola del PRD: qui si guarda solo che il
        # talento, se c'è, porti la scuola
        from dmcore import sistemi as S
        from dmcore import creature_pf1e as CP
        dati = S.dati("pf1e", "creature.costruzione")
        for liv, ruolo, seme in ((1, "controllore", 0), (1, "blaster", 0), (3, "controllore", 1)):
            sb, _ = G.genera_png_pf1e(liv, ruolo=ruolo, classi=CP.leggi_classi(f"alchemist:{liv}", dati),
                                      rng=random.Random(seme))
            for t in self._focalizzati(sb):
                self.assertRegex(t, r"\((\w+)\)$", (liv, ruolo, seme, _talenti(sb)))


if __name__ == "__main__":
    unittest.main()


class Prestigio(unittest.TestCase):
    """Lotto 4: i requisiti d'accesso delle classi di prestigio PF1e."""

    def _png(self, via: str):
        from dmcore import sistemi as S
        from dmcore import creature_pf1e as CP
        return G.genera_png_pf1e(9, classi=CP.leggi_classi(via, S.dati("pf1e", "creature.costruzione")),
                                 rng=random.Random(1), ruolo="tiratore")

    def test_requisiti_letti_dal_prd(self):
        r = TL.dati("pf1e")["requisiti"]
        self.assertEqual(len(r), 18)
        self.assertEqual(r["arcane archer"]["bab"], 6)
        self.assertEqual(r["arcane archer"]["incantesimi"], {"arcani": 1})
        self.assertEqual(r["mystic theurge"]["incantesimi"], {"arcani": 2, "divini": 2})
        self.assertEqual(r["holy vindicator"]["oppure"], [["Alignment Channel", "Elemental Channel"]])

    def test_via_legale_prende_i_talenti_richiesti(self):
        sb, conto = self._png("fighter:6,wizard:1,arcane archer:1")
        testo = "\n".join(conto.righe)
        self.assertNotIn("✗", testo)
        nomi = {TL.nome_inglese("pf1e", t) for t in _talenti(sb)}
        self.assertTrue({"Point-Blank Shot", "Precise Shot", "Weapon Focus"} <= nomi, nomi)

    def test_via_illegale_lo_dice(self):
        _, conto = self._png("wizard:7,arcane archer:1")
        testo = "\n".join(conto.righe)
        self.assertIn("✗ BAB +6 (ha +3)", testo)
        self.assertIn("non si entra", testo)

    def test_sciamano_ha_le_orazioni(self):
        # il PRD non le ha in spell_lists: si leggono da «0-Level Shaman Spells» (ACG)
        import tomllib
        with open(REPO / "sistemi/pf1e/dati/liste_incantesimi.toml", "rb") as fh:
            zero = tomllib.load(fh)["liste"]["shaman"]["0"]
        self.assertEqual(len(zero), 17)
        self.assertIn("Stabilize", zero)
