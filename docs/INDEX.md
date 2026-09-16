# 📚 Indice della documentazione — RumblingStone

> Punto d'ingresso unico e **categorizzato** a tutta la documentazione del
> repo: tool/script, guide, governance (ADR), archivio piani, skill e
> contenuti di campagna. Creato dall'audit script del 2026-07-24.
>
> Se cerchi **come si usa uno strumento**, parti da §2. Se cerchi **perché
> una cosa è fatta così**, parti da §4 (ADR).

---

## 1. Start here

| Documento | Cos'è |
|---|---|
| [`README.md`](../README.md) | Panoramica del repo |
| [`AGENTS.md`](../AGENTS.md) | Regole operative per agenti/collaboratori (canone, no-invenzione, struttura) |
| **questo file** (`docs/INDEX.md`) | Indice maestro della documentazione |

## 2. Tool & script (automazione DM)

Contratto macchina e vista umana — **generati** dal manifest, sempre allineati al codice.

| Documento | Cos'è |
|---|---|
| [`docs/tools/README.md`](tools/README.md) | **Registro dei tool** categorizzato (A–J), leggibile — generato |
| [`docs/tools/registry.json`](tools/registry.json) | Registro **machine-readable** per orchestratori/altri tool |
| [`docs/tools/mcp-tools.json`](tools/mcp-tools.json) | Vista in stile **MCP tool-definitions** |
| [`scripts/tools.manifest.json`](../scripts/tools.manifest.json) | **Fonte di verità** dei contratti per-tool |
| [`scripts/schemas/tool_manifest.schema.json`](../scripts/schemas/tool_manifest.schema.json) | JSON Schema del manifest |
| [`scripts/README-automation.md`](../scripts/README-automation.md) | Guida discorsiva al toolkit DM + CLI `dm.py` |
| [`scripts/README.md`](../scripts/README.md) | Pipeline build/sync delle skill |
| [`scripts/README-import-ultraclear.md`](../scripts/README-import-ultraclear.md) | Contratto I/O di `import_ultraclear.py` |
| [`scripts/examples/README.md`](../scripts/examples/README.md) | Esempi di contratto JSON mappe (Modalità 3) |

## 3. Qualità, standard & audit

| Documento | Cos'è |
|---|---|
| [`docs/guides/GUIDA-CONDIVISIONE-IP.md`](guides/GUIDA-CONDIVISIONE-IP.md) | **Guida completa condivisione**: cosa si può fare con il materiale (tavolo, giocatori, amici, pubblicazione gratuita, vendita) — i tre corpi di IP, la procedura per ogni caso, confini per le illustrazioni, casi pratici risolti, checklist |
| [`docs/guides/GUIDA-SETUP-MACCHINA.md`](guides/GUIDA-SETUP-MACCHINA.md) | **Guida completa setup**: da repo clonato a «funziona tutto» — prerequisiti (cosa serve e cosa è opzionale), skill per agenti, hook git, branch di gruppo (ADR-0007), extra (PDF/pandoc/container), verifica finale coi controlli della CI, troubleshooting |
| [`docs/guides/GUIDA-BOOKLET-E-PDF.md`](guides/GUIDA-BOOKLET-E-PDF.md) | **Guida completa end-to-end**: dai master ai booklet (HTML/Homebrewery) ai **PDF A4** per giocatori e DM — prerequisiti per ogni sistema, anatomia del manifest, container opzionali, troubleshooting, checklist di consegna |
| [`docs/guides/GUIDA-FLUSSO-LOCALE.md`](guides/GUIDA-FLUSSO-LOCALE.md) | **Come far lavorare insieme tutti i tool**: le quattro famiglie e cosa fa ognuna, la regola «il markdown è la verità», il flusso di una serata prima/al tavolo/dopo, le **due catene dei booklet** (schermo e stampa), la catena delle immagini, e cosa il repo **non** fa e perché |
| [`docs/guides/GUIDA-IMMAGINI.md`](guides/GUIDA-IMMAGINI.md) | **Guida completa immagini**: quale generatore per cosa, come si scrive un prompt che funziona (esempio smontato + i 3 trucchi), preparare un arco intero con `dm.py prompts`, bibbia visiva e scena-madre, dove salvare/come agganciare i risultati, troubleshooting, checklist spoiler+IP |
| [`docs/guides/GUIDA-MAPPE.md`](guides/GUIDA-MAPPE.md) | **Guida completa mappe**: le 3 modalità, griglia emoji e legenda universale, contratto JSON per eserciti/strutture, import Watabou e ultra-clear, render SVG, export **PNG e UVTT (Foundry/Roll20 con muri e luci)**, troubleshooting della CI |
| [`docs/guides/GUIDA-BESTIARIO.md`](guides/GUIDA-BESTIARIO.md) | **Guida completa bestiario**: dove va un mostro/PNG/villain, naming e CR, formato statblock obbligatorio, dossier, flag di canone, rigenerazione del catalogo, gate CI, **quando potenziare invece di creare** |
| [`docs/guides/TOOL-AUTHORING-STANDARD.md`](guides/TOOL-AUTHORING-STANDARD.md) | **Standard obbligatorio** per ogni nuovo tool (checklist + verifica CI) |
| [`docs/audit/AUDIT-REPORT.md`](audit/AUDIT-REPORT.md) | Report d'audit degli script (findings azionabili) |
| [`docs/audit/SCORECARD.md`](audit/SCORECARD.md) | Scorecard 12-assi per script |
| [`docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md`](audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md) | Quanto il testo di campagna **nomina** cose di altri, per arco e per 1.000 parole — misura, non parere legale |

## 4. Governance & decisioni (ADR)

Il **perché** delle scelte strutturali. Indice completo in [`plans/adr/`](../plans/adr/).

| ADR | Tema |
|---|---|
| [ADR-0000](../plans/adr/ADR-0000-template.md) | Template |
| [ADR-0001](../plans/adr/ADR-0001-archivio-piani-con-puntatori.md) | Archivio piani con puntatori |
| [ADR-0002](../plans/adr/ADR-0002-cli-unica-dm-orchestratore.md) | `dm.py` come CLI orchestratrice unica |
| [ADR-0003](../plans/adr/ADR-0003-markdown-master-layout-generati.md) | Markdown master, layout generati |
| [ADR-0004](../plans/adr/ADR-0004-homebrewery-self-hosted.md) | Homebrewery self-hosted |
| [ADR-0005](../plans/adr/ADR-0005-confini-ip-uso-non-commerciale.md) | Confini IP / uso non commerciale |
| [ADR-0006](../plans/adr/ADR-0006-annotazioni-mappa-overlay-professionale.md) | Overlay professionale mappe |
| [ADR-0007](../plans/adr/ADR-0007-scritture-canone-triplo-vincolo.md) | Scritture canone: triplo vincolo |
| [ADR-0008](../plans/adr/ADR-0008-governance-set-skill-focalizzate.md) | Governance del set di skill |
| [ADR-0009](../plans/adr/ADR-0009-gate-tracciatura-changelog-adr.md) | Gate CHANGELOG + promemoria ADR |
| [ADR-0010](../plans/adr/ADR-0010-vendoring-skill-terzi.md) | Vendoring skill di terzi |
| [ADR-0011](../plans/adr/ADR-0011-de-collisione-scripts-converters.md) | De-collisione `Script/` → `converters/` |
| [ADR-0012](../plans/adr/ADR-0012-standard-ingegneria-tool-verificabile.md) | Standard di ingegneria verificabile in CI |
| [ADR-0013](../plans/adr/ADR-0013-standard-generazione-booklet-sessioni.md) | Standard di generazione dei booklet (stile, anti-spoiler, HTML/Homebrewery/PDF) |
| [ADR-0014](../plans/adr/ADR-0014-regia-sensoriale-obbligatoria.md) | Regia sensoriale obbligatoria nei master (descrizioni sempre, occhio da avventuriero) |
| [ADR-0015](../plans/adr/ADR-0015-standard-prompt-immagine.md) | Standard dei prompt immagine (estrazione scene, anatomia, coerenza d'arco) |
| [ADR-0016](../plans/adr/ADR-0016-lingua-sorgente-e-edizioni.md) | **Lingua sorgente italiana**; l'inglese è un'edizione derivata per transcreation, mai la stesura. Loc kit in `campaign/GLOSSARIO-E-LOCALIZZAZIONE.md` |
| [ADR-0017](../plans/adr/ADR-0017-moduli-autoconclusivi-classe-di-artefatto.md) | I moduli autoconclusivi (`STANDALONE-*`) sono una classe di artefatto a sé: contratto di file, gate proprio, generatori locali ammessi a condizioni |
| [ADR-0018](../plans/adr/ADR-0018-apparato-uso-obbligatorio.md) | L'apparato d'uso (cast, pronuncia, indice read-aloud, schermo) è parte del contenuto, non un extra |
| [ADR-0019](../plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md) | **Per le immagini generate la licenza sta nei pesi, non nel software**: SDXL e FLUX schnell sì, FLUX dev no; provenienza obbligatoria |
| [ADR-0020](../plans/adr/ADR-0020-edizione-da-stampa-su-un-secondo-binario.md) | L'edizione da stampa esce da **Typst** su un secondo binario, non dal browser; la catena HTML resta intatta |
| [ADR-0021](../plans/adr/ADR-0021-statblocchi-machine-readable.md) | I numeri delle schede sono un **dato**, non una frase: statblocchi machine-readable, GS coerente, gate in CI |
| [ADR-0022](../plans/adr/ADR-0022-competenza-guadagnata-sul-campo.md) | La competenza si guadagna sul campo, **ma con un tetto**: Acume, Perizia, Metodo |
| [ADR-0023](../plans/adr/ADR-0023-colophon-di-edizione.md) | Ogni volume porta il proprio colophon, e **la data non si deduce** |
| [ADR-0024](../plans/adr/ADR-0024-skill-edizione.md) | La diciassettesima skill: `rumblingstone-edizione`, il mestiere di chi risponde di cosa esce dal repo |
| [ADR-0025](../plans/adr/ADR-0025-riapertura-prosa-tradotta.md) | Il banco di prova di ADR-0016 ha dato **esito negativo**: la norma della prosa si misura, non si dichiara |
| [ADR-0026](../plans/adr/ADR-0026-vendoring-pacchetti-typst.md) | I pacchetti Typst si **vendorizzano**: la build non scarica niente |
| [ADR-0027](../plans/adr/ADR-0027-imposizione-con-pdfcpu.md) | `pdfcpu` come seconda dipendenza binaria, e la regola di **degradazione** quando manca |
| [ADR-0028](../plans/adr/ADR-0028-abbazia-master-markdown.md) | Anche un modulo nato in HTML ha un **master markdown** |
| [ADR-0029](../plans/adr/ADR-0029-licenza-doppia-testo-e-script.md) | **Licenza doppia**: CC BY-NC-SA sul testo, MIT sugli script |
| [ADR-0030](../plans/adr/ADR-0030-server-mcp-sui-tool.md) | Il server MCP esiste, ed è **read-only per difetto** |
| [ADR-0031](../plans/adr/ADR-0031-dm-volume-ordine-dei-mestieri.md) | `dm.py volume`: l'ordine dei mestieri, e il cancello detto a voce |
| [ADR-0032](../plans/adr/ADR-0032-misurare-la-leggibilita.md) | Misurare la **leggibilità** dell'artefatto, e perché veraPDF resta fuori dalla CI |
| [ADR-0033](../plans/adr/ADR-0033-derivare-e-dichiararlo.md) | Leggere prima di derivare, e **non derivare alla cieca** |
| [ADR-0034](../plans/adr/ADR-0034-generare-dalle-tabelle.md) | Generare dalle tabelle, e **dichiarare la taratura** |
| [ADR-0035](../plans/adr/ADR-0035-due-prose-due-norme.md) | **Due prose, due norme**: quella di gioco e quella dei documenti non si giudicano con lo stesso metro |
| [ADR-0036](../plans/adr/ADR-0036-misurare-il-miglioramento-non-lo-stato.md) | Misurare **il miglioramento**, non lo stato |
| [ADR-0037](../plans/adr/ADR-0037-stdlib-only-e-le-sue-eccezioni.md) | **Stdlib-only**, e le eccezioni che esistono davvero: binari sì, pacchetti Python no (salvo `pyyaml` e `Pillow`) |
| [ADR-0038](../plans/adr/ADR-0038-l-el-viene-da-una-gerarchia-dichiarata.md) | L'EL viene da una **gerarchia dichiarata**, non da un numero nel codice |
| [ADR-0039](../plans/adr/ADR-0039-profili-regole-multisistema.md) | **Profili di regole multi-sistema**: il motore è neutro, 3.5 / PF1e / 5e sono file sostituibili (era ADR-0016 nella #72) |
| [ADR-0040](../plans/adr/ADR-0040-separazione-prodotto-e-toolkit-estraibile.md) | Separazione dei due prodotti e rilicenziamento del toolkit (era ADR-0017 nella #72) |
| [ADR-0041](../plans/adr/ADR-0041-instradamento-delle-skill-con-un-gate.md) | L'instradamento delle skill è un principio, e **un gate lo verifica** |
| [ADR-0042](../plans/adr/ADR-0042-tre-glifi-per-tre-cose.md) | Tre cose sotto un glifo: `⬛` si separa in **edificio, tenda e dais** |
| [ADR-0043](../plans/adr/ADR-0043-le-montagne-sono-muri-e-nessun-master-esce-dal-controllo.md) | **Le montagne sono muri**, e nessun master esce dal controllo di `validate_maps` |
| [ADR-0044](../plans/adr/ADR-0044-prima-si-guardano-i-piani-che-ci-sono.md) | Prima di aprire un piano, **si guardano quelli che ci sono** |
| [ADR-0045](../plans/adr/ADR-0045-ogni-lotto-dichiara-engine-effort-e-qualita.md) | Ogni lotto dichiara **engine, effort e qualità attesa** — e se lavora su un insieme, il comando che lo enumera |
| [ADR-0046](../plans/adr/ADR-0046-un-rifiuto-senza-motivo-non-parte.md) | **Un rifiuto senza motivo non parte**: `--reroll` esige `--motivo`, e lo scarto si registra |
| [ADR-0047](../plans/adr/ADR-0047-le-decisioni-aperte-hanno-una-casa-sola.md) | Le decisioni aperte hanno **una casa sola**, e l'elenco si genera |
| [ADR-0048](../plans/adr/ADR-0048-legenda-funzionale-fonte-unica.md) | La **legenda funzionale è la fonte unica**: la funzione di gioco di un simbolo è un dato, non prosa né un `set` cablato (era ADR-0014 nella #72) |
| [ADR-0049](../plans/adr/ADR-0049-edizione-commerciale-ap-originale.md) | 🔵 **Proposta**: l'edizione commerciale è un **AP originale autonomo**, mai un'espansione di *Red Hand of Doom* — gate: decisione DM + avvocato IP (era ADR-0018 nella #72) |
| [ADR-0050](../plans/adr/ADR-0050-stato-di-campagna-dati-e-prosa.md) | **Lo stato di campagna: dati validati per i fatti, markdown per la prosa** — le tabelle di `state.md` si generano da `state.yaml`; il tempo non dichiarato si **conta**, non si indovina (era ADR-0017 nella #99) |
| [ADR-0051](../plans/adr/ADR-0051-il-margine-del-bosco-e-un-glifo-a-se.md) | **Il margine del bosco è un glifo a sé**: `🌲` diventa opaco, la fascia che si attraversa no — perché il muro del VTT è binario e il bosco non lo è |

## 5. Archivio piani

| Documento | Cos'è |
|---|---|
| [`plans/INDEX.md`](../plans/INDEX.md) | Stato di tutti i piani (% e gate) |
| [`plans/CHANGELOG.md`](../plans/CHANGELOG.md) | Una riga per lotto chiuso (ADR-0009) |
| [`plans/`](../plans/) | Piani e ricerche (`PIANO-*`, `RICERCA-*`) |

## 6. Convertitori di contenuto

| Documento | Cos'è |
|---|---|
| [`converters/README.md`](../converters/README.md) | Panoramica convertitori (ex `Script/`, ADR-0011) |
| [`converters/pdf-to-md-engine/README.md`](../converters/pdf-to-md-engine/README.md) | PDF ↔ Markdown |
| [`converters/Html_to_markdown/README.md`](../converters/Html_to_markdown/README.md) | HTML → Markdown |
| [`converters/Image-to-webp/README.md`](../converters/Image-to-webp/README.md) | Immagini → WebP |

## 7. Infrastruttura locale (opt-in)

| Documento | Cos'è |
|---|---|
| [`scripts/comfyui-local/README.md`](../scripts/comfyui-local/README.md) | Passata "hero map" ComfyUI (GPU locale) |
| [`scripts/homebrew-local/README.md`](../scripts/homebrew-local/README.md) | The Homebrewery self-hosted (ADR-0004) |

## 8. Skill multi-agente

Sorgenti canoniche in [`skills/`](../skills/) (pipeline build in §2). Set focalizzato per ADR-0008.

| Skill | Ambito |
|---|---|
| `dnd-35-srd` | Meccaniche d20 SRD |
| `forgotten-realms-lore` | Canone Faerûn 1372 DR |
| `pathfinder-1e-srd` | PF1e + conversione 3.5 |
| `npc-villain-boosting` | Potenziamento PNG/villain/mostri |
| `rumblingstone-campaign` | PG, artefatti, archi, coerenza |
| `rumblingstone-automation` | CLI `dm.py` e pipeline stato-sessioni |
| `rumblingstone-mapmaking` | Pipeline mappe tattiche |
| `rumblingstone-module-standard` | Standard qualità dei moduli DEF |
| `rumblingstone-narrative-style` | Motore di stile narrativo — **nove pilastri**, il nono ancorato a Eco |
| `rumblingstone-debugging` | Root-cause su infrastruttura |
| `rumblingstone-plans` | Disciplina archivio piani |
| `dnd-35-rules` | Meta-router legacy (compat) |

## 9. Contenuti di campagna (censimenti)

| Documento | Cos'è |
|---|---|
| [`CENSIMENTO-MOSTRI-PNG-VILLAIN.md`](../CENSIMENTO-MOSTRI-PNG-VILLAIN.md) | Censimento della libreria mostri/PNG/villain |
| [`MAPPE-CENSIMENTO.md`](../MAPPE-CENSIMENTO.md) | Censimento delle mappe |
| [`Bestiario/README.md`](../Bestiario/README.md) | Struttura della libreria Bestiario |

---

_Indice mantenuto a mano: aggiungendo una nuova guida o ADR, aggiungi qui la riga.
Il registro dei tool (§2) è invece **generato** — non si modifica a mano._
