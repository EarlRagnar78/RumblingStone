# `_ARCHIVIO/` — Mappe di ARC-08 (La Battaglia di Hammerfist)

## Cos'è

I tre master di mappe **deprecati** dell'arco, assorbiti dai tre definitivi
`Hammerfist-L1/L2/L3-REVISED-Ultra-Clear.md`. Stessa deroga alla regola D10 già
concordata col DM per i 16 sorgenti di ARC-07 (`07_…/_ARCHIVIO/README.md`): un
sorgente consolidato si sposta qui **dopo** che il suo contenuto è confluito nel
master definitivo.

| File | Mappe | Assorbito da |
|---|---|---|
| `Hammerfist-Lotto-1-Ricognizione.md` | 2 | `Hammerfist-L1-REVISED-Ultra-Clear.md` |
| `Hammerfist-Lotto-2-Assedio.md` | 1 | `Hammerfist-L2-REVISED-Ultra-Clear.md` |
| `Hammerfist-Lotto-3-FINALE.md` | 4 | `Hammerfist-L3-REVISED-Ultra-Clear.md` |

## Perché sono qui e non cancellati

Decisione **D1** del DM, 2026-09-05 (`plans/PIANO-RIPRESA-PR-ABBANDONATE` §1.2).
Il problema non erano i sette SVG: era che tre master deprecati stavano in
`Mappe/` accanto ai tre definitivi, ed è la condizione che genera il prossimo
errore di puntamento — un DM che apre la cartella e sceglie il file sbagliato.
Spostarli lo toglie.

⚠️ **I sette SVG sono venuti qui con i loro master, non sono stati cancellati.**
La PR #63 li cancellava tenendo i master, ed è il difetto che
[ADR-0043](../../../plans/adr/ADR-0043-le-montagne-sono-muri-e-nessun-master-esce-dal-controllo.md)
adesso intercetta. Tenendo insieme master e `rendered/`, questa cartella resta
**dentro** il raggio di `validate_maps` — che cerca ogni `**/rendered/*.svg` —
quindi i sette restano rigenerabili e in sincrono, e nessuno esce dal controllo.
Archiviare qui non è un modo per far tacere il gate: è un modo per non averne
bisogno.

## Regole

- **Non si gioca da qui.** Le mappe al tavolo sono quelle dei tre `…-REVISED-Ultra-Clear`.
- **Non si modificano.** Una correzione va nel master definitivo; se un
  contenuto di qui serve ancora, si porta là e si annota nel `CHANGELOG`.
- **I riferimenti puntano a `_ARCHIVIO/…`.** L'unico che esisteva —
  `Hammerfist-L2-REVISED-Ultra-Clear.md` §Round-per-round — è stato riscritto.
- **I log append-only restano intatti** (`plans/CHANGELOG.md`,
  `docs/guides/LEGENDA-FUNZIONALE-SPEC.md` §6.2 nella parte di censimento):
  sono record storici e dicono il vero su quando furono scritti.
