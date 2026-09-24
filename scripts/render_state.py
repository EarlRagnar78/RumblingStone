#!/usr/bin/env python3
"""render_state.py — genera le tabelle di canone di state.md da state.yaml (ADR-0050).

Scopo
  `campaign/state.yaml` è il master dei fatti di §0 (archi), §1 (party),
  §2.4 (difensori e scenari di Rethmar), §3 (clock dei villain), §4 (chi sa cosa)
  e §6 (artefatti). Questo tool ne genera la **vista markdown** dentro le regioni
  marcate di `campaign/state.md`, così che il DM continui a leggere un documento
  e non uno YAML.

  È la ragione per cui il lotto esiste: senza rendering, `state.yaml` sarebbe una
  **seconda fonte di verità** — cioè esattamente il difetto C2 che l'audit ha
  appena chiuso (`state.md` e `campaign-history.md` che si dichiaravano entrambi
  sorgente unica). Un master e una vista generata; mai due master.

  Le sezioni di **prosa** (§5 promesse, §7 fili narrativi, i banner dei due tempi)
  NON sono toccate: restano scritte a mano, perché sono narrazione e non dati.

Regioni gestite
  archi · party · artefatti · villain · conoscenze · difensori · scenari
  <!-- gen:state:NOME --> … <!-- /gen:state:NOME -->

  Tutto ciò che sta fra i marcatori è **rigenerato**: non modificarlo a mano,
  la modifica va fatta in `state.yaml`.

Uso
  python3 scripts/render_state.py            # rigenera le regioni
  python3 scripts/render_state.py --check    # gate CI: segnala drift, non scrive
  python3 scripts/render_state.py --stdout   # stampa senza toccare i file

Input   campaign/state.yaml
Output  campaign/state.md (regioni marcate) — deterministico, idempotente
Exit    0 = ok / in sync · 1 = drift (--check) o errore di dominio · 2 = errore d'uso
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_YAML = ROOT / "campaign" / "state.yaml"
STATE_MD = ROOT / "campaign" / "state.md"

try:
    import yaml
except ImportError:  # pragma: no cover
    print("✗ render_state: serve pyyaml (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

FASE = {"giocato": "✅", "in_corso": "🟡", "preparato": "⬜"}

BANNER = ("<!-- GENERATO da scripts/render_state.py a partire da campaign/state.yaml — "
          "non modificare a mano (ADR-0050) -->")


def _cell(v) -> str:
    """Una cella markdown: None diventa em-dash, le pipe interne sono neutralizzate."""
    if v is None or (isinstance(v, str) and not v.strip()):
        return "—"
    return str(v).replace("|", "\\|").replace("\n", " ").strip()


def _fase(v) -> str:
    return FASE.get(v, _cell(v))


def _eco_origine(rec: dict) -> str:
    """Ricompone la cella «Origin (sess., PC, choice)» dai campi scomposti.

    ⚠️ La scomposizione non è cosmetica. La falla che il 2026-08-06 permise di
    *rinominare* E-07c invece di riscriverla nasceva dall'avere autore, data e
    scelta in **una stringa sola**: rovesciare un'eco su un altro PG era una
    modifica di testo. Con `autore` come campo, cambiare la mano che ha scelto
    è una modifica di **dato**, e lo schema può pretenderla obbligatoria.
    """
    autore = f"**{rec['autore']}**"
    if rec.get("coautore"):
        autore += f" *(e **{rec['coautore']}**, dall'altra parte)*"
    return f"{rec['data']} · {autore} · {_cell(rec.get('fatto'))}"


def _eco_id(rec: dict) -> str:
    return f"**{rec['id']}**"


def _eco_stato(rec: dict) -> str:
    """La vista porta il glifo; il dato porta il valore d'enumerazione."""
    return _cell(rec.get("tag") or rec.get("stato"))


#: Il glifo con cui la vista mostra lo stato di una persona (§3 villain, §1 PG).
#: Il DATO resta la parola: il glifo è presentazione, e cambiarlo non cambia
#: quello che gli script leggono.
GLIFO_STATO = {
    "attivo": "🔴 attivo",
    "latitante": "🟠 latitante",
    "neutralizzato": "🟡 neutralizzato",
    "morto": "⚫ morto",
    "ignoto": "❔ ignoto",
}


def _stato_persona(rec: dict) -> str:
    """Stato + reversibilità, che in questa campagna è metà dell'informazione.

    Un morto qui torna: il Ghostlord nasce da un morto, Sal è protetto da un
    paradosso auto-consistente. Dire «morto» e basta sarebbe dire meno di quel
    che il canone sa — per questo `reversibile` è obbligatorio appena lo stato
    non è `attivo` (regola R9 di `validate_state`).
    """
    stato = rec.get("stato")
    reso = GLIFO_STATO.get(stato, _cell(stato))
    if rec.get("reversibile") is True:
        reso += " *(reversibile)*"
    elif rec.get("reversibile") is False:
        reso += " *(definitivo)*"
    return reso


def _giorno(rec: dict) -> str:
    return _cell(rec.get("giorno"))


# ---------------------------------------------------------------------------
# Le tabelle sono DATI, non otto funzioni cablate.
#
# ⚠️ `intestazione` e `separatore` sono copiati **alla lettera** da
# `campaign/state.md`, e devono restarci uguali: il criterio d'uscita del lotto
# 4d-1 e' che il file rigenerato sia **byte-identico** a quello committato.
# Cambiare una di queste stringhe cambia il canone che il DM legge, e non e'
# una cosa che fa un refactor: `test_state_data` confronta le intestazioni con
# quelle del file vero e diventa rossa.
#
# 🔎 Il generatore recuperato dalla PR #99 emetteva una forma DIVERSA — colonna
# `Tempo` in §3 e §4, intestazioni italiane in §1 e §6 — perche' era del 10
# agosto, mentre il lotto 4c ha ridisegnato quelle sezioni il 12 settembre.
# Adottarla avrebbe riportato indietro la presentazione del canone di cinque
# settimane, come portare i dati del ramo avrebbe riportato indietro i fatti.
# ---------------------------------------------------------------------------
TABELLE = {
    "archi": {
        "chiave": "archi",
        "intestazione": "| Arc | Fase | Stato | March Clock | PG Lv | Note |",
        "separatore": "|---|---|---|---|---|---|",
        "campi": [("arco", _cell), ("tempo", _fase), ("stato", _cell),
                  ("march_clock", _cell), ("pg_livello", _cell), ("note", _cell)],
    },
    "party": {
        "chiave": "party",
        "intestazione": ("| PC | Class | Stato | 🟢 Dov'è **adesso** (tavolo, ARC-07 P4 chiuso) "
                         "| 🔵 Dove lo porta il canone **preparato** (post ARC-08) "
                         "| HP / status **oggi** | Open personal threads |"),
        "separatore": "|---|---|---|---|---|---|---|",
        "campi": [("pg", _cell), ("classe", _cell), (None, _stato_persona),
                  ("oggi", _cell), ("preparato", _cell), ("hp", _cell),
                  ("filoni", _cell)],
        "composto": True,
    },
    # §2.1 — i waypoint sono dato puro: dieci righe di giorno/luogo/esito.
    "waypoints": {
        "chiave": "march_clock",
        "sotto": "waypoints",
        "intestazione": "| Day | Waypoint | Status |",
        "separatore": "|---|---|---|",
        "campi": [("giorno", _cell), ("waypoint", _cell), ("stato", _cell)],
    },
    "difensori": {
        "chiave": "difensori_rethmar",
        "intestazione": "| Contingent | Count | Condition |",
        "separatore": "|---|---|---|",
        "campi": [("contingente", _cell), ("conteggio", _cell), ("condizione", _cell)],
    },
    "scenari": {
        "chiave": "scenari_rethmar",
        "intestazione": "| Scenario PG | Horde | Difensori | Rapporto |",
        "separatore": "|---|---|---|---|",
        "campi": [("scenario", _cell), ("orda", _cell), ("difensori", _cell),
                  ("rapporto", _cell)],
    },
    "villain": {
        "chiave": "villain",
        "intestazione": "| Villain | Stato | Where | Agenda | Clock | Trigger if filled |",
        "separatore": "|---|---|---|---|---|---|",
        "campi": [("villain", _cell), (None, _stato_persona), ("dove", _cell),
                  ("agenda", _cell), ("clock", _cell), ("trigger", _cell)],
        "composto": True,
    },
    "conoscenze": {
        "chiave": "conoscenze",
        "intestazione": "| NPC | Knows that... | Learned how / when |",
        "separatore": "|---|---|---|",
        "campi": [("png", _cell), ("sa_che", _cell), ("come", _cell)],
    },
    "artefatti": {
        "chiave": "artefatti",
        "intestazione": ("| Artifact | Holder | **Today at the table (ARC-07 P4)** "
                         "| **Prepared (ARC-09 entry)** |"),
        "separatore": "|---|---|---|---|",
        "campi": [("artefatto", _cell), ("portatore", _cell), ("oggi", _cell),
                  ("preparato", _cell)],
    },
    "echi": {
        "chiave": "echi",
        "intestazione": "| ID | Origin (sess., PC, choice) | Tone | Fuse | Payoff sketch | Status |",
        "separatore": "|----|----------------------------|------|------|---------------|--------|",
        "campi": [(None, _eco_id), ("origine_composta", _eco_origine),
                  ("tono", _cell), ("miccia", _cell), ("payoff", _cell),
                  (None, _eco_stato)],
        "composto": True,
    },
}


def _record(spec: dict, d: dict) -> list:
    """I record di una tabella, anche quando stanno sotto una sottochiave."""
    blocco = d.get(spec["chiave"]) or []
    if spec.get("sotto"):
        blocco = (blocco or {}).get(spec["sotto"]) or []
    return blocco


def rendi(nome: str, d: dict) -> str:
    """Una tabella, dalla sua specifica. Deterministico: stesso YAML, stesso testo."""
    spec = TABELLE[nome]
    out = [BANNER, "", spec["intestazione"], spec["separatore"]]
    composto = spec.get("composto")
    for rec in _record(spec, d):
        if composto:
            # il formattatore riceve il record intero: certe celle della vista
            # nascono da piu' campi (l'origine di un'eco e' data + autore + fatto)
            celle = [f(rec) if k is None or k.endswith("_composta") else f(rec.get(k))
                     for k, f in spec["campi"]]
        else:
            celle = [f(rec.get(k)) for k, f in spec["campi"]]
        out.append("| " + " | ".join(celle) + " |")
    return "\n".join(out)


def rendi_march_clock(d: dict) -> str:
    """Le due righe che scrive la macchina — decisione **D14**.

    🔴 Fino al 2026-09-16 queste due righe e il ragionamento del DM erano lo
    stesso paragrafo, e per questo `state_apply --migrate` si **rifiutava** di
    marcarle: sostituirle avrebbe lasciato orfane a metà frase le quattro righe
    che spiegano perché il Giorno 19 è un bersaglio e non un passato.

    Adesso il numero è un campo e la spiegazione sta sotto, fuori dalla regione:
    la macchina riscrive la sua riga a ogni sessione senza mai toccare la nota
    del DM. È l'attuazione della risposta del DM: *«la riga va in state.yaml e
    poi riportata in state.md»*.
    """
    mc = d.get("march_clock") or {}
    corrente, arrivo = mc.get("giorno_corrente"), mc.get("giorno_arrivo")
    if corrente is None or arrivo is None:
        raise ValueError("march_clock: servono giorno_corrente e giorno_arrivo")
    finestra = mc.get("finestra")
    coda = f" ({finestra})" if finestra else ""
    return (f"{BANNER}\n\n"
            f"**Current March Day:** **{corrente}**\n"
            f"**Days remaining to Rethmar:** **{arrivo - corrente}**{coda}")


RENDERERS = {nome: (lambda d, n=nome: rendi(n, d)) for nome in TABELLE}
RENDERERS["march_clock"] = rendi_march_clock


def region_re(name: str) -> re.Pattern:
    return re.compile(
        rf"(<!-- gen:state:{name} -->\n)(.*?)(\n<!-- /gen:state:{name} -->)",
        re.DOTALL,
    )


def apply_regions(md: str, data: dict) -> tuple[str, list[str]]:
    """Sostituisce il contenuto delle regioni. Ritorna (testo, regioni mancanti)."""
    missing = []
    for name, fn in RENDERERS.items():
        rx = region_re(name)
        if not rx.search(md):
            missing.append(name)
            continue
        md = rx.sub(lambda m: m.group(1) + fn(data) + m.group(3), md)
    return md, missing


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="render_state.py",
        description="Genera le tabelle di canone di state.md da state.yaml (ADR-0050).",
    )
    ap.add_argument("--check", action="store_true",
                    help="Verifica che le regioni siano allineate; non scrive nulla.")
    ap.add_argument("--stdout", action="store_true",
                    help="Stampa le regioni generate senza toccare i file.")
    args = ap.parse_args(argv)

    if not STATE_YAML.exists():
        print(f"✗ render_state: {STATE_YAML} non esiste", file=sys.stderr)
        return 2
    data = yaml.safe_load(STATE_YAML.read_text(encoding="utf-8"))

    if args.stdout:
        for name, fn in RENDERERS.items():
            print(f"--- {name} ---\n{fn(data)}\n")
        return 0

    md = STATE_MD.read_text(encoding="utf-8")
    new, missing = apply_regions(md, data)

    if missing:
        print("✗ render_state: regioni assenti in state.md: " + ", ".join(missing),
              file=sys.stderr)
        print("  Inserire i marcatori <!-- gen:state:NOME --> … <!-- /gen:state:NOME -->",
              file=sys.stderr)
        return 1

    if args.check:
        if new != md:
            print("✗ render_state: state.md è fuori sync con state.yaml", file=sys.stderr)
            print("  Rigenerare con: python3 scripts/render_state.py", file=sys.stderr)
            return 1
        print("✓ render_state: state.md allineato a state.yaml")
        return 0

    if new == md:
        print("✓ render_state: già allineato — nessuna scrittura")
        return 0
    STATE_MD.write_text(new, encoding="utf-8")
    print(f"✓ render_state: rigenerate {len(RENDERERS)} regioni in campaign/state.md")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
