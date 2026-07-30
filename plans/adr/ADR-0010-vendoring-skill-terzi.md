# ADR-0010 — Vendoring di skill di terzi (cherry-pick, mai collezioni)

- **Stato**: accettato (DM, 2026-07-23)
- **Contesto**: il DM ha chiesto se aggiungere al repo collezioni di skill
  community (Understand-Anything, ECC/everything-claude-code, obra/superpowers,
  nexu-io/open-design, mattpocock/skills). La valutazione (registrata in
  `skills/rumblingstone-mapmaking/references/audit-mappe-workflow.md` §Tool
  esterni e in `plans/CHANGELOG.md` 2026-07-23) ha concluso che le collezioni
  intere danneggiano il repo: **inquinano il triggering** delle skill curate
  (ogni descrizione entra nel contesto degli agenti), ampliano la **superficie
  di fiducia** (istruzioni di terzi in un repo canon-sensibile: 3.5, italiano,
  CD non DC) e creano **manutenzione** (mirror, update upstream).

## Decisione

1. **Mai installare collezioni/plugin esterni in blocco.** Niente marketplace
   plugin, niente set da centinaia di skill.
2. **Cherry-pick consentito**, una skill alla volta, SOLO se:
   - licenza compatibile (MIT/Apache/BSD) con **attribuzione** completa
     (repo, autore, commit, data) nel file vendorizzato;
   - **vendorizzata** in `skills/` (mai dipendenza esterna live): passa da
     `validate_skills` e dai mirror `build-skills.sh` come ogni skill interna;
   - **adattata**: trigger ristretti al dominio reale d'uso, esempi locali,
     riferimenti a skill non vendorizzate rimossi;
   - **non sovrapposta** a una skill esistente (ADR-0008: una skill per
     dominio) e con riga in `plans/CHANGELOG.md`;
   - contenuto compatibile con gli standard del repo (niente 5e-ism, niente
     convenzioni che confliggono con l'italiano/3.5).
3. Gli **update upstream** NON sono automatici: si rivaluta il diff a mano,
   solo se serve.

## Prima applicazione

`skills/rumblingstone-debugging/` — vendorizzata `systematic-debugging` da
[`obra/superpowers`](https://github.com/obra/superpowers) (MIT, © 2025 Jesse
Vincent, commit `d884ae0`): metodo delle 4 fasi per la causa radice, con
trigger limitati a **infrastruttura** (`scripts/`, CI, pytest, renderer,
dm.py) — esplicitamente NON per il contenuto di campagna. Reference
vendorizzate: root-cause-tracing, defense-in-depth, condition-based-waiting,
find-polluter.sh. Scartati: esempi TypeScript, fixture di eval, cross-ref a
skill superpowers non vendorizzate.

## Conseguenze

- Il set skill resta curato e piccolo (12 dopo questa aggiunta); il triggering
  resta preciso.
- Ogni futura richiesta «aggiungiamo la skill/collezione X?» si valuta contro
  i 5 criteri del punto 2 — la risposta di default alle collezioni è no.
