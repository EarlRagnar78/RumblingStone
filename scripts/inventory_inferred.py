#!/usr/bin/env python3
"""inventory_inferred.py — inventario e ratchet dei `[INFERRED]` (finding C4).

Il problema
  `[INFERRED]` è la valvola di sicurezza di AGENTS.md §5: quando un fatto non è
  attestato, l'agente lo marca invece di inventarlo. Funziona — ma nessuno
  contava quanti ce ne fossero né dove, quindi il debito era **contabilizzabile
  solo a occhio** e in pratica non veniva mai smaltito.

La distinzione che rende il gate utile
  Ad agosto, su 340 marcatori, 96 stavano in `plans/` e 29 in
  `campaign/state-changelog.md`; il 2026-10-24 sono 1.038, di cui **754 in
  `plans/`** e 24 nello storico di stato: sono **record storici** — la frase «marcato
  `[INFERRED]` in §1» dentro un changelog *racconta* un debito, non lo *crea*.
  Contarli insieme agli altri produce un numero che non può scendere: si
  smaltisce un debito, si scrive nel changelog che l'hai smaltito, e il totale
  resta uguale. Un ratchet così si disattiva da solo entro una settimana.

  Quindi qui i marcatori sono divisi in tre classi, e **solo la prima conta**:

  - **aperti** — documenti vivi: canone, moduli d'arco, bestiario, schede PG.
    È il debito vero, ed è l'unico numero che il ratchet sorveglia.
  - **storici** — `plans/**` e i changelog: raccontano debiti, non li aprono.
  - **meta** — `docs/audit/**`: citano il marcatore *per misurarlo*.

  I record tipizzati di `campaign/state.yaml` (`inferred:`) sono elencati per
  primi e a parte: sono gli unici che portano già **la domanda da fare al DM**,
  ed è la forma verso cui gli altri dovrebbero migrare.

Ripreso dalla PR #99 (lotto G4) il 2026-10-24, scelta A del DM sulla chiusura
  della #99 (ADR-0088). Entra nel canale testing (ADR-0099): in CI gira
  `--check` non bloccante; diventa un cancello solo se il DM lo promuove.
  L'inventario si genera a richiesta e non si committa (è in `.gitignore`).

Il ratchet
  `--check` confronta gli **aperti** con la baseline in
  `docs/audit/inferred-baseline.json` e fallisce se il numero **sale**.
  Non è un divieto: aggiungere un `[INFERRED]` resta legittimo — è sempre
  meglio di un'invenzione. Chi ne aggiunge uno con ragione aggiorna la baseline
  con `--update-baseline` nello stesso commit, e la revisione lo vede nel diff.

Uso
  python3 scripts/inventory_inferred.py                 # scrive l'inventario
  python3 scripts/inventory_inferred.py --check         # gate CI
  python3 scripts/inventory_inferred.py --update-baseline
  python3 scripts/inventory_inferred.py --json

Exit  0 = ok · 1 = il debito aperto è salito sopra la baseline · 2 = errore d'uso
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INVENTARIO = ROOT / "docs" / "audit" / "INFERRED-INVENTARIO.md"
BASELINE = ROOT / "docs" / "audit" / "inferred-baseline.json"

# Mirror per-agente gitignored e artefatti: non sono fonti.
SKIP_DIRS = {".git", "build", ".claude", ".cursor", ".gemini", ".chatgpt",
             ".windsurf", ".kilo", ".agents", ".github", "_ARCHIVIO", "Old"}
SUFFISSI = {".md", ".yaml", ".yml"}

MARCATORE = re.compile(r"\[INFERRED(?P<coda>[^\]]*)\]")

# `[INFERRED` seguito da `:` o ` —` porta una nota; da solo è nudo.
NOTA = re.compile(r"^\s*[—:-]\s*(?P<testo>.+)$")


def classe(rel: str) -> str:
    """aperti | storici | meta — vedi il docstring."""
    if rel.startswith("docs/audit/"):
        return "meta"
    if rel.startswith("plans/") or "CHANGELOG" in rel or rel.endswith("state-changelog.md"):
        return "storici"
    return "aperti"


def area(rel: str) -> str:
    """Raggruppamento leggibile: il DM smaltisce per area, non per file."""
    testa = rel.split("/", 1)[0]
    if testa.startswith(tuple(f"{n:02d}_" for n in range(0, 12))):
        return f"Archi — {testa}"
    return {
        "campaign": "Canone e stato di campagna",
        "Bestiario": "Bestiario (PNG, mostri, villain)",
        "PG": "Personaggi e artefatti",
        "skills": "Skill degli agenti",
        "docs": "Documentazione",
        "scripts": "Strumenti",
        "converters": "Toolchain esterna",
    }.get(testa, "Radice del repo")


def sorgenti(base: Path):
    for p in sorted(base.rglob("*")):
        if p.suffix.lower() not in SUFFISSI or not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        # L'inventario conta i marcatori e li ristampa: contarsi da solo lo
        # renderebbe non convergente — ogni rigenerazione alzerebbe il totale.
        if p.resolve() == INVENTARIO.resolve():
            continue
        yield p


def _rel(p: Path, base: Path) -> str:
    """Percorso leggibile: dalla radice del repo, o dalla base se siamo fuori."""
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p.relative_to(base))


def scansiona(base: Path) -> list[dict]:
    trovati: list[dict] = []
    for p in sorgenti(base):
        try:
            testo = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = _rel(p, base)
        for lineno, riga in enumerate(testo.splitlines(), start=1):
            for m in MARCATORE.finditer(riga):
                coda = m.group("coda").strip()
                nota = NOTA.match(coda)
                trovati.append({
                    "file": rel,
                    "line": lineno,
                    "classe": classe(rel),
                    "area": area(rel),
                    "nota": nota.group("testo").strip() if nota else "",
                    "contesto": riga.strip()[:180],
                })
    return trovati


def record_tipizzati() -> list[dict]:
    """I `[INFERRED]` che hanno già la domanda: `inferred:` di state.yaml."""
    f = ROOT / "campaign" / "state.yaml"
    if not f.exists():
        return []
    try:
        import yaml  # opzionale: l'inventario funziona anche senza
    except ImportError:
        return []
    try:
        dati = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return []
    return list(dati.get("inferred") or [])


def scrivi_inventario(trovati: list[dict], tipizzati: list[dict]) -> str:
    aperti = [t for t in trovati if t["classe"] == "aperti"]
    per_classe = defaultdict(int)
    for t in trovati:
        per_classe[t["classe"]] += 1

    out: list[str] = []
    w = out.append
    w("<!-- GENERATO da scripts/inventory_inferred.py — non modificare a mano. -->")
    w("")
    w("# Inventario `[INFERRED]` — il debito di canone, smaltibile a lotti")
    w("")
    w("> Generato. Per rigenerarlo: `python3 scripts/inventory_inferred.py`.")
    w("> Il gate è `--check`, e sorveglia **solo la colonna «aperti»**.")
    w("")
    w("## Quanti sono, e quali contano")
    w("")
    w("| Classe | Quanti | Che cosa sono |")
    w("|---|---:|---|")
    w(f"| **aperti** | **{per_classe['aperti']}** | Documenti vivi: canone, moduli d'arco, "
      "bestiario, schede. **È il debito vero**, ed è l'unico numero sorvegliato |")
    w(f"| storici | {per_classe['storici']} | `plans/**` e i changelog: *raccontano* un "
      "debito, non lo aprono. Contarli renderebbe il totale incapace di scendere |")
    w(f"| meta | {per_classe['meta']} | `docs/audit/**`: citano il marcatore **per misurarlo** |")
    w("")

    if tipizzati:
        w("## Prima i record tipizzati — questi hanno già la domanda")
        w("")
        w("Sono le voci `inferred:` di `campaign/state.yaml`: le uniche che portano una "
          "**domanda formulata**, rispondibile senza rileggere i file. È la forma verso cui "
          "gli altri dovrebbero migrare — un marcatore nudo dice *che* non sai, non *cosa* chiedere.")
        w("")
        w("| ID | Dove | Domanda | A chi | Aperto dal |")
        w("|---|---|---|---|---|")
        for r in tipizzati:
            dom = " ".join(str(r.get("domanda", "")).split())
            w(f"| **{r.get('id','?')}** | `{r.get('dove','')}` | {dom} | "
              f"{r.get('a_chi','')} | {r.get('aperto_dal','')} |")
        w("")

    w("## Il debito aperto, per area")
    w("")
    w("Ordinato per numero: si smaltisce dall'alto, un'area per tornata.")
    w("")
    per_area: dict[str, list[dict]] = defaultdict(list)
    for t in aperti:
        per_area[t["area"]].append(t)
    for nome, voci in sorted(per_area.items(), key=lambda kv: -len(kv[1])):
        w(f"### {nome} — {len(voci)}")
        w("")
        per_file: dict[str, list[dict]] = defaultdict(list)
        for v in voci:
            per_file[v["file"]].append(v)
        for f, vs in sorted(per_file.items(), key=lambda kv: -len(kv[1])):
            note = sorted({v["nota"] for v in vs if v["nota"]})
            coda = f" — {'; '.join(note[:3])}" if note else ""
            righe = ", ".join(str(v["line"]) for v in vs[:12])
            piu = "…" if len(vs) > 12 else ""
            w(f"- `{f}` — **{len(vs)}** (righe {righe}{piu}){coda}")
        w("")

    w("---")
    w("")
    w("**Nudi contro parlanti.** Un `[INFERRED]` senza nota dice *che* qualcosa non è "
      "attestato, non *che cosa chiedere al DM*: è contabilizzabile ma non smaltibile. "
      "Quando ne tocchi uno, aggiungigli la domanda — o, se riguarda il canone di campagna, "
      "promuovilo a record `inferred:` in `campaign/state.yaml`.")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--path", help="Sottoalbero da scansionare (default: tutto il repo).")
    ap.add_argument("--check", action="store_true",
                    help="Gate: fallisce se il debito APERTO sale sopra la baseline.")
    ap.add_argument("--update-baseline", action="store_true",
                    help="Riscrive la baseline col conteggio attuale (da fare nello stesso commit).")
    ap.add_argument("--json", action="store_true", help="Report in JSON (opt-in).")
    ap.add_argument("--out", help="File dell'inventario (default: docs/audit/INFERRED-INVENTARIO.md).")
    args = ap.parse_args(argv)

    base = Path(args.path).resolve() if args.path else ROOT
    if not base.exists():
        print(f"ERRORE: percorso inesistente: {base}", file=sys.stderr)
        return 2

    trovati = scansiona(base)
    aperti = sum(1 for t in trovati if t["classe"] == "aperti")
    tipizzati = record_tipizzati()

    if args.update_baseline:
        BASELINE.write_text(json.dumps({"aperti": aperti}, indent=2) + "\n", encoding="utf-8")
        print(f"✓ baseline aggiornata: {aperti} aperti")
        return 0

    if args.check:
        if not BASELINE.exists():
            print("ERRORE: baseline assente — esegui --update-baseline una volta.", file=sys.stderr)
            return 2
        atteso = json.loads(BASELINE.read_text(encoding="utf-8"))["aperti"]
        if aperti > atteso:
            print(f"✗ inventory_inferred: il debito aperto è salito — {aperti} contro "
                  f"baseline {atteso} (+{aperti - atteso}).")
            print("  Aggiungere un [INFERRED] è legittimo (meglio di un'invenzione): se è")
            print("  voluto, esegui --update-baseline nello STESSO commit, così il diff lo mostra.")
            return 1
        segno = "" if aperti == atteso else f" (−{atteso - aperti}, baseline da abbassare)"
        print(f"✓ inventory_inferred: {aperti} [INFERRED] aperti, baseline {atteso}{segno}")
        return 0

    testo = scrivi_inventario(trovati, tipizzati)
    if args.json:
        print(json.dumps({"aperti": aperti, "totale": len(trovati),
                          "tipizzati": len(tipizzati), "voci": trovati},
                         ensure_ascii=False, indent=2))
        return 0

    out = Path(args.out).resolve() if args.out else INVENTARIO
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(testo, encoding="utf-8")
    try:
        dove = out.relative_to(ROOT)
    except ValueError:
        dove = out
    print(f"✓ inventory_inferred: {aperti} aperti · {len(trovati)} marcatori totali "
          f"· {len(tipizzati)} record tipizzati → {dove}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
