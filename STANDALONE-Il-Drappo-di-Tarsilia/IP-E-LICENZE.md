# IP e licenze — cosa è di chi, in questo modulo

Questo file esiste perché il modulo nasce da una domanda precisa: *si può fare una
versione del Palio svincolata dai Forgotten Realms?* La risposta è sì, e questo è il
rendiconto di **cosa è stato staccato e cosa no**.

> ⚠️ Analisi documentale, **non parere legale**. Per un uso commerciale reale serve
> un avvocato IP, e vale ancora la posture di
> [`plans/adr/ADR-0005`](../plans/adr/ADR-0005-confini-ip-uso-non-commerciale.md).

---

## §1 · I quattro corpi di diritti

| Corpo | Cosa tocca | Stato in questo modulo |
|---|---|---|
| **Meccaniche PF1e** | classi, incantesimi, abilità, statblocchi | **OGL**. Il modulo usa solo Core Rulebook / PRD |
| **Golarion (Paizo)** | nomi delle divinità, Regno dei Fiumi, fiume Sellen, Cassomir | **Community Use Policy**, uso non commerciale. Ridotto al minimo: §3 |
| **Wizards of the Coast** | Forgotten Realms, *Red Hand of Doom*, Channathgate | **assente**. È il punto di tutto il lavoro: §2 |
| **Palio di Siena / CTPS** | contrade, titoli, motti, livree, toponimi | bonificato quasi del tutto: §4 |

Il testo, i personaggi, la città di Tarsilia, il sottosistema della corsa e gli SVG
sono **materiale originale dell'autore**, sotto la licenza del repo (GPL-3).

---

## §2 · Il blocco WotC: perché qui non si applica

Il rapporto dell'arco di Channathgate
(`...P2D-PALIO-VERIFICA-LEGALE-IP.md` §6) individuava un blocco **assorbente**:
Channathgate è una località dei Reami, le divinità sono di Faerûn, i PNG e la trama
vengono da *Red Hand of Doom*.

**Nessuno dei tre è presente in questo modulo.** Verifica riga per riga:

| Elemento del blocco | Qui |
|---|---|
| Toponimi FR (Channathgate, Channath Vale, Rethmar) | **nessuno** — Tarsilia è inventata, il resto è Golarion |
| Divinità di Faerûn | **nessuna** — il pantheon è di Golarion (§3) |
| PNG e trama di *Red Hand of Doom* | **nessuno** — i ventidue personaggi nominati sono tutti nuovi |
| PG della campagna RumblingStone | **nessuno** — le sei schede sono pregenerate ex novo |
| Artefatti della campagna (Corona, Bracieri, Aegis Fang) | **nessuno** |

Ciò che è stato riportato è il **sistema** — Sorte, Partiti, contatori di Morale e
Onore, Stacco, Corsa a tre tratti — che il rapporto stesso classificava come
materiale originale dell'autore.

---

## §3 · Golarion e la Community Use Policy

Gli agganci a Golarion sono **quattro e soltanto quattro**: gli otto **nomi di
divinità** (Abadar, Iomedae, Gorum, Norgorber, Sarenrae, Erastil, Nethys, Calistria,
Shelyn, Gozreh, Desna), il **Regno dei Fiumi**, il fiume **Sellen** e la città di
**Cassomir** citata come luogo a valle. Tutto il resto è inventato.

Il testo di attribuzione richiesto dalla Community Use Policy va riportato su
qualsiasi copia distribuita:

> *This uses trademarks and/or copyrights owned by Paizo Inc., used under Paizo's
> Community Use Policy (paizo.com/communityuse). We are expressly prohibited from
> charging you to use or access this content. This work is not published, endorsed,
> or specifically approved by Paizo. For more information about Paizo Inc. and Paizo
> products, visit paizo.com.*

⚠️ **Verifica il testo corrente** sulla pagina della CUP prima di distribuire: le
policy cambiano, e questa formula è quella nota al momento della stesura.

> **La via d'uscita, se anche questo preoccupa.** Sostituisci gli otto patroni con
> divinità inventate e togli i tre toponimi: **il modulo non cambia di una riga** —
> le divinità non hanno effetti meccanici se non la scelta dei domini di Melchio, e i
> toponimi compaiono in tre frasi di colore. Tarsilia è progettata per essere
> world-neutral con dieci minuti di lavoro.

---

## §4 · Le bonifiche §7 del rapporto originale — stato reale

> ⚠️ **Decisione del DM, 2026-08-15**: *«per il momento usa gli scudi di Golarion e i
> nomi senesi, poi bonificheremo anche quelli»*. Il modulo ha quindi **rimesso i nomi
> delle contrade senesi** (Oca, Torre, Bruco, Istrice, Drago, Civetta, Leocorno,
> Onda). Questa sezione dice la verità su cosa ne consegue, perché una nota IP che
> dichiara il falso è il difetto peggiore che un file come questo possa avere.

La checklist del rapporto di Channathgate, punto per punto, **allo stato attuale**:

| # | Bonifica richiesta | Stato |
|---|---|---|
| 1 | Rinominare le contrade | ❌ **sospesa per decisione del DM** — i nomi sono quelli reali |
| 2 | Eliminare i titoli araldici ufficiali | ✅ **fatto** — nessun titolo («Nobile», «Sovrana», «Priora»). «Capitano» è usato come nome comune dell'ufficio |
| 3 | Cambiare le livree | ✅ già chiuso nella serie Golarion (2026-08-09): le otto livree derivano dalla divinità patrona, non dall'allegato A del Regolamento |
| 4 | Riscrivere i motti da zero | ✅ **fatto** — otto motti nuovi, nessuno dei quali parafrasa i motti reali (confronto in `CONTRADE-DI-TARSILIA.md` §1) |
| 5 | Rimuovere «Piazza il Campo» e la geometria a nove spicchi | ✅ **fatto** — la piazza è **la Ruota**: anello rettangolare intorno a un mercato coperto, nome e geometria diversi |
| 6 | Rinominare l'evento | ✅ **fatto** — è **il Drappo**. La parola *palio* non compare nel modulo |
| 7 | Correggere le note IP e documentare la provenienza delle immagini | ✅ **questo file**, più `ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md` §5. Le tavole vettoriali sono generate da `ALLEGATI/tavole/build_tavole.py`: provenienza tracciata per costruzione |
| 8 | Riambientare fuori da Forgotten Realms | ✅ **fatto** — §2 |

**Sei su otto chiuse, una sospesa, una già chiusa altrove.** Restano aperti insieme
il punto 1 (i nomi) e le **figure degli scudi** — oca, torre, bruco, istrice, drago,
civetta, leocorno, onda — che sommate ai nomi ricostruiscono l'evocazione che il
rapporto §3 individuava come il vero rischio.

**Il lessico è comunque sostituito**, e questo resta vero:

| Channathgate (3.5) | Tarsilia (PF1e) |
|---|---|
| la Tratta | **la Sorte** |
| la Mossa | **lo Stacco** |
| i canapi | **le funi** |
| il nerbo | **lo scudiscio** |
| il Barbaresco | **lo Stalliere** |
| il Gonfaloniere | **la Sovrintendente al Drappo** |
| il drappellone / il cencio | **il Drappo** |
| Piazza del Palio | **la Ruota** |

### Cosa serve per chiudere anche il punto 1

Una passata sola, e il modulo è già attrezzata per riceverla: i nomi delle contrade
compaiono in **nove file** e sono sostituibili con una tabella di rimpiazzo (l'ultima
è stata fatta nella direzione opposta il 2026-08-15). Insieme vanno cambiate almeno
**quattro figure su otto** negli scudi, altrimenti il cumulo resta. È il **Lotto 3**
in [`plans/PIANO-DRAPPO-DI-TARSILIA-STANDALONE-PF1E.md`](../plans/PIANO-DRAPPO-DI-TARSILIA-STANDALONE-PF1E.md).

## §5 · Le icone degli stemmi

Le figure degli scudi vengono da **game-icons.net**, licenza **CC BY 3.0**,
compatibile anche con l'uso commerciale **con attribuzione**. L'obbligo è assolto nel
`CREDITS.md` della cartella degli stemmi:

> *Icons made by Lorc, Delapouite and Caro Asercion* — <https://game-icons.net> —
> CC BY 3.0

---

## §6 · Riassunto per scenario d'uso

| Scenario | Verdetto |
|---|---|
| **Giocarlo al proprio tavolo** | ✅ senza riserve |
| **Darlo ai propri giocatori** | ✅ |
| **Pubblicarlo gratis** | 🟡 con la nota CUP del §3 e l'attribuzione del §5 — e sapendo che i **nomi delle contrade sono quelli reali** (§4, punto 1 sospeso): rischio basso ma non nullo, esattamente come per l'arco di Channathgate |
| **Venderlo** | ❌ non allo stato. La CUP vieta espressamente di far pagare l'accesso, e restano aperti il punto 1 e le figure degli scudi. Servirebbe: togliere gli agganci Golarion (§3, via d'uscita), rinominare le contrade, rifare quattro scudi |

La differenza rispetto al resto del repo resta netta, ed è tutto il senso di questo
lavoro: **qui il blocco assorbente WotC non c'è**. Quello che resta è governabile, e
adesso è scritto quanto manca.
