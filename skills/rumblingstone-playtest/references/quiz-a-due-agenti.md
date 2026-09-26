# Il quiz a due agenti — quanto resta dopo una lettura sola

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

## Quando si usa

- Su un master nuovo, dopo il lettore e il playtester: il quiz non trova
  buchi, misura se il testo si ricorda.
- **Prima e dopo** una riscrittura: se la riscrittura ha reso il modulo più
  chiaro, la quota «giusta dagli appunti» sale.
