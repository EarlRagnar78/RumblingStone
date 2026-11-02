# Un modello di linguaggio locale in container (la prova di ADR-0089)

Un server **Ollama** (MIT) dentro un **Distrobox** con la GPU dell'host, su
`http://127.0.0.1:11434`. Serve a una cosa sola: far scrivere i dieci casi del
banco di L11 a un modello che gira sulla macchina del DM, e misurarli con
`voto_scrittura.py` e con le coppie alla cieca. Il perché, le soglie e i limiti
sono in [ADR-0089](../../plans/adr/ADR-0089-un-llm-locale-per-la-prosa-si-misura-prima.md).

L'architettura è quella di [`comfyui-local/`](../comfyui-local/README.md): un box
isolato, niente installato sull'OS immutabile di Bazzite, i dati dove dice una
variabile, gli stessi quattro gesti (setup, scarica, start, stop). Cambia il
servizio, non il modo.

| Variabile | Default | A che serve |
|---|---|---|
| `LLM_DIR` | `scripts/llm-locale/dati/` (gitignorato) | dove stanno i pesi |
| `LLM_BOX` | `llm-locale` | il nome del box |
| `LLM_PORTA` | `11434` | la porta del server |
| `LLM_CTX` | `32768` | il contesto. I prompt veri arrivano a ~25.500 token più la risposta. Con 24.576 il server ne ha tagliati quattro su dieci a metà, senza errore (2026-10-10) |

## Quale modello, su quale macchina

`comune.sh` lo sceglie da solo (`consiglia`), dai tag di
[ollama.com/library/gemma4](https://ollama.com/library/gemma4), tutti Apache 2.0:

| Macchina | GPU | RAM | Modello | Peso |
|---|---|---|---|---|
| ASUS TUF F16, Bazzite | RTX 4050, 6 GB | 16 GB | `gemma4:e4b-it-qat`, poi `gemma4:12b-it-qat` | 6,1 GB · 7,2 GB |
| Dell Precision 5560 | RTX A2000, 4 GB | 32 GB | `gemma4:26b` (MoE, 3,8 miliardi di parametri attivi) | 16-19 GB |

Sull'ASUS il 12B non sta tutto nella GPU: Ollama mette il resto in RAM, e con
11 GB già occupati dal desktop la RAM non basta. **Chiudi Steam e Firefox
prima di avviare il server.**

## La prova da zero, su Bazzite

Serve solo il repo. Distrobox e Podman su Bazzite ci sono già, `python3`
pure.

```bash
cd ~/Scrivania/00_repo_github/RumblingStone      # il tuo clone
git fetch origin
git switch claude/project-thread-zxxz0m           # finché la #234 non è su main

nvidia-smi                 # deve elencare la RTX 4050
distrobox version          # deve rispondere

scripts/llm-locale/setup-distrobox.sh     # una tantum: box + Ollama (~2 GB)
```

L'ultima riga del setup stampa il modello consigliato. Poi due terminali:

```bash
# terminale A: il server (resta acceso; Ctrl-C per fermarlo)
scripts/llm-locale/start.sh

# terminale B
scripts/llm-locale/scarica-modello.sh     # il consigliato: gemma4:e4b-it-qat
scripts/llm-locale/prova.sh               # un caso per i tempi, poi i dieci, poi il voto
```

`prova.sh` si ferma dopo il primo caso (S02, il duello con Skullcrusher), ti fa
leggere il testo e il tempo, e chiede se andare avanti. Il primo caso sta in
`plans/scrittura/prove-locali/`, fuori dal voto e fuori da git. I dieci casi
vanno in `plans/scrittura/corse/L-<modello>-1/`, dove `voto_scrittura` li vota
come le corse degli agenti. Alla fine trovi il foglio alla cieca da compilare
leggendo ad alta voce.

Il secondo modello:

```bash
scripts/llm-locale/scarica-modello.sh gemma4:12b-it-qat
scripts/llm-locale/prova.sh gemma4:12b-it-qat
```

Se il primo caso impiega troppo (più di due minuti), riprova con meno norme nel
prompt: `LLM_CONTESTO=ridotto scripts/llm-locale/prova.sh`.

## Cosa riportare

L'uscita di `prova.sh` (i secondi per caso e la tabella del voto), e la riga di
`distrobox enter llm-locale -- ollama ps` mentre il modello lavora: dice quanto
del modello sta nella GPU e quanto nella CPU. Le cartelle `corse/L-*` si
committano sul ramo insieme a `plans/scrittura/voti.json`, che `prova.sh`
riscrive: la CI controlla che i due siano allineati. `prova.sh` stampa il
comando alla fine.

## Se qualcosa non va

| Sintomo | Causa probabile | Rimedio |
|---|---|---|
| `start.sh` resta fermo su «host's nvidia integration» | `distrobox enter` segue il log del box, e su Bazzite quel log si ferma | gli script ora avviano il box con `podman start` e controllano il log a intervalli (`box_pronto` in `comune.sh`): si vedono dei puntini e poi «pronto» |
| il setup dice che il box non vede la GPU | il box è stato creato senza `--nvidia` | `distrobox rm llm-locale --force` e rilancia il setup |
| `ollama ps` dice `100% CPU` | la GPU non arriva nel box, o il modello non ci sta | controlla `distrobox enter llm-locale -- nvidia-smi`; prova il modello più piccolo |
| il testo del caso ignora le norme | il contesto è stato tagliato | verifica che il server sia partito con `start.sh` (che imposta `LLM_CTX`) e non a mano |
| `banco_prosa_locale` esce con codice 3 | il server non risponde | il terminale A è ancora acceso? |
| esce con codice 4, «superano il contesto del server» | `LLM_CTX` troppo basso per i prompt | riavvia `start.sh` con un `LLM_CTX` più alto, o `LLM_CONTESTO=ridotto` |
| esce con codice 5, «casi guasti» | il server ha tagliato un prompt, o una risposta è vuota o interrotta al tetto | la corsa finisce in `prove-locali/`, fuori dal voto: leggi gli avvisi in `corsa.json` e rifalla |

Per togliere tutto: `scripts/llm-locale/stop.sh`, poi
`distrobox rm llm-locale --force` e `rm -rf scripts/llm-locale/dati`.

## Fonti

- Ollama: <https://github.com/ollama/ollama> (MIT), installazione Linux da
  <https://ollama.com/install.sh>, variabili `OLLAMA_HOST`, `OLLAMA_MODELS`,
  `OLLAMA_CONTEXT_LENGTH`
- Gemma 4: <https://ollama.com/library/gemma4>, licenza Apache 2.0
- Distrobox: <https://distrobox.it/>, `distrobox create --nvidia`
