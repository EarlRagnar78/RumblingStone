# 📚 ARCHIVIO PIANI — INDICE

> **Cos'è**: la vista d'insieme di tutti i piani di lavoro della campagna
> (revisioni, infrastruttura), con stato, % di completamento, lotti
> rimanenti e gate. Creato dal Lotto **K-A** del piano DM-TOOLKIT (K-D3).
>
> **Regola di manutenzione** (regola d'oro 4 dei piani): *chi chiude un
> lotto aggiorna — nello stesso commit — (1) la checklist del piano,
> (2) la riga qui sotto, (3) una riga in `plans/CHANGELOG.md`.*
>
> Le decisioni architetturali (il "perché" delle scelte di struttura)
> vivono in `plans/adr/`.

## Stato dei piani

| Piano | Ambito | Stato | % | Lotti/task rimanenti | Gate |
|---|---|---|---|---|---|
| [PIANO-REVISIONE-ARC07](PIANO-REVISIONE-ARC07-COERENZA-E-QUALITA.md) | Arco 07 — Portale della Forgia Eterna | 🟡 quasi completo | ~95% | B1 parziale: date/XP/loot **reali** dei log ricostruiti | sessioni giocate al tavolo |
| [PIANO-REVISIONE-ARC08](PIANO-REVISIONE-ARC08-COERENZA-E-QUALITA.md) | Arco 08 — Battaglia di Hammerfist | ✅ completo | 100% | — | — (l'arco resta ⬜ da giocare: il *piano* è chiuso, il *gioco* no) |
| [PIANO-REVISIONE-ARC09](PIANO-REVISIONE-ARC09-COERENZA-E-QUALITA.md) | Arco 09 — post-Hammerfist | ✅ completo | 100% | — | — (idem) |
| [PIANO-REVISIONE-TRASVERSALE](PIANO-REVISIONE-TRASVERSALE-COERENZA-E-QUALITA.md) | Rituale P3B · Mappe · Artefatti (tutta la campagna) | 🟡 gated dal tavolo | ~95% | T8 (sinergie Collana) · chiusura T9 (esito P3B in state.md §8) · SVG dei 16 narrativi (opzionale/estetico) | T8: quest ARC-09 giocata · T9: P3B giocato |
| [PIANO-DM-TOOLKIT](PIANO-DM-TOOLKIT-HYPE-E-ARCHIVIO-PIANI.md) | Infrastruttura: CLI dm.py · hype Homebrewery · questo archivio · **standard booklet [ADR-0013](adr/ADR-0013-standard-generazione-booklet-sessioni.md)** (K-B9…K-B11: builder pergamena, teaser spoiler-free, doppia via HTML/`.hb.md`) | ✅ completo | 100% | — | — (code da tavolo: verifica visiva dei brew al collaudo del container; piloti lettera/avviso-torneo quando il DM fornisce testo canone) |
| [RICERCA-GENERATORI-MAPPE](RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md) | Infrastruttura: pipeline mappe qualità AP — renderer "pergamena", import Watabou, export PNG, skill `rumblingstone-mapmaking` | 🟡 completo + follow-up in review | ~100% | Ultra-Clear P4 Piano Terra (PR #42 **aperta**, non mergiata) | — (hero map ComfyUI: opzionale, macchina DM con GPU; giudizio a occhio caso per caso) |
| [INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITÀ](PIANO-INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITA.md) | Infrastruttura: 3 modalità mappa, contratto JSON+validatore (Mod. 3), export UVTT/dd2vtt (Foundry/Roll20), infra container ComfyUI su Bazzite, **overlay professionale mappe** (bussola/movimenti/callout/zone, ADR-0006), direzione artistica IP-safe | 🟡 M1-M5 implementati, collaudo al tavolo | ~92% | collaudo DM: import `.uvtt` in Foundry, setup container ComfyUI su GPU; opz.: convertire Campo Drow 2/3 in JSON | collaudo al tavolo/macchina DM |
| [PIANO-RENDER-MAPPE-FEDELTÀ-DETTAGLI](PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md) | Infrastruttura: renderer mappe a **fedeltà piena** (ASCII ultra-clear → SVG senza perdere posizioni/annotazioni/token) | 🟢 **eseguito** (2026-07-23): F1-F6 nucleo completo, 6 SVG ARC-07 resi, 17 legacy byte-identici | ~95% | opzionale: callout grafici ancorati (F3 pieno), `--strict` come default | — |
| [PIANO-IMPORT-ULTRACLEAR](PIANO-IMPORT-ULTRACLEAR-ASCII-TO-JSON.md) | Infrastruttura: `import_ultraclear.py` — ASCII ultra-clear → **bozza JSON contratto + report conflitti** (migrazione semi-automatica delle mappe esistenti) | 🟢 **eseguito** (2026-07-24): F1-F7 completi — registro R1-R10, report `editor-ready` (`map_conflicts.schema.json`), golden case Hammerfist verde, 17 test + CI | ~100% | opzionale: migrare al contratto le altre ~30 mappe ultra-clear (al tavolo/DM); il `--json-report` sarà consumato dall'editor visuale (Piano 2) | — |
| [PIANO-EDITOR-VISUALE-MAPPE](PIANO-EDITOR-VISUALE-MAPPE-TATTICHE.md) | Infrastruttura: **editor visuale a griglia** (progetto separato) che round-trippa col contratto JSON — alternativa domain-fit a FreeCAD | 🔵 **pianificato** (2026-07-23) | 0% | E0 ADR + scaffold, E1 legenda condivisa `legend.json`, E2-E10 (canvas/strumenti/import/export/e2e/packaging/test/doc) | E0: ADR «editor come progetto separato» |
| [PIANO-AUTOMAZIONE-STATO-SESSIONI](PIANO-AUTOMAZIONE-STATO-SESSIONI-BRANCH-GRUPPO.md) | Infrastruttura: `dm.py session` — wizard fine-sessione, apply engine `state.md` (regioni marcate), visibilità per-PG, brief prossima sessione, branch-per-gruppo con guardia su `main` | 🟢 implementato (A-F ✅, LLM E-bis escluso per decisione DM; [ADR-0007](adr/ADR-0007-scritture-canone-triplo-vincolo.md); wizard, per-PG, hook ❓, 31 test in CI; Quick Guide nuovi DM) | ~98% | — | collaudo al tavolo del flusso `session end` alla prima sessione reale |
| [PIANO-AUDIT-SCRIPTS](PIANO-AUDIT-SCRIPTS-QUALITA-E-CONTRATTI.md) | Infrastruttura: audit qualità script + **contratto machine-readable** (manifest/registry/MCP), normalizzazione CLI, `docs/INDEX` categorizzato, de-collisione `Script/`→`converters/` ([ADR-0011](adr/ADR-0011-de-collisione-scripts-converters.md)), **standard ingegneria verificabile in CI** ([ADR-0012](adr/ADR-0012-standard-ingegneria-tool-verificabile.md)) | 🟢 **eseguito** (2026-07-24): F0-F7, 70/70 test verdi, `tools_manifest --check` pulito | ~100% | opz.: shellcheck bloccante · convertitori allo standard pieno · fallback pyyaml in compress_skills | — |
| [PIANO-REINTEGRAZIONE-PNG-AP-RHOD](PIANO-REINTEGRAZIONE-PNG-AP-RHOD.md) | Contenuto: reintegrazione PNG dell'AP originale (Guado di Drellin, Rethmar 2° anello, Witchwood/Tiri Kitor, Wyrmlord) + proposta PNG caotico Lirien | ✅ **completo** (2026-07-20): R1-R7 tutti chiusi | 100% | — | — (canonizzazione dei lotti di preparazione R2/R3 a valle, in gioco) |
| [PIANO-INCANTATORI-MEMORABILI](PIANO-INCANTATORI-MEMORABILI-MANO-ROSSA-E-DROW.md) | Contenuto: incantatori nuovi per Mano Rossa (generale ogre magi elementalista + comprimari ogre sotterranei) e drow di Sonjak (illusionista-ombra, trickster arcano, assassina) + **ala orchesca in equivalenti SRD** (chierico di Gruumsh, bruto deforme del Sottosuolo, Ushgar «Occhio Reso» con ramo politico sulla faglia Gruumsh/Tiamat) — 9 schede + 3 dossier, tarati sulle difese reali del party (Mind Blank di Thorik, vulnerabilità al fuoco di Hella) + **indice d'uso di una web enhancement di fonte privata** (roster valutato contro il benchmark, ricette di adattamento, errata; solo puntatori, nessuno statblock trascritto) | ✅ **completo** (L6 approvato dal DM 2026-08-05): materiale a `[ACCEPTED — DM-canon]`, righe applicate in `state.md` §3/§4/§5/§7.E/§8 | 100% | — (resta l'assegnazione dei token, cosmetica) | — |
| [PIANO-SFIDE-COMBINATE](PIANO-SFIDE-COMBINATE-INCANTATORI-E-FORZA-BRUTA.md) | Contenuto: **sei pacchetti di scontro** che combinano gli incantatori SRD del repo, i comprimari di forza bruta e quattro statblock di fonte privata (solo puntatori a pagina) — EL calcolati, apertura round per round, che PG mette sotto pressione, uscita; + **Ghaurush GS 18** con *muro di forza*, dichiarato sopra il tetto e segnalato come «fuggi o muori». Principio guida: contro questo gruppo l'architettura dello scontro conta più del grado del mostro — **sette** sfide dopo l'aggiunta di «Il Sangue Sbagliato» (ondata di tanarukk con resistenza al fuoco e RI, specchio della sfida A: toglie la soluzione agli incantatori e la restituisce alla mischia) | ✅ **completo** (S4 deciso dal DM 2026-08-05): sfide approvate; **sfida E** solo come variante *Advanced* GS 17 dentro il tetto; **faglia della sfida G aperta** | 100% | — (S7, CdP Signore della Guerra Orchesco, **non presa**: Ushgar resta Barbaro 13) | — |
| [PIANO-INNESTI-SFIDE](PIANO-INNESTI-SFIDE-NEI-BEAT-DI-CAMPAGNA.md) | Contenuto: **dove vanno le sfide dentro il canone giocato** — sei innesti (Hammerfist ≈372 DR, Battaglia di Hammerfist, Notte dei Drow, viaggio Giorni 33-38, Torneo di Dauth, Torre Invisibile), ciascuno con slot canonico verificato, EL, e un aggancio che muove qualcosa di tracciato (clock §3, numeri §2.4, echi §7.E). Include le **esclusioni motivate**: niente tanarukk né Ghaurush a 372 DR (verifica di epoca), e il vincolo di collisione col Giorno 3 del Torneo | ✅ **completo** (N4 deciso dal DM 2026-08-05): **tutti e sei** gli innesti approvati; attori in `state.md` §3/§4/§5, eco **E-08a** in §7.E | 100% | — | — |
| [PIANO-DRAPPO-DI-TARSILIA](PIANO-DRAPPO-DI-TARSILIA-STANDALONE-PF1E.md) | Contenuto: **modulo autonomo** — il sistema del Palio riambientato a **Golarion** e convertito a **Pathfinder 1e**, sei schede pregenerate di 3°, tre sessioni da 3-4 ore, città originale (Tarsilia, Regno dei Fiumi). Zero dipendenze da Forgotten Realms / Red Hand of Doom: è la strada indicata da [ADR-0005](adr/ADR-0005-confini-ip-uso-non-commerciale.md) e messa in coda da [ADR-0016](adr/ADR-0016-lingua-sorgente-e-edizioni.md) §2 | 🟡 Lotti 1-2-5 chiusi (impianto · profondità AP · **apparato d'uso** · 4 booklet con PDF · ADR-0017/0018 · gate CI); L6 con capitolato scritto | ~90% | L6 edizione illustrata (raster, tipografia embedded, mappa giocatore, PDF unico, carte, copertina) · L3 collaudo al tavolo (durate reali, alfa→beta) · L4 edizione pubblicabile (rinomina contrade **sospesa per scelta DM**, 4 figure di stemma, audit IP) | L6: nessuno, il prompt è pronto · L3: una sessione vera · L4: decisione DM su ADR-0005 |
| [RICERCA-MODULO-PUBBLICABILE](RICERCA-COSA-SERVE-A-UN-MODULO-PUBBLICABILE.md) | Metodo: **cosa separa un modulo scritto bene da uno che si gioca** — audit del divario su apparato d'uso, memorabilità, continuità fra sessioni, collaudo; e cosa di tutto ciò diventa canone della campagna | ✅ completa, attuata nel Lotto 5 del piano Drappo | 100% | ⬜ B3 carte da tavolo · ⬜ C3 recap automatico fra le serate · ⬜ D5 budget incontri PF1e come script | tutti e tre gated su una sessione vera: senza tempi reali si ottimizzerebbe alla cieca |
| [RICERCA-TOOL-ESTERNI-DM](RICERCA-TOOL-ESTERNI-DM-2026-08.md) | Metodo: **cosa vale la pena prendere dal panorama dei tool per DM** (agosto 2026) — categorie, verdetto per tool con licenza verificata, e le quattro soglie per gli import futuri. **Seconda passata sul testo vero dei thread** (fornito dal DM): cinque nomi nuovi e un'obiezione fondata alla raccomandazione principale | ✅ completa · **R2 applicato** (ancora storica per le immagini: `stile-illustrazione-handout.md` + prompt del Drappo) | 100% | ⬜ **R1** trascrizione locale della sessione (whisper.cpp, MIT, offline) → bozza di verbale per `session_recap.py`: chiude C3 ma richiede un ADR (prima dipendenza da binario esterno), la regola del consenso e il campo «cosa hanno capito male» · 🔎 conferma che **D5** (budget incontri PF1e) non era un capriccio | decisione DM sull'ADR della dipendenza esterna |
| VERIFICA LEGALE-IP (P2D "Palio") — [ADR-0005](adr/ADR-0005-confini-ip-uso-non-commerciale.md) · [rapporto](../09_Continuazione%20Arco%20Narrativo%20dopo%20Battaglia%20di%20Hammerfist/Arco-Post-Hammerfist-P2D-PALIO-VERIFICA-LEGALE-IP.md) | Conformità IP: Regolamento/Consorzio Palio di Siena + blocco WotC/Forgotten Realms | ✅ verifica completata (PR #47) | 100% | bonifica §7 (rinomina contrade/livree/motti, "Piazza il Campo", riambientazione fuori FR) — **solo se** si punta a edizione commerciale. 🔎 **Dal 2026-08-14 la bonifica è dimostrata su un modulo a parte**: `STANDALONE-Il-Drappo-di-Tarsilia/` chiude 8 punti su 8 del §7 (resta aperta la sola sostituzione delle figure degli stemmi) — l'arco P2D di Channathgate **resta invariato** | decisione DM su uso commerciale (non presa) |

## Prossimi passaggi (volutamente in bianco — si riempiono al tavolo / su decisione DM)

### PIANO-REVISIONE-ARC07
- ⬜ _(da definire al tavolo: date/XP/loot reali per chiudere B1)_

### PIANO-REVISIONE-ARC08
- ⬜ _(nessuno pianificato — eventuali emergenze dal gioco dell'arco)_

### PIANO-REVISIONE-ARC09
- ⬜ _(nessuno pianificato — eventuali emergenze dal gioco dell'arco)_

### PIANO-REVISIONE-TRASVERSALE
- ⬜ _(T8: quando la quest ARC-09 di Hella è giocata)_
- ⬜ _(chiusura T9: quando il P3B è giocato — esito reale in state.md §8)_

### PIANO-DM-TOOLKIT
- 🟡 _(K-B3.9 — tavole di Channathgate ricollocate in `immagini/` + ridimensionate con Pillow: **PR #46 aperta**, non mergiata; le tavole PNG del DM sono già su main via `ed56aa6`)_
- ⬜ _(riapertura estetica K-B0 solo se il DM indicherà template specifici del pack)_
- ⬜ _(collaudo al tavolo: container + brew I-V; piloti lettera/avviso-torneo quando arriva testo canone)_

### RICERCA-GENERATORI-MAPPE
- 🟡 _(P4 Piano Terra → griglie Ultra-Clear, dall'agguato Xorn al boss Terros: **PR #42 aperta**, non mergiata — quando merge, tracciare qui e in CHANGELOG)_
- ⬜ _(opzionale/estetico: portare a griglia Ultra-Clear le altre mappe KO del censimento — Torre P2A, Torneo P2B, Battaglia Finale P3 — ora che il renderer c'è)_
- ⬜ _(mappa regionale Cannath Vale/Dalelands con Azgaar FMG — `.map` master + export in rendered/)_
- ⬜ _(hero map ComfyUI sulle 2-3 mappe chiave — solo su macchina DM, vedi skill mapmaking)_

### INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITÀ
- ⬜ _(collaudo DM: generare una mappa Mod. 3 reale da JSON per un incontro ARC-08/09 e renderla)_
- ⬜ _(collaudo DM: importare un `.uvtt` in Foundry e verificare muri/luci)_
- ⬜ _(collaudo DM: setup container ComfyUI su Bazzite con GPU + hero map su una mappa chiave)_

### PIANO-AUTOMAZIONE-STATO-SESSIONI
- ⬜ _(collaudo al tavolo: primo `dm.py session end` — wizard incluso — su una sessione reale del gruppo, sul branch `campaign-group-rumblingstone-dm-gianfranco`)_
- ⬜ _(opzionale, decisione DM futura: lotto E-bis LLM per evoluzioni narrative — oggi escluso)_

### PIANO-IMPORT-ULTRACLEAR
- ✅ _(F1-F7 eseguiti 2026-07-24: `scripts/import_ultraclear.py` + `scripts/schemas/map_conflicts.schema.json` + 17 test + smoke CI + doc skill — branch `claude/piani-completare-5b85qg`)_
- ⬜ _(opzionale: migrare al contratto JSON le altre ~30 mappe ultra-clear del censimento — un file alla volta, risolvendo i conflitti segnalati; da fare al tavolo/su decisione DM)_
- ⬜ _(gancio Piano 2: l'editor visuale consuma `--json-report` per evidenziare le celle in conflitto e applicare le `actions`)_

### PIANO-EDITOR-VISUALE-MAPPE
- ⬜ _(E0: ADR «editor come sotto-progetto separato» — decisione stack/offline/confini, prerequisito a tutto il front-end)_
- ⬜ _(E1: `export_legend_json.py` → `legend.json` + gate CI di sync — prerequisito tecnico con valore autonomo, candidabile per primo)_
- ⬜ _(E2-E10: canvas griglia, strumenti, import Watabou/bozza-ultraclear, export contratto, round-trip e2e, packaging offline, test Playwright, doc)_

### PIANO-INCANTATORI-MEMORABILI
- ✅ _(L6 chiuso 2026-08-05: **approvato tutto**. 13 file a `[ACCEPTED — DM-canon]`; tre clock villain in `state.md` §3, conoscenze in §4, ramo terra in §5, eco E-08a in §7.E, changelog §8)_
- ✅ _(ramo di Ushgar: **aperto**, con l'ordine deciso dal DM — prima l'uscita laterale di **Hella** (il Cerchio non si oppone all'insediamento), la firma di Thorik solo come secondo passo. La penale «perdita status Custode Eterno» scatta **solo** se si arriva alla firma del nano)_
- ⬜ _(unica coda cosmetica: assegnare i token in `Bestiario/tokens/`)_
- ✅ _(ex-opzionale: l'ogre deforme del Sottosuolo da fonte privata è stato risolto in L7 come **equivalente SRD** — `bruto-deforme-sottosuolo-cr11.md`. Nessuna citazione di fonte privata necessaria)_

### PIANO-SFIDE-COMBINATE
- ✅ _(S4 chiuso 2026-08-05: **sfide approvate**. La scelta operativa passa dagli innesti I1-I6)_
- ✅ _(S5 chiuso 2026-08-05: scheda tanarukk fornita dal DM → sfida **G** «Il Sangue Sbagliato». Con correzione dichiarata: avevo dedotto GS 6, il tanarukk base è **GS 6 solo con Barbaro 4** — da solo è **GS 2**)_
- ✅ _(S6 chiuso 2026-08-05: scheda orchi montani fornita dal DM. Esito onesto: **nessun nemico nuovo** — i tratti sono identici all'orco SRD, quindi le schede orchesche del repo *sono già* orchi montani. Il valore sta altrove, in §2-ter dell'indice)_
- ✅ _(deciso 2026-08-05: **la faglia si apre**. Ushgar **non** ha «Adattamento alla Luce» e il Controllo delle Fiamme **fa scattare** la cecità alla luce — i tanarukk possono accecare i propri comandanti)_
- 🚫 _(S7 **non presa** 2026-08-05: Ushgar resta Barbaro 13. La CdP resta disponibile se un giorno servisse)_
- ✅ _(deciso 2026-08-05 sulla sfida **E**: **non come primo incontro**. Si usa la variante *Advanced* **GS 17** (EL 17, dentro il tetto); la GS 18 col *muro di forza* resta per il ritorno, e solo se il primo Ghaurush è scappato)_

### PIANO-INNESTI-SFIDE
- ✅ _(N4 chiuso 2026-08-05: approvati **tutti e sei** gli innesti I1-I6)_
- ⚠️ _(vincolo da rispettare: l'innesto **I5** va al **Giorno 1 o 2** del Torneo di Dauth, mai al Giorno 3 — quel giorno è già occupato dall'assalto di Xal'thor e dallo smascheramento di Sethrax, e tre trame nella stessa scena si annullano)_

### PIANO-DRAPPO-DI-TARSILIA
- ✅ _(Lotto 1 chiuso 2026-08-14: `STANDALONE-Il-Drappo-di-Tarsilia/` — hub, 8 contrade, regolamento della corsa PF1e, 6 pregen, 3 sessioni, statblocchi, 2 mappe dal contratto JSON, prompt d'illustrazione, nota IP)_
- ✅ _(Lotto 2 chiuso 2026-08-15: profondità da modulo AP — luoghi e intrigo, rito d'Investitura + 18 eventi personali, agende villain ora per ora, guida DM minuto per minuto, fascicolo schede con matrice dei legami, tavole vettoriali, playtest alfa con 9 correzioni applicate, 3 booklet + 22 PDF)_
- ⚠️ _(nomi senesi ripristinati su decisione DM 2026-08-15: la bonifica §7.1 è **sospesa**, non chiusa. Nota IP riscritta di conseguenza)_
- ✅ _(Lotto 5 chiuso 2026-08-15: apparato d'uso — cassetta del DM, 4 prop stampabili, stato del modulo con Echo Ledger, schede di feedback; **skill `rumblingstone-playtest`**; **`validate_standalone.py`** in CI; **ADR-0017** moduli autoconclusivi e **ADR-0018** apparato d'uso obbligatorio; module-standard §15-16; export UVTT)_
- 🟡 _(Lotto 6 aperto 2026-08-15: **capitolato dell'edizione illustrata** — `PROMPT-GENERAZIONE-BOOKLET-DEFINITIVO.md` misura i sei divari verso il livello Paizo/WotC (raster, tipografia embedded, mappa versione giocatore, PDF unico con segnalibri, carte da tavolo, frontespizio) e contiene il prompt autosufficiente per eseguirli in una sessione a parte)_
- ✅ _(Lotto 8 chiuso 2026-08-16: **le sei pregenerate diventano schede vere** — una pagina A4 a testa, fascia alta col ritratto dipinto, pannello sinistro «chi sei» e destro con lo statblocco, piede «come si gioca in un minuto». `scripts/typst/scheda-pg.typ` + `scripts/dmcore/schede.py`, accesi da `"layout": "schede"` nel manifest: i dati restano nei due master del tavolo, non ne esiste una seconda copia)_
- ⬜ _(L3 — collaudo al tavolo: durate reali per giornata, punti morti, prove mai usate. **Gated**: serve una sessione giocata)_
- ⬜ _(L2 — i sei ritratti e le tre tavole: i prompt ci sono, i PNG li produce il DM con ComfyUI locale)_
- ⬜ _(L3 — edizione pubblicabile: sostituire almeno 4 figure su 8 negli stemmi (restano oca/torre/bruco/istrice), rigenerare i cartigli coi motti nuovi, audit IP del solo standalone. **Gated** su ADR-0005)_

### VERIFICA LEGALE-IP (P2D "Palio")
- ⬜ _(bonifica §7 — rinomina contrade, cambio livree, riscrittura motti da zero, rimozione "Piazza il Campo", riambientazione fuori Forgotten Realms: **gated** su una decisione DM di puntare a un'edizione commerciale, non ancora presa — vedi ADR-0005)_
- ⬜ _(debito documentale a bassa priorità: correggere la nota IP interna che dichiara i motti "originali" — sono parafrasi §3.3; documentare provenienza/licenza delle 2 tavole PNG del DM)_

### PIANO-REINTEGRAZIONE-PNG-AP-RHOD
- ✅ _(R2 — secondo anello di Rethmar preparato 2026-07-20: `Bestiario/png/Secondo_Anello_Rethmar/`)_
- ✅ _(R3 — Witchwood/Tiri Kitor preparato 2026-07-20: `Bestiario/png/Witchwood_Tiri_Kitor/`; Killiar cross-linkato allo statblock d'arco)_
- ✅ _(R4 — deciso dal DM 2026-07-20: Hravek Kharn fuso in Karruk; Ulwai non reintegrata 1:1; blackspawn rilivellati → tier élite CR 13 «Razorfiend Blackspawn Alfa»)_
- ✅ _(R6 — canonizzazione DM di R1+R5 avvenuta il 2026-07-20: flag sciolti, righe applicate a state.md §1/§3/§7/§8)_
- ✅ _(R7 — Mira Serani «l'Aranea»: reintegrata + twist figlia-di-Lorana; statblock **canon CR 8** calibrato PG 8-9 (ramo APL-13 CR 11/13-14 nel dossier); collisione risolta: «Mira del Traghetto» → «Nania Seriv del Traghetto»)_
