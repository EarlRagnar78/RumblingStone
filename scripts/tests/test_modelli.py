"""I modelli semplici di PF1e (lotto J): un conto esatto per modello, il
ritorno al blocco di partenza, il GS che resta quello chiesto."""
import dataclasses
import io
import random
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import genera_creatura as G  # noqa: E402
from dmcore import modelli as M  # noqa: E402
from dmcore.statblock import Statblocco  # noqa: E402


def orso() -> Statblocco:
    """Un blocco scritto a mano: i conti attesi si rifanno con carta e penna."""
    return Statblocco(
        nome="orso di prova", gs="4", tipo="Large animal, 6d8+24",
        ca="15", ca_dettaglio="(-1 taglia, +1 Des, +5 naturale)",
        pf="51", pf_dado="6d8", ts="Temp +9, Rifl +6, Vol +3",
        velocita="12 m", iniziativa="+1", sensi="fiuto",
        attributi="For 27 Des 13 Cos 19 Int 2 Sag 12 Car 6",
        attacchi=["Mischia artiglio +11 (1d8+8)", "Distanza roccia +4 (2d6+8)"],
        voci=["Debolezza: lento"])


class TestDati(unittest.TestCase):
    def test_sette_modelli_ognuno_con_la_fonte(self):
        self.assertEqual(M.nomi(), ["advanced", "celestial", "entropic", "fiendish",
                                    "giant", "resolute", "young"])
        for nome in M.nomi():
            m = M.modello(nome)
            self.assertIn("PRD Bestiary, Simple Templates", m["fonte"], nome)
            self.assertIn("nome", m)

    def test_si_trova_anche_col_nome_italiano(self):
        self.assertEqual(M.modello("Gigante")["chiave"], "giant")
        with self.assertRaises(KeyError):
            M.modello("mezzo-drago")

    def test_gli_archetipi_di_classe_non_sono_modelli(self):
        for nome in ("two-handed fighter", "urban ranger"):
            with self.assertRaises(KeyError):
                M.modello(nome)


class TestConto(unittest.TestCase):
    def test_advanced(self):
        sb = orso()
        t = M.applica(sb, "advanced")
        # l'Intelligenza 2 dell'animale non sale
        self.assertEqual(sb.attributi, "For 31 Des 17 Cos 23 Int 2 Sag 16 Car 10")
        self.assertEqual((sb.pf, sb.tipo), ("63", "Large animal, 6d8+36"))
        self.assertEqual((sb.ca, sb.ca_dettaglio), ("19", "(-1 taglia, +3 Des, +7 naturale)"))
        self.assertEqual(sb.ts, "Temp +11, Rifl +8, Vol +5")
        self.assertEqual(sb.iniziativa, "+3")
        self.assertEqual(sb.attacchi, ["Mischia artiglio +13 (1d8+10)",
                                       "Distanza roccia +6 (2d6+10)"])
        self.assertEqual(t.gs_reale, "5")

    def test_giant(self):
        sb = orso()
        t = M.applica(sb, "giant")
        self.assertEqual(sb.attributi, "For 31 Des 11 Cos 23 Int 2 Sag 12 Car 6")
        self.assertEqual((sb.pf, sb.tipo), ("63", "Huge animal, 6d8+36"))
        # +3 naturale, −1 Des, da Grande (−1) a Enorme (−2)
        self.assertEqual((sb.ca, sb.ca_dettaglio), ("16", "(-2 taglia, +0 Des, +8 naturale)"))
        self.assertEqual(sb.ts, "Temp +11, Rifl +5, Vol +3")
        self.assertEqual(sb.iniziativa, "+0")
        self.assertEqual(sb.attacchi, ["Mischia artiglio +12 (2d6+10)",
                                       "Distanza roccia +2 (3d6+10)"])
        self.assertEqual(t.gs_reale, "5")

    def test_young(self):
        sb = orso()
        t = M.applica(sb, "young")
        self.assertEqual(sb.attributi, "For 23 Des 17 Cos 15 Int 2 Sag 12 Car 6")
        self.assertEqual((sb.pf, sb.tipo), ("39", "Medium animal, 6d8+12"))
        self.assertEqual((sb.ca, sb.ca_dettaglio), ("16", "(+3 Des, +3 naturale)"))
        self.assertEqual(sb.ts, "Temp +7, Rifl +8, Vol +3")
        self.assertEqual(sb.iniziativa, "+3")
        self.assertEqual(sb.attacchi, ["Mischia artiglio +10 (1d6+6)",
                                       "Distanza roccia +7 (1d10+6)"])
        self.assertEqual(t.gs_reale, "3")

    def test_young_non_porta_l_armatura_naturale_sotto_zero(self):
        sb = orso()
        sb.ca, sb.ca_dettaglio = "11", "(-1 taglia, +1 Des, +1 naturale)"
        t = M.applica(sb, "young")
        self.assertEqual(t.naturale, -1)
        self.assertEqual((sb.ca, sb.ca_dettaglio), ("13", "(+3 Des, +0 naturale)"))

    def _planare(self, nome, resistenze, rd, punire):
        sb = orso()
        prima = dataclasses.asdict(orso())
        t = M.applica(sb, nome)
        for campo in ("attributi", "pf", "ca", "ts", "iniziativa", "attacchi", "tipo"):
            self.assertEqual(getattr(sb, campo), prima[campo], campo)
        self.assertEqual(sb.sensi, "fiuto, scurovisione 18 m")
        # 6 dadi vita: fascia 5-10, resistenze 10 e RD 5; GS 4 + 1 = 5, RI 10
        self.assertIn("Resistenze: " + ", ".join(f"{r} 10" for r in resistenze), sb.voci)
        self.assertIn(f"RD 5/{rd}", sb.voci)
        self.assertIn("RI 10", sb.voci)
        self.assertTrue(any(v.startswith(f"Punire {punire} 1/giorno") and "+6 ai danni" in v
                            for v in sb.voci), sb.voci)
        self.assertEqual(t.gs_reale, "5")

    def test_celestial(self):
        self._planare("celestial", ("acido", "freddo", "elettricità"), "male", "il male")

    def test_fiendish(self):
        self._planare("fiendish", ("freddo", "fuoco"), "bene", "il bene")

    def test_entropic(self):
        self._planare("entropic", ("acido", "fuoco"), "legale", "la legge")

    def test_resolute(self):
        self._planare("resolute", ("acido", "freddo", "fuoco"), "caotico", "il caos")

    def test_le_tre_fasce_delle_difese(self):
        for dv, resistenza, rd, gs_reale in ((4, 5, None, "4"), (5, 10, 5, "5"), (11, 15, 10, "5")):
            sb = orso()
            sb.pf_dado, sb.tipo = f"{dv}d8", f"Large animal, {dv}d8+{4 * dv}"
            t = M.applica(sb, "fiendish")
            self.assertIn(f"Resistenze: freddo {resistenza}, fuoco {resistenza}", sb.voci)
            self.assertEqual([v for v in sb.voci if v.startswith("RD")],
                             [f"RD {rd}/bene"] if rd else [])
            # sotto i 5 dadi vita il modello non vale un GS in più
            self.assertEqual(t.gs_reale, gs_reale, dv)
            self.assertIn(f"RI {int(gs_reale) + 5}", sb.voci)

    def test_senza_costituzione_niente_pf(self):
        sb = orso()
        sb.attributi = "For 27 Des 13 Cos — Int — Sag 12 Car 6"
        M.applica(sb, "advanced")
        self.assertEqual(sb.pf, "51")
        self.assertEqual(sb.attributi, "For 31 Des 17 Cos — Int — Sag 16 Car 10")
        self.assertEqual(sb.ts, "Temp +9, Rifl +8, Vol +5")

    def test_un_dado_fuori_tabella_resta_e_si_dice(self):
        sb = orso()
        sb.attacchi = ["Mischia morso +11 (4d6+8)"]
        t = M.applica(sb, "giant")
        self.assertEqual(sb.attacchi, ["Mischia morso +12 (4d6+10)"])
        self.assertEqual(t.dadi_fermi, ["4d6"])
        self.assertTrue(any("fuori tabella" in r for r in t.righe))


class TestGsEVoce(unittest.TestCase):
    def test_il_gs_scritto_resta_quello_chiesto(self):
        for nome in M.nomi():
            sb = orso()
            t = M.applica(sb, nome)
            self.assertEqual(sb.gs, "4", nome)
            self.assertIn(f"GS {t.gs_reale}", sb.voci[-1], nome)
            self.assertTrue(sb.voci[-1].startswith("⚠"), nome)
            self.assertTrue(any(r.startswith("fonte: PRD Bestiary") for r in t.righe), nome)

    def test_sotto_gs_1_il_giovane_scende_per_frazioni(self):
        self.assertEqual(M.gs_reale("2", M.modello("young"), 2), "1")
        self.assertEqual(M.gs_reale("1", M.modello("young"), 1), "1/2")
        self.assertEqual(M.gs_reale("1/2", M.modello("young"), 1), "1/3")


class TestDisfare(unittest.TestCase):
    def test_applicare_e_disfare_torna_al_blocco_di_partenza(self):
        for nome in M.nomi():
            sb = orso()
            prima = dataclasses.asdict(sb)
            t = M.applica(sb, nome)
            self.assertNotEqual(dataclasses.asdict(sb), prima, nome)
            M.disfa(sb, t)
            self.assertEqual(dataclasses.asdict(sb), prima, nome)

    def test_anche_sui_blocchi_del_generatore(self):
        for nome in M.nomi():
            for ruolo, tipo in (("bruto", "humanoid"), ("tiratore", "magical beast"),
                                ("controllore", "undead")):
                sb, _ = G.genera(5, tipo=tipo, ruolo=ruolo, rng=random.Random(5), talenti=None)
                prima = dataclasses.asdict(sb)
                M.disfa(sb, M.applica(sb, nome))
                self.assertEqual(dataclasses.asdict(sb), prima, (nome, ruolo, tipo))


class TestVietati(unittest.TestCase):
    def test_gigante_su_colossale(self):
        sb = orso()
        sb.tipo = "Colossal animal, 6d8+24"
        with self.assertRaises(M.ModelloVietato):
            M.applica(sb, "giant")

    def test_giovane_su_piccolissima_e_sui_draghi(self):
        sb = orso()
        sb.tipo = "Fine animal, 6d8+24"
        with self.assertRaises(M.ModelloVietato):
            M.applica(sb, "young")
        sb.tipo = "Large dragon, 6d12+24"
        with self.assertRaises(M.ModelloVietato):
            M.applica(sb, "young")

    def test_un_modello_vietato_non_tocca_il_blocco(self):
        sb = orso()
        sb.tipo = "Colossal animal, 6d8+24"
        prima = dataclasses.asdict(sb)
        with self.assertRaises(M.ModelloVietato):
            M.applica(sb, "giant")
        self.assertEqual(dataclasses.asdict(sb), prima)


class TestGeneratore(unittest.TestCase):
    def _esce(self, *argomenti) -> str:
        fuori = io.StringIO()
        with redirect_stdout(fuori):
            G.main(["--gs", "5", "--ruolo", "bruto", "--seed", "7", *argomenti])
        return fuori.getvalue()

    def test_piu_cattivi_e_template_advanced_sono_la_stessa_cosa(self):
        self.assertEqual(self._esce("--piu-cattivi"), self._esce("--template", "advanced"))

    def test_la_fonte_dice_modello_e_gs_reale(self):
        testo = self._esce("--template", "giant")
        self.assertIn("gs: 5\n", testo)
        self.assertIn("template=giant-PF1e-gs-reale=6", testo)
        self.assertIn("⚠ modello Gigante (PF1e) applicato SENZA cambiare il GS: "
                      "vale in realtà GS 6", testo)

    def test_piu_cattivi_non_si_somma_a_un_altro_modello(self):
        with self.assertRaises(SystemExit):
            self._esce("--piu-cattivi", "--template", "giant")
        with self.assertRaises(ValueError):
            G.genera(5, piu_cattivi=True, modello="young")

    def test_il_giovane_non_si_applica_a_un_drago(self):
        with self.assertRaises(SystemExit):
            self._esce("--tipo", "dragon", "--template", "young")


if __name__ == "__main__":
    unittest.main()
