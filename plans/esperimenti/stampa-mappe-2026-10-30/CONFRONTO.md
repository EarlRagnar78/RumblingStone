# Confronto delle mappe: pergamena contro pianta in stampa (2026-10-30)

Per ogni mappa del repo, la pergamena di `rendered/` contro la pianta in stampa
(`rendered-stampa-pianta/`, mappa e legenda), messe nella gabbia A4 del booklet
(17,5 × 21 cm). Lo script è `confronto.py` in questa cartella; si rilancia dalla
radice del repo: `python3 plans/esperimenti/stampa-mappe-2026-10-30/confronto.py esito.json`.

- **corpo min.**: la scritta più piccola, in punti, una volta stampata;
- **< 7 pt**: quante scritte scendono sotto la soglia di `misura_stampa`;
- **filtri**: gli effetti che Typst rasterizza (a 288 dpi, o 72 dpi la vignettatura);
- **testi persi**: le scritte della pergamena (luoghi, zone, percorsi, voci di legenda) che
  non compaiono nella pianta in stampa. Le etichette di servizio (INDICAZIONI, LEGENDA,
  la riga «N×M quadretti», i numeri della scala) non contano: la pianta le scrive in un altro modo.

## Totale

| | Pergamena | Pianta in stampa |
|---|---|---|
| Mappe | 56 | 56 |
| Mappe con scritte sotto 7 pt | 47 | 0 |
| Scritte sotto 7 pt | 5820 | 0 |
| Corpo minimo | 1,4 pt | 7,4 pt |
| Filtri rasterizzati | 418 | 0 |
| Testi persi | — | 0 |

Dove la pianta non migliora: nove mappe piccole (le sei carte di Dauth, la foresta e il campo
dei cristalli, la stanza della corona) avevano già la scritta più piccola fra 7,6 e 9,7 pt;
in stampa scende a 7,4 pt, il corpo unico del modo stampa. Restano sopra la soglia e
perdono i filtri raster. Nessuna di queste nove sta oggi in un booklet.

## Il primo giro e cosa ha corretto

Il primo confronto ha trovato quattro difetti della pianta, corretti prima di adottarla:

1. le mappe alte (21×53, 20×100, 34×80) scendevano a 2,3-4,3 pt, perché la pagina le stringe
   in altezza: ora il foglio si allarga fino al rapporto della pagina;
2. le mappe con la foresta non si disegnavano (errore di tipo in `_canopy`);
3. la legenda tagliava la parentesi delle voci (19 mappe perdevano «copertura +4 CA, terreno
   difficile», 15 «blocca vista e movimento») e ignorava la legenda del master (🛡️ Thorik,
   💠 base corrosa del pilastro): ora in stampa la voce è intera e i simboli locali hanno il
   loro nome;
4. le acque si disegnavano nell'ordine di un set: l'SVG cambiava da un processo all'altro.

La legenda della fortezza di Hammerfist (120×80, 17 luoghi e 15 zone) superava i 21 cm:
luoghi e zone ora vanno su due colonne quando non stanno su una.

## Mappa per mappa

| Mappa | Celle | Pergamena: corpo min. | < 7 pt | filtri | Stampa: corpo min. | < 7 pt | filtri | testi persi |
|---|---|---|---|---|---|---|---|---|
| M7-D-livello-1-1372_map01_m7-d-1372-il-corridoio-della-fucina-livello-1-gi | 36x23 | 4,3 | 97 | 8 | 7,4 | 0 | 0 | 0 |
| M7-D-livello-1-372_map01_m7-d-il-corridoio-della-fucina-livello-1-notte-3 | 36x23 | 4,3 | 99 | 8 | 7,4 | 0 | 0 | 0 |
| M7-E-gallerie-1372_map01_m7-e-1372-i-passaggi-antichi-livello-2-giorno-3 | 34x24 | 4,5 | 85 | 6 | 7,4 | 0 | 0 | 0 |
| M7-E-gallerie-372_map01_m7-e-le-gallerie-di-zeth-livello-2-notte-372-dr | 34x24 | 4,5 | 73 | 6 | 7,4 | 0 | 0 | 0 |
| M7-F-fucina-grande-1372_map01_m7-f-1372-la-fucina-grande-livello-3-giorno-3-de | 30x22 | 4,9 | 77 | 8 | 7,4 | 0 | 0 | 0 |
| M7-F-fucina-grande-372_map01_m7-f-la-fucina-grande-livello-3-notte-372-dr | 30x22 | 5,1 | 71 | 8 | 7,4 | 0 | 0 | 0 |
| ARC07-MAPPE-DEFINITIVO_map01_foresta-di-cristalli-giganti-27-m-15-m-18-col-10 | 18x10 | 8,3 | 0 | 4 | 7,4 | 0 | 0 | 0 |
| ARC07-MAPPE-DEFINITIVO_map02_campo-dei-cristalli-viventi-30-m-12-m-20-col-8-r | 20x8 | 7,6 | 0 | 5 | 7,4 | 0 | 0 | 0 |
| ARC07-MAPPE-DEFINITIVO_map03_camera-centrale-sfera-60-m-zero-g-ovunque-tranne | 24x16 | 6,5 | 40 | 4 | 7,4 | 0 | 0 | 0 |
| ARC07-MAPPE-DEFINITIVO_map04_stanza-della-corona-15-m-19-5-m-10-col-13-righe | 10x13 | 7,6 | 0 | 6 | 7,4 | 0 | 0 | 0 |
| ARC07-MAPPE-DEFINITIVO_map05_cortile-interno-36-m-27-m-24-col-18-righe-1-5-m | 24x18 | 4,4 | 103 | 9 | 7,4 | 0 | 0 | 0 |
| ARC07-MAPPE-DEFINITIVO_map06_il-cuore-della-montagna-caverna-sacra-100-m-80-m | 33x27 | 4,9 | 76 | 8 | 7,4 | 0 | 0 | 0 |
| ARC07-MAPPE-DEFINITIVO_map07_cm-2-il-cuore-della-montagna-lato-nord-42-m-48-m | 28x32 | 4,6 | 74 | 7 | 7,4 | 0 | 0 | 0 |
| ARC07-MAPPE-M7C-TENDA-DEL-COMANDO_map01_m7-c-la-tenda-del-comando-di-zog-tar-notte-372-d | 27x23 | 3,7 | 115 | 9 | 7,4 | 0 | 0 | 0 |
| ARC07-MAPPE-M7H-QUARTIERE-DEL-COMANDO_map01_m7-h-il-campo-del-capo-lo-spiazzo-la-guardia-del | 44x40 | 3,0 | 164 | 9 | 7,4 | 0 | 0 | 0 |
| Portale-Forgia-L1-REVISED-UltraClear_map01_mappa-pf-1-stanza-della-corona-boss-fight-belkra | 20x14 | 6,9 | 2 | 8 | 7,4 | 0 | 0 | 0 |
| Portale-Forgia-L1-REVISED-UltraClear_map02_mappa-pf-2-sala-della-forgia-eterna-hub-divino | 27x27 | 5,4 | 66 | 8 | 7,4 | 0 | 0 | 0 |
| Portale-Forgia-L2-REVISED-UltraClear_map01_pf-3-corridoio-del-fuoco-fire-gauntlet | 21x53 | 2,8 | 110 | 7 | 7,4 | 0 | 0 | 0 |
| Portale-Forgia-L2-REVISED-UltraClear_map02_mappa-pf-4-forgia-adamantina-boss-elder-fire-ele | 33x33 | 4,8 | 81 | 8 | 7,4 | 0 | 0 | 0 |
| Hammerfist-Lotto-1-Ricognizione_map01_a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-colonne | 20x100 | 1,9 | 131 | 8 | 7,4 | 0 | 0 | 0 |
| Hammerfist-Lotto-1-Ricognizione_map02_a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x | 28x30 | 5,0 | 70 | 9 | 7,4 | 0 | 0 | 0 |
| Hammerfist-Lotto-2-Assedio_map01_mappa-2a-fortezza-hammerfist-vista-dall-alto-top | 34x80 | 2,3 | 130 | 9 | 7,4 | 0 | 0 | 0 |
| Hammerfist-Lotto-3-FINALE_map01_mappa-3x-ingresso-passaggi-antichi-evacuazione-d | 40x40 | 4,0 | 93 | 3 | 7,4 | 0 | 0 | 0 |
| Hammerfist-Lotto-3-FINALE_map02_griglia-33-33-caverna-intersection | 33x33 | 4,7 | 77 | 6 | 7,4 | 0 | 0 | 0 |
| Hammerfist-Lotto-3-FINALE_map03_golden-sphere-manifestation-round-8 | 40x41 | 4,0 | 93 | 5 | 7,4 | 0 | 0 | 0 |
| Hammerfist-Lotto-3-FINALE_map04_ground-battle-120m-200m | 30x71 | 2,5 | 114 | 6 | 7,4 | 0 | 0 | 0 |
| Hammerfist-L1-REVISED-Ultra-Clear_map01_mappa-1a-2-revised-il-torrione-di-vedetta-grigli | 40x40 | 3,1 | 139 | 6 | 7,4 | 0 | 0 | 0 |
| Hammerfist-L1-REVISED-Ultra-Clear_map02_mappa-1a-1-revised-il-sentiero-nascosto-canyon-c | 20x100 | 1,7 | 170 | 7 | 7,4 | 0 | 0 | 0 |
| Hammerfist-L1-REVISED-Ultra-Clear_map03_mappa-1a-3-revised-campo-della-mano-rossa-vista | 60x60 | 2,5 | 173 | 9 | 7,4 | 0 | 0 | 0 |
| Hammerfist-L1-REVISED-Ultra-Clear_map04_mappa-1d-il-pendio-sotto-le-mura | 12x12 | 5,6 | 70 | 8 | 7,4 | 0 | 0 | 0 |
| Hammerfist-L2-REVISED-Ultra-Clear_map01_mappa-2a-revised-fortezza-hammerfist-top-down-sc | 120x80 | 1,4 | 305 | 11 | 7,4 | 0 | 0 | 0 |
| Hammerfist-L2-REVISED-Ultra-Clear_map02_mappa-1-revised-disposizione-generale-giorno-1-0 | 60x108 | 1,5 | 240 | 11 | 7,4 | 0 | 0 | 0 |
| Hammerfist-L2-REVISED-Ultra-Clear_map03_mappa-2b-corretta-revised-attacco-del-drago-sui | 40x26 | 3,9 | 126 | 8 | 7,4 | 0 | 0 | 0 |
| Hammerfist-L3-REVISED-Ultra-Clear_map01_mappa-h3-1-revised-cortile-sfondato-ultima-difes | 72x36 | 2,2 | 195 | 10 | 7,4 | 0 | 0 | 0 |
| Hammerfist-L3-REVISED-Ultra-Clear_map02_mappa-3y-revised-il-ponte-sospeso-retroguardia | 33x27 | 4,1 | 112 | 7 | 7,4 | 0 | 0 | 0 |
| Hammerfist-L3-REVISED-Ultra-Clear_map03_mappa-3z-revised-l-incrocio-silenzioso-imboscata | 33x33 | 3,4 | 148 | 6 | 7,4 | 0 | 0 | 0 |
| Hammerfist-L3-REVISED-Ultra-Clear_map04_mappa-5-revised-il-cuore-della-montagna-ultima-r | 67x53 | 2,4 | 208 | 10 | 7,4 | 0 | 0 | 0 |
| Hammerfist-L3-REVISED-Ultra-Clear_map05_mappa-4-revised-battaglia-finale-terrestre-caric | 60x68 | 2,1 | 206 | 10 | 7,4 | 0 | 0 | 0 |
| DAUTH-A-breccia-porta-sud_map01_dauth-carta-a-la-breccia-della-porta-sud-giorno | 12x9 | 8,0 | 0 | 8 | 7,4 | 0 | 0 | 0 |
| DAUTH-B-razorfiend-sui-bastioni_map01_dauth-carta-b-il-razorfiend-sui-bastioni-giorno | 16x4 | 8,7 | 0 | 3 | 7,4 | 0 | 0 | 0 |
| DAUTH-C1-chiostro-ospedale_map01_dauth-carta-c-il-chiostro-ospedale-giorno-3 | 10x10 | 7,8 | 0 | 8 | 7,4 | 0 | 0 | 0 |
| DAUTH-C2-cunicolo-cisterna_map01_dauth-carta-c-il-cunicolo-della-cisterna-sotto-i | 5x8 | 9,2 | 0 | 7 | 7,4 | 0 | 0 | 0 |
| DAUTH-D-lance-di-khorn_map01_dauth-carta-d-le-lance-di-khorn-sulle-mura-ovest | 14x6 | 9,7 | 0 | 6 | 7,4 | 0 | 0 | 0 |
| DAUTH-E-cellula-nelle-mura_map01_dauth-carta-e-la-cellula-nelle-mura-corpo-di-gua | 8x8 | 8,2 | 0 | 6 | 7,4 | 0 | 0 | 0 |
| Arco-Post-Hammerfist-P1B-Cerchio-Treant-COMPLETO-maps_map01_cerchio-sacro-della-foresta-60m-diameter-circle | 40x40 | 3,5 | 112 | 6 | 7,4 | 0 | 0 | 0 |
| Arco-Post-Hammerfist-P1B-Foresta-In-Fiamme-MAPPA_map01_foresta-in-fiamme-i-piromanti-drow-quest-di-hell | 34x24 | 4,2 | 123 | 5 | 7,4 | 0 | 0 | 0 |
| Arco-Post-Hammerfist-P1C-Rituale-COMPLETO-SCALE_map01_campo-drow-1-burning-operations-80m-60m-53-40-gr | 53x40 | 3,1 | 115 | 10 | 7,4 | 0 | 0 | 0 |
| Arco-Post-Hammerfist-P1C-Rituale-COMPLETO-SCALE_map02_ondata-2-positions-round-22-fase-2 | 40x40 | 4,1 | 96 | 6 | 7,4 | 0 | 0 | 0 |
| Arco-Post-Hammerfist-P1C-Rituale-COMPLETO-SCALE_map03_desperate-last-stand-round-36-40 | 40x40 | 4,1 | 96 | 6 | 7,4 | 0 | 0 | 0 |
| SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO_map01_campo-drow-1-burning-operations-base-80m-60m-gri | 53x40 | 3,0 | 136 | 10 | 7,4 | 0 | 0 | 0 |
| SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO_map02_campo-drow-2-forward-base-98m-80m-grid-65-53-sca | 65x53 | 2,5 | 181 | 11 | 7,4 | 0 | 0 | 0 |
| tarsilia-la-ruota-giocatori_map01_tarsilia-versione-giocatore | 64x46 | 2,6 | 136 | 8 | 7,4 | 0 | 0 | 0 |
| tarsilia-la-ruota_map01_tarsilia-la-ruota-pista-del-drappo | 64x46 | 2,5 | 171 | 8 | 7,4 | 0 | 0 | 0 |
| tarsilia-stalle_map01_tarsilia-le-stalle-dell-istrice-assalto-notturno | 21x15 | 4,8 | 87 | 8 | 7,4 | 0 | 0 | 0 |
| campo-drow-1_map01_campo-drow-1-burning-operations-base-ricostruzio | 53x40 | 3,0 | 160 | 7 | 7,4 | 0 | 0 | 0 |
| hammerfist-L2-assedio_map01_hammerfist-l2-assedio-della-fortezza-ricostruzio | 120x80 | 1,4 | 274 | 10 | 7,4 | 0 | 0 | 0 |
