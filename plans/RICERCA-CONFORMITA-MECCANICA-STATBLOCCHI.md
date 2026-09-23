# RICERCA — Un rilevatore di conformità 3.5/PF1e è fattibile? L'audit di parsabilità

> **Cos'è**: la misura che risponde alla domanda del DM del 2026-09-21 —
> *«ha senso fare dei detector che verificano la conformità 3.5 e PF1e, in modo
> da marcare le sezioni con prove e statblocchi e misurare dove i valori sono
> errati?»*. Non propone un rilevatore: misura **se si può scrivere**, e su
> quanti documenti.
>
> **Perché una ricerca e non un piano**: la domanda era «ha senso?», e la
> risposta onesta richiede di contare prima. Un piano che partisse senza questo
> conto misurerebbe il proprio parser invece del contenuto — è il difetto che
> questo repo ha catalogato venti volte.
>
> **Metodo**: conteggio deterministico su `Bestiario/*/*-cr*.md`, eseguito il
> 2026-09-21. Riproducibile.

## 1 · Cosa questa ricerca NON rifà

- **`PIANO-GENERATORE-CREATURE-E-PNG`** va nella direzione opposta: da
  (GS + ruolo + tipo) **produce** un blocco. Qui si **verifica** un blocco che
  esiste già. I due si incontrano il giorno in cui il generatore usa il
  verificatore come collaudo.
- **`npc-villain-boosting`** e il tetto `EL ≤ APL+4` riguardano la
  **difficoltà dell'incontro**, non l'aritmetica interna di una creatura.
- **`validate_bestiario.py`** presidia già **struttura, naming, GS coerente col
  nome del file e catalogo in sync**. Questa ricerca guarda solo i **numeri**.

---

## 2 · La superficie: 231 file, 110 che portano numeri

| | Quanti | % |
|---|---:|---:|
| file in `Bestiario/` | 231 | |
| statblocchi con GS nel nome | 182 | |
| — di cui **`[POINTER]`**, che per progetto **non portano numeri** | **72** | 40% |
| — di cui **statblocchi veri** | **110** | 60% |

🔎 **I 72 POINTER non sono un buco**: dichiarano che i numeri stanno nel file
d'arco, per non tenerne due copie che divergono alla prima correzione
(ADR-0021). Contarli fra i «non misurabili» gonfierebbe il debito con righe che
si chiudono togliendo una regola giusta.

## 3 · Il formato è strutturato, ed è la buona notizia

Gli statblocchi veri usano un blocco ```` ```statblocco ```` con campi
espliciti. Sui **110**:

| campo | presente in | % |
|---|---:|---:|
| `gs` | 108 | 98% |
| `ca` | 108 | 98% |
| `pf` | 108 | 98% |
| `ts` | 108 | 98% |
| `ca-dettaglio` | 104 | 95% |
| `pf-dado` | 95 | 86% |
| `attacchi` | 65 | 59% |
| **`attributi`** | **14** | **13%** |

Il GS si legge dall'intestazione nel **100%** dei casi.

---

## 4 · 🐛 Il rilevatore esiste già, e legge il campo sbagliato

`validate_bestiario.py --rules` confronta **da luglio** il GS dichiarato con il
benchmark *Monster Statistics by CR* di PF1e. Gira in CI come **avviso, non
cancello**, e stampa **zero avvisi**.

Lo zero non vuol dire che vada tutto bene. Le sue due regex cercano `hp N` e
`ac N`, mentre il formato canonico scrive `pf:` e `ca:`:

| | legge | su 110 |
|---|---:|---:|
| `hp` (cerca `hp N`) | 54 | **49%** |
| CA (cerca `ac N`) | 64 | **58%** |
| il campo canonico `pf:` / `ca:` | 108 | **98%** |

⚠️ **Ma non legge spazzatura, e va detto.** Sui **53** file dove entrambe le
forme compaiono, il numero che estrae **coincide sempre** con il `pf:`
canonico: 53 su 53. Il difetto è **copertura**, non correttezza — vede metà
della libreria e tace sull'altra metà. Ventunesimo caso della famiglia «un
criterio che non pesca si traveste da repo pulito», e il più mite finora.

**Il primo lotto è quindi minuscolo**: far leggere al controllo i campi che il
repo usa davvero porta la copertura dal **49% al 98%** senza scrivere un
rilevatore nuovo. È lo stesso schema di F2.7.

---

## 5 · Cosa si può verificare, e cosa no

La domanda del DM era se le skill `dnd-35-srd` e `pathfinder-1e-srd` possano
servire a un controllo deterministico. ⚠️ **Una skill è testo di riferimento
per un agente, non una tabella leggibile da uno script**: i numeri vanno
estratti in un dato versionato. Fatto quello, ecco cosa regge e cosa no.

| Identità da verificare | Serve | Copertura | Verdetto |
|---|---|---:|---|
| **GS vs benchmark PF1e** (pf e CA nella fascia della sfida) | `gs`, `pf`, `ca` | **98%** | 🟢 **fattibile**, e il codice c'è già |
| **CA interna**: contatto e sprovvista **non superano** la CA | `ca`, `ca-dettaglio` | **95%** | 🟢 **fattibile** — misurato: **0 violazioni** su 104 |
| **pf dai DV e dalla Costituzione** | `attributi` | **13%** | 🔴 **no**: è `SUPERFICIE_VUOTA` (ADR-0062) |
| **TS dalla progressione di classe** | `attributi`, DV | **13%** | 🔴 **no**, stesso prerequisito |
| **attacco = BAB + modificatore + taglia** | `attributi`, `tipo` | **13%** | 🔴 **no**, stesso prerequisito |

🔴 **Il muro è uno solo, ed è un dato che manca: le caratteristiche.** Solo
**14 statblocchi su 110** dichiarano `attributi`. Senza For/Des/Cos non si
ricava nessuna delle tre identità profonde — e scrivere il rilevatore lo stesso
darebbe `0 violazioni` su un insieme vuoto, che è indistinguibile da
`0 violazioni` su una libreria corretta. È esattamente il caso che ADR-0062
esiste per non far ripetere.

---

## 6 · Cosa propone

| | Lotto | Costo | Cosa sblocca |
|---|---|---|---|
| **1** | far leggere a `--rules` i campi `pf:` e `ca:` | **due regex** | copertura **49% → 98%**, senza rilevatori nuovi |
| **2** | la coerenza interna della CA (contatto ≤ CA) | piccolo | oggi **0 violazioni**: nasce verde, presidia le prossime |
| **3** | promuovere `--rules` da **avviso** a **cancello** | una riga di CI | ⚠️ **solo dopo** il lotto 1: promuoverlo adesso renderebbe bloccante un controllo che vede metà libreria |
| **4** | la tabella PF1e in un YAML versionato accanto a `specifiche-qualita.yaml` | medio | il dato esce dal codice, e lo può correggere il DM |
| **5** | 🔵 **decisione del DM**: si dichiarano gli `attributi` nei 96 statblocchi che non li hanno? | **alto, e non è codice** | è l'unica porta verso le tre identità profonde, e verso il **primo `critico`** del punteggio |

🔎 **E il lotto 5 è il vero snodo.** La FASE 3 del `PIANO-MISURA-EDITORIALE` ha
misurato il 2026-09-21 che il κ è **0,0** perché la metrica promuove tutto: le
serve una norma che morda. Una verifica aritmetica su uno statblocco sarebbe
`critico` — un documento con i numeri incoerenti è ingiocabile — e sarebbe la
prima. Ma con `attributi` al 13% morderebbe su tredici documenti su cento.

⚠️ **Il conto onesto del lotto 5**: 96 statblocchi da completare a mano, e le
caratteristiche di una creatura non si indovinano. Dove la fonte è un export
PCGen i numeri esistono e si trascrivono; dove la creatura è originale, le
sceglie il DM. È lavoro di canone, non di codice, e per questo è una decisione
e non un lotto.

---

## 7 · Come si riproduce questa misura

```bash
python3 scripts/validate_bestiario.py --rules   # 21-09: 0 avvisi (§4 spiega perché) · 23-09: 29
grep -c '^pf:' Bestiario/*/*-cr*.md | grep -c ':1'
grep -rl '^attributi:' Bestiario --include='*.md' | wc -l   # 21-09: 14 · 23-09: 109
python3 scripts/genera_attributi.py --check      # 93 blocchi generati, riproducibili
python3 scripts/genera_attributi.py --taratura   # errore dello strato 3: 1,91 → 1,63 → 1,50 punti
python3 scripts/conformita_statblocchi.py --riepilogo   # 23-09 sera: 95 tornano, 0 scarti del generatore
```

---

## 8 · Esito dei lotti (2026-09-21 → 2026-09-23)

| | Lotto | Esito |
|---|---|---|
| ✅ | **1** · `--rules` legge `pf:` e `ca:` | copertura **49% → 98%**. Il ripiego sulla forma vecchia resta per i file senza blocco; i `[POINTER]` si saltano, perché i loro numeri stanno nel file d'arco |
| ✅ | **2** · la coerenza interna della CA | nata verde come previsto: **0 violazioni** |
| ✅ | **2-bis** · `pf-dado` registra i dadi vita *(non previsto)* | 🐛 **46 statblocchi su 95** non lo facevano: **26** portavano il danno di un'arma, già presente in `attacchi`; **20** una parte sola dei dadi (`4d8` per un ogre con sei livelli da barbaro). **42 ricostruiti** dalla formula che la scheda scrive o dalle classi del tipo, **4 tolti** (classi di prestigio non SRD). Il `danno dell'arma` mancava dal campo `attacchi` in un solo file, il sergente hobgoblin, e ora c'è. La causa: il lettore di settembre li rifiutava, ma i blocchi scritti ad agosto non sono mai stati ricontrollati. Da oggi `conformita_statblocchi.py --check` è un cancello in CI |
| 🟡 | **3** · promuovere `--rules` a cancello | **la parte che morde è promossa**: il controllo su `pf-dado` è un cancello (vedi 2-bis). Il benchmark per GS resta un avviso, ed è giusto: i suoi 5 avvisi sono quattro incantatori con pochi pf e un cavaliere gnoll da 11 pf, informazioni e non errori |
| ✅ | **4** · la tabella PF1e in un YAML versionato | `scripts/pf1e-statistiche-per-gs.yaml`, **31 righe e 11 colonne** trascritte dalla fonte OGL il 2026-09-23. 🔴 Il repo ne aveva **due copie** diverse, e le otto righe dichiarate «verificate» sbagliavano danno, CD e TS cattivo (il GS 12 aveva l'attacco del GS 11): la skill e la costante erano state scritte dalla stessa mano, e il test che le confrontava confrontava lo stesso errore. `dmcore`, `validate_bestiario` e la skill leggono ora un dato solo |
| ✅ | **5** · gli `attributi` nei 96 statblocchi | 🔵 **il DM ha deciso: generarli.** Fatto per **94** (gli altri due erano `[POINTER]`), con `genera_attributi.py` e alle condizioni di [ADR-0064](adr/ADR-0064-gli-attributi-si-scrivono-nel-bestiario.md). **39 copiati** dalla sestina che la scheda stessa scrive, **37 trascritti** dalla fonte, **18 scelti**. ⚠️ La prima versione di questo esito diceva «55 scelti»: 39 di quei 55 avevano i numeri del DM nella prosa (vedi l'emendamento di ADR-0064) |
| ✅ | **6** · pf, TS, BAB, lotta e attacco tornano con le caratteristiche *(chiesto il 2026-09-23)* | `conformita_statblocchi.py`, alle condizioni di [ADR-0065](adr/ADR-0065-la-conformita-si-corregge-dove-il-dato-non-e-una-scelta.md). Primo giro: 11 statblocchi corretti a mano, uno per uno. **Secondo giro, coi talenti** (idea del DM), l'iniziativa e la variante Advanced: altri **4** corretti (Ghaurush «Cenere Piena» CA 23 → 25, Mira Serani Vol +8 → +9 col talento che nominava, phantom fungus Init −1 → +0, blue psion lotta −4 → −5). Dopo le decisioni D8 e D9 del DM (For 18 al chierico gnoll; Karruk in tre stati d'ira, col BAB da +16 a +14): su **107** verificabili **86 tornano**, 5 uguali alla fonte, **7 decisioni aperte** (§9), **0 da correggere**, 9 scarti di un punto su caratteristiche scelte |
| ✅ | **6-ter** · i 9 scarti del generatore *(2026-09-23 sera)* | **Nessuno dei nove era del generatore soltanto**, e guardarli uno per uno ha dato quattro cause diverse. 🐛 **Il lettore**: una parentesi dopo il punteggio («For 25 (21 base +4 innesto)») nascondeva la sestina di tre schede, e Zin'thara, una maga con Int 22, aveva Car 21. 🐛 **Un giro circolare**: dove la Cos era generata, il bonus di `pf-dado` veniva ricavato dai pf supponendo la media, e il generatore ricavava la Cos da quel bonus; Khorn scrive «8d10+24, Cos 16» e ne usciva con Cos 18. Ora il bonus viene prima dalla **Tempra**, che è un'identità esatta, e dai pf solo se la Tempra li mette fuori fascia. ✅ **Il tetto dei TS** (strato 2-quinquies): un TS sotto l'atteso abbassa Cos, Des o Sag, ma solo se il valore viene dall'array. ✅ **L'iniziativa senza talenti** ammette due Des, e l'array sceglie fra quelle due. 🔧 **Quattro correzioni di numeri del DM**, con marca e conto: ogre micelio lotta +18 → **+22** (Lottare Migliorato elencato e non contato) e Tempra +10 → **+11** (era la Cos prima dell'innesto); ogre frantumapietra Riflessi +1 → **+2** (Des 8 confermata da CA, contatto e iniziativa); Teschio Nero Tempra +12 → **+13** (Cos 18 scritta due volte). Oggi: **95 tornano, 0 scarti del generatore, 0 da correggere, 7 decisioni aperte**. La taratura scende a **1,50 / 1,54** |

🔎 **Il template PF1e nei commit.** `5bdbbce` ha fatto nascere
`genera_creatura --piu-cattivi`: Advanced applicato **senza alzare il GS**. Nel
Bestiario nessuno statblocco viene da lì; i template dichiarati sono il Giant
del bruto e l'Advanced di Ghaurush, e il verificatore ora controlla la variante
scritta contro la sua regola: aveva la CA sbagliata di 2.

🔎 **Il sospetto del DM sui template PF1e, misurato.** *«Controlla se sono
questi i casi che non tornano: sono creature potenziate coi template PF1e»*. Il
verificatore rifà i conti con Advanced (+4 a tutto) e Giant (For e Cos +4, Des
−2) su ogni scheda che non torna: **nessuno scarto si spiega così**. I
potenziati tornano tutti, perché il template sta già nelle caratteristiche che
il DM ha scritto (For 31 del bruto è For 27 del gigante di pietra più il Giant).
Gli scarti rimasti sono errori di un punto nelle schede di maggio, o numeri che
si contraddicono fra loro.

📏 **La taratura ha il suo banco fuori campione.** Le 39 sestine delle schede
sono venute fuori dopo aver fissato le regole del generatore: lo strato scelto
ci sbaglia di **1,84 punti**, contro 1,63 sul banco su cui le regole sono state
scelte. Regge.

⚠️ **Cosa resta, e da chi dipende.** Le 7 decisioni di §9 sono del DM. Gli
scarti su caratteristiche generate sono chiusi (lotto 6-ter): il generatore
legge i TS, e dove un numero del DM era il solo a non tornare si è corretto
quello, alle condizioni di ADR-0065 §2.

🔵 **Un residuo che non è di questo piano.** I razorfiend verde e bianco, e
altre sei schede (Lorana, Varis, Salvatore, Azarr Kul, Ushgar, Sethrax),
portano `ts` scritti da `derive_statblocks --apply-ts` con una matrice di
caratteristiche propria (For 14, Cos 13). Nei razorfiend quella matrice è
smentita dalla formula del DM, `10d12+50`, che vuol dire Cos 20: la Tempra
derivata (+8) è di quattro punti sotto quella della variante blu, che il DM ha
scritto a mano (+12) con gli stessi dadi vita. Oggi il verificatore non la
vede, perché senza `tipo` né `pf-dado` la composizione non si legge. Rigenerare
quei `ts` dalle caratteristiche di adesso è un lotto di `derive_statblocks`
(ADR-0033), non di questo.

| | Lotto | Esito |
|---|---|---|
| ✅ | **7** · i TS derivati che nessuno aveva riletto *(2026-09-23 sera)* | 🐛 **La causa**: il 2 settembre `derive_statblocks --apply-ts` ha scritto i `ts` di otto schede perché il lettore non vedeva la forma dei dossier («- **Tempra:** +7»); il 3 settembre il lettore l'ha imparata (`d859a31`), e nessuno ha riletto gli otto blocchi. **15 TS su 18** dei sei dossier divergevano da quelli del DM: Salvatore Riflessi +6 dove il DM scrive +13, Sethrax Tempra +9 dove scrive +5. ✅ **A**: cinque dossier ritrascritti dalla loro prosa, col valore vecchio in nota. ✅ **E**: il dossier di Ushgar diventa `[RIMANDO]` allo statblocco `ushgar-occhio-reso-cr13.md`; nel catalogo Ushgar compariva **due volte**, con TS diversi. ✅ **C**: il lettore crollava su Sethrax (il GS scritto solo come «→ CR 12» prendeva un gruppo vuoto). ✅ **B**: `extract_statblocks --check` confronta ora pf, CA, GS e TS del blocco con la prosa della stessa scheda — **verde oggi, cinque rossi sullo stato di prima** — e il catalogo prende il CR dal blocco: Azarr Kul era **18** (il CR di Tyrgarun), Sonjak **14** (Urialle), Lythiel **5** (il suo gufo). 🐛 **E un difetto mio del lotto 6-ter**, trovato provando D: il tetto dei TS usava anche i `ts` derivati, e avrebbe abbassato la Sag del razorfiend verde da 16 a 10. Corretto con una prova. 🔵 **Restano D10 e D11**, al DM |

---

## 9 · Decisioni aperte al DM

Sono gli statblocchi dove `conformita_statblocchi.py` trova uno scarto e **due
numeri scritti dal DM puntano in direzioni opposte**: correggere l'uno o
l'altro cambia la creatura in modo diverso, e scegliere non spetta a uno
script. Il verificatore legge questa tabella: finche' una riga e' aperta, lo
scarto esce come «decisione aperta» e non come errore.

<!-- decisioni-dm: CONFORMITA-STATBLOCCHI -->

| # | Statblocco | Domanda |
|---|---|---|
| D1 | `goblin-warrior1-cr05` | **For 9 o For 11?** La riga delle caratteristiche e il danno (1d6−1) dicono For 9; la lotta −3 e l'attacco +2 presuppongono For 11, che e' la Forza del goblin SRD. Con For 9 la lotta e' −4 e l'attacco +1 |
| D2 | `tyrgarun-blue-old-cr18` | **For 33 o lotta +46?** Con BAB +30, taglia Enorme (+8) e For 33 (+11) la lotta e' **+49**. Il +46 presuppone For 26-27: forse la Forza di un'altra categoria d'eta' |
| D3 | `drow-assassina-lolth-cr10` | **For 12 o For 10-11?** La lotta +6 e il danno della spada corta +1 (1d6+1) presuppongono mod For +0; la riga delle caratteristiche dice 12. Riflessi e' gia' corretto (+13) |
| D4 | `drow-trickster-arcano-cr11` | **BAB +4 o +5?** Ladro 3 (+2), Mago 5 (+2) e Trickster Arcano 2 (+1) danno +5; la lotta +3 con For 8 presuppone +4. La classe di prestigio e' nel titolo, e il verificatore non la conta |
| D5 | `ghost-lion-spettrale-cr8` | **Come si legge il template?** Non morto con Cos 20 e `8d12+40`: nel 3.5 un non morto non ha Costituzione, e il bonus ai pf e' della regola PF1e (Carisma). L'attacco +15 non torna con BAB da non morto (+4) ne' da animale (+6) |
| D6 | `loxo-warrior3-cr4` | **Bestia magica o umanoide mostruoso?** La scheda dichiara bestia magica (`3d10`), ma i suoi TS (Temp +7, Rifl +2) non tornano con nessuna delle due progressioni |
| D7 | `druid-bear-ally-cr12` | **I 120 pf sono in forma selvatica?** Con `12d8` e Cos 13 il massimo possibile e' 108. In forma d'orso (Cos 19) la fascia arriva a 144 e 120 ci sta: se e' cosi', la scheda lo deve dire |
| D10 | `razorfiend-green-cr9` · `razorfiend-white-cr8` | **Si applicano i TS ricalcolati?** I due blocchi portano `ts` scritti da `derive_statblocks --apply-ts` il 2 settembre con Cos 13, e la formula dei dadi vita che il DM scrive in prosa (`10d12+50`, `9d12+36`) vuol dire Cos 20 e 18. La proposta (patch pronta, non applicata): trascrivere `pf-dado` dalla prosa, lasciare che `genera_attributi` ricavi la Cos, e ricalcolare i TS dal SRD. Verde **+12/+8/+10**, bianco **+10/+6/+7**; il verde torna con la variante blu che il DM ha scritto a mano (+12/+8/+9). ⚠ La Volontà dipende da una Sag **generata** (16 e 12): se il DM la vuole come la blu (Sag 11), il verde scende a Vol +7 |
| D11 | `derive_statblocks --apply-ts` | **Si toglie l'opzione che scrive?** È l'unica volta che uno dei tre script ha scritto numeri in `Bestiario/`, e ha prodotto gli otto blocchi sbagliati di questo lotto. Oggi il cancello di `extract_statblocks --check` la prende dove la prosa scrive i TS, ma non dove la prosa tace (i razorfiend). Senza `--apply-ts` lo strumento torna a quello che la sua docstring dichiara: **propone e non scrive**. L'alternativa è tenerla e farle scrivere anche gli `attributi` da cui deriva, perché non contraddicano quelli di `genera_attributi` |
| ~~D8~~ | `gnoll-cleric-yeenoghu-cr7` | ✅ **decisa dal DM il 2026-09-23: For 18**, anche nella riga delle caratteristiche. Lotta +10 e attacco +12 la presupponevano già; il danno 1d8+5 torna |
| ~~D9~~ | `wyrmlord-karruk-cr10` | ✅ **decisa dal DM il 2026-09-23: tre stati, fuori ira, in ira, affaticato.** L'ira era la causa: caratteristiche, Volontà, squartare e roccia erano in ira, pf, CA e `pf-dado` fuori, e lotta, Tempra, attacco e danno non tornavano con nessuno dei due. Lo statblocco ora è fuori ira, con una tabella dei tre stati calcolati dal SRD. In più il BAB scende da +16 a **+14** (gigante 12 DV + Barbaro 5), come dicono i tre attacchi iterativi |

