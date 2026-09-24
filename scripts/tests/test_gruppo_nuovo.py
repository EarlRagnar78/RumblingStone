"""`dm.py gruppo nuovo`: il gruppo nuovo da un comando e un modulo (lotto 4f-4).

Le decisioni del DM (D19, D21, 2026-09-24) sono il contratto di questi test:

* nessun YAML a mano: il DM risponde a domande, lo script scrive;
* il template e' DERIVATO dallo stato di oggi, non uno scheletro vuoto;
* cio' che e' partita per definizione si toglie da solo (le conoscenze sul
  party, i portatori degli artefatti, le note d'arco giocate, echi);
* cio' che richiede giudizio arriva UNA RIGA ALLA VOLTA, con tre scelte:
  tieni, svuota, segna da rivedere;
* gli artefatti restano nel prodotto, senza portatore (D21.3);
* arco e livello di partenza si scelgono (D21.4); ogni PG ha nome, razza,
  classe, livello e PF, al massimo sei (D21.5);
* i clock numerici ripartono da zero, i trigger restano (D21.6).

Si deriva dallo `state.yaml` VERO: un fixture scritto per passare proverebbe il
fixture (stessa scelta di `test_new_group.py`).
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import yaml  # noqa: E402

import validate_state  # noqa: E402
sys.path.insert(0, str(ROOT / "scripts" / "tests"))  # per `_copia` di test_new_group
from dmcore import gruppo_nuovo as G  # noqa: E402

STATO = yaml.safe_load((ROOT / "campaign" / "state.yaml").read_text(encoding="utf-8"))
PG_DEL_PRIMO = [p["pg"].split()[0] for p in STATO["party"]]

RISPOSTE_MINIME = {
    "gruppo": "beta",
    "arco_partenza": STATO["archi"][0]["arco"],
    "livello": 5,
    "pg": [{"nome": "Brunna", "razza": "Nana", "classe": "Guerriera",
            "livello": 5, "pf": 48}],
    "righe": {},
}


def _nuovo(risposte: "dict | None" = None) -> "tuple[dict, list]":
    base, domande = G.deriva(copy.deepcopy(STATO))
    r = copy.deepcopy(RISPOSTE_MINIME)
    r.update(risposte or {})
    return G.completa(base, domande, r), domande


class TestDerivazione(unittest.TestCase):
    def test_le_domande_una_alla_volta_sono_quelle_misurate(self):
        """Misurate il 2026-09-24: 5 villain, 4 difensori, 1 waypoint.

        «party» nelle agende NON conta: «Profile party's artifacts» vale per
        qualunque gruppo. Nelle conoscenze si', ma quelle si tolgono da sole.
        """
        _, domande = G.deriva(copy.deepcopy(STATO))
        per_sezione = {}
        for d in domande:
            per_sezione[d.sezione] = per_sezione.get(d.sezione, 0) + 1
        self.assertEqual(per_sezione, {"villain": 5, "difensori_rethmar": 4, "waypoints": 1})

    def test_ogni_domanda_ha_tre_scelte_e_mostra_il_testo(self):
        _, domande = G.deriva(copy.deepcopy(STATO))
        for d in domande:
            self.assertEqual(d.scelte, ("tieni", "svuota", "rivedi"))
            self.assertTrue(d.campi)
            self.assertTrue(all(d.testo[c] for c in d.campi))

    def test_le_conoscenze_sul_party_si_tolgono_da_sole(self):
        nuovo, _ = _nuovo()
        self.assertEqual(len(nuovo["conoscenze"]), 12)
        for r in nuovo["conoscenze"]:
            testo = f"{r['sa_che']} {r.get('come') or ''}"
            self.assertFalse(any(n in testo for n in PG_DEL_PRIMO), testo)
            self.assertNotRegex(testo.lower(), r"\bparty\b")

    def test_gli_artefatti_restano_senza_portatore(self):
        """D21.3: restano nel prodotto."""
        nuovo, _ = _nuovo()
        self.assertEqual([a["artefatto"] for a in nuovo["artefatti"]],
                         [a["artefatto"] for a in STATO["artefatti"]])
        for a in nuovo["artefatti"]:
            self.assertEqual(a["portatore"], "—")
            self.assertFalse(any(n in a["oggi"] for n in PG_DEL_PRIMO))

    def test_i_clock_numerici_ripartono_da_zero_e_i_trigger_restano(self):
        nuovo, _ = _nuovo()
        prima = {v["png_id"]: v for v in STATO["villain"]}
        for v in nuovo["villain"]:
            vecchio = prima[v["png_id"]]["clock"]
            if G.CLOCK_NUMERICO.match(str(vecchio)):
                self.assertRegex(v["clock"], r"^0/\d+$")
                self.assertEqual(v["clock"].split("/")[1],
                                 G.CLOCK_NUMERICO.match(vecchio).group(2))
            else:
                self.assertEqual(v["clock"], vecchio, "un trigger non e' un numero")
            self.assertEqual(v["stato"], "attivo")
            self.assertEqual(v["tempo"], "preparato")

    def test_la_partita_si_svuota(self):
        nuovo, _ = _nuovo()
        self.assertEqual(nuovo["echi"], [])
        self.assertEqual(nuovo["march_clock"]["giorno_corrente"], 1)
        for w in nuovo["march_clock"]["waypoints"]:
            self.assertNotIn("✅", w["stato"])
            self.assertNotIn("SYNC POINT", w["stato"])
        for a in nuovo["archi"]:
            self.assertFalse(a.get("note") and any(n in a["note"] for n in PG_DEL_PRIMO))

    def test_il_prodotto_resta(self):
        nuovo, _ = _nuovo()
        self.assertEqual(nuovo["png"], STATO["png"])
        self.assertEqual(nuovo["scenari_rethmar"], STATO["scenari_rethmar"])
        self.assertEqual(len(nuovo["villain"]), len(STATO["villain"]))
        self.assertEqual(len(nuovo["archi"]), len(STATO["archi"]))


class TestRisposte(unittest.TestCase):
    def test_l_arco_scelto_e_in_corso_e_i_precedenti_non_giocati(self):
        """D21.4."""
        scelto = STATO["archi"][7]["arco"]
        nuovo, _ = _nuovo({"arco_partenza": scelto, "livello": 13})
        tempi = [a["tempo"] for a in nuovo["archi"]]
        self.assertEqual(tempi[7], "in_corso")
        self.assertEqual(nuovo["archi"][7]["pg_livello"], "13")
        self.assertTrue(all(t == "preparato" for i, t in enumerate(tempi) if i != 7))
        self.assertTrue(all(a["stato"] == G.NON_GIOCATO for a in nuovo["archi"][:7]))
        self.assertTrue(all(a["stato"] == "da giocare" for a in nuovo["archi"][8:]))

    def test_i_pg_diventano_il_party(self):
        nuovo, _ = _nuovo()
        (pg,) = nuovo["party"]
        self.assertEqual(pg["pg"], "Brunna")
        self.assertEqual(pg["classe"], "Guerriera 5 (Nana)")
        self.assertEqual(pg["hp"], "48")
        self.assertEqual(pg["stato"], "attivo")

    def test_tieni_svuota_rivedi(self):
        _, domande = G.deriva(copy.deepcopy(STATO))
        tieni, svuota, rivedi = domande[0], domande[1], domande[2]
        righe = {d.id: "tieni" for d in domande}
        righe.update({svuota.id: "svuota", rivedi.id: "rivedi"})
        nuovo, _ = _nuovo({"righe": righe})

        def riga(d):
            return G.trova(nuovo, d)

        for c in tieni.campi:
            self.assertEqual(riga(tieni)[c], tieni.testo[c])
        for c in svuota.campi:
            self.assertEqual(riga(svuota)[c], G.SEGNAPOSTO)
        for c in rivedi.campi:
            self.assertEqual(riga(rivedi)[c], rivedi.testo[c])
        (inf,) = nuovo["inferred"]
        self.assertEqual(inf["id"], "INF-001")
        self.assertEqual(inf["dove"], f"{rivedi.sezione}[{rivedi.indice}].{rivedi.campi[0]}")
        self.assertEqual(inf["a_chi"], "DM")

    def test_una_domanda_senza_risposta_vale_rivedi(self):
        """Il default prudente: niente passa in silenzio, niente si cancella in silenzio."""
        nuovo, domande = _nuovo()
        self.assertEqual(len(nuovo["inferred"]), len(domande))

    def test_lo_stato_nuovo_passa_validate_state(self):
        nuovo, _ = _nuovo()
        self.assertEqual(validate_state.errori(nuovo, ROOT), [])

    def test_risposte_sbagliate_sono_rifiutate_prima_di_scrivere(self):
        base, domande = G.deriva(copy.deepcopy(STATO))
        casi = [
            {"pg": []},
            {"pg": [RISPOSTE_MINIME["pg"][0]] * 7},
            {"livello": 0},
            {"arco_partenza": "99 Non Esiste"},
            {"gruppo": "Nome Con Spazi!"},
            {"righe": {domande[0].id: "forse"}},
            {"righe": {"villain:non-esiste": "tieni"}},
            {"pg": [{"nome": "X", "razza": "Nano", "classe": "Guerriero",
                     "livello": 5, "pf": 0}]},
        ]
        for caso in casi:
            r = copy.deepcopy(RISPOSTE_MINIME)
            r.update(caso)
            with self.subTest(caso=list(caso)):
                with self.assertRaises(G.RispostaNonValida):
                    G.completa(copy.deepcopy(base), domande, r)


class TestContrattoPerLInterfaccia(unittest.TestCase):
    """Il modulo in terminale oggi, una pagina domani: il contratto e' il JSON."""

    def test_le_domande_escono_in_json_e_ritornano_in_json(self):
        esito = subprocess.run([sys.executable, "scripts/gruppo_nuovo.py", "--domande"],
                               cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(esito.returncode, 0, esito.stderr)
        dati = json.loads(esito.stdout)
        self.assertEqual({d["sezione"] for d in dati["righe"]},
                         {"villain", "difensori_rethmar", "waypoints"})
        self.assertIn("arco_partenza", dati["campi"])
        self.assertEqual(dati["campi"]["pg"]["massimo"], 6)
        self.assertEqual(dati["campi"]["arco_partenza"]["scelte"][0], STATO["archi"][0]["arco"])

    def test_attraverso_dm_py_stdout_resta_json(self):
        """Un'interfaccia chiamera' `dm.py`, non lo script: la riga del tramite
        «[dm] → …» non deve finire nei dati."""
        esito = subprocess.run([sys.executable, "scripts/dm.py", "gruppo", "nuovo", "--domande"],
                               cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(esito.returncode, 0, esito.stderr)
        self.assertIn("righe", json.loads(esito.stdout))


def _repo_di_prova(radice: Path) -> None:
    """Una copia del repo sotto git. `.gitignore` come FILE: git non segue un
    `.gitignore` simbolico, e i `__pycache__` renderebbero sporco l'albero."""
    import shutil
    from test_new_group import _copia  # noqa: PLC0415
    _copia(radice)
    (radice / ".gitignore").unlink()
    shutil.copy(ROOT / ".gitignore", radice / ".gitignore")
    for cmd in (["init", "-q", "-b", "main"], ["config", "user.email", "t@t"],
                ["config", "user.name", "t"], ["add", "-A"], ["commit", "-q", "-m", "base"]):
        subprocess.run(["git", *cmd], cwd=radice, check=True, capture_output=True)


class TestIlModuloInTerminale(unittest.TestCase):
    """Il percorso del DM: domande una dopo l'altra, invio per accettare il predefinito."""

    def test_il_modulo_produce_le_risposte(self):
        _, domande = G.deriva(copy.deepcopy(STATO))
        righe = ["gamma", "1", "", "1", "Kael", "Umano", "Mago", "", "20"]
        righe += ["1"] * (len(domande) - 1) + [""]  # l'ultima col predefinito: rivedi
        esito = subprocess.run(
            [sys.executable, "scripts/gruppo_nuovo.py", "--dry-run"], cwd=ROOT,
            input="\n".join(righe) + "\n", capture_output=True, text=True)
        self.assertEqual(esito.returncode, 0, esito.stdout[-800:] + esito.stderr)
        self.assertIn("ramo campaign-group-gamma · 1 PG", esito.stdout)
        self.assertIn(f"righe: {len(domande) - 1} tenute, 0 svuotate, 1 da rivedere",
                      esito.stdout)
        self.assertIn("dry-run: niente scritto", esito.stdout)

    def test_ctrl_d_a_meta_non_scrive_niente(self):
        esito = subprocess.run([sys.executable, "scripts/gruppo_nuovo.py", "--dry-run"],
                               cwd=ROOT, input="delta\n1\n", capture_output=True, text=True)
        self.assertEqual(esito.returncode, 1)
        self.assertIn("niente scritto", esito.stdout)


class TestDaCapoAFondo(unittest.TestCase):
    """Il comando vero su una copia del repo: ramo, reset, stato, commit."""

    def test_un_gruppo_nuovo_da_un_file_di_risposte(self):
        with tempfile.TemporaryDirectory() as tmp:
            radice = Path(tmp)
            _repo_di_prova(radice)
            risposte = Path(tempfile.mkdtemp()) / "risposte.json"  # fuori dal repo
            risposte.write_text(json.dumps(RISPOSTE_MINIME), encoding="utf-8")
            esito = subprocess.run(
                [sys.executable, "scripts/gruppo_nuovo.py", "--answers", str(risposte),
                 "--repo-root", str(radice)],
                cwd=radice, capture_output=True, text=True)
            self.assertEqual(esito.returncode, 0, esito.stdout + esito.stderr)

            ramo = subprocess.run(["git", "branch", "--show-current"], cwd=radice,
                                  capture_output=True, text=True).stdout.strip()
            self.assertEqual(ramo, "campaign-group-beta")
            pulito = subprocess.run(["git", "status", "--porcelain", "--", "campaign"],
                                    cwd=radice, capture_output=True, text=True).stdout
            self.assertEqual(pulito, "", "il reset e' committato tutto")
            stato = yaml.safe_load((radice / "campaign" / "state.yaml").read_text(encoding="utf-8"))
            self.assertEqual([p["pg"] for p in stato["party"]], ["Brunna"])
            self.assertIn("group: beta", (radice / "campaign" / "group.yaml").read_text(encoding="utf-8"))
            check = subprocess.run([sys.executable, "scripts/render_state.py", "--check"],
                                   cwd=radice, capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_con_l_albero_sporco_non_parte(self):
        with tempfile.TemporaryDirectory() as tmp:
            radice = Path(tmp)
            _repo_di_prova(radice)
            (radice / "campaign" / "sporco.md").write_text("x\n", encoding="utf-8")
            risposte = Path(tempfile.mkdtemp()) / "r.json"
            risposte.write_text(json.dumps(RISPOSTE_MINIME), encoding="utf-8")
            esito = subprocess.run(
                [sys.executable, "scripts/gruppo_nuovo.py", "--answers", str(risposte),
                 "--repo-root", str(radice)],
                cwd=radice, capture_output=True, text=True)
            self.assertEqual(esito.returncode, 1)
            ramo = subprocess.run(["git", "branch", "--show-current"], cwd=radice,
                                  capture_output=True, text=True).stdout.strip()
            self.assertEqual(ramo, "main", "niente ramo nuovo se non si parte")


if __name__ == "__main__":
    unittest.main()
