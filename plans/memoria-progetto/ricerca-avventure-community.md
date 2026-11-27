---
name: ricerca-avventure-community
description: Ricerca del 2026-10-18 sulle avventure community 3.5/PF1e e il suo lotto 1 (PR #244, ADR-0092: domande developer §9-§16, D9/D10/D15/D16, Statistiche base)
metadata:
  type: project
  modified: 2026-10-18T11:52:48.699Z
---

Analisi in /mnt/project-files/avventure-community/ e nel repo come plans/RICERCA-AVVENTURE-COMMUNITY-2026-10.md + PIANO-AVVENTURE-COMMUNITY-2026-10.md. Jfs ha scelto «Piano e PR»: lotto 1 nella PR #244, unita su main il 2026-10-18 (D9/D10/D15/D16 ora nel --check di CI per ogni master nuovo), ADR-0092. Misura del miglioramento: su main 13 rilievi, col lotto 24, gli 11 nuovi tutti in domande che prima nessuno misurava, 6½ difetti veri.

Lotto 1: sviluppo-degli-incontri.md §9-§16; domande_developer.py D9 (blocco «Se lo divinano», apl≥9), D10 (riga di scala per scontro), D15 (orde ≥6, apl≥9), D16 (salva o sei fuori); profilo `apl` in plans/domande-developer.json (Drappo 3, Abbazia 7, default 13). Riga «Statistiche base» nello statblocco: 11 su 37 la vogliono, nessuno toccato. D1-D3 decise da Jfs il 2026-10-18 come proposte: Statistiche base solo quando un master usa lo statblocco; D2 poi cambiata da Jfs lo stesso giorno: le 4 righe di scala di ARC-07 (DEF-1 S3, DEF-4 S6/S8/S10) le aggiunge il thread PNG nella #245, che toglie anche i residui; la PR #246 registra la D2 nel piano; lotto 2 insieme a S1 ARC-08. Lotto 2 (roster del sito, foglio dello scontro, indici) da fare con S1 di MASTER-DEF (ARC-08).

**Why:** calibrazione D10 6/9 veri, D16 non calibrata; residui ARC-07 dichiarati perché master già giocati.

**How to apply:** accordo col thread «Schede PNG e cattivi uniformi»: quel thread tocca i DEF di ARC-07 e il Bestiario, questo no; chi va su main per secondo fa merge e rilancia domande_developer --check. Vale [[scelte-inferred-versione-piu-forte]].

Prossimo (Jfs, 2026-10-18 14:05): dopo la ricerca sulla prosa deterministica (inventario + web, in corso), il thread «Schede PNG e cattivi uniformi» (decisione finale del coordinatore, 14:05:41) rifà i cinque DEF di ARC-07 come banco di misura prima/dopo: regole nuove, prosa, strutture, mappe, giro completo developer/playtester/DM. Si parte dopo che la #245 è su main; questo thread gli passa i risultati della ricerca sulla prosa.

Prosa (2026-10-18): /mnt/project-files/avventure-community/PROSA-DETERMINISTICA-2026-10-18.md. Deterministico solo per forma/difetti; la qualità solo col cieco del DM. Misura nuova più utile: parole per box (banda 30-70, >100 lungo): ARC-07 21/107 box >100, ARC-08 2/162. Protocollo proposto per il giro ARC-07: 20 box fissi prima, cieco del DM, successo ≥14/20 senza norme in crescita. Prototipo note-di-ricerca/box_metri.py, non nel repo.

**Prosa (2026-10-18, PR #246 lotto 4, ADR-0093)**: la prosa migliora solo se il DM sceglie la nuova versione alla cieca in ≥14 coppie su 20 (`cieco_versioni.py`). Campione ARC-07 congelato in plans/esperimenti/prosa-cieco/. `misura_craft --stile` = indicatori senza peso. Corpus di riferimento in /mnt/project-files/corpus-prosa/: solo numeri, ricavati da 121 box EN Paizo gratuiti e 56 IT del Gruppo Chimera. Il proxy blocca paizo, wizards, archive.org, gruppochimera e dragonslair: Jfs deve aggiungere i domini all'ambiente cloud. I testi di terzi non entrano mai nel repo.
