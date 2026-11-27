#!/usr/bin/env python3
"""documentazione_allineata.py — la documentazione segue la struttura (ADR-0153).

Scopo
  Un elemento strutturale nuovo del repo entra con la riga che lo cita nel suo
  indice. Nasce dall'audit del 27/11/2026: dopo la #510 `AGENTS.md` non nominava
  nessuno dei tredici agenti, `docs/INDEX.md` non nominava tre script nuovi, e
  nessun cancello se ne accorgeva.

Cosa controlla
  Ogni elemento e il suo indice:
    agente    `.claude/agents/X.md`               → `X` in `AGENTS.md`
    script    `scripts/X.py`, `scripts/X.sh`      → `X.py` / `X.sh` in `docs/INDEX.md`
              (solo il primo livello di `scripts/`)
    workflow  `.github/workflows/X.yml`           → `X.yml` in `docs/INDEX.md`
    hook      ogni `command` di `.claude/settings.json` → il nome dello script
              che lancia in `docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md`
  Un nome si cerca intero: `nuovo-agente-bis` non cita `nuovo-agente`.
  Gli ADR fuori da `docs/INDEX.md` non si ricontano qui: li conta
  `validate_docs.indice_adr()` (una norma, un rilevatore), e questo script ne
  riporta il risultato nel debito.

Uso
  python3 scripts/documentazione_allineata.py --rispetto-a origin/main
  python3 scripts/documentazione_allineata.py --debito [--json]
  python3 scripts/documentazione_allineata.py --debito --check

  --rispetto-a REF  solo gli elementi aggiunti rispetto a REF
                    (`git diff --diff-filter=A --no-renames REF...HEAD`; per gli
                    hook, gli script presenti nel settings di HEAD e assenti in
                    quello di REF). È il passo della CI sulle PR: il debito
                    vecchio non boccia.
  --debito          tutto il repo; con --json il dettaglio, compreso l'ultimo ADR
                    citato in `docs/explanation/ARCHITETTURA.md` contro l'ultimo
                    su disco (riportato, non contato nel totale).
  --check           con --debito: confronta il totale con il tetto di
                    `plans/debito-documentazione.json` (cricchetto: il tetto si
                    abbassa a mano quando il debito scende, mai si alza).
  --radice DIR      il repo da leggere (default: questo); serve ai test.

Input   `.claude/agents/`, `scripts/`, `.github/workflows/`, `.claude/settings.json`,
        gli indici qui sopra, `plans/adr/`, `plans/debito-documentazione.json`
Output  stdout testuale, oppure JSON con --debito --json
Exit    0 = niente di nuovo scoperto (o debito entro il tetto) · 1 = un elemento
        nuovo non citato, o debito oltre il tetto · 2 = errore d'uso (REF che
        non esiste, git assente, tetto illeggibile)
"""
from __future__ import annotations

import argparse
import contextlib
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_docs as vd  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

INDICE_AGENTI = "AGENTS.md"
INDICE_SCRIPT = "docs/INDEX.md"
INDICE_HOOK = "docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md"
SETTINGS = ".claude/settings.json"
ARCHITETTURA = "docs/explanation/ARCHITETTURA.md"
TETTO = "plans/debito-documentazione.json"
DIFF_DA_PASSARE = "chiama l'agente autore-documenti con il diff"

_AGENTE = re.compile(r"^\.claude/agents/([^/]+)\.md$")
_SCRIPT = re.compile(r"^scripts/([^/]+\.(?:py|sh))$")
_WORKFLOW = re.compile(r"^\.github/workflows/([^/]+\.ya?ml)$")
_ADR = re.compile(r"ADR-(\d{4})")


class ErroreUso(Exception):
    pass


def _git(radice: Path, *args: str) -> str:
    try:
        p = subprocess.run(["git", "-C", str(radice), *args], capture_output=True, text=True)
    except OSError as e:
        raise ErroreUso(f"git non disponibile: {e}") from e
    if p.returncode != 0:
        raise ErroreUso(f"git {' '.join(args)}: {p.stderr.strip()}")
    return p.stdout


def elemento(percorso: str) -> "tuple[str, str, str] | None":
    """(tipo, nome da cercare, indice) di un file strutturale, o None."""
    for regex, tipo, indice in ((_AGENTE, "agente", INDICE_AGENTI),
                                (_SCRIPT, "script", INDICE_SCRIPT),
                                (_WORKFLOW, "workflow", INDICE_SCRIPT)):
        m = regex.match(percorso)
        if m:
            return tipo, m.group(1), indice
    return None


def script_degli_hook(settings: str) -> "list[str]":
    """Il nome del file che ogni `command` dei gruppi `hooks` lancia, in ordine."""
    try:
        d = json.loads(settings)
    except ValueError:
        return []
    out: "list[str]" = []
    for gruppi in (d.get("hooks") or {}).values():
        for g in gruppi or []:
            for h in (g or {}).get("hooks") or []:
                try:
                    parole = shlex.split(str(h.get("command", "")))
                except ValueError:
                    parole = str(h.get("command", "")).split()
                for p in parole:
                    if re.search(r"\.(py|sh)$", p):
                        nome = p.rsplit("/", 1)[-1]
                        if nome not in out:
                            out.append(nome)
                        break
    return out


def citato(nome: str, testo: str) -> bool:
    return re.search(rf"(?<![\w-]){re.escape(nome)}(?![\w-])", testo) is not None


def _leggi(radice: Path, percorso: str) -> str:
    try:
        return (radice / percorso).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def scoperti(radice: Path, elementi: "list[tuple[str, str, str, str]]") -> "list[dict]":
    """Gli elementi (tipo, percorso, nome, indice) che il loro indice non cita."""
    testi: "dict[str, str]" = {}
    out = []
    for tipo, percorso, nome, indice in elementi:
        if indice not in testi:
            testi[indice] = _leggi(radice, indice)
        if not citato(nome, testi[indice]):
            out.append({"tipo": tipo, "percorso": percorso, "indice": indice})
    return out


def elementi_aggiunti(radice: Path, ref: str) -> "list[tuple[str, str, str, str]]":
    _git(radice, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    nomi = _git(radice, "diff", "--diff-filter=A", "--no-renames", "--name-only",
                f"{ref}...HEAD").splitlines()
    out = []
    for p in nomi:
        e = elemento(p.strip())
        if e:
            out.append((e[0], p.strip(), e[1], e[2]))
    try:
        prima = _git(radice, "show", f"{ref}:{SETTINGS}")
    except ErroreUso:
        prima = "{}"
    vecchi = set(script_degli_hook(prima))
    for nome in script_degli_hook(_leggi(radice, SETTINGS)):
        if nome not in vecchi:
            out.append(("hook", f"{SETTINGS} → {nome}", nome, INDICE_HOOK))
    return out


def elementi_tutti(radice: Path) -> "list[tuple[str, str, str, str]]":
    out = []
    for cartella, schema in ((".claude/agents", "*.md"), ("scripts", "*.py"),
                             ("scripts", "*.sh"), (".github/workflows", "*.yml"),
                             (".github/workflows", "*.yaml")):
        for f in sorted((radice / cartella).glob(schema)):
            p = f.relative_to(radice).as_posix()
            e = elemento(p)
            if e and f.is_file():
                out.append((e[0], p, e[1], e[2]))
    for nome in script_degli_hook(_leggi(radice, SETTINGS)):
        out.append(("hook", f"{SETTINGS} → {nome}", nome, INDICE_HOOK))
    return out


@contextlib.contextmanager
def _radice_di_validate_docs(radice: Path):
    vecchia = vd.ROOT
    vd.ROOT = radice
    try:
        yield
    finally:
        vd.ROOT = vecchia


def adr_fuori_indice(radice: Path) -> "list[str]":
    """Gli ADR che `validate_docs.indice_adr()` trova fuori da `docs/INDEX.md`."""
    with _radice_di_validate_docs(radice):
        return [x["path"] for x in vd.indice_adr()]


def architettura(radice: Path) -> dict:
    citati = _ADR.findall(_leggi(radice, ARCHITETTURA))
    su_disco = [m.group(1) for f in (radice / vd.CARTELLA_ADR).glob("ADR-*.md")
                if (m := _ADR.match(f.name))]
    return {"ultimo_adr_citato": max(citati, default=None),
            "ultimo_adr": max(su_disco, default=None)}


def debito(radice: Path) -> dict:
    s = scoperti(radice, elementi_tutti(radice))
    a = adr_fuori_indice(radice)
    return {"totale": len(s) + len(a), "scoperti": s, "adr_fuori_indice": a,
            "architettura": architettura(radice)}


def tetto(radice: Path) -> dict:
    try:
        d = json.loads((radice / TETTO).read_text(encoding="utf-8"))
        int(d["tetto"])
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise ErroreUso(f"{TETTO} illeggibile: {e}") from e
    return d


def _stampa_scoperti(righe: "list[dict]") -> None:
    for s in righe:
        print(f"  {s['tipo']:<8} {s['percorso']}  → manca in {s['indice']}")


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    modo = ap.add_mutually_exclusive_group(required=True)
    modo.add_argument("--rispetto-a", metavar="REF",
                      help="solo gli elementi aggiunti rispetto a REF (CI sulle PR)")
    modo.add_argument("--debito", action="store_true", help="tutto il repo")
    ap.add_argument("--json", action="store_true", help="con --debito: uscita JSON")
    ap.add_argument("--check", action="store_true",
                    help=f"con --debito: esce 1 se il totale supera il tetto di {TETTO}")
    ap.add_argument("--radice", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    radice = args.radice.resolve()
    if (args.json or args.check) and not args.debito:
        print("--json e --check valgono solo con --debito", file=sys.stderr)
        return 2
    try:
        if args.rispetto_a:
            nuovi = elementi_aggiunti(radice, args.rispetto_a)
            fuori = scoperti(radice, nuovi)
            if not fuori:
                print(f"Documentazione allineata: {len(nuovi)} elementi strutturali nuovi "
                      f"rispetto a {args.rispetto_a}, tutti citati nel loro indice.")
                return 0
            print(f"Documentazione indietro (ADR-0153): {len(fuori)} elementi strutturali "
                  f"nuovi rispetto a {args.rispetto_a} non sono citati nel loro indice.")
            _stampa_scoperti(fuori)
            print(f"Aggiorna gli indici: {DIFF_DA_PASSARE} e con queste righe.")
            return 1
        d = debito(radice)
        if args.json:
            print(json.dumps(d, ensure_ascii=False, indent=2))
        else:
            a = d["architettura"]
            print(f"Debito di documentazione: {d['totale']} "
                  f"({len(d['scoperti'])} elementi non citati, "
                  f"{len(d['adr_fuori_indice'])} ADR fuori da {vd.INDICE_ADR}).")
            _stampa_scoperti(d["scoperti"])
            for p in d["adr_fuori_indice"]:
                print(f"  adr      {p}  → manca in {vd.INDICE_ADR}")
            print(f"{ARCHITETTURA}: ultimo ADR citato {a['ultimo_adr_citato']}, "
                  f"ultimo su disco {a['ultimo_adr']}.")
        if args.check:
            t = tetto(radice)
            if d["totale"] > int(t["tetto"]):
                print(f"Debito {d['totale']} oltre il tetto {t['tetto']} di {TETTO} "
                      f"(misurato {t.get('misurato', '?')}): {DIFF_DA_PASSARE}.",
                      file=sys.stderr)
                return 1
            if not args.json:
                print(f"Entro il tetto {t['tetto']} di {TETTO}.")
        return 0
    except ErroreUso as e:
        print(f"errore: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
