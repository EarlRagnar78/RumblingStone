---
name: mappe-scala-reale
description: Regole di scala delle mappe (oggetti a misura reale, simbolo 🎪, scala nell'intestazione) e stato del rifacimento del 2026-10-21 (PR #261, #262)
metadata:
  type: project
  modified: 2026-10-21T20:51:38.110Z
---

2026-10-21 Jfs: le mappe avevano scale assurde (tenda di Zog'tar a un palo di 6 m larga oltre 50 m, tendine attaccate) e ha chiesto di rifarle con esempi dal web.

[riga riservata · sha256:f986e648]
- PR #262 unita: Campi Drow 1 e 2, Cerchio Sacro (disco di 60 m nelle tre griglie), Campo C, PF-1/3/4, S-2, CM-1, T-2, T-6, fucine M7-D/F, Foresta in Fiamme. collaudo_mappe da 69 a 23 errori.
- Audit e fonti in plans/esperimenti/mappe-campo-2026-10-21/ (AUDIT-SCALE-MAPPE.md, RICERCA-ACCAMPAMENTI.md).
- Regole: oggetti a misura reale, si allarga lo spazio e non l'oggetto; scala scritta nell'intestazione dentro la griglia (altrimenti l'SVG stampa 1,5 m); ⬛ solo muratura, 🟢 solo creature; un palo da 6 m regge al più ~9-10 m.
- Aperti: Hammerfist e 1A-3/MAPPA 1 di ARC-08 passati al thread ARC-08; T-3 (bassa); [INFERRED] colmo a due travi in M7-C, PF-1 storica (vale S-2), i 🌳 della Foresta in Fiamme letti come treant.
- 2026-10-22: standard ADR-0098 su main (PR #265, scripts/qualita_mappe.py, voto 0-100, CI non bloccante). Quote Hammerfist (Jfs via thread ARC-08), uguali nelle due epoche: piana 870 m s.l.m. (=0), ripiano +80 (950: nel ≈372 spianata degli arieti nuda, nel 1372 cancello), cortile +100 (970: duello M7-B / cortile interno), torre nord e cittadella +120 (990); campi a 500 m-1 km, tornanti. Le quote s.l.m. sono [INFERRED]. PR #266 (8 mappe peggiori a 96-100, nuova CM-2), #267 (quote M7, taglie in metri), #268 (ingressi distinti solo a ≥10 passi, metriche --profonde fuori voto) unite il 2026-10-22. Aperto: Foresta di Cristalli Giganti scesa a 97, probabile falso positivo (bordo quasi tutto aperto). PR #269 unita il 2026-10-22 (7f6a3ce): mappa regionale nostra della Cannath Vale col Cannath navigabile fino a Channathgate (quella di antariuk resta intatta, la sua barra di scala è sbagliata di circa ×2), piante in scala di Channathgate (45 ha + 82 ha di sobborghi, ~11.700 ab., persiana), Rethmar (romana, 250 m) e Dauth (città murata su sperone, 530-556 m). Tutte le quote s.l.m. sono [INFERRED]. Generatori fuori repo. Aperti: forma del Campo del Palio (rettangolo vs ventaglio), esagoni del Witchwood in P1B, P3 dice 40 mi invece di 35, Muraglia Nord a sud di Hammerfist sulla regionale mentre M7 mette la montagna a nord.
- PR #271 unita il 2026-10-22 (6122abf): piante organiche (generatore nostro in stile Watabou, fuori repo) scelte da Jfs invece di quelle Watabou. Taglie dal gazzettiere Elsir Vale: Channathgate = Dennovar, la più popolosa (~11.600, città aperta ~150 ha, solo l'arg murato); Rethmar = Brindol capitale (~8.400, 50 ha, impianto della mappa di antariuk, senza fossato); Dauth ~2.650 su 17 ha, 3 porte (nel libro è un borgo di 200). Ricerca in plans/esperimenti/mappe-citta-2026-10-22/. watabou.github.io raggiungibile solo dalle sessioni nate dopo il 2026-10-22 11:45 (nuovo ambiente cloud).
- PR #272 unita il 2026-10-22 (17d0b33): su richiesta di Jfs le tre città una taglia DMG più grandi per reggere l'orda di ~10.000: Rethmar grande città ~18.000 (110 ha, 4,3 km, 95 torri), Dauth piccola città ~7.000 (42 ha, 59 torri; difende solo sud e ovest), Channathgate grande città aperta ~25.000 (~250 ha). Difensori: 0,8 uomini/m di mura, abili 18% [INFERRED]. Manca il numero della guarnigione nanica di Dauth. Generatori v3 nello scratchpad, fuori repo.
Vedi anche [[mappe-contratti-json]].
