#!/usr/bin/env python3
r"""misura_fedelta_nli.py — il riscritto contraddice l'originale? Riga per riga, con un modello NLI.

## Perché esiste

`ciclo_prosa.confronta_fatti` vede un numero, un nome o una negazione che
cambiano; `box_impoveriti` vede i dettagli tolti. Nessuno dei due vede «si gira
verso nord» diventato «si gira verso sud», o un'azione standard diventata
veloce. È la *faithfulness* di Ragas, portata dove ha senso nel repo: due testi
allineati, l'originale e la sua riscrittura (RICERCA-GUARDRAIL §9).

Misura del 2026-11-03, sulle coppie (riga tolta, riga messa) dei commit di
correzione e di prosa:

* 105 coppie etichettate da Claude: NLI F1 0,857, AUC 0,932; solo numeri F1 0,627;
* **26 coppie etichettate alla cieca dal DM** (4 «?» escluse): NLI F1 0,83
  (10 contraddizioni su 13, un falso allarme), AUC 0,92; solo numeri F1 0,62,
  AUC 0,62. NLI meglio dei numeri in 97 ricampionamenti su 100.

Sui testi presi a caso dal repo, invece, l'NLI non trova niente di buono (§8):
lavora solo su coppie allineate, cioè sulla stessa riga prima e dopo.

Non è solo un indicatore (Jfs, 2026-11-03): **la riga che contraddice torna
com'era nell'originale**, in automatico (`ripara`, `--ripara`, e dentro
`ciclo_prosa revisione` e `misura`). Una riscrittura di prosa non cambia i
fatti; una correzione voluta (un nome, un numero) si fa a mano e si scrive.
Il costo misurato: nel campione del DM un falso allarme su 11 segnalazioni,
cioè una riga buona su undici torna all'originale. Si perde una riscrittura,
non si introduce un errore.

## Configurazione (quella misurata, da non cambiare senza rimisurare)

* coppie: per ogni riga tolta, la riga messa più simile nello stesso blocco del
  diff; si tengono le coppie con somiglianza fra 0,6 e 0,98 e righe di 40-400
  caratteri, niente tabelle, titoli, immagini, codice o disegni a caratteri;
* modello `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` (MIT);
* punteggio: probabilità di *contradiction*, il massimo dei due sensi
  (prima→dopo e dopo→prima); segnalata sopra 0,5.

## Dipendenze

`transformers` e `torch` (canale *unstable* di ADR-0099, fuori dai requisiti
del repo). Senza, lo strumento esce con 2 e lo dice. La scelta delle coppie è
deterministica e testata senza modello.

## Uso

    python3 scripts/misura_fedelta_nli.py ORIGINALE.md RISCRITTO.md
    python3 scripts/misura_fedelta_nli.py --rif origin/main FILE.md [FILE.md …]
    python3 scripts/misura_fedelta_nli.py --json ORIGINALE.md RISCRITTO.md
    python3 scripts/misura_fedelta_nli.py --ripara ORIGINALE.md RISCRITTO.md   # corregge RISCRITTO
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODELLO = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
SOGLIA = 0.5
SIM_MIN, SIM_MAX = 0.6, 0.98
LUNG_MIN, LUNG_MAX = 40, 400
_SALTA = re.compile(r"[🟩🟫🧱🏰⬛⬜✅═│]|^\|.*\|$|^#|^!\[|`")


def _pulisci(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _tenibile(s: str) -> bool:
    return LUNG_MIN <= len(s) <= LUNG_MAX and not _SALTA.search(s)


def coppie(prima: str, dopo: str) -> list[dict]:
    """Le coppie (riga tolta, riga messa) da confrontare, come nella misura.

    >>> c = coppie("Il drago si alza in volo e si gira verso nord, ruggendo.\\n",
    ...            "Il drago si alza in volo e si gira verso sud, ruggendo.\\n")
    >>> [(x["riga"], x["prima"][-21:], x["dopo"][-20:]) for x in c]
    [(1, 'verso nord, ruggendo.', 'verso sud, ruggendo.')]
    """
    a, b = prima.splitlines(), dopo.splitlines()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op != "replace":
            continue
        messe = [(j, _pulisci(b[j])) for j in range(j1, j2)]
        messe = [(j, s) for j, s in messe if _tenibile(s)]
        for i in range(i1, i2):
            t = _pulisci(a[i])
            if not _tenibile(t) or not messe:
                continue
            j, m = max(messe, key=lambda x: difflib.SequenceMatcher(None, t, x[1]).ratio())
            r = difflib.SequenceMatcher(None, t, m).ratio()
            if SIM_MIN <= r < SIM_MAX:
                out.append({"riga": j + 1, "riga_prima": i + 1, "prima": t, "dopo": m,
                            "somiglianza": round(r, 2)})
    return out


class Giudice:
    """Il modello NLI caricato una volta; `punteggio` è il massimo dei due sensi."""

    def __init__(self, modello: str = MODELLO):
        os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        self.torch = torch
        self.tok = AutoTokenizer.from_pretrained(modello)
        self.m = AutoModelForSequenceClassification.from_pretrained(modello).eval()
        etichette = {v.lower(): k for k, v in self.m.config.id2label.items()}
        self.ic = etichette["contradiction"]

    def punteggio(self, a: str, b: str) -> float:
        with self.torch.no_grad():
            return max(float(self.m(**self.tok(p, h, return_tensors="pt", truncation=True,
                                               max_length=256)).logits.softmax(-1)[0][self.ic])
                       for p, h in ((a, b), (b, a)))


def segnala(prima: str, dopo: str, giudice, soglia: float = SOGLIA) -> list[dict]:
    """Le coppie che il giudice dà per contraddittorie, la più sicura per prima."""
    out = []
    for c in coppie(prima, dopo):
        p = giudice.punteggio(c["prima"], c["dopo"])
        if p > soglia:
            out.append({**c, "contraddizione": round(p, 3)})
    return sorted(out, key=lambda x: -x["contraddizione"])


def ripara(prima: str, dopo: str, giudice, soglia: float = SOGLIA) -> tuple[str, list[dict]]:
    """La correzione automatica: ogni riga del riscritto che contraddice la sua
    riga d'origine torna com'era nell'originale. Una riscrittura di prosa non
    cambia i fatti; se il cambio era voluto, lo si fa a mano e lo si dice.

    >>> class Sud:
    ...     def punteggio(self, a, b): return 0.9 if ("sud" in a) != ("sud" in b) else 0.1
    >>> testo, rimesse = ripara("Il drago si alza in volo e si gira verso nord, ruggendo.\\nAltro.\\n",
    ...                         "Il drago si alza in volo e si gira verso sud, ruggendo.\\nAltro.\\n", Sud())
    >>> testo
    'Il drago si alza in volo e si gira verso nord, ruggendo.\\nAltro.\\n'
    >>> [r["riga"] for r in rimesse]
    [1]
    """
    segn = segnala(prima, dopo, giudice, soglia)
    if not segn:
        return dopo, []
    a = prima.splitlines(keepends=True)
    b = dopo.splitlines(keepends=True)
    for c in segn:
        vecchia = a[c["riga_prima"] - 1]
        fine = b[c["riga"] - 1][len(b[c["riga"] - 1].rstrip("\r\n")):]
        b[c["riga"] - 1] = vecchia.rstrip("\r\n") + fine
    return "".join(b), sorted(segn, key=lambda x: x["riga"])


def carica_giudice():
    """Il giudice, oppure (None, perché) se mancano le librerie o il modello."""
    try:
        import torch  # noqa: F401
        import transformers  # noqa: F401
    except ImportError:
        return None, "serve transformers con torch (canale unstable, ADR-0099): pip install transformers torch"
    try:
        return Giudice(), ""
    except Exception as e:                     # modello non in cache e rete assente
        return None, (f"il modello {MODELLO} non si carica ({type(e).__name__}): scaricalo una volta "
                      "con la rete, poi lo strumento lavora dalla cache")


def _alla_revisione(rif: str, p: Path) -> str:
    rel = p.resolve().relative_to(ROOT).as_posix()
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{rif}:{rel}"],
                       capture_output=True, text=True, errors="replace")
    return r.stdout if r.returncode == 0 else ""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", type=Path, nargs="+",
                    help="ORIGINALE RISCRITTO, oppure con --rif i file da confrontare")
    ap.add_argument("--rif", help="il commit o il ramo di prima (es. origin/main)")
    ap.add_argument("--soglia", type=float, default=SOGLIA,
                    help="probabilità di contraddizione oltre cui segnalare (default 0,5)")
    ap.add_argument("--json", action="store_true", help="tutto in JSON")
    ap.add_argument("--ripara", action="store_true",
                    help="riscrive il file: le righe che contraddicono tornano all'originale")
    a = ap.parse_args(argv)
    if not (0.0 <= a.soglia <= 1.0):           # anche nan
        ap.error("--soglia è una probabilità: fra 0 e 1")
    if a.rif:
        lavori = [(f.as_posix(), _alla_revisione(a.rif, f), f.read_text(encoding="utf-8")) for f in a.file]
    elif len(a.file) == 2:
        lavori = [(a.file[1].as_posix(), a.file[0].read_text(encoding="utf-8"),
                   a.file[1].read_text(encoding="utf-8"))]
    else:
        ap.error("senza --rif servono due file: ORIGINALE RISCRITTO")
    giudice, perche = carica_giudice()
    if giudice is None:
        print(f"✗ {perche}", file=sys.stderr)
        return 2
    risultati = {}
    for nome, p, d in lavori:
        if a.ripara:
            nuovo, risultati[nome] = ripara(p, d, giudice, a.soglia)
            if risultati[nome]:
                Path(nome).write_text(nuovo, encoding="utf-8")
        else:
            risultati[nome] = segnala(p, d, giudice, a.soglia)
    if a.json:
        print(json.dumps({"modello": MODELLO, "soglia": a.soglia, "file": risultati},
                         ensure_ascii=False, indent=1))
        return 0
    n = sum(len(v) for v in risultati.values())
    print(f"FEDELTÀ DEL RISCRITTO (NLI) — {n} righe che contraddicono l'originale"
          + (", rimesse com'erano" if a.ripara else " (con --ripara tornano all'originale)"))
    for nome, segn in risultati.items():
        for c in segn:
            print(f"\n{c['contraddizione']}  {nome}:{c['riga']}\n  prima: {c['prima']}\n  dopo:  {c['dopo']}")
    return 1 if n and not a.ripara else 0


if __name__ == "__main__":
    sys.exit(main())
