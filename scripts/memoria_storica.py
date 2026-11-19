#!/usr/bin/env python3
"""memoria_storica.py — la storia del lavoro che esce dalla memoria corta, cercabile.

Il DM, il 2026-11-12: *«evitare sempre la saturazione ed evitare di perdere
informazioni storiche che potrebbero essere importanti per una eventuale
regressione od una rivisitazione di soluzioni già adottate»*, e *«un
meccanismo che se ha necessità legga questo file per recuperare la parte di
memoria storica richiesta»* (ADR-0127).

La memoria del progetto (quella che ogni sessione d'agente legge all'avvio)
ha un limite di dimensione e tiene solo regole, stato aperto e puntatori.
Prima che una riga ne esca, i suoi fatti vanno in `plans/MEMORIA-STORICA.md`,
una voce `MS-NNNN` per riga, con data, PR, ADR e temi. Il file non ha limite
e non si riassume: si aggiunge in coda. Questo script lo **legge**:

    python3 scripts/memoria_storica.py --pr 242          # la storia di una PR
    python3 scripts/memoria_storica.py --adr 93          # di un ADR (0093)
    python3 scripts/memoria_storica.py --tema prosa      # di un tema
    python3 scripts/memoria_storica.py Skullcrusher      # parole nel testo
    python3 scripts/memoria_storica.py --da 2026-10-19 --a 2026-10-20
    python3 scripts/memoria_storica.py --elenco          # id, data e titolo
    python3 scripts/memoria_storica.py --json ...        # per un agente
    python3 scripts/memoria_storica.py --check           # il cancello della CI
    python3 scripts/memoria_storica.py --confronta-memoria DIR   # cosa della memoria
                                                         # delle sessioni non è nel repo
    python3 scripts/memoria_storica.py --tetto-memoria DIR       # MEMORY.md sotto il tetto?

`--pr N` trova anche le voci che la PR ha aggiunto senza scriversi il numero
(campo PR «—», perché il numero nasce dopo il commit): lo ricava da git, dal
merge «Merge pull request #N» che ha portato la voce su main (ADR-0137).

I filtri si sommano (tutti devono valere). `--check` controlla la forma
(numeri consecutivi, date valide, campi obbligatori) e che il CHANGELOG dei
piani porti al file: una voce scritta male non si trova più con i filtri.

Solo stdlib, nessuna rete, sola lettura.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
FILE = RADICE / "plans" / "MEMORIA-STORICA.md"
CHANGELOG = RADICE / "plans" / "CHANGELOG.md"
LINK = "MEMORIA-STORICA.md"

TESTA = re.compile(r"^### (MS-(\d{4})) · (\S+) · (.+?)\s*$")
CAMPO = re.compile(r"^- \*\*([^*]+):\*\* ?(.*)$")
OBBLIGATORI = ("Data", "PR", "ADR", "Temi", "Origine", "Testo")


@dataclass
class Voce:
    id: str
    numero: int
    data: str
    titolo: str
    riga: int
    campi: "dict[str, str]" = field(default_factory=dict)
    testo_md: str = ""
    pr_merge: "set[int]" = field(default_factory=set)

    @property
    def pr(self) -> "set[int]":
        return {int(x) for x in re.findall(r"#(\d+)", self.campi.get("PR", ""))} | self.pr_merge

    @property
    def adr(self) -> "set[int]":
        return {int(x) for x in re.findall(r"ADR-(\d{4})", self.campi.get("ADR", ""))}

    @property
    def temi(self) -> "list[str]":
        return self.campi.get("Temi", "").split()


def leggi(testo: str) -> "list[Voce]":
    """Le voci del file, nell'ordine in cui stanno. Il testo fuori dalle voci è intestazione."""
    voci: "list[Voce]" = []
    corrente: "Voce | None" = None
    righe: "list[str]" = []
    for n, r in enumerate(testo.splitlines(), 1):
        m = TESTA.match(r)
        if m:
            if corrente:
                corrente.testo_md = "\n".join(righe).rstrip()
            corrente = Voce(m.group(1), int(m.group(2)), m.group(3), m.group(4), n)
            voci.append(corrente)
            righe = [r]
            continue
        if corrente is None:
            continue
        if r.startswith("## "):          # una sezione nuova chiude l'ultima voce
            corrente.testo_md = "\n".join(righe).rstrip()
            corrente = None
            continue
        righe.append(r)
        c = CAMPO.match(r)
        if c:
            corrente.campi[c.group(1).strip()] = c.group(2).strip()
    if corrente:
        corrente.testo_md = "\n".join(righe).rstrip()
    return voci


_MERGE = re.compile(r"^Merge pull request #(\d+)|\(#(\d+)\)\s*$")


def pr_dai_merge(radice: "Path | None" = None, file: Path = FILE) -> "dict[str, set[int]]":
    """MS-NNNN → le PR il cui merge (primo genitore) ha aggiunto la testa della voce.

    Una voce si scrive prima che la PR abbia un numero: 82 voci su 98 dal
    2026-11-12 hanno «PR: —». Il numero sta nel messaggio del merge, e git lo
    sa. Senza git o in un clone shallow il dizionario è solo più corto.
    """
    try:
        if radice is None:     # il repo del file, non per forza questo (--file)
            radice = Path(subprocess.run(
                ["git", "-C", str(file.resolve().parent), "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, check=True, timeout=30).stdout.strip())
        rel = file.resolve().relative_to(radice.resolve())
        out = subprocess.run(
            ["git", "-C", str(radice), "log", "--first-parent", "-m", "--unified=0",
             "--format=@@@%s", "-p", "--", str(rel)],
            capture_output=True, text=True, check=True, timeout=120).stdout
    except (ValueError, OSError, subprocess.SubprocessError):
        return {}
    mappa: "dict[str, set[int]]" = {}
    corrente = None
    for r in out.splitlines():
        if r.startswith("@@@"):
            m = _MERGE.search(r[3:])
            corrente = int(m.group(1) or m.group(2)) if m else None
        elif corrente and r.startswith("+### MS-"):
            t = TESTA.match(r[1:])
            if t:
                mappa.setdefault(t.group(1), set()).add(corrente)
    return mappa


# Cosa di una riga di memoria si può cercare nel repo senza capirla: numeri di
# PR, ADR e voci, SHA, percorsi e nomi fra apici inversi.
_TOKEN = re.compile(r"#\d{3,4}\b|\bADR-\d{4}\b|\bMS-\d{4}\b|\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,8}\b"
                    r"|`([^`\s][^`]{2,80})`|\b[\w.-]+/[\w./-]+\.(?:md|py|json|toml|yaml|txt|pdf|png|sh)\b")


def _gettoni(riga: str) -> "list[str]":
    fuori = []
    for m in _TOKEN.finditer(riga):
        t = m.group(1) or m.group(0)
        if t not in fuori:
            fuori.append(t)
    return fuori


def _corpo_del_repo(radice: Path) -> str:
    """Il testo dei file tracciati più i messaggi dei commit (lì stanno SHA e numeri di PR)."""
    parti = []
    try:
        files = subprocess.run(["git", "-C", str(radice), "ls-files", "-z"], capture_output=True,
                               text=True, check=True, timeout=60).stdout.split("\0")
        parti.append(subprocess.run(["git", "-C", str(radice), "log", "--format=%h %H %s %b"],
                                    capture_output=True, text=True, check=True, timeout=120).stdout)
    except (OSError, subprocess.SubprocessError):
        files = []
    for f in files:
        if f.endswith((".md", ".json", ".toml", ".yaml", ".yml", ".txt", ".py", ".sh", ".tsv")):
            try:
                parti.append(f)
                parti.append((radice / f).read_text(encoding="utf-8", errors="replace"))
            except OSError:
                pass
    return "\n".join(parti)


def confronta_memoria(cartella: Path, radice: Path = RADICE, storica: str = "") -> dict:
    """Per ogni riga della memoria delle sessioni, i gettoni che il repo non ha.

    Non decide se una riga è archiviata: dice dove guardare. Una riga senza
    gettoni (una regola in prosa) non si può controllare così e lo si dichiara.
    """
    corpo = _corpo_del_repo(radice)
    note, righe_tot, con_gettoni, scoperte = [], 0, 0, []
    visti: "dict[str, bool]" = {}
    for f in sorted(cartella.glob("*.md")):
        nome = f.stem
        testo = f.read_text(encoding="utf-8", errors="replace")
        if nome != "MEMORY":
            note.append({"nota": nome, "citata_nella_storica": nome in storica})
        for n, r in enumerate(testo.splitlines(), 1):
            if not r.strip() or r.startswith("---") or r.startswith(("name:", "description:", "metadata:", "  type:", "  modified:")):
                continue
            righe_tot += 1
            g = _gettoni(r)
            if not g:
                continue
            con_gettoni += 1
            for t in g:
                if t not in visti:
                    # «#123» non deve passare per «#1234», né «ADR-0042» per un prefisso
                    visti[t] = (re.search(re.escape(t) + r"(?!\d)", corpo) is not None
                                if t[-1].isdigit() else t in corpo)
            mancano = [t for t in g if not visti[t]]
            if mancano:
                scoperte.append({"file": f.name, "riga": n, "mancano": mancano, "testo": r.strip()[:160]})
    return {"righe": righe_tot, "righe_con_gettoni": con_gettoni, "righe_scoperte": scoperte,
            "note": note, "note_citate": sum(x["citata_nella_storica"] for x in note)}


def _piano(s: str) -> str:
    """Minuscole e senza accenti: «città» si trova scrivendo «citta»."""
    s = unicodedata.normalize("NFKD", s.casefold())
    return "".join(c for c in s if not unicodedata.combining(c))


def filtra(voci: "list[Voce]", parole: "list[str]" = (), pr: "int | None" = None,
           adr: "int | None" = None, tema: "str | None" = None, da: "str | None" = None,
           a: "str | None" = None, ident: "str | None" = None) -> "list[Voce]":
    fuori = []
    for v in voci:
        corpo = _piano(v.testo_md)
        if ident and v.id != ident.upper():
            continue
        if pr is not None and pr not in v.pr and not re.search(rf"#{pr}(?!\d)", v.testo_md):
            continue
        if adr is not None and adr not in v.adr and f"ADR-{adr:04d}" not in v.testo_md:
            continue
        if tema and _piano(tema) not in {_piano(t) for t in v.temi}:
            continue
        if da and v.data < da:
            continue
        if a and v.data > a:
            continue
        if any(_piano(p) not in corpo for p in parole):
            continue
        fuori.append(v)
    return fuori


def controlla(testo: str, changelog: "str | None") -> "list[str]":
    """I difetti di forma. Lista vuota = il file si può cercare con i filtri."""
    errori = []
    voci = leggi(testo)
    if not voci:
        errori.append("nessuna voce MS-NNNN nel file")
    for atteso, v in enumerate(voci, 1):
        dove = f"{v.id} (riga {v.riga})"
        if v.numero != atteso:
            errori.append(f"{dove}: numero fuori sequenza, atteso MS-{atteso:04d}")
        try:
            date.fromisoformat(v.data)
        except ValueError:
            errori.append(f"{dove}: data «{v.data}» non è AAAA-MM-GG")
        for c in OBBLIGATORI:
            if c not in v.campi:
                errori.append(f"{dove}: manca il campo «{c}»")
        if v.campi.get("Data") and v.campi["Data"] != v.data:
            errori.append(f"{dove}: il campo Data ({v.campi['Data']}) non è la data del titolo")
        if not v.campi.get("Testo"):
            errori.append(f"{dove}: Testo vuoto")
        if v.campi.get("PR", "—") != "—" and not v.pr:
            errori.append(f"{dove}: PR senza numeri #NNN (o «—»)")
        if v.campi.get("ADR", "—") != "—" and not v.adr:
            errori.append(f"{dove}: ADR senza numeri ADR-NNNN (o «—»)")
    # Una testa che non si legge (per esempio «### MS-????» arrivata dalla coda senza
    # numero, ADR-0138) sparirebbe dentro la voce prima: i filtri non la troverebbero.
    dentro = False
    for n, r in enumerate(testo.splitlines(), 1):
        if r.strip() == "## Voci":
            dentro = True
        elif dentro and r.startswith("### MS-") and not TESTA.match(r):
            errori.append(f"riga {n}: testa «{r.strip()[:50]}» non è «### MS-NNNN · AAAA-MM-GG · titolo»")
    if changelog is not None and LINK not in changelog:
        errori.append(f"plans/CHANGELOG.md non porta a {LINK}: la storia va collegata al changelog")
    return errori


TETTO_MEMORIA = 12 * 1024
"""Tetto di MEMORY.md (ADR-0139): 12 KB lasciano 4 KB di margine al limite duro."""
LIMITE_MEMORIA = 16 * 1024
"""Il limite oltre il quale la piattaforma taglia l'indice della memoria delle sessioni."""


def misura_memoria(cartella: Path, tetto: int = TETTO_MEMORIA) -> dict:
    """Byte di MEMORY.md e le righe più lunghe: le prime da accorciare o archiviare."""
    f = cartella / "MEMORY.md"
    dati = f.read_bytes()
    righe = dati.decode("utf-8").splitlines()
    lunghe = sorted(((len(r.encode("utf-8")) + 1, i, r) for i, r in enumerate(righe, 1)),
                    reverse=True)[:5]
    return {
        "byte": len(dati),
        "tetto": tetto,
        "limite": LIMITE_MEMORIA,
        "sopra_tetto": len(dati) > tetto,
        "sopra_limite": len(dati) > LIMITE_MEMORIA,
        "righe_lunghe": [{"riga": i, "byte": b, "testo": r[:100]} for b, i, r in lunghe],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("parole", nargs="*", help="Parole che devono comparire tutte nella voce "
                    "(senza badare a maiuscole e accenti).")
    ap.add_argument("--pr", type=int, help="Numero della PR, senza #.")
    ap.add_argument("--adr", type=int, help="Numero dell'ADR, anche senza zeri (93 = ADR-0093).")
    ap.add_argument("--tema", help="Un tema della voce (campo Temi), per esempio prosa, regole, arc07.")
    ap.add_argument("--da", help="Prima data, AAAA-MM-GG compresa.")
    ap.add_argument("--a", help="Ultima data, AAAA-MM-GG compresa.")
    ap.add_argument("--id", dest="ident", help="Una voce sola, per esempio MS-0042.")
    ap.add_argument("--elenco", action="store_true", help="Solo id, data e titolo delle voci trovate.")
    ap.add_argument("--json", action="store_true", help="Uscita per un agente: le voci coi loro campi.")
    ap.add_argument("--check", action="store_true", help="Il cancello: esce 1 se il file è "
                    "scritto male o il CHANGELOG dei piani non lo collega.")
    ap.add_argument("--confronta-memoria", type=Path, metavar="DIR",
                    help="Cartella della memoria delle sessioni (MEMORY.md e note): elenca le righe "
                         "con PR, ADR, SHA o percorsi che il repo non ha. Non è un cancello: esce 0.")
    ap.add_argument("--tetto-memoria", type=Path, metavar="DIR",
                    help="Cartella della memoria delle sessioni: esce 1 se MEMORY.md supera il "
                         "tetto (ADR-0139) e mostra le righe più lunghe.")
    ap.add_argument("--tetto", type=int, default=TETTO_MEMORIA,
                    help=f"Tetto in byte per --tetto-memoria (predefinito {TETTO_MEMORIA}).")
    ap.add_argument("--senza-git", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--file", type=Path, default=FILE, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)

    for d in (a.da, a.a):
        if d:
            try:
                date.fromisoformat(d)
            except ValueError:
                print(f"data non valida: {d} (serve AAAA-MM-GG)", file=sys.stderr)
                return 2
    if a.tetto_memoria:
        if not (a.tetto_memoria / "MEMORY.md").is_file():
            print(f"manca {a.tetto_memoria / 'MEMORY.md'}", file=sys.stderr)
            return 2
        r = misura_memoria(a.tetto_memoria, a.tetto)
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=1))
        else:
            segno = "✗" if r["sopra_tetto"] else "✓"
            print(f"{segno} MEMORY.md: {r['byte']} byte, tetto {r['tetto']}, limite {r['limite']}"
                  + (" — OLTRE IL LIMITE: l'indice viene tagliato" if r["sopra_limite"] else ""))
            if r["sopra_tetto"]:
                print("  Togliere le righe di cronologia (PR unite, lavori chiusi) dopo averle "
                      "archiviate (ADR-0127). Le più lunghe:")
                for x in r["righe_lunghe"]:
                    print(f"    r.{x['riga']} ({x['byte']} byte): {x['testo']}")
        return 1 if r["sopra_tetto"] else 0

    if not a.file.is_file():
        print(f"manca {a.file}", file=sys.stderr)
        return 2
    testo = a.file.read_text(encoding="utf-8")

    if a.check:
        cl = CHANGELOG.read_text(encoding="utf-8") if a.file == FILE else None
        errori = controlla(testo, cl)
        for e in errori:
            print(f"✗ {e}")
        if errori:
            return 1
        print(f"✓ memoria storica: {len(leggi(testo))} voci in forma, collegata al changelog")
        return 0

    if a.confronta_memoria:
        if not a.confronta_memoria.is_dir():
            print(f"manca la cartella {a.confronta_memoria}", file=sys.stderr)
            return 2
        r = confronta_memoria(a.confronta_memoria, storica=testo)
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=1))
            return 0
        for s in r["righe_scoperte"]:
            print(f"✗ {s['file']}:{s['riga']}  mancano {', '.join(s['mancano'])}\n    {s['testo']}")
        print(f"\n— righe {r['righe']}, con gettoni cercabili {r['righe_con_gettoni']}, "
              f"con gettoni che il repo non ha {len(r['righe_scoperte'])}; note "
              f"{len(r['note'])}, citate nella memoria storica {r['note_citate']}. "
              "Le righe senza gettoni (regole in prosa) non si controllano così.")
        return 0

    voci = leggi(testo)
    if a.pr is not None and not a.senza_git:
        mappa = pr_dai_merge(file=a.file)
        for v in voci:
            # Solo le voci dell'addendum (nate da una riga del changelog) senza numero
            # scritto: le 67 righe portate in blocco dalla #381 non sono «della» #381.
            if not re.search(r"#\d", v.campi.get("PR", "")) and "CHANGELOG" in v.campi.get("Origine", ""):
                v.pr_merge = mappa.get(v.id, set())
    trovate = filtra(voci, a.parole, a.pr, a.adr, a.tema, a.da, a.a, a.ident)
    if a.json:
        print(json.dumps([{k: (sorted(v) if isinstance(v, set) else v)
                           for k, v in asdict(x).items() if k != "numero"} for x in trovate],
                         ensure_ascii=False, indent=1))
    elif a.elenco:
        for v in trovate:
            print(f"{v.id}  {v.data}  {v.titolo}")
    else:
        print("\n\n".join(v.testo_md for v in trovate) if trovate else "Nessuna voce trovata.")
        if trovate:
            print(f"\n— {len(trovate)} voci (plans/MEMORIA-STORICA.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
