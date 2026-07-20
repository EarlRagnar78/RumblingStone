# ADR-0008 — Governance del set di skill: focalizzate per dominio, copertura obbligatoria, router legacy come shim

**Stato**: accettata
**Data**: 2026-07-20
**Decisione-fonte**: audit skill vs PR #48-#55 (PR #56), richiesto dal DM

## Contesto

Il repo è passato da una skill monolitica (`dnd-35-rules`, ~60K token) a
skill focalizzate per dominio, ma senza una regola scritta su *quando* una
skill nasce, si aggiorna o muore. Risultato osservato nell'audit: il piano
AUTOMAZIONE-STATO-SESSIONI era implementato (PR #53/#54, ADR-0007) senza
alcuna copertura skill — un agente poteva scrivere canone a mano ignorando
il triplo vincolo; nel frattempo docs e lore citavano ancora percorsi
`skills/dnd-35-rules/references/*` inesistenti da mesi.

## Decisione

Il set di skill segue tre regole:

1. **Una skill per dominio, sottile dove possibile.** Le skill operative
   (automation, mapmaking, plans) *puntano* alle fonti di verità del repo
   (README, ADR, guide) invece di duplicarle; le skill di riferimento
   (SRD, lore, campaign) contengono il materiale. Confini espliciti tra
   skill dichiarati nel SKILL.md.
2. **Copertura obbligatoria**: quando un piano infrastrutturale introduce
   un flusso che un agente dovrà usare (CLI, pipeline, vincoli di
   scrittura), la skill che lo copre nasce o si aggiorna **nello stesso
   piano** — la copertura skill è un criterio di completamento del lotto,
   non un follow-up.
3. **Il router `dnd-35-rules` è uno shim in deprecazione.** Nessun
   documento nuovo lo referenzia; instrada tutte le skill focalizzate; si
   elimina il giorno in cui niente nel repo (e nessuna configurazione
   agent supportata) lo cita ancora. La condizione è misurabile con
   `grep -rl dnd-35-rules` fuori da `skills/dnd-35-rules/`.

## Conseguenze

- Gli agenti trovano sempre il flusso giusto (niente più «aggiorno
  state.md a mano» perché nessuna skill diceva altrimenti).
- Ogni nuova infrastruttura costa una voce di manutenzione skill in più —
  accettato: è il prezzo perché resti usabile dagli agenti.
- I puntatori incrociati (AGENTS.md, lore, README) vanno tenuti allineati:
  `validate_skills.py` copre i link nelle skill; il resto è a carico della
  revisione PR (vedi ADR-0009 per il gate di tracciatura).
- Da rivisitare: quando il router legacy non è più citato da nessun file,
  rimuoverlo e chiudere questo ADR con «superata».
