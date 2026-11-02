# ADR-0096 — La battaglia campale di Hammerfist si gioca con un libretto

**Stato**: proposta
**Data**: 2026-10-21
**Decisione-fonte**: richiesta del DM del 2026-10-21 nel thread di PIANO-MASTER-DEF («un libretto comune di poche pagine sia per i giocatori e i dm … ogni pregen avrà il suo gruppo di armata se possibile da gestire»); simulazioni in `plans/esperimenti/battaglia-campale-2026-10-21/`

## Contesto

Con D4 il flashback dei pregenerati resta prima di Hammerfist. Il DM vuole che
i giocatori provino qualcosa di diverso: l'assedio come battaglia campale, con
regole semplici e lo stesso libretto per giocatori e DM. Il sistema canonico
(`mass_combat_guide_Dm.md`, `ARC08-02` §4) fa tirare l'attacco dell'orda al
DM, e non dice cosa fa un eroe dentro la battaglia di massa. Il Fronte di
ARC-09 (D13) è invece un contatore nascosto del DM, quindi Hammerfist è
l'unico posto in cui il tavolo muove le truppe.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| Libretto con il sistema canonico rovesciato: i giocatori tirano attacco e difesa, l'eroe ha quattro gesti | stesse probabilità del canonico; i dadi sono tutti in mano al tavolo; si può tarare con una simulazione | regole nuove da insegnare: serve una Sessione 0 |
| Sistema canonico così com'è | niente da scrivere | il DM tira metà dei dadi; l'eroe non ha un ruolo nella massa |
| Solo i pregen sulla mappa, la battaglia raccontata | nessuna regola nuova | non è quello che il DM ha chiesto; diventa il modo A del libretto |

## Decisione

L'assedio dei pregen si gioca con `ARC08-18-LIBRETTO-BATTAGLIA-CAMPALE.md`:
una tabella sola, tre ordini, quattro gesti dell'eroe, la pressione che apre
le brecce, tre modi di giocare (solo l'eroe, l'eroe con due reparti, il
capitano con tre). Il dado bianco della difesa è il tiro d'attacco dell'orda
rovesciato (d20 + DU contro 22 + AU), con la stessa probabilità.

Le sessioni coi pregen restano tre. La Sessione 1 comincia con la lettura del
libretto e finisce con la scaramuccia dell'avanguardia: squadre di guastatori
che scavano trappole finché l'orda non le scaccia, e ogni trappola annulla una
tacca del primo giorno (`ARC08-10` §5.4-bis). Ogni settore ha il suo terreno e
le sue macchine, ogni reparto una capacità; quelle dell'orda il DM le tiene in
un file suo (`ARC08-19`). Il morale sui dadi conta al massimo ±2. Chi non vuole
un pregen gioca il capitano o l'orda (libretto §9). Ogni pregen ha una carta
dei poteri con i numeri già calcolati (`ARC08-15`, handout 1-4 bis). L'orda di default è quella feroce (+1 ad AU e DU sulla normale), con
una terza manopola terrificante, per la preferenza del DM per la versione
più forte.

## Conseguenze

- Nelle simulazioni della v2 (3.000 battaglie per variante) nessun ordine
  fisso vince: tenere sempre chiude i giorni 1-2 senza brecce il 9% delle
  volte, caricare sempre perde quasi tutti i reparti.
- Con il terreno, le capacità e le baliste (v3) i nani sono più forti, e
  l'orda del libretto sale di uno. Con l'orda feroce e tre-sei trappole la
  breccia resta chiusa il 73% delle volte e le posizioni tengono il 55%;
  normale 90% e 86%, terrificante 45% e 18%.
- Il morale senza tetto sui dadi faceva crollare tutto: un punto di morale
  all'alba spostava la breccia «pieno» dal 73% al 50%. Il tetto di ±2 lo
  contiene ma non lo toglie, e per questo l'avanguardia non tocca il morale
  né i reparti delle mura: costa solo le trappole.
- Nell'avanguardia ritirarsi dopo il terzo o quarto round porta a casa circa
  cinque trappole; restare fino al sesto ne porta due e perde tre squadre su
  quattro.
- Il modo C ferma la breccia quanto il modo B ma perde più reparti (v2).
- Le letture a freddo di un giocatore e di un DM hanno trovato un errore di
  uno nel dado bianco; corretto nel libretto e nel simulatore.
- Le carte dei comandanti, la palla di fuoco, il Fuoco di copertura e la
  retroguardia non sono simulati e restano `[INFERRED]`.
- Le schede dei pregen negli handout 1-4 sono state portate ai numeri del
  Bestiario, e ognuna ha la sua carta dei poteri.
- Manca la prova al tavolo, che è il solo modo di sapere se è divertente.

**Da rivedere se**: nella scaramuccia della Sessione 1 un round dura più di cinque minuti, o i
giocatori del modo B finiscono per scegliere sempre lo stesso ordine.
