<!-- generata da scripts/lavoro_in_corso.py: non si scrive a mano.
     Fonte curata: plans/lavoro-in-corso.json. Rigenera: python3 scripts/lavoro_in_corso.py -->

# Lavoro in corso

Istantanea del 2026-11-27 16:39 UTC, generata da `scripts/lavoro_in_corso.py`: non si
scrive a mano. Si corregge il registro `plans/lavoro-in-corso.json`, poi si
rigenera con `python3 scripts/lavoro_in_corso.py` (`--fetch` per aggiornare
prima i rami, `--offline` senza rete). Dipende da rete, clone e macchina: è
una fotografia, non un cancello. Ciò che è già su `main` sta in `MEMORIA.md`.

## Filoni

| Filone | Stato | Canale | PR | Rami | Cartelle condivise | Thread | Aspetta | Prossimo |
|---|---|---|---|---|---|---|---|---|
| **Registro e runner unico delle misure dei componenti**<br>`misure-agenti` | `in-corso` | — | [#544](https://github.com/gsamuele78/RumblingStone/pull/544) bozza, oggi | `claude/project-thread-2yp4ga` | `agenti-eval-2026-11-27`<br>`instradamento-coda` | Misurare e migliorare agenti, skill e automatismi | — | finire la bozza della PR #544 (ADR-0155) e portarla a pronta |
| **Allineare i sette piani fermi**<br>`piani-fermi` | `in-corso` | — | [#542](https://github.com/gsamuele78/RumblingStone/pull/542) bozza, oggi | `claude/project-thread-198cay` | `audit-settimanale/piani-fermi-2026-11-27` | Allineare i sette piani fermi | — | chiusure con prova e numeri aggiornati nella PR #542, poi da bozza a pronta |
| **Preparare la sessione del 30 novembre (ARC-07 DEF-4 e DEF-5)**<br>`serata-30-novembre` | `aspetta-jfs` | — | [#541](https://github.com/gsamuele78/RumblingStone/pull/541) pronta, oggi | `claude/project-thread-3o4an2` | `serata-2026-11-30`<br>`tavole-serata-2026-11-30` | Preparare la sessione del 30 novembre | la revisione e il merge della PR #541 (pronta, ADR-0156) prima della serata | dopo il merge, il corredo della serata con dm.py corredo --stampa |
| **Allineare i Doni di Hella nei rimandi**<br>`doni-di-hella` | `in-corso` | — | [#539](https://github.com/gsamuele78/RumblingStone/pull/539) bozza, oggi | `claude/project-thread-fm157b` | — | Allineare i Doni di Hella nei rimandi | — | TRASVERSALE T9-bis nella bozza #539, poi pronta per la revisione |
| **Provare la trascrizione locale della serata**<br>`trascrizione-locale` | `fermo` | — | [#424](https://github.com/gsamuele78/RumblingStone/pull/424) bozza, 9 g fa | `claude/project-thread-kcq3f8` | — | Provare la trascrizione locale della serata | una decisione: il thread è risolto ma la bozza #424 è ancora aperta (ADR-0135 prenotato) | riprendere la prova su GPU locale o chiudere la PR e liberare ADR-0135 |
| **Immagini FLUX del Drappo (D2) sul portatile 4050**<br>`drappo-flux` | `aspetta-jfs` | — | — | — | `drappo-flux-2026-11-16`<br>`drappo-flux-kaggle-2026-11-21`<br>`drappo-flux-kaggle-2026-11-25`<br>`drappo-flux-kaggle-2026-11-27`<br>`prove-4050-risultati`<br>`kaggle-2026-11-18` | Scrivere lo script FLUX per il 4050 | guardare i confronti, o lanciare scripts/prove-4050/drappo-flux.sh sull'ASUS, e scegliere A o B; niente è mai girato su GPU locale | con la scelta, il lotto D2 delle immagini del Drappo |
| **Agenti e cascate: vincolo delle skill, custode della memoria, documentazione automatica**<br>`agenti-e-cascate` | `in-prova` | `testing` | — | — | `agenti-2026-11-20`<br>`custode-memoria-2026-11-27`<br>`documentazione-automatica-2026-11-27` | Vincolare gli agenti all'uso delle skill (con Creare l'agente custode della memoria e Garantire che la documentazione si aggiorni da sola) | — | le regole sono su main; si misura nel canale testing (ADR-0099) prima di dirle stabili |
| **Rendere visibile il lavoro in corso (questa pagina)**<br>`lavoro-in-corso` | `in-corso` | `testing` | [#545](https://github.com/gsamuele78/RumblingStone/pull/545) bozza, oggi | `claude/project-thread-65g5a1` | — | Rendere visibile il lavoro in corso | — | PR del registro e dello script, poi la documentazione |

Stati: `in-corso` qualcuno ci lavora: thread aperto o PR che si muove · `aspetta-jfs` fermo su una decisione, una prova o una revisione del DM · `in-prova` su main o quasi, in canale testing: si misura prima di dirlo finito · `fermo` nessuno ci lavora: da riprendere, chiudere o portare.

## Senza filone

Ciò che si muove e il registro non nomina: o entra in un filone, o si chiude.

### PR aperte

| PR | Titolo | Ramo |
|---|---|---|
| [#543](https://github.com/gsamuele78/RumblingStone/pull/543) bozza, oggi | verifica_scheda: i nomi degli incantesimi si leggono con le varianti del lessico, la forma Greater e le note fra parentesi | `claude/project-thread-fv2zai` |
| [#537](https://github.com/gsamuele78/RumblingStone/pull/537) pronta, oggi | ARC-08: il libretto dice che un comandante può morire, Gorthak lo portano via i troll, l'alba è d'estate | `claude/project-thread-39qgl6` |
| [#519](https://github.com/gsamuele78/RumblingStone/pull/519) bozza, oggi | Il prompt d'immagine si scrive per il modello che lo esegue (ADR-0150) | `claude/project-thread-4eo6nn` |
| [#459](https://github.com/gsamuele78/RumblingStone/pull/459) pronta, 4 g fa | Update transformers requirement from >=5.22.1 to >=5.23.0 in /converters/pdf-to-md-engine in the convertitori-settimanale group across 1 directory | `dependabot/pip/converters/pdf-to-md-engine/convertitori-settimanale-239750c618` |

### Rami `claude/*` con commit negli ultimi 14 giorni, senza PR aperta né posto

- `claude/project-thread-84sweg`: ultimo commit 8 giorni fa
- `claude/project-thread-u8xojz-s1`: ultimo commit 7 giorni fa
- `claude/project-thread-wh9wu1`: ultimo commit 6 giorni fa

### Cartelle condivise toccate negli ultimi 14 giorni

| Cartella | Toccata | Titolo del LEGGIMI |
|---|---|---|
| `anteprima-volume-2026-11-19` | 2026-11-25 | — |
| `assalto-barile-zogtar` | 2026-11-21 | — |
| `best-practice-claude-code-2026-11-19` | 2026-11-19 | — |
| `booklet-arc07-2026-11-19` | 2026-11-19 | — |
| `carta-cielo-arc09` | 2026-11-18 | Banco della carta del cielo (ARC-09) — 13/11/2026 |
| `carte-drappo-2026-11-13` | 2026-11-14 | — |
| `cieco-a-ritmo-2026-11-19` | 2026-11-26 | Cieco A · il ritmo della frase (2026-11-19) |
| `confronto-prompt-arc08-2026-11-27` | 2026-11-27 | — |
| `correzioni-tordek-dominare-2026-11-21` | 2026-11-21 | — |
| `debito-thorik-2026-11-26` | 2026-11-26 | — |
| `draghi-corredo-2026-11-21` | 2026-11-21 | — |
| `duello-skullcrusher-2026-11-15` | 2026-11-15 | Il duello con Skullcrusher: simulazione Monte Carlo (15/11/2026) |
| `immagini-personaggi` | 2026-11-27 | — |
| `memoria-storica-2026-11-18` | 2026-11-18 | — |
| `nomi-incantesimi-2026-11-27` | 2026-11-27 | — |
| `ponte-arc07-arc08-2026-11-25` | 2026-11-27 | — |
| `pr-aperte` | 2026-11-25 | — |
| `prosa-peculiare-2026-11-19` | 2026-11-19 | — |
| `regole-lotto-j` | 2026-11-14 | — |
| `regole-lotto8` | 2026-11-13 | — |
| `regole-razze-dv-2026-11-20` | 2026-11-27 | — |
| `revisione-arkalseif-2026-11-19` | 2026-11-19 | — |
| `roadmap-motore-2026-11-08` | 2026-11-27 | — |
| `schede-schema-2026-11-13` | 2026-11-15 | — |
| `serata-2026-11-20` | 2026-11-21 | — |
| `serata-corta-2026-11-13` | 2026-11-13 | — |
| `tattiche-draghi-2026-11-15` | 2026-11-15 | Tattiche dei draghi: simulazione (15/11/2026) |
| `tattiche-villain-2026-11-15` | 2026-11-15 | — |

## Da aggiornare o ferme

Niente.

## Canali della piattaforma (ADR-0099)

Il canale di ogni componente viene da `plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md` §2: per ora la fonte è
scritta a mano, finché il lotto P1 del piano non porta il canale in
`binari.py`. unstable, poi testing (versione fissata, CI non bloccante,
misura prima e dopo), poi stable dopo 14 giorni e 10 run su `main` con
l'ok del DM.

stable **36** · testing **19** · unstable **11** · uscito **1** · non-si-adotta **1** · altro **1**

| Componente | Canale | Dal | Che cosa dice il piano | Riga |
|---|---|---|---|---|
| pip-audit | `testing` | 2026-09-24 | testing (non bloccante dal 2026-09-24, non è mai salito) | [55](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L55) |
| shellcheck | `testing` | — | testing (`\|\| true`); stable con A6 di AMBIENTE | [56](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L56) |
| riscontro SRD (`riscontro_srd.py` con l'SRD 3.5 e il PRD PF1e in cache, OGL 1.0a) | `testing` | — | testing da questa PR (P11, ADR-0103) | [69](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L69) |
| verifica dei rimandi per sezione (`verifica_rimandi.py`, ADR-0148) | `testing` | 2026-11-20 | testing dal 2026-11-20 (`continue-on-error`); stable non prima del 2026-12-04 | [71](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L71) |
| cricchetto degli agenti (`prove_skill.py cricchetto --rigoroso`, ADR-0148) | `testing` | 2026-11-20 | testing dal 2026-11-20 (`continue-on-error`); stable solo dopo la misura dell'oscillazione e i 14 giorni | [72](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L72) |
| hook del custode della memoria (`--hook-merge`, `--hook-scrittura`, ADR-0151) | `testing` | 2026-11-27 | testing dal 2026-11-27: il merge si ferma solo per righe tolte non archiviate o `MEMORY.md` oltre 16.384 byte (card aperta al DM), la scrit… | [74](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L74) |
| milestone pronte (`milestone_pronte.py` sul registro `plans/milestone.json`, ADR-0152) | `testing` | — | testing dal merge (workflow `milestone.yml`, push su main e lunedì 06:35 UTC, solo riepilogo); stable dopo 14 giorni e 10 run su main senza… | [75](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L75) |
| instradamento degli agenti (`instradamento_agenti.py --check`, ADR-0154) | `testing` | — | testing dal merge (`continue-on-error`); stable non prima di 14 giorni, con le sette condizioni di ADR-0154 (10 run su main, 3 su PR che ca… | [76](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L76) |
| metriche dei classificatori (`eval_metriche.py`, ADR-0154) | `testing` | — | testing con il cancello che la usa, e sale con lui | [77](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L77) |
| lavoro in corso fuori da main (`lavoro_in_corso.py`, registro `plans/lavoro-in-corso.json… | `testing` | — | testing dal merge: in CI solo `--check` sul registro, offline; la pagina dipende da rete e macchina e non diventa un cancello | [78](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L78) |
| shapely | `testing` | 2026-10-23 | testing dal 2026-10-23 | [92](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L92) |
| scikit-learn | `testing` | 2026-11-27 | testing dal 2026-11-27 (Jfs: «le librerie standard de facto della community») | [93](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L93) |
| bpy, torch, piq | `testing` | — | testing locale (non girano in CI: ADR-0084) | [94](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L94) |
| pdfcpu | `testing` | — | testing (non provato in CI) | [103](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L103) |
| Chromium | `testing` | — | testing finché non c'è Chrome for Testing fissato (D10 di AMBIENTE) | [104](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L104) |
| libretto imposto | `testing` | — | testing | [122](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L122) |
| mappe: piante delle città | `testing` | — | testing | [125](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L125) |
| agenti: instradamento misurato (`--eval`, `--check`) | `testing` | — | testing | [131](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L131) |
| `converters/` | `testing` | 2026-10-23 | testing dal 2026-10-23 (D6, P9): Python 3.13, ruff, Dependabot, import di ogni modulo in CI | [134](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L134) |
| mypy | `unstable` | — | unstable, non si adotta | [61](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L61) |
| pyright | `unstable` | — | unstable | [62](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L62) |
| spaCy, Stanza | `unstable` | — | unstable | [95](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L95) |
| pandoc, xelatex | `unstable` | — | unstable (catena non pronta) | [105](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L105) |
| LanguageTool, java, mvn | `unstable` | — | unstable (facoltativo) | [106](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L106) |
| Blender | `unstable` | — | unstable fuori CI; il piano di scena è stdlib e stable | [107](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L107) |
| ComfyUI, distrobox | `unstable` | — | unstable fuori CI | [108](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L108) |
| LLM locale per la prosa | `unstable` | — | unstable | [109](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L109) |
| CLI `claude` (Claude Code) | `unstable` | — | unstable fuori CI: chiede una chiave e costa token; `binari.py` la elenca fra gli opzionali | [110](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L110) |
| mappe: 3D e immagini | `unstable` | — | unstable | [126](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L126) |
| prosa: sintassi | `unstable` | — | unstable | [128](PIANO-PIATTAFORMA-DI-SVILUPPO.md#L128) |

Gli stable sono 36 e stanno nel piano, con le loro misure.

## Dove guardare

- `MEMORIA.md`: ciò che è già su `main`, decisioni aperte e lista viva dei piani.
- `plans/contenuti-nei-rami.json` e `python3 scripts/contenuti_nei_rami.py --fetch`:
  i file che stanno in un ramo e mai su `main`.
- I thread cloud: claude.ai/code. Le cartelle `mnt` della tabella stanno in
  `/mnt/project-files` sulla macchina dei thread, non sul PC del DM.
- Le sessioni locali di Claude Code: `claude --resume`. OpenCode tiene le sue
  sessioni per conto suo (`opencode`, elenco delle sessioni).
