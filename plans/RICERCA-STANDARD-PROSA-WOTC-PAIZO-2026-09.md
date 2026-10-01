# RICERCA — Gli standard di prosa di WotC e Paizo, e quali sono misurabili

> **Cos'è**: cosa prescrivono davvero i due editori di riferimento sulla
> **prosa e sui contenuti** di un'avventura, quali di quelle prescrizioni si
> possono trasformare in un **controllo eseguibile**, e a che punto sta il
> repo su ciascuna — misurato, non stimato.
>
> **Stato**: ✅ ricerca completa (2026-09-19) · **Alimenta**:
> [PIANO-MISURA-EDITORIALE-STANDARD](PIANO-MISURA-EDITORIALE-STANDARD.md) §F1.1
> **Gemella di**: la ricerca su impaginazione e resa grafica (da aprire)

---

## 1 · Le prescrizioni, con la fonte

### 1.1 · Il read-aloud — *Dungeon* (Paizo)

Le linee guida ufficiali di *Dungeon* dicono due cose in forma verificabile:

1. il read-aloud **non fa riferimento a chi guarda**;
2. si evitano *«vedi»*, *«appena entri nella stanza»*, e **qualunque frase che
   presupponga un'azione del giocatore**.

La ragione non è di gusto: il box che dice *«entri e senti paura»* decide al
posto del giocatore due cose che sono sue — che sia entrato, e cosa prova.

### 1.2 · Corsivo e maiuscole — WotC e Paizo, concordi

- **Incantesimi e oggetti magici vanno in corsivo**, e in **minuscolo** quando
  non contengono un nome proprio.
- Vanno invece **maiuscole** le caratteristiche (Forza, Destrezza), le abilità
  (Acrobazia), i talenti (Tiro Ravvicinato), le scuole (Necromanzia), le
  lingue (Comune) e le taglie (Media).
- Paizo aggiunge: **nessun trattamento speciale** per classi, razze, privilegi
  di classe, mostri e equipaggiamento comune — e il livello si scrive
  *«personaggio di 11° livello»*, non *«un 11°-livello personaggio»*.

### 1.3 · La rete degli indizi — la regola dei tre indizi

Fuori dai due editori ma adottata da entrambi gli ambienti: **per ogni
conclusione che vuoi che i PG raggiungano, metti almeno tre indizi**. Il
motivo è dichiarato e riguarda il tavolo, non l'eleganza: con meno di tre, è
del tutto possibile che il gruppo ne manchi uno e che il gioco si fermi.

### 1.4 · Il box e l'area chiave — *Dungeon*, riletto il 2026-10-01

Riletto sulla fonte per verificare il testo del §1.5. Le linee guida dicono,
oltre al §1.1:

1. il read-aloud *«should only rarely run more than a few sentences»*; i testi
   lunghi vanno in un **handout**;
2. il read-aloud **non descrive le creature** presenti, perché posizione e
   attività dipendono da come arrivano i PG;
3. un incontro ha queste voci, tutte facoltative salvo l'EL nell'intestazione:
   **Read-aloud**, **Descrizione generale** (effetti, scopo della stanza, le
   statistiche degli oggetti che probabilmente si romperanno), **Creature**,
   **Tattiche**, **Trappole**, **Tesoro**, **Sviluppo** (chi sente lo scontro,
   quando i nemici si arrendono o fuggono, come l'incontro cambia dopo),
   **Aggiustamento PX ad hoc**;
4. gli oggetti hanno una riga fissa: spessore, Durezza, pf, CD per rompere;
5. nella descrizione generale di un'avventura si dice come sono illuminati i
   luoghi e che porte prevalgono: è testo **per il DM**, non un box.

Applicato in `read-aloud-adulti.md` §2-bis (1, 2) e in
`rumblingstone-module-standard` §7 (3, 4).

### 1.5 · Il testo portato dal DM il 2026-10-01: cosa ha una fonte

Il DM ha portato un testo che descrive *«gli standard editoriali»* di WotC e
Paizo per il boxed text e l'introduzione di sezione, con un modello di stanza
e uno statblock d'esempio. Verificato punto per punto:

| Affermazione | Esito | Dove va |
|---|---|---|
| box di stanza in **3-4 frasi** | 🟢 coerente con *Dungeon* («poche frasi») | `read-aloud-adulti.md` §2-bis; misurato da `misura_craft --box`, colonna `>4 frasi` |
| box di stanza in **300-500 caratteri** | ⚠️ **nessuna fonte**: *Dungeon* conta frasi, non caratteri | indicatore `>500 car`, decisione del DM (PIANO-BOX-DI-LUOGO-E-AREA-CHIAVE, D1) |
| introduzione di sezione in **800-1.200 caratteri**, letta una volta | ⚠️ nessuna fonte; *Dungeon* mette illuminazione e porte in un testo **per il DM** | il repo ce l'ha già: è l'**apertura di scena** di 8-12 righe (`read-aloud-adulti.md` §2) |
| niente reazioni o emozioni presunte dei PG | 🟢 è il §1.1, già norma | P1, `misura_craft --p1` |
| il box si ferma prima dell'azione | 🟢 il repo ce l'ha già | congegno «chiusura su decision point», «Che fate?» |
| ordine: spazio e luce → arredo → dettaglio strano | 🟡 nessuna fonte primaria, è pratica di mestiere | `read-aloud-adulti.md` §2-bis, come forma consigliata |
| la **prima frase dà le dimensioni** («quaranta piedi») | 🔴 **in conflitto con ADR-0014** (niente metrature nella voce narrante) | decisione del DM (PIANO-BOX-DI-LUOGO-E-AREA-CHIAVE, D2); nel frattempo vale ADR-0014, e le misure vanno nei Dati per il DM |
| caratteristiche della stanza fuori dal box (lato, pareti, porta con CD, Durezza, pf) | 🟢 è la «descrizione generale» di *Dungeon* | `module-standard` §7, l'area chiave |
| lo statblock delle **ombre** | 🔴 **sbagliato in tutti e due i sistemi**, vedi sotto | non si usa: gli statblocchi vengono dal Bestiario |
| «usa il template 3.5 o quello PF1e» | ⚪ già deciso | la campagna gira su 3.5; il Drappo su PF1e |

🔴 **Lo statblock d'esempio mescola 3.5 e PF1e e sbaglia in entrambi.**
Confrontato con [d20srd.org](https://www.d20srd.org/srd/monsters/shadow.htm) e
[Archives of Nethys](https://aonprd.com/MonsterDisplay.aspx?ItemName=Shadow):

| Voce | Nel testo | SRD 3.5 | PF1e (Bestiary p. 245) |
|---|---|---|---|
| GS | 2 | 3 | 3 |
| pagina | 218 | — | 245 |
| CA | 15, contatto 15, impreparato 12 (+3 deviazione, +2 Des) | 13, contatto 13, impreparato 11 (+2 Des, +1 deviazione) | 15, contatto 15, impreparato 12 (+2 deviazione, +2 Des, +1 schivare) |
| TS | Tem +1, Rif +3, Vol +4 | **Tem +1, Rif +3, Vol +4** | Tem +3, Rif +3, Vol +4 |
| DMC / BMC | 15 / — | (non esiste) | 17 / +4 |
| tocco | +4 | +3 | +4 |
| talenti | «Furtività Rapida» | Allerta, Schivare | Schivare, Abilità Focalizzata (Percezione) |

I tiri salvezza sono quelli della 3.5, il resto è PF1e con errori. È il motivo
per cui `AGENTS.md` dice *«non inventare mai blocchi statistiche»*: uno
statblock scritto a memoria sembra giusto e non lo è. Anche le abilità del
modello (Percezione, Furtività, Conoscenze (Nobiltà)) sono PF1e: in un master
3.5 le segnala già `domande_developer.py` (D6-5E).

**Misurato sui box del repo** (estrattore `box_read_aloud`, 501 box nei file di
gioco): mediana **347 caratteri**; **122 (24%) oltre i 500**, 28 oltre gli 800.
Sui master DEF di ARC-07: 104 box, mediana fra 315 e 466 caratteri per master,
**27 oltre i 500** e **61 oltre le quattro frasi**. Lo stand-alone
dell'Abbazia, che è il banco del repo, ha 11 box: **zero** oltre i 500, uno
oltre le quattro frasi.

**Creature nel box di luogo: nessun rilevatore affidabile.** Con i 322 nomi del
registro, **315 box su 501 (63%)** contengono almeno un nome, ma il registro
comprende dei, PG, artefatti e parole come «Eterna»: il numero misura il
registro, non la norma. Per misurarla davvero ogni box dovrebbe dichiarare il
suo tipo (di luogo, d'ingresso, di round), e oggi nessuno lo fa.

---

## 2 · Quali diventano un controllo, e a che punto siamo

Ogni riga è stata **misurata sul repo oggi**, sui soli file di gioco
(archi, `Bestiario/`, `PG/`, standalone — non i piani, non `AGENTS.md`).

| # | Norma | Severità proposta | Stato misurato |
|---|---|---|---|
| **P1** | read-aloud che presuppone un'azione del giocatore | **minore** | 🔴 **229 box su 1.334 = 17%** (143 ARC-07 · 53 ARC-09 · 22 ARC-08 · 11 ARC-06) |
| **P2** | incantesimi in corsivo | **minore** | 🟡 **209 su 344 = 61%** a norma; **135 nude = 39%**. I più frequenti: *dispel magic* 16, *palla di fuoco* 15, *divine power* 9, *mind blank* 8 |
| **P3** | incantesimi in minuscolo a metà frase | **minore** | 🟢 **14 occorrenze** in tutto il repo di gioco |
| **P4** | regola dei tre indizi | **maggiore** | ⚠️ **3 file dichiarano un'indagine in un titolo, e tutti e tre risultano a 0 nodi** — ma vedi §4: il numero è sospetto, e non è colpa dei documenti |

⚠️ **P1 nasce minore, non maggiore, e la ragione va scritta.** Una parte delle
229 sono **visioni d'artefatto** — la Corona che parla al suo portatore, dove
la seconda persona è la scelta giusta. La norma entra con un'**esenzione
dichiarata** per quel contesto: 229 correzioni fatte a macchina farebbero più
danno della violazione.

---

## 3 · Cosa NON diventa un controllo, e perché dirlo

- **«La prosa è bella».** Nessuna di queste norme lo misura. Sono tutte
  conformità a specifiche (ISO 5060), e un testo a punteggio pieno può essere
  noioso. Resta il collaudo al tavolo.
- 🔴 ~~**Le maiuscole di caratteristiche e abilità** (§1.2). In italiano la
  convenzione WotC non si trasferisce pulita: *Forza* è anche un sostantivo
  comune, e un rilevatore darebbe più falsi positivi che errori.~~
  **Ritirata il 2026-09-20: vedi §3-bis.** Era vera del rilevatore che avevo in
  mente, e falsa della norma.
- **Il conteggio parole per sezione.** Le guide Paizo lo fissano per i loro
  formati; qui i formati sono altri, e importare un numero altrui sarebbe
  l'errore di taratura già documentato con Gulpease.

---

## 3-bis · 🔴 Una previsione sbagliata, e la misura che la corregge

Il DM, il giorno dopo la pubblicazione:

> *«se compaiono nello statblock di un PNG o mostro sono seguiti da un numero,
> come ad esempio* Forza 25*; nel caso di prove non dovrebbe essere nella forma
> simile a* prova di Forza CD 25*? In questo modo è più facile distinguerli?
> Puoi verificare se apporta dei miglioramenti misurandoli?»*

Verificato, e l'obiezione è fondata. **Non si cerca la parola: si cerca la
forma meccanica**, che un sostantivo comune non ha mai.

| | Occorrenze nei 511 file di gioco | Fuori norma | Falsi positivi, contati a mano |
|---|---|---|---|
| il matcher nudo, quello che avevo in mente | **2.014** | — | inutilizzabile |
| **F1** caratteristica + punteggio (`Forza 25`) | 1 | 0 | 0 |
| **F2** abilità + modificatore, **nessuno spazio dopo il segno** (`Nuotare +9`) | 213 | 0 | 0 |
| **F3** `prova/tiro/TS di X` con una **CD sulla stessa riga** | 38 | 2 | 0 |
| **F4** `bonus/modificatore di X` | 6 | 1 | 0 |
| **le quattro forme insieme** | **258** | **3** | **0** |

🔎 **Tre cose che solo la misura poteva dire, e nessuna era prevedibile.**

- **F1 trova una sola occorrenza**, perché questo repo scrive le caratteristiche
  **in sigla**: `For 25`, `Des 14`, **688** volte. La forma nominata dal DM è
  giusta, il repo la applica già, in un'altra grafia.
- **F2 ha dovuto vietare lo spazio dopo il segno.** Scritta larga catturava
  *«40.500 mo in oggetti di artigianato + 1 Sacrificio Personale»*: tre falsi
  positivi su tre, azzerati dalla stretta senza perdere un caso vero.
- **`intuizione` è stata tolta dall'elenco delle abilità, e l'ha trovata il
  cancello stesso.** Col lemma dentro, il conto saliva da 3 a **25**, e le
  ventidue in più erano *«bonus di intuizione +4»* — in 3.5 un **tipo di
  bonus**, non l'abilità, che è *Percepire Intenzioni*. È il quindicesimo caso
  della famiglia «un criterio largo si inventa copertura», e il primo trovato
  **prima** del commit invece che in una PR dopo.

Il controllo è `validate_prosa.py --caratteristiche`, la decisione è
[ADR-0060](adr/ADR-0060-la-forma-rende-misurabile-cio-che-la-parola-non-distingue.md),
le tre violazioni sono corrette e la soglia è **zero**.

> **La regola che ne esce**, e vale oltre questo caso: prima di dichiarare non
> misurabile una norma su un termine ambiguo, **cerca la forma**. Poi, se la
> forma non c'è, scrivilo — ma scrivilo dopo averla cercata.

---

## 4 · 🔴 Il metodo, e sei matcher rotti in una sessione

Questa ricerca ha prodotto **sei** misure sbagliate prima di produrne una
giusta, e la cosa va scritta perché è la stessa famiglia di difetto ogni
volta: **un criterio troppo largo si inventa copertura**.

| Misura sbagliata | Cosa la rompeva | Numero falso → vero |
|---|---|---|
| sovrapposizione fra skill | la virgola fra due trigger contava come trigger | 82 coppie → **5** |
| incantesimi in corsivo | «web» catturava *web enhancement* e la cartella `web/` | 80% fuori norma → **39%** |
| regola dei tre indizi | «caso» è italiano comune (*«in caso di»*) | 55 indagini → **3** |

E il quarto, che è il più insidioso: il rilevatore di **P4** che ho scritto qui
è **un secondo rilevatore** per una norma che `misura_craft` già presidia con
il suo congegno `nodo d'indizio`. Due tabelle per la stessa cosa è
esattamente il difetto che ADR-0048 descrive sulla legenda. Gli zeri di P4
probabilmente misurano **il disaccordo fra i due rilevatori**, non l'assenza
dei nodi.

> **Regola che ne esce, per il piano**: *una norma, un rilevatore*. Se una
> norma è già misurata da uno strumento, il nuovo controllo lo **riusa**;
> non ne scrive un secondo. Entra come criterio di F1.3.

E la regola generale, la stessa da tre giorni: **un numero senza il suo
matcher verificato all'indietro non è una misura, è un'impressione con le
cifre decimali.**

---

## 5 · Cosa alimenta

| Va in | Cosa |
|---|---|
| `PIANO-MISURA-EDITORIALE-STANDARD` F1.1 | P1-P4 come righe della tipologia, con la severità |
| `PIANO-MISURA-EDITORIALE-STANDARD` F1.3 | il criterio **una norma, un rilevatore** |
| `skills/REGISTRO-NORME-EDITORIALI.md` | le quattro norme nuove + le due **non misurate con la ragione scritta** (§3) |
| `skills/rumblingstone-narrative-style/references/read-aloud-adulti.md` | P1: la norma *Dungeon* non era scritta da nessuna parte nel repo |
| Decisione DM | cosa fare dei 229 box di P1 |

---

## Fonti

[Dungeon writers' guidelines](https://paizo.com/writersguidelines/dungeon_writer_guidelines.pdf) ·
[Dragon writers' guidelines](https://paizo.com/writersguidelines/dragon_writers_guidelines.pdf) ·
[Pathfinder Style Guide (Owen K.C. Stephens)](https://www.enworld.org/threads/pathfinder-style-guide-by-owen-stephens.353691/) ·
[D&D: quando corsivo e quando maiuscolo](https://www.dandwiki.com/wiki/Help:When_to_Italicize_and_Capitalize) ·
[D&D 5E Writer's Guide](https://olddungeonmaster.com/2015/08/03/5e-writers-guide/) ·
[The Alexandrian — Three Clue Rule](https://thealexandrian.net/wordpress/1101/roleplaying-games/three-clue-rule-part-3-the-three-clue-rule) ·
[The Alexandrian — The Art of the Key](https://thealexandrian.net/wordpress/35180/roleplaying-games/the-art-of-the-key)
