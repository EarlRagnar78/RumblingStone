---
name: ricerca-web-senza-firecrawl
description: Se Firecrawl non ha crediti o fallisce, la ricerca web continua con WebSearch/WebFetch o curl via proxy, senza fermarsi (richiesta di Jfs)
metadata:
  type: feedback
---

Quando Firecrawl è senza crediti o rifiuta, la ricerca non si ferma: si usano WebSearch e WebFetch (via ToolSearch), o curl/python attraverso il proxy del container, e lo si dice nel rapporto. Il 2026-10-18 i crediti Firecrawl erano finiti e la ricerca sulla prosa è andata avanti così.

**Why:** Jfs, 2026-10-18: «se non ha firecrawl usa altri metodi per fare webscraper».

**How to apply:** nei prompt degli agenti di ricerca web indicare subito l'alternativa. Vedi anche [[ricerca-archivi-wizards]] (archive.org bloccato da curl e WebFetch, lì Firecrawl era l'unica via).
