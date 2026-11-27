"""Banco di semina per la *d* eufonica: quanto trova il rilevatore, e dove.

Il corpus è a zero, quindi contare i rilievi non dice se il rilevatore vede: 0
può voler dire «pulito» o «cieco». Qui si **seminano** errori noti, in modo
deterministico, in una copia in memoria di ogni file di contenuto, e si conta
quante righe seminate il rilevatore segnala (richiamo), divise per il posto in
cui stanno: riga normale, citazione (`>`), tabella, riga rientrata che per
CommonMark è prosa (seguito di un elenco o di un paragrafo), riga rientrata che
è codice davvero, recinto di codice. Nelle ultime due il rilievo giusto è
**nessuno**.

Semi (solo minuscole, fuori da codice inline, link e nomi di file):
  «ad a…» → «a a…»   «ed e…» → «e e…»       (la d che manca)
  «a e/i/o/u…» → «ad …»   «e a/i/o/u…» → «ed …»   (la d che avanza; non «a esempio»)

Il posto di ogni riga lo dice **markdown-it-py** (il parser CommonMark di
riferimento in Python), che serve solo a questo banco. Con un indirizzo locale
si misura anche LanguageTool (ST_03_001) sugli stessi semi.

    python3 plans/esperimenti/d-eufonica-limiti-2026-11-11/semina.py [http://127.0.0.1:8081]
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

RADICE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RADICE / "scripts"))
import ciclo_prosa  # noqa: E402
import validate_lingua as V  # noqa: E402
from markdown_it import MarkdownIt  # noqa: E402

MD = MarkdownIt("commonmark").enable("table")
PRIMA = r"(?<![\w'’])"
SEMI = [
    (re.compile(PRIMA + r"ad (?=[aà]\w)"), "a "),
    (re.compile(PRIMA + r"ed (?=[eèé]\w)"), "e "),
    (re.compile(PRIMA + r"a (?!esempio|es\.)(?=[eèéiìoòuù]\w)"), "ad "),
    (re.compile(PRIMA + r"e (?=[aàiìoòuù]\w)"), "ed "),
]
POSTI = ("normale", "citazione", "tabella", "rientrata-prosa", "rientrata-codice", "recinto")
SENZA_RILIEVO = ("rientrata-codice", "recinto")


def posti(testo: str) -> dict[int, str]:
    righe = testo.split("\n")
    out: dict[int, str] = {}
    fm = 0
    if righe and righe[0].strip() == "---":
        for i, r in enumerate(righe[1:], 2):
            if r.strip() == "---":
                fm = i
                break
    corpo = "\n".join([""] * fm + righe[fm:])       # stesse righe, front-matter vuoto
    codice: dict[int, str] = {}
    for tok in MD.parse(corpo):
        if tok.map and tok.type in ("code_block", "fence"):
            for n in range(tok.map[0] + 1, tok.map[1] + 1):
                codice[n] = "rientrata-codice" if tok.type == "code_block" else "recinto"
    for n, r in enumerate(righe, 1):
        if n <= fm or not r.strip():
            continue
        if n in codice:
            out[n] = codice[n]
        elif r.startswith("    ") or r.startswith("\t"):
            out[n] = "rientrata-prosa"
        elif r.lstrip().startswith(">"):
            out[n] = "citazione"
        elif r.lstrip().startswith("|"):
            out[n] = "tabella"
        else:
            out[n] = "normale"
    return out


def semina(testo: str) -> tuple[str, set[int]]:
    righe = testo.split("\n")
    seminate: set[int] = set()
    for i, riga in enumerate(righe):
        maschera = V.INLINE.sub(lambda m: V.MASCHERA * len(m.group(0)), riga)
        tagli = sorted(((m.start(), m.end(), nuovo) for rx, nuovo in SEMI
                        for m in rx.finditer(maschera)), reverse=True)
        for a, b, nuovo in tagli:
            riga = riga[:a] + nuovo + riga[b:]
        if tagli:
            righe[i] = riga
            seminate.add(i + 1)
    return "\n".join(righe), seminate


def regex_righe(testo: str) -> set[int]:
    return {n for n, _ in V.d_eufonica_righe(list(V.righe_da_controllare(testo)))}


def lt_righe(testo: str, url: str) -> set[int]:
    piano = ciclo_prosa.testo_piano(testo)
    dati = urllib.parse.urlencode({"text": piano, "language": "it", "enabledOnly": "true",
                                   "enabledRules": "ST_03_001"}).encode()
    with urllib.request.urlopen(url.rstrip("/") + "/v2/check", dati, timeout=600) as r:
        risposta = json.load(r)
    u = piano.encode("utf-16-le")
    return {u[:2 * m["offset"]].decode("utf-16-le", "replace").count("\n") + 1
            for m in risposta.get("matches", [])}


def main(argv: list[str]) -> int:
    url = argv[1] if len(argv) > 1 else ""
    if url and urllib.parse.urlsplit(url).hostname not in ("localhost", "127.0.0.1", "::1"):
        print("solo un server locale")
        return 2
    semi: Counter = Counter()
    presi = {"regex": Counter(), "lt": Counter()}
    falsi = {"regex": 0, "lt": 0}
    persi: list[str] = []
    for f in V.file_di_contenuto():
        testo = f.read_text(encoding="utf-8", errors="ignore")
        dove = posti(testo)
        nuovo, seminate = semina(testo)
        lettori = {"regex": regex_righe(nuovo)}
        if url:
            lettori["lt"] = lt_righe(nuovo, url)
        for n in seminate:
            semi[dove.get(n, "normale")] += 1
        for nome, trovate in lettori.items():
            for n in trovate:
                if n in seminate:
                    presi[nome][dove.get(n, "normale")] += 1
            # la «a capo» segnala la riga prima: una riga non seminata accanto a una seminata non è un falso
            falsi[nome] += sum(1 for n in trovate if n not in seminate and n + 1 not in seminate)
        for n in sorted(seminate - lettori["regex"]):
            if dove.get(n) not in SENZA_RILIEVO:
                persi.append(f"{f.relative_to(RADICE)}:{n} [{dove.get(n)}] {nuovo.split(chr(10))[n-1].strip()[:90]}")
    print("| Posto | Righe seminate | Regex | LanguageTool |")
    print("|---|---:|---:|---:|")
    for p in POSTI:
        if not semi[p]:
            continue
        cella = lambda k: f"{presi[k][p]} ({100 * presi[k][p] / semi[p]:.1f}%)"  # noqa: E731
        print(f"| {p} | {semi[p]} | {cella('regex')} | {cella('lt') if url else '—'} |")
    dentro = sum(semi[p] for p in POSTI if p not in SENZA_RILIEVO)
    for k in ("regex",) + (("lt",) if url else ()):
        t = sum(presi[k][p] for p in POSTI if p not in SENZA_RILIEVO)
        print(f"{k}: richiamo sulla prosa {t}/{dentro} ({100 * t / dentro:.2f}%), "
              f"rilievi nel codice {sum(presi[k][p] for p in SENZA_RILIEVO)}, "
              f"rilievi su righe non seminate {falsi[k]}")
    print(f"\nsemi di prosa che la regex perde: {len(persi)}")
    for r in persi[:80]:
        print("  " + r)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
