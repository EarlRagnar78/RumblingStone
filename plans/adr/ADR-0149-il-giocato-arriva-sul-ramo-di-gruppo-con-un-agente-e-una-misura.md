# ADR-0149 — Il giocato arriva sul ramo di gruppo con un agente e una misura

**Stato**: proposta (2026-11-21)
**Data**: 2026-11-21
**Decisione-fonte**: il DM (Jfs), 2026-11-21. Nel thread «Preparare i booklet di ARC-07» sceglie il push diretto sul ramo di gruppo («spingi direttamente su campaign-group-rumblingstone … così quando fa pull ha tutto»), scelta passata dal coordinatore. L'agente e la misura sono la proposta del thread che ha scoperto il ritardo del ramo, e li accetta o li respinge il DM su questa PR.
**Rapporti**: applica [ADR-0007](ADR-0007-scritture-canone-triplo-vincolo.md) (il canone vivo si scrive solo su un ramo di gruppo) e [ADR-0090](ADR-0090-la-partita-riparte-su-un-ramo-di-gruppo-nuovo.md) (il ramo vivo, quello morto, main che entra con un merge prima di ogni preparazione); aggiunge un agente alla classe Tecnici di [ADR-0146](ADR-0146-le-skill-di-prosa-si-caricano-per-vincolo.md) e i suoi casi di prova nella forma di [ADR-0148](ADR-0148-i-fatti-si-verificano-con-script-e-gli-agenti-con-prove-fisse.md).

## Contesto

Il 21/11/2026 si è scoperto che `campaign-group-rumblingstone`, il ramo vivo
del primo tavolo, era fermo al 12/10 (`ce345991`, sessione 4), mentre la
memoria del lavoro lo dava «fermo al 25/09». Il primo conto del mattino
diceva 1.387 commit di main mancanti e quattro patch del giocato ferme dal
05/11 nella cartella del progetto. Nessuno strumento guardava il ramo: ADR-0090
dice che main entra prima di ogni preparazione, ma è una regola che si ricorda,
e per sei settimane nessuno l'ha ricordata.

La misura storica, ricostruita su `ce345991` con l'ora fissata al 21/11 alle
06:00, dà esito 1 con tre rossi:

- S2: 1.398 commit di main mancanti, il più vecchio da 41 giorni;
- S3: sette patch ferme, fra 381 e 955 ore;
- S5: la serata del 20/11 non registrata.

Lo script di questo ADR, se ci fosse stato, l'avrebbe segnalato al primo
lunedì.

Lo stesso giorno il thread «Preparare i booklet di ARC-07» ha spinto a mano
sul ramo, con il push diretto scelto da Jfs. La prima revisione di
`custode-canone` ha trovato tre errori gravi nel modo in cui il giocato era
arrivato e nel disegno della prima versione:

- le patch dei thread erano state prese per decisioni del DM: quella delle
  sessioni 5 e 6 «ricostruiva» chi era presente e chiudeva campi che solo Jfs
  può chiudere;
- la regola di merge «tieni il ramo» perdeva correzioni legittime arrivate su
  main, come `eba5fee00` (Tempestas GS 15), `870c27af3` (la CAR di Thorik) e
  `c4956fff3` (PG e schede);
- il cancello del push si aggirava con `HEAD`, con `git -C`, dentro `sh -c` e
  con gli strumenti MCP di GitHub.

Le sei osservazioni minori riguardavano il conteggio dei campi aperti (righe
invece di occorrenze, intestazioni contate) e la forma della marca INFERRED.

## Alternative considerate

| Opzione | Scartata perché |
|---|---|
| Una riga in più nel Playbook e in MEMORIA.md | è la regola che c'era già in ADR-0090 e che nessuno ha ricordato per sei settimane |
| Affidare il lavoro a `integratore-dm` o a `custode-canone` | il primo tiene il motore di `dm.py`, il secondo lavora in sola lettura e deve poter controllare chi scrive; dare a uno dei due anche la scrittura del giocato mescola chi fa e chi verifica |
| Un job nel `ci.yml` | `ci.yml` non ha un trigger `schedule`, e aggiungerlo farebbe girare di lunedì tutti i suoi job; un job sulle PR, poi, bloccherebbe lavoro che con il ramo di gruppo non c'entra |
| Rebase del ramo su main | riscrive la storia del canone, che ADR-0007 vuole intatta, e costringe a un push forzato |
| Merge con `git checkout --ours` sui file di partita | è la regola «tieni il ramo» della prima versione: perde le correzioni approvate su main |
| PR verso il ramo di gruppo invece del push diretto | Jfs ha scelto il push diretto il 21/11; la protezione si sposta sul fast-forward e sulle misure prima del push |

## Decisione

1. **Un agente con un solo compito.** `.claude/agents/sincronizzatore-giocato.md`,
   classe Tecnici, precarica `rumblingstone-automation` e
   `rumblingstone-campaign`. Porta sul ramo di gruppo vivo quello che il tavolo
   ha giocato e il DM ha deciso, fa entrare main con un merge e misura prima e
   dopo. Non scrive su main, non scrive prosa, non avvia altri agenti. La
   catena del thread è `sincronizzatore-giocato`, poi `custode-canone`, poi
   `autore-documenti`; `instradamento_agenti.py` la propone quando il messaggio
   parla del giocato, del ramo di gruppo o di patch ferme, e sulle 44 frasi di
   `casi.json` le scelte degli altri agenti restano identiche.
2. **Occhi deterministici.** `scripts/sincronia_giocato.py` misura senza
   scrivere niente (nessun checkout, nessun commit, nessun indice toccato).
   Ogni rilievo ha codice, livello, ramo e il comando che lo risolve:
   - S1, i rami `campaign-group-*` del remoto che non sono nel registro
     `plans/rami-di-gruppo.json`, né vivi né morti (giallo);
   - S2, i commit di main che mancano al ramo vivo e da quanti giorni aspetta
     il più vecchio (rosso oltre 14 giorni, giallo con un commit solo); un clone
     shallow dà «non misurabile» con il comando per rimediare, mai un numero
     sbagliato;
   - S3, le patch del canone ferme nelle cartelle scansionate, provate con un
     indice temporaneo (rosso se da applicare e più vecchie di 48 ore);
   - S4, i campi aperti al DM nelle sessioni e in `state.yaml`, contati per
     occorrenza con i criteri di `inventory_inferred.py` (sempre giallo: sono
     domande);
   - S5, una serata delle patch più recente dell'ultima sessione registrata
     (rosso);
   - S6, una patch, o con `--ref` il diff da spingere, che fa scendere i campi
     aperti senza la decisione datata del DM (giallo sulla patch, rosso sul
     push);
   - S7, con `--dopo-merge`, ogni riga che main ha aggiunto ai file di partita
     deve esserci nel risultato del merge, e ogni riga che main ha tolto (una
     correzione, come Tempestas da GS 14 a GS 15) non deve restarci, salvo che
     il ramo l'abbia aggiunta da sé.

   Esce 1 con almeno un rosso, 2 se qualcosa non si misura, 0 altrimenti.
3. **L'avviso arriva da solo.** Quando il prompt parla del giocato o del ramo
   di gruppo, l'hook di `instradamento_agenti.py` aggiunge al contesto l'esito
   breve di `sincronia_giocato.py --avviso`. Un errore o un ritardo dello
   script non fermano il lavoro.
4. **Il cancello del canone.** Il `PreToolUse` di `instradamento_agenti.py`,
   anche dentro un sottoagente, ferma un push che forza o cancella un ramo
   `campaign-group-*` (`--force`, `-f`, `--force-with-lease`, un refspec con
   «+», `--delete`, `--mirror`, `--prune`, un refspec a glob, `--all` o `--tags`
   forzati), un push di canone
   su main (anche `HEAD:main` dal ramo di gruppo, o un `git add` di file di
   partita nello stesso comando) e qualunque push verso un ramo morto. Legge il
   push dopo le opzioni globali di git e dentro `sh -c` e `bash -c`; `HEAD` e il
   push senza refspec valgono il ramo corrente della cartella. Il matcher in
   `.claude/settings.json` comprende ora gli strumenti MCP di GitHub che
   scrivono (`push_files`, `create_or_update_file`, `delete_file`,
   `create_branch`): non portano canone su main e non toccano i rami morti.
   Comprende anche `merge_pull_request` e `update_pull_request_branch`: base e
   head della PR si leggono con `gh api`, e se non si leggono lo strumento si
   ferma.
   `campaign_branch.py guard` rifiuta un ramo morto del registro.
5. **Il workflow del lunedì.** `.github/workflows/sincronia-giocato.yml` gira
   ogni lunedì alle 06:30 UTC, prima della routine delle 06:47, con le regole
   che bastano a git (S1, S2, S4, S5). Non gira sulle PR e non le blocca. Le
   patch ferme (S3) stanno nella cartella del progetto, che in CI non c'è: le
   guarda l'agente con `--scansiona`.
6. **Il canone resta di Jfs.** Una patch preparata da un thread non è una
   decisione del DM. Una riga che chiude un campo aperto (PX, bottino, esito di
   una prova, chi era presente, prezzo di un patto) deve citare la decisione
   con la data, con la marca
   `[CANONE — DM AAAA-MM-GG, <codice>]` di `docs/reference/GUIDA-MARCATURE.md`:
   S6 accetta «DM» o «Jfs» entro sessanta caratteri da una data ISO, prima o
   dopo. Senza, la patch resta ferma e diventa una
   domanda per il coordinatore, che la porta a Jfs su card. L'agente non
   sceglie mai un esito, nemmeno «il più probabile». La norma entra nel
   registro delle norme, misurata da S4 e S6.
7. **Il merge si risolve blocco per blocco.** Mai `checkout --ours` o
   `--theirs` su un file intero. Nella sezione `png` di `state.yaml` e nelle
   correzioni di canone approvate su main vince main; nei record del giocato
   (sessioni, stato dei PG dopo una serata, echi) vince il ramo; lo stesso
   record cambiato dalle due parti va al DM, senza scegliere. Dopo il merge
   girano `sincronia_giocato.py --dopo-merge`, `validate_state.py`,
   `render_state.py --check` e `dm.py doctor`; se uno fallisce non si spinge.
8. **Push diretto, solo fast-forward.** È la scelta di Jfs del 21/11, e vale
   per il modo di spingere, non per il contenuto. Prima del push
   `sincronia_giocato.py --ref HEAD --check`; se il remoto è avanti,
   `git pull --no-rebase` e di nuovo i controlli. `dm.py session end --yes` è
   vietato all'agente: ADR-0007 lo riserva ai test e alla CI. Il residuo che il
   wizard non copre va a mano in `state.yaml` solo dopo una card del DM.

## Le conseguenze

- Il ritardo del ramo ha un numero ogni lunedì e a ogni prompt che parla del
  giocato. Sul ramo vivo `8b3441e5f`, dopo le correzioni, l'esito è 0 con
  quattro gialli: S2, 18 commit di main mancanti; S6, la patch «Sessioni 5 e
  6» chiude 27 campi e 19 non citano una decisione datata del DM; S6, la patch
  «Sessione 7 risposte del DM» ne chiude 5 e 3 sono senza decisione; S4, 10
  campi aperti. La prova di merge di main in un clone temporaneo è pulita, e
  `--dopo-merge` non trova righe perse.
- I 19 e i 3 campi chiusi senza decisione sono domande per Jfs, non errori da
  correggere: restano gialli finché lui non decide.
- L'agente ha cinque casi di prova in `.claude/agent-evals/sincronizzatore-giocato/`
  (il conflitto in `state.yaml`, Tempestas GS 15 che arriva da main, la patch
  che chiude i campi, il campo dei PX vuoto, il ramo morto). Il conto di
  ADR-0148 passa da 36 casi per 12 agenti a 41 per 13.
- La suite dei test dà 3.519 passati, 17 saltati e 1 fallito prima di questo
  ADR: `test_verifica_sezione6::test_oggi_e_verde`, perché la norma nuova porta
  il registro a 100 norme e §6.2 di `STATO-E-ORDINE-DEI-PIANI.md` ne attendeva
  99. Lo stesso commit di questo ADR aggiorna l'attesa.

**Quello che si paga.**

- **Il cancello è una rete, non una gabbia.** Un push a main dopo un commit di
  canone fatto in un'altra chiamata non si vede, perché il cancello legge un
  comando alla volta. Uno script scritto su file e poi eseguito, un alias di
  git o un client diverso da `git` e dagli strumenti MCP elencati passano.
  Fuori da Claude Code il cancello non c'è: resta la protezione del remoto, se
  il DM la attiva.
- **S7 è testuale.** Confronta righe aggiunte, non record: una riga di main
  riscritta nel merge con un altro spazio o un altro ordine dei campi conta
  come persa, e una riga presente ma nel record sbagliato conta come salva.
- **La decisione del DM si riconosce solo dalla marca.** S6 vuole
  `[CANONE — DM AAAA-MM-GG, codice]` (il codice è facoltativo), la forma della
  guida delle marcature. Nominare il DM e una data non basta più: il secondo
  giro del `custode-canone` (2026-11-26) ha mostrato che «proposta del thread,
  da mostrare al DM, 2026-11-21» passava. Una decisione vera scritta in
  un'altra forma risulta mancante; una marca scritta senza che il DM abbia
  deciso passa. Lo script vede la forma, non la verità.
- **S7 conta le righe per file, non per blocco.** Una riga ripetuta che il
  ramo ha in più copie può coprirne una persa; il blocco per blocco resta
  all'agente e al DM.
- **Il cancello non legge gli aggiramenti voluti:** un alias di git
  (`git -c alias.x=push`), `eval` e `gh api -X DELETE …/git/refs/…`.
- **L'età di una patch viene dal `mtime` del file.** Una copia o un
  salvataggio sul mount di rete la ringiovanisce, e S3 può dare giallo dove il
  rosso era dovuto.
- **Le A/B dei casi non sono state eseguite.** I cinque casi hanno le due
  esecuzioni fisse, buona e cattiva, che `prove_skill.py esempi` controlla; un
  esito con l'agente vero non c'è ancora in `.claude/agent-evals/ESITI.jsonl`.
- **L'agente entra in testing**, come chiede la proposta della #510: l'hook lo
  suggerisce, ma nessun cancello pretende che il giocato passi da lui. Diventa
  stable dopo 14 giorni e 10 thread in cui è stato chiamato, senza trappole
  cadute.
- **La verifica dopo le correzioni non è stata ripetuta.** `custode-canone`
  lavora in sola lettura e ha rivisto il primo giro; sui tre rossi e sulle sei
  osservazioni corretti dopo non ha rilanciato la sua revisione. Le correzioni
  hanno i loro test, ma lo sguardo di chi controlla il canone su di esse manca.
- L'agente esiste solo dopo il merge della #510, della #512 e della PR di
  questo ADR.

**Da rivedere se**: il DM sceglie di proteggere il ramo di gruppo sul remoto
(allora il cancello locale diventa una seconda rete e il push diretto può
passare da PR); un secondo gruppo apre il suo ramo vivo (il registro e il
workflow vanno provati con due rami); S6 trova decisioni vere scritte in altra
forma (allora la grammatica va in `docs/reference/GUIDA-MARCATURE.md` e lo
script la legge da lì); dopo 14 giorni l'agente non è stato chiamato in nessun
thread dopo una serata.
