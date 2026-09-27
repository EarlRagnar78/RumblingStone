# ADR-0075 — Il ciclo del master vale per ogni piano

- **Stato**: accettata
- **Data**: 2026-09-27
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: il DM, prima di A3 di PIANO-MASTER-DEF: *«l'arco 07 è
  davvero completo anche con le nuove regole? ci hai fatto una passata anche
  con developer e playtester? […] tutti i piani da fare devono tenere conto di
  queste cose, sia quelli presenti in questo piano sia gli altri, se implicano
  una riscrittura o applicazione di stile»*
- **Rapporti**: raccoglie in una sequenza sola ADR-0073 (il contratto «In
  scena»), ADR-0074 (il master come componenti), le domande del developer
  (`sviluppo-degli-incontri.md`, da RICERCA-MANUALE-DEL-MASTER) e il collaudo a
  freddo di `rumblingstone-playtest`

## Contesto

Fra il 25 e il 27 settembre il repo ha preso quattro regole nuove sul master:
il contratto «In scena», i componenti con l'apparato generato, le domande del
developer, la lettura a freddo con il quiz. Ognuna è arrivata col suo ADR, il
suo strumento e il suo cancello, e ognuna è stata applicata a **un solo
master**, `ARC07-DEF-4`.

La domanda del DM era se questo bastasse. Misurato il 2026-09-27:

| Master di ARC-07 | Scene `### SCENA` | Contratto | Apparato | Box > 12 righe | Lettura a freddo |
|---|---:|---|---|---:|---|
| DEF-1 | 0 | no | no | 6 | no |
| DEF-2 | 0 | no | no | 1 | no |
| DEF-3 | 0 | no | no | 0 | no |
| DEF-4 | 13 | sì | sì | 0 | sì, con quiz |
| DEF-5 | 0 | no | no | 1 | no |

I cancelli in CI sono verdi su tutti e cinque, per due ragioni diverse. Su
DEF-1, 2, 3 e 5 il contratto è spento da un profilo dichiarato in
`plans/copertura-scene.json`, con la ragione scritta (lotto F4 di
PIANO-LETTORE). Questa è onestà. La seconda ragione no: `copertura_scene` e la
parte per scene di `domande_developer` riconoscono una scena **solo** dal
titolo `### SCENA`. Un master di prova senza quel titolo, con un PNG che parla
senza scheda e nessun box, ha avuto **zero rilievi**. Il cancello non l'aveva
visto.

E i piani aperti che riscrivono contenuto (MESTIERE-BANCHI, MASTER-DEF,
INDAGINE, MARCATURA, DRAPPO) non nominavano nessuna delle quattro regole: erano
stati scritti prima, o le citavano una alla volta.

## La decisione

1. **Una sequenza sola.** `rumblingstone-module-standard` porta il **ciclo
   completo** in sette passi: scene riconoscibili, contratto, componenti,
   developer, box al metro, lettore e playtester a freddo, quiz. Un master è DEF
   quando li ha fatti tutti; con i soli cancelli è alfa. Vale per ogni arco
   diviso in DEF e per ogni stand-alone (ADR-0017). Il developer e il
   playtester sono obbligatori: un passo si salta solo con una decisione del DM
   scritta nel piano. Il DM, lo stesso giorno: *«nelle skill e l'ADR ci va come
   giro obbligatorio la parte del developer e del playtester, sia per tutti gli
   archi e gli stand-alone che vengono divisi in DEF»*.
2. **I piani la citano, non la copiano.** Un lotto che scrive, riscrive o
   rifinisce nello stile un master, un modulo o uno stand-alone dichiara nella
   colonna «qualità» i passi del ciclo, per numero, e quali salta e perché. La
   regola sta in `rumblingstone-plans`, dove la legge chi apre o aggiorna un
   piano.
3. **ARC-07 non è completo, e lo si dice.** Il lotto F4 di PIANO-LETTORE si
   allarga dal solo contratto al ciclo intero, e va **prima** di A3 di
   PIANO-MASTER-DEF: ARC-08 comincia dove finisce DEF-5, che è anche il
   prossimo master al tavolo.
4. **Il buco del cancello diventa un lotto**, non una nota: un master
   `ARC*-DEF-*` con zero scene riconosciute deve essere un rilievo (F6 di
   PIANO-LETTORE).

## Le conseguenze

- Una regola nuova sul master, da oggi, entra nel ciclo o non è arrivata: il
  ciclo è l'unico posto che i piani leggono.
- Quello che si paga: ogni lotto di riscrittura costa di più. Una sidebar
  aggiunta a DEF-1 passa per contratto, componenti e lettura a freddo, e DEF-1
  non ha ancora le scene nel formato che i cancelli vedono. La prima volta si
  paga la conversione.
- I passi 6 e 7 restano fuori dalla CI: sono letture di un agente, e un
  cancello su un giudizio sarebbe rumore (ADR-0073). Li tiene in vita il piano,
  che non chiude il lotto senza di loro.
- Il tetto delle 12 righe resta una misura e non un cancello, finché i master
  esistenti non ci stanno: oggi sarebbe rosso su tre master di ARC-07 su
  cinque, e un cancello sempre rosso viene spento. È la lezione di
  `validate_modules.py` sui punti 15-16.
