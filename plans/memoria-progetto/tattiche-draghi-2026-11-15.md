---
name: tattiche-draghi-2026-11-15
description: Thread «Rivedere le tattiche di tutti i draghi» (15/11): inventario dei 7 draghi oltre Skullcrusher, diagnosi e ordine di lavoro
metadata:
  type: project
  modified: 2026-11-15T08:36:48.542Z
---

Richiesta di Jfs del 15/11: tattiche dei draghi da creature più intelligenti del gioco, per carattere, obiettivi, cosa sanno dei PG; diverse per ogni drago; simulate (riuso di /mnt/project-files/duello-skullcrusher-2026-11-15/simula_duello.py).

Inventario e dove stanno le tattiche:
- Fauci di Palude: `08_La Battaglia Di Hammerfist/ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md` §1 (molto canone del 19-20/10).
- Arbitrax/Abithriax: `Bestiario/villain/arbitrax-drago-rosso-cr15.md`.
- Ozyrrandion: `Bestiario/villain/ozyrrandion-drago-verde-cr14.md`.
- Tyrgarun: `Bestiario/villain/Tyrgarun/tyrgarun-blue-very-old-cr19.md` (stregone 11° non usato nella tattica).
- Regiarix: `09_.../Arco-Post-Hammerfist-P2-RHEST-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md` §2, scheda grezza.
- Drago rosso dell'invasione di Dauth: `09_.../Arco-Post-Hammerfist-P2B-Torneo-STATBLOCCHI-COMPLETO.md` §7, scheda grezza.
- Avatar di Tiamat: `Bestiario/villain/Avatar_Tiamat/avatar-tiamat-cr17.md`.
Il thread di Skullcrusher tocca ARC07-DEF-4 Scena 11 e BARILE B13: non toccarli finché la sua PR non è unita.

**Why:** evitare di rifare l'inventario. **How to apply:** ordine scelto: Fauci, poi Tyrgarun, poi gli altri; schede grezze su card prima delle tattiche. Vedi [[skullcrusher-tattica-dinamica]].

15/11 09:00 UTC: simulatore comune `simula_scontri.py` + `profili_draghi.py` in /mnt/project-files/tattiche-draghi-2026-11-15/ (condiviso col thread villain/PNG, che usa profili_villain.py). Proposta in TATTICHE-PROPOSTE.md. Quattro card aperte (prima opzione consigliata): Fauci nuova + fuga 112; Tyrgarun F4 (GS 16-17 non regge: il soffio 20d8 resta); Arbitrax bruto + «vista cieca»→percezione cieca; schede SRD di Regiarix e drago di Vaereth. Nel repo si scrive solo dopo le scelte. Domanda aperta: invocazioni di Artemis (vedere l'invisibile?) non nel repo.

15/11 pomeriggio: le quattro card decise (tutte A) e scritte nella PR #450 in bozza (testa 6b5db8a2, MS-0142 come la #448: chi entra dopo rinumera). Restano senza card: Ozyrrandion tentatore, Avatar di Tiamat vs Mythal, Fauci corrompere acqua/oscurità; domanda su Artemis.
15/11 10:20 UTC: #450 unita (merge 8171db3e sopra c0c5206a, MS-0143; prossima MS-0144). Tre card aperte nel thread dei draghi: Ozyrrandion tentatore (cr14 r.43-50), Avatar di Tiamat punta il Mythal (r.42), Fauci nell'assedio (consigliata: solo oscurità sulle balliste). Se scelte, PR nuova.
15/11 12:30: card Ozyrrandion (A) e Avatar (A) scritte sul ramo v9c5ie (non ancora PR), MS-0145. Fauci: Jfs aveva scelto «oscurità sulle baliste», ma è sbagliata (protegge i nani; baliste +10 vs CA 37 colpiscono solo col 20). Card nuova: oscurità su di sé nell'assedio (consigliata) o nessuna. Regola 3.5: oscurità 20%, la scurovisione non la attraversa (PF1e sì). «Baliste», non «balliste».
15/11 12:47: #451 unita (89721f9d, MS-0145; prossima MS-0146): Ozyrrandion tentatore, Avatar sul Mythal, Fauci oscurità su un sasso nell'assedio. Thread draghi chiuso; unica domanda aperta: invocazione di Artemis per vedere l'invisibile.
15/11 22:45: Jfs: Artemis ha See the Unseen (PortaleForgia-P1 r.249) ma non tutti i draghi lo sanno. PR #457 in bozza (MS-0148): Tyrgarun lo scopre in battaglia (lo sa da subito solo se Ozyrrandion è fuggito e combatte con lui), Ozyrrandion lo sa da Zalkatar, Fauci invariato.
16/11 00:50: #457 unita (merge 145e465f, MS-0153; prossima MS-0154). Ozyrrandion lo sa solo se Sethrax è fuggito dal Torneo (Zalkatar r.67). Resta aperta la card a Jfs sulla frase «parte informato» di r.50 (stessa condizione Sethrax, consigliato sì): se sceglie, PR nuova.
17/11 11:57: card scelta da Jfs (informato solo se Sethrax fugge), #462 unita (ec5fca70, MS-0157; prossima MS-0158). Thread draghi senza nulla aperto.
