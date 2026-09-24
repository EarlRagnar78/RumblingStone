#!/usr/bin/env python3
"""contenuti_nei_rami.py — i file che esistono in un ramo e mai su `main`.

Il 2026-09-24 il DM ha chiesto di controllare che niente si fosse perso «in
tutte le PR, anche quelle chiuse». A mano ha trovato due casi che nessun
documento nominava: `validate_skill_paths.py`, spinto sul ramo della PR #1
dopo il merge, e il soggetto della discesa nell'Underdark, 773 righe rimaste
nella #72. Questo script rifa' quella misura, cosi' la prossima volta non la
rifa' nessuno a mano (PIANO-RIPRESA-PR-ABBANDONATE §4.11, lotto 4i-2).

Cosa conta come «mai arrivato»: un file di un ramo il cui percorso non compare
in nessun commit di `main` E il cui contenuto (il blob) non c'e' in nessun
commit di `main`. Un file rinominato o rinumerato col contenuto identico non
e' perso; un file riscritto con un altro nome si', e il registro dice dove.

Il registro, `plans/contenuti-nei-rami.json`, da' un posto a ogni riga: un
ramo intero (una PR aperta che un piano segue, il ramo di un gruppo) o un file
solo, con uno stato e il documento che ne risponde. Una riga senza posto e' il
caso che si cerca.

⚠️ Limiti dichiarati:
  * vede i FILE, non le modifiche: un commit dopo il merge che corregge un file
    gia' su `main` non compare;
  * vede i rami che il clone conosce. `--fetch` scarica le teste di tutte le
    PR, chiuse comprese, e i rami di `origin`;
  * non e' un gate di CI e non deve diventarlo: i rami cambiano per conto
    loro, e una PR diventerebbe rossa per il lavoro di un'altra.

Uso:
    python3 scripts/contenuti_nei_rami.py --fetch     # aggiorna i rami, poi misura
    python3 scripts/contenuti_nei_rami.py             # misura su cio' che c'e'
    python3 scripts/contenuti_nei_rami.py --check     # esce 1 se una riga non ha posto
    python3 scripts/contenuti_nei_rami.py --json

Exit code: 0 = ogni riga ha un posto · 1 = righe senza posto (solo con
--check) o registro malformato · 2 = uso errato.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_docs as vd  # noqa: E402

ROOT = vd.ROOT
REGISTRO = ROOT / "plans" / "contenuti-nei-rami.json"

#: Gli stati ammessi, e cosa vogliono dire. Uno stato nuovo si aggiunge qui.
STATI = {
    "in-volo": "sta in una PR aperta che un piano segue",
    "portato": "e' arrivato su main con un altro nome o numero",
    "superato": "c'e' su main qualcosa che fa lo stesso lavoro",
    "rifiutato": "deciso di non portarlo, e scritto perche'",
    "partita": "ramo di un gruppo: e' partita, non prodotto (ADR-0007)",
    "da-decidere": "aspetta una decisione del DM",
}


def _git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def fetch() -> None:
    _git("fetch", "--quiet", "origin",
         "+refs/heads/*:refs/remotes/origin/*",
         "+refs/pull/*/head:refs/remotes/pr/*")


def riferimenti(base: str) -> "list[str]":
    refs = _git("for-each-ref", "--format=%(refname:short)", "refs/remotes/").split()
    return sorted(r for r in refs if not r.endswith("/HEAD") and r != base)


def mai_arrivati(base: str, refs: "list[str]") -> "dict[str, list[str]]":
    """{percorso: [ref, ...]} dei file che `base` non ha mai avuto."""
    percorsi_base = set(_git("log", base, "--name-only", "--format=").splitlines())
    oggetti_base = {r.split(" ", 1)[0] for r in _git("rev-list", "--objects", base).splitlines()}
    trovati: "dict[str, set[str]]" = defaultdict(set)
    for ref in refs:
        for riga in _git("ls-tree", "-r", ref).splitlines():
            meta, percorso = riga.split("\t", 1)
            blob = meta.split()[2]
            if percorso in percorsi_base or blob in oggetti_base:
                continue
            if vd._e_generato(percorso) or vd._is_generated_mirror(percorso):
                continue
            trovati[percorso].add(ref)
    return {p: sorted(r) for p, r in sorted(trovati.items())}


def leggi_registro(percorso: "Path | None" = None) -> dict:
    # Il default si risolve qui e non nella firma: legato alla definizione,
    # un test che sostituisce REGISTRO avrebbe letto comunque quello del repo.
    dati = json.loads((percorso or REGISTRO).read_text(encoding="utf-8"))
    errori = []
    for sezione, chiave in (("rami", "ref"), ("file", "percorso")):
        for voce in dati.get(sezione, []):
            if voce.get("stato") not in STATI:
                errori.append(f"{sezione}: {voce.get(chiave)}: stato «{voce.get('stato')}» "
                              f"non ammesso ({', '.join(STATI)})")
            if not voce.get("dove"):
                errori.append(f"{sezione}: {voce.get(chiave)}: manca «dove» (chi ne risponde)")
    if errori:
        raise ValueError("registro malformato:\n  · " + "\n  · ".join(errori))
    return dati


def posto(percorso: str, refs: "list[str]", registro: dict) -> "dict | None":
    """La voce che da' un posto al file, o None. Il file vince sul ramo."""
    for voce in registro.get("file", []):
        if voce["percorso"] == percorso:
            return voce
    def voce_del_ramo(ref: str) -> "dict | None":
        for voce in registro.get("rami", []):
            modelli = voce["ref"] if isinstance(voce["ref"], list) else [voce["ref"]]
            if any(fnmatch.fnmatchcase(ref, m) for m in modelli):
                return voce
        return None

    # Un file che sta in piu' rami ha un posto se ce l'ha in OGNUNO: basta un
    # ramo scoperto perche' quella copia possa essere l'unica diversa.
    voci = [voce_del_ramo(r) for r in refs]
    return voci[0] if voci and all(voci) else None


def confronta(trovati: "dict[str, list[str]]", registro: dict) -> dict:
    senza, per_stato = [], defaultdict(list)
    for percorso, refs in trovati.items():
        voce = posto(percorso, refs, registro)
        if voce is None:
            senza.append({"percorso": percorso, "rami": refs})
        else:
            per_stato[voce["stato"]].append(percorso)
    # Una voce di file che non trova piu' niente e' arrivata su main o il ramo
    # e' sparito: il registro va potato, se no racconta una cosa finita.
    scadute = [v["percorso"] for v in registro.get("file", []) if v["percorso"] not in trovati]
    return {"senza_posto": senza, "per_stato": dict(per_stato), "scadute": scadute}


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--fetch", action="store_true",
                    help="scarica prima le teste di tutte le PR e i rami di origin")
    ap.add_argument("--check", action="store_true",
                    help="esce 1 se un file mai arrivato non ha un posto nel registro")
    ap.add_argument("--base", default="origin/main", help="il ramo di riferimento")
    ap.add_argument("--json", action="store_true", help="report in JSON")
    args = ap.parse_args(argv)

    try:
        registro = leggi_registro()
    except (OSError, ValueError) as exc:
        print(f"✗ contenuti_nei_rami: {exc}", file=sys.stderr)
        return 1
    if args.fetch:
        fetch()
    try:
        _git("rev-parse", "--verify", "--quiet", args.base)
    except RuntimeError:
        print(f"○ contenuti_nei_rami: il clone non ha {args.base} "
              "(checkout della CI? usare --fetch). Niente da misurare.")
        return 0
    refs = riferimenti(args.base)
    if not refs:
        print("○ contenuti_nei_rami: il clone non conosce altri rami "
              "(clone shallow? usare --fetch). Niente da misurare.")
        return 0
    trovati = mai_arrivati(args.base, refs)
    esito = confronta(trovati, registro)

    if args.json:
        print(json.dumps({"riferimenti": len(refs), "percorsi": len(trovati), **esito},
                         ensure_ascii=False, indent=2))
    else:
        conti = " · ".join(f"{s} {len(v)}" for s, v in sorted(esito["per_stato"].items()))
        print(f"contenuti_nei_rami: {len(refs)} riferimenti, {len(trovati)} file mai "
              f"arrivati su {args.base} — {conti or 'nessuno'}")
        for p in esito["per_stato"].get("da-decidere", []):
            print(f"  ⏳ da decidere: {p}")
        for voce in esito["senza_posto"]:
            print(f"  ✗ senza posto: {voce['percorso']}  ← {', '.join(voce['rami'])}")
        for p in esito["scadute"]:
            print(f"  ⚠ nel registro ma non piu' nei rami (arrivato? ramo tolto?): {p}")
        if not esito["senza_posto"]:
            print("✓ ogni file mai arrivato ha un posto nel registro")
    return 1 if (args.check and esito["senza_posto"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
