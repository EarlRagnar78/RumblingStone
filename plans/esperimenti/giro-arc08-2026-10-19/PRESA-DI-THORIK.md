# Arco 08: la presa di Thorik (2026-10-19)

Ramo `claude/project-thread-e860p0`. Nessun commit e nessun push: le modifiche sono nel working tree. Fonte: `PROPOSTA-FAUCI-PRESA-DI-THORIK.md` e `SKULLCRUSHER-VS-FAUCI.md` sul ramo `claude/project-thread-ep4auu`, adattate alla versione F di Fauci (D9) che questo ramo ha già.

## File cambiati

| File | Cosa |
|---|---|
| `ARC08-02` §1 (G) | *Tattiche* riscritte; voce nuova **«La presa di Thorik»** `[CANONE — DM 2026-10-19]`, con i numeri ricalcolati e la battuta di Fauci; coda all'Odio della stirpe; *Volteggiare* → *Fluttuare* nei talenti |
| `ARC08-01` (A) | la stessa scheda copiata parola per parola; *corrompere acqua* con la gittata SRD (quella della Presenza, prima «30 m»); riga «Round 18-20» delle tattiche in combattimento; 4A, *Tattiche*; «ROUND 18-23» (perché scende, dove, *Ghermire* contro i PG in volo, il duello); timeline della Sessione 4; Scheda Boss 1; nota di regia «l'eco del re» nell'incontro 2B; punto mancante nella nota «Verifica» |
| `hammerfist_encounters-…-final.md` (B) | 4A *Tattiche*, «ROUND 18-23», timeline, eco del re nel 2B: gli stessi testi di A |
| `ARC08-10` §4.1 e §4.2 | la picchiata dei round 18-20 è la presa; il punto 3 di §4.2 dice perché lo prende in bocca prima di finirlo |
| `ARC08-03` | registro: Fauci da «/ 312» a «/ 337 (meno il carry-over)», più la casella della presa |
| `Mappe/Hammerfist-L3-…` MAPPA 4 | COMPRENSIONE, `@path` (ora G17 → AD37 → AD31: picchiata sulla linea, caduta nella zona ⚡), `@zone`, VISTA ALTITUDINI, FASE 5, AMBIENTE, stato C |
| `Mappe/Atlante-…` | timeline, tattiche di Fauci, «Round 18-20», PG in volo |
| `Mappe/rendered*/…map05…svg` | MAPPA 4 rigenerata nei due temi |
| `Bestiario/villain/Fauci_di_Palude.md` | i due potenziamenti segnati come tali, i talenti di volo con *Fluttuare*, la **Firma**; benchmark del morso da +35 a +33 |
| `scripts/monster_catalog.yaml` | rigenerato (cambia solo il campo note di Fauci) |

## Come sta insieme alla versione F

Il round 18 è la picchiata con Attacco in Volo: morso e presa su Thorik, sulla linea ⚔ o contro Gorthak. Al round 19 Fauci sale con lui in bocca, al 20 soffia sui compagni e lo lascia cadere sulla zona ⚡, alle spalle della punta. Al 21 atterra lì per finirlo, e il duello dei round 21-23 resta com'era. La zona ⚡ adesso è il punto dove cade Thorik e dove atterra il drago. Se Fauci va sotto i 100 pf prima, scende prima; se Aegis Fang non ha mai cantato né colpito, niente presa.

## Che cosa dice l'SRD (copia locale `srd-v3.5-md`)

| Regola | Testo SRD | Proposta |
|---|---|---|
| *Snatch* | presa come la presa migliorata, su morso o artiglio; stretta automatica da **tre** taglie in giù; chi è **in bocca** non ha i Riflessi contro il soffio; lasciarlo è un'azione gratuita, scagliarlo un'azione standard (1d6 × 10 piedi, 1d6 ogni 10 piedi, o la caduta se è di più) | giusta. **Il −20 non sta in *Snatch***: sta in *Improved Grab* (tipi e capacità speciali), insieme al danno del morso a ogni prova di lotta vinta e al trasporto della preda «se ne regge il peso» |
| *Improved Grab* | prova di lotta **contrapposta** gratuita; con la sola parte del corpo, −20 e non è in lotta, tiene la Destrezza, minaccia, usa gli altri attacchi | la proposta non diceva che la presa è contrapposta: a +23 contro il +18 di Thorik **riesce tre volte su quattro**, non sempre |
| *Hover* | ferma il moto in avanti con un'azione di movimento, poi vola in qualunque direzione a metà velocità; se comincia il turno fermo, ha l'azione di round completo; niente attacchi d'ala | giusta. Che fermarsi e salire stiano in una sola azione di movimento è una lettura, ed è scritta come tale |
| *Flyby Attack* | un'azione di movimento, anche in picchiata, e un'azione standard in un punto qualsiasi | la proposta e la versione F dicevano «carica in volo (+2) **e** Attacco in Volo»: in 3.5 non si sommano, la carica è un'azione di round completo. Corretto in A e B |
| Lotta | si attacca solo senz'armi, con armi naturali o leggere, a −4; fuga con prova di lotta al posto di un attacco o con Artista della Fuga (azione standard); attivare un oggetto non chiede prova; la prova di lotta è «**come** un tiro per colpire in mischia» | giusta sull'ascia. Sbagliata la motivazione dei due `[INFERRED]`: la proposta diceva «la prova di lotta non è un tiro per colpire», l'SRD dice che è *come* un tiro per colpire e non dice se bonus e penalità ai tiri la toccano |
| Caduta | 1d6 ogni 10 piedi, al massimo 20d6 | giusta |
| *Corrupt water* | 1 al giorno, gittata pari al raggio della Presenza | il «30 m» di A era sbagliato: ora è il raggio della Presenza |
| Presenza | 30 piedi per categoria d'età (adulto maturo: 63 m) | i 90 m sono un potenziamento, già segnato in G, A e ora nel Bestiario |
| Manovrabilità scarsa | salita a 45° e metà velocità | usata per la risalita del round 18 |

## I numeri, dalla scheda di G §1

- **Morso** in picchiata con Attacco in Volo: +33, più 4 dell'Odio, **+37**, 2d8+14 (media 23), critico 19-20. Con una carica sarebbe +39, ma la carica chiude il movimento. La proposta diceva +39 «(+35, più l'Odio)»: +35 era il morso prima della correzione del 2026-10-16.
- **Lotta**: BAB 25, FOR +10, Enorme +8 = **+43**; con la sola bocca **+23**.
- **Thorik** in lotta: +18 (BAB 13, FOR 20, i numeri che il repo usa; la sua scheda non c'è). Presa che riesce: 74%. Fuga a round con +18/+13/+8: circa 36%.
- **Il conto se nessuno lo ferma**: morso 23, una stretta 17 (23 × 0,74), soffio 14d4 senza TS 35, caduta da circa 35 m 11d6 = 38. **Circa 113.** Versione massima (sale ancora al round 20): caduta da circa 55 m, 18d6 = 63, conto **circa 138**. Il tetto di 20d6 è a 60 m.
- *Dissolvi magie* contro la pozione di *volare* di un Thorik in volo: d20+7 contro CD 16, 60%.

## Il nome «Thorik»

Sul ramo `campaign-group-rumblingstone` l'ultimo log è la sessione 4 del 2026-09-25: il tavolo è alla notte a ≈372 DR, e il duello con Skullcrusher **non è ancora giocato**. Il nome resta `[INFERRED]`: Fauci dice «Thorik» solo se al duello il tavolo l'ha dato a Skullcrusher, altrimenti «Portatore». Una sola riga di dialogo, fuori dai box: il numero dei box di ARC-08 resta 88.

## I punti ancora `[INFERRED]`, con la raccomandazione

| # | Punto | Raccomandazione (versione più forte, ma giocabile) |
|---|---|---|
| 1 | Una presa per incontro | **Una**, più una seconda solo se Thorik si libera da solo prima del round 20: il drago non molla la preda che gli è scappata. Due giri interi (circa 226) uccidono un Thorik da 155 pf |
| 2 | Lo *Scosso* del Bane sulla prova di lotta | **Sì, −2 alle prove di lotta di Fauci**, per simmetria col punto 3: l'SRD chiama la prova di lotta «come un tiro per colpire» |
| 3 | L'Odio della stirpe sulle prove di lotta | **Sì, +4**: presa a +27 contro +18 (86%), e la fuga di Thorik scende a circa una su sei a round. È la lettura più forte che l'SRD regge; con il punto 2, nel round dello Scosso, Fauci è a +25 (80%) |
| 4 | Il nome «Thorik» | **Sì se il tavolo l'ha dato** al duello del ≈372 (Skullcrusher li chiede): è un'eco gratis. Se no, «Portatore», e il nome lo impara al 2B dai nani che lo chiamano |

## Contraddizioni sistemate

- *Corrompere acqua* a volontà e Presenza a 90 m: non abbassate. Segnate come potenziamento in G e A (c'erano già) e ora nel Bestiario.
- *Volteggiare* → **Fluttuare**, il nome della scheda di Skullcrusher e del Bestiario sul ramo ep4auu: G, A, B, MAPPA 4, Atlante, Bestiario di Fauci. In ARC-08 non resta nessun *Volteggiare*.
- pf su 312: restava il registro di ARC08-03 (ora 337). Gli altri 312 sono nella nota `<!-- storico -->` del Bestiario e nell'ERRATA, e restano.
- Le *Tattiche* di A dicevano «atterra solo se costretto», G «sotto i 100 PF»: ora dicono la stessa cosa.

## Da guardare fuori da ARC-08

- **Su questo ramo** `ARC07-DEF-4` A.1 dà ancora *Ghermire* a Skullcrusher: lo scambio con *Virata* sta solo sul ramo ep4auu. La nota del Bestiario di Fauci rimanda ad A.1 per «combatte in passata e dice i nomi», e torna vera quando ep4auu arriva qui.
- `07_…/CORREZIONE-Boss-Fauci.md` (non toccato) ha ancora «Vendetta bloodline» e l'esito UCCISO dato per fatto.
- *Corrompere acqua* a volontà, con la gittata della Presenza (90 m), può guastare le cinque pozioni di *volare* nello zaino dei PG (Volontà CD 25 per oggetto, SRD). È la mossa più terrificante che la scheda già permette, e nessun file la scrive: la decide il DM.

## Controlli

| Comando | Esito |
|---|---|
| `validate_maps.py` | ✓ 53 SVG, allineati nei due temi |
| `validate_modules.py` | ✓ 5 master, 0 errori (l'avviso su ARC07-DEF-2 c'era già) |
| `validate_bestiario.py` | ✓ 190 statblock, catalogo in sync dopo `build_monster_catalog.py` |
| `conformita_statblocchi.py --master` A, B, G | 3 file, 0 conti che non tornano |
| `validate_docs.py --sorgenti` | ✓ 1088 documenti |
| `copertura_scene.py --check` | ✓ 15 rilievi |
| `domande_developer.py --check` | ✓ 18 rilievi |
| `verifica_sezione6.py --check` | ✓ nessuna riga mente; box di ARC-08 invariati (88) |
| `pytest scripts/tests` | ✓ 1943 passati, 8 saltati |
