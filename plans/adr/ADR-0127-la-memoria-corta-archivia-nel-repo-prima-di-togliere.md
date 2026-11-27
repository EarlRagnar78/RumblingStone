# ADR-0127 — La memoria corta archivia nel repo prima di togliere una riga

**Stato**: proposta (2026-11-12); i tre livelli (addendum in CI, istruzioni del progetto, regola nella memoria e nei file d'avvio) approvati dal DM il 2026-11-12
**Data**: 2026-11-12
**Decisione-fonte**: il DM (Jfs), 2026-11-12: «come si può obbligare tutte le sessioni a questo comportamento, tipo quello del changelog? Tipo addendum?»; prima ancora: salvare in un file del repo, collegato al changelog, ciò che la riduzione della memoria del progetto aveva tolto, e farne un meccanismo che eviti sempre la saturazione e non perda informazioni storiche utili per una regressione o per rivedere una soluzione già adottata, con un modo di leggerlo quando serve.
**Rapporti**: affianca [ADR-0087](ADR-0087-la-memoria-del-lavoro-e-generata.md) (`MEMORIA.md` generata dal repo: stato aperto, non storia). Non tocca il changelog dei piani (una riga per lotto chiuso), a cui si collega.

## Contesto

Le sessioni d'agente leggono all'avvio una memoria del progetto che sta
fuori dal repo e ha un limite di dimensione (circa 16 KB per l'indice, 4 KB
per nota). Il 2026-11-12 l'indice è passato da circa 25 KB a 8 KB togliendo
la cronologia delle PR unite. Il confronto riga per riga della versione
lunga col repo ha dato:

- 165 riferimenti distinti (PR, SHA, ADR, percorsi della cartella condivisa):
  127 già nel repo, 24 solo nelle note di memoria, 14 da nessuna parte
  (tra questi gli SHA di merge di #256, #257, #258, #260, #285, #298 e i
  percorsi dei PDF delle serate);
- 150 fatti di contenuto cercati per testo: 24 non trovati nel repo (per
  esempio l'ora della routine settimanale, le milestone v1.1.0…v1.5.0, la
  card «guida agenti» ritirata, l'artifact dei 152 termini sconosciuti).

Il changelog dei piani non poteva tenerli: ha una riga per lotto chiuso e
non registra le regole di lavoro, le aperture al DM, le scelte fatte in
chat né i numeri che la memoria si portava dietro. `MEMORIA.md` è generata
e mostra solo ciò che è aperto.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **File Markdown in `plans/`, una voce per riga tolta e per PR col changelog, con campi fissi, un lettore stdlib, un cancello di forma e l'addendum obbligatorio al merge** (scelta) | è lo standard del repo (Markdown + script stdlib + `--check`); si legge su GitHub e con `grep`; il lettore filtra per PR, ADR, tema e data; esposto via MCP senza codice nuovo nel server | dipende dal fatto che chi toglie una riga la archivi; la ricerca è per parole, non per significato |
| Tenere la cronologia dentro la memoria | nessun file nuovo | è la saturazione che si voleva evitare: la memoria torna sopra il limite |
| Righe in più nel changelog dei piani | un file solo | il changelog ha cinque colonne e un controllo di forma; righe che non sono lotti lo sporcano e `memoria.py` le mostrerebbe come lavoro fatto |
| SQLite o indice semantico (embedding) | ricerca per significato | un binario o un modello in più; il file non si legge più in una PR; per 67 voci la ricerca per parole e campi basta (ADR del 2026-11-08: si parte dallo standard di fatto) |
| Solo la regola per le sessioni, senza addendum in CI | nessun lavoro in più per PR | è la regola che il 2026-11-12 non era bastata: la riduzione della memoria aveva tolto 38 riferimenti e 24 fatti che il repo non aveva |
| Copiare nel repo tutte le note di memoria | niente resta fuori | le note sono vive e contengono dati personali; la regola le archivia quando escono, non prima |

## Decisione

1. **Il file**: [`plans/MEMORIA-STORICA.md`](../MEMORIA-STORICA.md). Una
   voce `MS-NNNN · data · titolo` per riga tolta dalla memoria, con i campi
   Data, PR, ADR, Temi, Origine, Testo (obbligatori) e Trovato nel repo,
   Fuori dal repo, Note di memoria, Solo qui (facoltativi). Si aggiunge in
   coda, non si riassume e non si riscrive.
2. **Scrittura, obbligatoria al merge (addendum del changelog)**: una PR
   che aggiunge righe a `plans/CHANGELOG.md` aggiunge anche almeno una voce
   in coda al file storico, con le decisioni, le misure, le questioni aperte
   e i rimandi che la riga del changelog non tiene.
   `check_plans_discipline.py` la boccia in CI se manca, come boccia una
   modifica strutturale senza riga del changelog. Così la storia è nel repo
   prima che qualcuno accorci la memoria delle sessioni.
3. **Scrittura, per regola**: prima di togliere una riga dalla memoria del
   progetto, la sessione che la toglie controlla che i suoi fatti siano qui
   e, se mancano, li archivia nello stesso giro. La regola sta
   nell'intestazione della memoria del progetto, in
   [`AGENTS.md`](../../AGENTS.md), nel modello delle PR e nel file stesso.
4. **Lettura**: `python3 scripts/memoria_storica.py` filtra per `--pr`,
   `--adr`, `--tema`, `--da`/`--a`, `--id` e parole; `--json` per un
   agente. È nel manifest dei tool, quindi nel server MCP in sola lettura.
   `MEMORIA.md` lo indica in «Come si riparte» e in «Dove vive ogni cosa»,
   con il numero di voci.
5. **Cancello di forma**: `memoria_storica.py --check` in CI: numeri consecutivi,
   date valide, campi obbligatori, e `plans/CHANGELOG.md` che porta al file.
6. **Dati personali**: nomi dei giocatori, macchine e nomi utente non entrano
   (scelta del DM del 2026-11-12); restano nelle note di memoria.

## Conseguenze

- Le 67 righe della memoria lunga sono nel repo (MS-0001…MS-0067): i 165
  riferimenti e i 24 fatti di contenuto prima assenti ora si ritrovano.
- La memoria del progetto può restare piccola: la storia ha un posto senza
  limite.
- **Obbligato e no.** Delle 67 righe della memoria lunga, 53 nascevano da
  una PR: con l'addendum sarebbero entrate nel repo al merge. Le altre 14
  (regole di lavoro del DM, ambiente e rete del container, routine,
  roadmap, milestone, schieramenti decisi in chat) non passano da una PR e
  restano affidate alla regola del punto 3: la memoria la scrivono più
  sessioni e la CI non la vede, perché sta fuori dal repo.
- L'addendum controlla che una voce ci sia, non che dica tutto: una voce
  vuota di sostanza passa. Lo SHA del merge non può stare nella PR stessa
  (nasce dopo): resta nel changelog dei piani o in una voce successiva.
- Due PR aperte insieme aggiungono la stessa `MS-NNNN` in coda: chi arriva
  seconda rinumera al riallineamento, come già succede per le righe del
  changelog. Il `--check` lo segnala.
- La ricerca è per parole e campi: un fatto scritto con altre parole non si
  trova cercando la parola sbagliata. Il campo Temi e il titolo servono a
  questo.

## Da rivedere se

- le voci superano qualche migliaio e il file non si legge più su GitHub
  (allora un file per anno, stesso formato);
- una regressione non trova la sua storia per un difetto della ricerca per
  parole (allora si misura un indice, prima di adottarlo);
- la memoria del progetto entra nel repo: il cancello potrà confrontare le
  due e controllare davvero la regola del punto 3;
- l'addendum produce voci che ripetono la riga del changelog senza
  aggiungere nulla (allora si misura se tenerlo bloccante).
