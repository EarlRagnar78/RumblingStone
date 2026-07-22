"""
config — configurazione del gruppo di campagna (`campaign/group.yaml`).

Formato volutamente minimale (subset YAML "chiave: valore", commenti con
`#`), così restiamo stdlib-only come il resto del toolkit. Esempio:

    # Gruppo attivo di questa working copy (piano AUTOMAZIONE §3)
    group: rumblingstone-dm-gianfranco

Il branch di canone corrispondente è `campaign-group-<group>` — lo stesso
schema di `scripts/new-campaign-group.sh` (Playbook §7).
"""

from __future__ import annotations

from pathlib import Path

GROUP_FILE = Path("campaign") / "group.yaml"
BRANCH_PREFIX = "campaign-group-"


class ConfigError(RuntimeError):
    pass


def _parse_kv(text: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            raise ConfigError(f"riga non valida in group.yaml: {raw!r}")
        key, val = line.split(":", 1)
        data[key.strip()] = val.strip().strip("'\"")
    return data


def load_group(repo: Path) -> "str | None":
    """Nome del gruppo configurato, o None se group.yaml non esiste."""
    path = repo / GROUP_FILE
    if not path.exists():
        return None
    data = _parse_kv(path.read_text(encoding="utf-8"))
    group = data.get("group", "")
    if not group:
        raise ConfigError(f"{path}: chiave 'group' mancante o vuota")
    return group


def write_group(repo: Path, group: str) -> Path:
    path = repo / GROUP_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Gruppo di campagna attivo in questa working copy.\n"
        "# Il canone vive sul branch campaign-group-<group> (ADR-0007;\n"
        "# vedi campaign/DM-CAMPAIGN-PLAYBOOK.md §7).\n"
        f"group: {group}\n",
        encoding="utf-8",
    )
    return path


def group_branch(group: str) -> str:
    return f"{BRANCH_PREFIX}{group}"
