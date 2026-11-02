# Corse scartate

Corse che non misurano il generatore perché il server le ha guastate. Restano
qui da leggere, fuori da `corse/`, quindi fuori dal voto di `voto_scrittura`.

| Corsa | Perché è scartata |
|---|---|
| `L-gemma4e4bitqat-1` (2026-10-10) | Ollama girava con 24.576 token di contesto. Quattro prompt (S02, S03, S04, S07) erano più lunghi e il server li ha tagliati a 12.291 token, senza errore. S09 ha riempito il contesto e la risposta è vuota; S07 si è fermato al tetto di 1.500 token. Vedi [`RISULTATI.md`](../RISULTATI.md) e ADR-0089. |
