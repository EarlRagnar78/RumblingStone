---
name: documentazione-a-ogni-milestone
description: Jfs 2026-11-09: ogni milestone deterministica si chiude con aggiornamento completo di doc, Mermaid, guide, ADR e dm.py; strumenti via testing→stable
metadata:
  type: feedback
---
Jfs (2026-11-09): per ogni milestone della roadmap si prevede l'aggiornamento completo della documentazione e dell'integrazione: diagrammi Mermaid in docs/ARCHITETTURA.md, README e docs/INDEX.md, guide d'uso e di sviluppo, stato degli ADR della piattaforma, comando in dm.py. I canali testing/stable restano come per gli strumenti in prova (ADR-0099) e per il passaggio 3.13→3.14. Ogni thread aggiorna la sua area.

**Why:** il 9/11 ARCHITETTURA era fermo al 7/11 e senza ADR-0109…0117, e dm.py non aveva comandi per i sistemi: la roadmap non aveva il passo.
**How to apply:** il thread padre non unisce la milestone successiva finché il passo doc non c'è; la regola è in DECISIONI-E-ROADMAP.md, sezione «Ogni milestone chiude con la documentazione». Vedi [[thread-padre-pr]].
