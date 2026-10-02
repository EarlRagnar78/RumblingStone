# Il banco: cosa si compra, cosa si vende, e chi storce il naso

<!-- indice: generato da scripts/indice_references.py, non scriverlo a mano -->
**In questo file**

- Quando serve
- Le quattro parti del banco
- La spezia: preferenze e diffidenze
- La misura
<!-- /indice -->

Norma per chi scrive un master. Nasce dal tavolo di `ARC07-DEF-4`, fra il 25 e
il 27 settembre 2026: nella fortezza i giocatori hanno chiesto pergamene di
*silenzio*, *identificare*, *rimuovi maledizione* e *rimuovi paralisi*, hanno
fatto identificare le pozioni, hanno venduto armi e armature naniche anche
d'adamantio, hanno pagato con monete di un altro millennio. Il master non
diceva niente di tutto questo, e il DM l'ha deciso al volo. Le sue decisioni
sono finite in DEF-4 come `[CANONE — DM 2026-09-25/26/27]`, e la Scena 5 di
DEF-4 è oggi l'esempio di riferimento.

Il DM, il 2026-09-27: *«organizza il tutto in modo che i prossimi moduli non
siano carenti, mettendo un po' di diffidenza e preferenze dei mercanti in
particolari condizioni e affiliazioni, se fanno colore: non sempre, come un
pizzico di spezie su un piatto insipido»*.

## Quando serve

Ogni volta che in una scena qualcuno vende: una scheda d'entrata con la riga
**Vende**, oppure la riga *bottega* (o *culto*, o *rimedi*, se vendono) della
tabella **Chi si trova qui** del passo 2 del ciclo. Dove nessuno vende, la riga
dice «nessuno» e il banco non si scrive.

## Le quattro parti del banco

Ogni parte ha i prezzi dell'SRD 3.5 (o PF1e negli stand-alone PF1e) e le
**quantità**: finito il banco, non c'è altro. Una quantità è un fatto del
mondo, e il tavolo la sente più di un prezzo.

**Cosa vende.** Oggetto, prezzo, quante, chi. Le armi e le armature
perfette, le pozioni, le bacchette, le pergamene. Una pergamena costa
livello dell'incantesimo × livello dell'incantatore × 25 mo, più le componenti
costose; una pozione × 50. Chi le scrive non ne fa di nuove in una notte: una
pergamena chiede un giorno di lavoro, quindi il banco ha quelle che ha.

**I servizi.** Chi lancia cosa, e a che livello: livello dell'incantesimo ×
livello dell'incantatore × 10 mo, più le componenti. Si scrive anche **cosa
costa alla comunità**: uno slot speso per i PG è uno slot che manca a qualcun
altro (le mura, il villaggio, la festa). E si controlla che chi lancia abbia
quell'incantesimo nella sua lista: *identificare* è da bardo e da mago (e dal
dominio della Magia), non da ogni chierico.

**Identificare.** È la domanda che torna sempre, quindi il banco la risponde
prima che venga fatta:
- una **pozione** si identifica con Sapienza Magica **CD 25**, un minuto,
  senza ritentare. Il banco dice chi lo fa, con che bonus, e **quanto tempo**
  concede: è lì che sta il limite, non nella prova;
- un **oggetto** si identifica con l'incantesimo *identificare* (un'ora, una
  perla da 100 mo). Con *individuazione del magico* e Sapienza Magica (15 +
  livello) si sa solo la **scuola**;
- se nessuno sul posto sa farlo, il banco lo dice, e dice dove si trova.

**Cosa compra, e a quanto.** Di norma metà del prezzo SRD. Poi i **tetti**,
che sono la cosa che al tavolo manca sempre:
- il **limite d'acquisto** (il massimo per un oggetto solo);
- la **cassa**: quanto ha in tutto chi compra, stanotte;
- in **cosa paga**: monete, gemme, merce, favori.

Il tavolo che vende un tesoro intero deve trovare scritto dove finisce la
cassa. *«Signore, io non ho quattromila monete d'oro»* (kit anti-improvvisazione
della Valle, §2) è una regola, non una scortesia.

## La spezia: preferenze e diffidenze

Facoltativa, e va usata poco: **un mercante per luogo, e non in ogni luogo**.
Un banco con la spezia ovunque è un piatto salato.

Una spezia ha sempre queste quattro cose:

| | |
|---|---|
| **Da dove viene** | una **condizione** del luogo (assedio, carestia, festa, lutto, un furto recente) o un'**affiliazione** (una fazione, un culto, una razza, una gilda, il nemico di turno). Mai il caso |
| **Cosa fa** | un effetto solo, dentro l'SRD: un passo della tabella degli atteggiamenti, un prezzo diverso (da ×0,5 a ×1,5), o un rifiuto |
| **Come si vede** | il mercante lo dice o lo mostra, anche se non lo spiega. Gunnvor conta tutto in *braccia*: il tavolo capisce da sé cosa le interessa |
| **Che via lascia** | chi la capisce la può usare: portare ciò che serve, coprire un simbolo, offrire un favore invece dell'oro |

Esempi, tutti da DEF-4 tranne gli ultimi due:

| Condizione o affiliazione | Preferenza o diffidenza | Effetto |
|---|---|---|
| assedio | paga ciò che arma o cura un difensore, non i gioielli | ×1,5 su armi, cure e munizioni; metà in gemme sul resto |
| il simbolo del nemico, in vista | diffidenza | parte **ostile** invece di indifferente |
| monete di un regno che nessuno conosce | le pesa | vale il peso, e una su dieci resta al pesatore |
| merce presa al drago che sta sopra le loro teste | rifiuto | la getta a terra |
| armi naniche d'adamantio, fra nani | preferenza | il re paga oltre il limite d'acquisto |
| un mago di passaggio | preferisce un **favore** all'oro | il servizio costa un favore, non monete |
| una carestia | il cibo vale più della magia | razioni al doppio, oggetti magici a metà del solito |

⚠️ La spezia non è una punizione. Se toglie qualcosa al gruppo (un prezzo più
alto, un rifiuto), deve lasciare una via; se non la lascia, è una porta chiusa
e va scritta come tale, fuori dalla spezia.

## La misura

- `copertura_scene.py --check`, regola **C6**: una scena in cui qualcuno vende
  e che non porta un solo prezzo in mo. Vede che il banco c'è, non che sia
  completo.
- Le quantità, i tetti e l'identificazione li chiede il playtester a freddo,
  nel codice `P-ABITATO`.
- La spezia **non si misura**: è facoltativa per costruzione, e un cancello che
  la chiedesse la metterebbe dappertutto, che è l'errore che questa pagina
  vieta.
