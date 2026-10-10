# ADR-0087 — La memoria del lavoro è un file generato, non una copia

- **Stato**: **accettata** (il DM, il 2026-10-10, fra tre strade: *«Nel repo, generata»*)
- **Data**: 2026-10-10
- **Decisori**: DM (Gianfranco Samuele), agente
- **Rapporti**: estende [ADR-0047](ADR-0047-le-decisioni-aperte-hanno-una-casa-sola.md) (le decisioni hanno una casa sola, l'aggregato si genera) a tutto quello che serve per ripartire; si appoggia a [ADR-0077](ADR-0077-revisione-a-due-giri.md) per le revisioni della prosa in attesa

## Contesto

Il DM: *«creare un progetto così tutta la memoria si raccoglie in un posto e
il lavoro si aggiorna senza perdere parti o decisioni»*.

Le sessioni d'agente sono effimere. Lo scratchpad di questa sessione aveva
uno script utile (riportare una revisione su un originale cambiato) che non
era in nessun posto del repo; la chat si riassume e perde i dettagli. E fra
il 3 e il 10 ottobre è successo il caso peggiore: due sessioni hanno deciso
D39 in due modi diversi, (a)+(b) su un ramo e (b) su `main`, perché nessuna
vedeva quello che l'altra aveva chiuso.

Le informazioni per ripartire ci sono già, ognuna con la sua casa: le
decisioni nelle tabelle dei piani (ADR-0047), la lista viva in
STATO-E-ORDINE §0, il CHANGELOG, il registro dei miglioramenti, i documenti di
revisione da approvare. Il difetto è che sono in cinque posti, e chi riparte
deve sapere dove guardare.

Le strade considerate:

| Strada | Pro | Contro |
|---|---|---|
| **A · un file nel repo, generato** | versionato, nessuna copia, la CI lo tiene allineato | si legge su GitHub o nel repo, non come documento vivo |
| B · un documento Claude Docs | si legge e si commenta dal telefono | è una seconda copia: se nessuno la aggiorna si allontana, e il repo vince comunque |
| C · tutte e due | comodo | il documento va riallineato a ogni sessione, cioè B col suo difetto |

## Decisione

1. **`MEMORIA.md`, nella radice, generato da `scripts/memoria.py`.** Lo script
   non scrive niente di suo: legge le fonti e le mette in fila. Prima cosa
   aspetta il DM (le decisioni aperte, le revisioni da approvare, le righe 🙋),
   poi da dove riparte l'agente (▶, ⬜, 🟡), poi il CHANGELOG recente e le
   misure. Ogni sezione dice la sua fonte e il link porta lì.
2. **Si corregge la fonte, mai la memoria.** Una riga sbagliata in `MEMORIA.md`
   è una riga sbagliata in un piano.
3. **Il cancello**: `memoria.py --check` in CI. Se un piano cambia e la memoria
   no, la CI è rossa. Il file non porta date di generazione: lo stesso repo dà
   lo stesso file, byte per byte.
4. **Lo scratchpad non tiene niente che serva**: quello che una sessione scopre
   e serve ancora entra nel repo prima della fine. Il primo caso è
   `ciclo_prosa.py rigenera`, che riporta le modifiche di una revisione su un
   originale cambiato.
5. **La sessione nuova parte da qui**: `AGENTS.md` e STATO-E-ORDINE §14.6 lo
   dicono come primo passo.

## Conseguenze

- Una PR che chiude un lotto, apre una decisione o aggiunge una revisione da
  approvare rigenera `MEMORIA.md` nello stesso commit, come già fa con
  `decisioni_dm.py --emit`. Chi lo dimentica lo scopre dalla CI.
- Due rami che toccano i piani si contendono `MEMORIA.md` al merge. Il
  conflitto non si risolve a mano: si rigenera.
- La memoria non impedisce che due sessioni decidano la stessa cosa in due
  modi, come per D39: lo rende visibile, perché la decisione chiusa compare
  sparita dall'elenco degli aperti nella prima sessione che rigenera.
- Quello che si paga: una riga in più nella CI e un file in più in radice. Una
  lettura comoda dal telefono (la strada B) resta possibile in futuro come
  vista di questo file, mai come sua copia.
