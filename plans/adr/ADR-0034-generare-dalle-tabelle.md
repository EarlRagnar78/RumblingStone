# ADR-0034 — Generare dalle tabelle, e dichiarare la taratura

> **Stato**: accettata · **Data**: 2026-09-03 · **Decide**: G. Samuele (DM)
> **Attua**: `plans/PIANO-GENERATORE-CREATURE-E-PNG.md`
> **Rapporti**: attua ADR-0033 (derivare e dichiararlo) sul verso opposto —
> là si legge una scheda, qui si costruisce una creatura che non c'è.
> Vincolata da ADR-0021 (il blocco è un dato) e ADR-0003 (il markdown è il master).

## Il contesto

Fra i 54 strumenti del DM ne mancava uno solo, e lo si è visto chiudendo il
lotto H: `suggest_encounter` **pesca** dal catalogo, `build_monster_catalog`
lo **indicizza**, `derive_statblocks` **legge** una scheda che esiste già.
Nessuno **costruisce** una creatura che non c'è.

Il DM ha chiesto la cosa in tre pezzi:

1. le tabelle SRD per generare mostri, PNG e **incantatori**;
2. Pathfinder 1e come **variante più cattiva**, quando ne servono di più duri;
3. il generatore come **opzione per quello che nel Bestiario non c'è**, e un
   innesto in `suggest_encounter` perché gli incontri non si ripetano mai uguali.

## La decisione

### 1 · Le tabelle SRD danno la forma, il bersaglio per GS dà il livello

Il SRD 3.5 dice quale dado, quale BAB, quali tiri salvezza buoni, quanti
incantesimi al giorno. Non dice **quanto deve essere duro** un mostro di GS 7:
una tabella «statistiche per GS» nel SRD non esiste. Quel numero viene dalla
riga PF1e, che è contenuto libero OGL, e serve come **bersaglio verso cui
costruire** — non come tabella da copiare.

Le caratteristiche di un mostro si **risolvono** verso quel bersaglio (è come
le sceglie chi scrive un mostro a mano), quelle di un PNG con livelli di classe
vengono dalla **matrice élite/standard** più gli aumenti ogni 4 livelli. Sono
due mestieri diversi, e confonderli è stato il primo difetto: costruendo ogni
cosa come un PNG usciva un «GS 7» con 38 punti ferita e CA 12.

### 2 · «Più cattivi» è un template dichiarato, non una seconda tabella

`--piu-cattivi` applica il template **Advanced** di PF1e — +4 a tutte le
caratteristiche, +2 di armatura naturale, +2 su tutti i tiri — **senza alzare il
GS**. Il template vale GS +1: applicarlo e continuare a vendere la creatura come
GS *n* è la definizione operativa di «più cattivo di quanto il GS prometta», che
è ciò che il DM ha chiesto.

E la creatura **lo dice di sé**, in una voce del blocco: *«template Advanced
applicato SENZA alzare il GS: vale in realtà GS 8»*. Un mostro più duro senza un
perché scritto è un mostro che al tavolo sembra barare; con la riga scritta, è
una scelta che il DM può disfare in dieci secondi.

### 3 · L'output non entra mai nel canone da solo

`genera_creatura` stampa, o scrive in una cartella di lavoro, e **si rifiuta**
di scrivere sotto `Bestiario/` — con un messaggio che spiega perché, non con un
errore. È il confine di ADR-0033: lo strumento propone, nel canone scrive il DM.
Il motivo è concreto: una scheda generata che entra nel Bestiario senza che
nessuno l'abbia letta è indistinguibile da una scritta a mano, e da quel momento
`suggest_encounter` bilancia gli incontri su di lei.

### 4 · Il carattere è parte del contratto, non un ornamento

Ogni creatura esce con un talento firma, una tattica in una riga e una
**debolezza sfruttabile**, prese da tabelle scritte a mano per ruolo. Senza,
il generatore produce mostri intercambiabili — e un mostro intercambiabile il DM
se lo scrive prima da solo che a leggerlo. La debolezza in particolare non è
colore: è la cosa che dà ai PG qualcosa da trovare.

## Una correzione a quello che era scritto nel piano

Il piano diceva, e l'avevo scritto io, che *«PF1e a parità di GS è molto più duro
del 3.5»*. Sulla riga base **non è vero**, e va corretto perché su quella frase
poggiava la scelta di tarare:

| GS | mostro del SRD 3.5 | pf · CA | riga PF1e | pf · CA |
|---|---|---|---|---|
| 3 | Ogre | 29 · 16 | | 30 · 17 |
| 5 | Troll | 63 · 16 | | 55 · 19 |
| 7 | Chimera | 76 · 19 | | 85 · 20 |
| 7 | Gigante delle Colline | 102 · 20 | | 85 · 20 |

Sui punti ferita le due tarature si sovrappongono; PF1e sta un punto o due sopra
sulla CA e sull'attacco. Quindi il bersaglio 3.5 è la riga PF1e con **CA −1 e
attacco −1** — non una derata inventata al 70%, che avrebbe prodotto mostri di
carta. La differenza vera fra i due sistemi non sta nella riga: sta nei
**template**, ed è esattamente da lì che viene la variante più cattiva.

## Le conseguenze

**Quello che si guadagna.** Un incontro di passaggio si prepara in un comando
invece che in venti minuti; gli incontri smettono di ripetersi; e le tabelle,
prima sparse fra `derive_statblocks.py` e le skill, ora stanno in un posto solo
(`dmcore/tabelle.py`) con la provenienza riga per riga e un test che le confronta
con le ancore delle skill.

**Quello che si paga.** Tre cose, dette:

- **Le righe non verificate restano non verificate.** Delle venti righe della
  tabella per GS, otto sono controllate contro la fonte; le altre sono
  estrapolate e la creatura generata a quei GS lo scrive nel proprio conto.
  Marcarle è meno comodo che nasconderle, ed è l'unica cosa onesta da fare.
- **La regola «DV ≈ GS» è una convenzione, non una fonte.** Il SRD non ha un
  «DV per GS». È tarata sui mostri del SRD e sta scritta come convenzione,
  perché è il genere di numero che, se non dichiarato, fra sei mesi sembra una
  fonte.
- **Sei ruoli sono una proposta.** Il piano §5 chiedeva al DM quali servissero
  davvero; sono dati, non rami del codice, e toglierne uno è una riga.

## Emendamento del 2026-09-03 — la lista di classe, non la tradizione

Trovato costruendo le schede del Bestiario, e va scritto qui perché è il difetto
più insidioso che questo strumento abbia prodotto.

Gli incantesimi erano scelti da liste **per ruolo** — «controllore» pescava
arcano, «comandante» divino. Sembra ragionevole e **non lo è**: a un druido
costruito come controllore il generatore dava *armatura magica*, *sonno* e *dito
della morte*, che sono da mago; come bruto gli dava *benedizione*, *santuario* e
*scudo della fede*, che sono da **chierico**. Il blocco usciva completo e
plausibile, e al tavolo il druido avrebbe annunciato un incantesimo che non ha.

**Non basta separare arcano e divino.** Chierico, druido e bardo hanno tre liste
diverse pur essendo tutti «divini» o «ibridi»: è la **lista di classe** a
decidere, non la tradizione e tantomeno il ruolo.

Provvedimenti presi subito:

- le due schede colpite sono state ripulite a mano: gli slot restano (vengono
  dalla tabella SRD del druido, che è giusta), la scelta è dichiarata pendente;
- il generatore **si rifiuta** di scegliere per una classe la cui lista non è
  coperta, e lo dice: *«Incantesimi da scegliere a mano»*. Un vuoto dichiarato si
  riempie in due minuti; una lista sbagliata arriva al tavolo e ci resta;
- un test lo tiene fermo per druido e adepto, e verifica che le classi coperte
  gli incantesimi li ricevano lo stesso.

La revisione vera — **tradizione × ruolo**, con le quattro funzioni che il DM ha
nominato (controllore · blaster · supporto · utilità) e le liste per *classe* —
è proposta e **non ancora approvata**: sta in
`plans/PIANO-GENERATORE-CREATURE-E-PNG.md` §7.

## Quando NON usarlo

Va scritto qui, o il generatore diventa la scorciatoia per tutto:

- se nel catalogo c'è già qualcosa di simile → **si potenzia** (skill
  `npc-villain-boosting`), non si genera un doppione;
- se la creatura ha un ruolo nella trama → **si scrive a mano**; il generatore
  al massimo dà l'ossatura;
- se serve per **un incontro di passaggio** → è esattamente il suo caso.
