"""La terza prova del nove: un sistema fuori dalla famiglia d20.

F6 (`test_prova_del_nove_2.py`) ha provato un sistema d20 con formule e
algoritmo propri. Qui il plugin finto `scripts/tests/dati/prova-mucchio-d10/`
non ha famiglia: si tira un mucchio di d10 (attributo + abilità), ogni dado da 8
in su è un successo e il 10 si rilancia, e la sfida di un incontro è una
minaccia in successi attesi, non un EL. Le meccaniche sono scritte con parole e
numeri nostri (scelta del DM del 2026-11-08: Lupi Mannari, solo come prova).

Cosa deve reggere senza toccare il nucleo:

1. il cancello resta verde con il sistema attivo, e un file della sua cartella
   prende il sistema nuovo;
2. le formule sono quelle del plugin e nessuna formula d20 passa di nascosto;
3. il tiro del plugin dà probabilità esatte (somma 1, successi attesi n/3) che
   un tiro simulato con seme fisso conferma, anche nella variante «uno annulla»
   solo cambiando i dati;
4. `suggest_encounter` usa la minaccia del plugin;
5. i termini d20 in un modulo del sistema si segnalano, e le abilità sono le sue;
6. ogni strumento d20 sa dire che su questo sistema non può lavorare, invece
   di usare le tabelle 3.5 senza dirlo: il censimento è in `CENSIMENTO`.
"""
from __future__ import annotations

import random
import shutil
import sys
import tempfile
import tomllib
import unittest
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import sistemi as CLI  # noqa: E402
import suggest_encounter as SE  # noqa: E402
import validate_modules as VM  # noqa: E402
from dmcore import formule as F  # noqa: E402
from dmcore import sistemi as S  # noqa: E402

FINTO = REPO / "scripts" / "tests" / "dati" / "prova-mucchio-d10"
ID = "prova-mucchio-d10"
CARTELLA = "moduli-di-prova"

#: Il censimento del 2026-11-08 sui 20 strumenti del manifest che chiedono
#: capacità di sistema: quanti trovano nel plugin tutte le capacità che chiedono
#: (lavorano), quanti una parte, quanti nessuna (devono rifiutare il file).
CENSIMENTO = {
    "tutte": {"domande_developer", "validate_modules", "validate_prosa", "validate_standalone"},
    "in_parte": {"suggest_encounter",  # la minaccia sì, le schede del Bestiario no
                 "genera_creatura",    # formule.regole sì (dichiarata dalla #376), il resto no: rifiuta
                 "verifica_scheda"},   # dichiara le 13 capacità che legge (lotto 4): formule.regole sì, i conti d20 no
}
CENSIMENTO_NESSUNA = 15  # verifica_scheda passa in «in_parte» col lotto 4 di ADR-0126. Prima: genera_creatura passa in «in_parte» con la #376; +verifica_talenti e verifica_scheda (ADR-0124): talenti e conti sono d20


def _file_dei_plugin() -> "set[str]":
    fuori = set()
    for f in (REPO / "sistemi").glob("*/sistema.toml"):
        for c in tomllib.loads(f.read_text(encoding="utf-8")).get("capacita", {}).values():
            fuori.update(c.get("dati", []))
            fuori.update(v.split(":", 1)[0] for v in c.get("codice", []))
    return fuori


class ProvaNonD20(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        r = cls.root = Path(cls._tmp.name)
        shutil.copytree(REPO / "sistemi", r / "sistemi")
        for rel in _file_dei_plugin() | {"scripts/tools.manifest.json"}:
            (r / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / rel, r / rel)
        for d in (REPO / "skills").iterdir():
            if (d / "SKILL.md").is_file():
                (r / "skills" / d.name).mkdir(parents=True)
                (r / "skills" / d.name / "SKILL.md").write_text("", encoding="utf-8")
        shutil.copytree(FINTO, r / "sistemi" / ID, ignore=shutil.ignore_patterns("__pycache__"))
        cfg = (REPO / "sistemi.toml").read_text(encoding="utf-8")
        letto = tomllib.loads(cfg)
        for cartella in {**letto.get("moduli", {}), **letto.get("ambientazioni", {}).get("moduli", {})}:
            (r / cartella).mkdir(parents=True)
        (r / CARTELLA).mkdir()
        cfg = cfg.replace('attivi = ["dnd35", "pf1e"]', f'attivi = ["dnd35", "pf1e", "{ID}"]')
        cfg = cfg.replace("[moduli]\n", f'[moduli]\n"{CARTELLA}" = "{ID}"\n')
        (r / "sistemi.toml").write_text(cfg, encoding="utf-8")
        cls._root_vero = S.ROOT
        S.ROOT = r
        S._carica.cache_clear()
        S._manifest.cache_clear()

    @classmethod
    def tearDownClass(cls):
        S.ROOT = cls._root_vero
        S._carica.cache_clear()
        S._manifest.cache_clear()
        cls._tmp.cleanup()

    # 1 ---------------------------------------------------------------------
    def test_il_cancello_resta_verde(self):
        self.assertIn(ID, S.attivi())
        self.assertEqual(S.problemi(self.root, CLI.strumenti(self.root)), [])
        self.assertEqual(F.problemi(self.root), [])

    def test_il_sistema_non_e_della_famiglia_d20(self):
        self.assertNotIn("famiglia", S.plugin(ID))
        self.assertEqual(S.sistema_di(f"{CARTELLA}/capitolo.md"), ID)
        self.assertNotIn("potenze", S.moduli(ID))   # niente codice d20 per eredità

    # 2 ---------------------------------------------------------------------
    def test_le_formule_sono_del_plugin(self):
        self.assertEqual(F.formula("mucchio", ID)(attributo=3, abilita=2), 5)
        self.assertEqual(F.formula("mucchio_con_penalita", ID)(attributo=1, abilita=1, penalita=4), 0)
        self.assertEqual(F.formula("difesa", ID)(destrezza=4, prontezza=2), 2)
        self.assertEqual(F.formula("salute", ID)(vigore=3, taglia=5), 8)

    def test_nessuna_formula_d20_passa_di_nascosto(self):
        for nome in F.formule("d20"):
            with self.subTest(formula=nome), self.assertRaises(F.ErroreFormula):
                F.formula(nome, ID)

    # 3 ---------------------------------------------------------------------
    def _dist(self, n, **dati):
        base = S.dati(ID, "incontri.livello")
        return S.modulo(ID, "successi")({**base, **dati})(n)

    def test_le_probabilita_sommano_a_uno(self):
        for n in range(0, 11):
            for variante in ({}, {"soglia": 6, "rilancio": None, "uno_annulla": True}):
                with self.subTest(n=n, variante=variante):
                    self.assertEqual(sum(self._dist(n, **variante).values()), 1)

    def test_un_dado_ha_tre_su_dieci_di_riuscire(self):
        d = self._dist(1)
        self.assertEqual(d[0], Fraction(7, 10))
        self.assertEqual(d[1], Fraction(2, 10) + Fraction(1, 10) * Fraction(7, 10))

    def test_i_successi_attesi_sono_un_terzo_per_dado(self):
        for n in (1, 3, 5, 8, 10):
            media = sum(k * p for k, p in self._dist(n).items())
            self.assertAlmostEqual(float(media), n / 3, places=12)

    def test_un_tiro_simulato_conferma_le_probabilita(self):
        def tira(n, rng):
            s, dadi = 0, n
            while dadi:
                facce = [rng.randint(1, 10) for _ in range(dadi)]
                s += sum(f >= 8 for f in facce)
                dadi = sum(f == 10 for f in facce)
            return s
        rng, n, prove = random.Random(20261108), 6, 20000
        conti: "dict[int, int]" = {}
        for _ in range(prove):
            k = tira(n, rng)
            conti[k] = conti.get(k, 0) + 1
        for k, p in self._dist(n).items():
            if p > Fraction(1, 100):
                sigma = (float(p) * (1 - float(p)) / prove) ** 0.5
                self.assertLess(abs(conti.get(k, 0) / prove - float(p)), 4 * sigma, k)

    def test_la_variante_uno_annulla_cambia_solo_i_dati(self):
        d = self._dist(1, soglia=6, rilancio=None, uno_annulla=True)
        self.assertEqual(d, {-1: Fraction(1, 10), 0: Fraction(4, 10), 1: Fraction(5, 10)})
        media = sum(k * p for k, p in self._dist(4, soglia=6, rilancio=None, uno_annulla=True).items())
        self.assertEqual(media, Fraction(16, 10))

    # 4 ---------------------------------------------------------------------
    def test_suggest_encounter_usa_la_minaccia(self):
        minaccia = SE.combinatore(ID)
        self.assertAlmostEqual(minaccia([6, 6, 3]), 5.0)
        self.assertEqual(minaccia([]), 0.0)
        self.assertEqual(SE.combinatore("dnd35")([10, 10]), 12.0)   # il 3.5 resta com'era

    # 5 ---------------------------------------------------------------------
    def test_i_termini_d20_si_segnalano(self):
        regex = [r for r, _ in VM.banditi(self.root / CARTELLA / "capitolo.md")]
        import re
        def segnala(riga):
            return any(re.search(x, riga) for x in regex)
        self.assertTrue(segnala("Il lupo fa un tiro salvezza sulla Tempra"))
        self.assertTrue(segnala("Il capobranco ha CA 18 e 40 punti ferita"))
        self.assertFalse(segnala("Il capobranco tira un mucchio di 7 dadi, Vigore 4 + Rissa 3"))
        self.assertTrue(VM.banditi(REPO / "campaign" / "x.md"))      # il 3.5 ha le sue

    def test_le_abilita_sono_del_sistema(self):
        a = S.abilita(ID)
        self.assertIn("fiuto", a["nomi"])
        self.assertNotIn("osservare", a["nomi"])
        self.assertIn("Osservare", a["estranee"])

    # 6 ---------------------------------------------------------------------
    def test_il_censimento_degli_strumenti(self):
        tutte, in_parte, nessuna = set(), set(), set()
        for t, chieste in S._manifest(self.root).items():
            mancano = [c for c in chieste if S.capacita(ID, c).modo != "dati"]
            (tutte if not mancano else nessuna if len(mancano) == len(chieste) else in_parte).add(t)
        self.assertEqual(tutte, CENSIMENTO["tutte"])
        self.assertEqual(in_parte, CENSIMENTO["in_parte"])
        self.assertEqual(len(nessuna), CENSIMENTO_NESSUNA)

    def test_gli_strumenti_d20_rifiutano_invece_di_usare_il_3_5(self):
        import genera_creatura as GC
        import suggest_loot as SL
        import update_xp as UX
        with self.assertRaisesRegex(S.ErroreSistemi, "non_supportato"):
            SL.tesoro_di(ID, None)
        with self.assertRaisesRegex(S.ErroreSistemi, "non_supportato"):
            UX.soglie_di(ID, None)
        with self.assertRaisesRegex(S.ErroreSistemi, "non_supportato"):
            S.etichette(ID)       # build_booklet_html ed export_booklet_typst
        with self.assertRaisesRegex(SystemExit, "nessuna conversione"):
            GC.main(["--sistema", ID, "--gs", "3", "--tipo", "animal"])
        for t in ("conformita_statblocchi", "derive_statblocks", "genera_attributi",
                  "impronta_creature", "validate_bestiario"):
            with self.subTest(strumento=t):
                self.assertTrue(S.regole_diverse(ID, t))   # F4: saltano il file e lo dicono

    def test_le_regole_d20_non_arrivano_per_sbaglio(self):
        for cap in ("stampa.etichette", "creature.costruzione", "pe.soglie", "statblocco.campi"):
            with self.subTest(capacita=cap), self.assertRaises(S.ErroreSistemi):
                S.dati(ID, cap)

    def test_il_plugin_finto_porta_solo_dati_e_il_suo_codice(self):
        file = sorted(str(p.relative_to(FINTO)) for p in FINTO.rglob("*")
                      if p.is_file() and "__pycache__" not in p.parts)
        self.assertEqual(file, ["codice/dadi.py", "codice/incontri.py", "dati/abilita.toml",
                                "dati/formule.toml", "dati/incontri.toml",
                                "dati/termini-vietati.toml", "sistema.toml"])


if __name__ == "__main__":
    unittest.main()
