#!/usr/bin/env python3
"""
campaign_branch.py — guardia e gestione del branch-per-gruppo (ADR-0007).

Il canone vivo (state.md, sessions/, recaps/, next/) si scrive SOLO sul
branch del gruppo `campaign-group-<nome>`; `main` resta la libreria di
prep condivisa. Questo script è l'unico posto dove vive quella policy:
gli altri script (state_apply, next_session) la importano, dm.py la
orchestra (ADR-0002).

Uso:
    python3 scripts/campaign_branch.py status          # dove sono? posso scrivere canone?
    python3 scripts/campaign_branch.py guard           # exit 1 se il canone NON è scrivibile qui
    python3 scripts/campaign_branch.py ensure          # crea/passa al branch del gruppo
    python3 scripts/campaign_branch.py ensure --group rumblingstone-dm-gianfranco

`ensure` legge il gruppo da `campaign/group.yaml` (o lo scrive, se passato
con --group la prima volta). Non tocca mai la working tree sporca.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore import REPO  # noqa: E402
from dmcore import config as cfg  # noqa: E402
from dmcore import gitio  # noqa: E402


def cmd_status(repo: Path) -> int:
    branch = gitio.current_branch(repo)
    group = cfg.load_group(repo)
    expected = cfg.group_branch(group) if group else None
    print(f"[branch] repo: {repo}")
    print(f"[branch] branch corrente: {branch or '(detached HEAD)'}")
    print(f"[branch] gruppo configurato: {group or '(nessuno — campaign/group.yaml assente)'}")
    if branch in gitio.PROTECTED_BRANCHES:
        print("[branch] ✗ canone NON scrivibile qui (branch protetto, ADR-0007)")
        return 1
    if expected and branch != expected:
        print(f"[branch] ⚠ canone scrivibile, ma il branch del gruppo è '{expected}'")
        return 1
    behind = gitio.behind_main_count(repo)
    if behind:
        print(f"[branch] ⚠ il branch è indietro di {behind} commit rispetto a main "
              f"— valuta `git merge main` (Playbook §7)")
    print("[branch] ✓ canone scrivibile su questo branch")
    return 0


def cmd_guard(repo: Path) -> int:
    group = cfg.load_group(repo)
    try:
        branch = gitio.guard_canon_branch(
            repo, expected=cfg.group_branch(group) if group else None)
    except gitio.BranchGuardError as exc:
        print(f"[branch] ✗ {exc}", file=sys.stderr)
        return 1
    print(f"[branch] ✓ ok: '{branch}'")
    return 0


def cmd_ensure(repo: Path, group_arg: "str | None") -> int:
    group = group_arg or cfg.load_group(repo)
    if not group:
        print("[branch] ✗ nessun gruppo: passa `--group <nome>` la prima volta "
              "(es. --group rumblingstone-dm-gianfranco)", file=sys.stderr)
        return 2
    target = cfg.group_branch(group)
    branch = gitio.current_branch(repo)
    if branch == target:
        pass  # già a posto; sotto scriviamo comunque group.yaml se mancava
    elif gitio.branch_exists(repo, target):
        if not gitio.is_clean(repo):
            print("[branch] ✗ working tree sporca: commit o stash prima di cambiare branch",
                  file=sys.stderr)
            return 1
        gitio.checkout(repo, target)
        print(f"[branch] ✓ checkout di '{target}'")
    else:
        gitio.checkout_new(repo, target)
        print(f"[branch] ✓ creato branch '{target}' da '{branch}'")
    if cfg.load_group(repo) != group:
        path = cfg.write_group(repo, group)
        sha = gitio.commit_paths(repo, [str(path.relative_to(repo))],
                                 f"campaign: configura gruppo '{group}' (group.yaml)")
        if sha:
            print(f"[branch] ✓ campaign/group.yaml scritto e committato ({sha})")
    print(f"[branch] ✓ pronto: canone del gruppo '{group}' su '{target}'")
    return 0


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(
        description="Guardia e gestione del branch-per-gruppo (ADR-0007).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="mostra branch/gruppo e se il canone è scrivibile")
    sub.add_parser("guard", help="exit 1 se il canone non è scrivibile qui")
    p = sub.add_parser("ensure", help="crea/passa al branch del gruppo")
    p.add_argument("--group", help="nome gruppo (solo la prima volta; poi da group.yaml)")
    args = ap.parse_args(argv)
    repo = REPO
    if args.cmd == "status":
        return cmd_status(repo)
    if args.cmd == "guard":
        return cmd_guard(repo)
    return cmd_ensure(repo, args.group)


if __name__ == "__main__":
    raise SystemExit(main())
