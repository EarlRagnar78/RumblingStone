# Fare le prove sul portatile con la RTX 4050

> Forma: **guida pratica** ([Diátaxis](../../plans/adr/ADR-0123-la-documentazione-segue-diataxis.md)).

Alcune prove del progetto non girano nel container dove lavora l'agente, perché
vogliono una GPU. Questa guida le raccoglie tutte per l'ASUS TUF F16 del DM
(RTX 4050 da 6 GB, 16 GB di RAM): cosa serve, i comandi esatti, quanto ci vuole
e come rimandare i risultati. Il kit gira su **Bazzite**, **Debian 13**,
**CachyOS** e **Windows** (attraverso WSL2), con gli stessi script e le stesse
verifiche ([ADR-0136](../../plans/adr/ADR-0136-il-kit-delle-prove-4050-e-uno-solo-per-quattro-sistemi.md)).
La stessa guida spiega come portare nel repo le chat di Gemini esportate a mano.

Ogni prova scrive in `~/rumblingstone-prove-4050/<giorno>/` (fuori dal repo;
si cambia con `PROVE_DIR`), e `riporta.sh` ne fa un archivio da caricare nel
thread del progetto. Non serve fare `git push` dal portatile.

## Quale prova, per quale thread

| Prova | Thread che la aspetta | Script | Tempo stimato | Stato degli script |
|---|---|---|---|---|
| [Lettore della coerenza](#1-il-lettore-della-coerenza-della-storia) | «Verificare la coerenza della storia» | `scripts/prove-4050/lettore-coerenza.sh` | 10-20 min | pronto, mai girato sulla 4050 |
| [Prosa col 12B](#2-la-prosa-col-12b) | «LLM locale per la prosa» | `scripts/prove-4050/prosa.sh` | 1-1,5 h, più la lettura alla cieca | pronto; il 4B è già girato lì l'11/10 |
| [Immagini in posa](#3-le-immagini-dei-personaggi-in-posa) | «Immagini dei personaggi in posa con l'AI» | `scripts/prove-4050/immagini.sh` | 2-3 h la prima volta, poi 20-40 min a scena | pronto, mai girato su 6 GB |
| [Tavole del Drappo con FLUX](#3-bis-le-tavole-del-drappo-con-flux2-klein) | D2 di RIPRESA-PR (arte del Drappo), la tua scelta tra A e B | `scripts/prove-4050/drappo-flux.sh` | 30-60 min la prima volta (8,3 GB di pesi), poi 1-3 min a tavola | pronto; grafo provato su CPU nel container, mai girato sulla 4050 |
| [Tattiche con la decodifica vincolata](#3-ter-le-tattiche-con-la-decodifica-vincolata) | «Applicare Document AI e Explainable AI», tecnica 3 | `scripts/prove-4050/schede-vincolate.sh` | 15-30 min col 7B già scaricato | pronto; provato con un Ollama finto, mai girato sulla 4050 |
| [Trascrizione sulla GPU](#4-la-trascrizione-sulla-gpu-e-quella-della-serata) | «Provare la trascrizione locale della serata» | `scripts/prove-4050/trascrizione-gpu.sh` | 20-30 min la prima volta (compilazione, 0,9 GB di modello, 290 MB di audio) | pronto; collaudato sulla CPU del container, mai girato sulla 4050 |
| [Trascrizione della serata](#4-la-trascrizione-sulla-gpu-e-quella-della-serata) | lo stesso | lo script della trascrizione, nella PR #424 | una serata registrata | nella PR #424, non ancora su main |
| [Chat di Gemini](#5-le-chat-di-gemini-nel-repo) | inventario Gemini, D6 | `scripts/importa_gemini.py` | 10 min, più l'attesa di Takeout | pronto; formato Takeout non visto dal vivo |

I tempi sono stime fatte dai pesi dei modelli e dalle prove su altre macchine,
non misure sulla 4050. La prima misura vera è proprio quella che
riporterai.

## Il kit in un comando

Tre comandi fanno tutto: preparare la macchina, lanciare le prove in fila,
verificarle e impacchettarle.

```bash
cd ~/Scrivania/00_repo_github/RumblingStone   # o dove hai il repo
git switch main && git pull
scripts/prove-4050/kit.sh installa            # una volta sola: pacchetti, box, controllo
scripts/prove-4050/kit.sh piano               # le prove, il thread che le aspetta, lo stato di oggi
scripts/prove-4050/kit.sh tutte               # tutte, nell'ordine di prove.json
scripts/prove-4050/kit.sh riporta             # verifica e archivio da caricare nel thread
scripts/prove-4050/kit.sh pulisci             # toglie i box (chiede conferma); modelli e risultati restano
```

`kit.sh tutte` lancia le prove di `scripts/prove-4050/prove.json` una dopo
l'altra: controllo della macchina, lettore della coerenza, decodifica
vincolata, trascrizione sulla GPU, tavole del Drappo, immagini in posa (una
scena) e per ultima la prosa, l'unica che ti chiede qualcosa a metà. Il server
Ollama lo accende e lo spegne il kit, col contesto che vuole ogni prova (4096
token per il lettore, 8192 per le schede, 32768 per la prosa): non serve il
secondo terminale. Una prova che fallisce non ferma le altre. Per saltarne
qualcuna: `kit.sh tutte --salta prosa,immagini`; per farne solo alcune:
`kit.sh esegui lettore-coerenza drappo-flux`. Il tempo stimato di tutto è
circa sei ore e mezza, la prima volta, più i download.

`scripts/prove-4050/verifica.py` (lo chiama `kit.sh` alla fine, e
`riporta.sh` prima dell'archivio) scrive `verifica.md` con lo stato di ogni
prova: **ok** (girata come doveva), **ko** (partita, ma qualcosa non torna, con
la nota), **da completare** (manca il foglio alla cieca della prosa) o
**non fatta**. «ok» non vuol dire che la tecnica migliora: quel verdetto lo dà
il thread della prova con la sua regola.

### I log di ogni giro

Tutto quello che il kit e le prove scrivono sul terminale, uscita ed errori,
finisce anche nella cartella `log/` del giorno
(`~/rumblingstone-prove-4050/<giorno>/log/`). Sul terminale vedi le stesse
righe di prima: il kit le copia con `tee`, e gli errori restano sullo stderr.

- `kit-<comando>-<ora>.log`: il giro intero di `kit.sh tutte`, `esegui`,
  `verifica`, `riporta` o `pulisci`, con il comando, la data, il sistema e la
  versione del repo in testa e il codice d'uscita in coda.
- `<prova>.log`: la parte di una prova, con il suo codice d'uscita in coda.
- `installa-<ora>.log`: `kit.sh installa` (anche con `--mostra`).
- `<script>-<ora>.log`: uno script lanciato da solo, per esempio
  `controlla.sh`. Lanciato dal kit non apre un secondo log.
- `avvisi.txt`: le righe con errori, avvisi, traceback e uscite diverse da
  zero, con il file e la riga da cui vengono. È la prima cosa da guardare
  quando qualcosa non è andato.

`kit.sh piano` e l'aiuto leggono soltanto e non scrivono log. Il server
Ollama scrive ancora il suo in `ollama-ctx<contesto>.log`. `riporta.sh` mette
i log nell'archivio fino a 64 MB l'uno.

### Cosa fa `installa` su ogni sistema

`scripts/prove-4050/installa.sh` riconosce il sistema da `/etc/os-release`.
Con `--mostra` stampa i comandi senza eseguirli; con `--driver` installa anche il
driver NVIDIA dove si può farlo da lì.

| Sistema | Sull'host | Dove girano le prove | Driver NVIDIA |
|---|---|---|---|
| Bazzite | niente (distrobox e podman ci sono già) | tre box Distrobox: `llm-locale`, `comfyui`, `whisper` | dall'immagine `bazzite-nvidia` |
| Debian 13 | `apt`: distrobox, podman, uidmap, python3, git, curl | gli stessi tre box | `--driver`: `nvidia-driver` dal ramo non-free (da abilitare nelle sorgenti se manca: lo script non le tocca), poi riavvio |
| CachyOS | `pacman`: distrobox, podman, python, git, curl; gli intervalli di uid per podman se mancano | gli stessi tre box | `--driver`: `chwd -a`, il rilevamento hardware di CachyOS, poi riavvio |
| Windows | WSL2 con Ubuntu 24.04, da `installa-windows.ps1` | dentro WSL2, senza box: Ollama, Python, CUDA e ffmpeg installati in Ubuntu | quello di Windows: in WSL2 non si installa nessun driver |

I box hanno un'immagine fissa (Ubuntu 24.04 per `llm-locale` e `comfyui`,
Fedora toolbox 43 per `whisper`, come nella guida della PR #424) e vedono la
GPU con `--nvidia`. Così sull'host non si installa niente oltre a distrobox e
podman, e le versioni degli strumenti sono le stesse su Bazzite, Debian e
CachyOS. Senza box si può lavorare anche su Debian:
`scripts/prove-4050/installa.sh --senza-box`, poi `RS_SENZA_BOX=1` davanti a
ogni comando del kit.

**Windows.** Da PowerShell come amministratore, nella copia del repo su Windows:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\prove-4050\installa-windows.ps1 -Memoria 12
```

Lo script `scripts/prove-4050/installa-windows.ps1` controlla il driver
(`nvidia-smi.exe`), installa WSL2 con Ubuntu 24.04 (la prima volta chiede di
riavviare e di creare l'utente di Ubuntu, poi lo si rilancia), clona il repo
nella home di Linux (non in `/mnt/c`, molto più lento) e lancia `installa.sh`
dentro WSL2. `-Memoria 12` scrive `%UserProfile%\.wslconfig` con 12 GB e 16 GB
di swap: di serie WSL2 prende metà della RAM, cioè 8 GB, pochi per FLUX e per
il 12B. Se il file c'è già non lo tocca. Poi le prove:

```powershell
wsl -d Ubuntu-24.04 -- bash -lc "cd ~/RumblingStone && scripts/prove-4050/kit.sh tutte"
```

L'archivio da caricare nel thread si trova da Esplora file in
`\\wsl$\Ubuntu-24.04\home\<utente>\rumblingstone-prove-4050\`.

`installa-windows.ps1` tiene il suo log con `Start-Transcript` in
`%USERPROFILE%\rumblingstone-prove-4050\log\installa-windows-<data-ora>.log`.
In Windows PowerShell 5.1 il transcript prende l'uscita di `wsl.exe` ma non i
suoi errori: quelli del kit dentro WSL2 stanno nel log di `installa.sh`.

**Cosa non è provato.** Nessuno di questi percorsi è girato su una macchina
vera: il container dell'agente non ha GPU, né Distrobox, né Windows. Nel
container sono provati il riconoscimento dei quattro sistemi e i comandi che
`installa.sh --mostra` stampa per ognuno, `kit.sh piano`, `verifica.py` su
risultati finti e la trascrizione su FLEURS sulla CPU (§4). Non sono provati:
il driver da `--driver` su Debian 13 e CachyOS, la GPU dentro WSL2,
`installa-windows.ps1` (nessun PowerShell nel container), e Ollama, ComfyUI e
whisper.cpp sulla 4050. Il primo giro su ogni sistema è anche il collaudo del
kit: se un passo si ferma, `verifica.md` e i log nell'archivio dicono dove.

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

## 3-bis · Le tavole del Drappo con FLUX.2 klein

**Cosa misura.** È il collaudo della D2 di
[PIANO-RIPRESA-PR-ABBANDONATE](../../plans/PIANO-RIPRESA-PR-ABBANDONATE.md):
le diciotto immagini del Drappo sono di Gemini, che non espone il seed, e la
domanda è se tenerle (A) o rigenerare tutto in locale con un seed fisso (B).
L'8/11 hai scelto di decidere guardando due o tre tavole fatte con
**FLUX.2 [klein] 4B** accanto a quelle di Gemini. Lo script ne fa tre, una per
tipo (il ritratto di Vanna, la Ruota, il Drappo come oggetto), con due semi
ciascuna, dagli stessi prompt del modulo
(`ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md`). Le immagini del modulo non
le tocca.

**Licenza.** Il 4B è Apache 2.0, come il suo codificatore di testo (Qwen3-4B) e
il VAE. Il [klein] 9B e il FLUX.2 [dev] no: girano sotto la FLUX Non-Commercial
License, e `comfyui_batch.py` li rifiuta per nome come già faceva con
FLUX.1 [dev] ([ADR-0019](../../plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md)).

**Ci sta in 6 GB?** Non nella versione di serie: Black Forest Labs dichiara
circa 13 GB di VRAM in bf16 (transformer 7,75 GB più Qwen3-4B 8 GB). Lo script
usa i pesi ridotti: il transformer in fp8 (4,07 GB, pubblicato da BFL) e il
Qwen3-4B in fp4 (3,85 GB, pubblicato da Comfy-Org), più il VAE (0,34 GB).
ComfyUI con `--lowvram` ne tiene in GPU uno alla volta: prima il
codificatore, poi il transformer. Sulla carta il transformer in fp8 più le
attivazioni a 832×1216 sta tra 5 e 6 GB, cioè al limite: se non ci sta,
ComfyUI ne lascia una parte in RAM e la tavola rallenta, senza errore. La RTX
4050 (Ada) calcola in fp8 ma non in fp4: il codificatore viene decompresso
mentre lavora, ed è più lento ma una volta sola per tavola. Il vincolo vero è
la **RAM**: i pesi in RAM sono circa 8,3 GB, e con il desktop che ne occupa 11
dei 16 serve chiudere Steam e Firefox. Lo script misura per ogni tavola i
secondi, il picco di VRAM e il picco di RAM di ComfyUI: sono quei numeri a
dire se ci sta, non questa stima.

**Requisiti.** Il box `comfyui`, come per le immagini in posa (se non c'è,
`scripts/comfyui-local/setup-distrobox.sh`). La cartella di lavoro è la stessa
di `immagini.sh` (`~/rumblingstone-prove-4050/immagini-lavoro/`): stesso
venv, ma un clone suo di ComfyUI (`ComfyUI-flux`, allo stesso commit
`0df1646`), così le due prove si possono lanciare in qualunque ordine. In più
circa 8,3 GB di pesi, che lo script scarica da Hugging Face e controlla contro
lo sha256 pubblicato. Se il venv non c'è ancora, lo script installa PyTorch
dall'indice `cu126`; se trova un PyTorch più vecchio della 2.8 (quello
dell'indice `cu124` è il 2.6) lo dice e scrive come aggiornarlo, perché sotto
la 2.8 ComfyUI gestisce la VRAM alla vecchia maniera. La versione usata
finisce in `riepilogo.json`.

**Passi.**

```bash
scripts/prove-4050/drappo-flux.sh                          # 3 tavole × 2 semi
scripts/prove-4050/drappo-flux.sh --solo tavola-la-cena --semi 4   # altre tavole, altri semi
```

Gli id sono quelli di `python3 scripts/comfyui_batch.py --lista`. ComfyUI
parte sulla porta 8189, così non urta un ComfyUI già acceso sulla 8188. Se va
in errore di memoria, `RS_COMFY_ARGS="--novram" scripts/prove-4050/drappo-flux.sh`,
e lo dici nel riepilogo.

**Cosa guardare.** Apri `~/rumblingstone-prove-4050/<giorno>/drappo-flux/confronto.html`:
per ogni tavola, Gemini a sinistra e i semi di FLUX a destra. Accanto ci sono
`confronto-<id>.jpg` (gli stessi affiancati, per il thread), `riepilogo.json`
(secondi, picchi di VRAM e di RAM per tavola) e `flux/seme-N/PROVENIENZA.txt`
con pesi, licenza e seed. Il confronto non è alla pari: le Gemini le hai scelte
tu tra più tentativi, qui ci sono due semi senza scarto. Il gate di rifiuto
del [README delle immagini](../../10-stand-alone/Il-Drappo-di-Tarsilia/ALLEGATI/immagini/README.md)
§6 si applica il giorno dopo. Due cose che FLUX klein non fa qui: a cfg 1 il
negativo («no text» e il resto) non entra nel calcolo, e i prompt sono quelli
scritti per SDXL, non riscritti per FLUX.

## 3-ter · Le tattiche con la decodifica vincolata

**Cosa misura.** È la tecnica 3 del thread «Applicare Document AI e
Explainable AI», che il 17/11 hai scelto di provare qui. Le schede di
`genera_creatura.py` hanno già i numeri giusti; la domanda è se un modello
locale, quando scrive le «Tattiche», nomina meno incantesimi e talenti che la
scheda non ha quando è vincolato a uno schema JSON (il campo `format` di
Ollama) invece di scrivere libero. Dodici schede, due bracci, tre ripetizioni:
72 risposte, giudicate dal controllo S8 del repo. Il piano e la regola del
verdetto, scritta prima della misura, sono in
[PIANO.md](../../plans/esperimenti/decodifica-vincolata-2026-11-17/PIANO.md).
Non scrive niente nel Bestiario.

**Requisiti.** Gli stessi del lettore: il server di
`scripts/llm-locale/start.sh` acceso in un altro terminale, e `qwen2.5:7b`
(lo scarica lo script se non c'è). Il contesto di serie basta: le schede sono
corte.

**Passi.**

```bash
# terminale A
scripts/llm-locale/start.sh
# terminale B
scripts/prove-4050/schede-vincolate.sh                  # qwen2.5:7b, 3 ripetizioni
RS_RIPETIZIONI=1 scripts/prove-4050/schede-vincolate.sh # una sola, per provare
```

Si salva a ogni risposta: se la interrompi, rilanciala e riparte. Alla fine
stampa la sintesi; `"migliora": true` vuol dire che la regola del piano è
soddisfatta, ma il verdetto lo scrivo io dopo aver letto le risposte, perché
il controllo può sbagliare in tutti e due i sensi.

**Cosa torna.** In `~/rumblingstone-prove-4050/<giorno>/schede-vincolate/`:
`misure.json` (sintesi e una riga per risposta), `risposte.json` (i testi del
modello), le schede con le tattiche in `libero/` e `vincolato/`, `gpu.txt` ed
`esito.txt`. Poi `riporta.sh`, come per le altre prove.

## 4 · La trascrizione sulla GPU e quella della serata

**Cosa misura.** La PR #424 (ADR-0135, in bozza) ha misurato whisper.cpp solo sulla CPU del container, e ha lasciato
aperta una domanda: la RTX 4050 si vede dal box, e quanto va veloce? La prova
`scripts/prove-4050/trascrizione-gpu.sh` risponde a quella, senza registrare
nessuno. Usa i parametri del thread della trascrizione: modello
`large-v3-turbo-q8_0` e `-l it -mc 0`, **senza VAD**; come audio le prime 40
righe di FLEURS `it_it/dev` (Google, CC BY 4.0), su cui la CPU del container ha
dato 2,3% di parole sbagliate. Il VAD sullo stesso audio porta l'errore a 8,6%,
perché perde parole nei tagli: per questo qui è spento. Sulla GPU il testo
deve tornare uguale; `verifica.py` segna «ko» sopra il 3,3% (2,3% più un punto
di tolleranza).

**Requisiti.** Il box `whisper` (lo crea `kit.sh installa`, con la ricetta del
§2 della guida della #424) e circa 2 GB di disco in
`~/rumblingstone-prove-4050/whisper-lavoro/`: whisper.cpp al commit misurato
nel container (`5922450`), il modello (0,9 GB) e l'archivio di FLEURS
(290 MB). Su WSL2 compila con CUDA invece di Vulkan
(`RS_WHISPER_BACKEND=cuda`, di serie lì); `RS_WHISPER_BACKEND=cpu` fa il
confronto onesto con la CPU del portatile.

**Passi.**

```bash
scripts/prove-4050/trascrizione-gpu.sh
```

**Cosa guardare.** In `trascrizione-gpu/`: `dispositivo.txt` (le righe di
avvio di whisper-cli: deve comparire la RTX 4050, non solo la CPU), `esito.txt`
(secondi, secondi di audio, quante volte il tempo reale), `grezza.txt` e
`riferimento.txt`. Le parole sbagliate le conta
`transcribe_session.py misura` della #424: se la #424 è già su main la prova
la fa da sé e scrive `misura.txt`, altrimenti la faccio io dall'archivio.

**La serata vera.** La guida passo passo è nella PR #424 (la guida della trascrizione della
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

Prima dell'archivio `riporta.sh` lancia `verifica.py`, che scrive
`verifica.md`; poi ne esce `~/rumblingstone-prove-4050/prove-4050-<giorno>.tar.gz`, con
`macchina.txt`, `verifica.md`, i log di `log/` con `avvisi.txt`, esiti, tempi, risposte, corse, misure e solo le
immagini finali e le generazioni sotto gli 8 MB. Pesi, venv, ComfyUI, l'audio
di FLEURS e le immagini intermedie restano fuori. Caricalo nel thread
«Preparare il kit unico di prove per la 4050», o in quello della prova. L'agente lo unisce al repo e lo registra
nell'ADR della prova:

- lettore: `estrai_rag.py --unisci` e `muta_grafo.py valuta`, poi ESITO.md;
- prosa: `plans/scrittura/RISULTATI.md` e ADR-0089;
- immagini: il confronto con le prove su CPU, nel thread delle immagini;
- tattiche vincolate: `misure.json` e `risposte.json` nel thread «Applicare Document AI e Explainable AI», con il verdetto secondo il piano;
- trascrizione sulla GPU: `esito.txt`, `dispositivo.txt` e la misura delle parole nel thread «Provare la trascrizione locale della serata»;
- Drappo: i `confronto-<id>.jpg` e `riepilogo.json` vanno nel thread «Scrivere lo script FLUX per il 4050», e la D2 si chiude con la tua scelta tra A e B.

## Se qualcosa va storto

| Sintomo | Cosa fare |
|---|---|
| «questo terminale gira dentro una sandbox Flatpak», oppure «sistema: altro 25.08» | Stai usando il terminale di un'applicazione installata da Flathub (un editor, per esempio): da lì GPU, distrobox e podman non si vedono. Apri il terminale del sistema (Ptyxis o Konsole) e rilancia; oppure `flatpak-spawn --host bash` se l'applicazione lo permette. |
| L'installazione si è interrotta (macchina spenta, rete caduta) | Rilancia `kit.sh installa`: i passi fatti non si rifanno, e un box rimasto a metà viene tolto e ricreato da solo. Per ripartire da zero: `kit.sh pulisci` (chiede conferma, toglie i box `llm-locale`, `comfyui` e `whisper`), poi `kit.sh installa`. I modelli scaricati, i pesi e i risultati stanno fuori dai box e non si perdono. Un solo box: `kit.sh pulisci comfyui`. |
| Dopo una prova il testo esce «a scaletta» (ogni riga parte dove finisce la precedente) | Il terminale è rimasto in modalità grezza dopo lo spegnimento del server nel box. Il kit ora lo rimette a posto da solo; se capita ancora, scrivi `stty sane` e premi Invio (anche se non vedi quello che scrivi) oppure `reset`. |
| `distrobox enter` resta appeso su «host's nvidia integration» | È noto sull'ASUS: il kit accende il box con `podman start` e legge il log a intervalli (`box_avvia`, cinque minuti al massimo: `RS_BOX_ATTESA`), poi entra lo stesso. Se non parte, `podman logs llm-locale \| tail` (o `comfyui`). |
| `verifica.md`: «ha lavorato un'altra scheda» sulla trascrizione | Vulkan ha scelto la scheda integrata: la memoria della NVIDIA non è salita mentre whisper girava. Guarda `trascrizione-gpu/dispositivo.txt` e `vram-durante.txt` e carica l'archivio lo stesso: è un risultato. |
| Una prova è uscita con un errore e il terminale è già scorso via | Apri `log/avvisi.txt` del giorno: dice file e riga; il resto è in `log/<prova>.log`. L'archivio di `riporta.sh` li contiene. |
| Su Windows lo script mostra lettere storpiate | Hai una copia vecchia di `installa-windows.ps1`: `git pull` (il file ora ha il BOM che Windows PowerShell 5.1 vuole). |
| `Ollama non risponde su 11434` | Il terminale A con `start.sh` non è acceso o si è chiuso. |
| Il 7B è lento come una CPU | Guarda `gpu.txt`: se la memoria usata è sotto 1 GB la GPU non è passata nel box. Riavvia il box: `podman restart llm-locale`. |
| `CUDA out of memory` nelle immagini | Prima `RS_VLM_DEVICE=cpu`, poi `RS_COMFY_ARGS="--novram"`. Lo dici nel riepilogo. |
| FLUX: una tavola impiega molti minuti | Guarda `riepilogo.json`: se `ram_comfyui_picco_mib` supera la RAM libera, il sistema sta usando lo swap. Chiudi Steam e Firefox e rilancia. |
| Debian 13: `nvidia-driver` non è tra i pacchetti | In `/etc/apt/sources.list.d/debian.sources` aggiungi `contrib non-free non-free-firmware` a `Components`, poi `sudo apt update` e `kit.sh installa --driver`. |
| CachyOS: podman dice «no subuid ranges found» | `installa.sh` li aggiunge; se l'hai saltato: `sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER && podman system migrate`. |
| WSL2: `nvidia-smi` non trovato dentro Ubuntu | Aggiorna il driver NVIDIA di Windows e lancia `wsl --update` da PowerShell; `nvidia-smi` sta in `/usr/lib/wsl/lib`. |
| WSL2: whisper non compila con CUDA | `RS_WHISPER_BACKEND=cpu scripts/prove-4050/trascrizione-gpu.sh` e lo dici nel riepilogo: la GPU su WSL2 resta da capire. |
| `kit.sh`: «Ollama non risponde» | Guarda `ollama-ctx<N>.log` nella cartella del giorno: di solito è il box che non parte (prima riga di questa tabella). |
| Disco pieno | `PROVE_DIR=/srv/prove scripts/prove-4050/...` e, per i pesi delle immagini, `IMMAGINI_LAVORO=/srv/immagini`. |
