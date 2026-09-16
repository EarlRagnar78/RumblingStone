#!/usr/bin/env python3
"""validate_state.py — gate su campaign/state.yaml (ADR-0050).

Scopo
  Verificare che i fatti di canone strutturati rispettino il contratto
  `scripts/schemas/campaign_state.schema.json` **e** le regole di coerenza che
  uno schema da solo non esprime.

  Nasce dal finding C1 dell'audit 2026-08: in `state.md` la distinzione fra
  giocato e preparato era una convenzione di prosa, quindi dimenticabile — e
  dimenticata. Qui è una chiave obbligatoria, quindi il file **non è valido**
  se un fatto non dichiara il proprio tempo.

  Nota di onestà sul limite: uno schema vincola la FORMA, non la VERITÀ. Un
  agente può ancora scrivere un fatto falso in un file perfettamente valido.
  Ciò che questo gate rende impossibile è più ristretto e più utile: scriverlo
  **senza dire a quale tempo appartiene**.

  ⚠️ E qui la promessa va ridimensionata, perché il 2026-09-16 si è scoperto
  che il canone non la mantiene ovunque. `archi` dichiara il tempo per riga;
  `party` e `artefatti` lo dichiarano come DUE COLONNE. Ma §3 (clock dei
  villain), §4 (chi sa cosa) e le due tabelle di Rethmar **non hanno una
  colonna Tempo**, e nessun banner la supplisce: il generatore recuperato
  dalla PR #99 ne aggiungeva una, ma quella forma è del 10 agosto e il lotto
  4c ha ridisegnato quelle sezioni cinque settimane dopo.

  Assegnare un tempo a quelle righe sarebbe **dedurlo** — plausibilmente, e
  comunque inventando canone in un lotto di infrastruttura. Quindi il campo è
  opzionale lì, e R7 le **conta a ogni esecuzione**: il numero si vede, non
  cresce in silenzio, e il giorno che il DM decide di dichiararlo il conteggio
  scende da sé. È la forma di ADR-0041: contare ciò che non è dichiarato vale
  più che indovinarlo.

Regole di coerenza (oltre allo schema)
  R1  ogni `id` in `inferred` è unico
  R2  ogni `dove` di un `inferred` punta a una sezione nota
  R3  esiste almeno un arco `in_corso` oppure il confine lo nega esplicitamente
  R4  nessun arco `giocato` sta dopo un arco `preparato` (ordine del cruscotto)
  R5  se un PG ha `preparato` valorizzato, `oggi` non può esserne una copia
  R6  echi: gli annullati portano il perché, gli armati portano il payoff,
      e nessun ID si riusa
  R7  il tempo non dichiarato si CONTA, non si indovina (vedi sotto)

Uso
  python3 scripts/validate_state.py [--file PATH] [--json] [--verbose]

Input   campaign/state.yaml + scripts/schemas/campaign_state.schema.json
Output  stdout testuale, oppure JSON con --json
Exit    0 = valido · 1 = violazioni · 2 = errore d'uso o dipendenza mancante
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "campaign" / "state.yaml"
SCHEMA = ROOT / "scripts" / "schemas" / "campaign_state.schema.json"

try:
    import yaml
except ImportError:  # pragma: no cover
    print("✗ validate_state: serve pyyaml (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

def sezioni_note(schema: dict) -> tuple[str, ...]:
    """Le sezioni valide per il campo `dove` di un [INFERRED].

    Derivate DALLO SCHEMA, non cablate: la prima versione le elencava a mano e
    si è disallineata al primo lotto che ha aggiunto sezioni (G2-ter). Una
    lista scritta due volte è una lista che diverge.
    """
    return tuple(k for k in schema.get("properties", {})
                 if k not in ("schema_version", "inferred"))


# --- validazione schema minimale (stdlib) ------------------------------------
# Volutamente NON si dipende da `jsonschema`: il repo dichiara le dipendenze
# per-tool nel manifest e ne aggiunge una solo se serve davvero. Qui basta il
# sottoinsieme di draft-07 effettivamente usato dallo schema.

def _type_ok(value, spec) -> bool:
    types = spec if isinstance(spec, list) else [spec]
    for t in types:
        if t == "object" and isinstance(value, dict):
            return True
        if t == "array" and isinstance(value, list):
            return True
        if t == "string" and isinstance(value, str):
            return True
        if t == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if t == "null" and value is None:
            return True
    return False


def validate_schema(data, schema, path="") -> list[str]:
    errs: list[str] = []
    if "const" in schema and data != schema["const"]:
        errs.append(f"{path or '<root>'}: atteso {schema['const']!r}, trovato {data!r}")
        return errs
    if "enum" in schema and data not in schema["enum"]:
        errs.append(f"{path or '<root>'}: {data!r} non è fra {schema['enum']}")
        return errs
    if "type" in schema and not _type_ok(data, schema["type"]):
        errs.append(f"{path or '<root>'}: tipo {type(data).__name__} non ammesso "
                    f"(atteso {schema['type']})")
        return errs
    if isinstance(data, str):
        if "minLength" in schema and len(data) < schema["minLength"]:
            errs.append(f"{path}: stringa troppo corta ({len(data)} < {schema['minLength']})")
        if "pattern" in schema:
            import re
            if not re.search(schema["pattern"], data):
                errs.append(f"{path}: {data!r} non rispetta il pattern {schema['pattern']}")
    if isinstance(data, list):
        if "minItems" in schema and len(data) < schema["minItems"]:
            errs.append(f"{path}: servono almeno {schema['minItems']} elementi")
        item = schema.get("items")
        if item:
            for i, v in enumerate(data):
                errs += validate_schema(v, item, f"{path}[{i}]")
    if isinstance(data, dict):
        for req in schema.get("required", []):
            if req not in data or data[req] is None and req != "note":
                if req not in data:
                    errs.append(f"{path or '<root>'}: manca la chiave obbligatoria «{req}»")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for k in data:
                if k not in props:
                    errs.append(f"{path or '<root>'}: chiave non prevista «{k}»")
        for k, v in data.items():
            if k in props:
                errs += validate_schema(v, props[k], f"{path}.{k}" if path else k)
    return errs


# --- regole di coerenza -------------------------------------------------------

def coherence_rules(d: dict, schema: "dict | None" = None) -> list[str]:
    errs: list[str] = []
    note = sezioni_note(schema) if schema else tuple(
        k for k in d if k not in ("schema_version", "inferred"))

    ids = [i["id"] for i in d.get("inferred", [])]
    dup = {x for x in ids if ids.count(x) > 1}
    if dup:
        errs.append(f"R1 · id [INFERRED] duplicati: {sorted(dup)}")

    for i in d.get("inferred", []):
        head = i.get("dove", "").split("[")[0].split(".")[0]
        if head not in note:
            errs.append(f"R2 · {i.get('id')}: «dove» punta a «{head}», che non è una sezione nota "
                        f"({', '.join(note)})")

    archi = d.get("archi", [])
    if not any(a["tempo"] == "in_corso" for a in archi):
        errs.append("R3 · nessun arco marcato «in_corso»: se è voluto, dirlo nel confine")

    tempi = [a["tempo"] for a in archi]
    if "preparato" in tempi:
        primo_prep = tempi.index("preparato")
        dopo = [a["arco"] for a in archi[primo_prep:] if a["tempo"] == "giocato"]
        if dopo:
            errs.append(f"R4 · archi «giocato» dopo il primo «preparato» (cruscotto fuori ordine): {dopo}")

    for p in d.get("party", []):
        prep = p.get("preparato")
        if prep and prep.strip() == (p.get("oggi") or "").strip():
            errs.append(f"R5 · {p['pg']}: «preparato» è identico a «oggi» — usare null se non diverge")

    # R6 — Echo Ledger. Le due regole che la storia di E-07c/E-07e ha reso
    # necessarie: un'eco annullata deve dire PERCHÉ (altrimenti sparisce la
    # lezione insieme all'eco), e un ID non si riusa mai.
    visti: dict[str, int] = {}
    for e in d.get("echi", []):
        visti[e["id"]] = visti.get(e["id"], 0) + 1
        if e["stato"] == "annullato" and not (e.get("nota_stato") or "").strip():
            errs.append(f"R6 · {e['id']}: eco annullata senza `nota_stato` — "
                        "un'eco che sparisce senza il perché porta via anche la lezione")
        if e["stato"] == "armato" and not (e.get("payoff") or "").strip():
            errs.append(f"R6 · {e['id']}: eco armata senza `payoff` — "
                        "un'eco che non dice come riemerge non è armata, è un appunto")
    for id_, n in visti.items():
        if n > 1:
            errs.append(f"R6 · {id_}: ID usato {n} volte — gli ID degli echi non si riusano "
                        "(consequence-echoes.md §1)")

    return errs


SENZA_TEMPO = ("villain", "conoscenze", "difensori_rethmar", "scenari_rethmar")


def righe_senza_tempo(d: dict) -> "dict[str, int]":
    """R7 · quante righe non dichiarano il proprio tempo, sezione per sezione.

    Non è un errore: è un **numero che deve restare visibile**. Vedi la nota
    in testa al modulo.
    """
    fuori = {}
    for nome in SENZA_TEMPO:
        mancanti = sum(1 for r in d.get(nome) or [] if not r.get("tempo"))
        if mancanti:
            fuori[nome] = mancanti
    return fuori


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="validate_state.py",
        description="Valida campaign/state.yaml contro schema e regole di coerenza (ADR-0050).",
    )
    ap.add_argument("--file", type=Path, default=STATE, help="File di stato da validare.")
    ap.add_argument("--json", action="store_true", help="Report in JSON (opt-in).")
    ap.add_argument("--verbose", action="store_true", help="Stampa il conteggio per sezione.")
    args = ap.parse_args(argv)

    if not args.file.exists():
        print(f"✗ validate_state: {args.file} non esiste", file=sys.stderr)
        return 2
    if not SCHEMA.exists():
        print(f"✗ validate_state: schema mancante ({SCHEMA})", file=sys.stderr)
        return 2

    try:
        data = yaml.safe_load(args.file.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        print(f"✗ validate_state: YAML malformato — {e}", file=sys.stderr)
        return 1

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = validate_schema(data, schema) + coherence_rules(data, schema)

    if args.json:
        print(json.dumps({"report_version": 1, "file": str(args.file.relative_to(ROOT)),
                          "valid": not errors, "errors": errors},
                         indent=2, ensure_ascii=False))
        return 1 if errors else 0

    if errors:
        print(f"✗ validate_state: {len(errors)} violazioni\n", file=sys.stderr)
        for e in errors:
            print(f"  · {e}", file=sys.stderr)
        return 1

    aperti = len(data.get("inferred", []))
    buchi = righe_senza_tempo(data)
    if buchi:
        tot = sum(buchi.values())
        print(f"  ⚠ R7 · {tot} righe senza tempo dichiarato — "
              + ", ".join(f"{k} {v}" for k, v in sorted(buchi.items())))
        print("     Non è un errore: §3, §4 e le due tabelle di Rethmar non hanno "
              "una colonna «Tempo»,")
        print("     e dedurne uno sarebbe inventare canone. Il numero resta in "
              "vista finché il DM non decide.")
    print(f"✓ validate_state: {args.file.name} valido — "
          f"{len(data['archi'])} archi, {len(data['party'])} PG, "
          f"{len(data['artefatti'])} artefatti, {aperti} [INFERRED] aperti")
    if args.verbose:
        for a in data["archi"]:
            print(f"    {a['tempo']:10s} {a['arco']}")
        for i in data.get("inferred", []):
            print(f"    {i['id']} → {i['a_chi']}: {i['domanda'][:70]}…")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
