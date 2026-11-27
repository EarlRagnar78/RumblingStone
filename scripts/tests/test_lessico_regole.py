"""lessico_regole.py legge i talenti delle schede e li confronta con le fonti giuste.

Il DM, 2026-11-07: vincoli sui termini ufficiali di 3.5 e PF1e «una volta per
tutte», e per i moduli PF1e la tabella diretta italiano → PF1e, mai il passaggio
per la 3.5. Queste prove non usano la rete: l'indice delle fonti è finto.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import lessico_regole as L  # noqa: E402

# Indice finto: tre talenti dell'SRD 3.5 e uno del PRD.
IDX = {
    L.norma("Power Attack"): [{"fonte": "srd35", "tipo": "talento", "nome": "Power Attack"}],
    L.norma("Cleave"): [{"fonte": "srd35", "tipo": "talento", "nome": "Cleave"}],
    L.norma("Weapon Finesse"): [{"fonte": "srd35", "tipo": "talento", "nome": "Weapon Finesse"},
                                {"fonte": "pf1", "tipo": "talento", "nome": "Weapon Finesse"}],
}
ITA = L.mappa_italiana([
    {"it": "Attacco Poderoso", "srd35": "Power Attack", "pf1": "Power Attack"},
    {"it": "Incalzare", "srd35": "Cleave", "pf1": "Cleave", "varianti": "Fendere"},
    {"it": "Arma Accurata", "srd35": "Weapon Finesse", "pf1": "Weapon Finesse",
     "varianti": "Finezza nell'Arma"},
])
PF1 = {L.norma("Arma Accurata"): {"it": "Arma Accurata", "pf1": "Weapon Finesse"},
       L.norma("Attacco Poderoso"): {"it": "Attacco Poderoso", "pf1": "Power Attack"}}


def esiti(testo: str, file: str = "modulo.md") -> list[tuple[str, str]]:
    return [(r["termine"], r["esito"]) for r in L.controlla_testo(testo, IDX, ITA, file, PF1)]


class TestLetturaDelleRighe(unittest.TestCase):
    def test_norma_toglie_tipo_accenti_e_maiuscole(self):
        self.assertEqual(L.norma("Improved Trip <small>[General]</small>"), L.norma("improved trip"))
        self.assertEqual(L.norma("Volontà di Ferro"), L.norma("volonta di ferro"))

    def test_legge_tutti_i_talenti_separati_da_punto_in_mezzo(self):
        self.assertEqual(L.termini_della_riga("Attacco Poderoso · Incalzare · Arma Accurata"),
                         ["Attacco Poderoso", "Incalzare", "Arma Accurata"])

    def test_si_ferma_al_campo_seguente(self):
        self.assertEqual(L.termini_della_riga("Incalzare, Attacco Poderoso **Abilità** Scalare +5"),
                         ["Incalzare", "Attacco Poderoso"])

    def test_segue_l_elenco_che_va_a_capo(self):
        testo = "**Talenti**: Attacco Poderoso · Arma\nAccurata\n**Abilità**: Scalare +4\n"
        self.assertIn(("Attacco Poderoso", "tabella"), esiti(testo))
        self.assertEqual(len(esiti(testo)), 2)

    def test_toglie_la_sigla_del_manuale_attaccata(self):
        self.assertEqual(L.termini_della_riga("GoadCAd, Improved Initiative"), ["Goad", "Improved Initiative"])

    def test_divide_sulla_e_ma_non_i_nomi_che_la_contengono(self):
        self.assertEqual(L.termini_della_riga("Incalzare e Attacco Poderoso, Creare Armi e Armature Magiche"),
                         ["Incalzare", "Attacco Poderoso", "Creare Armi e Armature Magiche"])

    def test_campo_qs_chiude_i_talenti(self):
        self.assertEqual(L.termini_della_riga("Allerta, Iniziativa Migliorata · **QS** Anfibio"),
                         ["Allerta", "Iniziativa Migliorata"])
        self.assertEqual(L.termini_della_riga("Allerta · QS Anfibio"), ["Allerta"])

    def test_sigle_cadv_e_ph(self):
        self.assertEqual(L.termini_della_riga("GoadCAdv, Improved TripPH e Combat ExpertisePH"),
                         ["Goad", "Improved Trip", "Combat Expertise"])

    def test_la_prosa_non_e_un_elenco_di_talenti(self):
        testo = ("they've got more feats. Basically, take two.\n"
                 "Elusive Target is a feat worth consideration, I'm told.\n"
                 "Un guerriero 8 ha 8 talenti (3 di livello, 5 bonus) e la scheda.\n"
                 "- Talenti e capacità: Death Attack, Schivare Prodigioso\n"
                 "## Feats: Key Categories\n")
        self.assertEqual(esiti(testo), [])

    def test_elenco_dopo_la_parentesi_e_in_minuscolo_con_due_punti(self):
        self.assertIn(("Attacco Poderoso", "tabella"), esiti("· **Talenti** (7) Attacco Poderoso, Incalzare\n"))
        self.assertIn(("Discipline", "fonte"), esiti("Regional feats: Discipline (PGF p38)\n"))

    def test_statblock_inglese_con_la_barra_a_fine_riga(self):
        testo = ("Feats Blind-Fight, Exotic Weapon Proficiency (bastard \\\n"
                 "sword)B, Rapid Reload, Weapon Focus (bastard sword)B, \\\n"
                 "Weapon Specialization (bastard sword)B\n")
        self.assertEqual([t for t, _ in esiti(testo)],
                         ["Blind-Fight", "Exotic Weapon Proficiency", "Rapid Reload", "Weapon Focus",
                          "Weapon Specialization"])

    def test_skills_and_feats_legge_solo_i_talenti(self):
        testo = "Skills and Feats: Hide +15, Listen +16; Combat Casting, Improved Initiative\n"
        self.assertEqual([t for t, _ in esiti(testo)], ["Combat Casting", "Improved Initiative"])

    def test_fine_campo_su_parentesi_aperta_doppio_spazio_e_trattini(self):
        self.assertEqual(L.termini_della_riga("Multiattacco, Capacità Focalizzata (aura): la scheda non li"),
                         ["Multiattacco", "Capacità Focalizzata"])
        self.assertEqual(L.termini_della_riga("Shot on the Run, Expeditious Dodge  In terms of equipment"),
                         ["Shot on the Run", "Expeditious Dodge"])
        self.assertEqual(L.termini_della_riga("Power Attack, Spell Focus --Bonus from Domination Domain"),
                         ["Power Attack", "Spell Focus"])
        self.assertEqual(L.termini_della_riga("Brew Potion, Craft Magic Arms/Armor"),
                         ["Brew Potion", "Craft Magic Arms and Armor"])

    def test_nome_italiano_con_l_inglese_tra_parentesi(self):
        self.assertIn(("Inscribe Rune", "fonte"), esiti("- Talenti: Incidere Rune (Inscribe Rune), Allerta\n"))
        self.assertIn(("Snake Style", "marcato"), esiti("**Talenti:** Stile del Serpente (Snake Style, PF1e)\n"))

    def test_la_riga_era_e_storia(self):
        self.assertEqual(esiti("era: talenti Attacco in Volata, Fluttuare\n"), [])

    def test_talento_pf1e_di_un_manuale(self):
        self.assertIn(L.norma("Combat Vigor"), L.talenti_pf1_dei_manuali())

    def test_talento_di_un_manuale_3_5(self):
        self.assertIn(L.norma("Goad"), L.talenti_dei_manuali())


class TestEsiti(unittest.TestCase):
    def test_nome_ufficiale_variante_e_sconosciuto(self):
        e = esiti("**Talenti** Attacco Poderoso, Fendere, Spezzaferro Nanico\n")
        self.assertEqual(e, [("Attacco Poderoso", "tabella"), ("Fendere", "variante"),
                             ("Spezzaferro Nanico", "sconosciuto")])

    def test_nome_inglese_delle_fonti(self):
        self.assertEqual(esiti("**Feats** Power Attack, Cleave\n"),
                         [("Power Attack", "fonte"), ("Cleave", "fonte")])

    def test_marcato_fuori_srd_passa(self):
        e = esiti("**Talenti** Spezzaferro Nanico [Private source — Races of Stone, p. 1]\n")
        self.assertEqual(e[0][1], "marcato")


class TestModuliPF1e(unittest.TestCase):
    """Nei moduli PF1e vale la tabella diretta: un nome 3.5 è un errore."""

    def test_il_percorso_dichiara_il_modulo_pf1e(self):
        self.assertTrue(L.e_pf1("10-stand-alone/Il Giardino PF1e/appendice.md", ""))
        self.assertFalse(L.e_pf1("Bestiario/mostri/ogre.md", "**Talenti** Incalzare"))

    def test_l_intestazione_dichiara_il_modulo_pf1e(self):
        self.assertTrue(L.e_pf1("x.md", "# Modulo\n\n**Sistema**: Pathfinder 1e\n"))

    def test_nome_3_5_in_un_modulo_pf1e(self):
        e = esiti("**Talenti**: Finezza nell'Arma · Arma Accurata\n", "PREGEN-PF1E.md")
        self.assertEqual(e, [("Finezza nell'Arma", "nome 3.5"), ("Arma Accurata", "tabella")])

    def test_lo_stesso_nome_in_un_modulo_3_5_e_una_variante(self):
        self.assertEqual(esiti("**Talenti**: Finezza nell'Arma\n", "STATBLOCCHI.md"),
                         [("Finezza nell'Arma", "variante")])


class TestTabelle(unittest.TestCase):
    def test_la_tabella_italiana_del_repo_si_legge(self):
        voci = L.carica_tabella()
        self.assertGreaterEqual(len(voci), 80)
        self.assertTrue(all(v.get("it") for v in voci))

    def test_la_variante_della_tabella_3_5_si_corregge(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "t.tsv"
            p.write_text("italiano\tsrd35\ttipo\tabbinamento\n"
                         "Freccia acida di Melf\tAcid Arrow\tincantesimo\tprefisso\n"
                         "Freccia acida\tAcid Arrow\tincantesimo\tvariante (forma SRD)\n", encoding="utf-8")
            voci = L.tabella_35(p)
            self.assertEqual([(v["it"], v.get("varianti")) for v in voci], [("Freccia acida di Melf", "Freccia acida")])

    def test_tabella_pf1_per_tipo(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "t.tsv"
            p.write_text("# commento\nitaliano\tpf1\ttipo\nArma Accurata\tWeapon Finesse\ttalento\n"
                         "Dardo Incantato\tMagic Missile\tincantesimo\n", encoding="utf-8")
            self.assertEqual(list(L.tabella_pf1(p)), [L.norma("Arma Accurata")])
            self.assertEqual(L.tabella_pf1(p, "incantesimo")[L.norma("Dardo Incantato")]["pf1"],
                             "Magic Missile")

    def test_la_tabella_pf1_del_repo_ha_i_quattro_tipi(self):
        for tipo, minimo in (("talento", 1000), ("incantesimo", 1400), ("abilità", 26), ("condizione", 30)):
            with self.subTest(tipo=tipo):
                self.assertGreaterEqual(len(L.tabella_pf1(tipo=tipo)), minimo)


# Campi dello statblocco: tabelle finte per tipo.
T35 = {"incantesimo": {L.norma("Luminescenza"): {"it": "Luminescenza", "srd35": "Faerie Fire"},
                       L.norma("Cura ferite gravi"): {"it": "Cura ferite gravi", "srd35": "Cure Serious Wounds"}},
       "abilità": {L.norma("Nascondersi"): {"it": "Nascondersi", "srd35": "Hide"}},
       "oggetto magico": {L.norma("Mantello della resistenza"): {"it": "Mantello della resistenza",
                                                                "srd35": "Cloak of Resistance"},
                          L.norma("Protezione"): {"it": "Protezione", "srd35": "Protection"},
                          L.norma("Negazione"): {"it": "Negazione", "srd35": "Negation"}},
       "equipaggiamento": {L.norma("Spada lunga"): {"it": "Spada lunga", "srd35": "Longsword"}},
       "proprietà magica": {L.norma("Sacra"): {"it": "Sacra", "srd35": "Holy"},
                            L.norma("Affilata"): {"it": "Affilata", "srd35": "Keen"}}}
TPF = {"incantesimo": {L.norma("Fuoco Fatato"): {"it": "Fuoco Fatato", "pf1": "Faerie Fire"}},
       "abilità": {}, "oggetto magico": {}, "equipaggiamento": {}}
IDX_C = {L.norma("teleport greater"): [{"fonte": "srd35", "tipo": "incantesimo", "nome": "Teleport, Greater"}]}


def campi(testo: str, file: str = "modulo.md") -> list[tuple[str, str, str]]:
    return [(r["tipo"], r["termine"], r["esito"]) for r in L.controlla_campi(testo, IDX_C, T35, TPF, file)]


class TestCampi(unittest.TestCase):
    """ADR-0110, lotto 2: incantesimi, abilità e oggetti delle schede."""

    def test_incantesimi_in_corsivo_anche_in_elenco(self):
        self.assertEqual(campi("**Capacità magiche** (CL 9): *a volontà* — *luminescenza*, *fuoco fatuo, greater teleport*\n"),
                         [("incantesimo", "luminescenza", "tabella"), ("incantesimo", "fuoco fatuo", "sconosciuto"),
                          ("incantesimo", "greater teleport", "fonte")])

    def test_abilita_prima_del_bonus(self):
        self.assertEqual(campi("**Abilità**: Nascondersi +12, Furtività +8\n"),
                         [("abilità", "Nascondersi", "tabella"), ("abilità", "Furtività", "sconosciuto")])

    def test_oggetti_pozioni_e_armi(self):
        e = campi("**Equipaggiamento**: *mantello della resistenza +2*, *spada lunga*, 2 *pozioni di cura ferite gravi*\n")
        self.assertEqual(e, [("oggetto magico", "mantello della resistenza", "tabella"),
                             ("oggetto magico", "spada lunga", "tabella"),
                             ("oggetto magico", "cura ferite gravi", "tabella")])

    def test_anelli_e_verghe_col_nome_del_gdm(self):
        e = campi("**Equipaggiamento**: *anello di protezione +2*, *verga della negazione*, *anello dell'invisibilità totale*\n")
        self.assertEqual(e, [("oggetto magico", "anello di protezione", "tabella"),
                             ("oggetto magico", "verga della negazione", "tabella"),
                             ("oggetto magico", "anello dell'invisibilità totale", "sconosciuto")])

    def test_arma_con_proprieta_magiche(self):
        e = campi("**Equipaggiamento**: *spada lunga sacra affilata +2*, *spada lunga runica*\n")
        self.assertEqual(e, [("oggetto magico", "spada lunga sacra affilata", "tabella"),
                             ("oggetto magico", "spada lunga runica", "sconosciuto")])

    def test_oggetto_della_campagna(self):
        e = campi("**Equipaggiamento**: *Corona dei Re Hammerfist*, *Martello da Guerra degli Antenati +3*\n")
        self.assertEqual(e, [("oggetto magico", "Corona dei Re Hammerfist", "campagna"),
                             ("oggetto magico", "Martello da Guerra degli Antenati", "campagna")])

    def test_nel_modulo_pf1e_il_nome_3_5_e_un_errore(self):
        self.assertEqual(campi("**Incantesimi**: *luminescenza*, *fuoco fatato*\n", "PF1e/modulo.md"),
                         [("incantesimo", "luminescenza", "nome 3.5"), ("incantesimo", "fuoco fatato", "tabella")])

    def test_le_tabelle_del_repo_per_tipo(self):
        t35, tpf = L.tabelle_per_tipo()
        for tipo, minimo in (("incantesimo", 600), ("abilità", 35), ("oggetto magico", 600), ("equipaggiamento", 180)):
            with self.subTest(tipo=tipo):
                self.assertGreaterEqual(len(t35.get(tipo, {})), minimo)
        for tipo, minimo in (("incantesimo", 2000), ("oggetto magico", 2000), ("equipaggiamento", 250)):
            with self.subTest(tipo=tipo, sistema="pf1"):
                self.assertGreaterEqual(len(tpf.get(tipo, {})), minimo)


if __name__ == "__main__":
    unittest.main()
