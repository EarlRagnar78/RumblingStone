"""I sistemi di gioco come plugin di dati (ADR-0111): caricatore e cancello.

I difetti che questi test esistono per impedire:

- un modulo PF1e letto come 3.5 perché il rilevamento sbaglia il percorso;
- una capacità presa da un altro sistema senza che nessuno l'abbia scritto
  (l'eredità implicita è il modo in cui il Giardino PF1e è finito trattato
  come 3.5 dove si escludeva solo il Drappo);
- un plugin che punta a una tabella che nel codice non c'è più;
- uno strumento che chiede una capacità che un sistema attivo non dichiara.

I casi costruiti scrivono in cartelle temporanee, mai nel repo vero.
Solo `unittest`.
"""
from __future__ import annotations

import io
import subprocess
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import sistemi as CLI  # noqa: E402
from dmcore import sistemi as S  # noqa: E402

CATALOGO = """
[capacita]
"pe.soglie" = "soglie"
"termini.vietati" = "vietati"
"""

CONFIG = """
[progetto]
predefinito = "alfa"
attivi = ["alfa", "beta"]
rinforzo = ["alfa"]

[moduli]
"moduli/beta" = "beta"
"moduli/beta/eccezione" = "alfa"
"""

FAMIGLIA = """
id = "fam"
nome = "Famiglia"
tipo = "famiglia"
licenza = "OGL"
fonti = []
skill = ["skill-fam"]
[capacita]
"termini.vietati" = { dati = ["dati/vietati.txt"] }
"""

ALFA = """
id = "alfa"
nome = "Alfa"
tipo = "sistema"
famiglia = "fam"
licenza = "OGL"
fonti = []
skill = ["skill-alfa"]
[capacita]
"termini.vietati" = { eredita = "fam", motivo = "comuni" }
"pe.soglie" = { codice = ["codice.py:SOGLIE"], lotto = "L4" }
"""

BETA = """
id = "beta"
nome = "Beta"
tipo = "sistema"
famiglia = "fam"
licenza = "OGL"
fonti = []
skill = ["skill-beta"]
[capacita]
"termini.vietati" = { eredita = "alfa", motivo = "come alfa" }
"pe.soglie" = { non_supportato = "solo alfa ha le soglie" }
"""


class Albero:
    """Un repo finto in una cartella temporanea."""

    def __init__(self, **sostituzioni: str):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        file = {
            "sistemi.toml": CONFIG,
            "sistemi/catalogo.toml": CATALOGO,
            "sistemi/fam/sistema.toml": FAMIGLIA,
            "sistemi/alfa/sistema.toml": ALFA,
            "sistemi/beta/sistema.toml": BETA,
            "dati/vietati.txt": "vantaggio\n",
            "codice.py": "SOGLIE = {1: 0}\n",
            "moduli/beta/eccezione/x.md": "",
            "skills/skill-fam/SKILL.md": "",
            "skills/skill-alfa/SKILL.md": "",
            "skills/skill-beta/SKILL.md": "",
            "scripts/tools.manifest.json": '{"tools": [{"id": "xp", "sistema": {"capacita": ["pe.soglie"]}}]}',
        }
        file.update(sostituzioni)
        for rel, testo in file.items():
            if testo is None:
                continue
            f = self.root / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(textwrap.dedent(testo), encoding="utf-8")
        S._carica.cache_clear()

    def __enter__(self):
        return self.root

    def __exit__(self, *_):
        S._carica.cache_clear()
        self._tmp.cleanup()


class TestSkillEscluse(unittest.TestCase):
    """L6: build-skills.sh e sync-skills.sh saltano le skill dei sistemi spenti."""

    def test_tutti_accesi_nessuna_esclusa(self):
        with Albero() as r:
            self.assertEqual(S.skill_escluse(r), [])

    def test_sistema_spento_le_sue_skill_escono(self):
        cfg = CONFIG.replace('attivi = ["alfa", "beta"]', 'attivi = ["alfa"]')
        self.assertNotEqual(cfg, CONFIG)
        with Albero(**{"sistemi.toml": cfg}) as r:
            self.assertEqual(S.skill_escluse(r), ["skill-beta"])
            self.assertNotIn("skill-beta", S.skill_da_installare(r))

    def test_il_rinforzo_basta_a_tenerla(self):
        cfg = CONFIG.replace('attivi = ["alfa", "beta"]', 'attivi = ["alfa"]').replace(
            'rinforzo = ["alfa"]', 'rinforzo = ["beta"]')
        with Albero(**{"sistemi.toml": cfg}) as r:
            self.assertEqual(S.skill_escluse(r), [])

    def test_repo_vero_installa_tutto(self):
        self.assertEqual(S.skill_escluse(REPO), [])

    def test_gli_script_chiedono_a_sistemi(self):
        for f in ("build-skills.sh", "sync-skills.sh"):
            self.assertIn("sistemi.py\" --skill-escluse", (REPO / "scripts" / f).read_text(encoding="utf-8"), f)


class TestRepoVero(unittest.TestCase):
    def test_il_cancello_e_verde(self):
        self.assertEqual(S.problemi(REPO, CLI.strumenti(REPO)), [])

    def test_i_moduli_pf1e_sono_pf1e(self):
        self.assertEqual(S.sistema_di("10-stand-alone/Il-Drappo-di-Tarsilia/01-GIORNO.md", REPO), "pf1e")
        self.assertEqual(S.sistema_di("10-stand-alone/Il Giardino di Sale e Calce PF1e/x.md", REPO), "pf1e")

    def test_il_giardino_3_5_resta_3_5(self):
        # «Il Giardino di Sale e Calce» e «… PF1e» hanno lo stesso inizio: il
        # confronto è per cartelle intere, non per prefisso di stringa.
        self.assertEqual(S.sistema_di("10-stand-alone/Il Giardino di Sale e Calce/x.md", REPO), "dnd35")

    def test_il_resto_e_il_predefinito(self):
        self.assertEqual(S.sistema_di("07_il Portale Della Forgia Eterna/ARC07-DEF-4.md", REPO), "dnd35")

    def test_pathfinder_si_installa_anche_come_rinforzo(self):
        self.assertIn("pathfinder-1e-srd", S.skill_da_installare(REPO))

    def test_ogni_strumento_dichiarato_esiste_nel_manifest(self):
        st = CLI.strumenti(REPO)
        self.assertIn("update_xp", st)
        self.assertIn("pe.soglie", st["update_xp"])


class TestAmbientazioni(unittest.TestCase):
    """D4 di ADR-0111: il mondo è un asse diverso dal sistema."""

    def test_il_drappo_e_golarion_e_il_giardino_pf1e_nessuna(self):
        self.assertEqual(S.ambientazione_di("10-stand-alone/Il-Drappo-di-Tarsilia/01.md", REPO), "golarion")
        self.assertEqual(S.ambientazione_di("10-stand-alone/Il Giardino di Sale e Calce PF1e/x.md", REPO), "nessuna")

    def test_la_campagna_e_i_reami(self):
        self.assertEqual(S.ambientazione_di("campaign/state.md", REPO), "forgotten-realms")
        self.assertEqual(S.ambientazione_di("10-stand-alone/Il Giardino di Sale e Calce/x.md", REPO), "forgotten-realms")

    def test_ambientazione_sconosciuta_e_rossa(self):
        cfg = CONFIG + """
[ambientazioni]
predefinito = "mondo"
[ambientazioni.elenco]
mondo = { nome = "Mondo", skill = [] }
[ambientazioni.moduli]
"moduli/beta" = "altrove"
"""
        with Albero(**{"sistemi.toml": cfg}) as r:
            self.assertTrue(any("«altrove»" in p for p in S.problemi(r)))

    def test_senza_sezione_vale_nessuna(self):
        with Albero() as r:
            self.assertEqual(S.ambientazione_di("moduli/beta/x.md", r), "nessuna")
            self.assertEqual(S.problemi(r), [])


class TestRilevamento(unittest.TestCase):
    def test_vince_il_percorso_piu_lungo(self):
        with Albero() as r:
            self.assertEqual(S.sistema_di("moduli/beta/a.md", r), "beta")
            self.assertEqual(S.sistema_di("moduli/beta/eccezione/x.md", r), "alfa")
            self.assertEqual(S.sistema_di("altrove/x.md", r), "alfa")

    def test_percorso_assoluto(self):
        with Albero() as r:
            self.assertEqual(S.sistema_di(r / "moduli/beta/a.md", r), "beta")


class TestEredita(unittest.TestCase):
    def test_la_catena_arriva_ai_dati(self):
        with Albero() as r:
            c = S.capacita("beta", "termini.vietati", r)
            self.assertEqual((c.modo, c.da, c.catena), ("dati", "fam", ("beta", "alfa", "fam")))
            self.assertTrue(c.utilizzabile)

    def test_non_supportato_resta_non_supportato(self):
        with Albero() as r:
            c = S.capacita("beta", "pe.soglie", r)
            self.assertEqual(c.modo, "non_supportato")
            self.assertFalse(c.utilizzabile)

    def test_un_ciclo_e_un_errore(self):
        ciclo = ALFA.replace('{ eredita = "fam", motivo = "comuni" }', '{ eredita = "beta", motivo = "giro" }')
        with Albero(**{"sistemi/alfa/sistema.toml": ciclo}) as r:
            with self.assertRaises(S.ErroreSistemi):
                S.capacita("alfa", "termini.vietati", r)
            self.assertTrue(any("circolare" in p for p in S.problemi(r)))


class TestCancello(unittest.TestCase):
    def test_albero_pulito_e_verde(self):
        with Albero() as r:
            self.assertEqual(S.problemi(r, CLI.strumenti(r)), [])

    def test_capacita_chiesta_e_non_dichiarata(self):
        senza = BETA.replace('"pe.soglie" = { non_supportato = "solo alfa ha le soglie" }\n', "")
        with Albero(**{"sistemi/beta/sistema.toml": senza}) as r:
            prob = S.problemi(r, CLI.strumenti(r))
            self.assertTrue(any("«xp» chiede «pe.soglie», che «beta» non dichiara" in p for p in prob), prob)

    def test_tabella_sparita_dal_codice(self):
        with Albero(**{"codice.py": "ALTRO = 1\n"}) as r:
            self.assertTrue(any("«SOGLIE» non è definito" in p for p in S.problemi(r)))

    def test_eredita_senza_motivo(self):
        muto = BETA.replace(', motivo = "come alfa"', "")
        with Albero(**{"sistemi/beta/sistema.toml": muto}) as r:
            self.assertTrue(any("senza motivo" in p for p in S.problemi(r)))

    def test_predefinito_spento(self):
        spento = CONFIG.replace('attivi = ["alfa", "beta"]', 'attivi = ["beta"]')
        with Albero(**{"sistemi.toml": spento}) as r:
            self.assertTrue(any("predefinito" in p for p in S.problemi(r)))

    def test_capacita_fuori_catalogo(self):
        strana = BETA + '"magia.selvaggia" = { non_supportato = "no" }\n'
        with Albero(**{"sistemi/beta/sistema.toml": strana}) as r:
            self.assertTrue(any("non è nel catalogo" in p for p in S.problemi(r)))

    def test_skill_inesistente(self):
        with Albero(**{"skills/skill-beta/SKILL.md": None}) as r:
            self.assertTrue(any("skill-beta" in p for p in S.problemi(r)))

    def test_un_sistema_nuovo_della_famiglia_e_solo_dati(self):
        # La prova del nove in piccolo (L8): un sistema in più si aggiunge
        # con la sua cartella e una riga in sistemi.toml, senza codice.
        gamma = BETA.replace('id = "beta"', 'id = "gamma"').replace("skill-beta", "skill-alfa")
        config = CONFIG.replace('attivi = ["alfa", "beta"]', 'attivi = ["alfa", "beta", "gamma"]')
        with Albero(**{"sistemi/gamma/sistema.toml": gamma, "sistemi.toml": config}) as r:
            self.assertEqual(S.problemi(r, CLI.strumenti(r)), [])
            self.assertEqual(S.capacita("gamma", "termini.vietati", r).modo, "dati")


class TestRigaDiComando(unittest.TestCase):
    def _esegui(self, *argv: str, root: Path = REPO) -> "tuple[int, str]":
        out = io.StringIO()
        with redirect_stdout(out):
            codice = CLI.main([*argv, "--root", str(root)])
        return codice, out.getvalue()

    def test_check_verde_sul_repo(self):
        codice, out = self._esegui("--check")
        self.assertEqual(codice, 0, out)

    def test_check_rosso_esce_1(self):
        with Albero(**{"codice.py": "ALTRO = 1\n"}) as r:
            self.assertEqual(self._esegui("--check", root=r)[0], 1)

    def test_configurazione_illeggibile_esce_2(self):
        with Albero(**{"sistemi.toml": "[progetto\n"}) as r:
            self.assertEqual(self._esegui("--json", root=r)[0], 2)

    def test_di(self):
        self.assertEqual(self._esegui("--di", "10-stand-alone/Il-Drappo-di-Tarsilia/x.md")[1].strip(), "pf1e")

    def test_la_matrice_e_deterministica(self):
        a = subprocess.run([sys.executable, str(REPO / "scripts/sistemi.py"), "--json"],
                           capture_output=True, cwd=REPO).stdout
        b = subprocess.run([sys.executable, str(REPO / "scripts/sistemi.py"), "--json"],
                           capture_output=True, cwd=REPO).stdout
        self.assertEqual(a, b)
        self.assertIn(b'"matrice"', a)


if __name__ == "__main__":
    unittest.main()


class TestRigaSistema(unittest.TestCase):
    """L2: la riga «**Sistema:**» di un modulo e sistemi.toml dicono lo stesso
    sistema. Prima il Drappo era PF1e per sistemi.toml e 3.5 per e_pf1() in 19
    file su 22, e nessun controllo lo vedeva."""

    ALFA_R = ALFA.replace('skill = ["skill-alfa"]', 'riconosci = ["Alfa"]\nskill = ["skill-alfa"]')
    BETA_R = BETA.replace('skill = ["skill-beta"]', 'riconosci = ["Beta"]\nskill = ["skill-beta"]')

    def albero(self, **file):
        cfg = CONFIG.replace('"moduli/beta" = "beta"', '"moduli/beta" = "beta"\n"10-beta" = "beta"')
        return Albero(**{"sistemi.toml": cfg, "sistemi/alfa/sistema.toml": self.ALFA_R,
                         "sistemi/beta/sistema.toml": self.BETA_R, "10-beta/x.md": "", **file})

    def test_vince_il_nome_che_compare_prima(self):
        with self.albero() as r:
            self.assertEqual(S.sistema_dichiarato("**Sistema:** Alfa (con rinforzo Beta)", r), "alfa")
            self.assertEqual(S.sistema_dichiarato("- **Regole**: Beta, poi Alfa", r), "beta")
            self.assertIsNone(S.sistema_dichiarato("**Sistema di movimento:** a esagoni", r))
            self.assertIsNone(S.sistema_dichiarato("x" * S.TESTA + "\n**Sistema:** Beta", r))

    def test_divergenza_e_un_problema(self):
        with self.albero(**{"10-beta/m.md": "# M\n\n**Sistema:** Alfa\n", "05-alfa/ok.md": "**Sistema:** Alfa"}) as r:
            div = S.dichiarazioni_divergenti(r)
            self.assertEqual(div, [("10-beta/m.md", "alfa", "beta")])
            self.assertTrue(any("10-beta/m.md" in p and "Sistema" in p for p in S.problemi(r)))

    def test_homebrew_e_archivio_non_contano(self):
        with self.albero(**{"10-beta/homebrew/b.md": "**Sistema:** Alfa",
                            "10-beta/_ARCHIVIO/a.md": "**Sistema:** Alfa"}) as r:
            self.assertEqual(S.dichiarazioni_divergenti(r), [])

    def test_repo_vero_senza_divergenze(self):
        self.assertEqual(S.dichiarazioni_divergenti(REPO), [])
        drappo = "10-stand-alone/Il-Drappo-di-Tarsilia/REGOLE-DELLA-CORSA-PF1E.md"
        self.assertEqual(S.sistema_dichiarato((REPO / drappo).read_text(encoding="utf-8")), "pf1e")


class TestRilevamentoUnico(unittest.TestCase):
    """L2: catalogo dei mostri, censimento e domande del developer prendono il
    sistema da sistemi.toml. Il Giardino PF1e era nel catalogo dei mostri 3.5
    (proposto in 7 incontri su 120 a EL 17-18) e nel censimento del Bestiario."""

    def test_catalogo_salta_i_moduli_pf1e(self):
        import build_monster_catalog as B
        for rel in ("10-stand-alone/Il Giardino di Sale e Calce PF1e/appendice_creature.md",
                    "10-stand-alone/Il-Drappo-di-Tarsilia/STATBLOCCHI-PF1E.md"):
            self.assertTrue(B.should_skip(Path(rel)), rel)
        self.assertFalse(B.should_skip(Path("10-stand-alone/Il Giardino di Sale e Calce/appendice_creature.md")))

    def test_censimento_senza_moduli_pf1e(self):
        from dmcore import censimento as C
        docs = C.documenti_con_statistiche(REPO)
        self.assertFalse([d for d in docs if S.sistema_di(d) != "dnd35"])

    def test_domande_developer_non_accetta_il_sistema_nei_profili(self):
        import json
        cfg = json.loads((REPO / "plans/domande-developer.json").read_text(encoding="utf-8"))
        self.assertFalse([f for f, p in cfg["profili"].items() if "sistema" in p])


class TestEPf1(unittest.TestCase):
    """L2: lessico_regole.e_pf1() segue sistemi.toml. Prima diceva PF1e per 3
    file del Drappo su 22, e il controllo dei termini leggeva gli altri in 3.5."""

    def test_tutto_il_drappo_e_pf1e(self):
        import lessico_regole as LR
        file = sorted((REPO / "10-stand-alone/Il-Drappo-di-Tarsilia").glob("*.md"))
        self.assertGreater(len(file), 10)
        self.assertEqual([f.name for f in file if not LR.e_pf1(str(f.relative_to(REPO)), "")], [])

    def test_un_modulo_3_5_resta_3_5(self):
        import lessico_regole as LR
        self.assertFalse(LR.e_pf1("07_il Portale Della Forgia Eterna/x.md", "**Sistema:** D&D 3.5"))


class TestTerminiDalPlugin(unittest.TestCase):
    """L3: la lista dei termini 5e è una sola, nel plugin d20. Prima c'erano due
    copie con forme diverse: validate_modules non vedeva «azione bonus» né «con
    vantaggio», validate_standalone non vedeva «bonus action» né «lair action»."""

    def test_una_lista_per_i_due_validatori(self):
        import validate_modules as VM
        import validate_standalone as VS
        f = REPO / "10-stand-alone/x.md"
        self.assertEqual(VS.vietati(f), S.termini_vietati())
        self.assertEqual(VM.banditi(f)[: len(S.termini_vietati())], S.termini_vietati())
        self.assertEqual(VM.banditi(f)[len(S.termini_vietati()):], VM.CANONE_DEPRECATO)

    def test_le_forme_che_mancavano_a_ciascuno(self):
        regex = [r for r, _ in S.termini_vietati()]
        def preso(testo):
            import re
            return any(re.search(r, testo, re.I) for r in regex)
        for testo in ("con un'azione bonus colpisce", "attacca con vantaggio", "come bonus action",
                      "una lair action del drago", "DC 15", "dopo un riposo lungo"):
            self.assertTrue(preso(testo), testo)
        for testo in ("ottiene un vantaggio tattico", "CD 15", "un'azione di movimento"):
            self.assertFalse(preso(testo), testo)

    def test_pf1e_eredita_la_lista(self):
        self.assertEqual(S.termini_vietati("pf1e"), S.termini_vietati("dnd35"))


class TestLessicoDalPlugin(unittest.TestCase):
    """L3: abilità e entità lette dai dati dei plugin, non da costanti nel codice."""

    def test_abilita_3_5_invariate(self):
        import validate_prosa as VP
        vecchie = subprocess.run(["git", "show", "fe4ca17:scripts/validate_prosa.py"], cwd=REPO,
                                 capture_output=True, text=True).stdout
        if vecchie:
            import re
            m = re.search(r"^ABILITA = \(([^)]*)\)", vecchie, re.M)
            # le 31 di prima restano, nello stesso ordine; dal 2026-11-09 (audit
            # dei plugin) seguono le sette abilità SRD 3.5 che mancavano
            self.assertEqual(VP.ABILITA[:31], tuple(re.findall(r'"([^"]+)"', m.group(1))))
        self.assertEqual(len(VP.ABILITA), 38)
        self.assertIn("muoversi silenziosamente", VP.ABILITA)
        self.assertIn("osservare", VP.ABILITA)
        self.assertNotIn("percezione", VP.ABILITA)

    def test_abilita_pf1e_nei_moduli_pf1e(self):
        import validate_prosa as VP
        pf = S.abilita("pf1e")["nomi"]
        self.assertIn("percezione", pf)
        self.assertNotIn("osservare", pf)
        forme = dict((n, rx) for n, rx, _ in VP.forme_caratteristica("pf1e"))
        self.assertTrue(forme["F2 abilità col modificatore"].search("Percezione +12"))
        self.assertFalse(dict((n, rx) for n, rx, _ in VP.FORME_CARATTERISTICA)
                         ["F2 abilità col modificatore"].search("Percezione +12"))

    def test_abilita_estranee_per_sistema(self):
        import domande_developer as D
        self.assertIn("Percezione", D.ABILITA_ESTRANEE["3.5"])
        self.assertEqual(D.ABILITA_ESTRANEE["pf1e"], ("Atletica",))

    def test_entita_3_5_dai_dati(self):
        import coerenza_campagna as C
        e = S.dati("dnd35", "lessico.entita")
        self.assertEqual(C.CLASSI, set(e["classi"]))
        self.assertEqual(C.RAZZE, set(e["razze"]))
        self.assertIn("guerriero", C.CLASSI)


class TestScenaSocialePf1e(unittest.TestCase):
    """Il nome PF1e di Sense Motive fa una scena sociale come quello 3.5. Con il
    Drappo rinominato in «Intuizione» la D18 aveva smesso di vedere §3 «L'offerta»."""

    def test_intuizione_meccanica_conta(self):
        import domande_developer as D
        for testo in ("Intuizione CD 20: Vesca non mente", "lei ha Intuizione +12",
                      "Percepire Intenzioni CD 15"):
            self.assertTrue(D.SOCIALE.search(testo), testo)
        self.assertFalse(D.SOCIALE.search("ebbe un'Intuizione improvvisa"))
