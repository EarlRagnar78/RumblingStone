#!/usr/bin/env python3
"""Le capacità dei plugin che `verifica_scheda` legge davvero, contro quelle che
il manifest dichiara (stessa misura fatta per genera_creatura nella #376).

Uso: python3 misura_capacita_verifica_scheda.py [ref git ...]   (default: la copia di lavoro)
"""
from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from dmcore import sistemi as S  # noqa: E402


def lette() -> "set[str]":
    viste: set[str] = set()
    vera = S.capacita

    def spia(id_, nome, root=None):
        viste.add(nome)
        return vera(id_, nome, root)

    S.capacita = spia
    try:
        import verifica_scheda as V
        cartelle = ["Bestiario"] + sorted(p.name for p in ROOT.glob("0*") if p.is_dir())
        with contextlib.redirect_stdout(io.StringIO()):
            V.main([*cartelle, "--json"])
    finally:
        S.capacita = vera
    return viste


def dichiarate(ref: "str | None") -> "set[str]":
    testo = (subprocess.check_output(["git", "show", f"{ref}:scripts/tools.manifest.json"], cwd=ROOT, text=True)
             if ref else (ROOT / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
    return set(next(t for t in json.loads(testo)["tools"] if t["id"] == "verifica_scheda")["sistema"]["capacita"])


def main() -> int:
    viste = lette()
    print("lette:", sorted(viste))
    for ref in sys.argv[1:] or [None]:
        d = dichiarate(ref)
        print(ref or "copia di lavoro", "· dichiarate:", len(d), "· lette ma non dichiarate:", sorted(viste - d),
              "· dichiarate ma non lette:", sorted(d - viste), f"· coperte: {len(viste & d)}/{len(viste)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
