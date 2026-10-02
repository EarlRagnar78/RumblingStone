"""La lettura a scene: il lettore non guarda avanti perche' non puo', non perche' promette.

L1 di PIANO-AGENT-SKILLS-ESTERNE. Ogni test fissa una delle promesse del
meccanismo dal lato che morde: il testo del master non tocca il disco, la scena
dopo non arriva senza diario ne' prima del tempo, e alla chiusura si scrivono
impronte, non testo.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "lettura_a_scene.py"


def _modulo():
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location("lettura_a_scene", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


LS = _modulo()

FRASE_SEGRETA = "Il traditore e' il fabbro con la mano bruciata"
MASTER = f"""# Modulo di prova

Premessa per il DM.

### SCENA 1 — La porta

> *La porta e' socchiusa.*

Qui succede poco.

### SCENA 2 — La forgia

{FRASE_SEGRETA}.

## Appendice

Tabelle.
"""
DIARIO = "ago=+1 | mi aspettavo: una porta | ho trovato: una porta | so adesso: niente di nuovo"


class TestPassaggi(unittest.TestCase):
    def test_premessa_scene_e_coda_ricompongono_il_file(self):
        p = LS.passaggi(MASTER)
        self.assertEqual("".join(t for _, t in p), MASTER)
        self.assertEqual([t for t, _ in p][:2], ["premessa", "SCENA 1 — La porta"])

    def test_i_master_veri_si_ricompongono(self):
        for f in sorted((ROOT / "07_il Portale Della Forgia Eterna").glob("ARC07-DEF-*.md")):
            testo = f.read_text(encoding="utf-8")
            p = LS.passaggi(testo, LS.profilo_di(f.relative_to(ROOT).as_posix()))
            self.assertEqual("".join(t for _, t in p), testo, f.name)
            self.assertGreater(sum(1 for t, _ in p if t.startswith("SCENA")), 0, f.name)


class TestDiario(unittest.TestCase):
    def test_il_diario_completo_passa(self):
        self.assertIsNone(LS.controlla_diario(DIARIO))

    def test_senza_ago_o_fuori_scala_e_rifiutato(self):
        self.assertIn("ago", LS.controlla_diario(DIARIO.replace("ago=+1", "senza ago")))
        self.assertIn("ago", LS.controlla_diario(DIARIO.replace("ago=+1", "ago=+5")))

    def test_senza_so_adesso_e_rifiutato(self):
        """Il campo che rende visibile L-ORDINE non si salta."""
        motivo = LS.controlla_diario(DIARIO.replace("so adesso", "e poi"))
        self.assertIn("so adesso", motivo)


class TestLettura(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.master = base / "MODULO.md"
        self.master.write_text(MASTER, encoding="utf-8")
        self.corsa = base / "corsa"

    def tearDown(self):
        self.tmp.cleanup()

    def _testo_su_disco(self) -> str:
        return "".join(p.read_text(encoding="utf-8") for p in self.corsa.rglob("*") if p.is_file())

    def test_la_scena_dopo_non_arriva_prima_del_tempo(self):
        lt = LS.Lettura(self.master, self.corsa, ["lettore"], {}, tempo_per_parola=10.0)
        r = next(iter(lt.lettori.values()))
        lt.inizia(r)
        esito = lt.avanti(r, DIARIO)
        self.assertIn("troppo presto", esito["rifiutato"])
        self.assertEqual(r["cursore"], 0)

    def test_il_testo_non_tocca_il_disco_nemmeno_alla_chiusura(self):
        lt = LS.Lettura(self.master, self.corsa, ["lettore"], {}, tempo_per_parola=0)
        r = next(iter(lt.lettori.values()))
        lt.inizia(r)
        while not r["finito"]:
            lt.avanti(r, DIARIO)
        self.assertTrue(lt.chiusa)
        self.assertNotIn(FRASE_SEGRETA, self._testo_su_disco())
        stato = json.loads((self.corsa / "lettore" / "stato.json").read_text(encoding="utf-8"))
        self.assertEqual(len(stato["passaggi"]), len(LS.passaggi(MASTER)))
        self.assertTrue(all(len(p["impronta"]) == 64 for p in stato["passaggi"]))

    def test_smettere_e_un_rilievo_e_chiude(self):
        lt = LS.Lettura(self.master, self.corsa, ["lettore"], {}, tempo_per_parola=0)
        r = next(iter(lt.lettori.values()))
        lt.inizia(r)
        self.assertIn("Fermato al passaggio 1", lt.smetti(r, DIARIO)["fine"])
        self.assertTrue(lt.chiusa)

    def test_il_lettore_lavora_solo_con_l_indirizzo(self):
        """Il giro vero: server su 127.0.0.1, lettore da riga di comando."""
        lt = LS.Lettura(self.master, self.corsa, ["lettore"], {}, tempo_per_parola=0)
        server, base = LS.avvia_server(lt)
        filo = threading.Thread(target=server.serve_forever, daemon=True)
        filo.start()
        try:
            gettone = next(iter(lt.lettori))
            env = dict(os.environ, READER_FEED=f"{base}/{gettone}")
            primo = subprocess.run([sys.executable, str(SCRIPT), "inizia"], env=env,
                                   capture_output=True, text=True, check=False)
            self.assertIn("PASSAGGIO 1/", primo.stdout)
            self.assertNotIn(FRASE_SEGRETA, primo.stdout)
            rifiuto = subprocess.run([sys.executable, str(SCRIPT), "avanti", "--diario", "troppo corto"],
                                     env=env, capture_output=True, text=True, check=False)
            self.assertEqual(rifiuto.returncode, 1)
            self.assertIn("RIFIUTATO", rifiuto.stdout)
        finally:
            server.shutdown()


if __name__ == "__main__":
    unittest.main()
