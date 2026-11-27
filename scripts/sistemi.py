#!/usr/bin/env python3
"""sistemi.py — i sistemi di gioco del repo, e cosa ogni strumento sa fare con ciascuno (ADR-0111).

Legge `sistemi.toml`, i plugin in `sistemi/<id>/sistema.toml` e il campo
`sistema.capacita` di `scripts/tools.manifest.json`, e stampa:

  1. i sistemi supportati dal repo, quali sono attivi e quali di rinforzo;
  2. la matrice strumenti × sistemi: per ogni capacità chiesta da uno
     strumento, come la copre ogni sistema attivo
        ✅ dati          i dati stanno in file
        🔧 codice (Ln)   ancora cablata nel codice, la migra il lotto Ln
        ⬜ non supportato lo strumento non lavora su quel sistema
        ❌ mancante      nessuna dichiarazione: è un buco
     con «↪ da» quando la capacità è ereditata;
  3. le misure del piano: quante capacità sono in dati, in codice, non
     supportate.

    python3 scripts/sistemi.py                    # sistemi e matrice
    python3 scripts/sistemi.py --di FILE          # il sistema di un file
    python3 scripts/sistemi.py --skill            # le skill da installare (D5)
    python3 scripts/sistemi.py --skill-escluse    # quelle che build/sync saltano (L6)
    python3 scripts/sistemi.py --json             # tutto, per altri strumenti
    python3 scripts/sistemi.py --check            # il cancello

Uscita: 0 ok · 1 `--check` ha trovato problemi · 2 configurazione illeggibile.
Solo libreria standard; uscita deterministica (ordinamenti fissi).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore import sistemi as S  # noqa: E402

MANIFEST = S.MANIFEST
SIMBOLO = {"dati": "✅", "codice": "🔧", "non_supportato": "⬜", "mancante": "❌"}


def strumenti(root: Path) -> "dict[str, list[str]]":
    """{id: [capacità]} per gli strumenti che dipendono dal sistema."""
    m = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    return {t["id"]: list(t["sistema"]["capacita"]) for t in m["tools"] if t.get("sistema")}


def descrivi(c: S.Copertura) -> str:
    s = SIMBOLO[c.modo] + " " + c.modo.replace("_", " ")
    if c.modo == "codice" and c.nota:
        s += f" ({c.nota})"
    if c.da != c.sistema:
        s += f" ↪ {c.da}"
    return s


def rapporto(root: Path) -> dict:
    cfg, cat, plug = S.carica(root)
    pr = cfg.get("progetto", {})
    att = list(pr.get("attivi", []))
    st = strumenti(root)
    sistemi = [{"id": i, "nome": p.get("nome"), "tipo": p.get("tipo"), "licenza": p.get("licenza"),
                "attivo": i in att, "rinforzo": i in pr.get("rinforzo", []),
                "skill": p.get("skill", [])} for i, p in sorted(plug.items())]
    matrice = []
    for sid in sorted(st):
        for nome in st[sid]:
            riga = {"strumento": sid, "capacita": nome}
            for i in att:
                c = S.capacita(i, nome, root)
                riga[i] = {"modo": c.modo, "da": c.da, "voci": list(c.voci), "nota": c.nota}
            matrice.append(riga)
    conta = {i: {m: 0 for m in SIMBOLO} for i in att}
    for i in att:
        for nome in sorted(cat):
            conta[i][S.capacita(i, nome, root).modo] += 1
    return {"predefinito": pr.get("predefinito"), "attivi": att, "rinforzo": pr.get("rinforzo", []),
            "moduli": cfg.get("moduli", {}), "sistemi": sistemi, "catalogo": cat,
            "matrice": matrice, "capacita_per_sistema": conta,
            "skill_da_installare": S.skill_da_installare(root)}


def stampa(r: dict) -> None:
    print("Sistemi di gioco (sistemi.toml)\n")
    print("| Sistema | Nome | Tipo | Licenza | Stato | Skill |\n|---|---|---|---|---|---|")
    for s in r["sistemi"]:
        stato = ("attivo" if s["attivo"] else "spento" if s["tipo"] == "sistema" else "famiglia")
        if s["rinforzo"]:
            stato += ", rinforzo"
        if s["id"] == r["predefinito"]:
            stato += ", predefinito"
        print(f"| {s['id']} | {s['nome']} | {s['tipo']} | {s['licenza']} | {stato} | "
              f"{', '.join(s['skill']) or '—'} |")
    print("\nModuli con un sistema diverso dal predefinito:")
    for k, v in sorted(r["moduli"].items()):
        print(f"  {k} → {v}")
    att = r["attivi"]
    print("\nCosa sa fare ogni strumento con ogni sistema attivo\n")
    print("| Strumento | Capacità | " + " | ".join(att) + " |\n|---|---|" + "---|" * len(att))
    for riga in r["matrice"]:
        celle = []
        for i in att:
            c = riga[i]
            cop = S.Copertura(i, riga["capacita"], c["modo"], c["da"], (), tuple(c["voci"]), c["nota"])
            celle.append(descrivi(cop))
        print(f"| {riga['strumento']} | {riga['capacita']} | " + " | ".join(celle) + " |")
    print("\nCapacità del catalogo per sistema (dati · codice · non supportato · mancante)")
    for i, c in r["capacita_per_sistema"].items():
        print(f"  {i}: {c['dati']} · {c['codice']} · {c['non_supportato']} · {c['mancante']}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--di", metavar="FILE", help="stampa il sistema di FILE")
    g.add_argument("--skill", action="store_true", help="le skill da installare, una per riga")
    g.add_argument("--skill-escluse", action="store_true",
                   help="le skill di sistemi né attivi né di rinforzo, che build/sync saltano (L6)")
    g.add_argument("--json", action="store_true", help="tutto il rapporto in JSON")
    g.add_argument("--check", action="store_true", help="cancello: esce 1 se c'è un problema")
    ap.add_argument("--root", type=Path, default=S.ROOT, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    root = a.root.resolve()
    try:
        if a.check:
            from dmcore import formule as F
            prob = S.problemi(root, strumenti(root)) + F.problemi(root)
            for p in prob:
                print("🔴 " + p)
            print(f"{'✗' if prob else '✓'} sistemi: {len(prob)} problemi")
            return 1 if prob else 0
        if a.di:
            print(S.sistema_di(a.di, root))
            return 0
        if a.skill:
            print("\n".join(S.skill_da_installare(root)))
            return 0
        if a.skill_escluse:
            escluse = S.skill_escluse(root)
            if escluse:
                print("\n".join(escluse))
            return 0
        r = rapporto(root)
    except (S.ErroreSistemi, FileNotFoundError, KeyError) as e:
        print(f"sistemi: configurazione illeggibile: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1, sort_keys=True))
    else:
        stampa(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
