# ADR-0133 — La scheda a tutta pagina va su due colonne dentro il riquadro

**Stato**: accettata, in prova fino al 2026-11-28
**Data**: 2026-11-14
**Decisione-fonte**: il DM (Jfs), 2026-11-13 23:22: «verifica se nei manuali PF1e e 3.5 le schede sono a pagina piena o in colonna, misura, e adotta in testing e poi stable». Sulla card delle 23:30 ha scelto «Sì, due colonne nel riquadro», in prova 14 giorni.
**Rapporti**: tocca il riquadro di [ADR-0105](ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md) e di [ADR-0091](ADR-0091-la-scheda-del-png-ha-una-forma.md), senza cambiarne l'ordine né i campi. Non tocca pagina, corpo e interlinea, che restano quelli del 12 novembre.

## Contesto

Burnt Offerings (PF1e) e Red Hand of Doom (3.5) stampano la scheda sempre in
una colonna di due: il riquadro occupa il 35-39% della larghezza della pagina.
Da noi 158 schede su 194 stanno già in una colonna. Le altre 36 stanno nelle
appendici a una colonna (`<!-- pagina: una-colonna -->`) di cinque booklet di
ARC-07, larghe quanto la pagina: una riga piena lì è lunga 99 caratteri di
mediana e arriva a 157. Sopra gli 80-90 caratteri l'occhio perde la riga a
capo, e al tavolo la scheda si legge a colpo d'occhio.

## Decisione

1. Quando la pagina è a una colonna, il tema divide il corpo della scheda in
   **due colonne pari dentro lo stesso riquadro**, con 16 pt di canale. Nome e
   GS restano su una riga sola in testa.
2. Una scheda il cui corpo, a mezza larghezza, è più basso di **6 cm** resta
   intera: due colonne di tre righe si leggono peggio di una.
3. L'ordine delle fasce non cambia: si legge la colonna di sinistra, poi
   quella di destra.
4. Una scheda più alta della pagina si spezza come prima, e le due colonne
   riprendono nella pagina dopo.
5. Nelle pagine a due colonne non cambia niente.
6. **In prova 14 giorni**: il 2026-11-28 il DM dice se resta, dopo averla
   usata al tavolo. Per tornare indietro basta togliere il blocco `context`
   in `intero` di `scripts/typst/tema-rumblingstone.typ`.

## Alternative

- **Mettere quelle appendici a due colonne di pagina**: le appendici sono a una
  colonna per le tabelle e i testi lunghi che hanno accanto; cambierebbe pagine
  che il DM ha già letto.
- **Stringere il riquadro a mezza pagina**: lascia mezza pagina vuota e
  allunga i booklet.
- **Lasciare com'è**: è lo stato misurato sopra.

## Misura

Contro main 91a34b37, sui 21 booklet, con `misura_stampa.py` e il conto delle
righe dentro i 36 riquadri larghi:

| | main | questa PR |
|---|---|---|
| righe oltre 100 caratteri | 174 | 11 |
| riga piena, mediana | 99 caratteri | 64 |
| riga più lunga | 157 | 126 |
| pagine dei 21 booklet | 991 | 990 |
| schede spezzate | 2 | 2 |

`misura_stampa.py --tutti --check` è verde; i cinque booklet che cambiano sono
conformi a veraPDF PDF/UA-1 e PDF/A-2a. La serata Notte e Alba resta a 126
pagine; il booklet della Resurrezione scende da 173 a 172.

## Conseguenze

- Le 11 righe lunghe che restano sono di tre schede sotto la soglia dei 6 cm
  (le guardie di Zog'tar, il Treant di Adamantio e la sua copia per i giocatori): lì la
  riga arriva ancora a 126 caratteri. Abbassare la soglia è una scelta del DM.
- Chi legge il PDF con uno schermo sente le fasce nello stesso ordine di prima.
- Cancello: `scripts/tests/test_scheda_due_colonne.py` (due colonne in pagina a
  una colonna, scheda bassa intera, pagina a due colonne invariata, scheda più
  alta di una pagina senza testo perso).
