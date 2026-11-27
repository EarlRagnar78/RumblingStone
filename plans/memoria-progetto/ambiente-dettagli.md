---
name: ambiente-dettagli
description: Dettagli di ambiente e storia degli agenti spostati dall'indice il 27/11 (Kaggle, rete, Python e canali, PR degli agenti #510-#515)
metadata:
  type: reference
---

Righe spostate testuali da MEMORY.md il 27/11/2026 (thread «Creare l'agente custode della memoria») per riportare l'indice sotto il tetto di 12 KB (ADR-0139). L'indice tiene un puntatore.

- Python 3.13; job 3.14 non bloccante. Tre canali Debian (ADR-0099); dal 25/11 (#516, e552c899, D8) stable e bloccanti: xdist nel job principale, cancello dei numeri, 14 conti PF1e, d eufonica, scheda delle skill, marche; un test che scrive nel repo va in SCRIVONO_NEL_REPO (conftest.py) o dà rossi a caso; passo pytest su main ×4 in 13 giorni senza causa nota (P2). Ruleset da aggiornare da Jfs; check richiesti su main = Validate + Build skill packages. → [[piattaforma-di-sviluppo]] [[piattaforma-promozioni-stable]]
- Rete: Hugging Face con HF_HUB_DISABLE_XET=1; aperti pytorch, SRD 3.5/PF1e, LanguageTool, Debian, typst, api.kaggle.com, www.kaggleusercontent.com, dnd.arkalseif.info (seconda fonte 3.5 non SRD, scelta di Jfs del 19/11: solo nomi e numeri nel repo, mai nei test CI); srd.dndtools.org bloccato. → [[hugging-face-rete]] [[ricerca-web-senza-firecrawl]] [[srd-in-rete]]
- Kaggle: nessun connettore; servono token nell'ambiente cloud RumblingStone-corpus (KAGGLE_API_TOKEN o KAGGLE_USERNAME+KAGGLE_KEY, li mette Jfs, mai in chat). Codice mai provato: /mnt/project-files/immagini-personaggi/pipeline-2026-10-29/kaggle/backend.py; istruzioni /mnt/project-files/kaggle-2026-11-18/IMPOSTAZIONI-KAGGLE.md. Funziona (telefono verificato 21/11, CLI 2.2.5 + `six`): notebook privato FLUX sulle tavole del Drappo 6/6 su T4; machine_shape vuoto, una sessione GPU alla volta; immagini dei PG mai caricate senza sì di Jfs. 25/11: HF_TOKEN (sola lettura gated) nell'ambiente per FLUX 3 Klein, caricarlo su Kaggle solo con riga scritta di Jfs; lavori Kaggle in coda per ore senza partire.
- #510 (14085a37) e #518 (879f0284, config a livello utente) su main, ADR-0146: hook di prosa, dodici agenti, cricchetto; misura sui primi 5 thread nuovi (baseline 0 skill/188 chiamate); chi coordina usa /mnt/project-files/agenti-2026-11-20/GUIDA-COORDINATORE.md → [[vincolo-skill-prosa]]
- #512 su main (4d3437b5, ADR-0148): verifica_px, verifica_rimandi, prove per agente. #515 su main (550c4402, ADR-0149): agente sincronizzatore-giocato e `sincronia_giocato.py` → [[sincronizzatore-giocato]]
