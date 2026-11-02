# Arco 08: applicazione delle decisioni D9-D20 (2026-10-19)

Ramo `claude/project-thread-e860p0`. Nessun commit, nessun push: è tutto nel working tree. Le sigle dei file sono quelle del mandato (A guida, B Guida agli Scontri, C esiti, D ponte, E Cerimonia, F mappe L3, G schede). Il tag nuovo è `[CANONE — DM 2026-10-19, Dn]`, con il numero del piano.

## Che cosa è cambiato, decisione per decisione

**D9 · Fauci nella versione F.** In A e in B il «ROUND 5: LA FUGA DEL DRAGO» non c'è più. Al suo posto c'è «ROUND 18-23: LA PICCHIATA E IL DUELLO», con la causa dello schianto, il punto in cui atterra, un box nuovo e la reazione ai PG in volo; in B resta al round 5 una riga, «FAUCI RESTA IN ARIA». In testa al 4A di A e di B c'è la linea del tempo unica, la stessa di F e dell'Atlante: round 1-3 sui bastioni, 4-5 la discesa, 6 l'urto, 6-8 le strafing, 11-17 il logoramento, 18-20 la picchiata, 21-23 il duello. La carica passa ai round 4-10 e l'impatto al round 6. I pf di partenza sono 337 meno il carry-over, oppure 232 se il P5 non è stato giocato, in A, B, C §4.1 e §5.5, F e Atlante. Le tattiche di Fauci in A hanno i round nuovi. In F sono riscritte le FASI, la COMPRENSIONE, la zona ⚡ e lo stato «C» dell'evoluzione, e lo stato B va ai round 4-6. Nell'Atlante «Crash landing 60 m davanti» diventa la picchiata nella zona ⚡. Il ramo «ucciso / fuggito» di C resta, come esito del duello.

**D10 · Tre schede nuove in `Bestiario/mostri/`.**
- `bugbear-assassino-ladro5-assassino2-cr9.md`: Ladro 5 / Assassino 2, GS 9, CA 20, 58 pf, attacco furtivo +4d6, attacco mortale CD 16.
- `gufo-gigante-celestiale-cr6.md`: 8 DV, modello celestiale, GS 6, CA 16, 52 pf.
- `orog-guardia-nera-guerriero6-cr7.md`: Guerriero 6, GS 7, CA 19, 63 pf, ascia +13/+8 (1d12+10). Ha `[Private source — Monsters of Faerûn / Races of Faerûn]` e `⚠ Non SRD`.

Il catalogo è rigenerato. In A e in B le schede prendono il posto di «decisione aperta», nella regia, nelle capacità dei bugbear e nei pf dei gufi. G §5 rimanda alla scheda dell'orog. Ho corretto anche il «GS 7» e il «+5d6» dei bugbear in A e nell'Atlante (per l'SRD fanno GS 9 e +4d6). La fixture `scripts/tests/fixtures/impronta-creature.json` è rigenerata: cambiano solo le tre voci nuove e i tre conteggi, e c'è il precedente del commit 2912e07e.

**D11 · Grimjaw al round 12, col corno al round 11.** Allineati A (3B, ondate, Apparizione, round 11-15), B, D §2, F e l'Atlante. In F, MAPPA 5: `@mark 17` e una rotta nera nuova (`@path`, AG2→AG18), la tabella delle ondate e lo stato F. In F, MAPPA 4: `@mark 15` su AJ44, valido solo se nel 3B Grimjaw ha suonato la ritirata. Gli SVG di MAPPA 4 e MAPPA 5 sono rigenerati, in tutti e due i temi.

**D12 · Re Thorek e Dana.** La regola è nelle Prove Mediche di A: Guarigione CD 25 a ogni round, il Re muore al terzo fallimento, e la cura segue l'SRD. È riportata in B, C §2, D, F (`@mark 7` e la riga del Re, senza più `[INFERRED]`) e nell'Atlante. Per Dana vince il canone del 2026-10-18: 20 pf e un solo *Muro di Pietra*. Sono tolti da A e da B «Heal round 1 / Consacration round 2», e da A, B ed F «metà incantesimi».

**D13 · Dalla caverna ai bastioni.** La regia di A non ha più `[INFERRED]`. In più c'è la tabella «Chi è ancora in campo all'inizio della Sessione 4», con la fonte di ogni numero. Nell'Atlante (4X) sono corrette le righe su Grimjaw e su Re Thorek.

**D14 · La tempesta.** È di Orion, druido di 14° (verificato in A), con *controllare tempo*. I fulmini vengono dalla Cantata di Tempestas e da *chiamare fulmini* di Orion. Gli arcieri alleati hanno una deroga dichiarata: l'occhio della tempesta sopra i bastioni. Allineati A (Presagi, Condizioni, FASE 3 senza la «Sinfonia» `[INFERRED]`), B, F (VISTA ALTITUDINI con LI 14 al posto di LI 20, Orion, AMBIENTE con la riga dell'occhio) e l'Atlante.

**D15 · Il cavaliere.** In C c'è il nuovo §4.2: tre cose che sa e una tabella «Se lo divinano», con lo *scrutare* di Hella, la *comunione* della Corona e l'interrogatorio. A, B e G rimandano lì.

**D16 · Lythiel.** In A e in B, nel 4A (round 1-2), c'è un paragrafo per il DM e un box. E §3.2 dice che cavalca coi gufi. In `09_…/Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ARMATE-SYNC.md` ho tolto il «compare solo alla Cerimonia».

**D17 · Il conto dei caduti.** In C §1 ed E §1.1: 210 = 118 + 92, e i 9 si nominano senza contarli. I superstiti si contano dal Registro PFU, in C §1 e §2.

**D18 · La serata.** Tolto l'`[INFERRED]` dalla regia di A e di B.

**D19 · EL e PE.** Sono tolti dal 3B e dal 4A di A e di B l'EL 17 e l'EL 20, e la nota EL dalle appendici di A e di B. Al loro posto vanno i PE dell'Appendice C e le righe di scala per 3 e 5 PG, più la riga «Stasera: 4 PG di 13°».

**D20 · L'Atto 2 della Cerimonia.** Il segno «in attesa» nel file non c'era. Il box di E §3 resta con due figure non coordinate; ho tolto il grassetto e la parentesi, e il rimando alle note è fuori dal box.

## Le scelte che ho dedotto

- **La causa dello schianto.** Fauci scende per scelta: la sua scheda (G §1) dice che atterra sotto i 100 pf o per finire Thorik, e l'Odio della stirpe gli dà la ragione. È una picchiata, con Attacco in Volo, ed è legale in 3.5.
- **Dove atterra.** Nella zona ⚡ AB30-AG32, alle spalle della punta, a circa 30 m da Thorik, e non più «60 m davanti».
- **Le due letture della regola di Re Thorek** (`[INFERRED]`). Un round senza prova conta come fallito. Il conto parte dal round 1 coi pregen, oppure dal round 11 se il flashback non è stato giocato.
- **Dana.** 20 pf e un solo *Muro di Pietra* per tutto il 3B. Tiene il Re in vita con le mani, ed è lei a tirare la prova.
- **Le unità della Sessione 4, circa 400.** Hobgoblin ~100 e fanteria orchesca ~200 vengono dall'Atlante (4X). Giganti 8 ed ettin 2 vengono dal Registro e dalle strafing, e sono più Gorthak. I 4 capitani sui worg vengono dalle strafing. Restano circa 70 «élite» senza nome, per cui propongo 40 worg riders e 30 sergenti (`[INFERRED]`). Gli incantatori sono ~20: 15 warpriest e 5 war adept, e i 5 sono `[INFERRED]`. Grimjaw c'è solo se è fuggito dal 3B.
- **Le righe di scala.** 3B con 3 PG: cinque guardie; con 5 PG: dieci, più il sergente con i suoi quindici. 4A con 3 PG: il cavaliere è a terra; con 5 PG: in sella fino alla fine, e gli ettin stanno accanto a Gorthak.
- **Le schede.** Il bugbear è a GS 9, e non al GS 7 dei file, perché l'SRD somma i livelli di classe. Il gufo è a 8 DV, il massimo per restare Grande. L'orog è a GS 7: è il GS 6 dei file più un livello.

## Contrasti col canone, e incoerenze da guardare

- **Il ramo di gruppo** (`origin/campaign-group-rumblingstone`) non contraddice nessuna delle dodici scelte. Lythiel combacia («Direct recognition during Hammerfist Battle Sessione 4»). Su Dana il ramo tace. Per Fauci il default del ramo è «flees gravely wounded», e resta come esito del duello.
- **Dana**: la versione F («metà incantesimi») contrastava col canone del 2026-10-18, e ha vinto il canone, come chiedeva il D12.
- **I 232 pf contro C §4.1.** C §4.1 diceva «statblock invariato» se il P5 non è stato giocato, il che vorrebbe dire 337. Il D9 dà 232. Ho scritto il D9 e lasciato la frase di §4.1, ma resta strano che senza P5 Fauci parta più debole che con il P5 (303 o 337).
- **`Bestiario/png/Lythiel/Lythiel.md`** dice che è «una dei 12 ranger» sotto Ventolesto, che consegna la Ghianda «alla Battaglia» e che riparte dopo 24 ore. A, E e il D16 dicono che è l'inviata della Foresta e che resta fino alla Cerimonia. Non l'ho toccato.
- **Le guardie orog**: G §5 e gli statblocchi di A ne contano 4, mentre il 3B, B e la MAPPA 5 ne contano 10. Lo segnala la scheda.
- **La fanteria orchesca a inizio Sessione 4**: l'Atlante dice 200, le strafing di A e di B dicevano 300, e il Registro all'inizio ne schiera 120. Ho portato le strafing a ~200.

## Esito dei controlli

| Comando | Esito |
|---|---|
| `validate_maps.py` | ✓ 53 SVG allineati, nei due temi |
| `validate_modules.py` | ✓ 5 master, 0 errori (resta l'avviso su ARC07-DEF-2, che c'era già) |
| `validate_bestiario.py` | ✓ 190 statblock, catalogo in sync |
| `conformita_statblocchi.py --master` A, B, G | 3 file, 0 conti che non tornano |
| `collaudo_mappe.py` su F | 5 mappe · 7 errori · 13 avvisi, come prima |
| `validate_docs.py --sorgenti` | ✓ 1087 documenti |
| `copertura_scene.py --check` | ✓ 15 rilievi |
| `domande_developer.py --check` | ✓ 18 rilievi |
| `pytest scripts/tests` | ❌ 1 rosso su 1943: `test_verifica_sezione6`. `plans/STATO-E-ORDINE-DEI-PIANI.md` r.790 dichiara «20 box su 540», e oggi `misura_craft --p1` dà «20 box su 544» perché ho aggiunto quattro box. È in `plans/`, quindi lo correggi tu |
| `misura_craft --box`, riga ARC-08 | prima 86 box · 0 oltre le 12 righe · 7 con parentesi · 40 con più di un nome · 16 con più di 4 frasi · 15 oltre i 500 caratteri. Dopo 88 · 0 · 7 · 40 · 16 · 15 |

I box nuovi sono quattro: la picchiata e Lythiel, uno per ciascuno in A e in B. Sono etichettati `Read-aloud (Salvatore lead)` e `Read-aloud (Casa di Davide lead)`, stanno sotto le 4 righe, hanno un solo nome già noto e nessuna parentesi, e chiudono su «Che fate?».

## Che cosa resta aperto

- Come i nani tornano dalla caverna ai bastioni: il D13 conferma la mezza giornata, ma la strada il testo non la dice.
- I 70 «élite» senza nome e i 5 war adept.
- Il livello della *comunione* della Corona e il punto preciso della tana di Fauci (C §4.2).
- Il gufo di Lythiel, Inathiel (GS 5 nella sua scheda), si gioca con la scheda nuova del gufo, a GS 6.
- La riga 790 di `plans/STATO-E-ORDINE-DEI-PIANI.md`, da 540 a 544, per far tornare verde pytest.
- La scheda di Lythiel da riallineare (vedi i contrasti).
