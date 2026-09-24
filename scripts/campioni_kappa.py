#!/usr/bin/env python3
"""campioni_kappa.py — i due campioni disgiunti e l'accordo fra la macchina e chi decide.

## Perche' esiste

Il punteggio di `punteggio_mqm` dice che un documento vale 97,9. La domanda che
nessuna metrica risponde da sola e': **il DM sarebbe d'accordo?** Se non lo e',
il numero misura il suo autore, non il repo — ed e' il pilastro che
`PIANO-MISURA-EDITORIALE-STANDARD` §1.4 dichiara mancante fin dalla prima
stesura.

La misura standard e' il **κ di Cohen**: l'accordo fra due valutatori,
corretto per l'accordo che si otterrebbe **a caso**. Due giudici che dicono
«promosso» al 95% dei documenti concordano nel 90% dei casi anche tirando i
dadi: la percentuale grezza non dice niente, il κ si'.

    κ = (Po − Pe) / (1 − Pe)

dove `Po` e' l'accordo osservato e `Pe` quello atteso per caso. La soglia del
piano e' **κ ≥ 0,60** (Landis & Koch: «substantial»): sotto, la metrica **non
entra in CI** e si dichiara non affidabile.

## I due campioni, e perche' sono disgiunti

Il DM ha scelto due campioni distinti invece di due passaggi sullo stesso. E'
la scelta giusta: due valutatori sullo *stesso* campione misurano l'accordo ma
non la **copertura**; due campioni disgiunti misurano anche se la metrica
regge su materiale diverso.

| | Campione A | Campione B |
|---|---|---|
| **chi giudica** | il **DM** | un secondo modello |
| **cosa misura** | l'accordo fra la macchina e chi decide | la tenuta su materiale che il DM non ha visto |

⚠️ **Il κ che conta e' quello di A.** Se B da' κ alto e A basso, la metrica e'
coerente con se stessa e in disaccordo col DM — e in quel caso **ha torto la
metrica**.

🔴 **E il bias del giudice B va scritto, non nascosto.** Il secondo giudice e'
il modello di questa sessione, che ha **scritto meta' dei rilevatori**. Non e'
indipendente da loro: tendera' a concordare con la macchina piu' di un giudice
estraneo, e il κ(B) e' quindi un **limite superiore ottimistico**. Serve a
prendere gli errori grossolani, non a certificare la metrica.

## L'estrazione

Stratificata per classe, **disgiunta**, a **seme fisso**: due esecuzioni sullo
stesso commit danno gli stessi 40 file, nello stesso ordine. Senza seme fisso
il campione cambierebbe a ogni esecuzione e il κ non sarebbe confrontabile con
se stesso.

## Uso

    python3 scripts/campioni_kappa.py --estrai        # F1.5: i due campioni
    python3 scripts/campioni_kappa.py --scheda A      # la scheda da compilare
    python3 scripts/campioni_kappa.py --kappa         # F3.3: l'accordo, se i voti ci sono

Decisione: ADR-0059 §κ · piano: F1.5 e F3.3.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import punteggio_mqm as pm  # noqa: E402

CAMPIONI = ROOT / "campaign" / "misure" / "campioni-kappa.json"
VOTI = ROOT / "campaign" / "misure" / "voti-kappa.json"
SEME = 20260921          # la data dell'estrazione: fisso, e dichiarato
PER_CAMPIONE = 20


def estrai() -> dict:
    """I due campioni disgiunti, stratificati per classe, a seme fisso."""
    spec = pm.carica_specifiche()
    per_classe: "dict[str, list[str]]" = {}
    for f in pm.bersagli(spec, None):
        e = pm.valuta(f, spec)
        if e.get("classe") and e.get("punteggio") is not None:
            per_classe.setdefault(e["classe"], []).append(e["file"])
    rng = random.Random(SEME)
    a: "list[str]" = []
    b: "list[str]" = []
    # Stratificazione proporzionale, con almeno un documento per classe: senza
    # il minimo, `master_def` (5 file su 515) uscirebbe quasi sempre a zero e
    # il campione non direbbe niente sulla classe piu' curata del repo.
    totale = sum(len(v) for v in per_classe.values())
    for classe in sorted(per_classe):
        pool = sorted(per_classe[classe])
        rng.shuffle(pool)
        quota = max(1, round(PER_CAMPIONE * len(pool) / totale))
        a.extend(pool[:quota])
        b.extend(pool[quota:quota * 2])
    return {
        "seme": SEME,
        "per_campione": PER_CAMPIONE,
        "A": {"giudice": "il DM", "file": sorted(a[:PER_CAMPIONE])},
        "B": {"giudice": "un secondo modello (bias dichiarato: ha scritto "
                         "meta' dei rilevatori — il kappa di B e' un limite "
                         "superiore ottimistico)",
              "file": sorted(b[:PER_CAMPIONE])},
    }


def kappa(coppie: "list[tuple[str, str]]") -> "dict | None":
    """κ di Cohen su giudizi binari `promosso` / `bocciato`."""
    if not coppie:
        return None
    n = len(coppie)
    concordi = sum(1 for x, y in coppie if x == y)
    po = concordi / n
    cx, cy = Counter(x for x, _ in coppie), Counter(y for _, y in coppie)
    pe = sum(cx[k] * cy[k] for k in set(cx) | set(cy)) / (n * n)
    k = 1.0 if pe == 1 else (po - pe) / (1 - pe)
    return {"n": n, "accordo_osservato": round(po, 4),
            "accordo_atteso_per_caso": round(pe, 4), "kappa": round(k, 4),
            "lettura": _lettura(k), "supera_la_soglia": k >= 0.60}


def _lettura(k: float) -> str:
    """Landis & Koch 1977, la scala che il piano cita."""
    if k < 0:    return "peggio del caso"
    if k < 0.21: return "lieve"
    if k < 0.41: return "discreto"
    if k < 0.61: return "moderato"
    if k < 0.81: return "sostanziale"
    return "quasi perfetto"


def giudizio_macchina(percorso: str) -> str:
    spec = pm.carica_specifiche()
    e = pm.valuta(ROOT / percorso, spec)
    ok, _ = pm.promosso(e, spec)
    return "promosso" if ok else "bocciato"


def stampa_scheda(quale: str, dati: dict) -> None:
    c = dati[quale]
    print(f"\nSCHEDA DI VALUTAZIONE — campione {quale}\n" + "=" * 70)
    print(f"Giudice: {c['giudice']}\n")
    print("Per ogni documento, una sola domanda, e NON e' «e' bello»:\n")
    print("  «Questo documento rispetta le norme dichiarate abbastanza da")
    print("   poter essere consegnato al tavolo cosi' com'e'?»   promosso / bocciato\n")
    print("⚠️  Il punteggio della macchina NON e' stampato qui, apposta: vederlo")
    print("    prima di decidere e' il modo piu' rapido per misurare zero.\n")
    for i, f in enumerate(c["file"], 1):
        print(f"  {i:2}. [ promosso / bocciato ]  {f}")
    print(f"\nI voti si scrivono in {VOTI.relative_to(ROOT)}, nella forma:")
    print('  {"A": {"percorso/del/file.md": "promosso", ...}, "B": {...}}\n')


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--estrai", action="store_true", help="F1.5: scrive i due campioni")
    ap.add_argument("--scheda", choices=("A", "B"), help="la scheda da compilare")
    ap.add_argument("--kappa", action="store_true", help="F3.3: l'accordo, se i voti ci sono")
    args = ap.parse_args(argv)

    if args.estrai:
        dati = estrai()
        CAMPIONI.parent.mkdir(parents=True, exist_ok=True)
        CAMPIONI.write_text(json.dumps(dati, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
        sovrapposti = set(dati["A"]["file"]) & set(dati["B"]["file"])
        print(f"✓ campioni estratti in {CAMPIONI.relative_to(ROOT)} — "
              f"A: {len(dati['A']['file'])} · B: {len(dati['B']['file'])} · "
              f"sovrapposizione: {len(sovrapposti)}")
        return 1 if sovrapposti else 0

    if not CAMPIONI.exists():
        print("✗ i campioni non sono stati estratti: `--estrai` prima")
        return 1
    dati = json.loads(CAMPIONI.read_text(encoding="utf-8"))

    if args.scheda:
        stampa_scheda(args.scheda, dati)
        return 0

    if args.kappa:
        voti = json.loads(VOTI.read_text(encoding="utf-8")) if VOTI.exists() else {}
        uscita = 0
        for quale in ("A", "B"):
            print(f"\nκ — campione {quale}  ({dati[quale]['giudice']})")
            suoi = voti.get(quale, {})
            coppie = [(v, giudizio_macchina(f))
                      for f, v in sorted(suoi.items()) if f in dati[quale]["file"]]
            if not coppie:
                print("  🔴 nessun voto: il κ non esiste, e la metrica NON entra")
                print(f"     in CI finche' non esiste. `--scheda {quale}` stampa la scheda.")
                if quale == "A":
                    uscita = 0   # non e' un errore: e' un lavoro che spetta al DM
                continue
            r = kappa(coppie)
            print(f"  n={r['n']}  Po={r['accordo_osservato']}  "
                  f"Pe={r['accordo_atteso_per_caso']}")
            print(f"  **κ = {r['kappa']}** — {r['lettura']}  "
                  f"({'✓ sopra' if r['supera_la_soglia'] else '🔴 SOTTO'} la soglia 0,60)")
            if quale == "A" and not r["supera_la_soglia"]:
                print("  🔴 Il κ che conta e' questo: la metrica si dichiara NON")
                print("     affidabile e non entra in CI. Ha torto la metrica, non il DM.")
        print()
        return uscita

    print(f"A: {len(dati['A']['file'])} documenti · B: {len(dati['B']['file'])} · "
          f"seme {dati['seme']}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
