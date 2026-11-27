---
name: memoria-storica-repo
description: Dove sta la storia tolta dalla memoria (plans/MEMORIA-STORICA.md), come si legge e le regole per scriverla (ADR-0127, PR #381)
metadata:
  type: project
  modified: 2026-11-12T11:24:56.909Z
---

Il 2026-11-12 Jfs ha chiesto di non perdere la storia tolta dalla memoria del progetto (ridotta da ~25 KB a 8 KB) e di obbligare tutte le sessioni a conservarla; ha approvato i tre livelli.

- File: `plans/MEMORIA-STORICA.md` nel repo, voci `### MS-NNNN · data · titolo` con Data, PR, ADR, Temi, Origine, Testo (obbligatori), Trovato nel repo, Fuori dal repo, Note di memoria, Solo qui. MS-0001…0067 = le 67 righe della memoria lunga; MS-0068 = la PR #381 (unita il 2026-11-12, merge ba8b8edf); MS-0069/0070/0071 = #380, #379, #382.
- Lettura: `python3 scripts/memoria_storica.py --pr N | --adr N | --tema T | --da/--a | --id | parole | --json`; nel server MCP in sola lettura.
- Scrittura: (a) addendum bloccante in CI: PR con righe nuove in plans/CHANGELOG.md senza `### MS-` nuovo = rossa; (b) prima di togliere una riga da MEMORY.md, archiviarla lì se manca.
- Misura del recupero: riferimenti nel repo 127/165 → 165/165; fatti di contenuto mancanti 24 → 0. 53 righe su 67 nascevano da una PR, 14 no (regole, ambiente, chat): per quelle vale solo la regola (b), che la CI non vede.
- Dati personali (nomi dei giocatori, macchine di Jfs, vecchi utenti) fuori dal repo per scelta di Jfs (card del 12/11).
- Notati e non corretti: ADR-0104 citato ma il file non esiste; ADR-0123 usato sia da #371 sia dai commit locali di #370.

**Why:** la memoria ha un limite e la CI non la vede; la storia serve per regressioni e per rivedere soluzioni già adottate.
**How to apply:** prima di accorciare MEMORY.md controlla/archivia; per la storia di una PR o ADR interroga lo script; in ogni PR col changelog aggiungi la voce MS (due PR in parallelo: la seconda rinumera).

2026-11-18 (thread «Rendere obbligatoria la memoria storica»): audit e ADR-0137 in PR #471 (bozza, MS-0166). Misure: 88/90 PR col changelog hanno voce; 0/98 voci nate fuori da una PR; `--pr` ora ricava il numero dal merge (37→90/90, solo per le voci nate dal changelog); `--confronta-memoria DIR` dà 84 righe di memoria non nel repo e 41/77 note citate. Jfs ha scelto il 18/11 la coda per thread in /mnt/project-files/memoria-storica-coda/ + routine del lunedì (testo istruzioni in /mnt/project-files/memoria-storica-2026-11-18/PROPOSTA-ISTRUZIONI.md). Regole phd (incollate da Jfs) confrontate punto per punto nell'ADR.
2026-11-18 pomeriggio: #471 unita (44f0cbc7). Jfs ha chiesto il cancello del punto 3: PR #480 (bozza) con `scripts/memoria_coda.py DIR --check | --thread "Titolo" | --threads elenco.json | --piega | --nome "Titolo"`, ADR-0138, MS-0167…0172. Coda e istruzioni: /mnt/project-files/memoria-storica-coda/LEGGIMI.md. Limiti dichiarati: non parte da solo, non vede card chiuse in thread aperti.

18/11: #480 unita (merge da04ea71, ADR-0138, MS-0169…0180). Cancello della coda: `python3 scripts/memoria_coda.py /mnt/project-files/memoria-storica-coda/ --thread "Titolo"` prima di risolvere un thread; lunedì `--check`, `--threads elenco.json`, `--piega`. Dentro anche la rilettura per intero dei 13 thread risolti 12-17/11 (sei voci). La piega si ferma se un file della coda è senza testa «### MS-???? · data · titolo» (caso vero del 18/11: script-flux-4050.md): si corregge il file, non si aggira il cancello.
Da fare alla prossima piega del lunedì: segnare ADR-0138 in plans/adr-prenotati.json (promemoria anche nel LEGGIMI della coda).
