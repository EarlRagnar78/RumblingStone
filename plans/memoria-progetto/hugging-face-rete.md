---
name: hugging-face-rete
description: Hugging Face dal container: funziona dal 2026-10-22 dopo l'apertura del CDN da parte di Jfs, ma serve HF_HUB_DISABLE_XET=1
metadata:
  type: reference
  modified: 2026-10-22T11:10:42.416Z
---

Prova del 2026-10-22 (thread «Stanza contro spaCy»): `huggingface.co/api/...` dà 200, ma ogni file di modello (es. stanfordnlp/stanza-it default.zip) fa redirect 302 a `us.aws.cdn.hf.co`, che il proxy rifiuta (403). Rifiutati anche cdn-lfs.hf.co, cdn-lfs-us-1.huggingface.co, cas-bridge.xethub.hf.co, nlp.stanford.edu, downloads.cs.stanford.edu, lindat.mff.cuni.cz (UDPipe). pypi.org funziona (il pacchetto stanza si installa, il modello no).

**How to apply:** prima di promettere un modello HF, provare `curl -I` sul file `resolve/main/...` e seguire il redirect. Per sbloccarlo Jfs deve aggiungere `us.aws.cdn.hf.co` (e per sicurezza `cas-bridge.xethub.hf.co`) agli Allowed domains dell'ambiente cloud; in alternativa la prova va fatta sul suo PC. Collegato a [[ricerca-web-senza-firecrawl]].


Aggiornamento 2026-10-22: Jfs ha aperto il dominio, ora i modelli si scaricano. Il protocollo Xet (cas-server.xethub.hf.co) resta chiuso: usare sempre `HF_HUB_DISABLE_XET=1` con huggingface_hub, stanza o transformers. PyTorch arriva da pypi (download.pytorch.org è chiuso).
