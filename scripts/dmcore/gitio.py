"""
gitio — helper git per il toolkit DM (ADR-0007 vincoli 1 e 4).

La guardia di branch è il cuore: nessuno script che scrive canone può
farlo su `main` (o sui branch protetti). I commit automatici pre/post
applicazione rendono ogni scrittura reversibile con `git revert`.

Solo stdlib (subprocess); ogni funzione accetta `repo` esplicito così i
test lavorano su repository temporanei senza toccare quello reale.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

#: Branch su cui le scritture di canone sono SEMPRE vietate (ADR-0007).
PROTECTED_BRANCHES = ("main", "master")


class BranchGuardError(RuntimeError):
    """Scrittura di canone tentata su un branch protetto."""


def _git(repo: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def current_branch(repo: Path) -> str:
    return _git(repo, "branch", "--show-current")


def branch_exists(repo: Path, name: str) -> bool:
    rc = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet",
         f"refs/heads/{name}"],
        capture_output=True,
    ).returncode
    return rc == 0


def is_clean(repo: Path) -> bool:
    return _git(repo, "status", "--porcelain") == ""


def guard_canon_branch(repo: Path, expected: "str | None" = None) -> str:
    """Verifica il vincolo 1 di ADR-0007. Ritorna il branch corrente.

    - su un branch protetto → BranchGuardError (mai scrivere canone lì);
    - se `expected` è dato e non coincide → BranchGuardError con istruzioni.
    """
    branch = current_branch(repo)
    if branch in PROTECTED_BRANCHES:
        raise BranchGuardError(
            f"sei su '{branch}': le scritture di canone sono vietate qui "
            f"(ADR-0007). Crea/passa al branch del gruppo con "
            f"`python3 scripts/campaign_branch.py ensure`.")
    if expected and branch != expected:
        raise BranchGuardError(
            f"sei su '{branch}' ma il branch del gruppo configurato è "
            f"'{expected}' (campaign/group.yaml). Passa al branch giusto "
            f"o aggiorna la configurazione.")
    return branch


def checkout_new(repo: Path, name: str, start_point: "str | None" = None) -> None:
    args = ["checkout", "-b", name]
    if start_point:
        args.append(start_point)
    _git(repo, *args)


def checkout(repo: Path, name: str) -> None:
    _git(repo, "checkout", name)


def commit_paths(repo: Path, paths: list[str], message: str) -> "str | None":
    """Committa SOLO i path indicati. Ritorna lo sha abbreviato, o None se
    non c'era nulla da committare (idempotenza)."""
    _git(repo, "add", "--", *paths)
    staged = _git(repo, "diff", "--cached", "--name-only", "--", *paths)
    if not staged:
        return None
    _git(repo, "commit", "-m", message, "--", *paths)
    return _git(repo, "rev-parse", "--short", "HEAD")


def behind_main_count(repo: Path, branch: "str | None" = None,
                      main: str = "main") -> "int | None":
    """Quanti commit di `main` mancano al branch (drift, piano §4).
    None se il conteggio non è possibile (es. main assente)."""
    try:
        ref = branch or "HEAD"
        return int(_git(repo, "rev-list", "--count", f"{ref}..{main}"))
    except (subprocess.CalledProcessError, ValueError):
        return None
