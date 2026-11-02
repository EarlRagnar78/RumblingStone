# Giro 3 su `ARC07-DEF-4`, completo: tutto il master

Continua `def4-giro3-serata/`, che aveva letto solo le parti della serata. Qui
le letture sono sul master intero, **un subagente alla volta** (regola del DM),
sul `main` di `3a22df9` più le correzioni di questo ramo fatte fra una lettura
e l'altra.

| Lettura | 🔴 | 🟠 | 🟡 | Rapporto |
|---|---:|---:|---:|---|
| lettore (a scene e intera, con diario) | 1 | 5 | 35 | `def4-giro3-LETTORE.md`, `def4-giro3-LETTORE-diario.md` |
| playtester | 0 | 4 | 20 | `def4-giro3-PLAYTESTER.md` |
| developer | 0 | 7 | 16 | `def4-giro3-DEVELOPER.md` |
| DM a freddo (a scene, `lettura_a_scene.py`) | 0 | 9 | 24 | `def4-giro3-DM.md`, diario in `corsa-dm/dm/` |

Lettore, playtester e developer non sono passati da `lettura_a_scene.py` e non
entrano in `letture-a-freddo.json`; il DM a freddo sì, ed è registrato con
l'impronta e lo stato di ogni 🟠.

## Il triage

| Rilievo | Chi | Esito |
|---|---|---|
| le pozioni del re in due versioni | lettore 🔴, playtester 🟠 | **D49** al DM |
| Grask con 4 tacche esatte | lettore | **D50** |
| ucciso «in silenzio» o «spettacolare» | lettore | **D51** |
| la lastra di Balvar | lettore | **D52** |
| il prezzo delle rune d'annullamento (Zeth è druido) | playtester | **D53** |
| i Treant nel duello | playtester | **D54**; corretto il rimando (era `DEF-3` §7, è A.2) e aggiunti CA, velocità, danni, durata |
| Balvar recuperato e il ritorno in volo | playtester | **D55** |
| Zog'tar catturato, il trasporto | playtester | **D56** |
| cosa ha il gruppo di stasera | lettore | non è del master: sta nel log del ramo di gruppo |
| sette elmi e sei nani · mezz'ora per 500 m · «come sopra» · le rune date o vendute · «due» pozioni fermano Kettra · la fonte dell'handout · la CA 37 «lanciata prima» | lettore | corretti |
| la tenda del generale «da non dire» che Durin indica | lettore e playtester | corretto: la prova serve solo se Durin non l'ha indicata |
| i giavellotti di Zog'tar a +20 | playtester | corretto: +19 (BAB 15, DES +5, −1 taglia) |
| la CA di Skullcrusher «dovrebbe essere 35» | playtester | **falso allarme**: 10 −2 taglia +2 DES (14 col template) +23 naturale (21 + 2 del template) = 33, già contato |
| *comando superiore* di Balvar «si ripete per 13 round» | developer | corretto: il TS si ritenta ogni turno (SRD) |
| il volo dei nani in armatura a 18 m | developer | corretto: 12 m (SRD), 1.200 m in 5 minuti; la pozione comprata copre 720 m |
| C.2 con altre CD e un'altra soglia della pattuglia | developer | corretto: le prove della Scena 6, due tiri falliti = la pattuglia |
| il drago Vecchio «GS 17» nella sidebar Scalare | developer | **falso allarme**: l'SRD dà GS 16 (d20srd.org, *Dragon, True*, tabella dei GS del drago nero) |
| la Presenza Minacciosa di Zog'tar | developer | **D57** |
| i PX delle Scene 6-8 | developer | **D58** |
| il bottino della tenda | developer | **D59** |
| lo sconto sull'ascia: 9.375, non 9.350 | developer | resta: è il conto pagato al tavolo |
| i 🟡 delle schede (Balvar contatto 14, guardie, Durin), gli altri PX, le tattiche di ronde e wyvern | developer | restano aperti per il giro 4 |
| gli esiti del rito e il punto di ripresa della Scena 5 | DM a freddo | non è del master: sta nel log del ramo di gruppo (`residuo` nel registro) |
| Durik senza statistiche nel master | DM a freddo | corretto: le righe del duello dalla sua scheda, con il rimando |
| il drago Vecchio più debole del base | DM a freddo | **D60** |
| *Dragondoom* di Aegis Fang | DM a freddo | **D61** |
| il *Registro delle Perdite* | lettore e DM a freddo | **D62**: il tiro non è definito in nessun file, non basta portare dentro una tabella |
| la pozione di *neutralizza veleno* | lettore (non contato) | **falso allarme**: è di 3° per il druido, e 750 mo è il prezzo SRD |

⚠️ **Un errore mio nell'incarico del playtester**: ho scritto che Hella è
umana. Il modulo la dice «nana del sogno», e il playtester lo ha segnalato
invece di seguirmi. Nessun rilievo dipende da questo.
