---
name: rumblingstone-playtest
description: >
  Come si collauda un modulo o una sessione della campagna RumblingStone prima e
  dopo il tavolo: audit meccanico a tavolino, dry-run cronometrato, schede di
  feedback, e il ciclo alfa → beta → collaudato. Use WHENEVER si prepara un
  playtest, si chiude una sessione di prova, si chiede se un modulo è pronto per
  il tavolo, o si devono trasformare le impressioni dei giocatori in correzioni
  scritte. Trigger su: "playtest", "collaudo", "dry-run", "sessione di prova",
  "alfa", "beta", "feedback dei giocatori", "il modulo è pronto?", "tempi
  reali", "punti morti", "spotlight", "quanto dura la sessione", "cosa non ha
  funzionato al tavolo", "questionario", "debrief".
---

# RumblingStone — Playtest e collaudo

Il repo sa **scrivere** contenuto (`rumblingstone-narrative-style`), sa
**strutturarlo** (`rumblingstone-module-standard`) e sa **validarlo a macchina**
(`validate_*`). Questa skill copre il pezzo che mancava: **come si scopre se
funziona davanti a delle persone**, e come si trasformano le loro reazioni in
correzioni scritte nei file.

> **La regola di fondo**: un playtest non produce opinioni, produce **rilievi**. Un
> rilievo ha un numero, una gravità, una correzione applicata e il file che l'ha
> ricevuta. Tutto il resto è una chiacchierata dopo cena.

---

## 1. Le tre passate, in quest'ordine

Non si salta la 1 per andare alla 3. Ogni passata trova cose che le altre non vedono.

| # | Passata | Cosa trova | Cosa **non** trova | Costo |
|---|---|---|---|---|
| **1** | **Audit meccanico** — a tavolino, senza giocare | aritmetica sbagliata, CD irraggiungibili, riferimenti rotti, economia incoerente, incontri fuori scala | tutto ciò che riguarda il ritmo | ore |
| **2** | **Dry-run cronometrato** — sessione simulata, tiri alla media | blocchi che sforano, scene che evaporano, giocatori senza niente da fare, buchi di regia | cosa fa ridere sei persone vere | ore |
| **3** | **Tavolo vero** | tutto il resto — e **solo** il resto | niente: è il giudice | serate |

**Il dry-run non sostituisce il tavolo.** Serve a non sprecare il tavolo su difetti
che si trovavano da soli.

## 2. L'audit meccanico — le sette passate

Una cosa alla volta, altrimenti si guarda tutto e non si vede niente.

1. **Aritmetica degli statblocchi** — BAB, TS, CA, CMB/CMD, pf, slot incantesimi,
   talenti per livello, poteri a *3 + modificatore*.
2. **CD e raggiungibilità** — per ogni CD: *chi la tira, con che bonus, con che
   probabilità?* Una CD che il personaggio designato fallisce due volte su tre è un
   difetto, non una sfida. **È il rilievo che si trova più spesso.**
3. **Economia** — equipaggiamento iniziale contro la tabella, tesoro distribuito,
   e la domanda che nessuno si fa: *«un giocatore può comprare la soluzione del
   problema centrale?»*
4. **Riferimenti incrociati** — ogni `file` §`sezione` citato esiste davvero.
5. **Cronologia interna** — date, età, «vent'anni fa», e l'anno del presente
   dichiarato una volta sola in un posto solo.
6. **Scalabilità** — la composizione per 4/5/6/7 giocatori, calcolata **con i px per
   GS**, non a occhio.
7. **Coerenza d'ambientazione** — nessun fatto di canone altrui inventato; ogni
   `[INFERRED]` dichiarato.

**Output**: una tabella `# · rilievo · gravità · esito`, con 🔴 rompe il tavolo /
🟠 confonde / 🟢 verificato-ok. **Anche i 🟢 si scrivono**: servono a sapere cosa è
già stato guardato.

## 3. Il dry-run — come si simula un tavolo

- **Composizione**: dichiara chi immagini al tavolo (quanti esperti, quanti no). Un
  dry-run con sei ottimizzatori e uno con sei principianti danno numeri diversi.
- **Tiri alla media (10,5)**, tranne dove la varianza cambia la scena: lì si prova
  **sia il risultato alto sia quello basso**.
- **Cronometro per blocco**, previsto contro reale.
- **Annota i silenzi**: dove il tavolo simulato non avrebbe avuto niente da dire.
- **Conta le azioni per giocatore.** È il modo per scoprire chi passa la serata a
  guardare — il difetto più frequente e il meno segnalato.

**Output**: una tabella per serata (`blocco · previsto · reale · nota`) e l'esito
narrativo della simulazione. L'esito serve: se il dry-run finisce sempre allo stesso
modo, il modulo ha un solo finale vero.

## 4. Le schede di feedback

**Non chiedere «ti è piaciuto».** Le tre domande che misurano davvero:

1. *«Senza guardare niente: le tre cose che ricordi di stasera.»* — misura cosa è
   **atterrato**. Se nessuno cita la scena su cui hai lavorato di più, quella scena
   non c'è.
2. *«Il momento in cui ti sei annoiato o distratto.»* — l'unica domanda che trova i
   punti morti. Va scritta in modo che «mai» sia una risposta lecita e non una scusa.
3. *«Una cosa che non hai capito e hai fatto finta di sì.»* — trova le regole spiegate
   male. Nessuno lo dice a voce, tutti lo scrivono.

Più: **il mio personaggio ha contato?** (scala a cinque), **una decisione di cui non
conosciamo il prezzo** (misura se gli echi funzionano), e le domande specifiche del
modulo (il villain è stato capito? il dilemma ha tenuto?).

**Regole di raccolta**: anonime, compilate **prima di alzarsi**, lette **il giorno
dopo**. Modello pronto:
`STANDALONE-Il-Drappo-di-Tarsilia/PLAYTEST-SCHEDA-FEEDBACK.md`.

**Come si leggono**: cerca **le ripetizioni**, non le opinioni singole. Tre giocatori
su sei che scrivono lo stesso punto morto = difetto del modulo. Uno solo = quella
serata.

## 5. Il debrief del DM — i numeri che contano

| Metrica | Target |
|---|---|
| Volte che ho **improvvisato qualcosa di strutturale** | **zero** |
| Volte che ho **cercato un'informazione** per più di 30 secondi | sotto 5 a serata |
| Blocchi sforati oltre il **+30%** | zero |
| Contatori mossi **in silenzio** | mai |
| Azioni per giocatore, scarto fra il massimo e il minimo | sotto il doppio |

Le prime due sono le più importanti: misurano se l'**apparato d'uso**
(`08-CASSETTA-DEL-DM` nel modulo standalone) sta facendo il suo lavoro.

## 6. Il ciclo alfa → beta → collaudato

| Stato | Cosa significa | Come ci si arriva |
|---|---|---|
| **alfa** | scritto e validato a macchina; audit e dry-run fatti | le tre passate 1-2 |
| **beta** | giocato **una volta** da un gruppo vero, tempi reali annotati, correzioni applicate ai file | una sessione + il §6 del playtest |
| **collaudato** | giocato da **due gruppi diversi** senza improvvisazioni strutturali e senza noie ripetute | la seconda replica |

**Il criterio per smettere**: due gruppi diversi lo giocano senza che il DM debba
inventare niente di strutturale, e senza che nessuno scriva la stessa noia due volte.

## 7. Come si scrive una correzione

Mai un elenco di buoni propositi. Sempre **quattro campi**:

```
| A | Il -5 per cavalcare a pelo non si applica al fantino di contrada.
      A pelo ci è nato: è il motivo per cui la contrada lo tiene | REGOLE §6.1 |
```

**lettera · cosa cambia · perché (il rilievo che l'ha causata) · il file toccato.**
Poi si applica **al file**, e nel file resta una riga che dice *«correzione del
playtest, rilievo N»*. Fra sei mesi qualcuno chiederà perché quella regola è così: la
risposta deve stare lì.

## 8. Cosa vale per le sessioni della campagna, non solo per i moduli

La campagna non ha playtest — ha **sessioni giocate**, che sono la stessa cosa con
più poste in gioco. Trasferibile così com'è:

- la **scheda giocatore** (le tre domande) dopo una sessione cardine;
- il **debrief del DM** con le due metriche (improvvisazioni strutturali, ricerche
  oltre i 30 secondi);
- il **conteggio dello spotlight** — che nella campagna ha un nome già suo,
  *Shine Time* (`rumblingstone-campaign`), e che nessuno finora ha **misurato**;
- la disciplina delle correzioni: dal feedback ai file, con il rilievo citato.

Il ciclo di chiusura sessione resta quello di `rumblingstone-automation`
(`dm.py session end`, ADR-0007): questa skill non lo sostituisce, gli dice **cosa
guardare** mentre lo esegue.

## 9. Da non fare

1. **Non chiedere al tavolo di progettare.** I giocatori sanno dire dove si sono
   annoiati; non sanno dire come si aggiusta. Quello è mestiere tuo.
2. **Non correggere durante la sessione.** Annota e vai avanti: una regola cambiata a
   metà serata ne rompe altre tre.
3. **Non trattare una serata storta come un difetto del modulo.** Un gruppo stanco,
   una persona in meno, una discussione fuori gioco: succede. Serve la **ripetizione**
   per chiamarlo difetto.
4. **Non saltare l'audit meccanico** perché «tanto lo proviamo». Un'ora di aritmetica
   evita di bruciare una serata su un numero sbagliato.
5. **Non archiviare il feedback.** Se non diventa una riga in un file entro la
   settimana, non è mai esistito.
