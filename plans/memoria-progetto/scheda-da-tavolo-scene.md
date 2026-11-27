---
name: scheda-da-tavolo-scene
description: Scheda da tavolo in testa a ogni scena del booklet di serata (12/11/2026): come funziona, esito del giro, cosa resta aperto
metadata:
  type: project
---

**2026-11-12, scheda da tavolo per scena (scelta di Jfs).** Sei schede in DEF-4, Scene 6-11, fra `<!-- scheda-da-tavolo -->`: escono solo nei capitoli presi per `sezioni` (dmcore.testo), la scena comincia a pagina nuova. Serata 118 → 122 pp. Giro dei tre lettori fatto e corretto; developer: «peggio degli AP come esecuzione» per i quattro strati (foglio, In scena, In tre righe, scheda), fusione non fatta perché toglie testo: decide Jfs. Corretto `#strong[..];` che perdeva il «;» nel PDF. Commit locali 46ab36c0 e successivo, non spinti (#370 aperta); PDF in /mnt/project-files/taglia-portata/v3/. Aperti: «Dove guardare» senza numeri di pagina; «Il bottino della tenda e il tempo» e Appendice B non stampati nella serata.

Vedi [[standard-volume-booklet]].

**2026-11-12, fusione chiesta da Jfs.** Nella serata la scheda da tavolo è l'unica apertura di scena: voci «Succede», «Dove», «Chi c'è», «Chi vuole cosa», …, «Sviluppo», «Come finisce», «Dove guardare», EL nel titolo. Nel master «In tre righe» resta fra `<!-- senza-scheda -->`/`<!-- /senza-scheda -->` (si stampa solo nei volumi senza scheda); la riga «In scena» resta nel master (la leggono chi_si_incontra e copertura_scene) e in stampa entra nella scheda con `dmcore.testo.fondi_contratto_e_scheda`. Giro al cieco: DM e redattore scelgono la fusa, il developer solo con «Succede» in testa; resta «peggio degli AP, di poco» (scheda lunga, niente numeri di pagina). La fusione non accorcia il booklet (125 pagine). Tema Typst: ogni tabella larga sta in cima alla pagina (in fondo Typst 0.15 la sovrappone ai riquadri), riga breve non spezzabile.
