#!/usr/bin/env python3
"""vincolo_skill.py — l'hook che lega le scritture di prosa alla skill giusta (ADR-0146).

Claude Code lo chiama prima di ogni Edit, Write e MultiEdit (hook PreToolUse in
`.claude/settings.json`). Guarda il file che si sta per scrivere e la
trascrizione della sessione, e decide:

    prosa      handout, recap, introduzioni e appendici dei volumi: senza
               `rumblingstone-narrative-style` caricata la scrittura si BLOCCA
    misto      master, schede, moduli: si blocca solo se il testo nuovo contiene
               un box read-aloud (il rilevatore e' `misura_craft.box_read_aloud`,
               una norma un rilevatore); statblock e tabelle passano
    documento  ADR, piani, guide, skill: se manca `rumblingstone-prosa-documenti`
               passa con un promemoria, non si blocca
    (nessuna)  codice, file generati, archivi: passa in silenzio

La skill conta come caricata se la sessione l'ha invocata (strumento Skill o
comando `/nome`), se un sottoagente l'ha invocata nella propria trascrizione, o
se l'agente che scrive la precarica nel campo `skills:` del suo file in
`.claude/agents/`. Con la skill caricata, i `references/` obbligatori di
narrative-style che la sessione non ha ancora letto arrivano come promemoria
(prima regola d'oro), senza blocco.

Ogni decisione su un file vincolato va in `.claude/.uso-skill.jsonl`
(ignorato da git): e' la misura d'uso che prima costava una lettura di
trascrizioni. Un errore dell'hook non blocca mai: esce 0.

Uso:
    python3 scripts/vincolo_skill.py --hook            # da Claude Code, evento su stdin
    python3 scripts/vincolo_skill.py --riepilogo       # quanti blocchi, passaggi, promemoria
    python3 scripts/vincolo_skill.py --classe FILE...  # in che classe cade un file
    python3 scripts/vincolo_skill.py --cambiati REV    # i file di gioco cambiati da REV
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
AGENTI = ROOT / ".claude" / "agents"
REGISTRO = ROOT / ".claude" / ".uso-skill.jsonl"

SKILL_PROSA = "rumblingstone-narrative-style"
SKILL_DOCUMENTI = "rumblingstone-prosa-documenti"
#: I references che AGENTS.md dichiara «obbligatori e da leggere» per la prosa di gioco.
REFERENCES_PROSA = ("italiano-nativo.md", "read-aloud-adulti.md",
                    "editorial-standards.md", "style-pillars.md")

#: Le cartelle del contenuto di gioco: le stesse di validate_prosa.CONTENUTO.
CONTENUTO = ("00_", "01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_",
             "10-stand-alone", "STANDALONE-", "campaign", "PG", "Bestiario")
#: Le cartelle e i file dei documenti: validate_prosa.DOCUMENTI e DOC_RADICE.
DOCUMENTI = ("docs/", "plans/", "skills/")
DOC_RADICE = ("README.md", "AGENTS.md", "CLAUDE.md", "LICENSES.md", "MEMORIA.md")
#: Archivi e generati: misura_craft.ESCLUSI ed ESCLUSI_NOME, senza «homebrew»,
#: perche' le introduzioni dei volumi (homebrew/volume-*/NN-*.md) si scrivono a mano.
ESCLUSI = ("_ARCHIVIO", "build", "rendered")
ESCLUSI_NOME = ("DEPRECATO", "ERRATA-", "APPARATO-", ".hb.md")

#: Prosa pura: chi legge e' il giocatore, o il DM la legge ad alta voce.
#: Ogni modello deve pescare almeno un file del repo (lo prova un test).
PROSA_PURA = (
    r"/homebrew/volume-[^/]+/\d\d-[^/]+\.md$",   # introduzioni e capitoli del volume
    r"HANDOUT",                                   # handout ai giocatori
    r"(^|/)campaign/recaps/",                     # recap della serata
    r"(^|/)appendice[_-][^/]+\.md$",              # appendici dei moduli
    r"TEASER",
)
_PROSA = re.compile("|".join(PROSA_PURA), re.I)


def relativo(percorso: str) -> "str | None":
    """Il percorso relativo al repo, o None se il file e' fuori."""
    p = Path(percorso)
    if not p.is_absolute():
        p = ROOT / p
    try:
        return p.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return None


def classe(rel: str) -> "str | None":
    """prosa, misto, documento, o None se il file non si vincola."""
    if not rel.endswith(".md"):
        return None
    parti = rel.split("/")
    if any(x in parti for x in ESCLUSI) or any(x in parti[-1] for x in ESCLUSI_NOME):
        return None
    if any(p.startswith("_SNAPSHOT") for p in parti):
        return None
    if parti[0].startswith(CONTENUTO):
        return "prosa" if _PROSA.search(rel) else "misto"
    if rel.startswith(DOCUMENTI) or rel in DOC_RADICE:
        return "documento"
    return None


def testo_nuovo(evento: dict) -> str:
    inp = evento.get("tool_input") or {}
    if "content" in inp:
        return str(inp["content"])
    if "edits" in inp:
        return "\n".join(str(e.get("new_string", "")) for e in inp["edits"])
    return str(inp.get("new_string", ""))


def _ha_box(testo: str) -> bool:
    import misura_craft as mc
    return bool(mc.box_read_aloud(testo))


# ── che cosa ha caricato la sessione ────────────────────────────────────────

def _trascrizioni(evento: dict) -> "list[Path]":
    out = []
    t = evento.get("transcript_path")
    if t:
        out.append(Path(t))
        aid = evento.get("agent_id")
        if aid:
            base = Path(t).with_suffix("")
            out += sorted((base / "subagents").glob(f"agent-{aid}*.jsonl"))
    if evento.get("agent_transcript_path"):
        out.append(Path(evento["agent_transcript_path"]))
    return out


_COMANDO = re.compile(r"<command-name>/?(?:[\w-]+:)?([\w-]+)</command-name>")


def caricato(evento: dict) -> "tuple[set[str], set[str]]":
    """Le skill invocate e i file di skill letti, da tutte le trascrizioni utili."""
    skill: "set[str]" = set()
    letti: "set[str]" = set()
    for t in _trascrizioni(evento):
        try:
            righe = t.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for riga in righe:
            if '"Skill"' not in riga and "skills/" not in riga and "command-name" not in riga:
                continue
            try:
                dato = json.loads(riga)
            except ValueError:
                continue
            msg = dato.get("message") or {}
            contenuto = msg.get("content")
            if isinstance(contenuto, str):
                skill.update(_COMANDO.findall(contenuto))
                continue
            for b in contenuto or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text":
                    skill.update(_COMANDO.findall(b.get("text", "")))
                if b.get("type") != "tool_use":
                    continue
                inp = b.get("input") or {}
                if b.get("name") == "Skill":
                    skill.add(str(inp.get("skill", "")).split(":")[-1])
                elif b.get("name") == "Read" and "skills/" in str(inp.get("file_path", "")):
                    letti.add(str(inp["file_path"]))
                elif b.get("name") == "Bash" and "skills/" in str(inp.get("command", "")):
                    letti.update(re.findall(r"skills/[\w./-]+\.md", inp["command"]))
    return skill, letti


def precaricate(agente: "str | None") -> "set[str]":
    """Le skill nel campo `skills:` del file dell'agente, se e' uno del repo."""
    if not agente:
        return set()
    f = AGENTI / f"{agente.split(':')[-1]}.md"
    try:
        testo = f.read_text(encoding="utf-8")
    except OSError:
        return set()
    m = re.match(r"---\n(.*?)\n---", testo, re.S)
    if not m:
        return set()
    out: "set[str]" = set()
    dentro = False
    for riga in m.group(1).splitlines():
        if riga.startswith("skills:"):
            resto = riga[len("skills:"):].strip()
            if resto.startswith("["):
                out.update(x.strip(" '\"") for x in resto.strip("[]").split(",") if x.strip())
            dentro = not resto
            continue
        if dentro and riga.lstrip().startswith("- "):
            out.add(riga.split("- ", 1)[1].strip(" '\""))
        elif dentro and riga and not riga.startswith(" "):
            dentro = False
    return {s.split(":")[-1] for s in out}


# ── la decisione ───────────────────────────────────────────────────────────

def decidi(evento: dict) -> dict:
    rel = relativo(str((evento.get("tool_input") or {}).get("file_path", "")))
    c = classe(rel) if rel else None
    esito = {"file": rel, "classe": c, "esito": "passa", "motivo": ""}
    if c is None:
        return esito
    if c == "misto" and not _ha_box(testo_nuovo(evento)):
        return esito

    invocate, letti = caricato(evento)
    disponibili = invocate | precaricate(evento.get("agent_type"))
    esito["skill"] = sorted(disponibili)

    if c == "documento":
        if SKILL_DOCUMENTI not in disponibili:
            esito.update(esito="ricorda", motivo=(
                f"{rel} è un documento del repo: prima di scriverlo carica la skill "
                f"`{SKILL_DOCUMENTI}` (strumento Skill) e, a testo finito, "
                f"`python3 scripts/validate_prosa.py --documenti {rel}` (ADR-0146)."))
        return esito

    if SKILL_PROSA not in disponibili:
        perche = ("contiene un box read-aloud" if c == "misto"
                  else "è prosa che legge o ascolta un giocatore")
        esito.update(esito="blocca", motivo=(
            f"Scrittura fermata: {rel} {perche}, e in questa sessione la skill "
            f"`{SKILL_PROSA}` non è stata caricata. Caricala con lo strumento Skill, "
            f"leggi i suoi references obbligatori ({', '.join(REFERENCES_PROSA)}) e "
            "riprova; oppure affida il lavoro all'agente `autore-prosa-gioco`, che la "
            "precarica. Statblock e tabelle senza box passano senza skill (ADR-0146)."))
        return esito

    mancano = [r for r in REFERENCES_PROSA if not any(l.endswith(r) for l in letti)]
    if mancano:
        esito.update(esito="ricorda", motivo=(
            f"La skill `{SKILL_PROSA}` è caricata, ma questi references obbligatori "
            f"non risultano letti in questa sessione: {', '.join(mancano)} "
            f"(skills/{SKILL_PROSA}/references/). Il SKILL.md è l'indice, non la norma "
            "(prima regola d'oro, G1). Prima di consegnare: `python3 scripts/misura_craft.py "
            f"--box {rel}`."))
    return esito


def _registra(esito: dict, evento: dict) -> None:
    if esito.get("classe") is None:
        return
    riga = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "sessione": evento.get("session_id"), "agente": evento.get("agent_type"),
            "strumento": evento.get("tool_name"), **{k: esito.get(k) for k in
                                                       ("file", "classe", "esito", "skill")}}
    try:
        REGISTRO.parent.mkdir(parents=True, exist_ok=True)
        with REGISTRO.open("a", encoding="utf-8") as f:
            f.write(json.dumps(riga, ensure_ascii=False) + "\n")
    except OSError:
        pass


def esegui_hook(grezzo: str) -> int:
    """0 = passa (con o senza promemoria), 2 = blocca con il motivo su stderr."""
    try:
        evento = json.loads(grezzo)
        esito = decidi(evento)
    except Exception as e:  # noqa: BLE001 — un hook rotto non deve fermare il lavoro
        print(f"vincolo_skill: errore interno ({e}), scrittura lasciata passare",
              file=sys.stderr)
        return 0
    _registra(esito, evento)
    if esito["esito"] == "blocca":
        print(esito["motivo"], file=sys.stderr)
        return 2
    if esito["esito"] == "ricorda":
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "additionalContext": esito["motivo"]}},
            ensure_ascii=False))
    return 0


def riepilogo(registro: Path = REGISTRO) -> "dict[str, int]":
    c: Counter = Counter({"blocca": 0, "passa": 0, "ricorda": 0})
    if registro.exists():
        for riga in registro.read_text(encoding="utf-8").splitlines():
            try:
                c[json.loads(riga).get("esito", "?")] += 1
            except ValueError:
                continue
    return dict(c)


def cambiati(rev: str) -> "list[str]":
    """I file di prosa o misti cambiati da `rev` (per il rapporto CI sul testo cambiato)."""
    import subprocess
    out = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AM", f"{rev}...HEAD"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [f for f in out.splitlines() if classe(f) in ("prosa", "misto")]


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--hook", action="store_true", help="evento PreToolUse su stdin")
    g.add_argument("--riepilogo", action="store_true", help="i conti del registro")
    g.add_argument("--classe", nargs="+", metavar="FILE", help="la classe di ogni file")
    g.add_argument("--cambiati", metavar="REV", help="i file di gioco cambiati da REV")
    a = ap.parse_args(argv)
    if a.hook:
        return esegui_hook(sys.stdin.read())
    if a.riepilogo:
        print(json.dumps(riepilogo(), ensure_ascii=False))
        return 0
    if a.cambiati:
        print("\n".join(cambiati(a.cambiati)))
        return 0
    for f in a.classe:
        rel = relativo(f)
        print(f"{classe(rel) if rel else None}\t{f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
