"""Il generatore contro i mostri veri.

Il criterio d'accettazione del piano è uno solo e non è negoziabile: *il
risultato supera il collaudo sul GS — e se non passa, il generatore è sbagliato*.

La prima versione non passava: un «GS 7» con 38 punti ferita e CA 12, cioè meno
della metà di quello che ha un mostro di GS 7 nel manuale. Il collaudo l'ha detto
al primo giro (−55%), ed è esattamente il lavoro per cui esiste. Queste sono le
ancore che hanno chiuso quel difetto: mostri del SRD 3.5, con i loro numeri.

Le bande sono larghe di proposito. Un mostro di GS 7 nel SRD sta fra i 76 punti
ferita della Chimera e i 102 dell'Ettin: pretendere che il generatore centri un
numero solo vorrebbe dire pretendere che esista un solo mostro di GS 7.
"""
from __future__ import annotations

import io
import random
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import genera_creatura as G  # noqa: E402
from dmcore import caratteristiche as CAR  # noqa: E402
from dmcore import incantesimi as INC  # noqa: E402
from dmcore import tabelle as T  # noqa: E402

#: Mostri del SRD 3.5, con i numeri del manuale. Sono le ancore: se il
#: generatore si allontana da questi, si è allontanato dal gioco.
#: (nome, GS, tipo, taglia, pf, CA)
ANCORE_SRD = [
    ("Ogre",                   3, "giant",         "large",  29, 16),
    ("Troll",                  5, "giant",         "large",  63, 16),
    ("Ettin",                  6, "giant",         "large",  65, 18),
    ("Chimera",                7, "magical beast", "large",  76, 19),
    ("Gigante delle Colline",  7, "giant",         "large", 102, 20),
    ("Osyluth (diavolo osso)", 9, "outsider",      "large",  95, 25),
]


class ControlDelGS(unittest.TestCase):
    """La creatura generata sta nella fascia dei mostri veri di quel GS."""

    def test_ogni_ancora_del_srd(self):
        for nome, gs, tipo, taglia, pf, ca in ANCORE_SRD:
            with self.subTest(mostro=nome, gs=gs):
                sb, _ = G.genera(gs, tipo=tipo, taglia=taglia, ruolo="bruto",
                                 rng=random.Random(0))
                scarto = abs(int(sb.pf) - pf) / pf
                self.assertLess(scarto, 0.60,
                                f"{nome}: {sb.pf} pf contro i {pf} del manuale")
                self.assertLessEqual(abs(int(sb.ca) - ca), 6,
                                     f"{nome}: CA {sb.ca} contro {ca}")

    def test_nessun_ruolo_e_indifeso(self):
        """Il difetto della prima versione: −55% sui pf, per ogni ruolo."""
        for gs in (1, 3, 5, 7, 10, 13, 16, 20):
            for ruolo in G.RUOLI:
                with self.subTest(gs=gs, ruolo=ruolo):
                    sb, _ = G.genera(gs, ruolo=ruolo, rng=random.Random(0))
                    bersaglio, _ = G.bersaglio_di(gs, ruolo, piu_cattivi=False)
                    scarto = (int(sb.pf) - bersaglio["pf"]) / bersaglio["pf"]
                    self.assertGreater(scarto, -0.25,
                                       f"GS {gs} {ruolo}: {sb.pf} pf contro un "
                                       f"bersaglio di {bersaglio['pf']}")
                    self.assertLess(scarto, 0.25)

    def test_i_punteggi_restano_nella_banda(self):
        """Cos 24 e Des 28 a GS 7 erano il sintomo: numeri giusti, mostro sbagliato."""
        for gs in range(1, 21):
            sb, _ = G.genera(gs, ruolo="bruto", rng=random.Random(0))
            for pezzo in re.findall(r"[A-Z][a-z]{2} (\d+)", sb.attributi):
                with self.subTest(gs=gs, punteggio=pezzo):
                    self.assertLessEqual(int(pezzo), 10 + 2 * G.MOD_MAX)

    def test_il_conto_e_sempre_scritto(self):
        """Un numero senza il suo conto è un numero di cui non ci si fida."""
        sb, conto = G.genera(7, ruolo="bruto", rng=random.Random(0))
        self.assertGreaterEqual(len(conto.righe), 5)
        self.assertTrue(any("bersaglio" in r for r in conto.righe))
        self.assertTrue(any("pf" in r for r in conto.righe))
        self.assertIn("generato-SRD-3.5", sb.fonte)


class VariantePiuCattiva(unittest.TestCase):
    """`--piu-cattivi` = template Advanced di PF1e, senza alzare il GS."""

    def test_alza_tutto_quello_che_advanced_alza(self):
        mite, _ = G.genera(7, ruolo="bruto", rng=random.Random(0))
        cattivo, conto = G.genera(7, ruolo="bruto", piu_cattivi=True,
                                  rng=random.Random(0))
        self.assertGreater(int(cattivo.pf), int(mite.pf))
        self.assertGreater(int(cattivo.ca), int(mite.ca))
        self.assertNotEqual(cattivo.attacchi, mite.attacchi)
        self.assertNotEqual(cattivo.ts, mite.ts)

    def test_dichiara_di_valere_un_gs_in_piu(self):
        """La cosa che rende onesta la variante: lo dice la creatura stessa."""
        sb, conto = G.genera(7, ruolo="bruto", piu_cattivi=True,
                             rng=random.Random(0))
        self.assertEqual(sb.gs, "7", "il GS venduto resta quello chiesto")
        self.assertTrue(any("GS 8" in v for v in sb.voci),
                        "deve dire che in realtà picchia come un GS 8")
        self.assertTrue(conto.rincari, "i rincari vanno elencati")
        self.assertIn("piu-cattivi", sb.fonte)

    def test_le_caratteristiche_salgono_di_quattro(self):
        mite, _ = G.genera(9, ruolo="comandante", rng=random.Random(0))
        cattivo, _ = G.genera(9, ruolo="comandante", piu_cattivi=True,
                              rng=random.Random(0))
        prima = [int(n) for n in re.findall(r"\d+", mite.attributi)]
        dopo = [int(n) for n in re.findall(r"\d+", cattivo.attributi)]
        self.assertEqual(dopo, [n + G.ADVANCED["caratteristiche"] for n in prima])


class Incantatori(unittest.TestCase):
    """La parte che il DM ha chiesto per nome."""

    def test_gli_slot_vengono_dalla_tabella_di_classe(self):
        sb, _ = G.genera(9, ruolo="blaster", classe=("mago", 9),
                         rng=random.Random(0))
        atteso = "/".join(str(n) for n in T.MAGO[9])
        self.assertTrue(any(atteso in v for v in sb.voci),
                        f"gli slot devono essere quelli del SRD: {atteso}")

    def test_la_cd_massima_sta_sulla_riga_del_gs(self):
        """Il controllo che chiude il cerchio: la CD di un incantatore di GS n
        deve stare sulla CD primaria della riga di GS n."""
        for gs, livelli in ((5, 5), (9, 9), (13, 13), (16, 16)):
            for classe in ("mago", "chierico", "stregone"):
                with self.subTest(gs=gs, classe=classe):
                    sb, _ = G.genera(gs, ruolo="controllore",
                                     classe=(classe, livelli), rng=random.Random(0))
                    cd = int(re.search(r"CD (\d+)\)", " ".join(sb.voci)).group(1))
                    atteso = T.riga_gs(gs)[0]["cd"]
                    self.assertLessEqual(abs(cd - atteso), 3,
                                         f"CD {cd} contro una riga da {atteso}")

    def test_lo_stregone_porta_gli_incantesimi_conosciuti(self):
        sb, _ = G.genera(11, ruolo="blaster", classe=("stregone", 11),
                         rng=random.Random(0))
        self.assertTrue(any("conosciuti" in v for v in sb.voci))

    def test_il_chierico_ricorda_i_domini(self):
        sb, _ = G.genera(7, ruolo="comandante", classe=("chierico", 7),
                         rng=random.Random(0))
        self.assertTrue(any("domini" in v for v in sb.voci))

    def _preparati(self, sb):
        """La riga degli incantesimi scelti, comunque si chiami.

        Un preparato li «prepara», un bardo e uno stregone li «conoscono»: sono
        due etichette diverse per la stessa riga, e un test che ne cercasse una
        sola passerebbe a vuoto sulla metà delle classi.
        """
        for v in sb.voci:
            for etichetta in ("Preparati — ", "Conosciuti — "):
                if v.startswith(etichetta):
                    return v.removeprefix(etichetta)
        return ""

    def _voci_per_livello(self, riga):
        for pezzo in riga.split(" · "):
            liv = int(pezzo.split("°")[0])
            for nome in pezzo.split(": ", 1)[1].split(", "):
                yield liv, nome

    def test_gli_incantesimi_vengono_dalla_lista_di_QUELLA_classe(self):
        """Il criterio d'accettazione del lotto I.

        La versione vecchia di questo test controllava contro `G.INCANTESIMI` —
        cioè contro la lista del **ruolo**, che era il difetto stesso: un druido
        con incantesimi da mago lo superava senza fare una piega. Ora il
        confronto è con la lista della classe, e i nomi che non le appartengono
        cadono.
        """
        casi = [("mago", "controllore"), ("mago", "blaster"),
                ("chierico", "supporto"), ("druido", "controllore"),
                ("druido", "blaster"), ("bardo", "controllore"),
                ("stregone", "blaster")]
        for classe, funzione in casi:
            for livelli in (5, 9, 13):
                with self.subTest(classe=classe, funzione=funzione, livelli=livelli):
                    sb, _ = G.genera(livelli, ruolo="controllore",
                                     classe=(classe, livelli), funzione=funzione,
                                     rng=random.Random(4))
                    riga = self._preparati(sb)
                    self.assertTrue(riga, "un incantatore senza incantesimi scelti")
                    lista, _usata = INC.cella(classe, funzione)
                    for liv, nome in self._voci_per_livello(riga):
                        self.assertIn(nome, lista[liv],
                                      f"«{nome}» non è nella lista di {classe} "
                                      f"({funzione}) al {liv}° livello")

    def test_nessun_incantesimo_sopra_il_livello_lanciabile(self):
        sb, _ = G.genera(5, ruolo="blaster", classe=("mago", 5),
                         rng=random.Random(1))
        riga = self._preparati(sb)
        massimo = max(liv for liv, _ in self._voci_per_livello(riga))
        self.assertEqual(massimo, T.livello_massimo(T.MAGO, 5))

    def test_ogni_ruolo_ha_una_funzione_da_incantatore(self):
        """Un ruolo senza funzione finirebbe sul ripiego generico e nessuno se
        ne accorgerebbe: la creatura uscirebbe comunque con degli incantesimi."""
        for ruolo in G.RUOLI:
            with self.subTest(ruolo=ruolo):
                self.assertIn(ruolo, INC.FUNZIONE_DA_RUOLO)
                self.assertIn(INC.FUNZIONE_DA_RUOLO[ruolo], INC.FUNZIONI)

    def test_il_druido_adesso_gli_incantesimi_li_prende(self):
        """Il difetto per cui il lotto I esiste, girato: prima il druido usciva
        vuoto per non uscire sbagliato, e il vuoto era il debito."""
        for funzione in ("controllore", "blaster", "supporto", "utilita"):
            with self.subTest(funzione=funzione):
                sb, _ = G.genera(12, ruolo="controllore", classe=("druido", 12),
                                 funzione=funzione, rng=random.Random(0))
                riga = self._preparati(sb)
                self.assertTrue(riga, "il druido è tornato vuoto")
                nomi = {n for _, n in self._voci_per_livello(riga)}
                for da_mago in ("armatura magica", "sonno", "palla di fuoco"):
                    self.assertNotIn(da_mago, nomi)
                for da_chierico in ("benedizione", "santuario", "scudo della fede"):
                    self.assertNotIn(da_chierico, nomi)

    def test_l_adepto_resta_l_unico_a_rifiutarsi(self):
        """Il residuo dichiarato: fuori dalle 21 celle approvate dal DM, e il
        rifiuto va dichiarato invece che lasciato in silenzio."""
        sb, _ = G.genera(12, ruolo="comandante", classe=("adepto", 12),
                         rng=random.Random(0))
        self.assertFalse(self._preparati(sb))
        self.assertTrue(any("da scegliere a mano" in v for v in sb.voci))

    def test_le_classi_coperte_gli_incantesimi_li_prendono(self):
        for classe in ("mago", "stregone", "chierico", "druido", "bardo"):
            with self.subTest(classe=classe):
                sb, _ = G.genera(9, ruolo="controllore", classe=(classe, 9),
                                 rng=random.Random(0))
                self.assertTrue(self._preparati(sb))

    def test_ranger_e_paladino_lanciano_da_tre_livelli_sotto(self):
        """Il livello dell'incantatore non è il livello di classe, e un blocco
        che li confonde ha la CD sbagliata di due punti."""
        for classe in ("ranger", "paladino"):
            with self.subTest(classe=classe):
                sb, _ = G.genera(12, ruolo="comandante", classe=(classe, 12),
                                 rng=random.Random(0))
                riga = next(v for v in sb.voci if v.startswith("Incantatore"))
                self.assertIn("Incantatore di livello 9", riga)
                self.assertIn("livello di classe 12", riga)
                self.assertTrue(self._preparati(sb))

    def test_sotto_il_quarto_ranger_e_paladino_non_lanciano(self):
        sb, _ = G.genera(3, ruolo="comandante", classe=("paladino", 3),
                         rng=random.Random(0))
        self.assertFalse(self._preparati(sb))
        self.assertTrue(any("dal 4° livello di classe" in v for v in sb.voci))

    def test_il_bardo_porta_i_suoi_conosciuti_non_quelli_dello_stregone(self):
        sb, _ = G.genera(10, ruolo="comandante", classe=("bardo", 10),
                         rng=random.Random(0))
        riga = next(v for v in sb.voci if v.startswith("Incantesimi conosciuti"))
        atteso = "/".join(str(n) for n in T.BARDO_CONOSCIUTI[10])
        self.assertIn(atteso, riga)
        self.assertNotEqual(T.BARDO_CONOSCIUTI[10], T.STREGONE_CONOSCIUTI[10])

    def test_la_funzione_scavalca_quella_del_ruolo(self):
        """I due assi sono davvero due: un bruto con livelli da chierico è un
        chierico da guerra, e deve poter prendere la lista di supporto."""
        a, _ = G.genera(9, ruolo="bruto", classe=("chierico", 9),
                        rng=random.Random(2))
        b, _ = G.genera(9, ruolo="bruto", classe=("chierico", 9),
                        funzione="controllore", rng=random.Random(2))
        self.assertNotEqual(self._preparati(a), self._preparati(b))
        self.assertIn("funzione=supporto", a.fonte)
        self.assertIn("funzione=controllore", b.fonte)

    def test_gli_incantesimi_pf1e_solo_a_richiesta(self):
        base, _ = G.genera(13, ruolo="blaster", classe=("mago", 13),
                           rng=random.Random(6))
        pf, conto = G.genera(13, ruolo="blaster", classe=("mago", 13),
                             incantesimi_pf1e=True, rng=random.Random(6))
        self.assertNotIn("PF1e:", self._preparati(base))
        self.assertIn("PF1e:", self._preparati(pf))
        self.assertTrue(any("PF1e" in r for r in conto.rincari),
                        "un innesto PF1e non dichiarato nei rincari è invisibile")
        self.assertIn("incantesimi=PF1e", pf.fonte)

    def test_piu_cattivi_accende_anche_la_lista(self):
        """«Più cattivo a pari GS» vale per il template e per la lista: due
        interruttori per una cosa sola sarebbero due modi di dimenticarne uno."""
        sb, _ = G.genera(13, ruolo="blaster", classe=("mago", 13),
                         piu_cattivi=True, rng=random.Random(6))
        self.assertIn("PF1e:", self._preparati(sb))
        solo_template, _ = G.genera(13, ruolo="blaster", classe=("mago", 13),
                                    piu_cattivi=True, incantesimi_pf1e=False,
                                    rng=random.Random(6))
        self.assertNotIn("PF1e:", self._preparati(solo_template))

    def test_gli_aumenti_ogni_quattro_livelli(self):
        """Senza, un mago di 9° usciva con Intelligenza 15."""
        sb, _ = G.genera(9, ruolo="blaster", classe=("mago", 9),
                         rng=random.Random(0))
        intelligenza = int(re.search(r"Int (\d+)", sb.attributi).group(1))
        self.assertEqual(intelligenza, T.ELITE[0] + 9 // 4)


class IlConfine(unittest.TestCase):
    """ADR-0033: lo strumento propone, nel canone scrive il DM."""

    def test_si_rifiuta_di_scrivere_nel_bestiario(self):
        for dove in ("Bestiario", "Bestiario/mostri", "Bestiario/villain/x"):
            with self.subTest(cartella=dove):
                with self.assertRaises(SystemExit) as e:
                    G._rifiuta_bestiario(ROOT / dove)
                self.assertIn("Bestiario", str(e.exception))

    def test_una_cartella_di_lavoro_va_bene(self):
        with tempfile.TemporaryDirectory() as d:
            G._rifiuta_bestiario(Path(d))   # non solleva

    def test_scrive_dove_gli_si_dice(self):
        with tempfile.TemporaryDirectory() as d:
            with redirect_stdout(io.StringIO()):
                G.main(["--gs", "5", "--ruolo", "bruto", "--in", d, "--seed", "1"])
            prodotti = list(Path(d).glob("*.md"))
            self.assertEqual(len(prodotti), 1)
            self.assertIn("```statblocco", prodotti[0].read_text(encoding="utf-8"))


class LaRigaDiComando(unittest.TestCase):
    def test_niente_abbreviazioni(self):
        """Nel lotto H `--apply` passava come abbreviazione di `--apply-ts`.
        `--piu-cattivi` non deve poter essere invocato per sbaglio."""
        p = G.costruisci_parser()
        with self.assertRaises(SystemExit):
            p.parse_args(["--gs", "5", "--piu"])

    def test_il_gs_sta_fra_uno_e_venti(self):
        with self.assertRaises(SystemExit):
            G.main(["--gs", "0"])
        with self.assertRaises(SystemExit):
            G.main(["--gs", "21"])

    def test_lo_stesso_seed_da_la_stessa_creatura(self):
        a, _ = G.genera(7, ruolo="bruto", rng=random.Random(99))
        b, _ = G.genera(7, ruolo="bruto", rng=random.Random(99))
        self.assertEqual(a, b)

    def test_il_json_e_leggibile(self):
        import json
        f = io.StringIO()
        with redirect_stdout(f):
            G.main(["--gs", "7", "--json", "--quanti", "2", "--seed", "3"])
        dati = json.loads(f.getvalue())
        self.assertEqual(len(dati), 2)
        self.assertIn("blocco", dati[0])
        self.assertIn("conto", dati[0])

    def test_i_tipi_e_le_classi_ignote_si_rifiutano(self):
        import argparse
        with self.assertRaises(argparse.ArgumentTypeError):
            G._tipo("draghetto")
        with self.assertRaises(argparse.ArgumentTypeError):
            G._classe("negromante:5")
        with self.assertRaises(argparse.ArgumentTypeError):
            G._classe("mago")


class IlCarattere(unittest.TestCase):
    """Lotto E del piano: senza, escono mostri intercambiabili."""

    def test_ogni_ruolo_ha_le_sue_voci(self):
        for ruolo in G.RUOLI:
            with self.subTest(ruolo=ruolo):
                self.assertIn(ruolo, G.CARATTERE)
                self.assertGreaterEqual(len(G.CARATTERE[ruolo]), 3)
                for talento, tattica, debolezza in G.CARATTERE[ruolo]:
                    self.assertTrue(talento and tattica and debolezza)

    def test_la_creatura_esce_con_una_cosa_sua(self):
        sb, _ = G.genera(7, ruolo="bruto", rng=random.Random(0))
        self.assertTrue(sb.tattica, "senza tattica è un mucchio di numeri")
        self.assertTrue(any("Debolezza" in v for v in sb.voci),
                        "senza debolezza i PG non hanno niente da trovare")

    def test_due_creature_dello_stesso_ruolo_non_sono_identiche(self):
        visti = {G.genera(7, ruolo="bruto", rng=random.Random(s))[0].tattica
                 for s in range(20)}
        self.assertGreater(len(visti), 1)


class UnaTabellaDeiRuoli(unittest.TestCase):
    """D2 di `PIANO-QUALITA-DEL-CODICE` (E6-E7): l'ordine viene da `PROFILI`.

    Fino a E6 ogni ruolo aveva un ordine suo, e su sei ruoli quattro non
    coincidevano con il profilo omonimo con cui `genera_attributi` sceglie gli
    `attributi` del Bestiario. Questi test guardano il blocco generato, non la
    tabella: un ordine riscritto a mano nel generatore li fa rossi.
    """

    def test_ogni_ruolo_nomina_un_profilo_che_esiste(self):
        for nome, R in G.RUOLI.items():
            with self.subTest(ruolo=nome):
                self.assertTrue(CAR.profilo_esatto(R.profilo))

    def test_il_png_esce_nell_ordine_del_profilo(self):
        # il guerriero non lancia: l'ordine e' quello del profilo e basta
        for nome, R in G.RUOLI.items():
            for elite in (True, False):
                with self.subTest(ruolo=nome, elite=elite):
                    sb, _ = G.genera(5, ruolo=nome, classe=("guerriero", 5),
                                     elite=elite, rng=random.Random(0))
                    letti = tuple(re.findall(r"([A-Z][a-z]{2}) \d+", sb.attributi))
                    self.assertEqual(letti, CAR.profilo_esatto(R.profilo))

    def test_il_tiratore_ha_le_caratteristiche_del_profilo_ranged(self):
        # l'ancora numerica di D2 = a: prima usciva Cos 14 Sag 13 For 12
        sb, _ = G.genera(5, ruolo="tiratore", classe=("guerriero", 5),
                         rng=random.Random(0))
        self.assertEqual(sb.attributi, "Des 16 For 14 Cos 13 Sag 12 Int 10 Car 8")

    def test_un_profilo_che_non_esiste_non_ripiega(self):
        self.assertEqual(CAR.profilo_di("sconosciuto"), CAR.PROFILO_DI_RIPIEGO)
        with self.assertRaises(KeyError):
            CAR.profilo_esatto("sconosciuto")
        with self.assertRaises(KeyError):
            CAR.profilo_esatto("psi onico")    # niente ricerca per sottostringa

    def test_la_caratteristica_da_incantatore_passa_davanti(self):
        v = CAR.matrice_png("arcane", 9, True, lancia_su="Sag")
        self.assertEqual(list(v)[0], "Sag")
        self.assertEqual(v["Sag"], 15 + 2)
        self.assertEqual(list(v)[1:], [c for c in CAR.profilo_esatto("arcane") if c != "Sag"])

    def test_un_aumento_ogni_quattro_livelli_sulla_prima(self):
        for livelli, aumenti in ((3, 0), (4, 1), (11, 2), (20, 5)):
            with self.subTest(livelli=livelli):
                v = CAR.matrice_png("brute", livelli, False)
                self.assertEqual(v["For"], CAR.ARRAY_STANDARD[0] + aumenti)
                self.assertEqual(sorted(v.values())[:-1], sorted(CAR.ARRAY_STANDARD)[:-1])


if __name__ == "__main__":
    unittest.main()
