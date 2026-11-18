# ADR-0136 — Il kit delle prove 4050 è uno solo per quattro sistemi

**Stato**: proposta (2026-11-17), in prova fino al primo giro completo sull'ASUS
**Data**: 2026-11-17
**Decisione-fonte**: il DM (Jfs), 2026-11-17, thread «Preparare il kit unico di prove per la 4050»: «un kit completo con tutti i test necessari da fare con gli script e le configurazioni e i deploy automatici e le verifiche dei test (bazzite os, debian 13, chaucy os, windows os)». «chaucy os» si legge **CachyOS** (derivata di Arch). Per Windows il DM ha scelto sulla card del 17/11 la consigliata: **WSL2 con Ubuntu 24.04**.
**Rapporti**: estende `scripts/prove-4050/` (PR #447, MS-0141) e la guida [GUIDA-PROVE-PORTATILE-4050](../../docs/how-to/GUIDA-PROVE-PORTATILE-4050.md). Riusa senza cambiarle le prove di [ADR-0125](ADR-0125-la-coerenza-della-storia-si-verifica-contro-state-yaml-solo-sui-fatti-strutturati.md) (lettore), [ADR-0089](ADR-0089-un-llm-locale-per-la-prosa-si-misura-prima.md) (prosa), la D2 di RIPRESA-PR (FLUX, #461), la tecnica 3 di Document AI (#466) e aggiunge la parte GPU di ADR-0135 (trascrizione, #424, in bozza).

## Contesto

Sei prove aspettano la GPU dell'ASUS (RTX 4050 da 6 GB, 16 GB di RAM), ognuna
con uno script suo, e ognuna chiede di accendere a mano il server giusto in un
secondo terminale. Gli script davano per scontato Bazzite: `distrobox` e
`podman` già installati, il box creato dalla prova stessa. Il DM vuole poterle
lanciare tutte insieme, anche da Debian 13, CachyOS o Windows, con
l'installazione fatta dal kit e un controllo che dica cosa è girato e cosa no.
La trascrizione aveva una domanda aperta che non richiede una serata
registrata: whisper.cpp vede la 4050 dal box, e quanto va veloce?

## Decisione

1. **Un ingresso solo**: `scripts/prove-4050/kit.sh` (`installa`, `piano`,
   `tutte`, `esegui`, `verifica`, `riporta`). L'elenco delle prove, il loro
   ordine, il thread che le aspetta, il contesto del server e i file attesi
   stanno in `scripts/prove-4050/prove.json`. Una prova nuova si aggiunge lì.
2. **Gli strumenti stanno in un Distrobox su ogni Linux** (`llm-locale`,
   `comfyui`, `whisper`), con immagine fissa e `--nvidia`. Sull'host si
   installano solo distrobox e podman, col gestore del sistema: niente su
   Bazzite, `apt` su Debian 13, `pacman` su CachyOS. È lo standard di fatto
   per le distribuzioni immutabili ed è già quello del repo (ADR-0089, comfyui-local).
3. **Windows passa da WSL2 con Ubuntu 24.04**, in modo «diretto» (niente box):
   `installa-windows.ps1` prepara WSL2 e lancia lo stesso `installa.sh`. La GPU
   arriva dal driver di Windows, come documentano NVIDIA e Microsoft per CUDA
   su WSL2. Un solo codice delle prove per quattro sistemi.
4. **Il server Ollama lo gestisce il kit**, col contesto che dichiara la prova
   (4096 il lettore, 8192 le schede, 32768 la prosa). Se il DM l'ha già acceso,
   il kit usa il suo e lo dice.
5. **Verifica automatica**: `verifica.py` (solo libreria standard) legge
   `prove.json` e i risultati e scrive `verifica.md`/`verifica.json` con
   ok, ko, da completare, non fatta. «ok» vuol dire che la prova è girata come
   doveva, non che la tecnica migliora: il verdetto resta del thread della prova.
6. **Trascrizione sulla GPU senza registrare nessuno**: `trascrizione-gpu.sh`
   con i parametri chiesti dal thread della trascrizione (large-v3-turbo-q8_0,
   `-l it -mc 0`, senza VAD, prime 40 righe di FLEURS it_it/dev, CC BY 4.0). Soglia: 2,3% di parole
   sbagliate, il valore della CPU del container; `verifica.py` tollera un punto.

Nessuna libreria nuova: bash, Python della libreria standard, PowerShell di
Windows. I pacchetti dell'host sono quelli delle distribuzioni.

## Conseguenze

- Il DM lancia `kit.sh installa` una volta e `kit.sh tutte` per tutte le
  prove; l'archivio di `riporta.sh` contiene `verifica.md`.
- `scripts/llm-locale/` e `scripts/comfyui-local/` entrano nel box con
  `nel_box` invece che con `distrobox enter`: su Linux il comportamento non
  cambia, su WSL2 (o con `RS_SENZA_BOX=1`) girano sul sistema.
- **Non provato** (il container non ha GPU, Distrobox né Windows): i box su
  Debian 13 e CachyOS, il driver installato con `--driver`, CUDA dentro WSL2,
  `installa-windows.ps1`, e ogni prova sulla 4050. Provati nel container: il
  riconoscimento dei sistemi, i comandi di `installa.sh --mostra` per ognuno,
  `kit.sh piano`, `verifica.py` su risultati finti, e `trascrizione-gpu.sh`
  per intero sulla CPU (numeri in MS della PR).
- Su WSL2 whisper.cpp compila con CUDA 12.0 di Ubuntu e `g++-12`: è il punto
  più fragile; se non compila, `RS_WHISPER_BACKEND=cpu` e lo si dice.
- La decisione si rivede dopo il primo giro completo sull'ASUS: se un
  sistema non regge, si toglie dalla tabella della guida invece di tenerlo
  «supportato» senza prova.
