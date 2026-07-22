#!/usr/bin/env python3
"""
dm.py — CLI unica del DM RumblingStone (orchestratore, MAI logica).

Un solo punto d'ingresso per il flusso pre/durante/post sessione del
DM-CAMPAIGN-PLAYBOOK. Ogni sottocomando invoca gli script esistenti in
`scripts/` senza duplicarne una riga (ADR-0002); gli script restano
invocabili singolarmente. Solo stdlib; idempotente. Le scritture di canone
(`campaign/state.md`) avvengono SOLO via `session end` → `state_apply.py`,
col triplo vincolo di ADR-0007: branch di gruppo (mai main), conferma
diff del DM, regioni marcate `auto:`.

Sottocomandi (fase del Playbook tra parentesi):
    prep      (§2)   catalogo → incontri → mappa → loot per la prossima sessione
    maps      (prep) render SVG / valida le griglie emoji
    post      (§4)   ledger XP → proposta diff state.md → checklist §4
    session   (§4+§7) ciclo su branch-per-gruppo (ADR-0007): end/next/status/branch
    recap     (§4.6) recap spoiler-safe per i player (+ --hype → Homebrewery)
    handout   (prep) handout giocatori in markdown Homebrewery V3
    skills    (manutenzione) build/sync pipeline skill multi-agente
    doctor    (tutte) diagnosi ambiente e freschezza del catalogo

Esempi:
    python3 scripts/dm.py prep --el 13 --env forest --factions red-hand
    python3 scripts/dm.py maps validate
    python3 scripts/dm.py post --session 2026-05-03_session-3.md
    python3 scripts/dm.py recap --hype
    python3 scripts/dm.py handout --tipo lettera --da bozza.md
    python3 scripts/dm.py doctor

I flag non riconosciuti da `prep`/`recap` vengono inoltrati allo script
sottostante (es. `--seed`, `--narrative`): vedi `<script>.py --help`.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO = SCRIPTS.parent
CATALOG = SCRIPTS / "monster_catalog.yaml"
CATALOG_STALE_DAYS = 7  # oltre → suggerisce il refresh

# ---------------------------------------------------------------- helpers


def run(script: str, *args: str, check: bool = True) -> int:
    """Esegue uno script del toolkit col medesimo interprete Python."""
    path = SCRIPTS / script
    if not path.exists():
        print(f"[dm] ✗ script mancante: {path}", file=sys.stderr)
        return 1
    if script.endswith(".sh"):
        cmd = ["bash", str(path), *args]
    else:
        cmd = [sys.executable, str(path), *args]
    print(f"[dm] → {' '.join(cmd[1:] if cmd[0] != 'bash' else cmd)}")
    rc = subprocess.call(cmd, cwd=REPO)
    if check and rc != 0:
        print(f"[dm] ✗ {script} è uscito con codice {rc}", file=sys.stderr)
    return rc


def catalog_age_days() -> float | None:
    if not CATALOG.exists():
        return None
    return (time.time() - CATALOG.stat().st_mtime) / 86400.0


def ensure_catalog(refresh: bool) -> None:
    age = catalog_age_days()
    if refresh or age is None:
        run("build_monster_catalog.py")
    elif age > CATALOG_STALE_DAYS:
        print(f"[dm] ⚠ catalogo mostri vecchio di {age:.0f} giorni — "
              f"rigenera con `dm.py prep --refresh` se hai aggiunto statblock")


# ------------------------------------------------------------ subcommands


def cmd_prep(args: argparse.Namespace, extra: list[str]) -> int:
    ensure_catalog(args.refresh)
    enc = []
    if args.el is not None:
        enc += ["--el", str(args.el)]
    if args.env:
        enc += ["--env", args.env]
    rc = run("suggest_encounter.py", *enc, *extra)
    if args.env:
        rc |= run("suggest_map.py", "--env", args.env)
    else:
        rc |= run("suggest_map.py", "--list")
    if args.el is not None:
        rc |= run("suggest_loot.py", "--el", str(args.el))
    print("[dm] ✓ prep: rivedi le proposte sopra; niente è stato scritto nel canone")
    return rc


def cmd_maps(args: argparse.Namespace, extra: list[str]) -> int:
    if args.action == "validate":
        return run("validate_maps.py", "--repo-root", str(REPO))
    if not args.files:
        print("[dm] uso: dm.py maps render <file.md ...> — file con griglie emoji "
              "(gli SVG finiscono in rendered/ accanto al sorgente)")
        return 2
    return run("render_map_svg.py", *args.files, *extra)


def cmd_post(args: argparse.Namespace, extra: list[str]) -> int:
    rc = run("update_xp.py", *extra)
    sync = ["--session", args.session] if args.session else []
    rc |= run("state_sync.py", *sync)
    print(
        "\n[dm] ✓ post-sessione: XP aggiornati, diff state.md PROPOSTO sopra "
        "(applicalo a mano).\n"
        "[dm] Checklist Playbook §4 rimanente:\n"
        "      1. rinomina il draft in campaign/sessions/YYYY-MM-DD_session-N.md\n"
        "      2. applica il diff a campaign/state.md (§0 dashboard incluso)\n"
        "      3. aggiorna i PNG cambiati (campaign/npcs/ · PNG/)\n"
        "      4. commit & push\n"
        "      5. 1-2 giorni prima della prossima: `dm.py recap --hype`"
    )
    return rc


def cmd_recap(args: argparse.Namespace, extra: list[str]) -> int:
    rec = []
    if args.last_n != 1:
        rec += ["--last-n", str(args.last_n)]
    if args.pdf:
        rec += ["--pdf"]
    rc = run("session_recap.py", *rec, *extra)
    if args.hype and rc == 0:
        rc = run("hype_homebrew.py")
    return rc


def cmd_handout(args: argparse.Namespace, extra: list[str]) -> int:
    ho = ["--handout", args.tipo]
    if args.da:
        ho += ["--da", args.da]
    if args.out:
        ho += ["--out", args.out]
    return run("hype_homebrew.py", *ho, *extra)


def cmd_hype(args: argparse.Namespace, extra: list[str]) -> int:
    # Homebrewery self-hosted (K-B4/K-B5, K-D5): wrapper sui comandi ufficiali
    script = {"setup": "setup.sh", "start": "start.sh",
              "docker": "setup-docker.sh", "docker-stop": "stop-docker.sh"}[args.action]
    return run(f"homebrew-local/{script}", *extra)


def cmd_dossier(args: argparse.Namespace, extra: list[str]) -> int:
    # Dossier DM (K-B7): fotografia di state.md in veste Homebrewery, SOLO DM
    return run("dm_dossier.py", *extra)


def cmd_session(args: argparse.Namespace, extra: list[str]) -> int:
    # Ciclo di vita sessione su branch-per-gruppo (ADR-0007) — solo orchestrazione
    if args.action == "status":
        return run("campaign_branch.py", "status", check=False)
    if args.action == "branch":
        ens = ["--group", args.group] if args.group else []
        return run("campaign_branch.py", "ensure", *ens)
    if args.action == "next":
        nx = []
        if args.last_n != 1:
            nx += ["--last-n", str(args.last_n)]
        if args.hype:
            nx += ["--hype"]
        return run("next_session.py", *nx, *extra)
    if args.action == "recap":
        # recap per-PG (Lotto D): policy in session_recap/dmcore.visibility,
        # veste in hype_homebrew --pg; senza --pg equivale a `dm.py recap`
        rec = ["--pg", args.pg] if args.pg else []
        if args.last_n != 1:
            rec += ["--last-n", str(args.last_n)]
        rc = run("session_recap.py", *rec, *extra)
        if args.hype and rc == 0:
            rc = run("hype_homebrew.py", *(["--pg", args.pg] if args.pg else []))
        return rc
    # action == "end": guardia → (wizard se serve) → ledger XP → apply → residuo
    rc = run("campaign_branch.py", "guard")
    if rc != 0:
        return rc
    if not args.session:
        # nessun log indicato: il wizard lo crea ora (Lotto B); state_apply
        # senza --session prenderà poi proprio l'ultimo file scritto
        rc = run("session_wizard.py")
        if rc != 0:
            return rc
    rc = run("update_xp.py")
    ses = ["--session", args.session] if args.session else []
    if args.yes:
        ses += ["--yes"]
    rc |= run("state_apply.py", *ses, "--commit", *extra)
    print(
        "\n[dm] ✓ session end: ledger XP aggiornato, regioni marcate di "
        "state.md applicate (su conferma) e committate.\n"
        "[dm] Residuo manuale (Playbook §4): prosa/PNG di state.md dalle "
        "proposte sopra, poi `dm.py session next --hype` quando vuoi il "
        "brief della prossima sessione."
    )
    return rc


def cmd_skills(args: argparse.Namespace, extra: list[str]) -> int:
    if args.action == "sync":
        return run("sync-skills.sh", *extra)
    return run("build-skills.sh", "--no-deploy" if args.no_deploy else "", *extra)


def cmd_doctor(args: argparse.Namespace, extra: list[str]) -> int:
    problems = 0

    def ok(label: str) -> None:
        print(f"  ✓ {label}")

    def warn(label: str) -> None:
        nonlocal problems
        problems += 1
        print(f"  ⚠ {label}")

    print(f"[dm] doctor — repo: {REPO}")
    if sys.version_info >= (3, 8):
        ok(f"python {sys.version.split()[0]}")
    else:
        warn(f"python {sys.version.split()[0]} — serve ≥ 3.8")

    for rel in ("campaign/state.md", "campaign/sessions", "campaign/templates",
                "scripts/map_templates", "plans/INDEX.md"):
        (ok if (REPO / rel).exists() else warn)(rel)

    age = catalog_age_days()
    if age is None:
        warn("monster_catalog.yaml assente — lancia `dm.py prep --refresh`")
    elif age > CATALOG_STALE_DAYS:
        warn(f"monster_catalog.yaml vecchio di {age:.0f} giorni")
    else:
        ok(f"monster_catalog.yaml fresco ({age:.1f} giorni)")

    # sessione su branch-per-gruppo (ADR-0007): check informativi, mai fatali
    try:
        sys.path.insert(0, str(SCRIPTS))
        from dmcore import config as _cfg, gitio as _gitio
        from dmcore.regions import find_regions as _find_regions
        _group = _cfg.load_group(REPO)
        _branch = _gitio.current_branch(REPO)
        if _group:
            ok(f"gruppo '{_group}' (campaign/group.yaml)")
            if _branch == _cfg.group_branch(_group):
                ok(f"branch gruppo attivo: {_branch}")
            else:
                print(f"  ○ branch corrente '{_branch}' ≠ branch gruppo "
                      f"'{_cfg.group_branch(_group)}' — ok per la prep, ma "
                      f"`session end` rifiuterà di scrivere canone qui")
        else:
            print("  ○ campaign/group.yaml assente — `dm.py session branch "
                  "--group <nome>` per attivare il flusso ADR-0007")
        _state = REPO / "campaign" / "state.md"
        if _state.exists():
            _regs = _find_regions(_state.read_text(encoding="utf-8"))
            if {"march-clock", "changelog"} <= set(_regs):
                ok("marker auto: presenti in state.md (march-clock, changelog)")
            else:
                print("  ○ marker auto: assenti in state.md — "
                      "`state_apply.py --migrate` sul branch gruppo")
    except Exception as exc:  # doctor non deve mai crashare
        warn(f"check sessione ADR-0007 falliti: {exc}")

    for tool, why in (("pandoc", "recap --pdf"), ("xelatex", "recap --pdf")):
        if shutil.which(tool):
            ok(f"{tool} presente ({why})")
        else:
            print(f"  ○ {tool} assente — opzionale, serve solo per {why}")

    if problems:
        print(f"[dm] doctor: {problems} avvisi")
        return 0 if args.ci else 1
    print("[dm] doctor: tutto ok")
    return 0


# ------------------------------------------------------------------ main


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="dm.py",
        description="CLI unica del DM RumblingStone — orchestra gli script di scripts/ "
                    "per fase del Playbook (prep / post / recap / handout).",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prep", help="Playbook §2: proposte incontro+mappa+loot")
    p.add_argument("--el", type=int, help="EL bersaglio (→ suggest_encounter/loot)")
    p.add_argument("--env", help="ambiente: forest, cave, urban, swamp, ruins, ...")
    p.add_argument("--refresh", action="store_true", help="rigenera il catalogo mostri")

    p = sub.add_parser("maps", help="render SVG / validazione griglie emoji")
    p.add_argument("action", choices=["render", "validate"])
    p.add_argument("files", nargs="*", help="file markdown con griglie (per render)")

    p = sub.add_parser("post", help="Playbook §4: XP ledger + diff state.md proposto")
    p.add_argument("--session", help="scansiona solo questo file di sessione")

    p = sub.add_parser("recap", help="Playbook §4.6: recap spoiler-safe per i player")
    p.add_argument("--last-n", type=int, default=1)
    p.add_argument("--pdf", action="store_true", help="anche PDF A4 (pandoc)")
    p.add_argument("--hype", action="store_true",
                   help="anche versione Homebrewery V3 (campaign/recaps/homebrew/)")

    p = sub.add_parser("handout", help="handout giocatori in Homebrewery V3")
    p.add_argument("--tipo", required=True,
                   choices=["lettera", "profezia", "avviso-torneo", "scheda-artefatto"])
    p.add_argument("--da", help="file markdown sorgente col contenuto")
    p.add_argument("--out", help="file di output (default: accanto al sorgente)")

    p = sub.add_parser("hype", help="Homebrewery self-hosted locale (editor 2 pannelli su localhost:8000)")
    p.add_argument("action", choices=["setup", "start", "docker", "docker-stop"],
                   help="setup/start = via nativa (node+mongo); docker = container "
                        "chiavi-in-mano col compose ufficiale; docker-stop = ferma i container")

    sub.add_parser("dossier", help="⚠️ SOLO DM: dossier di tutte le trame (da state.md) in Homebrewery V3")

    p = sub.add_parser("session",
                       help="ciclo sessione su branch-per-gruppo (ADR-0007): "
                            "end / next / status / branch")
    p.add_argument("action", choices=["end", "next", "recap", "status", "branch"])
    p.add_argument("--session", help="(end) file di sessione sotto campaign/sessions/; "
                                     "se assente parte il wizard guidato")
    p.add_argument("--yes", action="store_true", help="(end) applica senza conferme")
    p.add_argument("--last-n", type=int, default=1, help="(next/recap) sessioni da scandire")
    p.add_argument("--hype", action="store_true", help="(next/recap) anche vesti Homebrewery")
    p.add_argument("--pg", help="(recap) recap personale per questo PG (blocchi Split)")
    p.add_argument("--group", help="(branch) nome gruppo la prima volta")

    p = sub.add_parser("skills", help="pipeline skill multi-agente")
    p.add_argument("action", choices=["build", "sync"])
    p.add_argument("--no-deploy", action="store_true")

    p = sub.add_parser("doctor", help="diagnosi ambiente")
    p.add_argument("--ci", action="store_true", help="in CI: gli avvisi non falliscono")

    args, extra = ap.parse_known_args(argv)
    return {
        "prep": cmd_prep, "maps": cmd_maps, "post": cmd_post, "recap": cmd_recap,
        "handout": cmd_handout, "hype": cmd_hype, "dossier": cmd_dossier,
        "session": cmd_session, "skills": cmd_skills, "doctor": cmd_doctor,
    }[args.cmd](args, extra)


if __name__ == "__main__":
    raise SystemExit(main())
