# ADR-0102 — Lo stile delle piante diventa un tema delle mappe, e i generatori delle città entrano nel repo

**Stato**: accettata il 2026-10-23
**Data**: 2026-10-23
**Decisione-fonte**: il DM, il 2026-10-23 («molto belle le mappe fatte con questo stile puoi provare a rifare tutte quelle dell arco 07 e delle arco 08 con questo sile dettaglio e coerenza»; sulla scheda «Come rifaccio le 18 mappe di ARC-07?» ha scelto «Stile e forma»; poi «controlla se lo strumento per le mappe è nel repo con guida documentazione ed integrazione in modo che possa essere usato dal repo in maniera uniforme»)

## Contesto

Le piante di Rethmar, Dauth e Channathgate (PR #269, #271, #272, #276) le ha
disegnate un generatore scritto apposta: quartieri di Voronoi rilassati, vie
che corrono sui bordi, lotti per bisezione, mura con le torri. Quel codice
stava solo nella cartella di lavoro di una sessione. Nel repo c'erano gli SVG,
ma nessuno poteva rifarli né controllare che fossero ancora quelli giusti.

Al DM lo stile è piaciuto e ha chiesto le mappe tattiche di ARC-07 e ARC-08
nello stesso stile. Le mappe tattiche però nascono da una griglia emoji
(ADR-0048) e passano da `render_map_svg.py`, che ha due temi (pergamena e
texture) e usa solo la libreria standard.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Un tema «pianta» del renderer, in un modulo suo, solo libreria standard; i generatori delle città in `scripts/piante/` con un comando che li rigenera e li controlla; shapely in requirements-dev** | stessa griglia, stessi simboli, stessa legenda per tutti i temi; la sera al tavolo non serve niente di nuovo; le piante si rifanno e la CI sa se sono cambiate | il renderer non può usare shapely, quindi la roccia frastagliata si fa a mano; una dipendenza di sviluppo in più |
| Disegnare le mappe tattiche con il generatore delle città (shapely) | contorni più ricchi | due strade per la stessa mappa; il master JSON non sarebbe più la fonte; il renderer del DM smetterebbe di essere stdlib |
| Lasciare i generatori fuori dal repo | niente dipendenze nuove | le piante canoniche non si possono rifare: un errore di legenda come quello della #276 si correggerebbe solo a mano nell'SVG |

## Decisione

1. **`--tema pianta`** di `render_map_svg.py` chiama `scripts/render_map_pianta.py`.
   Disegna la roccia con il tratteggio e i bordi frastagliati (al massimo 0,24
   quadretti, quindi le celle calpestabili non cambiano), il lastricato a corsi,
   i terreni naturali con la loro trama, i blocchi a conci. Sotto la mappa mette
   il pannello «Luoghi» (le `@mark`) e la legenda. Gli SVG vanno in
   `rendered-pianta/`, accanto a `rendered/`.
2. **Il tema pianta si adotta una cartella alla volta.** `validate_maps` vuole
   `rendered-pianta/` completo e allineato al master solo dove la cartella
   esiste. Così ARC-07 passa allo stile nuovo adesso e ARC-08 quando il suo
   thread ridisegna le mappe, senza che un thread tocchi i file di un altro.
   `render_map_svg.py --tutti-i-master --tema pianta` e `dm.py maps pianta`
   rifanno solo le cartelle che l'hanno adottato.
3. **I generatori delle città stanno in `scripts/piante/`**: il motore
   `organica.py`, i pezzi comuni in `comune.py` e un programma per città
   (`rethmar.py`, `dauth.py`, `channathgate.py`) con le taglie scelte dal DM.
   `scripts/genera_pianta_citta.py` li lancia e scrive la pianta nel suo posto
   canonico. Con `--check` controlla che la pianta committata sia identica byte
   per byte a quella che il programma produce. `dm.py maps citta` fa lo stesso,
   e con una scheda `*.watabou.json` resta l'URL di Watabou di prima.
4. **shapely entra in requirements-dev in canale testing** (ADR-0099), alla
   versione 2.2.0 fissata, con numpy e scipy che c'erano già (ADR-0084).
   Licenza BSD-3-Clause. In CI `genera_pianta_citta.py --tutte --check` gira
   come passo non bloccante; sale a stable con le regole di ADR-0099.
   requirements.txt non cambia. La misura: senza i generatori le tre piante
   non si potevano rifare; con loro si rifanno in circa 9 secondi.

## Conseguenze

- Le 18 mappe di ARC-07 hanno il gemello in `rendered-pianta/`. Hanno ancora la
  forma dei master di oggi, fatta di rettangoli. Il DM ha chiesto anche la
  forma: i JSON si ridisegnano a gruppi, controllando ogni stanza contro i
  moduli, e il gemello si rigenera con loro.
- ARC-08 riceve lo strumento dal thread di ARC-08, che decide quando adottarlo.
- Una versione nuova di GEOS può spostare un arrotondamento e far fallire il
  confronto delle piante: si rigenera la pianta e si guarda la differenza prima
  di committarla.

**Da rivedere se**: il DM preferisce la pergamena dopo aver visto le mappe
ridisegnate; il frastagliamento della roccia nasconde un bordo che conta al
tavolo; il confronto byte per byte delle piante fallisce per GEOS più di una
volta per trimestre (allora il controllo passa a una misura con tolleranza).
