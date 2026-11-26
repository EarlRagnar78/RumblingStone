# 🧠 MEMORIA — il lavoro su RumblingStone in un posto solo

> **Generata da `scripts/memoria.py`: non si scrive a mano** ([ADR-0087](plans/adr/ADR-0087-la-memoria-del-lavoro-e-generata.md)). Ogni riga viene da una fonte che ha la sua casa, e il link porta lì: si corregge la fonte, poi `python3 scripts/memoria.py`. La CI boccia questo file se resta indietro.

## Come si riparte, in una sessione nuova

```bash
git fetch --prune origin
python3 scripts/memoria.py --check      # questa pagina è allineata?
python3 scripts/decisioni_dm.py --check # le decisioni aperte
python3 scripts/fase1.py <file>         # sempre, prima di toccare
python3 scripts/memoria_storica.py --pr N  # la storia di una PR, di un ADR, di un tema
```

Poi si legge questa pagina dall'alto: prima cosa aspetta il DM, poi da dove riparte l'agente. Le regole di lavoro stanno in [`AGENTS.md`](AGENTS.md).

## Aspetta il DM: 1 decisioni aperte

Fonte: le tabelle `decisioni-dm` dei piani, aggregate in [STATO-E-ORDINE §4](plans/STATO-E-ORDINE-DEI-PIANI.md). Si risponde col numero e il piano: *«CODA-SECONDO-LETTORE D2 sì»*.

| Piano | # | Ambito | Domanda |
|---|---|---|---|
| `RIPRESA-PR` | D2 | F3 · 3d | **Riformulata il 2026-09-11: la domanda di prima partiva da un fatto falso.** Diceva *«i diciotto raster si generano sulla tua macchina — quando?»*, ma **esistono tutti e diciotto** (più le due extra), generati dal DM *… |

### Revisioni della prosa da approvare: 0

Fonte: i documenti `REVISIONE-*.md` sotto `plans/scrittura/` che `ciclo_prosa.py applica` può ancora applicare. Ogni cartella ha un `LEGGIMI.md` con i passaggi interi.

Nessuna.

## ▶ In corso: da qui si riparte: 5

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **P01 · MASTER-DEF: A3 chiuso, D4 e D5 decise** (#259, ARC-08: il collo e l'ala nella presa di Thorik, ADR-0096) | [MASTER-DEF](plans/PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md) A3 | merge della #259 quando il thread dà il via; poi S1-S4 |
| **P02 · AVVENTURE-COMMUNITY 7c**: D4-D6 decise dal DM il 2026-10-23 e applicate (ARC-08 allineato al Bestiario nella #286, possessivo vietato solo sul corpo, fronti e orologi canone da ARC-08). Resta il primo… | [AVVENTURE-COMMUNITY](plans/PIANO-AVVENTURE-COMMUNITY-2026-10.md) §Decisioni | il thread di ARC-08, col prossimo master |
| **P03 · ARC-07 riscritto con le norme nuove**, misurato contro le versioni di prima (tag `prima-rifacimento-arc07`), e l'handout del contratto del Seme da portare in `ARC07-HANDOUTS` | ADR-0093 · `/mnt/project-files/contratto-seme/` | il thread |
| **P04 · LLM locale, la prova del 12B sull'ASUS e del 26B sulla Dell** (gemma4 e4b bocciato, #234 su `main`) | [ADR-0089](plans/adr/ADR-0089-un-llm-locale-per-la-prosa-si-misura-prima.md) · `plans/scrittura/` | una PR nuova dal thread |
| **P16 · Le marcature rimaste nel contenuto**: rimisurate il 2026-11-04 con `inventory_inferred.py` corretto (righe di regola in «meta», note che vanno a capo contate): **240 aperte su `main`**, non 44 (il `grep` vedeva… | … | le card di ARC-08, poi un lotto per arco: ARC-07, ARC-09, il resto |

## 🙋 Aspetta il DM: 10

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **P06 · Accettare le ADR ancora «proposta»**: ADR-0090 (la partita sul ramo di gruppo nuovo, dal 2026-10-11), ADR-0094 (il giro si misura contro la versione di prima), ADR-0095 (correzione, verifica e seconda passata).… | `plans/adr/` | un sì o un no per ADR; l'agente cambia lo stato e la riga di CHANGELOG |
| **P07 · Le decisioni numerate dei piani**: resta solo RIPRESA-PR D2 (l'arte del Drappo: Gemini o la pipeline locale con FLUX.2 klein, da scegliere guardando 2-3 tavole, metodo del DM dell'8/11). Rimisurata il 2026-11-16… | §4, generata da `decisioni_dm.py` | rispondere col piano e il numero: *«RIPRESA-PR D2 A»* |
| **P08 · Le patch di `state.md` sul ramo di gruppo**, scritte e mai applicate (verificato su `ce34599`): il Bane di Aegis Fang contro Fauci (affresco A7); la Cintura della Devastazione a 4 cariche al giorno (lo stato dic… | `/mnt/project-files/ramo-di-gruppo-2026-11-05/` (serie unica 0001-0004, provata su `ce34599` il 2026-11-05: ingloba le… | `git am --3way` sul ramo `campaign-group-rumblingstone`, passi in `docs/how-to/GUIDA-PATCH-RAMO-DI-GRUPPO.md` |
| **P09 · Le domande di canone lasciate aperte dai thread di ARC-07 e ARC-08**: restano le domande 28-33 del giro 4 (non riverificate). Chiuse: i pf di Terros (348, deciso dal DM il 2026-11-13); *Virata* (si chiama «Virar… | `plans/esperimenti/giro4-arc07-2026-10-19/DECISIONI-DM.md` · `DEF-4` · `ARC08` | una risposta per domanda; l'agente le porta nei master in una PR |
| **P10 · Mappe, le scelte del DM**: texture e tessere nella pagina di scelta (R8, livello B), la prima immagine di ComfyUI (R4-quinquies), il giro di prova sui modelli 3D CC0 e lo zip Standard di Quaternius (R4-ter), il… | [RESA-ASSET](plans/PIANO-RESA-E-ASSET-DELLE-MAPPE.md) §8 · [COLLAUDO-MAPPE](plans/PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md) | DM; poi l'agente mette le tessere nel tema e rimisura |
| **P11 · I collaudi che solo il DM può fare**: l'import `.uvtt` in Foundry (INTEGRAZIONE, ~92%), il gate κ ≥ 0,6 (MISURA-EDITORIALE, ~90%), la prova del blocco dei segreti (PRATICHE PI-3), il collaudo del Drappo L9 al ta… | i piani | DM |
| **P12 · Immagini da Canva**: gli originali a piena risoluzione dei sette ritratti al posto delle copie da 533 × 800, e Skullcrusher nel cortile col cane di Hella sbagliato | `07_…/Immagini/PROMPT-RITRATTI-E-TAVOLE-ARC07.md` §4 | esportare da Canva con lo stesso nome di file |
| **P13 · La bozza del Caos Ultimo** (TRASVERSALE D13): approvarla o correggerla | `PG/Artefatti/…/04_Anello_S3_Caos_Ultimo_DM.html` | DM |
| **P14 · Le promozioni a stable** (ADR-0099): ruff e uv proponibili dal 2026-11-06, pytest-xdist dopo 14 giorni dal 2026-10-23 | [PIATTAFORMA](plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md) | la card nel thread padre |
| **P29 · Le chat di Claude.ai, la parte che solo il DM può fare**: archiviare a mano le 24 chat del triage (nessuno strumento qui le raggiunge, né i loro allegati) e ripetere la ricerca dentro gli altri progetti di Claud… | triage chat 2026-10-23, «Note oneste» | archiviare; dire se esistono altri progetti RumblingStone |

## ⬜ Da fare, nell'ordine dei piani: 8

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **P19 · Il rilevatore dei box e le battute etichettate** (`> **2 di 3 — …**`): da riverificare se `misura_craft.box_read_aloud` le apre; se no, allargare l'apertura e rimisurare i residui | `scripts/misura_craft.py` | prima la prova su `DEF-4` (Balvar) |
| **P20 · Residui di stampa**: «Naviga i capitoli qui sopra» ancora stampato nel Palio (`PALIO-BOOKLET-INTRO.md`); l'ultima riga dell'indice dell'Abbazia sola a pagina 35; i residui d'apparato del Palio e del Drappo (… | §11.3 · CICLO-SESSIONE 2g | una PR di classe M |
| **P22 · L'ambiente riproducibile dentro la piattaforma**: A1-A3 di AMBIENTE (checksum nel registro, tre piattaforme, lock) vanno rimisurati contro ADR-0099, che ha già portato Python 3.13, i canali e i test una volta so… | [AMBIENTE](plans/PIANO-AMBIENTE-RIPRODUCIBILE.md) · [PIATTAFORMA](plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md) | dire cosa di AMBIENTE è superato, poi A1 |
| **P23 · PRATICHE**: PI-6, PI-2, PI-5, PI-4 (dopo CICLO D6); PI-1 4i-3 aspetta la prima PR che resta indietro rispetto a `main` | [PRATICHE](plans/PIANO-PRATICHE-DI-INGEGNERIA.md) §5 e §8 | una PR ciascuno, in quest'ordine |
| **P24 · CICLO-DI-SESSIONE, la Fase 0** (D1-D6 decise il 2026-09-30) | [CICLO-SESSIONE](plans/PIANO-CICLO-DI-SESSIONE-E-MENU.md) §5 | la Fase 0 |
| **P25 · Il Drappo L9, la lettura a freddo**: lettore e playtester che non vedono il piano sul §2-bis, e un dry-run cronometrato | [DRAPPO](plans/PIANO-DRAPPO-DI-TARSILIA-STANDALONE-PF1E.md) Lotto 9 | due agenti a freddo, poi P11 |
| **P27 · I nomi dell'Elsir Vale rimasti nel testo di gioco**: il triage delle chat dice «sostituiti da Cannath», ma «Elsir» compare ancora in ~30 file di contenuto. Molte righe sono note d'adattamento e vanno tenute (REA… | triage chat 2026-10-23, chat 15 | censire le righe, separare note d'adattamento e finzione, correggere solo la finzione |
| **P30 · Gli altri archi senza testo, e cosa si è perso nell'import**: 06, 07, 10 senza perdite. D7-D12 decise dal DM il 2026-10-23 e la cronaca corretta (P30-b: partenza all'8° livello, appunti d'apertura giocati, chier… | [ARCHI-SENZA-TESTO](plans/RICERCA-ARCHI-SENZA-TESTO-2026-10.md) §5 | P30-a, le schede che mancano nel Bestiario |

## 🟡 Fatto a metà: 0

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

Nessuna.

## Fatto di recente: le ultime 12 righe del CHANGELOG

Fonte: [`plans/CHANGELOG.md`](plans/CHANGELOG.md), una riga per lotto chiuso.

| Data | Piano | Lotto | Esito |
|---|---|---|---|
| 2026-11-25 | PIANO-REVISIONE-ARC08-COERENZA-E-QUALITA | Gli scontri dei pregen sulla griglia, più duri e con schede legali (thread «Ren… | 🟡 in PR, ogni numero alzato è INFERRED con la domanda al DM (5 in DEF-1, 15 in DEF-2). Simulatore, 4.000 duelli per riga, seme 7: Gorthak di oggi con Borin poi… |
| 2026-11-25 | REGOLE-SENZA-OMISSIONI | Lotto «razze coi dadi vita razziali» e caratteristiche (card di Jfs del 20/11).… | ✅ schede bocciate dalla regola 21 → 3, tutte spiegate (l'orog letto come orco, Zin'thara letta come elfa, Tempestas dichiarato); dopo la verifica a due agenti,… |
| 2026-11-25 | PIANO-REVISIONE-ARC09-COERENZA-E-QUALITA | I nomi della Cannath Vale nei file di gioco (scelta di Jfs su card del 25/11, t… | 🟡 `git grep -w` su tutto il repo: Rhest 358 + RHEST 135 in 89/46 file, Blackfens 63 + 8, Brindol 167 in 36 → restano in archivi e storia, log e recap del 05/20… |
| 2026-11-25 | STATO-E-ORDINE | ADR-0142, aggiunta: la voce `**/rendered-*/` in `.claudeignore` (scelta di Jfs… | 🟡 file tracciati coperti 881 → 1.136; `rg -n -M 500 --ignore-file .claudeignore`, `main` → ramo: byte da −0,4% (Skullcrusher) a −2,7% (Belkram), file da −0,9%… |
| 2026-11-25 | STATO-E-ORDINE | ADR-0146, correzione: la configurazione Claude arriva anche a livello utente. D… | 🟡 sessione headless nuova in `/home/user` nello stesso container: con la configurazione utente scattano UserPromptSubmit e PreToolUse su Bash,… |
| 2026-11-25 | PIATTAFORMA-DI-SVILUPPO | P4 e P7, promozioni da testing a stable (D8, card del DM del 2026-11-25: «Tutti… | ✅ P4, P7. Su `main` 168 run su 168 con le stesse prove nei due job; mediana del passo pytest negli ultimi 10 run 1.127 s, sul run della #516 761 s (−32%; la st… |
| 2026-11-21 | P16 · REGOLE | Skullcrusher Vecchio come al duello del 20/11 (scelte di Jfs del 21/11 su card)… | ✅ tre conosciuti mancanti (7/5/3/2 dell'SRD), oggetti dal tesoro (CA 43, contatto 13, TS +24/+21/+23), *immagine speculare* al corno, passate lunghe, gittate;… |
| 2026-11-21 | PIANO-REVISIONE-ARC08-COERENZA-E-QUALIT… | Corredo dei draghi, scelte del DM sulle card del 21/11. **Fauci di Palude** «A… | In PR. Quota del tesoro triplo addosso: Fauci 0% → 47%, Tyrgarun 0% → 24%, Ozyrrandion 27% → 88%, Regiarix 0% → 36%, drago di Vaereth 0% → 19%. CA: Fauci 29 →… |
| 2026-11-21 | P16 · REGOLE | Due incoerenze trovate dal thread dei draghi (richiesta del coordinatore del 21… | ✅ due file, nessun numero di scheda cambiato |
| 2026-11-20 | STANDARD-STAMPA | ADR-0122, S4: l'appendice della regione nel booklet della serata di ARC-07 (ric… | S4 pagine di regione/PNG 0/3 → 9/3; pagine 132 → 141; note di lavoro in stampa nella serata 0 (prima di togliere l'apparato dal conto ne contava 6); parole del… |
| 2026-11-20 | PIATTAFORMA-DI-SVILUPPO | ADR-0148 (proposta), i fatti si verificano con script e gli agenti con prove fi… | 🟡 `verifica_px`: 16 test, 366 mutanti su 366, 0 falsi allarmi su 3 versioni storiche del registro; `verifica_rimandi`: 1.744 rimandi, 1.026 tornano, 1 rotto (… |
| 2026-11-20 | STATO-E-ORDINE | ADR-0146 (proposta), le skill di prosa si caricano per vincolo (richiesta di Jf… | ✅ baseline su un campione di cinque thread: zero invocazioni di skill su 188 chiamate; l'hook si attiva su circa 200 modifiche su 2.944 ai file di gioco degli… |

## Le misure che si portano dietro

- **Decisioni**: 1 aperte, 324 chiuse (`decisioni_dm.py`).
- **Memoria storica**: 229 voci, l'ultima MS-0229 del 2026-11-20 (`memoria_storica.py`, ADR-0127).
- **Prosa**: 11 revisioni applicate, segnalazioni -28, MQM +2.52 punti (`ciclo_prosa.py registro`).

## Dove vive ogni cosa

| Cosa | Casa unica |
|---|---|
| Lo stato del mondo di gioco | [`campaign/state.md`](campaign/state.md), e il canone si scrive sul ramo del gruppo (ADR-0007) |
| Cosa si fa e in che ordine | [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md) |
| Le decisioni del DM | le tabelle `decisioni-dm` dentro ogni piano (ADR-0047) |
| Cosa è successo | [`plans/CHANGELOG.md`](plans/CHANGELOG.md) |
| Che piani esistono | [`plans/INDEX.md`](plans/INDEX.md) |
| Perché si è deciso così | [`plans/adr/`](plans/adr/) |
| Cosa sapevano le sessioni prima, la storia dietro una scelta | [`plans/MEMORIA-STORICA.md`](plans/MEMORIA-STORICA.md), si cerca con `scripts/memoria_storica.py` (ADR-0127) |
| Le norme e chi le misura | [`skills/REGISTRO-NORME-EDITORIALI.md`](skills/REGISTRO-NORME-EDITORIALI.md) |
| Le regole per gli agenti | [`AGENTS.md`](AGENTS.md) |
| Questa pagina | `scripts/memoria.py`, mai a mano |
