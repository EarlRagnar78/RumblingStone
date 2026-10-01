#!/usr/bin/env python3
"""registro_letture.py — le letture a freddo dei master, e quando vanno rifatte.

D26 di PIANO-LETTORE-E-PLAYTESTER, decisa il 2026-09-30: *«il registro delle
letture a freddo in JSON e il cancello in CI che chiede una lettura nuova
quando il master cambia»*. Lotto L4 di PIANO-AGENT-SKILLS-ESTERNE, con l'idea
dell'«ancora» di `first-reader` (awesome-llm-apps, ADR-0076): una lettura nuova
sullo stesso testo, confrontata con quella di prima.

Il registro `plans/letture-a-freddo.json` tiene, per ogni master DEF, le
letture fatte: ruolo (lettore, playtester, dm), data, rapporto, l'**impronta**
del testo letto e i rilievi 🔴 e 🟠 con il loro stato (`corretto`, `residuo`
con la ragione, `domanda` con la decisione del DM).

Il cancello dice **quando** una lettura va rifatta; la lettura la fa un agente.
Per ogni master, l'ultima lettura di ogni ruolo e':
- `senza impronta`: non si sa quale testo ha letto (le diciotto letture fatte
  prima del 2026-10-01 sono tutte cosi': il commit che le ha aggiunte ha
  cambiato anche il master, e la versione letta non si ricostruisce);
- `scaduta`: il master e' cambiato dopo, e nessuna voce «sola forma» lo copre;
- `allineata`.

**Avviso, poi bloccante da solo** (D4, il DM: *«dopo se c'e' l'avviso vogliono
siano bloccati cosi' si modificano davvero»*). Si decide **master per master**:
finche' un master non ha una lettura con impronta del lettore **e** del
playtester, i suoi problemi sono avvisi. Appena le ha, il master e' sotto
cancello e `--check` esce 1 su una sua lettura scaduta o su un suo 🔴/🟠 senza
stato. Non torna piu' in avviso, e un master nuovo senza letture non ci
rimette gli altri. Nessun interruttore a mano.

Uso:
    python3 scripts/registro_letture.py                       # la tabella
    python3 scripts/registro_letture.py --check               # il cancello
    python3 scripts/registro_letture.py --registra <master> --ruolo lettore \\
        --corsa <corsa>/<lettore> [--rapporto R.md]           # aggiunge una lettura
    python3 scripts/registro_letture.py --sola-forma <master> --ragione "…"
    python3 scripts/registro_letture.py --confronta <corsaA>/<l> <corsaB>/<l>

Solo libreria standard.
Exit code: 0 = ok o avviso · 1 = un master sotto cancello ha una lettura da rifare · 2 = registro malformato.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRO = ROOT / "plans" / "letture-a-freddo.json"
GLOB_MASTER = "ARC*-DEF-*.md"
FUORI = ("_ARCHIVIO/", "build/", ".claude/", "homebrew/")
RUOLI_OBBLIGATORI = ("lettore", "playtester")
STATI = ("corretto", "residuo", "domanda")
_RIGA_RILIEVO = re.compile(r"^\|\s*(\d+)\s*\|.*?(🔴|🟠)", re.M)


def impronta(testo: str) -> str:
    return hashlib.sha256(testo.encode("utf-8")).hexdigest()


def masters() -> "list[str]":
    return sorted(f.relative_to(ROOT).as_posix() for f in ROOT.glob(f"**/{GLOB_MASTER}")
                  if not any(x in f.relative_to(ROOT).as_posix() for x in FUORI))


def carica() -> dict:
    return json.loads(REGISTRO.read_text(encoding="utf-8"))


def salva(dati: dict) -> None:
    REGISTRO.write_text(json.dumps(dati, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ultime(voce: dict) -> "dict[str, dict]":
    """L'ultima lettura di ogni ruolo, per data (a parita', l'ultima scritta)."""
    out: "dict[str, dict]" = {}
    for lettura in voce.get("letture", []):
        precedente = out.get(lettura["ruolo"])
        if precedente is None or lettura["data"] >= precedente["data"]:
            out[lettura["ruolo"]] = lettura
    return out


def raggiungibile(da: str, a: str, sola_forma: "list[dict]") -> bool:
    """`a` si raggiunge da `da` con una catena di voci «sola forma»."""
    visti, attuale = set(), da
    while attuale != a:
        if attuale in visti:
            return False
        visti.add(attuale)
        passo = next((s for s in sola_forma if s["da"] == attuale), None)
        if passo is None:
            return False
        attuale = passo["a"]
    return True


def stato_master(rel: str, voce: dict) -> "tuple[dict, list[str]]":
    """Lo stato di ogni ruolo, e i problemi che bloccano a registro popolato."""
    corrente = impronta((ROOT / rel).read_text(encoding="utf-8"))
    stati, problemi = {}, []
    for ruolo, lettura in sorted(ultime(voce).items()):
        if not lettura.get("impronta"):
            stati[ruolo] = "senza impronta"
            continue
        if raggiungibile(lettura["impronta"], corrente, voce.get("sola_forma", [])):
            stati[ruolo] = "allineata"
        else:
            stati[ruolo] = "scaduta"
            problemi.append(f"{rel}: il {ruolo} ha letto un testo che non c'e' piu' "
                            f"(lettura del {lettura['data']}): serve una lettura nuova, o una voce «sola forma»")
        for r in lettura.get("rilievi", []):
            if r.get("gravita") in ("🔴", "🟠") and r.get("stato") not in STATI:
                problemi.append(f"{rel}: rilievo {r.get('n')} {r.get('gravita')} del {ruolo} senza stato "
                                f"({' · '.join(STATI)})")
            elif r.get("stato") == "residuo" and not r.get("ragione"):
                problemi.append(f"{rel}: rilievo {r.get('n')} residuo senza ragione")
            elif r.get("stato") == "domanda" and not r.get("decisione"):
                problemi.append(f"{rel}: rilievo {r.get('n')} in domanda senza la decisione del DM")
    for ruolo in RUOLI_OBBLIGATORI:
        stati.setdefault(ruolo, "nessuna lettura")
    return stati, problemi


def sotto_cancello(voce: dict) -> bool:
    """L'ultima lettura di ogni ruolo obbligatorio ha l'impronta del testo letto.

    Si decide master per master: un master nuovo senza letture resta in avviso
    e non rimette in avviso quelli che il cancello tiene gia'.
    """
    ult = ultime(voce)
    return all(ult.get(r, {}).get("impronta") for r in RUOLI_OBBLIGATORI)


def rilievi_dal_rapporto(rapporto: Path) -> "list[dict]":
    testo = rapporto.read_text(encoding="utf-8")
    return [{"n": int(n), "gravita": g, "stato": None} for n, g in _RIGA_RILIEVO.findall(testo)]


def registra(rel: str, ruolo: str, corsa: Path, rapporto: "Path | None") -> dict:
    stato = json.loads((corsa / "stato.json").read_text(encoding="utf-8"))
    corrente = impronta((ROOT / rel).read_text(encoding="utf-8"))
    if stato["impronta_master"] != corrente:
        raise ValueError(f"la corsa ha letto un testo diverso da {rel} di oggi: si registra la lettura "
                         "del testo che c'e', non di un altro")
    return {"ruolo": ruolo, "data": dt.date.today().isoformat(),
            "rapporto": rapporto.relative_to(ROOT).as_posix() if rapporto else None,
            "corsa": corsa.as_posix(), "impronta": corrente,
            "smesso_a": stato.get("smesso_a"),
            "rilievi": rilievi_dal_rapporto(rapporto) if rapporto else []}


def confronta(a: Path, b: Path) -> str:
    """Scena per scena, l'ago prima e dopo: dove la lettura e' cambiata."""
    def leggi(c: Path) -> "dict[str, str]":
        out = {}
        for riga in (c / "diario.jsonl").read_text(encoding="utf-8").splitlines():
            v = json.loads(riga)
            m = re.search(r"ago\s*=\s*([+-]?\d)", v["diario"])
            out[v["titolo"]] = (m.group(1) if m else "?") + (" SMESSO" if v.get("smesso") else "")
        return out
    prima, dopo = leggi(a), leggi(b)
    righe = [f"{'passaggio':48} {'prima':>9} {'dopo':>9}"]
    for titolo in list(dict.fromkeys(list(prima) + list(dopo))):
        righe.append(f"{titolo[:48]:48} {prima.get(titolo, '—'):>9} {dopo.get(titolo, '—'):>9}")
    return "\n".join(righe)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="il cancello: avviso finche' il registro non e' popolato, poi bloccante")
    ap.add_argument("--registra", metavar="MASTER", help="aggiunge la lettura di una corsa di lettura_a_scene.py")
    ap.add_argument("--ruolo", choices=("lettore", "playtester", "dm"))
    ap.add_argument("--corsa", type=Path, help="<corsa>/<lettore>, con stato.json")
    ap.add_argument("--rapporto", type=Path, help="il rapporto con la tabella dei rilievi")
    ap.add_argument("--sola-forma", metavar="MASTER", help="dichiara che il master e' cambiato solo nella forma")
    ap.add_argument("--ragione")
    ap.add_argument("--confronta", nargs=2, type=Path, metavar=("A", "B"))
    a = ap.parse_args(argv)

    if a.confronta:
        print(confronta(*a.confronta))
        return 0
    try:
        dati = carica()
    except (OSError, json.JSONDecodeError) as e:
        print(f"✗ registro_letture: registro illeggibile — {e}")
        return 2
    voci = dati.setdefault("master", {})
    if a.registra:
        if not (a.ruolo and a.corsa):
            ap.error("--registra vuole --ruolo e --corsa")
        try:
            voci.setdefault(a.registra, {"letture": [], "sola_forma": []})["letture"].append(
                registra(a.registra, a.ruolo, a.corsa, a.rapporto))
        except ValueError as e:
            print(f"✗ {e}")
            return 1
        salva(dati)
        print(f"✓ registrata la lettura del {a.ruolo} di {a.registra}")
        return 0
    if a.sola_forma:
        if not a.ragione:
            ap.error("--sola-forma vuole --ragione")
        voce = voci.setdefault(a.sola_forma, {"letture": [], "sola_forma": []})
        catena = voce.setdefault("sola_forma", [])
        base = catena[-1]["a"] if catena else next(
            (lt["impronta"] for lt in sorted(voce["letture"], key=lambda x: x["data"]) if lt.get("impronta")), None)
        if base is None:
            print("✗ non c'e' una lettura con impronta da cui partire: serve prima una lettura")
            return 1
        catena.append({"da": base, "a": impronta((ROOT / a.sola_forma).read_text(encoding="utf-8")),
                       "data": dt.date.today().isoformat(), "ragione": a.ragione})
        salva(dati)
        print(f"✓ «sola forma» registrata per {a.sola_forma}")
        return 0

    bloccanti, avvisi = [], []
    for rel in masters():
        voce = voci.get(rel, {})
        stati, problemi = stato_master(rel, voce)
        dentro = sotto_cancello(voce)
        (bloccanti if dentro else avvisi).extend(problemi)
        segno = "🔒" if dentro else "⚠️ "
        print(f"{segno} {rel.split('/')[-1][:44]:44} " + " · ".join(f"{r}: {s}" for r, s in sorted(stati.items())))
    if avvisi or any(not sotto_cancello(voci.get(r, {})) for r in masters()):
        print("\n⚠️  i master senza 🔒 sono in AVVISO: diventano bloccanti da soli quando hanno una lettura "
              "con impronta di lettore e playtester (D4).")
        for p in avvisi:
            print(f"   avviso: {p}")
    for p in bloccanti:
        print(f"  ✗ {p}")
    if a.check and bloccanti:
        print(f"✗ registro_letture: {len(bloccanti)} problema/i sui master sotto cancello")
        return 1
    if not bloccanti:
        print("✓ registro_letture: nessun master sotto cancello ha una lettura da rifare")
    return 0

if __name__ == "__main__":
    sys.exit(main())
