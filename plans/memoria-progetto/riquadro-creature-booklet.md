---
name: riquadro-creature-booklet
description: Riquadro unico delle creature nei booklet (ADR-0105, PR #295, 2026-10-29): forma, misura, cosa resta da convertire
metadata:
  type: project
  modified: 2026-10-29T07:17:27.004Z
---

Jfs 2026-10-29: tutte le creature (PNG, villain, mostri, PG) nei booklet in un layout uniforme, misurato anche in stampa.
- ADR-0105 (0104 lasciato al thread immagini in posa, mai prenotato). Riquadro a fasce Difesa/Attacco/Statistiche/Capacità speciali/Tattiche in Typst, HTML e Homebrewery, riempito dal recinto ```statblocco + righe ADR-0091. `gs:` testo («PG di 13°») o «—» ammessi.
- Ancora `#scheda` in componenti.py; `misura_statblocchi_booklet.py --check` in CI, tetti in docs/audit/statblocchi-booklet.json (solo verso il basso).
- Prima 4/79, poi 76/88 (ARC-07, Palio, Abbazia al 100%; Drappo: fuori i 6 pregenerati, letti anche da dmcore.schede).
- 2026-10-29 Jfs ha scelto «Fermarla»: la #295 resta in bozza, NON si unisce; si rifà dentro uno standard unico dati→layout (piano in /mnt/project-files/standard-stampa/PIANO.md), confrontato con gli AP 3.5/PF1e più apprezzati per impaginazione (ricerca in standard-stampa/RIFERIMENTI-AP.md).
- Scelta di Jfs: riquadro anche per le creature minori delle tabelle (worg, orchi, wyvern).
- Conversione: mai cambiare numeri (confronto numeri prima/dopo); la regia per il tavolo resta sotto il riquadro. Le schede dei PG in PG/schede/*.yaml citano frasi esatte dei master (`cita:`): validate_pg fallisce se la frase sparisce.
- Piano plans/PIANO-STANDARD-STAMPA.md; `misura_stampa.py` in CI (tetti in docs/audit/stampa-booklet.json, solo in giù) compila con --ignore-system-fonts e conta righe, non span. Solo fonti legali per pagine AP.
- D5 decisa da Jfs 2026-10-29: schede intere in appendice (come RHoD); nell'incontro riga con rimando + la tattica di quell'incontro (cambia per tempo/luogo). ADR-0105 da emendare.
- 2026-10-29 A3 chiuso con Burnt Offerings intero (PDF di Jfs, fuori repo): Paizo 9 pt/1,33/63 car, box da leggere sans colorato senza riquadro, schede 31-34 car, tattica sempre nell'incontro, ibrido scheda intera alla 1ª comparsa + «see page N» (≠ D5 = appendice WotC), illustrazioni 3× le nostre (ritratto accanto a 8/15 schede). standard-stampa/CONFRONTO-PAIZO-AP-2026-10-29.md; risultati passati al thread padre.
- 2026-10-29 commit 88bcd3b3 nella #295: appendice fatta (Typst `modo-schede`/`appendice-creature()`, HTML, HB; manifest `"schede": "qui"` per i volumi giocatori). Schede spezzate 14→0, Drappo schede PG fuori gabbia 299→0. `varianti_stampa.py` per il cieco di I6: CIECO.pdf in /mnt/project-files/standard-stampa/cieco-2026-10-29/ (chiave nella sottocartella non-aprire-prima-del-voto). In Typst una riga compatta sotto un float a piena larghezza deve essere `breakable: true` (bug 0.15).
- Cieco I6 votato da Jfs 2026-10-29: box da leggere colorato scartato 4-0 (resta nel riquadro); interlinea 1,08 vs 1,30 pari 2-2, resta 1,30 (commit 88336943).
- 2026-10-29 21:06 la #295 è unita su main (fe93e5b, testa 8833694, CI verde), dopo che Jfs ha tolto la bozza alle 20:56. Al cieco I6 il box colorato perde 4 a 0 e l'interlinea finisce 2 a 2, quindi resta 1,30. Il piano STANDARD-STAMPA resta aperto su A4, I1, I2, I4, I5, il resto di I7 e V1-V3.
- PR #297 unita il 2026-10-29: titoli appendice senza sillabazione (23→0), scheda che continua nella colonna accanto sulla stessa pagina (posizioni calcolate sommando altezze, non here(): con here() l'impaginazione non converge), misura rimandi_sbagliati tetto 0, misura fallisce se Typst non converge. Lezione Typst: contesto/metadata prima di un blocco non spezzabile si sposta con il blocco; nel piede ripetuto allineato a destra la x non è quella della colonna.
- PR #298 (2026-10-30, testa e530a782, in CI): capitolo VII barile in Notte e Alba + M7-H in DEF-4 App. D. Jfs ha scelto di rifare le scritte invece di alzare i tetti: nuovo `render_map_svg.py --tema stampa` (rendered-stampa/, mappa + `_legenda`, corpi ≥7,4 pt per gabbia A4 17,5 cm, niente filtri/vignetta perché Typst li rasterizza a 288/72 dpi), GUIDA-MAPPE §5.5, seguito ADR-0105. Tetti di main invariati. M7-C e le altre mappe di I2 possono passarci una alla volta.
- 2026-10-30 Jfs ha scelto al cieco (X texture/Y pergamena/Z pianta) lo stile pianta di Dauth: `--stampa` ora è un modo di ogni tema (rendered-stampa-<tema>/), M7-H e M7-C in pianta-stampa nella #298; tetti ARC-07 scesi a 217/52, 256/62, 217/50. Chiave in /mnt/project-files/standard-stampa/cieco-mappe-2026-10-30/.

2026-10-30 (stessa PR #298, commit dfdb8e3c): Jfs ha chiesto la pianta in stampa per TUTTE le mappe «se le misure migliorano». ADR-0106 (proposta): ogni rendered/ ha rendered-stampa-pianta/ (mappa + _legenda), validate_maps lo pretende, validate_booklets ferma pergamena/mappa senza legenda nei booklet. 56 mappe: scritte <7 pt 5820→0, filtri 418→0, testi persi 0. ARC-07 tre volumi righe <7 pt a 0. Nove mappe piccole scendono da 7,6-9,7 a 7,4 pt (non in booklet). Confronto in plans/esperimenti/stampa-mappe-2026-10-30/.

2026-10-30 seguito (#298): nessuna griglia ASCII stampata nei booklet ARC-07 (ASCII → `<!-- apparato -->`, validate_booklets la ferma). Scelte Jfs: S-1/R-1/T-5 in scala in Mappe/ARC07-MAPPE-SCHEMATICHE-IN-SCALA.md (S-1 = pianta PF-2 con affreschi DEF-2, differenze in nota); T-1/T-4/M7-A schemi da scripts/render_schemi.py (--check in CI; uno schema più alto della pagina va spezzato in schema + _legenda, sennò Typst lo rimpicciolisce sotto 7 pt). Il thread ha un tetto di 24 allegati: anteprime in /mnt/project-files/standard-stampa/mappe-2026-10-30/.

2026-11-10 Jfs (thread padre): due stampe coerenti, volume d'avventura (Paizo + schede RHoD, ADR-0122) e booklet di serata. Prima di abbandonare un contenuto del booklet attuale, card a Jfs che dice dove va ogni cosa, con la consigliata. Standard di fatto della community anche per la stampa di serata, misurato.
