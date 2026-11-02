# Giro 4: brief per chi corregge un master

Il DM gioca **stasera** da DEF-4 Scena 5 e vuole i booklet aggiornati dopo un
giro di developer, playtester e DM a freddo, con mappe, PNG, villain e
tattiche allineati. I rilievi sono già scritti: tu li correggi.

Lavori **direttamente nel repo** (la radice del repo, ramo
`claude/project-thread-ep4auu`). Niente git, niente commit, niente push:
li fa chi ti ha avviato. Non tocchi il ramo `campaign-group-rumblingstone`,
`campaign/state.md`, i `.hb.md`/`.html` generati, né i file dell'altro master.

## Da leggere prima (AGENTS.md G1)

- I rilievi del tuo master in `plans/esperimenti/giro4-arc07-2026-10-19/<DEF-N>/`
  (DEVELOPER.md, PLAYTESTER.md, DM.md), più `COERENZA-PNG-MAPPE.md` se c'è.
- Lo stato vero del gruppo: `plans/esperimenti/giro4-arc07-2026-10-19/stato-del-gruppo/`
  (state del ramo di gruppo e log della serata 4). **Il canone del tavolo batte il modulo.**
  In più valgono come canone: il Bane di Aegis Fang contro Fauci
  (+2 a colpire, +3d6, critico ×4, Scosso 1/incontro CD 22) e la patch della Cintura in
  `/mnt/project-files/giro-arc07-2026-10-18/PATCH-STATE-MD.md`.
- `skills/rumblingstone-module-standard/SKILL.md` e `references/sviluppo-degli-incontri.md`;
  per la prosa che il tavolo sente, `skills/rumblingstone-narrative-style/references/read-aloud-adulti.md`
  (§2-ter) e `italiano-nativo.md`; per il testo per il DM, le regole del modulo.
- `skills/rumblingstone-campaign/references/campaign-coherence.md` per ogni fatto che tocchi.

## Cosa correggi

Tutti i 🔴 e 🟠, e i 🟡 che servono stasera al DM (ordine, risorse del gruppo,
regole che si contraddicono, rimandi sbagliati). In questo ordine:

1. **Contraddizioni interne** (due regole per la stessa cosa, conti sbagliati, nomi che
   indicano due cose): scegli quella coerente col canone e col resto del modulo e
   allinea l'altra.
2. **Lo stato del gruppo** dove il modulo lo ignora (volo, risorse comprate, Doni,
   pozioni, pergamene, chi le legge): aggiungi righe per il DM, brevi, nel punto dove servono.
3. **Statistiche mancanti**: solo se esiste una fonte (SRD in `skills/dnd-35-srd/`, una
   scheda di `Bestiario/`, un altro punto del modulo). Cita la fonte accanto.
   **Mai inventare un numero.** Senza fonte, la voce va in
   `plans/esperimenti/giro4-arc07-2026-10-19/DECISIONI-DM.md` (crealo se manca, aggiungi in
   fondo: una riga di domanda, l'opzione che consigli, cosa succede se il DM non decide) e
   nel modulo resta una riga `[INFERRED — needs DM confirmation]` con la proposta.
4. **Bestiario**: se una scheda in `Bestiario/` contraddice il master che il booklet usa,
   allinea la scheda al master (il master è stato verificato sull'SRD nei giri precedenti),
   e annota il cambio.

## Regole che non si violano

- Prosa del tavolo: mai meno dettagli sensoriali, un monologo resta un blocco, i nomi
  noti restano, ≤12 righe per box, niente parentesi nei box. Tocca un box solo se un
  rilievo lo chiede.
- Il cancello, dalla radice del repo (copia prima l'originale in scratchpad per confronto
  non serve: la base è il commit 8a6b1e1):
  ```
  python3 plans/esperimenti/giro4-arc07-2026-10-19/cancello.py "<file>" "<file>"
  ```
  Deve dire `✓ passa`. Un «fatto cambiato» in un box è ammesso solo se è la correzione di un
  rilievo: scrivilo nella nota.
- Poi: `python3 scripts/validate_modules.py`, `python3 scripts/copertura_scene.py --check`,
  `python3 scripts/domande_developer.py --check`, `python3 scripts/ciclo_prosa.py segnala <file>`
  (nessuna segnalazione in più rispetto alla base).

## Cosa consegni

- I file corretti nel repo.
- `plans/esperimenti/giro4-arc07-2026-10-19/<DEF-N>/CORREZIONI.md`: per ogni rilievo una
  riga (corretto come / lasciato e perché / mandato al DM), poi l'output del cancello.
- Nella risposta: i conteggi corretti/lasciati/al DM, e le decisioni DM aperte, in
  italiano, onesto.
