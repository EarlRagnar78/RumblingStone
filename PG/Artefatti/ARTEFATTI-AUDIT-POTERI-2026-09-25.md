# Artefatti dei PG — audit dei poteri, versione per versione (2026-09-25)

> **Cosa c'è qui.** Per ognuno dei cinque artefatti: quali file esistono, quale
> è la versione definitiva, e una tabella potere per potere con cosa dice ogni
> fonte. Le discordanze hanno la fonte che vince e il perché; quelle che le
> fonti non risolvono sono domande al DM (§7), con una proposta, e **non sono
> scritte come canone** finché il DM non risponde.
>
> **Stato descritto**: il tavolo **prima** della serata del 2026-09-25
> (resurrezione di Hella, viaggio a −1.000 fino al primo ariete). I Doni e il
> Rituale 4 compaiono come caselle da segnare. L'esito della serata lo scrive
> il DM sul ramo del gruppo con `dm.py session end` (ADR-0007).
>
> **Richiesta del DM** (2026-09-25): *«la scheda di Thorik non è aggiornata
> correttamente… controlla bene i poteri di tutti gli artefatti e lo storico
> per eventuali modifiche»*, poi: *«ci sono dei poteri passivi… vedi le schede»*
> e *«fai lo stesso per tutti gli artefatti»*. Fiducia dichiarata dal DM sulle
> fonti: Bracieri alta, Anello bassa, Corona bassissima.

## §0 · Le fonti lette, e con che peso

La gerarchia usata per decidere chi vince, dalla più forte:

1. **Una decisione del DM datata** (`state-changelog.md`, un blocco
   `[CANONE — DM …]` in un master, `STATO-E-ORDINE` §12, la matrice).
2. **La regola del 2026-09-20**: *decide la scheda che il giocatore ha letto*
   (matrice §1, riga del Rituale 4).
3. **Il modulo giocato** (`PortaleForgia-P1`, `P2`, `P3`, `ARC07-DEF-1`), quando
   descrive un effetto che al tavolo è stato dato.
4. Il master dell'artefatto.
5. Le schede e gli export precedenti.

Lette per intero o nelle sezioni degli artefatti: i 14 file di testo, 4 HTML e
2 PDF della cartella della Corona; `LaCorona_di_Adamantio-DM.md` (capitoli
1-3 e scheda finale); `PortaleForgia-P1-REVISED-Corretta.md` §5-7;
`PortaleForgia-P2-REVISED-Corretta-PARTE2.md` §9, §13-15;
`PortaleForgia-P3-PianoFuoco-PARTE2.md` §10; `ARC07-DEF-1` §7b e §9;
`ARC07-DEF-2` §4 (A7); `ARC07-DEF-3` §2-bis, §5, §8-ter; `ARC07-DEF-4`
Scene 1, 12, 13; la regia della serata; `campaign/state.md` §1, §6, §7.E;
`state-changelog.md` 2026-07-02, 07-04, 07-31, 08-01, 09-12; i commit
`e0aa826`, `23d4530`, `c5411ca`, `f93facc`, `53f0aa0`, `f7e75d8`, `b6eef4a`;
`_ARCHIVIO/doni-v1-2026-09-12/`; per l'Anello le due generazioni in
`PG/Artefatti/` e la cartella `Old/`; per Aegis Fang il `.docx` originale.

**I PDF, letti anche loro** (testo estratto con `pypdf`, 17 file): il PDF del
giocatore della Corona (`LaCorona_di_Adamantio.pdf`, stampato il 22/10/2025) e
quello DM; `Aegis Fang.pdf`; `Ring of Chaotic Illumination (Reforged).pdf`, il
PDF di `Old/` e quello della seconda generazione; `Bracieri Gemelli di Moradin
(Fuoco).pdf`; la scheda PCGen di Tordek; i sei PDF di `Cerebromorphosis/`,
fra cui l'analisi di Lord of Sun and Shadow. Il PDF DM della Corona coincide
col master markdown, che ne è la conversione; Aegis e Anello *Reforged*
coincidono coi loro master. Quello che i PDF aggiungono è in §1.5 e §3.

⚠️ **Non letti**: i log delle sessioni vere, che nel repo non ci sono: `campaign/sessions/` ha una sessione di maggio e i log
retroattivi `[INFERRED]`. Dove il tavolo ha deciso a voce e nessuno l'ha
scritto, questo audit non lo può sapere.

---

## §1 · CORONA DI ADAMANTIO (Thorik)

### Le versioni

| File | Cos'è | Verdetto |
|---|---|---|
| `LaCorona_di_Adamantio-DM.md` | master DM, conversione da PDF | fonte di regole e rituali; **superato** in quattro punti da decisioni successive (§1.3) |
| `000_Guida_Dm_ogetto_prove_rituali_sfide.md` | stessa materia, in markdown pulito | annesso; stesse divergenze del master |
| `00_scheda_Giocatore.md` | la **prima scheda giocatore**: poteri attivi, poteri da risvegliare, i quattro rituali, sinergia con Aegis, giuramento | superata, ma è **la più completa di struttura**: è quella che il DM ricorda |
| `00_Scheda_Giocatore_Aggiornata_Fase2.md`, `01_…Sintesi_Pratica_Fase2.md` | schede dopo il Topazio | superate; portano la **Percezione del Tempo**, che poi sparisce |
| `00_SCHEDA-GIOCATORE-STATO-ATTUALE.md` | scheda viva in markdown, con note DM | la più aggiornata sui costi; conteneva ancora il «−2 COS» dei Doni v1 (corretto qui) |
| `01_Corona_1_Gemma.html` | pagina a una gemma | superata |
| `02_Corona_2_Gemme.html` / `_DM.html` | pagina a due gemme | **incompleta** (§1.2); la `_DM` parlava ancora dei Doni v1 |
| `03_Corona_3_Gemme.html` | pagina a tre gemme | **superata e da non stampare**: Rubino settimanale, Topazio che implode, Aura all'arrivo. Banner messo |
| gli altri `.md`/`.txt` | generazioni precedenti, inglese, scene | snapshot, già marcati nella matrice |

**Nessuna versione era definitiva.** Le nuove `02_Corona_2_Gemme.html` e
`02_Corona_2_Gemme_DM.html` (riscritte il 2026-09-25) lo sono per lo stato a
due gemme, con i poteri in attesa di conferma marcati come tali.

### 1.2 · Potere per potere

Legenda: ✅ c'è ed è coerente · ❌ manca · ⚠️ c'è ma diverso · — non pertinente.
Colonne: **M** master DM · **P** moduli giocati (P1-P3, DEF-1) · **S1** prima
scheda giocatore · **02** pagina a 2 gemme prima di questo audit · **Sk**
`campaign-artifacts.md` · **St** `state.md` §6.

| Potere | M | P | S1 | 02 | Sk | St | Vince, e perché |
|---|---|---|---|---|---|---|---|
| Prerequisiti (nano o mezzonano, BAB +5, fede in Moradin **o** legame con Aegis Fang) | ⚠️ la scheda finale del master chiede anche «un incantesimo divino» | — | ✅ | ❌ | ✅ | — | la formula di S1, ripetuta in `000_…ogetto`, nella pagina a 1 gemma e nella skill. Il banner di T6b dice già che sul prereq vince il master, ma il master si contraddice fra cap. 1 e scheda finale: Thorik è guerriero, e l'incantesimo divino lo escluderebbe dal proprio artefatto |
| Corona di Protezione +2 (deflessione) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | tutti. Il Dono può portarla a +1 (§1.4) |
| Consapevolezza della Pietra | ⚠️ senza Linguaggi | ✅ | ⚠️ senza Trappole | ✅ | ✅ | ✅ | entrambe le liste, DM 2026-07-04 |
| Intuito di Moradin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Volontà Adamantina | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | immunità **e** +4 (master cap. 3) |
| Manto di Pietra e Spirito | ✅ Rit. 3 | — | ⚠️ Rit. 4 | ✅ | ✅ | ✅ | **Rituale 3**, correzione DM 2026-09-20 |
| RD del Manto | «5/epic and evil» | — | — | «5/epico» `[da confermare]` | — | «5/epico» | **domanda D7** |
| +4 CAR, −2 DES, non rimovibile volontariamente | — | ✅ P1 §5 | — | ❌ | — | ✅ | P1, **DM 2026-09-04**. Mancavano dalla pagina |
| −2 DES / +2 COS del pegno del Rituale 3 | — | ✅ DEF-1 §9 | — | solo nel registro | — | ✅ | DEF-1 §9, rettifica DM 2026-07-31/08-06 |
| **Immunità alla paura** | — | ✅ P1 §5 | ⚠️ solo come sinergia con Aegis | ❌ | ❌ | ❌ | **domanda D3** |
| **Scurovisione 36 m** | — | ✅ P1 §5, ripresa in P2 §10 | — | ❌ | ❌ | ❌ | **domanda D3** |
| **Aura di Comando** 1/giorno (*Comando* CD 15, LI 13) | — | ✅ P1 §5 | — | ❌ | ❌ | ❌ | **domanda D3** |
| **Guida di Moradin** 1/giorno (la direzione verso le gemme) | — | ✅ P1 §5 | — | ❌ | ❌ | ❌ | **domanda D3** |
| Topazio: viaggio 1/mese, 1 ora, 1d10 anni, pegno per i non fedeli | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | DM 2026-07-04 per l'ora |
| **Topazio: Percezione del Tempo** (sa quanto manca a Hammerfist) | — | ✅ P3 §10 | — | ❌ | ❌ | ❌ | **domanda D4**; era sulla scheda Fase 2 che il giocatore ha letto |
| **Topazio: Visione Temporale** (echi del passato dei luoghi) | — | ✅ P3 §10 | — | ❌ | ❌ | ❌ | **domanda D4** |
| **Topazio: Rallentare il Tempo** 1/giorno (*accelerazione* 3 round, solo Thorik) | — | ✅ P3 §10 | — | ❌ | ❌ | ❌ | **domanda D4** |
| Smeraldo: tre effetti 1/settimana, 1.000 mo | ✅ | ✅ DEF-1 | ✅ | ✅ | ✅ | ✅ | — |
| Smeraldo: **Chiave del Tempo** (stabilizza il viaggio) | — | ✅ DEF-1 §9 | — | ❌ | — | — | DEF-1, canone giocato. Aggiunto alla pagina come tratto, non come potere attivabile |
| Rubino | ⚠️ 1/settimana, sbloccato al Rit. 3 | ✅ monouso | ⚠️ 1/settimana | «vuota» | ⚠️ «si accende all'alba» | ✅ speso | **monouso, entra al Rituale 4 e si spende nel ritorno**: D16, `DEF-4` Scene 12-13 (DM 2026-09-19). Il Rubino settimanale del master è superato |
| Rituale 4 → Corona +3 | ✅ | ✅ DEF-4 | — | solo DM | ✅ | ✅ | tutti. Con il Dono: **domanda D5** |
| Rituale 4 → Senzienza | ⚠️ «dopo il Rituale 1, con Aegis» | ✅ DEF-4 | ⚠️ «quando impugni entrambi» | solo DM | — | ✅ | **Rituale 4**: `DEF-4` Scena 12 (DM 2026-09-19), `state.md`, la scheda Fase 2 (*«al completamento»*) e soprattutto il **PDF del giocatore** del 22/10/2025: *«dopo aver completato Ritual: Siege of the Eternal Forge»*. D2 chiusa dalla fonte |
| Rituale 4 → Aura della Forgia Eterna | ⚠️ evento unico all'arrivo | ✅ DEF-4 Momento 4 | — | ❌ | ⚠️ evento unico | ✅ matrice | **dopo il duello, fino all'alba la prima volta, poi 1/settimana**: DM 2026-09-20 |
| Rituale 4 → «la Gemma del Tempo si disintegra» | ✅ | ❌ | — | — | — | — | **superato**: il Topazio resta, si spende il Rubino (D16). Il master descriveva un Rituale 4 di una scena sola |
| Rituale 4 → costi | 1d10 anni + pegno alleati | «senza ulteriori costi» (DEF-4 Scena 12) | — | — | — | — | il rito non costa niente; il **viaggio** col Topazio sì: **domanda D6** |
| Costi dei rituali («Rituale della Donazione») | R1 2.500 mo · R2 12.500 mo · R3 40.500 mo + pegno | R2 pagato (Fase 2); R3 solo pegno (DEF-1) | — | ❌ | — | — | riportati nel registro della pagina. R1: al tavolo non registrato |
| Giuramento del Portatore | ✅ | — | ✅ | ❌ | — | — | reintegrato |

### 1.5 · Cosa aggiunge il PDF del giocatore (22/10/2025)

È la prima scheda stampata, quella che il DM ricorda «con molti più poteri e
i riti da fare». Coincide con `00_scheda_Giocatore.md` tranne tre righe:

- il **Manto**: *«Mente Vuota… e una riduzione al danno epica e malvagia»*.
  Il giocatore ha letto «epica e malvagia» qui e «5/epico» sulla pagina del
  2026-07-31: D7 resta aperta, con questa informazione in più;
- il **Rubino** «richiede Anvil of the World»: superato da D16;
- la **sinergia con Aegis Fang** si attiva *«dopo aver completato Ritual:
  Siege of the Eternal Forge»*, con «Liv Inc 18°»: chiude D2.

### 1.6 · I prezzi, come controllo

Il DM ha suggerito di usare i calcoli di prezzo per scoprire poteri mancanti.
Per la Corona le fonti danno **stime a parole, non tabelle**: ~85.000 mo a una
gemma, ~190.000 a due, ~315.000 a tre (quest'ultima col Rubino settimanale,
superato). Non contano poteri che le schede non abbiano. Però **si
contraddicono**: la stima a tre gemme dà alla sola *Mente Vuota* ~240.000 mo,
e la pagina a due gemme, che la *Mente Vuota* ce l'ha già, dice ~190.000 in
tutto. Rifarle con la tabella dei prezzi della SRD è il lotto T10-f. Le due
stime degli stadi 0 e 3 che avevo scritto in una prima stesura delle pagine
non avevano fonte, e sono state tolte.

### 1.3 · La sinergia con Aegis Fang: due strati, che il master confonde

`LaCorona_di_Adamantio-DM.md` cap. 3 mette **in un blocco solo** due cose che i
moduli giocati tengono separate:

| Strato | Cosa dà | Fonte | Stato |
|---|---|---|---|
| **Risonanza** (da quando Thorik ha preso la Corona) | +2 sacro a tutti i TS · +1d6 sacro contro caotici o malvagi · *Richiamo Ancestrale* 1/giorno · *Eco degli Eroi* 1/combattimento · *Bane* +3d6 ×4 contro i draghi | P1 §6, P2 §9, `Sinergie_Artefatti_QuickReference.html`, HANDOUT 4 di `P2` | ❌ **assente** da `SINERGIE-ARTEFATTI-MASTER.md` dal 2026-07-03, e **nessuna decisione registra il taglio**. **Domanda D1** |
| **Completamento** (Rituale 4) | Corona senziente · Aegis +4 Sacra Ritornante, Ego 20 · telepatia coi nani 90 m · nani vicini immuni alla paura · *Guarigione* 1/giorno | master cap. 3, `05_Aegis_Fang_Final_Awakening.html`, `DEF-4` Scena 12 | ✅ canone al Rituale 4. **Domanda D2** solo per chiudere la lettura del master |

⚠️ Il *Bane* del primo strato (+3d6 ×4 contro **tutti** i draghi) contraddice
`ARC07-DEF-2` A7, dove +3d6 ×4 è il premio **contro Fauci di Palude** e
*«invece di +2d6 vs draghi»*. Dentro D1.

### 1.4 · Il Dono e il Rituale 4

- **Doni v1 superati** (2026-09-12): *Il Sangue della Stirpe* (−2 COS), *La
  Memoria della Battaglia*, *Il Filo dell'Ascia*. Restavano nella pagina DM a
  due gemme e in una nota della scheda markdown; tolti.
- **Doni v4-bis** (canone): Thorik dona il +2 di deflessione, scende a **+1**,
  e Hella riceve lo Scudo del Custode. Nella pagina è una casella.
- ⚠️ **Il Rituale 4 non si gioca stasera.** La regia della serata (decisione
  S1) chiude al **primo ariete** (`DEF-4` Scena 10). Il Rituale è la Scena 12:
  **la sessione dopo**. Stasera si gioca solo il Dono.
- ⚠️ **Cosa non dire al giocatore** (`DEF-3` §2-bis e §8-ter): che l'incasso
  vuoto si riempie a −1.000, e che il Rubino si spende. La pagina del giocatore
  dice cosa sblocca il Rituale 4, non dove né cosa costa alla pietra.

---

## §2 · AEGIS FANG (Thorik)

| File | Verdetto |
|---|---|
| `Aegis Fang.docx` / `.pdf` | fonte originale dello Stadio 0; **coincide** col master |
| `00_Aegis_Fang-MASTER-DM.md` | ⭐ master, corretto. Un `[INFERRED]` si risolve dalla sua fonte (sotto) |
| `00_Aegis_Fang-SCHEDA-GIOCATORE-STATO-ATTUALE.md` | corretto (Doni v4-bis) |
| `00_Aegis_Fang_Stadio0.html` / `_DM.html` | **definitive dopo questo audit**; prima portavano ancora il *Filo dell'Ascia* (Doni v1) e non avevano sinergie né la reazione dell'ascia al Dono |
| `05_Aegis_Fang_Final_Awakening.html` | lo Stadio 1, fonte |

| Potere | Fonti | Vince |
|---|---|---|
| Allineamento | `.docx`, master, pagine: **Legale Neutrale**; skill: *Lawful Good* | **LN**, la fonte originale. Skill corretta |
| Poteri inferiori (*cura ferite moderate* 3/g, *resistere all'energia* 1/g) | `.docx`, master, pagina; skill: assenti | aggiunti alla skill |
| *Filo dell'Ascia* | pagine HTML | **superato** (2026-09-12) |
| Reazione al Dono di Thorik | `DEF-3` §5, master, scheda md; HTML: assente | aggiunta |
| Bane contro Fauci (A7) | `DEF-2` §4; si gioca **stasera**, Atto I | casella nella pagina DM, non nella pagina giocatore (è una scoperta) |
| Stadio 1: aura dei comandanti | master: `[INFERRED — effetto non quantificato]` | **risolto dalla fonte**: `05_…Final_Awakening.html` dice *telepatia coi nani entro 90 m* e *nani vicini immuni alla paura* (aura di 18 m nel calcolo del valore) |
| Stadio 1: quando | `.docx`/master: apoteosi all'Assedio + Corona senziente; `state.md`: vittoria dell'Assedio; `DEF-4` Scena 12: una scena | coincidono: tutto al Rituale 4 |

---

## §3 · ANELLO DELL'ILLUMINAZIONE CAOTICA (Artemis)

| File | Verdetto |
|---|---|
| `PG/Artefatti/Ring of Chaotic Illumination.md` | generazione 1, inglese, pre-riforgiatura; ha dettagli dei poteri di crisi che poi cadono |
| `PG/Artefatti/Ring_of_chaotic_illumination-master.md` | generazione 2, «documento riservato DM»: intelligenza (Int 14, Sag 12, Car 16, Ego 12, CB), prova di legame CD 17, lo Scettro di Ylluminuk |
| `Old/` | export delle due generazioni, deprecati |
| `00_Ring_of_Chaotic_Illumination_Revised.md` | ⭐ master (A10), inglese, *Reforged* |
| `00_Ring-SCHEDA-GIOCATORE-STATO-ATTUALE.md` | scheda viva, con il Dono |
| `00_Ring_Riforgiato.html` / `_DM.html` | **definitive dopo questo audit** per lo stadio 2; prima mancava il Dono |
| `Artemis/Cerebromorphosis/…Lord of Sun and Shadow - Power Analysis….pdf` | **lo stadio 1 dell'Anello**, che nessuna versione successiva riportava: i poteri di Mask svegli, tre poteri di crisi, le quattro scelte A-D della crisi |
| `Artemis/Cerebromorphosis/Italiano/cerebromorphosis_italian-final.md` | master eletto del sistema di crisi: la **Opzione C, Rifiuto**, è la scelta di Artemis |
| `Old/Ring_of_chaotic_illumination_pg*.html` | la scheda italiana del giocatore dello stadio 0: **42.000 mo**, i tre poteri, i comandi in infernale |
| `Artemis/Cerebromorphosis/` | sottosistema di crisi, non poteri dell'anello |
| `PrestigeClass/lord_sun_shadow/` | percorso rifiutato: nessun potere in gioco |

| Potere | Revised | Pagine HTML | Generazione 1 / 2 | Moduli giocati | Vince |
|---|---|---|---|---|---|
| Sempre attivi (vista, conoscenze, diplomazia, doppia fiamma) | ✅ | ✅ | vista ✅ | — | Revised |
| Sei poteri attivabili | ✅ | ✅ | tre soli | — | Revised |
| Parole di comando (*Noctis Revelum/Velum* per la vista) | ❌ | ❌ | ✅ | — | colore; aggiunte alla pagina DM come nota |
| Aspetto per chi non è il prescelto | acquamarina blu | — | anello di **resistenza +3** | — | Revised; la versione 1 resta nota DM |
| *Dawn's Defiance* | *Spezzare Incantamento*, immunità 24 h | lato DM | + luce 3 m, **1/settimana** | — | **domanda D9** |
| *Solar Purge* | 1d6/DV alle aberrazioni, anello spento 24 h | lato DM | + cura metà dei danni, toglie un livello negativo | — | **domanda D9** |
| Intelligenza dell'anello (Ego 12) | ❌ «opera con lui» | ❌ | ✅ gen. 2 | — | Revised: **nessun Ego**. La generazione 2 aveva anche il cambio d'allineamento dello Scettro, un filo mai giocato |
| *Dualità Armoniosa* (+1 carica con la Corona entro 9 m) | ❌ | ❌ | — | ✅ P1 §7, P2 §9 | **domanda D9**: il Riforgiato non ha cariche, quindi va tradotta o tolta |
| *Parlare coi Morti* sul corpo di Hella 1/giorno | ❌ | ❌ | — | ✅ P1 §7, «fino alla resurrezione» | temporaneo: **scade stasera**. Nota DM |
| Il Dono (1d6 di *Eldritch Blast*) e le reazioni | scheda md ✅ | ❌ | — | `DEF-3` §5 | aggiunto |
| Sinergie S1-S3 | ✅ | ✅ | — | P2 §9 (+4 all'Alba Oscura) | S1-S3 come nel master delle sinergie (T4, ripetuto dal Revised) |

### 3.1 · Gli stadi dell'Anello

| Stadio | Innesco (dalle fonti) | Poteri | Pagine |
|---|---|---|---|
| **S0** · l'anello del caos | il legame con Artemis | Visione Potenziata, Ali d'Ombra, Passo d'Ombra; due poteri di crisi dormienti. **42.000 mo** | `01_Anello_S0_Originale{,_DM}` |
| **S1** · le due divinità | Lathander e Mask; la crisi di Cerebromorphosis nella Tomba di Belkram | Mask sveglio: +4 Osservare al buio, **+2 deviazione in volo**, 3/giorno +1d6 elettricità in carica, **Sussurri di Mask**; crisi: Sfida dell'Alba, Purificazione Solare, **Santuario del Crepuscolo** (1/mese, solo qui). **52.000 mo** | `02_Anello_S1_Due_Divinita{,_DM}` |
| **S2** · il Riforgiato | il **Rifiuto** di Lord of Sun and Shadow (Opzione C) e la Forgia | quattro costanti, sei attivabili, due di crisi. **163.400 gp** | `00_Ring_Riforgiato{,_DM}` |
| **S3** · il Caos Ultimo | la Torre Invisibile: Zalkatar sconfitto, o purificato rinunciando a un potere (P2A-PARTE4) | **decisi dal DM il 2026-09-25 (D13)**: *Alba Voluta*, *Purificazione del Crepuscolo*, il *Prezzo dell'Armonia* | `04_Anello_S3_Caos_Ultimo{,_DM}` |

**I prezzi.** 42.000 mo (scheda italiana dello stadio 0) contro 62.000 gp
(prima versione inglese); l'analisi dello stadio 1 dice 52.000 «aumentato per
la doppia natura», che torna solo col 42.000. La tabella voce per voce del
*Revised* (163.400 gp) non conta il *Passo d'Ombra* né i poteri di crisi. Nessun
prezzo nasconde un potere che le schede non abbiano.

**La Opzione C.** Il master italiano le dà la *Fortezza Mentale* (+2 ai TS
contro l'influenza divina) e poteri di Lathander solo di crisi «con penalità»;
il PDF inglese la fa molto più pesante (−2 LI, Sfida dell'Alba 1/mese, un
difetto, un talento bonus, anello non rimovibile 30 giorni). Nessuna delle due
è sulla scheda di Artemis in `state.md` o in `campaign-party.md`: domanda D12.

---

## §4 · BRACIERI GEMELLI DI MORADIN + CINTURA DELLA DEVASTAZIONE (Tordek)

| File | Verdetto |
|---|---|
| `05_Bracieri_Gemelli_Scheda_PG_Completa.md` / `.html` | ⭐ **definitive** (pagina giocatore), con due correzioni sotto |
| `01_Bracieri_Gemelli_di_Moradin.md` | master di struttura e parte DM (il Dono sta qui) |
| `02_`, `03_` | scene dei due risvegli, giocate |
| `04_…Fuoco` | superata dallo stadio Terra |
| `05_…Final.html`, `05_…copy 2.html` | copie deprecate |
| `00_Cintura_della_Devastazione.md` | master della Cintura |

| Voce | Fonti | Vince |
|---|---|---|
| Nomi dei poteri del Fuoco | `01_`: *Pugno di Moradin*, *Salto Infuocato*; `04_`/`05_`: *Pugni di Magma*, *Salto Fiammeggiante*, *Passo di Brace*; skill: i nomi di `01_` | **`05_`**, la scheda che il giocatore ha in mano (regola 2026-09-20). Skill allineata |
| Benedizione della Forgia | DM 2026-07-04: **permanente**; `05_.md`: permanente; `05_.html` e Cintura: «fino al completamento dell'avventura» | **permanente**. HTML e Cintura corretti |
| *Diventare una Collina* | `05_`, `state.md`, changelog 2026-08-01 | ✅ coerenti; mancava dalla skill |
| Stadio Terra | skill: «in completamento»; tutto il resto: giocato | giocato. Skill corretta |
| Il Dono (Ancoraggio della Montagna) | `01_` e `DEF-3` §5 ✅; `05_.html`: solo nella riga delle sinergie | aggiunto come casella |

**Pagina DM**: non esiste in HTML, e non serve una pagina nuova: la parte DM
dei Bracieri è `01_Bracieri_Gemelli_di_Moradin.md`, che ha già il Dono, le
reazioni e la coscienza. Fiducia del DM alta, e l'audit la conferma.

---

## §5 · COLLANA DEI SEMI ETERNI (Hella)

Pagine fatte il 2026-09-25 (PR #177) su decisioni del DM dello stesso giorno:
`01_Collana_Radicata{,_DM}.html`, `02_Durik_Guardiano_di_Pietra{,_DM}.html`.
Confrontate con `DEF-3` §5 e §7, con la skill e con `SINERGIE` §1: coerenti, i
Doni sono già caselle. **Definitive, nessuna modifica.**

---

## §6 · I file toccati da questo audit

| File | Cosa |
|---|---|
| `00…03_Corona_*{,_DM}.html` | **otto pagine a stadi**, giocatore e DM; le revisioni precedenti di 01, 02, 02_DM e 03 in `_ARCHIVIO/pagine-v1-2026-09-25/` |
| `01_Anello_S0_Originale{,_DM}.html`, `02_Anello_S1_Due_Divinita{,_DM}.html`, `04_Anello_S3_Caos_Ultimo_DM.html` | **gli stadi dell'Anello** che mancavano |
| `plans/adr/ADR-0071-…`, `scripts/tests/test_versioni_artefatti.py`, `skills/REGISTRO-NORME-EDITORIALI.md` | il versionamento, il suo gate, la norma registrata |
| `00_SCHEDA-GIOCATORE-STATO-ATTUALE.md` (Corona) | nota 3-ter dei Doni v1 corretta; rimando alle pagine |
| `LaCorona_di_Adamantio-DM.md` | banner con i quattro punti superati |
| `00_Aegis_Fang_Stadio0{,_DM}.html` | Dono v4-bis, sinergie, Stadio 1 e A7 lato DM |
| `00_Aegis_Fang-MASTER-DM.md` | `[INFERRED]` dello Stadio 1 risolto dalla fonte |
| `00_Ring_Riforgiato{,_DM}.html` | Dono, note di crisi e dei moduli giocati lato DM |
| `05_Bracieri_…Completa.html`, `00_Cintura_della_Devastazione.md` | Benedizione permanente; Dono nella pagina |
| `ARTEFATTI-MATRICE-VERSIONI.md` | una riga «versione definitiva» per artefatto |
| `skills/rumblingstone-campaign/references/campaign-artifacts.md` | Aegis LN e poteri inferiori; Corona gemme, Aura, prereq; Bracieri coi nomi della scheda |

---

## §7 · Domande al DM

Una per voce, con la proposta. Nelle pagine, ogni voce aperta porta la
marcatura `[da confermare col DM — D<n>]` e **non è scritta come canone**.
Le stesse domande sono in `plans/PIANO-REVISIONE-TRASVERSALE-COERENZA-E-QUALITA.md`
§3, lotto T10, dove il gate `decisioni_dm` le conta.

| # | Domanda | Proposta |
|---|---|---|
| D1 | **La Risonanza fra Corona e Aegis Fang** (P1 §6, P2 §9, la quick reference data al tavolo): +2 sacro a tutti i TS, +1d6 sacro contro caotici o malvagi, *Richiamo Ancestrale* 1/giorno, *Eco degli Eroi* 1/combattimento. Il master delle sinergie l'ha tolta il 2026-07-03 senza dirlo. È attiva? | **Sì**, dal P1: è nel modulo giocato e nell'handout. Entra in `SINERGIE` come **S0**. Il *Bane* +3d6 ×4 invece resta **solo contro Fauci**, come dice A7: contro gli altri draghi vale il +2d6 della *Dragondoom* |
| D3 | **I bonus di quando l'ha indossata** (P1 §5): immunità alla paura, scurovisione 36 m, *Aura di Comando* 1/giorno (*Comando* CD 15, LI 13), *Guida di Moradin* 1/giorno. Il 2026-09-04 ha confermato solo +4 CAR e non-rimovibilità dallo stesso blocco | **Sì a tutti e quattro**: stanno nello stesso elenco di cui metà è già canone, e nessuna fonte li revoca |
| D4 | **I poteri del Topazio** (P3 §10): *Percezione del Tempo* (sa quanto manca a Hammerfist), *Visione Temporale* (echi del passato dei luoghi), *Rallentare il Tempo* 1/giorno (accelerato 3 round, solo lui). E il «+1 a tutti i poteri della Corona»? | **Sì ai tre**: la *Percezione* era sulla scheda Fase 2 che il giocatore ha letto. **No al +1 generico**: non dice a cosa si somma, e nessuna scheda l'ha mai applicato. ⚠️ *Rallentare il Tempo* e l'Eco del Custode sono entrambi *accelerazione*: non si sommano |
| D5 | **La deflessione dopo il Rituale 4, se Thorik ha donato**: +2 (il rito aggiunge uno) o +3 (il rito la porta a +3 comunque)? | **+2**. `DEF-3` §5: *«La Corona protegge di 1 in meno, per sempre»* |
| D6 | **Il Topazio al viaggio a −1.000**: si tira l'invecchiamento di 1d10 anni? E Artemis, che non è né nano né fedele di Moradin, paga il pegno o tira Tempra CD 25? `DEF-4` non ne parla, e la Scena 12 dice «senza ulteriori costi» per il **rito** | **Sì a entrambi, al portale**: sono il prezzo del Topazio, stampato sulla scheda da luglio; D-B esclude i costi del rito, non quelli del viaggio. La *Guarigione del passaggio* non li toglie, come non toglie il −4 DES |
| ~~D2~~ | chiusa dalla fonte: il PDF del giocatore del 22/10/2025 mette la sinergia completa con Aegis Fang «dopo aver completato Ritual: Siege of the Eternal Forge» | — |
| D7 | **La RD del Manto**: 5/epico o 5/epico **e** male? Il giocatore ha letto «epica e malvagia» nel PDF del 2025 e «5/epico» nella pagina del 2026-07-31 | **5/epico**, l'ultima letta |
| D8 | **La Senzienza della Corona**: il master le dà Int 16, Sag 17, Car 18, **Ego 20**, gli stessi numeri dello Stadio 1 di Aegis Fang. Li ha entrambi? | **Sì, e la Corona non tira mai l'Ego contro Thorik**: `DEF-4` la vuole voce calda o fredda, con un *Want* suo (la montagna), non un padrone. Se il DM preferisce, niente punteggi |
| D9 | **L'Anello**: (a) i poteri di crisi tornano ai dettagli della prima versione (*Dawn's Defiance* 1/settimana con luce 3 m; *Solar Purge* che cura metà dei danni e toglie un livello negativo)? (b) la *Dualità Armoniosa* dei moduli (+1 carica con la Corona vicina) come si traduce, visto che il Riforgiato non ha cariche? | (a) **No**: vince il Revised, eletto dopo e con la fiducia bassa del DM sulle versioni vecchie. (b) **Tolta**: era scritta per l'anello a cariche della P1, e nessuna scheda del Riforgiato l'ha mai portata |
| D10 | **I livelli minimi** del libro della Corona (5°, 6°, 13°, 15°, 17°, 20°) contano? Thorik è di 13° e ha già Volontà Adamantina (15°) e Manto (17°) per decisione del DM | **No, decide il rituale**; la tabella dei livelli resta sulle pagine come indicazione |
| D11 | **Lo stadio 1 dell'Anello** (i poteri di Mask svegli, dall'analisi di Lord of Sun and Shadow) è stato usato al tavolo? | Il DM lo sa; la pagina c'è comunque, perché è la storia dell'anello e spiega da dove viene il Riforgiato |
| D12 | **Gli effetti della Opzione C** sulla scheda di Artemis: quelli del master italiano, del PDF inglese, o nessuno? | **La Fortezza Mentale** del master italiano (+2 ai TS contro l'influenza divina); la penalità ai poteri di crisi è superata dalla riforgiatura |
| D13 | **I poteri del Caos Ultimo** (stadio 3 dell'Anello, Torre Invisibile) | Da progettare col DM. Una proposta di forma, non canone, è sulla pagina `04_Anello_S3_Caos_Ultimo_DM.html` |


### §7-bis · Le risposte del DM (2026-09-25, pomeriggio)

Prima di chiedere, ho cercato le versioni **stampate** fuori da `PG/Artefatti/`.
Due stampe del 16/01/2026 hanno correzioni fatte a mano al tavolo, che nessun
file markdown aveva registrato: la quick reference delle sinergie
(`07_…/SinergieArteFattiQuickReference.pdf`) toglie l'*Eco degli Eroi* dalla
Risonanza e la *Dualità Armoniosa* dalla sinergia Corona + Anello, lasciando le
righe vuote; `BenedizioniDiMoradin.pdf` tiene tre benedizioni su sei. Le copie
della cartella `06_` sono identiche a quelle di `PG/`.

| # | Decisione | Applicata in |
|---|---|---|
| D1 | **La stampa del 16/01**: Risonanza = +2 sacro ai TS, +1d6 sacro contro caotici o malvagi, *Richiamo Ancestrale*. Niente *Eco degli Eroi*; contro i draghi solo il Bane di A7 su Fauci | pagine Corona e Aegis, `SINERGIE` S0, skill |
| D3 | **Tutti e quattro** i bonus di quando l'ha indossata sono canone | pagine Corona, skill |
| D4 | Del Topazio restano **Percezione del Tempo** e **Visione Temporale**; tolti *Rallentare il Tempo* e il «+1» | pagine Corona, skill |
| D5 | Dopo il Rituale 4: **+3**, o **+2** se ha donato | pagina Corona S3, skill |
| D6 | Al portale si pagano **entrambi**: 1d10 anni a Thorik, pegno o Tempra CD 25 ad Artemis | pagina DM Corona S2 |
| D7 | RD del Manto **5/epico e male** (il PDF del 2025, contro la mia proposta) | pagine Corona, scheda markdown, skill. ⚠️ `state.md` §6 dice ancora «RD 5/epico»: si corregge sul ramo del gruppo |
| D8 | Senzienza **Int 16, Sag 17, Car 18, Ego 20**, senza dominio | pagina Corona S3 |
| D9 | Poteri di crisi come nel **PDF riforgiato**; *Dualità Armoniosa* tolta | pagine Riforgiato e S0 |
| D10 | Livelli **indicativi**: decide il rituale | pagine Corona |
| D11 | Lo stadio 1 dell'Anello **non è mai stato dato**: al tavolo c'è stata solo la crisi | pagina giocatore S1 tolta, DM resta |
| D12 | Ad Artemis la **Fortezza Mentale** (+2 ai TS contro l'influenza divina) | pagine Riforgiato e S1 DM, skill. ⚠️ va sulla scheda di Artemis e in `state.md` col prossimo `dm.py session end` |
| D13 | Approvata la proposta: *Alba Voluta* 1/giorno; *Purificazione del Crepuscolo* 1/giorno **senza** la cura, che resta della versione di crisi; nel *Prezzo dell'Armonia* **sceglie Artemis** quale potere perdere, e **Zalkatar lo eredita** da alleato | `04_Anello_S3_Caos_Ultimo{,_DM}.html` (r3); la pagina del giocatore si consegna alla Torre |
| D14 | Aegis Fang: il giocatore la usa **ritornante** (corretto: è nel `.docx` dal primo giorno). Il DM, dopo aver visto le fonti: il potere è la **Dragondoom**, la punizione del MIC (3/giorno, +1d6…+4d6 per taglia di drago); il *bane* contro non morti e il Tuono sonoro **non ci sono**: +2d6 contro non morti e aberrazioni arriva solo con lo stadio 1. Vale la scheda del repo | pagine Aegis S0 (r5), master, skill |

### §7-ter · Le domande aperte dopo gli stadi (2026-09-25, sera)

Il DM ha chiesto di completare gli stadi di tutti gli artefatti. Dove una fonte
fissa il momento ma non i poteri, la pagina è **solo DM** e porta una bozza; la
pagina del giocatore si fa quando il DM approva.

| # | Domanda | Proposta |
|---|---|---|
| D15 | **Aegis Fang allo stadio 1** tiene la *Dragondoom* e i poteri inferiori dello stadio 0? La fonte dello stadio 1 non li nomina, e il suo conto del valore (+7, 98.000 mo) non conta la Dragondoom | **Sì, restano**: uno stadio aggiunge e non toglie, come per la Corona, e la caccia ai draghi è il motore dell'ascia. Il bonus equivalente sale a +8 (128.000 mo) |
| D16 | **Il terzo stadio dei Bracieri**, *le Chiavi della Forgia*: innesco al Torneo di Dauth (Tordek non apre il portale che Xal'thor gli chiede), *La Chiave* 1/settimana verso la Forgia Eterna, *Mente di Pietra* +4 contro psionici e ammaliamenti, un orologio che avanza a ogni uso | bozza sulla pagina `06_Bracieri_S3_Chiavi_della_Forgia_DM.html`. Le fonti dicono che i Bracieri **sono** chiavi planari: la bozza parte da lì |
| D17 | **La Collana Fiorita e la Foresta che Cammina**: i momenti sono canone, i poteri no. Fiorita: *Radici che Sentono*, *Il Muro dei Guardiani* 1/giorno, Avatar 2/giorno, un'eco di Dauth; Foresta che Cammina: i due Treant insieme senza il mese di silenzio, *Radici nel Mythal* | bozze sulle pagine `03_Collana_S2_Fiorita_DM.html` e `04_Collana_S3_Foresta_che_Cammina_DM.html`, dalla materia di ARC-09 P1B, P1C e P3 riportata a tre semi |

**Le risposte del DM, la sera stessa (2026-09-25)**:

| # | Decisione | Applicata in |
|---|---|---|
| D15 | Aegis Fang allo stadio 1 **tiene** Dragondoom e poteri inferiori (equivalente +8) | pagine Aegis S1 (r4), master, skill, `state.yaml` |
| D16 | Il terzo stadio dei Bracieri, **le Chiavi della Forgia**, approvato com'era proposto | pagine Bracieri S3 giocatore e DM (r3), skill |
| D17 | Fiorita e Foresta che Cammina approvate come proposte, *Radici nel Mythal* in ogni cerchio consacrato | pagine Collana S2 e S3 giocatrice e DM (r3), Radicata DM, skill |

Con l'autorizzazione del DM, **una volta sola**, sono state scritte in
`campaign/state.yaml` (e rigenerato `state.md`) tre righe di fatti decisi:
Aegis Fang Dragondoom (D14, D15), il Manto con RD 5/epico e male (D7), la
Fortezza Mentale di Artemis (D12). Niente esiti della serata: quelli restano
a `dm.py session end`.

---

## §8 · Il versionamento (ADR-0071)

Ogni pagina viva porta `artefatto · S<stadio> · r<revisione> · <data>` e sta
nel registro di `ARTEFATTI-MATRICE-VERSIONI.md` §0; le revisioni superate vanno
in `_ARCHIVIO/`. Il test `scripts/tests/test_versioni_artefatti.py` li tiene
allineati, e ha trovato un errore al primo giro (le pagine del Riforgiato
dicevano «S1», che con i quattro stadi dell'Anello è diventato «S2»).

## §9 · Gli stadi, artefatto per artefatto (2026-09-25, sera)

| Artefatto | Stadi con le pagine | Cosa manca |
|---|---|---|
| Corona | 0, 1, 2, 3 (giocatore e DM) | — |
| Anello | 0 (G+DM), 1 (solo DM, D11), 2 (G+DM), 3 (G+DM, D13 decisa) | — |
| Aegis Fang | 0 (G+DM), 1 (G+DM) | — (D15 decisa) |
| Bracieri | 0, 1, 2, 3 (G+DM) | — (D16 decisa) |
| Collana | 0 (solo DM: la Collana non esisteva), 1, 2, 3 (G+DM) | — (D17 decisa) |

Cosa ho trovato costruendoli, oltre alle tre domande:

- **La Collana di ARC-09 non è quella del canone.** P1B e P1C, scritti prima
  del rito, parlano di una «Collana dei Semi Treant» con **quattro** semi che
  Hella avrebbe già al collo. Il canone ne ha **tre**, e la Collana nasce al rito.
  Le bozze della Fiorita riportano quella materia a tre semi; i due moduli, al
  momento di prepararli, vanno corretti allo stesso modo.
- **Damarath** è il vecchio nome di **Rethmar** (D2 del piano ARC-09).
- **I Bracieri hanno due stesure dello stadio 1.** `01_…md` «Versione 1» (Pugno
  di Moradin, Salto Infuocato con +10 a Saltare) e la scheda `04_…Fuoco`
  (Pugni di Magma, Passo di Brace). Vale la **04**, che il giocatore ha letto e
  che il PDF «Fuoco» stampa. Il +10 a Saltare della Versione 1 torna allo **stadio 2**:
  la scheda 05 lo dà col Salto Fiammeggiante, finché resta un uso.
- **Le schede degli stadi hanno la lore e lo stile delle originali** (richiesta del
  DM prima del merge). I Bracieri S0, S1 e S3 sono costruiti sulla scheda 05
  (aspetto e lore, statistiche, requisiti, senzienza, tabelle dei poteri, dettagli
  del Salto, riepilogo tattico); la pagina DM dello stadio 2 è la 05 intera più la
  parte DM; la vecchia scheda 04 è in `_ARCHIVIO/pagine-v1-2026-09-25/`. Le
  pagine della Collana S2 e S3 partono dalla Radicata e portano tutti i poteri che
  restano, con i nuovi tratteggiati; Aegis S1 ha la lore e il valore della sua
  fonte; l'Anello S3 riporta scheda tecnica e poteri del Riforgiato.
- **Le cariche di devastazione sono della Cintura** (D17 del piano ARC-07): le
  schede dei Bracieri le riportano come sinergia. È un solo gruppo di cariche.

⚠️ **Una nota per il DM sui Bracieri**: la scheda PCGen di Tordek (12° livello)
porta equipaggiati i *guanti della forza dell'orco*, sullo stesso slot dei
Bracieri. È una scheda vecchia; se è ancora quella in uso, uno dei due non
funziona.

---

## §10 · I prezzi voce per voce, con la tabella della SRD (lotto T10-f)

Gli artefatti non hanno prezzo e non si vendono. Il conto serve a **controllare
che le schede siano complete**: una stima di valore che conta un potere assente
dalla scheda, o che manca un potere presente, è un buco. Regole usate (SRD,
*Estimating Magic Item Gold Piece Values*, riassunta in
`skills/dnd-35-srd/references/items.md`):

- bonus di caratteristica = bonus² × 1.000; deviazione, armatura naturale = bonus² × 2.000;
  CA di altro tipo (cognizione) = bonus² × 2.500; competenza a un'abilità = bonus² × 100;
  potenziamento d'arma = bonus² × 2.000;
- incantesimo continuo o a uso = livello × LI × 2.000; a parola di comando = livello × LI × 1.800;
  n usi al giorno = diviso (5 ÷ n); un incantesimo continuo che dura 24 ore = metà;
- **LI minimo** dell'incantesimo, non il 20° dell'artefatto: è come la SRD prezza gli oggetti comuni;
- **somma semplice**: è un **limite inferiore**. La SRD alza il prezzo quando un oggetto
  ha più poteri diversi, ma il fattore che ricordo (×1,5 sul minore) e quello della
  skill `items.md` (×2) non coincidono `[INFERRED — da verificare sul testo SRD]`;
- **fuori tabella**: i poteri che la SRD non sa contare (1/settimana, 1/mese,
  viaggi nel tempo, RD speciali). Si elencano, non si inventano.

### Corona, stadio 2 (oggi)

| Voce | Formula | mo |
|---|---|---|
| +2 di deviazione | 2² × 2.000 | 8.000 |
| +4 Carisma | 4² × 1.000 | 16.000 |
| Consapevolezza: *individuare porte segrete* a volontà | 1 × 1 × 2.000 | 2.000 |
| Consapevolezza: *trovare trappole* a volontà | 2 × 3 × 2.000 | 12.000 |
| Consapevolezza: *comprensione dei linguaggi* a volontà | 1 × 1 × 2.000 | 2.000 |
| Su pietra: +2 cognizione alla CA | 2² × 2.500 | 10.000 |
| Su pietra: +1 morale ad attacco e danni | come +1 d'arma, per analogia | 2.000 |
| Manto: *Mente Vuota* continua | 8 × 15 × 2.000 ÷ 2 (dura 24 ore) | **120.000** |
| Dal primo giorno: scurovisione 36 m | 2 × 3 × 2.000 | 12.000 |
| *Aura di Comando* 1/giorno (*comando*, LI 13 come da fonte) | 1 × 13 × 1.800 ÷ 5 | 4.680 |
| *Guida di Moradin* 1/giorno (come *localizza oggetti*) | 2 × 3 × 1.800 ÷ 5 | 2.160 |
| Intuito: +4 cognizione ad Artigianato (fabbro) | 4² × 100 | 1.600 |
| Intuito: *visione del vero* 1/giorno (chierico 5°) | 5 × 9 × 1.800 ÷ 5 | 16.200 |
| **Totale che la tabella sa contare** | | **≈ 208.600** |
| Fuori tabella | immunità alla paura; Volontà Adamantina; RD 5/epico e male; *Comunione* 1/mese; il Topazio (viaggio, Percezione e Visione del Tempo); lo Smeraldo 1/settimana (*muro di pietra*, *santificare*, *terremoto*) | — |

Cosa dice il conto:

- **La stima della pagina a tre gemme era sbagliata di un fattore due**: dava alla
  sola *Mente Vuota* ~240.000 mo, ma l'incantesimo dura 24 ore e la SRD dimezza.
  Le pagine della Corona (r4) ora citano questo conto.
- **La pagina HTML del Manto taceva la parte più forte di *Mente Vuota***:
  l'immunità a **tutti** gli effetti mentali. La scheda markdown la diceva; le
  pagine (r4) adesso anche.
- **Volontà Adamantina è ridondante col Manto.** Arrivano allo stesso rituale, e
  *Mente Vuota* dà già l'immunità a charme e compulsione, ovunque. Volontà
  Adamantina conta solo se il Manto viene soppresso (un *campo anti-magia* non
  basta: sono entrambi soprannaturali). Non è un errore da correggere: è una cosa
  che il DM deve sapere quando dà a Thorik un nemico che domina.

### Corona, stadio 3 (al Rituale 4), in più

| Voce | Formula | mo |
|---|---|---|
| deviazione da +2 a +3 (o resta +2 se ha donato) | 3² × 2.000 − 8.000 | +10.000 (o 0) |
| Senzienza, Aura della Forgia Eterna 1/settimana, il Rubino | tabella degli oggetti intelligenti; 1/settimana; uso singolo | fuori tabella |

### Anello, stadio 2 (il Riforgiato)

| Voce | Formula | mo |
|---|---|---|
| Scurovisione 36 m | 2 × 3 × 2.000 | 12.000 |
| +8 competenza a Conoscenze (arcane) e (religioni) | 8² × 100, due volte | 12.800 |
| +2 competenza a Diplomazia | 2² × 100 | 400 |
| Resistenza al fuoco 10 | come l'anello minore della SRD | 12.000 |
| Ali d'Ombra: *volare* a volontà | 3 × 5 × 2.000 | 30.000 |
| Passo d'Ombra: *porta dimensionale* ogni 5 round | 4 × 7 × 2.000, come a volontà | 56.000 |
| Luce di Lathander 1/giorno (*luce diurna*) | 3 × 5 × 1.800 ÷ 5 | 2.700 |
| Ombra di Mask 1/giorno (*invisibilità superiore*) | 4 × 7 × 1.800 ÷ 5 | 10.080 |
| Invocazione Tempesta di Fuoco 1/giorno (8d6, come *palla di fuoco* LI 8) | 3 × 8 × 1.800 ÷ 5 | 8.640 |
| **Totale che la tabella sa contare** | | **≈ 144.600** |
| Fuori tabella | *Vista del Diavolo*; +1d6 fuoco e +1d6 freddo all'*Eldritch Blast*; Attacco in Volo; il bonus morale della Luce; il secondo bersaglio dell'Ombra; Dono dell'Unità; i poteri di crisi | — |

Il master *Revised* diceva **163.400 gp** senza contare il Passo d'Ombra: con LI
più alti dei minimi i due conti si avvicinano. **Nessun potere manca**: le voci
della stima sono tutte sulla scheda.

**Stadio 3, in più**: *Alba Voluta* 1/giorno (*spezzare incantamento*, livello 5,
LI 9) = 5 × 9 × 1.800 ÷ 5 = **16.200**; la *Purificazione del Crepuscolo* è fuori
tabella; il *Prezzo dell'Armonia* toglie il potere che Artemis sceglie.

### Aegis Fang

| Stadio | Voce | mo |
|---|---|---|
| 0 | +2, Ritornante (+1), Dragondoom (+1) = equivalente +4 | 4² × 2.000 = 32.000, + 330 l'ascia perfetta |
| 1 | +4, Sacra (+2), Ritornante (+1) = equivalente +7 | 7² × 2.000 = **98.000**, come dice la fonte |
| 1 (D15) | + Dragondoom = equivalente +8 | 8² × 2.000 = 128.000 |
| 1 | *Guarigione* 1/giorno, come base | 6 × 11 × 1.800 ÷ 5 = 23.760; che colpisca **tutti** i nani entro 9 m è fuori tabella |
| 0 e 1 | senzienza, poteri inferiori, telepatia, immunità alla paura dei nani | tabella degli oggetti intelligenti, non applicata qui |

### Bracieri e Collana

Quasi tutti i loro poteri sono su misura (colpi elementali, salto, evocazioni,
Avatar) e la tabella non li sa contare. Le voci che sa contare:

- **Bracieri**: resistenza al fuoco 10 = 12.000; *Frantumare* 1/giorno (livello 2,
  LI 3) = 2 × 3 × 1.800 ÷ 5 = 2.160. Le stime del file `01_` (~60.400 per il Fuoco,
  ~94.900 completo) sono fatte sulla **Versione 1**, non sulla scheda 04 che vale:
  contano *Pugno di Moradin*, che la scheda non ha, e non contano
  Passo di Brace, Benedizione e Collina, che la scheda ha. **Sono da rifare**
  quando il DM vuole un numero; per la completezza il confronto basta.
- **Collana**: +4 Saggezza = 4² × 1.000 = 16.000; +3 armatura naturale = 3² × 2.000 = 18.000.
  Il resto è fuori tabella, e la scheda lo dice già: «nessun valore che si possa scrivere».

