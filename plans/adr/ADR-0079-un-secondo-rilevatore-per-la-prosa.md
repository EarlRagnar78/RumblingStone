# ADR-0079 — Un secondo rilevatore per la prosa: Vale, LanguageTool, proselint

- **Stato**: **accettata, opzione B** (il DM, il 2026-10-03: *«da usare quando
  serve un secondo lettore come verifica […] altrimenti vai di B»*). Le opzioni
  C e D restano scartate. La parte «Decisione proposta» qui sotto è il testo su
  cui il DM ha risposto; l'esito è nella sezione «Esito: opzione B applicata».
- **Data**: 2026-10-03
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: il DM, il 2026-10-03, dopo la PR #213: se la licenza MIT
  non è un problema, qual è il vero motivo per non usare Vale, proselint e
  LanguageTool come secondo rilevatore; rivalutarli, mostrare cosa apportano,
  e chiedere se importarli, anche con un'eccezione ad ADR-0077 e al principio
  «stdlib-only» e «una norma, un rilevatore», se il miglioramento è evidente e
  misurabile.
- **Rapporti**: ritorna su [ADR-0077](ADR-0077-revisione-a-due-giri.md) §«Alternative scartate» e su
  [ADR-0078](ADR-0078-il-foglio-di-stile-si-esegue.md) §«Installare Vale»; applica
  [ADR-0060](ADR-0060-la-forma-rende-misurabile-cio-che-la-parola-non-distingue.md)
  («una norma, un rilevatore») e la sesta regola d'oro; misura: [RICERCA-SECONDO-RILEVATORE](../RICERCA-SECONDO-RILEVATORE-VALE-LT-PROSELINT-2026-10.md)

## Contesto

ADR-0077 aveva scartato Vale e proselint in una riga e lasciato LanguageTool
come servizio facoltativo fuori dalla CI. ADR-0078 aveva ripetuto il rifiuto di
Vale. **Nessuna delle due volte c'era una misura**: lo strumento non era
installato. Il motivo vero della scelta era un giudizio di costo e beneficio,
non un dato, e il DM ha fatto bene a chiederlo.

La ricerca allegata ha installato i tre strumenti nel sandbox (LanguageTool 6.8
da Maven Central come server locale; Vale compilato dal sorgente; proselint 0.16
da PyPI), li ha fatti girare su 521 file di gioco e 414 documenti, e ha letto a
mano 100 rilievi di validazione e 98 di calibrazione, con le soglie scritte
prima. Un **secondo giro** (richiesto dal DM, con effort più alto) ha aggiunto un
secondo lettore a cieco (un agente Opus che non vedeva le mie etichette), un
campione di 260 rilievi sui soli box read-aloud, uno di 74 sulle regole spente, e
un corpus di 100 frasi con errori noti scritto da un secondo agente per misurare
il richiamo.

## Misura (sintesi; il dettaglio e l'elenco dei 100 rilievi sono nella ricerca)

| | LanguageTool | Vale | proselint |
|---|---|---|---|
| Configurazione predefinita | 94.755 rilievi, il 99,4% da scartare | n/a | 3.167, quasi tutti sbagliati |
| Dopo la calibrazione | 189 rilievi, precisione 86% (1° lettore) e **78%** (2° lettore, κ 0,53) su 100; con due sole regole 91% | calchi: **11/11 identici** ai nostri; foglio: 5 veri su 10 (due lettori concordi) | **0/40** su righe italiane |
| Veri nuovi rispetto ai rilevatori del repo | sì: 93% dei veri | **5**, ma sono difetti del foglio di stile | 0 |
| Veri nuovi rispetto a **una regex** nel repo | **11 righe in 5 difetti** di concordanza sui nomi propri, più 2 altri (soglia 10 righe) | 0 come motore | 0 |
| Richiamo su 100 frasi scritte da un terzo (80 con errore) | 35% con tutte le regole (e 12 falsi allarmi su 20 frasi giuste); **1%** con la configurazione ridotta | 0 | n/a; i rilevatori del repo: 2,5% |
| Tempo | 171-189 s, JVM, 252 MB | 3 s, 65 MB | 14 s |
| Determinismo | sì (due giri identici) | sì | sì |

**Cosa ha cambiato il secondo giro.** Due numeri, e in direzioni opposte. La
regola `COMMA_PARENTHESIS_WHITESPACE` esce dalla configurazione (0 su 14 col
secondo lettore: metadati e artefatti di conversione, che avevo contato come
veri). `ARTICOLATA_SOSTANTIVO` sale da 3 su 10 a 6 su 10, e sull'intera
popolazione di 20 rilievi risultano **11 vere in 5 difetti**: il genere di un
nome proprio che oscilla (*la Torre* 15 volte, *il Torre* 12 nello stesso modulo;
*del Mano Rossa* ×3). Questo è l'unico contributo che una regex non riproduce. Il
resto è stato confermato: ortografia scartata 0 su 115, proselint 0 su 40,
le cinque grafie mascherate dal foglio 5 su 5 con due lettori. Il κ di 0,53 dice
che il giudizio di un lettore solo non bastava, e che nelle divergenze ci sono
state ragioni da entrambe le parti.

Tre fatti pesano più degli altri:

1. **Il guadagno di LanguageTool è un solo errore ripetuto**: l'apostrofo al posto
   dell'accento (*e'* per *è*). 72 dei 100 letti sono questo, e 45 sono i
   contesti distinti. Una regex in `validate_lingua` trova le stesse 121 righe
   di LanguageTool, più 58 che LanguageTool non vede, e nessun falso *Da'*.
2. **Le regole grammaticali italiane di LanguageTool sono poche**: su 80 frasi
   con un errore noto, scritte da un terzo, non rileva nessun accordo di verbo
   o aggettivo, congiuntivo, ausiliare, tempo (0 su 40). L'ortografia, che è la
   parte forte, sul nostro testo è rumore: anche sui soli box read-aloud ne
   confermano 4 su 215 parole distinte (il 2%). Ma **i rilevatori del repo
   prendono 2 errori su 80 della stessa prova**: la cecità grammaticale non è un
   difetto solo di LanguageTool.
3. **Vale come motore non aggiunge niente alle nostre regole**, ma usato come
   *secondo parere* sul foglio di stile ha trovato cinque grafie sbagliate
   (*Hellas*, *Cannathgate*) che due scorciatoie di `validate_prosa` mascheravano:
   `/` accanto alla forma e la freccia `→` in riga.

Le soglie scritte prima: S1 (precisione ≥ 70%) passa per LanguageTool ridotto;
S2 (≥ 30% nuovi e ≥ 50) passa alla lettera; S3 e S4 passano. **La lettura onesta
è che S2, scritta così, si supera per una ragione che G6 vieta di accettare**, e
ho aggiunto S5 dopo aver visto i dati: il contributo marginale contro la miglior
alternativa interna (almeno 10 righe vere). S5 non passa per `GR_04_002` e
**passa per poco per `ARTICOLATA_SOSTANTIVO`** (11 righe). Lo dichiaro come
criterio aggiunto a posteriori: il DM può non riconoscerlo, e allora
LanguageTool ridotto passa tutte e quattro le soglie originali.

## Decisione proposta

**Raccomandazione (prima opzione): non importare nessuno dei tre come
rilevatore di default; prendere dalla misura tre correzioni interne. Dopo il
secondo giro l'opzione B (uso facoltativo di LanguageTool) è difendibile; C e D
no.** Il «miglioramento evidente e misurabile» che il DM chiede come condizione
per il default non c'è: LanguageTool trova in tutto il contenuto di gioco sette
difetti che le altre vie non trovano (5 di concordanza sui nomi propri, 1
parentesi troncata, 1 parola ripetuta), e per trovarli bisogna leggere
duecento segnalazioni.

1. `validate_lingua.py`: una regola nuova, **avviso** e non errore, per
   l'apostrofo al posto dell'accento (*e', gia', piu', puo', perche', cio'…*),
   con la lista di parole accentabili. 179 righe oggi. Una norma, un
   rilevatore: è dove la norma già vive.
2. `validate_prosa.py`: le due scorciatoie del foglio di stile. Una forma
   esclusa accanto a `/` in prosa è un rilievo (il confine di parola vale per i
   percorsi, non per *Hellas/druidi*); una riga con `→` non è «spiegata» se la
   forma esclusa sta fuori dalle virgolette della spiegazione. Poi correggere i
   cinque casi nei quattro file, in un lotto di contenuto separato.
3. `ciclo_prosa.languagetool()`: la correzione degli offset UTF-16, **già in
   questa PR** con un test che fallisce sul vecchio codice. Il servizio
   facoltativo resta come in ADR-0077 (`--languagetool URL`, fuori dalla CI),
   ora con la riga giusta.

Cosa **non** cambia: ADR-0077 resta in vigore. L'eccezione che il DM ha
previsto non serve.

### Le opzioni, per la risposta del DM

| | Cosa | Costo | Cosa si ottiene |
|---|---|---|---|
| **A (raccomandata)** | le tre correzioni interne sopra; niente di nuovo in CI | poche righe, con test | tutto il vero che LanguageTool e Vale hanno trovato, più 58 righe |
| B | A, più LanguageTool come **passo facoltativo** del ciclo (`ciclo_prosa.py segnala --languagetool`) con tre regole (`ARTICOLATA_SOSTANTIVO`, `UNPAIRED_BRACKETS`, `ITALIAN_WORD_REPEAT_RULE`) e un preprocessore markdown che mantiene i numeri di riga (circa 30 righe); documentato, non in CI | uno script di avvio del server, 252 MB in locale, il preprocessore da mantenere | i 7 difetti di cui sopra, e le concordanze sui nomi propri a ogni nuovo master |
| C | B, più LanguageTool come **passo di CI** (Java 17, cache Maven di 252 MB, ~3 minuti, non bloccante, peso `minore` in `specifiche-qualita.yaml`) | JVM e Maven nella CI, manutenzione del server, rumore da governare | il controllo a ogni PR |
| D | Vale come secondo motore del foglio di stile | un binario Go, **due tabelle per una norma** | niente che A non dia |

Con **B o C** servono, prima di scrivere il codice: la lista delle regole tenute
in una sola tabella (non una seconda tabella di norme: LanguageTool è un
*rilevatore* e la norma resta in `editorial-standards.md`); una riga nel
`REGISTRO-NORME-EDITORIALI.md` che dica *chi la misura* (ADR-0056); un test con
il server finto, come quelli di `TestLanguageTool`; la voce nel manifest dei
tool; e il comando di avvio con il percorso Maven riproducibile. Il peso nel
punteggio MQM sarebbe `minore` (1), mai `critico`: un falso positivo non può
bocciare un documento.

## Alternative scartate

- **Importare LanguageTool con tutte le regole**: 94.755 rilievi. Inutilizzabile.
- **Dizionario personale per l'ortografia**: il gergo (statblocco, humanoid,
  upscale, nanica) è di migliaia di parole e cresce a ogni sessione.
- **Vale con regole scritte in YAML**: le regole diventerebbero due tabelle,
  quella di `validate_prosa` e quella di Vale, e andrebbero tenute in sincronia
  a mano. È proprio ciò che ADR-0060 e ADR-0078 hanno vietato.
- **proselint**: lista di parole inglesi letta su testo italiano; consiglia
  `“”` dove il repo prescrive «».
- **Aggiungere un criterio di accettazione per non decidere**: S5 è dichiarata a
  posteriori e il DM può scartarla; non è nascosta.

## Conseguenze

**Quello che si paga con A.** Un avviso nuovo in `validate_lingua` (179 righe in
contenuto che oggi non lo vede: il conteggio degli avvisi sale), e un lotto di
correzione quando il DM lo approva. Il foglio di stile, riparato, segnala
cinque righe che oggi tace. Nessuna dipendenza nuova.

**Quello che si paga con B o C.** Java 17 e 252 MB di jar; un server da avviare;
un rilevatore che dipende dalla rete al primo download e dal dizionario di una
versione (6.8): un aggiornamento di LanguageTool cambia i rilievi e rompe il
confronto prima/dopo. Il rumore resta alto se si apre una regola non tarata.
La LGPL-2.1 non pesa finché LanguageTool si usa come servizio e non si copia
nel repo; la CI lo scarica, non lo distribuisce. Il contenuto di gioco non
esce dal repo: il server è su `127.0.0.1`. **`api.languagetool.org` non va mai
usato**: manderebbe il testo della campagna a un servizio esterno.

**Cosa non so.** Il secondo lettore è un modello, non una persona; κ = 0,53 è
moderato, e le 14 divergenze sono elencate nell'appendice della ricerca perché il
DM le rilegga. Il corpus del richiamo ha un solo scrittore (un modello) e alcune
sue «frasi con errore» sono discutibili. Il numero di difetti di concordanza
veri nel repo è un minimo, perché il rilevatore non vede quelli di verbo e
aggettivo. I tempi sono del sandbox. Non ho provato i modelli n-gram, Vale con
Hunspell, né l'edizione a pagamento.

## Da rivisitare

Se in un anno LanguageTool avrà regole italiane di grammatica che scattano su
errori veri della prosa nostra (concordanza, congiuntivo), la prova a venti
frasi e la validazione si rifanno con la stessa procedura: le soglie S1-S4 sono
scritte nella ricerca.

## Se il DM risponde sì a B, C o D

Si introduce l'eccezione a questo ADR (che passa da *proposta* ad *accettata*,
con la riga della scelta), si scrivono le soglie e i pesi **prima**, si
implementa con test e si rimisura il miglioramento sul repo. Niente di questo è
stato fatto.

## Esito: opzione B applicata

Il DM ha scelto di tenere LanguageTool **come secondo lettore quando serve una
verifica**, non come rilevatore di default. È l'opzione B, che comprende A. Fatto
nello stesso lotto, con test:

| Cosa | Dove | Misura dopo |
|---|---|---|
| Avviso sull'apostrofo al posto dell'accento (*e'*, *gia'*, *perche'*) | `validate_lingua.py`, sezione `AVVISI`; mai un errore | 156 righe di contenuto, 0 falsi *Da'* e *po'*; gli avvisi del repo passano da 2.446 a 2.598 e la CI non si ferma |
| Le due maschere del foglio di stile | `validate_prosa.py`: la barra non scarta più la forma (solo `/forma/`); una freccia lontana non spiega il cambio | 14 righe di **grafie sbagliate** che il gate non vedeva, in 6 file; corrette nello stesso lotto (*Hellas* → *Hella* in 13 righe, *Cannathgate* → *Channathgate* in 1). `--foglio --strict` torna a zero |
| Gli offset UTF-16 di LanguageTool | `ciclo_prosa.languagetool()` | test che fallisce sul vecchio codice |
| LanguageTool come secondo lettore | `ciclo_prosa.py segnala FILE --languagetool http://127.0.0.1:8081` | tre regole (`ARTICOLATA_SOSTANTIVO`, `UNPAIRED_BRACKETS`, `ITALIAN_WORD_REPEAT_RULE`), preprocessore che tiene i numeri di riga, **rifiuta ogni indirizzo non locale** (test), 52 s su tutto il contenuto |
| Avvio del server | `scripts/avvia_languagetool.sh [PORTA]` | scarica LanguageTool 6.8 da Maven Central in `~/.cache`, ascolta solo su `127.0.0.1`; niente nel repo |

Cosa **non** è stato fatto, di proposito: LanguageTool non è in CI, non pesa nel
punteggio MQM e non ha una riga nel registro delle norme, perché non introduce
una norma: la grafia italiana era già la norma, e il rilevatore che la misura in
modo permanente è la regex di `validate_lingua`. Il secondo lettore è uno
strumento di verifica, non un cancello. Nessuna soglia da dichiarare, quindi:
nessun peso.

**Cosa produce oggi sul repo** (rimisurato con la funzione vera, non con il mio
script di prova): 84 segnalazioni in 52 secondi, e conviene leggerle sapendo da
dove vengono.

- `UNPAIRED_BRACKETS` 45, di cui **32 in un solo file**
  (`PROMPT-IMMAGINI-07ILP.md`, il campo *Etichetta regia* troncato nel
  sorgente: un difetto sistematico di quel file che nessun altro rilevatore
  vede). Non l'ho corretto: il file è un elenco di prompt e il difetto sembra
  uscire da chi lo compila, non da un refuso. Resta al DM.
- `ARTICOLATA_SOSTANTIVO` 21, di cui 11 vere in 5 difetti (§9 della ricerca):
  *del Mano Rossa* ×3, *la Torre* ×5, *la Civetta*, *nel Tana dei Minotauri*,
  *dalla Conoscenze*. Non corretti: la scelta del genere di *Torre* è del DM
  (il modulo usa 15 volte *della* e 12 volte *del*).
- `ITALIAN_WORD_REPEAT_RULE` 18, per lo più in testi inglesi copiati.

**Il costo che resta.** Chi lo usa deve avere Java 17 e Maven la prima volta, e
leggere un elenco in cui poco più della metà è vero. Per questo non è un
cancello. Se in un anno le regole grammaticali italiane di LanguageTool
migliorano, la procedura di misura sta nella ricerca e si rifà in un'ora.

