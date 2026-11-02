# I segreti dell'orda — solo per il DM

> **Per chi**: il DM. I giocatori leggono il libretto (`ARC08-18`), non questo
> file: quello che sta qui lo scoprono sul campo, quando succede.
> **Cosa c'è**: le capacità dei reparti dell'orda, l'avanguardia della
> Sessione 1 (mazzo, sergente, statblocchi della ricognizione, tracciatore), e
> le scelte fatte fra i numeri dell'arco che non si accordavano.
> **Stato**: proposta (ADR-0096). Le capacità sono nelle simulazioni di
> `plans/esperimenti/battaglia-campale-2026-10-21/assedio_v3.py`; le carte
> dell'avanguardia in `avanguardia.py`.

---

## 1. Le capacità dei reparti dell'orda

Vengono dalle schede delle unità di `ARC08-02` §1 e §4, lette con i numeri del
libretto. Il DM non le spiega, ma dice sempre il numero del bersaglio
(«stavolta contro 32»). La prima volta racconta quello che si vede, senza
spiegare la regola.

| Reparto | Capacità | Effetto nel libretto | Fonte |
|---|---|---|---|
| **Orchi** | **Carica selvaggia** | nel round in cui arrivano sul fronte: **+1** AU e **−2** DU | `ARC08-02`, unità orchi (AU +8 e DU 12 al primo round) |
| **Orchi** | **Furia** | a 4 PFU o meno: **+1** AU | `ARC08-02`, unità orchi (AU +8 a ≤4 PFU) |
| **Hobgoblin** | **Formazione tattica** | se sul fronte ci sono due o più reparti di hobgoblin (i guerrieri non contano: non marciano al tamburo), ognuno ha **+1** DU | `ARC08-02` e `ARC08-01`, unità hobgoblin |
| **Lupi e goblin** | **Sbilanciare** | il reparto nanico che hanno davanti ha **−2** al bianco, una volta sola anche con due reparti di lupi davanti | `ARC08-02`, unità worg (−2 DU al bersaglio) |
| **Giganti** | **Bombardamento** | un macigno per settore; ignora le merlature delle Mura | `ARC08-02`, giganti |

Come si raccontano, la prima volta:

- la Carica selvaggia è il muro di scudi che arretra di un passo sotto l'urto,
  e gli orchi che restano scoperti dopo;
- la Formazione tattica è il suono: gli hobgoblin avanzano al passo, al
  tamburo, e gli scudi si chiudono fra un reparto e l'altro;
- lo Sbilanciare sono i lupi che tirano le caviglie e i goblin che tagliano i
  tendini a chi cade.

## 2. L'avanguardia (Sessione 1, libretto §13)

### Il mazzo, round per round

È la versione più dura, la stessa di `avanguardia.py`. La ferocia è quella
dell'assedio: feroce, se il DM non dice altro. I reparti hanno i numeri del
libretto §11 (all'orda feroce: lupi e goblin AU 9, DU 19, PFU 10; hobgoblin
AU 12, DU 22, PFU 10).

| Round | Carta | Cosa arriva |
|---|---|---|
| 1-2 | **I lupi cavalcati** | un reparto di lupi e goblin per squadra, che sbilancia (§1). Se cade, ne arriva un altro |
| 3 | **La pattuglia avanzata** | arrivano gli hobgoblin: il fronte di ogni squadra sale a due, e il **sergente** dà **+1** ad AU e DU di tutta l'avanguardia. Da qui ogni reparto distrutto è sostituito da un reparto di hobgoblin, senza limite: l'avanguardia è lunga quanto la pazienza del gruppo |
| 4 | nessuna | |
| 5 | **Il corno di Grimjaw** | un altro **+1** ad AU e DU di tutta l'avanguardia, +2 col sergente. Si legge il box sotto |

Il giocatore che ha scelto l'orda pesca le carte e decide su quale squadra
cadono i lupi; il DM gli dà questo paragrafo e il successivo, non il resto
del file.

> **Read-aloud (Tolkien lead) — il corno.** *Dalla cresta viene un suono
> lungo, basso, che non è di un animale. Le file degli hobgoblin si fermano
> tutte insieme, e poi ripartono più in fretta. Laggiù, in piedi sulla
> cresta, un orog con una benda nera guarda verso le mura e non si muove.
> Che fate?*

Grimjaw non si sfida e non si colpisce: la cresta è a 400 m, oltre la
portata dell'arco di Dara (330 m). Guarda, e ricorda chi ha visto.

### Il sergente

Si può **Sfidare** dal round 3 (libretto §13): l'eroe lascia la squadra per
un round e lo affronta sulla mappa del pendio. Ha **50 pf**; quando ne ha
perso la metà fugge, come un comandante, e il suo +1 esce dall'avanguardia; ma non è un comandante
dell'assedio, e la sua fuga non dà il +2 al morale (libretto §13). Se muore
nel duello vale lo stesso. La retroguardia è un'altra
cosa: copre la ritirata e non porta al duello.

È lo stesso sergente della postazione degli scout nella ricognizione. Se lì
è morto o è stato preso, la carta del round 3 arriva **senza il suo +1**.

**Il sergente** · *hobgoblin bladebearer* di *Red Hand of Doom* (D&D 3.5,
⚠️ **non SRD**), dal PCGen `hobgoblin bladebearer 6 liv longsword`, con
l'armatura completa al posto della corazza di piastre +1 · GS 6 · hobgoblin
guerriero 6°, Medio, LM · Iniz +4 · scurovisione 18 m · Ascoltare +1,
Osservare +1 · CA **21** (armatura completa +8, Des +1 fino al tetto
dell'armatura, anello di protezione +1, Difesa con Due Armi +1), contatto 12,
colto alla sprovvista 20 · pf **50** (6d10+12) · Temp +7, Rifl +6, Vol +5 ·
velocità 6 m · *spada lunga +1* +11/+6 (1d8+6, 19-20); con due spade +9/+4
(1d8+6, 19-20) e *spada lunga perfetta* +9/+4 (1d8+3, 19-20) · For 16, Des
18, Cos 15, Int 10, Sag 12, Car 8 · Combattere con Due Armi, Combattere con
Due Armi Migliorato, Difesa con Due Armi, Arma Focalizzata e Arma
Specializzata (spada lunga), Volontà di Ferro, *Oversized Two-Weapon
Fighting* (⚠️ non SRD, *Complete Warrior*: la seconda spada lunga conta come
arma leggera) · due pozioni di *cura ferite moderate*, il corno · lingue
Comune, Goblin.
*Nota di conto*: l'armatura completa toglie 6 a Scalare, Saltare, Muoversi
Silenziosamente e Acrobazia del PCGen (Scalare +3, Muoversi Silenziosamente
+3, Acrobazia +0) e porta la velocità da 9 a 6 m. La scheda del Bestiario
`hobgoblin-sergente-cr5` (guerriero 5°, 37 pf) è il sergente di un reparto
qualunque; questo è più forte, e vale solo per l'avanguardia.

### La ricognizione: pattuglia e scout

Gli statblocchi della Sessione 1, scena della ricognizione. Fonti nell'ordine
del DM: le schede di *Red Hand of Doom* sono D&D 3.5 ma ⚠️ **non SRD**
(PCGen in `Bestiario/pregen-pcgen/png_La_mano_rossa_del_destino/`, trascritte
in `Bestiario/mostri/`).

**Goblin cavalcatore di worg** (×3, la pattuglia) · *goblin worg raider*,
non SRD · GS 5 · goblin guerriero 5°, Piccolo, LM · Iniz +4 · scurovisione
18 m · Ascoltare +1, Osservare +3, Nascondersi +9, Muoversi Silenziosamente
+9, Cavalcare +17 · CA 19, contatto 15, colto alla sprovvista 15 · pf 42
(5d10+10) · Temp +6, Rifl +5, Vol +1 · *arco corto composito perfetto* +12
(1d4, ×3), entro 9 m +13 (1d4+1); *scimitarra perfetta* +7 (1d4, 18-20) ·
Tiro in Sella, Combattere in Sella, Tiro Ravvicinato, Tiro Preciso, Arma
Focalizzata (arco corto) · lingue Comune, Draconico, Goblin.

**Worg** (×3, le cavalcature) · scheda del Bestiario `worg-cavalcatura-cr2`,
avanzato a 6 DV (⚠️ potenziamento: l'SRD dà 4 DV e 30 pf) · GS 2 · bestia
magica Media, NM · Iniz +2 · scurovisione 18 m, visione crepuscolare,
**fiuto** (sente chi passa entro 9 m; 18 m se il vento gli porta l'odore, 4,5 m se chi passa è sottovento) · Ascoltare +7,
Osservare +7, Nascondersi +4, Muoversi Silenziosamente +7, Sopravvivenza +2
(+6 seguendo col fiuto) · CA 14 · pf 51 · Temp +7, Rifl +7, Vol +4 ·
velocità 15 m · morso +9 (1d8+4) e **sbilanciare** gratuito (+3) · Allerta,
Attacco Naturale Migliorato (morso), Robustezza Migliorata (⚠️ non SRD).

La pattuglia intera: EL 8 (tre GS 5; i worg non la alzano di un punto intero).

**Hobgoblin regolare** (×9, la postazione degli scout) · *hobgoblin
regular*, non SRD · GS 2 · hobgoblin combattente 3°, Medio, LM · Iniz +1 ·
scurovisione 18 m · Ascoltare +3, Osservare +2 · CA 19 (cotta di maglia
perfetta, scudo pesante +1), contatto 11, colto alla sprovvista 18 · pf 23
(3d8+6) · Temp +6, Rifl +3, Vol +1 · velocità 6 m · *spada lunga perfetta*
+6 (1d8+1, 19-20); arco lungo composito (+1) +4 (1d8+1, ×3) · Allerta, Arma
Focalizzata (spada lunga) · *mantello della resistenza +1*, una pozione di
*cura ferite moderate* · lingue Comune, Goblin.

Gli scout sono nove più **il sergente** qui sopra: EL 9 circa. Pattuglia e
scout insieme: EL 10 circa. Con tre pregen gli scout sono sei più il
sergente.

### Il tracciatore dell'avanguardia

Una riga per squadra, fino a due reparti nemici ciascuna. Si copia su un
foglio e si cancella a matita.

| Squadra | Nemico 1 · PFU | Nemico 2 · PFU | Tacche | Mezze trappole | Travolta |
|---|---|---|---|---|---|
| Borin (Guardia) | ______ □□□□□□□□□□ | ______ □□□□□□□□□□ | □□□ | □□□□□□ | □ |
| Dara (balestrieri) | ______ □□□□□□□□□□ | ______ □□□□□□□□□□ | □□□ | □□□□□□ | □ |
| Thorin (veterani) | ______ □□□□□□□□□□ | ______ □□□□□□□□□□ | □□□ | □□□□□□ | □ |
| Nala (veterani) | ______ □□□□□□□□□□ | ______ □□□□□□□□□□ | □□□ | □□□□□□ | □ |
| capitano (veterani) | ______ □□□□□□□□□□ | ______ □□□□□□□□□□ | □□□ | □□□□□□ | □ |

Sotto: round □□□□□□ · sergente in campo □ · sergente fuggito □ · corno □ ·
morale della rocca ____.

## 3. Le scelte fra numeri che non si accordavano

La ricerca nell'arco ha trovato fonti che si contraddicono. Il libretto ha
preso queste, e le altre restano dove sono senza correzioni in questo
giro.

| Cosa | Le versioni | Scelta del libretto |
|---|---|---|
| Massi dei giganti | AU +14 (`ARC08-02`), 3d8 dal gomito della strada a ~100 m, incremento 36 m (`Mappe` L2), 2d8+12 (scontri) | la carta usa **AU +14**, la scheda dell'unità |
| Riserva | 30 nani senza postazione nel cortile esterno, che il DM manda alla breccia (DM, 2026-10-22; `Mappe` L2, MAPPA 2) | nel libretto (§1) entra nel settore che cede come terzo reparto della schiera, e non torna indietro `[INFERRED]` |
| Baliste | 6 con AU +10 (`ARC08-02`), 10 a +18 (`Mappe` L2), 12 (archivio) | una per torre, **d20 + 10**, perché nel libretto le altre stanno sui settori senza giocatore |
| Carica | +2 att/−1 CA, +2 att/+2 danni/+1 morale (due righe di `mass_combat_guide_Dm.md`) | l'ordine **Caricare**: +2 al rosso, −2 al bianco |
| Comandare | Car CD 15 (`ARC08-02`), Diplomazia CD 18 (`ARC08-01`) | il gesto **Comandare** senza prova |
| Trappole | 2d6, +2 danni, 4d6 ×3, −2 CA in quattro file | una trappola **annulla una tacca del Giorno 1 o del Giorno 2**, nel settore che i giocatori vogliono |
| Morale | scala ±5 (`ARC08-02`), ±4 (variante 2d6), −6 (`Mappe` L3) | scala ±5, sui dadi al massimo ±2 (libretto §6) |
| Olio bollente | non c'è in nessun file | non c'è nemmeno qui |

Le strutture (mura 1.800 pf in `ARC08-02` contro 240 in `Mappe` L2) restano
fuori dal libretto: la breccia si misura con le tacche, non con i pf delle
mura. Il **cancello ha 200 pf** `[CANONE — DM 2026-10-21]`: valgono nei
combattimenti sulla mappa coi PG, e nel libretto non si traducono in niente.

## 4. Il mazzo, la ferocia e le carte (era il §12 del libretto)

Stava nel libretto dei giocatori; dal 2026-10-21 sta qui, perché il libretto dice che quello che l'orda sa fare i giocatori lo scoprono sul campo `[CANONE — DM 2026-10-21]`.

**Il mazzo dell'orda.** Ogni giorno, per ogni settore, quattordici reparti
mescolati: sei di hobgoblin, quattro di guerrieri, tre d'orchi, uno di lupi.
Si pesca a caso. Quello che resta nel mazzo a fine giorno non torna.

**La ferocia.** Un numero solo, da dire prima della battaglia, che si somma
ad AU e DU di tutti i reparti dell'orda. Le percentuali sono dalle prove con
il terreno, le capacità, le baliste e da tre a sei trappole.

| Orda | AU e DU | Breccia contenuta, «pieno» | Posizioni tenute, «pieno» |
|---|---|---|---|
| **Normale** | −1 rispetto al libretto §11 | quasi sempre | quasi 9 volte su 10 |
| **Feroce** (default) | come in §11 | 8-9 volte su 10 | 6 volte su 10 |
| **Terrificante** | +1 rispetto al libretto §11 | 5-6 volte su 10 | 2 volte su 10 |

Con le trappole che valgono il primo e il secondo giorno, ognuna fino alla
sesta toglie all'orda feroce tre o quattro probabilità su cento di aprire una
breccia. Negli script la ferocia ha un numero: normale = 1, feroce = 2,
terrificante = 3.

**Le carte dell'orda.** Una per round al massimo, in un settore a scelta;
solo i giganti tirano in tutti i settori. Le simulazioni hanno provato i
giganti, la breccia del cancello e il soffio; Gorthak, Grimjaw, la palla di
fuoco, il gesto Sfidare e il Fuoco di copertura non sono ancora provati e si
tarano al primo tavolo. Le capacità dell'orda sono al §1.

| Giorno | Carta | Effetto |
|---|---|---|
| 1-2 | **I giganti** | round 2: **un macigno per settore**. Per ognuno il DM tira d20 + 14 contro la DU di un reparto (con il +1 del primo giorno e il morale; le merlature delle Mura non contano), e usa la tabella del rosso |
| 1-2 | **Gorthak al cancello** | comandante: il Cancello può **Sfidare**. Finché c'è, il fronte del Cancello sale di uno |
| 1-2 | **La palla di fuoco** | 1d4+1 PFU a un reparto; il giocatore tira d20 + 5 contro 16, se riesce dimezza |
| 2 | **La breccia del cancello** | non occupa un round: dall'inizio del giorno il fronte del Cancello sale di uno. Con Gorthak sale di due |
| 2-3 | **Grimjaw e la guardia nera** | comandante: si può **Sfidare** |
| 3 | **Il soffio** | round 2: ogni reparto sulle Mura perde 1d4 PFU |
| 3 | **La ritirata** | non occupa un round: il terzo giorno ha quattro round, poi tutti verso il Cuore della Montagna |

**Cosa si legge nella tabella dei bonus** (`ARC08-10-ESITI-E-CONTINGENZE.md`
§5) alla fine dell'assedio:

| Obiettivo | Pieno | Parziale | Fallito |
|---|---|---|---|
| **Breccia contenuta** (§5.2) | nessuna breccia nei giorni 1 e 2 | una | due o più |
| **Comandanti logorati** (§5.2) | Gorthak e Grimjaw fuggiti feriti | uno dei due | nessuno |
| **Cantitrici protette** (§5.2) | le Mura non cedono il giorno 2 | cedono al round 4 o 5 | cedono entro il round 3 |
| **Posizioni tenute** (§5.3) | alla ritirata restano tre quarti dei reparti o più | da un terzo a tre quarti | meno di un terzo |
| **Re Thorek** ed **evacuazione** (§5.3) | come nel master, nella resistenza al Cuore | | |

Le Cantitrici sono un obiettivo, non una carta: si annunciano all'alba del
secondo giorno. Nel modo A le righe di massa sono **parziali**, e contano solo
i combattimenti sulla mappa.
