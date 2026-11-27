# I limiti della *d* eufonica, misurati seminando (2026-11-11)

> Seguito di `plans/esperimenti/d-eufonica-2026-11-09/`. Decisione in ADR-0120,
> emendamento del 2026-11-11. Script: `semina.py` (vuole markdown-it-py; con un
> indirizzo **locale** misura anche LanguageTool, mai l'API pubblica).

## Perché un banco di semina

Il corpus è a zero, quindi contare i rilievi non distingue un rilevatore che
legge da uno cieco. Il banco mette errori noti in una copia in memoria di ogni
file di contenuto (*ad a…* → *a a…*, *ed e…* → *e e…*, *a e/i/o/u…* → *ad …*,
*e a/i/o/u…* → *ed …*) e conta le righe seminate che il rilevatore segnala,
divise per posto. Il posto lo dice il parser CommonMark. È deterministico: stessi
file, stessi semi, stesso numero.

## Esito

| Posto | Righe seminate | Regex prima | Regex dopo | LanguageTool |
|---|---:|---:|---:|---:|
| riga normale | 2.503 | 2.503 | 2.503 | 2.502 |
| citazione (`>`) | 758 | 758 | 758 | 757 |
| tabella | 619 | 619 | 619 | 0 |
| rientrata, prosa | 64 | **0** | **64** | 64 |
| recinto di codice (rilievo giusto: nessuno) | 106 | 1 | 0 | 1 |
| **richiamo sulla prosa** | 3.944 | **98,38%** | **100%** | 84,25% |
| rilievi su righe non seminate | | 0 | 0 | 23 |

## Le tre letture del codice rientrato

| Lettura | Richiamo | Rilievi nel codice | Righe diverse da CommonMark | Righe lette |
|---|---:|---:|---:|---:|
| ogni riga rientrata è codice (prima) | 3.880 | 1 | 1.465 | 116.470 |
| regola stdlib (ripiego) | 3.944 | 1 | 184 | 117.812 |
| markdown-it-py (scelta) | 3.944 | 0 | 0 | 117.589 |

Sul corpus vero le tre letture danno 0 errori; gli avvisi di virgolette dritte
passano da 2.403 a 2.451, perché ora si leggono righe che prima si saltavano.

## Cosa non misura

- I semi vengono da quattro schemi vicini a quelli della regex: il banco dice
  **dove** il rilevatore legge, non che gli schemi coprano tutta la lingua. Il
  riscontro indipendente è la colonna di LanguageTool.
- Solo minuscole, solo sulla stessa riga. Maiuscole, corsivo in mezzo e
  congiunzione a fine riga sono nei test di `test_lingua.py`.
- Una citazione alla lettera va marcata a mano con `<!-- sic -->`.
