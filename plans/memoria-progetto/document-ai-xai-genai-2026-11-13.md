---
name: document-ai-xai-genai-2026-11-13
description: Thread «Applicare Document AI e Explainable AI» (Jfs 13/11): tecniche misurate una per PR; stato delle 8 candidate e della tecnica 3 sulla RTX 4050 (PR #466)
metadata:
  type: project
  modified: 2026-11-18T18:04:19.263Z
---

Jfs 2026-11-13: tecniche di document AI, explainable AI e GenAI con standard e librerie standard di fatto, misurate in testing e approvate secondo lo schema del repo; poi «continua con le prossime che mancano e che misurate migliorano». Rapporto in Claude Docs: https://claude.ai/artifact/7XtxdjPCpNTuQvmhhF52UR

Stato delle candidate (dettagli nelle voci MS e negli ADR):
- PDF/UA-1: #394 unita (ADR-0129, MS-0083).
- 1 glifi a colori: #398 unita.
- 2 PDF/A-2a: #416 unita (ADR-0131, MS-0106); veraPDF UA-1 e A-2a 21/21 booklet. A-4 incompatibile con UA-1 in typst 0.15.2.
- 4 provenienza IPTC: #418 unita (bd2ba318, ADR-0132, MS-0112); copie web 0→28/28; le 24 copie senza manifesto C2PA restano senza etichetta (card Jfs 13/11).
- 5 andata e ritorno del testo: misurata il 14/11 su 3,2 milioni di caratteri, nessun difetto, nessuna PR.
[riga riservata · sha256:a524de96]
- 6 Docling (servono etichette), 7 MAPIE (26 coppie, poche), 8 Captum/SHAP: poco margine. XAI: i cancelli sono deterministici e spiegano già (ADR-0124).

18/11: Jfs ha chiesto di ricontrollare la prova; tre errori dello script corretti nella PR #473, UNITA il 18/11 (merge 7b0587f4, MS-0168: impaginazione del libero, tetto token 700→1500, campi non testuali). Ora Jfs può lanciare la prova; nella misura guardare anche il conto `troncate` (non provato che Ollama rispetti maxLength).

Il difetto «Incantesimi focalizzati (bene, caos, legge o male)» di genera_creatura.py, trovato qui, è corretto da #468 (1908471a, MS-0163): alla PR della tecnica aggiornare il limite in PIANO.md.

veraPDF: Maven repo1 dà 429, usare repo.maven.apache.org; serve Avvio.java (plans/esperimenti/pdfua-2026-11-13/).

**How to apply:** una PR per tecnica con banco prima/dopo e regola scritta prima; non riproporre RAG 3B, gemma4 e4b, Prolog/clingo senza configurazione nuova. Vedi [[coerenza-storia-verificatore]] [[feedback-standard-di-fatto]] [[prove-portatile-4050]].
