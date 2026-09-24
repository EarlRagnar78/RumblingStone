# Varietà fra gli archi — la tavolozza e il governo del ritmo

Il mixer di `SKILL.md` decide **quale pilastro guida una scena**. Non dice
niente su **di che colore è un arco intero**, né se quel colore è già stato
usato nell'arco precedente. Questo file copre quel piano — ed è il piano su
cui una campagna diventa «abbatti abbatti mostro» senza che nessuna singola
sessione sia scritta male.

> **Il difetto che questo file previene**: ogni arco, preso da solo, può
> essere ottimo; e la campagna essere monotona lo stesso. La monotonia non è
> un difetto di scena, è un difetto di **sequenza**, e non si vede leggendo
> un modulo — si vede leggendo due recap di fila.

---

## 1. La tavolozza d'arco — cinque dichiarazioni

Ogni arco dichiara queste cinque cose **prima** che se ne scriva il
contenuto. Stanno in cinque righe, non in un documento.

```
COLORE DOMINANTE   la tinta che il tavolo ricorderà (una sola)
CONTRAPPUNTO       la seconda tinta, ~1/4 dell'arco. DIVERSA dal dominante
FAMIGLIA DI CASO   quale delle sei, oppure «nessuna» (dichiarata, non omessa)
CONGEGNO           uno, oppure «nessuno». Due solo se l'arco è MODULARE (§6.3)
IL PICCO           la scena da fotografare (una per arco, dichiarata)
```

`«nessuna»` e `«nessuno»` sono risposte legittime e vanno **scritte**: un
arco senza indagine è una scelta, un arco che si è dimenticato di averne una
è un incidente. La differenza si vede solo se la casella è compilata.

## 2. Le sei tinte

| Tinta | Com'è al tavolo | Cosa stanca | L'antidoto (= il contrappunto giusto) |
|---|---|---|---|
| **Guerra / assedio** | pressione continua, decisioni di massa, perdite | la ripetizione tattica: dopo tre scontri il quarto è aritmetica | una tinta **stretta** — indagine o orrore: pochi, al chiuso, in silenzio |
| **Indagine** | lento, verbale, i giocatori parlano più del DM | l'immobilità: se non si muove niente si spegne | **guerra** o **esplorazione**: qualcosa che costringe a muoversi |
| **Politica** | tavoli, favori, reputazione come risorsa | l'astrazione: se non arriva a misura di PG è fondale | **orrore** o **indagine**: qualcosa di concreto e sporco |
| **Esplorazione / viaggio** | il mondo è grande, le risorse contano | la lista di luoghi: tre villaggi non sono tre scene | **politica**: arrivare da qualche parte e trovarci gente |
| **Orrore** | pochi, al buio, sotto qualcosa che non si capisce | l'assuefazione: al terzo mostro impossibile è un mostro | **cerimonia** o **guerra**: luce, gente, rumore |
| **Cerimonia / rito** | il tavolo guarda, il mondo riconosce i PG | non regge una sessione intera, quasi mai | **qualunque cosa la interrompa** |

L'ultima colonna è il vero contenuto della tabella: **il contrappunto non è
un capriccio, è la cura del difetto specifico del dominante.**

## 3. Le regole di rotazione — il governo

1. **Due archi consecutivi non hanno lo stesso colore dominante.** Nessuna
   eccezione, nemmeno «ma questa guerra è diversa».
2. **Il contrappunto di un arco è il dominante di quello dopo** (o di quello
   prima). Così la varietà è **preparata** invece che a scatti: il tavolo ha
   già assaggiato la tinta nuova prima che diventi il piatto principale.
3. **Un congegno per arco al massimo, e mai due archi di fila.** È la
   risorsa che si consuma più in fretta
   (`rumblingstone-indagine/references/congegno-e-enigmi.md` §9).
   **Unica eccezione**: un arco *modulare* con ~10 moduli vale, per
   estensione, più di un arco lineare — lì il tetto è **2** (§6.3). Non è
   un allentamento della regola: è la stessa densità applicata a una durata
   diversa.
4. **Una famiglia di caso non si ripete a meno di due archi di distanza.**
   Due impostori vicini e il terzo lo indovinano dal titolo.
5. **Un arco senza indagine è legittimo**: ma allora il contrappunto deve
   essere forte, e dichiarato.
6. **Ogni arco ha almeno una sessione che non gioca come le altre.** È il
   quarto d'arco del contrappunto: se non riesci a indicarla col dito, non
   c'è.

## 4. La prova del recap — la diagnosi in trenta secondi

> Prendi i recap di due archi consecutivi, **togli i nomi propri**, e
> leggili di fila. Se suonano uguali, uno dei due va ricolorato.

Funziona perché il recap registra **cosa ha fatto il tavolo**, non cosa il
DM aveva preparato. Due archi possono avere ambientazioni diversissime e
produrre lo stesso recap: *«siamo arrivati, abbiamo combattuto, abbiamo
vinto, siamo ripartiti»*. Quello è il segnale.

Diagnosi correlate, più veloci:

- **Nell'ultimo arco, quante scene si sono chiuse senza tirare iniziativa?**
  Se meno di un quarto, il dominante è guerra qualunque cosa dica la
  tavolozza.
- **Il picco dichiarato è lo stesso tipo di scena del picco precedente?**
  (Due cariche di fila, due rivelazioni di fila.) Se sì, ricolora.

## 5. Il registro — dove vive

La tavolozza è **dato di campagna**, non di skill: vive in
`campaign/state.md` §7 accanto agli altri tracker, e si scrive col triplo
vincolo di [ADR-0007](../../../plans/adr/ADR-0007-scritture-canone-triplo-vincolo.md).
Formato:

```markdown
### §7.T — Tavolozza degli archi

| Arco | Dominante | Contrappunto | Famiglia di caso | Congegno | Picco |
|---|---|---|---|---|---|
| 07 | esplorazione | orrore | nessuna | — | … |
| 08 | guerra | ? | ? | ? | la carica (4C) |
| 09 | ? | ? | ? | ? | ? |
```

**Le celle `?` sono informazione**: dichiarano che la decisione non è stata
presa, e impediscono di scoprirlo a metà arco.

## 6. La quota di modulo — quando un arco ha molti moduli

Un arco lineare si governa con la tavolozza (§1). Un arco **modulare** —
molti moduli paralleli, e sceglie il tavolo quale fare — no: lì «un mistero
per arco» è troppo poco e «uno per modulo» è troppo. Serve una **quota**.

### 6.1 Le sei assi da bilanciare

| Asse | Cos'è | Difetto se manca | Difetto se abbonda |
|---|---|---|---|
| **Battaglia** | scontro come corpo del modulo | l'arco non ha peso | «abbatti abbatti» |
| **Esplorazione** | il mondo, la strada, le risorse | tutto succede al chiuso | itinerario invece di scene |
| **Intrigo / politica** | favori, debiti, reputazione | la Valle è un fondale | astrazione lontana dai PG |
| **Mistero** | un caso vero, con nodi e ricomposizione | non si ragiona mai | i giocatori inventariano tutto |
| **Congegno** | la macchina scenografica | niente stupore | assuefazione (`congegno-e-enigmi.md` §9) |
| **Villain in scena** | un cattivo **nominato**, presente di persona | la minaccia è astratta | il cattivo perde statura |

### 6.2 La quota, su ~10 moduli

I numeri sono **conteggi**; la percentuale serve solo a leggerli.

| Cosa | Quota | ~% | Perché quel numero |
|---|---|---|---|
| Moduli **puliti** (né mistero né congegno: battaglia, esplorazione, recupero diretto) | **4-5** | ~45% | **È la quota più importante.** Se gli speciali sono la maggioranza smettono di essere speciali. Il fondo neutro è ciò che fa risaltare il resto |
| Moduli con **mistero, senza congegno** | **2** | ~20% | sotto 2 è un incidente, sopra 3 il tavolo comincia ad aspettarselo |
| Moduli con **mistero E congegno** | **1** | ~10% | è il modulo-picco dell'arco. **Uno solo** |
| Moduli con **congegno, senza mistero** | **1** | ~10% | la macchina incontrata senza indagine attorno: pura scenografia che cambia lo scontro |
| Moduli a **intrigo dominante**, senza caso formale | **1-2** | ~15% | politica giocata, non investigata |
| Moduli con **villain nominato in scena** | **3-4** | ~35% | trasversale: si somma agli altri, non li sostituisce |

**Totale speciali: 4 su 10.** È il rapporto che regge: sei moduli su dieci
sono quello che il tavolo si aspetta, quattro no.

### 6.3 Il tetto che non si sposta

**Congegni per arco modulare: 2, mai 3.** Uno dentro il modulo-picco (con
mistero), uno da solo. È l'unica riga di questa sezione che non è una
raccomandazione ma un limite: lo stupore è la risorsa che si ricarica più
lenta di tutte.

## 7. L'orchestrazione dinamica — perché la quota non si assegna in anticipo

Il difetto di una quota assegnata a tavolino è che diventa **un calendario**,
e un calendario si impara. Se il mistero cade sempre al terzo modulo, al
secondo arco il tavolo lo sa.

E c'è un problema più concreto: in un arco modulare **l'ordine lo scelgono i
giocatori**. Un'assegnazione fissa non sopravvive al contatto.

La soluzione è assegnare **al momento**, in tre livelli:

### Livello 1 — La vocazione del modulo (si scrive quando si scrive il modulo)
Ogni modulo dichiara **cosa può ospitare**, due o tre etichette, secondo la
sua finzione. Non cosa ospiterà: cosa *può*.

```
P2C Salvatore Mercante — vocazioni: [sparizione] [esplorazione] [villain]
P2A Torre Invisibile   — vocazioni: [congegno] [orrore] [cospirazione]
P2B Torneo di Dauth    — vocazioni: [accusa falsa] [intrigo] [cerimonia]
```

### Livello 2 — Il conto aperto (si tiene durante l'arco)
Una riga: quanta quota è stata spesa e quanta resta.
`speciali 2/4 · misteri 1/3 · congegni 0/2 · villain in scena 1/4`

### Livello 3 — L'assegnazione (si decide quando il tavolo sceglie il modulo)
Quando i PG dichiarano dove vanno, si incrocia **vocazione × quota residua ×
le cinque regole qui sotto**, e si decide *lì*. Il modulo era scritto per
reggere entrambe le versioni: quella pulita e quella con il caso.

### Le cinque regole anti-ritmo

1. **Mai due speciali di fila.** Dopo un modulo con mistero o congegno, il
   successivo è pulito. Senza eccezioni.
2. **Mai una cadenza regolare.** La distanza fra due speciali varia: 1, poi
   3, poi 2. Se un giocatore può contare, la sorpresa è finita.
3. **Il primo modulo dell'arco è pulito.** L'arco si apre su ciò che il
   tavolo si aspetta; lo speciale arriva quando si sono rilassati.
4. **Un gettone resta in mano fino ai 2/3 dell'arco.** Non si assegna
   all'inizio: si tiene, e si spende dove il tavolo sta meno in guardia.
5. **La regola dello scarto**: la più importante. Se il tavolo **ha già
   capito** che quel modulo è un caso (*«eh, qui c'è sotto qualcosa»*
   prima di cominciare), **lì non si spende niente**: si gioca pulito e il
   gettone si sposta. La loro aspettativa è il segnale, e disattenderla vale
   più del caso che avevi preparato.

### Il modulo che cambia natura

Il singolo strumento più efficace contro l'aspettativa, e va usato **una
volta per arco**: un modulo che comincia come una cosa e **diventa
un'altra**. Una missione di recupero diretta che a metà scopre una cosa che
non torna; un caso che a due terzi smette di essere un caso perché arriva un
esercito.

Requisiti: il cambio avviene **a metà o dopo** (prima è solo un aggancio
lungo), e il tavolo deve poter dire, ripensandoci, che i segni c'erano. Non
è un colpo di scena calato: è la **vocazione secondaria** del modulo che si
attiva.

### La leva finale: cambiare quale asse *sorprende*

Un tavolo abituato ai misteri si sorprende per una **battaglia** vera —
grande, senza trucchi, con delle perdite. Se in un arco lo strumento della
sorpresa è stato l'indagine, nell'arco dopo lo strumento è che **non c'è
niente da indagare** e l'orco è solo un orco, ma sono duecento.

## 8. Applicazione proposta agli archi in corso

> ⚠️ **`[PROPOSTA — needs DM confirmation]`.** Questa sezione non è canone e
> non è stata scritta in `state.md`: ARC-08 e ARC-09 sono **preparati** e la
> loro colorazione è una decisione del DM, non di un agente
> (`campaign-coherence.md` §0). Serve come esempio lavorato del §1 e come
> proposta concreta da approvare, correggere o rifiutare.

### ARC-08 — Battaglia di Hammerfist

| | |
|---|---|
| **Dominante** | **guerra / assedio.** Non si discute: è l'arco della battaglia |
| **Contrappunto proposto** | **indagine, tinta stretta** — e *dentro* le scene già scritte, non in scene nuove |
| **Famiglia proposta** | **2 — l'impostore.** Un assedio è un cast chiuso in uno spazio chiuso: la condizione ideale della famiglia. Gli errori di competenza (§famiglie-di-caso 2) si posano dentro i consigli di guerra che l'arco ha già |
| **Congegno** | **nessuno.** L'arco ha già 68 read-aloud e un picco dichiarato (la carica, 4C): una macchina competerebbe col picco invece di servirlo. E per la regola 3 conviene spenderlo dopo |
| **In compenso** | **un innesco in piena vista** (`congegno-e-enigmi.md` §5) — a scala d'assedio: un tratto di mura minato, un pozzo, il meccanismo di una porta. Costa una descrizione, non un arco |
| **Picco** | resta quello già dichiarato dall'arco |

**Perché questa combinazione**: è la sola che aggiunge varietà **senza
riscrivere niente**. L'impostore gira dentro le scene esistenti; l'innesco è
una riga in una descrizione. Il costo di preparazione è quasi zero e il
recap dell'arco smette di essere *«abbiamo difeso e abbiamo vinto»*.

### ARC-09 — dopo Hammerfist

L'arco è **modulare** (una decina di quest parallele fra Day 20 e Day 42) e
per questo è il posto naturale per la varietà: le tinte non si susseguono,
**convivono**, e sceglie il tavolo.

**Quota proposta** (§6.2 applicata ai ~11 moduli pianificati, esclusa la
battaglia finale che è fissa):

```
puliti (né mistero né congegno) ...... 5     ~45%
mistero senza congegno ............... 2     ~18%
mistero + congegno (modulo-picco) .... 1      ~9%
congegno senza mistero ............... 1      ~9%
intrigo dominante, senza caso ........ 2     ~18%
villain nominato in scena ............ 4     ~36%   (trasversale)
                                      ────
speciali .............................. 4 su 11
congegni .............................. 2  ← il tetto del §6.3, non 3
```

Proposta di colorazione per ramo — è una **vocazione** (§7 livello 1), non
un'assegnazione: quale ramo *porta* il gettone si decide quando il tavolo
sceglie dove andare.

| Ramo | Tinta | Famiglia proposta | Nota |
|---|---|---|---|
| Torre Invisibile (Zalkatar) | orrore | — | **il congegno dell'arco**, se il DM ne vuole uno: una torre che non si vede *è già* la premessa di una macchina |
| Torneo di Dauth (Tordek) | cerimonia | **5 — accusa falsa** | cast chiuso, reputazione in gioco, e Tordek ha lo spotlight. ⚠️ **vincolo esistente**: il Giorno 3 è già occupato (INDEX, innesto I5) |
| Salvatore Mercante | esplorazione | **4 — la sparizione** | è già una quest di recupero: la famiglia costa zero |
| Ghostlord | politica | — | i tre rami esistenti fanno già il lavoro |
| Campi Drow | infiltrazione (Andor) | — | procedurale, non deduttivo: giusto così |
| Rethmar (battaglia finale) | guerra | — | il dominante torna, ed è giusto che torni **alla fine** |
| P1A/P1B/P1C (Hellas, Treant, Rituale) | esplorazione / rito | — | ⚠️ **sono il primo blocco dell'arco: puliti** (regola anti-ritmo 3) |
| Rhest · Starsong Hill · Missioni CR12 | battaglia / esplorazione | — | il fondo neutro che fa risaltare gli speciali (§6.2 riga 1) |

🔎 **La questione «un congegno per arco» è risolta dal §6.3**, non lasciata
aperta: ARC-09 è modulare e vale più di un arco lineare, quindi il tetto è
**2** — la Torre (congegno da solo, senza indagine attorno) e **un secondo
dentro il modulo-picco**, quello che porta mistero *e* congegno insieme.
Quale sia il modulo-picco **non si decide adesso**: si sceglie ai 2/3
dell'arco fra i rami ancora da giocare (regola anti-ritmo 4, il gettone che
resta in mano).

⚠️ **Resta al DM** una sola decisione, non delegabile: se ARC-09 vada
contato come **un arco** o come **due** ai fini della regola 3. Se due, i
congegni diventano 2 + 2 e la quota sopra va rifatta su due metà.

## 9. Autocontrollo, prima di dichiarare un arco pronto

1. Le cinque righe della tavolozza sono compilate, `«nessuna»` incluse?
2. Il dominante è diverso da quello dell'arco precedente?
3. Il contrappunto è la cura del difetto del dominante (§2, ultima colonna)?
4. So indicare **quale sessione** è il quarto d'arco che gioca diverso?
5. Il picco è di un tipo diverso dal picco precedente?
6. Prova del recap: tolti i nomi propri, questo arco suona come il
   precedente?
7. **Se l'arco è modulare**: la quota del §6.2 è scritta, i moduli hanno le
   loro **vocazioni** (§7 livello 1), e il conto aperto è aggiornato?
8. **Gli speciali sono la minoranza?** (4 su 10. Se sono 6, l'arco non ha
   più un fondo neutro e niente risalta.)
9. **C'è un gettone ancora in mano?** (Regola anti-ritmo 4: se hai assegnato
   tutto all'inizio, hai scritto un calendario.)
10. **Il primo modulo è pulito?**
