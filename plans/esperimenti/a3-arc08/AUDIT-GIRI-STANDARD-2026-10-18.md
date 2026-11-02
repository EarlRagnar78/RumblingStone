# Audit dei giri di ARC-07: cosa è già standard e cosa manca

*2026-10-18, per Jfs. Sola lettura: nel repo non è stato toccato nessun file. Repo
su `origin/main` = `2ee82472` (dopo la #249). Rami letti con `git show`/`git diff`,
senza checkout: #246 (`claude/project-thread-q4s7mw`, `ff8f399d`), #251
(`claude/project-thread-ep4auu`, `43c4f682`), #250 (`87f4485c`, contenuta nella #246).*

Legenda dello stato:
✅ già standard su `main` (file normativo e riga; lo script o il gate se c'è) ·
🟡 su un ramo o una PR non unita ·
🔴 solo nei file di un giro o nella cartella condivisa, non è norma da nessuna parte.

Le ricerche «non c'è» sono `grep -rlnE "<parola>" skills/ plans/adr/ scripts/*.py .github/workflows/`,
con `plans/esperimenti/` escluso. Le parole cercate sono scritte nella riga.

Abbreviazioni dei percorsi:
`G1` = `plans/esperimenti/giro-arc07-2026-10-18/` · `G2` = `plans/esperimenti/giro2-arc07-2026-10-18/` ·
`MS` = `skills/rumblingstone-module-standard/` · `PT` = `skills/rumblingstone-playtest/` ·
`SVI` = `MS/references/sviluppo-degli-incontri.md` · `RAA` = `skills/rumblingstone-narrative-style/references/read-aloud-adulti.md` ·
`REG` = `skills/REGISTRO-NORME-EDITORIALI.md` · `/pf/` = `/mnt/project-files/`.

---

## A · Le pratiche dei giri, una per riga

### A.1 · Il procedimento del giro

| # | Pratica | Dove è nata | Stato | Standard? | Dove andrebbe |
|---|---|---|---|---|---|
| 1 | Tre letture per DEF (developer, playtester, DM a freddo), agenti nuovi, solo master e rubrica | G1 `README.md` r.9-13; G2 `README.md` r.146-150 | ✅ `MS/SKILL.md` r.273 (passo 6) e r.284-288 («Il giro»); `PT/SKILL.md` r.85-93. Nessun gate: lo dice r.276 | già c'è | — |
| 2 | Il lettore a freddo saltato perché il DM ha chiesto tre ruoli | G1 `README.md` r.128-129 | ✅ la regola contraria c'è: il passo 6 vuole quattro letture, e un passo si salta solo con una decisione del DM scritta nel piano (`MS/SKILL.md` r.261-264, ADR-0075 r.49-57) | no: va scritta la decisione, non la pratica | il piano del lotto |
| 3 | Un **correttore** per DEF, distinto da chi orchestra, che unisce i doppi | G1 `README.md` r.14-17; `G1/DEF-*/FIX.md` | ✅ in parte: il triage c'è ma lo fa «chi orchestra» (`MS/SKILL.md` r.289) | sì: separare il triage dai lettori ha retto su 10 master | `MS/SKILL.md` «Il giro», passo 3 |
| 4 | Tre esiti per ogni 🔴/🟠: **corretto** nel master · **al DM** se tocca canone o bilanciamento · **respinto con la riga che lo smentisce** | G1 `README.md` r.14-17; es. G2 `DEF-1/FIX.md` r.24 (EL 13 respinto col conto) | ✅ in parte: `MS/SKILL.md` r.304-306 dà «corretto, residuo con la ragione, o decisione del DM». Il **respinto con la prova** non c'è (`grep "RESPINTO|respinto"`: zero) | sì: «residuo» (vero ma lasciato) e «respinto» (falso) sono due cose, e i giri ne hanno 11 | `MS/SKILL.md` r.304-306; `PT/SKILL.md` §7 |
| 5 | Formato di `FIX.md`: riga d'esiti in testa («CORRETTO n · DECISIONE DM n · RESPINTO n · 🟡 lasciati n»), tabella rilievo/gravità/esito/perché, 🟡 corretti, 🟡 lasciati con la ragione, decisioni in forma di scheda | `G1/DEF-1/FIX.md` r.1-74 | 🔴 `PT/SKILL.md` §7 r.205-217 prescrive i quattro campi della correzione, non il rapporto del correttore | sì, insieme alla 4 | `PT/SKILL.md` §7 |
| 6 | Un **verificatore nuovo** per DEF: rilegge ogni 🔴/🟠 sul master corretto, giudica CHIUSO · PARZIALE · APERTO · IN ATTESA DM, cita il master corretto fra «», e cerca i **NUOVI** errori introdotti dalla correzione | G1 `README.md` r.18-20; `G1/DEF-1/VERIFICA.md` r.1-49 | 🔴 `grep "verificatore"` in skills: zero (le occorrenze in ADR-0061/65/66 e negli script parlano d'altro) | **sì**: ha trovato 14 parziali e 2 🟠 nuovi nel G1, 11 parziali, 1 🟠 e 17 🟡 nuovi nel G2 (es. una tabella senza riga vuota che inghiottiva i PX della Sentinella, `G1/DEF-1/VERIFICA.md` r.45) | `MS/SKILL.md` «Il giro», nuovo passo fra 3 e 4 |
| 7 | La **seconda passata** del correttore su parziali e nuovi | G1 `README.md` r.21-22; `G2/DEF-1/FIX.md` r.200-211 | 🔴 `grep "seconda passata"`: solo `scripts/render_map_blender.py`, d'altro | sì, con la 6 | idem |
| 8 | Le letture servite intere invece che scena per scena | G1 `README.md` r.123-127 | ✅ la norma contraria: il lettore legge due volte, la prima con `lettura_a_scene.py` (`PT/SKILL.md` r.98-103); il DM a freddo legge con `lettura_a_scene.py` (`PT/references/dm-a-freddo.md` r.71-80) | no: la pratica è uno scarto dalla norma, che ha costi (riga 26) | — |
| 9 | Quindici letture partite insieme | G1/G2 `README.md` (lo implicano) | ⚠️ contraddizione su main: `MS/SKILL.md` r.286 dice «in parallelo»; la regola del DM «un subagente alla volta» sta in `plans/PIANO-LETTORE-E-PLAYTESTER.md` r.525 e r.562, ed è stata seguita in `def4-giro4/README.md` r.3-6 e `def5-giro2/README.md` r.3-8 | va decisa una delle due | `MS/SKILL.md` r.286 |
| 10 | Archivio per giro in una cartella con README dei conti | G1, G2 | ✅ `MS/SKILL.md` r.307-308 | già c'è | — |
| 11 | I conti 🔴·🟠·🟡 di giri diversi messi in tabella come misura del miglioramento | G2 `README.md` r.154-163 | ✅ la cautela c'è già nel giro stesso: G1 `README.md` r.26-31 («non si confrontano uno a uno»); ADR-0036 vuole il confronto fra due versioni dello stesso testo | no (vedi C.4) | — |
| 12 | `componenti.py --apparato` lasciato a chi orchestra perché il correttore non tocca altri file | `G1/DEF-1/FIX.md` r.7; `G2/DEF-1/FIX.md` r.211 | ✅ `MS/SKILL.md` r.270, r.335 (`componenti.py --check`, in CI) | già c'è | — |
| 13 | Elenco dei gate verdi a fine correzione | G2 `APPLICATE.md` r.92-107 | ✅ `scripts/gate_locale.py` legge il job `validate` di `ci.yml` | già c'è: basta usare quello invece della lista a mano | — |

### A.2 · Le domande dei lettori

| # | Pratica | Dove è nata | Stato | Standard? | Dove andrebbe |
|---|---|---|---|---|---|
| 14 | Le domande dell'alto livello: segreto e divinazione, riga di scala, orde, «salva o sei fuori», mostro insostituibile, pericolo usato, incontro che resta uno, rinforzo visibile | `G2/DEF-4/DEVELOPER.md` (#6, #10); `RICERCA-AVVENTURE-COMMUNITY` | ✅ `SVI` §9-§16 r.186-292; ADR-0092 (accettata); `REG` r.130; `domande_developer.py --check` in CI (`ci.yml` r.171) per D9, D10, D15, D16 | già c'è | — |
| 15 | Il blocco **«Se lo divinano»**, una riga per segreto, completato dove mancava (G2-18, G2-27) | G2 `DECISIONI-DM.md` r.307; `APPLICATE.md` r.50, r.59 | ✅ `SVI` r.194-203; D9 di `domande_developer.py` (vede che c'è, non che copra ogni segreto: `REG` r.130) | già c'è | — |
| 16 | **Righe di scala** per tre e cinque PG nel duello (DEV#6) e in DEF-5 (G2-39) | `G2/DEF-4/VERIFICA.md` riga DEV#6; G2 `APPLICATE.md` r.71 | ✅ `SVI` §10 r.207-219; D10 | già c'è | — |
| 17 | La riga di scala deve dire **in quale riga cade il gruppo di stasera** (le wyvern: il gruppo di 13° è «straripante»?) | `G2/DEF-4/DM.md` #7; `PLAYTESTER.md` #12; `DEVELOPER.md` #20 | 🔴 `SVI` §10 chiede tre e cinque PG, non quale riga vale per il tavolo vivo | sì: tre lettori su tre l'hanno trovata | `SVI` §10, una frase |
| 18 | **Ogni creatura che il modulo mette sotto attacco ha CA e pf**, anche un alleato (Re Thorek bersaglio del drago; Vatore; la CA del re in DEF-5, l'unico bersaglio, 🔴) | `G2/DEF-4/DEVELOPER.md` #4, `PLAYTESTER.md` #1, `DM.md` #17; G2 `README.md` r.173-174 | 🔴 `SVI` §8 chiede la tattica di chi combatte, non le statistiche di chi viene colpito | sì: un 🔴 e cinque 🟠 nel G2 | `SVI` §8, un capoverso; misurabile in parte da `domande_developer.py` |
| 19 | **I sensi dei nemici contro il piano dei PG**: scurovisione contro il buio della tenda (🔴 in due lettori), percezione tremorica contro l'imboscata, olfatto dei lupi | `G2/DEF-4/DEVELOPER.md` #1, `DM.md` #5; `G1/DEF-1/FIX.md` r.24 | 🔴 `SVI` §2 chiede «e se volano, se sono invisibili, se sono silenziosi», non «chi vede al buio» | sì: è il tipo di 🔴 che il G2 ha trovato col solo SRD in mano | `SVI` §2, una riga |
| 20 | Economia d'azione SRD dei mostri (gli Xorn che emergono, mordono e si rituffano nello stesso turno, 🔴 in tre lettori; Terros con due azioni standard) | G2 `README.md` r.169-170; `G1/DEF-1/FIX.md` r.16 | 🔴 nessuna domanda di `SVI` la chiede | sì, come voce del codice V-N (riga 23) | `SVI`, voce nuova o nota al §8 |
| 21 | Le otto domande usate dal G1 mentre su main ne valevano sedici | `G1/DEF-1/DEVELOPER.md` r.5; `G2/DEF-1/DM.md` («Le otto domande») | ✅ la rubrica giusta è `SVI` r.6-21 | no: è un difetto del prompt d'invio, non una pratica | — |
| 22 | Il developer nomina **codici suoi**, perché la rubrica non li fissa: V-1…V-8, più V-N (numero o regola contro l'SRD), V-C (due punti che si contraddicono), V-X (dato in un file esterno) | `G1/DEF-1/DEVELOPER.md` r.5 («la rubrica non ne fissa»); `G1/DEF-5/DEVELOPER.md` r.5 | 🔴 `PT/SKILL.md` r.92 dice «con i codici `V-`», ma `SVI` non li definisce (`grep "\`V-"` in skills: solo quella riga). Nei 10 rapporti del developer i codici sono `§8`, `V-8`, `regola`, `regola SRD`, `numeri`, `contraddizione`, `n/a` | **sì**: oggi i rapporti non si aggregano | `SVI`, una tabella dei codici e la riga d'uscita come in `PT/references/playtester-a-freddo.md` r.45-56 |
| 23 | La categoria più numerosa del developer è «regola o numero contro l'SRD» (31 righe fra `regola`, `regola SRD`, `numeri`, `contraddizione`) | conteggio sulla colonna Codice dei 10 `DEVELOPER.md` | 🔴 manca come codice (vedi 22); `P-RISORSA` del playtester la copre per durate e distanze (`playtester-a-freddo.md` r.35) | sì, con la 22 | idem |
| 24 | DM a freddo: primo passo (vista), secondo (preparazione con tempo dichiarato e «chi parla per primo»), terzo (il giorno dopo) | `G2/DEF-4/DM.md` r.24-60 | ✅ primo passo obbligatorio (`PT/references/dm-a-freddo.md` r.33-36); secondo e terzo «in prova» (r.28-40) | già c'è; i dieci rapporti del 10-18 sono materiale per farli uscire dalla prova | `dm-a-freddo.md` r.28-40 |
| 25 | Il **tempo di preparazione calcolato in minuti** dalle parole della lista di lettura («il master chiede circa 92 minuti», «66 minuti») | `G2/DEF-3/DM.md` r.43; `G2/DEF-5/DM.md` r.36; `G2/DEF-1/FIX.md` r.206 (script del correttore, non salvato) | 🔴 `dm-a-freddo.md` r.74-75 chiede di dichiarare il tempo, non di stimarlo | forse: è un numero che si conta, ed è il rilievo D-TEMPO più frequente | `dm-a-freddo.md` secondo passo; il conto in `vista_di_chi_scorre.py` |
| 26 | Terzo passo fatto dallo stesso agente sul suo diario | `G2/DEF-4/DM.md` r.65 | ✅ la norma contraria: «con un agente nuovo» (`dm-a-freddo.md` r.119) | no | — |
| 27 | Sezione «Regole controllate e trovate giuste» / «Le domande che reggono» in coda al rapporto | `G2/DEF-3/DM.md` r.68; `G2/DEF-5/DEVELOPER.md` r.25; `G2/DEF-1/DEVELOPER.md` r.31 | ✅ per le mappe soltanto: la riga «Verificato senza rilievi» di `skills/rumblingstone-mapmaking/references/collaudo-mappe.md` r.172-174. Nelle rubriche dei lettori c'è solo «cosa non ha potuto verificare» (`lettore-a-freddo.md` r.156) | sì: distingue il silenzio dal controllo saltato, come per le mappe | le tre rubriche di `PT/references/` e `SVI` |
| 28 | Lettori con i **mirror dell'SRD 3.5**, che citano l'URL nella prova (anche con `oldid`) | G2 `README.md` r.149-150, r.176; `G2/DEF-4/DM.md` #5 | 🔴 `grep "birthright|rpgcrossing"`: zero. `skills/RULES-VERIFICATION.md` r.7-12 nomina solo d20srd.org e aonprd | sì, con la 29 | `skills/RULES-VERIFICATION.md`; `skills/dnd-35-srd/references/resources.md` |

### A.3 · I numeri contro l'SRD

| # | Pratica | Dove è nata | Stato | Standard? | Dove andrebbe |
|---|---|---|---|---|---|
| 29 | **Verifica dei numeri dei master contro l'SRD** su mirror raggiungibili (D&D Wiki fandom, birthright.net, rpgcrossing.com, legacy.aonprd.com), con una tabella voce · file:riga · cosa dice il master · cosa dice la pagina (URL) · esito · correzione | G1 `VERIFICA-SRD.md` r.1-139 (≈40 voci confermate, 9 discrepanze) | 🔴 per i master. `skills/RULES-VERIFICATION.md` r.1-5 copre «every hard number in `skills/` and in the scripts», non i master | **sì** | `skills/RULES-VERIFICATION.md`, una sezione «master»; il passo 4 del ciclo (`MS/SKILL.md` r.271) |
| 30 | Il **criterio della discrepanza**: conta solo se il master attribuisce il numero all'SRD e l'SRD dice altro, o se il conto è sbagliato; `⚠ Non SRD`, `[CANONE — DM …]` e `Boost log` sono scelte dichiarate | G1 `VERIFICA-SRD.md` r.13 | 🔴 non scritto altrove | sì: evita di «correggere» le scelte del DM | idem |
| 31 | **Aritmetica degli statblocchi dentro i master** (Terros CA 26 con DES 8 → 25; Durin Vol +3 → +4; Fauci +22 nella regia contro +29 nello statblocco) | G1 `VERIFICA-SRD.md` r.61, r.65, r.84; riassunto r.89-97 | ✅ in parte: `scripts/conformita_statblocchi.py` fa questi conti (in CI, `ci.yml` r.143), ma legge solo `Bestiario/**/*-cr*.md` (r.341, 500, 523, 555). Gli statblocchi scritti nel master non li vede | **sì**: sei delle nove discrepanze erano aritmetica o coerenza interna | `conformita_statblocchi.py`, opzione sui master; oppure lo statblocco nel Bestiario con l'include di ADR-0074 (`MS/SKILL.md` r.335) |
| 32 | Una copia **locale** dell'SRD 3.5 in markdown (`olimot/srd-v3.5-md`, OGL 1.0a, 7,4 MB) | `/pf/corpus-prosa/grezzi/test-srd/srd-v3.5-md/` (`/pf/corpus-prosa/RAPPORTO.md` r.73) | 🔴 non è nel repo, e `RULES-VERIFICATION.md` r.7-8 dice che le fonti di verifica «not committed, kept outside the repo» (scelta del DM, 2026-07-03) | sì, ma la decide il DM | `RULES-VERIFICATION.md`; la copia contiene `Goods and Services` (`equipment.md`), il tipo Elementale e i bonus agli incantesimi, cioè voci che G1 `VERIFICA-SRD.md` r.101-109 dava per non verificabili |
| 33 | La lista di ciò che **non si è potuto verificare**, con le pagine cadute (429, errori) | G1 `VERIFICA-SRD.md` r.99-112 | ✅ la forma c'è nelle rubriche («cosa non ha potuto verificare», `lettore-a-freddo.md` r.156) | già c'è | — |

### A.4 · Le decisioni del DM

| # | Pratica | Dove è nata | Stato | Standard? | Dove andrebbe |
|---|---|---|---|---|---|
| 34 | Scheda di decisione: domanda · tabella opzione/conseguenza · **Raccomandata** con il perché; i fatti che sa solo il DM con un ripiego | G1 `DECISIONI-DM.md` r.1-20; `G1/DEF-1/FIX.md` r.76-88 | ✅ in parte: `skills/rumblingstone-plans/SKILL.md` r.43-46 vuole la riga marcata `<!-- decisioni-dm: … -->` nel piano; la forma della scheda non è scritta | forse: la forma ha funzionato, basta un esempio | `skills/rumblingstone-plans/SKILL.md` |
| 35 | Le decisioni dei giri **fuori dal cruscotto**: 29 del G1 e 55 del G2 vivono in `plans/esperimenti/*/DECISIONI-DM.md`, senza marker | G1, G2 `DECISIONI-DM.md` | ✅ la regola c'è (`rumblingstone-plans/SKILL.md` r.43-46), ma non è applicata, e `scripts/decisioni_dm.py` r.80 legge solo `plans/*.md`. `MEMORIA.md` e `STATO-E-ORDINE` non vedono nessun `G2-` | **sì**: oggi 55 decisioni aperte sono invisibili al cruscotto | la tabella marcata in `PIANO-MASTER-DEF`, o `decisioni_dm.py` che legge anche le `DECISIONI-DM.md` degli esperimenti |
| 36 | La raccomandata segue «la versione più forte e terrificante», con una lettura scritta: vince la più dura che **non contraddice un `[CANONE]`, il canone giocato o `state.md`, e lascia viva la meccanica** | G1 `DECISIONI-DM.md` r.3; G2 `DECISIONI-DM.md` r.17 | ✅ in parte: la regola del DM è in ADR-0091 §4-bis r.135-144, per le **schede** dei PNG. Per le decisioni aperte no | sì: la lettura del G2 è più precisa della regola e ha evitato tre meccaniche impossibili (G2-33, G2-41, G2-42) | `rumblingstone-plans/SKILL.md`, accanto alla 34; o ADR-0091 |
| 37 | **Il canone giocato del ramo di gruppo** prima di chiedere al DM: `origin/campaign-group-rumblingstone` (`state.md`, `state.yaml`, il diario della sessione 4). Ha chiuso 3 decisioni, ne ha aperte 3, e ha corretto la fonte di un rifiuto che citava lo `state.md` di main | G2 `DECISIONI-DM.md` r.7-9, r.23-50 | 🔴 ADR-0090 crea il ramo, ADR-0007 dice dove si scrive; nessuna norma dice «controlla il ramo prima di decidere o respingere». La regola 7 di `AGENTS.md` manda a `campaign/state.md`, che su main è indietro per scelta | **sì** | `MS/SKILL.md` «Il giro», passo 3 «manca canone»; `skills/rumblingstone-campaign/references/campaign-coherence.md` |
| 38 | Correzioni dal canone giocato marcate `[CANONE GIOCATO 2026-09-25]` dentro `<!-- storico -->` (K1-K4) | G2 `DECISIONI-DM.md` r.29-36 | ✅ ADR-0013 r.129 e r.211 (`✅ CANONE GIOCATO (DM data)`), ADR-0069 per lo storico che non va in stampa | già c'è (forma leggermente diversa) | — |
| 39 | Il tag **`[CANONE — DM data, G2-NN]`**: il codice della decisione nel tag, così ogni decisione applicata si trova e si annulla con `grep -n "G2-NN"` (80 tag nei master) | G2 `APPLICATE.md` r.5-8, r.27 | ✅ il marcatore `[CANONE — DM data]`: ADR-0069 r.21 e r.53, `skills/rumblingstone-editoria/SKILL.md` r.183 e r.196; `export_booklet_typst.py` r.448 lo toglie dalla stampa. 🔴 il codice dentro il tag: `grep "G2-"` trova solo `REGOLE-DORO.md` e `validate_state.py`, d'altro | sì: costa due caratteri e rende reversibile ogni decisione | ADR-0069 o `editoria/SKILL.md` r.196 |
| 40 | Raccomandate **applicate in bozza prima della risposta del DM** | G2 `APPLICATE.md` r.5 («Il DM non ha ancora risposto alla scheda»); commit `9bff7044` | ✅ la regola contraria: «manca canone → decisione nel piano e `[INFERRED]`. Non si inventa» (`MS/SKILL.md` r.301-303) | no (vedi C.2) | — |
| 41 | Il conto degli `[INFERRED` prima e dopo, per file | G2 `APPLICATE.md` r.12-27 | ✅ in parte: `validate_modules.py` e i piani contano gli INFERRED (es. `STATO-E-ORDINE` r.58, «51 marcature a zero»); nessun gate | già c'è come pratica | — |
| 42 | Patch di `state.md` consegnata come file, da applicare a mano sul ramo di gruppo | `/pf/giro-arc07-2026-10-18/PATCH-STATE-MD.md` | ✅ ADR-0007; regola 10 di `AGENTS.md` (proposta stampata che il DM applica) | già c'è | — |

### A.5 · Misure, prosa e voto cieco

| # | Pratica | Dove è nata | Stato | Standard? | Dove andrebbe |
|---|---|---|---|---|---|
| 43 | Box al metro: ≤12 righe, un nome nuovo, niente parentesi | G1 `README.md` r.91-104; G2 `README.md` r.204-213 | ✅ `RAA` §2 r.75-89, §7 r.222-239; `misura_craft.py --box` (non in CI: `MS/SKILL.md` r.272) | già c'è | — |
| 44 | **Misure prima e dopo con un tag** (`prima-rifacimento-arc07`), stessi comandi, uscite salvate in `misure/` | G2 `README.md` r.199-241 | ✅ il principio: ADR-0036 («si misura la differenza fra due versioni»). 🔴 la pratica del tag: il tag **non esiste** su `origin` (`git ls-remote --tags`: 9 tag, tutti `archivio/…`); il commit `503c9fde` c'è | sì, ma con il tag spinto e il comando scritto in testa a ogni file di misura | `skills/rumblingstone-playtest/SKILL.md` §5, o ADR-0036 |
| 45 | `box_metri`: parole per box, sensi per box, «telecomando», parole ripetute entro 20 | `/pf/avventure-community/note-di-ricerca/box_metri.py`; `G2/misure/BOX-METRI-VARIANZA.txt` | 🔴 lo script sta solo nella cartella condivisa. Una parte entra con la #246: i sensi (`misura_craft --stile`, colonna `sens.`, `dettagli_sensoriali()` r.571) e il «telecomando» è già P1 di `misura_craft` su main (r.449) | in parte (le ripetizioni no: C.3) | `misura_craft --stile`, del thread della #246 |
| 46 | **La varianza delle lunghezze dal corpus**: i box rifatti erano troppo regolari (88% fra 30 e 70 parole contro il 47% umano); un passaggio per master ha accorciato i box d'urto e unito le battute sullo stesso luogo | G2 `README.md` r.264-292; il DM ha approvato «di adottare le misure del corpus» (r.269-270) | 🔴 nessuna norma: `grep "varianza"` trova ADR-0036, `lettore-a-freddo.md`, `italiano-nativo.md`, `validate_prosa.py`, nessuno sulle parole per box. Le fonti dei numeri sono sulla #246 (`note-prosa-corpus.md` r.53, r.82) | forse: come indicatore, non come soglia | `RAA` §2, una riga d'indicatore registrata in `REG` |
| 47 | Il **voto cieco del DM** su un campione congelato prima di riscrivere, con la soglia riproporzionata alle coppie non identiche (12 su 16) | G2 `README.md` r.243-262; `/pf/giro2-arc07-2026-10-18/SCHEDA-CIECA.md`, `CHIAVE-NON-APRIRE-PRIMA-DEI-VOTI.json` | 🟡 #246: ADR-0093 (stato «proposta»), cieco_versioni.py (sulla #246), la cartella prosa-cieco. L'esito sulla #251: `G2/misure/CIECO-*` | sì: è l'unica misura che ha detto «non meglio» dove i numeri dicevano «meglio» | resta alla #246 |
| 48 | **Le due preferenze di Jfs dal cieco**: una riscrittura non toglie dettagli sensoriali; un monologo resta un blocco | ESITO sulla #246 (ESITO-ARC07-2026-10-18.md della cartella prosa-cieco (sulla #246)) | 🟡 #246: `RAA` §2-ter e due righe in `REG`, misurate da `cieco_versioni.py coppie` e `ciclo_prosa misura` | sì | resta alla #246 |
| 49 | **La terza preferenza**: i nomi che il tavolo conosce da archi interi non diventano perifrasi per stare sotto il tetto di un nome nuovo (Moradin → «il dio dei nani» ha perso la coppia 5) | #251, `G2/README.md` nel diff, sezione «L'esito» | 🔴 come norma: `RAA` r.41 dice «nuovo», ma `misura_craft.py` conta i nomi **distinti** (r.307-312 lo dichiara), e il rifacimento ha inseguito l'indicatore | **sì** | `RAA` §2-ter (file della #246) o §1 r.41; l'etichetta `>1 nome` di `misura_craft --box` |
| 50 | **I 26 box impoveriti** di ARC-07 (sensi tolti, monologhi spezzati in 3-8 battute) | `/pf/giro2-arc07-2026-10-18/BOX-IMPOVERITI-2026-10-18.md`; prodotti da `ciclo_prosa.box_impoveriti` della #246 | 🟡 la #251 rimette **le otto coppie del cieco** (2, 3, 4, 5, 9, 12, 16, 20), che coprono circa sei voci dell'elenco. Le altre restano come sono | sì, ma è lavoro, non norma | resta al thread della #251 |
| 51 | Chiusure su domanda sopra il corpus (21% contro 6,5%), lasciate perché ADR-0014 le vuole sui box di combattimento e di scelta | G2 `README.md` r.284-288 | ✅ ADR-0014; `RAA` §7 r.237; congegno `chiusura su decision point` (`REG` r.42) | già c'è | — |
| 52 | Gerundi in coda e avverbi in -mente letti contro una **fascia umana**, non contro lo zero | `/pf/corpus-prosa/RAPPORTO.md` §4.3 p.4 e §6; ADR-0093 punto 2 | 🟡 #246 (`misura_craft --stile`, fascia del Gruppo Chimera) | sì | resta alla #246 |
| 53 | MQM prima e dopo | G2 `README.md` r.227-228 | ✅ `scripts/punteggio_mqm.py` | già c'è; ma è saturo (C.5) | — |
| 54 | Etichette di provenienza nelle ricerche: LETTO / INDICE / DEDOTTO, [letto] / [inferenza] / [misurato] | `/pf/archivi-wizards/ARCHIVI-WIZARDS-E-PF1E-2026-10-18.md` r.7-9; `/pf/corpus-prosa/RAPPORTO.md` r.5; `/pf/avventure-community/ANALISI-…` r.5 | 🔴 `grep "DEDOTTO|\[letto\]|\[inferenza\]"` in skills e ADR: zero. C'è l'equivalente per il gioco, `[INFERRED — needs DM confirmation]` (regola 5 di `AGENTS.md`) | forse: utile per le ricerche, non per i master | `skills/rumblingstone-prosa-documenti/` o `rumblingstone-plans/SKILL.md` (piani di ricerca) |

### A.6 · Mappe

| # | Pratica | Dove è nata | Stato | Standard? | Dove andrebbe |
|---|---|---|---|---|---|
| 55 | Il **collaudatore mappe a freddo** con i quattro materiali e le tre viste | `plans/esperimenti/collaudo-mappe-2026-10/COLLAUDATORE-M7C-2026-10-09.md` | ✅ `skills/rumblingstone-mapmaking/references/collaudo-mappe.md` r.102-191; ADR-0082. ⚠️ r.181 dice ancora che il ruolo «non ha ancora prodotto un rapporto vero», ma il rapporto del 2026-10-09 c'è | già c'è; va corretta la r.181 | `collaudo-mappe.md` r.181 |
| 56 | I giri di ARC-07 **non hanno chiamato il collaudatore**, anche dove hanno cambiato legende (M7-C, T-2, T-5, T-6, S-1, CM-1) | `grep -rln "collaudatore|collaudo_mappe|M-POSIZIONI"` su G1 e G2: zero | ✅ in parte: il giro completo delle mappe (`collaudo-mappe.md` r.183-191) esiste, ma il giro dei master non lo richiama | sì | `MS/SKILL.md` «Il giro», passo 3: se una correzione tocca una legenda, passi 2-4 di `collaudo-mappe.md` |
| 57 | **L'allineamento Atlante ↔ master**: le mappe del master sono copie dell'Atlante, il correttore non può toccare l'Atlante, e le due copie divergono (T-4 nel G1; T-1 e T-3 con la runa di Varis; Xorn, «LETALI» e zero-G nel G2, NUOVO 1 🟠) | `G1/DEF-1/FIX.md` r.31, r.48, r.72; `G2/DEF-1/FIX.md` r.17, r.207; G2 `README.md` r.143-144 | 🔴 nessuno script confronta le due copie (`grep "MAPPE-DEFINITIVO|Atlante"` negli script: solo `build_monster_catalog.py`, `extract_scene_prompts.py`, `validate_corredo.py`, che non lo fanno). In `ARC07-DEF-1` la T-4 è a r.2924, nell'Atlante a r.202, senza `<!-- include -->` (i master di ARC-07 hanno un solo include in tutto, in DEF-4) | **sì**: è il difetto che torna in ogni giro | l'include di ADR-0074 per le mappe (`componenti.py`), o un controllo in `validate_maps.py` |
| 58 | La legenda di una mappa allineata al master e la griglia lasciata com'è, quando una decisione cambia una posizione (CM-1, G2-32; S-1, G2-09) | G2 `APPLICATE.md` r.42, r.64 | ✅ `collaudo-mappe.md` vista del DM: «le posizioni della griglia sono quelle del testo della scena» (r.120-121) | già c'è | — |

---

## B · Le lacune vere, in ordine di utilità

Le prime sette sono di questo repo e non toccano i rami altrui. L'ottava e la
nona sono dei thread della #246 e della #251: si segnalano, non si portano.

### B.1 · Il verificatore e la seconda passata entrano nel giro (righe 3-7)

**Cosa si aggiunge.** In `MS/SKILL.md`, «Il giro», fra il passo 3 e il 4:
un correttore per master con tre esiti (corretto · al DM · respinto con la riga
che lo smentisce, distinto dal residuo vero lasciato con la ragione); poi un
**verificatore nuovo** che giudica ogni 🔴/🟠 sul master corretto (CHIUSO ·
PARZIALE · APERTO · IN ATTESA DM, con la citazione fra «») e cerca i NUOVI
errori della correzione; poi la **seconda passata** del correttore sui parziali
e sui nuovi. La forma di `FIX.md` e di `VERIFICA.md` va in `PT/SKILL.md` §7,
che oggi descrive solo la riga di correzione.

**Perché.** Il verificatore ha trovato 14 parziali e 2 🟠 nuovi nel primo giro,
11 parziali, un 🟠 e 17 🟡 nuovi nel secondo. Senza di lui quei parziali
sarebbero stati contati come corretti.

**Misura (G3).** Una riga in `REG`: «ogni 🔴/🟠 di un giro ha un esito in `FIX.md`
e un giudizio in `VERIFICA.md`». Si misura contando le righe delle due tabelle:
un controllo nuovo di poche righe in `registro_letture.py` (che già legge le
tabelle dei rilievi, `rilievi_dal_rapporto` r.140), o, se non si scrive, 🔴 con
la ragione «le tabelle dei giri non hanno ancora una forma fissa».

### B.2 · I numeri dei master si verificano contro l'SRD, e l'aritmetica la fa uno script (righe 28-32)

**Cosa si aggiunge.**
1. In `skills/RULES-VERIFICATION.md` una sezione per i master: il criterio della
   discrepanza di `G1/VERIFICA-SRD.md` r.13, i mirror che rispondono (fandom,
   birthright, rpgcrossing, legacy.aonprd) e la tabella voce/file:riga/URL/esito.
2. `conformita_statblocchi.py` legge anche gli statblocchi scritti nei master,
   oppure ogni statblocco del master sta nel Bestiario e ci arriva con l'include
   di ADR-0074. Sei delle nove discrepanze del G1 (CA di Terros, Volontà di
   Durin, morso di Fauci nella regia) le avrebbe trovate lo script.
3. La copia locale dell'SRD in markdown (`olimot/srd-v3.5-md`, OGL 1.0a) **è una
   decisione del DM**: `RULES-VERIFICATION.md` r.7-8 tiene fuori dal repo le
   fonti di verifica dal 2026-07-03. Le alternative: la copia in `asset-esterni/`
   fuori da git con un comando di `dm.py doctor` che la scarica da GitHub (che il
   proxy lascia passare, `/pf/corpus-prosa/RAPPORTO.md` r.11), oppure nel repo
   dopo il gate di `rumblingstone-edizione`. Coprirebbe voci che il G1 non ha
   potuto verificare (servizi d'incantesimo, tipo Elementale, bonus agli
   incantesimi).

**Misura.** `conformita_statblocchi.py --check` esteso, già in CI (`ci.yml` r.143).
In `REG` la riga «lo statblocco di un master torna con le caratteristiche».

### B.3 · Il developer ha codici fissi e quattro domande nuove (righe 17-23)

**Cosa si aggiunge** in `SVI`:
- la tabella dei codici `V-1`…`V-16` più `V-N` (numero o regola contro l'SRD),
  `V-C` (due punti che si contraddicono), `V-X` (dato fuori dal file), e la riga
  d'uscita `| # | Scena | Codice | Cosa manca | Gravità | Prova |`. Oggi
  `PT/SKILL.md` r.92 cita i codici `V-` che `SVI` non definisce, e ogni developer
  li inventa;
- §2: «chi vede al buio, chi sente sotto terra, chi fiuta», contro il piano dei PG;
- §8: ogni creatura che il modulo mette sotto attacco, alleati compresi, ha CA e
  pf (o la soglia a colpi, come la decisione G2-08);
- §10: la riga di scala dice in quale riga cade il gruppo di stasera;
- §8 o voce nuova: l'economia d'azione SRD dei mostri (emergere, attaccare,
  rituffarsi).

**Misura.** I codici si contano nei rapporti (stesso controllo della B.1). Delle
domande, la CA del bersaglio è la più vicina a una forma («bersaglio» o «va su
di lui» senza «CA» nella stessa scena): candidata per `domande_developer.py`,
da calibrare come D10 (ADR-0092, Conseguenze). Le altre tre restano alla
lettura, dichiarate 🔴 con la ragione in `REG`, come le §11-§14.

### B.4 · L'Atlante e il master hanno una mappa sola (righe 55-57)

**Cosa si aggiunge.** Le mappe del master entrano dall'Atlante con
`<!-- include: Mappe/ARC07-MAPPE-DEFINITIVO.md#T-4 -->` (il meccanismo di
`componenti.py`, ADR-0074, che oggi copia gli statblocchi). Dove non si può,
un controllo in `validate_maps.py` o in `collaudo_mappe.py` che confronta griglia
e legenda di due mappe con lo stesso titolo. In `MS/SKILL.md` «Il giro», passo 3:
una correzione che tocca una legenda passa dal collaudo delle mappe
(`collaudo-mappe.md` r.183-191). E va corretta la r.181 di `collaudo-mappe.md`.

**Misura.** `componenti.py --check` (in CI) se si usa l'include; altrimenti il
controllo nuovo, con una riga in `REG` («una mappa ha una copia sola, o le copie
coincidono»).

### B.5 · Le decisioni dei giri entrano nel cruscotto, col codice nel tag (righe 34-36, 39)

**Cosa si aggiunge.** Le 55 decisioni del G2 nella tabella marcata
`<!-- decisioni-dm: … -->` di un piano (PIANO-MASTER-DEF, che possiede i DEF),
come chiede già `rumblingstone-plans/SKILL.md` r.43-46; oppure
`decisioni_dm.py` che legge anche `plans/esperimenti/**/DECISIONI-DM.md` (oggi
r.80 legge solo `plans/*.md`). In `rumblingstone-plans/SKILL.md`: la forma della
scheda (domanda, opzioni con conseguenza, raccomandata col perché) e la lettura
della regola del DM di G2 `DECISIONI-DM.md` r.17. In ADR-0069 o
`editoria/SKILL.md` r.196: il codice della decisione dentro `[CANONE — DM data, Gn-NN]`.

**Misura.** `decisioni_dm.py --check` ed `eco_decisioni.py --check`, già in CI
(`ci.yml` r.97). Che il tag col codice esca dalla stampa come oggi
(`export_booklet_typst.py` r.448, `togli_storico` in `build_booklet_html.py` r.347)
va provato con un test: `APPLICATE.md` r.8 lo afferma, io non l'ho verificato.

### B.6 · Il canone giocato si legge dal ramo di gruppo (riga 37)

**Cosa si aggiunge.** In `MS/SKILL.md` «Il giro», passo 3 («manca canone»), e in
`campaign-coherence.md`: prima di mandare una domanda al DM o di respingere un
rilievo citando lo stato, si legge il ramo di gruppo
(`git show origin/campaign-group-<nome>:campaign/state.yaml` e i diari). Nel G2
ha chiuso tre decisioni, ne ha aperte tre, e ha mostrato che un rifiuto
corretto citava la fonte sbagliata (`state.md` di main).

**Misura.** 🔴 non misurato, con la ragione: il ramo di gruppo può mancare nel
clone, e un gate non lo può pretendere. Una via: il passo 3 di `fase1.py`
(regola G6 di `AGENTS.md`) stampa l'ultima sessione del ramo, se c'è.

### B.7 · Il registro delle letture vede anche le letture intere e il developer (riga 8)

**Cosa si aggiunge.** `registro_letture.py --registra` vuole una corsa di
`lettura_a_scene.py` con `stato.json` (r.146, r.177-179) e conosce tre ruoli
(lettore, playtester, dm). Le 30 letture del 10-18 non ci entrano, e tutti e
cinque i DEF restano in avviso («il dm ha letto un testo che non c'è più»).
Due aggiunte: `--intero --impronta <sha256 del master letto>` per una lettura sul
file intero, e il ruolo `developer`.

**Misura.** Lo stesso `registro_letture.py --check`, in CI (`ci.yml` r.80).
⚠️ La lettura intera è un ripiego: la norma resta quella a scene (riga 8), e il
registro deve dire quale delle due è.

### B.8 · Da segnalare al thread della #251

- La #251 rimette le otto versioni vecchie che hanno vinto il cieco. Le altre
  voci di `/pf/giro2-arc07-2026-10-18/BOX-IMPOVERITI-2026-10-18.md` (circa
  venti su 26: DEF-1 Zone 1, 7a, A5; DEF-3 Scene 2, 5, 6 e il blocco «Come lo
  chiede Moradin» spezzato in 4 e 8 battute; DEF-4 Scene 4, 11 e la fucina)
  restano impoverite. `cieco_versioni.py coppie` della #246 le deciderebbe da
  sé o le manderebbe al cieco.
- La terza preferenza (riga 49) sta solo nel README del giro, nel diff della #251:
  per diventare norma serve una riga in `RAA`.

### B.9 · Da segnalare al thread della #246

- Il «nuovo» del tetto dei nomi (riga 49): `misura_craft` conta i distinti, e il
  rifacimento li ha tolti. Un'etichetta più onesta della colonna (`nomi distinti`)
  e una frase in §2-ter.
- La varianza delle lunghezze (riga 46) è approvata dal DM ma non è norma, e i
  suoi numeri stanno sulla #246. Se entra, entra come indicatore di `--stile`,
  non come soglia: ADR-0036 vieta le soglie assolute sulla prosa di gioco, e
  ADR-0093 fa decidere il cieco.
- L'appaiamento di `cieco_versioni.py` sui box spezzati (G2 `README.md` r.253-259)
  risulta già corretto sulla #246 (ESITO, «Il voto cieco»).

---

## C · Cosa non conviene rendere standard

1. **Le letture sul master intero al posto di quelle a scene** (riga 8). Costano
   la registrazione (B.7), la prova `L-ORDINE` e il diario del passo 7. Erano un
   ripiego.
2. **Applicare le raccomandate prima che il DM risponda** (riga 40). Il codice
   `G2-NN` le rende reversibili, ma la regola del triage (`MS/SKILL.md` r.301-303)
   è «non si inventa». Se il DM vuole questa scorciatoia, la dice lui, una volta,
   in un piano.
3. **«Parole ripetute entro 20» come miglioramento** (riga 45, 1,0 → 0,5 nel G2
   `README.md` r.223). `italiano-nativo.md` r.288 dice il contrario: in italiano
   la ripetizione non è un difetto, l'alternanza forzata sì.
4. **I conti 🔴·🟠·🟡 fra giri con lettori diversi come misura del
   miglioramento** (riga 11). Lo dice il giro stesso (G1 `README.md` r.26-31), e i
   🔴 saliti da 2 a 6 nel G2 erano difetti vecchi visti con l'SRD in mano.
5. **Spingere a zero `>4 frasi` e `>500 car`, e il MQM a 100.** L'ESITO della
   #246 indica proprio quel taglio come probabile causa delle coppie perse, e il
   MQM ha mediana 99,51 (ADR-0093, Contesto): non distingue più niente.
6. **Lettori in parallelo senza decisione**, e il terzo passo del DM a freddo
   fatto da chi ha preparato (righe 9, 26). Vanno contro una regola scritta.
7. **Script di conteggio scritti al volo e non salvati** (il «contate col mio
   script» di `G2/DEF-1/FIX.md` r.206; `box_metri.py` fuori dal repo). Se il
   numero serve, lo script entra in `scripts/`; altrimenti il numero non si cita.

---

## D · Note oneste

**Cosa ho letto per intero**: i due `README.md`, `G1/VERIFICA-SRD.md`,
`G2/APPLICATE.md`, `G1/DEF-1/FIX.md` e `VERIFICA.md`, la testa e la seconda
passata di `G2/DEF-1/FIX.md`, `G2/DEF-4/VERIFICA.md` (prima parte),
`G2/DEF-4/DEVELOPER.md`, `DM.md`, `PLAYTESTER.md`, i due `DECISIONI-DM.md` per
la parte generale e l'indice, i file della cartella condivisa elencati, ADR-0092,
ADR-0093 e l'ESITO della #246, il diff della #251, le rubriche di
`rumblingstone-playtest/references/` (dm, playtester), `SVI`, il ciclo di
`MS/SKILL.md`, `collaudo-mappe.md` dal collaudatore in poi, `RAA` §2-§7.
**Campionati**: gli altri `FIX.md` e `VERIFICA.md` (titoli e conti), gli altri
`DEVELOPER/PLAYTESTER/DM.md` (titoli e colonna dei codici, contata su tutti e
trenta), `lettore-a-freddo.md` e `quiz-a-due-agenti.md` (solo per grep), gli
esperimenti di settembre e inizio ottobre (README). **Non letti**: i grezzi del
corpus, `note-di-ricerca/*` oltre a `box_metri.py` (sono gli stessi delle note
già nel repo o sulla #246, salvo `prosa-inventario-repo.md` e `prosa-web.md`,
che differiscono dalle versioni della #246 e non ho confrontato riga per riga),
`ARCHIVI-WIZARDS` oltre l'indice e le tre decisioni.

**Contraddizioni trovate.**
1. Lettori in parallelo (`MS/SKILL.md` r.286) contro «un subagente alla volta»
   (`PIANO-LETTORE-E-PLAYTESTER.md` r.525, r.562), seguito a ottobre in
   `def4-giro4` e `def5-giro2` e non il 18.
2. D2 di `PIANO-AVVENTURE-COMMUNITY` su main dice «niente righe di scala nei
   master di ARC-07 già giocati»; il G2 le ha aggiunte. Sulla #246 la D2 è già
   cambiata («Sì, nella #245»): su main la riga è vecchia finché la #246 non entra.
3. `collaudo-mappe.md` r.181 («nessun rapporto vero») contro
   `COLLAUDATORE-M7C-2026-10-09.md`.
4. Il corpus: G2 `README.md` r.266 parla di 1.762 box (PR #250), mentre
   `/pf/corpus-prosa/RAPPORTO.md` ne misura 177 (121 EN, 56 IT). Sono due stadi
   diversi del lavoro; il RAPPORTO è il primo. La #250 è contenuta nella #246.
5. `G2/misure/MISURA-PRIMA.txt` e `MISURA-DOPO.txt` hanno la sezione `box_metri`
   identica (142 box, mediana 51): il «prima» del README (108 box, mediana 66) non
   viene da quel file. E il tag `prima-rifacimento-arc07` non è su `origin`.
6. G2 `APPLICATE.md` r.5 dice che il DM non aveva ancora risposto; il G1
   `README.md` r.75 dice che per il G1 aveva scelto «Tutte». Per il G2 non ho
   trovato la risposta.
7. La #251 non è «i 26 box impoveriti»: rimette le 8 coppie del cieco. Il suo ramo
   è `claude/project-thread-ep4auu`, lo stesso della #249 (il rifacimento); il
   thread che la possiede l'ho preso dalla consegna e non l'ho verificato.
8. `PT/SKILL.md` r.92 parla di codici `V-` che `SVI` non definisce.
9. Il G1 ha usato le otto domande del developer lo stesso giorno in cui le §9-§16
   entravano su main (ADR-0092, 2026-10-18).

**Una nota sul repo locale.** Il ramo di lavoro risultava «ahead of
`origin/claude/project-thread-e860p0` by 70 commits»: ho confrontato con
`origin/main` (`2ee82472`), come da consegna. Per leggere le PR ho creato tre ref
locali (`refs/remotes/pr/246`, `pr/250`, `pr/251`) con `git fetch`; nessun
checkout, nessun file del repo toccato.
