# ADR-0071 — Gli artefatti crescono per stadi, e ogni pagina ha una versione

- **Stato**: accettata
- **Data**: 2026-09-25
- **Numero**: 0071 e non 0070, che la PR #175 (in bozza) ha già preso per l'apparato di lavoro fuori dalla stampa
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: tre richieste del DM dello stesso giorno. *«Si deve
  arrivare a 4 schede per la corona: zero gemme, 1 gemma, 2 gemme, e poi con
  tutte e tre… una cosa simile per l'anello e per i bracciali… degli artefatti
  che crescono di potere facendo rituali o sbloccando o che aprono quest, in
  modo simile a Weapons of Legacy»*; *«ci deve essere anche una controparte DM,
  altrimenti sarà difficile gestirli»*; *«non c'è stato mai un versionamento,
  che credo sia la scelta migliore in questo caso»*
- **Rapporti**: applica D9/D10 del piano ARC-07 (`PG/Artefatti/` è la fonte,
  i file superati si archiviano e non si cancellano); lascia a
  [ADR-0007](ADR-0007-scritture-canone-triplo-vincolo.md) la scrittura
  dello stadio raggiunto in `state.md`

## Contesto

Il 2026-09-25 il DM ha segnalato che la pagina a due gemme della Corona era
meno completa di quella a una gemma. L'audit
(`PG/Artefatti/ARTEFATTI-AUDIT-POTERI-2026-09-25.md`) ha trovato di peggio:

- la cartella della Corona aveva 14 file di testo, 4 HTML e 2 PDF, e **nessuno
  diceva quale fosse la versione viva**;
- la pagina DM a due gemme portava ancora i Doni superati il 2026-09-12, e le
  pagine di Aegis Fang il *Filo dell'Ascia*;
- i moduli giocati davano poteri (i bonus di quando Thorik ha indossato la
  Corona, i tre poteri del Topazio, la Risonanza con Aegis Fang) che nessuna
  scheda successiva aveva riportato;
- l'Anello aveva uno stadio intero, quello delle due divinità, scritto in un
  PDF e sparito dalle versioni dopo.

Il meccanismo era sempre lo stesso: una pagina si riscriveva sul posto, la
stesura prima spariva dall'albero, e la successiva ripartiva da quella più
vicina invece che dalla più completa.

## La decisione

1. **Un artefatto cresce per stadi.** Uno stadio si apre con un rituale, una
   quest o una scelta del giocatore, e ha un prezzo: la forma è quella di
   *Weapons of Legacy* `[Private — WotC 2005]`, di cui qui si usa solo la
   struttura. Gli stadi di ogni artefatto sono nella tabella «progressione»
   della sua pagina DM.
2. **Ogni stadio ha due pagine**: una per il giocatore, che dice cosa ha e
   cosa lo aspetta senza svelare quello che il tavolo deve scoprire, e una per
   il DM, che ripete la pagina del giocatore e aggiunge da «Solo DM» in poi le
   fonti, le scene, le domande aperte. Uno stadio senza poteri scritti ha solo
   la pagina DM, che lo dice.
3. **Ogni pagina ha una versione**, nella meta
   `<meta name="versione-artefatto" content="artefatto · S<stadio> · r<revisione> · <data>">`
   e in fondo alla pagina. La revisione sale a ogni modifica del contenuto.
   Sulla pagina del giocatore il piede dice **solo la versione**: il percorso
   del registro e i nomi dei file sono apparato di lavoro, e non vanno in
   stampa ([ADR-0070](ADR-0070-l-apparato-di-lavoro-non-va-in-stampa-e-ogni-pagina-si-stampa-una-volta.md)).
   La pagina DM li tiene, perché è lì che il DM li cerca.
4. **Il registro è uno**: la tabella `<!-- versioni-artefatti -->` in
   `PG/Artefatti/ARTEFATTI-MATRICE-VERSIONI.md` §0.
5. **La revisione superata si archivia** in `_ARCHIVIO/` della cartella
   dell'artefatto, con un banner, e perde la meta.
6. **Il gate** è `scripts/tests/test_versioni_artefatti.py`: fallisce se una
   pagina registrata manca o dice un'altra versione, se una pagina viva porta
   una versione che il registro non conosce, se una pagina archiviata porta
   ancora la meta.

Quale stadio sia raggiunto al tavolo **non** è in questo registro: lo scrive
`state.md` §6 sul ramo del gruppo. Il registro dice quale pagina stampare per
ogni stadio.

## Le conseguenze

- **Quello che si guadagna**: una pagina viva per stadio, riconoscibile da
  chiunque apra la cartella; le versioni vecchie leggibili senza `git`; e una
  domanda precisa per ogni stadio che nessuno ha ancora scritto.
- **Quello che si paga**: il doppio delle pagine, e ogni modifica tocca tre
  posti (pagina giocatore, pagina DM, registro). Il test prende il terzo; i
  primi due restano disciplina.
- **Cosa il gate non vede**: che la pagina del giocatore e quella DM dicano la
  stessa cosa nella parte comune. Per la Corona e per gli stadi 0, 1 e 3
  dell'Anello le due pagine escono dallo stesso generatore; per le altre pagine,
  scritte a mano, la coerenza è affidata a chi le modifica.
- **Cosa resta fuori**: i file markdown e i PDF di lavoro delle cartelle. Sono
  fonti, e la matrice li cataloga come prima.
