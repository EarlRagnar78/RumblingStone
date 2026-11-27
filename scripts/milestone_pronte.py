#!/usr/bin/env python3
"""milestone_pronte.py — quale milestone della roadmap è pronta per il rilascio?

Le milestone vivono su GitHub (1-5, v1.1.0…v1.5.0), ma i loro criteri d'uscita
stavano solo nella descrizione, in prosa: nessuno poteva dire senza rileggerle
tutte se una era finita. `plans/milestone.json` li tiene in forma che una
macchina legge (lo schema è in `_schema`, in testa al file), e questo script li
valuta. Misura e basta: non scrive niente, non apre issue, non tocca GitHub.

Tre tipi di criterio, ognuno vero o falso:

- **comando**: si lancia dalla radice del repo, con `shlex` e mai con una
  shell; vero se esce 0. `python`/`python3` in testa diventa l'interprete che
  sta girando questo script. Oltre `--timeout` (300 s) è falso. Lo stesso
  comando in più milestone (i criteri comuni) si esegue una volta sola.
- **file**: `file` e `regex` (uno o una lista), `deve` = `comparire` (ogni
  regex trova almeno una riga in ogni file) o `mancare` (nessuna trova niente
  in nessun file). `re.MULTILINE`.
- **dm**: vero solo se `confermato` è `{data, dove}`; `null` è falso.

Una milestone è **pronta** se tutti i criteri sono veri tranne i tre del
rilascio stesso (`fatto-changelog`, `fatto-versione`, `fatto-tag`), e
**rilasciata** se sono veri anche quelli; altrimenti **non pronta**, con l'id
dei criteri falsi.

Il registro è **rotto** (exit 2, sempre, prima di valutare) se non è JSON, se
un file citato manca o non è UTF-8, se una regex non compila, se un id o un
numero di milestone è doppio, se lo script o il programma di un `comando` non
esiste, se un tipo o un `deve` è sconosciuto, se un `confermato` non ha `data`
e `dove`. Un file mancante è un errore del registro e non un «vero» di
`mancare`: altrimenti un rinomina farebbe passare il criterio in silenzio.

    python3 scripts/milestone_pronte.py                   # tabella
    python3 scripts/milestone_pronte.py --json            # tutto, per il workflow
    python3 scripts/milestone_pronte.py --pronte          # versioni pronte, una per riga
    python3 scripts/milestone_pronte.py --check --solo-integrita   # solo il registro
    python3 scripts/milestone_pronte.py --github          # confronta con le milestone di GitHub

`--github` chiede a `gh api repos/{owner}/{repo}/milestones?state=all` numero e
titolo di ogni milestone e li confronta col registro; senza `gh`, o se la
chiamata fallisce, dice «non misurato» e non cambia l'uscita.

Exit: 0 registro integro (anche se niente è pronto: è una misura, canale
testing di ADR-0099) · 2 registro rotto o errore d'uso. Solo stdlib.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
REGISTRO = Path("plans") / "milestone.json"
RILASCIO = ("fatto-changelog", "fatto-versione", "fatto-tag")
TIPI = ("comando", "file", "dm")
DEVE = ("comparire", "mancare")
TIMEOUT = 300
PYTHON = ("python", "python3")
DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _lista(v) -> list:
    return v if isinstance(v, list) else [v]


def _argv(comando: str) -> list[str]:
    argv = shlex.split(comando)
    if argv and argv[0] in PYTHON:
        argv[0] = sys.executable
    return argv


# ---------------------------------------------------------------- integrità

def integrita(reg, radice: Path) -> list[str]:
    """Gli errori del registro, vuoti se è integro. Non esegue niente."""
    if not isinstance(reg, dict) or not isinstance(reg.get("milestone"), list):
        return ["manca la lista «milestone»"]
    errori: list[str] = []
    numeri: set = set()
    versioni: set = set()
    for i, m in enumerate(reg["milestone"]):
        dove = f"milestone[{i}]"
        if not isinstance(m, dict):
            errori.append(f"{dove}: non è un oggetto")
            continue
        for campo in ("numero", "versione", "titolo", "criteri"):
            if campo not in m:
                errori.append(f"{dove}: manca «{campo}»")
        if "numero" in m:
            dove = f"M{m['numero']}"
            if m["numero"] in numeri:
                errori.append(f"{dove}: numero doppio")
            numeri.add(m["numero"])
        if m.get("versione") in versioni:
            errori.append(f"{dove}: versione {m['versione']} doppia")
        versioni.add(m.get("versione"))
        criteri = m.get("criteri")
        if not isinstance(criteri, list):
            errori.append(f"{dove}: «criteri» non è una lista")
            continue
        ids: set = set()
        for c in criteri:
            cid = c.get("id") if isinstance(c, dict) else None
            if not cid:
                errori.append(f"{dove}: criterio senza id")
                continue
            if cid in ids:
                errori.append(f"{dove}/{cid}: id doppio")
            ids.add(cid)
            errori += [f"{dove}/{cid}: {e}" for e in _integrita_criterio(c, radice)]
    return errori


def _integrita_criterio(c: dict, radice: Path) -> list[str]:
    tipo = c.get("tipo")
    if tipo not in TIPI:
        return [f"tipo sconosciuto {tipo!r} (ammessi: {', '.join(TIPI)})"]
    if tipo == "comando":
        try:
            argv = shlex.split(c.get("comando") or "")
        except ValueError as e:
            return [f"comando che shlex non legge: {e}"]
        if not argv:
            return ["comando vuoto"]
        if argv[0] in PYTHON:
            if len(argv) < 2 or argv[1].startswith("-"):
                return []  # python -c / -m: niente file da controllare
            if not (radice / argv[1]).is_file():
                return [f"lo script {argv[1]} non esiste"]
            return []
        if shutil.which(argv[0]) is None and not (radice / argv[0]).is_file():
            return [f"il programma {argv[0]} non c'è"]
        return []
    if tipo == "dm":
        conf = c.get("confermato", "manca")
        if conf == "manca":
            return ["manca «confermato» (null o {data, dove})"]
        if conf is None:
            return []
        if not isinstance(conf, dict) or not conf.get("dove") or \
                not DATA.match(str(conf.get("data", ""))):
            return ["«confermato» vuole {\"data\": \"AAAA-MM-GG\", \"dove\": \"…\"}"]
        return []
    # file
    errori: list[str] = []
    if c.get("deve") not in DEVE:
        errori.append(f"deve {c.get('deve')!r} sconosciuto (ammessi: {', '.join(DEVE)})")
    if not c.get("file") or not c.get("regex"):
        errori.append("servono «file» e «regex»")
        return errori
    for r in _lista(c["regex"]):
        try:
            re.compile(r, re.MULTILINE)
        except (re.error, TypeError) as e:
            errori.append(f"regex {r!r} non compila: {e}")
    for f in _lista(c["file"]):
        p = radice / f
        if not p.is_file():
            errori.append(f"il file {f} non esiste")
            continue
        try:
            p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errori.append(f"il file {f} non è UTF-8")
    return errori


# --------------------------------------------------------------- valutazione

def _valuta_file(c: dict, radice: Path) -> tuple[bool, str]:
    trovati, mancati = [], []
    for f in _lista(c["file"]):
        testo = (radice / f).read_text(encoding="utf-8")
        for r in _lista(c["regex"]):
            (trovati if re.search(r, testo, re.MULTILINE) else mancati).append(
                f"{Path(f).name}: {r[:40]}")
    if c["deve"] == "comparire":
        return not mancati, ("non trova " + "; ".join(mancati)) if mancati else "trova tutte"
    return not trovati, ("trova " + "; ".join(trovati)) if trovati else "nessuna"


def _valuta_comando(c: dict, radice: Path, timeout: float, memo: dict) -> tuple[bool, str, float]:
    cmd = c["comando"]
    if cmd not in memo:
        inizio = time.monotonic()
        try:
            p = subprocess.run(_argv(cmd), cwd=radice, capture_output=True, text=True,
                               timeout=timeout)
            esito = (p.returncode == 0, f"exit {p.returncode}")
        except subprocess.TimeoutExpired:
            esito = (False, f"timeout dopo {timeout:g} s")
        except OSError as e:
            esito = (False, f"non parte: {e}")
        memo[cmd] = (*esito, round(time.monotonic() - inizio, 2))
    return memo[cmd]


def valuta(reg: dict, radice: Path, timeout: float = TIMEOUT) -> list[dict]:
    memo: dict = {}
    uscita = []
    for m in reg["milestone"]:
        criteri = []
        for c in m["criteri"]:
            voce = {"id": c["id"], "tipo": c["tipo"], "testo": c.get("testo", ""),
                    "comune": bool(c.get("comune")), "rilascio": c["id"] in RILASCIO}
            if c["tipo"] == "comando":
                vero, det, secondi = _valuta_comando(c, radice, timeout, memo)
                voce["secondi"] = secondi
            elif c["tipo"] == "file":
                vero, det = _valuta_file(c, radice)
            else:
                conf = c.get("confermato")
                vero = conf is not None
                det = f"confermato il {conf['data']} ({conf['dove']})" if vero else "non confermato"
            voce.update(vero=vero, dettaglio=det)
            criteri.append(voce)
        falsi = [c["id"] for c in criteri if not c["vero"] and not c["rilascio"]]
        if falsi:
            stato = "non pronta"
        elif all(c["vero"] for c in criteri):
            stato = "rilasciata"
        else:
            stato = "pronta"
        uscita.append({"numero": m["numero"], "versione": m["versione"], "titolo": m["titolo"],
                       "stato": stato, "falsi": falsi, "criteri": criteri})
    return uscita


# -------------------------------------------------------------------- github

def confronta_github(reg: dict, radice: Path) -> dict:
    """Numero e titolo del registro contro le milestone di GitHub."""
    if shutil.which("gh") is None:
        return {"esito": "non misurato", "motivo": "gh non è installato"}
    try:
        p = subprocess.run(["gh", "api", "--paginate", "--jq", ".[] | {number, title}",
                            "repos/{owner}/{repo}/milestones?state=all&per_page=100"],
                           cwd=radice, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"esito": "non misurato", "motivo": str(e)}
    if p.returncode != 0:
        return {"esito": "non misurato", "motivo": (p.stderr.strip() or f"exit {p.returncode}")[:200]}
    try:
        # --jq: un oggetto per riga, su tutte le pagine
        su_gh = {g["number"]: g["title"]
                 for g in map(json.loads, p.stdout.splitlines()) if g}
    except (ValueError, KeyError, TypeError) as e:
        return {"esito": "non misurato", "motivo": f"risposta illeggibile: {e}"}
    rilievi = []
    for m in reg["milestone"]:
        if m["numero"] not in su_gh:
            rilievi.append(f"M{m['numero']} non c'è su GitHub")
        elif su_gh[m["numero"]] != m["titolo"]:
            rilievi.append(f"M{m['numero']}: su GitHub «{su_gh[m['numero']]}», "
                           f"nel registro «{m['titolo']}»")
    nel_registro = {m["numero"] for m in reg["milestone"]}
    rilievi += [f"M{n} «{t}» è su GitHub e non nel registro"
                for n, t in sorted(su_gh.items()) if n not in nel_registro]
    return {"esito": "coincide" if not rilievi else "diverge", "rilievi": rilievi}


# -------------------------------------------------------------------- uscita

def tabella(esiti: list[dict]) -> str:
    righe = ["| M | Versione | Stato | Criteri falsi |", "|---|---|---|---|"]
    for m in esiti:
        falsi = ", ".join(f"`{i}`" for i in m["falsi"]) or "—"
        righe.append(f"| {m['numero']} | {m['versione']} | {m['stato']} | {falsi} |")
    return "\n".join(righe)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    modo = ap.add_mutually_exclusive_group()
    modo.add_argument("--json", action="store_true", help="ogni milestone, stato, criteri ed esito")
    modo.add_argument("--pronte", action="store_true",
                      help="solo le versioni pronte e non rilasciate, una per riga")
    ap.add_argument("--check", action="store_true",
                    help="esce 2 se il registro è rotto, 0 altrimenti (è una misura)")
    ap.add_argument("--solo-integrita", action="store_true",
                    help="controlla il registro senza eseguire i comandi né valutare")
    ap.add_argument("--github", action="store_true",
                    help="confronta numero e titolo con le milestone di GitHub (serve gh)")
    ap.add_argument("--registro", type=Path, help="default: <radice>/plans/milestone.json")
    ap.add_argument("--radice", type=Path, default=RADICE, help="la radice del repo da misurare")
    ap.add_argument("--timeout", type=float, default=TIMEOUT,
                    help=f"secondi per ogni comando (default {TIMEOUT})")
    a = ap.parse_args(argv)

    radice = a.radice.resolve()
    percorso = a.registro or radice / REGISTRO
    try:
        reg = json.loads(percorso.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"✗ registro illeggibile: {percorso}: {e}", file=sys.stderr)
        return 2
    errori = integrita(reg, radice)
    if errori:
        print(f"✗ registro rotto ({percorso}): {len(errori)} errori", file=sys.stderr)
        for e in errori:
            print(f"  - {e}", file=sys.stderr)
        return 2
    if a.solo_integrita:
        n = sum(len(m["criteri"]) for m in reg["milestone"])
        print(f"✓ registro integro: {len(reg['milestone'])} milestone, {n} criteri")
        return 0

    esiti = valuta(reg, radice, a.timeout)
    pronte = [m["versione"] for m in esiti if m["stato"] == "pronta"]
    github = confronta_github(reg, radice) if a.github else None

    if a.pronte:
        for v in pronte:
            print(v)
    elif a.json:
        dati = {"registro": str(percorso), "integro": True, "errori": [],
                "milestone": esiti, "pronte": pronte}
        if github is not None:
            dati["github"] = github
        print(json.dumps(dati, ensure_ascii=False, indent=2))
    else:
        print(tabella(esiti))
        if github is not None:
            print(f"\nGitHub: {github['esito']}"
                  + (f" ({github['motivo']})" if "motivo" in github else ""))
            for r in github.get("rilievi", []):
                print(f"  - {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
