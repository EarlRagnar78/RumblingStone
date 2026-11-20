# ADR-0147 — L'introduzione del capitolo promette e non conta

**Stato**: proposta (2026-11-20), scelta dal DM alla cieca
**Data**: 2026-11-20
**Decisione-fonte**: il DM (Jfs), 2026-11-20, 12:40: «per ogni introduzione inserire una parte letta ai giocatori che sia epica […] non è un libro di ragioneria ci vuole estro e stile», e alle 14:25 ora italiana, sulla versione finale: «bene mi piace diventa lo standard questa versione».
**Rapporti**: completa [ADR-0122](ADR-0122-il-volume-segue-lo-schema-degli-adventure-path.md) (S1, l'introduzione del capitolo); la divergenza dagli editori entra per [ADR-0145](ADR-0145-l-ordine-del-booklet-della-serata-si-misura.md) e il voto alla cieca di [ADR-0093](ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md). Norma: `skills/rumblingstone-narrative-style/references/read-aloud-adulti.md` §2-quater.

## Contesto

Le prime introduzioni della serata di ARC-07 dicevano al DM che cosa succede, quali mappe tenere e come si chiude il capitolo: regia, non atmosfera. Gli editori di riferimento aprono sul mondo. Le parti di *Burnt Offerings* cominciano dall'antefatto («For five years…»), l'introduzione della Parte I di *Red Hand of Doom* è un paragrafo, e nessuna delle due mette mappe o conteggi nella prosa d'apertura: misurate, 0 parole di regia ogni 100 nelle aperture di luogo, contro 1,5-7,8 delle nostre. Paizo chiude l'introduzione con l'«Advancement Track», generico, e non nomina mai i PG di un gruppo.

Due giri alla cieca col DM: il primo, solo più corto e meno contabile, ha vinto 9 a 0 ma non bastava; il secondo, con il box per i giocatori, 8 a 1, e l'unica coppia persa è entrata come il DM l'ha scelta su card.

## Decisione

Ogni capitolo di gioco ha:

1. **un paragrafo per il DM che apre sul mondo**, senza mappe, tacche, registri, PX né «il capitolo dà al DM»: quelli stanno nella regia della serata;
2. **un box da leggere ai giocatori** nel registro del trailer: promette e non svela, finisce su un'immagine aperta, almeno due sensi, 8-12 righe;
3. **una nota del livello**, generica come in Paizo: a che livello gli eroi dovrebbero essere e dove il capitolo li porta;
4. in fondo al capitolo, **una nota dei PX** con tutte le quest e senza le facoltative (chiave `chiusura` del manifest, `dmcore.testo.con_chiusura`).

Introduzioni, note e appendici parlano di **eroi**, mai dei PG del tavolo; i PNG mantengono il nome. La storia di una regione si scrive **a epoche datate**, al passato remoto, ognuna con la sua svolta, come le voci di regione del *Forgotten Realms Campaign Setting* e i gazetteer degli AP.

## Conseguenze

- Misura, a indicatori e non a cancello: `python3 scripts/misura_craft.py --apertura FILE…` (box, righe, sensi, contabilità per 100 parole, cifre nel box, nota del livello).
- Il box per i giocatori diverge dagli editori: Paizo non lo mette nelle parti, *Red Hand of Doom* ne ha uno solo. Resta perché il DM l'ha scelto alla cieca; se un giro futuro lo boccia, si toglie.
- L'emozione non si misura: lo strumento conta quello che la spegne e quello che la porta, il resto lo decide il cieco.
- Le tabelle dentro un capitolo galleggiano in fondo: le note dei PX sono elenchi.
- I PX di un gruppo preciso stanno nel suo registro (`campaign/REGISTRO-PX.md`), non nel modulo.
