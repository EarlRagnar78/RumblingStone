# 📋 Stato dei piani e ordine di chiusura

> **Cos'è**: la fotografia di dove sono i piani **oggi** e in che **ordine** si
> chiudono per non sovrapporsi. Nasce dalla richiesta DM del 2026-09-04 —
> *«documentazione completa su cosa fatto, cosa apre, cosa introduce di nuovo,
> cosa fixa e cosa rimane da fare nel plan, e quale plan chiudere in ordine per
> non sovrapporre i plan»*.
> **Si aggiorna** a ogni lotto chiuso, come `INDEX.md`. Non sostituisce
> `INDEX.md` (che dice *cosa esiste*) né `CHANGELOG.md` (che dice *cosa è
> successo*): questo dice **in che ordine si va avanti, e perché**.

---

## 0 · 🧭 Adesso — l'unica lista viva

> **Perché c'è.** Fino al 2026-09-24 ogni chat aggiungeva in coda una sezione
> «Ripartire da qui» (§6, §7, §8, §9, §10), e ognuna ricopiava la lista di
> quella prima. Per sapere dove si era bisognava leggere l'ultima e fidarsi che
> fosse aggiornata. Da qui in avanti la lista vive **solo in questa sezione** e
> si corregge sul posto: una riga chiusa diventa ✅ con la PR, la riga dopo
> diventa ▶. Le sezioni §6-§10 restano come diario (il perché di ogni scelta)
> e non si aggiornano più.

**Ultimo aggiornamento**: 2026-10-10, nella #230 prima del suo merge: tutti i piani rimisurati contro checklist, CHANGELOG, decisioni, rami e PR (anche chiuse); il piano di recupero della #232 portato qui. Il diario di prima: 2026-10-09, dopo il merge della #227 (`f40ffeb`): R4-ter di [RESA-E-ASSET-DELLE-MAPPE](PIANO-RESA-E-ASSET-DELLE-MAPPE.md) in una PR nuova (D18), gli oggetti di scena del tema texture dai modelli 3D CC0 resi con Blender; codice, guida e secondo emendamento di ADR-0085 fatti, D19-D22 decise; le tessere vere le fa il DM. Lo stato di ogni voce dei due piani delle mappe è nei loro §8, le voci rese inutili dalla #227 in §2-bis qui sotto. Prima: 2026-10-08, sera, secondo messaggio del DM: aperto [RESA-E-ASSET-DELLE-MAPPE](PIANO-RESA-E-ASSET-DELLE-MAPPE.md) con ADR-0085 (font dei volumi e ripiego Noto nelle 47 mappe, 🔺 e 🔷 universali; R4-R6 aspettano D6-D8), scipy nel collaudo (D17) e `@tipo` su tutte le 44 mappe (D18), nella stessa PR #227. Prima, la stessa sera, dopo la #226: fatto V2-quater di [COLLAUDO-MAPPE](PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md) (l'asse delle chiusure, ADR-0083; `tcod` nel collaudo, ADR-0084; D13-D16), e la riga ▶ torna al giro 3 delle letture su DEF-4. Prima, la stessa sera: fusa la #226 ([COLLAUDO-MAPPE](PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md) con ADR-0082, il corredo dei simboli, `collaudo_mappe.py` e il collaudatore); la riga ▶ è l'ordine nuovo del DM: asset di Wesnoth, dipendenze in deroga, orientamento di porte e grate, in una sessione nuova e prima degli altri. Prima, lo stesso giorno: chiuso il lotto mappe D28 (D44-D48), il prossimo lavoro è il giro 3 delle letture su DEF-4. Prima, lo stesso giorno: aperto [AMBIENTE-RIPRODUCIBILE](PIANO-AMBIENTE-RIPRODUCIBILE.md) con ADR-0081, da eseguire dopo il lotto mappe D28, che resta la riga ▶. Prima: 2026-10-07, notte: DEF-4 chiuso nel canone con la #222, i due booklet completi, e il lotto mappe D28 come prossimo lavoro. Prima: 2026-10-07, sera: completata e chiusa la #206 (§15), fuse le PR di Dependabot. Prima: 2026-10-07, con la #218 (i banchi, le monete antiche e le locande di ARC-08 e ARC-09; D41-D43 decise). Il controllo contro le PR ha trovato **una PR mergiata che l'archivio non conosceva**: la #217 (`7343093`, 2026-10-06), il conto della fucina di `ARC07-DEF-4` giocato al tavolo, ora nel CHANGELOG e qui sotto. Le PR aperte rimisurate sono in §3, «Le PR ancora aperte, oggi». Prima: 2026-10-03, dopo il merge della #215 (la tavola di fuori nel Drappo, ADR-0080). Il CHANGELOG del 2026-10-03 porta anche #213 e #214 (le quattro scelte del DM sul foglio di stile; la coda del secondo lettore), che questa fotografia non aveva ancora: la loro coda sta in [PIANO-CODA-DEL-SECONDO-LETTORE](PIANO-CODA-DEL-SECONDO-LETTORE-2026-10.md). Il da fare in ordine per ripartire è in §14.4-ter. Prima: 2026-10-02, dopo il merge della #200 (`5f3cb520`), che ha portato su `main` anche #186-#199, #187 e #188: le sole PR aperte sono #99 e #106, e il da fare è in §14.4-bis. Prima: 2026-09-30 notte, il giro delle quattro letture su DEF-4 e DEF-5 (riga ▶ qui sotto). Prima: 2026-09-30, dopo il merge della #182 (`c80af16`), della #183 (`ac97197`) e della #184. **La fotografia della tornata, con i numeri, i piani aperti e le decisioni per piano, è il §14.** DEF-4 pronto per la prossima serata, ARC-07 al ciclo del master con DEF-5 ai passi 1-6, e la prova cieca di `P-ABITATO` riuscita. Le righe marcate *(PR #183)* e *(30 settembre)* qui sotto dicono cosa è fatto e cosa resta; il dettaglio è in [LETTORE-PLAYTESTER](PIANO-LETTORE-E-PLAYTESTER.md) F3-bis e F4. Prima: il 2026-09-25, dopo il merge delle #170-#174 (`eef36a9`) e della #176, e i lotti 2f e 2g di CICLO-SESSIONE. Cosa ha chiuso la #169 e cosa ha lasciato aperto: §11. La storia delle scelte fuori stampa e il conto delle marcature aperte: §12.

| | Cosa | Classe | Dove sta il dettaglio | Da dove si parte |
|---|---|---|---|---|
| ▶ | **Le PR aperte al 2026-10-10, e cosa resta a ciascuna** *(rimisurate in questa tornata)*: **#231** Python 3.13 in CI (AMBIENTE A2, D7), verde, sblocca la **#228** di Dependabot, rossa finché la #231 non entra · **#216** la revisione della prosa: porta D13, D17, D38 e la *Torre*, ma il suo `ADR-0086` collide con quello di questa PR e va rinumerato a `0087` nel suo ramo prima del merge (D2 di RECUPERO). Un merge di prova sulla #230 (2026-10-10) dà conflitti in `plans/INDEX.md` (2), `STATO-E-ORDINE` (4), `CHANGELOG` e `skills/REGISTRO-NORME-EDITORIALI.md` (1): si risolvono tenendo le righe di `main` e aggiungendo le sue, poi si **rigenerano** §4 (`decisioni_dm.py --emit`) e i conteggi del registro (`validate_norme_editoriali.py`), mai a mano. Le tabelle delle decisioni nei piani si uniscono senza conflitti: D17, D38 e la *Torre* entrano, la D12 chiusa qui resta chiusa · **#232** il piano di recupero: portato nella #230, si chiude come superato · **#106** codice già su `main` in forma nuova, aperta solo per D3 di RECUPERO · **#99** restano i lotti 4g (le schede dei PG, dati nel ramo), 4h e 4i-3 di RIPRESA-PR | G | [PIANO-RECUPERO](PIANO-RECUPERO-DECISIONI-E-REVISIONI-INCOMPIUTE-2026-10.md) · RIPRESA-PR | DM: il merge della #231 e della #216, poi D3-D6 di RECUPERO |
| ⬜ | **Al DM, dalla #230**: la scelta delle texture (`terreni-scelta`) e delle tessere CC0 (`coppie`), la prima immagine di ComfyUI, le celle `[PROPOSTA]` di M7-C, PF-4 e Campo Drow 1 (13 tende su 15), il livello B | G | RESA-ASSET R8 e R4-quinquies · GUIDA-MAPPE §5.1.2 | DM, sulla sua macchina |
| ⬜ | **Due lavori mai arrivati su `main`, non persi**: le schede A4 dei quattro PG (ramo della #99, `fce04907`; lotto 4g di RIPRESA-PR) e la riscrittura di voce di quattro file della sessione Terros (02, 03, 04, 06; 4 rilievi di `validate_prosa`) | K | RIPRESA-PR 4g · CHIUSURA-CATENA lotto P | DM |
| ✅ | I 24 «refusi» di `validate_lingua`: 11 veri corretti | M | §10.1 · #167 | fatto |
| ✅ | I 13 falsi positivi di `validate_lingua`; il passo in CI blocca i refusi (non gli avvisi) | C | CHANGELOG 2026-09-24 · #168 | fatto |
| ✅ | Il falso positivo di `validate_prosa` sul registro delle conseguenze del Torneo di Dauth | C | CHANGELOG 2026-09-24 · #168 | fatto |
| ✅ | **La serata del 2026-09-25**: booklet DM, 13 pagine ✉ per i giocatori e il volume «Il viaggio a mille anni fa»; decisioni S1-S4 del DM; regola 3 degli echi (*un eco non anticipa*, `consequence-echoes.md` §3-ter) | C + G3 | §11.1 · #169 | fatto |
| ✅ | **Nove decisioni del DM** del 2026-09-24 applicate ai master (cugini Thorek e Thorgrim, Frostcleaver, Zeth a mille anni, Balvar INT 16 e SAG 20, Occhio di Ossidiana, Hella come nei ritratti, Therysol donna, Durik 102 pf, preghiera in nanico) | K | regia della serata §7 · #169 | fatto |
| ✅ | **`DEF-4` e `DEF-3` in ordine di gioco**; mappe di `DEF-2` in appendice A4; M7-C nuova, M7-B corretta; discorso di Moradin sui Doni in `DEF-3` §5 | C | §11.1 · `DEF-4` §9 · #169 | fatto |
| ✅ | **Editoria**: una mappa entra in colonna (48 celle) o va su A4 e non va mai a capo; ogni capitolo apre una pagina; immagini fuori da una pagina dedicata sotto i 16 cm. Norma registrata (43 norme) | C + G3 | `rumblingstone-editoria` §2 e §4.4 · #169 | fatto |
| ✅ | **Il controllo a vista di tutti i volumi dopo la regola editoriale della #169**: quindici volumi compilati prima e dopo `a9fe251`. Un difetto veniva dalla #169 (la figura su A4 riservava sempre 21 cm), tre c'erano da prima (codice in linea, righe `____`, tabelle più alte di un foglio). Corretti nel tema e nell'esportatore: sovrapposizioni da 1.474 a 0 | C + G3 | §11.3 · `rumblingstone-editoria` §4.5 | fatto |
| ✅ | **La storia delle scelte non va in stampa**: blocchi `<!-- storico -->` nei sorgenti e attribuzioni di forma fissa tolte dalle due catene con la stessa funzione; la tecnica per fare un booklet, con le regole della #169, scritta come canone | C + G3 | §12.2 · ADR-0069 · `rumblingstone-editoria` §2-bis e §4.6 | fatto: righe con un segnale di storia nei PDF da 257 a 67, storia vera in stampa da 161 righe a 15 dichiarate |
| ✅ | **Le tabelle che in colonna vanno a capo in ogni cella scavalcano le due colonne**, misurate dal tema; marcatore `<!-- tabella: larga -->` / `colonna` per l'autore; i PDF della #169 rifatti con tutte le regole nuove | C + G3 | §13 · `rumblingstone-editoria` §2 e §4.7 | fatto: nei volumi della #169 100 tabelle su 125 erano alte il doppio in colonna; ora 330 tabelle larghe su tutti i volumi, 60% nella stessa pagina |
| ✅ | **Le `[PROPOSTA]` e gli `[INFERRED]` di ARC-07 chiusi**: il DM ha deciso il 2026-09-25, tutto canone; l'equipaggiamento di Hella è quello della sua scheda | K | §12.1 | fatto: 32 marcature dei sorgenti chiuse, 5 restano (tre descrivono una convenzione, due sono i tratti del volto nei prompt) |
| ✅ | **Il giro di merge del 2026-10-02**: la serie AGENT-SKILLS (#186, #189-#199), #187, #188 e la #200 su `main`; restano aperte solo #99 e #106 | C | §14.4-bis · #200 | fatto: il da fare in ordine è in §14.4-bis, a partire dal lotto D13 da approvare |
| ✅ | **Il conto della fucina di DEF-4, come l'ha giocato il tavolo** *(PR #217, mergiata il 2026-10-06 senza riga nell'archivio, aggiunta il 2026-10-07)*: venduto, comprato, il saldo di circa 19.600 mo, le richieste rimaste aperte, l'eco delle reliquie nella Scena 5 | K | `ARC07-DEF-4` Scena 5 · CHANGELOG 2026-10-06 | fatto |
| ✅ | **La configurazione degli agenti** *(2026-10-02)*: `.claudeignore` e `.serena/project.yml` (#201, #202); Serena all'avvio in OpenCode e `test_genera_creatura` pulito (#203); `.mcp.json` collega `scripts/mcp_server.py` in sola lettura, plugin e skill generiche su richiesta (#205). **I due tool che il server scartava** (`campaign_branch`, `dm`: la chiave del sottocomando era «status\|guard\|ensure») si chiamano ora «comando»: 89 su 89 costruiscono la riga, e un test lo tiene (2026-10-07) | C | CHANGELOG 2026-10-02 e 2026-10-07 · `scripts/tools_manifest.py` `mcp_key` | fatto |
| 🙋 | **Al DM: il lotto D13 e la D17 di AGENT-SKILLS** *(dalla #206)*: undici documenti di revisione, 23 modifiche applicabili con `ciclo_prosa.py applica --auto` e quattro da guardare; la D17 decide se i box con «sembra» seguito dalla smentita restano | G | `plans/scrittura/revisioni-D13/LEGGIMI.md` · §14.4-bis | DM: approvare il lotto, rispondere alla D17; agente: `applica` e rimisura |
| 🙋 | **Al DM: quattro incoerenze di canone** trovate dalle corse di L11 e L12 *(dalla #206)*: il carry-over su Fauci nell'handout di DEF-5 §9, le pozioni antiche fra DEF-4 §6 e DEF-5 §0-bis, il «−2 COS» di Thorik in `ARC08-11` contro `state.md`, le tre descrizioni del Rubino | K | `plans/scrittura/RISULTATI.md` «Cosa hanno trovato le corse» | DM: quale versione vince, una riga per incoerenza |
| 🙋 | **Al DM: le D1-D6 di BOX-DI-LUOGO** *(dalla #206)*: il tetto del box di luogo, le dimensioni nella prima frase, il tipo del box, i box già giocati, l'Abbazia *keyed*, il template d'area | G | [BOX-DI-LUOGO](PIANO-BOX-DI-LUOGO-E-AREA-CHIAVE.md) | DM; poi la chat editoriale di quel piano, da B1 |
| ✅ | **Il registro dei rami potato e completo** *(2026-10-07)*: le dieci voci scadute tolte (otto le contava la #206, più due); la #216 registrata come «in volo»; `contenuti_nei_rami --check` verde e senza avvisi, 42 file tutti col loro posto | M | §15.2 · `plans/contenuti-nei-rami.json` | fatto |
| ✅ | **I banchi di ARC-08 e ARC-09** *(PR #218)*: Hammerfist 1372 chiuso durante l'assedio e socchiuso dopo; nove banchi nell'arco 09 con prezzi SRD, quantità, limiti e casse; oggetti maledetti alla Torre e ai campi drow; le monete antiche (§9 dei banchi); le locande quartiere per quartiere. D41 (le reliquie del 372), D42 e D43 decise il 2026-10-07 | C + K | LETTORE F3-ter, F3-quater · `ARC08-17` · `Arco-Post-Hammerfist-BANCHI-E-MERCATI.md` · `Arco-Post-Hammerfist-LOCANDE.md` | fatto. Restano le letture a freddo (`P-ABITATO`) quando i banchi entrano nei master di MASTER-DEF |
| ✅ | **Drappo L9: la tavola di fuori** (`02-GIORNO-2` §2-bis) e [ADR-0080](adr/ADR-0080-le-fonti-di-pubblico-dominio-entrano-come-logica.md): un innesto da una fonte di pubblico dominio, come logica e mai come personaggi. D1-D4 decise il 2026-10-03; nessun altro innesto (Torre Invisibile e Strappo fra le Ere esclusi) | G | [DRAPPO](PIANO-DRAPPO-DI-TARSILIA-STANDALONE-PF1E.md) Lotto 9 · #215 | fatto lo scritto; il collaudo è la riga sotto |
| ⬜ | **Drappo L9, il collaudo**: lettore e playtester a freddo sul §2-bis (passo 6 di ADR-0075, rubrica di LETTORE F5), dry-run cronometrato (sta in cinque minuti per taglio?), booklet `DRAPPO-BOOKLET-DM` da rigenerare con `validate_booklets`, poi il tavolo. La scena resta **alfa** | G | DRAPPO Lotto 9 | agente: due agenti che non vedono il piano; poi il DM al tavolo |
| ✅ | **DEF-4 chiuso nel canone** *(2026-10-07)*: 51 marcature `[INFERRED]` a zero con le risposte del DM (Q1-Q50, D27, D39, D40); nel 372 l'orda è di Zog'tar, non la Mano Rossa; Skullcrusher e Zog'tar Avanzati PF1e senza alzare il GS; le Cronache «quando l'orda calò»; il giro 2 delle quattro letture (il playtester a zero 🔴); Zog'tar Barbaro 14 con mithral e Colpo Devastante, la tenda alta 6 m, chi vola, il drago che arriva al corno, *comando* «Cadi»; **i due booklet completi** (volume del DM 59 pagine, fascicolo dei giocatori 19) in HTML, Homebrewery, PDF da stampa e libretto, con typst 0.15.1 e pdfcpu 0.11.0 installati in locale | K | [LETTORE-E-PLAYTESTER](PIANO-LETTORE-E-PLAYTESTER.md) F3-ter · `esperimenti/def4-giro2/` | fatto: restano le mappe qui sotto e il giro 3 |
| ✅ | **Il lotto mappe D28 di Hammerfist, 372 e 1372** *(2026-10-08)*: M7-A orientata (la postierla sotto la torre est, D44), M7-B col cortile della Scena 11, M7-C con le altezze della tenda; la sezione M7-S e le griglie M7-D (livello −1), M7-E (gallerie di Zeth), M7-F (fucina grande), ognuna nel 372 e nel 1372 (D45-D47). Gli stati del 1372 decisi con la D48: ritirata e riconquista dalle gallerie di Zeth, rune che esplodono su chi non è nano, leoni vuoti | C + K | [LETTORE-E-PLAYTESTER](PIANO-LETTORE-E-PLAYTESTER.md) F3-bis · `07_…/Mappe/ARC07-MAPPE-HAMMERFIST-372-1372.md` | fatto |
| ▶ | **Il giro 3 delle letture su DEF-4**, con le mappe nuove, **un subagente alla volta**; poi DEF-5 | K / C | [LETTORE-E-PLAYTESTER](PIANO-LETTORE-E-PLAYTESTER.md) F3-quinquies | agente, sessione nuova |
| ⬜ | **L'ambiente riproducibile: la macchina come la CI** *(ordine del DM, 2026-10-08; D1-D11 decise)*. La CI è lo standard e la macchina combacia: versione e checksum di ogni binario nel registro, Python 3.13 ovunque, lock con hash, Chrome for Testing fissato, pacchetti di sistema col registro, shellcheck bloccante, pdfcpu provato in CI; Debian stable, Ubuntu 24.04 e Bazzite in distrobox Debian 13. Parte **dopo** il lotto mappe D28 (D4) | C | [AMBIENTE-RIPRODUCIBILE](PIANO-AMBIENTE-RIPRODUCIBILE.md) · [ADR-0081](adr/ADR-0081-il-contratto-d-ambiente.md) | agente, dopo D28: A1, un ramo e una PR per lotto. |
| ✅ | **Gli asset delle mappe, le dipendenze in deroga e l'orientamento** *(ordine del DM, 2026-10-08, sera; fatto la stessa sera)*: porte, grate e sbarre prendono l'asse dai quattro vicini, una funzione per collaudo, renderer ed export UVTT (36 porte disegnate e 13 portali UVTT raddrizzati, 13 SVG rigenerati, `@verso` per i casi ambigui); Battle for Wesnoth entra solo come idea (GPL o CC BY-SA senza crediti per immagine, PNG obliqui su esagoni, nessun concetto che il corpus chieda); sei librerie misurate, vince solo `tcod` (M4 esatta in 0,6 s contro 70 s), obbligatoria nel collaudo per decisione del DM | G → C | [COLLAUDO-MAPPE](PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md) V2-quater, D13-D16 · [ADR-0083](adr/ADR-0083-l-asse-delle-chiusure-si-ricava-dai-vicini.md) · [ADR-0084](adr/ADR-0084-il-collaudo-delle-mappe-e-uno-strumento-di-sviluppo.md) | fatto; al DM restano un `@verso` per le 2 porte ambigue del Portale, D10 e D12 |
| ✅ | **Il collaudo delle mappe, primo giro** *(richiesta del DM, 2026-10-08, da un documento sulla generazione procedurale; PR #226)*: ADR-0082 accettata, D1-D9 e D11 decise; il corredo dei simboli (84, con la regola di posa), `collaudo_mappe.py` in CI e il collaudatore di mappe. Sulle sei griglie D28 della #225: cinque a zero errori, uno su M7-E del 372 | G → C | [COLLAUDO-MAPPE](PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md) V2-bis, V1, V11-bis · [ADR-0082](adr/ADR-0082-la-mappa-si-collauda-come-grafo-prima-che-come-immagine.md) | fatto; restano al DM D10 (i glifi) e D12 (le mappe della #225 al set nuovo, il braciere di M7-E); agente: V2 in avanti, dopo la riga ▶ qui sotto |
| ✅ | **La resa uniforme e il tema texture** *(PR #227, mergiata il 2026-10-09, `f40ffeb`)*: font dei volumi e ripiego Noto nelle mappe, 🔺 e 🔷 universali (R1-R3); `@tipo` su tutte le mappe e scipy nel collaudo (COLLAUDO V2, D17-D18); l'installatore di 2-Minute Tabletop (R4, D9); le sei griglie dell'assedio di Dauth e la scheda della pianta (R5, D10); il tema texture CC0 con 11 texture di Poly Haven e 53 SVG in `rendered-texture/`, velatura 0,30 (R4-bis, D13-D16) | G → C | [RESA-ASSET](PIANO-RESA-E-ASSET-DELLE-MAPPE.md) §8 · [ADR-0085](adr/ADR-0085-la-resa-delle-mappe-e-uguale-su-ogni-macchina.md) | fatto |
| 🟡 | **Gli oggetti di scena dai modelli 3D CC0** *(RESA-ASSET R4-ter, D17-D22, PR nuova come da D18)*: `build_oggetti_cc0.py` e la scena Blender con un lock solo per il set; il renderer usa la tessera dove c'è e il glifo dove no; muretto orientabile, fiammella sopra il braciere; misurato che i modelli coprono il 24% delle celle-oggetto (Poly Haven) e al più il 4% (Quaternius), e il 72% resta glifo per scelta | C | [RESA-ASSET](PIANO-RESA-E-ASSET-DELLE-MAPPE.md) R4-ter · [esperimento](esperimenti/oggetti-cc0-2026-10/RISULTATI.md) · GUIDA-MAPPE §5.1.1 | codice fatto; DM: il giro di prova sui modelli veri |
| 🟡 | **La resa misurata** *(RESA-ASSET R8, D23-D30, ADR-0086; PR #230)*: `misura_resa.py` con il cancello in CI (244 misure di simboli, 20 di terreni), la pagina di scelta del DM (D28: riquadri con il nome, più fonti, «nessuna va bene»), il secondo parere di `piq` sulla sua macchina; M7-C corretta sui 18 rilievi (D29); PF-4 e Campo Drow 1 completati (D30); il tema texture della #227 misurato e tarato: glifi da 4,46 a 7,78 di contrasto mediano (pergamena 7,90), quattro coppie di terreni da separare con texture nuove; ComfyUI in prova | C + G | [RESA-ASSET](PIANO-RESA-E-ASSET-DELLE-MAPPE.md) R8 · [esperimento](esperimenti/misura-resa-2026-10/RISULTATI.md) · GUIDA-MAPPE §5.1.2 | DM: la scelta di texture e tessere nella pagina nuova, la prima immagine di ComfyUI, le celle `[PROPOSTA]` delle tre mappe |
| 🙋 | **Al DM, per le mappe** *(dopo la #227)*: il giro di prova di R4-ter e il confronto su M7-D e sul cortile di ARC07 (GUIDA-MAPPE §5.1.1); lo zip Standard di Quaternius e l'elenco dei suoi modelli; la pianta di Dauth da esportare da Watabou; i tre `[INFERRED]` delle griglie di Dauth (le barelle di C1, la botola di E, il sabotatore di E); il pacchetto base di 2-Minute Tabletop, solo se il tema dipinto interessa ancora | G | [RESA-ASSET](PIANO-RESA-E-ASSET-DELLE-MAPPE.md) §8 | DM; poi l'agente: le tessere nel tema, il peso misurato, la tabella Quaternius |
| ▶ | **Le `[PROPOSTA]` e gli `[INFERRED]` degli altri archi**, un lotto alla volta: 568 in tutto il repo, circa 400 nel contenuto | K | §12.1 | agente: il prossimo lotto è ARC-08 (32), poi ARC-09 (53), `campaign/` (50), `PG/` (22), il Bestiario (212) per ultimo perché è il più grande |
| ✅ | **Le pagine stampabili della Collana dei Semi Eterni e di Durik**, giocatrice e DM, nella famiglia della Corona a 2 gemme; **le sinergie della Collana (F1-F4, la Quaternità) canone** e scritte in ogni pagina di artefatto | K | `PG/Artefatti/ARTEFATTI-MATRICE-VERSIONI.md` §5 · `SINERGIE-ARTEFATTI-MASTER.md` | fatto: decisioni del DM su Treant, tipi dei poteri, scheda tecnica e sinergie applicate a pagine, master, skill di campagna. Chiusi anche gli ultimi tre punti (forma selvatica, ricarica all'alba, momenti degli stati futuri); i poteri degli stati futuri si scrivono in ARC-09. `state.md` §6 non toccato: il canone si scrive sul ramo del gruppo (ADR-0007) |
| ✅ | **I fogli ✉ della serata non portano più l'istruzione di consegna per il DM**: undici fogli la stampavano in testa. Chiusa fra `<!-- consegna -->`; la regia e `DEF-3` ora dicono tutto quello che diceva (la preghiera letta in piedi con la mano sull'Altare, le caselle dei Doni che segna il DM, la seconda metà dell'eco di Hella) | C + G3 | ADR-0069, «Estensione» · `rumblingstone-editoria` §4.5 punto 6 | fatto: `TestIFogliDeiGiocatori` verde su 26 fogli `player` |
| ✅ | **I tratti del volto dei sette PNG di ARC-07 sono canone**, confrontati col ritratto della #172 uno per uno: dove scheda e ritratto non coincidevano il DM ha fatto vincere il ritratto (Durin, Re Thorek, Balvar); per Thorgrim ha corretto il box di `DEF-4` sulle mani aperte verso la luce | K | §12.1-ter | fatto: nessuna `[PROPOSTA]` nei due file dei prompt. L'arma di Durin resta l'ascia doppia dello statblocco, il ritratto ne disegna una a una lama |
| ✅ | **I capitoli da beta del Drappo usciti dal volume del DM** (IP e licenze, playtest alfa, stato del modulo, schede di feedback), su decisione del DM | M | §12.2 | fatto: da 94 a 83 pagine, nessun rimando alla beta nel PDF; i file restano nel repo |
| ✅ | **Gli artefatti a stadi, con le versioni**: audit dei cinque artefatti su master, schede, PDF, moduli giocati e storia; la Corona in quattro stadi e l'Anello in quattro, giocatore e DM; Doni v4-bis su tutte le pagine; registro delle versioni e il suo test | K + C | `PG/Artefatti/ARTEFATTI-AUDIT-POTERI-2026-09-25.md` · ADR-0071 · TRASVERSALE T10 | fatto: Bracieri, Collana e Aegis a stadi (T10-c/d/e) e i prezzi voce per voce (T10-f) restano |
| ✅ | **Le domande sugli artefatti**: tredici risposte del DM applicate il 2026-09-25, D13 e D14 comprese (TRASVERSALE T10-g) | K | audit §7-bis | fatto |
| ✅ | **Tutti gli artefatti a stadi** e i prezzi voce per voce con la tabella SRD (TRASVERSALE T10-c/d/e/f); D15 Aegis S1, D16 Bracieri S3, D17 Collana S2-S3 decise dal DM la sera stessa; tre righe di `state.yaml` con la sua autorizzazione | K | audit §7-ter, §9, §10 | fatto |
| ✅ | **Le schede con l'immagine dentro**, come quelle di prima ma a un decimo del peso: 29 pagine vive su 36, 7 mancanti dichiarate (Aegis Fang e i Bracieri dormienti vanno commissionati) | K + G3 | TRASVERSALE T10-h · ADR-0072 | fatto |
| 🙋 | **Al DM: la bozza del Caos Ultimo** (D13) e due righe per `state.md` sul ramo del gruppo: RD del Manto 5/epico e male, *Fortezza Mentale* di Artemis | K | `04_Anello_S3_Caos_Ultimo_DM.html` · audit §7-bis | DM: approvare o correggere la bozza; `dm.py session end` per `state.md` |
| 🙋 | **Al DM: chiudere la serata del 2026-09-25.** In `campaign/sessions/` non c'è ancora il log: cosa è successo al tavolo lo sa solo il DM | K | regia della serata §6 (il registro) · `rumblingstone-automation` | `python3 scripts/dm.py session end` sul ramo `campaign-group-rumblingstone-dm-gianfranco`, mai su `main` (ADR-0007) |
| ✅ | **Le domande rimaste nei master di ARC-07** (Q1-Q5) | K | §11.2 · §12.1 | fatto: tutte canone il 2026-09-25 |
| 🟡 | **I sette ritratti e le otto tavole sono nel repo** (#172, Canva AI). Restano: gli originali a piena risoluzione al posto delle copie da chat a 533 × 800, e Skullcrusher nel cortile, dove il cane di Hella è sbagliato; il grido *«Baruk Khazâd! Khazâd ai-mênu!»* di Tolkien resta, voluto, in `PortaleForgia-P1` e nell'errata di ARC-08 | | `Immagini/PROMPT-RITRATTI-E-TAVOLE-ARC07.md` §4 | DM: esportare da Canva gli originali, stesso nome di file |
| ✅ | **Il registro dei rami dopo le #170-#174**: i cinque rami passano da «in volo» a «portato» | M | CHANGELOG 2026-09-25 | fatto: 192 riferimenti, 50 file mai arrivati, tutti col loro posto; i 27 in volo sono della #99 |
| ✅ | **Il corredo della serata**: «genera il booklet» fa uscire tutto (booklet del DM, fogli ✉, approfondimento, echi per PG, carte e handout, prompt con il confronto immagine-scheda, PDF controllati). Norma, contratto `*.corredo.json`, `validate_corredo.py` in CI, `dm.py corredo --stampa` | C + G3 | [CICLO-SESSIONE](PIANO-CICLO-DI-SESSIONE-E-MENU.md) 2f · `rumblingstone-automation` | fatto: il corredo di ARC-07 passa, sei box oltre 12 righe spezzati al primo giro; 168 pagine con 0 sovrapposizioni e 0 testo sul bordo |
| ✅ | **Le procedure delle immagini**: Canva AI con il confronto PNG per PNG (`art-direction` §7-bis); la hero map di Canva AI, e quando si butta (`mapmaking` regola 8) | G3 | CICLO-SESSIONE 2f | fatto: due righe nel registro delle norme, una 🟡 e una 🔴 con la ragione |
| ✅ | **La D7 di CICLO-SESSIONE**: PyMuPDF fra le dipendenze di sviluppo. Il DM ha detto sì; la misura del PDF gira in CI | | CICLO-SESSIONE §8 · `requirements-dev.txt` | fatto |
| ✅ | **L'apparato di lavoro fuori dalla stampa, e ogni pagina una volta** ([ADR-0070](adr/ADR-0070-l-apparato-di-lavoro-non-va-in-stampa-e-ogni-pagina-si-stampa-una-volta.md)): quattro classi, `DEF-N` tradotto dall'esportatore, fogli ✉ solo nel volume dei giocatori, rilevatore sul PDF con un tetto per volume | C + G3 | CICLO-SESSIONE 2g · `rumblingstone-editoria` §4.8 | fatto: booklet della serata da 150 rilievi a 0 e da 106 a 90 pagine; il −1000 esce dal corredo |
| ⬜ | **I residui d'apparato del Palio (26) e del Drappo (43)**: patch a `state.md`, procedura degli stemmi, mappa dei file dell'hub. Cosa è apparato in un modulo autonomo | G | CICLO-SESSIONE 2g · `scripts/apparato-residui.json` | agente con il DM: una domanda per gruppo, poi i marcatori, poi si abbassa il tetto |
| ✅ | **L'eco di Hella si consegna nell'Atto I**, decisione del DM del 2026-09-25: lei legge il suo sogno all'inizio del risveglio nella Sala, come dice la regia. `DEF-3` §0 e §7 e l'introduzione della serata si allineano; la seconda metà del foglio le serve al §8 | K | regia della serata §1 · `DEF-3` §0 e §7 · `00-INTRO-DOVE-SIAMO.md` | fatto: booklet e fogli rigenerati, `validate_corredo --stampa` a 0 difetti |
| ✅ | **I fogli di Hella, di Durik e dei Doni allineati alle pagine della #177**: la Collana funziona anche in forma selvatica, Treant per 1 ora e al massimo due, i due insieme spengono l'Evocazione per un mese, i semi tornano all'alba, il Rovo è magico, le sinergie F2 e F3 sulle carte di Tordek e Artemis. Tolto il percorso del repo dalle pagine giocatore di Corona, Anello e Bracieri | K | `09-SCHEDA-HELLA-RISORTA` · `08-SCHEDA-DURIK` · `07b`, `07c` · `DEF-3` §7 e A.2 · pagine degli artefatti | fatto: fogli e booklet rigenerati, `validate_corredo --stampa` a 0 |
| ✅ | **Le Benedizioni di Moradin: vale il PDF**, decisione del DM del 2026-09-25. Tre benedizioni per tutti: Pelle di Pietra (resistenza al fuoco 10 e al freddo 5), Cuore Incrollabile, Vigore della Forgia (3d8+5 a sé, 2d8+2 a contatto). Allineati `DEF-1`, `DEF-2` §7, `DEF-3` §8-bis, `ARC07-HANDOUTS.md` e il suo handout Homebrewery. I file P2-P3 della generazione precedente restano con i numeri vecchi | K | `BenedizioniDiMoradin.pdf` · `DEF-1` §6 · `DEF-2` §7 · `DEF-3` §8-bis · `ARC07-HANDOUTS.md` · `HANDOUT-5-…hb.md` | fatto: booklet rigenerato, nessun 3d8+10 nel PDF |
| ✅ | **La Corona a due gemme: RD 5/epico e male**, decisione del DM del 2026-09-25, come scrive la fonte. La pagina lo spiega: la supera solo un'arma insieme epica e malvagia. ⚠️ `campaign/state.md` §6 dice ancora «RD 5/epico»: la correzione è del DM, a mano | K | `02_Corona_2_Gemme.html` e `_DM` · `00_SCHEDA-GIOCATORE-STATO-ATTUALE.md` · `campaign/state.md` §6 | fatto nelle pagine; `state.md` al DM |
| ⬜ | **Il rilevatore dei box non apre le battute etichettate** (`> **2 di 3 — …** *…`, la forma di Balvar in `DEF-4`): `--box`, `--p1` e `validate_corredo` misurano la prima battuta e non le altre | C | `misura_craft.box_read_aloud` | agente: allargare l'apertura del box e rimisurare; il denominatore di `--p1` sale, i 22 residui vanno riverificati uno per uno |
| ▶ | **Le regole di 3.5 fuori rete**: gli incantesimi nelle esportazioni PCGen di `Bestiario/pregen-pcgen/` | M + G3 | §8.3 | agente: una riga in `dnd-35-srd/references/resources.md` e la sua voce nel registro delle norme |
| ✅ | **Le 120 legature della Corona** (`aﬀresco`) *(fatto il 2026-10-10, #230)*: ﬁ 54, ﬀ 40, ﬂ 17, ﬃ 9 sciolte in 107 righe di `LaCorona_di_Adamantio-DM.md`, nessun'altra riga cambiata | M | §10.1 | — |
| ⬜ | **Due residui editoriali minori**: l'ultima riga dell'indice delle 48 aree dell'Abbazia cade sola a pagina 35; il Palio stampa «Naviga i capitoli qui sopra», che è una frase della catena HTML | M | §11.3 | agente: il primo si prova con una soglia di righe per pagina, il secondo va tolto dall'introduzione del manifest solo nella stampa |
| ✅ | **`fase1.py` e `contenuti_nei_rami` in un clone shallow** non misurano più: lo dicono, e chiedono `git fetch --unshallow`. Il 2026-10-07, shallow, davano 61 file e decine «senza posto»; con la storia intera erano 42 | C | §11.4 · §15.2 | fatto, con il suo test |
| 🟡 | **PI-3, il resto**: la prova del blocco dei segreti (DM), la revisione con l'IA. Le PR di Dependabot su `origin` (#207-#212, dal 2026-10-02) si fondono una alla volta il 2026-10-07, e con le tre azioni alla v7 si chiude anche la riga di Node.js 20 (§15.3) | | PRATICHE PI-3 · §15.3 | DM: la prova del segreto |
| 🟡 | **PI-1 · 4i-3**: la prova della prima PR indietro rispetto a `main` | | RIPRESA-PR §4.11.6 | la prima PR che resta indietro |
| ⬜ | **PI-6**, **PI-2**, **PI-5**, **PI-4** (dopo CICLO D6) | | PRATICHE §5 e §8 | in quest'ordine, una PR ciascuno |
| ⬜ | **Ciclo di sessione e menu**: Fase 0, poi F1-F4. **D1-D6 decise il 2026-09-30**: la cronaca si aggiorna da sola, le alleanze sono un dato, la prosa la scrive l'agente con le skill, menu numerato, le immagini si elencano con le descrizioni (o Canva), BDD senza framework | | [CICLO-SESSIONE](PIANO-CICLO-DI-SESSIONE-E-MENU.md) §5 | agente: la Fase 0 |
| ⬜ | **RIPRESA-PR 4g e 4h**; PR aperte #99 e #106 | | RIPRESA-PR | `python3 scripts/contenuti_nei_rami.py --fetch` |
| ⬜ | **🧲 e 🤖**, e la nota locale di una mappa che non arriva nella legenda | | [RENDER-MAPPE-FEDELTA](PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md) §1 · §9.3 | prima si legge che cosa vuol dire il simbolo in ogni mappa che lo usa |
| ✅ | **I nove rami fusi o portati, cancellati** dal DM il 2026-10-02: i sei di §9.2 più tre fusi o con ogni patch su `main`, con un tag per ramo su `origin` (`archivio/2026-10-02/<ramo>`) e un bundle verificato con `ripristina.sh` *(dalla #206, portata il 2026-10-07)* | | §15 · CHANGELOG 2026-10-02 | fatto: su `origin` restano i rami di §15.2 |
| ✅ | **I master DEF di ARC-08 e ARC-09, le decisioni e la divisione**: D1-D3 decise, 4 master per ARC-08 e 12 per ARC-09 approvati (A1), misure di partenza (A2). *(2026-09-27)* | G + R | [MASTER-DEF](PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md) A1-A2 · PR #182 | fatto |
| ✅ | **Il ciclo del master vale per ogni piano** ([ADR-0075](adr/ADR-0075-il-ciclo-del-master-vale-per-ogni-piano.md)): sette passi in `module-standard`, e ogni piano che riscrive contenuto li cita. *(2026-09-27)* | G3 | MASTER-DEF §1-bis · PR #182 | fatto |
| ▶ | **DEF-1, 2, 3 nella forma del ciclo** *(30 settembre, sera)*: passi 1-4 fatti (scene, contratto, schede, apparati), box letti al tavolo invariati. Letture cieche: DEF-1 lettore 🔴 2, DEF-2 🔴 2 + 2, DEF-3 🔴 1 + 2, DEF-1 playtester 🔴 1; corretti quelli che il testo risolve, le due risposte nuove di DEF-2 sono canone (DM, 30 settembre), gli altri sono D34-D37 | K / C | LETTORE F4 · `esperimenti/f4-def1-def3/` | DM: D35 (il rito che va male), D36 (sei rilievi di regole), D37 (la Sentinella); D34 e D9 sono decise. Poi agente: applica e rilegge |
| ▶ | **ARC-07 al ciclo completo** *(30 settembre)*: DEF-5 ai passi 1-6 (tre scene col contratto, schede di Re Thorek e Madre Dana, box al metro, letture a freddo prima e dopo). Restano il passo 7 di DEF-5 (il quiz, D10) e DEF-1, 2, 3 nella forma | K / C | [LETTORE](PIANO-LETTORE-E-PLAYTESTER.md) F4 | agente: DEF-1 (Varis), poi DEF-2 e DEF-3, `fase1.py` prima di ognuno; una scena già letta al tavolo si converte nella forma, non si riscrive |
| ▶ | **Il giro delle quattro letture** *(30 settembre, notte)*: lettore, playtester, developer e il DM a freddo (rubrica nuova) su DEF-4 e DEF-5; la procedura è il passo 6 del ciclo in `module-standard`. Giro 1: DEF-5 🔴 2 → D38; DEF-4 🔴 3 → uno corretto (chi non vola nel duello), l'orologio è D39, le mappe M7-B e M7-C il lotto D28 | K / C | LETTORE F4 · `esperimenti/giro-def4-def5/` | fatti D39, D40, il lotto mappe D28 (2026-10-08) e il giro 2 su DEF-4; D38 è decisa nella #216, non ancora su `main`. Resta il giro 3 di DEF-4 |
| ✅ | **Il cancello che non vede un master senza `### SCENA`** (zero scene = zero rilievi): la regola C0 di `copertura_scene` | C | LETTORE F6-a · #183 | fatto |
| ⬜ | **A3 di MASTER-DEF**: il canone di ARC-08 contro lo stato del tavolo, dopo F4 | K | MASTER-DEF A3 | agente, poi conferma del DM |
| ✅ | **DEF-4 pronto per la prossima serata** *(PR #183)*: Skullcrusher adulto maturo SRD; Zog'tar Barbaro 11 / Guerriero 4 con l'Ira Superiore e il `Boost log:`; il campo sorvegliato con i numeri SRD; Balvar con le sue abilità; il banco della Scena 5 e la notte già giocata messa in conto; le rune di Zeth; le tacche (3 segnate, il sonno a 6, il ritorno a piedi a 1); il Rubino che appare sull'incudine, si usa una volta sola per il ritorno, e dopo l'uso completa la Corona (+3 e Senzienza in DEF-5 §3); il corno nella custodia incatenata a Grask; le corde a Forza CD 25 | K | LETTORE F3-bis · D5, D6, D11, D13, D18, D20, D22, D24 | fatto: terza lettura cieca lettore 36 → 33 rilievi (🔴 2 → 1, poi chiuso con D22), playtester 23 → 26 (🔴 2 → 0) |
| ✅ | **Niente riposi brevi e lunghi** in 3.5 e PF1e *(PR #183)*: sei righe corrette in DEF-1, 2, 4; il controllo `RIPOSO_5E` in `validate_modules` e `validate_standalone`; la tabella del riposo SRD in `dnd-35-srd` | C + G3 | LETTORE F3-bis | fatto |
| ✅ | **Il banco** *(PR #183)*: la norma `module-standard/references/il-banco.md` (cosa vende e quante, servizi, identificare, tetti, la spezia facoltativa); `copertura_scene` C6 e C7; `P-ABITATO`; §2-bis del kit anti-improvvisazione. Registro delle norme a 68 | C + G3 | LETTORE F3-bis | fatto |
| ✅ | **Le decisioni di DEF-4** *(30 settembre, sera)*: D12 (la pietra di *silenzio*: Brynja resta di 9°, la pietra è all'8°, 8 minuti), D14-D17, D19, D21, D23, D25, D29, D30, e D7 (Balvar runaio di altre fortezze, venuto a Hammerfist per la sua abilità). Applicate a DEF-4 e DEF-5 | K | LETTORE «Decisioni aperte» · PR #185 | fatto |
| 🙋 | **Al DM: le marcature `[INFERRED]` di DEF-5**: in DEF-4 sono **0** dal 2026-10-07 (chiuse con Q1-Q50); in DEF-5 restano **12** (`grep -c INFERRED`, rimisurato il 2026-10-10) | K | LETTORE F4 | DM |
| ✅ | **D27** *(30 settembre, sera)*: chiusa dal DM il 2026-10-07, non c'era niente da considerare | G | §4 | — |
| ✅ | **La quarta lettura cieca di DEF-4** *(30 settembre)*: lettore 45 rilievi (🔴 1, nuovo: la profezia, D33), playtester 29 (🔴 0). Sei 🟠 corretti subito, tre dei quali lasciati dalla D6 | C | LETTORE F3-bis · `esperimenti/def4-seconda-serata/lettura-quarta-*` | fatto |
| ✅ | **La prova cieca di `P-ABITATO`** *(30 settembre)*: il playtester, su DEF-5 senza la tabella *Chi si trova qui*, trova da solo il buco. La domanda funziona e resta com'è | C | LETTORE F4 · `esperimenti/def5-ciclo/` | fatto |
| ✅ | **D31, D32, D33, D34** *(30 settembre, sera)*: l'arrivo nel Cuore della Montagna è fisso e sopra la prima ondata è già passata; il Cuore di Moradin fa parte della Forgia e non entra nel ritorno; le Cronache dicono «quattro eroi» senza «dal futuro»; il salto di DEF-1 da un detrito a metà strada, il Tempio a 40 m, la scala alzata dal Diapason | K | PR #185 | fatto; restano `[INFERRED]` le prove del Diapason |
| 🙋 | **Al DM: D35, D36, D37** *(30 settembre, sera)*: il rito di DEF-3 quando va male; sei rilievi di regole; la Sentinella di DEF-1. Ognuna con la proposta | K | §4 | DM: rispondere col numero |
| ✅ | **D9, i box oltre 12 righe spezzati** *(30 settembre, sera)*: DEF-1 e DEF-2 a zero, nessuna parola cambiata; D34 canone; *silenzio* corretto a 1 minuto per livello (la pietra 8 minuti, la pergamena 3); tolta la riga di Moradin «Siete VOI» dall'handout delle Cronache | K | PR #185 | fatto |
| 🙋 | **Al DM: `state.md` e il Rubino**: §6 lo dà «speso»; ora si usa una volta sola, resta nell'incasso, e dopo l'uso la Corona è intera, +3 e Senzienza (D6). E il log delle serate del 25-27 settembre | K | `campaign/state.md` §6 · `campaign/sessions/` | `dm.py session end` sul ramo del gruppo, mai su `main` (ADR-0007) |
| ⬜ | **Le decisioni prese che non sono su `main`, e i piani mai finiti** *(richiesta del DM, 2026-10-10)*: D17, D38, la *Torre* e il lotto D13 sono chiusi solo nella #216, D12 di RICERCA-MESTIERE solo nella #230, e le due PR creano entrambe ADR-0086. Alcune righe di questa tabella sono ferme: il piano le elenca (§2.5) e L3 le corregge qui | G + M | [RECUPERO-DECISIONI](PIANO-RECUPERO-DECISIONI-E-REVISIONI-INCOMPIUTE-2026-10.md) | DM: D1-D6; agente: L2 e L3 non aspettano nessuno |

Le decisioni aperte al DM sono in §4, generata da `decisioni_dm.py`.

**Il primo comando di una sessione nuova**:

```bash
git fetch --prune origin
python3 scripts/fase1.py <i file che stai per toccare>
python3 scripts/decisioni_dm.py --check
python3 scripts/validate_lingua.py     # 0 refusi attesi: il passo in CI è bloccante
```

Un lotto per PR, salvo lotti piccoli della stessa famiglia che il DM chiede di
tenere insieme (come i due validatori della #168). Dopo il merge il ramo della
sessione si ricrea da `main`.

---

## 1 · Cosa è stato fatto in questa tornata

Sette lotti, dal 2026-09-04. Ognuno con la sua riga nel `CHANGELOG`.

| Lotto | Che cos'era | Esito |
|---|---|---|
| **R1** | Il canone su `main` attribuiva a Tordek un pegno permanente di Thorik, per un mese | ✅ corretto in 12 file, con **E-07c riscritta, E-07e annullata, E-07f nuova** |
| **R2** | `AGENTS.md` elencava **13 skill su 18** e diceva il falso su come si caricano | ✅ [ADR-0041](adr/ADR-0041-instradamento-delle-skill-con-un-gate.md): principio → tabella per compito → inventario, **con un gate bidirezionale** |
| **R5** | Cinque PR aperte senza giudizio | ✅ giudicate una per una **sul codice di oggi**: #109 superata e chiusa, le altre quattro **abbandonate, non superate** |
| **R9** *(2026-09-05)* | Il conto di R5 era **incompleto**: la **#67** non aveva giudizio in nessun documento | ✅ **superata** — su `main` gli stessi hint esistono dal 31 luglio come booklet da manifest, e la PR è **contraria alla norma degli handout**. Da chiudere. Zero issue aperte |
| **R6** | `⬛` valeva insieme *tenda, edificio, dais* su 8.216 celle | ✅ [ADR-0042](adr/ADR-0042-tre-glifi-per-tre-cose.md): tre glifi, e `⬛` **non cambia comportamento** |
| **R7** | La DES di Thorik scritta in modo ambiguo; due clausole della Corona mai decise | ✅ tabella punteggio/modificatore; **+4 CAR e non-rimovibilità confermati** dal DM |
| **F0** | `⛰` disegnato solido e non muro nell'export; `validate_maps` con un punto cieco | ✅ [ADR-0043](adr/ADR-0043-le-montagne-sono-muri-e-nessun-master-esce-dal-controllo.md) |
| **D6** | La griglia di `…P1C` mappa 3: dichiarava 40×40, aveva righe da 24 a 26 celle | ✅ ridisegnata **26×29**, nessuna coordinata del testo cambiata |

### Cosa **fixa**, in una riga ciascuno

- Un PG portava il malus permanente di un altro.
- Un agente poteva pubblicare **senza il gate d'uscita IP**, perché la sua skill non era instradata.
- Su Foundry si **attraversava la catena montuosa** e ci si vedeva attraverso.
- Cancellare tutti gli SVG di un master lo faceva **sparire dalla validazione**.
- Un accampamento drow esportava **2.173 quadretti di muro** dove ci sono tende.
- Una scheda diceva a Tordek di sommare un −2 DES **che non è suo**.
- Quattro mappe di ARC-09 non erano mai state renderizzate.

### Cosa **introduce di nuovo**

| | |
|---|---|
| **4 ADR** | 0041 instradamento · 0042 tre glifi · 0043 muri e controllo · 0044 apertura dei piani |
| **3 gate bloccanti** | skill instradate (bidirezionale) · master senza SVG · renderer/export d'accordo sui solidi |
| **1 glifo** | `🔳` dais |
| **21 test** | in tre file nuovi, di cui **sette provano che i gate mordono** |
| **3 documenti** | il piano di ripresa PR · la ricerca sul mestiere · questo |
| **1 regola di disciplina** | ADR-0044, nella skill dei piani |

### Cosa **apre**

- La **ricerca sul mestiere** (cartografia + illustrazione), col suo audit da eseguire.
- La **coda di riclassificazione** delle 8.216 celle `⬛` — lettura, non sostituzione.
- La **coda delle 6 mappe** con l'intestazione discorde dalla griglia.
- Il **piano di ripresa** delle quattro PR abbandonate, con la Fase 0 già chiusa.

---

## 2 · L'ordine di chiusura, e perché è questo

Il criterio **non** è l'età né la dimensione. È: *si può chiudere senza aprire
un fronte in un altro piano?*

```
  ①  RIPRESA-PR-ABBANDONATE  F1 → F2 → F3 → F4          ← la coda vera
                                       │
                                       └── F3 è il committente della ─┐
                                                                      ▼
  ②  RICERCA-MESTIERE       F1 audit → F2 gate → F3 norme  ← dà i criteri a F3
                                       │
                                       └── eredita le 6 mappe di §6
  ③  VENDIBILITA            bloccata su D1 e sul cancello di qualità
```

| # | Piano | Quando si chiude | Perché non prima |
|---|---|---|---|
| **①** | [PIANO-RIPRESA-PR-ABBANDONATE](PIANO-RIPRESA-PR-ABBANDONATE.md) | F1 → F2 → F3 → F4, in quest'ordine | Ogni fase svuota una PR aperta. Finché sono aperte, **qualunque piano nuovo rischia di riscriverne il contenuto** — è già successo con la #72 |
| **②** | [RICERCA-MESTIERE-CARTOGRAFO-E-ILLUSTRATORE](RICERCA-MESTIERE-CARTOGRAFO-E-ILLUSTRATORE.md) | la **F1 (audit)** può partire subito e in parallelo; la **F2 (gate)** dopo la F1 | La F2 senza la F1 tara le soglie a occhio, e un gate tarato male si disattiva entro un mese. La **F3 della ripresa** (la catena raster) è il **committente**: se parte prima che l'audit dica i criteri, automatizza senza saperli |
| **③** | [PIANO-VENDIBILITA](PIANO-VENDIBILITA.md) | dopo che ① e ② hanno chiuso il cancello di qualità | Il DM ha già deciso: **prima la qualità, poi il mercato**. E il suo blocco **D1** (le immagini non arrivano al volume da stampa) è nel perimetro della ② |
| **④** | I piani d'arco (`REVISIONE-ARC07/08/09`) | quando l'arco si gioca | Gated sul tavolo, non su di noi |
| **⑤** | [PIANO-CICLO-DI-SESSIONE-E-MENU](PIANO-CICLO-DI-SESSIONE-E-MENU.md) | Fase 0 appena il DM risponde a D1-D5; la Fase 1 dopo 4f di ① | Aperto il 2026-09-24 dalla D21: assorbe 4f-5. Partire prima di chiudere 4f vorrebbe dire scrivere il delta allargato su un reset che cambia ancora |

### Le due sovrapposizioni da non creare

⚠️ **Non aprire un piano sulle mappe.** Ce ne sono già quattro più una ricerca.
Qualunque lavoro sulle mappe entra in **②** (qualità del disegno) o in
`PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI` (fedeltà del renderer). La scelta fra i
due è: *è un problema di cosa si vede, o di cosa si perde?*

⚠️ **Non aprire un piano sulle immagini.** L'automazione è **F3 di ①**, il
mestiere è **②**, la norma è la skill `rumblingstone-art-direction`. Tre posti,
tutti esistenti.

---

## 2-bis · Le voci dei piani di mappe che la #227 ha reso inutili

Misurato il 2026-10-09, per R4-ter di RESA-ASSET su richiesta del DM: le voci
dei piani e delle ricerche sulle mappe che il lavoro della #227 ha già fatto
per altra via, o che una decisione di quella PR ha tolto di mezzo. Non si
cancellano dai documenti d'origine, che sono diario: si legge qui che non vanno
più eseguite. Lo stato di ogni lotto vivo è nei §8 di
[RESA-ASSET](PIANO-RESA-E-ASSET-DELLE-MAPPE.md) e di
[COLLAUDO-MAPPE](PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md).

| Documento | Voce | Stato | Perché, e chi la chiude |
|---|---|---|---|
| [RICERCA-GENERATORI-MAPPE](RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md) §2.2, Fase 1 | le tessere CC0 di Kenney come texture dei terreni | ⚰ obsoleta | il tema texture usa le texture CC0 di Poly Haven (D13, `260210e`); Kenney è pixel art da videogioco, lo diceva già la ricerca |
| RICERCA-GENERATORI-MAPPE, Fase 1 | il flag `--style 2mtt` del renderer | ⚰ obsoleta | il tema dipinto passa da un installatore e da una tabella `simbolo → file` (R4, `b8423c1`), ed è un extra per il tavolo, non uno stile del renderer (D13) |
| RICERCA-GENERATORI-MAPPE, Fase 3 | Azgaar per la mappa regionale della Cannath Vale e dei Dalelands | ⚰ obsoleta | D11: la Cannath Vale è la Elsir Vale di *Red Hand of Doom*, canone, e non si genera; Azgaar solo per una regione inventata (R6, in attesa) |
| RICERCA-GENERATORI-MAPPE, Fase 3 | il City Generator per Rethmar e il Palio, export SVG con il seme | ⏭ superata | R5 parte da Dauth (D10) con una scheda committata e `dm.py maps citta` (`b8423c1`); il Palio sta nel modulo autonomo in Golarion, fuori dalla campagna |
| RICERCA-GENERATORI-MAPPE, «Rischi» | il peso degli SVG con le texture incorporate | ✅ misurato | 7,6 MB per i 53 SVG del tema, contro 6,2 della pergamena (`1bbf7bf`) |
| [LEVEL-DESIGN](PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md) A3, P1.3 e la domanda di C2 | il campo `map_kind`, e «Ground Battle → map_kind?» | ⏭ superata | `@tipo <tattica, strategica o schema> <ambiente>` su 50 mappe su 50 (D18 di COLLAUDO, `69930a2`): è il `map_kind`, con un nome solo |
| LEVEL-DESIGN, C2 | «le metriche M1-M9 chiedono il linter di B1, che non c'è» | ⏭ in parte superata | il linter è `collaudo_mappe.py` (V1, `fb55e9f`) con M1, M2 e M4; C2 aspetta ancora V5 (M7, M8) |
| LEVEL-DESIGN, §2-bis | le dipendenze Python a livelli | ⏭ superata due volte | prima da ADR-0037 (solo libreria standard), poi da ADR-0084 (tcod e scipy nel collaudo, fonttools e Pillow solo sviluppo): la regola vigente è ADR-0084 |
| [EDITOR-VISUALE](PIANO-EDITOR-VISUALE-MAPPE-TATTICHE.md) §2 e §6 | «nessun asset di terzi; icone procedurali/originali» | ⚰ obsoleta come premessa | ADR-0085 e i suoi emendamenti ammettono asset CC0 (texture, modelli resi in tessere) e Noto in Apache-2.0; l'editor, quando partirà, legge le stesse tessere |
| EDITOR-VISUALE §2 e §6 | «il repo principale resta puro-stdlib» | ⚰ obsoleta come premessa | ADR-0084: il collaudo vuole tcod e scipy; il renderer resta in libreria standard, ed è questo il vincolo che conta per l'editor |
| [COLLAUDO-MAPPE](PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md) §4 e §6 | i «41 SVG identici»; il rischio sulla licenza dello shadowcasting | ⚰ obsolete | §8 di quel piano |
| [RESA-ASSET](PIANO-RESA-E-ASSET-DELLE-MAPPE.md) R4-bis, il tema texture della #227 | «le texture CC0 rendono le mappe più ricche» | 🔁 rivista con la misura | misurato il 2026-10-09 (ADR-0086): i glifi perdevano contrasto (7,90 → 4,46) e ⛰/🔳 si confondevano (ΔE 1,22). Corretto con alone e velature (`b9ca8da`); quattro coppie di terreni aspettano texture nuove (D27). Le 11 texture restano, ma da oggi ogni texture nuova entra solo se la misura non la boccia e il DM la preferisce |
| [RESA-ASSET](PIANO-RESA-E-ASSET-DELLE-MAPPE.md) D15, D3, D7, D12 | l'IA locale per gli oggetti; il tema dipinto come strada principale; R5 rimandato; lo sfondo dipinto per Foundry | ⏭ superate | da D17, D13, D10 e dal tema texture; §8 di quel piano |

Restano **vive** e non toccate dalla #227: in LEVEL-DESIGN C1, C3 e il ramo D
(D3 ha la base in `render_map_blender.py`); tutto EDITOR-VISUALE da E0; in
[INTEGRAZIONE-PIPELINE-MAPPE](PIANO-INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITA.md) il
collaudo al tavolo (una mappa di Modalità 3 vera, un `.uvtt` in Foundry, che
D12 rende concreto).

---

## 2-ter · Cosa le sessioni hanno usato per decidere senza metterlo nel repo

Il DM, il 2026-10-09: *«tutto quello presente qui sarà riportato nel repo o
rimane soltanto qui? Verificalo anche per le PR mergiate, e reimporta
algoritmi, skill e ruoli usati e poi non inseriti né documentati»*.

**Come si è misurato.**
- I commit: `git log origin/main..refs/pull/N/head` è vuoto per la #226 e per
  la #227, quindi nessun commit è rimasto fuori da `main`. La #228 è di
  Dependabot, aperta.
- Le sessioni: due agenti hanno letto i transcript di quelle due PR. Della #227
  manca un tratto, dalle 13:15 alle 21:19 del 2026-10-08, che `list_events` non
  restituisce; per quel tratto si sono controllati i file nel repo. Della
  sessione di questa PR si è guardato lo scratchpad.
- In nessuna delle tre sessioni è stata chiamata una skill con lo strumento
  `Skill`: le skill si leggevano con `cat`. Un solo ruolo è stato lanciato, il
  collaudatore di mappe, e fu interrotto.

| Da dove | Cosa | Era | Ora |
|---|---|---|---|
| #227 | la griglia delle velature 0,45 / 0,30 / 0,20 su due mappe (D16) | script nello scratchpad | `misura_resa.py velature` |
| #227 | il criterio di scelta delle texture: parole chiave sul catalogo di Poly Haven, i primi otto per download, poi a occhio | non scritto | `build_texture_cc0.py --cerca` e la sua intestazione |
| #227 e questa | il giro di tutti i gate prima del push | una lista copiata a mano, rimasta indietro rispetto alla CI | `gate_locale.py`, che legge `ci.yml` |
| questa | la prova di Blender vero su modelli procedurali (9 tessere in 18 s) | scratchpad | `test_blender_vero.py`, saltato dove `bpy` manca |
| questa | il confronto affiancato prima e dopo, su M7-D | scratchpad | `misura_resa.py affianca` |
| questa | il passaggio delle velature fra 0 e 0,75 per l'alone | scratchpad | ⚰ superato da `misura_resa.py tara` |
| #226 | sette dettagli della rubrica del collaudatore (sola lettura, il canone, le due citazioni, 25 righe, «Verificato senza rilievi») | solo nel prompt | `collaudo-mappe.md` |
| #226 | il collaudatore **mai eseguito fino in fondo** | la tabella di COLLAUDO diceva «fatto» | prima esecuzione vera su M7-C, il 2026-10-09: 0 rilievi dallo strumento, 18 dal collaudatore (10 🟠), Grask compreso. Rapporto in `esperimenti/collaudo-mappe-2026-10/` |
| #226 | la griglia campione dei 20 simboli nuovi | scratchpad | `scripts/tests/fixtures/prova-simboli.md` e `test_prova_simboli.py`, che fissa anche i tre errori del collaudo |
| #226 | gli URL delle fonti di §2.4-§2.5 | non registrati | COLLAUDO §2.5-ter. Nessuna pagina era stata letta per intero, e la *GameMastery Guide* p. 52 non è verificata |
| #226 | Grask e il sacerdote dell'orda nella mappa M7-C | stavano nella bozza D28 ritirata (`5f2e284`) | **aperto, al DM**: DEF-4 mette Grask alla tenda, la mappa su `main` no. Il collaudatore l'ha trovato da solo, con altri 17 rilievi su M7-C |
| #227 | la misura del peso delle tessere webp (128-512 px) e i terreni per mappa | heredoc | numeri in `dipendenze-e-asset-2026-10/RISULTATI.md`; il codice non serve più |
| #226 | il generatore delle griglie della bozza D28 | scratchpad | ⚰ obsoleto con la bozza |

## 3 · Cosa resta da fare, per piano

### ① Ripresa PR abbandonate — F0, F1, F2 ✅; F3 e F4 in corso

- ✅ **F1 · #63** e ✅ **F2 · #52**: chiuse il 2026-09-05, PR chiuse il
  2026-09-11.
- 🟡 **F3 · #106**: 3a-3c chiusi. Resta **3d**, che è la decisione D2 del
  piano: il collaudo SDXL di due immagini accanto alle Gemini, sulla macchina
  del DM.
- 🟡 **F4 · #99**: 4a, 4b, 4c, 4d (4d-1 … 4d-8) e **4e** (una sola via di
  scrittura, 2026-09-24) e **4f** (prodotto e partita, 2026-09-24: la partita
  è un elenco, la cronaca è separata, `dm.py gruppo nuovo`; 4f-5 è passato al
  piano del ciclo di sessione per decisione D21) chiusi. Restano **4g** (schede
  PG a dati), **4h**
  (`groups/<slug>/`, PR dedicata) e **4i**, aggiunto il 2026-09-24 su richiesta
  del DM: il gate vede i percorsi fra backtick in tutti i sorgenti,
  `contenuti_nei_rami.py` dà un posto ai file rimasti nei rami, e la D22 ha
  dato un esito a tutti e quattro. Resta **4i-3**, la protezione di `main`
  (misurato `protected: false`), che il DM ha rinviato. La D24 è chiusa: il
  Collezionista fugge nel Piano del Fuoco, e Varis è il suo informatore.

### ② Ricerca sul mestiere — tutta da eseguire

F1 audit (31 SVG / 17 master + set immagini) · F2 i gate scrivibili · F3 le
norme nelle skill esistenti. **Bloccata su una domanda**: quali mappe pubblicate
sono lo standard.

### Le PR ancora aperte, oggi

*Rimisurato il 2026-10-07 (prima il 2026-09-24) sull'elenco delle PR aperte del repo. La tabella di
prima era ferma al 2026-09-04: dava aperte #63, #52 e #67, chiuse l'11
settembre, e non conosceva la #143.*

| PR | Verdetto | Dove sta scritto | Che si fa |
|---|---|---|---|
| **#143** | contenuto portato su `main` | `PIPELINE-IBRIDE`, riga del CHANGELOG del 2026-09-24 | ✅ **chiusa il 2026-09-24**: il piano è entrato con la #160, l'ADR come **0067** (lo 0050 era occupato) |
| **#160** | lotti 4e, 4f, 4i di RIPRESA-PR, CICLO-SESSIONE, RICERCA-BDD, PRATICHE | CHANGELOG del 2026-09-24 | ✅ **mergiata il 2026-09-24**. Cosa ha lasciato aperto: §7 |
| **#106** | abbandonata, **non** superata | ① F3 · 3d | resta aperta finché il DM non ha fatto il collaudo SDXL (D2): serve la sua GPU |
| **#99** | abbandonata, **non** superata | ① F4 · 4f, 4g, 4h | si svuota: restano tre lotti, e 4h vuole una PR sua |
| **#216** | bozza aperta dal 2026-10-03: la revisione della prosa misurata (D13, D17, D38, D39, la Torre). Fino al 2026-10-07 **non stava in nessun piano** né in questa tabella | da leggere: il suo corpo nomina i piani che tocca | va riletta contro `main` prima di qualunque merge; il DM decide se riprenderla |
| **#206** | lo STATO dopo la #205 | §15 | ✅ **chiusa il 2026-10-07**: il contenuto che valeva ancora è portato su `main` con la PR di §15 (righe di §0, CHANGELOG del 2026-10-02), e le due voci aperte che conteneva sono fatte |
| **#207-#212** | Dependabot dal 2026-10-02: tre azioni della CI (checkout, setup-python, upload-artifact a 7) e tre requisiti pip (pillow, pip-audit, tiktoken) | PRATICHE PI-3 · §15.3 | ✅ **fuse il 2026-10-07**, una alla volta, ognuna con la sua riga nel CHANGELOG |

⚠️ **Nessuna delle due si mergia com'è.** Hanno una base di agosto: se ne porta
il **contenuto**, non i commit, come si è fatto con la #143.

### Code aperte che non sono un piano

| Coda | Quanto | Dove sta scritta |
|---|---|---|
| Celle `⬛` da riclassificare in ⛺/🔳 | **8.216** in 24 file | `LEGENDA-FUNZIONALE-SPEC` §6.2, mappa per mappa |
| Mappe con l'intestazione discorde | **6** | `RICERCA-MESTIERE` §6 |
| `state.md` §1 forward-written | — | lotto **4c** di F4 (era il difetto C1 della #99) |

---

## 3-bis · La classe di ogni lotto rimasto (ADR-0045)

Il taglio segue la **classe di lavoro**, non la dimensione — e serve a rendere
esplicito il compromesso fra costo e qualità, che finora era un default
silenzioso.

| Piano | M meccanico | R ricognizione | C costruzione | G giudizio | K canone |
|---|:---:|:---:|:---:|:---:|:---:|
| ① Ripresa PR — F1 | 2 | — | 1 | 1 | — |
| ① F2 | 2 | — | 1 | — | — |
| ① F3 | 1 | — | 2 | 1 *(il DM)* | — |
| ① F4 | 1 | — | 3 | 1 | **3** |
| ② Ricerca sul mestiere | — | 2 | 1 | 1 | **1** |
| **Totale** | **6** | **2** | **8** | **4** | **4** |

**Come si legge.** Otto lotti su ventiquattro sono **C** — codice con un
contratto chiaro e dei test — e delegabili. Sei sono **M** e non hanno bisogno di
niente più di un gate che dica sì o no. **Otto sono G o K**, cioè giudizio o
canone: quelli restano in sessione principale su `Opus 5` e non si delegano.

⚠️ **Quattro lotti su otto della F4 sono K.** È la misura di quanto la #99 tocchi
il canone, e la ragione per cui non si mergia in blocco.

⚠️ **La tabella è tarata a occhio.** Nessuno ha eseguito lo stesso lotto su due
engine per confrontare: è un'ipotesi dichiarata, da correggere quando i lotti
classificati saranno abbastanza da dire qualcosa.

⚠️ **I 24 non sono tutto il lavoro aperto dell'archivio**, e la mia prima
stesura lo lasciava intendere. Sono i lotti dei **due piani aperti**. Altri
undici documenti contengono in tutto **43 caselle `⬜`** — ma quel numero grezzo
**non è un conteggio di lotti**: separandole sono **29 citate nel testo · 6
celle vuote · 5 lotti veri · 3 glifi di stato** (il «⬜ NON giocato» di un arco
non è un lotto). Contarle bene vuol dire **leggerle una per una**, che è un lotto
**G** e non **R** — e finché non è fatto, «quanto lavoro resta nell'archivio» non
ha una risposta onesta.

⚠️ **Il guadagno vero non è il prezzo per token.** È la colonna «qualità», che
costringe a scrivere il collaudo **prima** di partire — e un lotto la cui
riuscita non si sa descrivere è un lotto tagliato male.

## 4 · Le decisioni ferme al DM

> ⚠️ **Questa tabella è generata**, come `docs/tools/registry.json` lo è dal
> manifest. La fonte sono le tabelle marcate `<!-- decisioni-dm: … -->` dentro i
> piani: si modifica **là**, e qui si rigenera con
> `python3 scripts/decisioni_dm.py --emit`. Il gate `--check` fa rossa la CI se
> le due cose divergono — vedi
> [ADR-0047](adr/ADR-0047-le-decisioni-aperte-hanno-una-casa-sola.md).
>
> ⚠️ **`D<n>` non è un identificatore globale**: otto piani hanno il loro
> `D1..Dn` con significati diversi (in `REVISIONE-ARC07` sono 17 decisioni *già
> prese*). L'identità è la coppia **piano#Dn**, e la colonna «Piano» serve a
> quello, non all'ordine.

<!-- auto:begin key=decisioni-dm -->

**17 aperte** · 208 chiuse — generato da `scripts/decisioni_dm.py --emit`, non si scrive a mano.

| # | Piano | Ambito | Domanda |
|---|---|---|---|
| **D17** | `AGENT-SKILLS` | L12 | **«Sembra» seguito dalla smentita è lecito?** Tre box usano l'apparenza per prepararne la rottura: «quella che sembrava una parete — è una palpebra». Lì «sembra» non esita, è il colpo. *Proposta*: sì, entra in `read-aloud-adulti.md` §1 punto 7 come confine, e il rilevatore salta un «sembra» seguito entro la frase dopo da «invece», «non lo è», «si rivela», «è». I box restano come sono finché il DM non decide |
| **D1** | `BOX-LUOGO` | B3 | **Il tetto del box di luogo: righe, frasi o caratteri?** Oggi la norma è ≤ 12 righe; *Dungeon* conta le frasi; i 300-500 caratteri non hanno fonte. Proposta: si tiene ≤ 12 righe come norma pesata; **≤ 4 frasi** diventa norma **minore** per il solo box di luogo, pesata quando i box dichiarano il tipo (D3), perché oggi colpirebbe anche le aperture di scena da 8-12 righe, che sono legittime; i caratteri restano un indicatore |
| **D2** | `BOX-LUOGO` | B0 | **Le dimensioni nella prima frase del box** («camera quadrata di quaranta piedi»), come nel modello del 2026-10-01, o il paragone di ADR-0014 con le misure nei Dati per il DM? Proposta: resta ADR-0014. Dal modello esterno si prende la struttura (le caratteristiche della stanza fuori dal box), non le misure nella voce |
| **D3** | `BOX-LUOGO` | B2 | **Ogni box dichiara il suo tipo?** Per esempio `**Read-aloud (luogo · Salvatore lead).**`, con i tipi luogo, ingresso, round, rivelazione, chiusura. Sblocca la norma «niente creature nel box di luogo» e le soglie per tipo della tabella del §2 di `read-aloud-adulti.md`, che oggi nessuno può misurare. Proposta: sì, sui master nuovi (S1-S4 di PIANO-MASTER-DEF), scritto da chi scrive il box e controllato da `componenti.py`; non sui DEF già giocati |
| **D4** | `BOX-LUOGO` | — | **I box già giocati fuori dalle nuove misure**: nei DEF di ARC-07, 27 box oltre i 500 caratteri e 61 oltre le quattro frasi. Proposta: non si toccano, come per D9 di PIANO-LETTORE: si spezzano solo se lo chiedi, e senza cambiare una parola |
| **D5** | `BOX-LUOGO` | B5 | **L'Abbazia con le stanze *keyed*** (è la F5 di PIANO-LETTORE, «decidere col DM se ogni stanza vuole un box»). Proposta: sì, un box di luogo breve per stanza nell'ordine di *Dungeon*, quando F5 tocca l'Abbazia; è il banco del repo e già oggi ha 1 box su 11 oltre le quattro frasi |
| **D6** | `BOX-LUOGO` | B1 | **Il template d'area va in `campaign/templates/`**, accanto a quelli di sessione e di mappa, in due versioni (3.5 e PF1e)? Proposta: sì, tutte e due, con la creatura sempre come rimando al Bestiario e mai trascritta |
| **D35** | `LETTORE-PLAYTESTER` | F4 | **DEF-3, il rito quando va male** (i due 🔴 del playtester a freddo). **(a)** Gli Step 1-3 falliti dicono solo «riprova» (−2 cumulativo, 2d6 non letali, −10 min), senza tetto né uscita, e Conoscenze e Utilizzare Oggetti Magici senza gradi non si tirano oltre CD 10. Proposta: ogni step si ritenta al massimo tre volte, ognuna costa 10 minuti; al terzo fallimento lo step riesce lo stesso e il suo esito ❌ della regia resta come prezzo. Chi non ha gradi può usare la prova grezza della caratteristica (SAG per l'Invocazione, CAR per la Stabilizzazione) con −4. **(b)** Con 0 successi allo Step 5 il modulo apre «un'indagine di un'ora» ma non dice cosa fanno i PG trovata la risposta. Proposta: la risposta è occupare il Sud vuoto (un PG, o Therysol); fatto questo lo Step 5 si ritira una volta, con 2 successi su 3 |
| **D36** | `LETTORE-PLAYTESTER` | F4 | **I 🟠 di regole di DEF-1, DEF-2 e DEF-3 che chiedono canone**, raccolti dalle letture a freddo del 2026-09-30 (`esperimenti/f4-def1-def3/`). **(a)** DEF-1: la Benedizione «ignora le penalità» ma la tabella della gravità le applica ridotte (−25%, −5): vale la tabella? **(b)** DEF-1: polvere ogni 10 minuti e stalattiti ogni 15 per tutto il viaggio, o solo come evento del d6? Proposta: solo come evento del d6, più la prova di gruppo per zona. **(c)** DEF-1: la via B contro gli Xorn non ha CD. Proposta: Intimidire o Diplomazia CD 18, come la via C; fallita, gli Xorn non sono accerchiati e si combatte senza il bonus. **(d)** DEF-1: al terzo fallimento di Thorik nel rito lo Smeraldo si incastona comunque? Proposta: sì, e il prezzo sono i malus già scritti. **(e)** DEF-2: il +1 sacro al rito viene dal toccare l'incisione o dal dormire nella Stanza? **(f)** DEF-3: la soglia dei 3 su 3 è «se Thorik rifiuta» nella Quick-Reference e «uno o nessun dono» nel §5: vale il §5? |
| **D37** | `LETTORE-PLAYTESTER` | F4 | **DEF-1 Scena 7: Tordek da solo contro la Sentinella, e se cade?** (🔴 del playtester a freddo). L'anticamera immobilizza Thorik (Forza CD 28, che lui al massimo fa 27) e lascia Artemis prono e indifeso: se Tordek va a 0 pf il modulo non dice cosa succede, e gli altri due passano la scena senza agire. Proposta: la Sentinella è una prova, come Terros è un voto: quando Tordek cade la Magnetite si spegne, la Sentinella torna immobile, e si può ritentare dopo un riposo (−12 h). E per gli altri due un'azione possibile: Thorik può liberarsi con la CD 28 grazie all'aiuto di Artemis (+2), Artemis può parlare, e un suo incantesimo senza componenti somatiche passa |
| **D38** | `LETTORE-PLAYTESTER` | F4 | **DEF-5: quando si gioca la Fase 0 dell'ARC-08?** (🔴 del playtester e del developer a freddo, 30 settembre). DEF-5 fa arrivare i PG nel Cuore della Montagna nell'ultima resistenza, col drago sulle mura e il riposo impossibile; la tabella dei rami prometteva una Fase 0 (consiglio di guerra, preparativi) prima della battaglia. Dopo D31 «sopra la prima ondata è già passata» le due cose non stanno insieme. Proposta: la Fase 0 si gioca **dopo** il drago ai bastioni: prima il Cuore, poi Fauci, poi il consiglio di guerra per le ondate che restano. E l'aura dell'Apparizione segue l'SRD della presenza terrificante: ogni orco tira, chi fallisce (quasi tutti, con Volontà −2 contro CD 25) è in panico, chi fa 20 è scosso; la Scena 3 si gioca con i pochi che restano e con i nemici che arrivano dopo (CM-1) |
| **D3** | `RECUPERO` | L5 | **`RIPRESA-PR#D2` e la #106**: il collaudo SDXL accanto a Gemini tiene aperta la #106 da otto settimane, e il suo codice è già su `main` in forma nuova. La #230 installa ComfyUI e scarica SDXL sulla tua Debian 13. *Proposta*: il collaudo delle due o tre immagini si fa con la #230 installata; la #106 si chiude subito come «contenuto portato», e la D2 resta aperta in RIPRESA-PR senza tenere aperta una PR |
| **D4** | `RECUPERO` | L5 | **`RIPRESA-PR#D11` (ADR-0049, l'AP originale)**: resta aperta dal 2026-09-11, legata a un avvocato IP e a VENDIBILITA, che non è autorizzato. *Proposta*: passa a voce di `adozioni-in-attesa.json` con la condizione «VENDIBILITA autorizzato», e lascia §4 |
| **D5** | `RECUPERO` | L4 | **I ⬜ opzionali dei piani chiusi o fermi**, per gruppo. *Proposta*: (a) chiusi come «non si fa»: AUDIT-SCRIPTS (shellcheck lo fa AMBIENTE A6), IMPORT-ULTRACLEAR (migrazione delle ~30 mappe, ora COLLAUDO-MAPPE), RENDER-FEDELTA (`--strict` default); (b) in attesa con condizione: TRAVASO A6 (quando ARC-07 finisce al tavolo), INTEGRAZIONE (quando c'è Foundry al tavolo), RICERCA-MODULO-PUBBLICABILE B3, C3, D5, RICERCA-TOOL-ESTERNI R1, RICERCA-TOOL-LGM P1-P3, GENERATORE J e K; (c) restano lotti: nessuno |
| **D6** | `RECUPERO` | L3 | **RICONCILIAZIONE-PR-APERTE si chiude come superato?** R3, R6, R7, R8 sono decisi o fatti altrove (§2.3). *Proposta*: sì, ✅ con il rimando a dove sta ognuno |
| **D2** | `RIPRESA-PR` | F3 · 3d | **Riformulata il 2026-09-11: la domanda di prima partiva da un fatto falso.** Diceva *«i diciotto raster si generano sulla tua macchina — quando?»*, ma **esistono tutti e diciotto** (più le due extra), generati dal DM **con Gemini** il 2026-08-15, montati nel modulo, `validate_standalone` verde. `comfyui_batch --lista` dava «6 da fare» per un **disallineamento di nomi**, corretto in questo lotto. La domanda vera è: **l'arte del Drappo è di Gemini, la catena di F3 genera con SDXL in locale — quale delle due è il canone del modulo?** Le differenze che contano (ADR-0019 §2, che questo caso l'aveva previsto): Gemini **non espone il seed**, quindi la serie è irripetibile e il PNG è la sorgente; i suoi termini sono un **contratto che cambia**, verificato per di più su fonti secondarie; SDXL è OpenRAIL++-M, **perpetua**. Di contro la provenienza di Gemini è **firmata C2PA**, e SDXL su queste immagini **nessuno l'ha visto**. 🔵 **Metodo scelto dal DM il 2026-09-11: collaudo prima di scegliere** — la decisione **resta aperta**, si chiude quando il DM ha visto il confronto. Il DM: *«voglio fare prima un collaudo con 2 o 3 immagini e vedere davvero la qualità prima di buttare quelle di Gemini, che sono carine»*. Si generano **due o tre** immagini con SDXL in una cartella a parte, si mettono accanto alle attuali, e A (tenere Gemini) o B (rigenerare tutto) si sceglie **guardando**. Il collaudo chiude anche il buco vero di F3 — la catena mai provata contro un ComfyUI reale — al costo di due immagini invece che diciotto |
| **D11** | `RIPRESA-PR` | F4 · 4b | **L'ADR ex-0018 della #72: recuperato il 2026-09-11 come [ADR-0049](adr/ADR-0049-edizione-commerciale-ap-originale.md), e resta 🔵 *proposta* — non accettata.** Dice che, *se e quando* si pubblica, si pubblica un **AP originale autonomo**, mai un'espansione di RHoD, e porta il **perimetro della v1**. ✅ **I due avvertimenti che bloccavano la domanda sono tolti**: l'audit mancante è stato **rifatto da zero** ([`AUDIT-DERIVAZIONE-IP-CAMPAGNA`](../docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md)), e la tesi **regge sul repo di oggi** — archi 07+08 a **0,2** e **0,7** occorrenze RHoD per 1.000 parole contro il **5,6** dell'arco 09. 🔎 **E la misura ha aggiunto due cose che la #72 non sapeva**: il **`Bestiario/` è a 3,0** e **esce col modulo** — un perimetro che tace su di lui lascia fuori il conto una dipendenza vera — e i **moduli autoconclusivi sono già puliti** (`10-stand-alone` e il Drappo a **0,0**), quindi su quest'asse il prodotto della linea 3 di `PIANO-VENDIBILITA` è pronto. 🔴 **Cosa resta da decidere al DM**: (a) si adotta il perimetro così com'è? (b) il **bestiario** sta dentro o fuori? (c) l'ADR resta proposta finché non c'è la **verifica di un avvocato IP**, che l'audit non sostituisce — conta i nomi, non la struttura |
| ~~D1~~ | `AGENT-SKILLS` | L2 | ✅ **Decisa il 2026-10-01**: sì. Il ricordo dal diario diventa il passo 7 del ciclo per tutti i master; il quiz resta dove una chiave approvata c'è già (DEF-4). ADR-0075 va aggiornato in L2. Era: **Il ricordo del giorno dopo sostituisce il quiz?** |
| ~~D2~~ | `AGENT-SKILLS` | L5 | ✅ **Decisa il 2026-10-01**: la bozza non c'è; L5 parte dalla vista di chi scorre (`skim.py`), poi il DM la rivede. Era: **Dov'è la bozza del DM a freddo?** |
| ~~D3~~ | `AGENT-SKILLS` | L1 | ✅ **Decisa il 2026-10-01**: sì, il passaggio è la scena intera; una scena troppo lunga per una lettura è un rilievo. Era: **Il passaggio è la scena intera?** |
| ~~D4~~ | `AGENT-SKILLS` | L4 | ✅ **Decisa il 2026-10-01**: in avviso finché le letture già fatte hanno l'impronta, poi **bloccante, da solo**: il DM, *«dopo se c'è l'avviso vogliono siano bloccati così si modificano davvero»*. Il cancello passa a bloccante appena il registro è popolato, senza un intervento a mano. Era: **Il cancello del registro parte bloccante o in avviso?** |
| ~~D5~~ | `AGENT-SKILLS` | L7 | ✅ **Decisa il 2026-10-01**: si toglie il comando, resta il rimando; e il controllo resta in CI con un test che lo fa mordere. Era: **La riga `curl … \ |
| ~~D6~~ | `AGENT-SKILLS` | L8, L9 | ✅ **Decisa il 2026-10-01**: partono tutti e due. L8: misure sulle frasi vere del DM e un rilevatore; L9: si prova, poi si applica, *«altrimenti non servono a niente»*. Era: **Partono, o restano proposte?** |
| ~~D7~~ | `AGENT-SKILLS` | L10 | ✅ **Decisa il 2026-10-01**: resta fuori per ora, ma citato e messo in un registro di adozioni in attesa con gli URL e una condizione che, quando si accende, fa partire l'adozione (`plans/adozioni-in-attesa.json`, ADR-0076). Era: **`commit-archaeologist` resta fuori?** |
| ~~D8~~ | `AGENT-SKILLS` | L1 | ✅ **Decisa il 2026-10-01**: due letture: prima a scene, con il diario, poi il modulo intero; la tabella dice in quale è nato ogni rilievo. Il DM: *«leggere la scena la prima volta per capire cosa capisce della scena e poi una seconda lettura che legge tutto intero»*. Era: **Il lettore a freddo legge intero o a scene? |
| ~~D9~~ | `AGENT-SKILLS` | L5 | ✅ **Decisa il 2026-10-01**: proposta accettata: il primo passo obbligatorio al passo 6, il secondo e il terzo in prova finché il DM non giudica `corsa-def5/PREPARAZIONE.md`. Il registro delle letture chiede ora anche la lettura `dm`. Era: **Il DM a freddo entra nel ciclo del master? |
| ~~D10~~ | `AGENT-SKILLS` | L8 | ✅ **Decisa il 2026-10-01**: non si confermano a mano: si verificano con test di correttezza e coerenza, e si confrontano con le pratiche di agentskills.io, `skill-creator` di Anthropic e `run_trigger_evals.py` di awesome-llm-apps (L8-bis). Era: **Gli insiemi attesi delle trenta frasi sono giusti? |
| ~~D11~~ | `AGENT-SKILLS` | L8-bis | ✅ **Decisa il 2026-10-01**: sì. Confine aggiunto e cinque frasi nuove di verifica: le obbligatorie caricate dagli agenti salgono a 45 su 50, le nuove 3 su 3. Il confine non ha avuto effetto sulla frase del Drappo, che il Drappo non lo nomina: corretta l'etichetta. Era: **Il Drappo fuori dalla campagna, nella descrizione di `campaign`?** |
| ~~D12~~ | `AGENT-SKILLS` | L5 | ✅ **Decisa il 2026-10-01**: la preparazione dell'agente non basta. Il DM elenca la sua: risolvere i problemi oltre a vederli, lo stato del gruppo e del mondo, cosa si muove senza i PG, lo stile e le immagini già fatte, le immagini e gli handout mancanti, il flusso, le domande dei PG, i congegni descritti col read-aloud senza anticipare, le interazioni con artefatti e mondo, e il confine fra ciò che sanno i PG e ciò che sa il master. Diventano le undici voci `P-*` di `dm-a-freddo.md`. Era: **La preparazione di `corsa-def5/PREPARAZIONE.md` somiglia alla tua?** |
| ~~D13~~ | `AGENT-SKILLS` | L11 | ✅ **Decisa il 2026-10-01**: sì. «Sembra» e «pare» nei box diventano una norma **minore**, con il rilevatore di `voto_scrittura.py` che passa da indizio a controllo e un lotto che corregge i 34 box; «come se» resta fuori. Era: **«Sembra» e «pare» nei box: norma nuova?** |
| ~~D14~~ | `AGENT-SKILLS` | L11 | ✅ **Decisa il 2026-10-01**: vince P1. Il gesto passa a un PNG o al mondo; P1 si scrive in `read-aloud-adulti.md` §1 e i tre esempi ✅ si correggono. Era: **P1 contro la reticenza sull'emozione** |
| ~~D15~~ | `AGENT-SKILLS` | L12 | ✅ **Decisa il 2026-10-02**: sì, con un documento di revisione in mezzo. Il DM: *«deve proporre un documento che faccia leggere cosa e cambiato rispetto all originale così si possono approvare le modifiche»*, come fra revisore e autore. Le modifiche si approvano una per una, e il testo approvato porta la riga di revisione (ADR-0077). Era: **Fin dove arriva la correzione automatica?** |
| ~~D16~~ | `AGENT-SKILLS` | L12 | ✅ **Decisa il 2026-10-02**: si cercano le soluzioni della comunità con una licenza compatibile e si applicano: CriticMarkup, Humanizer, *Signs of AI writing*, la guida di Anthropic sulle skill (ADR-0077). Era: **Quale «documento migliorato» si migliora con le misure?** |
| ~~D1~~ | `AMBIENTE` | A5c | ✅ **Decisa il 2026-10-08, risposta del DM: sì, col registro di ciò che si installa** (*«magari mettendo un registro di cosa installato così si può disinstallare nella procedura con sudo»*). **Fin dove arriva il setup automatico?** Pacchetti di sistema dopo conferma; il registro segue come Debian e Ubuntu tengono il conto (A5c) |
| ~~D2~~ | `AMBIENTE` | A2 | ✅ **Decisa il 2026-10-08, risposta del DM, poi corretta: una versione sola, vedi D7.** La prima risposta era «CI su 3.11 e 3.13»; il DM l'ha cambiata lo stesso giorno |
| ~~D3~~ | `AMBIENTE` | A3 | ✅ **Decisa il 2026-10-08, risposta del DM: lock con hash** (*«pip deve bloccare le versioni a meno di una correzione di sicurezza»*). La CI è lo standard: un aggiornamento entra prima in CI, poi in locale |
| ~~D4~~ | `AMBIENTE` | tutti | ✅ **Decisa il 2026-10-08, risposta del DM: dopo D28.** Il piano parte dopo il lotto mappe D28; in questa sessione solo piano, ADR e tracciatura |
| ~~D5~~ | `AMBIENTE` | A2, A6 | ✅ **Decisa il 2026-10-08, risposta del DM: Debian stable, Ubuntu stable, Bazzite.** **Quali piattaforme si supportano?** |
| ~~D6~~ | `AMBIENTE` | A5b | ✅ **Decisa il 2026-10-08, risposta del DM: facoltativo** (*«d6 ok facoltativo»*, dopo la spiegazione). **`act` per simulare la CI in locale?** Modulo opzionale del profilo `sviluppo`, versione e checksum nel registro come gli altri binari; il suo verde non sostituisce la CI |
| ~~D7~~ | `AMBIENTE` | A2 | ✅ **Decisa il 2026-10-08, risposta del DM: 3.13 ovunque.** **Quale versione di Python, visto che Debian 13 ha 3.13, Ubuntu 24.04 3.12, Ubuntu 26.04 e Bazzite 3.14?** La versione di Debian stable; si sale quando sale Debian, e la regola vale per Dependabot |
| ~~D8~~ | `AMBIENTE` | A2 | ✅ **Decisa il 2026-10-08, risposta del DM: 24.04, poi 26.04 con una PR.** **Quale Ubuntu stable?** |
| ~~D9~~ | `AMBIENTE` | A5b | ✅ **Decisa il 2026-10-08, risposta del DM: distrobox Debian 13.** **Come si installa su Bazzite, che è immutabile?** |
| ~~D10~~ | `AMBIENTE` | A1 | ✅ **Decisa il 2026-10-08, risposta del DM: Chrome for Testing fissato.** **Da dove viene il Chromium uguale in CI e in locale?** La licenza passa dal gate di `rumblingstone-edizione` prima dell'adozione |
| ~~D11~~ | `AMBIENTE` | A4 | ✅ **Decisa il 2026-10-08, risposta del DM: sì** (*«d11 ok»*). **Gli hook proposti in A4 vanno bene?** `pre-commit` bloccante su shellcheck, compilazione, file pesanti e token; `pre-push` con regola d'oro, verifica rapida dell'ambiente e test; `post-merge` che avvisa quando l'ambiente non combacia più. A4 li costruisce come scritti |
| ~~D1~~ | `CICLO-SESSIONE` | F1 · 1c | ✅ **Decisa il 2026-09-30**: sì: la cronaca si aggiorna da sola, in una regione marcata in coda (estende il vincolo 3 di ADR-0007). Era: **La cronaca si aggiorna da sola?** La chiusura aggiungerebbe una voce costruita dal log (Summary e Key decisions) in una regione marcata di `campaign-chronicle.md`. Oggi il vincolo 3 di ADR-0007 ammette scritture automatiche solo nelle regioni `auto:` di `state.md`: dire sì vuol dire estenderlo alla cronaca. Proposta: sì, in una regione marcata in coda |
| ~~D2~~ | `CICLO-SESSIONE` | F1 · 1b | ✅ **Decisa il 2026-09-30**: sì: le alleanze diventano un dato, con gli atteggiamenti SRD; i valori di partenza li sceglie il DM. Era: **Le alleanze diventano un dato?** Oggi non esistono in `state.yaml`: `state_sync` le riconosce nel testo del log (Dauth, Rethmar, Starsong, i druidi…) e le stampa. Per farne una domanda serve una tabella nuova (fazione, atteggiamento SRD, nota). È canone: i valori di partenza li scegli tu. Proposta: sì, con gli atteggiamenti SRD (ostile … amichevole) |
| ~~D3~~ | `CICLO-SESSIONE` | F2 · 2d | ✅ **Decisa il 2026-09-30**: (a): la prosa di gioco la scrive l'agente con le skill del repo (i nove pilastri di `rumblingstone-narrative-style`), controllata dal DM. Era: **Chi scrive la prosa di gioco che manca** (interazioni dei PNG, testo degli handout, echi)? (a) il DM, o una sessione di agente con le skill, partendo dal brief; (b) una bozza del ponte di ADR-0067, che riapre il lotto E-bis escluso il 2026-07-20. Proposta: (a) adesso, (b) da rivalutare dopo il collaudo |
| ~~D4~~ | `CICLO-SESSIONE` | F3 · 3a | ✅ **Decisa il 2026-09-30**: numerato in testo semplice, per il momento. Era: **Che menu?** Numerato in testo semplice (libreria standard, funziona ovunque e si avvolge facilmente) oppure a schermo intero con `curses` (che su Windows non c'è). Proposta: numerato |
| ~~D5~~ | `CICLO-SESSIONE` | F2 · 2c | ✅ **Decisa il 2026-09-30**: la preparazione elenca le immagini mancanti con la descrizione da dare a un generatore, oppure le fa con Canva come per la serata precedente. Era: **Le immagini mancanti si generano durante la preparazione?** Serve ComfyUI sulla macchina del DM e minuti per immagine. Proposta: la preparazione le **elenca** e lancia `comfyui_batch` solo se il DM lo chiede |
| ~~D7~~ | `CICLO-SESSIONE` | F2 · 2f | ✅ **Decisa dal DM il 2026-09-25: sì**, in `requirements-dev.txt`; lotto 2g. **PyMuPDF in CI?** `validate_corredo --stampa` conta righe sovrapposte e testo sul bordo leggendo il PDF con PyMuPDF, che è AGPL e oggi non è fra le dipendenze (`rumblingstone-editoria` §4). In CI la misura quindi si dichiara saltata, e il PDF difettoso lo trova solo chi esegue il controllo in locale. (a) ammetterla in `requirements-dev.txt`, come pytest: è uno strumento di verifica e non esce dal repo; (b) tenerla fuori, come oggi. Proposta: (a), dopo aver riletto la licenza con `rumblingstone-edizione` |
| ~~D6~~ | `CICLO-SESSIONE` | F0 · 0c | ✅ **Decisa il 2026-09-30**: (a): la pratica senza framework. Era: **BDD con un framework, o solo la sua pratica?** Misurato in [RICERCA-BDD-O-TDD-2026-09](RICERCA-BDD-O-TDD-2026-09.md): `behave` trova gli stessi 16 difetti su 16 del TDD, con +42% di righe, +45% di tempo e 3 MB di dipendenze contro ADR-0037; in cambio il `.feature` si legge senza aprire Python. (a) la pratica senza framework: scenari con identificatore in §4, test che li citano, un gate stdlib che li tiene allineati; (b) `pytest-bdd` con un'eccezione ad ADR-0037; (c) niente, come oggi. Proposta: (a) |
| ~~D1~~ | `COLLAUDO-MAPPE` | V0 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **Quando parte, rispetto a D28 e ad AMBIENTE?** Entrambi aspettano D28. Proposta: D28, poi V1 (piccolo, e collauda le mappe appena fatte), poi AMBIENTE A1-A8, poi V2 in avanti |
| ~~D2~~ | `COLLAUDO-MAPPE` | V3 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **Che simbolo prende il pavimento oggi disegnato con `⬛`** nella Stanza della Corona e nel Cuore della Montagna? Proposta: `⬜` pavimento lavorato per la sala, `🟫` per la caverna; il colore scuro, se serve, lo dà un terreno nuovo in `legend.yaml`, non la ridefinizione locale |
| ~~D3~~ | `COLLAUDO-MAPPE` | V1, V4 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **Quali controlli sono errori e bloccano a tetto**, e quali solo avvisi? Proposta: quelli di ADR-0082 §3 |
| ~~D4~~ | `COLLAUDO-MAPPE` | V9 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **Il generatore di bozze serve?** Proposta: sì, piccolo (BSP e caverne), dopo V6; per gli incontri casuali e i luoghi nuovi dell'arco 09 |
| ~~D5~~ | `COLLAUDO-MAPPE` | V6 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **Come dichiara la taglia una griglia emoji?** Proposta: una direttiva `@taglia <coordinata> ; Grande`, solo dove serve; nel contratto JSON il campo `size` |
| ~~D6~~ | `COLLAUDO-MAPPE` | V0 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **Il linter di level design e `map_kind` passano a questo piano?** Oggi LEVEL-DESIGN li dà a VENDIBILITA, che non li elenca. Proposta: sì, e LEVEL-DESIGN C2 dipende da V1 e V5 |
| ~~D7~~ | `COLLAUDO-MAPPE` | V5 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **La copertura parziale di PF1e** (+2 CA, +1 Riflessi) entra nel livello neutro già ora o col profilo PF1e di VENDIBILITA 1.2? Proposta: col profilo; il collaudo distingue solo i quattro livelli neutri |
| ~~D8~~ | `COLLAUDO-MAPPE` | V2-bis | ✅ **Decisa il 2026-10-08, il DM: anticipato, e il lotto D28 si rifà col set nuovo** (*«check if there are the d28 maps and recreate d28 with new simbol set»*). Era: **Il corredo dei simboli e la regola di posa**: entrano i simboli di §2.3-bis (porte per tipo, porta segreta, saracinesca, grata, finestra, sbarre, scale che salgono e che scendono, botola, pozzo, arredi), ognuno con un campo `posa` che il collaudo verifica? E quando: dopo V2, come nell'ordine di D1, oppure prima di D28, perché le mappe di Hammerfist (fucina, gallerie, cappella, armeria, la sezione a livelli) sono proprio quelle con scale, porte e grate? Proposta: dopo V2; D28 si disegna con i simboli di oggi più simboli locali dichiarati, e V3 li migra. Anticiparlo costa a D28 il tempo dell'arte nuova e del lotto di test |
| ~~D9~~ | `COLLAUDO-MAPPE` | V2-bis | ✅ **Decisa il 2026-10-08, il DM: sì.** Era: **Le porte segrete nella versione per i giocatori**: si disegnano come muro (il giocatore non sa che c'è) e il collaudo boccia una porta segreta che compare in una mappa per i giocatori? Proposta: sì |
| ~~D10~~ | `COLLAUDO-MAPPE` | V2-bis | ✅ **Decisa il 2026-10-08, sera (terzo messaggio), il DM: approvati.** Era: **I glifi del set nuovo**: quelli della tabella di V2-bis? Proposta: sì; se un glifo non si legge bene al tavolo, si cambia lì, prima che una mappa lo usi |
| ~~D11~~ | `COLLAUDO-MAPPE` | V11-bis | ✅ **Decisa il 2026-10-08, il DM: serve un ruolo LLM in più** che controlli che le mappe siano corrette, che gli algoritmi richiesti siano stati usati e che le parti sbagliate siano state corrette (*«it will need another llm role for checking that maps are correct»*). Diventa V11-bis: il collaudatore di mappe |
| ~~D12~~ | `COLLAUDO-MAPPE` | D28, V3 | ✅ **Decisa il 2026-10-08, sera (terzo messaggio), il DM: sì, in un lotto solo.** Fatto lo stesso giorno: collaudo dei sei master da 1 errore e 10 avvisi a 0 errori e 2 avvisi (M4). Era: **Le mappe della #225 passano al set nuovo?** Le cinque `🪜` diventano `🔼`/`🔽` con `@collega`, e il braciere di M7-E in M10 (e i tre gemelli) si sposta in una nicchia del muro, perché oggi chiude la galleria fra la scala e Zeth. Proposta: sì, in un lotto solo, con i sei SVG rigenerati e il collaudo a zero errori |
| ~~D13~~ | `COLLAUDO-MAPPE` | V2-quater | ✅ **Decisa il 2026-10-08, sera, il DM: come proposto.** Era: **Quanto tocca la funzione dell'asse?** Proposta: una funzione, tre lettori (collaudo, renderer, export UVTT); si rigenerano gli SVG, fra cui 4 D28 della #225, master intatti |
| ~~D14~~ | `COLLAUDO-MAPPE` | V2-quater | ✅ **Decisa il 2026-10-08, sera, il DM: come proposto.** Era: **I casi che i vicini non decidono?** Proposta: la direttiva `@verso <cella> ; NS\ |
| ~~D15~~ | `COLLAUDO-MAPPE` | V2-quater | ✅ **Decisa il 2026-10-08, sera, il DM: come proposto.** Era: **Come si usa Battle for Wesnoth?** Proposta: solo l'idea delle regole di terreno, nessun file e nessun simbolo nuovo |
| ~~D16~~ | `COLLAUDO-MAPPE` | V2-quater, V5 | ✅ **Decisa il 2026-10-08, sera, il DM: obbligatoria nel collaudo**, non come proposto. Era: **Come si tratta `tcod`?** Proposta: opzionale per V5, importata nella funzione, con il ripiego esatto e lento in libreria standard. Alternative: obbligatoria nel collaudo (scelta), nessuna dipendenza |
| ~~D17~~ | `COLLAUDO-MAPPE` | V2-quater, V5 | ✅ **Decisa il 2026-10-08, sera (secondo messaggio), il DM: scipy per M1 e M2**, non come proposto. Era: **Quali librerie ammettere, rimisurate sul loro compito?** Proposta: nessuna. scipy entra obbligatoria nel collaudo come tcod; fonttools solo sviluppo, per i font delle mappe (RESA-ASSET). networkx, shapely, hypothesis, resvg-py restano fuori (ADR-0084, emendamento) |
| ~~D18~~ | `COLLAUDO-MAPPE` | V2 | ✅ **Decisa il 2026-10-08, sera (secondo messaggio), il DM: come proposto.** Era: **`@tipo` su tutte le 44 mappe?** Proposta: tipo (tattica, strategica, schema) e ambiente (interni, caverna, esterno, abitato), con l'elenco in `dmcore/legenda.py` e i campi `tipo`/`ambiente` nel contratto JSON |
| ~~D19~~ | `COLLAUDO-MAPPE` | V2, V3 | ✅ **Decisa il 2026-10-08, sera (terzo messaggio), il DM: confermate tutte e tre** (Portale L2 mappa 1 e M7-E nei due tempi: tattica caverna). Era: **Le tre classificazioni dubbie.** Portale L2 mappa 1 (il titolo letto è «[COLONNA K = 15m da Nord]»: tattica caverna?), M7-E nel 372 e nel 1372 (gallerie scavate: caverna o interni? è legato a `🟤` della D12). Proposta: come in `esperimenti/dipendenze-e-asset-2026-10/classificazione-mappe.tsv`, da confermare |
| ~~D1~~ | `DRAPPO-TAVOLA` | L9 | ✅ **Decisa il 2026-10-03** (il DM: *«approvo con tutte le premesse e verifiche che vuoi fare»*): l'innesto nel Drappo parte, con la forma proposta |
| ~~D2~~ | `DRAPPO-TAVOLA` | L9 | ✅ **Decisa il 2026-10-03** (il DM: *«D2 ok»*): le tre correzioni restano. Era: **Confermi le tre correzioni?** Dedotto da me: la scena sta ai Partiti e non alla Cena; l'enigma senza risposta è tolto; le rose dipinte sono tolte. Sono scelte mie, e il DM approvando non le aveva viste |
| ~~D3~~ | `DRAPPO-TAVOLA` | L9 | ✅ **Decisa il 2026-10-03** (il DM: *«d3 ok»*): il foglietto letto a tutti resta nella scena. Era: **Il foglietto letto a tutti è una regola che vuoi?** Dà ai cinque fuori un modo di pesare sulla trattativa di Vanna, ed è l'unica cosa della scena che tocca i Partiti. Alternativa: tavola senza porta |
| ~~D4~~ | `DRAPPO-TAVOLA` | futuro | ✅ **Decisa il 2026-10-03** (il DM: *«d4 non adottarlo»*): le altre due proposte **non si adottano**, e il Drappo resta l'unico innesto. Era: **Le altre due proposte della valutazione** (la Torre Invisibile in ARC-09, liv. 2-3; lo Strappo fra le Ere come appendice opzionale di DEF-5) restano non decise. Vanno decise prima di toccare altri file |
| ~~D1~~ | `LETTORE-PLAYTESTER` | F7 | ✅ **Decisa il 2026-09-27**: la chiave del quiz di DEF-4 è approvata |
| ~~D2~~ | `LETTORE-PLAYTESTER` | F7 | ✅ **Decisa il 2026-09-27**: alla q8 valgono tutti e due i desideri di Balvar (Hammerfist che cade in fretta, e qualcuno che dica che c'era) |
| ~~D3~~ | `LETTORE-PLAYTESTER` | F7 | ✅ **Decisa il 2026-09-27**: il riquadro *La serata in tre frasi* entra in testa a DEF-4 |
| ~~D4~~ | `LETTORE-PLAYTESTER` | F9 | ✅ **Decisa il 2026-09-27**: DEF-4 Scena 11 dice cosa fa chi non vola (preparare un'azione, le corde, le balestre delle mura `[INFERRED]`) |
| ~~D5~~ | `LETTORE-PLAYTESTER` | F3 · F3-bis | ✅ **Decisa il 2026-09-27**: Skullcrusher è un **drago nero adulto maturo** dell'SRD (il DM: *«anziano adulto, con resistenza agli incantesimi e lista degli incantesimi»*). Numeri dalla tabella SRD, raggiunta via Firecrawl: 22 DV, 253 pf, CA 29, RI 21, RD 10/magia, soffio 14d4 CD 26, Presenza CD 23, incantatore di 5°. GS 14 = APL+1. Talenti, abilità e incantesimi conosciuti sono una proposta `[INFERRED]`. Aggiornati il giro del boss, la regia dei round, la scalatura (Vecchio SRD) e i PX (5.400, `[INFERRED]`) |
| ~~D6~~ | `LETTORE-PLAYTESTER` | F3 | ✅ **Decisa il 2026-09-28** (il DM: *«il Rubino appare alla vittoria»*): nessuno lo porta, si forma sull'incudine nel momento della vittoria, e nessun nano del 372 sa spiegarlo. Riscritti il box dell'incudine e le note della Scena 12. Il Rubino **si usa una volta sola**, per il ritorno, e **la Corona si completa dopo l'uso** (precisazione del DM lo stesso giorno): all'incudine la Corona resta a +2 e muta, il +3 e la Senzienza arrivano all'arrivo nel 1372 (`DEF-5` §3, dove sono passati il Momento 2 e il box della corona intera). Allineati `campaign-artifacts.md`, la scheda del giocatore e le pagine S3 della Corona (r7) |
| ~~D7~~ | `LETTORE-PLAYTESTER` | F3 | ✅ **Decisa il 2026-09-30**: Balvar era già runaio, ma di altre fortezze: è arrivato a Hammerfist, giovane, perché era un mastro runaio. La fortezza resta giovane. Era: **La fortezza «giovane, appena eretta» e Balvar che ne è stato il runaio** prima dei bisnonni dei nani di oggi: una delle due cose va cambiata. È aperta anche in `PIANO-CHIUSURA-DEI-MILLE-ANNI` M7 |
| ~~D8~~ | `LETTORE-PLAYTESTER` | F5 | ✅ **Decisa il 2026-09-30**: sì al Riflessi (la caduta nella curva); la Volontà solo se il DM la vuole. Era: **Il Drappo vuole un Riflessi e una Volontà?** `domande_developer` non ne trova nessuno sull'intero modulo. Proposta: il Riflessi sì (la caduta nella curva), la Volontà solo se il DM la vuole in un modulo d'intrigo |
| ~~D9~~ | `LETTORE-PLAYTESTER` | F4 | ✅ **Decisa il 2026-09-30**: si spezzano, senza cambiare una parola. Fatto: sei box di DEF-1 e uno di DEF-2, oggi zero box oltre 12 righe (due erano note per il DM in corsivo e righe `storico` dentro la citazione, uscite dal box). Era: **Nei master già giocati (DEF-1, DEF-2, DEF-3) i box oltre 12 righe si spezzano?** Il passo 5 del ciclo li vuole ≤ 12; DEF-1 ne ha 6, DEF-2 uno. Spezzarli in battute non cambia una parola, ma tocca prosa già letta ai giocatori, ed è la D3 ancora aperta di MESTIERE-BANCHI. Proposta: sì, solo spezzare, come il box di Balvar in DEF-4; mai riscrivere cosa dicono |
| ~~D10~~ | `LETTORE-PLAYTESTER` | F4 | ✅ **Decisa il 2026-09-30**: sì alla proposta: niente quiz sulle conversioni di sola forma di DEF-1, 2, 3; il quiz sui master nuovi e su quelli riscritti nella prosa (ADR-0075). Era: **Il quiz a due agenti (passo 7) va fatto su ogni master?** Ogni quiz chiede una chiave approvata dal DM: con ARC-07, ARC-08, ARC-09 e gli stand-alone sono una ventina di chiavi. Proposta: sì sui master nuovi e su quelli riscritti nella prosa; no sulle conversioni di sola forma dei master già giocati (DEF-1, 2, 3), dove bastano lettore e playtester. Saltarlo lì è una decisione del DM, e va scritta (ADR-0075) |
| ~~D11~~ | `LETTORE-PLAYTESTER` | F3-bis | **I numeri del campo, delle guardie e di Zog'tar.** *(2026-09-27, risposta del DM)*: fuori girano i lupi, dentro le ronde di hobgoblin, orchi e goblin senza lupi; gli sciamani gli esploratori non li hanno visti, ma possono esserci. Scritto in DEF-4 Scena 6: sei squadre di cavalieri su worg sull'anello esterno, ronde di orchi, squadroni hobgoblin e vedette goblin dentro, con i numeri SRD (worg, orco, goblin, hobgoblin); circa quindici sciamani (adepti orchi di 5°) che dopo il corno lanciano *vedere invisibilità*; un sacerdote della Mano (hobgoblin adepto 7, GS 6) nella tenda accanto a Zog'tar, EL della tenda sempre 16. La pattuglia dei tre fallimenti ha i suoi numeri (guerriero 4 SRD). Tutto `[INFERRED]` fino al tuo OK. ✅ **Zog'tar, decisa lo stesso giorno** (il DM: *«lo voglio con l'Ira Superiore, e tosto: deve reggere più di un round»*): Barbaro 11 / Guerriero 4, GS 15, 253 pf (298 in Ira), numeri ricalcolati sull'SRD, `Boost log:` nel Bestiario; la tenda arriva a EL 17, il tetto. E **Balvar**, stessa data (il DM: *«sì, certo»*): abilità nel suo statblocco del Bestiario, ricopiato in DEF-4; Percepire Intenzioni +13 (8 gradi fuori classe + SAG), gli 80 punti spiegati, `[INFERRED]` perché il ritmo del Runecaster è del FRCS |
| ~~D12~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: la pietra la incanta Sorella Brynja, chierica di 9° livello, ma all'8°: *silenzio* dell'SRD, 1 minuto per livello, cioè 8 minuti, e 160 mo (servizio SRD: livello dell'incantesimo × livello dell'incantatore × 10 mo). Brynja resta di 9°. Copre il volo di andata e la tenda. *Corretto il 2026-09-30 su segnalazione del DM: la prima stesura diceva 8 round*. Era: **La pietra del silenzio della variante dall'alto: chi la dà, e quanto dura?** Nessuno la vende. Proposta: Brynja, alla cappella, lancia *silenzio* su un sasso; dura un round per il suo livello, quindi basta per l'atterraggio e la tenda, non per il volo intero. Serve il livello di Brynja |
| ~~D13~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-28**: il corno sta nella **custodia col glifo**, e la custodia è **incatenata al polso di Grask**: chi la tocca lo sveglia anche se dorme. Le ore di veglia e di sonno (prima metà della notte sveglio, seconda a −10) sono una proposta `[INFERRED]`. Resta aperta la seconda metà della domanda: dopo un allarme di notte, il drago va sulle colline o sul campo? |
| ~~D14~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: sì alla proposta: fuga a metà pf = FERITO GRAVE; la Catena spezzata vale FERITO GRAVE se il drago aveva già perso un terzo dei pf; a ⅓ dei pf fugge al suo turno, salvo due colpi subiti nel round prima. Era: **Due esiti del duello senza casella.** Se Balvar è morto il drago fugge a metà pf: conta come FERITO GRAVE o FUGGITO? E la Catena spezzata dà «FUGGITO garantito», che per il carry-over B4 è l'esito più debole: è voluto? Proposta: fuga a metà pf = FERITO GRAVE; la Catena spezzata vale FERITO GRAVE se il drago aveva già perso almeno un terzo dei pf. E la fuga a ⅓ dipende da «se i PG premono o allentano», che non è una regola. Proposta: a ⅓ dei pf fugge al suo turno, a meno che nel round prima abbia subito almeno due colpi |
| ~~D15~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: sì: il duello crolla con due PG a terra nello stesso round, o con il gruppo che si ritira dal cortile. Era: **Quando il duello «crolla» e intervengono gli avi (§6)?** Non c'è una soglia. Proposta: due PG a terra nello stesso round, oppure il gruppo che si ritira dal cortile |
| ~~D16~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: sì: vince l'esito del duello, gli altri tre colorano la prima frase della Corona. Era: **Il tono del Rubino è deciso in quattro posti** (la targa nella Scena 3, come muore Zog'tar nella Scena 8, l'esito del duello in §7, il «vinto sporco» in §6). Quale vince? Proposta: vince l'esito del duello; gli altri tre colorano la prima frase della Corona |
| ~~D17~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: sì: l'Aura dura fino all'alba del giorno dopo, quindi arriva a DEF-5. Era: **L'Aura della Forgia «dura fino all'alba», ma il rito si fa già all'alba.** Proposta: fino all'alba del giorno dopo, e quindi i PG arrivano a DEF-5 con *Possenza Divina* e *Protezione dal Male* ancora addosso, oppure fino al ritorno col Rubino |
| ~~D18~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-28**: prova di **Forza CD 25**, con gli aiuti SRD di chi tira insieme (+2 a testa), l'ala inchiodata per un round. Le corde sono quelle delle **gru sulle mura** `[INFERRED]`; fuori dalle mura restano quelle degli arieti rovesciati |
| ~~D19~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: sì: i nani capiscono il nanico antico a fatica (il senso, non le sfumature), Thorik lo legge. Era: **Chi del gruppo capisce il nanico antico?** Balvar parla solo quello, e la trattativa della Scena 7 si regge su chi lo capisce. Oggi il modulo nomina solo Thorik come lettore. Proposta: i nani lo capiscono a fatica (tutto il senso, non le sfumature), Thorik lo legge |
| ~~D20~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-27**: al tavolo hanno fatto il consiglio e il giro della fortezza (fucina, alchimista, cappella, rune di Zeth): **3 tacche** segnate: sono scesi da Zeth nelle gallerie (DM, 2026-09-28). Non hanno dormito. Il «campo di corsa» resta senza regola, ma con 6 tacche per il sonno la scelta non si pone più |
| ~~D24~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-27** (il DM: *«forse 6 tacche»*): dormire otto ore vale **6 tacche**. Con il consiglio segnato, chi dorme non fa in tempo a fare il campo prima dell'alba. (b) chiusa il 2026-09-28: al tavolo del 31 luglio i pf **non** sono tornati pieni, quindi vale l'SRD già scritto in DEF-2 |
| ~~D25~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: sì a tutti e tre: (a) −2 ad attacchi e prove, senza la parola «confusi»; (b) il banchetto dà +1 ai TS; (c) con le campane suonate il drago perde il round di sorpresa della picchiata (Ascoltare CD 20). Era: **Tre rilievi di regole della prima lettura a freddo (2026-09-25) mai chiusi**, trovati rileggendo i rapporti vecchi. Il riposo breve era il quarto, e il playtester l'aveva già visto (#13). **(a)** Scena 1: «confusi 1d4 round (−2…)» è la condizione *confuso* dell'SRD o un −2? Proposta: *frastornato* non basta, quindi un −2 a attacchi e prove, scritto senza la parola «confusi». **(b)** Il +1 morale del banchetto e il +2 morale delle Benedizioni **non si sommano** in 3.5 (stesso tipo): proposta, il banchetto dà il +1 ai TS, dove le Benedizioni non arrivano. **(c)** Scena 11: «togliere al drago il vantaggio del suono in picchiata» non ha un numero. Proposta: con le campane suonate il drago perde il round di sorpresa della picchiata (ascoltare CD 20 per sentirlo arrivare) |
| ~~D26~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: sì alla proposta: il registro delle letture a freddo in JSON e il cancello in CI che chiede una lettura nuova quando il master cambia. È un lotto da aprire. Era: **Il giro lettore, playtester e developer in automatico.** Oggi è obbligatorio (ADR-0075) ma lo ricorda solo il piano, e il riposo breve dimostra che un rilievo 🟡 può restare nel testo per giorni. Proposta: un registro in `plans/`, le letture a freddo in JSON, con per ogni master DEF, l'impronta del testo letto e i rilievi con il loro stato (corretto, residuo con ragione, domanda al DM); un cancello in CI che fallisce se il master è cambiato dopo l'ultima lettura, o se un rilievo 🔴 o 🟠 non ha uno stato. La lettura la fa un agente, non la CI: il cancello dice solo *quando* va rifatta. Costo: ogni modifica a un DEF, anche un refuso, chiede una lettura prima del merge, salvo una dichiarazione «modifica di sola forma» |
| ~~D27~~ | `LETTORE-PLAYTESTER` | — | ✅ **Decisa il 2026-10-07**: non c'era niente da considerare: il DM chiude la domanda. Era: **Il messaggio del 2026-09-27 si interrompe a «considera che i…».** Cosa andava considerato? |
| ~~D28~~ | `LETTORE-PLAYTESTER` | F3-bis | **La mappa di Hammerfist nel 372, dall'alto in basso.** Il DM, 2026-09-27: *«in ogni regno nanico, più si scende e più le stanze sono ampie, soprattutto le fucine grandi, come Erebor sotto la Montagna. Magari una mappa, anche con i camminamenti e le gallerie che le rune di Zeth riempiono come difesa contro un assalto interno, e il contorno delle mura esterne»*. Tre cose da decidere prima di disegnare: **(a)** che tipo di mappa (una sezione verticale a livelli, da consultare, o una griglia tattica da 1,5 m per giocarci sopra); **(b)** le rune di Zeth nelle gallerie sono già in gioco la prossima serata, con un effetto meccanico (per esempio un *glifo di interdizione* per corridoio), o solo colore; **(c)** la Scena 5 già giocata descrive tre forge e gallerie strette puntellate da poco: la fucina grande sta **sotto** quella giocata, oppure si riscrive il box. Proposta: (a) una sezione a livelli per il DM, più la griglia del solo cortile e delle mura, che c'è già (M7-B); (b) colore fino al 1372, dove Zeth è il Ghostlord; (c) la fucina grande sta sotto, e la si vede scendendo da Zeth  *(2026-09-28, il DM)*: la mappa è della **fucina, delle gallerie sotterranee, dell'alchimista, del chierico e dell'armeria**, e deve combaciare con il modulo, con le modifiche che il tempo porta (372 e 1372). ✅ **(a) decisa il 2026-09-28**: una **sezione a livelli** per il DM e le **griglie tattiche da 1,5 m** di fucina, gallerie, alchimista, cappella e armeria, con le varianti 372 e 1372. Il disegno è un lotto a sé (checklist F3-bis, con `rumblingstone-mapmaking`); resta aperta la (b), le rune di Zeth sui camminamenti con un effetto meccanico o solo colore |
| ~~D21~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: sì: con 8 tacche o più la Scena 10 non si gioca, le mura valgono «a stento»; Muoversi Silenziosamente CD 20 fallito fa partire il duello col bersaglio già scelto dal drago. Era: **Con 8 tacche o più, la Scena 10 si gioca?** Il modulo fa cominciare il duello fuori dalle mura, ma non dice se la prova delle mura salta né quale esito vale. Proposta: la Scena 10 non si gioca, le mura valgono «a stento» (2-3 successi), e un fallimento della prova di Muoversi Silenziosamente CD 20 fa partire il duello con il drago che ha già scelto il suo bersaglio |
| ~~D22~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-28**: il ritorno a piedi costa **1 tacca** di base, più una per blocco fallito. Chiude l'unico 🔴 della terza lettura |
| ~~D23~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: sì: Balvar recuperato può sciogliere la Catena, ma solo toccando la scaglia, nel cortile durante il duello, e lo sa. Era: **Un Balvar recuperato può sciogliere lui la Catena?** È la prima cosa che un tavolo gli chiede. Oggi il modulo dice solo che spiega dove sta la runa e come si spezza. Proposta: può, ma solo toccando la scaglia, cioè nel cortile durante il duello, e lo sa |
| ~~D29~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: sì: dopo un allarme il drago va sulle colline e torna solo al corno successivo. Era: **Dopo un allarme di notte, il drago dove va?** È la metà di D13 rimasta aperta: il testo dice «se ne va», senza scegliere fra le colline e il campo. Proposta: sulle colline, come ogni notte, e torna solo al corno successivo; così un allarme brucia il corno e non porta il drago sopra la tenda |
| ~~D30~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: sì: colore nel 372, difese del Ghostlord nel 1372. Era: **Le rune di Zeth sui camminamenti e nelle gallerie hanno un effetto meccanico la prossima serata, o sono colore?** È la (b) di D28, che la forma della mappa non chiude. Proposta: colore nel 372 (Zeth scrive in fretta e da un uso, e quelle le ha date ai PG), e nel 1372 sono le difese del Ghostlord |
| ~~D31~~ | `LETTORE-PLAYTESTER` | F4 | ✅ **Decisa il 2026-09-30**: l'arrivo nel Cuore della Montagna è fisso; l'orologio decide cosa succede sopra, e cioè la prima ondata già passata. Si toglie «all'istante di partenza». Era: **L'orologio di DEF-5 si contraddice** (🔴 del lettore e del playtester a freddo). Il modulo dice che il Rubino riporta i PG «all'istante di partenza» e che il viaggio non consuma orologio; dice anche che li deposita nell'istante in cui le porte del Cuore della Montagna cedono e la fortezza sta per cadere; e la tabella dei rami dice che con 3g 15h le mura sono intatte e c'è tempo per la Fase 0. Tre cose che non stanno insieme. Proposta: il **Cuore della Montagna è fisso** (è il «punto più nero» che il Rubino sceglie, e la cucitura con ARC08-11), e il ramo dell'orologio decide **cosa c'è sopra**: le mura intatte e la Fase 0 piena, o la prima ondata già passata. Si toglie «all'istante di partenza» |
| ~~D32~~ | `LETTORE-PLAYTESTER` | F4 | ✅ **Decisa il 2026-09-30**: sì: il Cuore di Moradin fa parte della Forgia e non entra nella meccanica del ritorno; l'ancora è la Forgia. Era: **Il Cuore di Moradin è speso o fa da ancora?** DEF-5 lo dà SPESO per la resurrezione di Hella, e nello stesso §3 lo fa agganciare gli spiriti dei PG «nella Forgia del 1372». Proposta: l'ancora è la **Forgia** (il luogo), non l'artefatto speso; si toglie il Cuore dalla meccanica del ritorno |
| ~~D33~~ | `LETTORE-PLAYTESTER` | F3-bis | ✅ **Decisa il 2026-09-30**: sì: la targa dice «quattro eroi dal fuoco e dalla pietra» in tutti e tre i punti; le Cronache dicono «quattro eroi» senza «dal futuro», e il «dal futuro» lo capisce il tavolo. Era: **La profezia: le Cronache in mano ai giocatori dicono già «eroi dal futuro»** (🔴 della quarta lettura di DEF-4). Il nodo della targa vieta di dire che la profezia parla di loro, la porta *Sapere* dice che è stata cancellata dalle cronache del 1372, e il testo della targa ha tre versioni («dal futuro», «dal fuoco e dalla pietra», e quella lunga del re). Proposta: la targa dice **«quattro eroi dal fuoco e dalla pietra»** in tutti e tre i punti; le Cronache che i giocatori hanno parlano di «quattro eroi» senza «dal futuro», e il «dal futuro» lo capisce il tavolo |
| ~~D34~~ | `LETTORE-PLAYTESTER` | F4 | ✅ **Decisa il 2026-09-30**: Tordek salta da un detrito sopra l'oceano, a metà strada; il Tempio è a 40 m; la strada si crea suonando il Diapason e tenendo la musica, con prove che sollevano blocchi dall'oceano. Quante prove e cosa costa un fallimento restano `[INFERRED]` nel master. Era: **DEF-1 Scena 6: da dove parte il salto verso il Tempio, e quanto è lontano?** (🔴 del lettore a freddo). Il modulo dice il portale a 50 m sopra l'oceano e i detriti fluttuanti, ma non la distanza dalla riva né da dove salta Tordek; la mappa T-4 lo fa partire dal pelo dell'oceano. Proposta: una catena di detriti parte dalla riva e sale fino al portale; ogni balzo è Saltare CD 25 (circa 7,5 m in 3.5), a ~20 m dal portale la gravità del Tempio cattura chi salta; il Tempio ruota sopra l'oceano a circa 40 m dalla riva, cioè sei-sette balzi |
| ~~D39~~ | `LETTORE-PLAYTESTER` | F4 | ✅ **Decisa il 2026-10-07**: (b): parlare con Balvar **durante** lo scontro nella tenda non costa tacche; prima di colpire costa ancora 1. Applicata nell'orologio della notte di DEF-4. Era: **L'orologio di DEF-4 non ha margine.** Con le 3 tacche già spese dal gruppo di oggi, parlare con Balvar (1) o fallire un solo blocco del campo porta a 8 tacche: l'alba fuori dalle mura, e la Scena 10 non si gioca. Lo dicono sia il playtester sia il developer del giro 1. Proposta: **(a)** la soglia 🔴 passa a 9 tacche; **(b)** parlare con Balvar costa 0 se lo si fa durante lo scontro nella tenda; **(c)** si lascia così: l'alba fuori è l'esito più probabile, ed è voluto |
| ~~D40~~ | `LETTORE-PLAYTESTER` | F4 | ✅ **Decisa il 2026-10-07**: (b): il duello al conto SRD, 1.460 PX a testa; il totale del beat scende a ~6.360, e il 14° arriva dopo DEF-5. Applicata in DEF-4 §8; DEF-5 §8 va rifatto con questa cifra. Era: **I PX del beat sono circa tre volte la tabella SRD** (Skullcrusher: 5.400 a testa scritti, ~1.460 da tabella). Il 14° livello di DEF-5 poggia su quella cifra. Proposta: **(a)** si tiene la cifra come premio di storia, detto apertamente; **(b)** si scende al conto SRD, e il 14° arriva dopo DEF-5 |
| ~~D41~~ | `LETTORE-PLAYTESTER` | F3-ter | ✅ **Decisa il 2026-10-07**: strada **B**. Il re dà il Giorno 21 le reliquie vendute a Gunnvor nel 372 e copre la differenza in gemme, fino a 10.000 mo per PG; vale anche la tacca nel legno del conto. Applicata in `ARC08-17` §2-§3 |
| ~~D42~~ | `LETTORE-PLAYTESTER` | F3-ter | ✅ **Decisa il 2026-10-07**: sì a tutto. Profili PF1e di Rethmar, Dauth e Channathgate, le casse, i loxo, la Cintura del monaco come premio del Torneo, il Tempio di Rethmar con un chierico di 13° e un diamante. Marcati `[CANONE — DM 2026-10-07, D42]` nei banchi e in `ARC08-17` |
| ~~D43~~ | `LETTORE-PLAYTESTER` | F3-quater | ✅ **Decisa il 2026-10-07** (il DM: *«1 calcola in proporzione, 2 ok»*). **(a)** In proporzione al conto della fucina le monete di Thorek I in tasca ai PG sono **zero**: la borsa al momento di pagare (10.000 in monete del 372, 6.314 in gemme, 19.603 in monete del 1372) è uguale ai conti (35.917), quindi tutto torna ai nani. **(b)** Sì: un quarto delle monete dell'hoard di Regiarix è conio elfico, **6.250 mo**, nella stessa proporzione delle reliquie di Rhest sul tesoro non magico. Applicata nei banchi §9 e in `ARC08-17` §3 |
| ~~D44~~ | `LETTORE-PLAYTESTER` | F3-bis, D28 | ✅ **Decisa il 2026-10-08** (il DM sceglie la proposta). **Da dove escono i PG di notte?** La **postierla** è nel muro sud, all'angolo sud-est, sotto la torre est: esce verso il fianco est del campo, col bosco come riparo. Corregge M7-A, che la dava a nord |
| ~~D45~~ | `LETTORE-PLAYTESTER` | F3-bis, D28 | ✅ **Decisa il 2026-10-08** (il DM: *«ci sono più fucine»*, poi lo schema proposto). **Le fucine di Hammerfist nel 372**: tre, una per livello. La **fucina originale** (la prima forgia) apre sul cortile: è quella che i Bracieri di Tordek riconoscono, dove si spinge il drago (Scena 11) e da cui viene l'incudine del rito (Scena 12); la **fucina di Gunnvor**, tre forge, dentro la montagna sul corridoio di cappella, alchimista e quartieri (Scena 5); la **fucina grande**, sotto le gallerie di Zeth, la più ampia. Chiude la (c) di D28 |
| ~~D46~~ | `LETTORE-PLAYTESTER` | F3-bis, D28 | ✅ **Decisa il 2026-10-08** (il DM sceglie la proposta). **La fortezza del 372 rispetto a quella del 1372**: è il **nucleo**. Esistono già il cortile (M7-B, che nel 1372 diventa il cortile interno), mura più basse (+4,5 m) e le sale nella montagna; fossato, cortile esterno, torri da 20 m e bastioni vengono nei secoli dopo |
| ~~D47~~ | `LETTORE-PLAYTESTER` | F3-bis, D28 | ✅ **Decisa il 2026-10-08** (il DM sceglie la proposta). **Dove sta l'armeria?** Accanto alla fucina di Gunnvor: la stanza del «mucchio buono» e delle armi per le mura. Nel 1372 è l'armeria nanica del banco di ARC-08 B4 |
| ~~D48~~ | `LETTORE-PLAYTESTER` | F3-bis, D28 | ✅ **Decisa il 2026-10-08** (il DM sceglie le proposte, una per una). **(a)** Il percorso e le misure come nelle griglie; **(b)** le rune di Zeth nel 1372 sono glifi di interdizione dell'SRD legati alla razza: un'esplosione per runa su chi non è nano, 4d8, Riflessi CD 14 dimezza (incantatore di 9°, come una pergamena, Q5), Cercare e Disattivare Congegni CD 28; **(c)** i leoni di pietra sono statue vuote, un'eco dei leoni spettrali del Ghostlord in ARC-09. Era: **Gli stati del 1372 delle sale sotto la montagna vanno bene?** Nessun master li descriveva, e le griglie M7-D, M7-E e M7-F del 1372 li propongono: la ritirata del Giorno 3 dal tunnel della statua alle gallerie di Zeth, poi alla fucina grande e al Cuore; gli orchi che saccheggiano il livello −1 dal corridoio principale; la riconquista al contrario; le rune di Zeth accese (D30) e due leoni di pietra nelle gallerie; le misure delle stanze. Resta da fissare l'effetto meccanico delle rune nel 1372. Proposta: approvare le griglie come sono e decidere le rune quando ARC-08 gioca la ritirata |
| ~~D1~~ | `MASTER-DEF` | A1 | ✅ **Decisa il 2026-09-27.** ARC-08: **quattro master**; ARC-09: **uno per beat**, circa dodici. Le fonti hanno spostato il taglio di ARC-08 rispetto alla proposta (il passaggio pregen → PG cade a metà della Sessione 3, non fra due master): la tabella in «A1» taglia per sessione, e attende l'OK |
| ~~D2~~ | `MASTER-DEF` | S1-S2 | ✅ **Decisa il 2026-09-27: rifinire.** I master nascono completi di read-aloud, battute, contingenze e vie non combattive. Chiude anche la D2 di MESTIERE-BANCHI: confluiscono qui S5 e S6. S4 resta là perché riguarda ARC-07 (vedi §1) |
| ~~D3~~ | `MASTER-DEF` | S4 | ✅ **Decisa il 2026-09-27: sì, solo forma.** Il contratto «In scena» e i rilievi di `domande_developer` come note del DM; nessuna riga di prosa cambiata, coerente con la D1 di MESTIERE-BANCHI |
| ~~D1~~ | `PIPELINE-IBRIDE` | Lotto A | ✅ **Decisa il 2026-09-30**: (a): il grounding segnala e basta, gate non bloccante, ma i segnali restano registrati in modo da poterci lavorare dopo. Era: **Cosa fa il grounding quando trova un difetto in una mappa di canone già giocata?** 🔎 **Non è più una domanda astratta: la misura del 2026-09-16 c'è.** 97 sacche isolate su 40 griglie, di cui **58 con dentro un segnalino di creatura**, 15 porte cieche, 12 griglie che una creatura Grande non attraversa. Una sola sacca è stata verificata a mano fino in fondo, ed **era un difetto vero**: i tre box delle stalle di Tarsilia, chiusi da `🏰` senza `🚪`, con dentro il cavallo che la tattica scritta dice di raggiungere. Le altre 57 **non sono state triangolate**, e il conto grezzo non dice quante siano difetti. Le tre risposte restano: (a) **segnala e basta**, gate non bloccante, canone invariato; (b) **segnala e si correggono le mappe**, cioè toccare griglie approvate; (c) **si esenta il canone esistente**, col rischio dell'esenzione silenziosa che ADR-0032 §1 ha già evitato una volta. 🔵 La proposta resta **(a)**, e adesso con un motivo misurato: 58 segnali non triangolati non possono bloccare una CI. Ma Tarsilia va corretta comunque, perché è un modulo standalone destinato a uscire. ✅ **Tarsilia corretta il 2026-09-24** (variante B: `🧱` e una porta per box); la domanda di D1 resta aperta per le altre 57 |
| ~~D2~~ | `PIPELINE-IBRIDE` | Lotto B · B1 | ✅ **Decisa il 2026-09-30**: vince la strada che costa meno token, misurata con `measure_tokens.py`. Era: **Dove vive il contratto d'estrazione dalla prosa?** Dentro `skills/rumblingstone-mapmaking/SKILL.md`, dove ogni agente lo vede sempre e paga i token a ogni conversazione, oppure in un file di riferimento caricato solo quando la skill instrada là. `measure_tokens.py` sa dare il costo delle due strade sullo stesso testo: la domanda si può decidere con un numero invece che a occhio |
| ~~D3~~ | `PIPELINE-IBRIDE` | Lotto E | ✅ **Decisa il 2026-09-30**: sì alla proposta: il ponte aspetta la chiusura dei lotti A e B. Era: **Il ponte `llm_bridge.py` si costruisce, o ADR-0067 resta scritta e il codice aspetta?** La proposta è aspettare: con A e B chiusi il ciclo funziona a mano, e allora si vedrà se il ponte fa risparmiare davvero. Serve una risposta solo quando A e B sono chiusi |
| ~~D4~~ | `PIPELINE-IBRIDE` | Lotto D | ✅ **Decisa il 2026-09-30**: tre scene annotate dal DM. Era: **Quante scene il DM è disposto ad annotare?** Il banco di misura della prosa esiste solo se qualcuno dice quali testi sono buoni, e l'unico che può dirlo è chi li ha visti funzionare al tavolo. Con zero scene annotate il lotto D copre le prime tre famiglie di §6 e la quarta resta fuori, il che è una risposta legittima e va detta invece che rimandata |
| ~~D1~~ | `MESTIERE-BANCHI` | F2 · S7 | ✅ **DECISA E ATTUATA il 2026-09-18, nello stesso commit.** Il DM ha **separato le due cose**: *«l'unica cosa da prendere è l'ADR quarta colonna, che può essere usata in diversi contesti nei vari archi [...] gli ADR interni li lascerei all'Abbazia [...] ma ovviamente la versione nell'Abbazia rimane così com'è senza estensione»*. → [ADR-0057](adr/ADR-0057-la-quarta-colonna-e-di-tutto-il-repo.md): la quarta colonna entra in `editorial-standards.md` §2 come norma del repo; i dodici ADR interni restano dell'Abbazia; l'Abbazia **non si tocca**. 🔎 **Misurato prima di scrivere la norma, e il numero ha cambiato cosa aspettarsi**: nel repo giocabile esisteva **un solo** blocco sensoriale strutturato (`ARC07-DEF-1` §4) — gli archi il sensoriale lo scrivono dentro la prosa dei read-aloud, non in schede. Come retrofit la norma vale **un posto**; il suo valore è prospettico, sui lotti S4-S6. ⚠️ **La forma è diversa dall'Abbazia, e apposta**: negli archi le schede sono **elenchi**, quindi la norma è sul *blocco* e non sulla colonna — in tabella è la quarta colonna, in elenco l'ultimo punto. Imporre la tabella avrebbe riscritto la forma per portare il contenuto |
| ~~D2~~ | `MESTIERE-BANCHI` | F2 · S4-S6 | ✅ **Decisa il 2026-09-27: rifinire**, dentro i master di [PIANO-MASTER-DEF](PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md). S5 e S6 passano là; S4 resta qui, perché i suoi bersagli (ARC07-DEF-4 e DEF-5) sono di ARC-07. Domanda originale: **ARC-08 e ARC-09 si rifiniscono nello stile, o si toccano solo dove manca un congegno operativo al tavolo?** Cambia l'ampiezza dei lotti da «aggiungere una sidebar» a «riscrivere prosa». I due archi sono chiusi come *piano* e ⬜ come *gioco*: la Torre non ha **una sola battuta** in 12 file e la Battaglia Finale **zero read-aloud** in 16, ma nessuno dei due è mai stato giocato, quindi nessuno li ha visti mancare. 🔗 *(2026-09-27)* La stessa domanda è la D2 di [PIANO-MASTER-DEF](PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md), che consolida i due archi in master: l'ordine del DM di fare i DEF la presuppone, ma non la chiude |
| ~~D3~~ | `MESTIERE-BANCHI` | F2 · S2-S3 | ✅ **Decisa il 2026-09-30**: sì: i lotti su DEF-1 restano additivi (sidebar, niente riscritture della prosa letta ai giocatori). Era: **DEF-1 è 🟡 in corso al tavolo: i lotti su di lui restano additivi?** Il piano assume di sì (si aggiungono sidebar, non si riscrive prosa già letta ai giocatori), ma è un'assunzione mia. DEF-1 ha **0 vie non combattive in 2.277 righe**: colmarlo è additivo, ma toccare i suoi read-aloud non lo sarebbe |
| ~~D1~~ | `PRATICHE` | PI-2 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). **La soglia delle 400 righe di codice per PR, come avviso in CI?** Oggi 13 merge su 34 la superano, e questa PR la supera di otto volte. Proposta: sì, avviso e non blocco |
| ~~D2~~ | `PRATICHE` | PI-3 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). **Dependabot, scansione dei segreti con push protection, `pip-audit`?** Le prime due si attivano nelle impostazioni del repository e sono gratuite perché il repo è pubblico. Proposta: sì a tutte e tre, `pip-audit` non bloccante per un mese |
| ~~D3~~ | `PRATICHE` | PI-6 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). **Le PR che toccano il canone si mergiano solo dopo la tua lettura dell'elenco?** Proposta: sì. Il resto lo verificano i gate |
| ~~D4~~ | `PRATICHE` | PI-1 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). **Il merge automatico delle PR verdi**, una volta protetto `main`? Proposta: sì, ed è ciò che rende economiche le PR piccole |
| ~~D5~~ | `PRATICHE` | PI-2 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). L'elenco misurato dopo `git fetch --prune` è di **38** rami, ed è nella risposta al DM dello stesso giorno: si cancellano quando il DM lo conferma. **I 39 rami remoti già interamente su `main` si cancellano?** L'elenco lo produce `misura_flusso`; `contenuti-nei-rami.json` conferma che non portano niente di nuovo. Proposta: sì, dopo che hai visto l'elenco |
| ~~D6~~ | `PRATICHE` | tutti | ✅ **Risposta del DM il 2026-09-24: (a).** **Come si esegue la regola di D1 dopo la #160?** (a) un ramo e una PR per lotto, (b) si aspetta il merge della #160 e si riparte sullo stesso ramo un lotto alla volta. Da qui ogni lotto di questo piano ha un ramo suo e una PR sua in bozza |
| ~~D7~~ | `PRATICHE` | PI-2 | ✅ **Risposta del DM il 2026-09-24: no.** Gli 11 rami del gruppo B restano. La misura riga per riga (`plans/esperimenti/misura-rami/misura_rami.py`) dà otto rami con tutto su `main` e tre (#42, #109, #67) con contenuto giudicato ma non su `main`; il DM: *«ci sono delle varianti che si possono estrarre e integrare nel main»*. Le varianti dei tre sono il lotto [RIPRESA-PR 4j-4](PIANO-RIPRESA-PR-ABBANDONATE.md) |
| ~~D8~~ | `PRATICHE` | PI-2 | ✅ **Risposta del DM il 2026-09-24: no, e il recupero previsto davvero** (*«no solo se è previsto davvero il recupero, altrimenti mantieni»*). I due rami senza PR restano finché il loro recupero non è chiuso: il Torneo di Dauth di maggio è [RIPRESA-PR 4j-1](PIANO-RIPRESA-PR-ABBANDONATE.md), `measure_tokens.py` è 4j-3 |
| ~~D10~~ | `PRATICHE` | PI-3b | ✅ **Risposta del DM il 2026-10-07: sì, raggruppate** (*«le PR settimanali vanno bene se non spalmate»*). **Una PR per pacchetto o una per ecosistema?** Applicata con i `groups` di Dependabot, una PR a settimana per ecosistema, la sicurezza a parte |
| ~~D11~~ | `PRATICHE` | PI-3b | ✅ **Risposta del DM il 2026-10-07: sì** (*«usa pip-audit in modo che Dependabot aggiorni facendo l'audit e verificando che non rompe niente o che è necessario un aggiornamento del codice sorgente»*). **Ogni aggiornamento si prova prima di entrare?** Applicata con `dipendenze.yml`: audit bloccante sulle PR di dipendenze, test sulle versioni minime, commento nella PR quando è rossa |
| ~~D12~~ | `PRATICHE` | PI-3b | ✅ **Risposta del DM il 2026-10-07: sì** (*«controlla il Dockerfile e aggiornalo se necessario in automatico usando Dependabot»*). **Docker sotto Dependabot?** Applicata: ecosistema `docker` su `scripts/booklet-container`, base portata a Debian 13 e fissata per digest |
| ~~D9~~ | `PRATICHE` | PI-3 | ✅ **Risposta del DM il 2026-09-24: sì agli avvisi, no alle PR settimanali** (*«d9 ok, non le PR di aggiornamenti settimanali»*). **Dependabot anche per `converters/`?** Gli avvisi di sicurezza vengono dal grafo delle dipendenze, che legge già `converters/Html_to_markdown` e `converters/pdf-to-md-engine`; `dependabot.yml` resta sulla radice, e un commento in testa dice perché |
| ~~D1~~ | `QUALITA-CODICE` | E1 · E3 | ✅ **decisa dal DM il 2026-09-23: sì**, il verificatore condivide il lettore ([ADR-0066](adr/ADR-0066-le-creature-hanno-una-libreria-e-il-verificatore-non-importa-la-scelta.md)). **Il verificatore condivide il lettore?** Oggi lo fa già: importa 23 simboli da `genera_attributi`. **Sì** (consigliato): il lettore va in `dmcore/lettura_creatura.py` e lo usano tutti; l'indipendenza sta nelle regole e nella scelta, che il verificatore non importa mai (E4 lo prova). **No**: il verificatore tiene un lettore suo, copiato, più sicuro contro un errore di lettura condiviso e con una seconda copia da tenere allineata a mano |
| ~~D2~~ | `QUALITA-CODICE` | E6 | ✅ **decisa dal DM il 2026-09-23: (a)**, vince `genera_attributi`; attuata in E6. **Quale tabella dei ruoli vince?** Dei 6 ruoli di `genera_creatura`, 4 ordinano le caratteristiche diversamente dal profilo corrispondente di `genera_attributi` (schermagliatore, tiratore, blaster, controllore). **(a)** vince `genera_attributi`: cambiano i PNG che `genera_creatura` genera d'ora in poi, nessun blocco del Bestiario; **(b)** vince `genera_creatura`: cambiano gli `attributi` di alcuni dei 15 blocchi scelti dall'array, che il DM vede prima; **(c)** si tengono separate e si dichiara perché |
| ~~D3~~ | `QUALITA-CODICE` | E9 | ✅ **decisa dal DM il 2026-09-23: sì, subito**; attuata in E9. **`dm.py bestiario` si fa in questo lotto o dopo?** Costa poco e non dipende dalla libreria; farlo prima di E8 vuol dire toccare `dm.py` due volte se un'interfaccia cambia |
| ~~D1~~ | `RECUPERO` | L1 | ✅ **Decisa il 2026-10-10, il DM: prima la #229 e la #230** (*«mergia se verde»*), non come proposto. Era: **In che ordine arrivano su `main` #216, #229 e #230?** La #216 porta D13, D17, D38 e la *Torre*, che hai già deciso; la #230 è impilata sulla #229. Tutte e tre sono bozze tue. *Proposta*: prima la #216 (più vecchia, fondibile senza conflitti, chiude tre decisioni), poi la #229 e la #230 con il loro ADR rinumerato a 0087. Nessuna si fonde senza il tuo sì |
| ~~D2~~ | `RECUPERO` | L1 | ✅ **Chiusa il 2026-10-10 dalla regola stessa della proposta, l'ordine di arrivo**: la #230 arriva prima, quindi tiene `ADR-0086` (la sostituzione misurata); la #216 si rinumera a `ADR-0087` nel suo ramo prima del merge, la chiusura della #99 a `0088`. Era: **Chi tiene il numero ADR-0086?** Tre candidati: la memoria generata (#216), la sostituzione misurata (#230), la chiusura della #99 (proposta del thread dedicato). *Proposta*: nell'ordine di arrivo su `main`, quindi 0086 alla #216, 0087 alla #230, 0088 alla #99; ognuno si rinumera nel suo ramo prima del merge, con `validate_docs --prossimo-adr` |
| ~~D1~~ | `RESA-ASSET` | R1 | ✅ **Decisa il 2026-10-08, sera, il DM: come proposto.** Era: **Il testo delle mappe come lo uniformo ai volumi?** Proposta: font OFL incorporati in sottoinsieme (+52 KB stimati a SVG; misurati 43) |
| ~~D2~~ | `RESA-ASSET` | R2, R3 | ✅ **Decisa il 2026-10-08, sera, il DM: come proposto, tutte e due.** Era: **Le 177 celle a emoji di sistema?** Proposta: nuovi universali in casa dove il significato è uno, e il ripiego Noto per il resto. game-icons.net per le legende non scelto |
| ~~D3~~ | `RESA-ASSET` | R4 | ✅ **Decisa il 2026-10-08, sera, il DM: sì.** Era: **Un tema «dipinto» con 2-Minute Tabletop?** Proposta mia: non raccomandata (lavoro grosso, deroga alla regola 5); il DM l'ha scelta |
| ~~D4~~ | `RESA-ASSET` | R5 | ✅ **Decisa il 2026-10-08, sera, il DM: sì.** Era: **Un importatore Watabou per città, villaggi, edifici?** |
| ~~D5~~ | `RESA-ASSET` | R6 | ✅ **Decisa il 2026-10-08, sera, il DM: sì.** Era: **Azgaar FMG per le regionali?** Solo per regioni inventate |
| ~~D6~~ | `RESA-ASSET` | R4 | ✅ **Decisa il 2026-10-08, sera (terzo messaggio), il DM: come proposto.** Era: **Quali pacchetti di 2-Minute Tabletop, e dove stanno?** Proposta: si comincia con un pacchetto solo, quello dei dungeon; i PNG restano sulla macchina del DM (cartella ignorata da git) e il repo tiene solo la tabella `simbolo → file` e i crediti, perché un pacchetto pesa decine di MB |
| ~~D7~~ | `RESA-ASSET` | R5 | ✅ **Decisa il 2026-10-08, sera (terzo messaggio), il DM: R5 si rimanda** finché non ci sono le esportazioni vere. Era: **Le esportazioni di Watabou da cui partire.** Servono una città, un villaggio e un edificio esportati in JSON dal DM, con il loro seme: l'importatore si scrive su file veri |
| ~~D8~~ | `RESA-ASSET` | R6 | ✅ **Decisa il 2026-10-08, sera (terzo messaggio), il DM: nessuna per ora**, come proposto. Era: **Quale regione inventata con Azgaar?** Proposta: nessuna finché un arco non ne chiede una; il lotto resta pronto |
| ~~D9~~ | `RESA-ASSET` | R4 | ✅ **Decisa il 2026-10-09, il DM: una prova su una mappa.** Era: **R4 come procede?** Il DM aveva chiesto a cosa serve e se valeva un download automatico; la misura: il pacchetto gratuito dei dungeon ha 131 tessere e copre circa 10-15 degli 86 simboli, i link arrivano per email dopo una cassa a 0 $, la rete dell'ambiente non raggiunge Dropbox. Proposta: un installatore (`dm.py asset installa <zip>`) con guida e controllo in `doctor`, poi una sola mappa di interni nel tema dipinto, da confrontare con la pergamena |
| ~~D10~~ | `RESA-ASSET` | R5 | ✅ **Decisa il 2026-10-09, il DM: si parte da Dauth.** Era: **R5 come procede?** Proposta: la guida per esportare da Watabou la pianta di Dauth assediata, da usare come immagine; le cinque mappe tattiche dell'assedio (carte A-E di `DAY3-CITY-SIEGE`) col contratto JSON; l'importatore di città ed edifici solo se le esportazioni vere lo meritano. Sostituisce il «rimandato» di D7 |
| ~~D11~~ | `RESA-ASSET` | R6 | ✅ **Decisa il 2026-10-09, il DM: resta in attesa**, come proposto. La Cannath Vale è la Elsir Vale di *Red Hand of Doom* rinominata: è canone e non si genera. Nessun codice finché un arco non porta i PG in una regione inventata |
| ~~D12~~ | `RESA-ASSET` | R4 | ✅ **Risposta del DM il 2026-10-09: al tavolo usa Foundry.** Era: **Usi un VTT?** Decide il valore di R4: la resa dipinta va nell'export UVTT come immagine di sfondo |
| ~~D13~~ | `RESA-ASSET` | R4-bis | ✅ **Decisa il 2026-10-09, il DM: sì, CC0 principale**, come proposto. Era: **Le texture CC0 (Poly Haven, ambientCG) diventano la strada principale per mappe più ricche, e 2-Minute Tabletop un extra opzionale solo per il tavolo?** Il DM aveva chiesto una strada senza problemi di licenza; le licenze lette alla fonte: Poly Haven e ambientCG CC0 1.0 |
| ~~D14~~ | `RESA-ASSET` | R4-bis | ✅ **Decisa il 2026-10-09, il DM: committate accanto alla pergamena**, non come proposto. Era: **Le mappe con texture dove finiscono?** Proposta: solo in locale. Scelto: un secondo SVG per ogni mappa in `rendered-texture/`, controllato da `validate_maps`; stima +2,3 MB sui 50 SVG |
| ~~D15~~ | `RESA-ASSET` | R4-bis | ✅ **Decisa il 2026-10-09, il DM: glifi ora, IA locale dopo.** Era: **Gli oggetti di scena da dove vengono?** I glifi in casa restano sopra le texture; un lotto futuro genera oggetti zenitali con ComfyUI e pesi a licenza permissiva (ADR-0019), col gate di rifiuto di `rumblingstone-art-direction` |
| ~~D16~~ | `RESA-ASSET` | R4-bis | ✅ **Decisa il 2026-10-09, il DM: velatura 0,30**, come proposto, dopo il confronto 0,45 / 0,30 / 0,20 sulle texture vere (M7-D per gli interni, Hammerfist L1 per l'esterno). Era: **Quale velatura per il tema texture?** A 0,45 erba e sentiero sembravano tinte piatte; a 0,20 muri e pavimenti degli interni si avvicinavano di tono |
| ~~D17~~ | `RESA-ASSET` | R4-ter | ✅ **Decisa il 2026-10-09, il DM: modelli 3D di Poly Haven e Quaternius**, non come proposto (solo Poly Haven). Era: **Gli oggetti di scena nel tema texture da dove vengono?** Modelli 3D CC0 renderizzati dall'alto con Blender in tessere webp, solo per il tema texture; Quaternius (Fantasy Props MegaKit, CC0, solo la parte gratuita) per ciò che Poly Haven non ha. Sostituisce l'IA locale di D15 |
| ~~D18~~ | `RESA-ASSET` | R4-ter | ✅ **Decisa il 2026-10-09, il DM: in una PR nuova, dopo il merge della #227**, non come proposto (nella #227) |
| ~~D19~~ | `RESA-ASSET` | R4-ter | ✅ **Decisa il 2026-10-09, il DM: sulla sua macchina**, come proposto. Era: **I modelli 3D (2,5-6 MB l'uno, 50-70 MB in tutto) dove stanno, e chi li rende?** Restano in `asset-esterni/oggetti-cc0/`, ignorata da git; il DM scarica e rende con `bpy` nel `.venv` o con il binario Blender; nel repo entrano solo le tessere e l'indice. Scartate: nel ramo solo per il render, nel repo per sempre |
| ~~D20~~ | `RESA-ASSET` | R4-ter | ✅ **Decisa il 2026-10-09, il DM: impronta uguale**, come proposto. Era: **Che scala hanno gli oggetti nella cella?** Il lato lungo di ogni modello al 76% della cella, come i glifi; l'indice tiene la misura vera e il fattore. Scartata: la scala vera (1 cella = 1,5 m) |
| ~~D21~~ | `RESA-ASSET` | R4-ter | ✅ **Decisa il 2026-10-09, il DM: sì, ma 🧱 diventa un modello**, non come proposto. Era: **Restano glifi anche segnali, creature, strutture in scala di mappa, scale e buchi, muretto, affresco e gru?** Il muretto (94 celle) è un oggetto orientabile, con due tessere rese girando il modello |
| ~~D22~~ | `RESA-ASSET` | R4-ter | ✅ **Decisa il 2026-10-09, il DM: focolare con la fiamma glifo sopra**, come proposto. Era: **Il braciere 🏮: Poly Haven ha solo un focolare spento.** Scartate: solo il focolare, resta glifo |
| ~~D23~~ | `RESA-ASSET` | R8 | ✅ **Decisa il 2026-10-09, il DM: misura e preferenza, tutte e due**, come proposto. Era: **Quando una sostituzione (tessera da modello CC0, da ComfyUI, o una texture) prende il posto di un glifo o di un terreno?** Le misure del livello A non peggiorano (contrasto del contorno ≥ 3:1 o ≥ 90% del glifo, WCAG 1.4.11; non si confonde di più col vicino, SSIM; resta nella tavolozza, ΔE2000) **e** il DM la preferisce nel confronto a coppie alla cieca; in CI un cancello blocca chi peggiora la scheda committata oltre il 5%. Scartate: solo la preferenza, solo la misura |
| ~~D24~~ | `RESA-ASSET` | R8 | ✅ **Decisa il 2026-10-09, il DM: correggo e rimisuro**, come proposto. Era: **Il tema texture della #227 misurato contro la pergamena: glifi che perdono contrasto, ⛰ e 🔳 indistinguibili, ⬛ vicino al suo vicino, il segnalino su ⬜ che sparisce.** Nel solo tema texture un alone chiaro sotto glifi e segnalini e velature per terreno, tarati da `misura_resa.py tara` finché ogni misura è almeno pari alla pergamena. Scartate: velatura più alta per tutti, lasciare com'è |
| ~~D25~~ | `RESA-ASSET` | R4-quinquies | ✅ **Decisa il 2026-10-09, il DM: sì, giro di prova**, come proposto. Era: **ComfyUI in locale come terza fonte di oggetti?** Sulla GPU del DM, gli otto simboli del giro di prova, SDXL (ADR-0019), quattro semi ciascuno, sfondo tolto, gate di rifiuto di art-direction; ogni tessera passa da `misura_resa.py` e dalle coppie, contro glifo e modello CC0 |
| ~~D26~~ | `RESA-ASSET` | R8 | ✅ **Decisa il 2026-10-09, il DM: secondo parere**, come proposto. Era: **Le metriche apprese (LPIPS, DISTS, CLIP-IQA di piq) che ruolo hanno?** Girano sulla macchina del DM con `misura_resa_appresa.py`, i pesi restano lì, il JSON entra nella scheda e non blocca; diventano cancello solo se concordano con le preferenze del DM (κ ≥ 0,6). Scartate: cancello subito, non servono |
| ~~D27~~ | `RESA-ASSET` | R8 | ✅ **Decisa il 2026-10-09, il DM: cambio texture, le scarica lui**, come proposto. Era: **Con l'alone a 0,75 i glifi tornano al livello della pergamena; restano ⛰/🔳 a ΔE 1,48 e ⬛/🔳 a 2,29, più ⛰/⬛ e ⛰/🟤, che la velatura non separa senza cancellare la foto.** Tre candidati CC0 per ⛰ 🔳 ⬛ (`build_texture_cc0.py --candidati`), scelti da `misura_resa.py tara --candidati`; nel frattempo alone 0,75 e velature minime committati, le quattro coppie come difetto noto. Scartate: velature alte, tinte diverse |
| ~~D28~~ | `RESA-ASSET` | R8 | ✅ **Decisa il 2026-10-09, il DM: le texture si tengono solo dopo una scelta vera**, non come proposto. Il DM: *«le tengo se tengono conto di queste obiezioni e quindi mi fanno davvero scegliere oppure buttare quell'immagine per quella tipologia se non c'è nessuna valida»*. Le obiezioni: la prima pagina alla cieca non diceva a cosa si riferiva ogni immagine, aveva molte coppie identiche, non permetteva di rispondere «nessuna» e non distingueva ComfyUI dalle altre fonti. Era: **Le texture della fase 2 (⛰ roccia con licheni, 🔳 assi): le tieni dopo averle viste?** Fatto: una pagina di scelta per oggetti (`coppie`, più fonti con `--anche`) e terreni (`terreni-scelta`), riquadri con il nome, opzioni identiche tolte e dichiarate, «nessuna va bene» e «non vedo differenze», alla cieca o `--aperta`; `voti` rivela le fonti; `build_oggetti_cc0 --check` e `build_texture_cc0 --check` fanno valere la scelta |
| ~~D29~~ | `RESA-ASSET` | — | ✅ **Decisa il 2026-10-09, il DM: «sì, assolutamente»**, come proposto. Era: **M7-C: correggo i 18 rilievi del collaudatore in questa PR o in una nuova?** In questa PR. Fatto: i 18 rilievi applicati alla mappa, il master DEF-4 resta canone, le celle non scritte nel testo marcate `[PROPOSTA]`; il collaudo dà 0 errori e 0 avvisi |
| ~~D30~~ | `RESA-ASSET` | — | ✅ **Decisa il 2026-10-09, il DM: «vedi di correggere la griglia se possibile»**, non come proposto il 2026-09-11 (D10 di RICERCA-MESTIERE: «completare è progettazione»). Era: **PF-4 dichiara 33×33 con 25 righe; il Campo Drow 1 del P1C dichiara 53×40 con 33 colonne: va corretta la dichiarazione o completata la griglia?** Completata dove la geometria scritta lo permette: PF-4 per specchio attorno alla riga 17 più le passerelle delle POSIZIONI; il Campo Drow 1 dal SUPPLEMENTO-P1C (25 righe su 40), completato e copiato nel P1C. Le righe ricostruite sono `[PROPOSTA]` |
| ~~D1~~ | `TRASVERSALE-ARTEFATTI` | La **Risonanza** fra Corona e Aegis Fang dei moduli giocati (+2 sacro ai TS, +1d6 sacro contro caotici o malvagi, *Richiamo Ancestrale*, *Eco degli Eroi*) è attiva dal P1? | **Deciso**: la stampa del 16/01, senza Eco degli Eroi |
| ~~D2~~ | `TRASVERSALE-ARTEFATTI` | Il blocco «Sinergia con Aegis Fang» del master vale dal Rituale 1? | Chiusa dalla fonte: il PDF del giocatore del 22/10/2025 lo mette al Rituale 4 |
| ~~D3~~ | `TRASVERSALE-ARTEFATTI` | I bonus di quando Thorik ha indossato la Corona (immunità alla paura, scurovisione 36 m, *Aura di Comando*, *Guida di Moradin*)? | **Deciso**: tutti e quattro |
| ~~D4~~ | `TRASVERSALE-ARTEFATTI` | I poteri del Topazio in P3 (*Percezione del Tempo*, *Visione Temporale*, *Rallentare il Tempo*) e il «+1 a tutti i poteri»? | **Deciso**: Percezione e Visione; tolti Rallentare e il +1 |
| ~~D5~~ | `TRASVERSALE-ARTEFATTI` | La deflessione dopo il Rituale 4 se Thorik ha donato: +2 o +3? | **Deciso**: +2 |
| ~~D6~~ | `TRASVERSALE-ARTEFATTI` | Al portale per −1.000: 1d10 anni a Thorik, e pegno o Tempra CD 25 ad Artemis? | **Deciso**: entrambi |
| ~~D7~~ | `TRASVERSALE-ARTEFATTI` | RD del Manto: 5/epico o 5/epico e male? | **Deciso**: 5/epico e male |
| ~~D8~~ | `TRASVERSALE-ARTEFATTI` | La Senzienza della Corona: Int 16, Sag 17, Car 18, Ego 20? | **Deciso**: sì, senza dominio |
| ~~D9~~ | `TRASVERSALE-ARTEFATTI` | Anello: i dettagli di crisi della prima versione, e la *Dualità Armoniosa*? | **Deciso**: vale il PDF riforgiato; Dualità tolta |
| ~~D10~~ | `TRASVERSALE-ARTEFATTI` | I livelli minimi del libro della Corona contano? | **Deciso**: indicativi |
| ~~D11~~ | `TRASVERSALE-ARTEFATTI` | Lo stadio 1 dell'Anello (Mask sveglio) è stato usato al tavolo? | **Deciso**: no, solo la crisi; pagina giocatore tolta |
| ~~D12~~ | `TRASVERSALE-ARTEFATTI` | Gli effetti della Opzione C sulla scheda di Artemis? | **Deciso**: la Fortezza Mentale |
| ~~D13~~ | `TRASVERSALE-ARTEFATTI` | I poteri del Caos Ultimo (Anello, stadio 3)? | **Deciso**: *Alba Voluta* e *Purificazione del Crepuscolo* (senza cura) 1/giorno; il potere del *Prezzo dell'Armonia* lo sceglie Artemis e lo eredita Zalkatar |
| ~~D15~~ | `TRASVERSALE-ARTEFATTI` | Aegis Fang allo stadio 1 tiene la *Dragondoom* e i poteri inferiori dello stadio 0? | **Deciso**: restano tutti (equivalente +8) |
| ~~D16~~ | `TRASVERSALE-ARTEFATTI` | Il terzo stadio dei Bracieri, *le Chiavi della Forgia* (Torneo di Dauth, Xal'thor)? | **Deciso**: approvato com'era proposto (La Chiave, Mente di Pietra, l'orologio) |
| ~~D17~~ | `TRASVERSALE-ARTEFATTI` | La Collana Fiorita e la Foresta che Cammina: i poteri? | **Deciso**: approvate come proposte; *Radici nel Mythal* in ogni cerchio consacrato |
| ~~D14~~ | `TRASVERSALE-ARTEFATTI` | Aegis Fang: i poteri usati al tavolo e mai scritti (Ritornante, *bane*, Tuono, Dragondoom)? | **Deciso**: vale la scheda del repo, Ritornante e Dragondoom (la punizione del MIC); niente *bane* né Tuono allo stadio 0 |
| ~~D1~~ | `RIPRESA-PR` | F1 | ✅ **decisa 2026-09-05: archiviazione.** I tre master e i loro 7 SVG in `_ARCHIVIO/`; gli SVG non cancellati, così la cartella resta dentro il raggio di `validate_maps` |
| ~~D3~~ | `RIPRESA-PR` | F4 · 4c | ✅ **chiusa il 2026-09-12, eseguita nello stesso commit in cui e' stata dichiarata chiusa** (la lezione di D4). Il DM ha risposto il 2026-09-11 e il lotto 4c ha applicato entrambe le risposte: il **Giorno di Marcia 19** e' il punto di sincronia a cui il calendario torna col viaggio nel tempo — non un difetto, un tempo verbale, corretto; il **-2 COS di Thorik** era registrato come versato per una scena mai giocata, tolto dal presente insieme ai **-500 PE di Tordek**, che avevano lo stesso difetto e che nessuno aveva notato. 🔎 **E il lotto ha trovato il resto della stessa crepa**: §1 collocava tutti e quattro i PG dopo Hammerfist e dava **Hella viva**, mentre §6 dello stesso file la dava *«dead — resurrection pending»*. Vedi **§4.2-quater** |
| ~~D13~~ | `RIPRESA-PR` | F4 · 4c | ✅ **DECISA E ATTUATA il 2026-09-12, nello stesso commit.** Il DM ha approvato la **v4-bis**, con l'ultima taratura sua: **−1 CA invece di −2** per Thorik. 🛡️ **Thorik** dona il **+2 di deflessione della Corona** → **Scudo del Custode** (1/g, immediata: Hella prende il danno di un alleato entro 9 m **dimezzato**) + **l'Eco del Custode**, che e' l'idea del DM: quando lei scuda qualcuno **lui e' accelerato 3 round e si muove verso chi e' stato protetto** — l'anello si chiude, la protezione data torna al donatore trasformata in velocita'. ⚒️ **Tordek** dona **Ancoraggio della Montagna** → **Pelle di Adamantio RD 3/adamantino**. 🔮 **Artemis** dona **1d6 di Eldritch Blast** (7d6 → 6d6) → **Rovo Eldritch** a volonta': il DM ha visto che il dono precedente **si sovrapponeva** a quello di Thorik (stessa casella, dare tempo a un altro). ⚒️ **Reazioni degli artefatti al dono e al rifiuto**, tutte reversibili e tutte fondate sulla personalita' gia' in scheda. 🌱 **E il potere #6 della Collana non e' piu' `[da definire col DM]`**: il seme **restituisce** al donatore, una volta sola, e decide Hella. **Attuato in 17 file** + **12 istantanee** in `_ARCHIVIO/doni-v1-2026-09-12/`. Vedi **§4.2-quinquies** |
| ~~D4~~ | `RIPRESA-PR` | F4 | ✅ **chiusa il 2026-09-11: non era una domanda.** Misurato invece di ricordare: il `PALIO-BOOKLET` cita **14 file** — 8 stemmi, 4 mappe, 2 immagini — ed **esistono tutti e 14**. SVG veri da 2,7-5,4 KB, due PNG da ~2 MB, e `CREDITS.md` con l'attribuzione **CC BY 3.0** a game-icons.net già in regola. Niente da produrre, niente da togliere. 🔎 Settimo presupposto invecchiato di questa campagna, e la chiusura era rimasta indietro di un giro: annunciata il 2026-09-11 e non eseguita nello stesso commit |
| ~~D14~~ | `RIPRESA-PR` | F4 · 4d-2 | ✅ **CHIUSA E ATTUATA il 2026-09-16, nello stesso commit.** Il DM: *«la riga va in state.yml e poi riportata in state.md»*. Misurata, la risposta regge: la tabella dei waypoint è **dato puro** (10 righe) e il March Day è **un campo** (`march_clock.giorno_corrente`); il paragrafo di cinque righe che spiega perché il Giorno 19 è un bersaglio e non un passato resta **prosa, sotto e fuori** dalla regione generata. Separati, la macchina riscrive la sua riga a ogni sessione senza mai toccare la nota del DM — che era il nodo. ⚠️ La regione `auto:march-clock` **sparisce**, e marcarla oggi sarebbe *peggio* di prima: una regione dentro una `gen:state:` sono due scrittori sullo stesso testo. Sparisce anche `RETHMAR_DAY = 42`, cablato in `state_apply`: era la seconda fonte di verità più piccola del repo, e sopravviveva perché nessuno aveva mai eseguito il tool. Vedi **§4.8.9** e [ADR-0052](adr/ADR-0052-cosa-e-dato-e-cosa-e-prosa.md) |
| ~~D16~~ | `RIPRESA-PR` | F4 · 4d-2 | ✅ **CHIUSA E ATTUATA il 2026-09-16, nello stesso commit.** Il DM ha scelto l'enumerazione **con il compagno**: `attivo · latitante · neutralizzato · morto · ignoto`, più `reversibile`. ⚒️ `neutralizzato` copre il caso più frequente al tavolo — sconfitto ma non morto — e senza di lui il DM dovrebbe scrivere `morto` per non scrivere `attivo`. 🔴 **E `reversibile` è la metà che conta**: in questa campagna un morto torna (il Ghostlord nasce da un morto, Sal è protetto da un paradosso auto-consistente, Hella è morta in attesa del rito), quindi registrare «morto» senza dire se è definitivo è registrare **meno di quel che il canone sa**. La regola **R9** lo pretende. ⚠️ `state_apply` scrive `stato` ma **non** `reversibile`: il primo è la lettura letterale del log, il secondo è una decisione narrativa, e R9 la chiede al DM alla prima esecuzione — provato sul canone vero. 🔎 **§4 conoscenze è stata esclusa dopo averla misurata**, benché il DM avesse chiesto di includerla: tre righe non sono persone e tre persone compaiono sotto due nomi, quindi `stato` lì vorrebbe dire un valore privo di senso in tre casi e due copie divergenti in altri tre. Va nell'anagrafica del lotto della chiave. Vedi **§4.8.9** |
| ~~D17~~ | `RIPRESA-PR` | F4 · 4d-4 | ✅ **CHIUSA il 2026-09-17 — e la domanda aveva una premessa falsa, trovata dal DM.** Era posta come «i due villain senza scheda: si scrivono, si contano o escono da §3?». 🐛 **Tre delle quattro voci che avevo dichiarato senza scheda ce l'avevano.** Il DM: *«controlla bene negli archi o nel bestiario se c'è qualcosa magari annegato come prosa»*. **Zalkatar** ha uno statblocco a **GS 13** (14d4+70, CA 24) in `09_…/P2A-Torre-PARTE4-STATBLOCCHI-Zalkatar.md`; **Saarvith + Regiarix** ne hanno uno a **GS 13** in `09_…/P2-RHEST-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md`, e il file `FASE4` accanto dichiara esplicitamente *«le statistiche sono lì; questo è la regia dello scontro»*; il **Cerchio Druidico** ne ha uno in `Bestiario/mostri/cerchio-druid7-cr7.md`, marcato [ACCEPTED — DM-canon 2026-05-05]. L'errore non è stato non trovarle: ho cercato **solo dentro `Bestiario/`**, e allargando la ricerca ho **troncato l'output a sei righe** concludendo da una lista tagliata. ✅ Non c'era niente da scrivere né da togliere: c'era da **cercare meglio**. Resta **un** buco su 28 (`lathander-mask`), ed è corretto. ⚠️ **Conseguenza di progetto**: una scheda non vive per forza nel `Bestiario/`, e un cancello tarato lì avrebbe continuato a dare per mancanti due boss da GS 13. Nasce **R13**, che mette alla prova ogni buco dichiarato contro tutto il repo. Vedi **§4.8.10** e [ADR-0053](adr/ADR-0053-la-chiave-verso-il-bestiario-si-dichiara.md) |
| ~~D18~~ | `RIPRESA-PR` | F4 · 4d-6 | ✅ **DECISA E ATTUATA il 2026-09-17, nello stesso commit.** Il DM: *«spezzarli per intestazione verificando che non esistano già»*. Il catalogo portava **19 record intitolati al documento** invece che alla creatura, perché `build_monster_catalog.py` faceva **un record per file** e prendeva il primo GS: «Parte 2A – Torre Invisibile», GS 10. **19 → 8**, pool **372 → 397**. 🔎 Quel che ne è uscito non sono comparse: gli **otto fantini del Palio**, i **Sicari di Sonjak**, il Gonfaloniere Aldemar Vosk, la Drow Chierica di Lolth, gli esempi d'onda di Rethmar — tutti chiusi dentro un record solo. ⚠️ **La deduplica è ancorata a un fatto dichiarato**: si confrontano i nomi **solo** dentro l'insieme delle voci del Bestiario che citano *quel* documento come `Source`. È il modo di rispettare ADR-0053 (un matcher permissivo traveste l'ignoranza) senza rinunciare a dedurre: il legame documento↔voce l'ha scritto qualcuno, la somiglianza sceglie solo *quale* voce sta per *quale* intestazione. 🔴 **E il rischio opposto ha il suo presidio**: il record di file sparisce solo quando **ogni** creatura che il documento nomina ha già la sua voce — gli otto che restano sono quelli dove non è vero, e toglierli significherebbe meno rumore e **meno creature**. 🐛 Due difetti nei nomi generati, trovati misurando: la numerazione del Palio è **multi-livello** (`### 3.2 Drow Chierica`) e lasciava nomi che cominciavano per cifra, e la coda tagliata lasciava parentesi mai chiuse («Aldemar Vosk (LN»). 🔎 **E il cancello nuovo ha trovato un errore mio al primo giro**: contava **due** «Skullcrusher il Nero», perché la voce che avevo appena scritto puntava al file che il drago lo *nomina* soltanto — i numeri stanno in `_ARCHIVIO/PortaleForgia-P5-FASTPLAY.md`. Correggendo il puntamento è poi caduto fuori che `P6-INTEGRAZIONE` restava scoperto, e dentro c'erano **Re Thorek I** (Grr 16, il re di mille anni prima che si inginocchia davanti alla Corona) e **Durin Hammerfist**, l'antenato di Othrek: due PNG di canone che non aveva nessuno. Vedi **§4.8.12** e [ADR-0054](adr/ADR-0054-un-archivio-non-e-una-copia.md) |
| ~~D19~~ | `RIPRESA-PR` | F4 · 4f | ✅ **Risposta del DM il 2026-09-24, ed è un principio più largo della domanda**: *«la procedura dovrebbe essere quanto più automatizzata possibile: un DM normalmente non tocca affatto i file yml, al massimo se ha un'interfaccia scrive dei campi o seleziona i valori da un form già impostato»*. Quindi né lo scheletro da compilare né il derivato da rivedere a mano: il template è **derivato in automatico** dal prodotto, e ciò che resta di giudizio passa da un **modulo** a scelte. Procedura in §4.10.6, il via è **D21** |
| ~~D21~~ | `RIPRESA-PR` | F4 · 4f | ✅ **Risposta del DM il 2026-09-24.** Sulla procedura di §4.10.6: sì al comando `dm.py gruppo nuovo`; sì a togliere da sole le conoscenze sul party e a chiedere una riga alla volta solo dove serve un giudizio; **gli artefatti restano nel prodotto**, senza portatore; arco e livello di partenza a scelta; PG con nome, razza, classe, livello e PF, al massimo sei; clock a zero e trigger lasciati. Attuato in **4f-4**, §4.10.7. Sulle proposte di fine sessione (4f-5) il DM ha chiesto di più: *«non c'è un tool chiamato dal DM a fine sessione che prende le domande e genera lo state.md e la parte relativa di state.yaml in maniera automatica?»*, con il ciclo intero preparazione → tavolo → chiusura e un **menu testuale** che chiami `dm.py` e che un'interfaccia grafica possa avvolgere. 4f-5 passa a quel piano, commit successivo |
| ~~D22~~ | `RIPRESA-PR` | F4 · 4i | ✅ **Risposta del DM il 2026-09-24**: per le domande aperte del soggetto, cercare le risposte in tutte le PR, anche chiuse, poi seguire le proposte; piano di level design, `agents.conf` e Giorno 3 di Dauth come proposto. Trovato: **avevi risposto a tutto** (changelog della #72, rev. 5 e 6), e 133 righe su 133 sono in cronaca. Il soggetto è in `plans/`, datato; il basilisco confermato con la tua citazione; restano due conferme, la **D24**. Esiti degli altri tre file in §4.11.5 |
| ~~D23~~ | `RIPRESA-PR` | F4 · 4i | ✅ **Risposta del DM il 2026-09-24: da verificare dopo, e da riproporre come piano.** Diventa il lotto **4i-3** (§4.11.6), con le sue tre fasi. Misurato nel frattempo: `main` risulta `protected: false`, cioè oggi nemmeno una CI rossa impedisce il merge |
| ~~D24~~ | `RIPRESA-PR` | F4 · 4i | ✅ **Risposta del DM il 2026-09-24**: *«la destinazione del Piano del Fuoco è canone, e ha un senso anche per Therysol che vuole vendetta»*; e *«Varis era un informatore del Collezionista, non sono la stessa persona»*. Il GS di Maur (11) aveva già la sua risposta nel foglio XP. Attuato: la fuga nel Piano del Fuoco è canone in cronaca, coerenza, archi, lore di Cannath Vale, dossier del Collezionista e di Therysol. Varis verificato: la sua scheda (`Bestiario/png/Varis_Seta_Argento`) lo dà umano, GS 6, intermediario inconsapevole; la confusione stava solo nel dossier del Collezionista della prima stesura (aprile), nel titolo del suo file-rimando, in un prompt immagine e in due file di dati. Vedi §4.11.5 |
| ~~D20~~ | `RIPRESA-PR` | F4 · 4f-2 | ✅ **DECISA E ATTUATA il 2026-09-24, nello stesso commit.** Il DM: *«D20 ok ma non tralasciare nulla»*. Split per sezione come in §4.10.4: **528 righe su 528** ritrovate nelle due metà (controllate contro git da un test), nessuna duplicata, una sola parola spostata («ESCAPED», che la cronaca racconta già tre volte). Tredici rimandi aggiornati in undici file; restano sul nome vecchio i documenti datati (`plans/`, l'audit IP, la baseline del 21 settembre), come registro di quando sono stati scritti |
| ~~D1~~ | `VENDIBILITA` | ✅ **DECISA il 2026-09-12 — la spec funzionale è ratificata.** Vedi §10 per cosa è entrato e a che prezzo. In sintesi: i campi neutri entrano tutti per i **56 simboli** che ne hanno uno; `📦` diventa muro; `🌲` e `🌳` **no**, con deroga motivata; la luce resta quella del codice, scritta in metri. | ✅ Costo pagato: **+4 polilinee** su ciascuno dei 2 `.uvtt` committati, **zero** SVG. Il resto è additivo. 🔵 Ne è nata [**ADR-0051**](adr/ADR-0051-il-margine-del-bosco-e-un-glifo-a-se.md): `🌲` avrà un glifo per il margine, con una coda di **1.873 celle** da rileggere |
| ~~D2~~ | `VENDIBILITA` | ✅ **DECISA il 2026-09-12 — e allargata: le altezze diventano moduli di griglia.** Il DM: *«i muri normalmente sono 1.5, le tende falle più basse 1m»*. 🔎 **Il «1.5» non erano i muri veri**: nel repo `🏰` sta a 4 m, `⬛` a 3,2, `🗼` a 9 — un muro di pietra a 1,5 m sarebbe più basso di un uomo. Era `🧱` **muretto / copertura bassa**, l'unico simbolo chiamato «muro» che un'altezza non ce l'aveva: si estrudeva al default generico di 0,6 m, cioè un gradino, mentre l'etichetta promette copertura al petto. Poi il DM ha esteso la regola: *«muri piccoli 1.5 metri e poi multipli di 1.5 o approssimazioni più vicine possibili»*. Il quadretto del repo è 1,5 m, quindi **tutte e 31** le altezze sono state portate sul modulo: quadretti interi per ciò che sta in piedi (15), mezzo quadretto per l'ingombro che si scavalca (9), zero per ciò che è piatto (7). Prima erano numeri a occhio — 3.2 · 2.2 · 1.6 · 1.4 · 1.1 · 0.9 · 0.8 · 0.6 · 0.4 — che non volevano dire niente rispetto alla griglia su cui la scena è costruita. | ✅ Costo zero: nessun artefatto 3D è committato. 48 celle `🧱`, 9 `⛺`. 🔵 **Resta il dais** `🔳`, e non è una dimenticanza: **zero celle nel repo** — è nato con ADR-0042 e nessuno l'ha ancora disegnato. Deciderlo adesso sarebbe inventarlo; il giorno che serve costa zero |
| ~~D1~~ | `CONFORMITA-STATBLOCCHI` | `goblin-warrior1-cr05` | ✅ **decisa dal DM il 2026-09-23: For 11**, la Forza del goblin SRD. Cambiano la riga delle caratteristiche e il danno (1d6−1 → 1d6); lotta e attacco la presupponevano già |
| ~~D2~~ | `CONFORMITA-STATBLOCCHI` | `tyrgarun-blue-old-cr18` | ✅ **decisa dal DM il 2026-09-23: lotta +49, For 33 resta.** Tenere +46 voleva dire For 26-27 e abbassare morso, artigli, ali, coda e stritolamento, che tornavano tutti con For 33 |
| ~~D3~~ | `CONFORMITA-STATBLOCCHI` | `drow-assassina-lolth-cr10` | ✅ **decisa dal DM il 2026-09-23: For 12.** Lotta +6 → +7, danno della spada corta 1d6+1 → 1d6+2; l'attacco con Arma Accurata non cambia |
| ~~D4~~ | `CONFORMITA-STATBLOCCHI` | `drow-trickster-arcano-cr11` | ✅ **decisa dal DM il 2026-09-23: BAB +5.** Lotta +3 → +4; stocco e balestra tornavano già |
| ~~D5~~ | `CONFORMITA-STATBLOCCHI` | `ghost-lion-spettrale-cr8` | ✅ **decisa dal DM il 2026-09-23, in due passi.** Prima: trascrivere la fonte d'arco. Poi: *«verifica se è coerente con 3.5 o PF1e e scegli la versione più forte»*. Sulla base della fonte (9 DV, Des 18, Sag 12, Car 24) il **fantasma PF1e** vince: pf 103 contro 58, Tempra +10 contro +3, BAB +6 contro +4, tocco corruttore 8d6 contro 1d6. Il verificatore impara la variante PF1e dei non morti (d8, BAB ¾, Carisma per pf e Tempra), solo dove il `tipo` la dichiara. La fonte d'arco §2 diventa una copia di regia con il rimando alla scheda. ⚠ Regole del template citate a memoria: SRD e PRD bloccati dalla rete |
| ~~D12~~ | `CONFORMITA-STATBLOCCHI` | `ghost-lion-spettrale-cr8` | ✅ **chiusa con D5, il 2026-09-23**: nella versione PF1e scelta dal DM l'iniziativa è **+4** (Des +4, nessun talento) e l'attacco è il tocco corruttore **+9** (BAB +6, Des +4, Grande −1); il morso +10 della fonte non è un potere del fantasma |
| ~~D6~~ | `CONFORMITA-STATBLOCCHI` | `loxo-warrior3-cr4` | ✅ **decisa dal DM il 2026-09-23: umanoide mostruoso.** DV razziali in d8; dalla progressione SRD seguono BAB +6 (con lotta +15 e attacchi +1), Riflessi +4, Volontà +6 (ADR-0065 §2). 🐛 Il primo tentativo scriveva `pf-dado: 6d8+18` e il cancello lo respingeva: il campo deve seguire la formula della scheda, `3d8+3d8+18` |
| ~~D7~~ | `CONFORMITA-STATBLOCCHI` | `druid-bear-ally-cr12` | ✅ **decisa dal DM il 2026-09-23: due gruppi di statistiche, e la composizione della fonte d'arco** (`…STATBLOCCHI-EPICI` §6): Druido 10 / Barbaro 2. Il blocco è la forma d'orso bruno (pf 102, CA 20, artigli +16, TS +14/+4/+11), e tutto torna col SRD; la forma umana sta in una sezione a parte (pf 70, TS +11/+4/+11). `extract_statblocks --check` impara che una sezione «Forma …» o «Variante …» non è la prosa del blocco |
| ~~D10~~ | `CONFORMITA-STATBLOCCHI` | `razorfiend-green-cr9` · `razorfiend-white-cr8` | ✅ **decisa dal DM il 2026-09-23: si applicano.** `pf-dado` trascritto dalla prosa (`10d12+50`, `9d12+36`), la Cos ricavata da lì da `genera_attributi` (20 e 18, erano 18 e 23), i TS ricalcolati dal SRD: verde **+12/+8/+10**, bianco **+10/+6/+7**. Il verde torna con la variante blu del DM su Tempra e Riflessi; la Volontà resta legata a una Sag generata, e la marca lo dice |
| ~~D11~~ | `CONFORMITA-STATBLOCCHI` | `derive_statblocks --apply-ts` | ✅ **decisa dal DM il 2026-09-23: si tiene, e scrive anche le caratteristiche da cui deriva.** Le caratteristiche non le sceglie più la matrice di `derive_statblocks`: vengono da `genera_attributi.genera`, la stessa funzione con gli stessi strati, e i TS si ricalcolano da quelle. Il blocco porta la marca di `genera_attributi`, quindi il suo `--check` lo verifica come uno suo. 🐛 La prima stesura lasciava i TS della matrice nel blocco provvisorio, e il tetto dei TS li leggeva: una prova lo presidia |
| ~~D8~~ | `CONFORMITA-STATBLOCCHI` | `gnoll-cleric-yeenoghu-cr7` | ✅ **decisa dal DM il 2026-09-23: For 18**, anche nella riga delle caratteristiche. Lotta +10 e attacco +12 la presupponevano già; il danno 1d8+5 torna |
| ~~D9~~ | `CONFORMITA-STATBLOCCHI` | `wyrmlord-karruk-cr10` | ✅ **decisa dal DM il 2026-09-23: tre stati, fuori ira, in ira, affaticato.** L'ira era la causa: caratteristiche, Volontà, squartare e roccia erano in ira, pf, CA e `pf-dado` fuori, e lotta, Tempra, attacco e danno non tornavano con nessuno dei due. Lo statblocco ora è fuori ira, con una tabella dei tre stati calcolati dal SRD. In più il BAB scende da +16 a **+14** (gigante 12 DV + Barbaro 5), come dicono i tre attacchi iterativi |
| ~~D7~~ | `RICERCA-MESTIERE` | metro di paragone | ✅ **decisa 2026-09-11: le mappe di *Red Hand of Doom* e quelle di *Rise of the Runelords* (Paizo)** — *«voglio quella qualità e risultato, o il più vicino possibile»*. 🔎 Le prime **sono già nel repo**: **69 immagini** in `00_Red Hand Of Doom/Immagini/`, divise in `MappeIncontri`, `MappeLuoghiTattiche`, `MappeVarie` — il metro si guarda, non si immagina. ⚠️ **Rise of the Runelords non si porta nel repo**: è IP Paizo (ADR-0005). Si nomina come riferimento e si tiene fuori; l'audit cita numeri e criteri, mai i file |
| ~~D8~~ | `RICERCA-MESTIERE` | stampa | ✅ **decisa 2026-09-11: a colori.** A1.6 (daltonismo) e A1.7 (resa in grigi) **restano non bloccanti**: la seconda perde quasi tutto il suo senso, la prima no — il daltonismo non dipende dalla stampante, e va tenuta come avviso |
| ~~D9~~ | `RICERCA-MESTIERE` | doppia versione | ✅ **decisa 2026-09-11: né tutte né solo le hero map — quelle che nascondono qualcosa.** Il DM: *«per le mappe che hanno interazione con i giocatori e che devono nascondere cose ai giocatori o dettagli che devono scoprire»*. Il criterio è **funzionale**, quindi decidibile da chi scrive la mappa e non da una lista: se la griglia contiene una porta segreta, un nemico non ancora visto, una trappola o un indizio da scoprire, serve la versione giocatori. Oggi ce l'ha **una sola** (`tarsilia-la-ruota-giocatori`) |
| ~~D10~~ | `RICERCA-MESTIERE` | §6 | ✅ **decisa e fatta il 2026-09-11.** Il DM: leggile tutte, proponi mappa per mappa, e archivia **solo dove tocchi la griglia** — oggi **nessuna**, quindi nessuna copia in `_ARCHIVIO/` e `git` fa da archivio. 🔎 Rileggendole una per una **la mia stessa proposta si è rivelata sbagliata su due mappe su tre**: solo `L1` era una pura etichetta da correggere; `L2` mappa 1 e mappa 2 sono **estratti**, non griglie mal etichettate. Vedi §6-bis, riscritta sulle celle contate. Fatte: **1 etichetta corretta** (`L1` 20×13 → 20×14, con l'area a 21 m che ne discende), **1 intestazione trasposta corretta** (`L2` mappa 1 → 21 colonne × 53 righe) e **4 marcature di estratto**. `validate_maps` resta a 40 SVG / 18 master, nessuna cella toccata |
| ~~D12~~ | `RICERCA-MESTIERE` | §6-bis | ✅ **Chiusa il 2026-10-09 contando le celle**: il secondo «17» di `Portale-Forgia-L2` mappa 2 aveva **3 celle**, ed era la didascalia delle passerelle est e ovest scritta con il numero davanti, non una riga della griglia. Ora è una didascalia senza numero. Era: 🐛 **`Portale-Forgia-L2` mappa 2 ha una riga `17` duplicata** — una alla riga 290 del sorgente, una alla 297; quale debba portare un altro numero lo sapeva solo chi aveva disegnato l'arena |

<!-- auto:end key=decisioni-dm -->

---

## 5 · Come si tiene aggiornato

Chi chiude un lotto aggiorna **quattro** cose nello stesso commit: la checklist
del piano, `INDEX.md`, `CHANGELOG.md` e — se cambia l'ordine o le dipendenze —
**questo documento**.

In questo documento si aggiorna **§0**, sul posto: la riga chiusa diventa ✅, la
successiva ▶. Non si aggiunge una sezione «Ripartire da qui» in coda: §6-§10
sono nate così, e ognuna ricopiava la lista di quella prima.

Le prime tre le controlla `check_plans_discipline`. La quarta era *«una debolezza
dichiarata»*, e il 2026-09-06 ha ceduto: §4 dava una decisione aperta il giorno
dopo che era stata presa, ne ometteva un'altra, e ne elencava **quattro che non
esistevano in nessun piano**. Adesso **§4 è generata** e il drift è rosso in CI
([ADR-0047](adr/ADR-0047-le-decisioni-aperte-hanno-una-casa-sola.md)):

```bash
python3 scripts/decisioni_dm.py --check   # gate: l'aggregato combacia coi piani?
python3 scripts/decisioni_dm.py --emit    # rigenera §4 dopo aver toccato un piano
```

### La quinta voce — prima di **creare** un ADR o un piano

⚠️ **Le quattro sopra riguardano chi *chiude* un lotto. Questa riguarda chi
*apre* un documento**, ed è nata da un errore vero.

🐛 **`ADR-0049` è stato assegnato due volte in due giorni**: all'edizione
commerciale (PR #138) e poi al margine del bosco (PR #141), perché chi scriveva
il secondo non aveva guardato la cartella. Nessun controllo poteva vederlo —
nessun link era rotto e nessun ADR mancava dall'indice, che mostrava
semplicemente due righe con lo stesso numero.

**Il numero di un ADR è la sua identità**: si cita nei commit, nei piani, nel
codice e nei changelog. Due decisioni che lo condividono rendono ambigua ogni
citazione **all'indietro**, sui documenti già scritti.

```bash
python3 scripts/validate_docs.py --prossimo-adr   # PRIMA di scrivere l'ADR
```

Stampa l'ultimo numero sul disco e il primo libero, e **esce 1** se una
collisione esiste già. Il numero si conta da `plans/adr/`, non dall'indice:
quarta regola di ADR-0045, e in questo caso l'indice era proprio il documento
che non se n'era accorto.

**Per un piano nuovo** il numero non c'è, ma la regola è la stessa e ha già la
sua decisione: si legge `plans/INDEX.md` **prima** di aprirlo
([ADR-0044](adr/ADR-0044-prima-si-guardano-i-piani-che-ci-sono.md)).
Un piano duplicato non rompe le citazioni, ma divide il lavoro in due posti che
divergono — ed è già costato sei settimane con la PR #72.

⚠️ **Il limite, dichiarato**: `validate_docs --sorgenti` vede la collisione
**dopo** che il file esiste, quindi in CI arriva comunque; `--prossimo-adr` è la
metà preventiva, e funziona solo se la si esegue. È una regola con un cancello
in fondo, non un cancello all'ingresso.

⚠️ **Il resto di questo documento resta scritto a mano**, e resta una
fotografia: l'ordine delle fasi, le dipendenze, i costi. Il gate copre la
tabella delle decisioni, non il giudizio che c'è attorno.

---

## 6 · 🔁 Ripartire da qui — la tornata del 2026-09-20/21

> **A cosa serve questa sezione.** La tornata si chiude con dei lotti aperti, e
> il DM riprende **in un'altra conversazione**. Qui c'è tutto ciò che serve a
> ripartire senza rileggere niente: **ogni cosa da fare ha un comando che la
> rimisura**, perché un elenco che dipende dalla memoria di una chat non è un
> elenco, è un ricordo.

### 6.1 · Il primo comando da dare, sempre

```bash
python3 scripts/fase1.py <i file che stai per toccare>
```

È la **sesta regola d'oro** (`G6`, `AGENTS.md`): quattro passi in sola lettura
prima di qualunque modifica, `--check` esce 1 se stai per toccare un archivio.
L'ordine delle sei regole sta in [`skills/REGOLE-DORO.md`](../skills/REGOLE-DORO.md),
per momento del ciclo.

### 6.2 · Cosa resta, e il comando che lo rimisura

| | Lotto | Dove | Il comando che dice a che punto è |
|---|---|---|---|
| ✅ | **2C** — i box read-aloud che presuppongono un'azione del giocatore | [PIANO-QUATTRO-ORDINI](PIANO-QUATTRO-ORDINI-2026-09-20.md) §2C | *chiuso il 2026-09-21*: `misura_craft --p1` → **22 su 477**, e sono un **elenco nominale** (12 dialoghi · 6 falsi positivi · 2 visioni · 1 canto · 1 condizionale), ancorato file per file da `test_ogni_residuo_e_uno_dei_ventidue_dichiarati`. ⚠️ **Non si porta a zero**: il rilevatore dichiara di non distinguere il dialogo dalla narrazione *(485 box dal 2026-09-25: una nota di allineamento in `DEF-2` A3, le battute di Moradin che chiedono i Doni in `DEF-3` §5, e i quattro box nuovi di `DEF-4` riordinato: il bosco, la sala del trono, la postierla, la tenda; i residui restano 22. I lotti 2f e 2g di CICLO-SESSIONE lo lasciano a 485: il sogno di Artemis spezzato in due battute ne aggiunge uno in `DEF-2`; in `DEF-1` sparisce una riga che il rilevatore scambiava per un box (`>   *DES 10 → 8*)`), riscrivendo il rimando alla Corona. Dal 2026-10-07 i box sono **511** su 487 file: `main` era già a 502, e l'attesa passava solo perché i file misurati erano 485; i banchi di ARC-08 e ARC-09 aggiungono due file e nove box, le locande un file e due box: **513** su 488. I residui restano 22)* <!-- attesa: 22 box su 514 --> |
| ⬜ | **M1-M3** — marcare gli incontri | [PIANO-MARCATURA-DEGLI-INCONTRI](PIANO-MARCATURA-DEGLI-INCONTRI.md) | `python3 scripts/validate_modules.py --tetto-el` → oggi **zero incontri marcati** |
| ✅ | **F1.1/F1.2/F1.3** — mappare le norme su severità | [PIANO-MISURA-EDITORIALE](PIANO-MISURA-EDITORIALE-STANDARD.md) | *chiuso il 2026-09-21*: `punteggio_mqm --norme` → **12 norme su 41** (la mattina erano **4 su 39**, e il «~40» era scritto a mano e sbagliato; poi F2.7-F2.9 hanno collegato i rilevatori che esistevano e registrato due norme mai elencate). *(42 dal 2026-09-24: si è aggiunta la regola 3 degli echi, non misurata; 43 dal 2026-09-25: la mappa che entra in colonna o va su A4, misurata dal gate di stampa; 44 lo stesso giorno: niente esce dalla colonna, misurata in parte; 45: la storia delle scelte fuori stampa; 46: le tabelle che in colonna vanno a capo; 50 col lotto 2f di CICLO-SESSIONE: il corredo della serata, i suoi PDF, le immagini con un servizio, la hero map di Canva AI; 52 col 2g: l'apparato fuori dalla stampa, una pagina una volta; 53 col lotto T10 di TRASVERSALE: la versione su ogni pagina di artefatto; 54 col T10-h: l'immagine dentro la pagina; 55 col lotto F1 di LETTORE-E-PLAYTESTER: chi e dove sta scritto nella scena; 59 con le domande del developer, da RICERCA-MANUALE-DEL-MASTER; 62 con ADR-0074 e il quiz a due agenti: l'apparato generato e le copie sincronizzate, la chiave del quiz, il tetto degli appunti; 63 con domande_developer, che misura quattro righe delle domande del developer e divide la §1 dalla §7; 69 col lotto L1 di AGENT-SKILLS-ESTERNE, il 2026-10-01: il lettore a freddo legge a scene, con il diario; 70 con L2: ogni master dichiara la sua serata; 71 con L4: la lettura nuova quando il master cambia; 75 con D13: niente «sembra» nel read-aloud; 76 con ADR-0077: i tic minori in gruppo; 77 con la lettura che frena l'automatico; 78 con l'indice dei references; 82 col merge del 2026-10-02 della PR #188, che porta le quattro del lotto F2.10 di MISURA-EDITORIALE: il box di luogo in poche frasi, senza creature, nell'ordine consigliato, e l'area chiave di *Dungeon*; 83 col lotto F2.11 del 2026-10-03: il foglio di stile, la grafia dei nomi e dei termini; 85 col lotto V1 di COLLAUDO-MAPPE, il 2026-10-08: la mappa tattica collaudata come grafo, e il suo nord; 86 con V2-quater, la sera: le chiusure nel verso del loro muro; 87 con la D18: ogni mappa dichiara la sua categoria; 88 con la D9 di RESA-ASSET, il 2026-10-09: la licenza dei file di terzi e i pacchetti premium fuori da ciò che esce; 89 con D17-D22, lo stesso giorno: gli oggetti di scena da modelli 3D CC0 verificati, e i simboli che restano glifi; 90 con D23-D26: una sostituzione nella resa entra solo se misurata e preferita dal DM)* <!-- attesa: 92 norme; qui ne entrano 12 --> La severità è una colonna del registro — **1 critico · 15 maggiori · 20 minori** — e `misura_craft --discriminante` dice che i congegni-rumore sono **zero su 23** <!-- attesa: 0 congegni su 23 --> |
| 🟡 | **F1.5 + F3.3** — i due campioni e il κ | idem | ✅ F1.5 chiuso; F3.3 **eseguito sul campione B: κ = 0,0** *(misurato 2026-09-21)*. La metrica si dichiara non affidabile e **non entra in CI**. Le manca una norma che morda, e la strada è la verifica aritmetica degli statblocchi, sbloccata dagli `attributi` (riga sotto) |
| ✅ | **Conformità meccanica degli statblocchi** — tutti i lotti chiusi: L1, L2, L2-bis, L3, L4, L5, L6, L6-ter, L7; restano solo **decisioni del DM** (§9) | [RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI](RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI.md) §8-9 | `python3 scripts/conformita_statblocchi.py --check` → **ogni `pf-dado` registra i dadi vita** · `python3 scripts/conformita_statblocchi.py --riepilogo` → **101 tornano, 0 da correggere, 0 scarti del generatore, 0 decisioni aperte al DM** *(misurato 2026-09-23, dopo D1-D12)* <!-- attesa: da correggere 0 --> |
| ✅ | ~~i 27 ADR mancanti in `docs/INDEX.md` §4~~ | *nessun lotto: non c'era niente da fare* | `validate_docs --sorgenti` → **0** *(misurato 2026-09-21)*. 🐛 **I 27 non sono mai esistiti**: il buco più grande che `plans/adr/` abbia mai avuto è stato **uno**, il 2026-09-12, e da `14694c4` (16 settembre) l'indice è completo. Vedi §6.5 |

### 6.2-bis · 🐛 Quello che questa tabella ha sbagliato su se stessa

Delle cinque righe di §6.2, scritte il 20-21 settembre, **una era falsa nel
momento in cui è stata scritta** e una portava un numero già corretto da nove
giorni. Il conto, verificato eseguendo i comandi che le righe stesse citavano:

| Riga | Quel che diceva | Quel che dice il comando |
|---|---|---|
| **2C** | 104 box | ✅ **104** — esatta |
| **M1-M3** | zero incontri marcati | ✅ **zero** — esatta |
| **F1.1-F1.3** | «4 norme su **~40**» | 🟡 4 su **39**: il tilde copriva un numero mai contato |
| **F1.5 + F3.3** | bloccato sul DM | ✅ esatta |
| **i 27 ADR** | 27 mancanti | 🔴 **zero**, e non per poco: il buco più grande mai esistito è stato **uno** |

E la riga gemella in `PIANO-QUATTRO-ORDINI` §310 parlava di *«51 link rotti dei
booklet generati»*: erano **44**, sono stati chiusi il **12 settembre** dal
lotto E1 di `RIPRESA-PR`, che nello stesso documento li registra a **zero**.
Due rami dello stesso archivio dicevano due cose diverse sullo stesso fatto.

⚠️ **E il difetto non è dove sembra.** §6 nasce con un principio dichiarato —
*«ogni cosa da fare ha un comando che la rimisura, perché un elenco che dipende
dalla memoria di una chat non è un elenco, è un ricordo»* — e quel principio è
giusto. Ma **scrivere il comando accanto alla riga non è eseguirlo**: i 27 sono
stati scritti *citando* `validate_docs --sorgenti`, che in quel momento
stampava zero. Il gate esisteva, girava in CI, era verde, e la riga lo
contraddiceva.

**Cosa cambia, quindi.** Ogni riga di §6.2 porta da oggi la **data della
misura** fra parentesi. Non prova che il comando sia stato eseguito — niente lo
prova — ma rende visibile *quando* si dice che sia stato, e una data ferma da
due settimane accanto a un numero è la cosa che fa venire il dubbio. Un
cancello vero su questo è una proposta, non una decisione mia: è in **§6.4**.

---

### 6.3 · Le tre cose decise in questa tornata che NON vanno ridiscusse

1. **Il Rituale 4 è chiuso.** Decide la scheda che il giocatore ha letto: il
   *Manto di Pietra e Spirito* è del Rituale 3, l'*Aura della Forgia Eterna*
   del Rituale 4, e le tre fonti concordano sulla **CD 20**. L'innesco è la
   **vittoria**, non l'arrivo: `§4` non va ribilanciato.
2. **Fondere le skill peggiora.** Misurato: F1 da 0,744 a 0,728, richiamo sotto
   1,000. Non si rifà.
3. **La soglia del punteggio nasce dal repo.** I numeri vengono da
   `punteggio_mqm.py --distribuzione`, e si rimisurano con quel comando prima
   di cambiarli. Mai scriverne uno a memoria: è già successo, il 2026-09-21.

### 6.4 · Le decisioni aperte al DM, in ordine di costo

| | Decisione | Perché non la posso prendere io |
|---|---|---|
| 🔵 | **Aprire il piano di marcatura degli incontri?** | è lavoro su decine di file, e sblocca il primo critico vero del punteggio |
| ~~🔵~~ | ~~**I 104 box P1 si correggono tutti?**~~ | ✅ **eseguito il 2026-09-21**, e la risposta misurata è «82 sì, 22 no»: gli altri 22 sono dialogo, canto, visione, condizionale o falso positivo del rilevatore, e correggerli avrebbe **rotto dodici battute** per far scendere un numero. QUATTRO-ORDINI è **chiuso** |
| 🔵 | **Il campione A per il κ** | costa tempo al DM, e senza non si sa se la metrica concorda con lui |
| ~~🔵~~ | ~~**Un cancello sulle righe di §6.2?**~~ | ✅ **DECISO E ATTUATO dal DM il 2026-09-21, nello stesso giorno in cui è stato proposto.** → [ADR-0063](adr/ADR-0063-i-comandi-citati-si-eseguono.md): `verifica_sezione6.py --check` in CI, in un **job suo** perché esegue i comandi più lenti del repo. 🔒 I tre presidi sul rischio dichiarato — forma rigida (niente pipe, `;`, `&&`, `$()`), allowlist di script, `shell=False` — con **sette prove** che verificano *cosa si rifiuta di eseguire*. 🔎 **E al primo giro ha trovato tre cose**: la riga di F1.1-F1.3 era **già invecchiata di poche ore** (diceva «4 norme su 39», il repo era a 12 su 41), due righe citavano una misura senza dichiarare cosa si aspettassero, e il mio primo criterio dava un **falso positivo** su M1-M3 — `--tetto-el` stampa `✓` perché nessun incontro sfora, ma è verde **a vuoto**: un `⚠` non conta come pulito |
| 🔵 | **Un EL oltre il tetto si ribilancia o si dichiara?** | è una decisione di difficoltà, e oggi non si sa nemmeno quanti siano |

---

## 7 · 🔁 Ripartire da qui — la tornata del 2026-09-24 (PR #160)

> **Perché questa sezione.** Il DM ha chiesto di mergiare la #160 e di
> continuare in un'altra conversazione *«con tutto il resto, dalla pulizia a
> tutto quello che è stato aperto in questa PR e non ancora concluso o
> integrato in un piano, così siamo sicuri che non ci sia uno script, una
> tecnica o una discussione che va persa»*. Ogni riga qui sotto rimanda al
> posto dove la cosa è scritta per intero: questa sezione è l'indice, non la
> copia.

### 7.1 · Il primo comando, e come si lavora da qui

```bash
git fetch --prune origin
python3 scripts/fase1.py <i file che stai per toccare>
```

Da qui **un lotto = un ramo = una PR in bozza** (PRATICHE D1 e D6). La soglia è
di 400 righe di codice per PR, contenuti e file generati esclusi. La #160 ne
aveva 3.357: è il motivo della regola, non un precedente.

### 7.2 · Cosa resta, e dove sta scritto

| | Cosa | Dove | Da dove si parte |
|---|---|---|---|
| ✅ | **Pulizia dei rami già su `main`** (D5 sì): 38 su 38 cancellati dal DM il 2026-09-24, con lo SHA di ognuno in PRATICHE §7.1. I 17 rami rimasti sono in §8 | [PRATICHE](PIANO-PRATICHE-DI-INGEGNERIA.md) §7.1 e §7.2 | fatto |
| ✅ | **Il registro dei rami dopo il merge** (fatto il 2026-09-24, 216 riferimenti, 50 file mai arrivati; tolte anche le voci di `PIANO-LEVEL-DESIGN-…` e `agents.conf`, ormai identici su `main`): la voce `pr/160` passa da `in-volo` a `portato`, e la testata di `docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md` esce dalla misura | `plans/contenuti-nei-rami.json` | `python3 scripts/contenuti_nei_rami.py --fetch` |
| 🟡 | **PI-1 · 4i-3**, `main` protetto: verificato `protected: true`; manca la prova della prima PR indietro rispetto a `main`, e le due righe nella skill `rumblingstone-plans` e nel Playbook | [RIPRESA-PR](PIANO-RIPRESA-PR-ABBANDONATE.md) §4.11.6 | la prima PR del §7.1 che resta indietro |
| 🟡 | **PI-3**: `dependabot.yml`, `pip-audit` non bloccante e runner fissato a `ubuntu-24.04` sono su `main` con la [#162](https://github.com/gsamuele78/RumblingStone/pull/162). CodeQL JavaScript verde sulla #162. Restano la prima PR di Dependabot, la prova del blocco dei segreti e la revisione con l'IA di GitHub, che sulla #162 non è comparsa | PRATICHE PI-3 | §8 |
| ⬜ | **PI-6** canone toccato nella PR, **PI-2** `misura_flusso`, **PI-5** proprietà sui parser, **PI-4** scenari tracciati (dopo CICLO D6) | PRATICHE §5 e §8 | in quest'ordine, una PR ciascuno |
| ⬜ | **Ciclo di sessione e menu**: Fase 0 (ADR-0068, contratti, D1-D6), poi F1-F4 | [CICLO-SESSIONE](PIANO-CICLO-DI-SESSIONE-E-MENU.md) §5 | le D1-D6 del DM |
| ⬜ | **RIPRESA-PR** 4g e 4h; PR aperte #99 e #106 | RIPRESA-PR, §3 qui sopra | `python3 scripts/contenuti_nei_rami.py --fetch` |
| 🟡 | **Le azioni della CI su Node.js 20** (Dependabot per `github-actions` è configurato: la proposta arriva dopo il merge), deprecato: `actions/checkout@v4`, `actions/setup-python@v5`, `actions/upload-artifact@v4` girano già forzate su Node.js 24 (avviso in ogni esecuzione dal 2026-09-24) | PRATICHE PI-3 | Dependabot per `github-actions` le propone da solo; altrimenti si alzano a mano di una versione maggiore, in una PR sua |
| ✅ | **`ubuntu-latest` passa a Ubuntu 26 dal 19 ottobre 2026**: fissato `ubuntu-24.04` nei due job, si prova 26.04 in una PR sua (avviso di GitHub) | PRATICHE PI-3 | prima di quella data: o si fissa `runs-on: ubuntu-24.04`, o si prova la CI su `ubuntu-26.04` in una PR e si tiene `latest` |
| ⬜ | **`validate_lingua` rosso su `main`**: 24 refusi in 8 file (misurato il 2026-09-24). Il passo è non bloccante, ma GitHub lo annota come errore («exit code 1») anche con la CI verde, e confonde chi legge | nessun piano: nasce qui | `python3 scripts/validate_lingua.py`, poi correggere in una PR di soli refusi |
| ✅ | **L'esperimento BDD**: feature, step e i 16 mutanti restano come prova riproducibile, fuori dalla CI | [RICERCA-BDD-O-TDD](RICERCA-BDD-O-TDD-2026-09.md) §3 | `plans/esperimenti/bdd-gruppo-nuovo/` |

✅ *Eseguito dal DM il 2026-09-24: 38 rami cancellati su 38.*

**La pulizia dei rami, per il DM.** Cancella soltanto i 38 nomi della tabella
di PRATICHE §7.1, e ciascuno solo se è ancora interamente su `main`. Un ramo
nuovo, anche vuoto, non viene toccato:

```bash
git fetch --prune origin && git fetch --unshallow origin 2>/dev/null
grep -oE '^\| 2026-[0-9-]+ \| `[0-9a-f]{40}` \| `claude/[^`]+`' plans/PIANO-PRATICHE-DI-INGEGNERIA.md \
  | sed -E 's/.*`(claude\/[^`]+)`$/\1/' \
  | while read b; do git merge-base --is-ancestor "origin/$b" origin/main && git push origin --delete "$b"; done
```

### 7.3 · Decise in questa tornata, da NON ridiscutere

1. **Nessun YAML a mano** (RIPRESA D19): il DM risponde a domande, il codice
   scrive. `dm.py gruppo nuovo` è la forma di riferimento.
2. **Il Collezionista fugge nel Piano del Fuoco, e Varis non è lui**: Varis è un
   suo informatore (RIPRESA D24, canone). Maur è GS 11.
3. **Il TDD resta.** Il BDD è misurato: stessi difetti trovati, +42% di righe,
   dipendenze contro ADR-0037. Se ne tiene la pratica o il framework lo decide
   CICLO D6; la misura non si rifà.
4. **Le pratiche d'ingegneria**: sette su dodici c'erano già, tre non si
   applicano a uno strumento offline. PRATICHE D1-D6 decise.

### 7.4 · Le decisioni aperte al DM che nascono da questa tornata

| Decisione | Dove |
|---|---|
| **D1-D6** del ciclo di sessione (cronaca automatica, alleanze, chi scrive la prosa, che menu, immagini, BDD) | CICLO-SESSIONE §8 |
| La revisione di sicurezza con l'IA di GitHub: cambiare modello o spegnerla | PRATICHE PI-3 |
| Le D7 e D8 di PRATICHE, i rami rimasti | §8 qui sotto |

---

## 8 · 🔁 Ripartire da qui — dopo la #162 (2026-09-24, sera)

> **Perché questa sezione.** Il DM ha chiesto di ripartire da qui
> *«considerando quello che è stato fatto e aggiornando di conseguenza»*. §7
> resta com'era, con le righe chiuse segnate; questa sezione dice lo stato di
> adesso e cosa viene dopo.

### 8.1 · Cosa è successo dopo §7

- La [#162](https://github.com/gsamuele78/RumblingStone/pull/162) è su `main`
  (`87bd083`): PI-3 in parte, il registro dei rami dopo la #160, i 38 rami con
  il loro SHA.
- Il DM ha cancellato i 38 rami. Rimisurato con `git ls-remote`: non ce n'è
  più nessuno.
- La CI di `main` dopo il merge è verde e gira su `ubuntu-24.04`. Il passo
  `pip-audit` gira; essendo non bloccante GitHub lo mostra verde comunque, e la
  prova che non trova niente resta quella locale (13 pacchetti, nessuna
  vulnerabilità nota).
- Dependabot ha aggiornato il grafo delle dipendenze e **non ha ancora aperto
  PR**. Il suo primo giro, prima della #162, ha letto anche
  `converters/Html_to_markdown` e `converters/pdf-to-md-engine`, che
  `dependabot.yml` non copre.
- Sulla #162 il bot di revisione di Codex ha risposto solo che il limite d'uso
  è esaurito: nessuna revisione.

### 8.2 · Cosa resta, in ordine

| | Cosa | Classe | Dove | Da dove si parte |
|---|---|---|---|---|
| ✅ | **Le correzioni del ramo Salvatore**: la de-pietrificazione e i PF su `main`; la riga su Sonjak adattata, perché Sal non conosce quel nome (scheda di Sonjak). Corretto anche `Armate-COMPOSIZIONE-DETTAGLIATA.md` §8, che faceva di Sajak e Sonjak due persone (GS 12 → 13, dalla scheda) | **K** | [RIPRESA-PR](PIANO-RIPRESA-PR-ABBANDONATE.md) 4j-2 | fatto; il ramo si cancella dopo il merge |
| ✅ | **Il punto cieco del registro dei rami**: `contenuti_nei_rami.py --righe RAMO…` confronta riga per riga; rosso su Salvatore, verde su `documento-stemmi-alternativi` | **C** | RIPRESA-PR 4j-5 | fatto; il prototipo `misura_rami.py` resta come superato |
| ✅ | **D7 = no**: gli 11 rami del gruppo B restano. Otto hanno tutto su `main`, tre hanno varianti che si possono estrarre | DM | PRATICHE §7 | le varianti dei tre sono RIPRESA-PR 4j-4 |
| ✅ | **Le varianti dei rami giudicati**: decise dal DM. Il simbolo 🌫 del #42 è nella legenda (64 simboli) e due mappe di ARC-07 che lo usavano sono rigenerate; #109 e #67 no | **G** | RIPRESA-PR 4j-4 | fatto |
| ✅ | **Il Torneo di Dauth di maggio**: recuperati, con le scelte del DM, gli strumenti di regia del master (§6-§10), la sotto-quest di Thorik (Verric, Consiglio, mura), quattro aggiunte a Hella e due ad Artemis; corretto «Stonefist» in Durinheart | **K** | RIPRESA-PR 4j-1 (D8 = no) | fatto; il ramo si cancella dopo il merge |
| ✅ | **La correzione di `measure_tokens.py`**: il preload si legge dal «load order» del `SKILL.md`; le domande di campagna passano da 3.500-5.600 token a 18.500-23.000 | **C** | RIPRESA-PR 4j-3 | fatto |
| ⬜ | **I 24 refusi di `validate_lingua`** in 8 file, rimisurati stasera: gli stessi del mattino | **M** | nessun piano | `python3 scripts/validate_lingua.py`, una PR di soli refusi |
| ✅ | **Dependabot per `converters/`** (PRATICHE D9): sì agli avvisi, che vengono dal grafo; no alle PR settimanali. `dependabot.yml` resta sulla radice e lo dice in un commento | DM | PRATICHE §7 | fatto |
| 🟡 | **PI-3, il resto**: la prima PR di Dependabot, la prova del segreto (DM), la revisione con l'IA (impostazioni) | | PRATICHE PI-3 | si guarda alla prossima PR |
| ⬜ | **Da §7.2, invariati**: PI-1 · 4i-3 (la prova della prima PR indietro rispetto a `main`), Node.js 20 (aspetta Dependabot), PI-6, PI-2, PI-5, PI-4, il ciclo di sessione, RIPRESA-PR 4g e 4h | | §7.2 | nell'ordine di §7.2 |

### 8.3 · Come si lavora da una sessione con un ramo solo

La regola resta **un lotto, un ramo, una PR** (PRATICHE D6). Una sessione
d'agente però ha un ramo assegnato e non ne apre altri. Il modo che ha
funzionato con la #162: un lotto sul ramo, PR, merge, poi il ramo si
ricrea da `main` con lo stesso nome e ospita il lotto successivo. Nessun
lotto si somma a un altro nella stessa PR.

🔎 **Le regole di 3.5 fuori rete.** La skill `dnd-35-srd` non contiene il
testo degli incantesimi: `spells.md` ha le scuole e qualche esempio, e
`resources.md` manda a d20srd.org, che dalla sessione non si raggiunge. Il
testo c'è però nelle esportazioni PCGen di `Bestiario/pregen-pcgen/`, che per
ogni incantesimo preparato riportano effetto, livello (ricavabile dalla CD) e
pagina del PHB. È da lì che si è verificata la de-pietrificazione. Dirlo nella
skill è una riga in `resources.md`, e sarebbe una norma nuova da registrare
(G3): un lotto suo.

Due cose che la sessione non può fare, viste stasera: cancellare rami
remoti (i permessi rifiutano `git push --delete`) e raggiungere d20srd.org
(la rete lo blocca). La prima la fa il DM; per la seconda una regola si
marca `[INFERRED — needs DM confirmation]` invece di dirla verificata.

### 8.4 · Le decisioni aperte al DM che nascono qui

| Decisione | Dove |
|---|---|
| ~~PRATICHE D7~~: no, i rami restano; varianti in RIPRESA-PR 4j-4 | PRATICHE §7 |
| ~~PRATICHE D8~~: no, con il recupero in RIPRESA-PR 4j-1 e 4j-3 | PRATICHE §7 |
| ~~La regola della de-pietrificazione~~: verificata sulle schede PCGen del repo; via del DM al porting (RIPRESA-PR 4j-2) | PRATICHE §7.2 |
| ~~PRATICHE D9~~: decisa, avvisi sì e PR settimanali no | PRATICHE §7 |

---

## 9 · 🔁 Ripartire da qui — dopo la chiusura di RIPRESA-PR 4j (2026-09-24, notte)

> **Perché questa sezione.** Il DM: *«concluso la parte 4j si aggiorna con cosa
> fatto e si mergia, in modo da poter riaprire una nuova chat con cosa rimane da
> fare»*. §8 resta com'era, con le righe chiuse segnate. Questa sezione dice cosa
> resta dopo 4j, e da dove parte la prossima sessione.

### 9.1 · Cosa ha chiuso 4j

| Sotto-lotto | Cosa | PR |
|---|---|---|
| 4j-1 | il Torneo di Dauth di maggio, recuperato e adattato al canone di oggi | [#165](https://github.com/gsamuele78/RumblingStone/pull/165) |
| 4j-2 | le correzioni di Salvatore, una adattata; `Armate-COMPOSIZIONE-DETTAGLIATA.md` §8 | [#164](https://github.com/gsamuele78/RumblingStone/pull/164) |
| 4j-3 | `measure_tokens.py` conta il preload obbligatorio delle skill | quella che porta questa sezione |
| 4j-4 | 🌫 nella legenda; #109 e #67 no | 🌫 nella PR di questa sezione, il resto nella #165 |
| 4j-5 | `contenuti_nei_rami.py --righe` | quella che porta questa sezione |

Il dettaglio, con «Com'è andato» per ciascuno, è in
[RIPRESA-PR](PIANO-RIPRESA-PR-ABBANDONATE.md) §4.12.

### 9.2 · I rami che il DM può cancellare

Sei rami hanno il loro sotto-lotto chiuso (RIPRESA-PR §4.12, FASE 3). Lo SHA è
quello misurato in PRATICHE §7.2, e il comando cancella un ramo solo se la sua
testa è ancora quella: un ramo che nel frattempo ha ricevuto un commit resta.

```bash
git fetch --prune origin
while read sha b; do
  [ "$(git rev-parse "origin/$b" 2>/dev/null)" = "$sha" ] && git push origin --delete "$b"
done <<'RAMI'
895863241eaff57d135ed1b2527bd9f55009c2c1 claude/review-tournament-integration-yYlwv
64df2ebc8f87992e951b212e59996866ad4bf326 claude/salvatore-character-art-wSjuH
b5e04d2d78799a56bcfa8257c09bc0d817d61e28 claude/optimize-skills-agent-folders-dwJC4
4986ce87cb7826c804df3be3c34a1f3e3614b30b claude/dnd-map-generation-research-55pzry
c45c9cc43d64cb6723682a96f56b58f364267cfe claude/golarion-pregen-character-sheets-cstheq
23f14b607be177699b915c33dbaa7f9e022dee6a claude/terros-battle-hints-booklet-hfvbef
RAMI
```

Gli altri dieci rami `claude/*` restano (D7 = no), e resta
`campaign-group-rumblingstone-dm-gianfranco`, che è la partita (ADR-0007).
Le sessioni d'agente non possono cancellare rami remoti: lo fa il DM.

### 9.3 · Cosa resta, in ordine

| | Cosa | Classe | Dove | Da dove si parte |
|---|---|---|---|---|
| ✅ | **I 24 refusi di `validate_lingua`**: letti uno per uno, **11 erano veri** e sono corretti in 5 file («ad Damarath», «nè… E'», gli spazi della Corona da PDF, due refusi nel box di Tordek, un URL); gli altri 13 sono falsi positivi del validatore | **M** | nessun piano | fatto; restano 13, tutti nella riga sotto |
| ⬜ | **I 13 falsi positivi di `validate_lingua`**: il mascheramento del codice inline con «x» fa sembrare parole i due spazi prima di un'ancora (7, `PROMPT-IMMAGINI-07ILP.md`); «spazio prima della punteggiatura» scatta su una cella di tabella che contiene solo «?» (1) e sul rapporto «5.8 : 1» (5). Il testo è giusto, da correggere è la regola | **C** | nessun piano | `validate_lingua.py`, con un test per ciascuno dei tre casi e uno che provi che «familiare : è» resta rosso; a zero il passo può diventare `--strict` |
| ⬜ | **Il falso positivo di `validate_prosa`** sui file con «ECHI-» nel nome: `…DAUTH-CONSEGUENZE-ECHI-LUNGO-PERIODO.md` è per il DM e viene misurato come testo per i giocatori | **C** | RIPRESA-PR §4.12, 4j-1 | il criterio del nome in `validate_prosa.py`, con un test |
| ⬜ | **Le regole di 3.5 fuori rete**: dire in `dnd-35-srd/references/resources.md` che il testo degli incantesimi c'è nelle esportazioni PCGen di `Bestiario/pregen-pcgen/` | **M** + G3 | §8.3 | una riga nella skill e la sua voce nel registro delle norme |
| 🟡 | **PI-3, il resto**: la prima PR di Dependabot, la prova del blocco dei segreti (DM), la revisione con l'IA di GitHub | | PRATICHE PI-3 | si guarda alla prossima PR |
| 🟡 | **PI-1 · 4i-3**: la prova della prima PR indietro rispetto a `main`, e le due righe nella skill `rumblingstone-plans` e nel Playbook | | RIPRESA-PR §4.11.6 | la prima PR che resta indietro |
| 🟡 | **Le azioni della CI su Node.js 20** | | PRATICHE PI-3 | aspetta Dependabot |
| ⬜ | **PI-6**, **PI-2**, **PI-5**, **PI-4** (dopo CICLO D6) | | PRATICHE §5 e §8 | in quest'ordine, una PR ciascuno |
| ⬜ | **Ciclo di sessione e menu**: Fase 0, poi F1-F4 | | [CICLO-SESSIONE](PIANO-CICLO-DI-SESSIONE-E-MENU.md) §5 | le D1-D6 del DM |
| ⬜ | **RIPRESA-PR 4g e 4h**; PR aperte #99 e #106 | | RIPRESA-PR | `python3 scripts/contenuti_nei_rami.py --fetch` |
| ⬜ | **🧲 e 🤖**, gli altri due simboli locali che il renderer disegna come emoji. E una domanda che 🌫 ha aperto: quando un simbolo è universale, la nota locale della mappa («ZERO-G DILEMMA…» in map03) non arriva più nella legenda dell'SVG | | [RENDER-MAPPE-FEDELTA](PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md) §1 · RIPRESA-PR 4j-4 | come 🌫: prima si legge che cosa vuol dire il simbolo in ogni mappa che lo usa, poi legenda, test, mappe rigenerate |

### 9.4 · Il primo comando della prossima sessione

```bash
git fetch --prune origin
python3 scripts/fase1.py <i file che stai per toccare>
python3 scripts/decisioni_dm.py --check
```

Le decisioni aperte al DM sono in §4, generata da `decisioni_dm.py`.

---

## 10 · 🔁 Ripartire da qui — dopo la #167 (2026-09-24, notte)

> **Perché questa sezione.** Il DM: *«registra le modifiche e mergia la 167 e
> riinizia in una nuova chat con quello che bisogna ancora fare»*. §9 resta
> com'era, con la riga dei refusi chiusa; questa sezione dice cosa ha fatto la
> chat della #167 e da dove riparte la prossima.

### 10.1 · Cosa ha fatto la #167

| Cosa | Esito |
|---|---|
| I «24 refusi» di `validate_lingua` | letti uno per uno: **11 veri**, corretti su 8 righe di 5 file; **13 falsi positivi**, che vengono dalla regola e diventano il primo lotto di §10.2 |
| La Corona di Adamantio (`PG/Artefatti/LaCorona_di_Adamantio-DM.md`) | corrette le tre righe «Dopo  X : L'…»; restano **120 legature** tipografiche su 107 righe («aﬀresco»), che il validatore non vede |
| Il box del risveglio di Tordek | corretti «familiare :» e «vuoto  pronto… una altra»; il secondo il validatore non lo vedeva |
| `REGISTRO-LOTTI.md` | una riga «metà è salita»: un lotto **M** che si fida del gate non regge quando è il gate a sbagliare |

Il dettaglio è nella riga del CHANGELOG del 2026-09-24 «§9.3: i refusi di
`validate_lingua`» e nel corpo della
[#167](https://github.com/gsamuele78/RumblingStone/pull/167).

🔎 **I sei rami di §9.2 ci sono ancora**, rimisurati dopo la #167 con le stesse
teste. Il comando di §9.2 vale così com'è; lo lancia il DM.

### 10.2 · Cosa resta, in ordine

La tabella che stava qui è passata in **§0**, dove si corregge sul posto. Le
prime due righe sono state chiuse nella #168.

### 10.3 · Il primo comando della prossima sessione

Passato in **§0**. Qui diceva «13 attesi» per `validate_lingua`; dopo la #168
sono 0.

---

## 11 · Dopo la #169 (2026-09-25)

> **Perché questa sezione.** Il DM, dopo il merge della
> [#169](https://github.com/gsamuele78/RumblingStone/pull/169): *«continua il
> lavoro che c'è da fare guardando i piani, e scrivi nello stato che cosa è
> stato fatto e che cosa manca»*. La lista viva resta §0; qui c'è il diario.

### 11.1 · Cosa ha chiuso la #169

| Cosa | Dove |
|---|---|
| La serata del 2026-09-25: booklet del DM, 13 pagine ✉ per i giocatori, il volume «Il viaggio a mille anni fa» | `07_…/homebrew/sessione-resurrezione-mille-anni/` · `homebrew/volume-mille-anni/` |
| `ARC07-DEF-4` in ordine di gioco: tre atti, tredici scene, schede d'entrata dei PNG, appendici A4 da A a D, dieci contraddizioni corrette | `DEF-4` §9 «Cosa è cambiato» |
| `ARC07-DEF-3`: lo Step 6 dopo i Doni e la Custode, §8-bis e §8-ter, le righe «✉ Si consegna qui», appendici A e B, il discorso di Moradin sui Doni in §5 | `DEF-3` |
| `ARC07-DEF-2`: le mappe in un'appendice A4 | `DEF-2` |
| M7-C, la tenda del comando, nuova; M7-B corretta | `Mappe/ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.{json,md}` · `ARC07-MAPPE-DEFINITIVO.md` |
| Nove decisioni del DM applicate ai master | regia della serata §7 |
| Regola 3 degli echi: un eco non anticipa | `consequence-echoes.md` §3-ter |
| Una mappa entra in colonna o va su A4; ogni capitolo apre una pagina; immagini fuori pagina sotto i 16 cm | `rumblingstone-editoria` §2 e §4.4 · `rumblingstone-mapmaking` regola 7 |
| Catalogo dei mostri a 379 voci, impronta delle creature rigenerata | `build_monster_catalog --check` verde |

Rimisurato su `main` il 2026-09-25: `validate_norme_editoriali` 43 norme prima
di questa sessione, `build_monster_catalog --check` 379 voci in pari,
`decisioni_dm --check` 15 aperte su 60 e allineato. `pytest scripts/tests`
su `main` dà 1.336 passati e 20 saltati in un ambiente senza `typst` né Pillow;
con i due installati, come in CI, i saltati girano. A fine sessione, con i nove
test nuovi di §11.3: 1.365 passati, nessuno saltato.

### 11.2 · Le domande rimaste nei master di ARC-07

✅ **Chiuse il 2026-09-25**: il DM ha risposto «canone» a tutte e cinque, e per
Q3 vale la scheda della giocatrice. Come sono state applicate: §12.1.

Sono marcate nei file e nessuna è una decisione di un piano, perciò non
entrano nell'aggregato di §4. Si risponde qui sotto o nel file; l'agente poi
toglie la marcatura.

| # | Dove | La domanda |
|---|---|---|
| Q1 | `Mappe/ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.json` | La tenda misura 18 m × 16,5 m. `DEF-4` dice dove stanno le quattro rune e chi c'è, non quanto è grande: va bene così? |
| Q2 | `DEF-4` Scena 12, riga 1365 | Il nano molto vecchio del Rituale è Thorgrim? Il box non lo nomina, quindi regge in tutti e due i casi |
| Q3 | `DEF-3` Appendice A, riga 1200 | L'equipaggiamento di Hella: la scheda dice cuoio borchiato, scudo di legno e scimitarra, il §11 C dice cuoio, falcetto o scudo leggero. Oggi vale la scheda della giocatrice |
| Q4 | `DEF-4` riga 658 | Se al rito Hella ha trovato la ghianda annerita e non l'ha ancora piantata, il suolo sacro del −1000 può essere il suo? |
| Q5 | `DEF-4` righe 370-372, 486-488, 668-670 · `DEF-3` riga 770 | Sette dettagli di recitazione nelle schede d'entrata (Durin, Re Thorek I, Zeth, la Custode): come stanno in scena e come parlano. Sono proposte, e un «sì a tutte» basta |

### 11.3 · Il controllo a vista dopo la regola editoriale

La #169 ha cambiato il tema e l'esportatore, quindi tutti i volumi, non solo
i tre della serata. I quindici manifest sono stati compilati sul commit prima
della regola (`34a0b70`) e su `main`, e letti con PyMuPDF. La procedura sta
adesso in `rumblingstone-editoria` §4, «Il controllo a vista».

| Volume | Pagine prima → dopo la #169 → adesso |
|---|---|
| Palio | 52 → 64 → 61 |
| Drappo, booklet del DM | 83 → 92 → 92 |
| Serata della resurrezione | 95 → 104 → 104 |
| Serata, fogli dei giocatori | 13 → 18 → 18 |
| Abbazia della Rotta Sicura | 34 → 36 → 38 |
| Terros · volume del −1000 · ritorno alla Forgia · prop del Drappo | +3 · +2 · +1 · +2 |
| gli altri cinque | invariati |

La crescita viene da «ogni capitolo apre una pagina», ed è voluta. Le mappe
larghe della sessione di Terros e del Palio ora stanno su A4 e non vanno a
capo: su `main` prima della #169 uscivano dal foglio in quattro pagine di
Terros, ora in nessuna.

I difetti trovati, e dove sono stati corretti:

| Difetto | Da quando | Correzione |
|---|---|---|
| Una figura su pagina A4 riservava sempre 21 cm: nel Palio una riga sola a pagina 4 e un fregio solo a pagina 62 | dalla #169, che ci manda ogni mappa verticale | tema, `figura()`: il tetto si applica misurando |
| Percorsi in `codice` e parole come `PortaleDellaForgiaEterna` uscivano dalla colonna | da prima | tema, `show raw.where(block: false)` |
| Righe da compilare `____` uscivano dalla colonna (schede di feedback del Drappo) | da prima | esportatore, `_RIGA_DA_COMPILARE` |
| L'indice delle 48 aree dell'Abbazia, un float più alto di un foglio, si stampava sopra se stesso: 1.462 righe sovrapposte | da prima | esportatore, `RIGHE_TABELLA_FLOTTANTE` = 30, e `tabella(pagina: true)` nel tema |
| I `.typ` dei volumi in `homebrew/<sessione>/` non erano ignorati da git | da prima | `.gitignore`, `**/homebrew/**/*.typ` |

Sovrapposizioni di testo su `main`: 1.474 in quattro volumi; adesso zero.
Pagine con testo oltre il bordo: otto in quattro volumi; adesso zero, più un
falso positivo noto. Restano due residui minori, in §0.

⚠️ **Quello che non è stato guardato a occhio.** Le pagine sono state
scelte dalle misure, e guardate una per una solo dove una misura segnalava
qualcosa o dove la pagina conteneva una mappa del Palio, di Terros o
dell'Abbazia. Un difetto che non sposta il testo (un colore, un'immagine
sbagliata al posto giusto) le misure non lo vedono.

### 11.4 · Una misura falsa evitata

`fase1.py`, nel clone della sessione, diceva *«108 file mai arrivati su
`main`, 65 senza posto»*. Il clone era shallow: `rev-list --objects` vedeva
206 commit su una storia più lunga, e i file entrati su `main` prima di quei
206 sembravano mai arrivati. Con `git fetch --unshallow` lo stesso comando dà
50 file, tutti col loro posto, e `--check` è verde. Il registro è giusto;
lo strumento non dice che sta misurando su metà storia. È una riga di §0.

---

## 12 · La storia delle scelte fuori stampa, e le marcature aperte (2026-09-25)

> **Perché questa sezione.** Il DM, sulla #170: *«1 da aggiungere come task:
> chiudere tutte le proposte e inferred nel repo, così si decide e diventano
> canone o sono bocciate. 2 per tutti i booklet e gli echi rimuovere le parti
> che riguardano le scelte fatte nel repo; prima misura, poi prova a spostarle
> in una parte non renderizzata, e se il risultato è più pulito si aggiunge
> come tecnica per creare i booklet, insieme alle modifiche fatte nella 169»*.

### 12.1 · Le `[PROPOSTA]` e gli `[INFERRED]`, contati

Contati su ogni `.md` tracciato il 2026-09-25: **621 marcature in 209 file**,
542 `[INFERRED …]` e 79 `[PROPOSTA …]`.

| Dove | Marcature |
|---|---:|
| `Bestiario/` | 212 |
| piani, skill, documenti (descrivono la convenzione: non si chiudono) | 140 |
| ARC-07 | 85 |
| ARC-09 | 54 |
| `campaign/` | 50 |
| ARC-08 | 32 |
| `PG/` | 26 |
| altri (censimenti, RHoD, Drappo, stanza della Corona) | 22 |
| di cui in `_ARCHIVIO/` | 20 |

Sono decisioni di canone, quindi K: nessuna si chiude senza il DM. Il lavoro si
taglia per arco, nell'ordine in cui si gioca. Per ogni lotto l'agente prepara
le domande (una riga ciascuna, col file e la proposta), il DM risponde
«canone» o «bocciata», e l'agente applica: se canone toglie la marcatura, se
bocciata toglie o riscrive la riga, e in entrambi i casi rimisura il conto.
Le domande Q1-Q5 di §11.2 sono il primo pezzo del lotto di ARC-07.

**Il lotto di ARC-07, chiuso il 2026-09-25.** Nella cartella c'erano 82
marcature fuori dall'archivio: 45 negli `.hb.md` generati, che si puliscono
rigenerandoli, e 37 nei sorgenti. Il DM ha risposto per gruppi, e tutte
le risposte sono state «canone»:

| Gruppo | Marcature | Decisione |
|---|---:|---|
| Recitazione dei PNG (Durin, Re Thorek I, Zeth, la Custode, la Sentinella, Zog'tar) | 12 | canone |
| Trama: Thorgrim nel Rituale, la ghianda annerita, la tenda M7-C 18 × 16,5 m | 6 | canone |
| Equipaggiamento di Hella | 1 | vale la scheda: cuoio borchiato +2, scudo di legno +1, scimitarra +1 |
| Regole e numeri inferiti (durate, un ruling, morale, PX, tesoro, soglie) | 12 | canone come scritti |

Una conseguenza da dire: il §11 C di `DEF-3` elencava un solo «scudo/arma +1»
da 2.000 mo, la scheda ne ha due. Con i prezzi SRD il corredo di Hella passa da
~15.600 a **~16.900 mo**, e il tesoro ordinario dell'arco da ~52.050 a
**~53.350 mo**; allineati `DEF-3`, `DEF-5` e l'audit del tesoro.

Restano 5 marcature: tre frasi che descrivono la convenzione (riscritte perché
non dicano più che i valori sono da confermare, e l'istruzione di `DEF-4` su
come segnare un'improvvisazione futura), una riga dentro un blocco storico, e i
tratti del volto nei prompt delle immagini, che non erano nella domanda.

Nel repo: da **621 a 568** marcature. Il prossimo lotto è ARC-08.

### 12.1-bis · Il Drappo esce dalla beta

Su decisione del DM (2026-09-25) il volume del DM non contiene più i quattro
capitoli da beta: playtest alfa, IP e licenze, stato del modulo, schede di
feedback. I file restano nel repo; `STATO-DEL-MODULO.md` si stampa a parte, come
dice l'hub. Due note «(playtest alfa, serata…)» nelle giornate e due righe della
mappa dei file dell'hub sono passate nello storico. Il volume va da 94 a 83
pagine, e nel PDF non resta un rimando alla beta.

### 12.1-ter · I volti dei PNG di ARC-07, confrontati coi ritratti

La #172 ha portato i sette ritratti. Il confronto con le schede, PNG per PNG:

| PNG | Scheda e ritratto | Decisione del DM |
|---|---|---|
| Durin | il ritratto ha la barba lunga in una treccia, nessun naso rotto, cappuccio verde, ascia a una lama | vale il ritratto; l'ascia resta doppia perché lo è nello statblocco |
| Re Thorek I | quattro trecce invece di tre; il resto coincide | vale il ritratto |
| Thorgrim | mani aperte verso la luce, il box diceva sulle ginocchia | si corregge il box di `DEF-4` e la scheda d'entrata |
| Balvar | casacca verde sotto il grembiule invece del grigio ardesia | vale il ritratto |
| Zeth, Zog'tar, Vatore | coincidono | canone; il volto di Vatore non si confronta con Sal, che non ha un'immagine nel repo |

### 12.2 · La storia delle scelte fuori stampa

**La misura, prima di toccare.** Sugli 80 file che i manifest stampano, 181
righe portavano un segnale di storia (date di lavoro del repo, «decisione del
DM», «prima diceva», «riscritto», «cosa è cambiato»). Lette a mano: 161 vere,
20 falsi positivi, cioè frasi della finzione («la Sala non è cambiata») e
regole («a scelta del DM»). Nei quindici PDF le righe con un segnale erano 257.

**La prova.** La storia è rimasta nei sorgenti, accanto alla riga che spiega,
fra `<!-- storico -->` e `<!-- /storico -->`; le due catene di stampa la saltano
con la stessa funzione, `dmcore.testo.togli_storico`, che toglie da sola anche
le attribuzioni di forma fissa (`[CANONE — DM …]`, «(decisione DM …)»).
Segnati a mano 27 file, fra cui i quattro master `DEF` di ARC-07, la Cassetta,
la regia della serata, le introduzioni dei volumi, il Palio e tre note di
playtest del Drappo.

**Il risultato.**

| | Prima | Dopo |
|---|---:|---:|
| righe dei PDF con un segnale di storia (finzione compresa) | 257 | 67 |
| storia vera che arriva in stampa | 161 righe | 15, dichiarate |
| pagine: volume del −1000 · serata · Terros | 42 · 104 · 48 | 40 · 101 · 47 |
| sovrapposizioni · pagine quasi vuote nuove | 0 · 0 | 0 · 0 |

Le 15 righe rimaste sono in `scripts/tests/test_storico.py` col loro motivo:
date d'edizione, date di gioco, la provenienza di due immagini del Palio, un
`[INFERRED]` nell'intestazione di Balvar, due marche spezzate dentro gli
statblocchi e cinque righe dei capitoli da beta del Drappo.

**Due errori della funzione, presi prima del merge** e diventati casi del test:
un marcatore in linea a inizio riga veniva letto come l'inizio di un blocco, e
nel Palio si portava via l'intera intestazione; una marca che va a capo, tolta
dentro uno statblocco, univa due righe e mandava quello di Terros su una pagina
sua. Il test sul corpus morde: rimettendo il secondo errore diventa rosso.

**Diventa canone.** [ADR-0069](adr/ADR-0069-la-storia-delle-scelte-resta-nel-sorgente.md);
la tecnica completa per fare un booklet, con le regole della #169, è in
`rumblingstone-editoria` §2-bis, e `rumblingstone-module-standard` dice cosa
la #169 ha reso obbligatorio nei master.

⚠️ **Quello che resta fuori.**
- Gli `.html` del Drappo non sono stati rigenerati: qui la rigenerazione
  incorpora i font, e il file cresce di megabyte per una differenza che non è
  di contenuto. I `.hb.md` del Drappo sì.
- L'errata dell'Abbazia («nel testo originale era…») è rimasta: è un'errata
  dichiarata, e riscriverla è una scelta sul modulo.
- Una frase di storia senza data né formula il test non la vede. Il marcatore
  resta un obbligo di chi scrive, scritto in `module-standard`.

---

## 13 · Le tabelle strette, e i PDF della #169 rifatti (2026-09-25)

> **Perché questa sezione.** Il DM: *«rifammi i pdf della 169 vedendo come
> vengono applicate davvero queste nuove skills. Le tabelle ristrette in una
> colonna saranno illegibili: vedere se esiste un marcatore per tabelle o
> specchietti che per dimensione vanno su una colonna, e adattare il layout
> perché vengano rappresentati a una colonna, e poi si continua a due»*.

**Cosa c'era.** Un solo criterio: le tabelle da quattro colonne in su
scavalcavano le due colonne, e salivano sempre in cima alla pagina. Nessun
marcatore per l'autore. Nessuna tabella stava dentro un riquadro: gli
specchietti riassuntivi sono tabelle normali, e le note del DM sono prosa,
che in colonna si legge.

**La misura.** Con una sonda nel tema, Typst ha misurato ogni tabella dei tre
volumi della #169 in colonna (8,1 cm) e a tutta pagina (17,5 cm). Delle 125
rimaste in colonna, **100 erano alte almeno 1,8 volte** quanto a tutta pagina,
cioè andavano a capo in ogni cella; la peggiore 22,8 cm contro 6,3.

**Cosa non si può fare.** Mettere la tabella nel punto esatto e ripartire a due
colonne: Typst 0.15.1 non bilancia le colonne, e un blocco a due colonne
interrotto a metà pagina riempie solo quella di sinistra. Provato e scartato.

**Cosa si fa.** Come un manuale stampato: la tabella scavalca le due colonne in
cima o in fondo alla pagina dove è citata (`auto`), e porta una riga col titolo
della sezione, perché può finire sopra il suo titolo o alla pagina dopo. La
decide il tema misurando (soglia 1,8, scelta fra 1,8 e 2,2 provate sui PDF:
la 1,8 lasciava nella stessa pagina una quota maggiore). L'autore può forzarla
con `<!-- tabella: larga -->` o `<!-- tabella: colonna -->`. Nelle pagine a una
colonna (A5, appendici A4, fogli dei giocatori) non scavalca niente.

**Il risultato su tutti i quindici volumi.** 330 tabelle larghe: 198 nella
stessa pagina del loro testo, 111 nella successiva, 20 più lontano, dove molte
tabelle si susseguono (il Drappo e la serata). Zero sovrapposizioni, zero testo
oltre il bordo, nessuna pagina quasi vuota nuova; la serata passa da 101 a 102
pagine, il Drappo da 92 a 94, il Palio da 61 a 62.

**Un errore mio, preso dalla misura.** La prima versione teneva in colonna ogni
tabella più alta di 20 cm a tutta pagina, anche quelle da cinque colonne: a
pagina 26 dell'Abbazia le celle si stampavano una sopra l'altra. Il limite ora
vale solo per le tabelle da due e tre colonne.

**I PDF della #169 rifatti** (booklet della serata 102 pagine, fogli dei
giocatori 18, volume del −1000 40) sono stati consegnati al DM in chat; sono
artefatti e non entrano nel repo.

⚠️ **Quello che resta.** Quanto lontano finisce un float non lo controlla
nessun cancello: è la misura di questa sezione, da ripetere quando si cambia il
tema. Le 20 tabelle a due o più pagine dal loro testo si possono avvicinare
solo spezzando le sequenze di tabelle nei master, o forzandone qualcuna in
colonna col marcatore: è una scelta di chi scrive, caso per caso.


---

## 14 · Il punto al 30 settembre: cosa si è mosso, cosa resta, cosa aspetta il DM

Il DM, il 2026-09-30: *«fai un piano che segna il progresso e cosa rimane da
fare, aggiornando tutto l'elenco dei piani»*. La lista viva resta il §0; questa
sezione è la fotografia della tornata 27-30 settembre, con i numeri, per chi
riparte da una chat nuova.

### 14.1 · I piani, contati da `INDEX.md`

| Stato | Quanti |
|---|---:|
| ✅ o 🟢 chiusi o eseguiti | 32 |
| 🟡 in corso | 11 |
| 🔵 pianificati o proposti, non partiti | 8 |
| **In tutto** | **51** |

### 14.2 · Cosa si è mosso in questa tornata

| Piano | Prima | Adesso | Con cosa |
|---|---:|---:|---|
| LETTORE-E-PLAYTESTER | ~75% | **~85%** | DEF-4 pronto per la serata (#183); DEF-5 ai passi 1-6 del ciclo; quattro letture cieche su DEF-4, due su DEF-5; la prova cieca di `P-ABITATO` riuscita; il banco e la regola dei riposi (#183) |
| MASTER-DEF-ARC08-ARC09 | 0%, aperto il 27 | **~15%** | D1-D3 decise, A1 approvato, A2 misurato, ADR-0075 (#182) |
| Le decisioni del DM | 67 chiuse, 22 aperte | **80 chiuse**, 34 aperte | chiuse D1-D6, D11, D13, D18, D20, D22, D24 di LETTORE e la forma di D28; aperte le nuove che le letture hanno trovato (D12-D33) |

Le misure della prosa, sulle letture cieche (agenti diversi a ogni giro):

| Master | Lettore, 🔴 | Playtester, 🔴 |
|---|---|---|
| DEF-4 | 2 → 2 → 1 → 1 | 2 → 1 → 0 → 0 |
| DEF-5 | 3 → **1** | 1 → **1** |

Il 🔴 che resta in DEF-4 è nuovo (D33, la profezia); quello di DEF-5 è l'orologio
(D31). Tutti e due sono canone.

**Il giro delle quattro letture** (30 settembre, notte; lettore · playtester ·
developer · DM a freddo, 🔴):

| Master | Lettore | Playtester | Developer | DM a freddo |
|---|---:|---:|---:|---:|
| DEF-4 | 2 | 1 | 1 | 1 |
| DEF-5 | 0 | 1 | 1 | 0 |

Corretti nel testo quelli che il testo risolveva. Restano D38 (DEF-5, la Fase 0),
D39 (DEF-4, l'orologio senza margine) e le mappe M7-B e M7-C (lotto D28).

### 14.3 · I piani aperti, e da dove riparte ognuno

| Piano | % | Il prossimo passo | Chi |
|---|---:|---|---|
| LETTORE-E-PLAYTESTER | ~88 | F4: il giro 2 su DEF-4 e DEF-5, dopo D38, D39 e il lotto mappe; il quiz di DEF-5 dopo D10; F5 gli stand-alone | DM, poi agente |
| MASTER-DEF-ARC08-ARC09 | ~15 | A3: il canone di ARC-08 contro lo stato del tavolo, dopo F4 | agente, poi DM |
| REVISIONE-ARC07 | ~95 | le sessioni giocate al tavolo | tavolo |
| REVISIONE-TRASVERSALE | ~90 | T8 e T9, legati al tavolo | tavolo |
| DRAPPO-DI-TARSILIA | ~90 | L9 il collaudo a freddo della tavola di fuori; poi L6 e il tavolo | agente, poi DM |
| MISURA-EDITORIALE-STANDARD | ~90 | la soglia κ ≥ 0,6 prima di entrare in CI | agente |
| INTEGRAZIONE-PIPELINE-MAPPE | ~92 | collaudo al tavolo | DM |
| RIPRESA-PR-ABBANDONATE | ~88 | 3d (D2, il collaudo SDXL) e 4d-4h, uno alla volta | DM, poi agente |
| PORTARE-IL-MESTIERE-DEI-BANCHI | ~25 | S2-S4 sui master, dopo D3 | agente |
| PRATICHE-DI-INGEGNERIA | 25 | PI-6, PI-2, PI-5, PI-4 | agente |
| CICLO-DI-SESSIONE-E-MENU | ~12 | la Fase 0, dopo D1-D6 | DM, poi agente |
| RICONCILIAZIONE-PR-APERTE | 3/7 | le due decisioni sul simbolo ⬛ | DM |
| PIPELINE-IBRIDE | 10 | D1-D4 | DM |
| EDITOR-VISUALE-MAPPE | ~9 | E0 | agente |
| MARCATURA-DEGLI-INCONTRI | 0 | il primo lotto con `validate_modules --tetto-el` | agente |
| LEVEL-DESIGN-E-INQUADRATURA | 0 | C2, dopo il linter di VENDIBILITA | agente |
| RICERCA-MESTIERE-CARTOGRAFO | 0 | le quattro domande al DM, una bloccante | DM |
| VENDIBILITA | 7 | **non autorizzato**: si parte solo su richiesta del DM | DM |
| **Il lotto mappe D28** (dentro LETTORE) | 0 | sezione a livelli di Hammerfist 372 e griglie di fucina, gallerie, alchimista, cappella, armeria | agente, con `rumblingstone-mapmaking` |

### 14.4 · Le PR aperte che non sono su `main`

Il DM ha chiesto di fondere prima le PR con piani aperti. Misurato il
2026-09-30, con la storia intera (`git merge-tree`):

| PR | Indietro rispetto a `main` | Conflitti se si fonde | Cosa contiene che non è già su `main` |
|---|---:|---:|---|
| **#99** (audit, dati di campagna) | 394 commit | **52 file** | solo i lotti 4d-4h di RIPRESA-PR, da portare uno alla volta; il resto è già stato portato |
| **#106** (catena raster, Blender) | 379 commit | **12 file** | solo 3d, che aspetta la D2 del DM (il collaudo SDXL); il resto è su `main` |

**Non si fondono.** Fonderle riporterebbe su `main` versioni di agosto di file
riscritti dopo (i master DEF, la CI, la guida delle immagini), e due ADR con
numeri già presi. RIPRESA-PR le tiene aperte apposta come segnaposto
(§4.12, tabella delle PR): si chiudono quando l'ultimo lotto che ne viene è su
`main`. Dal 2026-10-02 sono le sole due PR aperte (§14.4-bis); la #184 è fusa.

### 14.4-bis · Il giro di merge del 2026-10-02

Il DM: *«se verde mergia anche le PR precedenti aggiornando i piani con quello
fatto e da fare, perché il main è indietro di molte PR»*. Le PR aperte erano
diciassette. Sono entrate tutte con la #200, fusa il 2026-10-02 (`5f3cb520`),
che le conteneva; GitHub le ha chiuse come fuse:

| PR | Come entra | Cosa porta |
|---|---|---|
| #186, #189-#199 | già dentro il ramo della #200 (serie impilata) | PIANO-AGENT-SKILLS-ESTERNE L0-L9, L8-bis, D1-D11 |
| #187 | fusa nel ramo, conflitti risolti | il giro delle quattro letture su DEF-4 e DEF-5 e i loro rapporti; il developer come quarta lettura. Il DM a freddo resta quello della serie (D2, D9, D12), e i codici `D-*` della bozza sono tradotti in `dm-a-freddo.md` |
| #188 | fusa nel ramo, conflitti risolti | F2.10 (il box di luogo e l'area chiave di *Dungeon*), quattro norme nuove, il piano BOX-DI-LUOGO con le sue D1-D6 |
| #200 | la PR del giro | D12, L11, L12: il voto sulla scrittura, `ciclo_prosa.py`, ADR-0077, gli indici dei references, il lotto D13 da approvare |

Restano aperte **#99 e #106**, per la ragione di §14.4: sono i segnaposto di
RIPRESA-PR, e fonderle riporterebbe su `main` versioni di agosto.

**Da fare, in ordine.**

1. Il DM approva il lotto D13 (`plans/scrittura/revisioni-D13/LEGGIMI.md`):
   undici documenti, 23 modifiche applicabili con `applica --auto`, quattro
   da guardare.
2. D17: «sembra» seguito dalla smentita è lecito? Decide se i cinque box
   rimasti restano come sono.
3. Le quattro incoerenze di canone che le corse di L11 e L12 hanno trovato da
   sole (`plans/scrittura/RISULTATI.md`): il carry-over su Fauci nell'handout,
   le pozioni antiche fra DEF-4 e DEF-5, il «−2 COS» di Thorik in `ARC08-11`,
   le tre descrizioni del Rubino.
4. Le D1-D6 di BOX-DI-LUOGO, che sbloccano la chat editoriale di quel piano.
5. Una corsa del DM a freddo su DEF-5 con le undici voci `P-*` (D12).
6. RIPRESA-PR 4g e 4h, che chiudono #99 e #106.

### 14.4-ter · Ripartire in una chat pulita (2026-10-03)

Il DM: *«aggiorna tutti i piani in modo che si può continuare in una chat pulita»*.
Su `main` non c'è niente di aperto a metà: la #215 è fusa, le sole PR aperte
restano #99 e #106 (§14.4). Il da fare, **in questo ordine**, e chi lo sblocca:

| # | Cosa | Chi | Dove sta |
|---|---|---|---|
| 1 | **Approvare il lotto D13** (undici documenti di revisione, 23 modifiche con `applica --auto`, quattro da guardare) e rispondere a **D17** («sembra» seguito dalla smentita) | DM | `plans/scrittura/revisioni-D13/LEGGIMI.md` · §14.4-bis |
| 2 | **La coda del secondo lettore**: il genere di *Torre* e quattro concordanze (decide il DM); poi gli accenti di 57 schede del Bestiario (lotto meccanico) e i 32 campi troncati nei prompt immagini | DM, poi agente | [CODA-DEL-SECONDO-LETTORE](PIANO-CODA-DEL-SECONDO-LETTORE-2026-10.md), col suo primo messaggio per una chat pulita |
| 3 | **Il collaudo di Drappo L9**: due letture a freddo, dry-run, booklet rigenerati | agente | DRAPPO Lotto 9 |
| 4 | **Le quattro incoerenze di canone** trovate da L11 e L12 (Fauci nell'handout, le pozioni antiche fra DEF-4 e DEF-5, il «−2 COS» di Thorik in `ARC08-11`, le tre descrizioni del Rubino) | DM, poi agente | `plans/scrittura/RISULTATI.md` |
| 5 | **LETTORE F4**: il giro 2 su DEF-4 e DEF-5, dopo D38, D39 e il lotto mappe D28; poi **MASTER-DEF A3**, che aspetta F4 | DM, poi agente | LETTORE-PLAYTESTER · MASTER-DEF |
| 6 | **Le D1-D6 di BOX-DI-LUOGO** e **una corsa del DM a freddo su DEF-5** con le undici voci `P-*` | DM | BOX-DI-LUOGO · D12 di AGENT-SKILLS |
| 7 | **RIPRESA-PR 4g e 4h**, che chiudono #99 e #106 | agente | RIPRESA-PR |

Le decisioni aperte al DM sono **17** (`decisioni_dm.py --check`); le più
urgenti per la prossima serata sono D31 e D33 di LETTORE-PLAYTESTER. VENDIBILITA
resta **non autorizzato**.

### 14.5 · Le decisioni al DM, per piano

> ⚠️ **Superata il 2026-10-02**: le aperte erano 17, non 34 (§15.1). Il conto vivo è sempre in §4.

Sono **34**, in §4 con la proposta di ognuna. Contate per piano:

| Piano | Aperte | Le più urgenti |
|---|---:|---|
| LETTORE-PLAYTESTER | 20 | **D31** (l'orologio di DEF-5) e **D33** (la profezia), perché toccano la prossima serata; poi D12, D14-D17, D19, D21, D23, D29, D30 su DEF-4 |
| CICLO-SESSIONE | 6 | D1-D6, che sbloccano la Fase 0 |
| PIPELINE-IBRIDE | 4 | D1-D4 |
| RIPRESA-PR | 2 | D2 (Gemini o SDXL), D11 (il perimetro dell'edizione) |
| MESTIERE-BANCHI | 1 | D3 (si spezzano i box dei master già giocati?), che è anche la D9 di LETTORE |

> ⚠️ *(2026-10-10)* Questa tabella è la fotografia del 2026-09-30 e non si
> aggiorna: CICLO-SESSIONE (D1-D7), PIPELINE-IBRIDE (D1-D4) e MESTIERE-BANCHI
> (D3) sono state decise il giorno stesso, e la D12 di RICERCA-MESTIERE il
> 2026-10-09. Le aperte di oggi sono in §4, generato da `decisioni_dm.py`.

E fuori da §4, perché sono marcature e non decisioni: le **44 `[INFERRED]` di
DEF-4** e le nuove di DEF-5, e `state.md` sul ramo del gruppo (il Rubino che
completa la Corona, i log delle serate del 25-27 settembre).

### 14.6 · Il primo comando di una chat nuova

```bash
git fetch --prune origin
python3 scripts/decisioni_dm.py --check      # le decisioni aperte, allineate
python3 scripts/fase1.py <il file che tocchi> # sempre, prima di toccare
```

Poi si legge il §0 di questo file, e la riga ▶ dice da dove si parte.

---

## 15 · Il 2026-10-07: la #206 completata e chiusa, le Dependabot fuse

Il DM, il 2026-10-07: *«controlla se c'è qualcosa di appeso e non completato
nella 206, completalo se ha senso […] chiudi la 206, se serve mergia, e mergia le
dependabot una alla volta»*.

La #206 (aperta il 2026-10-02) era il controllo di questo file contro commit, PR
e rami dopo la #205. Non si poteva fondere: è in conflitto con tutto quello che
STATO ha preso dopo (la #213, la #214, la #215, la #217, la #218). Il suo §15
fotografava il 2026-10-02, e i numeri sono quelli di quel giorno; qui resta il
loro esito, e il contenuto che valeva ancora è entrato in §0.

### 15.1 · Cosa è stato portato dalla #206

| Dalla #206 | Oggi |
|---|---|
| La riga ✅ della configurazione degli agenti (#201-#203, #205) | in §0, con la correzione dei due tool MCP (§15.2) |
| Le tre righe 🙋: il lotto D13 e la D17, le quattro incoerenze di canone, le D1-D6 di BOX-DI-LUOGO | in §0, invariate: sono ancora aperte (17 decisioni in §4, le stesse di allora) |
| La correzione delle righe di D26 (fatta con L4, #193), di DEF-1/2/3 (D34 e D9 decise), degli `[INFERRED]` (51 in DEF-4, 12 in DEF-5) | in §0, ricontate il 2026-10-07: gli stessi numeri |
| I nove rami fusi o portati, cancellati dal DM il 2026-10-02 con tag e bundle | in §0 come ✅, e le tre righe di quel giorno nel CHANGELOG |
| §14.5 superata (34 decisioni contro 17) | marcata in §14.5 |
| Le sei PR di Dependabot su `upstream` (EarlRagnar78 #19-#24) | superato: Dependabot ha aperto le stesse su `origin` (#207-#212), e quelle si sono fuse (§15.3). Le sei su `upstream` le chiude il DM |

### 15.2 · Cosa la #206 lasciava aperto, e ora è fatto

| Voce | Cosa si è fatto |
|---|---|
| **Due tool MCP scartati** (`campaign_branch`, `dm`): il nome della proprietà era l'elenco delle scelte, «status\|guard\|ensure», e l'API accetta solo `[a-zA-Z0-9_.-]` | `mcp_key` in `scripts/tools_manifest.py` chiama «comando» un sottocomando e toglie i caratteri non ammessi; `docs/tools/mcp-tools.json` rigenerato; due test in `test_mcp_server.py`. `mcp_server.py --self-check`: 89 su 89 |
| **Le voci del registro dei rami senza più un ramo**: otto per la #206, dieci oggi | tolte da `plans/contenuti-nei-rami.json`: il registro va potato quando una voce non trova più niente (lo dice lo script). La loro storia sta nei commit |
| **`fase1.py` in un clone shallow** | `contenuti_nei_rami.shallow()`: in un clone shallow i due script lo dicono e non misurano. Era il caso di questa sessione: shallow davano 61 file e decine «senza posto», con la storia intera 42, tutti col loro posto. Un test |

E una che la #206 non poteva vedere: la **#216**, aperta il 2026-10-03, aveva
nove file senza posto nel registro, e `contenuti_nei_rami --check` era rosso.
Ora è registrata come «in volo», e il controllo è verde e senza avvisi.

### 15.3 · Le Dependabot, una alla volta

Le sei PR di Dependabot (#207-#212) avevano la CI rossa per una sola ragione: il
cancello della regola d'oro (`check_plans_discipline`) boccia un file
strutturale toccato senza una riga nel CHANGELOG, e Dependabot non la scrive. A
ognuna, prima del merge, si è allineato il ramo a `main` e aggiunta la riga; poi
la CI verde, poi il merge, e la successiva solo dopo.

| PR | Cosa | Effetto |
|---|---|---|
| #207 | `actions/checkout` da v4 a v7 | la riga di Node.js 20 di PI-3 comincia a chiudersi |
| #208 | `actions/setup-python` da v5 a v7 | idem |
| #209 | `actions/upload-artifact` da v4 a v7 | idem: con le tre, nessuna azione della CI gira più su Node.js 20 |
| #210 | `Pillow>=12.3.0` | |
| #211 | `pip-audit>=2.10.1` | |
| #212 | `tiktoken>=0.14.0` | |

⚠️ Per le prossime PR di Dependabot vale lo stesso: la riga nel CHANGELOG la
aggiunge chi la fonde. Se il DM preferisce che il cancello le esenti, è una riga
in `check_plans_discipline.py`, e la decide lui.
