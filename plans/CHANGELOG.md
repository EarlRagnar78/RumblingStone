# 📜 CHANGELOG DEI PIANI

> Una riga per **lotto chiuso** (`data · piano · lotto · riferimento ·
> esito`). La riga si aggiunge **nello stesso commit** che chiude il lotto
> (Lotto K-A3 del piano DM-TOOLKIT). Le righe 2026-07-02→07-04 sono
> **seminate retroattivamente** dalle checklist dei piani e dai merge PR
> (#13-#25) — il dettaglio task-per-task vive nelle checklist dei piani e,
> per il canone, in `campaign/state.md` §8.

| Data | Piano | Lotto | Riferimento | Esito |
|---|---|---|---|---|
| 2026-07-02 | REVISIONE-ARC09 | Lotto A (A1-A13) | PR #13-#14 | ✅ incoerenze di canone chiuse (global-replace nomi, clock, orfani sotto-quest) |
| 2026-07-02 | REVISIONE-ARC09 | Lotto B (B1-B7) | PR #15 | ✅ contenuti sotto-standard completati (Rhest, handouts, WBL audit, errata 3.5) |
| 2026-07-02 | REVISIONE-ARC09 | Lotto C (C1-C7) | PR #15-#16 | ✅ meccanismi "magnifica" (event deck battaglia finale incluso) — **PIANO COMPLETO** |
| 2026-07-02 | REVISIONE-ARC07 | Lotto A (A1-A11) | PR #18 | ✅ canone e igiene file (Skullcrusher/1.000 anni propagato, matrice versioni, indice) |
| 2026-07-02 | REVISIONE-ARC07 | Lotto B (B1-B9) | PR #18 | 🟡 B1 parziale (log ricostruiti; mancano date/XP/loot reali); B2-B9 ✅ |
| 2026-07-02 | REVISIONE-ARC07 | Lotto C (C1-C3) | PR #18 | ✅ atlante asset, handouts, conseguenze/echi |
| 2026-07-02 | REVISIONE-ARC08 | Lotto A (A0-A12) | PR #17, #19 | ✅ REGOLA ZERO applicata (state.md al giocato reale) + igiene file |
| 2026-07-02 | REVISIONE-ARC08 | Lotto B (B1-B7) | PR #19 | ✅ ponte ARC07→08 (cucitura D16), contenuti di gioco completi |
| 2026-07-02 | REVISIONE-ARC08 | Lotto C (C1-C4) | PR #19 | ✅ da "coerente" a "memorabile" — **PIANO COMPLETO** |
| 2026-07-03 | REVISIONE-ARC07 | Validazione DM | state.md §8 | ✅ D1-D17 sciolte; A12 eredità Skullcrusher→Fauci |
| 2026-07-03 | TRASVERSALE | Lotto T-A (T1-T4) | PR #24 | ✅ fondazioni: ramo del rifiuto P3B, render_map_svg.py, template companion, matrice artefatti |
| 2026-07-03 | TRASVERSALE | T5a (censimento+rendering) | PR #24 | ✅ MAPPE-CENSIMENTO.md + SVG di massa |
| 2026-07-03/04 | TRASVERSALE | T5b+T5c (companion mappe) | PR #24-#25 | ✅ LOTTO MAPPE COMPLETO (16 companion ARC-09, griglia Campo Drow 2) |
| 2026-07-03/04 | TRASVERSALE | T6a+T6b+T6c (artefatti) | PR #24-#25, #26 | ✅ LOTTO ARTEFATTI COMPLETO (regola 3 documenti; §6 doppia colonna, T-D10) |
| 2026-07-04 | TRASVERSALE | T7+T9 (schede giocatore, echi) | PR #25 | ✅ schede STATO-ATTUALE per tutti; T9 cross-link (chiusura post-P3B gated) |
| 2026-07-10 | DM-TOOLKIT | Piano scritto e approvato | PR #28 | ✅ decisioni K-D1…K-D4; esecuzione autorizzata dal merge |
| 2026-07-10 | DM-TOOLKIT | Lotto K-A (K-A1…K-A4) | 0070a49 | ✅ archivio `plans/` + puntatori, INDEX con %, questo changelog, 3 ADR + template |
| 2026-07-10 | DM-TOOLKIT | Lotto K-C1 (dm.py) | 618ae7b | ✅ CLI unica `scripts/dm.py` (prep/maps/post/recap/handout/skills/doctor), solo orchestrazione (ADR-0002) |
| 2026-07-10 | DM-TOOLKIT | Lotto K-B1 (recap-hype) | 810f9a7 | ✅ `scripts/hype_homebrew.py`: recap → Homebrewery V3 (copertina, note, paginazione euristica, guardia anti-DM-notes); esemplare `campaign/recaps/homebrew/recap-2026-05-05.hb.md` |
| 2026-07-10 | DM-TOOLKIT | Lotto K-B2 (handout) | 15173e0 | ✅ 4 template V3 in `campaign/templates/homebrew/` + `--sezione`/anti-regia-DM in hype_homebrew.py; 2 piloti da canone (profezia Cronache Quattro Eroi, scheda Collana); piloti lettera/avviso-torneo gated su testo canone DM |
| 2026-07-10 | DM-TOOLKIT | Lotto K-C2 (docs) | 7664d87 | ✅ README-automation attorno a dm.py, Playbook §2/§4/§4.6 aggiornati, AGENTS.md (plans/, dm.py, .hb.md), banner SUPERATO su scripts/Old, disambiguazione Script/ vs scripts/ |
| 2026-07-10 | DM-TOOLKIT | Lotto K-C3 (CI) | f01f311 | ✅ smoke test in ci.yml: dm.py --help, dm.py doctor --ci, hype_homebrew.py --help |
| 2026-07-12 | DM-TOOLKIT | Lotto K-B4 (self-host) | 875fef1 | ✅ Homebrewery self-hosted: guida con comandi ufficiali (README + README.DOCKER di naturalcrit), setup.sh/start.sh, `dm.py hype setup\|start`, ADR-0004; chiude Q2 (K-D5) |
| 2026-07-12 | DM-TOOLKIT | Lotto K-B5 (container) | b9f3b25 | ✅ Docker chiavi-in-mano: compose ufficiale naturalcrit (mongodb+app), setup-docker.sh/stop-docker.sh, `dm.py hype docker\|docker-stop`, guida "da zero al container" |
| 2026-07-12 | DM-TOOLKIT | Lotto K-B3.1 (booklet Fascicolo I) | cb74328 | ✅ `07_.../homebrew/ARC07-BOOKLET-FASCICOLO-1-P1-P2.hb.md` in stile AP: copertina, crediti, background G0, sinossi D2/D16, capitoli P1-P2 con read-aloud e tabelle scena→master (cita, non riscrive); prossimi fascicoli II-V (P3, P4, P3B, P5-P6) |
| 2026-07-12 | DM-TOOLKIT | Lotti K-B3.2-.5 (Fascicoli II-V) | 2c0d1aa…312b8e5 | ✅ **BOOKLET ARC-07 COMPLETO** (I-V): Fuoco, Terra+Viaggio, Resurrezione P3B, Mille Anni+ponte B4/D16 — stile AP, citano i master, zero numeri nuovi |
| 2026-07-12 | DM-TOOLKIT | K-B0 + chiusura | 21a006b | ✅ **PIANO COMPLETO (100%)**: K-B0 chiuso col default dichiarato (snippet V3 nativi — sito pack inaccessibile, mandato DM "completa tutto"); code da tavolo: verifica visiva brew + piloti lettera/avviso-torneo su testo canone |
| 2026-07-12 | DM-TOOLKIT | Lotto K-B6 (feedback collaudo DM) | 9f8fabf | ✅ Recap player-safe v2: clock/villain → voci vaghe con Conoscenze locali (mai numeri/deadline), tabella archi = solo cammino vissuto (futuri → sussurri §V), calendario di Marcia/Harptos in testata + `00-CRONOLOGIA.hb.md` auto-generata; fix glob sessioni (esclusi file non-log tipo RETROATTIVI) |
| 2026-07-12 | DM-TOOLKIT | Lotto K-B7 (dossier DM + ancora Harptos) | 7654e1b | ✅ `scripts/dm_dossier.py` + `dm.py dossier`: fotografia di state.md (§0-§7) in Homebrewery V3 con cornici stile RHoD, banner SOLO DM; ancora Harptos = 1 Mirtul 1372 [INFERRED: coerente con state.md §0; house-rules "Flamerule" da riconciliare] → date piene ovunque |
| 2026-07-12 | DM-TOOLKIT | Lotto K-B8 (calendario estivo) | questo commit | ✅ Ancora Harptos CONFERMATA dal DM: piena estate nella Valle di Channath → Giorno 1 = **1 Flamerule 1372** (Day 19 = 19 Flamerule; Rethmar Day 42 = 11 Eleasis); state.md In-world date corretta con changelog §8; [INFERRED] di K-B7 risolto; esemplari rigenerati |
| 2026-07-12/16 | RICERCA-MAPPE | ricerca + attuazione completa (4 round) | PR #40 | ✅ **PIPELINE MAPPE QUALITÀ AP COMPLETA**: renderer "pergamena" (terreni organici, AO, ~45 prop originali, griglia leggibile, ⛰ terreno) + 16 SVG rigenerati; `import_watabou.py` (JSON 1PD → griglia emoji); `export_map_png.py` (PNG hi-res, gitignored); skill `rumblingstone-mapmaking` (workflow + legenda universale + guida hero-map ComfyUI opzionale) |
