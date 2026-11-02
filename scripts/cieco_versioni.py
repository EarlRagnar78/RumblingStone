#!/usr/bin/env python3
"""cieco_versioni.py — il confronto cieco fra due versioni degli stessi box.

Le misure deterministiche dicono se un testo ha **meno difetti**; nessuna dice
se è **migliore** (ADR-0093). I giudici automatici non concordano con gli
esperti (κ vicino a zero in TTCW, 2024, e in «Measuring AI Slop», 2025), e
ottimizzare un numero peggiora il testo. Resta il lettore: il DM legge ad alta
voce due versioni dello stesso box, senza sapere quale è la nuova, e sceglie.

Tre passi, in quest'ordine, e il primo si fa **prima** di riscrivere:

| Comando | Cosa fa |
|---|---|
| `campione` | sceglie i box da confrontare, con un seme dichiarato, e ne congela il testo |
| `coppie` | trova in una versione successiva il box che corrisponde a ciascuno, mette le due versioni in ordine casuale e scrive la scheda per il DM e la chiave a parte |
| `esito` | legge le scelte del DM, scioglie la chiave e dice se la nuova versione vince |

Il criterio di `esito` è quello scritto prima del rifacimento di ARC-07
(`PROSA-DETERMINISTICA-2026-10-18` §6): la nuova versione deve essere
preferita in **almeno 14 coppie su 20**; le coppie identiche non si votano, e
con meno coppie votabili la soglia si riproporziona per eccesso (12 su 16). Con 20 coppie, 14 dà un intervallo di
Wilson al 95% che parte sopra 0,48: basta per dire «meglio», non «molto
meglio». Il pari conta come non vinto.

⚠️ **L'appaiamento è il punto debole.** Dopo una riscrittura un box può
cambiare posto, nome di sezione o essere spezzato in due. `coppie` sceglie,
nello stesso file, il box più simile (difflib, senza `autojunk`: con il
default due box quasi uguali di 300 caratteri davano 0,08), e preferisce quello sotto la
stessa intestazione; se il box è stato spezzato in battute, prova anche a
unire fino a otto battute consecutive sotto la stessa intestazione. Dice la somiglianza di ogni coppia, e segna le coppie
dubbie (sotto 0,2) e quelle identiche, che non si votano.

Uso:

    python3 scripts/cieco_versioni.py campione --ref main --seme 20261018 \\
        --per-file 4 --uscita CAMPIONE.json FILE...
    python3 scripts/cieco_versioni.py coppie --campione CAMPIONE.json \\
        --dopo REF --seme 7 --scheda SCHEDA.md --chiave CHIAVE.json
    python3 scripts/cieco_versioni.py esito --chiave CHIAVE.json --voti VOTI.txt

**Il perché, facoltativo.** Dopo il voto si possono scrivere una o più
etichette che dicono che cosa non andava nella versione scartata, per esempio
`7 B goffo spiega`. Vengono dalla tassonomia LAMP delle correzioni degli
scrittori (Chakrabarty et al. 2025) e dai test TTCW (CHI 2024), e sono in
`ETICHETTE`. Non cambiano il verdetto: `esito` le conta, divise fra nuova e
vecchia versione, così dopo una cinquantina di voti si sa quali difetti il DM
vede davvero e si cerca una misura per quelli (lotto 7 di
PIANO-AVVENTURE-COMMUNITY: nessuna misura della letteratura prevedeva i primi
38 voti).
"""
from __future__ import annotations

import argparse
import difflib
import json
import math
import random
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import misura_craft as mc  # noqa: E402

#: Un box sotto queste parole è una didascalia o una battuta sola: non si vota.
PAROLE_MINIME = 25
#: Il perché di un voto: il difetto della versione scartata (LAMP e TTCW).
ETICHETTE = {
    "goffo": "fraseggio goffo, parola sbagliata o pronome ambiguo",
    "struttura": "frase costruita male, troppo lunga o spezzata",
    "spiega": "spiega quello che la scena dovrebbe mostrare",
    "cliche": "immagine già sentita",
    "ricercata": "prosa ricercata, aggettivi di troppo",
    "vaga": "manca il dettaglio specifico",
    "incoerente": "fatti, tempi o luoghi che non tornano",
    "ritmo": "si legge male ad alta voce",
    "piatta": "niente sensi, niente atmosfera",
    "inglese": "suona tradotto",
}
#: Sotto questa somiglianza la coppia è dubbia: forse non è lo stesso box.
SOMIGLIANZA_DUBBIA = 0.2
#: Il criterio scritto prima del rifacimento di ARC-07: 14 su 20. Con meno
#: coppie votabili (le identiche non si votano) la soglia si riproporziona,
#: per eccesso: 12 su 16, come nel primo voto del 2026-10-18.
VITTORIE_RICHIESTE = 14
COPPIE_ATTESE = 20
#: Una riscrittura può spezzare un box in battute: si prova anche a unire fino
#: a tante battute consecutive sotto la stessa intestazione.
BATTUTE_UNIBILI = 8

#: Le coppie già decise dalla misura che si fanno votare lo stesso, a caso e
#: senza dirlo: sono il controllo che la misura regge. Se il DM ne contraddice
#: più di una su quattro, la misura non decide più e si torna al cieco intero.
CONTROLLI = 4
CONTROLLI_TOLLERATI = 1

_TITOLO = re.compile(r"^#{1,6}\s+(.*\S)")

#: Un box con un numero di regola dentro è una nota per il DM scritta in
#: corsivo citato («Calibrazione rapida: Blast di Artemis ~28/colpo»), non
#: prosa da leggere: `box_read_aloud` la prende, il campione no.
_NOTA_DI_REGOLA = re.compile(r"\b(?:pf|RD|CD|TS|GS|PE|DV|CA)\s*\d|\d+\s*pf\b|~\d")


def testo_a(ref: str, percorso: str) -> str:
    """Il file com'era a `ref`. Con ref vuoto, il file sul disco."""
    if not ref:
        return (ROOT / percorso).read_text(encoding="utf-8")
    return subprocess.run(["git", "show", f"{ref}:{percorso}"], cwd=ROOT,
                          check=True, capture_output=True, text=True).stdout


#: Una battuta fuori dai box: `Hella: *«…»*`, `> **VARIS (telepatico):** *«…»*`,
#: o l'inciso in corsivo fra due battute. `box_read_aloud` non le prende, e non
#: deve (non sono box); ma quando una riscrittura spezza un box in battute, il
#: box vecchio va confrontato con le battute rimesse insieme.
#: L'etichetta in grassetto può avere una didascalia lunga e due punti dentro
#: («**AEGIS FANG (non canta: urla, dentro il cranio):**»): la #251 ne aveva
#: due che il primo pattern non vedeva, e i box sembravano impoveriti.
_BATTUTA = re.compile(r"^(?:>\s*)?(?:\*\*[A-ZÀ-Ù][^*\n]{0,100}:\*\*|[A-ZÀ-Ù][^:\n]{0,40}:)\s*[*_]«")
_INCISO = re.compile(r"^[*_][^*_\s].*[*_]$")


def _battute(righe: "list[str]") -> "list[tuple[int, list[str]]]":
    """Le battute e gli incisi, come paragrafi, con la riga d'inizio."""
    uscita, i = [], 0
    while i < len(righe):
        if _BATTUTA.match(righe[i]) or _INCISO.match(righe[i]):
            j = i + 1
            while j < len(righe) and righe[j].strip() and not _TITOLO.match(righe[j]):
                j += 1
            uscita.append((i, righe[i:j]))
            i = j
        else:
            i += 1
    return uscita


def box_con_titolo(testo: str, battute: bool = False) -> "list[dict]":
    """I box di `box_read_aloud`, ognuno con l'intestazione sotto cui sta.

    Con `battute`, anche le battute e gli incisi fuori dai box, nell'ordine del
    file: serve solo dal lato della versione nuova, per ricomporre un box
    spezzato."""
    righe = testo.splitlines()
    titoli, corrente = {}, ""
    for i, r in enumerate(righe):
        m = _TITOLO.match(r)
        if m:
            corrente = m.group(1)
        titoli[i] = corrente
    uscita, cursore, inizi = [], 0, []
    for b in mc.box_read_aloud(testo):
        # La riga d'inizio del box: la prima occorrenza dopo il box precedente.
        try:
            inizio = righe.index(b[0], cursore)
        except ValueError:
            inizio = cursore
        cursore = inizio + len(b)
        inizi.append((inizio, b))
    if battute:
        dentro = {i for inizio, b in inizi for i in range(inizio, inizio + len(b))}
        inizi += [(i, b) for i, b in _battute(righe) if i not in dentro]
        inizi.sort(key=lambda x: x[0])
    for inizio, b in inizi:
        corpo = mc.corpo_del_box(b)
        uscita.append({"titolo": titoli.get(inizio, ""), "testo": corpo,
                       "parole": len(corpo.split())})
    return uscita


def campione(ref: str, files: "list[str]", per_file: int, seme: int) -> dict:
    rng = random.Random(seme)
    voci = []
    for f in files:
        candidati = [(i, b) for i, b in enumerate(box_con_titolo(testo_a(ref, f)))
                     if b["parole"] >= PAROLE_MINIME
                     and not _NOTA_DI_REGOLA.search(b["testo"])]
        scelti = sorted(rng.sample(candidati, min(per_file, len(candidati))),
                        key=lambda x: x[0])
        voci += [{"file": f, "indice": i, **b} for i, b in scelti]
    return {"ref": ref, "seme": seme, "per_file": per_file,
            "parole_minime": PAROLE_MINIME, "voci": voci}


def _candidati(dopo: "list[dict]") -> "list[tuple[int, dict]]":
    """Ogni box, e ogni fila di box consecutivi sotto la stessa intestazione."""
    uscita = []
    for i, b in enumerate(dopo):
        uscita.append((i, b))
        testi = [b["testo"]]
        for j in range(i + 1, min(i + BATTUTE_UNIBILI, len(dopo))):
            if dopo[j]["titolo"] != b["titolo"]:
                break
            testi.append(dopo[j]["testo"])
            uscita.append((i, {"titolo": b["titolo"], "testo": "\n\n".join(testi)}))
    return uscita


def appaia(voce: dict, dopo: "list[dict]") -> "tuple[int, float, str]":
    """L'indice del primo box più simile nella versione dopo, la somiglianza e
    il testo, che può essere più battute consecutive unite."""
    if not dopo:
        return -1, 0.0, ""
    def punteggio(b):
        r = difflib.SequenceMatcher(None, voce["testo"], b["testo"],
                                    autojunk=False).ratio()
        return r + (0.1 if b["titolo"] == voce["titolo"] else 0.0), r
    i, b = max(_candidati(dopo), key=lambda c: punteggio(c[1])[0])
    return i, punteggio(b)[1], b["testo"]


def verdetto_misurato(vecchio: str, nuovo: str) -> "tuple[str, str]":
    """Quale versione sceglierebbe il DM, secondo le due regole del primo voto
    cieco (2026-10-18, ADR-0093), e perché. «indecisa» va al cieco.

    1. Un box spezzato in battute perde: nelle due coppie in cui la
       riscrittura divideva un monologo, il DM ha scelto la vecchia.
    2. Chi ha più dettagli sensoriali vince: dove la riscrittura ne toglieva
       il DM ha scelto la vecchia cinque volte su cinque.
    A pari dettagli la misura non sa dire nulla: lo dice il DM.
    """
    # Tre pezzi almeno: battuta, inciso, battuta. Due pezzi sono spesso un box
    # e il suo vicino che l'appaiamento ha unito (coppie 8 e 18 del primo voto).
    pezzi = nuovo.count("\n\n") + 1
    if pezzi >= 3 and "\n\n" not in vecchio and "«" in vecchio:
        return "vecchia", f"spezzato in {pezzi} battute"
    d = mc.dettagli_sensoriali(nuovo) - mc.dettagli_sensoriali(vecchio)
    if d < 0:
        return "vecchia", f"{-d} dettagli sensoriali in meno"
    if d > 0:
        return "nuova", f"{d} dettagli sensoriali in più"
    return "indecisa", "stessi dettagli sensoriali"


def coppie(camp: dict, ref_dopo: str, seme: int) -> "tuple[str, dict]":
    rng = random.Random(seme)
    cache: dict = {}
    scheda = ["# Confronto cieco fra due versioni", "",
              "Leggi ad alta voce **A** e poi **B**. Scrivi nel file dei voti una "
              "riga per coppia, `N A`, `N B` o `N =`. Non aprire la chiave.",
              "Se vuoi, dopo la lettera scrivi che cosa non andava nell'altra: "
              + ", ".join(f"`{k}`" for k in ETICHETTE) + ".", ""]
    chiave = {"campione_ref": camp["ref"], "dopo": ref_dopo, "seme": seme, "coppie": []}
    n, testi = 0, {}
    for voce in camp["voci"]:
        if voce["file"] not in cache:
            try:
                cache[voce["file"]] = box_con_titolo(testo_a(ref_dopo, voce["file"]),
                                                     battute=True)
            except subprocess.CalledProcessError:
                cache[voce["file"]] = []
        dopo = cache[voce["file"]]
        _, somiglianza, nuovo = appaia(voce, dopo)
        stato = ("identica" if nuovo == voce["testo"] else
                 "dubbia" if somiglianza < SOMIGLIANZA_DUBBIA else "valida")
        n += 1
        nuova_e_a = rng.random() < 0.5
        misura, perche = verdetto_misurato(voce["testo"], nuovo)
        chiave["coppie"].append({"n": n, "file": voce["file"], "titolo": voce["titolo"],
                                 "nuova": "A" if nuova_e_a else "B",
                                 "somiglianza": round(somiglianza, 3), "stato": stato,
                                 "misura": misura, "perche": perche, "controllo": False})
        testi[n] = (nuovo, voce)
    # Al cieco vanno le indecise, più CONTROLLI coppie già decise, scelte a caso.
    decise = [c for c in chiave["coppie"]
              if c["stato"] != "identica" and c["misura"] != "indecisa"]
    for c in rng.sample(decise, min(CONTROLLI, len(decise))):
        c["controllo"] = True
    for c in chiave["coppie"]:
        if c["stato"] == "identica" or (c["misura"] != "indecisa" and not c["controllo"]):
            continue
        nuovo, voce = testi[c["n"]]
        a, b = (nuovo, voce["testo"]) if c["nuova"] == "A" else (voce["testo"], nuovo)
        a, b = (x.replace("\n\n", "\n>\n> ") for x in (a, b))
        scheda += [f"## Coppia {c['n']}", "", f"*{Path(voce['file']).name} · {voce['titolo']}*",
                   "", "**A**", "", f"> {a}", "", "**B**", "", f"> {b}", ""]
    return "\n".join(scheda), chiave


def wilson(k: int, n: int, z: float = 1.96) -> "tuple[float, float]":
    if n == 0:
        return 0.0, 0.0
    p = k / n
    centro = (p + z * z / (2 * n)) / (1 + z * z / n)
    margine = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centro - margine), min(1.0, centro + margine)


def soglia_per(votabili: int) -> int:
    """Le vittorie richieste su `votabili` coppie, in proporzione a 14 su 20."""
    return math.ceil(VITTORIE_RICHIESTE * votabili / COPPIE_ATTESE)


_VOTO = re.compile(r"^\s*(\d+)\s*[:.)-]?\s*([AaBb=])(?=\s|$)\s*(.*?)\s*$")


def esito(chiave: dict, voti_testo: str) -> dict:
    voti, motivi = {}, {}
    for r in voti_testo.splitlines():
        m = _VOTO.match(r)
        if m:
            voti[int(m.group(1))] = m.group(2).upper()
            parole = [w.strip(",;.").lower() for w in m.group(3).split()]
            motivi[int(m.group(1))] = [w for w in parole if w]
    etichette: dict = {"nuova": {}, "vecchia": {}, "sconosciute": []}
    nuova = vecchia = pari = misurate = 0
    controlli = contraddetti = 0
    for c in chiave["coppie"]:
        if c["stato"] == "identica":
            continue
        misura = c.get("misura", "indecisa")
        if c["n"] in voti:
            v = voti[c["n"]]
            scartata = "nuova" if v not in ("=", c["nuova"]) else "vecchia"
            for w in motivi.get(c["n"], []) if v != "=" else []:
                if w in ETICHETTE:
                    etichette[scartata][w] = etichette[scartata].get(w, 0) + 1
                else:
                    etichette["sconosciute"].append(w)
            if c.get("controllo"):
                controlli += 1
                scelta = "=" if v == "=" else ("nuova" if v == c["nuova"] else "vecchia")
                contraddetti += scelta != misura
        elif misura != "indecisa" and not c.get("controllo"):
            # Decisa dalla misura: conta come il voto che la misura prevede.
            misurate += 1
            v = c["nuova"] if misura == "nuova" else ("B" if c["nuova"] == "A" else "A")
        else:
            continue
        if v == "=":
            pari += 1
        elif v == c["nuova"]:
            nuova += 1
        else:
            vecchia += 1
    n = nuova + vecchia + pari
    votabili = sum(1 for c in chiave["coppie"] if c["stato"] != "identica")
    soglia = soglia_per(votabili)
    basso, alto = wilson(nuova, n)
    if controlli and contraddetti > CONTROLLI_TOLLERATI:
        verdetto = (f"misura smentita: il DM contraddice {contraddetti} controlli su "
                    f"{controlli}; si rifà il cieco su tutte le coppie")
    elif n < votabili:
        verdetto = f"incompleto: {n} coppie decise su {votabili}"
    elif nuova >= soglia:
        verdetto = "meglio: la nuova versione vince in modo dimostrabile"
    else:
        verdetto = "non dimostrato: la nuova versione non vince abbastanza coppie"
    return {"nuova": nuova, "vecchia": vecchia, "pari": pari, "votate": n,
            "votabili": votabili, "soglia": soglia, "misurate": misurate,
            "controlli": [controlli - contraddetti, controlli],
            "wilson_95": [round(basso, 3), round(alto, 3)], "verdetto": verdetto,
            "etichette": etichette}


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("campione", help="sceglie e congela i box, prima di riscrivere")
    c.add_argument("--ref", default="", help="la versione di partenza (vuoto: il disco)")
    c.add_argument("--seme", type=int, required=True)
    c.add_argument("--per-file", type=int, default=4)
    c.add_argument("--uscita", required=True)
    c.add_argument("files", nargs="+")
    p = sub.add_parser("coppie", help="scheda per il DM e chiave a parte")
    p.add_argument("--campione", required=True)
    p.add_argument("--dopo", default="", help="la versione nuova (vuoto: il disco)")
    p.add_argument("--seme", type=int, required=True)
    p.add_argument("--scheda", required=True)
    p.add_argument("--chiave", required=True)
    e = sub.add_parser("esito", help="scioglie la chiave e applica il criterio")
    e.add_argument("--chiave", required=True)
    e.add_argument("--voti", required=True)
    a = ap.parse_args(argv)

    if a.cmd == "campione":
        dati = campione(a.ref, a.files, a.per_file, a.seme)
        Path(a.uscita).write_text(json.dumps(dati, ensure_ascii=False, indent=1) + "\n",
                                  encoding="utf-8")
        print(f"{len(dati['voci'])} box congelati in {a.uscita} (seme {a.seme})")
    elif a.cmd == "coppie":
        camp = json.loads(Path(a.campione).read_text(encoding="utf-8"))
        scheda, chiave = coppie(camp, a.dopo, a.seme)
        Path(a.scheda).write_text(scheda + "\n", encoding="utf-8")
        Path(a.chiave).write_text(json.dumps(chiave, ensure_ascii=False, indent=1) + "\n",
                                  encoding="utf-8")
        stati = [c["stato"] for c in chiave["coppie"]]
        print(f"{stati.count('valida')} coppie valide, {stati.count('dubbia')} dubbie, "
              f"{stati.count('identica')} identiche (non si votano)")
        al_cieco = [c for c in chiave["coppie"] if c["stato"] != "identica"
                    and (c["misura"] == "indecisa" or c["controllo"])]
        print(f"{len(al_cieco)} al cieco del DM ({sum(c['controllo'] for c in al_cieco)} "
              f"di controllo), le altre le decide la misura")
    else:
        chiave = json.loads(Path(a.chiave).read_text(encoding="utf-8"))
        r = esito(chiave, Path(a.voti).read_text(encoding="utf-8"))
        print(f"decise dalla misura {r['misurate']} · controlli confermati "
              f"{r['controlli'][0]} su {r['controlli'][1]}")
        print(f"nuova {r['nuova']} · vecchia {r['vecchia']} · pari {r['pari']} "
              f"su {r['votate']} (soglia {r['soglia']} su {r['votabili']}) · Wilson 95% {r['wilson_95']}")
        print(r["verdetto"])
        for chi in ("nuova", "vecchia"):
            if r["etichette"][chi]:
                conti = sorted(r["etichette"][chi].items(), key=lambda x: -x[1])
                print(f"perché ha perso la {chi}: " + ", ".join(f"{k} {n}" for k, n in conti))
        if r["etichette"]["sconosciute"]:
            print("etichette non riconosciute: " + ", ".join(r["etichette"]["sconosciute"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
