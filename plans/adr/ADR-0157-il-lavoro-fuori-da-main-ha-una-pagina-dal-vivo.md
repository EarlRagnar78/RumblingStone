# ADR-0157 — Il lavoro fuori da main ha una pagina dal vivo

**Stato**: accettata (2026-11-27, scelta di Jfs su card)
**Data**: 2026-11-27
**Decisione-fonte**: le domande di Jfs del 27/11 nel thread «Rendere visibile il lavoro in corso»: «dove sono i lavori sugli agenti, le prove su FLUX e tutte le parti in sviluppo nei thread? non lo trovo nella documentazione» e «come vedo tutto il lavoro anche lato Claude Code o OpenCode?».
**Rapporti**: affianca [ADR-0087](ADR-0087-la-memoria-del-lavoro-e-generata.md) (`MEMORIA.md`, ciò che è su main) senza toccarla; riusa `plans/contenuti-nei-rami.json` (ADR-0044) per dare un posto ai rami; la routine del lunedì è quella di [ADR-0153](ADR-0153-la-documentazione-segue-la-struttura.md) §3.

## Contesto

Il 27/11 il lavoro in sviluppo stava in cinque posti che nessun documento
collegava: le PR in bozza, i rami `claude/*` senza PR, `plans/contenuti-nei-rami.json`,
le cartelle condivise dei thread cloud in `/mnt/project-files` e i thread di
progetto su claude.ai. `MEMORIA.md` racconta solo ciò che è su main, per
scelta (ADR-0087): è deterministica e la CI la confronta con le sue fonti.
Le prove FLUX del Drappo, per esempio, avevano sei cartelle condivise e nessuna
PR: dal repo non si vedevano.

Il DM lavora anche dal suo PC, con Claude Code CLI o con OpenCode. Lì
`/mnt/project-files` non c'è, e OpenCode legge `AGENTS.md` e
`.opencode/commands/`, non `CLAUDE.md` né `.claude/`.

## Decisione

1. **Un registro curato dei filoni**, `plans/lavoro-in-corso.json`. Un filone
   ha titolo, stato (`in-corso`, `aspetta-jfs`, `in-prova`, `fermo`), thread e
   `thread_id`, PR, rami, cartelle condivise, file del repo, che cosa aspetta,
   il passo dopo e la data dell'ultimo aggiornamento. Si scrive a mano.
2. **Una pagina generata**, `plans/LAVORO-IN-CORSO.md`, da
   `scripts/lavoro_in_corso.py`. Incrocia il registro con le PR aperte (REST
   pubblica di GitHub, token facoltativo), i rami di origin e le cartelle di
   primo livello di `/mnt/project-files` (solo nome, data e primo titolo del
   LEGGIMI). Una PR si attacca a un filone per numero, per ramo o per il
   `thread=cmsg_…` del suo corpo. La pagina elenca ciò che non ha un filone e
   ciò che va aggiornato: PR del registro chiuse, PR ferme da oltre 30 giorni,
   filoni non aggiornati da 14.
3. **In CI entra solo `--check`**, che valida il registro offline. La pagina
   dipende da rete, clone e macchina, quindi non è un cancello.
4. **Lo stesso comando per i due strumenti**: `/lavoro-in-corso` in
   `.claude/commands/` per Claude Code e in `.opencode/commands/` per OpenCode,
   con lo stesso testo. Il rimando sta in `AGENTS.md` accanto a quello di
   `MEMORIA.md`, nel `CLAUDE.md` scritto da `claude-progetto.sh` e nella
   tabella «Dove vive ogni cosa» di `MEMORIA.md` (dalla fonte, `memoria.py`).
5. **La routine del lunedì** lancia `lavoro_in_corso.py --fetch`, attacca a un
   filone o chiude ciò che sta «Senza filone», aggiorna stato e passo dei
   filoni e porta il registro su una PR.
6. **La pagina mostra i canali di ADR-0099**: conteggio per canale e tabella
   dei componenti in testing e unstable, letti dalle tabelle di §2 di
   `PIANO-PIATTAFORMA-DI-SVILUPPO.md` in una funzione sola, che il lotto P1
   sostituirà con `binari.py --canali`; un filone può dichiarare il suo
   `canale` (richiesta di Jfs del 27/11).

## Alternative considerate

- **Allargare `MEMORIA.md` ai rami e alle PR.** Scartata: diventerebbe
  dipendente dalla rete, e ADR-0087 la vuole uguale su ogni macchina.
- **Solo la pagina generata, senza registro.** Elencherebbe PR e cartelle ma
  non direbbe che cosa aspetta Jfs né il passo dopo, che è quello che il DM
  cercava; e le cartelle senza PR, come quelle di FLUX, resterebbero sciolte.
- **Leggere i thread da claude.ai.** Non c'è un'interfaccia dal repo; il
  registro li nomina, e il legame passa dal `thread=` nel corpo delle PR.

## Le conseguenze

La prima pagina vera, del 27/11: 8 filoni; 4 PR aperte senza filone (#543
#537 #519 #459); 3 rami `claude/*` recenti senza PR né posto; 28 cartelle
condivise recenti senza filone su 94. Su main prima non c'era nessuna pagina
del lavoro fuori da main. 25 test in `scripts/tests/test_lavoro_in_corso.py`.

Quello che si paga:

- **Il registro è curato a mano.** Un filone che nessuno aggiorna invecchia;
  la pagina lo segnala dopo 14 giorni, non lo corregge.
- **La pagina invecchia appena scritta.** È un'istantanea: chi la legge
  guarda la data in testa, o la rigenera.
- **Le date delle cartelle sono mtime** del filesystem: una cartella copiata
  di peso sembra recente.
- **Sul PC del DM la cartella condivisa non c'è.** La pagina lo dice, e le
  cartelle elencate vengono dal registro, non da una misura.
- **Il numero di questo ADR non è prenotato su main**: 0150, 0155 e 0156 sono
  presi da PR aperte (#519, #544, #541). Se un'altra PR prende il 0157 prima
  del merge, si rinumera.
