# ADR-0011 — De-collisione `Script/` → `converters/`

**Stato**: accettata
**Data**: 2026-07-24
**Decisione-fonte**: richiesta DM (audit script, 2026-07-24) — "sì, entrambe + de-collisione".
**Relazione**: esegue la fusione **rinviata** da [ADR-0002](ADR-0002-cli-unica-dm-orchestratore.md)
("l'eventuale fusione resta possibile in futuro con un ADR dedicato").

## Contesto

Il repo aveva due cartelle top-level con nomi che differiscono solo per il
case: `scripts/` (automazione DM) e `Script/` (convertitori di contenuto
pdf→md, html→md, immagini→webp). Su filesystem **case-insensitive**
(macOS default, Windows) le due cartelle collidono: `git checkout` e i merge
possono comportarsi in modo imprevedibile, e umani/agenti le confondono di
continuo (ADR-0002 lo cita come motivo per NON fondere allora — beneficio
solo estetico contro un costo di path elevato).

L'audit (`docs/audit/AUDIT-REPORT.md`, F5) ha riconfermato il rischio; il DM
ha autorizzato la de-collisione.

## Decisione

Rinominare la cartella dei convertitori da `Script/` a **`converters/`**
(nome descrittivo, minuscolo, nessuna collisione). La rinomina è un
`git mv` che preserva la storia.

Si aggiornano **solo i riferimenti che puntano alla cartella del repo**:

- `.github/workflows/ci.yml` — `compileall -q scripts Script` → `scripts converters`;
- `scripts/check_plans_discipline.py` — `STRUCTURAL_PREFIXES` include `converters/`;
- `.gitignore` — pattern `Script/...` → `converters/...`;
- `scripts/tools.manifest.json` + artefatti generati (`docs/tools/*`);
- `AGENTS.md`, `scripts/README*.md`, `skills/rumblingstone-plans/SKILL.md`,
  `converters/README.md`, `converters/pdf-to-md-engine/PROJECT_STATUS.md`;
- nota di supersessione in ADR-0002.

**NON** si toccano i riferimenti interni allo strumento `Image-to-webp`
(`conver_webp_new.sh`, `setup.sh`, il suo README): lì `Script/` è una
cartella di **staging propria del tool**, creata relativamente alla `PWD`
dell'utente (`SOURCE_DIR="${PWD}/Script"`), non un puntatore alla cartella
del repo. Rinominarla cambierebbe il *comportamento a runtime* del
convertitore, non un percorso di repo — fuori dallo scopo di questa ADR.
(Quirk pre-esistente di quel tool; eventuale rinomina in una ADR sua.)

I documenti d'archivio (`plans/*.md`, `plans/CHANGELOG.md`, `docs/audit/*`)
che citano `Script/` come **stato storico** restano invariati: descrivono il
prima, non un percorso vivo.

## Conseguenze

- Fine della collisione case-insensitive: checkout/merge deterministici ovunque.
- Un solo nome ovvio per i convertitori; la disambiguazione "Script vs scripts"
  nei README diventa storia.
- Costo una-tantum: la PR tocca ~10 file di riferimento + la rinomina. La
  storia git dei file convertiti è preservata (`git mv`).
- `dm.py` non è impattato (non invoca i convertitori).

## Alternative scartate

- **Fondere i convertitori dentro `scripts/`**: mescolerebbe due domini
  (automazione DM stdlib-only vs toolchain esterne) — no.
- **Lasciare `Script/`** e vivere con la collisione: il rischio su FS
  case-insensitive è reale e ricorrente. No.
