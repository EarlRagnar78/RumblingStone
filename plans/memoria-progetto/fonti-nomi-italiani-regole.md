---
name: fonti-nomi-italiani-regole
description: Fonti dei nomi italiani ufficiali di D&D 3.5 e PF1e (Mephit, Editori Folli, Dragons' Lair, Golarion API, aonprd) e come abbinarli all'inglese (aggiornato 2026-11-07)
metadata:
  type: reference
  modified: 2026-11-07T10:53:12.188Z
---
Per le tabelle dei termini (ADR-0110, ramo `regole-ufficiali`, scripts/lessico_it_35.tsv e lessico_it_pf1.tsv). Dal 2026-11-07 (Jfs ha aperto i domini) curl arriva a: editorifolli.it, mephit.it, dragonslair.it, aonprd.com, golarion.altervista.org (API MediaWiki: con curl sì, con urllib di Python 403 per lo user agent).

- **Editori Folli**: SRD 3.5 tradotto in PDF, `https://www.editorifolli.it/f/srd35/<file>.pdf` (solo https). Cache ~/.cache/rumblingstone/editorifolli/ con .txt da `pdftotext -layout`. Incantesimi, condizioni, abilità, equipaggiamento sì; **niente bestiario**. Abbinamento senza nomi: incantesimi per scuola+livelli+componenti+tratti; equipaggiamento per firma (costo, danni o CA, peso) unica nelle due lingue. Due refusi della fonte: «Spade corta», «Scudo pesante legno».
- **Dragons' Lair**: prontuario delle condizioni in italiano (download con cookie e csrfKey), cache ~/.cache/rumblingstone/dragonslair/.
- **Mephit** (github.com/mephitrpg/mephit, GPL-3): dump MySQL in `_sql_backup/mephit_test.7z` con tabelle `srd35_*` bilingui (talenti, abilità, classi, domini, oggetti magici, equipaggiamento). La tabella dei mostri è solo inglese. Nomi degli incantesimi con refusi: vince la doppia fonte.
- **Golarion Insider (PF1e)**: `list=exturlusage` o `prop=extlinks` danno pagina italiana → URL aon/d20pfsrd. Archetipi di mostro: una pagina «Archetipo X» con il suo link. Archetipi di classe: le pagine «X di Golarion» hanno «Fonte: [aon ArchetypeDisplay …]» per voce; le pagine «X/Archetipi» no, e si abbinano per firma dei privilegi (livello + Str/Sop/Mag), unica nella classe, contro il PRD o le pagine aon.
- **aonprd.com**: `Archetypes.aspx?Class=X` (1.252 archetipi), `MonsterTemplates.aspx?ItemName=All` (165 modelli). Con curl serve `-g` per i nomi con [ ].
- **Mostri 3.5 in italiano**: nessun elenco legale completo in rete (Wikidata rumoroso, fandom/d20srd 403, 25edition.it oggi è un casinò, web.archive.org chiude la connessione, Sigil non esiste, rpgcrossing rifiuta i programmi). Elenchi completi solo in scansioni piratate (Scribd, PDFCoffee, anyflip, dokumen.pub): mai. Strada legale: indice cartaceo di Jfs. I nomi PF1e italiani non valgono per la 3.5.
- **Tabelle del tesoro GDM 3.5** (scheda di Mindbender, untidigradsul.wordpress.com/wp-content/uploads/2011/06/dd-3-5e-ita-scheda-tesoro-e-oggetti-magici.pdf): righe abbinabili all'SRD per d%+prezzo (abbinamenti/abbina_tesoro.py); la tabella degli oggetti meravigliosi maggiori ha ordine e prezzi diversi dall'SRD, non usarla per firma. Il GDM italiano tiene i nomi dei maghi (Zainetto pratico di Heward).
- **5° Clone** con `?limit=0`: incantesimi 1.368, talenti 794, classi/CdP 247 voci con «Nome (Ita)/Nome (Ing)» e manuale+pagina (anche manuali non base); il suo Bestiario (79) è Dragon/Planescape, non il MM.
- **tapionx/manuale_incantesimi_dungeons_and_dragons_3.5** (CC0): src/incantesimi_ded35_per_classe.json via raw.githubusercontent.com (github.com è fuori scope), 606 incantesimi SRD name/altname: 600/605 concordi con la tabella.
- Glossario MdG di gdrzine (Lord Orpheus): nomi probabilmente 3.0 (Arma Preferita, Specializzazione in un'Arma), solo per misura.
- Editori Folli ha anche 118 PDF srd35_02_01_razze_* (mostri come razze, nomi plurali e varianti UA): candidati, non nomi del MM.
- PDF di Jfs (2026-11-07): prontuario abilità (35/35 concordi) e condizioni (Blown Away = Portato via).
- miniaturefantasy.com: liste 3.5 italiane, alcune pagine sono regole della casa: usare solo i nomi. dandwiki «Pianura dei Draghi» è homebrew.

Vedi [[standard-marcature-inferred]], [[ricerca-web-senza-firecrawl]].
