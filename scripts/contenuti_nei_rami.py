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
  * senza `--righe` vede i FILE, non le modifiche: un commit che corregge un
    file gia' su `main` non compare. 🐛 Il 2026-09-24 un ramo con tre
    correzioni di canone mai arrivate (Salvatore) sembrava cancellabile per
    questo. `--righe RAMO` guarda le righe (RIPRESA-PR 4j-5): ogni riga che il
    ramo aggiunge si cerca su `main`, identica o quasi (somiglianza >= 0,9 nello
    stesso file o in un file con lo stesso nome). Una riga mancante non vuol
    dire lavoro perso: puo' essere tolta apposta o riscritta. Vuol dire che va
    letta prima di cancellare il ramo;
  * vede i rami che il clone conosce. `--fetch` scarica le teste di tutte le
    PR, chiuse comprese, e i rami di `origin`;
  * non e' un gate di CI e non deve diventarlo: i rami cambiano per conto
    loro, e una PR diventerebbe rossa per il lavoro di un'altra.

Uso:
    python3 scripts/contenuti_nei_rami.py --fetch     # aggiorna i rami, poi misura
    python3 scripts/contenuti_nei_rami.py             # misura su cio' che c'e'
    python3 scripts/contenuti_nei_rami.py --check     # esce 1 se una riga non ha posto
    python3 scripts/contenuti_nei_rami.py --json
    python3 scripts/contenuti_nei_rami.py --righe claude/un-ramo [altri...]

Exit code: 0 = ogni riga ha un posto · 1 = righe senza posto (solo con
--check), registro malformato, o un ramo con righe mai arrivate (con
--righe) · 2 = uso errato.
"""
from __future__ import annotations

import argparse
import difflib
import fnmatch
import io
import json
import os
import re
import subprocess
import sys
import tarfile
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


def _git_bytes(*args: str) -> bytes:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    if r.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout


def fetch() -> None:
    _git("fetch", "--quiet", "origin",
         "+refs/heads/*:refs/remotes/origin/*",
         "+refs/pull/*/head:refs/remotes/pr/*")


def riferimenti(base: str) -> "list[str]":
    refs = _git("for-each-ref", "--format=%(refname:short)", "refs/remotes/").split()
    return sorted(r for r in refs if not r.endswith("/HEAD") and r != base)


def _ref_esiste(ref: str) -> bool:
    try:
        _git("rev-parse", "--verify", "--quiet", ref)
        return True
    except RuntimeError:
        return False


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


# --- le righe, non i file (RIPRESA-PR 4j-5) ----------------------------------

#: Immagini e SVG generati non si confrontano riga per riga.
NON_TESTO = re.compile(r"\.(svg|png|jpe?g|webp|pdf|gif|pcg|zip|typ)$", re.I)
SIMILE = 0.9


def _norm(riga: str) -> str:
    return re.sub(r"\s+", " ", riga.strip())


def indice_righe(base: str) -> tuple[set, dict, dict]:
    """(tutte le righe di `base`, righe per file, file per nome)."""
    tutte: set = set()
    per_file: dict = {}
    per_nome: dict = defaultdict(list)
    tar = tarfile.open(fileobj=io.BytesIO(_git_bytes("archive", base)))
    for m in tar.getmembers():
        if not m.isfile() or NON_TESTO.search(m.name):
            continue
        try:
            testo = tar.extractfile(m).read().decode("utf-8")
        except UnicodeDecodeError:
            continue
        righe = [_norm(r) for r in testo.splitlines() if _norm(r)]
        tutte.update(righe)
        per_file[m.name] = righe
        per_nome[os.path.basename(m.name)].append(m.name)
    return tutte, per_file, per_nome


def righe_mai_arrivate(ref: str, base: str, indice) -> dict:
    """Le righe che `ref` aggiunge dal punto d'incontro con `base`, classificate."""
    tutte, per_file, per_nome = indice
    punto = _git("merge-base", base, ref).strip()
    cur, tot, identiche, quasi, mancanti = None, 0, 0, 0, []
    for riga in _git("diff", "--no-renames", "-U0", punto, ref).splitlines():
        if riga.startswith("+++ "):
            cur = riga[6:].rstrip("\t").strip('"') if riga.startswith("+++ b/") else None
            if cur and NON_TESTO.search(cur):
                cur = None
            continue
        if cur is None or not riga.startswith("+"):
            continue
        s = _norm(riga[1:])
        if len(s) < 4 or re.fullmatch(r"[-|:=*#`>_ .~]+", s):
            continue
        tot += 1
        if s in tutte:
            identiche += 1
            continue
        cand = per_file.get(cur) or [
            x for f in per_nome.get(os.path.basename(cur), []) for x in per_file[f]]
        vicine = [c for c in cand if difflib.SequenceMatcher(None, s, c).quick_ratio() >= SIMILE]
        if any(difflib.SequenceMatcher(None, s, c).ratio() >= SIMILE for c in vicine):
            quasi += 1
        else:
            mancanti.append({"file": cur, "riga": s[:200]})
    return {"righe": tot, "identiche": identiche, "quasi": quasi, "mancanti": mancanti}


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
    ap.add_argument("--righe", nargs="+", metavar="RAMO",
                    help="per ogni ramo, le righe che aggiunge e che su --base non ci "
                         "sono; esce 1 se ce n'e' anche una")
    args = ap.parse_args(argv)

    if args.righe:
        if args.fetch:
            fetch()
        indice = indice_righe(args.base)
        esiti = {}
        for ramo in args.righe:
            ref = ramo if _ref_esiste(ramo) else f"origin/{ramo}"
            if not _ref_esiste(ref):
                print(f"✗ contenuti_nei_rami: il clone non conosce il ramo {ramo} "
                      "(nome sbagliato, o serve --fetch)", file=sys.stderr)
                return 2
            esiti[ramo] = righe_mai_arrivate(ref, args.base, indice)
        if args.json:
            print(json.dumps(esiti, ensure_ascii=False, indent=2))
        else:
            for ramo, e in esiti.items():
                segno = "✗" if e["mancanti"] else "✓"
                print(f"{segno} {ramo}: {e['righe']} righe aggiunte · {e['identiche']} "
                      f"identiche · {e['quasi']} quasi · {len(e['mancanti'])} mai arrivate")
                per = defaultdict(int)
                for m in e["mancanti"]:
                    per[m["file"]] += 1
                for f, n in sorted(per.items(), key=lambda x: -x[1])[:5]:
                    print(f"      {n:5d}  {f}")
        return 1 if any(e["mancanti"] for e in esiti.values()) else 0

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
