# ADR-0086 — Una sostituzione nella resa delle mappe entra solo se misurata e preferita

- **Stato**: **accettata** (il DM, il 2026-10-09: D23-D26 di [PIANO-RESA-E-ASSET-DELLE-MAPPE](../PIANO-RESA-E-ASSET-DELLE-MAPPE.md)); attuata nel codice lo stesso giorno, le tessere da giudicare arrivano dalla macchina del DM
- **Data**: 2026-10-09
- **Decisori**: DM (Gianfranco Samuele), agente
- **Rapporti**: si applica a ciò che [ADR-0085](ADR-0085-la-resa-delle-mappe-e-uguale-su-ogni-macchina.md) e i suoi emendamenti hanno fatto entrare (texture CC0, oggetti dai modelli 3D) e a ciò che entrerà (immagini generate, [ADR-0019](ADR-0019-licenza-dei-pesi-non-del-software.md)); le dipendenze di sviluppo sono quelle di [ADR-0084](ADR-0084-il-collaudo-delle-mappe-e-uno-strumento-di-sviluppo.md); il gate di rifiuto è quello di `rumblingstone-art-direction` §6

## Contesto

Il tema texture (#227) e gli oggetti dai modelli CC0 (#229) sono entrati perché
la licenza era pulita e il DM aveva scelto la strada, non perché qualcuno avesse
misurato che la mappa si leggeva meglio. Guardando le prime prove il DM ha
scritto che *«i letti o i detriti di roccia come glifi sembrano più belli che
le equivalenti modelli CC0»*, e ha chiesto che ogni sostituzione sia
**migliorativa e misurata con algoritmi**, glifo per glifo, comprese le texture
già entrate, con le metriche che la community usa davvero.

Il 2026-10-09 nessun algoritmo del repo misurava l'estetica delle mappe. Quelli
che girano da soli controllano l'integrità (`validate_maps` confronta i byte,
`build_*_cc0 --check` le impronte e le licenze) e la giocabilità
(`collaudo_mappe`). `--misura-stile` di R4-ter descriveva le tessere e non
decideva niente.

La prima misura sul tema texture, fatta per questa decisione, ha trovato
regressioni vere che nessuno aveva visto: il contrasto mediano dei glifi da 7,9
a 4,5; i glifi sotto 3:1 da 5 a 17; creste ⛰ e pedana 🔳 a ΔE 1,2, cioè dello
stesso colore all'occhio.

## Decisione

1. **Tre livelli di misura, con ruoli diversi.**

   | Livello | Cosa | Dove gira | Ruolo |
   |---|---|---|---|
   | A | contrasto del contorno (WCAG 2.1 §1.4.11, 3:1), nitidezza del bordo (Sobel), somiglianza col simbolo più vicino (SSIM, Wang 2004), distanza dalla tavolozza della casa (ΔE CIEDE2000), inchiostro, colorfulness (Hasler e Süsstrunk 2003); per i terreni ΔE dal più vicino, visibilità della griglia, contrasto del segnalino | qui, in CI, ovunque: numpy e scikit-image (BSD-3), Chrome per rasterizzare | **cancello** |
   | B | CLIP-IQA, LPIPS, DISTS di `piq` (Apache-2.0) | sulla macchina del DM: torch e pesi da scaricare | **secondo parere** (D26); cancello solo se concorda col DM, κ ≥ 0,6 |
   | C | il confronto a coppie alla cieca: glifo e candidato, lato e ordine casuali con il seme scritto | il DM, nel browser | **cancello** |

2. **Una sostituzione entra solo se passa A e C** (D23): non peggiora il
   livello A rispetto al glifo, e il DM la preferisce alla cieca in ogni
   ambiente provato. `build_oggetti_cc0.py --check` lo verifica leggendo
   `scripts/scheda-resa.json`.

3. **La resa non può peggiorare in silenzio.** `scripts/scheda-resa.json` tiene
   le misure di ogni simbolo-oggetto nei due temi e su due terreni, e di ogni
   terreno con texture. `misura_resa.py --check` in CI ricalcola e boccia ogni
   misura peggiorata oltre il 5%; per cambiarla si riscrive la scheda, e la
   riscrittura passa dalla PR.

4. **Il tema texture si corregge da solo** (D24). `misura_resa.py tara` cerca
   l'alone chiaro più leggero sotto glifi e segnalini e la velatura più bassa
   per terreno che riportano il tema almeno al livello della pergamena, e le
   scrive in `scripts/texture-cc0/taratura.json`, che il renderer legge. Si
   prende il minimo, perché più alone e più velatura avvicinano la foto alla
   pergamena, e la foto è la ragione per cui il tema esiste.

5. **ComfyUI è una fonte in prova** (D25): le immagini generate in locale
   passano dalle stesse misure e dallo stesso confronto, contro il glifo e
   contro il modello CC0. Entrano con la provenienza di ADR-0019 (modello,
   seme, licenza dei pesi) al posto della licenza CC0.

## Alternative scartate

- **IQA-PyTorch (pyiqa)**: la raccolta più completa (NIQE, MUSIQ, TOPIQ,
  NIMA), ma la licenza è PolyForm Noncommercial. Fuori.
- **Il predittore estetico di LAION** come metro: il codice è Apache-2.0, la
  licenza dei pesi non è scritta sulla pagina del progetto; ed è tarato su
  fotografie belle, non su icone da 28 px.
- **Solo la misura** o **solo la preferenza** (D23): la misura senza l'occhio
  del DM premia ciò che le metriche sanno vedere; l'occhio senza la misura non
  ferma le regressioni che nessuno guarda, come quelle del tema texture.
- **Golden image** (confronto pixel per pixel con un PNG approvato, come
  BackstopJS o `toHaveScreenshot`): già coperta, e meglio, da `validate_maps`,
  che pretende l'SVG identico al byte. Quello che mancava era sapere se la
  resa approvata **era buona**, non se era cambiata.

## Le conseguenze

- Il DM ha un lavoro in più per ogni sostituzione: un confronto alla cieca.
  È il prezzo della D23, e il punto.
- La CI rasterizza con Chrome: circa un minuto in più, e una dipendenza di
  sviluppo nuova (scikit-image). Senza browser la misura dice che non gira e
  non blocca.
- Le soglie del livello A (5%, 3:1, SSIM +0,05) sono una proposta: si ritoccano
  se il confronto alla cieca del DM le smentisce, e si scrive perché.
- Le metriche del livello B non sono tarate su icone: finché non concordano
  con il DM non decidono niente.
- Le misure del livello A sono misure **di leggibilità e di coerenza**, non di
  bellezza. Che un glifo «sembri più bello» lo dice solo il livello C.
