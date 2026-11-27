"""Il catalogo del riferimento dei plugin (§5) dice quello che dicono manifest e plugin.

`docs/reference/RIFERIMENTO-PLUGIN-DI-SISTEMA.md` §5 ha una riga per capacità:
chi la chiede (campo `sistema.capacita` di `scripts/tools.manifest.json`) e,
per dnd35 e pf1e, i file dati o il plugin da cui la eredita (`sistema.toml`).
Il 2026-11-12 la tabella è rimasta indietro quattro volte in un giorno (#376,
#386, #388, #390): ogni PR che cambia una capacità, chi la chiede o i suoi
file deve aggiornare anche la riga, e questo test la fa diventare rossa finché
non lo fa.

Le parentesi nella colonna «chi la chiede» sono note («le usa anche il
nucleo») e non contano.
"""
from __future__ import annotations

import json
import re
import tomllib
import unittest
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]
RIFERIMENTO = RADICE / "docs" / "reference" / "RIFERIMENTO-PLUGIN-DI-SISTEMA.md"
SISTEMI = ("dnd35", "pf1e")  # le colonne della tabella, in quest'ordine

RIGA = re.compile(r"^\| `([a-z_.]+)` \| .*? \| (.*?) \| (.*?) \| (.*?) \|$", re.M)


def _sezione5(testo: str) -> str:
    inizio = testo.index("## 5 ·")
    fine = testo.index("\n## ", inizio + 1)
    return testo[inizio:fine]


def righe(testo: str) -> dict[str, tuple[str, str, str]]:
    """capacità → (chi la chiede, cella dnd35, cella pf1e), dalla tabella del §5."""
    trovate: dict[str, tuple[str, str, str]] = {}
    for m in RIGA.finditer(_sezione5(testo)):
        if m.group(1) in trovate:
            raise AssertionError(f"capacità `{m.group(1)}` due volte nel §5")
        trovate[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    return trovate


def chi_la_chiede() -> dict[str, set[str]]:
    manifest = json.loads((RADICE / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
    uso: dict[str, set[str]] = {}
    for t in manifest["tools"]:
        for c in (t.get("sistema") or {}).get("capacita", []):
            uso.setdefault(c, set()).add(t["id"])
    return uso


def strumenti_scritti(cella: str) -> set[str]:
    senza_note = re.sub(r"\(.*?\)", "", cella)
    return {p.strip().strip("`") for p in senza_note.split(",") if p.strip().strip("`") not in ("", "—")}


def differenze(testo: str) -> list[str]:
    """Ogni disaccordo fra il §5 e manifest, catalogo e plugin; vuoto = allineato."""
    catalogo = set(tomllib.loads((RADICE / "sistemi" / "catalogo.toml").read_text(encoding="utf-8"))["capacita"])
    tabella = righe(testo)
    uso = chi_la_chiede()
    errori: list[str] = []
    for c in sorted(catalogo - tabella.keys()):
        errori.append(f"`{c}` è nel catalogo ma non ha una riga nel §5")
    for c in sorted(tabella.keys() - catalogo):
        errori.append(f"`{c}` ha una riga nel §5 ma non è nel catalogo")
    for c in sorted(catalogo & tabella.keys()):
        scritti, atteso = strumenti_scritti(tabella[c][0]), uso.get(c, set())
        if scritti != atteso:
            errori.append(f"`{c}`, chi la chiede: §5 {sorted(scritti)}, manifest {sorted(atteso)}")
    for i, sistema in enumerate(SISTEMI, start=1):
        dichiarate = tomllib.loads((RADICE / "sistemi" / sistema / "sistema.toml").read_text(encoding="utf-8"))["capacita"]
        for c, voce in sorted(dichiarate.items()):
            if c not in tabella or not isinstance(voce, dict):
                continue
            cella = tabella[c][i]
            for f in voce.get("dati", []):
                if Path(f).name not in cella:
                    errori.append(f"`{c}`, {sistema}: manca `{Path(f).name}` (dati di sistema.toml)")
            if "eredita" in voce and f"da {voce['eredita']}" not in cella:
                errori.append(f"`{c}`, {sistema}: eredita da {voce['eredita']}, il §5 non lo dice")
    return errori


class TestRiferimentoPlugin(unittest.TestCase):
    def test_il_catalogo_del_riferimento_e_allineato(self):
        errori = differenze(RIFERIMENTO.read_text(encoding="utf-8"))
        self.assertEqual(errori, [], "Aggiorna docs/reference/RIFERIMENTO-PLUGIN-DI-SISTEMA.md §5:\n" + "\n".join(errori))

    def test_il_controllo_vede_una_riga_tolta_e_una_sbagliata(self):
        testo = RIFERIMENTO.read_text(encoding="utf-8")
        riga_gradi = next(l for l in testo.splitlines() if l.startswith("| `creature.gradi` |"))
        senza = testo.replace(riga_gradi + "\n", "")
        self.assertIn("`creature.gradi` è nel catalogo ma non ha una riga nel §5", differenze(senza))
        sbagliata = testo.replace(riga_gradi, riga_gradi.replace("effetti_talenti.toml", "altro.toml"))
        self.assertTrue(any("effetti_talenti.toml" in e for e in differenze(sbagliata)))
        chi = testo.replace(riga_gradi, riga_gradi.replace("| verifica_scheda |", "| — |"))
        self.assertTrue(any("`creature.gradi`, chi la chiede" in e for e in differenze(chi)))


if __name__ == "__main__":
    unittest.main()
