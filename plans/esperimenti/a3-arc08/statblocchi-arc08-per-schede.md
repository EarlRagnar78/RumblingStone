# Statblocchi ARC-08: divergenze fra file (per il thread delle schede PNG)

Analisi in sola lettura, 2026-10-16, branch `claude/project-thread-e860p0`
(HEAD b79fcee2). **Elenca, non sceglie**: per ogni blocco riporta i valori
che divergono, con file e riga. La scelta spetta al thread delle schede e al
DM.

Abbreviazioni: **01** = `08_…/ARC08-01-GUIDA-DM.md`, **02** =
`08_…/ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md`, **enc** =
`08_…/hammerfist_encounters-…-final.md`, **L2/L3** =
`08_…/Mappe/Hammerfist-L{2,3}-REVISED-Ultra-Clear.md`, **Lotto-3** =
`08_…/Mappe/_ARCHIVIO/Hammerfist-Lotto-3-FINALE.md`, **DEF-5** =
`07_…/ARC07-DEF-5-RITORNO-HAMMERFIST.md`, **CORR** =
`07_…/CORREZIONE-Boss-Fauci.md`, **B4** =
`07_…/PortaleForgia-P5-B4-CARRYOVER-Forgia-Ricorda.md`.

> ⚠️ **PR #241 non è in questo branch.** I valori di Tempestas sotto sono quelli
> di prima di #241. Dopo il merge, da ricontrollare: 01:443-462, 02:388-410 e
> la menzione in 01:2463, 01:2612, enc:1019, L3.

## Dove puntano le schede del Bestiario oggi

| Scheda | GS / classe nella scheda | Punta a |
|---|---|---|
| `villain/Fauci_di_Palude.md` | GS 15, drago nero adulto avanzato | 02 §1 |
| `villain/Generale_Grimjaw.md` | GS 14, Orog Gue 10 / Signore della Guerra 3 | 02 §1 |
| `villain/Gorthak_il_Trifronte.md` | [RIMANDO] | — |
| `png/Re_Thorek_Hammerfist.md` | GS 16, Gue 15 / Nobile 2 | 01 §PNG |
| `png/Dana_Forgiapietra.md` | GS 14, Chierico 12 / Cantante Divina 3 | 01 §PNG |
| `png/Signore_Ventolesto.md` | GS 8, gufo gigante celestiale | 01 §PNG |
| `png/Orion_Pelleorsa.md` | GS 14, Druido 14 | 01 §PNG |
| `png/Capitano_Lunapiena.md` | GS 10, Ranger 10 | 02 §2 |
| `png/Tempestas/Tempestas.md` | Br 12 / Arcimago 2, GS 14, CA 19 (statblock proprio, 2026-09-24) | — |
| `png/Borin…`, `Dara…`, `Thorin…`, `Nala…` | GS 13/12/12/12 | 02 §3 |

Tutte le schede, salvo Tempestas, sono del 2026-09-17 e dicono «NON
duplicare». Il dossier vero sta quindi in 01 o 02, che però **non concordano
fra loro** (sotto).

---

## Villain e comandanti nemici

### Fauci di Palude (drago nero adulto avanzato, GS 15)

| Voce | Valori e fonti |
|---|---|
| Base | CA 28, PF 312, soffio in linea 14d4, Riflessi CD 29: 01:151-186 = 02:64-119 = CORR:48 e CORR:68 |
| Presenza terrificante | 01:172 «CD 25, <25 DV». Scheda rapida 01:3349-3356: CD 25, atterra sotto i 100 PF, fugge sotto i 50 |
| Incantesimi | 01:178-179 ne ha di più di 02 |
| Soffio a cono | 02:92 come house-rule con nota (errata B5). 01:171 senza nota |
| TS del soffio nella 2B | 01:1680 Riflessi CD 25. **enc:527 Tempra CD 25** |
| PF attuali nel finale | 01:2578 **180/312**. enc:1028 **220/312**. L3 e Lotto-3 **232/312** |
| Carry-over B4 (se si è giocato P5) | 281 PF, presenza CD 23, soffio CD 27, fuga sotto i 75 (B4, mappa in ARC08-10 §4.1) |
| Esito | ramo D10: fugge sotto i 50 PF, muore solo se i PG lo bloccano (02:105-119, L3:633-634). Lotto-3:440-492 lo fa morire per Aegis Fang (superato) |
| Profilo GS 12 | CORR: 285 PF, 12d4, dichiarato superato |
| Solo in CORR | soffio che scioglie le armature, −2 CA permanente (CORR:71) |

### Cavaliere hobgoblin (Gue 8 / Guardia Nera 2, GS 10)

| Voce | 01 | 02 |
|---|---|---|
| Punire il Bene | 01:204: 2/giorno, +10 ai danni | 02:141: 1/giorno, +2 (errata B5) |
| Aura di Disperazione | 01:205: presente | 02:145-147: rimossa; 02:142 Attacco furtivo +1d6 |

### Generale Grimjaw (Orog Gue 10 / Signore della Guerra 3)

| Voce | Valori e fonti |
|---|---|
| Equipaggiamento | 01:234 scudo con spuntoni e arco composito. 02:178 senza |
| Scheda rapida | 01:3358: GS 14, PF 178, CA 25 |
| Morte | −3 morale all'esercito (scheda del Bestiario) |
| Guardia del corpo | 02:719 (orog che assorbono PFU al posto suo) |

### Gorthak il Trifronte (ettin)

| Voce | Valori e fonti |
|---|---|
| Statblock | 01:255-265: refuso «Ascervare», 6 giavellotti. 02:202-212: «Tre teste», Furia sotto 97 PF |
| Attacco | 02:197: 3 randelli +20/+15/+10 (2d6+9). enc:360: «+20/+15/+10 2d6+9» |
| Scheda rapida | 01:3367-3374: PF 195, CA 22 |
| Esito | resa o morte, a scelta dei PG (L3:637) |

---

## Alleati

### Re Thorek Hammerfist

| Voce | Valori e fonti |
|---|---|
| PF | 195 ovunque (01, L2:643) |
| Talenti | solo nella 01. 02 non li ha |
| Dopo il soffio | 01:1738: −80 PF, Costituzione ridotta. **DEF-5 §0-bis: stabilizzato a 8 pf, esausto, −6 For/Des, non combatte** (D77, 2026-10-12). 01:2753 (4C): «miracolosamente guarito». Compatibili solo se fra 3B e 4C c'è la cura di Dana: DEF-5 la rimanda all'ARC-08 |
| Nome | Thorek (re) ≠ Thorik (PG): INDICE:42. Lotto-1 «Re Thorek XIII» |

### Madre Superiora Dana

| Voce | Valori e fonti |
|---|---|
| Classe | 01:298: Chierico 12 di Moradin / Cantante Divina 3, LI 15 (come la scheda del Bestiario) |
| Ruolo | A3 (A6) la vuole **senza cure** in scena. DEF-5 le assegna «la cura vera» di Thorek nell'ARC-08 |

### Cantitrici della Pietra

| Voce | Valori e fonti |
|---|---|
| Classe | 01 e 02: Chierico 8 / Bardo 4, GS 11, PF 98 |
| Variante | A3 (A7): in DEF-5 sono chieriche di 5° |
| 02:282-283 | Ispirare coraggio +2; Scacciare 5/giorno +3 |

### Signore Ventolesto (gufo gigante celestiale) e gufi

| Voce | Valori e fonti |
|---|---|
| PF | 95 in 01 e 02. enc:1033: «PF 95 ciascuno, +4» (anche per i 2 gufi) |
| Punire il Male | Lotto-3 e L3: +10 |
| Perdite nell'epilogo | enc:1287-1291: 1 gufo. 01:2923-2925: 2 gufi |

### Capitano Lunapiena e ranger elfici

| Voce | Valori e fonti |
|---|---|
| Lunapiena | 02:325-357: Ranger 10, PF 88, CA 19, arco +17/+17/+12, nemico prescelto Draghi +4 / Giganti +4 / Orchi +2. Nella 01 è un paragrafo |
| Corno | 02:344: evoca 2d4+2 barbari di 4° livello. 01:2711: «berserker celestiali per 1 ora» |
| 12 ranger elfici | 01:400-415: Ranger 8, PF 68, CA 18 |
| Archi | L3: +15, 1d8+6 +2d6 (bane) |
| Perdite nell'epilogo | enc: 3 ranger feriti. 01: 5 ranger |

### Orion Pelleorsa (umano, Druido 14)

| Voce | Valori e fonti |
|---|---|
| PF | 98 (01, 02) |
| Forma d'orso | 02:373: artigli +19 (1d8+9), morso +14 (2d8+4), Lotta +24. 01:2604 ed enc:1038: «PF 150, CA 22, +18/+18/+13» |
| Lotta su Fauci | L3: +18/+20. Lotto-3: Grapple +18. 02: +24 |
| Identità | Orion ≠ Hella (ERRATA epica §4) |

### Maestro Tempestas (prima di #241)

| Voce | Valori e fonti |
|---|---|
| Classe | Bardo 12 / Arcimago 2, PF 84, GS 14 (01:443, 02:388). Scheda del Bestiario: CA 19 |
| Musica | 02:402: Ispirare coraggio +3 |
| Tempesta | L3: «LI 20», Tempesta 10d6. 01:2612: 8d6 + 6d6 a catena. 01:2463 ed enc:1019: 6d6 per round |

---

## Pregen («Eroi di Hammerfist»)

Fonti: 01:488-619 (completi), 02:419-522 (stampabili, verificati dall'ERRATA
§3), 01:3311-3491 (schede stampabili, duplicato di 02).

| Pregen | Voce | 01:488-619 | 02 / 01:3380-3491 |
|---|---|---|---|
| Borin Ferropugno (Gue 10 / Campione nanico 3) | CA 24 | 01:495 «+10 armatura, +3 scudo» | 02:427 «Arm. +2, Scudo +1, Des +1» (il totale torna, la scomposizione no) |
| Dara Occhiolesto (Ranger 8 / Esploratrice dei picchi 4) | CA 20 | «+4 armatura» | «Cuoio borchiato +2» |
| Nala Cantapietre (Br 8 / Spia maestra 4) | Canto di guerra nanico | 01:602 «+3 morale» | 02:522 e 01:3491 «+1 extra» |
| Nala | Ispirare coraggio | — | 02:515 +2 |
| Thorin Runaforte (Chierico 9 / Sacerdote delle rune 3) | Scacciare | — | 02:486: 7/giorno, +5 |
| tutti | bonus di transizione permanenti | 01:624-631 (A3, A10: da decidere) | — |
| tutti | PX | D9: 0 PX ai Rumbling Stones, bonus in ARC08-10 | — |

---

## Unità (sistema di massa)

I **valori di unità coincidono** fra 01:677-942 e 02:616-802: PFU, DU, morale,
AU e danni di fanteria hobgoblin e orchesca, warrior 3, worg, giganti, ettin,
veterani, balestrieri, élite, ingegneri. Cambia il resto:

| Voce | Valori e fonti |
|---|---|
| Solo nella 01 | statistiche SRD della creatura singola (per esempio gigante delle colline 01:770-779: GS 7, PF 102, Lotta +24) |
| Solo in 02 | movimento e capacità speciali: Furia orchesca, Carica selvaggia, Leadership tattica, orog (02:714: PFU 13, DU 19, AU +12), War Adepts (Palla di fuoco 1d4+1 PFU, CD 16), Guardia del Re, Spezzare la carica |
| Formazione tattica | 01:685: +2 CA se adiacente ad almeno 2 alleati. 02: DU 19 se adiacente ad almeno 1 unità |
| Balista nanica | 02:800: AU +10, 3d8, 120 m. L2 e Lotto-2: +18, 3d8+10 |
| Giganti in 2A | enc: 6. 01 e 02: 8 |
| Troll rigeneranti | solo enc (2A, Fase 2) |
| Bugbear | 01:2152 ed enc:790: furtivo +3d6, Nascondersi +8. 2F (01:1848-1851): Ladro 5 / Assassino 2, GS 7, +5d6, Nascondersi +12 |
| Ondate in 3A | 01:1986-1989: 50/30/20. 01:2038-2041: 30/20/15 |
| Morale «Rinforzi» | 02:567 +3. 01:3228 +2. `mass_combat_guide_Dm`:192 (variante 2d6) +2 |
| Sfera / Apparizione | 01 ed enc: 2d4+4, CD 20. Lotto-3 e DEF-5: 2d8, Volontà CD 25 (DEF-5: +6 morale, immuni alla paura 1 ora) |
| Bonus della carica | 01:2815-2822: 5 voci, +15. 01:2828: «Attacco +23». enc:1189-1199: 6 voci, +23 |
| Strutture | 02:574-611: cancello 800 PF, CA 23, durezza 20; mura 1.800; torri 2.500. L2:171 e COMPLETE: cancello 120 PF, CA 25, durezza 15. Legende: 01:120 mura 1.800 per 30 m; enc:10 mura 180 per 3 m |
