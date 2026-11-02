# ADR-0094 — Il giro completo di un arco si misura contro la versione di prima, handout compresi

**Stato**: proposta (diventa accettata se il giro di DEF-4 e DEF-5 della serata del 2026-10-19 va bene, decide il DM)
**Data**: 2026-10-19
**Decisione-fonte**: richiesta del DM del 2026-10-19 («riscrittura dell'arc07 nello specifico def4 e def5 […] con un giro check di prosa playtester dm e developer e mappe, i png villain e tattiche aggiornate e misura del miglioramento e alla fine booklet aggiornati […] si misura anche con gli handout dei giocatori e se va bene diventa un processo standard»)

## Contesto

Il ciclo del master ([ADR-0075](ADR-0075-il-ciclo-del-master-vale-per-ogni-piano.md),
`rumblingstone-module-standard`, «Il ciclo completo») dice quando un master è
DEF: scene, contratto «In scena», componenti, domande del developer, box al
metro, le quattro letture a freddo, il ricordo del giorno dopo. Non dice come
si sa che **un secondo giro** su un master già DEF ha migliorato qualcosa, e
non guarda gli handout, che il giocatore tiene in mano più a lungo di qualunque
box.

[ADR-0093](ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md) ha
dato la risposta per i box: decide la misura (dettagli sensoriali, monologhi
interi), e il DM vota alla cieca solo dove la misura tace. Mancava lo
strumento che la applica a tutti i file di un giro in una volta, master e
handout insieme, contro la versione di partenza.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| Un comando che confronta ogni file del giro con la sua versione a un commit, handout compresi, e i passi 8-9 aggiunti al ciclo | una tabella sola, la stessa misura per master e handout, un file che peggiora esce 1 | gli handout sono pochi e corti: la misura su di loro dice poco finché non ne passano altri |
| `ciclo_prosa misura` file per file, come ora | c'è già | due file alla volta, e chi rifà il giro deve tenere a mano i prima |
| Misurare solo il booklet stampato | è quello che arriva al tavolo | il `.typ` e l'`.hb.md` sono generati: la prosa si corregge nelle fonti, e la misura va dove si corregge |

## Decisione

**Un giro su un arco già DEF si chiude con due passi dopo i sette del ciclo.**

8. **La misura contro la versione di prima.**
   `python3 scripts/ciclo_prosa.py confronta --rif <commit di partenza> <master> <handout> …`
   su tutti i file che il giro tocca, handout dei giocatori compresi. Nessun
   file peggiora (segnalazioni, MQM, box impoveriti, fatti cambiati); dove le
   misure non distinguono, il voto cieco di ADR-0093 sulle coppie indecise e
   sui controlli.
9. **I booklet rigenerati dalle fonti**, mai corretti a mano, con
   `validate_booklets.py` verde e l'ordine dei capitoli controllato contro
   l'ordine delle scene del master.

`misura_craft` conta gli handout dei tre archi come bersagli propri
(«Handout ARC-07», «Handout ARC-08», «Handout ARC-09»), così `--box` e
`--stile` li mettono accanto ai master.

## Conseguenze

- Il primo giro che usa i passi 8-9 è quello di DEF-4 e DEF-5 per la serata del
  2026-10-19. Se regge, i passi entrano nella tabella del ciclo in
  `rumblingstone-module-standard` e questo ADR diventa «accettata».
- Gli handout dentro `homebrew/` (per esempio `volume-mille-anni/03-…`) sono
  fonti del corredo: `confronta` li accetta per percorso, `misura_craft` no,
  perché la cartella `homebrew` resta esclusa dai bersagli.

- **Il primo giro (giro 4 di ARC-07, PR #254, 2026-10-19)** non ha trovato
  peggioramenti di prosa, e ha segnato ✗ anche i numeri e i nomi **aggiunti**
  per il DM. `confronta` adesso tiene a parte i fatti solo aggiunti («solo
  aggiunti», non peggiora) da quelli tolti o cambiati (✗). `ciclo_prosa misura`,
  il cancello del singolo file, resta severo.

**Da rivedere se**: il giro di stasera trova un difetto che nessuna delle misure
del passo 8 aveva visto, o se `confronta` blocca un giro per un cambio di fatti
voluto dal DM (in quel caso serve un modo di dichiararlo).
