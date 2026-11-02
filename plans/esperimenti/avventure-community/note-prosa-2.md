# Prosa deterministica, secondo giro: cosa si può contare e correggere che il repo non conta ancora

**Data**: 2026-10-18 · **Segue**: `PROSA-DETERMINISTICA-2026-10-18.md`, `note-di-ricerca/prosa-web.md`, `prosa-inventario-repo.md` (non ripeto quello che coprono).
**Legenda**: **[letto]** = l'ho letto nella fonte citata · **[inferenza]** = deduzione mia o ricordo non riverificato · **[misurato]** = l'ho contato io sui box del repo, in sola lettura, con lo script `conta2.py` nello scratchpad (regex, nessun tagger: spaCy e Stanza non sono installati nel container).
**Metodi di accesso**: Firecrawl senza crediti. Ho usato WebSearch e WebFetch. `curl` attraverso il proxy ha restituito `403 CONNECT` su arxiv.org e units.it, quindi non l'ho più usato. Tre pagine erano bloccate da Anubis (centaur.reading.ac.uk, revistas.uam.es, publikationen.ub.uni-frankfurt.de) e le ho sostituite con altre fonti. Dove serve dico quale fonte ho letto.

---

## 0 · Il dato che cambia la classifica: quanto sono puliti i box di oggi

Prima di proporre un rilevatore ho contato il tasso di base sui 291 box read-aloud (17.857 parole) di ARC-07 DEF, ARC-08 e Drappo, estratti con `misura_craft.box_read_aloud` **[misurato]**:

| Rilevatore candidato | ARC-07 DEF (107 box) | ARC-08 (162 box) | Drappo (22 box) |
|---|---|---|---|
| **Gerundio in coda** («, formando…», «, rivelando…» fino al punto) | **1** | **28** | 0 |
| Gerundi ogni 1.000 parole | 3,1 | 6,1 | 2,2 |
| **Avverbi in -mente ogni 1.000 parole** | **0,39** | **6,03** | 0,00 |
| Intensificatori (molto, davvero, completamente…) ogni 1.000 | 0,78 | 0,68 | 0,74 |
| Frasi oltre 20 parole | 23% (p90 27, max 58) | 21% (p90 25) | 21% |
| «comincia a / inizia a» + infinito | 2 | 6 | 1 |
| Pronome soggetto tonico (lui, lei, egli, ella) | 2 | 0 | 0 |
| Verbo supporto + nome in -zione/-mento | 0 | 3 (tutti «fare irruzione», falsi positivi) | 0 |
| Spiegazione del gesto («il che vuol dire», «come a dire», «segno che») | 0 | 0 | 1 |
| Filtro in terza persona («si accorse che», «notò che») | 0 | 1 | 0 |

Due conclusioni **[inferenza]**:

1. **Gerundio in coda e -mente separano nettamente i box vecchi da quelli riscritti.** ARC-08 contiene generazioni LLM più vecchie, ARC-07 DEF è stato riscritto con le skill. Il rapporto è 28 a 1 sul gerundio in coda e 15 a 1 sui -mente. Sono gli unici due candidati che, sui dati di oggi, dicono qualcosa. ⚠️ ARC-08 ha file duplicati (versioni): gli stessi gerundi compaiono tre volte, quindi il 28 va ripulito dai doppioni prima di diventare un numero ufficiale.
2. **Molti marcatori classici del traduttese sono già quasi a zero nei box** (pronomi soggetto, nominalizzazioni con verbo supporto, «egli»). Nei box servirebbero come **guardia** sulle generazioni nuove, non come bersaglio del rifacimento. Restano utili fuori dai box (handout, recap, testo per il DM), dove non li ho contati.

---

## 1 · Le checklist professionali di autorevisione

### 1.1 Browne e King, «Self-Editing for Fiction Writers»

Fonte: il riassunto della checklist in 14 voci della Columbia Fiction Foundry, https://fictionfoundry.alumni.columbia.edu/seffw **[letto]**. Il libro non l'ho letto. Altre pagine (jamigold.com, storycoach, wordsdeferred) elencano solo i capitoli. Le voci contabili:

| Voce | Regola **[letto]** | Ricetta per l'italiano | Falsi positivi | Nel repo? |
|---|---|---|---|---|
| 2, *Dialogue Directives* | segnalare i verbi dichiarativi diversi da «said», gli avverbi in -ly attaccati al dialogo e le spiegazioni messe dopo la battuta | nella prosa narrativa: verbo dichiarativo non neutro dopo la battuta (`»\s*,?\s*(sibilò|ringhiò|tuonò|ruggì|sussurrò|esclamò|replicò|ribatté|ammise)`); avverbio in -mente nel raggio di 5 parole dal verbo dichiarativo | «sussurrò» è spesso informazione vera di volume (regìa per il DM). Il formato del repo per i PNG (`**NOME (tono):** *«…»*`) mette il tono fra parentesi: **è proprio il caso che B&K sconsigliano**, ma è una norma scelta del repo (`editorial-standards.md` §2). Non va toccata, va solo tenuto presente il conflitto | no |
| 4, *Easy Beats* | evitare i *beat* che descrivono il dialogo, ed evitarne così tanti da spezzettarlo | numero di incisi d'azione fra le battute di uno stesso PNG; allarme se c'è un inciso dopo ogni battuta per ≥3 battute di fila | dipende dal formato dei dialoghi | no |
| 5, *Interior monologue* | il monologo interiore non deve essere una spiegazione travestita; togliere le didascalie superflue | — (giudizio) | — | — |
| 6, *Sophistication* | trovare le costruzioni con «as» e con «-ing» e riscrivere quelle che non servono | **in italiano diventa il gerundio in coda e il «mentre» di contemporaneità** (vedi §5.1) | gerundio modale vero («entra correndo») | in parte: `italiano-nativo.md` §9.2-bis dice che il «gerundio d'analisi» non è rilevabile |
| 9, *Once Is Usually Enough* | se due frasi fanno la stessa cosa, tenere la più forte | — (giudizio; vicino alla «esposizione ridondante» di LAMP, già nel primo giro) | — | — |
| 13, *Don't Let Them See You Sweat* | attenzione a «very» e «rather», alle file di aggettivi, alle immagini vistose, al corsivo e ai punti esclamativi | intensificatori su lista; aggettivi in fila (serve un tagger); `!` fuori dalle battute | il corsivo nel repo è il formato del box, non un'enfasi | punti esclamativi: no; corsivo: non applicabile |

La regola **RUE** (*Resist the Urge to Explain*) è di B&K, ma nel riassunto letto non c'è con quel nome. Coincide con le voci 2 e 5 (spiegazioni dopo la battuta e monologo interiore come spiegazione) **[inferenza]**.

**Qualità delle prove**: è consenso professionale, cioè un manuale molto citato di due editor, non uno studio. Le soglie non ci sono: «nessun limite numerico, la guida è qualitativa» **[letto]**.

### 1.2 Gli avverbi: l'unico dato correlazionale

Ben Blatt, *Nabokov's Favorite Word Is Mauve* (2017), secondo il resoconto della radio pubblica: i libri con meno di 50 avverbi in -ly ogni 10.000 parole erano più spesso considerati «grandi» (67%), quelli sopra 150 solo nel 16% dei casi. Il confronto è fra i 37 «Great Books» e gli altri romanzi degli stessi autori. https://www.kcur.org/2017-03-31/nabokovs-favorite-word-is-mauve-crunches-the-literary-numbers **[letto]**. Un altro resoconto (https://ar.casact.org/1278-2/) riporta che i romanzi più noti di Hemingway hanno il tasso più basso **[letto]**.
**Qualità**: correlazione su un corpus inglese, senza controllo del genere. Non prova che togliere avverbi migliori un testo **[inferenza]**.
**Nel repo [misurato]**: ARC-08 sta a 60 ogni 10.000 parole, ARC-07 DEF a 4. Le parole più frequenti in ARC-08 sono *finalmente* (7), *ufficialmente*, *chiaramente*, *completamente* (4 ciascuna), *simbolicamente*, *istintivamente*, *nervosamente*. *Simbolicamente* è l'«importanza dichiarata» che il repo già cerca, ma in forma d'avverbio.

### 1.3 Le *filter words*

Louise Harnby (editor di narrativa) elenca *noticed, seemed, spotted, saw, realized, felt, thought, wondered, believed, knew, decided*. Le tratta come strumenti da dosare, non come errori, e **rifiuta le regole fisse** («too prescriptive»): https://www.louiseharnbyproofreader.com/blog/filter-words-in-fiction-purposeful-inclusion-and-dramatic-restriction **[letto]**. TCK Publishing aggiunge *watched, could, noted, remembered, sounded, to be able to* e le due eccezioni: si tiene quando cambia il senso, o quando conta l'atto del percepire più della cosa percepita (https://www.tckpublishing.com/filter-words/ **[letto]**).
**Nel repo**: i verbi di percezione in seconda persona sono **già coperti** da P1 in `misura_craft.py` (`_P1_VEDERE`: vedete, notate, scorgete, sentite, udite, vi accorgete…). In terza persona ho trovato un solo caso nei box **[misurato]**. **Valore aggiunto basso nei box**. Avrebbe senso solo per recap ed echi scritti in terza persona su un PG («Thorik si accorse che…») **[inferenza]**.

### 1.4 «Cominciò a» (*began to*)

Nessuna fonte primaria letta: è un consiglio diffuso negli elenchi di autorevisione **[inferenza]**. Nel repo ci sono 9 casi in 291 box («comincia a sgretolarsi», «iniziano a vibrare», «inizia a brillare») **[misurato]**. Il passaggio deterministico è semplice («inizia a brillare» → «brilla»), ma qualche volta l'inizio dell'azione è proprio l'informazione («comincia a tirare»: prima non tirava). Va proposto, non applicato in automatico.

---

## 2 · Fonti italiane: traduttese, calchi, stile nominale

### 2.1 Pronomi soggetto espliciti: le prove ci sono, ma per l'italiano letterario il bersaglio è piccolo

- **Cardinaletti** (2004, 2005; e «Ancora sull'italiano delle traduzioni», *Altre Modernità* 2012, https://riviste.unimi.it/index.php/AMonline/article/view/2462): le parole chiave dell'articolo sono pronomi personali, soggetto, aggettivi e registro. L'interferenza va «monitorata» **[letto, solo l'abstract]**.
- Uno studio sul doppiaggio dal finlandese (Firenze University Press, https://oaj.fupress.net/index.php/bsfm-qulso/article/download/9282/8240/) riprende Cardinaletti 2004-2005, Garzone 2005 e Giusti 2005: le traduzioni letterarie da inglese e tedesco mostrano **pronomi soggetto espliciti dove l'italiano li ometterebbe**. Nei film doppiati, fra il 27% e il 61% dei pronomi espliciti è «inatteso»; i pronomi singolari espliciti sono 1.675 ogni 100.000 parole nel parlato (LIP) e fra 631 e 1.425 nei doppiaggi **[letto]**.
- **Gallitelli, Laurenti e Parks**, «Romanzi italiani e romanzi tradotti dall'inglese», *Tradurre* (https://rivistatradurre.it/romanzi-italiani-e-romanzi-tradotti-dallinglese/?pdf=4986) **[letto]**, ogni 10.000 parole, 1989-2011: *egli/ella/essi/esse* 0,9 negli originali e 1,2 nelle traduzioni. Sono **quasi spariti da entrambi**: per la narrativa di oggi «egli» è una spia di registro arcaico o burocratico, più che di traduzione. Nello stesso studio *stare* + gerundio vale 3,4 negli originali e **8,4 nelle traduzioni** (il repo lo rileva già), e la lunghezza media della frase è uguale (13 parole). Le particelle enfatiche *mica, meno male, senz'altro, magari* sono **più frequenti negli originali** in tutti i periodi (3,3 contro 1,6).
- **Ondelli e Sciumbata**, *Capitoli sul traduttese* (EUT 2024), https://arts.units.it/bitstream/11368/3107738/1/LIS_06_traduttese_online.pdf **[letto: indice e cap. 1; il PDF leggibile si ferma prima dei risultati]**: si attende nelle traduzioni più pronomi soggetto e più connettivi (esplicitazione), meno ricchezza lessicale, più aderenza alla norma. Il **sovrauso dei possessivi** è indicato come segno di traduzione, ma senza numeri nella parte che ho letto.
- **LLM multilingue**: Valentini e altri, arXiv 2608.17399 (https://arxiv.org/html/2608.17399v1) **[letto]**, usano la frequenza dei pronomi fra gli indicatori di traduttese. Le lingue sono cinque, l'italiano no e lo spagnolo (pro-drop) sì. Le generazioni native vengono classificate come «tradotte» nel 37-60% dei casi in tedesco e nel 46% in spagnolo. Le cifre per il pronome da solo non ci sono.
- **De Cesare** (Trento 2025, https://eventi.unitn.it/sites/eventi/files/2025-03/CL_De_Cesare_Abstract.pdf) **[letto]**: le biografie italiane generate da GPT-3, GPT-4 e GPT-4o mostrano «molte interferenze dall'inglese», grafiche, lessicali e sintattiche. L'abstract non dà numeri. Il progetto DFG «GenerateIT» (TU Dresden, dal 2025) studierà proprio questo.

**Nel repo [misurato]**: 2 pronomi tonici in 291 box, nessun «egli». ⚠️ La norma del repo ha già il suo confine: `read-aloud-adulti.md` riga 48 dice «Ri-ancorare i soggetti. Dopo tre righe, "lui" non è più nessuno». Il pronome tonico va quindi sostituito con il **soggetto nullo o con il nome**, mai solo cancellato. Coincide con la regola radiofonica di ripetere i nomi chiave (§3.1).

### 2.2 Stile nominale: verbo supporto + nome astratto

- Guida pratica per la PA (lentepubblica.it, https://lentepubblica.it/cittadini-e-imprese/il-potere-del-verbo-liberare-lazione-dalle-catene-del-burocratese-nella-pa/) **[letto]**: la nominalizzazione da sola non è un errore. Lo diventa con un **verbo vuoto** (*effettuare il pagamento*, *procedere all'esame*, *porre in essere una verifica*, *prendere una decisione*). La ricetta: cercare i nomi in *-zione/-mento*, rimetterli in forma di verbo e chiedersi chi agisce. Nessuna soglia.
- **Reinhart e altri** («Do LLMs write like humans?», PNAS 2025; https://arxiv.org/html/2410.16107v2) **[letto]**: i modelli istruiti usano le nominalizzazioni **1,5-2 volte** più degli umani (GPT-4o 2,1×, d = 1,23).
- **Nel repo [misurato]**: zero casi veri nei box. La guardia esiste già in parte (`la sensazione di`, `un senso di` in `CALCHI_SEMPRE`). **Valore aggiunto: basso nei box, forse alto nel testo per il DM** (non misurato).

### 2.3 «Andare a» + infinito, passivo con «venire»

- «Andare a + infinito»: Amenta e Strudsholm 2002 (https://revistas.ucm.es/index.php/CFIT/article/view/CFIT0202110011A) studiano la variazione regionale e diacronica. **Non dicono che sia un calco** **[letto, abstract]**. Nei box non ce n'è nessuno **[misurato]**. Scartato.
- Passivo con «venire»: 4 casi nei box, metà legittimi («viene dalle ossa» non è un passivo) **[misurato]**. Paizo e dScryb sconsigliano il passivo (già nel primo giro). Valore basso.
- Le frasi scisse («È X che…») sono italiano nativo. Non ho trovato fonti che le indichino come calco. Non proposte.

### 2.4 Treccani, Crusca, manuali italiani

Non ho trovato una regola **contabile** sullo stile nominale, sul «che» polivalente o sui gerundi in catena né nelle pagine Treccani né in quelle della Crusca raggiungibili dalla ricerca. Le guide sono prosa normativa, non soglie **[letto: risultati di ricerca; inferenza sul resto]**. Il primo giro era arrivato alla stessa conclusione. Una tesi padovana sull'editing di un romanzo (Rampazzo 2016, relatore Cortelazzo) non tratta il traduttese **[letto]**. La fonte italiana più contabile resta Gallitelli, Laurenti e Parks (§2.1).

---

## 3 · Prosa da ascoltare

### 3.1 Regole della scrittura radiofonica

*The News Manual*, cap. 48 (https://thenewsmanual.net/Manuals%20Volume%202/volume2_48.htm) **[letto]**:
- «Nessuna frase più lunga di 20 parole, salvo casi insoliti»; una o due idee per frase.
- **Mai un nome o un termine nuovo come prima parola del paragrafo**: prima il contesto noto, poi il nuovo.
- Ripetere almeno una volta i nomi e i luoghi chiave.
- Numeri arrotondati e scritti in lettere.
- Solo punto, virgola, punto interrogativo e trattino.

**Conflitto con il repo**: `italiano-nativo.md` §4 dice che «l'italiano respira più lungo» e chiede periodi lunghi chiusi da una frase corta. Un tetto di 20 parole **contraddice una norma del repo**. Nei box di oggi il 21-23% delle frasi supera le 20 parole; il p90 è 25-27 parole e il massimo 58 **[misurato]**. La proposta compatibile è un **tetto sulla frase più lunga** (per esempio oltre 35 parole), non sulla media **[inferenza]**. La soglia va tarata sul cieco, e la regola «non aprire con il nome nuovo» va affiancata al tetto di un nome proprio per box.

### 3.2 Comprensione all'ascolto

- **Peelle e altri 2009** (*Cerebral Cortex*, https://pmc.ncbi.nlm.nih.gov/articles/PMC2837088) **[letto]**: su frasi ascoltate di 6 parole, le relative sull'oggetto sono capite peggio di quelle sul soggetto (84,3% contro 93,5%), e il divario cresce con l'età e con la velocità. **Per l'italiano [inferenza]**: «il nano che l'orco colpisce» è ambiguo all'orecchio («che» soggetto o oggetto). Una relativa sull'oggetto con il soggetto posposto è il caso peggiore da leggere ad alta voce. Per rilevarla serve un parser (Stanza: `acl:relcl` con l'antecedente come `obj` della relativa).
- **Du Bois, *Preferred Argument Structure***, citato da Chui (https://irtest.lib.nccu.edu.tw/retrieve/119937/p1142-chui.pdf) **[letto]**: nel parlato si evita più di **un argomento lessicale** (un nome pieno) per proposizione e più di **un argomento nuovo** per proposizione. Nel corpus cinese di Chui il 94% delle proposizioni ha zero o un argomento lessicale, e il 100% al massimo un referente nuovo. È un dato descrittivo sul parlato spontaneo, non uno studio sulla comprensione. È però la generalizzazione naturale della norma del repo «un nome proprio nuovo per box», portata alla proposizione e ai nomi comuni **[inferenza]**.
- Chafe e la «one new idea constraint»: non ho trovato una fonte leggibile; la pagina che la citava era bloccata **[non letto]**.

---

## 4 · Dialoghi di gioco: regole contabili per le battute dei PNG

- **BioWare, tramite il Neverwinter Vault** (Wydraz 2015, https://neverwintervault.org/article/reference/creating-dialogue-neverwinter-nights) **[letto, di seconda mano]**: circa **25 parole** per battuta del PNG, «fino a circa 40 se serve davvero»; dopo qualche scambio lungo, alternare battute brevi. Il lore va negli oggetti e nei tomi, non nella battuta.
- **Beyond Skyrim**, guida di stile unificata (https://wiki.beyondskyrim.org/wiki/Arcane_University:Unified_Style_Guide) **[letto]**: 149 caratteri per battuta del PNG e 80 per la risposta del giocatore; numeri sempre in lettere; il PNG non dice mai il nome del giocatore; da 1 a 3 saluti per PNG.
- **Game Developer**, «8 key principles» (https://www.gamedeveloper.com/game-platforms/8-key-principles-of-writing-effective-game-dialogue) **[letto]**: esempio di una richiesta di 62 parole ridotta a 20; il lore forzato è una trappola.
- Avellone (RPG Codex) e il blog BioWare: nessuna regola contabile nelle pagine raggiungibili **[letto]**.

**Nel repo [misurato]**, sulle battute nel formato `**NOME (…):** *«…»*`: ARC-07 DEF ne ha 33, con mediana 20 parole, p90 54 e massimo 80. **12 superano le 25 parole e 5 le 40.** Il rilevatore vede solo questo formato, quindi il conto è parziale. Al tavolo il DM dice la battuta a voce e non la legge su uno schermo: la soglia dei videogiochi va tarata, ma una battuta di 80 parole è un monologo in qualunque mezzo **[inferenza]**.

---

## 5 · Passaggi deterministici che migliorano il testo generato: cosa dicono le prove

### 5.1 Le frasi participiali sono la firma sintattica più forte dell'LLM

Reinhart e altri, PNAS 2025 (https://arxiv.org/html/2410.16107v2) **[letto]**: i modelli istruiti usano le **proposizioni participiali al presente** (*-ing*) **2-5 volte** più degli umani (GPT-4o 5,3×, d = 1,38). È lo scarto più grande fra i tratti di Biber. Seguono le nominalizzazioni (2,1×) e la coordinazione di sintagmi (1,9×). Il passivo senza agente è invece **circa la metà** del tasso umano. Le differenze **crescono con l'istruzione** del modello: i modelli base sono più vicini agli umani. Il benchmark di Milička e altri (arXiv 2509.10179) **[letto]** conferma che l'istruzione allontana dallo stile umano e che in ceco i modelli vanno «molto peggio» che in inglese. Sull'italiano non c'è niente, ma il ceco suggerisce che lo scarto in una lingua meno rappresentata è maggiore **[inferenza]**.

**Corrispondente italiano [inferenza]**: il gerundio. Il caso più tipico è il **gerundio in coda dopo una virgola**, che aggiunge un effetto alla frase principale («…, creando un muro di morte», «…, irradiando una luce dorata»). È la stessa costruzione che B&K chiedono di riscrivere (voce 6) e lo stesso «gerundio d'analisi» che `italiano-nativo.md` §9.2-bis giudica non rilevabile perché «135 gerundi sono italiano normale». **La ricetta stretta lo rende rilevabile**: virgola, gerundio, poi la fine della frase. Nei box trova 28 casi in ARC-08 e uno in ARC-07 DEF **[misurato]**, e tutti gli esempi letti sono il tic vero.

### 5.2 La correzione manuale del testo LLM, misurata

- **Baumler e altri**, arXiv 2604.24444 (https://www.alphaxiv.org/abs/2604.24444.md) **[letto]**: 81 persone correggono una bozza LLM per renderla «propria». La correzione avvicina lo stile alla scrittura della persona (g = 0,55), ma il testo resta più vicino all'LLM che al suo stile spontaneo (g = −1,43). Le correzioni tipiche: trattini lunghi tolti per circa il 23%, parole marcate cancellate, frasi fiorite semplificate. Il numero di interventi correla con la somiglianza (r = 0,31). **Lo studio non misura la qualità percepita.**
- LAMP, Antislop e WQRM sono nel primo giro e non li ripeto. Resta il fatto già noto: **nessuno studio letto mostra che un passaggio a regole, da solo, migliori la preferenza umana**. Le prove dirette riguardano la revisione esperta (LAMP), mentre il divieto duro peggiora il testo (Antislop) **[letto nel primo giro]**.
- **StoryScope** (Russell e altri, arXiv 2604.03136, https://arxiv.org/abs/2604.03136v1) **[letto, abstract]**: le storie generate «spiegano troppo i temi» e preferiscono trame ordinate a filo unico. È il RUE di B&K misurato a livello di discorso (93,2% macro-F1 fra umano e IA). Come lo misurino in superficie l'abstract non lo dice.
- Gli «show, don't tell» rilevati da un LLM hanno κ ≈ 0 con l'annotatore umano su 100 scene, per cinque modelli di fila (forum Hugging Face, https://discuss.huggingface.co/t/claude-and-chatgpt-vs-a-human-annotator-on-show-dont-tell-features-one-definition-four-very-different-thresholds/178204) **[letto]**. Conferma che questi tratti vanno contati con regole, non affidati a un giudice.

---

## 6 · Classifica: metodi non ancora nel repo

Il protocollo è quello di `PROSA-DETERMINISTICA` §6: fotografia di partenza, 20 box fissi (4 per DEF, metà luogo e metà evento, seme dichiarato), preferenza cieca del DM ad alta voce con successo a ≥14/20, e il cancello di `ciclo_prosa` (nessuna norma cresce). Per ogni metodo aggiungo cosa si conta prima e dopo. Tutti i conteggi si riportano **con la lunghezza accanto** (parole del box).

### 1 · Gerundio in coda (proposizione participiale di effetto) — priorità **alta**
- **Ricetta**: `,\s+\w{3,}(?:ando|endo)(?:l[oaie]|si|ne)?\b[^.!?]{0,80}[.!?]`, esclusi `quando`, `secondo`, `comando`, `tremendo`, `orrendo`, `stupendo`, `reverendo`, `nefando`, `venerando`. Con Stanza: `VERB` con `VerbForm=Ger`, figlio `advcl` della radice e ultimo costituente della frase. Accanto si conta la **densità di gerundi ogni 1.000 parole**, come banda e non come «meno è meglio».
- **Falsi positivi attesi**: il gerundio modale o temporale voluto («esce sbattendo la porta»). È raro in coda dopo una virgola: negli esempi letti non ne ho trovato nessuno.
- **Prove**: [letto] Reinhart PNAS 2025 (2-5×, il tratto più discriminante); [letto] B&K voce 6; [misurato] 28 contro 1 fra ARC-08 e ARC-07 DEF.
- **Passaggio deterministico**: no. Si segnala e si propone, perché la riscrittura chiede una frase sua o un taglio (lo dice già `italiano-nativo.md`: «taglia la coda; se il legame conta, è una frase sua»). Va in `ciclo_prosa segnala`.
- **Prima e dopo**: gerundi in coda ogni 1.000 parole sui 20 box e sul corpus fisso; obiettivo vicino a quello di ARC-07 DEF. Il cieco decide.

### 2 · Densità di avverbi in -mente e di intensificatori — priorità **alta**
- **Ricetta**: `\b\w{4,}mente\b` meno una lista d'esclusione (`mente`, `demente`, `clemente`, `veemente`, `semente`, `fremente`); intensificatori su lista chiusa (`molto`, `davvero`, `assolutamente`, `incredibilmente`, `estremamente`, `terribilmente`, `completamente`, `totalmente`, `veramente`, `particolarmente`, `decisamente`, `profondamente`, `del tutto`). Si riportano ogni 10.000 parole per confrontarli con Blatt (<50 buono, >150 cattivo).
- **Falsi positivi**: avverbi necessari («lentamente» come istruzione di ritmo al DM). Per questo si conta una **densità**, non un divieto.
- **Prove**: [letto] B&K voci 2 e 13; [letto] Blatt, correlazione su un corpus inglese; [misurato] 60 contro 4 ogni 10.000 parole fra ARC-08 e ARC-07 DEF.
- **Passaggio deterministico**: solo per *simbolicamente*, *letteralmente* e *chiaramente* nei box, che sono quasi sempre importanza dichiarata [inferenza]. Si propone la cancellazione e il DM approva in `applica`.
- **Prima e dopo**: -mente ogni 10.000 parole sui 20 box; soglia d'allarme a 50.

### 3 · Lunghezza della battuta del PNG — priorità **alta** per ARC-07
- **Ricetta**: battute nel formato `**NOME (…):** *«…»*` su più righe, con i `>` tolti. Si contano le parole per battuta: banda ≤25, allarme oltre 40. Allarme anche per tre battute lunghe di fila dello stesso PNG (BioWare: alternare).
- **Falsi positivi**: il monologo voluto (un dio, un villain al climax). Si esenta con un marcatore esplicito, come il repo fa per altre norme.
- **Prove**: [letto, seconda mano] BioWare 25/40; [letto] Skyrim 149 caratteri; [letto] Game Developer 62 → 20 parole. È consenso di settore, nessuno studio. [misurato] ARC-07 DEF ha 12 battute su 33 oltre 25 parole e 5 oltre 40 (massimo 80).
- **Prima e dopo**: quota di battute ≤25 e numero oltre 40. Nel campione cieco vanno aggiunte 4 battute oltre 40 accanto ai 20 box (o al loro posto).

### 4 · Tetto alla frase più lunga del box, compatibile con «l'italiano respira lungo» — priorità **media**
- **Ricetta**: frasi tagliate su `.!?`; si conta la frase più lunga per box e le frasi oltre 35 parole. **Non** la media e **non** il tetto di 20 della radio, che contraddirebbe `italiano-nativo.md` §4. Con Stanza si aggiunge la **posizione della radice** (parole prima del verbo principale): allarme oltre 12.
- **Falsi positivi**: il periodo lungo voluto prima della frase corta che chiude. Per questo si mette un tetto alto e si guarda solo la coda della distribuzione.
- **Prove**: [letto] The News Manual (≤20 parole, una o due idee per frase); [letto] Peelle 2009 (la complessità costa di più all'ascolto e con l'età). [misurato] p90 25-27 parole, massimo 58. La soglia di 35 è un'**inferenza** da tarare.
- **Prima e dopo**: numero di frasi oltre 35 parole e p90 della lunghezza nei 20 box.

### 5 · Un solo argomento lessicale nuovo per proposizione (Du Bois) — priorità **media**, serve Stanza
- **Ricetta**: per ogni proposizione (verbo e suoi dipendenti `nsubj`, `obj`, `obl`) si contano i nomi pieni (`NOUN`/`PROPN`, non pronomi) **mai comparsi prima nel box**. Allarme con ≥2 nuovi nella stessa proposizione. Generalizza «un nome proprio nuovo per box» ai nomi comuni e alla proposizione.
- **Falsi positivi**: la prima frase di un box di luogo, che deve introdurre il luogo. Va esentata la prima proposizione.
- **Prove**: [letto] Du Bois tramite Chui, descrittivo sul parlato spontaneo (94% e 100%). Che migliori l'ascolto di un testo letto è **un'inferenza**.
- **Prima e dopo**: proposizioni con ≥2 argomenti nuovi ogni 100 proposizioni, sui 20 box.

### 6 · Spiegazione del gesto (RUE) — priorità **media** come guardia, bassa come bersaglio
- **Ricetta**: `come (se )?(a|per) (dire|voler|sottolineare)`, `quasi a (dire|voler)`, `a (indicare|sottolineare|significare|testimoniare) (che|il|la)`, `segno che`, `il che (significa|vuol dire)`, `in segno di`. Si cercano dopo un'azione o una battuta, nella stessa frase.
- **Falsi positivi**: «in segno di resa» detto come fatto. Basso, il conteggio è piccolo.
- **Prove**: [letto] B&K voci 2 e 5; [letto] StoryScope, le storie IA «spiegano troppo i temi». [misurato] un solo caso nei box di oggi: serve sulle **generazioni nuove** e nel testo per il DM.
- **Passaggio deterministico**: il taglio della coda da «come a dire» fino alla fine della frase è quasi sempre sicuro [inferenza]. Si propone e il DM approva.
- **Prima e dopo**: conteggio sulle corse nuove di `voto_scrittura` più che sui master.

### 7 · Pronomi soggetto tonici (lui, lei, egli, ella, essi) — priorità **bassa** nei box, **media** su handout e recap
- **Ricetta**: inizio di frase, dopo virgola o dopo «e/ma/poi», seguito dal verbo: `(?:^|[.!?;:»]\s+|,\s+|\be\s+|\bma\s+)(egli|ella|essi|esse|lui|lei)\s+(?!stess)…verbo`. «Egli» e «ella» si segnalano sempre, perché sono spia di registro arcaico o burocratico.
- **Falsi positivi**: il contrasto («lui resta, lei va») e l'enfasi, che sono italiano nativo. La correzione non è cancellare: è il **nome o il soggetto nullo**, rispettando `read-aloud-adulti.md` riga 48 (ri-ancorare dopo tre righe).
- **Prove**: [letto] Cardinaletti, Garzone, Giusti tramite il lavoro sul doppiaggio; Ondelli e Sciumbata (esplicitazione attesa); Valentini e altri (il pronome come indicatore di traduttese degli LLM, senza l'italiano). [letto] Gallitelli, Laurenti e Parks: «egli» ormai a circa 1 ogni 10.000 parole nella narrativa. [misurato] 2 casi nei box. La norma è già scritta in `italiano-nativo.md` §1, riga 2, **senza rilevatore**: il rilevatore la chiude (obbligo G3).
- **Prima e dopo**: conteggio su handout, recap ed echi, che non ho misurato.

### 8 · Verbi fasali «cominciò a / iniziò a» + infinito — priorità **bassa**, il passaggio più economico
- **Ricetta**: `(comincia|cominciò|inizia|iniziò|prende|si mette)(no|rono)?\s+a\s+\w+(are|ere|ire)(si)?`.
- **Falsi positivi**: quando l'inizio dell'azione è l'informazione («comincia a tirare»). Va proposto, mai applicato da solo.
- **Prove**: consenso diffuso sull'autorevisione, nessuna fonte primaria letta [inferenza]. [misurato] 9 casi in 291 box.
- **Prima e dopo**: conteggio; è un intervento piccolo, il cieco non lo vedrà da solo.

### Scartati, con la ragione
- **Filter words in seconda persona**: già coperte da P1 (`_P1_VEDERE`). In terza persona c'è un solo caso [misurato].
- **Verbo supporto + nome astratto**: zero casi veri nei box; in parte già in `CALCHI_SEMPRE`. Da riconsiderare sul testo per il DM.
- **«Andare a» + infinito e frasi scisse**: nessuna fonte li dà per calchi, zero casi.
- **Said-bookisms nel formato del repo**: il tono fra parentesi è una norma scelta (`editorial-standards.md` §2). Contarlo vorrebbe dire combattere una norma registrata. Il conflitto va segnalato al DM, non risolto da un rilevatore.
- **Coppie di aggettivi senza tagger**: la mia regex sui suffissi aggettivali ha prodotto quasi solo rumore («altare, preparandosi», «naniche, giganti») [misurato]. Serve Stanza (`ADJ` + `ADJ` attaccati allo stesso `NOUN`). La norma c'è già in `italiano-nativo.md` §1 («una fredda, silenziosa pietra»); il rilevatore va rimandato al giorno in cui ci sarà un tagger nel container.
- **Relative sull'oggetto all'ascolto (Peelle)**: le prove sono buone, ma servono un parser e una taratura sull'ambiguità del «che». Da riprendere insieme al n. 5.

---

## 7 · Cosa non ho fatto, e i limiti

- Non ho letto il libro di Browne e King né quello di Sol Stein; per B&K ho usato un riassunto universitario della checklist. Orwell e Strunk non danno né soglie né prove, e li ho lasciati fuori.
- I risultati di Ondelli e Sciumbata sulla narrativa (cap. 3) non sono nella parte del PDF che il fetch riesce a leggere: le cifre sui possessivi restano da trovare.
- Tutti i miei conteggi sono regex su 291 box, senza tagger e con i duplicati di ARC-08 dentro. Sono indizi di ordine di grandezza, non numeri da pubblicare: andrebbero rifatti con `fase1.py` e `misura_craft`, come chiede G6.
- Il contrasto fra ARC-08 e ARC-07 DEF non prova che i rilevatori misurino la qualità. Prova solo che separano una generazione vecchia da una riscritta che il DM ha approvato. Il cieco resta l'unico metro del «meglio».
