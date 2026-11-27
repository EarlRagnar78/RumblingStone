---
paths:
  - "skills/**"
  - "scripts/build-skills.sh"
  - "scripts/sync-skills.sh"
  - "scripts/validate_skills.py"
  - ".claude/**"
---
<!-- Generato da scripts/regole_claude.py da AGENTS.md (ADR-0141): si corregge AGENTS.md, poi si rigenera. I percorsi sono dalla radice del repo. -->
### Inventario completo

Diciotto skill. L'elenco è **verificato da un gate**
([ADR-0041](plans/adr/ADR-0041-instradamento-delle-skill-con-un-gate.md)):
`validate_skills.py` fallisce se una directory con `SKILL.md` non è citata qui,
o se questo documento cita una skill che non esiste. Nessun agente «scopre»
queste skill da solo: è questa sezione a instradarli.

| Skill | Che cos'è |
|---|---|
| `skills/dnd-35-srd/` | meccaniche d20 SRD pure |
| `skills/pathfinder-1e-srd/` | regole PF1e, template semplici, benchmark GS, conversione 3.5↔PF1e |
| `skills/forgotten-realms-lore/` | canone di Faerûn, 1372 DR |
| `skills/npc-villain-boosting/` | quando e come potenziare PNG, villain e mostri |
| `skills/rumblingstone-campaign/` | questa campagna: PG, artefatti, archi, coerenza |
| `skills/rumblingstone-narrative-style/` | motore di stile a nove pilastri, protagonismo dei PG nel bene e nel male |
| `skills/rumblingstone-indagine/` | come si costruisce e si gioca un **caso**: nodo d'indizio, registro Acume/Perizia/Metodo (ADR-0022), ricomposizione, vicolo cieco |
| `skills/rumblingstone-prosa-documenti/` | come si scrivono i **documenti** del repo perché non suonino generati a macchina |
| `skills/rumblingstone-module-standard/` | standard di qualità dei master DEF (benchmark: Red Hand of Doom + AP Pathfinder 1e) |
| `skills/rumblingstone-editoria/` | layout e tipografia: riquadri, blocchi statistiche, dove si tocca (nel tema, mai nel `.typ` generato) |
| `skills/rumblingstone-edizione/` | il mestiere dell'editore: colophon, Product Identity / Open Content, **gate d'uscita** IP, versione/ristampa/errata |
| `skills/rumblingstone-art-direction/` | coerenza di un set di immagini, e quando un'immagine si butta ([ADR-0019](plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md)) |
| `skills/rumblingstone-mapmaking/` | generazione mappe: Watabou, template, export VTT |
| `skills/rumblingstone-automation/` | CLI `dm.py` e pipeline sessione→stato; scritture di canone solo sotto il vincolo triplo ADR-0007 |
| `skills/rumblingstone-playtest/` | collaudo: audit meccanico, dry-run, schede di feedback, alfa → beta → collaudato ([ADR-0018](plans/adr/ADR-0018-apparato-uso-obbligatorio.md)) |
| `skills/rumblingstone-plans/` | convenzioni dell'archivio dei piani: INDEX, gate, ADR |
| `skills/rumblingstone-debugging/` | debugging per root cause, **solo infrastruttura**; vendorizzata da obra/superpowers (MIT), ADR-0010 |
| `skills/dnd-35-rules/` | meta-router legacy: rimanda alle skill qui sopra |

### Gli agenti di `.claude/agents/`

Quattordici agenti ([ADR-0146](plans/adr/ADR-0146-le-skill-di-prosa-si-caricano-per-vincolo.md)),
ognuno con le sue skill precaricate. Li lancia il thread con lo strumento Agent
(`subagent_type: "<nome>"`); un agente non ne avvia altri, quindi la catena la
guida il thread. Ogni catena che cambia file finisce con `autore-documenti`, e
la riga «Catena: a → b» nelle istruzioni del thread ferma push e PR finché
manca una chiamata (`scripts/instradamento_agenti.py --cancello`).

| Agente | Classe | Quando |
|---|---|---|
| `autore-prosa-gioco` | Autori | box read-aloud, handout, recap, dialoghi, introduzioni e appendici dei volumi |
| `autore-master` | Autori | master DEF di un arco: stanze, incontri, tattiche, bottega |
| `autore-documenti` | Autori | ADR, piani, guide, corpi di PR; la documentazione dopo ogni lavoro |
| `integratore-dm` | Tecnici | `dm.py`, `dmcore`, plugin di sistema, server MCP, manifest degli strumenti |
| `sviluppatore` | Tecnici | il resto di `scripts/`, CI, test, hook |
| `piattaforma` | Tecnici | canali, versioni fissate, promozioni, rilasci, roadmap |
| `cartografo` | Tecnici | mappe tattiche, Watabou, UVTT |
| `impaginatore` | Tecnici | booklet, PDF, typst, licenze e gate d'uscita |
| `art-director` | Tecnici | immagini, prompt, set coerenti |
| `regolista` | Tecnici | statblock, schede, potenziamenti, arbitrati 3.5 e PF1e |
| `sincronizzatore-giocato` | Tecnici | il giocato sul ramo di gruppo e il merge di main in quel ramo ([ADR-0149](plans/adr/ADR-0149-il-giocato-arriva-sul-ramo-di-gruppo-con-un-agente-e-una-misura.md)) |
| `custode-memoria` | Tecnici | che cosa sanno memoria del progetto, file storico e coda; righe tolte da `MEMORY.md`, tetto della memoria, merge fermato dal custode ([ADR-0151](plans/adr/ADR-0151-la-memoria-del-progetto-ha-uno-specchio-e-un-custode.md)) |
| `lettore-a-freddo` | Verificatori, sola lettura | lettura a freddo di prosa o master appena scritti |
| `custode-canone` | Verificatori, sola lettura | coerenza con il canone della campagna e del 1372 DR |

Un agente nuovo entra in questa tabella nella stessa PR: la CI lo controlla
con `scripts/documentazione_allineata.py`
([ADR-0153](plans/adr/ADR-0153-la-documentazione-segue-la-struttura.md)).

