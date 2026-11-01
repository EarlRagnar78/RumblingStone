#!/usr/bin/env python3
"""Quanto due moduli sono lo stesso modulo: misura ripetibile, solo stdlib.

Nasce dalla domanda del DM del 2026-11-01 sul Drappo di Tarsilia e sul Palio di
Channathgate: *«se sono diversi bisogna capire misurando quando sono identici e
poi decidere»*. Lo script non decide: misura su due assi che vanno tenuti
separati, perché danno risposte diverse.

1. **Testo** (automatico, nessuna scelta umana): quanta parte dei 6-grammi di
   parole di B compare anche in A e viceversa, quante frasi di B sono quasi
   copiate da A, quali titoli di sezione si somigliano, quali nomi propri
   ricorrono in tutti e due.
2. **Impianto** (dichiarato): un file JSON di corrispondenze elenca i concetti
   (scene, PNG, contrade, regole della corsa, struttura) con le espressioni
   regolari che li riconoscono in A e in B. Lo script conta dove compaiono e li
   classifica: condiviso con lo stesso nome, condiviso ma rinominato, solo in A,
   solo in B. Le corrispondenze sono una lettura umana e si possono discutere:
   per questo stanno in un file a parte, versionato, e non nel codice.

Uso:
    python3 scripts/misura_derivazione.py CORRISPONDENZE.json \
        [--json USCITA.json] [--md USCITA.md]

Lo stesso ingresso dà sempre la stessa uscita (niente caso, ordinamenti fissi).
"""
from __future__ import annotations

import argparse
import difflib
import glob
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
N_SHINGLE = 6
N_FRASE = 4
SOGLIA_FRASE = 0.6
SOGLIA_TITOLO = 0.75
MIN_PAROLE_FRASE = 8

_PAROLA = re.compile(r"[a-zà-ÿ0-9]+(?:'[a-zà-ÿ0-9]+)?", re.IGNORECASE)
_TITOLO = re.compile(r"^#{1,4}\s+(.*)$", re.MULTILINE)
_COMMENTO = re.compile(r"<!--.*?-->", re.DOTALL)
_NOME = re.compile(r"(?<=[a-zà-ÿ,;:] )([A-ZÀ-Ý][a-zà-ÿ]{2,})")

# Parole con la maiuscola che non sono nomi di nessuno: titoli, termini di
# regola, abbreviazioni. Servono solo a pulire la lista dei nomi in comune.
_NON_NOMI = {
    "Giorno", "Corsa", "Morale", "Onore", "Prova", "Riflessi", "Volontà",
    "Tempra", "Diplomazia", "Intimidire", "Raggirare", "Percepire", "Cavalcare",
    "Addestrare", "Conoscenze", "Intuizione", "Furtività", "Acrobazia",
    "Artigianato", "Professione", "Sapienza", "Guarire", "Scalare", "Nuotare",
    "Sopravvivenza", "Disattivare", "Rapidità", "Raccogliere", "Cercare",
    "Osservare", "Ascoltare", "Nascondersi", "Muoversi", "Saltare", "Utilizzare",
    "Car", "For", "Des", "Cos", "Int", "Sag", "Tiro", "Iniziativa", "Talenti",
    "Abilità", "Lingue", "Velocità", "Attacco", "Difesa", "Statistiche",
    "Tattiche", "Scena", "Fase", "Sessione", "Contrada", "Capitano", "Capitana",
    "Fantino", "Tabella", "Nota", "Vedi", "Esito", "Successo", "Fallimento",
}


def normalizza(testo: str) -> str:
    testo = unicodedata.normalize("NFC", testo)
    return testo.replace("’", "'").replace("`", "")


def parole(testo: str) -> list[str]:
    return [p.lower() for p in _PAROLA.findall(testo)]


def shingle(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    return {tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}


def frasi(testo: str) -> list[str]:
    pezzi = re.split(r"(?<=[.!?»])\s+|\n\s*\n|\n[-*|>#]", testo)
    return [p.strip() for p in pezzi if len(parole(p)) >= MIN_PAROLE_FRASE]


def titoli(testo: str) -> list[str]:
    out = []
    for t in _TITOLO.findall(testo):
        t = re.sub(r"[*_`§#]|\(.*?\)|<.*?>", " ", t)
        t = re.sub(r"^[\s\d.·—–-]+", "", t)
        t = " ".join(parole(t))
        if t:
            out.append(t)
    return out


def carica_corpus(schemi: list[str], escludi: list[str] | None = None) -> dict[str, str]:
    file = set()
    for schema in schemi:
        file.update(glob.glob(str(ROOT / schema)))
    for schema in escludi or []:
        file.difference_update(glob.glob(str(ROOT / schema)))
    corpus = {}
    for f in sorted(file):
        p = Path(f)
        if p.is_file():
            testo = _COMMENTO.sub(" ", normalizza(p.read_text(encoding="utf-8")))
            corpus[p.relative_to(ROOT).as_posix()] = testo
    return corpus


def misura_testo(a: dict[str, str], b: dict[str, str]) -> dict:
    tok_a = {f: parole(t) for f, t in a.items()}
    tok_b = {f: parole(t) for f, t in b.items()}
    sh_a = set().union(*(shingle(t, N_SHINGLE) for t in tok_a.values()))
    sh_b = set().union(*(shingle(t, N_SHINGLE) for t in tok_b.values()))
    comuni = sh_a & sh_b

    def cont(x: set, y: set) -> float:
        return round(len(x & y) / len(x), 4) if x else 0.0

    per_file_b = {}
    for f, t in tok_b.items():
        s = shingle(t, N_SHINGLE)
        per_file_b[f] = {"parole": len(t), "contenuto_in_A": cont(s, sh_a)}

    # Frasi di B quasi copiate da A: la frase c'è se almeno il 60% dei suoi
    # 4-grammi sta nel corpus A.
    q_a = set().union(*(shingle(t, N_FRASE) for t in tok_a.values()))
    quasi = []
    totale_frasi = 0
    for f, t in b.items():
        for fr in frasi(t):
            totale_frasi += 1
            s = shingle(parole(fr), N_FRASE)
            r = len(s & q_a) / len(s) if s else 0.0
            if r >= SOGLIA_FRASE:
                quasi.append({"file": f, "quota": round(r, 2),
                              "frase": fr[:160]})
    quasi.sort(key=lambda d: (-d["quota"], d["file"], d["frase"]))

    # Passaggi comuni più lunghi: si fondono i 6-grammi comuni consecutivi di B.
    passaggi = []
    for f, t in tok_b.items():
        i = 0
        while i <= len(t) - N_SHINGLE:
            if tuple(t[i:i + N_SHINGLE]) in comuni:
                j = i
                while j <= len(t) - N_SHINGLE and tuple(t[j:j + N_SHINGLE]) in comuni:
                    j += 1
                passaggi.append((j - i + N_SHINGLE - 1, f, " ".join(t[i:j + N_SHINGLE - 1])))
                i = j
            else:
                i += 1
    passaggi.sort(key=lambda x: (-x[0], x[1], x[2]))

    return {
        "parole_A": sum(len(t) for t in tok_a.values()),
        "parole_B": sum(len(t) for t in tok_b.values()),
        "shingle_n": N_SHINGLE,
        "jaccard": round(len(comuni) / len(sh_a | sh_b), 4) if sh_a | sh_b else 0.0,
        "shingle_comuni": len(comuni),
        "shingle_B": len(sh_b),
        "B_contenuto_in_A": cont(sh_b, sh_a),
        "A_contenuto_in_B": cont(sh_a, sh_b),
        "frasi_B": totale_frasi,
        "frasi_B_quasi_da_A": len(quasi),
        "esempi_frasi": quasi[:12],
        "passaggi_comuni_piu_lunghi": [
            {"parole": n, "file": f, "testo": s[:200]} for n, f, s in passaggi[:12]],
        "per_file_B": per_file_b,
    }


def misura_titoli(a: dict[str, str], b: dict[str, str]) -> dict:
    ta = sorted({t for testo in a.values() for t in titoli(testo)})
    tb = sorted({t for testo in b.values() for t in titoli(testo)})
    coppie = []
    for t in tb:
        migliore = max(ta, key=lambda x: (difflib.SequenceMatcher(None, t, x).ratio(), x),
                       default="")
        r = difflib.SequenceMatcher(None, t, migliore).ratio() if migliore else 0.0
        if r >= SOGLIA_TITOLO:
            coppie.append({"B": t, "A": migliore, "somiglianza": round(r, 2)})
    coppie.sort(key=lambda d: (-d["somiglianza"], d["B"]))
    return {"titoli_A": len(ta), "titoli_B": len(tb),
            "titoli_B_simili_in_A": len(coppie), "soglia": SOGLIA_TITOLO,
            "coppie": coppie}


def misura_nomi(a: dict[str, str], b: dict[str, str], minimo: int = 3) -> dict:
    def conta(c: dict[str, str]) -> Counter:
        n = Counter()
        for testo in c.values():
            n.update(m for m in _NOME.findall(testo) if m not in _NON_NOMI)
        return Counter({k: v for k, v in n.items() if v >= minimo})
    na, nb = conta(a), conta(b)
    comuni = sorted(set(na) & set(nb), key=lambda k: (-(na[k] + nb[k]), k))
    return {"nomi_A": len(na), "nomi_B": len(nb), "comuni": len(comuni),
            "jaccard": round(len(comuni) / len(set(na) | set(nb)), 4) if na or nb else 0.0,
            "elenco_comuni": [{"nome": k, "A": na[k], "B": nb[k]} for k in comuni[:40]]}


def conta_regex(corpus: dict[str, str], espressioni: list[str],
                maiuscole: bool = False) -> dict[str, int]:
    flag = 0 if maiuscole else re.IGNORECASE
    out = {}
    for f, testo in corpus.items():
        n = sum(len(re.findall(e, testo, flag)) for e in espressioni)
        if n:
            out[f] = n
    return out


def misura_concetti(a: dict[str, str], b: dict[str, str], concetti: list[dict]) -> dict:
    righe = []
    for c in concetti:
        # Senza "B" il concetto si cerca in B con le stesse espressioni di A.
        # «Stesso nome» vuol dire che le parole di A ricorrono anche in B;
        # «rinominato» che in B il concetto c'è solo con parole sue.
        ea = c.get("A", [])
        eb = c.get("B", ea)
        mc = bool(c.get("maiuscole"))
        fa, fb = conta_regex(a, ea, mc), conta_regex(b, eb, mc)
        if fa and fb:
            stato = "stesso nome" if conta_regex(b, ea, mc) else "rinominato"
        elif fa:
            stato = "solo A"
        elif fb:
            stato = "solo B"
        else:
            stato = "assente"
        righe.append({"id": c["id"], "dimensione": c["dimensione"],
                      "descrizione": c.get("descrizione", ""), "stato": stato,
                      "occorrenze_A": sum(fa.values()), "occorrenze_B": sum(fb.values()),
                      "file_A": sorted(fa), "file_B": sorted(fb),
                      "nota": c.get("nota", "")})
    dimensioni = {}
    for r in righe:
        d = dimensioni.setdefault(r["dimensione"], Counter())
        d[r["stato"]] += 1
    sintesi = {}
    for d, cnt in sorted(dimensioni.items()):
        tot = sum(cnt.values()) - cnt["assente"]
        condivisi = cnt["stesso nome"] + cnt["rinominato"]
        sintesi[d] = {**{k: cnt[k] for k in ("stesso nome", "rinominato", "solo A",
                                             "solo B", "assente")},
                      "quota_condivisa": round(condivisi / tot, 3) if tot else 0.0}
    return {"righe": righe, "per_dimensione": sintesi}


def misura(cfg: dict) -> dict:
    a = carica_corpus(cfg["A"]["file"], cfg["A"].get("escludi"))
    b = carica_corpus(cfg["B"]["file"], cfg["B"].get("escludi"))
    if not a or not b:
        raise SystemExit("corpus vuoto: controlla gli schemi dei file")
    return {
        "A": {"nome": cfg["A"]["nome"], "file": sorted(a)},
        "B": {"nome": cfg["B"]["nome"], "file": sorted(b)},
        "testo": misura_testo(a, b),
        "titoli": misura_titoli(a, b),
        "nomi": misura_nomi(a, b),
        "impianto": misura_concetti(a, b, cfg.get("concetti", [])),
    }


def _pct(x: float) -> str:
    return f"{x * 100:.1f}%".replace(".", ",")


def rapporto_md(r: dict) -> str:
    A, B = r["A"]["nome"], r["B"]["nome"]
    t, ti, no, im = r["testo"], r["titoli"], r["nomi"], r["impianto"]
    out = [f"# Misura: {B} contro {A}", "",
           "Generato da `scripts/misura_derivazione.py`. Non modificare a mano: "
           "si rigenera dal file delle corrispondenze.", "",
           "## Testo (automatico)", "",
           "| Misura | Valore |", "|---|---|",
           f"| Parole di A / di B | {t['parole_A']} / {t['parole_B']} |",
           f"| 6-grammi di B presenti anche in A | {_pct(t['B_contenuto_in_A'])} "
           f"({t['shingle_comuni']} su {t['shingle_B']}) |",
           f"| 6-grammi di A presenti anche in B | {_pct(t['A_contenuto_in_B'])} |",
           f"| Jaccard dei 6-grammi | {_pct(t['jaccard'])} |",
           f"| Frasi di B quasi copiate da A (≥60% dei 4-grammi) | "
           f"{t['frasi_B_quasi_da_A']} su {t['frasi_B']} |",
           f"| Titoli di B simili a un titolo di A (≥{ti['soglia']}) | "
           f"{ti['titoli_B_simili_in_A']} su {ti['titoli_B']} |",
           f"| Nomi propri ricorrenti in comune | {no['comuni']} "
           f"(Jaccard {_pct(no['jaccard'])}) |", ""]
    if t["passaggi_comuni_piu_lunghi"]:
        out += ["### Passaggi comuni più lunghi", ""]
        out += [f"- {p['parole']} parole, `{p['file'].rsplit('/', 1)[-1]}`: «{p['testo']}»"
                for p in t["passaggi_comuni_piu_lunghi"][:8]]
        out.append("")
    if ti["coppie"]:
        out += ["### Titoli simili", "", "| B | A | Somiglianza |", "|---|---|---|"]
        out += [f"| {c['B']} | {c['A']} | {c['somiglianza']} |" for c in ti["coppie"]]
        out.append("")
    out += ["### Nomi propri in comune", "",
            ", ".join(f"{n['nome']} ({n['A']}/{n['B']})" for n in no["elenco_comuni"]) or "nessuno",
            "", "## Impianto (corrispondenze dichiarate)", "",
            "| Dimensione | Stesso nome | Rinominato | Solo A | Solo B | Quota condivisa |",
            "|---|---|---|---|---|---|"]
    for d, s in im["per_dimensione"].items():
        out.append(f"| {d} | {s['stesso nome']} | {s['rinominato']} | {s['solo A']} | "
                   f"{s['solo B']} | {_pct(s['quota_condivisa'])} |")
    out += ["", "| Concetto | Dimensione | Stato | Occ. A | Occ. B | Nota |",
            "|---|---|---|---|---|---|"]
    for riga in im["righe"]:
        out.append(f"| {riga['descrizione'] or riga['id']} | {riga['dimensione']} | "
                   f"{riga['stato']} | {riga['occorrenze_A']} | {riga['occorrenze_B']} | "
                   f"{riga['nota']} |")
    out += ["", "## Testo per file di B", "", "| File | Parole | 6-grammi presenti in A |",
            "|---|---|---|"]
    for f, v in sorted(t["per_file_B"].items()):
        out.append(f"| `{f.rsplit('/', 1)[-1]}` | {v['parole']} | {_pct(v['contenuto_in_A'])} |")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("corrispondenze", type=Path)
    ap.add_argument("--json", type=Path)
    ap.add_argument("--md", type=Path)
    args = ap.parse_args(argv)
    cfg = json.loads(args.corrispondenze.read_text(encoding="utf-8"))
    r = misura(cfg)
    if args.json:
        args.json.write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n",
                             encoding="utf-8")
    testo = rapporto_md(r)
    if args.md:
        args.md.write_text(testo, encoding="utf-8")
    if not args.json and not args.md:
        sys.stdout.write(testo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
