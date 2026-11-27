---
name: tattiche-villain-2026-11-15
description: Thread «Rivedere le tattiche di villain e PNG» (15/11): schema dei draghi su villain e PNG, inventario per vicinanza al tavolo, divisione dei file con gli altri thread
metadata:
  type: project
  modified: 2026-11-15T08:44:12.885Z
---

Richiesta di Jfs del 15/11: rivedere le tattiche di villain e PNG importanti con lo schema dei draghi (carattere, obiettivi, cosa sanno dei PG, ambiente, stato dei PG, adattamento, Monte Carlo).
Inventario: /mnt/project-files/tattiche-villain-2026-11-15/INVENTARIO.md. Ordine: Zog'tar sulla breccia (ARC07-DEF-4 Scena 10, non usa quello che ha imparato col barile), Balvar; poi Grimjaw e Gorthak (ARC08-02 §1); poi ARC-09; alleati per ultimi.
Divisione: draghi e Cavaliere di Fauci sono del thread dei draghi (simulatore comune simula_scontri.py in /mnt/project-files/tattiche-draghi-2026-11-15/, profili miei in un file a parte, motore non si tocca senza dirlo). Skullcrusher, DEF-4 Scena 11 e BARILE B13 del suo thread: io entro dopo la sua PR su DEF-4. Schede del Bestiario: chiedere prima ai thread regole e volume.
Stato 15/11 11:00: #449 unita (26137052, MS-0144): Zog'tar sulla breccia «separa e finisce» (DEF-4 Scena 10), Balvar e sacerdote al campo (BARILE §8), Gorthak in ARC08-02 allineato a DEF-2. Profili in plans/esperimenti/tattiche-2026-11-15/ sul motore plans/esperimenti/tattiche-draghi-2026-11-15/simula_scontri.py (#450). ARC-08 DEF-2 ha già lo schema. ARC-09: Jfs ha scelto (card 15/11) il dossier per i master DEF, non i sorgenti. Dossier in /mnt/project-files/tattiche-villain-2026-11-15/DOSSIER-ARC09-TATTICHE.md (per villain: dove sta la tattica, schema in 6 punti, buchi con file e riga: Zarim ed Emissario con **Tattiche** vuoto, Xilthra e Kragar senza tattica, Sethrax con tre primi round, esplosione mentale di Xal'thor con ricarica non SRD). Va letto da chi fonde ogni ARC09-DEF-NN; non è nel repo.


**Why:** evitare di rifare l'inventario e di toccare file altrui. **How to apply:** vedi [[tattiche-draghi-2026-11-15]] e [[skullcrusher-tattica-dinamica]].

Stato al 17/11 22:15: lotti 1-5 tutti uniti (#454 MS-0148, #463 MS-0158, #465 merge 6951f2b2 MS-0159; prossima MS-0160). Card chiuse: Zarim (charme su Hella), Karruk (Aegis Fang non si spezza), Collezionista (esiti dai quattro patti). Sethrax: applicata la consigliata senza risposta registrata; se Jfs sceglie l'altra, PR a parte. Ghaurush non misurabile (muri). #467 unita (ea63a192, MS-0162): inventory_inferred ha la classe «copie» per le marche ristampate nei file generati (solo contro un sorgente vivo), baseline 14. commit-archaeologist è a un file dalla soglia (un file di gioco con 10 commit in 60 giorni senza `<!-- storico -->` la fa scattare). Marche [INFERRED] sempre con domanda e base; nei sorgenti dei booklet vanno in commento HTML, dopo i blocchi statistiche.
18-19/11: ricontrollo. #479 unita (39da52b7, MS-0189). 19/11 thread «Completare le tattiche di villain e PNG»: rilettura completa dei lotti 1-4; card scelte da Jfs: fantino rapito al Palio, Xal'thor suggestione CD 16, Zalkatar con Ozyrrandion solo su storditi. Card Xilthra (slot) era un mio errore: scheda giusta, non applicata. #495 unita il 19/11 (3cee661c, MS-0203 e MS-0204). Pozioni di Zog'tar (2 cura ferite gravi, card del 19/11) nella #497 del thread booklet ARC-07. Kragar (P2B BATTLE-STATS r.64-74) ha conti sbagliati, girato al thread regole. Lezione: `verifica_scheda` prima di ogni card su un numero; una frase INFERRED va riletta contro la scheda.
