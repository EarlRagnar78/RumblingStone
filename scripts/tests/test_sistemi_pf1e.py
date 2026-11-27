"""Le cinque capacità PF1e prima «non supportate» (ADR-0111): PE, incontri,
tesoro, classi e razze, costruzione delle creature.

I difetti che questi test esistono per impedire:

- un numero PF1e scritto a mano che non è quello del PRD (i dati li scrive
  estrai_prd_pf1e.py; qui si controllano i punti che il PRD stesso dà come
  esempio, e il --check quando il PRD è in cache);
- un incontro PF1e combinato con la formula 3.5 (tre GS 10 fanno GS 13 in
  PF1e, 13,17 in 3.5);
- un blocco portato in PF1e che perde i pf del suo GS cambiando dado vita;
- uno strumento che con --sistema pf1e cambia anche l'uscita 3.5 (quella la
  tiene il banco d'invarianza, qui si prova solo che il predefinito resta 3.5).

Solo `unittest`.
"""
from __future__ import annotations

import os
import random
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from dmcore import sistemi as S  # noqa: E402
from dmcore import creature_pf1e as CP  # noqa: E402
import coerenza_campagna as C  # noqa: E402
import genera_creatura as G  # noqa: E402
import suggest_encounter as E  # noqa: E402
import suggest_loot as L  # noqa: E402
import update_xp as X  # noqa: E402

ESTRATTORE = REPO / "plans/esperimenti/sistemi-plugin-2026-11-07/estrai_prd_pf1e.py"
CACHE = Path(os.environ.get("RUMBLINGSTONE_SRD_CACHE",
                            Path.home() / ".cache/rumblingstone/srd")) / "PSRD-Data-76ea47846041"


class Dati(unittest.TestCase):
    def test_nessuna_capacita_pf1e_resta_non_supportata(self):
        cat = S.carica()[1]
        modi = {n: S.capacita("pf1e", n).modo for n in cat}
        self.assertEqual([n for n, m in modi.items() if m not in ("dati", "codice")], [])

    def test_dati_rifiuta_una_capacita_in_codice(self):
        # Dopo F1 di ADR-0112 nessuna capacità vera resta «codice»: la prova si
        # fa su una copia dei plugin dove fonti.regole torna codice.
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            r = Path(tmp)
            shutil.copytree(REPO / "sistemi", r / "sistemi")
            shutil.copy2(REPO / "sistemi.toml", r / "sistemi.toml")
            desc = r / "sistemi" / "dnd35" / "sistema.toml"
            righe = [('"fonti.regole" = { codice = ["scripts/riscontro_srd.py:FONTI"], lotto = "F1" }'
                      if riga.startswith('"fonti.regole"') else riga)
                     for riga in desc.read_text(encoding="utf-8").splitlines()]
            desc.write_text("\n".join(righe) + "\n", encoding="utf-8")
            with self.assertRaises(S.ErroreSistemi):
                S.dati("dnd35", "fonti.regole", r)

    def test_le_fonti_stanno_nei_dati_del_plugin(self):
        # F1 di ADR-0112: repo, commit e sha256 delle fonti sono dati del plugin.
        for sis, chiave in (("dnd35", "srd35"), ("pf1e", "pf1")):
            d = S.dati(sis, "fonti.regole")
            self.assertEqual(d["chiave"], chiave)
            self.assertRegex(d["commit"], r"^[0-9a-f]{40}$")
            self.assertIn(d["file_licenza"], d["file"])
            self.assertTrue(all(len(v) == 64 for v in d["file"].values()))

    def test_opzioni_di_campagna(self):
        self.assertEqual(S.opzione("pf1e", "traccia_pe"), "media")
        self.assertIsNone(S.opzione("pf1e", "inesistente"))

    @unittest.skipUnless(CACHE.is_dir(), "PRD PF1e non in cache (riscontro_srd.py scarica)")
    def test_i_dati_sono_quelli_del_prd(self):
        r = subprocess.run([sys.executable, str(ESTRATTORE), "--check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class PE(unittest.TestCase):
    def test_tre_tracce_del_prd(self):
        for traccia, liv2, liv20 in (("lenta", 3000, 5350000), ("media", 2000, 3600000),
                                     ("veloce", 1300, 2400000)):
            soglie, _ = X.soglie_di("pf1e", traccia)
            self.assertEqual((soglie[1], soglie[2], soglie[20]), (0, liv2, liv20))

    def test_predefinito_resta_3_5(self):
        soglie, etichetta = X.soglie_di()
        self.assertEqual(soglie, X.THRESHOLDS)
        self.assertEqual(etichetta, "3.5")

    def test_livello_e_mancanti(self):
        soglie, _ = X.soglie_di("pf1e", "media")
        self.assertEqual(X.next_threshold(1025, soglie), (1, 975))
        self.assertEqual(X.next_threshold(1025), (2, 1975))  # 3.5, come prima

    def test_soglie_3_5_dai_dati_invariate(self):
        """L4: i numeri spostati in sistemi/dnd35/dati/pe.toml sono quelli di prima."""
        prima = {1: 0, 2: 1000, 3: 3000, 4: 6000, 5: 10000, 6: 15000, 7: 21000, 8: 28000,
                 9: 36000, 10: 45000, 11: 55000, 12: 66000, 13: 78000, 14: 91000,
                 15: 105000, 16: 120000, 17: 136000, 18: 153000, 19: 171000, 20: 190000}
        self.assertEqual(X.THRESHOLDS, prima)
        self.assertEqual(X.soglie_di("dnd35", "media"), (prima, "3.5"))  # una traccia sola

    def test_sistema_spento_rifiutato(self):
        with self.assertRaises(SystemExit):
            X.soglie_di("pf2e")


class Incontri(unittest.TestCase):
    def test_somma_dei_pe(self):
        f = E.combina_gs_pf1e
        self.assertEqual(f([10, 10]), 12)
        self.assertEqual(f([10, 10, 10]), 13)       # 3.5: 13,17
        self.assertEqual(f([0.5, 0.5]), 1)          # 400 PE = GS 1
        self.assertEqual(f([25, 25]), 27)           # oltre la tabella si raddoppia ogni 2 GS
        self.assertEqual(f([]), 0)

    def test_predefinito_resta_3_5(self):
        self.assertIs(E.COMBINA, E.combine_el)

    def test_metodo_dal_plugin(self):
        """L4: il metodo di combinazione lo dice il plugin, non un `if pf1e`."""
        for crs in ([10, 10], [10, 10, 10], [3, 5, 7, 7], [0.5, 0.5], [16]):
            self.assertEqual(E.combinatore("dnd35")(crs), E.combine_el(crs))
            self.assertEqual(E.combinatore("pf1e")(crs), E.combina_gs_pf1e(crs))


class Tesoro(unittest.TestCase):
    def test_valori_per_incontro(self):
        tab, etichetta = L.tesoro_di("pf1e", "media")
        self.assertEqual((tab[1], tab[13], tab[20]), (260, 11600, 67000))
        self.assertIn("velocità media", etichetta)
        self.assertEqual(L.tesoro_di("pf1e", "veloce")[0][20], 100000)

    def test_predefinito_resta_3_5(self):
        self.assertIsNone(L.TESORO_SISTEMA)


class ClassiERazze(unittest.TestCase):
    DRAPPO = "10-stand-alone/Il-Drappo-di-Tarsilia/x.md"

    def test_classi_pf1e_solo_nei_moduli_pf1e(self):
        paren = "Umano Inquisitore 9/Fattucchiere 3, GS 11"
        self.assertEqual(C.classi_da_paren(paren, self.DRAPPO), "fattucchiere 3/inquisitore 9")
        self.assertIsNone(C.classi_da_paren(paren, "07_x/a.md"))
        self.assertIsNone(C.classi_da_paren(paren))

    def test_il_3_5_resta_quello_di_prima(self):
        classi, razze = C.entita_di("dnd35")
        self.assertEqual(classi, frozenset(C.CLASSI))
        self.assertEqual(razze, frozenset(C.RAZZE))

    def test_pf1e_contiene_il_3_5(self):
        classi, razze = C.entita_di("pf1e")
        self.assertTrue(frozenset(C.CLASSI) <= classi)
        self.assertTrue(frozenset(C.RAZZE) <= razze)
        self.assertIn("kitsune", razze)          # razze ARG dalla PR #318
        self.assertNotIn("kitsune", C.entita_di("dnd35")[1])


class Creature(unittest.TestCase):
    def blocco(self, tipo, taglia="medium", gs=7, seed=42):
        sb, _ = G.genera(gs, tipo=tipo, taglia=taglia, rng=random.Random(seed))
        return sb, CP.converti(sb, tipo, taglia,
                               pf_bersaglio=G.bersaglio_di(gs, "bruto", piu_cattivi=False)[0]["pf"])

    def test_non_morto_tiene_i_pf_col_carisma(self):
        sb, (pf, conto) = self.blocco("undead")
        self.assertEqual(pf.pf_dado.split("d")[1].split("+")[0], "8")       # 3.5 d12, PF1e d8
        # lotto 5: il 3.5 non ha Costituzione (pf = soli dadi, sotto il bersaglio);
        # il PF1e porta i pf sul bersaglio del GS col Carisma
        self.assertIn("Cos —", sb.attributi)
        bersaglio = G.bersaglio_di(7, "bruto", piu_cattivi=False)[0]["pf"]
        self.assertLess(int(sb.pf), bersaglio)
        self.assertLessEqual(abs(int(pf.pf) - bersaglio), 14 // 2 + 1)
        self.assertIn("Car 16", pf.attributi)
        self.assertIn("Cos —", pf.attributi)

    def test_costrutto_bab_pieno(self):
        sb, (pf, conto) = self.blocco("construct")
        self.assertTrue(any("BAB +14 (3.5: +10)" in r for r in conto), conto)
        # pf bonus per taglia dalle schede del Bestiary (Medium +20, Animated Object 3d10+20)
        self.assertTrue(any("pf bonus del costrutto medium: +20" in r for r in conto), conto)
        self.assertTrue(pf.pf_dado.endswith("+20"), pf.pf_dado)

    def test_i_blocchi_convertiti_passano_il_cancello_pf1e(self):
        import conformita_statblocchi as CS
        for tipo, taglia, gs in (("construct", "large", 9), ("undead", "medium", 7), ("dragon", "huge", 14),
                                 ("giant", "large", 9), ("outsider", "medium", 7), ("construct", "small", 3)):
            with self.subTest(tipo=tipo, taglia=taglia):
                sb, (pf, _) = self.blocco(tipo, taglia=taglia, gs=gs)
                self.assertEqual(CS.conti_del_recinto({"sb": pf, "prosa": "", "riga": 1}, sistema="pf1e"), [])

    def test_bmc_dmc_con_la_taglia(self):
        sb, (pf, conto) = self.blocco("dragon", taglia="huge", gs=14, seed=7)
        voce = next(v for v in pf.voci if v.startswith("Manovre"))
        self.assertEqual(voce, "Manovre: BMC +27, DMC 37")      # 19 BAB +6 For +2 taglia

    def test_gigante_diventa_umanoide(self):
        sb, (pf, conto) = self.blocco("giant")
        self.assertIn("humanoid", pf.tipo)
        self.assertIn("generato-PRD-PF1e", pf.fonte)

    def test_esterno_due_ts_a_scelta_deterministici(self):
        self.assertEqual(CP.ts_buoni("outsider", S.dati("pf1e", "creature.costruzione")["tipi"]["outsider"]),
                         ("temp", "rifl"))



class CreatureConClassi(unittest.TestCase):
    """PNG con livelli di classe in PF1e (audit dei plugin, ADR-0121): prima
    erano rifiutati. Si costruiscono da zero con classi.toml e creature.toml,
    generati dal PRD e misurati riga per riga da misura_plugin_regole.py."""

    def blocco(self, testo, gs=7, seed=42, ruolo="bruto"):
        dati = S.dati("pf1e", "creature.costruzione")
        return G.genera_png_pf1e(gs, ruolo=ruolo, classi=CP.leggi_classi(testo, dati),
                             rng=random.Random(seed))

    def test_ogni_classe_del_prd_si_genera(self):
        dati = S.dati("pf1e", "creature.costruzione")
        for en, v in dati["classi"].items():
            if v["gruppo"] == "prestigio":
                continue
            with self.subTest(classe=en):
                sb, conto = self.blocco(f"{en}:5")
                self.assertTrue(sb.completo, sb.mancanti())
                self.assertEqual(sb.gs, "4")                          # PRD: livelli − 1

    def test_prestigio_in_multiclasse(self):
        sb, conto = self.blocco("mago:5,mistificatore arcano:3")
        self.assertIn("Incantatore di livello 8 (mago, INT +3) — 3 livelli dalle classi di prestigio", sb.voci)
        # dal lotto 4 delle regole complete i requisiti si leggono dal PRD: quelli che
        # non si contano (gradi, allineamento, attacco furtivo) vanno al DM
        self.assertTrue(any(r.startswith("requisiti di arcane trickster") for r in conto.righe), conto.righe)
        self.assertTrue(any("da verificare dal DM" in r for r in conto.righe))
        self.assertEqual(sb.pf_dado.split("+")[:2], ["5d6", "3d6"])

    def test_teurgo_mistico_avanza_due_classi(self):
        sb, _ = self.blocco("chierico:3,mago:3,teurgo mistico:4")
        self.assertIn("Incantatore di livello 7 (chierico, SAG +3) — 4 livelli dalle classi di prestigio",
                      sb.voci)
        self.assertTrue(any(v.startswith("Incantatore di livello 7 (mago") for v in sb.voci), sb.voci)

    def test_pf_col_primo_dado_al_massimo(self):
        sb, _ = self.blocco("guerriero:9", gs=8, seed=1)
        cos = int(sb.attributi.split("Cos ")[1].split()[0])
        # Robustezza PF1e: +3, o +1 per DV se sono più di 3 (lotto 3 delle regole complete)
        robustezza = 9 if any("Robustezza" in v for v in sb.voci if v.startswith("Talenti:")) else 0
        self.assertEqual(int(sb.pf), 10 + 44 + 9 * ((cos - 10) // 2) + robustezza)  # 10 + ⌈8 × 5,5⌉ + Cos

    def test_griglie_pf1e(self):
        sb, _ = self.blocco("mago:5")
        self.assertIn("Incantesimi al giorno (dal 1° livello): 3/2/1 · trucchetti a volontà", sb.voci)
        sb, _ = self.blocco("ranger:8")
        self.assertIn("Incantatore di livello 5 (ranger, SAG +3)", sb.voci)    # LI = livello − 3
        sb, _ = self.blocco("alchimista:6")
        self.assertIn("Estratti al giorno (dal 1° livello): 4/3", sb.voci)

    def test_conosciuti_dell_oracolo(self):
        sb, _ = self.blocco("oracolo:7")
        attesi = "/".join(map(str, S.dati("pf1e", "creature.costruzione")["conosciuti"]["oracle"]["7"]))
        self.assertIn(f"Incantesimi conosciuti: {attesi}", sb.voci)

    def test_ts_di_prestigio_pf1e(self):
        self.assertEqual(CP.ts_di_classe(10, ("temp",), "prestigio"), {"temp": 5, "rifl": 3, "vol": 3})
        self.assertEqual(CP.ts_di_classe(1, ("temp",), "prestigio"), {"temp": 1, "rifl": 0, "vol": 0})
        self.assertEqual(CP.ts_di_classe(20, ("vol",), "base"), {"temp": 6, "rifl": 6, "vol": 12})

    def test_i_blocchi_passano_il_cancello_pf1e(self):
        # pf (primo dado al massimo), CA e il resto dei conti PF1e dei moduli
        import conformita_statblocchi as CS
        for testo in ("guerriero:9", "bardo:10", "ranger:8", "magus:7", "oracolo:12", "adepto:6",
                      "combattente:3", "ladro:1", "intrepido:5", "sacerdote guerriero:11"):
            with self.subTest(classe=testo):
                sb, _ = self.blocco(testo)
                self.assertEqual(CS.conti_del_recinto({"sb": sb, "prosa": "", "riga": 1}, sistema="pf1e"), [])

    def test_classe_ignota(self):
        with self.assertRaises(SystemExit) as e:
            G.main(["--gs", "7", "--sistema", "pf1e", "--classe", "pasticciere:3"])
        self.assertIn("senza riga PF1e", str(e.exception))

    def test_da_riga_di_comando(self):
        self.assertEqual(G.main(["--gs", "7", "--sistema", "pf1e", "--classe", "magus:3,guerriero:2",
                                 "--seed", "1", "--json"]), 0)


if __name__ == "__main__":
    unittest.main()
