# Correzioni dei nomi nei booklet: ARC-07 e ARC-08, prima e dopo (2026-11-07)

Fase 5 del lotto di [ADR-0110](../../adr/ADR-0110-i-termini-ufficiali-hanno-una-tabella-e-un-cancello.md).
Si corregge solo un nome che ha una forma ufficiale certa nella tabella 3.5; gli oggetti unici della
campagna e le forme incerte restano come sono e sono elencati qui sotto.

## Cosa è cambiato

| Nel testo | Diventa | Fonte del nome | Dove |
|---|---|---|---|
| Soffio Aderente | Soffio Impregnante (Clinging Breath) | 5° Clone, Draconomicon | ARC-07 DEF-4, «Chi c'è stanotte», scheda di Skullcrusher |
| Guanti della Forza dell'Orco | Guanti del Potere Orchesco (Gauntlets of Ogre Power) | tesoro del GDM | ARC-07 DEF-3, ARC-08 |
| Incutere Paura | Incuti Paura (Cause Fear) | doppia fonte + Editori Folli | ARC-08 |
| Rimuovere Paura | Rimuovi Paura (Remove Fear) | doppia fonte + Editori Folli | ARC-08 |
| Resistenza all'Energia (incantesimo) | Resistere all'Energia (Resist Energy) | doppia fonte + Editori Folli | ARC-08 |
| Scudo Leggero in Acciaio | Scudo Leggero di Acciaio | Editori Folli (tabella SRD) | ARC-08 |

I volumi `.hb.md` e `.html` di ARC-07 sono rigenerati dai manifest (`build_booklet_html.py`), non
toccati a mano. L'impronta delle creature resta identica: cambiano solo nomi, nessun numero.

## Misura (`lessico_regole.py controlla --tutto --volumi --campi`)

| Termini sconosciuti | Prima | Dopo |
|---|---|---|
| talenti, repo | 137 | 133 (cricchetto della CI a 133) |
| incantesimi, repo | 26 | 22 |
| oggetti magici, repo | 45 | 41 |
| ARC-07 + ARC-08, tutti i tipi | 64 | 52 |

## Cosa resta, e perché

- **Oggetti unici della campagna** (Corona dei Re Hammerfist, Martello da Guerra degli Antenati,
  Scudo Pesante Runico, Armatura Completa Ancestrale…): non sono nomi del manuale, il controllo li
  segnala perché non hanno una marca. Vanno marcati come oggetti della campagna, non rinominati.
- **Forme dell'equipaggiamento** (Armatura di Cuoio Borchiato, Armatura a Bande, Kit da Scasso
  Perfetto): la tabella ha «Cuoio borchiato», «Corazza di bande» da Editori Folli e Mephit, ma la
  forma del Manuale del Giocatore italiano non è riscontrata. Non si cambiano senza la fonte.
- **Campi letti male**: «Tiro Rapido e Tiro Multiplo» sono due talenti giusti uniti da «e»;
  «Attacco Furtivo» e «Sapere bardico» sono privilegi di classe finiti nel campo delle abilità.
- `epurare` (ARC-07 DEF-4) e «Incidere Rune» non hanno un riscontro: restano da decidere.

## Oggetti della campagna (2026-11-07, scelta del DM sulla card)

Gli oggetti unici adesso stanno in [campaign/OGGETTI-DELLA-CAMPAGNA.md](../../../campaign/OGGETTI-DELLA-CAMPAGNA.md), ognuno
con la base SRD, il portatore e la scheda. Il controllo li legge con l'esito `campagna`. Nei campi
oggetto del repo (volumi compresi) gli sconosciuti scendono da 41 a 24, e 17 letture diventano
`campagna`. Due punti restano aperti nell'elenco, marcati INFERRED: la regola di *Annientatore* e
il legame fra il Martello degli Avi e quello degli Antenati.
