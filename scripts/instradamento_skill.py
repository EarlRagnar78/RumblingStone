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
            "violazioni": [s for s in c.get("escluse", []) if s in r],
            "conflitto_l1": all(x in r for x in L1),
            "perche": {k: v for k, v in r.items() if k in attese},
        })
    return righe


_PAROLA = re.compile(r"[a-z0-9]+")
_VUOTE = set("""il lo la i gli le un una di da in con su per tra fra e o a al del della dei delle
che non si come quando cosa chi use the and for when on of to or with this skill trigger any
""".split())


def vocabolario(desc: str) -> "set[str]":
    """Le parole della descrizione, come le conta run_trigger_evals.py (ADR-0076)."""
    return {w for w in _PAROLA.findall(normalizza(desc)) if len(w) >= 4 and w not in _VUOTE}


def collisioni(skill_trigger: "dict[str, list[str]]", soglia: float = 0.5,
               radice: Path = RADICE) -> "list[tuple[str, str, float]]":
    """Coppie di descrizioni che condividono piu' della soglia del vocabolario minore.

    E' il controllo «near-collide» di run_trigger_evals.py di awesome-llm-apps:
    due descrizioni troppo simili si rubano le frasi a vicenda.
    """
    voc = {n: vocabolario(descrizione(radice / "skills" / n / "SKILL.md")) for n in skill_trigger}
    nomi, out = sorted(voc), []
    for i, a in enumerate(nomi):
        for b in nomi[i + 1:]:
            if voc[a] and voc[b]:
                q = len(voc[a] & voc[b]) / min(len(voc[a]), len(voc[b]))
                if q > soglia:
                    out.append((a, b, round(q, 2)))
    return out


def suggerisci(frase: str) -> str:
    """Le skill obbligatorie che i trigger suggeriscono per una frase, in ordine di strato."""
    r = raggiunte(frase, tutte_le_skill())
    obb = [s for s in sorted(r) if s in OBBLIGATORIE]
    righe = [f"frase: {frase}"]
    if all(x in r for x in L1):
        righe.append("⚠️  tutte e due le L1: decide chi legge (ORCHESTRAZIONE, domanda 2)")
    for s in obb:
        righe.append(f"  {s:34} ← {', '.join(r[s][:3])}")
    altre = [s for s in sorted(r) if s not in OBBLIGATORIE]
    if altre:
        righe.append("  (L3, L4, LR suggerite: " + ", ".join(altre) + ")")
    if not obb:
        righe.append("  nessuna skill obbligatoria raggiunta dai trigger: applica le cinque domande a mano")
    return "\n".join(righe)


def comportamentale(cartella: Path, casi: "list[dict]", soglia: float = 0.5) -> dict:
    """La prova con agenti veri: ogni `run*.json` della cartella e' una corsa.

    Il formato e' {"1": [skill…], "2": […]} con i numeri dei casi nell'ordine di
    casi.json. Una skill e' «caricata» se il suo tasso fra le corse supera la
    soglia: e' il trigger rate di agentskills.io, con tre corse come base.
    """
    corse = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(cartella.glob("run*.json"))]
    out = {"corse": len(corse), "attese_caricate": 0, "attese_saltate": 0, "in_piu": 0,
           "violazioni": 0, "disaccordi": []}
    for i, c in enumerate(casi, 1):
        scelte = {s for s in OBBLIGATORIE
                  if sum(s in r.get(str(i), []) for r in corse) / max(1, len(corse)) > soglia}
        attese, escluse = set(c["attese"]), set(c.get("escluse", []))
        out["attese_caricate"] += len(attese & scelte)
        out["attese_saltate"] += len(attese - scelte)
        out["in_piu"] += len(scelte - attese)
        out["violazioni"] += len(escluse & scelte)
        if scelte != attese:
            out["disaccordi"].append({"n": i, "frase": c["frase"], "saltate": sorted(attese - scelte),
                                      "in_piu": sorted(scelte - attese)})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--casi", type=Path, default=CASI)
    ap.add_argument("--frase", help="suggerisce le skill per una frase sola, ed esce")
    ap.add_argument("--comportamentale", type=Path, help="cartella con le corse run*.json degli agenti")
    a = ap.parse_args(argv)
    if a.frase:
        print(suggerisci(a.frase))
        return 0
    if a.comportamentale:
        r = comportamentale(a.comportamentale, json.loads(a.casi.read_text(encoding="utf-8"))["casi"])
        print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else
              f"{r['corse']} corse · attese caricate {r['attese_caricate']}, saltate {r['attese_saltate']} · "
              f"in più {r['in_piu']} · escluse caricate {r['violazioni']} · disaccordi {len(r['disaccordi'])}")
        return 0
    dati = json.loads(a.casi.read_text(encoding="utf-8"))
    righe = misura(dati["casi"], tutte_le_skill())
    omesse = sum(len(r["omesse"]) for r in righe)
    attese = sum(len(r["attese"]) for r in righe)
    conflitti = sum(r["conflitto_l1"] for r in righe)
    in_piu = sum(len(r["in_piu"]) for r in righe)
    violazioni = sum(len(r["violazioni"]) for r in righe)
    tetto_v = dati.get("tetto_violazioni")
    tetto = dati.get("tetto_omissioni")

    if a.json:
        print(json.dumps({"omesse": omesse, "attese": attese, "in_piu": in_piu, "violazioni": violazioni,
                          "collisioni": collisioni(tutte_le_skill()), "conflitti_l1": conflitti,
                          "tetto": tetto, "casi": righe}, ensure_ascii=False, indent=2))
    elif not a.check:
        for r in righe:
            segno = "✓" if not r["omesse"] else "✗"
            print(f"{segno} {r['frase'][:70]}")
            if r["omesse"]:
                print(f"     omesse: {', '.join(r['omesse'])}")
            if r["violazioni"]:
                print(f"     ⛔ raggiunge un'esclusa: {', '.join(r['violazioni'])}")
            if r["in_piu"]:
                print(f"     in più: {', '.join(r['in_piu'])}")
            if r["conflitto_l1"]:
                print("     ⚠️ conflitto: tutte e due le L1")
        print(f"\nomissioni {omesse} su {attese} skill obbligatorie, in {len(righe)} frasi · in più {in_piu} · violazioni {violazioni} · conflitti L1 {conflitti}")
        for ins in ("taratura", "verifica"):
            sub = [r for r in righe if r["insieme"] == ins]
            if sub:
                print(f"  {ins}: {sum(len(r['omesse']) for r in sub)} su {sum(len(r['attese']) for r in sub)}"
                      f" omesse · {sum(len(r['violazioni']) for r in sub)} violazioni")
        coll = collisioni(tutte_le_skill())
        print(f"collisioni fra descrizioni (oltre il 50% del vocabolario): {len(coll)}")
        for a_, b_, q in coll:
            print(f"  {a_} ↔ {b_}: {q:.0%}")

    if a.check:
        if tetto is None:
            print(f"✗ instradamento_skill: manca «tetto_omissioni» in {a.casi.name} (oggi {omesse})")
            return 1
        if omesse > tetto or conflitti or (tetto_v is not None and violazioni > tetto_v):
            print(f"✗ instradamento_skill: {omesse} omissioni (tetto {tetto}), "
                  f"{violazioni} violazioni (tetto {tetto_v}), {conflitti} conflitti L1")
            return 1
        piu_basso = f" — il tetto si può abbassare a {omesse}" if omesse < tetto else ""
        print(f"✓ instradamento_skill: {omesse} omissioni su {attese}, tetto {tetto}{piu_basso}; "
              f"{violazioni} violazioni, tetto {tetto_v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
