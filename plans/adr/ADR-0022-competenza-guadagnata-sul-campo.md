# ADR-0022 — La competenza si guadagna sul campo, ma con un tetto

**Stato**: accettata
**Data**: 2026-08-25
**Decisione-fonte**: richiesta DM del 2026-08-25 — *«alla fine di un'indagine
premiare quelli che hanno usato di più e spremuto le meningi regalando dei
punti abilità nelle skills appropriate, in modo tale che anche se nel gruppo
non c'è un ladro possano in qualche modo come gruppo sopperire»*
**Piano**: [`PIANO-INDAGINE-E-DEDUZIONE`](../PIANO-INDAGINE-E-DEDUZIONE.md) (Lotto I1)

## Contesto

I quattro PG di questa campagna hanno schede costruite per il combattimento:
i punti abilità sono andati dove servivano a sopravvivere, non su Cercare,
Raccogliere Informazioni, Intuizione o Sapienza. Non è un errore dei
giocatori — è una scelta razionale in una campagna che finora ha premiato
quello.

La conseguenza è che **un caso investigativo, scritto secondo le CD del
manuale, li escluderebbe dal proprio stesso gioco**: il ladro assente
diventa un buco strutturale, e i tre presenti guardano tirare l'unico che
può.

Il DM ha chiesto due cose insieme: che chiunque possa *provarci* comunque, e
che chi ci prova e ci riesce **porti a casa qualcosa che resta**.

La seconda metà è quella pericolosa. Gradi veri, regalati senza limite, al
decimo caso producono due danni che si vedono tardi e non si disfano:

1. **inflazione di scheda**: un guerriero con dieci gradi gratis in Cercare
   ha una scheda che nessuno ha progettato e che il bilanciamento degli
   incontri non conosce;
2. **erosione della classe**: se tutti hanno Cercare, nessuno *è* quello
   che cerca, e il giorno in cui un ladro entra nel gruppo scopre che il suo
   mestiere è già coperto.

## Decisione

Si adottano **due monete distinte**, e solo la seconda tocca la scheda.

### 1. Acume — per-PG, si spende nel caso, si azzera alla fine

Si guadagna **nel momento** in cui un giocatore fa la cosa che vogliamo
premiare (una deduzione a voce, una porta grezza aperta con la
caratteristica, due indizi collegati). Si spende subito: +2 a una prova
investigativa, una domanda sì/no al DM sulla scena, o la conversione di un
Fatto in Lettura senza tirare.

**Non tocca la scheda e non sopravvive al caso.** È la moneta che fa il
lavoro motivazionale vero, perché il premio arriva nella stessa scena
dell'intuizione e non tre settimane dopo.

### 2. Perizia — permanente, e col tetto

A fine caso, ogni PG deposita una **perizia** in *un'abilità che ha
davvero usato nella finzione* (non una che gli piacerebbe avere).

- **Tre perizie nella stessa abilità = 1 grado vero**, permanente.
- Il grado così ottenuto conta come **abilità di classe** per quel PG in
  quella sola abilità: l'ha imparata sul campo, non a scuola.
- **Tetto duro: 1 grado da questo sistema per PG per livello.** Non si
  accumula arretrato: un livello saltato è perso.
- Vale il massimale SRD normale (grado massimo = livello + 3 per abilità di
  classe). Un grado da Perizia che sfonderebbe il massimale **non si
  assegna**: la perizia resta in banca fino al livello successivo.
- Le abilità **solo per addestrati** (Sapienza, Decifrare Scritture,
  Disattivare Congegni, Artigianato Magico…) si possono aprire così — è
  proprio il caso d'uso: il primo grado è quello che consente di provarci.

### 3. Il Metodo — di gruppo, non di scheda

Il gruppo che chiude casi accumula un **Metodo** condiviso (una tecnica
d'indagine dichiarata, usabile una volta per caso). È un bene del gruppo,
non una riga sulla scheda di nessuno, e sopravvive ai cambi di
composizione. È la risposta diretta a *«sopperire come gruppo»*.

Il dettaglio operativo delle tre monete vive in
[`skills/rumblingstone-indagine/references/registro-e-ricompense.md`](../../skills/rumblingstone-indagine/references/registro-e-ricompense.md).

## Conseguenze

- **Il tetto è la decisione, non un dettaglio.** Con 1 grado/livello, dopo
  cinque casi un guerriero ha due o tre gradi in Cercare: abbastanza per
  tentare la prova, mai abbastanza per sostituire un ladro. Se si toglie il
  tetto, questo ADR non regge più e va riaperto.
- **Serve un registro scritto**, altrimenti in tre sessioni nessuno ricorda
  chi ha depositato cosa. Formato in `registro-e-ricompense.md` §4; vive
  accanto allo XP ledger nel branch di gruppo ([ADR-0007](ADR-0007-scritture-canone-triplo-vincolo.md)).
- **La scheda cambia fuori dal salire di livello.** È uno strappo alla
  procedura 3.5 ed è consapevole: la contropartita è che il cambiamento è
  guadagnato in scena e tracciato per iscritto.
- **Da rivedere dopo il primo caso giocato** (Lotto I5 del piano): i due
  numeri da tarare sono il tetto (1/livello) e il costo di un grado (3
  perizie). Sono scelti a tavolino, non collaudati.
- Se un giocatore costruisce apposta un PG che accumula perizie in fretta,
  la regola ha funzionato: sta giocando l'indagine. Il tetto lo trattiene
  comunque.
