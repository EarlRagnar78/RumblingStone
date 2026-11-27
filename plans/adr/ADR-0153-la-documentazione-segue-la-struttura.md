# ADR-0153 — La documentazione segue la struttura

**Stato**: proposta (2026-11-27)
**Data**: 2026-11-27
**Decisione-fonte**: l'audit del 27/11/2026 sulla documentazione dopo la #510 (`/mnt/project-files/documentazione-automatica-2026-11-27/AUDIT.md`). La forma del meccanismo è aperta su una card a Jfs con tre opzioni: cancello in CI (consigliata, ed è quella scritta qui), CI più una routine settimanale nel cloud che chiama `autore-documenti`, solo una misura il lunedì. Se Jfs sceglie un'altra opzione, questo ADR si corregge prima di passare ad accettata.
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

## Decisione

1. **Il cancello della catena legge anche la trascrizione.**
   `decidi_cancello` in `scripts/instradamento_agenti.py` prende la catena dal
   registro e, se lì manca, dall'ultima riga «Catena:» dei messaggi a Claude
   nella trascrizione: solo testo scritto, righe `isMeta` comprese, mai un
   `tool_result` (una guida letta con uno strumento porta esempi di catena) né
   una riga `isSidechain` (un sottoagente). 8 test.

2. **Un elemento strutturale nuovo entra con la riga nel suo indice.**
   `scripts/documentazione_allineata.py` conosce queste coppie:

   | Elemento | Indice |
   |---|---|
   | agente `.claude/agents/X.md` | `AGENTS.md` |
   | script di primo livello `scripts/X.py`, `scripts/X.sh` | `docs/INDEX.md` |
   | workflow `.github/workflows/X.yml` | `docs/INDEX.md` |
   | script lanciato da un hook di `.claude/settings.json` | `docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md` |
   | ADR | `docs/INDEX.md` §4, tramite `validate_docs.indice_adr()` |

   Sulle PR, `--rispetto-a origin/<base>` esce 1 se un elemento aggiunto non è
   citato, e il messaggio dice al thread di chiamare `autore-documenti` con il
   diff. È un passo di `ci.yml`: nessun workflow nuovo. In CI non ci sono
   agenti, quindi il meccanismo non chiama nessuno da solo; ferma la PR finché
   il thread non lo fa. 11 test.

3. **Il debito vecchio sta sotto un cricchetto.** `--debito --check` confronta
   il totale con il `tetto` di `plans/debito-documentazione.json`: il tetto si
   abbassa a mano quando il debito scende, mai si alza.

4. **Gli script vecchi restano nel debito.** L'indice degli script nuovi resta
   `docs/INDEX.md`. I 106 script di primo livello che oggi non cita non si
   pagano con altrettante righe: li tiene il cricchetto, e scendono quando
   qualcuno tocca la loro parte.

## Alternative considerate

- **Misurare gli script contro il registro generato `docs/tools/README.md`.**
  Il debito sarebbe sceso subito a 18. Scartata: il registro si genera dal
  manifest e cita in automatico ogni script che ha un contratto, quindi non
  avrebbe preso i tre script della #510, che avevano il manifest ma nessuna
  riga scritta da una persona.
- **Pagare ora tutto il debito degli script.** Circa 110 righe in
  `docs/INDEX.md`, scritte in fretta e quasi tutte copia del registro
  generato. Scartata per la stessa ragione: l'indice diventerebbe una seconda
  copia del registro.
- **Una routine settimanale che chiama `autore-documenti`**, o solo una misura
  il lunedì: sono le altre due opzioni della card. Una misura settimanale trova
  il buco dopo il merge; il cancello lo trova nella PR che lo apre.

## Le conseguenze

Prova retroattiva sulle PR già unite: la #510 avrebbe avuto 15 elementi nuovi
scoperti (12 agenti, `cricchetto_prosa.py`, `instradamento_agenti.py`,
`vincolo_skill.py`) e sarebbe stata rossa; la #512 0, verde; la #515 2
(l'agente `sincronizzatore-giocato` e il workflow `sincronia-giocato.yml`),
rossa.

Il debito misurato su main 076a74d1 era 127: 109 script fuori da
`docs/INDEX.md`, 13 agenti fuori da `AGENTS.md`, 4 workflow, l'hook
`session-start.sh`, 0 ADR. Con la PR di questo ADR scende a 106, tutti script
vecchi: la tabella degli agenti entra in `AGENTS.md`, i workflow e i tre script
della #510 in `docs/INDEX.md`, l'hook nella guida di configurazione. Il tetto
passa da 127 a 106.

Quello che si paga:

- **Il cancello controlla che un elemento sia citato, non che la descrizione
  sia buona.** Una riga sbagliata o vuota lo fa passare. La qualità resta al
  giudizio di chi rivede la PR.
- **I registri restano locali.** Che `autore-documenti` sia stato chiamato in un
  thread si sa solo nel thread; la CI vede l'effetto (la riga nell'indice), non
  la chiamata.
- **La correzione del cancello della catena è provata su una sola trascrizione
  reale**, quella del thread dell'audit, più i casi sintetici dei test. Una
  forma diversa del messaggio di avvio la farebbe tornare cieca; il test che lo
  direbbe è un thread nuovo con la catena nel primo messaggio e un
  `git push --dry-run`.
- **ARCHITETTURA ha il blocco degli agenti e dei cancelli (§14.1)**, che cita
  gli ADR dal 0140 a questo; le parti degli ADR intermedi (0127-0139,
  0142-0145, 0147) non sono state riportate.
- Un nome si cerca intero nell'indice: uno script citato solo in una frase che
  non lo descrive conta come documentato.
