---
name: rumblingstone-debugging
description: >
  Debugging sistematico per causa radice, SOLO per l'INFRASTRUTTURA di
  RumblingStone — scripts/ (validator, renderer, dm.py, builder del catalogo),
  workflow CI (.github/workflows), test pytest, hook git. Va usata quando
  compare un problema tecnico, PRIMA di proporre qualunque fix: "CI rosso",
  "CI failure", "test fallisce",
  "validate_modules/maps/bestiario/skills fallisce", "bug nello script",
  "render sbagliato", "SVG non allineato", "rendering non deterministico",
  "catalogo out of sync", "hook pre-push fallisce", "dm.py errore", stack
  trace, exit code non-zero. NON va usata per le domande di contenuto della
  campagna (regole 3.5, canone, mappe come contenuto): quelle hanno le loro
  skill.
---

# Systematic Debugging (infrastruttura RumblingStone)

> **Origine**: vendorizzata da [`obra/superpowers`](https://github.com/obra/superpowers)
> `skills/systematic-debugging` (MIT License, © 2025 Jesse Vincent, commit <!-- validate-docs: ignore -->
> `d884ae0`) — adattata a questo repo: trigger ristretti a `scripts/`/CI,
> esempi locali, riferimenti esterni rimossi. Politica di vendoring e data:
> `plans/adr/ADR-0010-vendoring-skill-terzi.md`.

**Legge di ferro** (le fix a caso creano bug nuovi; le patch rapide mascherano il problema):
```
NESSUNA FIX SENZA PRIMA L'INVESTIGAZIONE DELLA CAUSA RADICE
```
Senza la Fase 1 completa niente fix: ANCHE se ovvia, ANCHE di fretta, ANCHE dopo 2 tentativi falliti (*soprattutto* allora).

## Quando no

Perimetro: SOLO infrastruttura (pytest, `validate_*`, renderer e SVG, `dm.py`,
CI, hook git, `build_monster_catalog` out-of-sync). **NON** per il contenuto
(canone, regole, prosa): là valgono le skill di campagna.

## Fonti

Tecniche di supporto, in `references/`:
- **`root-cause-tracing.md`**: risalire lo stack fino al trigger originale.
- **`defense-in-depth.md`**: dopo la causa radice, validazione a più livelli (il pattern dei `validate_*`).
- **`condition-based-waiting.md`**, mai sleep arbitrari: poll di una
  condizione con timeout (CI, processi, render).
- **`find-polluter.sh`**: bisezione per trovare il test che inquina lo stato
  (esempio d'uso pytest incluso).

- Caso studio interno (bug «celle fantasma» del renderer: diagnosi → contratto →
  fix → non-regressione byte-identica): `plans/PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md`.

## Procedura

Quattro fasi, ognuna completa prima della successiva.
### Fase 1 — Investigazione della causa radice
1. **Leggi il messaggio d'errore per intero** (stack trace completo, riga,
   file, exit code — spesso contiene la soluzione esatta).
2. **Riproduci in modo consistente** (comando esatto; se non riproducibile →
   raccogli dati, non tirare a indovinare).
3. **Controlla i cambi recenti** (`git diff`, ultimi commit, config, ambiente).
4. **Sistemi multi-componente** (es. master `.md` → parser → renderer → SVG →
   `validate_maps`; o CI → build-skills → mirror): PRIMA di proporre fix,
   strumenta ogni confine — logga cosa entra/esce da ogni componente, esegui
   una volta, individua DOVE si rompe, POI investiga quel componente.
   *Esempio locale*: se `validate_maps` è rosso, prima chiedi: è il master
   cambiato, il parser, o l'SVG committato? Un `--list` sul master e un render
   in-memory rispondono senza toccare nulla.
5. **Traccia il flusso del dato all'indietro** fino all'origine del valore
   sbagliato: fixa alla SORGENTE, non al sintomo →
   `references/root-cause-tracing.md`.

### Fase 2 — Analisi del pattern
Trova un esempio funzionante simile nello stesso codebase (un altro validator,
un'altra mappa che rende bene), confronta OGNI differenza («questa non può
contare» è vietato), capisci le dipendenze (config, ambiente, ordine).

### Fase 3 — Ipotesi e test
UNA ipotesi esplicita («credo che X sia la causa perché Y»), il TEST PIÙ
PICCOLO possibile (una variabile alla volta), verifica prima di continuare.
Se fallisce: NUOVA ipotesi, non fix impilate. Se non capisci: dillo e
ricerca — non fingere.

### Fase 4 — Implementazione
1. **Caso di test che fallisce** PRIMA della fix (pytest in `scripts/tests/`
   se possibile, script one-off altrimenti).
2. **UNA fix**, alla causa radice — niente «già che ci sono», niente
   refactoring in bundle.
   Se la fix porta una libreria o uno strumento nuovo, prima di proporla
   dichiara il canale e la misura: unstable, testing con versione fissata e
   misura prima e dopo, stable dopo 14 giorni e 10 run su `main` con l'ok del
   DM ([ADR-0099](../../plans/adr/ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md)).
3. **Verifica completa** (`## Prima di consegnare`).
4. **Se la fix non funziona**: STOP. Conta i tentativi. <3 → torna alla
   Fase 1 coi dati nuovi. **≥3 → il problema è ARCHITETTURALE**: fermati e
   discuti col DM il pattern, non tentare la fix #4.

## Bandiere rosse (se ti sorprendi a pensarlo, torna alla Fase 1)
«Fix rapida ora, indago poi» · «provo a cambiare X e vediamo» · «più modifiche
insieme e poi i test» · «salto il test, verifico a mano» · «sarà probabilmente
X» · «non capisco bene ma potrebbe funzionare» · «ancora un tentativo» (dopo
2+) · ogni fix rivela un problema nuovo altrove.

## Razionalizzazioni comuni
| Scusa | Realtà |
|---|---|
| «È semplice, niente processo» | Anche i bug semplici hanno cause radice; il processo sui bug semplici è veloce. |
| «Emergenza, niente tempo» | Il metodo è PIÙ VELOCE del guess-and-check (fix al primo colpo ~95% vs ~40%). |
| «Provo questo, poi indago» | La prima fix detta il pattern: falla giusta. |
| «Test dopo, prima confermo la fix» | Le fix senza test non reggono. |
| «Più fix insieme risparmiano tempo» | Non isoli cosa ha funzionato; crei bug nuovi. |

## Formato d'uscita

La causa radice in una frase (Fase 3), il test che falliva (Fase 4.1), UNA fix
alla sorgente; dopo 3 tentativi, il pattern da discutere col DM (Fase 4.4).

## Prima di consegnare

- Il test passa e il problema è risolto? Restano verdi
  `validate_modules/maps/bestiario/skills`, `check_plans_discipline`, catalogo
  in sync (prima del commit)?
- Riga in `plans/CHANGELOG.md` se il file è strutturale (ADR-0009)? Nessun PNG
  locale committato?

## Cancelli deterministici

I controlli che non chiedono un giudizio, da far girare prima di consegnare.
Quello che qui non c'è resta giudizio di chi legge (registro delle norme).

- `python3 scripts/tools_manifest.py --check`: ogni strumento citato esiste ed è dichiarato.
- `python3 scripts/validate_docs.py`: rimandi e ADR.
