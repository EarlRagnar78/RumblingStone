#!/usr/bin/env python3
"""
session_wizard.py — wizard guidato di fine sessione (Lotto B del piano
AUTOMAZIONE-STATO-SESSIONI).

Fa le domande giuste al DM (con default intelligenti) e scrive il session
log canonico `campaign/sessions/YYYY-MM-DD_session-N.md` conforme al
template — garantendo il formato che gli altri script si aspettano
(`**Total**: N xp a testa`, `Day X → Day Y`, blocchi `## Split — …` per il
party diviso). Il file viene committato subito (ADR-0007 vincolo 4).

Uso:
    python3 scripts/session_wizard.py                 # interattivo
    python3 scripts/session_wizard.py --answers r.json  # non-interattivo (test/CI)
    python3 scripts/dm.py session end                 # wizard + apply, orchestrato

Risposte non-interattive: JSON con le chiavi di DEFAULT_ANSWERS (vedi
sotto); le mancanti usano i default. Sezioni multi-riga: liste di stringhe.

Il wizard crea SOLO file nuovi (mai tocca state.md — quello è compito di
state_apply). Interrompere con Ctrl-C non lascia file a metà: si scrive tutto
alla fine, atomicamente.

🔵 **Il front-matter coi delta (lotto 4e).** Le risposte su March Clock, clock
e stato dei PNG diventano anche un blocco `delta:` in testa al log, coi villain
nominati per `png_id` (`dmcore/delta_sessione.py`). I nomi si risolvono contro
`campaign/state.yaml` **adesso**, mentre il DM è davanti al terminale: un nome
che non aggancia nessuno, o un valore che non torna con lo stato di oggi, lo
vede lui e resta solo prosa. Prima lo scopriva `state_apply`, o nessuno. Per
leggere `state.yaml` serve pyyaml (debito dichiarato, ADR-0037): senza, il log
esce senza front-matter e il wizard lo dice.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore import REPO  # noqa: E402
from dmcore import config as cfg  # noqa: E402
from dmcore import gitio  # noqa: E402
from dmcore import delta_sessione as ds  # noqa: E402

SESSIONS_REL = Path("campaign") / "sessions"

DEFAULT_ANSWERS: dict = {
    "date": None,          # default: oggi
    "number": None,        # default: ultimo N + 1
    "title": "Sessione senza titolo",
    "players": "",         # default: quelli dell'ultima sessione
    "location": "",
    "in_world": "",        # es. "from Day 19 to Day 20"
    "xp_budget": "",
    "summary": [],         # righe di prosa
    "decisions": [],       # bullet
    "xp_lines": [],        # bullet (dettaglio incontri)
    "xp_total": 0,         # int, xp a testa
    "loot": [],            # bullet
    "march_clock": "",     # es. "Day 19 → Day 20 (+1)"
    "ritual_clock": "",    # es. "9/18 → 9/18 (no change)"
    "villain_clocks": "",
    "png_status": "",
    "hooks": [],           # bullet
    "dm_notes": [],        # bullet PRIVATI
    "splits": [],          # [{"pgs": "Tordek", "place": "...", "body": [righe]}]
}


# ------------------------------------------------------------------ input


def _ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val or default


def _ask_multiline(prompt: str) -> list[str]:
    print(f"{prompt} (una voce per riga; riga vuota per finire):")
    out: list[str] = []
    while True:
        line = input("  > ").strip()
        if not line:
            return out
        out.append(line)


def last_session_info(sessions_dir: Path) -> "tuple[int, str]":
    """(ultimo numero di sessione, players dell'ultima sessione)."""
    files = sorted(sessions_dir.glob("????-??-??_session-*.md"))
    if not files:
        return 0, ""
    last = files[-1].read_text(encoding="utf-8", errors="replace")
    m = re.search(r"_session-(\d+)\.md$", files[-1].name)
    num = int(m.group(1)) if m else 0
    pm = re.search(r"\*\*Players present\*\*\s*:\s*(.+)", last)
    return num, (pm.group(1).strip() if pm else "")


def interactive_answers(sessions_dir: Path) -> dict:
    last_n, last_players = last_session_info(sessions_dir)
    a = dict(DEFAULT_ANSWERS)
    print("[wizard] Fine sessione — rispondi; invio = accetta il default.\n")
    a["date"] = _ask("Data reale (YYYY-MM-DD)", date.today().isoformat())
    a["number"] = int(_ask("Numero sessione", str(last_n + 1)))
    a["title"] = _ask("Titolo della sessione", a["title"])
    a["players"] = _ask("Giocatori presenti", last_players)
    a["location"] = _ask("Luogo in-mondo")
    a["in_world"] = _ask("Giorni in-mondo (es. 'from Day 19 to Day 20')")
    a["xp_budget"] = _ask("Budget XP (es. 'CR 13 target (party avg level 13)')")
    a["summary"] = _ask_multiline("\nSummary (2-4 paragrafi)")
    a["decisions"] = _ask_multiline("\nDecisioni chiave")
    a["xp_lines"] = _ask_multiline("\nXP: dettaglio incontri")
    total = _ask("XP TOTALI a testa (solo numero)", "0")
    a["xp_total"] = int(re.sub(r"[^\d]", "", total) or 0)
    a["loot"] = _ask_multiline("\nLoot distribuito")
    print("\nWorld events (formato ESATTO, è ciò che state_apply capisce):")
    a["march_clock"] = _ask("March Clock (es. 'Day 19 → Day 20 (+1)'; vuoto = non toccato)")
    a["ritual_clock"] = _ask("Ritual Clock Azarr Kul (es. '9/18 → 10/18'; vuoto = no change)")
    a["villain_clocks"] = _ask("Villain clocks toccati, separati da virgola "
                               "(es. 'Sonjak 3→4, Ghaurush 0→1')")
    a["png_status"] = _ask("PNG status changes, separati da virgola "
                           "(es. 'Regiarix morto, Sonjak latitante')")
    a["hooks"] = _ask_multiline("\nHook per la prossima sessione")
    while _ask("\nIl party si è diviso? aggiungere un blocco Split? (s/n)", "n").lower() in ("s", "y", "si", "sì"):
        pgs = _ask("  Visto da (PG, separati da virgola)")
        place = _ask("  Dove")
        body = _ask_multiline("  Cosa hanno visto SOLO loro")
        a["splits"].append({"pgs": pgs, "place": place, "body": body})
    a["dm_notes"] = _ask_multiline("\nNote PRIVATE del DM (mai esportate)")
    return a


# ------------------------------------------------------------------ delta

STATE_YAML_REL = Path("campaign") / "state.yaml"
_DAY = re.compile(r"Day\s*(\d+)\s*(?:→|->)\s*Day\s*(\d+)", re.I)
_RITUALE = re.compile(r"(\d+)\s*/\s*(\d+)\s*(?:→|->)\s*(\d+)\s*/\s*\2", re.I)
_CLOCK = re.compile(r"^(.+?)\s+(\d+)\s*(?:/\s*\d+\s*)?(?:→|->)\s*(\d+)(?:\s*/\s*\d+)?$")
#: Come il DM dice uno stato, e quale stato dello schema vuol dire.
_STATO = {
    "killed": "morto", "dead": "morto", "slain": "morto", "morto": "morto",
    "morta": "morto", "ucciso": "morto", "uccisa": "morto",
    "escaped": "latitante", "fled": "latitante", "fuggito": "latitante",
    "fuggita": "latitante", "latitante": "latitante",
    "neutralizzato": "neutralizzato", "neutralizzata": "neutralizzato",
    "catturato": "neutralizzato", "catturata": "neutralizzato",
    "ignoto": "ignoto", "attivo": "attivo",
}


def carica_stato(repo: Path) -> "dict | None":
    """`campaign/state.yaml` letto, o None se manca il file o pyyaml."""
    path = repo / STATE_YAML_REL
    if not path.exists() or ds.yaml is None:
        return None
    return ds.yaml.safe_load(path.read_text(encoding="utf-8"))


def _voci(testo: str) -> "list[str]":
    return [v.strip() for v in re.split(r"[,;]", testo or "") if v.strip()]


def _nome(dati: dict, nome: str, avvisi: list) -> "str | None":
    pid, candidati = ds.risolvi_villain(dati, nome)
    if pid is None:
        avvisi.append(f"«{nome}»: " + (
            f"ambiguo fra {', '.join(candidati)} — scrivi il png_id"
            if candidati else "nessun villain in state.yaml ha questo nome"))
    return pid


def delta_dalle_risposte(a: dict, dati: dict) -> "tuple[dict, list[str]]":
    """(delta, avvisi): le risposte che diventano dati, e quelle che no.

    Ogni voce si valida da sola contro lo stato di oggi: quella che non torna
    esce dal delta con il suo motivo, e resta nella prosa del log, dove il DM
    la vede. Una voce cattiva non trascina fuori le buone.
    """
    delta: dict = {}
    avvisi: list[str] = []

    def valida(chiave, voce) -> bool:
        try:
            ds.operazioni({chiave: voce}, dati)
        except ds.DeltaError as exc:
            avvisi.append(str(exc))
            return False
        return True

    m = _DAY.search(a.get("march_clock") or "")
    if m:
        voce = {"da": int(m.group(1)), "a": int(m.group(2))}
        if voce["da"] != voce["a"] and valida("march_clock", voce):
            delta["march_clock"] = voce
    clock: list = []
    m = _RITUALE.search(a.get("ritual_clock") or "")
    if m and m.group(1) != m.group(3):
        from dmcore.statedata import trova_villain
        i = trova_villain(dati, fondo=m.group(2))
        if i is None:
            avvisi.append(f"Ritual Clock: nessun clock unico su /{m.group(2)}")
        else:
            voce = {"png_id": dati["villain"][i]["png_id"],
                    "da": int(m.group(1)), "a": int(m.group(3))}
            if valida("clock", [voce]):
                clock.append(voce)
    for testo in _voci(a.get("villain_clocks") or ""):
        m = _CLOCK.match(testo)
        if not m:
            avvisi.append(f"«{testo}»: non è nella forma «Nome 3→4», resta prosa")
            continue
        pid = _nome(dati, m.group(1), avvisi)
        if pid is None or m.group(2) == m.group(3):
            continue
        voce = {"png_id": pid, "da": int(m.group(2)), "a": int(m.group(3))}
        if valida("clock", [voce]):
            clock.append(voce)
    stato: list = []
    for testo in _voci(a.get("png_status") or ""):
        parole = testo.rsplit(None, 1)
        if len(parole) != 2 or parole[1].lower() not in _STATO:
            avvisi.append(f"«{testo}»: non è nella forma «Nome morto|latitante|"
                          "neutralizzato|ignoto», resta prosa")
            continue
        pid = _nome(dati, parole[0], avvisi)
        if pid is None:
            continue
        voce = {"png_id": pid, "stato": _STATO[parole[1].lower()]}
        if valida("stato", [voce]):
            stato.append(voce)
    if clock:
        delta["clock"] = clock
    if stato:
        delta["stato"] = stato
    try:
        ds.operazioni(delta, dati)  # i doppioni si vedono solo tutti insieme
    except ds.DeltaError as exc:
        avvisi.append(f"delta scartato per intero: {exc}")
        return {}, avvisi
    return delta, avvisi


# ------------------------------------------------------------------ render


def _bullets(items: list[str], empty: str = "- —") -> str:
    return "\n".join(f"- {i.lstrip('- ')}" for i in items) if items else empty


def render(a: dict, delta: "dict | None" = None) -> str:
    o: list[str] = []
    if delta:
        o.append(ds.emetti(delta))
    o.append(f"# Session {a['number']} — {a['title']} ({a['date']})\n")
    o.append(f"**Players present**: {a['players'] or '—'}")
    o.append(f"**Location**: {a['location'] or '—'}")
    o.append(f"**In-world dates**: {a['in_world'] or '—'}")
    o.append(f"**Session XP budget**: {a['xp_budget'] or '—'}\n")
    o.append("## Summary\n")
    o.append("\n\n".join(a["summary"]) if a["summary"] else "—")
    o.append("\n## Key decisions\n")
    o.append(_bullets(a["decisions"]))
    o.append("\n## XP awarded\n")
    if a["xp_lines"]:
        o.append(_bullets(a["xp_lines"]))
    o.append(f"- **Total**: {a['xp_total']} xp a testa")
    o.append("\n## Loot distributed\n")
    o.append(_bullets(a["loot"]))
    o.append("\n## World events triggered\n")
    o.append(f"- **March Clock**: {a['march_clock'] or 'no change'}")
    o.append(f"- **Ritual Clock Azarr Kul**: {a['ritual_clock'] or 'no change'}")
    o.append(f"- **Villain clocks**: {a['villain_clocks'] or 'nessuno toccato'}")
    o.append(f"- **PNG status changes**: {a['png_status'] or 'nessuno'}")
    o.append("\n## Next session hooks\n")
    o.append(_bullets(a["hooks"]))
    for s in a["splits"]:
        pgs = s.get("pgs", "?")
        o.append(f"\n## Split — {pgs} @ {s.get('place', '?')}\n")
        o.append(f"**Visto da**: {pgs}\n")
        body = s.get("body", [])
        o.append("\n".join(body) if isinstance(body, list) else str(body))
    if a["dm_notes"]:
        o.append("\n## DM notes (private — optional)\n")
        o.append(_bullets(a["dm_notes"]))
    return "\n".join(o).rstrip() + "\n"


# ------------------------------------------------------------------ main


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(
        description="Wizard guidato di fine sessione → session log canonico.")
    ap.add_argument("--answers", type=Path,
                    help="JSON di risposte (non-interattivo, per test/CI)")
    ap.add_argument("--out", help="nome file esplicito sotto campaign/sessions/")
    ap.add_argument("--no-commit", action="store_true", help="non committare il file")
    ap.add_argument("--no-guard", action="store_true",
                    help="salta la guardia branch (SOLO test)")
    ap.add_argument("--repo-root", type=Path, default=REPO, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    repo = args.repo_root.resolve()
    sessions_dir = repo / SESSIONS_REL

    if not args.no_guard:
        group = cfg.load_group(repo)
        try:
            gitio.guard_canon_branch(
                repo, expected=cfg.group_branch(group) if group else None)
        except gitio.BranchGuardError as exc:
            print(f"[wizard] ✗ {exc}", file=sys.stderr)
            return 1

    if args.answers:
        a = dict(DEFAULT_ANSWERS)
        a.update(json.loads(args.answers.read_text(encoding="utf-8")))
        if a["date"] is None:
            a["date"] = date.today().isoformat()
        if a["number"] is None:
            a["number"] = last_session_info(sessions_dir)[0] + 1
    else:
        try:
            a = interactive_answers(sessions_dir)
        except (KeyboardInterrupt, EOFError):
            print("\n[wizard] interrotto — nessun file scritto")
            return 130

    delta: dict = {}
    dati = carica_stato(repo)
    if dati is None:
        print(f"[wizard] ⚠ {STATE_YAML_REL} o pyyaml assenti: il log esce senza "
              "front-matter, e state_apply ricadrà sulla regex")
    else:
        delta, avvisi = delta_dalle_risposte(a, dati)
        for testo in avvisi:
            print(f"[wizard] ⚠ {testo}")
        voci = (len(delta.get("clock") or []) + len(delta.get("stato") or [])
                + (1 if delta.get("march_clock") else 0))
        print(f"[wizard] front-matter: {voci} voci diventano dati"
              + (f", {len(avvisi)} restano solo prosa" if avvisi else ""))

    name = args.out or f"{a['date']}_session-{a['number']}.md"
    out_path = sessions_dir / name
    if out_path.exists():
        print(f"[wizard] ✗ {out_path} esiste già — scegli --out diverso o "
              f"rimuovi il file", file=sys.stderr)
        return 1
    sessions_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render(a, delta), encoding="utf-8")
    print(f"[wizard] ✓ scritto {out_path}")

    if not args.no_commit:
        sha = gitio.commit_paths(
            repo, [str(out_path.relative_to(repo))],
            f"Session {a['number']}: {a['title']} ({a['date']}) [wizard]")
        print(f"[wizard] ✓ commit {sha}" if sha else "[wizard] (niente da committare)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
