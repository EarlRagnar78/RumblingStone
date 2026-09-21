#!/usr/bin/env python3
"""punteggio_mqm.py — il punteggio di qualita' editoriale, MQM adattato.

Perche' esiste, e cosa cambia rispetto a `misura_craft`.

  `misura_craft.py` risponde a «questo congegno c'e'?». E' utile e ha trovato
  difetti veri, ma **tutto pesa uguale**: un box di tredici righe e una
  contraddizione col canone valgono un'unita' a testa, non c'e' una soglia di
  accettazione, e il metro d'oro l'ha scritto un valutatore solo.

  Il mestiere ha risposto a questo problema prima di noi. **MQM**
  (Multidimensional Quality Metrics), dal 2024 anche norma **ISO 5060**,
  definisce l'errore come *«mancato rispetto delle specifiche di progetto»* —
  non «brutto», ma **difforme da cio' che era stato dichiarato** — e lo pesa
  con tre severita': **minore 1 · maggiore 5 · critico 25**, dove il critico e'
  **pass/fail assoluto**.

  E' esattamente il problema del repo: una skill dichiara una norma, un
  documento non ce l'ha.

## Le tre cose che questo strumento NON fa, dichiarate

1. **Non giudica la bellezza.** Misura conformita' a specifiche dichiarate. Un
   documento a punteggio pieno puo' essere noioso, e nessuna metrica di questa
   famiglia lo vede. Resta il collaudo al tavolo.
2. **Non scrive rilevatori nuovi.** Riusa quelli che il repo ha gia'
   (`misura_craft`, `validate_prosa`): e' il criterio *una norma, un
   rilevatore*. Le norme registrate senza rilevatore restano **fuori dal
   punteggio**, e `--norme` le elenca invece di farle valere zero.
3. **Non rileva nessun critico, oggi.** Il meccanismo pass/fail e' cablato e
   non scatta mai: i tre casi critici (statblocco inventato, contraddizione con
   `state.md`, EL oltre APL+4) vogliono un confronto col canone che nessuno
   script fa. E' pronto, non attivo, e va detto.

## La soglia nasce dal repo

`--distribuzione` e' il lotto **F1.4** del piano: stampa P10/P25/P50/P75 per
classe. I numeri che finiscono in `specifiche-qualita.yaml` vengono da li',
arrotondati in basso, **perche' il cancello nasca verde e non butti via
niente**. Da li' si stringe per gradi (ADR-0036: si misura il miglioramento,
non lo stato).

## Uso

    python3 scripts/punteggio_mqm.py --distribuzione   # F1.4: da dove nascono le soglie
    python3 scripts/punteggio_mqm.py --soglia          # il cancello (exit 1 sotto soglia)
    python3 scripts/punteggio_mqm.py --norme           # cosa entra nel punteggio e cosa no
    python3 scripts/punteggio_mqm.py --json 'ARC*/ARC07-DEF-4-*.md'

Decisione: ADR-0059.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from fnmatch import fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERRORE: serve pyyaml — pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)

import misura_craft as mc  # noqa: E402
import validate_prosa as vp  # noqa: E402

SPECIFICHE = ROOT / "scripts" / "specifiche-qualita.yaml"

#: Il ponte fra il nome della norma nella specifica e il rilevatore che la
#: misura. ⚠️ Nessuna funzione nuova: solo chiamate a cio' che esiste.
#: Ogni voce e' (chiave nella specifica) -> funzione(testo, percorso) -> conteggio.
def _difetti_box(testo: str, _percorso: Path) -> "dict[str, int]":
    d = mc.difetti_dei_box(testo)
    return {
        "box_oltre_12_righe": d["oltre 12 righe"],
        "box_con_parentesi": d["con parentesi"],
        "box_piu_di_un_nome_proprio": d[">1 nome proprio"],
    }


def _caratteristiche(_testo: str, percorso: Path) -> "dict[str, int]":
    return {"caratteristica_minuscola": len(vp.controlla_caratteristiche(percorso))}


def _prosa(_testo: str, percorso: Path) -> "dict[str, int]":
    """Le sei norme che `validate_prosa` misurava **senza che nessuno le pesasse**.

    🔎 **Il difetto, e perche' era invisibile.** Non mancava il rilevatore:
    `validate_prosa` conta i calchi dall'inglese, la terminologia fuori
    glossario, le maiuscole di enfasi, l'antitesi ripetuta e il trattino come
    respiro **da settembre**. Mancava il **nome**: `controlla()` restituiva
    stringhe gia' formattate, e contarle per norma avrebbe voluto dire
    riconoscere la frase italiana con cui erano scritte. Il ponte non si poteva
    costruire, quindi non c'era.

    Il conto: da **4 norme pesate a 10**, e da **una sola maggiore a due** —
    la terminologia non canonica e' `maggiore`, ed e' la prima norma pesata che
    non sia una prassi da un punto.
    """
    conta: "dict[str, int]" = {k: 0 for k in vp.NORME if k != "caratteristica_minuscola"}
    for chiave, _ in vp.rilievi(percorso):
        if chiave in conta:
            conta[chiave] += 1
    return conta


def _p1(testo: str, _percorso: Path) -> "dict[str, int]":
    """Il read-aloud che presuppone un'azione o un senso del giocatore.

    ⚠️ **Il rilevatore dichiara di non distinguere il dialogo dalla
    narrazione**, quindi i suoi 22 rilievi sul repo sono in maggioranza
    legittimi (lotto 2C). Entra come **minore** apposta: e' un indizio pesato
    poco, non un'accusa. Pesarlo di piu' vorrebbe dire far pagare a un
    documento le battute dei suoi PNG.
    """
    return {"read_aloud_presuppone": len(mc.box_con_p1(testo))}


def _metrature(testo: str, _percorso: Path) -> "dict[str, int]":
    """ADR-0014 §2: la metratura nella voce narrante.

    ⚠️ **La norma gemella NON entra qui, ed e' una scelta.** «Almeno un `c'e'`
    presentativo o una dislocazione a sinistra» (`italiano-nativo.md` §8) e'
    rilevata **a meta'**: la dislocazione vuole un'analisi sintattica che una
    regex non fa. Pesarla produrrebbe penalita' **false** su box che la norma
    la rispettano in un modo che il pattern non vede — 281 rilievi su 477, il
    59%, che e' il numero di una sovrastima e non di un difetto. Si misura con
    `--costrutto-italiano` e non si pesa: contare male in negativo e' peggio
    che non contare.
    """
    return {"metratura_nella_voce_narrante": len(mc.metrature_nei_box(testo))}


RILEVATORI = (_difetti_box, _caratteristiche, _prosa, _p1, _metrature)


def carica_specifiche() -> dict:
    if not SPECIFICHE.exists():
        raise SystemExit(
            f"manca {SPECIFICHE.relative_to(ROOT)}: le soglie sono una decisione "
            "di prodotto e stanno fuori dal codice (ADR-0059)")
    return yaml.safe_load(SPECIFICHE.read_text(encoding="utf-8"))


def classe_di(percorso: Path, spec: dict) -> "str | None":
    """La classe del documento, dal primo modello che lo pesca.

    🔴 **Prima stesura rotta, e l'ha detto la prima esecuzione.** Usava
    `Path.match`, che confronta solo la **coda** del percorso: `0*/**/*.md` non
    pescava niente e **294 documenti su 515 finivano «fuori classe»** — cioe'
    senza soglia, cioe' mai bocciabili. Il confronto giusto e' `fnmatch` sulla
    stringa relativa intera, che e' come lo fanno gli altri strumenti del repo.
    Diciottesimo caso della famiglia: un criterio che non pesca si traveste da
    repo pulito.
    """
    rel = str(percorso.relative_to(ROOT) if ROOT in percorso.parents else percorso)
    for nome, dati in spec["classi"].items():
        if any(fnmatch(rel, m) for m in dati["modelli"]):
            return nome
    return None


def valuta(percorso: Path, spec: dict) -> dict:
    """Il punteggio di un documento, con il dettaglio degli errori."""
    testo = percorso.read_text(encoding="utf-8", errors="replace")
    righe = max(1, testo.count("\n"))
    conteggi: "dict[str, int]" = {}
    for rilevatore in RILEVATORI:
        conteggi.update(rilevatore(testo, percorso))

    penalita = 0
    critici = 0
    dettaglio = []
    for chiave, n in conteggi.items():
        if not n:
            continue
        norma = spec["norme"].get(chiave)
        if norma is None:  # pragma: no cover — il gate lo impedisce
            continue
        sev = spec["severita"][norma["severita"]]
        penalita += n * sev["peso"]
        if sev["pass_fail"]:
            critici += n
        dettaglio.append({"norma": chiave, "severita": norma["severita"],
                          "conteggio": n, "penalita": n * sev["peso"]})

    punteggio = 100.0 * (1 - penalita / righe)
    return {
        "file": str(percorso.relative_to(ROOT) if ROOT in percorso.parents else percorso),
        "classe": classe_di(percorso, spec),
        "righe": righe,
        "penalita": penalita,
        "critici": critici,
        "punteggio": round(punteggio, 2),
        "dettaglio": dettaglio,
    }


def bersagli(spec: dict, modelli: "list[str]") -> "list[Path]":
    """I file da valutare: i modelli dati, o tutto il contenuto di gioco vivo."""
    if modelli:
        return mc.espandi(modelli)
    return [f for f in vp.file_di_gioco()]


def promosso(esito: dict, spec: dict) -> "tuple[bool, str]":
    soglia = spec["soglie"].get(esito["classe"] or "", {})
    if esito["critici"] > soglia.get("critici_ammessi", 0):
        return False, f"{esito['critici']} errore/i critico/i (pass-fail assoluto)"
    minimo = soglia.get("punteggio_minimo")
    if minimo is not None and esito["punteggio"] < minimo:
        return False, f"punteggio {esito['punteggio']} sotto la soglia {minimo}"
    return True, ""


def stampa_norme(spec: dict) -> None:
    print("\nCosa entra nel punteggio\n" + "=" * 58)
    for chiave, n in spec["norme"].items():
        peso = spec["severita"][n["severita"]]["peso"]
        print(f"  {n['severita']:9} (×{peso:2})  {chiave}")
        print(f"  {'':14}  rilevatore: {n['rilevatore']}")
        print(f"  {'':14}  {n['norma']}")
    # 🐛 Il conto era approssimato («~53») perche' contava le righe di TUTTE le
    # tabelle del registro, compresa quella del conto onesto. Le norme vere si
    # contano con lo stesso codice del cancello: una norma, un rilevatore —
    # applicato anche al contare.
    import validate_norme_editoriali as vne  # noqa: PLC0415
    registro = ROOT / "skills" / "REGISTRO-NORME-EDITORIALI.md"
    if registro.exists():
        conto = vne.conto_vero(registro.read_text(encoding="utf-8"))
        tot = sum(conto.values())
        print(f"\n⚠️  Il registro elenca {tot} norme; qui ne entrano "
              f"{len(spec['norme'])}.")
        print("   Le altre non hanno un rilevatore, e valere zero sarebbe una bugia.")
        # 🔎 «Le altre» era una frase, e una frase non dice **cosa manca**.
        # Dal 2026-09-21 ogni norma scoperta porta il suo stato di superficie,
        # cosi' la riga smette di essere una scusa e diventa un elenco di lavoro
        # con il suo prerequisito accanto (ADR-0062).
        import superficie_norme as sn  # noqa: PLC0415
        conta: "dict[str, int]" = {}
        for r in sn.misura():
            conta[r["stato"]] = conta.get(r["stato"], 0) + 1
        print("\n   Delle scoperte, cosa manca davvero — "
              "`python3 scripts/superficie_norme.py` per il dettaglio:")
        for stato, n in sorted(conta.items()):
            print(f"     {sn.ETICHETTA[stato]:26} {n}")
        print("   🔎 Per otto su nove **non manca il codice**: manca il dato, la")
        print("      convenzione di marcatura, o il fatto non sta nel testo.")
        pesi = [spec["severita"][n["severita"]]["peso"] for n in spec["norme"].values()]
        print(f"   🔎 E pesano poco: {sum(1 for p in pesi if p == 1)} minori su "
              f"{len(pesi)}. Il punteggio di oggi misura il bordo, non il centro "
              "— vedi la tabella incrociata del registro (lotto F1.2).")
    print("\n⛔ Nessun rilevatore di severita' «critico» esiste oggi: il pass/fail")
    print("   e' cablato e non scatta mai. Pronto, non attivo.\n")


def stampa_distribuzione(esiti: "list[dict]") -> None:
    """Lotto F1.4: da dove nascono le soglie."""
    print("\nF1.4 — DISTRIBUZIONE DEL PUNTEGGIO PER CLASSE\n" + "=" * 62)
    print("La soglia nasce dal valore che il repo ha gia', arrotondato in basso,")
    print("cosi' il cancello nasce verde. Poi si stringe per gradi (ADR-0036).\n")
    print(f"{'classe':14}{'n':>5}{'P10':>9}{'P25':>9}{'P50':>9}{'P75':>9}{'min':>9}")
    per_classe: "dict[str, list[float]]" = {}
    for e in esiti:
        per_classe.setdefault(e["classe"] or "(fuori classe)", []).append(e["punteggio"])
    for classe, v in sorted(per_classe.items()):
        v.sort()
        def q(p: float) -> float:
            if len(v) == 1:
                return v[0]
            return statistics.quantiles(v, n=100, method="inclusive")[int(p) - 1]
        print(f"{classe:14}{len(v):>5}{q(10):>9.2f}{q(25):>9.2f}"
              f"{q(50):>9.2f}{q(75):>9.2f}{min(v):>9.2f}")
    print()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("modelli", nargs="*",
                    help="modelli glob; se assenti, tutto il contenuto di gioco vivo")
    ap.add_argument("--soglia", action="store_true",
                    help="cancello: esce 1 se un documento e' sotto la soglia della sua classe")
    ap.add_argument("--distribuzione", action="store_true",
                    help="P10/P25/P50/P75 per classe — e' da qui che nascono le soglie (F1.4)")
    ap.add_argument("--norme", action="store_true",
                    help="cosa entra nel punteggio, con la severita' e il rilevatore")
    ap.add_argument("--json", action="store_true", help="il rapporto in JSON")
    args = ap.parse_args(argv)

    spec = carica_specifiche()
    if args.norme:
        stampa_norme(spec)
        return 0

    esiti = [valuta(f, spec) for f in bersagli(spec, args.modelli) if f.suffix == ".md"]

    if args.json:
        print(json.dumps({"tool": "punteggio_mqm", "versione_specifiche": spec["versione"],
                          "documenti": esiti}, indent=2, ensure_ascii=False))
        return 0

    if args.distribuzione:
        stampa_distribuzione(esiti)
        return 0

    bocciati = []
    for e in sorted(esiti, key=lambda x: x["punteggio"]):
        ok, perche = promosso(e, spec)
        if not ok:
            bocciati.append((e, perche))

    if args.soglia:
        if not bocciati:
            print(f"✓ punteggio_mqm: {len(esiti)} documenti, nessuno sotto la soglia "
                  f"della sua classe, zero critici")
            return 0
        print(f"✗ punteggio_mqm: {len(bocciati)} documenti su {len(esiti)} sotto soglia")
        for e, perche in bocciati:
            print(f"  - {e['file']} [{e['classe']}] — {perche}")
            for d in e["dettaglio"]:
                print(f"      {d['severita']:9} ×{d['conteggio']:<3} {d['norma']}")
        return 1

    for e in sorted(esiti, key=lambda x: x["punteggio"])[:25]:
        marca = "✓" if promosso(e, spec)[0] else "✗"
        print(f"{marca} {e['punteggio']:7.2f}  [{e['classe'] or '—':10}] {e['file']}")
    print(f"\n({len(esiti)} documenti; i 25 col punteggio piu' basso)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
