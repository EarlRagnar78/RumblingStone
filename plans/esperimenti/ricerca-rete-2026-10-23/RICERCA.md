# Ricerca in rete: strumenti liberi che misurano mappe, moduli e regole

**Data**: 2026-10-23 · **Richiesta del DM** (Jfs), testuale: «ora che i siti
sono sbloccati sei sicuro che non c'è qualcosa in rete che migliora la qualità
del progetto misurando il miglioramento?». Contesto: le mappe tattiche di
ARC-08 (ADR-0098, `qualita_mappe.py`, `confronta_mappe.py`) e i master
ARC08-DEF-1 e DEF-2 (letture a freddo di ADR-0095, `misura_craft`,
`ciclo_prosa`, `domande_developer`).
**Stato**: esperimento. Il riscontro SRD del §3 è entrato in canale testing
come `scripts/riscontro_srd.py` ([ADR-0103](../../adr/ADR-0103-le-regole-si-riscontrano-sull-srd-in-cache.md));
il resto no. Gli script di prova stanno in `prove/`, i risultati in `out/`. I dati scaricati
(SRD 3.5, PRD PF1e, il codice dei candidati) stanno fuori dal repo, nella
cartella di lavoro della sessione.

Le affermazioni hanno il link della fonte. Quello che è dedotto da chi scrive
porta **[INFERRED]**.

## In breve

- **L'SRD in locale serve, e ha già trovato un errore nel master.** Con l'SRD
  3.5 in Markdown ([olimot/srd-v3.5-md](https://github.com/olimot/srd-v3.5-md),
  OGL) e il PRD di Pathfinder in SQLite
  ([devonjones/PSRD-Data](https://github.com/devonjones/PSRD-Data), OGL) le
  nove regole che il giro della Sessione 2 aveva controllato a memoria si
  riscontrano in 0,04 s: otto concordano, una no. DEF-2 scrive che la
  *freccia assassina* fa «50 danni» e che «l'SRD 3.5 dà i 50 danni»; l'SRD 3.5
  dice **«save or die»**, i 50 danni sono la regola di Pathfinder (*Ultimate
  Equipment*). Il triage (T36, N12) aveva accettato la versione sbagliata.
  **Da adottare in prova.**
- **Le misure di Liapis (area sicura, esplorazione, bilancio) e la linea di
  tiro sull'avvicinamento** si calcolano in 0,5 s sulle mappe di ARC-08 e sono
  deterministiche, ma non dicono se una mappa è migliore: gli scontri del
  modulo sono asimmetrici per scelta, nessuna fonte dà una soglia, e metà del
  segnale è già nelle metriche dello standard (ρ 0,57 con la distanza fra le
  fazioni, −0,61 con la copertura). **Scartare** come metrica; il DM decide se
  vuole la linea di tiro come numero informativo.
- **Simulatori di combattimento 3.5 liberi**: quelli trovati sono fermi da anni
  e non girano (pyd20 non passa la raccolta dei suoi test su Python 3.13).
  **Scartare.**
- **Ludii, GVGAI, EDD, pattern di Baldwin, linearity e leniency** non portano
  niente di misurabile alle battlemap: licenza non libera (Ludii), giochi
  arcade in tempo reale (GVGAI), codice non pubblicato e soglie scelte
  dall'utente (EDD), metriche da platform già scartate dallo standard.
- **La rete di questa sessione non è sbloccata per gli script.** `curl` passa
  solo verso GitHub (git e `raw`), PyPI, npm, GitLab e Bitbucket; d20srd,
  aonprd, arXiv, Wikipedia, AAAI, Hugging Face: 97 dei 110 domini provati
  danno 403 al tunnel. WebFetch, che esce dai server di Anthropic, li legge;
  Firecrawl è senza crediti. L'elenco esatto è in fondo.

## 1. Cosa c'era già

Prima di cercare si è letto:

- `plans/esperimenti/mappe-strumenti-2026-10-22/RICERCA-STRUMENTI-MAPPE.md`:
  space syntax (oggi `qualita_mappe_profonde.py`), confronto fra versioni
  (oggi `confronta_mappe.py`), OR-Tools, clingo, python-constraint, python-sat,
  Sturgeon, WFC, depthmapX, alcyon, topologicpy, `pcg_benchmark`, `gym-pcgrl`,
  networkx, shapely già valutati, con i motivi del no;
- RICERCA-QUALITA-MISURABILE-2026-10 (in `plans/` sul ramo
  `claude/project-thread-nfo3yf`, commit `b5adf4e2`; non su questo ramo): 17 misure di prosa sui
  38 voti ciechi del DM, nessuna lo prevede; per l'architettura la Three Clue
  Rule, la domanda drammatica, i fronti e gli orologi, diventate D18-D21;
- `plans/esperimenti/piattaforma-2026-10-23/`: ruff, uv, xdist già adottati;
- lo standard delle mappe (`standard-qualita-mappe.md`): Liapis 2013 è citato
  come base della distanza fra le fazioni, ma l'area sicura, l'esplorazione e
  il bilancio non sono calcolati; *leniency* e *linearity* sono state scartate
  («la traduzione dal platform non regge»);
- `validate_tipografia.py` simula già il daltonismo sulle tavole SVG;
- la memoria del progetto: d20srd, d20pfsrd e archive.org bloccati
  (`srd-in-rete`), paizo, wizards, gruppochimera, dragonslair bloccati per il
  corpus della prosa, Hugging Face aperto il 2026-10-22 con il protocollo Xet
  chiuso.

**Fonti che le ricerche precedenti non avevano raggiunto**, da cui si è
cominciato: d20srd.org e d20pfsrd.com (il giro della Sessione 2 aveva
controllato le regole a memoria: `PLAYTESTER.md` riga 9, `VERIFICA.md` riga 5,
`TRIAGE.md` N12), archive.org, i siti degli editori per il corpus. La ricerca
sugli strumenti delle mappe non dichiara fonti mancate; leggeva le licenze dal
`LICENSE` grezzo su raw.githubusercontent.com.

## 2. Come si è cercato

Firecrawl ha risposto «Insufficient credits» alla prima chiamata. La ricerca è
andata avanti con WebSearch e WebFetch e, per scaricare, con `git clone` e
`curl` attraverso il proxy. WebFetch legge d20srd.org, legacy.aonprd.com,
ojs.aaai.org e pcgworkshop.com; `curl` no (§6).

## 3. Controlli SRD in locale

### I due archivi

| Archivio | Licenza | Ultimo commit | Formato | Peso | Si scarica qui |
|---|---|---|---|---|---|
| [olimot/srd-v3.5-md](https://github.com/olimot/srd-v3.5-md) | OGL 1.0a (file `legal-information.md`; la PI di Wizards esclusa) | `c7f30a0c`, 2024-02-16 | 118 file Markdown con tabelle HTML | 7,5 MB | sì, `git clone --depth 1` |
| [devonjones/PSRD-Data](https://github.com/devonjones/PSRD-Data) | OGL (il libro `book-ogl.db`; nessun file `LICENSE` nel repo) | `76ea4784`, 2015-05-08 | un SQLite per manuale (CR, APG, UE, UC, Bestiari 1-4…) con tabelle strutturate per incantesimi, creature, oggetti | 277 MB | sì, `git clone --depth 1` |

Nessuno dei due è su PyPI; il codice di prova li legge da una cartella passata
come argomento, con `python3 -I`.

### La prova

`prove/riscontro_srd.py` legge `prove/affermazioni-sessione2.json`: le regole
che i quattro lettori del giro della Sessione 2 hanno segnato «a memoria»,
ognuna con l'espressione da cercare nell'SRD e quella da cercare nel master.

```bash
python3 -I prove/riscontro_srd.py prove/affermazioni-sessione2.json SRD35_DIR PSRD_DIR .
```

| Rilievo del giro | Regola | SRD 3.5 (o PRD) | Master oggi | Esito |
|---|---|---|---|---|
| P#39, DM-R12, L#40, T36, N12 | *freccia assassina*, TS fallito | «DC 20 Fortitude save or die» | «Tempra CD 20 o subisce 50 danni … l'SRD 3.5 dà i 50 danni» (DEF-2 r. 1393-1397) | **discorda** |
| idem | la stessa in PF1e | «DC 20 Fortitude save or take 50 points of damage» (*Ultimate Equipment*) | — | i 50 danni vengono da qui |
| P#39 | danni extra a TS riuscito | nessuno nel testo 3.5 | nessuno | concorda (R5 del triage aveva ragione) |
| P#36, N12, T1 | togliere un'armatura pesante | 1d4+1 minuti; **con aiuto la metà** | 1d4+1 minuti | concorda; `TRIAGE.md` N12 scrive «con aiuto», che è l'opposto |
| P#38, T35 | *comunione*, tempo di lancio | 10 minuti | 10 minuti (DEF-2 r. 261, `ARC08-15` r. 241) | concorda |
| DM-R20, T35 | *comando* | elenco chiuso nel 3.5 («You may select from the following options»): avvicinati, lascia, cadi, fuggi, fermati | «Lascia!» | concorda; «Apri» non c'è, come diceva il DM |
| DM-R9, T30 | Scalare la corda | un quarto della velocità per azione di movimento, metà con −5 | 5 round, 3 con l'accelerata | concorda |
| P#17, T5 | *scudo*, durata | 1 minuto per livello | 7 minuti a ogni passaggio | concorda |
| D-R3, R1 | l'ettin, due armi | «2 morningstars +12/+7»: gli iterativi a ogni mano, senza penalità | sei colpi | concorda |

Otto concordano, una discorda, nessuna resta senza risposta.

La discordanza è un problema di **attribuzione**: il master chiama SRD 3.5 una
regola di Pathfinder. La scelta fra le due la fa il DM. La preferenza
registrata in memoria («la versione più potente e terrificante, cercando
nell'ordine D&D 3.5, poi PF1e») indicherebbe il «muore» del 3.5; con Tempra +21
Fauci fallisce solo con un 1 naturale, quindi al tavolo cambia poco, ma se la
freccia lo prende il drago muore invece di perdere 50 pf su ~230. **Domanda
per il DM.**

Fuori dall'elenco del giro, la stessa prova ha toccato la riga 40 di DEF-2
(«per l'SRD una balista pesante ha incremento 36 m»): l'SRD 3.5 non ha le
macchine d'assedio (il file sul tempo atmosferico le nomina soltanto); in
Pathfinder la balista **leggera** ha 120 piedi (36 m) e la **pesante** 180
piedi (54 m) ([PRD, *Ultimate Combat*](https://legacy.aonprd.com/ultimateCombat/combat/siegeEngines.html),
letto con WebFetch). Il PSRD-Data locale non ha quella tabella: è un limite
dell'archivio, che è del 2015. Il 36 m coincide con la balista del DMG 3.5
[INFERRED, a memoria], che non è OGL. Anche qui decide il DM; la riga è già
marcata ⚙️ nel master.

### Che cosa costa e che cosa resta fuori

- La prova copre nove regole scelte a mano. DEF-1 e DEF-2 nominano «SRD» 55
  volte; un riscontro automatico di tutte richiede un glossario
  italiano-inglese dei nomi di incantesimi, oggetti e creature, che il repo non
  ha in forma leggibile da una macchina [INFERRED].
- I due archivi sono testi: la prova cerca espressioni, non capisce le regole.
  Un'espressione scritta male dà «non trovato» (è successo due volte nella
  prima esecuzione, corrette).
- Il PSRD-Data è fermo al 2015 e incompleto (la tabella delle macchine
  d'assedio manca). Per il 3.5 l'archivio Markdown è completo rispetto
  all'SRD, ma l'SRD stesso non contiene il DMG.
- La licenza OGL permetterebbe di mettere l'SRD nel repo con il testo della
  licenza; la regola del repo per i testi di terzi è di tenerli fuori. Un
  `git clone` in una cartella esterna, come per la skill di scrittura
  italiana di ADR-0097, è la via che non tocca la regola.

**Raccomandazione: adottare in prova.** Un comando che, dato un elenco di
affermazioni (o i rilievi «a memoria» di un giro), le riscontra sui due
archivi clonati fuori dal repo, e un passo nel giro dei lettori: ogni rilievo
segnato «a memoria» passa dal riscontro prima del triage. La misura del
miglioramento è quella di questa prova: rilievi «a memoria» rimasti aperti
dopo il triage, 9 → 0, e discordanze trovate, 1.

## 4. Mappe: misure nuove provate su ARC-08

### Che cosa offre la rete

| Candidato | Licenza | Ultimo commit | Che cosa misura | Esito |
|---|---|---|---|---|
| Liapis, Yannakakis, Togelius, [*Towards a Generic Method of Evaluating Game Levels*](https://ojs.aaai.org/index.php/AIIDE/article/download/12680/12528/16197) (AIIDE 2013) | metodo pubblicato | — | area sicura per fazione (eq. 1, soglia 0,35), esplorazione (riempimento a 4 direzioni fino all'altra fazione, eq. 2), bilancio di area e di esplorazione | **provato**, §4.2 |
| Linea di tiro sull'avvicinamento [INFERRED: misura costruita qui sul modello dei pattern «sniper location» e «arena» di Hullett e Whitehead, [*The Science of Level Design*](https://eis.ucsc.edu/papers/khullett-fdg-doccon-camera-ready.pdf)] | — | — | quota del cammino PG → nemico vista dai nemici, e senza copertura | **provato**, §4.2 |
| Evolutionary Dungeon Designer, pattern di Baldwin et al. ([PCG 2017](https://www.pcgworkshop.com/archive/baldwin2017patternbased.pdf), [EDDy](https://games.mau.se/research/eddy/)) | nessuna licenza né codice pubblicati trovati | — | stanza di guardia, del tesoro, imboscata, vicolo cieco; ogni qualità è la distanza da un **obiettivo che sceglie l'utente** | scartato senza prova: l'imboscata è una stanza con l'ingresso e un nemico, il vicolo cieco è già nello standard, e le soglie le sceglie chi usa lo strumento |
| Smith e Whitehead, *linearity* e *leniency* | metodo | — | regressione delle altezze delle piattaforme; pericoli sul cammino | già scartate dallo standard (platform); confermato |
| [Ludii](https://github.com/Ludeme/Ludii) | **CC BY-NC-ND 4.0** (letta dal `LICENSE`) | 2025-02-21 | giochi da tavolo astratti descritti in ludemi; metriche su partite simulate | scartato: non è libera e non descrive battlemap |
| [GVGAI](https://github.com/GAIGResearch/GVGAI) | GPL-3 | 2021-07-12 | giochi arcade in tempo reale (VGDL), agenti che li giocano | scartato: Java, fermo dal 2021, niente turni né regole d20 |
| Khalifa et al., *On the Evaluation of Procedural Level Generation Systems* ([arXiv 2404.18657](https://arxiv.org/html/2404.18657v1)) | articolo | — | rassegna: gamma espressiva, simulazione con agenti, studi con persone | conferma quello che ADR-0098 fa già (misure senza soglia, confronto fra versioni); niente di nuovo da calcolare |

### La prova

`prove/fazioni_liapis.py` usa il parser e il grafo di `collaudo_mappe.py`
(otto direzioni, la diagonale non passa l'angolo di un muro) e lo
shadowcasting simmetrico di `tcod` già in `requirements-dev.txt`. Nessuna
dipendenza nuova. `--rev` legge una versione da git senza toccare il disco.

```bash
python3 prove/fazioni_liapis.py "08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md" …
python3 prove/fazioni_liapis.py --rev d726e6a2 …     # le mappe prima dei rifacimenti
```

Le tre mappe master di ARC-08 hanno nove griglie con PG e nemici prima dei
rifacimenti (commit `d726e6a2`, la versione A del confronto del 2026-10-22) e
otto oggi (la MAPPA 4 non ha più i segnalini di entrambe le fazioni). I voti di
`qualita_mappe.py` vengono da
`plans/esperimenti/confronto-mappe-arc08-2026-10-22/CONFRONTO.md`.

| Mappa | Voto A → oggi | Bilancio d'area A → oggi | Bilancio d'esplorazione | Avvicinamento visto dai nemici | Di quello, senza copertura |
|---|---|---|---|---|---|
| 1A-2 | 93 → 94 | 0,17 → 0,17 | 0,55 → 0,55 | 1,00 → 1,00 | 1,00 → 1,00 |
| 1A-1 | 87 → 94 | 0,26 → 0,28 | 0,52 → 0,54 | 1,00 → 1,00 | 0,24 → 0,24 |
| 1D | 97 → 98 | 0,37 → 0,37 | 0,56 → 0,56 | 1,00 → 1,00 | 0,00 → 0,00 |
| 2B | 78 → 94 | 0,03 → 0,27 | 0,20 → 0,63 | 1,00 → 1,00 | 0,67 → 1,00 |
| H3-1 | 91 → 94 | 0,65 → 0,96 | 0,77 → 0,93 | 1,00 → 1,00 | 1,00 → 0,50 |
| 3Y | 78 → 94 | 0,92 → 0,47 | 0,67 → 0,67 | 1,00 → 1,00 | 1,00 → 0,80 |
| 3Z | 43 → 98 | 0,31 → 0,11 | 0,40 → 0,24 | 1,00 → 1,00 | 0,50 → 0,50 |
| 5 | 81 → 94 | 0,04 → 0,03 | 0,09 → 0,14 | 1,00 → 0,07 | 0,50 → 0,00 |

Numeri completi in `out/liapis-A.md` e `out/liapis-C.md`; due esecuzioni danno
lo stesso SHA (deterministico).

Come si leggono:

- **La linea di tiro satura.** Su sette mappe su otto i nemici vedono l'intero
  cammino d'avvicinamento, prima e dopo: le mappe di ARC-08 sono cortili,
  pendii e bastioni all'aperto. Sul corpus intero (50 griglie con PG e
  nemici) la mediana è 0,63 e 17 griglie sono a 0,95 o più. Su un modulo di
  battaglia campale il numero non distingue.
- **Il bilancio non va nella direzione del voto**, e non deve. Sulla 3Z il voto
  sale da 43 a 98 e il bilancio d'area scende da 0,31 a 0,11: il rifacimento ha
  messo i bugbear in agguato nei tunnel, che è quello che la scena chiede. Uno
  scontro d'imboscata o d'assedio è asimmetrico per progetto; Liapis misura
  mappe di strategia in tempo reale dove l'equilibrio è un requisito.
- **La 5 è la mappa in cui il rifacimento ha cambiato la tattica**: il cammino
  dei PG verso i nemici è passato da tutto visto a quasi tutto coperto (1,00 →
  0,07). È l'unico caso in cui la misura dice qualcosa che il voto non dice;
  se sia un miglioramento lo sa solo chi conosce la scena.

`prove/ridondanza.py` mette in rango le misure nuove contro quelle che lo
standard già calcola, sulle 50 griglie del corpus (`out/ridondanza.md`):

| Misura nuova | voto | distanza PG-nemici | copertura | M1 | M2 | libere |
|---|---|---|---|---|---|---|
| area sicura dei PG | +0,06 | −0,08 | −0,08 | −0,07 | +0,06 | −0,01 |
| bilancio d'area | −0,30 | +0,36 | +0,26 | +0,29 | −0,27 | −0,18 |
| esplorazione dei PG | −0,13 | **+0,57** | +0,30 | +0,35 | −0,42 | **−0,57** |
| bilancio d'esplorazione | −0,27 | +0,44 | +0,23 | +0,28 | −0,25 | −0,23 |
| avvicinamento senza copertura | −0,02 | −0,18 | **−0,61** | **−0,63** | **+0,65** | +0,57 |

Nessuna è un doppione (|ρ| < 0,8), ma l'esplorazione segue la distanza fra le
fazioni e la linea di tiro scoperta segue la copertura; l'area sicura è quasi
indipendente da tutto perché dipende solo da dove stanno i segnalini.

**Raccomandazione: scartare** le misure di Liapis come metriche dello standard
(nessuna soglia, la direzione «giusta» dipende dalla scena, il segnale utile è
già nella distanza e nella copertura). **Da decidere dal DM** se vuole vedere,
nel confronto fra due versioni, la quota d'avvicinamento coperta: è l'unico
numero che sulla MAPPA 5 ha raccontato un cambiamento tattico. Sarebbe una
colonna di `confronta_mappe.py`, non un rilievo.

## 5. Moduli e incontri

| Candidato | Licenza | Ultimo commit | Prova | Esito |
|---|---|---|---|---|
| [pyd20](https://github.com/dkargin/pyd20) (simulatore di battaglia 3.5 su griglia) | GPL-2 | 2017-08-11 | clonato, `pytest test`: 5 errori su 5 alla raccolta (import circolare del pacchetto) su Python 3.13; implementa attacco, attacco completo, movimento e attacchi d'opportunità, niente incantesimi, coperture né creature volanti | scartato: non gira, e non simulerebbe un drago che soffia su un re |
| [CombatWiz / CombatSim](https://pypi.org/project/CombatWiz/) | BSD | 0.12, 2013-06-29 | solo metadati da PyPI | scartato: simulatore generico, non d20, fermo dal 2013 |
| [PCGen](https://github.com/PCGen/pcgen) | LGPL-2.1 | 2026-10-18 (nightly del 2026-10-19) | non eseguito; ha i dati 3.5 e PF1e in `data/35e` e `data/pathfinder` | da decidere dal DM: costruisce e controlla schede di PG, quindi servirebbe ai pregen, non ai master; Java e formato LST da imparare |
| Three Clue Rule misurabile ([The Alexandrian](https://thealexandrian.net/?p=7985), [node-based design](https://thealexandrian.net/creations/misc/node-design/node-design2.html)) | metodo | — | i master DEF-1 e DEF-2 non hanno marcatori `<!-- conclusione -->` né `<!-- indizio -->` (D21 della #264 non è su questo ramo) | niente da misurare su ARC-08, che è un arco di battaglia; il metodo è già D21 |
| Budget di EL e ritmo | — | — | nessuno strumento libero trovato oltre ai calcolatori 5e; la tabella dell'EL per gruppi misti è nel DMG 3.5, non nell'SRD (l'SRD la nomina solo per tesori e trappole) | niente da adottare; `suggest_encounter.py` resta il riferimento |

## 6. Domini bloccati

Provati il 2026-10-23 con `curl` attraverso il proxy della sessione. «Tunnel
403» vuol dire che il proxy rifiuta la connessione (`CONNECT tunnel failed,
response 403`, registrato anche in `__agentproxy/status`). WebFetch, che esce
dai server di Anthropic, ha letto d20srd.org, legacy.aonprd.com, ojs.aaai.org,
pcgworkshop.com e games.mau.se: il blocco pesa sugli script, sui `git clone` e
sui download, non sulla lettura.

**Raggiungibili**: `github.com` solo per git (`ls-remote`, `clone`; le pagine
web e `codeload.github.com` danno 403 per i repo non collegati alla
sessione), `raw.githubusercontent.com`, `objects.githubusercontent.com`,
`release-assets.githubusercontent.com`, `api.github.com` (radice; i repo
fuori sessione 403), `gitlab.com`, `bitbucket.org`, `pypi.org`,
`files.pythonhosted.org`, `registry.npmjs.org`. `www.npmjs.com`,
`sourceforge.net` e `crates.io` aprono il tunnel ma rispondono 403 dal loro
server.

**Tunnel 403** (97 domini), con la fonte che serviva:

| Dominio | Per che cosa |
|---|---|
| `www.d20srd.org` | SRD 3.5 (le regole del giro della Sessione 2) |
| `www.d20pfsrd.com`, `pf2.d20pfsrd.com` | PRD PF1e |
| `legacy.aonprd.com`, `aonprd.com`, `2e.aonprd.com`, `www.archivesofnethys.com` | PRD PF1e (le macchine d'assedio) |
| `dungeons.fandom.com`, `www.rpgcrossing.com`, `srd.dndtools.org`, `dndtools.net`, `www.dandwiki.com`, `www.5esrd.com` | mirror dell'SRD usati dalla memoria `srd-in-rete` |
| `olimot.github.io` | versione HTML dell'SRD 3.5 di olimot (il Markdown passa da git) |
| `web.archive.org`, `archive.org` | SRD originale di Wizards, pagine sparite |
| `www.wizards.com`, `paizo.com`, `www.drivethrurpg.com`, `www.dmsguild.com`, `www.dndbeyond.com` | editori |
| `www.gruppochimera.it`, `www.dragonslair.it` | corpus italiano |
| `arxiv.org`, `export.arxiv.org`, `ar5iv.labs.arxiv.org` | articoli di PCG (Lucas e Volz, Khalifa) |
| `ojs.aaai.org` | Liapis 2013, Cooper 2022 |
| `www.pcgworkshop.com`, `pcgworkshop.com`, `www.pcgbook.com` | Dormans, Smith e Whitehead, Baldwin |
| `dl.acm.org`, `ieeexplore.ieee.org`, `link.springer.com`, `www.semanticscholar.org`, `api.semanticscholar.org`, `api.openalex.org`, `dblp.org`, `scholar.google.com`, `citeseerx.ist.psu.edu`, `www.researchgate.net`, `www.academia.edu`, `paperswithcode.com`, `zenodo.org` | indici e editori accademici |
| `games.mau.se`, `pure.itu.dk`, `eis.ucsc.edu`, `escholarship.org`, `www.um.edu.mt`, `webdocs.cs.ualberta.ca`, `discovery.ucl.ac.uk`, `nottingham-repository.worktribe.com`, `course.ccs.neu.edu`, `www.cs.uky.edu`, `ianparberry.com`, `soletlab.asu.edu`, `boa.unimib.it`, `aclanthology.org`, `www.ledonline.it` | archivi universitari citati dalle ricerche |
| `ludii.games`, `www.gvgai.net` | Ludii, GVGAI |
| `thealexandrian.net`, `theangrygm.com`, `tenfootpole.org`, `www.enworld.org`, `www.giantitp.com`, `www.myth-weavers.com`, `www.reddit.com`, `old.reddit.com` | mestiere del DM, forum |
| `www.boristhebrave.com`, `www.gamedeveloper.com`, `www.redblobgames.com`, `www.jeremykun.com`, `www.albertford.com`, `isovists.org` | articoli sulla generazione e sulla vista |
| `ldtk.io`, `doc.mapeditor.org`, `help.roll20.net`, `roll20.net`, `watabou.itch.io`, `itch.io`, `alternativeto.net` | formati e programmi di mappe |
| `en.wikipedia.org` | voci su space syntax e VGA |
| `www.opengamingnetwork.com`, `kobold.club`, `www.pathfindercommunity.net`, `www.scribd.com` | strumenti e testi della community |
| `cran.r-project.org` | alcyon (R) |
| `huggingface.co`, `us.aws.cdn.hf.co`, `cas-bridge.xethub.hf.co`, `cas-server.xethub.hf.co` | modelli (la memoria li dà aperti dal 2026-10-22: in questa sessione non lo sono) |
| `nlp.stanford.edu`, `lindat.mff.cuni.cz`, `download.pytorch.org` | modelli di Stanza, UDPipe, PyTorch |
| `languagetool.org`, `deb.debian.org`, `typst.app` | la memoria li dà aperti dal 2026-10-23: in questa sessione non lo sono |

La differenza con la memoria va segnalata: Hugging Face, LanguageTool,
Debian, typst e l'SRD risultano aperti dal 2026-10-22/23 nell'ambiente del
progetto, ma questa sessione ha il tunnel chiuso verso tutti. O
l'apertura non vale per questo ambiente, o va riavviato [INFERRED].

## 7. I file di questa cartella

| File | Che cosa fa |
|---|---|
| `prove/riscontro_srd.py` | §3: riscontra un elenco di affermazioni sull'SRD 3.5 e sul PRD clonati fuori dal repo; `python3 -I` |
| `prove/affermazioni-sessione2.json` | le nove regole «a memoria» del giro della Sessione 2, con le espressioni da cercare |
| `prove/fazioni_liapis.py` | §4: area sicura, esplorazione, bilancio, linea di tiro; `--rev` per una versione di git |
| `prove/ridondanza.py` | §4: ρ di Spearman fra le misure nuove e quelle di `qualita_mappe.py` |
| `out/riscontro-srd.md` | la tabella del §3 |
| `riscontri-arc08.yaml`, `RISCONTRO-ARC08.md`, `out/riscontro-arc08.md` | il §3 adottato in testing ([ADR-0103](../../adr/ADR-0103-le-regole-si-riscontrano-sull-srd-in-cache.md)): 53 regole di DEF-1 e DEF-2 riscontrate con `scripts/riscontro_srd.py`, 3 discordanze |
| `out/liapis-A.md`, `out/liapis-C.md` e i `.json` | ARC-08 prima dei rifacimenti e oggi |
| `out/liapis-corpus.json`, `out/ridondanza.md` | le 50 griglie del corpus; il JSON di `qualita_mappe.py` si rigenera con `python3 scripts/qualita_mappe.py --json OUT.json` |

**Scaricati, fuori dal repo** (cartella di lavoro della sessione, non
committati): `srd35-md` (7,5 MB), `psrd-data` (277 MB), `pyd20`; i metadati di
GVGAI, Ludii e PCGen sono cloni senza file. Nessun pacchetto installato.

## Fonti

- SRD 3.5 in Markdown: https://github.com/olimot/srd-v3.5-md · PRD PF1e in SQLite: https://github.com/devonjones/PSRD-Data
- SRD 3.5, armature: https://www.d20srd.org/srd/equipment/armor.htm (WebFetch)
- PRD, macchine d'assedio: https://legacy.aonprd.com/ultimateCombat/combat/siegeEngines.html (WebFetch)
- Liapis, Yannakakis, Togelius 2013: https://ojs.aaai.org/index.php/AIIDE/article/download/12680/12528/16197 (WebFetch)
- Baldwin et al. 2017: https://www.pcgworkshop.com/archive/baldwin2017patternbased.pdf (WebFetch) · EDDy: https://games.mau.se/research/eddy/
- Hullett, *The Science of Level Design*: https://eis.ucsc.edu/papers/khullett-fdg-doccon-camera-ready.pdf
- *On the Evaluation of Procedural Level Generation Systems*: https://arxiv.org/html/2404.18657v1
- Ludii: https://github.com/Ludeme/Ludii (LICENSE) · GVGAI: https://github.com/GAIGResearch/GVGAI (LICENSE.txt) · PCGen: https://github.com/PCGen/pcgen
- pyd20: https://github.com/dkargin/pyd20 · CombatWiz: https://pypi.org/project/CombatWiz/
- The Alexandrian: https://thealexandrian.net/?p=7985 · https://thealexandrian.net/creations/misc/node-design/node-design2.html
