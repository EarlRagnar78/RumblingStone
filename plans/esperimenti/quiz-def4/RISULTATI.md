# Quiz a due agenti su `ARC07-DEF-4` — tre versioni

Le prime esecuzioni del quiz
([`quiz-a-due-agenti.md`](../../../skills/rumblingstone-playtest/references/quiz-a-due-agenti.md))
su tre versioni del modulo:

- **prima**: `ddd683c`, il testo giocato al tavolo, prima delle correzioni di F3;
- **dopo**: il testo del 2026-09-26, dopo F3;
- **riquadro**: il testo del 2026-09-27, col riquadro *La serata in tre frasi*
  in testa al §0 e la sezione «Chi non vola» nella Scena 11.

Per ogni versione un agente nuovo ha letto il modulo e scritto gli appunti, e un
altro ha risposto con i soli appunti. Le risposte a libro aperto sono di agenti
ancora diversi, con il modulo davanti; per la terza versione valgono quelle di
«dopo», perché il riquadro aggiunge testo senza toglierne.

## I conti

Chiave: [`plans/quiz/ARC07-DEF-4.json`](../../quiz/ARC07-DEF-4.json), 14 domande,
**approvata dal DM il 2026-09-27**.

| | prima | dopo | riquadro |
|---|---:|---:|---:|
| Parole degli appunti | 400 | 386 | 381 |
| Giusta dagli appunti | 6 | 6 | 6 |
| Giusta solo a libro aperto | 4 | 8 | 8 |
| **Sbagliata anche a libro aperto** | **4** | **0** | **0** |

Le risposte, domanda per domanda, sono nei file `*-PUNTEGGIO.txt` e si
rigenerano con `quiz_lettura.py` dai file `*-RISPOSTE-*.json` di questa
cartella. `test_quiz_lettura.py` fissa i tre conti.

## Cosa dicono

**La riscrittura ha chiuso i buchi.** Quattro domande erano senza risposta anche
con il modulo aperto: dove si comprano pozioni e incantesimi (q6), come si
richiama il drago (q10), cosa fa la soglia a un nano invisibile (q11), chi è il
capitano delle mura (q13). Dopo F3 le risposte ci sono tutte e quattro.

**Non ha reso il modulo più facile da ricordare, e il riquadro nemmeno.**
Dagli appunti restano 6 domande su 14 in tutte e tre le versioni.

**Quello che manca dagli appunti non è a caso.** I tre lettori hanno riempito
i loro 400 parole di CD, tacche e punti ferita, e tutti e tre hanno lasciato
fuori le stesse cose:

| Domanda | prima | dopo | riquadro |
|---|---|---|---|
| q1 · dove li lascia il portale | non c'è | non c'è | non c'è |
| q3 · chi comanda la fortezza | c'è | non c'è | non c'è |
| q4 · **cosa chiede il re, e quando** | non c'è | non c'è | **non c'è** |

La q4 è la missione della serata. Il 2026-09-27 il DM ha approvato il riquadro
*La serata in tre frasi*, che la dice nelle prime righe del §0. Il terzo lettore
l'ha avuta sotto gli occhi e non l'ha annotata.

## Il limite che il terzo quiz ha mostrato

Tre lettori su tre prendono appunti **procedurali**: quello che serve per fare
i tiri, non quello che serve per raccontare la serata. Con il riquadro in testa
la scelta non cambia, e questo sposta il sospetto dal modulo al lettore. Un
agente a cui si chiede *«appunti per condurre la serata»* annota le regole
perché pensa che la storia la ricorderà comunque, e poi il secondo agente non
la trova. Un DM vero, probabilmente, fa il contrario.

Quindi, per le domande di storia (q1, q3, q4), il quiz **non distingue** un
modulo che le seppellisce da un lettore che le salta. Per le domande di
procedura invece funziona, ed è lì che ha visto la differenza fra le versioni
(q6, q10, q11, q13). Il limite è scritto nel protocollo, alla voce «Il limite
osservato».

Il riquadro resta nel modulo: serve al DM, anche se il quiz non riesce a
vederlo.

## I falsi negativi, contati a mano

Il protocollo lo chiede alla prima esecuzione di ogni chiave.

| Domanda | Risposta | Esito | Cosa si è fatto |
|---|---|---|---|
| q14 | «intervengono gli **avi**» · «lo salvano gli **avi**» | giusta, la chiave conosceva solo «antenati» | aggiunte `avi+interven`, `avi+salv` |
| q11 | «la soglia **smaschera** i nani» · «una runa **anti-invisibilità**» | giusta, la chiave voleva «visibili» o «epurare» | aggiunte `smaschera`, `anti+invisibil` |
| q8 | «vuole che si dica **"dite che c'ero"**» | giusta per il DM | il 2026-09-27 il DM ha accettato **tutti e due** i desideri di Balvar (Hammerfist che cade in fretta, e qualcuno che dica che c'era); resta chiesto anche **chi è** |

## Cosa non prova

- **Non prova** che la riscrittura sia stata inutile: ha tolto quattro buchi che
  un tavolo avrebbe trovato. Prova che *chiudere buchi* e *farsi ricordare* sono
  due lavori diversi.
- **Non vale per le persone.** Un agente che scrive 400 parole sceglie in modo
  diverso da un DM, e il terzo quiz lo ha mostrato più chiaramente dei primi due.
