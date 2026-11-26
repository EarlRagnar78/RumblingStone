# Drow Priestess of Lolth 9 (Sajak rituals) [CANONE — DM 2026-05-05]
**Faction**: drow-sonjak | **Role**: divine-caster-boss | **Environment**: underdark/ritual | **CR**: 10 | **Source**: FRCS p.17 drow + PHB Cleric 9 + Lolth faith | **Status**: inferred

```statblocco
gs: 10
taglia: Media
spazio: 1,5 m
portata: 1,5 m (4,5 m con la frusta, anche i quadretti adiacenti, senza minacciare)
ca: 23
ca-dettaglio: (+9 +1 mithral full plate, +3 Dex, +1 light shield)
pf: 40
pf-dado: 9d8
ts: Temp +7, Rifl +7, Vol +10
attributi: For 10 Des 16 Cos 11 Int 10 Sag 17 Car 14
velocita: 20 ft
iniziativa: +3
```

> `attributi` scritti a mano, non generati: serie d'élite della DMG 3.5 p. 110 più la razza drow (SRD), card del DM del 2026-11-20 (vedi il blocco storico in fondo).

**Size/Type**: Medium humanoid (elf) | **HD**: 9d8 (40 HP)
**AC**: 23 (+9 +1 mithral full plate, +3 Dex, +1 light shield) | **Init**: +3 | **Speed**: 20 ft
**Saves**: Fort +7, Ref +7, Will +10 (mantello della resistenza +1 incluso) | **BAB/Grapple**: +6/+6
**Attacks**: +1 snake-headed whip/scourge +7/+2 (1d4+1 + 1d6 poison on bite)
**Abilities**: Str 10, Dex 16, Con 11, Int 10, Wis 17, Cha 14
**Domains**: Evil, Destruction (or Drow, Trickery — FRCS)
**Spells/day (CL 9, CD 13+lvl)**: 0 — 6; 1 — 5+1; 2 — 5+1; 3 — 4+1; 4 — 2+1; 5 — 1+1.
**Typical**: *doom, shield of faith, divine favor*; *hold person, silence, spiritual weapon*; *dispel magic, prayer, summon monster III*; *freedom of movement, divine power, unholy blight (CD 18)*; *flame strike (CD 19), slay living (CD 18)*.
**SR**: 20 | **SLA**: *clairaudience/clairvoyance, detect good, detect magic, dispel magic, levitate, suggestion* (CL 9)
**Feats**: Spell Focus (evocation), Extend Spell, Divine Metamagic (Extend Spell) [Private — Complete Divine], Combat Casting
**Rebuke undead**: 5/day (3 + Cha +2, SRD); con Divine Metamagic ogni incantesimo esteso costa 2 tentativi (1 + l'aumento di livello di Extend Spell) [Private — Complete Divine], quindi 2 incantesimi estesi al giorno
**Notes**: Usata per Notte dei Drow Fase 0 + rituale Spider-Kiss. Matrona Sajak simile ma CR 13-14.

> correzione 3.5 da `scripts/verifica_scheda.py` (2026-11-12, scelta del DM «tenere il numero, dichiarare la sorgente»): *mantello della resistenza +1* aggiunto all'equipaggiamento (SRD, 1.000 mo), perché Volontà +11 superava il conto senza un bonus dichiarato. Il mantello vale per tutti e tre i tiri salvezza: Riflessi +6 → **+7**. Prezzo da ricontrollare col lotto della ricchezza per livello.

> correzione 3.5 da `scripts/verifica_scheda.py` (2026-11-12, lotto 1-bis, regola del DM «il numero più forte, se si ricostruisce»): un'armatura completa +1 dà +9 (8 +1, SRD), non +8; e con Des +3 l'armatura deve essere di mithral (Des massima +3 invece di +1). CA 22 → **23**.

<!-- storico -->
- era: fino al 2026-11-20 For 12 Des 16 Cos 12 Int 14 Sag 19 Car 16 (acquisto a punti 39, sopra i 32 della DMG), pf 49 (9d8+9), Temp +7, Vol +11, Lotta +7, CD 14 + livello, incantesimi di 4° e 5° 3+1 e 2+1 (il 5° era già uno sopra la Tabella del Chierico SRD). Rifatta con la serie d'élite della DMG 3.5 p. 110 più la razza drow (SRD), card del DM del 2026-11-20: Sag 15 (+1 al 4° e all'8°), Des 14, Cos 13, Car 12, For 10, Int 8. Incantesimi al giorno: Chierico 9 SRD 6/4/4/3/2/1 più i bonus di Sag 17 al 1°, 2° e 3°.
- era: fino al 2026-11-26 Temp +6, frusta +8/+3 (1d4+2), *unholy blight* CD 17, *flame strike* CD 18. La verifica del regolista ha rifatto i conti: Tempra +7 (Chierico 9 +6, Cos 11 +0, mantello +1); frusta +7/+2 (1d4+1) con For 10; le due invocazioni prendono il +1 di Spell Focus (evocation), che la scheda aveva fra i talenti e non contava. Card del dm del 2026-11-26 «tutto, anche quelli già su main».
- era: fino al 2026-11-26 cinque talenti (Combat Casting, Spell Focus (evocation), Extra Turning, Divine Metamagic (Extend, CD), Improved Counterspell). Nove DV ne danno quattro (1°, 3°, 6°, 9°) e Divine Metamagic chiede il talento metamagico a cui si applica [Private — Complete Divine]: entrano Extend Spell e Divine Metamagic (Extend Spell), escono Extra Turning e Improved Counterspell. Intimorire non morti 9/giorno → 5. Card del dm del 2026-11-26 «Con Metamagia Divina».
- era: fino al 2026-11-26 GS 11 senza un Boost log. Un drow con classi da PG ha GS pari al livello più 1 (SRD): Chierico 9 = GS 10, come la chierica del Palio, la guardia nobile, l'assassina e Zin'thara. Il file passa da `drow-priestess9-cr11.md` a `drow-priestess9-cr10.md`, perché il validatore vuole il GS nel nome. Card del dm del 2026-11-26 «GS 10 come l'SRD».
<!-- /storico -->
