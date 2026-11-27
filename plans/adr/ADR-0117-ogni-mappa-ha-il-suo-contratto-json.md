# ADR-0117 — Ogni mappa di campagna ha il suo contratto JSON

**Stato**: accettata (2026-11-10, card del DM; proposta il 2026-11-09)
**Data**: 2026-11-09
**Decisione-fonte**: il DM (Jfs), 2026-11-09: *«per le mappe fai sempre il json chiudi il buco e controlla e fixa: su una mappa di Hammerfist (Lotto 2, Assedio), perché le dimensioni dichiarate non tornano con quelle disegnate»*.
**Rapporti**: completa la migrazione di [PIANO-IMPORT-ULTRACLEAR](../PIANO-IMPORT-ULTRACLEAR-ASCII-TO-JSON.md) e porta in CI il `--strict` di [PIANO-RENDER-MAPPE-FEDELTA](../PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md). Il contratto è quello di `scripts/schemas/tactical_map.schema.json` (Modalità 3 di GUIDA-MAPPE). Chiude due voci di RECUPERO D5.

## Contesto

Al 2026-11-09 il repo aveva 73 griglie a emoji nei file markdown. 25 griglie vive non avevano un contratto JSON: 14 in ARC-07, 6 della fortezza di Hammerfist, 5 in ARC-09. Erano scritte a mano, e nessuno controllava che una griglia corretta in un punto restasse coerente altrove.

`import_ultraclear.py` non bastava a migrarle. Riempiva il rettangolo che contiene una formazione anche quando la formazione non è rettangolare (i nani a scacchiera del Cuore della Montagna diventavano un blocco pieno). Scartava inoltre i simboli che un master spiega solo nella sua legenda locale.

L'intestazione di `_ARCHIVIO/Hammerfist-Lotto-2-Assedio.md` dichiarava 120 colonne, ma lo schizzo ne disegna 34. `render_map_svg --strict` lo diceva da tempo, ma `--strict` si lanciava solo a mano.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Un contratto JSON per ogni griglia di campagna, che ricompilato ridà la griglia identica cella per cella, con un test in CI** (scelta) | una fonte sola per ogni mappa; il test boccia una griglia ritoccata a mano senza il JSON; `--strict` diventa cancello | 25 file in più; il contratto minimo non porta ancora tipo, ambiente e quote |
| Il JSON solo per le mappe nuove (regola di prima) | nessun lavoro sulle vecchie | le 25 vecchie restano senza controllo, ed è il buco che il DM ha chiesto di chiudere |
| Rigenerare i master dal JSON e accettare differenze | griglie «pulite» | cambia mappe già giocate e già stampate; la regola del DM sulle battaglie più dure vieta di semplificare di nascosto le formazioni |

## Decisione

1. Ogni griglia a emoji in un file markdown tracciato ha un contratto JSON nel repo. Ricompilato con `compile_map_json.py`, il contratto ridà la stessa griglia cella per cella.
2. Una mappa nuova nasce dal JSON (`compile_map_json.py`). Una vecchia si migra con `import_ultraclear.py FILE --map N -o CONTRATTO.json`, poi si controlla l'identità.
3. Il contratto accetta `simboli_locali` (simbolo → descrizione) per i simboli che non sono nella legenda universale. `emit_master` li scrive nella riga `LEGENDA` della griglia.
4. `import_ultraclear.py` scompone le formazioni non rettangolari in rettangoli pieni e porta i simboli locali. Un simbolo senza una spiegazione nel master è un ERROR (R3).
5. `scripts/tests/test_contratti_mappe.py` è il cancello. Pretende il contratto per ogni griglia e `render_map_svg.py --strict --tutti-i-master` a codice 0.
6. Fuori dal cancello restano le fixture dei test, gli esperimenti, gli esempi della guida e le cartelle `_ARCHIVIO/`. Per l'archivio ha deciso il DM sulla card del 2026-11-09 («Fuori, sono archivio»): sono schizzi deprecati, assorbiti da L2-REVISED e HF-2A, che hanno già il loro JSON.

## Misura

- 25 contratti su 25 ridanno la griglia del master identica.
- `--strict` passa su tutti i master dopo la correzione dell'intestazione del Lotto 2: 34 × 80, disegno fuori scala in larghezza rispetto ai 180 × 120 m dichiarati. Gli SVG non cambiano (`validate_maps`).
- `test_import_ultraclear`: 21 test su 21.
- In archivio, 4 schizzi su 8 non tornano: righe di lunghezza diversa (32-34 celle, 39/40, 20/30/6). Un contratto dipinge sempre un rettangolo.

## Conseguenze

- Chi ritocca una griglia a mano senza toccare il JSON ha la CI rossa, e chi tocca il JSON deve rigenerare la griglia.
- I 25 contratti sono minimi: geometria, unità e legenda. Tipo, ambiente, quote e luci si aggiungono quando servono, per esempio all'export UVTT.
- **Quello che non è misurato:** l'identità vale per la griglia. Le note e le tabelle di coordinate attorno alla griglia restano testo del master.

## Da rivedere se

- il DM sceglie di portare anche l'archivio sotto contratto;
- una mappa ha bisogno di una cella che il formato a rettangoli non sa dire (forme diagonali, celle a metà).
