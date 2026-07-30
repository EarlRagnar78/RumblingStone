#!/usr/bin/env python3
"""
tools_manifest.py — fonte di verita' -> artefatti derivati per i tool del repo.

La fonte di verita' e' ``scripts/tools.manifest.json`` (un array di descrittori
conformi a ``scripts/schemas/tool_manifest.schema.json``). Questo script:

  * VALIDA il manifest contro lo schema (subset pragmatico, stdlib-only) e
    verifica che ogni script del repo sia coperto (nessun tool "orfano");
  * GENERA gli artefatti che consumano altri tool/umani:
      - ``docs/tools/registry.json``   (registro machine-readable, ordinato)
      - ``docs/tools/README.md``       (tabelle categorizzate, leggibili)
      - ``docs/tools/mcp-tools.json``  (vista in stile MCP tool-definitions)

Uso:
    python3 scripts/tools_manifest.py --check       # gate CI (non scrive)
    python3 scripts/tools_manifest.py --emit-all    # rigenera tutti gli artefatti
    python3 scripts/tools_manifest.py --render-md    # solo docs/tools/README.md
    python3 scripts/tools_manifest.py --emit-mcp     # solo docs/tools/mcp-tools.json

Exit code (convenzione repo — vedi docs/guides/TOOL-AUTHORING-STANDARD.md):
    0 = ok
    1 = manifest non conforme / drift rilevato (--check)
    2 = errore d'uso

Dipendenze: solo stdlib (implementazione di riferimento dello standard).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
MANIFEST = SCRIPTS / "tools.manifest.json"
SCHEMA = SCRIPTS / "schemas" / "tool_manifest.schema.json"
OUT_DIR = REPO / "docs" / "tools"

GEN_HEADER_MD = (
    "<!-- AUTO-GENERATO da scripts/tools_manifest.py — non modificare a mano.\n"
    "     Fonte: scripts/tools.manifest.json. Rigenera: "
    "python3 scripts/tools_manifest.py --emit-all -->\n"
)

CATEGORY_TITLES = {
    "A-session-prep": "A · Session Prep (incontri · mappe · tesoro)",
    "B-maps-pipeline": "B · Maps Pipeline (render · import · export · validate)",
    "C-post-session-canon": "C · Post-Session Canon (XP · state.md · branch)",
    "D-materials": "D · Materiali giocatore / DM (Homebrewery V3)",
    "E-bestiary-catalog": "E · Bestiario / Catalogo mostri",
    "F-skill-pipeline": "F · Pipeline skill multi-agente",
    "G-orchestration-governance": "G · Orchestrazione & Governance",
    "H-local-infra": "H · Infrastruttura locale (opt-in)",
    "I-converters": "I · Convertitori di contenuto",
    "J-data-assets": "J · Dati & Schemi",
    "lib": "Librerie (non-CLI)",
    "tests": "Test",
}
CATEGORY_ORDER = list(CATEGORY_TITLES.keys())


# --------------------------------------------------------------------------- #
# Caricamento
# --------------------------------------------------------------------------- #
def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[tools_manifest] file mancante: {path}", file=sys.stderr)
        raise SystemExit(2)
    except json.JSONDecodeError as e:
        print(f"[tools_manifest] JSON non valido in {path}: {e}", file=sys.stderr)
        raise SystemExit(2)


def load_manifest():
    data = _load_json(MANIFEST)
    if not isinstance(data, dict) or "tools" not in data:
        print("[tools_manifest] manifest privo della chiave 'tools'", file=sys.stderr)
        raise SystemExit(2)
    return data


def _enum(schema: dict, *path: str):
    """Estrae una lista enum annidata dallo schema (mantiene gli enum in sync)."""
    node = schema.get("properties", {})
    for i, key in enumerate(path):
        node = node.get(key, {})
        if i < len(path) - 1:
            # scendi in items/properties a seconda della struttura
            if "items" in node:
                node = node["items"].get("properties", {})
            else:
                node = node.get("properties", {})
    return node.get("enum")


# --------------------------------------------------------------------------- #
# Validazione (subset pragmatico dello JSON Schema, stdlib-only)
# --------------------------------------------------------------------------- #
def validate(manifest: dict, schema: dict) -> list[str]:
    errors: list[str] = []
    required = schema.get("required", [])
    cat_enum = schema["properties"]["category"]["enum"]
    lang_enum = schema["properties"]["language"]["enum"]
    stab_enum = schema["properties"]["stability"]["enum"]
    arg_type_enum = schema["properties"]["args"]["items"]["properties"]["type"]["enum"]
    in_kind_enum = schema["properties"]["inputs"]["items"]["properties"]["kind"]["enum"]
    out_kind_enum = schema["properties"]["outputs"]["items"]["properties"]["kind"]["enum"]
    id_pat = re.compile(schema["properties"]["id"]["pattern"])

    seen_ids: set[str] = set()
    for i, t in enumerate(manifest["tools"]):
        tid = t.get("id", f"<voce #{i}>")
        for field in required:
            if field not in t:
                errors.append(f"{tid}: campo obbligatorio mancante '{field}'")
        if "id" in t:
            if not id_pat.match(t["id"]):
                errors.append(f"{tid}: id non conforme al pattern")
            if t["id"] in seen_ids:
                errors.append(f"{tid}: id duplicato")
            seen_ids.add(t["id"])
        if t.get("category") not in cat_enum:
            errors.append(f"{tid}: category '{t.get('category')}' fuori enum")
        if t.get("language") not in lang_enum:
            errors.append(f"{tid}: language '{t.get('language')}' fuori enum")
        if t.get("stability") not in stab_enum:
            errors.append(f"{tid}: stability '{t.get('stability')}' fuori enum")
        for b in ("stdlib_only", "idempotent"):
            if b in t and not isinstance(t[b], bool):
                errors.append(f"{tid}: '{b}' deve essere booleano")
        # args
        for a in t.get("args", []):
            if a.get("type") not in arg_type_enum:
                errors.append(f"{tid}: arg '{a.get('name')}' type '{a.get('type')}' fuori enum")
            for f in ("name", "type", "required", "desc"):
                if f not in a:
                    errors.append(f"{tid}: arg '{a.get('name')}' privo di '{f}'")
        # inputs / outputs
        for inp in t.get("inputs", []):
            if inp.get("kind") not in in_kind_enum:
                errors.append(f"{tid}: input kind '{inp.get('kind')}' fuori enum")
        for out in t.get("outputs", []):
            if out.get("kind") not in out_kind_enum:
                errors.append(f"{tid}: output kind '{out.get('kind')}' fuori enum")
        # blocchi obbligatori annidati
        det = t.get("determinism")
        if not isinstance(det, dict) or "deterministic" not in det:
            errors.append(f"{tid}: 'determinism.deterministic' mancante")
        fx = t.get("side_effects")
        if not isinstance(fx, dict) or not {"writes_canon", "git_commit", "network"} <= set(fx or {}):
            errors.append(f"{tid}: 'side_effects' incompleto (servono writes_canon/git_commit/network)")
        # il file esiste?
        p = REPO / t.get("path", "")
        if t.get("path") and not p.exists():
            errors.append(f"{tid}: path inesistente '{t.get('path')}'")
    return errors


def coverage(manifest: dict) -> list[str]:
    """Verifica che ogni script eseguibile del repo sia nel manifest."""
    problems: list[str] = []
    covered = {t["path"] for t in manifest["tools"]}
    # script Python e shell sotto scripts/ (escludendo Old/, dmcore interni,
    # tests/, e questo stesso generatore che e' nel manifest)
    for p in sorted(SCRIPTS.glob("*.py")):
        rel = str(p.relative_to(REPO))
        if rel not in covered:
            problems.append(f"scoperto (nessun manifest): {rel}")
    for p in sorted(SCRIPTS.glob("*.sh")):
        rel = str(p.relative_to(REPO))
        if rel not in covered:
            problems.append(f"scoperto (nessun manifest): {rel}")
    return problems


def check_help_flags(manifest: dict) -> list[str]:
    """Cross-check morbido: per i tool Python 'stable', verifica che i flag
    dichiarati compaiano nel testo di --help (rileva doc che mente)."""
    import subprocess

    warnings: list[str] = []
    for t in manifest["tools"]:
        if t.get("language") != "python" or t.get("stability") != "stable":
            continue
        # i flag dei subcomandi non compaiono nell'--help top-level: salta
        if any(a.get("type") == "subcommand" for a in t.get("args", [])):
            continue
        path = REPO / t["path"]
        if not path.exists():
            continue
        try:
            out = subprocess.run(
                [sys.executable, str(path), "--help"],
                capture_output=True, text=True, timeout=30, cwd=str(REPO),
            )
        except Exception as e:  # pragma: no cover - ambiente
            warnings.append(f"{t['id']}: impossibile eseguire --help ({e})")
            continue
        help_text = (out.stdout or "") + (out.stderr or "")
        if out.returncode != 0:
            warnings.append(f"{t['id']}: '--help' esce con codice {out.returncode}")
        for a in t.get("args", []):
            name = a["name"]
            if a["type"] in ("subcommand",) or "/" in name or " " in name:
                continue  # positional/subcommand: match troppo fragile
            flag = name.split("/")[0]
            if flag.startswith("--") and flag not in help_text:
                warnings.append(f"{t['id']}: flag '{flag}' assente da --help")
    return warnings


# --------------------------------------------------------------------------- #
# Generazione artefatti
# --------------------------------------------------------------------------- #
def _sorted_tools(manifest: dict):
    def key(t):
        try:
            ci = CATEGORY_ORDER.index(t["category"])
        except ValueError:
            ci = len(CATEGORY_ORDER)
        return (ci, t["id"])
    return sorted(manifest["tools"], key=key)


def emit_registry(manifest: dict) -> str:
    reg = {
        "generated_by": "scripts/tools_manifest.py",
        "source": "scripts/tools.manifest.json",
        "manifest_version": manifest.get("manifest_version"),
        "tool_count": len(manifest["tools"]),
        "tools": _sorted_tools(manifest),
    }
    return json.dumps(reg, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def emit_mcp(manifest: dict) -> str:
    """Vista in stile MCP tool-definitions (name/description/inputSchema)."""
    _TMAP = {"int": "integer", "float": "number", "bool": "boolean",
             "path": "string", "str": "string", "choice": "string",
             "subcommand": "string"}
    tools = []
    for t in _sorted_tools(manifest):
        if t["category"] in ("lib", "tests", "J-data-assets"):
            continue
        props, required = {}, []
        for a in t.get("args", []):
            key = a["name"].split("/")[0].lstrip("-").replace(" ", "_") or a["name"]
            schema = {"type": _TMAP.get(a["type"], "string"), "description": a["desc"]}
            if a.get("choices"):
                schema["enum"] = a["choices"]
            props[key] = schema
            if a.get("required"):
                required.append(key)
        tools.append({
            "name": t["id"].replace("/", "_").replace("-", "_"),
            "description": t["summary"],
            "invocation": t["invocation"],
            "inputSchema": {
                "type": "object",
                "properties": props,
                "required": required,
                "additionalProperties": False,
            },
            "outputs": [o["path"] for o in t.get("outputs", [])],
            "exit_codes": t.get("exit_codes", {}),
            "deterministic": t.get("determinism", {}).get("deterministic"),
        })
    return json.dumps(
        {"generated_by": "scripts/tools_manifest.py", "tools": tools},
        indent=2, ensure_ascii=False,
    ) + "\n"


def _md_flags(t: dict) -> str:
    parts = []
    for a in t.get("args", []):
        tag = a["name"]
        if a.get("required"):
            tag = f"**{tag}**"
        parts.append(tag)
    return " · ".join(parts) if parts else "—"


def _md_bool(b) -> str:
    return "✔" if b else "—"


def emit_markdown(manifest: dict) -> str:
    lines = [GEN_HEADER_MD, "# Registro dei tool — RumblingStone", "",
             "> Vista umana del contratto machine-readable "
             "[`registry.json`](registry.json). "
             "Fonte di verita': `scripts/tools.manifest.json`.", "",
             f"**{len(manifest['tools'])} tool** · convenzione exit code "
             "`0=ok · 1=errore-dominio · 2=errore-uso`.", ""]
    by_cat: dict[str, list] = {}
    for t in _sorted_tools(manifest):
        by_cat.setdefault(t["category"], []).append(t)
    for cat in CATEGORY_ORDER:
        tools = by_cat.get(cat)
        if not tools:
            continue
        lines.append(f"## {CATEGORY_TITLES[cat]}")
        lines.append("")
        lines.append("| Tool | Scopo | Parametri | Determ. | Canone | Git | Exit |")
        lines.append("|---|---|---|:--:|:--:|:--:|---|")
        for t in tools:
            det = _md_bool(t.get("determinism", {}).get("deterministic"))
            canon = _md_bool(t.get("side_effects", {}).get("writes_canon"))
            git = _md_bool(t.get("side_effects", {}).get("git_commit"))
            exits = " · ".join(f"`{k}`" for k in sorted(t.get("exit_codes", {}), key=int))
            lines.append(
                f"| `{t['path'].split('/')[-1] or t['id']}` | {t['summary']} "
                f"| {_md_flags(t)} | {det} | {canon} | {git} | {exits or '—'} |"
            )
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("Aggiungere un tool? Vedi "
                 "[`../guides/TOOL-AUTHORING-STANDARD.md`](../guides/TOOL-AUTHORING-STANDARD.md).")
    lines.append("")
    return "\n".join(lines)


def write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="gate CI: valida manifest + copertura + coerenza flag; non scrive")
    ap.add_argument("--emit-all", action="store_true", help="rigenera tutti gli artefatti")
    ap.add_argument("--render-md", action="store_true", help="rigenera solo docs/tools/README.md")
    ap.add_argument("--emit-mcp", action="store_true", help="rigenera solo docs/tools/mcp-tools.json")
    ap.add_argument("--strict-help", action="store_true",
                    help="con --check, il cross-check flag/--help diventa fatale")
    args = ap.parse_args(argv)

    manifest = load_manifest()
    schema = _load_json(SCHEMA)

    if args.check:
        errors = validate(manifest, schema)
        errors += coverage(manifest)
        warnings = check_help_flags(manifest)
        for w in warnings:
            print(f"  ⚠ {w}", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        if args.strict_help:
            errors += warnings
        if errors:
            print(f"✗ tools_manifest: {len(errors)} problema/i", file=sys.stderr)
            return 1
        print(f"✓ tools_manifest: {len(manifest['tools'])} tool conformi, "
              f"copertura completa ({len(warnings)} warning)")
        return 0

    if not (args.emit_all or args.render_md or args.emit_mcp):
        ap.print_help()
        return 2

    # per generare, il manifest deve essere valido
    errors = validate(manifest, schema)
    if errors:
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        print("✗ tools_manifest: manifest non valido, generazione annullata", file=sys.stderr)
        return 1

    changed = []
    if args.emit_all or args.render_md:
        if write_if_changed(OUT_DIR / "README.md", emit_markdown(manifest)):
            changed.append("docs/tools/README.md")
    if args.emit_all:
        if write_if_changed(OUT_DIR / "registry.json", emit_registry(manifest)):
            changed.append("docs/tools/registry.json")
    if args.emit_all or args.emit_mcp:
        if write_if_changed(OUT_DIR / "mcp-tools.json", emit_mcp(manifest)):
            changed.append("docs/tools/mcp-tools.json")

    if changed:
        print("✓ aggiornati: " + ", ".join(changed))
    else:
        print("✓ nessuna modifica (artefatti gia' allineati)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
