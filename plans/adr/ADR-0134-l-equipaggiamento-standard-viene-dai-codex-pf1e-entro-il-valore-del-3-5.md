# ADR-0134 — L'equipaggiamento standard viene dai Codex PF1e, entro il valore del 3.5

**Stato**: accettata (2026-11-13)
**Data**: 2026-11-13
**Decisione-fonte**: il DM (Jfs), 2026-11-13, card «Codex PF1e, livello effettivo» nel thread del volume, dopo aver chiesto che l'equipaggiamento standard di mostri e PNG non si inventi ma si prenda «in modo deterministico» dalle tabelle dei manuali. I nove punti sono quelli della card.
**Rapporti**: è la prima regola ibrida registrata secondo la D-B-ter di [ADR-0126](ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md). Usa la verifica `ricchezza` del lotto 8 di ADR-0126 e la forma della scheda di [ADR-0091](ADR-0091-la-scheda-del-png-ha-una-forma.md).

## Contesto

Molte schede del Bestiario non scrivono l'equipaggiamento, o ne scrivono solo
la parte che serve ai conti. Il 3.5 aperto (SRD) dà il valore
dell'equipaggiamento di un PNG per livello (DMG, Tabella 4-23) ma non un
elenco di oggetti per classe e livello: le tabelle 4-12…4-22 del DMG non sono
nell'SRD e non si possono copiare. PF1e ha tutte e due le cose sotto OGL: la
Tabella 14-9 del Core Rulebook (valore per livello diviso in cinque
categorie) e i PNG già equipaggiati dell'NPC Codex e del Monster Codex.

## Decisione

1. **Chi ha l'equipaggiamento di un PNG lo dice l'SRD** («Improving
   Monsters»): solo le creature che avanzano per classe. Le altre tengono la
   riga «Tesoro».
2. **Prima fonte: i conti della scheda.** Ciò che attacchi, CA e tiri
   salvezza già mostrano si scrive così com'è.
3. **Poi il PNG dei Codex PF1e di pari classe e livello**, coi prezzi
   ricalcolati sul 3.5.
4. **Tetto: Tabella 4-23 del DMG 3.5 al livello effettivo** (dadi vita +
   modificatore di livello + livelli di classe). In una scheda PF1e il tetto è
   la Tabella 14-9.
5. **Sopra il tetto si toglie in ordine fisso**: uso limitato, attrezzatura,
   magia. Mai ciò che la scheda usa nei conti.
6. **Senza un PNG nei Codex**: budget nelle cinque categorie della 14-9, e
   gli oggetti li sceglie il DM su una card.
7. **Un oggetto che nel 3.5 non esiste** va su una card.
8. **Classi da PNG**: colonna unica della 4-23. La riduzione di p. 127 del
   DMG non è riscontrata su una fonte aperta.
9. **È una regola ibrida** (elenco PF1e, valore 3.5): sta nel registro
   `campaign/REGOLE-CUSTOM.md`, voce RC-001.

## Che cosa c'è nel repo

- `sistemi/pf1e/dati/codex.toml`: 454 PNG dei due Codex con classe, livello,
  grado di sfida ed elenco degli oggetti (solo nomi). Generato da
  `estrai_codex.py` dal PRD in cache, con `--check`.
- `sistemi/pf1e/dati/oggetti.toml`: la Tabella 14-9 (totale e cinque
  categorie), dalla sezione «Table: NPC Gear» del PRD.
- `estrai_codex.py --cerca CLASSE LIVELLO`: i PNG di quella classe e livello
  col prezzo 3.5 di ogni oggetto che `ricchezza` conosce e il tetto.
- `creature_base.toml` del 3.5: `avanza = "classe"` su 52 creature dell'SRD.
- `verifica_scheda.ricchezza`: prezzo base di armi, armature e scudi comuni e
  fattura perfetta; regola `equipaggiamento.da_png` per il punto 1; legge le
  voci «Equipaggiamento da combattimento» e «Altro equipaggiamento», dentro
  il recinto e nella riga delle Statistiche, e conta una volta sola
  l'equipaggiamento scritto in tutti e due i posti.

## Alternative scartate

- **Tabelle 4-12…4-22 del DMG 3.5**: sono la fonte più vicina, ma non sono
  contenuto aperto.
- **Solo il budget per categorie**: deterministico nel valore, non negli
  oggetti. Resta il ripiego del punto 6.
- **Prezzi PF1e**: più semplici da estrarre, ma le schede sono 3.5 e il
  tetto è del 3.5.

## Conseguenze

- Il riempimento delle schede è un lavoro a parte (thread del volume), una
  scheda alla volta, e parte dai dati di questa decisione.
- Il prezzo 3.5 si conosce solo per gli oggetti che `ricchezza` riconosce:
  per gli altri la ricerca stampa «?» e il totale è un minimo. Chi riempie
  deve guardare ogni «?».
- Una scheda PF1e non si giudica ancora contro la 14-9: mancano i prezzi
  degli oggetti PF1e.
- La quarta riga della 14-9 somma 1.750 mo nelle categorie contro un totale
  di 1.650: i dati tengono i numeri del manuale.
- Le schede che col prezzo base superano il tetto diventano card per il DM,
  non correzioni automatiche. Le prime sette (2026-11-14) il DM le ha tenute
  com'erano: portano la riga «Equipaggiamento sopra la tabella: scelta del
  DM» col valore, il tetto e il GS.
