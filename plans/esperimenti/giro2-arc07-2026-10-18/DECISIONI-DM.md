# ARC-07, giro 2 · le decisioni che restano al DM

Fonti:
- le sezioni «Decisioni per il DM» e «Seconda passata» dei cinque `giro2/DEF-*/FIX.md`;
- le domande aperte di `rifacimento/APERTI.md`;
- gli `[INFERRED` ancora presenti in `07_il Portale Della Forgia Eterna/ARC07-DEF-{1..5}-*.md`, apparati esclusi;
- il **canone giocato sul ramo di gruppo** `origin/campaign-group-rumblingstone` (ADR-0090): `campaign/state.md` e `campaign/state.yaml` del ramo, e il diario `campaign/sessions/2026-09-25_session-4.md`, che è identico a `/mnt/project-files/sessione-2026-09-25/2026-09-25_session-4.md`.

Il `state.md` di `main` resta indietro di proposito (ADR-0007). Per sapere dove sta il tavolo vale il ramo, che dice questo: la sessione 4 del 2026-09-25 ha giocato tutto DEF-3 (P3B) e DEF-4 fino al giro della fortezza. Il P5 riprende dalla notte, dalla Scena 5, con 3 tacche su 8, e nessuno ha dormito. Quindi DEF-1, DEF-2 e DEF-3 sono giocati; DEF-4 è in corso e DEF-5 è da giocare.

**I conti.** Le domande di partenza sono 57: 55 dei correttori (DEF-1 D1-D11, DEF-2 D1-D13, DEF-3 D1-D13, DEF-4 D1-D9, DEF-5 D1-D9) e 2 di `APERTI.md`.
- Unendo i doppioni ne spariscono 4: DEF-2 D2 e DEF-3 D7 diventano G2-04; DEF-1 D7, DEF-2 D10 e DEF-3 D8 diventano G2-18; DEF-2 D3 e DEF-3 D5 diventano G2-06.
- Il primo giro ne aggiungeva 2, G2-03 e G2-07, e arrivava a 55.
- Il controllo sul ramo di gruppo ne chiude 3: G2-02 e G2-13 le ha risolte il canone giocato, e G2-03 non era una contraddizione. Ne apre 3 nuove, G2-56, G2-57 e G2-58, che vengono dal diario.
- **Restano 55 decisioni aperte.** I codici non sono stati rinumerati, perché ogni codice resti tracciabile fra un giro e l'altro.

**Come leggo la regola del DM («la versione più potente e terrificante»).** Vince l'opzione più dura fra quelle che non contraddicono un tag `[CANONE — DM …]`, il canone giocato del ramo o `state.md`, e che lasciano in vita la meccanica che la scena ha scritto. In tre casi l'opzione più dura renderebbe una meccanica impossibile (G2-41, G2-42, G2-33), e lì lo dico. Ho cambiato la raccomandazione del correttore in cinque decisioni: G2-01, G2-04, G2-16, G2-38 e G2-44.

**Gli `[INFERRED` nei master di `main`: 24, su 23 righe.** DEF-1 ne ha 6 (5 righe), DEF-2 9, DEF-3 5, DEF-4 0, DEF-5 4. Il conto è `grep -o "\[INFERRED" ARC07-DEF-[1-5]-*.md | wc -l`. Nessuno di questi tag lo chiude il canone giocato. La mappa è in fondo. L'eco E-07g del ramo ne ha un altro, che è nello stato e non in un master: va con G2-58.

---

## Già decise dal canone giocato

Queste non si chiedono più al DM: diventano correzioni dei master, con la fonte. Il «ramo» è `origin/campaign-group-rumblingstone`. Il «diario» è `campaign/sessions/2026-09-25_session-4.md` di quel ramo.

### Le correzioni da fare

**Stato: K1-K4 applicate** nel master `ARC07-DEF-3-RESURREZIONE-HELLA.md`. Il canone nuovo è marcato `[CANONE GIOCATO 2026-09-25]` dentro `<!-- storico -->`. I gate dopo le correzioni: `misura_craft --box` dà per DEF-3 20 box, 0 oltre le 12 righe, 0 parentesi, 0 con più di un nome; `validate_modules` 0 errori; `test_storico` 8 su 8; `validate_prosa` esce con 0 e non segnala niente su DEF-3.

| # | Era | Master e riga | Testo attuale | Testo nuovo | Fonte |
|---|---|---|---|---|---|
| K1 ✅ applicata | G2-02 | DEF-3 §0, «Come arrivano», righe 48-49 | «Hella, dall'altro lato, **ha già sentito Thorik dire il suo nome nel sonno**.» | «Hella, dall'altro lato, **ha già sentito Tordek dire il suo nome nel sonno**.» | Il foglio della giocatrice stampato per la serata: `homebrew/sessione-resurrezione-mille-anni/06-ECHI-HELLA.md` r. 23, «La voce è quella di **Tordek**», che c'è dal commit 75bc7e2b del 2026-09-24 («booklet della serata»), ed è uguale in `ARC07-SERATA-GIOCATORI.hb.md` r. 142. Al tavolo del 25 settembre la giocatrice ha avuto quel foglio. Il diario non registra un'altra voce. Lo confermano anche il §1 di Tordek e il §7 di DEF-3. |
| K2 ✅ applicata | G2-13 | DEF-3 §11 A, dopo la riga 1387 («**TOTALE beat** … ~1.900/PG») | (nessuna riga su Hella) | «> I PX del beat li prende anche Hella, tutti, come gli altri tre: è morta fino allo Step 6, ma risponde alla Custode e fa il racconto.» Dentro `<!-- apparato -->` va il rimando: «(giocato il 2026-09-25: 1.900 a testa a tutti e quattro, Hella compresa)». | Il diario, «XP awarded»: rito 800, scelta-costo 400, Debito 400, Racconto 300, più le Scene 1-4 di DEF-4 600, «**Total**: 2.500 xp a testa, a tutti e quattro (Hella compresa)». |
| K3 ✅ applicata | (nuova) | DEF-3 §6, righe 1014-1018 | «Se un PG si offre («lo porto io»), la Custode non lo guarda: il debito è della radice, e la radice è di Hella. L'offerta resta detta e lo spirito la sente, ma la frase che sceglie resta a Hella. Al §8 lei ricorda chi si è offerto.» | Il testo resta, e sotto si aggiunge, dentro `<!-- storico -->`: «Al tavolo del 2026-09-25 è andata così, ed è canone di quel gruppo: Thorik ha detto che il prezzo lo paga lui, senza sapere quale sia. La Custode ha preso nota del suo nome. È un quarto ramo, fuori da A, B e C, e il prezzo è ancora da decidere (eco E-07g).» | Il diario, «Key decisions» («Thorik prende su di sé il Debito della Radice … un quarto ramo, fuori da A/B/C») e «Next session hooks» («La Custode delle Radici ha preso nota del nome di Thorik»); il ramo, `state.md` §7.E, E-07g. |
| K4 ✅ applicata | (nuova) | DEF-3 §8, righe 1176-1177 | «Se un PG si è offerto di portarlo (§6), Hella lo guarda: *«Ti sei offerto. Non era tuo da portare, e lo sapevi.»*» | La battuta resta, e dopo si aggiunge, dentro `<!-- storico -->`: «Con Thorik che il debito se l'è già preso, come al tavolo del 2026-09-25, il suo «lo pago io, non voi» apre una discussione fra loro due e non chiude la scena.» | Il diario, «DM notes»: «con Thorik che l'ha già preso, la battuta diventa una discussione fra loro, non una chiusura». |

K3 registra quello che è successo, e lascia intera la regola del 2026-10-18 («Chi risponde: l'ultima parola è di Hella»). Se il quarto ramo valga anche per un gruppo nuovo resta una scelta del DM, ed è dentro G2-58.

### Verificate sul ramo, nessuna correzione

- **G2-03 non era una contraddizione.** Il `state.md` di `main` è indietro per regola (ADR-0007, ADR-0090). Sul ramo: P3B è giocato il 2026-09-25, P5 è in corso dalla notte, 3 tacche su 8. Le righe di DEF-4 sul «tavolo del 25 settembre» (r. 377, 740, 800) dicono lo stesso. La decisione è tolta.
- **L'Eldritch Blast di Artemis.** Sul ramo, dopo il Dono a Hella, è 6d6 per sempre. DEF-3 dice lo stesso in tutti i punti: r. 238, 674, 723 e 795 («da 7d6 a 6d6»), r. 1364 («resta a 6d6 per il resto della campagna»), r. 884 (torna a 7d6 solo se il Dono si annulla). Il correttore di DEF-3 ha respinto DM#11 citando il 7d6 dal `state.md` di `main`. Il rifiuto regge, perché anche il ramo dà 7d6 *prima* del rito (7 → 6), ma la fonte da citare è il ramo. DEF-4 e DEF-5 non scrivono i dadi dell'Eldritch Blast, quindi non c'è niente da allineare: chi ci aggiunge un numero scriva 6d6.
- **I tre Doni.** Il ramo e il diario coincidono con DEF-3 §5 (r. 236-238): Thorik −1 CA permanente e lo Scudo del Custode a Hella, Tordek l'Ancoraggio (RD 3/adamantino a Hella), Artemis 1d6 di Eldritch Blast (il Rovo Eldritch). Il `state.md` del ramo scrive «il +2 di deflessione della Corona è passato a Hella, lui resta a −1 CA», mentre il master scrive «metà del +2». La CA che resta a Thorik è la stessa, ma la frase del ramo si legge male: è da sistemare in `state.yaml`, non nel master.
- **Il sonno dopo il rito (G2-01).** Al tavolo nessuno ha dormito: il gruppo ha attraversato subito (diario, «Summary»; ramo, «nessuno ha dormito»). La contraddizione fra DEF-2 e DEF-3 resta, ma riguarda solo i gruppi futuri.
- **Il Torque di Thorek I.** Il diario dice che non è stato dato al consiglio: lo consegna il re alla Scena 12, Momento 5. DEF-4 r. 3439 dice già la stessa cosa `[CANONE — DM 2026-10-11]`.
- **L'ascia e lo scudo del capo fabbro tornano nel 1372.** DEF-4 r. 1454 e r. 1516 lo dicono già `[CANONE — DM 2026-10-06]`. G2-14 ora chiede solo se la regola vale per tutto il resto.
- **Hella al risveglio.** Il ramo dice «Full». Per il gruppo di oggi la domanda di G2-12 è chiusa. Resta la regola per i gruppi futuri.

---

## Tabella riassuntiva

I codici in ~~barrato~~ sono chiusi: vedi sopra.

### A · Contraddizioni fra master (le più urgenti)

| Codice | Domanda | Raccomandazione | Master | Tocca il tavolo? |
|---|---|---|---|---|
| G2-01 | Dormire nella Sala dopo il rito costa −4 h o 8 h? | −4 h prima del rito, 8 h dopo: rispetta tutti e due i tag | DEF-2 §0-bis · DEF-3 §0, §8-ter, §9 | no, solo gruppi futuri |
| ~~G2-02~~ | ~~Chi dice il nome di Hella nel sonno?~~ | → K1: Tordek | DEF-3 §0 | chiusa |
| ~~G2-03~~ | ~~La serata del 25 settembre è di questo gruppo?~~ | sì, lo dice il ramo | — | chiusa |
| G2-04 | Dalla Forgia si esce senza passare dal portale? | Una porta sola | DEF-2 §8 · DEF-3 soglia | no |
| G2-05 | Il +1 della Stanza va al «ritual-master», che in DEF-3 non esiste | +1 senza tipo al TS dello Step 5 di chi tocca | DEF-2 §4-bis · DEF-3 Step 5 | no |
| G2-06 | Quanto durano le Benedizioni: 24 h, «finché nel Piano», «per una battaglia»? | 24 ore vissute per tutte (D80) | DEF-1 · DEF-2 §7 · DEF-3 §11 | sì, il duello di DEF-4 |
| G2-07 | Chi muove il PG di un giocatore assente: il DM (DEF-3) o un giocatore (DEF-5)? | Un giocatore presente tira; le scelte di canone restano al giocatore assente | DEF-3 §0 · DEF-5 Scalare | DEF-5 |
| G2-08 | Re Thorek I: il Bestiario dice che lo statblocco è nel master, il master dice che non c'è | Soglia a colpi, e il puntatore del Bestiario va corretto | DEF-4 A.5, Scena 11 · Bestiario | sì, il duello |
| G2-09 | Dove sta il corpo di Hella: lato sud, fra A6 e A8, accanto all'Altare? | Lato sud, e la mappa S-1 si allinea | DEF-2 S-1, §4 | no |
| G2-56 | Il pesatore trattiene una moneta su dieci (Q10), ma il saldo giocato (D43) non lo applica | La trattenuta vale, e si scala ora dalla cassa del 1372 | DEF-4 r. 1160, 1223, 1451 · diario | sì |

### B · Il tavolo e la partita in corso (ramo di gruppo)

| Codice | Domanda | Raccomandazione | Master |
|---|---|---|---|
| G2-10 | Quando ha pregato all'Altare il gruppo di oggi? | Lo chiede il DM ai giocatori; se nessuno lo sa, prima del portale | DEF-4 §0-bis · DEF-2 §7 |
| ~~G2-13~~ | ~~Quanti PX del beat prende Hella?~~ | → K2: tutti | DEF-3 §11 |
| G2-14 | Tutto quello che i PG portano addosso torna nel 1372, come l'ascia e lo scudo? | Sì, tutto | DEF-4 Scena 5, §7 · DEF-5 |
| G2-15 | Le due wyvern scortano Skullcrusher stasera? | Sì | DEF-4 Scena 11 |
| G2-57 | I PE del Piano del Fuoco: quale delle tre versioni? | Nessuna dalle fonti; decide il DM | ramo, registro PE · DEF-3 §11 |
| G2-58 | Il Debito della Radice portato da Thorik: quale prezzo, e il quarto ramo vale per i gruppi futuri? | Il pegno di A, portato da Thorik e riscosso al Cerchio Sacro; per i futuri resta la regola del 2026-10-18 | DEF-3 §6 · ramo E-07g |

### C1 · Regole da fissare prima che il gruppo di oggi ci arrivi (DEF-4 dalla Scena 5, DEF-5)

| Codice | Domanda | Raccomandazione | Master |
|---|---|---|---|
| G2-18 | Si confermano i blocchi «Se lo divinano»? | Sì, e si completano dove mancano righe (anche DEF-5) | DEF-1 §0 · DEF-2 §4-bis · DEF-3 · DEF-5 |
| G2-24 | Picchiata o «senza sorpresa», se valgono insieme? | Picchiata | DEF-4 Scene 8, 11 |
| G2-25 | Un PG ucciso da *slay living* resta morto? | Sì, morte vera | DEF-4 Scena 7 |
| G2-26 | Vatore colpito: che CA, e che effetto ha l'urlo? | CA 15, e l'urlo dà l'allarme | DEF-4 Scena 9 |
| G2-27 | Che cosa ottiene chi divina Vatore, il Sigillo, Zeth? | Mezze verità, una riga per segreto | DEF-4 Scene 5, 9 |
| G2-28 | Chi paga il primo prezzo del Sigillo, e quando? | Sempre acceso | DEF-4 Scena 9, App. B |
| G2-29 | Quando cambia lo stato di Grask durante la trattativa? | All'atterraggio | DEF-4 Scene 6-7 |
| G2-30 | Si toglie «Avete chiuso il cerchio» dalla Scena 13? | Si conferma il taglio | DEF-4 Scena 13 |
| G2-31 | Contro quale CA tirano gli hobgoblin quando Dana copre il re? | Scudo di carne: la CA di contatto di Dana | DEF-5 round 6, A.5-A.6 |
| G2-32 | I due orchi scossi sono dentro o fuori dall'anello? | Già dentro | DEF-5 Scena 2, mappa |
| G2-33 | Quante volte Hella usa le radici, e fino a dove? | Una volta per scena | DEF-5 Scena 2 |
| G2-34 | Da dove viene il potere del portale di Dana? | Dall'altare consacrato | DEF-5 §6 |
| G2-35 | Nel ramo «meno luminoso» si fa in tempo a murare il varco? | No, troppo tardi | DEF-5 Scena 2 |
| G2-36 | Si confermano i tempi della serata? | Sì | DEF-5 Quickstart |
| G2-37 | I tre esempi di «assorbi, poi rilancia» diventano canone? | Sì | DEF-5 §0-ter |
| G2-38 | Quando si sente il fischio dei sergenti? | Com'è: nel ramo duro coincide con l'ingresso | DEF-5 Scena 2 |
| G2-39 | Si conferma la scala dello scontro (EL ~9, righe per 3 e 5 PG)? | Sì | DEF-5 Scalare |

### C2 · Solo per i gruppi futuri (DEF-1, DEF-2, DEF-3, già giocati dal gruppo di oggi)

| Codice | Domanda | Raccomandazione | Master |
|---|---|---|---|
| G2-11 | Se alla serata della resurrezione manca la giocatrice di Hella | Si rinvia; se non si può, «Frase prima» | DEF-3 §0 |
| G2-12 | Con che risorse torna Hella? | Come *resurrezione*: pf pieni, slot e usi del giorno | DEF-3 §8, §8-bis |
| G2-16 | Le ore da svegli nella Sala costano all'orologio? | Per intero, come il rito di D81 | DEF-2 §0-bis |
| G2-17 | I PG possono lavorare alla Forgia Eterna? | Solo riti | DEF-2 Scena 1, §8 |
| G2-19 | Che cosa fa un dono che attecchisce a metà? | Il primo uso va perso | DEF-3 §5, Step 5 |
| G2-20 | Chi può tenere il Sud? | Chi non officia (Therysol, Durik) | DEF-3 §9 |
| G2-21 | Sulle prove del rito valgono Prendere 10, aiuti, incantesimi? | Niente 10, niente aiuti; gli incantesimi lanciati prima valgono | DEF-3 Step 1-5 |
| G2-22 | Il Cuore si lascia studiare? | No: si tocca e basta | DEF-3 §9 |
| G2-23 | Durante l'ora d'indagine si può ancora donare? | No | DEF-3 §9 |
| G2-40 | Come si attraversano i 20 m di zero-G fino al Tempio? | Una spinta sola | DEF-1 §7a |
| G2-41 | Quale parte del colpo di Tordek diventa sonica? | Il danno base più il Pugno Frana | DEF-1 §8 |
| G2-42 | Che regole ha il duello formale con Terros? | Fino all'arrocco (172 pf) | DEF-1 §8 Contingenze |
| G2-43 | Dove cade il pilastro della via A? | Su una striscia scelta da chi legge la pietra | DEF-1 §5 |
| G2-44 | Quante volte si può cantare la scala? | Un round a prova, al terzo fallimento cade chi sta sui blocchi | DEF-1 §7 |
| G2-45 | Se Thorik rifiuta il Peso e nessuno paga | Si riposa, e al secondo rifiuto la Corona prende | DEF-1 §9 Fase 1 |
| G2-46 | Chi capisce il campo del Tempio ha un aiuto? | Nessun aiuto da Aegis Fang | DEF-1 §7a |
| G2-47 | Contro un PG più debole l'Overdrive dà due attacchi o tre? | Tre sempre | DEF-1 §7b |
| G2-48 | Le CD e il segno dei rinforzi di Terros a 34 DV | Spinta a 26, Radice a 25 | DEF-1 §8 Scalare |
| G2-49 | La fatica della sconfitta si cura nel Piano? | No | DEF-1 §8 Contingenze |
| G2-50 | Le CD della rete della Sala, e la porta di N4 | Si confermano, e N4 passa per Sapienza Magica CD 20 | DEF-2 §4-bis |
| G2-51 | Che cosa non si taglia mai? | A7, A3, il sogno di Hella e anche A8 | DEF-2 §0 |
| G2-52 | Il ricordo di Thorik resta dipinto su A3 per tutti? | Per tutti | DEF-2 §4, A3 |
| G2-53 | I Dipinti Invisibili si aprono? | Muti in ARC-07 | DEF-2 §4-bis |
| G2-54 | Il gesto per la Cronaca ha un prezzo? | Il prezzo più alto: il giuramento rotto vela A8 | DEF-2 §8 |
| G2-55 | Il segno del «conta quattro» su A6 | I quattro battiti | DEF-2 §4, A6 |

Il totale è di 55 decisioni aperte: 8 in A, 5 in B, 17 in C1 e 25 in C2. Delle otto contraddizioni, quattro toccano il tavolo di oggi (G2-06, G2-07, G2-08, G2-56).

---

## A · Contraddizioni fra master

### G2-01 · Dormire nella Sala dopo il rito: −4 h o 8 h `[gruppi futuri]`

**Domanda.** Quanto costa all'orologio di Hammerfist un sonno nella Sala dopo il rito, prima della soglia?

**Dove.** DEF-2 §0-bis, la tabella delle tariffe (−4 h nella Sala; R4 giocato a −4 h). DEF-3 §0 (r. 42), §8-ter, la scelta «Riposare e prepararsi prima» (r. 1253) e la riga «Vogliono dormire prima della soglia» del §9 (r. 1289), con il tag `[CANONE — DM 2026-10-18]`. Origine: DEF-3 D11. Al tavolo del 2026-09-25 il gruppo ha attraversato senza dormire (diario), quindi la decisione riguarda solo i gruppi futuri.

- **Vale DEF-2** · −4 h. DEF-3 cambia due righe, ma si scrive contro un tag del DM.
- **Vale DEF-3 dopo il rito** · −4 h prima del rito, 8 h dopo. DEF-2 §0-bis aggiunge una riga: spento il Cuore, la Sala non rallenta più il tempo.
- **8 h sempre** · si riprezza anche R4, che è giocato.

**Raccomandata: Vale DEF-3 dopo il rito.** Il correttore aveva scelto DEF-2, ma così si contraddice un `[CANONE — DM 2026-10-18]`. Con questa opzione reggono tutti e due i tag, e regge anche D81: il rito dura un'ora e porta l'orologio da 3g 16h a 3g 15h, cioè dopo il rito la Sala conta il tempo per intero. La ragione nella finzione va confermata.

### G2-04 · Dalla Forgia si esce senza il portale? `[gruppi futuri]`

**Domanda.** Prima del rito o dopo, i PG possono lasciare la Forgia per un'altra via: un tempio, il Sottosuolo, i Bracieri verso Hammerfist?

**Dove.** DEF-2 §8, «Cercano un'altra via» (r. 1079); DEF-2 S-2 (l'ingresso sud della Stanza porta alla Sala, il portale drow è sigillato); DEF-3, le scelte della soglia. Origine: DEF-2 D2 e DEF-3 D7. I due correttori hanno raccomandato il contrario. Il gruppo di oggi ha attraversato il portale.

- **Una porta sola** · finché il ciclo non è compiuto, dalla Forgia si esce solo dai portali dei Piani e da quello del Tempo.
- **Sottosuolo con prezzo** · si esce dalla Stanza per la strada di ARC-06; il primo tempio è a più di due giorni, e l'orologio scende sotto la soglia del §8.
- **I Bracieri aprono** · le chiavi planari di Tordek portano a Hammerfist saltando DEF-4.

**Raccomandata: Una porta sola**, in tutti e due i master. È la più terrificante: il gruppo è chiuso dentro mentre A7 ticchetta. È l'unica che non inventa una geografia e che non riordina gli archi (coerenza, regola 8).

### G2-05 · Il +1 della Stanza e il «ritual-master» `[gruppi futuri]`

**Domanda.** Chi riceve il +1 dell'incisione della druida, e si somma al +1 sacro di A1?

**Dove.** DEF-2 §4-bis (D36 e, «+1 sacro al primo TS del ritual-master»); DEF-3 Step 5, dove il TS di Volontà lo tirano tutti e tre gli officianti e un ritual-master non c'è. Origine: DEF-2 D1.

- **Senza tipo** · +1 al TS dello Step 5 di ogni PG che ha toccato l'incisione, cumulabile con tutto.
- **Sacro com'è** · per chi ha meditato davanti ad A1 non conta niente.
- **Sacro a tutti** · il primo che tocca dà +1 sacro a tutti e tre, non cumulabile con A1.

**Raccomandata: Senza tipo.** È la più forte. ⚠ Non SRD: un dono divino senza tipo è raro, e va scritto come eccezione. Va aggiunto alla tabella dello Step 5 di DEF-3.

### G2-06 · Quanto durano le Benedizioni `[tavolo: il duello]`

**Domanda.** Le Benedizioni della Sala, compresi il Mantello della Fiamma e la Benedizione di Moradin Incarnato di Hella, durano 24 ore vissute, finché si resta nel Piano o «per una battaglia»?

**Dove.** DEF-2 §7 (r. 885): 24 ore vissute dalla preghiera, rinnovo una volta ogni 24 ore `[CANONE — DM 2026-10-12, D80]`. DEF-1 ha due righe in conflitto (PT#9, lasciato). DEF-3 §11 dice «per una battaglia» e «1/battaglia», che non sono durate 3.5. Origine: DEF-1 PT#9, DEF-2 D3, DEF-3 D5. Il ramo non registra le Benedizioni di Hella.

- **24 ore vissute per tutte** · DEF-1 si allinea a D80. All'arrivo dalla Terra sono scadute e la preghiera le rinnova. Mantello: resistenza al fuoco 20 per 24 ore, non cumulabile con la Pelle di Pietra. Incarnato: 1 al giorno, azione veloce, 1 minuto.
- **Dieci minuti per le due di Hella** · le altre restano a 24 ore.
- **Finché si resta nel Piano** · si riscrive D80.

**Raccomandata: 24 ore vissute per tutte.** È la più forte, ed è l'unica che non tocca D80. Il prezzo resta, perché a −1.000 le Benedizioni non si rinnovano (DEF-2 §7, r. 888). L'azione e il «1 al giorno» di Incarnato sono numeri del correttore `[da confermare]`. Al duello conta anche G2-10.

### G2-07 · Il PG di un giocatore assente `[DEF-5]`

**Domanda.** Chi tira e chi sceglie per il PG di un giocatore che manca?

**Dove.** DEF-3 §0, «Se manca un giocatore» (`[INFERRED` r. 166): tira il DM. DEF-5 «Scalare lo scontro» (`[INFERRED` r. 687): non si sa chi muove il quarto PG. Origine: DEF-3 D3 e DEF-5 D9, per la parte che riguarda questo. Il 2026-09-25 c'erano tutti e quattro i giocatori.

- **Un giocatore presente** · tira e muove il PG assente; le scelte di canone (il Dono, il finisher, una risposta alla Custode) restano del giocatore assente, e si chiedono prima se servono.
- **Il DM** · tira e muove; il PG difende e non cerca il finisher.
- **Come scritto in ogni master** · DM in DEF-3, giocatore in DEF-5.

**Raccomandata: Un giocatore presente**, in tutti e due i master. Il PG resta in mano a un giocatore. La regola del Dono dormiente di DEF-3 resta com'è.

### G2-08 · Re Thorek I come bersaglio del drago `[tavolo: il duello]`

**Domanda.** Come si contano i colpi di Skullcrusher sul re, che nel master non ha né CA né pf?

**Dove.** DEF-4 A.5 (r. 3815: «Guerriero 16 senza statblocco completo»); Scena 11, «Il re» `[CANONE — DM 2026-10-18]`; Scena 10, «8 pf» (r. 2827). `Bestiario/png/re-thorek-i-cr16.md` dice che lo statblocco è nel master DEFINITIVO, ed è falso. Non va confuso con Re Thorek Hammerfist del 1372 (DEF-5, CA 30, 196 pf). Origine: DEF-4 D2.

- **Statblocco breve** · CA, pf, TS e Frostcleaver per un Guerriero 16 in mithral +2.
- **Soglia a colpi** · due colpi del drago lo mettono a terra stabile, uno solo se è a 8 pf. Non si tira per colpirlo.
- **Fuori bersaglio** · nei round senza chiamata il drago va sui nani.

**Raccomandata: Soglia a colpi.** È la più dura che rispetta il canone (il re non muore), e non chiede numeri. Lo statblocco breve chiede numeri che nel repo non ci sono. Il puntatore del Bestiario va corretto in ogni caso.

### G2-09 · Dove sta il corpo di Hella nella Sala `[gruppi futuri]`

**Domanda.** Il corpo è sul lato sud dell'Altare, fra A6 e A8, o «accanto all'Altare»?

**Dove.** DEF-2 legenda S-1 (`[INFERRED` r. 1231, lato sud); la griglia S-1 lo mette fra A6 e A8; la scheda di Therysol dice «accanto all'Altare»; sulla S-1 manca Durik. Origine: DEF-2 D12.

- **Lato sud** · il corpo guarda verso A8 e regge N1; si sposta il segnalino † e si aggiunge Durik.
- **Davanti ad A8** · la manifestazione parte appena arrivano.
- **Lato nord** · il giro verso sud si vede di più.

**Raccomandata: Lato sud.** Regge l'indizio di Therysol («si gira ancora verso sud»). Nella stessa mappa va riallineata anche la distanza dall'Altare alla parete (15 m contro i 19-20 m di un diametro di 40).

### G2-56 · La moneta su dieci del pesatore `[tavolo]` (nuova)

**Domanda.** Il saldo della fucina pagato in monete del 1372 subisce la trattenuta di una moneta su dieci?

**Dove.** DEF-4 Scena 5, r. 1160 (trattiene una su dieci `[CANONE — DM 2026-10-07, Q10]`), r. 1223 e r. 1451 («ne servono circa 21.800»). Il diario, «Loot distributed»: «19.603 mo pagate in monete del 1372 … nessuna moneta di Thorek I resta in tasca ai PG (D43, deciso dal DM il 2026-10-07). ⚠️ DEF-4 dice anche che il pesatore ne trattiene una su dieci (≈21.800): D43 non lo applica». Due decisioni del DM dello stesso giorno, e il diario segnala il buco.

- **Vale il diario** · si paga 19.603 e basta; DEF-4 r. 1451 aggiunge che al tavolo del 2026-09-25 la trattenuta non si è contata.
- **Trattenuta adesso** · il pesatore ha pesato quella sera, e circa 2.180 mo del 1372 escono adesso dalla cassa del gruppo, sul ramo. La finzione non cambia.
- **Trattenuta in un debito** · i 2.180 mo restano un debito con la fucina, da saldare prima dell'alba, oppure il pesatore lo racconta in giro (la riga del Raggirare, r. 1162).

**Raccomandata: Trattenuta adesso.** Rende vere tutte e due le decisioni del DM, Q10 e D43, ed è la più cara. Non contraddice il giocato, perché il diario stesso segna il conto come aperto. Si registra con `dm.py` sul ramo di gruppo.

---

## B · Il tavolo e la partita in corso

Queste decisioni scrivono un fatto del gruppo di oggi. Si registrano sul ramo di gruppo con `dm.py` (ADR-0007, ADR-0090), mai su `main`.

### G2-10 · Quando ha pregato all'Altare il gruppo di oggi

**Domanda.** In che momento il gruppo ha pregato l'ultima volta, e quindi le Benedizioni sono attive all'alba di −1.000?

**Dove.** DEF-4 §0-bis e Scena 5; DEF-2 §7. Dipende da G2-06. Origine: DEF-4 D8. Il diario della sessione 4 non lo dice, e nemmeno `state.md` e `state.yaml` del ramo.

- **Prima del portale** · sono attive fino al duello, se l'alba cade entro le 24 ore.
- **Prima, nella Sala** · scadono prima dell'alba.
- **Mai** · il gruppo non le ha.

**Raccomandata: lo chiede il DM ai giocatori prima della Scena 5; se nessuno lo ricorda, Prima del portale.** È un fatto già successo e si conferma, non si sceglie. «Prima del portale» è il caso che la Scena 5 dà come normale.

### G2-14 · Gli oggetti comprati a −1.000 tornano nel 1372

**Domanda.** Tutto quello che i PG hanno comprato e portano addosso (pozioni, pergamene, bacchette, rune) torna nel presente con il Rubino?

**Dove.** DEF-4 Scena 5 e §7. Per l'ascia d'adamantio +2 e lo scudo con gli spuntoni gelidi DEF-4 dice già di sì (r. 1454, r. 1516, `[CANONE — DM 2026-10-06]`), e così per il Torque (r. 3439). Il diario elenca il resto (47.967 mo di acquisti). Origine: `APERTI.md`, DEF-5 PT#13.

- **Tutto** · vale la ragione che il master dà per l'ascia e lo scudo: i PG li portano addosso.
- **Solo i pezzi del re e del fabbro** · i consumabili restano a −1.000.
- **Tutto, ma i consumabili spenti** · gli oggetti tornano, e la magia dei consumabili è inerte.

**Raccomandata: Tutto.** La regola c'è già per tre pezzi, e la sua ragione vale per tutto. Basta una riga in DEF-5, all'arrivo. Il conto WBL si rifà in ARC-08 B4. Chi ha in mano ogni pezzo il diario non lo dice («non registrato al tavolo»): va raccolto ai giocatori.

### G2-15 · Le wyvern stasera

**Domanda.** Con il gruppo di oggi (13°, fiducia piena, tutti gli artefatti, 47.967 mo spese) le due wyvern scortano Skullcrusher?

**Dove.** DEF-4, sidebar del duello (Scena 11). Il diario conferma la fiducia piena e gli acquisti. Origine: DEF-4 D9.

- **Sì** · le wyvern arrivano dal round 2 e vanno su chi tiene la corda e su chi vola.
- **No** · «straripante» vuol dire 14°, e c'è solo il drago di A.1.
- **Secondo le mura** · arrivano solo se la Scena 10 dà 3 successi o più.

**Raccomandata: Sì.** È la più forte, e da solo il drago (GS 14 contro APL 13) rischia di cadere prima che la Catena e le corde contino. L'EL resta sotto APL+4 (`npc-villain-boosting`).

### G2-57 · I PE del Piano del Fuoco (nuova)

**Domanda.** Quale delle tre versioni dei PE del Fuoco va nel registro del gruppo?

**Dove.** Il diario, «XP awarded»: tre versioni che non coincidono (`PortaleForgia-P3-PianoFuoco-PARTE2` 3.000 a testa, `RicalibrazioneScontriPianoDelFuoco` 7.200, `La_Piramide_Ricalibrata` 18.000 ÷ 3), più ~11.600 a testa per la Terra (DEF-1 §A), «da registrare quando il DM sceglie». Da qui dipende quando arriva il 14° (DEF-3 §11: «il 14° matura a Hammerfist»).

- **3.000** · il 14° arriva più tardi.
- **6.000 o 7.200** · il 14° arriva prima, forse già in DEF-4.

**Raccomandata: nessuna dalle fonti.** Vale il file che il DM ha davvero usato al tavolo del Fuoco. La regola del più potente qui non si applica, perché si tratta di registrare una cosa giocata. ⚠️ Il diario avverte di non committare `campaign/pg/xp-ledger.md` generato da `update_xp.py`, che riparte da zero.

### G2-58 · Il Debito della Radice portato da Thorik (nuova)

**Domanda.** Che prezzo paga Thorik, e quando lo riscuote la Custode? E il quarto ramo vale anche per i gruppi futuri?

**Dove.** DEF-3 §6 (rami A, B, C; «Chi risponde: l'ultima parola è di Hella» `[CANONE — DM 2026-10-18]`); K3; il ramo, `state.md` §7.E, E-07g (`[INFERRED — needs DM confirmation]` sul prezzo e sul momento); il diario, «DM notes»: da decidere prima di ARC-09, Cerchio Sacro. Non è urgente.

- **Il pegno di A, su Thorik** · Thorik deve un servizio futuro al Sogno della Terra, che si riscuote come quest al Cerchio Sacro di ARC-09. Se lo ignora, il debito degrada in B, come il master scrive per A. Hella non ha il legame di A (Earth Dream 2 al giorno), perché il pegno non l'ha preso lei.
- **Il vuoto di B, su Thorik** · qualcosa risale dal Sogno, e cerca lui.
- **Un prezzo nuovo** · il DM lo scrive per ARC-09.

**Raccomandata: Il pegno di A, su Thorik.** Usa un prezzo che il master ha già scritto, e porta dentro anche la minaccia di B. Non inventa poteri. Per i gruppi futuri resta la regola del 2026-10-18, e il quarto ramo si annota in K3 come canone del gruppo di oggi, non come opzione per tutti.

---

## C1 · Regole da fissare prima che il gruppo di oggi ci arrivi

Il tavolo riprende da DEF-4 Scena 5 (ramo). Queste regole valgono anche per i gruppi futuri, e si scrivono nel master su `main`.

### G2-18 · I blocchi «Se lo divinano»

**Domanda.** Le tabelle con le risposte delle divinazioni diventano canone, e si completano dove mancano righe?

**Dove.** DEF-1 §0 (`[INFERRED` r. 172); DEF-2 §4-bis (`[INFERRED` r. 758); DEF-3 (`[INFERRED` r. 176); DEF-5, dove il blocco manca (DEV#15, lasciato). Origine: DEF-1 D7, DEF-2 D10, DEF-3 D8, DEF-5 DEV#15. Per il gruppo di oggi conta solo il blocco di DEF-5; gli altri tre sono di beat già giocati. Il caso di DEF-4 è G2-27.

- **Confermare e completare** · i tre blocchi diventano canone. In DEF-3 si aggiungono tre righe: *individuazione del magico* sull'Altare sente una presenza divina e non dice quale; *divinazione* non dice la forma dei Doni prima del sì; *parlare con i morti* sul corpo risponde con quello che Hella sapeva alla morte (SRD: legge il corpo, non l'anima). DEF-5 riceve un blocco nuovo.
- **Confermare così** · DEF-5 resta senza.
- **Più avari** · la Sala resta muta (proposta di DEF-1), e Moradin risponde «non chiaro» sul rito (proposta di DEF-2).

**Raccomandata: Confermare e completare.** Premia chi lancia senza rompere l'asimmetria su Hella (§9 del developer). Thorik ha *comunione* 1/mese dalla Corona. Le righe di DEF-5 vanno scritte.

### G2-24 · Picchiata o «senza sorpresa»

**Domanda.** Se Zog'tar muore in modo spettacolare e il drago ha già visto i PG, quale regola vince?

**Dove.** DEF-4 Scene 8 e 11. Origine: DEF-4 D1.

- **Picchiata** · il drago ha il round di sorpresa; agisce chi supera Ascoltare CD 20, o tutti se le campane hanno suonato (D25).
- **Senza sorpresa** · iniziativa normale.
- **Tutte e due** · niente sorpresa, ma il soffio parte prima dell'iniziativa.

**Raccomandata: Picchiata.** È la più forte, e le campane restano la contromossa `[CANONE — DM 2026-09-30, D25]`.

### G2-25 · *Slay living* di Balvar sui PG

**Domanda.** Un PG che fallisce il TS contro *slay living* resta morto?

**Dove.** DEF-4 Scena 7 (round 2, Tempra CD 20); Q29 (i PG caduti nella tenda sono catturati vivi). Origine: DEF-4 D3.

- **Morte vera** · vale l'SRD. Si torna con *rianimare morti* alla cappella (l'unico diamante, 5.450 mo) o con *reincarnazione*. Q29 vale per chi cade a 0 pf.
- **Cattura** · il PG va a −1 e stabile. ⚠ Non SRD.
- **Niente *slay living* sui PG**.

**Raccomandata: Morte vera.** È la più terrificante e non tocca Q29. Hella è viva e ha la Collana (ramo), quindi *reincarnazione* dipende da quello che ha preparato.

### G2-26 · Vatore colpito

**Domanda.** Contro quale CA si tira il primo colpo su Vatore, e che effetto ha il suo urlo?

**Dove.** DEF-4 Scena 9; Q31 (Vatore non ha statistiche). Origine: DEF-4 D4.

- **Allarme** · CA 15; la ronda arriva in 1d4+2 round, le mura perdono un successo, il blocco dopo è a CD +2.
- **Strillo** · CA 15; vale come l'urlo delle vedette.
- **Senza tiro** · nessuna CA, e l'urlo si perde.

**Raccomandata: Allarme.** La CA 15 è del correttore, non viene da nessuno statblocco: il DM deve confermarla come eccezione a Q31.

### G2-27 · Divinare Vatore, il Sigillo e i componenti di Zeth

**Domanda.** Che cosa ottiene chi divina i due segreti lunghi (Vatore che diventerà Sal, il Collezionista dietro Zeth)?

**Dove.** DEF-4 Scene 5 e 9. Il gruppo ha già incontrato Zeth nelle gallerie (diario). Origine: DEF-4 D5.

- **Mezze verità** · *individuazione dei pensieri* su Vatore legge «il Cronolito», «la gilda», «non devono vedermi», mai «Sal»; *leggende e tradizioni* sul Sigillo dà Shar e il prezzo delle anime; *individuazione del magico* sui componenti di Zeth mostra necromanzia sotto la consacrazione; su Zeth Vatore fa un nome di gilda.
- **Schermo** · il Sigillo rende Vatore vuoto alla divinazione.
- **Com'è** · improvvisa il DM.

**Raccomandata: Mezze verità.** Il segreto di Sal regge, perché Vatore non lo sa. Prima di scriverlo va controllato contro `campaign-coherence`.

### G2-28 · Il prezzo del Sigillo rubato stanotte

**Domanda.** Se un PG ruba il Sigillo prima dell'alba, chi paga il primo prezzo, e quando?

**Dove.** DEF-4 Scena 9, Appendice B (potere d'artefatto, coerenza §2.1). Origine: DEF-4 D6.

- **Sempre acceso** · un'ora dopo il DM sceglie la creatura toccata per ultima, compagni e Durik compresi; non si spegne, nemmeno nel buco portatile.
- **Solo addosso** · conta solo chi lo porta.
- **Tace fino al 1372**.

**Raccomandata: Sempre acceso.** È quella che l'Appendice B racconta. Il buco portatile di Artemis è canone (diario, DM 2026-10-11), quindi la riga serve davvero.

### G2-29 · Grask e la tacca di Balvar

**Domanda.** Quando cambia lo stato di Grask, se la trattativa con Balvar porta la 5ª tacca?

**Dove.** DEF-4 Scene 6-7; D50; D74. Il gruppo riprende con 3 tacche (ramo). Origine: DEF-4 D7.

- **All'atterraggio** · lo stato si fissa all'arrivo.
- **A fine trattativa** · dorme dal primo colpo.
- **A inizio trattativa** · dorme già mentre parlano.

**Raccomandata: All'atterraggio.** È la più forte, e lascia intera D50.

### G2-30 · «Avete chiuso il cerchio» tolta dalla Scena 13

**Domanda.** Si conferma il taglio della battuta?

**Dove.** DEF-4 Scena 13. Origine: `APERTI.md`.

- **Confermare il taglio** · la scena chiude senza.
- **Rimetterla**.

**Raccomandata: Confermare il taglio.** È una scelta di stile.

### G2-31 · Le frecce al re, e Dana che le prende

**Domanda.** Contro quale CA tirano gli hobgoblin quando Dana copre Re Thorek Hammerfist?

**Dove.** DEF-5 round 6, A.5 e A.6 (re esausto CA 27, 31 contro gli archi perché steso); il canone del 2026-10-18 («cinque o sei frecce»). Origine: DEF-5 D1.

- **SRD puro** · Dana non è quasi mai in pericolo.
- **Dana bersaglio** · contro la sua CA 29: cambia poco.
- **Scudo di carne** · contro la sua CA di contatto, 14: circa 15 pf a round, e cade in due round.

**Raccomandata: Scudo di carne.** È l'unica che rende veri i numeri a canone. ⚠ Non SRD. Il talento PF1e *In Harm's Way* (Advanced Player's Guide) proteggerebbe di più Dana, e quindi non si usa.

### G2-32 · I due orchi scossi

**Domanda.** I due orchi sono dentro o fuori dall'anello?

**Dove.** DEF-5 Scena 2, la tattica D77, la mappa. Origine: DEF-5 D2.

- **Già dentro** · caricano al round 1; si spostano due segnalini.
- **Restano fuori**.
- **L'anello si apre** · arrivano al round 2.

**Raccomandata: Già dentro.** Tiene alla lettera D77.

### G2-33 · Le radici di Hella

**Domanda.** Quante volte Hella usa le radici, con che azione, fino a dove?

**Dove.** DEF-5 Scena 2; D77. Origine: DEF-5 D3.

- **Una volta** · per scena, azione standard, gittata di *intralciare* (lunga: 264 m al 12° livello di incantatore).
- **A ogni round**.
- **Solo all'arrivo**.

**Raccomandata: Una volta.** «A ogni round» toglierebbe agli hobgoblin la minaccia che D77 vuole.

### G2-34 · Il portale di Dana

**Domanda.** Da dove viene il potere del portale?

**Dove.** DEF-5 §6; la Consacrazione di Moradin (§2). Origine: DEF-5 D4.

- **Il luogo** · lo apre l'altare consacrato, per un round di preghiera; resta aperto 1 minuto.
- **Dono di classe** · Cantante Divina, 1 al giorno.
- **Costa il muro**.

**Raccomandata: Il luogo.** Il minuto di apertura è un numero del correttore `[da confermare]`.

### G2-35 · Murare il varco nel ramo «meno luminoso»

**Domanda.** Si fa in tempo?

**Dove.** DEF-5 Scena 2. Origine: DEF-5 D5.

- **Troppo tardi** · il muro chiude fuori l'ondata dopo.
- **Nel round di sorpresa**.

**Raccomandata: Troppo tardi.** Va d'accordo con il canone del 2026-10-18 e con D77.

### G2-36 · I tempi della serata

**Domanda.** I tempi del Quickstart diventano canone?

**Dove.** DEF-5 Quickstart (`[INFERRED` r. 133). Origine: DEF-5 D6.

- **Conferma**.
- **Più lungo** · 20 minuti per la Scena 2.

**Raccomandata: Conferma.**

### G2-37 · I tre esempi di «assorbi, poi rilancia»

**Domanda.** I tre esempi del §0-ter diventano canone?

**Dove.** DEF-5 §0-ter (`[INFERRED` r. 249). Origine: DEF-5 D7.

- **Canone**.
- **Solo esempi**.

**Raccomandata: Canone.** Il secondo esempio (il torque nella mano del re del 1372) presuppone che il Torque torni: è coerente con DEF-4 r. 3439 e con G2-14.

### G2-38 · Il fischio dei sergenti

**Domanda.** Quando si sente il fischio, nei due rami?

**Dove.** DEF-5 Scena 2 (`[INFERRED` r. 583). Origine: DEF-5 D8.

- **Un round prima** · in tutti e due i rami.
- **Com'è** · nel ramo «meno luminoso» coincide con l'ingresso.

**Raccomandata: Com'è.** Il correttore aveva scelto «Un round prima». Nel ramo luminoso il fischio fa già da preavviso, e nel ramo duro la versione più terrificante è quella in cui il fischio arriva insieme al nemico.

### G2-39 · Scalare lo scontro della caverna

**Domanda.** Si conferma la scala (EL intorno a 9, righe per tre e per cinque PG)?

**Dove.** DEF-5 «Scalare lo scontro» (`[INFERRED` r. 687); il quarto PG è in G2-07. Origine: DEF-5 D9.

- **Conferma**.
- **Riscrivere la riga per cinque PG**.

**Raccomandata: Conferma.** Il tag cade quando è decisa anche G2-07.

---

## C2 · Solo per i gruppi futuri

Il gruppo di oggi ha giocato DEF-1 (2026-07-31), DEF-2 e DEF-3 (2026-09-25): per lui vale quello che si è giocato.

### G2-11 · Se alla serata della resurrezione manca la giocatrice di Hella

**Domanda.** Che cosa si fa se la giocatrice di Hella non c'è?

**Dove.** DEF-3 §0, §6, §8. Origine: DEF-3 D3. Il 2026-09-25 la giocatrice c'era.

- **Si rinvia**.
- **Frase prima** · il DM le chiede prima A, B o C e la frase.
- **Come è scritto** · il silenzio vale B.

**Raccomandata: Si rinvia, e «Frase prima» se il tavolo non può aspettare.**

### G2-12 · Con che risorse torna Hella

**Domanda.** Al risveglio Hella ha pf, incantesimi, usi della Collana e forme selvatiche?

**Dove.** DEF-3 §8 e §8-bis. Origine: DEF-3 D4. Per il gruppo di oggi il ramo dice «Full».

- **Come resurrezione** · pf pieni e gli incantesimi preparati alla morte (SRD, *Resurrezione*); le prove del §8-bis spendono slot veri.
- **Prove gratis**.
- **Svuotata** · metà dei pf e nessuno slot fino al sonno.

**Raccomandata: Come resurrezione.** È la versione SRD più forte, ed è quella che il gruppo di oggi ha giocato (pf pieni).

### G2-16 · Le ore da svegli nella Sala

**Domanda.** Prima del rito, quanto costa all'orologio un'ora da svegli nella Sala?

**Dove.** DEF-2 §0-bis. Origine: DEF-2 D4.

- **A metà**.
- **Per intero**.
- **Gratis** · come scrive oggi il master.

**Raccomandata: Per intero.** «A metà» contraddirebbe D81, che fa costare un'ora piena al rito nella Sala.

### G2-17 · La Forgia Eterna come bottega

**Domanda.** I PG possono lavorare il metallo alla Forgia Eterna?

**Dove.** DEF-2 Scena 1, §8. Origine: DEF-2 D5.

- **Solo riti**.
- **Artigianato SRD**.
- **Forgia divina**.

**Raccomandata: Solo riti.** La «Forgia divina» inventerebbe un potere (coerenza §2.1).

### G2-19 · Il dono che attecchisce a metà

**Domanda.** Con 2 successi su 3, che cosa fa un dono che attecchisce a metà?

**Dove.** DEF-3 §5, Step 5. Origine: DEF-3 D1.

- **Primo uso perso** · a −1.000 il primo uso non funziona e si consuma.
- **Metà valore** · per la prima scena.
- **Solo un'eco**.

**Raccomandata: Primo uso perso**, più una riga: se chi ha fallito aveva rifiutato, attecchisce a metà il dono di un altro. ⚠ Non SRD.

### G2-20 · Chi può tenere il Sud

**Domanda.** Chi può tenere il Sud, e un punto lasciato vuoto conta?

**Dove.** DEF-3 §9; `[INFERRED` r. 1293 (Therysol sul corpo) e r. 166 (il quinto PG). Origine: DEF-3 D2.

- **Chi non officia** · Therysol e Durik.
- **Chiunque**.
- **Solo Therysol**.

**Raccomandata: Chi non officia.** Premia la mossa naturale della giocatrice (Durik al Sud).

### G2-21 · Prendere 10, aiuti e incantesimi sulle prove del rito

**Domanda.** Sugli Step 1-3 e sulla Volontà valgono Prendere 10, gli aiuti, gli incantesimi?

**Dove.** DEF-3 Step 1-5. Origine: DEF-3 D6.

- **Niente aiuti** · il rito è una distrazione; gli incantesimi lanciati prima valgono.
- **Prendere 10**.
- **Aiuti larghi**.

**Raccomandata: Niente aiuti.** ⚠ Non SRD solo in parte: l'SRD lascia al DM decidere che cosa distrae.

### G2-22 · Il Cuore toccato prima di posarlo

**Domanda.** Il Cuore si lascia toccare e non studiare?

**Dove.** DEF-3 §9 (`[INFERRED` r. 1294). Origine: DEF-3 D9.

- **Confermo**.
- **Con un prezzo**.
- **Si studia**.

**Raccomandata: Confermo.**

### G2-23 · Il seme dormiente durante l'ora d'indagine

**Domanda.** Chi aveva rifiutato può donare durante l'ora?

**Dove.** DEF-3 §9 (`[INFERRED` r. 1352). Origine: DEF-3 D10.

- **Confermo** · il seme resta chiuso fino ad ARC-09.
- **Si dona tardi**.

**Raccomandata: Confermo.**

### G2-40 · Il salto verso il Tempio

**Domanda.** Come si attraversano i 20 m di zero-G?

**Dove.** DEF-1 §7a, T-4; la regola dello zero-G del §0-bis. Origine: DEF-1 D1.

- **Spinta unica** · un tiro solo fino ai 20 m; se fallisce entra l'Ancora.
- **SRD letterale** · tre salti.
- **Catena di detriti** · due salti.

**Raccomandata: Spinta unica.** Il tratto «gravità assente» dell'SRD (Tratti planari) non dà una regola di movimento. ⚠ Non SRD. Il «Take 10 = 26» giocato al tavolo va confermato: comprende già il −5 della gravità e il +2 della Benedizione?

### G2-41 · Quanto del pugno di Tordek diventa sonico

**Domanda.** Quale parte del colpo diventa sonica?

**Dove.** DEF-1 §8. Origine: DEF-1 D2.

- **Tutto**.
- **Solo la base** · 1d10+2.
- **Base più Pugno Frana**.

**Raccomandata: Base più Pugno Frana.** Con 1d10+2 si fa al massimo 12, e la soglia di 15 diventerebbe impossibile.

### G2-42 · Il duello formale con Terros

**Domanda.** Con che regole si combatte?

**Dove.** DEF-1 §8 Contingenze. Origine: DEF-1 D3.

- **Toglierlo**.
- **Fino alla morte**.
- **Fino all'arrocco** · a 172 pf Terros si inginocchia.

**Raccomandata: Fino all'arrocco.** È la versione più dura che resta vincibile.

### G2-43 · Il pilastro della via A

**Domanda.** In che area cade il pilastro?

**Dove.** DEF-1 §5. Origine: DEF-1 D4.

- **Linea scelta** · 3 × 30 m.
- **Cerchio alla base** · 6 m.
- **Solo gli Xorn**.

**Raccomandata: Linea scelta.** Le misure sono del correttore: vanno confermate.

### G2-44 · Quante volte si canta la scala

**Domanda.** La scala cantata ha un limite di tentativi?

**Dove.** DEF-1 §7. Origine: DEF-1 D5.

- **Illimitati**.
- **Tre fallimenti**.
- **Un round a prova** · al terzo fallimento cade chi sta sui blocchi.

**Raccomandata: Un round a prova**, con la caduta della regola del §3. Il correttore aveva scelto «Tre fallimenti».

### G2-45 · Thorik rifiuta il Peso e nessuno paga

**Domanda.** Come va avanti il rito?

**Dove.** DEF-1 §9 Fase 1. Origine: DEF-1 D6.

- **Si riposa** · al secondo rifiuto la Corona prende.
- **La Corona prende**.
- **Pagamento misto**.

**Raccomandata: Si riposa.**

### G2-46 · Chi capisce il campo gravitazionale

**Domanda.** Chi fallisce la prova ha l'aiuto di Aegis Fang?

**Dove.** DEF-1 §7a (`[INFERRED` r. 1288). Origine: DEF-1 D8.

- **Confermare**.
- **Senza aiuto**.

**Raccomandata: Senza aiuto.**

### G2-47 · L'Overdrive contro un PG più debole

**Domanda.** Due attacchi o tre?

**Dove.** DEF-1 §7b (`[INFERRED` r. 1480). Origine: DEF-1 D9.

- **Due attacchi**.
- **Tre sempre**.

**Raccomandata: Tre sempre.**

### G2-48 · Terros a 34 DV

**Domanda.** Quali CD salgono, e qual è il segno dei rinforzi?

**Dove.** DEF-1 §8, r. 1980 (due `[INFERRED`). Origine: DEF-1 D10.

- **Com'è scritto**.
- **Spinta 26**.
- **Tutto +1**.

**Raccomandata: Spinta 26, e il segno si conferma com'è.** Mancano il Boost log e il benchmark (DEV#20).

### G2-49 · La fatica della sconfitta

**Domanda.** Si cura nel Piano?

**Dove.** DEF-1 §8 Contingenze (`[INFERRED` r. 2045). Origine: DEF-1 D11.

- **Confermare** · no.
- **Col Vigore**.

**Raccomandata: Confermare.**

### G2-50 · Le CD della rete della Sala, e la porta di N4

**Domanda.** Si confermano le CD nuove, e da che prova si apre N4?

**Dove.** DEF-2 §4-bis (`[INFERRED` r. 723). Origine: DEF-2 D6.

- **Confermate**.
- **N4 per Sapienza Magica** CD 20.
- **N4 senza gradi**.

**Raccomandata: N4 per Sapienza Magica, e le altre due CD si confermano.**

### G2-51 · Che cosa non si taglia mai

**Domanda.** Se manca tempo, che cosa resta?

**Dove.** DEF-2 §0 (`[INFERRED` r. 88). Origine: DEF-2 D7.

- **Confermato**.
- **Anche A8**.
- **Solo A7**.

**Raccomandata: Anche A8.**

### G2-52 · Il ricordo di Thorik dipinto su A3

**Domanda.** Lo vedono tutti?

**Dove.** DEF-2 §4 (`[INFERRED` r. 582). Origine: DEF-2 D8.

- **Per tutti**.
- **Solo per Thorik**.
- **Fino al rito**.

**Raccomandata: Per tutti.**

### G2-53 · I Dipinti Invisibili

**Domanda.** Si aprono, e quando?

**Dove.** DEF-2 §4-bis (`[INFERRED` r. 754). Origine: DEF-2 D9.

- **Muti in ARC-07**.
- **Si aprono al rito**.
- **Mai**.

**Raccomandata: Muti in ARC-07.**

### G2-54 · Il gesto per la Cronaca

**Domanda.** Che prezzo ha un giuramento rotto?

**Dove.** DEF-2 §8 (`[INFERRED` r. 1081). Origine: DEF-2 D11.

- **Confermato** · spegne A1.
- **Senza prezzo**.
- **Prezzo più alto** · vela anche A8.

**Raccomandata: Prezzo più alto.**

### G2-55 · Il segno del «conta quattro» su A6

**Domanda.** Come capiscono i PG che il varco aspetta quattro Custodi?

**Dove.** DEF-2 §4 (`[INFERRED` r. 652). Origine: DEF-2 D13.

- **Quattro battiti**.
- **La quarta figura**.
- **Nessun segno**.

**Raccomandata: Quattro battiti.**

---

## Gli `[INFERRED` nei master e la decisione che li chiude

24 tag su 23 righe, contati su `main`. DEF-4 non ne ha nessuno.

| Master | Riga | Che cosa | Si chiude con |
|---|---:|---|---|
| DEF-1 | 172 | «Se lo divinano» | G2-18 |
| DEF-1 | 1288 | Aegis Fang suggerisce il campo del Tempio | G2-46 |
| DEF-1 | 1480 | l'Overdrive a due attacchi | G2-47 |
| DEF-1 | 1980 (1) | il +1 alle CD solo per Onda e Stalattiti | G2-48 |
| DEF-1 | 1980 (2) | il segno dei due Elementali Grandi | G2-48 |
| DEF-1 | 2045 | la fatica che il *Vigore* non toglie | G2-49 |
| DEF-2 | 24 | la nota d'apparato «le aggiunte nuove sono marcate» | cade quando sono chiuse G2-09, G2-18, G2-50…G2-55 |
| DEF-2 | 88 | l'ordine dei tagli | G2-51 |
| DEF-2 | 582 | il ricordo di Thorik su A3 | G2-52 |
| DEF-2 | 652 | i quattro battiti | G2-55 |
| DEF-2 | 723 | le CD nuove del §4-bis | G2-50 |
| DEF-2 | 754 | i Dipinti Invisibili | G2-53 |
| DEF-2 | 758 | «Se lo divinano» | G2-18 |
| DEF-2 | 1081 | il gesto per la Cronaca | G2-54 |
| DEF-2 | 1231 | il corpo di Hella sul lato sud | G2-09 |
| DEF-3 | 166 | la scala dei giocatori | G2-07 (e G2-20 per il quinto PG) |
| DEF-3 | 176 | «Se lo divinano» | G2-18 |
| DEF-3 | 1293 | Therysol risponde sul corpo | G2-20 |
| DEF-3 | 1294 | il Cuore toccato | G2-22 |
| DEF-3 | 1352 | il seme dormiente | G2-23 |
| DEF-5 | 133 | i tempi della serata | G2-36 |
| DEF-5 | 249 | i tre esempi del §0-ter | G2-37 |
| DEF-5 | 583 | il fischio dei sergenti | G2-38 |
| DEF-5 | 687 | scalare lo scontro | G2-39 (e G2-07 per il quarto PG) |

I conti tornano con `APERTI.md`: i 6 tag di DEF-1, i 5 di DEF-3 e i 4 di DEF-5 sono quelli che il rifacimento aveva elencato. Il FIX di DEF-1 ne conta «cinque» perché conta le righe: il +1 alle CD e il segno dei rinforzi stanno tutti e due sulla riga 1980. Le correzioni K1-K4 non toccano nessun tag e non ne aggiungono.

## Fatti da raccogliere al tavolo (non sono decisioni)

Il diario li lascia aperti, e servono a DEF-4 e DEF-5:
- a chi è andato ogni pezzo comprato («non registrato al tavolo»);
- quali delle richieste rimaste aperte il gruppo ha preso davvero (*silenzio*, la pietra di Brynja, *identificare*, *rimuovi paralisi*, *rimuovi maledizione*): nel diario c'è ancora «______»;
- quando il gruppo ha pregato all'Altare (G2-10);
- i quattro tiri sul *Registro delle Perdite*, da fare alla Scena 10.

## Che cosa non è una decisione

Questi punti di `APERTI.md` e dei FIX sono lavori da fare, non scelte del DM.

- **DEF-1**: riportare nell'Atlante (`Mappe/ARC07-MAPPE-DEFINITIVO.md`) T-1 «Skill+ Varis», la runa di Varis della T-3 (J05) e le Rune di Attracco della T-4, poi togliere la frase di divergenza nel master; togliere il residuo C3 «SCENA 7 · Dove: l'anticamera» da `plans/copertura-scene.json`; rigenerare l'APPARATO di DEF-1 e il booklet. Già chiusi dai correttori, da ratificare: i pf di Terros (345), le due regole di caduta, il mithral della via C, Terros che non si spinge nello zero-G. Lasciati: i TS di Terros tutti su Riflessi (DEV#18), il Boost log (DEV#20), le fenditure senza tattica (DEV#6).
- **DEF-2**: nell'Atlante S-2 la reliquia passa da «Osservare CD 22» a Cercare; controllare l'abbinamento cieco di A6 e del sogno di Hella; la griglia S-1 (G2-09).
- **DEF-3**: la griglia R-1 (Tordek e Artemis sulla riga di Thorik); le correzioni K1-K4.
- **DEF-4**: la riga della Scena 7 scritta per non far scattare il rilevatore (D10) va riformulata come riga di scala, togliendo il residuo dal JSON nello stesso commit; `Mappe/ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.md/.json` dice ancora «Fondo buio: dà occultamento»; GP1-GP4 della M7-A non li usa nessuno. Già chiusi: le campane della Scena 11, e Durin (A.3 ora dice ascia «a una mano», quindi lo scudo e la CA 22 tornano).
- **DEF-5**: la legenda CM-1 (la sfera dorata vale anche per la regia breve, da correggere nel JSON); rigenerare l'APPARATO di DEF-5.
- **Bestiario**: il puntatore di `re-thorek-i-cr16.md` (G2-08).
- **Ramo di gruppo**: la frase sul Dono di Thorik in `state.yaml` («il +2 … è passato a Hella, lui resta a −1 CA»), da allineare a DEF-3 §5 («metà del +2»).
