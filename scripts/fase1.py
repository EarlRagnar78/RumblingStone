#!/usr/bin/env python3
"""fase1.py — l'analisi in sola lettura che precede ogni modifica.

Perche' esiste, in un numero.

  **Quattordici misure sbagliate in un ramo solo**, fra il 2026-09-17 e il
  2026-09-20. Non una veniva da una regex scritta male: venivano tutte
  dall'aver scritto una regex **prima di guardare se il dato c'era gia'**.

  * la virgola fra due trigger contata come trigger -> 82 coppie di skill
    sovrapposte invece di 5;
  * «web» che cattura *web enhancement* -> 80% di incantesimi fuori norma
    invece di 39%;
  * «caso» che e' italiano comune -> 55 indagini invece di 3;
  * le maiuscole d'inizio frase contate come nomi propri -> nove box di DEF-4
    fuori norma invece di tre, e il numero falso finito nel corpo di una PR;
  * un filtro di percorso che non scattava mai -> 1.548 «file di gioco»
    invece di 511, misurato il 2026-09-20 mentre si scriveva **questo** script.

La cura, ogni volta, e' stata la stessa: **un dato che il repo gia' possedeva**.
I 322 nomi propri stanno nel `Bestiario/` e in `state.md`. Gli archivi si
dichiarano da soli con un `_SNAPSHOT-STORICO.md`. Le versioni superate stanno
nella matrice dell'arco. Le norme gia' misurate stanno nel registro.

Questo script non misura niente di nuovo. **Mette in fila cio' che il repo sa
gia'**, sul bersaglio che stai per toccare, e lo fa prima che tu scriva la
prima regex. E' la sesta regola d'oro di `AGENTS.md` resa comando: la regola
e' eseguita quando questo output esiste.

## I quattro passi, in ordine di precedenza

    1 · il registro delle norme   «questa cosa la misura gia' qualcuno?»
    2 · l'algoritmo a strati      «quali skill devo avere aperte?»
    3 · i dati del repo           «cosa e' archivio, cosa e' superato, chi sono
                                   i nomi propri?»
    4 · le misure di oggi         «da che numero parto?»

Una regex nuova viene **dopo** il passo 4, e va pubblicata con i suoi falsi
positivi contati a mano.

## Uso

    python3 scripts/fase1.py '07_*/ARC07-DEF-4-*.md'
    python3 scripts/fase1.py --check 'PG/**/*.md'     # esce 1 se tocchi un archivio
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import misura_craft as mc  # noqa: E402  (dopo il sys.path)

REGISTRO = ROOT / "skills" / "REGISTRO-NORME-EDITORIALI.md"
ORCHESTRAZIONE = ROOT / "skills" / "ORCHESTRAZIONE.md"

#: Le cartelle i cui documenti parlano al **repo**, non al tavolo (ADR-0035).
CARTELLE_DOCUMENTO = ("plans", "docs", "skills", "scripts", ".github")

#: Le marche di stato che il repo si e' gia' dato, e chi le dichiara.
MARCHE = {
    "_SNAPSHOT-STORICO.md": "snapshot storico dichiarato nella cartella",
    "_ARCHIVIO": "archivio (ADR-0054: un archivio non e' una copia)",
    "DEPRECATO": "deprecato (`misura_craft.ESCLUSI_NOME`)",
    "ERRATA-": "errata corrige (`misura_craft.ESCLUSI_NOME`)",
}


def cartelle_snapshot() -> "set[Path]":
    """Le cartelle che si dichiarano archivio con un file, non con un nome."""
    return {p.parent for p in ROOT.rglob("_SNAPSHOT-STORICO.md")}


def stato_del_file(f: Path, snapshot: "set[Path]") -> "list[str]":
    """Cosa il repo dichiara gia' su questo file, senza che nessuno lo deduca."""
    detto: "list[str]" = []
    if any(s in f.parents for s in snapshot):
        detto.append(MARCHE["_SNAPSHOT-STORICO.md"])
    if "_ARCHIVIO" in f.parts:
        detto.append(MARCHE["_ARCHIVIO"])
    for marca in ("DEPRECATO", "ERRATA-"):
        if marca in f.name:
            detto.append(MARCHE[marca])
    return detto


def matrici_versioni() -> "dict[str, list[str]]":
    """Cosa dicono le matrici delle versioni, file per file nominato.

    ⚠️ Si legge la **riga**, non si interpreta: questa colonna ha gia'
    ingannato uno strumento il 2026-09-17, e lo dice da sola in testa.
    """
    fuori: "dict[str, list[str]]" = {}
    for matrice in ROOT.rglob("*MATRICE-VERSIONI.md"):
        for riga in matrice.read_text(encoding="utf-8").splitlines():
            if not riga.startswith("|"):
                continue
            for m in re.finditer(r"`([^`]+\.md)`", riga):
                righe = fuori.setdefault(Path(m.group(1)).name, [])
                # Le matrici si citano a vicenda: la stessa riga compare in
                # piu' di un file e non e' una seconda informazione.
                if riga.strip() not in righe:
                    righe.append(riga.strip())
    return fuori


def primo_semaforo(cella: str) -> str:
    """La prima marca di stato della cella, o stringa vuota."""
    for ch in cella:
        if ch in "🟢🟡🔴⚪":
            return ch
    return ""


def norme_del_registro() -> "list[tuple[str, str, str]]":
    """(file normativo, norma, chi la misura) dal registro, riga per riga."""
    if not REGISTRO.exists():
        return []
    fuori = []
    for riga in REGISTRO.read_text(encoding="utf-8").splitlines():
        if not riga.startswith("|") or riga.startswith("|---"):
            continue
        celle = [c.strip() for c in riga.strip("|").split("|")]
        if len(celle) < 3 or celle[0].lower() in ("file", "norma"):
            continue
        fuori.append((celle[0], celle[1], celle[2]))
    return fuori


def strati() -> "list[tuple[str, str]]":
    """Gli strati dell'algoritmo, letti dal marcatore invece che ricopiati."""
    if not ORCHESTRAZIONE.exists():
        return []
    testo = ORCHESTRAZIONE.read_text(encoding="utf-8")
    dopo = testo.split("<!-- orchestrazione: strati -->", 1)
    if len(dopo) < 2:
        return []
    fuori = []
    for riga in dopo[1].splitlines():
        if not riga.startswith("|") or riga.startswith("|---"):
            continue
        celle = [c.strip() for c in riga.strip("|").split("|")]
        if len(celle) < 3 or celle[0].startswith("Strato"):
            continue
        if not celle[0].startswith("**"):
            break
        fuori.append((celle[0].strip("* "), celle[2]))
    return fuori


def espandi(modelli: "list[str]") -> "list[Path]":
    """Come `misura_craft.espandi`, ma **senza** escludere archivi.

    🔴 La differenza e' il punto dello script: `misura_craft` toglie gli
    archivi perche' non li deve misurare; qui vanno **mostrati**, perche' la
    domanda e' «stai per toccare un archivio?».
    """
    fuori: "list[Path]" = []
    for m in modelli:
        trovati = sorted(ROOT.glob(m))
        if not trovati:
            raise SystemExit(f"modello che non pesca niente: {m!r}")
        fuori.extend(t for t in trovati if t.is_file())
    visti, tenuti = set(), []
    for f in fuori:
        if f not in visti:
            visti.add(f)
            tenuti.append(f)
    return tenuti


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("bersagli", nargs="+",
                    help="file o modelli glob relativi alla radice del repo")
    ap.add_argument("--check", action="store_true",
                    help="esce 1 se un bersaglio e' un archivio dichiarato")
    args = ap.parse_args()

    files = espandi(args.bersagli)
    snapshot = cartelle_snapshot()
    matrici = matrici_versioni()

    print(f"\n{'='*72}\nFASE 1 — sola lettura · {len(files)} file\n{'='*72}")

    # ── Passo 1 ──────────────────────────────────────────────────────────
    norme = norme_del_registro()
    # ⚠️ Si guarda la **prima** marca della cella, non se la marca c'e'.
    # Una cella puo' portarne due — «🟢 congegno X — 🔴 era a zero in nove
    # archi» dice «misurato» e «il numero fa schifo», e sono due cose diverse.
    misurate = [n for n in norme if primo_semaforo(n[2]) == "🟢"]
    print(f"\n1 · IL REGISTRO DELLE NORME — {len(norme)} righe, "
          f"{len(misurate)} con un misuratore vero")
    print("    «questa cosa la misura gia' qualcuno?» Se si', si riusa:")
    print("    una norma, un rilevatore.\n")
    for f, norma, chi in misurate:
        print(f"    🟢 {norma[:58]:58} {chi}")
    senza = [n for n in norme if primo_semaforo(n[2]) == "🔴"]
    if senza:
        print(f"\n    ⚠️  {len(senza)} norme senza misuratore, con la ragione scritta:")
        for f, norma, chi in senza[:6]:
            print(f"    🔴 {norma[:58]:58} {chi[:40]}")

    # ── Passo 2 ──────────────────────────────────────────────────────────
    print("\n2 · L'ALGORITMO A STRATI — quali skill devo avere aperte")
    # ⚠️ `ROOT.glob()` restituisce percorsi **assoluti**: senza `relative_to`
    # la prima parte e' «/» e nessun bersaglio risulta mai un documento. E' lo
    # stesso difetto del filtro che non scattava mai, in miniatura.
    documento = [f for f in files
                 if f.relative_to(ROOT).parts[0] in CARTELLE_DOCUMENTO]
    tavolo = [f for f in files if f not in documento]
    print("    La domanda 2 e' l'unica con una risposta sola, e il bersaglio")
    print("    la risponde da se':")
    if tavolo:
        print(f"    → {len(tavolo):3} file parlano al TAVOLO   ⇒ L1 `rumblingstone-narrative-style`")
    if documento:
        print(f"    → {len(documento):3} file parlano al REPO     ⇒ L1 `rumblingstone-prosa-documenti`")
    if tavolo and documento:
        print("    ⚠️  Il bersaglio mescola i due registri: ADR-0035 dice che le")
        print("       due norme sono opposte. Vanno in due lotti, non in uno.")
    print("\n    Gli altri strati si sommano (ORCHESTRAZIONE.md, cinque domande):")
    for nome, skill in strati():
        print(f"      {nome:22} {skill[:78]}")

    # ── Passo 3 ──────────────────────────────────────────────────────────
    print("\n3 · I DATI CHE IL REPO GIA' POSSIEDE")
    registro = mc._registro_dei_nomi()
    print(f"    Nomi propri della campagna: **{len(registro)}**, presi da")
    print("    `Bestiario/` e dalla prima colonna di `campaign/state.md`.")
    print("    Non scrivere una lista di nomi: usare questa.\n")
    archiviati = []
    for f in files:
        rel = f.relative_to(ROOT)
        detto = stato_del_file(f, snapshot)
        righe_matrice = matrici.get(f.name, [])
        if detto:
            archiviati.append(rel)
            print(f"    ⛔ {rel}")
            for d in detto:
                print(f"         {d}")
        if righe_matrice:
            print(f"    📜 {rel} — nominato in una matrice delle versioni:")
            for r in righe_matrice[:2]:
                print(f"         {r[:150]}")
    if not archiviati:
        print("    ✅ Nessun bersaglio e' un archivio dichiarato.")

    # ── Passo 4 ──────────────────────────────────────────────────────────
    print("\n4 · LE MISURE DI OGGI — da che numero parti")
    vivi = [f for f in files if f.relative_to(ROOT) not in archiviati]
    testo = "\n".join(f.read_text(encoding="utf-8", errors="replace")
                      for f in vivi if f.suffix == ".md")
    if testo.strip():
        box = mc.difetti_dei_box(testo)
        print(f"    box read-aloud {box['box']:4} · oltre 12 righe {box['oltre 12 righe']:3}"
              f" · con parentesi {box['con parentesi']:3} · >1 nome proprio {box['>1 nome proprio']:3}")
        attivi = {n: v for n, v in mc.misura(testo).items() if v}
        print(f"    congegni del mestiere attivi: {len(attivi)} su {len(mc.CONGEGNI)}")
        zero = [n for n, _, _ in mc.CONGEGNI if n not in attivi]
        if zero:
            print(f"    a ZERO: {', '.join(zero)}")
    else:
        print("    (nessun markdown vivo fra i bersagli)")

    print(f"\n{'='*72}")
    print("Solo ora una regex nuova, e va pubblicata con i suoi falsi positivi")
    print("contati a mano.")
    print(f"{'='*72}\n")

    if args.check and archiviati:
        print(f"✗ fase1: {len(archiviati)} bersaglio/i sono archivi dichiarati")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
