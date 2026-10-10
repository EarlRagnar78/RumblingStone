# ADR-0077 — La correzione della prosa passa per una revisione a due giri

- **Stato**: accettata
- **Data**: 2026-10-02
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: il DM, il 2026-10-02, sulle decisioni D15 e D16 di
  PIANO-AGENT-SKILLS-ESTERNE: *«D15 ok ma per fare la verifica deve proporre un
  documento che faccia leggere cosa e cambiato rispetto all originale così si
  possono approvare le modifiche e il documento diventa definitivo esattamente
  come le correzioni fatte sugli articoli di ricerca dei revisori che passano
  alla autore e alla fine di nuovo al revisore per vedere se e rimasto
  qualcosa? Forse puo aiutare un meccanismo di versioning del def ?»* e *«D16
  cerca le migliori soluzioni della community con licenza applicabile e
  applicale»*
- **Rapporti**: applica [ADR-0010](ADR-0010-vendoring-skill-terzi.md) (si
  prende il pezzo che serve, mai la collezione) e
  [ADR-0076](ADR-0076-adozione-da-awesome-llm-apps.md) (un ADR per ogni cosa
  presa da fuori); estende ai testi la riga di revisione di
  [ADR-0023](ADR-0023-colophon-di-edizione.md) e
  [ADR-0071](ADR-0071-gli-artefatti-crescono-per-stadi-e-ogni-pagina-ha-una-versione.md)

## Contesto

Fino a L11 i rilevatori del repo segnalavano e basta. La misura di L11
(`plans/scrittura/RISULTATI.md`) dice che le skill alzano la conformità dall'81%
al 100% sui testi nuovi; sui testi che ci sono già, i master DEF-1..4 di ARC-07
hanno da 13 a 30 segnalazioni ciascuno, e nessuno strumento le porta a una
correzione.

Correggere con una regex non è sicuro. Il repo l'ha già misurato due volte: un
trattino dipende dalla frase in cui sta, e «sembra» si toglie solo riscrivendo
quello che la frase voleva dire. La riscrittura la fa un modello o una persona;
quello che manca è un modo di leggerla, approvarla pezzo per pezzo e sapere
cosa è rimasto.

## Decisione

**1. Tre comandi, tre ruoli.** `scripts/ciclo_prosa.py` fa il revisore, due
volte:

| Comando | Ruolo | Cosa produce |
|---|---|---|
| `segnala FILE` | revisore, primo giro | i passaggi da correggere, ognuno con la norma e il rimedio |
| `revisione ORIGINALE RISCRITTO` | l'autore risponde | il documento `REVISIONE-*.md`: ogni modifica numerata, in CriticMarkup, con la norma che la motiva e una casella `[ ]` |
| `applica REVISIONE.md --data` | revisore, secondo giro | l'originale con le sole modifiche spuntate, la riga di revisione alzata, i residui |

La riscrittura sta fra il primo e il secondo comando, e lo script non la fa.

**2. Due garanzie, scritte in testa al documento di revisione.** Nessun
controllo peggiora: il conto delle segnalazioni per norma non cresce. E nessun
fatto cambia: i nomi propri del registro (`misura_craft`, Bestiario e
`state.md`), i numeri e le CD sono gli stessi prima e dopo. Se una delle due
manca, il comando esce 1; `applica` ricontrolla i fatti sulle sole modifiche
accettate e rifiuta.

**3. Una modifica senza una norma si guarda per prima.** Il documento le conta
e le segna «⚠️ non motivata». Possono essere giuste, ma sono quelle dove il
modello ha riscritto per gusto suo.

**4. Le modifiche si leggono come frasi.** Il diff è per parole, e due cambi
separati da tre parole o meno, senza una fine di frase in mezzo, diventano una
modifica sola. Sulla prima prova (l'eco privata di Hella della corsa
A-senza-4) undici modifiche di una parola sono diventate tre.

**5. Il versionamento è una riga, non un sistema.** `applica` scrive o alza
`<!-- revisione-testo: rN · AAAA-MM-GG -->` in testa al file, dopo il
frontmatter se c'è. La storia vera resta in git; la riga serve a chi legge il
master stampato o aperto fuori dal repo, come il `r<rev>` di ADR-0071. La data
si passa a mano (`--data`), perché ADR-0023 non la fa dedurre.

**6. Tre sbarramenti su `applica`.** Non scrive su `main` né su `master`
(regola di sempre del DM: niente canone su main via script). Non applica una
revisione se l'originale o il riscritto sono cambiati dopo: l'impronta SHA-256
dei due testi sta nella testata del documento, perché i numeri delle modifiche
valgono solo su quel diff. E non applica se le modifiche spuntate cambiano un
fatto.

**7. Quello che è migliorativo si applica da solo, e il documento lo dice.**
Aggiunto lo stesso giorno, su richiesta del DM (*«se migliorative applicarle
anche in modo automatico»*). Una modifica è segnata «auto» se, presa da sola,
soddisfa quattro condizioni: è motivata da una segnalazione; non cambia un
fatto; non fa crescere il conto di nessuna norma e ne fa scendere almeno uno;
non abbassa la lettura oltre la tolleranza (un punto di Gulpease, 0,05 di
ritmo). `applica --auto` le applica e riscrive la loro riga come `[x] auto`,
così chi legge il documento dopo vede cosa ha deciso la macchina. Le altre
restano al lettore, e le non motivate restano sempre al lettore.

**8. La lettura, prima e dopo.** Il documento riporta l'**indice Gulpease**
(GULP, Università La Sapienza, 1988: `89 + (300 × frasi − 10 × lettere) /
parole`, tarato sull'italiano) e il **ritmo**, cioè quanto varia la lunghezza
delle frasi. Tutti e due si misurano sui box quando ci sono, perché sono quelli
che si leggono ad alta voce. Non dicono se la prosa è bella. Dicono se una
riscrittura l'ha resa più dura da seguire a voce o più piatta, che è il modo in
cui una correzione di norma peggiora un testo senza che nessun controllo se ne
accorga. Sulla prima prova la lettura ha fermato una modifica giusta per P1 che
fondeva due frasi in una.

**9. Le skill si leggono a pezzi, e devono dirlo in testa.** La guida di
Anthropic sulle skill chiede un indice in testa a ogni reference oltre le 100
righe, perché un agente spesso ne legge solo l'inizio. Il 2026-10-02 erano 51
su 59 senza (la skill vendorizzata `rumblingstone-debugging` resta fuori).
`scripts/indice_references.py` genera l'indice dai titoli, fra due marcatori, e
`--check` gira in CI. La stessa guida chiede che ogni reference sia a un solo
livello dallo `SKILL.md`: misurato, nessun reference è raggiungibile solo
passando da un altro, e lì non c'era niente da cambiare.

## Che cosa si prende dalla comunità, e con che licenza

Nessuna riga di codice di terzi entra nel repo. Si prendono una sintassi e due
idee, riscritte con la sola stdlib (`difflib`, `hashlib`).

| Fonte | Licenza | Che cosa | Dove |
|---|---|---|---|
| **CriticMarkup**, Gabe Weatherhead ed Erik Hess ([criticmarkup.com](https://criticmarkup.com), `CriticMarkup/CriticMarkup-toolkit`) | Apache 2.0 | la sintassi di revisione: `{~~vecchio~>nuovo~~}`, `{++aggiunto++}`, `{--tolto--}`, `{>>commento<<}` | il testo marcato del documento di revisione |
| **Humanizer**, blader (`blader/humanizer`) | MIT | la regola «weak alone»: un segnale minore da solo non prova niente, conta il gruppo; e il divieto di inventare fatti mentre si riscrive | il controllo «tic minori in gruppo» e la garanzia sui fatti |
| ***Wikipedia: Signs of AI writing*** | CC BY-SA 4.0 | la stessa regola, nella forma di una guida per i revisori | citata, nessun testo copiato |
| Anthropic, ***Skill authoring best practices*** | documentazione pubblica | l'indice in testa ai references lunghi, i references a un livello, il ciclo «validatore → correggi → ripeti», gli esempi input/output | `indice_references.py`, la domanda 8 della self-check, `italiano-nativo.md` §1-bis |
| Anthropic, ***Building effective agents*** | documentazione pubblica | il modello *evaluator-optimizer*: chi scrive e chi valuta sono due ruoli, e si gira finché il valutatore non ha più niente | l'ordine dei tre comandi |
| **Indice Gulpease**, GULP (Lucisano e Piemontese, 1988) | formula pubblicata, nessuna licenza | la leggibilità tarata sull'italiano, in lettere e non in sillabe | la lettura prima e dopo, e la tolleranza dell'automatico |
| **LanguageTool** (`languagetool-org/languagetool`) | LGPL 2.1 | il controllo grammaticale italiano, usato come **servizio** (`--languagetool URL`, per esempio un server locale): nessun suo file entra nel repo, quindi la LGPL non lo tocca | `segnala`, facoltativo e fuori dalla CI |

I tic minori sono quelli che `italiano-nativo.md` §9.2-ter e §9.2-quater elenca
già e lascia fuori da ogni controllo, con la ragione scritta: da soli sono
italiano corretto. Ora contano quando due diversi cadono nella stessa unità di
prosa, che è un paragrafo, una voce d'elenco o un box. Il trattino
dell'etichetta di regia non conta, perché il giocatore non lo sente.

### Che cosa si è scartato

- **Vale** e **proselint**: le regole sono in inglese, e tradurle vorrebbe dire
  scrivere un altro rilevatore senza la loro taratura.
- **Le regole di LanguageTool copiate nel repo** (`grammar.xml` italiano):
  LGPL, e si appoggiano alle etichette morfologiche del suo motore, che il repo
  non ha. Il servizio sì, come sopra. Da questo container
  `api.languagetool.org` è bloccato dalla politica di rete, ed è un motivo in più
  per tenerlo facoltativo.
- **Hunspell** con il dizionario italiano: vuole un binario fuori dalla stdlib,
  e i nomi della campagna (322 nel registro) darebbero più rumore che errori.

## Conseguenze

- Un master DEF si corregge per revisioni approvate, e ognuna lascia un
  documento che dice cosa è cambiato e perché. Il DM approva modifiche, non
  file interi.
- Il controllo «tic minori in gruppo» entra nel registro come 🟡 e fuori dal
  punteggio MQM: la soglia di due tic diversi viene da Humanizer e non è
  ancora tarata su questo repo.
- La prima prova ha trovato un buco nel metro di D13: `SEMBRA` non vedeva il
  participio («ti è sembrato») né il passato remoto. Corretto in
  `voto_scrittura.py`; i conti di L11 non cambiano (stessi voti sulle corse).
  Leggendo i box uno per uno per il lotto, un secondo buco dall'altro lato:
  «appare» stava nel rilevatore ma non nella norma. Tolto, i box sono 30 su
  501, e il lotto che li corregge è il primo uso vero del ciclo
  (`plans/scrittura/revisioni-D13/`).
- Il lotto ha chiesto due cambi allo script: il documento di revisione basta a
  se stesso (`applica` ricostruisce le due versioni dal CriticMarkup, senza
  una seconda copia del master), e il diff si fa a due livelli, per righe e
  poi per parole, perché per parole su un master di 2.600 righe costava minuti.
- Lo script non riscrive. Se un giorno lo farà, la riscrittura passerà dagli
  stessi tre comandi.

## Estensione del 2026-10-03: di quanto migliora

### Contesto

Il DM, approvato il lotto D13: *«la parte di revisione della prosa è
automatizzata in modo da presentare la versione cambiata e migliorata? Se non è
così si può automatizzarla migliorando la prosa il più possibile e misurando il
miglioramento ottenuto»*. Il ciclo diceva che una riscrittura **non peggiora**
niente, ma non di quanto migliorava: il punteggio MQM (ADR-0059) esisteva e non
entrava nel documento di revisione, e fra un giro di riscrittura e l'altro
l'agente non aveva un comando che gli desse il conto.

### Decisione

- Il documento di revisione porta la sezione **«Di quanto migliora»**: il
  punteggio MQM e la penalità prima e dopo, e le segnalazioni norma per norma.
  Una garanzia in più: **il punteggio MQM non scende**.
- `lotto FILE... -o CARTELLA` prepara un pacchetto per ogni file con
  segnalazioni: i passaggi, la norma, il rimedio, i fatti che non si toccano, i
  numeri di partenza, i `references/` da leggere prima. In testa, la classifica
  dei file per MQM. Sui master già letti al tavolo (DEF-1, 2, 3) il pacchetto
  dice che i box si spezzano e non si riscrivono (D9).
- `misura ORIGINALE RISCRITTO` dà il delta di un giro. Esce 1 se una norma
  cresce, se MQM scende o se un fatto cambia, e dice quando fermarsi: dopo un
  giro che non abbassa le segnalazioni, o al terzo (`GIRI_MASSIMI`). Senza un
  tetto, «il più possibile» diventerebbe riscrivere per il gusto di farlo.
- `applica` scrive ogni revisione applicata in `plans/scrittura/miglioramenti.json`;
  `registro --check` è un cancello in CI: nessuna revisione applicata ha
  peggiorato la misura.
- «Sembra» e «pare» entrano nel punteggio come norma minore
  (`box_sembra_pare`), col lotto che li ha corretti, come il registro delle
  norme aveva scritto. Le norme pesate passano da 12 a 13, e la linea di base
  di `campaign/misure/` si riscrive.

La riscrittura resta di un agente con le skill, e l'approvazione resta del DM,
modifica per modifica. Lo script continua a non scrivere prosa.

### Conseguenze

- Il registro, riempito a ritroso con le undici revisioni di D13: segnalazioni
  da 293 a 265, MQM +2,52 punti sui file toccati.
- La prova sull'ARC-08 (`plans/scrittura/revisioni-pilota-ARC08/`) ha
  trovato un difetto del metro dei nomi propri: un nome composto contava due,
  e chiedeva di togliere un nome che la garanzia sui fatti vieta di togliere.
  Un nome composto che sta nei dati ora conta uno (`misura_craft._nomi_composti`).
  «Mano Rossa» e «Drellin's Ferry» non stanno nei dati, e valgono ancora due.
- Quello che si paga: MQM misura la conformità alle norme registrate, non la
  bellezza. Un box può salire di punteggio e restare piatto, e un tic che non è
  una norma pesata (i tic minori in gruppo) abbassa le segnalazioni senza
  muovere MQM. Il giudizio resta di chi legge a voce, e il lettore a freddo di
  `rumblingstone-playtest` resta il passo che nessun numero sostituisce.
