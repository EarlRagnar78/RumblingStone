# 📏 Registro delle norme editoriali — e chi le misura

> **Cos'è**: l'elenco di **ogni file normativo** su prosa, stile e linea
> editoriale, con le sue norme **numeriche o verificabili** e — per ognuna —
> se qualcosa la misura o no.
>
> **Perché esiste**: il 2026-09-18 si è scoperto che `read-aloud-adulti.md`
> dichiara da agosto **box ≤ 12 righe, un solo nome proprio nuovo, niente
> parentesi**, e che **nessuno strumento del repo lo guardava**. `ADR-0014`
> era stato applicato a **un documento su cento**. Non per cattiva volontà:
> perché una norma senza misura non fa rumore quando viene ignorata.
>
> **Gate**: `python3 scripts/validate_norme_editoriali.py` —
> [ADR-0056](../plans/adr/ADR-0056-una-norma-senza-misura-non-esiste.md)

---

## Come si legge, e come si aggiorna

- **Ogni file** della superficie normativa deve stare qui. Aggiungerne uno
  senza registrarlo fa **fallire il gate**.
- **`misurato da`** deve nominare un congegno che esiste davvero in
  `scripts/misura_craft.py` o un cancello che esiste davvero. Un nome inventato
  fa **fallire il gate** — è la lezione di ADR-0053 applicata al registro
  stesso.
- **`non misurato`** è una risposta legittima, ma **deve portare il perché**.
  Una riga vuota fa fallire il gate.

⚠️ **Questo registro non dice che le norme sono rispettate.** Dice se
**qualcuno le guarda**. La differenza è tutta la ragione per cui esiste.

---

## 1 · `rumblingstone-narrative-style/references/` — la voce e la pagina

| File | Norma verificabile | Severità | Stato |
|---|---|---|---|
| `read-aloud-adulti.md` | box **≤ 12 righe** (2-4 per un round, 8-12 apertura, 4-6 rivelazione) | **maggiore** · `box_oltre_12_righe` | 🟢 `misura_craft --box` |
| `read-aloud-adulti.md` | **un solo nome proprio nuovo** per box | **minore** · `box_piu_di_un_nome_proprio` | 🟢 `misura_craft --box` |
| `read-aloud-adulti.md` | **niente parentesi né incisi** lunghi | **minore** · `box_con_parentesi` | 🟢 `misura_craft --box` |
| `read-aloud-adulti.md` | max **due livelli** di subordinate | **minore** | 🔴 non misurato — servirebbe un parser sintattico dell'italiano; il segnale povero (contare le virgole) darebbe falsi positivi come i 64/64 di `PIANO-PROSA-CHE-NON-SEMBRI-GENERATA` |
| `read-aloud-adulti.md` | box di combattimento chiude su **«Che fate?»** | **maggiore** | 🟢 congegno `chiusura su decision point` |
| `editorial-standards.md` | `**Read-aloud (pilastro lead).**` etichettato | **maggiore** | 🟢 congegno `regia etichettata **Read-aloud (X)**` |
| `editorial-standards.md` | `**NOME (registro/tono):** *«battuta»*` | **maggiore** | 🟢 congegno `dialogo nella forma dichiarata` |
| `editorial-standards.md` | **la quarta colonna**: un blocco sensoriale chiude con «Cosa NON dire» (ADR-0057) | **minore** | 🟡 congegno `quarta colonna sensoriale` — conta **chi ce l'ha**, non accusa chi non ce l'ha: non esiste modo automatico di sapere se un blocco *avrebbe dovuto* averla |
| `editorial-standards.md` | terminologia canonica (CD non DC, 5e bandito, metri) | **maggiore** · `terminologia_non_canonica` | 🟢 `validate_modules.py` §BANNED — ma **solo sui 5 master DEF** |
| `editorial-standards.md` | blockquote **3-10 righe**; max **1-2 MAIUSCOLE** per read-aloud | **minore** · `maiuscole_di_enfasi` | 🟡 parziale — `--box` usa il tetto **12** di `read-aloud-adulti`; le due fonti non concordano sul minimo e lo script **non sceglie per loro**. 🐛 **La seconda metà diceva il falso**: «le maiuscole non sono misurate» era scritto qui mentre `validate_prosa` le contava da settembre, con la soglia in `SOGLIE['maiuscole']`. Non mancava il rilevatore, mancava il **nome**: `controlla()` restituiva stringhe già formattate e nessuno poteva contarle per norma. Dal 2026-09-21 pesano |
| `style-pillars.md` | *fusion rule*: **un lead, max due support** per scena | **minore** | 🟢 congegno `PILASTRO dichiarato (lead/support)` — conta la marca, non la conformità |
| `style-pillars.md` §Mercer | **`[HDYWTDT]`**: al colpo che uccide un boss la narrazione passa al giocatore, e il marcatore **va scritto** nel testo dell'incontro | **minore** | 🟢 congegno `[HDYWTDT] il finisher al giocatore` — 🔴 era a **zero in tutti e nove gli archi** |
| `style-pillars.md` §Mercer | **yes-and with teeth**: l'invenzione del giocatore entra nel canone **e** genera una complicazione | **minore** | 🟡 congegno `assorbi e rilancia (yes-and with teeth)` — conta chi **dichiara** il congegno, non chi lo applica al tavolo: quello lo sa solo il DM |
| `SKILL.md` §Self-check | **sette domande prima di consegnare**, più il controllo di coerenza | **minore** | 🟡 cinque delle sette hanno un comando (vedi `AGENTS.md` §quarto obbligo); la **4** (numeri di serie) è giudizio puro, e la **2** è un indicatore |
| `pc-protagonism.md` | **nessun PG oltre il 40%** delle scene marcate; **≥1 scena** a testa | **maggiore** | 🟡 `misura_craft --spotlight` — indicatore: conta le **menzioni del nome**, non le scene marcate, che il repo non marca |
| `consequence-echoes.md` | **≥1 eco armato** quando la finzione lo consente; **≥2** alla convergenza | **maggiore** | 🟡 congegno `eco / conseguenze a distanza` conta le **menzioni**, non gli echi armati e pagati |
| `passate-redazionali.md` | **massimo una chiusa a effetto** per documento; massimo un tricolon | **minore** · `antitesi_ripetuta` | 🟢 `validate_prosa.py --documenti` (lotto D di PROSA-CHE-NON-SEMBRI-GENERATA) |
| `italiano-nativo.md` §8 | almeno una **dislocazione a sinistra** o un **c'è presentativo** | **minore** | 🟡 `misura_craft --costrutto-italiano` — **281 box su 477 (59%)**, e il numero dice che è una **sovrastima**, non un difetto. Il «c'è» presentativo si riconosce con certezza; la **dislocazione a sinistra** («Il libro, l'ho letto») vuole sapere che *libro* è l'oggetto di *letto*, e una regex non lo sa: il pattern prende i casi col clitico dopo la virgola e perde gli altri. 🔴 **Misura e non pesa, apposta**: una norma *positiva* rilevata a metà produce penalità **false** su chi la rispetta in un modo che il pattern non vede. Contare male in negativo è peggio che non contare |
| `italiano-nativo.md` §9 | i **tic dell'IA**: antitesi «non X: è Y», tricolon, chiuse a effetto | **minore** · `calco_dall_inglese` | 🟢 `validate_prosa.py` |
| `italiano-nativo.md` §9.2 | il **trattino lungo come respiro**: sopra il 3% delle parole di un read-aloud è un tic | **minore** · `trattino_come_respiro` | 🟢 `validate_prosa.py` — 🐛 **misurata da settembre e mai registrata**, trovata dal cancello dei pesi il 2026-09-21: il controllo di copertura guardava che ogni *file* normativo fosse elencato, non che ogni *misura* avesse la sua riga |
| `varieta-fra-archi.md` | **mai due archi di fila** con la stessa tinta dominante | **minore** | 🔴 non misurato — richiede che ogni arco **dichiari** la sua tinta, e nessuno lo fa: è un prerequisito di dato, non di codice |
| `living-world.md` · `quest-design-baldur.md` | nessuna norma numerica: sono repertori di pattern | — non è una norma: sono repertori di pattern, e un repertorio non si viola | ⚪ non applicabile |

## 2 · `rumblingstone-indagine/references/` — il caso

| File | Norma verificabile | Severità | Stato |
|---|---|---|---|
| `nodi-e-sei-porte.md` | **≥3 porte** per nodo, **≥1 fisica** (FOR/DES/COS) | **maggiore** | 🔴 non misurato — i nodi non sono marcati nei moduli; è il gate **I6** del `PIANO-INDAGINE-E-DEDUZIONE`, dichiarato ⬜ e gated su I5 |
| `nodi-e-sei-porte.md` | ogni fatto raggiungibile da **≥2 nodi diversi** | **maggiore** | 🔴 non misurato — stesso prerequisito |
| `congegno-e-enigmi.md` · `famiglie-di-caso.md` | **6-9 nodi** per caso | **minore** | 🔴 non misurato — stesso prerequisito |
| `congegno-e-enigmi.md` | **almeno un congegno per campagna** deve scattare davvero | **minore** | 🔴 non misurato — è un fatto di **gioco**, non di testo: lo sa solo il tavolo |
| `ricomposizione.md` | **mai più di 9** elementi nella ricomposizione | **minore** | 🔴 non misurato — stesso prerequisito dei nodi |
| `registro-e-ricompense.md` | tetto **livello + 3** per abilità di classe; **max +6**; 1 grado per PG per livello (ADR-0022) | **maggiore** | 🔴 non misurato — 🔎 **trovato dal cancello stesso, al primo giro**: avevo scritto «`validate_pg.py`», che **non esiste**. Nessuno script del repo controlla i gradi dei PG |
| `documento-ed-errore-fecondo.md` | box **≤ ~12 righe**, un solo nome proprio | **maggiore** | 🟢 `misura_craft --box` — **stessa norma** di `read-aloud-adulti.md`, ripetuta qui |

## 3 · Skill e ADR normativi fuori dai `references/`

| Dove | Norma verificabile | Stato |
|---|---|---|
| `ADR-0014` §1 | **nessuna sequenza a battute senza regia** (apertura di round, una battuta per attore, esito riuscita **e** fallimento, chiusura) | **maggiore** | 🟢 congegno `regia di round (una battuta per attore)` — e dice che esiste **in un documento solo** |
| `ADR-0014` §2 | **occhio da avventuriero**: scala per paragone, niente metrature nel box | **minore** · `metratura_nella_voce_narrante` | 🟢 `misura_craft --metrature` — **28 box su 477 (6%)**, in 9 file. Cerca la **forma** numero + unità di *spazio* (m · cm · quadretti · °C · Ø), non il numero: «tre round» e «sessanta battiti al minuto» sono legittimi. Falsi positivi **contati a mano: 1 su 28**, un PNG che dice «8-15 km» in un dialogo |
| `rumblingstone-module-standard` §5 | un testo **per i giocatori** porta almeno **un'ancora nominata**: un nome del canone che chi legge riconosca | **maggiore** · `testo_giocatori_senza_ancore` | 🟢 `validate_prosa.py` — 🐛 **stessa storia del trattino**: misurata e mai registrata. 🔎 Nasce da un rilievo del tavolo — la giocatrice di Hella non capiva i suoi echi, e contando le ancore nei quattro testi per-PG della stessa sessione: Tordek 8, Thorik 5, Artemis 4, **Hella 0** |
| `rumblingstone-module-standard` | le 16 sezioni obbligatorie della checklist | **maggiore** | 🟡 `validate_modules.py` — **solo su `ARC*-DEF-*.md`**: 96 file su 100 non sono mai guardati |
| `rumblingstone-module-standard` §8 | sidebar **«Scalare lo scontro»** obbligatoria per i boss | **maggiore** | 🟢 congegno `scalare lo scontro` — e dice **zero** in tutti i 71 file di ARC-08 e ARC-09 |
| `rumblingstone-prosa-documenti` | norme sui **documenti** del repo (non sul contenuto di gioco) | **minore** | 🟢 `validate_prosa.py --documenti` |
| `rumblingstone-editoria` | impaginazione, riquadri, statblocchi in stampa | **maggiore** | 🟢 `validate_booklets.py --stampa` |
| `ADR-0060` (norma WotC/Paizo) | **caratteristiche e abilità maiuscole** nelle quattro forme meccaniche: `Forza 25` · `Nuotare +9` · `prova di X` con una CD · `bonus di X` | **minore** · `caratteristica_minuscola` | 🟢 `validate_prosa.py --caratteristiche` — 258 occorrenze sotto controllo, soglia **zero**, e **fuori dalle quattro forme non si misura** (una frase discorsiva senza CD non si vede: costerebbe più falsi positivi di quanti errori trovi) |
| `read-aloud-adulti.md` + linee guida *Dungeon* | il read-aloud **non presuppone un'azione né un senso del giocatore** | **minore** · `read_aloud_presuppone` | 🟢 `misura_craft --p1` — da **104 box su 477 (22%)** a **22 (5%)** col lotto 2C, e i 22 sono un elenco nominale, non un residuo: 12 dialoghi, 1 canto, 2 visioni interiori, 6 falsi positivi del rilevatore, 1 condizionale. Il cancello è `test_ogni_residuo_e_uno_dei_ventidue_dichiarati`, che àncora il conto **file per file**: un rilievo in più è rosso, e va corretto il testo, non il test. ⚠️ Resta vero che il rilevatore non distingue la **narrazione** dal **dialogo** — per questo il conto atteso non è zero, e non lo sarà mai |
| `ADR-0059` (MQM) | il **punteggio di qualità pesato**: severità 1 / 5 / **25**, soglia per classe, critico pass-fail | — è il metro, non una norma che un documento possa violare | 🟢 `punteggio_mqm.py --soglia` — 515 documenti, soglie da `specifiche-qualita.yaml` misurate con `--distribuzione`. ⚠️ Copre **4 norme su 40**: entra solo ciò che ha già un rilevatore |
| `npc-villain-boosting` | **EL ≤ APL+4**, e oltre il tetto serve un `Boost log:` | **critico** | 🔴 non misurato — il controllo **esiste** (`validate_modules.py --tetto-el`, APL letto da `state.md`) ma **non ha superficie**: la forma `**EL**: [N]` che `AGENTS.md` prescrive ha **zero occorrenze**, e i 150 «EL N» nudi mescolano dichiarazioni e menzioni. Prerequisito: marcare gli incontri |
| `ADR-0060` (norma WotC/Paizo) | le **sigle** di caratteristica — `For 25`, `Des 14`, 688 occorrenze | — non applicabile: le sigle sono maiuscole per costruzione | ⚪ non applicabile — sono maiuscole per costruzione, non c'è niente da controllare |

---

## 4 · Il conto onesto

| | Norme registrate |
|---|---:|
| 🟢 misurate | 22 |
| 🟡 misurate in parte, con il limite scritto | 8 |
| 🔴 **non misurate, con la ragione scritta** | 9 |
| ⚪ non applicabili | 2 |

> 🐛 **Questi quattro numeri erano sbagliati tutti e quattro**, e nessuno se
> n'era accorto perché erano scritti a mano: dicevano **16+9+12+3 = 40** su
> **39** righe vere, e il paragrafo qui sotto parlava di *«undici norme su
> trentaquattro»* — tre numeri, tre verità diverse. Dal lotto **F1.2** il
> confronto lo fa `validate_norme_editoriali.py`, che li conta sulle **righe**
> e non sulle occorrenze delle emoji (prima ne contava **47**, prosa inclusa).

### Le severità — quanto costa violare ciascuna

| Severità | Peso | Quante | Cosa ci finisce |
|---|---:|---:|---|
| **critico** | 25 | **1** | solo `EL ≤ APL+4` senza `Boost log:`. È l'unica norma **di questo registro** che rende un documento ingiocabile: gli altri due critici di ADR-0059 — statblocco inventato, contraddizione con `state.md` — sono norme di **canone**, e il canone qui non ci abita |
| **maggiore** | 5 | **15** | le norme **prescrittive** con una forma o un numero: box ≤ 12 righe, la forma del dialogo, le 16 sezioni obbligatorie, lo spotlight sotto il 40%, le tre porte per nodo |
| **minore** | 1 | **20** | i congegni assenti dove sarebbero serviti e le prassi disattese: `[HDYWTDT]`, i tic dell'IA, la regola Paizo sui read-aloud, le maiuscole di caratteristica |
| — | — | **3** | e la ragione è scritta accanto: due non sono norme che un documento possa violare (i repertori di pattern, il punteggio stesso), una non è applicabile |

⚠️ **Un candidato al critico che non è stato promosso, e perché.** *«Ogni fatto
raggiungibile da ≥2 nodi diversi»* (`nodi-e-sei-porte.md`) è la norma che più
somiglia a un critico: un fatto con una sola fonte è la causa documentata di un
caso che muore in un vicolo cieco. È rimasta **maggiore** perché **nessuno la
misura** — e un pass/fail assoluto appeso a un rilevatore che non esiste è un
pass/fail su niente. Il giorno che i nodi si marcano, la promozione è una riga.

### Severità × misura — la tabella incrociata (F1.2)

Il conto di sopra dice *quante norme sono guardate*. Incrociarlo con la
severità dice una cosa diversa e più utile: **quanto vale quel che nessuno
guarda**.

| | 🟢 misurata | 🟡 in parte | 🔴 per niente | totale | **pesata** |
|---|---:|---:|---:|---:|---:|
| **critico** (25) | — | — | **1** | 1 | 0 |
| **maggiore** (5) | 10 | 3 | 3 | 16 | **3** |
| **minore** (1) | 11 | 5 | 5 | 21 | **9** |
| senza peso | 1 | — | — | 3 *(+2 ⚪)* | — |

🔎 **Tre cose che la tabella dice e le due colonne separate non dicevano.**

1. **L'unico critico è l'unico completamente scoperto.** `EL ≤ APL+4` è la
   norma più cara del registro ed è **🔴**: il controllo esiste
   (`validate_modules --tetto-el`) ma non ha superficie, perché la forma
   `**EL**: [N]` ha zero occorrenze. La severità più alta e la copertura più
   bassa cadono sulla stessa riga.
2. **Le maggiori stanno meglio delle minori**: 9 su 15 sono misurate (60%),
   contro 9 su 20 fra le minori (45%). Non è un caso — le prescrittive hanno
   una forma o un numero, e una forma si cerca. Le prassi no.
3. ~~**Ma il punteggio pesa il bordo, non il centro.**~~ ✅ **Corretto il
   2026-09-21, e la diagnosi era giusta ma la causa era un'altra.** Scritto il
   mattino, quando le norme pesate erano **4** (tre minori e una maggiore) e la
   classe `arco` aveva P10, P25, P50 e P75 tutti a 100,00. La causa non era che
   mancassero i rilevatori: **`validate_prosa` ne misurava sei che nessuno
   contava**. Mancava il *nome* — `controlla()` restituiva stringhe già
   formattate, e contarle per norma avrebbe voluto dire riconoscere la frase
   italiana con cui erano scritte. Adesso le norme pesate sono **11**, di cui
   **3 maggiori**, e la distribuzione ha smesso di dire che va tutto bene: il
   P10 della classe `arco` è sceso da 100,00 a **99,31**, e **41 documenti su
   479** stanno sotto il 99. La coda c'era; il metro non la vedeva.

   ⚠️ **E il cancello dei pesi ha trovato due norme che il registro non aveva
   mai elencato** — il trattino come respiro e l'ancora nei testi per i
   giocatori: misurate da settembre, registrate mai. Il controllo di copertura
   guardava che ogni *file* normativo fosse elencato, non che ogni *misura*
   avesse la sua riga. È ADR-0056 al contrario, e adesso è rosso in CI.

🔎 **Una norma è passata da 🔴 a 🟢, e non perché sia cambiato il repo.** Le
maiuscole di caratteristiche e abilità erano archiviate come non misurabili
dal 2026-09-19 con una ragione che sembrava definitiva: *«in italiano* Forza
*è anche un sostantivo comune»*. Vero del rilevatore, falso della norma.
Cercare la **forma** invece della parola porta 2.014 occorrenze inutilizzabili
a **258 sotto controllo con zero falsi positivi** ([ADR-0060](../plans/adr/ADR-0060-la-forma-rende-misurabile-cio-che-la-parola-non-distingue.md)).
Prima di scrivere «non misurabile», vale la pena cercare la forma.

🔴 **Undici norme su trentanove non sono guardate da niente**, e nove delle undici
hanno la stessa causa: **i moduli non marcano le cose di cui la norma parla**
(i nodi d'indagine, la tinta d'arco, le scene di spotlight). Non è un buco di
codice: è che **la norma presuppone un dato che il testo non porta**. Scrivere
il rilevatore prima di quel dato darebbe un numero finto — ed è esattamente
l'errore che questo registro esiste per non ripetere.

🔎 **E l'undicesima l'ha trovata il cancello, sulla prima stesura di questo
file.** Avevo scritto che il tetto dei gradi di ADR-0022 era presidiato da
`validate_pg.py`: quello script **non esiste**, e nessun altro controlla i
gradi dei PG. È la prova che serviva — un registro scritto a mano mente come
qualunque altra cosa scritta a mano, e per questo i suoi rimandi sono
verificati contro il filesystem.
