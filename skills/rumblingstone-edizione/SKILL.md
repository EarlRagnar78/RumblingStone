---
name: rumblingstone-edizione
description: >
  Il mestiere dell'editore in RumblingStone: risponde di **cosa esce dal
  repo**. Compila il colophon (crediti, licenza, versione, data), separa
  Product Identity e Open Content (OGL 1.0a), passa il **gate d'uscita** (la
  checklist IP *prima* di consegnare) e tiene versione, ristampa ed errata.
  Si usa ogni volta che qualcosa esce dal repo o si parla di crediti, licenza
  o versione: "posso pubblicare", "posso condividere", "mando ai giocatori",
  "lo metto su GitHub", "consegno l'handout", "colophon", "crediti",
  "licenza", "OGL", "Product Identity", "Open Content", "diritti", "IP",
  "versione del volume", "ristampa", "errata", "che edizione è", "questo PDF
  è vecchio", "si può vendere", "posso monetizzare". ⚠️ Si usa ANCHE per la
  licenza di ciò che si vorrebbe **adottare**: "è open source?", "che licenza
  ha", "MIT", "GPL", "Creative Commons", "posso usare questo tool", "posso
  includere questo font/asset/modello", "i pesi di questo modello sono
  liberi?". Far entrare e far uscire è lo stesso mestiere.
---

# RumblingStone — Edizione

L'[editoria](../rumblingstone-editoria/SKILL.md) decide **come sta sulla pagina**;
questa skill decide **se quella pagina può uscire, con che nome e che versione**
([ADR-0024](../../plans/adr/ADR-0024-skill-edizione.md)).

> **La riga da ricordare**: un volume che non sa dire **da dove viene, quando è
> stato fatto e cosa se ne può fare** non è un'edizione, è un file.

## Quando no

La pagina è di [`rumblingstone-editoria`](../rumblingstone-editoria/SKILL.md), le immagini di [`rumblingstone-art-direction`](../rumblingstone-art-direction/SKILL.md), la prosa e le passate redazionali di [`rumblingstone-narrative-style`](../rumblingstone-narrative-style/SKILL.md), la profondità di un modulo di [`rumblingstone-module-standard`](../rumblingstone-module-standard/SKILL.md).
Non serve per: materiale che **resta nel repo** e non va a nessuno; il **PDF
settimanale per il tavolo**, che passa dal §1 in dieci secondi (caso
«giocatori») e non dall'intera skill; **decidere se pubblicare per soldi**, che
non è una domanda editoriale: è ADR-0005, e la risposta è già scritta.

## Fonti

1. [`GUIDA-CONDIVISIONE-IP.md`](../../docs/how-to/GUIDA-CONDIVISIONE-IP.md): §0 i
   casi, §4 il denaro, §7 il gate. **Se guida e skill divergono, vince la guida.**
2. [ADR-0005](../../plans/adr/ADR-0005-confini-ip-uso-non-commerciale.md) (uso
   non commerciale), [ADR-0023](../../plans/adr/ADR-0023-colophon-di-edizione.md)
   (il meccanismo del colophon), ADR-0024, ADR-0107 (chi si incontra).

## Procedura

1. In stesura, la tabella di licenza (§2).
2. Se il volume esce, il colophon (§3); alla seconda uscita, §4.
3. Prima di consegnare, il gate (§1).

### §1 · Il gate d'uscita: si passa PRIMA, non dopo

Le cinque domande della guida, §7, qui dove servono.

- [ ] **So in quale caso rientro** (§0 della guida): materiale originale ·
      derivato da Red Hand of Doom · SRD. Sono tre regimi diversi.
- [ ] **Va ai giocatori?** Solo file `pg-`, e il filtro anti-spoiler è passato.
- [ ] **Va in pubblico?** La nota di §3 in calce, niente `pregen-pcgen/`, **niente
      verbatim non-SRD**.
- [ ] **Ci sono illustrazioni?** Nessun nome di artista vivente, provenienza delle
      tavole nota (`PROVENIENZA.txt`).
- [ ] **C'è di mezzo del denaro?** ⛔ **Fermati** e leggi §4 della guida. Oggi la
      risposta è no ([ADR-0005](../../plans/adr/ADR-0005-confini-ip-uso-non-commerciale.md)).

⚠️ **Il gate non si supera «in buona fede».** Se una casella resta vuota, il
materiale non esce e si dice quale: non uscire con una riga di motivo è un esito
legittimo, uscire con un dubbio non lo è.

### §2 · L'igiene di licenza si compila in stesura, non a posteriori

La tabella («Formato d'uscita») si scrive **mentre si scrive il modulo**.
`10-stand-alone/L'abbazia Della Rotta Sicura/` la ha dentro: ha separato *Il
Nocchiero* e *la Signora del Frangente* (inventate) da Valkur e Umberlee
(Forgotten Realms non-SRD) **prima** del commit. Bonificare dopo costa dieci
volte tanto (il Palio, `…-VERIFICA-LEGALE-IP.md`, PR #47).

⚠️ **I due rami si tengono separati dal primo commit.** Il ramo Faerûn ricade
sotto il DMs Guild Community Content Agreement, incompatibile con MIT, GPL e
CC BY. Separarli dopo significa riscrivere.

### §3 · Il colophon: quando si compila

ADR-0023 è il meccanismo; le sette voci sono in «Formato d'uscita». **Chi non
dichiara `colophon` esce come prima**: è una possibilità, non una migrazione.

### §4 · L'edizione come oggetto: versione, ristampa, errata

**Il volume è alla seconda uscita, e qualcuno sa cosa è cambiato?**

- **Versione**: si alza quando cambia il contenuto. Due stampe con la stessa
  versione devono essere lo stesso testo.
- **Errata**: una correzione che arriva **dopo** che qualcuno ha stampato non si
  fa in silenzio nel master. Si scrive in un file `ERRATA-*.md` accanto al
  modulo, e **poi** si integra alzando la versione. Precedente:
  `ERRATA-ARC08-DESCRIZIONE-EPICA.md`.
- **Ristampa**: stesso contenuto, edizione nuova (carta diversa, impaginazione
  rifatta). Cambia `edizione`, non `versione`.

🟡 **Oggi è una convenzione, non un meccanismo**: niente lo verifica.
Diventerà un gate il giorno della prima ristampa vera (ADR-0024, «da rivisitare»).

### Chi si incontra sta nel capitolo (ADR-0107, accettata)

Un booklet del DM nuovo nasce con `"schede": "entrambe"` e
`"chi_si_incontra": true`: scheda d'entrata, ritratto e riquadro intero di chi
si incontra nel capitolo, la mappa dello scontro vicino alla scena,
l'appendice dei riquadri resta. Si tiene solo se il PDF migliora:
`misura_distanza_pagine.py` prima e dopo, nessuna persona più lontana dai suoi
numeri, `misura_stampa --check` verde. Se una persona peggiora (Terros: da 7 a
8 pagine) il booklet resta com'era e lo si scrive nell'ADR.

## Formato d'uscita

**La tabella di licenza**, dentro il modulo:

| Elemento | Stato | Nota |
|---|---|---|
| Creature | ✅ SRD 3.5 / OGL 1.0a | nessuna da manuali non-SRD |
| Classi PNG, oggetti magici | ✅ SRD | |
| Divinità | ⚠️ inventate o FR? | i nomi di Faerûn **non** sono SRD |
| Toponimi | ⚠️ inventati o reali? | un luogo reale va bene come riferimento visivo, non come nome nel prodotto |
| Tavole e immagini | ✅ originali | nessun asset di terzi, provenienza dichiarata |

**Il colophon**, chiave `colophon` del manifest:

| Voce | Cosa ci va | La trappola |
|---|---|---|
| `edizione` | come si chiama l'uscita | — |
| `versione` | `v1`, `v2`… | si alza **quando cambia il contenuto**, non a ogni compilazione |
| `data` | in chiaro, `AAAA-MM-GG` | ⚠️ **si scrive, non si deduce**: un `today()` rende il PDF diverso a ogni compilazione e toglie senso al gate di stampa |
| `autori` | chi l'ha scritto | ⛔ **mai un nome inventato**. Se non lo sai, la riga non esce |
| `basato_su` | SRD 3.5 · OGL 1.0a · l'opera originale | è la riga che ADR-0005 chiede e che viveva solo nelle guide |
| `licenza` | il regime d'uso di **questo** volume | «materiale del DM, uso privato» è una frase stampata, non da ripetere a voce |
| `nota` | dedica, ringraziamenti, avvertenza | — |

**L'esito del gate**: esce, o non esce con la casella vuota e il motivo.

## Prima di consegnare

- Le cinque caselle del §1 sono spuntate?
- `data` scritta e non dedotta, nessun autore inventato, `versione` alzata solo
  se cambia il contenuto, una correzione dopo la stampa in `ERRATA-*.md`?
- Con `chi_si_incontra`: misurato prima e dopo, `misura_stampa --check` verde?

## Cancelli deterministici

I controlli che non chiedono un giudizio, da far girare prima di consegnare.
Quello che qui non c'è resta giudizio di chi legge (registro delle norme).

- `python3 scripts/validate_booklets.py --stampa`: il gate d'uscita compila davvero.
- `python3 scripts/misura_distanza_pagine.py`: quanto sfoglia il DM nel volume stampato.
- `python3 scripts/misura_distanza_pagine.py --volume --manifest <manifest>`: la struttura del volume come gli AP, S1-S5 (ADR-0122, canale testing).
