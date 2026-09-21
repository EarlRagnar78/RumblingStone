#!/usr/bin/env python3
"""verifica_sezione6.py — i comandi che §6.2 cita vengono ESEGUITI, non creduti.

## Il difetto che questo cancello presidia, e che e' gia' successo

`STATO-E-ORDINE-DEI-PIANI` §6 nasce con un principio dichiarato:

> *«ogni cosa da fare ha un comando che la rimisura, perche' un elenco che
> dipende dalla memoria di una chat non e' un elenco, e' un ricordo»*

Il principio e' giusto. Ma il 2026-09-21 si e' scoperto che **scrivere il
comando accanto alla riga non e' eseguirlo**: la riga *«i 27 ADR mancanti in
`docs/INDEX.md` §4»* citava `validate_docs --sorgenti`, che in quel momento
stampava **zero**, girava in CI ed era verde. I 27 non erano invecchiati: non
erano **mai** stati misurati. E la riga gemella parlava di «51 link rotti nei
booklet», chiusi nove giorni prima e registrati a zero nello stesso archivio.

Il DM, lo stesso giorno: *«fai un cancello che esegua in CI i comandi citati
da §6.2»*.

## Le due specie di comando, e perche' vanno trattate diversamente

Non tutti i comandi citati sono la stessa cosa, e confonderli darebbe un
cancello che sbaglia in entrambi i versi:

| specie | come si riconosce | cosa dice una riga ⬜ |
|---|---|---|
| **cancello** | stampa un verdetto `✓` / `✗` | se stampa `✓`, la riga mente: non c'e' lavoro |
| **misura** | stampa numeri, nessun verdetto | la riga deve **dichiarare** il numero atteso, e il gate lo ricerca nell'output |

`validate_docs --sorgenti` e' un cancello: e' verde o rosso, e un ⬜ accanto a
un verde e' esattamente il difetto dei 27. `misura_craft --p1` e' una misura:
stampa «22 box su 477» e non ha un'opinione, quindi la riga deve dire **quale**
numero si aspetta e il gate verifica che quel numero ci sia ancora.

## Sicurezza: si esegue una allowlist, non del testo

🔴 **Questo strumento esegue comandi che stanno in un file Markdown**, ed e' la
ragione per cui il DM ha esitato prima di ordinarlo. I presidi, tutti e tre:

1. **Forma rigida.** Si riconosce solo `python3 scripts/<nome>.py [--flag …]`.
   Niente pipe, redirezioni, `;`, `&&`, sostituzioni di comando: un carattere
   fuori dall'alfabeto ammesso e la riga e' **rifiutata**, non eseguita.
2. **Allowlist di file.** `<nome>.py` deve esistere in `scripts/` ed essere in
   `CONSENTITI`. Un comando nuovo va aggiunto **qui**, da una persona.
3. **Niente shell.** `subprocess.run` con una lista di argomenti e
   `shell=False`, timeout per comando, `cwd` alla radice del repo.

⚠️ **Il costo e' vero e va detto**: questo passo esegue tutti i comandi citati,
e sono i piu' lenti del repo. Gira in un job suo, e non blocca gli altri.

## Uso

    python3 scripts/verifica_sezione6.py           # la tabella, con gli esiti
    python3 scripts/verifica_sezione6.py --check   # esce 1 se una riga mente

Decisione: ADR-0063.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEZIONE = ROOT / "plans" / "STATO-E-ORDINE-DEI-PIANI.md"
TIMEOUT = 900

#: 🔒 I soli script che questo cancello puo' eseguire. Aggiungerne uno e' una
#: decisione umana, non una conseguenza di aver scritto un backtick in un `.md`.
CONSENTITI = frozenset({
    "misura_craft.py", "punteggio_mqm.py", "validate_docs.py",
    "validate_modules.py", "validate_prosa.py", "validate_norme_editoriali.py",
    "validate_booklets.py", "superficie_norme.py", "decisioni_dm.py",
})

#: La forma ammessa, e nient'altro. `[\w.-]` esclude ogni metacarattere di shell.
COMANDO = re.compile(r"`(?:python3\s+)?(?:scripts/)?(\w+\.py|\w+)\s*((?:--[\w-]+\s*)*)`")
#: Il numero che una riga dichiara di aspettarsi da una misura.
ATTESA = re.compile(r"<!--\s*attesa:\s*([^>]+?)\s*-->")


def righe_di_62() -> "list[dict]":
    """Le righe della tabella §6.2, con stato, testo e comandi citati."""
    testo = SEZIONE.read_text(encoding="utf-8")
    dentro, fuori = False, []
    for riga in testo.splitlines():
        if riga.startswith("### 6.2 · "):
            dentro = True
            continue
        if dentro and riga.startswith("### "):
            break
        if not dentro or not riga.startswith("|") or riga.startswith("|---"):
            continue
        celle = [c.strip() for c in riga.strip().strip("|").split("|")]
        if len(celle) < 4 or celle[0] in ("", "Lotto"):
            continue
        stato = "aperto" if "⬜" in celle[0] else "chiuso" if "✅" in celle[0] else "altro"
        fuori.append({
            "stato": stato,
            "lotto": re.sub(r"[*~]", "", celle[1])[:58],
            "cella": celle[3],
            # ⚠️ **Le attese sono piu' d'una apposta.** Una riga puo' citare
            # due misure — e' successo subito a F1.1-F1.3, che cita
            # `punteggio_mqm --norme` e `misura_craft --discriminante`. Con
            # una sola attesa il gate la confrontava con l'output sbagliato e
            # dichiarava invecchiato un numero giusto: un falso positivo che
            # avrebbe insegnato a disattivare il cancello.
            "attese": ATTESA.findall(celle[3]),
            "comandi": _comandi(celle[3]),
        })
    return fuori


def _comandi(cella: str) -> "list[list[str]]":
    """I comandi citati, **solo** quelli che passano la forma e l'allowlist."""
    fuori = []
    for nome, flag in COMANDO.findall(cella):
        script = nome if nome.endswith(".py") else f"{nome}.py"
        if script not in CONSENTITI or not (ROOT / "scripts" / script).exists():
            continue
        fuori.append([sys.executable, f"scripts/{script}", *flag.split()])
    return fuori


def esegui(argv: "list[str]") -> "tuple[int, str]":
    """Esecuzione senza shell, con timeout. Nessun argomento viene interpretato."""
    try:
        p = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                           timeout=TIMEOUT, shell=False, check=False)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, f"(timeout dopo {TIMEOUT}s)"


def _specie(uscita: str) -> str:
    return "cancello" if ("✓ " in uscita or "✗ " in uscita) else "misura"


def verifica() -> "tuple[list[str], list[dict]]":
    errori, esiti = [], []
    for r in righe_di_62():
        if not r["comandi"]:
            esiti.append(dict(r, esito="nessun comando citato", specie="—"))
            if r["stato"] == "aperto" and "bloccato sul DM" not in r["cella"]:
                errori.append(
                    f"«{r['lotto']}» e' ⬜ e non cita nessun comando eseguibile: "
                    "una riga di §6.2 senza comando e' un ricordo, non un elenco")
            continue
        for argv in r["comandi"]:
            codice, uscita = esegui(argv)
            specie = _specie(uscita)
            esiti.append(dict(r, esito=f"exit {codice}", specie=specie,
                              comando=" ".join(argv[1:])))
            nome = " ".join(argv[1:])
            if codice == 124:
                errori.append(f"«{r['lotto']}»: `{nome}` non risponde entro {TIMEOUT}s")
                continue
            if specie == "cancello":
                # 🐛 **Il primo criterio era «stampa ✓», e ha dato un falso
                # positivo al primo giro.** `validate_modules --tetto-el`
                # stampa `✓ nessuno sforamento` **e** un `⚠ ZERO incontri
                # marcati`: e' verde **a vuoto**, perche' nessun incontro puo'
                # sforare se nessun incontro e' dichiarato. E' esattamente il
                # `SUPERFICIE_VUOTA` di ADR-0062, e la riga ⬜ accanto **dice
                # il vero**. Un cancello che emette un avviso ha qualcosa da
                # dire, e non conta come pulito.
                pulito = ("✓ " in uscita and "✗ " not in uscita
                          and "⚠" not in uscita)
                if r["stato"] == "aperto" and pulito:
                    errori.append(
                        f"«{r['lotto']}» e' ⬜ ma `{nome}` e' **verde**: la riga "
                        "dichiara del lavoro che il comando dice non esistere. "
                        "E' il difetto dei «27 ADR mancanti», che erano zero")
            elif not r["attese"]:
                errori.append(
                    f"«{r['lotto']}» cita la misura `{nome}` senza dichiarare "
                    "cosa si aspetta: aggiungi `<!-- attesa: N -->` nella cella, "
                    "altrimenti il numero scritto accanto non e' verificabile")
            elif not any(all(p in uscita for p in a.split()) for a in r["attese"]):
                errori.append(
                    f"«{r['lotto']}»: nessuna delle attese dichiarate "
                    f"({' | '.join(r['attese'])}) compare nell'output di "
                    f"`{nome}` — il numero nella tabella e' invecchiato")
    return errori, esiti


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="esce 1 se una riga mente")
    args = ap.parse_args(argv)
    errori, esiti = verifica()
    if not args.check:
        print("\n§6.2 — I COMANDI CITATI, ESEGUITI\n" + "=" * 66)
        for e in esiti:
            marca = {"aperto": "⬜", "chiuso": "✅"}.get(e["stato"], "  ")
            print(f"  {marca} {e['lotto']:58} [{e['specie']}] {e['esito']}")
            if e.get("comando"):
                print(f"       {e['comando']}")
        print()
    for e in errori:
        print(f"  ✗ {e}")
    if errori:
        print(f"✗ verifica_sezione6: {len(errori)} riga/he di §6.2 non dicono il vero")
        return 1
    n = sum(1 for e in esiti if e.get("comando"))
    print(f"✓ verifica_sezione6: {len(righe_di_62())} righe, {n} comandi eseguiti "
          "davvero, nessuna riga mente")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
