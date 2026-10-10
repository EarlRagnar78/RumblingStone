# ADR-0084 — Il collaudo delle mappe è uno strumento di sviluppo, e usa tcod

- **Stato**: **accettata** e attuata (il DM, il 2026-10-08, sera: D16 di [PIANO-COLLAUDO-E-GENERAZIONE-MAPPE](../PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md))
- **Data**: 2026-10-08
- **Decisori**: DM (Gianfranco Samuele), agente
- **Rapporti**: emenda [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md) (aggiunge un tool al piano di sviluppo) e [ADR-0082](ADR-0082-la-mappa-si-collauda-come-grafo-prima-che-come-immagine.md) §5 (che rifiutava `tcod` perché non serviva); riprende la misura di [PIANO-LEVEL-DESIGN](../PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md) §L5 e il rifiuto di ADR-0015 della PR #72; [ADR-0012](ADR-0012-standard-ingegneria-tool-verificabile.md) per la dichiarazione nel manifest

## Contesto

Il DM, la sera della #226, ha chiesto quali progetti, i più aggiornati e
meglio valutati, portano al repo funzioni utili per generare e verificare
mappe, per il level design e per la resa, anche in deroga alla sola libreria
standard: *«misura cosa apporta ciascuno e perché usarlo»*.

ADR-0082 §5 aveva rifiutato `scipy`, `networkx` e `tcod` con una misura: il
collaudo di allora girava su tutto il corpus in 1,3 secondi, e il guadagno non
pagava la dipendenza. Valeva per connettività e componenti. Non valeva per la
linea di vista, che il collaudo non calcolava ancora (V5) e che il criterio di
V5 vuole **esatta su tutto il corpus sotto i 10 secondi**.

Misurato il 2026-10-08 (`plans/esperimenti/orientamento-e-dipendenze-2026-10/`),
sei candidati, ognuno sul corpus vero:

| Candidato | Licenza · ultimo rilascio · peso | Cosa farebbe | Misura | Verdetto |
|---|---|---|---|---|
| `tcod` 21.2.1 | BSD-2 · 2026-06 · 8,2 MB, più numpy | linea di vista (M4, V5), in futuro i percorsi pesati di V6 | M4 da tutte le **43.423** celle: **0,6 s**, contro **69,9 s** dello shadowcasting simmetrico scritto in libreria standard (già a pendenze intere: con `Fraction` era sette volte più lento). Stesso risultato: Jaccard 0,9999, 414 insiemi identici su 470 | **entra** |
| `resvg-py` 0.5.0 | MIT · 2026-08 · 1,4 MB | PNG delle mappe senza browser | circa **37 s a mappa** contro **5,2 s** di Chromium headless, che è già deterministico (8 PNG su 8 identici al byte in due giri) | no |
| `hypothesis` 6.168 | MPL-2.0 · 2026-10 · 1,2 MB | test di proprietà | quattro mutanti dell'asse delle chiusure: ne coglie 3, gli **stessi 3** di un generatore a seme fisso in libreria standard; aggiunge solo il controesempio minimo | no |
| `networkx` 3.7 | BSD-3 · 2026-09 · 2,1 MB | anelli e strozzature (V7) | connettività e componenti già a 1,3 s; i punti d'articolazione sono una trentina di righe | no, finché V7 non misura il contrario |
| `scipy` 1.18 | BSD-3 · 2026-08 · 34 MB | etichette e dilatazioni (M1, M2) | M1 e M2 già nel tempo del collaudo | no |
| `shapely` 2.2 | BSD-3 · 2026-10 · 2,2 MB | fondere i muri dell'export UVTT | i segmenti collineari sono già fusi in `extract_walls` | no |

`tcod` è l'unico che vince sui numeri. Le opzioni presentate al DM erano tre:
opzionale con un ripiego in libreria standard, obbligatoria nel collaudo,
nessuna dipendenza con il criterio dei 10 secondi rilassato.

## Decisione

1. **`collaudo_mappe.py` sta sul piano di sviluppo di ADR-0037**, con i test e
   la CI. Gira in CI e nelle mani di chi disegna una mappa, non la sera della
   sessione: le mappe si disegnano, si renderizzano (`render_map_svg.py`) e si
   esportano (`export_uvtt.py`) in libreria standard come prima.

2. **`tcod` è obbligatoria nel collaudo** (D16, il DM, contro la proposta di
   tenerla opzionale). Sta in `requirements-dev.txt` con `numpy`, che
   `collaudo_mappe` importa direttamente; nel manifest `stdlib_only: false` e
   `external_deps: ["tcod"]`; in `scripts/binari.py` come libreria
   obbligatoria della catena «collaudo mappe». Senza, il collaudo esce con 2 e
   dice come installarla, senza traccia di stack.

3. **Il primo uso è M4, esatta.** Da ogni cella percorribile, la frazione del
   percorribile che si vede, con lo shadowcasting simmetrico, su tutte le
   celle e senza campionamento; avviso `m4/esposizione` sopra 0,45, soglia
   euristica come M1 e M2. Il collaudo intero passa da 1,3 a 2,5 secondi.
   Questo anticipa la parte di V5 che chiedeva la misura; copertura SRD, M7 e
   M8 restano in V5.

4. **Gli altri cinque restano fuori**, e la tabella sopra dice con quale
   misura. Si riaprono con una misura che dica il contrario, come questo ADR
   ha fatto per `tcod`.

## Alternative scartate

| Alternativa | Perché no |
|---|---|
| `tcod` opzionale, importata nella funzione, con il ripiego esatto e lento | era la proposta. Il DM ha preferito un collaudo che dà sempre gli stessi numeri: con il ripiego, lo stesso comando stampa M4 in 2,5 secondi su una macchina e in 70 su un'altra |
| Nessuna dipendenza, V5 in libreria standard | 70 secondi in CI a ogni push per un avviso; e la misura dice che il resto del collaudo ne prende due |
| Riaprire ADR-0037 per tutti gli script | la sua ragione (il portatile del DM, senza rete, alle 20:45) vale ancora per tutto ciò che il DM esegue. Il collaudo non è fra quelli |
| Le dipendenze della PR #72 in blocco (`scipy`, `networkx`, `tcod`, `jsonschema`) | tre su quattro non portano niente che la misura veda oggi. `jsonschema` non la usa nessuno script, e i due validatori scritti a mano non hanno un difetto misurato che la giustifichi |

## Le conseguenze

**Cosa si ottiene.** M4 smette di essere una stima: l'audit di luglio
campionava 1 cella su 7 con Bresenham e sottostimava (0,88 contro 0,913 esatta
sulla mappa del Dirupo). Sul corpus di oggi la mediana è 0,72, e 27 mappe su 38
oltre la soglia, che resta da calibrare. V5 ha già lo strumento per la parte
più cara, e V6 avrà i percorsi pesati di `tcod.path` se servono.

**Quello che si paga.**

- Una terza libreria obbligatoria nel repo, dopo `pyyaml`: 8,2 MB di ruota con
  un'estensione in C, più numpy. `pip-audit` la guarda in CI come le altre.
- Chi lancia il collaudo sul portatile, anche il DM con `dm.py` o con il server
  MCP, deve aver installato `requirements-dev.txt`. Il messaggio d'errore lo
  dice; la catena della sessione non cambia (`test_ambiente`).
- Il test `test_solo_pyyaml_e_obbligatoria` diventa
  `test_solo_pyyaml_e_tcod_sono_obbligatorie`: il cancello che chiedeva di
  rileggere ADR-0037 se cambiava l'elenco ha fatto il suo lavoro.
- Lo shadowcasting di `tcod` e quello scritto per la misura non coincidono
  sempre al bordo (56 insiemi su 470 differiscono di qualche cella). M4 è una
  media e non se ne accorge; una regola di copertura SRD cella per cella, in
  V5, dovrà dire quale dei due segue.

**Quando si rivede.** Se il collaudo entra nella catena della sessione (per
esempio un controllo delle mappe nel corredo della serata), la ragione di
ADR-0037 torna a valere e `tcod` va resa opzionale.

---

## Emendamento della stessa sera: scipy entra, gli altri quattro restano fuori con una misura migliore

**Stato**: accettato dal DM il 2026-10-08 (D17 di COLLAUDO-MAPPE). **Misura**:
[`esperimenti/dipendenze-e-asset-2026-10/`](../esperimenti/dipendenze-e-asset-2026-10/RISULTATI.md).

Il DM ha chiesto perché `resvg-py`, `hypothesis`, `networkx`, `scipy` e
`shapely` fossero rimasti fuori, e di misurarli sul compito per cui li si
adotterebbe, non su uno solo. Rimisurati:

| Libreria | Compito | Misura | Esito |
|---|---|---|---|
| `scipy` | M1 e M2 del collaudo | 20 ms contro 105, risultato identico al decimale | **entra**, obbligatoria nel collaudo come `tcod` (D17, scelta del DM; la proposta era «nessuna») |
| `networkx` | strozzature e anelli (V7) | 461 ms contro 209 del Tarjan in casa, identico su 44 mappe su 44 | fuori: più lenta |
| `shapely` | muri dell'export UVTT | 175 polilinee invece di 1.674 oggetti, ma 1.674 muri in Foundry in entrambi i casi | fuori: al tavolo non cambia niente |
| `hypothesis` | test di proprietà sul grafo del collaudo | 5 mutanti su 6, gli stessi del generatore a seme fisso | fuori: aggiunge solo il controesempio minimo |
| `resvg-py` | PNG senza browser | 5 volte più lento di Chromium, 5-9% dei pixel diversi | fuori |

`scipy.ndimage` sostituisce in `collaudo_mappe.py` il calcolo a mano di M1 e
M2; il test `test_m1_e_m2_come_il_calcolo_a_mano` tiene il vecchio calcolo come
riferimento. Il guadagno assoluto è piccolo (85 ms su un collaudo di 2,5 s), e
lo si dice: entra perché il DM l'ha voluta, con la misura scritta accanto.

**fonttools** (MIT) entra fra le dipendenze di sviluppo per un'altra ragione,
la resa delle mappe ([ADR-0085](ADR-0085-la-resa-delle-mappe-e-uguale-su-ogni-macchina.md)):
serve solo a rigenerare i sottoinsiemi dei font, e il renderer resta in
libreria standard.
