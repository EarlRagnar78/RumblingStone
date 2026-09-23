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
    bestiario (prep) i cinque script delle creature: estrai, deriva, attributi,
                     creatura, conformita
    skills    (manutenzione) build/sync pipeline skill multi-agente
    doctor    (tutte) diagnosi ambiente e freschezza del catalogo

Esempi:
    python3 scripts/dm.py prep --el 13 --env forest --factions red-hand
    python3 scripts/dm.py maps validate
    python3 scripts/dm.py post --session 2026-05-03_session-3.md
    python3 scripts/dm.py recap --hype
    python3 scripts/dm.py handout --tipo lettera --da bozza.md
    python3 scripts/dm.py bestiario creatura --gs 7 --ruolo bruto
    python3 scripts/dm.py doctor

I flag non riconosciuti da `prep`/`recap` vengono inoltrati allo script
sottostante (es. `--seed`, `--narrative`): vedi `<script>.py --help`.
"""

from __future__ import annotations

import argparse
import json
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


#: `dm.py bestiario <azione>` → lo script delle creature che la fa. Gli script
#: restano invocabili per nome, perché la CI e il manifest li chiamano così
#: (`PIANO-QUALITA-DEL-CODICE` §8, E9).
BESTIARIO = {
    "estrai": "extract_statblocks.py",
    "deriva": "derive_statblocks.py",
    "attributi": "genera_attributi.py",
    "creatura": "genera_creatura.py",
    "conformita": "conformita_statblocchi.py",
}


def cmd_bestiario(args: argparse.Namespace, extra: list[str]) -> int:
    if not args.action:
        print("[dm] uso: dm.py bestiario <azione> [flag dello script]")
        for azione, script in BESTIARIO.items():
            print(f"      {azione:11} → {script}")
        print("[dm] i flag passano allo script: `dm.py bestiario <azione> --help`")
        return 2
    return run(BESTIARIO[args.action], *extra)


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


def cmd_prompts(args: argparse.Namespace, extra: list[str]) -> int:
    # Prompt immagine dell'arco (ADR-0015): lo script estrae le scene,
    # i prompt li scrive l'agente/DM nelle schede generate
    po = [args.arc]
    if args.out:
        po += ["-o", args.out]
    if args.list:
        po += ["--list"]
    return run("extract_scene_prompts.py", *po, *extra)


def cmd_booklet(args: argparse.Namespace, extra: list[str]) -> int:
    # Booklet HTML «pergamena» (stile canonico del Palio) da manifest JSON
    bo = [args.manifest]
    if args.out:
        bo += ["--out", args.out]
    if args.format:
        bo += ["--format", args.format]
    rc = run("build_booklet_html.py", *bo, *extra)
    if rc == 0 and (args.pdf or args.pdf_all):
        # ADR-0013 §5-bis: PDF A4 via Chromium headless — --pdf = pagine ✉
        # player (da inviare), --pdf-all = TUTTE le schede (anche ⚠ DM)
        ex = ["--all"] if args.pdf_all else []
        rc = run("export_booklet_pdf.py", args.manifest, *ex)
    return rc


# ---------------------------------------------------------- volume (G3)

#: I mestieri, **nell'ordine in cui si chiamano**. E' la cosa che la ricerca sul
#: colophon Paizo ha trovato mancante (§C, «la combinazione»): le skill c'erano
#: tutte, nessun documento diceva in che ordine si usano per fare un volume. Chi
#: ne salta uno se ne accorge in copisteria.
#:
#: `stampa` assorbe il `dm.py stampa` promesso dall'audit di agosto e mai fatto.
PASSI_VOLUME = ("prosa", "lingua", "manifest", "colophon", "schermo", "stampa", "imposizione")


def _colophon_del_manifest(mp: Path) -> tuple[bool, str]:
    """Il volume ha un colophon, e la sua data e' scritta invece che dedotta?

    ADR-0023. Non e' un controllo di schema — quello lo fa `validate_booklets` —
    e' la domanda dell'editore: **questo volume dice di chi e', che versione e'
    e cosa se ne puo' fare?** Un volume anonimo si stampa lo stesso.
    """
    try:
        man = json.loads(mp.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"manifest illeggibile: {e}"
    col = man.get("colophon")
    if not col:
        return False, ("nessun colophon: il volume esce anonimo, senza versione "
                       "ne' regime d'uso (ADR-0023)")
    mancanti = [k for k in ("versione", "data", "autori", "licenza") if not col.get(k)]
    if mancanti:
        return False, "colophon incompleto, mancano: " + ", ".join(mancanti)
    return True, (f"{col.get('edizione', 'edizione')} {col['versione']} · "
                  f"{col['data']} · {col['autori']}")


def cmd_volume(args: argparse.Namespace, extra: list[str]) -> int:
    """La catena dei mestieri in ordine, da un manifest a un volume."""
    mp = Path(args.manifest)
    if not mp.is_absolute():
        mp = REPO / mp
    if not mp.is_file():
        print(f"[dm] \u2717 manifest inesistente: {args.manifest}", file=sys.stderr)
        return 2

    salta = set(args.salta or [])
    solo = set(args.solo or [])
    passi = [x for x in PASSI_VOLUME
             if (not solo or x in solo) and x not in salta]
    if not args.stampa and not solo:
        passi = [x for x in passi if x not in ("stampa", "imposizione")]
    if args.imposto and "imposizione" not in passi and not salta:
        passi.append("imposizione")

    capitoli = []
    try:
        man = json.loads(mp.read_text(encoding="utf-8"))
        capitoli = [str((mp.parent / c["file"]).resolve().relative_to(REPO))
                    for c in man.get("chapters", [])
                    if (mp.parent / c["file"]).is_file()]
    except Exception:
        pass

    print(f"[dm] volume \u2014 {mp.name}")
    print("[dm] passi: " + " \u2192 ".join(passi) + "\n")
    esiti: list[tuple[str, str, str]] = []
    duro = 0

    for passo in passi:
        print(f"\u2500\u2500 {passo} " + "\u2500" * max(0, 60 - len(passo)))
        if passo == "prosa":
            # Misura, non blocca: la norma e' `italiano-nativo.md`, questo la
            # conta (ADR-0025). Un gate rumoroso che blocca viene disattivato.
            rc = run("validate_prosa.py", *capitoli, check=False) if capitoli else 0
            esiti.append((passo, "\u26a0" if rc else "\u2713",
                          "rilievi di prosa: guardali" if rc else "nessun calco, nessun tic"))
        elif passo == "lingua":
            rc = run("validate_lingua.py", *capitoli, check=False) if capitoli else 0
            esiti.append((passo, "\u26a0" if rc else "\u2713",
                          "refusi meccanici" if rc else "nessun refuso"))
        elif passo == "manifest":
            rc = run("validate_booklets.py", check=False)
            if rc:
                duro = rc
            esiti.append((passo, "\u2717" if rc else "\u2713",
                          "schema o parita' fra le catene" if rc else "schema e parita' ok"))
            if rc:
                break
        elif passo == "colophon":
            ok, dettaglio = _colophon_del_manifest(mp)
            print(("  \u2713 " if ok else "  \u26a0 ") + dettaglio)
            esiti.append((passo, "\u2713" if ok else "\u26a0", dettaglio))
        elif passo == "schermo":
            rc = run("build_booklet_html.py", str(mp), check=False)
            if rc:
                duro = rc
            esiti.append((passo, "\u2717" if rc else "\u2713",
                          "compilazione HTML fallita" if rc else "HTML costruito"))
            if rc:
                break
        elif passo == "stampa":
            rc = run("export_booklet_typst.py", str(mp), "--all", check=False)
            if rc == 2:
                esiti.append((passo, "\u25cb", "typst assente: il volume da stampa "
                                                "si fa quando c'e' (ADR-0027)"))
                continue
            if rc:
                duro = rc
            esiti.append((passo, "\u2717" if rc else "\u2713",
                          "compilazione Typst fallita" if rc else "PDF con segnalibri"))
            if rc:
                break
        elif passo == "imposizione":
            esiti.append(_imponi(mp))

    print("\n[dm] volume \u2014 riepilogo")
    for nome, segno, dettaglio in esiti:
        print(f"  {segno} {nome:12} {dettaglio}")

    # Il cancello d'uscita. Non e' automatizzabile e non si finge che lo sia: si
    # DICE, qui, perche' questo e' il momento in cui un volume sta per uscire ed
    # e' esattamente il punto in cui il lotto E aveva trovato il buco — una
    # regola scritta che nessuno carica non e' una regola.
    print("\n  \u26a0 Prima che questo volume esca dal repo: il cancello \u00a77 di "
          "docs/guides/GUIDA-CONDIVISIONE-IP.md.\n"
          "    Uso privato al tavolo: nessun cancello. Fuori di li', quelle cinque "
          "domande vengono prima — e se c'\u00e8 di mezzo del denaro, ci si ferma "
          "(ADR-0005).")
    return duro


def _imponi(mp: Path) -> tuple[str, str, str]:
    """Il libretto da piegare (ADR-0027). Degrada pulito: dichiara e non fallisce."""
    sys.path.insert(0, str(SCRIPTS))
    import binari
    percorso = binari.trova(binari.PDFCPU)
    pdf = mp.parent / f"{mp.stem.replace('.manifest', '')}-STAMPA.pdf"
    if percorso is None:
        return ("imposizione", "\u25cb", "pdfcpu assente: " + binari.PDFCPU.ripiego)
    if not pdf.is_file():
        return ("imposizione", "\u25cb", "nessun PDF da imporre (serve il passo «stampa»)")
    fuori = pdf.with_name(pdf.stem + "-LIBRETTO.pdf")
    esito = subprocess.run(
        [percorso, "booklet", "-c", "disable", "-o", "-q", "--",
         "formsize:A4, border:off, margin:0", str(fuori), "2", str(pdf)],
        capture_output=True, text=True)
    if esito.returncode != 0:
        return ("imposizione", "\u2717", (esito.stderr or "pdfcpu fallito").strip()[:120])
    return ("imposizione", "\u2713",
            f"{fuori.name} \u2014 da piegare. Non si versiona: l'output di pdfcpu "
            f"non e' byte-identico (ADR-0027)")


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
    try:
        import binari as _binari
        _minimo = ".".join(str(n) for n in _binari.PYTHON_MINIMO)
        if _binari.python_ok():
            ok(f"python {sys.version.split()[0]}")
        else:
            warn(f"python {sys.version.split()[0]} — serve ≥ {_minimo}")
    except Exception as exc:  # doctor non deve mai crashare
        warn(f"check versione di Python fallito: {exc}")

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
        # Le due regioni vivono in due file dal 2026-09-16 (lotto 4d-2): lo
        # storico ha il suo, e cercarle entrambe in state.md darebbe sempre
        # «assenti» anche col changelog marcato correttamente.
        _state = REPO / "campaign" / "state.md"
        _clog = REPO / "campaign" / "state-changelog.md"
        _regs = set()
        if _state.exists():
            _regs |= set(_find_regions(_state.read_text(encoding="utf-8")))
        if _clog.exists():
            _regs |= set(_find_regions(_clog.read_text(encoding="utf-8")))
        if _state.exists():
            # ⚠️ `march-clock` non e' piu' qui: con D14 (2026-09-16) il March Day
            # e' un campo di state.yaml e la sua riga si RIGENERA come le altre
            # tabelle. Quel che il doctor deve cercare in state.md sono i
            # marcatori `gen:state:`, che `render_state --check` gia' verifica.
            mancanti = {"changelog"} - _regs
            if not mancanti:
                ok("marker auto: changelog presente in state-changelog.md")
            else:
                print(f"  ○ marker auto: manca {', '.join(sorted(mancanti))} — "
                      "`state_apply.py --migrate` sul branch gruppo")
    except Exception as exc:  # doctor non deve mai crashare
        warn(f"check sessione ADR-0007 falliti: {exc}")

    # Tutte le dipendenze esterne, lette da `binari.py` (lotto D di
    # PIANO-QUALITA-DEL-CODICE). Prima `doctor` aveva la propria lista di
    # pandoc e xelatex accanto a quella del registro, e le due divergevano.
    # Sono opzionali: qui si dice cosa manca e cosa resta possibile senza, mai
    # un avviso — `doctor` non deve trasformare un ripiego dichiarato in un
    # difetto. L'unica eccezione e' una libreria obbligatoria che manca, che
    # ferma un gate della CI ed e' quindi un problema vero.
    try:
        import binari as _binari
        for _b, _p in (*_binari.stato(), *_binari.stato_opzionali()):
            if _p:
                ok(f"{_b.nome} presente ({_b.a_cosa_serve})")
            else:
                print(f"  ○ {_b.nome} assente — {_b.ripiego}")
        for _lib, _c_e in _binari.stato_librerie():
            if _c_e:
                ok(f"{_lib.nome} presente ({_lib.a_cosa_serve})")
            elif _lib.obbligatoria:
                warn(f"{_lib.nome} assente — {_lib.ripiego}")
            else:
                print(f"  ○ {_lib.nome} assente — {_lib.ripiego}")
        _non_pronte = [
            (_catena, [_n for _n in _servono
                       if not _binari.disponibile(_n)])
            for _catena, _servono in _binari.CATENE.items()
        ]
        for _catena, _mancano in _non_pronte:
            if _mancano:
                print(f"  ○ catena «{_catena}»: manca {', '.join(_mancano)}")
    except Exception as exc:  # doctor non deve mai crashare
        warn(f"check dipendenze esterne fallito: {exc}")

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

    # add_help=False: `--help` non lo prende dm.py ma lo script, così
    # `dm.py bestiario creatura --help` stampa l'aiuto di genera_creatura.
    p = sub.add_parser("bestiario", add_help=False,
                       help="le creature: estrai / deriva / attributi / creatura / "
                            "conformita (i flag passano allo script)")
    p.add_argument("action", nargs="?", choices=list(BESTIARIO))

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

    p = sub.add_parser("prompts", help="scene illustrabili di un arco → scheletro dei "
                                      "prompt immagine (ADR-0015)")
    p.add_argument("arc", help="cartella dell'arco (es. \"07_il Portale Della Forgia Eterna\")")
    p.add_argument("-o", "--out", help="file di output (default: <arco>/Immagini/PROMPT-IMMAGINI-*.md)")
    p.add_argument("--list", action="store_true", help="elenca soltanto le scene trovate")

    p = sub.add_parser("booklet", help="booklet in stile pergamena da manifest JSON "
                                       "(ADR-0013): HTML autonomo e/o sorgente Homebrewery V3")
    p.add_argument("manifest", help="manifest *.manifest.json del booklet")
    p.add_argument("--out", help="file di output (default: dal manifest)")
    p.add_argument("--format", choices=["html", "hb", "both"], default=None,
                   help="html = pagina autonoma · hb = .hb.md per il self-hosted/Docker "
                        "(dm.py hype) · both = entrambi")
    p.add_argument("--pdf", action="store_true",
                   help="dopo la build: PDF A4 delle pagine ✉ player "
                        "(export_booklet_pdf.py, serve Chromium/Chrome)")
    p.add_argument("--pdf-all", action="store_true", dest="pdf_all",
                   help="dopo la build: PDF A4 di TUTTE le schede "
                        "(copertina e capitoli ⚠ DM inclusi, prefissi pg-/dm-)")

    p = sub.add_parser("volume",
                       help="la catena dei mestieri in ordine: da un manifest a un "
                            "volume (assorbe il «dm.py stampa» mai fatto)")
    p.add_argument("manifest", help="il manifest del volume (.manifest.json)")
    p.add_argument("--stampa", action="store_true",
                   help="fai anche l'edizione da stampa (Typst, un volume con segnalibri)")
    p.add_argument("--imposto", action="store_true",
                   help="e imponilo in libretto da piegare (pdfcpu, ADR-0027)")
    p.add_argument("--solo", action="append", choices=PASSI_VOLUME,
                   help="esegui solo questi passi (ripetibile)")
    p.add_argument("--salta", action="append", choices=PASSI_VOLUME,
                   help="salta questi passi (ripetibile)")

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
        "booklet": cmd_booklet, "prompts": cmd_prompts, "bestiario": cmd_bestiario,
        "session": cmd_session, "volume": cmd_volume, "skills": cmd_skills, "doctor": cmd_doctor,
    }[args.cmd](args, extra)


if __name__ == "__main__":
    raise SystemExit(main())
