#!/usr/bin/env python3
"""controlla_marche.py — i due cancelli delle marche sulle righe cambiate (ADR-0109).

Guarda solo il diff fra la base e HEAD, mai il repo intero:

1. **Marca senza domanda e base.** Una riga aggiunta che apre un INFERRED
   deve scriverlo come vuole GUIDA-MARCATURE: `[INFERRED — domanda?; base: …]`.
2. **INFERRED tolto in silenzio.** Se un file perde dei marcatori INFERRED, nello
   stesso diff ci dev'essere un `[CANONE`, un `[GENERATO` o un blocco
   `<!-- storico -->` aggiunto nello stesso file.

Fuori dai controlli, come per `inventory_inferred.py`: `plans/` e i changelog
(storia), le righe di regola e i modelli (meta), i volumi di stampa generati
(`.hb.md`, `.html`), dove le marche si tolgono apposta.

Bloccante in CI sulle PR dal 2026-11-25 (ADR-0109, scheda 4): è salito dal
canale testing di ADR-0099 dopo 510 run di PR con 3 rossi, tutti difetti veri
(D8 di PIANO-PIATTAFORMA-DI-SVILUPPO).

Uso
  python3 scripts/controlla_marche.py --base origin/main
  python3 scripts/controlla_marche.py --base origin/main --rigido   # exit 1 se trova qualcosa

Exit 0 = nessun avviso (o avvisi senza --rigido) · 1 = avvisi con --rigido · 2 = errore d'uso
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import inventory_inferred as inv  # noqa: E402

CHIUSURA = re.compile(r"\[CANONE|\[GENERATO|<!--\s*storico")
SUFFISSI = (".md", ".yaml", ".yml")


def diff(base: str, cwd: Path = ROOT) -> str:
    r = subprocess.run(["git", "diff", "-M", "-U0", "--no-color", f"{base}...HEAD", "--"],
                       cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ERRORE: git diff {base}...HEAD: {r.stderr.strip()}")
    return r.stdout


def per_file(testo: str) -> dict[str, dict[str, list[tuple[int, str]]]]:
    """{file: {"+": [(riga, testo)], "-": [(riga, testo)]}} dal diff unificato."""
    out: dict[str, dict[str, list]] = defaultdict(lambda: {"+": [], "-": []})
    corrente = vecchio = None
    riga_nuova = 0
    for r in testo.splitlines():
        if r.startswith("--- "):
            vecchio = None if r[4:] == "/dev/null" else r[6:]
            continue
        if r.startswith("+++ "):
            # un file cancellato conta col suo nome vecchio: perde i suoi INFERRED
            corrente = vecchio if r[4:] == "/dev/null" else r[6:]
            continue
        if r.startswith("@@"):
            m = re.search(r"\+(\d+)", r)
            riga_nuova = int(m.group(1)) if m else 0
            continue
        if corrente is None:
            continue
        if r.startswith("+"):
            out[corrente]["+"].append((riga_nuova, r[1:]))
            riga_nuova += 1
        elif r.startswith("-"):
            out[corrente]["-"].append((0, r[1:]))
    return out


def da_guardare(rel: str) -> bool:
    if not rel.endswith(SUFFISSI) or rel.endswith(".hb.md"):
        return False
    return inv.classe(rel) == "aperti"


def marche_di_fatto(testo: str):
    """I marcatori INFERRED della riga che aprono un fatto: non le citazioni
    («marcati `[INFERRED]`») né lo schema da copiare."""
    for m in inv.MARCATORE.finditer(testo):
        if inv.cita_la_convenzione(testo[:m.start()]):
            continue
        coda = " ".join(m.group("coda").split())
        nota = inv.NOTA.match(coda)
        testo_nota = nota.group("testo").strip() if nota else ""
        if testo_nota and inv.SCHEMA.match(testo_nota):
            continue
        yield testo_nota


def avvisi(cambi: dict[str, dict[str, list]]) -> list[str]:
    out: list[str] = []
    for rel, d in sorted(cambi.items()):
        if not da_guardare(rel):
            continue
        for n, testo in d["+"]:
            for testo_nota in marche_di_fatto(testo):
                if inv.forma(testo_nota) != "nuova":
                    out.append(f"{rel}:{n}: marca senza domanda e base — scrivi "
                               f"`[INFERRED — domanda?; base: …]` (GUIDA-MARCATURE)")
        tolti = sum(len(list(marche_di_fatto(t))) for _, t in d["-"])
        messi = sum(len(list(marche_di_fatto(t))) for _, t in d["+"])
        chiusi = any(CHIUSURA.search(t) for _, t in d["+"])
        if tolti > messi and not chiusi:
            out.append(f"{rel}: {tolti - messi} INFERRED tolti senza CANONE, GENERATO o "
                       f"blocco storico nello stesso file (GUIDA-MARCATURE, regola 6)")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--base", required=True, help="Ref di confronto, es. origin/main.")
    ap.add_argument("--rigido", action="store_true", help="Exit 1 se c'è almeno un avviso.")
    a = ap.parse_args(argv)
    trovati = avvisi(per_file(diff(a.base)))
    for t in trovati:
        print(f"⚠ {t}")
    if not trovati:
        print(f"✓ controlla_marche: nessuna marca da sistemare nel diff contro {a.base}")
        return 0
    print(f"controlla_marche: {len(trovati)} avvisi contro {a.base}")
    return 1 if a.rigido else 0


if __name__ == "__main__":
    raise SystemExit(main())
