# ADR-0118 — Un numero entra solo se la regola lo calcola

**Stato**: accettata (2026-11-09)
**Data**: 2026-11-09
**Canale (ADR-0099)**: stable dal 2026-11-25, scelta del DM sulla card del 2026-11-25 (*«Tutti e sei, con il codice»*, D8 di [PIANO-PIATTAFORMA-DI-SVILUPPO](../PIANO-PIATTAFORMA-DI-SVILUPPO.md)). 146 run su `main` senza rossi; 3 rossi su 384 run di PR, 2 veri e 1 falso allarme del lettore (il +1 dell'arma letto come bonus d'attacco), spiegato ma non corretto nel lettore. Il passo perde `continue-on-error` ([misura](../esperimenti/promozioni-2026-11-25/MISURE.md)).
**Decisione-fonte**: il DM (Jfs), 2026-11-09, thread «Scelte dell'8/11». Dopo che una ★ aveva portato nel canone l'AU +10 della Fanteria Hobgoblin, preso da una chat e non da una scheda: *«i valori sempre i più forti ma calcolati e non inventati; nel caso, se la versione PF1e è più forte usa PF1e, ma non inventare: deve essere compliant con le regole, altrimenti a cosa servono?»*. Poi: *«questa regola deve essere dentro un ADR per essere rispettata da tutti i thread, o ogni proposta di calcolo deve essere vincolata a questo controllo»*. Sulla card ha scelto «ADR più cancello in CI». E sulla copertura: *«vale per tutti gli stat block e le regole usate nel repo, nei booklet e negli stand alone? […] deve coprire tutto»*.
**Rapporti**: precisa [ADR-0091](ADR-0091-la-scheda-del-png-ha-una-forma.md) §4-bis (la versione più forte, costruita con un mezzo legale) e la estende a ogni numero di combattimento del repo. Usa i conti di `conformita_statblocchi.py` ([ADR-0064](ADR-0064-gli-attributi-si-scrivono-nel-bestiario.md), [ADR-0066](ADR-0066-le-creature-hanno-una-libreria-e-il-verificatore-non-importa-la-scelta.md)) e i dati dei sistemi di [ADR-0112](ADR-0112-il-motore-e-agnostico-e-le-regole-d20-sono-dati-e-formule.md). Le marche sono quelle di [ADR-0109](ADR-0109-una-marcatura-sola-e-il-dm-decide-il-canone.md).

## Contesto

La regola «la versione più forte» era scritta in ADR-0091 §4-bis e nel blocco «Vincoli sui fatti» di dieci skill. Non l'ha fatta rispettare nessun controllo, e il 2026-11-09 una ★ ha portato nel canone un AU +10 che nessuna scheda 3.5 o PF1e produce: l'ha fermato il DM, non la CI.

Misura dello stesso giorno, su `main`:

| Dove | Conti prima di questo ADR |
|---|---|
| Bestiario (119 schede) | pf, TS, BAB, lotta, attacco, iniziativa; l'attacco con una tolleranza da −1 a +2; in CI blocca solo `pf-dado` |
| Master in forma `**Campo:**` (ARC-08) | pf, CA, iniziativa, lotta; **non l'attacco**; solo rapporto. Un morso +37 finto di Fauci passava con «0 conti che non tornano» |
| Recinti ```statblocco``` dei master e degli stand alone | pf, CA, CD, scurovisione; non l'attacco |
| Unità di massa (AU) | nessun conto |
| Altri file con numeri di combattimento | nessuno legge i loro statblocchi: 75 file, soprattutto ARC-09, ARC-07 e PG |

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **ADR più cancello a cricchetto dentro `conformita_statblocchi.py`** (scelta del DM) | un numero nuovo che la regola non ricostruisce fa fallire la CI; si allarga lo strumento che il repo ha già | le discrepanze di oggi restano finché il DM non le decide; la copertura dei file in prosa si fa a lotti |
| Solo ADR | nessun codice | il +10 è passato con la regola già scritta: un agente la può saltare |
| Solo cancello, richiamando ADR-0091 | meno documenti | ADR-0091 parla delle schede dei PNG, non di unità, moduli e stand alone |
| Uno script nuovo | nessuna dipendenza dal vecchio | duplica il lettore delle creature (ADR-0066 lo vieta) |

## Decisione

1. **La regola.** Un numero di combattimento (pf, CA, TS, BAB, lotta o BMC, attacco, iniziativa, CD, AU) entra in una scheda del repo, in un booklet o in uno stand alone solo se la regola del suo sistema lo ricostruisce dalla scheda: 3.5 per il canone, PF1e per i moduli PF1e. Fra le versioni che si ricostruiscono vince la più forte (ADR-0091 §4-bis). Un numero che viene da una fonte esterna (una chat, un PDF, un modulo vecchio) e non si ricostruisce non entra, anche se è più alto. Un bonus che la regola non vede (oggetto, incantesimo, regola della casa) la scheda lo scrive accanto, con la marca di ADR-0109.
2. **I conti.** `conformita_statblocchi.py` fa tutti i conti che sa fare, **esatti**:
   - Bestiario: ogni scarto di `giudica`, più l'attacco esatto;
   - master in forma `**Campo:**`: anche l'attacco;
   - recinti ```statblocco```: anche l'attacco;
   - unità di massa: **AU = attacco della creatura singola** (`ARC08-02` §4: «AU e DU sono i valori medi di attacco e CA dell'unità»). L'unità rimanda alla sua scheda con una riga `Uno contro uno: \`Bestiario/…\``, oppure al blocco «STATISTICHE CREATURA SINGOLA» di una guida con `Uno contro uno: \`file.md\` § «TITOLO»`. Quel blocco scrive «Attacco Base» e le caratteristiche, e il suo attacco si rifà come gli altri. *(Corretto il 2026-11-09: la prima stesura diceva «+ 2», vedi in fondo.)*

   L'attacco è BAB + For in mischia (Des a distanza o con Arma Accurata) + taglia + potenziamento dell'arma (+1 se perfetta) + Arma Focalizzata (+1) + Arma Focalizzata Superiore (+1). Arma Focalizzata vale per l'arma che nomina; «in Ira» accanto all'attacco usa la Forza che la scheda dichiara in Ira; l'addestramento nelle armi del guerriero PF1e vale solo se la scheda lo scrive (aggiunte del 2026-11-09, con la prima correzione degli scarti). La formula è la stessa in 3.5 e PF1e: il conto `attacco` sta in `sistemi/*/dati/conformita.toml`.
3. **Il cancello.** `python3 scripts/conformita_statblocchi.py --cancello-numeri` è un cricchetto. `docs/audit/numeri-baseline.json` tiene gli scarti di oggi e i file che nessun conto legge ancora:
   - uno scarto nuovo, o un file nuovo con numeri che nessuno legge, fa fallire;
   - uno risolto si toglie con `--aggiorna-numeri`, che non aggiunge niente.

   In CI parte **non bloccante** (`continue-on-error`) e diventa bloccante dal 2026-11-23, come i cancelli di ADR-0109 e ADR-0114. Bloccante dal 2026-11-25, con la scelta del DM D8 di PIANO-PIATTAFORMA-DI-SVILUPPO.
4. **La copertura.** «Tutto» si misura con `non_coperti` della baseline e scende a lotti, un thread alla volta coordinato dal thread padre. Un lotto insegna allo script una forma nuova (la riga «A.5 · … · **morso** +34» delle appendici DEF, le tabelle di ARC-09, le schede dei PG), oppure porta la scheda nella forma di ADR-0091. Le regole PF1e che il cancello oggi salta (BMC e DMC al posto della lotta, scurovisione, *corrompere l'acqua*) le scrive nel plugin PF1e il thread «Completare le regole PF1e per il cancello».

## Misura

Il 2026-11-09, sul repo:
- **38 scarti in baseline**: 15 AU di unità (13 senza scheda uno contro uno, 1 Orog a +12 contro +15, la «Supporto Tecnico» di ARC08-03); Gorthak e Madre Dana (+1, nelle due copie di ARC-08); Zog'tar (+3, in ARC07-DEF-4 e nel booklet); 9 schede del Bestiario (8 da +1 a +2, duergar −3) che la tolleranza nascondeva; 7 statblocchi degli stand alone PF1e; 2 pf dell'Abbazia; la scurovisione di Skullcrusher nel booklet.
- **75 file non coperti**.
- La prova: con Fauci a +37 e gli Orog a +16 il cancello fallisce e dice il conto (`test_il_numero_gonfiato_non_torna`, `test_l_au_e_l_attacco_della_scheda_piu_due`). Con +33 e +15 passa.

## Conseguenze

- Una ★ «più forte» si propone solo col conto scritto accanto, e il cancello lo rifà.
- I 38 scarti diventano decisioni del DM. Ciascuno si corregge col conto, oppure con un mezzo legale che porta il numero dove serve (ADR-0091 §4-bis.2). Il «+1 da spiegare» è la parte più grande.
- `--master` resta un rapporto e ora conta anche l'attacco. Il test `test_il_cricchetto_dei_master` ha il tetto di Gorthak e Dana.
- **Quello che non è misurato**: gli attacchi secondari (artigli, ali, coda con Multiattacco), le iterazioni (+22/+17), i danni, le CA delle unità (DU). Le capacità che alzano l'attacco senza un talento elencato (Ira, *favore divino*, Odio della stirpe) la scheda le deve scrivere, altrimenti il conto le segna.

## Da rivedere se

- Il cancello blocca un numero giusto per una regola che lo script non conosce: si aggiunge la regola con la sua prova, non si allarga la tolleranza.
- I lotti di copertura non scendono per un mese: il DM decide se portare quei file nella forma di ADR-0091 o se archiviarli.

## Aggiornamento 2026-11-09: la prima correzione degli scarti

Il DM: «Ovviamente correggi i problemi che ci sono». Da 37 scarti a 13.

- **Lacune del verificatore (6 scarti erano falsi):** il potenziamento in mezzo al nome («grande ascia +1 a due mani», «martello +1 gelido»), l'attacco «in Ira» di Zog'tar, l'addestramento nelle armi PF1e dello skum, Arma Focalizzata contata su un'arma che non è la sua (Karkator), «Sensi come A.1» in un booklet che include la scheda a pezzi.
- **Numeri corretti col conto:** megera verde 49 pf e annis 52 pf (Abbazia); dovil runecaster +6; gnoll in sella +3, +5 solo in carica; monaco, raffica +7/+7; coltello del bravaccio +3 e spada corta del miliziano +4 (Drappo PF1e); sgherro di Hamid +12/+7; asservito PF1e danno 1d6+4.
- **Numeri tenuti con un mezzo legale scritto in scheda** (ADR-0091 §4-bis.2): Gorthak, Arma Focalizzata nel sesto talento libero; Madre Dana, Arma Focalizzata dal dominio della Guerra; duergar, Competenza nelle Armi Esotiche al posto di Schivare (+6); monaco, Arma Focalizzata (catena chiodata) al posto di Schivare (+10); drow, stocco perfetto; Uomo di Sal, sgherro, asservito, bravaccio e miliziano, i talenti del guerriero che il danno già implicava; Ghaurush, «perfetto» anche nel recinto.
- **Restavano 13 scarti**, tutti AU di unità di Hammerfist senza scheda uno contro uno leggibile (chiusi qui sotto). Le altre chiedono una scheda nel Bestiario e, dove il conto abbassa l'AU, una scelta del DM sull'equilibrio della battaglia.

## Correzione 2026-11-09: l'AU non ha il «+2»

**L'errore.** La prima stesura di questo ADR, e la PR #360 prima di lui, prendevano la regola delle unità dalla riga «Bonus Attacco: Media +2 (effetto massa)» di `mass_combat_guide_Dm.md`. Quella riga sta nella sezione della **variante 2d6**. Il sistema canonico a d20 (`ARC08-02` §4, quello che ARC-09 eredita) dice che AU e DU sono i valori medi di attacco e CA, senza +2, e la guida stessa dice di non mischiare i due motori. In `ARC08-01` undici unità su tredici avevano già l'AU uguale all'attacco della creatura singola.

**La scelta del DM** (card del 2026-11-09): «AU = attacco della creatura».

**Che cosa cambia.**

| Unità | AU prima | AU dopo | Perché |
|---|---|---|---|
| Fanteria Hobgoblin | +8 | **+6** | spada lunga perfetta del regolare (Bestiario, combattente 3); il +8 della #360 era «6 + 2» |
| Orog Guardie Nere | +15 | **+13** | ascia +13 della scheda; era +12, la #360 l'aveva portato a +15 col «+2» |
| Fanteria Orchesca | +6 | **+5** | barbaro 1, For 17, Arma Focalizzata; furia e carica da +8 a +7 |
| Giganti delle Colline, randello | +14 | **+16** | BAB +9 con 12 DV (era +8), For 27, Grande |
| Giganti delle Colline, massi | +14 | **+8** | il masso dell'SRD: BAB +9, Des −1, taglia −1, +1 razziale. Il +14 di `ARC08-02` era il randello |
| Ettin | +11 | **+12** | For 23 dell'SRD (il blocco dava 19) |
| War Adepts, raggio rovente | +7 | **+5** | contatto a distanza: BAB +3, Des +2 |

Le altre otto (guerrieri hobgoblin, worg riders, Doom Hand, sciamani, veterani, balestrieri, élite, ingegneri) restano come sono: il loro blocco ora scrive «Attacco Base» e le caratteristiche, e il conto torna.

**Che cosa non cambia.** Il libretto della battaglia (`ARC08-18`), le DEF e `ARC08-19` usano numeri loro, col morale dentro e tarati con le simulazioni: non si toccano. Due di quei numeri citano però `ARC08-02`: la carta dei massi dei giganti (AU 14) e le baliste (AU +10). La carta resta a 14 finché il DM non decide; `ARC08-19` §8 lo dice.

**Le baliste** (chiusura del 2026-11-09, richiesta del DM «cerca un valore plausibile»). L'SRD 3.5 dice che una creatura Media che punta una balista ha −4. Un Ingegnere da Guerra (Esperto 4) arriva a +3 anche con Arma Focalizzata e la balista perfetta. Il +10 scritto, che è anche il «d20 + 10» del libretto, torna con un mastro artigliere Guerriero 8 a ogni pezzo: BAB +8, Des +3, due talenti di focalizzazione +2, perfetta +1, −4 (`Bestiario/mostri/nano-mastro-artigliere-guerriero8-cr8.md`). Gli ingegneri caricano. Il cancello conosce il −4 della balista. Il «+18, 3d8+10» di `Mappe` L2 non si ricostruiva ed è sceso a +10.

**I GS dei blocchi «creatura singola»** seguono i livelli di classe (SRD: un PNG con livelli di classe ha GS pari al livello): Doom Hand da 6 a 8 (scelta del DM, card del 2026-11-09: Chierico 8 al posto di Chierico 7/Warpriest 1, numeri invariati; cade la «Furia 1/giorno», che un Chierico 8 non ha), War Adepts (Stregone 6) da 5 a 6, Sciamani (Chierico 5) da 6 a 5, Veterani nanici (Guerriero 5) da 4 a 5, orchi (Barbaro 1) da 1/2 a 1. Il cancello non rifà ancora questo conto.

**La carta dei massi nel libretto.** La carta dei giganti di `ARC08-18` tirava d20 + 14: era l'AU col randello che `ARC08-02` dava per sbaglio ai massi. Il masso dell'SRD è +8, col morale dei giganti +9. Otto giganti su quattro settori fanno **due macigni per settore a d20 + 9**: la simulazione `tre_giorni.py` dà la stessa battaglia della carta vecchia (orda feroce, nessuna breccia 50% → 54%, posizioni tenute 74% → 73%), mentre un macigno solo a +9 la rendeva più facile (61%). Scelta del DM con la card del 2026-11-10: «Due macigni per settore a d20 + 9».

**Scarti rimasti: 0.**

