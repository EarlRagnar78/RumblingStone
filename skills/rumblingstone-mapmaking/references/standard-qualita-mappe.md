# Lo standard di qualità delle mappe

<!-- indice: generato da scripts/indice_references.py, non scriverlo a mano -->
**In questo file**

- Le fonti
- Come si prepara una mappa nuova o rifatta
- Le regole misurabili
- Metriche profonde (solo misura)
- Cosa si controlla a vista
- Il rilievo e il contesto
- Cosa lo standard non misura
<!-- /indice -->

Questo file dice quando una mappa tattica è plausibile e giocabile, con regole
che si misurano e regole che si guardano. Lo ha chiesto il DM il 2026-10-22:
mappe «quanto più plausibili e vicine sia come scale che posizionamento» a
quelle che cartografi e community considerano le migliori, e i metodi trovati
in rete «integrati nel repo in modo che diventino standard»
([ADR-0098](../../../plans/adr/ADR-0098-la-qualita-delle-mappe-si-misura-con-uno-standard.md)).

Le misure le prende `scripts/qualita_mappe.py`, sopra il collaudo
(`collaudo_mappe.py`, [collaudo-mappe.md](collaudo-mappe.md)). Il collaudo
risponde a «si gioca?»; questo standard a «quanto è buona?». Le misure delle
cose reali (porte, tende, mura, ponti) stanno in
`plans/esperimenti/mappe-campo-2026-10-21/AUDIT-SCALE-MAPPE.md` §1 e
`RICERCA-ACCAMPAMENTI.md`, con le loro fonti; qui si citano solo dove diventano
una soglia.

## Le fonti

| Fonte | Che cosa insegna |
|---|---|
| Justin Alexander, [Jaquaying the Dungeon](https://thealexandrian.net/wordpress/13085/roleplaying-games/jaquaying-the-dungeon) e [parte 2, le tecniche](https://thealexandrian.net/wordpress/13103/roleplaying-games/xandering-the-dungeon-part-2-xandering-techniques) | più ingressi, anelli, più collegamenti fra livelli, passaggi segreti, sotto-livelli, piccoli dislivelli, ingresso a metà percorso. *Caverns of Thracia* ha tre ingressi al primo livello e otto vie non convenzionali verso il basso |
| [Checklist breve per mappe alla Jaquays](https://www.goodreads.com/author_blog_posts/23244936-a-simpler-checklist-for-jaquays-style-dungeon-maps) | per le mappe piccole: pianta non lineare e asimmetrica, più ingressi, percorsi ad anello, più strade dall'inizio alla fine, scorciatoie |
| Joris Dormans, [Adventures in Level Design](https://www.pcgworkshop.com/archive/dormans2010adventures.pdf) (PCG 2010) e [il generatore ciclico di *Unexplored*](https://www.gamedeveloper.com/design/unexplored-s-secret-cyclic-dungeon-generation-) | una mappa è una *missione* (l'ordine delle prove) posata su uno *spazio* (le stanze): si progettano separate. Si parte da un anello, non da un albero |
| Gillian Smith e Jim Whitehead, [Analyzing the Expressive Range of a Level Generator](https://www.pcgworkshop.com/archive/smith2010analyzing.pdf) (PCG 2010) | le metriche di *linearity* e *leniency*: un livello si misura su poche proprietà globali e si confronta con gli altri, mai da solo |
| Antonios Liapis, Georgios Yannakakis, Julian Togelius, [Towards a Generic Method of Evaluating Game Levels](https://ojs.aaai.org/index.php/AIIDE/article/download/12680/12528/16197) (AIIDE 2013) | *area control*, *exploration*, *balance* su una griglia: le celle «sicure» per ciascuna fazione e quanto costa a una fazione trovare l'altra. È la base della distanza fra le fazioni |
| Ross e Peter Mawhorter, [Metrics for exploration games](https://cs.wellesley.edu/~pmwh/mvmap/papers/meg/metrics_for_exploration_games.md) | la *cyclic fraction*: la quota di nodi che sta su un anello di almeno tre. Nelle mappe intere dei giochi d'esplorazione è intorno all'80% |
| Boris the Brave, [Lock and Key Dungeons](https://www.boristhebrave.com/2021/02/27/lock-and-key-dungeons) | un livello che sembra intricato può essere lineare se una sola strada fa progredire; i vicoli ciechi si vedono solo sovrapponendo il grafo alla mappa |
| Johnn Four, la *Five Room Dungeon* ([sintesi](https://bestiarumgames.com/blogs/news/better-ttrpg-dungeon-design-with-five-room-dungeon)) | ingresso e guardiano, enigma, imprevisto, scontro, ricompensa. Sconsiglia il «corridoio dritto con cinque fermate» |
| Sean K. Reynolds (Paizo), [Superstar Maps](https://paizo.com/blog/design-tuesday-superstar-maps) | una mappa per l'avventura è leggibile prima che ricca: barra di scala sulla mappa, rosa dei venti, simboli riconoscibili, colore per distinguere, niente dettagli di cui il cartografo non capisce il ruolo |
| [Criteri del Cartographic Salon della NSS](https://legacy.caves.org/committee/salons/Cartographic%20Salon%20Criteria.shtml) | i requisiti di una carta da concorso: nome, ingresso evidente, nord, barra di scala, controllo verticale (profili), legenda dei simboli non standard, fine dei passaggi distinta dal vero vicolo cieco |
| [Coup-De-Grace: Arena Design](https://wiki.rpg.net/index.php/Coup-De-Grace:_Arena_Design) (RPG.net) | circa 2 quadretti di larghezza per miniatura; le mappe troppo grandi ritardano il contatto; zone di partenza non sicure, più accessi, strozzature fra corridoio e sala, strade di rischio simile |
| Paizo, [Flip-Mat](https://pathfinderwiki.com/wiki/Battlefield_Flip-Mat) e [Flip-Mat Enormous](https://store.paizo.com/pathfinder-flip-mat-enormous-basic-pdf/) | la misura di un campo di scontro al tavolo: 24 × 30 quadretti il Flip-Mat (Jason Engle), 30 × 46 l'Enormous |
| Dyson Logos, [The Giant's Halls](https://dysonlogos.blog/2015/10/16/friday-map-the-giants-halls-part-1/) | un'esagerazione voluta (sale da 9-12 m) si dichiara, con la sua ragione: «poco senso costruttivo, viste epiche per gli scontri» |
| Paizo, [discussione su Abomination Vaults](https://paizo.com/threads/rzs43dl6) (James Jacobs, Ron Lundeen) | realismo e «una creatura per quadretto» tirano in direzioni opposte: si allarga lo spazio di manovra, non gli oggetti |
| Mike Schley, Rob Lazzaretti, Jason Engle | i riferimenti visivi: Schley per *Red Hand of Doom* e il DMG ([le sue mappe](https://www.aidedd.org/adj/cartes-maps/)), [Lazzaretti](https://en.wikipedia.org/wiki/Rob_Lazzaretti) per la 3ª edizione e i folio Paizo, Engle per i Flip-Mat. Non hanno scritto regole pubbliche; si guardano e non si copiano |
| Community: [discussione «cosa fa una buona battlemap»](https://lemmy.world/post/72982), [Dungeon Scrawl, consigli](https://blog.dungeonscrawl.com/2025/10/01/top-tips-for-dungeon-maps/) | colonne e corridoi allineati alla griglia, stanze con una ragione (dove si dorme, come arrivano le scorte), più uscite per aggirare, porte segrete larghe 1-2 quadretti e poche |
| Ecologia del dungeon ([piramide alimentare](https://steemit.com/tabletoprpg/@grimjim/plausible-dungeon-ecology)) | chi vive in un luogo mangia, dorme e scarica da qualche parte; a ogni gradino della catena serve circa dieci volte la massa del gradino sopra |
| ENnie, [Best Cartography 2006](https://en.wikipedia.org/wiki/2006_ENnie_Award_winners) | l'anno di *Red Hand of Doom*: oro a *Tasslehoff's Map Pouch*, argento a *The Shackled City* di Paizo |
| ArchDaily, [scale a chiocciola](https://www.archdaily.com/896537/how-to-calculate-spiral-staircase-dimensions-and-designs) | raggio minimo 0,70 m, meglio 0,80: una chiocciola sta in un quadretto solo come simbolo, il vano è 2 × 2 |

Le mappe protette (Paizo, Schley, 2-Minute Tabletop) servono a vedere come si
legge un luogo su una griglia. Nessun disegno si riprende.

## Come si prepara una mappa nuova o rifatta

L'ordine conta: chi parte dalla tattica disegna un'arena, chi parte dalla
funzione disegna un luogo in cui poi si combatte.

1. **La funzione.** Chi ci vive o ci lavora, e che cosa ci fa. Per ogni area:
   dove si dorme, si mangia, si tengono le scorte, si scarica, da dove arrivano
   l'acqua e l'aria, dov'è la luce. Un accampamento ha il comando separato, le
   file di tende, la cucina sottovento, le latrine lontane dall'acqua. Un
   castello ha le mura spesse, la porta difesa, il pozzo dentro. Una caverna
   abitata ha una via per l'acqua e una per l'aria. Una stanza senza funzione si
   toglie o se ne scrive la ragione (crollo, abbandono, magia).
2. **Il flusso.** Il grafo prima della pianta (Dormans): le aree come nodi, i
   passaggi come archi. Almeno due ingressi per un complesso, almeno un anello,
   e i vicoli ciechi solo dove c'è qualcosa da trovare (Jaquays). Si scrive da
   dove entrano i PG, da dove arrivano i rinforzi e da dove si scappa.
3. **La scala.** Ogni oggetto alla sua misura reale (tabelle dell'audit del
   2026-10-21): porta 1-2 quadretti, portone da carro 2-3, cortina di castello
   2-4 di spessore, tenda a un palo fino a 6-7 quadretti, tenda del contubernium
   2 × 2. La mappa tattica è a 1,5 m per quadretto; se lo scontro è più grande di
   due Flip-Mat Enormous si divide in carte o si fa una vista strategica
   (`@tipo strategica`) e si ritaglia la parte dello scontro.
4. **La tattica.** Solo ora le creature: dove partono, in quanti round si
   toccano, quali coperture e linee di vista ci sono, dove sta la strozzatura e
   se è voluta. Le creature Grandi e Enormi hanno `@taglia` e il loro ingombro
   libero. Poi il collaudo, la misura di qualità, il render, il PNG e il
   collaudatore a freddo, come in [collaudo-mappe.md](collaudo-mappe.md).

## Le regole misurabili

Il comando:

```bash
python3 scripts/qualita_mappe.py FILE.md            # metriche, rilievi e voto
python3 scripts/qualita_mappe.py --classifica       # tutto il corpus, dal peggiore
python3 scripts/qualita_mappe.py FILE.md --strict   # esce 1 se resta un errore
python3 scripts/qualita_mappe.py --json OUT.json    # per un altro programma
```

Gli **errori** (E) sono fatti: l'intestazione mente, una direttiva punta fuori
dalla griglia, una quota non è un numero. Una mappa nuova o rifatta esce senza errori. Gli **avvisi** (A)
sono soglie di mestiere; ognuno si spegne con `@deroga <codice> ; <motivo>`,
con un motivo di almeno 15 caratteri, come nel collaudo.

| Codice | Classe | Regola e soglia | Fonte |
|---|---|---|---|
| `scala/dichiarata` | E | l'intestazione `N col × M righe` coincide con la griglia disegnata | contratto di fedeltà (SKILL.md, regola 6) |
| `direttive/fuori-griglia` | E | ogni cella scritta in `@mark`, `@path`, `@zone`, `@taglia`, `@collega`, `@verso` esiste | idem |
| `scala/tattica-non-a-1-5` | A | una mappa tattica è a 1,5 m per quadretto | SKILL.md, regola 2; Flip-Mat |
| `scala/titolo` | A | le misure in metri del titolo valgono la griglia per la scala, ±15%; un titolo «strategico» vuole `@tipo strategica` | audit 2026-10-21 (1A-3, MAPPA 1) |
| `dimensioni/oltre-tavolo` | A | una tattica non supera due Flip-Mat Enormous (2.760 quadretti) | Paizo, Flip-Mat Enormous 30 × 46 |
| `funzione/blocco-pieno` | A | in esterni nessun blocco di ⬛ supera il 25% della mappa (e 60 celle) | audit 2026-10-21 (Campo Drow 2) |
| `oggetti/telo-enorme` | A | un telo 🎪 non supera 18 m di lato | Ricerca accampamenti, regola 1 |
| `oggetti/tende-a-grappolo` | A | non più di 3 ⛺ attaccate: la tenda grande è 🎪 riempito | idem, regole 2 e 5 |
| `oggetti/fuoco-enorme` | A | un fuoco da campo sta in 4 quadretti; l'incendio si deroga | audit, «Fuoco da campo» |
| `oggetti/fuoco-sotto-il-telo` | A | nessun 🔥 adiacente a 🎪 o ⛺ | idem |
| `oggetti/porta-enorme` | A | una fila di porte non supera 3 quadretti (4,5 m) | PF1 Core, Doors; Timeref, Gatehouses |
| `coerenza/mura-sottili` | A | in una fortezza, non oltre l'80% delle 🏰 spesse un quadretto | h2g2, Curtain Wall; Caernarfon |
| `taglia/non-entra` | A | una creatura con `@taglia` ha N × N quadretti liberi attorno alla sua cella | SRD, Spazio e portata |
| `taglia/non-dichiarata` | A | un drago, un treant, un gigante su un quadretto solo ha `@taglia` | SRD; audit (Foresta in Fiamme, Last Stand) |
| `fazioni/lontane` | A | il nemico più vicino è entro 54 m di cammino dai PG (tre round di doppio movimento a 9 m) | Coup-De-Grace, «sprawling maps delay contact»; Liapis 2013 |
| `fazioni/a-contatto` | A | PG e nemici non partono adiacenti, salvo imboscata scritta | idem |
| `spazio/affollato` | A | almeno 4 celle libere per creatura | Coup-De-Grace, 2 quadretti di larghezza per miniatura |
| `spazio/disperso` | A | non oltre 150 celle per creatura su una mappa più grande di un Flip-Mat Enormous | idem; Flip-Mat |
| `struttura/un-ingresso` | A | in interni e caverne con almeno 150 celle percorribili, almeno 2 ingressi distinti: due varchi contano come due solo se stanno ad almeno 10 passi l'uno dall'altro (sotto, «Gli ingressi») | Jaquays, *Multiple Entrances*; RICERCA-STRUMENTI-MAPPE §5 |
| `struttura/senza-anelli` | A | in interni e caverne con almeno 300 celle percorribili, almeno un anello attorno a un blocco | Jaquays, *Loops*; Dormans; Mawhorter |
| `struttura/vicoli-ciechi` | A | meno di 3 vicoli ciechi senza niente in fondo (entro 2 quadretti) | Jaquays; Boris the Brave; NSS |
| `struttura/fila-indiana` | A | con almeno 6 creature, non oltre metà del percorribile largo un quadretto | Coup-De-Grace, strozzature |
| `lettura/troppi-simboli` | A | al più 18 simboli diversi | Reynolds (Paizo), leggibilità |
| `lettura/legenda-locale-lunga` | A | al più 8 simboli locali | SKILL.md, regola 3 |
| `lettura/affollata` | A | al più il 30% del pavimento con un'icona | Reynolds (Paizo); NSS, *balance and layout* |
| `contesto/quota-illeggibile` | E | `@quota` e `@dislivello` hanno un numero in metri o piedi | contratto di fedeltà |
| `contesto/quota-mancante` | A | una mappa all'aperto, di abitato o strategica dichiara `@quota` e `@dislivello` | DM, 2026-10-22; NSS, controllo verticale |
| `contesto/quote-discordi` | A | le mappe con lo stesso `@luogo` dichiarano la stessa quota, entro 5 m | DM, 2026-10-22 |

Il punteggio parte da 100. Ogni errore toglie 12 punti, gli avvisi i pesi
scritti in testa allo script (da 1 a 6). Pesano anche i rilievi del collaudo:
12 punti per errore fino a 48, 4 per `ingombro/grande`, 2 per M1, M2, M4 e
`zone/separate`, 1 per gli altri. Le bande sono **buona** da 90, **da
ritoccare** da 75, **da rivedere** da 55, **da rifare** sotto.

Le soglie sono di mestiere: vengono dalle fonti dove una fonte dà un numero, e
dal corpus del repo dove non lo dà. Il punteggio serve a ordinare le mappe, non
a dire quanto vale una scena.

### Le metriche che lo strumento riporta senza soglia

Escono nel rapporto di ogni mappa e nel JSON, per confrontare le mappe fra loro
come vuole il metodo di Smith e Whitehead.

| Metrica | Come si calcola |
|---|---|
| `libere` | celle percorribili sul totale (porte aperte) |
| `anelli`, `anelli_strutturali` | i buchi dello spazio percorribile (primo numero di Betti): ostacoli chiusi su ogni lato da celle percorribili. Strutturale se il blocco ha almeno 4 celle e il giro attorno almeno 16 |
| `varchi`, `ingressi` | `varchi`: tratti percorribili del bordo, più scale, botole, pozzi e portali. `ingressi`: i varchi distinti, uniti quando stanno a meno di 10 passi. Un bordo tutto aperto conta 4 |
| `vicoli_ciechi`, `vicoli_vuoti` | celle con un solo vicino ortogonale percorribile, lontano dal bordo; vuoti se niente di notevole sta entro 2 quadretti |
| `fila_indiana` | quota del percorribile in cui il tratto più corto, orizzontale o verticale, è di un quadretto |
| `copertura` | quota del percorribile con una copertura (½, ¾ o totale) a contatto; M1 e M2 come nel collaudo |
| `distanza_min_m`, `distanza_media_m`, `round_al_contatto` | cammino dai PG (🔵) ai nemici (🔴 ⚫ 🟡 🟣) con la diagonale 5-10-5 e il costo del terreno |
| `strozzatura` | il passaggio più stretto del cammino più largo fra PG e nemici |
| `celle_per_creatura`, `flipmat`, `area_m2` | spazio per miniatura, tappeti Enormous occupati, superficie |
| `simboli`, `simboli_locali`, `densita_icone` | quanti simboli deve imparare il giocatore, e quanto pavimento è coperto |

### Gli ingressi

Due porte a due quadretti nella stessa stanza sono un ingresso solo: chi
difende le copre con la stessa fila. Fino al 2026-10-22 lo strumento contava
ogni tratto aperto del bordo, e il riparatore automatico della ricerca sugli
strumenti (`RICERCA-STRUMENTI-MAPPE.md` §5, commit `ffe206b5` del ramo
`claude/project-thread-e860p0`) ne ha approfittato: apriva un secondo varco
accanto al primo e il rilievo spariva.

La regola, come la misura la ricerca:

- un **passo** è lo spostamento fra due celle percorribili che hanno un lato
  in comune, senza diagonale. Le porte contano aperte, come nel resto dello
  strumento; una scala o un portale disegnati su una cella che blocca restano
  raggiungibili;
- la distanza fra due varchi è il numero minimo di passi fra le loro celle più
  vicine. Fra due porte nel muro nord a *d* colonne l'una dall'altra se ne fanno
  *d* + 2: si scende, si cammina, si risale;
- due varchi sono due ingressi se la distanza è di **almeno 10 passi**, o se a
  piedi non si passa dall'uno all'altro. Sotto, si uniscono, anche a catena: A
  vicino a B e B vicino a C fanno un ingresso solo.

Nella ricerca la soglia sta nel riparatore (`genera_ripara.py`, che misura i
passi con una visita in ampiezza a quattro direzioni) e nella raccomandazione
§6.3 («almeno 10 passi a piedi, o danno su componenti diverse»). Il «passo»
della profondità a piedi (§3 della ricerca, e le metriche profonde qui sotto)
è un'altra misura: lì il passo diagonale vale uno.

## Metriche profonde (solo misura)

```bash
python3 scripts/qualita_mappe.py --json OUT.json --profonde
```

Le calcola `scripts/qualita_mappe_profonde.py` e finiscono **solo nel JSON**
(`map_quality/1`), sotto la chiave `profonde` di ogni mappa. Non hanno soglia,
non cambiano il voto e non danno avvisi: nessuna fonte dà un numero giusto per
una battlemap, e servono a confrontare due mappe, o due versioni della stessa,
come vuole il metodo di Smith e Whitehead. Le mappe strategiche e gli schemi si
saltano (`"saltata"`). Sul corpus intero la misura costa circa un minuto: la
vista è quadratica nelle celle.

| Chiave | Che cosa misura | Fonte |
|---|---|---|
| `vista` | space syntax sul grafo di visibilità: i nodi sono le celle percorribili, gli archi uniscono le celle che si vedono. `connettivita_media` (celle viste), `profondita_media` MD = Σd/(k−1), `integrazione_media`, `_min`, `_max` = D_k/RA con RA = 2(MD−1)/(k−2), `intelligibilita_r2` = r² fra connettività e integrazione | Turner, Doxa, O'Sullivan, Penn, [*From isovists to visibility graphs*](https://discovery.ucl.ac.uk/id/eprint/160/) (2001); Ostwald, [*The Mathematics of Spatial Configuration*](https://link.springer.com/content/pdf/10.1007/s00004-011-0075-3.pdf) (2011) per RA e D_k; Hillier, citato in Dalton e Bafna, [*The syntactical image of the city*](https://discovery-pp.ucl.ac.uk/1104/1/SIC.pdf.pdf) (2003), per l'intelligibilità |
| `accesso` | le stesse misure sul grafo di movimento del collaudo: otto direzioni, la diagonale non passa l'angolo di un muro, ogni passo vale uno | idem |
| `vista_accesso_r` | r di Pearson fra l'integrazione di ogni cella alla vista e a piedi. Basso: quello che si vede non è quello che si raggiunge (la lava, i ponti, le feritoie) | Martin, [*A spatial analysis of the JBA headquarters in Splinter Cell: Double Agent*](https://nottingham-repository.worktribe.com/output/722027/a-spatial-analysis-of-the-jba-headquarters-in-splinter-cell-double-agent) (2014). La formula è della ricerca: l'abstract di Martin non la dà |
| `simmetria` | quota di celle uguali allo specchio sinistra-destra (`orizzontale`), alto-basso (`verticale`) e alla rotazione di 180 gradi, sulle classi di cella (muro, ostacolo, porta, scala, pericolo, copertura, creatura, pavimento, fuori) | Summerville et al., [*Understanding Mario*](https://webdocs.cs.ualberta.ca/~santanad/papers/2017/summervilleMSOL17.pdf) (2017) |
| `pattern_2x2` | le finestre 2 × 2 sulle stesse classi: quante (`finestre`), quante diverse (`distinti`), entropia di Shannon della distribuzione in bit (`entropia_bit`) | Lucas e Volz, [*Tile Pattern KL-Divergence*](https://arxiv.org/pdf/1905.05077) (2019); [ETPKLDiv](https://github.com/amidos2006/ETPKLDiv) (MIT) |

Come si leggono, e i limiti:

- k è la grandezza della componente della cella; sotto 4 celle le formule non
  valgono e la cella si salta. Dove RA è zero (una stanza in cui ogni cella vede
  tutte le altre) l'integrazione non è definita ed esce `null`.
- Il D_k è quello di Hillier e Hanson, 2{k[log₂((k+2)/3) − 1] + 1}/((k−1)(k−2)),
  tarato sui grafi assiali piccoli: l'integrazione della vista cresce con le
  celle (95 sul *Corridoio del Fuoco*, 667 celle; 9,5 sulla *Tenda del comando*,
  493). Fra mappe diverse si confronta la profondità media; l'integrazione si
  confronta fra due versioni della stessa mappa.
- La vista è lo shadowcasting simmetrico di [Albert Ford](https://www.albertford.com/shadowcasting/)
  (CC0), scritto in libreria standard. È lo stesso algoritmo che `tcod` chiama
  `FOV_SYMMETRIC_SHADOWCAST` e che il collaudo usa per M4, ma l'implementazione
  di `tcod` non coincide cella per cella con quella di riferimento di Ford: su
  7.321 punti di vista del corpus, da 625 (l'8,5%) il campo differisce di qualche
  cella percorribile. Le metriche profonde seguono Ford; M4 resta su `tcod`.
- Lo space syntax è una misura accettata della configurazione in architettura e
  urbanistica, ed è stato applicato ai videogiochi; le sue correlazioni con il
  comportamento vengono da persone che camminano, non da miniature a turni.
- Dalla prova della ricerca non sono entrati: il clustering di Turner (per ogni
  cella conta gli archi fra tutte le coppie di celle che vede), l'isovista media in m² (è M4 del collaudo), la
  divergenza KL contro il corpus (cambia con il corpus del momento) e la
  *leniency* adattata (la traduzione dal platform non regge sul terreno letale
  esteso).

Il codice viene da `metriche_nuove.py`, nella cartella `mappe-strumenti-2026-10-22`
degli esperimenti (commit `ffe206b5`, non ancora su `main`), riscritto senza `numpy`, `scipy` e `tcod`, che stanno in
`requirements-dev.txt` e non in `requirements.txt`. Sulle tre mappe della prova
(*Corridoio del Fuoco*, *Fucina grande 372*, *Tenda del comando*) le misure a
piedi, la simmetria e i pattern coincidono con la ricerca; alla vista i numeri
differiscono alla terza cifra (profondità media della tenda 1,744 contro 1,739),
per la differenza fra Ford e `tcod`.

## Cosa si controlla a vista

Lo strumento non vede tutto. Prima di consegnare, chi ha disegnato e il
collaudatore a freddo controllano sul PNG:

- **Funzione.** Ogni area ha uno scopo leggibile; chi ci vive ha dove dormire,
  mangiare, tenere le scorte e scaricare; acqua e aria hanno una via.
- **Logica difensiva.** Una fortezza ha la porta difesa da torri o da un
  androne, mura con il camminamento, un pozzo dentro; un campo ha il comando al
  centro e libero attorno, le tende in file con le corsie, i fuochi lontani dai
  teli, il recinto con i varchi sulle vie.
- **Coerenza fra le mappe dello stesso luogo.** Due mappe della stessa fortezza
  hanno le stesse misure; una scala porta alla sua gemella (`@collega`).
- **Misure delle cose.** Porte, tende, ponti, letti, incudini alla loro misura
  reale anche quando lo spazio di manovra è allargato; l'esagerazione voluta si
  scrive nella mappa con la sua ragione (Dyson Logos).
- **Tattica.** Le zone di partenza non sono rifugi; c'è più di una strada di
  rischio simile; le coperture stanno dove servono, non sparse a caso; si
  capisce in quanti round ci si tocca.
- **Leggibilità.** Nord, barra di scala e legenda nell'SVG; i simboli si
  distinguono senza la legenda locale; colonne e corridoi stanno sulla griglia;
  le annotazioni non coprono le celle.
- **Verticalità.** Dove ci sono dislivelli, una tavola di profilo con le quote
  (SKILL.md, «Le tavole di supporto»).

## Il rilievo e il contesto

Il DM, il 2026-10-22: Hammerfist «è scavata nella collina o nella montagna,
quindi sopra la pianura con gli accampamenti dell'orda», e ogni mappa va
confrontata con quello che la circonda. Una mappa che non dice a che altezza sta
non si può mettere accanto alla regionale.

### Che cosa dichiara una mappa

Nel blocco della griglia, accanto a `@tipo`:

```text
@luogo Hammerfist, porta principale
@quota 1050 m ; s.l.m.
@dislivello +150 m ; sulla piana dell'orda, a sud
```

- `@quota` è l'altezza del punto più usato della mappa (la porta, la piazza, il
  pavimento della sala), in metri o piedi, con il riferimento dopo il `;`.
- `@dislivello` è quanto quel punto sta sopra (+) o sotto (−) il terreno
  intorno che conta per la scena: la piana da cui sale l'assedio, il fiume, la
  strada. Per una sala sotterranea è la profondità dalla superficie.
- `@luogo` unisce le mappe dello stesso punto. Due punti diversi dello stesso
  sito (la porta e la cima del maschio) prendono due nomi, perché hanno due
  quote.

Lo strumento legge le tre direttive, avvisa se una mappa all'aperto, di abitato
o strategica non dichiara quota e dislivello, dà errore se il valore non è un
numero, e confronta le quote delle mappe con lo stesso `@luogo`. Le mappe al
chiuso e in caverna non sono obbligate; dichiararle aiuta lo stesso.

### Che cosa si controlla a vista

- **Le carte di zona e regionali hanno il rilievo.** Isoipse, o fasce di quota
  colorate con la loro legenda, o almeno un profilo dalla piana alla fortezza.
  Il tratteggio dei monti da solo non dice quanto si sale.
- **Le distanze tornano fra le scale.** La distanza fra due luoghi è la stessa
  sulla regionale, nella tabella dei viaggi e nel testo dell'avventura; un campo
  «a 2 km dalle mura» sulla mappa di zona sta a 2 km anche nel read-aloud. La
  barra di scala di una mappa derivata da un'altra si verifica, non si eredita.
- **La città ha la grandezza della sua gente.** L'area dentro le mura per la
  densità della tabella sotto dà gli abitanti; se il testo ne dice un numero
  diverso, si corregge l'uno o l'altro.
- **La fortezza sta dove la difesa ha senso.** Su uno sperone o in parete la
  piana è sotto tiro e la salita è lenta; su una piana aperta servono fossato,
  mura spesse e torri fitte. Quale dei due si sceglie, si disegna.

### Le misure di riferimento

Fortezze sulla roccia, per la quota e la salita:

| Luogo | Misure | Fonte |
|---|---|---|
| Mehrangarh (Jodhpur) | 122 m sopra la piana; mura alte fino a 36 m e larghe 21; sette porte in salita | [Wikipedia](https://en.wikipedia.org/wiki/Mehrangarh) |
| Krak des Chevaliers | sulla cima di un colle di circa 650 m; mura esterne di 9 m; un corridoio voltato in salita di 137 m con tornanti; guarnigione fino a 2.000 | [Wikipedia](https://en.wikipedia.org/wiki/Krak_des_Chevaliers) |
| Masada | altopiano di 550 × 270 m, 400 m sopra il Mar Morto a est e 90 m a ovest; cinta a casematte di 1.300 m; la rampa d'assedio romana alta circa 114 m | [Wikipedia](https://en.wikipedia.org/wiki/Masada) |
| Monemvasia | rupe con pareti di circa 180 m, una sola strada rialzata dalla costa | [Britannica](https://www.britannica.com/place/Monemvasia) |
| Derinkuyu | città scavata profonda circa 85 m su almeno cinque livelli, pozzi d'aria, macine di pietra come porte, fino a 20.000 persone | [Wikipedia](https://en.wikipedia.org/wiki/Derinkuyu_underground_city) |
| Dover | gallerie scavate nella falesia circa 15 m sotto la cima; nel 1216 i difensori scavarono contro-mine verso gli assedianti | [Wikipedia](https://en.wikipedia.org/wiki/Dover_Castle) |

Gittate, per la distanza fra mura e campo nemico:

| Arma | Gittata | Fonte |
|---|---|---|
| arco lungo | fino a circa 366 m in tiro curvo; il tiro utile contro una formazione è sui 200 m | [Archery Historian](https://archeryhistorian.com/english-longbow/) |
| balista antica | oltre 460 m di gittata massima | [Wikipedia, Ballista](https://en.wikipedia.org/wiki/Ballista) |
| macchine d'assedio PF1 | incremento di gittata: balista leggera 36 m, pesante 54 m, catapulta leggera 45 m, pesante 90 m, trabucco leggero 60 m | PF1 Ultimate Combat, [Siege Engines](https://thecrazygm.root.sx/ogl/pf1e/variants/variant-combat/siege-weapons/) (OGL) |

Un campo d'assedio sta fuori dal tiro utile delle macchine dei difensori: con una
balista pesante PF1 a 54 m d'incremento, cinque incrementi fanno 270 m; con il
tiro dall'alto il campo arretra ancora.

Città, per l'area, la gente e le strade:

| Riferimento | Misure | Fonte |
|---|---|---|
| densità di una città medievale | circa 150 abitanti per ettaro, fino al doppio nelle più grandi; villaggio fino a 1.000, cittadina 1.000-8.000, città 8.000-12.000, grande città oltre | S. John Ross, [Medieval Demographics Made Easy](https://lacrypte.fr/index.php/autres/articles-divers-sur-le-medieval/84-medieval-demographics) |
| Pompei | 64-67 ha dentro le mura, circa 11.000 abitanti: 170 per ettaro | [Wikipedia](https://en.wikipedia.org/wiki/Pompeii) |
| Ávila | mura di 2.516 m, alte 12, spesse 3; 88 torri (una ogni 29 m circa); 9 porte; 31 ha | [Wikipedia](https://en.wikipedia.org/wiki/Walls_of_%C3%81vila) |
| Roma, mura serviane | 11 km, alte fino a 10 m, spesse 3,6 alla base; 16 porte | [Wikipedia](https://en.wikipedia.org/wiki/Servian_Wall) |
| Roma, mura aureliane | 19 km, circa 1.400 ha; alte 8 m poi 16, spesse 3,5; una torre ogni 29,6 m; 18 porte | [Wikipedia](https://en.wikipedia.org/wiki/Aurelian_Walls) |
| strade romane | via da 4,8 a 6,5 m (le XII Tavole: 16 piedi); vicoli e marciapiedi intorno ai 2,9 m | [Calzadas romanas](https://aragonromano.ftp.catedu.es/streets.htm) |
| Baghdad rotonda | raggio di circa 1 km, quattro porte, palazzo e moschea al centro | [Wikipedia](https://en.wikipedia.org/wiki/Round_city_of_Baghdad) |
| Ctesifonte | circa 30 km², più del doppio della Roma del IV secolo (13,7 km²), sul Tigri | [Wikipedia](https://en.wikipedia.org/wiki/Ctesiphon) |
| Persepoli | terrazza di circa 450 × 300 m, alta 18 m nella parte centrale | [Livius](https://livius.org/articles/place/persepolis/persepolis-photos/persepolis-terrace) |
| Isfahan, Naqsh-e Jahan | piazza di 560 × 160 m; il bazar coperto, lungo circa 2 km, parte dal suo lato nord; la città vive del fiume Zayanderud | [Wikipedia](https://en.wikipedia.org/wiki/Naqsh-e_Jahan_Square) |
| qanat | canale sotterraneo per l'acqua, largo pochi decimetri, lungo di solito meno di 5 km e fino a 70; non porta barche | [Wikipedia](https://en.wikipedia.org/wiki/Qanat) |

Le torri delle mura stanno a un tiro d'arco o meno l'una dall'altra: 30 m ad
Ávila e a Roma. Una cinta con una torre ogni 150 m non si difende da sola.

## Cosa lo standard non misura

Il divertimento, i tempi veri al tavolo, il bilanciamento del GS e la bellezza
della pergamena. Il primo e il secondo li dice il playtest
(`rumblingstone-playtest`), il terzo il prep dell'incontro, l'ultimo
`misura_resa.py` e il DM.
