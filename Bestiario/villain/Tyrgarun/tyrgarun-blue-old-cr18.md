# Tyrgarun — Blue Old Dragon (Sky-Terror of Rethmar) [ACCEPTED — DM-canon 2026-07-02, D11 v2]
**Faction**: red-hand | **Role**: aerial-hazard / grounded-boss | **Environment**: aerial | **CR**: 18 (aerial hazard) → **16–17** (grounded, Fase 4) | **Source**: MM p.71 Blue Dragon Old (SRD 3.5) | **Status**: accepted


```statblocco
gs: 18
ca: 37
ca-dettaglio: (-2 taglia, +29 naturale); contatto 8, colto alla sprovvista 37
pf: 405
pf-dado: 30d12+210
ts: Temp +24, Rifl +19, Vol +23
attributi: For 33 Des 10 Cos 25 Int 18 Sag 19 Car 18
velocita: 12 m, scavare 6 m, volare 45 m (scarsa)
iniziativa: +4
attacchi:
  - Mischia morso +39 (2d8+11); 2 artigli +37 (2d6+5); 2 ali +37 (1d8+5); coda +37 (2d6+16); stritolamento (2d8+16)
voci:
  - Soffio: linea 30 m, 20d8 elettricità, Rifl CD 32 dimezza, 1 ogni 1d4 round
  - Presenza terrificante 72 m, Vol CD 29
  - RI 25; RD 15/magia; immune a elettricità, paralisi e sonno
  - Incantesimi da stregone di 11° livello, al giorno 6/7/7/7/6/3, CD 14 + livello
fonte: corpo del drago blu molto vecchio dell'SRD 3.5 (30 DV) con Cos 25 e soffio 20d8 della scheda; conti rifatti sull'SRD
```

> [CANONE — DM 2026-09-23, D2] correzione 3.5 da `scripts/conformita_statblocchi.py`: **D2, deciso dal DM il 2026-09-23: lotta +46 → +49**: BAB +30 + Enorme (+8) + For 33 (+11). La For 33 la confermano il morso +38 (2d8+11), gli artigli e le ali (+5, metà For), la coda e lo stritolamento (+16, For e mezzo): la lotta era il solo numero che non tornava.

> [GENERATO] `attributi` copiati dalla riga delle caratteristiche di questa stessa scheda da `scripts/genera_attributi.py`.

> **Nota rinomina (2026-07-02, D11 v2 / A7)**: file precedentemente
> `tyrgarun-black-adult-cr13.md` (black adult, riserva). Corretto a **blue Old
> CR 18** per allineamento a **state.md §2.2**, INDICE, ARMATE-SYNC §2.1 e
> STRUTTURA §4-7/§9. Tyrgarun **NON è la cavalcatura di Azarr Kul**: è il
> **terrore dei cieli** della battaglia (D11 v2). Le meccaniche del set-piece
> (hazard di bombardamento, contromosse, inchiodamento del Mythal) vivono in
> `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-RETHMAR-STRUTTURA.md` §9.4 (C1.d).

---

## Profilo AEREO (Fasi 1-3) — *hazard, non incontro frontale*

A CR 18 in volo con Flyby è **imbattibile per design** per un party APL 14: si
gioca come **pericolo ambientale con contromosse quantificate** (vedi STRUTTURA
§9.4), non come statblock da azzerare a iniziativa.

**Size/Type**: Huge dragon (earth)

**Iniziativa** +4

**Difesa** **AC**: 37 (-2 taglia, +29 naturale), contatto 8, colto 37 · **HD**: 30d12+210 (**405 HP**) · **Saves**: Fort +24, Ref +19, Will +23 · **SR (RI)**: 25 | **DR (RD)**: 15/magic | **Immune**: elettricità, paralisi, sonno

**Attacco** **Speed**: 12 m, scavare 6 m, **volare 45 m (scarsa)**
**Attack**: Morso +39 mischia (2d8+11)
**Full**: Morso +39 (2d8+11), 2 artigli +37 (2d6+5), 2 ali +37 (1d8+5), coda +37 (2d6+16), stritolamento (Huge) 2d8+16
**Breath weapon (soffio)**: **linea 30 m, 20d8 elettricità**, Ref **CD 32** dimezza (10 + ½ DV + Cos), 1/1d4 round — *usato dall'alto sui bastioni come hazard di bombardamento*

**Statistiche** **Abilities**: For 33, Des 10, Cos 25, Int 18, Sag 19, Car 18 · **BAB/Grapple**: +30/+49
**Feats**: Flyby Attack, Hover, Wingover, Multiattack, Power Attack, Cleave, Improved Initiative, Snatch, Wingstorm `[Private source — Draconomicon]`, Riflessi Fulminei, Volontà di Ferro — undici, quanti ne dànno 30 DV; gli ultimi due spiegano il Ref +19 della scheda e portano Will a +23
**Skills**: Spot +37, Listen +37, Nascondersi -4 (Huge), Raggirare +25, Concentrazione +30
**Incantesimi** da stregone di 11° livello (Car +4), al giorno 6/7/7/7/6/3, CD 14 + livello, la scheda non li elencava; conosciuti — 0: *individuazione del magico*, *mano magica*, *prestidigitazione*, *lettura del magico*, *suono fantasma*, *messaggio*, *resistenza*, *luce*, *frastornare*; 1°: *scudo*, *dardo incantato*, *colpo accurato*, *allarme*, *ritirata rapida*; 2°: *vedere invisibilità*, *immagine speculare*, *raffica di vento*, *resistere all'energia*, *invisibilità*; 3°: *dissolvi magie*, *velocità*, *fulmine*, *protezione dall'energia*; 4°: *invisibilità superiore*, *pelle di pietra*, *porta dimensionale*; 5°: *muro di forza*, *telecinesi*

**Capacità speciali**
- **Presenza Terrificante**: CD 29 (10 + ½ DV + Car), 72 m (creature con < 30 DV, Will o scosse/panico)
- **Special**: creare/distruggere acqua (a volontà (non SRD: l'SRD dà 3/giorno)), imitazione suoni (a volontà), ventriloquio 3/giorno, terreno allucinatorio 1/giorno, velo 1/giorno (non SRD: l'SRD lo dà dal drago antico)
- **Tempesta d'ali** (Wingstorm) `[Private source — Draconomicon]`: in volo stazionario, raffica che spegne fiamme e abbatte le creature piccole.
> ⚠ Prerequisito: Wingstorm chiede Hover e Flyby Attack, che ha; il *velo* chiede l'età antica (SRD), qui tenuto perché la Fase 4 lo nomina. PF1e: nel Bestiary il blu prende *veil* solo da antico, come in 3.5; anticiparlo di un'età si avvicina, non stravolge.

---

## Profilo A TERRA (Fase 4) — *incontro uccidibile, CR effettivo ~16-17*

Il **Mythal del Circolo degli Otto** (STRUTTURA §7, canone P2D-INTEGRAZIONE
r.201) **gli nega il volo** entro l'area protetta. Senza Flyby/kiting il suo CR
effettivo scende a **~16-17**: epico ma battibile da party APL 14 + alleati.

**Differenze dal profilo aereo:**
- **Speed**: 12 m, scavare 6 m — **niente volo** (Mythal attivo). Se il Mythal cade, torna al profilo aereo.
- **Soffio**: invariato (20d8 linea, CD 32) ma ora **tracciabile a terra**: i PG possono spezzare la linea di tiro con copertura/mura.
- **Malus da Mythal (già canone STRUTTURA §7)**: -2 a tutti i tiri per colpire e TS, niente teletrasporto/*velo* offensivo.
- **Tattica**: vedi **Tattiche** qui sotto, *A terra (Fase 4)*.

---

**Tattiche**
- *Prima del combattimento e durante (profilo aereo, Fasi 1-3)*: resta in **volo alto**, alterna passate di soffio sui camminamenti e Snatch sulle balliste/serventi. **Non atterra mai** finché il Mythal non lo inchioda (Fase 4).
- *A terra (Fase 4)*: costretto alla mischia, usa stritolamento, coda e morso; cerca di sfondare verso il cerchio del Mythal per spegnere l'ancoraggio (se lo raggiunge e uccide un PG-focus, riguadagna il volo).
- *Morale*: Se le contromosse dei PG (balliste, gufi Tiri Kitor, esca) hanno successo ripetuto, sceglie di ritirarsi 1d4 round per ricaricare — *non* di ingaggiare corpo a corpo.
- *Morale — trigger di fuga (nemesi ARC-10)*: se ridotto sotto **80 pf** *prima* che il
  Mythal sia completo, Tyrgarun **fugge** (scavare + volo appena fuori area) e
  diventa una **nemesi ricorrente** per campagne future. Se il Mythal è già attivo
  quando scende sotto 80 pf, **non può fuggire** e va abbattuto.

---

**Cross-ref**: state.md §2.2 · INDICE r.27/443 · ARMATE-SYNC §2.1/§4-Fase1 ·
STRUTTURA §4/§5/§7/§9.4 · `Bestiario/villain/Azarr_Kul/Azarr_Kul/Azarr_Kul.md` (Tyrgarun NON cavalcatura).

Benchmark: PF T1-1 riga 18: CA 37 sopra (33) / pf 405 sopra (300) / attacco +39 sopra (+28) / danno pieno ~100 in linea (100) / CD 32 sopra (25) / TS buono +24 sopra (20). Il corpo è quello del blu molto vecchio dell'SRD (GS 19), con Cos 25 e soffio 20d8: al tavolo vale GS 19-20 in volo. Il file lo tiene a 18, sopra il tetto EL dell'APL 13 (+4 = 17): resta un pericolo da negare, non un nemico da abbattere, finché il Mythal non lo inchioda.

Boost log: conti rifatti sull'SRD del blu molto vecchio, nessun numero sceso — GS 18 → 18 (il corpo vale 19-20) — armatura naturale +29 dell'SRD, CD del soffio da 10 + ½ DV + Cos, due talenti liberi su undici, incantesimi da stregone di 11° livello che il drago ha per l'SRD e la scheda non scriveva.

> <!-- storico -->
> era: CA 35 (+27 naturale), colto 35, da prosa d'origine.
> era: Vol +22, morso +38, artigli, ali e coda +36, da prosa d'origine.
> era: soffio Ref CD 29, presenza terrificante 55 m, da prosa d'origine.
> era: nove talenti su undici, nessun incantesimo, da prosa d'origine.
> <!-- /storico -->
