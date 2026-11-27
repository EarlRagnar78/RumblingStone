# ADR-0156 — Il giocato sta sul ramo di gruppo, e main resta rigiocabile

**Stato**: accettata (2026-11-27, parola di Jfs)
**Data**: 2026-11-27
**Decisione-fonte**: Jfs, 2026-11-27, nel thread di preparazione della serata del 30/11: «l'allineamento di cosa è stato fatto dai giocatori va soltanto nella campagna dei rumblingstone in modulo presenti ancora le scelte e permetta di essere rigiocato da un altro futuro gruppo».
**Rapporti**: estende [ADR-0007](ADR-0007-scritture-canone-triplo-vincolo.md) (il canone vivo si scrive solo su un ramo di gruppo), [ADR-0090](ADR-0090-la-partita-riparte-su-un-ramo-di-gruppo-nuovo.md) (il ramo vivo del primo tavolo è `campaign-group-rumblingstone`) e [ADR-0149](ADR-0149-il-giocato-arriva-sul-ramo-di-gruppo-con-un-agente-e-una-misura.md) (il giocato arriva sul ramo con un agente e una misura).

> Il numero 0155 è il primo libero per `validate_docs.py --prossimo-adr` su
> main `21906369`; nessun ramo aperto porta un ADR da 0155 in su. Non è in
> `plans/adr-prenotati.json`, che si scrive solo su main: la PR lo dichiara.

## Contesto

ADR-0007 vieta agli script di scrivere canone vivo su main, e ADR-0149 porta
il giocato sul ramo di gruppo. Nessuno dei due dice che cosa può stare nei
master di main quando lo scrive una persona o un agente a mano. Così su main
sono rimasti fatti del primo tavolo, misurati il 27/11 su
`ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`:

- §8 A, r.4142: il blocco «Il gruppo di oggi, dal registro dei PX», con i PX
  di Hella e degli altri tre `[CANONE — DM 2026-11-05, P16, PX]`;
- r.83 e r.3103: «il gruppo di oggi» riprende dalla notte, e si è fermato a
  metà atto;
- §8 A, fino a questa PR: «Hella prende il 14° in questa notte», con il conto
  dei PX che le mancano;
- `campaign/REGISTRO-PX.md` su main, copia del foglio dei PX del gruppo al
  2026-11-05;
- `ARC07-DEF-5` r.942: «Hella li raggiunge durante la notte di `DEF-4`».

Un gruppo nuovo che apre questi master li trova già decisi dove dovrebbero
restare aperti.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Il giocato solo sul ramo di gruppo, main con le scelte aperte** | main resta un modulo che un altro gruppo può giocare da capo; è la parola di Jfs | ogni riga di giocato già su main va trovata e spostata, una per una |
| Tenere il giocato su main dentro un blocco marcato («Il gruppo di oggi») | si legge accanto alla regola | il master di un gruppo nuovo esce con i numeri di un altro tavolo; il marcatore non lo toglie dalla stampa |
| Due edizioni del master su main, neutra e del gruppo | entrambe a portata di mano | due testi che divergono al primo ritocco, cioè il problema che ADR-0007 voleva evitare |

## Decisione

**Quello che i giocatori hanno fatto si scrive solo sul ramo di gruppo; main
tiene il modulo con le scelte ancora aperte, perché un altro gruppo lo possa
rigiocare.**

- Vanno sul ramo di gruppo: i log di sessione, il registro dei PX, lo stato,
  i booklet che ripartono dal punto giocato, le tavole e i prompt che
  ritraggono i PG del gruppo.
- Su main una regola dice che cosa succede per ogni scelta, senza dire quale
  ha fatto il gruppo: dove serviva il conto di un tavolo, il master rimanda
  al registro del ramo di gruppo.
- I residui di giocato su main si neutralizzano uno per uno, su decisione del
  DM. La frase tolta resta nell'apparato o nella tabella «Cosa è cambiato»
  del master, con la data.
- Le domande al DM portano «ramo» se la risposta è giocato, «main» se è una
  regola che vale per ogni gruppo.

## Conseguenze

- Un gruppo nuovo parte da main con `dm.py gruppo nuovo` e trova i master
  aperti; il primo tavolo trova il suo giocato sul suo ramo.
- Il primo residuo è neutralizzato in questa PR: la frase su Hella al 14° in
  DEF-4 §8 A, ora un rimando a `campaign/REGISTRO-PX.md` sul ramo
  `campaign-group-rumblingstone`.
- Quello che si paga: restano su main il blocco «Il gruppo di oggi» di DEF-4
  §8 A, le righe 83 e 3103 di DEF-4, la r.942 di DEF-5 e
  `campaign/REGISTRO-PX.md`. Toglierli tocca canone marcato del 05/11, e lo
  decide il DM (domanda 14 della serata del 30/11). Fino ad allora la regola
  vale per le scritture nuove, non per quelle vecchie.
- Nessun cancello lo misura ancora: «giocato» contro «regola» è un giudizio,
  e un rilevatore di frasi come «il gruppo di oggi» darebbe falsi positivi
  sui box che parlano al tavolo. Lo fanno il custode del canone e la colonna
  «Dove» delle domande al DM.

**Da rivedere se**: un secondo gruppo comincia a giocare da main e trova un
master che dà per fatta una scelta del primo tavolo; o il DM decide di tenere
su main un esempio giocato, marcato come tale.
