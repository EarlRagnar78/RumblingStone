# Quiz a due agenti su `ARC07-DEF-4` — prima e dopo F3

La prima esecuzione del quiz
([`quiz-a-due-agenti.md`](../../../skills/rumblingstone-playtest/references/quiz-a-due-agenti.md)),
sulle stesse due versioni della seconda lettura a freddo: `ddd683c`, prima delle
correzioni, e il testo di oggi. Quattro agenti nuovi: due hanno letto un modulo
ciascuno e scritto gli appunti, due hanno risposto con i soli appunti. Le
risposte a libro aperto sono di due agenti ancora diversi, con il modulo davanti.

## I conti

Chiave: [`plans/quiz/ARC07-DEF-4.json`](../../quiz/ARC07-DEF-4.json), 14 domande,
**stato «bozza»**: finché il DM non la approva, i numeri qui sotto misurano
anche la chiave.

| | prima (`ddd683c`) | dopo (oggi) |
|---|---:|---:|
| Parole degli appunti | 400 | 386 |
| Giusta dagli appunti | 5 | 6 |
| Giusta solo a libro aperto | 5 | 8 |
| **Sbagliata anche a libro aperto** | **4** | **0** |

Le risposte, domanda per domanda, sono in `prima-PUNTEGGIO.txt` e
`dopo-PUNTEGGIO.txt`, e si rigenerano con `quiz_lettura.py` dai file
`*-RISPOSTE-*.json` di questa cartella.

## Cosa dicono

**La riscrittura ha chiuso i buchi.** Quattro domande erano senza risposta anche
con il modulo aperto: dove si comprano pozioni e incantesimi (q6), come si
richiama il drago (q10), cosa fa la soglia a un nano invisibile (q11), chi è il
capitano delle mura (q13). Nel testo di oggi le risposte ci sono tutte e quattro.

**Non ha reso il modulo più facile da ricordare.** Dagli appunti si passa da 5 a
6: una domanda sola, con un campione di un lettore per versione, è rumore. Il
testo di oggi contiene di più, e la quota che resta dopo una lettura è rimasta
la stessa.

**Quello che manca dagli appunti non è a caso.** Tutti e due i lettori hanno
riempito i loro 400 parole di CD, tacche e punti ferita, e tutti e due hanno
lasciato fuori le stesse tre cose:

| Domanda | Prima | Dopo |
|---|---|---|
| q1 · dove li lascia il portale | non c'è | non c'è |
| q4 · **cosa chiede il re, e quando** | non c'è | non c'è |
| q12 · chi è l'incappucciato, chi diventerà | confuso con Zeth | non c'è |

La q4 è la missione della serata. Un DM che ha letto il modulo una volta sa le CD
della targa e non sa cosa il re chiede ai PG. È un'osservazione su due lettori, e
va presa per quello; ma è la stessa in entrambi, e coincide con la domanda di
modulo del lettore a freddo che la rubrica non misurava ancora: *«in tre frasi,
che cosa succede?»*.

## I falsi negativi, contati a mano

Il protocollo lo chiede alla prima esecuzione di ogni chiave. Tre casi:

| Domanda | Risposta | Esito | Cosa si è fatto |
|---|---|---|---|
| q14 | «intervengono gli **avi**» · «lo salvano gli **avi**» | giusta, la chiave conosceva solo «antenati» | aggiunte le alternative `avi+interven`, `avi+salv` |
| q11 | «la soglia **smaschera** i nani» | giusta, la chiave voleva «visibili» o «epurare» | aggiunta l'alternativa `smaschera` |
| q8 | «vuole che si dica **"dite che c'ero"**» | **aperta** | nessuna: è una scelta di canone, al DM |

La q8 chiede cosa vuole Balvar. Il modulo gli dà due desideri: che Hammerfist
cada in fretta, per risparmiarle un assedio di fame, e che qualcuno ricordi che
lui c'era. La chiave accetta solo il primo; tutti e due i lettori hanno annotato
solo il secondo. Se il DM considera giusto anche il secondo, la chiave si
allarga e i conti sopra salgono di uno per parte.

## Cosa propone questo esperimento, e cosa no

- **Propone** di mettere in testa a ogni master un riquadro *La serata in tre
  frasi* (dove si arriva, cosa chiede chi, cosa succede se non lo si fa), e di
  rifare il quiz dopo. È un intervento di contenuto su DEF-4: lo decide il DM.
- **Non prova** che la riscrittura sia stata inutile: ha tolto quattro buchi che
  un tavolo avrebbe trovato. Prova che *chiudere buchi* e *farsi ricordare* sono
  due lavori diversi, e che il secondo non si fa da solo.
- **Non vale per le persone.** Un agente che scrive 400 parole sceglie in modo
  diverso da un DM. Il limite è dichiarato nel protocollo, e resta.
