# ADR-0109 — Una marcatura sola, e il DM decide cosa diventa canone

**Stato**: accettata (2026-11-07, Jfs sulle 8 schede; il punto 3 è adottato solo se la prova A/B non peggiora)
**Data**: 2026-11-07
**Canale (ADR-0099)**: stable dal 2026-11-25, scelta del DM sulla card del 2026-11-25 (*«Tutti e sei, con il codice»*, D8 di [PIANO-PIATTAFORMA-DI-SVILUPPO](../PIANO-PIATTAFORMA-DI-SVILUPPO.md)). Le marche sulle righe cambiate girano solo sulle PR: 3 rossi su 510 run dal 2026-11-07, tutti marche senza domanda e base, corrette; i run di PR valgono come i 10 run su `main`. Il passo perde `continue-on-error` ([misura](../esperimenti/promozioni-2026-11-25/MISURE.md)).
**Decisione-fonte**: il DM (Jfs), 2026-11-07: *«le parti inferred vengano marcate in modo tale che il dm possa decidere se farle diventare canone; per le regole di skill, agents ecc. vale la regola più stringente»*. Schede 1-8 nel thread «Standardizzare marcatura INFERRED e skill vincolate».
**Rapporti**: rende unica la marca di AGENTS.md §5; aggiorna il modello di [ADR-0091](ADR-0091-la-scheda-del-png-ha-una-forma.md) (`[ACCEPTED — DM-canon]` → `[CANONE — DM …]`); usa lo storico di [ADR-0069](ADR-0069-la-storia-delle-scelte-resta-nel-sorgente.md) e i cancelli di [ADR-0108](ADR-0108-i-cancelli-deterministici-stanno-in-ogni-skill.md); i canali sono quelli di [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md). Ricerca in [RICERCA-MARCATURE-INFERRED-2026-11](../RICERCA-MARCATURE-INFERRED-2026-11.md).

## Contesto

La marca INFERRED filtra davvero: sulla storia del repo, delle 171 righe
passate da INFERRED a CANONE il DM ne ha cambiate 30 (18%), 16 con un numero
diverso. Ma la forma era dispersa: quattro modi di scrivere INFERRED, cinque di
scrivere canone, la regola scritta in sei posti con parole diverse, e l'86%
delle marche senza la domanda da fare al DM. Il ratchet di
`inventory_inferred.py` gira non bloccante.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| Grammatica unica con domanda e base, regola in un file solo (scelta) | ogni marca è già una card; un controllo conosce una forma sola | migrazione una tantum delle forme vecchie fuori da `plans/` |
| Solo la domanda, senza base | meno da scrivere | il DM non vede su cosa poggia un numero |
| Lasciare le forme di oggi | nessuna migrazione | card da ricostruire a mano, sei testi che divergono |
| Aggiungere un grado di fiducia | sembra più informazione | la fiducia dichiarata dagli LLM non segue l'esattezza (arXiv 2507.06306, 2507.10587) |

## Decisione

**Ogni fatto di gioco porta una sola marca della grammatica di
[GUIDA-MARCATURE](../../docs/reference/GUIDA-MARCATURE.md), e solo il DM fa
passare un INFERRED a CANONE.**

1. **Grammatica** (scheda 1 = A, 8 = A): `[INFERRED — <domanda>; base: <…>]`,
   `[CANONE — DM <data>, <codice>]`, `[CANONE GIOCATO <data>]`, `[GENERATO]`
   con lo script nella riga, più le marche di fonte. Niente gradi di fiducia.
2. **Un posto solo** (scheda 3 = A): la grammatica sta nella guida; AGENTS.md,
   le skill e gli agent la richiamano. Un test fallisce se una skill la riscrive.
3. **Blocco vincoli** (scheda 5 = A) nelle 10 skill che scrivono contenuto di
   gioco: permesso di dire «non so», divieto di inventare statblocchi e poteri,
   ordine delle fonti, dati non istruzioni, rilettura di ogni numero prima di
   consegnare. Entra come standard solo se la prova A/B (scheda 7 = B: 30
   consegne × 2 versioni) non peggiora le invenzioni non marcate, le marche
   senza domanda e le marche con domanda e base.
4. **Migrazione** (scheda 2 = A): fuori da `plans/` le forme vecchie passano
   alla grammatica, con il conto prima e dopo. `plans/` resta storia.
5. **Righe di regola** (scheda 6 = A): skill, modelli, README, fixture e
   questa guida contano come «meta»; P16 arriva a 0 aperti.
6. **Cancelli** (scheda 4 = A): marca senza domanda nelle righe nuove, e
   INFERRED tolto senza CANONE, GENERATO o storico. Partono non bloccanti nel
   canale testing; dopo due settimane l'audit settimanale propone di renderli
   bloccanti, con i falsi positivi contati.

## Conseguenze

- Il DM decide da una riga sola: domanda e base sono già scritte.
- Chi marca scrive di più, ogni volta.
- Un commit grande e meccanico di migrazione, separato dal resto.
- I controlli riconoscono una forma sola e non devono indovinare.
- Per due settimane una marca senza domanda passa con un avviso.

**Da rivedere se**: la prova A/B mostra che il blocco vincoli peggiora una
delle tre misure; o se dopo un mese i cancelli bloccano più PR legittime che
marche sbagliate.
