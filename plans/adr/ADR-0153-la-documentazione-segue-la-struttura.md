# ADR-0153 — La documentazione segue la struttura

**Stato**: proposta (2026-11-27)
**Data**: 2026-11-27
**Decisione-fonte**: la scelta di Jfs del 27/11 sulla card del thread, opzione B, «CI più routine settimanale», da attivare «in modo smart» e con il costo in token per attivazione misurato. Le altre opzioni erano A (solo il cancello in CI) e C (solo una misura il lunedì). La base è l'audit del 27/11/2026 sulla documentazione dopo la #510 (`/mnt/project-files/documentazione-automatica-2026-11-27/AUDIT.md`).
**Rapporti**: corregge il cancello della catena di [ADR-0146](ADR-0146-le-skill-di-prosa-si-caricano-per-vincolo.md); riusa `validate_docs.indice_adr()` per gli ADR (una norma, un rilevatore); il cricchetto ha la forma di quello della prosa (ADR-0146). È parallelo ad ADR-0151 (custode della memoria, hook prima del merge) e ad ADR-0152 (`milestone.yml` su push a main, che leggerà `--debito --json`), scritti in altri thread.

## Contesto

Dal merge della #510 (21/11) a main 076a74d1 sono entrate 14 PR. Quattro
aggiungevano struttura (#508, #510, #512, #515), e nessun cancello guardava se
gli indici la seguivano:

- `AGENTS.md` non nominava nessuno dei 13 agenti di `.claude/agents/`; la loro
  tabella esisteva solo in una guida fuori dal repo;
- `docs/INDEX.md` non nominava `cricchetto_prosa.py`, `instradamento_agenti.py`,
  `vincolo_skill.py`, né i 4 workflow;
- `docs/explanation/ARCHITETTURA.md` citava gli ADR fino ad ADR-0126, su disco
  arrivano ad ADR-0149;
- `scripts/README.md` diceva «five skills»; sono 18.

L'agente che dovrebbe chiudere questi buchi, `autore-documenti`, è dichiarato
nel corpo di 9 PR su 14 (#512 #515 #516 #517 #518 #520 #521 #522 #524); non in
#507 #508 #523 #525 #526. Deroghe dichiarate: 0. È un'autodichiarazione: i
registri `.claude/.uso-*.jsonl` sono in `.gitignore` e muoiono con il
container del thread, quindi non resta nessuna prova che un agente sia stato
chiamato.

L'audit ha trovato anche perché il blocco della riga «Catena:» non fermava
niente. Il messaggio di avvio di un thread, con la nota del coordinatore e la
catena, arriva nella trascrizione come riga `type: "user"` con `isMeta: true`:
non è un prompt inviato, l'hook UserPromptSubmit non scatta e il registro resta
senza catena. Un `git push --dry-run` in un thread con
`Catena: sviluppatore → autore-documenti` passava con «nessuna catena scritta
nelle istruzioni». Dalla #510 il cancello non ha mai potuto fermare un thread
avviato così.

## Perché il cancello in CI da solo non basta

Il cancello sulle PR vede un elemento nuovo che il suo indice non cita. Non vede
un documento che resta indietro senza che nessuna PR aggiunga niente di
scoperto, né una descrizione che non è più vera. `ARCHITETTURA.md` lo mostra:
si è fermata ad ADR-0126 mentre entravano 22 ADR (0127-0149, senza lo 0135
prenotato), e nessuna di quelle PR aggiungeva un elemento che quel file dovesse
citare. Con la sola opzione A il buco sarebbe rimasto aperto.

## Decisione

1. **Il cancello della catena legge anche la trascrizione.**
   `decidi_cancello` in `scripts/instradamento_agenti.py` prende la catena dal
   registro e, se lì manca, dall'ultima riga «Catena:» dei messaggi a Claude
   nella trascrizione: solo testo scritto, righe `isMeta` comprese, mai un
   `tool_result` (una guida letta con uno strumento porta esempi di catena) né
   una riga `isSidechain` (un sottoagente). 8 test.

2. **In CI, a zero token.** `scripts/documentazione_allineata.py` conosce
   queste coppie:

   | Elemento | Indice |
   |---|---|
   | agente `.claude/agents/X.md` | `AGENTS.md` |
   | script di primo livello `scripts/X.py`, `scripts/X.sh` | `docs/INDEX.md` |
   | workflow `.github/workflows/X.yml` | `docs/INDEX.md` |
   | script lanciato da un hook di `.claude/settings.json` | `docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md` |
   | ADR | `docs/INDEX.md` §4, tramite `validate_docs.indice_adr()` |

   Sulle PR, `--rispetto-a origin/<base>` esce 1 se un elemento aggiunto non è
   citato, e il messaggio dice al thread di chiamare `autore-documenti` con il
   diff. `--debito --check` gira su ogni evento e confronta il totale con il
   `tetto` di `plans/debito-documentazione.json`: il tetto si abbassa a mano
   quando il debito scende, mai si alza. Sono passi di `ci.yml`. 11 test per
   il cancello e il cricchetto.

3. **Il lunedì, solo se serve.** La routine «Audit settimanale PR e
   decisioni», che gira già, lancia `documentazione_allineata.py --attiva
   --json` (circa 0,35 s; una chiamata Bash, stimata a 1-2 mila token di
   contesto). Se il campo `attiva` è vero, chiede al coordinatore un solo
   thread «Aggiornare la documentazione», con la riga
   `Catena: autore-documenti` e la lista `lavoro` (file e cosa) dell'uscita.
   Se è falso, non succede niente. `attiva` è vero se scatta almeno una regola:

   | Regola | Quando scatta |
   |---|---|
   | (a) | il debito supera il tetto |
   | (b) | c'è un agente, un workflow o un hook scoperto (gli script vecchi no: li tiene il cricchetto) |
   | (c) | `ARCHITETTURA.md` è indietro di 3 o più ADR, o di uno solo con più di 14 giorni |
   | (d) | un indice non è stato toccato negli ultimi 30 giorni mentre entravano elementi del suo tipo |

   Nessuna sessione programmata nuova e nessun workflow nuovo: la routine c'è
   già, e il workflow su main è `milestone.yml` di ADR-0152.

4. **Gli script vecchi restano nel debito.** L'indice degli script nuovi resta
   `docs/INDEX.md`. I 106 script di primo livello che oggi non cita non si
   pagano con altrettante righe: li tiene il cricchetto, e scendono quando
   qualcuno tocca la loro parte.

## Alternative considerate

- **A, solo il cancello in CI.** Costa zero token e ferma il buco nella PR che
  lo apre, ma non vede i documenti che restano indietro (sezione sopra).
- **C, solo una misura il lunedì.** Trova il buco dopo il merge, e qualcuno
  deve comunque decidere di chiamare l'agente.
- **Una sessione programmata che chiama `autore-documenti` ogni settimana.**
  Scartata perché paga un'attivazione anche quando non c'è niente da fare:
  `--attiva` decide prima di spendere.
- **Misurare gli script contro il registro generato `docs/tools/README.md`.**
  Il debito sarebbe sceso subito a 18. Scartata: il registro si genera dal
  manifest e cita in automatico ogni script che ha un contratto, quindi non
  avrebbe preso i tre script della #510, che avevano il manifest ma nessuna
  riga scritta da una persona.
- **Pagare ora tutto il debito degli script.** Circa 110 righe in
  `docs/INDEX.md`, quasi tutte copia del registro generato. Scartata per la
  stessa ragione.

## Le conseguenze

Prova retroattiva sulle PR già unite: la #510 avrebbe avuto 15 elementi nuovi
scoperti (12 agenti, `cricchetto_prosa.py`, `instradamento_agenti.py`,
`vincolo_skill.py`) e sarebbe stata rossa; la #512 0, verde; la #515 2
(l'agente `sincronizzatore-giocato` e il workflow `sincronia-giocato.yml`),
rossa.

Il debito misurato su main 076a74d1 era 127: 109 script fuori da
`docs/INDEX.md`, 13 agenti fuori da `AGENTS.md`, 4 workflow, l'hook
`session-start.sh`, 0 ADR. Con la PR di questo ADR scende a 106, tutti script
vecchi, e il tetto passa da 127 a 106.

`--attiva` sul ramo di questa PR dà `attiva: false`. Su main 076a74d1, con il
tetto a 106, dà `attiva: true` per tre regole: (a) debito 127 oltre 106, (b) 18
elementi (13 agenti, 4 workflow, 1 hook), (c) 22 ADR non citati in
`ARCHITETTURA.md`. Sulla regola (b) la lista `lavoro` coincide con quello che
`autore-documenti` ha fatto in questa PR: gli stessi 18 elementi. Sulla (a)
mette in testa i tre script della #510, quelli citati qui; ne chiede 21 e non 3
perché il tetto confrontato è già quello abbassato. Sulla (c) chiede di citare
tutti i 22 ADR; §14.1 ne cita sei (0140, 0141, 0146, 0148, 0149 e questo), e la
regola si spegne lo stesso perché guarda solo il numero più alto.

Il costo di un'attivazione è misurato su questa PR: 174.239 token di
sottoagente, 45 chiamate, 6 min 19 s, per pagare 21 elementi, scrivere §14.1
di `ARCHITETTURA.md`, questo ADR e le righe di CHANGELOG e memoria storica. Il
valore sta in `token_per_attivazione` di `plans/debito-documentazione.json`, e
`--attiva --json` lo riporta come `stima_token`. Un'attivazione piccola costa
meno, ma non è misurata.

Quello che si paga:

- **Il cancello controlla che un elemento sia citato, non che la descrizione
  sia buona.** Una riga sbagliata o vuota lo fa passare, e nessuna delle
  quattro regole se ne accorge. La qualità resta al giudizio di chi rivede la
  PR.
- **I registri restano locali.** Che `autore-documenti` sia stato chiamato in un
  thread si sa solo nel thread; la CI vede l'effetto (la riga nell'indice), non
  la chiamata.
- **La correzione del cancello della catena è provata su una sola trascrizione
  reale**, quella del thread dell'audit, più i casi sintetici dei test. Una
  forma diversa del messaggio di avvio la farebbe tornare cieca; il test che lo
  direbbe è un thread nuovo con la catena nel primo messaggio e un
  `git push --dry-run`.
- **Le regole di `--attiva` hanno limiti noti.** In un clone shallow la regola
  (d) non giudica gli hook, e le date che legge da git sono incomplete. La (c)
  guarda solo il numero di ADR più alto citato, non i buchi in mezzo. La (d)
  dice che un indice è fermo, non che cosa manca: il lavoro che elenca va
  verificato da chi lo esegue.
- **ARCHITETTURA ha il blocco degli agenti e dei cancelli (§14.1)**, che cita
  gli ADR dal 0140 a questo; le parti degli ADR intermedi (0127-0139,
  0142-0145, 0147) non sono state riportate.
- Un nome si cerca intero nell'indice: uno script citato solo in una frase che
  non lo descrive conta come documentato.
