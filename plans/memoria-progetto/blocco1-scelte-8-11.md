---
name: blocco1-scelte-8-11
description: Blocco 1 «Scelte dell'8/11» chiuso il 2026-11-10 (PR #358, #360, #364, #366, #368); decisioni di Jfs, promozioni 23-24/11, lezioni
metadata:
  type: project
  modified: 2026-11-10T00:08:52.199Z
---

Thread «Scelte dell'8/11», ramo `claude/project-thread-9srfje`, una PR per voce; a CI verde il merge lo fa il thread padre (audit), nell'ordine #364, #363, #365.

- Voce 1: PR #358 unita. Voce 2: PR #360 unita il 2026-11-09.
- Voce 1-ter: **PR #364** (ADR-0118 «un numero entra solo se la regola lo calcola» + `conformita_statblocchi.py --cancello-numeri`, cricchetto su `docs/audit/numeri-baseline.json`, non bloccante fino al 2026-11-23). Unita il 2026-11-10 (421dbd0), scarti 37 → 0.
- Decisioni di Jfs dentro la #364 (card, 9-10/11):
  - **AU delle unità = attacco della creatura singola, senza +2** (il «+2 effetto massa» è della variante 2d6; errore mio entrato con la #360). Fanteria Hobgoblin +6, Orog +13, orchi +5, giganti randello +16 e massi +8, ettin +12.
  - **Baliste AU +10** con un mastro artigliere nano Guerriero 8 a ogni pezzo (`Bestiario/mostri/nano-mastro-artigliere-guerriero8-cr8.md`); SRD: −4 a un Medio che punta una balista.
  - **Doom Hand = Chierico 8, GS 8** (non più Chierico 7/Warpriest 1). GS dei blocchi «creatura singola» = livelli di classe.
  - **Carta dei giganti del libretto: due macigni per settore a d20 + 9** (era uno a d20 + 14), in ARC08-18, ARC08-19, DEF-2; `tre_giorni.py` con `MACIGNI = (2, 9)` dà la stessa battaglia.
- Scelte di build mie, rifiutabili: duergar Competenza Armi Esotiche; monaco Arma Focalizzata catena; drow stocco perfetto; Gorthak e Madre Dana Arma Focalizzata; talenti/armi perfette nei blocchi singola di ARC08-01.
- Limiti noti del cancello: non rifà il GS dai livelli; per un'unità senza etichetta prende il primo attacco in mischia della scheda; 75 file in prosa non coperti (lotti nella roadmap del padre).
- Voce 3: PR #366 unita il 2026-11-10 (873bacc). Voce 4: **PR #368** aperta il 2026-11-10 (ADR-0120, «d» eufonica), ultima del blocco; unita il 2026-11-10 (f65d78e): **blocco 1 chiuso**, thread risolto. Il controllo è in canale testing (avviso in validate_lingua, errore non bloccante con `--d-eufonica`), promozione dal 2026-11-24.
- Lezione: un controllo nuovo nasce sempre in testing (ADR-0099), anche col corpus a zero; il padre lo verifica prima del merge.
- Lezione: dopo ogni merge di main cercare i segni di conflitto (`git grep -nE '^(<<<<<<< |>>>>>>> )'`): la CI non li vede e la #365 li aveva lasciati in CHANGELOG.md.
- `plans/esperimenti/sistemi-plugin-2026-11-07/impronte.py --confronta` non è in CI: dopo ogni modifica a Bestiario o conformita_statblocchi va lanciato e, se le differenze sono attese, `--scrivi`.

Lezioni sui controlli in locale: `ci.sh <dir>` con path assoluto e PATH del venv dello scratchpad davanti; `test_validate_pg` instabile in parallelo, `test_fase1` rosso anche su main. Dopo modifiche al Bestiario: `impronta_creature.py --scrivi` e `build_monster_catalog.py`; una fazione nuova con un solo membro fa fallire i test (usare una esistente). Dopo righe nei piani: `memoria.py`. Una nota in scheda che cita «Arma Focalizzata» senza arma fa contare il talento al cancello. Il ramo remoto viene cancellato al merge: `git fetch origin main` da solo, poi `checkout -B` da origin/main. → [[feedback-numeri-piu-forti-calcolati]]

Seguito 2026-11-11 (Jfs: «superare i limiti dell'ADR-0120 in modo deterministico, misurando»): **PR #377** (unita il 2026-11-12, merge 21400285), emendamento di ADR-0120. Banco di semina `plans/esperimenti/d-eufonica-limiti-2026-11-11/semina.py` (3.944 errori seminati): regex 98,38% → 100%, LanguageTool 84,25%. validate_lingua legge 1.309 righe rientrate di prosa (markdown-it-py opzionale in requirements.txt, ripiego stdlib), marchio `<!-- sic -->`. Jfs ha scelto a card il parser CommonMark. Non fatto: revisione Sourcery/Codex (budget), LanguageTool dopo l'11/11. Metodo riusabile: quando un cancello è a zero, il miglioramento si misura seminando errori noti, non contando i rilievi. Dopo aver toccato un reference di una skill: `indice_references.py --emit`.
