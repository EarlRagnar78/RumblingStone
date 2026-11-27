---
name: prolog-verificatore-regole
description: ADR-0124 e PR #378: verifica delle schede via MCP (verifica_talenti, verifica_scheda), cascata SRD→3.5→PF1e, talenti dei manuali da PCGen e srd.dndtools.org, divario dei plugin misurato
metadata:
  type: project
---
2026-11-11 Jfs ha chiesto di valutare «grafo di eventi + regole Prolog + regola violata/controesempio all'LLM via MCP». Banco in plans/esperimenti/prolog-verificatore-2026-11-11/ (PR #378 bozza, ramo claude/project-thread-fv2zai, ADR-0124 proposta). Esito: Python, SWI-Prolog e clingo trovano le stesse violazioni e 141/141 difetti iniettati: niente motore logico, si adotta l'uscita strutturata regola/atteso/ha/fonte/file:riga via MCP.

Nella #378 (2026-11-12, richieste di Jfs in thread):
- scripts/verifica_talenti.py e scripts/verifica_scheda.py (talenti + numeri di conformita_statblocchi), manifest e server MCP, sola lettura, canale testing.
- Ordine delle fonti voluto da Jfs: **SRD d20 → D&D 3.5 → PF1e**, con `fonte` su ogni voce.
- SRD 3.5 talenti 110 → 363 (mostri, epici, psionici, divini). sistemi/dnd35/dati/talenti_manuali.toml: 2.193 talenti dei manuali, da PCGen (clone sparso di BahamutDragon/pcgen in /home/user/bahamutdragon/pcgen, git read via proxy) + tabelle di srd.dndtools.org (host aggiunto all'ambiente il 12/11, 138 pagine dei manuali sotto srd/meta/books/). Script in plans/esperimenti/talenti-manuali-35-2026-11-12/. Le due fonti divergono su 353/1.156: vince la tabella del manuale.
- D1, D2, D3 corretti in dmcore.talenti (classi it/en, Leadership = DV, «Incantesimi Focalizzati» nel generatore).
- Inventario del divario dei plugin: plans/esperimenti/verifica-scheda-2026-11-12/ESITO.md. Misura numeri con errori inseriti: 701/1.278.
- Jfs 2026-11-12 (card): fonti non OGL (PCGen, srd.dndtools.org) nel repo **solo nomi e numeri**.
- §8 classi: sistemi/dnd35/dati/classi_manuali.toml, 658 classi fuori SRD (script in plans/esperimenti/classi-manuali-35-2026-11-12/, pagine in /tmp scaricate dalla sitemap del sito, file *classes*.lst aggiunti al clone sparso PCGen). Entrano nei conti solo se regolari e concordi fra le fonti (17 divergono; il sito sbaglia il dado di Factotum e Healer). Nomi dei manuali solo a parola intera («tempest» leggeva «tempeste»).
- §9 prerequisiti fisici letti dalla scheda (volo, taglia, tipo, attacchi naturali…): non verificabili 82 → 47.
- §10-§11 capacità creature.liste_incantesimi: dnd35 dall'SRD più liste_incantesimi_manuali.toml (3.969 incantesimi, 84 classi da PCGen, file *spells*.lst aggiunti al clone), pf1e dal PRD. La classe che lancia si legge anche dal tipo (righe senza classe 94 → 16). Razza, sottotipo, allineamento come prerequisito (effetto zero sulle schede di oggi). «(B)» = talento bonus, vale solo con DV razziali.
- Stato al 12/11 (testa 9a657b94): violazioni 34 → 7 (12 falsi positivi, 16 corrette in 9 schede con nota in fondo). Le 7 vere aspettano il DM: Salvatore (2 incantesimi sotto livello), Fulmine a Tempestas (ARC08-01:679, ARC08-02:603), Divine Armor di Rurik, Inscribe Rune del dovil, Flame Strike al 4° in ARC-09 P1C:361. Elenco in ESITO §2-sexies di plans/esperimenti/verifica-scheda-2026-11-12/.
- Jfs 12/11: prima di chiudere violazioni che toccano classi dei manuali, finire i dati di quelle classi e rigiudicare.
- Report finale: Claude Doc https://claude.ai/artifact/F3qiww8C8Mci75kp2oZHhB. Restano: conto dei talenti rispetto ai DV, nomi italiani degli incantesimi dei manuali, riscontro delle liste PCGen sui libri.
- **#378 unita su main il 2026-11-12 (merge 43656328)**, sì di Jfs nel thread, merge fatto da questo thread su richiesta del coordinatore. Coerenza della storia: thread a parte, PR #379 (ADR-0125), riallinea a main.

Regola Jfs: una correzione di talento **aggiunge il prerequisito**, non toglie il talento (vedi [[feedback-numeri-piu-forti-calcolati]]).

[riga riservata · sha256:9ddb17a4]
