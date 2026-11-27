---
name: regole-stato-2026-11-14
description: Thread delle regole al 18/11 23:10 UTC: #468, #470 e #477 unite (main 4588bc5f, MS-0183), cosa resta dei lotti
metadata:
  type: project
  modified: 2026-11-14T21:12:52.498Z
---

Stato del thread delle regole (ADR-0126, regole senza omissioni) al 2026-11-18 01:35 UTC. La storia delle PR sta in plans/MEMORIA-STORICA.md (MS-0108…0134) e negli addendum dell'ADR-0126.

- Main = 4588bc5f (#477, MS-0183: scuola di tutti i 1536 incantesimi PF1e in liste_incantesimi.toml [scuole]; il numero MS lo dà il coordinatore). Misura del 19/11 su main 0cfa1357: 153 schede, 34 violazioni (27 in ARC-08/09, quasi tutte incantesimi al giorno e CD), 386 non verificabili (`verifica_scheda.py Bestiario 0*/ --json` dalla radice, >2 min: in background).
- #464 (17/11): segugio infernale mezzo-immondo dall'SRD, card del 15 e 17/11. Restano i dadi degli attacchi naturali coi modelli.
- #468 (18/11): Incantesimi focalizzati col nome giusto e la scuola prevalente sul blocco ([scuole] nei dati 3.5 e PF1e); senza incantesimi, o senza scuola nelle tabelle (estratti dell'alchimista, osservazione di Codex), si prende il talento seguente del ruolo (card di Jfs del 17/11). #470: la nota nel conto solo se l'esclusione cambia la scelta (impronte.py torna a 3 rossi noti). Seguiti possibili: CD +1 della scuola, altri talenti da incantatore sui non incantatori, 912 voci PF1e senza scuola, nome «Thundering Drums».
- Non giudicati perché il tipo non nomina il modello: Azarr Kul finale, Therysol, Ghostlord.
- Prossimi: razze coi dadi vita razziali, lotti 9-12, prezzi PF1e.
- `adozioni_in_attesa.py --check` (in CI, vuole la storia completa: `git fetch --unshallow`) è a 2 file su 3; al terzo file di gioco con 10+ commit in 60 giorni scatta, rimedio: blocco `<!-- storico -->` nel sorgente (ADR-0069).
- Resta: mostri dei manuali, secondo giro prezzi 3.5; 96 oggetti Codex in /mnt/project-files/schede-schema-2026-11-13/OGGETTI-CODEX-SENZA-PREZZO-2026-11-14.md.
- Non toccati, restano a Jfs: GS «16–17» a terra di Tyrgarun (Fase 4) e la riga «Boost log» della sua scheda. Il monaco (Riflessi +8, mantello) lo porta su card il thread del volume.

**Why:** l'indice MEMORY.md viene riscritto da altri thread e le righe di stato si perdono.

**How to apply:**
- Una scheda non si corregge mai senza la risposta di Jfs, nemmeno un errore di trascrizione: card prima.
- Dichiarazione di variante nella scheda: riga «Armatura naturale diversa dalla base: N …» o «Grado di sfida diverso dalla regola: N …» con DM/RC/ADR; conta il primo numero dopo i due punti.
- Misura contro main: `git worktree add --detach <scratchpad>/wt origin/main`, poi remove e prune prima della suite. Una misura che tace va controllata.
- La base si dichiara solo dopo «SRD», «MM» o «Monster Manual»: il solo nome nella fonte no (l'Ogre Skullcrusher di Races of Faerûn prendeva una violazione falsa).
- `_recinti_del_master` non vede un blocco senza `ca:` e `ts:`: le schede di prova dei test devono averli.
- test_validate_docs.py e test_validate_pg.py::TestDeriva possono fallire con `-n 4` e passare da soli: difetto noto di xdist, dichiararlo nella PR.
- Dopo una modifica fatta con uno script guardare `git diff --stat` prima del push (un replace su stringa vuota ha gonfiato un ADR di 373.000 righe e la CI era verde).
- Dopo il merge il ramo si riallinea con reset su origin/main e push semplice (il ramo remoto viene cancellato dal merge).

Vedi [[regole-senza-omissioni]], [[equipaggiamento-standard-codex]], [[regole-lotti-archivio-1]], [[regole-lotti-archivio-2]].
- Da guardare (segnalato dal thread del volume il 19/11, #478 su main 2ebb687c, MS-0188): verifica_scheda conta una sola perla del potere per grado a Therysol.
- 19/11 revisione storica su dnd.arkalseif.info: #498 unita il 19/11 (main 2af972cd, MS-0207), ventidue card applicate, Tempestas GS 15 anche in state.yaml/state.md (flusso nel playbook §4.3-bis), 34 → 2 violazioni. Registro in /mnt/project-files/revisione-arkalseif-2026-11-19/. Fulmine e chierica di Lolth chiusi su card.
- 20/11 lotto «razze coi dadi vita razziali» (sì di Jfs 14:37): parte abilità fatta su ramo locale `lavoro/razze-dv` (commit 4f6c2e1f su main 696448ac; patch in /mnt/project-files/regole-razze-dv-2026-11-20/), più 7587e171 (verifica caratteristiche_dalla_fonte contro il .pcg; Bothor For 18 per card del 20/11), patch 0001-0002, da portare sul ramo del thread dopo il merge di #509: [razze_dv] in gradi.toml (31 creature), banco muta_abilita +1 su due casi, 0 violazioni nuove. Caratteristiche razziali: misura in /mnt/project-files/regole-razze-dv-2026-11-20/ (serie DMG 49/64 scarti, non è una regola), scelta di Jfs: contro il .pcg (fatto). Card aperta: dove bocciare chi non rientra in serie DMG o acquisto a punti (21 su 64; consigliata: solo i generici di mostri/).

**20/11 16:00:** lotto razze-dv in locale (worktree scratchpad wt-razze, ramo lavoro/razze-dv su main 696448ac), 3 commit, patch 0001-0003 in /mnt/project-files/regole-razze-dv-2026-11-20/. Drow ×4 e Orog rifatti con élite + razza (card 20/11); ARC08-02 orog AU +14 DU 21; lettura_creatura.dalla_scheda ora salta il blocco storico. PR dopo merge #509. Aperte: card dei 7 PNG >32 punti; Comune dell'orog INFERRED.
**20/11 18:10:** sette PNG >32 punti decisi su card (Khorn mantello Car+2, Zin'thara guanti Des+2, Balvar cinque +2; Lythiel/Maewen/Dauth élite); commit locale 0004. Tempestas: card ri-chiesta coi numeri veri dell'élite (pf 97→67, CD −2). Grimjaw (orog) non ancora controllato.
