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
il 2026-10-01 (`plans/esperimenti/dm-a-freddo/`); il secondo e il terzo hanno
una corsa intera su DEF-5 (`corsa-def5/`): 13 rilievi, 2 nuovi rispetto a
lettore e playtester, e un peso diverso su quelli già noti.

**Cosa è obbligatorio (D9, deciso il 2026-10-01).** Il **primo passo** è
obbligatorio al passo 6 del ciclo del master, accanto a lettore e playtester:
`registro_letture.py` non mette un master sotto cancello finché non ha anche la
lettura `dm` con l'impronta del testo. Il secondo e il terzo passo restano **in
prova**: il DM ha letto la preparazione di
`plans/esperimenti/dm-a-freddo/corsa-def5/PREPARAZIONE.md` e ha detto che la
sua ne copre molto di più (D12, 2026-10-01). Le undici voci qui sotto vengono
da quella risposta, ed escono dalla prova dopo una corsa che le esegue tutte.

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
  appunto, una pagina segnata, un incontro da tenere aperto, e **chi parla per
  primo, con la prima battuta**. La corsa su DEF-5 senza quest'ultima riga ha
  lasciato il giorno dopo a «non è rimasto niente» su chi entra in scena,
  anche se il master le schede d'entrata le aveva.

### La preparazione del DM, voce per voce (D12)

La prima corsa su DEF-5 ha fatto una cosa sola: leggere il master e annotare
dove il DM dovrebbe inventare. Il DM, leggendola:

> *«Nella preparazione che avrei fatto io oltre a vedere e risolvere tutti
> questi problemi ,avrei visto lo stato del gruppo  cosa sanno e cosa no e
> dell avventura cosa il mondo sa o cosa si muove anche senza i pg da solo
> […] stando bene attento a dividere quello che I pg sanno da wuellonche sa
> il master»* (2026-10-01, trascritto com'è arrivato)

Quindi la preparazione non è una lettura: sono undici lavori, e ognuno chiude
con un esito nella tabella d'uscita (fatto · manca nel repo · rilievo sul
master). Il tempo dichiarato resta, e una voce che non entra nell'ora è un
rilievo, non un salto.

| Codice | La voce | Dove si guarda |
|---|---|---|
| `P-RILIEVI` | vedere **e risolvere** i problemi del master, non solo elencarli: per ognuno, la risposta che si darebbe al tavolo | la lettura a scene qui sopra |
| `P-GRUPPO` | lo stato del gruppo: cosa sanno i PG e cosa **non** sanno | `campaign/state.md`, gli echi, i DEF precedenti |
| `P-MONDO` | cosa sa il mondo, e cosa si muove **senza i PG** | orologi del master, agenda dei villain, `living-world.md` |
| `P-STATO` | in che stato sono PG, PNG, villain e luoghi all'inizio della serata | `state.md`, `Bestiario/`, la coda del DEF precedente |
| `P-STILE` | le descrizioni e lo stile già fissati, comprese le immagini già generate (Canva AI, quelle del Drappo) | `rumblingstone-art-direction`, le schede-personaggio |
| `P-IMMAGINI` | le immagini che servono e non ci sono nel repo: si generano, o si elencano se la corsa non può | il master (§ immagini) contro i file presenti |
| `P-HANDOUT` | gli handout da dare ai PG che non ci sono: si scrivono | il master (§ handout) contro i file presenti |
| `P-FLUSSO` | rileggere il DEF per il flusso e per le opzioni che lascia aperte | il master intero, dopo la lettura a scene |
| `P-DOMANDE` | provare a rispondere alle domande più disparate dei PG, e annotare dove si trova la risposta | la lettura intera; il giorno dopo le rimette alla prova |
| `P-CONGEGNI` | ogni orologio e meccanismo: saperlo condurre e **descriverlo col read-aloud** senza anticipare, lasciando posto alle soluzioni non previste | i box delle scene e degli ambienti |
| `P-INTERAZIONI` | cosa interagisce con i PG, con gli artefatti e col mondo, e come deve muoversi | `campaign-coherence.md`, le pagine degli artefatti |

🔒 **Su tutte le voci, una regola che le attraversa**: separare ciò che sanno i
PG da ciò che sa il master. Una preparazione che lo mescola è un rilievo
(`P-CONFINE`) anche se ogni voce è fatta, perché è il modo in cui un DM
anticipa senza accorgersene.

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
