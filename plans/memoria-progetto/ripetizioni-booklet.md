---
name: ripetizioni-booklet
description: Misura delle ripetizioni nei booklet (13/11/2026): la serata ripete il 12,3% delle parole contro l'1,2% di Burnt Offerings; come si conta e cosa resta da fare
metadata:
  type: project
---

Jfs, 2026-11-12 22:40 («come mai è così lungo, siamo sicuri che non ci siano ripetizioni non misurate?»): le ripetizioni non erano misurate. Misura del 2026-11-13 sul PDF: parole che stanno in passi di almeno 8 parole identiche, contate dalla seconda volta, tolte le testatine (n-grammi su più di 8 pagine).
- Serata «La Notte e l'Alba»: 125 pp, 72.041 parole, 8.842 ripetute = 12,3%.
- Burnt Offerings (uploads/hearth/165a89a4…): 100 pp, 73.899 parole, 1,2%. Estratto RHoD (dc4571c4…): 0,5%.
- Circa 3.700 parole sono copie volute da Jfs il 10/11 (schede e mappe intere in appendice); circa 5.200 nel corpo: schede d'entrata «in breve» ristampate a ogni scena, pezzi di scheda del capitolo II ripetuti nel capitolo X, mappa M7-C due volte.
- Stesse parole di Burnt Offerings ma 25 pagine in più: conta anche l'impaginazione.

**Why:** la lunghezza del booklet è il difetto che Jfs vede; i giri dei lettori guardavano solo le aperture di scena.
**How to apply:** PR di seguito alla #370 (unita, b6bae7be): portare la misura in `misura_stampa.py` fra le IN_PROVA con la soglia presa dai due riferimenti, e una card a Jfs sulle copie da togliere (i tagli di testo sono suoi). Lo script di prova era nello scratchpad della sessione, da riscrivere. Vedi [[standard-volume-booklet]] [[scheda-da-tavolo-scene]].

**Aggiornamento 2026-11-13.** PR #395 (bozza, ramo `claude/project-thread-u8xojz`): la misura `parole_ripetute` entra in prova in `misura_stampa.py`, voce MS-0085 (la #393 aveva prenotato lo stesso numero: chi entra dopo rinumera). Nessuna soglia. Lettura onesta dei numeri della serata: 72.041 parole in 125 pagine = 576 parole per pagina, *Burnt Offerings* 739; alla densità dell'AP lo stesso testo starebbe in circa 97 pagine. Le copie valgono poco: scheda d'entrata di Zog'tar «in breve» stampata 4 volte (pp. 24, 58, 75, 83), circa 1.300 parole di schede d'entrata ripetute = circa 2 pagine; tutte le copie del corpo 5.177 parole = al più 9 pagine. Card aperta a Jfs il 13/11: quali copie togliere (consigliata: nessuna, provare la densità di pagina). I tagli restano suoi.

**2026-11-13, dopo.** #395 unita: 43d42b96, voce MS-0086.

**2026-11-13 pomeriggio.** Jfs sulla card: «pagine più fitte + b + c insieme». PR #399 (bozza, MS-0088): manifest `"pagina": "fitta"` (A4 9,6 pt, interlinea 0,56em) e `"copie": "una-volta"` (riga per il tavolo e scheda in breve una volta sola, poi una riga con le pagine); solo la serata le usa. 125 → 113 pagine (la stima di 100 era sbagliata). Prezzo misurato: numeri di Zog'tar a 13 pagine in mediana invece di 5. Non tagliate le circa 1.100 parole di frasi dette due volte fra regia e scene (meno di 2 pagine, scelta di testo): detto a Jfs. La misura ora toglie le testatine riga per riga (BO 1,1%, RHoD 0,4%). PDF in /mnt/project-files/serata-corta-2026-11-13/.

**2026-11-13 14:17, Jfs boccia le schede accorpate.** Visto il PDF: «le schede dei png mostri e villan e gregari si leggono peggio così accorpate». `"copie": "una-volta"` tolta dalla #399 (non accorciava: 113 pagine con e senza). Resta solo `"pagina": "fitta"`: 125 → 114 pagine (margini laterali 2,0 e 1,5 come gli altri: a 1,8 e 1,3 erano 113 ma `misura_stampa --tutti --check` andava rosso per righe fuori margine ed emoji delle mappe sopra i 2 cm), testo identico a main (MS-0090, testa d48d0af0). Prima di spingere lanciare sempre misura_stampa con --check. **Come applicarlo:** schede e righe per il tavolo restano intere in ogni scena; non riproporre rimandi al posto delle schede. PDF buono: /mnt/project-files/serata-corta-2026-11-13/ARC07-NOTTE-E-ALBA-SERATA-114pp-schede-in-ogni-scena.pdf.

**Unita.** #399 su main il 13/11: merge 32bfbfdc.

**2026-11-13 16:09, Jfs: schede «tutte attaccate», fa fatica a leggerle.** Causa misurata: l'interlinea della pagina fitta entrava nelle schede (passo 11,2 → 10,6 pt in appendice, 12,0 → 11,1 nei capitoli; corpo 8,8 pt invariato). PR #402 (MS-0092): `statblocco` fissa l'interlinea del tema, 114 pagine invariate. **Come applicarlo:** ogni cambio di densità della pagina va confrontato sulle schede con i PDF precedenti prima di consegnare; le schede non si stringono. Proposto a Jfs, non fatto: fasce Difesa/Attacco anche nelle schede in breve dei capitoli. Confronti in /mnt/project-files/serata-corta-2026-11-13/confronto-*.png; PDF buono `…-114pp-schede-ariose.pdf`.

**Unita.** #402 su main il 13/11: merge 0c25ab2d, voce rinumerata MS-0093.

**2026-11-13 18:58, Jfs: «Preferisco sempre la versione del 12 novembre, abbandona la versione stretta per tutto».** Pagina fitta tolta del tutto (PR #406): serata di nuovo 125 pagine, corpo 10,2 pt, schede col passo di riga del 12/11. In un giorno Jfs ha bocciato schede accorpate, schede strette e pagina fitta. **Come applicarlo:** non proporre più di accorciare i booklet stringendo pagina, corpo, interlinea o schede; la densità degli AP non è un obiettivo per Jfs, la leggibilità sì. PDF buono: /mnt/project-files/serata-corta-2026-11-13/ARC07-NOTTE-E-ALBA-SERATA-125pp-come-il-12-novembre.pdf.

**Unita.** #406 su main il 13/11: merge cc18206e, voce MS-0097.
