---
name: sincronizzatore-giocato
description: ADR-0149 (#515, su main 550c4402 il 26/11, MS-0232): agente sincronizzatore-giocato e scripts/sincronia_giocato.py S1-S7 che misurano quanto il ramo di gruppo è indietro
metadata:
  type: project
  modified: 2026-11-21T08:30:19.552Z
---

PR #515 in bozza (21/11/2026), ramo claude/project-thread-wh9wu1, base claude/project-thread-o55i68 (#512): si unisce dopo #510 e #512. ADR-0149 non prenotato su main (segnarlo alla piega), voce MS-0216 (collide con i rami aperti: chi entra dopo rinumera).

- `python3 scripts/sincronia_giocato.py --aggiorna --check --scansiona /mnt/project-files`: S1 registro `plans/rami-di-gruppo.json` (vivo campaign-group-rumblingstone, morto -dm-gianfranco); S2 commit di main mancanti; S3 patch del canone ferme; S4 campi aperti; S5 serata non registrata; S6 patch/push (`--ref HEAD`) che chiudono campi senza `[CANONE — DM AAAA-MM-GG, codice]`; S7 `--dopo-merge` righe di main perse.
- Regole dell'agente: una patch di thread non è una decisione di Jfs; merge blocco per blocco (main vince su png e correzioni approvate, il ramo sul giocato); push diretto solo fast-forward; `--yes` vietato. Cancello in instradamento_agenti.py anche su MCP GitHub; workflow sincronia-giocato.yml lunedì 06:30 UTC.
- Catena: sincronizzatore-giocato → custode-canone → autore-documenti. Guida coordinatore aggiornata in /mnt/project-files/agenti-2026-11-20/.

**Why:** il 21/11 il ramo di gruppo era fermo al 12/10 senza che nessuno lo vedesse (misura storica: 1.398 commit, 7 patch ferme).
**How to apply:** dopo ogni serata e prima di ogni preparazione lanciare la misura; i gialli S4/S6 sono domande per Jfs su card. Il 21/11 S6 segnala 19 campi chiusi senza decisione nella patch «Sessioni 5 e 6» del thread ARC-07. Vedi [[ramo-di-gruppo-campagna]] [[vincolo-skill-prosa]] [[verificatori-e-prove-agenti]].

2026-11-26: ramo di gruppo a f8a5f4de0. Debito della Radice di Thorik chiuso con l'opzione A (anima promessa al Sogno, resurrezioni valide, saldabile al Cerchio Sacro col Voto di Hella). Thorik, Tordek e Hella venerano Moradin (detto da Jfs, non scritto nelle schede). Resta S4 su session-4 r.60 (pergamene comprate).

26/11 sera: #515 unita (merge 550c4402, MS-0232) dopo tre giri di custode-canone. Dal secondo giro: S6 accetta solo la marca CANONE (una riga con «DM» e data non basta); S7 vede anche le righe corrette da main rimaste nel merge (conto per file, non per blocco); il cancello ferma --prune, refspec a glob, merge_pull_request e update_pull_request_branch (base/head via gh api, timeout 5 s). Fuori, dichiarati: alias git, eval, gh api -X DELETE.
