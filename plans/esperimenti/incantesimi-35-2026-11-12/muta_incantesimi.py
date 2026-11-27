#!/usr/bin/env python3
"""muta_incantesimi.py — quanti incantesimi messi al livello sbagliato vede `verifica_scheda`.

Per ogni riga di incantesimi che oggi passa (classe riconosciuta, livello ≥ 1),
si abbassa di uno il livello scritto nella riga, oppure si aggiunge un
incantesimo che la classe non ha. Si conta quante volte la verifica se ne accorge.

Uso: python3 muta_incantesimi.py   (stampa la tabella e scrive misure-incantesimi.json)
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402

#: un incantesimo che la classe non ha: il primo dei tre che nessuna delle sue liste porta
CANDIDATI = (("palla di fuoco", "fireball"), ("cura ferite leggere", "cure light wounds"), ("intralciare", "entangle"))


def fuori_lista(classe: str) -> "str | None":
    liste = V._liste("dnd35")[0]
    for it, en in CANDIDATI:
        if not any(en in liste.get(c, {}) for c in classe.split("+")):
            return it
    return None


def main() -> int:
    conto = {"livello abbassato di uno": [0, 0], "incantesimo fuori lista": [0, 0], "righe con classe": 0,
             "righe senza classe": 0}
    schede = sorted((ROOT / "Bestiario").rglob("*.md")) + sorted(q for d in ROOT.glob("0[0-9]_*") for q in d.rglob("*.md"))
    with tempfile.TemporaryDirectory() as tmp:
        for p in schede:
            testo = p.read_text(encoding="utf-8", errors="replace")
            righe = testo.splitlines()
            for i, riga in enumerate(righe):
                m = V.RIGA_LIVELLO.match(riga)
                if not m or "*" not in m.group(2) or re.match(r"\d", m.group(2)):
                    continue
                classe = V._classe_che_lancia(righe, i)
                conto["righe con classe" if classe else "righe senza classe"] += 1
                if classe is None or int(m.group(1)) < 1 or any(v["riga"] == i + 1 for v in V.incantesimi(p)[0]):
                    continue
                q = Path(tmp) / p.name
                intruso = fuori_lista(classe)
                for nome, nuova in (
                        ("livello abbassato di uno", riga[:m.start(1)] + str(int(m.group(1)) - 1) + riga[m.end(1):]),
                        ("incantesimo fuori lista", riga + f", *{intruso}*")):
                    if nome.startswith("livello") and not re.search(r"\*", riga) or nome.startswith("inc") and not intruso:
                        continue
                    q.write_text("\n".join(righe[:i] + [nuova] + righe[i + 1:]) + "\n", encoding="utf-8")
                    conto[nome][1] += 1
                    conto[nome][0] += any(v["riga"] == i + 1 for v in V.incantesimi(q)[0])
    for k, v in conto.items():
        print(f"{k:28} {v[0]:3}/{v[1]:3}" if isinstance(v, list) else f"{k:28} {v}")
    (Path(__file__).parent / "misure-incantesimi.json").write_text(
        json.dumps(conto, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
