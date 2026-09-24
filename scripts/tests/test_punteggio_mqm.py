"""Il punteggio MQM, provato all'indietro per ogni severita'.

Il criterio di F3.1 del piano: **il cancello morde per ogni severita'**, e
F3.2: **nessun documento buono viene bocciato** alla soglia iniziale. Se alla
soglia iniziale cade un master, la soglia e' sbagliata, non il documento.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import punteggio_mqm as pm  # noqa: E402


class TestSpecifiche(unittest.TestCase):

    def setUp(self) -> None:
        self.spec = pm.carica_specifiche()

    def test_ogni_norma_nomina_una_severita_che_esiste(self):
        for chiave, n in self.spec["norme"].items():
            self.assertIn(n["severita"], self.spec["severita"],
                          f"{chiave}: severita' '{n['severita']}' non definita")

    def test_ogni_norma_nomina_un_rilevatore_che_esiste(self):
        """ADR-0053 applicata alle specifiche: un rimando inventato e' un difetto."""
        for chiave, n in self.spec["norme"].items():
            modulo, funzione = n["rilevatore"].split(".")
            m = __import__(modulo)
            self.assertTrue(hasattr(m, funzione),
                            f"{chiave}: {n['rilevatore']} non esiste")

    def test_i_pesi_sono_quelli_canonici_mqm(self):
        self.assertEqual(self.spec["severita"]["minore"]["peso"], 1)
        self.assertEqual(self.spec["severita"]["maggiore"]["peso"], 5)
        self.assertEqual(self.spec["severita"]["critico"]["peso"], 25)

    def test_solo_il_critico_e_pass_fail(self):
        self.assertTrue(self.spec["severita"]["critico"]["pass_fail"])
        self.assertFalse(self.spec["severita"]["maggiore"]["pass_fail"])
        self.assertFalse(self.spec["severita"]["minore"]["pass_fail"])

    def test_ogni_classe_ha_una_soglia(self):
        for classe in self.spec["classi"]:
            self.assertIn(classe, self.spec["soglie"],
                          f"la classe '{classe}' non ha una soglia: non e' bocciabile")


class TestIlCancelloMorde(unittest.TestCase):
    """F3.1 — un errore iniettato deve far scendere il punteggio del suo peso."""

    def setUp(self) -> None:
        self.spec = pm.carica_specifiche()
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def scrivi(self, corpo: str) -> Path:
        f = self.dir / "prova.md"
        f.write_text(corpo, encoding="utf-8")
        return f

    def test_un_documento_pulito_vale_cento(self):
        f = self.scrivi("# Titolo\n\n> *Una riga di prosa breve e a norma.*\n\nTesto.\n")
        self.assertEqual(pm.valuta(f, self.spec)["punteggio"], 100.0)

    def test_un_maggiore_pesa_cinque_volte_un_minore(self):
        """Il box oltre le 12 righe e' maggiore; la parentesi e' minore."""
        breve = "# T\n\n> *Box (con parentesi) corto.*\n"
        lungo = "# T\n\n> *Apertura.*\n" + "".join(f"> riga {i}\n" for i in range(14))
        p_min = pm.valuta(self.scrivi(breve), self.spec)
        p_mag = pm.valuta(self.scrivi(lungo), self.spec)
        self.assertEqual(p_min["penalita"], 1, p_min["dettaglio"])
        self.assertEqual(p_mag["penalita"], 5, p_mag["dettaglio"])

    def test_la_caratteristica_minuscola_entra_nel_punteggio(self):
        f = self.scrivi("# T\n\nIl nano tenta una prova di forza, CD 18.\n")
        e = pm.valuta(f, self.spec)
        self.assertEqual(e["penalita"], 1)
        self.assertEqual(e["dettaglio"][0]["norma"], "caratteristica_minuscola")

    def test_il_critico_e_pass_fail_anche_a_punteggio_alto(self):
        """Il meccanismo, provato su una specifica di prova: oggi nessun
        rilevatore produce critici, ma la regola deve reggere quando esisteranno."""
        spec = pm.carica_specifiche()
        spec["norme"]["box_con_parentesi"]["severita"] = "critico"
        # 1.200 righe: la penalita' di 25 diluita vale ~2 punti, quindi il
        # punteggio resta sopra ogni soglia. E' esattamente il caso che il
        # pass/fail assoluto esiste per prendere.
        f = self.scrivi("# T\n\n> *Box (con parentesi) corto.*\n\n"
                        + "riga\n" * 1200)
        e = pm.valuta(f, spec)
        soglia_piu_alta = max(
            s["punteggio_minimo"] for s in spec["soglie"].values()
            if s.get("punteggio_minimo") is not None)
        self.assertGreater(e["punteggio"], soglia_piu_alta,
                           "il punteggio deve restare SOPRA ogni soglia: e' il punto")
        self.assertEqual(e["critici"], 1)
        ok, perche = pm.promosso(e, spec)
        self.assertFalse(ok, "un critico deve bocciare anche a punteggio alto")
        self.assertIn("critico", perche)

    def test_rimosso_l_errore_torna_verde(self):
        f = self.scrivi("# T\n\n> *Box (con parentesi) corto.*\n")
        self.assertLess(pm.valuta(f, self.spec)["punteggio"], 100.0)
        f.write_text("# T\n\n> *Box senza incisi, corto.*\n", encoding="utf-8")
        self.assertEqual(pm.valuta(f, self.spec)["punteggio"], 100.0)


class TestSulRepoVero(unittest.TestCase):

    def test_f3_2_nessun_documento_buono_bocciato(self):
        """Alla soglia iniziale il cancello nasce verde: e' la regola di taratura."""
        r = subprocess.run([sys.executable, "scripts/punteggio_mqm.py", "--soglia"],
                           capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_ogni_documento_ha_una_classe(self):
        """Un documento «fuori classe» non ha soglia, quindi non e' bocciabile mai.

        🔴 Al primo giro erano **294 su 515**, per un `Path.match` che confronta
        solo la coda del percorso. Il repo sembrava pulito e non lo era.
        """
        spec = pm.carica_specifiche()
        senza = [str(f.relative_to(ROOT)) for f in pm.bersagli(spec, [])
                 if f.suffix == ".md" and pm.classe_di(f, spec) is None]
        self.assertEqual(senza[:10], [], f"{len(senza)} documenti senza classe")

    def test_la_distribuzione_si_stampa(self):
        """F1.4 deve restare eseguibile: e' da li' che nascono le soglie."""
        r = subprocess.run([sys.executable, "scripts/punteggio_mqm.py", "--distribuzione"],
                           capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("master_def", r.stdout)
        self.assertIn("P25", r.stdout)

    def test_le_soglie_scritte_non_sono_sopra_il_minimo_misurato(self):
        """La regola di taratura, verificata invece che promessa.

        Una soglia sopra il minimo della classe **butta via** qualcosa, che e'
        esattamente cio' che il DM ha chiesto di non fare.
        """
        spec = pm.carica_specifiche()
        per_classe: "dict[str, list[float]]" = {}
        for f in pm.bersagli(spec, []):
            if f.suffix != ".md":
                continue
            e = pm.valuta(f, spec)
            per_classe.setdefault(e["classe"], []).append(e["punteggio"])
        for classe, valori in per_classe.items():
            minimo = spec["soglie"][classe].get("punteggio_minimo")
            if minimo is None:
                continue
            self.assertLessEqual(
                minimo, min(valori),
                f"la soglia di '{classe}' ({minimo}) e' sopra il minimo misurato "
                f"({min(valori)}): butterebbe via un documento esistente")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
