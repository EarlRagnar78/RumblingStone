# ADR-0144 — Due stampe per arco, e i rimandi portano il numero di pagina

**Stato**: proposta (2026-11-19)
**Data**: 2026-11-19
**Decisione-fonte**: il DM (Jfs), 2026-11-19: «mi fai la stampa sia della sessione che del ap per l arc07 e verifica se sono perfetti e se hanno le informazioni importanti e la struttura editoriale adatta per i 2 tipi di stampa», e «la stampa per l ap completo presenta la possibilità di dividerli per arc se ha senso?». Le due stampe per arco erano già state scelte il 2026-11-10.
**Rapporti**: segue [ADR-0122](ADR-0122-il-volume-segue-lo-schema-degli-adventure-path.md) (il volume segue lo schema degli AP) e [ADR-0128](ADR-0128-ogni-scheda-dichiara-taglia-spazio-e-portata.md); usa la traduzione dei rimandi di `scripts/dmcore/testo.py`; tocca `scripts/export_booklet_typst.py` e `scripts/typst/tema-rumblingstone.typ`. Misura: `plans/esperimenti/booklet-arc07-2026-11-19/misura_rimandi.py`.

## Contesto

Per ARC-07 c'era una sola stampa da tavolo, il booklet della serata «La notte e
l'alba» (130 pagine), più il booklet lungo da 162 pagine da cui è nato. Il
volume dell'arco intero, quello da leggere e preparare come un AP, non c'era:
i cinque master DEF stavano solo come file.

Nel booklet della serata, su main, i rimandi interni erano 107. Nessuno aveva
un numero di pagina: «cap. V Scena 6» chiede al DM di sfogliare fino al
capitolo e poi cercare la scena. Otto rimandi puntavano a un titolo che nel
capitolo indicato non c'è, perché il traduttore dei rimandi mandava al primo
capitolo i riferimenti spezzati da un a capo e la forma «§7 di `DEF-4`».

Gli AP di riferimento (Red Hand of Doom, le AP Paizo) stampano «see page 42»
nel testo del DM. È lo standard di fatto della comunità per un volume che si
usa al tavolo, e Typst lo permette senza librerie: `query` e `counter(page)`
danno la pagina di un titolo al momento della composizione.

## Alternative considerate

1. **Una stampa sola per arco, lunga.** Scartata: il 10/11 Jfs ha scelto due
   stampe, e la serata ha bisogno solo di ciò che si gioca dal barile in poi.
2. **Rimandi solo come link nel PDF.** Il link aiuta a schermo e sparisce sulla
   carta, dove la serata si usa.
3. **Numero di pagina scritto a mano nei sorgenti.** Si rompe alla prima
   modifica di un capitolo qualunque.
4. **Numero calcolato da Typst al momento della composizione** (scelta).

## Decisione

- **Ogni arco ha due stampe.** Il booklet della serata contiene ciò che si
  gioca, con le schede intere in ogni scena (scelta di Jfs del 13/11). Il
  volume d'arco contiene i master DEF nell'ordine di gioco, con le schede in
  scena e in appendice (`"schede": "entrambe"`), l'indice di chi si incontra e
  l'indice analitico. Il primo volume d'arco è
  `07_il Portale Della Forgia Eterna/homebrew/volume-arco/ARC07-VOLUME-ARCO.manifest.json`.
  Se un volume d'arco passa le 300 pagine, si propone a Jfs su card di
  dividerlo in due tomi.
- **I rimandi portano la pagina.** La chiave di manifest `pagine_nei_rimandi`
  fa accodare all'esportatore, a ogni rimando «cap. N …» o «appendice delle
  creature/mappe, in fondo», un `#rif-pagina` che il tema risolve in «, p. 42»
  con il link. Se il bersaglio è nella stessa pagina non stampa niente. La
  chiave di capitolo `rimandi_romani` fa lo stesso per i numeri romani nudi di
  un foglio riassuntivo.
- **Il traduttore dei rimandi riconosce le forme spezzate.** Il master e la sua
  parte separati da un a capo, e «§7 di `DEF-4`», vanno al capitolo giusto.

## Conseguenze

Misure del 2026-11-19, PDF composti con la catena di stampa:

| Stampa | Pagine | Rimandi | Titolo non trovato | Con pagina | Pagina giusta |
|---|---|---|---|---|---|
| Serata, main | 130 | 107 | 8 | 0 | 0 |
| Serata, questa PR | 131 | 108 | 1 | 100 | 100 |
| Volume d'arco ARC-07 | 294 | 242 | 2 | 236 | 236 |

Il titolo non trovato rimasto nella serata è un'apertura in grassetto, non un
titolo: il rimando resta senza pagina. Nel volume d'arco i due sono quello e
«cap. III §7-bis», che il sorgente nomina e non ha.

Quello che si paga:

- una scheda alta meno di una colonna che, dopo il salto di colonna, trova
  la colonna di destra accorciata da un float va alla pagina dopo invece di
  spezzarsi a pagina girata (tema, ramo «in fondo a una colonna»). Nel volume
  d'arco toglie due schede spezzate su tre (Zog'tar e Skullcrusher) al prezzo
  di una pagina. Resta spezzata Terros, alta due colonne intere: con la scheda
  d'entrata in float sopra non sta in una pagina. Nella serata e nel
  booklet lungo toglie la scheda spezzata di Balvar, con una pagina in più. Una prima prova che decideva dalla
  posizione prima del salto di colonna non convergeva (la posizione letta era
  quella del giro di composizione precedente) ed è stata scartata;
- una figura in colonna che non entra nello spazio rimasto va a capo
  colonna da sé, con la stessa misura della scheda. Il ritratto di Vatore,
  sotto la tabella larga della Scena 9, usciva di 80 pt dal fondo del foglio
  (serata p. 71, volume d'arco p. 194; lo stesso taglio c'era su main, a
  p. 69). Nessuna misura lo vedeva: `misura_stampa.py` ha ora
  `immagini_tagliate`, con tetto 0, e su tutti i 22 booklet la misura passa da
  2 a 0. Nel Drappo e nel Giardino la stessa regola sposta quattro ritratti
  che finivano nel margine basso, accanto al numero di pagina, senza uscire
  dal foglio: una pagina in più in quattro booklet (fascicolo dei giocatori
  del Drappo 8 → 9, schede del Drappo 11 → 12, Giardino 40 → 41, Giardino
  PF1e 25 → 26). Si paga con lo spazio: a p. 71 della serata la
  colonna di destra resta bianca sotto le tabelle (circa 220 pt), perché il
  testo che segue la figura la segue anche in pagina. Un float di colonna,
  che lascerebbe al testo quello spazio, è stato provato e scartato: Typst
  0.15 lo colloca sotto le tabelle e l'immagine esce lo stesso dal foglio;
- le distanze fra dove la persona agisce e la sua scheda, nel volume d'arco,
  sono in mediana 2-8 pagine (Balvar 7, Durin 2, Skullcrusher 3,5, Terros 6,5,
  Zog'tar 8); con le schede solo alla prima apparizione erano 24 per Balvar e
  17 per Zog'tar, in 289 pagine;
- la misura `titoli_rovinati` segnala «LORDO» alle pp. 47 e 102 del volume: è
  una parola in maiuscolo nelle tabelle del tesoro dei master, non un titolo;
- la composizione di un volume con molti `#rif-pagina` richiede più iterazioni
  di layout a Typst: il volume d'arco si compone in circa 14 secondi;
- il volume d'arco porta in stampa, per la prima volta, `ARC07-DEF-5` e
  `ARC07-CONSEGUENZE-ECHI.md`: sette righe di storia del repo (date di
  approvazione, «dal 2026-10-22») sono avvolte in `<!-- storico -->` come
  vuole §4.6 di `rumblingstone-editoria`, e restano nel sorgente. Le tre note
  aperte dei master che arrivavano in stampa sono chiuse: il «(da verificare)»
  di DEF-4 sulle pergamene di Hella con la card del 19/11 (sono nella lista del
  druido, SRD 3.5), e i due «TODO» di DEF-1 §8 perché «Diventare una Collina»
  era già scritto sulla scheda dei Bracieri dal 2026-08-01 (K-B28): la nota del
  master non era stata aggiornata;
- i rimandi a un file che non sta nel volume restano come nome di file, come
  negli altri booklet del repo (uno nel booklet lungo da 162 pagine).

Per tornare indietro basta togliere `pagine_nei_rimandi` dal manifest: il
testo resta identico, senza i numeri di pagina.
