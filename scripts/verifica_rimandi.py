#!/usr/bin/env python3
"""verifica_rimandi.py — i rimandi «FILE §N» e «vedi §N» puntano a una sezione che esiste?

Perché esiste
  I master e i moduli si rimandano a vicenda per sezione: «`ARC08-02` §1»,
  «state.md §2», «vedi §4». `validate_docs.py --sorgenti` controlla i link e i
  percorsi, non le sezioni: un rimando a un § che un riordino ha spostato
  resta verde, e oggi se ne accorge solo chi rilegge (ADR-0148).

Che cosa controlla
  Un rimando è una coppia (file bersaglio, numero di sezione). Il bersaglio è:
    - il file stesso, per «vedi §N», «il §N», «del §N», «al §N», «in §N»;
    - un file nominato subito prima, in backtick o no («`ARC08-02` §1»,
      «state.md §2»), se il nome individua UN solo .md del repo (per nome
      intero o per prefisso del nome). Un nome ambiguo o sconosciuto non si
      giudica: finisce fra i non verificabili, mai fra le violazioni.
  La sezione esiste se un titolo del bersaglio (riga che inizia con #) porta
  «§N» come parola, oppure inizia con il numero («## 4.», «## 4 —», «### 4)»).

  Fuori: `plans/` (parlano della storia del repo, i § cambiano apposta), i
  generati (`.hb.md`, `homebrew/`), i blocchi di codice.

Uso
  python3 scripts/verifica_rimandi.py [PERCORSI ...] [--json] [--check]

Senza percorsi legge i .md degli archi (cartelle 00_… 10-…), di campaign/ e
di Bestiario/. --check esce 1 se c'è una violazione. Solo stdlib.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RADICI = re.compile(r"^(\d\d[_-]|campaign/|Bestiario/)")
ESCLUSI = re.compile(r"(^plans/|\.hb\.md$|/homebrew/|_SNAPSHOT-STORICO)")
# «`ARC08-02` §1», «state.md §2», «ARC07-DEF-5 §8»
ESTERNO = re.compile(r"`?(?P<nome>[A-Za-z0-9][A-Za-z0-9_.-]{2,})`?\s+§(?P<n>\d+)(?![\w-])")
# «vedi §4», «il §8», «del §6»: rimando dentro lo stesso file
INTERNO = re.compile(r"\b(?:vedi|il|del|al|nel|in|dal|cfr\.?)\s+§(?P<n>\d+)(?![\w-])", re.I)
TITOLO = re.compile(r"^#{1,6}\s+(.*)$")
# Una riga che nomina un altro documento rende ambiguo un «§N» senza nome:
# «il §13 (libretto §12)», «§10 del supplemento», «aggiungi il §6 a X.md».
ALTRO_DOCUMENTO = re.compile(
    r"\.md\b|`[A-Za-z0-9][\w.-]{3,}`|\b(libretto|supplemento|manuale|master|SRD|PRD|PHB|DMG|MM|ADR-\d+|"
    r"ARC\d\d[\w-]*|DEF-\d)\b", re.I)
DOPO_ALTRO = re.compile(r"^\s*(del|della|dello|dei|di|a|al|nel|nella)\s+(?!questo|questa|sopra|sotto)\w", re.I)


# Violazioni vere già trovate e portate al DM su card: il cancello le tollera
# finché la card non è chiusa, e boccia ogni rimando rotto nuovo. Chiave:
# (file, testo del rimando). Una voce che non si trova più fa fallire il test:
# il dizionario si svuota insieme alla correzione.
# Vuoto dal 20/11: l'unica voce («`ARC07-DEF-5` §94» in campaign/state.md) è
# stata corretta in §0-bis su scelta del DM (card del 20/11).
IN_ATTESA: "dict[tuple[str, str], str]" = {}


@dataclass
class Rimando:
    file: str
    riga: int
    testo: str
    bersaglio: str
    sezione: str
    esito: str  # "ok" | "violazione" | "in_attesa" | "non_verificabile"
    motivo: str = ""


def _md_del_repo() -> "list[str]":
    out = subprocess.run(["git", "ls-files", "-z", "*.md"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    return sorted(f for f in out.split("\0") if f)


def indice_nomi(tutti: "list[str]") -> "dict[str, list[str]]":
    """nome intero e nome senza .md → percorsi."""
    idx: dict[str, list[str]] = {}
    for f in tutti:
        p = Path(f)
        for chiave in {p.name, p.stem}:
            idx.setdefault(chiave.lower(), []).append(f)
    return idx


def risolvi(nome: str, idx: "dict[str, list[str]]", tutti: "list[str]") -> "tuple[str | None, str]":
    chiave = nome.strip("`.").lower()
    if chiave.endswith(".md"):
        chiave = chiave[:-3]
    esatti = sorted(set(idx.get(chiave, []) + idx.get(chiave + ".md", [])))
    if len(esatti) == 1:
        return esatti[0], ""
    if len(esatti) > 1:
        return None, f"«{nome}» individua {len(esatti)} file"
    if not re.search(r"[A-Z0-9]", nome) or len(chiave) < 5:
        return None, f"«{nome}» non è un nome di file"
    prefisso = sorted({f for f in tutti if Path(f).stem.lower().startswith(chiave)})
    if len(prefisso) == 1:
        return prefisso[0], ""
    if not prefisso:
        return None, f"«{nome}» non individua nessun file"
    return None, f"«{nome}» individua {len(prefisso)} file per prefisso"


def sezioni(testo: str) -> "set[str]":
    trovate: set[str] = set()
    in_codice = False
    for riga in testo.splitlines():
        if riga.lstrip().startswith("```"):
            in_codice = not in_codice
            continue
        m = TITOLO.match(riga)
        if in_codice or not m:
            continue
        t = m.group(1).strip().strip("*_ ")
        trovate.update(re.findall(r"§\s?(\d+)(?![\d])", t))
        n = re.match(r"(?:\W*\s*)?(?:Parte|Sezione|Capitolo)?\s*(\d+)\s*(?:[.)—–:-]|\s|$)", t, re.I)
        if n:
            trovate.add(n.group(1))
    return trovate


def rimandi(file: str, idx, tutti, cache: "dict[str, set[str]]",
            testo: "str | None" = None) -> "list[Rimando]":
    """I rimandi di un file; `testo` sostituisce il contenuto su disco (per le prove)."""
    if testo is None:
        testo = (ROOT / file).read_text(encoding="utf-8", errors="replace")
    proprie = cache.setdefault(file, sezioni(testo))
    esito: list[Rimando] = []
    in_codice = False
    righe = testo.splitlines()
    for n, riga in enumerate(righe, 1):
        if riga.lstrip().startswith("```"):
            in_codice = not in_codice
            continue
        if in_codice or TITOLO.match(riga):
            continue
        intorno = "\n".join(righe[max(0, n - 3):n + 1])  # due righe prima, la riga, la dopo
        presi: list[tuple[int, int]] = []
        for m in ESTERNO.finditer(riga):
            nome = m.group("nome")
            if nome.lower() in {"vedi", "il", "del", "al", "nel", "in", "dal", "cfr", "cfr.", "e", "ed", "o"}:
                continue
            presi.append(m.span())
            bersaglio, perche = risolvi(nome, idx, tutti)
            if bersaglio is None:
                esito.append(Rimando(file, n, m.group(0), nome, m.group("n"), "non_verificabile", perche))
                continue
            sez = cache.setdefault(bersaglio, sezioni((ROOT / bersaglio).read_text(encoding="utf-8", errors="replace")))
            if not sez:
                esito.append(Rimando(file, n, m.group(0), bersaglio, m.group("n"), "non_verificabile",
                                     "il bersaglio non numera le sezioni"))
            elif m.group("n") in sez:
                esito.append(Rimando(file, n, m.group(0), bersaglio, m.group("n"), "ok"))
            elif (file, m.group(0)) in IN_ATTESA:
                esito.append(Rimando(file, n, m.group(0), bersaglio, m.group("n"), "in_attesa",
                                     IN_ATTESA[(file, m.group(0))]))
            else:
                esito.append(Rimando(file, n, m.group(0), bersaglio, m.group("n"), "violazione",
                                     f"sezioni del bersaglio: {', '.join(sorted(sez, key=int)[:12])}"))
        for m in INTERNO.finditer(riga):
            if any(a <= m.start("n") < b for a, b in presi):
                continue
            elenco = riga.lstrip().startswith("|") and riga.count("§") > 1
            if elenco or ALTRO_DOCUMENTO.search(intorno) or DOPO_ALTRO.match(riga[m.end():]):
                esito.append(Rimando(file, n, m.group(0), "?", m.group("n"), "non_verificabile",
                                     "la riga o le vicine nominano un altro documento, o è un elenco di §: il § può non essere di questo file"))
                continue
            if not proprie:
                esito.append(Rimando(file, n, m.group(0), file, m.group("n"), "non_verificabile",
                                     "il file non numera le sezioni"))
            elif m.group("n") in proprie:
                esito.append(Rimando(file, n, m.group(0), file, m.group("n"), "ok"))
            else:
                esito.append(Rimando(file, n, m.group(0), file, m.group("n"), "violazione",
                                     f"sezioni del file: {', '.join(sorted(proprie, key=int)[:12])}"))
    return esito


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("percorsi", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    tutti = _md_del_repo()
    idx = indice_nomi(tutti)
    scelti = a.percorsi or [f for f in tutti if RADICI.match(f) and not ESCLUSI.search(f)]
    cache: dict[str, set[str]] = {}
    tutti_r = [r for f in scelti for r in rimandi(f, idx, tutti, cache)]
    viol = [r for r in tutti_r if r.esito == "violazione"]
    if a.json:
        print(json.dumps([asdict(r) for r in tutti_r if r.esito != "ok"], ensure_ascii=False, indent=1))
    else:
        for r in viol:
            print(f"✗ {r.file}:{r.riga} «{r.testo}» → {r.bersaglio} non ha §{r.sezione} ({r.motivo})")
        for r in tutti_r:
            if r.esito == "in_attesa":
                print(f"… {r.file}:{r.riga} «{r.testo}» in attesa: {r.motivo}")
        conta = {k: sum(1 for r in tutti_r if r.esito == k)
                 for k in ("ok", "violazione", "in_attesa", "non_verificabile")}
        print(f"{len(scelti)} file, {len(tutti_r)} rimandi: {conta['ok']} tornano, "
              f"{conta['violazione']} violazioni, {conta['in_attesa']} in attesa del DM, "
              f"{conta['non_verificabile']} non verificabili")
    return 1 if viol and a.check else 0


if __name__ == "__main__":
    sys.exit(main())
