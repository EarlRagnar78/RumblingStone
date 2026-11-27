#!/usr/bin/env python3
r"""misura_ripetizioni_frasi.py — le immagini ripetute fra i box, frase per frase.

## Perché esiste

Il registro delle norme dà «ripetizioni fra box» come buco. Il confronto dei
4-grammi trova le copie, non le parafrasi («come un martello divino» contro
«come una valanga di ferro»). Il 2026-11-03 (RICERCA-GUARDRAIL §8) due
configurazioni dello stesso modello a confronto:

* box interi, soglia 0,90: **1** parafrasi oltre i 4-grammi su 362 box;
* **frase per frase**, box di scene diverse, copie (4-grammi ≥ 0,5) e handout
  esclusi, soglia 0,80: **6** ripetizioni vere che i 4-grammi non vedono, 3 nei
  master DEF vivi (il «filo tirato attraverso mille anni» di DEF-5 contro
  ARC08-11, il metallo sulla fronte di DEF-4 contro DEF-5, le piattaforme di
  cristallo due volte in DEF-1).

È la seconda che si adotta, come **indicatore**: un elenco da leggere prima di
consegnare un booklet. Non è un cancello: un'eco voluta è un'eco voluta, e la
riscrittura di un box passa dal cieco del DM (ADR-0093).

## Dipendenze

`sentence-transformers` col modello `paraphrase-multilingual-MiniLM-L12-v2`
(Apache 2.0, ~0,5 GB). Non sono nei requisiti del repo: canale *unstable* di
ADR-0099. Senza, lo strumento esce con 2 e lo dice. Le funzioni che scelgono
le frasi e filtrano le coppie sono deterministiche e testate senza modello.

Dal 2026-11-03 (richiesta del DM) è anche un **cancello locale**: le 2
ripetizioni vere nei master (piattaforme di DEF-1, lo strappo di ARC08-11
contro DEF-5) sono state corrette (21 → 19 coppie), le altre 19 lette e
scritte in `plans/scrittura/ripetizioni-accettate.json` col perché. `--check`
esce con 1 se compare una coppia nuova. Non gira in CI (serve il modello):
lo chiede la sezione «Cancelli deterministici» della skill narrativa.

## Uso

    python3 scripts/misura_ripetizioni_frasi.py              # master vivi, soglia 0,80
    python3 scripts/misura_ripetizioni_frasi.py --soglia 0.85 --json
    python3 scripts/misura_ripetizioni_frasi.py --check      # il cancello
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

MODELLO = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
PAROLE_MIN = 8
COPIA = 0.5          # 4-grammi in comune da cui la coppia è una copia, non una parafrasi
ACCETTATE = ROOT / "plans" / "scrittura" / "ripetizioni-accettate.json"


def _chiave(c: dict) -> frozenset:
    return frozenset({(c["a"], c["frase_a"]), (c["b"], c["frase_b"])})


def nuove(trovate: list[dict], accettate: list[dict]) -> list[dict]:
    """Le coppie trovate che non sono fra quelle lette e accettate.

    >>> x = {"a": "A.md", "b": "B.md", "frase_a": "uno", "frase_b": "due"}
    >>> y = {"a": "B.md", "b": "A.md", "frase_a": "due", "frase_b": "uno"}
    >>> nuove([x], [y]), len(nuove([x], []))
    ([], 1)
    """
    note = {_chiave(c) for c in accettate}
    return [c for c in trovate if _chiave(c) not in note]


def file_vivi() -> list[Path]:
    """I master e i moduli vivi, come la prova del 2026-11-03."""
    import misura_craft as mc
    fs = sorted(ROOT.glob("0[0-9]_*/**/*.md")) + sorted((ROOT / "10-stand-alone").glob("**/*.md"))
    return [p for p in fs
            if not any(x in str(p) for x in mc.ESCLUSI) and not any(x in p.name for x in mc.ESCLUSI_NOME)
            and "Immagini" not in str(p)
            and ("DEF-" in p.name or p.relative_to(ROOT).parts[0].startswith(("08_", "09_", "10-")))]


def frasi(testo: str, dove: str) -> list[tuple[str, int, str]]:
    """(file, numero del box, frase) per ogni frase di almeno 8 parole nei box.

    >>> frasi("> *Il vento passa fra le lame piantate e canta piano. Poi tace.*", "f")[0][2]
    'Il vento passa fra le lame piantate e canta piano.'
    """
    import misura_craft as mc
    out = []
    for k, b in enumerate(mc.box_read_aloud(testo)):
        for s in re.split(r"(?<=[.!?»])\s+", mc.corpo_del_box(b)):
            s = s.strip()
            if len(s.split()) >= PAROLE_MIN:
                out.append((dove, k, s))
    return out


def _ng(t: str, n: int = 4) -> set:
    w = re.findall(r"\w+", t.lower())
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def jaccard(a: str, b: str) -> float:
    """4-grammi in comune.

    >>> jaccard("uno due tre quattro cinque", "uno due tre quattro sei")
    0.33
    """
    x, y = _ng(a), _ng(b)
    return round(len(x & y) / (len(x | y) or 1), 2)


def tieni(a: tuple, b: tuple) -> bool:
    """La coppia è da leggere? No se è lo stesso box, la stessa frase, una copia
    (la vedono già i 4-grammi) o un handout del giocatore (copia voluta della scheda).

    >>> tieni(("A.md", 1, "x y"), ("A.md", 1, "x z"))
    False
    >>> tieni(("A.md", 1, "x"), ("ARC08-15-HANDOUTS-GIOCATORE.md", 2, "y"))
    False
    """
    if (a[0], a[1]) == (b[0], b[1]) or a[2] == b[2]:
        return False
    if any("HANDOUT" in Path(x[0]).name.upper() for x in (a, b)):
        return False
    return jaccard(a[2], b[2]) < COPIA


def coppie(fr: list[tuple], sim, soglia: float) -> list[dict]:
    """Le coppie sopra soglia da una matrice di similarità (righe = frasi)."""
    out = []
    n = len(fr)
    for i in range(n):
        for j in range(i + 1, n):
            s = float(sim[i][j])
            if s >= soglia and tieni(fr[i], fr[j]):
                out.append({"coseno": round(s, 3), "a": fr[i][0], "b": fr[j][0],
                            "frase_a": fr[i][2], "frase_b": fr[j][2]})
    return sorted(out, key=lambda x: -x["coseno"])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--soglia", type=float, default=0.80, help="coseno minimo (default 0,80)")
    ap.add_argument("--json", action="store_true", help="tutto in JSON")
    ap.add_argument("--check", action="store_true",
                    help="cancello: esce con 1 se c'è una coppia fuori da ripetizioni-accettate.json")
    a = ap.parse_args(argv)
    if not (-1.0 <= a.soglia <= 1.0):          # anche nan: un confronto con nan è falso
        ap.error("--soglia è un coseno: fra -1 e 1")
    try:
        os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("✗ serve sentence-transformers (canale unstable, ADR-0099): pip install sentence-transformers",
              file=sys.stderr)
        return 2
    fr = []
    for p in file_vivi():
        fr += frasi(p.read_text(errors="replace"), p.relative_to(ROOT).as_posix())
    try:
        m = SentenceTransformer(MODELLO)
    except Exception as e:                     # modello non in cache e rete assente
        print(f"✗ il modello {MODELLO} non si carica ({type(e).__name__}): scaricalo una volta "
              "con la rete, poi lo strumento lavora dalla cache", file=sys.stderr)
        return 2
    E = m.encode([s for *_, s in fr], normalize_embeddings=True, batch_size=64)
    out = coppie(fr, E @ E.T, a.soglia)
    if a.check:
        accettate = json.loads(ACCETTATE.read_text(encoding="utf-8"))["coppie"]
        da_correggere = nuove(out, accettate)
        print(f"RIPETIZIONI FRA BOX — {len(out)} coppie, {len(da_correggere)} nuove da correggere")
        for c in da_correggere:
            print(f"\n✗ {c['coseno']}  {c['a']}  |  {c['b']}\n  A: {c['frase_a']}\n  B: {c['frase_b']}")
        return 1 if da_correggere else 0
    if a.json:
        print(json.dumps({"frasi": len(fr), "soglia": a.soglia, "coppie": out}, ensure_ascii=False, indent=1))
    else:
        print(f"RIPETIZIONI FRA BOX — {len(fr)} frasi, {len(out)} coppie da leggere (indicatore, non cancello)")
        for c in out:
            print(f"\n{c['coseno']}  {c['a']}  |  {c['b']}\n  A: {c['frase_a']}\n  B: {c['frase_b']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
