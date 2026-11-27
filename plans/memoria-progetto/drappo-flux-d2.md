---
name: drappo-flux-d2
description: RIPRESA-PR D2 (arte del Drappo): script FLUX.2 klein 4B per la 4050, PR #461 (16/11), cosa è misurato e cosa no
metadata:
  type: project
---

PR #461 unita il 2026-11-16 (merge 8cf54678 sopra af28c7ea, MS-0156; prossima MS-0157; voce pr/461 del registro dei rami ancora «in-volo», da portare a «portato»): `scripts/prove-4050/drappo-flux.sh` + `drappo_flux.py`, guida GUIDA-PROVE-PORTATILE-4050 §3-bis. Tre tavole (ritratto-vanna, tavola-la-ruota, il-drappo) × 2 semi, accanto alle Gemini in confronto.html. Pesi: FLUX.2-klein-4b-fp8 (BFL) + Qwen3-4B fp4 e VAE (Comfy-Org/Flux-2-Klein-4B), Apache 2.0, sha256 nel codice. FLUX.2 dev e klein 9B = non commerciali, rifiutati da comfyui_batch.py.

Misurato: grafo completo su CPU nel container (553 s a tavola, RAM picco 13,4 GB in fp32). Non misurato: la 4050 (stima 5-6 GB VRAM al picco; rischio vero è la RAM). Immagini della prova CPU in /mnt/project-files/drappo-flux-2026-11-16/.

**Why:** Jfs ha scelto sulla card del 16/11 «prima lo script, poi A o B guardando».
**How to apply:** la D2 resta aperta finché Jfs non carica l'archivio di riporta.sh e sceglie A o B; poi chiudere la riga D2 nel piano e il registro dei rami. Vedi [[prove-portatile-4050]].


**18/11, ricontrollo chiesto da Jfs:** PR #482 (unita il 18/11, merge 1295e3a8, MS-0182) corregge quattro difetti della #461: Gemini con blocco C2PA che Pillow non apriva (2 tavole su 3), clone di ComfyUI condiviso con immagini.sh (ora `immagini-lavoro/ComfyUI-flux`), PyTorch da cu124 fermo al 2.6 (ora cu126), pipefail che saltava l'esito. Chi ha lanciato la #461 cancella `immagini-lavoro/ComfyUI` prima di immagini.sh. immagini.sh e setup-distrobox.sh passati anch'essi a cu126 (RS_TORCH_INDEX). Sulla 4050 ancora mai girato. Domanda hardware di Jfs (5070/5080/L40S, memoria unificata): risposto nel thread; non ha detto quali portatili, budget, né se il Drappo si vende.

**25/11:** Jfs ha visto il confronto Kaggle del 21/11 (Vanna FLUX ok ma mani pulite; Ruota e Drappo meglio Gemini) e ha chiesto lo standard dei prompt: PR #519 in bozza (ADR-0150 proposta, MS-0222, `scripts/misura_prompt_immagine.py`, blocchi `didascalia` in §9 di PROMPT-RITRATTI-E-TAVOLE.md, guida §2.4-bis/ter). Fatto: le Gemini vengono dagli stessi prompt a etichette; Gemini li espande, klein no. Prova cieca chiesta da Jfs fra Opus e Fable come scrittori di didascalie: incarico, consegne e chiave in /mnt/project-files/drappo-flux-kaggle-2026-11-25/gara/ (chiave.json: non dirla a Jfs prima della sua scelta). Kaggle il 25/11 ha tenuto i lavori in coda oltre 4 ore (max 2 sessioni GPU, nessun annulla da CLI, i segreti non seguono `kernels push`): ripiego su CPU nel container. FLUX 3 Klein: Jfs lo vuole solo se gratuito e su Kaggle gratuita; serve che accetti la licenza su HF e metta `HF_TOKEN` (fine-grained, solo quel repo) nell'ambiente; mai provato.

**25/11 sera, esito del cieco (un seme, CPU):** Jfs sceglie Vanna = A (mani da rovinare di più), Ruota = Gemini, Drappo = Gemini. Chiave in /mnt/project-files/drappo-flux-kaggle-2026-11-25/gara/chiave.json (aperta). Riprova mani (A2) esagerata: sembrano ferite e sangue, non lavoro; età resa ~55 invece di fine trenta. Esito in ADR-0150 (PR #519, 54206905). Kaggle: i due notebook in coda dalle 08:19 alle 22:00 UTC senza partire. Dataset Kaggle rs-hf-token-temporaneo ancora da cancellare a prova FLUX 3 finita.
**25/11 notte:** Jfs sulla card: tavole (Ruota, Drappo) restano Gemini, Vanna in sospeso fino a FLUX 3; «preferisco le mani di Gemini» (sporche e scure, senza sangue). A3 (mani per causa e materia, «thirty-eight years old») corregge età e sangue: vanna-mani-gemini-A-A3.jpg. Piano e ADR aggiornati (735afd40).
**26/11:** Jfs vede su Kaggle quota GPU 0:19/30 h e, lanciando a mano, «position in the queue is 817»: la coda è capacità di Kaggle, non quota né errore nostro. Due notebook ancora QUEUED alle 07:31 UTC del 26/11.
**26/11 Canva (chiesto da Jfs):** stesse tre tavole col prompt corto v1 via connettore Canva generate-image: Vanna MAHcBG02uGQ (1664x2496), Ruota MAHcBPpLkSE, Drappo MAHcBEpnsVI. Dal container si vedono solo miniature 200 px: media.canva.com bloccato dal proxy; il giudizio a piena risoluzione lo fa Jfs dai link canva.com/M/<id>. Stesso giorno Jfs: «come non detto, meglio il test con flux e gemini»: Canva fuori dal confronto D2. Giudizio di Jfs a piena risoluzione: solo Vanna Canva vicina a Gemini, Ruota e Drappo con errori di direzione e glitch.
**27/11:** rs-drappo-ab COMPLETE: 27/27 su T4 (10-17 s, 8,8 GB VRAM), uscite in /mnt/project-files/drappo-flux-kaggle-2026-11-27/. rs-drappo-flux3 ancora in coda.
