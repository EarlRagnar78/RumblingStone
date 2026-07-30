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
| [`docs/guides/GUIDA-BOOKLET-E-PDF.md`](guides/GUIDA-BOOKLET-E-PDF.md) | **Guida completa end-to-end**: dai master ai booklet (HTML/Homebrewery) ai **PDF A4** per giocatori e DM — prerequisiti per ogni sistema, anatomia del manifest, container opzionali, troubleshooting, checklist di consegna |
| [`docs/guides/TOOL-AUTHORING-STANDARD.md`](guides/TOOL-AUTHORING-STANDARD.md) | **Standard obbligatorio** per ogni nuovo tool (checklist + verifica CI) |
| [`docs/audit/AUDIT-REPORT.md`](audit/AUDIT-REPORT.md) | Report d'audit degli script (findings azionabili) |
| [`docs/audit/SCORECARD.md`](audit/SCORECARD.md) | Scorecard 12-assi per script |

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
| `rumblingstone-narrative-style` | Motore di stile narrativo |
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
