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

| File | Norma verificabile | Stato |
|---|---|---|
| `read-aloud-adulti.md` | box **≤ 12 righe** (2-4 per un round, 8-12 apertura, 4-6 rivelazione) | 🟢 `misura_craft --box` |
| `read-aloud-adulti.md` | **un solo nome proprio nuovo** per box | 🟢 `misura_craft --box` |
| `read-aloud-adulti.md` | **niente parentesi né incisi** lunghi | 🟢 `misura_craft --box` |
| `read-aloud-adulti.md` | max **due livelli** di subordinate | 🔴 non misurato — servirebbe un parser sintattico dell'italiano; il segnale povero (contare le virgole) darebbe falsi positivi come i 64/64 di `PIANO-PROSA-CHE-NON-SEMBRI-GENERATA` |
| `read-aloud-adulti.md` | box di combattimento chiude su **«Che fate?»** | 🟢 congegno `chiusura su decision point` |
| `editorial-standards.md` | `**Read-aloud (pilastro lead).**` etichettato | 🟢 congegno `regia etichettata **Read-aloud (X)**` |
| `editorial-standards.md` | `**NOME (registro/tono):** *«battuta»*` | 🟢 congegno `dialogo nella forma dichiarata` |
| `editorial-standards.md` | **la quarta colonna**: un blocco sensoriale chiude con «Cosa NON dire» (ADR-0057) | 🟡 congegno `quarta colonna sensoriale` — conta **chi ce l'ha**, non accusa chi non ce l'ha: non esiste modo automatico di sapere se un blocco *avrebbe dovuto* averla |
| `editorial-standards.md` | terminologia canonica (CD non DC, 5e bandito, metri) | 🟢 `validate_modules.py` §BANNED — ma **solo sui 5 master DEF** |
| `editorial-standards.md` | blockquote **3-10 righe**; max **1-2 MAIUSCOLE** per read-aloud | 🟡 parziale — `--box` usa il tetto **12** di `read-aloud-adulti`; le due fonti non concordano sul minimo e lo script **non sceglie per loro**. Le maiuscole non sono misurate |
| `style-pillars.md` | *fusion rule*: **un lead, max due support** per scena | 🟢 congegno `PILASTRO dichiarato (lead/support)` — conta la marca, non la conformità |
| `style-pillars.md` §Mercer | **`[HDYWTDT]`**: al colpo che uccide un boss la narrazione passa al giocatore, e il marcatore **va scritto** nel testo dell'incontro | 🟢 congegno `[HDYWTDT] il finisher al giocatore` — 🔴 era a **zero in tutti e nove gli archi** |
| `style-pillars.md` §Mercer | **yes-and with teeth**: l'invenzione del giocatore entra nel canone **e** genera una complicazione | 🟡 congegno `assorbi e rilancia (yes-and with teeth)` — conta chi **dichiara** il congegno, non chi lo applica al tavolo: quello lo sa solo il DM |
| `SKILL.md` §Self-check | **sette domande prima di consegnare**, più il controllo di coerenza | 🟡 cinque delle sette hanno un comando (vedi `AGENTS.md` §quarto obbligo); la **4** (numeri di serie) è giudizio puro, e la **2** è un indicatore |
| `pc-protagonism.md` | **nessun PG oltre il 40%** delle scene marcate; **≥1 scena** a testa | 🟡 `misura_craft --spotlight` — indicatore: conta le **menzioni del nome**, non le scene marcate, che il repo non marca |
| `consequence-echoes.md` | **≥1 eco armato** quando la finzione lo consente; **≥2** alla convergenza | 🟡 congegno `eco / conseguenze a distanza` conta le **menzioni**, non gli echi armati e pagati |
| `passate-redazionali.md` | **massimo una chiusa a effetto** per documento; massimo un tricolon | 🟢 `validate_prosa.py --documenti` (lotto D di PROSA-CHE-NON-SEMBRI-GENERATA) |
| `italiano-nativo.md` | almeno una **dislocazione a sinistra** o un **c'è presentativo** | 🔴 non misurato — è una norma *positiva* su costrutti sintattici; il rilevatore andrebbe scritto e provato su un corpus, e non esiste |
| `italiano-nativo.md` §9 | i **tic dell'IA**: antitesi «non X: è Y», tricolon, chiuse a effetto | 🟢 `validate_prosa.py` |
| `varieta-fra-archi.md` | **mai due archi di fila** con la stessa tinta dominante | 🔴 non misurato — richiede che ogni arco **dichiari** la sua tinta, e nessuno lo fa: è un prerequisito di dato, non di codice |
| `living-world.md` · `quest-design-baldur.md` | nessuna norma numerica: sono repertori di pattern | ⚪ non applicabile |

## 2 · `rumblingstone-indagine/references/` — il caso

| File | Norma verificabile | Stato |
|---|---|---|
| `nodi-e-sei-porte.md` | **≥3 porte** per nodo, **≥1 fisica** (FOR/DES/COS) | 🔴 non misurato — i nodi non sono marcati nei moduli; è il gate **I6** del `PIANO-INDAGINE-E-DEDUZIONE`, dichiarato ⬜ e gated su I5 |
| `nodi-e-sei-porte.md` | ogni fatto raggiungibile da **≥2 nodi diversi** | 🔴 non misurato — stesso prerequisito |
| `congegno-e-enigmi.md` · `famiglie-di-caso.md` | **6-9 nodi** per caso | 🔴 non misurato — stesso prerequisito |
| `congegno-e-enigmi.md` | **almeno un congegno per campagna** deve scattare davvero | 🔴 non misurato — è un fatto di **gioco**, non di testo: lo sa solo il tavolo |
| `ricomposizione.md` | **mai più di 9** elementi nella ricomposizione | 🔴 non misurato — stesso prerequisito dei nodi |
| `registro-e-ricompense.md` | tetto **livello + 3** per abilità di classe; **max +6**; 1 grado per PG per livello (ADR-0022) | 🔴 non misurato — 🔎 **trovato dal cancello stesso, al primo giro**: avevo scritto «`validate_pg.py`», che **non esiste**. Nessuno script del repo controlla i gradi dei PG |
| `documento-ed-errore-fecondo.md` | box **≤ ~12 righe**, un solo nome proprio | 🟢 `misura_craft --box` — **stessa norma** di `read-aloud-adulti.md`, ripetuta qui |

## 3 · Skill e ADR normativi fuori dai `references/`

| Dove | Norma verificabile | Stato |
|---|---|---|
| `ADR-0014` §1 | **nessuna sequenza a battute senza regia** (apertura di round, una battuta per attore, esito riuscita **e** fallimento, chiusura) | 🟢 congegno `regia di round (una battuta per attore)` — e dice che esiste **in un documento solo** |
| `ADR-0014` §2 | **occhio da avventuriero**: scala per paragone, niente metrature nel box | 🔴 non misurato — distinguere «grande come una piazza» da «Ø 60 m» dentro un box è fattibile e **non è stato fatto**: candidato naturale al prossimo lotto |
| `rumblingstone-module-standard` | le 16 sezioni obbligatorie della checklist | 🟡 `validate_modules.py` — **solo su `ARC*-DEF-*.md`**: 96 file su 100 non sono mai guardati |
| `rumblingstone-module-standard` §8 | sidebar **«Scalare lo scontro»** obbligatoria per i boss | 🟢 congegno `scalare lo scontro` — e dice **zero** in tutti i 71 file di ARC-08 e ARC-09 |
| `rumblingstone-prosa-documenti` | norme sui **documenti** del repo (non sul contenuto di gioco) | 🟢 `validate_prosa.py --documenti` |
| `rumblingstone-editoria` | impaginazione, riquadri, statblocchi in stampa | 🟢 `validate_booklets.py --stampa` |

---

## 4 · Il conto onesto

| | Norme registrate |
|---|---:|
| 🟢 misurate | 14 |
| 🟡 misurate in parte, con il limite scritto | 8 |
| 🔴 **non misurate, con la ragione scritta** | 11 |
| ⚪ non applicabili | 2 |

🔴 **Undici norme su trentaquattro non sono guardate da niente**, e nove delle undici
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
