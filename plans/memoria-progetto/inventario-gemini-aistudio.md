---
name: inventario-gemini-aistudio
description: Inventario dei contenuti di Gemini/AI Studio su Drive contro il repo (PR #284, 2026-10-23): cosa manca, cosa non si è potuto guardare
metadata:
  type: project
  modified: 2026-11-08T14:56:10.206Z
---

PR #284 unita su main il 2026-10-23 (dcd403e9): plans/INVENTARIO-GEMINI-AISTUDIO-2026-10.md, D1-D6 al DM (in STATO §4).
Cartella Drive «Google AI Studio» (id 1sBs0cKM-GJv5y1Vuqd7qiopoLrs7gxLk): 182 file, ~45 della campagna; i file restano su Drive, mai nel repo.
Mancano: battle_stats_maps.md, mini-boss Krusk/Vreek/Ur-Vrax e patrono Tiamat, «Manuale da campo del DM», doc «Red Hand of Doom 3.5 Conversion».
Non guardati: chat dell'app Gemini (non su Drive, servono esportate), 10 chat con immagini >10 MB (il connettore Drive non le scarica), 7 chat piccole, RedHandOfDoom.zip.
Card del 2026-11-08 (Jfs): D1 tutto in ARC-08 convertito, D3 dentro S1 voce per voce, D4 confronto e vince la più forte, D5 il doc Conversion fa da controllo dei numeri di ARC-09, D6 «Esporto io, poi secondo giro», D2 mini-boss Krusk/Vreek/Ur-Vrax nel Bestiario (Tiamat già canone). BOX-LUOGO D2: resta ADR-0014 (misure non obbligate nella prima frase). BOX-LUOGO D3: ogni box dichiara il tipo ovunque, solo l'etichetta. BOX-LUOGO D4: i box già giocati oltre le misure non si toccano, con l'eccezione scritta. BOX-LUOGO D5: l'Abbazia ha un box di luogo breve per ogni stanza. BOX-LUOGO D6: template d'area in due versioni, 3.5 e PF1e. CODA D2: correggere extract_scene_prompts.py (etichette regia troncate da parentesi annidate), con test. CODA D3: d eufonica diventa norma misurata. RIPRESA D2: collaudo Drappo con FLUX.2 klein 4B (D2 resta aperta fino al confronto). RIPRESA D11: Jfs prima «in attesa», poi la consigliata: perimetro ADR-0049 con Bestiario dentro, lotto 2.1 VENDIBILITA sotto 1,0 RHoD/1000 parole senza togliere creature. CODA D2 attuata (extract_scene_prompts). Tutto nella PR #346, unita su main il 2026-11-08 (b6e9324, squash). Lotti nati (mini-boss, confronto statblocchi, template d area, d eufonica, pulizia Bestiario) nella roadmap del thread regolamenti plugin, che ora tiene i merge.
PR #349 unita il 2026-11-08: ripiego pyyaml in compress-skill misurato (18/18 uguale, ma 17 altri script importano yaml e PyYAML ha wheel cp313 ovunque) e non fatto. MASTER-DEF D6 = orda più forte (PR #347). Card 2026-11-09 «Chiudi, superato»: fallback chiuso come superato (prova requirements.txt:28, script solo di build), PR #357 unita; le altre voci di RECUPERO D5 restano ⬜ con condizione, D5 aperta.
**How to apply:** un secondo giro solo se Jfs esporta le chat Gemini o mette i file grandi in /mnt/project-files/. Le chat AI Studio sono JSON (chunkedPrompt.chunks, saltare isThought).
