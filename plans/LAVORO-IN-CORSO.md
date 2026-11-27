<!-- generata da scripts/lavoro_in_corso.py: non si scrive a mano.
     Fonte curata: plans/lavoro-in-corso.json. Rigenera: python3 scripts/lavoro_in_corso.py -->

# Lavoro in corso

Istantanea del 2026-11-27 15:56 UTC, generata da `scripts/lavoro_in_corso.py`: non si
scrive a mano. Si corregge il registro `plans/lavoro-in-corso.json`, poi si
rigenera con `python3 scripts/lavoro_in_corso.py` (`--fetch` per aggiornare
prima i rami, `--offline` senza rete). Dipende da rete, clone e macchina: è
una fotografia, non un cancello. Ciò che è già su `main` sta in `MEMORIA.md`.

## Filoni

| Filone | Stato | PR | Rami | Cartelle condivise | Thread | Aspetta | Prossimo |
|---|---|---|---|---|---|---|---|
| **Registro e runner unico delle misure dei componenti**<br>`misure-agenti` | `in-corso` | [#544](https://github.com/gsamuele78/RumblingStone/pull/544) bozza, oggi | `claude/project-thread-2yp4ga` | `agenti-eval-2026-11-27`<br>`instradamento-coda` | Misurare e migliorare agenti, skill e automatismi | — | finire la bozza della PR #544 (ADR-0155) e portarla a pronta |
| **Allineare i sette piani fermi**<br>`piani-fermi` | `in-corso` | [#542](https://github.com/gsamuele78/RumblingStone/pull/542) bozza, oggi | `claude/project-thread-198cay` | `audit-settimanale/piani-fermi-2026-11-27` | Allineare i sette piani fermi | — | chiusure con prova e numeri aggiornati nella PR #542, poi da bozza a pronta |
| **Preparare la sessione del 30 novembre (ARC-07 DEF-4 e DEF-5)**<br>`serata-30-novembre` | `aspetta-jfs` | [#541](https://github.com/gsamuele78/RumblingStone/pull/541) pronta, oggi | `claude/project-thread-3o4an2` | `serata-2026-11-30`<br>`tavole-serata-2026-11-30` | Preparare la sessione del 30 novembre | la revisione e il merge della PR #541 (pronta, ADR-0156) prima della serata | dopo il merge, il corredo della serata con dm.py corredo --stampa |
| **Allineare i Doni di Hella nei rimandi**<br>`doni-di-hella` | `in-corso` | [#539](https://github.com/gsamuele78/RumblingStone/pull/539) bozza, oggi | `claude/project-thread-fm157b` | — | Allineare i Doni di Hella nei rimandi | — | TRASVERSALE T9-bis nella bozza #539, poi pronta per la revisione |
| **Provare la trascrizione locale della serata**<br>`trascrizione-locale` | `fermo` | [#424](https://github.com/gsamuele78/RumblingStone/pull/424) bozza, 9 g fa | `claude/project-thread-kcq3f8` | — | Provare la trascrizione locale della serata | una decisione: il thread è risolto ma la bozza #424 è ancora aperta (ADR-0135 prenotato) | riprendere la prova su GPU locale o chiudere la PR e liberare ADR-0135 |
| **Immagini FLUX del Drappo (D2) sul portatile 4050**<br>`drappo-flux` | `aspetta-jfs` | — | — | `drappo-flux-2026-11-16`<br>`drappo-flux-kaggle-2026-11-21`<br>`drappo-flux-kaggle-2026-11-25`<br>`drappo-flux-kaggle-2026-11-27`<br>`prove-4050-risultati`<br>`kaggle-2026-11-18` | Scrivere lo script FLUX per il 4050 | guardare i confronti, o lanciare scripts/prove-4050/drappo-flux.sh sull'ASUS, e scegliere A o B; niente è mai girato su GPU locale | con la scelta, il lotto D2 delle immagini del Drappo |
| **Agenti e cascate: vincolo delle skill, custode della memoria, documentazione automatica**<br>`agenti-e-cascate` | `in-prova` | — | — | `agenti-2026-11-20`<br>`custode-memoria-2026-11-27`<br>`documentazione-automatica-2026-11-27` | Vincolare gli agenti all'uso delle skill (con Creare l'agente custode della memoria e Garantire che la documentazione si aggiorni da sola) | — | le regole sono su main; si misura nel canale testing (ADR-0099) prima di dirle stabili |
| **Rendere visibile il lavoro in corso (questa pagina)**<br>`lavoro-in-corso` | `in-corso` | — | `claude/project-thread-65g5a1` | — | Rendere visibile il lavoro in corso | — | PR del registro e dello script, poi la documentazione |

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

## Dove guardare

- `MEMORIA.md`: ciò che è già su `main`, decisioni aperte e lista viva dei piani.
- `plans/contenuti-nei-rami.json` e `python3 scripts/contenuti_nei_rami.py --fetch`:
  i file che stanno in un ramo e mai su `main`.
- I thread cloud: claude.ai/code. Le cartelle `mnt` della tabella stanno in
  `/mnt/project-files` sulla macchina dei thread, non sul PC del DM.
- Le sessioni locali di Claude Code: `claude --resume`. OpenCode tiene le sue
  sessioni per conto suo (`opencode`, elenco delle sessioni).
