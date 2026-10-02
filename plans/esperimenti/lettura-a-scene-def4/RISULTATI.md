# Calibrazione della lettura a scene — DEF-4 del tavolo, 2026-10-01

Lotto L1 di [PIANO-AGENT-SKILLS-ESTERNE](../../PIANO-AGENT-SKILLS-ESTERNE.md).
Bersaglio: `ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` al commit `ddd683c`, il testo
che il DM aveva al tavolo il 2026-09-25 (lo stesso della calibrazione F2 di
PIANO-LETTORE). Due agenti nuovi, la stessa rubrica di oggi
(`lettore-a-freddo.md`), lo stesso giorno:

- **lettura intera**: il modulo in un file, letto dall'inizio alla fine
  ([`LETTURA-INTERA.md`](LETTURA-INTERA.md));
- **lettura a scene**: il modulo servito da `lettura_a_scene.py`, 17 passaggi,
  il diario obbligatorio, nessun percorso del file
  ([`LETTURA-A-SCENE.md`](LETTURA-A-SCENE.md), [`diario.jsonl`](diario.jsonl)).

## I numeri

| | Intera | A scene |
|---|---:|---:|
| Rilievi | 69 | 55 |
| 🔴 · 🟠 · 🟡 | 3 · 26 · 40 | 4 · 21 · 30 |
| `L-ORDINE` | 7 | 7 |
| delle sette lacune che il DM inventò al tavolo, quante trovate come rilievo | 3 (quartieri, gallerie, capitano) | 2 (chierico, capitano) |

**`L-ORDINE`, rilievo per rilievo, contati a mano.** In comune: 3 (la
Quick-Reference che usa il Nome e gli aiuti dimezzati prima di definirli; le
Cronache dei giocatori che compaiono solo al §9; i doni del re spiegati solo al
§8). Uno per parte si somiglia senza coincidere (il §6 che arriva dopo la Scena
12). Solo nella lettura intera: 3 (il tono del Rubino al §7, «FUGGITO» e «⅓ pf»
prima della Scena 11, la Luce di Lathander in appendice). Solo in quella a
scene: 3, e due sono più contraddizioni o mancanze che problemi d'ordine
(l'uscita dalla tenda mai scritta, la provenienza del Rubino).

**Il diario non ha guardato avanti.** Diciassette righe su diciassette
passaggi, con tutti i campi. L'unico rimando a una scena successiva («Scena 8»
nel diario della Scena 7) sta nel testo stesso della Scena 7.

## Cosa dice, e cosa no

- **L'ipotesi non regge su questo caso.** La lettura a scene non ha trovato più
  `L-ORDINE` di quella intera (7 e 7), ne ha trovati di diversi, e ha trovato
  meno rilievi in tutto (55 contro 69) e una lacuna del tavolo in meno (2 contro 3).
- **Il guadagno su `L-ORDINE` viene dalla rubrica.** La lettura intera di
  settembre (F2, rubrica di allora) ne trovava 3 sullo stesso testo; quella
  intera di oggi 7. Fra le due è cambiata la rubrica (le domande fisse per
  scena, F7), non il modo di leggere.
- **Il diario serve ad altro.** È la memoria del lettore: il ricordo del passo
  7 e le domande dopo la lettura (L2) ci lavorano sopra, e la lettura intera
  non ne produce uno.
- ⚠️ **Un caso solo per modo.** Due letture dello stesso testo non danno lo
  stesso elenco (PIANO-LETTORE §2): questa è una misura, non una legge. Nessun
  controllo sulle invenzioni: la scena di controllo prevista dal piano non c'è,
  perché nessuna scena di questo DEF-4 è senza difetti noti.

Decisione al DM: D8 di PIANO-AGENT-SKILLS-ESTERNE.

## Il ricordo dal diario (L2)

Lo stesso diario della lettura a scene, dato a due agenti nuovi che non hanno
visto il modulo: uno ha risposto alle 14 domande del quiz
(`diario-RISPOSTE-QUIZ.json`), l'altro alle sette del ricordo
(`diario-RICORDO.json`). Le risposte a libro aperto sono quelle di settembre
sulla stessa versione (`quiz-def4/prima-RISPOSTE-APERTO.json`).

| | appunti (settembre) | diario |
|---|---:|---:|
| Parole | 400 | 3.582 |
| Giusta dalla memoria | 6 | 8 |
| di cui q4, la missione | no | **sì** |

Cambiano quattro risposte: q1, q4 e q12 diventano giuste, q8 (chi è Balvar)
diventa sbagliata. La missione, che tre lettori su tre avevano perso a
settembre, dal diario c'è: nel quiz e nella prima risposta del ricordo.

⚠️ **Il confronto non è pari.** Il diario è nove volte più lungo degli
appunti: il guadagno può venire dalla quantità di testo, non dalla forma. Il
quiz misura quanto resta, e il diario resta di più perché è di più. Quello che
la prova dice senza riserve è un'altra cosa: **chi riceve solo il diario sa dire
qual è la serata**, e il quiz su questo testo non ci riusciva.

Il ricordo trova cose che il quiz non chiede. Le sue risposte coincidono con
rilievi delle due letture: la prova centrale della traversata con quattro
regole diverse, il tono del Rubino deciso in quattro posti, il punto d'arrivo
che l'atlante e la Scena 1 danno diversi, la runa e la Catena che spariscono
dal duello.

L'intenzione dichiarata di questa versione non serve come metro:
`ricordo_lettura.py intenzione` su `ddd683c` restituisce il primo paragrafo
del Quickstart, che dice *dove* sono i PG e non *cosa* devono fare. Il
riquadro *La serata in tre frasi* è arrivato dopo, e senza di lui il giudizio
del ricordo non ha contro cosa misurarsi. È il motivo della norma del
registro: ogni master dichiara la sua serata.

