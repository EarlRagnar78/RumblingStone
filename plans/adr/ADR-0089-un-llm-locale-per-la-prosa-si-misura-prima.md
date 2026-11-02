# ADR-0089 — Un LLM locale per la prosa si misura prima, e oggi non sostituisce niente

- **Stato**: proposta; I1 applicato il 2026-10-10 su richiesta del DM («risolvi i problemi trovati»), il resto in attesa
- **Data**: 2026-10-10
- **Numero**: 0089. 0086 e 0087 sono della #230 e della #233, 0088 è prenotato
  per la #99
- **Misurato su**: `main` a `e63fddd` (merge della #230)
- **Decisione-fonte**: il DM, 2026-10-10: *valutare, cercare, misurare e provare
  se conviene un LLM locale specializzato per la prosa, orchestrato «come
  ComfyUI», con gli strumenti e i benchmark migliori della community, sotto i
  vincoli di ruoli e skill del repo*
- **Rapporti**: applica [ADR-0067](ADR-0067-il-confine-dichiarato-fra-codice-e-llm.md)
  (il ponte e le sue sette condizioni), [ADR-0036](ADR-0036-misurare-il-miglioramento-non-lo-stato.md)
  (il tavolo vince sul modello), [ADR-0019](ADR-0019-licenza-dei-pesi-non-del-software.md)
  (la licenza è quella dei pesi); riusa il banco di L11
  (`plans/scrittura/`, `voto_scrittura.py`) e `campioni_kappa.py`
- **Strumento**: [`scripts/banco_prosa_locale.py`](../../scripts/banco_prosa_locale.py), il ponte della prova (I2)

## Prima di leggere

**Cosa manca per rispondere meglio.**

| Cosa manca | Perché cambia la risposta |
|---|---|
| Il **perché** del locale | Privacy, costo, uso offline al tavolo o qualità sono quattro domande diverse, e solo l'ultima chiede di battere il generatore di oggi |
| Un corpus di prosa approvata dal DM | Senza, un fine-tuning (LoRA) non ha dati. È la stessa mancanza di D4 di `PIANO-PIPELINE-IBRIDE` |

**Assunzioni.** «L'approccio attuale» è un agente Claude con le skill e accesso
al repo, cioè le corse B-con e C-con di L11. Il caso d'uso è la prosa di gioco
in italiano. Il DM non vuole servizi remoti per il modello locale.

**Le due macchine del DM** (dichiarate il 2026-10-10):

| Macchina | GPU | RAM | Cosa ci sta, a 4 bit |
|---|---|---|---|
| Dell Precision 5560 | RTX A2000 Laptop, **4 GB** (scheda Dell) | 32 GB | **Gemma 4 26B-A4B** (MoE, 3,8 miliardi di parametri attivi, 16,2 GB quantizzato secondo il rapporto tecnico): i pesi stanno in RAM, gli esperti girano sulla CPU e l'attenzione sulla GPU (`llama-server --n-cpu-moe`). Velocità attesa nell'ordine di 5-15 token al secondo `[INFERRED]` |
| ASUS TUF F16 | RTX 4050 Laptop, **6 GB** | 16 GB (11 già in uso) | **Gemma 4 12B** (7,65 GB) solo in parte sulla GPU, oppure E4B (2,3 GB) tutto sulla GPU. Il 26B-A4B non ci sta |

Nessuna delle due regge un modello denso da 27-31B in tempi da tavolo: Qwen3.8-27B
e Gemma 4 31B escono dalla prova. La macchina della prova è la Dell. Con
18.000 token di references nel prompt, la lettura del prompt sulla CPU pesa più
della scrittura: va misurata in A4, ed è la ragione di `--contesto ridotto`.

## Contesto

La domanda ha due metà: se conviene un modello locale, e con che cosa si
misurerebbe. Sulla seconda il repo è più avanti della community, e va detto
subito perché sposta la prima.

### Cosa misura già il repo

| Strumento | Domanda | Stato |
|---|---|---|
| `voto_scrittura.py` + `plans/scrittura/casi.json` | il testo rispetta le norme registrate? 10 casi, taratura e verifica, 11 controlli che riusano `misura_craft` e `validate_prosa` | in uso: B-con 100%, C-con 98%, A-senza 81% in verifica |
| `punteggio_mqm.py` | quanto pesano i difetti (MQM / ISO 5060) | in uso, i critici non scattano mai (nessun confronto col canone) |
| `campioni_kappa.py` | il DM è d'accordo con la macchina? κ ≥ 0,60 | in uso |
| `ciclo_prosa.py --languagetool` | secondo lettore locale (ADR-0079) | in uso, facoltativo |
| `comfyui_batch.py` | il solo script che chiama un modello | in uso, per le immagini |

### Una misura nuova, presa per questa ADR: il banco ha un pavimento alto

Ho fatto votare a `voto_scrittura` un testo spazzatura, lo stesso per tutti e
dieci i casi: due righe senza box, con «sembra», una parentesi e una metratura.

| | taratura | verifica | casi superati per intero |
|---|---:|---:|---:|
| B-con (agente con skill) | 100% | 100% | 10/10 |
| A-senza (agente senza skill) | 89% | 81% | 4/10 |
| **testo spazzatura** | **81%** | **78%** | **4/10** |

La causa è precisa: i sei controlli sui box (`box_tetto_righe`, `box_un_nome`,
`box_senza_parentesi`, `box_p1`, `box_senza_sembra`, `box_senza_metrature`)
**passano quando il box non c'è**, e i casi S04, S05, S08 e S10 si superano per
intero senza forma. Il voto distingue bene chi rispetta le norme da chi le viola
dentro un box; non distingue un buon testo da un testo vuoto. Per confrontare
due generatori va letta la colonna dei casi superati per intero, e i controlli
sui box vanno condizionati a `box_presente` (§Implementazione, I1).

**I1 è applicato** (2026-10-10). Dopo la correzione lo stesso testo prende
14/32 in taratura e 14/33 in verifica (44% e 42%), e le corse vere non cambiano
di un voto: in tutte, dove il caso chiede un box, il box c'era. `voti.json`
resta identico. Restano superati per intero, anche dalla spazzatura, i quattro
casi senza un controllo di presenza (S04, S05, S08, S10): lì una norma che dica
cosa *deve* esserci non è registrata, e inventarla qui violerebbe G3.

### Cosa offre la community, e quanto vale qui

**Benchmark di scrittura creativa.**

| Benchmark | Cosa misura | Limite per questo repo |
|---|---|---|
| [EQ-Bench Creative Writing v3](https://eqbench.com/creative_writing.html) e Longform | rubrica + Elo a coppie, giudice Claude Sonnet 4.6 (dal 2026-03-01); misura anche «slop» e ripetizione | inglese; il giudice è della stessa famiglia del generatore attuale, quindi un vantaggio Claude è sospetto di auto-preferenza |
| [Judgemark v4](https://eqbench.com/judgemark-v4.html) | quanto un modello sa **giudicare** la scrittura | serve a scegliere un giudice, non un autore |
| [lechmazur/writing](https://github.com/lechmazur/writing) | racconti con 10 elementi obbligatori, giuria di LLM | è lo schema giusto per noi (elementi obbligatori = controlli), ma inglese e senza forma da tavolo |
| [Evalita-LLM](https://arxiv.org/abs/2502.02289), [ITA-Bench](https://github.com/sapienzanlp/ita-bench), Open ITA LLM Leaderboard | competenza in italiano (comprensione, QA, alcuni compiti generativi) | nessuno misura la prosa narrativa: servono solo come filtro d'ingresso |

Nessun benchmark della community misura **prosa narrativa italiana sotto vincoli
di forma**. Il banco di L11 lo fa già, su dieci casi.

**I modelli locali, secondo EQ-Bench Creative Writing v3** (Elo, letto il
2026-10-10; per confronto `claude-opus-5-5` = 2050):

| Modello | Elo | Licenza dei pesi | Gira su |
|---|---:|---|---|
| Qwen3.8-27B | 1671 | da verificare sul `LICENSE` del modello (le versioni precedenti erano Apache 2.0) | GPU 24 GB `[INFERRED]` |
| gemma-4-31B-it | 1368 | **Apache 2.0** (Google, marzo 2026) | GPU 24 GB `[INFERRED]` |
| gemma-4-12B-it | 1289 | Apache 2.0 | GPU 12 GB, o in parte su RAM `[INFERRED]` |
| gemma-4-26B-A4B-it | non in classifica; 1438 sull'Arena generale (rapporto tecnico) | Apache 2.0 | **32 GB di RAM + GPU piccola**: la Dell |

Letta come Elo, una distanza di 380 punti dà al modello locale migliore circa
**il 10% di preferenze** contro il generatore di oggi; 680 punti (Gemma 4 31B)
circa il 2%. È inglese, con un giudice di parte, e su prosa libera: è un ordine
di grandezza, non una misura nostra. Gemma 4 31B nel Longform ha «slop» 63,5
contro 5,6 di Claude Opus 5: il tipo di difetto che `italiano-nativo.md`
combatte già.

**Strumenti di valutazione** (software, tutti FOSS):

| Strumento | Licenza | Uso possibile qui |
|---|---|---|
| promptfoo | MIT | matrice modelli × prompt con asserzioni Python: potrebbe chiamare `voto_scrittura.controlli` |
| Inspect AI (UK AISI) | MIT | stesso ruolo, più rigoroso sui log |
| Prometheus 2 (`prometheus-eval`) | Apache 2.0 | giudice locale con rubrica; 72-85% d'accordo con umani a coppie, in inglese |
| DeepEval | Apache 2.0 | G-Eval, rubriche |

Nessuno aggiunge una misura che il repo non abbia: aggiungono un cruscotto.
Il banco di L11 fa già la matrice, in 300 righe di stdlib.

**L'orchestrazione «come ComfyUI».** ComfyUI per il testo esiste come nodi
Ollama, pensati per arricchire i prompt delle immagini. Per una catena di testo
gli equivalenti visuali sono Langflow (MIT) e Flowise (Apache 2.0); n8n (Sustainable
Use License) e Dify (Apache 2.0 con condizioni aggiuntive) non sono licenze
OSI. Ma la catena che ADR-0067 ha già deciso (un ponte, un file, un
validatore) è il grafo: ogni nodo è uno script con un'uscita controllabile. Un
editor a nodi aggiunge un servizio da tenere in piedi e toglie il `cmp` fra due
giri.

### I vincoli che un modello locale deve reggere

I references obbligatori di `narrative-style` pesano **73.368 caratteri, circa
18.000 token** prima della richiesta; con `state.md` e `campaign-coherence.md`
si va oltre 35.000. Un agente con gli strumenti apre il master da solo; un
modello locale senza strumenti vede solo l'estratto che gli si passa. Per S04
(l'eco di Hella) non c'è una sezione da estrarre: il modello locale scrive senza
il canone, e il controllo `ancore` non se ne accorge.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Una prova misurata sul banco di L11, sulla macchina del DM** (scelta) | riusa i dieci casi e i rilevatori registrati; le soglie si scrivono prima; il DM giudica alla cieca | dieci casi danno un indizio, non una prova; la Dell è lenta; il sandbox non può farla |
| Sostituire subito il generatore con un modello locale | niente dati fuori casa, nessun costo per chiamata | 380-680 Elo sotto su EQ-Bench; senza strumenti il modello non legge `state.md`, e i critici MQM restano scoperti |
| Adottare EQ-Bench Creative Writing così com'è | metodo pubblico, classifica aggiornata, misura anche «slop» e ripetizione | inglese, giudice della stessa famiglia del generatore attuale, prosa libera senza forma da tavolo |
| Un editor a nodi (ComfyUI con nodi Ollama, Langflow MIT, Flowise Apache 2.0) | la catena si vede come un grafo, come per le immagini | un servizio in più, nessuna misura in più; ADR-0067 ha già il grafo (ponte, file, validatore) e il `cmp` fra due giri |
| Fine-tuning (LoRA) subito | lo stile del repo entrerebbe nei pesi | nessun corpus di prosa approvata dal DM; si addestrerebbe sullo stile del generatore attuale |
| Un giudice automatico al posto del DM (Prometheus 2, lo stesso modello) | ripetibile, senza la sera del DM | ADR-0036: la burstiness aveva detto il contrario del tavolo; un giudice entra solo dopo κ ≥ 0,60 col DM |

## Decisione

1. **Nessun modello locale sostituisce il generatore attuale.** Non c'è una
   misura che lo giustifichi, e quella esterna dice il contrario.
2. **Si fa una prova misurata, una volta, sulla macchina del DM**, con il banco
   che c'è: `banco_prosa_locale.py` genera i dieci casi in
   `plans/scrittura/corse/L-<modello>-<n>/`, `voto_scrittura --corse` li vota,
   e il DM sceglie alla cieca fra coppie (corsa locale contro B-con).
3. **Il banco si corregge prima della prova** (I1, fatto), perché un
   generatore che non scriveva box prendeva 78%.
4. **Un caso d'uso locale si dichiara prima di misurare**, con la sua soglia. La
   proposta è uno solo: **bozze offline al tavolo** (battute di PNG, nomi,
   descrizioni di riempimento), mai canone, sempre riletto dal DM.
5. **Niente editor a nodi, niente giudice automatico decisivo, niente
   fine-tuning** finché non c'è un corpus di prosa approvata.

## Piano in tre fasi

### Audit (prima di toccare)

| # | Passo | Comando | Esito atteso |
|---|---|---|---|
| A1 | Rimisurare la linea di base | `python3 scripts/voto_scrittura.py --corse` | B-con 100/100, C-con 98% |
| A2 | Contare i casi superati per intero per condizione | `voto_scrittura` con I1 applicato | la colonna che conta per il confronto |
| A3 | Verificare la licenza dei pesi scelti sul `LICENSE` del modello | lettura, gate d'uscita di `rumblingstone-edizione` | Apache 2.0 o MIT, altrimenti fuori |
| A4 | Misurare l'hardware | `nvidia-smi`, tempo di un caso con `--dry-run` + una chiamata | ≤ 120 s a caso, o il caso d'uso al tavolo cade |
| A5 | `fase1.py` sui bersagli | `python3 scripts/fase1.py scripts/voto_scrittura.py` | nessun archivio toccato |

### Implementazione

| # | Lotto | Cosa | Costo |
|---|---|---|---|
| I1 ✅ | il voto non regala i box | in `voto_scrittura.controlli`, i sei `box_*` falliscono se `box_presente` fallisce; rimisura di tutte le corse | fatto: nessuna corsa cambia, la spazzatura scende da 78% a 42% |
| I2 ✅ | il ponte | `banco_prosa_locale.py` in `scripts/`, voce nel manifest con `external_bins: []`, modello dichiarato in `corsa.json` (condizione 6 di ADR-0067); CI solo su `--dry-run` e su `coppie`/`esito` con un foglio di prova | medio |
| I3 | la norma | riga in `REGISTRO-NORME-EDITORIALI.md`: «una corsa locale si vota con il banco di L11» | piccolo |
| I4 | la prova | `scripts/llm-locale/` ✅; poi, sulla macchina del DM: 1 o 2 modelli × 3 ripetizioni × `--contesto pieno`, poi una ripetizione `ridotto` per vedere quanto pesano i references | tempo del DM, nessun costo di repo |

L'installazione e la prova stanno in [`scripts/llm-locale/`](../../scripts/llm-locale/README.md),
sullo stesso schema di `comfyui-local/`: un Distrobox con la GPU dell'host,
Ollama (MIT) dentro, niente sull'OS di Bazzite. Il DM ha chiesto di provarla
prima sull'ASUS con Bazzite, partendo da una macchina con il solo repo, e poi
sulla Dell.

```bash
scripts/llm-locale/setup-distrobox.sh     # una tantum
scripts/llm-locale/start.sh               # terminale A, il server
scripts/llm-locale/scarica-modello.sh     # terminale B: il modello consigliato per la macchina
scripts/llm-locale/prova.sh               # un caso per i tempi, i dieci casi, il voto, il foglio
```

`comune.sh` sceglie il modello da VRAM e RAM: `gemma4:e4b-it-qat` (6,1 GB)
sull'ASUS, poi `gemma4:12b-it-qat` (7,2 GB) a mano; `gemma4:26b` sulla Dell.
Sulla Dell resta possibile `llama-server --n-cpu-moe`, che tiene in RAM i soli
esperti; Ollama divide per strati, e la differenza di velocità si misura lì.

### Validazione

Le soglie sono scritte prima della prova e non si spostano dopo.

| Domanda | Misura | Soglia per «sì» |
|---|---|---|
| Rispetta le norme? | `voto_scrittura`, verifica, dopo I1 | ≥ 90% dei controlli e ≥ 3/5 casi interi su tre ripetizioni |
| Il DM la usa come bozza? | coppie alla cieca contro B-con, 10 casi | il DM la preferisce o la dà pari in almeno 3 casi su 10 |
| Sostituisce il generatore? | coppie alla cieca, **almeno 40 coppie** | limite inferiore di Wilson al 95% sopra 0,5. Con 10 coppie è impossibile per costruzione: il miglior esito, 10 su 10, dà [0,72, 1,00] e il peggiore [0,00, 0,28], e tutto quello che sta in mezzo non si distingue |
| Il canone regge? | lettura del DM su S04 e S08, le due che toccano `state.md` | zero contraddizioni (sono i critici MQM) |
| È ripetibile? | stesso seme, stessa corsa | stessi file, byte per byte, se il server rispetta `seed` |

Un giudice automatico (Prometheus 2 o lo stesso modello locale) può compilare
un secondo foglio; `esito --giudice` stampa il κ col DM e l'accordo grezzo.
Entra come aiuto solo sopra κ 0,60, e con preferenze sbilanciate il κ crolla
anche con l'80% d'accordo (provato: 8 su 10 concordi, κ 0,00), quindi si leggono
tutti e due.

## Che cosa ho potuto provare qui, e cosa no

**Non ho fatto girare un modello locale.** Il sandbox ha 4 CPU, 15 GB di RAM,
nessuna GPU, e il proxy nega Hugging Face, il registro di Ollama e ModelScope.
Il confronto vero è la prova I4, e la fa il DM.

**Ho provato l'harness da capo a fondo** con un server finto compatibile OpenAI,
in due modi:

- **eco** (restituisce i testi di B-con-1): la corsa esce identica byte per
  byte e `voto_scrittura` le dà 100% e 100%, come B-con. L'harness non sporca il
  testo, e toglie i blocchi `<think>` dei modelli a ragionamento.
- **piatto** (il testo spazzatura): 81% e 78%. È la misura che ha portato a I1.

E inoltre: senza server esce con codice 3 e non scrive niente (condizione 2 di
ADR-0067); l'estratto trova la sezione giusta in 8 casi su 10 (S04 non nomina
una sezione, S05 e S10 sono documenti); `coppie` ed `esito` producono foglio,
chiave, quota con l'intervallo di Wilson e κ.

### La prima prova sull'ASUS (2026-10-10), scartata

Il DM ha installato tutto da zero su Bazzite e ha fatto girare
`gemma4:e4b-it-qat`. Il voto è uscito al 40% e al 60%, ma la corsa non vale:
con 24.576 token di contesto il server ha tagliato a metà quattro prompt su
dieci senza errore, un quinto ha lasciato la risposta vuota. Il banco adesso
si ferma prima (codice 4) o mette la corsa fuori dal voto (codice 5), e il
contesto predefinito è 32.768. Resta valido il dato sui tempi, da 13 a 50
secondi a caso. Il dettaglio è in [`RISULTATI.md`](../scrittura/RISULTATI.md).

### La corsa valida sull'ASUS (2026-10-11)

Rifatta con il contesto a 32.768: nessun caso guasto, 40% in taratura e 42% in
verifica. Quasi tutta la distanza viene dalla forma del box: il modello scrive
il read-aloud in paragrafi normali. Rimesso in forma da uno script, il voto
sarebbe 94% e 91%, ma il banco non vede la sostanza, e lì il modello decide per
i PG e non porta le meccaniche. Per la prima domanda della validazione la
risposta resta no.

Il foglio alla cieca dà la seconda: il DM ha preferito B-con in tutte e dieci
le coppie, nessun pari (0/10, Wilson [0,00, 0,28]; la soglia era 3). Il 4B non
serve nemmeno come bozza. Restano aperti il 12B sull'ASUS e il 26B sulla Dell:
se il 12B finisce sotto 3 su 10 anche lui, la domanda si chiude con un no per
l'hardware che il DM ha oggi.

### Il canale, dopo ADR-0099 (2026-10-23)

Con [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md) il LLM
locale sta nel canale **unstable**: Ollama e i pesi non entrano nei
`requirements*.txt` e non girano in CI. In CI restano solo `--help` e
`corsa --dry-run` di `banco_prosa_locale.py`, che è codice del repo e non
chiama nessun modello. Sale a testing solo con una misura che passi le soglie
qui sopra, e oggi non ce n'è.

## Conseguenze

**Si guadagna** una risposta misurata sulla domanda, invece di un'opinione
sulle classifiche altrui, e un banco che vale per qualunque generatore futuro,
locale o no.

**Si paga** una sera del DM per leggere dieci coppie ad alta voce, e la
lentezza della Dell: un modello che lascia gli esperti in RAM è utilizzabile per
una prova, non per improvvisare al tavolo, finché A4 non dice il contrario. I1
non è costato niente: le tabelle di `RISULTATI.md` restano vere.

**Resta fuori**, e va detto: nessuna misura qui vede se la prosa è *bella*.
Il banco vede le norme, le coppie vedono la preferenza del DM su dieci casi.
Una preferenza su dieci casi è un indizio.

**Da rivedere se**: un modello aperto supera 1900 Elo su EQ-Bench con licenza
OSI e gira sulla Dell (32 GB di RAM, 4 GB di GPU); oppure il DM raccoglie 30 o più testi approvati al tavolo,
e allora un LoRA ha i dati per essere provato; oppure il caso d'uso diventa
«nessun dato fuori casa», che cambia il criterio da qualità a privacy.
