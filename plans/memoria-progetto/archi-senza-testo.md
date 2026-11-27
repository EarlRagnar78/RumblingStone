---
name: archi-senza-testo
description: Censimento dei file non markdown degli archi 00-10 (PR #287), D1-D12 decise dal DM il 2026-10-23/24 (PR #290), testi altrui in _testi-altrui/
metadata:
  type: project
  modified: 2026-10-23T19:41:55.277Z
---

PR #287 unita su main il 2026-10-23 (c4e5a70d, thread «Archi senza testo nel repo»): plans/RICERCA-ARCHI-SENZA-TESTO-2026-10.md + 05_aa-stanza-runica/ARC05-STANZA-RUNICA-TRASCRIZIONE.md. STATO §0: P28 🟡 (aspetta D1-D6), P30 ⬜ (P30-a schede Bestiario mancanti: Orrore Palustre, Zanna, Grell Patriarca, chierica di Lolth, Antenato Nanico).
06, 07, 10 senza perdite; 01 e parte di 03 sono trascrizioni WotC da non convertire (D12).
La trascrizione arco 05 è in FUORI_RAGGIO di test_png_archi_nel_bestiario.py finché D1-D6 aperte; i read-aloud sono paragrafi e non box per non spostare misura_craft --p1 (§6.2, «20 box su 544»).
La #282 (ramo claude/indice-triage-chat) ha tolto la sua vecchia riga P28: vale quella della #287.
Merge: lo fa il thread padre, vedi [[thread-padre-pr]].

2026-10-24: D1-D12 decise da Jfs, una card per voce; tutte sulla proposta salvo D6 = numeri più duri (coerente con [[scelte-inferred-versione-piu-forte]]), D8 = appunti d'apertura tutti giocati, D12 cambiata in «convertili anche, poi si cerca una soluzione» → 16 md in */_testi-altrui/ (archi 00, 01, 03), esclusi da validate_lingua e build_monster_catalog. Dove tenerli: da decidere prima che il repo diventi pubblico. PR #290 unita su main il 2026-10-24 (b1500ca1) applica tutto: cronaca archi 00-05 (8° livello, Thorek I, gemma-chiave, chierico di Abbathor GS 11, retriever su commissione di Abbathor, EL 14 al tempio), P28 chiuso, P30 resta su P30-a. Scelte grezze in /mnt/project-files/archi-senza-testo/SCELTE-DM.txt.
**How to apply:** per D-domande di Jfs: una card per voce con la proposta più forte come consigliata; il merge lo fa sempre il thread padre.
