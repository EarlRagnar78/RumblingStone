# F4: cosa cambia sulle schede PF1e (da leggere prima del merge)

> 2026-11-08 · ADR-0112, F4 · PIANO-MOTORE-AGNOSTICO-D20 · scelte delle card F4 1-3 decise dal DM il 2026-11-08 (in fondo).

## In breve

Prima di F4 gli strumenti contavano le schede del Drappo e del Giardino PF1e con le regole 3.5, e solo se qualcuno passava il file a mano. Adesso le schede PF1e entrano da sole nel rapporto `conformita_statblocchi --master`, e si contano con le regole PF1e scritte nel plugin (`sistemi/pf1e/dati/conformita.toml`).

Sulle 14 schede, rispetto alla lettura 3.5 di prima:

- **2 scarti spariscono.** Sfregio e lo Sgherro di Hamid tornano col primo dado di classe al massimo e i dadi dopo a mezza in su.
- **1 scarto nuovo.** L'Asservito armato ha i pf contati con la mezza in giù, quindi con la regola PF1e scelta è 1 punto sotto.
- **3 conti non si fanno più sulle schede PF1e, e il rapporto lo scrive.** Sono lotta, scurovisione e *corrompere l'acqua*: la loro regola è riscontrata solo sull'SRD 3.5. Oggi nessuna delle 14 schede ne aveva uno scarto.
- **5 schede restano non lette, come prima.** Le quattro comparse del Drappo §4 non hanno il `pf-dado`, e Skum somma due dadi (`2d10+8d10+60`).

Sulle schede 3.5 non cambia niente: `impronta_creature --confronta` è identica, il banco `impronte.py --confronta` dà 12/12, e le uscite JSON di `conformita_statblocchi`, `derive_statblocks`, `genera_attributi` e `validate_bestiario` sono byte per byte quelle di prima.

## Le 14 schede

Le colonne «max + giù» e «max + su» sono il primo dado al massimo e gli altri a media, col totale arrotondato in giù o in su.

| Modulo | Scheda | Tipo | pf scritti | Dadi | Media | Max + giù (3.5) | Max + su (PF1e scelta) | Prima | Dopo |
|---|---|---|---|---|---|---|---|---|---|
| Drappo | §1 Vidalia Roncetti | esperta 6 | 33 | 6d8+6 | **33** | 36 | 37 | torna | torna |
| Drappo | §3 Sfregio | ladro 4 | 26 | 4d8+4 | 22 | 25 | **26** | ✗ 26 ≠ 22 | torna |
| Drappo | 4.1 Tintore mezzo ubriaco | comparsa | 6 | — | | | | non letta | non letta |
| Drappo | 4.2 Bravaccio del canale | comparsa | 16 | — | | | | non letta | non letta |
| Drappo | 4.3 Miliziano della Torre | comparsa | 20 | — | | | | non letta | non letta |
| Drappo | 4.4 Cerbo, guardiano | comparsa | 9 | — | | | | non letta | non letta |
| Drappo | §5 I cavalli | animale | 15 | 2d8+6 | **15** | | | torna | torna |
| Giardino | Karkator | aberrazione | 248 | 16d8+176 | **248** | | | torna | torna |
| Giardino | Ragno delle Catene | bestia magica | 147 | 14d10+70 | **147** | | | torna | torna |
| Giardino | Mastro Tariq | chierico 13 | 88 | 13d8+26 | 84 | **88** | **88** | torna | torna |
| Giardino | Skum guerriero 8 | due dadi | 115 | 2d10+8d10+60 | | | | non letta | non letta |
| Giardino | Chuul avanzato | aberrazione | 105 | 10d8+60 | **105** | | | torna | torna |
| Giardino | Sgherro di Hamid | guerriero 6 | 50 | 6d10+12 | 45 | 49 | **50** | ✗ 50 ≠ 45 | torna |
| Giardino | Asservito armato | guerriero 4 | 34 → **35** | 4d10+8 | 30 | 34 | **35** | torna | torna dopo la correzione (34 era ✗) |

## Le scelte del DM (2026-11-08, card F4 1-3)

1. **Le schede PF1e si controllano, e la CI blocca.** `conformita_statblocchi.py --cancello-moduli` è uno step di CI: ogni conto delle schede dei moduli di un altro sistema deve tornare con le regole di quel sistema.
2. **Punti ferita PF1e: massimo al primo dado di classe, mezze in su dopo.** L'Asservito armato del Giardino passa da 34 a 35 pf; Sfregio e lo Sgherro restano come sono.
3. **Un conto senza regola PF1e lo dice e si salta.** Lotta (manca il conto di BMC e DMC), scurovisione (manca la lista dei tipi PF1e) e *corrompere l'acqua* (manca il riscontro sul PRD) restano fuori finché la regola non entra nel plugin.

Dopo le scelte il rapporto dà 0 conti che non tornano su 36 file.

## Come si rifà

```
python3 scripts/conformita_statblocchi.py --master
python3 scripts/conformita_statblocchi.py --cancello-moduli
python3 scripts/impronta_creature.py --confronta
python3 plans/esperimenti/sistemi-plugin-2026-11-07/impronte.py --confronta
python3 plans/esperimenti/motore-agnostico-2026-11-08/censimento_formule.py --check
```
