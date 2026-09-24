# PIANO — Prosa che non sembri generata

> **Stato**: ✅ **completo** — tutti i lotti chiusi (2026-09-03)
> **Aperto**: 2026-09-03
> **Nasce da**: il DM porta due file esterni — la skill *the writing whip* e
> l'elenco *tropes.fyi* di Ossama Chaib — e chiede se convenga usarli per
> migliorare la prosa del repo e chiudere rilievi emersi al tavolo.
> **Risposta**: sì, ma su un bersaglio diverso da quello che sembrava.
> **ADR**: [ADR-0035](adr/ADR-0035-due-prose-due-norme.md) · [ADR-0036](adr/ADR-0036-misurare-il-miglioramento-non-lo-stato.md)

---

## §1 · Il rilievo che torna

I giocatori hanno detto la stessa cosa due volte: **2026-07-31** e
**2026-09-02**, *«la prosa sembra tradotta dall'inglese»*. Fra le due date sta un
motore di stile da 1.900 righe. La norma quindi non manca; quello che mancava
era la misura, e per la prosa di gioco l'ha aggiunta `validate_prosa.py`
(lotto P della catena editoriale).

Questo piano risponde alla domanda successiva: **i tropi dell'elenco esterno
aggiungono qualcosa a quella norma?**

---

## §2 · Cosa dice la misura

Provati tutti sul repo prima di scriverne uno. I numeri decidono, non il
giudizio.

### Sul contenuto di gioco (255 file)

| Tropo provato | Occorrenze | Verdetto |
|---|---:|---|
| Nomi ornati (arazzo, panorama, ecosistema) | 64 | **64 falsi positivi**: `sinergia` è un termine di regole 3.5, `panorama` sta in un nome di file PNG, `ecosistema` è ecologia letterale in una prova di Natura |
| Rotazione dei sinonimi | 31 | falsi positivi: descrizioni di mappe (`stanza`/`camera` sono due posti) e un'iscrizione runica |
| Gerundio d'analisi | 135 | gerundi italiani normali (*irradiando un'aura*, *innescando la Sfida*); il tic vero compare **una volta** |
| Anafora ravvicinata | 291 finestre | un file di tattiche in inglese e un'etichetta `**Costo**` ripetuta |
| Autocitazione | 2.149 candidati | termini di dominio ripetuti (`illithid`, `oscurità`) |

Nessuno di questi regge come controllo automatico. Metà dell'elenco esterno,
inoltre, era **già coperta** da `italiano-nativo.md` §9: antitesi, trattino
lungo, tricolon, chiusura a effetto, maiuscole di portento.

### Sui documenti del repo (177 file, 32.566 righe)

Contando la sola prosa — fuori tabelle, codice, titoli e citazioni:

| Tic | Occorrenze | Densità |
|---|---:|---|
| Trattino lungo | 2.080 | 92 ogni 1.000 righe · mediana 82 · quartile alto 118 |
| Numero annunciato prima dell'elenco | 138 | `AGENTS.md` a 315/1000, `plans/INDEX.md` a 831/1000 |
| Antitesi «non X: è Y» | 58 | |

Qui il segnale c'è, è denso, ed è quasi tutto scritto da un agente.

---

## §3 · La conclusione che la misura impone

**I tropi non si trapiantano da una lingua all'altra né da un genere all'altro.**

Tre di quelli dell'elenco sono **attivamente sbagliati** per la narrativa: la
frase breve isolata è legittima in un read-aloud, l'apertura *«immagina di…»* è
letteralmente cosa fa un box in seconda persona, e il tricolon è uno strumento
retorico vero. Applicarli alla prosa di gioco la peggiorerebbe.

E uno è un tell **solo in inglese**: le intestazioni con parola interrogativa. In
italiano «Come si usa» è il titolo giusto per la sezione che spiega come si usa.

**Ma una prescrizione e un gate non sono la stessa cosa**, ed è l'errore che
questo piano ha commesso a metà strada: i quattro tic immisurabili erano stati
lasciati cadere insieme alle regole scartate dal validatore. Un occhio umano vede
la rotazione dei sinonimi che una regex non trova. Vanno **scritti**, non
**contati**.

---

## §4 · I lotti

### ✅ Lotto A — La skill per i documenti del repo
`skills/rumblingstone-prosa-documenti`. Copre guide, ADR, piani, ricerche,
skill, README, corpi delle PR e messaggi di commit. Porta i numeri misurati, i
sei tic che contano lì, e l'elenco esplicito di **cosa non importare
dall'inglese** con la misura accanto.
**Accettazione**: la skill dichiara il proprio perimetro e il confine con la
prosa di gioco; `validate_skills` verde.

**✅ Chiuso 2026-09-03.**

### ✅ Lotto B — I quattro tic che una macchina non trova
`italiano-nativo.md` §9.2-bis: rotazione dei sinonimi, autocitazione, anafora
ravvicinata, gerundio d'analisi. Ognuno con **la ragione per cui non è
misurabile** accanto all'antidoto, così nessuno prova a metterli in un gate fra
sei mesi.
**Accettazione**: i quattro tic sono scritti con esempio italiano e antidoto; la
sezione dichiara di essere l'unica parte di §9 che dipende da un occhio.

**✅ Chiuso 2026-09-03.**

### ✅ Lotto C — La misura sui documenti
`validate_prosa.py --documenti`: densità del trattino, conteggio annunciato,
antitesi. Non bloccante, come `validate_lingua`. Soglie tarate sulla
distribuzione reale.
**Accettazione**: il rilievo copre circa un terzo dei documenti, non tutti — un
rilievo che compare ovunque non lo legge nessuno. 18 test, e le quattro soglie
**fissate da una mutazione**.

**✅ Chiuso 2026-09-03.** Risultato: 54 rilievi su 154 documenti.

⚠️ Due difetti nei test, trovati mutando il validatore e non rileggendolo:
- il caso «sotto soglia» usava cinque trattini, che stanno anche sotto il
  **minimo di dieci occorrenze**: era quello a tenerlo quieto, e abbassare la
  soglia da 150 a 5 non lo faceva cadere;
- il caso «poche occorrenze» stava sotto entrambe le condizioni, quindi azzerare
  il minimo non lo faceva cadere. Ora usa otto trattini su cinquanta righe:
  sopra la densità, sotto il minimo.

### ✅ Lotto D — Ripulire i documenti peggiori
I rilievi aperti. `plans/INDEX.md` a 831 trattini ogni mille righe,
`AGENTS.md` a 315, `PIANO-CHIUSURA-CATENA-EDITORIALE.md` con 144 trattini e
undici conteggi annunciati.
**Accettazione**: i dieci file peggiori sotto la soglia; la mediana del repo
scende sotto 82/1000. ⚠️ **Da fare a mano**: una sostituzione automatica del
trattone produce punteggiatura sbagliata, perché il segno giusto (due punti,
punto e virgola, virgola, niente) dipende dalla frase.

**✅ Chiuso 2026-09-03.** Da 55 rilievi a **2**, e i due che restano sono
argomentati sotto.

| | prima | dopo |
|---|---:|---:|
| Trattini lunghi (157 documenti, 15.870 righe di prosa) | 2.005 | 1.145 |
| Densità globale | 126/1000 | 72/1000 |
| Mediana per documento | 109 | 73 |
| File sopra la soglia di 150 | 12 | 0 |
| `plans/INDEX.md` · `AGENTS.md` · `README.md` | 831 · 315 · 288 | 25 · 26 · 0 |

⚠️ **La mediana di partenza non era 82: era 109.** L'82 del §2 viene da una
passata precedente con una base di righe diversa (32.566 righe contro le 15.870
che `prosa_documento` conta davvero), e il messaggio del validatore lo ripeteva
al lettore come se fosse la misura corrente. Sotto la misura del validatore
stesso il criterio d'accettazione era quindi più duro di come suonava, ed è
soddisfatto in entrambe le letture. Il numero nel messaggio è stato corretto.

**Tre falsi positivi del gate, trovati facendo il lavoro** (il primo segnalato
dal DM), con un test ciascuno e una mutazione che li fa cadere:

- **«due punti»** era contato come conteggio annunciato, e in italiano è il nome
  del segno `:`. Cercate tutte le occorrenze nei documenti: **nessuna** annuncia
  un elenco, sono il segno o un valore di regole («Resist Freddo nei due punti»).
  Il tic vero non ha questa forma, perché nessuno chiama «tre punti» la
  punteggiatura: si esclude la sola coppia.
- **L'intervallo numerico** (`3–4 ore`, `GS 17–19`) contava come trattone, e lì
  la lineetta enne è la notazione giusta: **79 delle 96** lineette enne dei
  documenti sono di questa forma. Il respiro resta la lineetta emme fra spazi, e
  resta contato anche fra numeri («Chiuso 2026-09-03 — 157 su 157»): l'esclusione
  chiede la enne **e** l'assenza di spazi.
- **Il conteggio citato** contava come conteggio commesso, e un documento che
  parla del tic lo cita per forza. Non è teorico: chiudendo questo lotto, il
  gate ha cominciato a segnalare **il piano, la skill e il changelog** che
  portano gli esempi fra virgolette basse come prova. Misurate: 6 occorrenze su
  77 stanno dentro una citazione, e sono citazioni tutte e sei.

**Come, visto che il `sed` era vietato.** Il divieto vale per il trattone come
respiro, e regge: quelle sostituzioni sono state scritte a mano, frase per
frase: **565**, verificate una a una da uno script che rifiuta la coppia che non
si applica esattamente una volta. Ma una parte dei trattoni non era un respiro:
era il **separatore fra un'etichetta e la sua definizione** in un elenco, la
forma «trattino grassetto descrizione» o «trattino percorso descrizione», dove il
segno giusto è sempre i due punti e non dipende dalla frase. Quei **295 casi**
sono stati fatti con una regola sola, leggendone il diff. In tutto: **76
documenti** toccati.

**Quello che resta contato e non va tolto**, misurato:

- **32 marcatori di stato** `[INFERRED — needs DM confirmation]`,
  `[ACCEPTED — DM-canon]`, `[Private — …]`: sono notazione del repo, uno di essi
  è perfino una costante di `compile_map_json.py`. Contati, non toccati.
- **Formati-record** come `Anointing: <PC> — <mark> — <status>` in
  `pc-protagonism.md` e `DR 2/—` del SRD: cambiarli cambierebbe un dato.
- **I 2 rilievi rimasti**, entrambi «numero annunciato»:
  `PIANO-CHIUSURA-CATENA-EDITORIALE.md` (7) e `PIANO-GENERATORE-CREATURE-E-PNG.md`
  (4). Letti uno per uno, sono **numeri misurati** («cinque difetti chiusi», «erano
  quattro problemi diversi», «restava cinque punti sotto la riga del GS») o
  **riferimenti a insiemi definiti** («le cinque domande del §7»), cioè
  esattamente il caso che la skill dice di tenere. Un documento di 616 righe che
  racconta otto lotti misurati supera una soglia di 2 senza avere il tic, e
  mangiare quei numeri per far tacere il gate sarebbe il difetto peggiore.

**La soglia resta a 150** anche se ora non segnala più niente. Non è una
classifica da riazzerare a ogni passata: è una guardia contro la ricaduta, e a
quella densità un documento nuovo è stato scritto con l'abitudine vecchia.

### ✅ Lotto E — Le due lacune vere dell'analisi esterna
`italiano-nativo.md` §9.2-ter (elusione della copula, inflazione di significato)
e §9.2-quater (watchlist del registro narrativo italiano). Sono le tre proposte
dell'analisi che reggono.
**Accettazione**: ogni tic con esempio prima/dopo e **la densità misurata
accanto**, perché si veda che sono prescrizione e non gate.

**✅ Chiuso 2026-09-03.** Densità: 20 elusioni della copula, 3 inflazioni, 22
voci della watchlist su 292 file — e buona parte legittime (*«un tesoro che
rappresenta il tuo passato»*, *«nel cuore della battaglia»*).

### ✅ Lotto F — Misurare il miglioramento invece dello stato
`validate_prosa --prima-dopo --rispetto-a REV`.

⚠️ **Nasce da una proposta dell'analisi che la misura ha smentito.** La
*burstiness* — varianza della lunghezza delle frasi, la misura più citata in
letteratura — sulla riscrittura che il DM ha approvato **peggiora**:

| `05-ECHI-HELLA.md` | burstiness | frammenti ≤6 parole | aperture ripetute |
|---|---:|---:|---:|
| originale | 0,55 | 2/18 | 1 |
| intermedia | 0,52 | 2/18 | 1 |
| **riscritta, approvata** | **0,47** | **0/18** | **0** |

La riscrittura aveva tolto i frammenti brevi, e togliere frammenti riduce la
varianza: **la metrica premia il tic che §9 vieta**. Non è taratura sbagliata, è
direzione sbagliata.

Le altre due misure assolute provate: la densità di frasi corte trova grida
(*«PORTATORE MALEDETTO!»*) e note telegrafiche di regia (*«Treant lo lancia»*);
le aperture ripetute sono tre in tutto il corpus.

**Le stesse misure fra due versioni dello stesso testo funzionano**, perché
grida e note di regia ci sono prima e dopo e si annullano.

**✅ Chiuso 2026-09-03.** 14 test scritti **prima** dell'implementazione, sul
caso vero. Uno di essi tiene ferma la decisione: se la burstiness smettesse di
contraddire il giudizio del tavolo, cade e la scelta va riesaminata.

### ✅ Lotto G — Il profilo delle lunghezze, e la prova sui documenti
Il DM chiede di capire la burstiness prima di decidere se introdurla. Spiegarla
ha prodotto una prova che mancava e uno strumento che resta.

**La prova che mancava.** L'obiezione onesta era che sulla prosa di gioco la
metrica sbaglia verso *perché* lì il frammento breve è legittimo, mentre nei
documenti il sospetto è l'opposto — paragrafi tutti uguali. Misurata su 124
documenti: mediane fra 0,59 e 0,70 nelle quattro famiglie, bande sovrapposte,
estremi che classificano il genere del file e non il ritmo. **Non separa niente
nemmeno lì.** I numeri stanno in ADR-0036, insieme all'artefatto che rende
`spells.md` il file più «vario» del repo (una lista senza punti finali diventa
una frase da 587 parole).

**Quello che sopravvive.** La sua forma **non compressa**:
`--prima-dopo` sui file nominati stampa le lunghezze in ordine di lettura con
media e scarto. Sul caso Hella si legge in due righe cosa ha fatto la
riscrittura — sparite le frasi da 3, 6 e 8 parole — e perché il CV mente.

**Accettazione**: il profilo è informazione e non punteggio, e un test lo tiene
fermo (`test_il_profilo_NON_entra_nel_verdetto`). 8 test nuovi, **5 mutazioni,
5 cadute**: profilo ordinato invece che di lettura, scarto campionario invece
che di popolazione, troncamento tolto, profilo acceso sulle scansioni intere,
profilo dentro il verdetto.

**✅ Chiuso 2026-09-03.**

⚠️ E un test l'ho dovuto correggere contro me stesso: pretendevo che una frase di
**una** parola contasse come frammento. Misurando, le frasi di una parola nei
read-aloud sono **279 e quasi tutte artefatti** dei puntini di sospensione
(*«È…»*, *«Solo…»*, *«Ma…»*). Contarle avrebbe inventato 279 tic.

---

## §5 · Da dove si comincia, in una chat nuova

```bash
# la riscrittura di un testo e' migliorata? (l'unica misura di qualita' che regge)
python3 scripts/validate_prosa.py --prima-dopo --rispetto-a HEAD~1 FILE.md

# lo stesso comando su un file nominato stampa sotto il profilo delle lunghezze
# (informazione, non punteggio: il verdetto resta dei cinque tic contati)

python3 scripts/validate_prosa.py --documenti           # oggi: 2 rilievi, argomentati in §4 D
python3 scripts/validate_prosa.py --documenti plans/INDEX.md
python3 -m pytest scripts/tests/test_prosa_documenti.py -q
```

**L'ordine**: partire dai file che si leggono di più — `README.md`, `AGENTS.md`,
`plans/INDEX.md` — invece che dai piani vecchi, che nessuno riapre.

**Il metodo**: sostituire il trattone frase per frase. Nella maggior parte dei
casi il segno giusto è **due punti** (quando la seconda metà spiega la prima) o
**niente** (quando l'inciso si può togliere). Se la frase perde senso togliendo
l'inciso, l'inciso era il punto e va promosso a frase.

**Cosa NON fare**: `sed` sul trattone. La punteggiatura non è sostituibile in
blocco, e il risultato sarebbe peggiore del difetto.
