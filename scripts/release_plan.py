#!/usr/bin/env python3
"""
release_plan.py — cosa rilascia il workflow Release, e su quale commit (ADR-0100).

Ripreso da iemod-fetch (tools/release_plan.py, ADR-0027 di quel progetto, MIT,
stesso autore). La sezione `## [X.Y.Z]` più recente del CHANGELOG.md di
progetto, alla radice del repo, dà la versione. Il tag `vX.Y.Z` va sul commit
della linea principale (first-parent) in cui `scripts/dmcore/__init__.py` dice
per la prima volta `__version__ = "X.Y.Z"`, cioè l'unione della PR di rilascio:
dentro ci sono tutte le correzioni fatte in revisione, e niente di ciò che è
entrato dopo. Un tag che esiste già vuol dire «già rilasciato».

Se dopo quel commit non è cambiato niente di ciò che il rilascio impacchetta,
si rilascia la testa di main: gli stessi pacchetti, ed è il solo commit che
GITHUB_TOKEN può sempre etichettare (un token senza il permesso `workflows`
non può creare un ref i cui workflow differiscono da quelli del ramo
principale). Quando non si può evitare, lo dice `workflows_differ=true`, e il
workflow spiega cosa fare invece di fallire con un 403 muto.

    python3 scripts/release_plan.py [VERSIONE]
    python3 scripts/release_plan.py --pull-request

Stampa le righe `release=`, `tag=`, `sha=` e `workflows_differ=` per
$GITHUB_OUTPUT. Senza VERSIONE usa la sezione più recente del CHANGELOG.
`--pull-request` prepara la prova generale sul commit della PR stessa.

Exit: 0 ok · 1 la versione non è mai stata scritta nel file di versione ·
2 errore d'uso. Solo stdlib.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

VERSION_FILE = "scripts/dmcore/__init__.py"
CHANGELOG = "CHANGELOG.md"
# Ciò che il rilascio impacchetta: le skill (build-skills.sh) e ciò che le
# costruisce. Un cambio solo di piani, CI o contenuti di gioco non cambia
# i pacchetti.
SHIPPED = ("skills", "scripts/build-skills.sh", "scripts/compress_skills.py",
           "scripts/index_skills.py",
           "requirements.txt", "LICENSE", "LICENSES.md", "OGL.txt")
WORKFLOWS = ".github/workflows"
_SECTION = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)
_SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
_VERSION = re.compile(r'^__version__ = "(\d+\.\d+\.\d+)"', re.MULTILINE)


def newest_release(changelog: str) -> str | None:
    """La prima sezione con un numero; `[Non rilasciato]` non è un rilascio."""
    m = _SECTION.search(changelog)
    return m.group(1) if m else None


def current_version(text: str) -> str | None:
    m = _VERSION.search(text)
    return m.group(1) if m else None


def _git(repo: str, *args: str) -> str:
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def release_commit(repo: str, version: str) -> str | None:
    """Il commit first-parent più vecchio in cui il file di versione dice `version`."""
    commits = _git(repo, "rev-list", "--first-parent", "--reverse", "HEAD",
                   "--", VERSION_FILE).split()
    for sha in commits:
        text = subprocess.run(["git", "-C", repo, "show", f"{sha}:{VERSION_FILE}"],
                              capture_output=True, text=True, check=False).stdout
        if current_version(text) == version:
            return sha
    return None


def _same(repo: str, left: str, right: str, *paths: str) -> bool:
    return subprocess.run(["git", "-C", repo, "diff", "--quiet", left, right,
                           "--", *paths], check=False).returncode == 0


def plan(repo: str, version: str, explicit: bool = False) -> dict[str, str]:
    """`explicit`: chiesta per numero, quindi un tag esistente si rilascia com'è."""
    tag = f"v{version}"
    found = subprocess.run(["git", "-C", repo, "rev-parse", "-q", "--verify",
                            f"refs/tags/{tag}^{{commit}}"], capture_output=True,
                           text=True, check=False)
    if found.returncode == 0:
        if explicit:
            return {"release": "true", "tag": tag, "sha": found.stdout.strip(),
                    "workflows_differ": "false"}
        return {"release": "false", "tag": tag, "sha": "", "workflows_differ": "false"}
    sha = release_commit(repo, version)
    if sha is None:
        raise SystemExit(f"{VERSION_FILE} non dice mai __version__ = \"{version}\" sulla "
                         "linea principale: la versione si alza insieme al CHANGELOG")
    head = _git(repo, "rev-parse", "HEAD")
    if _same(repo, sha, head, *SHIPPED):
        sha = head
    differ = not _same(repo, sha, head, WORKFLOWS)
    return {"release": "true", "tag": tag, "sha": sha,
            "workflows_differ": "true" if differ else "false"}


def pull_request(repo: str) -> dict[str, str]:
    """La prova generale su una PR: il suo commit, con la sua versione.

    Costruzione sì, pubblicazione mai. Così un cambio al workflow di rilascio,
    anche di Dependabot, si prova prima di entrare.
    """
    with open(os.path.join(repo, VERSION_FILE), encoding="utf-8") as fh:
        version = current_version(fh.read())
    if version is None:
        raise SystemExit(f"nessun __version__ in {VERSION_FILE}")
    return {"release": "true", "tag": f"v{version}",
            "sha": _git(repo, "rev-parse", "HEAD"), "workflows_differ": "false"}


def main(argv: list[str]) -> int:
    if argv[1:] in (["--help"], ["-h"]):
        print(__doc__)
        return 0
    if argv[1:] == ["--pull-request"]:
        planned = pull_request(".")
    elif len(argv) == 2:
        version = argv[1].lstrip("v")
        if not _SEMVER.match(version):
            print(f"non è una versione: {argv[1]!r}", file=sys.stderr)
            return 2
        planned = plan(".", version, explicit=True)
    elif len(argv) == 1:
        with open(CHANGELOG, encoding="utf-8") as fh:
            version = newest_release(fh.read())
        if version is None:
            print("release=false")
            return 0
        planned = plan(".", version)
    else:
        print(__doc__, file=sys.stderr)
        return 2
    for key, value in planned.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
