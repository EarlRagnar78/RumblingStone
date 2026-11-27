# Ricerca: guardrail deterministici e tecniche avanzate per booklet e avventure

**Data**: 2026-11-03 · **Richiesta del DM** (Jfs, due messaggi dello stesso
mattino): evidenziare cosa cambia fra le versioni; cercare altre skill,
tecniche e caratteristiche che i DM riconoscono come migliori; mettere
guardrail deterministici a tutte le skill, anche a quelle dello stile;
provare transformer per NLP, tecniche di *document AI* e altre tecniche
avanzate; misurare e verificare il miglioramento in modo deterministico; e
adottare come standard ciò che migliora.

**Fonti**: WebSearch (Firecrawl senza crediti fino alle 13:00 UTC; il proxy
rifiuta slyflourish, dndbeyond e thealexandrian con curl). Prove nel
container, con i risultati in
[`esperimenti/guardrail-2026-11-03/`](esperimenti/guardrail-2026-11-03/README.md).

## In breve

| Tecnica | Provata su | Esito misurato | Decisione |
|---|---|---|---|
| **Conti SRD dei boss recintati** (pf, CA, CD di soffio, schiacciare e presenza, *corrompere l'acqua*, «come A.n», scurovisione) | 19 statblocchi recintati nei master DEF, prima mai controllati | **6 rilievi, tutti veri.** Trova i 2 difetti numerici che il playtester aveva trovato a mano (CD di *corrompere l'acqua* del Vecchio, scurovisione di Zog'tar) e altri 4 che nessun lettore aveva visto | **adottato**: `conformita_statblocchi --master`, cricchetto in test |
| **Note di lavoro in stampa** («[INFERRED…]», «va riscontrato», «(da verificare)», TODO) | i 10 booklet del DM | **60** in 5 volumi. Tutte vere: il DM le leggerebbe al tavolo | **adottato**: `misura_standard_tavolo`, cricchetto in test |
| ***Document AI* deterministica**: distanza in pagine fra scena e numeri, letta dal PDF (PyMuPDF) | i due PDF della prova ADR-0107 | ripete la lettura a mano: Zog'tar 23,5 → 5, Skullcrusher 21 → 4, Balvar 28,5 → 5,5, Durin 53 → 4,5 pagine (mediana). Durik peggiora (102,5 → 112) | **adottato** come indicatore: `misura_distanza_pagine.py` |
| **Cancelli dichiarati in ogni skill** | 18 skill | prima: 7 skill su 18 citavano un comando, nessuna in una sezione fissa | **adottato**: sezione «Cancelli deterministici», test che la impone |
| **Embedding multilingue** (MiniLM, transformer) per i box ripetuti | 362 box di almeno 25 parole | sopra 0,90 di similarità: 4 coppie, tutte ripetizioni vere, ma 3 le trova già il confronto di 4-grammi. Il guadagno è **1 parafrasi**, in un file pre-DEF. Sotto 0,90 trova scene dello stesso tipo, non ripetizioni | a box interi non adottato; **frase per frase adottato** (6 vere invece di 1, §8): `misura_ripetizioni_frasi.py` |
| **Rilevatore dei box «telecomando»** (il box decide cosa i PG provano, sanno, decidono) | 569 box | 15 colpi fuori dalle battute, **2 veri** (13%). Gli altri sono echi personali, effetti magici, sogni: la seconda persona lì è voluta | col singolare non adottato; **solo plurale adottato** (2 su 4, §8): `misura_box_telecomando.py` |
| **NLI** (mDeBERTa-v3 multilingue, transformer) per trovare contraddizioni fra file | 120 coppie etichettate a mano, poi 1.500 coppie di frasi simili prese da file diversi del repo | sulle coppie etichettate F1 0,86 (i numeri da soli 0,63). Sul repo vero **0 contraddizioni nuove nelle prime 30**: 1.268 coppie su 1.500 sopra 0,5, perché due statblocchi di creature diverse «si contraddicono» sempre; le 2 vere (veleno drow CD 18/13) le ha già l'errata. 28 minuti di CPU per 1.500 coppie | **non adottato**: sul repo 28 delle prime 30 sono rumore, e `coerenza_campagna` trova già 20 contraddizioni di fatto senza modello (§7) |
| **Varianti dei nomi** (fuzzy, come PerfectIt), **numeri incrociati** (come Xbench), **correzione grammaticale** con un modello | §5 | 1 vero su 64; 0 veri su 6; non applicabile | **non adottati** |
| **LLM come giudice** della prosa | letteratura | l'accordo con gli esperti è basso sulle dimensioni fini (τ ≤ 0,31) | **non adottato**: il giudice resta il cieco del DM (ADR-0093) |

## 1. Cosa cambia fra le versioni (la prova di ADR-0107)

La lettura a mano del 2026-11-03 ora ha un numero ripetibile. Mediana delle
pagine fra dove la persona agisce e la pagina con la sua CA e i suoi pf, sui
due PDF della serata del 2026-09-25 (157 e 172 pagine):

| persona | prima | dopo |
|---|---|---|
| Zog'tar | 23,5 (max 118) | **5** (max 94) |
| Skullcrusher | 21 (max 123) | **4** (max 106) |
| Balvar | 28,5 (max 118) | **5,5** (max 94) |
| Durin | 53 (max 61) | **4,5** (max 18) |
| Durik (`--nomi`) | 102,5 | **112** |

Il massimo resta alto perché alcune pagine d'azione stanno in capitoli che il
generatore non arricchisce (regia e cassetta, di proposito). Durik peggiora:
non ha un riquadro, i suoi numeri stanno solo in appendice, e le 15 pagine in
più li allontanano. È il costo dichiarato di ADR-0107, ora misurato.

## 2. Cosa dicono i DM, e cosa diventa un controllo

| Standard riconosciuto | Fonte | Diventa |
|---|---|---|
| il box non decide cosa i PG pensano, provano o fanno («remote-control boxed text») | J. Alexander, [GM Don't #13](https://thealexandrian.net/wordpress/48312/roleplaying-games/gm-dont-list-13-boxed-text-pitfalls) | già P1 in `misura_craft` per percezione e azione; per pensieri e sentimenti la regex non separa (§3) |
| il box non congela i PG mentre succedono cose («freeze-frame») | stessa fonte | resta giudizio: non c'è una forma testuale riconoscibile |
| box corti, circa tre frasi | commento allo stesso articolo; [EN World](https://www.enworld.org/forum/showthread.php?p=7592572) | già misurato (`>4 frasi`, tetto 12 righe), indicatore |
| numeri e mappa dove si gioca, non in appendice | ricerca della PR #306 | ADR-0107, ora misurato anche sul PDF |
| un numero senza fonte non va al tavolo | regola del repo (INFERRED) | **cricchetto** sulle note di lavoro in stampa |
| le CD delle capacità seguono 10 + ½ DV + caratteristica | SRD 3.5, *Dragon, True* e capacità speciali | **cricchetto** sui conti dei recinti |

## 3. Le prove che non hanno passato

**Box telecomando.** Una regex su 40 verbi di pensiero, sentimento e
decisione in seconda persona («capite che», «sapete che», «vi rendete conto»,
«decidete») dà 29 colpi su 569 box, 15 fuori dalle battute dei PNG. Letti uno
per uno (`box-telecomando.tsv`), 2 sono veri: «capite che qualunque cosa
facciate, lui ne guadagnerà» e «anche se sapete che è stata qui per millenni».
Gli altri 13 sono echi personali per un PG («la ricordi coperta del sangue di
Hella»), effetti magici («una lingua che non conosci e che capisci lo
stesso») e sogni. La seconda persona lì è il punto. Il dato utile è un altro:
i box del repo quasi non hanno questo difetto.

**Embedding per le ripetizioni.** Il registro delle norme dà «ripetizioni fra
box» come buco. Con `paraphrase-multilingual-MiniLM-L12-v2` (Apache 2.0) sui
362 box dei master vivi, le coppie sopra 0,90 sono 4 e sono tutte vere, ma
sono copie volute (la scheda del PG ripetuta nell'handout) tranne una
parafrasi («come un martello divino» contro «come una valanga di ferro») fra
ARC08-01 e un file pre-DEF. Il confronto dei 4-grammi, senza modello, ne
trova 3 su 4. Fra 0,80 e 0,90 il modello trova scene dello stesso genere (due
passaggi del drago, due notti d'assedio), che non sono ripetizioni.

## 4. Le tecniche avanzate in rete, e se si applicano

| Tecnica | Fonte | Si applica? |
|---|---|---|
| **Docling**, layout e ordine di lettura dei PDF (MIT) | [rapporto tecnico](https://hyper.ai/fr/papers/2408.09869), [slide](https://opensource.siemens.com/events/2026/slides/Panos_Vagenas__Docling_The_Open-Source_Document_AI_Engine.pdf) | non serve: i nostri PDF li genera Typst, il testo è già in ordine e PyMuPDF basta. Servirebbe per importare PDF di terzi, che ha già `converters/pdf-to-md-engine` |
| **NLI a frasi** per le incoerenze (SummaC) | [SummaC](https://arxiv.org/abs/2111.09525v1) | sì in teoria, per i fatti fra scene. Ma lo stesso filone dice che i dati NLI generici rendono poco sulle contraddizioni narrative ([DECODE](https://arxiv.org/pdf/2012.13391.pdf)). Si prova quando `coerenza_campagna` avrà 30 contraddizioni di fatto etichettate (oggi 6, tutte numeriche) |
| **Controllo con validità nel tempo** dei fatti | [FactTrack](https://www.arxiv.org/pdf/2407.16347) | sì, ed è la parte utile anche senza modello: un fatto vale dal giorno X al giorno Y (il viaggio a mille anni lo chiede). Candidato per `coerenza_campagna` |
| **Banchi di coerenza narrativa** con giudice LLM | [ConStory-Bench](https://arxiv.org/html/2603.05890) | gli errori si concentrano nei fatti e nei tempi a metà racconto: conferma dove guardare, ma il giudice è un LLM |
| **LLM come giudice** della prosa | [Limits of automatic evaluation of creativity](https://arxiv.org/pdf/2608.23705), [studio su 431 racconti](https://arxiv.org/pdf/2411.02316), [RAVEL](https://arxiv.org/pdf/2603.00686) | no come giudice: l'accordo con gli esperti è basso (τ ≤ 0,31 su 10 dimensioni su 11). Con rubriche e testi di riferimento sale, quindi resta utile come prima lettura, non come voto |

Le misure di prosa della letteratura (17, più spaCy, Stanza e la perplessità
di Qwen) sono già state provate sui voti ciechi del DM e nessuna li prevede
([RICERCA-QUALITA-MISURABILE](RICERCA-QUALITA-MISURABILE-2026-10.md) §3,
PR #270). Questa ricerca non le rifà.

## 5. Seconda tornata: tecniche di text AI che il repo non ha

Il DM, lo stesso giorno: cercare tecniche di text AI avanzate non ancora nel
repo, misurarle, e adottarle come standard solo se il prima/dopo mostra un
miglioramento. Tre provate, nessuna adottata.

| Tecnica | Da dove viene | Prova sul repo | Esito |
|---|---|---|---|
| **Varianti dei nomi** (fuzzy matching, come il controllo delle grafie dei nomi di PerfectIt) | [PerfectIt](https://support.perfectit.com/kb/guide/en/features-perfectit-cloud-XfloRYXDDu/Steps/2426078), [GNverifier](https://globalnames.org/apps/gnverifier/) | parole rare (≤ 3) con somiglianza ≥ 0,80 a uno dei 96 nomi del glossario, su 285 file vivi: 64 candidati (`varianti-dei-nomi.txt`) | **1 vero su 64** («Duric» per Durik in un prompt d'immagine). Il resto sono flessioni («Portali», «Forgiato») e inglese. Il glossario con `validate_prosa` tiene già le grafie dei nomi: non adottata |
| **Numeri incrociati** (il controllo dei numeri dei programmi di QA della traduzione, come Xbench) | [Xbench](https://xtm-cloud.atlassian.net/wiki/x/NQBV6Q), [ProZ](https://www.proz.com/doc/3310) | ogni «CA N» e «N pf» dopo il nome di una creatura recintata, fuori dal recinto, contro i valori del recinto: 19 confronti (`numeri-incrociati.txt`) | **0 veri su 6**: soglie di fuga (172 pf = metà), varianti scalate (391 pf al 34 DV), numeri di un'altra creatura nella stessa riga. Pochi confronti e nessun difetto: non adottata |
| **Correzione grammaticale con un modello** (GEC) | [17 modelli fino a 9B](https://arxiv.org/pdf/2505.06004); [mBART italiano su MERLIN](https://huggingface.co/MRNH/mbart-italian-grammar-corrector) | non provata | **non applicabile**: i modelli italiani sono addestrati su testi di chi impara la lingua (MERLIN), i nostri box passano già LanguageTool, e una riscrittura della prosa entra solo col cieco del DM (ADR-0093) |

Che cosa dice questa tornata. I difetti che il repo ha ancora non sono di
lingua né di grafia, che sono già coperti, ma di **regole del gioco**
(CD, sensi) e di **impaginazione** (numeri lontani, note in stampa): quelli
della prima parte, che sono stati adottati.

## 6. Cosa resta aperto

- Le correzioni trovate (6 conti, 60 note) sono canone: le decide il DM nei
  master. DEF-4 è anche della PR #305.
- Il tetto EL ≤ APL+4 resta 🔴 senza superficie: per misurarlo gli incontri
  vanno marcati `**EL**: N`, e questo tocca i master.
- NLI: provata e non adottata (§7). Si riprova solo se un modello sa a quale
  entità si riferisce ogni frase; validità nel tempo dei fatti ancora aperta.

## 7. Le etichette: la prova definitiva dell'NLI

Il DM, il 2026-11-03: «fai le robe complete, la parte etichette verifica, e
adotta quello che migliora davvero». Due prove, con gli script e i dati in
`plans/esperimenti/guardrail-2026-11-03/etichette/`.

**Prova 1, su coppie etichettate.** 120 coppie prima/dopo prese dalle
revisioni dei master (git log), etichettate a mano: contraddizione o no.
Le ho etichettate io, non il DM, e sono modifiche allineate, quindi il caso
facile.

| Metodo | Precisione | Richiamo | F1 |
|---|---|---|---|
| NLI (classe più probabile) | 0,878 | 0,837 | **0,857** (AUC 0,932) |
| solo numeri diversi | | | 0,627 |
| numeri + negazioni + nomi | | | 0,608 |
| deterministico **e** NLI | | | 0,73 |
| deterministico **o** NLI | | | 0,714 |

**Prova 2, sul repo vero.** 12.742 coppie di frasi quasi uguali in file
diversi (33.080 frasi); per i tempi di CPU un campione casuale di 1.500,
punteggio NLI nei due sensi, poi le prime 30 lette a mano.

| | Valore |
|---|---|
| coppie sopra 0,5 | 1.268 su 1.500 (85%) |
| sopra 0,9 | 920 |
| contraddizioni vere nelle prime 30 | 2, la stessa (CD del veleno drow 18 contro 13), già corretta in `ERRATA-PARTE1-Quest-Hellas-35-Verification.md` |
| contraddizioni **nuove** nelle prime 30 | **0** |
| tempo | 1.696 s per 1.500 coppie su 4 CPU; il repo intero ~4 ore |

Perché. Le frasi simili del repo sono righe di statblocco («Iniziativa +1 ·
Sensi …») o titoli di box di creature e scene diverse. Il modello non sa che
parlano di due soggetti, e due valori diversi per lui sono una
contraddizione. Sulle coppie etichettate il soggetto era lo stesso per
costruzione: è lì che sta il salto da F1 0,86 a precisione quasi nulla.

**Decisione.** Non adottato. Il controllo che funziona è quello che sa di chi
si parla: `coerenza_campagna` (fatti per entità, 20 contraddizioni) e
`conformita_statblocchi --master` (6 conti). Si riprova solo con un passo
che leghi ogni frase alla sua entità prima del confronto.

## 8. Le prove scartate, rifatte con una configurazione rigorosa

Il DM, il 2026-11-03 alle 14:13: le prove scartate vanno ricontrollate e
configurate bene prima di escluderle. Ognuna è stata rifatta cambiando solo
la configurazione, sugli stessi file, con lo stesso giudizio a mano. File in
`plans/esperimenti/guardrail-2026-11-03/rigorose/` ed `etichette/`.

| Prova | Prima | Configurazione rigorosa | Dopo | Decisione |
|---|---|---|---|---|
| **Embedding** per le ripetizioni (MiniLM) | box interi, soglia 0,90: **1** parafrasi oltre i 4-grammi | frase per frase (1.255 frasi), solo box diversi, copie (4-grammi ≥ 0,5) e handout esclusi, soglia 0,80 | **6** ripetizioni vere oltre i 4-grammi, 3 nei master DEF vivi (DEF-5/ARC08-11 «filo attraverso mille anni», DEF-4/DEF-5 il metallo sulla fronte, DEF-1 le piattaforme di cristallo due volte) su 21 coppie | **adottata**: `misura_ripetizioni_frasi.py`, indicatore, solo in locale |
| **Box «telecomando»** | 40 verbi, seconda persona singolare e plurale: 2 veri su 15 (13%) | solo il plurale (il gruppo intero), fuori dalle battute, non «… voi» | **2 veri su 4** (50%), stessi 2 difetti, 11 falsi in meno | **adottata**: `misura_box_telecomando.py`, indicatore |
| **NLI** (mDeBERTa) | coppie di frasi simili qualsiasi: 0 nuove nelle prime 30 | solo prosa (via righe di statblocco, tabelle, chiavi: valore), solo coppie che nominano la **stessa entità**: 1.149 coppie su 12.742 | **1 plausibile nelle prime 40** (dove Lythiel incontra Hella: cortile esterno o interno), il resto rami alternativi, momenti diversi, versioni 3.5/PF1e volute | non adottata: precisione 2,5% |
| **Varianti dei nomi** | glossario con parole comuni («Portale», «Tempio»): 1 su 64 | solo nomi propri (mai in minuscolo nel repo, ≥ 10 usi), varianti mai in minuscolo, niente genitivo inglese | **0 veri su 13** a distanza 1 («Mangino» è il singolare di «Mangini») | non adottata: i nomi sono già coerenti, lo tiene il glossario |
| **Numeri incrociati** | 19 confronti, 0 veri su 6 | solo nomi propri, solo il numero nella parentesi subito dopo il nome, soglie e varianti escluse | **1 confronto**, 0 difetti (Terros avanzato a 34 DV, variante voluta) | non adottata: fuori dal recinto i numeri quasi non si scrivono, e il recinto lo controlla `conformita_statblocchi` |

Che cosa cambia rispetto a §3 e §7. La configurazione conta: per due prove
su cinque decide fra «scartata» e «adottata». Per le altre tre la seconda
misura conferma la prima, e la ragione è nel repo, non nello strumento:
nomi e numeri sono già tenuti da controlli deterministici più forti. I
difetti trovati (2 box telecomando, 3 ripetizioni nei master vivi, Lythiel)
sono prosa e canone: li decide il DM, la riscrittura passa dal cieco.

## 9. Fedeltà del riscritto: l'NLI dove funziona, e le correzioni

Dalla lista di guardrail proposta al DM (NeMo Guardrails, Guardrails AI,
Ragas, DeepEval) l'unica idea nuova per il repo è la *faithfulness* di Ragas:
il testo prodotto non deve dire cose che la fonte non dice. Da noi la fonte è
l'originale e il prodotto è la riscrittura. L'NLI di §7 qui lavora sulle
coppie per cui è stata misurata: la stessa riga, prima e dopo.

**Etichette del DM, alla cieca** (2026-11-03, `esperimenti/guardrail-2026-11-03/fedelta/`):
30 coppie (riga tolta, riga messa) dai commit di correzione e di prosa, una
domanda sola («il dopo dice qualcosa che non può essere vero insieme al
prima?»), le parole cambiate marcate. 26 risposte sì/no, 4 «?».

| Metodo | Precisione | Richiamo | F1 | AUC |
|---|---|---|---|---|
| NLI, massimo dei due sensi > 0,5 | 0,91 | 0,77 | **0,83** | **0,92** |
| solo numeri diversi | 0,62 | 0,62 | 0,62 | 0,62 |
| numeri **o** NLI | 0,65 | 0,85 | 0,73 | |

NLI meglio dei numeri in 4.835 ricampionamenti su 5.000 (IC 95% della
differenza di F1 da −0,01 a +0,47): al limite, ma nella stessa direzione delle
105 coppie di §7 (0,86 contro 0,63). Le etichette di Claude e quelle del DM
coincidono su 25 coppie su 26.

**Decisione del DM**: non indicatore, correzione. `misura_fedelta_nli.py
--ripara` e, da sé, `ciclo_prosa revisione` rimettono come nell'originale la
riga che lo contraddice; `ciclo_prosa misura` esce con 1. Il costo misurato è
un falso allarme su 11 segnalazioni: si perde una riscrittura buona, non si
introduce un errore. Un cambio di fatto voluto (un nome, un numero, il canone)
si fa a mano, fuori dal ciclo della prosa: la prova è il cortile di Lythiel
qui sotto, che `misura` segnala con 0,997.

**Correzioni e cancelli, misurati sullo stesso giro**:

| Problema | Prima | Dopo | Cancello |
|---|---|---|---|
| box telecomando (`misura_box_telecomando`) | 4 colpi, 2 veri (PALIO «capite che…», P1-REVISED «sapete che…») | 2 colpi, 0 veri (i 2 accettati in `ACCETTATI` col perché) | `--check`, **in CI** |
| ripetizioni fra box (`misura_ripetizioni_frasi`) | 21 coppie, 3 vere nei master | 19 coppie: corrette le piattaforme di DEF-1 e lo strappo di ARC08-11; DEF-4/DEF-5 «il metallo sulla fronte» resta, è il richiamo del box di DEF-5 votato dal DM (CONGELATI) | `--check`, locale, `plans/scrittura/ripetizioni-accettate.json` |
| Lythiel e Hella | cortile esterno (Cerimonia §5.1) contro «cortile interno o sui bastioni» (HOOKS) | cortile esterno, dopo la cerimonia, in tutti e due | — |
| fedeltà delle correzioni stesse | | `misura_fedelta_nli --rif origin/main` sulle 4 riscritture: 0 contraddizioni; `ciclo_prosa misura`: MQM invariato, nessun box impoverito (ARC08-11 lo era alla prima stesura, corretto rimettendo un dettaglio sensoriale) | `ciclo_prosa` |
