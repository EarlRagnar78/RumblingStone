#!/usr/bin/env python3
"""
state_apply.py — applica a campaign/state.md le proposte meccaniche di
state_sync.py, SOLO dentro le regioni marcate `auto:` (ADR-0007).

Divisione dei ruoli (piano AUTOMAZIONE §3):
  - `state_sync.py`  rileva i trigger nei session log e PROPONE (invariato);
  - questo script APPLICA il sottoinsieme meccanico delle proposte, con
    diff a video e conferma per blocco, dentro le regioni marcate;
  - tutto il resto (prosa, tabelle villain, §1 party) resta proposta da
    applicare a mano: viene stampato, mai toccato.

Regioni gestite (v1):
  march-clock   righe "Current March Day" / "Days remaining" (§2.1)
  changelog     blocco append-only del §8

Uso:
    python3 scripts/state_apply.py --migrate            # inserisce i marker (una tantum, idempotente)
    python3 scripts/state_apply.py --session FILE.md    # proponi+applica dagli eventi di un log
    python3 scripts/state_apply.py --session FILE.md --check   # solo diff, niente scritture
    python3 scripts/state_apply.py --session FILE.md --yes --commit

Sicurezza (ADR-0007): guardia branch (mai su main); rifiuta se state.md ha
modifiche non committate (così `git revert` è sempre pulito); qualsiasi
anomalia di parsing → nessuna scrittura, restano le proposte a video.
`--no-guard` esiste SOLO per i test su repository temporanei.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore import REPO  # noqa: E402
from dmcore import config as cfg  # noqa: E402
from dmcore import gitio  # noqa: E402
from dmcore.regions import RegionError, find_regions, replace_region, wrap  # noqa: E402
from state_sync import extract_events, _suggest  # noqa: E402

STATE_REL = Path("campaign") / "state.md"
SESSIONS_REL = Path("campaign") / "sessions"

#: Day di arrivo dell'orda a Rethmar (waypoint finale §2.1 — canone RHoD adattato).
RETHMAR_DAY = 42

MARCH_DAY_RE = re.compile(r"\*\*Current March Day:\*\*\s*\*\*(\d+)\*\*")
DAYS_LEFT_RE = re.compile(r"\*\*Days remaining to Rethmar:\*\*")
FENCE_RE = re.compile(r"^```", re.M)


# ------------------------------------------------------------------ migrate


def migrate(text: str) -> "tuple[str, list[str]]":
    """Avvolge nei marker le zone gestite. Idempotente: salta le regioni
    già presenti. Ritorna (testo, regioni aggiunte)."""
    added: list[str] = []
    existing = find_regions(text)

    if "march-clock" not in existing:
        m = MARCH_DAY_RE.search(text)
        if not m:
            raise RegionError("riga '**Current March Day:**' non trovata: "
                              "impossibile migrare la regione march-clock")
        start = text.rfind("\n", 0, m.start()) + 1
        # la regione copre la riga del Day e l'eventuale riga Days remaining
        end = text.find("\n", m.end()) + 1
        m2 = DAYS_LEFT_RE.search(text, end)
        if m2 and m2.start() == end:  # riga immediatamente successiva
            end = text.find("\n", m2.end()) + 1
        text = text[:start] + wrap("march-clock", text[start:end]) + "\n" + text[end:]
        added.append("march-clock")

    existing = find_regions(text)
    if "changelog" not in existing:
        h = re.search(r"^##\s*8\.\s*Changelog.*$", text, re.M)
        if not h:
            raise RegionError("sezione '## 8. Changelog' non trovata: "
                              "impossibile migrare la regione changelog")
        fences = [f for f in FENCE_RE.finditer(text, h.end())]
        if len(fences) < 2:
            raise RegionError("blocco ``` del changelog non trovato dopo §8")
        start = fences[0].start()
        end = text.find("\n", fences[1].end()) + 1
        text = text[:start] + wrap("changelog", text[start:end]) + "\n" + text[end:]
        added.append("changelog")

    return text, added


# ------------------------------------------------------------------ apply


def apply_march_clock(text: str, new_day: int, session_label: str) -> str:
    content = (
        f"**Current March Day:** **{new_day}** "
        f"(aggiornato da `state_apply` — {session_label}).\n"
        f"**Days remaining to Rethmar:** **{RETHMAR_DAY - new_day}** "
        f"(arrivo dell'orda a Rethmar: Day {RETHMAR_DAY}).\n"
    )
    return replace_region(text, "march-clock", content)


def append_changelog(text: str, line: str) -> str:
    regions = find_regions(text)
    if "changelog" not in regions:
        raise RegionError("regione 'changelog' assente — lancia --migrate")
    content = regions["changelog"].content(text)
    fences = list(FENCE_RE.finditer(content))
    if len(fences) < 2:
        raise RegionError("regione changelog malformata (fence ``` mancanti)")
    close = fences[-1].start()
    new_content = content[:close] + line.rstrip("\n") + "\n" + content[close:]
    return replace_region(text, "changelog", new_content)


def _diff(old: str, new: str, label: str) -> str:
    return "".join(difflib.unified_diff(
        old.splitlines(keepends=True), new.splitlines(keepends=True),
        fromfile=f"a/{label}", tofile=f"b/{label}", n=2))


def _confirm(prompt: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    try:
        return input(f"{prompt} [s/N] ").strip().lower() in ("s", "y", "si", "sì", "yes")
    except EOFError:
        return False


# ------------------------------------------------------------------ main


def run(repo: Path, session_name: "str | None", check: bool, assume_yes: bool,
        do_commit: bool, no_guard: bool) -> int:
    state_path = repo / STATE_REL
    sessions = repo / SESSIONS_REL

    if not no_guard:
        group = cfg.load_group(repo)
        try:
            gitio.guard_canon_branch(
                repo, expected=cfg.group_branch(group) if group else None)
        except gitio.BranchGuardError as exc:
            print(f"[apply] ✗ {exc}", file=sys.stderr)
            return 1
        if not check:
            import subprocess
            dirty = subprocess.run(
                ["git", "-C", str(repo), "status", "--porcelain", "--", str(STATE_REL)],
                capture_output=True, text=True).stdout.strip()
            if dirty:
                print("[apply] ✗ campaign/state.md ha modifiche non committate: "
                      "committa (o scarta) prima, così l'undo resta `git revert` "
                      "(ADR-0007 vincolo 4)", file=sys.stderr)
                return 1

    if session_name:
        spath = sessions / session_name
        if not spath.exists():
            print(f"[apply] ✗ sessione non trovata: {spath}", file=sys.stderr)
            return 2
    else:
        cands = sorted(sessions.glob("????-??-??_session-*.md"))
        if not cands:
            print(f"[apply] ✗ nessun log di sessione in {sessions}", file=sys.stderr)
            return 2
        spath = cands[-1]
    ev = extract_events(spath)
    print(f"[apply] sessione: {ev['file']} ({ev['date']}) — trigger: {len(ev['hits'])}")

    text = state_path.read_text(encoding="utf-8")
    original = text
    applied: list[str] = []
    manual: list[str] = []
    session_label = f"sessione {ev['date']} ({ev['file']})"

    for name, raw, groups in ev["hits"]:
        if name == "march_clock":
            a, b = int(groups[0]), int(groups[1])
            if a == b:
                continue
            try:
                candidate = apply_march_clock(text, b, session_label)
            except RegionError as exc:
                print(f"[apply] ⚠ march_clock non applicabile ({exc}) — resta manuale")
                manual.append(_suggest(name, groups))
                continue
            if candidate == text:
                print(f"[apply] march-clock già a Day {b} — niente da fare (idempotente)")
                continue
            print(f"\n[apply] proposta march-clock: Day {a} → Day {b}")
            print(_diff(text, candidate, str(STATE_REL)) or "  (nessuna differenza)")
            if _confirm("[apply] applico questo blocco?", assume_yes):
                text = candidate
                applied.append(f"March Clock Day {a} → Day {b}")
            else:
                manual.append(_suggest(name, groups))
        elif name == "ritual_clock" and groups[0] == groups[1]:
            continue  # nessun cambiamento: niente rumore
        else:
            manual.append(_suggest(name, groups))

    if applied:
        entry = (f"{date.today().isoformat()}  {session_label}: "
                 + "; ".join(applied) + " (state_apply).")
        try:
            candidate = append_changelog(text, entry)
            print("\n[apply] proposta changelog §8:")
            print(_diff(text, candidate, str(STATE_REL)))
            if _confirm("[apply] appendo al changelog?", assume_yes):
                text = candidate
        except RegionError as exc:
            print(f"[apply] ⚠ changelog non applicabile ({exc}) — aggiorna §8 a mano")

    if manual:
        print("\n[apply] proposte NON meccaniche — applicale a mano in state.md:")
        for line in manual:
            print(line)

    if text == original:
        print("\n[apply] ✓ niente da scrivere (già allineato o tutto rifiutato)")
        return 0
    if check:
        print("\n[apply] --check: nessuna scrittura eseguita")
        return 0

    state_path.write_text(text, encoding="utf-8")
    print(f"\n[apply] ✓ scritto {state_path}")
    if do_commit:
        sha = gitio.commit_paths(
            repo, [str(STATE_REL)],
            f"state: {'; '.join(applied) or 'sync'} — {session_label} [state_apply]")
        print(f"[apply] ✓ commit {sha}" if sha else "[apply] (nulla da committare)")
    else:
        print("[apply] ricordati il commit: git add campaign/state.md && git commit")
    return 0


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(
        description="Applica le proposte meccaniche a state.md dentro le "
                    "regioni marcate auto: (ADR-0007).")
    ap.add_argument("--migrate", action="store_true",
                    help="inserisce i marker auto: in state.md (idempotente)")
    ap.add_argument("--session", help="file sotto campaign/sessions/ (default: l'ultimo)")
    ap.add_argument("--check", action="store_true", help="solo diff, nessuna scrittura")
    ap.add_argument("--yes", action="store_true", help="applica senza chiedere conferma")
    ap.add_argument("--commit", action="store_true", help="committa state.md dopo l'applicazione")
    ap.add_argument("--no-guard", action="store_true",
                    help="salta guardia branch e check working-tree (SOLO test)")
    ap.add_argument("--repo-root", type=Path, default=REPO, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    repo = args.repo_root.resolve()

    if args.migrate:
        state_path = repo / STATE_REL
        text = state_path.read_text(encoding="utf-8")
        try:
            new_text, added = migrate(text)
        except RegionError as exc:
            print(f"[apply] ✗ migrazione fallita: {exc}", file=sys.stderr)
            return 1
        if not added:
            print("[apply] ✓ marker già presenti — niente da fare")
            return 0
        if args.check:
            print(_diff(text, new_text, str(STATE_REL)))
            print("[apply] --check: nessuna scrittura eseguita")
            return 0
        if not args.no_guard:
            group = cfg.load_group(repo)
            try:
                gitio.guard_canon_branch(
                    repo, expected=cfg.group_branch(group) if group else None)
            except gitio.BranchGuardError as exc:
                print(f"[apply] ✗ {exc}", file=sys.stderr)
                return 1
        state_path.write_text(new_text, encoding="utf-8")
        print(f"[apply] ✓ marker inseriti: {', '.join(added)}")
        if args.commit:
            sha = gitio.commit_paths(repo, [str(STATE_REL)],
                                     "state: migrazione marker auto: (ADR-0007)")
            print(f"[apply] ✓ commit {sha}" if sha else "[apply] (nulla da committare)")
        return 0

    return run(repo, args.session, args.check, args.yes, args.commit, args.no_guard)


if __name__ == "__main__":
    raise SystemExit(main())
