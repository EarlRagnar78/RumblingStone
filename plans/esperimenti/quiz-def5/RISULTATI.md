# Quiz a due agenti su `ARC07-DEF-5` — il passo 7

Il quiz
([`quiz-a-due-agenti.md`](../../../skills/rumblingstone-playtest/references/quiz-a-due-agenti.md))
è il passo 7 del ciclo del master per DEF-5 (F4 di
[LETTORE-PLAYTESTER](../../PIANO-LETTORE-E-PLAYTESTER.md)). Tre agenti nuovi,
uno alla volta: il primo ha letto il modulo e scritto gli appunti, il secondo ha
risposto con i soli appunti, il terzo con il modulo aperto.

## I conti

Chiave: [`plans/quiz/ARC07-DEF-5.json`](../../quiz/ARC07-DEF-5.json), 12 domande,
**approvata dal DM il 2026-10-15**.

| | DEF-5 |
|---|---:|
| Parole degli appunti | 351 |
| Giusta dagli appunti | 10 |
| Giusta solo a libro aperto | 2 |
| **Sbagliata anche a libro aperto** | **0** |

Le risposte, domanda per domanda, sono in `PUNTEGGIO.txt` e si rigenerano con
`quiz_lettura.py` dai due file `RISPOSTE-*.json`. Ho riletto a mano le dodici
coppie: nessun falso positivo, **un falso negativo** (q4, sotto). Il DM ha
allargato la chiave il 2026-10-15 e il correttore ora conta **10 su 12**.

## Cosa dicono

**Nessun buco.** Con il modulo aperto tutte e dodici le risposte ci sono.

**Il racconto della serata resta negli appunti.** Al contrario di DEF-4, dove
tre lettori su tre avevano perso la missione del re, qui il lettore ha tenuto
dove arrivano, chi è sull'altare, come finisce la serata, dove porta il
portale e cosa si consegna prima. DEF-5 è corto (tre scene) e la sua ossatura
sta nel §0-bis.

**Le tre che il correttore dava per sepolte**, e cosa ne faccio:

| Domanda | Perché si perde | Esito |
|---|---|---|
| q3 · chi parla per primo | la battuta di Dana («Sono tornati.») sta in mezzo alla Scena 2, dopo gli effetti | resta: è una battuta, il DM la trova quando legge la scena |
| q4 · cosa fa l'aura agli orchi | non si perde: gli appunti dicono «Volontà CD 25: uno o due restano scossi, gli altri fuggono», e la chiave accetta «volont» o «25» solo insieme a «panico» | falso negativo del correttore. La chiave accetta ora anche `['volont', 'fugg']` (DM, 2026-10-15, D90) |
| q8 · il costo dei due Treant | sta in una cella di tabella, nella riga di Hella | resta, ma ora la cella dice cos'è l'Evocazione (era il rilievo del terzo agente) |

## Le ambiguità trovate a libro aperto, e cosa ho corretto

Il terzo agente ha segnalato sette punti. Quelli che il testo risolve da sé li
ho corretti nel modulo. Nessuno cambia il canone, ma la q7 riformula una riga
marcata D77 («si rialza, con qualunque cura sopra gli 8 pf»): l'ho letta come
«si rialza anche a 8 pf», e il DM l'ha confermata il 2026-10-15 (D90).

| Domanda | Rilievo | Esito |
|---|---|---|
| q2 | la legenda di CM-1 diceva Re Thorek «stabilizzato» prima dell'Apparizione | la legenda dice ora che l'acido lo consuma finché l'Apparizione non lo ferma |
| q4 | gli hobgoblin «immuni a paura» in tabella, «entrano dopo l'aura» nella Scena 3 | la tabella dice che nella regia breve entrano dopo, e l'aura non li tocca comunque |
| q7 | cosa rimette in piedi il re: solo *ristorare*, o anche *guarigione*; e da affaticato | la Scena 3 dice ora *ristorare* o *guarigione*, e che da affaticato si rialza già; il §6 dice che si rialza anche a 8 pf |
| q9 | il §6 diceva «il resto della tabella resta uguale», la Scena 3 cambia la riga dei nemici | il §6 rimanda alla Scena 3 per la riga dei nemici |
| q12 | la tavola dell'Affresco A8 senza un momento di consegna | la Scena 3 la consegna prima del portale, con lo Stato dei Custodi |
| q8 | «l'Evocazione» non spiegata | detta per esteso: l'Evocazione dei Guardiani della Collana |
| q1 | due regie e due orologi | resta: il modulo li spiega tutti e due (§0-bis e CM-1), ed è canone (D31) |

Il quiz non si ripete: le correzioni aggiungono parole senza toglierne, e il
precedente di DEF-4 mostra che un quiz ripetuto su un testo arricchito non
cambia il conto degli appunti.
