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
  R8  le persone con stato `ignoto` si CONTANO, per la stessa ragione di R7
  R9  `reversibile` è obbligatorio appena `stato` non è `attivo`: in questa
      campagna un morto torna, e registrare l'uscita di scena senza dire se è
      definitiva è registrare meno di quello che il canone sa
  R10 ogni `png_id` risolve a una voce dell'anagrafica `png`, gli id sono unici,
      e un `scheda: null` porta sempre il proprio perché
  R11 ogni `scheda` dichiarata punta a un file che esiste davvero
  R12 le voci senza scheda si CONTANO, per la stessa ragione di R7 e R8
  R13 un buco dichiarato non deve avere candidati evidenti nel repo: dire
      «ho cercato e non c'è» è un'affermazione, e va messa alla prova

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
        # `bool` è sottoclasse di `int` in Python: l'ordine conta, e `integer`
        # sopra lo esclude apposta — `giorno_corrente: true` non è il Giorno 1.
        if t == "boolean" and isinstance(value, bool):
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


#: Le sezioni le cui righe sono UNA PERSONA, e quindi hanno uno stato vivo.
#:
#: ⚠️ §4 `conoscenze` **non** è qui, ed è una scelta misurata il 2026-09-16, non
#: una dimenticanza: tre delle sue righe non sono persone («Druid Circle of the
#: Sacred Forest», «Lathander + Mask», «Tiri Kitor wild elves») e tre persone
#: vi compaiono sotto **due nomi diversi** (Sonjak, Varis, Zalkatar/Sethrax).
#: Metterci `stato` costringerebbe a un valore privo di senso in tre righe e a
#: due copie divergenti in altre tre. La casa giusta è l'anagrafica dei PNG, che
#: è il lotto successivo — quello della chiave verso `Bestiario/`.
CON_STATO = ("villain", "party")


def stati_ignoti(d: dict) -> "dict[str, int]":
    """R8 · quante persone hanno lo stato `ignoto`, sezione per sezione.

    Come R7: non è un errore, è un numero che deve restare **visibile**.
    `ignoto` è la risposta onesta quando i PG non sanno l'esito, e va contato
    perché scenda quando il DM lo dichiara — non perché si smetta di usarlo.
    """
    fuori = {}
    for nome in CON_STATO:
        n = sum(1 for r in d.get(nome) or [] if r.get("stato") == "ignoto")
        if n:
            fuori[nome] = n
    return fuori


def reversibilita_mancante(d: dict) -> "list[str]":
    """R9 · `reversibile` è obbligatorio appena lo stato non è `attivo`.

    In questa campagna un morto torna — il Ghostlord nasce da un morto, Sal è
    protetto da un paradosso auto-consistente, Hella è morta in attesa del rito.
    Registrare «morto» senza dire se è definitivo è registrare **meno** di
    quello che il canone sa, e chi legge il dato dopo non ha modo di accorgersene.
    """
    errs = []
    for nome in CON_STATO:
        for i, r in enumerate(d.get(nome) or []):
            if r.get("stato") not in (None, "attivo") and "reversibile" not in r:
                chi = r.get("villain") or r.get("pg") or f"#{i}"
                errs.append(f"R9 · {nome}[{i}] ({chi}): stato "
                            f"'{r.get('stato')}' senza `reversibile` — "
                            "dire se il canone prevede un ritorno non è "
                            "opzionale quando qualcuno esce di scena")
    return errs


# --- la chiave verso il Bestiario (D17) --------------------------------------

#: Le sezioni le cui righe puntano all'anagrafica `png`.
CON_PNG_ID = ("villain", "conoscenze")


def riferimenti_rotti(d: dict) -> "list[str]":
    """R10 · ogni `png_id` risolve a una voce dell'anagrafica.

    Un id che non risolve e' un collegamento rotto che **nessuno vedrebbe**: il
    nome per esteso resta leggibile nella riga, quindi il documento sembra sano
    e solo la macchina inciampa.
    """
    noti = {r.get("id") for r in d.get("png") or []}
    errs = []
    for nome in CON_PNG_ID:
        for i, r in enumerate(d.get(nome) or []):
            pid = r.get("png_id")
            if pid and pid not in noti:
                errs.append(f"R10 · {nome}[{i}]: png_id '{pid}' non e' "
                            "nell'anagrafica `png`")
    return errs


def schede_inesistenti(d: dict, radice: Path) -> "list[str]":
    """R11 · ogni `scheda` dichiarata punta a un file che esiste davvero.

    🔴 E' la regola che rende la chiave una chiave. Senza, `scheda` sarebbe una
    stringa plausibile — cioe' la stessa cosa che si aveva prima, scritta meglio.
    Le schede si spostano e si rinominano: questa regola se ne accorge il giorno
    stesso, non sei settimane dopo al tavolo.
    """
    errs = []
    for i, r in enumerate(d.get("png") or []):
        s = r.get("scheda")
        if s and not (radice / s).exists():
            errs.append(f"R11 · png[{i}] ({r.get('id')}): la scheda '{s}' "
                        "non esiste sul filesystem")
    return errs


def anagrafica_incoerente(d: dict) -> "list[str]":
    """R10-bis · id unici, e un `scheda: null` porta sempre il suo perche'.

    Un buco senza motivo scritto e' indistinguibile da una dimenticanza, e alla
    rilettura qualcuno lo «corregge» indovinando — che e' il danno che tutto
    questo lotto esiste per evitare.
    """
    errs = []
    visti = {}
    for i, r in enumerate(d.get("png") or []):
        pid = r.get("id")
        if pid in visti:
            errs.append(f"R10-bis · png[{i}]: id '{pid}' gia' usato a png[{visti[pid]}]")
        visti[pid] = i
        if r.get("scheda") is None and not r.get("perche_senza_scheda"):
            errs.append(f"R10-bis · png[{i}] ({pid}): `scheda: null` senza "
                        "`perche_senza_scheda` — un buco senza motivo scritto "
                        "verra' riempito indovinando")
    return errs


def png_senza_scheda(d: dict) -> "list[str]":
    """R12 · chi non ha una scheda si CONTA, come R7 e R8."""
    return [r.get("id") for r in d.get("png") or [] if r.get("scheda") is None]


#: Cartelle che rispecchiano o generano altro: cercarci dentro trova copie,
#: non originali.
FUORI_RAGGIO = ("build/", ".claude/", ".chatgpt/", ".windsurf/", ".github/",
                "plans/", "_ARCHIVIO/", "docs/audit/")


def _parole_chiave(rec: dict) -> "list[str]":
    """Le parole con cui si cerca la scheda di una voce: dall'`id`, lunghe >4."""
    return [p for p in str(rec.get("id", "")).split("-") if len(p) > 4]


def buchi_con_candidati(d: dict, radice: Path) -> "list[str]":
    """R13 · un buco dichiarato non deve avere candidati evidenti nel repo.

    🐛 **Questa regola nasce da un errore mio, e lo dice.** Costruendo
    l'anagrafica ho cercato le schede **solo dentro `Bestiario/`**, poi ho
    troncato un `grep` a sei righe e ho concluso dalla lista tagliata che
    Zalkatar e Saarvith+Regiarix non avessero una scheda da nessuna parte.
    Ne avevano una ciascuno, **con statblocco completo a GS 13**, nell'arco 09 —
    e il Cerchio Druidico ne aveva una nel Bestiario sotto un nome che la mia
    ricerca non copriva. Tre buchi su quattro erano falsi, e li ho scritti in un
    ADR.

    Un buco dichiarato e' un'affermazione forte: dice «ho cercato e non c'e'».
    Questa regola la mette alla prova a ogni esecuzione, su **tutto** il repo
    scritto a mano — perche' una scheda puo' vivere in un arco, non solo nel
    Bestiario. Se emergono candidati, o uno di quelli e' la scheda, o va detto
    in `candidati_esclusi` perche' non lo e'.
    """
    errs = []
    fonti = None
    for i, r in enumerate(d.get("png") or []):
        if r.get("scheda") is not None:
            continue
        chiavi = _parole_chiave(r)
        if not chiavi:
            continue
        if fonti is None:
            fonti = [p for p in radice.rglob("*.md")
                     if not any(e in str(p.relative_to(radice)) + "/" for e in FUORI_RAGGIO)]
        esclusi = {str(x) for x in r.get("candidati_esclusi") or []}
        trovati = [str(p.relative_to(radice)) for p in fonti
                   if any(k in p.name.lower() for k in chiavi)
                   and str(p.relative_to(radice)) not in esclusi]
        if trovati:
            errs.append(
                f"R13 · png[{i}] ({r.get('id')}): dichiarato senza scheda, ma "
                f"esistono {len(trovati)} file che ne portano il nome — "
                f"{', '.join(trovati[:3])}"
                + (" …" if len(trovati) > 3 else "")
                + ". O uno di questi e' la scheda, o va scritto in "
                "`candidati_esclusi` perche' non lo e'.")
    return errs


def errori(data: dict, radice: Path = ROOT) -> "list[str]":
    """Tutte le violazioni bloccanti di uno stato, in un posto solo.

    Lo usa anche `azzera_partita.py`, che valida il gruppo nuovo prima di
    dichiararsi finito: con due elenchi di controlli, il giorno che se ne
    aggiunge uno il reset lo salterebbe senza dirlo.
    """
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    return (validate_schema(data, schema) + coherence_rules(data, schema)
            + reversibilita_mancante(data) + riferimenti_rotti(data)
            + anagrafica_incoerente(data)
            + schede_inesistenti(data, radice)
            + buchi_con_candidati(data, radice))


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

    errors = errori(data, ROOT)

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
    # Chi non e' in scena si CONTA nella riga di riepilogo: un villain
    # neutralizzato che nessuno nota e' un villain che torna per sbaglio.
    persone = (data.get("villain") or []) + (data.get("party") or [])
    fuori_scena = sum(1 for r in persone if r.get("stato") != "attivo")
    buchi = righe_senza_tempo(data)
    if buchi:
        tot = sum(buchi.values())
        print(f"  ⚠ R7 · {tot} righe senza tempo dichiarato — "
              + ", ".join(f"{k} {v}" for k, v in sorted(buchi.items())))
        print("     Non è un errore: §3, §4 e le due tabelle di Rethmar non hanno "
              "una colonna «Tempo»,")
        print("     e dedurne uno sarebbe inventare canone. Il numero resta in "
              "vista finché il DM non decide.")
    ignoti = stati_ignoti(data)
    if ignoti:
        tot = sum(ignoti.values())
        print(f"  ⚠ R8 · {tot} persone con stato `ignoto` — "
              + ", ".join(f"{k} {v}" for k, v in sorted(ignoti.items())))
        print("     Non è un errore: è la risposta onesta quando i PG non "
              "sanno l'esito. Scende quando il DM lo dichiara.")
    orfani = png_senza_scheda(data)
    if orfani:
        print(f"  ⚠ R12 · {len(orfani)} voci dell'anagrafica senza scheda nel "
              f"Bestiario: {', '.join(orfani)}")
        print("     Ognuna dichiara il perche'. Scrivere le schede mancanti e' "
              "contenuto, non infrastruttura.")
    print(f"✓ validate_state: {args.file.name} valido — "
          f"{len(data['archi'])} archi, {len(data['party'])} PG, "
          f"{len(data['artefatti'])} artefatti, {aperti} [INFERRED] aperti, "
          f"{fuori_scena} fuori scena")
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
