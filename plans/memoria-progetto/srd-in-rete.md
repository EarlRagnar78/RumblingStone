---
name: srd-in-rete
description: Come raggiungere l'SRD 3.5 dal container quando d20srd.org e Firecrawl non vanno (mirror che rispondono a WebFetch)
metadata:
  type: reference
---

Il proxy blocca d20srd.org, d20pfsrd.com e web.archive.org (curl 000, WebFetch rifiutato), e i crediti di Firecrawl possono finire. WebSearch e WebFetch funzionano su mirror dell'SRD 3.5: `dungeons.fandom.com/wiki/SRD:<Nome>` (es. SRD:Elder_Xorn), `birthright.net/wiki` (sezione «D20 SRD (3.5)»), `www.rpgcrossing.com/srd/*.html`; per PF1e `legacy.aonprd.com`. A volte danno 429: si passa a un altro mirror. Si trova l'URL con WebSearch e poi si fa WebFetch su quello.

**Why:** il 2026-10-18 un giro intero di letture su ARC-07 aveva controllato i numeri SRD a memoria; con questi mirror la verifica ha trovato 9 discrepanze vere (PR #245).

**How to apply:** prima di dichiarare un numero «SRD», verificalo su uno di questi mirror e cita l'URL. Vale con [[scelte-inferred-versione-piu-forte]].

2026-11-19: dnd.arkalseif.info (D&D Tools, classi/talenti/incantesimi 3.5 dei manuali, es. /classes/stormsinger/index.html) aggiunto da Jfs ai domini dell'ambiente RumblingStone-corpus; curl risponde 200. Fonte non OGL: nel repo solo nomi e numeri (regola del 12/11); nei test solo riscontro, mai dipendenza di CI. Prima prova: il Cantore delle tempeste non dà Fulmine e chiede Attitudine Magica e Magia della Tempesta.
