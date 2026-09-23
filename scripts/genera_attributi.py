#!/usr/bin/env python3
"""genera_attributi.py — le caratteristiche dei PNG, VINCOLATE prima che generate.

## Perche' esiste

`RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI` ha misurato il muro: solo **14
statblocchi su 110** dichiarano `attributi`, e senza For/Des/Cos non si ricava
nessuna delle identita' profonde — i pf dai DV e dalla Costituzione, i TS dalla
progressione di classe, l'attacco da BAB + modificatore + taglia. Quelle tre
identita' sono la strada verso il **primo `critico`** del punteggio, che il
κ 0,0 di F3.3 dice mancare.

Il DM, il 2026-09-21: *«generare coerentemente gli statblock nei 96 che non li
hanno usando generatori random che utilizzano le regole di D&D 3.5 e/o PF1e o
gli stat array elite e standard del manuale del DM (usa le regole deterministiche
piu' affidabili con una percentuale di random in modo che non siano tutti
uguali)»*.

## Il principio: prima si copia, poi si legge, poi si sceglie, e il caso per ultimo

Cinque strati, in quest'ordine. Ogni caratteristica scende di strato solo se il
precedente non la determina. Misurato sui 93 file, 2026-09-23 (Karruk e'
uscito dalla marca: le sue caratteristiche ora sono del DM):

| strato | da dove viene | file |
|---|---|---:|
| **0a · copiato** | la sestina che la **scheda stessa** scrive nella prosa, in inglese o in italiano | **41** |
| **0b · trascritto** | la fonte citata in `Bestiario/pregen-pcgen/` (export PCGen, SRD) | **37** |
| **1 · letto** | la Destrezza scritta in `ca-dettaglio` (`+3 Dex`) | } sugli |
| **2 · derivato** | Des dalla CA di contatto e dall'iniziativa; Cos da `pf` e `pf-dado`; For da BAB e lotta | } altri |
| **2-quinquies · tetto** | un TS scritto **sotto** l'atteso abbassa Cos, Des o Sag; l'iniziativa senza talenti ammette due Des | } 15 |
| **3 · scelto** | array del **Manuale del DM 3.5**, per ruolo, con taglia e razza SRD | **15** |

🔴 **Gli strati 0a e 0b la prima stesura non li aveva.** Generava numeri per
42 file che citano la loro fonte, e per 27 che li scrivevano due righe sotto il
blocco. Il conto di ADR-0064 («55 scelti») era sbagliato per questo: i
file davvero scelti sono **18**.

🔴 **Lo strato 3 e' una scelta, non una misura**, e per questo **ogni blocco
scritto porta `[INFERRED — needs DM confirmation]`**, con la sua provenienza e
le divergenze trovate: e' la regola 5 di `AGENTS.md`. Il confine con ADR-0033
lo discutono ADR-0064 e ADR-0065.

## Quanto sbaglia lo strato 3, misurato

Dove la risposta vera c'e', `--taratura` genera **come se non ci fosse** e
confronta, su due banchi separati:

| banco | file | errore medio | entro ±1 di mod |
|---|---:|---:|---:|
| fonti citate — **in campione** (le regole sono state scelte guardandole) | 37 | 1,50 | 85% |
| sestine delle schede — **fuori campione** (trovate dopo) | 41 | **1,54** | 83% |

Prima dello strato 2-quinquies erano 1,63 e 1,84. ⚠️ Il banco fuori campione non e'
piu' del tutto fuori: le tre sestine nuove sono dell'ogre micelio, dell'ogre
frantumapietra e di Zin'thara (Karruk ne e' uscito), e l'ogre frantumapietra
era uno degli otto scarti da cui il tetto e' nato. Sulle altre 38 le regole
non sono state scelte.

Il secondo numero e' quello che conta: dice quanto il generatore vale su un
file che non ha visto. Le mentali (Int e Car sopra i 2 punti) restano le piu'
lontane, perche' il ruolo dice come un PNG combatte e non quanto e'
intelligente.

## Gli array, e quando si usa quale

Manuale del DM 3.5, PNG, tramite `dmcore.tabelle`:

* **elite** — `15 14 13 12 10 8` — per le **creature** e per i ruoli di
  `T.RUOLI_ELITE` (boss, elite, leader, caster…);
* **standard** — `13 12 11 10 9 8` — per gli altri PNG con livelli di classe.

Poi l'**avanzamento**, sul GS come surrogato dei DV (dichiarato: i DV totali
stanno nel `tipo` solo nell'8% dei file); la **taglia** SRD per le creature
(*Improving Monsters*: Large For +8, Des −2, Cos +4) e per i PNG di razza
mostruosa; i **modificatori razziali** SRD per i PNG di razza comune. Non morti:
**Cos —**. Scheletri e zombi: **Int —, Sag 10, Car 1**.

## Il caso: quanto, e perche' a seme fisso

Il DM ha chiesto *«una percentuale di random perche' non siano tutti uguali»*.
La variazione e' **±1 su due caratteristiche secondarie, a somma zero**. Non
tocca mai la caratteristica principale del ruolo, e non tocca lo strato 0.

🔴 **Il seme e' il nome del file**, non l'orologio. Due esecuzioni sullo stesso
repo danno gli **stessi** numeri: un generatore che a ogni giro cambia il
canone non e' uno strumento, e' un dado che scrive sui file.

## Cosa ha trovato strada facendo

🐛 **`pf-dado` in 20 statblocchi su 95 e' il danno di un'arma**, non i dadi
vita: `1d8+7` accanto a «hp 93 (12 HD)». Il controllo e' `pf_dado_sospetto`,
e lo usa anche `validate_bestiario --rules`.

🐛 **Una parentesi dopo il punteggio nascondeva la sestina** (`_NOTA`):
«For 25 (21 base +4 innesto)». Tre schede finivano all'array, e Zin'thara, una
maga con Int 22, ne usciva con Car 21.

🐛 **Il giro circolare con `pf-dado`**: dove la Cos era generata,
`conformita_statblocchi` ricavava il bonus dei dadi vita dai pf supponendo la
media, e `cos_da_pf` ricavava la Cos da quel bonus. Il generatore confermava
se stesso: Khorn scrive «8d10+24, Cos 16» e ne usciva con Cos 18. Ora il bonus
viene prima dalla Tempra, che e' un'identita' esatta.

## Cosa NON fa, dichiarato

* **Non tocca i file con `attributi` scritti a mano**, ne' i `[POINTER]`, che
  per progetto rimandano al file d'arco (ADR-0021). `--rigenera` riscrive
  **solo** i blocchi che portano la sua marca.
* **Non legge il PDF** del death tyrant: la sola stdlib non lo apre, e `--check`
  in CI deve poter rigenerare tutto. Quel file resta generato, e lo dice.
* **Non verifica** che pf, TS e attacco tornino con le caratteristiche: lo fa
  `conformita_statblocchi.py`, che queste caratteristiche rendono possibile.

## Uso

    python3 scripts/genera_attributi.py              # proposta a video, non scrive
    python3 scripts/genera_attributi.py --scrivi     # applica, marcando [INFERRED]
    python3 scripts/genera_attributi.py --rigenera   # riscrive i soli blocchi suoi
    python3 scripts/genera_attributi.py --taratura   # errore dello strato 3 sulle fonti
    python3 scripts/genera_attributi.py --check      # esce 1 se un blocco generato non torna
                                                     # con la regola, o e' duplicato
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

# 🔴 Le tabelle SRD stanno in `dmcore/tabelle.py`, e `genera_creatura` le usa
# gia'. La prima stesura di questo script le aveva **ricopiate**, e ricopiando
# aveva sbagliato due righe: il ranger a d10 (nel 3.5 e' d8) e «minuta» e
# «minuscola» scambiate. Una tabella, un posto.
from dmcore import tabelle as T  # noqa: E402,F401


#: Il lettore delle schede sta in `dmcore.lettura_creatura` e la scelta delle
#: caratteristiche in `dmcore.caratteristiche` (ADR-0066). Qui restano la
#: proposta, la scrittura nel Bestiario, `--check` e `--taratura`, e si importa
#: solo quello che usano: chi cerca una funzione del lettore o della scelta la
#: trova in `dmcore`, non qui.
from dmcore.lettura_creatura import (  # noqa: E402
    BLOCCO, CODA_ARRAY, CODA_FONTE, CODA_SCHEDA, MARCA, ORDINE, dalla_scheda,
)
from dmcore.caratteristiche import dalla_fonte, genera, mod, riga_attributi  # noqa: E402


RIGA_MARCA = re.compile("^" + re.escape(MARCA) + ".*$", re.M)


def statblocchi(rigenera: bool = False) -> "list[Path]":
    """I file da generare; con `rigenera`, anche quelli gia' generati da qui."""
    fuori = []
    for p in sorted(ROOT.glob("Bestiario/*/*-cr*.md")) + sorted(ROOT.glob("Bestiario/*/*/*-cr*.md")):
        t = p.read_text(encoding="utf-8", errors="replace")
        if "[POINTER" in t or "[RIMANDO]" in t:
            continue
        if not BLOCCO.search(t):
            continue
        if re.search(r"^attributi:", t, re.M) and not (rigenera and MARCA in t):
            continue
        fuori.append(p)
    return fuori


def proponi(rigenera: bool = False) -> "list[dict]":
    fuori = []
    for p in statblocchi(rigenera):
        t = p.read_text(encoding="utf-8", errors="replace")
        ruolo = re.search(r"\*\*Role\*\*:\s*([^\|\n]+)", t, re.I)
        gs = re.search(r"^gs:\s*([\d.,]+)", t, re.M)
        if not (ruolo and gs):
            continue
        v, note = genera(p.name, ruolo.group(1).strip(),
                         float(gs.group(1).replace(",", ".")), t)
        scritta = re.search(r"^attributi:.*$", t, re.M)
        fuori.append({"file": p, "ruolo": ruolo.group(1).strip(),
                      "attributi": v, "riga": riga_attributi(v), "note": note,
                      "marca": MARCA + (CODA_SCHEDA if note[0].startswith("letta dalla riga")
                                        else CODA_FONTE if note[0].startswith("trascritt")
                                        else CODA_ARRAY)
                               + "".join(" " + n for n in note if n.startswith("⚠")),
                      "scritta": scritta.group(0) if scritta else None})
    return fuori


def applica(prop: "list[dict]", rigenera: bool = False) -> int:
    """Scrive i blocchi. Idempotente: un secondo giro non cambia un byte.

    Senza `rigenera` salta i file che hanno gia' `attributi`; con `rigenera`
    riscrive **solo** quelli che portano la marca di questo script, mai un
    blocco scritto a mano.
    """
    scritti = 0
    for r in prop:
        t = r["file"].read_text(encoding="utf-8", errors="replace")
        if r["scritta"]:
            if not (rigenera and MARCA in t):
                continue
            nuovo_t = re.sub(r"^attributi:.*$", lambda _: r["riga"], t, count=1, flags=re.M)
            nuovo_t = RIGA_MARCA.sub(lambda _: r["marca"], nuovo_t, count=1)
            if nuovo_t != t:
                r["file"].write_text(nuovo_t, encoding="utf-8")
                scritti += 1
            continue
        m = BLOCCO.search(t)
        corpo = m.group(1)
        # dopo `ts:` se c'e', altrimenti in coda al blocco: e' il posto in cui
        # i 14 file che gia' l'hanno lo scrivono.
        if re.search(r"^ts:.*$", corpo, re.M):
            nuovo = re.sub(r"^(ts:.*)$", lambda x: x.group(1) + "\n" + r["riga"],
                           corpo, count=1, flags=re.M)
        else:
            nuovo = corpo.rstrip("\n") + "\n" + r["riga"] + "\n"
        t = t[:m.start(1)] + nuovo + t[m.end(1):]
        # la marca va subito sotto il blocco chiuso: sempre, e sempre li'
        fine = t.index("```", m.start(1) + len(nuovo)) + 3
        t = t[:fine] + "\n\n" + r["marca"] + t[fine:]
        r["file"].write_text(t, encoding="utf-8")
        scritti += 1
    print(f"✓ scritti {scritti} blocchi `attributi`, tutti marcati [INFERRED]")
    return 0


VALORE = re.compile(r"(For|Des|Cos|Int|Sag|Car) (\d+|—)")


def controlla() -> "list[str]":
    """Tre promesse, e il cancello le verifica tutte e tre sui file veri."""
    problemi = []
    for r in proponi(rigenera=True):
        nome = r["file"].name
        if r["scritta"] and r["scritta"] != r["riga"]:
            problemi.append(f"{nome}: scritto «{r['scritta']}», la regola da' «{r['riga']}»")
        if r["scritta"] and r["marca"] not in r["file"].read_text(encoding="utf-8"):
            problemi.append(f"{nome}: la marca non dice piu' da dove vengono i numeri")
        for c, v in VALORE.findall(r["riga"]):
            if v != "—" and not 1 <= int(v) <= 45:
                problemi.append(f"{nome}: {c} {v} fuori da 1–45")
    for p in ROOT.glob("Bestiario/**/*-cr*.md"):
        t = p.read_text(encoding="utf-8", errors="replace")
        if len(RIGA_MARCA.findall(t)) > 1 or len(re.findall(r"^attributi:", t, re.M)) > 1:
            problemi.append(f"{p.name}: blocco o marca duplicati — la scrittura non e' idempotente")
    return problemi


def taratura(insieme: str = "fonti") -> dict:
    """Quanto sbaglia lo strato 3 dove la risposta vera c'e'.

    Si genera **come se la risposta non ci fosse** e si confronta. Due banchi:

    * ``fonti`` — le 39 sestine trascritte da `pregen-pcgen/`. **In-campione**:
      e' su questi file che si e' visto che taglia e razza servivano;
    * ``schede`` — le 27 sestine che le schede scrivono nella loro prosa,
      trovate **dopo** aver fissato le regole. **Fuori campione**: e' il
      numero che dice quanto il generatore vale su un file che non ha visto.
    """
    coppie = []
    for r in proponi(rigenera=True):
        t = r["file"].read_text(encoding="utf-8", errors="replace")
        vera = dalla_scheda(t) if insieme == "schede" else (
            None if dalla_scheda(t) else dalla_fonte(r["file"].name, t))
        if not vera:
            continue
        gs = float(re.search(r"^gs:\s*([\d.,]+)", t, re.M).group(1).replace(",", "."))
        gen, _ = genera(r["file"].name, r["ruolo"], gs, t, usa_fonte=False)
        coppie.append((r["file"].name, vera[0], gen))
    per_car, tutti, mods = {}, [], []
    for _, v, g in coppie:
        for c in ORDINE:
            if isinstance(v[c], int) and isinstance(g[c], int):
                e = abs(v[c] - g[c])
                per_car.setdefault(c, []).append(e)
                tutti.append(e)
                mods.append(abs(mod(v[c]) - mod(g[c])))
    media = lambda xs: round(sum(xs) / len(xs), 2) if xs else 0.0  # noqa: E731
    return {"insieme": insieme, "file": len(coppie), "mae": media(tutti), "mae_mod": media(mods),
            "entro_1_mod": round(sum(e <= 1 for e in mods) / len(mods), 2) if mods else 0.0,
            "per_caratteristica": {c: media(per_car.get(c, [])) for c in ORDINE},
            "coppie": coppie}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--scrivi", action="store_true", help="applica ai file")
    ap.add_argument("--rigenera", action="store_true",
                    help="riscrive i soli blocchi marcati da questo script")
    ap.add_argument("--check", action="store_true",
                    help="esce 1 se un blocco generato non e' riproducibile")
    ap.add_argument("--taratura", action="store_true",
                    help="errore dello strato 3 contro le fonti trascrivibili")
    args = ap.parse_args(argv)
    if args.taratura:
        for insieme, etichetta in (("fonti", "fonti citate, IN-CAMPIONE"),
                                   ("schede", "sestine scritte nelle schede, FUORI CAMPIONE")):
            m = taratura(insieme)
            print(f"TARATURA dello strato 3 su {m['file']} file — {etichetta}")
            print(f"  errore medio: {m['mae']} sul punteggio, {m['mae_mod']} sul modificatore; "
                  f"entro ±1 di modificatore: {m['entro_1_mod']:.0%}")
            print("  per caratteristica: " + "  ".join(
                f"{c} {e}" for c, e in m["per_caratteristica"].items()))
        return 0
    if args.check:
        problemi = controlla()
        for x in problemi:
            print(f"✗ {x}")
        if problemi:
            return 1
        gen = sum(1 for r in proponi(rigenera=True) if r["scritta"])
        print(f"✓ genera_attributi: {gen} blocchi generati, tutti riproducibili "
              f"e nei limiti; {len(proponi())} ancora da generare")
        return 0
    if args.rigenera:
        return applica(proponi(rigenera=True), rigenera=True)
    prop = proponi()
    if args.scrivi:
        return applica(prop)
    print(f"\nPROPOSTA — {len(prop)} statblocchi senza `attributi`\n" + "=" * 70)
    for r in prop[:12]:
        print(f"\n  {r['file'].name}  [{r['ruolo']}]")
        print(f"    {r['riga']}")
        for n in r["note"]:
            print(f"      · {n}")
    if len(prop) > 12:
        print(f"\n  … e altri {len(prop) - 12}. `--scrivi` li applica.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
