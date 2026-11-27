---
name: registro-px-gruppo
description: Dove sta il registro PX del gruppo (ods del DM) e lo stato del conto ARC-06/ARC-07 verso il 14°
metadata:
  type: project
  modified: 2026-11-05T06:45:45.160Z
---

Il registro PX vero è `00_Red Hand Of Doom/CalcoloPuntiEperienza-current.ods` (foglio «Calcolo PX», una riga per incontro, parte da 28.000 = 8°). Si ferma alla quest della Gemma (ARC-05, 5.800); la riga del finale ARC-06 è vuota. Totali: Thorik 81.130, Tordek 82.946, Artemis 78.495, Hella 78.217 (tutti 13°). Per leggerlo: unzip content.xml e parse XML (odfpy non si installa).

Dopo: solo sessione 4 del 25/09 sul ramo di gruppo, 2.500 a testa a tutti e quattro. `update_xp.py`/xp-ledger non esistono su main.

Conto del 2026-11-05: con i PX scritti nei master ARC-07 i tre PG vivi superano già il 14° (anche nel minimo); Hella 21-50% verso il 14°, passa solo a fine DEF-5 nel conto minimo. Domande D1-D14 in /mnt/project-files/px-arc07-2026-11-05/PX-ARC07-DOMANDE.md; card al DM sul limite di un livello (consigliato: 14° al primo riposo, stop a 104.999). Serve per chiudere la riga del 14° in DEF-4 r. 3825. → [[p16-marcature-inferred]]

Mappa righe foglio (2026-11-05): 74-96 = Cittadella/Tomba (archi 03-04: cavalieri, retriever, palude, beholder, torrette, xorn, rinascita/cerebromorfosi), 97 = ARC-05 gemma, 98 = ARC-06 Corona (vuota). Riga 41 CD 14 = cubo gelatinoso nella torre dei funghi, non la cerebromorfosi. Nota «Duergar Ambush sul ponte» in r.100 col. I, fuori tabella. Risposte DM: Tordek 500 PX mai versati (chiusa); foglio + copia in testo; Hella 0 PX da morta fino al rito.
Fuoco (DM 2026-11-05): Therysol liberata dalle salamandre condivide i PX, divisione per 4; giocati corridoio ricalibrato + Piramide = 7.700 a testa (Thorik, Tordek, Artemis).
DM 2026-11-05: riga 89 = stanza T3 della Tomba (fontana rossa, 2 demoni a due bocche e quattro braccia, `04_tomba_di_Belkram/t3_stanza.txt`) + 2 drow GS 9; «sport» = spore (riga 39); Artemis TS CD 14 superato (nessun −4.000); nota del ponte = chierico di Abbathor alla Scala d'Ossa, già contato.
Corona (DM 2026-11-05): prova della Corona 800 a tutti e quattro. Storia archi 00-06 in /mnt/project-files/px-arc07-2026-11-05/STORIA-ARCHI-00-06.md con 7 dubbi di collocazione righe.
Finale Corona (DM 2026-11-05): 3.737 a tutti e quattro, Hella compresa.
Sala P1-P2 (DM 2026-11-05): 400 a testa ai tre vivi.
Terra (DM 2026-11-05): 11.800 a testa ai tre vivi (completo con Diapason).
Spirito di Hella (DM 2026-11-05): 800 a Hella.
Affreschi DEF-2 (DM 2026-11-05): 1.900 ai tre, 300 a Hella.
Dopo il 25/09 (DM 2026-11-05): giocato solo fino al barile, tenda non chiusa, 0 PX nuovi.
Storia (DM 2026-11-05): righe 43-62 = compagnia drow della torre fungina; riga 36 grell filosofo = Grell Patriarca, battuto all'INIZIO della discesa nella miniera, dove ci sono le torrette (riga fuori ordine; correzione Jfs 07:24).
Storia: riga 74 (cavalieri di Abbathor e non morti) = i cavalieri non morti della Cittadella (arco 03), foglio non in ordine lì.
Storia: righe 78-81 = prime sale della Cittadella.
Storia: riga 20 = morte di Thorik a Traghetto, Moradin lo riporta senza perdita.
Storia: Jorr muore nella valle (arco 00), dopo la riga 21.
Storia: righe 63-64 (statue barbute, vrock) = ultimi piani della torre fungina. Tutte le 7 card storia risposte.
2026-11-05: PR #312 (bozza) con foglio aggiornato (righe 98-108), copia campaign/REGISTRO-PX.md (sotto 00_ il catalogo mostri la leggeva come scheda), PX-DECISIONI.md e STORIA-ARCHI-00-06.md in plans/esperimenti/p16-inferred-2026-11-04/. Totali: Th/To/Ar 104.999 (14°, cap), Hella 86.354. ARC-07 0 marcature aperte, repo 61. Il foglio .ods si modifica con LibreOffice headless via UNO (python3 uno funziona).
Patch ramo di gruppo (livelli per arco + nota PX sessione 4) in /mnt/project-files/px-arc07-2026-11-05/ramo-di-gruppo/, la applica Jfs con git am. state.yaml su main: pg_livello 00=8, 01=10-11, 02=11, 03=11, 04=12, 05=12, 06=13, 07=13 (14 dai PX).
PR #312 unita su main il 2026-11-05 07:37 (head cb03fead). Restano lotti P16: ARC-09, campagna, PG.
2026-11-05: serie unica per il ramo di gruppo in /mnt/project-files/ramo-di-gruppo-2026-11-05/ (0001-0004, provata su ce34599): dado dei caduti, Bane, PX, e Cintura 4/giorno + guarigione rapida Hella + Belkram in state.yaml. Le cartelle vecchie non vanno più applicate. Guida: docs/guides/GUIDA-PATCH-RAMO-DI-GRUPPO.md.
