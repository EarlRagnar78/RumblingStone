# Registro delle regole custom della campagna

Le regole ibride e le varianti che il DM ha scelto per RumblingStone. È il
registro che chiede la D-B-ter di
[ADR-0126](../plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md):
una scheda può mescolare regole di sistemi diversi solo se la mescolanza è
scritta qui. Ogni voce dice l'elemento, il sistema da cui viene, il sistema
della scheda, la fonte e la data della decisione. Una voce si aggiunge solo
con una decisione del DM.

| Voce | Elemento | Sistema d'origine | Sistema della scheda | Fonte | Data | Decisione |
|---|---|---|---|---|---|---|
| RC-001 | Equipaggiamento standard di chi avanza per classe: elenco degli oggetti dal PNG di pari classe e livello | PF1e (NPC Codex, Monster Codex; Core Rulebook, Tabella 14-9 per il ripiego a categorie) | D&D 3.5 | valore: DMG 3.5, Tabella 4-23, al livello effettivo; prezzi: SRD 3.5; chi ne ha diritto: SRD 3.5, «Improving Monsters» | 2026-11-13 | [ADR-0134](../plans/adr/ADR-0134-l-equipaggiamento-standard-viene-dai-codex-pf1e-entro-il-valore-del-3-5.md) |
| RC-002 | Arbitrax, drago rosso giovane adulto: armatura naturale +24 (SRD +18) e GS 15 (SRD 13) | variante del DM | D&D 3.5 | scheda `Bestiario/villain/arbitrax-drago-rosso-cr15.md`, righe `gs` e `ca-dettaglio`; export PCGen della scheda | 2026-11-14 | risposta del DM sulla card del 2026-11-14: «Variante del DM, numeri di oggi» |

## RC-001 · Equipaggiamento standard

1. Solo le creature che avanzano per classe hanno l'equipaggiamento di un
   PNG; le altre tengono «Tesoro».
2. Prima si scrive ciò che i conti della scheda già mostrano.
3. Poi si prende dal PNG dei Codex PF1e di pari classe e livello, coi prezzi
   del 3.5.
4. Il tetto è la Tabella 4-23 al livello effettivo (dadi vita + modificatore
   di livello + livelli di classe); la 14-9 nelle schede PF1e.
5. Sopra il tetto si toglie nell'ordine: uso limitato, attrezzatura, magia.
   Mai ciò che la scheda usa.
6. Senza un PNG nei Codex: budget nelle cinque categorie della 14-9, oggetti
   scelti dal DM.
7. Un oggetto che nel 3.5 non esiste lo decide il DM.
8. Per le classi da PNG vale la colonna unica della 4-23.

Come si cerca: `python3 plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_codex.py --cerca fighter 5`.

## RC-002 · Arbitrax oltre la sua categoria d'età

1. Arbitrax è un drago rosso giovane adulto (19 DV, Enorme) con le scaglie
   più spesse della sua età: armatura naturale +24, CA 32.
2. Il grado di sfida è 15, due sopra il 13 dell'SRD: conta i +6 di armatura
   naturale e gli oggetti che porta.
3. La variante vale solo per lui. Un altro drago fuori dalla base chiede una
   voce sua.
4. Come si dichiara in una scheda: una riga «Armatura naturale diversa dalla
   base: …» o «Grado di sfida diverso dalla regola: …» col numero della
   scheda e «DM» o la voce RC. Senza la riga `verifica_scheda.py` segna lo
   scarto.
