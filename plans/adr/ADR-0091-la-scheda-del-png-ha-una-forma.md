# ADR-0091 — La scheda di un PNG o di un villain ha una forma sola

**Stato**: accettata *(il DM, 2026-10-15: «sì ad entrambi; dopo controlla che la parte di tattiche, se prevista, ci sia»: conversione di tutte le schede; poi: «no, i dossier di gruppo come sono adesso»)*
**Data**: 2026-10-15
**Decisione-fonte**: domanda del DM del 2026-10-15, nel progetto sulle PR ferme: *«perché tutte le schede dei PNG e villain sono tutte diverse, non si possono uniformare nello stile e contenuti come ad esempio quelle presenti in RHoD o Rise of the Runelords PF1e?»*
**Rapporti**: completa [ADR-0021](ADR-0021-statblocchi-machine-readable.md) (i numeri sono un blocco), che dice *dove* stanno i numeri e non come si legge il resto; rispetta L-D3 di `PIANO-REVISIONE-LIBRERIA-MOSTRI-PNG-VILLAIN` (gli statblocchi d'arco restano nel loro arco)

## Contesto

`Bestiario/png/` e `Bestiario/villain/` contengono 113 file, misurati il
2026-10-15. Vanno da 10 righe (Avatar di Tiamat, Tyrgarun) a 280 (Tempestas).
Ci sono almeno cinque forme diverse, e ognuna corrisponde a un momento del
repo:

| Forma | Da dove viene | Esempio |
|---|---|---|
| statblocco del catalogo Armate, un paragrafo con tutti i numeri | maggio 2026, `Armate-UNITA-NUOVE`, poi lotto L0 | `villain/balvar-fuocospento-cr13.md` |
| dossier a campi AGENTS.md, 11 righe senza sezioni | i 30 file della vecchia cartella `PNG/` | `png/Dana_Forgiapietra.md` |
| dossier lungo a sezioni MAIUSCOLE, statistiche in tabella | le generazioni di luglio | `png/Lorana/Lorana/Lorana.md`, `villain/Sonjak/Sonjak.md` |
| dossier a sezioni numerate | canonizzazioni del DM di fine luglio | `villain/Mira_Serani/Mira_Serani.md` |
| voce `POINTER` senza numeri | i 47 + 20 PNG d'arco raccolti il 2026-09-17 | `png/grandmaster-rihan-cr14.md` |

Nessuna di queste forme è sbagliata, e il repo ha già uno standard: il
`README` del Bestiario fissa le sei intestazioni, ADR-0021 il blocco
` ```statblocco `, il modello `png-dossier-template.md` i campi. Ma lo standard
copre i **dati** e non la **lettura**. Tre cose lo dicono in numeri:

- `validate_bestiario.py` guarda di un dossier solo il titolo H1. Una scheda di
  11 righe e una di 280 passano allo stesso modo;
- la direzione del rimando non è fissata. La guida lo scrive (`GUIDA-BESTIARIO`
  §6-bis: «certi dossier puntano al proprio statblocco e certi statblocchi al
  proprio dossier»): Lorana tiene i numeri nel dossier e la sua `-cr7.md` è un
  rimando, Ushgar fa il contrario;
- le **tattiche**, che in *Red Hand of Doom* e in ogni AP Paizo sono la parte
  per cui una scheda esiste, compaiono in 21 file su 113, ognuno con un titolo
  suo.

I due modelli che il DM cita hanno lo stesso scheletro, e si può prendere senza
copiare una riga del loro testo. *Red Hand of Doom* (2006) usa il blocco 3.5
della serie *Monster Manual V*: difesa, attacco, statistiche, poi le tattiche
nell'incontro. Le AP di Pathfinder 1e lo dividono in titoletti fissi
(DIFESA, ATTACCO, TATTICHE, STATISTICHE, CAPACITÀ SPECIALI) e nella galleria dei
PNG aggiungono sempre le stesse voci di racconto: chi è, com'è, cosa vuole,
che ruolo ha nella campagna.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Due file con una forma fissa ciascuno** (statistiche e persona), sezioni e ordine dichiarati, una misura che li conta | non tocca il catalogo, i nomi `-crN.md`, i 56 rimandi né i `componenti.py --includi`; si converte un file alla volta | resta la coppia di file per i PNG maggiori, che *Red Hand of Doom* non ha |
| Un file solo per PNG, statistiche e racconto insieme, come l'appendice di RHoD | una sola cosa da aprire al tavolo | cambia `build_monster_catalog`, `validate_bestiario`, `suggest_encounter` e gli `id` del catalogo; tocca 56 rimandi in una volta |
| Generare la parte leggibile dal blocco ` ```statblocco ` | i numeri non si scrivono due volte | il blocco non ha talenti, abilità, equipaggiamento e tattiche se non come `voci`; la prosa porta le note del DM e i marchi `[INFERRED]`, che un generatore cancellerebbe |
| Lasciare tutto com'è | nessun costo | la domanda del DM resta senza risposta, e ogni scheda nuova sceglie la forma dell'ultima che l'agente ha letto |

## Decisione

**Ogni PNG o villain nominato ha al più due file, ciascuno con una forma
fissa: i numeri in `nome-crN.md`, la persona in `Nome.md`. Il rimando va
sempre dal dossier allo statblocco.**

### 1. Lo statblocco (`nome-crN.md`)

L'ordine è quello delle AP PF1e, coi nomi della 3.5 (BAB e Lotta, niente
BMC/DMC):

````markdown
# Nome — epiteto (razza, classi) [ACCEPTED — DM-canon] | [INFERRED — …]
**Faction**: … | **Role**: … | **Environment**: … | **CR**: N | **Source**: … | **Status**: …

```statblocco
(ADR-0021, invariato)
```

**Iniziativa** … · **Sensi** … (facoltativa, come la prima riga delle AP)
**Difesa** CA …, contatto …, colto alla sprovvista … · pf … (DV …) · TS Temp …, Rifl …, Vol … · RD, immunità, resistenze
**Attacco** Vel … · Mischia … · Distanza … · attacchi speciali · incantesimi (livello e CD, mai il testo)
**Statistiche** For … Des … Cos … Int … Sag … Car … · BAB …; Lotta … · Talenti … · Abilità … · Linguaggi … · Qualità speciali … · Equipaggiamento …
**Capacità speciali** una voce per capacità, col tipo (Str, Sop, Mag)
**Tattiche** *Prima del combattimento* … · *Durante il combattimento* … · *Morale* … (la soglia di pf o la condizione in cui smette)

Benchmark, combinazioni ed EL (facoltativi)
Notes: dove si usa nella campagna, e il rimando al dossier
Boost log: …
````

Le cinque etichette in grassetto sono obbligatorie e in quest'ordine. Dove
manca il contenuto si scrive l'etichetta con `[DA SCRIVERE — …]`, oppure con il
rimando al master che lo tiene (le tattiche di Balvar stanno nella Scena 7 di
`ARC07-DEF-4`).

### 2. Il dossier (`Nome.md`)

In testa i campi di AGENTS.md (Role, Status, Location, Motivation, CR con
razza e classe, Key stats, Token), con `[RIMANDO]` e `**Key stats**: →
\`nome-crN.md\`` quando i numeri stanno nello statblocco. Poi queste sezioni
`##`, in quest'ordine:

| Sezione | Obbligo | Cosa ci va |
|---|---|---|
| `## In breve` | facoltativa | due o tre righe: chi è per il tavolo, in che archi |
| `## Chi è` | **sì** | la storia, fino a oggi |
| `## Aspetto e voce` | **sì** | com'è, come si muove, come parla |
| `## Cosa vuole` | **sì** | il *Want* che non riguarda i PG (domanda 5 della self-check di `narrative-style`), e cosa teme |
| `## Nella campagna` | **sì** | dove e quando compare, cosa offre, le risorse che porta |
| `## Con i PG` | facoltativa | una voce per PG |
| `## Rapporti` | facoltativa | con chi sta, contro chi |
| `## In combattimento` | **sì** se ha uno statblocco | come combatte, in prosa; i numeri restano nello statblocco |
| `## Esiti possibili` | **sì** | i rami aperti, legati ai dadi e alle scelte (D13) |
| `## Al tavolo` | facoltativa | battute, cose da fare e da non fare |
| `## Segreti del DM` | facoltativa | quello che i giocatori non devono leggere |
| `## Fonti e canone` | **sì** | decisioni del DM con la data, l'adattamento da RHoD, i file dove compare |

Il **dossier breve** resta: per una comparsa nominata bastano i campi, senza
sezioni (oggi 16 file). Se però un dossier ha anche una sola sezione `##`, le
ha tutte quelle obbligatorie.

### 3. Cosa resta fuori

- I **dossier di gruppo** (il Consiglio di Rethmar, i Profughi del Guado, il
  Secondo Anello, Witchwood e Tiri Kitor, la Zhentarim di Dauth) non sono un
  PNG e restano come sono (decisione del DM del 2026-10-15). `--forma` non li
  conta.
- I `POINTER` verso un master d'arco restano come sono (L-D3).
- `Bestiario/mostri/` non cambia: le creature generiche hanno già la forma del
  catalogo, e questa decisione riguarda chi ha un nome.

### 4. La conversione non inventa

Riordinare una scheda sposta testo, non lo scrive. Una sezione obbligatoria
senza fonte nel repo si apre con `[DA SCRIVERE — …]` e la riempie il DM, o un
lotto che carica `rumblingstone-narrative-style`. Un numero che non torna si
segnala con `[INFERRED — needs DM confirmation]` accanto, e resta quello che
era.

### 4-bis. Quando le versioni non concordano (DM, 2026-10-16)

Il §4 vale per il riordino. Dopo, il DM ha chiesto di correggere: *«usa ed
adatta la versione più terrificante delle stats, in linea con il PNG e il
villain […] lascia sempre quelle più potenti in ogni caso e fixa tutti i
problemi»*. Per le schede nominate valgono quindi quattro regole, che per
questo lotto allargano il §2 di ADR-0065 (lì si corregge un numero solo quando
è l'unico che non torna).

1. **Vince la versione più forte che resta il personaggio.** Si confronta la
   build intera, non il massimo campo per campo. Una versione dichiarata MASTER,
   ERRATA o decisione del DM batte una non dichiarata. Si scarta la versione
   più forte solo quando rompe il ruolo: un luogotenente non supera il suo
   comandante, e un mostro generato che non è la creatura dell'arco resta fuori.
2. **Un conto sbagliato si corregge senza togliere potere.** Se il valore giusto
   è più basso, lo si riporta in alto con un mezzo legale: una caratteristica,
   un talento o un oggetto coerente col personaggio, marcato `[INFERRED]`.
   Quando non c'è un mezzo legale, si accetta il valore più basso e la scheda
   ne scrive il motivo.
3. **Il materiale non SRD si segnala.** Accanto alla classe si scrive
   `[Private source — <libro>]`. Un prerequisito mancato resta, con una nota ⚠.
   Si scrive anche, in una riga, se un archetipo PF1e del PRD fa la stessa cosa
   o la stravolge.
4. **Il vecchio non si cancella.** I numeri superati vanno in un blocco
   `<!-- storico -->` della scheda, e il cambio di GS in `Boost log:`. Se il GS
   cambia, cambia anche il nome del file.

### 5. La misura

`python3 scripts/validate_bestiario.py --forma` conta, per ogni dossier e
statblocco nominato, le sezioni obbligatorie che mancano e quelle fuori ordine.
Stampa il conto e non blocca. Diventa un cancello quando il DM chiude la
conversione di massa.

## Conseguenze

- Tre schede di prova nella stessa PR: **Lorana** (alleata: i numeri passano
  dal dossier a `capitana-lorana-cr7.md`, che smette di essere un rimando),
  **Ushgar** (villain: dossier e statblocco riordinati, nessun numero toccato),
  **Balvar** (statblocco senza dossier). Sono la prova che la forma regge su
  tre casi diversi.
- Col via del DM, la conversione ha riordinato tutte le altre schede nella
  stessa PR, spostando il testo senza riscriverlo: 37 statblocchi su 37 e
  24 dossier su 24 nella forma. I conti che non tornano sono elencati nella
  PR e non corretti.
- Le sezioni vuote diventano visibili. Lorana non ha tattiche né esiti scritti
  da nessuna parte: oggi non si vede, dopo sì. È il costo voluto.
- Si paga un secondo file da aprire per i PNG maggiori, che RHoD non ha.

**Da rivedere se**: la conversione dei primi dieci dossier lascia vuota la
stessa sezione obbligatoria in più della metà dei casi (vuol dire che non era
obbligatoria), oppure il blocco ` ```statblocco ` arriva a portare talenti,
abilità ed equipaggiamento come campi propri, e allora la parte leggibile dello
statblocco si può generare (terza alternativa).
