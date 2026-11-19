#!/usr/bin/env python3
"""misura_ordine.py — l'ordine delle sezioni di un booklet di serata, misurato.

Domanda di Jfs del 2026-11-19: l'ordine in cui compaiono le sezioni del
booklet della serata segue gli standard editoriali, o al tavolo si perde
l'informazione e si va a braccio?

Il PDF dà le sezioni e le loro pagine (i segnalibri). Il **ruolo** di ogni
sezione (avvio, preparazione, gioco, sintesi, fuori serata, riferimento) è
un'etichetta scritta a mano in `ruoli-<nome>.json`: è il giudizio di chi
legge, dichiarato e rivedibile, non una misura. Da lì le regole sono
deterministiche:

| regola | fonte | misura |
|---|---|---|
| R1 avvio in testa | Paizo «Adventure Summary» prima delle Part; EN World, «the scheme up front» | pagine d'avvio prima del primo gioco / pagine d'avvio |
| R2 preparazione prima del gioco | Shea, *Lazy DM* (passo 1 «Review the Characters», passo 6 PNG); ADR-0013 (regia prima dei master) | pagine di preparazione prima del primo gioco / pagine di preparazione |
| R3 ordine di gioco = ordine di pagina | ADR-0013 («ordine di gioco»); Alexander, *The Art of the Key* («nell'ordine in cui serve») | coppie di scene consecutive con la pagina che scende |
| R4 sintesi prima del dettaglio | Paizo (sintesi, poi le parti); Alexander (riassunto + pagina) | sintesi stampate prima del dettaglio che riassumono / sintesi |
| R6 niente fuori serata fra le scene | Lynch (scrittura economica); ADR-0070 | pagine fuori serata fra la prima e l'ultima pagina di gioco |
| R7 riferimento una volta sola, in fondo | RHoD (appendice delle schede); ADR-0070 («una pagina si stampa una volta») | sezioni di riferimento stampate due volte; riferimento prima della fine del gioco |
| R8 la guida ai capitoli dice il vero | indice generato, mai scritto a mano (lo standard di ogni impaginatore) | righe «N · …» stampate prima dei capitoli che non corrispondono al capitolo N |

R5 (tutto dell'incontro sulla doppia pagina: Milton, «control panel»; il
formato Delve) non si rifà qui: lo misurano `misura_distanza_pagine.py` e
`misura_standard_tavolo.py`.

Per il volume d'arco (una regola con `"parte": true` apre ogni parte) valgono
in più V1 (il quadro del volume prima della Parte I), V2 (l'indice in due
pagine) e V3 (nessuna parte senza gioco fra due parti giocate), e le regole sopra si contano parte per parte: vedi `misura_volume`.

Uso: python3 scripts/misura_ordine.py PDF RUOLI.json [--json]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RUOLI = ("avvio", "preparazione", "gioco", "sintesi", "fuori-serata", "riferimento", "regole")


def sezioni(pdf: Path, livello: int = 3) -> list[dict]:
    """Le voci dei segnalibri fino a `livello`. Dal 2026-11-19 i segnalibri
    sono annidati (capitolo 1, sezione 2, sottosezione 3: ADR-0145); prima
    erano piatti e bastava il 2."""
    import pymupdf
    doc = pymupdf.open(pdf)
    toc = [(l, t.strip(), p) for l, t, p in doc.get_toc() if l <= livello]
    out = []
    for i, (l, t, p) in enumerate(toc):
        fine = next((q for l2, _, q in toc[i + 1:] if l2 <= l), len(doc) + 1) - 1
        out.append({"livello": l, "titolo": t, "da": p, "a": max(p, fine)})
    return out


def etichetta(sez: list[dict], regole: list[dict]) -> list[dict]:
    """La prima regola il cui `titolo` (regex) combacia dà il ruolo; il resto
    eredita il ruolo del capitolo che lo contiene. Un capitolo è una regola
    con `"capitolo": true`: nei PDF di prima del 2026-11-19 i segnalibri
    erano piatti e il livello non bastava a dire dove comincia un capitolo;
    la regola resta, così si misurano anche quelli."""
    padre = None
    sopra: dict[int, str] = {}   # livello → ruolo dell'ultima sezione con una regola
    for s in sez:
        ruolo = next((r for r in regole if re.search(r["titolo"], s["titolo"])), None)
        if ruolo and ruolo.get("capitolo"):
            padre = ruolo
            sopra = {}
        scelto = ruolo or padre
        s["ruolo"] = scelto["ruolo"] if scelto else "?"
        # Una sottosezione senza regola eredita dalla sezione sopra di lei
        # che ne ha una: «La parte in trenta secondi» sotto «§0 — QUICKSTART».
        su = [sopra[l] for l in sorted(sopra) if l < s["livello"]]
        if not ruolo and su:
            s["ruolo"] = su[-1]
        sopra = {l: r for l, r in sopra.items() if l < s["livello"]}
        if ruolo and not ruolo.get("capitolo"):
            sopra[s["livello"]] = ruolo["ruolo"]
        if ruolo and ruolo.get("parte"):
            s["parte"] = True
        for k in ("scena", "riassume", "doppione_di"):
            if scelto and k in scelto and scelto is ruolo:
                s[k] = scelto[k]
    return sez


def pagine(sez, ruolo):
    """Le pagine di un ruolo, contate sulle foglie (una pagina divisa fra due
    sezioni conta per entrambe: è la pagina che il DM deve trovare)."""
    foglie = [s for s in sez if not any(t is not s and t["da"] >= s["da"] and t["a"] <= s["a"]
                                           and t["livello"] > s["livello"] for t in sez)]
    return sorted({p for s in foglie if s["ruolo"] == ruolo for p in range(s["da"], s["a"] + 1)})


def misura(sez: list[dict]) -> dict:
    gioco = pagine(sez, "gioco")
    primo, ultimo = (gioco[0], gioco[-1]) if gioco else (0, 0)
    avvio, prep = pagine(sez, "avvio"), pagine(sez, "preparazione")
    scene = [s for s in sez if "scena" in s]
    scene_ord = sorted(scene, key=lambda s: s["scena"])
    salti = [(a["titolo"], b["titolo"]) for a, b in zip(scene_ord, scene_ord[1:]) if b["da"] < a["da"]]
    sintesi = [s for s in sez if "riassume" in s]
    dopo = []
    for s in sintesi:
        dett = [t for t in sez if re.search(s["riassume"], t["titolo"]) and t is not s]
        if dett and s["da"] > min(t["da"] for t in dett):
            dopo.append((s["titolo"], s["da"], min(t["da"] for t in dett)))
    fuori = [p for p in pagine(sez, "fuori-serata") if primo < p < ultimo]
    rif_presto = [p for p in pagine(sez, "riferimento") if p < ultimo]
    doppioni = [(s["titolo"], s["da"]) for s in sez if "doppione_di" in s]
    # Si conta il blocco, non le sue sezioni: i segnalibri sono piatti, e
    # «XV · Durik» con le sue quattro sezioni fuori posto è un difetto, non
    # cinque. Un blocco è una fila di sezioni di preparazione dopo il gioco.
    prep_dopo, prima_era = [], False
    for x in sez:
        fuori_posto = bool(gioco) and x["ruolo"] == "preparazione" and x["da"] > primo and x["livello"] <= 2
        if fuori_posto and not prima_era:
            prep_dopo.append((x["titolo"], x["da"]))
        if x["livello"] <= 2:
            prima_era = fuori_posto
    return {
        "pagine_di_gioco": f"{primo}-{ultimo}",
        "R1_avvio_in_testa": f"{sum(p < primo for p in avvio)}/{len(avvio)}",
        "R2_preparazione_prima": f"{sum(p < primo for p in prep)}/{len(prep)}",
        "R2_dopo": prep_dopo,
        "R3_scene_fuori_ordine": salti,
        "R4_sintesi_dopo_il_dettaglio": f"{len(dopo)}/{len(sintesi)}",
        "R4_dettaglio": dopo,
        "R6_pagine_fuori_serata_fra_le_scene": len(fuori),
        "R6_pagine": fuori,
        "R7_doppioni": doppioni,
        "R7_riferimento_prima_della_fine_del_gioco": len(rif_presto),
    }


_ROMANO = re.compile(r"^([IVXL]+) · (.+)$")


def _parole(t: str, n: int = 2) -> list[str]:
    return re.findall(r"\w+", t.lower())[:n]


def guida_sbagliata(righe: list[str], titoli: list[str]) -> list[str]:
    """R8: le righe della guida ai capitoli («V · La cassetta del DM») che non
    corrispondono al capitolo con quel numero. Si confrontano le prime due
    parole: «XII · Durik» e «XII · Durik, il compagno di Hella» vanno d'accordo."""
    capitoli = {m.group(1): m.group(2) for t in titoli if (m := _ROMANO.match(t.strip()))}
    sbagliate = []
    for r in righe:
        m = _ROMANO.match(r.strip())
        if not m:
            continue
        vero = capitoli.get(m.group(1))
        n = min(2, len(_parole(m.group(2))))
        if vero is None or _parole(vero, n) != _parole(m.group(2), n):
            sbagliate.append(r.strip())
    return sbagliate


def guida_del_pdf(pdf: Path) -> tuple[list[str], list[str]]:
    """Le righe «N · …» stampate prima del primo capitolo numerato, e i titoli
    dei capitoli numerati dai segnalibri."""
    import pymupdf
    doc = pymupdf.open(pdf)
    titoli = [t for _, t, _ in doc.get_toc() if _ROMANO.match(t.strip())]
    primo = min((p for _, t, p in doc.get_toc() if _ROMANO.match(t.strip())), default=1)
    righe = [r for n in range(primo - 1) for r in doc[n].get_text().splitlines() if _ROMANO.match(r.strip())]
    return righe, titoli


def difetti(m: dict) -> int:
    """Quanti difetti di struttura: sezioni di preparazione dopo il primo
    gioco, scene fuori ordine, sintesi dopo il dettaglio, pagine fuori serata
    fra le scene, doppioni e pagine di riferimento prima della fine del gioco."""
    return (len(m["R2_dopo"]) + len(m["R3_scene_fuori_ordine"]) + len(m["R4_dettaglio"])
            + m["R6_pagine_fuori_serata_fra_le_scene"] + len(m["R7_doppioni"])
            + m["R7_riferimento_prima_della_fine_del_gioco"] + len(m.get("R8_guida_sbagliata", [])))


_PUNTINI = re.compile(r"(?:\. ){4,}")


def pagine_di_indice(testi: list[str]) -> int:
    """Le pagine dell'indice stampato: quelle con le righe a puntini."""
    return sum(1 for t in testi if _PUNTINI.search(t))


def misura_volume(sez: list[dict], pagine_indice: int) -> dict:
    """Il volume d'arco, nello schema degli AP (Paizo, Red Hand of Doom):

    V1 il quadro del volume (antefatto, sinossi, come si usa) prima della
    Parte I: sezioni d'avvio prima della prima parte; 0 è un difetto.
    V2 l'indice si legge in una o due pagine (quello di un AP Paizo è una):
    pagine oltre la seconda.
    Poi ogni parte, dalla sua apertura alla successiva, con le regole della
    serata (R2-R7): ogni parte di un AP è una serata o più."""
    inizi = [i for i, x in enumerate(sez) if x.get("parte")]
    primo = sez[inizi[0]]["da"] if inizi else 0
    quadro = sum(1 for x in sez[:inizi[0] if inizi else 0] if x["ruolo"] == "avvio" and x["da"] <= primo)
    parti = {}
    for k, i in enumerate(inizi):
        fine = inizi[k + 1] if k + 1 < len(inizi) else len(sez)
        # Il titolo della parte è un segnalibro di una pagina allo stesso
        # livello delle sezioni: conta come apertura, non come gioco.
        pezzo = [dict(sez[i], ruolo="avvio")] + sez[i + 1:fine]
        parti[sez[i]["titolo"]] = misura(pezzo)
    giocate = [t for t, mp in parti.items() if mp["pagine_di_gioco"] != "0-0"]
    fra = [t for t, mp in parti.items() if mp["pagine_di_gioco"] == "0-0" and giocate
           and list(parti).index(giocate[0]) < list(parti).index(t) < list(parti).index(giocate[-1])]
    return {"V1_quadro_del_volume": quadro,
            "V2_pagine_di_indice_oltre_due": max(0, pagine_indice - 2),
            "V3_parti_senza_gioco_fra_le_parti": fra,
            "parti": parti}


def difetti_volume(m: dict) -> int:
    return ((m["V1_quadro_del_volume"] == 0) + m["V2_pagine_di_indice_oltre_due"]
            + len(m.get("V3_parti_senza_gioco_fra_le_parti", []))
            + sum(difetti(p) for p in m["parti"].values()))


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 epilog="ADR-0145. Regole e fonti nella docstring del modulo.")
    ap.add_argument("pdf", type=Path, help="il PDF composto del booklet")
    ap.add_argument("ruoli", type=Path, help="il file JSON dei ruoli delle sezioni")
    ap.add_argument("--json", action="store_true", help="misure e sezioni in JSON")
    a = ap.parse_args(argv)
    pdf, ruoli = a.pdf, a.ruoli
    sez = etichetta(sezioni(pdf), json.loads(ruoli.read_text(encoding="utf-8"))["regole"])
    if any(x.get("parte") for x in sez):
        import pymupdf
        doc = pymupdf.open(pdf)
        primo = min(x["da"] for x in sez if x.get("parte"))
        m = misura_volume(sez, pagine_di_indice([doc[n].get_text() for n in range(primo - 1)]))
        if "--json" in argv:
            print(json.dumps({"misura": m, "sezioni": sez}, ensure_ascii=False, indent=1))
            return 0
        for x in sez:
            print(f"{'  ' * (x['livello'] - 1)}{x['ruolo']:>13}  {x['da']:>3}-{x['a']:<3} {x['titolo'][:70]}")
        print()
        print(f"V1_quadro_del_volume: {m['V1_quadro_del_volume']}")
        print(f"V2_pagine_di_indice_oltre_due: {m['V2_pagine_di_indice_oltre_due']}")
        print(f"V3_parti_senza_gioco_fra_le_parti: {m['V3_parti_senza_gioco_fra_le_parti']}")
        for t, mp in m["parti"].items():
            print(f"\n{t} — difetti {difetti(mp)}")
            for k, v in mp.items():
                if v not in ([], 0) and not str(v).startswith("0/"):
                    print(f"  {k}: {v}")
        print(f"\ndifetti di struttura: {difetti_volume(m)}")
        return 0
    m = misura(sez)
    m["R8_guida_sbagliata"] = guida_sbagliata(*guida_del_pdf(pdf))
    if "--json" in argv:
        print(json.dumps({"misura": m, "sezioni": sez}, ensure_ascii=False, indent=1))
    else:
        for s in sez:
            print(f"{'  ' * (s['livello'] - 1)}{s['ruolo']:>13}  {s['da']:>3}-{s['a']:<3} {s['titolo'][:70]}")
        print()
        for k, v in m.items():
            print(f"{k}: {v}")
        print(f"difetti di struttura: {difetti(m)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
