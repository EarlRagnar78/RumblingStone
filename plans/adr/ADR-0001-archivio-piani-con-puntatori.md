# ADR-0001 — Archivio piani in `plans/` con file-puntatore ai vecchi percorsi

**Stato**: accettata
**Data**: 2026-07-10
**Decisione-fonte**: K-D3 (DM 2026-07-10, domanda 3) + regola d'oro 5 del piano trasversale ("non cancellare file")

## Contesto

I piani di revisione (ARC-07/08/09 + trasversale) erano sparsi tra la root
del repo e tre cartelle-arco: nessuna vista d'insieme, nessuna % di
completamento consultabile, nessun changelog unificato dei lotti. Decine di
file di gioco citano i piani per **nome file** (es. "vedi
`PIANO-REVISIONE-ARC07-...md` §0 D2"), quindi uno spostamento secco
romperebbe la tracciabilità.

## Decisione

Tutti i piani vivono in `plans/` con tre file di servizio: `INDEX.md`
(stato · % · lotti rimanenti · gate, più i "prossimi passaggi" in bianco),
`CHANGELOG.md` (una riga per lotto chiuso, nello stesso commit che lo
chiude) e `adr/`. Ogni vecchio percorso conserva un **file-puntatore di
~4 righe** con lo stesso nome, che rimanda a `plans/`.

## Conseguenze

- Una sola pagina (`plans/INDEX.md`) risponde a "a che punto siamo?".
- I riferimenti per nome file continuano a risolvere (via puntatore).
- Costo: doppio file per piano (puntatore + master) — accettato perché i
  puntatori sono minuscoli e auto-esplicativi.
- I piani futuri nascono direttamente in `plans/` (niente più puntatori).
