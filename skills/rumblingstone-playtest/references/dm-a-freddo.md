# Il DM a freddo — rubrica fissa

Il lettore chiede *«capisco cosa c'è?»*, il playtester *«cosa succede quando i
giocatori fanno quello che vogliono?»*, il developer *«si gioca?»*. Il DM a
freddo chiede una cosa sola: **«stasera riesco a condurla, con questo file
aperto sul tavolo?»**. Legge per preparare e per condurre, non per trovare
difetti: i difetti sono i punti in cui si ferma.

Condizioni: solo il modulo e i file che cita per nome (se non ci sono, sono
un rilievo). Nessuna storia di git, nessun piano.

## Il procedimento — due letture, come un DM vero

**Prima lettura: la preparazione, scena per scena, senza guardare avanti.**
Leggi una scena (`### SCENA N`), poi scrivi la sua riga di preparazione **prima
di leggere la successiva**:

```
Scena N · ago=<-2..+2> · devo preparare: … · devo dire a voce: … · mi fermo su: …
```

L'ago è quanto la scena ti fa venire voglia di condurla: +2 non vedo l'ora,
0 la conduco, −1 mi pesa, −2 non la so condurre. Un −2 è sempre un rilievo.
Tornare indietro a rileggere è permesso, ma va scritto nella riga
(«ho riletto la Scena 3 per…»): un passo che si rilegge al tavolo fa perdere
tempo.

**Seconda lettura: la conduzione.** Immagina di avere i giocatori davanti.
Per ogni scena: da dove parto a leggere, cosa leggo ad alta voce, quali numeri
devo avere sott'occhio (CD, pf, tempi), cosa chiedo ai giocatori, come
chiudo. Se per rispondere devi saltare a un'altra parte del file, è un
rilievo `D-SALTO`.

**Il giorno dopo** *(la prova di memoria)*. Senza riaprire il modulo, scrivi:
in cinque righe cosa succede nella serata; i cinque numeri che ti servono di
più; il nome e la voce di ogni PNG che parla; come finisce. Poi riapri e
confronta: ogni cosa che hai sbagliato o dimenticato ed era importante per
condurre è un rilievo `D-RICORDO`.

## I codici

| Codice | La domanda |
|---|---|
| `D-PREP` | Per condurre la scena devo preparare qualcosa (una mappa, un handout, un numero, una voce) e il modulo non me lo dice, o me lo dice dopo? |
| `D-VOCE` | Devo dire qualcosa ad alta voce e non c'è scritto cosa, o c'è scritto in una forma che non si legge a voce (tabella, parentesi, rimandi)? |
| `D-SALTO` | Mentre conduco devo saltare altrove nel file per un dato che serviva qui? |
| `D-FLUSSO` | Finita la scena non so qual è la prossima, o i giocatori possono andare in un posto per cui la scena dopo non è scritta? |
| `D-TEMPO` | La scena non dice quanto dura al tavolo, o cosa tagliare se si è in ritardo? |
| `D-RICORDO` | Il giorno dopo ho dimenticato o sbagliato una cosa che mi serviva per condurre? |

## L'uscita

La stessa tabella delle altre rubriche:

```
| # | Scena | Codice | Cosa manca | Gravità | Prova |
```

Gravità: 🔴 *al tavolo mi fermo e invento* · 🟠 *perdo più di 30 secondi* ·
🟡 *me ne accorgo io, i giocatori no*. La prova è la riga del modulo, fra
virgolette. Poi le righe di preparazione della prima lettura, la prova di
memoria con il confronto, e in coda **cosa questa lettura non ha potuto
verificare**.

Non si propongono riscritture. Si dice dove ci si ferma.

---
Il metodo della lettura senza guardare avanti, dell'ago e della prova di
memoria del giorno dopo viene da *first-reader*
(`Shubhamsaboo/awesome-llm-apps`, `agent_skills/first-reader`, Apache 2.0),
adattato dal lettore di un articolo al DM che prepara una serata.
