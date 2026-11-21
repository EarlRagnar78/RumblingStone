# 🗄️ MEMORIA STORICA — quello che la memoria corta non tiene più

> **Cos'è** ([ADR-0127](adr/ADR-0127-la-memoria-corta-archivia-nel-repo-prima-di-togliere.md)).
> La memoria del progetto, quella che ogni sessione d'agente legge all'avvio,
> ha un limite di dimensione: tiene solo regole, stato aperto, ambiente e
> puntatori. Quando una sua riga esce (PR unita, canone ormai nel repo,
> questione chiusa), i fatti che non stanno altrove finiscono **qui**, una
> voce per riga. Questo file non ha limite, non si riassume e non si
> riscrive: si aggiunge in coda. Serve a chi lavora su una regressione o
> rivede una soluzione già adottata e ha bisogno di sapere *che cosa si
> sapeva allora*.
>
> **Non è il canone e non è il changelog.** Il canone sta nei file della
> campagna e nei piani; i lotti chiusi stanno in [`CHANGELOG.md`](CHANGELOG.md),
> che porta qui; le decisioni in [`adr/`](adr/); la memoria del lavoro
> generata in [`MEMORIA.md`](../MEMORIA.md). Una voce dice cosa la memoria
> riportava a quella data e dove il fatto si ritrova nel repo; dove non si
> ritrova, lo dice nel campo **Solo qui**.

## Come si legge

```bash
python3 scripts/memoria_storica.py --pr 242        # la storia di una PR
python3 scripts/memoria_storica.py --adr 93        # di un ADR
python3 scripts/memoria_storica.py --tema prosa    # di un tema (campo Temi)
python3 scripts/memoria_storica.py Skullcrusher Virata   # parole, tutte
python3 scripts/memoria_storica.py --da 2026-10-19 --a 2026-10-20 --elenco
python3 scripts/memoria_storica.py --json --pr 380 # per un agente
```

Lo stesso strumento è esposto dal server MCP del repo (`memoria_storica`,
sola lettura). I filtri si sommano; maiuscole e accenti non contano.

## Come si scrive una voce

Tre regole (ADR-0127, ADR-0137, ADR-0138):

- **Addendum del changelog, obbligatorio in CI**: una PR che aggiunge righe a
  [`CHANGELOG.md`](CHANGELOG.md) aggiunge anche almeno una voce qui, con le
  decisioni, le misure, le questioni aperte e i rimandi che la riga non
  tiene. `check_plans_discipline.py` boccia la PR se manca.
- **Prima di togliere una riga dalla memoria del progetto** (fuori dal repo,
  la CI non la vede) si controlla che i suoi fatti siano qui; se mancano, si
  copia la riga com'era in una voce nuova, nello stesso giro di lavoro.

- **A fine di ogni blocco di lavoro che non finisce in una PR** (scelta su
  card, dato verificato, file solo nella cartella condivisa, thread che si
  risolve) il thread scrive la voce, con la testa `### MS-???? · data · titolo`,
  nel suo file della coda `/mnt/project-files/memoria-storica-coda/`.
  `python3 scripts/memoria_coda.py DIR --thread "Titolo"` esce 1 se manca;
  `--piega` la porta qui col numero e col campo `Coda`. Una voce piegata non
  ha una riga del changelog: la sua origine è la card o il thread.

Si aggiunge in coda col numero dopo l'ultimo e si fa girare
`python3 scripts/memoria_storica.py --check` (la CI fa lo stesso).

```markdown
### MS-NNNN · AAAA-MM-GG · Titolo breve, cercabile

- **Data:** AAAA-MM-GG            (la data del fatto principale; uguale al titolo)
- **PR:** #380 #379               (oppure —)
- **ADR:** ADR-0126               (oppure —)
- **Temi:** regole motore         (parole singole, minuscole, separate da spazi)
- **Origine:** memoria del progetto, riga tolta il AAAA-MM-GG
- **Testo:** la riga della memoria, intera
- **Trovato nel repo:** `#380` → `plans/CHANGELOG.md` · …   (facoltativo)
- **Fuori dal repo:** percorsi della cartella condivisa         (facoltativo)
- **Note di memoria:** `nome-nota`                              (facoltativo)
- **Solo qui:** i fatti che non si ritrovano altrove             (facoltativo)
- **Coda:** `nome-del-file-di-coda`      (lo scrive `memoria_coda.py --piega`)
```

Niente dati personali (nomi dei giocatori, macchine del DM, nomi utente):
quelli restano nelle note di memoria (scelta del DM del 2026-11-12).

## Da dove vengono le voci MS-0001…MS-0067

Il 2026-11-12 la memoria del progetto è stata ridotta da circa 25 KB a 8 KB
togliendo la cronologia delle PR unite. Le sue 67 righe sono state
confrontate con il repo e con le note di memoria e archiviate qui, una per
voce, col testo intero; «Jfs» è scritto «il DM» come nel resto del repo, e
tre righe hanno dati personali tolti: il DM ha scelto il 2026-11-12 di lasciarli fuori dal repo (MS-0005,
MS-0006, MS-0009).

Misura del recupero: dei **165 riferimenti** distinti delle 67 righe (PR,
SHA, ADR, percorsi della cartella condivisa) **127** si trovavano già nel
repo, **24** solo nelle note di memoria (fuori dal repo), **14** da nessuna
parte; dei 150 fatti di contenuto controllati con una ricerca testuale, **24**
non si trovavano nel repo. Ora sono tutti qui. La ricerca è testuale: un
riferimento «trovato nel repo» vuol dire che la stringa c'è in quel file, non
che il file racconti tutto il fatto; un fatto «solo qui» può esistere nel
repo scritto con altre parole.

## Voci

### MS-0001 · 2026-10-11 · Python 3.13 ovunque e i PR di Dependabot

- **Data:** 2026-10-11
- **PR:** #228 #231 #236
- **ADR:** —
- **Temi:** piattaforma dipendenze
- **Origine:** memoria del progetto, riga 1 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Python: 3.13 ovunque (D7 di AMBIENTE-RIPRODUCIBILE, vale anche per Dependabot). #231 (CI a 3.13) e #236 (i 6 aggiornamenti di Dependabot della #228, portati a mano perché Dependabot non riusciva a rigenerarla) fuse su main il 2026-10-11. La #228 è stata chiusa come superata il 2026-10-23. I commenti `@dependabot` postati da Claude arrivano con l'@ neutralizzata, quindi un recreate lo deve scrivere il DM.
- **Trovato nel repo:** `#228` → `plans/CHANGELOG.md` · `#231` → `plans/CHANGELOG.md` · `#236` → `plans/CHANGELOG.md`

### MS-0002 · 2026-10-24 · Chiusura della PR #99 e schede dei PG

- **Data:** 2026-10-24
- **PR:** #99 #289 #291
- **ADR:** ADR-0007
- **Temi:** pr schede-pg
- **Origine:** memoria del progetto, riga 2 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #99 chiusa il 2026-10-24 (scelta A del DM): echi §1-bis, nota Golarion e inventory_inferred.py riportati con la #289 (d8b2985); 4g rifatto come 4g-1/4g-2, 4h scartato (ADR-0007). 4g-2 prima parte #291 unita il 2026-10-26 (b92f1f1).
- **Trovato nel repo:** `#99` → `plans/CHANGELOG.md` · `#289` → `plans/STATO-E-ORDINE-DEI-PIANI.md` · `#291` → `plans/STATO-E-ORDINE-DEI-PIANI.md` · `ADR-0007` → `plans/adr/ADR-0007-scritture-canone-triplo-vincolo.md` · `b92f1f1` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv` · `d8b2985` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `pr99-e-schede-pg`

### MS-0003 · 2026-10-10 · Piano recupero incompiuti: #232 e #233

- **Data:** 2026-10-10
- **PR:** #72 #99 #216 #232 #233
- **ADR:** —
- **Temi:** piani adr memoria
- **Origine:** memoria del progetto, riga 3 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Piano recupero incompiuti: #232 e #233 fuse il 2026-10-10. #233 ha portato la #216 (chiusa come portata, ADR memoria = 0087), le voci #72 nel registro rami, e D7: numeri ADR prenotati in plans/adr-prenotati.json (0088 alla #99), modello ADR con alternative e «Da rivedere se», .github/pull_request_template.md. Aperte al DM: D3-D6 di RECUPERO.
- **Trovato nel repo:** `#72` → `plans/CHANGELOG.md` · `#99` → `plans/CHANGELOG.md` · `#216` → `plans/CHANGELOG.md` · `#232` → `plans/CHANGELOG.md` · `#233` → `plans/STATO-E-ORDINE-DEI-PIANI.md`

### MS-0004 · 2026-10-12 · Routine settimanale del lunedì

- **Data:** 2026-10-12
- **PR:** —
- **ADR:** —
- **Temi:** routine audit
- **Origine:** memoria del progetto, riga 4 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Routine settimanale lunedì 06:47 UTC: PR, piani aperti (plans/INDEX.md, REGISTRO-LOTTI.md), changelog. Dal 2026-10-12 pubblica anche la coda dei piani per urgenza e avvia un thread «Chiusura piano …» alla volta.
- **Solo qui:** Routine settimanale lunedì 06:47 UTC

### MS-0005 · 2026-10-11 · Push dal computer del DM

- **Data:** 2026-10-11
- **PR:** —
- **ADR:** —
- **Temi:** ambiente git
- **Origine:** memoria del progetto, riga 5 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Push locale dal computer del DM: usare `gh auth setup-git`; il gestore delle credenziali del desktop proponeva un vecchio utente. *[Sistema operativo, desktop e nome del gestore esclusi: dati personali, fuori dal repo per scelta del DM del 2026-11-12.]*

### MS-0006 · 2026-10-11 · LLM locale per la prosa bocciato (ADR-0089)

- **Data:** 2026-10-11
- **PR:** #234
- **ADR:** ADR-0089
- **Temi:** prosa llm
- **Origine:** memoria del progetto, riga 6 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** LLM locale per la prosa (ADR-0089, PR #234): gemma4 e4b bocciato il 2026-10-11 (voto 40/42%, cieco 0/10 vs B-con). Prossima prova possibile: gemma4:12b-it-qat sul portatile del DM, poi 26B su un'altra macchina del DM *[modelli delle macchine esclusi: dati personali, fuori dal repo per scelta del DM del 2026-11-12]*. Avvio: start.sh poi prova.sh; dopo un riavvio il box impiega minuti.
- **Trovato nel repo:** `#234` → `plans/CHANGELOG.md` · `ADR-0089` → `plans/adr/ADR-0089-un-llm-locale-per-la-prosa-si-misura-prima.md`

### MS-0007 · 2026-10-12 · Ramo della partita del primo tavolo

- **Data:** 2026-10-12
- **PR:** #235 #237 #240
- **ADR:** ADR-0090
- **Temi:** campagna ramo-di-gruppo
- **Origine:** memoria del progetto, riga 7 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Partita del primo tavolo: ramo `campaign-group-rumblingstone` (ADR-0090, PR #237 unita il 2026-10-12), il vecchio `-dm-gianfranco` non riceve più main. Patch della serata 2026-09-25 in /mnt/project-files/sessione-2026-09-25/. PR #235 pozioni unita il 2026-10-11. PR #240 (rune di Balvar nel Bestiario allineate al master) unita su main il 2026-10-14.
- **Trovato nel repo:** `#235` → `plans/CHANGELOG.md` · `#240` → `plans/CHANGELOG.md` · `ADR-0090` → `plans/adr/ADR-0090-la-partita-riparte-su-un-ramo-di-gruppo-nuovo.md`
- **Fuori dal repo:** `/mnt/project-files/sessione-2026-09-25/` (cartella condivisa del progetto)
- **Note di memoria:** `ramo-di-gruppo-campagna`
- **Solo qui:** `#237`

### MS-0008 · 2026-10-12 · Tattiche DEF-4 canone e Seme di Varis

- **Data:** 2026-10-12
- **PR:** #238
- **ADR:** —
- **Temi:** canone arc07 booklet
- **Origine:** memoria del progetto, riga 8 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #238 unita il 2026-10-12: tattiche DEF-4 [INFERRED] diventate canone; Seme di Varis (da DEF-1 §6-bis) è capitolo II del booklet DM (77 pp). Canone: Seme nello zaino di Tordek, lo identifica Artemis con la pergamena del re (UOM CD 21, 1 tacca) perché Brynja e Kettra non sanno usarla; le pozioni le identificano Brynja e Kettra. Aperta: quale versione delle pozioni del re in Scena 4 per gruppi futuri.
- **Trovato nel repo:** `#238` → `plans/CHANGELOG.md`

### MS-0009 · 2026-11-05 · Tavolo e registro PX

- **Data:** 2026-11-05
- **PR:** #312
- **ADR:** —
- **Temi:** campagna tavolo px
- **Origine:** memoria del progetto, riga 9 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Tavolo: chi gioca quale PG è nella nota di memoria `registro-px-gruppo` *[nomi dei giocatori esclusi: dati personali, fuori dal repo per scelta del DM del 2026-11-12]*. PX e livelli: vedi Registro PX (PR #312).
- **Trovato nel repo:** `#312` → `plans/esperimenti/p16-inferred-2026-11-04/ARC09-DECISIONI.md`

### MS-0010 · 2026-10-18 · Schede PNG e villain (ADR-0091)

- **Data:** 2026-10-18
- **PR:** #241
- **ADR:** ADR-0091
- **Temi:** schede-png canone
- **Origine:** memoria del progetto, riga 10 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Schede PNG/villain: ADR-0091 (PR #241 unita su main il 2026-10-18): statblocco Difesa/Attacco/Statistiche/Capacità speciali/Tattiche, dossier a sezioni fisse, numeri solo nello statblocco. Tutte convertite; i 5 dossier di gruppo restano come sono. Tempestas = Bardo 12 / Stormsinger 2, 70 anni; Ozyrrandion drago verde adulto GS 14, ora nel sanctum di Zalkatar (scontro unico EL 16, volta ≥15 m). Cantitrici chieriche 8/barde 4 GS 12, Dana Chierica 12/Cantante Divina 3. Con #241 tutti gli INFERRED di contenuto sono chiusi (numeri da script ora [GENERATO]). Canone da applicare dal DM sul ramo di gruppo: Belkram morendo redento dice «sono in pace» e riconosce Thorik degno degli avi e portatore della Corona.
- **Trovato nel repo:** `#241` → `plans/CHANGELOG.md` · `ADR-0091` → `plans/adr/ADR-0091-la-scheda-del-png-ha-una-forma.md`

### MS-0011 · 2026-10-18 · Versione più potente e terrificante

- **Data:** 2026-10-18
- **PR:** —
- **ADR:** —
- **Temi:** regole preferenze
- **Origine:** memoria del progetto, riga 11 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Preferenzal DM (2026-10-18): versione più potente e terrificante, nell'ordine D&D 3.5, PF1e, SRD, con fonte e divergenza dall'SRD. Dal 9/11: solo se il numero si ricostruisce da una scheda legale.
- **Note di memoria:** `feedback-numeri-piu-forti-calcolati`

### MS-0012 · 2026-10-15 · Lettore e playtester completo, Bane di Thorik

- **Data:** 2026-10-15
- **PR:** #239
- **ADR:** —
- **Temi:** arc07 canone piani
- **Origine:** memoria del progetto, riga 12 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #239 unita il 2026-10-15: PIANO-LETTORE-E-PLAYTESTER completo (ARC-07 DEF-1…DEF-5 al ciclo del master; DEF-5 senza INFERRED, D90-D92). Canone: Thorik ha il Bane contro Fauci di Aegis Fang dall'affresco A7 (serata 2026-09-25); patch di state.md §6 per il ramo di gruppo in /mnt/project-files/sessione-2026-10-15/, la applical DM. Prossimo: A3 di PIANO-MASTER-DEF (canone ARC-08 contro il tavolo), poi S1.
- **Trovato nel repo:** `#239` → `plans/CHANGELOG.md`
- **Fuori dal repo:** `/mnt/project-files/sessione-2026-10-15/` (cartella condivisa del progetto)
- **Solo qui:** patch state.md §6 in /mnt/project-files/sessione-2026-10-15/

### MS-0013 · 2026-10-18 · Domande developer dell'alto livello (ADR-0092)

- **Data:** 2026-10-18
- **PR:** #244
- **ADR:** ADR-0092
- **Temi:** misura qualita
- **Origine:** memoria del progetto, riga 13 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #244 unita il 2026-10-18: domande developer dell'alto livello (ADR-0092), D1-D3 decise, default in CI (da ARC-08 in poi; i master ARC-07 restano invariati per D2). Misura: 13 → 24 rilievi sui 9 moduli, 6½ degli 11 nuovi sono difetti veri.
- **Trovato nel repo:** `#244` → `plans/PIANO-AVVENTURE-COMMUNITY-2026-10.md` · `ADR-0092` → `plans/adr/ADR-0092-le-domande-dell-alto-livello.md`
- **Note di memoria:** `ricerca-avventure-community`

### MS-0014 · 2026-10-18 · Quattro creature dalla WE RHoD

- **Data:** 2026-10-18
- **PR:** #247 #248
- **ADR:** —
- **Temi:** bestiario canone arc09
- **Origine:** memoria del progetto, riga 14 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #247 e #248 unite il 2026-10-18: 4 creature ispirate alla WE RHoD (abishai azzurro GS 11, Spezzamente GS 12, Lucertola del tuono GS 10, Furia della Mano GS 10) canone in Bestiario/mostri/ senza INFERRED, usate in ARC-09 (tabella viaggio Day 31-42 e battaglia finale). D2 archivi chiusa per queste creature.
- **Trovato nel repo:** `#247` → `plans/CHANGELOG.md` · `#248` → `plans/STATO-E-ORDINE-DEI-PIANI.md`

### MS-0015 · 2026-10-18 · Giro developer/playtester/DM su ARC-07

- **Data:** 2026-10-18
- **PR:** #245
- **ADR:** —
- **Temi:** arc07 giro srd
- **Origine:** memoria del progetto, riga 15 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #245 unita il 2026-10-18: giro developer/playtester/DM su ARC-07 DEF-1…5 (plans/esperimenti/giro-arc07-2026-10-18/), 29 decisioni DM applicate (scelta «Tutte»), righe di scala + «Se lo divinano», 9 discrepanze SRD corrette (VERIFICA-SRD.md). Fauci GS 12 (file -cr12), voce Treant di Adamantio. Aperti: patch state.md Cintura in /mnt/project-files/giro-arc07-2026-10-18/PATCH-STATE-MD.md (la applical DM); pf di Terros 345 vs 348 con Robustezza.
- **Trovato nel repo:** `#245` → `plans/CHANGELOG.md`
- **Fuori dal repo:** `/mnt/project-files/giro-arc07-2026-10-18/PATCH-STATE-MD.md` (cartella condivisa del progetto)
- **Note di memoria:** `srd-in-rete`

### MS-0016 · 2026-10-23 · Corpus della prosa italiana

- **Data:** 2026-10-23
- **PR:** #279
- **ADR:** —
- **Temi:** prosa corpus
- **Origine:** memoria del progetto, riga 16 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Corpus prosa: PDF, box e script in /mnt/project-files/corpus-prosa/ (mai nel repo); config per PDF = carattere del read-aloud. 2026-10-23 (PR #279, nota §7): +Dragons' Lair (download senza login, 21 avventure) e Chimera «Dove le profezie sbagliano» → 2.335 box IT, 34 titoli. Fasce --stile confermate (16 titoli: -mente med 6,1‰, gerundio 1,7‰). Need Games/Isola Illyon/Liber Liber fuori rete; archive.org raggiungibile ma non usato (copie non verificabili).
- **Fuori dal repo:** `/mnt/project-files/corpus-prosa/` (cartella condivisa del progetto)
- **Solo qui:** `#279` · 2026-10-23 PR #279 +Dragons' Lair 21 avventure e Chimera → 2.335 box IT, 34 titoli

### MS-0017 · 2026-10-19 · Rifacimento ARC-07 e cieco 8 a 8

- **Data:** 2026-10-19
- **PR:** #246 #249 #251
- **ADR:** —
- **Temi:** prosa cieco arc07
- **Origine:** memoria del progetto, riga 17 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #249 unita su main il 2026-10-18 (rifacimento 5 DEF ARC-07 + giro2). Cieco del DM: 8 a 8 su 16, miglioramento non dimostrato. PR #251 unita il 2026-10-19 (prima della #246, fuori ordine): le 8 vecchie vincitrici rimesse intatte, lezione applicata agli altri box (dettagli sensoriali, nomi noti, monologhi interi; box impoveriti da 26 a 2 falsi positivi con ciclo_prosa.box_impoveriti della #246). Nomi noti rimessi = lettura della norma §2-ter, non voto (cieco diviso: coppie 5 vs 6, 10). Le 55 decisioni G2 applicate come «Tutte». Una PR in conflitto con main non fa partire la CI: guardare mergeable_state.
- **Trovato nel repo:** `#246` → `plans/CHANGELOG.md` · `#249` → `plans/CHANGELOG.md` · `#251` → `plans/PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md`

### MS-0018 · 2026-10-19 · Riscrittura ARC-07 misurata contro le versioni di prima

- **Data:** 2026-10-19
- **PR:** #246 #249 #251
- **ADR:** —
- **Temi:** prosa arc07 regole
- **Origine:** memoria del progetto, riga 18 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** 2026-10-19 Il DM: rendere standard (#246 su main) e poi ricominciare la riscrittura di ARC-07 con tutte le norme nuove, misurando contro le versioni precedenti (tag prima-rifacimento-arc07, #249=2ee82472, #251=e0ce0e6). Ogni box nuovo entra solo se verdetto_misurato/box_impoveriti non lo peggiora; cieco nuovo su campione nuovo.
- **Trovato nel repo:** `#246` → `plans/CHANGELOG.md` · `#249` → `plans/CHANGELOG.md` · `#251` → `plans/PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md` · `2ee82472` → `plans/esperimenti/a3-arc08/AUDIT-GIRI-STANDARD-2026-10-18.md` · `e0ce0e6` → `plans/esperimenti/giro3-arc07-2026-10-19/cancello.py`

### MS-0019 · 2026-10-19 · La prosa migliora solo se il DM la sceglie alla cieca (ADR-0093)

- **Data:** 2026-10-19
- **PR:** #246 #251
- **ADR:** ADR-0093
- **Temi:** prosa cieco adr
- **Origine:** memoria del progetto, riga 19 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #246 unita il 2026-10-19 (ADR-0093, ancora «proposta»): la prosa migliora solo se il DM la sceglie alla cieca (14/20 riproporzionato). Decide prima la misura (§2-ter read-aloud-adulti: meno dettagli sensoriali o monologo spezzato = perde), al cieco solo le indecise + 4 controlli. ciclo_prosa.box_impoveriti è standard. Primo cieco ARC-07 8 a 8; dopo #251 resta 1 box su 26 (DEF-4 Scena 4, Thorgrim).
- **Trovato nel repo:** `#246` → `plans/CHANGELOG.md` · `#251` → `plans/PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md` · `ADR-0093` → `plans/adr/ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md`

### MS-0020 · 2026-10-19 · Giro 3 ARC-07 e box congelati

- **Data:** 2026-10-19
- **PR:** #252
- **ADR:** —
- **Temi:** prosa cieco arc07
- **Origine:** memoria del progetto, riga 20 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #252 (giro 3 ARC-07) unita il 2026-10-19 (8a6b1e1). Cieco del DM: nuova 5, vecchia 4 (soglia 7/9): non dimostrato; le 4 vecchie vincitrici rimesse e i 9 box votati in giro3/misure/CONGELATI.json (25 congelati totali). -mente ancora 0,6‰ vs 3,8-13,4‰ umano.
- **Trovato nel repo:** `#252` → `plans/esperimenti/giro4-arc07-2026-10-19/cancello.py` · `8a6b1e1` → `plans/CHANGELOG.md`

### MS-0021 · 2026-10-19 · Giro 4: DEF-4/DEF-5 per la serata

- **Data:** 2026-10-19
- **PR:** #254
- **ADR:** —
- **Temi:** arc07 serata giro
- **Origine:** memoria del progetto, riga 21 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #254 (giro 4, 2026-10-19): DEF-4/DEF-5 per la serata sullo stato del ramo di gruppo; 6 letture a freddo, correzioni, regia con risorse del gruppo e tacche in volo; numeri senza fonte INFERRED con domande in plans/esperimenti/giro4-arc07-2026-10-19/DECISIONI-DM.md (+ DEF-5/). PDF serata in /mnt/project-files/sessione-notte-e-alba/. Skullcrusher resta file -cr12 col GS 14 nella Source; ERRATA §2.3 e ARC08-11-PONTE-ARRIVO da aggiornare.
- **Trovato nel repo:** `#254` → `plans/CHANGELOG.md`
- **Fuori dal repo:** `/mnt/project-files/sessione-notte-e-alba/` (cartella condivisa del progetto)

### MS-0022 · 2026-10-19 · Giro finale DEF-4/DEF-5 e simulazione del duello

- **Data:** 2026-10-19
- **PR:** #256
- **ADR:** —
- **Temi:** arc07 skullcrusher serata
- **Origine:** memoria del progetto, riga 22 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #256 unita il 2026-10-19 (22162fc): giro finale su DEF-4/DEF-5 e booklet della serata (42/48 rilievi corretti, domande 28-33 in giro4/DECISIONI-DM.md). Il DM: Skullcrusher Adulto GS 14 + 2 wyvern (non il Vecchio). Simulazione duello in giro4/finale/SIMULAZIONE-DUELLO.md (~8 round, prima versione senza Risonanza/Ali e Passo d'Ombra; rifatta con tutti gli artefatti). validate_booklets --stampa boccia rimandi «(Dnn)» nel testo stampato.
- **Solo qui:** `#256` · `22162fc` · PR #256 unita 2026-10-19 (22162fc) 42/48 rilievi

### MS-0023 · 2026-10-19 · Duello con Skullcrusher il Vecchio e Zog'tar

- **Data:** 2026-10-19
- **PR:** #242 #257
- **ADR:** —
- **Temi:** arc07 skullcrusher canone
- **Origine:** memoria del progetto, riga 23 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #257 unita il 2026-10-19 (45d1fcf): scelte del DM dopo simulazioni con tutti gli artefatti. Duello ARC-07 = Skullcrusher Vecchio + 2 wyvern EL 17 (D60 esteso al 13°), Virata al posto di Ghermire («la passata e il nome»: colpisce solo chi ha un nome, D71); la presa in bocca con caduta è di Fauci contro Thorik in ARC-08 (thread PR #242). Zog'tar: guardie che aiutano la CA, sacerdote nella tenda, >20 cariche di bacchetta = una tacca. Aperti: nome falso/silenzio, Virata da riscontrare su d20srd.
- **Trovato nel repo:** `#242` → `plans/CHANGELOG.md`
- **Solo qui:** `#257` · `45d1fcf` · PR #257 unita 2026-10-19 (45d1fcf) Skullcrusher Vecchio + 2 wyvern EL 17

### MS-0024 · 2026-10-19 · Skullcrusher sente i nomi attraverso la Catena

- **Data:** 2026-10-19
- **PR:** #258
- **ADR:** —
- **Temi:** arc07 skullcrusher canone
- **Origine:** memoria del progetto, riga 24 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #258 unita il 2026-10-19 (7f508b9): Skullcrusher non chiede i nomi, li sente attraverso la Catena (runa gemella del corno di Grask fuori dalla tenda); chi non ha sentito lo chiama per epiteto; regia allineata al Vecchio EL 17. Aperto [INFERRED]: portata del sussurro. PDF finali in /mnt/project-files/sessione-notte-e-alba/.
- **Trovato nel repo:** `#258` → `plans/STATO-E-ORDINE-DEI-PIANI.md`
- **Fuori dal repo:** `/mnt/project-files/sessione-notte-e-alba/` (cartella condivisa del progetto)
- **Solo qui:** `7f508b9`

### MS-0025 · 2026-10-20 · Fauci in ARC-08: presa in bocca

- **Data:** 2026-10-20
- **PR:** #242
- **ADR:** ADR-0095
- **Temi:** arc08 fauci canone
- **Origine:** memoria del progetto, riga 25 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #242 unita il 2026-10-20 (thread «Chiusura piano LETTORE-PLAYTESTER · F4»; standard del giro = ADR-0095, perché 0094 era già usato). Fauci in ARC-08: presa in bocca (presa migliorata, CA normale, niente AdO), solleva Thorik senza sforzo, Scalare CD 25 sul collo; cicatrice ancestrale da Aegis Fang, Fauci riconosce l'ascia e chiama Thorik «Portatore» (i nomi sono di Skullcrusher). Regola della casa PF1e Called Shots solo per questo scontro: occhio −10, ala −2. Aperti: D4-D6 (flashback pregen, risposte A3, censimento versioni), cosa succede sul collo, discesa da ala colpita (proposti 22,5 m).
- **Trovato nel repo:** `#242` → `plans/CHANGELOG.md` · `ADR-0095` → `plans/adr/ADR-0095-il-giro-ha-correzione-verifica-e-seconda-passata.md`

### MS-0026 · 2026-10-28 · Mappe a scala reale e barile sulla tenda

- **Data:** 2026-10-28
- **PR:** #261 #262 #292 #296
- **ADR:** —
- **Temi:** mappe arc07
- **Origine:** memoria del progetto, riga 26 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Mappe a scala reale (2026-10-21): PR #261 tenda di Zog'tar e campo, PR #262 altre 13 mappe ARC-07/09; simbolo 🎪 per i teli. PR #292 unita il 2026-10-28 (0a67e19): barile sulla tenda di Zog'tar, M7-C e M7-H; B16-B21 decise; B22-B25 decise dal DM il 2026-10-29 e unite con la PR #296 (21d4a8a), nessun INFERRED nel documento.
- **Trovato nel repo:** `#261` → `plans/esperimenti/barile-zogtar-2026-10-24/genera_mappe.py` · `#292` → `CHANGELOG.md` · `#296` → `CHANGELOG.md` · `0a67e19` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv` · `21d4a8a` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `mappe-scala-reale`
- **Solo qui:** `#262`

### MS-0027 · 2026-10-21 · Skill scrittura-italiana come eccezione (ADR-0097)

- **Data:** 2026-10-21
- **PR:** #260
- **ADR:** ADR-0097
- **Temi:** prosa adr contratto-seme
- **Origine:** memoria del progetto, riga 27 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #260 unita il 2026-10-21 (e639efa, ADR-0097 accettata): skill esterna scrittura-italiana (CC BY-SA, commit e397599, mai nel repo) usata solo come eccezione via references/scrittura-italiana-eccezione.md (documenti-regole in gioco, testi non capiti, Gulpease <60); colonna `Gulp.` in misura_craft --stile. Cieco DEF-4/DEF-5: nuova 10, vecchia 3 (soglia esatta); perse le 2 del «grigio» di Zog'tar. Handout DM/giocatore del contratto del Seme in /mnt/project-files/contratto-seme/; dissolvi superiore = regola 3.5 (CD 20, l'anticipo speso resta), scritto nella clausola 8; handout da portare in ARC07-HANDOUTS.
- **Trovato nel repo:** `#260` → `plans/CHANGELOG.md` · `ADR-0097` → `plans/adr/ADR-0097-scrittura-italiana-entra-come-eccezione.md` · `e397599` → `plans/adr/ADR-0097-scrittura-italiana-entra-come-eccezione.md`
- **Fuori dal repo:** `/mnt/project-files/contratto-seme/` (cartella condivisa del progetto)
- **Solo qui:** `e639efa`

### MS-0028 · 2026-10-22 · Ricerca sulla qualità misurabile

- **Data:** 2026-10-22
- **PR:** #264
- **ADR:** —
- **Temi:** prosa misura qualita
- **Origine:** memoria del progetto, riga 28 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #264 (2026-10-22, lotto 7 di AVVENTURE-COMMUNITY): ricerca sulla qualità misurabile (plans/RICERCA-QUALITA-MISURABILE-2026-10.md). 17 misure di prosa provate sui 38 voti ciechi del DM: nessuna lo prevede (vincono le versioni con più possessivi, p 0,057), quindi niente cancelli di prosa nuovi. 7a: `cieco_versioni` accetta etichette del perché (`7 B goffo spiega`, dieci da LAMP/TTCW). 7b: D18-D21 in domande_developer (domanda della scena, scelta con conseguenza, presagio del boss, rete indizi marcata `<!-- conclusione C1 -->`/`<!-- indizio C1 -->`), cancello solo sui master nuovi, 30 residui. 7c fronti/orologi in attesa del DM.
- **Trovato nel repo:** `#264` → `plans/STATO-E-ORDINE-DEI-PIANI.md`

### MS-0029 · 2026-10-23 · Rete del container: Hugging Face

- **Data:** 2026-10-23
- **PR:** —
- **ADR:** —
- **Temi:** ambiente rete
- **Origine:** memoria del progetto, riga 29 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Hugging Face dal container: funziona dal 2026-10-22, ma con HF_HUB_DISABLE_XET=1. Dal 2026-10-23 l'ambiente apre anche xethub, pytorch, SRD 3.5/PF1e, LanguageTool, Debian, typst.Ricerca web: se Firecrawl manca, WebSearch/WebFetch/curl via proxy.
- **Note di memoria:** `hugging-face-rete` · `ricerca-web-senza-firecrawl`

### MS-0030 · 2026-10-23 · Stanza contro spaCy

- **Data:** 2026-10-23
- **PR:** #264 #270
- **ADR:** —
- **Temi:** prosa sintassi misura
- **Origine:** memoria del progetto, riga 30 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #270 unita il 2026-10-23 nel ramo della #264, su main con la #264 (bfe0e39): Stanza contro spaCy (anche spaCy lg, peggio del md; tratti esterni Stanza + perplessità Qwen2.5-0.5B in sintassi/stanza/tratti-esterni.json). Stanza non vince (precisione dei calchi 87% contro 90%, calibrazione più debole, 50-100 volte più lento), quindi misura_sintassi resta con spaCy. Su 54 coppie votate nessuna misura sintattica passa Bonferroni. Segnalato: in riscrittura/ESITO-VOTO.md B08 la vince N, non V.
- **Trovato nel repo:** `#264` → `plans/STATO-E-ORDINE-DEI-PIANI.md` · `#270` → `plans/STATO-E-ORDINE-DEI-PIANI.md` · `bfe0e39` → `plans/STATO-E-ORDINE-DEI-PIANI.md`

### MS-0031 · 2026-10-22 · Watabou dal container

- **Data:** 2026-10-22
- **PR:** —
- **ADR:** —
- **Temi:** mappe citta
- **Origine:** memoria del progetto, riga 31 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Watabou pilotabile dal container dal 2026-10-22: piante Rethmar/Dauth/Channathgate in /mnt/project-files/mappe-valle-2026-10-22/watabou/.
- **Fuori dal repo:** `/mnt/project-files/mappe-valle-2026-10-22/watabou/` (cartella condivisa del progetto)
- **Note di memoria:** `watabou-generatore`

### MS-0032 · 2026-10-22 · Città della valle e taglie

- **Data:** 2026-10-22
- **PR:** #269 #271 #272
- **ADR:** —
- **Temi:** mappe citta canone
- **Origine:** memoria del progetto, riga 32 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Città della valle (PR #269, #271, #272 su main il 2026-10-22): entrano solo le piante del generatore nostro, non Watabou. Taglie scelte dal DM per reggere l'orda di ~10.000: Rethmar capitale ~18.000 ab., 110 ha, mura 4,3 km senza fossato; Dauth ~7.000, 42 ha, murata sullo sperone; Channathgate città aperta ~25.000, 250 ha, la più popolosa. Aperta: guarnigione nanica di Dauth.
- **Trovato nel repo:** `#269` → `plans/STATO-E-ORDINE-DEI-PIANI.md` · `#271` → `plans/STATO-E-ORDINE-DEI-PIANI.md` · `#272` → `plans/STATO-E-ORDINE-DEI-PIANI.md`

### MS-0033 · 2026-11-09 · Piattaforma a tre canali

- **Data:** 2026-11-09
- **PR:** #273 #353 #359
- **ADR:** ADR-0099
- **Temi:** piattaforma ci
- **Origine:** memoria del progetto, riga 33 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Piattaforma (ADR-0099, PR #273): tre canali Debian, Python 3.13. PR #353 unita il 2026-11-08 (125e535): ruff, uv, converters/ stable; xdist in testing fino al 22/11; ruleset da aggiornare dal DM. Job Python 3.14 non bloccante dal 2026-11-09 (#359).
- **Trovato nel repo:** `#273` → `plans/CHANGELOG.md` · `#353` → `plans/esperimenti/promozioni-2026-11-08/MISURE.md` · `#359` → `plans/esperimenti/python-314-2026-11-09/MISURE.md` · `ADR-0099` → `plans/adr/ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md`
- **Note di memoria:** `piattaforma-promozioni-stable` · `piattaforma-di-sviluppo`
- **Solo qui:** `125e535`

### MS-0034 · 2026-10-23 · Rilascio v1.0.0

- **Data:** 2026-10-23
- **PR:** #275
- **ADR:** —
- **Temi:** rilasci documentazione
- **Origine:** memoria del progetto, riga 34 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Rilasci: PR #275 unita il 2026-10-23, v1.0.0 pubblicata (skill riproducibili, SHA256SUMS, Sigstore). Rilasciare = PR con `## [X.Y.Z]` in CHANGELOG.md e `__version__`; ogni cambio di superficie pubblica va in «Non rilasciato». Architettura in docs/ARCHITETTURA.md (20 diagrammi Mermaid, poi 26).
- **Trovato nel repo:** `#275` → `plans/CHANGELOG.md`

### MS-0035 · 2026-10-23 · Merge passato al thread padre

- **Data:** 2026-10-23
- **PR:** —
- **ADR:** —
- **Temi:** regole pr
- **Origine:** memoria del progetto, riga 35 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Regolal DM 2026-10-23: a CI verde il thread figlio avvisa i thread interessati e passa il merge al thread padre, che tiene la lista delle PR aperte.
- **Note di memoria:** `chiusura-pr-dai-thread-figli`

### MS-0036 · 2026-10-23 · Pipeline prova-1, modello di preferenza e lotto 7

- **Data:** 2026-10-23
- **PR:** #285 #286
- **ADR:** ADR-0102
- **Temi:** prosa misura canone
- **Origine:** memoria del progetto, riga 36 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** 2026-10-23 voto DM pipeline prova-1: pipeline 4/orig 1/pari 1 (non dimostrato); modello di preferenza passa SOGLIA (0,661 su 59, 5/5 in prospettiva) → `migliora` tiene l'originale se la migliore < 0,5. Aperta per il DM: i voti ciechi premiano i possessivi, contro italiano-nativo §1. ADR-0102 va al thread schede PNG. Poi PR #285 unita il 2026-10-23 (f2da2512): lotto 7 chiuso, D4 schede ARC-08 al Bestiario (nella #286), D5 possessivo vietato solo su corpo/cose addosso, D6 fronti e orologi canone da ARC-08 (`ARCnn-FRONTI.yaml` in CI, orologio a tempo con `unita`).
- **Trovato nel repo:** `#286` → `plans/CHANGELOG.md` · `ADR-0102` → `plans/adr/ADR-0102-lo-stile-delle-piante-e-i-generatori-delle-citta-nel-repo.md`
- **Solo qui:** `#285` · `f2da2512` · PR #285 unita 2026-10-23 (f2da2512) lotto 7 chiuso

### MS-0037 · 2026-10-23 · P15 chiuso: CHANGELOG a 5 colonne

- **Data:** 2026-10-23
- **PR:** #283
- **ADR:** —
- **Temi:** piani ci
- **Origine:** memoria del progetto, riga 37 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #283 unita il 2026-10-23: P15 chiuso (intestazioni piani = INDEX, CHANGELOG a 5 colonne con controllo in check_plans_discipline.py, RECUPERO D3/D4 spostate in RIPRESA-PR D2/D11; §4 a 14 aperte).
- **Trovato nel repo:** `#283` → `plans/CHANGELOG.md`

### MS-0038 · 2026-10-23 · Inventario Gemini/AI Studio

- **Data:** 2026-10-23
- **PR:** #284
- **ADR:** —
- **Temi:** inventario
- **Origine:** memoria del progetto, riga 38 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Inventario Gemini/AI Studio contro il repo: PR #284 unita il 2026-10-23, D1-D6 al DM.
- **Note di memoria:** `inventario-gemini-aistudio`
- **Solo qui:** `#284` · Inventario Gemini PR #284

### MS-0039 · 2026-10-24 · Archi senza testo: censimento e decisioni

- **Data:** 2026-10-24
- **PR:** #287 #290
- **ADR:** —
- **Temi:** archi censimento
- **Origine:** memoria del progetto, riga 39 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #287 unita il 2026-10-23 (censimento file non markdown archi 00-10, arco 05 trascritto). D1-D12 decise dal DM il 2026-10-24, PR #290 unita (b1500ca1): cronaca corretta, P28 chiuso, testi altrui in */_testi-altrui/, P30 aperto su P30-a.
- **Trovato nel repo:** `#287` → `plans/STATO-E-ORDINE-DEI-PIANI.md`
- **Note di memoria:** `archi-senza-testo`
- **Solo qui:** `#290` · `b1500ca1` · D1-D12 decise 2026-10-24, PR #290 (b1500ca1) P28 chiuso, _testi-altrui, P30-a

### MS-0040 · 2026-10-29 · Personaggi in posa con l'AI (ADR-0104)

- **Data:** 2026-10-29
- **PR:** —
- **ADR:** ADR-0015 ADR-0104
- **Temi:** immagini adr
- **Origine:** memoria del progetto, riga 40 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Personaggi in posa con l'AI (2026-10-29): esiste già catena testo-solo (ADR-0015/0019, GUIDA-IMMAGINI, comfyui_batch), manca posa/identità da immagine; ADR-0104 proposta, D1-D4 al DM.
- **Trovato nel repo:** `ADR-0015` → `plans/adr/ADR-0015-standard-prompt-immagine.md` · `ADR-0104` → `plans/PIANO-STANDARD-STAMPA.md`
- **Note di memoria:** `immagini-personaggi-in-posa`

### MS-0041 · 2026-10-31 · Standard di stampa (ADR-0105, ADR-0106)

- **Data:** 2026-10-31
- **PR:** #295 #298
- **ADR:** ADR-0105 ADR-0106
- **Temi:** stampa booklet mappe
- **Origine:** memoria del progetto, riga 41 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Standard di stampa: PR #295 unita il 2026-10-29 (fe93e5b; ADR-0105 con D5 = appendice delle creature + tattica nell'incontro). PR #298 unita il 2026-10-31 (ae8d1884): ADR-0106, ogni mappa in pianta da stampa, nessun disegno a caratteri stampato nei booklet (validate_booklets), schemi da render_schemi.py. Piano STANDARD-STAMPA ancora in corso.
- **Trovato nel repo:** `#295` → `plans/CHANGELOG.md` · `#298` → `plans/CHANGELOG.md` · `ADR-0105` → `plans/adr/ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md` · `ADR-0106` → `plans/adr/ADR-0106-ogni-mappa-si-stampa-in-pianta.md` · `fe93e5b` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `riquadro-creature-booklet`
- **Solo qui:** `ae8d1884`

### MS-0042 · 2026-10-30 · Cuore della Montagna: schieramento dei nani

- **Data:** 2026-10-30
- **PR:** —
- **ADR:** —
- **Temi:** mappe arc08 canone
- **Origine:** memoria del progetto, riga 42 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Cuore della Montagna (2026-10-30): 90 nani schierati verso la porta (centro pesante, ali piegate), numeri invariati; allineata anche ARC-08 MAPPA 5.
- **Note di memoria:** `cuore-montagna-nani`

### MS-0043 · 2026-10-31 · Regola: vince la decisione senza regressione

- **Data:** 2026-10-31
- **PR:** —
- **ADR:** —
- **Temi:** regole decisioni
- **Origine:** memoria del progetto, riga 43 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Regolal DM 2026-10-31: tra decisioni che si superano vince quella senza regressione misurabile, i dubbi vanno a card con la consigliata. Voci ⬜ dell'indice §0 lavorate un thread alla volta.
- **Note di memoria:** `decisioni-superate-regressione`

### MS-0044 · 2026-11-02 · Stand alone Il Giardino di Sale e Calce

- **Data:** 2026-11-02
- **PR:** #301
- **ADR:** —
- **Temi:** stand-alone
- **Origine:** memoria del progetto, riga 44 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Stand alone «Il Giardino di Sale e Calce» dalla chat Gemini: PR #301 unita il 2026-11-02 (2cf8a0d): modulo 3.5 a Rethmar e PF1e a Qasr al-Milah; resta un tavolo vero.
- **Trovato nel repo:** `#301` → `plans/CHANGELOG.md` · `2cf8a0d` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `standalone-giardino-sale-calce`

### MS-0045 · 2026-11-01 · Drappo e Palio misurati

- **Data:** 2026-11-01
- **PR:** #302
- **ADR:** —
- **Temi:** stand-alone misura
- **Origine:** memoria del progetto, riga 45 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Drappo/Palio misurati (2026-11-01): il Drappo deriva dal Palio, 0 frasi in comune, 62% dell'impianto condiviso; PR #302 unita (229adc6) con lo spostamento del Drappo in 10-stand-alone/Il-Drappo-di-Tarsilia e i rimandi nei due sensi.
- **Trovato nel repo:** `#302` → `plans/CHANGELOG.md` · `229adc6` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `drappo-palio-genealogia`

### MS-0046 · 2026-11-03 · Fork e upstream EarlRagnar78

- **Data:** 2026-11-03
- **PR:** #33
- **ADR:** —
- **Temi:** fork git
- **Origine:** memoria del progetto, riga 46 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Fork: gsamuele78/RumblingStone è fork di EarlRagnar78/RumblingStone. Il DM (2026-11-02): PR dal fork verso EarlRagnar78, in conflitto vince il fork; merge su EarlRagnar78 solo col sì del DM e a fork stabile. Il 2026-11-03 la PR #33 su EarlRagnar78 (59ff922) ha riallineato i due main, alberi identici.
- **Trovato nel repo:** `#33` → `plans/adr/ADR-0075-il-ciclo-del-master-vale-per-ogni-piano.md`
- **Note di memoria:** `fork-e-upstream`
- **Solo qui:** `59ff922` · 59ff922

### MS-0047 · 2026-11-03 · Serata del 2026-11-02 e booklet v5

- **Data:** 2026-11-03
- **PR:** #305
- **ADR:** —
- **Temi:** serata booklet arc07
- **Origine:** memoria del progetto, riga 47 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Serata 2026-11-02 (il DM): si riparte dal volo sul campo, pozioni di Kettra fatte, si rigioca lo sgancio del barile. PR #305: barile cucito in DEF-4 Scene 6/9/10/11 + Echo Ledger, riga in DEF-5, regia «dal barile al drago», colophon v2. PDF in /mnt/project-files/sessione-2026-11-02/. Ramo di gruppo fermo alla sessione 4 (25/09): patch Bane (10-15), Cintura (10-18) e canone Belkram mai applicate. In locale typst 0.15.1 va scaricato nello scratchpad (install in /usr/local/bin negato). Poi (2026-11-03) booklet v5 con cap. II «Chi c'è stanotte» (chi è/vuole/aspetto/ritratto/scheda + mappe M7-C/M7-H), barile cap. III, manifest `"schede": "entrambe"` (scheda nel capitolo E appendice, il DM lo vuole); CI verde su 651cf82.
- **Trovato nel repo:** `#305` → `plans/CHANGELOG.md`
- **Fuori dal repo:** `/mnt/project-files/sessione-2026-11-02/` (cartella condivisa del progetto)
- **Solo qui:** `651cf82` · PDF /mnt/project-files/sessione-2026-11-02/ · 651cf82

### MS-0048 · 2026-11-02 · Booklet pronto solo dopo lettura da DM

- **Data:** 2026-11-02
- **PR:** —
- **ADR:** —
- **Temi:** regole booklet
- **Origine:** memoria del progetto, riga 48 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Feedback del DM 2026-11-02: booklet pronto solo dopo lettura da DM scena per scena.
- **Note di memoria:** `booklet-letto-da-dm`

### MS-0049 · 2026-11-03 · Usabilità al tavolo (ADR-0107, ADR-0108)

- **Data:** 2026-11-03
- **PR:** #305 #306
- **ADR:** ADR-0107 ADR-0108
- **Temi:** booklet adr usabilita
- **Origine:** memoria del progetto, riga 49 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Usabilità al tavolo: PR #306 unita il 2026-11-03 (47489fb) con dentro la #305. ADR-0107 e ADR-0108 accettate: chi_si_incontra+entrambe in 6 booklet (Terros escluso), cancelli in ogni skill, NLI provata e non adottata. Card al DM: 4 conti dei master all'SRD.
- **Trovato nel repo:** `#305` → `plans/CHANGELOG.md` · `#306` → `plans/CHANGELOG.md` · `ADR-0107` → `plans/adr/ADR-0107-chi-si-incontra-sta-nel-capitolo.md` · `ADR-0108` → `plans/adr/ADR-0108-i-cancelli-deterministici-stanno-in-ogni-skill.md` · `47489fb` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `usabilita-al-tavolo`

### MS-0050 · 2026-11-03 · Documentazione dopo la #306

- **Data:** 2026-11-03
- **PR:** #306 #307 #308 #309
- **ADR:** —
- **Temi:** documentazione
- **Origine:** memoria del progetto, riga 50 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Documentazione dopo la #306: PR #307 unita il 2026-11-03 (90db0f7), allineata a #308 e #309 (ARCHITETTURA 26 diagrammi, §10.1/§11-§13/§16/§18/§19; README 107 ADR; GUIDA-BOOKLET-E-PDF). Ogni PR che aggiunge una riga a plans/CHANGELOG.md rigenera MEMORIA.md.
- **Trovato nel repo:** `#306` → `plans/CHANGELOG.md` · `#307` → `plans/CHANGELOG.md` · `#308` → `plans/CHANGELOG.md` · `#309` → `plans/CHANGELOG.md` · `90db0f7` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`

### MS-0051 · 2026-11-03 · Tecnica scartata: rifarla con configurazione rigorosa

- **Data:** 2026-11-03
- **PR:** #308 #309
- **ADR:** —
- **Temi:** regole misura
- **Origine:** memoria del progetto, riga 51 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Feedback del DM 2026-11-03: una tecnica scartata va rifatta con configurazione rigorosa e rimisurata; ciò che un controllo trova si corregge e il controllo diventa cancello (PR #308, PR #309 unita 008c07c, NLI fedeltà in ciclo_prosa).
- **Trovato nel repo:** `#308` → `plans/CHANGELOG.md` · `#309` → `plans/CHANGELOG.md` · `008c07c` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `feedback-configurazione-rigorosa`

### MS-0052 · 2026-11-07 · P16 marcature INFERRED da 240 a 25

- **Data:** 2026-11-07
- **PR:** #310 #311 #313
- **ADR:** —
- **Temi:** inferred marcature
- **Origine:** memoria del progetto, riga 52 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** P16 marcature INFERRED: 240 → 25 aperte (#310, #311 unite; #313 con i lotti 3-5 unita il 2026-11-07). Le 25 restanti sono righe di regole. Termine ufficiale «Sbilanciare», mai «sgambetto».
- **Trovato nel repo:** `#310` → `Bestiario/pregen-pcgen/Myconid Sovereign - Monster Stat Block - Kassoon.com_files/js.js` · `#311` → `plans/esperimenti/p16-inferred-2026-11-04/ARC07-DECISIONI.md` · `#313` → `plans/CHANGELOG.md`
- **Note di memoria:** `p16-marcature-inferred`

### MS-0053 · 2026-11-04 · Card chiuse solo se risolte

- **Data:** 2026-11-04
- **PR:** —
- **ADR:** —
- **Temi:** regole card
- **Origine:** memoria del progetto, riga 53 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Regolal DM 2026-11-04: card chiuse solo se già fatte/risolte/superate (con prova).
- **Note di memoria:** `card-solo-se-risolte`

### MS-0054 · 2026-11-05 · Registro PX completato al 25/09

- **Data:** 2026-11-05
- **PR:** #312
- **ADR:** —
- **Temi:** campagna px
- **Origine:** memoria del progetto, riga 54 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Registro PX = CalcoloPuntiEperienza-current.ods (+ campaign/REGISTRO-PX.md), completato fino al 25/09 con le card del DM del 2026-11-05 (PR #312): Th/To/Ar al 14° fermi a 104.999, Hella 86.354 passa nella notte di DEF-4. Storia giocata archi 00-06 in plans/esperimenti/p16-inferred-2026-11-04/STORIA-ARCHI-00-06.md.
- **Trovato nel repo:** `#312` → `plans/esperimenti/p16-inferred-2026-11-04/ARC09-DECISIONI.md`
- **Note di memoria:** `registro-px-gruppo`
- **Solo qui:** STORIA-ARCHI-00-06.md

### MS-0055 · 2026-11-05 · Indice §0 al 4-5 novembre

- **Data:** 2026-11-05
- **PR:** #300 #310 #311 #312
- **ADR:** ADR-0114
- **Temi:** piani inferred
- **Origine:** memoria del progetto, riga 55 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Indice §0 (2026-11-04/05): #300 unita (8d4bb89, P17/P18/P26); P16 con #310 (ARC-08 109→11), #311 (mare a 520 m, ARC-07 70→1), #312 (fcf6642): 61 aperte sul repo. RECUPERO D5 rifatta col criterio del DM: 2 card aperte. Card «guida agenti» ritirata l'8/11: superata da ADR-0114 (esempi in evals/, testo letto = dato).
- **Trovato nel repo:** `#310` → `Bestiario/pregen-pcgen/Myconid Sovereign - Monster Stat Block - Kassoon.com_files/js.js` · `#311` → `plans/esperimenti/p16-inferred-2026-11-04/ARC07-DECISIONI.md` · `#312` → `plans/esperimenti/p16-inferred-2026-11-04/ARC09-DECISIONI.md` · `ADR-0114` → `plans/adr/ADR-0114-ogni-prompt-ha-una-scheda-e-le-sue-prove.md` · `8d4bb89` → `plans/esperimenti/p16-inferred-2026-11-04/ARC08-DECISIONI.md` · `fcf6642` → `plans/esperimenti/p16-inferred-2026-11-04/ARC09-DECISIONI.md`
- **Solo qui:** `#300` · #300 unita (8d4bb89, P17/P18/P26) · Card guida agenti ritirata l'8/11 superata da ADR-0114

### MS-0056 · 2026-11-07 · Standard marcature INFERRED (ADR-0109)

- **Data:** 2026-11-07
- **PR:** #314
- **ADR:** ADR-0109
- **Temi:** inferred adr
- **Origine:** memoria del progetto, riga 56 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Standard marcature INFERRED (2026-11-07, PR #314): ADR-0109, A/B 11 meglio/4 peggio, P16 a 0, migrazione ACCEPTED→CANONE e controlla_marche.py fatti; resta card statblock potenziati.
- **Trovato nel repo:** `#314` → `plans/PIANO-SISTEMI-DI-GIOCO-PLUGIN.md` · `ADR-0109` → `plans/adr/ADR-0109-una-marcatura-sola-e-il-dm-decide-il-canone.md`
- **Note di memoria:** `standard-marcature-inferred`

### MS-0057 · 2026-11-09 · Regolamenti plugin e motore (ADR-0111, ADR-0112)

- **Data:** 2026-11-09
- **PR:** #355 #361
- **ADR:** ADR-0111 ADR-0112
- **Temi:** motore plugin
- **Origine:** memoria del progetto, riga 57 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Regolamenti plugin ADR-0111 e motore ADR-0112: tutto su main (L0-L8, F0-F6, #355, #361 19c8670); piano chiuso il 9/11.
- **Trovato nel repo:** `#361` → `plans/esperimenti/plugin-regole-2026-11-09/RAPPORTO.md` · `ADR-0111` → `plans/adr/ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md` · `ADR-0112` → `plans/adr/ADR-0112-il-motore-e-agnostico-e-le-regole-d20-sono-dati-e-formule.md`
- **Note di memoria:** `regolamenti-plugin-cronologia` · `sistemi-di-gioco-plugin`
- **Solo qui:** `#355` · `19c8670`

### MS-0058 · 2026-11-08 · Regola: si parte dallo standard di fatto

- **Data:** 2026-11-08
- **PR:** —
- **ADR:** —
- **Temi:** regole dipendenze
- **Origine:** memoria del progetto, riga 58 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Regolal DM 2026-11-08 (codice, mappe, storia, editoria, booklet): si parte dallo standard de facto, il fatto in casa entra solo se la misura boccia lo standard (motivo nell'ADR); librerie dentro il pacchetto (modello iemod-fetch). Librerie oltre la stdlib solo se standard di fatto e la misura dice che migliorano (D1 del motore: simpleeval e fastjsonschema dentro; pydantic fuori perché non prende un difetto in più).
- **Note di memoria:** `feedback-standard-di-fatto`

### MS-0059 · 2026-11-07 · Termini ufficiali, razze PF1e e oggetti unici

- **Data:** 2026-11-07
- **PR:** #314 #315 #316 #317 #318 #319
- **ADR:** ADR-0110
- **Temi:** regole lessico canone
- **Origine:** memoria del progetto, riga 59 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** 2026-11-07: #315, #314, #316 (ADR-0110) e #318 (eae2126: fase 5 ARC-07/08, 37 razze PF1e tipo «razza» per il plugin #317) unite. A/B rifatta C10/C11/C16: 2 inventati non marcati contro 15/12. Oggetti unici in campaign/OGGETTI-DELLA-CAMPAGNA.md (esito `campagna` del controllo). Schede dei 152 termini sconosciuti con scelta del DM: artifact K9QvJMTuxvwK7mBPxF2fuD (db: termini, scelte); PR #319 le applica. Criterio Il DM: termine sconosciuto → SRD → 3.5 → PF1e.
- **Trovato nel repo:** `#314` → `plans/PIANO-SISTEMI-DI-GIOCO-PLUGIN.md` · `#315` → `skills/forgotten-realms-lore/references/fr-feats.md` · `#316` → `plans/PIANO-SISTEMI-DI-GIOCO-PLUGIN.md` · `#318` → `plans/PIANO-SISTEMI-DI-GIOCO-PLUGIN.md` · `#319` → `plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md` · `ADR-0110` → `plans/adr/ADR-0110-i-termini-ufficiali-hanno-una-tabella-e-un-cancello.md` · `eae2126` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `fonti-nomi-italiani-regole`
- **Solo qui:** `#317` · 152 termini sconosciuti artifact K9QvJMTuxvwK7mBPxF2fuD; PR #319

### MS-0060 · 2026-11-07 · Indici dei talenti 3.5/PF1e

- **Data:** 2026-11-07
- **PR:** #319 #328
- **ADR:** —
- **Temi:** regole talenti
- **Origine:** memoria del progetto, riga 60 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Talenti 3.5/PF1e (#319-#328, 2026-11-07): indici tsv, sconosciuti 0, cricchetto CI a 0.
- **Trovato nel repo:** `#319` → `plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md`
- **Note di memoria:** `talenti-indici-2026-11-07`
- **Solo qui:** `#328` · Talenti #319-#328 indici tsv sconosciuti 0 cricchetto

### MS-0061 · 2026-11-08 · Prompt a schede (ADR-0114)

- **Data:** 2026-11-08
- **PR:** #339 #343
- **ADR:** ADR-0114
- **Temi:** prompt skill
- **Origine:** memoria del progetto, riga 61 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Standard dei prompt a schede: PR #339 unita il 2026-11-08 (d0cc674, ADR-0114): GUIDA-SCHEDE-PROMPT, 54 prove in skills/*/evals/, prove_skill.py. Lotto 2: PR #343 unita (A/B 32→30 inventati; ADR-0114 accettata). Resta: avvisi check_schede bloccanti dopo 2 settimane.
- **Trovato nel repo:** `ADR-0114` → `plans/adr/ADR-0114-ogni-prompt-ha-una-scheda-e-le-sue-prove.md` · `d0cc674` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `standard-prompt-a-schede`
- **Solo qui:** `#339` · `#343` · PR #339 (d0cc674 ADR-0114) 54 prove skills/*/evals, prove_skill.py; lotto 2 PR #343 A/B 32→30 · #343

### MS-0062 · 2026-11-08 · Strumenti binari da PyPI (ADR-0116)

- **Data:** 2026-11-08
- **PR:** #338 #341 #342
- **ADR:** ADR-0113 ADR-0116
- **Temi:** piattaforma strumenti
- **Origine:** memoria del progetto, riga 62 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Strumenti binari: ADR-0113 (mise, #338/#341) superata da ADR-0116 (PR #342, 29056bf): typst e pdfimpose da PyPI, mise/Renovate/strumenti.py tolti, bundle_offline.py nel rilascio. Check richiesti su main = Validate + Build skill packages.
- **Trovato nel repo:** `#338` → `plans/adr/ADR-0113-gli-strumenti-binari-si-installano-da-un-lockfile.md` · `#341` → `plans/CHANGELOG.md` · `#342` → `plans/CHANGELOG.md` · `ADR-0113` → `plans/adr/ADR-0113-gli-strumenti-binari-si-installano-da-un-lockfile.md` · `ADR-0116` → `plans/adr/ADR-0116-typst-si-installa-da-pypi.md` · `29056bf` → `plans/esperimenti/promozioni-2026-11-08/MISURE.md`
- **Note di memoria:** `strumenti-binari-lockfile`

### MS-0063 · 2026-11-08 · Roadmap unica del motore

- **Data:** 2026-11-08
- **PR:** —
- **ADR:** —
- **Temi:** roadmap
- **Origine:** memoria del progetto, riga 63 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Roadmap unica: /mnt/project-files/roadmap-motore-2026-11-08/DECISIONI-E-ROADMAP.md.
- **Fuori dal repo:** `/mnt/project-files/roadmap-motore-2026-11-08/DECISIONI-E-ROADMAP.md` (cartella condivisa del progetto)
- **Solo qui:** Roadmap unica DECISIONI-E-ROADMAP.md

### MS-0064 · 2026-11-10 · Merge del 10 novembre e blocco 1

- **Data:** 2026-11-10
- **PR:** #363 #364 #365 #366 #367 #368
- **ADR:** ADR-0118 ADR-0120 ADR-0122
- **Temi:** pr motore
- **Origine:** memoria del progetto, riga 64 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** 2026-11-10 su main: #364 (ADR-0118), #363, #365, #367, #366, #368 (f65d78e, ADR-0120 «d» eufonica in testing fino al 24/11). Blocco 1 chiuso; prossimo 1-bis standard del volume (ADR-0122).
- **Trovato nel repo:** `#363` → `plans/CHANGELOG.md` · `#364` → `plans/CHANGELOG.md` · `#365` → `plans/CHANGELOG.md` · `ADR-0118` → `plans/adr/ADR-0118-un-numero-entra-solo-se-la-regola-lo-calcola.md` · `ADR-0120` → `plans/adr/ADR-0120-la-d-eufonica-si-misura-con-una-regex-tarata-su-languagetool.md` · `f65d78e` → `plans/adr/ADR-0121-un-plugin-di-regole-si-misura-contro-la-fonte.md`
- **Note di memoria:** `thread-padre-pr` · `blocco1-scelte-8-11`
- **Solo qui:** `#366` · `#367` · `#368` · `ADR-0122` · 2026-11-10 #364 #363 #365 #367 #366 #368 (f65d78e ADR-0120) · #367 · Blocco 1 chiuso; prossimo 1-bis standard del volume ADR-0122

### MS-0065 · 2026-11-10 · Milestone v1.1.0-v1.5.0

- **Data:** 2026-11-10
- **PR:** —
- **ADR:** —
- **Temi:** roadmap milestone
- **Origine:** memoria del progetto, riga 65 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Milestone GitHub v1.1.0…v1.5.0 fissate il 2026-11-10.
- **Note di memoria:** `milestone-roadmap`
- **Solo qui:** Milestone GitHub v1.1.0…v1.5.0 fissate 2026-11-10

### MS-0066 · 2026-11-10 · Regole PF1e del cancello e regole complete

- **Data:** 2026-11-10
- **PR:** #363 #369 #372 #375
- **ADR:** ADR-0119 ADR-0121
- **Temi:** regole motore plugin
- **Origine:** memoria del progetto, riga 66 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Regole PF1e del cancello (ADR-0119, #363): 14 conti in prova, promozione proposta 23/11. Audit plugin regole (ADR-0121): 3.5 605/606, PF1e 217/217; completamento = v1.2.0. Regole complete 3.5/PF1e: lotti 1-5 su main (#369, #372-#375, ultimo 0f70d7c), tre limiti ADR-0121 chiusi.
- **Trovato nel repo:** `#363` → `plans/CHANGELOG.md` · `#372` → `Bestiario/pregen-pcgen/Myconid Sovereign - Monster Stat Block - Kassoon.com_files/js.js` · `ADR-0119` → `plans/adr/ADR-0119-le-regole-pf1e-del-cancello-vengono-dal-prd.md` · `ADR-0121` → `plans/adr/ADR-0121-un-plugin-di-regole-si-misura-contro-la-fonte.md`
- **Solo qui:** `#369` · `#375` · `0f70d7c` · Regole complete lotti 1-5 (#369 #372-#375, 0f70d7c)

### MS-0067 · 2026-11-12 · Verifica schede via MCP, coerenza, regole senza omissioni

- **Data:** 2026-11-12
- **PR:** #378 #379 #380
- **ADR:** ADR-0124 ADR-0125 ADR-0126
- **Temi:** regole motore coerenza
- **Origine:** memoria del progetto, riga 67 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Verifica schede via MCP (ADR-0124, PR #378 unita il 2026-11-12, 43656328): violazioni 34 → 7, le 7 al DM. Coerenza della storia (ADR-0125, PR #379): +4 difetti su 35, parafrasi 1/18. Regole senza omissioni (ADR-0126, 12 lotti): lotto 1 = PR #380.
- **Trovato nel repo:** `#378` → `plans/CHANGELOG.md` · `#379` → `plans/esperimenti/regole-senza-omissioni-2026-11-12/INVENTARIO-E-PIANO.md` · `#380` → `plans/esperimenti/regole-senza-omissioni-2026-11-12/INVENTARIO-E-PIANO.md` · `ADR-0124` → `plans/adr/ADR-0124-le-regole-si-verificano-in-python-e-l-llm-riceve-regola-e-controesempio.md` · `ADR-0125` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md` · `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`

### MS-0068 · 2026-11-12 · La memoria storica nel repo e l'addendum del changelog

- **Data:** 2026-11-12
- **PR:** —
- **ADR:** ADR-0127
- **Temi:** memoria regole ci
- **Origine:** addendum della riga del 2026-11-12 «la memoria storica nel repo (ADR-0127)» in `plans/CHANGELOG.md`
- **Testo:** Richiesta del DM: verificare che la riduzione della memoria del progetto (da circa 25 KB a 8 KB, 2026-11-12) non avesse perso niente, salvare il resto nel repo collegato al changelog, farne un meccanismo che eviti la saturazione e si possa leggere quando serve, e obbligare tutte le sessioni «tipo changelog, tipo addendum». Fatto: MS-0001…MS-0067 con le 67 righe della memoria lunga; `scripts/memoria_storica.py` (lettore e `--check`, nel server MCP); addendum in `check_plans_discipline.py` (riga del changelog senza voce nuova = PR bocciata); regola in AGENTS.md, nel modello delle PR, nella skill rumblingstone-plans e nell'intestazione della memoria del progetto. Misura: riferimenti delle 67 righe nel repo da 127/165 a 165/165; fatti di contenuto non trovati da 24 a 0. Delle 67 righe 53 nascevano da una PR (l'addendum le avrebbe prese), 14 no (regole, ambiente, routine, roadmap, scelte in chat): per queste resta solo la regola. Deciso dal DM (card del 2026-11-12): i dati personali tolti da MS-0005, MS-0006, MS-0009 restano fuori dal repo, nelle note di memoria. Notato durante la verifica: ADR-0104 (personaggi in posa) è citato come «proposta» ma il file non esiste in `plans/adr/`; ADR-0123 è usato sia dal ramo della #371 sia dai commit locali della #370.
- **Trovato nel repo:** `ADR-0127` → `plans/adr/ADR-0127-la-memoria-corta-archivia-nel-repo-prima-di-togliere.md`

### MS-0069 · 2026-11-12 · ADR-0126 lotto 1: cumulo dei bonus, niente tolleranza

- **Data:** 2026-11-12
- **PR:** #380
- **ADR:** ADR-0126 ADR-0124
- **Temi:** regole motore
- **Origine:** voce scritta dopo il merge, per la riga del 2026-11-12 «ADR-0126 … lotto 1» in `plans/CHANGELOG.md` (la PR è entrata prima dell'addendum)
- **Testo:** PR #380 unita il 2026-11-12 (merge b23fd0d0). Programma «regole senza omissioni» in 12 lotti, chiesto dal DM; lotto 1 = cumulo dei bonus per tipo (`bonus.cumulo`, `dmcore.bonus`), tiri salvezza e attacco senza tolleranza in `verifica_scheda` (`--tolleranza` per tornare indietro). Misura: errori messi apposta visti 55% → 79% (701 → 1.007 su 1.279), TS +2 visti 1/362 → 286/362; 22 numeri senza sorgente chiusi (16 in 14 schede con la sorgente scelta dal DM: mantello della resistenza o bonus razziale). Prossimo: lotto 1-bis (CA 3.5, oggetti col prezzo). Il DM ha scelto anche: variante della campagna per elemento intero, motore dichiarabile e vincolabile, forme ibride solo nella variante e registrate.
- **Trovato nel repo:** `#380` → `plans/CHANGELOG.md` (riga senza numero di PR) · `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** lo SHA del merge b23fd0d0 e il numero #380 accanto alla riga del changelog

### MS-0070 · 2026-11-12 · Coerenza della storia contro state.yaml

- **Data:** 2026-11-12
- **PR:** #379
- **ADR:** ADR-0125
- **Temi:** coerenza storia regole
- **Origine:** voce scritta dopo il merge, per le due righe ADR-0125 del 2026-11-12 in `plans/CHANGELOG.md` (la PR è entrata prima dell'addendum)
- **Testo:** PR #379 unita il 2026-11-12 (merge c2cc7756), dopo la #380. Verificatore deterministico della storia con àncora su `state.yaml`; scelta del DM «solo le regole precise, in testing»: `coerenza_campagna.py fatti --state` con S1 arrivo dell'orda, S5 portatore, S6 modifiche permanenti, S7 echi armati senza scena; «chi sa cosa» fra i non verificabili; S2-S4 restano in laboratorio. Misura: +4 incoerenze su 35 del corpus storico, mutanti S1/S5/S6 9/9, parafrasi 0/9 (1/18 nel prototipo), 0 violazioni su main. Il server MCP ora passa le opzioni di un sottocomando. Segue la PR del grafo degli eventi (Prolog/clingo equivalenti a Python; RAG col modello locale 3B: 0 rilievi veri su 23); prova sulla GPU locale ancora da fare. Aperti al DM: i 5 file di ARC-09 tarati per l'11°-12°.
- **Trovato nel repo:** `#379` → `plans/CHANGELOG.md` · `ADR-0125` → `plans/adr/` (file ADR-0125)
- **Solo qui:** lo SHA del merge c2cc7756; il seguito sul grafo degli eventi e l'esito del RAG col modello locale

### MS-0071 · 2026-11-12 · ADR-0126 lotto 1-bis: classe armatura del 3.5

- **Data:** 2026-11-12
- **PR:** #382
- **ADR:** ADR-0126
- **Temi:** regole motore schede
- **Origine:** voce scritta dopo il merge, per la riga del 2026-11-12 «ADR-0126, lotto 1-bis» in `plans/CHANGELOG.md` (la PR è entrata prima dell'addendum)
- **Testo:** PR #382 unita il 2026-11-12 (merge 66ce69b6, base c2cc7756). `dmcore.classe_armatura` ricostruisce la CA del 3.5 dalle voci (armature e scudi dalla tabella, bonus per tipo, contatto, sprovvista); sensi della razza e CD delle capacità dentro `verifica_scheda`; banco `muta_ca.py`; 18 schede corrette per la CA e 10 per la scurovisione (27 file del Bestiario toccati, impronta delle creature rigenerata); `_dv` somma i dadi vita di più classi. Misura: errori di CA messi apposta visti 0/379 → 377/379; scarti veri nel Bestiario 31 → 0. Limiti: 28 schede su 145 senza voci di CA restano non verificabili; scurovisione vista solo per le razze in tabella (10/25); gli oggetti col prezzo, annunciati per il 1-bis, passano al lotto 8.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** il numero #382 e lo SHA del merge 66ce69b6 accanto alla riga del changelog; lo spostamento degli oggetti col prezzo dal lotto 1-bis al lotto 8 rispetto a quanto annunciato in memoria

### MS-0072 · 2026-11-12 · Documentazione della v1.1.0 e docs/ in Diátaxis

- **Data:** 2026-11-12
- **PR:** #371 (e #381)
- **ADR:** ADR-0123 ADR-0117 ADR-0111 ADR-0112
- **Temi:** documentazione piattaforma
- **Origine:** addendum delle due righe del 2026-11-10 in `plans/CHANGELOG.md` (passo della documentazione della milestone v1.1.0; ADR-0123)
- **Testo:** PR #371, passo della documentazione della milestone v1.1.0 chiesto dal DM il 2026-11-09: `dm.py sistemi`, ARCHITETTURA §19 (motore e plugin) e §20 (da dove viene un fatto), guida pratica dei sistemi di gioco e riferimento dei plugin (20 capacità al 2026-11-12). Card del DM del 2026-11-10: Diátaxis scelta «Riorganizzare docs/ subito» (alternativa B, contro la consigliata «regola per le nuove più etichette»), ADR-0117 accettata. `docs/` in `tutorials/`, `how-to/`, `reference/`, `explanation/`; le sezioni spostate tengono il numero e lasciano un rimando, così «GUIDA-MAPPE §5.1.2» negli ADR vecchi resta vero; `docs/tools/` e `docs/audit/` restano dove sono (superficie pubblica e registri della CI). Misura: file in una forma sola 5/14 → 15/21; link e percorsi rotti 0 → 0; ancore verso file del repo 0 rotte su 20. Restano misti 6 file, elencati in `plans/esperimenti/documentazione-2026-11-10/MISURA-DIATAXIS.md`. ADR-0123 era conteso col thread del volume dei booklet: il coordinatore l'ha lasciato alla #371 (precedente del 10/11), il volume rinumera. Sourcery e Codex non hanno revisionato la PR (budget esaurito). La #381, su cui la #371 si è riallineata, è entrata con il merge ba8b8edf (base 66ce69b6), che MS-0068 non riporta.
- **Trovato nel repo:** `ADR-0123` → `plans/adr/ADR-0123-la-documentazione-segue-diataxis.md` · misura → `plans/esperimenti/documentazione-2026-11-10/MISURA-DIATAXIS.md` · traslochi → `docs/guides/README.md`
- **Solo qui:** la contesa del numero 0123 e come si è chiusa; lo SHA del merge della #381 (ba8b8edf); l'assenza di revisione dei bot sulla #371

### MS-0073 · 2026-11-12 · I limiti della d eufonica misurati seminando

- **Data:** 2026-11-12
- **PR:** #377
- **ADR:** ADR-0120 ADR-0037
- **Temi:** lingua prosa cancelli piattaforma
- **Origine:** addendum della riga del 2026-11-11 «Punto 4, seguito: i limiti della *d* eufonica» in `plans/CHANGELOG.md`
- **Testo:** PR #377, chiesta dal DM l'11/11 nel thread delle scelte dell'8/11: «si può vedere come superare i limiti, c'è un modo deterministico affidabile misurando il miglioramento?». Col corpus a zero contare i rilievi non distingue un rilevatore che legge da uno cieco, quindi la misura è un banco di semina: errori noti messi in una copia in memoria di ogni file di contenuto, e si conta quanti ne trova il rilevatore, posto per posto. Richiamo della regex 98,38% → 100% su 3.944 semi (692 file), rilievi nel codice 1 → 0, falsi 0; LanguageTool 84,25% perché svuota le tabelle. I 64 semi persi stavano in righe rientrate che per CommonMark sono prosa: `validate_lingua.py` ora legge 1.309 righe in più con tutti i suoi controlli. Card del DM del 12/11: «Parser CommonMark (markdown-it-py)» contro «Regola del repo, solo stdlib», scelta la prima (la consigliata); la regola stdlib resta come ripiego dichiarato. `<!-- sic -->` marca una citazione alla lettera. Il canale della d eufonica non cambia: testing fino al 2026-11-24. Sourcery e Codex non hanno revisionato la PR oltre la guida automatica (budget esaurito).
- **Trovato nel repo:** `ADR-0120` → `plans/adr/ADR-0120-la-d-eufonica-si-misura-con-una-regex-tarata-su-languagetool.md` (emendamento del 2026-11-11) · misura → `plans/esperimenti/d-eufonica-limiti-2026-11-11/RISULTATO.md` · libreria → `requirements.txt`, `LICENSES.md`
- **Solo qui:** il testo della domanda del DM e della card; il metodo riusabile (quando un cancello è a zero il miglioramento si misura seminando errori noti); le 184 righe che la regola stdlib classifica in altro modo stanno quasi tutte in un file d'archivio di ARC-08 coi recinti di codice rotti, non corretto

### MS-0074 · 2026-11-12 · ADR-0126 lotto 2: armi e danno

- **Data:** 2026-11-12
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole motore schede
- **Origine:** addendum della riga del 2026-11-12 «ADR-0126, lotto 2» in `plans/CHANGELOG.md`
- **Testo:** Lotto 2 del programma «regole senza omissioni». Capacità `creature.armi` (72 armi dell'SRD da «Table: Weapons», nomi italiani dal lessico, scala del dado per taglia) e `dmcore.danno`; `verifica_scheda` giudica dado, bonus e critico delle armi della tabella. Misura: errori messi apposta visti 0/364 → 336/364. Corrette 11 schede del Bestiario: 12 critici non scritti = numero della tabella; githyanki d'élite 1d10+3 → 1d10+4 (il più forte ricostruibile, ADR-0118). Non corretti e lasciati al DM 4 scarti di ARC-07: giavellotti di Zog'tar 1d8+13 (è il danno in Ira Superiore, Forza 36, e la riga non lo dice; fuori dall'Ira sarebbe +10), spadone delle guardie senza 19-20, martello runico di Balvar senza x3 nel master e nel Bestiario. Provato e tolto: correggere il master di ARC-07 e riallineare le copie con `componenti.py --includi` rompe le impronte dei manifest dei booklet (`ARC07-SERATA-RESURREZIONE-BOOKLET`, `ARC07-MILLE-ANNI-VOLUME`), `test_corredo` e `test_copertura_scene` (la copia di Balvar): chi lo farà deve rigenerare quelli nella stessa PR. Il PF1e eredita la capacità: le 72 armi del manuale base coincidono 72 su 72 (PSRD-Data). «Specialista del martello» (livello di sostituzione del chierico nano, Races of Stone) è una sorgente di +2 ai danni col martello da guerra, riscontrata nei dati PCGen: spiega Morlin e Ainin. Questioni aperte: attacchi naturali (lotto 5), armi dei manuali, danno aggiuntivo. Avviso mandato al thread della #370 per hobgoblin-captain-cr8 (critico aggiunto alla spada lunga).
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** il riscontro PCGen su «specialista del martello»; quali test si rompono toccando il master di ARC-07

### MS-0075 · 2026-11-12 · Grafo degli eventi, Prolog e RAG per «chi sa cosa»

- **Data:** 2026-11-12
- **PR:** #383
- **ADR:** ADR-0125
- **Temi:** coerenza storia regole
- **Origine:** voce scritta con la PR, per la riga del 2026-11-12 «Punti chiave, grafo degli eventi, Prolog e RAG» in `plans/CHANGELOG.md`
- **Testo:** Domanda del DM del 12/11: punti chiave nel tempo, grafo degli eventi, Prolog e RAG, tutto insieme e misurato. Laboratorio `plans/esperimenti/grafo-eventi-2026-11-12/`. Misura: i giorni si ricavano da state.yaml solo per 6 righe su 31 di §4; Python, SWI-Prolog e clingo danno violazioni identiche (29/29 sui mutanti, 6/6 su main), quindi il motore logico non entra; la regola ricorsiva trova 3 catene rotte in §4; il RAG (BM25 + e5-small + Qwen2.5-3B su CPU) recupera 8 parafrasi su 11 ma su main dà 0 rilievi veri su 23, quindi non entra; regole + RAG: parafrasi 0/11 → 5/11 con 42 rilievi in più. Correzione in corsa: la Cerimonia delle 100 Asce è al Day 21, non al 19; numeri invariati. Due correzioni alla #379 dalla revisione automatica arrivata dopo il merge: S1 dichiarata non verificabile se manca `giorno_arrivo`, `STATE` letto alla chiamata; gli altri 8 rilievi restano come limiti dichiarati nella PR. Decisione del DM (card): i giorni di §4 li propone il thread e li conferma lui riga per riga; T1 e T2 entrano in `coerenza_campagna --state` solo dopo. Aperti al DM: le 31 righe di `PROPOSTA-GIORNI-CHI-SA-COSA.md` e D1-D4 (D1: la lettera di Brenna usa «Custodi Eterni» ed è datata al Day 21 e al Giorno 22 nello stesso file); `ARC07-DEF-1-PIANO-TERRA-TERROS.md:69`; la prova del lettore con 7B e 12B via Ollama sulla RTX 4050 (6 GB di VRAM: il 12B non ci sta tutto).
- **Trovato nel repo:** `ADR-0125` → `plans/adr/` (file ADR-0125) · il laboratorio → `plans/esperimenti/grafo-eventi-2026-11-12/ESITO.md`
- **Solo qui:** il criterio per riprovare il lettore (90% di SÌ giusti, 5% col PNG sbagliato, 70% di precisione su main) accanto alla decisione di non adottarlo; l'errore di lettura dello stato della PR (controlli verdi ma PR in conflitto dopo #382 e #381)

### MS-0076 · 2026-11-12 · ADR-0126 lotto 3: incantatori

- **Data:** 2026-11-12
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole motore schede
- **Origine:** addendum della riga del 2026-11-12 «ADR-0126, lotto 3» in `plans/CHANGELOG.md`
- **Testo:** Lotto 3 del programma «regole senza omissioni». Capacità `creature.incantatori` (tabelle delle classi che lanciano, 3.5 dall'SRD e PF1e dal PRD, solo numeri) e `dmcore.magia`; `verifica_scheda` giudica incantesimi al giorno, conosciuti, livello massimo e CD. Errori messi apposta visti 0/616 → 376/616. Trovati 40 scarti veri in 9 file, non corretti: slot e incantesimi preparati sono scelta del DM. La tabella PF1e del bardo (card del 2026-11-09) esce come forma ibrida dichiarata, non come violazione.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** il costruttore non calcola gli incantesimi bonus (`dmcore.tabelle` dà solo la griglia della classe): gli slot delle schede sono scritti a mano, ed è lì che nascono gli scarti (ur-vrax ne ha uno in più a ogni livello); una riga della lista che nomina «incantesimi» (immunità agli incantesimi) veniva presa per intestazione

### MS-0077 · 2026-11-12 · genera_creatura dichiara le capacità che legge

- **Data:** 2026-11-12
- **PR:** #376
- **ADR:** ADR-0111, ADR-0121
- **Temi:** regole motore plugin
- **Origine:** addendum della riga del 2026-11-12 «Regole complete, coda del lotto 3» in `plans/CHANGELOG.md`
- **Testo:** Segnalazione del thread della documentazione (#371): `creature.talenti` era nel catalogo e nei due plugin, ma nessuno strumento la dichiarava, quindi la matrice di `dm.py sistemi` non la mostrava e il cancello non controllava che un sistema attivo la coprisse. Misura con una spia su `dmcore.sistemi.capacita` durante 288 generazioni: `genera_creatura` legge `creature.costruzione`, `creature.talenti` e `formule.regole`; su main ne dichiarava 1 su 3, dopo 3 su 3. `formule.regole` è uscita dalla misura, non dalla segnalazione. Nella prima versione della PR (10/11) le righe dei sistemi di prova erano mie; nel frattempo le hanno portate su main le PR di ADR-0126, quindi nel merge ho tenuto le loro. Effetto sul sistema di prova non d20 (`test_prova_non_d20`): `genera_creatura` passa da «nessuna capacità coperta» a «in parte», perché il d10 copre `formule.regole`, ma rifiuta comunque la generazione. Il censimento è aggiornato: nessuna 17 → 16. La CI della prima versione era rossa per la riga di CHANGELOG mancante e la PR è rimasta ferma due giorni senza che me ne accorgessi.
- **Trovato nel repo:** la misura → `plans/esperimenti/regole-complete-2026-11-10/misura_capacita_dichiarate.py`
- **Solo qui:** `creature.incantesimi` e `creature.statistiche_per_gs` sono dichiarate, ma la spia non le vede passare da `capacita()`, perché vengono lette per altra via. Va controllato prima di toglierle. Gli altri strumenti col blocco `sistema` non sono stati spiati.

### MS-0078 · 2026-11-12 · ADR-0126 lotto 3-bis: classi di prestigio

- **Data:** 2026-11-12
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole motore schede
- **Origine:** addendum della riga del 2026-11-12 «ADR-0126, lotto 3-bis» in `plans/CHANGELOG.md`
- **Testo:** Lotto 3-bis del programma «regole senza omissioni». Capacità `creature.prestigio` (requisiti d'ingresso delle classi di prestigio: 493 classi 3.5 dall'SRD e dai tag PRE di PCGen, 10 PF1e dal PRD, solo nomi e numeri) e `dmcore.prestigio`; `verifica_scheda` giudica bonus di attacco base delle altre classi, gradi, talenti, razza, allineamento e livello d'incantesimo contro il personaggio prima dell'ingresso. Requisiti tolti apposta dalle 8 schede vere: 30 su 30. Trovate e non corrette 3 violazioni in 2 schede del Bestiario (Blackguard 10 senza altre classi; Ladro 4 / Assassino 5 con Nascondersi 8).
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** il 40% dei requisiti 3.5 (877 su 2.178) non si riduce a un numero e resta solo contato: chi vuole chiuderli deve leggere i manuali, i tag di PCGen li danno come testo libero (PRETEXT) che non si copia; PCGen scrive la stessa classe in più libri (6 con requisiti diversi) e l'Assassino del suo file della Guida del DM è una variante, per questo le 15 classi dell'SRD si leggono dall'SRD; l'alias delle classi di `dmcore.talenti` è bidirezionale (cleric ↔ chierico), una mappa costruita passandoci dentro i nomi inglesi li rovescia in italiano; l'estrattore dei gradi del lotto 1 saltava Spellcraft per un titolo senza `<small>`, e nessun test lo vedeva perché nessuno contava le 38 abilità; `verifica_scheda` non può importare `dmcore.progressione` senza far salire il censimento A2 (le chiamate passano da `dmcore.prestigio.bab_di`).

### MS-0079 · 2026-11-12 · ADR-0126 lotto 4: numero dei talenti

- **Data:** 2026-11-12
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole motore schede
- **Origine:** addendum della riga del 2026-11-12 «ADR-0126, lotto 4» in `plans/CHANGELOG.md`
- **Testo:** Lotto 4 del programma «regole senza omissioni». `verifica_scheda.numero_talenti` (regola `numero.talenti`) conta i talenti scritti contro quelli che spettano per dadi vita, talenti bonus di classe e razza umana; fuori dal conto i concessi dalla classe e quelli dichiarati accanto al nome. Un talento in più o in meno messo apposta: 101 su 127. Quindici schede del Bestiario fuori conto, non corrette.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** il conto esisteva già nel generatore (`dmcore.talenti.quanti`) ma le chiavi dei talenti bonus 3.5 sono in italiano («guerriero») e la lettura delle schede dà le classi in inglese: senza alias il guerriero 8 risultava con 3 talenti invece di 8; `quanti` somma anche i «concessi» (Seguire Tracce, Scrivere Pergamene), che una scheda può scrivere o no, per questo il verificatore li toglie dai scritti invece di aggiungerli agli attesi; i dadi vita di `verifica_talenti.leggi` sono la somma dei gruppi letti e per un mostro con una classe possono essere solo i livelli (minotauro 6 + barbaro 1 dava 1): serve `dv_totali`; un nome sconosciuto alla lettura va contato come talento, altrimenti ogni scheda con un talento dei manuali esce dal controllo (al primo giro il banco dava 91 su 127 per questo).

### MS-0080 · 2026-11-12 · ADR-0126 lotto 4: effetti dei talenti sulle abilità

- **Data:** 2026-11-12
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole motore schede
- **Origine:** addendum della riga del 2026-11-12 «ADR-0126, lotto 4, seconda parte» in `plans/CHANGELOG.md`
- **Testo:** Seconda parte del lotto 4 del programma «regole senza omissioni». Nel conto dei gradi di `verifica_scheda` il bonus di un talento d'abilità va solo alle abilità che il talento nomina, col numero del plugin (`effetti_talenti.toml` di 3.5 e PF1e, capacità `creature.gradi`, generati da `estrai_effetti_talenti.py`). Banco `muta_effetti_talenti.py`: 44 errori su 44 visti, prima 0; 2 controlli in regola, nessuno segnato a torto; il Bestiario resta a 72 violazioni.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** degli effetti dei talenti sui numeri, pf, tiri salvezza, iniziativa, attacco e danno erano già nei conti (`conformita_statblocchi`, `dmcore.danno`): mancavano solo le abilità; il margine di prima scattava su una parola nel testo, e «furtivo» di «attacco furtivo» o «agile» in una frase bastavano; il banco tocca solo 10 schede perché solo quelle nominano un talento d'abilità; Autoipnosi manca da `gradi.toml` (l'estrattore dei gradi legge la tabella riassuntiva delle abilità, che non ha le psioniche fuori da Psicraft e Usare Oggetti Psionici).

### MS-0081 · 2026-11-12 · ADR-0126 lotto 3-ter: avanzamento d'incantatore delle classi di prestigio

- **Data:** 2026-11-12
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole motore schede
- **Origine:** addendum della riga del 2026-11-12 «ADR-0126, lotto 3-ter» in `plans/CHANGELOG.md`
- **Testo:** Lotto 3-ter del programma «regole senza omissioni». `prestigio.toml` (3.5 e PF1e) ha per ogni classe di prestigio i livelli che danno +1 livello d'incantatore a una classe che si aveva già (`avanza`); `dmcore.prestigio.avanzamento` fa il conto e `verifica_scheda` ha la regola `numero.incantesimi.livello_incantatore`. Banco `muta_avanzamento.py`: 12 liste troppo alte su 12 viste, prima 0; 6 controlli, nessuno segnato a torto; il Bestiario resta a 72 violazioni.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** in PCGen l'avanzamento è il tag `ADD:SPELLCASTER|Arcane/Divine/ANY` sulle righe di livello, con `REPEATLEVEL` per «ogni N livelli»; `BONUS:PCLEVEL` è un altro meccanismo (stirpi, psionici) e non si legge; l'assenza del tag non prova che la classe non avanzi, per questo una classe dei manuali senza `avanza` è un dubbio e una dell'SRD no; tre classi hanno avanzamenti diversi in due libri (`avanza = { diverge = true }`); il confronto fra i libri per `diverge` dei requisiti esclude `avanza`, altrimenti i requisiti di molte classi sarebbero diventati dubbi; senza livello scritto la lista di un «Chierico 3 / Loremaster 2» si giudicava da chierico di 3°.

### MS-0082 · 2026-11-12 · Cancello del riferimento dei plugin

- **Data:** 2026-11-12
- **PR:** —
- **ADR:** ADR-0111, ADR-0123
- **Temi:** documentazione plugin cancelli
- **Origine:** addendum della riga del 2026-11-12 «Cancello del riferimento dei plugin» in `plans/CHANGELOG.md`
- **Testo:** Il §5 di `docs/reference/RIFERIMENTO-PLUGIN-DI-SISTEMA.md` (una riga per capacità: chi la chiede, file dati di dnd35 e pf1e) è rimasto indietro quattro volte il 2026-11-12, dopo le #376, #386, #388 e #390, ed è stato riallineato a mano con le #387 e #389. `scripts/tests/test_riferimento_plugin.py` lo confronta con catalogo, manifest e `sistema.toml`: sulle teste di main dopo quelle quattro PR avrebbe dato 5, 6, 15 e 17 disaccordi, su 591dd927 zero. Costo: una PR di regole che cambia una capacità, chi la chiede o i suoi file è rossa finché non aggiorna la riga.
- **Trovato nel repo:** `scripts/tests/test_riferimento_plugin.py`
- **Solo qui:** `creature.armi` e `creature.incantatori` mancavano dal §5 già prima della #376 (lotti 2 e 3 di ADR-0126); le parentesi della colonna «chi la chiede» sono note e il test le ignora, quindi «— (la legge verifica_scheda)» conta come nessuno strumento.

### MS-0083 · 2026-11-13 · ADR-0129: il volume da stampa è PDF/UA-1

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0129, ADR-0032
- **Temi:** stampa booklet accessibilita document-ai
- **Origine:** addendum della riga del 2026-11-13 «ADR-0129: il volume da stampa è PDF/UA-1» in `plans/CHANGELOG.md`
- **Testo:** Prima tecnica della richiesta del DM del 2026-11-13 (document AI, explainable AI, AI generativa con standard e librerie standard di fatto, misurate). veraPDF 1.28.2 profilo ua1 sui 19 booklet: main 837876d6 0/19 conformi e 132 controlli falliti (7.3-1 ×78 figure senza alt, 7.4.2-1 ×9 titoli che saltano un livello, 5-1 ×19 e 7.1-10 ×19 di typst, 7.21.5-1 ×7 font); ramo 17/19 e 7. Misure di stampa identiche su tutte le chiavi, pagine identiche al pixel salvo 4 pagine d'indice in 3 booklet.
- **Trovato nel repo:** `plans/esperimenti/pdfua-2026-11-13/MISURE.md` · `plans/adr/ADR-0129-il-volume-da-stampa-e-pdf-ua-1.md`
- **Solo qui:** `hide(heading(...))` toglie il titolo dall'albero dei tag e typst con ua-1 si ferma su «the first heading must be of level 1»; la prima prova col titolo trasparente passava PDF/UA ma metteva il testo due volte (fuori_margine 0 → 6 nelle schede PG, titolo doppio nel testo estratto), quindi è stata scartata; la testatina interrogava ogni titolo di livello 1 e con il titolo visibile taggato mostrava il titolo grande in rosso, da qui `outlined: true` nella query. repo1.maven.org ha risposto 429, lo specchio repo.maven.apache.org no. I glifi su Unifont dipendono dai font della macchina: su un'altra il 7.21.5-1 può cambiare.
### MS-0084 · 2026-11-12 · Standard del volume, booklet di serata, taglia spazio e portata

- **Data:** 2026-11-12
- **PR:** #370
- **ADR:** ADR-0122 ADR-0128
- **Temi:** stampa booklet schede mappe
- **Origine:** voce scritta con la PR, per le righe STANDARD-STAMPA del 2026-11-10, 11 e 12 in `plans/CHANGELOG.md`
- **Testo:** Misura del volume S1-S5 contro *Burnt Offerings* e *Red Hand of Doom* (canale testing; linea di base 10 booklet del DM, 36 misure sotto soglia). Booklet di serata «La Notte e l'Alba» per `sezioni`: 158 → 122 pagine, 32 → 24 schede stampate una volta sola, con «Il foglio della serata» di una pagina (pagina unica di sessione, dal «Lazy DM») e una scheda da tavolo in testa alle Scene 6-11, scelta dal DM il 2026-11-12 fra i candidati della community. Taglia, spazio e portata in ogni scheda (ADR-0128, proposta; il DM ha voluto l'SRD su tutte e cinque le schede dubbie: la frusta non minaccia, il cavaliere senza lancia minaccia 1,5 m). Pedine delle mappe collegate alle schede: 41 su 110, taglie discordi 4 → 0. Tre misure di lettura in prova nate dai giri dei tre lettori (sigle morte, righe brevi incomplete, titoli rovinati). Corretto nell'esportatore il «;» che spariva dopo un grassetto in ogni PDF. Giudizio del developer sulle schede da tavolo: sotto gli AP, perché «In scena», «In tre righe» e scheda ripetevano le stesse cose; il DM ha chiesto la fusione il 2026-11-12 e nella serata i tre strati sono un blocco solo (il riassunto resta nel master fra i segni `senza-scheda` per gli altri volumi). Giro al cieco fra le due versioni: DM e redattore scelgono la fusa, il developer la sceglie al secondo giro, dopo la riga «Succede», e la tiene «peggio degli AP, di poco». CI rossa su 81403a04: `validate_corredo --stampa`, 98 righe sovrapposte in due volumi; causa, l'interazione fra la riga di taglia, spazio e portata (ADR-0128) e la CA spiegata del lotto 1-bis (#382), che hanno allungato la scheda di Skullcrusher Vecchio fin sopra una tabella messa a fondo pagina (difetto dei float di Typst 0.15); la correzione nel tema è generale: ogni tabella che scavalca sta in cima.
- **Trovato nel repo:** `ADR-0122` e `ADR-0128` → `plans/adr/` · `plans/esperimenti/standard-volume-2026-11-10/` · `plans/esperimenti/taglia-portata-2026-11-10/` · `docs/audit/stampa-booklet.json` · `docs/audit/mappe-schede.json`
- **Solo qui:** l'ADR di taglia e portata è nato 0123, poi 0127, infine 0128, perché i primi due numeri erano di altre PR; le 17 misure di prosa della community restano non adottate; ripetizioni mai misurate, contate il 2026-11-13 su domanda del DM (passi di almeno 8 parole identiche, dalla seconda volta): serata 12,3% delle parole contro l'1,2% di *Burnt Offerings* e lo 0,5% dell'estratto di *Red Hand of Doom*; circa 3.700 parole sono le copie volute in appendice, circa 5.200 stanno nel corpo e non sono toccate qui; aperti 69 pedine senza scheda, pedine non in scala nel disegno, 4 card del DM sul volume (VOL-3)

### MS-0085 · 2026-11-12 · ADR-0126 coda del lotto 3: i fatti di una scheda in JSON

- **Data:** 2026-11-12
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole motore schede coerenza
- **Origine:** addendum della riga del 2026-11-12 «ADR-0126, coda del lotto 3» in `plans/CHANGELOG.md`
- **Testo:** `verifica_scheda --fatti` (funzione `fatti`) stampa per file talenti, incantesimi e capacità speciali con nome canonico e riga, più inizio e fine di ogni «Tattiche» e «Descrizione». L'aveva chiesto il thread della coerenza della storia per la regola S8 (prosa contro scheda). Non giudica ed esce 0. Misura su `Bestiario 0*/`: 186 file, 486/508 talenti canonici, 626/688 incantesimi canonici, 214 capacità speciali, 265 «Tattiche» in 111 file, 120 «Descrizione».
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** la prima stesura passava dal lettore delle schede e su un file che quello non riconosce non dava nulla, quindi ora la riga «Talenti» si legge anche da sola. Fuori da una scheda riconosciuta «1° …» è spesso un elenco di prosa (stanze, passi): la riga conta solo se almeno un nome è un incantesimo noto, e così 14 falsi sono usciti. Una sezione aperta da un titolo si chiude al titolo dopo, perché dentro ha i suoi grassetti («**Round 1**»); una aperta da un'etichetta in grassetto si chiude all'etichetta dopo. Limiti: solo la prima riga «Talenti» del file; 62 incantesimi in italiano senza canonico perché il dizionario dell'SRD non li ha; capacità speciali solo con la sigla fra parentesi.

### MS-0086 · 2026-11-13 · Le ripetizioni dei booklet hanno una misura

- **Data:** 2026-11-13
- **PR:** #395
- **ADR:** ADR-0122 ADR-0099
- **Temi:** stampa booklet misure
- **Origine:** voce scritta con la PR, per la riga STANDARD-STAMPA del 2026-11-13 in `plans/CHANGELOG.md`
- **Testo:** Il DM, vista la serata di 125 pagine, ha chiesto se c'erano ripetizioni non misurate. C'erano. `misura_stampa.parole_ripetute` conta le parole che stanno in un passo di almeno 8 parole già stampato prima (w-shingling, lo standard di fatto per i quasi-duplicati), dalla seconda volta e senza le testatine. È in prova: avvisa e non ferma. Serata «La Notte e l'Alba» 12,3% (8.842 parole su 72.041) contro l'1,2% di *Burnt Offerings* e lo 0,5% dell'estratto di *Red Hand of Doom*. Nella serata 3.665 parole sono le copie in appendice (schede e mappe), 5.177 stanno nel corpo: le schede d'entrata «in breve» ristampate a ogni scena, pezzi delle schede del capitolo II ridetti nelle scene, la legenda delle mappe a ogni mappa. Dei 20 booklet tre superano il 10%, tredici stanno sopra il 5%.
- **Trovato nel repo:** `scripts/misura_stampa.py` · `docs/audit/stampa-booklet.json` · `docs/audit/volume-booklet.json` (riferimenti S6) · `scripts/tests/test_misure_in_prova.py`
- **Solo qui:** nessuna soglia, perché una parte delle copie è voluta e il confronto con gli AP non è alla pari (gli AP non ristampano le schede in appendice); tolte tutte le copie del corpo la serata scenderebbe a circa il 5%, non all'1%; i passi sotto le 22 parole pesano 3.906 parole su 5.177 del corpo e sono in gran parte righe di statistiche, non prosa; quali copie togliere lo decide il DM.
### MS-0087 · 2026-11-13 · S8: le tattiche di una scheda contro la scheda

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0125
- **Temi:** coerenza storia schede regole
- **Origine:** voce scritta con la PR, per la riga del 2026-11-13 «ADR-0125, aggiunta S8» in `plans/CHANGELOG.md`
- **Testo:** `coerenza_campagna.py fatti --tattiche` (funzione `verifica_tattiche`) legge i fatti di `verifica_scheda --fatti` e segnala un incantesimo in corsivo o un talento che le «Tattiche» nominano e la scheda non ha, né fra i fatti né scritto altrove nel file. Canale testing, esce 0. Su main 0 violazioni su 220 menzioni in 60 schede. Mutanti (`muta_tattiche.py`, 569): 181 su 183 e 178 su 180 nelle due famiglie da vedere, 0 falsi su 26 controlli; incantesimo senza corsivo 0 su 60, talento di una parola in minuscolo 0 su 60, talento di più parole in minuscolo 60 su 60.
- **Trovato nel repo:** `ADR-0125` → `plans/adr/` (file ADR-0125, «Aggiunta del 2026-11-13») · il banco → `plans/esperimenti/coerenza-storia-2026-11-12/ESITO.md`
- **Solo qui:** la prima corsa dava 9 violazioni, tutte false: `lessico_regole.norma` toglie il contenuto delle parentesi, dove una scheda scrive incantesimi preparati e pozioni (5), quindi il confronto «scritto altrove» usa un normalizzatore suo; «la Corona» risolta come talento dei manuali (una parola sola conta solo se il talento è nei dati del sistema); una nota di correzione del DM dentro le Tattiche (le righe «>» non si leggono); «contro *polvere luccicante*» (incantesimo di chi attacca); l'incantesimo del padrone passato con condividere incantesimi. Leggere gli incantesimi senza corsivo è stato provato e scartato: 32 menzioni in più su main, 2 segnalazioni e tutte e due false. Sui master degli archi 4 segnalazioni su 4 false, perché la tattica rimanda a una scheda in un altro file: S8 legge solo il Bestiario.

### MS-0088 · 2026-11-13 · ADR-0126 lotto 5: la creatura base

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole motore schede
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 5, prima parte» in `plans/CHANGELOG.md`
- **Testo:** Prima parte del lotto 5 del programma «regole senza omissioni». Capacità `creature.base` nel plugin 3.5: 409 creature dell'SRD con dadi vita razziali, armatura naturale, attacchi naturali col dado, modificatore di livello; più la tabella dei draghi veri per taglia. `verifica_scheda` confronta dadi vita razziali, armatura naturale e dado degli attacchi naturali con la base, solo dove la scheda la dichiara nella fonte. Bestiario: non verificabili 321 → 297, violazioni 72 → 73.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** i blocchi dell'SRD in cache sono tabelle HTML dentro il Markdown: con più colonne i nomi stanno nella prima riga, con una creatura sola la tabella parte dal tipo e il nome è il titolo sopra (senza questo caso se ne leggevano 157 su 409). Dedurre la base dal sottotipo dava due violazioni false sul flind, che è «umanoide (gnoll)». Il colore del drago deve stare accanto alla parola «drago»: la lucertola del tuono «progenie azzurra di Tiamat (drago)» è di tipo drago ma non è un drago vero, e con il colore sciolto veniva presa. Le righe `tipo:` in italiano («Drago Enorme … drago nero») vanno lette prima di tradurre il tipo, altrimenti «drago nero» diventa «dragon nero» e non si riconosce. Nel conto del danno il nome `base` era già una variabile locale: il parametro si chiama `creatura`. Il test `test_nessuna_capacita_pf1e_resta_non_supportata` non lascia dichiarare `non_supportato` in PF1e, e i sistemi di prova in `scripts/tests/dati/` devono coprire ogni capacità del catalogo: per questo i dati PF1e (1138 creature dei Bestiary 1-4 di PSRD-Data) sono entrati nella stessa PR.
### MS-0089 · 2026-11-13 · ADR-0130: le emoji del volume vengono dal repo

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0130 ADR-0129 ADR-0020
- **Temi:** stampa booklet font accessibilita document-ai
- **Origine:** addendum della riga del 2026-11-13 «ADR-0130: le emoji del volume da stampa vengono dal repo» in `plans/CHANGELOG.md`
- **Testo:** Seconda tecnica della richiesta del DM del 2026-11-13. Il DM vuole le emoji a colori, con i font nel repo se la licenza è compatibile e lo standard di fatto della community, senza problemi per typst e veraPDF. Su main 80 caratteri (3.172 occorrenze) uscivano da font di sistema: Noto Color Emoji, FreeSans, Inter, Unifont. Unifont lasciava non conformi il Palio e Terros (7 controlli 7.21.5-1). Con Noto Color Emoji 2.051 CBDT nel repo e l'export coi soli font del repo: veraPDF 18/20 → 20/20, 7 → 0; pagine uguali (985); 83 pagine con ► e ⬦ in un altro tratto.
- **Trovato nel repo:** `plans/adr/ADR-0130-le-emoji-del-volume-vengono-dal-repo.md` · `plans/esperimenti/glifi-2026-11-13/MISURE.md` · `scripts/fonts/README.md`
- **Solo qui:** la prima scelta era il Noto vettoriale COLRv1 di Google Fonts (5 MB, tolta la tabella SVG): typst non disegna i glifi COLR dentro le immagini SVG, «⏳» spariva dalla legenda della Sala della Forgia e due booklet uscivano non conformi. Noto Sans Symbols 2 intero cambiava le etichette SVG del Palio («DC 2 4» con le cifre di un altro font); ridotto ai soli simboli rompeva «⏳»; i font interni di typst coprono già i 13 simboli. GitHub raw di googlefonts/noto-emoji e jsDelivr sono bloccati nel container: il CBDT viene da deb.debian.org (sha256 del .deb 03141cd5…). Una corsa che esporta e misura i 20 booklet in un solo comando fa uccidere il worker per memoria (exit 137): va in uno script in background. Twemoji Mozilla passa veraPDF ma cambia lo stile; OpenMoji è CC BY-SA, incompatibile; le icone (game-icons.net, Material) sono una scelta di stile al DM, con card aperta (consigliata: Noto a colori).

### MS-0090 · 2026-11-13 · Serata più corta con la pagina fitta, e le copie rimesse

- **Data:** 2026-11-13
- **PR:** #399
- **ADR:** ADR-0122
- **Temi:** stampa booklet misure
- **Origine:** voce scritta con la PR, per la seconda riga STANDARD-STAMPA del 2026-11-13 in `plans/CHANGELOG.md`
- **Testo:** Alla card «quali copie togliere» il DM ha risposto: pagine più fitte, schede d'entrata ripetute e copie del corpo, insieme. Fatte tutte e tre, il DM ha visto il PDF e ha bocciato le copie una volta sola: le schede di PNG, mostri, villain e gregari si leggono peggio accorpate. Resta una chiave di manifest, `"pagina": "fitta"`: A4 con corpo 9,6 pt (quello dell'A5), interlinea 0,56em, margini alto e basso più stretti, spenta per tutti gli altri booklet. Serata «La Notte e l'Alba»: 125 → 114 pagine, 561 → 614 parole per pagina, schede e righe per il tavolo in ogni scena come prima.
- **Trovato nel repo:** `scripts/typst/tema-rumblingstone.typ` (`pagina`) · `scripts/schemas/booklet_manifest.schema.json` · `docs/audit/stampa-booklet.json` · `ADR-0122` → `plans/adr/`
- **Solo qui:** la chiave `"copie": "una-volta"` (riga per il tavolo e scheda in breve una volta sola, poi un rimando con le pagine) è stata scritta, misurata e tolta nella stessa PR: non accorciava (113 pagine con e senza, a margini laterali stretti) e portava i numeri di Zog'tar da 5 a 13 pagine di distanza in mediana. Non riproporla senza una misura diversa. I margini laterali stretti (1,8 e 1,3 cm) facevano 113 pagine ma `misura_stampa` contava 2.337 righe fuori margine e 12 emoji delle mappe salivano sopra i 2 cm, a 72 dpi: tornati a 2,0 e 1,5 cm come gli altri booklet, al prezzo di una pagina. La stima di «circa 100 pagine» data sulla card era sbagliata: tabelle, schede, mappe e scene a pagina nuova non si stringono con il corpo. La misura delle ripetizioni contava come copia la testatina dei capitoli corti: corretta, i riferimenti scendono a 1,1% e 0,4%. Nel corpo della serata restano circa 1.100 parole di frasi dette due volte fra regia e scene, non toccate, e due schede intere di Skullcrusher (capitolo II e capitolo X).


### MS-0091 · 2026-11-13 · Decisioni del DM sulle schede: tagli, prestigio, talenti, Zog'tar

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede canone
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, decisioni del DM sulle card del 13/11» in `plans/CHANGELOG.md`
- **Testo:** Il DM ha risposto a otto card nel thread delle regole. Quattro risposte si scrivono subito: i giavellotti di Zog'tar fanno 1d8+13 in Ira e 1d8+10 fuori; spadone delle guardie 19-20 e martello di Balvar x3; lo gnoll guerriero ha armatura naturale +1 come l'SRD; la pattuglia si dà il fiancheggiamento ai due lati opposti del PG. Le altre quattro chiedevano una proposta, approvata lo stesso giorno: tagli degli incantesimi di quattro incantatori, drow Ladro 5 / Assassino 4, cavaliere di Abbathor ex-Paladino 7 / Guardia Nera 3, Dovil a livello d'incantatore 6 con Scrivere Pergamene al posto di Incidere Rune, Rurik con la pietra ioun arancione, tredici schede riportate al numero di talenti dei loro dadi vita. Misura: violazioni 73 → 30, non verificabili 297 → 293; nel Bestiario restano due sole violazioni (Salvatore).
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** le decisioni erano in elenco nel testo del thread dal 12/11 e il DM non le trovava: sono arrivate tutte in due minuti appena messe su card con scheda, file e riga. Le «sette violazioni vecchie» di talenti, rigiudicate dopo i lotti 3-5, erano due. Una riga del master ripetuta nei booklet si corregge nel master e poi si rigenerano i `.hb.md` con `build_booklet_html.py <manifest> --format hb` (il test dei manifest lo chiede); gli HTML dei booklet in repo erano già indietro rispetto ai manifest e non sono stati rigenerati qui. Cambiare la CA di una scheda del Bestiario cambia la fixture `impronta-creature.json` (`impronta_creature.py --scrivi`); cambiarne il titolo cambia l'id nel catalogo (`build_monster_catalog.py`). La prima card su Abbathor (Guerriero 6 / Guardia Nera 4) era sbagliata: Nascondersi è incrociata e i 5 gradi arrivano al 7° livello. Due schede «fuori conto» erano un errore del controllo (mezzelfi letti come umani). Il controllo cerca i nomi dei talenti in tutto il testo: una nota che nomina il talento tolto lo fa ricontare (lotta dell'ogre), quindi le note lo descrivono senza nominarlo. Persuasive nell'SRD dà Raggirare e Intimidire, non Diplomazia. Koth aveva una nota «si tengono tutti e cinque, come chiede il DM»: la superano le card del 13/11.

### MS-0092 · 2026-11-13 · ADR-0126 lotto 5: il grado di sfida

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede plugin
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 5 seconda parte: il grado di sfida» in `plans/CHANGELOG.md`
- **Testo:** Il grado di sfida scritto nel blocco si confronta con quello che danno i livelli di classe, la razza e la creatura base. Classe da PG pari al livello e classe da PNG un grado sotto nel 3.5, uno e due sotto in PF1e; drow, duergar e svirfneblin +1 con classi da PG; goblin −2 e coboldo −3 con classi da PNG; creatura base con livelli dentro la forbice fra tutti non associati e tutti associati. Misura: violazioni 30 → 33, non verificabili 293 → 371. Tre scarti veri vanno al DM: due duergar con classi da PG scritti senza il +1 e il goblin combattente a 1/2 invece di 1/3.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** la lettura della scheda rende «1/2» come 1, quindi il grado si legge dalla riga del blocco. I dadi di una classe che la lettura non conosce finiscono al tipo come dadi razziali: si tolgono quando il tipo nomina la classe. «Mezzorco» conteneva «mezzo» e passava per un modello: le parole dei modelli sono espressioni regolari. La regola generale di PG e PNG del 3.5 non è nell'SRD ma nel manuale del DM: nel repo solo i numeri, e i blocchi dell'SRD la confermano. Githyanki e orog hanno la loro riga in manuali fuori dai dati e restano dubbi.


### MS-0093 · 2026-11-13 · Pagina fitta: le schede tengono l'interlinea di prima

- **Data:** 2026-11-13
- **PR:** #402
- **ADR:** ADR-0122
- **Temi:** stampa booklet schede
- **Origine:** voce scritta con la PR, per la terza riga STANDARD-STAMPA del 2026-11-13 in `plans/CHANGELOG.md`
- **Testo:** Il DM ha letto la serata a 114 pagine e ha trovato le schede di PG, PNG, villain e mostri «tutte attaccate». Confronto con i PDF del 2 e del 12 novembre: corpo delle schede uguale (8,8 pt), ma l'interlinea della pagina fitta (0,56em) entrava anche nelle schede, e il passo di riga scendeva da 11,2 a 10,6 pt in appendice e da 12,0 a 11,1 pt nelle schede in breve dei capitoli. Ora `statblocco` fissa l'interlinea del tema: 11,2 e 11,7 pt. La serata resta di 114 pagine.
- **Trovato nel repo:** `scripts/typst/tema-rumblingstone.typ` (`statblocco`) · `docs/audit/stampa-booklet.json` · `ADR-0122` → `plans/adr/`
- **Solo qui:** rispetto al 2 novembre le schede portano anche più righe (taglia, spazio e portata di ADR-0128, i sensi interi): quella parte di «attaccato» non viene dall'interlinea e resta. Le schede in breve nei capitoli non hanno le fasce Difesa/Attacco dell'appendice: proposto al DM, non fatto. Confronti in `/mnt/project-files/serata-corta-2026-11-13/`.

### MS-0094 · 2026-11-13 · ADR-0126 lotto 5: i fatti scheda per scheda

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede coerenza
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 5 terza parte: i fatti scheda per scheda» in `plans/CHANGELOG.md`
- **Testo:** `verifica_scheda --fatti` dà una voce per scheda del file (`blocchi`: titolo, righe di inizio e fine, talenti) e la regola S8 giudica le «Tattiche» di ogni scheda contro quella scheda anche nei file che ne hanno più d'una. Misura: talenti dati da `--fatti` 500 → 748 su 595 file; S8 sul Bestiario 60 → 65 schede lette e 220 → 246 menzioni, sempre 0 violazioni.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** i cinque file del Bestiario saltati per «più schede» non avevano due schede: la seconda riga «Talenti» era una nota citata con «>» o la stessa scheda riscritta più sotto, e tre file con il recinto senza talenti li hanno in prosa sotto un altro titolo. Aggiungere una chiave a ogni voce dei fatti rompeva i test che confrontano le voci intere: il blocco di una riga si chiede a `blocco_di`. Provata sugli archi, S8 dà 33 segnalazioni fra negazioni («senza Estrazione Rapida») e booklet generati: lì serve una lettura una per una prima di farne una misura.

### MS-0095 · 2026-11-13 · ADR-0126 lotto 6: le abilità di classe

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede abilità
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 6 prima parte: le abilità di classe e il margine dei gradi» in `plans/CHANGELOG.md`
- **Testo:** il plugin 3.5 sa quali abilità sono di quale classe (38 classi), quali aggiungono cinque domini, quali danno sinergia e i bonus delle sette razze dell'SRD. `verifica_scheda` giudica le abilità fuori classe (massimo dimezzato, costo doppio, regola `gradi.massimo.fuori_classe`) e conta il margine vero per le sette razze. Misura: violazioni 33 → 33; banco, ogni abilità +4 da sola 10 → 16 su 162.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** il guadagno è piccolo perché 86 schede su 130 non scrivono la riga delle abilità coi numeri e fra le 18 con soltanto classi note solo 6 sono di una razza dell'SRD. Nell'SRD l'elenco delle abilità di classe del mago finisce con un rimando al capitolo 4 e quello dell'arciere arcano ha un punto in mezzo: l'elenco si taglia su virgole e punti, non sulla fine della frase. Le sinergie non stanno solo nella riga «Synergy»: si prendono da ogni frase «If you have 5 or more ranks in».

### MS-0096 · 2026-11-13 · ADR-0126 lotto 6: la penalità di armatura alla prova

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede abilità
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 6 seconda parte: la penalità di armatura alla prova» in `plans/CHANGELOG.md`
- **Testo:** il plugin 3.5 ha la penalità alla prova di dodici armature e sei scudi dell'SRD e le nove abilità che la subiscono (Nuotare doppia). `verifica_scheda` legge armatura e scudo dalla riga della CA e aggiunge la penalità ai gradi minimi, contando ogni oggetto perfetto. Misura: violazioni 33 → 33; 62 schede con un'armatura riconosciuta; banco, tutte +6 18 → 20 su 32.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** nella tabella dell'SRD lo scudo torre è «+4» con una nota in apice «3»: tolti i tag diventava +43, e gli apici vanno tolti prima. L'armatura si riconosce dal bonus e dalla Des massima, che nella tabella non si ripetono mai, così i nomi italiani del plugin non servono una seconda volta. I gradi dichiarati fra parentesi li scrive abilità per abilità una scheda sola del Bestiario: non se ne fa una regola.

### MS-0097 · 2026-11-13 · Pagina fitta abbandonata: la serata torna com'era il 12 novembre

- **Data:** 2026-11-13
- **PR:** #406
- **ADR:** ADR-0122
- **Temi:** stampa booklet schede
- **Origine:** voce scritta con la PR, per la quarta riga STANDARD-STAMPA del 2026-11-13 in `plans/CHANGELOG.md`
- **Testo:** Dopo aver visto la serata a 114 pagine con le schede rimesse larghe (MS-0093), il DM ha scelto la versione del 12 novembre e ha chiesto di abbandonare la versione stretta per tutto. La chiave `"pagina": "fitta"` è tolta da manifest, tema, esportatore, schema e validatore: nessun booklet la usava oltre alla serata. La serata torna a 125 pagine, corpo 10,2 pt, con lo stesso passo di riga delle schede del 12 novembre.
- **Trovato nel repo:** `scripts/typst/tema-rumblingstone.typ` · `docs/audit/stampa-booklet.json` · `ADR-0122` → `plans/adr/`
- **Solo qui:** in un giorno il DM ha bocciato tre modi di accorciare la serata: le schede accorpate (MS-0090), le schede strette (MS-0093) e la pagina fitta intera (questa voce). La lunghezza della serata non si riduce stringendo la pagina né togliendo le schede dalle scene: non riproporlo. Resta di quella giornata solo la misura delle ripetizioni corretta sulle testatine. Il testo della serata non è identico a quello del 12 novembre: porta le correzioni alle schede entrate dopo (#400 e seguenti).

### MS-0098 · 2026-11-13 · ADR-0126 lotto 7: la velocità a terra

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 7 prima parte: la velocità a terra» in `plans/CHANGELOG.md`
- **Testo:** il plugin 3.5 ha `movimento.toml` (velocità delle sette razze dell'SRD, categoria delle armature, velocità ridotta, movimento veloce di barbaro e monaco) e `verifica_scheda` ha la verifica `velocita`: la velocità scritta di chi ha soltanto livelli di classe deve tornare con razza, classe e armatura. Misura: violazioni 33 → 33; 18 schede giudicate su 100; banco 15 su 18 per verso, su main 0.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** la prima lista delle parole che rendono dubbia una velocità aveva «mount» e «carico», e quasi ogni scheda dei nani ha «mountain» nell'ambiente: 8 mutazioni su 18 sfuggivano per questo. La lista ora ha solo gli oggetti e gli incantesimi che cambiano davvero la velocità, più la nota scritta nella riga stessa. Un umano con dadi vita razziali non esiste: la prova «chi ha dadi vita razziali» non si scrive su una scheda di prova umana.

### MS-0099 · 2026-11-13 · ADR-0126 lotto 7: resistenza agli incantesimi e riduzione del danno

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 7 seconda parte: resistenza agli incantesimi e riduzione del danno» in `plans/CHANGELOG.md`
- **Testo:** il plugin 3.5 ha `difese.toml` (sei razze dell'SRD con la RI «N + livelli di classe», monaco, RD del barbaro per livello) e `verifica_scheda` ha la verifica `difese` (regole `numero.RI`, `numero.RD`). Misura: violazioni 33 → 34 (RI del Collezionista, 27 contro 38, in attesa del DM); 8 RI giudicate su 26 e 3 RD su 4; banco 6 su 6 e 3 su 3 per verso, su main 0.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** i livelli di classe letti dal nome delle classi non bastano: il Trickster Arcano della drow non veniva letto e la RI attesa veniva 19 invece di 21. Si contano i dadi vita oltre quelli della razza. Il nome della razza nel titolo non basta: «Cultista Rakshasa» è un umanoide, e conta il tipo della scheda. I sensi delle razze non si sono fatti perché `conformita_statblocchi` li controlla già.

### MS-0100 · 2026-11-13 · ADR-0126 lotto 7: le immunità del tipo

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 7 terza parte: le immunità del tipo» in `plans/CHANGELOG.md`
- **Testo:** `difese.toml` ha `[difese.immunita]` (le immunità che l'SRD dà a sette tipi di creatura) e la verifica `difese` ha la regola `tratti.immunita`: la scheda scrive «tratti dei …» o tutte le immunità del tipo. Misura: violazioni 34 → 37 (deathlock, leone spettrale e leone crudele scheletrico senza i tratti dei non morti, in attesa del DM); 18 schede in regola su 21; banco 16 su 18, su main 0.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** i miconidi scrivono «tratti vegetali», senza «dei»: la formula deve accettarla, altrimenti quattro schede giuste diventano violazioni. La parola «mente» da sola combacia con gli avverbi («completamente»): va cercata come parola intera. La scheda di prova dei test ha Int 10, quindi un costrutto di prova non è mai «senza mente» se non glielo si toglie.

### MS-0101 · 2026-11-13 · ADR-0126 lotto 7: i linguaggi automatici

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 7 quarta parte: i linguaggi automatici» in `plans/CHANGELOG.md`
- **Testo:** il plugin 3.5 ha `linguaggi.toml` (linguaggi automatici delle sette razze dell'SRD, Druidico del druido) e `verifica_scheda` ha la verifica `linguaggi` (regola `tratti.linguaggi`), solo per chi scrive la riga dei linguaggi. Misura: violazioni 37 → 37; 7 schede giudicate su 24; banco 13 su 13, su main 0. Il lotto 7 è chiuso.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** il numero dei linguaggi non si conta di proposito. Le schede dei PNG hanno linguaggi regionali (Chondathan, Illuskan, Shaaran) che l'SRD non conosce e non scrivono i gradi di Parlare Linguaggi: un conto darebbe violazioni che sono scelte del DM. Chi non scrive la riga non è una violazione, perché il blocco 3.5 non la prevede.

### MS-0102 · 2026-11-13 · ADR-0126 lotto 8: il valore dell'equipaggiamento

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 8 prima parte: il valore dell'equipaggiamento» in `plans/CHANGELOG.md`
- **Testo:** il plugin 3.5 ha `oggetti.toml` (623 prezzi degli oggetti magici dell'SRD, prezzo del potenziamento, valore dell'equipaggiamento di un PNG per livello) e `verifica_scheda` ha la verifica `ricchezza` (regola `equipaggiamento.valore`). Misura: violazioni 37 → 37, non verificabili 372 → 374; banco 24 violazioni e 88 non verificabili su 112, su main 0.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** la tabella dei PNG (DMG 3.5, Tabella 4-23) non è nell'SRD: nel repo stanno solo i venti numeri, riscontrati su realmshelps.net. La somma è un minimo di proposito: si contano solo gli oggetti dal prezzo certo, così una violazione è sicura e sotto la tabella non si dice niente. 88 schede su 112 del banco restano non verificabili perché il plugin non ha il modificatore di livello delle razze dei mostri: è il resto del lotto 5 e alzerebbe questa misura più di ogni altra aggiunta.

### MS-0103 · 2026-11-13 · ADR-0126 lotto 5: il modificatore di livello delle razze senza dadi vita

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 5 quarta parte: il modificatore di livello delle razze senza dadi vita razziali» in `plans/CHANGELOG.md`
- **Testo:** il plugin 3.5 ha `mdl.toml` (dieci razze che l'SRD presenta come combattenti di 1° livello, con il loro modificatore di livello) e la verifica `ricchezza` lo usa per il livello effettivo. Misura: violazioni 37 → 37, non verificabili 374 → 374; banco della ricchezza: violazioni 24 → 57, non verificabili 88 → 55.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** `creature_base.toml` non ha queste razze perché nell'SRD non hanno dadi vita razziali: il loro blocco è un combattente di 1° livello, ma la riga «Level Adjustment» c'è. Una scheda che nomina un modello (mezzo-drago, vampiro, immondo) non si giudica: il modello cambia il modificatore e il plugin non ha ancora i modelli.

### MS-0104 · 2026-11-13 · ADR-0126 lotto 8: capacità speciali, pozioni, pergamene, bacchette

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 8 seconda parte: capacità speciali, pozioni, pergamene, bacchette» in `plans/CHANGELOG.md`
- **Testo:** `oggetti.toml` ha le capacità speciali di armi, armature e scudi e i prezzi delle pergamene; la verifica `ricchezza` legge i nomi italiani dal lessico e conta capacità speciali, pozioni, pergamene e bacchette con le cariche scritte. Misura: violazioni 37 → 37; valore riconosciuto nel Bestiario 224.000 → 267.830 mo; banco, seconda prova: 41 → 57 su 125.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** la prima versione cercava le capacità in tutto il tratto fino alla virgola e prendeva «Cerchio Sacro» (il nome di un arco di Lythiel) per la capacità «sacra»: 2.000 mo diventavano 18.000. Per questo una capacità conta solo se sta attaccata al nome dell'arma o al bonus. La somma deve restare un minimo sicuro: nel dubbio non si conta.
### MS-0105 · 2026-11-13 · ADR-0126: RI del Collezionista 38 e tratti dei non morti a tre schede

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, due decisioni del DM sulle card delle difese» in `plans/CHANGELOG.md`
- **Testo:** il DM ha scelto sulle card la RI 38 dell'SRD per il Collezionista (27 del rakshasa + 11 livelli di classe) e la riga «Tratti dei non morti» per deathlock, leone spettrale e leone crudele scheletrico. Le quattro schede sono corrette e `IN_ATTESA` di `test_difese.py` è vuoto. Misura: violazioni 37 → 33.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** le due card erano rimaste aperte dalle PR dei lotti 7 seconda e terza parte; le schede non si toccano senza la risposta del DM, quindi fino a oggi stavano nell'elenco in attesa. La RI 27 era quella del rakshasa base: la regola dell'SRD la alza di uno per livello di classe.
### MS-0106 · 2026-11-13 · ADR-0131: il volume da stampa è anche PDF/A-2a

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0131 ADR-0129 ADR-0130
- **Temi:** stampa booklet archiviazione document-ai
- **Origine:** addendum della riga del 2026-11-13 «ADR-0131: il volume da stampa è anche PDF/A-2a» in `plans/CHANGELOG.md`
- **Testo:** Terza tecnica della richiesta del DM del 2026-11-13 («continua con le prossime che mancano e che misurate migliorano»). `export_booklet_typst` chiede a typst PDF/A-2a insieme a PDF/UA-1. veraPDF 1.28.2 sui 20 booklet, main 683480af: PDF/A-2a 0/20 e 544 controlli falliti (6.2.10-2 ×484 trasparenza senza intento d'uscita, 6.6.4-1 ×20 e 6.6.2.3.1 ×40 metadati XMP); ramo 20/20 e 0. PDF/UA-1 resta 20/20, pagine 985 = 985, testo estratto identico, peso 75,2 → 75,3 MB.
- **Trovato nel repo:** `plans/adr/ADR-0131-il-volume-da-stampa-e-anche-pdf-a-2a.md` · `plans/esperimenti/pdfa-2026-11-13/MISURE.md` · `scripts/tests/test_pdfua.py` (TestPdfA)
- **Solo qui:** typst 0.15.2 rifiuta PDF/A-4 con PDF/UA-1 («mutually incompatible»: A-4 vuole PDF 2.0, UA-1 PDF 1.7); A-2a, 2b, 2u e 3a si combinano. 86 pagine su 985 hanno pixel diversi a 40 dpi, al più 3 livelli su 255 e in media 1: è l'intento d'uscita sRGB, non si vede. Ghostscript `-dPDFA` scartato senza misura perché rifà il PDF e perde i tag. La voce è nata MS-0105 ed è diventata MS-0106 al riallineo, dopo la #414 delle regole.

### MS-0107 · 2026-11-13 · ADR-0091: le schede nell'ordine di Burnt Offerings

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0091
- **Temi:** schede stampa booklet
- **Origine:** riga del 2026-11-13 «ADR-0091, aggiornamento: le schede nell'ordine delle AP PF1e» in `plans/CHANGELOG.md`
- **Testo:** Jfs, 2026-11-13 20:21: confrontare le schede con Pathfinder 1e e Red Hand of Doom, «secondo me si è perso qualcosa, manca ad esempio la voce dell'equipaggiamento». Misura su 205 schede: Equipaggiamento 46 (34 delle 90 con livelli di classe), Linguaggi 26, Qualità speciali 15, nessuna separa l'equipaggiamento da combattimento. Sulla card ha scelto «Voci mancanti, ordine PF1e»: Tattiche fra Attacco e Statistiche. 99 schede riordinate, pagine dei booklet 985 → 985.
- **Trovato nel repo:** `ADR-0091` → `plans/adr/ADR-0091-la-scheda-del-png-ha-una-forma.md`
- **Solo qui:** la consigliata sulla card era tenere l'ordine di prima, e Jfs ha scelto l'altro. Il secondo passo automatico ha spostato la sola etichetta «Tattiche» in tre schede che hanno le tattiche in paragrafi numerati (i due Ghaurush, Zin'thara): `sezioni_leggibili` si ferma alla prima riga vuota seguita da un paragrafo, quindi quelle si spostano a mano. In appendice la scheda di chi ha la riga breve nel capitolo esce senza Tattiche: è voluto (ADR-0107), non una perdita.

### MS-0108 · 2026-11-13 · ADR-0126 lotto 8: adamantio, mithral, bastoni con le cariche

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede
- **Origine:** addendum della riga del 2026-11-13 «ADR-0126, lotto 8 terza parte: adamantio, mithral, bastoni con le cariche» in `plans/CHANGELOG.md`
- **Testo:** `oggetti.toml` ha il costo in più di adamantio e mithral per categoria; la verifica `ricchezza` lo somma al potenziamento e conta i bastoni con le cariche scritte. Misura: violazioni 33 → 33, non verificabili 374 → 375; banco, terza prova: 1 → 52 su 125. Nella stessa PR le risposte di Jfs a cinque card del 13/11 (thread dell'audit): duergar con classi da PG a GS 2 e 8 con i file rinominati, goblin combattente di 1° a GS 1/3, tre righe di Balvar rimesse intere (Jfs non ha scelto la consigliata «tieni i tagli»), Terros 348 pf, «Virare» al posto di «Virata».
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** «scudo pesante» sta anche fra le armi del plugin: la prima versione contava uno «scudo pesante di adamantio» come un'arma di adamantio (3.000 mo), ma la tabella dell'SRD non prezza uno scudo di adamantio. Un nome che è anche scudo o armatura non prende il prezzo dell'arma. Il bastone del fuoco di Ghaurush (10 cariche, 3.550 mo) porta la sua scheda sopra la tabella di 1.300 mo: resta non verificabile perché la razza non ha un modificatore di livello noto.
### MS-0109 · 2026-11-13 · Piano di recupero: D5 chiusa e lotto L4, il registro delle adozioni prende i lotti interni

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0076
- **Temi:** piani decisioni adozioni registro
- **Origine:** riga del 2026-11-13 «L4 · I piani fermi, una casella alla volta (e D5 chiusa)» in `plans/CHANGELOG.md`
- **Testo:** Jfs ha risposto voce per voce alla quinta domanda del piano di recupero sulle card del thread audit (13/11, 23:40-23:50): convertitori e shellcheck nel blocco piattaforma v1.5.0; frecce sulle mappe in attesa di un caso vero; dossier di ARC-09 dopo ARC-07 al tavolo; Foundry quando lo usa; carte del Drappo subito in un thread a parte; riassunto del Drappo dopo una serata; whisper.cpp in prova su una serata; carta del cielo sì per ARC-09; template PF1e sì col thread delle regole; incontri tarati alla chiusura della v1.2.0; Blockbench in attesa. Due card nel thread del piano: il registro prende solo le condizioni misurabili (R-6), e Blockbench aspetta una serie ComfyUI vera.
- **Trovato nel repo:** `plans/PIANO-RECUPERO-DECISIONI-E-REVISIONI-INCOMPIUTE-2026-10.md` (R-6, D5, L4) · `plans/adozioni-in-attesa.json` · `scripts/adozioni_in_attesa.py`
- **Solo qui:** la prima condizione di Blockbench («lo script per le serie ComfyUI su main») era vera dal 2026-09-05 (`scripts/comfyui_batch.py`, 494174ce): la riga di RICERCA-TOOL-LGM §3.3 che lo diceva «non fatto» era ferma da settembre. Le cinque attese lasciate fuori dal registro non hanno nessun allarme: le trova solo la routine del lunedì leggendo i piani. La soglia di 3 righe per «serie vera» e shellcheck nella v1.5.0 sono deduzioni del thread, non risposte di Jfs. La voce è nata MS-0108 ed è diventata MS-0109 al riallineo, dopo la #417 delle regole; il numero MS-0118 assegnato prima non è servito, perché la PR è entrata prima delle altre in coda.

### MS-0110 · 2026-11-14 · RICERCA-TOOL-LGM-2026 §3.1: la carta del cielo di Zalkatar

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0005 ADR-0019
- **Temi:** arc09 handout immagini indagine
- **Origine:** riga del 2026-11-14 «§3.1, la carta del cielo come handout» in `plans/CHANGELOG.md`
- **Testo:** Jfs, 2026-11-13: «Sì, per ARC-09» alla carta del cielo come indizio; sulla card della pista ha scelto la Torre invisibile, «dove cammina» (consigliata). Stellarium 23.4 da apt gira nel container con Xvfb e Mesa software; uno script `.ssc` dà un PNG 1400×1400. Cultura del cielo `rumblingstone` con dieci figure sopra le posizioni reali (Hipparcos); stella-chiave HIP 81833 nel Sigillo, allo zenit a latitudine 38,922, sul meridiano alle 00:04 UT del 2000-06-01 a longitudine 0 (= mezzanotte del 30 Mirtul, giorno 152). Handout 7 con nota DM a tre strati.
- **Trovato nel repo:** `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-HANDOUTS.md` (handout 7) · `09_…/Immagini-Handout/carta-del-cielo/PROVENIENZA.txt`
- **Solo qui:** la voce è nata MS-0108 ed è diventata MS-0110 al riallineo, dopo la #417 e la #421. La 23.4 di Ubuntu non ha il plugin SkyCultureMaker citato nel §3.1: la cultura del cielo è scritta a mano nei file `.fab`. Il segno di selezione è l'unico modo trovato per cerchiare la stella: `MarkerMgr.markerEquatorial` non disegna nulla nella 23.4, e il segno è animato (due lanci differiscono in 36×36 pixel). A mezzanotte esatta la stella è a un grado dal meridiano, quindi lo script usa le 00:04. Il punto di consegna l'ha deciso Jfs sulla card il 2026-11-14 («tutte e due»: il mago dei piromanti drow, e Sethrax come seconda occasione); anche la distanza del passo, un grado a sud (circa 110 km), l'ha decisa Jfs sulla seconda card: nessun `[INFERRED]` resta nell'handout. Il dossier delle piste di ARC-09 è fermo fino alla fine di ARC-07 al tavolo.

### MS-0111 · 2026-11-13 · B3: le carte da tavolo del Drappo prima della serata

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0020 ADR-0129 ADR-0131
- **Temi:** stampa drappo standalone tavolo
- **Origine:** riga del 2026-11-13 «Voce B3 della ricerca sul modulo pubblicabile: le carte da tavolo del Drappo» in `plans/CHANGELOG.md`
- **Testo:** Jfs ha scelto «Subito» sulla card delle carte da tavolo del Drappo di Tarsilia (voce B3 di `plans/RICERCA-COSA-SERVE-A-UN-MODULO-PUBBLICABILE.md`), contro la consigliata di aspettare una serata vera come diceva il §5. Fatte nella catena typst dei booklet: 36 carte 63 × 88 mm in quattro fogli A4, PDF/UA-1 e PDF/A-2a conformi con veraPDF 1.28.2 (0 controlli falliti); misura_stampa delle carte senza errori. La voce B3 resta 🟡 finché una serata non dice quali carte servono.
- **Trovato nel repo:** `10-stand-alone/Il-Drappo-di-Tarsilia/homebrew/README.md` (Le carte da tavolo) · `docs/reference/RIFERIMENTO-BOOKLET.md` §1.2-bis · `scripts/tests/test_carte_tavolo.py`
- **Solo qui:** la voce è nata MS-0108 sul ramo ed è diventata MS-0111 al riallineo dopo #417, #421 e #422 (il coordinatore aveva detto prima MS-0116, poi corretto: il check vuole numeri consecutivi). Gli scudi della serie Golarion portano nel cartiglio il motto del Palio («Pungo solo chi mi assale» per l'Istrice): sulle carte le scritte si tolgono alla lettura e il cartiglio resta vuoto, perché copiare gli SVG avrebbe fatto copie vecchie (CONTRADE §7). La griglia delle Lunghezze sul segnaposto è una scelta di disegno, non una regola: le regole dicono «su un foglio a vista, una riga per contrada».

### MS-0112 · 2026-11-13 · ADR-0132: le copie delle immagini tengono la provenienza

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0132 ADR-0019
- **Temi:** immagini provenienza booklet ai-generativa
- **Origine:** addendum della riga del 2026-11-13 «ADR-0132: le copie delle immagini tengono la dichiarazione di provenienza» in `plans/CHANGELOG.md`
- **Testo:** Quarta tecnica della richiesta del DM del 2026-11-13. 28 master del repo hanno un manifesto C2PA firmato (Google per il Drappo e Durik, OpenAI per tre ritratti di Hella) con la sorgente digitale IPTC; le copie `web/` che vanno nei booklet la perdevano alla ricompressione. `provenienza_immagini.py` la riscrive nella copia come XMP IPTC senza ricomprimere. Copie etichettate 0 → 28 su 28; immagini JPEG nei 20 PDF 0 → 36 su 89; pixel e pagine identici.
- **Trovato nel repo:** `plans/adr/ADR-0132-le-copie-delle-immagini-tengono-la-provenienza.md` · `plans/esperimenti/provenienza-immagini-2026-11-13/MISURE.md` · `scripts/provenienza_immagini.py`
- **Solo qui:** Gemini mette il manifesto C2PA in un blocco di testo del PNG («Raw profile type app11») scritto in esadecimale, con un'intestazione che ha cifre sue: cercare «c2pa» nei byte del file ne trovava 18 su 28, e togliere tutti i caratteri non esadecimali sfasava la decodifica; si tengono solo le righe lunghe di esadecimale. Typst incorpora il JPEG così com'è, quindi l'XMP arriva dentro il PDF. Firmare le copie con c2pa-python scartato: chiede un certificato della lista di fiducia C2PA. Una prima corsa di misura è stata buttata perché l'export girava nella cartella di lavoro mentre cambiavo ramo: le misure lunghe vanno in un worktree a parte. Le 24 copie senza manifesto (20 di ARC-07, 4 ritratti dei PG) restano senza etichetta: dichiararle è una scelta del DM.

### MS-0113 · 2026-11-14 · ADR-0091: le voci che mancavano in sei schede di ARC07-DEF-4

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0091
- **Temi:** schede stampa booklet regole
- **Origine:** riga del 2026-11-14 «ADR-0091, le voci che mancavano nelle schede di ARC07-DEF-4» in `plans/CHANGELOG.md`
- **Testo:** seconda PR della scelta del DM «Voci mancanti, ordine PF1e» (2026-11-13). Linguaggi, Qualità speciali e «Altro equipaggiamento» in sei schede, solo da ciò che la scheda usa già o che l'SRD 3.5 dà alla razza. La serata Notte e Alba passa da 125 a 126 pagine e il booklet completo da 158 a 159: la scheda di Balvar si spezza su due pagine, e il DM l'ha accettato sulla card del 2026-11-14.
- **Trovato nel repo:** `ADR-0091` → `plans/adr/ADR-0091-la-scheda-del-png-ha-una-forma.md` · `docs/audit/stampa-booklet.json`
- **Solo qui:** bastano quattro righe in più nelle schede di guardie e sacerdote per spezzare Balvar, prima ancora che le sue tre righe tornino intere. `verifica_scheda` legge l'equipaggiamento solo da una riga che comincia con «Equipaggiamento»: non vede né la voce dentro le Statistiche (la forma di ADR-0091) né «Altro equipaggiamento», quindi la misura di `ricchezza` non si muove; detto al thread delle regole. `linguaggi.toml` ha solo le razze dei PG: per hobgoblin e orco i linguaggi automatici stanno nelle voci dei mostri dell'SRD. Sulla card avevo scritto «due pagine affiancate» senza verificarlo, e l'ho corretto subito dopo. La riga 994 di questo file è storia e non si corregge, anche dove l'audit del 2026-11-13 la trova superata. Nella stessa PR le righe ferme trovate dall'audit del 2026-11-13: P09 e inventario Gemini in STATO-E-ORDINE, casella VOL-3 del piano di stampa.

### MS-0114 · 2026-11-14 · ADR-0134: l'equipaggiamento standard dai Codex PF1e entro il valore del 3.5

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0134, ADR-0126
- **Temi:** regole schede equipaggiamento
- **Origine:** riga del 2026-11-14 «ADR-0134 e ADR-0126, lotto 8 quarta parte: l'equipaggiamento standard» in `plans/CHANGELOG.md`
- **Testo:** Jfs, 2026-11-13 sera: l'equipaggiamento standard di mostri e PNG non si inventa, si prende dalle tabelle dei manuali in modo deterministico; sulla card ha scelto «Codex PF1e, livello effettivo». Nel repo entrano i 454 PNG dei due Codex, la Tabella 14-9, il prezzo base degli oggetti comuni, la regola «Improving Monsters» e il registro delle regole custom con la voce RC-001. Sette schede vere risultano sopra la Tabella 4-23 (Avarthel, Bothor e Malvur, il comandante dei mercenari di Dauth, il blackguard e il chierico di Abbathor, Krusk, Ur-Vrax): Jfs ha risposto «Tieni e dichiara» alle sette card il 2026-11-14 e ogni scheda porta la riga «Equipaggiamento sopra la tabella: scelta del DM», senza cambiare numeri. Misura: violazioni 30 → 30 (37 senza le dichiarazioni), non verificabili 372 → 374; banco, quarta prova 0 → 50 su 118.
- **Trovato nel repo:** `ADR-0134` → `plans/adr/ADR-0134-l-equipaggiamento-standard-viene-dai-codex-pf1e-entro-il-valore-del-3-5.md`; `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** le sette schede sopra la tabella non vengono dal prezzo base ma dal leggere l'equipaggiamento dove le schede lo scrivevano già, dentro la riga delle Statistiche: prima la verifica non lo vedeva. Una scheda scrive l'equipaggiamento due volte (recinto e prosa) e la prima versione l'avrebbe contato doppio. La quarta riga della Tabella 14-9 nel PRD somma 1.750 mo nelle categorie contro un totale di 1.650. Il thread del volume ha segnalato le forme non lette; Durin non risulta sopra la tabella con la misura di oggi.

### MS-0115 · 2026-11-14 · RICERCA-TOOL-LGM-2026 §3.1: la carta del cielo con Stellarium 26.2

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0005 ADR-0019
- **Temi:** arc09 handout immagini indagine
- **Origine:** riga del 2026-11-14 «§3.1, la carta del cielo passa a Stellarium 26.2» in `plans/CHANGELOG.md`
- **Testo:** Jfs, 2026-11-14: «usalo e aggiorna Stellarium se migliora il risultato ed il miglioramento è misurabile». Misura: due lanci dello stesso script davano 619 pixel diversi con la 23.4 (la stella-chiave segnata dalla selezione, che è animata) e ne danno 0 con la 26.2 e un segno fisso (`MarkerMgr.markerEquatorial`). Sulla card del 2026-11-14 Jfs ha scelto «Sì, con il parallelo»: il plugin ArchaeoLines traccia la declinazione 38,922, il parallelo della stella-chiave.
- **Trovato nel repo:** `09_…/Immagini-Handout/carta-del-cielo/PROVENIENZA.txt` · `09_…/Immagini-Handout/carta-del-cielo/carta-del-cielo-zalkatar.ssc` · handout 7 in `Arco-Post-Hammerfist-HANDOUTS.md`
- **Solo qui:** la voce è nata MS-0114 ed è diventata MS-0115 al riallineo dopo la #425. SkyCultureMaker, il plugin nominato nel §3.1, c'è nella 26.2 ma è solo a finestre: non ha comandi da script, quindi `index.json` è scritto a mano e il plugin non migliora alcuna misura. La 26.2 rifiuta i `.fab` («Failed to find index.json») e non ha più `core.setSkyLanguage`. Senza schermo restava appesa a `quitStellarium` finché in `config.ini` non ci sono il luogo fisso, `automatic_updates_enabled=false` e `flag_search_online=false`. L'AppImage legge `/usr/share/stellarium` se c'è una 23.4 installata da apt. ArchaeoLines accende di suo tutte le sue linee: vanno spente una per una; l'etichetta del parallelo non compare nell'immagine. Fra 23.4 e 26.2 senza segno cambiano circa 25.000 pixel di disegno, senza differenze che si vedano.

### MS-0116 · 2026-11-14 · ADR-0133: la scheda a tutta pagina va su due colonne

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0133
- **Temi:** schede stampa booklet typst
- **Origine:** riga del 2026-11-14 «ADR-0133, la scheda a tutta pagina va su due colonne dentro il riquadro» in `plans/CHANGELOG.md`
- **Testo:** terza PR dello standard delle schede. Nelle pagine a una colonna il corpo della scheda esce su due colonne pari dentro il riquadro, come le colonne dei manuali PF1e e 3.5. Scelta del DM sulla card del 2026-11-13, in prova fino al 2026-11-28.
- **Trovato nel repo:** `ADR-0133` → `plans/adr/ADR-0133-la-scheda-a-tutta-pagina-va-su-due-colonne.md` · `scripts/tests/test_scheda_due_colonne.py`
- **Solo qui:** in typst un blocco di altezza fissa con dentro `columns(2)` si spezza da sé a pagina girata e le colonne riprendono: provato con una scheda di 4000 parole, nessuna parola persa. L'altezza del blocco è metà del corpo misurato a mezza larghezza più 16 pt, perché le fasce non si dividono mai a metà esatta. La misura delle righe lunghe non è nel repo: conta le righe dentro i riquadri col fondo del tema larghi più di metà pagina che contengono la fascia DIFESA; un primo conto per corpo del carattere prendeva anche piedi e colophon e dava 80 righe invece di 11. Durante la misura ho usato `git stash` per provare che il test fallisce senza la modifica mentre `misura_stampa` girava: ho fermato e rifatto la misura da capo. Il worktree di confronto aveva ancora la modifica della prova: fermato e rifatto anche quello. Il DM ha visto la prova con la soglia a 6 cm, e la soglia è rimasta quella.

### MS-0117 · 2026-11-13 · I giorni di «chi sa cosa» in state.yaml e la regola T2

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0125
- **Temi:** coerenza storia canone state
- **Origine:** voce scritta con la PR, per la riga del 2026-11-13 «Canone di «chi sa cosa»» in `plans/CHANGELOG.md`
- **Testo:** Il DM ha risposto a D1-D4 della proposta dei giorni e alla riga 69 di ARC07-DEF-1. `conoscenze[]` ha `dal_giorno` e `informato_da`; 27 righe su 33 hanno un giorno: dei 27 proposti il DM ne ha confermati 22 su card («Sì, tranne i 5 a fiducia bassa») e i cinque dedotti senza fonte restano senza giorno (Sonjak su Sal, Ghostlord, Xal'thor sui Bracieri, il Collezionista su Therysol, Therysol sulla cella di Dauth). Il Collezionista sa dei Custodi e degli artefatti dalla sua gilda, dal Giorno 22 (card del DM). Lettera di Brenna: Thorik comandante, niente «Custodi Eterni», consegna al Giorno 22; Brenna sa della vittoria dal Giorno 19 (uccelli) e di Lorana di persona. Norro conosce il titolo dal Giorno 23. DEF-1 r.69: «I Rumbling Stones». `coerenza_campagna fatti --state` ha T2; su main 0 violazioni.
- **Trovato nel repo:** `ADR-0125` → `plans/adr/` (file ADR-0125, «i giorni di chi sa cosa e la regola T2») · la proposta → `plans/esperimenti/grafo-eventi-2026-11-12/PROPOSTA-GIORNI-CHI-SA-COSA.md`
- **Solo qui:** T1 non è entrata perché state.yaml non ha chiave del fatto, alias e finestre dei file; T2 senza chiave del fatto confronta i PNG e non i fatti. Brenna non ha `informato_da: tempestas`: col giorno 19 sarebbe stata una catena rotta, perché Tempestas ha la sua prima riga al 21, e il DM ha messo gli uccelli come fonte della vittoria. Zalkatar ha il giorno 26 scritto, uguale a quello di Sethrax che lo informa nello stesso giorno. Le righe 6 e 17 (Conte Valerius) restano doppie: nessuna risposta del DM. Per la riga del Collezionista il canone non dava una fonte sola: Sonjak non sa delle tre gemme e Mira non ha legami con la gilda, quindi è andata a card. Il dossier del DM rigenerato porta anche i livelli degli archi che erano rimasti indietro dal 17/10. Il coordinatore aveva prenotato MS-0114: il cancello vuole la sequenza, quindi il numero si rifà al riallineo.

### MS-0118 · 2026-11-14 · Generatore, lotto J: i sette modelli semplici di PF1e

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0034
- **Temi:** generatore creature modelli pf1e
- **Origine:** riga del 2026-11-14 «Lotto J, i modelli semplici di PF1e» in `plans/CHANGELOG.md`
- **Testo:** Jfs ha autorizzato il lotto J sulla card del 2026-11-13 («Sì, col thread delle regole»). Il generatore applica al blocco finito i sette modelli semplici del Bestiary di PF1e senza cambiare il GS scritto: i numeri stanno in `sistemi/pf1e/dati/modelli.toml` con la fonte per riga, il conto in `scripts/dmcore/modelli.py`, l'opzione è `--template`. `--piu-cattivi` è `--template advanced`. Gli archetipi di classe restano fuori.
- **Trovato nel repo:** `ADR-0034` → `plans/adr/ADR-0034-generare-dalle-tabelle.md`
- **Solo qui:** il vecchio conto del modello Avanzato lasciava ferma l'iniziativa e scriveva «+2 Advanced» nel dettaglio della CA invece di alzare Destrezza e armatura naturale; l'ha trovato il test del conto esatto. `pf-dado` registra i dadi e i bonus che non vengono dalla Costituzione, quindi un modello non lo tocca: cambia il bonus nella riga del tipo. I dadi di danno seguono le tabelle delle armi del Core Rulebook; da 2d6 in su le tabelle delle armi e degli attacchi naturali divergono, e un dado che la tabella non ha resta com'è e viene dichiarato. Per disfare un modello serve la traccia di ciò che ha fatto: il passo dei dadi all'ingiù non è l'inverso di quello all'insù.

### MS-0119 · 2026-11-14 · Regole, lotto 7 quinta parte: linguaggi di hobgoblin, orco, drow, duergar

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole linguaggi razze verifica-scheda
- **Origine:** riga del 2026-11-14 «lotto 7 quinta parte» in `plans/CHANGELOG.md`
- **Testo:** La verifica `linguaggi` giudica anche nove razze senza dadi vita razziali, coi linguaggi automatici che l'SRD scrive nel capitolo dei mostri. L'ha chiesto il thread del volume. Schede giudicate nel Bestiario 7 → 14 su 24, banco 13 → 27 su 27, nessuna violazione e nessuna scheda toccata.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** le razze coi dadi vita razziali (bugbear, gnoll, ogre, troll) restano fuori apposta: la riga dell'SRD è per il personaggio giocante. Un test vecchio dava il drow come «razza fuori dalla tabella» ed è stato girato.

### MS-0120 · 2026-11-14 · Regole, lotto 6 terza parte: razze dei mostri, taglia e velocità nelle abilità

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole abilità razze saltare verifica-scheda
- **Origine:** riga del 2026-11-14 «lotto 6 terza parte» in `plans/CHANGELOG.md`
- **Testo:** Il margine dei gradi contato voce per voce vale anche per nove razze senza dadi vita razziali. Entrano il +4 di taglia a Nascondersi dei Piccoli e il modificatore della velocità a Saltare. Una violazione nuova, vera: Bothor e Malvur hanno Saltare +6 dove la regola dà +2. Il DM ha risposto «Correggi a +2» sulla card e la scheda è corretta.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** la prima estrazione dava «hide = 1» ai Piccoli, perché l'espressione prendeva il «+1» dell'attacco nella stessa frase; l'ha mostrato il diff del file dati. Le schede di prova dei talenti erano un orco barbaro tarato sul margine fisso: ora sono uno gnoll.

### MS-0121 · 2026-11-14 · Regole, lotto 7 sesta parte: velocità di hobgoblin, orco, drow, duergar

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole velocità razze armature verifica-scheda
- **Origine:** riga del 2026-11-14 «lotto 7 sesta parte» in `plans/CHANGELOG.md`
- **Testo:** La verifica `velocita` giudica anche nove razze senza dadi vita razziali: schede giudicate 18 → 34. Due violazioni vere, su card al DM: la Furia della Mano a 12 m con un'armatura media e il bladebearer hobgoblin con il nome dell'armatura sbagliato rispetto alla fonte PCGen. Il DM ha risposto sulle card: corazza di mithral per la Furia (resta a 12 m), giaco di maglia +1 per il bladebearer.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** due schede di hobgoblin regolari scrivono 6 m senza scomporre la CA: la prima versione le dava per violazioni, ed erano solo armature non nominate. Da lì la regola del dubbio. La correzione diretta del nome dell'armatura del bladebearer è stata fermata: una scheda si cambia solo con la risposta del DM, anche quando è un errore di trascrizione.

### MS-0122 · 2026-11-14 · Regole, lotto 8 quinta parte: la ricchezza di un file con più schede

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole ricchezza equipaggiamento master verifica-scheda
- **Origine:** riga del 2026-11-14 «lotto 8 quinta parte» in `plans/CHANGELOG.md`
- **Testo:** `ricchezza` giudica scheda per scheda anche i file con più schede. Prima usciva senza dire niente, e ARC07-DEF-4 non era controllato contro la Tabella 4-23. Una violazione vera: Durin Rocciadura ha 6.137 mo di equipaggiamento contro i 5.600 di un PNG di 6°. Il DM ha scelto sulla card del 14/11 lo scudo pesante perfetto al posto del +1: CA 22 → 21, valore sotto il tetto, tre booklet rigenerati.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** nella #425 era stato scritto che le schede allungate di ARC07-DEF-4 non davano violazioni nuove: era vero solo perché non erano lette. L'ha notato il thread del volume, ed è stato detto a Jfs. Una misura che tace va controllata: tace perché è in regola o perché non guarda?

### MS-0123 · 2026-11-14 · Regole, lotti 6 e 7: velocità, linguaggi e abilità di un file con più schede

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole velocita linguaggi abilita master verifica-scheda
- **Origine:** riga del 2026-11-14 «lotti 6 e 7: velocità, linguaggi e abilità di un file con più schede» in `plans/CHANGELOG.md`
- **Testo:** `velocita`, `linguaggi` e `abilita` giudicano scheda per scheda i file con più schede, con la stessa funzione di `ricchezza` (`_scheda_per_scheda`). Violazioni 30 → 30, non verificabili 383 → 384. Nei 5 master con più recinti `velocita` legge 11 schede (prima 0), `linguaggi` 3 (prima 0), `abilita` 11 (prima 5).
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** il guadagno è piccolo e va detto: nessuna violazione nuova, e 13 schede su 30 dei master non si leggono perché il recinto non ha attributi o GS. Per misurare contro la versione di prima serve un worktree pulito: `git worktree add` su una cartella rimasta da una prova vecchia non la aggiorna, e la prima misura confrontava con un commit di giorni fa (54 violazioni invece di 30).
### MS-0124 · 2026-11-14 · ADR-0134: il corredo delle schede PCGen e i Codex come complemento

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0134
- **Temi:** schede equipaggiamento regole bestiario
- **Origine:** riga del 2026-11-14 «ADR-0134, regola RC-001 applicata alle prime undici schede del Bestiario» in `plans/CHANGELOG.md`
- **Testo:** undici schede di `Bestiario/mostri/` hanno le voci «Equipaggiamento da combattimento» e «Altro equipaggiamento». Il corredo è quello della riga «Possessions» dell'export PCGen; dai Codex PF1e entrano solo uso limitato e attrezzatura, entro la Tabella 4-23 al livello effettivo. Nessun numero di scheda cambia.
- **Trovato nel repo:** `ADR-0134` → `plans/adr/ADR-0134-l-equipaggiamento-standard-viene-dai-codex-pf1e-entro-il-valore-del-3-5.md` · `campaign/REGOLE-CUSTOM.md`
- **Solo qui:** l'audit dell'equipaggiamento guardava solo i file .md e dava 24 schede senza corredo: dodici lo avevano nell'export PCGen (riga «Possessions», o righe EQUIPNAME nel .pcg). Tolto quello, il PNG dei Codex aggiunge poco: armi e armature doppiano quelle della scheda, mantelli e anelli cambierebbero i numeri. Tre export stanno sopra il tetto (duergar chierico 3, Ainin, orco regular) e l'orco regular non torna con la scheda confermata il 18/10: decisioni del DM, fuori da questa PR. Scrivere il mantello della resistenza nel corredo fa rifare a `genera_attributi.py --rigenera --scrivi` la marca della Saggezza (hobgoblin regular), e dopo va riscritta l'impronta delle creature. `ricchezza` somma un minimo: i valori nelle note delle schede sono contati a mano coi prezzi dell'SRD.

### MS-0125 · 2026-11-14 · Regole, lotto 8 sesta parte: merci, proiettili, pezzi doppi e arco composito

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole ricchezza prezzi oggetti merci proiettili arco-composito verifica-scheda
- **Origine:** riga del 2026-11-14 «lotto 8 sesta parte: merci, proiettili, pezzi doppi e arco composito nei prezzi 3.5» in `plans/CHANGELOG.md`
- **Testo:** `ricchezza` conta le merci dell'SRD 3.5, i proiettili, le armi a più pezzi, lo scudo d'acciaio, la mezza armatura, le pozioni con la forza nel nome e l'arco composito con la Forza scritta. I dati li genera `estrai_oggetti.py` in `oggetti.toml` (`merci`, `ammo`, `scudi_acciaio`, `arco_forza`). Elenco dei Codex del thread del volume: 0 → 63 voci col prezzo su 96. Nel repo 472 → 489 voci col prezzo. Violazioni 30 → 30, non verificabili 384 → 384.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** il guadagno sul repo di oggi è di 17 voci: il lavoro serve alle schede che il thread del volume riempie dai Codex. Errori trovati per strada e corretti: gli shuriken prezzati come arma e non come proiettili, «unholy water» letta come acqua santa, «pozione di scudo della fede +2» letta come scudo +2, «arco lungo composito (+1 For)» contato 100 mo invece di 200. Le 33 voci che ha solo PF1e non si prezzano dall'SRD 3.5 e vanno a card.

### MS-0126 · 2026-11-14 · Regole, lotto 5 quinta parte: i draghi veri per colore e categoria d'età

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole draghi creatura-base grado-di-sfida armatura-naturale verifica-scheda
- **Origine:** riga del 2026-11-14 «lotto 5 quinta parte: i draghi veri per colore e categoria d'età» in `plans/CHANGELOG.md`
- **Testo:** `creature_base.toml` ha le 120 voci dei draghi veri dell'SRD 3.5 per colore ed età, generate da `estrai_creature_base.py`. `verifica_scheda` giudica armatura naturale e grado di sfida di un drago che dichiara colore ed età. Violazioni 30 → 33, non verificabili 376 → 380. Le tre violazioni nuove (Arbitrax due, Tyrgarun una) sono su card al DM.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** la prima versione dava tre violazioni false su Skullcrusher: ha «Avanzato» nel tipo (+2 di armatura naturale, canone del DM) e ora un modello dichiarato esce «non verificabile». Dadi vita diversi dall'età non sono una violazione perché i draghi crescono dentro l'età. L'adulto rosso dell'SRD ha Sag 19, più del maturo: è così nella fonte e i dati generati non si correggono a mano.

### MS-0127 · 2026-11-14 · Regole, lotto 5 sesta parte: il grado di sfida di chi avanza per dadi vita

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole grado-di-sfida avanzamento dadi-vita draghi verifica-scheda
- **Origine:** riga del 2026-11-14 «lotto 5 sesta parte: il grado di sfida di chi avanza per dadi vita» in `plans/CHANGELOG.md`
- **Testo:** `gs.atteso` conta i dadi vita aggiunti a una base dichiarata con la tabella dell'SRD 3.5 (`[gs.avanzamento]`: +1 ogni 4, 3 o 2 dadi vita per tipo, +1 se cresce di taglia). Violazioni 33 → 34, non verificabili 380 → 378. Ozyrrandion è a posto a GS 14; Tyrgarun diventa violazione (18 contro 19) sulla scheda già a card.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** la regola non si applica a una base trovata per nome. Flind (Manuale dei Mostri II) e ogre Skullcrusher (Races of Faerûn) hanno «gnoll» e «ogre» nel nome ma sono mostri loro: contarli come avanzati avrebbe dato due violazioni false (flind GS 1 invece di 3).

### MS-0128 · 2026-11-14 · ADR-0134: le quattro decisioni del DM sul corredo

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0134
- **Temi:** schede equipaggiamento regole bestiario
- **Origine:** riga del 2026-11-14 «ADR-0134, regola RC-001: le quattro decisioni del DM sulle card del 14/11» in `plans/CHANGELOG.md`
- **Testo:** duergar chierico 3 e Ainin tengono il corredo dell'export sopra la Tabella 4-23, dichiarato come scelta del DM; per l'orco regular vale la scheda del 18/10 e non il .pcg; il mantello della resistenza +1 dei Codex entra nel goblin incursore su worg e nel Portalame, coi tiri salvezza +1.
- **Trovato nel repo:** `ADR-0134` → `plans/adr/ADR-0134-l-equipaggiamento-standard-viene-dai-codex-pf1e-entro-il-valore-del-3-5.md` · `campaign/REGOLE-CUSTOM.md`
- **Solo qui:** il «sì» agli oggetti che alzano CA e tiri salvezza tocca in pratica solo il mantello della resistenza +1: l'anello e l'amuleto del Bloodfire Sorcerer Kulkorzhul li ha già, il mantello non entra nel chierico della Mano del Destino (5.567 + 1.000 supera 5.600), la cintura della forza del gigante +2 nel 3.5 non esiste a quel prezzo (punto 7 della regola: DM). Il monaco «Pugno del Destino» resta fuori da questa PR: il suo Riflessi +8 ha un +1 che la scheda non spiega e la scheda è in mano al thread delle regole per la velocità. La riga «Equipaggiamento sopra la tabella: … DM» è quella che `verifica_scheda.ricchezza` riconosce. La scheda dell'orco regular non aveva `voci:` nello statblocco: aggiunte.

### MS-0129 · 2026-11-14 · Regole: le tre risposte del DM su monaco, Arbitrax e Tyrgarun

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole schede variante-del-dm regole-custom draghi grado-di-sfida velocita verifica-scheda
- **Origine:** riga del 2026-11-14 «le tre risposte del DM sulle card» in `plans/CHANGELOG.md`
- **Testo:** il DM ha risposto alle tre card del 2026-11-14. Monaco «Pugno del Destino»: velocità 15 m, «Hobgoblin» nel titolo. Arbitrax: variante del DM, +24 di armatura naturale e GS 15 restano, voce RC-002 delle regole custom. Tyrgarun: molto vecchio, GS 19. `verifica_scheda` accetta una variante dichiarata nella scheda se porta il numero della scheda e «DM», una voce RC o un ADR. Misura contro main 99c09bb6: violazioni 34 → 30, non verificabili 378 → 375.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** la prima forma della dichiarazione cercava il numero in tutta la riga, e «15 contro il 13» faceva passare anche una scheda che scrivesse 13: ora conta solo il primo numero dopo i due punti. Il file di Tyrgarun è stato rinominato in `tyrgarun-blue-very-old-cr19.md`: `extract_statblocks.py --check` boccia un blocco con GS 19 in un file «cr18»; le citazioni vive seguono, quelle storiche no. Il GS «16–17» a terra della Fase 4 e la riga «Boost log» della scheda non sono stati toccati: restano al DM.

### MS-0130 · 2026-11-14 · ADR-0134: il corredo dell'Hobgoblin Bladebearer

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0134
- **Temi:** schede equipaggiamento regole bestiario
- **Origine:** riga del 2026-11-14 «ADR-0134, regola RC-001: il corredo dell'Hobgoblin Bladebearer» in `plans/CHANGELOG.md`
- **Testo:** il Bladebearer ha il corredo dei suoi due export PCGen (Build A nello statblocco, Build B in nota) più una pozione di cura ferite moderate e il mantello della resistenza +1 del «Troglodyte Champion»; tiri salvezza +1.
- **Trovato nel repo:** `ADR-0134` → `plans/adr/ADR-0134-l-equipaggiamento-standard-viene-dai-codex-pf1e-entro-il-valore-del-3-5.md` · `campaign/REGOLE-CUSTOM.md`
- **Solo qui:** la doppia ascia orchesca +1 dell'export ha una testa sola incantata («Axe, Orc Double +1;-»): 60 mo + 600 del perfetto sulle due teste + 2.000 = 2.660 mo; il verificatore la legge come un'ascia +1 da 2.306. Con pozione e mantello la Build A arriva a 7.160 su 7.200: non c'è più posto per niente. La cintura della forza del gigante +2 dei Codex (4.000 mo come i guanti del potere dell'ogre) non entra in nessuna delle schede che la avrebbero dal loro PNG: supera il tetto ovunque, quindi non serve una decisione del DM. Lythiel sta a circa 23.800 mo su 9.400 per l'amuleto della salute +4 che tiene i suoi pf 60: card al DM.

### MS-0131 · 2026-11-14 · Regole, lotto 5 settima parte: il grado di sfida dei modelli dell'SRD

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole grado-di-sfida modelli scheletro zombi mezzo-immondo celestiale verifica-scheda conformita
- **Origine:** riga del 2026-11-14 «lotto 5 settima parte: il grado di sfida dei modelli dell'SRD» in `plans/CHANGELOG.md`
- **Testo:** `gs.atteso` conta dieci modelli dell'SRD 3.5 con `[gs.modelli_gs]`: aumento per soglie di dadi vita (celestiale, immondo, mezzo-celestiale, mezzo-immondo), aumento fisso (mezzo-drago, lich, vampiro, fantasma), grado dai dadi vita (scheletro, zombi). Violazioni 30 → 31, non verificabili 375 → 372 contro main ce805024. Nella stessa PR `conformita_statblocchi` smette di leggere una voce di equipaggiamento come attacco.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** `vampir\w*(?!\s+spawn)` non esclude «vampire spawn», perché `\w*` torna indietro di una lettera: serve `\b` prima del lookahead. L'SRD scrive «Hellhound» nel blocco sotto il titolo «Hell Hound»: `[gs.nomi_base]` in `gs.toml` porta i nomi delle schede alle chiavi dei dati. Il gufo gigante celestiale resta non verificabile perché avanza anche per dadi vita e la sua fonte nomina un modello. Lo Skeletal Dire Lion scrive «2x HD», ma il modello scheletro non raddoppia i dadi vita: lo fa lo zombi.

### MS-0132 · 2026-11-14 · Regole, lotto 5 ottava parte: la base dichiarata con un modello che non ne cambia i numeri

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole creatura-base modelli celestiale immondo avanzamento dadi-vita gufo-gigante verifica-scheda
- **Origine:** riga del 2026-11-14 «lotto 5 ottava parte: la base dichiarata con un modello che non ne cambia i numeri» in `plans/CHANGELOG.md`
- **Testo:** `creature_base.dichiarata` accetta una fonte che nomina celestiale o immondo, la base fra parentesi e i nomi di `[gs.nomi_base]`; `verifica_scheda.creatura_base` accetta i dadi vita di un avanzamento che la fonte dichiara. Violazioni 31 = 31, non verificabili 372 → 369 contro main 2ade1d5c: il gufo gigante celestiale è giudicato per intero e in regola.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** la prima versione faceva dichiarare la base a ogni fonte col nome della creatura accanto a un modello, e l'Ogre Skullcrusher (Races of Faerûn, «Ogre» nel percorso del file citato) prendeva una violazione falsa sul grado di sfida: la base si dichiara solo dopo «SRD», «MM» o «Monster Manual». `_recinti_del_master` non vede un blocco senza `ca:` e `ts:`: una scheda di prova troppo corta non arriva mai a `_base_del_blocco`. Il massimo della riga «Advancement» non è nei dati.

### MS-0133 · 2026-11-14 · ADR-0134: Lythiel senza l'amuleto e i tiri salvezza del monaco

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0134
- **Temi:** schede equipaggiamento regole bestiario png
- **Origine:** riga del 2026-11-14 «ADR-0134, regola RC-001: due decisioni del DM sulle card del 14/11» in `plans/CHANGELOG.md`
- **Testo:** Lythiel perde l'amuleto della salute +4 (Cos 13, pf 44, Tempra +8, Concentrazione +7); il Monaco «Pugno del Destino» prende il mantello della resistenza +1 e passa a +8/+8/+8.
- **Trovato nel repo:** `ADR-0134` → `plans/adr/ADR-0134-l-equipaggiamento-standard-viene-dai-codex-pf1e-entro-il-valore-del-3-5.md` · `campaign/REGOLE-CUSTOM.md`
- **Solo qui:** sulla card di Lythiel il DM aveva tre scelte (tenere il corredo sopra il tetto come scelta del DM, amuleto +2, via l'amuleto) e ha scelto la terza contro la consigliata: l'amuleto era entrato il 16/10 solo per far tornare i pf 60 della scheda. La soglia di morale di Lythiel («sotto 20 pf») non è stata toccata: su 44 pf è quasi la metà, prima era un terzo. Sul monaco le scelte erano regola più mantello (+8/+8/+8), numeri dell'export più mantello (+8/+9/+8), niente mantello; il +8 ai Riflessi dell'export PCGen resta senza spiegazione.

### MS-0134 · 2026-11-14 · Regole: lo Skeletal Dire Lion ha 16 dadi vita e grado di sfida 7

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole grado-di-sfida scheletro skeletal-dire-lion ghostlord decisione-dm
- **Origine:** riga del 2026-11-14 «risposta del DM sulla card dello Skeletal Dire Lion» in `plans/CHANGELOG.md`
- **Testo:** il DM ha scelto sulla card del 2026-11-14 di tenere i 16 dadi vita e di portare il grado di sfida a 7. La scheda toglie «2x HD», il file diventa `skeletal-dire-lion-cr7.md`, `IN_ATTESA` del grado di sfida torna vuoto. Violazioni 31 → 30 contro main e88959fd.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** nel tipo non si può scrivere «avanzato» né ripetere «scheletro» accanto a «skeleton»: `gs.modello_noto` vede un avanzamento o un secondo modello e il grado torna non verificabile. Restano al DM il livello d'incontro delle due righe del viaggio verso Cannath Vale che usano questi leoni e l'armatura naturale +4 (lo scheletro Grande dell'SRD ha +2).

### MS-0135 · 2026-11-14 · A6: il dossier delle piste di ARC-09

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** —
- **Temi:** indagine piste ARC-09 torre-invisibile zalkatar sonjak collezionista ghaurush zin-thara carta-del-cielo travaso gate
- **Origine:** riga del 2026-11-14 «A6, il dossier delle piste di ARC-09» in `plans/CHANGELOG.md`
- **Testo:** `Arco-Post-Hammerfist-DOSSIER-DELLE-PISTE.md` riscrive come piste i tre misteri di ARC-09: la torre che cammina (congegno, A1-A7), il «dottore» che compra i drow (B1-B6, pista morale senza bonus) e le due lettere di Sonjak (C1-C7). Gate «dopo ARC-07» tolto da Jfs il 2026-11-14 nel progetto, superando la sua card D5 del 2026-11-13. Tre scelte nuove a Jfs su card: S1 piromanti in scena fissa, S2 effetto delle lettere uguale a Zin'thara voltata, S3 lettere nella trattativa di Ghaurush al posto del Seme-Mercato.
- **Trovato nel repo:** `plans/PIANO-TRAVASO-DRAPPO-CAMPAGNA.md` §A6 · `skills/rumblingstone-indagine`
- **Solo qui:** il nodo più forte della pista della torre (la carta del cielo) stava su una voce di tabella d% al 15% per giornata; le lettere di Ghaurush stanno su un villain il cui esito di default è la fuga; il ramo «Sonjak tradisce la Mano Rossa» non aveva effetto scritto; l'handout 7 rimandava a un §4.3 della sub-quest di Artemis che non esiste (è §4.1); `P2A-Torre-PARTE1` §1 chiama ancora Artemis «alleata/PNG chiave», lasciato com'è. Saraah è marcata `[NON-CREATURA]` come Thorgrim: persona senza numeri in nessun file, e `test_bestiario_h` ne elenca le schede. «CS» delle schede di Ghaurush e Zin'thara non è definito altrove nel repo. Jfs ha deciso le tre card il 2026-11-14, tutte sulla consigliata: S1 scena fissa dei piromanti fra G22 e G26 sulla strada vera; S2 le lettere valgono come Zin'thara voltata (−1 CS Fase 0, non si sommano ai registri); S3 Ghaurush vende le lettere al posto del Seme-Mercato, chi le prende rinuncia alla tregua.

### MS-0136 · 2026-11-14 · ADR-0134: il corredo del Fantino Cavaliere del Palio

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0134
- **Temi:** schede equipaggiamento regole palio
- **Origine:** riga del 2026-11-14 «ADR-0134, regola RC-001: il corredo del Fantino Cavaliere del Palio» in `plans/CHANGELOG.md`
- **Testo:** il Fantino Cavaliere ha giaco di maglia +1, nerbo, una pozione di cura ferite moderate e due di contrastare elementi; 1.650 mo su 5.600.
- **Trovato nel repo:** `ADR-0134` → `plans/adr/ADR-0134-l-equipaggiamento-standard-viene-dai-codex-pf1e-entro-il-valore-del-3-5.md` · `campaign/REGOLE-CUSTOM.md`
- **Solo qui:** sulla card il DM aveva tre scelte (armatura leggera e pozioni; le stesse più il mantello della resistenza +1 del «Troglodyte Champion», TS +8/+7/+5; nessun corredo) e ha scelto la prima. La scheda dice solo «armatura leggera da corsa»: il giaco di maglia +1 (1.250 mo) è l'armatura leggera meno cara che dà +5; anche il cuoio borchiato +2 (4.175 mo) lo darebbe. Il tetto è contato sul 6° livello della classe; la scheda dichiara GS 8 e «Cavaliere-ish», quindi il livello effettivo non è certo. Sulla card la pozione era chiamata «resistere agli elementi»: il nome del lessico è «contrastare elementi».

### MS-0137 · 2026-11-14 · ARC-07/08: nuovi nomi e appellativi degli Eroi di Hammerfist e della Madre Superiora

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** —
- **Temi:** arc08 arc07 nomi pregen eroi-di-hammerfist decisione-dm
- **Origine:** riga del 2026-11-14 «Nomi degli Eroi di Hammerfist scelti dal DM» in `plans/CHANGELOG.md`
- **Testo:** il DM ha scelto sulle card del 2026-11-14 (21:37 e 22:17-22:18): Borin Ferropugno diventa Borin Giuraferro, «Colui che non arretra» (era «Il Martello di Hammerfist»); Thorin Runaforte diventa Harbek Runaforte, «Custode dell'Ultima Runa» (era «La Voce di Moradin»); Dara Occhiolesto prende «Morte dai Picchi» (era «L'Occhio delle Montagne»); Nala Cantapietre prende «Il Sorriso prima della Lama» (era «La Lama Nascosta»); la Madre Superiora Dana Forgiapietra diventa Dagmar Forgiapietra, detta Dana. Schede rinominate `Borin_Giuraferro.md` e `Harbek_Runaforte.md`; quella della Madre resta `Dana_Forgiapietra.md`, col nome d'uso.
- **Trovato nel repo:** `Bestiario/png/Borin_Giuraferro.md`, `Bestiario/png/Harbek_Runaforte.md`, `Bestiario/png/Dana_Forgiapietra.md` (vecchi nomi nei blocchi storico)
- **Solo qui:** con Harbek cade l'avviso dei tre nomi simili (A10, D2); resta quello Thorik/Thorek. Il file della Madre non si rinomina perché il registro dei nomi di `misura_craft.py` prende i nomi dai file del Bestiario: senza «Dana» il voto della corsa A-senza-1/S06 cambiava (box_un_nome) e `voto_scrittura --check` cadeva. Restano coi vecchi nomi, per scelta: esperimenti, scritture, archivi, registri, fixture di test congelate, i caduti «Borin Manodura» e «Dara Passolesto, occhio delle montagne» della Cerimonia delle 100 Asce (altri nani). Nell'ARC-09 (P1B, P1C) «Borin» porta Aegis Fang, quindi è un segnaposto per Thorik e non il pregen: non toccato, da decidere a parte. Non scritti perché le card sono aperte: cosa fare se un giocatore non vuole guidare un eroe, la rosa allargata.

### MS-0138 · 2026-11-14 · Regole: l'armatura naturale dei modelli dell'SRD

- **Data:** 2026-11-14
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole armatura-naturale modelli scheletro mezzo-immondo mezzo-drago lich vampiro zombi
- **Origine:** riga del 2026-11-14 «lotto 5 nona parte» in `plans/CHANGELOG.md`
- **Testo:** le voci di `[gs.modelli_gs]` portano la chiave `naturale` con la riga «Armor Class» dei modelli dell'SRD; il controllo sta dentro `creatura_base`. Il controllo ha trovato lo Skeletal Dire Lion (+4 contro il +2 dello scheletro Grande); il DM ha scelto sulla card del 2026-11-15 «+2 come l'SRD, CA 13» e la scheda è corretta nella stessa PR. Misura contro main fc5c1a8e: violazioni 30 = 30, non verificabili 368 → 369; schede con modello giudicate sull'armatura naturale 0 → 2.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** la base è nota solo per le razze fatte di livelli di classe (0, coboldo +1); altrove si giudica il minimo del modello. Una CA scritta come «contatto 11, alla sprovvista 16» non è un conto e non dà violazione. Azarr Kul finale, Therysol e il Ghostlord non sono giudicati perché il tipo non nomina il modello. `naturale_razze` sta dentro `[gs.modelli_gs]`, non in `[gs]`.

### MS-0139 · 2026-11-15 · ARC-09: il Borin di P1B e P1C è il pregen Borin Giuraferro, col martello

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** —
- **Temi:** arc09 pregen borin aegis-fang eroi-di-hammerfist decisione-dm
- **Origine:** riga del 2026-11-15 «ARC-09, scelta del DM sulla card del 15/11» in `plans/CHANGELOG.md`
- **Testo:** in P1B (Cerchio dei Treant) e P1C (Rituale) un «Borin» impugnava Aegis Fang, l'ascia di Thorik. Il DM ha scelto sulla card del 15/11 che sia il pregen Borin Giuraferro col *Martello da Guerra degli Avi +2*; la consigliata era Thorik. I poteri dell'ascia sono tolti e sostituiti dalle capacità della scheda di Borin (ARC08-01 §PNG giocabili).
- **Trovato nel repo:** i due file di ARC-09, col vecchio testo riassunto nel blocco storico.
- **Solo qui:** la scelta tocca il D14, che dà Borin «campione di Re Thorek a Hammerfist» dopo la battaglia: in ARC-09 viaggia col gruppo. Se Borin muore nel flashback le due scene vanno rifatte per il PG che prende il suo posto. Thorik, che porta Aegis Fang, in quelle scene non ha un posto scritto (in P1B c'è un «PG4», in P1C «PG2» e «PG3»). La carica fermata si regge sulla regola SRD del percorso libero della carica, non su un potere.

### MS-0140 · 2026-11-15 · ADR-0134: il corredo del Fantino Ladro e della Drow Chierica di Lolth del Palio e del Collezionista

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** ADR-0134
- **Temi:** schede equipaggiamento regole palio
- **Origine:** riga del 2026-11-15 «ADR-0134, regola RC-001: il corredo del Fantino Ladro e della Drow Chierica di Lolth del Palio e del Collezionista» in `plans/CHANGELOG.md`
- **Testo:** il Fantino Ladro ha cuoio borchiato +1, anello di protezione +1, nerbo con aghi, arnesi da scasso e una pozione di cura ferite moderate; 3.505 mo su 9.400. La Drow Chierica di Lolth ha armatura completa +1, scudo pesante di acciaio, mantello della resistenza +1, perla del potere 1°, pugnale e balestra leggera; 4.709 mo su 12.000. Il Collezionista ha cinque pozioni, una bacchetta di scudo, anello di protezione +1 e mantello della resistenza +2: CA 26, tiri salvezza +13/+12/+15, 9.060 mo.
- **Trovato nel repo:** `ADR-0134` → `plans/adr/ADR-0134-l-equipaggiamento-standard-viene-dai-codex-pf1e-entro-il-valore-del-3-5.md` · `campaign/REGOLE-CUSTOM.md`
- **Solo qui:** sulla card il DM aveva tre scelte (armatura, anello e pozione; le stesse più il mantello della resistenza +1 del «Trapsmith», TS +5/+11/+4, 4.505 mo; nessun corredo) e ha scelto la prima. La scheda non nomina l'armatura: cuoio borchiato +1 (1.175 mo) più anello di protezione +1 (2.000 mo) è una lettura della CA 19 con Des 18, non l'unica possibile. Il veleno del nerbo (CD 14, 1d2 Des) non ha un nome nella scheda e non è contato nel valore. Come per il Fantino Cavaliere, il corredo sta anche nella riga Statistiche perché il booklet non stampa le `voci:` delle schede con Statistiche scritta a mano. Per la Drow Chierica le scelte erano quattro (questa; la stessa più il talismano della saggezza +2 con Sag 20, 8.709 mo; il corredo del «Drow Priest», che è un Chierico 5, più un anello di protezione +1, 5.133 mo; nessun corredo) e il DM ha scelto la prima. La scheda dà solo CA 22, pf 63 e Sag 18: la Destrezza 12 che fa tornare la CA è una lettura, non un dato. Il tetto è 12.000 mo al 9° livello di classe, 21.000 se si conta il modificatore di livello +2 dei drow. Per il Collezionista le scelte erano quattro (questa; mantello del Carisma +2 al posto di quello della resistenza, Car 22 e CD +1; solo pozioni e bacchetta, 3.060 mo; niente) e il DM ha scelto la prima. Dal «Lucky Mage» non entrano l'amuleto dell'armatura naturale, perché al collo c'è già l'Amuleto dell'Eclissi Planare, e la fascia del Carisma, che nel 3.5 è un mantello. Le pozioni di volare e di invisibilità e la bacchetta di scudo doppiano incantesimi che conosce già. Il suo livello effettivo è 25 (18 DV più il modificatore +7 del rakshasa): la Tabella 4-23 si ferma al 20°. Il benchmark della scheda lo dava a CA −8 dalla riga del GS 18; ora è −7.

### MS-0141 · 2026-11-15 · Le prove sul portatile con la RTX 4050 hanno uno script ciascuna

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** ADR-0089 · ADR-0125
- **Temi:** prove-4050 gpu ollama llm-locale coerenza immagini gemini
- **Origine:** riga del 2026-11-15 «Prove sul portatile con la RTX 4050» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto se i thread che aspettano la prova sul suo ASUS (RTX 4050 da 6 GB, 16 GB di RAM, Bazzite) avessero istruzioni e script pronti. L'inventario del 15/11: pronta solo la prosa col 12B (`scripts/llm-locale/`); trascrizione pronta ma solo nella PR #424 in bozza; lettore della coerenza senza file delle domande; immagini in posa con la pipeline solo nei file del progetto e un profilo GPU da 10 GB; nessuno strumento per importare le chat di Gemini esportate. Ora ogni prova ha uno script in `scripts/prove-4050/`, la guida è `docs/how-to/GUIDA-PROVE-PORTATILE-4050.md` e i risultati tornano come archivio caricato nel thread.
- **Trovato nel repo:** `docs/how-to/GUIDA-PROVE-PORTATILE-4050.md` · `scripts/prove-4050/` · `scripts/importa_gemini.py` · `plans/esperimenti/immagini-posa-4050-2026-11-15/LEGGIMI.md`
- **Solo qui:** le domande del lettore sono state generate nel container con torch su CPU e `intfloat/multilingual-e5-small` (recupero 3,5 minuti sul repo). Il lettore va lanciato con `LLM_CTX=4096`, perché col contesto di serie di 32k token il 7B non starebbe tutto nei 6 GB: è una stima dal peso del modello, non una misura. Le tre manopole delle immagini (`RS_COMFY_ARGS`, `RS_LIBERA`, `RS_VLM_DEVICE`) non sono mai girate su una GPU. Il formato di Takeout per «App Gemini» non è documentato: il lettore è scritto sui campi noti di «La mia attività» e provato su campioni sintetici. Le schede con decodifica vincolata (tecnica 3 di Document AI) non hanno ancora una prova da lanciare.

### MS-0142 · 2026-11-15 · ARC-07: la tattica di Skullcrusher diventa dinamica, e la misura del duello

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** ADR-0118
- **Temi:** arc07 skullcrusher tattiche drago simulazione barile decisione-dm
- **Origine:** riga del 2026-11-15 «ARC-07 DEF-4 Scena 11, la tattica di Skullcrusher» in `plans/CHANGELOG.md`
- **Testo:** Jfs ha chiesto perché il drago attacchi solo nel cortile, che cosa faccia coi PG in volo o invisibili e perché li attacchi se ne sa solo il nome. Audit: «Chi sceglie» era già dinamico sul chi ma non sul dove; r.2403 («cala dove sta il re») non reggeva, perché dalla piana l'orda non vede il cortile. Otto card, tutte scelte sulla consigliata: porta principale e re; tabella «Dove sono i PG all'alba»; *vedere invisibilità* al corno; B13 secondo l'SRD; chi colpisce l'orda dall'alto subito dopo la Catena; alla prima paura esita; inchiodato attacca chi tiene la corda (com'era); *dissolvi* solo su chi in aria lo minaccia.
- **Trovato nel repo:** `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` Scena 11 e Appendice A.1 · `07_il Portale Della Forgia Eterna/ARC07-BARILE-SULLA-TENDA.md` B13 · `plans/esperimenti/duello-skullcrusher-2026-11-15/`
- **Solo qui:** la simulazione (20.000 duelli per tattica) stima i bonus d'attacco di Thorik (+22) e Tordek (+23 in ira), che la carta del 05/11 non porta, e lascia fuori Durik, gli evocati e le pozioni: le morti sono un tetto. Con la CA 40 i due combattenti in mischia contano poco e la Catena (CA 44) si spezza nel 4-6% dei duelli: il DM non ha cambiato questi numeri. Il motivo per cui il drago va sui PG non è il nome, che è solo la componente di *colpo accurato*: è la Corona di Thorik (per lui un re), il barile della notte e il fatto che stanno fra lui e la porta. Il 50 minuti di *vedere invisibilità* in A.1 era il numero dell'Adulto. Sullo stesso metodo il thread «Rivedere le tattiche di tutti i draghi».

### MS-0143 · 2026-11-15 · Le tattiche di Fauci di Palude e di Tyrgarun, simulate e scelte dal DM

- **Data:** 2026-11-15
- **PR:** #450
- **ADR:** —
- **Temi:** draghi tattiche fauci tyrgarun arbitrax regiarix vaereth simulazione decisione-dm arc08 arc09
- **Origine:** riga del 2026-11-15 «Tattiche dei draghi, richiesta del DM del 15/11» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto tattiche da creature più intelligenti del gioco per tutti i draghi tranne Skullcrusher: carattere, obiettivi, cosa sanno dei PG, adattamento all'ambiente e allo stato dei PG, simulate. Inventario: Fauci, Arbitrax, Ozyrrandion, Regiarix, il drago rosso dei Githyanki di Vaereth, Tyrgarun, l'Avatar di Tiamat. Sulle card del 15/11 il DM ha scelto per Fauci la tattica nuova con la fuga a 112 pf, per Tyrgarun la tattica da stregone nelle Fasi 1-3 con la condizione scritta per la Fase 4, e per Arbitrax il bruto col difetto d'orgoglio, con la percezione cieca al posto della «vista cieca». Le schede di Regiarix e del drago rosso di Vaereth sono rifatte sull'SRD, come ha scelto il DM.
- **Trovato nel repo:** `plans/esperimenti/tattiche-draghi-2026-11-15/` (proposta, simulatore, esiti) · `08_La Battaglia Di Hammerfist/ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md` §1 · `Bestiario/villain/Tyrgarun/tyrgarun-blue-very-old-cr19.md`
- **Solo qui:** la misura ha detto che un drago più astuto uccide meno PG, non di più: la leva dei morti è la soglia di fuga. Il Mythal toglie a Tyrgarun il volo ma non il soffio da 20d8, quindi il «GS 16-17» a terra non reggeva. Con resistere all'energia 30 dei PG il canone di Arbitrax non uccideva nessuno in 20.000 prove. Regiarix giovane adulto (GS 9, l'età delle Armate, che però gli davano GS 10) abbassa Rhest da EL 13 a circa 11-12; il titolo del file diceva CR 13. Il drago di Vaereth non ha nome nelle fonti. Gli incantesimi conosciuti di tutti e due e i talenti sono scelte di questa revisione o del DM, non fonte. Corrompere acqua sulle cisterne di Hammerfist e l'oscurità sulle balliste sono nella proposta, non nella scheda. Non si sa se Artemis abbia un'invocazione per vedere l'invisibile.

### MS-0144 · 2026-11-15 · Zog'tar sulla breccia dell'alba separa e finisce, e sa che i nani volano

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** —
- **Temi:** tattiche villain zogtar arc07 simulazione barile balvar
- **Origine:** riga del 2026-11-15 «Tattiche di villain e PNG, primo gruppo (ARC-07)» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto di rivedere le tattiche di villain e PNG con lo schema dei draghi (carattere, cosa sanno dei PG, ambiente, stato dei PG, simulazione). Primo gruppo: Zog'tar sulla breccia (ARC07-DEF-4 Scena 10). Sulle card del 15/11 il DM ha scelto «separa e finisce» (Occhio su Tordek, Colpo Terrificante che butta Thorik nel cortile, attacco completo −5/+10 su chi resta) e Balvar e il sacerdote al campo all'alba, come DEF-4. Corrette nel BARILE §8 le righe che li mettevano sulla collina e sulla breccia, e le cure del sacerdote, che la sua scheda non ha. In ARC08-02 §1 la tattica di Gorthak diceva ancora «tre attacchi» e «Furia fino alla morte»: allineata al canone del 04/11 di ARC08-DEF-2 (due randelli, un round di Furia, poi la fuga). Grimjaw e Gorthak in ARC08-DEF-2 hanno già lo schema (vuole, sa, teme, ambiente) e non sono stati riscritti.
- **Trovato nel repo:** `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` (Scena 10) · `07_il Portale Della Forgia Eterna/ARC07-BARILE-SULLA-TENDA.md` (§8) · `plans/esperimenti/tattiche-2026-11-15/LEGGIMI-ZOGTAR.md`
- **Solo qui:** 20.000 prove per riga, seme 1372. Stretto sul camminamento (CA 20) Zog'tar muore il 99-100% delle volte in circa 3 round, con qualunque tattica. Un PG muore nell'11% delle prove col solo Colpo su chi ha davanti, nel 28% con «separa e finisce», nel 32% con l'attacco pieno; fuori dal camminamento 33%, 69% e 73%. I bonus d'attacco di Thorik e Tordek sono stimati (con +4 cambia di 1-6 punti). Fuori dal modello: le guardie, le balestre dell'orda, Re Thorek, i PG che scendono alle spalle, la vulnerabilità alla luce divina (non ha un numero). Il DM ha scelto l'opzione più letale sapendo che pesa sul duello col drago che segue. 264 pf all'alba = 249 (mediana del barile) + 15 di riposo SRD.

### MS-0145 · 2026-11-15 · Ozyrrandion tentatore, l'Avatar di Tiamat sul Mythal, l'oscurità di Fauci su di sé

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** —
- **Temi:** draghi tattiche ozyrrandion tiamat fauci mythal decisione-dm arc08 arc09
- **Origine:** riga del 2026-11-15 «Tattiche dei draghi, seconde card del DM del 15/11» in `plans/CHANGELOG.md`
- **Testo:** dopo la #450 restavano tre proposte senza card; il DM ha scelto la consigliata su tutte e tre. Ozyrrandion parte informato (Sethrax al Torneo, Zalkatar e l'Anello di Artemis) e a metà scontro, sotto 150 pf o con Zalkatar in difficoltà, offre ai PG di tradirlo: offerta vera a metà. L'Avatar di Tiamat attacca chi tiene il Mythal, la sua sola debolezza. Fauci non corrompe le cisterne, che toccherebbero la trama dell'assedio. Il DM aveva scelto l'oscurità sulle baliste; alla verifica era sbagliata (l'occultamento va a chi sta nell'area, quindi ai serventi, e le baliste a +10 colpiscono la CA 37 solo col 20 naturale), e su una seconda card il DM ha scelto l'oscurità su un sasso che Fauci tiene durante l'assedio, lasciato cadere prima della picchiata su Thorik.
- **Trovato nel repo:** `Bestiario/villain/ozyrrandion-drago-verde-cr14.md` (Tattiche) · `Bestiario/villain/Avatar_Tiamat/avatar-tiamat-cr17.md` (Tattiche, round 2) · `08_La Battaglia Di Hammerfist/ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md` §1 (Tattiche)
- **Solo qui:** nessuna simulazione: per Ozyrrandion senza Zalkatar nel modello il numero direbbe poco, per l'Avatar cambia solo il bersaglio. Thorik non si può ammaliare per la Corona (Volontà Adamantina e vuoto mentale permanente, `campaign/state.md`). L'oscurità dà il 20% di mancare e nell'SRD 3.5 anche contro la scurovisione; in PF1e la scurovisione la attraversa, e vale la 3.5. *Oscurità profonda* non è nella scheda e darebbe lo stesso 20%. La soglia dei 150 pf per l'offerta di Ozyrrandion è una scelta di questa revisione, non del DM. Resta aperto: Artemis ha un'invocazione per vedere l'invisibile?

### MS-0146 · 2026-11-15 · Xal'thor con l'esplosione mentale a volontà, Kragar con una tattica che sbilancia anche il nano

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** —
- **Temi:** tattiche villain xalthor kragar torneo dauth arc09 simulazione decisione-dm
- **Origine:** riga del 2026-11-15 «Tattiche di villain e PNG, ARC-09 lotto 1 (Torneo di Dauth)» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto di misurare le tattiche del dossier di ARC-09 e di adottare quelle che migliorano. Sulle card del 15/11 ha scelto l'esplosione mentale di Xal'thor a volontà, come l'illithid dell'SRD (ADR-0118), al posto della «ricarica 1d4 round» della scheda, e di scrivere subito la tattica di Kragar, che non ne aveva. La tattica proposta per Kragar diceva di non sbilanciare Tordek per la stabilità del nano e di disarmarlo, e di fare un passo indietro per tenere la portata: la misura l'ha smentita sulle due cose, e il testo adottato sbilancia anche il nano.
- **Trovato nel repo:** `Bestiario/villain/Xal_thor/Xal_thor/Xal_thor.md` (Mind Blast) · `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2B-Torneo-Tordek-BATTLE-STATS-e-VILLAIN-ICONICI.md` (§1, Tattiche) · `plans/esperimenti/tattiche-2026-11-15/duelli_arc09.py`
- **Solo qui:** 20.000 prove per riga, seme 1372, Tordek da solo con i numeri della carta del 05/11 (al Torneo sarà più alto: il confronto fra tattiche è relativo). Kragar si arrende sempre in circa 2 round; Tordek finisce con 79 pf se Kragar lo sbilancia, 81 con soli attacchi completi, 86 se prova a disarmarlo. Il passo indietro non serve: la catena chiodata minaccia anche a 1,5 m e Tordek si avvicina con un passo di 1,5 m. Xal'thor contro Tordek: Tordek muore nel 15% dei duelli con la ricarica, nel 24% a volontà. Se Xal'thor segue il suo obiettivo (Tordek vivo, convinto ad aprire il portale) e usa la suggestione invece di estrarre il cervello, Tordek non muore mai ed è convinto nel 35% dei duelli: il DM l'ha scelto sulla card del 15/11. Danza delle Catene e Pioggia di Ferri non sono SRD: segnalate, non toccate.

### MS-0147 · 2026-11-15 · Zalkatar che non scende mai in mischia, Xilthra con una scheda legale al posto dell'Ombra Drow

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** —
- **Temi:** tattiche villain zalkatar xilthra torre sabotaggio arc09 simulazione decisione-dm scheda-legale
- **Origine:** riga del 2026-11-15 «Tattiche di villain e PNG, ARC-09 lotto 2» in `plans/CHANGELOG.md`
- **Testo:** secondo lotto del dossier delle tattiche di ARC-09. Sulle card del 15/11 il DM ha scelto che Zalkatar resti in alto e non scenda mai in mischia, e che Xilthra Vel'ssin abbia prima una scheda legale e poi la tattica (Sag 20 con 69 pf; il dominio dell'Inganno al posto dell'«Ombra Drow»). Le due versioni d'arco di Xilthra avevano tre errori: l'Ombra Drow non è una classe dell'SRD né di PF1e, *dictum* è un incantesimo legale di 7° che una chierica di Lolth non lancia, e 13 livelli di classe su un drow fanno GS 14, non 13.
- **Trovato nel repo:** `Bestiario/villain/xilthra-velssin-cr13.md` · `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2A-Torre-PARTE4-STATBLOCCHI-Zalkatar.md` (Fasi, Tattiche) · `…-P3-Sabotaggio-Campi-Drow-STATBLOCCHI.md` §4 · `…-Upscale-CR12.md` · `plans/esperimenti/tattiche-2026-11-15/profili_villain.py` (scontri `zalkatar-sanctum` e `xilthra-corte`)
- **Solo qui:** 20.000 prove per riga, seme 1372, PG della carta del 05/11. Zalkatar senza Ozyrrandion: con le fasi di prima muore nell'81% dei casi e nessun PG muore; restando in alto muore nel 65% e almeno un PG muore nel 40% dei combattimenti, che durano 6,8 round invece di 4,4. Xilthra senza scorta e senza arcieri: l'abbozzo (95 pf, CA 25) muore sempre in 1,2 round; la scheda legale con la tattica fugge col Patto nel 47% dei casi, e mettere *influenza sacrilega* prima del *comando superiore* è misurato meglio dell'ordine contrario (PG all'81% dei pf invece dell'88%). Da sola Xilthra non uccide nessun PG: la scorta, che il modello non contiene, è la minaccia vera. Nella scheda la pietra di Ioun resta «non verificabile» perché il lettore della CA non conosce il bonus cognitivo; l'*amuleto di armatura naturale* della proposta è stato tolto perché il collo lo occupa l'*amuleto della saggezza*.

### MS-0148 · 2026-11-15 · Il duello di Karruk sui gradini uccide quasi sempre il campione

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** —
- **Temi:** tattiche villain karruk zarim rethmar torneo arc09 simulazione duello
- **Origine:** riga del 2026-11-15 «Tattiche di villain e PNG, ARC-09 lotto 3» in `plans/CHANGELOG.md`
- **Testo:** terzo lotto del dossier delle tattiche di ARC-09. La tattica scritta di Karruk per il duello sui gradini della breccia (Carta 13) è risultata la migliore di tre: entrare in ira solo quando il campione lo ferisce e usare l'Attacco Poderoso solo contro una CA sotto 25. Non si cambia; nella scheda entra un avviso per il DM, perché il duello così è quasi sempre mortale per il campione. Due incoerenze sono andate al DM su card e il 15/11 sera ha scelto le consigliate: Zarim non estrae il cervello a Tordek e non lo ammalia, perché Xal'thor lo vuole vivo; Karruk non prova a spezzare Aegis Fang, perché un artefatto non si spezza coi mezzi normali.
- **Trovato nel repo:** `Bestiario/villain/Wyrmlord_Karruk/wyrmlord-karruk-cr13.md` (Tattiche, Misura) · `Bestiario/villain/Zarim/zarim-illithid-luogotenente-cr12.md` (Round 2 e 3, Cosa sa dei PG, Misura) · `plans/esperimenti/tattiche-2026-11-15/duelli_arc09.py` (duello di Karruk) · `plans/esperimenti/tattiche-2026-11-15/profili_villain.py` (scontro `zarim-torneo`)
- **Solo qui:** 20.000 prove per riga, seme 1372, campioni coi numeri della carta del 05/11, senza la scorta e senza il razorfiend. Contro Thorik il campione muore nel 79% dei duelli con la tattica scritta e con l'ira al primo turno, nel 57% con l'Attacco Poderoso sempre a −5; Karruk ripiega nel 5%. Contro Tordek il campione muore nel 76-77% in tutte e tre. Zarim senza le ondate è ucciso nel 54-55% dei casi e non uccide nessun PG, sia che salti Tordek sia che no: la scelta su Tordek è di coerenza, non di forza.
### MS-0149 · 2026-11-15 · Eroi di Hammerfist: rosa a sei, eroe al DM sullo sfondo, Cantitrici e capi con nome

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** —
- **Temi:** arc08 arc07 pregen eroi-di-hammerfist cantitrici decisione-dm schede pf1e
- **Origine:** riga del 2026-11-15 «Eroi di Hammerfist, scelte del DM sulle card del 15/11» in `plans/CHANGELOG.md`
- **Testo:** il DM ha scelto sulle card del 15/11: due eroi nuovi (Ragnhild Mantoferro, Maga 10/Maestra del Sapere 3; Yrsa Portastendardo, Cavaliera 12 PF1e dell'Ordine del Drago), il loro destino (Ragnhild incide la Runa dei Custodi Eterni, Yrsa porta lo stendardo alla Cerimonia), l'eroe rifiutato mosso dal DM sullo sfondo, i nomi delle cinque Cantitrici, due capi dei novanta con nome e gesto (Hrolf e Yrsa), cognomi degli altri eroi invariati.
- **Trovato nel repo:** ARC08-01 §PNG giocabili, ARC08-02 §3, ARC08-10 §5.6 e §6.1, ARC07-DEF-5 (comparse e colpo al re), schede nel Bestiario.
- **Solo qui:** sono proposte del thread, non scelte del DM, le tre righe di tattica per ogni eroe, il conto dei bonus con un eroe mosso dal DM e la soglia «tre o quattro rifiuti → §5.5» (marcate come proposta in ARC08-10). La specializzazione in Invocazione di Ragnhild e il nome «Ragnhild» (proposto dal thread audit perché «Sigrun» è la guida delle Cantitrici) non hanno avuto una card a parte. Yrsa è una scheda PF1e in un arco 3.5: BMC, DMC e Percezione restano di PF1e. I pf seguono la convenzione del cancello dei numeri (dado medio arrotondato per difetto, senza massimo al 1° livello): 84 e 114.

### MS-0150 · 2026-11-15 · Regole: le caratteristiche che i modelli dell'SRD cambiano

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole caratteristiche modelli scheletro zombi mezzo-immondo mezzo-drago lich vampiro fantasma
- **Origine:** riga del 2026-11-15 «lotto 5 decima parte» in `plans/CHANGELOG.md`
- **Testo:** le voci di `[gs.modelli_gs]` portano la chiave `caratteristiche` con la riga «Abilities» dei modelli dell'SRD; il controllo sta dentro `creatura_base` (regola `numero.caratteristiche.modello`). Ha trovato lo Skeletal Dire Lion: Des 15 e Car 10 del leone vivo contro Des 17 e Car 1 dello scheletro; il DM ha scelto sulla card del 2026-11-15 «Des 17 e Car 1 come l'SRD» e la scheda è corretta nella stessa PR (CA 13 → 14, Riflessi +7 → +8). Misura: violazioni 30 = 30, non verificabili 369 → 371; schede con modello giudicate sulle caratteristiche 0 → 5.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** gli aumenti si giudicano solo sopra la base che la fonte dichiara, con la stessa taglia e senza livelli di classe, e solo come minimo. Il segugio infernale «mezzo-immondo» ha i numeri del modello draconico (For 15, Cos 15, Car 8, sottotipo dragonblood): visto a mano, il controllo non lo dice perché la fonte è un file PCGen e non dichiara la base. Il DM ha scelto sulla card «Rifarlo mezzo-immondo dall'SRD»: si fa in una PR sua.

### MS-0151 · 2026-11-15 · Regole: la velocità delle creature coi dadi vita razziali

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole velocita creature-base ogre barbaro armatura dadi-vita-razziali
- **Origine:** riga del 2026-11-15 «lotto 7 settima parte» in `plans/CHANGELOG.md`
- **Testo:** `creature_base.toml` del 3.5 porta `vel`, la velocità a terra senza armatura dalla riga «Speed» dell'SRD (378 creature su 409). La verifica `velocita` la usa per chi dichiara la base nella fonte. Ha trovato l'Ogre Frantumapietra: 12 m scritti contro 10,5 m (ogre 40 piedi, barbaro +10, cotta di maglia media che riduce 50 a 35); il DM ha scelto sulla card del 2026-11-15 «10,5 m come l'SRD» e la scheda è corretta nella stessa PR. Nella stessa PR la verifica `ricchezza` prende come livello il massimo fra classi lette e dadi vita dichiarati: una classe ignota («Diviner 5» di Dovil) non abbassa più il livello. Misura: violazioni invariate.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** un'assegnazione a tupla `razza, tabella[razza[0]] = razza[0], razza[1]` usa la `razza` già riassegnata: va scritta in due righe. Il file `misure-velocita.json` era fermo a prima di due correzioni del DM, quindi il passaggio 34 → 42 del banco non è tutto di questo pezzo. PF1e non rigenerato.

### MS-0152 · 2026-11-15 · «Chi sa cosa»: una riga per il Conte Valerius e tre giorni nuovi

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** ADR-0125
- **Temi:** stato campagna conoscenze chi-sa-cosa doppione decisione-dm coerenza-storia
- **Origine:** riga del 2026-11-15 «"Chi sa cosa", dopo la #419» in `plans/CHANGELOG.md`
- **Testo:** il DM ha scelto di tenere una sola riga per il Conte Valerius: resta quella che dice che non sa né della Corona né di Sal. Sulle cinque righe senza giorno ha dato il 23 a Sonjak su Sal, lo 0 al Ghostlord e il 19 a Xal'thor sui Bracieri; le due su Therysol restano senza giorno. Righe 33 → 32, non verificabili 6 → 3, T2 sempre a 0
- **Trovato nel repo:** `campaign/state.yaml` (sezione `conoscenze`) · `scripts/tests/test_state_data.py` · `scripts/tests/test_anagrafica_png.py`
- **Solo qui:** una card del 14/11 chiedeva se la lettera di Brenna fosse già consegnata al tavolo citando la sessione del 3 maggio; quel file è marcato «scritto in anticipo, non giocato», quindi la risposta non è stata applicata e nessun testo è cambiato. Prima di citare un file di `campaign/sessions` come cronaca va letta la testata. Il test dell'anagrafica legge ancora `conoscenze` per posizione (indice 19 → 18): togliere una riga lo sposta

### MS-0153 · 2026-11-15 · I draghi e il See the Unseen di Artemis: chi lo sa e chi lo scopre

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** —
- **Temi:** draghi tattiche artemis invisibilita tyrgarun ozyrrandion fauci conoscenza decisione-dm arc08 arc09
- **Origine:** riga del 2026-11-15 «Tattiche dei draghi contro il See the Unseen di Artemis» in `plans/CHANGELOG.md`
- **Testo:** alla domanda aperta delle MS-0143 e 0145 il DM ha risposto che Artemis vede l'invisibile, ma che non tutti i draghi lo sanno, e ha chiesto di adeguare le tattiche. L'invocazione è *See the Unseen* (`07_il Portale Della Forgia Eterna/PortaleForgia-P1-REVISED-Corretta.md` r.249, con *Voidsense*). Fra i draghi usano l'invisibilità solo Tyrgarun e Ozyrrandion. Tyrgarun non lo sa e lo scopre in battaglia; lo sa dall'inizio solo se Ozyrrandion è fuggito dalla Torre e combatte con lui. Ozyrrandion lo sa da Zalkatar solo se Sethrax è fuggito dal Torneo col seme, come dice il blocco di Zalkatar (`P2A-Torre-PARTE4-STATBLOCCHI-Zalkatar.md` r.67); altrimenti lo scopre al primo colpo. Fauci non usa l'invisibilità, e l'invocazione non attraversa la sua oscurità.
- **Trovato nel repo:** `Bestiario/villain/Tyrgarun/tyrgarun-blue-very-old-cr19.md` (Tattiche, Fasi 1-3) · `Bestiario/villain/ozyrrandion-drago-verde-cr14.md` (Il tentatore) · `08_La Battaglia Di Hammerfist/ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md` §1
- **Solo qui:** chi sa che cosa è dedotto da questa revisione, non scritto dal DM caso per caso: per Tyrgarun che i suoi informatori di Hammerfist non abbiano visto Artemis contro un invisibile; per Ozyrrandion che Zalkatar, quando sa del gruppo, gli passi anche questo. La condizione su Sethrax l'ha segnalata il thread dei villain. La frase canone del 15/11 («Zalkatar ha studiato l'Anello di Artemis») andrebbe letta con la stessa condizione: non l'ho toccata, è una scelta del DM. Arbitrax, Regiarix, il drago di Vaereth e l'Avatar non usano l'invisibilità, quindi per loro non cambia nulla. Skullcrusher ha il suo thread. Il testo di *See the Unseen* (Complete Arcane) non è SRD: vale la descrizione del repo (scurovisione, invisibili, eterei).
### MS-0154 · 2026-11-15 · ADR-0134: il corredo di sette schede (Dovil, Drow Assassina, Duergar mago/ladro, Maewen, Varis, Tempestas, Therysol)

- **Data:** 2026-11-15
- **PR:** —
- **ADR:** ADR-0134
- **Temi:** schede equipaggiamento regole drow duergar png
- **Origine:** riga del 2026-11-15 «ADR-0134, regola RC-001: il corredo di sette schede» in `plans/CHANGELOG.md`
- **Testo:** la Drow Assassina di Lolth ha giaco di maglia in mithral +1, anello di protezione +1, mantello della resistenza +2, spada corta +1, balestra a mano, veleno drow e tre dosi di sangue nero di Lolth; 10.510 mo su 12.000 senza i veleni. Duergar mago/ladro: anello di protezione +1, spada corta +1, collana delle palle di fuoco con una sfera da 4d6, pozione di cura ferite moderate, pergamena di invisibilità (≤6.410 su 9.400). Maewen: anello di protezione +2, mantello della resistenza agli incantesimi, amuleto dei pugni potenti +1 (104.000 su 21.000, sopra la tabella). Varis: giaco di cuoio borchiato +1, pugnale +1, anello dello scudo mentale, borsa conservante tipo I, bacchetta di charme su persone (5 cariche), sigillo di autenticità Non SRD (14.052 su 9.400, sopra la tabella). Tempestas: giaco di maglia +2, anello di protezione +1, spada corta +1, lira della tempesta e mantello d'ombra Non SRD (8.560 su 45.000). Therysol: amuleto dell'armatura naturale +1, anello di protezione +1, mantello del carisma +4, quattro perle del potere, balestra leggera perfetta, lente (30.435 su 9.400, sopra la tabella).
- **Trovato nel repo:** `ADR-0134` → `plans/adr/ADR-0134-l-equipaggiamento-standard-viene-dai-codex-pf1e-entro-il-valore-del-3-5.md` · `campaign/REGOLE-CUSTOM.md`
- **Solo qui:** sulla card il DM aveva tre scelte (solo ciò che la scheda usa; lo stesso più una pozione di cura ferite gravi dal «Sacred Killer» dei Codex, Ladro 6 / Assassino 2 / Chierico 1, 11.260 mo; nessun corredo) e ha scelto la prima. La balestra a mano è contata normale (100 mo), anche se l'attacco a distanza +13 della scheda torna solo con una balestra perfetta o con un bonus che la scheda non scrive: non toccato. I veleni non hanno prezzo nel conto. Nello stesso giro Dovil (`underdark-dovil-runecaster-cr7.md`) ha la scelta del DM (il corredo dell'export PCGen, 5.865 mo su 7.200) e all'inizio non si poteva scrivere: `verifica_scheda.ricchezza` leggeva 2 livelli invece di 7 (non riconosceva «Diviner 5») e faceva cadere `test_ricchezza.py`. Col fix della #446 (3ff97fad) la patch dà 0 violazioni ed entra in questa PR: armatura completa, spadone +1, anello di protezione +1, libro degli incantesimi. Varis: la card diceva 10.575 mo per la sola tabella in prosa; il giaco +1 e il pugnale +1 che la CA 16 e l'attacco già usavano non erano nella tabella e portano il valore a 14.052. Tempestas: l'anello +1 non era nella prosa ma la CA conta «+1 deviazione». Therysol: il verificatore legge 2 dadi vita (non riconosce «Acolita 6») e non conosce il modificatore di livello del modello draconico: giudizio non verificabile, non violazione. La collana del Duergar non ha un prezzo nel lessico (una sola sfera rimasta): il conto la tiene fuori.

### MS-0155 · 2026-11-16 · PIANO-RECUPERO chiuso: L2, L5 e L6, il registro dei rami di nuovo a zero

- **Data:** 2026-11-16
- **PR:** —
- **ADR:** —
- **Temi:** piani recupero registro-rami contenuti-nei-rami decisioni-dm chiusura-piano drappo
- **Origine:** riga del 2026-11-16 «L2, L5 e L6: il piano si chiude» in `plans/CHANGELOG.md`
- **Testo:** il piano di recupero delle decisioni perse (aperto il 2026-10-10) si chiude con tutti i lotti ✅. L5 era chiudibile dal 24/10: la #106 chiusa senza merge quel giorno, RIPRESA-PR D11 decisa l'8/11. L2: R-3 misurato su `91a4f1be` con `--fetch`, dieci rami di `origin` con commit che `main` non raggiunge, quattro di PR fuse (#66, #120, #92, #51), tutti con commit precedenti all'ultimo merge (squash); l'unico successivo, `e5cf5177` del 20/07, è della #52 chiusa senza merge. Test nuovo per la regola R-2. L6: `contenuti_nei_rami --fetch --check` aveva 9 file senza posto, tutti della #424 (trascrizione whisper, bozza dal 14/11), registrata «in volo»; la #99 passa a «superato» (4g-2 fatta con la #313) e la #216 a «portato» (fusa il 10/10). Dopo: 476 riferimenti, 41 file mai arrivati, 0 senza posto. `decisioni_dm`: 324 decisioni in 25 piani, 1 aperta. In STATO §0 la riga P07 elencava sette decisioni aperte (ne resta una) e P21 dava ⬜ L2 e L4.
- **Trovato nel repo:** `plans/PIANO-RECUPERO-DECISIONI-E-REVISIONI-INCOMPIUTE-2026-10.md` §5 L2, L5, L6 · `plans/contenuti-nei-rami.json` · `scripts/tests/test_contenuti_nei_rami.py`
- **Solo qui:** la memoria del progetto dava rosso `contenuti_nei_rami --check` per tre file del ramo `vyifoi`: il 16/11 quel ramo non c'era più e il rosso era della #424. L'unica decisione aperta del repo è RIPRESA-PR D2, l'arte del Drappo: il metodo l'ha scelto il DM l'8/11 (2-3 tavole FLUX.2 klein accanto alle Gemini), ma in `scripts/prove-4050/` non c'è uno script per il Drappo; card a Jfs il 16/11 con la consigliata «script FLUX per il portatile 4050 in un thread a parte». Il criterio di §6 «la routine del lunedì non trova una riga di §2.5» si verifica solo al giro del 23/11.

### MS-0156 · 2026-11-16 · D2 del Drappo: lo script FLUX.2 klein per il portatile 4050

- **Data:** 2026-11-16
- **PR:** #461
- **ADR:** —
- **Temi:** drappo immagini flux comfyui prove-4050 licenze decisioni-dm ripresa-pr
- **Origine:** riga del 2026-11-16 «D2, collaudo dell'arte del Drappo: lo script per il portatile 4050» in `plans/CHANGELOG.md`
- **Testo:** il DM ha scelto sulla card del 16/11 di scrivere prima lo script e poi decidere la D2 guardando. Pesi scelti per la RTX 4050 da 6 GB: `black-forest-labs/FLUX.2-klein-4b-fp8` (4,07 GB, sha256 97ed34fe…), `Comfy-Org/Flux-2-Klein-4B` per Qwen3-4B fp4 (3,85 GB, 3eab03a7…) e VAE (0,34 GB, 868fe7b3…), tutti Apache 2.0 al 16/11. BFL dichiara ~13 GB di VRAM in bf16; la RTX 4050 (Ada) calcola fp8 ma non fp4 (ComfyUI disattiva nvfp4 sotto la capacità 10 e decomprime). ComfyUI al commit `0df1646`, lo stesso di immagini-posa-4050, ha già i nodi di FLUX.2. FLUX.2 [dev] e [klein] 9B sono sotto FLUX Non-Commercial License: aggiunti a `PESI_VIETATI`.
- **Trovato nel repo:** `scripts/prove-4050/drappo-flux.sh` · `scripts/prove-4050/drappo_flux.py` · `scripts/comfyui_batch.py` (`flux2-klein-4b`, `workflow_flux2`) · `docs/how-to/GUIDA-PROVE-PORTATILE-4050.md` §3-bis · `plans/PIANO-RIPRESA-PR-ABBANDONATE.md` D2
- **Solo qui:** prova completa su CPU nel container il 16/11 (4 core, 15 GB): ritratto-vanna in 553 s, PNG da 1,7 MB, RAM di ComfyUI al picco 13.387 MiB (su CPU in fp32, quindi più che sulla GPU); ComfyUI ha caricato 4.254 MB di transformer, 3.670 MB di codificatore e 321 MB di VAE. Corretto lì un errore: ComfyUI rifiuta `--lowvram` insieme a `--cpu`. Che entri nei 6 GB della 4050 è una stima sulla carta (5-6 GB al picco), non una misura; il vincolo più probabile è la RAM (≈8,3 GB di pesi, desktop a 11 GB su 16). Il confronto non è alla pari: le Gemini sono scelte tra più tentativi, il collaudo usa due semi senza scarto, prompt scritti per SDXL, e a cfg 1 il negativo non entra nel calcolo.

### MS-0157 · 2026-11-17 · Ozyrrandion informato sui PG solo se Sethrax è fuggito

- **Data:** 2026-11-17
- **PR:** —
- **ADR:** —
- **Temi:** tattiche draghi ozyrrandion zalkatar sethrax canone decisioni-dm coerenza
- **Origine:** riga del 2026-11-17 «Ozyrrandion parte informato sui PG solo se Sethrax è fuggito dal Torneo col seme» in `plans/CHANGELOG.md`
- **Testo:** la #451 (MS-0145) aveva scritto che Ozyrrandion «è il solo drago che parte informato», da Sethrax al Torneo e da Zalkatar. Il blocco di Zalkatar (r.67) dice invece che Zalkatar sa del gruppo solo se Sethrax è fuggito col seme; la #457 (MS-0153) aveva già messo la condizione sul *See the Unseen*, non sulla frase d'apertura. Il DM ha scelto sulla card del 17/11 la consigliata: la condizione vale per tutto quello che il drago sa dei PG. Se Sethrax è stato catturato, Ozyrrandion legge il gruppo nel primo round, come Zalkatar.
- **Trovato nel repo:** `Bestiario/villain/ozyrrandion-drago-verde-cr14.md` r.50 · `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2A-Torre-PARTE4-STATBLOCCHI-Zalkatar.md` r.67
- **Solo qui:** che quello che Zalkatar ha studiato dell'Anello di Artemis arrivi al drago solo con Sethrax fuggito è una mia lettura della card, che parlava dei PG in generale.

### MS-0158 · 2026-11-17 · Sethrax ha un primo round solo; Azarr Kul e Ushgar già al meglio

- **Data:** 2026-11-17
- **PR:** —
- **ADR:** —
- **Temi:** tattiche villain sethrax torneo azarr-kul ushgar ghaurush rethmar arc09 coerenza decisioni-dm simulazione
- **Origine:** riga del 2026-11-17 «Tattiche di villain e PNG, ARC-09 lotto 4 (Sethrax, Azarr Kul, Ushgar)» in `plans/CHANGELOG.md`
- **Testo:** il primo round di Sethrax dopo lo smascheramento era scritto in due modi: il Bestiario e lo statblocco completo lo fanno teletrasportare al piedistallo dell'Orbe con *Psionic Dimension Door* dopo *Mental Barrier*; PARTE3 lo faceva correre a piedi. PARTE3 stessa rimanda allo statblocco. Il DM ha scelto sulla card del 15/11 la consigliata: vale il Bestiario, e PARTE3 è allineata con una riga di storico. Nello stesso lotto Azarr Kul e Ushgar sono stati misurati sul motore comune: per tutti e due la tattica scritta è la migliore di tre e non cambia; Azarr Kul ha ora una riga su cosa sa dei PG (`[INFERRED]`). Ghaurush non si misura, perché il motore non ha muri né nebbie: le sue schede hanno già una tattica che tiene conto di Hella e dell'Anello di Artemis.
- **Trovato nel repo:** `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2B-Torneo-Tordek-PARTE3-Giorno3-Finale-e-Invasione.md` r.124 · `Bestiario/villain/Sethrax_il_Velato/Sethrax.md` (Round 1) · `Bestiario/villain/Azarr_Kul/azarr-kul-final-cr17.md` (Tattiche, Misura) · `Bestiario/villain/Ushgar_Occhio_Reso/ushgar-occhio-reso-cr13.md` (Tattiche, Misura) · `plans/esperimenti/tattiche-2026-11-15/profili_villain.py` (scontri `azarr-kul-rethmar`, `ushgar-carica`)
- **Solo qui:** la scelta non è stata misurata col simulatore: nel primo round Sethrax non attacca il party, quindi il rischio per i PG non cambia. Il teletrasporto lo espone sul piedistallo a un attacco preparato, che è l'occasione di cattura su cui conta MS-0157 per Ozyrrandion. Numeri, 20.000 prove, seme 1372, PG della carta del 05/11. Azarr Kul (pre-buff, senza Avatar, erinni e luogotenenti, contingenza della parola del ritorno): con la tattica scritta Azarr Kul è ucciso nel 30% dei casi e almeno un PG muore nel 76%; aprendo con *ferire* su Thorik è ucciso nel 52% e un PG muore nel 75%; con *ferire* su Hella al round 2 un PG muore nell'80%, ma i PG finiscono con il 58% dei pf invece del 48%. Ushgar da solo muore sempre, in 1,8 round: un PG muore nel 5% degli scontri se punta Hella, nel 2% se punta Artemis in volo, nell'1% con l'Attacco Poderoso solo contro CA 22 o meno.

### MS-0159 · 2026-11-17 · I villain senza duello di ARC-09 completano lo schema

- **Data:** 2026-11-17
- **PR:** —
- **ADR:** —
- **Temi:** tattiche villain collezionista ghostlord valerius palio sonjak arc09 schema decisioni-dm
- **Origine:** riga del 2026-11-17 «Tattiche di villain e PNG, ARC-09 lotto 5, villain senza duello» in `plans/CHANGELOG.md`
- **Testo:** ultimo lotto del dossier delle tattiche di ARC-09. Per i villain che non si misurano col simulatore si è controllato il cancello delle tattiche e si sono riempiti i punti dello schema che mancavano. Il Collezionista aveva gli esiti `[DA SCRIVERE]`: il DM ha scelto sulla card del 17/11 di scriverli dai quattro patti di §Con i PG. Il Ghostlord e i sicari di Sonjak al Palio hanno ora cosa sanno dei PG. Valerius l'aveva già.
- **Trovato nel repo:** `Bestiario/villain/Il_Collezionista_Rakshasa/Il_Collezionista_Rakshasa.md` §Esiti possibili · `Bestiario/villain/Ghostlord/Ghostlord.md` §Cosa sa dei PG · `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2D-PALIO-STATBLOCCHI.md` §3.1, §3.2
- **Solo qui:** i patti del Collezionista sono scritti per l'anno −1000, mentre il dossier lo mette nel master DEF-04/05 del Torneo. Gli esiti valgono per la scena dei patti; il loro peso al Torneo va deciso quando si fonde quel master. Il ratchet degli `[INFERRED]` era rosso su main da prima (10 contro 7) per le marche nude dei lotti 3-4: qui tutte le marche delle tattiche hanno domanda e base, e la baseline sale a 16 di proposito (14 nei sorgenti, 2 copie nel booklet del Palio generato, dove stanno in un commento e non si stampano).
### MS-0160 · 2026-11-17 · Regole: il segugio infernale rifatto mezzo-immondo dall'SRD

- **Data:** 2026-11-17
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** regole modelli mezzo-immondo hell-hound armatura-naturale creature-base decisioni-dm
- **Origine:** riga del 2026-11-17 «lotto 5 undicesima parte» in `plans/CHANGELOG.md`
- **Testo:** `hell-hound-mezzoimmondo-cr4.md` portava i numeri del modello draconico di Races of the Dragon sotto il nome «mezzo-immondo». Il DM ha scelto sulla card del 2026-11-15 di rifarlo dall'SRD: segugio infernale più mezzo-immondo, For 17 Des 17 Cos 15 Int 10 Sag 10 Car 8, CA 19, artigli 1d4+3 e morso 1d8+1 secondario, soffio CD 14, volo 12 m, punire il bene, *oscurità* e *dissacrare*, GS 4. I 14 punti abilità in più vanno in Acrobazia 3, Intimidire 3 e Scalare 1 (card del 2026-11-17). La verifica `creatura_base` giudica ora l'armatura naturale dei modelli sopra la base che la fonte dichiara, se ha la stessa taglia. Misura: violazioni 34 = 34, non verificabili 388 → 387.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** la card diceva Acrobazia +6, ma Saltare con 5 gradi dà +2 di sinergia: nella scheda è +8, e la nota lo dice. Il .pcg mezzo-immondo spendeva solo 42 punti e aveva Enlarge Breath (fuori SRD) al posto di Correre. I dadi degli attacchi naturali coi modelli restano non verificabili.

### MS-0161 · 2026-11-17 · Tecnica 3 di Document AI: la prova della decodifica vincolata per il 4050

- **Data:** 2026-11-17
- **PR:** #466
- **ADR:** —
- **Temi:** document-ai decodifica-vincolata ollama schema-json tattiche genera-creatura s8 prove-4050 decisioni-dm
- **Origine:** riga del 2026-11-17 «Tecnica 3, decodifica vincolata delle «Tattiche»: la prova per il portatile 4050» in `plans/CHANGELOG.md`
- **Testo:** il DM ha scelto sulla card del 17/11 «Sì, quando accendi l'ASUS»: la tecnica 3 si prova sulla RTX 4050 ed entra solo se migliora. Ragionamento: `genera_creatura.py` fa già i numeri da tabelle, quindi il vincolo serve solo sul testo che rimanda alla scheda, cioè le «Tattiche» che nominano incantesimi o talenti assenti (S8, ADR-0125). La prova confronta, sullo stesso modello (`qwen2.5:7b` di serie), il testo libero con il JSON vincolato dal campo `format` di Ollama, in cui l'azione è un enum delle voci della scheda. Regola del verdetto in `PIANO.md`: meno S8 per scheda, tutte le risposte valide, copertura almeno l'80% del libero.
- **Trovato nel repo:** `scripts/prove-4050/schede-vincolate.sh` · `plans/esperimenti/decodifica-vincolata-2026-11-17/PIANO.md` · `plans/esperimenti/decodifica-vincolata-2026-11-17/schede_vincolate.py` · `scripts/tests/test_prove_4050.py` (`TestSchedeVincolate`) · `docs/how-to/GUIDA-PROVE-PORTATILE-4050.md` §3-ter
- **Solo qui:** S8 vede un incantesimo solo in corsivo, quindi sul braccio libero può contare meno errori di quelli che ci sono: per questo c'è il conto `fuori_lista`. Trovato preparando il campione e non corretto qui: `genera_creatura.py` scrive il talento *Incantesimi focalizzati* con «(bene, caos, legge o male)» invece di una scuola. Le altre tecniche del thread: 1 glifi #398, 2 PDF/A-2a #416, 4 provenienza IPTC #418, 5 andata e ritorno del testo misurata il 13/11 senza margine.

### MS-0162 · 2026-11-17 · Le marche ristampate nei booklet generati non sono debito nuovo

- **Data:** 2026-11-17
- **PR:** —
- **ADR:** —
- **Temi:** inferred marcature ratchet inventory_inferred booklet generati copie baseline
- **Origine:** riga del 2026-11-17 «`inventory_inferred` non conta due volte la marca ristampata in un file generato» in `plans/CHANGELOG.md`
- **Testo:** con la #465 il booklet del Palio ristampava le due marche `[INFERRED]` dei sicari e della chierica, e il ratchet le contava due volte: la baseline saliva a 16 invece che a 14. Ora un file che dichiara in testa `<!-- GENERATO da scripts/` mette le marche già presenti in un sorgente nella classe «copie», che il ratchet non sorveglia.
- **Trovato nel repo:** `scripts/inventory_inferred.py` (`e_generato`, classe «copie») · `scripts/tests/test_inventory_inferred.py`
- **Solo qui:** la copia si riconosce dal testo della marca, spazi normalizzati. Se il sorgente cambia la marca e il booklet non è rigenerato, la vecchia marca nel booklet torna fra gli aperti finché non lo si rigenera: è voluto, perché il booklet non allineato è già un errore di `validate_booklets`.

### MS-0163 · 2026-11-17 · Il generatore scrive la scuola di Incantesimi focalizzati

- **Data:** 2026-11-17
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** generatore talenti incantesimi lessico scuole spell-focus decisioni-dm
- **Origine:** riga del 2026-11-17 «ADR-0126, il generatore: Incantesimi focalizzati con la scuola» in `plans/CHANGELOG.md`
- **Testo:** il lessico dava a Spell Focus il nome «Incantesimi focalizzati (bene, caos, legge o male)», che è il talento degli allineamenti del Libro delle Imprese Eroiche; nel 2026-11-11 (D3 dell'esito del verificatore Prolog) `talenti._per_chiave` aveva tolto la parentesi per la ricerca, ma il generatore la stampava. Ora il nome è «Incantesimi focalizzati» e la scuola è quella con più incantesimi sul blocco (tabella `[scuole]` dall'SRD 3.5, dal PRD per l'APG). Un mostro senza incantesimi prende il talento seguente del ruolo (card del DM del 17/11). Sull'impronta: nome sbagliato 234 → 0, senza scuola 312 → 0.
- **Trovato nel repo:** `scripts/genera_creatura.py` (`scuola_prevalente`, `incantesimi_del_blocco`) · `sistemi/dnd35/dati/liste_incantesimi.toml` `[scuole]`
- **Solo qui:** la regola di parità (vince la scuola dell'incantesimo di livello più alto) è mia, non del DM.

### MS-0164 · 2026-11-17 · Il kit unico delle prove 4050 per quattro sistemi

- **Data:** 2026-11-17
- **PR:** #469
- **ADR:** ADR-0136
- **Temi:** prove-4050 kit distrobox wsl2 debian cachyos bazzite windows ollama whisper fleurs verifica decisioni-dm
- **Origine:** riga del 2026-11-17 «Kit unico delle prove sulla RTX 4050» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto il 17/11 un kit unico per tutte le prove in sospeso sull'ASUS, con installazione, configurazione e verifica automatiche, per Bazzite, Debian 13, «chaucy os» (letto come CachyOS) e Windows. Per Windows ha scelto sulla card la consigliata, WSL2 con Ubuntu 24.04. Il kit riusa senza cambiarle le prove dei thread (lettore, decodifica vincolata, FLUX del Drappo, immagini in posa, prosa) e aggiunge la parte GPU della trascrizione, coi parametri chiesti da quel thread. Coordinato col coordinatore: nessun thread ha cambiato nomi di file di uscita.
- **Trovato nel repo:** `scripts/prove-4050/kit.sh` · `scripts/prove-4050/prove.json` · `scripts/prove-4050/installa.sh` · `scripts/prove-4050/installa-windows.ps1` · `scripts/prove-4050/ospite.sh` · `scripts/prove-4050/verifica.py` · `scripts/prove-4050/trascrizione-gpu.sh` · `scripts/tests/test_prove_4050.py` (`TestKitMultiSistema`, `TestVerifica`) · `docs/how-to/GUIDA-PROVE-PORTATILE-4050.md` («Il kit in un comando», §4)
- **Solo qui:** prova di `trascrizione-gpu.sh` sulla CPU del container (4 thread, RS_SENZA_BOX=1, RS_WHISPER_BACKEND=cpu): FLEURS it_it/dev, 40 righe, 646 s di audio, large-v3-turbo-q8_0, `-l it -mc 0`, riferimento = colonna 3 del TSV. Prima corsa col VAD silero-v6.2.0: 8,6% di parole sbagliate (87 su 1.012), 1.217 s con la suite dei test accanto. Il thread della trascrizione ha chiarito che il VAD perde 62 parole nei buchi (q8_0: 2,3% senza, 8,6% con; q5_0: 5,8% senza, 6,1% con) e ha chiesto di toglierlo: seconda corsa senza VAD, 2,3% (23 su 1.012) in 249 s, 2,6 volte il tempo reale. `verifica.py` segna ko sopra il 3,3%. Trovati e corretti per strada: `gpu_foto` fermava ogni prova sotto `set -e` dove nvidia-smi manca (su WSL2 sta fuori dal PATH), e `-np` di whisper-cli nascondeva le righe che dicono su quale dispositivo gira. Non provati: box su Debian 13 e CachyOS, `--driver`, CUDA in WSL2 (CUDA 12.0 di Ubuntu con g++-12), `installa-windows.ps1`, ogni prova sulla 4050. ADR-0135 della #424 non era prenotato: prenotato qui.

### MS-0165 · 2026-11-18 · La nota di Incantesimi focalizzati solo quando cambia la scelta

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** generatore talenti spell-focus impronte conto rumore
- **Origine:** riga del 2026-11-18 «ADR-0126, il generatore: la nota «niente Incantesimi focalizzati» nel conto» in `plans/CHANGELOG.md`
- **Testo:** dopo la #468 (MS-0163) il conto di ogni blocco senza incantesimi diceva «niente Incantesimi focalizzati», anche quando il ruolo non l'avrebbe mai preso. Il coordinatore ha visto due rossi nuovi in `impronte.py --confronta` (genera_creatura_gs7 e gs14): la sola differenza con ea63a192 era quella riga. Ora `applica_talenti` rifà la scelta senza esclusioni, su copie dello stato e del generatore casuale, e scrive la nota solo se la scelta senza esclusioni avrebbe preso il talento.
- **Trovato nel repo:** `scripts/genera_creatura.py` (`applica_talenti`) · `scripts/tests/test_talenti.py` (`Focalizzati`)
- **Solo qui:** sull'impronta delle 720 creature 484 note tolte e 156 restano, e null'altro cambia; `impronte.py --confronta` torna ai 3 rossi di prima (suggest_encounter, conformita_statblocchi, derive_statblocks).

### MS-0166 · 2026-11-18 · La memoria storica si ritrova per PR e si confronta con la memoria delle sessioni

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** ADR-0137 ADR-0127
- **Temi:** memoria-storica memoria processo audit thread card
- **Origine:** riga del 2026-11-18 «ADR-0137, la memoria storica a ogni blocco di lavoro» in `plans/CHANGELOG.md`
- **Testo:** audit dell'obbligo di ADR-0127 a sei giorni dalla nascita. Imposto da un cancello: voce MS per ogni PR col changelog (88 PR su 90 unite dal 12/11; #387 e #389 toccano solo `docs/`) e forma del file (165 voci). Solo regola scritta: archiviare prima di togliere una riga dalla memoria delle sessioni; nessuna voce su 98 è nata così, né da una scelta su card o da un thread senza PR. Il campo PR resta «—» in 82 voci su 98 perché la voce precede il numero: ora `--pr` lo ricava dal merge, solo per le voci nate da una riga del changelog (le 67 righe portate in blocco dalla #381 non diventano «della» #381); PR ritrovate 37 → 90 su 90, di cui #387 e #389 solo citate in MS-0082. Righe della memoria delle sessioni con PR, ADR, SHA o percorsi che il repo non ha: 84 su 408 controllabili. Il confronto con le regole del progetto di dottorato del DM (lettura a inizio conversazione, cercare prima di chiedere, controllo delle decisioni superate, diario a fine di ogni blocco, decisioni una volta sola, discordanze segnalate) dice che qui mancano l'ordine di ricerca prima di chiedere e la voce a fine blocco fuori dalle PR.
- **Trovato nel repo:** `scripts/memoria_storica.py` (`pr_dai_merge`, `confronta_memoria`) · `plans/adr/ADR-0137-la-memoria-storica-si-scrive-a-ogni-blocco-di-lavoro-non-solo-al-merge.md`
- **Solo qui:** fatti decisi su card trovati solo nella memoria delle sessioni al 18/11: rilascio 1.1.0 dopo le promozioni del 22-24/11 con card prima del tag; Lychee per le ancore solo su richiesta del DM. 21 righe della memoria rimandano solo a `/mnt/project-files/`. Il confronto dà falsi positivi su nomi di codice fra apici inversi (per esempio `goto`) e non controlla le 311 righe in prosa. Lo SHA 48871bd citato nella nota degli strumenti binari non è un oggetto di git.

### MS-0167 · 2026-11-18 · Kit 4050: quattro errori trovati rileggendo, prima del primo giro

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** ADR-0136
- **Temi:** prove-4050 kit distrobox box-appeso vulkan scheda-integrata powershell bom verifica
- **Origine:** riga del 2026-11-18 «Kit delle prove 4050, rilettura a caccia di errori chiesta dal DM il 18/11» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto il 18/11 di controllare che non ci fossero errori nel kit unito con la #469. CI verde, Codex senza rilievi, Sourcery senza budget: i tre errori sono venuti dalla rilettura. Il box spento che resta appeso su `distrobox enter` era già noto dal 2026-10-10 per `llm-locale` (`box_pronto`), ma il kit non lo applicava ai box `comfyui` e `whisper`. La verifica della trascrizione guardava solo se il log nominava la NVIDIA. Lo script di Windows era senza BOM e non guardava l'uscita di `installa.sh`. Un quarto errore l'ha visto il thread «Preparare le prove sul portatile RTX 4050»: il giorno ricalcolato a ogni script divideva in due cartelle un giro che passa la mezzanotte (`PROVE_GIORNO`).
- **Trovato nel repo:** `scripts/prove-4050/ospite.sh` (`box_avvia`, `nel_box`) · `scripts/prove-4050/verifica.py` (`VRAM_WHISPER_MIB`) · `scripts/prove-4050/trascrizione-gpu.sh` (`vram-durante.txt`) · `scripts/tests/test_prove_4050.py` (`test_box_spento_si_accende_senza_restare_appesi`, `test_trascrizione_sulla_scheda_integrata_e_ko`, `test_script_windows_con_bom`)
- **Solo qui:** la soglia di 400 MiB è una stima mia (il modello q8_0 pesa circa 870 MB), non una misura sulla 4050: se al primo giro la memoria sale meno con la GPU giusta, va abbassata. Divisione dei file col thread «Preparare le prove sul portatile RTX 4050», che ha avuto la stessa richiesta: a lui `lettore-coerenza.sh`, `prosa.sh`, `immagini.sh`, `leggi_ollama.py`, `importa_gemini.py`; `drappo-flux.sh` e `schede-vincolate.sh` non toccati. Controllati e trovati a posto: `kit.sh`, `comune.sh`, `controlla.sh`, `riporta.sh`, `prove.json`.

### MS-0168 · 2026-11-18 · Decodifica vincolata: tre errori dello script corretti prima della misura

- **Data:** 2026-11-18
- **PR:** #473
- **ADR:** —
- **Temi:** document-ai decodifica-vincolata tattiche prova-4050 ollama S8
- **Origine:** riga del 2026-11-18 «Tecnica 3, decodifica vincolata: tre errori dello script della prova corretti prima della misura» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto il 18/11 di ricontrollare la prova della #466 (MS-0161) prima di lanciarla. Il braccio libero perdeva violazioni S8 per l'impaginazione (grassetto, elenco numerato, titoli): 1 su 4 trovate, ora 4 su 4. Il tetto di 700 token troncava il JSON pieno del vincolato: ora 1500 e le troncate si contano. Un campo non testuale faceva cadere lo script. La regola del verdetto è rimasta quella scritta prima.
- **Trovato nel repo:** `plans/esperimenti/decodifica-vincolata-2026-11-17/schede_vincolate.py` (`valido_libero`, `in_markdown`, `GETTONI`) · `plans/esperimenti/decodifica-vincolata-2026-11-17/PIANO.md` · `scripts/tests/test_prove_4050.py` (`TestSchedeVincolate`)
- **Solo qui:** `verifica_scheda` tratta una riga che comincia col grassetto come l'inizio di una sezione: chi scrive tattiche da un modello deve togliere il grassetto prima di S8. Non è provato che l'Ollama del portatile rispetti `maxLength` dello schema.

### MS-0169 · 2026-11-12 · Regola di merge: una PR entra senza un nuovo sì se verde, dichiarata e misurata

- **Data:** 2026-11-12
- **PR:** —
- **ADR:** —
- **Temi:** merge regole processo coordinatore thread
- **Origine:** regola del DM nella chat di progetto (2026-11-12), tenuta solo nella memoria delle sessioni; archiviata dal thread «Rendere obbligatoria la memoria storica»
- **Testo:** una PR di un thread entra su main senza un nuovo sì del DM se valgono tutte e tre: CI verde e mergeable clean; tutti i problemi e le misure dichiarati senza omissioni; un miglioramento misurato contro main. Se manca una condizione non entra e si dice quale. I merge sono in coda unica: il coordinatore li ordina uno alla volta e avvisa i thread che toccano gli stessi file; il thread manda testa e misura prima, SHA e file condivisi dopo, e unisce la sua PR al via del coordinatore. Il thread padre dell'audit tiene la lista delle PR e non unisce più. Restano del DM: canone, tagli di testo, merge verso il repo a monte.
- **Solo qui:** imparato il 2026-11-16: il «via» del coordinatore non è il sì del DM; il merge lo copre questa regola, e lo stato mergeable si legge solo dopo aver tolto la bozza. Prima di unire: grep dei segni di conflitto e `impronte.py --confronta` (non è in CI).
- **Coda:** `rendere-obbligatoria-la-memoria-storica`

### MS-0170 · 2026-11-13 · Le decisioni del DM vanno sempre su card, con scheda, file e riga

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** —
- **Temi:** card decisioni processo coordinatore
- **Origine:** richiesta del DM del 2026-11-13 nel thread delle regole e addendum alle istruzioni di progetto del 2026-11-15
- **Testo:** il 13/11 il DM non trovava nel testo dei messaggi le decisioni che gli venivano chieste: da allora ogni scelta va su una card con la soluzione consigliata e con il nome della scheda, il file e la riga. Dal 15/11 ogni thread che apre una card la segnala subito al coordinatore con una riga; il coordinatore le raccoglie e le porta al DM nel canale, così si gestiscono in un punto solo, e il thread va avanti con ciò che non dipende dalla scelta. Una card si chiude solo con una prova.
- **Coda:** `rendere-obbligatoria-la-memoria-storica`

### MS-0171 · 2026-11-13 · Il rilascio 1.1.0 aspetta le promozioni a stable

- **Data:** 2026-11-13
- **PR:** —
- **ADR:** ADR-0099
- **Temi:** rilascio v110 canali card
- **Origine:** scelta del DM su una card del thread dell'audit settimanale (2026-11-13)
- **Testo:** il rilascio 1.1.0 si fa dopo le promozioni dei canali a stable previste per il 22-24/11 (xdist in testing fino al 22/11, «d» eufonica fino al 24/11). La PR di rilascio parte allora, con una card al DM prima del tag. Rilasciare vuol dire una PR con `## [1.1.0]` in `CHANGELOG.md` e `__version__`.
- **Solo qui:** il controllo delle ancore con Lychee non si adotta di iniziativa: solo se il DM lo chiede (stessa data, stessa riga della memoria).
- **Coda:** `rendere-obbligatoria-la-memoria-storica`

### MS-0172 · 2026-11-13 · Document AI: una tecnica per PR, con misura contro main

- **Data:** 2026-11-13
- **PR:** #398 #416 #418
- **ADR:** ADR-0132
- **Temi:** document-ai xai metodo misura
- **Origine:** indicazione del DM del 2026-11-13 nel thread «Applicare Document AI e Explainable AI», tenuta solo nella memoria delle sessioni
- **Testo:** le tecniche di Document AI si provano una per PR, ognuna con una misura contro main, ed entrano solo se la misura migliora. Per l'Explainable AI il margine stimato è poco. Entrate così: font a colori del repo, PDF/A-2a, provenienza IPTC nelle copie web. Prossima in lista al 13/11: andata e ritorno del testo dei booklet.
- **Coda:** `rendere-obbligatoria-la-memoria-storica`

### MS-0173 · 2026-11-18 · La voce di memoria storica è obbligatoria anche senza PR, con un cancello

- **Data:** 2026-11-18
- **PR:** #471
- **ADR:** ADR-0137 ADR-0138
- **Temi:** memoria-storica coda card thread cancello
- **Origine:** due scelte del DM del 2026-11-18: card nel thread «Rendere obbligatoria la memoria storica» e messaggio nella chat di progetto
- **Testo:** sulla card il DM ha scelto la consigliata: ogni thread scrive la voce in un file suo nella coda `/mnt/project-files/memoria-storica-coda/` e la routine del lunedì la porta nel repo. Nella chat ha poi detto di aggiungere le righe alle istruzioni di progetto (lo ha fatto il coordinatore) e ha chiesto «il cancello di verifica per il punto 3 per superare dall'inizio il limite trovato»: da qui `scripts/memoria_coda.py` (forma delle voci, thread risolti senza voce, piega numerata). Termine di confronto: le regole di memoria del suo progetto di dottorato; di quelle sono entrate qui cercare prima di chiedere, controllare che un documento non sia superato, la voce a fine di ogni blocco e la segnalazione delle discordanze.
- **Solo qui:** il repo del dottorato contiene solo documenti, nessuna configurazione di memoria: il confronto è stato fatto sul testo delle regole incollato dal DM.
- **Coda:** `rendere-obbligatoria-la-memoria-storica`

### MS-0174 · 2026-11-18 · Il cancello della coda della memoria storica

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** ADR-0138 ADR-0137
- **Temi:** memoria-storica coda cancello thread routine
- **Origine:** riga del 2026-11-18 «ADR-0138, il cancello della coda della memoria storica» in `plans/CHANGELOG.md`
- **Testo:** richiesta del DM del 18/11 dopo la scelta della coda per thread: un cancello per il punto 3 di ADR-0137, che era solo regola. `scripts/memoria_coda.py` controlla la forma delle voci in coda (`--check`), dice se un thread ha la sua voce (`--thread`, `--threads` con l'elenco dei thread risolti) e porta le voci nel file storico numerandole (`--piega`), solo se il risultato passa `memoria_storica.py --check`; quest'ultimo ora boccia in CI una testa `### MS-` che non si legge. Prima piega: MS-0169…MS-0173, cinque scelte del DM che stavano solo nella memoria delle sessioni.
- **Trovato nel repo:** `scripts/memoria_coda.py` · `scripts/tests/test_memoria_coda.py` · `plans/adr/ADR-0138-la-coda-della-memoria-storica-ha-un-cancello.md`
- **Solo qui:** misura del 18/11: 13 thread risolti dal 12/11 al 17/11, nessuno con una voce sua; il controllo parte dal 18/11 e non li conta. Il cancello non parte da solo (la CI non vede la cartella condivisa né i thread), non vede una card chiusa in un thread aperto e non giudica il contenuto oltre i 40 caratteri del Testo. Comandi per il coordinatore: `python3 scripts/memoria_coda.py /mnt/project-files/memoria-storica-coda/ --thread "Titolo"` prima di risolvere; per la routine `--check`, `--threads elenco.json`, `--piega` e poi `memoria_storica.py --confronta-memoria`.

### MS-0175 · 2026-10-11 · LLM locale: il DM ha scelto la prova del 12B, mai eseguita

- **Data:** 2026-10-11
- **PR:** #234
- **ADR:** ADR-0089
- **Temi:** llm-locale prosa card prove-4050
- **Origine:** card dell'11/10 nel thread «LLM locale per la prosa» e chiusura del thread del 15/11
- **Testo:** dopo la bocciatura del modello da 4B (voto 40/42%, cieco 0 su 10) il DM ha scelto sulla card «Prova il 12B» (la consigliata) al posto di fermare la linea. La prova non è mai stata eseguita: il thread si è chiuso il 15/11 con la prova in sospeso, e da allora appartiene alle prove sul portatile con la GPU da 6 GB (`scripts/prove-4050/`, riga P04 di `plans/STATO-E-ORDINE-DEI-PIANI.md`). Questione aperta: finché l'archivio dei risultati non viene caricato, ADR-0089 resta senza il confronto fra 4B e 12B, e la bocciatura vale solo per il 4B.
- **Trovato nel repo:** `plans/adr/ADR-0089-un-llm-locale-per-la-prosa-si-misura-prima.md` · `scripts/llm-locale/`
- **Coda:** `llm-locale-per-la-prosa`

### MS-0176 · 2026-10-29 · Immagini in posa: licenze ammesse e niente servizi a pagamento

- **Data:** 2026-10-29
- **PR:** —
- **ADR:** ADR-0015 ADR-0019
- **Temi:** immagini licenze comfyui kaggle
- **Origine:** thread «Immagini dei personaggi in posa con l'AI», risposte del DM del 2026-10-29 e card dello stesso giorno
- **Testo:** due scelte del DM che valgono per ogni lavoro sulle immagini. (1) Le licenze con soglia di fatturato (uso commerciale sotto 5 milioni di dollari, come FLUX 3 Klein) sono usabili, con quattro vincoli: revisione umana, dichiarazione che l'immagine è fatta con l'AI, nessun addestramento sulle uscite, la licenza può essere revocata. (2) Non si paga: solo GPU locale da almeno 10 GB o Kaggle gratuito (scelto su card), mai servizi a pagamento lanciati in automatico; come ultima via automatica il profilo «sola CPU» (SD1.5 con LCM-LoRA, 12-15 minuti a scena, 16 GB di RAM), buono per bozze di posa e non per il tavolo. Licenze verificate quel giorno: non commerciali OpenPose CMU, InsightFace (InstantID, PuLID, IP-Adapter FaceID), Qwen-Image-2.1, FLUX.2 klein 9B; Apache 2.0 DWPose, Qwen-Image-Edit-2511, FLUX.2 klein 4B, Z-Image-Turbo, MOSS-Image. La regola del DM: chi non ha una GPU adeguata usa la migliore via gratuita in rete, mai una a pagamento; il profilo «sola CPU» l'ha chiesto il DM. Ordine di priorità (le pagine con un'illustrazione erano il 17% contro il 40% dei moduli Paizo presi a confronto): prima i ritratti scontornati dei PNG con scheda intera, poi PNG ricorrenti e cattivi, per ultime le scene coi PG.
- **Fuori dal repo:** `/mnt/project-files/immagini-personaggi/pipeline-2026-10-29/` (sei fasi, banco di misura, backend GPU locale → Kaggle → CPU) e `prove-2026-10-29/`
- **Solo qui:** i pesi ripubblicati da terzi perdono l'etichetta di licenza, quindi il registro dei pesi punta sempre all'origine. Misure del banco su CPU: riconosce un altro PG e le scritte, non riconosce una mano rovinata (0,78); le due scene di prova bocciate per identità (0,33 e 0,50) con la posa a 0,996.
- **Coda:** `immagini-dei-personaggi-in-posa-con-l-ai`

### MS-0177 · 2026-10-31 · Immagini in posa: la prova con Gemini si fa a mano, e non è mai stata misurata

- **Data:** 2026-10-31
- **PR:** —
- **ADR:** —
- **Temi:** immagini gemini card
- **Origine:** card del 2026-10-31 nel thread «Immagini dei personaggi in posa con l'AI»
- **Testo:** sulla card il DM ha scelto la prova a mano dall'app, gratis (la consigliata), contro la via automatica da circa 4 dollari. Il piano del DM non include crediti per l'API, quindi la via automatica sarebbe a pagamento e richiede un sì esplicito. Come seconda fonte a mano il DM ha indicato ChatGPT gratuito. Pronti e mai usati: lo script automatico con tetto di spesa e 14 casi (8 PG in posa, 3 ritratti di PNG, 3 seconde pose) e i prompt per la prova a mano con busti e scheletri. Questione aperta: le immagini fatte a mano non sono mai state caricate, quindi il confronto con SD1.5 e con gli originali non esiste. La licenza commerciale delle uscite di Gemini non è stata verificata.
- **Fuori dal repo:** `/mnt/project-files/immagini-personaggi/pipeline-2026-10-29/gemini/` (`gemini_ritratti.py`, `casi_gemini.json`, `PROMPT-A-MANO.md`)
- **Coda:** `immagini-dei-personaggi-in-posa-con-l-ai`

### MS-0178 · 2026-11-08 · Immagini in posa: revisione con gli standard di fatto, ADR-0115 mai prenotato

- **Data:** 2026-11-08
- **PR:** —
- **ADR:** ADR-0115 ADR-0114
- **Temi:** immagini adr standard-di-fatto
- **Origine:** thread «Immagini dei personaggi in posa con l'AI», revisione dell'8/11 dopo l'allineamento del coordinatore
- **Testo:** la proposta (prima ADR-0104, numero mai prenotato e poi usato da altri) prende il numero ADR-0115 e cambia in tre punti per la regola dello standard di fatto: la posa si misura con l'OKS di COCO al posto del coseno degli arti; lo scontorno passa a rembg al posto di BiRefNet a mano; il giudice dei glitch scritto da noi resta solo se batte VQAScore. In più i nodi ComfyUI vanno fissati a un commit e il prompt dell'immagine sta nella scheda di ADR-0015. Stato delle decisioni: D2 chiusa, D3 chiusa in parte, D1 (prima PR leggera, senza generazione in CI) e D4 aperte al DM. Questione aperta: ADR-0115 non è in `plans/adr-prenotati.json` e il file dell'ADR non esiste, ma il repo lo cita come proposta in `plans/esperimenti/immagini-posa-4050-2026-11-15/LEGGIMI.md` riga 10 e in `scripts/prove-4050/immagini.sh` riga 3; chi riprende il lavoro deve prenotare un numero libero e correggere i due rimandi.
- **Solo qui:** nessuna delle tre sostituzioni (OKS, rembg, VQAScore) è stata misurata: sono scelte di metodo, non risultati.
- **Coda:** `immagini-dei-personaggi-in-posa-con-l-ai`

### MS-0179 · 2026-11-12 · La revisione dei bot non è una condizione di merge

- **Data:** 2026-11-12
- **PR:** #379 #381
- **ADR:** ADR-0127
- **Temi:** merge revisione sourcery codex regola
- **Origine:** messaggi del coordinatore nel thread «Salvare la memoria storica nel repo», 2026-11-12
- **Testo:** sulla #379 la revisione di Sourcery è arrivata otto minuti dopo il merge con 2 rilievi veri su 10. Il coordinatore ha prima chiesto di aspettare la revisione sulla #381, poi ha ritirato la condizione: la revisione dei bot non fa parte della regola di merge del DM del 12/11, e col budget dei bot esaurito per due giorni avrebbe fermato tutta la coda. Da allora ogni PR dichiara nel corpo se Sourcery e Codex hanno revisionato, e i rilievi veri di una revisione arrivata dopo il merge vanno in una PR di seguito. È una regola del coordinatore, non una scelta del DM su card.
- **Solo qui:** dal 12/11 i due bot di fatto non revisionano; nessuna misura dice quanti rilievi veri si sono persi così.
- **Coda:** `salvare-la-memoria-storica-nel-repo`

### MS-0180 · 2026-11-15 · Il bug dei tag PDF/UA di typst 0.15.1 dipende dall'impaginazione

- **Data:** 2026-11-15
- **PR:** #448
- **ADR:** ADR-0129
- **Temi:** typst pdfua stampa booklet diagnosi
- **Origine:** thread «Rendere dinamica la tattica di Skullcrusher», intoppo in CI sulla #448
- **Testo:** la stampa del booklet della serata falliva in CI per un errore interno di typst 0.15.1 sui tag di accessibilità («tags weren't properly closed»), che compare solo quando un'interruzione di pagina cade in un certo punto. Il motore lo riportava con un messaggio fuorviante, come se il binario typst non fosse nel PATH. A spostare la pagina era il capoverso di B13, diventato più lungo; è stato diviso in tre senza cambiare parole. Il bug può tornare con qualunque modifica che sposti le pagine di un booklet. Come si trova: applicare i pezzi del diff uno alla volta al `.typ` di main finché la compilazione cade.
- **Solo qui:** il messaggio sbagliato del motore non è stato corretto; chi vede «typst non nel PATH» in CI con typst installato deve pensare prima a questo bug.
- **Coda:** `rendere-dinamica-la-tattica-di-skullcrusher`

### MS-0181 · 2026-11-18 · Il ricontrollo delle prove 4050: sette errori negli script di lettore, immagini e Gemini

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** —
- **Temi:** prove-4050 comfyui lowvram immagini lettore ollama gemini takeout ricontrollo errori
- **Origine:** riga del 2026-11-18 «Prove sulla RTX 4050, ricontrollo chiesto dal DM il 18/11» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto il 18/11 di ricontrollare gli errori e correggerli, a questo thread (#447) e a quello del kit (#469). I due thread si sono divisi i file: qui lettore, prosa, immagini, la pipeline delle immagini, `leggi_ollama.py` e `importa_gemini.py`; al thread del kit il resto. L'errore più grave: `immagini.sh --profilo cpu`, che la guida dà come confronto col 29/10 «sulla GPU», passava a ComfyUI `--cpu` e `--lowvram` insieme. Stanno nello stesso gruppo esclusivo e ComfyUI esce subito; lo script aspettava sei minuti e diceva «non parte». Lo stesso errore era già stato trovato in `drappo_flux.py` (commit 03ca93f7) e non riportato qui. Ora il profilo leggero gira sulla GPU (`RS_COMFY_DEVICE=gpu`) e senza `--lowvram`.
- **Trovato nel repo:** `scripts/prove-4050/immagini.sh` · `plans/esperimenti/immagini-posa-4050-2026-11-15/dati/esegui_gpu.py` (`argomenti_comfy`, `avvia`) · `plans/esperimenti/grafo-eventi-2026-11-12/leggi_ollama.py` · `scripts/importa_gemini.py` (`ora_iso`, `_di_gemini`) · `scripts/tests/test_prove_4050_correzioni.py`
- **Solo qui:** niente di tutto questo è girato su una GPU: le correzioni sono provate con server finti e leggendo gli argomenti. Controllato e trovato a posto: le 636 domande del lettore sono lunghe al massimo 981 caratteri, quindi il contesto 4096 del kit non le taglia. Tolto anche un rimando a «ADR-0115 (proposta)» in `immagini.sh` e nel LEGGIMI delle immagini: il numero non è prenotato e il file non esiste, l'aveva scritto questo thread nella #447 senza controllarlo (trovato dal thread della memoria storica). Segnalato dal thread FLUX e verificato sulla fonte: `immagini.sh` e `scripts/comfyui-local/setup-distrobox.sh` installavano PyTorch dall'indice cu124, che si ferma alla 2.6.0 (`pip install --dry-run` del 18/11: torch 2.6.0+cu124, torchvision 0.21.0); il README del ComfyUI fissato (0df1646) dà la 2.7 come minimo e `main.py` avvisa sotto la 2.8. Ora cu126 (lo stesso dry-run: torch 2.14.1+cu126, torchvision 0.29.1), e un venv con la 2.6 viene aggiornato. Tolto torchaudio, aggiunto per errore in questa stessa PR: su cu126 è fermo alla 2.11 e avrebbe riportato indietro torch. Segnalato al thread del kit e non toccato: `comune.sh` calcola il giorno a ogni script, e un `kit.sh tutte` che passa la mezzanotte (il giro stimato supera le sei ore) divide i risultati su due cartelle (corretto dal thread del kit nella #474, MS-0167).

### MS-0182 · 2026-11-18 · D2 del Drappo: quattro difetti dello script FLUX trovati al ricontrollo

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** —
- **Temi:** drappo immagini flux comfyui prove-4050 pillow c2pa pytorch regressione
- **Origine:** riga del 2026-11-18 «D2, collaudo dell'arte del Drappo: quattro difetti dello script trovati al ricontrollo» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto il 18/11 di ricontrollare tutto il thread. La prova su CPU del 16/11 (MS-0156) aveva usato solo ritratto-vanna, l'unica delle tre Gemini di serie che Pillow apre senza ritocchi: tavola-la-ruota e il-drappo hanno il manifesto C2PA in un blocco di testo oltre `PngImagePlugin.MAX_TEXT_CHUNK` e davano `ValueError`, dopo le generazioni e prima di `riepilogo.json`. Trovato rifacendo la prova su CPU con il-drappo (593 s, RAM di ComfyUI al picco 12.962 MiB). Gli altri tre: clone di ComfyUI condiviso con `esegui_gpu.py`, che clona i nodi ControlNet e IP-Adapter solo se la cartella non esiste (ora `ComfyUI-flux`); indice PyTorch `cu124` fermo al 2.6.0, mentre ComfyUI `0df1646` sotto la 2.8 ripiega sul vecchio ModelPatcher e avverte che le stime di VRAM non sono affidabili (ora `cu126`, 2.14.1 al 18/11); `set -o pipefail` che chiudeva `drappo-flux.sh` prima dell'esito.
- **Trovato nel repo:** `scripts/prove-4050/drappo_flux.py` (`affianca`, `prepara`, `torch_vecchio`) · `scripts/prove-4050/drappo-flux.sh` · `scripts/tests/test_prove_4050.py` (`TestDrappoFlux`) · `docs/how-to/GUIDA-PROVE-PORTATILE-4050.md` §3-bis
- **Solo qui:** `immagini.sh` e `scripts/comfyui-local/setup-distrobox.sh` installavano anch'essi PyTorch da `cu124`: segnalato al coordinatore, corretti da un'altra PR prima di questa (`RS_TORCH_INDEX`, che ora legge anche `drappo-flux.sh`). Nella prova su CPU FLUX klein ha mancato il soggetto di il-drappo (uno stendardo bianco appeso sopra una corsa, non il drappo dipinto come oggetto): è un solo seme su CPU, con prompt scritti per SDXL, e non decide la D2. Corrette anche due affermazioni fatte al DM nel thread: FLUX.2 [dev] (64 GB) non entra intero in una L40S da 48 GB, e Qwen-Image non entra nelle GPU da 16 GB di Kaggle.

### MS-0183 · 2026-11-18 · La scuola di tutti gli incantesimi delle liste PF1e

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** generatore talenti incantesimi scuole spell-focus pf1e prd ricontrollo
- **Origine:** riga del 2026-11-18 «ADR-0126, ricontrollo di Incantesimi focalizzati» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto il 18/11 di ricontrollare #468 e #470. Cancelli e impronta erano verdi; il difetto rimasto era quello dichiarato nella #468: 912 voci su 8548 delle liste PF1e senza scuola. Su 945 PNG a classi, 693 incantesimi su 5553 restavano fuori dal conto, 168 blocchi sceglievano la scuola su una parte sola e 59 perdevano il talento. Ora `[scuole]` sta anche in `liste_incantesimi.toml` del PF1e, 1536 incantesimi dal PRD: 0 senza scuola e 0 blocchi parziali. Incantesimi focalizzati passa da 621 a 665, tutti con la scuola: tornano i 44 che l'alchimista perdeva.
- **Trovato nel repo:** `plans/esperimenti/sistemi-plugin-2026-11-07/estrai_prd_pf1e.py` (`liste_incantesimi`) · `scripts/genera_creatura.py` (`_scuole_per_nome`) · `scripts/tests/test_talenti.py` (`Focalizzati`)
- **Solo qui:** fra SRD 3.5 e PRD i 598 nomi comuni hanno la stessa scuola, per questo la tabella di ricerca è una sola per i due sistemi. I 5 incantesimi «universal» non danno scuola. L'impronta delle 720 creature non cambia: i PNG PF1e a classi non ci sono dentro.

### MS-0184 · 2026-11-18 · RICERCA-TOOL-LGM-2026 §3.1: la carta del cielo passa dal 30 Mirtul al 30 Flamerule

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** ADR-0005 ADR-0019
- **Temi:** arc09 handout immagini calendario canone
- **Origine:** riga del 2026-11-18 «§3.1, ricontrollo della carta del cielo chiesto dal DM» in `plans/CHANGELOG.md`
- **Testo:** Jfs, 2026-11-18: «ricontrolla se ci sono errori e fixali». Il ricontrollo ha trovato che i file di ARC-09 dicono «fine Mirtul» per il Giorno 30, mentre la decisione del DM del 2026-07-12 fissa Giorno di Marcia 1 = 1 Flamerule. Sulla card Jfs ha scelto «30 Flamerule: rifaccio la carta». Carta rifatta: 2000-07-31 00:05:45 UT a longitudine 0, stella-chiave HIP 102098 allo zenit a latitudine 45,281.
- **Trovato nel repo:** `09_…/Immagini-Handout/carta-del-cielo/PROVENIENZA.txt` · handout 7 in `Arco-Post-Hammerfist-HANDOUTS.md` · A4 in `Arco-Post-Hammerfist-DOSSIER-DELLE-PISTE.md`
- **Solo qui:** la voce è nata MS-0166 ed è diventata MS-0184 al riallineo su main 4588bc5f. Vicino all'ascensione retta giusta non c'è una stella alla declinazione di prima (38,9°): per questo cambiano anche la latitudine e il parallelo, che ora passa per l'angolo ovest del Sigillo e non più per l'Anello. I «circa nove gradi» del 22 del mese restano giusti: otto notti più il grado e mezzo che manca a mezzanotte esatta. Il primo lancio di Stellarium dopo aver copiato una cultura del cielo nuova differisce dai successivi di un livello di grigio in circa 1800 pixel, quasi tutti fuori dall'orizzonte; i quattro lanci dopo sono identici. Gli altri «Mirtul» di ARC-09 (HOOKS, INTEGRATION-MASTER, Cerimonia, Tempestas) non sono toccati qui: li prende il thread della coerenza della storia.

### MS-0185 · 2026-11-18 · Le impronte rosse dal 14/11 erano dati, provato incrociando codice e dati

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** ADR-0111
- **Temi:** impronte banco-invarianza regressione prova-incrociata audit indice piani
- **Origine:** riga del 2026-11-18 «Correzioni dall'audit del 18/11» in `plans/CHANGELOG.md`
- **Testo:** l'audit del 18/11 trovava `impronte.py --confronta` rosso su suggest_encounter, conformita_statblocchi e derive_statblocks dal 16/11, con le impronte ferme a 2f48498b (14/11). Prima di rigenerarle si è provato che il comportamento degli strumenti non è cambiato: due worktree incrociati, uno coi dati del 14/11 e i `*.py` di `scripts/` e `sistemi/` di main, l'altro coi dati di main e il codice del 14/11. Il primo ridà le impronte del 14/11, il secondo quelle di main, per 11 strumenti su 12. Il dodicesimo, validate_bestiario, è rosso in tutti e due perché `build_monster_catalog.py` tiene nel codice l'elenco dei nomi degli Eroi di Hammerfist, cambiati dal DM: il catalogo generato non torna se si mescolano codice e dati di date diverse. Su main non cambia. Le differenze dei tre rossi: catalogo da 390 a 392 voci (Ragnhild, Yrsa, Saraah, lo scheletro di leone crudele GS 7, Tyrgarun molto vecchio), una scheda in più verificabile, il corredo RC-001 dell'hobgoblin regolare.
- **Trovato nel repo:** `plans/esperimenti/sistemi-plugin-2026-11-07/impronte.py` · `plans/esperimenti/sistemi-plugin-2026-11-07/IMPRONTE.json`
- **Solo qui:** il metodo della prova (dati vecchi e codice nuovo, poi il contrario, con i file YAML e TSV di `scripts/` dalla parte dei dati) serve a ogni futura rigenerazione del banco. Residuo, non corretto qui perché è codice fuori dal perimetro: la scheda dell'hobgoblin regolare torna (Warrior 3 base Vol +1, Sag 9 −1, mantello della resistenza +1 = Vol +1), ma `conformita_statblocchi` (`talenti()`) legge anche la «Volontà di Ferro» della riga della variante «Combattente GS2» e si aspetta +3; lo conta fra gli «uguali alla fonte» con Vol +1≠3 (prima del corredo RC-001, +1≠2).

### MS-0186 · 2026-11-18 · Kit 4050: sandbox Flatpak al primo giro, installazione interrotta al secondo

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** ADR-0136
- **Temi:** prove-4050 kit flatpak sandbox ospite verifica primo-giro asus pulisci box-a-meta installazione-interrotta stty terminale-grezzo scaletta
- **Origine:** riga del 2026-11-18 «Kit delle prove 4050, primo giro del DM sull'ASUS» in `plans/CHANGELOG.md`
- **Testo:** il 18/11 sera il DM ha lanciato il kit sull'ASUS (main 1295e3a8) e ha caricato il log nel thread «Preparare le prove sul portatile RTX 4050». Il kit vedeva «sistema: altro 25.08» in modo box, senza nvidia-smi, distrobox e podman; il prompt era `sh-5.3$`. 25.08 è la versione del runtime Freedesktop: il terminale era quello di un'applicazione Flatpak, non quello di Bazzite. Il kit ora lo riconosce e si ferma con le istruzioni. Lo stesso log ha mostrato che la verifica chiamava «non fatta» il lettore, che invece era stato lanciato ed era uscito con 3. Al secondo giro, dal terminale del sistema, il kit ha riconosciuto Bazzite e la 4050; il DM ha però dovuto spegnere la macchina mentre il box `comfyui` si inizializzava e ha chiesto come ripartire pulito («non c'è nemmeno questa opzione»). Aggiunti `kit.sh pulisci` (conferma, poi toglie i box; modelli, pesi e risultati stanno fuori dai box e restano) e in `installa.sh` il giro che toglie e rifà un box il cui log non ha mai scritto «container_setup_done». Al terzo giro l'installazione è arrivata in fondo e `controlla` e `lettore-coerenza` sono andate; spento Ollama, il terminale restava in modalità grezza e la verifica usciva a scaletta: `kit.sh` ora fa `stty sane` (`terminale_a_posto`), solo se l'uscita è un terminale.
- **Trovato nel repo:** `scripts/prove-4050/ospite.sh` (`rs_sandbox`, `rs_ferma_se_sandbox`, `box_a_meta`, `box_togli`) · `scripts/prove-4050/kit.sh` (`pulisci`) · `scripts/prove-4050/installa.sh` · `scripts/prove-4050/comune.sh` · `scripts/prove-4050/verifica.py` · `scripts/tests/test_prove_4050.py` (`test_sandbox_flatpak_ferma_subito`, `test_prova_lanciata_e_mai_partita_e_ko`, `test_box_rimasto_a_meta_si_riconosce`, `test_pulisci_chiede_conferma_e_lascia_i_dati`, `test_terminale_rimesso_a_posto_dopo_il_server`)
- **Solo qui:** la sandbox era una deduzione del thread «Preparare le prove sul portatile RTX 4050» dal log; il secondo giro dall'host l'ha confermata (riferito dal coordinatore). A mano, prima di `pulisci`: `distrobox rm --force comfyui whisper`, poi `kit.sh installa`. Un box acceso col log vuoto (driver dei log spento) non viene giudicato a metà, per non rifarlo a ogni `installa`. `pulisci` e `box_a_meta` sono provati solo con podman e distrobox finti. Non riconosciuti di proposito: un terminale dentro un Distrobox o un toolbox (lì `/run/.containerenv` c'è, ma c'è anche nei container dove girano i test) e Snap. `flatpak-spawn --host` funziona solo se l'applicazione ha il permesso `org.freedesktop.Flatpak`.

### MS-0187 · 2026-11-19 · Il talento di una variante non è della scheda: falso positivo di conformita_statblocchi

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** conformita statblocchi talenti variante hobgoblin falso-positivo impronte audit
- **Origine:** riga del 2026-11-19 «`conformita_statblocchi`: il talento di una riga di variante» in `plans/CHANGELOG.md`
- **Testo:** residuo dichiarato in MS-0185. L'hobgoblin regolare usciva fra gli «uguali alla fonte» con Vol +1≠3. La scheda è giusta: Warrior 3 base Vol +1, Sag 9 −1, mantello della resistenza +1, totale +1. Lo strumento contava anche la Volontà di Ferro, scritta solo nella riga della variante «Combattente GS2» («Volontà di Ferro al posto di Arma Focalizzata»). `talenti()` ora salta le righe di variante. Lo stesso talento falso arrivava a `genera_attributi` da `tetti_dai_ts` e produceva sulla scheda l'avviso «Sag al più 5 ricavata da Vol +1 (base +4)»; con `--rigenera` la riga `[GENERATO]` perde l'avviso, le caratteristiche non cambiano. Il coordinatore ha chiesto la correzione come PR a parte dopo la #476, con un test che fallisce su main.
- **Trovato nel repo:** `scripts/dmcore/lettura_creatura.py` (`talenti`, `VARIANTE`) · `scripts/tests/test_conformita_statblocchi.py` (`test_il_talento_di_una_variante_non_e_della_scheda`)
- **Solo qui:** la CI ha fermato la prima testa su `test_impronta_creature`: la fixture va rigenerata in un commit suo che dice le chiavi (18, tutte dell'hobgoblin regolare o dei riepiloghi; taratura sulle fonti 1,24 → 1,21, Sag 1,38 → 1,19). In locale quel test non era stato lanciato. Provata e scartata la strada più larga, togliere le righe di variante in `senza_note()`: faceva comparire un falso «da correggere» su Ghaurush Cenerevento (CA della variante «Cenere Piena», +22≠26), perché altri lettori usano quella riga. Le righe di variante nel Bestiario sono 5 (Koth, Ghaurush, Kulkorzhul war adept, duergar mago-ladro, hobgoblin regolare); solo quella dell'hobgoblin nomina un talento che il conto conosce.
### MS-0188 · 2026-11-18 · ADR-0134: ricontrollo del corredo di dieci schede, quattro note corrette

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** ADR-0134
- **Temi:** schede equipaggiamento regole drow ricontrollo
- **Origine:** riga del 2026-11-18 «ADR-0134, regola RC-001: ricontrollo del corredo di dieci schede» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto il 18/11 di ricontrollare e correggere. Rifatti a mano prezzi, CA e attacchi delle dieci schede di MS-0140 e MS-0154: tornano tutti. Corretti: la spiegazione del contatto 12 di Dovil (il limite di Destrezza dell'armatura completa vale anche al contatto); il tetto di Drow Assassina e Drow Chierica del Palio, ora al livello effettivo 11 (21.000 mo) invece che al 9° (12.000); dieci quadrelli alla balestra a mano della Drow Assassina e alla balestra leggera di Therysol (30.436 mo). Sulla card del 18/11 il DM ha scelto la balestra a mano perfetta per la Drow Assassina: attacco a distanza +12, +13 entro 9 m con Tiro Ravvicinato; corredo 10.811 mo su 21.000.
- **Trovato nel repo:** `ADR-0134` → `plans/adr/ADR-0134-l-equipaggiamento-standard-viene-dai-codex-pf1e-entro-il-valore-del-3-5.md`
- **Solo qui:** visti e non toccati, perché sono numeri delle schede o scelte del DM: l'attacco a distanza +13 della Drow Assassina tornava solo con una balestra a mano perfetta ed entro 9 m (attacco base +6, Des +5, perfetta +1, Tiro Ravvicinato +1), mentre il corredo aveva una balestra normale: il DM ha scelto sulla card del 18/11 nel thread del volume (nel primo giro Tiro Ravvicinato era stato dimenticato e la prima card, nel canale del coordinatore, partiva da quel conto sbagliato); Tiro Ravvicinato dà anche +1 ai danni entro 9 m e la riga non lo scrive (non era sulla card); la tabella in prosa di Varis non elenca il giaco di cuoio borchiato +1 e il pugnale +1 che il blocco ora ha; `verifica_scheda` conta una sola perla per grado a Therysol (25.435 mo, è un minimo). I quadrelli non erano su nessuna card: aggiunti perché l'arma è nella riga d'attacco.

### MS-0189 · 2026-11-18 · Sei frasi del lotto 5 delle tattiche corrette contro la loro fonte

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** —
- **Temi:** tattiche villain palio ghostlord collezionista arc09 errori rilettura inferred
- **Origine:** riga del 2026-11-18 «Tattiche di villain e PNG, ARC-09 lotto 5: sei frasi corrette dopo la rilettura chiesta dal DM» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto di ricontrollare. I cancelli erano verdi e le misure di Azarr Kul, Ushgar e Zarim si ripetono uguali, ma la rilettura dei testi della #465 contro le schede ha trovato sei frasi sbagliate: nel Palio i sicari «colpivano per primo la guardia», contro l'obiettivo scritto una riga sopra, e due dettagli della notte del Giorno 2 erano inventati; nel Ghostlord c'erano un «Cerchio» e un «patto» che la scheda non ha; nel Collezionista la conseguenza del furto di Tordek diceva più della scheda.
- **Trovato nel repo:** i tre file della riga del changelog, ognuno con il blocco `<!-- storico -->` che riporta la frase di prima
- **Solo qui:** erano frasi marcate INFERRED, e la marca copriva la deduzione ma non la contraddizione con la fonte. Un testo INFERRED va comunque riletto contro la scheda da cui parte. I lotti 1-4 (#449, #452, #453, #454, #463) sono stati riletti solo nelle righe aggiunte, senza trovare contraddizioni; non è una rilettura completa da DM.

### MS-0190 · 2026-11-18 · Calendario di ARC-09: quickstart e armate allineati a state.yaml

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** ADR-0125
- **Temi:** calendario arc-09 torneo dauth finestre quickstart armate decisione-dm coerenza-storia
- **Origine:** riga del 2026-11-18 «Calendario di ARC-09» in `plans/CHANGELOG.md`
- **Testo:** due calendari di ARC-09 non coincidevano. `P2B-Torneo-DAUTH-DM-MASTER-REFERENCE` §1.1 (autoritativa) e `campaign/state.md` r.381 mettono i tre giorni del Torneo di Dauth ai Day 30-32, e `state.yaml` dà solo le finestre delle fasi (Torneo Day 25-34); il quickstart e la tabella delle armate (§4b) dicevano Day 26-30, con finestre più strette per P1, Rhest, Torre e Mercante. Il DM ha scelto che vale `state.yaml`: P1 Day 20-30, Rhest 25-32, Torre 28-35, Torneo 25-34 con i tre giorni ai Day 30-32, Mercante 28-36
- **Trovato nel repo:** `campaign/DM-QUICKSTART-ARC09.md` · `00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md` · `campaign/state.yaml` · `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DM-MASTER-REFERENCE.md`
- **Solo qui:** l'ha trovata una delle tre «contraddizioni candidate» sui giorni del verificatore; le altre due, e ciò che resta della prima, sono falsi allarmi perché il confronto mette insieme fasi diverse della stessa entità e il giorno del torneo col Giorno di Marcia. Nella tabella dello scheduling una riga con due finestre fa nascere un falso allarme nuovo: una finestra per riga. La card citava `state.yaml` come fonte dei Day 30-32: il thread dell'audit ha fatto notare che lì c'è solo la finestra, e la fonte giusta è la tabella §1.1 del master del Torneo. I «Mirtul» rimasti in ARC-09 dopo la scelta «Giorno 1 = 1° Flamerule» sono fuori da questa voce e aspettano una card a parte

### MS-0191 · 2026-11-18 · I «Mirtul» rimasti in ARC-09 diventano «Flamerule», con un cancello

- **Data:** 2026-11-18
- **PR:** —
- **ADR:** ADR-0125
- **Temi:** calendario arc-09 mirtul flamerule torre-invisibile lettera-brenna tempestas decisione-dm cancello
- **Origine:** riga del 2026-11-18 «Calendario di ARC-09: i «Mirtul» rimasti» in `plans/CHANGELOG.md`
- **Testo:** il DM ha confermato sulla card della carta del cielo che vale l'ancora del 12/07: Giorno di Marcia 1 = 1° Flamerule, e la Torre cammina la notte del 30 Flamerule. Restavano 31 «Mirtul» in 9 file: la scadenza «fine Mirtul, poi la torre cammina» nei file degli agganci, nel dossier delle piste, nella Cerimonia delle 100 Asce, nella scheda di Tempestas e in `state.yaml`, più la data della lettera di Brenna. Il DM ha scelto di correggerli tutti, lettera compresa: ora è datata «il diciannovesimo di Flamerule»
- **Trovato nel repo:** `scripts/tests/test_calendario_flamerule.py` · `campaign/state.yaml` (riga di Tempestas in `conoscenze`) · `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-HOOKS-Artemis-TorreInvisibile.md` · `scripts/session_recap.py` (`MARCH_DAY1_HARPTOS`)
- **Solo qui:** il coordinatore aveva chiesto di distinguere i «Mirtul» compatibili da quelli in contrasto: letti uno per uno, nessuno era compatibile, perché tutti legano il mese al Giorno 30 o al dopo-Hammerfist. La regola pensata all'inizio (mese scritto contro Giorno di Marcia, riga per riga) non è stata scritta: il cancello cerca solo la parola «Mirtul» nei testi di gioco, e non vede una data sbagliata scritta con un altro mese. Restano fuori `campaign/state-changelog.md`, che è storia, e i riferimenti di lore in `skills/`

### MS-0192 · 2026-11-19 · Il lettore da 7B sulla RTX 4050 non entra nel verificatore della storia

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0125
- **Temi:** coerenza-storia rag lettore qwen2.5 7b rtx-4050 ollama prova-4050 esito-negativo
- **Origine:** riga del 2026-11-19 «Lettore del RAG per «chi sa cosa»» in `plans/CHANGELOG.md`
- **Testo:** il DM ha lanciato il kit sull'ASUS: `qwen2.5:7b` a 4 bit via Ollama, 636 risposte su 636 in circa 2 minuti. Il criterio fissato il 12/11 (90% di SÌ sulle domande giuste, al massimo 5% col PNG sbagliato, 70% di precisione su main) non è raggiunto. Il 7B dice SÌ a 499 candidati su 560 su main e a 78 domande su 79 sulle righe dei mutanti: li trova (21 su 25) perché dice SÌ quasi a tutto. Il RAG resta fuori dal verificatore
- **Trovato nel repo:** `plans/esperimenti/grafo-eventi-2026-11-12/ESITO.md` · `plans/esperimenti/grafo-eventi-2026-11-12/misure/risposte-qwen2.5-7b.json` · `plans/esperimenti/grafo-eventi-2026-11-12/leggi_ollama.py`
- **Solo qui:** le letture complete (`main-rag-7b.json`, `mut-rag-7b.json`) e l'archivio del kit stanno in `/mnt/project-files/prove-4050-risultati/2026-11-19/`, fuori dal repo. Le 302 righe segnalate su main non sono state lette una per una: sei prese a caso erano false. Il 3B sbagliava per troppi NO, il 7B per troppi SÌ; riprovare ha senso solo cambiando la domanda al lettore, e il 12B non sta nei 6 GB della 4050

### MS-0193 · 2026-11-19 · La memoria corta passa il limite: il tetto di 12 KB diventa un controllo

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0139
- **Temi:** memoria memoria-storica cancello tetto processo
- **Origine:** riga del 2026-11-19 «ADR-0139: la memoria corta ha un tetto» in `plans/CHANGELOG.md`
- **Testo:** il DM ha trovato l'indice della memoria delle sessioni a 16.878 byte, oltre il limite di 16.384, e ha chiesto perché la memoria storica non l'avesse evitato. Causa: ADR-0127 e ADR-0137 obbligano ad archiviare prima di togliere ma non a togliere, e nessun controllo misurava i byte; i thread chiudevano aggiungendo una riga «unita il …» invece di togliere la loro riga di stato (8 KB il 12/11, +8,8 KB in sette giorni). Indice riscritto a 11.255 byte dopo aver verificato che le 18 PR citate hanno tutte una voce; `memoria_storica.py --tetto-memoria DIR` esce 1 sopra i 12 KB e mostra le righe più lunghe, lanciato dalla routine del lunedì e dal coordinatore dopo ogni modifica dell'indice (scelta del DM sulla card del 19/11)
- **Trovato nel repo:** `scripts/memoria_storica.py` · `scripts/tests/test_memoria_storica.py` · `plans/adr/ADR-0139-la-memoria-corta-ha-un-tetto-misurato.md`
- **Solo qui:** le righe tolte senza un posto nel repo sono nella coda del thread («riportare-la-memoria-sotto-il-limite.md»): numerazione MS del 13/11 ormai superata, coda dei merge del 13/11, card sulle copie del booklet della serata forse superata da MS-0097 ma di chiusura non vista. Il controllo non parte da solo e non misura le note
### MS-0194 · 2026-11-19 · La configurazione Claude del repo non arrivava nei thread del progetto

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0140
- **Temi:** claude-code best-practice thread hook claude-md agents-md mcp rumblingstone-tools contesto token skilloverrides
- **Origine:** riga del 2026-11-19 «ADR-0140 (proposta), la configurazione Claude del repo arriva anche nei thread» in `plans/CHANGELOG.md`
- **Testo:** audit delle best practice di Claude Code chiesto dal DM. Nei thread Claude parte in `/home/user`, la cartella che contiene il clone: AGENTS.md fuori dal contesto, hook SessionStart mai girato, `dnd-35-rules` legacy non spenta, `rumblingstone-tools` assente. Il thread del 19/11 è partito con 131.128 token di contesto; circa 113.000 caratteri venivano da plugin e connettori dell'account estranei al progetto. Già coperte e non rifatte: piani e ADR, MEMORIA.md e memoria storica (vanno oltre il «Document & Clear» dell'articolo), 3.289 test e circa 60 cancelli, un thread per compito
- **Trovato nel repo:** `plans/adr/ADR-0140-la-configurazione-claude-del-repo-arriva-anche-nei-thread.md` · `scripts/claude-progetto.sh` · `scripts/tests/test_claude_progetto.py`
- **Solo qui:** l'audit con la tabella pratica per pratica sta in `/mnt/project-files/best-practice-claude-code-2026-11-19/AUDIT.md`. Le cifre dell'articolo (33%, 150-200 istruzioni, 60% del contesto) sono di terzi e non sono state usate come obiettivi. AGENTS.md dice 77 tool per `rumblingstone-tools`, il server ne espone 135 e il manifest ne elenca 144: non corretto in questa PR. Delle ultime 100 corse CI sulle PR (15-19/11) 14 sono fallite, cause non classificate; il passo pytest dura circa 17 minuti. Scelte del DM sulle card del 19/11: config del repo nei thread; regole `deny` per dieci connettori inutilizzati (tolti dal thread appena scritto il settings generato); i plugin da spegnere erano ancora in attesa

### MS-0195 · 2026-11-19 · Spenti per RumblingStone i plugin dell'account mai usati nel repo

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0140
- **Temi:** claude-code plugin enabledplugins contesto token mcp best-practice decisione-dm thread
- **Origine:** riga del 2026-11-19 «ADR-0140 accettata: i plugin dell'account che il repo non ha mai usato» in `plans/CHANGELOG.md`
- **Testo:** il DM ha scelto prima i 14 plugin di business, poi ha allargato: «chiudi anche altro ma lascia i plugin che sono stati usati nel repo davvero nello storico». L'unica prova d'uso nello storico è la PR #205 (2/10), che accese `pdf-viewer`, `review` e `tdd`; per gli altri 29 nessuna traccia in commit, changelog, memoria storica o file del progetto. `engineering`, `docs` e `reflexion` erano solo skill «solo nome» nella stessa PR. Misura con `claude -p`: contesto da 59.670 a 53.965 token (−9,6%), server MCP da 102 a 2. Nel thread, dopo un riavvio, l'hook SessionStart ha scritto `ok 916ed032` e `rumblingstone-tools` si è connesso: ADR-0140 passa ad accettata
- **Trovato nel repo:** `.claude/settings.json` (`enabledPlugins`) · `plans/adr/ADR-0140-la-configurazione-claude-del-repo-arriva-anche-nei-thread.md` punto 5
- **Solo qui:** `bio-research` serve a Jfs per il lavoro nel gruppo BIOME ma non a questo progetto: resta acceso negli altri progetti, perché `enabledPlugins` del repo vale solo dove arriva il suo settings. I connettori di claude.ai non si spengono così: per quelli valgono le regole `deny` del punto 4

### MS-0196 · 2026-11-19 · Riaccesi i plugin di metodo di sviluppo

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0140
- **Temi:** claude-code plugin enabledplugins contesto token sviluppo decisione-dm thread
- **Origine:** riga del 2026-11-19 «ADR-0140, correzione: riaccesi per RumblingStone i nove plugin di metodo di sviluppo» in `plans/CHANGELOG.md`
- **Testo:** subito dopo la #487 il DM ha chiesto se non avesse senso tenere i plugin delle tecniche di sviluppo. Nessuna prova d'uso nello storico (commit, file del progetto), consigliato lasciarli spenti; il DM ha scelto sulla card di riaccendere tutti e nove: `sdd`, `sadd`, `engineering`, `reflexion`, `docs`, `fpf`, `ddd`, `recursive-decomposition`, `mcp`. Costo misurato con `claude -p`: contesto da 54.372 a 56.719 token (+4,3%), 42 skill in più, 10 server MCP di `engineering` che nel container falliscono o chiedono l'accesso
- **Trovato nel repo:** `.claude/settings.json` (`enabledPlugins`) · `plans/adr/ADR-0140-la-configurazione-claude-del-repo-arriva-anche-nei-thread.md` punto 5
- **Solo qui:** misurando si è visto che un container partito prima di un merge tiene la copia vecchia di `/home/user/.claude/settings.json` finché non si rilancia `scripts/claude-progetto.sh`; i thread nuovi la rigenerano all'avvio

### MS-0197 · 2026-11-19 · Le regole di AGENTS.md arrivano con i file

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0141
- **Temi:** claude-code contesto token rules agents-md progressive-disclosure decisione-dm thread
- **Origine:** riga del 2026-11-19 «ADR-0141: le regole di AGENTS.md arrivano a Claude con i file a cui servono» in `plans/CHANGELOG.md`
- **Testo:** il DM ha scelto sulla card le regole a percorso. Provato che `.claude/rules/` del repo si carica anche quando Claude parte nella cartella che contiene il clone, e che una regola con `paths:` entra solo con i suoi file. AGENTS.md resta la fonte; `regole_claude.py` ne ricava cinque regole e `--check` le tiene allineate. Nella prima prova senza la riga di `fase1.py` nel CLAUDE.md l'agente non lanciava `fase1.py`, perché le regole arrivano dopo il primo file letto: la riga è rimasta nel CLAUDE.md. Il DM aveva chiesto anche di un grafo a eventi o di un RAG per le istruzioni: scartati perché non deterministici (MS-0192 per la prova del RAG sui contenuti)
- **Trovato nel repo:** `scripts/regole_claude.py` · `.claude/rules/rs-*.md` · `plans/adr/ADR-0141-le-regole-di-agents-arrivano-con-i-file.md`
- **Solo qui:** il nucleo resta il 55% di AGENTS.md; ridurlo vuol dire riscrivere AGENTS.md. Le misure con `claude -p` sono una corsa per lato

### MS-0198 · 2026-11-19 · `.claudeignore` diventa regole deny, e la guida al ritorno indietro

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0142
- **Temi:** claude-code claudeignore permissions deny contesto grep guida regressione decisione-dm thread
- **Origine:** riga del 2026-11-19 «ADR-0142: `.claudeignore` diventa regole `Read` di `permissions.deny`» in `plans/CHANGELOG.md`
- **Testo:** provato che Claude Code non legge `.claudeignore` (un file elencato si apre) e che `permissions.deny` con `Read(...)` blocca Read, Grep e Glob. `claudeignore_deny.py` traduce le voci; immagini, PDF, `.claude/skills/` e `.claude/.skills-sync-status` restano leggibili apposta. Nei thread le regole ancorate prendono il nome del repo davanti. Il DM ha chiesto di fare le pratiche in ordine (A, B, C, D) una PR ciascuna, di documentare tutte le scelte per poter tornare indietro e di verificare che nessuna abbia problemi: la guida `docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md` raccoglie le sei scelte del 19/11
- **Trovato nel repo:** `scripts/claudeignore_deny.py` · `.claudeignore` · `docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md` · `plans/adr/ADR-0142-claudeignore-diventa-regole-deny.md`
- **Solo qui:** nella verifica delle scelte è emerso che le istruzioni dei server dei connettori negati entrano comunque nel contesto (la regola deny toglie i tool, non le istruzioni) e che le 18 skill del repo compaiono due volte, come skill utente e come `RumblingStone:*` appena si legge un file del repo

### MS-0199 · 2026-11-19 · I gate veloci della CI prima del push (pre-commit, hook locale)

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0143
- **Temi:** ci pre-commit hook gate-locale pre-push tdd thread misura decisione-dm
- **Origine:** riga del 2026-11-19 «ADR-0143: i gate bloccanti e veloci della CI girano prima del push» in `plans/CHANGELOG.md`
- **Testo:** pratica C dell'ordine scelto dal DM (A, B, C, D). Classificate dal log le 11 corse CI rosse fra le 100 più recenti di PR (15-19/11) più la prima testa della #490: 4 regola d'oro o CHANGELOG a 4 colonne, 2 `componenti.py`, 1 adozione attiva, 1 booklet in stampa, 3 impronta delle creature, 1 `test_tabelle`. `gate_locale --rapido` costa 3 min 11 s e su 100 push non si ripaga; `--pre-push` (bloccanti, senza pytest né resa delle mappe, edizione da stampa, corredo) costa 45 s e prende 7 rossi su 12. pre-commit, scartato da ADR-0099 perché scaricava dalla rete, rifatto con `repo: local` e `language: system`: provato con il proxy su una porta morta, gira. Test scritti prima e visti rossi (`test_gate_locale.TestPrePush`, `test_install_git_hooks`). Nella stessa giornata B (hook sui file generati: nessuna modifica a mano nello storico) e D (riordino della radice: tre rimandi voluti e due censimenti citati da 15 file) sono stati misurati e lasciati senza PR
- **Trovato nel repo:** `scripts/gate_locale.py` · `.pre-commit-config.yaml` · `scripts/install-git-hooks.sh` · `plans/adr/ADR-0143-i-gate-veloci-girano-prima-del-push.md`
- **Solo qui:** gli id delle 11 corse rosse (44426033056, 44425938003, 44183963956, 44181729147, 43919525637, 43770067168, 43769907951, 43769733440, 43769518617, 43729307832, 43727650247); la stima del giro di CI in più (circa 22 minuti per rosso) non è misurata; le skill del repo «doppie» costano circa 0,7k token, non 5k

### MS-0200 · 2026-11-19 · Due test che fallivano solo nei container dei thread

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** —
- **Temi:** test ermetici tdd thread build shallow conformita fase1
- **Origine:** riga del 2026-11-19 «Due test che dipendevano dalla macchina, corretti con il test scritto prima» in `plans/CHANGELOG.md`
- **Testo:** trovati lanciando l'intera suite in un thread durante la verifica di ADR-0142 e ADR-0143: in CI erano verdi, nei container rossi. (1) `conformita_statblocchi` scorreva `ROOT.rglob("*.md")`, compresa la `build/` che `session-start.sh` costruisce: 112 copie di SKILL.md segnalate come file con numeri non letti. Ora enumera come `validate_docs.sorgenti` (tracciati più nuovi non ignorati), con ritorno a `rglob` fuori da un clone git. (2) `TestRamiAccanto` chiamava `contenuti_nei_rami.shallow()` vero: nel clone shallow dei thread `fase1` stampa «rami non misurati» e il test non trovava i file attesi; ora `shallow` è finto come gli altri accessi al repo. Test scritti prima e visti rossi (`test_le_cartelle_di_gitignore_restano_fuori`); impronta delle creature identica dopo la modifica
- **Trovato nel repo:** `scripts/conformita_statblocchi.py` · `scripts/tests/test_conformita_statblocchi.py` · `scripts/tests/test_fase1.py`
- **Solo qui:** il clone dei thread di questo container risultava shallow (`git rev-parse --is-shallow-repository` = true) nonostante lo script d'avvio faccia l'unshallow

### MS-0201 · 2026-11-19 · Il kit delle prove sulla 4050 salva in un log tutto quello che scrive

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0136
- **Temi:** prove-4050 kit log tee transcript windows tdd misura
- **Origine:** riga del 2026-11-19 «Log di ogni giro del kit» in `plans/CHANGELOG.md`
- **Testo:** il DM ha chiesto (19/11) che uscita, errori e avvisi di tutti gli strumenti del kit restino recuperabili dopo un giro. Su main restavano solo `kit.tsv` (id, codice, minuti), il log di Ollama e i log che immagini, Drappo e trascrizione scrivevano da sé; l'uscita di `kit.sh`, di `installa.sh` e delle altre prove si perdeva. Scelto lo standard di fatto: `exec` con `tee` in Bash, `Start-Transcript` in PowerShell, niente librerie. Misura con una prova finta: righe salvate da 0/32 a 32/32. `stty sane` ora guarda il terminale salvato su un descrittore a parte (fd 9), perché dietro `tee` `[ -t 1 ]` è falso. Il kit dietro `tee` non dà più un terminale alle prove: `distrobox enter` parte senza tty e le barre di avanzamento escono come righe semplici.
- **Trovato nel repo:** `scripts/prove-4050/comune.sh` · `scripts/tests/test_prove_4050_log.py` · `docs/how-to/GUIDA-PROVE-PORTATILE-4050.md`
- **Solo qui:** il transcript di Windows PowerShell 5.1 non prende lo stderr di `wsl.exe` (si evita `2>&1` per via di `ErrorActionPreference=Stop`); non provato, nessun PowerShell nel container. I log oltre 64 MB restano fuori dall'archivio.
### MS-0202 · 2026-11-19 · ADR-0134: danno entro 9 m della Drow Assassina e tabella di Varis

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0134
- **Temi:** corredo rc-001 schede bestiario decisione-dm card tiro-ravvicinato
- **Origine:** riga del 2026-11-19 «ADR-0134, regola RC-001: due scelte del DM sulle card del 19/11» in `plans/CHANGELOG.md`
- **Testo:** dopo la #478 restavano due differenze, messe su card dal thread del volume. Il DM ha scelto: la riga a distanza della Drow Assassina scrive anche il danno entro 9 m (1d4+1 + veleno, Tiro Ravvicinato SRD dà +1 all'attacco e ai danni); la tabella in prosa di Varis elenca il giaco di cuoio borchiato +1 e il pugnale +1 già nel blocco. Tiene gli oggetti aggiunti senza card nella #458 e nella #478: giaco e pugnale di Varis, anello +1 di Tempestas, 10 quadrelli della Drow Assassina e di Therysol
- **Trovato nel repo:** `Bestiario/mostri/drow-assassina-lolth-cr10.md` · `Bestiario/png/Varis_Seta_Argento/Varis_Seta_Argento.md`
- **Solo qui:** le note della tabella di Varis dicono solo ciò che la scheda già scriveva (CA 16, attacco +7/+2, 1d4+1); «sotto le sete» era una frase inventata e non è entrata

### MS-0203 · 2026-11-19 · I sicari di Sonjak al Palio possono rapire il fantino

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** —
- **Temi:** tattiche villain palio sonjak sicari drow fantino arc09 decisione-dm card coerenza
- **Origine:** riga del 2026-11-19 «Tattiche di villain e PNG, Palio: i sicari di Sonjak possono puntare il cavallo o il fantino» in `plans/CHANGELOG.md`
- **Testo:** la rilettura del 18/11 (MS-0189) aveva lasciato aperta una differenza fra due file precedenti al lavoro sulle tattiche: gli statblocchi del Palio davano ai sicari drow solo il cavallo, l'integrazione e il Giorno 2 anche il fantino da rapire. Il DM ha scelto sulla card del 19/11 la consigliata, «cavallo o fantino, sceglie il DM»: gli statblocchi si allineano agli altri due file. Come lo prendono (veleno del sonno della balestra, la scorta del fantino trattata come la guardia della stalla) è dedotto dalla scheda dei sicari, non scritto altrove.
- **Trovato nel repo:** `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2D-PALIO-STATBLOCCHI.md` §3.1, col blocco `<!-- storico -->`
- **Solo qui:** il booklet HTML del Palio su main non era stato rigenerato dopo la #465 e la #478; rigenerarlo porta dentro anche quelle righe. La rilettura completa dei lotti 1-4 fatta nello stesso thread ha trovato tre punti da decidere (CD della *suggestione* di Xal'thor, slot di Xilthra, Zalkatar con Ozyrrandion), messi su card; la voce che segue dice come sono finiti.

### MS-0204 · 2026-11-19 · Rilettura completa dei lotti 1-4 delle tattiche: due contraddizioni con la scheda

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** —
- **Temi:** tattiche villain xalthor xilthra zalkatar kragar arc09 rilettura decisione-dm card slot suggestione
- **Origine:** riga del 2026-11-19 «Tattiche di villain e PNG, rilettura completa dei lotti 1-4 contro le schede» in `plans/CHANGELOG.md`
- **Testo:** MS-0189 aveva riletto i lotti 1-4 solo nelle righe aggiunte. La rilettura completa, riga per riga contro la scheda di ognuno, ha trovato due contraddizioni, decise dal DM sulle card del 19/11 con la consigliata, e ha aperto una terza card sbagliata. Xal'thor: la *suggestione* su Tordek era CD 20 nella scena (dal maggio 2026) e nella tattica, CD 16 nei poteri; vale 16, che si ricostruisce dalla scheda. Xilthra: la card diceva che mancava uno slot al 2°, 3° e 4°, e il DM ha scelto di aggiungerli; ma il conto era sbagliato (chierico 12: 4/4/3 slot base a quei livelli, non 5/5/4) e `verifica_scheda`, che conta gli slot, dà 6 violazioni con la modifica e 0 senza. La scheda resta com'è e la scelta della card non si applica. Zalkatar: con Ozyrrandion lo mandava in lotta su un PG sano, contro «mai in mischia» della card del 15/11.
- **Trovato nel repo:** i file della riga del changelog, ognuno col blocco `<!-- storico -->`
- **Solo qui:** riletti senza correzioni Zog'tar e Balvar (ARC07-DEF-4 Scena 10, BARILE §8: il Colpo Terrificante è un'azione standard e la tattica lo mette in round diversi dall'attacco completo, l'Occhio è un'azione di movimento), Gorthak, Karruk, Zarim, Sethrax, Azarr Kul, Ushgar. Kragar (P2B BATTLE-STATS r.64-74) ha conti sbagliati più vecchi delle tattiche: Ladro 4 con attacco furtivo +3d6 (SRD +2d6), 88 pf invece di circa 98, nessuna Competenza nelle armi esotiche per la catena; segnalati al coordinatore per il thread delle regole. Lezione: prima di aprire una card su un numero di scheda, lanciare `verifica_scheda` su quella scheda.

### MS-0205 · 2026-11-19 · Due stampe per arco, e i rimandi con il numero di pagina

- **Data:** 2026-11-19
- **PR:** #497
- **ADR:** ADR-0144
- **Temi:** stampa booklet volume arco rimandi pagina typst serata arc07
- **Origine:** riga del 2026-11-19 «ADR-0144: due stampe per arco e rimandi con il numero di pagina» in `plans/CHANGELOG.md`
- **Testo:** richiesta di Jfs del 19/11 per venerdì: la stampa della serata (dal barile in avanti) e quella dell'AP di ARC-07, misurate. Misura di base su main: serata 130 pp, 107 rimandi interni, nessuno con la pagina, 8 a un titolo che nel capitolo indicato non c'è (il traduttore mandava al primo capitolo i rimandi spezzati da un a capo e la forma «§7 di `DEF-4`»). Dopo: 100 su 108 con la pagina, tutti giusti, 1 titolo non trovato (apertura in grassetto). Volume d'arco: con le schede solo alla prima apparizione 289 pp e Balvar a 24 pagine dalla scheda, Zog'tar a 17; con `entrambe` 294 pp e distanze mediane 2-8. Schede spezzate del volume da 3 a 1: dopo il salto di colonna il tema rimisura, e se la colonna di destra è accorciata da un float la scheda va alla pagina dopo (+1 pagina); resta Terros, alta due colonne; serata (131 pp) e booklet lungo (163) perdono la scheda spezzata di Balvar. La CI della prima testa ha trovato in DEF-5 e CONSEGUENZE-ECHI, mai stampati prima, sette righe di storia (avvolte in `storico`) e tre note aperte dei master (TODO dei Bracieri in DEF-1 §8, «(da verificare)» in DEF-4 sulle pergamene di Hella), contate con tetto 3; poi Jfs su card ha chiuso il «(da verificare)» (le cure e neutralizza veleno sono nella lista del druido, SRD 3.5: Hella le legge senza Usare Oggetti Magici) e i due TODO di DEF-1 §8 erano una nota mai aggiornata: «Diventare una Collina» è sulla scheda dei Bracieri (`05_Bracieri_Gemelli_Scheda_PG_Completa.md` §7, righe 123-131) dal 2026-08-01, K-B28, come *ingrandire persona* 1 minuto 1/giorno; nessun tetto serve più. Nella stessa PR, su richiesta del thread delle tattiche e per la card di Jfs del 19/11 (10:55 UTC): Zog'tar porta 2 pozioni di *cura ferite gravi* (DEF-4 A.2) e le beve la notte dopo il barile, quindi sale sulla breccia a 283 pf invece di 264 e con «separa e finisce» un PG muore nel 35% delle prove invece del 28% (profili_villain zogtar-breccia, 20.000 prove, misura del thread delle tattiche, non rifatta qui). Scartata la prima prova, che decideva dalla posizione prima del salto: Typst la legge dal giro di composizione precedente e il risultato non converge. Bug preesistenti trovati: `indice_analitico` mancava da `CHIAVI_NOTE` (avviso «chiave sconosciuta»), `marca_indice` metteva la voce dentro i titoli (sparivano dal titolo, e la testatina stampava `#voce-indice[...]` letterale) e dentro le stringhe. Card a Jfs nella serata: l'Echo Ledger resta (il foglio vi rimanda e contiene le conseguenze della notte); tolto l'indice dei read-aloud della cassetta in attesa della sua scelta. Rifiuti già noti rispettati: niente pagina fitta, schede intere in ogni scena. Domanda di Jfs (19/11): il ritratto di Vatore era tagliato in fondo alla pagina (serata p. 71, volume d'arco p. 194, 80 pt oltre il foglio; preesistente su main, booklet della serata p. 69). Causa: `figura` del tema è un blocco che non si spezza, collocato sotto la tabella larga della Scena 9 in float; Typst 0.15 sbaglia lo spazio che resta. Nessuna misura guardava le immagini fuori dal foglio. Test scritto prima (rosso), poi la misura `immagini_tagliate` (tetto 0, smarginatura 3 mm tollerata) e la figura che misura lo spazio rimasto e va a capo colonna: 2 → 0 sui 22 booklet. La stessa regola sposta i ritratti che finivano nel margine basso (Drappo, Giardino): +1 pagina in quattro booklet (8 → 9, 11 → 12, 40 → 41, 25 → 26). Il primo tentativo con `layout` attorno cambiava la spaziatura di 5 pt e spezzava la scheda del Treant nel fascicolo giocatori della resurrezione; quello con solo `context` lasciava Vatore tagliato. Tenuto: blocco esterno con la spaziatura di sempre, `layout` dentro. Costo: a p. 71 della serata circa 220 pt di colonna destra bianchi sotto le tabelle. Provato e scartato il float di colonna (`place(top, float: true, scope: "column")`): Typst 0.15 lo mette sotto le tabelle a tutta pagina e l'immagine esce lo stesso; dentro `layout` un float non esce dal contenitore
- **Trovato nel repo:** `plans/adr/ADR-0144-due-stampe-per-arco-e-rimandi-con-la-pagina.md` · `07_il Portale Della Forgia Eterna/homebrew/volume-arco/ARC07-VOLUME-ARCO.manifest.json` · `plans/esperimenti/booklet-arc07-2026-11-19/misura_rimandi.py`
- **Solo qui:** «LORDO» segnalato da `titoli_rovinati` alle pp. 47 e 102 del volume è una parola in maiuscolo nelle tabelle del tesoro, falso positivo della misura; PDF consegnati in /mnt/project-files/booklet-arc07-2026-11-19/

### MS-0206 · 2026-11-19 · L'ordine del booklet della serata si misura

- **Data:** 2026-11-19
- **PR:** #497
- **ADR:** ADR-0145
- **Temi:** stampa booklet serata ordine capitoli struttura guida rimandi arc07 misura_ordine
- **Origine:** riga del 2026-11-19 «ADR-0145 (proposta): l'ordine dei capitoli del booklet della serata si misura» in `plans/CHANGELOG.md`
- **Testo:** domanda di Jfs del 19/11 (12:52-12:56 UTC): l'ordine delle sezioni del booklet della serata ha senso e segue uno standard? Cercare le regole, misurare quanto sono applicate, creare strumenti con test dove mancano. Fonti lette: schema degli AP Paizo e di Red Hand of Doom (scelto da Jfs il 09/11), Alexander (*The Art of the Key*, *History of the Stat Block*), Shea (otto passi del Lazy DM), Milton (pannello di controllo), EN World (best practice per moduli facili da giocare), ADR-0013 e la ricerca K1-K14. Nessuno strumento del repo misurava l'ordine. Misura nuova `misura_ordine.py` con regole per volume in un file di ruoli; i segnalibri del PDF sono piatti, quindi il ruolo si eredita dal capitolo con il flag `capitolo`. Serata v3 (131 pp): 15 difetti, contando un blocco fuori posto come uno (2 blocchi di preparazione dopo il gioco, §0-ter con i momenti dei PG e le zone, e la cassetta con Durik; 3 riassunti dopo il dettaglio, 3 pagine di dopo-serata fra le scene, 2 doppioni, 5 righe sbagliate della guida, che era quella del booklet lungo). v4 (134 pp): 3 (Durik in coda; doppioni A.1 Skullcrusher adulto maturo GS 14 contro lo Skullcrusher Vecchio GS 17 canone della serata, e A.6). Il riordino ha rotto i numeri romani scritti a mano nei sorgenti (15 rimandi a un titolo assente): sostituiti con i nomi dei file, che il volume traduce. Bug trovati nel traduttore: i rimandi senza parte a un master diviso andavano al primo capitolo (il riferimento rapido), corretto con `principale`; «B. Tesoro» non si riconosceva come parte; il §N dopo un nome di file non passava da `capitolo_della_parte`, quindi il §10 e il §13 del barile andavano al cap. V invece del XIII. Rimandi dopo: 115 con pagina su 124, tutti giusti, 1 a un'apertura in grassetto senza titolo. Alle 13:10 UTC Jfs ha chiesto lo stesso lavoro per l'avventura completa: modo volume di `misura_ordine.py` (regola `parte`, V1 quadro del volume, V2 indice oltre due pagine, V3 parte senza gioco fra parti giocate), con le sottosezioni che ereditano dalla sezione sopra e i difetti di preparazione contati per blocco. Volume v1.2 (294 pp): 12 difetti (nessun quadro, indice di 8 pagine, ponte P5 fra duello e ritorno, 4 riassunti dopo il dettaglio). v1.3 (288 pp): 0, con il quadro dell'arco scritto dai riquadri «La serata in tre frasi», `indice_profondita: 1`, versioni veloci C.1-C.3 in testa alla loro parte, il ponte dopo il ritorno. Un rimando di `DEF-2` (riga 1118) puntava a un §7-bis di `DEF-3` che non esiste: la ghianda è nel §11 C, corretto. Limite: C.1 riassume scene di un'altra parte e la misura parte per parte non la vede. Bug trovato: una sezione chiesta per nome con `sezioni` usciva anche se avvolta in `storico` (il §12 «Domande al DM» del barile, 21 righe fuori margine in misura_stampa); ora `estrai_sezioni` la tiene dentro il blocco
- **Trovato nel repo:** `plans/adr/ADR-0145-l-ordine-del-booklet-della-serata-si-misura.md` · `scripts/misura_ordine.py` · `07_il Portale Della Forgia Eterna/homebrew/sessione-notte-e-alba/ARC07-NOTTE-E-ALBA-SERATA.manifest.json` (i ruoli, dal 2026-11-19: MS-0212)
- **Solo qui:** card a Jfs su ordine v4, doppioni e posizione di Durik; l'ordine del volume d'arco resta da discutere a parte; i segnalibri piatti del PDF sono un difetto di navigazione non corretto

### MS-0207 · 2026-11-19 · Revisione delle scelte storiche con dnd.arkalseif.info: venti card del DM

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0126
- **Temi:** revisione storica arkalseif schede domini chierici talenti spymaster sublime-chord stormsinger card verifica-scheda
- **Origine:** riga del 2026-11-19 «revisione storica delle schede su dnd.arkalseif.info» in `plans/CHANGELOG.md`
- **Testo:** il DM ha aggiunto dnd.arkalseif.info ai domini dell'ambiente e chiesto di ricontrollare le scelte già fatte sulle schede. Fonte non OGL: nel repo solo nomi, numeri e pagine, nessun test di CI ne dipende. Dove il sito dava una risposta sola si è corretto (pagine citate, note «non verificato»); dove restava una scelta, una card alla volta con la consigliata. Venti card risolte, tutte sulla consigliata tranne Ur-Vrax (il DM ha prima scelto Legale Malvagio per errore e ha chiesto di ripresentarla, poi Neutrale Malvagio). Rifacendo gli slot sulla tabella SRD sono usciti due errori non chiesti dalle card: Salvatore aveva 4 incantesimi di 3° al giorno (l'SRD ne dà 2) e i chierici drow di Lolth del P1C non avevano lo slot di dominio al 3° e al 4°. Misura contro main 517a3e79: violazioni di `verifica_scheda` 34 → 2, e le due rimaste sono nell'archivio di ARC-06, che non si tocca.
- **Trovato nel repo:** `/mnt/project-files/revisione-arkalseif-2026-11-19/REVISIONE-SCELTE-STORICHE.md` (fuori dal repo) · `Bestiario/png/Harbek_Runaforte.md` · `Bestiario/villain/Sonjak/Sonjak.md` · `08_La Battaglia Di Hammerfist/ARC08-01-GUIDA-DM.md`
- **Solo qui:** il sito non copre il Monster Manual oltre 60 voci, il Magic Item Compendium oltre 200, né le liste di domini del FRCS per gli dei che hanno anche una pagina del Deities and Demigods: restano non verificati rakshasa Ak'chazar, death tyrant, mezzo-illithid, yochlol, Curst e Corrupted Frenzy, Hammer Specialist, Deceive Item, la Cantante Divina di Dana e il dominio Selvaggio di Yeenoghu. Le due ERRATA (ARC08 e PARTE2-3) sono archivi per `fase1.py --check` ma hanno blocchi che `verifica_scheda` misura e che le PR precedenti hanno già corretto: toccate con il blocco storico. L'archivio `_ARCHIVIO/CoronaDiAdamantio/villans.md` è stato riportato com'era. Chiuse dopo l'apertura della PR: la chierica di Lolth del P1C apre con *blocca persone* su Hella invece del *colpo infuocato* che non ha; Tempestas sale a Cantore delle tempeste 3 (GS 15) per avere il *colpo di tuono* (Frostburn p. 70), il fulmine del «Bardo del Tuono», al posto di *fulmine*, che un bardo non lancia: il DM l'ha preferito alla *lentezza* consigliata e a una bacchetta con Usare Oggetti Magici. Con il sì esplicito del DM anche su `main`: la riga di Tempestas cambia in `campaign/state.yaml` (Stormsinger 3, GS 15), `render_state.py` rigenera `state.md`, la prosa fuori dai marcatori si corregge a mano e `dm.py dossier` rigenera il DM-DOSSIER; `dm.py` non ha un comando che riscriva la riga di un PNG, e il flusso ora sta nel playbook al §4.3-bis. `state-changelog.md` resta com'era (dice ancora GS 14, ed è storia).

### MS-0208 · 2026-11-19 · Lo Skullcrusher Vecchio ha la scheda intera, e la serata non stampa l'Adulto

- **Data:** 2026-11-19
- **PR:** #499
- **ADR:** ADR-0145
- **Temi:** stampa booklet serata doppioni skullcrusher vecchio adulto scheda durik arc07
- **Origine:** riga del 2026-11-19 «Card di Jfs sulla serata di ARC-07: Durik resta in fondo come galleria dei PNG» in `plans/CHANGELOG.md`
- **Testo:** card del 19/11 dopo il merge della #497. Durik: Jfs sceglie «in fondo, come galleria PNG» (ruolo riferimento, non preparazione). Doppioni: Jfs (14:02 UTC) chiede di verificare che la scheda del Vecchio abbia tutti i dati e non rimandi all'adulto maturo, poi di togliere il doppione. Verifica: A.1-bis rimandava ad A.1 in sei punti (Ascoltare e Osservare, abilità, capacità magiche, incantesimi conosciuti, tattica, soffio impregnante, respirare sott'acqua mancante). Ricopiati i valori dove il blocco diceva «come A.1», senza numeri nuovi; due INFERRED con domanda, uno chiuso lo stesso giorno: Allerta (+2 a Ascoltare e Osservare) e i conosciuti dello stregone di 7° secondo la tabella SRD (7/5/3/2 contro i 6/4/2 di A.1, D64 aggiunge solo i due di 3°). «Cosa cambia al tavolo», che stava dentro A.1, è ora A.1-ter con i numeri del Vecchio accanto (16d4 CD 31, RI 22, morso col nome +54). A.6 non è un doppione puro (tabella delle complicazioni dello skill challenge; le schede sono in appendice come tutte per `entrambe`). Serata: 3 → 0 difetti di struttura, 132 pp
- **Trovato nel repo:** `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` · `07_il Portale Della Forgia Eterna/homebrew/sessione-notte-e-alba/ARC07-NOTTE-E-ALBA-SERATA.manifest.json` (i ruoli, dal 2026-11-19: MS-0212)
- **Solo qui:** incantesimi del Vecchio decisi da Jfs alle 14:06 UTC: i conosciuti dell'Adulto più *dissolvi magie* e *lentezza* (D64); l'INFERRED è tolto. Allerta: +31 a Ascoltare e Osservare, perché i talenti del Vecchio elencano Allerta e l'SRD dà +2 (consiglio del coordinatore; Jfs può riportarlo a +29). Nessun INFERRED nuovo resta


### MS-0209 · 2026-11-19 · Le tecniche di prosa proprie del repo, messe accanto alle case

- **Data:** 2026-11-19
- **PR:** —
- **ADR:** ADR-0093
- **Temi:** prosa standard editoriale cieco corpus paizo wotc caratteristiche decisione-dm card
- **Origine:** riga del 2026-11-19 «RICERCA-PROSA-PECULIARE» in `plans/CHANGELOG.md`
- **Testo:** domanda di Jfs del 19/11: lo standard della prosa si allinea a Paizo, Wizards e alla community, e quanto se ne discosta da diventare caratteristica del repo? Criterio di Jfs: entrano solo le differenze peculiari e ovviamente migliorative. Misura su main e5339cee contro il corpus (2.335 box italiani, 118 Paizo): frasi del repo a 11-15 parole contro 16-18, -mente da 0 a 2,7‰ contro 5,9-8,3‰ (ARC-08 era a 5,8‰ il 23/10), «Che fate?» o domanda in chiusura nel 16-18% dei box contro il 2-5%; i box sono il 5,6% delle parole dei master di ARC-07. Scelte del DM sulle card: tecniche 1 (sensi) e 2 (chiusa) entrano come caratteristiche, tecnica 4 (voce per l'orecchio) prima al cieco, etichette dei pilastri tolte da tutte le stampe; tecnica 3 e ordine dei cieco A, B, C aperti.
- **Trovato nel repo:** `plans/RICERCA-PROSA-PECULIARE-2026-11.md` · `skills/rumblingstone-narrative-style/references/editorial-standards.md` §4-bis
- **Solo qui:** la checklist chiedeva ancora di togliere «la frase che spiega» dal 22/10, contro il voto; la regola 3 del §2-ter non era nel registro. Le etichette dei pilastri nel booklet della serata v4.1 erano 18 intestazioni e 24 richiami; il filtro nel renderer spetta al thread dei booklet. Gli esempi con e senza mostrati a Jfs vengono da giro2 coppie 2 e 3 e dalla riscrittura del 22/10, B14 e B16.
### MS-0210 · 2026-11-19 · Typst converge sul volume d'arco, e il controllo di convergenza vede di nuovo

- **Data:** 2026-11-19
- **PR:** #501
- **ADR:** ADR-0144
- **Temi:** stampa typst convergenza rimandi pagina volume arco abbazia misura_stampa avvisi tema scheda colonna
- **Origine:** riga del 2026-11-19 «Convergenza di typst» in `plans/CHANGELOG.md`
- **Testo:** il coordinatore mette la convergenza prima dei segnalibri: il volume d'arco di ARC-07 su main stampava 15 rimandi su 242 sbagliati di una pagina (`plans/esperimenti/booklet-arc07-2026-11-19/misura_rimandi.py`). Bisezione per varianti del tema (ognuna compilata con `typst.compile_with_warnings`): togliere il rimando muto sulla stessa pagina, la figura che va a capo, la tabella che scavalca non cambia niente (44 avvisi); la logica della scheda «entrambe» li porta a 3. Due colpevoli: la scheda su una pagina a una colonna (l'appendice A4 di DEF-4, A.1-bis, entrata con la #499) e il primo `colbreak()` deciso su `here()` prima del riquadro (l'Abbazia, indice a 30, 31, 32 a ogni giro). Restano avvisi «a measured element did not stabilize» (tabelle e schede misurate con dentro un `context`): non cambiano numeri stampati, e il gate non li conta. Il gate di `misura_stampa` cercava «did not converge» nello stderr, che col typst di PyPI è sempre vuoto: era cieco da ADR-0116. Ora `Esito.avvisi` e `typst_motore.numeri_instabili()`; prova su main: 11 numeri instabili nel volume, 0 nella serata. Senza il primo «a capo colonna» la CI della #501 ha bocciato il volume (schede spezzate 2, tetto 1): lo Skullcrusher Vecchio partiva in cima alla colonna sinistra di p. 204, accorciata dalle tabelle a tutta pagina, e finiva su tre colonne. Strumentato con `metadata <dbg>` (qui 0,07 colonne, alto 0,90): ora, in cima alla colonna di sinistra, se il riquadro supera due volte lo spazio che resta va alla pagina dopo. Volume 289 pp, una sola scheda spezzata (Terros, 26-27, come su main)
- **Trovato nel repo:** `scripts/typst/tema-rumblingstone.typ` · `scripts/typst_motore.py` · `scripts/misura_stampa.py` · `scripts/tests/test_typst_motore.py`
- **Solo qui:** il documento che oscilla nel test (`OSCILLA`) mette un salto pagina se il segno cade su una pagina pari: è il più piccolo che typst non fa convergere. Una riproduzione minima della scheda su una colonna non oscilla da sola (serve il resto del volume), perciò il cancello è la misura sui booklet veri, non un test unitario

### MS-0211 · 2026-11-19 · I segnalibri del PDF seguono l'albero dei titoli, e il volume è messo accanto alle case

- **Data:** 2026-11-19
- **PR:** #502
- **ADR:** ADR-0145
- **Temi:** stampa segnalibri annidati pdf typst heading offset paizo wizards red hand of doom burnt offerings community confronto standard editoriale
- **Origine:** riga del 2026-11-19 «ADR-0145, segnalibri annidati» in `plans/CHANGELOG.md`
- **Testo:** Jfs (14:07 UTC) vuole chiusi i limiti dichiarati della #497 in modo deterministico e con uno standard editoriale professionale; alle 14:10 chiede il confronto con Paizo, Wizards e community, e alle 14:11 che le differenze entrino solo se proprie del repo e migliorative. Il coordinatore ha messo in coda: convergenza (#501), poi segnalibri e ruoli, poi etichette dei pilastri. Typst annida un segnalibro sotto l'ultimo titolo segnalato: se il titolo di primo livello ha `bookmarked: false`, i figli salgono al primo livello. Per questo il titolo nascosto del capitolo non è un segnalibro, e lo è quello visibile (`titolo-visibile(..., segnalibro: true)`). PDF/UA-1 rifiutava il salto dal primo al terzo livello: ogni capitolo si porta al minimo dei suoi titoli (`cala`); la sentinella `prima` è None, non 0, perché `if prima and` trattava lo 0 come falso. «1. Che cosa…» dentro `[...]` diventava un elenco e perdeva il numero, quindi si protegge con «1\.». Le misure sono nella riga del changelog. Il ruolo delle sezioni nel manifest (CMOS 1.4, EPUB 3 `epub:type`) e la misura d'ordine come cancello restano per la PR dopo
- **Trovato nel repo:** `scripts/export_booklet_typst.py` · `scripts/typst/tema-rumblingstone.typ` · `scripts/tests/test_pdfua.py` · `plans/adr/ADR-0145-l-ordine-del-booklet-della-serata-si-misura.md`
- **Solo qui:** i PDF di riferimento sono quelli caricati da Jfs nel thread (/mnt/project-files/uploads/hearth/, Burnt Offerings e l'estratto di RHoD), mai nel repo. Per la community si sono guardati Ben Milton e Mike Shea: è una lettura, non una misura

### MS-0212 · 2026-11-19 · I ruoli delle sezioni passano nel manifest, e l'ordine del booklet diventa un cancello

- **Data:** 2026-11-19
- **PR:** #503
- **ADR:** ADR-0145
- **Temi:** stampa ordine ruoli manifest cancello misura_ordine misura_stampa cmos front matter back matter epub type difetti_ordine
- **Origine:** riga del 2026-11-19 «ADR-0145, i ruoli nel manifest e l'ordine come cancello» in `plans/CHANGELOG.md`
- **Testo:** Jfs (14:07 UTC) vuole chiusi in modo deterministico i limiti dichiarati; due erano «la misura d'ordine non è un cancello» e «i ruoli sono scritti a mano in file a parte». Lo standard degli editori tiene il ruolo accanto al contenuto (CMOS 1.4, EPUB 3 `epub:type`), e così si è fatto: chiave `ruolo` nei capitoli, `ruoli_sezioni` per le eccezioni. La migrazione è stata provata etichettando i PDF della #502 con i file vecchi e con i manifest: zero differenze su 128 e 398 sezioni. Il thread del volume ha accettato il nome `ruolo` e darà alla sua appendice `"ruolo": "riferimento"`. Tre regole non combaciano più con nessuna sezione (A.1 dell'Adulto, la cassetta nella serata, l'Appendice C) e restano come guardie. Il cancello statico sta in `test_misura_ordine.py`, quello sul PDF in `misura_stampa.py`
- **Trovato nel repo:** `scripts/misura_ordine.py` · `scripts/misura_stampa.py` · `scripts/schemas/booklet_manifest.schema.json` · `plans/adr/ADR-0145-l-ordine-del-booklet-della-serata-si-misura.md`
- **Solo qui:** la prova del manifest rotto apposta è in scratchpad, non nel repo: tre difetti (R0 e due pagine di R6)

### MS-0213 · 2026-11-19 · Le etichette dei pilastri escono dalle stampe, e il bug dei tag di typst torna con le liste

- **Data:** 2026-11-19
- **PR:** #504
- **ADR:** ADR-0070
- **Temi:** stampa etichette pilastri prosa filtro typst pdfua pdfa bug tag liste impaginazione
- **Origine:** riga del 2026-11-19 «Le etichette dei pilastri non si stampano» in `plans/CHANGELOG.md`
- **Testo:** Jfs ha scelto sulla card del thread della prosa di togliere le etichette dei pilastri («Read-aloud (Andor lead)», «(pilastro GoT)») da tutte le stampe, tenendole nel sorgente: servono a chi scrive e a `misura_craft`. Il filtro sta in `leggi_per_la_stampa`, quindi vale per Typst e per Homebrewery, e non tocca i master. Togliere «(Mercer lead)» da un riquadro ha accorciato di una riga la colonna e ha spostato una voce d'elenco a cavallo della pagina 102, che è una tabella a pagina piena: typst 0.15.2 rifiuta allora PDF/UA-1 con «invalid list (L) structure», e il motore ripiega sul PDF senza standard. Come si trova: applicare al `.typ` di main le righe cambiate una alla volta (qui una sola), poi provare a tenere insieme ogni lista dopo quella riga. Tenere insieme ogni voce nel tema chiude il bug ma manda 27 righe fuori margine nella serata e aggiunge da 2 a 3 pagine a volume: scartato. Si è diviso in due il capoverso «Dal round 3 si smette» di DEF-4, senza cambiare parole. Il bug può tornare con qualunque modifica che sposti le pagine
- **Trovato nel repo:** `scripts/dmcore/testo.py` · `scripts/tests/test_etichette_pilastri.py` · `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`
- **Solo qui:** l'export avvisa con «non è PDF/A» ma esce verde: in CI il ripiego non ferma niente, e lo si vede solo leggendo l'avviso o ricompilando con gli standard

### MS-0214 · 2026-11-20 · Il corredo nella prosa senza grassetto non si leggeva, e sei schede passano nel recinto

- **Data:** 2026-11-20
- **PR:** —
- **ADR:** ADR-0134
- **Temi:** corredo equipaggiamento rc-001 ricchezza tabella 4-23 verifica_scheda pcg modificatori razziali bestiario
- **Origine:** riga del 2026-11-20 «le sei schede di `Bestiario/mostri/` che avevano il corredo solo nella prosa» in `plans/CHANGELOG.md`
- **Testo:** Il primo conteggio delle schede senza corredo diceva 29, ma veniva da un grep grezzo: con il lettore di `verifica_scheda.py` sono 6. Su quattro di queste la riga «Equipaggiamento» stava nella prosa delle Statistiche senza grassetto, e `_righe_dell_equipaggiamento` non la legge: il loro valore non era mai stato controllato contro la Tabella 4-23. Messe nel recinto, quattro risultano sopra il tetto. Il DM ha scelto sulle card una per una: orog e duergar tengono il corredo e lo dichiarano; lo Spezzamente perde la fascia +4 e tutte le CD di ammaliamento scendono di 2; per la Furia è stato il DM a proporre i guanti dell'orco +2 al posto della cintura +4, che costano 12.000 mo in meno e un punto di attacco e danni. L'hobgoblin regular 4 ha mostrato un difetto diverso: il .pcg salva le caratteristiche prima dei modificatori razziali, e `genera_attributi.py` le copia così. La scheda esce dalla marca del generatore, come Karruk nel 2026-09.
- **Trovato nel repo:** `Bestiario/mostri/furia-della-mano-cr10.md` · `Bestiario/mostri/spezzamente-kulkor-zhul-cr12.md` · `Bestiario/mostri/hobgoblin-regular-warrior4-cr3.md` · `scripts/genera_attributi.py`
- **Solo qui:** il difetto del .pcg può toccare altre schede «solo .pcg» (orco regular 4, Karkilan, koth, doom-hand); non è verificato ed è del thread delle regole
### MS-0215 · 2026-11-20 · L'orco regular senza la razza, Karkilan e l'orco berserk con l'ira dentro i numeri base

- **Data:** 2026-11-20
- **PR:** —
- **ADR:** ADR-0118
- **Temi:** pcgen pcg razza ira barbaro karkilan orco berserk card verifica-scheda
- **Origine:** riga del 2026-11-20 «Caratteristiche dal .pcg: l'ira dentro i numeri» in `plans/CHANGELOG.md`
- **Testo:** il thread del volume ha trovato che il .pcg di PCGen salva le caratteristiche prima dei modificatori di razza. Su 13 schede del Bestiario che citano un .pcg, il difetto della razza tocca l'hobgoblin regular 4 (corretto nella #505) e l'orco regular 4. Il confronto ha trovato un secondo difetto: gli export di Karkilan e dell'orco berserk 2 erano salvati in ira, e l'orco aggiungeva l'ira una seconda volta nella sua riga. Il DM ha scelto i numeri base fuori ira con l'ira nella sua riga, e la razza per l'orco regular (For 18, falchion +9).
- **Trovato nel repo:** `Bestiario/villain/minotauro-karkilan-cr5.md` · `Bestiario/mostri/orco-berserk-barbaro2-cr2.md` · `08_La Battaglia Di Hammerfist/ARC08-DEF-2-TRE-GIORNI-DI-SANGUE.md` · `Bestiario/mostri/orco-regular-warrior4-cr3.md`
- **Solo qui:** `verifica_scheda.py` non lo vede: non conosce la razza né sa se un export è in ira; il controllo è `/mnt/project-files/revisione-arkalseif-2026-11-19/pcgcheck.py`, fuori dal repo. Il controllo della lotta legge come lotta base anche una «Lotta» scritta dentro la riga Ira: per questo la lotta in ira sta solo nella riga delle Statistiche.

### MS-0216 · 2026-11-21 · Tordek è Monaco anche sulla carta, e dominare persone non è permanente

- **Data:** 2026-11-21
- **PR:** —
- **ADR:** —
- **Temi:** regole pg tordek monaco barbaro trascrizione srd incantesimi dominare persone confusione durata mantello resistenza inferred skill
- **Origine:** riga del 2026-11-21 «Due incoerenze trovate dal thread dei draghi» in `plans/CHANGELOG.md`
- **Testo:** La trascrizione della foto della scheda di carta del 2026-11-05 dava a Tordek Guerriero 4 / Barbaro 9, mentre `campaign/state.yaml` dice Fighter 4 / Monk 9; il DM ha confermato il Monaco. I numeri della carta lo dicono da soli: con il Monaco i tiri salvezza fanno Temp 13, Rifl 10, Vol 11, e la carta ne ha uno in più su tutti e tre, il *mantello della resistenza +1* della scheda PCGen al 12° livello; con il Barbaro Riflessi e Volontà sarebbero 7 e 8. L'«armatura +1» della carta è marcata INFERRED: forse è l'amuleto dell'armatura naturale +1 della scheda PCGen, perché il contatto 21 torna solo se Tordek non porta armatura. Nella skill dnd-35-srd *dominare persone* diceva «permanent until dispelled», ma l'SRD dà 1 giorno per livello: chi usava la skill per un villain che domina un PNG avrebbe tenuto il controllo per sempre. Nella stessa sezione *confusione* colpiva 1 creatura per livello, senza durata; l'SRD dice un'esplosione di 4,5 m di raggio per 1 round per livello. Il regolista ha controllato le due righe sul testo SRD, perché d20srd.org risponde 403 dal proxy
- **Trovato nel repo:** `plans/esperimenti/p16-inferred-2026-11-04/SCHEDE-PG-CARTA.md` · `skills/dnd-35-srd/references/spells.md`
- **Solo qui:** il mantello non è scritto sulla carta: sta solo nella scheda PCGen in PDF. Il custode del canone ha trovato altre tracce del Tordek barbaro o di un altro livello, fuori da questo lavoro e ancora aperte: il Torneo dell'arco 09 lo dà Monk 13 (`Arco-Post-Hammerfist-P2B-Torneo-STATBLOCCHI-COMPLETO.md` r.12-30, `Arco-Post-Hammerfist-P2B-Torneo-Tordek-PARTE1-Round1.md` r.10 e 23); `ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` r.3247 lo manda in ira; il 77% di `wyrmlord-karruk-cr13.md` r.38 viene da `duelli_arc09.py` r.167, che simula Tordek in ira, come gli altri simulatori di `plans/esperimenti/` che gli danno l'ira; MS-0142 scrive «+23 in ira»; i due file `OTTO-PORTE` dell'arco 09 legano le porte 3 e 4 dell'Orbe a Monaco 10 e 12

### MS-0217 · 2026-11-20 · I rimandi tecnici escono dai booklet di ARC-07

- **Data:** 2026-11-20
- **PR:** #511
- **ADR:** —
- **Temi:** stampa booklet serata rimandi tecnici marcatori di lavoro adr pdf tavolo
- **Origine:** riga del 2026-11-20 «Via i rimandi tecnici dai booklet di ARC-07» in `plans/CHANGELOG.md`
- **Testo:** Jfs ha chiesto il booklet della serata del 20/11 pronto da usare, poi (14:37 UTC) di togliere i rimandi tecnici. Il PDF è stato composto da main più le bozze #505-#509 e messo in /mnt/project-files/serata-2026-11-20/; questa PR porta nei sorgenti le stesse correzioni. Una copia generata da `componenti.py --includi` va corretta nella sua fonte (qui la scheda di Balvar), altrimenti il riallineamento rimette il testo vecchio. «#4» resta, perché il booklet stesso dice che è il capitolo VII
- **Trovato nel repo:** `Bestiario/villain/balvar-fuocospento-cr13.md` · `07_il Portale Della Forgia Eterna/PortaleForgia-P5-B4-CARRYOVER-Forgia-Ricorda.md`
- **Solo qui:** la ricerca dei marcatori era una regex in scratchpad, non un cancello del repo

### MS-0218 · 2026-11-21 · Il corredo dei cinque draghi esce dal tesoro triplo, e i gesti contano più dei bonus

- **Data:** 2026-11-21
- **PR:** #513
- **ADR:** —
- **Temi:** draghi corredo tesoro fauci tyrgarun ozyrrandion regiarix vaereth pergamene tattiche simulatore inferred card
- **Origine:** riga del 2026-11-21 «Corredo dei draghi» in `plans/CHANGELOG.md`
- **Testo:** Jfs ha scelto sulle card del 21/11 il corredo dei cinque draghi della campagna: Fauci «A · Signore dell'assedio», Tyrgarun «A · Tempesta e ferro», Ozyrrandion «B · Il tentatore armato» (la consigliata era la A, 28.975 mo), Regiarix «A» con *lettura del magico* al posto di *resistenza*, il drago rosso di Vaereth «A». Il corredo esce dal tesoro triplo dell'SRD (tesoro standard della Guida del DM 3.5 per GS, per tre), quindi il GS non cambia. L'inventario ha mostrato che Regiarix e il drago di Vaereth non avevano gli incantesimi conosciuti: erano schede incomplete prima che sotto-equipaggiate. La misura che ha orientato le proposte: un corredo solo difensivo su Fauci (CA +2/+4, TS +2/+3) sposta gli esiti del simulatore di 1-3 punti, e Fauci fugge nel 66-94% degli scontri in ogni versione; il corredo scelto è quindi fatto di pergamene da usare in scena, scritte round per round nella tattica. Su Tyrgarun anello +3 e mantello +3 in Fase 4 danno ucciso nel 21-40% (prima 23-45%) e almeno un PG morto +0-1 punti. Catena: regolista (cinque passate, una per drago), custode del canone (1 rosso e 13 gialli, corretti tranne l'ERRATA di ARC-08, che è archivio), autore del master, lettore a freddo (3 rossi e 8 gialli), autore del master (tattiche round per round, marca dei pregen in A.5), autore dei documenti. Card aperte, scritte come INFERRED con la consigliata: (a) Fauci conosce *lettura del magico*; (b) il corredo di Fauci vale anche coi pregen; (c) *dominare persone* di Ozyrrandion su Artemis (32%) o Tordek (4%); (d) il drago di Vaereth cambia *ritirata rapida* con *raggio di indebolimento*; (e) per il freddo prima la vulnerabilità, poi la resistenza; (f) i reduci di Hammerfist raccontano che Artemis vede l'invisibile; (g) i round delle pergamene di Fauci in Sessione 4 (1-3 e 15-17). Il 21/11 fra le 06:04 e le 06:20 UTC Jfs ha chiuso tutte e sette le card sulla consigliata: le marche sono diventate CANONE, e il drago di Vaereth ha *raggio di indebolimento* al posto di *ritirata rapida*
- **Trovato nel repo:** `Bestiario/villain/Fauci_di_Palude.md` · `Bestiario/villain/Tyrgarun/tyrgarun-blue-very-old-cr19.md` · `Bestiario/villain/ozyrrandion-drago-verde-cr14.md` · `08_La Battaglia Di Hammerfist/ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md` · `plans/esperimenti/tattiche-draghi-2026-11-15/LEGGIMI.md`
- **Fuori dal repo:** `/mnt/project-files/draghi-corredo-2026-11-21/INVENTARIO-E-PROPOSTE.md` · `/mnt/project-files/draghi-corredo-2026-11-21/misura_fauci.py` · `/mnt/project-files/draghi-corredo-2026-11-21/misura_tyr.py`
- **Solo qui:** questioni aperte fuori da questa PR: `campaign/state.md` r.220 dice ancora «flees under 50 hp» per Fauci (canone 112, si corregge sul ramo di gruppo, ADR-0007); `ERRATA-ARC08-35-Verification.md` r.61 dà CA 29 (archivio, non si tocca); GS 18 o 19 di Tyrgarun (il blocco dice 19 dal 2026-11-14, il Boost log e il benchmark lo tengono a 18); «draghi rossi» al plurale nei file del Torneo; Tordek Monaco 9 (`state.md` r.94) o Barbaro 9 (carta INFERRED); il simulatore non ha i numeri nuovi (i profili sono del 15/11 e non modellano pergamene né pozioni); il corredo di Skullcrusher arriva con la PR del thread del booklet di ARC-07. Il numero MS-0214 è anche quello delle bozze #505-#509: chi entra dopo rinumera
### MS-0219 · 2026-11-21 · Skullcrusher arriva al duello con i suoi oggetti, e la runa del martello di Balvar

- **Data:** 2026-11-21
- **PR:** —
- **ADR:** —
- **Temi:** skullcrusher drago nero vecchio incantesimi conosciuti stregone oggetti tesoro anello mantello bacchetta paura pergamene dominare suggestione immagine speculare gittate eldritch spear runa zeth balvar martello boost
- **Origine:** riga del 2026-11-21 «Skullcrusher Vecchio come al duello del 20/11» in `plans/CHANGELOG.md`
- **Testo:** Durante la serata del 20/11 Jfs ha chiesto perché il drago non usasse incantesimi di paura e di dominio. La scheda dava al Vecchio i conosciuti 6/4/2/2 contro i 7/5/3/2 dello stregone di 7° dell'SRD; le card del 21/11 hanno riempito i posti con *messaggio*, *causare paura* e *spaventare*, e hanno dato al drago anello +3, mantello +3, bacchetta di *paura* e tre pergamene (circa 51.900 mo del tesoro triplo da 108.000), *immagine speculare* al corno e passate oltre i 18 m. Con l'anello il contatto sale a 13 e Tordek (+21) lo colpisce solo col 20 naturale; Jfs ha scelto di tenerlo. Il PDF della serata diceva 18 m per la deflagrazione di Artemis: con *Eldritch Spear* sono 75 m, e il colpo a 72 m giocato al tavolo era legale. Al tavolo Zeth ha ricambiato il martello di Balvar con una runa +2 al colpire contro i draghi, regola della casa
- **Trovato nel repo:** `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` · `07_il Portale Della Forgia Eterna/PortaleForgia-P1-REVISED-Corretta.md`
- **Solo qui:** il duello simulato con questi numeri dura circa 10 round e il drago muore nel 3-11% delle prove, contro i 3 round stimati da Jfs: la simulazione sottostima la mischia e non conta Durik né le evocazioni. Le varianti stanno solo nello scratchpad del thread. Il 21/11 Jfs ha sciolto le due domande: la runa del martello vale per un colpo solo, come il potere contro i draghi dei Bracieri; delle due rune di acido comprate nella sessione 4 se n'è attivata una, su Durik, alla vista del drago, e Hella si è lanciata *protezione dall'energia* (acido). L'INFERRED sulla durata stampava nel volume d'arco e teneva rosso il cricchetto delle note di lavoro (tetto 0): diventato canone, il cricchetto torna verde senza toccare il tetto

### MS-0220 · 2026-11-20 · Le piante stampano le chiavi d'area del testo, e un «;» nella descrizione non è una chiave

- **Data:** 2026-11-20
- **PR:** #506
- **ADR:** ADR-0122
- **Temi:** stampa mappe chiavi area zone pianta booklet volume standard s2
- **Origine:** riga del 2026-11-20 «ADR-0122, S2: le chiavi d'area» in `plans/CHANGELOG.md`
- **Testo:** S2 dello standard del volume chiede che i codici d'area dei titoli del testo stiano anche sulla mappa. Nel booklet della serata non ce n'era nessuno (0/0): le zone delle piante avevano lettere minuscole («a», «b»), che nessun titolo usa. La chiave entra come ultima parte di `@zone`. Nell'anteprima del 19/11 la chiave era «la terza parte», e così sedici SVG di Hammerfist, del Giardino e del Drappo cambiavano lettera: le loro descrizioni contengono già un «;» (per esempio «+4 CA; riparo per Nascondersi»). Lo ha trovato `validate_maps.py`, che confronta ogni SVG col suo master. Ora la chiave vale solo se ha la forma `[A-Z]{1,2}\d{1,2}`. Per far misurare le chiavi serve un `<!-- nuova-pagina -->` prima di ogni pianta, altrimenti i titoli finiscono sulla pagina della mappa, che S2 esclude. La pianta del duello, M7-B, non ha zone e non ha preso chiavi.
- **Trovato nel repo:** `scripts/render_map_svg.py` · `scripts/tests/test_chiavi_area.py` · `07_il Portale Della Forgia Eterna/homebrew/sessione-notte-e-alba/02-CHI-CE-STANOTTE.md`
- **Solo qui:** il testo delle voci C1-C6 e H1 è un montaggio nuovo di frasi già nel repo e aspetta la lettura del DM sulla PR; i codici stanno nel JSON delle due piante (chiave `codice` degli oggetti, letta da `compile_map_json.py`), perché i master M7-C e M7-H sono generati: la prima spinta li aveva scritti a mano nel master e `test_master_generati` l'ha bocciata
### MS-0221 · 2026-11-20 · Le skill di prosa si caricano per vincolo: hook, dodici agenti e cricchetto

- **Data:** 2026-11-20
- **PR:** #510
- **ADR:** ADR-0146
- **Temi:** skill prosa narrative-style hook pretooluse agenti sottoagenti cricchetto ci mqm claude-code thread decisione-dm misura
- **Origine:** riga del 2026-11-20 «ADR-0146 (proposta), le skill di prosa si caricano per vincolo» in `plans/CHANGELOG.md`
- **Testo:** Jfs vedeva i thread «perdere pezzi» e non usare le skill di stile. Baseline del 20/11 su cinque thread (dossier ARC-09, Skullcrusher, Eroi di Hammerfist, carte del Drappo, booklet ARC-07), lette con `list_events` del server claude-code-remote: 9 pagine, 188 chiamate, zero invocazioni di skill, zero letture di `skills/`. Taratura sullo storico: 2.944 modifiche a file di gioco negli ultimi 400 commit, 184 aggiungono un box, 16 toccano prosa pura. Card del cancello CI: Jfs sceglie il cricchetto bloccante e supera «niente cancelli di prosa nuovi» («la misura da sola non obbliga all'utilizzo»). Card degli agenti: «mettili tutti e tre», dieci agenti in tre classi; poi Jfs chiede un agente per il motore del DM (dm.py, dmcore, integrazioni) con TDD e piccoli passi, e diventano undici (`integratore-dm`); Jfs corregge anche «solo stdlib»: le librerie già nel repo sono standard e si usano liberamente; per un problema nuovo si adotta la libreria standard di fatto della comunità, che entra per i canali di ADR-0099 (unstable, testing per 14 giorni e 10 run su main, stable). Card del 20/11: un agente `piattaforma` a parte (canali, versioni fissate, promozioni, rilasci, roadmap), e sono dodici. Jfs chiede poi di vincolare il coordinatore agli agenti con gli hook: il coordinatore gira fuori dal repo, quindi il vincolo va nei thread, con `instradamento_agenti.py` (UserPromptSubmit suggerisce agente e catena riusando i trigger delle skill, Stop registra se sono stati chiamati). Misura sulle 33 frasi vere con skill attesa di `plans/instradamento/casi.json`: primo agente giusto 23, nessuno 4, sbagliato 6; per questo suggerisce e non blocca. Poi Jfs chiede un blocco tecnico: il coordinatore scrive «Catena: …» nelle istruzioni, e un PreToolUse su git push, gh pr create|ready e la PR via MCP esce 2 se mancano le chiamate Agent di quegli agenti o di autore-documenti; deroga con `--deroga "motivo"` registrata. Senza catena scritta niente blocco; Stop non blocca. Sui 144 comandi Bash del thread il riconoscimento del push prende gli 8 push veri e 1 heredoc che lo cita. `autore-documenti` aggiorna la documentazione dal diff e dai resoconti, che chiudono tutti con «Documentazione da aggiornare:». Un sottoagente non avvia altri agenti: la catena resta al thread principale. Una skill indice è stata scartata perché va invocata, ed è il passo che salta: l'albero di decisione sta in una riga del CLAUDE.md dei thread (il test ne tiene la lunghezza a 10 righe). Claude Code 2.1.329: il campo `skills:` degli agenti precarica le skill; l'hook riceve `agent_id` e `agent_type` dentro un sottoagente, e la trascrizione del sottoagente sta in `<sessione>/subagents/agent-<id>.jsonl`
- **Trovato nel repo:** `scripts/vincolo_skill.py` · `scripts/cricchetto_prosa.py` · `.claude/agents/` · `scripts/tests/test_vincolo_skill.py` · `scripts/tests/test_agenti.py` · `scripts/tests/test_cricchetto_prosa.py` · `plans/adr/ADR-0146-le-skill-di-prosa-si-caricano-per-vincolo.md`
- **Solo qui:** il campione è delle pagine più recenti di ogni thread, non delle trascrizioni intere (una pagina sono 100 eventi, circa 30 dell'assistente). Le scritture da Bash (`sed -i`, heredoc) non passano dall'hook. La norma «il box che promette» del thread del volume (`misura_craft --apertura`, #508) entrerà nel cricchetto solo quando sarà fra le norme di `punteggio_mqm`. Da misurare dopo una settimana: `vincolo_skill.py --riepilogo` nei thread


### MS-0222 · 2026-11-20 · L'appendice della regione diventa un gazetteer d'AP fatto solo col canone del repo

- **Data:** 2026-11-20
- **PR:** #507
- **ADR:** ADR-0122
- **Temi:** stampa appendice regione gazetteer hammerfist 372 booklet volume standard s4 lore canone
- **Origine:** riga del 2026-11-20 «ADR-0122, S4: l'appendice della regione» in `plans/CHANGELOG.md`
- **Testo:** Nell'anteprima del 19/11 l'appendice era una pagina sola, ripresa da DEF-4 §2. Jfs l'ha trovata striminzita e ha chiesto le stesse informazioni che danno le appendici di regione degli AP Paizo e Wizards, ma prese dal repo e non dai loro libri. Lo schema seguito è quello delle appendici degli AP: la regione in breve, la storia, la geografia, i luoghi, chi la abita, le fazioni, i PNG, le voci. In più c'è una tabella che hanno solo i viaggi nel tempo: che cosa del 372 resta nel 1372. Due scelte. Le voci sono frasi che i PNG del master dicono davvero, e non circolano le cose che sa solo il DM (la Catena, Vatore, Zeth): le voci false di un AP sarebbero state contenuto nuovo. Le date in DR sono contate all'indietro dal 372 e portano il segno ≈. Con il tema di stampa le tabelle vanno in testa alla pagina, con il titolo della sezione per didascalia; senza una riga di testo, i titoli delle sezioni restavano da soli in fondo alla colonna, quindi ogni sezione ha una frase d'apertura. Con i segnalibri annidati della #502 i `##` dell'appendice non diventano capitoli, e S4 resta giusta. Poi Jfs ha chiesto anche una mappa della regione, le lore e gli agganci. La mappa M7-R è uno schema generato da `render_schemi.py`, come M7-A, perché il repo non ha una mappa della valle del 372: le quote vengono dalle piante, le direzioni che le piante non danno (valichi a nord, orda da sud) non sono disegnate: la proposta sta nell'apparato. Il test completo ha poi trovato due cose. Le marche INFERRED in stampa rompevano il cricchetto delle note di lavoro (tetto 1 per la serata): abitanti, popoli, allineamento, conto dei difensori e pendio sono usciti dalla stampa e stanno come proposte nell'apparato. E `misura_standard_tavolo` contava anche l'apparato, che l'esportatore toglie: ora toglie apparato e storico prima di contare, con un test che fallisce senza la correzione. Gli agganci partono tutti da un fatto già scritto nel master; nessuno introduce un PNG nuovo. Al terzo giro Jfs ha chiesto meno tabelle e più profondità sui personaggi, confrontando con le appendici pubblicate. La misura sul PDF di *Burnt Offerings* (pp. 58-71) dice che il gazetteer di Sandpoint è quasi tutto prosa: 50 voci di luogo da 171 parole in media, 45 PNG presentati nel testo con razza e classe fra parentesi, tabelle solo nel blocco d'insediamento. L'appendice era al 69% di parole in tabella; ora è al 16%, con 14 PNG in prosa (114 parole in media) e gli agganci dentro le voci. Restano tabelle dove servono a tirare o a confrontare: in breve, mercato, voci 1d8, ieri e domani, i sensi. Poi i due ciechi del 20/11 sull'apertura e sulla storia. Jfs ha trovato la storia «un racconto puntuale» e ha chiesto di prendere a metro le voci di regione del manuale dei Forgotten Realms: la storia ora va a epoche datate, ognuna con una svolta, e l'apertura parte dai sensi di chi arriva, le forge sotto i piedi prima delle mura. Il secondo giro ha vinto tutte e due le coppie. Jfs ha anche chiesto di non nominare mai i PG del tavolo, perché un modulo così non lo gioca un altro gruppo: undici nomi sono diventati «gli eroi» o l'oggetto che lega l'aggancio.
- **Trovato nel repo:** `07_il Portale Della Forgia Eterna/homebrew/sessione-notte-e-alba/98-APPENDICE-TERRE-DI-HAMMERFIST.md` · `scripts/render_schemi.py` · `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`
- **Solo qui:** sulle sei proposte INFERRED del 20/11 il DM ha deciso su card: entrano i difensori (800 + 200), i nani dello scudo, legale buono e il pendio del 1372; restano fuori gli abitanti (circa duemila) e i valichi a nord; le percentuali per razza (nani dello scudo 99%, altri 1%) sono una stima che il DM ha approvato su card. Il testo è un montaggio nuovo e aspetta la lettura del DM sulla PR; S4 riconosce ancora l'appendice dal titolo e non dal `ruolo: riferimento`
