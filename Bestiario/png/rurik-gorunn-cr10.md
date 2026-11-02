# Rurik Gorunn, Martello di Moradin [TRANSCRIBED — PCGen, L1 2026-07-08]
**Faction**: martello-moradin | **Role**: melee-heavy | **Environment**: mountain | **CR**: 10 | **Source**: PCGen export `Bestiario/pregen-pcgen/png_La_mano_rossa_del_destino/Rurik Gorunn martello di moradin 10 liv.htm` | **Status**: transcribed-pcgen


```statblocco
gs: 10
tipo: Medium humanoid (dwarf), Paladin 8 / Hammer of Moradin 2, LG
ca: 22
ca-dettaglio: touch 10, flat-footed 22 (armatura completa +1, scudo pesante +1, anello di protezione +1, −1 Des)
pf: 80
pf-dado: 10d10+20
ts: Temp +13, Rifl +3, Vol +8
attributi: For 14 Des 8 Cos 14 Int 10 Sag 14 Car 14
velocita: 6 m
iniziativa: -1
attacchi:
  - Mischia martello da guerra +1 gelido +14/+9 (1d8+3 +1d6 freddo/x3)
  - Distanza martello da guerra +1 gelido lanciato +11 (1d8+3 +1d6 freddo/x3, incremento 6 m, ritorna)
  - Mischia colpo di scudo pesante +1 +12/+7 (1d4+2)
voci:
  - Talenti: Celestial Mount, Divine Armor, Volontà di Ferro, Arma Focalizzata (martello da guerra)
  - Incantesimi: paladino 8, LI 4, 2/1, CD 12 + livello
```

> **Caratteristiche trascritte a mano dall'export PCGen** (le stesse che `genera_attributi.py` aveva copiato). La CA di contatto 10 con Des 8 non è un errore: è l'anello di protezione +1 dell'export (10 −1 +1).

> **I dadi vita** (non verificato sul libro). I pf dell'export sono 80, tirati livello per livello (10+6+5+6+5+6+5+6 da paladino, 5+6 da Martello di Moradin, +2 di Cos a livello): il d10 da paladino è SRD, quello della classe di prestigio è letto dai tiri dell'export, nessuno sopra 10. Da qui `pf-dado` 10d10+20.

**Iniziativa** −1 · **Sensi** scurovisione 18 m; *individuazione del male* a volontà; Ascoltare +2, Osservare +2 · **Aura** di coraggio (3 m)

**Difesa** **CA 22**, contatto 10, colto alla sprovvista 22 (+4 schivare contro i giganti) · **pf 80** (10d10+20) · TS Temp +13, Rifl +3, Vol +8 (+2 contro veleni, incantesimi e capacità magiche) · immune a paura e malattie; alleati entro 3 m +4 contro la paura · stabilità

**Attacco** Vel 6 m · **Mischia** martello da guerra +1 gelido +14/+9 (1d8+3 più 1d6 freddo/x3); colpo di scudo pesante +1 +12/+7 (1d4+2) in alternativa · **Distanza** il martello lanciato +11 (incremento 6 m), torna in mano prima del turno successivo · **Attacchi speciali** punire il male 2/giorno (+2 al colpire, +8 ai danni); *Goblinkiller* 1/giorno; scacciare non morti 5/giorno (come chierico di 5°) · **Incantesimi preparati** (paladino 8, LI 4; CD 12 + livello): 2° — *resistere all'energia*; 1° — *benedire l'arma*, *favore divino*

**Statistiche** For 14, Des 8, Cos 14, Int 10, Sag 14, Car 14 · BAB +10; Lotta +12 · **Talenti** Celestial Mount [Private source — Book of Exalted Deeds], Divine Armor [Private source — Player's Handbook II], Volontà di Ferro, Arma Focalizzata (martello da guerra) · **Abilità** Artigianato (fabbro d'armi) +12, Concentrazione +8 · **Linguaggi** Comune, Nanico · **Equipaggiamento** armatura completa +1, scudo pesante di metallo +1, martello da guerra +1 gelido, anello di protezione +1, bacchetta di *cura ferite leggere*, pozioni di *volare*, *cura ferite gravi* e *cura ferite moderate*

**Capacità speciali**
- **Paladino 8** (SRD): aura di bene, *individuazione del male*, punire il male 2/giorno, grazia divina, imposizione delle mani (16 pf al giorno), aura di coraggio, salute divina, scacciare non morti, *rimuovi malattie* 1/settimana, cavalcatura speciale (l'ariete celestiale, scheda gemella nella stessa cartella).
- **Martello di Moradin 2** [Private source — Player's Guide to Faerûn, variante del Martello di Moradin]: aura di coraggio; **lancio del martello** (Str: il martello da guerra è un'arma da lancio con incremento 6 m, senza penalità); **Goblinkiller** (Sop: 1/giorno, con un'azione di movimento, il martello diventa *anatema dei goblinoidi* per un numero di round pari al mod Car, 2 round); **ritorno del martello** (Sop: il martello lanciato torna come un'arma *di ritorno*).
- **Divine Armor** [Private source — Player's Handbook II]: spende un uso di scacciare non morti per una protezione divina sull'armatura. Il testo non è nel repo (non verificato).

> ⚠ Prerequisito: il Martello di Moradin chiede la regione **Spina del Mondo**; l'export dà a Rurik le **Smoking Mountains**. Gli altri requisiti tornano (BAB +7, Artigianato fabbro d'armi 10 gradi, Volontà di Ferro, Arma Focalizzata martello, incantesimi divini di 2°, patrono Moradin). Si tiene la classe. PF1e: nessuna classe o archetipo del PRD fa lancio-e-ritorno del martello con l'aura del paladino; l'arma *di ritorno* più il talento Lancio Rapido sul paladino base si avvicinano nel combattimento ma perdono Goblinkiller e l'aura, quindi stravolge poco e dà meno. Basta ignorare la regione.

**Tattiche**
- *Prima del combattimento*: se ha un minuto, *benedire l'arma* sul martello (contro i malvagi ogni minaccia di critico è confermata) e richiama l'ariete; *resistere all'energia* al fuoco se c'è un drago rosso nell'aria.
- *Durante il combattimento*: al primo round, se il nemico è lontano, lancia il martello (+11, torna da solo) sul bersaglio malvagio più vicino, oppure carica in sella all'ariete. Contro goblinoidi attiva Goblinkiller con un'azione di movimento e passa all'attacco: con *anatema* il martello fa +2 al colpire e 2d6 in più. Il punire il male lo spende sul capo nemico, non sui gregari. Resta a contatto con i suoi: l'aura di coraggio vale solo entro 3 m. Contro i non morti scaccia prima di colpire. Contro chi vola lancia il martello a ogni round, o beve *volare*.
- *Morale*: è un paladino, non fugge da un male che minaccia innocenti. Sotto i 25 pf usa l'imposizione delle mani su se stesso (16 pf) e poi la *cura ferite gravi*, senza lasciare la linea. Si ritira soltanto se gli innocenti sono già al sicuro, e per ultimo.


**Benchmark**: PF T1-1 riga 10 (CA 24, pf 130, att +18, danno 45, CD 19): CA 22 (−2), pf 80 (−50), att +14 (−4), danno con l'attacco completo ≈23, ≈31 col punire (sotto). Con l'ariete (GS 5) intorno l'incontro sale a EL 10-11.

Notes: campione dell'ordine del Martello di Moradin; alleato.

Boost log: correzione dei conti (dadi vita, colpo di scudo, lancio del martello) — GS 10 → 10 — nessun numero cambia verso il basso; `pf-dado` ricostruito dai tiri dell'export.

<!-- storico -->
- era: senza `pf-dado`, tolto da `conformita_statblocchi.py` perché portava «1d8+3» (il danno del martello) e la classe di prestigio non è SRD.
- era: colpo di scudo +8/+3, dall'export, che lo conta come seconda arma con le penalità del combattimento a due armi; da solo fa +12/+7.
- era: «⚠ la CA di contatto suggerisce Des 10, la fonte dice 8», nella marca di `genera_attributi.py`: la differenza è l'anello di protezione +1.
<!-- /storico -->
