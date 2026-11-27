---
name: prove-portatile-4050
[riga riservata · sha256:d651c548]
metadata:
  type: project
  modified: 2026-11-15T07:34:58.940Z
---

PR #447 unita il 15/11/2026 (MS-0141): uno script per prova in `scripts/prove-4050/`, guida `docs/how-to/GUIDA-PROVE-PORTATILE-4050.md`, `importa_gemini.py`.

Risultati: Jfs carica nel thread `~/rumblingstone-prove-4050/prove-4050-<giorno>.tar.gz` (da `riporta.sh`); l'agente unisce: lettore con `estrai_rag.py --unisci` + `muta_grafo.py valuta` (radice mutato rifatta con `muta_grafo.py prepara`; serve venv torch CPU + sentence-transformers), prosa in RISULTATI.md/ADR-0089, immagini nel thread immagini.

[riga riservata · sha256:92f58ab7]

**Why:** Jfs (15/11) chiedeva se ogni thread in attesa della 4050 avesse istruzioni e script lanciabili; solo la prosa li aveva.
**How to apply:** nessuno script è mai girato su GPU; le manopole RS_COMFY_ARGS/RS_LIBERA/RS_VLM_DEVICE sono non provate. Lettore col server a LLM_CTX=4096. La tecnica 3 di Document AI ha lo script dal 17/11 (#466 unita 02b1764e, schede-vincolate.sh, §3-ter della guida); la trascrizione resta in #424. Vedi [[coerenza-storia-verificatore]] [[llm-locale-prosa-valutazione]] [[immagini-personaggi-in-posa]] [[trascrizione-serata]] [[inventario-gemini-aistudio]].

Ricontrollo del 18/11 (chiesto da Jfs): PR #475 unita il 18/11 (merge 1da2233d, MS-0181) con nove errori corretti (anche PyTorch da cu126 invece di cu124, RS_TORCH_INDEX) nei file di questo thread. Divisione dei file col thread del kit (#469, ADR-0136): qui lettore-coerenza.sh, prosa.sh, immagini.sh, la pipeline delle immagini, leggi_ollama.py, importa_gemini.py; al kit tutto il resto di scripts/prove-4050/ e la guida.

[riga riservata · sha256:3b8b8018]

**Log del kit (#492, merge 517a3e79 il 19/11, MS-0201).** Ogni giro scrive `<giorno>/log/`: `kit-<comando>-<ora>.log`, `<prova>.log` col codice d'uscita, `installa-<ora>.log`, `avvisi.txt` (errori/avvisi con file e riga); Windows: transcript in `%USERPROFILE%\rumblingstone-prove-4050\log\`. Da chiedere a Jfs al prossimo giro: com'è `avvisi.txt`, e se le barre di avanzamento senza tty (distrobox enter dietro tee) danno fastidio. Il `.ps1` non è mai stato eseguito.
