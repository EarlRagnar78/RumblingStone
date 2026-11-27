# ADR-0108 — I cancelli deterministici stanno in ogni skill, con un cricchetto

**Stato**: accettata (2026-11-03, Jfs: «quello che migliora in modo che sia std e non solo ricerca»)
**Data**: 2026-11-03
**Decisione-fonte**: il DM (Jfs), 2026-11-03: *«è necessario mettere delle guardrail anche a tutte le skills e anche a quelle dello stile»* e *«per ogni tecnica, skill, plugin, guardrail e tecnica avanzata che migliora, adottare nel repo come standard»*.
**Rapporti**: estende [ADR-0107](ADR-0107-chi-si-incontra-sta-nel-capitolo.md) (la misura sul PDF), [ADR-0091](ADR-0091-la-scheda-del-png-ha-una-forma.md) (i recinti ora controllati), [ADR-0070](ADR-0070-l-apparato-di-lavoro-non-va-in-stampa-e-ogni-pagina-si-stampa-una-volta.md) (le note di lavoro); il giudice della prosa resta [ADR-0093](ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md). Ricerca in [RICERCA-GUARDRAIL-E-TECNICHE-2026-11](../RICERCA-GUARDRAIL-E-TECNICHE-2026-11.md).

## Contesto

Il DM, il 2026-11-03: *«è necessario mettere delle guardrail anche a tutte le
skills, anche a quelle dello stile, per migliorare in maniera deterministica
le avventure e i booklet»*. La lettura alla cieca della prova di ADR-0107 ha
trovato nel booklet della serata una CD sbagliata, una scurovisione mancante e
note di lavoro stampate. Nessun controllo le guardava: i boss recintati di
ADR-0091 erano fuori da `conformita_statblocchi`, e le note «[INFERRED…]»
restano in stampa di proposito. Solo 7 skill su 18 nominavano un comando che
le verifica, nessuna in un posto fisso.

## Decisione

1. Ogni `skills/*/SKILL.md` chiude con la sezione **«Cancelli
   deterministici»**: i comandi che la verificano senza giudizio. Un test
   (`test_cancelli_delle_skill.py`) chiede la sezione e controlla che ogni
   comando sia uno script dichiarato in `tools.manifest.json`.
2. `conformita_statblocchi --master` legge anche i recinti di ADR-0091 e
   controlla pf, CA, CD di soffio, schiacciare e presenza, *corrompere
   l'acqua*, le voci ereditate con «come A.n» e la scurovisione dei tipi che
   la hanno nell'SRD.
3. Le **note di lavoro in stampa** si contano per volume
   (`misura_standard_tavolo`).
4. Per 2 e 3 vale un **cricchetto** nei test: un rilievo in più è rosso. Il
   tetto scende a mano quando il DM corregge il master, perché le correzioni
   sono canone e i master hanno proprietari diversi.
5. `misura_distanza_pagine.py` misura sul PDF stampato la distanza fra scena e
   numeri. È un indicatore, non un cancello.
6. Una tecnica entra come standard solo se una prova ne misura il guadagno sul
   repo. Gli embedding per le ripetizioni (1 rilievo in più su 362 box) e il
   rilevatore dei box telecomando (precisione 2 su 15) non entrano.

## Alternative considerate

- **Cancello duro, tetto zero**: renderebbe rossa la CI su master di altri
  thread (DEF-4 è anche della PR #305) per correzioni che solo il DM può
  decidere.
- **Togliere le note «[INFERRED]» in stampa**: nasconderebbe al DM un numero
  senza fonte. Meglio contarle e farle sparire chiudendole.
- **Un LLM come giudice delle skill di stile**: la letteratura dà un accordo
  basso con gli esperti, e il giudice della prosa resta il cieco (ADR-0093).
- **Transformer come standard** (embedding, NLI): provati o senza etichette
  su cui provarli; nessun guadagno misurato che valga la dipendenza.

## Conseguenze

- Una skill nuova senza la sezione rompe i test.
- I tetti di oggi, dopo la PR #305 (che ha corretto il *corrompere l'acqua*
  del Vecchio e la scurovisione di Zog'tar): 4 conti nei master (DEF-3: 1,
  DEF-4: 3), 59 note di lavoro in stampa (Notte e Alba 18, Serata
  Resurrezione 19, Volume Mille Anni 18, Terros 3, Giardino PF1e 1).
- Le correzioni vanno al DM come proposte. Non le applica questo ramo.

## Da rivedere se

- il cricchetto blocca una PR per un rilievo che è un falso positivo: si
  corregge il controllo, non il tetto;
- ci sono almeno 30 contraddizioni di fatto etichettate: allora si prova
  l'NLI a frasi (SummaC) contro `coerenza_campagna`.

## Adozione (2026-11-03)

Accettata insieme ad ADR-0107. I cancelli adottati restano quelli misurati
(conti dei recinti, note in stampa, distanza in pagine, sezione nelle skill).
L'NLI, rimandata qui per mancanza di etichette, è stata provata fino in fondo
(ricerca §7): F1 0,86 su coppie etichettate, 0 contraddizioni nuove nelle
prime 30 sul repo vero. Non entra: non sa di quale creatura parla una frase.

Seconda verifica (2026-11-03, 14:13, richiesta del DM): le cinque prove
scartate rifatte con una configurazione rigorosa (ricerca §8). Due
migliorano e si adottano come indicatori: `misura_ripetizioni_frasi.py`
(6 ripetizioni vere invece di 1) e `misura_box_telecomando.py` (precisione
dal 13% al 50%). NLI, varianti dei nomi e numeri incrociati restano fuori:
la seconda misura conferma la prima.

Terza verifica (2026-11-03, 17:06-17:13, richiesta del DM: «correggi, non
solo indicatore», «diventino std misurando il miglioramento»):

- **NLI sulla fedeltà del riscritto** (ricerca §9): sulle 26 coppie
  etichettate alla cieca dal DM F1 0,83 contro 0,62 dei soli numeri. Entra in
  `ciclo_prosa revisione` e `misura` come **correzione automatica**: la riga
  che contraddice l'originale torna com'era, e `misura` esce con 1.
- **Box telecomando**: i 2 veri corretti nel testo, `--check` cancello in CI
  (4 colpi → 2, entrambi accettati e motivati).
- **Ripetizioni fra box**: le 2 vere nei master corrette (21 → 19 coppie),
  `--check` cancello locale con l'elenco delle accettate.
- **Lythiel**: il cortile allineato (esterno, dopo la cerimonia).
