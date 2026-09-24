"""La gerarchia delle skill e' un dato, e il gate la prova dai due lati.

Il DM il 2026-09-19: *«fai un ordine gerarchico delle skill che eviti di far
saltare le skill [...] verifica se ci sono skill che si sovrappongono e
orchestrale in maniera smart, con meccanismi davvero misurabili»*.

🔎 **La gerarchia esisteva gia', sparsa in cinque frasi di `AGENTS.md`** — «la
coerenza batte lo stile», «sopra `narrative-style`, che resta il fondo»,
«regole opposte», «le righe si sommano», «read-aloud ceilings winning any
conflict». Tutte corrette, **nessuna verificabile**, e `validate_skills.py`
presidiava l'instradamento (ADR-0041) ma non la precedenza: una skill nuova
poteva nascere senza che nessuno decidesse dove sta.

⚠️ **Cosa questo test NON prova.** Che lo strato sia quello *giusto*. Se
qualcuno mettesse `editoria` in LR il gate resterebbe verde: verifica la
forma, non la saggezza. E' scritto anche in ADR-0058, e va ripetuto qui
perche' un verde che sembra piu' forte di quello che e' fa danno.
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORCH = ROOT / "skills" / "ORCHESTRAZIONE.md"


def _vs():
    spec = importlib.util.spec_from_file_location(
        "vs", ROOT / "scripts" / "validate_skills.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VS = _vs()


def _skill_su_disco() -> "set[str]":
    return {d.name for d in (ROOT / "skills").iterdir()
            if d.is_dir() and (d / "SKILL.md").exists()}


class TestLaGerarchiaCopreTutto(unittest.TestCase):
    def test_oggi_e_verde(self):
        self.assertEqual(VS.check_orchestrazione(ROOT), [])

    def test_diciotto_skill_diciotto_caselle(self):
        """🔎 Il fatto che ha dato fiducia al modello: le skill entrano negli
        strati **una per una**, senza buchi ne' doppioni. Se un giorno il conto
        non torna, o e' nata una skill o il modello non descrive piu' il repo."""
        self.assertEqual(len(_skill_su_disco()), 18)

    def test_i_due_marcatori_esistono(self):
        """Il gate legge due tabelle per marcatore, non per posizione: spostare
        una sezione non deve rompere il controllo."""
        testo = ORCH.read_text(encoding="utf-8")
        for marca in ("<!-- orchestrazione: strati -->",
                      "<!-- orchestrazione: conflitti -->"):
            with self.subTest(marcatore=marca):
                self.assertIn(marca, testo)

    def test_le_due_prose_restano_mutuamente_esclusive(self):
        """🔴 ADR-0035, e il motivo per cui «caricarle tutte» e' il danno:
        `narrative-style` e `prosa-documenti` dettano regole **opposte** sullo
        stesso italiano. Se un giorno la tabella le dichiarasse additive,
        qualcuno le applicherebbe insieme."""
        testo = ORCH.read_text(encoding="utf-8")
        riga = next(r for r in testo.splitlines()
                    if r.startswith("|") and "L1 · CHI LEGGE" in r)
        self.assertIn("mutuamente esclusive", riga)


class TestIlGateMorde(unittest.TestCase):
    """Un cancello che non si e' visto bocciare non e' un cancello."""

    def _con_orchestrazione(self, testo: str):
        originale = ORCH.read_text(encoding="utf-8")
        try:
            ORCH.write_text(testo, encoding="utf-8")
            return VS.check_orchestrazione(ROOT)
        finally:
            ORCH.write_text(originale, encoding="utf-8")

    def test_una_skill_senza_strato_boccia(self):
        """Il caso che il gate esiste per prendere: una skill nuova che nessuno
        ha collocato viene saltata, o caricata a caso."""
        testo = ORCH.read_text(encoding="utf-8").replace(
            "`rumblingstone-playtest`", "`qualcosaltro`")
        errori = self._con_orchestrazione(testo)
        self.assertTrue(any("rumblingstone-playtest" in e and "nessuno strato" in e
                            for e in errori), errori)

    def test_una_skill_in_due_strati_boccia(self):
        testo = ORCH.read_text(encoding="utf-8").replace(
            "| **L4 · COME SI LAVORA** | «Che gesto di lavoro sto facendo?» | `rumblingstone-plans`",
            "| **L4 · COME SI LAVORA** | «Che gesto di lavoro sto facendo?» | `rumblingstone-editoria` · `rumblingstone-plans`")
        errori = self._con_orchestrazione(testo)
        self.assertTrue(any("2 strati" in e for e in errori), errori)

    def test_un_conflitto_che_cita_una_skill_inesistente_boccia(self):
        testo = ORCH.read_text(encoding="utf-8").replace(
            "| C1 | `rumblingstone-campaign`", "| C1 | `skill-che-non-esiste`")
        errori = self._con_orchestrazione(testo)
        self.assertTrue(any("skill-che-non-esiste" in e for e in errori), errori)

    def test_il_nome_CORTO_e_legittimo(self):
        """⚠️ Il lato opposto, e serve: la tabella dei conflitti usa
        «`indagine`», non «`rumblingstone-indagine`», perche' e' cosi' che il
        repo li scrive in prosa. Un gate che pretendesse i nomi lunghi
        renderebbe la tabella illeggibile, e una tabella illeggibile non la
        rilegge nessuno."""
        self.assertEqual(VS.check_orchestrazione(ROOT), [])
        self.assertIn("`indagine`", ORCH.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
