#!/usr/bin/env python3
"""validate_modules.py — lint deterministico dei MASTER DEFINITIVI (ARC*-DEF-*).

Review automatica e SENZA token (niente LLM): verifica che ogni master
definitivo rispetti la checklist della skill `rumblingstone-module-standard`
(sezioni obbligatorie, niente terminologia 5e/deprecata, mappe in scala).
Stesso stile degli altri validator del repo (exit 1 = errori bloccanti;
i warning non bloccano).

Uso:  python scripts/validate_modules.py [--verbose]
"""
from __future__ import annotations

import re
import sys
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOB = "ARC*-DEF-*.md"

# --- Sezioni obbligatorie (checklist skill, §Struttura 1-14) -----------------
# `combat=True` = richiesta solo per i beat di combattimento (module-type: dungeon,
# il default). I beat `module-type: hub` (interludio/ritorno/investigazione/social —
# come i capitoli non-combat dei migliori AP) ne sono esenti, senza abbassare lo
# standard narrativo: tutto il resto resta obbligatorio.
REQUIRED = [
    (r"^## INDICE", "INDICE del modulo", False),
    (r"QUICKSTART", "Quickstart DM", False),
    (r"QUICK-REFERENCE", "Quick-Reference stampabile", False),
    (r"HIGHLIGHT", "Highlight asimmetrici per PG", False),
    (r"Tattiche .*round", "Tattiche round-per-round (stile RHoD)", True),
    (r"Scalare lo scontro", "Sidebar scaling (stile RHoD)", True),
    (r"Contingenze", "Contingenze «Se i PG fanno X»", False),
    (r"[Ss]confitta|[Ff]alliment", "Ramo sconfitta/fallimento (mai punizione gratuita)", False),
    (r"Sviluppi", "Riga Sviluppi negli incontri/scene", False),
    (r"ECHI|Echo Ledger", "Echo Ledger / conseguenze", False),
    (r"Budget PX|PX .*sezione", "Budget PX sezione-per-sezione", False),
    (r"[Tt]esoro PREGENERATO|Tesoro pregenerato", "Tesoro pregenerato itemizzato", False),
    (r"HANDOUT", "Handout & Asset", False),
    (r"### MAPPA", "Mappe ASCII ultra-clear", False),
    (r"1,5 m", "Scala 1,5 m/quadretto dichiarata", False),
    (r"Pathfinder 1e|PF1e", "Box supporto PF1e (dove il 3.5 è vago)", False),
]

# --- Termini banditi (5e / canone deprecato) ---------------------------------
# Una riga che contiene un termine bandito è ESENTE se contiene anche un
# marcatore di divieto/deprecazione (es. la frase che vieta il termine stesso).
BANNED = [
    (r"\bbonus action\b", "terminologia 5e (bonus action → azione veloce/swift)"),
    (r"\blair action", "terminologia 5e (lair action → attacco speciale con ricarica)"),
    (r"\bazioni? del covo\b", "terminologia 5e (azione del covo)"),
    (r"\bDC\s?[0-9]", "usare CD, non DC (convenzione repo)"),
    (r"\bNymeria\b", "canone deprecato (il compagno è DURIK, D14)"),
    (r"\bSkulldark\b|\bInfernotooth\b", "canone deprecato (il drago è SKULLCRUSHER, D6)"),
    (r"[Cc]ane da [Gg]uerra .*(COSTRUTTO|animato)", "canone deprecato (Durik è compagno VIVENTE riforgiato)"),
]
EXEMPT = re.compile(
    r"niente|MAI 5e|mai 5e|rimoss|vietat|deprecat|non usare|→|banditi|Errato"
    r"|errato|convenzione|usava|avevano|superat|storic|fonte|era(no)? ",
)


def check_file(path: Path, verbose: bool) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []
    warnings: list[str] = []

    # module-type: dichiarato con un marker HTML in testa. "hub" = beat non-combat.
    is_hub = bool(re.search(r"module-type:\s*hub", text, re.IGNORECASE))

    for pattern, label, combat_only in REQUIRED:
        if combat_only and is_hub:
            continue
        if not re.search(pattern, text, re.MULTILINE):
            errors.append(f"sezione mancante: {label} (pattern /{pattern}/)")

    for pattern, label in BANNED:
        rx = re.compile(pattern)
        for i, line in enumerate(lines, 1):
            if rx.search(line) and not EXEMPT.search(line):
                errors.append(f"r.{i}: termine bandito — {label}: «{line.strip()[:80]}»")

    n_readaloud = len(re.findall(r"[Rr]ead-aloud", text))
    if n_readaloud < 5:
        warnings.append(f"solo {n_readaloud} read-aloud (attesi ≥5 per un master AP-quality)")
    if "[INFERRED" not in text:
        warnings.append("nessun flag [INFERRED]: verificare che ogni fatto nuovo sia attestato")
    if verbose:
        print(f"  {path.name}: {n_readaloud} read-aloud, "
              f"{len(re.findall(r'### MAPPA', text))} mappe")

    return errors, warnings


# ─────────────────────────────────────────────────────────────────────────
# Il tetto EL ≤ APL+4 — il primo rilevatore di severità «critico»
#
# 🔴 **Perché qui, e perché solo questo dei tre casi critici.** Il DM, il
# 2026-09-21: *«non sarebbe opportuno creare questo verificatore? Ci sono le
# regole 3.5 e PF1e come skill nel repo, non si possono usare per farlo in
# maniera deterministica?»*. Dei tre casi critici del piano MQM, **uno solo è
# decidibile con i dati che il repo già possiede**, ed è questo:
#
#   * ⛔ **EL oltre APL+4 senza `Boost log:`** — è ARITMETICA. L'APL è
#     dichiarato in `campaign/state.md` (ADR-0038: l'EL viene da una gerarchia
#     dichiarata), l'EL è scritto nel file, il tetto è la regola di
#     `npc-villain-boosting`, e `Boost log:` è la deroga prevista. Nessun
#     giudizio: una sottrazione.
#   * 🟡 **contraddizione con `state.md`** — decidibile solo in forme strette
#     (un punteggio permanente di un PG che contraddice la scheda), non in
#     generale. Non è qui perché mezzo rilevatore che si spaccia per intero è
#     peggio di nessuno.
#   * 🔴 **statblocco inventato** — NON decidibile. Le skill SRD dicono cosa
#     esiste, non se i numeri di un PNG originale sono coerenti. Un rilevatore
#     lo confonderebbe con «PNG non nel Bestiario», che è un'altra cosa.
#
# ⚠️ Il tetto è una **regola di progettazione**, non del sistema: la fonte è
# `skills/npc-villain-boosting/`, che impone EL ≤ APL+4 e il `Boost log:` sui
# file di PNG nominati. Senza quella skill questo controllo non avrebbe senso.

APL_DICHIARATO = re.compile(r"\*\*Party APL:?\*\*:?\s*(\d{1,2})", re.I)

#: 🔴 **La forma PRESCRITTA, e non una piu' larga.** `AGENTS.md` §«Encounter
#: file format» prescrive `**EL**: [N]`. Misurato il 2026-09-21: quella forma ha
#: **ZERO occorrenze** nel repo, mentre la forma nuda `EL 14` ne ha **150** —
#: e quelle 150 mescolano dichiarazioni («Boss Fight - EL 14») con menzioni
#: («Standard Treasure for EL 16», «Nota di verifica EL»).
#:
#: Allargare il rilevatore alla forma nuda darebbe un numero, e il numero
#: sarebbe finto: e' il difetto che questo repo ha gia' commesso quattordici
#: volte. Quindi il controllo cerca **solo** la forma prescritta, oggi trova
#: zero incontri marcati, **e lo dice** — perche' «zero sforamenti su zero
#: incontri misurati» non e' un repo sano, e' un repo non marcato.
EL_DICHIARATO = re.compile(r"\*\*EL\*\*:?\s*(\d{1,2})\b")
DEROGA = re.compile(r"Boost log", re.I)
MARGINE_TETTO = 4


def party_apl() -> "int | None":
    """L'APL del gruppo, **preso da `state.md`** e non da una costante.

    ADR-0038 ha già trovato una volta che il repo dichiarava il `Party APL` e
    nessuno strumento lo leggeva. Questo lo legge.
    """
    stato = ROOT / "campaign" / "state.md"
    if not stato.exists():
        return None
    m = APL_DICHIARATO.search(stato.read_text(encoding="utf-8"))
    return int(m.group(1)) if m else None


def _file_di_gioco() -> "list[Path]":
    """Il contenuto di gioco vivo, con le esclusioni che il repo già dichiara."""
    snapshot = {p.parent for p in ROOT.rglob("_SNAPSHOT-STORICO.md")}
    fuori = ("_ARCHIVIO", "build", "homebrew", "node_modules")
    out = []
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in (
                "plans", "docs", "skills", "scripts", "converters", "campaign"):
            continue
        for f in d.rglob("*.md"):
            if any(x in f.parts for x in fuori) or f.name.endswith(".hb.md"):
                continue
            if "DEPRECATO" in f.name or f.name.startswith("ERRATA-"):
                continue
            if any(s in f.parents for s in snapshot):
                continue
            out.append(f)
    return out


def controlla_tetto_el() -> "list[dict]":
    """Gli incontri che sforano EL ≤ APL+4 senza il `Boost log:` che lo deroga."""
    apl = party_apl()
    if apl is None:
        return [{"file": "campaign/state.md", "el": None, "tetto": None,
                 "perche": "nessun **Party APL:** dichiarato: il tetto non è calcolabile"}]
    tetto = apl + MARGINE_TETTO
    fuori: "list[dict]" = []
    self_marcati = 0
    for f in _file_di_gioco():
        testo = f.read_text(encoding="utf-8", errors="replace")
        deroga = bool(DEROGA.search(testo))
        visti = set()
        for riga in testo.splitlines():
            for m in EL_DICHIARATO.finditer(riga):
                self_marcati += 1
                el = int(m.group(1))
                if el <= tetto or el in visti:
                    continue
                visti.add(el)
                fuori.append({
                    "file": str(f.relative_to(ROOT)), "el": el, "tetto": tetto,
                    "deroga": deroga, "riga": riga.strip()[:110],
                    "perche": (f"EL {el} oltre il tetto APL+{MARGINE_TETTO} = {tetto}"
                               + ("" if deroga else " e il file non porta un `Boost log:`")),
                })
    sfori = [x for x in fuori if not x.get("deroga")]
    if not self_marcati:
        # ⚠️ Non e' un successo: e' un controllo senza superficie.
        sfori.append({
            "file": "(nessuno)", "el": None, "tetto": tetto, "deroga": False,
            "perche": "ZERO incontri marcati con la forma `**EL**: N` che "
                      "AGENTS.md prescrive: il tetto non e' misurabile finche' "
                      "gli incontri non si dichiarano. 150 EL esistono nel repo "
                      "in forma nuda, e distinguere una dichiarazione da una "
                      "menzione con una regex darebbe un numero finto",
        })
    return sfori


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Gate CI: verifica i master ARC*-DEF-* contro la checklist module-standard.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true", help="dettaglio per file")
    ap.add_argument("--json", action="store_true",
                    help="emette il report in JSON (opt-in) invece del testo")
    ap.add_argument("--tetto-el", action="store_true",
                    help="il tetto EL ≤ APL+4 su tutto il contenuto di gioco "
                         "(severità CRITICA: il Boost log lo deroga)")
    args = ap.parse_args(argv)
    verbose = args.verbose

    if args.tetto_el:
        sfori = controlla_tetto_el()
        apl = party_apl()
        if args.json:
            print(json.dumps({"tool": "validate_modules", "modo": "tetto_el",
                              "ok": not sfori, "party_apl": apl,
                              "tetto": (apl + MARGINE_TETTO) if apl else None,
                              "sfori": sfori}, indent=2, ensure_ascii=False))
            return 1 if sfori else 0
        # ⚠️ «Nessun incontro marcato» e' un RILIEVO, non un fallimento: non
        # c'e' niente di rotto da aggiustare, c'e' una marcatura da mettere. Il
        # controllo esce 1 solo su uno sforamento VERO, cosi' puo' stare in CI
        # oggi e diventare rosso il giorno in cui un incontro sfora davvero.
        veri = [s for s in sfori if s["el"] is not None]
        if not veri:
            print(f"✓ validate_modules --tetto-el: APL {apl}, tetto "
                  f"{apl + MARGINE_TETTO} — nessuno sforamento")
            for s in sfori:
                print(f"  ⚠ {s['perche']}")
            return 0
        tetto = (apl + MARGINE_TETTO) if apl else "?"
        print(f"✗ validate_modules --tetto-el: {len(veri)} sforamenti "
              f"(APL {apl}, tetto {tetto})")
        for s in veri:
            print(f"  - {s['file']}: {s['perche']}")
            if s.get("riga"):
                print(f"      «{s['riga']}»")
        print("\n  La deroga prevista è il `Boost log:` di "
              "`skills/npc-villain-boosting/`: mai potenziare in silenzio.")
        return 1

    masters = sorted(ROOT.glob(f"**/{GLOB}"))
    masters = [m for m in masters if "_ARCHIVIO" not in m.parts and "build" not in m.parts]
    if not masters:
        if args.json:
            print(json.dumps({"tool": "validate_modules", "ok": True,
                              "masters": 0, "findings": []}, indent=2, ensure_ascii=False))
        else:
            print("✓ validate_modules: nessun master ARC*-DEF-* nel repo — ok")
        return 0

    total_err = 0
    findings = []
    for m in masters:
        errors, warnings = check_file(m, verbose)
        rel = m.relative_to(ROOT)
        findings.append({"file": str(rel), "errors": errors, "warnings": warnings})
        if not args.json:
            for w in warnings:
                print(f"  ⚠ {rel}: {w}")
            for e in errors:
                print(f"  ✗ {rel}: {e}")
        total_err += len(errors)

    if args.json:
        print(json.dumps({"tool": "validate_modules", "ok": total_err == 0,
                          "masters": len(masters), "findings": findings},
                         indent=2, ensure_ascii=False))
        return 1 if total_err else 0

    if total_err:
        print(f"✗ validate_modules: {len(masters)} master, {total_err} errore/i "
              f"(checklist skill rumblingstone-module-standard)")
        return 1
    print(f"✓ validate_modules: {len(masters)} master conformi alla checklist "
          f"module-standard — 0 errori")
    return 0


if __name__ == "__main__":
    sys.exit(main())
