# 🧠 MEMORIA — il lavoro su RumblingStone in un posto solo

> **Generata da `scripts/memoria.py`: non si scrive a mano** ([ADR-0087](plans/adr/ADR-0087-la-memoria-del-lavoro-e-generata.md)). Ogni riga viene da una fonte che ha la sua casa, e il link porta lì: si corregge la fonte, poi `python3 scripts/memoria.py`. La CI boccia questo file se resta indietro.

## Come si riparte, in una sessione nuova

```bash
git fetch --prune origin
python3 scripts/memoria.py --check      # questa pagina è allineata?
python3 scripts/decisioni_dm.py --check # le decisioni aperte
python3 scripts/fase1.py <file>         # sempre, prima di toccare
```

Poi si legge questa pagina dall'alto: prima cosa aspetta il DM, poi da dove riparte l'agente. Le regole di lavoro stanno in [`AGENTS.md`](AGENTS.md).

## Aspetta il DM: 18 decisioni aperte

Fonte: le tabelle `decisioni-dm` dei piani, aggregate in [STATO-E-ORDINE §4](plans/STATO-E-ORDINE-DEI-PIANI.md). Si risponde col numero e il piano: *«CODA-SECONDO-LETTORE D2 sì»*.

| Piano | # | Ambito | Domanda |
|---|---|---|---|
| `INVENTARIO-GEMINI-AISTUDIO` | D1 | `battle_stats_maps.md`: Spaventadraghi,… | Si riprende come proposta in ARC-08 (MASTER-DEF), con le regole confrontate con l'SRD; quello che diverge da ADR-0091 resta fuori. |
| `INVENTARIO-GEMINI-AISTUDIO` | D2 | I tre mini-boss di «Branch of Sistema C… | Restano fuori finché il DM non dice se Tiamat è mai stato canone; i mini-boss possono entrare nel Bestiario come proposta. |
| `INVENTARIO-GEMINI-AISTUDIO` | D3 | Il «Manuale da campo del DM» e il «Gior… | Si confrontano con `ARC08-01` quando si scrive il master definitivo di ARC-08. |
| `INVENTARIO-GEMINI-AISTUDIO` | D4 | Statblocchi alternativi di «Organizing… | Restano fuori: le schede canone sono quelle di ADR-0091. |
| `INVENTARIO-GEMINI-AISTUDIO` | D5 | «Red Hand of Doom 3.5 Conversion» | Si legge come fonte di idee per ARC-09, senza importare nulla. |
| `INVENTARIO-GEMINI-AISTUDIO` | D6 | Le chat non scaricate (§5), le sette no… | Secondo giro solo se il DM esporta le chat dell'app Gemini o mette i file grandi in `/mnt/project-files/`. |
| `BOX-LUOGO` | D2 | B0 | **Le dimensioni nella prima frase del box** («camera quadrata di quaranta piedi»), come nel modello del 2026-10-01, o il paragone di ADR-0014 con le misure nei Dati per il DM? Proposta: resta ADR-0014. Dal modello ester… |
| `BOX-LUOGO` | D3 | B2 | **Ogni box dichiara il suo tipo?** Per esempio `**Read-aloud (luogo · Salvatore lead).**`, con i tipi luogo, ingresso, round, rivelazione, chiusura. Sblocca la norma «niente creature nel box di luogo» e le soglie per ti… |
| `BOX-LUOGO` | D4 | — | **I box già giocati fuori dalle nuove misure**: nei DEF di ARC-07, 27 box oltre i 500 caratteri e 61 oltre le quattro frasi. Proposta: non si toccano, come per D9 di PIANO-LETTORE: si spezzano solo se lo chiedi, e senza… |
| `BOX-LUOGO` | D5 | B5 | **L'Abbazia con le stanze *keyed*** (è la F5 di PIANO-LETTORE, «decidere col DM se ogni stanza vuole un box»). Proposta: sì, un box di luogo breve per stanza nell'ordine di *Dungeon*, quando F5 tocca l'Abbazia; è il ban… |
| `BOX-LUOGO` | D6 | B1 | **Il template d'area va in `campaign/templates/`**, accanto a quelli di sessione e di mappa, in due versioni (3.5 e PF1e)? Proposta: sì, tutte e due, con la creatura sempre come rimando al Bestiario e mai trascritta |
| `CODA-SECONDO-LETTORE` | D2 | 3 | **Il campo *Etichetta regia* troncato in `PROMPT-IMMAGINI-07ILP.md`**: si cerca chi compila il file e si corregge lì, o si correggono a mano le 32 righe? *Proposta*: prima si cerca il generatore (`extract_scene_prompts`… |
| `CODA-SECONDO-LETTORE` | D3 | 4 | **La *d* eufonica** (*legato a Aegis Fang*, *a area*): la vuoi come norma? *Proposta*: sì, *ad* solo davanti alla stessa vocale, scritta in `editorial-standards.md` e misurata; se no, resta com'è |
| `MASTER-DEF` | D6 | A3 | Le domande del censimento delle versioni (D1-D4, D6-D15 nel file, le consigliate fra parentesi): soffio di 2B su Riflessi; PF di Fauci dal massimo della sua scheda meno il carry-over; bonus della carica ricalcolato; can… |
| `RECUPERO` | D5 | L4 | **I ⬜ opzionali dei piani chiusi o fermi**, per gruppo. *Proposta*: (a) chiusi come «non si fa»: AUDIT-SCRIPTS (shellcheck lo fa AMBIENTE A6), IMPORT-ULTRACLEAR (migrazione delle ~30 mappe, ora COLLAUDO-MAPPE), RENDER-F… |
| `RECUPERO` | D6 | L3 | **RICONCILIAZIONE-PR-APERTE si chiude come superato?** R3, R6, R7, R8 sono decisi o fatti altrove (§2.3). *Proposta*: sì, ✅ con il rimando a dove sta ognuno |
| `RIPRESA-PR` | D2 | F3 · 3d | **Riformulata il 2026-09-11: la domanda di prima partiva da un fatto falso.** Diceva *«i diciotto raster si generano sulla tua macchina — quando?»*, ma **esistono tutti e diciotto** (più le due extra), generati dal DM *… |
| `RIPRESA-PR` | D11 | F4 · 4b | **L'ADR ex-0018 della #72: recuperato il 2026-09-11 come [ADR-0049](plans/adr/ADR-0049-edizione-commerciale-ap-originale.md), e resta 🔵 *proposta* — non accettata.** Dice che, *se e quando* si pubblica, si pubblica un *… |

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
| **P05 · La #99 e lo schedario dei PG**: #99 chiusa il 2026-10-24 (ADR-0088 accettata, scelta A); 4g-1 su `main` con la #278; i tre pezzi rimasti ripresi (§4.14); 4h scartato | [RIPRESA-PR](plans/PIANO-RIPRESA-PR-ABBANDONATE.md) F4 §4.13-§4.14 | 4g-2: i valori delle caratteristiche dalle schede del DM, con un modulo |

## 🙋 Aspetta il DM: 10

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **P06 · Accettare le ADR ancora «proposta»**: ADR-0090 (la partita sul ramo di gruppo nuovo, dal 2026-10-11), ADR-0094 (il giro si misura contro la versione di prima), ADR-0095 (correzione, verifica e seconda passata).… | `plans/adr/` | un sì o un no per ADR; l'agente cambia lo stato e la riga di CHANGELOG |
| **P07 · Le decisioni numerate dei piani**: BOX-DI-LUOGO D2-D6, CODA-SECONDO-LETTORE D2 e D3, MASTER-DEF D6 (il censimento delle versioni), RECUPERO D5 e D6, RIPRESA-PR D2 (Gemini o SDXL per il Drappo, con la #106) e D11… | §4, generata da `decisioni_dm.py` | rispondere col piano e il numero: *«BOX D2 sì»* |
| **P08 · Le patch di `state.md` sul ramo di gruppo**, scritte e mai applicate (verificato su `ce34599`): il Bane di Aegis Fang contro Fauci (affresco A7); la Cintura della Devastazione a 4 cariche al giorno (lo stato dic… | `/mnt/project-files/sessione-2026-10-15/` · `/mnt/project-files/giro-arc07-2026-10-18/PATCH-STATE-MD.md` | `git am` o a mano sul ramo `campaign-group-rumblingstone` |
| **P09 · Le domande di canone lasciate aperte dai thread di ARC-07 e ARC-08**: i pf di Terros (345 o 348 con Robustezza); *Virata* da riscontrare su d20srd; la portata del sussurro della Catena… | `plans/esperimenti/giro4-arc07-2026-10-19/DECISIONI-DM.md` · `DEF-4` · `ARC08` | una risposta per domanda; l'agente le porta nei master in una PR |
| **P10 · Mappe, le scelte del DM**: texture e tessere nella pagina di scelta (R8, livello B), la prima immagine di ComfyUI (R4-quinquies), il giro di prova sui modelli 3D CC0 e lo zip Standard di Quaternius (R4-ter), il… | [RESA-ASSET](plans/PIANO-RESA-E-ASSET-DELLE-MAPPE.md) §8 · [COLLAUDO-MAPPE](plans/PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md) | DM; poi l'agente mette le tessere nel tema e rimisura |
| **P11 · I collaudi che solo il DM può fare**: l'import `.uvtt` in Foundry (INTEGRAZIONE, ~92%), il gate κ ≥ 0,6 (MISURA-EDITORIALE, ~90%), la prova del blocco dei segreti (PRATICHE PI-3), il collaudo del Drappo L9 al ta… | i piani | DM |
| **P12 · Immagini da Canva**: gli originali a piena risoluzione dei sette ritratti al posto delle copie da 533 × 800, e Skullcrusher nel cortile col cane di Hella sbagliato | `07_…/Immagini/PROMPT-RITRATTI-E-TAVOLE-ARC07.md` §4 | esportare da Canva con lo stesso nome di file |
| **P13 · La bozza del Caos Ultimo** (TRASVERSALE D13): approvarla o correggerla | `PG/Artefatti/…/04_Anello_S3_Caos_Ultimo_DM.html` | DM |
| **P14 · Le promozioni a stable** (ADR-0099): ruff e uv proponibili dal 2026-11-06, pytest-xdist dopo 14 giorni dal 2026-10-23 | [PIATTAFORMA](plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md) | la card nel thread padre |
| **P29 · Le chat di Claude.ai, la parte che solo il DM può fare**: archiviare a mano le 24 chat del triage (nessuno strumento qui le raggiunge, né i loro allegati) e ripetere la ricerca dentro gli altri progetti di Claud… | triage chat 2026-10-23, «Note oneste» | archiviare; dire se esistono altri progetti RumblingStone |

## ⬜ Da fare, nell'ordine dei piani: 13

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **P16 · Le marcature rimaste nel contenuto**: 44 `[INFERRED]` e `[PROPOSTA]` (erano 568 il 2026-09-25; il Bestiario è a 0): ARC-08 3, ARC-09 9, `campaign/` 26 (20 nel `state-changelog`), PG 2, ARC-07 1 fuori archivio | `grep -rc "\[INFERRED\]\\|\[PROPOSTA\]"` | un lotto per arco: prima ARC-08, poi ARC-09 |
| **P17 · Skullcrusher Vecchio nei file di ARC-08**: l'ERRATA §2.3 e `ARC08-11-PONTE-ARRIVO` vanno allineati al duello deciso (il Vecchio con 2 wyvern, EL 17) | memoria del 2026-10-19 · `08_…/ERRATA-*.md` | da riverificare prima di toccare |
| **P18 · Le regole di 3.5 fuori rete**: gli incantesimi nelle esportazioni PCGen di `Bestiario/pregen-pcgen/` non hanno ancora la loro riga in `dnd-35-srd/references/resources.md` | §8.3 | una riga e la voce nel registro delle norme |
| **P19 · Il rilevatore dei box e le battute etichettate** (`> **2 di 3 — …**`): da riverificare se `misura_craft.box_read_aloud` le apre; se no, allargare l'apertura e rimisurare i residui | `scripts/misura_craft.py` | prima la prova su `DEF-4` (Balvar) |
| **P20 · Residui di stampa**: «Naviga i capitoli qui sopra» ancora stampato nel Palio (`PALIO-BOOKLET-INTRO.md`); l'ultima riga dell'indice dell'Abbazia sola a pagina 35; i residui d'apparato del Palio e del Drappo (… | §11.3 · CICLO-SESSIONE 2g | una PR di classe M |
| **P21 · RECUPERO L2 e L4**: R-3 e il suo test; i piani fermi, quando il DM risponde a D5 | [RECUPERO](plans/PIANO-RECUPERO-DECISIONI-E-REVISIONI-INCOMPIUTE-2026-10.md) | L2 subito, L4 dopo D5 |
| **P22 · L'ambiente riproducibile dentro la piattaforma**: A1-A3 di AMBIENTE (checksum nel registro, tre piattaforme, lock) vanno rimisurati contro ADR-0099, che ha già portato Python 3.13, i canali e i test una volta so… | [AMBIENTE](plans/PIANO-AMBIENTE-RIPRODUCIBILE.md) · [PIATTAFORMA](plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md) | dire cosa di AMBIENTE è superato, poi A1 |
| **P23 · PRATICHE**: PI-6, PI-2, PI-5, PI-4 (dopo CICLO D6); PI-1 4i-3 aspetta la prima PR che resta indietro rispetto a `main` | [PRATICHE](plans/PIANO-PRATICHE-DI-INGEGNERIA.md) §5 e §8 | una PR ciascuno, in quest'ordine |
| **P24 · CICLO-DI-SESSIONE, la Fase 0** (D1-D6 decise il 2026-09-30) | [CICLO-SESSIONE](plans/PIANO-CICLO-DI-SESSIONE-E-MENU.md) §5 | la Fase 0 |
| **P25 · Il Drappo L9, la lettura a freddo**: lettore e playtester che non vedono il piano sul §2-bis, e un dry-run cronometrato | [DRAPPO](plans/PIANO-DRAPPO-DI-TARSILIA-STANDALONE-PF1E.md) Lotto 9 | due agenti a freddo, poi P11 |
| **P26 · L'eccezione di ruff per `misura_craft.py`**, da togliere dopo la #264 | `ruff.toml` | dopo il merge della #264 |
| **P27 · I nomi dell'Elsir Vale rimasti nel testo di gioco**: il triage delle chat dice «sostituiti da Cannath», ma «Elsir» compare ancora in ~30 file di contenuto. Molte righe sono note d'adattamento e vanno tenute (REA… | triage chat 2026-10-23, chat 15 | censire le righe, separare note d'adattamento e finzione, correggere solo la finzione |
| **P30 · Gli altri archi senza testo, e cosa si è perso nell'import**: 06, 07, 10 senza perdite. D7-D12 decise dal DM il 2026-10-23 e la cronaca corretta (P30-b: partenza all'8° livello, appunti d'apertura giocati, chier… | [ARCHI-SENZA-TESTO](plans/RICERCA-ARCHI-SENZA-TESTO-2026-10.md) §5 | P30-a, le schede che mancano nel Bestiario |

## 🟡 Fatto a metà: 0

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

Nessuna.

## Fatto di recente: le ultime 12 righe del CHANGELOG

Fonte: [`plans/CHANGELOG.md`](plans/CHANGELOG.md), una riga per lotto chiuso.

| Data | Piano | Lotto | Esito |
|---|---|---|---|
| 2026-11-01 | STANDALONE-GIARDINO-SALE-CALCE | B6 prima parte: otto mappe tattiche | 🟡 contratti JSON e master in 10-stand-alone/Il Giardino di Sale e Calce/mappe/, quattro temi di render, collaudo_mappe e qualita_mappe a 0 errori; D7 decisa (q… |
| 2026-11-01 | STANDALONE-GIARDINO-SALE-CALCE | B8 progetto: Rethmar e l'assedio | 🟡 15 scelte agganciate a Fronte, Morale Cittadino, contingenti e clock esistenti; tre ingressi (cripta della Cattedrale di Lathander, sfioratore nascosto, pozz… |
| 2026-11-01 | STANDALONE-GIARDINO-SALE-CALCE | B4 seconda parte: Tariq e skum; lotto B8 aperto | 🟡 Tariq chierico 13 di Umberlee GS 13 con nube acida al posto della nebbia di calce; skum guerriero 8 GS 10 (63 pf, non 115); B8 conseguenze sull'assedio di Re… |
| 2026-11-01 | STANDALONE-GIARDINO-SALE-CALCE | B4 prima parte: conti di Karkator e del Ragno delle Catene (3.5) | 🟡 Karkator aboleth mezzo-immondo a 24 DV, GS 15 (16 col Cuore); Ragno delle Catene ragno fase Enorme a 14 DV, GS 10; Tariq, skum e chuul da fare |
| 2026-11-01 | STANDALONE-GIARDINO-SALE-CALCE | A3: budget di EL e di tesoro; D6 decisa | ✅ due moduli separati; tesoro della chat circa 161.000 mo contro 63.000-97.000 del budget SRD; aboleth a 24 DV GS 12 prima del Cuore; fase A chiusa |
| 2026-11-01 | STANDALONE-GIARDINO-SALE-CALCE | A2: le capacità dei quattro PG nella cisterna; D2-D4 decise | ✅ 3.5 sotto Rethmar (Sonjak, Sal), PF1e in una città del deserto inventata; il monaco 3.5 non corre sui muri; equipaggiamento di tre PG assente dal repo; D6 (c… |
| 2026-11-01 | STANDALONE-GIARDINO-SALE-CALCE | A1: riscontro sull'SRD in cache delle creature, di Tariq e delle regole d'ambie… | ✅ D1 (doppio 3.5/PF1e) e D5 (aboleth a conti) decise; nessun numero della chat coincide con un'avanzata; due creature con taglia sbagliata per i DV; 5 incantes… |
| 2026-11-01 | STANDALONE-GIARDINO-SALE-CALCE | A0: inventario della chat Gemini e piano aperto | ✅ chat letta per intero, copia e inventario in project-files; cinque decisioni al DM (sistema, collocazione, ampiezza, titolo, boss) |
| 2026-10-31 | STANDARD-STAMPA | I2 seguito: nessun disegno a caratteri stampato in tutto il repo | ✅ linee del tempo di Palio e Drappo in tabella; `validate_booklets` ferma i recinti con ≥ 20 caratteri di riquadro fuori dall'apparato |
| 2026-10-30 | STANDARD-STAMPA | I2 seguito: le sei mappe schematiche di ARC-07 in pianta o in schema (ADR-0106… | ✅ nessuna griglia ASCII stampata nei booklet di ARC-07; T-5, R-1, S-1 in scala, T-1, T-4, M7-A schemi a 7,4 pt senza filtri, `render_schemi.py --check` in CI |
| 2026-10-30 | STANDARD-STAMPA | I2 chiuso: pianta in stampa per tutte le 56 mappe del repo (ADR-0106), controll… | ✅ scritte sotto 7 pt 5.820→0 e filtri rasterizzati 418→0 sulle 56 mappe, nessun testo perso; ARC-07 righe sotto 7 pt a 0 in tutti e tre i volumi (Notte e Alba… |
| 2026-10-30 | STANDARD-STAMPA | I2 prime mappe: modo stampa per M7-H e M7-C, stile pianta scelto al cieco | 🟡 scritte ≥ 7,4 pt, niente filtri rasterizzati; tetti ARC-07 giù: Notte e Alba 291→217 righe e 58→52 immagini, Resurrezione 330→256 e 68→62, Mille anni 291→217… |

## Le misure che si portano dietro

- **Decisioni**: 18 aperte, 305 chiuse (`decisioni_dm.py`).
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
| Le norme e chi le misura | [`skills/REGISTRO-NORME-EDITORIALI.md`](skills/REGISTRO-NORME-EDITORIALI.md) |
| Le regole per gli agenti | [`AGENTS.md`](AGENTS.md) |
| Questa pagina | `scripts/memoria.py`, mai a mano |
