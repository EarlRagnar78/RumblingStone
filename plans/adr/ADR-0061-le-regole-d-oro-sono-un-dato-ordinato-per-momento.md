# ADR-0061 — Le regole d'oro sono un dato, ordinato per momento

**Stato**: accettata (2026-09-20), attuata
**Contesto**: domanda del DM, 2026-09-20 · [`skills/REGOLE-DORO.md`](../../skills/REGOLE-DORO.md)
**Parente stretta**: [ADR-0058](ADR-0058-orchestrazione-a-strati-delle-skill.md), che
ha fatto la stessa cosa alle skill

---

## Contesto

Il DM, dopo l'aggiunta della sesta regola d'oro:

> *«Questa nuova golden rule migliora la gestione e la misurazione dei problemi
> […] o deve essere cambiata, o era meglio la versione precedente? […] Le
> golden rule si sovrappongono o entrano in conflitto? Questi conflitti possono
> essere eliminati, se esistono? Quale è il miglior modo per organizzare le
> golden rule?»*

Misurato su `AGENTS.md` prima di rispondere, e la struttura era peggiore di
quanto la lettura suggerisse:

| Difetto | Misura |
|---|---|
| **tre forme diverse** per sei regole | G1-G3 voci di elenco (righe 109-115), G4-G6 titolo `####` più blockquote (128-211). Nessun pattern le estrae tutte |
| **il numero non identifica** | tre elenchi partono da `1.` nello stesso file (righe 109, 301, 363). *«regola 8»* compare due volte e si riferisce al terzo |
| **l'ordine dei numeri non è l'ordine d'uso** | G1 (*leggi i `references/`*) non è eseguibile prima di G5 (*quali skill*), ma viene prima |
| **nessun cancello** | è la condizione di ADR-0056, applicata alle regole che ADR-0056 ha generato |

## Decisione

**Le sei regole diventano una tabella con un gate, ordinata per il momento del
ciclo in cui scattano** — non per la data in cui sono state aggiunte, che è
l'ordine attuale e non ha nessun significato operativo.

```
🟦 PRIMA    G5 quali skill  →  G6 FASE 1 sui bersagli  →  G1 leggi i references
🟨 DURANTE  G2 misura prima di affermare
🟥 DOPO     G4 self-check   →  G3 registra la norma nuova
```

Tre scelte dentro la decisione, ognuna con la sua ragione:

1. **Gli id diventano `G1`..`G6`**, e i numeri restano quelli storici. Cambia
   solo la lettera, perché i numeri sono citati in ADR, piani e commit già
   scritti; la `G` toglie l'ambiguità con le altre due liste numerate.
2. **La narrazione resta in `AGENTS.md`**, la struttura va in
   `skills/REGOLE-DORO.md`. Un agente che legge solo la tabella sa *cosa* fare;
   uno che legge solo la narrazione sa *perché*, e il perché è quello che
   impedisce di applicarle a vuoto.
3. **I conflitti si dichiarano invece di eliminarli.** Misurati: **uno solo** è
   un conflitto vero (G1 contro G5 sul perimetro di cosa leggere), e ha ora un
   vincitore. Gli altri quattro sono **sovrapposizioni utili**, e fonderle
   toglierebbe presidio.

## Conseguenze

- `scripts/validate_skills.py` verifica quattro cose sulla tabella: id unici e
  in sequenza, un momento previsto per ognuna, ogni `scripts/*.py` nominato che
  **esiste**, un verdetto per ogni conflitto. Più il ponte: ogni id della
  tabella compare anche nella narrazione.
- **Una regola nuova non può più nascere senza un momento e un verificatore.**
  È lo stesso meccanismo che impedisce a una skill di nascere fuori dalla
  gerarchia.
- La risposta alla domanda *«era meglio prima?»* diventa verificabile: la sesta
  regola non ha peggiorato nulla, ma **ha reso visibile** che il gruppo non
  aveva struttura. Un elenco di sei voci senza ordine di esecuzione si applica
  a memoria, e a memoria se ne salta una.

## Limiti dichiarati

1. **Il gate controlla la forma, non la saggezza.** Può verificare che G4
   dichiari un comando esistente; non può verificare che qualcuno l'abbia
   eseguito. L'unica regola con un cancello che *morde davvero* resta G6
   (`fase1.py --check`), e le altre cinque si applicano ancora sulla parola.
2. **L'ordine del ciclo è una scelta, non un teorema.** G2 potrebbe stare in
   PRIMA (si misura anche per decidere). Sta in DURANTE perché il fallimento
   che l'ha generata è un'affermazione fatta senza misura, non una decisione.
3. **Il terzo pilastro delle misure non esiste ancora.**
   `PIANO-MISURA-EDITORIALE-STANDARD` è dove vivrà *quanto vale un difetto*
   (MQM, severità, soglie, κ), ed è **pianificato allo 0%**:
   `scripts/punteggio_mqm.py` e `specifiche-qualita.yaml` non sono scritti.
   `REGOLE-DORO.md` §2 e `fase1.py` lo nominano **con il suo stato**, perché un
   meccanismo deterministico che punta a un file inesistente è peggio di uno
   che dichiara il buco.
