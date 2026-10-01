# Strumenti di terzi

Codice scritto fuori dal repo e copiato qui com'è. **Non è MIT**: ogni file
ha la licenza del suo autore, e la licenza viaggia con lui in questa cartella.
Decisione: [ADR-0076](../../plans/adr/ADR-0076-adozione-da-awesome-llm-apps.md),
che applica ADR-0010.

| File | Fonte | Commit | Licenza | Modificato |
|---|---|---|---|---|
| `skill_scanner.py` | [awesome-llm-apps `agent_skills/evals/tools/skill_scanner.py`](https://github.com/Shubhamsaboo/awesome-llm-apps/blob/4bf51ab704fb2c5b3803cd5191b30d7dcdb51dc2/agent_skills/evals/tools/skill_scanner.py), Shubham Saboo e contributori; entrato upstream col commit `ca8e5b3` (2026-07-08) | `4bf51ab` (2026-09-28) | Apache 2.0, [`LICENSE-APACHE-2.0`](LICENSE-APACHE-2.0) | no: identico, SHA-256 fissato in `scripts/tests/test_skill_scanner.py` |

Un aggiornamento si rivaluta a mano (ADR-0010 §3): si copia il file nuovo, il
test dell'impronta diventa rosso, e il diff si legge prima di cambiare
l'impronta.
