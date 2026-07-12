# ADR-0004 — Homebrewery self-hosted in locale per l'editor a due pannelli

**Stato**: accettata
**Data**: 2026-07-12
**Decisione-fonte**: K-D5 (DM 2026-07-12: "Voglio la soluzione B, con i comandi dalla documentazione ufficiale") — chiude la domanda aperta Q2 del piano DM-TOOLKIT

## Contesto

Il DM vuole l'esperienza a due pannelli (markdown + anteprima stile
Manuale del Giocatore in tempo reale) vista su Homebrewery, "con la
stessa qualità", per i materiali hype/handout della campagna. Le
alternative valutate: (A) incollare i `.hb.md` sul sito pubblico
naturalcrit (qualità identica ma il contenuto — RHoD privato — finisce
su server terzi), (C) previewer statico in-repo (privato ma qualità
approssimata, richiede di reimplementare il parser V3).

## Decisione

Self-hostare **The Homebrewery** (naturalcrit, licenza MIT) in locale:
stesso codice del sito ⇒ **qualità identica per costruzione**, contenuto
mai fuori dal PC del DM, funziona offline. I comandi di installazione
sono ripresi **alla lettera dalla documentazione ufficiale** (README.md
sezione *Installation* e README.DOCKER.md del repo naturalcrit/homebrewery,
recuperati 2026-07-12), mai inventati. Nel repo vivono solo la guida
(`scripts/homebrew-local/README.md`), due wrapper sottili
(`setup.sh`/`start.sh`) e il sottocomando `dm.py hype setup|start`;
il clone di Homebrewery è gitignorato (software di terze parti).

## Conseguenze

- Editor due-pannelli identico su `http://localhost:8000`; privacy totale.
- Prerequisiti sul PC del DM: Node ≥16, MongoDB Community, git (o Docker).
- L'aggiornamento di Homebrewery è a carico del DM (`git pull` +
  `npm install`, o la procedura Docker ufficiale) — documentato nella guida.
- Il sito pubblico resta il fallback a zero setup (opzione A) quando si
  è fuori casa.
