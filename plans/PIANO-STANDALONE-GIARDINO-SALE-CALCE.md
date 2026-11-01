# PIANO — La stand alone della cisterna: «Il Giardino di Sale e Calce»

> **Stato**: 🟡 aperto (2026-11-01). fase A chiusa; modulo 3.5 scritto con otto mappe; D1-D7 decise: due moduli, 3.5 canonico sotto Rethmar e PF1e autonomo in Qasr al-Milah · **Classe**: K (contenuto nuovo), con le tavole sulla catena delle mappe
> **Nasce da**: la richiesta del DM del 2026-11-01: *«aggiungere una altra stand alone nella folder delle stand alone […] prendendo tutti i dati e idee necessarie da questa chat di gemini e dai suoi documenti generati adattandosi e verificandone secondo il processo sviluppato finora per le altre stand alone per esempio la stand alone della abbazia»*.
> **Sorgente**: la chat Gemini «One-shot D&D 3.5 e Pathfinder 1e» (creata il 2026-10-27, condivisa il 2026-11-01). Copia integrale e inventario in `/mnt/project-files/standalone-giardino-sale-calce/`, fuori dal repo: entra solo ciò che passa le verifiche.
> **Decisioni collegate**: [ADR-0017](adr/ADR-0017-moduli-autoconclusivi-classe-di-artefatto.md) (i moduli autoconclusivi), [ADR-0103](adr/ADR-0103-le-regole-si-riscontrano-sull-srd-in-cache.md) (riscontro sull'SRD in cache), [ADR-0105](adr/ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md) (il riquadro delle creature), [ADR-0106](adr/ADR-0106-ogni-mappa-si-stampa-in-pianta.md) (ogni mappa in pianta).
> **Banco di riferimento**: `10-stand-alone/L'abbazia Della Rotta Sicura/` per forma, tavole, indice maestro e manifest; `10-stand-alone/Il-Drappo-di-Tarsilia/` per l'apparato d'uso e il playtest (spostato lì con la PR #302).

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
| D6 | Canone: la versione 3.5 sotto Rethmar entra in ARC-09 o resta una stand alone? | stand alone con aggancio | ✅ decisa dal DM il 2026-11-01 (card, opzione C, non la proposta): **due moduli distinti**. La 3.5 è canonica, sotto Rethmar, prima dell'assedio, con Sonjak e Sal; la PF1e è autonoma, in Qasr al-Milah. Tutti e due stanno in `10-stand-alone/` |
| D7 | Per quanti PG è la 3.5, visto che nel canone Hella è morta fino al rito? | tre PG più un posto libero | ✅ decisa dal DM il 2026-11-01 in chat, non la proposta: **quattro PG di 13° con Hella**. La morte canonica non conta in questo modulo |

## Fase A — Audit

- [x] **A0** Inventario della chat e dei due PDF resi come testo (2026-11-01).
- [x] **A1** Riscontro sull'SRD in cache di ogni regola, creatura e incantesimo citato (ADR-0103); tabella «idea della chat → regola 3.5 → fonte → scarto». Fatto il 2026-11-01: [A1-RISCONTRO-SRD](esperimenti/giardino-sale-calce-2026-11/A1-RISCONTRO-SRD.md).
- [x] **A2** Le capacità dei quattro PG al 13° che toccano la cisterna (volo, scurovisione, forma selvatica, ki, invocazioni) da `campaign/state.yaml` e dalle schede, per tarare i pericoli senza annullarli. Fatto il 2026-11-01: [A2-CAPACITA-DEI-PG](esperimenti/giardino-sale-calce-2026-11/A2-CAPACITA-DEI-PG.md).
- [x] **A3** Budget: EL degli scontri e tesoro per livello del gruppo (DMG 3.5, tabella 5-1 e ricchezza per incontro). Fatto il 2026-11-01: [A3-BUDGET-EL-E-TESORO](esperimenti/giardino-sale-calce-2026-11/A3-BUDGET-EL-E-TESORO.md).

## Fase B — Scrittura

- [x] **B1** Cartella `10-stand-alone/<titolo D4>/` con master markdown e manifest come l'Abbazia: verità, perché adesso, nota di tono, igiene di licenza. Fatto il 2026-11-01 per la 3.5: `10-stand-alone/Il Giardino di Sale e Calce/` con `giardino_sale_calce.md`, `appendice_creature.md` e `homebrew/giardino-sale-calce.manifest.json`.
- [ ] **B2** L'atto in città (se D3 = media o ampia): il Visir, Nadia, i segni su Tariq, la discesa. 🟡 3.5 fatta il 2026-11-01 (Rethmar: Brenna, Tredora, Lorana, Sal, Mira, la bottega di Tariq, dicerie, tre ingressi con indizi); manca la PF1e.
- [ ] **B3** Le aree della cisterna a prefisso di quota, ciascuna con box di luogo, cosa c'è e perché ci si torna (indice maestro). 🟡 3.5 fatta il 2026-11-01: 14 aree (A, B, C, G, T, S) con le reazioni per ingresso; manca la PF1e.
- [ ] **B4** 🟡 3.5 fatta il 2026-11-01 (anche il chuul avanzato a 17 DV e il Cuore a prezzo calcolato, in `appendice_creature.md`; il cloaker non entra); manca la PF1e. Le creature nel riquadro unico: Ragno delle Catene sul ragno fase, chuul, cloaker, skum avanzati, Mastro Tariq chierico 11 con incantesimi veri, Karkator secondo D5. Numeri solo nello statblocco (ADR-0091). 🟡 Prima parte il 2026-11-01: [B4-CONTI-CREATURE-35](esperimenti/giardino-sale-calce-2026-11/B4-CONTI-CREATURE-35.md), Karkator (aboleth mezzo-immondo a 24 DV, GS 15, 16 col Cuore) e Ragno delle Catene (ragno fase a 14 DV, GS 10). Seconda parte lo stesso giorno: Mastro Tariq chierico 13 di Umberlee (domini Acqua e Distruzione, *nube acida* come nebbia di calce, GS 13) e skum guerriero 8 (GS 10); Tariq e skum EL 15.
- [x] **B5** Le interazioni di classe come leve con CD, costo e conseguenza, nella forma di regia del repo.
- [x] **B6** Le tavole: pianta a scala reale e sezione verticale per ogni ambiente con quota (ADR-0106), dal generatore del repo. Richiesta del DM del 2026-11-01: mappe tattiche dettagliate per ogni incontro e mappe d'ambientazione (Rethmar e la discesa). 🟡 2026-11-01: otto mappe tattiche in `10-stand-alone/Il Giardino di Sale e Calce/Mappe/` (contratti JSON, master compilati, SVG pergamena, texture, pianta e pianta da stampa), collaudo e qualità a 0 errori (voto medio 94). Poi, su richiesta del DM: GS-0 (come si collegano le aree, coi tre ingressi da Rethmar), GS-S1 (la cisterna in sezione, dalla piazza al Santuario) e GS-S2 (l'incontro coi Ragni delle Catene in sezione, tre momenti), da `render_schemi.py`; nello stesso giro le piante allineate fra loro (Torre di GS-3 grande come l'officina di GS-4, chiocciola del Santuario sul lato della Torre, volta della grotta a −1 e cadute ricalcolate). Chiuso il 2026-11-01 con GS-R, i tre ingressi sulla pianta canonica di Rethmar (foro, Cattedrale, Ponte, le due gallerie); allineate anche le quote al canone della città: il Cannath è a +13, otto metri sotto il foro, e il Santuario è una sorgente in pressione che risale la galleria di drenaggio fino al fiume.
- [x] **B8** Rethmar e l'assedio (richiesta del DM del 2026-11-01): scene, villain, PNG e artefatti collegati a Rethmar, con scelte ampie per i PG e conseguenze sui difensori dell'assedio o vantaggi agli attaccanti, agganciate ai clock di ARC-09 in `campaign/state.yaml`. 🟡 Progetto il 2026-11-01: [B8-RETHMAR-E-ASSEDIO](esperimenti/giardino-sale-calce-2026-11/B8-RETHMAR-E-ASSEDIO.md), con 15 scelte e i loro effetti su Fronte, Morale Cittadino, contingenti e clock, tre ingressi (cripta della Cattedrale di Lathander, sfioratore nascosto, pozzo del mercato) e undici mappe.
- [x] **B7** Apparato d'uso dal Drappo: quickstart, guida al DM passo passo, kit anti-improvvisazione, scheda di playtest.

## Fase C — Verifica

- [ ] **C1** `validate_standalone`, `validate_booklets --stampa`, `validate_prosa`, `validate_lingua` verdi.
- [x] **C2** Box misurati con `ciclo_prosa.box_impoveriti` e lo standard del giro (ADR-0093, ADR-0095). *(2026-11-01: il modulo è nuovo, quindi non c'è un prima da impoverire: misurati i 15 box con `misura_craft` contro Abbazia e DEF-4. Nessun P1, nessuna metratura, nessuna parentesi, nessun box oltre 12 righe; 5 su 14 oltre 4 frasi (Abbazia 1 su 11, DEF-4 17 su 37); sensoriali 48‰ (Abbazia 31‰, DEF-4 55‰); `ciclo_prosa segnala` aveva un «sembra» e un calco, corretti; D3 del developer chiusa con il TS su Riflessi di chi cade dalle passerelle)*
- [x] **C3** Simulazione degli scontri contro i quattro PG con le loro risorse (come per il duello di ARC-07), con esiti in un file accanto al modulo. *(2026-11-01: `SIMULAZIONE-SCONTRI.md`; ragni e Tariq giusti, Karkator al LI 24 è un TPK; applicata la consigliata della card D-a, LI 16 e il Cuore come chiave, in attesa della scelta del DM)*
- [ ] **C4** Lettura a freddo di lettore e playtester senza 🔴.
- [ ] **C5** Booklet stampato e misurato con `misura_stampa.py`.

## Registro

| Data | Cosa |
|---|---|
| 2026-11-01 | Piano aperto. Chat letta per intero da link pubblico (il proxy del container la blocca, letta via servizio esterno); inventario e copia in `/mnt/project-files/standalone-giardino-sale-calce/`. D1-D5 alle card. |
| 2026-11-01 | D5 e D1 decise alle card: boss a conti, sistema doppio 3.5 con note PF1e. A1 fatto: nessun numero della chat coincide con un'avanzata calcolata; cinque incantesimi di Tariq su tredici sbagliati. |
| 2026-11-01 | D2-D4 decise: Rethmar per la 3.5 (legami con Sonjak e Sal), città inventata per la PF1e, ampiezza media, titolo della chat. A2 fatto: il monaco 3.5 non corre sui muri, la nebbia non deve togliere il volo ad Artemis, l'equipaggiamento di tre PG non è nel repo. D6 aperta. |
| 2026-11-01 | D6 decisa: due moduli. A3 fatto: il tesoro della chat (circa 161.000 mo) supera da una volta e due terzi a due volte e mezza il budget SRD della sessione (63.000-97.000); l'aboleth avanzato a 24 DV fa GS 12 prima del Cuore. Fase A chiusa. |
| 2026-11-01 | B4 prima parte: Karkator è un aboleth mezzo-immondo Mastodontico a 24 DV (324 pf, CA 28 con aura e Cuore, GS 15; 16 col Cuore); il Ragno delle Catene è un ragno fase Enorme a 14 DV (GS 10). Tariq, skum e chuul nella seconda parte. |
| 2026-11-01 | B4 seconda parte (Tariq, skum). Il DM chiede mappe tattiche e d'ambientazione dettagliate e il legame con l'assedio di Rethmar: lotto B8 aggiunto. |
| 2026-11-01 | B8 progettato: verità 3.5 (Sonjak vuole il tunnel, il Collezionista il Cuore, Sal ha comprato Tariq), 15 scelte con effetti sull'assedio, tre ingressi chiesti dal DM, undici mappe. |
| 2026-11-01 | D7 decisa da Jfs: la 3.5 è per quattro PG di 13° con Hella, anche se nel canone è morta fino al rito. Mostri, PNG ed EL restano tarati su quattro. |
| 2026-11-01 | B6 prima parte: otto mappe tattiche (cripta della Cattedrale, sfioratore, piazza del pozzo, quota alta, quota media e fondo, Torre delle Volte, Santuario di Sale, galleria di drenaggio), con le scale collegate fra loro. |
| 2026-11-01 | Modulo 3.5 scritto: verità, tre ingressi con indizi, atto in città, 14 aree, cast con leve, scelta sul Cuore, conseguenze sull'assedio, tesoro (circa 94.500 mo), modi di fallimento, ADR; appendice delle creature con i conti; manifest. validate_booklets, validate_prosa --strict e conformita_statblocchi verdi. B8 chiuso. |
