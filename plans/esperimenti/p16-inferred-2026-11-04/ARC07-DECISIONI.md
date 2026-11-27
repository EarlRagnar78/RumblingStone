# P16 · lotto 2: le marcature aperte di ARC-07

Origine: P16 dell'indice §0 di `plans/STATO-E-ORDINE-DEI-PIANI.md`, dopo il lotto
1 (ARC-08, `ARC08-DECISIONI.md`). Regola del DM del 2026-11-04: si chiude solo
ciò che è già fatto, risolto o superato, con la prova; il resto va a card di
decisione vere, per tema, ognuna con la consigliata.

## 1. Il conto

`inventory_inferred.py` su main dopo la PR #311: **70 aperte in ARC-07**. Sono
**24 voci**: il resto sono copie delle stesse righe nei quattro volumi `.hb.md`
(NOTTE-E-ALBA, SERATA-RESURREZIONE, MILLE-ANNI-VOLUME, SESSIONE-TERROS), che
cambiano insieme al master.

## 2. Chiuse perché già risolte (card «R»)

| # | Dove | Cosa | Prova |
|---|---|---|---|
| R1 | DEF-4 Scena 5 (r. 1917) | Hella in forma d'aquila fa scattare i glifi «dei nani» | SRD: la forma selvatica «funziona come la forma alternativa», che «conserva tipo e sottotipo» (d20srd, *Druid*; *Special Abilities*, Alternate Form); *glifo di interdizione*: polymorph e simili non ingannano il glifo |
| R2 | DEF-4 Scena 10 (r. 3093) | Chi cade dal muro sud prende 8d6 | 24,5 m = gradone 20 m (DM 2026-10-22) + mura 4,5 m (M7-B); SRD: 1d6 ogni 3 m (10 ft) → 80 ft = 8d6 |
| R3 | MAPPE «La torre nord» (r. 648) | Torre nord sul gradone di +120 con la porta nella montagna | Quote del DM del 2026-10-22, commit 8959571 (#267): «torre nord +120 m»; memoria `quota-hammerfist` («a +120 m, la torre nord con la porta alla montagna») |
| R4 | Portale-Forgia-L1 (r. 31) | PF-1 è una generazione storica, al tavolo vale S-2 | `ARC07-MAPPE-DEFINITIVO.md` r. 45: S-2 = «geometria canonica ARC-06» (`06_…/Tactics_and_maps.md`) |

## 3. Aperte: card per tema

### Card 1 · Le mura del 372 e la discesa
- **La rampa della porta** (DEF-4 r. 429 e r. 3016, MAPPE r. 639 e legenda r. 610/4561): rampa di terra e pietra di circa 150 m sotto il muro sud, dalla spianata (+80) alla porta (+100). Il DM ha dato le quote, la rampa no (commit 8959571: «la rampa resta INFERRED»).
- **Le scale sul tratto est e Hrodgar lì** (DEF-4 r. 3016).
- **La discesa dal bosco** (DEF-4 r. 508): il portale li lascia sulla spalla est poco sopra le mura, e il bosco scende di 100 m fino alla piana; autunno, 5 °C.
- Consigliata: **tenerle come scritte**. Le quote del DM le richiedono: senza rampa gli arieti non arrivano alla porta, e il fronte sud sta sul ciglio a 24,5 m.

### Card 2 · La notte nella tenda di Zog'tar
- **Il palo centrale** (DEF-4 r. 2522): Zog'tar lo abbatte (Forza CD 20) e il telo crolla su chi vola dentro.
- **Le 20 cariche** (DEF-4 r. 883 e r. 2627): chi spende più di 20 cariche di bacchetta prima di ripartire segna una tacca. Il CHANGELOG del 2026-10-19 la lascia aperta.
- **Vatore sa chi è stato** (DEF-4 r. 2915) quando il fagotto si strappa di mano.
- **La portata del sussurro** (DEF-4 r. 1987): dal corno Skullcrusher sente chi parla sottovoce fuori dal telo, da dentro solo i gridi.
- Consigliata: **tenerle come scritte** (la versione più dura per i PG, coerente con le simulazioni del giro 4).

### Card 3 · Skullcrusher
- **Il nome gridato vale da fuoco** di *colpo accurato* (DEF-4 r. 3336): fuori dall'SRD, che vuole un bersaglio di legno.
- **Soffio Aderente** (DEF-4 r. 4012): il testo viene da una trascrizione secondaria del Draconomicon; il master non dà un modo per toglierselo, e l'acido torna solo una volta (metà danni al round dopo).
- **Il 14° livello** (DEF-4 r. 3825): se arriva prima di `DEF-5` dipende dai PX con cui il gruppo è partito, che il ledger non ha.
- Consigliata: nome = fuoco **sì** (la versione più terrificante), Soffio Aderente **com'è scritto** (l'acido torna una volta e basta, senza prova per toglierselo), PX: **il DM dice il totale del gruppo**, e la riga si corregge.

### Card 4 · Poteri, portali e luoghi sotto la montagna
- **Benedizione di Moradin Incarnato** (DEF-3 r. 1212): 1 al giorno, azione veloce, 1 minuto (proposta del giro 2, G2-06, «numeri del correttore»).
- **Il portale di Dana** (DEF-5 r. 810): quanto resta aperto. Proposta: 1 minuto (10 round), poi si chiude.
- **La runa di Zeth su Durik la mette Hella** (DEF-4 r. 1117): *resistere all'energia* è a contatto.
- **Il Cuore a −150 m** sotto il cortile (DEF-5 r. 1137, MAPPE r. 836).
- **La galleria dei fonditori** dietro la porta segreta (Cercare CD 20) nell'arena del Topazio (Portale-Forgia-L2 r. 339 e r. 587).
- **Il pilastro di Terros** (DEF-1 r. 691): crolla su una striscia larga 3 m e lunga 30 m dalla base G08 (la volta è a 50 m).
- Consigliata: **tenerle come scritte**, con il portale a 1 minuto.

## 4. Come si applicano

Ogni risposta diventa `[CANONE — DM 2026-11-04, P16, <tema>]` nel master e nei
quattro volumi `.hb.md`, poi `inventory_inferred.py --update-baseline` e
`memoria.py`.

**Da rivedere se** il DM cambia le quote del 372 o la scheda di Skullcrusher.

## 5. Risposte del DM (2026-11-04)

- Card R (chiuse perché risolte): sì, R1-R4 chiuse.
- Card 1 (mura del 372): come scritte.
- Card 2 (tenda di Zog'tar): come scritte.
- Card 3 (Skullcrusher): il nome gridato vale da fuoco; Soffio Aderente com'è (l'acido torna una volta, senza prova per toglierselo).
- Card 4 (poteri e luoghi): come scritte, portale di Dana aperto 1 minuto (10 round); Incarnato 1 al giorno, azione veloce, 1 minuto.
- Resta aperta solo la riga del 14° livello (DEF-4 r. 3825): serve il totale dei PX di partenza del gruppo.
