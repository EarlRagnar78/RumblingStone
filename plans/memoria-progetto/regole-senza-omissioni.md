---
name: regole-senza-omissioni
description: Programma chiesto da Jfs il 2026-11-12: chiudere il divario delle regole 3.5/PF1e sezione per sezione, tolleranza zero sui bonus, variante della campagna, poi MCP e controllo finale
metadata:
  type: project
---
Jfs 2026-11-12 07:54 (thread della PR #378): completare le regole dei plugin con tutto ciò che hanno srd.dndtools.org, PCGen e altri siti, senza omettere nulla; cercare altri siti per il riscontro; stringere la tolleranza («un +4 è un bonus importante»); aggiungere al MCP la variante della campagna (SRD d20 → D&D 3.5 → PF1e, risultato più forte per villain, PNG e mostri) con logica deterministica; il verificatore non salta niente di ciò che la scheda scrive, tranne descrizione e tattica (che devono comunque essere coerenti). Dubbi = card con scelta consigliata.

Audit fatto: /mnt/project-files/regole-senza-omissioni-2026-11-12/INVENTARIO-E-PIANO.md (12 lotti, decisioni D-A…D-D in forma ADR). Fatti misurati:
- 12 campi della scheda senza nessun controllo (danno, CA 3.5, velocità, conto dei talenti, modificatore delle abilità, slot, CD, RI/RD, sensi, ricchezza, GS, linguaggi).
- Siti raggiungibili dal container: realmshelps.net (3.5, seconda fonte), aonprd.com (PF1e tutti i libri, OGL). Chiusi: d20srd.org (403), dndtools.net/new.dndtools.org/dndtools.one, dnd.arkalseif.info, d20pfsrd.com (410).

Deciso da Jfs il 2026-11-12 (card): «più forte» si sceglie **per elemento intero** (ogni classe, talento, incantesimo o tipo di creatura prende un solo sistema, scritto sulla scheda; niente ibridi dentro lo stesso elemento). Ambito (card, stesso giorno): **tutto ciò che una scheda può scrivere** (regole base, manuali, psionici, invocazioni, manovre e gli altri sottosistemi); varianti di Unearthed Arcana come opzioni spente; homebrew del sito fuori.

Coordinamento (Jfs 12/11: organizzarsi con gli altri thread): ordine #378 (testa 9a657b94 ferma) → una PR per lotto, ramo ripartito da main; un solo ADR per il programma, numeri in plans/adr-prenotati.json; il thread della #379 fa la coerenza tattiche/scheda (S8) e vuole da verifica_scheda un JSON per scheda con talenti, incantesimi, capacità speciali e righe delle sezioni Tattiche/Descrizione. Lotto 1 = PR #380 unita il 2026-11-12 (b23fd0d0, ADR-0126 di programma): capacità bonus.cumulo (sistemi/d20/dati/bonus.toml), dmcore.bonus, tolleranza zero in verifica_scheda. Banco 701 → 1.007 su 1.279; 22 numeri trovati e chiusi (6 difetti del verificatore, 14 schede con mantello della resistenza o bonus razziale dichiarato, scelta di Jfs). Regola pratica: una capacità nuova va dichiarata anche in scripts/tests/dati/prova-d20/sistema.toml.

ADR-0123 è del thread #370 (campi taglia/spazio/portata nei recinti, 205 schede, non ancora su main; bundle in /mnt/project-files/taglia-portata/): primo ADR libero per questo programma = 0126; avvisare quel thread prima di cambiare CA, attacco o Lotta delle schede che ha toccato (elenco in INVENTARIO-E-PIANO §8).

Jfs 12/11 08:03: il motore deve potersi vincolare, per regole e verifica MCP: parametro unico `motore` = srd35 | dnd35 | pf1e | rumblingstone (variante «più forte», solo su richiesta); con motore vincolato un elemento di un altro sistema è una violazione. Oggi la cascata è cablata in verifica_talenti.risolvi.

**How to apply:** una PR per lotto dopo il merge della #378, ogni lotto con misura prima/dopo. Vedi [[prolog-verificatore-regole]], [[feedback-numeri-piu-forti-calcolati]], [[regole-complete-2026-11-10]].
Jfs 12/11 08:07: le forme ibride (regole di sistemi diversi nella stessa scheda) sono lecite solo col motore `rumblingstone`, vanno verificate per coerenza e scritte nel registro delle regole custom del DM (D-B-ter del piano; registro previsto in sistemi/rumblingstone/dati/ibride.toml, lotto 11). Non registrata = violazione anche nella variante.
Lotto 1-bis (dopo merge #380): portare in verifica_scheda i conti dei recinti (CA 27, sensi 10, CD 1 sul Bestiario).
