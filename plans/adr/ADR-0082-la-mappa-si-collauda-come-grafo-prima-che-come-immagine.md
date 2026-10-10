# ADR-0082 — La mappa si collauda come grafo prima che come immagine

- **Stato**: **accettata** (il DM, il 2026-10-08: D1-D7 di [PIANO-COLLAUDO-E-GENERAZIONE-MAPPE](../PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md) come proposte); **non attuata**. Il punto 8, la regola di posa, è **proposto** (D8)
- **Data**: 2026-10-08
- **Decisori**: DM (Gianfranco Samuele), agente
- **Rapporti**: si appoggia ad [ADR-0048](ADR-0048-legenda-funzionale-fonte-unica.md) (la legenda funzionale è il solo dato che il collaudo legge); rispetta [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md) (solo libreria standard in ciò che il DM esegue), [ADR-0039](ADR-0039-profili-regole-multisistema.md) (i numeri di gioco stanno nei profili), [ADR-0012](ADR-0012-standard-ingegneria-tool-verificabile.md) (tool a contratto), [ADR-0005](ADR-0005-confini-ip-uso-non-commerciale.md) (niente mappe di terzi come dato) e [ADR-0056](ADR-0056-una-norma-senza-misura-non-esiste.md) (una norma arriva con la sua misura); prende in carico il linter di level design e il discriminante `map_kind` che [PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA](../PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md) assegnava a [PIANO-VENDIBILITA](../PIANO-VENDIBILITA.md), che non li elenca fra i suoi lotti

## Contesto

Il DM ha portato un documento di ricerca, *«Algorithmic Frameworks and Automated
Evaluation Architectures for Deterministic Map Generation in Tabletop
Role-Playing Games»*, e ha chiesto cosa se ne può applicare alla generazione e
alla correzione delle mappe del repo, per D&D 3.5 e Pathfinder 1e.

Il documento descrive una pipeline in sei stadi: parametri e seme, generazione
deterministica (BSP, Wave Function Collapse, simmetria locale alla Watabou,
automi cellulari), collaudo automatico (algoritmo genetico a due popolazioni
FI-2Pop e agenti di playtest), riparazione, archivio di diversità MAP-Elites,
arricchimento ed export VTT. È scritto per 5e e Pathfinder 2e: i valori di
copertura che cita (+2 e +5 CA) sono quelli di 5e, non dell'SRD 3.5.

Il repo ha già quattro di quei sei stadi. Un LLM non disegna mai la griglia
(`tre-modalita-mappe.md`), il rendering è deterministico e la CI lo verifica al
byte, il contratto JSON viene validato prima di compilare, l'export UVTT porta
muri, porte e luci (100 px per quadretto di default, `--ppg` per i 70 che il
documento indica come convenzione). Manca il collaudo: misurato il
2026-10-08 su 38 griglie in 18 file (`plans/esperimenti/collaudo-mappe-2026-10/`),
**nessuno script verifica che una mappa si possa giocare**. `validate_maps.py`
controlla che l'SVG corrisponda al master; `compile_map_json.py` che le
coordinate stiano nella griglia. Nessuno chiede se dall'ingresso si arriva al
nemico, se una porta sta in un muro, se un ogre passa per il corridoio.

La misura ha trovato difetti che un collaudo avrebbe preso:

- in due mappe giocate dell'arco 07 (la Stanza della Corona e il Cuore della
  Montagna, in tre sorgenti) il pavimento è disegnato con `⬛`, che la
  legenda definisce muratura piena. La legenda locale lo ridefinisce
  «pavimento», cosa che `audit-mappe-workflow.md` STEP 4 già vieta. Letto dalla
  legenda, il Cuore della Montagna è fatto di 13 sacche separate con le unità
  sparse in 17 di esse; l'audit di luglio la portava come la mappa riuscita del
  corpus (M1 = 1,00), e quel voto veniva dallo stesso errore;
- delle 97 celle-porta, 20 non hanno un muro accanto: 13 stanno in una vista
  d'insieme della fortezza di Hammerfist e 7 nelle mappe del Drappo, dove `🚪`
  vuol dire «il portone» a una scala in cui il muro non si disegna. Un
  controllo sulle porte che non sa *che tipo di mappa è* segnala anche quelle.

La seconda osservazione è la stessa che l'audit di luglio faceva per le
metriche di level design (§3.4): il discriminante va aggiunto **prima** dello
strumento. La misura stessa, al primo giro, ha contato come mappe di campagna
le fixture dei test, rotte apposta; anche lo strumento deve dichiarare il suo
corpus.

## Decisione

1. **Il collaudo legge un grafo, non un'immagine.** La griglia diventa un grafo
   di celle percorribili secondo i campi `blocks_movement`, `blocks_sight` e
   `cover` di `scripts/legend.json`, e nessun'altra fonte. Uno script che
   dichiara un proprio insieme di simboli viola ADR-0048 e il gate
   `legend/single-source` lo boccia già.

2. **Le regole di movimento e di copertura sono quelle dell'SRD**, uguali in 3.5
   e PF1e: diagonale 5-10-5; niente diagonale oltre l'angolo di un muro, sì
   oltre una fossa o una creatura; una creatura Grande occupa 2×2 e un'Enorme
   3×3; strizzarsi in uno spazio largo almeno metà del proprio costa doppio e
   dà −4 a colpire e alla CA; la copertura si calcola da un angolo del proprio
   quadretto verso gli angoli del bersaglio. Sono **geometria**, non numeri di
   gioco: il collaudo dice *se* c'è copertura, il profilo di ADR-0039 dice
   *quanto vale*. Finché il lotto 1.2 di VENDIBILITA non porta i profili, il
   profilo geometrico «d20» vive nello strumento, dichiarato, e si sposta lì
   quando arriva.

3. **Due classi di rilievo, decise una volta.**
   - **E · errore**: un fatto che non dipende dal gusto. Simbolo né universale
     né dichiarato; legenda locale che dà a un simbolo universale la funzione
     opposta (blocca contro percorribile); porta in una mappa tattica senza
     muro né bordo su due lati opposti; obiettivo, ingresso o unità
     irraggiungibili senza una deroga scritta. Entrano in CI **a tetto**: un
     file `scripts/collaudo-mappe-tetti.json` fissa i conteggi di oggi e il
     gate fallisce solo se crescono. Si scende a zero un lotto alla volta.
   - **A · avviso**: un'opinione informata. M1, M2, M4, M7, M8, M9 dell'audit,
     anelli e strozzature, accesso per le creature grandi. **Non bloccano mai**
     e dichiarano nel messaggio di essere soglie euristiche finché non sono
     calibrate, come stabilito in LEVEL-DESIGN §1. Una mappa può violarle
     tutte di proposito.

4. **La mappa dichiara cosa è e dove deroga, dentro la griglia.** Due direttive
   nuove, della stessa famiglia di `@north` e `@zone`, che il renderer ignora:
   `@tipo tattica|strategica|schema` e `@deroga <codice> ; <motivo>`. Una vista
   strategica non riceve i controlli tattici. Una deroga senza motivo vale come
   assente, come le deroghe di `legend.yaml`.

5. **Solo libreria standard.** Connettività, componenti, M1, M2 e accesso 2×2
   girano sull'intero corpus in 1,3 secondi con la sola libreria standard. La
   linea di vista per M4 si fa con lo shadowcasting simmetrico, che in Python
   puro sta in un centinaio di righe. ADR-0015 della PR #72 proponeva `scipy`,
   `networkx` e `tcod` per guadagnare velocità; con questi tempi il guadagno non
   paga la dipendenza.
   *(Emendato il 2026-10-08 da [ADR-0084](ADR-0084-il-collaudo-delle-mappe-e-uno-strumento-di-sviluppo.md):
   la frase sullo shadowcasting era una stima. Misurato, in Python puro M4 su
   tutto il corpus costa 70 s, con `tcod` 0,6 s; il DM ha fatto entrare `tcod`
   nel collaudo, obbligatoria. `scipy` e `networkx` restano fuori.)*

6. **Il collaudo non tocca il canone.** Su una mappa già giocata il collaudo
   segnala e basta; la correzione è una decisione del DM e cambia simboli, mai
   posizioni (`audit-mappe-workflow.md` STEP 2). La riparazione automatica
   esiste solo per le bozze del generatore e per le mappe in contratto JSON non
   ancora giocate, e produce una proposta da approvare, mai una scrittura.

7. **Il generatore, se si fa, produce contratti JSON, e una bozza che non passa
   il collaudo non esce.** BSP per gli interni, automi cellulari per le caverne,
   seme dichiarato, solo libreria standard, per i luoghi nuovi e gli incontri
   casuali. L'unica idea di FI-2Pop che entra è la **distanza dalla
   giocabilità** come somma pesata dei rilievi E: il generatore scarta o
   ritenta finché è zero.

8. **Proposto (D8): ogni simbolo dichiara come si posa.** La legenda dice cosa
   fa una tessera e non dove può stare; una porta in mezzo a un prato ha la
   stessa funzione di una porta in un muro. Un campo neutro `posa` in
   `legend.yaml` (`nel_muro`, `recinto`, `fra_livelli`, `sul_pavimento`,
   `solo_master`) rende la posa un dato che il collaudo verifica, come la
   funzione. Le scale e le botole portano la loro coppia su un'altra mappa o un
   altro livello (`@collega`), e il collaudo controlla che esista. Entra con il
   corredo di simboli che oggi manca (misurato: una porta, una scala, nessuna
   grata, gabbia, saracinesca, botola o porta segreta). I numeri di porte e
   saracinesche (durezza, punti ferita, CD) stanno nel profilo, non qui.

## Alternative scartate

| Alternativa | Perché no |
|---|---|
| Algoritmo genetico FI-2Pop completo, con due popolazioni che evolvono | il corpus è di 38 mappe scritte a mano, quasi tutte giocate. Non c'è una popolazione da far evolvere, e una mutazione casuale su una mappa giocata sposterebbe il canone |
| Archivio MAP-Elites per la diversità | risolve la monotonia di un generatore che sforna migliaia di mappe a un pubblico. Qui c'è un DM e una campagna; il problema misurato è l'opposto, mappe di campo aperto tutte uguali (M2 mediana 0,52), e si corregge progettandole (LEVEL-DESIGN C2). Si riapre solo se il generatore del punto 7 entra in uso e produce bozze che il DM giudica ripetitive |
| Wave Function Collapse | serve un set di tessere con regole d'adiacenza che il repo non ha, e porta il problema delle contraddizioni da disfare. BSP e automi cellulari coprono i due casi d'uso con un decimo del codice |
| Agenti di reinforcement learning o Monte Carlo Tree Search come playtester | una ricerca in ampiezza su un grafo di poche migliaia di celle risponde alle stesse domande («ci si arriva?», «ci passa un Grande?») in modo esatto e ripetibile |
| Un LLM che genera o corregge la geometria | vietato da `tre-modalita-mappe.md` per una ragione misurata: l'arte ASCII scritta token per token slitta di un quadretto in poche righe. L'LLM scrive il contratto JSON o i parametri del generatore; il collaudo lo giudica |
| Arricchimento con statblocchi generati da IA (come fanno CharGen e simili) | AGENTS.md vieta di inventare statistiche. Le unità della mappa puntano al Bestiario |
| Lasciare il linter in VENDIBILITA | VENDIBILITA §6 non lo elenca e nessun piano lo esegue. Due piani che si rimandano lo stesso lavoro lo lasciano senza proprietario, ed è successo |
| Bloccare in CI anche le metriche di level design | un ponte stretto sopra il vuoto viola M1, M2 e M4 per scelta. Un gate che boccia una buona mappa viene spento, e con lui i controlli che servivano |

## Le conseguenze

**Cosa si ottiene.** Una domanda a cui oggi nessuno risponde, «questa mappa si
gioca?», ha una risposta ripetibile in CI. Il lotto mappe D28 di
LETTORE-E-PLAYTESTER produce le prime griglie nuove dopo molte settimane e sono
i primi clienti naturali. Le metriche dell'audit di luglio, che ha calcolato a
mano e con un insieme di coperture inventato per l'occasione, diventano uno
strumento che legge la legenda ratificata. Il generatore, se il DM lo vuole,
nasce con il collaudo già attaccato.

**Quello che si paga.**

- Due direttive nuove nel formato delle griglie, da registrare come norme
  ([`REGISTRO-NORME-EDITORIALI`](../../skills/REGISTRO-NORME-EDITORIALI.md), G3)
  e da applicare alle 38 griglie esistenti.
- Le due mappe con `⬛` usato come pavimento vanno ridisegnate nel simbolo, con
  la rigenerazione dei loro SVG: l'unico punto in cui il piano cambia artefatti
  committati, e su mappe giocate. Lo decide il DM (D2).
- Il profilo geometrico «d20» vive per un po' dentro lo strumento invece che in
  un profilo di ADR-0039. È un debito dichiarato con una data di scadenza: il
  lotto 1.2 di VENDIBILITA.
- Il collaudo legge la griglia tramite il parser di `render_map_svg.py`, come
  già fa `validate_maps.py`. La dipendenza va nella direzione sbagliata (il
  dominio dalla presentazione) finché il lotto 1.3 di VENDIBILITA non la
  separa; il collaudo non la peggiora e non la risolve.
- Le soglie di M1-M9 restano euristiche. Il corpus su cui calibrarle deve
  essere materiale proprio o con licenza libera (ADR-0005), e oggi non c'è.

**Cosa resta fuori.** Il collaudo misura le affordance, non il divertimento.
Non giudica le scene sociali né l'esplorazione. Non sostituisce la verifica a
vista del PNG (STEP 5 di `audit-mappe-workflow.md`) né la prova al tavolo.
