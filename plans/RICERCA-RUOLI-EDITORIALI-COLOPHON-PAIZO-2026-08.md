# 🏛️ RICERCA — I ruoli del colophon Paizo, misurati sulle skill del repo

**Aperta**: 2026-08-26
**Domanda-fonte (DM)**: *«questa immagine presenta i componenti necessari a un
progetto editoriale per una saga completa Paizo: tenendo conto della skill
editoriale presente nel repo, manca qualcosa nelle skill o nella combinazione di
skill? Quali altri ruoli sarebbe opportuno aggiungere per arrivare a un livello
paragonabile? Quali server MCP, se esistono, servirebbero, o quali tool
potrebbero migliorare la resa editoriale finale?»*

**Fonte**: la pagina dei crediti di *Ascesa dei Signori delle Rune — Saga
Completa* (Paizo / Giochi Uniti — Wyrd Edizioni, ristampa 2019), fotografata dal
DM. Contiene **due** colophon sovrapposti: quello dell'edizione originale
(autori, redazione, arte, cartografia, più l'organigramma dell'azienda) e quello
dell'**edizione italiana** (direttore responsabile, supervisione, traduzione,
grafica, adattamento grafico della ristampa, produzione), seguiti dalle
dichiarazioni legali (Product Identity, Open Content, OGL 1.0a), dal
ringraziamento ai playtester e dai dati di stampa e distribuzione.

**Metodo**: leggere il colophon **come un capitolato** — ogni riga è un mestiere
che qualcuno ha dovuto fare perché quel volume esistesse — e cercare, per ognuno,
chi lo fa in questo repo. Le prove sono comandi e percorsi di file, non
impressioni. Dove il repo ha già deciso di non fare una cosa, questo documento
**non la riapre**: la cita e rimanda alla decisione.

> **La conclusione in tre righe**: le skill non hanno un buco di *mestiere* — il
> divario grosso non è un ruolo mancante, è che **i volumi del repo non hanno un
> colophon**: nessun credito, nessuna licenza, nessuna data, nessuna versione. La
> pagina che il DM ha fotografato è esattamente quella che i booklet di
> RumblingStone non stampano. E dei ventuno ruoli elencati, **otto sono coperti
> bene, quattro sono fuori perimetro per decisione già presa, e i restanti nove
> si concentrano in due mestieri veri: la redazione come *processo* e l'edizione
> come *oggetto con una versione*.**

---

## §1 · Il colophon, riga per riga, mappato sul repo

Ventuno voci. La colonna «qui» dice chi lo fa oggi; il verdetto è misurato, non
stimato.

| Ruolo nel colophon | Chi lo fa nel repo | Verdetto |
|---|---|---|
| **Autori** (6 nomi) | `rumblingstone-narrative-style` (9 pilastri) + `rumblingstone-module-standard` + `rumblingstone-indagine` + `rumblingstone-campaign` + le tre skill di regole | ✅ **il pezzo più forte del repo**, e con un margine |
| **Redazione** (17 nomi) + **assistenti** | `references/editorial-standards.md` (dentro narrative-style) + `validate_modules.py` | 🟡 **le regole ci sono, il processo no** — vedi §2.C2 |
| **Capo del progetto** | `rumblingstone-plans` (piani, lotti, INDEX, CHANGELOG) | 🟡 traccia il lavoro, non **compone il volume**: nessun budget di pagine, nessuna scaletta d'uscita |
| **Copertina** · **Illustrazioni interne** · **Sezione artistica** | `rumblingstone-art-direction` (bibbia visiva, scheda-personaggio, gate di rifiuto) | ✅ maturo — l'audit di agosto lo dava già come «la parte più matura» |
| **Cartografia** | `rumblingstone-mapmaking` (3 modalità, contratto JSON, renderer deterministico, UVTT) | ✅ **il componente più maturo del repo** |
| **Grafica / impaginazione** (Avatar Studio, nel colophon italiano) | `rumblingstone-editoria` + `scripts/typst/tema-rumblingstone.typ` | ✅ dal 2026-08-22, con le rinunce dichiarate in §5 della skill |
| **Adattamento grafico della ristampa** | — | ❌ **non esiste il concetto di ristampa**: vedi §2.C3 |
| **Produzione** (prestampa, tipografia, carta) | `rumblingstone-editoria` §5, parziale | 🟡 imposizione e indice analitico dichiarati aperti; CMYK/PDF-X rinuncia scritta (ADR-0020) |
| **Traduzione** (2 nomi) | `campaign/GLOSSARIO-E-LOCALIZZAZIONE.md` + ADR-0016 | ⏸️ **chiuso per decisione**, non per dimenticanza (ADR-0016: sorgente italiana, l'inglese è edizione derivata e non si costruisce adesso) |
| **Supervisione** · **Direttore responsabile** | — | ❌ manca il ruolo che dice **«questo esce»**: vedi §2.C3 |
| **Editore** (Erik Mona) — cioè chi risponde di cosa si pubblica | `ADR-0005` + `docs/guides/GUIDA-CONDIVISIONE-IP.md` §7 | ❌ **la checklist esiste e nessuna skill la carica**: vedi §2.C2 |
| **Product Identity · Open Content · OGL 1.0a** | nulla nei volumi | ❌ **il buco più netto**: vedi §2.C1 |
| **Ringraziamenti speciali** (i playtester) | `rumblingstone-playtest` (tre passate, questionari, alfa→beta→collaudato) | ✅ |
| **Technical Director** · **Senior Software Developer** | `rumblingstone-automation` + `rumblingstone-debugging` + ADR-0012 (37 tool a manifest, 70+ test in CI) | ✅ — è l'unica riga dove il repo **supera** il colophon: Paizo non ha una CI che rifiuta il volume |
| **CEO · VP Operations · Corporate Accountant · Director of Sales · Financial Analyst · Production Specialist** | — | ⛔ **fuori perimetro**, e va detto: sono un'**azienda**, non un libro. ADR-0005 esclude l'uso commerciale |
| **Campaign Coordinator** (organized play) | — | ⛔ fuori perimetro (non c'è una rete di tavoli da coordinare) |
| **Tipografia · distributore · dati legali di stampa** | — | ⛔ fuori finché non c'è una tiratura (ADR-0020) |

**Il conto**: 8 coperti bene · 2 chiusi per decisione · 5 fuori perimetro · **6
aperti**. I sei aperti non sono sei lavori: sono **tre**, perché si raggruppano.

---

## §2 · I tre buchi veri

### C1 · Il colophon stesso — i volumi escono anonimi, senza licenza e senza data

**Il difetto è letterale**: la pagina che il DM ha fotografato non ha
corrispettivo nei volumi di RumblingStone.

*Prova.* Le chiavi che un manifest di booklet può dichiarare sono diciassette:

```
$ python3 -c "import json;print(list(json.load(open('scripts/schemas/booklet_manifest.schema.json'))['properties']))"
['title','subtitle','brand','banner','meta','header','footer','player_footer',
 'front_matter','cover_image','cover_tag','intro_md','carta','capolettera','out','chapters']
```

Nessuna è `credits`, `license`, `edition`, `version` o `date`. E infatti
`grep -n "colophon\|crediti" scripts/export_booklet_typst.py` non trova niente, e
`grep -n "datetime\|versione" scripts/typst/tema-rumblingstone.typ` nemmeno: **i
PDF del repo non portano una data**. Oggi l'unica traccia di provenienza è una
riga di prosa scritta a mano dentro `meta`, manifest per manifest — nel booklet
del Palio è *«Campagna privata basata su Red Hand of Doom»*, e in altri non c'è.

**Perché conta più di quanto sembri.** Un volume senza colophon è un volume che
non sa dire da dove viene. Nel caso di questo repo dice tre cose diverse, tutte
utili al tavolo prima che a un avvocato:

1. **su cosa si basa** (Red Hand of Doom, SRD 3.5, OGL) — la riga che ADR-0005
   chiede e che oggi vive nelle guide, non nei file che escono;
2. **chi l'ha fatto e quando**: un PDF stampato tre mesi fa e uno di ieri oggi
   sono indistinguibili, e al tavolo qualcuno stampa la versione vecchia;
3. **cosa si può farne**: «materiale del DM, non da diffondere» è una frase che
   sta bene su una pagina, non in una conversazione ogni volta.

**Costo**: basso. È una chiave di manifest, una funzione nel tema, una pagina
generata. È la voce con il miglior rapporto effetto/costo dell'intero documento.

### C2 · La redazione come **processo** (e l'editore che firma)

Il colophon dedica alla redazione **diciassette nomi su cinquanta**: nell'editoria
vera è il mestiere più affollato del libro, e nel repo è quello meno formalizzato.

Attenzione a non confondere due cose che il repo tiene già giustamente separate:
`editorial-standards.md` è **la norma** (come si scrive CD, come si formatta un
read-aloud, quali termini sono banditi) e `validate_modules.py` ne rende
meccanica una parte in CI. Quello che manca non è la norma: è **il giro**.

*Prova per contrasto.* Per il collaudo al tavolo il repo ha un processo scritto e
completo — `rumblingstone-playtest` ha nove sezioni: le tre passate, l'audit
meccanico, il dry-run, le schede di feedback, il debrief, il ciclo
alfa→beta→collaudato, come si scrive una correzione. **Per la revisione del testo
non esiste niente di equivalente**: non c'è scritto quante passate fa un master
prima di essere consegnabile, cosa si guarda in ciascuna, chi decide che è
chiuso, e cosa succede quando si riapre.

Nello stesso buco cade **l'editore**: `docs/guides/GUIDA-CONDIVISIONE-IP.md` ha
al §7 una *«checklist prima di far uscire qualcosa dal repo»* — cioè esattamente
il gate — e **nessuna skill la carica**. `grep -rl "GUIDA-CONDIVISIONE-IP" skills/`
restituisce un solo file, e per un'altra ragione (l'art direction, sulle
immagini). Un agente che genera un handout e lo consegna non incontra mai quella
checklist. La verifica IP sul Palio (`…-VERIFICA-LEGALE-IP.md`, PR #47) dimostra
che il mestiere il repo lo sa fare: l'ha fatto **una volta, a mano, su un
arco**. Non è un ruolo, è un episodio.

### C3 · L'edizione come oggetto: versione, errata, ristampa

Il colophon italiano ha una riga che a prima vista è burocrazia e invece è la
domanda più profonda che la foto pone: **«Adattamento grafico ristampa»**. Quel
volume è alla sua *seconda* uscita. Qualcuno sa qual è la prima, cosa è cambiato,
e perché la nuova non è un file diverso ma **la stessa opera, versione due**.

Nel repo questo concetto non esiste. I master cambiano a ogni sessione (è
corretto: `state.md` e ADR-0007 governano il canone vivo), ma **il volume
generato non eredita nessuna identità**: niente numero di versione, niente data,
nessun registro di cosa è cambiato fra due generazioni dello stesso booklet.
Esiste un solo `ERRATA-ARC08-DESCRIZIONE-EPICA.md`, nato una volta e a mano.

Le conseguenze sono già visibili nell'archivio: `rumblingstone-editoria` §6 dice
di non impaginare *«un master che cambia ancora ogni sera»* — è la regola giusta,
ma è una **rinuncia** dove serviva un meccanismo. Con una versione stampata sul
frontespizio, impaginare un master vivo smette di essere pericoloso: diventa
«questa è la v3 del 26 agosto», e chi ha in mano la v2 lo sa.

Questo è anche il posto della **supervisione / direzione responsabile**: non
serve una skill che «controlla la qualità» (la fanno già playtest, module-standard
e la CI). Serve la riga che dice **chi firma un'edizione e con quale gesto** — e
in un repo il gesto esiste già ed è un tag git.

---

## §3 · Le skill: cosa aggiungere, cosa estendere, cosa non toccare

ADR-0008 avvisa sul costo della frammentazione, e le skill sono già sedici. Perciò
la proposta è **una skill nuova sola**, e il resto come estensione di quelle che
esistono.

### 3.1 · Una skill nuova: `rumblingstone-edizione`

Il mestiere dell'**editore** (nel senso del colophon: chi risponde di cosa esce) e
del **direttore responsabile** messi insieme, perché al di sotto di una casa
editrice vera sono la stessa persona. Copre C1 + C3 e la metà «editore» di C2:

- **il colophon**: cosa ci va (opera, base OGL/SRD, versione, data, autore,
  regime d'uso), come si genera, e la regola che nessun volume esce senza;
- **le dichiarazioni**: Product Identity e Open Content applicate a *questo*
  materiale, con la distinzione che ADR-0005 e la guida IP hanno già fatto fra i
  tre corpi (originale · derivato da RHoD · SRD);
- **il gate d'uscita**: la checklist del §7 della guida IP, portata dentro una
  skill così che un agente la incontri **prima** di consegnare, non dopo;
- **la versione e l'errata**: cosa è un'edizione, come si numera, cosa va in
  errata invece che in una modifica silenziosa del master, come si firma.

*Perché una skill e non un ADR*: ADR-0005 esiste già e va benissimo — il problema
non è che la decisione manchi, è che **nessun agente la carica al momento
giusto**. È letteralmente la regola 2 di ADR-0008 (copertura obbligatoria).

### 3.2 · Tre estensioni, senza skill nuove

| Dove | Cosa | Perché lì |
|---|---|---|
| `rumblingstone-editoria` | **§7 Prestampa e colophon**: la pagina dei crediti nel tema, le chiavi `credits`/`license`/`edition` nel manifest e nello schema, l'imposizione (R9), l'indice analitico (R8) | è già la skill del «come sta sulla pagina»; il colophon è una pagina |
| `rumblingstone-narrative-style` | **`references/passate-redazionali.md`**: le tre passate (struttura → voce → bozze), cosa si guarda in ciascuna, quando un master è *chiuso*, come si riapre | `editorial-standards.md` è già lì: la norma e il giro devono stare insieme, o si separano e divergono |
| `rumblingstone-plans` | una riga sul **volume come unità di lavoro**: quali capitoli, quante pagine, quale edizione — il «capo del progetto» del colophon | l'archivio piani è già l'unico posto dove si dichiara cosa si sta facendo |

### 3.3 · Cosa **non** aggiungere (rinunce, scritte perché non si riaprano)

1. **Nessuna skill di traduzione.** ADR-0016 ha deciso: sorgente italiana,
   inglese come edizione derivata da fare **quando** ci sarà materiale IP-pulito
   e finito. Il loc kit esiste già (`GLOSSARIO-E-LOCALIZZAZIONE.md`). L'unica cosa
   che vale la pena fare adesso è **agganciare la lista non-tradurre a un gate**,
   così il glossario resta vero mentre nessuno lo guarda — e costa venti righe.
2. **Nessuna skill «vendite / distribuzione / produzione industriale».** Sei righe
   del colophon sono l'organigramma di un'azienda da cinquanta persone. ADR-0005
   esclude l'uso commerciale: inseguirle sarebbe copiare la forma di Paizo senza
   il motivo di Paizo.
3. **Nessuna skill «revisore» separata dallo stile.** Sarebbe la sedicesima e
   mezza, e la norma redazionale vive già in `narrative-style`. Il processo va
   dove sta la norma.
4. **Non trasformare il colophon in trade dress altrui.** Vale qui la §5.2
   dell'audit di agosto: la pagina dei crediti si fa con la faccia del repo
   (avorio/seppia/rosso), non con la banda cremisi di nessuno.

### 3.4 · La combinazione che manca — l'**ordine dei mestieri**

Questa è la risposta alla parte della domanda che dice *«o nella combinazione di
skill»*, ed è meno ovvia delle singole voci.

Un colophon non elenca solo dei mestieri: ne implica **la sequenza**. Autori →
redazione → capo progetto → arte e cartografia → grafica → prestampa → produzione
→ e in testa a tutto l'editore che dice quando è finito. Nel repo i mestieri ci
sono quasi tutti, **e nessun documento dice in che ordine si chiamano** per
produrre un volume. Ogni skill sa fare la sua parte e sa dove finisce il proprio
confine (ADR-0008 lo impone), ma la **catena** vive nella testa di chi la esegue.

La forma che il repo userebbe se lo decidesse è quella che ha già scelto per tutto
il resto: **un sottocomando dell'orchestratore** (ADR-0002). `dm.py volume`, che
non impagina niente di nuovo ma *chiama in ordine* ciò che esiste — validatori,
apparato d'uso (ADR-0018), gate IP, generazione, colophon, compilazione — e si
ferma alla prima cosa che manca. Vale la pena notare che l'audit di agosto aveva
già trovato la stessa crepa da un'altra direzione: *«`dm.py stampa` come
sottocomando: oggi la catena di stampa si invoca solo a mano, ed è l'unico tool
del toolkit fuori dall'orchestratore»*. Sono la stessa mancanza vista due volte.

---

## §4 · Server MCP: quale serve davvero (e perché quasi nessuno)

Prima la premessa che decide tutto il paragrafo: **questo repo è ostile per
costruzione agli MCP di rete**. La catena è offline, gli script sono stdlib-only,
il renderer è deterministico byte-identico, i pacchetti Typst non si scaricano
(§5.3 dell'audit), i pesi si vendorizzano (ADR-0010, ADR-0019). Un server che
risponde diversamente domani è esattamente ciò che quelle decisioni escludono.
Quindi un MCP paga solo se è **locale**, oppure **di sola consultazione** e fuori
dalla catena di build.

Con quel filtro, ne restano tre — e il primo è già mezzo scritto.

### MCP-1 · Il server che manca è **il vostro** ⭐

`ADR-0012` prometteva: *«un orchestratore/agente esterno può scoprire e invocare i
tool leggendo `docs/tools/registry.json` / `mcp-tools.json` senza leggere il
codice»*. Il file **esiste ed è completo**:

```
$ python3 -c "import json;d=json.load(open('docs/tools/mcp-tools.json'));print(len(d['tools']))"
44
```

— **44 tool** (erano 37 quando ADR-0012 è stato scritto: il descrittore è cresciuto
da solo, perché è generato), ognuno con `name`, `description`, `invocation` e un `inputSchema`
JSON-Schema già valido. È il **descrittore di un server MCP senza il server**.
Mancano circa centocinquanta righe di JSON-RPC su stdio, zero dipendenze nuove,
che leggano quel file e girino le chiamate agli script.

Il guadagno non è teorico: oggi un agente che vuole rendere una mappa o validare
un booklet deve conoscere i percorsi, i flag e l'ordine. Con il server conosce
solo i nomi, e **il manifest è già sotto gate CI** (`tools_manifest --check`
bloccante), quindi la descrizione non può mentire. È l'unico MCP che questo repo
dovrebbe scrivere, ed è l'unico che nessuno può dargli.

### MCP-2 · **Context7** (o equivalente) per la documentazione Typst 🟢

Sola consultazione, fuori dalla build, e c'è una prova che serve: il §7
dell'audit di agosto è un'**errata di tre errori Typst** contenuti in una ricerca
precedente — `dropcap` invece di `droplet`, `center([...])` che non esiste, e
`locate(loc => …)` che è la sintassi pre-0.11. Tre errori su tre generati da
memoria invece che da documentazione, in un motore che cambia in fretta. È
esattamente la classe di errore che un server di documentazione azzera.

### MCP-3 · **ComfyUI locale** come MCP 🟡 (gated sulla GPU del DM)

`scripts/comfyui-local/` esiste, ADR-0015 standardizza i prompt, ADR-0019 tratta
la licenza dei pesi, e il divario **[1]** (zero raster) è dichiarato il più
visibile di tutti. ComfyUI ha un'API HTTP locale: un MCP sottile davanti a quella
API farebbe generare all'agente le illustrazioni **fissando seed e parametri**,
cioè rendendo la serie riproducibile invece che irripetibile — che è la richiesta
che `rumblingstone-art-direction` fa già a parole. Resta gated dove era: la GPU.

### Quelli che **non** servono, e la ragione

| Categoria | Verdetto |
|---|---|
| MCP di **ricerca web** (Tavily, Firecrawl e simili) | 🟡 utili al singolo agente, **inutili al repo**: nessuna decisione editoriale dipende da una fetch. E la ricerca di agosto ha già misurato che le fonti che servivano davvero erano bloccate a monte |
| MCP di **font** | 🟡 la scelta è chiusa (Garamond/Cinzel/Inconsolata, vendorizzati). Quello che serve non è scoprire font: è **verificare che la licenza sia OFL e che il file stia nel repo** — e questo è un controllo, non un server |
| MCP di **immagini stock** | ❌ ADR-0005: materiale di terzi dentro il repo è il problema che si sta evitando, non la soluzione |
| MCP di **diagrammi / canvas** | ❌ le mappe hanno un contratto JSON e un renderer deterministico. Un canvas esterno lo romperebbe |
| MCP che **impaginano o compilano** | ❌ è la build. La build sta in CI, a versione fissata, offline (D4 dell'audit è stato chiuso proprio per questo) |

---

## §5 · I tool (non MCP) che alzano davvero la resa

Qui il rapporto effetto/costo è migliore che negli MCP, e tre di questi chiudono
voci che il repo ha già lasciato aperte **come decisioni**, non come dimenticanze.

| | Tool | Chiude | Licenza | Nota |
|---|---|---|---|---|
| **T1** | **`pdfcpu`** — `booklet`/`nup` su un PDF già fatto | **R9 imposizione** (aperta dall'audit: *«richiede uno strumento che manipoli un PDF già fatto, cioè una dipendenza nuova da decidere»*) | **Apache-2.0**, binario Go singolo, offline | è *esattamente* la dipendenza descritta, e ha la funzione già fatta. Stesso trattamento di Typst: versione fissata, mai `latest` |
| **T2** | **`in-dexter`** (pacchetto Typst) | **R8 indice analitico** | da verificare prima di adottare | ⚠️ **si scarica dalla rete**: ricade nella §5.3. Ma vedi la nota qui sotto — è la stessa decisione del capolettera |
| **T3** | **veraPDF** | **R11 tag PDF / accessibilità**, oggi in ripiego `--no-pdf-tags` per un bug di Typst | open source, guidato da Open Preservation Foundation + PDF Association | dà la riga di CI che **fa togliere il ripiego da solo** quando Typst lo risolve |
| **T4** | Un **`validate_lingua.py`** stdlib | metà di C2: refusi meccanici (perché/perchè, virgolette dritte, spazi doppi, apostrofi, d eufonica) | — | ⭐ la via del repo: gratis, offline, in CI, zero dipendenze |
| **T5** | **LanguageTool** self-hosted, se T4 non basta | l'altra metà di C2 | **LGPL-2.1**, API REST locale | ⚠️ **richiede una JVM**: è una dipendenza pesante per un toolkit stdlib-only. Da prendere solo se T4 dimostra di non bastare, mai prima |
| **T6** | Una **misura di caratteri per riga** sul PDF compilato | il 🟡 lasciato aperto in §2.3 dell'audit (*«la misura giusta non è il corpo, sono i caratteri per riga»*) | — | venti righe; toglie l'unico parametro tipografico ancora deciso a occhio |
| **T7** | Un **simulatore di daltonismo** sul PNG delle mappe | **B4**, l'accessibilità già tracciata (le legende usano rosso *e* verde) | — | riguarda una persona su dodici, e oggi si verifica solo guardando |

> ⚠️ **Le licenze di T1, T3 e T5 sono state verificate online il 2026-08-26**;
> T2 no. Prima di adottare qualsiasi voce, la licenza si riverifica alla fonte e si
> scrive nel repo: è la soglia che `RICERCA-TOOL-ESTERNI-DM` ha già fissato.

### La scoperta laterale che vale il documento

**T2 e il capolettera annegato sono la stessa decisione.** L'audit di agosto le ha
lasciate aperte come due code separate — *«capolettera annegato → vendoring dei
pacchetti Typst»* e *«indice analitico → una convenzione di marcatura nei
master»* — ma il pacchetto `droplet` (capolettera) e `in-dexter` (indice) si
scaricano entrambi dalla rete e ricadono entrambi sotto §5.3. Prese insieme,
**delle quattro code editoriali rimaste, due si chiudono con un solo sì o un solo
no**: *si vendorizzano i pacchetti Typst nella cache locale del repo, con la loro
licenza, come già si fa per le skill di terzi (ADR-0010)?* È una domanda sola, con
un precedente già scritto, e vale due rifiniture da manuale.

---

## §6 · Sequenza proposta

Nessun lotto è aperto: questa è una proposta d'ordine, col costo onesto.

| Lotto | Contenuto | Costo | Gate |
|---|---|---|---|
| **P1** | **Colophon** (C1): chiavi `credits`/`license`/`edition`/`version` nello schema, pagina generata nel tema, data e versione sul frontespizio | mezza giornata | nessuno |
| **P2** | Skill **`rumblingstone-edizione`** (C1+C3+gate IP) + la checklist del §7 della guida IP portata dentro | mezza giornata | ⚠️ nuova skill → ADR-0008 chiede che sia motivata: la motivazione è qui |
| **P3** | **`references/passate-redazionali.md`** + **T4 `validate_lingua.py`** in CI | mezza giornata | nessuno |
| **P4** | **Decisione sul vendoring dei pacchetti Typst** → sblocca capolettera annegato **e** T2 indice analitico | la decisione è gratis, l'esecuzione ~1 giornata | ⚠️ **decisione DM** |
| **P5** | **T1 `pdfcpu`** per l'imposizione (R9), con ADR sulla dipendenza | 1 giornata | ⚠️ ADR (seconda dipendenza da binario esterno dopo Typst — il precedente ora esiste) |
| **P6** | **MCP-1**: il server MCP sui 44 tool già descritti in `mcp-tools.json` | ~1 giornata | nessuno tecnico; è una scelta di direzione |
| **P7** | **T3 veraPDF** in CI + **T6** caratteri per riga + **T7** daltonismo | 1 giornata | dopo P1 |
| **P8** | `dm.py volume` — la catena dei mestieri in ordine (§3.4), che assorbe anche `dm.py stampa` | 1-2 giornate | dopo P1-P3 |

Fuori sequenza perché gated altrove, come già dichiarato: raster e MCP-3
(GPU del DM), edizione inglese (ADR-0016), CMYK/PDF-X e dati di stampa
(ADR-0020, il giorno di una tiratura vera).

---

## §7 · Se si fa una cosa sola

**P1.** Ventuno ruoli nel colophon, e il divario più grande è che i volumi del
repo **il colophon non ce l'hanno**. Non è la voce più difficile: è quella che ha
prodotto la domanda. Un PDF che porta il proprio nome, la propria data, la propria
versione e la riga che dice su cosa si basa smette di essere un file generato e
diventa **un'edizione** — ed è da lì che C3, e mezzo di questo documento,
diventano possibili.

---

## §8 · Addendum (2026-08-27) — la seconda standalone, e gli undici punti che aggiunge

**Perché questo addendum.** Dopo il merge della PR #114 il DM ha segnalato una
**seconda standalone** — `10-stand-alone/L'abbazia Della Rotta Sicura/` — scritta
*«emulando lo stile dei migliori AP Paizo per Pathfinder 1e»*, con un indice
maestro e tre appendici, e ha chiesto di verificare cosa contenga che questo
documento non aveva previsto. La risposta è: **parecchio**, e in due direzioni
opposte — un apparato editoriale più ricco di quello che le skill sanno chiedere,
su un supporto che sta **fuori da ogni catena del repo**.

Quattro file, tutti HTML scritti a mano (CSS e tavole SVG in linea), ~2.750 righe:
`indice_maestro.html`, `abbazia_rotta_sicura.html`, `appendice_corsari_borgo.html`,
`appendice_b_oppressione.html`.

### §8.1 · Gli undici punti nuovi

Ognuno verificato assente dalle sedici skill (`grep -ril` su `skills/`), non
supposto.

| | Punto | Modello nell'Abbazia | Dove va |
|---|---|---|---|
| **P9** | **Riscalatura a tre assi** — per livello del party, per numero di giocatori, per durata disponibile, ognuna con la colonna **«cosa si perde davvero»** | tabella dell'indice maestro: 5 fasce di livello × 12 righe, 4 formati di durata | sezione obbligatoria in `module-standard`; estende `playtest` §2.6, che oggi copre **solo** il numero di giocatori |
| **P10** | **Avvertenza di contenuto e consenso del tavolo** — la riga da dire *prima* di cominciare, e la sostituzione alternativa già pronta | Fase 1: *«c'è un culto che uccide ragazzi; niente sarà mostrato in scena»* + le vittime sostituibili con marinai catturati | `module-standard` (apparato d'uso, ADR-0018) |
| **P11** | **Igiene di licenza per documento** — tabella *elemento · stato · nota* compilata **in stesura**, non a posteriori | separa divinità inventate («Il Nocchiero») dai nomi FR non-SRD, e toponimi inventati da luoghi reali | confluisce in **P2**: è il gate IP di §2.C2 già dimostrato funzionante |
| **P12** | **ADR di modulo** — decisioni di progettazione locali (ADR-01…05), distinte da quelle di repo | «il nemico non è uno, sono tre»; «le vittime bambine restano fuori scena» | convenzione nuova: quando una decisione è di modulo e quando è di `plans/adr/` |
| **P13** | **Indirizzamento delle aree fra documenti** — prefisso di livello + indice maestro trasversale | il dry-run ha trovato **«16, 17, 18 usati tre volte su tre documenti»** | ⭐ estende `validate_modules.py`: è un difetto che una macchina trova gratis |
| **P14** | **Il limite dichiarato del dry-run** — *«cosa il dry-run non ha potuto verificare»* | *«non dice se l'avventura è divertente, se il ritmo regge… quello lo dice solo un tavolo»* | una riga in `playtest`: le sette passate ci sono, la dichiarazione del limite no |
| **P15** | **Cancelli d'uscita a tempo per atto** — con il rimedio scritto | *«Atto I, 60-75 min. Se a 60 minuti manca uno dei due segnali, Berto Cassola arriva e lo dice in faccia»* | `module-standard`: regia del ritmo |
| **P16** | **Tavole non zenitali** — veduta prospettica e profilo laterale con quote, distanze e **tempi**, più ogni vista di supporto che serva a spiegare | Tavola I-a (dal mare), Tavola I-b (profilo laterale: quote, distanze, tempi) | `mapmaking`: oggi è tutto dall'alto. ✅ **Confermato dal DM il 2026-09-02**: sì alle verticali, e sì alle viste in più «quando serve a spiegare meglio» |
| **P17** | ⚠️ **Il supporto: l'Abbazia è fuori da ogni catena** | nessun master markdown (contro ADR-0003), nessun manifest, né HTML né Typst, e **nessun gate**: la CI copre `STANDALONE-*`, e `10-stand-alone/` non corrisponde a niente | **il più urgente dei nuovi** |
| **P18** | ⚠️ **`LICENSE` è GPL-3.0 su un'opera testuale** | il rilievo lo solleva il documento stesso: *«GPL-3.0 su un'opera testuale resta l'errore da correggere, qui come nel repo principale»* — verificato: `head -3 LICENSE` | **decisione**, non lavoro |
| **P20** | ⭐ **Corpo + appendici**: il modulo si divide in ciò che si *gioca* (atti, scene, incontri in ordine) e ciò che si *consulta* (bestiario, gazetteer del luogo e della sua storia, cast dei PNG, riepilogo degli scontri) | Appendice A (corsari, borgo, livello 0) · Appendice B (oppressione, storia, cronologia, bestiario) · Appendici I/II/III (bestiario · incontri e prove · i sei misteri) | `module-standard`: le 16 sezioni obbligatorie sono un **elenco lineare**, non un'architettura. Verificato: `grep -ril "appendice" skills/` non trova niente, e nessun master `ARC*-DEF-*` né il Drappo la usano |
| **P19** | **Tabelle vive del borgo** — dicerie `1d8` di cui **due deliberatamente false**, e reazione del capo-fazione a `1d20` + modificatori | *«Dicerie all'osteria (1d8 — due sono false, deliberatamente)»* | `narrative-style` / `indagine`: la diceria falsa è un nodo d'indizio a costo zero |

### §8.1-bis · Due punti dal tavolo (2026-09-02) — e un ADR che si riapre da solo

Rilievo del DM, riportato dai giocatori: *«incoerenza e prosa inglese tradotta
male, anche negli echi»*. Non è un'impressione nuova — è **la stessa** che aveva
generato ADR-0016 — e il repo ci aveva messo una condizione esplicita:

> **Banco di prova**: i prossimi handout. Se i giocatori diranno ancora che sembra
> tradotto, il problema non è la lingua e non è la pipeline — e **questa ADR va
> riaperta**. — ADR-0016, «Il vero rimedio al rilievo dei giocatori»

⚠️ **La condizione è scattata.** Va detto senza girarci intorno.

**Cosa esiste già**: la norma, e non è poca — `italiano-nativo.md` (274 righe: §1
i dieci calchi, §9 i tic dell'IA con l'antitesi «non X: è Y» in testa),
`read-aloud-adulti.md`, `campaign-coherence.md`, il glossario e la lista DNT.
**Cosa non esiste**: **nessun gate**. `grep -ril "traduttese\|calco" scripts/` non
trova niente. La norma c'è, e nessuno la applica: è esattamente la forma del
divario **C2** (la redazione come processo), vista da un'altra angolazione.

| | Punto | Perché è fattibile a macchina | Dove |
|---|---|---|---|
| **P21** | **Validatore di prosa**: i calchi con firma inequivocabile (*realizzare* per *to realize*, *eventualmente* per *eventually*, *assumere* per *to assume*, il possessivo su parti del corpo, il progressivo «stai camminando», la nominalizzazione «la sensazione di») **e i tic dell'IA a densità** — l'antitesi «non X: è Y» **max 1 per documento**, le maiuscole di portento max 1, i trattini lunghi | metà di `italiano-nativo.md` §1 e §9.2 sono **regole di conteggio**: «massimo uno per documento» è la cosa che una macchina fa meglio di un revisore stanco, e che un revisore non fa mai perché dovrebbe contare | nuovo `scripts/validate_prosa.py`, accanto a `validate_lingua.py` |
| **P22** | **Coerenza d'ambientazione**, la parte meccanizzabile: nomi canonici, glossario e **lista non-tradurre** applicati a **tutto** il contenuto — non solo ai cinque master `ARC*-DEF-*` che `validate_modules` già copre. **Compresi gli echi**, che il rilievo nomina esplicitamente | il lessico è verificabile; il *senso* no. Va dichiarato: questo gate trova un nome sbagliato, non una contraddizione di trama | estensione di `validate_modules.py` + `GLOSSARIO-E-LOCALIZZAZIONE.md` come fonte |
| **P23** | ⭐ **Il rimando d'area in forma parentetica**: *«la chiave è in sacrestia (6)»*, *«la botola in cappella (9)»* — 63 casi nell'Abbazia dopo la chiusura dei 55 `area N`. Stessa ambiguità, forma diversa, e **il gate non li vede** | ⚠️ **fattibile solo a metà, e questa è la voce onesta della tabella**: un `(8)` può essere un'area, un risultato di dado, una CD o una nota. La macchina può *elencarli* con il contesto e il codice probabile; **non può decidere**. Il gate propone, il DM conferma — come per le passate redazionali | estensione di `check_aree_ambigue` in `validate_standalone.py`, in modalità elenco (non bloccante e mai automatica) |

⚠️ **Quello che questi due punti NON possono fare**, e va scritto perché non si
prendano per più di quello che sono: un validatore trova *«realizzi che»*, non
trova una scena che suona tradotta pur essendo tutta in italiano corretto. Quella
resta una **passata redazionale umana** — cioè il lotto E. I due gate tolgono il
rumore meccanico *perché la passata umana veda il resto*.

### §8.2 · Cosa NON è nuovo (per non contarlo due volte)

- **Indice e Quick-Reference**: `module-standard` li chiede già ai punti 2 e 4.
  Il pezzo nuovo è solo l'indirizzamento **fra documenti** (P13).
- **Audit meccanico a tavolino**: `playtest` §2 ha già sette passate. Il pezzo
  nuovo è la **dichiarazione del limite** (P14).
- **Apparato d'uso e prop**: ADR-0018 li impone già.
- **Bestiario SRD-only**: già la regola del repo (ADR-0005).

### §8.3 · La lettura d'insieme

L'Abbazia è **la prova che l'apparato serve**: è stata scritta con riscalatura,
consenso, igiene di licenza e ADR locali *senza che nessuna skill glieli
chiedesse*, e il risultato è il modulo più completo del repo. Ma è anche la prova
del contrario: essendo HTML a mano, **non è impaginabile, non è validabile e non
è un'edizione** — non ha colophon, non ha versione, non ha data. Cioè inciampa
esattamente in **C1**, il buco che questo documento aveva già isolato.

Il seguito operativo di tutti e diciannove i punti è
[`PIANO-CHIUSURA-CATENA-EDITORIALE`](PIANO-CHIUSURA-CATENA-EDITORIALE.md).
