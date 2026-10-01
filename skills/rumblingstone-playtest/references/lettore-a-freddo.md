# Il lettore a freddo — rubrica fissa

Il lettore è un DM esperto che **non ha mai visto il modulo** e deve portarlo
al tavolo stasera. Legge dall'inizio alla fine, una volta, e annota ogni punto
in cui dovrebbe **inventare** o **cercare** per andare avanti. Non giudica lo
stile e non propone riscritture: trova i buchi.

Serve perché chi ha scritto il modulo non vede le proprie lacune: sa già che
aspetto ha ogni stanza e chi ci sta dentro, e non si accorge che sulla
pagina non c'è scritto. Il 2026-09-25, al tavolo, il DM ha dovuto inventare sul
momento sette cose che `ARC07-DEF-4` non diceva, fra luoghi e persone. Nessun
validatore le aveva viste.

⚠️ **Gli esempi di questa rubrica non vengono mai dai casi di calibrazione.**
Quelle sette lacune servono a misurare quanto il lettore trova: se la rubrica
le nominasse, il lettore le troverebbe perché gliele abbiamo dette. La prima
stesura ne citava tre, ed è stata fermata prima di dare un numero.

## Le condizioni

- Il lettore riceve **solo il modulo**, e i file che il modulo cita per nome.
  Niente storia di git, niente piani, niente conversazioni: sono proprio le
  cose che il DM al tavolo non ha.
- Legge **nell'ordine di gioco**, non a salti. Un'informazione che arriva tre
  scene dopo il punto in cui serviva è un rilievo.
- Scrive un rilievo per ogni buco, anche piccolo. Il conteggio si fa dopo.

## La lettura a scene

Dal 2026-10-01 il modulo non si consegna intero: lo serve
`scripts/lettura_a_scene.py`, **una scena alla volta**, e la scena dopo arriva
solo quando il lettore ha scritto il diario di quella appena letta, e non prima
del tempo che serve a leggerla. È il modo in cui un DM incontra il modulo la
prima volta, e l'unico in cui `L-ORDINE` si vede davvero: un lettore che ha già
letto la scena dopo non sa più che cosa mancava prima.

Il diario, una riga per passaggio:

```
ago=<-2..+2> | mi aspettavo: … | ho trovato: … | so adesso: … | codici: L-…
```

- **ago** è come va la lettura: +2 dentro, 0 neutro, −1 la perdo, −2 smetto.
  Smettere è permesso, e il punto in cui si smette è un rilievo;
- **so adesso** è cosa sanno i PG a questo punto, e da chi l'hanno saputo. Una
  cosa che il diario dice di non sapere e che compare tre scene dopo è un
  `L-ORDINE`, con la prova già scritta;
- i **codici** si annotano nel momento in cui scattano; la tabella dei rilievi
  si compila alla fine, dal diario.

Chi orchestra avvia la lettura e dà a ogni agente **solo il suo indirizzo**, mai
il percorso del file, con questo messaggio d'invio (forma presa da
`advisor-orchestrator-worker` di awesome-llm-apps, ADR-0076):

```
Sei il lettore a freddo di un modulo. Questo messaggio è tutto quello che hai.
COMPITO: leggere il modulo una scena alla volta e trovare dove il DM dovrebbe
inventare o cercare.
INPUT: export READER_FEED=<indirizzo>; poi
  python3 scripts/lettura_a_scene.py inizia
  python3 scripts/lettura_a_scene.py avanti --diario "ago=… | mi aspettavo: … | ho trovato: … | so adesso: …"
  python3 scripts/lettura_a_scene.py smetti --diario "…"   (se ti fermi)
  e la rubrica skills/rumblingstone-playtest/references/lettore-a-freddo.md
CRITERI (l'uscita fallisce se uno manca):
1. non apri il modulo per altre vie: niente grep, niente cat, niente git;
2. ogni passaggio ha la sua riga di diario, con tutti i campi;
3. la tabella finale ha una prova citata per ogni rilievo.
USCITA: la tabella | # | Scena | Codice | Cosa manca | Gravità | Prova |, e in
coda cosa la lettura non ha potuto verificare.
Se un input manca o si contraddice, scrivi INPUT GAP in testa, con una riga.
```

⚠️ **Il limite.** L'agente ha il repo davanti: se cerca il master con `grep`, lo
trova. Il meccanismo gli toglie il percorso, non la possibilità. Si controlla
dopo: un diario che cita cose delle scene successive ha guardato avanti, e la
lettura si rifà.

## Le domande, sempre le stesse

Un lettore vero non cerca «difetti»: si fa domande, e il buco è la domanda
che resta senza risposta. Le domande sono fisse, così due letture di due moduli
diversi si possono confrontare. Vengono dalla pratica di chi prepara un modulo
pubblicato: *The Alexandrian*, «How to Prep a Module», chiede di leggerlo tutto
immaginando di condurlo; Sly Flourish, di leggerlo tutto per sapere quali
segreti mettere davanti ai giocatori.

**Per ogni scena**, nell'ordine:

| Domanda | Se resta senza risposta |
|---|---|
| Dove siamo, e cosa si percepisce appena si entra? | `L-LUOGO` |
| Chi c'è? Com'è, come parla, cosa vuole? | `L-PNG` |
| Perché chi agisce agisce così, e perché proprio adesso? | `L-AMBIGUO` o `L-RIFERIMENTO` |
| Cosa sanno i PG a questo punto, e da chi l'hanno saputo? | `L-ORDINE` |
| Cosa possono fare qui, e cosa succede se falliscono? | `L-AMBIGUO` (e il playtester) |
| Quanto costa: tempo, risorse, tacche? | `L-NUMERO` |
| Da qui dove si va? | `L-ORDINE` |

**Per il modulo intero**, alla fine: *in tre frasi, di cosa parla?* · *chi è il
cattivo, e cosa vuole?* · *cosa ho dovuto rileggere, e perché?* L'ultima è la
più utile: un passo che si rilegge è un passo che al tavolo fa perdere tempo.

Quanto di tutto questo **resta** dopo una lettura sola lo misura il quiz a due
agenti: `quiz-a-due-agenti.md`.

## I sei codici

| Codice | La domanda che fa scattare il rilievo |
|---|---|
| `L-LUOGO` | I PG entrano in un posto, o ci possono andare, e non c'è niente da leggere o da dire su com'è? |
| `L-PNG` | Una persona parla con i PG, vende o combatte, e manca **aspetto**, **come parla** o **cosa vuole**? Vale anche per chi ha solo un ruolo e nessun nome |
| `L-RIFERIMENTO` | Il testo nomina una cosa, una regola o un evento come già noto, e il modulo non lo spiega da nessuna parte? |
| `L-ORDINE` | Un'informazione serve prima del punto in cui compare? |
| `L-AMBIGUO` | Una frase si può leggere in due modi, e le due letture portano a un gioco diverso? |
| `L-NUMERO` | Manca un numero che il DM dovrà dire ad alta voce: una distanza, una durata, un prezzo, quanti sono? |

## L'uscita

Una tabella, niente prosa intorno:

```
| # | Scena | Codice | Cosa manca | Gravità | Prova |
```

- **Gravità**: 🔴 *il DM deve inventare qualcosa di strutturale* · 🟠 *il DM
  perde più di 30 secondi a cercare* · 🟡 *se ne accorge un giocatore attento*.
  Sono le due metriche del debrief (`SKILL.md` §5), usate come soglie.
- **Prova**: la riga del modulo, citata tra virgolette, che rende evidente il
  buco. Senza prova il rilievo non si conta.

In coda, sempre, **cosa questa lettura non ha potuto verificare**: il ritmo, il
divertimento, se una scena regge davanti a sei persone. Lo dice il tavolo, non
il lettore.

## Come si usa il risultato

- Un rilievo 🔴 o 🟠 diventa una correzione nel modulo, scritta con i quattro
  campi del `SKILL.md` §7.
- Un **tipo** di rilievo che torna in due moduli diversi diventa una regola di
  `scripts/copertura_scene.py`: il lettore trova il difetto la prima volta, il
  cancello impedisce che si ripeta. È la strada per cui il contratto
  «In scena» è nato dai rilievi `L-LUOGO` e `L-PNG` di DEF-4.
- Il lettore **non è un cancello**. Due letture dello stesso testo non danno
  lo stesso elenco, e l'affidabilità di un giudice-agente nel repo non è
  ancora misurata: l'unico κ calcolato, quello di MQM, vale 0,0 perché il
  campione non aveva varianza, e quindi non dice niente
  (`PIANO-MISURA-EDITORIALE-STANDARD` F3.3). Il suo compito è trovare; quello
  del cancello è impedire che si ripeta.
