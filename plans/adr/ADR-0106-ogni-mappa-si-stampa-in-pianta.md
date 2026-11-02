# ADR-0106 — Ogni mappa si stampa in pianta

**Stato**: proposta
**Data**: 2026-10-30
**Decisione-fonte**: il DM (Jfs), 2026-10-30, dopo il cieco su M7-H vinto dalla pianta: *«Si per tutte le mappe nel repo diventando std migliorando tutte le mappe e tutti le modifiche registrate in modo che diventino std per tutto il repo»*, e subito dopo: *«se le misure migliorano ovviamente con i confronti che sono stati fatti»*.
**Rapporti**: estende il seguito del 2026-10-30 di [ADR-0105](ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md) (il modo stampa, adottato una mappa alla volta) a tutte le mappe; usa il tema di [ADR-0102](ADR-0102-lo-stile-delle-piante-e-i-generatori-delle-citta-nel-repo.md); non tocca pergamena e texture, che restano per lo schermo e i VTT.

## Contesto

Il modo stampa era nato per M7-H e M7-C, le due mappe che nel booklet di
ARC-07 scendevano a 3 pt. Le altre restavano a pergamena. Il confronto del
2026-10-30 su tutte le 56 mappe del repo
([CONFRONTO.md](../esperimenti/stampa-mappe-2026-10-30/CONFRONTO.md)) dice:

| | Pergamena | Pianta in stampa |
|---|---|---|
| Mappe con scritte sotto 7 pt | 47 su 56 | 0 |
| Scritte sotto 7 pt | 5.820 | 0 |
| Corpo minimo | 1,4 pt | 7,4 pt |
| Filtri che Typst rasterizza | 418 | 0 |
| Testi della pergamena assenti | — | 0 |

Nei tre volumi di ARC-07, con M7-B, PF-2 e M7-D/E/F passate alla pianta come
M7-H e M7-C:

| Volume | Righe < 7 pt prima → dopo | Immagini < 300 dpi | Pagine |
|---|---|---|---|
| Notte e Alba | 217 → 0 | 52 → 45 | 125 → 129 |
| Resurrezione | 256 → 0 | 62 → 45 | 148 → 153 |
| Mille anni | 217 → 0 | 50 → 43 | 88 → 92 |

Il primo giro del confronto ha trovato quattro difetti della pianta, corretti
prima di adottarla: le mappe alte scendevano a 2,3-4,3 pt; le mappe con la
foresta non si disegnavano; la legenda tagliava la parentesi delle voci
(«copertura +4 CA, terreno difficile») e ignorava la legenda del master; le
acque si disegnavano nell'ordine di un set, quindi l'SVG cambiava da un
processo all'altro.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Pianta in stampa per ogni mappa, con `validate_maps` che pretende il gemello e `validate_booklets` che ferma la pergamena nei booklet** (scelta) | una regola sola; ogni mappa è pronta per un booklet prima che serva; la CI la tiene | +112 SVG, ~41 MB su disco e ~9 MB compressi nella storia; nove mappe piccole scendono da 7,6-9,7 pt a 7,4 pt |
| Continuare una mappa alla volta (ADR-0105) | nessun file in più | è quello che ha lasciato 5 mappe a 3-5 pt nei booklet di ARC-07 fino a oggi |
| Solo le mappe che stanno in un booklet | 7 mappe invece di 56 | la mappa entra nel booklet senza versione di stampa, e nessun controllo lo vede |
| Generare la stampa al momento della compilazione, senza committarla | niente MB nel repo | `validate_maps` non può confrontare i byte; il booklet dipende dal renderer del giorno |

## Decisione

1. Accanto a ogni `rendered/` c'è un `rendered-stampa-pianta/` con la mappa e
   la `_legenda` di ogni master
   (`render_map_svg.py --tutti-i-master --tema pianta --stampa`).
   `validate_maps` segnala gli SVG mancanti e quelli non allineati al master.
2. Un booklet punta una mappa generata solo da `rendered-stampa-pianta/`, con
   la sua `_legenda` nello stesso master. `validate_booklets` ferma il resto.
3. In stampa: corpo unico di 7,4 pt; la mappa alta allarga il foglio fino al
   rapporto della pagina; la legenda lunga mette luoghi e zone su due colonne;
   la voce di legenda è intera; i simboli locali prendono il nome dalla
   legenda del master.
4. Una mappa nuova o rifatta entra con le tre versioni: pergamena, texture e
   pianta in stampa.
5. In un booklet la griglia che il renderer sa disegnare non si stampa: al
   suo posto va la pianta, e la griglia resta nel master fra
   `<!-- apparato -->` e `<!-- /apparato -->` (Jfs, 2026-10-30: *«perché le
   mappe con le griglie ultra Clear non sono state rifatte con il nuovo
   metodo e layout?»*). `validate_booklets` lo controlla. Le griglie
   schematiche, che il renderer non legge (T-1, T-4, T-5, S-1, R-1, M7-A),
   passano in pianta così, per scelta di Jfs del 2026-10-30: S-1 (ottagono),
   R-1 (cerchio di 6 m) e T-5 (esagono di 18 m) diventano griglie in scala;
   T-1, T-4 (sezione) e M7-A (non in scala) diventano schemi disegnati nello
   stesso stile, senza griglia. Le tre in scala stanno in
   `Mappe/ARC07-MAPPE-SCHEMATICHE-IN-SCALA.md`; S-1 è la pianta di PF-2 con
   gli affreschi come li mette DEF-2 (scelta di Jfs, 2026-10-30), con le
   differenze in nota. Gli schemi li genera `scripts/render_schemi.py`
   (carta, inchiostro, numeri rossi e corpo di 7,4 pt della pianta, nessun
   filtro), e la CI controlla con `--check` che gli SVG siano quelli dello
   script. Lo stesso vale in tutto il repo per ogni disegno a caratteri in un
   booklet (Jfs, 2026-10-31: «fai diventare standard queste cose in tutto il
   repo»): una carta o una sezione diventa uno schema, una linea del tempo una
   tabella, e il disegno resta come apparato. `validate_booklets` ferma un
   recinto senza linguaggio con 20 o più caratteri di riquadro fuori
   dall'apparato.

## Conseguenze

- I tetti di `docs/audit/stampa-booklet.json` dei tre volumi scendono (righe
  sotto 7 pt a 0); ogni volume ha 4-5 pagine in più, le legende.
- Nove mappe piccole (le sei carte di Dauth, foresta e campo dei cristalli,
  stanza della corona) in stampa hanno la scritta più piccola a 7,4 pt invece
  di 7,6-9,7. Restano sopra la soglia; oggi nessuna è in un booklet.
- La legenda della pianta a schermo (`rendered-pianta/`) ora usa la legenda
  del master per i simboli locali: cinque SVG di ARC-07 rigenerati.
- Il repo cresce di ~9 MB compressi.

## Da rivedere se

- Il DM vuole per le mappe piccole un corpo più grande di 7,4 pt in stampa.
- Una mappa del booklet perde dettagli che il DM usa al tavolo: il controllo
  dei «testi persi» del confronto va rilanciato su quella mappa.
- La crescita del repo diventa un problema: allora la terza alternativa,
  con un controllo dei byte fatto in CI su una compilazione.
