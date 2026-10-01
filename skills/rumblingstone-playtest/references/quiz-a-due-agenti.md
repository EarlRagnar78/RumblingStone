# Il quiz a due agenti — quanto resta dopo una lettura sola

> **Dal 2026-10-01 il passo 7 del ciclo è il ricordo dal diario** (D1 di
> PIANO-AGENT-SKILLS-ESTERNE), e il quiz resta dove una chiave approvata c'è
> già (oggi DEF-4). La procedura del ricordo è in fondo, «Il ricordo dal
> diario»; il quiz è descritto qui com'era.

Il DM, il 2026-09-26: *«capisco qualcosa se leggo, o devo rileggere il modulo
più volte perché non è proprio chiaro?»*. Il lettore a freddo trova i buchi, ma
non dice quanto di un modulo **resta in testa** a chi lo ha letto una volta. Il
quiz lo misura, con un punteggio che si calcola a macchina.

## Il limite, prima del resto

Un agente ricorda tutto quello che ha letto, un DM no. Per questo il quiz non
lo fa chi ha letto il modulo: lo fa **un secondo agente**, che ha soltanto gli
appunti del primo. Gli appunti hanno un tetto di parole, come la pagina di
appunti di un DM. Quello che il secondo agente sa rispondere è quello che la
lettura ha lasciato. Resta un'approssimazione, e non una misura sulle persone.

## Il procedimento

1. **Chi legge.** Un agente riceve solo il modulo, lo legge una volta
   nell'ordine di gioco e scrive **appunti di al massimo 400 parole**, come se
   dovesse condurre la serata con quella pagina sola. Non vede il quiz.
   **Chi orchestra conta le parole** (`wc -w`) prima di passare avanti: oltre
   400 si rifà la lettura, non si taglia. Tagliare vorrebbe dire scegliere al
   posto del lettore cosa resta, cioè la cosa che si misura. Nella prova
   pilota del 2026-09-26 i due lettori ne avevano scritte 654 e 574, con il
   tetto detto una volta sola: adesso l'istruzione chiede di contarle.
2. **Chi risponde a memoria.** Un secondo agente riceve **solo gli appunti** e
   le domande del quiz, e risponde a ognuna in una frase. Se gli appunti non
   bastano, scrive «non lo so»: è una risposta lecita, e conta come sbagliata.
3. **Chi risponde a libro aperto.** Lo stesso quiz, con il modulo davanti.
4. **Il punteggio.** `python3 scripts/quiz_lettura.py` confronta le risposte
   con la chiave e divide le domande in tre classi.

| Esito | Cosa vuol dire | Cosa si fa |
|---|---|---|
| giusta dagli appunti | chiaro alla prima lettura | niente |
| giusta solo a libro aperto | c'è, ma non resta: è sepolta o sparsa | si sposta dove serve, o si ripete dove si usa |
| sbagliata anche a libro aperto | manca, o si contraddice | è un rilievo del lettore, e si corregge |

## La chiave

Ogni modulo che si misura ha la sua chiave in `plans/quiz/<modulo>.json`: da 10
a 15 domande, e per ognuna le risposte accettate. Le scrive chi ha scritto il
modulo, e **le approva il DM**, perché la chiave è canone: dice cosa il modulo
deve far sapere.

Una risposta è giusta se contiene **tutte le parole** di almeno una delle
alternative accettate, a meno di maiuscole e accenti. Il confronto è
deterministico, e ha un limite dichiarato: una risposta giusta scritta con
altre parole risulta sbagliata. Per questo le alternative sono più d'una, e i
falsi negativi si contano a mano alla prima esecuzione su ogni chiave.

Le domande chiedono i fatti che servono **al tavolo**: dove si arriva, chi
comanda, cosa vuole il cattivo, quanto dura una cosa, cosa succede se si
fallisce. Non chiedono dettagli che un DM cercherebbe comunque sulla pagina,
come una CD o un punteggio.

## Il limite osservato

Il 2026-09-27, su tre versioni di `ARC07-DEF-4`, tre lettori su tre hanno preso
appunti **procedurali** (CD, tacche, punti ferita) e hanno lasciato fuori la
missione della serata, anche quando il modulo la diceva in tre frasi nelle
prime righe del §0 (`plans/esperimenti/quiz-def4/RISULTATI.md`).

Per le domande di **procedura** il quiz distingue le versioni. Per le domande di
**storia** (dove si arriva, chi comanda, cosa chiede chi) non distingue un
modulo che le seppellisce da un lettore che le salta. Un risultato basso su
quelle domande, da solo, non è un rilievo sul modulo: va confermato dal lettore
a freddo, che le domande di modulo («in tre frasi, che cosa succede?») le fa
esplicitamente.

## Quando si usa

- Su un master nuovo, dopo il lettore e il playtester: il quiz non trova
  buchi, misura se il testo si ricorda.
- **Prima e dopo** una riscrittura: se la riscrittura ha reso il modulo più
  chiaro, la quota «giusta dagli appunti» sale.

## Il ricordo dal diario — il passo 7, senza chiave

Il quiz misura bene, e chiede ogni volta una chiave che il DM deve approvare.
Il ricordo non la chiede: si giudica contro quello che il master **dichiara**
di voler far restare, cioè il riquadro *La serata in tre frasi*, o in mancanza
il primo paragrafo del Quickstart. L'idea viene da `first-reader` di
awesome-llm-apps (ADR-0076).

1. **La lettura.** Chi legge, legge a scene con `lettura_a_scene.py`
   (`lettore-a-freddo.md`, «La lettura a scene»). Il suo diario è la sua
   memoria: non ci sono appunti a parte, e quindi niente tetto di parole da
   contare.
2. **Il ricordo.** `python3 scripts/ricordo_lettura.py domande <corsa>/<lettore>`
   stampa il pacchetto: il diario e sette domande da DM (la serata in tre frasi,
   chi si oppone e cosa vuole, da dove a dove, cosa succede se si fallisce, il
   momento più forte, come finisce, cosa si è dovuto rileggere). Lo riceve un
   agente **nuovo**, che non ha visto il modulo; «non è rimasto niente» è una
   risposta lecita.
3. **Il giudizio.** `python3 scripts/ricordo_lettura.py intenzione <master>`
   stampa l'intenzione; chi orchestra la mette accanto alle risposte. Una
   risposta che manca la missione o il cattivo è un rilievo sul modulo, da
   confermare col lettore a freddo come per il quiz («Il limite osservato»). Un
   master senza intenzione dichiarata è un rilievo da solo.
4. **Le domande dopo.** `python3 scripts/ricordo_lettura.py chiedi <corsa>
   <lettore|tutti> "perché ti sei fermato alla Scena 7?"`: il lettore risponde
   dal suo diario, senza rivedere il testo, e se non l'ha annotato lo dice.

⚠️ **Cosa si paga.** Il quiz ha un punteggio deterministico; il ricordo lo
giudica chi orchestra. Costa meno (niente chiave da approvare per ogni master)
e si ripete peggio: due giudizi sulle stesse risposte possono non coincidere.
Per questo, dove la chiave c'è, il quiz resta.

📏 **La prova del 2026-10-01** (`plans/esperimenti/lettura-a-scene-def4/`).
Sul DEF-4 del tavolo, il quiz dato a chi ha solo il diario fa 8 su 14 contro
i 6 degli appunti, e la missione (q4), persa da tre lettori su tre a
settembre, c'è. Ma il diario è lungo nove volte gli appunti, e il confronto non
è pari. Sul primo paragrafo del Quickstart di quella versione il giudizio non
regge: dice dove sono i PG, non cosa devono fare. Senza riquadro il ricordo
trova i buchi e non ha un metro.
