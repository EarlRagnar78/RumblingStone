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

Da dove legge (lotto 4e): se il log comincia con un front-matter `delta:`
(lo scrive il wizard), le quattro scritture meccaniche vengono SOLO da li', coi
villain nominati per `png_id` (`dmcore/delta_sessione.py`). Senza front-matter
si ricade sulla regex di `state_sync`, che conosce i nomi scritti nel suo
sorgente e non gli altri.

Cosa scrive, e dove:
  changelog       regione `auto:changelog` di `state-changelog.md` (append-only)
  march clock     `march_clock.giorno_corrente` in state.yaml — **D14**
  clock villain   campo `clock` dei record di state.yaml (§3)
  morte / fuga    campo `stato` dei record di state.yaml (§3) — **D16**

Dopo ogni scrittura in `state.yaml` le regioni `gen:state:` di `state.md` si
rigenerano nello stesso giro: il master e la sua vista non restano mai sfasati.

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
from dmcore import delta_sessione  # noqa: E402
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

#: ⚠️ `RETHMAR_DAY = 42` stava qui, cablato. Era la seconda fonte di verita' piu'
#: piccola del repo, e sopravviveva perche' nessuno aveva mai eseguito il tool:
#: il giorno d'arrivo e' un DATO (`march_clock.giorno_arrivo`), e la vista se lo
#: deriva. Tolto con D14.
FENCE_RE = re.compile(r"^```", re.M)


# ------------------------------------------------------------------ migrate


def migrate(text: str) -> "tuple[str, list[str]]":
    """Non c'e' piu' niente da marcare in `state.md` — **decisione D14**.

    🔵 Questa funzione marcava la regione `auto:march-clock`, e si **rifiutava**
    di farlo: il lotto 4c aveva reso «`**Current March Day:**`» l'inizio di un
    paragrafo di cinque righe, e sostituirne solo la prima avrebbe lasciato le
    altre quattro **orfane a meta' frase**. Il rifiuto era la cosa giusta, ma
    era un blocco, non una soluzione.

    Il DM ha sciolto il nodo il 2026-09-16: **il numero e' un dato**
    (`march_clock.giorno_corrente` in `state.yaml`) e la sua vista si rigenera
    come le altre otto tabelle; **la spiegazione resta prosa**, sotto e fuori
    dalla regione generata. I due non condividono piu' una riga, quindi non si
    contendono piu' uno scrittore.

    Marcare oggi quella riga con `auto:` sarebbe **peggio** che prima: creerebbe
    una regione dentro una regione `gen:state:`, cioe' due scrittori sullo stesso
    testo — il difetto dei due master, ricreato dalla sua stessa correzione.

    Resta come funzione, e non come buco, perche' `--migrate` deve continuare a
    rispondere qualcosa di vero se un giorno `state.md` avra' di nuovo zone che
    la macchina scrive fuori dal rendering.
    """
    return text, []


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


#: Come il trigger del log si traduce in uno stato dichiarato (D16, 2026-09-16).
#:
#: ⚠️ `npc_killed` → `morto` è la lettura letterale del log, ma **non decide se
#: è definitivo**: `reversibile` non si tocca qui. In questa campagna un morto
#: torna, e dirlo è del DM — la regola R9 di `validate_state` glielo chiederà
#: alla prima esecuzione, che è il posto giusto per chiederlo.
STATO_DA_TRIGGER = {"npc_killed": "morto", "npc_escaped": "latitante"}


def _stato_villain(dati_yaml: str, name: str, groups: tuple) -> "tuple[int, str, str] | None":
    """(indice, stato nuovo, etichetta) per una morte o una fuga, o None.

    None quando il nome del log non corrisponde a **esattamente un** villain di
    §3: il PNG può non essere in tabella (il log nomina chiunque), o il nome può
    essere ambiguo. In entrambi i casi resta una proposta a mano.
    """
    import yaml as _yaml

    dati = _yaml.safe_load(dati_yaml)
    chi = groups[0]
    trovati = [i for i, r in enumerate(dati.get("villain") or [])
               if chi.lower() in str(r.get("villain", "")).lower()]
    if len(trovati) != 1:
        return None
    i = trovati[0]
    nuovo = STATO_DA_TRIGGER[name]
    if dati["villain"][i].get("stato") == nuovo:
        return None
    return i, nuovo, f"{chi}: stato → {nuovo}"


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

    # 🔵 Lotto 4e: se il log porta un front-matter coi delta, le scritture
    # meccaniche vengono SOLO da li', per `png_id`. La regex resta per i log
    # senza front-matter, e per quelli con il front-matter i suoi trigger
    # meccanici si ignorano: le due vie insieme scriverebbero due volte.
    hits = ev["hits"]
    try:
        delta = delta_sessione.estrai(spath.read_text(encoding="utf-8"))
    except delta_sessione.DeltaError as exc:
        print(f"[apply] ✗ {ev['file']}: {exc} — nessuna scrittura", file=sys.stderr)
        return 1
    if delta is not None:
        if ydata is None:
            print(f"[apply] ✗ il log porta un delta ma {STATE_YAML_REL} non "
                  "esiste — nessuna scrittura", file=sys.stderr)
            return 1
        import yaml as _yaml  # pyyaml: debito dichiarato (ADR-0037)
        try:
            ops = delta_sessione.operazioni(delta, _yaml.safe_load(ydata))
        except delta_sessione.DeltaError as exc:
            print(f"[apply] ✗ delta di {ev['file']} non applicabile: {exc}\n"
                  "        nessuna scrittura: un delta si applica tutto o "
                  "niente", file=sys.stderr)
            return 1
        ignorati = [h for h in hits if h[0] in delta_sessione.MECCANICI]
        hits = [h for h in hits if h[0] not in delta_sessione.MECCANICI]
        print(f"[apply] front-matter: {len(ops)} scritture dal delta")
        for _nome, raw, _g in ignorati:
            # A video, non in silenzio: se il DM ha aggiunto a mano una riga
            # che il delta non ha, deve vederla restare fuori.
            print(f"[apply]   ignorata (la scrive solo il delta): {raw}")
        for op in ops:
            from dmcore.statedata import StateDataError, imposta_campo, imposta_campo_oggetto
            try:
                if op.indice is None:
                    nuovo_yaml = imposta_campo_oggetto(ydata, op.sezione, op.campo, op.valore)
                else:
                    nuovo_yaml = imposta_campo(ydata, op.sezione, op.indice,
                                               op.campo, op.valore)
            except StateDataError as exc:
                print(f"[apply] ✗ {op.etichetta}: {exc} — nessuna scrittura",
                      file=sys.stderr)
                return 1
            print(f"\n[apply] proposta dal delta: {op.etichetta} (in {STATE_YAML_REL})")
            print(_diff(ydata, nuovo_yaml, str(STATE_YAML_REL)))
            if op.campo == "stato":
                print("[apply] ⚠ `reversibile` NON viene scritto: se il canone "
                      "prevede un ritorno lo dice il DM (regola R9).")
            if _confirm("[apply] applico questo blocco?", assume_yes):
                ydata = nuovo_yaml
                applied.append(op.etichetta)
            else:
                # il trigger equivalente, solo per dire in quale master va
                equivalente = ("march_clock" if op.indice is None else
                               "villain_clock" if op.campo == "clock" else "npc_killed")
                manual.append((equivalente, f"- {op.etichetta} (rifiutato a video)"))

    for name, raw, groups in hits:
        if name == "march_clock":
            # 🔵 D14, chiusa dal DM il 2026-09-16: il March Day e' un CAMPO di
            # state.yaml, non piu' una riga da sostituire dentro la prosa. Prima
            # la riga della macchina e la nota del DM erano lo stesso paragrafo,
            # e per questo `--migrate` si rifiutava di marcarla.
            a, b = int(groups[0]), int(groups[1])
            if a == b:
                continue
            if ydata is None:
                print(f"[apply] ⚠ {STATE_YAML_REL} assente — march_clock resta manuale")
                manual.append((name, _suggest(name, groups)))
                continue
            try:
                from dmcore.statedata import StateDataError, imposta_campo_oggetto
                nuovo_yaml = imposta_campo_oggetto(
                    ydata, "march_clock", "giorno_corrente", b)
            except StateDataError as exc:
                print(f"[apply] ⚠ march_clock non applicabile ({exc}) — resta manuale")
                manual.append((name, _suggest(name, groups)))
                continue
            if nuovo_yaml == ydata:
                print(f"[apply] march clock già a Day {b} — niente da fare (idempotente)")
                continue
            print(f"\n[apply] proposta march_clock: Day {a} → Day {b} "
                  f"(in {STATE_YAML_REL})")
            print(_diff(ydata, nuovo_yaml, str(STATE_YAML_REL)))
            if _confirm("[apply] applico questo blocco?", assume_yes):
                ydata = nuovo_yaml
                applied.append(f"March Clock Day {a} → Day {b}")
            else:
                manual.append((name, _suggest(name, groups)))
        elif name in STATO_DA_TRIGGER:
            if ydata is None:
                print(f"[apply] ⚠ {STATE_YAML_REL} assente — {name} resta manuale")
                manual.append((name, _suggest(name, groups)))
                continue
            esito = _stato_villain(ydata, name, groups)
            if esito is None:
                print(f"[apply] ⚠ {name} «{groups[0]}»: nessun villain di §3 "
                      f"identificato con certezza (o già a posto) — resta manuale")
                manual.append((name, _suggest(name, groups)))
                continue
            indice, valore, etichetta = esito
            try:
                from dmcore.statedata import StateDataError, imposta_campo
                nuovo_yaml = imposta_campo(ydata, "villain", indice, "stato", valore)
            except StateDataError as exc:
                print(f"[apply] ⚠ {etichetta} non applicabile ({exc}) — resta manuale")
                manual.append((name, _suggest(name, groups)))
                continue
            print(f"\n[apply] proposta {name} → {STATE_YAML_REL} (§3 villain)")
            print(_diff(ydata, nuovo_yaml, str(STATE_YAML_REL)))
            print(f"[apply] ⚠ `reversibile` NON viene scritto: se il canone "
                  f"prevede un ritorno lo dice il DM, e la regola R9 di "
                  f"`validate_state` lo chiederà alla prossima esecuzione.")
            if _confirm("[apply] applico questo blocco?", assume_yes):
                ydata = nuovo_yaml
                applied.append(etichetta)
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
