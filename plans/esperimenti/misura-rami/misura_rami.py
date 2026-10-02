#!/usr/bin/env python3
"""misura_rami.py: le righe che un ramo aggiunge esistono su main?

SUPERATO dal lotto 4j-5 (2026-09-24): la stessa misura vive in
`python3 scripts/contenuti_nei_rami.py --righe RAMO...`, con i test. Resta
qui come prototipo, perché PRATICHE §7.2 cita i numeri che ha prodotto.

Nasce il 2026-09-24 (PRATICHE D7 e D8). Il registro dei rami
(`scripts/contenuti_nei_rami.py`) conta i file nuovi e non vede le modifiche a
file esistenti: un ramo con tre correzioni di canone mai arrivate su `main`
sembrava cancellabile. Questo script guarda le righe, non i file.

Per ogni ramo prende il diff fra il punto d'incontro con `origin/main` e la
testa, e classifica ogni riga aggiunta:

* identica: la stessa riga (spazi normalizzati) esiste in un file qualunque
  di `main`;
* quasi: somiglianza >= 0.9 con una riga dello stesso file, o di un file con
  lo stesso nome altrove (i file spostati);
* mancante: nessuna delle due.

Gli SVG e le immagini non contano: sono generati o binari. Una riga
mancante non vuol dire lavoro perso: può essere testo tolto apposta, o
riscritto dopo. Lo dice solo la lettura, e i numeri dicono dove leggere.

Controllo positivo: `claude/salvatore-character-art-wSjuH` deve dare 3
mancanti su 3.

    python3 plans/esperimenti/misura-rami/misura_rami.py claude/<ramo> [...]
    python3 plans/esperimenti/misura-rami/misura_rami.py --json claude/<ramo>

Solo libreria standard. Richiede un clone completo (`git fetch --unshallow`).
"""
import collections
import difflib
import io
import json
import os
import re
import subprocess
import sys
import tarfile

SALTA = re.compile(r"\.(svg|png|jpe?g|webp|pdf|gif|pcg|zip|typ)$", re.I)


def git(*a: str, binario: bool = False):
    r = subprocess.run(["git", *a], capture_output=True, check=True)
    return r.stdout if binario else r.stdout.decode("utf-8", "replace")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def righe_di_main():
    tutte, per_file, per_nome = set(), {}, collections.defaultdict(list)
    tar = tarfile.open(fileobj=io.BytesIO(git("archive", "origin/main", binario=True)))
    for m in tar.getmembers():
        if not m.isfile() or SALTA.search(m.name):
            continue
        try:
            testo = tar.extractfile(m).read().decode("utf-8")
        except UnicodeDecodeError:
            continue
        n = [norm(x) for x in testo.splitlines() if norm(x)]
        tutte.update(n)
        per_file[m.name] = n
        per_nome[os.path.basename(m.name)].append(m.name)
    return tutte, per_file, per_nome


def misura(ramo: str, tutte, per_file, per_nome) -> dict:
    ref = ramo if ramo.startswith("origin/") else "origin/" + ramo
    base = git("merge-base", "origin/main", ref).strip()
    cur, tot, identiche, quasi, mancanti = None, 0, 0, 0, []
    for riga in git("diff", "--no-renames", "-U0", base, ref).splitlines():
        if riga.startswith("+++ "):
            cur = riga[6:].rstrip("\t").strip('"') if riga.startswith("+++ b/") else None
            if cur and SALTA.search(cur):
                cur = None
            continue
        if cur is None or not riga.startswith("+"):
            continue
        s = norm(riga[1:])
        if len(s) < 4 or re.fullmatch(r"[-|:=*#`>_ .~]+", s):
            continue
        tot += 1
        if s in tutte:
            identiche += 1
            continue
        cand = per_file.get(cur) or [
            x for p in per_nome.get(os.path.basename(cur), []) for x in per_file[p]]
        vicine = [c for c in cand if difflib.SequenceMatcher(None, s, c).quick_ratio() >= 0.9]
        if any(difflib.SequenceMatcher(None, s, c).ratio() >= 0.9 for c in vicine):
            quasi += 1
        else:
            mancanti.append([cur, s[:200]])
    return {"righe": tot, "identiche": identiche, "quasi": quasi, "mancanti": mancanti}


def main(argv: list) -> int:
    come_json = "--json" in argv
    rami = [a for a in argv if a != "--json"]
    if not rami:
        print(__doc__)
        return 2
    indice = righe_di_main()
    esito = {r: misura(r, *indice) for r in rami}
    if come_json:
        json.dump(esito, sys.stdout, ensure_ascii=False, indent=1)
        return 0
    for r, v in esito.items():
        print(f"{r}: {v['righe']} righe aggiunte · {v['identiche']} identiche · "
              f"{v['quasi']} quasi · {len(v['mancanti'])} mancanti")
        per = collections.Counter(f for f, _ in v["mancanti"])
        for f, n in per.most_common(5):
            print(f"    {n:5d}  {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
