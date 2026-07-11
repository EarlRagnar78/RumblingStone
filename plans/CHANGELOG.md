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
| 2026-07-10 | DM-TOOLKIT | Lotto K-C3 (CI) | questo commit | ✅ smoke test in ci.yml: dm.py --help, dm.py doctor --ci, hype_homebrew.py --help |
