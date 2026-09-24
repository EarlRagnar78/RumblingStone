# Prompt di consegna — playtest del booklet e della guida giocatori

> **A cosa serve questo file.** Il modulo è collaudato come **testo** (18 rilievi +
> dry-run, `PLAYTEST-ALFA.md` §2-§4) e come **schede** (§6). Non lo è come **libro
> illustrato**: le venti immagini sono entrate dopo, e nessuno ha ancora guardato
> dove atterrano. Qui c'è lo stato esatto e il prompt da incollare in una sessione
> nuova, scritto per essere autosufficiente.
>
> Chi lo riceve **non ha letto** la conversazione che l'ha prodotto.

---

## §1 · Stato al 2026-08-18 — cosa è verificato e cosa no

| Ambito | Stato | Dove |
|---|---|---|
| Testo del modulo: 18 rilievi + dry-run cronometrato delle tre serate | ✅ Lotto 2 | `PLAYTEST-ALFA.md` §2-§4 |
| Le sei schede: aritmetica, economia, CD, poteri | ✅ 2026-08-17, **2 correzioni** | `PLAYTEST-ALFA.md` §6 |
| Impaginazione delle schede (6 pagine A4, una per PG) | ✅ vista a occhio, pagina per pagina | `homebrew/DRAPPO-SCHEDE-PG.manifest.json` |
| Immagini presenti e derivate committate | ✅ 20 master + 20 derivate `web/` | `ALLEGATI/immagini/` |
| **Booklet del DM con le immagini dentro** | ❌ **mai guardato** | `homebrew/DRAPPO-BOOKLET-DM.html` |
| **Guida giocatori con le immagini dentro** | ❌ **mai guardata** | `homebrew/DRAPPO-BOOKLET-GIOCATORI.html` |
| Tavolo vero | ❌ mai — è il gate dichiarato da mesi | `PLAYTEST-ALFA.md` §5 |

**Numeri utili per capire cosa è cambiato**: il booklet del DM è passato da **0,3 MB
a 7,45 MB** (HTML, immagini incorporate) e da **20 a 72 pagine** in stampa. La guida
giocatori da 0,04 a 2,5 MB. Sono le figure: prima non c'erano.

## §2 · Il lavoro richiesto

**Passata 1 della skill `rumblingstone-playtest`, applicata all'oggetto impaginato**
— non al testo, che è già stato collaudato. Le domande a cui rispondere:

### Sul booklet del DM (`DRAPPO-BOOKLET-DM`, 20 capitoli)

1. **Dove atterrano le figure.** Una tavola d'ambiente che scavalca le due colonne
   può cadere fra un read-aloud e la sua tabella delle prove. Serve l'elenco dei
   punti in cui la figura **separa cose che vanno lette insieme**.
2. **Read-aloud spezzati.** Un box di prosa che cambia pagina a metà frase si legge
   male ad alta voce. Vanno trovati e segnalati (non necessariamente risolti: la
   soluzione può essere spostare la figura, non il testo).
3. **Vedove e orfane sulle aperture di capitolo**, dove il fregio e il titolo
   flottano in cima.
4. **Il peso**: 7,45 MB di HTML si aprono su un tablet al tavolo? Se no, va detto e
   va proposta l'alternativa (la catena da stampa produce già un PDF da 5,8 MB).

### Sulla guida giocatori (`DRAPPO-BOOKLET-GIOCATORI`)

5. ⚠️ **Spoiler.** È il controllo più importante e il più facile da saltare. La guida
   è `tag: player` e finisce **in mano ai giocatori**: ogni immagine entrata va
   guardata chiedendosi *«questa figura racconta qualcosa che al Giorno 1 non
   devono sapere?»*. Precedente vero: nel Lotto 7 una sezione «Nota per il DM» era
   finita in un booklet giocatori e bruciava i collegamenti fra i segreti.
6. **Le didascalie**: `#figura` usa l'`alt` del markdown come didascalia. Un alt
   scritto per l'accessibilità («Vesca conta le monete davanti al registro falso»)
   diventa una didascalia **che dice troppo**.

### Su entrambi

7. **Le quattro domande del §5 di `PLAYTEST-ALFA`** restano aperte e non vanno
   rifatte: sono per il tavolo, non per il tavolino.

## §3 · Come si esegue

```bash
# 1. le skill: NON si caricano da sole (ADR-0021)
#    - rumblingstone-playtest   (il metodo: passata 1, formato dei rilievi)
#    - rumblingstone-art-direction (se una figura va rifiutata o ritagliata)
#    - rumblingstone-plans      (per chiudere: piano + INDEX + CHANGELOG, stesso commit)

# 2. rigenerare gli oggetti da guardare
cd STANDALONE-Il-Drappo-di-Tarsilia/homebrew
python3 ../../scripts/build_booklet_html.py DRAPPO-BOOKLET-DM.manifest.json --format both
python3 ../../scripts/build_booklet_html.py DRAPPO-BOOKLET-GIOCATORI.manifest.json --format both

# 3. la versione da stampa, che è quella dove l'impaginazione si vede davvero
python3 ../../scripts/export_booklet_typst.py DRAPPO-BOOKLET-DM.manifest.json --all
python3 ../../scripts/export_booklet_typst.py DRAPPO-BOOKLET-GIOCATORI.manifest.json

# 4. GUARDARLE. Non basta che compilino: rendere le pagine in PNG e passarle in rassegna
typst compile --font-path ../../scripts/typst/fonts --root ../.. \
    --format png --ppi 110 DRAPPO-BOOKLET-DM.typ 'pagina{n}.png'   # serve --keep-typ al passo 3
```

> ⚠️ **`typst` non è installato in CI**: l'impaginazione **nessun gate la controlla**.
> Questa passata è l'unico posto in cui viene guardata. Se non la si guarda a occhio,
> non è stata fatta.

## §4 · Cosa NON toccare

- **Il testo dei master**: è collaudato. Se un rilievo richiede di cambiarlo, si
  scrive il rilievo e si chiede al DM — non si riscrive.
- **`scripts/typst/scheda-pg.typ`** e la catena delle schede: già collaudata.
- I file della campagna (`00_`–`09_`, `campaign/`, `Bestiario/`, `PG/`).
- Le due correzioni del §6 di `PLAYTEST-ALFA` (CMD di Ombra, CD di Tesio): sono
  applicate e verificate, non vanno rimesse in discussione.

## §5 · Criteri di accettazione

1. Una tabella di rilievi nel formato della skill — `# · rilievo · gravità · esito`,
   con 🔴/🟠/🟢 — aggiunta come **§7 di `PLAYTEST-ALFA.md`**. **Anche i 🟢 si
   scrivono**: servono a sapere cosa è già stato guardato.
2. Ogni correzione applicata ha le **quattro colonne** del §4 (lettera · cosa cambia ·
   perché, col rilievo che l'ha causata · il file toccato).
3. Zero spoiler nella guida giocatori, **dichiarato per iscritto** — non implicito.
4. `python3 scripts/validate_standalone.py` verde e `check_plans_discipline.py` verde.
5. Riga in `plans/CHANGELOG.md` + riga in `plans/INDEX.md` + checklist del piano,
   **nello stesso commit**.

## §6 · Stato dei rami, per non perdere pezzi

| Ramo | Cosa contiene | PR |
|---|---|---|
| `main` | le sei schede pregenerate | PR #107, **mergiata** |
| `claude/golarion-pathfinder-campaign-xbyvzt` | le venti immagini + il merge di `main` + i booklet rigenerati | PR #108, **aperta** |
| `claude/golarion-pregen-character-sheets-cstheq` | ADR-0021 e la tabella di instradamento delle skill | PR #109, **aperta** |

Il lavoro di questo prompt va fatto **su `xbyvzt` (PR #108)**, che è l'unico ramo
dove immagini, schede e booklet coesistono. Se #108 è già mergiata, si riparte da
`main`.

## §7 · Decisioni già prese, da non ridiscutere

- I ritratti stanno a **1400 px / q88**, come tutte le altre derivate: una taratura
  sola per le venti immagini. Il master PNG a 6 MB resta l'archivio.
- Gli HTML **incorporano** i raster in base64: è il motivo per cui sono autonomi e si
  aprono ovunque. Il peso è il prezzo, accettato consapevolmente.
- Le schede pregenerate hanno una **pagina A4 a testa** e si consegnano **singole**
  (`--per-scheda`): il fascicolo unico brucerebbe i sei segreti insieme.
