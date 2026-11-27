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
| 2026-11-27 | P16 · REGOLE | DEF-4 di ARC-07 allineato alla scheda A.1-bis di Skullcrusher il Vecchio (canon… | 🟡 numeri allineati alla scheda; aperti al DM: C.3 contro CA 43 dà «fuggito» nel 99,9% dei casi (misura del regolista, problema dichiarato e non risolto), quand… |
| 2026-11-27 | PIATTAFORMA-DI-SVILUPPO | Il lavoro fuori da main ha una pagina dal vivo (ADR-0157, domande di Jfs del 27… | 🟡 25 test; pagina del 27/11: 8 filoni, canali 36 stable · 19 testing · 11 unstable, 4 PR senza filone (#543 #537 #519 #459), 3 rami `claude/*` senza posto, 28… |
| 2026-11-27 | LEVEL-DESIGN-E-INQUADRATURA | D4, igiene IP dei prompt versionati (scelta di Jfs sulla card dell'audit settim… | 🟡 57 righe con opere protette in 12 file → 0 (l'audit ne contava 31, il piano 10 in 7: artisti e compositori non contati); 128 righe aggiunte e 91 tolte; resta… |
| 2026-11-27 | PIANO-REVISIONE-ARC08-COERENZA-E-QUALITA | Le due frasi oscure che il DM aveva segnalato nel cieco A sul ritmo (MS-0231),… | ✅ `cricchetto_prosa --rispetto-a origin/main` 0 peggiorati; `ciclo_prosa misura` 1 → 1 (DEF-1) e 0 → 0 (DEF-2). Non controllate fedeltà NLI e ripetizioni con e… |
| 2026-11-27 | REGOLE-SENZA-OMISSIONI | Palio: un solo rapimento del fantino a notte (card di Jfs del 27/11 «Si escludo… | ✅ misura_stampa del Palio entro i tetti |
| 2026-11-27 | MISURA-AGENTI-E-AUTOMATISMI | M2-bis, emendamento «raccolta settimanale e annotatore cieco» di ADR-0154 (scel… | 🟡 script fatto; la routine del lunedì non lo chiama ancora; il tetto di dieci a settimana non è nel codice; 24/27 sopravvaluta l'accordo; la cecità dell'annota… |
| 2026-11-27 | STATO-E-ORDINE | ADR-0151, correzioni dopo la #529 (richiesta di Jfs del 27/11, 08:29 UTC: «fai… | ✅ suite 3.639 passati e 19 saltati, `gate_locale --pre-push` 56 verdi, `tools_manifest --check` 156 conformi; hook su Bash mediana 46-54 ms (prima 42-47), merg… |
| 2026-11-27 | MISURA-AGENTI-E-AUTOMATISMI | M2, emendamento «M2» di ADR-0154: gli omonimi dei trigger e i messaggi che non… | 🟡 M2 fatto; la tecnica 1 senza cricchetto finché manca un set di prompt grezzi; ogni `<relay>` tace anche quando apre lavoro; regex euristiche, «avventura» non… |
| 2026-11-27 | REGOLE-SENZA-OMISSIONI | Il fantino nella stalla del Palio solo se è un PNG ancora lì (card di Jfs del 2… | ✅ misura_stampa del Palio entro i tetti |
| 2026-11-27 | MISURA-AGENTI-E-AUTOMATISMI | M1, emendamento di ADR-0154: le metriche passano a scikit-learn e scipy (Jfs, 2… | 🟡 M1 riscritto, cancello ancora in testing; D1 aperta; M2, M3 e M3-bis da fare |
| 2026-11-27 | MISURA-AGENTI-E-AUTOMATISMI | M1, ADR-0154 (proposta), l'instradamento degli agenti si misura su messaggi ver… | 🟡 M1 fatto, cancello in testing; D1 aperta (etichette del test da confermare dal DM); M2 e M3 da fare |
| 2026-11-27 | PIATTAFORMA-DI-SVILUPPO | P12, ADR-0152 (accettata), la milestone pronta si misura su main (domanda di Jf… | 🟡 in testing: nessuna milestone pronta, v1.1.0 ferma su `readme-adr`, `fatto-guide`, `fatto-adr-stato`; 2,6 s (`--check --solo-integrita` 0,06 s); test raccolt… |

## Le misure che si portano dietro

- **Decisioni**: 1 aperte, 325 chiuse (`decisioni_dm.py`).
- **Memoria storica**: 249 voci, l'ultima MS-0249 del 2026-11-27 (`memoria_storica.py`, ADR-0127).
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
| Il lavoro che non è ancora su `main` (PR, rami, cartelle dei thread) | [`plans/LAVORO-IN-CORSO.md`](plans/LAVORO-IN-CORSO.md), istantanea dal registro `plans/lavoro-in-corso.json`: `python3 scripts/lavoro_in_corso.py --fetch` (ADR-0157) |
| Le norme e chi le misura | [`skills/REGISTRO-NORME-EDITORIALI.md`](skills/REGISTRO-NORME-EDITORIALI.md) |
| Le regole per gli agenti | [`AGENTS.md`](AGENTS.md) |
| Questa pagina | `scripts/memoria.py`, mai a mano |
