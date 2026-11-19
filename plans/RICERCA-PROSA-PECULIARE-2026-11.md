# RICERCA · Le tecniche di prosa proprie del repo, messe accanto a Paizo, Wizards e alla community

**Data**: 2026-11-19 · **Richiesta del DM** (thread «Valutare le tecniche di
prosa del repo»): vedere se lo standard della prosa di gioco si allinea a
quello di Paizo e Wizards e alle buone pratiche della community, quanto se ne
discosta, e se gli scostamenti sono abbastanza propri del repo da entrare
nello standard editoriale come sue caratteristiche. Il criterio del DM:
*le differenze entrano soltanto se sono peculiari e ovviamente migliorative*,
e devono rendere il gioco più profondo e adatto a giocatori adulti senza
appesantirlo.

**Stato**: ✅ ricerca completa; scelte del DM al §8, due ancora aperte.
**Vincoli già fissati**: la prosa migliora solo se il DM la sceglie alla
cieca ([ADR-0093](adr/ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md));
niente cancelli di prosa nuovi (MS-0028); i box votati sono congelati
(`CONGELATI.json`).

---

## 0 · Prima di leggere

**Cosa manca per una risposta migliore.**

1. Un giudizio del tavolo sulla prosa. Su `main` c'è un solo resoconto di
   sessione, e il ramo della partita è fermo al 25/09: nessuna tecnica è
   misurata sui giocatori, solo sul DM che legge alla cieca.
2. Un editore professionale italiano nel corpus. Need Games e Isola Illyon
   sono fuori dalla rete dell'ambiente; il riferimento italiano è fatto di
   un'associazione da torneo (Gruppo Chimera) e della community (Dragons'
   Lair).
3. Il testo delle AP Paizo migliori. Il corpus inglese sono i dieci moduli
   gratuiti del Free RPG Day, livelli 1-6, un terzo umoristici.

**Assunzioni.** Il lettore che conta è il DM che legge ad alta voce a
quattro adulti che leggono fantasy da vent'anni. «Peculiare» vuol dire che
la tecnica non c'è nelle linee guida di *Dungeon*, nelle guide di stile
Paizo e WotC lette in [RICERCA-STANDARD-PROSA-WOTC-PAIZO](RICERCA-STANDARD-PROSA-WOTC-PAIZO-2026-09.md)
e nelle pratiche della community lette in
[RICERCA-AVVENTURE-COMMUNITY](RICERCA-AVVENTURE-COMMUNITY-2026-10.md), oppure
che il repo la porta dove quelle fonti non arrivano. «Ovviamente migliorativa»
vuol dire che ha vinto nei voti ciechi del DM con un margine che non si
spiega col caso, o che corregge un difetto che il tavolo ha già pagato.

## 1 · La risposta breve

Lo standard è **allineato alle case in quasi tutto ciò che è regola di
mestiere**: il box che non decide per il giocatore, il box di luogo senza
creature, le misure fuori dalla voce narrante, le tattiche prima, durante e
morale, i tre indizi, il corsivo degli incantesimi, il foglio di stile.

È **peculiare in una dozzina di punti**. Di questi, solo due hanno una prova
che regge il criterio del DM, ed entrambi vanno *contro* il consiglio delle
fonti: quando il tetto di lunghezza e i dettagli sensoriali si scontrano
vincono i sensi (5 voti su 5), e la frase che chiude con enfasi non si toglie
(4 su 4). Sono le candidate a diventare caratteristiche del repo.

Il resto delle peculiarità non è provato: la regia dei round a micro-box per
attore, «Che fate?» in fondo al box, la quarta colonna, i tetti per tipo di
box, il monologo in blocco (2 su 2, troppo pochi). Restano come convenzioni
della casa, senza il titolo di caratteristica.

Poi ci sono **scostamenti che nessuno ha scelto**, e la misura dice che il
repo scrive diverso dalle case senza una prova che sia meglio: frasi più
corte (11-15 parole contro 16-18), avverbi in -mente e gerundi quasi a zero
contro una fascia umana stabile, e in ARC-08 il calo è avvenuto fra ottobre e
oggi. Il repo stesso, in `italiano-nativo.md` §4, chiede il contrario
(«l'italiano respira più lungo»), e nei voti ciechi la versione con più
subordinate vince 11 volte su 12. Qui va riallineato, con un cieco prima di
toccare i box che ci sono.

Infine due incoerenze interne, che non sono scelte: la checklist chiede
ancora di togliere «la frase che spiega» l'ultima immagine, contro la regola
nata dal voto; e il booklet della serata stampa al tavolo le etichette dei
pilastri («Andor lead», «PILASTRO GOT»), che servono a chi scrive.

Sul peso al tavolo: i box sono il **5,6% delle parole** dei master di ARC-07
(7.963 su 143.303). La lunghezza del booklet, che il DM sente, non viene
dalla prosa letta ad alta voce.

## 2 · Metodo e fonti

- Le norme del repo: `skills/rumblingstone-narrative-style/references/`
  (letti per intero `read-aloud-adulti.md`, `editorial-standards.md`, le
  sezioni pertinenti di `italiano-nativo.md`), il registro delle norme, gli
  ADR citati.
- Le case: [RICERCA-STANDARD-PROSA-WOTC-PAIZO](RICERCA-STANDARD-PROSA-WOTC-PAIZO-2026-09.md)
  (*Dungeon*, guide di stile Paizo e WotC, Merwin su D&D Beyond),
  [RICERCA-AVVENTURE-COMMUNITY](RICERCA-AVVENTURE-COMMUNITY-2026-10.md) e le
  note di ricerca nella cartella privata del progetto (Alexandrian, Bryce
  Lynch, Raging Swan, Necromancer, PFS, RPG Superstar, Gruppo Chimera).
- Il corpus: 2.335 box italiani (Gruppo Chimera e Dragons' Lair) e 118
  inglesi (Paizo, Free RPG Day), estratti dai PDF dell'editore
  ([note-prosa-corpus](esperimenti/avventure-community/note-prosa-corpus.md)).
  I testi restano nella cartella privata; qui solo numeri.
- La misura di oggi: lo script del corpus (`misura_corpus.py`, cartella
  privata) rilanciato su `main` del 19/11 (e5339cee), con gli stessi
  rilevatori di `misura_craft.py` sui due lati.
- La prova: i voti ciechi del DM già dati (giro 2 del 18/10, 16 coppie;
  giro 3 del 19/10, 9; prova del 21/10, 13; riscrittura del 22/10, 14;
  pipeline del 23/10, 6) e le regole che ne sono uscite in
  `read-aloud-adulti.md` §2-ter.

## 3 · Le tecniche, una per una

### 3.1 · Allineate alle case (non sono peculiari)

| Tecnica nel repo | Fonte della casa | Nota |
|---|---|---|
| il box non decide per il giocatore (P1: niente «vedete», «entrate») | linee guida di *Dungeon* | il repo esenta visioni d'artefatto ed echi per un PG, dove la seconda persona è giusta |
| box di luogo di poche frasi, senza le creature | *Dungeon* | |
| niente «sembra», «pare» | Merwin, D&D Beyond | il confine della smentita («sembrava… è») è un'aggiunta del repo |
| misure nei Dati per il DM, scala per paragone nel box (ADR-0014) | *Dungeon*, «descrizione generale»; prassi delle AP | la vecchia scuola mette i piedi nella prima frase; le AP no |
| tattiche prima, durante, morale | AP Paizo | |
| almeno tre indizi per conclusione | Alexandrian, adottata da entrambi | |
| incantesimi in corsivo e minuscolo, caratteristiche in forma meccanica | guide WotC e Paizo | ADR-0060 |
| foglio di stile eseguibile | prassi del copyeditor, WotC | ADR-0078 |
| niente parentesi nel box | prassi: 2% dei box Paizo, 5-7% degli italiani | il repo è più severo, e ARC-08 (7%) e ARC-09 (10%) non la rispettano |
| *d* eufonica, possessivo tolto su corpo e cose addosso | norma dell'italiano editoriale | ADR-0120; D5 di MS-0036 |

### 3.2 · Peculiari, con una prova che regge

| Tecnica | Dove | Contro chi va | Prova |
|---|---|---|---|
| **i sensi battono il tetto di lunghezza**: una riscrittura non toglie luce, colore, suono, caldo, freddo, il corpo che sente | `read-aloud-adulti.md` §2-ter, regola 1 | *Dungeon* («poche frasi»), Merwin («niente dettagli superflui»), Bryce Lynch | 5 su 5 nel giro 2: ogni volta che la versione nuova toglieva 13-54 parole di sensi, il DM ha scelto la vecchia. I box che ha scelto stanno al 47% oltre le quattro frasi, contro il 15-25% delle case |
| **la chiusa enfatica resta**: la frase che nomina la meraviglia o l'eroe in fondo al box non si taglia | `read-aloud-adulti.md` §2-ter, regola 3 | LAMP («spiega»), la regola della reticenza del repo stesso | 4 su 4 nella riscrittura del 22/10 (B09, B10, B14, B16) |

Per un pubblico adulto sono coerenti col resto dello standard: il DM premia
il mondo che si sente e la chiusa da tavolo alla Mercer, e punisce i tagli
fatti per stare sotto un numero. Nessuna delle due aggiunge parole al gioco:
impediscono di toglierne.

### 3.3 · Peculiari, senza prova

| Tecnica | Dove | Cosa porta, in ipotesi | Perché non basta |
|---|---|---|---|
| un solo nome proprio **nuovo** per box, al più due livelli di subordinate | `read-aloud-adulti.md` §1 | il box si ascolta e non si rilegge | nessun voto l'ha isolata. Il corpus le dà ragione sui box d'area (0,3-1,9 maiuscole interne per box), ma è una conferma di forma, non di resa |
| tetti per tipo di box (round 2-4 righe, rivelazione 4-6, micro-box per PG 2-3) | §2 | ritmo al tavolo | nessun voto; il corpus non distingue i tipi |
| **regia dei round**: un micro-box per attore e una riga d'esito per riuscita e fallimento | ADR-0014, `editorial-standards.md` §2 | i dadi non spengono la scena | è la tecnica che più rischia di appesantire, e non è mai stata provata contro la sola tattica in prosa delle AP |
| il box di combattimento chiude su «Che fate?» | ADR-0014 | il box si ferma prima dell'azione | 16-18% dei box di ARC-07, ARC-08 e del Drappo chiude con una domanda, contro il 2-5% delle case. È la cosa che il DM dice comunque; stamparla costa poco e non è provata |
| **la quarta colonna**, «Cosa NON dire» in fondo alla scheda dei sensi | ADR-0057 | il DM non racconta la scoperta descrivendo l'atmosfera | strumento per il DM e non prosa letta; nessun riscontro dal tavolo. 34 occorrenze in 15 file |
| il monologo resta un blocco | §2-ter, regola 2 | la voce del PNG non si spezza | 2 su 2: va nella direzione giusta, ma due coppie non fanno una prova |
| il dettaglio che non serve a niente, la competenza concreta, il registro alto una volta per scena | §3 e §5 | profondità per lettori adulti | Raging Swan chiede il contrario («ogni dettaglio giocabile»). Nessun voto li ha isolati; la regola 1 li protegge di riflesso |
| nove pilastri con un lead e al più due support per scena, etichetta sul box | `style-pillars.md`, `editorial-standards.md` §2 | una voce sola fra molti autori e agenti | è un attrezzo di scrittura. Al tavolo arriva solo come etichetta stampata (§3.5) |
| dialogo nella forma `**NOME (tono):** «battuta»` | `editorial-standards.md` §2 | il DM sa come recitarla | utile al DM, 178 battute nella forma; nessuna misura di resa |

Le idee di struttura (echi a distanza, protagonismo dei PG, varietà fra gli
archi, le sei porte dell'indagine) sono la parte più peculiare del repo, e la
più vicina al criterio «più profondo per adulti». Non sono prosa del box e
non pesano sul testo letto: si giudicano al tavolo, e il tavolo non ha ancora
un resoconto su `main`.

### 3.4 · Scostamenti senza una scelta dietro

Box descrittivi, stessi rilevatori sui due lati, `main` del 19/11.

| | Paizo EN | Chimera IT | Dragons' Lair IT | ARC-07 DEF | ARC-08 | ARC-09 | Drappo |
|---|---:|---:|---:|---:|---:|---:|---:|
| box | 111 | 1.102 | 270 | 114 | 104 | 89 | 17 |
| parole, mediana (IQR) | 52 (33-80) | 41 (27-67) | 40 (24-68) | 62 (46-86) | 64 (54-75) | 40 (25-77) | 67 (35-88) |
| parole per frase, mediana | 18 | 17 | 16 | 14 | 15 | 12 | 11 |
| oltre 4 frasi | 25% | 15% | 19% | 47% | 30% | 33% | 65% |
| oltre 500 caratteri | 23% | 17% | 21% | 20% | 11% | 15% | 18% |
| con parentesi | 2% | 5% | 7% | 0% | 7% | 10% | 0% |
| seconda persona | 9% | 25% | 30% | 22% | 13% | 27% | 29% |
| chiude con una domanda | 2% | 5% | 5% | 18% | 16% | 6% | 18% |
| gerundio in coda ‰ (-ing) | 3,5 | 2,2 | 1,2 | 0,0 | 1,0 | 0,2 | 0,0 |
| -mente ‰ (-ly) | 12,6 | 5,9 | 8,3 | 0,7 | 2,7 | 1,3 | 0,0 |

Cosa dice, con la cautela dovuta:

1. **Le frasi sono corte ovunque nel repo**, da 11 a 15 parole contro 16-18
   delle tre case. La norma del repo chiede il contrario (`italiano-nativo.md`
   §4: periodi lunghi, poi la frase corta che chiude), e nei voti già dati la
   versione con più subordinate vince 11 su 12. La frase breve in serie è
   anche il ritmo tipico del testo generato. È uno scostamento che nessuna
   regola ha chiesto.
2. **-mente e gerundio in coda vanno a zero**, e scendono col tempo: ARC-08
   era a 5,8‰ e 1,6‰ il 23/10, oggi è a 2,7‰ e 1,0‰. La fascia umana
   italiana regge su sedici titoli (-mente 4,0-14,6‰, gerundio 0,6-3,8‰,
   MS-0016). I rilevatori dei tic dell'IA li hanno tolti dove erano tic, e
   anche dove erano italiano normale; `misura_craft --stile` lo segnala già
   con le fasce, senza che nessuno agisca.
3. **I box sono più lunghi e più regolari** in ARC-07 e ARC-08 (mediana
   62-64 parole contro 40-52; IQR di ARC-08 largo 21 parole contro 40-47).
   ARC-09 è dentro le case. Per ARC-07 la lunghezza in più è quella scelta
   alla cieca (§3.2), quindi non va toccata.
4. **Le parentesi** in ARC-08 e ARC-09 violano una norma del repo che le case
   rispettano quasi: è un difetto, non una scelta.

### 3.5 · Due incoerenze interne

- **La checklist contraddice il voto.** `read-aloud-adulti.md` §7 e
  `italiano-nativo.md` §8 chiedono ancora «Ho tolto la frase che spiega
  l'ultima immagine?». La regola 3 del §2-ter, nata dal voto del 22/10, dice
  di non togliere la chiusa. Chi scrive segue la checklist, che è l'ultima
  cosa che legge. La regola 3 inoltre non è nel registro delle norme, come
  chiede G3.
- **Le etichette dei pilastri arrivano al tavolo.** Il booklet della serata
  v4.1 stampa 18 intestazioni «Read-aloud (Andor lead)» e simili, e 24
  richiami di pilastro in tutto, fra cui «IL GRIGIO… (PILASTRO GOT)». La
  norma che le vuole (registro, riga «Read-aloud (pilastro lead)»,
  **maggiore**) serve all'agente che continua la scena. Nessuna casa stampa
  metadati di redazione nel libro del DM.

## 4 · Cosa portano al gioco, e quanto pesano

Il criterio del DM chiede due cose: più profondità per adulti, nessun peso
in più. Sul peso la misura è netta: i box di ARC-07 sono 7.963 parole su
143.303 dei cinque master, il 5,6%. La serata di 132 pagine e 80.000 parole
pesa per le schede, la regia, le tattiche e le copie (MS-0085 e seguenti),
non per la prosa letta. Le due caratteristiche del §3.2 non aggiungono una
riga: vietano di tagliare.

Sulla profondità, l'unica misura che c'è è il DM alla cieca, e dice due cose
sole con forza: sensi e chiusa. Tutto il resto del giudizio «rende il gioco
più profondo» è un'ipotesi del repo, plausibile e non misurata.

## 5 · Decisione proposta, in forma di ADR breve

**Contesto.** Il DM vuole che lo standard editoriale nomini le tecniche
proprie del repo, a condizione che siano peculiari e migliorative. Il repo ha
molte norme proprie e due sole con una prova.

**Decisione proposta.**

1. Lo standard editoriale apre una sezione «Le scelte proprie» con le due
   tecniche del §3.2, ciascuna con la fonte che contraddice e la prova.
2. Le tecniche del §3.3 restano dove sono, come convenzioni della casa, e
   diventano candidate solo dopo un cieco che le isoli.
3. La checklist si allinea alla regola 3 del §2-ter, e la regola entra nel
   registro.
4. Il ritmo della frase si riallinea alle case nei testi nuovi; nei testi che
   ci sono, solo dopo un cieco (§6).
5. Le etichette dei pilastri restano nel sorgente e si tolgono in stampa.

**Conseguenze.** Lo standard dice cosa del repo è provato e cosa no, e la
differenza resta visibile. Nessun cancello nuovo. Il prezzo: un giro di cieco
per ogni tecnica che si vuole promuovere, cioè tempo del DM; e una modifica
al renderer dei booklet, che tocca il lavoro sulla struttura del volume.

## 6 · Piano in tre fasi

**Audit (fatto in questa ricerca).** Inventario delle norme, confronto con le
case, misura di oggi contro il corpus, lettura dei voti già dati.

**Sviluppo.**

1. Checklist allineata e regola 3 nel registro (nessuna scelta da fare: la
   decisione nuova supera quella vecchia e il voto lo misura).
2. Dopo la scelta del DM: la sezione «Le scelte proprie» in
   `editorial-standards.md`, registrata come chiede G3.
3. Il primo cieco di ablazione sulla tecnica scelta dal DM: otto box non
   congelati, in due versioni che differiscono **solo** per quella tecnica,
   più quattro coppie di controllo, con `cieco_versioni.py`.
4. Dopo la scelta del DM e d'accordo con chi tiene la struttura del volume:
   le etichette tolte in stampa.

**Validazione.**

- Per promuovere una tecnica a caratteristica: almeno 7 coppie su 8 al
  cieco, o la soglia riproporzionata di ADR-0093, e i controlli confermati.
- Per il ritmo: dopo il riallineamento, parole per frase dentro 16-18 e
  -mente e gerundio dentro la fascia, senza perdere al cieco.
- Per la stampa: zero etichette di pilastro nel testo del PDF
  (`pdftotext | grep -ci pilastro`), e le stesse etichette ancora nel
  sorgente (il congegno di `misura_craft` non scende).
- Cosa questa validazione non dirà: se il tavolo si diverte di più. Lo dice
  il debrief della serata.

## 7 · Limiti

- I voti sono di un solo lettore, il DM, su coppie di riscritture leggere: la
  potenza è bassa, e per questo solo le regole con quattro o cinque casi su
  quattro o cinque sono trattate come prova.
- Le case misurate sono i moduli gratuiti, non le AP che la community
  ricorda. Descrivono la prosa corrente e capace, non la migliore.
- Le maiuscole interne sono un limite superiore dei nomi propri, non il
  conto dei nomi nuovi.
- I confini dei box italiani del corpus sono sbagliati in circa un caso su
  sette: le lunghezze sono approssimate, i tassi per mille no.

## 8 · Le scelte del DM (card del 2026-11-19)

| Card | Scelta |
|---|---|
| tecnica 1, i sensi battono il tetto di lunghezza | **entra come caratteristica** (`editorial-standards.md` §4-bis) |
| tecnica 2, la chiusa enfatica resta | **entra come caratteristica**; la checklist di `read-aloud-adulti.md` §7 e di `italiano-nativo.md` §8 è allineata, la regola è nel registro |
| tecnica 4, voce per l'orecchio | **prima un cieco**: nomi nuovi in più o in meno, senza toccare i nomi già noti al tavolo |
| etichette dei pilastri nella stampa | **tolte in tutte le stampe**, tenute nel sorgente; il filtro nel renderer lo fa il lavoro sui booklet |
| tecnica 3 (monologo) e ordine dei cieco A, B, C | aperte |

Per i cieco, le regole che il DM ha chiesto di scrivere perché il voto non sia
falsato: una sola cosa cambia per coppia; le due versioni sono entrambe
riscritte (mai l'originale contro la nuova, che si riconosce); ordine con un
seme; nessun segno di quale sia la versione del repo (stesse virgolette,
corsivo, lunghezza entro il 10%); niente box congelati né della serata in
corso; quattro coppie di controllo; chiave chiusa fino al voto. Per il ritmo
l'ultima frase resta identica e i periodi non superano due subordinate; per la
regia dei round il cieco puro è debole (il formato si riconosce) e va
affiancato da una prova cronometrata; per «Che fate?» servono 12 coppie.

## Come si rifà

```
python3 -I <corpus-prosa>/script/misura_corpus.py --repo . \
  --box <corpus-prosa>/grezzi/box-tutti-2026-10-23 \
  --config <corpus-prosa>/script/config-tutti-2026-10-23.tsv \
  --bersaglio "ARC07-DEF=.:07_il Portale Della Forgia Eterna/ARC07-DEF-*.md" \
  --bersaglio "ARC08=.:08_La Battaglia Di Hammerfist/ARC08-*.md" \
  --bersaglio "ARC09=.:09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/*.md" \
  --bersaglio "Drappo=.:10-stand-alone/Il-Drappo-di-Tarsilia/**/*.md" --out <cartella>
cat "07_il Portale Della Forgia Eterna/"ARC07-DEF-*.md | wc -w
pdftotext ARC07-NOTTE-E-ALBA-SERATA-v4.1-venerdi-132pp.pdf - | grep -c "Read-aloud ("
```

`<corpus-prosa>` è la cartella privata del progetto: il corpus non entra nel
repo.
