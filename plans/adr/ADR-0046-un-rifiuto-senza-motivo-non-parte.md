# ADR-0046 — Un rifiuto senza motivo non parte

- **Stato**: accettata
- **Data**: 2026-09-05
- **Decisori**: DM (Gianfranco Samuele), agente
- **Origine**: il sesto requisito mancante della #106, misurata contro la pratica
  dell'illustrazione AI-aided (`PIANO-RIPRESA-PR-ABBANDONATE` §3.2-3.3) ·
  `skills/rumblingstone-art-direction` §6, il gate di rifiuto

## Contesto

La catena raster della #106 fa cinque cose su sei bene: prompt e seed fuori dal
codice, determinismo *prima* della scelta, provenienza scritta, igiene di licenza
come exit 1, condizionamento da geometria reale. Manca il sesto — **il giudizio
umano nel ciclo** — e non manca per distrazione.

`PROVENIENZA.txt` registra **quale immagine è stata tenuta**. Ma il mestiere
dell'art director non è tenere: è **buttare**. La skill lo dice già —
un'immagine si butta invece di tenerla perché «è già venuta» — e quel giudizio,
che è la parte cara del lavoro, oggi evapora. Resta il PNG scelto; non resta
nessuna traccia dei tre che l'hanno preceduto né del perché.

Il costo non è estetico. Chi rifà la serie fra un anno — o chi la rifà su
un'altra macchina, che è lo scenario per cui i seed sono deterministici —
**ripercorre gli stessi vicoli ciechi uno per uno**, perché nessuno gli ha detto
che erano vicoli ciechi.

C'era già il posto dove scriverlo: `--reroll N` *è* la dichiarazione che il
tentativo prima si butta. Mancava l'obbligo di dire perché.

## Decisione

### 1. `SCARTI.txt`, accanto a `PROVENIENZA.txt`

Stessa cartella, stessa forma, stessa intestazione che spiega la regola:

```
<id> · seed <n> · reroll <k> · <motivo>
```

Due file, due domande diverse: il primo risponde *«con che pesi è nata questa
immagine»*, il secondo *«perché non è nata quell'altra»*.

### 2. Il motivo è obbligatorio, e il gate sta prima di tutto

`--reroll` senza `--motivo` esce **2**, *prima* di leggere il markdown, prima di
scrivere qualsiasi file e prima di ogni chiamata di rete. Un motivo di soli
spazi non conta.

La collocazione è la stessa scelta di ADR-0019 per i pesi vietati, e per la
stessa ragione: **un rifiuto che non si sa spiegare non deve nemmeno cominciare**.

### 3. Il gate riguarda il rifiuto, non la generazione

`--reroll 0` non chiede niente. Senza reroll non c'è nulla da buttare, e
chiedere un motivo lì sarebbe attrito senza scopo — la strada più corta perché
qualcuno scriva «x» e il registro diventi rumore.

### 4. Lo scarto si registra prima di rigenerare

Non dopo. Il tentativo di ieri è stato buttato **comunque**, anche se quello di
oggi fallisce: legare la registrazione al successo perderebbe proprio le serie
difficili, che sono quelle in cui il registro serve.

### 5. La scrittura è idempotente sulla coppia `(id, reroll)`

Rilanciare lo stesso comando **aggiorna** la riga invece di accodarne una
seconda, come già `scrivi_provenienza` per la scelta. Un motivo si può correggere
senza sporcare il file.

## Conseguenze

**Cosa migliora.** Il giudizio dell'art director diventa un artefatto versionato:
diciotto immagini scelte smettono di essere diciotto file e diventano **una serie
motivata**. E il registro è utile anche a chi l'ha scritto, tre mesi dopo.

**Cosa costa.** Una frase per ogni reroll, e l'attrito è voluto. Il rischio non è
che pesi troppo: è che pesi **abbastanza poco** da farsi aggirare con «brutta».
Nessun gate può distinguere un motivo vero da uno finto — questo è un obbligo di
forma, e la sostanza resta di chi scrive. L'intestazione del file lo dice a chiare
lettere, ed è tutto quello che si può fare a macchina.

**Cosa non copre.** Le immagini generate fuori dalla catena — la GUI, o un
servizio come Gemini che non espone il seed — non passano da qui. Per quelle il
registro si scrive a mano, ed è la stessa deroga che `PROVENIENZA.txt` già
prevede per gli asset importati.

**Verificato in CI, non solo nei test.** Il passo *«i cancelli mordono»* fa rossa
la pipeline se un `--reroll` senza motivo **passa**. È scritto al contrario di
come viene naturale — fallisce quando il comando riesce — ed è l'unico modo di
provare un divieto: un gate che esiste e non si verifica è un gate che un giorno
smette di funzionare senza dirlo, che è la lezione di ADR-0043.

## Alternative scartate

**Un campo opzionale.** Un registro che si può non compilare non si compila:
è la stessa dinamica dell'elenco delle skill di ADR-0041, scritto a mano e
rimasto a 13 voci su 18. Se il motivo è la cosa che serve, l'obbligo è la sola
forma che regge.

**Registrarlo nel markdown, accanto al prompt.** Il markdown è il master del
*prompt*, e ci sta bene il seed scelto (`--fissa-seed` lo fa già). Gli scarti
sono cronaca del processo, non contenuto del documento: metterli lì
gonfierebbe di storia un file che si legge per il presente.

**Dedurre lo scarto dai reroll registrati in `PROVENIENZA.txt`.** Si saprebbe
*che* c'è stato un reroll, mai **perché** — cioè la sola parte che non si può
ricostruire dopo.
