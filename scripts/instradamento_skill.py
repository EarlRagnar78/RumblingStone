#!/usr/bin/env python3
"""instradamento_skill.py — le frasi vere del DM raggiungono le skill obbligatorie?

L8 di PIANO-AGENT-SKILLS-ESTERNE (D6 del 2026-10-01). ORCHESTRAZIONE dice che
il bersaglio misurabile e' *zero omissioni di cio' che e' obbligatorio*
(§4: L0, una L1, le L2). Questo script lo misura nel solo modo che non chiede
un agente: per ogni frase di `plans/instradamento/casi.json` guarda quali
skill vengono raggiunte dai **trigger fra virgolette** delle loro descrizioni,
cioe' quello che legge un agente che instrada sulle descrizioni.

Una skill obbligatoria che nessun trigger raggiunge e' un'**omissione**.
Due L1 raggiunte insieme (`narrative-style` e `prosa-documenti`) sono un
**conflitto**, perche' sono mutuamente esclusive (ADR-0035).

⚠️ Il limite, da dire: e' una misura lessicale. Un agente che legge la
descrizione intera, o AGENTS.md, puo' arrivare alla skill giusta anche senza
un trigger letterale; e un trigger puo' scattare su una frase che parla
d'altro. Misura il pavimento, non il soffitto.

Il gate (`--check`) e' a cricchetto: fallisce se le omissioni superano il
`tetto_omissioni` scritto nel file dei casi. Il tetto si abbassa a mano
quando le descrizioni migliorano, mai in automatico.

    python3 scripts/instradamento_skill.py            # la tabella
    python3 scripts/instradamento_skill.py --check    # il gate
    python3 scripts/instradamento_skill.py --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
CASI = RADICE / "plans" / "instradamento" / "casi.json"
L1 = ("rumblingstone-narrative-style", "rumblingstone-prosa-documenti")
# Le skill obbligatorie per ORCHESTRAZIONE §4: L0, L1, L2. Solo queste contano «in più».
OBBLIGATORIE = {"rumblingstone-campaign", *L1, "rumblingstone-indagine",
                "rumblingstone-module-standard", "npc-villain-boosting"}

_VIRGOLETTE = re.compile(r'"([^"\n]{2,80})"|“([^”\n]{2,80})”|«([^»\n]{2,80})»')


def normalizza(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    # l'elisione si stacca: «l'avventura» deve dare «avventura», da tutte e due le parti
    s = s.replace("’", " ").replace("‘", " ").replace("'", " ")
    return " ".join(re.sub(r"[^\w+\-−/ ]", " ", s).split())


def descrizione(skill_md: Path) -> str:
    """La descrizione del frontmatter, scalare piegato (`description: >`) o su una riga."""
    righe = skill_md.read_text(encoding="utf-8").splitlines()
    if not righe or righe[0].strip() != "---":
        return ""
    out, dentro = [], False
    for r in righe[1:]:
        if r.strip() == "---":
            break
        if r.startswith("description:"):
            resto = r[len("description:"):].strip()
            if resto and resto not in (">", "|", ">-", "|-"):
                return resto.strip("'\"")
            dentro = True
            continue
        if dentro:
            if r and not r[0].isspace():
                break
            out.append(r.strip())
    return " ".join(out)


def trigger(desc: str) -> "list[str]":
    return [normalizza(next(g for g in m.groups() if g)) for m in _VIRGOLETTE.finditer(desc)]


def tutte_le_skill(radice: Path = RADICE) -> "dict[str, list[str]]":
    return {
        p.parent.name: trigger(descrizione(p))
        for p in sorted((radice / "skills").glob("*/SKILL.md"))
    }


def _prende(t: str, f: str, parole: "set[str]") -> bool:
    """Il trigger intero, o per una parola sola il suo plurale o femminile italiano
    (mistero → misteri, scheda → schede): la radice senza l'ultima vocale."""
    if (" " + t + " ") in f:
        return True
    if " " in t or len(t) < 5 or t[-1] not in "aeio":
        return False
    radice = t[:-1]
    return any(p.startswith(radice) and len(p) <= len(t) + 1 and p[len(radice):] in ("a", "e", "i", "o") for p in parole)


def raggiunte(frase: str, skill: "dict[str, list[str]]") -> "dict[str, list[str]]":
    f = " " + normalizza(frase) + " "
    parole = set(f.split())
    out = {}
    for nome, trig in skill.items():
        presi = [t for t in trig if t and _prende(t, f, parole)]
        if presi:
            out[nome] = presi
    return out


def misura(casi: "list[dict]", skill: "dict[str, list[str]]") -> "list[dict]":
    righe = []
    for c in casi:
        r = raggiunte(c["frase"], skill)
        attese = c["attese"]
        righe.append({
            "frase": c["frase"],
            "attese": attese,
            "raggiunte": sorted(r),
            "omesse": [s for s in attese if s not in r],
            "insieme": c.get("insieme", ""),
            "in_piu": [s for s in sorted(r) if s in OBBLIGATORIE and s not in attese],
            "conflitto_l1": all(x in r for x in L1),
            "perche": {k: v for k, v in r.items() if k in attese},
        })
    return righe


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--casi", type=Path, default=CASI)
    a = ap.parse_args(argv)
    dati = json.loads(a.casi.read_text(encoding="utf-8"))
    righe = misura(dati["casi"], tutte_le_skill())
    omesse = sum(len(r["omesse"]) for r in righe)
    attese = sum(len(r["attese"]) for r in righe)
    conflitti = sum(r["conflitto_l1"] for r in righe)
    in_piu = sum(len(r["in_piu"]) for r in righe)
    tetto = dati.get("tetto_omissioni")

    if a.json:
        print(json.dumps({"omesse": omesse, "attese": attese, "in_piu": in_piu, "conflitti_l1": conflitti,
                          "tetto": tetto, "casi": righe}, ensure_ascii=False, indent=2))
    elif not a.check:
        for r in righe:
            segno = "✓" if not r["omesse"] else "✗"
            print(f"{segno} {r['frase'][:70]}")
            if r["omesse"]:
                print(f"     omesse: {', '.join(r['omesse'])}")
            if r["in_piu"]:
                print(f"     in più: {', '.join(r['in_piu'])}")
            if r["conflitto_l1"]:
                print("     ⚠️ conflitto: tutte e due le L1")
        print(f"\nomissioni {omesse} su {attese} skill obbligatorie, in {len(righe)} frasi · in più {in_piu} · conflitti L1 {conflitti}")
        for ins in ("taratura", "verifica"):
            sub = [r for r in righe if r["insieme"] == ins]
            if sub:
                print(f"  {ins}: {sum(len(r['omesse']) for r in sub)} su {sum(len(r['attese']) for r in sub)}")

    if a.check:
        if tetto is None:
            print(f"✗ instradamento_skill: manca «tetto_omissioni» in {a.casi.name} (oggi {omesse})")
            return 1
        if omesse > tetto or conflitti:
            print(f"✗ instradamento_skill: {omesse} omissioni (tetto {tetto}), {conflitti} conflitti L1")
            return 1
        piu_basso = f" — il tetto si può abbassare a {omesse}" if omesse < tetto else ""
        print(f"✓ instradamento_skill: {omesse} omissioni su {attese}, tetto {tetto}{piu_basso}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
