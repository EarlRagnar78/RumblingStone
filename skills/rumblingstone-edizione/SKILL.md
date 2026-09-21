---
name: rumblingstone-edizione
description: >
  Il mestiere dell'editore applicato a RumblingStone: chi risponde di **cosa esce
  dal repo**. Il colophon (crediti, licenza, versione, data), le dichiarazioni
  Product Identity / Open Content, il **gate d'uscita** — la checklist IP che va
  passata *prima* di consegnare, non dopo — e l'edizione come oggetto: versione,
  ristampa, errata. Use WHENEVER si sta per far uscire qualcosa dal repo o si
  parla di crediti, licenza o versione: "posso pubblicare", "posso condividere",
  "mando ai giocatori", "lo metto su GitHub", "consegno l'handout", "colophon",
  "crediti", "licenza", "OGL", "Product Identity", "Open Content", "diritti",
  "IP", "versione del volume", "ristampa", "errata", "che edizione è", "questo
  PDF è vecchio", "si può vendere", "posso monetizzare". ⚠️ Trigger ANCHE quando
  la licenza riguarda uno **strumento o un materiale che si vorrebbe adottare**,
  non solo ciò che esce: "è open source?", "che licenza ha", "MIT", "GPL",
  "Creative Commons", "posso usare questo tool", "posso includere questo
  font/asset/modello", "i pesi di questo modello sono liberi?" — valutare se una
  cosa può ENTRARE è lo stesso mestiere di valutare se può uscire.
---

# RumblingStone — Edizione

L'[editoria](../rumblingstone-editoria/SKILL.md) decide **come sta sulla pagina**.
Questa skill decide **se quella pagina può uscire, con che nome e che versione**.
È il mestiere che in un colophon Paizo occupa tre righe — *editore*, *Product
Identity*, *Open Content* — e che qui esisteva come guida che nessun agente
apriva ([ADR-0024](../../plans/adr/ADR-0024-skill-edizione.md)).

> **La riga da ricordare**: un volume che non sa dire **da dove viene, quando è
> stato fatto e cosa se ne può fare** non è un'edizione, è un file.

---

## §1 · Il gate d'uscita — si passa PRIMA, non dopo

Cinque domande. Vengono da
[`GUIDA-CONDIVISIONE-IP.md`](../../docs/guides/GUIDA-CONDIVISIONE-IP.md) §7, che è
la fonte: **se le due divergono, vince la guida**. Stanno qui perché è qui che un
agente le incontra al momento giusto.

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

---

## §2 · L'igiene di licenza si compila in stesura, non a posteriori

Il modo che funziona non è controllare alla fine: è **scrivere la tabella mentre
si scrive il modulo**, elemento per elemento.

| Elemento | Stato | Nota |
|---|---|---|
| Creature | ✅ SRD 3.5 / OGL 1.0a | nessuna da manuali non-SRD |
| Classi PNG, oggetti magici | ✅ SRD | |
| Divinità | ⚠️ inventate o FR? | i nomi di Faerûn **non** sono SRD |
| Toponimi | ⚠️ inventati o reali? | un luogo reale va bene come riferimento visivo, non come nome nel prodotto |
| Tavole e immagini | ✅ originali | nessun asset di terzi, provenienza dichiarata |

**Esemplare, e non è teoria**: `10-stand-alone/L'abbazia Della Rotta Sicura/` ha
questa tabella dentro il modulo. Ha separato *Il Nocchiero* e *la Signora del
Frangente* (inventate) da Valkur e Umberlee (Forgotten Realms non-SRD) **prima**
del commit. Bonificare dopo costa dieci volte tanto: l'arco del Palio lo ha
dimostrato (`…-VERIFICA-LEGALE-IP.md`, PR #47).

⚠️ **I due rami si tengono separati dal primo commit.** Il ramo Faerûn ricade
sotto il DMs Guild Community Content Agreement, incompatibile con MIT, GPL e
CC BY. Separarli dopo significa riscrivere.

---

## §3 · Il colophon: quando si compila, e con che valori

Il meccanismo è [ADR-0023](../../plans/adr/ADR-0023-colophon-di-edizione.md); qui
c'è **quando** si tocca. La chiave `colophon` del manifest, e le sue sette voci:

| Voce | Cosa ci va | La trappola |
|---|---|---|
| `edizione` | come si chiama l'uscita | — |
| `versione` | `v1`, `v2`… | si alza **quando cambia il contenuto**, non a ogni compilazione |
| `data` | in chiaro, `AAAA-MM-GG` | ⚠️ **si scrive, non si deduce**: un `today()` rende il PDF diverso a ogni compilazione e toglie senso al gate di stampa |
| `autori` | chi l'ha scritto | ⛔ **mai un nome inventato**. Se non lo sai, la riga non esce |
| `basato_su` | SRD 3.5 · OGL 1.0a · l'opera originale | è la riga che ADR-0005 chiede e che viveva solo nelle guide |
| `licenza` | il regime d'uso di **questo** volume | «materiale del DM, uso privato» è una frase stampata, non da ripetere a voce |
| `nota` | dedica, ringraziamenti, avvertenza | — |

**Chi non la dichiara esce come prima**: non è una migrazione, è una possibilità.

---

## §4 · L'edizione come oggetto: versione, ristampa, errata

Il colophon italiano di un AP Paizo ha una riga che sembra burocrazia —
*«adattamento grafico ristampa»* — e invece è la domanda più profonda: **quel
volume è alla seconda uscita, e qualcuno sa cosa è cambiato.**

- **Versione**: si alza quando cambia il contenuto. Due stampe con la stessa
  versione devono essere lo stesso testo.
- **Errata**: una correzione che arriva **dopo** che qualcuno ha stampato non si
  fa in silenzio nel master. Si scrive in un file `ERRATA-*.md` accanto al
  modulo, e **poi** si integra alzando la versione. Precedente:
  `ERRATA-ARC08-DESCRIZIONE-EPICA.md`.
- **Ristampa**: stesso contenuto, edizione nuova (carta diversa, impaginazione
  rifatta). Cambia `edizione`, non `versione`.

🟡 **Oggi questo è una convenzione, non un meccanismo**: niente lo verifica.
Diventerà un gate il giorno della prima ristampa vera (ADR-0024, «da rivisitare»).

---

## §5 · Confini con le altre skill

| Se la domanda è… | Skill |
|---|---|
| come sta sulla pagina | [`rumblingstone-editoria`](../rumblingstone-editoria/SKILL.md) |
| che faccia hanno le immagini | [`rumblingstone-art-direction`](../rumblingstone-art-direction/SKILL.md) |
| come si scrive la prosa, e le passate redazionali | [`rumblingstone-narrative-style`](../rumblingstone-narrative-style/SKILL.md) |
| quanto è profondo un modulo | [`rumblingstone-module-standard`](../rumblingstone-module-standard/SKILL.md) |
| **se può uscire, con che crediti e che versione** | **questa** |

---

## §6 · Quando NON serve

- **Materiale che resta nel repo** e non va a nessuno: il gate serve all'uscita.
- **Il PDF settimanale per il tavolo**: passa dal §1 in dieci secondi (caso
  «giocatori»), non dall'intera skill.
- **Decidere se pubblicare per soldi**: quella non è una domanda editoriale, è
  ADR-0005, e la risposta è già scritta.
