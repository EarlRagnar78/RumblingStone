#!/usr/bin/env python3
"""banco_prosa_locale.py — un modello locale sugli stessi dieci casi delle skill di scrittura.

ADR-0089 (I2, 2026-10-10). In CI gira solo senza il servizio (`--dry-run`,
`coppie`, `esito`). È un ponte nel senso di ADR-0067: chiama
un servizio, degrada pulito senza, e ciò che produce è un candidato che entra
nel repo dalla porta normale, cioè una cartella di `plans/scrittura/corse/` che
`voto_scrittura.py --corse` vota come tutte le altre.

Tre comandi, tre domande diverse:

    corsa   «il modello locale rispetta le norme registrate?»
            Genera i dieci casi di `plans/scrittura/casi.json` contro un endpoint
            compatibile OpenAI (Ollama, llama.cpp `llama-server`, vLLM, LM Studio:
            tutti espongono /v1/chat/completions) e li scrive in
            `plans/scrittura/corse/L-<etichetta>-<n>/`, con `corsa.json` accanto
            (modello, parametri, tempi, impronta del prompt). Il voto lo dà
            `voto_scrittura.py --corse`, invariato.

    coppie  «la prosa è migliore?» — la domanda che nessun controllo risponde.
            Prepara un foglio alla cieca per il DM: per ogni caso, il testo di
            due corse in ordine casuale (seme dichiarato), senza il nome della
            condizione. La chiave sta in un file a parte.

    esito   legge il foglio compilato e la chiave: quota di preferenze per la
            condizione sfidante con l'intervallo di Wilson al 95%, e — se c'è
            anche un foglio compilato da un giudice automatico — il κ di Cohen
            fra giudice e DM (la soglia del repo è 0,60, campioni_kappa.py).

Il giudice automatico è facoltativo e **non decide**: ADR-0036 vale anche qui,
il tavolo vince sul modello.

    python3 scripts/banco_prosa_locale.py corsa --url http://127.0.0.1:8080/v1 \
        --modello gemma4-26b-a4b --etichetta gemma26moe --ripetizione 1
    python3 scripts/banco_prosa_locale.py corsa --dry-run          # solo il prompt
    python3 scripts/banco_prosa_locale.py coppie --a B-con-1 --b L-gemma26moe-1 \
        --seme 7 -o /tmp/foglio.md
    python3 scripts/banco_prosa_locale.py esito /tmp/foglio.md     # dopo la compilazione
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
CASI = RADICE / "plans" / "scrittura" / "casi.json"
CORSE = RADICE / "plans" / "scrittura" / "corse"
# Le prove parziali (--caso) servono a misurare i tempi: non sono corse, e
# voto_scrittura non deve vederle. Cartella fuori da git.
PROVE = RADICE / "plans" / "scrittura" / "prove-locali"
NS = RADICE / "skills" / "rumblingstone-narrative-style"
PD = RADICE / "skills" / "rumblingstone-prosa-documenti"

# I references che AGENTS.md dichiara obbligatori per la prosa di gioco. Per i
# documenti, la skill opposta (ADR-0035: mai le due insieme).
OBBLIGATORI_GIOCO = [NS / "SKILL.md"] + [NS / "references" / f for f in (
    "italiano-nativo.md", "read-aloud-adulti.md", "editorial-standards.md", "style-pillars.md")]
OBBLIGATORI_DOC = [PD / "SKILL.md"]

RE_FILE = re.compile(r"«([^»]+\.md)»")
RE_PUNTO = re.compile(r"(Scena \d+|Zona \d+|§\s?\d+)")


class ServizioAssente(Exception):
    pass


# ---------------------------------------------------------------- prompt

def _leggi(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def estratto(testo: str, punto: "str | None", tetto: int) -> str:
    """La sezione del master che il caso nomina, dal titolo al titolo dello
    stesso livello. Senza un punto riconosciuto, l'inizio del file. Sempre
    entro `tetto` caratteri: un modello locale non regge un master intero."""
    righe = testo.splitlines()
    if punto:
        chiave = re.compile(r"\s*".join(map(re.escape, punto.split())) + r"\b", re.I)
        titoli = [(i, re.match(r"^(#+)\s+(.*)", r)) for i, r in enumerate(righe)]
        titoli = [(i, m) for i, m in titoli if m and chiave.search(m.group(2))]
        # Il titolo che COMINCIA con il punto («### SCENA 11 — …») batte quello
        # che lo cita fra parentesi («### A.1 · Skullcrusher (Scena 11)»).
        titoli.sort(key=lambda t: (chiave.match(re.sub(r"^\W+", "", t[1].group(2))) is None, t[0]))
        if titoli:
            i, m = titoli[0]
            livello = len(m.group(1))
            fine = len(righe)
            for j in range(i + 1, len(righe)):
                m2 = re.match(r"^(#+)\s", righe[j])
                if m2 and len(m2.group(1)) <= livello:
                    fine = j
                    break
            return "\n".join(righe[i:fine])[:tetto]
    return testo[:tetto]


def componi(caso: dict, contesto: str, tetto_fonte: int) -> "tuple[str, str]":
    """(system, user). `contesto`: «pieno» carica i references obbligatori
    interi, «ridotto» il solo SKILL.md, «nessuno» niente (la condizione
    A-senza, ma senza AGENTS.md)."""
    doc = caso["genere"] == "documento"
    fonti = OBBLIGATORI_DOC if doc else OBBLIGATORI_GIOCO
    if contesto == "ridotto":
        fonti = fonti[:1]
    elif contesto == "nessuno":
        fonti = []
    parti = [
        "Sei l'autore della campagna RumblingStone (D&D 3.5, Faerûn 1372 DR). "
        "Scrivi in italiano. Rispondi con il solo testo richiesto, in Markdown, "
        "senza preamboli. Le norme che seguono sono vincolanti.",
    ]
    for f in fonti:
        parti.append(f"\n\n===== {f.relative_to(RADICE)} =====\n{_leggi(f)}")
    system = "".join(parti)

    user = caso["prompt"]
    m = RE_FILE.search(user)
    if m:
        sorgente = RADICE / m.group(1)
        punto = RE_PUNTO.search(user)
        brano = estratto(_leggi(sorgente), punto.group(1) if punto else None, tetto_fonte)
        if brano:
            # Un agente con gli strumenti apre il file da solo; un modello
            # locale senza strumenti no. Il brano è il suo unico grounding.
            user += f"\n\n----- estratto da {m.group(1)} -----\n{brano}"
    return system, user


# Un token italiano di questi prompt vale da 3,3 a 3,4 caratteri (le due corse
# sull'ASUS, 2026-10-10 e 2026-10-11, contate dai prompt_tokens del server).
# Il controllo prima della chiamata usa 3,3, il valore più basso misurato:
# con 3 i prompt cresciuti con le norme di main (89.000 caratteri) venivano
# rifiutati a 32k pur entrandoci con 3.000 token di margine, e un taglio che
# sfugge qui lo prende comunque `avvisi`. Per riconoscere un prompt tagliato si
# stima stretto (5): sotto, il server ne ha buttato via una parte.
CAR_PER_TOKEN_LARGO, CAR_PER_TOKEN_STRETTO = 3.3, 5


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(RADICE))
    except ValueError:
        return str(p)


def stima_token(*testi: str) -> int:
    return int(sum(len(t) for t in testi) / CAR_PER_TOKEN_LARGO)


def avvisi(caratteri: int, uso: dict, fine: "str | None", testo: str) -> "list[str]":
    """Perché un caso non vale come misura. Il 2026-10-10 quattro prompt su dieci
    hanno superato il contesto del server: llama.cpp li ha tagliati a metà
    senza errore, e il modello ha scritto senza metà delle norme."""
    out = []
    pt = uso.get("prompt_tokens")
    if isinstance(pt, int) and pt < caratteri // CAR_PER_TOKEN_STRETTO:
        out.append(f"prompt tagliato dal server ({pt} token per {caratteri} caratteri)")
    if fine == "length":
        out.append("risposta interrotta al tetto di token")
    if not testo.strip():
        out.append("risposta vuota")
    return out


def impronta(*testi: str) -> str:
    h = hashlib.sha256()
    for t in testi:
        h.update(t.encode("utf-8"))
    return h.hexdigest()[:16]


# ---------------------------------------------------------------- servizio

def chiama(url: str, modello: str, system: str, user: str, temperatura: float,
           seme: int, max_token: int, timeout: int) -> "tuple[str, dict, str | None]":
    corpo = json.dumps({
        "model": modello,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "temperature": temperatura,
        "seed": seme,
        "max_tokens": max_token,
        "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(url.rstrip("/") + "/chat/completions", data=corpo,
                                 headers={"Content-Type": "application/json"})
    chiave = os.environ.get("BANCO_API_KEY")
    if chiave:
        req.add_header("Authorization", f"Bearer {chiave}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            dati = json.loads(r.read().decode("utf-8"))
    except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
        raise ServizioAssente(f"{url}: {getattr(e, 'reason', e)}") from None
    try:
        testo = dati["choices"][0]["message"]["content"] or ""
        fine = dati["choices"][0].get("finish_reason")
    except (KeyError, IndexError, TypeError):
        raise ServizioAssente(f"{url}: risposta senza choices[0].message.content") from None
    return pulisci(testo) + "\n", dati.get("usage", {}), fine


def pulisci(testo: str) -> str:
    """Toglie il ragionamento che i modelli lasciano nel testo quando il server
    non lo separa: `<think>…</think>`, e il blocco di Gemma 4, che c'è anche
    vuoto a pensiero spento (`<|channel>thought…<channel|>`)."""
    testo = re.sub(r"<think>.*?</think>\s*", "", testo, flags=re.S)
    return re.sub(r"<\|channel>thought.*?<channel\|>\s*", "", testo, flags=re.S).strip()


def cmd_corsa(a) -> int:
    casi = json.loads(CASI.read_text(encoding="utf-8"))["casi"]
    if a.insieme != "tutti":
        casi = [c for c in casi if c["insieme"] == a.insieme]
    if a.caso:
        casi = [c for c in casi if c["id"] in a.caso]
    if a.dry_run:
        for c in casi:
            s, u = componi(c, a.contesto, a.tetto_fonte)
            print(f"{c['id']} {c['genere']:<16} system {len(s):>7} car (~{len(s)//4} tok) · "
                  f"user {len(u):>6} car · impronta {impronta(s, u)}")
        return 0
    if not a.url or not a.modello:
        print("✗ banco_prosa_locale corsa: servono --url e --modello (o --dry-run)", file=sys.stderr)
        return 2
    if a.ctx:
        troppo = [(c["id"], stima_token(*componi(c, a.contesto, a.tetto_fonte)))
                  for c in casi]
        troppo = [(i, n) for i, n in troppo if n + a.max_token > a.ctx]
        if troppo:
            for i, n in troppo:
                print(f"✗ {i}: ~{n} token di prompt + {a.max_token} di risposta superano "
                      f"il contesto del server ({a.ctx})", file=sys.stderr)
            print("  Il server taglierebbe il prompt senza dirlo. Alza il contesto "
                  "(LLM_CTX, OLLAMA_CONTEXT_LENGTH) o usa --contesto ridotto.", file=sys.stderr)
            return 4
    nome = f"L-{a.etichetta}-{a.ripetizione}"
    dest = (PROVE if a.caso else CORSE) / nome
    if dest.exists() or (PROVE / nome).exists():
        print(f"✗ {rel(dest)} esiste già: cambia --ripetizione", file=sys.stderr)
        return 2
    # Si scrive in una cartella temporanea e si sposta alla fine: una corsa
    # interrotta non lascia mai una cartella che voto_scrittura conterebbe.
    tmp = Path(tempfile.mkdtemp(prefix=f"banco-{nome}-"))
    meta = {"corsa": nome, "modello": a.modello, "url": a.url, "contesto": a.contesto,
            "temperatura": a.temperatura, "seme": a.seme, "max_token": a.max_token,
            "tetto_fonte": a.tetto_fonte, "ctx": a.ctx or None, "inizio": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "casi": {}}
    try:
        for c in casi:
            s, u = componi(c, a.contesto, a.tetto_fonte)
            t0 = time.monotonic()
            testo, uso, fine = chiama(a.url, a.modello, s, u, a.temperatura, a.seme,
                                      a.max_token, a.timeout)
            dt = round(time.monotonic() - t0, 1)
            (tmp / f"{c['id']}.md").write_text(testo, encoding="utf-8")
            av = avvisi(len(s) + len(u), uso, fine, testo)
            meta["casi"][c["id"]] = {"secondi": dt, "uso": uso, "fine": fine,
                                     "avvisi": av, "impronta_prompt": impronta(s, u)}
            print(f"  {c['id']} {dt:>6}s  {uso.get('completion_tokens', '?')} token"
                  + "".join(f"  ⚠ {x}" for x in av))
    except ServizioAssente as e:
        for f in tmp.iterdir():
            f.unlink()
        tmp.rmdir()
        print(f"✗ servizio non raggiungibile ({e}). Avvia Ollama o llama-server e riprova; "
              "nessun file scritto.", file=sys.stderr)
        return 3
    guasti = {i: m["avvisi"] for i, m in meta["casi"].items() if m["avvisi"]}
    if guasti and dest.parent == CORSE:
        # Una corsa con un caso guasto misura il server, non il modello: resta
        # da leggere, ma fuori dal voto.
        dest = PROVE / nome
        meta["fuori_dal_voto"] = guasti
    (tmp / "corsa.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                    encoding="utf-8")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(tmp), dest)
    tot = sum(m["secondi"] for m in meta["casi"].values())
    print(f"✓ {rel(dest)}: {len(casi)} casi in {tot:.0f} s.")
    if guasti:
        print(f"⚠ {len(guasti)} casi guasti ({', '.join(guasti)}): la corsa è in "
              f"{rel(dest)}, fuori dal voto. Correggi e rifalla.")
        return 5
    if a.caso:
        print("  È una prova dei tempi: non entra nel voto. Per la corsa vera togli --caso.")
    else:
        print("  Ora: python3 scripts/voto_scrittura.py --corse")
    return 0


# ---------------------------------------------------------------- coppie

def cmd_coppie(a) -> int:
    casi = json.loads(CASI.read_text(encoding="utf-8"))["casi"]
    rng = random.Random(a.seme)
    chiave = {"a": a.a, "b": a.b, "seme": a.seme, "ordine": {}}
    out = ["# Foglio alla cieca", "",
           "Per ogni caso, due testi. Scrivi **1** o **2** (o **=** se non vedi "
           "differenze) dopo «Preferito:». Leggi ad alta voce, come al tavolo.", ""]
    for c in casi:
        ta, tb = CORSE / a.a / f"{c['id']}.md", CORSE / a.b / f"{c['id']}.md"
        if not (ta.is_file() and tb.is_file()):
            continue
        coppia = [("a", ta), ("b", tb)]
        rng.shuffle(coppia)
        chiave["ordine"][c["id"]] = [k for k, _ in coppia]
        out += [f"## {c['id']} · {c['genere']}", "", f"> {c['prompt']}", ""]
        for i, (_, p) in enumerate(coppia, 1):
            out += [f"### Testo {i}", "", p.read_text(encoding="utf-8").strip(), ""]
        out += ["Preferito: ", ""]
    foglio = Path(a.o)
    foglio.write_text("\n".join(out), encoding="utf-8")
    foglio.with_suffix(".chiave.json").write_text(json.dumps(chiave, indent=2) + "\n",
                                                  encoding="utf-8")
    print(f"✓ {foglio} ({len(chiave['ordine'])} coppie); chiave in {foglio.with_suffix('.chiave.json')}")
    return 0


def leggi_preferenze(foglio: Path) -> "dict[str, str]":
    pref, caso = {}, None
    for r in foglio.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (S\d+)", r)
        if m:
            caso = m.group(1)
        m = re.match(r"^Preferito:\s*([12=])", r)
        if m and caso:
            pref[caso] = m.group(1)
    return pref


def wilson(k: int, n: int, z: float = 1.96) -> "tuple[float, float]":
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - m), min(1.0, c + m))


def kappa(x: "list[str]", y: "list[str]") -> float:
    n = len(x)
    if n == 0:
        return float("nan")
    po = sum(i == j for i, j in zip(x, y)) / n
    cat = set(x) | set(y)
    pe = sum((x.count(c) / n) * (y.count(c) / n) for c in cat)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def in_condizione(pref: "dict[str, str]", chiave: dict) -> "dict[str, str]":
    """1/2 del foglio -> 'a'/'b'/'='."""
    out = {}
    for cid, v in pref.items():
        if cid in chiave["ordine"]:
            out[cid] = "=" if v == "=" else chiave["ordine"][cid][int(v) - 1]
    return out


def cmd_esito(a) -> int:
    foglio = Path(a.foglio)
    chiave = json.loads(foglio.with_suffix(".chiave.json").read_text(encoding="utf-8"))
    dm = in_condizione(leggi_preferenze(foglio), chiave)
    decisi = [v for v in dm.values() if v != "="]
    vb = decisi.count("b")
    lo, hi = wilson(vb, len(decisi))
    print(f"{chiave['b']} preferita a {chiave['a']}: {vb}/{len(decisi)} "
          f"({100*vb/len(decisi) if decisi else 0:.0f}%), Wilson 95% [{lo:.2f}, {hi:.2f}]; "
          f"pari: {list(dm.values()).count('=')}")
    if hi < 0.5:
        print("  → la sfidante perde in modo netto")
    elif lo > 0.5:
        print("  → la sfidante vince in modo netto")
    else:
        print("  → non si distingue con questi casi: servono più coppie")
    if a.giudice:
        g = in_condizione(leggi_preferenze(Path(a.giudice)), chiave)
        comuni = sorted(set(dm) & set(g))
        k = kappa([dm[c] for c in comuni], [g[c] for c in comuni])
        po = sum(dm[c] == g[c] for c in comuni) / len(comuni) if comuni else 0
        # Con preferenze sbilanciate (il DM sceglie quasi sempre la stessa
        # condizione) il κ crolla anche con un accordo alto: è il paradosso di
        # Feinstein e Cicchetti. Si stampano tutti e due, e si legge il κ.
        print(f"κ giudice/DM su {len(comuni)} coppie: {k:.2f} "
              f"({'sopra' if k >= 0.60 else 'sotto'} la soglia 0,60 di campioni_kappa); "
              f"accordo grezzo {100*po:.0f}%")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("corsa")
    c.add_argument("--url", default=os.environ.get("BANCO_URL"))
    c.add_argument("--modello", default=os.environ.get("BANCO_MODELLO"))
    c.add_argument("--etichetta", default="locale")
    c.add_argument("--ripetizione", type=int, default=1)
    c.add_argument("--contesto", choices=("pieno", "ridotto", "nessuno"), default="pieno")
    c.add_argument("--insieme", choices=("tutti", "taratura", "verifica"), default="tutti")
    c.add_argument("--caso", action="append", help="solo questo caso (ripetibile), es. S02 per la prova dei tempi")
    c.add_argument("--temperatura", type=float, default=0.7)
    c.add_argument("--seme", type=int, default=1)
    c.add_argument("--max-token", type=int, default=3000)
    c.add_argument("--ctx", type=int, default=int(os.environ.get("BANCO_CTX", "0")),
                   help="il contesto del server in token: sopra, la corsa non parte")
    c.add_argument("--tetto-fonte", type=int, default=12000)
    c.add_argument("--timeout", type=int, default=900)
    c.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("coppie")
    p.add_argument("--a", required=True, help="corsa di riferimento, es. B-con-1")
    p.add_argument("--b", required=True, help="corsa sfidante, es. L-qwen27-1")
    p.add_argument("--seme", type=int, default=7)
    p.add_argument("-o", required=True)
    e = sub.add_parser("esito")
    e.add_argument("foglio")
    e.add_argument("--giudice", help="lo stesso foglio compilato da un giudice automatico")
    a = ap.parse_args(argv)
    return {"corsa": cmd_corsa, "coppie": cmd_coppie, "esito": cmd_esito}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
