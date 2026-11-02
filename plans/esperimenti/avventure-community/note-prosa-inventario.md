# Inventario della misura della prosa di gioco — RumblingStone, 2026-10-18

Audit in sola lettura. Ramo di lavoro `claude/project-thread-q4s7mw` a `d6716f4` (allineato a main); PR #234 letta da `origin/claude/project-thread-zxxz0m` (`05587c1`). Nessun file del repo modificato. Le uscite grezze dei comandi stanno in `/tmp/claude-0/-home-claude-RumblingStone/50331982-18a6-5e0b-aa5e-5a3f5d0f7335/scratchpad/out/`.

Legenda: **[L]** = letto in un file o in un'uscita · **[I]** = mia inferenza.

---

## 1. Tabella degli strumenti

| Strumento | Cosa misura | Determ. | Cancello CI | Numero di oggi |
|---|---|---|---|---|
| `scripts/validate_prosa.py` | 7 norme (`NORME`, `validate_prosa.py:909-917`): terminologia non canonica, testo per i giocatori senza ancore, calchi dall'inglese, antitesi ripetuta (>1), maiuscole di enfasi (>1), trattino come respiro (>3% parole in read-aloud ≥80 parole), caratteristica minuscola. Tic contati solo nella prosa per i giocatori (`:920-982`). `--prima-dopo` confronta 5 tic fra due versioni (ADR-0036). `--foglio` = foglio di stile | sì (`:921-926`) | default **non bloccante** (`ci.yml:182-185`, `continue-on-error`); `--foglio --strict` **bloccante** (`ci.yml:189-190`) | **230 rilievi in 406 file** |
| `scripts/punteggio_mqm.py` + `scripts/specifiche-qualita.yaml` | MQM / ISO 5060 adattato: 13 norme pesate (minore 1, maggiore 5, critico 25) prese da misura_craft, validate_prosa, voto_scrittura. `punteggio = 100·(1 − penalità/righe)` (`punteggio_mqm.py:205`) | sì | **sì**: `--soglia` (`ci.yml:383-385`); soglie master_def 96,0, arco 87,0 (yaml) | 530 documenti, 0 sotto soglia, 0 critici; media 99,61, mediana 100, 443/530 a 100 |
| `scripts/misura_craft.py` | 23 «congegni di mestiere» (presenza o conteggio), `--box` (tetti di read-aloud-adulti), `--p1`, `--metrature`, `--spotlight`, `--costrutto-italiano`, `--copertura` contro due banchi (Abbazia, Palio) | sì | **no** in modo diretto (l'uscita stessa dice «Nessuna di queste soglie è sotto cancello»); entra in CI solo attraverso MQM | box >12 righe = 0 sui 12 bersagli; copertura da 35% (ARC-09 Battaglia Finale) a 96% (DEF-4) |
| `scripts/ciclo_prosa.py` | revisione a due giri (ADR-0077): `segnala` → `revisione` (CriticMarkup) → `applica [--auto]`; `misura` = delta MQM e segnalazioni per norma fra due versioni; aggiunge «tic minori in gruppo» (regola Humanizer) e Gulpease/ritmo come guard rail | sì (docstring) | **sì**: `registro --check` (`ci.yml:387-388`) = nessuna revisione applicata ha peggiorato | 11 revisioni applicate, segnalazioni −28, MQM +2,52 punti in tutto |
| `voto_scrittura.py` (tolto il 2026-10-22) + `plans/scrittura/casi.json` | percentuale di controlli superati su 10 casi (5 taratura, 5 verifica), corse con e senza skill; i controlli richiamano misura_craft e validate_prosa, più `box_senza_sembra` | sì | no come passo CI; un test tiene allineato `voti.json` (`RISULTATI.md:7-8`) | B-con 100/100%, A-con 97/96%, C-con —/98%, A-senza 89/81% |
| `scripts/validate_lingua.py` | refusi meccanici (accenti, virgolette, apostrofo al posto dell'accento); «o sono errori o non sono niente» | sì | **sì** sugli errori (`ci.yml:177-178`); avvisi non bloccanti | 637 file, 0 refusi, 2.458 avvisi |
| `scripts/lettura_a_scene.py` | non misura: serve un master una scena alla volta al lettore e al playtester a freddo, con diario a campi fissi (`ago`, `so adesso`) per trovare `L-ORDINE` | sì (serve il testo) | no | — (strumento di procedura) |
| `scripts/quiz_lettura.py` | quiz a due agenti: risposte dagli appunti contro libro aperto, confronto a radici di parola con la chiave | sì | **sì**, solo `--check` sulla forma delle chiavi (`ci.yml:163-164`) | 2 chiavi (ARC07-DEF-4, DEF-5), ben formate |
| `campioni_kappa.py` (tolto il <data della decisione del DM>) | κ di Cohen fra macchina (MQM promosso/bocciato) e un giudice, su due campioni disgiunti a seme fisso | sì | no (soglia κ ≥ 0,60 per entrare in CI) | campione A (DM): **nessun voto**; campione B (modello): n=20, Po 0,95, **κ = 0,0** |
| `ciclo_prosa.py segnala --languagetool` (ADR-0079) | secondo lettore LanguageTool locale, 3 regole | sì | no, non pesa in MQM | non eseguito (serve Java e il server locale) |
| `banco_prosa_locale.py` (solo nella PR #234, non su main) | genera i 10 casi con un LLM locale; `coppie` = foglio alla cieca; `esito` = quota con Wilson e κ giudice/DM | sì, con seme dichiarato | solo `--dry-run`, `coppie`, `esito` | gemma4 e4b: 40% / 42%; cieco 0/10 contro B-con |

---

## 2. Come si misura oggi un miglioramento della prosa (prima e dopo)

### 2.1 Il principio dichiarato: si misura la differenza, non lo stato
- [L] ADR-0036 (`plans/adr/ADR-0036-misurare-il-miglioramento-non-lo-stato.md:20-23`): «Nessuna soglia assoluta sulla prosa di gioco. Si misura la differenza fra due versioni dello stesso testo.» La burstiness è stata scartata perché **peggiorava** sulla versione che il DM aveva giudicato migliore (`:35-52`).
- [L] Limiti scritti (`:103-108`): il confronto non dice se un testo è buono, solo se è migliorato; serve una versione precedente.

### 2.2 MQM (`punteggio_mqm.py`)
- [L] Composizione: somma dei conteggi per norma × peso, divisa per le **righe del file** (`punteggio_mqm.py:186-205`). Norme pesate: 13 (uscita di `--norme`); «il registro elenca 101 norme; qui ne entrano 13».
- [L] Limiti dichiarati: non giudica la bellezza; nessun critico rilevato, il pass/fail «è cablato e non scatta mai» (docstring; `ADR-0059:67-71`); «un documento a 100 può violare trentasei norme che nessuno guarda» (`ADR-0059:76-79`); il κ col DM non è misurato (`:80-83`).
- [L] Prima/dopo: `--scrivi-baseline` / `--confronta` contro `campaign/misure/baseline-punteggi.json`. Oggi, rispetto alla baseline del 2026-10-10: 9 migliorati, 3 peggiorati (DEF-2 97,59 → 97,53; ARC08-02 100 → 99,90; P2B Torneo 98,49 → 98,48), 7 spariti.
- [I] **Sensibilità bassa.** La normalizzazione per riga schiaccia i delta: su DEF-1 (2.679 righe, penalità 13) togliere un difetto minore vale circa +0,04 punti. La distribuzione è al soffitto (443 file su 530 a 100, P25 = 100 per la classe `arco`). Come prova di un miglioramento di stile, il numero MQM da solo non regge: muove la coda e non il centro.
- [L] Il commento dello YAML dice «normalizzato per 1.000 righe» (`specifiche-qualita.yaml:143`), ma la formula è per riga (`punteggio_mqm.py:205`). [I] Si tratta solo di scala; i delta restano proporzionali.

### 2.3 Il registro dei miglioramenti (`ciclo_prosa.py` + `plans/scrittura/miglioramenti.json`)
- [L] `misura ORIGINALE RISCRITTO` dà il delta di un giro ed esce 1 se una norma cresce, se MQM scende o se un fatto cambia; ci si ferma dopo un giro che non abbassa le segnalazioni, o al terzo (`ADR-0077:184-187`, `ciclo_prosa.py:650`). `applica` scrive ogni voce in `miglioramenti.json` (segnalazioni, MQM, penalità, Gulpease, norma per norma).
- [L] Garanzie: nessun controllo peggiora, nessun fatto cambia (nomi del registro, numeri, CD) (`ADR-0077:49-54`). L'«auto» richiede anche una lettura non peggiorata: Gulpease al massimo −1, ritmo al massimo −0,05 (`ADR-0077:78-86`, `ciclo_prosa.py:507-531`).
- [L] Limite dichiarato (`ADR-0077:208-212`): «MQM misura la conformità alle norme registrate, non la bellezza… un tic che non è una norma pesata (i tic minori in gruppo) abbassa le segnalazioni senza muovere MQM. Il giudizio resta di chi legge a voce».
- [L] Oggi: 11 revisioni (tutte del 2026-10-03, lotto D13), segnalazioni −28, MQM +2,52 in tutto; nessuna ha peggiorato.
- [L] Gulpease non è un voto: «non discrimina» (70,1 nei box contro 65,4 nei documenti) e il 15% dei box esce dalla scala (`PIANO-MISURA-EDITORIALE-STANDARD.md:153-195`). Resta come guard rail.

### 2.4 `voto_scrittura` (il banco L11)
- [L] **Com'è fatto il voto.** Per ogni corsa e caso, `vota()` applica i controlli che il caso elenca in `casi.json`. `riepilogo()` somma controlli superati e controlli totali per condizione (le tre ripetizioni insieme) e per metà (`voto_scrittura.py:245-255`); la percentuale è `100·ok//tot` (`:279`). Taratura = 32 controlli × 3 corse = 96; verifica = 33 × 3 = 99. Controlli per caso: S01/S06 apertura 10, S02 combattimento 11, S07 12, dialogo 3, testo per un giocatore 3, documento 5. **16 controlli su 32 in taratura e 16 su 33 in verifica sono `box_*`**, otto per ciascun caso di apertura e di combattimento; con `chiude_che_fate` e `hdywtdt` si arriva a 17 e 18 [L, conteggio fatto su `casi.json`]. Se manca il box, cade metà del voto.
- [L] I controlli (`voto_scrittura.py:165-193`): `box_presente`, `box_tetto_righe`, `box_un_nome`, `box_senza_parentesi`, `box_p1`, `box_senza_sembra`, `box_senza_metrature`, `box_etichettato`, `chiude_che_fate`, `hdywtdt`, `dialogo_forma`, `ancore`, `calchi`, `tic_gioco`, `doc_*`.
- [L] Limite dichiarato: «Il voto misura la conformità alle norme, non se la prosa è bella» (`RISULTATI.md:49-51`). Tre corse per condizione: «un caso in più o in meno sposta tre punti» (`:43-47`).
- [L] **Il pavimento (PR #234, ADR-0089 §«il banco ha un pavimento alto», righe 60-84 sul ramo).** Un testo spazzatura prendeva 81% / 78% perché i controlli sui box passavano anche senza box. Con I1 (i controlli `box_*` richiedono `box_presente`) scende a 44% / 42%. Restano superati per intero, anche dalla spazzatura, i quattro casi senza controllo di presenza: S04, S05, S08, S10.

### 2.5 Il confronto cieco (PR #234)
- [L] `banco_prosa_locale.py coppie --a B-con-1 --b L-… --seme N` (`banco.py:305-328`): per ogni caso mette i due testi in ordine casuale (`random.Random(seme)`), con il prompt e senza il nome della condizione; la chiave va in un `.chiave.json` a parte. Il DM scrive `1`, `2` o `=` dopo «Preferito:» e legge «ad alta voce, come al tavolo».
- [L] `esito` (`:372-400`): quota di preferenze per la sfidante sui casi decisi (i pari esclusi), intervallo di Wilson al 95%; con `--giudice`, κ giudice/DM e accordo grezzo.
- [L] Soglie scritte prima della prova (ADR-0089, Validazione, righe 215-229 sul ramo): norme ≥ 90% in verifica e ≥ 3/5 casi interi; «la usa come bozza» = preferita o pari in ≥ 3/10; «sostituisce» = **almeno 40 coppie** con il limite inferiore di Wilson sopra 0,5. Con 10 coppie la superiorità «è impossibile per costruzione».
- [L] Esito del 2026-10-11: gemma4 e4b-it-qat al 40% in taratura (13/32) e al 42% in verifica (14/33), cioè al livello della spazzatura. Quasi tutta la distanza viene dalla forma: il read-aloud è scritto in paragrafi e non in `> *…*`. Rimesso in forma da uno script si arriverebbe a 94% / 91%, ma il modello decide per i PG e non porta le meccaniche. Al cieco B-con vince 10/10, nessun pari, Wilson [0,00, 0,28] (ADR-0089 righe 260-273; `RISULTATI.md` sul ramo).

### 2.6 Può servire da misura prima/dopo di un miglioramento della prosa? [I]
- **Il voto come numero, no.** B-con sta già al 100% (soffitto): non c'è margine per mostrare un miglioramento sopra l'agente con le skill. Pesa quasi solo la forma dei box e vede la sostanza solo per assenza. Due versioni di un testo che rispettano entrambe le norme prendono lo stesso voto.
- **Il foglio cieco, in parte sì.** È l'unica misura di *preferenza* del repo e risponde alla domanda «è meglio?». Però:
  1. è costruito per confrontare due **cartelle di corse** sugli stessi 10 casi (`CORSE / a / f"{id}.md"`), non due versioni di un master esistente. Per un prima/dopo andrebbe adattato, per esempio estraendo i box riscritti e quelli originali come due «corse»;
  2. con 10 coppie distingue solo una perdita o una vittoria nette; per dire «meglio» con Wilson > 0,5 servono ~40 coppie, cioè 40 letture del DM;
  3. il DM è il solo giudice valido: un giudice automatico entra solo sopra κ 0,60, e oggi il κ(B) di `campioni_kappa` è 0,0.
- **La combinazione già prevista dal repo** è questa: ciclo_prosa `misura` (non peggiora, MQM su, fatti uguali) come cancello inferiore, più un giudizio umano cieco. Oggi le due metà non sono collegate da nessuno strumento.

---

## 3. Buchi dichiarati sulla prosa di gioco

### 3.1 Registro (`skills/REGISTRO-NORME-EDITORIALI.md`)
- [L] Conto (`:156-161`): 🟢 47 · 🟡 30 · 🔴 20 · ⚪ 4. MQM ne pesa 13.
- [L] **🔴 prosa di gioco, non misurate:**
  - read-aloud-adulti: **max due livelli di subordinate** (servirebbe un parser sintattico; le virgole darebbero falsi positivi, `:42`);
  - read-aloud-adulti §2-bis: il **box di luogo non descrive le creature** (i box non dichiarano il loro tipo, `:44`);
  - consequence-echoes §3-ter: un eco **non anticipa** (servirebbe leggere il master intero);
  - varieta-fra-archi: mai due archi di fila con la stessa tinta (manca il dato);
  - sviluppo-degli-incontri §7, §8, §11-14 e il giro delle quattro letture a freddo: giudizi, lasciati di proposito fuori dai cancelli (ADR-0073).
- [L] **🟡 prosa di gioco, misurate in parte:**
  - box di luogo in «poche frasi» (`>4 frasi`, indicatore senza peso: 61 box su 104 nei DEF);
  - blockquote 3-10 righe contro 12 (le due fonti non concordano);
  - quarta colonna sensoriale (conta chi ce l'ha);
  - yes-and with teeth (conta la dichiarazione);
  - self-check (la domanda 4 è giudizio puro);
  - spotlight ≤ 40% (conta le menzioni del nome, non le scene);
  - echi armati (conta le menzioni);
  - italiano-nativo §8, dislocazione o «c'è» (sovrastima: 59% dei box);
  - tic minori in gruppo (soglia di Humanizer, non tarata sul repo, fuori da MQM, `ADR-0077:145-147`);
  - guard rail di Gulpease e del ritmo.
- [L] Causa comune dichiarata: «nove delle undici hanno la stessa causa: i moduli non marcano le cose di cui la norma parla… non è un buco di codice» (`REGISTRO:230-235`).

### 3.2 Cosa il repo dice di non saper misurare
- [L] **La bellezza o la qualità della voce**, ripetuto ovunque: docstring di `punteggio_mqm` («Non giudica la bellezza»), `voto_scrittura` («non se il testo è bello»), `RICERCA-STANDARD-PROSA…:141-145`, `ADR-0077:208-212`, ADR-0089 «Resta fuori».
- [L] **Lo stile come tessitura**: 64 falsi positivi su 64 sui tropi esterni (`PIANO-PROSA-CHE-NON-SEMBRI-GENERATA.md:31-43`); i quattro tic che «una macchina non trova» stanno in `italiano-nativo.md` §9.2-bis e vanno scritti, non contati (`:72-77`).
- [L] **La grammatica**: i rilevatori del repo prendono 2 errori su 80 in una prova scritta da un terzo, LanguageTool 0 su 40 su accordi e congiuntivi (`ADR-0079:65-71`).
- [L] **L'accordo col DM**: κ(A) inesistente, quindi nessuna metrica è validata contro il DM (`campioni_kappa --kappa`; `ADR-0059:80-83`).
- [L] **I critici di canone** (statblocco inventato, contraddizione con `state.md`): nessun rilevatore (`ADR-0059:67-71`).
- [L] **La sostanza dei casi senza forma** (S04, S05, S08, S10): manca una norma registrata su cosa *deve* esserci (ADR-0089, I1).
- [L] **Le virgolette dritte non sono dialogo** (limite dichiarato di misura_craft): un dialogo scritto con `"` viene contato meno del vero.

---

## 4. Numeri di oggi (main a `d6716f4`, 2026-10-18)

**punteggio_mqm**
- `--soglia`: ✓ 530 documenti, nessuno sotto soglia, zero critici (exit 0).
- `--distribuzione`:

| classe | n | P10 | P25 | P50 | P75 | min |
|---|---:|---:|---:|---:|---:|---:|
| arco | 491 | 99,33 | 100 | 100 | 100 | 87,44 |
| campagna | 34 | 98,15 | 100 | 100 | 100 | 94,62 |
| master_def | 5 | 98,02 | 98,76 | 99,51 | 99,73 | 97,53 |

- Aggregato da `--json` (mio calcolo): media 99,61, 443/530 a 100, penalità totale 793 su 96.208 righe.

| norma | occorrenze | penalità | file |
|---|---:|---:|---:|
| box_piu_di_un_nome_proprio | 205 | 205 | 44 |
| terminologia_non_canonica (×5) | 32 | 160 | 26 |
| box_con_parentesi | 138 | 138 | 33 |
| box_oltre_12_righe (×5) | 21 | 105 | 8 |
| calco_dall_inglese | 91 | 91 | 32 |
| read_aloud_presuppone (P1) | 33 | 33 | 17 |
| metratura_nella_voce_narrante | 28 | 28 | 9 |
| maiuscole_di_enfasi | 21 | 21 | 21 |
| antitesi_ripetuta | 6 | 6 | 6 |
| box_sembra_pare | 4 | 4 | 4 |
| trattino_come_respiro | 2 | 2 | 2 |

- I file peggiori: `Arco-Post-Hammerfist-HANDOUTS.md` 87,44 (sopra la soglia 87,0 per 0,44); `01_Scheda_Giocatore_Sintesi_Pratica_Fase2.md` 88,24; `00_Cintura_della_Devastazione.md` 90,0.

**misura_craft**
- `--box` (box / >12 righe / parentesi / >1 nome / >4 frasi / >500 car):
  - DEF-1: 28/0/3/7/16/9
  - DEF-2: 19/0/1/8/13/8
  - DEF-3: 19/0/1/9/12/6
  - DEF-4: 35/0/2/2/18/4
  - DEF-5: 7/0/0/1/3/1
  - ARC-08 Hammerfist: 84/0/5/40/14/13
  - Palio: 40/0/2/4/1/0
  - Abbazia: 11/0/0/0/1/0
  - Torre di Zalkatar e Battaglia Finale: 0 box.
- `--copertura` (congegni su 23): DEF-4 22 (96%), DEF-3 18, DEF-1 17, Torneo di Dauth 13, ARC-08 13, Abbazia 12 (banco), Palio 11 (banco), DEF-5 11, Zalkatar 11, Rhest 10, DEF-2 9, Battaglia Finale 8 (35%).

**validate_prosa**: 230 rilievi in 406 file, non bloccante. Tipi più frequenti nelle prime ~60 righe stampate (l'uscita tronca «… e altri 170»): progressivo all'inglese 26, possessivo su una parte del corpo 14, maiuscole di enfasi 8, forma inglese di glossario 8, antitesi 4. Il conto completo per norma è quello di MQM qui sopra.

**ciclo_prosa** su `07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md`
- `segnala`: **24 segnalazioni**: 16 tic minori in gruppo (soprattutto antitesi + trattino), 4 box con più nomi propri, 3 box con parentesi, 1 calco («state camminando», r.1140).
- `misura` (originale contro copia identica, per avere la linea di base): MQM 99,51, penalità 13, segnalazioni 24, Δ 0, exit 0.
- [I] Su DEF-1, 16 segnalazioni su 24 sono tic minori in gruppo, che **non entrano in MQM**: correggerle tutte lascia MQM fermo.

**voto_scrittura --corse**
- A-con 94/96 (97%) · 96/99 (96%); A-senza 86/96 (89%) · 81/99 (81%); B-con 96/96 · 99/99 (100%); C-con — · 98/99 (98%).
- `--check` ✓, 12 corse.
- PR #234: L-gemma4e4bitqat-1 13/32 (40%) · 14/33 (42%); spazzatura 44% / 42%.

**Altri**
- `validate_lingua`: 637 file, 0 refusi, 2.458 avvisi (exit 0).
- `campioni_kappa --kappa`: A nessun voto; B κ 0,0 (Po 0,95 = Pe 0,95, n=20).
- `quiz_lettura --check`: ✓ (2 chiavi).
- `ciclo_prosa registro --check`: ✓.

Dipendenze mancanti: nessuna per i comandi eseguiti. LanguageTool (Java 17, server locale) e il banco locale (Ollama e GPU) non sono stati eseguiti.
