# ADR-0048 — La legenda funzionale è la fonte unica: la funzione di gioco di un simbolo è un dato, non prosa né un `set` cablato

**Stato**: accettata — decisione DM del 2026-07-26, **rinumerata e non ancora attuata**

> ⚠️ **Perché il numero è cambiato, e perché arriva con un mese e mezzo di
> ritardo.** Questa decisione nacque come ADR-0014 nella PR #72 (26 luglio
> 2026), rimasta aperta come bozza. Il 2026-09-04 la PR #128 ne ha recuperate
> **due** — ADR-0039 (era 0016) e ADR-0040 (era 0017) — e ha dichiarato il
> motivo per cui la #72 non era più mergiabile: *«i numeri ADR 0014-0018 della
> #72 erano stati occupati da altre decisioni nel frattempo»*. Questa era la
> terza, ed è rimasta indietro. L'ha trovata il lotto 4b, non guardando gli ADR
> ma **un link rotto**: `docs/guides/LEGENDA-FUNZIONALE-SPEC.md` citava un file
> che non esiste in nessun posto.

**Data**: 2026-07-26 (corpo) · 2026-09-10 (recupero e riverifica)
**Decisione-fonte**: lotto A1 di `PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA`; misura in `docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md` §2.1. Specifica normativa: [`LEGENDA-FUNZIONALE-SPEC`](../../docs/guides/LEGENDA-FUNZIONALE-SPEC.md).
**Attuazione**: lotto **1.1** di [`PIANO-VENDIBILITA`](../PIANO-VENDIBILITA.md) — ⬜ **da fare**.

## Contesto

Un simbolo della griglia porta due informazioni distinte: **come si disegna**
(pattern, colore, prop) e **cosa fa in gioco** (blocca il movimento? la vista?
dà copertura? a che quota sta? è nominabile al tavolo?).

Solo la prima è un dato. `SYMBOLS` in `scripts/render_map_svg.py` descrive il
rendering; la funzione di gioco vive in due posti che nessuno script può
interrogare: **in prosa dentro l'etichetta** (`"🪨": {"it": "Rocce/macerie
(copertura +4 CA, terreno difficile)"}`) e **cablata in `set` dentro i
consumatori** (`WALL_SYMS`, `DOOR_SYMS`, `LIGHT_SYMS` in `export_uvtt.py`,
`HAZARD_SYMS` in `import_ultraclear.py`).

Due fonti di verità che possono divergere in silenzio — e avevano già diverso in
entrambe le direzioni. La conseguenza misurata a luglio: la parete rocciosa di
*Dirupo Mortale* (ARC-08) occludeva nell'SVG stampato e **non** bloccava la
linea di vista in Foundry. La stessa mappa, due regole a seconda del supporto.

## Riverifica contro il codice del 2026-09-10

Recuperata da `refs/pull/72/head` e riverificata riga per riga, come si fece per
ADR-0039 e ADR-0040. **La diagnosi regge**, e il modo in cui è invecchiata è la
prova migliore che aveva ragione.

| Cosa diceva a luglio | Oggi |
|---|---|
| `scripts/legend.yaml` fonte unica | **non esiste**. Mai creato |
| `WALL_SYMS` cablato nell'export | ancora cablato — `export_uvtt.py:63`, e nel frattempo **cresciuto** da 6 a 8 simboli |
| `HEAVY_PATS` seconda tabella nel renderer | ancora seconda tabella — `render_map_svg.py:169` |
| `HAZARD_SYMS` cablato nell'import | ancora cablato — `import_ultraclear.py:72` |
| `legenda-universale.md` copia manuale | ancora copia manuale |
| le 4 divergenze (`⛰` `🏛` `🗼` `🗿`) da risolvere | **due sono state chiuse, una per volta, nel consumatore** |

⚠️ **La riga che conta è l'ultima.** `⛰` è entrato in `WALL_SYMS` con
[ADR-0043](ADR-0043-le-montagne-sono-muri-e-nessun-master-esce-dal-controllo.md)
e `⛺` con [ADR-0042](ADR-0042-tre-glifi-per-tre-cose.md): due decisioni
separate, ognuna col suo ADR e i suoi test, per rattoppare **due sintomi della
stessa causa**. Ognuna era corretta; nessuna poteva togliere la causa, perché la
fonte unica non c'era. È il costo di questa decisione rimasta in un cassetto,
pagato due volte in due mesi.

Di conseguenza il §3 originale — *«le quattro divergenze si risolvono con una
decisione dichiarata»* — **non si recupera alla lettera**: rivendicherebbe come
propria una classificazione che ADR-0042 e ADR-0043 hanno già applicato. Restano
aperte `🏛` `🗼` `🗿`.

## Decisione

**Promuovere la funzione di gioco a dato di prima classe in una fonte unica,
`scripts/legend.yaml`, da cui tutto il resto è derivato.**

1. **Struttura.** Ogni simbolo dichiara `label`, `render{}` (mode, pat, prop,
   fill) e `function{}`:

   ```yaml
   symbols:
     "🪨":
       label: "Rocce / macerie"
       render:   {mode: icon, prop: pr_rocks, fill: "#ced4da"}
       function:
         blocks_movement: false
         blocks_sight: false
         cover: half              # none | half | three_quarters | total
         obscurement: none
         move_cost: 2
         elevation_m: 0
         destructible: true
         nameable: true           # → può fare da landmark (M8, Lynch)
   ```

2. **Derivazione, non duplicazione.** `render_map_svg.SYMBOLS` si genera dal
   YAML (o da un `legend.json` committato e verificato in CI, come già si fa per
   `docs/tools/`); `export_uvtt.py` deriva muri, porte e luci da `function` ed
   **elimina** i propri `set`, e così `import_ultraclear.HAZARD_SYMS`;
   `skills/rumblingstone-mapmaking/references/legenda-universale.md` si genera,
   con gate di sincronizzazione; i tool nuovi leggono la legenda, mai un set
   proprio.

3. **Le divergenze residue** (`🏛` `🗼` `🗿`) si risolvono con una decisione
   dichiarata, non con una scelta implicita del codice: è una questione di
   regole 3.5, e va al DM.

4. **Nessuna regressione visiva.** Il refactor è verde solo se gli SVG legacy
   restano **byte-identici** (`validate_maps.py`) e il round-trip UVTT passa.

5. **Nessun numero di gioco nel YAML.** `+4 CA`, `20%`, `×2` vivono nei profili
   di [ADR-0039](ADR-0039-profili-regole-multisistema.md). `legend.yaml` è neutro
   rispetto al sistema, ed è la ragione per cui il prodotto può supportarne tre.

## Conseguenze

**Cosa diventa più facile**

- una sola verità su cosa sia un muro: SVG, UVTT ed editor non possono più
  divergere in silenzio, e nessun `⛰` futuro costa un ADR a sé;
- le metriche di level design diventano calcolabili senza set sparsi, e il
  linter dipende dal dominio invece che da un exporter;
- `elevation_m` trova dove vivere; `nameable` rende misurabile se i giocatori
  possano dire «mi sposto dietro il carro bruciato» invece di «vado in K12»;
- `legenda-universale.md` smette di essere una copia manuale.

**Cosa diventa più difficile / a cosa si rinuncia**

- una dipendenza in più nel percorso di rendering: parser YAML stdlib o
  `legend.json` committato — **niente pyyaml obbligatorio**, coerentemente con
  `stdlib_only` del manifest e con [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md);
- aggiungere un simbolo richiede di dichiararne la funzione: attrito voluto;
- il refactor tocca quattro script maturi e ben testati. Il rischio è reale, e
  la mitigazione è il gate di byte-identità, non la prudenza.

**Il limite di questa decisione, dichiarato**

🔴 **È una decisione accettata senza un cancello che la faccia rispettare.**
Finché `legend.yaml` non esiste, niente impedisce a un quinto consumatore di
nascere col suo `set` privato — ed è esattamente ciò che è successo due volte
mentre la decisione stava in una PR chiusa. L'unico presidio è il lotto 1.1 di
`PIANO-VENDIBILITA`, che è ⬜; il suo criterio d'accettazione
(`legend/single-source` fallisce se un consumatore usa un set proprio) è il
cancello mancante.

**Cosa va rivisitato e quando**

- se l'editor visuale (lotti E2-E10 di `PIANO-EDITOR-VISUALE-MAPPE-TATTICHE`,
  che ha pianificato una **terza** casa per la stessa legenda) richiede campi non
  previsti qui, si estende `function` — mai si crea una seconda fonte;
- la scelta fra YAML sorgente + JSON derivato committato, o solo YAML letto a
  runtime, si decide in fase di attuazione sulla base del vincolo `stdlib_only`.
