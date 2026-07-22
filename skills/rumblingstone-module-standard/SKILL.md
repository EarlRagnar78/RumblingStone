---
name: rumblingstone-module-standard
description: >
  Quality standard for RumblingStone DEFINITIVE module masters — the depth,
  structure, and finish level required when consolidating or revising an arc
  beat into a single self-sufficient AP-quality document (benchmark: Red Hand
  of Doom + Pathfinder 1e APs). Use WHENEVER creating or revising a
  "master definitivo", consolidating multiple file generations into one,
  auditing an arc for a final version, or when asked for "qualità AP",
  "modulo definitivo", "consolidamento", "versione finale", "audit dell'arco",
  "ARC*-DEF-*". Encodes the DM-approved checklist (2026-07-22, PR #61) so
  agents know exactly how deep to go — sections, prose level, tactics format,
  budget accounting — without re-deriving it. Reference implementation:
  07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md.
---

# RumblingStone — Standard dei Master Definitivi (qualità modulo-AP)

**Scopo.** Quando un arco viene consolidato in "master definitivi" (un file
autosufficiente per beat, niente salti tra versioni), il risultato deve
essere **oggettivamente paragonabile ai migliori moduli D&D 3.5 / Pathfinder
1e** (Red Hand of Doom; AP Paizo). Questa skill è la **checklist vincolante**
approvata dal DM (2026-07-22, PR #61). Esemplare di riferimento:
`07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md`.

**Regola di fondo: il definitivo è PIÙ completo delle fonti, mai un
riassunto.** Prima di scrivere, scansionare TUTTI i file dell'arco (anche
deprecati e `_ARCHIVIO/`) e recuperare ogni contenuto valido: prove, esempi
numerici, read-aloud, ambienti dinamici, hook. Ciò che si scarta va motivato.

## Struttura obbligatoria del master (nell'ordine)

1. **Header canone**: cosa sostituisce/fonde (elenco file-fonte), stato al
   tavolo, ordine di gioco (D2), sistema (3.5 SRD, max PF1e; MAI 5e —
   niente lair action/vantaggio/reazioni), scala mappe 1,5 m/quadretto.
2. **INDICE** del modulo (tabella § → contenuto).
3. **Quickstart DM** (1 pagina): dove siete, chi c'è (composizione REALE),
   cosa stampare, come finisce, countdown/orologi attivi.
4. **Quick-Reference** (1 pagina stampabile): TUTTE le CD, pf e soglie dei
   nemici, il giro del boss in 5 righe, contromosse dei PG; box **Supporto
   PF1e** dichiarato dove il 3.5 è vago (zero-G, polveri, oggetti in caduta…).
5. **Highlight asimmetrici per PG**: cosa sa/vive/percepisce CIASCUN PG
   (la conoscenza è divisa; chi è morto/assente percepisce solo echi).
   Ogni PG ha un beat suo; i PG assenti non parlano lucidamente.
6. **Atlante delle Zone**: per OGNI ambiente — read-aloud di prosa NUOVA
   (non copia-incolla), callout meccanici del terreno stile RHoD,
   "cosa succede qui". + **Ambiente dinamico** (elementi che agiscono da
   soli: crolli, polveri, hazard innescabili) + **Eventi di viaggio (d6)**.
7. **Incontri**: sempre ≥2 vie non combattive (Premium Design), grigi
   (nemici con Want propri, mai malvagità gratuita); statblock 3.5 completi
   (Touch/Flat/BAB/Lotta espliciti); **Tattiche round-per-round stile RHoD**
   scritte dal punto di vista del MOSTRO, agganciate alle coordinate della
   mappa, con **soglie pf/morale**, debolezze caratteriali, e riga
   **Sviluppi**; nota di calibrazione numerica + tabella DPR per i boss.
8. **Boss**: read-aloud del risveglio/ingresso (pressione fisica: la si
   sente nei denti, non solo si vede), scenografia con leve tattiche,
   coreografia del primo scambio che chiude su un decision point dei
   giocatori, **sidebar "Scalare lo scontro"** (party più forte/più debole/
   composizione diversa/PG abbattuto).
9. **Contingenze "Se i PG fanno X"**: parlare col boss, rubare l'obiettivo,
   fuggire, sacrilegio, cadute ambientali, riposare (costo in countdown), e
   SEMPRE la riga **sconfitta** (mai TPK gratuito: la sconfitta costa tempo/
   orgoglio/countdown, non la campagna).
10. **Riti/prove corali**: le sfide chiave coinvolgono la volontà E i poteri
    di TUTTI i PG insieme (ruoli nominati, prove che si aiutano a vicenda,
    malus corporali, crescendo da giocare a ritmo).
11. **Conseguenze**: pannelli/echi nel mondo ("La Forgia Ricorda" o
    equivalente) + **Echo Ledger** del beat (evento → eco → quando riemerge
    → file che lo gestisce).
12. **Avanzamento**: budget **PX sezione-per-sezione** (incluse prove non
    combattive e story award, con totale/PG e lettura verso il livello) +
    **tesoro PREGENERATO** itemizzato per sezione (oggetti specifici con
    valori, sorprese nascoste con CD) + ricchezza speciale/artefatti
    (conteggio separato, con valore di riferimento).
13. **Ponte** al beat successivo + **Handout & Asset** (stampabili, immagini
    per momento d'uso, cue musicali).
14. **Mappe ASCII ultra-clear**: emoji-grid con coordinate lettera×numero,
    scala 1,5 m, posizioni PG/PNG/villain, elementi ambientali dinamici,
    legenda con dilemmi tattici e scenografia.

## Regole di lavorazione (sempre)

- **Coerenza batte stile**: caricare `rumblingstone-campaign` (coherence +
  state.md) e `rumblingstone-narrative-style` (mix di pilastri per scena)
  PRIMA di scrivere. Fatti non attestati → `[INFERRED — needs DM
  confirmation]`, mai inventati. Contraddizioni → flag al DM, mai retcon.
- **Un solo profilo per boss/PNG** nel repo: doppioni risolti, non segnalati
  e basta (le immagini "orfane" si riassegnano a ciò che esiste).
- **Prosa**: una scena = un pilastro lead (+2 support); dettaglio sensoriale
  concreto per paragrafo; il divino/gli artefatti si SENTONO nel corpo;
  una riga di storia profonda per luogo (costruttore+età+cicatrice).
- I file-fonte assorbiti: banner di deprecazione con puntatore al master,
  poi `_ARCHIVIO/` a consolidamento chiuso (deroga D10 approvata dal DM).
- Chiusura lotto: changelog `plans/CHANGELOG.md` (gate ADR-0009), catalogo
  mostri rigenerato se il master aggiunge statblock, `state.md` §8 se il
  canone cambia.

## Self-check finale (prima di consegnare)

1. Un DM può giocare la sessione **con questo solo file** aperto? (stampe a
   parte)
2. Ogni fonte (anche deprecata) è stata scansionata e il meglio recuperato?
3. C'è almeno: 1 scelta grigia, 1 prova corale, 1 sconfitta gestita,
   1 eco a lungo termine, 1 momento per OGNI PG?
4. Zero meccaniche 5e? CD in italiano? Statblock con Touch/Flat/BAB/Lotta?
5. PX+tesoro pregenerato quadrano sezione per sezione?
6. Le mappe hanno coordinate, posizioni e dilemmi tattici in legenda?
