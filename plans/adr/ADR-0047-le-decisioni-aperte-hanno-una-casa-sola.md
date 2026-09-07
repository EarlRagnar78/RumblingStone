# ADR-0047 — Le decisioni aperte hanno una casa sola, e l'elenco si genera

- **Stato**: accettata
- **Data**: 2026-09-06
- **Decisori**: DM (Gianfranco Samuele), agente
- **Origine**: richiesta DM del 2026-09-06 — *«la quarta cosa della regola d'oro
  (la tabella "cosa aspetta il DM") fagli un gate, e mantienila sincronizzata
  per evitare lo sfasamento»* · la debolezza dichiarata in
  `STATO-E-ORDINE-DEI-PIANI` §5

## Contesto

La regola d'oro dei piani (ADR-0009) chiede **quattro** aggiornamenti a ogni
lotto chiuso: la checklist del piano, `INDEX.md`, `CHANGELOG.md` e — se cambiano
ordine o dipendenze — `STATO-E-ORDINE-DEI-PIANI`. Le prime tre le controlla
`check_plans_discipline`. La quarta no, e il piano lo ammetteva per iscritto:
*«è una debolezza dichiarata: questo file è una fotografia, e una fotografia
invecchia»*.

Ha ceduto al primo giro in cui due decisioni si sono chiuse a un giorno di
distanza. Misurato il 2026-09-06:

| | Sfasamento |
|---|---|
| **D1** | decisa il 05-09; `INDEX` lo diceva, §4 la dava **ancora aperta** |
| **D6** | decisa il 04-09; §4 **non la elencava affatto** — la tabella saltava da D4 a D7 |
| **D7-D10** | 🐛 **non esistevano in nessun piano**: quattro identificatori nati nell'aggregato, senza una fonte |

Il terzo è il difetto vero, e spiega gli altri due. La tabella **non era
derivata da niente**: era un secondo elenco scritto a mano accanto ai piani. Due
elenchi paralleli sullo stesso fatto divergono sempre — è la forma esatta
dell'elenco delle skill di [ADR-0041](ADR-0041-instradamento-delle-skill-con-un-gate.md),
che diceva 13 voci su 18.

⚠️ **E c'è una trappola specifica di questo dominio**: `D<n>` **non è un
identificatore globale**. Otto piani hanno il loro `D1..Dn` con significati
incompatibili — in `REVISIONE-ARC07` sono **17 decisioni già prese** (canone), in
`RICERCA-AUDIT` sono **difetti**, in `IMPORT-ULTRACLEAR` sono **tipi di difetto**.
Un gate che confrontasse «D5 con D5» accoppierebbe il Rubino di ARC-07 con la
griglia di `…P1C`.

## Decisione

### 1. La decisione vive nel piano che l'ha generata

Il piano è dove la domanda nasce e dove le conseguenze della risposta atterrano.
L'aggregato è una comodità di lettura, non una fonte.

### 2. Conta solo ciò che è dichiarato

Una tabella entra nel conteggio se e solo se è preceduta dal marker

```
<!-- decisioni-dm: <etichetta> -->
```

Niente euristiche sui titoli: i piani li scrivono in tre modi diversi
(*«Le decisioni che restano al DM»*, *«Cosa resta da decidere al DM»*, *«Le
decisioni ferme al DM»*), e indovinare avrebbe raccolto le diciassette di
ARC-07. È la lezione di ADR-0041: **non indovinare, contare ciò che è
instradato**.

### 3. L'identità è `piano#Dn`, mai il numero da solo

La numerazione resta **per piano**, e non si rinumera: rinumerare romperebbe
ogni riferimento già scritto in changelog, commit e conversazioni. L'aggregato
porta la colonna «Piano» proprio per questo.

### 4. Lo stato si legge da un segno, non dal testo

**Chiusa** se l'identificatore è barrato — `~~D1~~`. Aperta altrimenti. Nessuna
inferenza sul contenuto: un ✅ in mezzo a una frase non è un dato.

### 5. §4 di `STATO-E-ORDINE` è generato

Fra i marker `<!-- auto:begin key=decisioni-dm -->` e `<!-- auto:end … -->` —
la stessa convenzione che `state_apply` usa già per il March Clock. Si rigenera
con `decisioni_dm.py --emit`; **si modifica il piano, mai l'aggregato**.

### 6. Il drift è rosso in CI

`decisioni_dm.py --check` esce 1 se aggregato e piani divergono, e il passo sta
in CI accanto al gate della regola d'oro. Le aperte vanno in cima all'elenco, e
il conteggio è scritto: **è la riga che il DM legge per sapere cosa aspetta lui**.

## Conseguenze

**Cosa migliora.** «Cosa aspetta il DM» smette di essere una fotografia e
diventa una misura: chiudere una decisione nel piano e non rigenerare **non
compila più**. E le quattro decisioni orfane hanno finalmente una casa — D7-D10
sono entrate in `RICERCA-MESTIERE` §7, coi numeri conservati.

**Cosa costa.** Un marker da mettere quando un piano apre la sua prima
decisione, e un `--emit` quando se ne chiude una. Se qualcuno dimentica il
marker, le decisioni di quel piano **non compaiono** — e questo il gate non lo
vede, perché non può sapere che una tabella esiste se nessuno gliel'ha detta.
È il limite dichiarato, ed è lo stesso di ADR-0043: un master che *nessuno*
dichiara resta fuori. Il rimedio parziale è che un marker **senza** tabella
sotto è già un errore.

**Cosa non copre.** La *qualità* della domanda. Il gate conta e confronta; che
una decisione sia scritta in modo comprensibile resta responsabilità di chi la
scrive.

**Cosa cambia nella regola d'oro.** Le cose controllate a macchina passano da
tre a quattro. `STATO-E-ORDINE` §5 va riscritto: la quarta non è più «una
debolezza dichiarata».

## Alternative scartate

**Un gate che chieda solo di "aver toccato il file".** Si aggira con uno spazio,
e avrebbe lasciato passare tutti e tre gli sfasamenti misurati: toccare non è
allineare.

**Rinumerare tutte le decisioni in un unico spazio globale.** Risolverebbe la
collisione fra piani, al prezzo di invalidare ogni riferimento già scritto —
`D5` compare in changelog e commit di due mesi. La coppia `piano#Dn` costa una
colonna e non rompe niente.

**Tenere l'aggregato a mano e riletto a ogni lotto.** È esattamente ciò che si
faceva: la riga di changelog del 2026-09-06 è la prova che «riletto a mano» non
regge due decisioni chiuse in due giorni.
