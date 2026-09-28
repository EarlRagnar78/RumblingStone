# Il playtester a freddo — rubrica fissa

Il lettore chiede *«capisco cosa c'è?»*. Il playtester chiede *«cosa succede
quando i giocatori fanno quello che vogliono?»*. Simula un tavolo, scena per
scena, e per ogni cosa che i giocatori proveranno controlla se il modulo ha
**una risposta scritta**.

Le condizioni sono quelle del lettore (`lettore-a-freddo.md`): solo il modulo,
nell'ordine di gioco, nessuna storia di git.

## Il procedimento, per ogni scena

1. **Tre azioni probabili dei giocatori**, e almeno una che il modulo non
   prevede. Le azioni si scelgono guardando le risorse dei PG che il modulo
   stesso elenca: incantesimi, oggetti, denaro, alleati. Chi ha una risorsa
   prova a usarla.
2. Per ognuna: **il modulo risponde?** Una risposta vale se dà il risultato, il
   numero o la persona che reagisce. «Il DM decida» non vale, a meno che il
   modulo dichiari quali sono le opzioni.
3. **Chi fa cosa**: ogni giocatore ha qualcosa da fare in questa scena? Un PG
   senza azione per un'intera scena è un rilievo.
4. **Le domande del developer**, per ogni scontro e ogni luogo sorvegliato: *e
   se volano, e se sono invisibili?* · *chi sente il rumore, e in quanti round
   arriva?* · *il PG che non vola e non ha gittata, cosa fa?* · *lo skill
   challenge dice chi tira, cosa, e quanto costa un fallimento?* Le spiega
   `rumblingstone-module-standard/references/sviluppo-degli-incontri.md`.

## Gli otto codici

| Codice | La domanda |
|---|---|
| `P-AZIONE` | Un'azione probabile resta senza risposta scritta? |
| `P-CD` | C'è una CD che nessuno sa chi deve tirare, o con che abilità? |
| `P-ECONOMIA` | Si può comprare, vendere o farsi dare qualcosa, e manca il prezzo, chi vende o quanto ce n'è? |
| `P-RISORSA` | Una durata, una carica o una distanza non torna con i numeri SRD, o non è scritta? |
| `P-VICOLO` | Un fallimento ferma l'avventura invece di portarla altrove? |
| `P-OROLOGIO` | Un'azione dovrebbe costare tempo (tacche, round, ore) e il modulo non dice quanto? |
| `P-SPOTLIGHT` | Un PG passa la scena senza niente da fare? |
| `P-ABITATO` | I PG hanno tempo libero in un luogo abitato (una fortezza, una città, un campo) e il modulo non dice chi trovano per **comandare o dare udienza**, **curare e benedire**, **rimedi e alchimia**, **armi e riparazioni**, **messaggi e annunci**, **guardia**? Un ruolo che lì non c'è va scritto come assente |

`P-ABITATO` nasce dal tavolo del 2026-09-25: in una notte libera a Hammerfist il
DM ha dovuto inventare la cappella con la sua chierica, l'alchimista e l'araldo.
Il testo non li nominava, quindi né il cancello né la prima lettura a freddo li
potevano vedere (ADR-0075). La domanda è costruita su quel caso: vale come
prova solo su un modulo che non l'ha generata.

## L'uscita

La stessa tabella del lettore, con i codici `P-`:

```
| # | Scena | Codice | Cosa manca | Gravità | Prova |
```

Più una riga per scena con le tre azioni simulate e l'esito:
`Scena N · azione → risposta trovata / rilievo #`.

In coda: **cosa la simulazione non ha potuto verificare**. Il playtester a
freddo non sa se i giocatori si annoiano. Sa solo dove il DM resterebbe senza
risposta.
