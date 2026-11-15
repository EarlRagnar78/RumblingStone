# Fare le prove sul portatile con la RTX 4050

> Forma: **guida pratica** ([Diátaxis](../../plans/adr/ADR-0123-la-documentazione-segue-diataxis.md)).

Alcune prove del progetto non girano nel container dove lavora l'agente, perché
vogliono una GPU. Questa guida le raccoglie tutte per l'ASUS TUF F16 del DM
(RTX 4050 da 6 GB, 16 GB di RAM, Bazzite/KDE): cosa serve, i comandi esatti,
quanto ci vuole e come rimandare i risultati. La stessa guida spiega come
portare nel repo le chat di Gemini esportate a mano.

Ogni prova scrive in `~/rumblingstone-prove-4050/<giorno>/` (fuori dal repo;
si cambia con `PROVE_DIR`), e `riporta.sh` ne fa un archivio da caricare nel
thread del progetto. Non serve fare `git push` dal portatile.

## Quale prova, per quale thread

| Prova | Thread che la aspetta | Script | Tempo stimato | Stato degli script |
|---|---|---|---|---|
| [Lettore della coerenza](#1-il-lettore-della-coerenza-della-storia) | «Verificare la coerenza della storia» | `scripts/prove-4050/lettore-coerenza.sh` | 10-20 min | pronto, mai girato sulla 4050 |
| [Prosa col 12B](#2-la-prosa-col-12b) | «LLM locale per la prosa» | `scripts/prove-4050/prosa.sh` | 1-1,5 h, più la lettura alla cieca | pronto; il 4B è già girato lì l'11/10 |
| [Immagini in posa](#3-le-immagini-dei-personaggi-in-posa) | «Immagini dei personaggi in posa con l'AI» | `scripts/prove-4050/immagini.sh` | 2-3 h la prima volta, poi 20-40 min a scena | pronto, mai girato su 6 GB |
| [Trascrizione della serata](#4-la-trascrizione-della-serata) | «Provare la trascrizione locale della serata» | lo script della trascrizione, nella PR #424 | una serata registrata | nella PR #424, non ancora su main |
| [Chat di Gemini](#5-le-chat-di-gemini-nel-repo) | inventario Gemini, D6 | `scripts/importa_gemini.py` | 10 min, più l'attesa di Takeout | pronto; formato Takeout non visto dal vivo |

I tempi sono stime fatte dai pesi dei modelli e dalle prove su altre macchine,
non misure sulla 4050. La prima misura vera è proprio quella che
riporterai.

## 0 · Una volta sola: controllare la macchina

```bash
cd ~/Scrivania/00_repo_github/RumblingStone
git switch main && git pull
scripts/prove-4050/controlla.sh
```

Lo script non installa niente. Controlla GPU, RAM libera, `distrobox`,
`podman`, `python3`, `git` e `curl`, il disco in `$HOME`, i box già creati e
se Ollama risponde, poi scrive tutto in `macchina.txt`. Esce con 1 solo se
manca qualcosa di bloccante (✗). Un «!» vuol dire che si può andare avanti, ma
è meglio liberare prima la RAM o il disco.

Prima di ogni prova chiudi **Steam e Firefox**: sull'ASUS il desktop occupa
già circa 11 GB di RAM, e i modelli che non stanno nella GPU finiscono lì.

## 1 · Il lettore della coerenza della storia

**Cosa misura.** Il verificatore della coerenza ([ADR-0125](../../plans/adr/ADR-0125-la-coerenza-della-storia-si-verifica-contro-state-yaml-solo-sui-fatti-strutturati.md))
trova i fatti nella prosa con un recupero più un lettore che risponde SÌ/NO.
Nel container il lettore è un 3B su CPU: su main ha dato 23 righe e 0 rilievi veri
([ESITO](../../plans/esperimenti/grafo-eventi-2026-11-12/ESITO.md)). La
domanda è se un 7B cambia il risultato. Il recupero è già fatto nel
container: le domande sono in
`plans/esperimenti/grafo-eventi-2026-11-12/misure/domande-ollama.json`, per il
repo e per la versione con gli errori inseriti apposta.

**Requisiti.** Il box `llm-locale` (se non c'è,
`scripts/llm-locale/setup-distrobox.sh`, circa 2 GB, una volta sola) e circa
5 GB di disco per `qwen2.5:7b` (Apache 2.0).

**Passi.** Servono due terminali.

```bash
# terminale A: il server, con un contesto corto (le domande sono brevi;
# con 32k token di contesto il 7B non starebbe più tutto nei 6 GB)
LLM_CTX=4096 scripts/llm-locale/start.sh

# terminale B
scripts/prove-4050/lettore-coerenza.sh            # default qwen2.5:7b
```

Se la interrompi con Ctrl-C, rilanciala: le risposte si salvano ogni 20 e la
corsa riparte da dove era. Si può provare un altro modello Ollama passando il
nome (`scripts/prove-4050/lettore-coerenza.sh gemma4:e4b-it-qat`): le risposte
si rileggono per qualunque nome.

**Cosa guardare.** Nella cartella `lettore-coerenza/` trovi `esito.txt`
(modello, domande, minuti, quanti SÌ e quanti NO), `gpu.txt` (memoria della GPU
prima e dopo) e `ollama-ps.json`. Se in `ollama-ps.json` `size_vram` è più
piccolo di `size`, una parte del modello è andata in RAM, e va detto quando si
riporta il tempo.

## 2 · La prosa col 12B

**Cosa misura.** È la seconda prova di [ADR-0089](../../plans/adr/ADR-0089-un-llm-locale-per-la-prosa-si-misura-prima.md).
Il 4B l'11/10 ha preso 42% in verifica (la soglia era 90%) e 0 su 10 alla
cieca (la soglia era 3). Il DM ha scelto di provare `gemma4:12b-it-qat`
prima di chiudere con un no. Se anche il 12B resta sotto 3 su 10, la domanda
si chiude per l'hardware di oggi.

**Requisiti.** Il box `llm-locale` e circa 8 GB di disco. Il 12B non sta tutto
nei 6 GB: Ollama mette il resto in RAM, e diventa più lento.

**Passi.**

```bash
# terminale A: il contesto di serie, 32k token (i prompt arrivano a ~25.500)
scripts/llm-locale/start.sh

# terminale B
scripts/prove-4050/prosa.sh                      # default gemma4:12b-it-qat
```

Lo script chiama `scripts/llm-locale/prova.sh`, che si ferma dopo il primo caso
(S02, il duello con Skullcrusher) per farti vedere testo e tempo, e ti chiede
se andare avanti. Se il primo caso supera i due minuti, rispondi «N» e
rilancia con meno norme nel prompt:
`LLM_CONTESTO=ridotto scripts/prove-4050/prosa.sh`.

Alla fine c'è il foglio alla cieca in
`plans/scrittura/prove-locali/foglio-gemma412bitqat-1.md`. Leggilo ad alta
voce e scrivi `1`, `2` o `=` dopo ogni «Preferito:», poi:

```bash
python3 scripts/banco_prosa_locale.py esito plans/scrittura/prove-locali/foglio-gemma412bitqat-1.md
cp plans/scrittura/prove-locali/foglio-gemma412bitqat-1.md ~/rumblingstone-prove-4050/$(date +%F)/prosa/
```

I passi sono pensati per un giorno solo. Se il foglio lo compili un altro
giorno, passa quel giorno a `riporta.sh`.

## 3 · Le immagini dei personaggi in posa

**Cosa misura.** La pipeline del 29/10 (SDXL, ControlNet union per la posa,
IP-Adapter per l'identità, poi dettaglio, scontorno, upscale e misura) è
girata solo su CPU, col profilo leggero SD1.5: 12-15 minuti a scena, ed
entrambe le scene di Hella bocciate per identità. La sua via GPU chiedeva 10
GB. Qui si prova sulla 4050 il profilo GPU vero, con tre adattamenti per i 6 GB:

- ComfyUI parte con `--lowvram` (`RS_COMFY_ARGS`), come la RTX A2000 da 4 GB misurata il 2026-10-08;
- un modello alla volta in memoria anche sul profilo GPU (`RS_LIBERA=1`);
- il giudice Qwen3-VL-4B (circa 8,5 GB in fp16) va con `device_map=auto`, in parte in VRAM e in parte in RAM (`RS_VLM_DEVICE`; `cpu` se `auto` va in errore di memoria).

La pipeline con questi adattamenti sta in
`plans/esperimenti/immagini-posa-4050-2026-11-15/`. È una prova di
laboratorio, non un'adozione: le decisioni D1-D4 del thread restano al DM.

**Requisiti.** Il box `comfyui` (se non c'è,
`scripts/comfyui-local/setup-distrobox.sh`, una volta sola). Circa 25 GB di
disco in `~/rumblingstone-prove-4050/immagini-lavoro/`: ComfyUI fissato al
commit provato, i due nodi, PyTorch CUDA in un venv suo, i pesi SDXL (circa
13 GB), il giudice e i modelli della misura. Tutti i pesi sono quelli del
cancello delle licenze del 29/10 (openrail++, Apache 2.0, BSD-3).

**Passi.** Il primo giro fa una sola scena con due semi, per i tempi:

```bash
scripts/prove-4050/immagini.sh                   # thorik_posa_artemis, 2 semi
```

Se regge, le dieci scene con quattro semi, come su Kaggle:

```bash
scripts/prove-4050/immagini.sh --tutte --semi 4
```

Se va in errore di memoria della GPU: `RS_VLM_DEVICE=cpu scripts/prove-4050/immagini.sh`.
Il confronto onesto col 29/10 è anche il profilo leggero sulla GPU:
`scripts/prove-4050/immagini.sh --profilo cpu` (SD1.5 + LCM, che sta largo nei 6 GB).

**Cosa guardare.** In `immagini-gpu/` (o `immagini-cpu/`) trovi
`riepilogo.json` con i secondi per scena, una cartella per scena con le misure
e `5_finale.png`, poi `console.log`, `comfy.log` e `gpu.txt`. Il ritratto
finale lo giudichi tu a occhio: il banco dice posa, identità e glitch, non se
è bello.

## 4 · La trascrizione della serata

La guida passo passo è nella PR #424 (la guida della trascrizione della
serata sul ramo `claude/project-thread-kcq3f8`, §2 per compilare whisper.cpp
con Vulkan in una distrobox `--nvidia`). Non la ripeto qui, perché finché la PR è
in bozza la fonte è quella. Oltre al portatile serve una serata registrata:
le misure M1-M3 si fanno su quella. Audio, trascrizioni e nomi dei giocatori
non vanno mai nel repo né nell'archivio di `riporta.sh`.

## 5 · Le chat di Gemini nel repo

L'inventario del 23/10 ([PR #284](../../plans/INVENTARIO-GEMINI-AISTUDIO-2026-10.md))
ha lasciato fuori due cose: le chat dell'app Gemini, che non stanno su Drive,
e le chat di AI Studio troppo grandi per il connettore. Per la D6 il DM ha
scelto «Esporto io, poi secondo giro». Lo script le trasforma in Markdown e fa
un indice ordinato per quante volte nominano la campagna. Non chiama Google e
non vuole chiavi.

**AI Studio.** Su Drive apri la cartella «Google AI Studio», seleziona tutto e
scegli «Scarica»: Drive fa uno zip. Poi:

```bash
python3 scripts/importa_gemini.py aistudio ~/Scaricati/drive-download-*.zip --out ~/gemini-md/aistudio
```

**App Gemini (Takeout).** Su <https://takeout.google.com> scegli
«Deseleziona tutto», poi solo «La mia attività». In «Tutti i dati di attività
inclusi» lascia solo «App Gemini», e nei formati scegli JSON se c'è (l'HTML va
bene lo stesso). Google manda il link per email, a volte dopo ore. Poi:

```bash
python3 scripts/importa_gemini.py takeout ~/Scaricati/takeout-*.zip --out ~/gemini-md/app
```

Le voci dei menu di Takeout le scrivo a memoria e possono essere diverse. Il
lettore di Takeout è provato su campioni sintetici, perché Google non documenta
il formato di «App Gemini». Se lo script dice «Nessuna chat riconosciuta»
(uscita 3), mandami l'elenco delle cartelle dell'archivio, senza il contenuto,
e adatto il lettore.

La cartella di uscita deve stare fuori dal repo: lo script si rifiuta di
scrivere dentro. Per il secondo giro carica `INDICE.md` e le chat che
nominano la campagna nel thread, oppure mettile nei file del progetto.

**Le immagini fatte a mano con Gemini** (i 14 casi del 31/10) vanno caricate nel
thread delle immagini col nome del caso e la fonte, per esempio
`hella_posa_artemis__gemini.png`, così il banco le misura senza indovinare.

## 6 · Mandare i risultati

```bash
scripts/prove-4050/riporta.sh                    # i risultati di oggi
scripts/prove-4050/riporta.sh 2026-11-16         # o di un altro giorno
```

Ne esce `~/rumblingstone-prove-4050/prove-4050-<giorno>.tar.gz`, con
`macchina.txt`, esiti, tempi, risposte, corse, misure e solo le immagini finali
e le generazioni sotto gli 8 MB. Pesi, venv, ComfyUI e immagini intermedie
restano fuori. Caricalo nel thread «Preparare le prove sul portatile RTX
4050», o in quello della prova. L'agente lo unisce al repo e lo registra
nell'ADR della prova:

- lettore: `estrai_rag.py --unisci` e `muta_grafo.py valuta`, poi ESITO.md;
- prosa: `plans/scrittura/RISULTATI.md` e ADR-0089;
- immagini: il confronto con le prove su CPU, nel thread delle immagini.

## Se qualcosa va storto

| Sintomo | Cosa fare |
|---|---|
| `distrobox enter` resta appeso su «host's nvidia integration» | È noto sull'ASUS: `box_pronto` aspetta tre minuti e prova lo stesso. Se non parte, `podman logs llm-locale \| tail` (o `comfyui`). |
| `Ollama non risponde su 11434` | Il terminale A con `start.sh` non è acceso o si è chiuso. |
| Il 7B è lento come una CPU | Guarda `gpu.txt`: se la memoria usata è sotto 1 GB la GPU non è passata nel box. Riavvia il box: `podman restart llm-locale`. |
| `CUDA out of memory` nelle immagini | Prima `RS_VLM_DEVICE=cpu`, poi `RS_COMFY_ARGS="--novram"`. Lo dici nel riepilogo. |
| Disco pieno | `PROVE_DIR=/srv/prove scripts/prove-4050/...` e, per i pesi delle immagini, `IMMAGINI_LAVORO=/srv/immagini`. |
