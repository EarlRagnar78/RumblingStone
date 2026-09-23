"""Gli `attributi` generati: vincolati prima che scelti, e a seme fisso.

⚠️ **Le prove che contano sono quelle che bocciano.** Un generatore che
accetta ogni Costituzione ricavata da `pf` scrive un 34 su un duergar da GS 4
e lo fa sembrare una misura: e' successo alla prima stesura, ed e' la prova
`test_la_guardia_respinge_i_dv_parziali`. Il caso peggiore e' venuto dopo, e
l'ha trovato la taratura: in 20 statblocchi `pf-dado` era il danno dell'arma
(`TestPfDadoNonEUnArma`).
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import genera_attributi as G  # noqa: E402


def blocco(tipo="Medium humanoid", ca="ca: 15", det="ca-dettaglio: +2 Dex, +3 armatura",
           pf="pf: 20", dado="pf-dado: 3d8+6", gs="gs: 3"):
    return f"```statblocco\n{gs}\ntipo: {tipo}\n{ca}\n{det}\n{pf}\n{dado}\n```\n"


class TestLaRegolaDiBase(unittest.TestCase):
    def test_modificatore_3_5(self):
        self.assertEqual([G.mod(x) for x in (1, 8, 9, 10, 11, 12, 19)],
                         [-5, -1, -1, 0, 0, 1, 4])

    def test_gli_array_sono_quelli_del_manuale(self):
        self.assertEqual(G.ARRAY_ELITE, (15, 14, 13, 12, 10, 8))
        self.assertEqual(G.ARRAY_STANDARD, (13, 12, 11, 10, 9, 8))

    def test_le_tabelle_vengono_da_dmcore(self):
        # la prima stesura le ricopiava, e sbagliava ranger e «minuta»
        self.assertEqual(G.DADO_DI_CLASSE["ranger"], 8)
        self.assertEqual(G.TAGLIA["minuta"], 4)
        self.assertEqual(G.TAGLIA["minuscola"], 2)


class TestIlVincoloBatteLArray(unittest.TestCase):
    def test_la_destrezza_scritta_si_legge(self):
        self.assertEqual(G.des_vincolata(blocco(), 3)[0], 14)

    def test_la_destrezza_si_ricava_dal_contatto(self):
        t = blocco(det="ca-dettaglio: touch 13, flat-footed 12", tipo="Small humanoid")
        # 13 = 10 + Des + 1 (piccola)  →  Des +2  →  14
        self.assertEqual(G.des_vincolata(t, 3)[0], 14)

    def test_la_costituzione_si_ricava_dal_bonus_scritto(self):
        self.assertEqual(G.cos_da_pf(blocco(dado="pf-dado: 4d8+8"), 3)[0], 14)

    def test_la_costituzione_si_ricava_dalla_media(self):
        # 14d8 senza bonus, 172 pf: (172 − 63) / 14 ≈ +8  →  26
        t = blocco(pf="pf: 172", dado="pf-dado: 14d8")
        self.assertEqual(G.cos_da_pf(t, 11)[0], 26)

    def test_la_guardia_respinge_i_dv_parziali(self):
        # 5d8 senza bonus e 80 pf a GS 4: +7, cioe' Cos 24 — un GS 4 non lo regge
        t = blocco(pf="pf: 80", dado="pf-dado: 5d8")
        self.assertIsNone(G.cos_da_pf(t, 4))

    def test_la_guardia_dipende_dal_gs(self):
        self.assertTrue(G.plausibile(8, 11))
        self.assertFalse(G.plausibile(8, 4))
        self.assertFalse(G.plausibile(-3, 20))


class TestPfDadoNonEUnArma(unittest.TestCase):
    def test_dv_dichiarati_diversi(self):
        # il caso vero: Morlin, `1d8+7` accanto a «hp 93 (12 HD)»
        t = blocco(pf="pf: 93", dado="pf-dado: 1d8+7") + "\n**hp 93** (12 HD)\n"
        self.assertIn("12 DV", G.pf_dado_sospetto(t, 12))
        self.assertIsNone(G.cos_da_pf(t, 12))

    def test_dado_della_classe_sbagliato(self):
        t = blocco(tipo="Medium humanoid (dwarf, duergar), Wizard 3", dado="pf-dado: 3d8")
        self.assertIn("d4", G.pf_dado_sospetto(t, 4))

    def test_dado_della_classe_giusto(self):
        t = blocco(tipo="Medium humanoid (dwarf, duergar), Rogue 1", dado="pf-dado: 1d6+1")
        self.assertIsNone(G.pf_dado_sospetto(t, 1))

    def test_i_dv_razziali_non_si_giudicano_col_dado_di_classe(self):
        # un gigante con livelli da barbaro tira anche d8 razziali: non e' umanoide
        t = blocco(tipo="Large giant, Barbarian 2", dado="pf-dado: 4d8+2d12")
        self.assertIsNone(G.pf_dado_sospetto(t, 6))


class TestLaFonteVince(unittest.TestCase):
    """Sulle fonti vere di `pregen-pcgen/`, che sono archivio in sola lettura."""

    def _file(self, nome):
        return next((ROOT / "Bestiario").rglob(nome))

    def test_fonte_dedicata(self):
        f = self._file("abbathor-cleric11-cr11.md")
        v, come = G.dalla_fonte(f.name, f.read_text(encoding="utf-8"))
        self.assertEqual((v["For"], v["Sag"]), (14, 18))
        self.assertIn("abbathor_clerics11", come)

    def test_fonte_con_piu_creature_si_sceglie_per_nome(self):
        # la regola tolta dava al worker la sestina del sovrano: For 26
        f = self._file("myconid-worker-cr2.md")
        v, _ = G.dalla_fonte(f.name, f.read_text(encoding="utf-8"))
        self.assertEqual(v["For"], 12)
        f = self._file("myconid-sovereign-cr7.md")
        v, _ = G.dalla_fonte(f.name, f.read_text(encoding="utf-8"))
        self.assertEqual(v["For"], 26)

    def test_un_modificatore_al_posto_del_punteggio_si_scarta(self):
        self.assertIsNone(G.SESTINA.search("Str 11, Dex 15, Con 14, Int 18, Wis 10, Cha -4"))
        self.assertIsNotNone(G.SESTINA.search("Str 11, Dex 15, Con —, Int —, Wis 10, Cha 1"))

    def test_senza_regola_per_scegliere_non_si_trascrive(self):
        f = self._file("duergar-mago3-cr4.md")
        self.assertIsNone(G.dalla_fonte(f.name, f.read_text(encoding="utf-8")))


class TestLaSchedaSiLeggePrima(unittest.TestCase):
    """Lo strato 0a: 27 dei 55 «scelti» avevano i numeri scritti nella prosa."""

    def test_la_sestina_inglese(self):
        t = blocco() + "\n**Abilities**: Str 14, Dex 12, Con 14, Int 10, Wis 10, Cha 8\n"
        v, come = G.dalla_scheda(t)
        self.assertEqual((v["For"], v["Car"]), (14, 8))
        self.assertIn("scheda stessa", come)

    def test_la_sestina_italiana(self):
        # il bruto deforme scrive in italiano, e la prima stesura non lo capiva
        t = blocco() + "\n**Car** For 31, Des 13, Cos 23, Int 10, Sag 12, Car 11.\n"
        self.assertEqual(G.dalla_scheda(t)[0]["For"], 31)

    def test_due_sestine_sono_una_scelta(self):
        t = blocco() + "\nStr 14, Dex 12, Con 14, Int 10, Wis 10, Cha 8\nStr 18, Dex 12, Con 14, Int 10, Wis 10, Cha 8\n"
        self.assertIsNone(G.dalla_scheda(t))

    def test_la_scheda_batte_la_fonte_e_i_vincoli(self):
        t = blocco(det="ca-dettaglio: +4 Dex") + "\nStr 14, Dex 12, Con 14, Int 10, Wis 10, Cha 8\n"
        v, note = G.genera("x-cr3.md", "brute", 3, t)
        self.assertEqual(v["Des"], 12)                 # la scheda, non il +4 della CA
        self.assertTrue(any(n.startswith("⚠ Des") for n in note))


class TestLaForzaDallaLotta(unittest.TestCase):
    def test_bab_lotta_e_taglia(self):
        t = blocco(tipo="Large giant") + "\nBAB +3; Lotta +14.\n"
        self.assertEqual(G.for_da_lotta(t, 4)[0], 24)   # 14 − 3 − 4 = +7

    def test_lotta_migliorata_si_toglie(self):
        t = blocco() + "\nBAB +5; Lotta +12. Talenti: Lottare Migliorato\n"
        self.assertEqual(G.for_da_lotta(t, 7)[0], 16)   # 12 − 5 − 4 = +3

    def test_le_marche_non_sono_numeri(self):
        # la marca che scrive «BAB +1 → +0» veniva letta come il BAB
        t = blocco() + "\nBAB +0; Lotta +1.\n\n> [INFERRED] BAB +1 → **+0**\n"
        self.assertEqual(G.for_da_lotta(t, 1)[0], 12)


class TestLaTagliaSiTrova(unittest.TestCase):
    def test_dal_size_type(self):
        self.assertEqual(G.taglia_di("**Size/Type**: Large giant | **HD**: 12d8"), -1)

    def test_dal_dettaglio_della_ca_e_non_dalla_prosa(self):
        # il loxo sciamano: «(-1 size…)» nella CA, e «Medium animal» e' il compagno
        t = "ca-dettaglio: (-1 size, +7 natural)\nAnimal companion: dire wolf (Medium animal)."
        self.assertEqual(G.taglia_di(t), -1)


class TestLaDestrezzaDallIniziativa(unittest.TestCase):
    def test_con_iniziativa_migliorata(self):
        t = blocco(det="") + "\niniziativa: +6\n\nTalenti: Iniziativa/Vergare Migliorato\n"
        self.assertEqual(G.des_da_iniziativa(t, 7)[0], 14)

    def test_senza_elenco_di_talenti_non_si_ricava(self):
        self.assertIsNone(G.des_da_iniziativa(blocco() + "\niniziativa: +5\n", 9))


class TestLeRegoleDiTipo(unittest.TestCase):
    def test_il_non_morto_non_ha_costituzione(self):
        t = blocco(tipo="Medium undead HD 8d12", dado="pf-dado: 8d12")
        v, _ = G.genera("x-cr8.md", "caster", 8, t)
        self.assertEqual(v["Cos"], "—")

    def test_lo_scheletro_ha_le_mentali_della_regola(self):
        t = blocco(tipo="Large undead (skeleton)")
        v, _ = G.genera("skeletal-x-cr6.md", "brute", 6, t)
        self.assertEqual((v["Int"], v["Sag"], v["Car"]), ("—", 10, 1))

    def test_la_classe_si_cerca_solo_nel_tipo(self):
        # la prosa che nomina «Barbaro 2» non fa di un gigante un PNG
        t = blocco(tipo="Huge giant") + "\nVariante: Barbaro 2\n"
        _, note = G.genera("gigante-cr11.md", "brute", 11, t)
        self.assertIn("creatura", note[0])


class TestIlCasoEASemeFisso(unittest.TestCase):
    def test_stesso_nome_stesso_risultato(self):
        a = G.genera("goblin-cr1.md", "fodder", 1, blocco())
        b = G.genera("goblin-cr1.md", "fodder", 1, blocco())
        self.assertEqual(a, b)

    def test_nomi_diversi_non_sono_tutti_uguali(self):
        righe = {G.riga_attributi(G.genera(f"g{i}-cr1.md", "fodder", 1, "")[0])
                 for i in range(20)}
        self.assertGreater(len(righe), 3)

    def test_la_taglia_srd_per_le_creature(self):
        v, _ = G.genera("x-cr1.md", "brute", 1, blocco(tipo="Large giant", det="", dado=""))
        self.assertEqual(v["For"], 15 + 8)          # elite, GS 1, Large: For +8

    def test_la_razza_srd_per_i_png(self):
        v, _ = G.genera("orco-x-cr1.md", "fodder", 1,
                        blocco(tipo="Medium humanoid (orc), Warrior 1", det="", dado=""))
        self.assertEqual(v["For"], 13 + 4)          # standard, For prima, orco +4

    def test_la_principale_non_varia(self):
        for i in range(20):
            v, _ = G.genera(f"g{i}-cr1.md", "brute", 1, "")
            self.assertEqual(v["For"], 15)          # elite, creatura, GS 1


class TestIlRepoVero(unittest.TestCase):
    def test_il_cancello_e_verde(self):
        self.assertEqual(G.controlla(), [])

    def test_ogni_blocco_generato_porta_la_sua_marca(self):
        for r in G.proponi(rigenera=True):
            if r["scritta"]:
                self.assertIn(r["marca"], r["file"].read_text(encoding="utf-8"),
                              r["file"].name)

    def test_la_taratura_non_peggiora(self):
        # 2026-09-23: 1,63 in campione, 1,84 fuori. Una regola nuova che le
        # alza va spiegata, non taciuta.
        self.assertLessEqual(G.taratura("fonti")["mae"], 1.70)
        self.assertLessEqual(G.taratura("schede")["mae"], 1.90)


if __name__ == "__main__":
    unittest.main()
