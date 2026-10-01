# Il DM a freddo — rubrica fissa

Il lettore cerca dove il DM dovrebbe inventare, il playtester cosa succede
quando i giocatori fanno quello che vogliono. Il DM a freddo è la terza
domanda: **un DM che non ha scritto il modulo riesce a condurlo stasera, con il
tempo che ha davvero per prepararlo?**

È un altro lettore, perché un DM vero non legge il master dall'inizio alla
fine come il lettore a freddo. Prima lo sfoglia per capire di che serata si
tratta, poi lo prepara con un tempo limitato, poi lo conduce ricordando quello
che ha preparato. Ognuno dei tre momenti ha i suoi buchi.

La forma viene da `first-reader` di awesome-llm-apps (ADR-0076), che fa
passare un testo per chi scorre, chi legge senza guardare avanti e chi ricorda
il giorno dopo. Qui le tre letture sono le tre fasi della preparazione di un
DM (D2 di PIANO-AGENT-SKILLS-ESTERNE).

⚠️ **Stato: in prova.** Il primo passo è stato provato sui cinque DEF di ARC-07
il 2026-10-01 (`plans/esperimenti/dm-a-freddo/`); il secondo e il terzo usano
gli strumenti di L1 e L2 e non hanno ancora una corsa completa. Finché il DM non
decide (D9 di PIANO-AGENT-SKILLS-ESTERNE), il DM a freddo **non** è un passo
obbligatorio del ciclo del master.

## Primo passo · la vista di chi scorre

```
python3 scripts/vista_di_chi_scorre.py <master>
```

stampa quello su cui l'occhio si ferma: la serata dichiarata (il riquadro *La
serata in tre frasi*, o il primo paragrafo del Quickstart), i titoli, la riga
«In scena» e la prima frase di ogni scena, i grassetti, le CD. Il testo intero
no, di proposito. Un agente **nuovo** riceve solo la vista e risponde a quattro
domande:

1. cosa succede stasera, in tre frasi;
2. chi si oppone ai PG, e cosa vuole;
3. cosa devo preparare prima di sedermi al tavolo;
4. quale elemento della vista mi ha fatto rispondere.

Le risposte si mettono accanto al master. «Non lo so» è lecito e vale un
rilievo, con il codice:

| Codice | Quando scatta |
|---|---|
| `D-SERATA` | la risposta 1 manca o sbaglia la missione: il master non dichiara la serata, o la dichiara in un punto che chi scorre non vede |
| `D-AVVERSARIO` | la risposta 2 manca o sbaglia chi si oppone |
| `D-PREPARA` | la risposta 3 non nomina cose che il master richiede (statblocchi fuori dal file, mappe, handout, un orologio) |
| `D-RUMORE` | la risposta 4 cita un elemento che non dice niente della serata: un grassetto di servizio, un'etichetta d'apparato |

## Secondo passo · la preparazione a scene

Il DM a freddo legge con `lettura_a_scene.py` (`lettore-a-freddo.md`, «La
lettura a scene»), con il messaggio d'invio del lettore e due differenze:

- dichiara in testa il **tempo di preparazione** che ha: un'ora è il caso
  normale. Se finisce il tempo, smette, e il punto in cui smette è un rilievo;
- nel campo `so adesso` scrive **cosa ha preparato**, non cosa sanno i PG: un
  appunto, una pagina segnata, un incontro da tenere aperto.

## Terzo passo · il giorno dopo, al tavolo

`ricordo_lettura.py domande` sul suo diario, con un agente nuovo, e tre domande
in più che fa solo chi conduce, passate con `ricordo_lettura.py chiedi`:

- *chi entra per primo in scena, e cosa dice?*
- *se i giocatori chiedono di \<una cosa che il master prevede\>, cosa rispondo,
  e dove lo trovo?*
- *dove ho dovuto tornare indietro, e quanto tempo ho perso?*

Una risposta che non si trova nel diario è un rilievo sul master. Una che il
diario ha e il master no è un'invenzione del DM, e va segnata come tale.

## L'uscita

La stessa tabella delle altre due rubriche:

```
| # | Passo | Codice | Cosa manca | Gravità | Prova |
```

Gravità: 🔴 *la serata non si capisce senza leggere tutto* · 🟠 *il DM perde più
di 30 secondi a cercare* · 🟡 *se ne accorge un DM attento*. La prova è la riga
della vista, del diario o della risposta che rende evidente il buco.
