# Il duello con Skullcrusher: simulazione Monte Carlo (15/11/2026)

Domanda del DM: la tattica di Skullcrusher regge contro le tattiche dei PG,
dalla più probabile alla meno probabile, tenendo conto di cosa sa e del suo
carattere? Script: `simula_duello.py`, esiti completi in `ESITI.md` (20.000
prove per riga, seme 1372).

## Che cosa è dato e che cosa è stimato

- **Drago e wyvern**: le schede di DEF-4, Appendici A.1-bis e A.6, senza un
  numero inventato. Il soffio, il nome con *colpo accurato*, Fluttuare alla
  prima paura, la fuga a ⅓ dei pf, le corde e la Catena a CA 44 vengono tutti dal
  master.
- **PG**: CA, pf, tiri salvezza e COS dalla carta del DM del 05/11
  (`plans/esperimenti/p16-inferred-2026-11-04/SCHEDE-PG-CARTA.md`).
- **STIMA**: i bonus d'attacco di Thorik (+22) e Tordek (+23 in ira), che sulla
  carta non ci sono, e le cure preparate da Hella. Con +4 (`--buff 4`) gli esiti
  cambiano poco, tranne la Catena (riga T4).
- **Fuori dal modello**: Durik, gli evocati di Hella, le pozioni, gli effetti
  degli artefatti oltre la Dragondoom, *neutralizzare veleno*, la ritirata dal
  cortile. Sono tutte cose che aiutano i PG, quindi le morti qui sono un tetto e
  non una previsione.

## Le tattiche dei PG, dalla più probabile alla meno probabile

1. **T1, la classica.** Nel cortile Artemis vola e deflagra (prima sulla wyvern
   che la punge), Hella lancia i semi di fuoco e i colpi infuocati e cura, e
   Thorik e Tordek abbattono la wyvern a terra e poi tirano le corde.
2. **T4, la Catena.** Come T1, ma nei round in cui il drago è a terra il primo
   colpo va sulla runa.
3. **T2, tutti in volo.** Pozioni di volare per Thorik, Tordek e Hella.
4. **T3, il barile sul drago.** Come T1, più Thorik in volo con la botte sopra il
   drago inchiodato.

## Quello che la misura dice

1. **Il drago quasi non muore: 0-5% in ogni riga.** La fuga a ⅓ dei pf e la CA
   40 fanno di «ferito grave» l'esito normale (70-90%). È quello che il master
   chiama «il più probabile», e la misura lo conferma.
2. **La prima paura è il colpo che uccide.** A ⅓ dei pf, fermo in aria, il drago
   fa l'attacco completo su chi lo ha ferito di più, che di solito è Artemis.
   Con l'attacco completo almeno un PG muore nel 79% dei duelli T1. Se in quel
   round esita e non attacca, si scende al 42%. Il testo dice «esita», ma la
   regola di Fluttuare gli dà l'attacco completo.
3. **Le corde costano ai PG più di quanto rendono.** Inchiodato, il drago fa
   l'attacco completo su chi tiene la corda, in media più di 80 danni. Con la CA
   40, invece, Thorik e Tordek lo colpiscono di rado. Se passa il round a
   liberare l'ala, le morti di T1 scendono dal 42% al 18% (insieme alla
   variante sull'esitazione).
4. **Contro la CA 40 Thorik e Tordek contano poco.** Il duello lo fanno Artemis
   e Hella. La Catena a CA 44 si spezza nel 4-6% dei duelli, nel 13% se i loro
   bonus sono 4 più alti della stima.
5. **Dissolvere chi vola e non lo minaccia è un'azione sprecata.** In T2 il
   *dissolvi* sui nani in volo li rimette a terra, dove abbattono la wyvern: i
   PG vanno meglio (morti 72% contro 84%). Un drago con INT 18 lo usa solo su
   chi in aria lo minaccia: chi lancia incantesimi o porta un barile.
6. **Il barile sul drago inchiodato rende**, ma di poco: l'1-5% di draghi uccisi
   in più e circa 10 pf di danno medio in più.

## Il carattere

Arrogante e orgoglioso, il tipo del drago antico che parla, si vanta e ha un
punto debole che non ha mai voluto vedere. Il master lo ha già: grida i nomi,
vuole essere visto, la Catena è la riga che non ha letto. Quello che stona è la
prima paura. Il testo dice che per la prima volta nella sua vita esita, ma i
numeri gli fanno fare il round più letale del duello. È la scelta portata al DM
sulla card del 15/11.
