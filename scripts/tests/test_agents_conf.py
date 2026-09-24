"""La matrice degli agenti sta in un posto solo: `scripts/agents.conf` (D22).

Prima del 2026-09-24 era scritta tre volte: in `build-skills.sh`, in
`sync-skills.sh` e nell'elenco «Supported Agents» di `AGENTS.md`. Il file che la
unificava era nato nella review della PR #1 e non era mai arrivato su `main`,
perche' spinto sul ramo dopo il merge. Questi test fanno rosso se una delle
copie ricompare o se `AGENTS.md` dice un formato diverso da quello che si
costruisce davvero.
"""
from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CONF = ROOT / "scripts" / "agents.conf"
SCRIPT = [ROOT / "scripts" / "build-skills.sh", ROOT / "scripts" / "sync-skills.sh"]

VOCE = re.compile(r'\["(?P<k>[^"]+)"\]="(?P<v>[^"]*)"')


def matrice() -> "dict[str, dict[str, str]]":
    """Le tabelle di agents.conf, lette da Bash stesso: la sintassi e' quella vera."""
    comando = ('source scripts/agents.conf; for t in AGENT_FORMAT AGENT_REPO_ROOTS '
               'AGENT_INSTALL_PATHS; do declare -n a=$t; for k in "${!a[@]}"; do '
               'printf "%s\\t%s\\t%s\\n" "$t" "$k" "${a[$k]}"; done; unset -n a; done')
    uscita = subprocess.run(["bash", "-c", comando], cwd=ROOT, capture_output=True,
                            text=True, check=True).stdout
    out: dict[str, dict[str, str]] = {}
    for riga in uscita.splitlines():
        tabella, chiave, valore = riga.split("\t")
        out.setdefault(tabella, {})[chiave] = valore
    return out


class TestUnaMatriceSola(unittest.TestCase):
    def test_gli_script_la_leggono_e_non_ne_hanno_una_propria(self):
        for s in SCRIPT:
            testo = s.read_text(encoding="utf-8")
            with self.subTest(script=s.name):
                self.assertIn('source "${SCRIPT_DIR}/agents.conf"', testo)
                self.assertNotRegex(testo, r"declare -A AGENT_")
                self.assertNotIn("AGENT_ENTRIES", testo)

    def test_ogni_agente_ha_formato_e_specchio(self):
        m = matrice()
        self.assertEqual(set(m["AGENT_FORMAT"]), set(m["AGENT_REPO_ROOTS"]))
        self.assertLessEqual(set(m["AGENT_INSTALL_PATHS"]), set(m["AGENT_FORMAT"]))
        self.assertLessEqual(set(m["AGENT_FORMAT"].values()),
                             {"compact.md", "structured.yaml", "machine.json"})

    def test_agents_md_dice_le_stesse_cose(self):
        """«Supported Agents»: radice dello specchio e formato, agente per agente."""
        testo = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        dichiarati = {m.group(1): m.group(2) for m in re.finditer(
            r"^- \*\*[^*]+\*\* → `([^`]+)/<skill>/` \((compact\.md|structured\.yaml|machine\.json)",
            testo, re.M)}
        m = matrice()
        attesi = {m["AGENT_REPO_ROOTS"][a]: f for a, f in m["AGENT_FORMAT"].items()}
        self.assertEqual(dichiarati, attesi)


if __name__ == "__main__":
    unittest.main()
