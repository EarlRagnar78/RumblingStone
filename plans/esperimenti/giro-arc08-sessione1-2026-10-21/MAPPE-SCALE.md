# Mappe di ARC-08: scale e misure (2026-10-21)

Origine: l'audit delle scale fatto sulle mappe di ARC-07
(AUDIT-SCALE-MAPPE, nel giro mappe-campo del 2026-10-21, che sta su `main`),
applicato a `08_La Battaglia Di Hammerfist/Mappe/`. Decisioni del DM:
`plans/esperimenti/a3-arc08/ZONE-HAMMERFIST-372-1372.md` §4.

La geometria di riferimento ora è una sola, ed è la tabella **MISURE DI
RIFERIMENTO DELLA FORTEZZA** in testa a `Hammerfist-L2-REVISED-Ultra-Clear.md`.
In breve: fronte sud di 102 m da torre a torre, cortili larghi 90 m, cinta
spessa 6 m (merlatura e camminamento da 4,5 m) e alta 12 m, torri di 9 × 9 m
alte 20 m, bastioni sud G1 e G2 di 15 × 12 m ai lati del cancello (40 nani e
2 baliste ciascuno), bastioni nord B1 e B2 di 12 × 12 m, cancello largo 6 m e
alto 8 m con 200 pf, fossato di 6 m al piede del muro, ponte levatoio di
6 × 7,5 m che lo scavalca, Porta Interna larga 6 m nel muro del 372, statua
del Re Antenato con il tunnel dietro, atrio della cittadella nella roccia.

Le tre griglie tattiche della fortezza ora nascono da un contratto JSON in
`Mappe/fortezza-json/` (prima ARC-08 non ne aveva). Le griglie si
rigenerano con `scripts/compile_map_json.py` e si incollano nel master; i
generatori non sono nel repo, il JSON sì.

## Mappa per mappa

| Mappa | Prima | Adesso |
|---|---|---|
| **2A** (L2, 120 × 80, 1,5 m) | fronte di 127,5 m fra le torri; mura spesse 1,5 m; bastioni di 6 × 4,5 m (27 m²) con 40 nani e 2 baliste; porta interna 9 m nella griglia e 6 m nella tabella; ponte su terra asciutta perché il fossato partiva dalla riga 76; tunnel a est; nessuna riga DIMENSIONI | griglia rigenerata da `HF-2A-fortezza.json` sulla tabella MISURE; DIMENSIONI nella recinzione; VISTA 2, posizioni, distanze, punti deboli, ambiente ed evoluzione riscritti sulle nuove coordinate (Re BH34, Borin BH54, Dara AD69, cancello BG-BJ73, Porta Interna BG-BJ41-42, statua BA-BB22-23, tunnel BA20) |
| **2B-CORRETTA** (L2, 40 × 26, 1,5 m) | camminamento largo 4,5 m sulla mappa e 1,5 m sulla 2A; nord indicato come «esterno delle mura»; Fauci su un solo quadretto; tunnel W15 sul bastione | è il tratto G1-cancello-G2 della 2A (colonne AO-CB, righe 53-78); il drago arriva da sud, dal fossato; Fauci Enorme su 3 × 3 quadretti; nessun tunnel sul bastione, l'evacuazione scende dalla scala di G1 e attraversa il cortile esterno; Dara a ~45 m invece di ~70 |
| **MAPPA 1** (L2, 60 × 108, 3 m) | fronte di 156 m (colonne E-BD); scala detta solo nel testo, l'SVG stampava 1,5 m | fronte di 102 m (colonne N-AU) con torri, G1, G2 e fossato al piede del muro; DIMENSIONI a 3 m nella recinzione; Cancello −40 / −80 sui 200 pf nel testo delle fasi |
| **MAPPA 2 e MAPPA 4** (L2, tabelle) | coordinate numeriche della vecchia 2A; G1/G2 con 25 uomini; breccia di 8 m a col 85-90 | coordinate a lettere della nuova 2A; G1/G2 con 40; breccia di 7,5 m a CM-CP righe 59-63; cancello a 120 e 40 pf |
| **H3-1** (L3, prima 40 × 40, ora 72 × 36, 1,5 m) | cortile senza misura riconoscibile; «LONTANO da Hammerfist» nel testo | è il cortile interno della 2A (colonne Y-CR, righe 18-53) con la Porta Interna sfondata e due brecce nella cinta; statua AC-AD05-06, tunnel AC03 che scende al Cuore, porta dell'atrio AI-AL03; rigenerata da `HF-H3-1-cortile-sfondato.json` |
| **MAPPA 4** (L3, 60 × 68, 3 m) | fronte di 156 m e nessun fossato | stesso fronte della MAPPA 1 (colonne N-AU), fossato con il ponte rimesso dopo la riconquista |
| **1A-1** (L1, 20 × 100, 1,5 m) | «strozzatura ~9 m» larga 21 m | righe 10-14 chiuse dalla roccia fino a 9 m (colonne H-M); rotta furtiva corretta |
| **1A-3** (L1, 40 × 50, 6 m) | scala solo nel testo, SVG a 1,5 m | DIMENSIONI a 6 m nella recinzione |
| **ARC08-01**, guida agli scontri, atlante | «TUNNEL EST → CUORE»; altare a 25 m; 2B con nord e sud scambiati; cancello di 10 m e 120 pf, ponte di 15 m, camminamento di 3 m nell'atlante | tunnel nord dietro la statua; altare a +3 m; 2B con il sud in alto; misure dell'atlante sulla tabella; la nota sul ritorno dal Cuore dice che il tunnel scende al Cuore |

Il master `ARC08-DEF-1-OMBRA-SULLA-MONTAGNA.md` non cambia: cita le quote
della VISTA 3 (12, 15 e 20 m), il cortile interno di 90 × 30 m alle righe
21-40, le rocce e le righe di 1A-1 e la scala di 1A-3, e sono tutti ancora
veri.

## Controlli

`validate_maps` verde (54 SVG, tema texture compreso). `collaudo_mappe`: L1 e
L2 senza errori; L3 ha 7 errori di posa delle porte in 3Y e 3Z, che c'erano
già e non toccano la fortezza. I test delle mappe passano (100). `gate_locale.py --rapido`: 50 passi, 0 rossi, 2 avvisi (manca typst in locale).

## Da chiedere al DM

- `ARC08-02` scrive «Sfondare il Cancello Principale (800 PF)»; il canone di
  oggi è 200 pf. Non l'ho toccato.
- Le truppe per postazione non tornano a 300 (le torri hanno 10 balestrieri
  nella tabella e 20 nella vecchia MAPPA 2; i bastioni sud ora 40).
- La 2B mette il Re sopra il cancello il Giorno 3, mentre la 2A lo tiene nel
  cortile interno: serve una riga che dica perché sale sui bastioni.
- 1A-3 ha una tenda sola e non un accampamento disegnato; non l'ho
  ridisegnato.
