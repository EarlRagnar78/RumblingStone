# ADR-0142 — `.claudeignore` diventa regole `Read` di `permissions.deny`

**Stato**: accettata (2026-11-19)
**Data**: 2026-11-19
**Decisione-fonte**: il DM (Jfs), 2026-11-19: «farle tutte in ordine con PR separate misurando per ognuna il miglioramento», dopo la card sulla pratica successiva alle regole a percorso (consigliata e prima in ordine: «Regole deny dal .claudeignore»).
**Rapporti**: completa [ADR-0140](ADR-0140-la-configurazione-claude-del-repo-arriva-anche-nei-thread.md) e [ADR-0141](ADR-0141-le-regole-di-agents-arrivano-con-i-file.md). Guida al ritorno indietro: [`docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md`](../../docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md).

## Contesto

Il repo ha un `.claudeignore` dal 14/11 (86 voci, sintassi `.gitignore`) per
togliere dal contesto dell'agente i file generati, vendorizzati e binari.
Provato il 2026-11-19 in una cartella di prova: **Claude Code non lo legge**,
un file elencato lì si apre con Read. Il meccanismo documentato è
`permissions.deny` con regole `Read(...)`; provato nella stessa sessione, blocca
Read, Grep e Glob.

Le voci coprono 165 file di testo tracciati da git (68 MB: SVG renderizzati,
HTML e Typst di homebrew, pacchetti vendorizzati). Grep rispetta già
`.gitignore`, non `.claudeignore`, quindi nelle ricerche quei file entrano.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Script che ricava le regole da `.claudeignore`, con `--check` in un test** (scelta) | una fonte sola, scritta in sintassi `.gitignore`; deterministico | le regole sono una copia generata dentro `settings.json` |
| Scrivere le regole a mano e cancellare `.claudeignore` | niente script | si perde la sintassi che altri strumenti capiscono; la lista si sposta in JSON |
| Lasciare com'è | niente da fare | il file promette qualcosa che non succede |

## Decisione

1. **`scripts/claudeignore_deny.py`** traduce ogni voce in una regola `Read`:
   una voce con una barra prima della fine è ancorata alla radice del
   progetto (`Read(/x)`), una senza vale a ogni livello (`Read(**/x)`), una
   cartella diventa `x/**`. Le negazioni (`!x`) fermano lo script, perché
   `deny` non ne ha.
2. **Restano leggibili sedici voci**, marcate in `.claudeignore` con un
   commento `# leggibile: motivo` sopra di loro (la marca vale fino alla
   prima riga vuota o al primo altro commento, e il motivo è obbligatorio):
   le immagini e i PDF, che l'agente apre apposta e che Grep salta da solo;
   gli specchi `.claude/skills/`, da cui si leggono i `references/`;
   `.claude/.skills-sync-status`, che AGENTS.md chiede di leggere.
3. **Nei thread** `claude-progetto.sh` mette il nome del repo davanti alle
   regole ancorate (`Read(/RumblingStone/x)`), perché lì la cartella del
   progetto è quella che contiene il clone.
4. **`--check`** esce 1 se `settings.json` non è allineato a `.claudeignore`;
   `scripts/tests/test_claudeignore_deny.py` lo lancia in CI.

## Le conseguenze

**Misura**: righe trovate da una ricerca nel repo, con `.gitignore` (come fa
Grep oggi) contro `.gitignore` più le 70 regole. Dalla cartella dei thread il
tool Grep ha dato 1.168 righe su «Skullcrusher», come `rg` con le regole.

| Ricerca | prima | dopo | |
|---|---|---|---|
| Skullcrusher | 1.912 | 1.168 | −39% |
| Thorik | 5.789 | 4.729 | −18% |
| Aegis Fang | 2.028 | 1.698 | −16% |
| Collezionista | 806 | 678 | −16% |
| Hammerfist | 7.555 | 6.785 | −10% |
| Sonjak | 698 | 635 | −9% |
| Belkram | 487 | 468 | −4% |

**Quello che si paga.** Un file generato non si apre più con Read: per
guardarlo serve togliere la voce o metterla sotto una marca `# leggibile:`. Bash non è
coperto: `cat` e `rg` da terminale leggono tutto, come prima. Il contesto
iniziale non cambia in modo misurabile: il guadagno è nelle ricerche.

**Correzione prima del merge.** La prima versione teneva le eccezioni in una
tabella dello script, che nominava lo specchio delle skill: il test
`test_tabelle.py::IlMirrorNonEUnaFonte` l'ha bocciata nella CI (nessuno
script cita lo specchio). Le eccezioni sono passate nella fonte, `.claudeignore`;
le regole generate sono le stesse 70.

**Aggiunta del 2026-11-25: la voce `**/rendered-*/`.** La voce `**/rendered/`
non copriva le cartelle dei temi nate dopo questo ADR (`CARTELLA_TEMA` in
`scripts/render_map_svg.py`): `rendered-pianta/`, `rendered-stampa-pianta/`,
`rendered-texture/`, con 255 SVG generati, 66,7 MB dei 140,6 MB di testo
tracciato che l'agente poteva leggere. Con la voce nuova le regole diventano
71 (sempre sedici voci leggibili) e i file tracciati coperti da `.claudeignore`
passano da 881 a 1.136. Scelta di Jfs su card del 25/11, «Sì, PR piccola dopo
la #518». Misura con il metodo di sopra, ma in byte e file trovati
(`rg -n -M 500 --ignore-file .claudeignore`), da `main` al ramo:

| Ricerca | byte | file |
|---|---|---|
| Skullcrusher | 232.067 → 231.230 (−0,4%) | 350 → 347 (−0,9%) |
| Thorik | 980.848 → 972.570 (−0,8%) | 696 → 676 (−2,9%) |
| Hammerfist | 1.367.804 → 1.357.446 (−0,8%) | 898 → 867 (−3,5%) |
| Aegis Fang | 344.278 → 342.339 (−0,6%) | 442 → 436 (−1,4%) |
| Belkram | 99.479 → 96.829 (−2,7%) | 115 → 108 (−6,1%) |

Il guadagno è piccolo e il contesto iniziale non cambia. In `rendered-texture/`
stanno anche texture CC0 committate, che l'agente non apre più con Read (gli
script e `validate_maps.py` sì). La regola non è stata provata in una sessione
vera; ha la stessa forma di `Read(**/rendered/**)`, provata qui il 19/11.
