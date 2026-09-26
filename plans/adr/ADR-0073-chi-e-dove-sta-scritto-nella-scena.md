# ADR-0073 — Chi e dove sta scritto nella scena

- **Stato**: accettata
- **Data**: 2026-09-26
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: il DM, lo stesso giorno: *«nell'avventura così come è
  scritta mancano davvero le descrizioni delle stanze e dei png che
  incontrano»*; *«vedi se si può implementare un ruolo lettore e playtester […]
  il lettore deve puntare sulla leggibilità e comprensione e il playtester
  sulla giocabilità […] integrato in maniera deterministica come gli altri
  test»*; sull'ordine, *«prima lo strumento lettore-playtester poi def 4»*
- **Rapporti**: misura la norma di `rumblingstone-module-standard` sulla scheda
  d'entrata (canone dalla #169); estende `rumblingstone-playtest` con due ruoli;
  piano: [PIANO-LETTORE-E-PLAYTESTER](../PIANO-LETTORE-E-PLAYTESTER.md)

## Contesto

Il 2026-09-25 il gruppo ha giocato `ARC07-DEF-4` fino alla soglia del campo
nemico, e il DM ha dovuto inventare sul momento sette cose che il master non
diceva: tre luoghi (i quartieri, le gallerie, la cappella con la sua
chierica), tre persone (l'alchimista, il capitano delle mura, l'araldo) e le
guardie della tenda, che avevano numeri ma nessun volto. Tutti i cancelli del
repo erano verdi.

La norma c'era. Da luglio `module-standard` scrive che la scheda d'entrata del
PNG sta nella scena in cui i PG lo incontrano. Ma nessuno strumento la misurava,
ed è la situazione che ADR-0056 descrive: una norma senza misura non fa rumore
quando viene ignorata.

C'è poi un limite di fondo: **uno script non vede quello che il testo non
nomina**. Un capitano che nessuno ha scritto non lascia traccia da cercare.

## La decisione

Lo strumento ha due metà, con due compiti diversi.

1. **Due letture a freddo**, fatte da un agente con una rubrica fissa: il
   **lettore** (leggibilità e comprensione: cosa manca per capire) e il
   **playtester** (giocabilità: cosa succede quando i giocatori fanno quello
   che vogliono). Ricevono solo il modulo. Consegnano rilievi con codice,
   gravità e la riga che fa da prova. **Non sono un cancello**: trovano.
2. **`scripts/copertura_scene.py`**, in CI, che impedisce che ciò che è stato
   trovato si ripeta:
   - **C1**: ogni scena ha almeno un box read-aloud;
   - **C2**: chi ha un'etichetta di battuta ha una scheda d'entrata, o una riga
     nel foglio del cast dello stand-alone;
   - **C3**: il **contratto «In scena»**. Ogni scena apre con
     `**In scena** — Dove: … — Chi: …`; ogni luogo ha un box che lo nomina
     nell'etichetta, ogni persona una scheda d'entrata o una riga in una
     tabella **Comparse** del modulo, messa dove la si incontra la prima volta;
   - **C4**: nessuna scheda o battuta della scena sta fuori dal suo *Chi*.

Il contratto è la risposta al limite di fondo. Non si può misurare un'assenza,
ma si può chiedere a chi scrive di **fare l'elenco**, e poi misurare l'elenco.
C4 lo tiene onesto per tutto quello che il testo nomina. Quello che il testo non
nomina resta compito del lettore.

Profili e residui stanno in `plans/copertura-scene.json`. Ogni residuo ha la sua
ragione, e un residuo che smette di verificarsi fa fallire il cancello finché
non lo si toglie. Un master `ARC*-DEF-*` che il file non elenca prende il
profilo severo, contratto compreso: i master nuovi di ARC-08 e ARC-09 nascono
sotto il cancello.

## Alternative scartate

- **Solo le letture a freddo.** Trovano molto: su DEF-4, 107 rilievi fra le
  due. Ma non sono ripetibili, e un difetto trovato una volta tornerebbe al
  master successivo.
- **Solo lo script, con regex più furbe.** Provate e misurate. «Luogo annunciato
  in grassetto senza box» ha dato 1 segnalazione vera su 6. «CD senza chi la
  tira» ha dato quasi solo falsi positivi. Entrambe scartate.
- **Una lista di ruoli da cercare** (capitano, araldo, alchimista…). Sarebbe il
  metro tarato sul campione, cioè l'errore che G6 elenca per primo.

## Conseguenze

- **Pro**: la calibrazione sul DEF-4 del tavolo trova tutte e sette le lacune,
  4 in pieno e 3 in parte, e nessuna delle tre metà da sola ne trova più di due.
  Fra le altre cose, le letture trovano due difetti già noti per altra via:
  l'invisibilità a 120 minuti e l'età di Balvar.
- **Contro**: il contratto è una riga in più per ogni scena, e va in stampa. È
  apparato per il DM, come la scheda d'entrata, e resta sotto la soglia del box.
- **Contro**: le letture costano un agente per modulo, e due letture non danno
  mai lo stesso elenco. Nel repo non c'è ancora una misura dell'affidabilità di
  un giudice-agente (l'unico κ, quello di MQM, non è informativo).
- **Debito dichiarato**: 22 residui al 2026-09-26, tutti con la ragione e un
  lotto nel piano (F4 i master di ARC-07, F5 gli stand-alone).
