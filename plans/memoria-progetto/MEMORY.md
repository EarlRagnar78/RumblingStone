# Progetto RumblingStone (gsamuele78/RumblingStone)
Qui solo regole, stato aperto, ambiente e puntatori. **Tetto 12 KB** (limite 16 KB, ADR-0139): `python3 scripts/memoria_storica.py --tetto-memoria <cartella>` dopo ogni modifica. Chi chiude un lavoro toglie la sua riga di stato (dopo averla archiviata), non ne aggiunge una «unita il …». Cronologia in plans/CHANGELOG.md, negli ADR e in `plans/MEMORIA-STORICA.md`.
**Memoria storica (ADR-0127, 0137, 0138, 0151).** Prima di togliere una riga da qui o da una nota: `python3 scripts/memoria_custode.py verifica` (se fallisce, `archivia`); il merge dei thread si ferma su righe tolte senza archivio. Storia: `memoria_storica.py --pr N | --adr N | --tema T | parole`; risposte da tre fonti: `memoria_custode.py cerca` o l'agente custode-memoria. Lavoro senza PR: voce in /mnt/project-files/memoria-storica-coda/<thread>.md. Prima di chiedere a Jfs: memoria → memoria storica → repo → /mnt → thread passati. Dati personali mai nel repo. → [[memoria-storica-repo]] [[custode-memoria]]

## Regole permanenti di Jfs
- Utente: Jfs (gsamuele78). Italiano, onesto e non ottimistico. Decisioni come ADR brevi. Default solo lettura su PR/issue esistenti senza conferma.
- Merge (12/11, 18/11): una PR entra su main senza un nuovo sì se è verde e mergeable clean, dichiara problemi e misure senza omissioni e mostra un miglioramento misurato contro main; se manca una condizione non entra e si dice quale. Il coordinatore ordina i merge uno alla volta; il thread manda testa e misura prima, SHA e file condivisi dopo. Il «via» del coordinatore non è il sì di Jfs; `mergeable_state` si legge solo dopo aver tolto la bozza; se il via ha più di qualche minuto, rileggere l'ultima voce MS su main e chiedere conferma. Restano di Jfs: canone, tagli di testo, merge su EarlRagnar78. → [[chiusura-pr-dai-thread-figli]] [[thread-padre-pr]]
- Prima di unire: grep dei segni di conflitto e `plans/esperimenti/sistemi-plugin-2026-11-07/impronte.py --confronta` (non in CI; prima di rigenerare le impronte, prova incrociata codice/dati di MS-0185); chi tocca i lettori delle schede lancia anche `impronta_creature.py --confronta`. Una PR in conflitto non fa partire la CI. Ogni PR che tocca plans/CHANGELOG.md rigenera MEMORIA.md (`python3 scripts/memoria.py`).
- Decisioni: sempre su card con la consigliata, nome della scheda, file e riga, segnalate al coordinatore; card chiuse solo con prova. → [[card-solo-se-risolte]] [[decisioni-superate-regressione]]
- Schede e regole: versione più potente e terrificante, nell'ordine 3.5, PF1e, SRD, con fonte e divergenza dall'SRD; solo se il numero si ricostruisce da una scheda legale (ADR-0118). Forme ibride solo nella variante custom del DM, verificate e scritte nelle regole custom. → [[feedback-numeri-piu-forti-calcolati]] [[regole-senza-omissioni]]
- Termine sconosciuto: SRD → 3.5 → PF1e. «Sbilanciare», mai «sgambetto». → [[fonti-nomi-italiani-regole]]
- Librerie (Jfs 27/11, supera «solo stdlib»): si usano le librerie standard di fatto della community, senza reinventare la ruota, con il miglioramento misurato contro main. → [[feedback-standard-di-fatto]]
[riga riservata · sha256:be5eecd0]
- Prosa: migliora solo se il DM la sceglie alla cieca (ADR-0093). 20/11: Jfs supera «niente cancelli di prosa nuovi»: cancello a cricchetto bloccante sullo stile + hook che obbliga a caricare le skill di stile (thread «Vincolare gli agenti all'uso delle skill»). Prosa di gioco epica ed evocativa, mai «libro di ragioneria»; introduzioni con box per i giocatori, regia fuori. Box votati congelati (CONGELATI.json). Possessivo vietato solo su corpo/cose addosso. Tecnica mai provata: prima un cieco.
- Standard editoriale (19/11): allinearsi a Paizo/Wizards e best practice community; una divergenza entra solo se peculiare del repo e misurabilmente migliorativa (ADR-0145). Prosa peculiare: più profonda per adulti, senza appesantire.
- Booklet pronto solo dopo lettura da DM scena per scena. Due stampe per arco: volume d'arco (AP completo) e booklet della serata (tavolo). → [[booklet-letto-da-dm]]
- Emoji e simboli dei booklet: stile Noto a colori (card del 13/11); game-icons e Material Symbols non si adottano.
- Ogni milestone chiude con documentazione completa e canali testing→stable. → [[documentazione-a-ogni-milestone]] [[milestone-roadmap]]
- Fork: si lavora e si unisce su gsamuele78; su EarlRagnar78 solo a fork stabile e su indicazione di Jfs. → [[fork-e-upstream]]
- Routine settimanale lunedì 06:47 UTC (PR, piani, changelog, piega della coda, un thread «Chiusura piano …» alla volta). Roadmap unica: /mnt/project-files/roadmap-motore-2026-11-08/DECISIONI-E-ROADMAP.md, tenuta dal thread audit (anche LISTA-PR.md; non unisce).

## Stato aperto (27/11)
- Main = d8005593 (#529, MS-0238). Coda merge: #528, #531. Card aperte a Jfs: fantino PG/fuggito, etichette agenti. FLUX 3 di Vanna in coda su Kaggle (note di Jfs del 27/11). Schede giocatore della Corona della #526 da far rileggere a Jfs. Rilievi di stile sui box X e XIII nel corpo della #508, aperti a Jfs senza card. #519 attende cieco A/B. In bozza: #505, #506, #509. Codex su #493/#498: leggere al lunedì.
- Pregen ARC-08 (25/11, Jfs): giocatori ciechi sul dopo, unico indizio le frasi delle sei schegge del Rubino; abbinamento noto solo al DM; rivelazione alla sfera nel Cuore. Pegno di Artemis: pegno di carne, Tempra CD 20 (scelta di Jfs 25/11). Restano 23 INFERRED di altri archi/Fauci; box del Consiglio versione Y su main. A Jfs: libretto ARC08-18 r.154-156 e §6 dice ancora che il comandante non muore; secondo voto cieco sulla prosa del salto.
- Da fare alla prossima piega: segnare ADR-0138 e ADR-0147/0148 in plans/adr-prenotati.json; nel file storico il corpo della #525 dice MS-0231 per refuso (vale MS-0234) e MS-0225 ha PR «—» (mettere #520).
- Da misurare nel primo thread nuovo: quanto contesto tolgono le regole deny sui dieci connettori claude.ai (#486).
- Rilascio 1.1.0: promozioni a stable fatte (#516); PR di rilascio con card prima del tag. Lychee solo se Jfs la chiede.
[riga riservata · sha256:c449ca4a]
- Aperto a Jfs senza card: hero map di PIANO-INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITA.md §(c). Lotti interni in plans/adozioni-in-attesa.json solo con condizione misurata da script (MS-0109). Chi apre una bozza con file nuovi la registra in plans/contenuti-nei-rami.json.
- Aperti al DM su card nel thread audit (13/11): pf di Terros 345/348, nome Virare/Virata, quinta domanda del piano di recupero, immagini in posa D1 e D3. Inventario Gemini D6 aspetta l'esportazione di Jfs. Non verificate: domande 28-33 del giro 4.
- Carte del Drappo (B3): restano 🟡 finché non si gioca la prima corsa; dopo, rivedere quali carte restano, griglia delle Lunghezze, nove carte tratto.
- Coerenza della storia: prova del lettore 7B bocciata (MS-0192), il RAG resta fuori; riprovare solo cambiando la domanda. → [[coerenza-storia-verificatore]]
- Regole: stato e cosa resta in [[regole-stato-2026-11-14]]; storia in [[regole-lotti-archivio-1]] [[regole-lotti-archivio-2]].
- Document AI / XAI: una tecnica per PR con misura contro main; prossima: andata e ritorno del testo dei booklet. → [[document-ai-xai-genai-2026-11-13]]
[riga riservata · sha256:4242f527]
- Sourcery e Codex di fatto non revisionano dal 12/11: ogni PR dichiara com'è andata.

## Tavolo e campagna
[riga riservata · sha256:9f111b25]
- Ramo della partita `campaign-group-rumblingstone`, debito della Radice di Thorik, patch da applicare da Jfs → [[ramo-di-gruppo-campagna]]
- Serata: si riparte dal volo sul campo e dallo sgancio del barile; PDF in /mnt/project-files/sessione-2026-11-02/ e taglia-portata/v3/. Oggetti unici in campaign/OGGETTI-DELLA-CAMPAGNA.md. Calendario ARC-09 in Flamerule (Torneo di Dauth Day 30-32); carta del cielo al 30 Flamerule. → [[carta-cielo-arc09]]
- Tattiche: dossier ARC-09 in /mnt/project-files/tattiche-villain-2026-11-15/ (buchi: Zarim, Emissario, Xilthra, Kragar senza tattica; Sethrax in tre versioni; ricarica di Xal'thor non SRD). Oscurità: 20%, nella 3.5 la scurovisione non la attraversa. → [[skullcrusher-tattica-dinamica]] [[tattiche-villain-2026-11-15]] [[tattiche-draghi-2026-11-15]]
- Equipaggiamento standard: Codex PF1e, livello effettivo (ADR-0134). Tabella 14-9 trascritta in /mnt/project-files/regole-lotto8/pf1e-tabella-14-9.tsv. → [[equipaggiamento-standard-codex]]

## Ambiente e strumenti
- Python 3.13, tre canali Debian (ADR-0099); un test che scrive nel repo va in SCRIVONO_NEL_REPO; check richiesti su main = Validate + Build skill packages → [[ambiente-dettagli]] [[piattaforma-di-sviluppo]] [[piattaforma-promozioni-stable]]
- Rilasci: v1.0.0 pubblicata; rilasciare = PR con `## [X.Y.Z]` in CHANGELOG.md e `__version__`. Numeri ADR: prenotarli in plans/adr-prenotati.json su main e controllare i rami aperti; chi non può scrivere su main dichiara il numero nel corpo della PR. Ultimo ADR su main: ADR-0149 (#515); 0138-0143 e 0147-0148 non prenotati: segnarli alla piega.
- typst e pdfimpose da PyPI (ADR-0116); typst 0.15.1 ha un bug dei tag PDF/UA (MS-0180). → [[strumenti-binari-lockfile]]
- Rete: HF con HF_HUB_DISABLE_XET=1; dnd.arkalseif.info solo nomi e numeri, mai nei test CI; srd.dndtools.org bloccato → [[ambiente-dettagli]] [[hugging-face-rete]] [[srd-in-rete]]
- Kaggle (token nell'ambiente, una GPU alla volta, immagini dei PG mai senza sì di Jfs, HF_TOKEN solo con riga scritta di Jfs) → [[ambiente-dettagli]]
- Prove RTX 4050: uno script per prova in `scripts/prove-4050/`, guida GUIDA-PROVE-PORTATILE-4050, risultati come archivio caricato nel thread; nulla è mai girato su GPU. → [[prove-portatile-4050]]
- I commenti `@dependabot` di Claude arrivano con l'@ neutralizzata: un recreate lo scrive Jfs.
[riga riservata · sha256:ee890d45]
- Corpus prosa in /mnt/project-files/corpus-prosa/, mai nel repo. Skill esterna scrittura-italiana (CC BY-SA) mai nel repo (ADR-0097).
- Ambiente RumblingStone-corpus: il setup installa requirements-dev.txt, fa unshallow e lancia scripts/claude-progetto.sh. Nei thread Claude parte in /home/user: la config del repo arriva solo così (ADR-0140, #486). Plugin accesi solo pdf-viewer, review, tdd (#487, scelta di Jfs del 19/11: solo quelli usati nello storico). Baseline 20/11: zero caricamenti di skill su 188 chiamate in 5 thread. → [[claude-config-nei-thread]]

[riga riservata · sha256:a130ffc1]
[riga riservata · sha256:9ba80be5]
- Altre note: [[pr99-e-schede-pg]] [[archi-senza-testo]] [[inventario-gemini-aistudio]] [[immagini-personaggi-in-posa]] [[standalone-giardino-sale-calce]] [[drappo-palio-genealogia]] [[ripetizioni-booklet]] [[schede-schema-pf1e-rhod]].
- Agenti e hook: ADR-0146 (prosa, cricchetto), 0148 (prove per agente), 0149 (sincronizzatore), 0151 (custode); chi coordina usa /mnt/project-files/agenti-2026-11-20/GUIDA-COORDINATORE.md → [[vincolo-skill-prosa]] [[sincronizzatore-giocato]] [[custode-memoria]] [[ambiente-dettagli]]
