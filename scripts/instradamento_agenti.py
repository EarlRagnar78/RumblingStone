#!/usr/bin/env python3
"""instradamento_agenti.py — il lavoro che entra in un thread trova il suo agente (ADR-0146).

Due hook di Claude Code, attivi nei thread che caricano la configurazione del
repo (ADR-0140):

- ``--prompt`` (UserPromptSubmit): legge il messaggio che arriva (le istruzioni
  del coordinatore, una richiesta del DM), riconosce il tipo di lavoro e mette
  nel contesto l'agente da usare e la catena che segue. Non blocca mai.
- ``--stop`` (Stop): a fine turno scrive nel registro se il thread ha chiamato
  gli agenti suggeriti. Non blocca mai: serve a misurare.
- ``--cancello`` (PreToolUse su ``git push``, ``gh pr create|ready`` e sulla
  creazione di una PR via MCP): **blocca** se le istruzioni del thread hanno
  scritto una catena (una riga «Catena: a → b → c») e nella sessione manca la
  chiamata Agent di uno di quegli agenti, o di ``autore-documenti``. Via
  d'uscita esplicita e registrata: ``--deroga "motivo"`` lanciato dal thread,
  che resta nella trascrizione.

Il blocco vale solo per una catena **scritta**: un riconoscimento per parole
che sbaglia non ferma mai il lavoro.

Il riconoscimento non ha un vocabolario suo: riusa i trigger delle descrizioni
delle skill (``instradamento_skill.raggiunte``, *una norma, un rilevatore*) e
porta ogni skill all'agente che la tiene. Le sole parole proprie sono quelle
dei due agenti le cui skill non le hanno (piattaforma e sviluppo della CI).

⚠️ Il limite: è un riconoscimento per parole. Sbaglia su un messaggio che parla
d'altro, e tace su uno che non usa le parole dei trigger. Per questo suggerisce
e non obbliga; il blocco vero resta quello di ``vincolo_skill.py`` sulla prosa.

    python3 scripts/instradamento_agenti.py --prova "riscrivi il box della forgia"
    python3 scripts/instradamento_agenti.py --riepilogo
    python3 scripts/instradamento_agenti.py --deroga "nessun file cambiato, solo una risposta"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import instradamento_skill as isk  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REGISTRO = ROOT / ".claude" / ".uso-agenti.jsonl"

# Chi tiene ogni skill: l'agente che il lavoro su quella skill deve chiamare.
SKILL_AGENTE = {
    "rumblingstone-narrative-style": "autore-prosa-gioco",
    "rumblingstone-indagine": "autore-prosa-gioco",
    "rumblingstone-module-standard": "autore-master",
    "rumblingstone-prosa-documenti": "autore-documenti",
    "rumblingstone-plans": "autore-documenti",
    "rumblingstone-automation": "integratore-dm",
    "rumblingstone-debugging": "sviluppatore",
    "rumblingstone-mapmaking": "cartografo",
    "rumblingstone-editoria": "impaginatore",
    "rumblingstone-edizione": "impaginatore",
    "rumblingstone-art-direction": "art-director",
    "dnd-35-srd": "regolista",
    "pathfinder-1e-srd": "regolista",
    "npc-villain-boosting": "regolista",
    "rumblingstone-playtest": "lettore-a-freddo",
    "rumblingstone-campaign": "custode-canone",
    "forgotten-realms-lore": "custode-canone",
}

# Parole proprie, solo per gli agenti che nessun trigger di skill raggiunge.
PAROLE_AGENTE = {
    "piattaforma": re.compile(
        r"\b(stable|testing|promuov\w*|promozion\w*|rilasci\w*|release|lockfile|"
        r"requirements|canal[ei] (?:debian|testing|stable)|roadmap|dipendenz\w*|"
        r"librer\w+ (?:nuov\w+|estern\w+))\b", re.I),
    # «CI» solo maiuscolo: in minuscolo è il pronome («ci sono»).
    "sviluppatore": re.compile(
        r"\bCI\b|\b(?i:pytest|workflow|pre-push|validator\w*|validate_\w+|renderer|"
        r"script)\b"),
    "regolista": re.compile(r"\b(potenzi\w*|statblock\w*|stat block)\b", re.I),
    "integratore-dm": re.compile(r"\b(dm\.py|dmcore|server mcp|tools\.manifest)\b", re.I),
}

# A parità di voti vince chi produce, poi chi verifica.
PRIORITA = ("autore-master", "autore-prosa-gioco", "integratore-dm", "piattaforma",
            "cartografo", "impaginatore", "art-director", "regolista", "sviluppatore",
            "autore-documenti", "custode-canone", "lettore-a-freddo")

CATENE = {
    "autore-prosa-gioco": ("autore-prosa-gioco", "custode-canone", "lettore-a-freddo"),
    "autore-master": ("autore-master", "regolista", "custode-canone", "lettore-a-freddo",
                      "autore-documenti"),
    "integratore-dm": ("integratore-dm", "regolista se tocca numeri o schede",
                       "autore-documenti"),
    "sviluppatore": ("sviluppatore", "autore-documenti"),
    "piattaforma": ("piattaforma", "integratore-dm o sviluppatore per il codice",
                    "autore-documenti"),
    "cartografo": ("cartografo", "custode-canone se fissa luoghi della storia",
                   "autore-documenti"),
    "impaginatore": ("impaginatore",),
    "art-director": ("art-director",),
    "regolista": ("regolista", "custode-canone", "autore-documenti"),
    "autore-documenti": ("autore-documenti",),
    "custode-canone": ("custode-canone",),
    "lettore-a-freddo": ("lettore-a-freddo",),
}

_SKILL = None


def _skill() -> "dict[str, list[str]]":
    global _SKILL
    if _SKILL is None:
        _SKILL = isk.tutte_le_skill(ROOT)
    return _SKILL


def voti(testo: str) -> "dict[str, int]":
    """Quante prove porta ogni agente: una per skill raggiunta, una per parola propria."""
    out: "dict[str, int]" = {}
    for skill in isk.raggiunte(testo, _skill()):
        agente = SKILL_AGENTE.get(skill)
        if agente:
            out[agente] = out.get(agente, 0) + 1
    for agente, rx in PAROLE_AGENTE.items():
        if rx.search(testo):
            out[agente] = out.get(agente, 0) + 1
    return out


def scegli(testo: str) -> "list[str]":
    """Al più due agenti: il primo per voti, poi per priorità; il secondo se ha almeno un voto
    e non è un verificatore che la catena del primo chiama già."""
    v = voti(testo)
    if not v:
        return []
    ordine = sorted(v, key=lambda a: (-v[a], PRIORITA.index(a)))
    primo = ordine[0]
    gia = " ".join(CATENE[primo])
    altri = [a for a in ordine[1:] if a not in gia]
    # Le due prose non si sommano (ADR-0035): l'autore dell'altra prosa non entra secondo.
    prose = {"autore-prosa-gioco", "autore-documenti"}
    if primo in prose:
        altri = [a for a in altri if a not in prose]
    return [primo] + altri[:1]


def contesto(agenti: "list[str]") -> str:
    righe = ["Instradamento degli agenti (ADR-0146): il lavoro di questo messaggio "
             "sembra di questo tipo. Usa lo strumento Agent con questi `subagent_type`, "
             "nell'ordine; un agente non ne lancia altri, la catena la guidi tu."]
    for a in agenti:
        righe.append(f"- catena: {' → '.join(CATENE[a])}")
    righe.append("Ogni resoconto chiude con «Documentazione da aggiornare:»; passala ad "
                 "`autore-documenti` insieme al diff. Se il riconoscimento sbaglia, "
                 "ignoralo e scrivi nel resoconto perché.")
    return "\n".join(righe)


def _registra(riga: dict) -> None:
    riga = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **riga}
    try:
        REGISTRO.parent.mkdir(parents=True, exist_ok=True)
        with REGISTRO.open("a", encoding="utf-8") as f:
            f.write(json.dumps(riga, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _ultimo_suggerito(sessione: "str | None") -> "list[str]":
    try:
        righe = REGISTRO.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for r in reversed(righe):
        try:
            d = json.loads(r)
        except ValueError:
            continue
        if d.get("sessione") == sessione and d.get("evento") == "suggerito":
            return d.get("agenti") or []
    return []


_CATENA = re.compile(r"^[\s>*_-]*catena\b[^:\n]*:(.+)$", re.I | re.M)
# Solo un comando che *inizia* con git push o gh pr create|ready (dopo ; && || | o a
# capo, con un eventuale timeout davanti): un heredoc che cita «git push» non conta.
_PUSH = re.compile(r"(?:^|[;&|\n])\s*(?:timeout\s+\S+\s+)?"
                   r"(?:git\s+push\b|gh\s+pr\s+(?:create|ready)\b)")
_DEROGA = re.compile(r"instradamento_agenti\.py\s+--deroga\s+[\"']([^\"']{15,})[\"']")
PR_MCP = ("mcp__github__create_pull_request",)


def nomi_agenti() -> "list[str]":
    return sorted((p.stem for p in (ROOT / ".claude" / "agents").glob("*.md")),
                  key=len, reverse=True)


def catena_scritta(testo: str) -> "list[str]":
    """Gli agenti delle righe «Catena: …» del testo, nell'ordine in cui compaiono."""
    out: "list[str]" = []
    for riga in _CATENA.findall(testo):
        trovati = []
        for nome in nomi_agenti():
            m = re.search(rf"(?<![\w-]){re.escape(nome)}(?![\w-])", riga)
            if m:
                trovati.append((m.start(), nome))
        out += [n for _, n in sorted(trovati) if n not in out]
    return out


def _ultima_catena(sessione: "str | None") -> "list[str]":
    try:
        righe = REGISTRO.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for r in reversed(righe):
        try:
            d = json.loads(r)
        except ValueError:
            continue
        if d.get("sessione") == sessione and d.get("evento") == "catena":
            return d.get("agenti") or []
    return []


def storia_sessione(trascrizione: "str | None") -> "tuple[set[str], list[str]]":
    """Tutti gli agenti chiamati nella sessione e le deroghe scritte, con il motivo."""
    agenti: "set[str]" = set()
    deroghe: "list[str]" = []
    if not trascrizione:
        return agenti, deroghe
    try:
        righe = Path(trascrizione).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return agenti, deroghe
    for r in righe:
        if '"subagent_type"' not in r and "--deroga" not in r:
            continue
        try:
            d = json.loads(r)
        except ValueError:
            continue
        for b in (d.get("message") or {}).get("content") or []:
            if not (isinstance(b, dict) and b.get("type") == "tool_use"):
                continue
            inp = b.get("input") or {}
            if inp.get("subagent_type"):
                agenti.add(str(inp["subagent_type"]))
            if b.get("name") == "Bash":
                deroghe += _DEROGA.findall(str(inp.get("command", "")))
    return agenti, deroghe


def decidi_cancello(ev: dict) -> dict:
    """Passa, o blocca con il motivo, un push o una PR (ADR-0146, punto 7)."""
    strumento = ev.get("tool_name", "")
    comando = str((ev.get("tool_input") or {}).get("command", ""))
    if ev.get("agent_id") or not (strumento in PR_MCP or
                                  (strumento == "Bash" and _PUSH.search(comando))):
        return {"esito": "fuori"}
    catena = _ultima_catena(ev.get("session_id"))
    if not catena:
        return {"esito": "passa", "motivo": "nessuna catena scritta nelle istruzioni"}
    richiesti = catena + ([] if "autore-documenti" in catena else ["autore-documenti"])
    chiamati, deroghe = storia_sessione(ev.get("transcript_path"))
    mancanti = [a for a in richiesti if a not in chiamati]
    if not mancanti:
        return {"esito": "passa", "catena": catena}
    if deroghe:
        return {"esito": "deroga", "catena": catena, "mancanti": mancanti, "motivo": deroghe[-1]}
    return {"esito": "blocca", "catena": catena, "mancanti": mancanti, "motivo": (
        "Push e PR fermati (ADR-0146): le istruzioni del thread scrivono la catena "
        f"{' → '.join(catena)}, e in questa sessione manca la chiamata Agent di "
        f"{', '.join(mancanti)}. Chiamali con lo strumento Agent (`subagent_type`) e passa "
        "ad `autore-documenti` il diff e le righe «Documentazione da aggiornare:». Se la "
        "catena qui non serve davvero, lancia `python3 scripts/instradamento_agenti.py "
        "--deroga \"motivo di almeno 15 caratteri\"`: resta nella trascrizione e nel "
        "registro, e va scritta nel resoconto.")}


def hook_cancello(dati: str) -> int:
    try:
        ev = json.loads(dati)
        d = decidi_cancello(ev)
    except Exception:  # un hook rotto non ferma mai il lavoro
        return 0
    if d["esito"] == "fuori":
        return 0
    _registra({"evento": f"push {d['esito']}", "sessione": ev.get("session_id"),
               **{k: d[k] for k in ("catena", "mancanti", "motivo") if k in d}})
    if d["esito"] == "blocca":
        print(d["motivo"], file=sys.stderr)
        return 2
    return 0


def agenti_chiamati(trascrizione: "str | None") -> "list[str]":
    """Gli agenti lanciati dopo l'ultimo messaggio dell'utente."""
    if not trascrizione:
        return []
    try:
        righe = Path(trascrizione).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    usati: "list[str]" = []
    for r in righe:
        if '"type": "user"' in r or '"type":"user"' in r:
            if '"tool_result"' not in r:
                usati = []
            continue
        if '"subagent_type"' not in r:
            continue
        try:
            d = json.loads(r)
        except ValueError:
            continue
        for b in (d.get("message") or {}).get("content") or []:
            if isinstance(b, dict) and b.get("type") == "tool_use":
                t = (b.get("input") or {}).get("subagent_type")
                if t:
                    usati.append(str(t))
    return usati


def hook_prompt(dati: str) -> int:
    try:
        ev = json.loads(dati)
        if ev.get("agent_id"):
            return 0
        testo = str(ev.get("prompt", ""))
        catena = catena_scritta(testo)
        if catena:
            _registra({"evento": "catena", "sessione": ev.get("session_id"), "agenti": catena})
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    f"Catena scritta nelle istruzioni (ADR-0146): {' → '.join(catena)}, poi "
                    "`autore-documenti`. Chiamali con lo strumento Agent, nell'ordine. Un push "
                    "o una PR senza queste chiamate si ferma; la via d'uscita è "
                    "`instradamento_agenti.py --deroga \"motivo\"`.")}}, ensure_ascii=False))
            return 0
        agenti = scegli(testo)
        if not agenti:
            return 0
        if agenti == _ultimo_suggerito(ev.get("session_id")):
            return 0  # già detto in questa sessione: non ripeterlo a ogni messaggio
        _registra({"evento": "suggerito", "sessione": ev.get("session_id"), "agenti": agenti})
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                                 "additionalContext": contesto(agenti)}},
                         ensure_ascii=False))
    except Exception:  # un hook rotto non ferma mai il lavoro
        return 0
    return 0


def hook_stop(dati: str) -> int:
    try:
        ev = json.loads(dati)
        suggeriti = _ultimo_suggerito(ev.get("session_id"))
        if suggeriti:
            usati = agenti_chiamati(ev.get("transcript_path"))
            _registra({"evento": "fine turno", "sessione": ev.get("session_id"),
                       "agenti": suggeriti, "usati": usati,
                       "seguito": suggeriti[0] in usati})
    except Exception:
        return 0
    return 0


def riepilogo(registro: Path = REGISTRO) -> dict:
    out = {"suggeriti": 0, "turni": 0, "seguiti": 0, "catene": 0,
           "push passati": 0, "push bloccati": 0, "push in deroga": 0}
    try:
        righe = registro.read_text(encoding="utf-8").splitlines()
    except OSError:
        return out
    for r in righe:
        try:
            d = json.loads(r)
        except ValueError:
            continue
        if d.get("evento") == "suggerito":
            out["suggeriti"] += 1
        elif d.get("evento") == "catena":
            out["catene"] += 1
        elif d.get("evento") in ("push passa", "push blocca", "push deroga"):
            chiave = {"push passa": "push passati", "push blocca": "push bloccati",
                      "push deroga": "push in deroga"}[d["evento"]]
            out[chiave] += 1
        elif d.get("evento") == "fine turno":
            out["turni"] += 1
            out["seguiti"] += bool(d.get("seguito"))
    return out


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt", action="store_true", help="hook UserPromptSubmit (stdin)")
    g.add_argument("--stop", action="store_true", help="hook Stop (stdin)")
    g.add_argument("--prova", metavar="TESTO", help="mostra l'instradamento di un testo")
    g.add_argument("--cancello", action="store_true",
                   help="hook PreToolUse su push e PR (stdin); esce 2 per bloccare")
    g.add_argument("--deroga", metavar="MOTIVO",
                   help="via d'uscita dal cancello, con il motivo (resta nella trascrizione)")
    g.add_argument("--riepilogo", action="store_true", help="suggerimenti e quanti seguiti")
    a = ap.parse_args(argv)
    if a.prompt:
        return hook_prompt(sys.stdin.read())
    if a.stop:
        return hook_stop(sys.stdin.read())
    if a.cancello:
        return hook_cancello(sys.stdin.read())
    if a.deroga is not None:
        if len(a.deroga.strip()) < 15:
            print("una deroga vuole un motivo di almeno 15 caratteri", file=sys.stderr)
            return 1
        _registra({"evento": "deroga", "motivo": a.deroga.strip()})
        print(f"deroga registrata: {a.deroga.strip()}. Scrivila nel resoconto.")
        return 0
    if a.riepilogo:
        print(json.dumps(riepilogo(), ensure_ascii=False))
        return 0
    agenti = scegli(a.prova)
    print(contesto(agenti) if agenti else "nessun agente riconosciuto")
    return 0


if __name__ == "__main__":
    sys.exit(main())
