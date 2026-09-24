#!/usr/bin/env python3
"""
gruppo_nuovo.py — un gruppo nuovo da un comando e un modulo, senza YAML a mano.

Lotto 4f-4 di PIANO-RIPRESA-PR-ABBANDONATE (D19 e D21 del DM, 2026-09-24). Il
DM risponde a domande; lo script deriva lo stato del gruppo nuovo da quello di
oggi, azzera la partita, crea il ramo `campaign-group-<gruppo>` e committa. La
logica sta in `dmcore/gruppo_nuovo.py`; qui ci sono solo il modulo in terminale
e i passi su disco e su git.

Cosa chiede:
  * il nome del gruppo, l'arco da cui parte e il livello;
  * i PG (da 1 a 6): nome, razza, classe, livello, PF;
  * le righe dello stato che portano tracce del primo tavolo e chiedono un
    giudizio, una alla volta: tieni, svuota, rivedi.
Cosa fa da solo: toglie le conoscenze sul party, i portatori degli artefatti
(che restano nel prodotto), gli echi, il giorno di marcia; rimette a zero i
clock numerici e lascia i trigger.

Ordine, e perche': si deriva e si VALIDA tutto prima di creare il ramo. Se
qualcosa non va non resta niente, ne' un ramo ne' mezzo reset.

Uso:
    python3 scripts/dm.py gruppo nuovo                    # modulo in terminale
    python3 scripts/dm.py gruppo nuovo --answers r.json   # risposte da file
    python3 scripts/dm.py gruppo nuovo --domande          # il modulo come JSON
    python3 scripts/dm.py gruppo nuovo --dry-run          # dice cosa farebbe

Exit code: 0 = fatto (o dry-run/domande) · 1 = risposte non valide, albero
sporco, ramo gia' esistente o reset fallito · 2 = uso errato.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore import REPO  # noqa: E402
from dmcore import config  # noqa: E402
from dmcore import gitio  # noqa: E402
from dmcore import gruppo_nuovo as G  # noqa: E402

INTESTAZIONE = (
    "# campaign/state.yaml — gruppo «{gruppo}», derivato con `dm.py gruppo nuovo`\n"
    "# (lotto 4f-4) dallo stato del gruppo di prima. Non si modifica a mano:\n"
    "# lo aggiornano `dm.py session end` e i suoi strumenti (ADR-0007, D19).\n\n")


def _yaml():
    import yaml
    return yaml


def _chiedi(domanda: str, predefinita: str = "") -> str:
    coda = f" [{predefinita}]" if predefinita else ""
    risposta = input(f"{domanda}{coda}: ").strip()
    return risposta or predefinita


def _scegli(domanda: str, scelte: "list[str]", predefinita: int = 1) -> str:
    print(domanda)
    for n, s in enumerate(scelte, 1):
        print(f"  {n:2}) {s}")
    while True:
        r = _chiedi("  numero", str(predefinita))
        if r.isdigit() and 1 <= int(r) <= len(scelte):
            return scelte[int(r) - 1]
        print("  ✗ un numero dell'elenco")


def modulo(base: dict, domande: "list[G.Domanda]") -> dict:
    """Il modulo in terminale. Produce lo stesso JSON di `--answers`."""
    print("\n== Gruppo nuovo · sessione 0 ==\n")
    r: dict = {"gruppo": _chiedi("Nome del gruppo (minuscole, cifre, trattini)")}
    r["arco_partenza"] = _scegli("\nDa quale arco parte?", [a["arco"] for a in base["archi"]])
    r["livello"] = _chiedi("Livello di partenza dei PG", "5")
    quanti = 0
    while not 1 <= quanti <= G.MASSIMO_PG:
        r_q = _chiedi(f"Quanti PG (1-{G.MASSIMO_PG})", "4")
        quanti = int(r_q) if r_q.isdigit() else 0
    r["pg"] = []
    for n in range(1, quanti + 1):
        print(f"\n  PG {n}")
        r["pg"].append({"nome": _chiedi("    nome"), "razza": _chiedi("    razza"),
                        "classe": _chiedi("    classe"),
                        "livello": _chiedi("    livello", str(r["livello"])),
                        "pf": _chiedi("    punti ferita")})
    print(f"\n{len(domande)} righe portano tracce del primo tavolo. Una alla volta:")
    r["righe"] = {}
    for n, d in enumerate(domande, 1):
        print(f"\n[{n}/{len(domande)}] {d.sezione} · {d.id}")
        for c in d.campi:
            print(f"    {c}: {d.testo[c]}")
        r["righe"][d.id] = _scegli("  Che ne faccio?",
                                   ["tieni", "svuota", "rivedi (resta e diventa una domanda aperta)"],
                                   predefinita=3).split()[0]
    return r


def _git(radice: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=radice, check=True, capture_output=True, text=True)


def esegui(radice: Path, risposte: dict, dry_run: bool = False) -> int:
    import azzera_partita
    import validate_state
    yaml = _yaml()

    stato = yaml.safe_load((radice / "campaign" / "state.yaml").read_text(encoding="utf-8"))
    base, domande = G.deriva(stato)
    try:
        nuovo = G.completa(base, domande, risposte)
    except G.RispostaNonValida as exc:
        print(f"[gruppo] ✗ {exc}", file=sys.stderr)
        return 1
    errori = validate_state.errori(nuovo, radice)
    if errori:
        print("[gruppo] ✗ lo stato nuovo non passerebbe validate_state:\n  · "
              + "\n  · ".join(errori), file=sys.stderr)
        return 1

    gruppo = risposte["gruppo"]
    ramo = config.group_branch(gruppo)
    conti = Counter((risposte.get("righe") or {}).get(d.id, "rivedi") for d in domande)
    print(f"[gruppo] ramo {ramo} · {len(nuovo['party'])} PG · arco «{risposte['arco_partenza']}» "
          f"· righe: {conti['tieni']} tenute, {conti['svuota']} svuotate, "
          f"{conti['rivedi']} da rivedere · conoscenze {len(stato['conoscenze'])} → "
          f"{len(nuovo['conoscenze'])}")
    if dry_run:
        print("[gruppo] dry-run: niente scritto")
        return 0

    if not gitio.is_clean(radice):
        print("[gruppo] ✗ l'albero di lavoro non e' pulito: committa o metti da parte "
              "prima, il reset committa tutto quello che trova", file=sys.stderr)
        return 1
    if gitio.branch_exists(radice, ramo):
        print(f"[gruppo] ✗ il ramo {ramo} esiste gia'", file=sys.stderr)
        return 1

    testo = INTESTAZIONE.format(gruppo=gruppo) + yaml.safe_dump(
        nuovo, allow_unicode=True, sort_keys=False, default_flow_style=False, width=100)
    partenza = gitio.current_branch(radice)
    gitio.checkout_new(radice, ramo)
    try:
        resoconto = azzera_partita.azzera(radice, testo_stato=testo)
    except azzera_partita.ResetError as exc:
        # Si torna dove si era: niente ramo a meta'.
        _git(radice, "checkout", "-f", partenza)
        _git(radice, "branch", "-D", ramo)
        print(f"[gruppo] ✗ reset fallito, ramo tolto: {exc}", file=sys.stderr)
        return 1
    config.write_group(radice, gruppo)
    _git(radice, "add", "-A", "--", "campaign")
    _git(radice, "commit", "-q", "-m", f"Gruppo {gruppo}: sessione 0 (dm.py gruppo nuovo)")
    for riga in resoconto:
        print(f"[gruppo] ✓ {riga}")
    print(f"[gruppo] ✓ ramo {ramo} creato e committato.\n"
          f"[gruppo]   Poi: git push -u origin {ramo}, e a fine della prima sessione "
          "`dm.py session end`.")
    if conti["rivedi"]:
        print(f"[gruppo]   {conti['rivedi']} righe sono domande aperte in state.yaml "
              "(`inferred`): le vedi in state.md.")
    return 0


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--answers", type=Path, help="risposte in JSON invece del modulo")
    ap.add_argument("--domande", action="store_true",
                    help="stampa il modulo come JSON (per un'interfaccia) ed esce")
    ap.add_argument("--dry-run", action="store_true", help="dice cosa farebbe, non scrive")
    ap.add_argument("--repo-root", type=Path, default=REPO, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    radice = args.repo_root.resolve()

    if args.domande:
        stato = _yaml().safe_load((radice / "campaign" / "state.yaml").read_text(encoding="utf-8"))
        base, domande = G.deriva(stato)
        print(json.dumps(G.domande_json(base, domande), ensure_ascii=False, indent=2))
        return 0
    if args.answers:
        risposte = json.loads(args.answers.read_text(encoding="utf-8"))
    else:
        stato = _yaml().safe_load((radice / "campaign" / "state.yaml").read_text(encoding="utf-8"))
        try:
            risposte = modulo(*G.deriva(stato))
        except (KeyboardInterrupt, EOFError):
            print("\n[gruppo] interrotto: niente scritto")
            return 1
    return esegui(radice, risposte, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
