#!/usr/bin/env python3
"""
gate_locale.py — i gate del job `validate` della CI, eseguiti sulla macchina.

Legge `.github/workflows/ci.yml` ed esegue, nell'ordine, i passi `run:` del job
`validate` con `bash -eo pipefail`, come fa GitHub. L'elenco non è scritto qui:
un gate nuovo in CI entra da solo.

Prima di questo script i gate si rilanciavano a mano, da una lista copiata che
restava indietro rispetto alla CI. Così un push poteva tornare rosso per un gate
che in locale nessuno aveva fatto girare.

Cosa salta, e lo dice:
- i passi che installano (`pip install`, `apt-get`, `curl`, `npm`): la macchina
  è già pronta, o lo dice `dm.py doctor`;
- i passi con espressioni `${{ … }}` diverse da `github.base_ref`, che qui non
  hanno valore;
- con `--rapido`, i due corridori dei test (`unittest`, `pytest`).

Un passo con `continue-on-error` che fallisce è un avviso, non un errore. Lo è
anche un passo che fallisce nominando uno strumento che in CI porta un passo
«Install X» saltato qui (typst, per esempio), se sulla macchina manca.

    python3 scripts/gate_locale.py              # tutto il job validate
    python3 scripts/gate_locale.py --rapido     # senza i corridori dei test
    python3 scripts/gate_locale.py --elenco     # cosa farebbe, senza eseguire
    python3 scripts/gate_locale.py --solo misura_resa --solo validate_maps

`python` nei passi è il Python che esegue questo script: lanciato dal `.venv`,
usa il `.venv`.

Exit: 0 tutti i gate bloccanti verdi · 1 almeno uno rosso · 2 ci.yml illeggibile.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CI = REPO / ".github" / "workflows" / "ci.yml"
JOB = "validate"
INSTALLA = re.compile(r"\b(pip install|apt-get|apt install|curl |wget |npm (ci|install))")
ESPRESSIONE = re.compile(r"\$\{\{\s*([^}]*?)\s*\}\}")
TEST = re.compile(r"\b(unittest discover|pytest)\b")


def passi(ci: Path = CI, base: str = "main") -> list[dict]:
    """I passi `run:` del job, ognuno con il suo esito previsto: esegui o salta, e perché."""
    import yaml
    dati = yaml.safe_load(ci.read_text(encoding="utf-8"))
    out = []
    for i, p in enumerate(dati["jobs"][JOB].get("steps", []), 1):
        if "run" not in p:
            continue
        nome = p.get("name") or p["run"].strip().splitlines()[0]
        run = p["run"].replace("${{ github.base_ref }}", base)
        voce = {"n": i, "nome": nome, "run": run, "avviso": bool(p.get("continue-on-error")),
                "salta": None}
        altre = ESPRESSIONE.findall(run)
        if INSTALLA.search(run):
            voce["salta"] = "installa"
        elif altre:
            voce["salta"] = f"espressione ${{{{ {altre[0]} }}}}"
        elif p.get("if") and "pull_request" not in str(p["if"]):
            # una condizione sulla PR vale anche qui: si confronta col ramo --base
            voce["salta"] = f"condizione «{p['if']}»"
        out.append(voce)
    return out


def mancanti(elenco: list[dict]) -> set[str]:
    """Gli strumenti che un passo saltato «Install X» avrebbe portato e che qui
    non ci sono: un passo che poi fallisce nominandoli non è un rosso del codice."""
    import shutil
    out = set()
    for v in elenco:
        m = re.match(r"install\s+(\w[\w-]*)", v["nome"], re.I)
        if v["salta"] == "installa" and m and m.group(1).lower() != "dependencies":
            if shutil.which(m.group(1).lower()) is None:
                out.add(m.group(1).lower())
    return out


def esegui(voce: dict, env: dict) -> tuple[int, str, float]:
    t = time.monotonic()
    r = subprocess.run(["bash", "-eo", "pipefail", "-c", voce["run"]], cwd=REPO, env=env,
                       capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip(), time.monotonic() - t


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--rapido", action="store_true", help="salta i corridori dei test (unittest, pytest)")
    ap.add_argument("--elenco", action="store_true", help="elenca i passi e cosa ne farebbe, senza eseguire")
    ap.add_argument("--solo", action="append", default=[], metavar="TESTO",
                    help="esegue solo i passi il cui nome o comando contiene TESTO (ripetibile)")
    ap.add_argument("--base", default="main", help="il ramo per i gate che confrontano (default: main)")
    args = ap.parse_args(argv)
    try:
        elenco = passi(base=args.base)
    except (OSError, KeyError, ImportError) as e:
        print(f"✗ gate_locale: ci.yml illeggibile ({e})", file=sys.stderr)
        return 2
    for v in elenco:
        if args.rapido and not v["salta"] and TEST.search(v["run"]):
            v["salta"] = "--rapido"
        if args.solo and not v["salta"] and not any(s in v["nome"] or s in v["run"] for s in args.solo):
            v["salta"] = "--solo"
    if args.elenco:
        for v in elenco:
            stato = f"salta ({v['salta']})" if v["salta"] else ("avviso" if v["avviso"] else "gate")
            print(f"{v['n']:3} {stato:24} {v['nome']}")
        return 0

    env = dict(os.environ)
    env["PATH"] = f"{Path(sys.executable).parent}{os.pathsep}{env.get('PATH', '')}"
    # Le variabili che il runner di GitHub dà a ogni passo. Senza, un passo che
    # scrive in "$RUNNER_TEMP/x" scrive in "/x" e fallisce per i permessi: il
    # 2026-10-09, sulla macchina del DM, il piano di scena 3D.
    import tempfile
    temp = tempfile.mkdtemp(prefix="gate-locale-")
    env.setdefault("RUNNER_TEMP", temp)
    env.setdefault("GITHUB_WORKSPACE", str(REPO))
    env.setdefault("PYTHONIOENCODING", "utf-8")
    rossi, avvisi, fatti = [], [], 0
    assenti = mancanti(elenco)
    for v in elenco:
        if v["salta"]:
            if v["salta"] != "--solo":
                print(f"○ {v['nome']} — saltato: {v['salta']}")
            continue
        rc, testo, sec = esegui(v, env)
        fatti += 1
        if rc == 0:
            print(f"✓ {v['nome']} ({sec:.0f} s)")
            continue
        colpa = [s for s in assenti if s in testo.lower()]
        avviso = v["avviso"] or bool(colpa)
        segno = "⚠" if avviso else "✗"
        nota = f" — manca {', '.join(colpa)}, che in CI installa un passo saltato qui" if colpa else ""
        print(f"{segno} {v['nome']} — uscita {rc} ({sec:.0f} s){nota}")
        for riga in testo.splitlines()[-8:]:
            print(f"    {riga}")
        (avvisi if avviso else rossi).append(v["nome"])
    print(f"\n{fatti} passi eseguiti · {len(rossi)} rossi · {len(avvisi)} avvisi")
    return 1 if rossi else 0


if __name__ == "__main__":
    sys.exit(main())
