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
  chiamata Agent di uno di quegli agenti, o di ``autore-documenti``. La catena
  si prende dal registro scritto da ``--prompt``; se lì manca (l'hook non scatta
  sul primo messaggio del thread, quello di avvio), dall'ultima riga «Catena:»
  dei messaggi a Claude nella trascrizione (anche quello di avvio, che la
  trascrizione marca ``isMeta``): solo testo scritto, mai il risultato di uno
  strumento. Via
  d'uscita esplicita e registrata: ``--deroga "motivo"`` lanciato dal thread,
  che resta nella trascrizione.

Il blocco vale solo per una catena **scritta**: un riconoscimento per parole
che sbaglia non ferma mai il lavoro.

Il riconoscimento non ha un vocabolario suo: riusa i trigger delle descrizioni
delle skill (``instradamento_skill.raggiunte``, *una norma, un rilevatore*) e
porta ogni skill all'agente che la tiene. Le sole parole proprie sono quelle
dei due agenti le cui skill non le hanno (piattaforma e sviluppo della CI).

Prima delle parole, la forma (M2 di PIANO-MISURA-AGENTI-E-AUTOMATISMI):
``testo_di_lavoro`` toglie quello che non chiede lavoro. L'hook tace su un
tocco di card, un inoltro ``<relay>`` del coordinatore, una notifica, il
resoconto di un sottoagente e un via libera breve; di una busta ``<wake>``
legge solo i messaggi ``trust="principal"``. Gli omonimi dei trigger
(«coordinate», «hook», «master»…) li toglie ``instradamento_skill.OMONIMI``.

⚠️ Il limite: è un riconoscimento per parole. Sbaglia su un messaggio che parla
d'altro, e tace su uno che non usa le parole dei trigger. Per questo suggerisce
e non obbliga; il blocco vero resta quello di ``vincolo_skill.py`` sulla prosa.

    python3 scripts/instradamento_agenti.py --prova "riscrivi il box della forgia"
    python3 scripts/instradamento_agenti.py --riepilogo
    python3 scripts/instradamento_agenti.py --deroga "nessun file cambiato, solo una risposta"
    python3 scripts/instradamento_agenti.py --eval [--json]   # la misura sul set d'oro
    python3 scripts/instradamento_agenti.py --check           # il cricchetto sul test

La misura (ADR-0154): ``--eval`` confronta il primo agente suggerito con il set
d'oro di ``plans/instradamento/agenti-oro.json`` (messaggi veri, «nessuno» se
il messaggio non chiede uno specialista), per split dev, test e tutto, con le
metriche di ``eval_metriche`` (scikit-learn e scipy) e la baseline della classe
maggioritaria del dev. Il JSON di ``--eval --json`` non porta il bootstrap, che
dipende dal generatore di numpy: lo stampa solo il rapporto di testo.
``--check`` legge il campo ``tetto`` del set d'oro (giusti esatti, giusti
indulgenti e macro-F1 sul test) ed esce 1 se uno scende sotto; se sale avvisa,
e il tetto si alza a mano. Confronta interi e la macro-F1 come frazione esatta
ricavata dai conteggi di ``confusion_matrix``, mai i float di sklearn. sklearn e
scipy si importano solo qui: ``--prompt``, ``--stop`` e ``--cancello`` no.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shlex
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eval_metriche as em  # noqa: E402
import instradamento_skill as isk  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REGISTRO = ROOT / ".claude" / ".uso-agenti.jsonl"
ORO = ROOT / "plans" / "instradamento" / "agenti-oro.json"
NESSUNO = "nessuno"
SPLIT = ("dev", "test", "tutto")

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
    # Due voti: le parole del giocato e quelle del ramo, così batte la skill della campagna.
    "sincronizzatore-giocato": re.compile(
        # «sincronizz…» da solo pesca «mantienila sincronizzata» fra le frasi vere: serve l'oggetto
        r"\b(rami? di gruppo|campaign-group-[\w-]+|patch ferm\w*|"
        r"sincronizz\w*\s+(?:\w+\s+){0,3}?(?:giocato|ram[oi]|serat\w*|session\w*|patch)|"
        r"serata giocata|sessione giocata|(?:il|del|al) giocato)\b", re.I),
    # «coda» da sola è «in coda al file»: serve che sia la coda della memoria (ADR-0151).
    "custode-memoria": re.compile(
        r"\b(memoria del progetto|memoria storica|memory\.md|archiviar\w*|archiviat\w*|"
        r"archivia|specchio|coda della memoria(?: storica)?|memoria-storica-coda|file di coda)\b",
        re.I),
}

# A parità di voti vince chi produce, poi chi verifica.
PRIORITA = ("autore-master", "autore-prosa-gioco", "integratore-dm", "sincronizzatore-giocato",
            "piattaforma",
            "cartografo", "impaginatore", "art-director", "regolista", "sviluppatore",
            "custode-memoria", "autore-documenti", "custode-canone", "lettore-a-freddo")

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
    "sincronizzatore-giocato": ("sincronizzatore-giocato", "custode-canone", "autore-documenti"),
    "lettore-a-freddo": ("lettore-a-freddo",),
    "custode-memoria": ("custode-memoria", "autore-documenti"),
}

_SKILL = None


def _skill() -> "dict[str, list[str]]":
    global _SKILL
    if _SKILL is None:
        _SKILL = isk.tutte_le_skill(ROOT)
    return _SKILL


# M2, tecnica 1: i messaggi che non chiedono lavoro. L'hook riceve come prompt anche i tocchi
# sulle card, gli inoltri del coordinatore, le notifiche e i resoconti dei sottoagenti, e
# suggeriva una catena a ognuno. Si riconoscono dalla forma, non dalle parole del lavoro.
_BUSTE_SENZA_LAVORO = re.compile(
    r"^\s*(?:<task-notification\b|\[SYSTEM NOTIFICATION|<system-note>|<system-reminder>|"
    r"<relay\b|<coordinator-relay\b|"
    r"Another Claude session sent a message:|<agent-message\b|\[Subagent hand-back\]|"
    r"This session is being continued from a previous conversation)", re.I)
# Il contesto del progetto in testa al primo messaggio del thread: si chiude con il suo nonce.
_CONTESTO_SESSIONE = re.compile(
    r"^\s*<session-context\b[^>]*?(?:\bnonce=\"([^\"]*)\")?[^>]*>.*?"
    r"</session-context\b(?(1)[^>]*\bnonce=\"\1\")[^>]*>", re.S | re.I)
_WAKE = re.compile(r"^\s*<wake\b([^>]*)>", re.I)
_MESSAGGIO_PRINCIPALE = re.compile(
    r"<message\b[^>]*\btrust=\"principal\"[^>]*>(.*?)</message>", re.S | re.I)
_CARD = re.compile(r"^\s*Chose\s+\"[^\"\n]*\"\s+on the decision card\b", re.I)
# Il resoconto di un sottoagente: almeno due segni della sua forma. Uno solo non basta:
# «Ho visto che la CI è rossa: sistemala» è una richiesta.
_PARTICIPIO = (r"(?:\w+(?:ato|ito|uto)|scritto|fatto|deciso|messo|aperto|chiuso|letto|corretto|"
               r"preso|rimosso|tolto|aggiunto|risolto|tradotto|ridotto|diviso|esteso)")
_SEGNI_RESOCONTO = (
    re.compile(rf"^\s*Ho\s+{_PARTICIPIO}\b", re.I),
    re.compile(r"^\s*Documentazione da aggiornare\s*:", re.I | re.M),
    re.compile(r"\b(?:niente|nessun) (?:commit|push)\b", re.I),
    re.compile(r"^\s*#{1,4}\s+\S", re.M),
    re.compile(r"^\s*\*\*[^*\n]{2,40}:\*\*", re.M),
)
# Il via libera breve: una parola d'assenso e nessun verbo di lavoro, in poche parole.
_ASSENSO = re.compile(
    r"\b(?:ok(?:ay)?|s[iì]|grazie|perfetto|ottimo|confermo|approvo|procedi|procedere|prosegui|"
    r"continua|vai|avanti|fallo|va bene|d'accordo|go ahead|proceed|yes)\b", re.I)
_VERBO_DI_LAVORO = re.compile(
    r"\b(?:scrivi|riscrivi|crea|aggiungi|disegna|sistema|correggi|rivedi|genera|rigenera|"
    r"prepara|fammi|controlla|verifica|cerca|apri|chiudi|misura|impagina|potenzia|"
    r"promuovi|rilascia|unisci|applica|valuta|togli|elimina|cancella|sposta|rinomina|"
    r"(?:stampa|porta) (?:il|lo|la|i|gli|le|un|una|tutt\w)|esporta|aggiorna|traduci|lancia|esegui|metti|usa|cambia|rifai|ricontrolla|"
    r"(?:sistem|corregg|rived|aggiung|toglie?|apr|chiud|aggiorn)[aei]l[aeio]|"
    # «fai», e l'imperativo con il pronome attaccato («scrivimi», «preparamelo»; Codex, #534)
    r"fai|fate|progetta|proponi|definisci|implementa|documenta|"
    r"(?:scriv|riscriv|cre|aggiung|disegn|sistem|corregg|rived|gener|prepar|controll|"
    r"verific|cerc|apr|misur|impagin|aggiorn|traduc|lanc|esegu|mett|cambi|rif)"
    r"[aei](?:mi|ci|ti|vi)(?:lo|la|li|le|ne)?|(?:scriv|prepar|cre|rif)[aei]melo)\b", re.I)
PAROLE_VIA_LIBERA = 12


def testo_di_lavoro(testo: str) -> str:
    """Il testo su cui instradare: vuoto se il messaggio non chiede lavoro.

    Una busta ``<wake>`` vale per i soli messaggi ``trust="principal"`` che porta, non per
    le note di sistema intorno; un tocco su una card, un inoltro del coordinatore, una
    notifica, il resoconto di un sottoagente e un via libera breve non chiedono lavoro. Il
    ``<session-context>`` in testa al primo messaggio del thread non è il messaggio."""
    testo = _CONTESTO_SESSIONE.sub("", testo, count=1)
    m = _WAKE.match(testo)
    if m:
        if 'reason="decision-chosen"' in m.group(1):
            return ""
        testo = "\n".join(html.unescape(x).strip() for x in _MESSAGGIO_PRINCIPALE.findall(testo))
    if not testo.strip() or _BUSTE_SENZA_LAVORO.match(testo) or _CARD.match(testo):
        return ""
    if sum(bool(rx.search(testo)) for rx in _SEGNI_RESOCONTO) >= 2:
        return ""
    if (len(testo.split()) <= PAROLE_VIA_LIBERA and _ASSENSO.search(testo)
            and not _VERBO_DI_LAVORO.search(testo)):
        return ""
    return testo


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
    e non è un verificatore che la catena del primo chiama già. Nessuno se il messaggio non
    chiede lavoro (``testo_di_lavoro``)."""
    testo = testo_di_lavoro(testo)
    if not testo:
        return []
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


# Il prompt parla del giocato o del ramo di gruppo: l'hook porta nel contesto lo stato della sincronia.
# Le stesse parole che danno il voto al sincronizzatore: una norma, un rilevatore.
_GIOCATO = PAROLE_AGENTE["sincronizzatore-giocato"]
CARTELLA_PATCH = Path("/mnt/project-files")


def avviso_sincronia(timeout: float = 8) -> str:
    """L'esito breve di `sincronia_giocato.py --avviso`: vuoto se tutto è in ordine o se non si misura."""
    script = ROOT / "scripts" / "sincronia_giocato.py"
    if not script.exists():
        return ""
    cmd = [sys.executable, str(script), "--avviso", "--repo", str(ROOT)]
    if CARTELLA_PATCH.is_dir():
        cmd += ["--scansiona", str(CARTELLA_PATCH)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return ""
    return r.stdout.strip()


def _con_sincronia(testo: str, agenti: "list[str]", contesto_: str) -> str:
    if not ("sincronizzatore-giocato" in agenti or _GIOCATO.search(testo)):
        return contesto_
    try:
        esito = avviso_sincronia()
    except Exception:  # un hook rotto non ferma mai il lavoro
        return contesto_
    if not esito:
        return contesto_
    return contesto_ + "\n\nSincronia del giocato (`sincronia_giocato.py --avviso`):\n" + esito


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
                   r"(?:git(?:\s+-\S+(?:\s+(?!push\b)[^\s-]\S*)?)*"
                   r"\s+push\b|gh\s+pr\s+(?:create|ready)\b)")
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


def _testo_del_prompt(d: dict) -> str:
    """Il testo di un messaggio scritto a Claude, o "" se la riga non lo è.

    Conta solo un ``type: "user"`` il cui contenuto è una stringa o blocchi
    ``text``: mai un ``tool_result`` (la guida del coordinatore letta con un
    tool porta esempi di «Catena:»), mai una riga ``isSidechain`` (un
    sottoagente). Le righe ``isMeta`` contano: il messaggio di avvio del thread,
    con la nota del coordinatore, arriva così, ed è per questo che l'hook del
    prompt non lo vede."""
    if d.get("type") != "user" or d.get("isSidechain"):
        return ""
    contenuto = (d.get("message") or {}).get("content")
    if isinstance(contenuto, str):
        return contenuto
    if isinstance(contenuto, list):
        return "\n".join(str(b.get("text", "")) for b in contenuto
                         if isinstance(b, dict) and b.get("type") == "text")
    return ""


def catena_dalla_trascrizione(trascrizione: "str | None") -> "list[str]":
    """L'ultima catena scritta nei messaggi a Claude della trascrizione.

    Serve perché l'hook UserPromptSubmit del repo non scatta sul primo messaggio
    di un thread, quello di avvio che porta la catena del coordinatore: senza
    questa lettura il registro resta vuoto e il cancello passa (audit del
    27/11/2026)."""
    if not trascrizione:
        return []
    try:
        righe = Path(trascrizione).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    ultima: "list[str]" = []
    for r in righe:
        if "atena" not in r or '"user"' not in r:
            continue
        try:
            d = json.loads(r)
        except ValueError:
            continue
        if isinstance(d, dict):
            catena = catena_scritta(_testo_del_prompt(d))
            if catena:
                ultima = catena
    return ultima


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


_SEPARATORI = {";", "&&", "||", "|", "&", "(", ")"}
_FORZA = re.compile(r"^(--force(?:-with-lease(?:=.*)?|-if-includes)?|-[a-zA-Z]*f[a-zA-Z]*)$")
# Le opzioni globali di git che prendono un valore, prima del sottocomando.
_GLOBALI_CON_VALORE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--super-prefix",
                       "--config-env", "--exec-path"}
_PUSH_CON_VALORE = {"-o", "--push-option", "--repo", "--receive-pack", "--exec"}
_PREFISSI_COMANDO = {"timeout", "command", "env", "nice", "exec", "nohup", "time", "sudo"}
GITHUB_SCRIVE = ("mcp__github__push_files", "mcp__github__create_or_update_file",
                 "mcp__github__delete_file", "mcp__github__create_branch")
# Gli strumenti che scrivono su una PR: l'input porta solo il numero, i rami si leggono.
GITHUB_PR_SCRIVE = ("mcp__github__merge_pull_request", "mcp__github__update_pull_request_branch")
FAST_FORWARD = ("Solo fast-forward: `git merge origin/main` (mai rebase) e `git push` senza "
                "--force né «+»; se il remoto è avanti, `git pull --no-rebase` e di nuovo i controlli.")


def _ramo_di(ref: str) -> str:
    ref = ref.lstrip("+")
    return ref[len("refs/heads/"):] if ref.startswith("refs/heads/") else ref


def _ramo_corrente(cwd: "str | None") -> str:
    try:
        return subprocess.run(["git", "-C", cwd or ".", "branch", "--show-current"],
                              capture_output=True, text=True, timeout=3).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def _segmenti(comando: str) -> "list[list[str]]":
    """I comandi semplici di una riga di shell, già divisi in parole (le virgolette contano)."""
    out: "list[list[str]]" = []
    for riga in comando.split("\n"):
        try:
            lx = shlex.shlex(riga, posix=True, punctuation_chars=True)
            lx.whitespace_split = True
            parole = list(lx)
        except ValueError:
            parole = re.split(r"\s+", re.sub(r"(&&|\|\||[;|&()])", r" \1 ", riga).strip())
        seg: "list[str]" = []
        for p in parole:
            if p in _SEPARATORI or (p and set(p) <= set(";&|()")):
                if seg:
                    out.append(seg)
                seg = []
            else:
                seg.append(p)
        if seg:
            out.append(seg)
    return out


def _motivo_ramo(dst: str, morti: "set[str]", riscrive: bool) -> "str | None":
    if dst in morti:
        return (f"Push verso `{dst}` fermato: è un ramo di gruppo morto (plans/rami-di-gruppo.json, "
                "ADR-0090) e non si tocca; si cancella quando lo decide il DM.")
    if dst.startswith("campaign-group-") and riscrive:
        return (f"Push che riscrive o cancella `{dst}` fermato: il canone non si riscrive "
                f"(ADR-0007, ADR-0090). {FAST_FORWARD}")
    return None


_CANONE_SU_MAIN = ("Push di canone su main fermato: il canone vivo (sessioni, state.yaml, "
                   "state.md, recap, schede) si scrive solo sul ramo di gruppo (ADR-0007). Porta "
                   "quei file su `campaign-group-<gruppo>` e su main solo il prodotto.")


def cancello_canone(comando: str, cwd: "str | None" = None, _prof: int = 0) -> "str | None":
    """Il motivo per fermare un push che riscrive un ramo di gruppo o porta canone su main, o None.

    Riscrivere: --force, -f, --force-with-lease, un refspec con «+», la cancellazione
    («:ramo», --delete), --mirror, e --all/--tags con la forzatura. HEAD e un push senza
    refspec valgono il ramo corrente della cartella (quella di `git -C` o dell'ultimo
    `cd`). Un ramo morto del registro non riceve nessun push. Canone su main: un push a
    main dal ramo di gruppo (anche `HEAD:main`), o un `git add`/`git commit` di file di
    partita nello stesso comando. `sh -c` e `bash -c` si leggono dentro. Un push a main
    dopo un commit di canone fatto in un'altra chiamata non si vede da qui. Fermati
    sempre: `--prune` e i refspec a glob («*»).

    Limiti noti (aggiramenti voluti, non errori): un alias di git (`git -c alias.x=push`),
    `eval` e `gh api -X DELETE …/git/refs/…` non si leggono.
    """
    import sincronia_giocato as sg  # file di partita e rami morti: una lista sola
    morti = sg.rami_morti(ROOT / "plans" / "rami-di-gruppo.json")
    canone_in_commit = False
    for tok in _segmenti(comando):
        while tok and (re.fullmatch(r"[A-Za-z_]\w*=.*", tok[0]) or tok[0] in _PREFISSI_COMANDO
                       or re.fullmatch(r"-\S*|\d+(?:\.\d+)?[smhd]?", tok[0])):
            tok = tok[1:]
        if not tok:
            continue
        if tok[0] == "cd" and len(tok) > 1:
            cwd = str(Path(cwd or ".") / tok[1])
            continue
        if tok[0] in ("sh", "bash", "zsh", "dash") and "-c" in tok and _prof < 3:
            i = tok.index("-c")
            if i + 1 < len(tok):
                motivo = cancello_canone(tok[i + 1], cwd, _prof + 1)
                if motivo:
                    return motivo
            continue
        if tok[0] != "git":
            continue
        dove, i = cwd, 1
        while i < len(tok) and tok[i].startswith("-"):
            if tok[i] in _GLOBALI_CON_VALORE and i + 1 < len(tok):
                if tok[i] == "-C":
                    dove = str(Path(dove or ".") / tok[i + 1])
                i += 2
            else:
                i += 1
        if i >= len(tok):
            continue
        sotto, args = tok[i], tok[i + 1:]
        if sotto in ("add", "commit"):
            canone_in_commit |= any(sg.e_canone(t) or sg.e_canone(t.rstrip("/") + "/")
                                    for t in args if not t.startswith("-"))
            continue
        if sotto != "push":
            continue
        opzioni, posizionali, j = [], [], 0
        while j < len(args):
            a = args[j]
            if a in _PUSH_CON_VALORE:
                j += 2
                continue
            (opzioni if a.startswith("-") else posizionali).append(a)
            j += 1
        forza = any(_FORZA.match(a) for a in opzioni)
        cancella = any(a in ("-d", "--delete") for a in opzioni)
        if "--mirror" in opzioni:
            return ("`git push --mirror` fermato: riscrive ogni ramo del remoto, compresi i rami "
                    f"di gruppo (ADR-0007, ADR-0090). {FAST_FORWARD}")
        if "--prune" in opzioni:
            return ("`git push --prune` fermato: cancella sul remoto i rami che qui non ci sono, "
                    f"compresi i rami di gruppo (ADR-0007, ADR-0090). {FAST_FORWARD}")
        if any("*" in a for a in posizionali[1:]):
            return ("Push con un refspec a glob («*») fermato: tocca tutti i rami che combaciano, "
                    f"compresi quelli di gruppo e i morti (ADR-0007, ADR-0090). {FAST_FORWARD}")
        if forza and any(a in ("--all", "--branches", "--tags") for a in opzioni):
            return ("Push forzato di tutti i rami o dei tag fermato: tocca anche i rami di gruppo "
                    f"(ADR-0007, ADR-0090). {FAST_FORWARD}")
        corrente = None

        def risolvi(nome: str) -> str:
            nonlocal corrente
            if nome in ("HEAD", "@", ""):
                if corrente is None:
                    corrente = _ramo_corrente(dove)
                return corrente
            return _ramo_di(nome)

        refspec = posizionali[1:]
        if not refspec and not any(a in ("--all", "--branches", "--tags") for a in opzioni):
            refspec = ["HEAD"]
        for r in refspec:
            piu = r.startswith("+")
            r = r.lstrip("+")
            src, sep, dst = r.partition(":")
            if not sep:
                dst = src
            elif not dst:
                dst = src
            src_ramo = risolvi(src) if src else ""
            dst_ramo = risolvi(dst)
            motivo = _motivo_ramo(dst_ramo, morti, forza or piu or cancella or (sep and not src))
            if motivo:
                return motivo
            if dst_ramo == "main" and (src_ramo.startswith("campaign-group-") or canone_in_commit):
                return _CANONE_SU_MAIN
    return None


def cancello_github(strumento: str, inp: dict) -> "str | None":
    """Gli strumenti MCP di GitHub che scrivono: mai su un ramo morto, mai canone su main.

    Sul ramo vivo un commit fatto da questi strumenti si aggiunge sopra la punta del ramo:
    è un fast-forward per costruzione, e passa.
    """
    import sincronia_giocato as sg
    ramo = _ramo_di(str(inp.get("branch") or ""))
    motivo = _motivo_ramo(ramo, sg.rami_morti(ROOT / "plans" / "rami-di-gruppo.json"), False)
    if motivo:
        return motivo
    if ramo == "main":
        percorsi = [str(inp.get("path") or "")] + [str(f.get("path", "")) for f in
                                                   inp.get("files") or [] if isinstance(f, dict)]
        if any(sg.e_canone(p) for p in percorsi if p):
            return _CANONE_SU_MAIN
    return None


def _rami_della_pr(numero: int, owner: str, repo: str) -> "tuple[str, str] | None":
    """(base, head) di una PR letti con `gh api`, o None se non si leggono."""
    try:
        r = subprocess.run(["gh", "api", f"repos/{owner}/{repo}/pulls/{int(numero)}", "--jq",
                            '.base.ref + " " + .head.ref'], capture_output=True, text=True,
                           timeout=5)  # sotto i 10 s dell'hook
    except (OSError, subprocess.SubprocessError, ValueError):
        return None
    parti = r.stdout.split()
    return (parti[0], parti[1]) if r.returncode == 0 and len(parti) == 2 else None


def cancello_pr(strumento: str, inp: dict) -> "str | None":
    """Merge di una PR e aggiornamento del suo ramo: mai un ramo morto, mai il ramo di gruppo su main.

    Se i rami della PR non si leggono, si ferma: non si sa che cosa tocca.
    """
    import sincronia_giocato as sg
    rami = _rami_della_pr(inp.get("pullNumber") or 0, str(inp.get("owner") or ""),
                          str(inp.get("repo") or ""))
    if rami is None:
        return (f"`{strumento}` fermato: non riesco a leggere base e head della PR, quindi non so "
                "se tocca un ramo di gruppo. Controllali con `gh pr view` e riprova.")
    base, head = rami
    morti = sg.rami_morti(ROOT / "plans" / "rami-di-gruppo.json")
    for ramo in ((base, head) if strumento.endswith("merge_pull_request") else (head,)):
        motivo = _motivo_ramo(ramo, morti, False)
        if motivo:
            return motivo
    if strumento.endswith("merge_pull_request") and base == "main" and head.startswith("campaign-group-"):
        return _CANONE_SU_MAIN
    return None


def decidi_cancello(ev: dict) -> dict:
    """Passa, o blocca con il motivo, un push o una PR (ADR-0146, punto 7)."""
    strumento = ev.get("tool_name", "")
    comando = str((ev.get("tool_input") or {}).get("command", ""))
    # Il canone vale anche nei sottoagenti: è il sincronizzatore che spinge.
    motivo = None
    if strumento == "Bash" and "push" in comando:
        motivo = cancello_canone(comando, ev.get("cwd"))
    elif strumento in GITHUB_SCRIVE:
        motivo = cancello_github(strumento, ev.get("tool_input") or {})
    elif strumento in GITHUB_PR_SCRIVE:
        motivo = cancello_pr(strumento, ev.get("tool_input") or {})
    if motivo:
        return {"esito": "blocca", "motivo": motivo}
    if ev.get("agent_id") or not (strumento in PR_MCP or
                                  (strumento == "Bash" and _PUSH.search(comando))):
        return {"esito": "fuori"}
    # Il registro c'è solo se l'hook del prompt è scattato; sul primo messaggio
    # del thread non scatta, e la catena si legge dalla trascrizione.
    catena = (_ultima_catena(ev.get("session_id"))
              or catena_dalla_trascrizione(ev.get("transcript_path")))
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
                "additionalContext": _con_sincronia(testo, catena, (
                    f"Catena scritta nelle istruzioni (ADR-0146): {' → '.join(catena)}, poi "
                    "`autore-documenti`. Chiamali con lo strumento Agent, nell'ordine. Un push "
                    "o una PR senza queste chiamate si ferma; la via d'uscita è "
                    "`instradamento_agenti.py --deroga \"motivo\"`."))}}, ensure_ascii=False))
            return 0
        agenti = scegli(testo)
        if not agenti:
            return 0
        testo = testo_di_lavoro(testo)  # l'avviso della sincronia legge il messaggio, non la busta
        if agenti == _ultimo_suggerito(ev.get("session_id")):
            return 0  # già detto in questa sessione: non ripeterlo a ogni messaggio
        _registra({"evento": "suggerito", "sessione": ev.get("session_id"), "agenti": agenti})
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                                 "additionalContext": _con_sincronia(
                                                     testo, agenti, contesto(agenti))}},
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


def predici(testo: str, scegli_=None) -> str:
    """Il primo agente suggerito, o «nessuno»: quello che il set d'oro giudica."""
    agenti = (scegli_ or scegli)(testo)
    return agenti[0] if agenti else NESSUNO


def _leggi_oro(percorso: Path) -> dict:
    return json.loads(Path(percorso).read_text(encoding="utf-8"))


def valuta(percorso: Path = ORO, scegli_=None, campioni: int = 1000) -> dict:
    """Le metriche per split; la baseline è la classe maggioritaria del dev, applicata a tutti.

    La baseline è ``DummyClassifier(strategy="most_frequent")`` addestrato sul dev.
    Con ``campioni=0`` niente bootstrap: il cancello e il JSON non lo portano."""
    scegli_ = scegli_ or scegli
    casi = _leggi_oro(percorso)["casi"]
    pred = [predici(c["testo"], scegli_) for c in casi]
    dev = [c["atteso"] for c in casi if c["split"] == "dev"]
    base = em.maggioritaria(dev)
    out: dict = {"baseline": {"classe": base, "regola": "classe maggioritaria del dev, "
                              "DummyClassifier most_frequent"}}
    for split in SPLIT:
        idx = [i for i, c in enumerate(casi) if split == "tutto" or c["split"] == split]
        oro = [casi[i]["atteso"] for i in idx]
        acc = [casi[i].get("accettabili", []) for i in idx]
        pr = [pred[i] for i in idx]
        r = em.rapporto(oro, pr, acc, campioni=campioni)
        costante = em.baseline_maggioritaria(dev, len(oro)) or [NESSUNO] * len(oro)
        k = em.giusti(oro, costante)
        r["baseline"] = {
            "giusti": k,
            "accuracy": em.frazione(k, len(oro)),
            "giusti_indulgenti": em.giusti_indulgenti(oro, costante, acc),
            "macro_f1": em.frazione(em.macro_f1_esatta(oro, costante)),
        }
        out[split] = r
    return out


def _frazione_tetto(v) -> Fraction:
    return Fraction(str(v))  # «a/b» esatta, o un decimale scritto («0.1234»)


def controlla(percorso: Path = ORO, scegli_=None) -> "tuple[int, list[str]]":
    """Il cricchetto: 1 se una misura del test scende sotto il tetto, 0 altrimenti."""
    tetto = _leggi_oro(percorso).get("tetto") or {}
    v = valuta(percorso, scegli_, campioni=0)["test"]  # interi e frazioni: niente bootstrap
    mancano = [k for k in ("giusti", "giusti_indulgenti", "macro_f1") if k not in tetto]
    if mancano:
        return 1, [f"✗ instradamento_agenti: nel set d'oro manca il tetto per {', '.join(mancano)} "
                   f"(oggi sul test: giusti {v['giusti']}, indulgenti {v['giusti_indulgenti']}, "
                   f"macro-F1 {v['macro_f1']['frazione']})"]
    misura_f1 = Fraction(v["macro_f1"]["frazione"])
    t_f1 = _frazione_tetto(tetto["macro_f1"])
    if "/" not in str(tetto["macro_f1"]):  # tetto arrotondato: si confronta alla stessa cifra
        misura_f1 = Fraction(round(misura_f1 * 10000), 10000)
    confronti = [("giusti", Fraction(v["giusti"]), Fraction(int(tetto["giusti"]))),
                 ("giusti indulgenti", Fraction(v["giusti_indulgenti"]),
                  Fraction(int(tetto["giusti_indulgenti"]))),
                 ("macro-F1", misura_f1, t_f1)]
    sotto = [f"{nome} {m} < tetto {t}" for nome, m, t in confronti if m < t]
    sopra = [f"{nome} {m} > tetto {t}" for nome, m, t in confronti if m > t]
    n = v["n"]
    riga = (f"test: giusti {v['giusti']}/{n}, indulgenti {v['giusti_indulgenti']}/{n}, "
            f"macro-F1 {v['macro_f1']['frazione']}")
    if sotto:
        return 1, [f"✗ instradamento_agenti: regressione sul test ({'; '.join(sotto)}). {riga}"]
    msg = [f"✓ instradamento_agenti: {riga}, al tetto o sopra"]
    if sopra:
        msg.append(f"⚠ instradamento_agenti: sopra il tetto ({'; '.join(sopra)}): "
                   "alza il tetto a mano nel set d'oro")
    return 0, msg


def _stampa_eval(v: dict) -> None:
    print(f"Instradamento degli agenti contro il set d'oro (ADR-0154); baseline: "
          f"«{v['baseline']['classe']}» ({v['baseline']['regola']})")
    for split in SPLIT:
        r = v[split]
        n = r["n"]
        lo, hi = r["wilson95"]
        b = r["baseline"]
        bo = r.get("macro_f1_bootstrap95")
        print(f"\n== {split} · n {n}")
        print(f"  accuracy             {r['giusti']}/{n} = {r['accuracy']['valore']:.4f}"
              f"  (Wilson 95%: {lo:.4f}-{hi:.4f})")
        print(f"  accuracy indulgente  {r['giusti_indulgenti']}/{n} = "
              f"{r['accuracy_indulgente']['valore']:.4f}")
        boot = (f"  (bootstrap 95%: {bo['basso']:.4f}-{bo['alto']:.4f}, seme {bo['seme']})"
                if bo else "")
        print(f"  macro-F1             {r['macro_f1']['frazione']} = "
              f"{r['macro_f1']['valore']:.4f}{boot}")
        print(f"  baseline             {b['giusti']}/{n} esatti, {b['giusti_indulgenti']}/{n} "
              f"indulgenti, macro-F1 {b['macro_f1']['valore']:.4f}")
        classi = r["classi"]
        larg = max(len(c) for c in classi) if classi else 0
        print("  matrice (righe oro, colonne predizione):")
        for i, c in enumerate(classi):
            print(f"    {i:>2} {c:<{larg}} " + " ".join(f"{x:>2}" for x in r["matrice"][i]))
        print("       " + " " * larg + " " + " ".join(f"{j:>2}" for j in range(len(classi)))
              + "   (la colonna j è la classe della riga j)")
        print(f"  {'classe':<{larg}}  P      R      F1     supporto")
        for c, m in r["per_classe"].items():
            print(f"  {c:<{larg}}  {m['precision']:.4f} {m['recall']:.4f} {m['f1']:.4f} "
                  f"{m['supporto']}")


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
    g.add_argument("--eval", action="store_true",
                   help="misura il primo agente suggerito contro il set d'oro, per split")
    g.add_argument("--check", action="store_true",
                   help="cricchetto sul test: esce 1 se scende sotto il tetto del set d'oro")
    ap.add_argument("--json", action="store_true", help="con --eval: l'uscita in JSON")
    ap.add_argument("--oro", type=Path, default=ORO, help="il set d'oro (default: plans/instradamento/agenti-oro.json)")
    a = ap.parse_args(argv)
    if a.eval:
        if a.json:  # senza bootstrap: l'intervallo cambia fra versioni di numpy
            print(json.dumps(valuta(a.oro, campioni=0), ensure_ascii=False, indent=2))
        else:
            _stampa_eval(valuta(a.oro))
        return 0
    if a.check:
        codice, msg = controlla(a.oro)
        print("\n".join(msg))
        return codice
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
