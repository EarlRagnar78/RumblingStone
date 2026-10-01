# ADR-0076 — Cosa entra da awesome-llm-apps, con che licenza, e cosa aspetta

- **Stato**: accettata
- **Data**: 2026-10-01
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: il DM, il 2026-09-30, sull'analisi di
  `Shubhamsaboo/awesome-llm-apps/agent_skills`: *«prendi e adatta solo quello
  che serve, script compresi, sempre con la logica del repo […] ADR per ogni
  codice adottato da fuori con la sua licenza e l'attribuzione»*; il
  2026-10-01, le risposte D1-D7 di PIANO-AGENT-SKILLS-ESTERNE
- **Rapporti**: applica [ADR-0010](ADR-0010-vendoring-skill-terzi.md)
  (cherry-pick, mai collezioni) e [ADR-0029](ADR-0029-licenza-doppia-testo-e-script.md)
  (testo CC BY-NC-SA, strumenti MIT); la valutazione completa è in
  [PIANO-AGENT-SKILLS-ESTERNE](../PIANO-AGENT-SKILLS-ESTERNE.md) §3

## Contesto

La cartella `agent_skills/` di awesome-llm-apps, letta al commit `4bf51ab`
(2026-09-28), ha otto skill e una cartella di strumenti di valutazione. Il
repository ha un `LICENSE` Apache 2.0 alla radice e nessun `NOTICE`. Sette
skill su otto dichiarano `Apache-2.0`; `first-reader` non dichiara niente (né
nel frontmatter né in `registry.json`) e ricade sotto la licenza della radice.

## Decisione

**1. Il codice copiato resta Apache 2.0, in una cartella sua.** Va in
`scripts/terzi/`, con il testo della licenza accanto
(`scripts/terzi/LICENSE-APACHE-2.0`) e la provenienza in
`scripts/terzi/README.md`. `LICENSES.md` ha una terza riga: gli strumenti del
repo sono MIT, quelli in `scripts/terzi/` hanno la licenza che dichiarano.

**2. Si copia identico quando si può, e un test lo controlla.** Lo scanner di
sicurezza delle skill (`evals/tools/skill_scanner.py`) entra senza una
modifica; `test_skill_scanner.py` ne fissa l'impronta SHA-256. Un aggiornamento
upstream è un diff da rivalutare a mano (ADR-0010 §3), e il test lo rende
visibile.

**3. Le idee si riscrivono, il codice adattato dichiara la sua origine.** Dalla
skill `first-reader` il repo prende quattro idee (la lettura a passaggi, il
diario, il ricordo dal diario, i lettori che rispondono): gli script che le
implementano sono riscritti per il repo e aprono con origine, commit, autore e
licenza, e la parola *modificato*, come chiede Apache 2.0 §4.

**4. Quello che si rimanda non sparisce.** Entra in
`plans/adozioni-in-attesa.json` con la fonte, il commit, la licenza e una
**condizione misurabile**; `scripts/adozioni_in_attesa.py --check` gira in CI
ed esce 1 quando una condizione è attiva su una voce ancora «in attesa». Prima
voce: `commit-archaeologist` (Matt Van Horn), che si adotta quando almeno tre
file di gioco cambiano dieci o più volte in sessanta giorni senza una riga di
storia nel sorgente (ADR-0069).

### Cosa entra, cosa no

| Da | Cosa | Come | Lotto |
|---|---|---|---|
| `evals/tools/skill_scanner.py` | lo scanner di sicurezza delle skill | copiato identico | L7 |
| `evals/tools/skill_lint.py` | il tetto di 1024 caratteri per la descrizione | riscritto in `validate_skills.py`, nessun codice copiato | L6 |
| `first-reader` | lettura a passaggi, ricordo, domande ai lettori, confronto fra letture, vista di chi scorre | riscritti, con l'origine dichiarata | L1, L2, L4, L5 |
| `evals/tools/run_trigger_evals.py` | prove d'instradamento delle skill | riscritte sulle frasi del DM e sugli strati di ORCHESTRAZIONE | L8 |
| `thinking-out-loud` | l'eco prima di applicare un blocco di decisioni | norma in `rumblingstone-plans`, con il suo rilevatore | L9 |
| `commit-archaeologist` | la storia di una riga da git | **in attesa**, con la condizione | L10 |
| `scope-creep-detector`, `dependency-doctor`, `project-graveyard`, `self-improving-agent-skills`, `advisor-orchestrator-worker` (il motore) | — | scartati, con la ragione in PIANO-AGENT-SKILLS §3 | — |

## Conseguenze

- Il repo ora contiene codice con tre licenze, e chi copia uno strumento deve
  guardare la cartella: `scripts/terzi/` non è MIT.
- Lo scanner ha già trovato un problema vero: `curl … | sh` in
  `dnd-35-srd/references/resources.md`, tolto (D5). In CI la regola resta:
  `test_skill_scanner.py` rimette quella riga in una skill finta e controlla
  che lo scanner la fermi.
- Quello che si paga: un file che non si può ritoccare. Se lo scanner
  segnalasse un falso positivo nel repo, la cura è il marcatore che lo scanner
  stesso prevede (`skillscan:allow` sulla riga), non una modifica al file.
- La condizione di `commit-archaeologist` si misura solo con la storia git
  completa: in un clone parziale lo script dice «non misurabile» invece di
  rispondere «spenta». In CI la storia c'è (`fetch-depth: 0`).
