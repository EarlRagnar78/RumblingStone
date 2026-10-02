# ADR-0070 — L'apparato di lavoro non va in stampa, e ogni pagina si stampa una volta

- **Stato**: accettata
- **Data**: 2026-09-25
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: richiesta del DM del 2026-09-25, sulla #175: *«l'apparato
  di lavoro esce dai volumi stampati, e ogni pagina si stampa una volta sola»*,
  con le quattro classi e la misura sul PDF proposte da lui; poi, a lavoro
  avviato: *«se l'esportatore prende come valori DEF-2 DEF-3 ecc usa quello
  […] è più coerente e facile da gestire se si usa quello standard invece di
  introdurre uno nuovo»*
- **Rapporti**: estende [ADR-0069](ADR-0069-la-storia-delle-scelte-resta-nel-sorgente.md)
  (la storia delle scelte) dalla storia a tutto l'apparato di lavoro; vale per
  le due catene di [ADR-0013](ADR-0013-standard-generazione-booklet-sessioni.md)
  e [ADR-0020](ADR-0020-edizione-da-stampa-su-un-secondo-binario.md); il corredo
  della serata è la norma di `rumblingstone-automation`

## Contesto

ADR-0069 aveva tolto dalla stampa la storia delle scelte, e il suo test la cerca
nei sorgenti con una regex di date e frasi fisse. Nei PDF restava tutto il
resto del lavoro sul repo. Misurato il 2026-09-25 sulla serata di ARC-07, dopo
la #174, contando le occorrenze nel testo estratto dal PDF: **150** nel booklet
del DM, **87** nel volume del −1000. Erano intestazioni come «⭐ MASTER
DEFINITIVO … Sostituisce e fonde … FILE-FONTE ASSORBITI», nomi di file `.md`,
«master #1..#5», «Correzione canone (DM)», «MAI 5e / CD non DC», i percorsi
`_ARCHIVIO/` e `state.md`, e in fondo a ogni mappa la didascalia «fonte: X.md ·
SVG generato da scripts/render_map_svg.py».

E la serata stampava due volte le stesse pagine. Il booklet conteneva `DEF-4`
per intero, e il volume del −1000 lo ristampava; i tredici fogli ✉ stavano nel
booklet, nel volume dei giocatori e, due di loro, anche nel −1000.

## La decisione

**L'apparato di lavoro ha quattro classi, e ognuna ha il suo destino.**

| Classe | Che cos'è | In stampa | Come |
|---|---|---|---|
| **A** · metadati del repo | provenienza, fusione, file-fonte, stato di consolidamento, «MASTER DEFINITIVO», «standard AP», promemoria di sistema, nomi di file e percorsi | mai | un blocco `<!-- apparato -->` … `<!-- /apparato -->` scritto a mano, uno per l'intestazione di ogni master, o gli stessi marcatori dentro una riga. Tre forme fisse se ne vanno da sole: la riga `**Faction**: … **Source**: …` del Bestiario, la parentesi che contiene solo un percorso (`` (`X.md` §5) ``), la citazione `*(Fonte: …)*`. La versione a ritroso la tiene git |
| **B** · storia delle scelte | «prima diceva», «Correzione canone (DM)» | mai | `<!-- storico -->`, come in ADR-0069; il fatto si riscrive senza la storia («A6 non gli mostra…») |
| **C** · stato al tavolo | cosa è già successo, il ramo che vale, l'orologio | sì | riscritto come fatto, senza etichette di lavoro: «**Quando si gioca**», «**Com'è il mondo a quel punto**» |
| **D** · rimandi interni | `DEF-3 §7`, «master #3», il nome di un file | tradotti | l'esportatore li traduce (sotto) |

A queste si aggiunge l'istruzione di consegna sui fogli ✉, che ADR-0069 chiude
già col blocco `<!-- consegna -->`.

**La forma standard di un rimando è `DEF-N`.** Non si introduce una sigla nuova.
L'esportatore la traduce così:

- il master sta nel volume → il suo capitolo, preso dal manifest: `DEF-3 §7`
  diventa «cap. IV §7»;
- non sta nel volume → il titolo del master, preso dal suo H1 standard
  («ARC-07 · DEFINITIVO #1 — IL PIANO DELLA TERRA & TERROS L'ANTICO» → «Il Piano
  della Terra & Terros l'Antico»);
- la forma in prosa «master #N» fuori dal volume resta com'è: diventerebbe «nel
  «Il Piano…»», e la riscrive chi scrive. La vede il rilevatore;
- un nome di file fra backtick che è un capitolo del volume diventa il suo
  capitolo («Allegato di `...PALIO-DM-MASTER-REFERENCE.md`» → «Allegato di
  cap. I»).

È **il manifest a decidere quali DEF entrano** in un volume: una serata normale
ne prende due, una sessione lunga anche il terzo.

**Una pagina si stampa una volta.** Il corredo di una serata è il booklet del DM
(regia e master che si giocano) e il volume dei fogli ✉. I fogli stanno **solo**
nel volume dei giocatori; il booklet del DM li cita per titolo. Un volume di
approfondimento entra nel corredo solo se non ristampa un capitolo del booklet.
Per ARC-07, confermato dal DM: il booklet della serata stampa `DEF-2`, `DEF-3` e
`DEF-4` (è una sessione lunga) e nessun foglio ✉; il volume del −1000 resta un
libro a sé, fuori dal corredo, e perde i due fogli ✉ che ristampava.

**La misura sta sul PDF, non sui sorgenti.** La stessa riga si stampa in un
volume e non in un altro, perché un rimando si traduce o un blocco si toglie:
conta la carta. `validate_corredo.rilievi_apparato` cerca nel testo del PDF le
firme delle classi A, B e D, e `validate_booklets --stampa` la esegue su ogni
volume del repo, contro un tetto dichiarato col suo perché in
`scripts/apparato-residui.json`. Il tetto funziona nei due versi: un rilievo in
più è rosso, e anche un tetto più alto del vero. Il bersaglio è zero. I doppioni
li boccia `validate_corredo`, che confronta i capitoli dei volumi dello stesso
corredo.

**Un caso giudicato**: «Per il giocatore di Thorik. Leggi in privato… Cosa
farne è affar tuo», in testa ai fogli di Terros, parla al giocatore e non gli
dice quando riceverà il foglio. Non è un'istruzione di consegna e resta.

## Le conseguenze

| Volume | Rilievi prima | Dopo | Pagine |
|---|---:|---:|---|
| booklet della serata ARC-07 (con `DEF-4`) | 150 | **0** | 106 → 90 (i fogli ✉ non si ristampano) |
| volume dei giocatori della serata | 0 | 0 | 18 → 17 |
| volume del −1000 | 87 | 2, dichiarati | 42 |
| booklet del Ritorno · di Terros | 60 · 93 | 0 · 0 | |
| Palio · Drappo, volume del DM | 65 · 97 | 26 · 43, dichiarati | |

I numeri di «prima» contano le occorrenze, non le righe: la stima del DM, fatta
a righe, era di circa 95 e 20.

Sui volumi fuori da ARC-07 la parte automatica (i nomi di file tradotti in
capitoli, le parentesi di soli percorsi, le citazioni delle fonti, la riga del
Bestiario, la didascalia degli SVG) ha fatto la metà del lavoro. Il resto sono
residui dichiarati, e ognuno chiede un giudizio dentro il modulo: le «patch a
state.md» del Palio, la mappa dei file nell'hub del Drappo, i crediti delle
icone del Palio, che sono un'attribuzione di licenza e devono restare.

La didascalia degli SVG è diventata un commento XML: chi apre il file la legge,
la stampa no. Sono stati rigenerati tutti i 41 SVG del repo.

Quello che si paga:

- **I marcatori della classe A e della classe B restano a mano.** Un blocco per
  file basta all'intestazione di un master; il resto è una riga per volta.
- **Il rilevatore ha falsi positivi, e si dichiarano.** «#1» dentro la finzione e
  «si consegna» nel Palio non li prende, perché le firme chiedono la parola
  «master» o il formato `DEF-N`; un nome di file dentro la finzione lo
  prenderebbe. Per questo il tetto è per volume e ha un perché.
- **La misura chiede PyMuPDF**, che è AGPL. È fra le dipendenze di sviluppo per
  decisione del DM (D7 di `PIANO-CICLO-DI-SESSIONE-E-MENU`), si usa senza
  modifiche e non si distribuisce. Senza, la misura si dichiara saltata.
- **Una frase con un rimando fuori dal volume** può uscire zoppa («il «Il
  Viaggio a 1.000 Anni fa» parte»): la regola del titolo preso dall'H1 è
  meccanica. Il rimando fra parentesi dopo il nome della cosa è la forma che
  regge in ogni volume, ed è quella da scrivere.
