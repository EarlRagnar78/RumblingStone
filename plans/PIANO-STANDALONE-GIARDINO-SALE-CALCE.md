# PIANO — La stand alone della cisterna: «Il Giardino di Sale e Calce»

> **Stato**: 🟡 aperto (2026-11-01). A0, A1 e A2 fatti; D1-D5 decise, D6 (canone o no) alla card · **Classe**: K (contenuto nuovo), con le tavole sulla catena delle mappe
> **Nasce da**: la richiesta del DM del 2026-11-01: *«aggiungere una altra stand alone nella folder delle stand alone […] prendendo tutti i dati e idee necessarie da questa chat di gemini e dai suoi documenti generati adattandosi e verificandone secondo il processo sviluppato finora per le altre stand alone per esempio la stand alone della abbazia»*.
> **Sorgente**: la chat Gemini «One-shot D&D 3.5 e Pathfinder 1e» (creata il 2026-10-27, condivisa il 2026-11-01). Copia integrale e inventario in `/mnt/project-files/standalone-giardino-sale-calce/`, fuori dal repo: entra solo ciò che passa le verifiche.
> **Decisioni collegate**: [ADR-0017](adr/ADR-0017-moduli-autoconclusivi-classe-di-artefatto.md) (i moduli autoconclusivi), [ADR-0103](adr/ADR-0103-le-regole-si-riscontrano-sull-srd-in-cache.md) (riscontro sull'SRD in cache), [ADR-0105](adr/ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md) (il riquadro delle creature), [ADR-0106](adr/ADR-0106-ogni-mappa-si-stampa-in-pianta.md) (ogni mappa in pianta).
> **Banco di riferimento**: `10-stand-alone/L'abbazia Della Rotta Sicura/` per forma, tavole, indice maestro e manifest; `STANDALONE-Il-Drappo-di-Tarsilia/` per l'apparato d'uso e il playtest (la sua cartella non si tocca: il DM sta decidendo se spostarla).

## Cosa porta la chat

Lo spunto è il Palombaro Lungo di Matera trasformato nella cisterna di una città del deserto, Qasr al-Milah. La cisterna è lunga 60 m e larga 40, con quattro navate e tre setti di tufo. Il soffitto è a +20 m e l'acqua scende fino a −12. La rende pericolosa una nebbia di calce sopra i +6 m, che si aggiunge a catene sospese, acqua corrotta, eco e paratoie che alzano il livello. Il boss è un aboleth, Karkator, che corrompe l'acqua con il Cuore di Selenite. Il gruppo descritto sono i quattro PG del tavolo, di 13°, che volano e vedono al buio fino a 36 m; la chat costruisce un'interazione per ciascuno.

Il materiale vale come traccia, non come modulo: tre aree e tre scontri, mappe solo a caratteri e incoerenti fra le versioni, regole 3.5 e PF1e mescolate, numeri senza conti. L'elenco di cosa non regge è nell'inventario.

## Decisioni al DM

| ID | Domanda | Proposta | Stato |
|---|---|---|---|
| D1 | Sistema | doppia: statblocchi e regole in D&D 3.5, con un riquadro di conversione PF1e per ogni creatura e regola d'ambiente; warlock da *Complete Arcane* con nota di licenza | ✅ decisa dal DM il 2026-11-01 (card, opzione C, non la proposta 3.5 sola) |
| D2 | Collocazione | 3.5: sotto **Rethmar** (il «Damarath» del messaggio è il vecchio nome, D2 di PIANO-REVISIONE-ARC09), legata a Sonjak e a Sal, l'agente del Collezionista; PF1e: Qasr al-Milah, città del deserto inventata, con una nota per collocarla in una regione di Golarion | ✅ decisa dal DM il 2026-11-01 nel thread: «sotto damarath o cannathgate […] per la parte pf1 una città inventata o su golarion o su una regione valida»; la scelta Rethmar e la città PF1e inventata sono dell'agente, sulle sue indicazioni |
| D3 | Ampiezza | media: un atto breve in città e 12-16 aree nella cisterna su tre quote, una sessione di 6-7 ore | ✅ decisa dal DM il 2026-11-01 (card): la proposta |
| D4 | Titolo | *Il Giardino di Sale e Calce* | ✅ decisa dal DM il 2026-11-01 (card): la proposta |
| D5 | Il boss | aboleth SRD avanzato a conti, potenziato con la regola della versione più terrificante (3.5, poi PF1e, poi SRD), fonte segnata | ✅ decisa dal DM il 2026-11-01 (card): la proposta |
| D6 | Canone: la versione 3.5 sotto Rethmar entra in ARC-09 (prima dell'assedio, con effetti su `state.md`) o resta una stand alone con un aggancio da usare se il DM vuole? | stand alone in `10-stand-alone/` con un riquadro d'aggancio ad ARC-09; `state.md` si tocca solo quando si gioca | card |

## Fase A — Audit

- [x] **A0** Inventario della chat e dei due PDF resi come testo (2026-11-01).
- [x] **A1** Riscontro sull'SRD in cache di ogni regola, creatura e incantesimo citato (ADR-0103); tabella «idea della chat → regola 3.5 → fonte → scarto». Fatto il 2026-11-01: [A1-RISCONTRO-SRD](esperimenti/giardino-sale-calce-2026-11/A1-RISCONTRO-SRD.md).
- [x] **A2** Le capacità dei quattro PG al 13° che toccano la cisterna (volo, scurovisione, forma selvatica, ki, invocazioni) da `campaign/state.yaml` e dalle schede, per tarare i pericoli senza annullarli. Fatto il 2026-11-01: [A2-CAPACITA-DEI-PG](esperimenti/giardino-sale-calce-2026-11/A2-CAPACITA-DEI-PG.md).
- [ ] **A3** Budget: EL degli scontri e tesoro per livello del gruppo (DMG 3.5, tabella 5-1 e ricchezza per incontro).

## Fase B — Scrittura

- [ ] **B1** Cartella `10-stand-alone/<titolo D4>/` con master markdown e manifest come l'Abbazia: verità, perché adesso, nota di tono, igiene di licenza.
- [ ] **B2** L'atto in città (se D3 = media o ampia): il Visir, Nadia, i segni su Tariq, la discesa.
- [ ] **B3** Le aree della cisterna a prefisso di quota, ciascuna con box di luogo, cosa c'è e perché ci si torna (indice maestro).
- [ ] **B4** Le creature nel riquadro unico: Ragno delle Catene sul ragno fase, chuul, cloaker, skum avanzati, Mastro Tariq chierico 11 con incantesimi veri, Karkator secondo D5. Numeri solo nello statblocco (ADR-0091).
- [ ] **B5** Le interazioni di classe come leve con CD, costo e conseguenza, nella forma di regia del repo.
- [ ] **B6** Le tavole: pianta a scala reale e sezione verticale per ogni ambiente con quota (ADR-0106), dal generatore del repo.
- [ ] **B7** Apparato d'uso dal Drappo: quickstart, guida al DM passo passo, kit anti-improvvisazione, scheda di playtest.

## Fase C — Verifica

- [ ] **C1** `validate_standalone`, `validate_booklets --stampa`, `validate_prosa`, `validate_lingua` verdi.
- [ ] **C2** Box misurati con `ciclo_prosa.box_impoveriti` e lo standard del giro (ADR-0093, ADR-0095).
- [ ] **C3** Simulazione degli scontri contro i quattro PG con le loro risorse (come per il duello di ARC-07), con esiti in un file accanto al modulo.
- [ ] **C4** Lettura a freddo di lettore e playtester senza 🔴.
- [ ] **C5** Booklet stampato e misurato con `misura_stampa.py`.

## Registro

| Data | Cosa |
|---|---|
| 2026-11-01 | Piano aperto. Chat letta per intero da link pubblico (il proxy del container la blocca, letta via servizio esterno); inventario e copia in `/mnt/project-files/standalone-giardino-sale-calce/`. D1-D5 alle card. |
| 2026-11-01 | D5 e D1 decise alle card: boss a conti, sistema doppio 3.5 con note PF1e. A1 fatto: nessun numero della chat coincide con un'avanzata calcolata; cinque incantesimi di Tariq su tredici sbagliati. |
| 2026-11-01 | D2-D4 decise: Rethmar per la 3.5 (legami con Sonjak e Sal), città inventata per la PF1e, ampiezza media, titolo della chat. A2 fatto: il monaco 3.5 non corre sui muri, la nebbia non deve togliere il volo ad Artemis, l'equipaggiamento di tre PG non è nel repo. D6 aperta. |
