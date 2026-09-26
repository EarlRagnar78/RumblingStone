# RICERCA — Il «Manuale del Master Supremo»: cosa regge, cosa c'era già, cosa si scarta

> **Cos'è**: il controllo, punto per punto, di due documenti che il DM ha portato
> il 2026-09-26 (*Il Manuale Supremo del Dungeon Master* e il suo *Modulo 2*),
> per decidere quali insight entrano nel repo e dove.
>
> **Stato**: ✅ ricerca completa (2026-09-26) · **Attuata in**:
> `skills/rumblingstone-module-standard/references/sviluppo-degli-incontri.md`
> e nelle domande del playtester · **Fonti**: i due file, così come sono
> arrivati, in `esperimenti/manuale-del-master/`

---

## 0 · Il giudizio d'insieme

La richiesta del DM: *«vedi se hanno regole e insight che, implementati, rendono
epiche le avventure senza togliere niente alla storia […] se servono e non sono
coperti, crea un ruolo, così non si perdono, se sono validi e affidabili»*.

I due documenti sono una sintesi generata a macchina: lo dice la nota di
chiusura del secondo, una clausola medica che con il gioco di ruolo non ha
niente a che fare. Le idee di fondo vengono da fonti vere e note: Robin D. Laws,
Justin Alexander, la DMG 3.5, Matt Mercer, le liste dei Tier di Giant in the
Playground. Gli errori stanno nei dettagli, dove una sintesi fatta così sbaglia
di solito: attribuzioni, tabelle, nomi di abilità, numeri dei mostri.

**Il ruolo che mancava** è quello del *developer*: chi guarda un incontro e
chiede se si gioca. Non serve una skill nuova. Il posto giusto è un riferimento
dentro `rumblingstone-module-standard`, che è già lo strato «che cosa sto
scrivendo» (L2 di `ORCHESTRAZIONE.md`). Una diciannovesima skill avrebbe dovuto
dividersi il campo con `module-standard`, `npc-villain-boosting` e
`rumblingstone-playtest`, e ADR-0058 dice che caricare di più è il bersaglio
sbagliato.

## 1 · Il verdetto, punto per punto

«Coperto» vuol dire che il repo ha già la regola, e dove. Il conteggio viene da
una ricerca sui `skills/` controllata a mano, non dalle parole chiave da sole.

| Insight dei manuali | Affidabile? | Nel repo | Esito |
|---|---|---|---|
| Robin's Laws: sette modi di stare al tavolo | ✅ libro del 2002, i sette tipi sono quelli | i **profili veri** dei quattro giocatori in `campaign-dm-strategy.md` §1, più precisi | ➕ solo per stand-alone e gruppi nuovi (§7 del riferimento) |
| Three Clue Rule, scenari a nodi (Alexandrian) | ✅ | `rumblingstone-indagine`: tre porte per nodo, fatto raggiungibile da due nodi, self-check 6 | già coperto |
| Ecologia del dungeon, fazioni | ✅ | fazioni e agende in `narrative-style` e `campaign-dm-strategy` §2; **chi sente il rumore** no | ➕ §4 del riferimento |
| Tier delle classi, *linear warrior / quadratic wizard* | ✅ il concetto · ❌ **la tabella**: Guerriero e Paladino stanno in due Tier diversi; nell'originale di JaronK sono Tier 5 | niente | ➕ §1 del riferimento, con l'originale |
| Pressione del tempo contro la «giornata da cinque minuti» | ✅ | l'orologio delle tacche di `DEF-4`, i clock di `state.md`, l'`ADR-10` dell'Abbazia | già coperto |
| Economia d'azione, sgherri | ✅ | `npc-villain-boosting` Gate 2: *add bodies first* | già coperto |
| Ricchezza per livello | ✅ la tabella della DMG · ❌ la soglia del 20%, che la DMG non dà | `ARC07-TESORO-WBL-AUDIT`, `module-standard` §8 | già coperto |
| *Automatic Bonus Progression* | ✅ esiste, in *Pathfinder Unchained* | — | ❌ scartato: è PF1e, e a metà campagna rifarebbe da capo il valore degli artefatti |
| Boss a più fasi | ✅ come pratica moderna (non è 3.5) | soglie di pf nelle tattiche round per round; nessuna regola | ➕ §5, **dentro l'SRD** e col tetto EL |
| I due boss pronti (Valerius, Xar'Kesh) | ❌ numeri non verificati, «RD 5/Magia e Adamo» non significa niente | — | ❌ scartati: la regola 5 di `AGENTS.md` vieta di importare statistiche inventate |
| Skill challenge | ✅ i numeri (da 4 a 12 successi prima di 3 fallimenti) · ❌ «perfezionate dall'Alexandrian», che invece ne ha criticato la matematica; l'esempio usa abilità di 5e (Atletica, Intuizione) | usati nei master, mai scritti come regola | ➕ §6 del riferimento |
| Enigmi: interattivi, tiri di supporto, fallimento in avanti | ✅ | le sei porte e le prove grezze di `indagine`; i «modi di fallimento» sono un congegno di `misura_craft` | già coperto |
| Mercer: fili del background, PNG come ancore, *how do you want to do this?*, terreno | ✅ | pilastro Mercer di `narrative-style`, congegno `[HDYWTDT]`, Echo Ledger, la regia del cortile in `DEF-4` | già coperto |
| Checklist: linee di vista, varietà dei TS, contromisure a volo e invisibilità, DR | ✅ | niente di questo | ➕ §2 e §3 del riferimento; linee di vista e DR restano a `mapmaking` e a `npc-villain-boosting` |
| «La Mercenaria», forum italiano | ⚠️ non verificato: nessuna traccia trovata | — | non citato |

## 2 · Una misura, perché «varietà dei tiri salvezza» è verificabile

Tiri salvezza con CD dichiarata nei master di ARC-07, contati con
`Tempra|Riflessi|Volontà … CD N`, senza le note storiche:

| Master | Tempra | Riflessi | Volontà |
|---|---:|---:|---:|
| `DEF-1` (Terros) | 8 | 7 | 1 |
| `DEF-2` (affreschi) | 0 | 0 | 3 |
| `DEF-3` (resurrezione) | 0 | 0 | 3 |
| `DEF-4` (mille anni) | 2 | 7 | 4 |
| `DEF-5` (ritorno) | 0 | 1 | 3 |

`DEF-2` e `DEF-3` sono riti e dialoghi: una sola Volontà è giusta. `DEF-1` ha
una Volontà sola in tutto il master, che è quello del combattimento con Terros, e `DEF-5` non ha Tempra.
Sono indizi, da guardare scena per scena: il conteggio non sa quale TS è in uno
scontro e quale in un rito. Per questo la norma è registrata **senza** cancello.

## 3 · Cosa questa ricerca non ha potuto verificare

- Le pagine della DMG 3.5 sull'ecologia del dungeon: il manuale le attribuisce a
  Monte Cook, e il riferimento cita solo «la DMG 3.5» senza pagina.
- L'esistenza del forum «La Mercenaria».
- Se le domande del developer migliorano davvero i master: lo dirà la prima
  lettura a freddo di un master di ARC-08 scritto con queste domande.
