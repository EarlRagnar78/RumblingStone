# Prosa: cosa si può migliorare in modo deterministico, e come si misura

**Data**: 2026-10-18 · **Richiesta**: Jfs, «verifica e misura come migliorare anche la prosa […] se c'è un modo per migliorarla deterministicamente con misura del miglioramento» · **Destinatario operativo**: il giro di rifacimento dei DEF di ARC-07

Note complete: [note-prosa-inventario.md](note-prosa-inventario.md) (cosa misura oggi il repo, con i numeri), [note-prosa-web.md](note-prosa-web.md) (la ricerca in rete, ogni affermazione marcata *letto* o *inferenza*, con gli URL); il prototipo della §4 è diventato `misura_craft --stile` e `cieco_versioni.py` (ADR-0093).

## 1 · La risposta breve

Sì, ma solo per metà. In modo deterministico si possono misurare e correggere la **forma** e i **difetti** della prosa: lunghezza dei box, sensi presenti, ripetizioni ravvicinate, stampi sintattici ripetuti, tic dell'IA, frasi che decidono per il giocatore. È quello che il repo fa già meglio della media, e si può fare di più.

La **qualità** invece nessuno la misura in modo deterministico. La letteratura recente è netta su due punti:

- i giudici LLM non concordano con gli esperti umani (κ vicino a zero in TTCW, Chakrabarty 2024, e in «Measuring AI Slop», 2025);
- ottimizzare un numero di leggibilità peggiora il testo (Martinc 2023; il divieto duro di Antislop porta la qualità a 28/100).

Quindi il miglioramento si misura in due strati: **difetti in calo** (deterministico, in CI) e **preferenza cieca del DM** su un campione fisso (umano, piccolo, ripetibile). Il secondo è l'unico che dice se il testo è migliorato. Il primo dice solo che non è peggiorato.

## 2 · Cosa manca per una risposta migliore, e cosa ho assunto

- **Manca un corpus umano di riferimento** in italiano fantasy (romanzi, moduli tradotti): serve per tarare le misure «a banda» (§3, punti 1-3). Ho assunto che si possa usare il testo dei master **scritto o riscritto a mano dal DM** come riferimento, se esiste; altrimenti va scelto.
- **Il κ fra un giudice automatico e il DM non è mai stato misurato** (`campioni_kappa.py`, campione A senza voti). Finché manca, ogni giudizio automatico di qualità è un'opinione.
- Assumo che il lettore che conta sia **il DM che legge ad alta voce e il giocatore che ascolta**, non chi legge il PDF. «The Reader is the Metric» (2025) mostra che lettori diversi pesano tratti diversi.

## 3 · Audit: cosa c'è già, e dove sono i buchi

Lo strato dei difetti è ricco: 9 strumenti, tutti deterministici, 47 norme misurate, 30 in parte, 20 no. I numeri di oggi su main:

| Misura | Oggi |
|---|---|
| MQM, classe master DEF | mediana 99,51, minimo 97,53 |
| Box con più di un nome proprio | 205 nel corpus |
| Box con parentesi | 138 |
| Calchi dall'inglese | 91 |
| Box oltre 12 righe | 21, in 8 file |
| Voto delle corse (`voto_scrittura`) | B-con al 100% |

Tre limiti che pesano sul rifacimento di ARC-07:

1. **MQM è schiacciato verso 100.** È normalizzato per riga: su DEF-1 (2.679 righe) togliere un difetto minore vale circa +0,04. Un rifacimento intero può muoverlo di un punto. Va riportato, ma non dice quanto è migliorato il testo.
2. **Il voto è saturo.** B-con è già al 100%, e metà dei controlli riguardano la forma dei box. Non può misurare un prima/dopo.
3. **Il confronto cieco della PR #234 è lo strumento giusto, ma confronta corse sui 10 casi, non due versioni di un master.** Va adattato: stesse coppie, le due versioni di uno stesso box.

## 4 · Quello che la community misura e il repo no, provato sui box di oggi

Ho scritto un prototipo in sola lettura (`box_metri.py`) e l'ho fatto girare sui box read-aloud. I numeri sotto sono **misurati**; la precisione dei rilevatori è **stimata a occhio** su una decina di box, non calibrata.

| Corpus | Box | Parole, mediana (IQR) | Oltre 100 parole | Nella banda 30-70 | Con al più un senso |
|---|---|---|---|---|---|
| ARC-07 DEF | 107 | 66 (49-92) | **21** | 52 | 73 |
| ARC-08 | 162 | 55 (37-67) | 2 | 118 | 119 |
| Drappo | 22 | 53 (32-88) | 2 | 8 | 21 |

Per file, ARC-07: DEF-1 mediana 79 parole e 6 box oltre 100; **DEF-2 mediana 75 e 8 box oltre 100**; DEF-3 4; DEF-4 2; DEF-5 1.

Cosa dicono, con onestà:

- **Parole per box** (dScryb con Merwin e Sims: 30-70, le migliori 50-70, oltre 100 è lungo; Sly Flourish: tagliare il 25% della prima stesura). È la misura più robusta delle quattro e la più semplice. Il tetto di 12 righe del repo non la sostituisce: un box di 12 righe piene arriva a 130 parole. **ARC-07 ha 21 box sopra 100, ARC-08 due.** Questo è un difetto vero e misurabile, ed è il primo bersaglio del rifacimento.
- **Sensi per box** (dScryb: 4-6 sensi per scena). Il prototipo **sottostima**: perde «le ossa», «un tono basso come una campana», «oscilla» sotto i piedi, e conta anche i box di dialogo, dove i sensi non c'entrano. Il dato «73 box su 107 con al più un senso» è quindi un tetto, non un conto. Diventa utile solo con un lessico sensoriale curato e i box marcati per tipo (luogo, dialogo, evento), che il registro delle norme chiede già.
- **Box «telecomando»** (The Alexandrian: il box decide cosa i PG fanno o provano). Zero nei tre corpora. Il repo ha già `read-aloud che presuppone un'azione del giocatore` (33 nel MQM), che copre la stessa cosa con un rilevatore migliore.
- **Echi entro 20 parole** (ProWritingAid; Ferrara e altri, arXiv 2508.00086): 1,0 per box in ARC-07, 0,4 in ARC-08, 1,5 nel Drappo. ⚠️ Lo stesso studio mostra che **l'IA ripete meno degli umani** a breve distanza. Una ripetizione voluta è retorica. Va letta come banda attorno al riferimento umano, mai come «meno è meglio».

## 5 · Sviluppo: cosa portare, in ordine

| # | Cosa | Che numero aggiunge | Costo | Nel giro di ARC-07 |
|---|---|---|---|---|
| 1 | **Parole per box** con banda 30-70 e allarme oltre 100, accanto al tetto delle 12 righe | quota di box nella banda, box oltre 100 | basso, il prototipo c'è | sì, come misura e come bersaglio |
| 2 | **Confronto cieco per versioni**: le due versioni dello stesso box, ordine casuale con seme, il DM legge ad alta voce e sceglie 1, 2 o =. Riportare il tasso di ribaltamento se c'è anche un giudice automatico | quota preferita con intervallo di Wilson | basso, `banco_prosa_locale.py` va solo adattato | **sì: è la misura del miglioramento** |
| 3 | **Annotazione a span del DM** con la tassonomia di LAMP (goffaggine, struttura, ridondanza, cliché, purple prose, genericità, tempi) su 20 box fissi | interventi per 100 parole, prima e dopo | medio: tempo del DM | sì, su un campione |
| 4 | **Lista di slop italiana derivata dai dati** (metodo Antislop: rapporto fra frequenza nel testo generato e nel riferimento umano) | indice di slop ogni 1.000 parole | medio, serve il corpus umano | dopo, se il corpus c'è |
| 5 | **Stampi sintattici ripetuti** (Shaib e altri: compression ratio sulle sequenze POS) | ripetizione della forma della frase fra i box | medio, serve un tagger (Stanza, Apache-2.0) | dopo |
| 6 | **Profilo sintattico** alla Profiling-UD: profondità dell'albero, subordinate, passivi, come distanza dal riferimento | chiude la norma 🔴 «al massimo due livelli di subordinate» | medio-alto | dopo |
| 7 | **Sensi per box** con lessico curato e box marcati per tipo | sensi distinti nei box di luogo | medio | dopo la marcatura dei box |

Scartati: proselint e write-good (solo inglese, il repo copre già quello che fanno), Vale (doppierebbe i rilevatori Python), WQRM e il campionatore Antislop (modelli e GPU, solo inglese), MATTR come numero da massimizzare (l'IA lo ha già più alto degli umani).

## 6 · Validazione: come si misura il rifacimento di ARC-07

Il protocollo, scritto prima di cominciare perché il numero non si scelga dopo:

1. **Fotografia di partenza**, sul main dopo la #245: MQM e norme per file (`punteggio_mqm`), `ciclo_prosa misura`, `misura_craft --box`, le risposte del developer (`domande_developer`), e le misure 1 della §5 (parole per box). Si salva in un file datato.
2. **Campione fisso per il cieco**: 20 box scelti prima del rifacimento, quattro per DEF, con seme dichiarato, metà di luogo e metà di evento. Non si tocca durante il lavoro.
3. **Dopo il rifacimento**: le stesse misure. Il criterio di successo è doppio:
   - **nessuna norma cresce e MQM non scende** (il cancello che `ciclo_prosa` ha già);
   - **il DM preferisce la nuova versione in almeno 14 casi su 20**. Con 20 coppie, 14 su 20 dà un intervallo di Wilson che parte sopra 0,48: basta per dire «meglio», non per dire «molto meglio». Se il risultato è fra 10 e 13, il rifacimento non ha migliorato la prosa in modo dimostrabile, e lo si scrive.
4. **Contro Goodhart**: le misure della §5 si guardano, non si ottimizzano. Nessuna riscrittura si giustifica solo con un numero sceso: deve passare anche il cieco. È la stessa regola di ADR-0077 §7-8 per le correzioni automatiche.

## 7 · Cosa non ho fatto

- Non ho letto le avventure di Dragons' Lair né i manuali di stile Paizo interni: la fonte Paizo è un post del blog.
- Il prototipo non è nel repo e non è un cancello. Le soglie 30-70 e oltre 100 vengono da fonti inglesi sul read-aloud: in italiano le parole sono in media un po' più lunghe, quindi la banda potrebbe stringersi. Va tarata sul cieco.
- Firecrawl aveva finito i crediti: la ricerca in rete è passata da una ricerca web normale. Le fonti lette sono citate una per una nelle note.
