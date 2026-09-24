# Il nodo d'indizio e le sei porte

Il pezzo di meccanica che regge tutto il resto. Se salti questo file e scrivi
indizi come «Cercare CD 20 per trovare la lettera», hai scritto un caso che
si apre con una sola chiave e che tre giocatori su quattro guarderanno da
fuori.

---

## 1. Il nodo a tre strati

Un indizio non è un'informazione: è **tre informazioni impilate**, e si
distribuiscono in modo diverso.

| Strato | Cos'è | Come si ottiene |
|---|---|---|
| **Fatto** | quello che c'è, oggettivamente. Descrivibile senza interpretarlo. | **gratis.** Si dà a chi guarda. Non si tira. |
| **Lettura** | cosa significa quel fatto | **una prova** — d'abilità o grezza, una qualsiasi delle porte aperte sul nodo |
| **Nome** | chi, che cosa, quale precisamente | **gradi veri**, oppure l'incrocio di due Letture già ottenute |

Esempio, lo stesso nodo:

```
FATTO    La porta della cripta è stata forzata — le schegge del legno
         sono cadute verso il corridoio.
LETTURA  Chi l'ha forzata era DENTRO. Non stava entrando: stava uscendo.
NOME     Il sigillo sul chiavistello è quello del custode delle chiavi
         del tempio: lì dentro poteva entrarci solo lui, e col permesso.
```

**Perché funziona**: il Fatto regalato mantiene il caso in movimento
qualunque cosa dicano i dadi; la Lettura è il punto in cui i giocatori
lavorano; il Nome resta il premio di chi ha speso i punti (e di chi li ha
guadagnati sul campo — vedi `registro-e-ricompense.md`).

**La regola dura**: se un Fatto è necessario per andare avanti, **non lo si
tira. Mai.** Nessuna CD, nessuna prova passiva, nessun «se qualcuno pensa di
guardare». Si descrive. Il gioco è capire cosa vuol dire, non accorgersi che
c'è.

## 2. Le sei porte, per esteso

Ogni nodo dichiara **almeno tre** porte, **almeno una fisica** (FOR/DES/COS).
Ogni porta restituisce un **pezzo diverso** della Lettura, mai la stessa
frase a CD diversa.

### FOR — la prova della forza che ci è voluta
Il giocatore prova a rifarlo: solleva, spinge, forza. Restituisce **quanti
erano** o **quanto era forte** chi ha agito.
> *«Ci provi. La lastra si muove di un dito e ti si spegne il fiato. Uno solo
> non la sposta. E qualcuno l'ha spostata.»*

### DES — la ricostruzione del gesto
Ripercorre il movimento, rifà il salto, controlla l'angolo. Restituisce
**come** è andata: la traiettoria, la mano, il punto da cui è partito il
colpo.
> *«Ti metti dove stava lui. Da qui, per colpire così, dovevi essere mancino.
> O tenere qualcosa nell'altra mano.»*

### COS — quello che sa il corpo
Quanto si resiste a una ferita così, quanto fa male quel veleno, quanto
freddo fa in questa stanza, quanta strada si fa in una notte. Restituisce
**quando** e **quanto è durato**.
> *«Con quella ferita non si muore subito. Tu lo sai. Ha avuto tempo di
> arrivare fin qui — e ha scelto di venire proprio qui.»*

### INT — il conto che non torna
La deduzione classica: il collegamento, il numero sbagliato, la cosa che
implica un'altra cosa. Restituisce il **perché**, e spesso il Nome.

### SAG — quello che è fuori posto
Percezione e lettura delle persone: l'agio che manca, il dettaglio che
stona, la faccia che ha esitato mezzo secondo di troppo. Restituisce **cosa**
è sbagliato in questa scena, senza dire ancora perché.

### CAR — farlo dire a qualcuno
Con le buone, con le cattive o con la faccia tosta. Restituisce quello che
nessun oggetto può dire: l'intenzione, la voce, quello che si è taciuto.
> Nota: CAR è l'unica porta che **produce conseguenze sociali**. Chi la usa
> lascia una traccia: qualcuno sa che avete chiesto. Scrivi la traccia.

### Le porte che NON esistono
Non si aprono porte su una caratteristica solo per farle esistere tutte e
sei. Tre porte vere valgono più di sei finte. Se non ti viene in mente cosa
restituisce FOR su questo nodo, **quel nodo non ha una porta FOR** — mettila
sul nodo dopo.

## 3. Le CD, e il rapporto con le abilità normali

La prova grezza è **d20 + modificatore di caratteristica, nessun grado**
(`dnd-35-srd/references/core-mechanics.md`: *ability check*).

| Situazione | CD |
|---|---|
| Il pezzo di Lettura sta lì e basta guardarlo bene | **10** |
| Il pezzo richiede di provarci davvero (rifare il gesto, insistere) | **15** |
| Il pezzo è nascosto o controintuitivo | **20** |
| Il **Nome** — l'identificazione precisa | **25**, e serve un grado o l'incrocio di due Letture |

Le prove d'abilità normali non spariscono e non vengono svalutate: **l'abilità
addestrata prende la Lettura *e* si avvicina al Nome con lo stesso tiro**, la
porta grezza prende solo il suo pezzo di Lettura. Chi ha speso i punti resta
più veloce. Chi non li ha spesi resta *dentro*.

Abilità **solo per addestrati** (Sapienza, Decifrare Scritture, Disattivare
Congegni, Artigianato Magico) restano tali: la porta grezza non le aggira —
gira **intorno** a loro, dando un pezzo di Lettura per via fisica o sociale.
Un'iscrizione che nessuno sa leggere si affronta con COS (da quanto è
incisa), DES (con che utensile), CAR (chi in città legge questa lingua) — mai
con «INT CD 15 per capire cosa c'è scritto».

**Aiutare un altro** (*aid another*, CD 10, +2): sempre disponibile e da
incoraggiare, ma non sostituisce una porta propria. Un giocatore che passa
la serata a dare +2 a un altro non sta giocando.

## 4. La mappa dei nodi — come si tengono insieme

Un caso non è una catena, è **una rete ridondante**. Regola di costruzione:

> **Ogni conclusione necessaria è raggiungibile da almeno due nodi diversi,
> e ogni nodo si apre da almeno due porte diverse.**

Con 6-9 nodi si ottiene una rete che regge qualunque cosa faccia il tavolo.
Formato di scrittura, uno per nodo:

```
### N3 — Il registro del molo
PORTE      SAG 15 (le pagine sono numerate a mano: ne mancano due)
           FOR 10 (il registro è stato strappato, non tagliato: mano forte)
           CAR 15 (il capitano dice a chi l'ha dato — se gli si dà un motivo)
FATTO      Il registro degli attracchi si interrompe fra il 3 e il 6 di Eleint.
LETTURA    In quei due giorni è entrato qualcosa che non doveva risultare.
NOME       [incrocio con N5] La stessa mano ha firmato la ricevuta del sale.
PORTA A    N5 (la ricevuta), N7 (il magazzino)
INNOCENZA  «Il vecchio Berrun perde le pagine, è mezzo cieco» — e per metà
           del caso è vero, perché Berrun È mezzo cieco.
```

Il campo **INNOCENZA** è obbligatorio: è la spiegazione banale che regge
finché non arriva la chiave di lettura. Un nodo senza innocenza è un nodo che
urla «sono un indizio», e brucia la sorpresa della ricomposizione
(`congegno-e-enigmi.md` §2).

## 5. Il vicolo cieco — cosa fa il DM quando non trovano niente

Non esiste, se hai costruito la rete del §4. Ma la sessione vera trova sempre
il modo, quindi: **tre mosse, in quest'ordine, e nessuna di queste è
"rivelare".**

1. **Il mondo si muove** (`narrative-style/references/living-world.md`). Non
   dai un indizio: fai agire il colpevole. Qualcuno scappa, qualcosa brucia,
   un testimone cambia versione. Il caso avanza perché *l'avversario*
   avanza, e i PG inseguono. Questa è la mossa giusta nove volte su dieci.
2. **Il Fatto già dato torna in scena.** Non aggiungi informazione: la
   ripeti in un contesto nuovo, dove pesa diversamente. («La cameriera porta
   il vino. Ha le maniche bagnate — come il tizio del molo.»)
3. **Si paga il costo.** Il tempo scorre, il congegno avanza di uno stadio, e
   il caso continua da una posizione peggiore. **Un caso non si risolve
   sempre in tempo, e va benissimo**: un caso perso è la sessione che si
   ricorderanno.

Quello che **non** si fa: far apparire un PNG che spiega, far tirare
«qualcuno tiri Intuizione» a vuoto finché non passa qualcuno, o annunciare la
soluzione perché è tardi. Se è tardi, si paga il costo e si va a casa con la
cosa irrisolta addosso.

## 6. Errori che questo file esiste per prevenire

| Errore | Perché è un errore | Cosa fare invece |
|---|---|---|
| «Cercare CD 20, se falliscono non trovano la lettera» | un tiro cancella il caso | la lettera è un Fatto; il tiro dà cosa la lettera *significa* |
| Sei porte su ogni nodo | tre sono finte e il tavolo se ne accorge | tre porte vere, una fisica |
| La porta FOR dà la stessa cosa della porta INT | è uno sconto, non un taglio | pezzi diversi della stessa Lettura |
| Tutti gli indizi sono strani | niente sorprende, la ricomposizione è piatta | ogni scheggia ha la sua INNOCENZA |
| Il PNG esperto che riassume | il tavolo smette di pensare | il mondo si muove (§5.1) |
| Una sola catena di indizi | si spezza al primo tiro sfortunato | rete ridondante (§4) |
