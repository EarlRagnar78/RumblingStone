# Verificatori deterministici: che cosa si controlla con uno script e che cosa no

Inventario del 2026-11-20, per [ADR-0148](../../adr/ADR-0148-i-fatti-si-verificano-con-script-e-gli-agenti-con-prove-fisse.md).
Domanda di Jfs: i numeri, le regole e il canone si controllano con script
testati e misurati, non con un modello che rilegge. Ogni riga dice chi controlla
oggi, se il controllo è deterministico e dove sta il buco. I numeri sono misurati
sul ramo `claude/project-thread-o55i68` (sopra la #510), con il comando accanto.

## Che cosa c'era già

| Ambito | Strumento | Canale | Che cosa non vede |
|---|---|---|---|
| Numeri delle schede (pf, BAB, TS, CA, danni, incantesimi, talenti, gradi, GS) | `verifica_scheda.py`, `conformita_statblocchi.py`, `verifica_talenti.py` | testing (misura, non cancello) | schede a dossier, classi fuori dai dati: finiscono in `non_verificabili` |
| Numeri derivati delle creature, a ogni rifattorizzazione | `impronta_creature.py --confronta` | test | solo i quattro script delle creature |
| Regole citate nei master contro SRD e PRD | `riscontro_srd.py` | testing | le regole parafrasate senza nome |
| Fatti strutturati del canone | `validate_state.py`, `coerenza_campagna.py fatti` (S1-S8, T2) | cancello | solo ciò che è già un campo di `state.yaml` |
| Calendario | `test_calendario_flamerule.py` | cancello | cerca solo la parola «Mirtul» |
| Marche INFERRED | `controlla_marche.py`, `inventory_inferred.py` | cancello | — |
| Link e percorsi nei documenti | `validate_docs.py --sorgenti` | cancello | i rimandi per sezione («§N») |
| Booklet | `validate_booklets.py`, `validate_corredo.py`, `misura_statblocchi_booklet.py` | cancello | il testo del booklet esce dal master per costruzione; i file scritti a mano non sono confrontati (non misurato qui) |
| Agenti | `test_agenti.py` (#510) | cancello | la forma del file, non quello che l'agente produce |
| Prosa | `cricchetto_prosa.py` (#510), `punteggio_mqm.py`, `misura_craft.py` | cancello e misura | la qualità: resta al voto alla cieca (ADR-0093) |

## Buchi chiusi in questa PR

| Buco | Prima | Ora | Misura |
|---|---|---|---|
| Somme, soglie e livelli del registro dei PX | nessuno: lo rileggeva chi passava | `verifica_px.py`, cancello bloccante | 0 violazioni sulle tre versioni del registro nella storia (87afeb19, 322633bd, 1deeb125); 366 mutanti su 366 trovati (ogni cella cambiata di 1.000 PX); R2, R3 (anche il limite inferiore), R4 (ECL, LA, PG senza riga) con test propri; 16 test. Le soglie sono del PHB, Table 3–2, non dell'SRD |
| Rimandi per sezione | nessuno | `verifica_rimandi.py --check`, testing fino al 2026-12-04 (non blocca) | 1.744 rimandi: 1.026 tornano, 1 rotto (corretto su scelta del DM), 717 non giudicabili. Sullo storico (15/09, 15/10, 05/11) trova 2 rotture vere distinte e 0 falsi allarmi; 435 mutanti su 435 trovati |
| Prove fisse degli agenti | nessuna | 36 casi in `.claude/agent-evals/`, `prove_skill.py esempi` in CI | ogni caso ha un giudice deterministico; i giudici promuovono l'esempio buono e bocciano il cattivo in 36 casi su 36 |

### Le due rotture vere trovate da `verifica_rimandi`

- `campaign/state.md:170` cita «`ARC07-DEF-5` §94», ma DEF-5 ha i §0-§9. Rotto
  almeno dal 15/09. Il testo che il rimando cerca (Giorno 3, sync con l'ARC-08)
  sta nel §0-bis, riga 233. Jfs ha scelto su card (20/11) di correggerlo in
  «§0-bis»; `IN_ATTESA` è tornato vuoto.
- Al 15/09 `Arco-Post-Hammerfist-HOOKS-Tordek-DauthInvitation.md:102` mandava al
  §7 del master del Torneo, che aveva i §1-§6. Corretto dopo, nella storia.

### Quanto è costata la taratura

La prima versione di `verifica_rimandi` dava 8 violazioni sul repo di oggi, e a
mano una sola era vera: le altre erano «il §13 (libretto §12)», «§10 del
supplemento», «aggiungi il §6 a `PLAYTEST-ALFA.md`», elenchi di § di un altro
master dentro una tabella. Il «§N» senza nome è giudicato solo se la riga e le
due prima non nominano un altro documento. La regola è stata tarata sul repo di
oggi; le tre istantanee della storia sono la prova fuori campione (2 vere, 0
false).

## Buchi aperti, in ordine

1. **Date e Giorni di Marcia nella prosa.** 55 file d'arco scrivono «Day N». Nessuno
   li confronta con le finestre di `state.yaml` fuori dalle tabelle che
   `coerenza_campagna` sa leggere. Proposta: una regola per riga «Day N»
   accanto al nome di una fase o di un luogo con finestra in `state.yaml`.
   Il problema noto è l'estrazione (MS-0192: il lettore RAG 3B ha trovato 0 veri
   su 23).
2. **PX e livelli scritti nella prosa.** 19 righe fuori dal registro danno PX in
   cifre, 13 danno il livello di un PG. Esempio che uno script ingenuo
   sbaglierebbe: `ARC07-DEF-4:4125` dice «oltre i 105.000 PX» e due righe dopo
   «restano fermi a 104.999», ed è giusto (prima e dopo la regola del livello).
   Proposta: confrontare solo le cifre accanto al nome di un PG con il totale del
   registro, e misurare i falsi allarmi prima di farne un cancello.
3. **Nomi propri sconosciuti.** `fase1.py` conosce 327 nomi della campagna.
   Un controllo che segnala i nomi in maiuscola fuori elenco è facile da scrivere
   e rumoroso: va misurato su un campione a mano prima di decidere.
4. **Rimandi `§N-bis` e `§N.M`.** Oggi non si catturano: né violazioni né conteggio.
5. **Il 41% dei rimandi non giudicabile** (717 su 1.744): nome ambiguo (`ARC08-02`
   individua più file), bersaglio senza sezioni numerate, riga che nomina un altro
   documento.

## Che cosa resta fuori da ogni script

- **La qualità della prosa.** Le norme di forma si misurano (box, parentesi,
  nomi, MQM); se un box funziona al tavolo lo dice il voto alla cieca di Jfs.
- **La verità di un fatto che il repo non ha.** Uno script controlla che un
  numero torni con la fonte del repo; se la fonte stessa è sbagliata, nessun
  confronto interno lo trova.
- **Che un agente faccia bene un lavoro nuovo.** Le prove fisse vedono una
  regressione sui loro 36 casi e sulle trappole che contengono, non la qualità
  su un compito che non hanno.

## Come si rifanno le misure

```bash
python3 scripts/verifica_px.py
python3 scripts/verifica_rimandi.py
python3 -m pytest -q -s scripts/tests/test_verifica_px.py scripts/tests/test_verifica_rimandi.py
python3 scripts/prove_skill.py controlla --agenti && python3 scripts/prove_skill.py esempi
# storico dei rimandi: un worktree per data, lo script copiato dentro scripts/
```
