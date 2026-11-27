# ADR-0128 — Ogni scheda dichiara taglia, spazio e portata

**Stato**: proposta (2026-11-10)
**Data**: 2026-11-10
**Decisione-fonte**: il DM (Jfs), 2026-11-10, nel thread dello standard del volume: «tutte le schede non hanno né taglia né portata, ed è necessario per sapere quanti quadretti occupano e quanto minacciano»; da controllare contro i migliori AP, correggere in tutti i booklet, far leggere a playtester, DM e developer, e vedere se entra come standard.
**Rapporti**: emenda [ADR-0105](ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md) (il riquadro unico) e la riga dell'incontro di [ADR-0122](ADR-0122-il-volume-segue-lo-schema-degli-adventure-path.md); i dati stanno nel plugin della famiglia d20 ([ADR-0111](ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md)).

## Contesto

Misura sul repo prima della modifica: su 205 schede (blocchi `statblocco` dei
master), 59 non dicevano la taglia in nessun campo, e solo 31 scrivevano la
portata da qualche parte nella prosa. Il riquadro stampato non aveva una riga
per l'ingombro. Al tavolo il DM non sapeva quanti quadretti occupa una
creatura né quali minaccia.

I riferimenti (gli stessi PDF di ADR-0122, fuori dal repo):

| | schede | taglia nella riga del tipo | riga «Space/Reach» |
|---|---|---|---|
| *Red Hand of Doom*, schede della WE | 99 | 98 | 16 |
| *Burnt Offerings* | 56 | sempre, dove si legge | 9 |

Lo standard di fatto è quindi: **taglia sempre**; spazio e portata **solo
quando non sono 1,5 m / 1,5 m** (è anche la regola scritta del formato PF1e).

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Tre campi nel blocco, riga sempre stampata, coi quadretti** (scelta) | il DM lo chiede per ogni scheda; i quadretti evitano il conto al tavolo; un cancello può controllarli | diverge dagli AP, che tacciono il caso standard: una riga in più su ogni scheda Media |
| Come gli AP: riga solo se non standard | lo standard di fatto; schede più corte | una riga assente non distingue «standard» da «dimenticata», ed è il difetto che il DM ha segnalato |
| Ricavare tutto dalla taglia in stampa, senza campi | niente dati nuovi | la tabella non sa se una creatura Grande è alta o lunga, né le armi con portata |
| Lasciare la portata nella prosa di «Attacco» | nessuna migrazione | 31 schede su 205, in forme diverse, non controllabili |

## Decisione

1. Il blocco `statblocco` ha tre campi nuovi: `taglia` (nome italiano della
   tabella), `spazio` e `portata` in metri. Le eccezioni stanno fra parentesi
   dopo la portata di base: `3 m (4,5 m con il morso)`,
   `1,5 m (3 m con la lancia lunga, e allora non i quadretti adiacenti)`.
2. La tabella è quella dell'SRD 3.5, uguale nel PRD di PF1e:
   `sistemi/d20/dati/taglie.toml`, capacità `statblocco.taglie`, ereditata da
   `dnd35` e `pf1e`.
3. Il riquadro stampa sotto il tipo «**Taglia** Grande · **Spazio** 3 m (2×2
   quadretti) · **Portata** 3 m (2 quadretti)», in Typst, HTML e Homebrewery
   (`dmcore.statblock.ingombro`). Una scheda di gruppo, «Guardia (4)», dice
   «ciascuno». La riga dell'incontro («scheda a pagina N») porta la stessa
   riga, e dal giro anche iniziativa, velocità, TS e attacchi.
4. **Cancello**: `scripts/tests/test_ingombro_schede.py`, cricchetto a zero.
   Ferma la CI una scheda senza uno dei tre campi, con uno spazio che non è
   quello della taglia, con una portata di base che non è né quella «alta» né
   quella «lunga», o con una taglia diversa da quella scritta nel tipo.

## Misura (2026-11-10)

- 205 schede su 205 con i tre campi; 20 booklet ricompilati, 0 schede spezzate,
  0 rimandi di pagina sbagliati (`misura_stampa --tutti --check`).
- Giro di tre letture, rapporti in
  `plans/esperimenti/taglia-portata-2026-11-10/`:
  - **developer**: 198 schede giuste su 205 alla prima compilazione; 4
    corrette (Karkator PF1e a 6 m, due lance da cavaliere, la frusta di
    Lirien); 36 delle 59 non Medie confermate in rete sull'SRD, le altre a
    memoria.
  - **DM** sul booklet della serata: i rimandi di pagina sono giusti; corretti
    il drago sbagliato nel duello, la riga dell'incontro senza attacchi e TS,
    le sigle «Appendice A.2» senza corrispondenza nel volume, la scheda del
    Vecchio che rimandava all'Adulto per velocità e sensi.
  - **playtester**: i tre campi sono giusti su tutte le non Medie giocate; i
    difetti che restano sono di contenuto (tattiche che la griglia non
    permette, misure assenti sulle tavole), elencati nel rapporto e **non
    corretti qui**.

## Conseguenze

- Ogni scheda Media ha una riga in più che gli AP non stampano.
- Il cancello non sa se la scelta fra portata alta e lunga è giusta per quella
  creatura: lo dice solo una lettura (il developer ne ha trovata una su 59).
- Non coperti, dal rapporto del playtester: manovrabilità di volo dove
  `velocita` non la scrive, portata verticale, cambi di taglia (*giusto
  potere*), cavalieri in sella, sciami, impronta delle creature sulle mappe.
- L'impronta delle creature è rigenerata: cambia solo `letture/senza_note`.

**Da rivedere se**: al tavolo la riga sulle schede Medie risulta rumore (allora
si torna alla regola degli AP, riga solo se non standard), o se il cancello
lascia passare un secondo errore alta/lunga (allora la scelta va scritta nei
dati del plugin, creatura per creatura).
