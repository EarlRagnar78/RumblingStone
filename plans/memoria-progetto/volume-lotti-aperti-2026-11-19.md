---
name: volume-lotti-aperti-2026-11-19
description: Lotti dello standard del volume (ADR-0122) e corredo RC-001 al 20/11: quattro PR in bozza (#505-#508), confronto con gli AP sui PDF caricati, trappole della misura
metadata:
  type: project
  modified: 2026-11-20T09:11:04.519Z
---

**Le PR (20/11), tutte in bozza, unione solo dopo la stampa della sera del 20/11 e la lettura di Jfs (card).**
- #505 corredo RC-001 (bugbear, orog, Spezzamente, duergar, Furia) + hobgoblin W4 con +2 Des/+2 Cos razziali (card del 20/11).
- #506 S2: chiavi d'area C1-C6, H1 su M7-C/M7-H (`@zone …; codice`).
- #507 S4: «Appendice: le terre di Hammerfist, ≈372 DR», 9 pagine. In prosa come Sandpoint (parole in tabella 69% → 16%), 14 PNG con storia e aggancio, mappa schematica M7-R in render_schemi.py. S4 0/3 → 9/3. Abitanti, allineamento, pendio, valichi: proposte INFERRED nell'apparato, in attesa del DM.
- #508 S1: introduzioni di V, VI, VII, VIII, X, XI, XIII con la chiave `apertura` (card di Jfs: solo i capitoli di gioco), messe prima del riquadro «Chi si incontra» (`con_apertura`), misura S1 rifatta. S1 main 2/17 → 9/17.
- Tutte portano MS-0214: chi entra dopo rinumera. #506-#508 toccano gli stessi hb/html della serata.

**In attesa di Jfs (20/11, 12:00).** Card sulle 6 proposte INFERRED dell'appendice (copia di lettura in /mnt/project-files/anteprima-volume-2026-11-19/da-leggere/APPENDICE-CON-PROPOSTE-INFERRED.pdf). Cieco ADR-0093 su 9 coppie (7 introduzioni, apertura e storia dell'appendice) in da-leggere/CONFRONTO-ALLA-CIECA-20-11.md; chiave in chiave-cieco-20-11.json, testi nuovi in riscrittura-20-11/. Solo le nuove scelte entrano in #507/#508. Stile chiesto: introduzioni epiche senza regia, appendice come guida di viaggio (Sandpoint).

**Confronto con gli AP.** I PDF che Jfs ha caricato stanno in /mnt/project-files/uploads/hearth/: 165a89a4… = *Burnt Offerings* (sha 79ac9236, gazetteer pp. 58-71: 11.853 parole, 50 voci di luogo da 171 parole, 45 PNG nel testo; introduzioni delle parti 290-990 parole); dc4571c4… = estratto RHoD (sha 4ef9e4e2; intro Parte I 80 parole); e4a097ac… = statblock RHoD. Jfs vuole che ogni scelta di forma sia misurata contro questi.

**Trappole della misura.**
- `--manifest` misura il PDF già nella cartella e non ricompila: per una modifica si passa il PDF. Compilare con `--all`.
- Giro 2 del 20/11 scelto (8/9; VIII = giro 1 tagliato + box, card) e fatto standard da Jfs: ADR-0147 (proposta, dichiarato nel corpo di #508, non prenotato su main: segnarlo alla piega). In #508 (32f16866: intro con box, note `chiusura` PX generiche, «eroi» mai nomi PG, etichette pilastri tolte in con_apertura, read-aloud-adulti §2-quater + misura_craft --apertura) e #507 (a36ab3d2: apertura e storia a epoche FRCS, 11 nomi PG → 0). Trappole: §2-quater lunga fa sforare test_banco_prosa_locale (32k token); il conto norme sta anche in STATO-E-ORDINE-DEI-PIANI.md (test_verifica_sezione6, niente comando in backtick dopo il numero). Le tabelle in un capitolo galleggiano a fine capitolo: per note brevi, elenchi.
- Le tabelle larghe vanno in testa alla pagina con il titolo di sezione come didascalia: un titolo `##` senza frase d'apertura resta solo in fondo alla colonna.
- Il cricchetto delle note di lavoro (test_misura_standard_tavolo) boccia ogni INFERRED in stampa: le proposte vanno in `<!-- apparato -->`, che l'esportatore toglie.
- I master delle mappe con «generata da compile_map_json.py» si correggono nel JSON, mai nel .md (test_master_generati).
- gate_locale --pre-push non lancia il pytest completo: lanciarlo prima del push.
- Ogni chiave nuova del manifest va nello schema `scripts/schemas/booklet_manifest.schema.json`, o validate_booklets la boccia.

**Why:** Jfs ha chiesto di vedere chiavi, appendici e intro prima di venerdì, poi più profondità misurata contro gli AP.
**How to apply:** [[standard-volume-booklet]] [[equipaggiamento-standard-codex]] [[schede-schema-pf1e-rhod]].
