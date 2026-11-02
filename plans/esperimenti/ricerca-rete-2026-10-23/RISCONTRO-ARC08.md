# Riscontro SRD dei master ARC08-DEF-1 e ARC08-DEF-2

**Data**: 2026-10-23 · **Strumento**: `scripts/riscontro_srd.py` (ADR-0103, canale testing)
**Riscontri**: [riscontri-arc08.yaml](riscontri-arc08.yaml) · **Tabella completa con le citazioni**: [out/riscontro-arc08.md](out/riscontro-arc08.md)
**Stato**: rapporto, con un seguito. Le tre discordanze sono state chiuse il 2026-10-23: la freccia assassina con la scelta del DM (regola 3.5, «o muore», `[CANONE — DM 2026-10-23]`), le due della presenza terrificante come errori di fatto (63 m per l'adulto maturo, commit ae684a20). Il riscontro rifatto dopo le correzioni dà 53 concordanze su 53 (`out/riscontro-arc08.md`).

```bash
python3 scripts/riscontro_srd.py scarica      # una volta: 50 MB in ~/.cache/rumblingstone/srd
python3 scripts/riscontro_srd.py riscontra plans/esperimenti/ricerca-rete-2026-10-23/riscontri-arc08.yaml
```

Fonti: SRD 3.5 in Markdown (olimot/srd-v3.5-md@c7f30a0c) e PRD PF1e in
SQLite (devonjones/PSRD-Data@76ea4784), entrambi OGL 1.0a, scaricati da
`raw.githubusercontent.com` in questa sessione con lo sha256 di ogni file
verificato. La copia nella cartella di lavoro della ricerca non è servita.

## In breve

| Master | Regole riscontrate | Concordano | Discordano | Non trovate |
|---|---:|---:|---:|---:|
| DEF-1 | 19 | 17 | **2** | 0 |
| DEF-2 | 34 | 33 | **1** | 0 |
| Totale | 53 | 50 | 3 | 0 |

Il riscontro gira in 0,25 s con la cache piena. Sono le regole di DEF-1 e
DEF-2 che il master attribuisce all'SRD, o che prende da una scheda SRD, e
che si confrontano con un numero o con un termine chiuso: raggi in metri
(dai piedi con la scala 0,3), CD, pf, CA, bonus, dadi, durate.

## Le tre discordanze

### 1. DEF-2, la *freccia assassina* (riga 1395)

| | Testo |
|---|---|
| SRD 3.5, `magic-items/magic-items-ii-armor-and-weapons.md:581` | «the target must make a DC 20 Fortitude save **or die** (or, in the case of unliving targets, be destroyed) instantly» |
| PRD PF1e, *Ultimate Equipment* (e *Core Rulebook*) › Slaying Arrow | «DC 20 Fortitude save **or take 50 points of damage**» |
| DEF-2:1394-1398 | «Tempra **CD 20** o subisce **50 danni** in più … l'SRD 3.5 dà i 50 danni» |

È la discordanza che la ricerca aveva trovato (RICERCA §3, T36 e N12 del
triage). Il riscontro aggiunge un dettaglio: i 50 danni non sono solo in
*Ultimate Equipment*, ci sono già nel *Core Rulebook* di Pathfinder. La CD
(20) e il prezzo (2.282 mo) concordano. **Domanda per il DM**: «muore» del 3.5
o «50 danni» di PF1e? In tutti e due i casi l'attribuzione nel master va
corretta.

### 2 e 3. DEF-1, il raggio della presenza terrificante (righe 1027 e 1518)

| | Testo |
|---|---|
| SRD 3.5, `monsters/monsters-dr-dw.md:47` | «within a radius of 30 feet x the dragon's age category» |
| SRD 3.5, `monsters/monsters-dr-dw.md:67` | categoria 6 *Adult*, categoria 7 *Mature adult* |
| DEF-1:1027 | «l'SRD dà **54 m all'adulto** (9 m per categoria d'età)» |
| DEF-1:1518 | «Presenza terrificante **90 m** … 54 m nell'SRD **per un adulto**» |
| DEF-2:1956 | «63 m nell'SRD per l'adulto maturo» |
| ARC08-01:231 e `Bestiario/villain/Fauci_di_Palude.md` | Fauci «resta un **adulto maturo** per canone»; «63 m all'adulto maturo» |

Il conto di DEF-1 è giusto per un adulto (6 × 9 m = 54 m), ma Fauci non è un
adulto: il canone, il Bestiario e DEF-2 dicono adulto maturo, cioè 7 × 9 m =
**63 m**. Le altre caratteristiche che DEF-1 dà a Fauci nella stessa riga
1518 (CA 29, RI 21, soffio 14d4, volo 45 m, linea di 30 m) sono quelle
dell'adulto maturo, e concordano. Al tavolo non cambia niente, perché il
raggio usato è il potenziamento di 90 m; cambia il confronto che il master
scrive per giustificarlo. Lo script segna la discordanza perché il file dei
riscontri confronta con la categoria di Fauci; letta alla lettera, la frase
«54 m all'adulto» è vera. **Domanda per il DM**: allineare DEF-1 a DEF-2
(«63 m all'adulto maturo»)?

## Che cosa concorda

DEF-1: il fiuto dei worg in tre distanze, due volte (testo della scena e
scheda A.2); DV, pf e velocità del worg dell'SRD; la CD 10 e il +2
dell'aiutare un altro; i 9 m per categoria d'età; linea, danni del soffio,
CA, RI e volo di Fauci.

DEF-2: CD e prezzo della freccia; *comunione* in dieci minuti; spremersi a
−4 (tre punti del master); pf e CA del gigante delle colline; nuotare con la
penalità d'armatura doppia; trattenere il fiato per il doppio della
Costituzione; guarigione naturale di 1 pf per DV; togliere l'armatura in
1d4+1 minuti; prono a −4 contro la mischia; stabilizzare con Guarire CD 15;
morte a −10; la spinta (1,5 m, più 1,5 m ogni 5 punti) e la stabilità dei
nani (+4); l'attacco mortale con tre round di studio; schivare prodigioso
migliorato (quattro livelli di ladro in più); il soffio che torna in 1d4
round; la scheda di Fauci (presenza, linea, danni, CA, RI, volo, *scudo* di 7
minuti per uno stregone di 7°); la scheda del troll (pf, CA, artigli,
sbranare, scurovisione, velocità).

## Che cosa resta fuori

- **Le regole che lo script non sa controllare**: quelle che il master
  stesso segna «scelta del modulo» o «non SRD» (Intimidire a CD fissa, il
  soffio a cono, la Presenza a 90 m, gli statblocchi di *Red Hand of Doom*),
  e quelle scritte senza un numero o un termine chiuso (*immagine
  silenziosa* creduta da chi la guarda, *frantumare* solo su oggetti
  fragili, l'attacco mortale che uccide o paralizza). Si potrebbero
  scrivere come voci di sola presenza, ma direbbero solo che la frase
  inglese esiste.
- **La balista** (DEF-2:40 e 846): il master la attribuisce alla *Guida del
  DM* 3.5, fuori SRD, e alla balista pesante di *Ultimate Combat*. L'SRD
  non ha le macchine d'assedio e il PRD del 2015 non ha quella tabella:
  RICERCA §3 la aveva letta con WebFetch.
- **Valori potenziati**: i pf, i DV e la CD del soffio di Fauci (25 DV), di
  Gorthak (ettin a 15 DV) e dei worg a 6 DV sono potenziamenti dichiarati.
  Si riscontra la base dell'SRD che il master cita, non il risultato.
- **Il resto di ARC-08**: `ARC08-01`, `ARC08-02` e gli altri file non sono
  stati riscontrati. Il formato regge; serve scrivere le voci.
