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

Regioni gestite:
  march-clock   righe "Current March Day" / "Days remaining" (§2.1, state.md)
  changelog     blocco append-only (state-changelog.md)
  clock villain campo `clock` dei record di `campaign/state.yaml` (§3)

I tre master (ADR-0050, `dmcore/masters.py`): i fatti tabellari stanno in
`campaign/state.yaml` e da li' si RIGENERANO in state.md; la prosa sta in
`campaign/state.md`; lo storico in `campaign/state-changelog.md`. Le proposte
che restano a mano dicono in QUALE dei tre vanno: dirle tutte «in state.md»
significava dire al DM di scriverle dove il prossimo `render_state.py` le
cancella.

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
from dmcore.masters import per_master  # noqa: E402
from dmcore.regions import RegionError, find_regions, replace_region, wrap  # noqa: E402
from state_sync import extract_events, _suggest  # noqa: E402

STATE_REL = Path("campaign") / "state.md"
#: I fatti tabellari (§0, §1, §2.4, §3, §4, §6, §7.E) hanno qui il loro master
#: dal lotto 4d-1: le tabelle di state.md sono una VISTA generata (ADR-0050).
STATE_YAML_REL = Path("campaign") / "state.yaml"
# Lo storico vive nel proprio file dal 2026-09-16 (lotto 4d-2): erano 1.179
# righe, il 71% di state.md, e lo stato vivo non si leggeva piu' perche' la
# storia gli stava sopra. `state_apply` lo segue li'.
CHANGELOG_REL = Path("campaign") / "state-changelog.md"
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
        # 🔴 Se la riga NON e' autonoma, marcarla corromperebbe il canone.
        #
        # Questo codice presumeva una riga a se'. Il lotto 4c (2026-09-12) ha
        # trasformato il March Day nell'inizio di un PARAGRAFO di cinque righe
        # — «**Current March Day:** **19** — e' il punto di sincronia previsto,
        # non un giorno gia' trascorso…» — che spiega perche' quel numero e' un
        # bersaglio e non un passato.
        #
        # Marcandone solo la prima riga, `apply_march_clock` la sostituirebbe e
        # lascerebbe le altre quattro **orfane, a meta' frase**. Trovato
        # accendendo la via di scrittura nel lotto 4d-2: non era mai emerso
        # perche' `--migrate` non era mai stato eseguito.
        #
        # Si rifiuta invece di indovinare dove finisce il paragrafo: allargare
        # la regione fino alla riga vuota cancellerebbe la nota del DM al primo
        # aggiornamento, che e' il danno peggiore dei due.
        resto = text[end:].split("\n", 1)[0]
        if resto.strip() and not resto.lstrip().startswith(("|", "#", "-", "*", ">")):
            raise RegionError(
                "la riga '**Current March Day:**' continua nel paragrafo "
                f"successivo ({resto.strip()[:48]}…): marcarla corromperebbe il "
                "canone al primo aggiornamento. Serve una riga autonoma per la "
                "macchina, accanto alla prosa — decisione del DM")
        text = text[:start] + wrap("march-clock", text[start:end]) + "\n" + text[end:]
        added.append("march-clock")

    return text, added


def migrate_changelog(text: str) -> "tuple[str, list[str]]":
    """Avvolge nel marker `changelog` l'ULTIMO blocco fenced dello storico.

    ⚠️ L'ultimo, non il primo: `campaign/state-changelog.md` ne contiene
    **tre** consecutivi, e `state_apply` appende sempre in coda. Marcare il
    primo significherebbe scrivere le voci nuove in mezzo a quelle del maggio
    2026.
    """
    added: list[str] = []
    if "changelog" in find_regions(text):
        return text, added
    fences = list(FENCE_RE.finditer(text))
    if len(fences) < 2:
        raise RegionError("nessun blocco ``` in state-changelog.md: "
                          "impossibile migrare la regione changelog")
    start = fences[-2].start()
    end = text.find("\n", fences[-1].end()) + 1
    if end == 0:
        end = len(text)
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


def rigenera_tabelle(md: str, yaml_text: str) -> str:
    """Le regioni `gen:state:` di state.md, rifatte dal YAML appena scritto.

    🔴 Senza questo passo la scrittura in `state.yaml` lascerebbe `state.md`
    indietro di una sessione, e `render_state.py --check` — che gira in CI —
    diventerebbe rosso subito dopo un `state_apply` andato a buon fine. Il tool
    che aggiorna il canone non puo' lasciare il repo in uno stato che il
    cancello del canone boccia.
    """
    import yaml as _yaml  # pyyaml: debito dichiarato (ADR-0037), import tardivo

    import render_state
    nuovo, mancanti = render_state.apply_regions(md, _yaml.safe_load(yaml_text))
    if mancanti:
        raise RegionError(
            "marcatori gen:state: assenti in state.md: " + ", ".join(mancanti))
    return nuovo


def _clock_villain(dati_yaml: str, name: str, groups: tuple) -> "tuple[int, str, str] | None":
    """(indice, valore nuovo, etichetta) del clock da far avanzare, o None.

    None significa «non identificato con certezza»: il chiamante lascia la
    proposta a mano. Non c'e' un ripiego, ed e' voluto — con tredici villain in
    tabella, avanzare il clock del villain sbagliato e' canone rotto in
    silenzio, il danno che ADR-0041 chiede di non correre.
    """
    import yaml as _yaml

    from dmcore.statedata import fondo_del_clock, trova_villain
    dati = _yaml.safe_load(dati_yaml)
    if name == "ritual_clock":
        a, b = groups
        # §2.0 e' l'unico clock su diciotto: il denominatore lo identifica.
        i = trova_villain(dati, fondo=18, numeratore=a)
        if i is None:
            return None
        return i, f"{b}/18", f"Ritual Clock {a}/18 → {b}/18"
    if name == "villain_clock":
        chi, a, b = groups
        i = trova_villain(dati, nome=chi, numeratore=a)
        if i is None:
            return None
        fondo = fondo_del_clock(dati, i)
        if fondo is None:
            return None
        return i, f"{b}/{fondo}", f"clock {chi} {a}/{fondo} → {b}/{fondo}"
    return None


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
            # ⚠️ Tutti e tre i master, non solo state.md: dal 2026-09-16 questo
            # tool scrive anche in state.yaml, e un file sporco fuori dalla
            # guardia e' un `git revert` che non torna indietro del tutto.
            dirty = subprocess.run(
                ["git", "-C", str(repo), "status", "--porcelain", "--",
                 str(STATE_REL), str(STATE_YAML_REL), str(CHANGELOG_REL)],
                capture_output=True, text=True).stdout.strip()
            if dirty:
                print("[apply] ✗ un master di campagna ha modifiche non committate:\n"
                      f"{dirty}\n"
                      "        committa (o scarta) prima, così l'undo resta "
                      "`git revert` (ADR-0007 vincolo 4)", file=sys.stderr)
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
    yaml_path = repo / STATE_YAML_REL
    ydata = yaml_path.read_text(encoding="utf-8") if yaml_path.exists() else None
    ydata_originale = ydata
    applied: list[str] = []
    #: (trigger, testo) — il trigger serve a dire in QUALE master va la proposta
    manual: "list[tuple[str, str]]" = []
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
                manual.append((name, _suggest(name, groups)))
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
                manual.append((name, _suggest(name, groups)))
        elif name in ("ritual_clock", "villain_clock"):
            if groups[-2] == groups[-1]:
                continue  # nessun cambiamento: niente rumore
            if ydata is None:
                print(f"[apply] ⚠ {STATE_YAML_REL} assente — {name} resta manuale")
                manual.append((name, _suggest(name, groups)))
                continue
            esito = _clock_villain(ydata, name, groups)
            if esito is None:
                # Zero corrispondenze o piu' d'una: si dichiara, non si sceglie.
                print(f"[apply] ⚠ {name} {' '.join(map(str, groups))}: nessun "
                      f"villain identificato con certezza in {STATE_YAML_REL} — "
                      "resta manuale")
                manual.append((name, _suggest(name, groups)))
                continue
            indice, valore, etichetta = esito
            try:
                from dmcore.statedata import StateDataError, imposta_campo
                nuovo_yaml = imposta_campo(ydata, "villain", indice, "clock", valore)
            except StateDataError as exc:
                print(f"[apply] ⚠ {etichetta} non applicabile ({exc}) — resta manuale")
                manual.append((name, _suggest(name, groups)))
                continue
            if nuovo_yaml == ydata:
                print(f"[apply] {etichetta} già a posto — niente da fare (idempotente)")
                continue
            print(f"\n[apply] proposta {name} → {STATE_YAML_REL} (§3 villain)")
            print(_diff(ydata, nuovo_yaml, str(STATE_YAML_REL)))
            if _confirm("[apply] applico questo blocco?", assume_yes):
                ydata = nuovo_yaml
                applied.append(etichetta)
            else:
                manual.append((name, _suggest(name, groups)))
        else:
            manual.append((name, _suggest(name, groups)))

    # Le tabelle di state.md sono una VISTA: dopo aver toccato il master vanno
    # rigenerate nello stesso giro, o il repo resta in uno stato che
    # `render_state.py --check` boccia.
    if ydata is not None and ydata != ydata_originale:
        try:
            text = rigenera_tabelle(text, ydata)
        except RegionError as exc:
            print(f"[apply] ✗ {exc}: annullo anche la scrittura in "
                  f"{STATE_YAML_REL} (un master senza la sua vista è drift)",
                  file=sys.stderr)
            return 1

    clog_path = repo / CHANGELOG_REL
    clog = clog_path.read_text(encoding="utf-8") if clog_path.exists() else None
    clog_originale = clog
    if applied:
        entry = (f"{date.today().isoformat()}  {session_label}: "
                 + "; ".join(applied) + " (state_apply).")
        if clog is None:
            print(f"[apply] ⚠ {CHANGELOG_REL} assente — aggiorna lo storico a mano")
        else:
            try:
                candidate = append_changelog(clog, entry)
                print(f"\n[apply] proposta changelog ({CHANGELOG_REL}):")
                print(_diff(clog, candidate, str(CHANGELOG_REL)))
                if _confirm("[apply] appendo al changelog?", assume_yes):
                    clog = candidate
            except RegionError as exc:
                print(f"[apply] ⚠ changelog non applicabile ({exc}) — "
                      f"aggiorna {CHANGELOG_REL} a mano")

    if manual:
        # 🔴 «applicale a mano in state.md», che questo blocco diceva fino al
        # 2026-09-16, era l'istruzione per perderne meta': le tabelle di
        # state.md sono generate da state.yaml e un'edizione a mano sparisce al
        # prossimo `render_state.py`, senza errore e senza avviso.
        print("\n[apply] proposte NON meccaniche — ognuna nel SUO master (ADR-0050):")
        for master, righe in per_master(manual).items():
            if master is None:
                print("\n  ⚠ destinazione non dichiarata in dmcore/masters.py:")
            else:
                print(f"\n  → `{master.file}` — {master.nota}")
            for line in righe:
                print(f"    {line}")

    if text == original and clog == clog_originale and ydata == ydata_originale:
        print("\n[apply] ✓ niente da scrivere (già allineato o tutto rifiutato)")
        return 0
    if check:
        print("\n[apply] --check: nessuna scrittura eseguita")
        return 0

    toccati = []
    # Prima il master, poi la vista: se il processo muore in mezzo, il fatto e'
    # salvo e `render_state.py` ricostruisce il resto. All'inverso si
    # perderebbe il dato e resterebbe una tabella che nessuno sa rigenerare.
    if ydata is not None and ydata != ydata_originale:
        yaml_path.write_text(ydata, encoding="utf-8")
        print(f"\n[apply] ✓ scritto {yaml_path}")
        toccati.append(str(STATE_YAML_REL))
    if text != original:
        state_path.write_text(text, encoding="utf-8")
        print(f"[apply] ✓ scritto {state_path}")
        toccati.append(str(STATE_REL))
    if clog is not None and clog != clog_originale:
        clog_path.write_text(clog, encoding="utf-8")
        print(f"[apply] ✓ scritto {clog_path}")
        toccati.append(str(CHANGELOG_REL))
    if do_commit:
        sha = gitio.commit_paths(
            repo, toccati,
            f"state: {'; '.join(applied) or 'sync'} — {session_label} [state_apply]")
        print(f"[apply] ✓ commit {sha}" if sha else "[apply] (nulla da committare)")
    else:
        print("[apply] ricordati il commit: git add "
              + " ".join(toccati) + " && git commit")
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
        clog_path = repo / CHANGELOG_REL
        text = state_path.read_text(encoding="utf-8")
        clog = clog_path.read_text(encoding="utf-8") if clog_path.exists() else None
        # Le due regioni si marcano in modo INDIPENDENTE: una che non si puo'
        # marcare in sicurezza non deve impedire l'altra. Il changelog vive in
        # un file suo dal 2026-09-16, e bloccarlo perche' il March Day di
        # state.md e' annegato nella prosa sarebbe punire il file sbagliato.
        added: list[str] = []
        problemi: list[str] = []
        new_text = text
        try:
            new_text, aggiunti = migrate(text)
            added += aggiunti
        except RegionError as exc:
            problemi.append(f"march-clock: {exc}")
        new_clog = None
        if clog is None:
            problemi.append(f"{CHANGELOG_REL} assente: regione changelog non marcabile")
        else:
            try:
                new_clog, aggiunti = migrate_changelog(clog)
                added += aggiunti
            except RegionError as exc:
                problemi.append(f"changelog: {exc}")
        for pr in problemi:
            print(f"[apply] ⚠ {pr}", file=sys.stderr)
        if not added and problemi:
            gia = [k for k, s in (("march-clock", text), ("changelog", clog or ""))
                   if f"key={k}" in s]
            if gia:
                print(f"[apply] ✓ gia' marcate: {', '.join(gia)} — "
                      f"resta da risolvere quanto sopra")
                return 1
            print("[apply] ✗ nessuna regione marcata", file=sys.stderr)
            return 1
        if not added:
            print("[apply] ✓ marker già presenti — niente da fare")
            return 0
        if args.check:
            print(_diff(text, new_text, str(STATE_REL)))
            if new_clog is not None:
                print(_diff(clog, new_clog, str(CHANGELOG_REL)))
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
        toccati = []
        if new_text != text:
            state_path.write_text(new_text, encoding="utf-8")
            toccati.append(str(STATE_REL))
        if new_clog is not None and new_clog != clog:
            clog_path.write_text(new_clog, encoding="utf-8")
            toccati.append(str(CHANGELOG_REL))
        print(f"[apply] ✓ marker inseriti: {', '.join(added)} "
              f"(in {', '.join(toccati)})")
        if args.commit:
            sha = gitio.commit_paths(repo, toccati,
                                     "state: migrazione marker auto: (ADR-0007)")
            print(f"[apply] ✓ commit {sha}" if sha else "[apply] (nulla da committare)")
        return 0

    return run(repo, args.session, args.check, args.yes, args.commit, args.no_guard)


if __name__ == "__main__":
    raise SystemExit(main())
