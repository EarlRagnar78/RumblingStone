# Piano: recupero delle decisioni perse e chiusura delle revisioni incompiute

> **Stato**: 🟡 **in corso** (2026-10-10). Portato nella #230 su richiesta del DM
> (*«questa PR la più recente e completa con tutto quello che è rimasto da fare»*):
> L3 fatto, L1 in corso col merge della #230, D1 e D2 chiuse. Il resto in §5.
> **Richiesta-fonte (DM, 2026-10-10)**: *«leggi tutti gli scratchpad relativi al
> repo rumblingstone per vedere se si sono perse decisioni prese o decisioni
> interrotte ma non più decise o script e parti che non sono mai arrivati nel
> main e crea un nuovo piano in modo che finiscono tutte le revisioni per piani
> mai completati; controlla se sono diventati obsoleti prima di importarli, in
> questo caso scartale»*.
> **Misurato su**: `main` a `f40ffeb` (merge della #227), storia completa
> (`git fetch --unshallow`), 7 PR aperte, 101 PR chiuse, 16 rami su `origin`.

## 0 · Informazioni mancanti e assunzioni

Quello che non so e che cambierebbe il piano:

1. **Che cosa intendi per «scratchpad».** Ho letto come tali i documenti di
   lavoro del repo: `plans/` (72 file), il registro dei rami
   `plans/contenuti-nei-rami.json`, `plans/adozioni-in-attesa.json`, i
   `PIANO-*` rimasti nella radice e i rami e le PR mai fusi. La cartella
   condivisa del progetto è vuota e la memoria del progetto non contiene
   niente: altrove non c'è altro da leggere. Se tenevi appunti fuori dal repo
   (una chat, un documento), questo piano non li vede.
2. **Cosa vuoi fare della #216.** È tua, in bozza, aggiornata oggi alle 15:22
   e fondibile senza conflitti. Porta su `main` tre decisioni che hai già
   preso (vedi §2.1). Assumo che la stai ancora portando avanti e che il merge
   sia una tua scelta (D1).
3. **Se un piano fermo con lotti «opzionali» vale ancora.** Non lo deduco: lo
   chiedo per gruppo (D5).

Assunzioni con cui procedo:

- Le PR #99 (lotti 4f, 4g, 4h) e #228/#231 (CI rossa) hanno ciascuna un thread
  di lavoro aperto in questo progetto. Questo piano **non le tocca**: le cita.
- Nessuna PR esistente si chiude o si modifica senza la tua conferma: dove
  serve, il lotto lo dice e si ferma.
- Una riga di una PR fusa che su `main` non c'è più è una **riscrittura
  successiva**, non una perdita, se il file è stato rifatto dopo il merge. L'ho
  verificato su sette PR campione (§2.4) e vale per tutte e sette.

## 1 · Cosa ho guardato, e cosa questo piano non rifà

Regola d'apertura di ADR-0044: prima di aprire si guardano i piani vicini.

| Piano vicino | Perché non basta, e il confine |
|---|---|
| [`PIANO-RIPRESA-PR-ABBANDONATE`](PIANO-RIPRESA-PR-ABBANDONATE.md) | Riprende quattro PR (#63, #52, #106, #99). Non guarda le PR aperte dopo il 4 settembre né le decisioni rimaste nei loro rami. **Qui non si rifà** niente di F1-F4: 4g, 4h e 4i-3 restano là. Per la #99 vale la proposta del thread dedicato (2026-10-10): chiuderla, 4g in due PR piccole da `main`, 4h scartato perché contrasta ADR-0007 |
| [`PIANO-RICONCILIAZIONE-PR-APERTE`](PIANO-RICONCILIAZIONE-PR-APERTE.md) | Fermo dal 4 settembre con R6-R8 «da decidere», che nel frattempo sono stati decisi altrove (§2.3). Questo piano propone di chiuderlo, non di continuarlo |
| [`STATO-E-ORDINE-DEI-PIANI`](STATO-E-ORDINE-DEI-PIANI.md) §0 | È la lista viva. Qui non la si duplica: si correggono le sue righe ferme (lotto L3) e si aggiunge una riga che punta a questo piano |
| Il thread «Audit settimanale PR e decisioni» | È una routine che **segnala** ogni lunedì. Questo piano **corregge** una volta. Dopo L1-L4 la routine trova meno rumore |

Il criterio per scartare viene da RICONCILIAZIONE: una cosa è **superata** se
è stata riscritta altrove, meglio o uguale; è **persa** se il contenuto
esiste solo in un ramo ed è ancora l'unico che quel problema abbia.

## 2 · Audit: cosa si è perso, cosa è obsoleto

Gli strumenti sono quelli del repo, nell'ordine di G6:

```bash
git fetch --unshallow origin
python3 scripts/contenuti_nei_rami.py --fetch        # i file
python3 scripts/contenuti_nei_rami.py --righe <ramo> # le righe
python3 scripts/decisioni_dm.py --check              # 14 aperte, 193 chiuse
python3 scripts/eco_decisioni.py --check             # 9 blocchi, 0 senza eco
python3 scripts/adozioni_in_attesa.py                # condizione spenta (1 file su 3)
```

### 2.1 · Decisioni prese che non sono su `main` (perdite vere)

Sono il ritrovamento principale. `main` le dà **aperte**, ma tu le hai già
decise e la risposta sta solo in un ramo.

| Decisione | Dove sta la risposta | Cosa dice `main` |
|---|---|---|
| `AGENT-SKILLS#D17` («sembra» seguito dalla smentita) | #216: decisa il 2026-10-03, il confine è in `read-aloud-adulti.md` §1 punto 7 | aperta in §4 |
| `LETTORE-PLAYTESTER#D38` (quando si gioca la Fase 0 di ARC-08) | #216: dopo il drago ai bastioni, aura come presenza terrificante SRD | aperta in §4 e nella riga di INDEX |
| Il genere di *Torre* nel Drappo (CODA-SECONDO-LETTORE §2 punto 1) | #216: decisa, applicata con quattro concordanze in ARC-09 | «decide il DM» |
| Il lotto D13 (27 modifiche «sembra/pare» su undici master) | #216: approvato e applicato | §0 riga 🙋 «al DM: approvare il lotto» |
| `RICERCA-MESTIERE#D12` (la riga `17` duplicata in `Portale-Forgia-L2`) | #230: non è una riga duplicata, è una didascalia di tre celle; le righe 19-33 sono lo specchio | aperta in §4 |
| `RESA-ASSET#D23`-`D30` (la resa misurata, ADR della sostituzione) | #230 | non esistono |
| `AMBIENTE#D7` (Python 3.13 ovunque, la versione di Debian stable) | decisa su `main` il 2026-10-08, **mai applicata**: la CI di `main` e quella della #230 girano ancora su 3.11 (`ci.yml` righe 26 e 422, `dipendenze.yml` righe 44 e 79) | decisa, ma il lotto A2 è ⬜. La #231, nel thread della CI rossa, porta la parte Python; A2 resta 🟡 per il job Debian 13 |

Due decisioni nuove esistono **solo** nella #216 e vanno al DM con lei:
`CODA-SECONDO-LETTORE#D2` (il campo *Etichetta regia* troncato) e `#D3` (la *d*
eufonica).

### 2.2 · Un conflitto che arriverà al merge

**La #216 e la #230 creano entrambe `plans/adr/ADR-0086-*`**, con due decisioni
diverse: *la memoria del lavoro è generata* e *una sostituzione nella resa entra
solo se misurata e preferita*. Chi arriva secondo su `main` fa fallire
`validate_docs --sorgenti`, e ogni citazione già scritta di «ADR-0086» diventa
ambigua: è il caso dell'ADR-0049 del 12 settembre. Il 2026-10-10 il thread sulla #99 ha proposto un **terzo** ADR-0086
(`/mnt/project-files/pr99/ADR-proposta-chiusura-PR-99.md`, la #99 si chiude):
tre candidati per un numero solo, e D2 deve assegnarli tutti. Per questo il piano **non
crea ADR numerati**: le sue decisioni stanno in §3 in forma breve.

### 2.3 · Decisioni aperte che l'aggregato non vede

Tabelle senza marker `decisioni-dm`, quindi assenti da §4:

| Dove | Voce | Verdetto |
|---|---|---|
| RICONCILIAZIONE, «Cosa resta da decidere» | R6 (⬛ tre glifi o uno) | **obsoleta**: `legend.yaml` ha ⬛ edificio, ⛺ tenda, 🔳 dais (ADR-0048) |
| idem | R7 (+4 CAR e non-rimovibilità della Corona) | **obsoleta**: confermati dal DM, STATO §1 riga R7 |
| idem | R8 (ordine di ripresa delle PR) | **obsoleta**: è l'ordine di RIPRESA-PR, approvato |
| CODA-SECONDO-LETTORE §2 | punti 3 e 4 | **già recuperati** nella #216 come D2 e D3 (§2.1) |
| DRAPPO §7.1 | la bonifica dei nomi senesi | **sospesa per tua scelta** il 2026-08-15, dichiarata: resta |
| RIPRESA-PR 4i-3 | la protezione di `main` (D23) | **rinviata da te**, è un lotto: resta |

Decisioni interrotte, cioè chieste e mai chiuse perché il messaggio si è
fermato: ne ho trovata una sola, `LETTORE-PLAYTESTER#D27`, ed è chiusa dal
2026-10-07. Ho cercato «si interrompe», «interrott», «troncat», «sospes»,
«rinviat», «in attesa del DM» in tutti i `plans/*.md`.

### 2.4 · Contenuto nei rami: misurato, poi giudicato

**PR chiuse senza merge** (dieci): #6, #42, #52, #63, #67, #72, #109, #143,
#206, #221.

| PR o ramo | Righe mai arrivate | Verdetto | Perché |
|---|---:|---|---|
| #72 | 1.292 | **portata, ma il registro l'ha dimenticata** | I piani assorbiti da VENDIBILITA, quattro ADR portati con altri numeri, ADR-0015 rifiutato, il soggetto in `plans/`. Le sue voci nel registro sono state potate come «scadute» il 2026-10-07 (commit `334dd46f`), e con `--fetch` tornano otto file «senza posto» |
| #6 (maggio) | 748 | **obsoleta** | `Armate-SINCRONIZZAZIONE-CAMPAGNA.md` è stato riscritto lo stesso giorno su `main` come «v2» (`cc382b3d`, base 10k e doppio orologio); il resto è `state.md` di maggio. Manca solo la riga nel registro |
| #63 e `claude/hammerfist-maps-ultra-clear-9pczfe` | 28 | **obsoleta** | Avvisi di «deprecato» su tre file `Hammerfist-Lotto-*` che su `main` non esistono più |
| #52, #221 | 1, 2 | **obsoleta** | Una riga di changelog; la #221 è sostituita dalla #228 |
| #42, #67, #109, #143, #206 | — | già giudicate | registro o STATO §3 |
| `claude/paizo-editorial-components-qky8nv` | 21 | **obsoleta** | Misure del 3 settembre (mediana 82 trattini), superate da quelle in skill |
| `claude/scripts-audit-documentation-u48g28` | 174 | **obsoleta** | Manifest e registri generati a luglio; `tools_manifest --check` oggi è verde su 100 tool |
| `claude/campaign-session-tools-j2dzx1` | 16 | **obsoleta** | Le pagine degli artefatti del 1° agosto, rifatte a stadi con ADR-0071; la frase sulla DES dei Bracieri è su `main` |
| `claude/map-generation-pipeline-7ka5a7` | 1 | **obsoleta** | Una riga di CHANGELOG; l'overlay è arrivato con la #51 |
| `claude/document-audit-prd-cleanup-j5ipln` | 11 | già «portato» | #143, ADR-0067 |
| #106 (aperta, ferma dal 15 agosto) | 68 | **obsoleta nel codice**, aperta per una decisione | `render_map_blender.py` su `main` legge le altezze da `legenda.altezze()` e la CI fa già il controllo di determinismo. Il ramo serve solo a `RIPRESA-PR#D2` |

**PR fuse con righe «mai arrivate»** (35 su 45 misurate): ho controllato le
sette più grandi (#85, #86, #87, #100, #138, #145, #148). In tutte le righe
mancanti stanno in file riscritti dopo il merge: booklet rigenerati, DEF
riletti, i Doni v2 sostituiti dalla v4-bis, `state_apply.py` rifatto in 4d.
**Si scartano in blocco**: l'evoluzione di `main` non è una perdita.

**Scratchpad nella radice**: `PIANO-REVISIONE-LIBRERIA-MOSTRI-PNG-VILLAIN.md`
è un piano completo (L0-L5 ✅) che non è in `plans/` e non ha una riga in
INDEX. Gli altri due `PIANO-*` della radice sono puntatori, come devono.

### 2.5 · Righe di stato ferme (dicono cose non più vere)

| Dove | Cosa dice | Cosa è vero oggi |
|---|---|---|
| STATO §0, riga «Il lotto mappe D28» ⬜ | da fare | fatto il 2026-10-08 (riga ✅ poco sopra) |
| STATO §0, riga «D27» 🙋 | aperta | chiusa il 2026-10-07 |
| STATO §0, riga «le marcature `[INFERRED]` di DEF-4 e DEF-5» | 51 in DEF-4 | 0 in DEF-4, 12 in DEF-5 |
| STATO §0, riga del giro 1 delle letture ▶ | «DM: D38, D39, D40; agente: D28, poi il giro 2» | D39, D40, D28 e il giro 2 sono fatti; D38 è nella #216 |
| STATO §0, riga del collaudo mappe | «restano al DM D10 e D12» | decise il 2026-10-08 |
| INDEX, RICERCA-RUOLI-EDITORIALI | P1-P7 tutti ⬜ | P1 (ADR-0023), P2 (skill `edizione`), P3 (`validate_lingua`), P4 (ADR-0026), P5 (ADR-0027), P6 (`mcp_server.py`), P8 (`dm.py volume`) esistono; P7 in parte (`validate_tipografia`) |
| INDEX, RICONCILIAZIONE | 🟡 3 lotti su 7 | quello che resta è deciso altrove (§2.3) |
| INDEX, REVISIONE-ARC08 | due ⬜ (i 65 read-aloud, l'apparato) | assorbiti da MASTER-DEF S1, che rifà i quattro master di ARC-08 |
| STATO §0, «le 120 legature della Corona» | 120 | 14 righe con `ﬀ` in tutto il repo: va rimisurato |

## 3 · Le decisioni, in forma ADR breve

Non sono ADR numerati per il motivo di §2.2. Se il DM ne vuole uno, si numera
dopo che #216 e #230 hanno risolto il loro 0086.

**R-1 · Le decisioni chiuse in un ramo entrano su `main` col ramo, non a mano.**
*Contesto*: D17, D38, la *Torre* e D12 risultano aperte su `main` e chiuse in
#216 e #230. *Decisione*: non si ricopiano le risposte su `main`; si portano su
`main` le due PR (D1). Se una delle due non arriva entro un giro, si porta il
solo contenuto delle tabelle `decisioni-dm`, come si è fatto con la #143.
*Conseguenze*: finché non succede, §4 mostra quattro decisioni aperte che non
lo sono. Il costo di ricopiarle sarebbe peggiore: due versioni della stessa
risposta che divergono al primo ritocco.

**R-2 · Il registro dei rami non pota le PR chiuse.**
*Contesto*: il 2026-10-07 dieci voci sono state tolte perché «scadute», cioè
non trovate fra i rami scaricati in quel momento. Le PR chiuse si scaricano
solo con `--fetch`, quindi la stessa voce era scaduta senza e viva con.
*Decisione*: una voce si toglie solo se il suo riferimento non esiste **dopo**
`--fetch`; altrimenti resta, col suo stato. *Conseguenze*: il registro cresce
di una riga per PR chiusa, e il giudizio dato una volta non si rifà.

**R-3 · Una riga mai arrivata da una PR fusa non è una perdita.**
*Contesto*: 35 PR fuse hanno righe che su `main` non ci sono. *Decisione*: si
scartano, salvo un commit sul ramo **dopo** la data del merge (lo cerca L2).
*Conseguenze*: si accetta il rischio di non vedere una correzione fatta sul
ramo dopo il merge e mai riportata. L2 lo riduce.

**R-4 · Un piano fermo non resta aperto per inerzia.**
*Contesto*: nove documenti chiusi o fermi (sette da più di 30 giorni) portano
ancora caselle ⬜, quasi tutte «opzionali» (§2.5 e D5). *Decisione*: ogni ⬜ di un piano fermo
diventa una delle tre cose: un lotto con una data, una voce di
`adozioni-in-attesa.json` con la condizione che la fa partire (ADR-0076), o
«non si fa» con il perché. *Conseguenze*: INDEX dice la verità su cosa resta;
il prezzo è una decisione del DM per gruppo, non per casella.

**R-5 · Nessun piano nuovo si apre per finire quelli vecchi.**
*Contesto*: la richiesta chiede «un nuovo piano». *Decisione*: questo documento
coordina, i lotti si chiudono nei piani dove stanno. Una casella chiusa qui
si chiude là, con la sua riga di CHANGELOG. *Conseguenze*: questo piano si
chiude quando L1-L6 sono fatti, e non accumula lavoro suo.

## 4 · Le decisioni al DM

<!-- decisioni-dm: RECUPERO -->

| # | Lotto | Domanda |
|---|---|---|
| ~~D1~~ | L1 | ✅ **Decisa il 2026-10-10, il DM: prima la #229 e la #230** (*«mergia se verde»*), non come proposto. Era: **In che ordine arrivano su `main` #216, #229 e #230?** La #216 porta D13, D17, D38 e la *Torre*, che hai già deciso; la #230 è impilata sulla #229. Tutte e tre sono bozze tue. *Proposta*: prima la #216 (più vecchia, fondibile senza conflitti, chiude tre decisioni), poi la #229 e la #230 con il loro ADR rinumerato a 0087. Nessuna si fonde senza il tuo sì |
| ~~D2~~ | L1 | ✅ **Chiusa il 2026-10-10 dalla regola stessa della proposta, l'ordine di arrivo**: la #230 arriva prima, quindi tiene `ADR-0086` (la sostituzione misurata); la #216 si rinumera a `ADR-0087` nel suo ramo prima del merge, la chiusura della #99 a `0088`. Era: **Chi tiene il numero ADR-0086?** Tre candidati: la memoria generata (#216), la sostituzione misurata (#230), la chiusura della #99 (proposta del thread dedicato). *Proposta*: nell'ordine di arrivo su `main`, quindi 0086 alla #216, 0087 alla #230, 0088 alla #99; ognuno si rinumera nel suo ramo prima del merge, con `validate_docs --prossimo-adr` |
| D3 | L5 | **`RIPRESA-PR#D2` e la #106**: il collaudo SDXL accanto a Gemini tiene aperta la #106 da otto settimane, e il suo codice è già su `main` in forma nuova. La #230 installa ComfyUI e scarica SDXL sulla tua Debian 13. *Proposta*: il collaudo delle due o tre immagini si fa con la #230 installata; la #106 si chiude subito come «contenuto portato», e la D2 resta aperta in RIPRESA-PR senza tenere aperta una PR |
| D4 | L5 | **`RIPRESA-PR#D11` (ADR-0049, l'AP originale)**: resta aperta dal 2026-09-11, legata a un avvocato IP e a VENDIBILITA, che non è autorizzato. *Proposta*: passa a voce di `adozioni-in-attesa.json` con la condizione «VENDIBILITA autorizzato», e lascia §4 |
| D5 | L4 | **I ⬜ opzionali dei piani chiusi o fermi**, per gruppo. *Proposta*: (a) chiusi come «non si fa»: AUDIT-SCRIPTS (shellcheck lo fa AMBIENTE A6), IMPORT-ULTRACLEAR (migrazione delle ~30 mappe, ora COLLAUDO-MAPPE), RENDER-FEDELTA (`--strict` default); (b) in attesa con condizione: TRAVASO A6 (quando ARC-07 finisce al tavolo), INTEGRAZIONE (quando c'è Foundry al tavolo), RICERCA-MODULO-PUBBLICABILE B3, C3, D5, RICERCA-TOOL-ESTERNI R1, RICERCA-TOOL-LGM P1-P3, GENERATORE J e K; (c) restano lotti: nessuno |
| D6 | L3 | **RICONCILIAZIONE-PR-APERTE si chiude come superato?** R3, R6, R7, R8 sono decisi o fatti altrove (§2.3). *Proposta*: sì, ✅ con il rimando a dove sta ognuno |

<!-- eco: RECUPERO 2026-10-10 -->
- **Decise**: D1 la #229 e la #230 su `main` per prime, se verdi · D2 lo `0086` resta alla #230, la #216 passa a `0087`
- **Aperte**: D3 (la #106), D4 (D11 di RIPRESA-PR), D5 (i ⬜ opzionali per gruppo), D6 (RICONCILIAZIONE chiusa come superata)
- **Cambiate**: D1, dove la proposta metteva prima la #216
- **Dedotto da me**: che la D2 segua l'ordine di arrivo anche quando l'ordine cambia, perché è la regola che la proposta stessa scriveva; e che la rinumerazione della #216 spetti al suo ramo, non a questo

## 5 · I lotti

Ogni lotto apre una PR sua, salvo L3 e L4 che stanno bene insieme.

### L1 · Le decisioni chiuse nei rami arrivano su `main` `[🟡 la #230 sì (D12, D23-D30); la #216 dopo, con l'ADR a 0087]`
`[engine: Opus 5, sessione principale · effort: alto · qualità: dopo il merge, decisioni_dm --check dà D17, D38, D12 chiuse, validate_docs --sorgenti verde con due ADR distinti]`

Classe **G**, perché decide un ordine di merge. Aspetta D1 e D2. Si esegue nel
thread della PR che arriva prima; qui si spunta. Se la #216 cambia ancora prima
del merge, si rimisura §2.1.

### L2 · Il registro dei rami, completo e che non dimentica `[⬜]`
`[engine: Sonnet 5 · effort: medio · qualità: contenuti_nei_rami --fetch --check esce 0; un test prova che una voce di PR chiusa sopravvive a un giro senza --fetch]`

Classe **C**. Fa R-2 nello script; rimette le voci della #72 come erano prima
di `334dd46f`; aggiunge #6, #52, #63, #221 e i cinque rami `claude/*` di §2.4
con stato `superato` o `rifiutato` e il perché in una riga. Per le PR fuse,
cerca i commit sul ramo con data successiva al merge (R-3) e li elenca: se ce
n'è uno con contenuto, diventa una riga di questo piano.

### L3 · Le righe di stato ferme `[✅ 2026-10-10, nella #230]`

Fatto: le righe di §2.5 di INDEX (RICERCA-RUOLI, RICONCILIAZIONE, REVISIONE-ARC08) e di STATO §0 (il lotto D28, D27, le `[INFERRED]` rimisurate: 0 in DEF-4, 12 in DEF-5; il giro delle letture); le 120 legature della Corona sciolte; questo piano della libreria in `plans/` con il puntatore nella radice. Con lo stesso giro, il controllo di tutti i piani contro checklist e CHANGELOG (17 righe corrette, 7 dubbi chiariti su commit e PR).

`[engine: Haiku 4.5 o inline · effort: basso · qualità: ogni riga di §2.5 corretta con la fonte accanto; decisioni_dm --check, check_plans_discipline verdi]`

Classe **M**, con una parte **G** (D6). Corregge sul posto le righe di STATO
§0 e di INDEX elencate in §2.5; rimisura le legature; sposta
`PIANO-REVISIONE-LIBRERIA-MOSTRI-PNG-VILLAIN.md` in `plans/` con un puntatore
nella radice e la riga ✅ in INDEX, come K-A ha fatto con gli altri.

### L4 · I piani fermi, una casella alla volta `[⬜]`
`[engine: Opus 5 · effort: medio · qualità: nessun ⬜ senza data, condizione o «non si fa» nei piani di D5; adozioni_in_attesa --check verde]`

Classe **G**. Applica D5 piano per piano. Le voci «in attesa» entrano in
`plans/adozioni-in-attesa.json` con una condizione misurabile, o restano fuori
se la condizione non si sa scrivere: in quel caso il lotto lo dice.

### L5 · Le due decisioni parcheggiate di RIPRESA-PR `[⬜]`
`[engine: Opus 5 · effort: basso · qualità: §4 non mostra più D11; la #106 chiusa con il commento che rimanda al registro, solo dopo il sì del DM]`

Classe **G**. Aspetta D3 e D4. La chiusura della #106 è un'azione su una PR:
si fa solo con la tua conferma esplicita.

### L6 · Chiusura `[⬜]`
`[engine: inline · effort: basso · qualità: le tre misure di §2 rifatte, con i numeri prima e dopo in questa sezione]`

Rimisura `contenuti_nei_rami --fetch --check`, `decisioni_dm --check` e le
righe di §2.5, e chiude il piano.

## 6 · Validazione

Ogni lotto, nello stesso commit:

```bash
python3 scripts/check_plans_discipline.py
python3 scripts/decisioni_dm.py --check
python3 scripts/eco_decisioni.py --check
python3 scripts/contenuti_nei_rami.py --check
python3 scripts/validate_docs.py --sorgenti
python3 -m pytest scripts/tests -q
```

Il piano ha funzionato se, alla fine, `--fetch --check` del registro esce 0
con tutte le PR scaricate, §4 contiene solo domande che nessun ramo ha già
chiuso, e la routine del lunedì non trova una riga di §2.5.
